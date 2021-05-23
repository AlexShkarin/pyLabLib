from .AndorShamrock_lib import lib, ShamrockLibError

from ...core.devio import data_format
from ...core.devio.interface import IDevice
from ...core.utils import funcargparse, py3, dictionary, strpack, general
from ...core.dataproc import image as image_utils

_depends_local=[".AndorShamrock_lib","...core.devio.interface"]

import numpy as np
import collections
import contextlib
import ctypes
import threading
import time

class ShamrockError(RuntimeError):
    "Generic Andor Shamrock error."
class ShamrockNotSupportedError(ShamrockError):
    "Option not supported."

def get_spectrographs_number():
    """Get number of connected Andor cameras"""
    with lib.using_handle():
        return lib.ShamrockGetNumberDevices()

class ShamrockSpectrograph(IDevice):
    """
    Shaprock spectrograph.

    Args:
        idx(int): spectrograph index (starting from 0; use :func:`get_spectrographs_number` to get the total number of connected spectrogaphs)
    """
    def __init__(self, idx=0):
        IDevice.__init__(self)
        self.idx=idx
        self._opened=False
        self.open()
        
        self._add_full_info_node("model_data",self.get_model_data)
        self._add_full_info_node("optical_parameters",self.get_optical_parameters)
        self._add_full_info_node("gratings_number",self.get_gratings_number)
        self._add_status_node("grating_infos",lambda: [self.get_grating_info(g) for g in range(1,self.get_gratings_number()+1)])
        self._add_settings_node("grating",self.get_grating,self.set_grating)
        self._add_settings_node("grating_offsets",self._get_all_grating_offsets,self._set_all_grating_offsets)
        self._add_settings_node("detector_offset",self.get_detector_offset,self.set_detector_offset)
        self._add_full_info_node("wavelength_present",self.is_wavelength_control_present)
        self._add_full_info_node("wavelength_limits",lambda: [self.get_wavelength_limits(g) for g in range(1,self.get_gratings_number()+1)],ignore_error=(ShamrockError,))
        self._add_settings_node("wavelength",self.get_wavelength,self.set_wavelength,ignore_error=(ShamrockError,))
        self._add_status_node("zero_order",self.is_at_zero_order,ignore_error=(ShamrockError,))
        self._add_full_info_node("slits_present",lambda: [self.is_slit_present(s) for s in range(1,5)])
        self._add_settings_node("slit_widths",self._get_all_slit_widths,self._set_all_slit_widths)
        self._add_full_info_node("shutter_present",self.is_shutter_present)
        self._add_settings_node("shutter_mode",self.get_shutter,self.set_shutter,ignore_error=(ShamrockError,))
        self._add_full_info_node("filter_present",self.is_filter_present)
        self._add_settings_node("filter",self.get_filter,self.set_filter,ignore_error=(ShamrockError,))
        self._add_full_info_node("flippers_present",lambda: [self.is_flipper_present(s) for s in range(1,3)])
        self._add_settings_node("flipper_ports",self._get_all_flipper_ports,self._set_all_flipper_ports)
        self._add_full_info_node("accessory_present",self.is_accessory_present)
        self._add_settings_node("accessory_states",self._get_all_accessory_states,self._set_all_accessory_states)
        self._add_settings_node("pixel_width",self.get_pixel_width,self.set_pixel_width)
        self._add_settings_node("number_pixels",self.get_number_pixels,self.set_number_pixels)
        self._add_status_node("calibration",self.get_calibration)

    def open(self):
        """Open connection to the camera"""
        if not self._opened:
            lib.open_handle()
            ncams=get_spectrographs_number()
            if self.idx>=ncams:
                lib.close_handle()
                raise ShamrockError("spectrograph index {} is not available ({} spectrograph exist)".format(self.idx,ncams))
            self._opened=True
    def close(self):
        """Close connection to the camera"""
        if self._opened:
            lib.close_handle()
            self._opened=False
    def is_opened(self):
        """Check if the device is connected"""
        return self._opened

    ModelData=collections.namedtuple("ModelData",["serial_number"])
    def get_model_data(self):
        """
        Get camera model data.

        Return tuple ``(serial_number)``.
        """
        serial_number=lib.ShamrockGetSerialNumber(self.idx)
        return self.ModelData(serial_number)
    OpticalParameters=collections.namedtuple("OpticalParameters",["focal_length","angular_deviation","focal_tilt"])
    def get_optical_parameters(self):
        """
        Get device optical parameters.

        Return tuple ``(focal_length, angular_deviation, focal_tilt)``.
        """
        params=lib.ShamrockEepromGetOpticalParams(self.idx)
        return self.OpticalParameters(*params)
        
    
    ### Grating control ###
    def get_gratings_number(self):
        """Get number of gratings"""
        return lib.ShamrockGetNumberGratings(self.idx)
    def _check_grating(self, grating):
        if grating is None:
            return self.get_grating()
        if grating<1 or grating>self.get_gratings_number():
            raise ValueError("incorrect grating index: {}; should be between 1 and {}".format(grating,self.get_gratings_number()))
        return grating
    def get_grating(self):
        """Get current grating index (counting from 1)"""
        return lib.ShamrockGetGrating(self.idx)
    def set_grating(self, grating, force=False):
        """
        Set current grating (counting from 1)
        
        Call blocks until the grating is exchanged (up to 10-20 seconds).
        If ``force==False`` and the current grating index is the same as requested, skip the call;
        otherwise, call the grating set command regardless (takes about a second in the grating is unchaged).
        """
        grating=self._check_grating(grating)
        if force or self.get_grating()!=grating:
            lib.ShamrockSetGrating(self.idx,grating)
        return self.get_grating()
    GratingInfo=collections.namedtuple("GratingInfo",["lines","blaze_wavelength","home","offset"])
    def get_grating_info(self, grating=None):
        """
        Get info of a given grating (by default, current grating).

        Return tuple ``(lines, blaze_wavelength, home, offset)`` (blazing wavelength is in nm).
        """
        grating=self._check_grating(grating)
        return self.GratingInfo(*lib.ShamrockGetGratingInfo(self.idx,grating))
    def get_grating_offset(self, grating=None):
        """Get grating offset (in steps) for a given grating (by default, current grating)"""
        grating=self._check_grating(grating)
        return lib.ShamrockGetGratingOffset(self.idx,grating)
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
    def get_detector_offset(self):
        """Get detector offset (in steps)"""
        return lib.ShamrockGetDetectorOffset(self.idx)
    def set_detector_offset(self, offset):
        """Set detector offset (in steps)"""
        lib.ShamrockSetDetectorOffset(self.idx,offset)
        return self.get_detector_offset()
    def get_turret(self):
        """Get turrent"""
        return lib.ShamrockGetTurret(self.idx)
    def set_turret(self, turret):
        """Set turret"""
        lib.ShamrockSetTurret(self.idx,turret)
        return self.get_turret()
        
    
    ### Wavelength control ###
    def is_wavelength_control_present(self):
        """Check if wavelength control is present"""
        return bool(lib.ShamrockWavelengthIsPresent(self.idx))
    def _check_wavelength(self):
        if not self.is_wavelength_control_present():
            raise ShamrockError("wavelength control is not preset")
    def get_wavelength(self):
        """Get current central wavelength (in m)"""
        self._check_wavelength()
        return lib.ShamrockGetWavelength(self.idx)*1E-9
    def set_wavelength(self, wavelength):
        """Get current central wavelength (in m)"""
        self._check_wavelength()
        lib.ShamrockSetWavelength(self.idx,wavelength/1E-9)
        return self.get_wavelength()
    def get_wavelength_limits(self, grating=None):
        """Get wavelength limits (in m) for a given grating (by default, current grating)"""
        self._check_wavelength()
        grating=self._check_grating(grating)
        lim=lib.ShamrockGetWavelengthLimits(self.idx,grating)
        return lim[0]*1E-9,lim[1]*1E-9
    def reset_wavelength(self):
        """Reset current wavelength to 0 nm"""
        self._check_wavelength()
        lib.ShamrockWavelengthReset(self.idx)
        return self.get_wavelength()
    def is_at_zero_order(self):
        """Check if current grating is at zero order"""
        self._check_wavelength()
        return bool(lib.ShamrockAtZeroOrder(self.idx))
    def goto_zero_order(self):
        """Set current grating to zero order"""
        self._check_wavelength()
        lib.ShamrockGotoZeroOrder(self.idx)
        return self.is_at_zero_order()
        

    ### Slit control ###
    _default_slits={"input_side":1,"input_direct":2,"output_side":3,"output_direct":4}
    def _slit_idx(self, slit):
        return self._default_slits.get(slit,slit)
    def is_slit_present(self, slit):
        """
        Check if the slit is present.

        `slit` cen be either a slit index (starting from 1), or one of the following: ``"input_side"``, ``"input_direct"``, ``"output_side"``, or ``"output_direct"``.
        """
        slit=self._slit_idx(slit)
        return bool(lib.ShamrockAutoSlitIsPresent(self.idx,slit))
    def _check_slit(self, slit):
        if not self.is_slit_present(slit):
            raise ShamrockError("slit {} is not preset".format(slit))
        return self._slit_idx(slit)
    def get_slit_width(self, slit):
        """
        Get slit width (in m).

        `slit` cen be either a slit index (starting from 1), or one of the following: ``"input_side"``, ``"input_direct"``, ``"output_side"``, or ``"output_direct"``.
        """
        slit=self._check_slit(slit)
        return lib.ShamrockGetAutoSlitWidth(self.idx,slit)*1E-6
    def set_slit_width(self, slit, width):
        """
        Set slit width (in m).

        `slit` cen be either a slit index (starting from 1), or one of the following: ``"input_side"``, ``"input_direct"``, ``"output_side"``, or ``"output_direct"``.
        """
        slit=self._check_slit(slit)
        lib.ShamrockSetAutoSlitWidth(self.idx,slit,width/1E-6)
        return self.get_slit_width(slit)
    def _get_all_slit_widths(self):
        return [self.get_slit_width(s) if self.is_slit_present(s) else None for s in range(1,5)]
    def _set_all_slit_widths(self, widths):
        for s,w in enumerate(widths,start=1):
            if w is not None:
                self.set_slit_width(s,w)
    def reset_slit(self, slit):
        """
        Reset slit to the default width (10 um).

        `slit` cen be either a slit index (starting from 1), or one of the following: ``"input_side"``, ``"input_direct"``, ``"output_side"``, or ``"output_direct"``.
        """
        slit=self._check_slit(slit)
        lib.ShamrockAutoSlitReset(self.idx,slit)
        return self.get_slit_width(slit)
        

    ### Shutter control ###
    def is_shutter_present(self):
        """Check if the shutter is present"""
        return bool(lib.ShamrockShutterIsPresent(self.idx))
    def _check_shutter(self):
        if not self.is_shutter_present():
            raise ShamrockError("shutter is not preset")
    _shutter_modes={0:"closed",1:"opened",-1:"not_set"}
    def get_shutter(self):
        """
        Get shutter mode.

        Can return ``"closed"``, ``"opened"``, or ``"not_set"``.
        """
        self._check_shutter()
        mode=lib.ShamrockGetShutter(self.idx)
        return self._shutter_modes[mode]
    def set_shutter(self, mode):
        """Set shutter mode"""
        self._check_shutter()
        mode=0 if mode in [False,"closed"] else 1
        lib.ShamrockSetShutter(self.idx,mode)
        return self.get_shutter()
        

    ### Filter control ###
    def is_filter_present(self):
        """Check if the filter is present"""
        return bool(lib.ShamrockFilterIsPresent(self.idx))
    def _check_filter(self):
        if not self.is_filter_present():
            raise ShamrockError("filter is not preset")
    def get_filter(self):
        """Get current filter"""
        self._check_filter()
        return lib.ShamrockGetFilter(self.idx)
    def set_filter(self, filter):
        """Set current flilter"""
        self._check_filter()
        lib.ShamrockSetFilter(self.idx,filter)
        return self.get_filter()
    def get_filter_info(self, filter):
        """Get info of the given filter"""
        self._check_filter()
        return lib.ShamrockGetFilterInfo(self.idx,filter)
    def reset_filter(self):
        """Reset flilter to default position"""
        self._check_filter()
        lib.ShamrockFilterReset(self.idx)
        return self.get_filter()
        

    ### Filpper control ###
    _default_filpperss={"input":1,"output":2}
    def _flipper_idx(self, flipper):
        return self._default_filpperss.get(flipper,flipper)
    def is_flipper_present(self, flipper):
        """
        Check if the flipper is present.

        `flipper` cen be either a flipper index (starting from 1), or one of the following: ``"input"``, or `"output"``.
        """
        flipper=self._flipper_idx(flipper)
        return bool(lib.ShamrockFlipperMirrorIsPresent(self.idx,flipper))
    def _check_flipper(self, flipper):
        if not self.is_flipper_present(flipper):
            raise ShamrockError("flipper {} is not preset".format(flipper))
        return self._slit_idx(flipper)
    _flipper_ports={0:"direct",1:"size"}
    def get_flipper_port(self, flipper):
        """
        Get flipper port.

        `flipper` cen be either a flipper index (starting from 1), or one of the following: ``"input"``, or `"output"``.
        Return either ``"direct"`` or ``"side"``.
        """
        flipper=self._check_flipper(flipper)
        port=lib.ShamrockGetFlipperMirror(self.idx,flipper)
        return self._flipper_ports[port]
    def set_flipper_port(self, flipper, port):
        """
        Set flipper port.

        `flipper` cen be either a flipper index (starting from 1), or one of the following: ``"input"``, or `"output"``.
        Port can be a numerical value (0 or 1), ``"direct"``, or ``"side"``.
        """
        flipper=self._check_flipper(flipper)
        port=0 if port in [0,False,"direct"] else 1
        lib.ShamrockSetFlipperMirror(self.idx,flipper,port)
        return self.get_flipper_port(flipper)
    def _get_all_flipper_ports(self):
        return [self.get_flipper_port(f) if self.is_flipper_present(f) else None for f in range(1,3)]
    def _set_all_flipper_ports(self, ports):
        for f,p in enumerate(ports,start=1):
            if p is not None:
                self.set_flipper_port(f,p)
    def reset_flipper(self, flipper):
        """
        Reset flipper to the default state.

        `flipper` cen be either a flipper index (starting from 1), or one of the following: ``"input"``, or `"output"``.
        """
        flipper=self._check_flipper(flipper)
        lib.ShamrockFlipperMirrorReset(self.idx,flipper)
        return self.get_flipper_port(flipper)
        

    ### Accessory control ###
    def is_accessory_present(self):
        """Check if the accessory is present"""
        return bool(lib.ShamrockAccessoryIsPresent(self.idx))
    def _check_accessory(self):
        if not self.is_accessory_present():
            raise ShamrockError("accessory is not preset")
    def get_accessory_state(self, line):
        """Get current accessory state on a given line (1 or 2)"""
        self._check_accessory()
        return lib.ShamrockGetAccessoryState(self.idx,line)
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
    def get_pixel_width(self):
        """Get current set detector pixel width (in m)"""
        return lib.ShamrockGetPixelWidth(self.idx)*1E-6
    def set_pixel_width(self, width):
        """Set current detector pixel width (in m)"""
        lib.ShamrockSetPixelWidth(self.idx,width/1E-6)
        return self.get_pixel_width()
    def get_number_pixels(self):
        """Get current set detector number of pixels"""
        return lib.ShamrockGetNumberPixels(self.idx)
    def set_number_pixels(self, number):
        """Set current detector number of pixels"""
        lib.ShamrockSetNumberPixels(self.idx,number)
        return self.get_number_pixels()
    def setup_from_camera(self, cam):
        """Setup detector parameters (number of pixels, pixel width) from the camera"""
        pixel_size=cam.get_pixel_size()
        det_size=cam.get_detector_size()
        self.set_pixel_width(pixel_size[0])
        self.set_number_pixels(det_size[0])
        return self.get_pixel_width(),self.get_number_pixels()
    def get_calibration(self):
        """
        Get wavelength calibration.

        Return numpy array with number equal preset number of detector pixels, which specifies wavelength (in m) corresponding to each pixel.
        """
        return np.array(lib.ShamrockGetCalibration(self.idx,self.get_number_pixels()))*1E-9
