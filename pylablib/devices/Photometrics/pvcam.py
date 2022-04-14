from .pvcam_lib import wlib as lib, PvcamError, PvcamLibError
from . import pvcam_defs

from ...core.utils import py3, nbtools
from ...core.utils.nbtools import au2, au4, au8
from ...core.devio import interface
from ..utils import load_lib
from ..interface import camera

import numpy as np
import numba as nb
import ctypes
import collections
import contextlib


class PvcamTimeoutError(PvcamError):
    """Pvcam frame timeout error"""
class PvcamAttributeValueError(PvcamError):
    """Pvcam attribute value error"""
    def __init__(self, name, value, all_values):
        self.name=name
        self.value=value
        self.all_values=all_values
        self.msg="unsupported value '{}' for parameter {}; supported values are {}".format(self.value,self.name,self.all_values)
        super().__init__(self.msg)


class LibraryController(load_lib.LibraryController):
    def _do_init(self):
        lib.pl_pvcam_init()
    def _do_uninit(self):
        lib.pl_pvcam_uninit()
libctl=LibraryController(lib)


def list_cameras():
    """List all cameras available through Pvcam interface"""
    with libctl.temp_open():
        n=lib.pl_cam_get_total()
        return [py3.as_str(lib.pl_cam_get_name(i)) for i in range(n)]

def get_cameras_number():
    """Get number of connected Pvcam cameras"""
    return len(list_cameras())


def _lstrip(s, pfx):
    if s.startswith(pfx):
        return s[len(pfx):]
    return s
