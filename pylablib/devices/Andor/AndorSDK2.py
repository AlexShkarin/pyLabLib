from .base import AndorError, AndorTimeoutError, AndorNotSupportedError
from . import atmcd32d_lib
from .atmcd32d_lib import wlib as lib, AndorSDK2LibError
from .atmcd32d_lib import DRV_STATUS
from .atmcd32d_lib import AC_ACQMODE, AC_READMODE, AC_TRIGGERMODE, AC_EMGAIN, AC_FEATURES, AC_GETFUNC, AC_SETFUNC
from .atmcd32d_lib import drAC_CAMERATYPE, AC_PIXELMODE

from ...core.utils import py3
from ...core.devio import interface
from ..interface import camera
from ..utils import load_lib

import numpy as np
import collections
import functools
import threading



class LibraryController(load_lib.LibraryController):
    def _do_uninit(self):
        try:
            self.lib.ShutDown()
        except AndorSDK2LibError as e:
            if e.code!=DRV_STATUS.DRV_NOT_INITIALIZED:
                raise
libctl=LibraryController(lib)
def restart_lib():
    libctl.shutdown()


def get_cameras_number():
    """Get number of connected Andor cameras"""
    libctl.preinit()
    return lib.GetAvailableCameras()


TDeviceInfo=collections.namedtuple("TDeviceInfo",["controller_model","head_model","serial_number"])
TCycleTimings=collections.namedtuple("TCycleTimings",["exposure","accum_cycle_time","kinetic_cycle_time"])
TAcqProgress=collections.namedtuple("TAcqProgress",["frames_done","cycles_done"])

_camsel_lock=threading.RLock()
def _camfunc(*args, **kwargs):
    if len(args)>0:
        return _camfunc(**kwargs)(args[0])
    option=kwargs.get("option",[])
    if not isinstance(option,list):
        option=[option]
    sel=kwargs.get("sel",True)
    setpar=kwargs.get("setpar",None)
    getpar=kwargs.get("getpar",None)
    par_lookup=(getpar is not None) and not option
    if (setpar is not None) and (getpar is not None):
        raise ValueError("a method is either a setpar or a getpar")
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):
            if par_lookup:
                return self._cpar[getpar]
            with _camsel_lock:
                if sel:
                    self._select_camera()
                for opt in option:
                    if not self._check_option(*opt):
                        return
                if getpar is not None:
                    return self._cpar[getpar]
                else:
                    res=func(self,*args,**kwargs)
                    if setpar is not None:
                        self._cpar[setpar]=res
                    return res
        return wrapped
    return wrapper
