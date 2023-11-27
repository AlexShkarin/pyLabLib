from .base import AndorError, AndorNotSupportedError
from .ShamrockCIF_lib import wlib as lib, ShamrockLibError, SHAMROCK_ERR, SHAMROCK_CONST
from .AndorSDK2 import _camsel_lock

from ...core.devio import interface
from ...core.utils import py3
from ..utils import load_lib

import numpy as np
import collections
import functools


_detector_ini_path=""
class LibraryController(load_lib.LibraryController):
    def _do_init(self):
        self.lib.ShamrockInitialize(_detector_ini_path)
    def _do_uninit(self):
        try:
            self.lib.ShamrockClose()
        except ShamrockLibError as e:
            if e.code!=SHAMROCK_ERR.SHAMROCK_NOT_INITIALIZED:
                raise
libctl=LibraryController(lib)
def restart_lib():
    libctl.shutdown()

def list_spectrographs():
    """Return list of serial numbers of all connected Shamrock spectrographs"""
    with libctl.temp_open():
        spec_num=lib.ShamrockGetNumberDevices()
        return [py3.as_str(lib.ShamrockGetSerialNumber(i)) for i in range(spec_num)]
def get_spectrographs_number():
    """Get number of connected Shamrock spectrographs"""
    return len(list_spectrographs())


TDeviceInfo=collections.namedtuple("TDeviceInfo",["serial_number"])
TOpticalParameters=collections.namedtuple("TOpticalParameters",["focal_length","angular_deviation","focal_tilt"])
TGratingInfo=collections.namedtuple("TGratingInfo",["lines","blaze_wavelength","home","offset"])

def _specfunc(func):
    @functools.wraps(func)
    def wrapped(self, *args, **kwargs):
        if getattr(self,"_sync_with_SDK2",False):
            with _camsel_lock:
                return func(self,*args,**kwargs)
        return func(self,*args,**kwargs)
    return wrapped