class PvcamAttribute:
    """
    Object representing an Pvcam camera parameter.

    Allows to query and set values and get additional information.
    Usually created automatically by an :class:`PvcamCamera` instance, but could be created manually.

    Args:
        handle: camera handle
        pid: parameter id of the attribute

    Attributes:
        name: attribute name
        kind: attribute kind; can be ``"INT8"``, ``"INT16"``, ``"INT32"``, ``"INT64"``,
            ``"UNS8"``, ``"UNS16"``, ``"UNS32"``, ``"UNS64"``, ``"FLT32"``, ``"FLT64"``, 
            ``"ENUM"``, ``"BOOLEAN"``, or ``"CHAR_PTR"``
        kind: attribute kind (e.g., ``"INT8"`` or ``"FLT32"``)
        available (bool): whether attribute is available on the current hardware
        readable (bool): whether attribute is readable
        writable (bool): whether attribute is writable
        min (float or int): minimal attribute value (if applicable)
        max (float or int): maximal attribute value (if applicable)
        inc (float or int): minimal attribute increment value (if applicable)
        ivalues: list of possible integer values for enum attributes
        values: list of possible text values for enum attributes
        labels: dict ``{label: index}`` which shows all possible values of an enumerated attribute and their corresponding numerical values
        ilabels: dict ``{index: label}`` which shows labels corresponding to numerical values of an enumerated attribute
        default: default values of the attribute
    """
    def __init__(self, handle, pid, cam=None):
        self.handle=handle
        self.pid=pid
        self.cam=cam
        self.name=_lstrip(pvcam_defs.drPARAM.get(pid,"UNKNOWN"),"PARAM_")
        try:
            self.available=lib.get_param(self.handle,self.pid,pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_AVAIL,pvcam_defs.PARAM_TYPE.TYPE_BOOLEAN)
            self._attr_type_n=lib.get_param(self.handle,self.pid,pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_TYPE,pvcam_defs.PARAM_TYPE.TYPE_UNS16)
            self.kind=_lstrip(pvcam_defs.drPARAM_TYPE.get(self._attr_type_n,"UNKNOWN"),"TYPE_")
            self._value_access_n=lib.get_param(self.handle,self.pid,pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_ACCESS,pvcam_defs.PARAM_TYPE.TYPE_UNS16)
            self.value_access=_lstrip(pvcam_defs.drPL_PARAM_ACCESS.get(self._value_access_n,"UNKNOWN"),"ACC_")
        except PvcamLibError as err:
            if err.code==25: # PL_NOT_AVAILABLE
                self.available=False
                self._attr_type_n=0
                self.kind="UNKNOWN"
                self._value_access_n=0
                self.value_access="UNKNOWN"
            else:
                raise
        self.readable=self.value_access in {"READ_ONLY","READ_WRITE"}
        self.writable=self.value_access in {"WRITE_ONLY","READ_WRITE"}
        
        self.min=self.max=self.inc=None
        self._cache=None
        self.values=[]
        self.ivalues=[]
        self.labels={}
        self.ilabels={}
        self.update_limits()
        self.default=self._get_default_value() if self.available else None

    def update_limits(self):
        """Update attribute constraints"""
        if not self.available:
            return
        if self._attr_type_n==pvcam_defs.PARAM_TYPE.TYPE_ENUM:
            n=lib.get_param(self.handle,self.pid,pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_COUNT,pvcam_defs.PARAM_TYPE.TYPE_UNS32)
            evals=[lib.get_enum_value(self.handle,self.pid,v) for v in range(n)]
            self.values=list([py3.as_str(sv) for _,sv in evals])
            self.ivalues=list([iv for iv,_ in evals])
            self.labels=dict(zip(self.values,self.ivalues))
            self.ilabels=dict(zip(self.ivalues,self.values))
        if self._attr_type_n in lib.numeric_params:
            try:
                self.min=lib.get_param(self.handle,self.pid,pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_MIN,self._attr_type_n)
                self.max=lib.get_param(self.handle,self.pid,pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_MAX,self._attr_type_n)
                self.inc=lib.get_param(self.handle,self.pid,pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_INCREMENT,self._attr_type_n)
            except PvcamLibError:
                self.min=self.max=self.inc=None
    def truncate_value(self, value):
        """Truncate value to lie within attribute limits"""
        self.update_limits()
        if self._attr_type_n in lib.numeric_params:
            if value<self.min:
                value=self.min
            elif value>self.max:
                value=self.max
            else:
                if self.inc>0:
                    value=((value-self.min)//self.inc)*self.inc+self.min
        return value

    def _get_default_value(self, enum_as_str=True):
        try:
            value=lib.get_param(self.handle,self.pid,param_attribute=pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_DEFAULT,typ=self._attr_type_n)
        except PvcamLibError:
            return None
        if enum_as_str and self._attr_type_n==pvcam_defs.PARAM_TYPE.TYPE_ENUM:
            value=self.ilabels.get(value,value)
        if self._attr_type_n==pvcam_defs.PARAM_TYPE.TYPE_BOOLEAN:
            value=bool(value)
        return value
    def get_value(self, enum_as_str=True, error_on_noacq=True):
        """
        Get attribute value.
        
        If ``enum_as_str==True``, return enum-style values as strings; otherwise, return corresponding integer values.
        """
        if self.cam is not None and self.cam.acquisition_in_progress():
            if self._cache is None:
                return None
            value=self._cache
        else:
            try:
                value=lib.get_param(self.handle,self.pid,typ=self._attr_type_n)
            except PvcamLibError as err:
                if not error_on_noacq and err.code==188: # PL_ERR_ACQUISITION_SETUP_REQUIRED
                    self._cache=None
                    return
                raise
            self._cache=value
        if enum_as_str and self._attr_type_n==pvcam_defs.PARAM_TYPE.TYPE_ENUM:
            value=self.ilabels[value]
        if self._attr_type_n==pvcam_defs.PARAM_TYPE.TYPE_BOOLEAN:
            value=bool(value)
        return value
    def set_value(self, value, truncate=True):
        """
        Set attribute value.
        
        If ``truncate==True``, automatically truncate value to lie within allowed range.
        """
        if self.cam is not None and self.cam.acquisition_in_progress():
            raise PvcamError("can not set attribute values during acquisition")
        if truncate:
            value=self.truncate_value(value)
        value=self.labels.get(value,value)
        if self._attr_type_n==pvcam_defs.PARAM_TYPE.TYPE_ENUM and value not in self.ivalues:
            raise PvcamAttributeValueError(self.name,value,self.ivalues)
        lib.set_param(self.handle,self.pid,value,typ=self._attr_type_n)

    def __repr__(self):
        return "{}(name='{}', kind='{}')".format(self.__class__.__name__,self.name,self.kind)








TDeviceInfo=collections.namedtuple("TDeviceInfo",["vendor","product","chip","system","part","serial"])
TFrameInfo=collections.namedtuple("TFrameInfo",["frame_index","timestamp_start_ns","timestamp_end_ns","framestamp","flags","exposure_ns"])
TReadoutInfo=collections.namedtuple("TReadoutInfo",["port_idx","port_name","speed_idx","speed_freq","gain_idx","gain_name"])
class PvcamCamera(camera.IBinROICamera, camera.IExposureCamera, camera.IAttributeCamera):
    """
    Generic Pvcam camera interface.

    Args:
        serial_number: camera serial number; if ``None``, connect to the first non-used camera
    """
    Error=PvcamError
    TimeoutError=PvcamTimeoutError
    _TFrameInfo=TFrameInfo
    _clear_pausing_acquisition=True
    def __init__(self, name=None):
        super().__init__()
        self.name=name
        self.handle=None
        self._buffer=None
        self._max_buff_size=2**32
        self._frame_bytes=None
        self._buffer_frames=None
        self._acq_in_progress=False
        self._cb=None
        self._acq_nframes=0
        self.open()
        self._add_info_variable("device_info",self.get_device_info)
        self._add_info_variable("pixel_size",self.get_pixel_size)
        self._add_info_variable("pixel_distance",self.get_pixel_distance)
        self._add_settings_variable("temperature",self.get_temperature_setpoint,self.set_temperature)
        self._add_status_variable("temperature_monitor",self.get_temperature)
        self._add_settings_variable("fan_mode",self.get_fan_mode,self.set_fan_mode)
        self._add_info_variable("binning_modes",self.get_supported_binning_modes)
        self._add_settings_variable("metadata_enabled",self.is_metadata_enabled,self.enable_metadata)
        self._add_settings_variable("clear_mode",self.get_clear_mode,self.set_clear_mode)
        self._add_settings_variable("clear_cycles",self.get_clear_cycles,self.set_clear_cycles)
        self._add_settings_variable("readout_mode",lambda: self.get_readout_mode(full=False),self.set_readout_mode)
        self._add_info_variable("readout_modes",self.get_all_readout_modes)
        self._add_settings_variable("trigger_mode",self.get_trigger_mode,self.set_trigger_mode)
        self._update_device_variable_order("exposure")
        self._add_status_variable("clearing_time",self.get_clearing_time)
        self._add_status_variable("frame_period",self.get_frame_period)


    def _get_connection_parameters(self):
        return self.name
    def open(self):
        """Open connection to the camera"""
        if self.handle is not None:
            return
        with libctl.temp_open():
            cams=list_cameras()
            if not cams:
                raise PvcamError("no cameras are avaliable")
            if self.name is None:
                self.name=cams[0]
            elif self.name not in cams:
                raise PvcamError("camera with name {} isn't present among available cameras: {}".format(self.name,cams))
            self.handle=lib.pl_cam_open(self.name,pvcam_defs.PL_OPEN_MODES.OPEN_EXCLUSIVE)
            self._opid=libctl.open().opid
            with self._close_on_error():
                self._update_attributes()
                self._setup_full_roi()
                self._setup_bin_ranges()
                self._readout_modes=self._detect_readout_modes()
                self.set_exposure(0)
    def close(self):
        """Close connection to the camera"""
        if self.handle is not None:
            self.clear_acquisition()
            lib.pl_cam_close(self.handle)
            self.handle=None
            libctl.close(self._opid)
    def is_opened(self):
        """Check if the device is connected"""
        return self.handle is not None

    def _list_attributes(self):
        atts=[PvcamAttribute(self.handle,p,cam=self) for p in pvcam_defs.PARAM]
        return [a for a in atts if a.available and a._attr_type_n in lib.supported_params]
    def get_attribute_value(self, name, error_on_missing=True, error_on_noacq=False, default=None, enum_as_str=True):  # pylint: disable=arguments-differ
        """
        Get value of an attribute with the given name.
        
        If the value doesn't exist or can not be read and ``error_on_missing==True``, raise error; otherwise, return `default`.
        If `default` is not ``None``, assume that ``error_on_missing==False``.
        If `name` points at a dictionary branch, return a dictionary with all values in this branch.
        If ``enum_as_str==True``, return enum-style values as strings; otherwise, return corresponding integer values.
        """
        return super().get_attribute_value(name,error_on_missing=error_on_missing,default=default,error_on_noacq=error_on_noacq,enum_as_str=enum_as_str)
    def set_attribute_value(self, name, value, truncate=True, error_on_missing=True):  # pylint: disable=arguments-differ
        """
        Set value of an attribute with the given name.
        
        If the value doesn't exist or can not be written and ``error_on_missing==True``, raise error; otherwise, do nothing.
        If `name` points at a dictionary branch, set all values in this branch (in this case `value` must be a dictionary).
        If ``truncate==True``, truncate value to lie within attribute range.
        """
        return super().set_attribute_value(name,value,truncate=truncate,error_on_missing=error_on_missing)
    def get_all_attribute_values(self, root="", enum_as_str=True, error_on_noacq=False):  # pylint: disable=arguments-differ
        """Get values of all attributes with the given `root`"""
        return super().get_all_attribute_values(root=root,enum_as_str=enum_as_str,error_on_noacq=error_on_noacq)
    def set_all_attribute_values(self, settings, root="", truncate=True):  # pylint: disable=arguments-differ
        """
        Set values of all attributes with the given `root`.
        
        If ``truncate==True``, truncate value to lie within attribute range.
        """
        return super().set_all_attribute_values(settings,root=root,truncate=truncate)
    @contextlib.contextmanager
    def _setting_parameter_attribute(self, par):
        try:
            yield
        except PvcamAttributeValueError as err:
            par=self._as_parameter_class(par)
            value=par.i(err.value,device=self) if par.check_value(err.value) else err.value
            all_values=[par.i(v,device=self) for v in err.all_values]
            raise PvcamAttributeValueError(err.name,value,all_values) from err
    
    def get_attribute_range(self, name, error_on_missing=True, default=None, parameter=None):
        """
        Return attribute range.

        For numerical attributes it is a tuple ``(min, max)``, while for enum attributes it is a dictionary ``{index: name}``.
        If ``parameter`` is specified, it is a parameter class used to convert the index for a enum attribute.
        """
        if name in self.attributes or error_on_missing:
            att=self.ca[name]
            att.update_limits()
            if att.kind=="ENUM":
                values=att.ilabels
                if parameter is not None:
                    parameter=self._as_parameter_class(parameter)
                    values={parameter.i(v):n for v,n in values.items()}
                return values
            return (att.min,att.max)
        return default
    def _detect_readout_modes(self):
        modes=[]
        def rng(vmin, vmax):
            return range(vmin,vmax+1)
        for port_idx,port_name in self.get_attribute_range("READOUT_PORT",error_on_missing=False,default={0:"Default"}).items():
            self.set_attribute_value("READOUT_PORT",port_idx,error_on_missing=False)
            for speed_idx in rng(*self.get_attribute_range("SPDTAB_INDEX",error_on_missing=False,default=(0,1))):
                self.set_attribute_value("SPDTAB_INDEX",speed_idx,error_on_missing=False)
                speed_freq=1E9/self.get_attribute_value("PIX_TIME",error_on_missing=False,default=1E9)
                for gain_idx in rng(*self.get_attribute_range("GAIN_INDEX",error_on_missing=False,default=(0,1))):
                    self.set_attribute_value("GAIN_INDEX",gain_idx,error_on_missing=False)
                    gain_name=self.get_attribute_value("GAIN_NAME",error_on_missing=False,default="Default")
                    modes.append(TReadoutInfo(port_idx,port_name,speed_idx,speed_freq,gain_idx,gain_name))
        self.set_attribute_value("READOUT_PORT",0,error_on_missing=False)
        self.set_attribute_value("SPDTAB_INDEX",0,error_on_missing=False)
        self.set_attribute_value("GAIN_INDEX",0,error_on_missing=False)
        return modes
    def get_all_readout_modes(self):
        """
        Get a list of all possible readout modes.

        Return a list of tuples ``(port_idx, port_name, speed_idx, speed_freq, gain_idx, gain_name)``.
        The indices (port, speed, and gain) can be used to set up a particular mode using :meth:`set_readout_mode`.
        """
        return list(self._readout_modes)
    def get_readout_mode(self, full=True):
        """
        Get current readout mode.

        If ``full==True``, return a full tuple ``(port_idx, port_name, speed_idx, speed_freq, gain_idx, gain_name)`` containing the descriptions;
        otherwise, return only indices ``(port_idx, speed_idx, gain_idx)``.
        """
        port_idx=self.get_attribute_value("READOUT_PORT",error_on_missing=False,enum_as_str=False,default=0)
        port_name=self.get_attribute_value("READOUT_PORT",error_on_missing=False,enum_as_str=True,default="Default")
        speed_idx=self.get_attribute_value("SPDTAB_INDEX",error_on_missing=False,default=0)
        speed_freq=1E9/self.get_attribute_value("PIX_TIME",error_on_missing=False,default=1E9)
        gain_idx=self.get_attribute_value("GAIN_INDEX",error_on_missing=False,default=0)
        gain_name=self.get_attribute_value("GAIN_NAME",error_on_missing=False,default="Default")
        return TReadoutInfo(port_idx,port_name,speed_idx,speed_freq,gain_idx,gain_name) if full else (port_idx,speed_idx,gain_idx)
    def set_readout_mode(self, port_idx=None, speed_idx=None, gain_idx=None):
        """
        Set the readout mode.

        Any ``None`` value stays unchanged.
        """
        if port_idx is not None:
            self.set_attribute_value("READOUT_PORT",port_idx,error_on_missing=False)
        if speed_idx is not None:
            self.set_attribute_value("SPDTAB_INDEX",speed_idx,error_on_missing=False)
        if gain_idx is not None:
            self.set_attribute_value("GAIN_INDEX",gain_idx,error_on_missing=False)
        self._setup_acquisition()
        return self.get_readout_mode()

    def get_device_info(self):
        """
        Get camera information.

        Return tuple ``(vendor, product, chip, system, part, serial)``.
        """
        atts=["VENDOR_NAME","PRODUCT_NAME","CHIP_NAME","SYSTEM_NAME","CAMERA_PART_NUMBER","HEAD_SER_NUM_ALPHA"]
        return TDeviceInfo(*[self.get_attribute_value(n,error_on_missing=False) for n in atts])

    def get_pixel_size(self):
        """Get camera pixel size (in m)"""
        return tuple([self.get_attribute_value(v,error_on_missing=False,default=0)*1E-9 for v in ["PIX_SER_SIZE","PIX_PAR_SIZE"]])
    def get_pixel_distance(self):
        """Get camera pixel distance (in m)"""
        return tuple([self.get_attribute_value(v,error_on_missing=False,default=0)*1E-9 for v in ["PIX_SER_DIST","PIX_PAR_DIST"]])

    def get_temperature_setpoint(self):
        """Get the temperature setpoint (in C)"""
        temp=self.get_attribute_value("TEMP_SETPOINT",error_on_missing=False)
        return temp/100 if temp is not None else None
    def get_temperature(self):
        """Get the current camera temperature (in C)"""
        temp=self.get_attribute_value("TEMP",error_on_missing=False)
        return temp/100 if temp is not None else None
    def set_temperature(self, temp):
        """Change the temperature setpoint (in C)"""
        self.set_attribute_value("TEMP_SETPOINT",temp*100,error_on_missing=False)
        return self.get_temperature_setpoint()
    
    _p_fan_mode=interface.EnumParameterClass("fan_mode",
        {   "high":pvcam_defs.PL_FAN_SPEEDS.FAN_SPEED_HIGH,
            "medium":pvcam_defs.PL_FAN_SPEEDS.FAN_SPEED_MEDIUM,
            "low":pvcam_defs.PL_FAN_SPEEDS.FAN_SPEED_LOW,
            "off":pvcam_defs.PL_FAN_SPEEDS.FAN_SPEED_OFF,
            None:None})
    @interface.use_parameters(_returns="fan_mode")
    def get_fan_mode(self):
        """Get current fan mode"""
        return self.get_attribute_value("FAN_SPEED_SETPOINT",error_on_missing=False,enum_as_str=False)
    @interface.use_parameters
    def set_fan_mode(self, fan_mode="high"):
        """Set current fan mode"""
        self.set_attribute_value("FAN_SPEED_SETPOINT",fan_mode,error_on_missing=False)
        return self.get_fan_mode()
    def is_metadata_enabled(self):
        """Check if metadata is enabled"""
        return self.get_attribute_value("METADATA_ENABLED",error_on_missing=False,default=False)
    @camera.acqcleared
    def enable_metadata(self, enable=True):
        """Enable or disable metadata"""
        self.set_attribute_value("METADATA_ENABLED",enable,error_on_missing=False)
        return self.is_metadata_enabled()
    
    _exp_res={  pvcam_defs.PL_EXP_RES_MODES.EXP_RES_ONE_SEC:1,
                pvcam_defs.PL_EXP_RES_MODES.EXP_RES_ONE_MILLISEC:1E-3,
                pvcam_defs.PL_EXP_RES_MODES.EXP_RES_ONE_MICROSEC:1E-6}
    def _get_exp_res(self):
        exp_res=self.get_attribute_value("EXP_RES",error_on_missing=False,default=0,enum_as_str=False)
        return self._exp_res[exp_res]
    def _set_min_exp_res(self):
        if "EXP_RES" in self.ca:
            att=self.ca["EXP_RES"]
            for er in [pvcam_defs.PL_EXP_RES_MODES.EXP_RES_ONE_MICROSEC,pvcam_defs.PL_EXP_RES_MODES.EXP_RES_ONE_MILLISEC,pvcam_defs.PL_EXP_RES_MODES.EXP_RES_ONE_SEC]:
                if er in att.ivalues:
                    att.set_value(er)
                    break
    def get_exposure(self):
        return self.cav["EXPOSURE_TIME"]*self._get_exp_res()
    def set_exposure(self, exposure):
        self._set_min_exp_res()
        self._setup_acquisition(exposure=int(exposure/self._get_exp_res()))
        return self.get_exposure()
    _p_clear_mode=interface.EnumParameterClass("clear_mode",
        {   "never":pvcam_defs.PL_CLEAR_MODES.CLEAR_NEVER,
            "pre_exp":pvcam_defs.PL_CLEAR_MODES.CLEAR_PRE_EXPOSURE,
            "pre_seq":pvcam_defs.PL_CLEAR_MODES.CLEAR_PRE_SEQUENCE,
            "post_seq":pvcam_defs.PL_CLEAR_MODES.CLEAR_POST_SEQUENCE,
            "pre_post_seq":pvcam_defs.PL_CLEAR_MODES.CLEAR_PRE_POST_SEQUENCE,
            "pre_exp_post_seq":pvcam_defs.PL_CLEAR_MODES.CLEAR_PRE_EXPOSURE_POST_SEQ})
    @interface.use_parameters(_returns="clear_mode")
    def get_clear_mode(self):
        """Get sensor clear mode"""
        return self.get_attribute_value("CLEAR_MODE",error_on_missing=False,default=pvcam_defs.PL_CLEAR_MODES.CLEAR_NEVER,enum_as_str=False)
    @interface.use_parameters(mode="clear_mode")
    def set_clear_mode(self, mode):
        """Set sensor clear mode"""
        with self._setting_parameter_attribute("clear_mode"):
            self.set_attribute_value("CLEAR_MODE",mode,error_on_missing=False)
        return self.get_clear_mode()
    def get_clear_cycles(self):
        """Get sensor clear cycles"""
        return self.get_attribute_value("CLEAR_CYCLES",error_on_missing=False,default=0)
    def set_clear_cycles(self, ncycles):
        """Set sensor clear cycles"""
        self.set_attribute_value("CLEAR_CYCLES",ncycles,error_on_missing=False)
        return self.get_clear_cycles()
    def get_clearing_time(self):
        """Get sensor clearing time (regardless of the mode)"""
        if not self.acquisition_in_progress():
            self._setup_acquisition()
        return self.get_attribute_value("CLEARING_TIME",error_on_missing=False,default=0)*1E-9
    def get_readout_time(self, include_clear=True):
        """
        Get frame readout time.
        
        If ``include_clear==True`` and the clear mode is per-exposure (``"Pre-Exposure"`` or ``"Pre-Exposure and Post-Sequence"``), include it into this time.
        """
        ro_time=self.cav["READOUT_TIME"]*1E-6
        if include_clear and self.get_clear_mode() in ["pre_exp","pre_exp_post_seq"]:
            ro_time+=self.get_clearing_time()
        return ro_time
    def get_frame_timings(self):
        exp=self.get_exposure()
        return self._TAcqTimings(exp,exp+self.get_readout_time())

    _p_trigger_mode=interface.EnumParameterClass("trigger_mode",
        {   "timed":pvcam_defs.PL_EXPOSURE_MODES.TIMED_MODE,
            "strobe":pvcam_defs.PL_EXPOSURE_MODES.STROBED_MODE,
            "bulb":pvcam_defs.PL_EXPOSURE_MODES.BULB_MODE,
            "trig_first":pvcam_defs.PL_EXPOSURE_MODES.TRIGGER_FIRST_MODE,
            "var_timed":pvcam_defs.PL_EXPOSURE_MODES.VARIABLE_TIMED_MODE,
            "int_strobe":pvcam_defs.PL_EXPOSURE_MODES.INT_STROBE_MODE,
            "e_int":pvcam_defs.PL_EXPOSURE_MODES.EXT_TRIG_INTERNAL,
            "e_trig_first":pvcam_defs.PL_EXPOSURE_MODES.EXT_TRIG_TRIG_FIRST,
            "e_rise_edge":pvcam_defs.PL_EXPOSURE_MODES.EXT_TRIG_EDGE_RISING,
            "e_level":pvcam_defs.PL_EXPOSURE_MODES.EXT_TRIG_LEVEL,
            "e_soft_first":pvcam_defs.PL_EXPOSURE_MODES.EXT_TRIG_SOFTWARE_FIRST,
            "e_soft_edge":pvcam_defs.PL_EXPOSURE_MODES.EXT_TRIG_SOFTWARE_EDGE,
            "e_level_overlap":pvcam_defs.PL_EXPOSURE_MODES.EXT_TRIG_LEVEL_OVERLAP,
            "e_level_pulsed":pvcam_defs.PL_EXPOSURE_MODES.EXT_TRIG_LEVEL_PULSED})
    _p_trigger_out_mode=interface.EnumParameterClass("trigger_out_mode",
        {   "first_row":pvcam_defs.PL_EXPOSE_OUT_MODES.EXPOSE_OUT_FIRST_ROW,
            "all_rows":pvcam_defs.PL_EXPOSE_OUT_MODES.EXPOSE_OUT_ALL_ROWS,
            "any_row":pvcam_defs.PL_EXPOSE_OUT_MODES.EXPOSE_OUT_ANY_ROW,
            "rolling_shutter":pvcam_defs.PL_EXPOSE_OUT_MODES.EXPOSE_OUT_ROLLING_SHUTTER,
            "line_trigger":pvcam_defs.PL_EXPOSE_OUT_MODES.EXPOSE_OUT_LINE_TRIGGER,
            "global_shutter":pvcam_defs.PL_EXPOSE_OUT_MODES.EXPOSE_OUT_GLOBAL_SHUTTER,
            None:None})
    def _get_exposure_mode(self):
        mode=self.get_attribute_value("EXPOSURE_MODE",error_on_missing=False,default=pvcam_defs.PL_EXPOSURE_MODES.TIMED_MODE,enum_as_str=False)
        if mode>=0x100: # extended mode; mask exposure-out
            mode&=0xFF00
            mode|=self.get_attribute_value("EXPOSE_OUT_MODE",error_on_missing=False,default=pvcam_defs.PL_EXPOSE_OUT_MODES.EXPOSE_OUT_FIRST_ROW,enum_as_str=False)
        return mode
    @interface.use_parameters(_returns=("trigger_mode","trigger_out_mode"))
    def get_trigger_mode(self):
        """Get trigger mode"""
        mode=self.get_attribute_value("EXPOSURE_MODE",error_on_missing=False,default=pvcam_defs.PL_EXPOSURE_MODES.TIMED_MODE,enum_as_str=False)
        if mode>=0x100: # extended mode; mask exposure-out
            mode&=0xFF00
            omode=self.get_attribute_value("EXPOSE_OUT_MODE",error_on_missing=False,default=pvcam_defs.PL_EXPOSE_OUT_MODES.EXPOSE_OUT_FIRST_ROW,enum_as_str=False)
        else:
            omode=None
        return (mode,omode)
    @interface.use_parameters(mode="trigger_mode",out_mode="trigger_out_mode")
    def set_trigger_mode(self, mode, out_mode=None):
        """Set trigger mode"""
        with self._setting_parameter_attribute("trigger_mode"):
            att=self.ca["EXPOSURE_MODE"]
            if mode not in att.ivalues:
                raise PvcamAttributeValueError(att.name,mode,att.ivalues)
        if mode>=0x100:
            if out_mode is None:
                out_mode=self.get_attribute_value("EXPOSE_OUT_MODE",error_on_missing=False,default=pvcam_defs.PL_EXPOSE_OUT_MODES.EXPOSE_OUT_FIRST_ROW,enum_as_str=False)
            mode|=out_mode
        self._setup_acquisition(exp_mode=mode)
        return self.get_trigger_mode()

    def _get_data_dimensions_rc(self):
        roi=self.get_roi()
        w,h=(roi[1]-roi[0])//roi[4],(roi[3]-roi[2])//roi[5]
        return h,w
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        return self.cav["SER_SIZE"],self.cav["PAR_SIZE"]
    def _setup_full_roi(self):
        w,h=self.get_detector_size()
        self._roi=(0,w,0,h,1,1)
        self._setup_acquisition()
    def _setup_bin_ranges(self):
        try:
            binss=list(self.ca["BINNING_SER"].labels)
            def s2t(s):
                h,v=s.split("x")
                return int(h),int(v)
            self._hvbins=sorted([s2t(s) for s in binss])
        except KeyError:
            self._hvbins=None
    def get_roi(self):
        return self._roi
    def _limit_bin(self, hb, vb):
        if self._hvbins is None:
            return hb,vb
        hvb=self._hvbins[0]
        for (thb,tvb) in self._hvbins:
            if (hb,vb)==(thb,tvb):
                return (hb,vb)
            if thb<=hb and tvb<=vb:
                hvb=(thb,tvb)
        return hvb
    @camera.acqcleared
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        hbin,vbin=self._limit_bin(hbin,vbin)
        hlim,vlim=self.get_roi_limits(hbin,vbin)
        hstart,hend,_=self._roi=camera.truncate_roi_axis((hstart,hend,hbin),hlim)
        vstart,vend,_=self._roi=camera.truncate_roi_axis((vstart,vend,vbin),vlim)
        self._roi=(hstart,hend,vstart,vend,hbin,vbin)
        self._setup_acquisition()
        return self.get_roi()
    def get_roi_limits(self, hbin=1, vbin=1):
        wdet,hdet=self.get_detector_size()
        hlim=camera.TAxisROILimit(max(2*hbin,4),wdet,hbin,hbin,max([hb for hb,_ in self._hvbins]))
        vlim=camera.TAxisROILimit(max(2*vbin,4),hdet,vbin,vbin,max([vb for _,vb in self._hvbins]))
        return hlim,vlim
    def get_supported_binning_modes(self):
        """Get all possible binning combinations as a list ``[(hbin, vbin)]``"""
        return self._hvbins if self._hvbins is not None else None
    

    def _allocate_buffer(self, frame_bytes, nframes):
        self._deallocate_buffer()
        self._frame_bytes=frame_bytes
        self._buffer_frames=nframes
        self._buffer=ctypes.create_string_buffer(frame_bytes*nframes)
    def _deallocate_buffer(self):
        self._buffer=None
    def _on_callback(self, frame_info, context):
        pass
    def _register_callback(self):
        self._deregister_callback()
        self._cb=lib.pl_cam_register_callback_ex3(self.handle,pvcam_defs.PL_CALLBACK_EVENT.PL_CALLBACK_EOF,self._on_callback,wrap=False)
    def _deregister_callback(self):
        if self._cb is not None:
            lib.pl_cam_deregister_callback(self.handle,pvcam_defs.PL_CALLBACK_EVENT.PL_CALLBACK_EOF)
            self._cb=None
    def _try_setup_acquisition(self, roi=None, exp_mode=None, exposure=None, acq_nframes=None):
        if roi is None:
            roi=self._roi
        if exposure is None:
            exposure=self.cav["EXPOSURE_TIME"]
        if exp_mode is None:
            exp_mode=self._get_exposure_mode()
        if acq_nframes is None:
            acq_nframes=self._acq_nframes
        self._acq_nframes=acq_nframes
        r0,r1,c0,c1,rb,cb=roi
        if acq_nframes<=0:
            return lib.pl_exp_setup_cont(self.handle,[(r0,r1-1,rb,c0,c1-1,cb)],exp_mode,exposure,pvcam_defs.PL_CIRC_MODES.CIRC_OVERWRITE)
        else:
            total_size=lib.pl_exp_setup_seq(self.handle,acq_nframes,[(r0,r1-1,rb,c0,c1-1,cb)],exp_mode,exposure)
            if total_size%acq_nframes:
                raise RuntimeError("sequence buffer size {} does not divide the number of frames {}".format(total_size,acq_nframes))
            return total_size//acq_nframes
    def _setup_acquisition(self, roi=None, exp_mode=None, exposure=None, acq_nframes=None):
        roi0=roi or self._roi
        roi=roi0
        roi_div=1
        bin_invalid=False
        def rrnd(v, up):
            return ((v-1)//roi_div+1)*roi_div if up else (v//roi_div)*roi_div
        for i in range(16):
            try:
                buffsize=self._try_setup_acquisition(roi=roi,exp_mode=exp_mode,exposure=exposure,acq_nframes=acq_nframes)
                if roi_div>1 or bin_invalid:
                    self.set_roi(*roi)
                return buffsize
            except PvcamLibError as err:
                if i==15:
                    raise
                if err.code==181:  # PL_ERR_REGION_INVALID
                    roi_div*=2
                elif err.code==182:  # PL_ERR_BINNING_INVALID
                    bin_invalid=True
                else:
                    raise
            roi=(rrnd(roi0[0],False),rrnd(roi0[1],True),rrnd(roi0[2],False),rrnd(roi0[3],True))+((1,1) if bin_invalid else roi[4:])

    @interface.use_parameters(mode="acq_mode")
    def setup_acquisition(self, mode="sequence", nframes=100):  # pylint: disable=arguments-differ
        """
        Setup acquisition mode.

        `mode` can be either ``"snap"`` (single frame or a fixed number of frames) or ``"sequence"`` (continuous acquisition).
        `nframes` sets up number of frame buffers.
        """
        self.clear_acquisition()
        super().setup_acquisition(mode=mode,nframes=nframes)
        buffsize=self._setup_acquisition(acq_nframes=self._acq_params["nframes"] if mode=="snap" else 0)
        if self._acq_params["nframes"]*buffsize>self._max_buff_size-1:
            return self.setup_acquisition(mode=mode,nframes=(self._max_buff_size-1)//buffsize)
        self._allocate_buffer(buffsize,self._acq_params["nframes"])
    def clear_acquisition(self):
        self.stop_acquisition()
        self._deallocate_buffer()
        super().clear_acquisition()
    def _try_start_acquisition(self, *args, **kwargs):
        self.stop_acquisition()
        super().start_acquisition(*args,**kwargs)
        self._frame_counter.reset(self._acq_params["nframes"])
        self.get_all_attribute_values()
        if self._acq_nframes<=0:
            lib.pl_exp_start_cont(self.handle,self._buffer,len(self._buffer))
        else:
            lib.pl_exp_start_seq(self.handle,self._buffer)
        self._acq_in_progress=True
    def start_acquisition(self, *args, **kwargs):
        while True:
            try:
                return self._try_start_acquisition(*args,**kwargs)
            except PvcamLibError as err:
                if err.code==199: # PL_ERR_DDI_DEVICE_IOCTL_FAILED
                    self._max_buff_size//=2
                    acq_params=self._acq_params
                    lib.pl_exp_abort(self.handle,pvcam_defs.PL_CCS_ABORT_MODES.CCS_HALT_CLOSE_SHTR)
                    self.clear_acquisition()
                    self.setup_acquisition(**acq_params)
                else:
                    raise
    def _abort_acquisition(self):
        self._frame_counter.update_acquired_frames(self._get_acquired_frames())
        lib.pl_exp_abort(self.handle,pvcam_defs.PL_CCS_ABORT_MODES.CCS_HALT_CLOSE_SHTR)
        self._acq_in_progress=False
    def stop_acquisition(self):
        if self.acquisition_in_progress():
            self._abort_acquisition()
        super().stop_acquisition()
    def acquisition_in_progress(self):
        if not self._acq_in_progress:
            return False
        if self._acq_nframes>0 and lib.pl_exp_check_status(self.handle)[0]==pvcam_defs.PL_IMAGE_STATUSES.READOUT_COMPLETE:
            self._abort_acquisition()
            return False
        return True
    def _get_acquired_frames(self):
        if self._buffer is None:
            return None
        if self._acq_nframes<=0:
            status=lib.pl_exp_check_cont_status_ex(self.handle)
            frame_info=status[-1]
            return frame_info.FrameNr
        else:
            status=lib.pl_exp_check_status(self.handle)
            bytes_arrived=status[-1]
            return bytes_arrived//self._frame_bytes
    

    _support_chunks=True
    def _get_frame_params(self):
        bypp=(self.cav["BIT_DEPTH"]-1)//8+1
        shape=self._get_data_dimensions_rc()
        return shape,bypp
    def _parse_frames_data(self, ptr, nframes, shape, bypp, off=0):
        stride=self._frame_bytes
        buffer=np.ctypeslib.as_array(ctypes.cast(ptr,ctypes.POINTER(ctypes.c_ubyte)),shape=(stride*nframes,))
        size=shape[0]*shape[1]*bypp
        dtype="<u{}".format(bypp)
        framedata=np.empty(nframes*size,dtype="u1")
        if size==stride:
            copy_simple(buffer,framedata,nframes,size)
        else:
            copy_strided(buffer,framedata,nframes,size,stride,off=off)
        frames=framedata.view(dtype).reshape((nframes,)+shape)
        frames=self._convert_indexing(frames,"rct",axes=(1,2))
        return frames
    def _parse_md_frames_data(self, ptr, nframes, start_index):
        stride=self._frame_bytes
        buffer=np.ctypeslib.as_array(ctypes.cast(ptr,ctypes.POINTER(ctypes.c_ubyte)),shape=(stride*nframes,))
        roi_info=get_roi_parameters(buffer)
        off=roi_info[0,0]
        bypp=roi_info[0,1]
        shape=tuple(roi_info[0,2:4])
        frames=self._parse_frames_data(ptr,nframes,shape,bypp,off=off)
        v3=buffer[4]>=3
        metainfo=parse_metainfo_v3(buffer,nframes,stride) if v3 else parse_metainfo_v1(buffer,nframes,stride)
        return frames,self._md_to_frame_info(metainfo,start_index,v3=v3)
    def _md_to_frame_info(self, metainfo, start_index, v3=False):
        if v3:
            timestamp_start_ns=metainfo[:,1]//1000
            timestamp_end_ns=metainfo[:,2]//1000
            exposure_ns=metainfo[:,3]//1000
        else:
            timestamp_start_ns=metainfo[:,1].astype("u8")*metainfo[:,3]
            timestamp_end_ns=metainfo[:,2].astype("u8")*metainfo[:,3]
            exposure_ns=metainfo[:,4].astype("u8")*metainfo[:,5]
        frame_indices=np.arange(len(metainfo),dtype=timestamp_start_ns.dtype)+start_index
        return np.column_stack((frame_indices,timestamp_start_ns,timestamp_end_ns,metainfo[:,0],metainfo[:,-1],exposure_ns)).astype("i8")
    def _read_frames(self, rng, return_info=False):
        shape,bypp=self._get_frame_params()
        base=ctypes.addressof(self._buffer)
        start=rng[0]%self._buffer_frames
        stop=start+(rng[1]-rng[0])
        if stop<=self._buffer_frames:
            chunks=[(rng[0],start,stop-start)]
        else:
            l0=self._buffer_frames-start
            chunks=[(rng[0],start,l0),(rng[0]+l0,0,stop-start-l0)]
        if self.is_metadata_enabled():
            data=[self._parse_md_frames_data(base+s*self._frame_bytes,l,idx) for (idx,s,l) in chunks]
            frames=[f for f,_ in data]
            frame_info=[i for _,i in data]
        else:
            frames=[self._parse_frames_data(base+s*self._frame_bytes,l,shape,bypp) for (_,s,l) in chunks]
            frame_info=None
        return frames,frame_info
    def _zero_frame(self, n):
        dim=self.get_data_dimensions()
        _,bypp=self._get_frame_params()
        dt="<u{}".format(bypp)
        return np.zeros((n,)+dim,dtype=dt)
    def read_multiple_images(self, rng=None, peek=False, missing_frame="skip", return_info=False, return_rng=False):
        """
        Read multiple images specified by `rng` (by default, all un-read images).

        If `rng` is specified, it is a tuple ``(first, last)`` with images range (first inclusive).
        If no new frames are available, return an empty list; if no acquisition is running, return ``None``.
        If ``peek==True``, return images but not mark them as read.
        `missing_frame` determines what to do with frames which are out of range (missing or lost):
        can be ``"none"`` (replacing them with ``None``), ``"zero"`` (replacing them with zero-filled frame), or ``"skip"`` (skipping them).
        If ``return_info==True``, return tuple ``(frames, infos)``, where ``infos`` is a list of :class:`TFrameInfo` instances
        describing frame index and frame metadata, which contains start and stop timestamps, framestamp, frame flags, and exposure;
        if some frames are missing and ``missing_frame!="skip"``, the corresponding frame info is ``None``.
        if ``return_rng==True``, return the range covered resulting frames; if ``missing_frame=="skip"``, the range can be smaller
        than the supplied `rng` if some frames are skipped.
        """
        return super().read_multiple_images(rng=rng,peek=peek,missing_frame=missing_frame,return_info=return_info,return_rng=return_rng)
    def _get_grab_acquisition_parameters(self, nframes, buff_size):
        params=super()._get_grab_acquisition_parameters(nframes,buff_size)
        if params["mode"]=="snap":
            params["nframes"]+=2+int(.05/self.get_frame_period())  # looks like the first/last several frame get missing sometimes
        return params



_par=False
copy_strided=nbtools.copy_array_strided(par=_par)
copy_simple=nbtools.copy_array_chunks(par=_par)
u1_1_RC=nbtools.c_array("u1",ndim=1,readonly=True)

def _get_img_size(buffer, roi_off):
    s1=au2(buffer,roi_off+10)
    s2=au2(buffer,roi_off+12)
    sbin=au2(buffer,roi_off+14)
    ssz=(s2-s1+1)//sbin
    p1=au2(buffer,roi_off+16)
    p2=au2(buffer,roi_off+18)
    pbin=au2(buffer,roi_off+20)
    psz=(p2-p1+1)//pbin
    return np.array([ssz,psz])
def get_roi_parameters(buffer):
    """
    Extract ROI parameters from the buffer.
    
    `buffer` is the buffer represented as bytes numpy byte array.
    Return numpy array with one row per ROI and 4 columns:
    data offset from the frame start, data bytes per pixel, ROI height, and ROI width.
    """
    nrois=au2(buffer,9)
    roi_data=np.empty((nrois,4),dtype="u4")
    bypp=(buffer[35]-1)//8+1
    roi_off=48+au2(buffer,38)
    for i in range(nrois):
        ssz,psz=_get_img_size(buffer,roi_off)
        resize=au2(buffer,roi_off+23)
        roi_data[i,0]=roi_off+32
        roi_data[i,1]=bypp
        roi_data[i,2]=psz
        roi_data[i,3]=ssz
        imbytes=ssz*psz*bypp
        roi_off=32+resize+imbytes
    return roi_data
@nb.njit(nb.u4[:,:](u1_1_RC,nb.u8,nb.u8))
def parse_metainfo_v1(buffer, nframes, stride):
    """
    Extract frames metainfo for frames with v1 or v2 header.

    `buffer` is the buffer represented as bytes numpy byte array, `nframes` is the number of frames in it,
    and `stride` is the frame stride (in bytes).

    Return a 2D array with `nframes` rows and 7 columns:
    ``framestamp, timestampBOF, timestampEOF, timestampRes, exposure, exposureRes, flags``.
    """
    p=nb.u8(0)
    metainfo=np.empty((nframes,7),dtype=nb.u4)
    for f in range(nframes):
        i=0
        for o in [5,11,15,19,23,27]:
            metainfo[f,i]=au4(buffer,p+o)
            i+=1
        metainfo[f,6]=buffer[p+37]
        p+=stride
    return metainfo
@nb.njit(nb.u8[:,:](u1_1_RC,nb.u8,nb.u8))
def parse_metainfo_v3(buffer, nframes, stride):
    """
    Extract frames metainfo for frames with v3 header.

    `buffer` is the buffer represented as bytes numpy byte array, `nframes` is the number of frames in it,
    and `stride` is the frame stride (in bytes).

    Return a 2D array with `nframes` rows and 5 columns:
    ``framestamp, timestampBOF, timestampEOF, exposure, flags``.
    """
    p=nb.u8(0)
    metainfo=np.empty((nframes,5),dtype=nb.u8)
    for f in range(nframes):
        metainfo[f,0]=au4(buffer,p+5)
        i=1
        for o in [11,19,27]:
            metainfo[f,i]=au8(buffer,p+o)
            i+=1
        metainfo[f,4]=buffer[p+37]
        p+=stride
    return metainfo