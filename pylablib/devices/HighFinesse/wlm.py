from .wlmData_lib import WlmDataLib, HighFinesseError, WlmDataLibError
from .wlmData_lib import ECtrlMode, EBaseOperation, EGetError, EMeasUnit, ECalibration, EAutocalibration, EEvent
from ...core.devio import interface
from ...core.utils import general

import collections





def muxchannel(*args, **kwargs):
    """Multiplex the function over its channel argument"""
    if len(args)>0:
        return muxchannel(**kwargs)(args[0])
    def ch_func(self, *_, **__):
        return list(range(1,self.get_channels_number(refresh=False)+1))
    return general.muxcall("channel",special_args={"all":ch_func},mux_argnames=kwargs.get("mux_argnames",None),return_kind=kwargs.get("return_kind","list"),allow_partial=True)
TDeviceInfo=collections.namedtuple("TDeviceInfo",["model","serial_number","revision_number","compilation_number"])
class WLM(interface.IDevice):
    """
    Generic HighFinesse wavemeter.

    Args:
        version(int): wavemeter version; if ``None``, use any available version
        dll_path: path to ``wlmData.dll``; if ``None``, use standard locations or search based on the version
        app_path: path to the wavemeter server application (looks like ``wlm_ws.exe`` or ``wlm_ws7.exe``);
            if ``None``, try to autodetect, or rely on the server already running
        autostart: if ``True``, start measurements automatically
            (if the wavemeter server app is not running, it will launch with the measurements stopped).
    """
    Error=HighFinesseError
    _start_timeout=20.
    def __init__(self, version=None, dll_path=None, app_path=None, autostart=True):
        super().__init__()
        self.lib=WlmDataLib()
        self.lib.initlib(dll_path or version)
        self.version=version
        self.dll_path=dll_path or self.lib.dll_path
        self.app_path=app_path or self.lib.app_path
        self.autostart=autostart
        self.dchannel=1
        self.auto_channel_tab=True
        self._channels_number=None
        self._opened=False
        self.open()

        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("measurement_running",self.is_measurement_running)
        self._add_info_variable("channels_number",self.get_channels_number)
        self._add_settings_variable("default_channel",self.get_default_channel,self.set_default_channel)
        self._add_status_variable("frequency",lambda: self.get_frequency(channel="all",error_on_invalid=False))
        self._add_settings_variable("exposure_mode",lambda: self.get_exposure_mode(channel="all"),lambda v: self.set_exposure_mode(v,channel="all"))
        self._add_settings_variable("exposure",lambda: self.get_exposure(sensor="all",channel="all"),lambda v: self.set_exposure(v,sensor="all",channel="all"))
        self._add_settings_variable("switcher_mode",self.get_switcher_mode,self.set_switcher_mode)
        self._add_settings_variable("pulse_mode",self.get_pulse_mode,self.set_pulse_mode)
        self._add_settings_variable("measurement_interval",self.get_measurement_interval,self.set_measurement_interval)
        self._add_status_variable("active_channel",self.get_active_channel)
        self._add_settings_variable("autocalibration",self.get_autocalibration_parameters,self.setup_autocalibration)

    def _get_connection_parameters(self):
        return (self.version,self.dll_path,self.app_path)
    def open(self):
        """Open the connection to the wavemeter"""
        mode=ECtrlMode.cCtrlWLMShow|ECtrlMode.cCtrlWLMWait|ECtrlMode.cCtrlWLMStartSilent|ECtrlMode.cCtrlWLMSilent
        try:
            self.lib.ControlWLMEx(mode,self.app_path or 0,self.version or 0,int(self._start_timeout*1E3),0)
        except (HighFinesseError,OSError):
            raise HighFinesseError("could not start wavemeter server {} for device {}".format(self.app_path or "''",self.version or "N/A"))
        if self.autostart:
            self.start_measurement()
        self._opened=True
    def close(self):
        """Close the connection to the wavemeter"""
        self._opened=False
    def is_opened(self):
        return self._opened

    def get_device_info(self):
        """
        Get the wavemeter info.

        Return tuple ``(model, serial_number, revision_number, compilation_number)``.
        """
        return TDeviceInfo(*[self.lib.GetWLMVersion(i) for i in range(4)])

    def start_measurement(self):
        """Start wavemeter measurement"""
        self.lib.Operation(EBaseOperation.cCtrlStartMeasurement)
    def stop_measurement(self):
        """Stop wavemeter measurement"""
        self.lib.Operation(EBaseOperation.cCtrlStopAll)
    def is_measurement_running(self):
        """Check if the measurement is running"""
        return self.lib.GetOperationState(0)==EBaseOperation.cCtrlStartMeasurement

    def get_channels_number(self, refresh=True):
        """Get number of channels in the wavemeter"""
        if self._channels_number is None or refresh:
            self._channels_number=self.lib.GetChannelsCount(0)
        return self._channels_number
    def _get_channel(self, channel):
        if channel is None:
            return self.dchannel
        chrng=(1,self.get_channels_number(refresh=False))
        if channel<chrng[0] or channel>chrng[1]:
            raise HighFinesseError("invalid channel index {}; must be between {} and {}".format(channel,*chrng))
        return channel
    def get_default_channel(self):
        """Get the default channel (starting from 1) which is used for querying"""
        return self.dchannel
    def set_default_channel(self, channel):
        """Set the default channel (starting from 1) which is used for querying"""
        self.dchannel=self._get_channel(channel)

    _get_error_codes={  EGetError.ErrNoValue:"noval",
                        EGetError.ErrNoSignal:"nosig",
                        EGetError.ErrBadSignal:"badsig",
                        EGetError.ErrLowSignal:"under",
                        EGetError.ErrBigSignal:"over"}
    @muxchannel
    def get_frequency(self, channel=None, error_on_invalid=True):
        """
        Get the wavemeter readings (in Hz) on a given channel.

        `channel` is the measurement channel (starting from 1); if ``None``, use the default channel.
        If ``error_on_invalid==True``, raise an error if the measurement is invalid (e.g., over- or underexposure);
        otherwise, the method can return ``"under"`` if the meter is underexposed or ``"over"`` is it is overexposed,
        ``"badsig"`` if there is no calculable signal, ``"noval"`` if there are no values acquire yet, or ``"nosig"`` if there is no signal.
        """
        try:
            return self.lib.GetFrequencyNum(self._get_channel(channel),0.)*1E12
        except WlmDataLibError as err:
            if (not error_on_invalid) and err.code in self._get_error_codes:
                return self._get_error_codes[err.code]
            raise
    @muxchannel
    def get_wavelength(self, channel=None, error_on_invalid=True):
        """
        Get the wavemeter readings (in m, and in vacuum).

        `channel` is the measurement channel (starting from 1); if ``None``, use the default channel.
        If ``error_on_invalid==True``, raise an error if the measurement is invalid (e.g., over- or underexposure);
        otherwise, the method can return ``"under"`` if the meter is underexposed or ``"over"`` is it is overexposed,
        ``"badsig"`` if there is no calculable signal, or ``"nosig"`` if there is no signal.
        """
        try:
            return self.lib.GetWavelengthNum(self._get_channel(channel),0.)*1E-9
        except WlmDataLibError as err:
            if (not error_on_invalid) and err.code in self._get_error_codes:
                return self._get_error_codes[err.code]
            raise

    _p_exposure_mode=interface.EnumParameterClass("exposure_mode",{"manual":0,"auto":1})
    @muxchannel
    @interface.use_parameters(_returns="exposure_mode")
    def get_exposure_mode(self, channel=None):
        """Get the exposure mode (``"manual"`` or ``"auto"``) at the given channel"""
        return self.lib.GetExposureModeNum(self._get_channel(channel),0)
    @muxchannel(mux_argnames="mode")
    @interface.use_parameters(mode="exposure_mode")
    def set_exposure_mode(self,  mode="auto", channel=None):
        """Set the exposure mode (``"manual"`` or ``"auto"``) at the given channel"""
        self.lib.SetExposureModeNum(self._get_channel(channel),mode)
        return self.get_exposure_mode(channel=channel)

    def _set_channel_tab(self, channel):
        if not self.lib.GetSwitcherMode(0):
            return
        if self.lib.GetChannelsCount(0)<=2:
            return
        channel=self._get_channel(channel)
        par=self.lib.GetSwitcherSignalStates(channel)
        if par[0]:
            self.lib.SetSwitcherSignalStates(channel,1,not par[1])
            self.lib.SetSwitcherSignalStates(channel,1,par[1])
    @muxchannel
    def get_exposure(self, sensor=1, channel=None):
        """Get the exposure for a given channel and sensor (starting from 1)"""
        if sensor=="all":
            e1=self.get_exposure(1,channel=channel)
            try:
                e2=self.get_exposure(2,channel=channel)
                return [e1,e2]
            except WlmDataLibError:
                return [e1]
        else:
            if self.auto_channel_tab:
                self._set_channel_tab(self._get_channel(channel))
            return self.lib.GetExposureNum(self._get_channel(channel),sensor,0)*1E-3
    @muxchannel(mux_argnames="exposure")
    def set_exposure(self, exposure, sensor=1, channel=None):
        """Manually set the exposure for a given channel and sensor (starting from 1)"""
        if sensor=="all":
            if isinstance(exposure,list):
                exps=[]
                for i,e in enumerate(exposure):
                    exps.append(self.set_exposure(e,i+1,channel=channel))
                return exps
            else:
                e1=self.set_exposure(exposure,1,channel=channel)
                try:
                    e2=self.set_exposure(exposure,2,channel=channel)
                    return [e1,e2]
                except WlmDataLibError:
                    return [e1]
        else:
            self.lib.SetExposureNum(self._get_channel(channel),sensor,int(exposure*1E3))
            return self.get_exposure(sensor=sensor,channel=channel)

    _p_switcher_mode=interface.EnumParameterClass("switcher_mode",{"off":0,"on":1})
    @interface.use_parameters(_returns="switcher_mode")
    def get_switcher_mode(self):
        """Get the switcher mode (``"off"`` for manual switching or ``"on"`` for cycling mode)"""
        return self.lib.GetSwitcherMode(0)
    @interface.use_parameters(mode="switcher_mode")
    def set_switcher_mode(self, mode="on"):
        """Set the switcher mode (``"off"`` for manual switching or ``"on"`` for cycling mode)"""
        if self.lib.GetSwitcherMode(0)!=mode:
            self.lib.SetSwitcherMode(mode)
        return self.get_switcher_mode()
    
    def get_active_channel(self):
        """Get the current active channel"""
        return self.lib.GetActiveChannel(1,0)[0]
    def set_active_channel(self, channel, automode=True):
        """
        Set the current switcher channel.
        
        Only makes sense in the manual (``"off"``) switcher mode. If ``automode==True``, switch to this mode automatically.
        """
        if automode:
            self.set_switcher_mode("off")
        return self.lib.SetActiveChannel(1,0,self._get_channel(channel),0)
    
    def _get_switcher_channel_state(self, channel, automode=True):
        if automode:
            self.set_switcher_mode("on")
        return self.lib.GetSwitcherSignalStates(self._get_channel(channel))
    @muxchannel
    def is_switcher_channel_enabled(self, channel, automode=True):
        """
        Check whether the switcher channel enabled.
        
        Only works in the cycling (``"on"``) switcher mode. If ``automode==True``, switch to this mode automatically.
        """
        return self._get_switcher_channel_state(channel,automode=automode)[0]
    @muxchannel
    def is_switcher_channel_shown(self, channel, automode=True):
        """
        Check whether the switcher channel is shown in the wavemeter control application.
        
        Only works in the cycling (``"on"``) switcher mode. If ``automode==True``, switch to this mode automatically.
        """
        return self._get_switcher_channel_state(channel,automode=automode)[1]
    @muxchannel
    def enable_switcher_channel(self, channel, enable=True, show=None, automode=True):
        """
        Enable or disable the current switcher channel in the switch mode.
        
        Only works in the cycling (``"on"``) switcher mode. If ``automode==True``, switch to this mode automatically.
        """
        if automode:
            self.set_switcher_mode("on")
        if show is None:
            show=enable
        self.lib.SetSwitcherSignalStates(self._get_channel(channel),enable,show)


    _p_pulse_mode=interface.EnumParameterClass("pulse_mode",{"cw":0,"int":1,"ext":2,"opt":3})
    @interface.use_parameters(_returns="pulse_mode")
    def get_pulse_mode(self):
        """
        Get the current pulse mode.

        Can be ``"cw"`` (CW laser mode), ``"int"`` (standard single-laser internally triggered mode),
        ``"ext"`` (single- or double-laser mode with external TTL trigger),
        or ``"opt"`` (double-laser mode with optical triggering).
        """
        return self.lib.GetPulseMode(0)
    @interface.use_parameters(mode="pulse_mode")
    def set_pulse_mode(self, mode):
        """
        Set the current pulse mode.

        Can be ``"cw"`` (CW laser mode), ``"int"`` (standard single-laser internally triggered mode),
        ``"ext"`` (single- or double-laser mode with external TTL trigger),
        or ``"opt"`` (double-laser mode with optical triggering).
        """
        self.lib.SetPulseMode(mode)
        return self.get_pulse_mode()
    _p_precision_mode=interface.EnumParameterClass("precision_mode",{"fine":0,"wide":1,"grating":2})
    @interface.use_parameters(_returns="precision_mode")
    def get_precision_mode(self):
        """Set the current precision mode (``"fine"``, ``"wide"``, or ``"grating"``)"""
        return self.lib.GetWideMode(0)
    @interface.use_parameters(mode="precision_mode")
    def set_precision_mode(self, mode):
        """Set the current precision mode (``"fine"``, ``"wide"``, or ``"grating"``)"""
        self.lib.SetWideMode(mode)
        return self.get_precision_mode()
    
    def get_measurement_interval(self):
        """Set measurement interval (per channel), or ``None`` if the interval mode is off"""
        if self.lib.GetIntervalMode(0)==0:
            return None
        return self.lib.GetInterval(0)*1E-3
    def set_measurement_interval(self, interval=None):
        """
        Set measurement interval (per channel).

        ``None`` means that the interval mode is off.
        """
        if interval is None:
            self.lib.SetIntervalMode(0)
        else:
            self.lib.SetIntervalMode(1)
            self.lib.SetInterval(int(interval*1000))

    _p_cal_source_type=interface.EnumParameterClass("cal_source_type",
        {"hene_633":ECalibration.cHeNe633,"hene_1152":ECalibration.cHeNe1152,"hene_free":ECalibration.cFreeHeNe,"nel":ECalibration.cNeL,"other":ECalibration.cOther})
    @interface.use_parameters(source_type="cal_source_type")
    def calibrate(self, source_type, source_frequency, channel=None):
        """
        Initialize the calibration.

        `source_type` is the calibration source type, which can be ``"hene_633"`` (HeNe 633nm laser), ``"hene_1152"`` (HeNe 1152nm laser),
        ``"hene_free"`` (free-running HeNe laser), ``"nel"`` (Ne lamp), or ``"other"`` (other source).
        `source_frequency` is the exact source frequency (in Hz) sent through the given `channel`.
        """
        self.lib.Calibration(source_type,EMeasUnit.cReturnFrequency,source_frequency,self._get_channel(channel))
    

    _p_autocal_unit=interface.EnumParameterClass("autocal_unit",
        {"start":EAutocalibration.cACOnceOnStart,"meas":EAutocalibration.cACMeasurements,
        "min":EAutocalibration.cACMinutes,"hour":EAutocalibration.cACHours,"day":EAutocalibration.cACDays})
    @interface.use_parameters(_returns=(None,"autocal_unit",None))
    def get_autocalibration_parameters(self):
        """
        Get up the automatic calibration parameters.

        Return tuple ``(enable, unit, period)``, where ``enable`` determines if it is enabled,
        and ``unit`` and ``period`` together specify the calibration period.
        ``unit`` can be ``"start"`` (once on the measurement start; ``period`` is irrelevant here),
        ``"meas"`` (once every ``period`` frequency measurements),
        ``"min"`` (once every ``period`` minutes), ``"hours"``, or ``"days"``.
        """
        enable=self.lib.GetAutoCalMode(0)
        unit=self.lib.GetAutoCalSetting(EEvent.cmiAutoCalUnit,0)[1]
        period=self.lib.GetAutoCalSetting(EEvent.cmiAutoCalPeriod,0)[1]
        return (bool(enable),unit,period)

    @interface.use_parameters(unit="autocal_unit")
    def setup_autocalibration(self, enable=True, unit=None, period=None):
        """
        Set up the automatic calibration parameters.

        `enable` determines if it is enabled.
        `unit` and `period` together specify the calibration period.
        `unit` can be ``"start"`` (once on the measurement start; `period` is irrelevant here),
        ``"meas"`` (once every `period` frequency measurements),
        ``"min"`` (once every `period` minutes), ``"hours"``, or ``"days"``.
        Any ``None`` parameters are kept at the present value.
        """
        if not enable:
            self.lib.SetAutoCalMode(0)
        if unit is not None:
            self.lib.SetAutoCalSetting(EEvent.cmiAutoCalUnit,unit,0,0)
        if period is not None:
            if self.lib.GetAutoCalSetting(EEvent.cmiAutoCalUnit,0)[1]!=EAutocalibration.cACOnceOnStart:
                self.lib.SetAutoCalSetting(EEvent.cmiAutoCalPeriod,period,0,0)
        if enable:
            self.lib.SetAutoCalMode(1)
        return self.get_autocalibration_parameters()