class ShamrockSpectrograph(interface.IDevice):
    """
    Shamrock spectrograph.

    Args:
        idx(int): spectrograph index (starting from 0; use :func:`list_spectrographs` to get the list of all connected spectrographs)
    """
    Error=AndorError
    def __init__(self, idx=0):
        super().__init__()
        self.idx=idx
        self._opid=None
        self.open()
        
        self._sync_with_SDK2=False
        self._add_info_variable("device_info",self.get_device_info)
        self._add_info_variable("optical_parameters",self.get_optical_parameters)
        self._add_info_variable("gratings_number",self.get_gratings_number)
        self._add_status_variable("grating_infos",lambda: [self.get_grating_info(g) for g in range(1,self.get_gratings_number()+1)])
        self._add_settings_variable("grating",self.get_grating,self.set_grating)
        self._add_settings_variable("grating_offsets",self._get_all_grating_offsets,self._set_all_grating_offsets)
        self._add_settings_variable("detector_offset",self.get_detector_offset,self.set_detector_offset)
        self._add_info_variable("wavelength_present",self.is_wavelength_control_present)
        self._add_info_variable("wavelength_limits",lambda: [self.get_wavelength_limits(g) for g in range(1,self.get_gratings_number()+1)],ignore_error=(AndorError,))
        self._add_settings_variable("wavelength",self.get_wavelength,self.set_wavelength,ignore_error=(AndorError,))
        self._add_status_variable("zero_order",self.is_at_zero_order,ignore_error=(AndorError,))
        self._add_info_variable("slits_present",lambda: [self.is_slit_present(s) for s in range(1,5)])
        self._add_settings_variable("slit_widths",self._get_all_slit_widths,self._set_all_slit_widths)
        self._add_info_variable("irises_present",lambda: [self.is_iris_present(s) for s in range(2)])
        self._add_settings_variable("iris_widths",self._get_all_iris_widths,self._set_all_iris_widths)
        self._add_settings_variable("focus_mirror_present",self.is_focus_mirror_present)
        self._add_settings_variable("focus_mirror",self.get_focus_mirror_position,self.set_focus_mirror_position,ignore_error=(AndorError,))
        self._add_info_variable("focus_mirror_max",self.get_focus_mirror_position_max,ignore_error=(AndorError,))
        self._add_info_variable("shutter_present",self.is_shutter_present)
        self._add_settings_variable("shutter_mode",self.get_shutter,self.set_shutter,ignore_error=(AndorError,))
        self._add_info_variable("filter_present",self.is_filter_present)
        self._add_settings_variable("filter",self.get_filter,self.set_filter,ignore_error=(AndorError,))
        self._add_info_variable("flippers_present",lambda: [self.is_flipper_present(s) for s in range(1,3)])
        self._add_settings_variable("flipper_ports",self._get_all_flipper_ports,self._set_all_flipper_ports)
        self._add_info_variable("accessory_present",self.is_accessory_present)
        self._add_settings_variable("accessory_states",self._get_all_accessory_states,self._set_all_accessory_states)
        self._add_settings_variable("pixel_width",self.get_pixel_width,self.set_pixel_width)
        self._add_settings_variable("number_pixels",self.get_number_pixels,self.set_number_pixels)
        self._add_status_variable("calibration",self.get_calibration)

    def open(self):
        if self._opid:
            return
        with libctl.temp_open():
            ncams=get_spectrographs_number()
            if self.idx>=ncams:
                raise AndorError("spectrograph index {} is not available ({} spectrograph exist)".format(self.idx,ncams))
            self._opid=libctl.open().opid
    def close(self):
        if self._opid is None:
            return
        libctl.close(self._opid)
        self._opid=None
    def is_opened(self):
        return self._opid is not None
    def _get_connection_parameters(self):
        return (self.idx,)

    @_specfunc
    def get_device_info(self):
        """
        Get spectrograph device info.

        Return tuple ``(serial_number)``.
        """
        serial_number=py3.as_str(lib.ShamrockGetSerialNumber(self.idx))
        return TDeviceInfo(serial_number)
    @_specfunc
    def get_optical_parameters(self):
        """
        Get device optical parameters.

        Return tuple ``(focal_length, angular_deviation, focal_tilt)``.
        """
        params=lib.ShamrockEepromGetOpticalParams(self.idx)
        return TOpticalParameters(*params)
        
    
    ### Grating control ###
    @_specfunc
    def get_gratings_number(self):
        """Get number of gratings"""
        return lib.ShamrockGetNumberGratings(self.idx)
    def _check_grating(self, grating):
        if grating is None:
            return self.get_grating()
        if grating<1 or grating>self.get_gratings_number():
            raise ValueError("incorrect grating index: {}; should be between 1 and {}".format(grating,self.get_gratings_number()))
        return grating
    @_specfunc
    def get_grating(self):
        """Get current grating index (counting from 1)"""
        return lib.ShamrockGetGrating(self.idx)
    @_specfunc
    def set_grating(self, grating, force=False):
        """
        Set current grating (counting from 1)
        
        Call blocks until the grating is exchanged (up to 10-20 seconds).
        If ``force==False`` and the current grating index is the same as requested, skip the call;
        otherwise, call the grating set command regardless (takes about a second in the grating is unchanged).
        """
        grating=self._check_grating(grating)
        if force or self.get_grating()!=grating:
            lib.ShamrockSetGrating(self.idx,grating)
        return self.get_grating()
    @_specfunc
    def get_grating_info(self, grating=None):
        """
        Get info of a given grating (by default, current grating).

        Return tuple ``(lines, blaze_wavelength, home, offset)`` (blazing wavelength is in nm).
        """
        grating=self._check_grating(grating)
        lines,blaze_wavelength,home,offset=lib.ShamrockGetGratingInfo(self.idx,grating)
        return TGratingInfo(lines,py3.as_str(blaze_wavelength),home,offset)
    @_specfunc
    def get_grating_offset(self, grating=None):
        """Get grating offset (in steps) for a given grating (by default, current grating)"""
        grating=self._check_grating(grating)
        return lib.ShamrockGetGratingOffset(self.idx,grating)
    @_specfunc
    def set_grating_offset(self, offset, grating=None):
        """Set grating offset (in steps) for a given grating (by default, current grating)"""
        grating=self._check_grating(grating)
        lib.ShamrockSetGratingOffset(self.idx,grating,offset)
        return self.get_grating_offset(grating)
    def _get_all_grating_offsets(self):
        return [self.get_grating_offset(g) for g in range(1,self.get_gratings_number()+1)]
    def _set_all_grating_offsets(self, offsets):
        for g,o in enumerate(offsets,start=1):
            if o is not None:
                self.set_grating_offset(g,o)
    @_specfunc
    def get_detector_offset(self):
        """Get detector offset (in steps)"""
        return lib.ShamrockGetDetectorOffset(self.idx)
    @_specfunc
    def set_detector_offset(self, offset):
        """Set detector offset (in steps)"""
        lib.ShamrockSetDetectorOffset(self.idx,offset)
        return self.get_detector_offset()
    @_specfunc
    def get_turret(self):
        """Get turret"""
        return lib.ShamrockGetTurret(self.idx)
    @_specfunc
    def set_turret(self, turret):
        """Set turret"""
        lib.ShamrockSetTurret(self.idx,turret)
        return self.get_turret()
        
    
    ### Wavelength control ###
    @_specfunc
    def is_wavelength_control_present(self):
        """Check if wavelength control is present"""
        return bool(lib.ShamrockWavelengthIsPresent(self.idx))
    def _check_wavelength(self):
        if not self.is_wavelength_control_present():
            raise AndorNotSupportedError("wavelength control is not present")
    @_specfunc
    def get_wavelength(self):
        """Get current central wavelength (in m)"""
        self._check_wavelength()
        return lib.ShamrockGetWavelength(self.idx)*1E-9
    @_specfunc
    def set_wavelength(self, wavelength):
        """Get current central wavelength (in m)"""
        self._check_wavelength()
        lib.ShamrockSetWavelength(self.idx,wavelength/1E-9)
        return self.get_wavelength()
    @_specfunc
    def get_wavelength_limits(self, grating=None):
        """Get wavelength limits (in m) for a given grating (by default, current grating)"""
        self._check_wavelength()
        grating=self._check_grating(grating)
        lim=lib.ShamrockGetWavelengthLimits(self.idx,grating)
        return lim[0]*1E-9,lim[1]*1E-9
    @_specfunc
    def reset_wavelength(self):
        """Reset current wavelength to 0 nm"""
        self._check_wavelength()
        lib.ShamrockWavelengthReset(self.idx)
        return self.get_wavelength()
    @_specfunc
    def is_at_zero_order(self):
        """Check if current grating is at zero order"""
        self._check_wavelength()
        return bool(lib.ShamrockAtZeroOrder(self.idx))
    @_specfunc
    def goto_zero_order(self):
        """Set current grating to zero order"""
        self._check_wavelength()
        lib.ShamrockGotoZeroOrder(self.idx)
        return self.is_at_zero_order()
        

    ### Slit control ###
    _p_slit_index=interface.EnumParameterClass("slit_index",
        {"input_side":SHAMROCK_CONST.SHAMROCK_INPUT_SLIT_SIDE,"input_direct":SHAMROCK_CONST.SHAMROCK_INPUT_SLIT_DIRECT,
        "output_side":SHAMROCK_CONST.SHAMROCK_OUTPUT_SLIT_SIDE,"output_direct":SHAMROCK_CONST.SHAMROCK_OUTPUT_SLIT_DIRECT})
    @interface.use_parameters(slit="slit_index")
    @_specfunc
    def is_slit_present(self, slit):
        """
        Check if the slit is present.

        `slit` cen be either a slit index (starting from 1), or one of the following: ``"input_side"``, ``"input_direct"``, ``"output_side"``, or ``"output_direct"``.
        """
        return bool(lib.ShamrockAutoSlitIsPresent(self.idx,slit))
    def _check_slit(self, slit):
        if not self.is_slit_present(slit):
            raise AndorNotSupportedError("slit '{}' is not present".format(self._p_slit_index.i(slit)))
    @interface.use_parameters(slit="slit_index")
    @_specfunc
    def get_slit_width(self, slit):
        """
        Get slit width (in m).

        `slit` cen be either a slit index (starting from 1), or one of the following: ``"input_side"``, ``"input_direct"``, ``"output_side"``, or ``"output_direct"``.
        """
        self._check_slit(slit)
        return lib.ShamrockGetAutoSlitWidth(self.idx,slit)*1E-6
    @interface.use_parameters(slit="slit_index")
    @_specfunc
    def set_slit_width(self, slit, width):
        """
        Set slit width (in m).

        `slit` cen be either a slit index (starting from 1), or one of the following: ``"input_side"``, ``"input_direct"``, ``"output_side"``, or ``"output_direct"``.
        """
        self._check_slit(slit)
        lib.ShamrockSetAutoSlitWidth(self.idx,slit,width/1E-6)
        return self._wip.get_slit_width(slit)
    def _get_all_slit_widths(self):
        return [self.get_slit_width(s) if self.is_slit_present(s) else None for s in range(1,5)]
    def _set_all_slit_widths(self, widths):
        for s,w in enumerate(widths,start=1):
            if w is not None:
                self.set_slit_width(s,w)
    @interface.use_parameters(slit="slit_index")
    @_specfunc
    def reset_slit(self, slit):
        """
        Reset slit to the default width (10 um).

        `slit` cen be either a slit index (starting from 1), or one of the following: ``"input_side"``, ``"input_direct"``, ``"output_side"``, or ``"output_direct"``.
        """
        self._check_slit(slit)
        lib.ShamrockAutoSlitReset(self.idx,slit)
        return self._wip.get_slit_width(slit)
        

    ### Shutter control ###
    @_specfunc
    def is_shutter_present(self):
        """Check if the shutter is present"""
        return bool(lib.ShamrockShutterIsPresent(self.idx))
    def _check_shutter(self):
        if not self.is_shutter_present():
            raise AndorNotSupportedError("shutter is not present")
    _p_shutter_mode=interface.EnumParameterClass("shutter_mode",{"closed":0,"opened":1,"bnc":2,"not_set":-1})
    @interface.use_parameters(_returns="shutter_mode")
    @_specfunc
    def get_shutter(self):
        """
        Get shutter mode.

        Can return ``"closed"``, ``"opened"``, ``"bnc"``, or ``"not_set"``.
        """
        self._check_shutter()
        return lib.ShamrockGetShutter(self.idx)
    @interface.use_parameters(mode="shutter_mode")
    @_specfunc
    def is_shutter_mode_possible(self, mode):
        """Check if the shutter mode (``"closed"``, ``"opened"``, or ``"bnc"``) is supported"""
        self._check_shutter()
        return mode>=0 and lib.ShamrockIsModePossible(self.idx,mode)
    @interface.use_parameters(mode="shutter_mode")
    @_specfunc
    def set_shutter(self, mode):
        """Set shutter mode (``"closed"`` or ``"opened"``)"""
        self._check_shutter()
        if not self._wip.is_shutter_mode_possible(mode):
            raise AndorNotSupportedError("shutter mode '{}' is not supported".format(self._p_shutter_mode.i(mode)))
        if mode!=-1:
            lib.ShamrockSetShutter(self.idx,mode)
        return self.get_shutter()
        

    ### Filter control ###
    @_specfunc
    def is_filter_present(self):
        """Check if the filter is present"""
        return bool(lib.ShamrockFilterIsPresent(self.idx))
    def _check_filter(self):
        if not self.is_filter_present():
            raise AndorNotSupportedError("filter is not present")
    @_specfunc
    def get_filter(self):
        """Get current filter"""
        self._check_filter()
        return lib.ShamrockGetFilter(self.idx)
    @_specfunc
    def set_filter(self, flt):
        """Set current filter"""
        self._check_filter()
        lib.ShamrockSetFilter(self.idx,flt)
        return self.get_filter()
    @_specfunc
    def get_filter_info(self, flt):
        """Get info of the given filter"""
        self._check_filter()
        return lib.ShamrockGetFilterInfo(self.idx,flt)
    @_specfunc
    def reset_filter(self):
        """Reset filter to default position"""
        self._check_filter()
        lib.ShamrockFilterReset(self.idx)
        return self.get_filter()
        

    ### Flipper control ###
    _p_flipper_index=interface.EnumParameterClass("flipper_index",{"input":1,"output":2})
    @interface.use_parameters(flipper="flipper_index")
    @_specfunc
    def is_flipper_present(self, flipper):
        """
        Check if the flipper is present.

        `flipper` can be a flipper index (starting from 1), ``"input"``, or `"output"``.
        """
        return bool(lib.ShamrockFlipperMirrorIsPresent(self.idx,flipper))
    def _check_flipper(self, flipper):
        if not self.is_flipper_present(flipper):
            raise AndorNotSupportedError("flipper {} is not present".format(flipper))
    _p_flipper_port=interface.EnumParameterClass("flipper_port",{"direct":0,"side":1})
    @interface.use_parameters(flipper="flipper_index",_returns="flipper_port")
    @_specfunc
    def get_flipper_port(self, flipper):
        """
        Get flipper port.

        `flipper` can be a flipper index (starting from 1), ``"input"``, or `"output"``.
        Return either ``"direct"`` or ``"side"``.
        """
        self._check_flipper(flipper)
        return lib.ShamrockGetFlipperMirror(self.idx,flipper)
    @interface.use_parameters(flipper="flipper_index",port="flipper_port")
    @_specfunc
    def set_flipper_port(self, flipper, port):
        """
        Set flipper port.

        `flipper` can be a flipper index (starting from 1), ``"input"``, or `"output"``.
        Port can be ``"direct"`` or ``"side"``.
        """
        self._check_flipper(flipper)
        lib.ShamrockSetFlipperMirror(self.idx,flipper,port)
        return self._wip.get_flipper_port(flipper)
    def _get_all_flipper_ports(self):
        return [self.get_flipper_port(f) if self.is_flipper_present(f) else None for f in range(1,3)]
    def _set_all_flipper_ports(self, ports):
        for f,p in enumerate(ports,start=1):
            if p is not None:
                self.set_flipper_port(f,p)
    @interface.use_parameters(flipper="flipper_index")
    @_specfunc
    def reset_flipper(self, flipper):
        """
        Reset flipper to the default state.

        `flipper` can be a flipper index (starting from 1), ``"input"``, or `"output"``.
        """
        self._check_flipper(flipper)
        lib.ShamrockFlipperMirrorReset(self.idx,flipper)
        return self._wip.get_flipper_port(flipper)
        

    ### Iris control ###
    _p_iris_port=interface.EnumParameterClass("iris_port",{"direct":0,"side":1})
    @interface.use_parameters(iris="iris_port")
    @_specfunc
    def is_iris_present(self, iris):
        """Check if the iris is present"""
        return bool(lib.ShamrockIrisIsPresent is not None and lib.ShamrockIrisIsPresent(self.idx,iris))
    def _check_iris(self, iris):
        if lib.ShamrockIrisIsPresent is None or not lib.ShamrockIrisIsPresent(self.idx,iris):
            raise AndorNotSupportedError("iris is not present")
    @interface.use_parameters(iris="iris_port")
    @_specfunc
    def get_iris_width(self, iris):
        """Get current iris width (0 to 100)"""
        self._check_iris(iris)
        return lib.ShamrockGetIris(self.idx,iris)
    @interface.use_parameters(iris="iris_port")
    @_specfunc
    def set_iris_width(self, iris, width):
        """Set current iris width (0 to 100)"""
        self._check_iris(iris)
        lib.ShamrockSetIris(self.idx,iris,int(width))
        return lib.ShamrockGetIris(self.idx,iris)
    def _get_all_iris_widths(self):
        return [self.get_iris_width(s) if self.is_iris_present(s) else None for s in range(2)]
    def _set_all_iris_widths(self, widths):
        for s,w in enumerate(widths):
            if w is not None:
                self.set_iris_width(s,w)
        

    ### Focus mirror control ###
    @_specfunc
    def is_focus_mirror_present(self):
        """Check if the focus mirror is present"""
        return bool(lib.ShamrockFocusMirrorIsPresent is not None and lib.ShamrockFocusMirrorIsPresent(self.idx))
    def _check_focus_mirror(self):
        if lib.ShamrockFocusMirrorIsPresent is None or not lib.ShamrockFocusMirrorIsPresent(self.idx):
            raise AndorNotSupportedError("focus mirror is not present")
    @_specfunc
    def get_focus_mirror_position(self):
        """Get current focus mirror position"""
        self._check_focus_mirror()
        return lib.ShamrockGetFocusMirror(self.idx)
    @_specfunc
    def set_focus_mirror_position(self, position):
        """Set current focus mirror position"""
        self._check_focus_mirror()
        lib.ShamrockSetFocusMirror(self.idx,int(position))
        return lib.ShamrockGetFocusMirror(self.idx)
    @_specfunc
    def get_focus_mirror_position_max(self):
        """Get maximal focus mirror position"""
        self._check_focus_mirror()
        return lib.ShamrockGetFocusMirrorMaxSteps(self.idx)
    @_specfunc
    def reset_focus_mirror(self):
        """Reset focus mirror position"""
        self._check_focus_mirror()
        return lib.ShamrockFocusMirrorReset(self.idx)
        

    ### Accessory control ###
    @_specfunc
    def is_accessory_present(self):
        """Check if the accessory is present"""
        return bool(lib.ShamrockAccessoryIsPresent(self.idx))
    def _check_accessory(self):
        if not self.is_accessory_present():
            raise AndorNotSupportedError("accessory is not present")
    @_specfunc
    def get_accessory_state(self, line):
        """Get current accessory state on a given line (1 or 2)"""
        self._check_accessory()
        return lib.ShamrockGetAccessoryState(self.idx,line)
    @_specfunc
    def set_accessory_state(self, line, state):
        """Set current accessory state (0 or 1) on a given line (1 or 2)"""
        self._check_accessory()
        lib.ShamrockSetAccessory(self.idx,line,state)
        return self.get_accessory_state(line)
    def _get_all_accessory_states(self):
        return [self.get_accessory_state(l) if self.is_accessory_present() else None for l in range(1,3)]
    def _set_all_accessory_states(self, states):
        for l,s in enumerate(states,start=1):
            if s is not None:
                self.set_accessory_state(l,s)


    ### Calibration ###
    @_specfunc
    def get_pixel_width(self):
        """Get current set detector pixel width (in m)"""
        return lib.ShamrockGetPixelWidth(self.idx)*1E-6
    @_specfunc
    def set_pixel_width(self, width):
        """Set current detector pixel width (in m)"""
        lib.ShamrockSetPixelWidth(self.idx,width/1E-6)
        return self.get_pixel_width()
    @_specfunc
    def get_number_pixels(self):
        """Get current set detector number of pixels"""
        return lib.ShamrockGetNumberPixels(self.idx)
    @_specfunc
    def set_number_pixels(self, number):
        """Set current detector number of pixels"""
        lib.ShamrockSetNumberPixels(self.idx,number)
        return self.get_number_pixels()
    def setup_pixels_from_camera(self, cam):
        """Setup detector parameters (number of pixels, pixel width) from the camera"""
        pixel_size=cam.get_pixel_size()
        det_size=cam.get_detector_size()
        self.set_pixel_width(pixel_size[0])
        self.set_number_pixels(det_size[0])
        return self.get_pixel_width(),self.get_number_pixels()
    @_specfunc
    def get_calibration(self):
        """
        Get wavelength calibration.

        Return numpy array which specifies wavelength (in m) corresponding to each pixel.
        Prior to calling this method, the total number of pixels and the pixel width of the sensor should be set up using the corresponding methods
        (:meth:`set_number_pixels` and :meth:`set_pixel_width`, or :meth:`setup_pixels_from_camera` to set both parameters using and AndorSDK2 camera instance)
        """
        npx=self.get_number_pixels()
        return np.array(lib.ShamrockGetCalibration(self.idx,self.get_number_pixels()))*1E-9 if npx else np.zeros(0)