class AndorSDK2Camera(camera.IBinROICamera, camera.IExposureCamera):
    """
    Andor SDK2 camera.

    Due to the library features, the camera needs to set up all of the parameters to some default values upon connection.
    Most of these parameters are chosen as reasonable defaults: full ROI, minimal exposure time, closed shutter,
    internal trigger, fastest recommended verticals shift speed, no EMCCD gain.
    However, some should be supplied during the connection: temperature setpoint (where appropriate), fan mode, and amplifier mode;
    while there is still a possibility to have default values of these parameters, they might not be appropriate in some settings, and frequently need to be changed.

    Caution: the manufacturer DLL is designed such that if the camera is not closed on the program termination, the allocated resources are never released.
    If this happens, these resources are blocked until the complete OS restart.

    Args:
        idx(int): camera index (use :func:`get_cameras_number` to get the total number of connected cameras)
        ini_path(str): path to .ini file, if required by the camera
        temperature: initial temperature setpoint (in C); can also be ``None`` (select the bottom 20% of the whole range),
            or ``"off"`` (turn the cooler off and set the maximal of the whole range)
        fan_mode: initial fan mode
        amp_mode: initial amplifier mode (a tuple like the one returned by :meth:`get_amp_mode`);
            can also be ``None``, which selects the slowest, smallest gain mode
    """
    _default_image_indexing="rcb"
    Error=AndorError
    TimeoutError=AndorTimeoutError
    def __init__(self, idx=0, ini_path="", temperature=None, fan_mode="off", amp_mode=None):
        super().__init__()
        self.idx=idx
        self.ini_path=ini_path
        self.handle=None
        self._opid=None
        self._minh=0
        self._minv=0
        self._cpar={}
        self._start_temperature=temperature
        self._start_fan_mode=fan_mode
        self._start_amp_mode=amp_mode
        self.open()
        
        self._device_var_ignore_error={"get":(AndorNotSupportedError,),"set":(AndorNotSupportedError,)}
        self._add_info_variable("device_info",self.get_device_info)
        self._add_info_variable("capabilities",self.get_capabilities,priority=-5)
        self._add_info_variable("amp_modes",self.get_all_amp_modes,ignore_error=AndorSDK2LibError,priority=-5)
        self._add_info_variable("pixel_size",self.get_pixel_size)
        self._add_settings_variable("temperature",self.get_temperature_setpoint,self.set_temperature)
        self._add_status_variable("temperature_monitor",self.get_temperature,ignore_error=AndorSDK2LibError)
        self._add_status_variable("temperature_status",self.get_temperature_status,ignore_error=AndorSDK2LibError)
        self._add_settings_variable("cooler",self.is_cooler_on,self.set_cooler,ignore_error=AndorSDK2LibError)
        self._add_status_variable("amp_mode",self.get_amp_mode,ignore_error=AndorSDK2LibError)
        self._add_settings_variable("channel",self.get_channel,lambda x:self.set_amp_mode(channel=x))
        self._add_settings_variable("oamp",self.get_oamp,lambda x:self.set_amp_mode(oamp=x))
        self._add_settings_variable("hsspeed",self.get_hsspeed,lambda x:self.set_amp_mode(hsspeed=x))
        self._add_settings_variable("preamp",self.get_preamp,lambda x:self.set_amp_mode(preamp=x),ignore_error=AndorSDK2LibError)
        self._add_settings_variable("vsspeed",self.get_vsspeed,self.set_vsspeed)
        self._add_settings_variable("EMCCD_gain",self.get_EMCCD_gain,self.set_EMCCD_gain)
        self._add_settings_variable("shutter",self.get_shutter_parameters,self.setup_shutter)
        self._add_settings_variable("fan_mode",self.get_fan_mode,self.set_fan_mode)
        self._add_settings_variable("trigger_mode",self.get_trigger_mode,self.set_trigger_mode)
        self._add_settings_variable("acq_parameters/accum",self.get_accum_mode_parameters,self.setup_accum_mode)
        self._add_settings_variable("acq_parameters/kinetic",self.get_kinetic_mode_parameters,self.setup_kinetic_mode)
        self._add_settings_variable("acq_parameters/fast_kinetic",self.get_fast_kinetic_mode_parameters,self.setup_fast_kinetic_mode)
        self._add_settings_variable("acq_parameters/cont",self.get_cont_mode_parameters,self.setup_cont_mode)
        self._add_settings_variable("acq_mode",self.get_acquisition_mode,self.set_acquisition_mode)
        self._add_status_variable("acq_status",self.get_status)
        self._add_settings_variable("frame_transfer",self.is_frame_transfer_enabled,self.enable_frame_transfer_mode)
        self._add_status_variable("cycle_timings",self.get_cycle_timings)
        self._add_status_variable("readout_time",self.get_readout_time)
        self._add_settings_variable("read_parameters/single_track",self.get_single_track_mode_parameters,self.setup_single_track_mode)
        self._add_settings_variable("read_parameters/multi_track",self.get_multi_track_mode_parameters,self.setup_multi_track_mode)
        self._add_settings_variable("read_parameters/random_track",self.get_random_track_mode_parameters,self.setup_random_track_mode)
        self._add_settings_variable("read_parameters/image",self.get_image_mode_parameters,self.setup_image_mode)
        self._add_settings_variable("read_mode",self.get_read_mode,self.set_read_mode)
        self._update_device_variable_order("exposure")
        self._add_settings_variable("frame_period",self.get_frame_period,self.set_frame_period)
        
    def _initial_setup_temperature(self):
        if self._start_temperature=="off":
            trng=self.get_temperature_range()
            self.set_temperature(trng[1] if trng else 0,enable_cooler=False)
        if self._start_temperature is None:
            trng=self.get_temperature_range()
            if trng:
                self._start_temperature=trng[0]+int((trng[1]-trng[0])*0.2)
            else:
                self._start_temperature=0
            self.set_temperature(self._start_temperature,enable_cooler=True)
    def _initial_setup_ext_trigger(self):
        try:
            lrng=self.get_trigger_level_limits()
            level=(lrng[0]+lrng[1])/2
        except AndorNotSupportedError:
            level=None
        self.setup_ext_trigger(level,False,True)
    def _setup_default_settings(self):
        self.capabilities=self._get_capabilities_n()
        self.device_info=self.get_device_info()
        try:
            self._strict_option_check=False
            self._initial_setup_temperature()
            self.init_amp_mode(mode=self._start_amp_mode)
            self.set_fan_mode(self._start_fan_mode)
            self.setup_shutter("closed")
            self._initial_setup_ext_trigger()
            self.set_trigger_mode("int")
            self.set_exposure(0)
            self.set_acquisition_mode("cont")
            self.setup_accum_mode(1)
            self.setup_kinetic_mode(1)
            self.setup_fast_kinetic_mode(1)
            self.setup_cont_mode()
            self.enable_frame_transfer_mode(False)
            self.setup_single_track_mode()
            self.setup_multi_track_mode()
            self.setup_random_track_mode()
            self._minh=self._find_min_roi_end("h")
            self._minv=self._find_min_roi_end("v")
            self.setup_image_mode()
            self.setup_acquisition("single") # flush the buffers
            self.setup_acquisition("cont")
            self.clear_acquisition()
            self._buffer_size=0
        finally:
            self._strict_option_check=True

    def _select_camera(self):
        if self.handle is None:
            raise AndorError("camera is not opened")
        if lib.GetCurrentCamera()!=self.handle:
            lib.SetCurrentCamera(self.handle)
    def _has_option(self, kind, option):
        if kind=="acq":
            opt=self.capabilities.ulAcqModes
        elif kind=="read":
            opt=self.capabilities.ulReadModes
        elif kind=="trig":
            opt=self.capabilities.ulTriggerModes
        elif kind=="set":
            opt=self.capabilities.ulSetFunctions
        elif kind=="get":
            opt=self.capabilities.ulGetFunctions
        elif kind=="feat":
            opt=self.capabilities.ulFeatures
        else:
            raise AndorError("unknown option kind: {}".format(kind))
        return bool(option&opt)
    def _check_option(self, kind, option):
        has_option=self._has_option(kind,option)
        if (not has_option) and self._strict_option_check:
            raise AndorNotSupportedError("option {}.{} is not supported by {}".format(kind,option,self.device_info.head_model))
        return has_option

    def _get_connection_parameters(self):
        return self.idx,self.ini_path
    def open(self):
        """Open connection to the camera"""
        if self.handle is None:
            ncams=get_cameras_number()
            if self.idx>=ncams:
                raise AndorError("camera index {} is not available ({} cameras exist)".format(self.idx,ncams))
            self.handle=lib.GetCameraHandle(self.idx)
            with self._close_on_error():
                with _camsel_lock:
                    self._select_camera()
                    lib.Initialize(py3.as_builtin_bytes(self.ini_path))
                    self._opid=libctl.open().opid
                self._setup_default_settings()
    def close(self):
        """Close connection to the camera"""
        if self.handle is not None:
            try:
                self.clear_acquisition()
                try:
                    self._select_camera()
                except AndorError:
                    pass
            finally:
                self.handle=None
                libctl.close(self._opid)
                self._opid=None
    def is_opened(self):
        """Check if the device is connected"""
        return self.handle is not None

    @_camfunc
    def get_device_info(self):
        """
        Get camera device info.

        Return tuple ``(controller_mode, head_model, serial_number)``.
        """
        control_model=py3.as_str(lib.GetControllerCardModel())
        head_model=py3.as_str(lib.GetHeadModel())
        serial_number=lib.GetCameraSerialNumber()
        return TDeviceInfo(control_model,head_model,serial_number)
        

    ### Generic controls ###
    _p_status=interface.EnumParameterClass("status",
        {"idle":DRV_STATUS.DRV_IDLE,"acquiring":DRV_STATUS.DRV_ACQUIRING,"temp_cycle":DRV_STATUS.DRV_TEMPCYCLE})
    @_camfunc(option=("feat",AC_FEATURES.AC_FEATURES_POLLING))
    @interface.use_parameters(_returns="status")
    def get_status(self):
        """
        Get camera status.

        Return either ``"idle"`` (no acquisition), ``"acquiring"`` (acquisition in progress) or ``"temp_cycle"`` (temperature cycle in progress).
        """
        status=lib.GetStatus()
        if status not in {DRV_STATUS.DRV_IDLE,DRV_STATUS.DRV_ACQUIRING,DRV_STATUS.DRV_TEMPCYCLE}:
            raise AndorSDK2LibError("GetStatus",status)
        return status
    def acquisition_in_progress(self):
        return self.get_status()=="acquiring"
    def _int_to_enumlst(self, value, enums):
        lst=[]
        for k in enums:
            if value&k:
                lst.append(enums(k).name)
        return lst
    def _parse_capabilities(self, caps):
        cap_dict={}
        cap_dict["acq_mode"]=self._int_to_enumlst(caps.ulAcqModes,AC_ACQMODE)
        cap_dict["read_mode"]=self._int_to_enumlst(caps.ulReadModes,AC_READMODE)
        cap_dict["ft_read_mode"]=self._int_to_enumlst(caps.ulFTReadModes,AC_READMODE)
        cap_dict["trig_mode"]=self._int_to_enumlst(caps.ulTriggerModes,AC_TRIGGERMODE)
        cap_dict["set_func"]=self._int_to_enumlst(caps.ulSetFunctions,AC_SETFUNC)
        cap_dict["get_func"]=self._int_to_enumlst(caps.ulGetFunctions,AC_GETFUNC)
        cap_dict["features"]=self._int_to_enumlst(caps.ulFeatures,AC_FEATURES)
        cap_dict["EM_gain"]=self._int_to_enumlst(caps.ulEMGainCapability,AC_EMGAIN)
        cap_dict["pci_speed"]=int(caps.ulPCICard)
        cap_dict["pix_mode"]=self._int_to_enumlst(caps.ulPixelMode&0xFFFF,AC_PIXELMODE),AC_PIXELMODE(caps.ulPixelMode&0xFFFF0000).name
        cap_dict["cam_type"]=drAC_CAMERATYPE.get(caps.ulCameraType,"UNKNOWN")
        return cap_dict
    @_camfunc
    def _get_capabilities_n(self):
        """Get camera capabilities as a plain ``AndorCapabilities`` structure"""
        return lib.GetCapabilities()
    def get_capabilities(self):
        """
        Get camera capabilities.

        For description of the structure, see Andor SDK manual.
        """
        return self._parse_capabilities(self._get_capabilities_n())
    @_camfunc
    def get_pixel_size(self):
        """Get camera pixel size (in m)"""
        return tuple([s*1E-6 for s in lib.GetPixelSize()])

    ### Cooler controls ###
    @_camfunc(option=("set",AC_SETFUNC.AC_SETFUNCTION_TEMPERATURE))
    def is_cooler_on(self):
        """Check if the cooler is on"""
        return bool(lib.IsCoolerOn())
    @_camfunc(option=("get",AC_GETFUNC.AC_GETFUNCTION_TEMPERATURE))
    def set_cooler(self, on=True):
        """Set the cooler on or off"""
        if on:
            lib.CoolerON()
        else:
            lib.CoolerOFF()
        return self.is_cooler_on()

    
    _p_temp_status=interface.EnumParameterClass("temp_status",{
            "off":DRV_STATUS.DRV_TEMPERATURE_OFF, "not_reached":DRV_STATUS.DRV_TEMPERATURE_NOT_REACHED, "not_stabilized":DRV_STATUS.DRV_TEMPERATURE_NOT_STABILIZED,
            "drifted":DRV_STATUS.DRV_TEMPERATURE_DRIFT, "stabilized":DRV_STATUS.DRV_TEMPERATURE_STABILIZED })
    @_camfunc(option=("get",AC_GETFUNC.AC_GETFUNCTION_TEMPERATURE))
    @interface.use_parameters(_returns="temp_status")
    def get_temperature_status(self):
        """
        Get temperature status.

        Can return ``"off"`` (cooler off), ``"not_reached"`` (cooling in progress), ``"not_stabilized"`` (reached but not stabilized yet),
        ``"stabilized"`` (completely stabilized) or ``"drifted"``.
        """
        return lib.GetTemperatureF()[0]
    @_camfunc(option=("get",AC_GETFUNC.AC_GETFUNCTION_TEMPERATURE))
    def get_temperature(self):
        """Get the current camera temperature (in C)"""
        return lib.GetTemperatureF()[1]
    @_camfunc(setpar="temperature_setpoint",option=[("get",AC_GETFUNC.AC_GETFUNCTION_TEMPERATURERANGE),("set",AC_SETFUNC.AC_SETFUNCTION_TEMPERATURE)])
    def set_temperature(self, temperature, enable_cooler=True):
        """
        Change the temperature setpoint (in C).

        If ``enable_cooler==True``, turn the cooler on automatically.
        """
        rng=lib.GetTemperatureRange()
        temperature=max(temperature,rng[0])
        temperature=min(temperature,rng[1])
        temperature=int(temperature)
        lib.SetTemperature(temperature)
        if enable_cooler:
            self.set_cooler(True)
        return temperature
    @_camfunc(getpar="temperature_setpoint",option=[("set",AC_SETFUNC.AC_SETFUNCTION_TEMPERATURE)])
    def get_temperature_setpoint(self):
        """Get the temperature setpoint (in C)"""
    @_camfunc
    def get_temperature_range(self):
        """Return the available range of temperatures (in C)"""
        return lib.GetTemperatureRange()
    
    ### Amplifiers/shift speeds controls ###
    @_camfunc
    def get_all_amp_modes(self):
        """
        Get all available preamp modes.

        Each preamp mode is characterized by an AD channel index, amplifier index, channel speed (horizontal scan speed) index and preamp gain index.
        Return list of tuples ``(channel, channel_bitdepth, oamp, oamp_kind, hsspeed, hsspeed_MHz, preamp, preamp_gain)``,
        where ``channel``, ``oamp``, ``hsspeed`` and ``preamp`` are indices, while ``channel_bitdepth``, ``oamp_kind``, ``hsspeed_MHz`` and ``preamp_gain`` are descriptions.
        """
        return lib.get_all_amp_modes()
    @_camfunc
    def get_max_vsspeed(self):
        """Get maximal recommended vertical scan speed"""
        return lib.GetFastestRecommendedVSSpeed()[0]
    @_camfunc
    def set_amp_mode(self, channel=None, oamp=None, hsspeed=None, preamp=None):
        """
        Setup preamp mode.

        Can specify AD channel index, amplifier index, channel speed (horizontal scan speed) index and preamp gain index.
        ``None`` (default) means leaving the current value.
        """
        channel=self._cpar["channel"] if channel is None else channel
        oamp=self._cpar["oamp"] if oamp is None else oamp
        hsspeed=self._cpar["hsspeed"] if hsspeed is None else hsspeed
        preamp=self._cpar["preamp"] if preamp is None else preamp
        if not self._has_option("set",AC_SETFUNC.AC_SETFUNCTION_PREAMPGAIN):
            preamp=None
        if not self._has_option("set",AC_SETFUNC.AC_SETFUNCTION_HREADOUT):
            hsspeed=None
        lib.set_amp_mode((channel,oamp,hsspeed,preamp))
        self._cpar["channel"]=channel
        self._cpar["oamp"]=oamp
        self._cpar["hsspeed"]=hsspeed
        self._cpar["preamp"]=preamp
    def get_amp_mode(self, full=True):
        """
        Return the current amplifier mode.
        
        If ``full==True``, return a full description (e.g., actual preamp gain or channel name);
        otherwise, return just the essential indices information (enough to set the mode for this camera, but no explanations).
        """
        mode=atmcd32d_lib.TAmpModeSimple(self.get_channel(),self.get_oamp(),self.get_hsspeed(),self.get_preamp())
        if full:
            mode=lib.get_amp_mode_description(mode)
        return mode
    @_camfunc(setpar="vsspeed",option=[("set",AC_SETFUNC.AC_SETFUNCTION_VREADOUT)])
    def set_vsspeed(self, vsspeed):
        """Set vertical scan speed index"""
        lib.SetVSSpeed(vsspeed)
        return vsspeed

    @_camfunc(getpar="channel")
    def get_channel(self):
        """Get current channel index"""
    @_camfunc
    def get_channel_bitdepth(self, channel=None):
        """Get channel bit depth corresponding to the given channel index (current by default)"""
        return lib.GetBitDepth(self._cpar["channel"] if channel is None else channel)

    @_camfunc(getpar="oamp")
    def get_oamp(self):
        """Get current output amplifier index"""
    @_camfunc
    def get_oamp_desc(self, oamp=None):
        """Get output amplifier kind corresponding to the given oamp index (current by default)"""
        return py3.as_str(lib.GetAmpDesc(self._cpar["oamp"] if oamp is None else oamp))

    @_camfunc(getpar="hsspeed")
    def get_hsspeed(self):
        """Get current horizontal speed index"""
    @_camfunc
    def get_hsspeed_frequency(self, hsspeed=None):
        """Get horizontal scan frequency (in Hz) corresponding to the given hsspeed index (current by default)"""
        return lib.GetHSSpeed(self._cpar["channel"],self._cpar["oamp"],self._cpar["hsspeed"] if hsspeed is None else hsspeed)*1E6
    
    @_camfunc(getpar="preamp")
    def get_preamp(self):
        """Get current preamp index"""
    @_camfunc
    def get_preamp_gain(self, preamp=None):
        """Get preamp gain corresponding to the given preamp index (current by default)"""
        return lib.GetPreAmpGain(self._cpar["preamp"] if preamp is None else preamp)

    @_camfunc(getpar="vsspeed")
    def get_vsspeed(self):
        """Get current vertical speed index"""
    @_camfunc
    def get_vsspeed_period(self, vsspeed=None):
        """Get vertical scan period corresponding to the given vsspeed index (current by default)"""
        return lib.GetVSSpeed(self._cpar["vsspeed"] if vsspeed is None else vsspeed)

    @_camfunc(option=("get",AC_GETFUNC.AC_GETFUNCTION_EMCCDGAIN))
    def get_EMCCD_gain(self):
        """
        Get current EMCCD gain.

        Return tuple ``(gain, advanced)``.
        """
        return lib.get_EMCCD_gain()
    @_camfunc(option=("set",AC_SETFUNC.AC_SETFUNCTION_EMCCDGAIN))
    def set_EMCCD_gain(self, gain, advanced=None):
        """
        Set EMCCD gain.

        Gain goes up to 300 if ``advanced==False`` or higher if ``advanced==True`` (in this mode the sensor can be permanently damaged by strong light).
        """
        gain=int(gain)
        if (advanced is not None) and not self._check_option("set",AC_SETFUNC.AC_SETFUNCTION_EMADVANCED): return
        lib.set_EMCCD_gain(gain,advanced)

    def init_amp_mode(self, mode=None):
        """
        Initialize the camera channel, frequencies and amp settings to some default mode.

        If ``mode`` is supplied, use this mode; otherwise, use the slowest, lowest gain mode (the first one returned by :meth:`get_all_amp_modes`).
        Also set the maximal recommended vertical shift speed and no EMCCD gain.
        """
        mode=mode or self.get_all_amp_modes()[0]
        self.set_amp_mode(mode.channel,mode.oamp,mode.hsspeed,mode.preamp)
        vsspeed=self.get_max_vsspeed()
        self.set_vsspeed(vsspeed)
        try:
            self.set_EMCCD_gain(0,advanced=None)
            self.set_EMCCD_gain(0,advanced=False)
        except AndorNotSupportedError:
            pass

    ### Shutter controls ###
    @_camfunc(option=("feat",AC_FEATURES.AC_FEATURES_SHUTTER))
    def get_min_shutter_times(self):
        """Get minimal shutter opening and closing times"""
        return lib.GetShutterMinTimes()
    _p_shutter_mode=interface.EnumParameterClass("shutter_mode",[("auto",0),("open",1),(True,1),("closed",2),(False,2)],allowed_alias="exact")
    @_camfunc(setpar="shutter",option=("feat",AC_FEATURES.AC_FEATURES_SHUTTER))
    @interface.use_parameters(mode="shutter_mode",_returns=("shutter_mode",None,None,None))
    def setup_shutter(self, mode, ttl_mode=0, open_time=None, close_time=None):
        """
        Setup shutter.

        `mode` can be ``"auto"``, ``"open"`` or ``"closed"``, ttl_mode can be 0 (low is open) or 1 (high is open),
        `open_time` and `close_time` specify opening and closing times (required to calculate the minimal exposure times).
        By default, these time are minimal allowed times.
        """
        min_open_time,min_close_time=self.get_min_shutter_times()
        open_time=min_open_time if open_time is None else open_time
        close_time=min_close_time if close_time is None else close_time
        lib.SetShutter(ttl_mode,mode,open_time,close_time)
        return (mode,ttl_mode,open_time,close_time)
    @_camfunc(getpar="shutter")
    def get_shutter_parameters(self):
        """Return shutter parameters as a tuple ``(mode, ttl_mode, open_time, close_time)``"""
    def get_shutter(self):
        """Get shutter state (``"auto"``, ``"open"``, or ``"closed"``)"""
        return self.get_shutter_parameters()[0]

    ### Misc controls ###
    _p_fan_mode=interface.EnumParameterClass("fan_mode",[("full",0),("low",1),("off",2)])
    @_camfunc(setpar="fan",option=("feat",AC_FEATURES.AC_FEATURES_FANCONTROL))
    @interface.use_parameters(mode="fan_mode",_returns="fan_mode")
    def set_fan_mode(self, mode):
        """
        Set fan mode.

        Can be ``"full"``, ``"low"`` or ``"off"``.
        """
        lib.SetFanMode(mode)
        return mode
    @_camfunc(getpar="fan")
    def get_fan_mode(self):
        """Return fan mode (``"full"``, ``"low"``, or ``"off"``)"""

    @_camfunc
    def read_in_aux_port(self, port):
        """Get state at a given auxiliary port"""
        return lib.InAuxPort(port)
    @_camfunc
    def set_out_aux_port(self, port, state):
        """Set state at a given auxiliary port"""
        return lib.OutAuxPort(port,state)

    ### Trigger controls ###
    _trigger_desc=[
        ("int",0,AC_TRIGGERMODE.AC_TRIGGERMODE_INTERNAL),
        ("ext",1,AC_TRIGGERMODE.AC_TRIGGERMODE_EXTERNAL),
        ("ext_start",6,AC_TRIGGERMODE.AC_TRIGGERMODE_EXTERNALSTART),
        ("ext_exp",7,AC_TRIGGERMODE.AC_TRIGGERMODE_EXTERNALEXPOSURE),
        ("ext_fvb_em",9,AC_TRIGGERMODE.AC_TRIGGERMODE_EXTERNAL_FVB_EM),
        ("software",10,AC_TRIGGERMODE.AC_TRIGGERMODE_INTERNAL),
        ("ext_charge_shift",12,AC_TRIGGERMODE.AC_TRIGGERMODE_EXTERNAL_CHARGESHIFTING),
    ]
    _p_trigger_mode=interface.EnumParameterClass("trigger_mode",{n:v for (n,v,_) in _trigger_desc})
    _trigger_caps={v:c for (_,v,c) in _trigger_desc}
    @_camfunc(setpar="trigger")
    @interface.use_parameters(mode="trigger_mode",_returns="trigger_mode")
    def set_trigger_mode(self, mode):
        """
        Set trigger mode.

        Can be ``"int"`` (internal), ``"ext"`` (external), ``"ext_start"`` (external start), ``"ext_exp"`` (external exposure),
        ``"ext_fvb_em"`` (external FVB EM), ``"software"`` (software trigger) or ``"ext_charge_shift"`` (external charge shifting).

        For description, see Andor SDK manual.
        """
        if not self._check_option("trig",self._trigger_caps[mode]): return
        lib.SetTriggerMode(mode)
        return mode
    @_camfunc(getpar="trigger")
    def get_trigger_mode(self):
        """Return trigger mode"""
    @_camfunc
    def get_trigger_level_limits(self):
        """Get limits on the trigger level"""
        try:
            return lib.GetTriggerLevelRange()
        except AndorSDK2LibError as e:
            if e.code==DRV_STATUS.DRV_NOT_SUPPORTED:
                raise AndorNotSupportedError("setting trigger level is not supported for this camera")
            else:
                raise
    @_camfunc(setpar="ext_trigger")
    def setup_ext_trigger(self, level=None, invert=None, term_highZ=None):
        """
        Setup external trigger (level, inversion, and high-Z termination).
        
        Any ``None`` values are not changed. If any returned values are ``None``, it means that this option is not supported.
        """
        if not self._has_option("trig",AC_TRIGGERMODE.AC_TRIGGERMODE_INVERTED):
            invert=None
        if not self._has_option("set",AC_SETFUNC.AC_SETFUNCTION_TRIGGERTERMINATION):
            term_highZ=None
        try:
            if level is not None:
                lib.SetTriggerLevel(level)
        except AndorSDK2LibError as e:
            if e.code==DRV_STATUS.DRV_NOT_SUPPORTED:
                level=None
            else:
                raise
        if invert is not None:
            lib.SetTriggerInvert(invert)
        if term_highZ is not None:
            lib.SetExternalTriggerTermination(term_highZ)
        curr_vals=self._cpar.get("ext_trigger",(None,None,None))
        level=curr_vals[0] if level is None else level
        invert=curr_vals[1] if invert is None else invert
        term_highZ=curr_vals[2] if term_highZ is None else term_highZ
        return (level,invert,term_highZ)
    @_camfunc(getpar="ext_trigger")
    def get_ext_trigger_parameters(self):
        """
        Return external trigger parameters ``(level, inversion, high-Z termination)``.

        If any returned values are ``None``, it means that this option is not supported.
        """
    @_camfunc
    def send_software_trigger(self):
        """Send software trigger signal"""
        lib.SendSoftwareTrigger()

    ### Acquisition mode controls ###
    _acqmode_desc=[
        ("single",1,AC_ACQMODE.AC_ACQMODE_SINGLE),
        ("accum",2,AC_ACQMODE.AC_ACQMODE_ACCUMULATE),
        ("kinetic",3,AC_ACQMODE.AC_ACQMODE_KINETIC),
        ("fast_kinetic",4,AC_ACQMODE.AC_ACQMODE_FASTKINETICS),
        ("cont",5,AC_ACQMODE.AC_ACQMODE_VIDEO),
    ]
    _p_acq_mode=interface.EnumParameterClass("acq_mode",{n:v for (n,v,_) in _acqmode_desc})
    _acqmode_caps={v:c for (_,v,c) in _acqmode_desc}
    @_camfunc(setpar="acq_mode")
    @interface.use_parameters(mode="acq_mode",_returns="acq_mode")
    def set_acquisition_mode(self, mode, setup_params=True):
        """
        Set the acquisition mode.

        Can be ``"single"``, ``"accum"``, ``"kinetic"``, ``"fast_kinetic"`` or ``"cont"`` (continuous).
        If ``setup_params==True``, make sure that the last specified parameters for this mode are set up.
        For description of each mode, see Andor SDK manual and corresponding ``setup_*_mode`` functions.
        """
        if setup_params and mode in [1,2,3,4]:
            if mode==1:
                self.setup_accum_mode(*self._cpar["acq_params/accum"])
            elif mode==2:
                self.setup_kinetic_mode(*self._cpar["acq_params/kinetic"])
            elif mode==3:
                self.setup_fast_kinetic_mode(*self._cpar["acq_params/fast_kinetic"])
            elif mode==4:
                self.setup_cont_mode(*self._cpar["acq_params/cont"])
        else:
            if not self._check_option("acq",self._acqmode_caps[mode]): return
            lib.SetAcquisitionMode(mode)
        return mode
    @_camfunc(getpar="acq_mode")
    def get_acquisition_mode(self):
        """Get the current acquisition mode"""

    @_camfunc(setpar="acq_params/accum",option=("acq",AC_ACQMODE.AC_ACQMODE_ACCUMULATE))
    def setup_accum_mode(self, num_acc, cycle_time_acc=0):
        """
        Switch into the accum acquisition mode and set up its parameters.
        
        `num_acc` is the number of accumulated frames, `cycle_time_acc` is the acquisition period
        (by default the minimal possible based on exposure and transfer time).
        """
        if self.set_acquisition_mode("accum",setup_params=False) is None: return
        lib.SetNumberAccumulations(num_acc)
        lib.SetAccumulationCycleTime(cycle_time_acc)
        return (num_acc,cycle_time_acc)
    @_camfunc(getpar="acq_params/accum")
    def get_accum_mode_parameters(self):
        """Return accum acquisition mode parameters ``(num_acc, cycle_time_acc)``"""

    @_camfunc(setpar="acq_params/kinetic",option=("acq",AC_ACQMODE.AC_ACQMODE_KINETIC))
    def setup_kinetic_mode(self, num_cycle, cycle_time=0., num_acc=1, cycle_time_acc=0, num_prescan=0):
        """
        Switch into the kinetic acquisition mode and set up its parameters.
        
        `num_cycle` is the number of kinetic cycles frames, `cycle_time` is the acquisition period between accum frames,
        `num_accum` is the number of accumulated frames, `cycle_time_acc` is the accum acquisition period,
        `num_prescan` is the number of prescans.
        """
        if self.set_acquisition_mode("kinetic",setup_params=False) is None: return
        lib.SetNumberKinetics(num_cycle)
        lib.SetNumberAccumulations(num_acc)
        if self._has_option("set",AC_SETFUNC.AC_SETFUNCTION_PRESCANS):
            lib.SetNumberPrescans(num_prescan)
        else:
            num_prescan=0
        lib.SetKineticCycleTime(cycle_time)
        lib.SetAccumulationCycleTime(cycle_time_acc)
        return (num_cycle,cycle_time,num_acc,cycle_time_acc,num_prescan)
    @_camfunc(getpar="acq_params/kinetic")
    def get_kinetic_mode_parameters(self):
        """Return kinetic acquisition mode parameters ``(num_cycle, cycle_time, num_acc, cycle_time_acc, num_prescan)``"""

    @_camfunc(setpar="acq_params/fast_kinetic",option=("acq",AC_ACQMODE.AC_ACQMODE_FASTKINETICS))
    def setup_fast_kinetic_mode(self, num_acc, cycle_time_acc=0.):
        """
        Switch into the fast kinetic acquisition mode and set up its parameters.
        
        `num_acc` is the number of accumulated frames, `cycle_time_acc` is the acquisition period
        (by default the minimal possible based on exposure and transfer time).
        """
        if self.set_acquisition_mode("fast_kinetic",setup_params=False) is None: return
        lib.SetNumberKinetics(num_acc)
        lib.SetAccumulationCycleTime(cycle_time_acc)
        return (num_acc,cycle_time_acc)
    @_camfunc(getpar="acq_params/fast_kinetic")
    def get_fast_kinetic_mode_parameters(self):
        """Return fast kinetic acquisition mode parameters ``(num_acc, cycle_time_acc)``"""

    @_camfunc(setpar="acq_params/cont",option=("acq",AC_ACQMODE.AC_ACQMODE_VIDEO))
    def setup_cont_mode(self, cycle_time=0):
        """
        Switch into the continuous acquisition mode and set up its parameters.
        
        `cycle_time` is the acquisition period (by default the minimal possible based on exposure and transfer time).
        """
        if self.set_acquisition_mode("cont",setup_params=False) is None: return
        lib.SetKineticCycleTime(cycle_time)
        return cycle_time
    @_camfunc(getpar="acq_params/cont")
    def get_cont_mode_parameters(self):
        """Return continuous acquisition mode parameters ``cycle_time``"""

    @_camfunc
    def set_exposure(self, exposure):
        """Set camera exposure"""
        lib.SetExposureTime(exposure)
        return self.get_exposure()
    @_camfunc
    def get_exposure(self):
        """Get current exposure"""
        return self.get_frame_timings()[0]
    def set_frame_period(self, frame_period):
        """Set frame acquisition period for the continuous mode"""
        self.setup_cont_mode(frame_period)
    @_camfunc(setpar="frame_transfer",option=("acq",AC_ACQMODE.AC_ACQMODE_FRAMETRANSFER))
    def enable_frame_transfer_mode(self, enable=True):
        """
        Enable frame transfer mode.

        For description, see Andor SDK manual.
        """
        lib.SetFrameTransferMode(enable)
        return enable
    @_camfunc(getpar="frame_transfer")
    def is_frame_transfer_enabled(self):
        """Return whether the frame transfer mode is enabled"""
    
    @_camfunc
    def get_cycle_timings(self):
        """
        Get acquisition timing.

        Return tuple ``(exposure, accum_cycle_time, kinetic_cycle_time)``.
        In continuous mode, the relevant cycle time is ``kinetic_cycle_time``.
        """
        return TCycleTimings(*lib.GetAcquisitionTimings())
    @_camfunc
    def get_frame_timings(self):
        """
        Get acquisition timing.

        Return tuple ``(exposure, frame_period)``.
        Frame period is the rate of frame generation, not of internal frame acquisition
        (e.g., in accumulator or kinetic mode this is the rate of generating a single accumulated frame, which is ``num_acc`` times larger than the internal frame period).
        """
        cycle_timings=self.get_cycle_timings()
        return self._TAcqTimings(cycle_timings.exposure,cycle_timings.kinetic_cycle_time)
    @_camfunc
    def get_readout_time(self):
        """Get frame readout time"""
        return lib.GetReadOutTime()
    @_camfunc
    def get_keepclean_time(self):
        """Get sensor keep-clean time"""
        return lib.GetKeepCleanTime()


    ### Image settings and transfer controls ###
    _readmode_desc=[
        ("fvb",0,AC_READMODE.AC_READMODE_FVB),
        ("multi_track",1,AC_READMODE.AC_READMODE_MULTITRACK),
        ("random_track",2,AC_READMODE.AC_READMODE_RANDOMTRACK),
        ("single_track",3,AC_READMODE.AC_READMODE_SINGLETRACK),
        ("image",4,AC_READMODE.AC_READMODE_FULLIMAGE),
    ]
    _p_read_mode=interface.EnumParameterClass("read_mode",{n:v for (n,v,_) in _readmode_desc})
    _readmode_caps={v:c for (_,v,c) in _readmode_desc}
    @camera.acqstopped
    @_camfunc(setpar="read_mode")
    @interface.use_parameters(mode="read_mode",_returns="read_mode")
    def set_read_mode(self, mode):
        """
        Set camera read mode.

        Can be ``"fvb"`` (average all image vertically and return it as one row), ``"single_track"`` (read a single row or several rows averaged together),
        ``"multi_track"`` (read multiple rows or averaged sets of rows), ``"random_track"`` (read several arbitrary lines),
        or ``"image"`` (read a whole image or its rectangular part).
        """
        if not self._check_option("read",self._readmode_caps[mode]): return
        lib.SetReadMode(mode)
        return mode
    @_camfunc(getpar="read_mode")
    def get_read_mode(self):
        """Get the current read mode"""

    @camera.acqstopped
    @_camfunc(setpar="read_params/single_track")
    def setup_single_track_mode(self, center=0, width=1):
        """
        Switch into the singe-track read mode and set up its parameters.

        `center` and `width` specify selection of the rows to be averaged together.
        """
        if self.set_read_mode("single_track") is None: return
        lib.SetSingleTrack(center+1,width)
        return (center,width)
    @_camfunc(getpar="read_params/single_track")
    def get_single_track_mode_parameters(self):
        """Return singe-track read mode parameters ``(center, width)``"""

    @camera.acqstopped
    @_camfunc
    def setup_multi_track_mode(self, number=1, height=1, offset=1):
        """
        Switch into the multi-track read mode and set up its parameters.

        `number` is the number of rows (or row sets) to read, `height` is number of one row set (1 for a single row),
        `offset` is the distance between the row sets.
        Return a tuple ``(number, height, offset, top, gap)``, where ``top`` is the offset of the first row from the top, and ``gap`` is the gap between the tracks.
        """
        if self.set_read_mode("multi_track") is None: return
        res=lib.SetMultiTrack(number,height,offset)
        self._cpar["read_params/multi_track"]=(number,height,offset)
        return (number,height,offset)+res
    @_camfunc(getpar="read_params/multi_track")
    def get_multi_track_mode_parameters(self):
        """Return multi-track read mode parameters ``(number, height, offset)``"""
        
    @camera.acqstopped
    @_camfunc(setpar="read_params/random_track")
    def setup_random_track_mode(self, tracks=None):
        """
        Switch into the random-track read mode and set up its parameters.

        `tracks` is a list of tuples ``(start, stop)`` specifying track span (start are inclusive, stop are exclusive, starting from 0).
        Note that it does not affect the current read mode, which should be set using :meth:`set_read_mode`.
        """
        if self.set_read_mode("random_track") is None: return
        tracks=tracks or [(0,1)]
        lib.SetRandomTracks([(t[0]+1,t[1]) for t in tracks])
        return list(tracks)
    @_camfunc(getpar="read_params/random_track")
    def get_random_track_mode_parameters(self):
        """Return random-track read mode parameters, i.e., the list of track positions"""

    @camera.acqstopped
    @_camfunc(setpar="read_params/image")
    def setup_image_mode(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        """
        Switch into the image read mode and set up its parameters.

        `hstart` and `hend` specify horizontal image extent, `vstart` and `vend` specify vertical image extent
        (start are inclusive, stop are exclusive, starting from 0), `hbin` and `vbin` specify binning.
        By default, all non-supplied parameters take extreme values.
        """
        if self.set_read_mode("image") is None: return
        hbin=self._truncate_roi_binning(hbin)
        vbin=self._truncate_roi_binning(vbin)
        hlim,vlim=self.get_roi_limits(hbin=hbin,vbin=vbin)
        hstart,hend,hbin=self._truncate_roi_axis((hstart,hend,hbin),hlim)
        vstart,vend,vbin=self._truncate_roi_axis((vstart,vend,vbin),vlim)
        try:
            lib.SetImage(hbin,vbin,hstart+1,hend,vstart+1,vend)
        except AndorSDK2LibError:
            hbin=vbin=1
            lib.SetImage(hbin,vbin,hstart+1,hend,vstart+1,vend)
        return (hstart,hend,vstart,vend,hbin,vbin)
    @_camfunc(getpar="read_params/image")
    def get_image_mode_parameters(self):
        """Return image read mode parameters, ``(hstart, hend, vstart, vend, hbin, vbin)``"""
    
    @_camfunc(option=("get",AC_GETFUNC.AC_GETFUNCTION_DETECTORSIZE))
    def get_detector_size(self):
        return lib.GetDetector()
    def get_roi(self):
        return self.get_image_mode_parameters()
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        return self.setup_image_mode(hstart,hend,vstart,vend,hbin,vbin)
        
    def _find_min_roi_end(self, kind="h"):
        wdet,hdet=self.get_detector_size()
        if self.set_read_mode("image") is None:
            return
        smin,smax=1,(wdet if kind=="h" else hdet)
        if not self._check_option("read",AC_READMODE.AC_READMODE_SUBIMAGE):
            return smax
        while smin<smax-1:
            smid=(smin+smax)//2
            try:
                if kind=="h":
                    lib.SetImage(1,1,1,smid,1,hdet)
                else:
                    lib.SetImage(1,1,1,wdet,1,smid)
                smax=smid
            except AndorSDK2LibError:
                smin=smid
        lib.SetImage(1,1,1,wdet,1,hdet)
        return smax
    def _truncate_roi_binning(self, binv):
        wdet,hdet=self.get_detector_size()
        maxbin=int(min(wdet//self._minh,hdet//self._minv,32)) if (self._minh and self._minv) else 32
        return max(1,min(binv,maxbin))
    def get_roi_limits(self, hbin=1, vbin=1):
        wdet,hdet=self.get_detector_size()
        maxbin=int(min(wdet//self._minh,hdet//self._minv,32)) if (self._minh and self._minv) else 32
        hlim=camera.TAxisROILimit(self._minh*hbin,wdet,1,hbin,maxbin)
        vlim=camera.TAxisROILimit(self._minv*vbin,hdet,1,vbin,maxbin)
        return hlim,vlim

    def _get_data_dimensions_rc(self):
        mode=self.get_read_mode()
        params=self._cpar.get("read_params/"+mode,None)
        hdet,_=self.get_detector_size()
        if mode in {"fvb","single_track"}:
            return (1,hdet)
        if mode=="multi_track":
            return (params[0],hdet)
        if mode=="random_track":
            return (len(params),hdet)
        if mode=="image":
            (hstart,hend,vstart,vend,hbin,vbin)=params
            return (vend-vstart)//vbin,(hend-hstart)//hbin

    ### Acquisition process controls ###
    @_camfunc
    def setup_acquisition(self, mode=None, nframes=None):  # pylint: disable=arguments-differ
        mode={"snap":"kinetic","sequence":"cont"}.get(mode,mode)
        if mode=="kinetic" and nframes is not None:
            par=self.get_kinetic_mode_parameters()
            self.setup_kinetic_mode(nframes,*par[1:])
        elif mode is not None:
            self.set_acquisition_mode(mode)
        else:
            mode=self.get_acquisition_mode()
        lib.PrepareAcquisition()
        super().setup_acquisition(mode=mode)
    @_camfunc
    def clear_acquisition(self):
        self.stop_acquisition()
        lib.FreeInternalMemory()
        super().clear_acquisition()
    @_camfunc
    def start_acquisition(self, *args, **kwargs):
        self.stop_acquisition()
        super().start_acquisition(*args,**kwargs)
        self._frame_counter.reset(int(self.get_buffer_size()*0.9)) # keep some buffer excess to account fro frames lost while reading / between request and reading
        lib.StartAcquisition()
    @_camfunc
    def stop_acquisition(self):
        if self.acquisition_in_progress():
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
            lib.AbortAcquisition()

    @_camfunc
    def get_acquisition_progress(self):
        """
        Get acquisition progress.

        Return tuple ``(frames_done, acc_done)`` with the number of full transferred frames
        and the number of acquired sub-frames in the current accumulation cycle.
        """
        acc_done,frames_done=lib.GetAcquisitionProgress()
        return TAcqProgress(frames_done,acc_done)
    def _get_acquired_frames(self):
        return self.get_acquisition_progress().frames_done
    
    @_camfunc
    def get_buffer_size(self):
        """Get the size of the image ring buffer"""
        try:
            self._buffer_size=lib.GetSizeOfCircularBuffer()
        except AndorSDK2LibError:
            pass
        return self._buffer_size
    
    @_camfunc
    def _wait_for_next_frame(self, timeout=20., idx=None):
        if timeout is None or timeout>0.1:
            timeout=0.1
        try:
            try:
                _camsel_lock.release()
                lib.WaitForAcquisitionByHandleTimeOut(self.handle,int(timeout*1E3))
            finally:
                _camsel_lock.acquire()
        except AndorSDK2LibError as e:
            if e.code!=DRV_STATUS.DRV_NO_NEW_DATA:
                raise
    @_camfunc
    def _read_frames(self, rng, return_info=False):
        """
        Read and return frames given the range.
        
        The range is always a tuple with at least a single frame in it, and is guaranteed to already be valid.
        Always return tuple ``(frames, infos)``; if ``return_info==False``, ``infos`` value is ignored, so it can be anything (e.g., ``None``).
        """
        dim=self._get_data_dimensions_rc()
        dt=np.dtype(self._default_image_dtype)
        get_method=lib.GetImages16 if dt.itemsize<=2 else lib.GetImages
        data,_,_=get_method(rng[0]+1,rng[1],dim[0]*dim[1]*(rng[1]-rng[0]))
        data=self._convert_indexing(data.reshape((-1,dim[0],dim[1])),"rcb",axes=(1,2))
        return list(data),None

    def _get_grab_acquisition_parameters(self, nframes, buff_size):
        return {"mode":"cont"}