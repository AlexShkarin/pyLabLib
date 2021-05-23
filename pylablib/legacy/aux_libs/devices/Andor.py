from .Andor_lib import lib, AndorLibError
from .AndorSDK3_lib import lib as lib3, AndorSDK3LibError, AndorSDK3_feature_types, nb_read_uint12, read_uint12

from ...core.devio import data_format
from ...core.devio.interface import IDevice
from ...core.utils import funcargparse, py3, dictionary, strpack, general
from ...core.dataproc import image as image_utils

_depends_local=[".Andor_lib",".AndorSDK3_lib","...core.devio.interface"]

import numpy as np
import collections
import contextlib
import ctypes
import threading
import time

class AndorError(RuntimeError):
    "Generic Andor camera error."
class AndorTimeoutError(AndorError):
    "Timeout while waiting."
class AndorNotSupportedError(AndorError):
    "Option not supported."

def get_cameras_number():
    """Get number of connected Andor cameras"""
    lib.initlib()
    return lib.GetAvailableCameras()

class AndorCamera(IDevice):
    """
    Andor camera.

    Caution: the manufacturer DLL is designed such that if the camera is not closed on the program termination, the allocated resources are never released.
    If this happens, these resources are blocked until the complete OS restart.

    Args:
        idx(int): camera index (use :func:`get_cameras_number` to get the total number of connected cameras)
        ini_path(str): path to .ini file, if required by the camera
    """
    def __init__(self, idx=0, ini_path=""):
        IDevice.__init__(self)
        lib.initlib()
        self.idx=idx
        self.ini_path=ini_path
        self.handle=None
        self._minh=0
        self._minv=0
        self.open()
        self.image_indexing="rct"
        
        self._nodes_ignore_error={"get":(AndorNotSupportedError,),"set":(AndorNotSupportedError,)}
        self._add_full_info_node("model_data",self.get_model_data)
        self._add_full_info_node("capabilities",self.get_capabilities)
        self._add_full_info_node("amp_modes",self.get_all_amp_modes,ignore_error=AndorLibError)
        self._add_full_info_node("pixel_size",self.get_pixel_size)
        self._add_settings_node("temperature",self.get_temperature_setpoint,self.set_temperature)
        self._add_status_node("temperature_monitor",self.get_temperature,ignore_error=AndorLibError)
        self._add_status_node("temperature_status",self.get_temperature_status,ignore_error=AndorLibError)
        self._add_settings_node("cooler",self.is_cooler_on,self.set_cooler,ignore_error=AndorLibError)
        self._add_settings_node("channel",lambda:self.channel,lambda x:self.set_amp_mode(channel=x))
        self._add_settings_node("oamp",lambda:self.oamp,lambda x:self.set_amp_mode(oamp=x))
        self._add_settings_node("hsspeed",lambda:self.hsspeed,lambda x:self.set_amp_mode(hsspeed=x))
        self._add_settings_node("preamp",lambda:self.preamp,lambda x:self.set_amp_mode(preamp=x),ignore_error=AndorLibError)
        self._add_settings_node("vsspeed",lambda:self.vsspeed,self.set_vsspeed)
        self._add_settings_node("EMCCD_gain",lambda:self.EMCCD_gain,self.set_EMCCD_gain)
        self._add_settings_node("shutter",lambda:self.shutter_mode,self.set_shutter)
        self._add_settings_node("fan_mode",lambda:self.fan_mode,self.set_fan_mode)
        self._add_settings_node("trigger_mode",lambda:self.trigger_mode,self.set_trigger_mode)
        self._add_settings_node("acq_parameters/accum",lambda:self.acq_params["accum"],self.setup_accum_mode)
        self._add_settings_node("acq_parameters/kinetics",lambda:self.acq_params["kinetics"],self.setup_kinetic_mode)
        self._add_settings_node("acq_parameters/fast_kinetics",lambda:self.acq_params["fast_kinetics"],self.setup_fast_kinetic_mode)
        self._add_settings_node("acq_parameters/cont",lambda:self.acq_params["cont"],self.setup_cont_mode)
        self._add_settings_node("acq_mode",lambda:self.acq_mode,self.set_acquisition_mode)
        self._add_status_node("acq_status",self.get_status)
        self._add_settings_node("frame_transfer",lambda:self.frame_transfer_mode,self.enable_frame_transfer_mode)
        self._add_settings_node("exposure",self.get_exposure,self.set_exposure)
        self._add_status_node("timings",self.get_timings)
        self._add_status_node("readout_time",self.get_readout_time)
        self._add_settings_node("read_parameters/single_track",lambda:self.read_params["single_track"],self.setup_single_track_mode)
        self._add_settings_node("read_parameters/multi_track",lambda:self.read_params["multi_track"],self.setup_multi_track_mode)
        self._add_settings_node("read_parameters/random_track",lambda:self.read_params["random_track"],self.setup_random_track_mode)
        self._add_settings_node("read_parameters/image",lambda:self.read_params["image"],self.setup_image_mode)
        self._add_settings_node("roi",self.get_roi,self.set_roi)
        self._add_status_node("roi_limits",self.get_roi_limits)
        self._add_settings_node("read_mode",lambda:self.read_mode,self.set_read_mode)
        self._add_status_node("data_dimensions",self.get_data_dimensions)
        self._add_status_node("buffer_size",self.get_buffer_size)
        self._add_full_info_node("detector_size",self.get_detector_size)

    def _setup_default_settings(self):
        self.capabilities=self.get_capabilities()
        self.model_data=self.get_model_data()
        try:
            self._strict_option_check=False
            self.temperature_setpoint=None
            self.set_temperature(-100)
            self.channel=None
            self.oamp=None
            self.hsspeed=None
            self.preamp=None
            self.vsspeed=None
            self.init_speeds()
            self.EMCCD_gain=None
            self.set_EMCCD_gain(0)
            self.set_EMCCD_gain(0,False)
            self.fan_mode=None
            self.set_fan_mode("off")
            self.shutter_mode=None
            self.set_shutter("close")
            self.trigger_mode=None
            self.set_trigger_mode("int")
            self.set_exposure(10E-3)
            self.acq_mode=None
            self.set_acquisition_mode("cont")
            self.acq_params=dict(zip(self._acq_modes,[()]*len(self._acq_modes)))
            self.setup_accum_mode(1)
            self.setup_kinetic_mode(1)
            self.setup_fast_kinetic_mode(1)
            self.setup_cont_mode()
            self.frame_transfer_mode=None
            self.enable_frame_transfer_mode(False)
            self.read_mode=None
            self.set_read_mode("image")
            self.read_params=dict(zip(self._read_modes,[()]*len(self._read_modes)))
            self.setup_image_mode()
            self.setup_single_track_mode()
            self.setup_multi_track_mode()
            self.setup_random_track_mode()
            self.flush_buffer()
            self.last_buffer_size=0
            self.get_buffer_size()
            self._minh=self._find_min_roi_end("h")
            self._minv=self._find_min_roi_end("v")
        finally:
            self._strict_option_check=True

    def _camsel(self):
        if self.handle is None:
            raise AndorError("camera is not opened")
        if lib.GetCurrentCamera()!=self.handle:
            lib.SetCurrentCamera(self.handle)
    def _has_option(self, kind, option):
        if kind=="acq":
            opt=self.capabilities.AcqModes
        elif kind=="read":
            opt=self.capabilities.ReadModes
        elif kind=="trig":
            opt=self.capabilities.TriggerModes
        elif kind=="set":
            opt=self.capabilities.SetFunctions
        elif kind=="get":
            opt=self.capabilities.GetFunctions
        elif kind=="feat":
            opt=self.capabilities.Features
        else:
            raise AndorError("unknown option kind: {}".format(kind))
        return option in opt
    def _check_option(self, kind, option):
        has_option=self._has_option(kind,option)
        if (not has_option) and self._strict_option_check:
            raise AndorNotSupportedError("option {}.{} is not supported by {}".format(kind,option,self.model_data.head_model))
        return has_option
    def open(self):
        """Open connection to the camera"""
        ncams=get_cameras_number()
        if self.idx>=ncams:
            raise AndorError("camera index {} is not available ({} cameras exist)".format(self.idx,ncams))
        self.handle=lib.GetCameraHandle(self.idx)
        self._camsel()
        lib.Initialize(py3.as_builtin_bytes(self.ini_path))
        self._setup_default_settings()
    def close(self):
        """Close connection to the camera"""
        try:
            self._camsel()
        except AndorError:
            return
        try:
            lib.ShutDown()
        except AndorLibError as e:
            if e.text_code!="DRV_NOT_INITIALIZED":
                raise
        self.handle=None
    def is_opened(self):
        """Check if the device is connected"""
        return self.handle is not None

    ModelData=collections.namedtuple("ModelData",["controller_model","head_model","serial_number"])
    def get_model_data(self):
        """
        Get camera model data.

        Return tuple ``(controller_mode, head_model, serial_number)``.
        """
        self._camsel()
        control_model=py3.as_str(lib.GetControllerCardModel())
        head_model=py3.as_str(lib.GetHeadModel())
        serial_number=lib.GetCameraSerialNumber()
        return self.ModelData(control_model,head_model,serial_number)
        

    ### Generic controls ###
    def get_status(self):
        """
        Get camera status.

        Return either ``"idle"`` (no acquisition), ``"acquiring"`` (acquisition in progress) or ``"temp_cycle"`` (temperature cycle in progress).
        """
        self._camsel()
        if not self._check_option("feat","AC_FEATURES_POLLING"): return
        status=lib.GetStatus()
        text_status=lib.Andor_statuscodes[status]
        if text_status=="DRV_IDLE":
            return "idle"
        if text_status=="DRV_TEMPCYCLE":
            return "temp_cycle"
        if text_status=="DRV_ACQUIRING":
            return "acquiring"
        raise AndorLibError("GetStatus",status)
    def get_capabilities(self):
        """
        Get camera capabilities.

        For description of the structure, see Andor SDK manual.
        """
        self._camsel()
        return lib.GetCapabilities()
    def get_pixel_size(self):
        """Get camera pixel size (in m)"""
        self._camsel()
        return (s*1E-6 for s in lib.GetPixelSize())

    ### Cooler controls ###
    def is_cooler_on(self):
        """Check if the cooler is on"""
        self._camsel()
        if not self._check_option("set","AC_SETFUNCTION_TEMPERATURE"): return
        return bool(lib.IsCoolerOn())
    def set_cooler(self, on=True):
        """Set the cooler on or off"""
        self._camsel()
        if not self._check_option("get","AC_GETFUNCTION_TEMPERATURE"): return
        if on:
            lib.CoolerON()
        else:
            lib.CoolerOFF()
    _temp_status={"DRV_TEMPERATURE_OFF":"off","DRV_TEMPERATURE_NOT_REACHED":"not_reached","DRV_TEMPERATURE_NOT_STABILIZED":"not_stabilized",
                    "DRV_TEMPERATURE_DRIFT":"drifted","DRV_TEMPERATURE_STABILIZED":"stabilized",}
    def get_temperature_status(self):
        """
        Get temperature status.

        Can return ``"off"`` (cooler off), ``"not_reached"`` (cooling in progress), ``"not_stabilized"`` (reached but not stabilized yet),
        ``"stabilized"`` (completely stabilized) or ``"drifted"``.
        """
        self._camsel()
        if not self._check_option("get","AC_GETFUNCTION_TEMPERATURE"): return
        status=lib.GetTemperature()[1]
        return self._temp_status[status]
    def get_temperature(self):
        """Get the current camera temperature"""
        self._camsel()
        if not self._check_option("get","AC_GETFUNCTION_TEMPERATURE"): return
        return lib.GetTemperatureF()[0]
    def set_temperature(self, temperature, enable_cooler=True):
        """
        Change the temperature setpoint.

        If ``enable_cooler==True``, turn the cooler on automatically.
        """
        self._camsel()
        if not self._check_option("set","AC_SETFUNCTION_TEMPERATURE"): return
        if not self._check_option("get","AC_GETFUNCTION_TEMPERATURERANGE"): return
        rng=lib.GetTemperatureRange()
        temperature=max(temperature,rng[0])
        temperature=min(temperature,rng[1])
        self.temperature_setpoint=int(temperature)
        lib.SetTemperature(self.temperature_setpoint)
        if enable_cooler:
            self.set_cooler(True)
    def get_temperature_setpoint(self):
        return self.temperature_setpoint
    
    ### Amplifiers/shift speeds controls ###
    def get_all_amp_modes(self):
        """
        Get all available pream modes.

        Each preamp mode is characterized by an AD channel index, amplifier index, channel speed (horizontal scan speed) index and preamp gain index.
        Return list of tuples ``(channel, channel_bitdepth, oamp, oamp_kind, hsspeed, hsspeed_MHz, preamp, preamp_gain)``,
        where ``channel``, ``oamp``, ``hsspeed`` and ``preamp`` are indices, while ``channel_bitdepth``, ``oamp_kind``, ``hsspeed_MHz`` and ``preamp_gain`` are descriptions.
        """
        self._camsel()
        return lib.get_all_amp_modes()
    def get_max_vsspeed(self):
        """Get  maximal recommended vertical scan speed"""
        self._camsel()
        return lib.GetFastestRecommendedVSSpeed()[0]
    def set_amp_mode(self, channel=None, oamp=None, hsspeed=None, preamp=None):
        """
        Setup preamp mode.

        Can specify AD channel index, amplifier index, channel speed (horizontal scan speed) index and preamp gain index.
        ``None`` (default) means leaving the current value.
        """
        self._camsel()
        channel=self.channel if channel is None else channel
        oamp=self.oamp if oamp is None else oamp
        hsspeed=self.hsspeed if hsspeed is None else hsspeed
        preamp=self.preamp if preamp is None else preamp
        if not self._has_option("set","AC_SETFUNCTION_PREAMPGAIN"):
            preamp=None
        if not self._has_option("set","AC_SETFUNCTION_HREADOUT"):
            hsspeed=None
        lib.set_amp_mode((channel,oamp,hsspeed,preamp))
        self.channel=channel
        self.oamp=oamp
        self.hsspeed=hsspeed
        self.preamp=preamp
    def set_vsspeed(self, vsspeed):
        """Set vertical scan speed index"""
        self._camsel()
        if not self._check_option("set","AC_SETFUNCTION_VREADOUT"): return
        lib.SetVSSpeed(vsspeed)
        self.vsspeed=vsspeed

    def get_channel_bitdepth(self, channel=None):
        """Get channel bit depth corresponding to the given channel index (current by default)"""
        self._camsel()
        return lib.GetBitDepth(self.channel if channel is None else channel)
    def get_oamp_desc(self, oamp=None):
        """Get output amplifier kind corresponding to the given oamp index (current by default)"""
        return lib._oamp_kinds[self.oamp if oamp is None else oamp]
    def get_hsspeed_frequency(self, hsspeed=None):
        """Get horizontal scan frequency (in Hz) corresponding to the given hsspeed index (current by default)"""
        self._camsel()
        return lib.GetHSSpeed(self.channel,self.oamp,self.hsspeed if hsspeed is None else hsspeed)*1E6
    def get_preamp_gain(self, preamp=None):
        """Get preamp gain corresponding to the given preamp index (current by default)"""
        self._camsel()
        return lib.GetPreAmpGain(self.preamp if preamp is None else preamp)
    def get_vsspeed_period(self, vsspeed=None):
        """Get vertical scan period corresponding to the given vsspeed index (current by default)"""
        self._camsel()
        return lib.GetVSSpeed(self.vsspeed if vsspeed is None else vsspeed)

    def get_EMCCD_gain(self):
        """
        Get current EMCCD gain.

        Return tuple ``(gain, advanced)``.
        """
        self._camsel()
        if not self._check_option("get","AC_GETFUNCTION_EMCCDGAIN"): return
        return lib.get_EMCCD_gain()
    def set_EMCCD_gain(self, gain, advanced=None):
        """
        Set EMCCD gain.

        Gain goes up to 300 if ``advanced==False`` or higher if ``advanced==True`` (in this mode the sensor can be permanently damaged by strong light).
        """
        self._camsel()
        gain=int(gain)
        if not self._check_option("set","AC_SETFUNCTION_EMCCDGAIN"): return
        if (advanced is not None) and not self._check_option("set","AC_SETFUNCTION_EMADVANCED"): return
        lib.set_EMCCD_gain(gain,advanced)
        self.EMCCD_gain=(gain,advanced)

    def init_speeds(self):
        """Initialize the camera channel, frequencies and amp settings to some default mode"""
        mode=self.get_all_amp_modes()[0]
        self.set_amp_mode(mode.channel,mode.oamp,mode.hsspeed,mode.preamp)
        vsspeed=self.get_max_vsspeed()
        self.set_vsspeed(vsspeed)
        self.set_EMCCD_gain(0,advanced=False)

    ### Shutter controls ###
    def get_min_shutter_times(self):
        """Get minimal shutter opening and closing times"""
        self._camsel()
        if not self._check_option("feat","AC_FEATURES_SHUTTER"): return
        return lib.GetShutterMinTimes()
    def set_shutter(self, mode, ttl_mode=0, open_time=None, close_time=None):
        """
        Setup shutter.

        `mode` can be ``"auto"``, ``"open"`` or ``"close"``, ttl_mode can be 0 (low is open) or 1 (high is open),
        `open_time` and `close_time` specify opening and closing times (required to calculate the minimal exposure times).
        By default, these time are minimal allowed times.
        """
        self._camsel()
        if not self._check_option("feat","AC_FEATURES_SHUTTER"): return
        if mode in [0,False]:
            mode="close"
        if mode in [1,True]:
            mode="open"
        shutter_modes=["auto","open","close"]
        funcargparse.check_parameter_range(mode,"state",shutter_modes)
        min_open_time,min_close_time=self.get_min_shutter_times()
        open_time=min_open_time if open_time is None else open_time
        close_time=min_close_time if close_time is None else close_time
        lib.SetShutter(ttl_mode,shutter_modes.index(mode),open_time,close_time)
        self.shutter_mode=mode

    ### Misc controls ###
    def set_fan_mode(self, mode):
        """
        Set fan mode.

        Can be ``"full"``, ``"low"`` or ``"off"``.
        """
        self._camsel()
        if not self._check_option("feat","AC_FEATURES_FANCONTROL"): return
        text_modes=["full","low","off"]
        funcargparse.check_parameter_range(mode,"mode",text_modes)
        lib.SetFanMode(text_modes.index(mode))
        self.fan_mode=mode

    def read_in_aux_port(self, port):
        """Get state at a given auxiliary port"""
        self._camsel()
        return lib.InAuxPort(port)
    def set_out_aux_port(self, port, state):
        """Set state at a given auxiliary port"""
        self._camsel()
        return lib.OutAuxPort(port,state)

    ### Trigger controls ###
    def set_trigger_mode(self, mode):
        """
        Set trigger mode.

        Can be ``"int"`` (internal), ``"ext"`` (external), ``"ext_start"`` (external start), ``"ext_exp"`` (external exposure),
        ``"ext_fvb_em"`` (external FVB EM), ``"software"`` (software trigger) or ``"ext_charge_shift"`` (external charge shifting).

        For description, see Andor SDK manual.
        """
        trigger_modes={"int":0,"ext":1,"ext_start":6,"ext_exp":7,"ext_fvb_em":9,"software":10,"ext_charge_shift":12}
        trigger_modes_cap={"int":"AC_TRIGGERMODE_INTERNAL","ext":"AC_TRIGGERMODE_EXTERNAL",
            "ext_start":"AC_TRIGGERMODE_EXTERNALSTART","ext_exp":"AC_TRIGGERMODE_EXTERNALEXPOSURE",
            "ext_fvb_em":"AC_TRIGGERMODE_EXTERNAL_FVB_EM","software":"AC_TRIGGERMODE_INTERNAL"}
        funcargparse.check_parameter_range(mode,"mode",trigger_modes.keys())
        self._camsel()
        if not self._check_option("trig",trigger_modes_cap[mode]): return
        lib.SetTriggerMode(trigger_modes[mode])
        self.trigger_mode=mode
    def get_trigger_level_limits(self):
        """Get limits on the trigger level"""
        self._camsel()
        return lib.GetTriggerLevelRange()
    def setup_ext_trigger(self, level, invert, term_highZ=True):
        """Setup external trigger (level, inversion, and high-Z termination)"""
        self._camsel()
        lib.SetTriggerLevel(level)
        lib.SetTriggerInvert(invert)
        lib.SetExternalTriggerTermination(term_highZ)
    def send_software_trigger(self):
        """Send software trigger signal"""
        self._camsel()
        lib.SendSoftwareTrigger()

    ### Acquisition mode controls ###
    _acq_modes={"single":1,"accum":2,"kinetics":3,"fast_kinetics":4,"cont":5}
    _acq_modes_cap={"single":"AC_ACQMODE_SINGLE", "accum":"AC_ACQMODE_ACCUMULATE",
        "kinetics":"AC_ACQMODE_KINETIC", "fast_kinetics":"AC_ACQMODE_FASTKINETICS",
        "cont":"AC_ACQMODE_VIDEO"}
    def set_acquisition_mode(self, mode):
        """
        Set acquisition mode.

        Can be ``"single"``, ``"accum"``, ``"kinetics"``, ``"fast_kinetics"`` or ``"cont"`` (continuous).
        For description of each mode, see Andor SDK manual and corresponding setup_*_mode functions.
        """
        funcargparse.check_parameter_range(mode,"mode",self._acq_modes.keys())
        self._camsel()
        if not self._check_option("acq",self._acq_modes_cap[mode]): return
        lib.SetAcquisitionMode(self._acq_modes[mode])
        self.acq_mode=mode
    def setup_accum_mode(self, num, cycle_time=0):
        """
        Setup accum acquisition mode.
        
        `num` is the number of accumulated frames, `cycle_time` is the acquisition period
        (by default the minimal possible based on exposure and transfer time).
        """
        self._camsel()
        if not self._check_option("acq","AC_ACQMODE_ACCUMULATE"): return
        self.set_acquisition_mode("accum")
        lib.SetNumberAccumulations(num)
        lib.SetAccumulationCycleTime(cycle_time)
        self.acq_params["accum"]=(num,cycle_time)
    def setup_kinetic_mode(self, num, cycle_time=0., num_acc=1, cycle_time_acc=0, num_prescan=0):
        """
        Setup kinetic acquisition mode.
        
        `num` is the number of kinetic cycles frames, `cycle_time` is the acquisition period between accum frames,
        `num_accum` is the number of accumulated frames, `cycle_time_acc` is the accum acquisition period,
        `num_prescan` is the number of prescans.
        """
        self._camsel()
        if not self._check_option("acq","AC_ACQMODE_KINETIC"): return
        self.set_acquisition_mode("kinetics")
        lib.SetNumberKinetics(num)
        lib.SetNumberAccumulations(num_acc)
        lib.SetNumberPrescans(num_prescan)
        lib.SetKineticCycleTime(cycle_time)
        lib.SetAccumulationCycleTime(cycle_time_acc)
        self.acq_params["kinetics"]=(num,cycle_time,num_acc,cycle_time_acc,num_prescan)
    def setup_fast_kinetic_mode(self, num, cycle_time_acc=0.):
        """
        Setup fast kinetic acquisition mode.
        
        `num` is the number of accumulated frames, `cycle_time` is the acquisition period
        (by default the minimal possible based on exposure and transfer time).
        """
        self._camsel()
        if not self._check_option("acq","AC_ACQMODE_FASTKINETICS"): return
        self.set_acquisition_mode("fast_kinetics")
        lib.SetNumberKinetics(num)
        lib.SetAccumulationCycleTime(cycle_time_acc)
        self.acq_params["fast_kinetics"]=(num,cycle_time_acc)
    def setup_cont_mode(self, cycle_time=0):
        """
        Setup continuous acquisition mode.
        
        `cycle_time` is the acquisition period (by default the minimal possible based on exposure and transfer time).
        """
        self._camsel()
        if not self._check_option("acq","AC_ACQMODE_VIDEO"): return
        self.set_acquisition_mode("cont")
        lib.SetKineticCycleTime(cycle_time)
        self.acq_params["cont"]=cycle_time
    def _setup_acquisition(self, acq_mode=None, params=None):
        acq_mode=acq_mode or self.acq_mode
        params=params or self.acq_params[self.acq_mode]
        if acq_mode=="accum":
            self.setup_accum_mode(*params)
        elif acq_mode=="kinetics":
            self.setup_kinetic_mode(*params)
        elif acq_mode=="fast_kinetics":
            self.setup_fast_kinetic_mode(*params)
        elif acq_mode=="cont":
            self.setup_cont_mode(params)
    def set_exposure(self, exposure):
        """Set camera exposure"""
        self._camsel()
        lib.SetExposureTime(exposure)
    def get_exposure(self):
        """Get current exposure"""
        return self.get_timings()[0]
    def enable_frame_transfer_mode(self, enable=True):
        """
        Enable frame transfer mode.

        For description, see Andor SDK manual.
        """
        self._camsel()
        if not self._check_option("acq","AC_ACQMODE_FRAMETRANSFER"): return
        lib.SetFrameTransferMode(enable)
        self.frame_transfer_mode=enable
    AcqTimes=collections.namedtuple("AcqTimes",["exposure","accum_cycle_time","kinetic_cycle_time"])
    def get_timings(self):
        """
        Get acquisition timing.

        Return tuple ``(exposure, accum_cycle_time, kinetic_cycle_time)``.
        In continuous mode, the relevant cycle time is ``kinetic_cycle_time``.
        """
        self._camsel()
        return self.AcqTimes(*lib.GetAcquisitionTimings())
    def get_readout_time(self):
        """Get frame readout time"""
        self._camsel()
        return lib.GetReadOutTime()
    def get_keepclean_time(self):
        """Get sensor keep-clean time"""
        self._camsel()
        return lib.GetKeepCleanTime()

    ### Acquisition process controls ###
    def prepare_acquisition(self):
        """
        Prepare acquisition.
        
        Isn't required (called automatically on acquisition start), but decreases time required for starting acquisition later.
        """
        self._camsel()
        lib.PrepareAcquisition()
    def start_acquisition(self, setup=True):
        """
        Start acquisition.

        If ``setup==True``, setup the acquisition parameters before the start
        (they don't apply automatically when the mode is changed).
        """
        self._camsel()
        if setup:
            self._setup_acquisition()
        self.get_buffer_size()
        lib.StartAcquisition()
    def stop_acquisition(self):
        """Stop acquisition"""
        self._camsel()
        if self.get_status()=="acquiring":
            lib.AbortAcquisition()
    AcqProgress=collections.namedtuple("AcqProgress",["frames_done","cycles_done"])
    def get_progress(self):
        """
        Get acquisition progress.

        Return tuple ``(frames_done, cycles_done)`` (these are different in accum or kinetic mode).
        """
        self._camsel()
        return self.AcqProgress(*lib.GetAcquisitionProgress())
    def wait_for_frame(self, since="lastwait", timeout=20.):
        """
        Wait for a new camera frame.

        `since` specifies what constitutes a new frame.
        Can be ``"lastread"`` (wait for a new frame after the last read frame), ``"lastwait"`` (wait for a new frame after last :meth:`wait_for_frame` call),
        or ``"now"`` (wait for a new frame acquired after this function call).
        If `timeout` is exceeded, raise :exc:`AndorTimeoutError`.
        """
        funcargparse.check_parameter_range(since,"since",{"lastread","lastwait","now"})
        if since=="lastwait":
            self._camsel()
            if timeout is None:
                lib.WaitForAcquisitionByHandle(self.handle)
            else:
                try:
                    lib.WaitForAcquisitionByHandleTimeOut(self.handle,int(timeout*1E3))
                except AndorLibError as e:
                    if e.text_code=="DRV_NO_NEW_DATA":
                        raise AndorTimeoutError
                    else:
                        raise
        elif since=="lastread":
            self._camsel()
            while not self.get_new_images_range():
                self.wait_for_frame(since="lastwait",timeout=timeout)
        else:
            rng=self.get_new_images_range()
            last_img=rng[1] if rng else None
            while True:
                self.wait_for_frame(since="lastwait",timeout=timeout)
                rng=self.get_new_images_range()
                if rng and (last_img is None or rng[1]>last_img):
                    return
    def cancel_wait(self):
        """Cancel wait"""
        self._camsel()
        lib.CancelWait()
    @contextlib.contextmanager
    def pausing_acquisition(self):
        """
        Context manager which temporarily pauses acquisition during execution of ``with`` block.

        Useful for applying certain settings which can't be changed during the acquisition.
        """
        acq=self.get_status()=="acquiring"
        try:
            self.stop_acquisition()
            yield
        finally:
            if acq:
                self.start_acquisition()

    ### Image settings and transfer controls ###
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        self._camsel()
        if not self._check_option("get","AC_GETFUNCTION_DETECTORSIZE"): return
        return lib.GetDetector()
    _read_modes=["fvb","multi_track","random_track","single_track","image"]
    _read_modes_cap={"fvb":"AC_READMODE_FVB", "multi_track":"AC_READMODE_MULTITRACK",
        "random_track":"AC_READMODE_RANDOMTRACK", "single_track":"AC_READMODE_SINGLETRACK",
        "image":"AC_READMODE_FULLIMAGE"}
    def set_read_mode(self, mode):
        """
        Set camera read mode.

        Can be ``"fvb"`` (average all image vertically and return it as one row), ``"single_track"`` (read a single row or several rows averaged together),
        ``"multi_track"`` (read multiple rows or averaged sets of rows), ``"random_track"`` (read several arbitrary lines),
        or ``"image"`` (read a whole image or its rectangular part).
        """
        funcargparse.check_parameter_range(mode,"mode",self._read_modes)
        self._camsel()
        if not self._check_option("read",self._read_modes_cap[mode]): return
        lib.SetReadMode(self._read_modes.index(mode))
        self.read_mode=mode
    def setup_single_track_mode(self, center=0, width=1):
        """
        Setup singe-track read mode.

        `center` and `width` specify selection of the rows to be averaged together.
        """
        self._camsel()
        if not self._check_option("read","AC_READMODE_FULLIMAGE"): return
        lib.SetSingleTrack(center+1,width)
        self.read_params["single_track"]=(center,width)
    def setup_multi_track_mode(self, number=1, height=1, offset=1):
        """
        Setup multi-track read mode.

        `number` is the number of rows (or row sets) to read, `height` is number of one row set (1 for a single row),
        `offset` is the distance between the row sets.
        """
        self._camsel()
        if not self._check_option("read","AC_READMODE_MULTITRACK"): return
        res=lib.SetMultiTrack(number,height,offset)
        self.read_params["multi_track"]=(number,height,offset)
        return res
    def setup_random_track_mode(self, tracks=None):
        """
        Setup random track read mode.

        `tracks` is a list of tuples ``(start, stop)`` specifying track span (start are inclusive, stop are exclusive, starting from 0)
        """
        self._camsel()
        if not self._check_option("read","AC_READMODE_RANDOMTRACK"): return
        tracks=tracks or [(0,1)]
        lib.SetRandomTracks([(t[0]+1,t[1]) for t in tracks])
        self.read_params["random_track"]=list(tracks)
    def setup_image_mode(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        """
        Setup image read mode.

        `hstart` and `hend` specify horizontal image extent, `vstart` and `vend` specify vertical image extent
        (start are inclusive, stop are exclusive, starting from 0), `hbin` and `vbin` specify binning.
        """
        hdet,vdet=self.get_detector_size()
        if not self._check_option("read","AC_READMODE_FULLIMAGE"): return
        hend=hdet if hend is None else hend
        vend=vdet if vend is None else vend
        hend=min(hdet,hend) # truncate the image size
        vend=min(vdet,vend)
        if (hstart,hend,vstart,vend)!=(0,hdet,0,vdet):
            if not self._check_option("read","AC_READMODE_SUBIMAGE"): return
        hend-=(hend-hstart)%hbin # make size divisible by bin
        hend=max(hend,hstart+hbin*self._minh)
        vend-=(vend-vstart)%vbin
        vend=max(vend,vstart+vbin*self._minv)
        lib.SetImage(hbin,vbin,hstart+1,hend,vstart+1,vend)
        self.read_params["image"]=(hstart,hend,vstart,vend,hbin,vbin)
    
    def get_roi(self):
        """
        Get current ROI.

        Return tuple ``(hstart, hend, vstart, vend, hbin, vbin)``.
        """
        return self.read_params["image"]
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        """
        Setup camera ROI.

        `hstart` and `hend` specify horizontal image extent, `vstart` and `vend` specify vertical image extent
        (start are inclusive, stop are exclusive, starting from 0), `hbin` and `vbin` specify binning.
        By default, all non-supplied parameters take extreme values.
        """
        self.setup_image_mode(hstart,hend,vstart,vend,hbin,vbin)
        self.set_read_mode("image")
    def _find_min_roi_end(self, kind="h"):
        roi=self.get_roi()
        smin,smax=1,self.get_detector_size()[0 if kind=="h" else 1]
        while smin<smax-1:
            smid=(smin+smax)//2
            try:
                if kind=="h":
                    self.set_roi(hend=smid)
                else:
                    self.set_roi(vend=smid)
                smax=smid
            except AndorLibError:
                smin=smid
        self.set_roi(*roi)
        return smax
    def get_roi_limits(self):
        """
        Get the minimal and maximal ROI parameters.

        Return tuple ``(min_roi, max_roi)``, where each element is in turn 6-tuple describing the ROI.
        """
        xdet,ydet=self.get_detector_size()
        roi=self.get_roi()
        min_roi=(0,0,roi[4]*self._minh,roi[5]*self._minv,1,1)
        maxbin=int(min(xdet//self._minh,ydet//self._minv,32)) if (self._minh and self._minv) else 32
        max_roi=(xdet-min_roi[2],xdet-min_roi[3],xdet,ydet,maxbin,maxbin)
        return (min_roi,max_roi)

    def _get_data_dimensions_rc(self, mode=None, params=None):
        if mode is None:
            mode=self.read_mode
        if params is None:
            params=self.read_params[mode]
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
    def get_data_dimensions(self, mode=None, params=None):
        """Get readout data dimensions for given read mode and read parameters (current by default)"""
        return image_utils.convert_shape_indexing(self._get_data_dimensions_rc(mode=mode,params=params),"rc",self.image_indexing)
    def read_newest_image(self, peek=False):
        """
        Read the newest image.

        If ``peek==True``, return the image but not mark it as read.
        """
        dim=self._get_data_dimensions_rc()
        self._camsel()
        if peek:
            data=lib.GetMostRecentImage16(dim[0]*dim[1])
            img=data.reshape((dim[0],dim[1]))
            return image_utils.convert_image_indexing(img,"rcb",self.image_indexing)
        else:
            rng=self.get_new_images_range()
            if rng:
                return self.read_multiple_images([rng[1],rng[1]])[0,:,:]
    def read_oldest_image(self):
        """
        Read the oldest un-read image in the buffer.

        `dim` specifies image dimensions (by default use dimensions corresponding to the current camera settings).
        """
        dim=self._get_data_dimensions_rc()
        self._camsel()
        data=lib.GetOldestImage16(dim[0]*dim[1])
        img=data.reshape((dim[0],dim[1]))
        return image_utils.convert_image_indexing(img,"rcb",self.image_indexing)
    def get_buffer_size(self):
        """Get the size of the image ring buffer"""
        self._camsel()
        try:
            self.last_buffer_size=lib.GetSizeOfCircularBuffer()
        except AndorLibError:
            pass
        return self.last_buffer_size
    def get_new_images_range(self):
        """
        Get the range of the new images.
        
        Return tuple ``(first, last)`` with images range (inclusive).
        If no images are available, return ``None``.
        """
        self._camsel()
        try:
            rng=lib.GetNumberNewImages()
            return (rng[0]-1,rng[1]-1)
        except AndorLibError as e:
            if e.text_code=="DRV_NO_NEW_DATA":
                return None
            raise
    def read_multiple_images(self, rng=None):
        """
        Read multiple images specified by `rng` (by default, all un-read images).

        `dim` specifies images dimensions (by default use dimensions corresponding to the current camera settings).
        """
        self._camsel()
        if rng is None:
            rng=self.get_new_images_range()
        dim=self._get_data_dimensions_rc()
        if rng is None:
            return np.zeros((0,dim[0],dim[1]))
        data,vmin,vmax=lib.GetImages16(rng[0]+1,rng[1]+1,dim[0]*dim[1]*(rng[1]-rng[0]+1))
        imgs=data.reshape((-1,dim[0],dim[1]))
        return np.asarray([image_utils.convert_image_indexing(im,"rcb",self.image_indexing) for im in imgs])

    def flush_buffer(self):
        """Flush the camera buffer (restart the acquisition)"""
        acq_mode=self.acq_mode
        if acq_mode=="cont":
            self.set_acquisition_mode("single")
        else:
            self.set_acquisition_mode("cont")
        self.prepare_acquisition()
        self.set_acquisition_mode(acq_mode)
        self.prepare_acquisition()

    ### Combined functions ###
    def snap(self):
        """Snap a single image (with preset image read mode parameters)"""
        self.set_acquisition_mode("single")
        self.set_read_mode("image")
        self.start_acquisition()
        self.wait_for_frame()
        self.stop_acquisition()
        return self.read_newest_image()










_open_cams_SDKs=0

def get_cameras_number_SDK3():
    """Get number of connected Andor cameras"""
    lib3.initlib()
    lib3.AT_InitialiseLibrary()
    return lib3.AT_GetInt(1,"DeviceCount")

class AndorSDK3Camera(IDevice):
    """
    Andor SDK3 camera.

    Args:
        idx(int): camera index (use :func:`get_cameras_number_SDK3` to get the total number of connected cameras)
    """
    def __init__(self, idx=0):
        IDevice.__init__(self)
        lib3.initlib()
        self.idx=idx
        self.handle=None
        self._default_nframes=100
        self._buffer_overflow=10
        self._buffer_mgr=self.BufferManager(self)
        self._last_wait_frame=-1
        self._reg_cb=None
        self._acq_mode=None
        self.open()
        self.image_indexing="rct"
        self.v=dictionary.ItemAccessor(self.get_value,self.set_value)

        self._nodes_ignore_error={"get":(AndorNotSupportedError,),"set":(AndorNotSupportedError,)}
        self._add_full_info_node("model_data",self.get_model_data)
        self._add_full_info_node("values",self.get_all_values)
        self._add_settings_node("trigger_mode",self.get_trigger_mode,self.set_trigger_mode)
        self._add_settings_node("shutter",self.get_shutter,self.set_shutter)
        self._add_settings_node("temperature",self.get_temperature_setpoint,self.set_temperature)
        self._add_status_node("temperature_monitor",self.get_temperature)
        self._add_settings_node("cooler",self.is_cooler_on,self.set_cooler)
        self._add_status_node("is_acquiring",self.is_acquiring)
        self._add_status_node("timings",self.get_timings)
        self._add_status_node("data_dimensions",self.get_data_dimensions)
        self._add_settings_node("roi",self.get_roi,self.set_roi)
        self._add_status_node("roi_limits",self.get_roi_limits)
        self._add_settings_node("exposure",self.get_exposure,self.set_exposure)
        self._add_settings_node("readout_time",self.get_readout_time,self.set_readout_time)
        self._add_status_node("frame_counter_status",self.get_frame_counter_status)
        self._add_status_node("buffer_size",self.get_buffer_size)
        self._add_full_info_node("detector_size",self.get_detector_size)



    _open_cams=0
    def open(self):
        """Open connection to the camera"""
        self.close()
        ncams=get_cameras_number_SDK3()
        if self.idx>=ncams:
            raise AndorError("camera index {} is not available ({} cameras exist)".format(self.idx,ncams))
        lib3.AT_InitialiseLibrary()
        self.handle=lib3.AT_Open(self.idx)
        self._open_cams+=1
        self._register_events()
    def close(self):
        """Close connection to the camera"""
        if self.handle is not None:
            self.stop_acquisition()
            self._unregister_events()
            lib3.AT_Close(self.handle)
            self._open_cams-=1
            if self._open_cams<=0:
                lib3.AT_FinaliseLibrary()
        self.handle=None
    def is_opened(self):
        """Check if the device is connected"""
        return self.handle is not None

    def is_feature_available(self, name):
        """Check if given feature is available"""
        return lib3.AT_IsImplemented(self.handle,name)
    def is_feature_readable(self, name):
        """Check if given feature is available"""
        return lib3.AT_IsImplemented(self.handle,name) and lib3.AT_IsReadable(self.handle,name) 
    def is_feature_writable(self, name):
        """Check if given feature is available"""
        return lib3.AT_IsImplemented(self.handle,name) and lib3.AT_IsWritable(self.handle,name) 
    def _check_feature(self, name, writable=False):
        if not self.is_feature_available(name) or (writable and not self.is_feature_writable(name)):
            raise AndorNotSupportedError("feature {} is not supported by camera {}".format(name,self.get_model_data().camera_model))
    def get_value(self, name, kind="auto", enum_str=True, default="error"):
        """
        Get current value of the given feature.
        
        `kind` determines feature kind, can be ``"int"``, ``"float"``, ``"str"``, ``"bool"`` or ``"enum``";
        by default (``"auto"``), auto-determine value kind (might not work for newer features).
        If ``enum_str==True``, return enum values as strings; otherwise, return as indices.
        If ``default=="error"``, raise :exc:`AndorError` if the feature is not implemented; otherwise, return `default` if it is not implemented.
        """
        if kind=="auto":
            if name in AndorSDK3_feature_types:
                kind=AndorSDK3_feature_types[name]
            else:
                raise AndorError("can't determine feature kind: {}".format(name))
        if not lib3.AT_IsImplemented(self.handle,name):
            if default=="error":
                raise AndorError("feature is not implemented: {}".format(name))
            else:
                return default
        if not lib3.AT_IsReadable(self.handle,name):
            raise AndorError("feature is not readable: {}".format(name))
        if kind=="int":
            return lib3.AT_GetInt(self.handle,name)
        if kind=="float":
            return lib3.AT_GetFloat(self.handle,name)
        if kind=="str":
            strlen=lib3.AT_GetStringMaxLength(self.handle,name)
            return lib3.AT_GetString(self.handle,name,strlen)
        if kind=="bool":
            return bool(lib3.AT_GetBool(self.handle,name))
        if kind=="enum":
            val=lib3.AT_GetEnumIndex(self.handle,name)
            if enum_str:
                val=lib3.AT_GetEnumStringByIndex(self.handle,name,val,512)
            return val
        raise AndorError("can't read feature '{}' with kind '{}'".format(name,kind))
    def set_value(self, name, value, kind="auto", not_implemented_error=True):
        """
        Set current value of the given feature.
        
        `kind` determines feature kind, can be ``"int"``, ``"float"``, ``"str"``, ``"bool"`` or ``"enum``";
        by default (``"auto"``), auto-determine value kind (might not work for newer features).

        If ``not_implemented_error==True`` and the feature is not implemented, raise :exc:`AndorError`; otherwise, do nothing.
        """
        if kind=="auto":
            if name in AndorSDK3_feature_types:
                kind=AndorSDK3_feature_types[name]
            else:
                raise AndorError("can't determine feature kind: {}".format(name))
        if not lib3.AT_IsImplemented(self.handle,name):
            if not_implemented_error:
                raise AndorError("feature is not implemented: {}".format(name))
            else:
                return
        if not lib3.AT_IsWritable(self.handle,name):
            raise AndorError("feature is not writable: {}".format(name))
        if kind=="int":
            lib3.AT_SetInt(self.handle,name,int(value))
        elif kind=="float":
            lib3.AT_SetFloat(self.handle,name,float(value))
        elif kind=="str":
            lib3.AT_SetString(self.handle,name,value)
        elif kind=="bool":
            lib3.AT_SetBool(self.handle,name,bool(value))
        elif kind=="enum":
            if isinstance(value,py3.anystring):
                lib3.AT_SetEnumString(self.handle,name,value)
            else:
                lib3.AT_SetEnumIndex(self.handle,name,int(value))
        else:
            raise AndorError("can't read feature '{}' with kind '{}'".format(name,kind))
    def command(self, name):
        """Execute given command"""
        if not lib3.AT_IsImplemented(self.handle,name):
            raise AndorError("command is not implemented: {}".format(name))
        lib3.AT_Command(self.handle,name)
    def get_value_range(self, name, kind="auto", enum_str=True):
        """
        Get allowed rande of the given value.
        
        `kind` determines feature kind, can be ``"int"``, ``"float"``, ``"str"``, ``"bool"`` or ``"enum``";
        by default (``"auto"``), auto-determine value kind (might not work for newer features).

        For ``"int"`` or ``"float"`` values return tuple ``(min, max)`` (inclusive); for ``"enum"`` return list of possible values
        (if ``enum_str==True``, return list of string values, otherwise return list of indices).
        For all other value kinds return ``None``.
        """
        if kind=="auto":
            if name in AndorSDK3_feature_types:
                kind=AndorSDK3_feature_types[name]
            else:
                raise AndorError("can't determine feature kind: {}".format(name))
        if not lib3.AT_IsImplemented(self.handle,name):
            raise AndorError("feature is not implemented: {}".format(name))
        if kind=="int":
            return (lib3.AT_GetIntMin(self.handle,name),lib3.AT_GetIntMax(self.handle,name))
        if kind=="float":
            return (lib3.AT_GetFloatMin(self.handle,name),lib3.AT_GetFloatMax(self.handle,name))
        if kind=="enum":
            count=lib3.AT_GetEnumCount(self.handle,name)
            available=[i for i in range(count) if lib3.AT_IsEnumIndexAvailable(self.handle,name,i)]
            if enum_str:
                available=[lib3.AT_GetEnumStringByIndex(self.handle,name,i,512) for i in available]
            return available
    def limit_value(self, name, value):
        """Limit value to lie within the allowed range"""
        vmin,vmax=self.get_value_range(name)
        return min(max(value,vmin),vmax)

    def get_all_values(self, enum_str=True):
        """
        Get all readable values.

        If ``enum_str==True``, return enum values as strings; otherwise, return as indices.
        """
        values={}
        for v in AndorSDK3_feature_types:
            if AndorSDK3_feature_types[v]!="comm" and lib3.AT_IsImplemented(self.handle,v) and lib3.AT_IsReadable(self.handle,v):
                try:
                    values[v]=self.get_value(v,enum_str=enum_str)
                except AndorSDK3LibError:
                    pass
        return values

    ModelData=collections.namedtuple("ModelData",["camera_model","serial_number","firmware_version","software_version"])
    def get_model_data(self, enum_str=True):
        """
        Get camera model data.

        Return tuple ``(camera_model, serial_number, firmware_version, software_version)``.
        """
        camera_model=self.get_value("CameraModel")
        serial_number=self.get_value("SerialNumber")
        firmware_version=self.get_value("FirmwareVersion")
        strlen=lib3.AT_GetStringMaxLength(1,"SoftwareVersion")
        software_version=lib3.AT_GetString(1,"SoftwareVersion",strlen)
        return self.ModelData(camera_model,serial_number,firmware_version,software_version)
        


    _trigger_modes={"int":"Internal","ext":"External","software":"Software","ext_start":"External start","ext_exp":"External Exposure"}
    _inv_trigger_modes=general.invert_dict(_trigger_modes)
    def get_trigger_mode(self):
        """
        Get trigger mode.

        Can be ``"int"`` (internal), ``"ext"`` (external), ``"software"`` (software trigger),
            ``"ext_start"`` (external start), or ``"ext_exp"`` (external exposure).
        """
        tm=self.get_value("TriggerMode")
        tm=self._inv_trigger_modes.get(tm,tm)
        return tm
    def set_trigger_mode(self, mode):
        """
        Set trigger mode.

        Can be ``"int"`` (internal), ``"ext"`` (external), or ``"software"`` (software trigger).
        """
        funcargparse.check_parameter_range(mode,"mode",self._trigger_modes)
        self.set_value("TriggerMode",self._trigger_modes[mode])
        return self.get_trigger_mode()
    _shutter_modes={"open":"Open","closed":"Closed","auto":"Auto"}
    _inv_shutter_modes=general.invert_dict(_trigger_modes)
    def get_shutter(self):
        """Get current shutter mode"""
        self._check_feature("ShutterMode")
        sm=self.get_value("ShutterMode")
        return self._inv_shutter_modes(sm)
    def set_shutter(self, mode):
        """
        Set trigger mode.

        Can be ``"open"``, ``"closed"``, or ``"auto"``.
        """
        self._check_feature("ShutterMode")
        funcargparse.check_parameter_range(mode,"mode",self._shutter_modes)
        self.set_value("ShutterMode",self._shutter_modes[mode])
        return self.get_shutter()


    ### Cooler controls ###
    def is_cooler_on(self):
        """Check if the cooler is on"""
        self._check_feature("SensorCooling")
        return self.get_value("SensorCooling")
    def set_cooler(self, on=True):
        """Set the cooler on or off"""
        self._check_feature("SensorCooling")
        self.set_value("SensorCooling",on)
        return self.get_value("SensorCooling")

    def get_temperature(self):
        """Get the current camera temperature"""
        self._check_feature("SensorTemperature")
        return self.get_value("SensorTemperature")
    def get_temperature_setpoint(self):
        """Get current temperature setpoint."""
        self._check_feature("TargetSensorTemperature")
        return self.get_value("TargetSensorTemperature")
    def set_temperature(self, temperature, enable_cooler=True):
        """
        Change the temperature setpoint.

        If ``enable_cooler==True``, turn the cooler on automatically.
        """
        self._check_feature("TargetSensorTemperature")
        if self.get_value("TargetSensorTemperature")!=temperature:
            self._check_feature("TargetSensorTemperature",writable=True)
            self.set_value("TargetSensorTemperature",temperature)
        if enable_cooler:
            self.set_cooler(True)
        return self.get_value("TargetSensorTemperature")


    def get_exposure(self):
        """Get current exposure"""
        return self.get_value("ExposureTime")
    def set_exposure(self, exposure, set_min_readout_time=True):
        """Set camera exposure"""
        self.set_readout_time(0)
        exposure=self.limit_value("ExposureTime",exposure)
        self.set_value("ExposureTime",exposure)
        return self.get_exposure()
    def get_readout_time(self):
        return 1./self.get_value("FrameRate")
    def set_readout_time(self, readout_time):
        if not self.is_feature_writable("FrameRate"):
            return
        fr_rng=self.get_value_range("FrameRate")
        ro_rng=1./fr_rng[1],1./fr_rng[0]
        readout_time=max(min(readout_time,ro_rng[1]),ro_rng[0])
        self.set_value("FrameRate",1./readout_time)
        return self.get_readout_time()
    AcqTimes=collections.namedtuple("AcqTimes",["exposure","accum_cycle_time","kinetic_cycle_time"])
    def get_timings(self):
        """
        Get acquisition timing.

        Return tuple ``(exposure, accum_cycle_time, kinetic_cycle_time)``.
        In continuous mode, the relevant cycle time is ``kinetic_cycle_time``.
        """
        return self.AcqTimes(self.get_exposure(),0,self.get_readout_time())


    
    ### Frame counting ###
    class BufferManager(object):
        """Buffer manager: stores, constantly reads and re-schedules buffers, keeps track of acquired and read frames, and of buffer overflow events"""
        def __init__(self, cam):
            object.__init__(self)
            self.buffers=None
            self.queued_buffers=0
            self.size=0
            self.acq_frames=0
            self.read_frames=0
            self.missed_frames=0
            self.buffer_overflows=0
            self.stop_requested=False
            self.overflow_detected=False
            self.cam=cam
            self._cnt_lock=threading.RLock()
            self._buffer_loop_thread=None
        def allocate_buffers(self, nbuff, size, queued_buffers=None):
            """
            Allocate and queue buffers.

            `queued_buffers`` specifies number of allocated buffers to keep queued at aagiven time (by default, all of them)
            """
            with self._cnt_lock:
                self.deallocate_buffers()
                self.buffers=[ctypes.create_string_buffer(size) for _ in range(nbuff)]
                self.queued_buffers=queued_buffers or len(self.buffers)
                self.size=size        
                for b in self.buffers[:self.queued_buffers]:
                    lib3.AT_QueueBuffer(self.cam.handle,ctypes.cast(b,ctypes.POINTER(ctypes.c_uint8)),self.size)
        def deallocate_buffers(self):
            """Deallocated buffers (flushing should be done manually)"""
            with self._cnt_lock:
                if self.buffers:
                    self.stop_loop()
                    self.buffers=None
                    self.size=0
        def reset(self, buffer_overflows=0):
            """Reset counter (on frame acquisition)"""
            self.acq_frames=0
            self.read_frames=0
            self.missed_frames=0
            self.buffer_overflows=buffer_overflows
            self.overflow_detected=False
        def _acq_loop(self):
            while not self.stop_requested:
                try:
                    # buff,size=lib3.AT_WaitBuffer(self.cam.handle,300)
                    # buff_addr=ctypes.cast(buff,ctypes.c_void_p).value
                    # next_buff=self.buffers[self.acq_frames%len(self.buffers)]
                    # next_buff_addr=ctypes.addressof(next_buff)
                    # if buff_addr!=next_buff_addr:
                    #     all_addr=[ctypes.addressof(rb) for rb in self.buffers]
                    #     exp_id=all_addr.index(next_buff_addr)
                    #     act_id=all_addr.index(buff_addr)
                    #     raise AndorError("unexpected buffer address: expected {}[{}], got {}[{}] (difference of {})".format(next_buff_addr,exp_id,buff_addr,act_id,next_buff_addr-buff_addr))
                    # if size!=self.size:
                    #     raise AndorError("unexpected buffer size: expected {}, got {}".format(self.size,size))
                    _,size=lib3.AT_WaitBuffer(self.cam.handle,300)
                    if size!=self.size:
                        raise AndorError("unexpected buffer size: expected {}, got {}".format(self.size,size))
                except AndorSDK3LibError as e:
                    if e.code!=13:
                        raise
                    continue
                next_buff=self.buffers[(self.acq_frames+self.queued_buffers)%len(self.buffers)]
                lib3.AT_QueueBuffer(self.cam.handle,ctypes.cast(next_buff,ctypes.POINTER(ctypes.c_uint8)),self.size)
                with self._cnt_lock:
                    self.acq_frames+=1
                    if self.acq_frames-self.read_frames>len(self.buffers)-self.cam._buffer_overflow:
                        self.missed_frames+=1
                        self.read_frames+=1
        def read(self, skip=False):
            """Return the oldest available acuqired but not read buffer, and mark it as read"""
            buff_idx=None
            with self._cnt_lock:
                if self.buffers and self.read_frames<self.acq_frames:
                    buff_idx=self.read_frames%len(self.buffers)
                    self.read_frames+=1
            if (buff_idx is not None) and not skip:
                return ctypes.string_at(self.buffers[buff_idx],self.size)
            return None
        def start_loop(self):
            """Start buffer scheduling loop"""
            self.stop_loop()
            self.stop_requested=False
            self._buffer_loop_thread=threading.Thread(target=self._acq_loop,daemon=True)
            self._buffer_loop_thread.start()
        def stop_loop(self):
            """Stop buffer scheduling loop"""
            if self._buffer_loop_thread is not None:
                self.stop_requested=True
                self._buffer_loop_thread.join()
                self._buffer_loop_thread=None
            self.reset()
        def overflow(self):
            """Process buffer overflow event"""
            with self._cnt_lock:
                self.overflow_detected=True
        def new_overflow(self):
            """Check if acquisition restart is needed (buffer overflowed)"""
            with self._cnt_lock:
                return self.overflow_detected
        def get_status(self):
            """Get counter status: tuple ``(acquired, read, missed, buffer_size, buffer_overflows)``"""
            with self._cnt_lock:
                return self.acq_frames,self.read_frames,self.missed_frames,len(self.buffers or []),self.buffer_overflows
    def _register_events(self):
        self._unregister_events()
        self.set_value("EventSelector","BufferOverflowEvent")
        self.set_value("EventEnable",True)
        buff_cb=lib3.AT_RegisterFeatureCallback(self.handle,"BufferOverflowEvent",lambda *args: self._buffer_mgr.overflow())
        self._reg_cb=buff_cb
        self._buffer_mgr.reset()
    def _unregister_events(self):
        if self._reg_cb is not None:
            lib3.AT_UnregisterFeatureCallback(self.handle,"BufferOverflowEvent",self._reg_cb)
            self.set_value("EventSelector","BufferOverflowEvent")
            self.set_value("EventEnable",False)
            self._reg_cb=None
            self._buffer_mgr.reset()

    def start_acquisition(self, mode="sequence", nframes=None):
        """
        Start acquisition.

        `mode` can be either ``"snap"`` (since frame or sequency acquisition) or ``"sequence"`` (continuous acquisition).
        `nframes` determines number of frames to acquire in ``"snap"`` mode, or size of the ring buffer in the ``"sequence"`` mode (by default, 100).
        """
        self.stop_acquisition()
        acq_modes=["sequence","snap"]
        funcargparse.check_parameter_range(mode,"mode",acq_modes)
        if mode=="snap":
            self.set_value("CycleMode","Fixed")
            self.set_value("FrameCount",nframes or 1)
        else:
            # self.set_value("CycleMode","Continuous") # Zyla bug doesn't allow continuous mode with >1000 FPS
            self.set_value("CycleMode","Fixed")
            self.set_value("FrameCount",self.get_value_range("FrameCount")[1])
        self.create_ring_buffer(nframes)
        self._buffer_mgr.reset()
        self._last_wait_frame=-1
        self._buffer_mgr.start_loop()
        self.command("AcquisitionStart")
        self._acq_mode=(mode,nframes)
    def stop_acquisition(self):
        """Stop acquisition"""
        if self.get_value("CameraAcquiring"):
            self.command("AcquisitionStop")
            self._buffer_mgr.stop_loop()
            self.remove_ring_buffer()
        self._acq_mode=None
    def is_acquiring(self):
        """Check if acquisition is in progress"""
        return self.get_value("CameraAcquiring")
    @contextlib.contextmanager
    def pausing_acquisition(self):
        """
        Context manager which temporarily pauses acquisition during execution of ``with`` block.

        Useful for applying certain settings which can't be changed during the acquisition.
        """
        acq_mode=self._acq_mode
        try:
            self.stop_acquisition()
            yield
        finally:
            if acq_mode:
                self.start_acquisition(*acq_mode)
    def wait_for_frame(self, since="lastread", timeout=20., period=1E-3):
        """
        Wait for a new camera frame.

        `since` specifies what constitutes a new frame.
        Can be ``"lastread"`` (wait for a new frame after the last read frame),
        ``"lastwait"`` (wait for a new frame after last :meth:`wait_for_frame` call),
        or ``"now"`` (wait for a new frame acquired after this function call).
        If `timeout` is exceeded, raise :exc:`AndorTimeoutError`.
        `period` specifies camera polling period.
        """
        ctd=general.Countdown(timeout)
        last_acq_frame=self._buffer_mgr.get_status()[0]
        while not ctd.passed():
            acq_frame,read_frame=self._buffer_mgr.get_status()[:2]
            since_last_wait=acq_frame-self._last_wait_frame
            self._last_wait_frame=acq_frame
            if since=="lastread" and acq_frame>read_frame:
                return
            if since=="now" and acq_frame>last_acq_frame:
                return
            if since=="lastwait" and since_last_wait>0:
                return
            time.sleep(min(period,ctd.time_left()))
        raise AndorTimeoutError()
    
    def create_ring_buffer(self, nframes=None):
        """
        Create and set up a new ring buffer.

        If a ring buffer is already allocated, remove it and create a new one.
        Called automatically on acquisition start, doesn't usually need to be called explicitly.
        """
        self.remove_ring_buffer()
        nframes=nframes or self._default_nframes
        frame_size=self.get_value("ImageSizeBytes")
        self._buffer_mgr.allocate_buffers(nframes+self._buffer_overflow,frame_size,queued_buffers=nframes)
    def remove_ring_buffer(self):
        """
        Remove the ring buffer and clean up the memory.

        Called automatically on acquisition stop, doesn't usually need to be called explicitly.
        """
        lib3.flush_buffers(self.handle)
        self._buffer_mgr.deallocate_buffers()
    def get_buffer_size(self):
        """Get ring buffer size"""
        return len(self._buffer_mgr.buffers or [])
    def get_frame_counter_status(self):
        """
        Get frame counter status.

        Return tuple ``(acquired, read, missed, buffer_size, buffer_overflows)`` with number of acquired frames,
        read (or skipped) frames, missed frame, and number of buffer overflows.
        """
        return self._buffer_mgr.get_status()


    def _parse_image(self, img):
        if img is None:
            return None
        height,width=self._get_data_dimensions_rc()
        metadata_enabled=self.get_value("MetadataEnable",default=False)
        imlen=len(img)
        if metadata_enabled:
            chunks={}
            read_len=0
            while read_len<imlen:
                clen=strpack.unpack_uint(img[imlen-read_len-4:imlen-read_len  ],"<")
                cid =strpack.unpack_uint(img[imlen-read_len-8:imlen-read_len-4],"<")
                chunks[cid]=img[imlen-read_len-clen-4:imlen-read_len-8]
                read_len+=clen+4
            if 0 not in chunks:
                raise AndorError("missing image data")
            img=chunks.pop(0)
            metadata=chunks
        else:
            metadata={}
        bpp=self.get_value("BytesPerPixel")
        if bpp not in [1,1.5,2,4]:
            raise ValueError("unexpected pixel byte size: {}".format(bpp))
        stride=self.get_value("AOIStride")
        if stride<int(np.ceil(bpp*width)):
            raise AndorError("unexpected stride: expected at least {}x{}={}, got {}".format(width,bpp,int(np.ceil(width*bpp)),stride))
        exp_len=int(stride*height)
        if len(img)!=exp_len:
            if len(img)<exp_len or len(img)>=exp_len+8: # sometimes image size gets rounded to nearest 4/8 bytes
                raise AndorError("unexpected image byte size: expected {}x{}={}, got {}".format(stride,height,int(stride*height),len(img)))
        if bpp==1.5:
            img=nb_read_uint12(np.frombuffer(img,"u1",count=exp_len).reshape(-1,stride),width=width)
        else:
            dtype=data_format.DataFormat(int(bpp),"u","<")
            if stride==bpp*width:
                img=np.frombuffer(img,dtype=dtype.to_desc("numpy"),count=width*height).reshape(height,width)
            elif stride%bpp==0:
                img=np.frombuffer(img,dtype=dtype.to_desc("numpy"),count=(stride//bpp)*height).reshape(height,-1)[:,:width]
            else: # only possible with bpp==2 or 4 and non-divisible stride
                bpp=int(bpp)
                byteimg=np.frombuffer(img,dtype="u1",count=exp_len).reshape(height,stride)
                byteimg=byteimg[:,:width*bpp].astype(dtype)
                if bpp==2:
                    img=(byteimg[:,::2])+(byteimg[:,1::2]<<8)
                else:
                    img=byteimg[:,::bpp]
                    for b in range(1,bpp):
                        img+=byteimg[:,b::bpp]<<(b*8)
        img=image_utils.convert_image_indexing(img,"rct",self.image_indexing)
        return img,metadata

    def _get_data_dimensions_rc(self):
        return self.get_value("AOIHeight"),self.get_value("AOIWidth")
    def get_data_dimensions(self):
        """Get readout data dimensions"""
        return image_utils.convert_shape_indexing(self._get_data_dimensions_rc(),"rc",self.image_indexing)
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        return int(self.get_value("SensorWidth")),int(self.get_value("SensorHeight"))
    def get_roi(self):
        """
        Get current ROI.

        Return tuple ``(hstart, hend, vstart, vend, hbin, vbin)``.
        """
        hbin=int(self.get_value("AOIHBin"))
        vbin=int(self.get_value("AOIVBin"))
        hstart=int(self.get_value("AOILeft"))-1
        hend=hstart+int(self.get_value("AOIWidth"))*hbin
        vstart=int(self.get_value("AOITop"))-1
        vend=vstart+int(self.get_value("AOIHeight"))*vbin
        return (hstart,hend,vstart,vend,hbin,vbin)
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        """
        Set current ROI.

        By default, all non-supplied parameters take extreme values. Binning is the same for both axes.
        """
        self.remove_ring_buffer()
        det_size=self.get_detector_size()
        hend=hend or det_size[0]
        vend=vend or det_size[1]
        minw=self.get_value_range("AOIWidth")[0]
        minh=self.get_value_range("AOIHeight")[0]
        self.set_value("AOIWidth",minw)
        self.set_value("AOIHeight",minh)
        self.set_value("AOILeft",1)
        self.set_value("AOITop",1)
        self.set_value("AOIHBin",hbin)
        self.set_value("AOIVBin",vbin)
        self.set_value("AOILeft",hstart+1)
        self.set_value("AOITop",vstart+1)
        self.set_value("AOIWidth",max((hend-hstart)//hbin,minw))
        self.set_value("AOIHeight",max((vend-vstart)//vbin,minh))
        return self.get_roi()
    def get_roi_limits(self):
        """
        Get the minimal and maximal ROI parameters.

        Return tuple ``(min_roi, max_roi)``, where each element is in turn 6-tuple describing the ROI.
        """
        params=["AOILeft","AOITop","AOIWidth","AOIHeight","AOIHBin","AOIVBin"]
        minp,maxp=[list(p) for p in zip(*[self.get_value_range(p) for p in params])]
        bin=[self.get_value(p) for p in params[-2:]]
        for i in range(2):
            minp[i]-=1
            maxp[i]-=1
        for i in range(4):
            minp[i]*=bin[i%2]
            maxp[i]*=bin[i%2]
        min_roi=(0,0)+tuple(minp[2:])
        max_roi=(maxp[2]-minp[2],maxp[3]-minp[3],maxp[2],maxp[3],maxp[4],maxp[5])
        return (min_roi,max_roi)

    def get_new_images_range(self):
        """
        Get the range of the new images.
        
        Return tuple ``(first, last)`` with images range (inclusive).
        If no images are available, return ``None``.
        """
        acq_frames,read_frames=self._buffer_mgr.get_status()[:2]
        if acq_frames>read_frames:
            return (read_frames,acq_frames-1)
        else:
            return None
            
    def read_multiple_images(self, rng=None, return_metadata=False):
        """
        Read multiple images specified by `rng` (by default, all un-read images).
        
        If ``return_metadata==True``, return raw metadata along with images.
        Metadata is a dictionary ``{section: data}``, where ``section`` is the section number (usually 1 or 7), and ``data`` is the corresponding binary data string.
        """
        if rng is None:
            rng=self.get_new_images_range()
        dim=self.get_data_dimensions()
        images,metadata=np.zeros((0,dim[0],dim[1])),[]
        if rng is not None:
            acq_frames,read_frames=self._buffer_mgr.get_status()[:2]
            rng=max(rng[0],read_frames),min(rng[1],acq_frames-1)
            if self._buffer_mgr.new_overflow():
                bovf=self._buffer_mgr.buffer_overflows
                self.start_acquisition(*self._acq_mode)
                self._buffer_mgr.buffer_overflows+=bovf+1
            for _ in range(read_frames,rng[0]):
                self._buffer_mgr.read(skip=True)
            frames=[self._parse_image(self._buffer_mgr.read()) for _ in range(rng[1]-rng[0]+1)]
            frames=[f for f in frames if f is not None]
            if frames:
                images,metadata=list(zip(*frames))
                images=np.asarray(images)
        return (images,metadata) if return_metadata else images

    ### Combined functions ###
    def snap(self):
        """Snap a single image (with preset image read mode parameters)"""
        self.start_acquisition("snap",1)
        self.wait_for_frame()
        img=self.read_multiple_images()[0]
        self.stop_acquisition()
        return img