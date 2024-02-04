from .tl_camera_sdk_lib import ThorlabsTLCameraError
from .tl_camera_sdk_lib import wlib as lib
from . import tl_camera_sdk_defs

from ...core.devio import interface
from ..interface import camera
from ...core.utils import py3
from ..utils import load_lib, color

import numpy as np
import collections
import ctypes
import struct
import threading
import warnings
import time


class ThorlabsTLCameraTimeoutError(ThorlabsTLCameraError):
    "TLCamera frame timeout error"


class LibraryController(load_lib.LibraryController):
    def _do_init(self):
        lib.tl_camera_open_sdk()
        lib.tl_camera_discover_available_cameras()
    def _do_uninit(self):
        lib.tl_camera_close_sdk()
libctl=LibraryController(lib)



def list_cameras():
    """List connected TLCamera cameras"""
    with libctl.temp_open():
        try:
            return py3.as_str(lib.tl_camera_discover_available_cameras()).split()
        except ThorlabsTLCameraError:
            return []

def get_cameras_number():
    """Get number of connected TLCamera cameras"""
    return len(list_cameras())




TDeviceInfo=collections.namedtuple("TDeviceInfo",["model","name","serial_number","firmware_version"])
TSensorInfo=collections.namedtuple("TSensorInfo",["sensor_type","bit_depth"])
TColorInfo=collections.namedtuple("TColorInfo",["filter_array_phase","correction_matrix","default_white_balance_matrix"])
TColorFormat=collections.namedtuple("TColorFormat",["color_format","color_space"])
TFrameInfo=collections.namedtuple("TFrameInfo",["frame_index","framestamp","pixelclock","pixeltype","offset"])
class ThorlabsTLCamera(camera.IBinROICamera, camera.IExposureCamera):
    """
    Thorlabs TSI camera.

    Args:
        serial(str): camera serial number; can be either a string obtained using :func:`list_cameras` function,
            or ``None``, which means connecting to the first available camera (not recommended unless only one camera is connected)
    """
    Error=ThorlabsTLCameraError
    TimeoutError=ThorlabsTLCameraTimeoutError
    _TFrameInfo=TFrameInfo
    def __init__(self, serial=None):
        super().__init__()
        self.serial=str(serial) if isinstance(serial,int) else serial
        self.handle=None
        self._buffer=self.RingBuffer()
        self._new_frame_cb=None
        self._tsclk=None
        self._sensor_info=None
        self._color_info=None
        self._white_balance_matrix=np.eye(3)
        self.open()
        
        self._add_info_variable("device_info",self.get_device_info)
        self._add_settings_variable("trigger_mode",self.get_trigger_mode,self.set_trigger_mode)
        self._add_settings_variable("ext_trigger",self.get_ext_trigger_parameters,self.setup_ext_trigger,ignore_error=self.Error)
        self._add_settings_variable("hotpixel_correction",self.get_pixel_correction_parameters,self.setup_pixel_correction,ignore_error=(self.Error,OSError))  # sometimes raises OSError; DLL issues?
        self._add_info_variable("gain_range",self.get_gain_range,ignore_error=self.Error)
        self._add_settings_variable("gain",self.get_gain,self.set_gain,ignore_error=self.Error)
        self._add_info_variable("black_level_range",self.get_black_level_range,ignore_error=self.Error)
        self._add_settings_variable("black_level",self.get_black_level,self.set_black_level,ignore_error=self.Error)
        self._add_settings_variable("nir_boost",self.is_nir_boost_enabled,self.enable_nir_boost,ignore_error=self.Error)
        self._add_settings_variable("cooling",self.is_cooling_enabled,self.enable_cooling,ignore_error=self.Error)
        self._add_settings_variable("led",self.is_led_enabled,self.enable_led,ignore_error=self.Error)
        self._add_info_variable("timestamp_clock_frequency",self.get_timestamp_clock_frequency)
        self._add_info_variable("sensor_info",self.get_sensor_info)
        self._add_info_variable("color_info",self.get_color_info)
        self._add_settings_variable("color_format",self.get_color_format,self.set_color_format)
        self._add_settings_variable("frame_period",self.get_frame_period,self.set_frame_period,ignore_error=self.Error)
        
    def _get_connection_parameters(self):
        return self.serial
    def open(self):
        """Open connection to the camera"""
        if self.handle is None:
            with libctl.temp_open():
                lst=list_cameras()
                if self.serial is None:
                    self.serial=lst[0] if lst else ""
                elif self.serial not in lst:
                    raise ThorlabsTLCameraError("camera with serial number {} isn't present among available cameras: {}".format(self.serial,lst))
                self.handle=lib.tl_camera_open_camera(self.serial)
                self._opid=libctl.open().opid
                with self._close_on_error():
                    lib.tl_camera_set_image_poll_timeout(self.handle,1000)
                    self._register_new_frame_callback()
                    self._tsclk=self.get_timestamp_clock_frequency()
                    self.set_color_format()
                    self.set_white_balance_matrix()
    def close(self):
        """Close connection to the camera"""
        if self.handle is not None:
            try:
                try:
                    self.clear_acquisition()
                except ThorlabsTLCameraError:
                    pass
                self._unregister_new_frame_callback()
                lib.tl_camera_close_camera(self.handle)
            finally:
                self.handle=None
                libctl.close(self._opid)
                self._opid=None
    def is_opened(self):
        """Check if the device is connected"""
        return self.handle is not None

    def get_device_info(self):
        """
        Get camera model data.

        Return tuple ``(model, name, serial_number, firmware_version)``.
        """
        model=py3.as_str(lib.tl_camera_get_model(self.handle))
        name=py3.as_str(lib.tl_camera_get_name(self.handle))
        serial_number=py3.as_str(lib.tl_camera_get_serial_number(self.handle))
        firmware_version=py3.as_str(lib.tl_camera_get_firmware_version(self.handle))
        return TDeviceInfo(model,name,serial_number,firmware_version)

    _sensor_types={"mono":tl_camera_sdk_defs.TL_CAMERA_SENSOR_TYPE.TL_CAMERA_SENSOR_TYPE_MONOCHROME,
                    "bayer":tl_camera_sdk_defs.TL_CAMERA_SENSOR_TYPE.TL_CAMERA_SENSOR_TYPE_BAYER,
                    "mono_pol":tl_camera_sdk_defs.TL_CAMERA_SENSOR_TYPE.TL_CAMERA_SENSOR_TYPE_MONOCHROME_POLARIZED}
    _p_sensor_types=interface.EnumParameterClass("sensor_type",_sensor_types)
    @interface.use_parameters(_returns=("sensor_type",None))
    def get_sensor_info(self):
        """
        Get camera sensor info.
        
        Return tuple ``(sensor_type, bit_depth)``, where sensor type is ``"mono"``, ``"bayer"``, or ``"mono_pol"``,
        and bit depth is an integer.
        """
        if self._sensor_info is None:
            self._sensor_info=TSensorInfo(lib.tl_camera_get_camera_sensor_type(self.handle),lib.tl_camera_get_bit_depth(self.handle))
        return self._sensor_info
    _filter_array_phase={"red":tl_camera_sdk_defs.TL_COLOR_FILTER_ARRAY_PHASE.TL_COLOR_FILTER_ARRAY_PHASE_BAYER_RED,
                    "blue":tl_camera_sdk_defs.TL_COLOR_FILTER_ARRAY_PHASE.TL_COLOR_FILTER_ARRAY_PHASE_BAYER_BLUE,
                    "green_left_or_red":tl_camera_sdk_defs.TL_COLOR_FILTER_ARRAY_PHASE.TL_COLOR_FILTER_ARRAY_PHASE_BAYER_GREEN_LEFT_OF_RED,
                    "green_left_or_blue":tl_camera_sdk_defs.TL_COLOR_FILTER_ARRAY_PHASE.TL_COLOR_FILTER_ARRAY_PHASE_BAYER_GREEN_LEFT_OF_BLUE}
    _p_filter_array_phase=interface.EnumParameterClass("filter_array_phase",_filter_array_phase)
    def get_color_info(self):
        """
        Get camera color info.

        Return tuple ``(filter_array_phase, correction_matrix, default_white_balance_matrix)``, or ``None`` if the sensor type is not ``"bayer"``.
        """
        if self.get_sensor_info().sensor_type!="bayer":
            return None
        if self._color_info is None:
            cmat=np.array(lib.tl_camera_get_color_correction_matrix(self.handle)).reshape((3,3))
            wbmat=np.array(lib.tl_camera_get_default_white_balance_matrix(self.handle)).reshape((3,3))
            filter_array_phase=self._parameters["filter_array_phase"].i(lib.tl_camera_get_color_filter_array_phase(self.handle))
            self._color_info=TColorInfo(filter_array_phase,cmat,wbmat)
        return self._color_info

    def get_white_balance_matrix(self):
        """Get the white balance matrix"""
        return self._white_balance_matrix
    def set_white_balance_matrix(self, matrix=None):
        """
        Set the white balance matrix.

        Can be ``None`` (the default matrix), a 3-number 1D array (multipliers for RGB), or a full 3x3 matrix.
        """
        if self.get_sensor_info().sensor_type!="bayer":
            self._white_balance_matrix=np.eye(3) if matrix is None else matrix
            return
        if matrix is None:
            matrix=self.get_color_info().default_white_balance_matrix
        elif np.ndim(matrix)==1:
            matrix=np.diag(matrix)
        self._white_balance_matrix=matrix

    _p_color_output=interface.EnumParameterClass("color_output",["raw","rgb","grayscale","auto"])
    _p_color_space=interface.EnumParameterClass("color_space",["srgb","linear"])
    @interface.use_parameters
    def set_color_format(self, color_output="auto", color_space="linear"):
        """
        Set camera color format.

        `color_output` determines the output frame format, and can be ``"raw"`` (raw pixel values without debayering),
        ``"rgb"`` (color images with the color corresponding to the last array axis), ``"grayscale"`` (average of the colored images),
        or ``"auto"`` (``"rgb"`` for cameras supporting color and ``"raw"`` otherwise). Note that setting ``"rgb"`` for monochrome cameras is not allowed.
        `color_space` defines the output color space, and can be ``"linear"`` (linear in the pixel values),
        or ``"srgb"`` (sRGB color space, which is a non-linear transformation of the linear values).
        """
        cinfo=self.get_color_info()
        if color_output=="rgb" and cinfo is None:
            raise ValueError("'rgb' color mode is only supported on color cameras")
        if color_output=="auto":
            color_output="rgb" if cinfo is not None else "raw"
        self._color_output=color_output
        if color_output=="rgb":
            color.bayer_interpolate(np.zeros((0,0),dtype="float"))
        self._color_space=color_space
        return self.get_color_format()
    def get_color_format(self):
        """Get camera color format as a tuple ``(color_output, color_space)``"""
        return TColorFormat(self._color_output,self._color_space)

    # ### Acquisition controls ###
    class RingBuffer:
        """
        Frames ring buffer.

        Reacts to each new frame and stores it in the internal buffer.
        """
        def __init__(self):
            self._frame_notifier=camera.FrameNotifier()
            self.lock=threading.RLock()
            self.cleanup()
        def reset(self):
            """Reset buffer and internal counters"""
            self.buffer=[]
            self.missed=0
            self._frame_notifier.reset()
        def setup(self, buffsize, frame_dim):
            """Setup a new buffer with the given maximal number of frames and frame dimensions"""
            self.reset()
            self.buffsize=max(buffsize,1)
            self.frame_dim=frame_dim
        def cleanup(self):
            """Cleanup the buffer"""
            self.reset()
            self.buffer=None
            self.buffsize=0
            self.frame_dim=None
        def new_frame(self, handle, buffer, idx, metadata, metadata_size, context):  # pylint: disable=unused-argument
            """Callback for receiving a new frame"""
            if self.buffer is not None:
                data=np.ctypeslib.as_array(buffer,shape=self.frame_dim).copy()
                metadata=ctypes.string_at(metadata,metadata_size)
                with self.lock:
                    if self.buffer is not None:
                        self.buffer.append((data,metadata))
                        if len(self.buffer)>self.buffsize:
                            self.buffer=self.buffer[-self.buffsize:]
                        acquired=self._frame_notifier.inc()
                        if idx>acquired+self.missed:
                            self.missed+=idx-(acquired+self.missed)
        def wait_for_frame(self, idx=None, timeout=None):
            """Wait for a new frame acquisition"""
            self._frame_notifier.wait(idx=idx,timeout=timeout)
        def get_frame(self, idx):
            """Get the frame with the given index (or ``None`` if it is outside the buffer range)"""
            with self.lock:
                bidx=self._frame_notifier.counter-idx
                if bidx>0 and bidx<=len(self.buffer):
                    return self.buffer[-bidx]
                else:
                    return None
        def get_status(self):
            """Get buffer status ``(acquired, missed, stored)``"""
            with self.lock:
                return self._frame_notifier.counter,self.missed,len(self.buffer or [])

    def _get_acquired_frames(self):
        return self._buffer.get_status()[0]
    

    def _register_new_frame_callback(self):
        if self._new_frame_cb is None:
            self._new_frame_cb=lib.tl_camera_set_frame_available_callback(self.handle,self._buffer.new_frame)
    def _unregister_new_frame_callback(self):
        if self._new_frame_cb is not None:
            lib.tl_camera_set_frame_available_callback(self.handle,None)
            self._new_frame_cb=None


    def get_frame_timings(self):
        return self._TAcqTimings(lib.tl_camera_get_exposure_time(self.handle)*1E-6, lib.tl_camera_get_frame_time(self.handle)*1E-6)
    def set_exposure(self, exposure):
        """Set camera exposure"""
        lib.tl_camera_set_exposure_time(self.handle,int(exposure/1E-6))
        return self.get_exposure()
    def get_frame_period_range(self):
        """Get minimal and maximal frame period (s)"""
        fps_range=lib.tl_camera_get_frame_rate_control_value_range()
        return (1./fps_range[1],1./max(fps_range[0],1E-6))
    def set_frame_period(self, frame_period):
        """
        Set camera frame period.
        
        If it is 0 or ``None``, set to the auto-rate mode, which automatically selects the highest frame rate.
        """
        if frame_period is None or frame_period<=0:
            lib.tl_camera_set_is_frame_rate_control_enabled(self.handle,0)
            return
        lib.tl_camera_set_is_frame_rate_control_enabled(self.handle,1)
        fpsmin,fpsmax=lib.tl_camera_get_frame_rate_control_value_range(self.handle)
        fps=min(max(fpsmin,1./frame_period),fpsmax)
        lib.tl_camera_set_frame_rate_control_value(self.handle,fps)
        return self.get_frame_period()


    _trigger_modes={"int":tl_camera_sdk_defs.TL_CAMERA_OPERATION_MODE.TL_CAMERA_OPERATION_MODE_SOFTWARE_TRIGGERED,
                    "ext":tl_camera_sdk_defs.TL_CAMERA_OPERATION_MODE.TL_CAMERA_OPERATION_MODE_HARDWARE_TRIGGERED,
                    "bulb":tl_camera_sdk_defs.TL_CAMERA_OPERATION_MODE.TL_CAMERA_OPERATION_MODE_BULB}
    _p_trigger_mode=interface.EnumParameterClass("trigger_mode",_trigger_modes)
    @interface.use_parameters(_returns="trigger_mode")
    def get_trigger_mode(self):
        """
        Get trigger mode.

        Can be ``"int"`` (internal/software), ``"ext"`` (external/hardware), or ``"bulb"`` (bulb trigger).
        """
        return lib.tl_camera_get_operation_mode(self.handle)
    @camera.acqstopped
    @interface.use_parameters(mode="trigger_mode")
    def set_trigger_mode(self, mode):
        """
        Set trigger mode.

        Can be ``"int"`` (internal/software), ``"ext"`` (external/hardware), or ``"bulb"`` (bulb trigger).
        """
        lib.tl_camera_set_operation_mode(self.handle,mode)
        return self.get_trigger_mode()
    _trigger_polarities={   "rise":tl_camera_sdk_defs.TL_CAMERA_TRIGGER_POLARITY.TL_CAMERA_TRIGGER_POLARITY_ACTIVE_HIGH,
                            "fall":tl_camera_sdk_defs.TL_CAMERA_TRIGGER_POLARITY.TL_CAMERA_TRIGGER_POLARITY_ACTIVE_LOW}
    _p_trigger_polarity=interface.EnumParameterClass("trigger_polarity",_trigger_polarities)
    @interface.use_parameters(_returns="trigger_polarity")
    def get_ext_trigger_parameters(self):
        """Return external trigger polarity"""
        return lib.tl_camera_get_trigger_polarity(self.handle)
    @camera.acqstopped
    @interface.use_parameters(polarity="trigger_polarity")
    def setup_ext_trigger(self, polarity):
        """Setup external trigger polarity (``"rise"`` or ``"fall"``)"""
        lib.tl_camera_set_trigger_polarity(self.handle,polarity)
        return self.get_ext_trigger_parameters()
    def send_software_trigger(self):
        """Send software trigger signal"""
        lib.tl_camera_issue_software_trigger(self.handle)

    def get_pixel_correction_parameters(self):
        """Return pixel correction parameters ``(enabled, threshold)``"""
        enabled=lib.tl_camera_get_is_hot_pixel_correction_enabled(self.handle)
        threshold=lib.tl_camera_get_hot_pixel_correction_threshold(self.handle)
        return (enabled,threshold)
    def setup_pixel_correction(self, enable=True, threshold=None):
        """Enable or disable hotpixel correction and set its threshold (``None`` means keep unchanged)"""
        lib.tl_camera_set_is_hot_pixel_correction_enabled(self.handle,enable)
        if threshold is not None:
            lib.tl_camera_set_hot_pixel_correction_threshold(self.handle,threshold)
        return self.get_pixel_correction_parameters()

    def get_gain_range(self):
        """Return the available gain range (in dB)"""
        return tuple(lib.tl_camera_convert_gain_to_decibels(self.handle,g) for g in lib.tl_camera_get_gain_range(self.handle))
    def get_gain(self):
        """Return the current gain (in dB)"""
        return lib.tl_camera_convert_gain_to_decibels(self.handle,lib.tl_camera_get_gain(self.handle))
    def set_gain(self, gain, truncate=True):
        """
        Set the current gain (in dB).
        
        If ``truncate==True``, truncate the value to lie within the allowed range; otherwise, out-of-range values cause an error.
        """
        gain=lib.tl_camera_convert_decibels_to_gain(self.handle,gain)
        if truncate:
            min_gain,max_gain=lib.tl_camera_get_gain_range(self.handle)
            gain=max(min_gain,min(gain,max_gain))
        lib.tl_camera_set_gain(self.handle,gain)
        return self.get_gain()
    
    def get_black_level_range(self):
        """Return the available black level range"""
        return lib.tl_camera_get_black_level_range(self.handle)
    def get_black_level(self):
        """Return the current black level"""
        return lib.tl_camera_get_black_level(self.handle)
    def set_black_level(self, level, truncate=True):
        """
        Set the current black level.
        
        If ``truncate==True``, truncate the value to lie within the allowed range; otherwise, out-of-range values cause an error.
        """
        if truncate:
            min_level,max_level=lib.tl_camera_get_black_level_range(self.handle)
            level=max(min_level,min(level,max_level))
        lib.tl_camera_set_black_level(self.handle,level)
        return self.get_black_level()
    
    def is_nir_boost_enabled(self):
        """Check if NIR boost is enabled"""
        if lib.tl_camera_get_nir_boost_enable is None:
            raise self.Error("NIR boost access is not supported by this version of the API")
        return lib.tl_camera_get_nir_boost_enable(self.handle)
    def enable_nir_boost(self, enable=True):
        """Enable or disable NIR boost"""
        if lib.tl_camera_get_nir_boost_enable is None:
            raise self.Error("NIR boost access access is not supported by this version of the API")
        lib.tl_camera_set_nir_boost_enable(self.handle,enable)
        return self.is_nir_boost_enabled()
    
    def is_cooling_enabled(self):
        """Check if cooling is enabled"""
        if lib.tl_camera_get_cooling_enable is None:
            raise self.Error("cooling access is not supported by this version of the API")
        return lib.tl_camera_get_cooling_enable(self.handle)
    def enable_cooling(self, enable=True):
        """Enable or disable cooling"""
        if lib.tl_camera_get_cooling_enable is None:
            raise self.Error("cooling access is not supported by this version of the API")
        lib.tl_camera_set_cooling_enable(self.handle,enable)
        return self.is_cooling_enabled()
    
    def is_led_enabled(self):
        """Check if led is enabled"""
        if lib.tl_camera_get_is_led_on is None:
            raise self.Error("LED access is not supported by this version of the API")
        return lib.tl_camera_get_is_led_on(self.handle)
    def enable_led(self, enable=True):
        """Enable or disable led"""
        if lib.tl_camera_get_is_led_on is None:
            raise self.Error("LED access is not supported by this version of the API")
        lib.tl_camera_set_is_led_on(self.handle,enable)
        return self.is_led_enabled()

    def get_timestamp_clock_frequency(self):
        """Return frequency of the frame timestamp clock (in Hz)"""
        if lib.tl_camera_get_timestamp_clock_frequency is None:
            return None
        try:
            return lib.tl_camera_get_timestamp_clock_frequency(self.handle) or None
        except ThorlabsTLCameraError:
            return None


    ### Acquisition process controls ###
    _max_frame_bytes=2000*2**20  # max RAM allowed by the API; seems to be exactly 2*2**30 (2GB), but adding ~2% margin of error
    _added_frame_size=2**15  # added internal RAM per frames; seems to be 2**14, but adding factor of 2 margin of error
    def setup_acquisition(self, nframes=100):  # pylint: disable=arguments-differ
        """
        Setup acquisition.

        `nframes` determines number of size of the ring buffer (by default, 100).
        """
        r,c=self._get_data_dimensions_rc()
        frame_nbytes=r*c*2+self._added_frame_size
        if self._max_frame_bytes is not None:
            nframes=min(int(self._max_frame_bytes/frame_nbytes),nframes)
        super().setup_acquisition(nframes=nframes)
        self._buffer.setup(nframes+10,self._get_data_dimensions_rc())
    def clear_acquisition(self):
        self.stop_acquisition()
        self._buffer.cleanup()
        super().clear_acquisition()
    def start_acquisition(self, frames_per_trigger="default", auto_start=True, nframes=None):  # pylint: disable=arguments-differ
        """
        Start camera acquisition.

        Args:
            frames_per_trigger: number of frames to acquire per trigger (software of hardware); ``None`` means unlimited number;
                by default, set to ``None`` for software trigger (i.e., run until stopped), and 1 for hardware trigger (i.e., one frame per trigger pulse)
            auto_start: if ``True`` and the trigger is set into software mode, automatically start recording;
                otherwise, only start recording when :meth:`send_software_trigger` is called explicitly;
                this value is meaningless in the hardware or bulb trigger mode
            nframes: number of frames in the ring buffer
        """
        self.stop_acquisition()
        kwargs={"nframes":nframes} if nframes else {}
        super().start_acquisition(**kwargs)
        nframes=self._acq_params["nframes"]
        if frames_per_trigger=="default":
            frames_per_trigger=None if self.get_trigger_mode()=="int" else 1
        lib.tl_camera_set_frames_per_trigger_zero_for_unlimited(self.handle,frames_per_trigger or 0)
        self._frame_counter.reset(self._acq_params["nframes"])
        self._buffer.reset()
        lib.tl_camera_arm(self.handle,max(self._acq_params["nframes"],10))
        if auto_start:
            time.sleep(0.05)
            lib.tl_camera_issue_software_trigger(self.handle)
    def stop_acquisition(self):
        if self.acquisition_in_progress():
            time.sleep(0.2) # seems to improve code stability (need to acquire several frames before disarming?)
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
            lib.tl_camera_disarm(self.handle)
    def acquisition_in_progress(self):
        return bool(lib.tl_camera_get_is_armed(self.handle))

    ### Image settings and transfer controls ###
    def get_detector_size(self):
        roi_range=lib.tl_camera_get_roi_range(self.handle)
        width=roi_range[6]+1
        height=roi_range[7]+1
        return width,height
    def get_roi(self):
        roi=lib.tl_camera_get_roi(self.handle)
        hbin=lib.tl_camera_get_binx(self.handle)
        vbin=lib.tl_camera_get_biny(self.handle)
        return (roi[0],roi[2]+1,roi[1],roi[3]+1,hbin,vbin)
    @camera.acqcleared
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        mhbin=lib.tl_camera_get_binx_range(self.handle)[1]
        mvbin=lib.tl_camera_get_biny_range(self.handle)[1]
        lib.tl_camera_set_binx(self.handle,min(max(hbin,1),mhbin))
        lib.tl_camera_set_biny(self.handle,min(max(vbin,1),mvbin))
        hbin=lib.tl_camera_get_binx(self.handle)
        vbin=lib.tl_camera_get_biny(self.handle)
        hlim,vlim=self.get_roi_limits(hbin=hbin,vbin=vbin)
        hstart,hend,hbin=self._truncate_roi_axis((hstart,hend,hbin),hlim)
        vstart,vend,vbin=self._truncate_roi_axis((vstart,vend,hbin),vlim)
        if hend-hstart==hlim.min and vend-vstart==vlim.min: # seems to not work for the absolute minimal roi
            if vend<vlim.max:
                vend+=1
            elif vstart>0:
                vstart-=1
        lib.tl_camera_set_roi(self.handle,hstart,vstart,hend-1,vend-1)
        return self.get_roi()
    def get_roi_limits(self, hbin=1, vbin=1):
        wdet,hdet=self.get_detector_size()
        roi_range=lib.tl_camera_get_roi_range(self.handle)
        hmin=roi_range[2]+1
        vmin=roi_range[3]+1
        mhbin=lib.tl_camera_get_binx_range(self.handle)[1]
        mvbin=lib.tl_camera_get_biny_range(self.handle)[1]
        hlim=camera.TAxisROILimit(hmin*hbin,wdet,1,hbin,mhbin)
        vlim=camera.TAxisROILimit(vmin*(1 if vbin==2 else vbin),hdet,1,vbin,mvbin)
        return hlim,vlim

    def _get_data_dimensions_rc(self):
        width=lib.tl_camera_get_image_width(self.handle)
        height=lib.tl_camera_get_image_height(self.handle)
        return height,width

    def _parse_metadata(self, metadata):
        if len(metadata)==0:
            return None
        tags={"TSI\x00","FCNT","PCKH","PCKL","IFMT","IOFF","ENDT"}
        tagvals={}
        for p in range(0,len(metadata),8):
            tag=py3.as_str(metadata[p:p+4])
            val=struct.unpack("<I",metadata[p+4:p+8])[0]
            if tag not in tags:
                warnings.warn("unrecognized metadata tag: {}".format(tag))
            elif tag=="ENDT":
                break
            else:
                tagvals[tag]=val
        metadata={}
        if "FCNT" in tagvals:
            metadata["fcnt"]=tagvals["FCNT"]
        if "PCKH" in tagvals and "PCKL" in tagvals:
            metadata["pck"]=(tagvals["PCKH"]<<32)+tagvals["PCKL"]
            if self._tsclk:
                metadata["tstmp"]=metadata["pck"]/self._tsclk
        if "IFMT" in tagvals:
            metadata["ifmt"]=tagvals["IFMT"]
        if "IOFF" in tagvals:
            metadata["ioff"]=tagvals["IOFF"]
        return [metadata.get(k) for k in ["fcnt","pck","ifmt","ioff"]]
    
    def _zero_frame(self, n):
        return np.zeros((n,)+self._buffer.frame_dim,dtype=self._default_image_dtype)
    def _wait_for_next_frame(self, timeout=20., idx=None):
        self._buffer.wait_for_frame(idx=idx,timeout=timeout)
    def _debayer(self, img, cinfo=None):
        cinfo=self.get_color_info() if cinfo is None else cinfo
        if cinfo is None:
            return img
        off={"red":(0,0),"blue":(1,1),"green_left_of_red":(0,1),"green_left_of_blue":(1,0)}.get(cinfo.filter_array_phase,(0,0))
        cimg=color.bayer_interpolate(img.astype("float"),off=off)
        cmatrix=np.dot(self._white_balance_matrix,cinfo.correction_matrix)
        cimg=np.tensordot(cimg,cmatrix,axes=(-1,1))
        cimg[cimg<0]=0
        return cimg.astype(img.dtype)
    def _color_convert(self, img, cinfo=None):
        if self._color_output=="raw" or cinfo is None:
            return img
        cimg=self._debayer(img,cinfo=cinfo)
        if self._color_space=="srgb":
            bit_depth=self.get_sensor_info().bit_depth
            cimg=color.linear_to_sRGB(cimg,2**bit_depth-1)
        if self._color_output=="grayscale":
            cimg=np.mean(cimg,axis=-1,dtype=cimg.dtype)
        return cimg
    def _read_frames(self, rng, return_info=False):
        data=[self._buffer.get_frame(n) for n in range(*rng)]
        cinfo=self.get_color_info()
        frames=[self._convert_indexing(self._color_convert(d[0],cinfo=cinfo),"rct") for d in data]
        infos=[TFrameInfo(n,*self._parse_metadata(d[1])) for n,d in zip(range(*rng),data)] if return_info else None
        return frames,infos,(1 if self._color_output=="rgb" and cinfo is not None else 0)

    def _get_grab_acquisition_parameters(self, nframes, buff_size):
        if buff_size is None:
            buff_size=self._default_acq_params.get("nframes",100)
        return {"nframes":buff_size,"frames_per_trigger":None,"auto_start":True}

    def read_multiple_images(self, rng=None, peek=False, missing_frame="skip", return_info=False, return_rng=False):
        """
        Read multiple images specified by `rng` (by default, all un-read images).

        If `rng` is specified, it is a tuple ``(first, last)`` with images range (first inclusive).
        If no new frames are available, return an empty list; if no acquisition is running, return ``None``.
        If ``peek==True``, return images but not mark them as read.
        `missing_frame` determines what to do with frames which are out of range (missing or lost):
        can be ``"none"`` (replacing them with ``None``), ``"zero"`` (replacing them with zero-filled frame), or ``"skip"`` (skipping them).
        If ``return_info==True``, return tuple ``(frames, infos)``, where ``infos`` is a list of :class:`TFrameInfo` instances
        describing frame index and frame metadata, which contains framestamp, pixel clock, pixel format, and pixel offset;
        if some frames are missing and ``missing_frame!="skip"``, the corresponding frame info is ``None``.
        if ``return_rng==True``, return the range covered resulting frames; if ``missing_frame=="skip"``, the range can be smaller
        than the supplied `rng` if some frames are skipped.
        """
        return super().read_multiple_images(rng=rng,peek=peek,missing_frame=missing_frame,return_info=return_info,return_rng=return_rng)