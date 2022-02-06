from .tl_camera_sdk_lib import ThorlabsTLCameraError
from .tl_camera_sdk_lib import wlib as lib
from . import tl_camera_sdk_defs

from ...core.devio import interface
from ..interface import camera
from ...core.utils import py3
from ..utils import load_lib

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
        self.open()
        
        self._add_info_variable("device_info",self.get_device_info)
        self._add_settings_variable("trigger_mode",self.get_trigger_mode,self.set_trigger_mode)
        self._add_settings_variable("ext_trigger",self.get_ext_trigger_parameters,self.setup_ext_trigger,ignore_error=self.Error)
        self._add_settings_variable("hotpixel_correction",self.get_pixel_correction_parameters,self.setup_pixel_correction,ignore_error=(self.Error,OSError))  # sometimes raises OSError; DLL issues?
        self._add_info_variable("timestamp_clock_frequency",self.get_timestamp_clock_frequency)
        self._add_status_variable("frame_period",self.get_frame_period)
        
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
                lib.tl_camera_set_image_poll_timeout(self.handle,1000)
                self._register_new_frame_callback()
                self._tsclk=self.get_timestamp_clock_frequency()
                self._opid=libctl.open().opid
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

    def get_timestamp_clock_frequency(self):
        """Return frequency of the frame timestamp clock (in Hz)"""
        return lib.tl_camera_get_timestamp_clock_frequency(self.handle) or None


    ### Acquisition process controls ###
    def setup_acquisition(self, nframes=100):  # pylint: disable=arguments-differ
        """
        Setup acquisition.

        `nframes` determines number of size of the ring buffer (by default, 100).
        """
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
        width=lib.tl_camera_get_image_width_range(self.handle)[1]
        height=lib.tl_camera_get_image_height_range(self.handle)[1]
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
        hmin=lib.tl_camera_get_image_width_range(self.handle)[0]
        vmin=lib.tl_camera_get_image_height_range(self.handle)[0]
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
    def _read_frames(self, rng, return_info=False):
        data=[self._buffer.get_frame(n) for n in range(*rng)]
        frames=[self._convert_indexing(d[0],"rct") for d in data]
        infos=[TFrameInfo(n,*self._parse_metadata(d[1])) for n,d in zip(range(*rng),data)] if return_info else None
        return frames,infos

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