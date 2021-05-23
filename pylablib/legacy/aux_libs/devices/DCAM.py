from ...core.devio.interface import IDevice
from ...core.utils import py3, funcargparse, dictionary, general
from ...core.dataproc import image as image_utils

_depends_local=[".DCAM_lib","...core.devio.interface"]

import numpy as np
import collections
import ctypes
import contextlib
import time
from future.utils import raise_from

from .DCAM_lib import lib, DCAMLibError

class DCAMError(RuntimeError):
    "Generic Hamamatsu camera error."
class DCAMTimeoutError(DCAMError):
    "Timeout while waiting."

def get_cameras_number():
    """Get number of connected Hamamatsu cameras"""
    lib.initlib()
    try:
        return lib.dcamapi_init()
    except DCAMLibError:
        return 0
_open_cameras=0

def restart_lib():
    global _open_cameras
    lib.dcamapi_uninit()
    _open_cameras=0

_rpyc=False

class DCAMCamera(IDevice):

    def __init__(self, idx=0):
        IDevice.__init__(self)
        lib.initlib()
        self.idx=idx
        self.handle=None
        self.dcamwait=None
        self.properties={}
        self._alloc_nframes=0
        self._default_nframes=100
        self._acq_mode=None
        self.open()
        self.image_indexing="rct"
        self._last_frame=None
        self.v=dictionary.ItemAccessor(self.get_value,self.set_value)

        self._add_full_info_node("model_data",self.get_model_data)
        self._add_status_node("properties",self.get_all_properties)
        self._add_settings_node("trigger_mode",self.get_trigger_mode,self.set_trigger_mode)
        self._add_settings_node("ext_trigger",self.get_ext_trigger_parameters,self.setup_ext_trigger)
        self._add_settings_node("exposure",self.get_exposure,self.set_exposure)
        self._add_settings_node("readout_speed",self.get_readout_speed,self.set_readout_speed)
        self._add_status_node("readout_time",self.get_readout_time)
        self._add_status_node("buffer_size",self.get_buffer_size)
        self._add_status_node("data_dimensions",self.get_data_dimensions)
        self._add_full_info_node("detector_size",self.get_detector_size)
        self._add_settings_node("roi",self.get_roi,self.set_roi)
        self._add_status_node("roi_limits",self.get_roi_limits)
        self._add_status_node("acq_status",self.get_status)
        self._add_status_node("transfer_info",self.get_transfer_info)
        
    def open(self):
        """Open connection to the camera"""
        global _open_cameras
        ncams=get_cameras_number()
        if self.idx>=ncams:
            raise DCAMError("camera index {} is not available ({} cameras exist)".format(self.idx,ncams))
        try:
            self.handle=lib.dcamdev_open(self.idx)
            _open_cameras+=1
            self.dcamwait=lib.dcamwait_open(self.handle)
            self._update_properties_list()
        except DCAMLibError:
            self.close()
    def close(self):
        """Close connection to the camera"""
        global _open_cameras
        if self.handle:
            lib.dcamwait_close(self.dcamwait.hwait)
            lib.dcamdev_close(self.handle)
            _open_cameras-=1
            if not _open_cameras:
                lib.dcamapi_uninit()
        self.handle=None
    def is_opened(self):
        """Check if the device is connected"""
        return self.handle is not None


    ModelData=collections.namedtuple("ModelData",["vendor","model","serial_number","camera_version"])
    def get_model_data(self):
        """
        Get camera model data.

        Return tuple ``(vendor, model, serial_number, camera_version)``.
        """
        vendor=py3.as_str(lib.dcamdev_getstring(self.handle,67109123))
        model=py3.as_str(lib.dcamdev_getstring(self.handle,67109124))
        serial_number=py3.as_str(lib.dcamdev_getstring(self.handle,67109122))
        camera_version=py3.as_str(lib.dcamdev_getstring(self.handle,67109125))
        model_data=self.ModelData(vendor,model,serial_number,camera_version)
        return tuple(model_data) if _rpyc else model_data


    class Property(object):
        def __init__(self, cam_handle, name, id, min, max, step, default, unit):
            object.__init__(self)
            self.cam_handle=cam_handle
            self.name=name
            self.id=id
            self.min=min
            self.max=max
            self.step=step
            self.default=default
            self.unit=unit
        def as_text(self, value=None):
            """Get property value as text (by default, current value)"""
            if value is None:
                value=self.get_value()
            return lib.dcamprop_getvaluetext(self.cam_handle,self.id,value)
        def get_value(self):
            """Get current property value"""
            return lib.dcamprop_getvalue(self.cam_handle,self.id)
        def set_value(self, value):
            """Set property value"""
            return lib.dcamprop_setgetvalue(self.cam_handle,self.id,value)
        def __repr__(self):
            return "{}(name='{}', id={}, min={}, max={}, unit={})".format(self.__class__.__name__,self.name,self.id,self.min,self.max,self.unit)

    def list_properties(self):
        """Return list of all available properties"""
        ids=lib.dcamprop_getallids(self.handle,0)
        names=[lib.dcamprop_getname(self.handle,i) for i in ids]
        props=[lib.dcamprop_getattr(self.handle,i) for i in ids]
        props=[self.Property(self.handle,name,idx,p.valuemin,p.valuemax,p.valuestep,p.valuedefault,p.iUnit) for (idx,name,p) in zip(ids,names,props)]
        return props
    def get_all_properties(self):
        props=self.list_properties()
        result={}
        for prop in props:    
            name=py3.as_str(prop.name).lower().replace(" ","_")
            result[name]={}
            result[name]["value"]=prop.get_value()
            try:
                result[name]["text_value"]=prop.as_text()
            except DCAMLibError:
                pass
        return result
    def _update_properties_list(self):
        props=self.list_properties()
        for p in props:
            self.properties[py3.as_str(p.name)]=p
    def get_value(self, name, error_on_missing=True, default=None):
        """
        Get value of a property with the given name.
        
        If the value doesn't exist and ``error_on_missing==True``, raise :exc:`DCAMError`; otherwise, return `default`.
        """
        if name not in self.properties:
            if error_on_missing:
                raise DCAMError("can't find property {}".format(name))
            else:
                return default
        return self.properties[name].get_value()
    def set_value(self, name, value, error_on_missing=True):
        """
        Set value of a property with the given name.
        
        If the value doesn't exist and ``error_on_missing==True``, raise :exc:`DCAMError`; otherwise, do nothing.
        """
        if name not in self.properties:
            if error_on_missing:
                raise DCAMError("can't find property {}".format(name))
            else:
                return
        return self.properties[name].set_value(value)


    def set_trigger_mode(self, mode):
        """
        Set trigger mode.

        Can be ``"int"`` (internal), ``"ext"`` (external), or ``"software"`` (software trigger).
        """
        trigger_modes={"int":1,"ext":2,"software":3}
        funcargparse.check_parameter_range(mode,"mode",trigger_modes.keys())
        self.set_value("TRIGGER SOURCE",trigger_modes[mode])
        return self.get_trigger_mode()
    def get_trigger_mode(self):
        """
        Get trigger mode.

        Can be ``"int"`` (internal), ``"ext"`` (external), or ``"software"`` (software trigger).
        """
        tm=int(self.get_value("TRIGGER SOURCE"))
        if tm in {1,2,3}:
            return ["int","ext","software"][tm-1]
        else:
            raise DCAMError("unknown trigger mode: {}".format(tm))
    def setup_ext_trigger(self, invert=False, delay=0.):
        """Setup external trigger (inversion and delay)"""
        self.set_value("TRIGGER POLARITY",2 if invert else 1)
        self.set_value("TRIGGER DELAY",delay,error_on_missing=False)
    def get_ext_trigger_parameters(self):
        """Return external trigger parameters (inversion and delay)"""
        invert=self.get_value("TRIGGER POLARITY")==2
        delay=self.get_value("TRIGGER DELAY",error_on_missing=False)
        return invert,delay
    def send_software_trigger(self):
        """Send software trigger signal"""
        lib.dcamcap_firetrigger(self.handle)
    def set_exposure(self, exposure):
        """Set camera exposure"""
        self.set_value("EXPOSURE TIME",exposure)
        return self.get_exposure()
    def get_exposure(self):
        """Set current exposure"""
        return self.get_value("EXPOSURE TIME")
    def set_readout_speed(self, speed="fast"):
        """Set readout speed (can be ``"fast"`` or ``"slow"``)"""
        self.set_value("READOUT SPEED",1 if speed=="slow" else 2,error_on_missing=False)
        return self.get_readout_speed()
    def get_readout_speed(self):
        """Set current readout speed"""
        return "fast" if self.get_value("READOUT SPEED",default=2,error_on_missing=False)==2 else "slow"
    def get_readout_time(self):
        """Set current readout time"""
        return self.get_value("TIMING READOUT TIME")
    def get_defect_correct_mode(self):
        """Check if the defect pixel correction mode is on"""
        return self.get_value("DEFECT CORRECT MODE",error_on_missing=False,default=1)==2
    def set_defect_correct_mode(self, enabled=True):
        """Enable or disable the defect pixel correction mode"""
        self.set_value("DEFECT CORRECT MODE",2 if enabled else 1,error_on_missing=False)
        return self.get_defect_correct_mode()

    def _allocate_buffer(self, nframes):
        self._deallocate_buffer()
        if nframes:
            lib.dcambuf_alloc(self.handle,nframes)
        self._alloc_nframes=nframes
    def _deallocate_buffer(self):
        lib.dcambuf_release(self.handle,0)
        self._alloc_nframes=0
        self._last_frame=None
    def _read_buffer(self, buffer):
        return lib.dcambuf_lockframe(self.handle,buffer)
    @contextlib.contextmanager
    def _reset_buffers(self):
        nframes=self._alloc_nframes
        self._deallocate_buffer()
        try:
            yield
        finally:
            self._allocate_buffer(nframes)
    def _buffer_to_array(self, buffer):
        bpp=int(buffer.bpp)
        if bpp==1:
            ct=ctypes.c_uint8*buffer.btot
        elif bpp==2:
            ct=ctypes.c_uint16*(buffer.btot//2)
        elif bpp==4:
            ct=ctypes.c_uint32*(buffer.btot//4)
        else:
            raise DCAMError("can't convert data with {} BBP into an array".format(bpp))
        data=ct.from_address(buffer.buf)
        img=np.array(data).reshape((buffer.height,buffer.width))
        return image_utils.convert_image_indexing(img,"rct",self.image_indexing)
    def get_buffer_size(self):
        """Get the size of the allocated ring buffer (0 if no buffer is allocated)"""
        return self._alloc_nframes
    FrameInfo=collections.namedtuple("FrameInfo",["framestamp","timestamp_us","camerastamp","left","top","pixeltype"])
    def get_frame(self, buffer, return_info=False):
        """
        Get a frame at the given buffer index.

        If ``return_info==True``, return tuple ``(data, info)``, where info is the :class:`FrameInfo` instance
        describing frame index and timestamp, camera stamp, frame location on the sensor, and pixel type.
        Does not advance the read frames counter.
        """
        sframe=self._read_buffer(buffer)
        info=self.FrameInfo(sframe.framestamp,sframe.timestamp[0]*10**6+sframe.timestamp[1],sframe.camerastamp,sframe.left,sframe.top,sframe.pixeltype)
        info=tuple(info) if _rpyc else info
        data=self._buffer_to_array(sframe)
        return (data,info) if return_info else data

    def get_data_dimensions(self):
        """Get the current data dimension (taking ROI and binning into account)"""
        dim=(int(self.get_value("IMAGE WIDTH")),int(self.get_value("IMAGE HEIGHT")))
        return image_utils.convert_shape_indexing(dim,"xy",self.image_indexing)
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        return (int(self.properties["SUBARRAY HSIZE"].max),int(self.properties["SUBARRAY VSIZE"].max))
    def get_roi(self):
        """
        Get current ROI.

        Return tuple ``(hstart, hend, vstart, vend, bin)`` (binning is the same for both axes).
        """
        hstart=int(self.get_value("SUBARRAY HPOS"))
        hend=hstart+int(self.get_value("SUBARRAY HSIZE"))
        vstart=int(self.get_value("SUBARRAY VPOS"))
        vend=vstart+int(self.get_value("SUBARRAY VSIZE"))
        bin=int(self.get_value("BINNING"))
        return (hstart,hend,vstart,vend,bin)
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, bin=1):
        """
        Set current ROI.

        By default, all non-supplied parameters take extreme values. Binning is the same for both axes.
        """
        with self._reset_buffers():
            self.set_value("SUBARRAY MODE",2)
            hend=hend or self.properties["SUBARRAY HSIZE"].max
            vend=vend or self.properties["SUBARRAY VSIZE"].max
            min_roi,max_roi=self.get_roi_limits()
            if bin==3:
                bin=2
            hstart=(hstart//min_roi[2])*min_roi[2]
            hend=(hend//min_roi[2])*min_roi[2]
            self.set_value("SUBARRAY HSIZE",min_roi[2])
            self.set_value("SUBARRAY HPOS",hstart)
            self.set_value("SUBARRAY HSIZE",max(hend-hstart,min_roi[2]))
            vstart=(vstart//min_roi[3])*min_roi[3]
            vend=(vend//min_roi[3])*min_roi[3]
            self.set_value("SUBARRAY VSIZE",min_roi[3])
            self.set_value("SUBARRAY VPOS",(vstart//min_roi[3])*min_roi[3])
            self.set_value("SUBARRAY VSIZE",max(vend-vstart,min_roi[3]))
            self.set_value("BINNING",min(bin,max_roi[4]))
        return self.get_roi()
    def get_roi_limits(self):
        """
        Get the minimal and maximal ROI parameters.

        Return tuple ``(min_roi, max_roi)``, where each element is in turn 5-tuple describing the ROI.
        """
        params=["SUBARRAY HPOS","SUBARRAY VPOS","SUBARRAY HSIZE","SUBARRAY VSIZE","BINNING"]
        minp=tuple([self.properties[p].min for p in params])
        maxp=tuple([self.properties[p].max for p in params])
        min_roi=(0,0)+minp[2:]
        max_roi=maxp
        return (min_roi,max_roi)

    def start_acquisition(self, mode="sequence", nframes=None):
        """
        Start acquisition.

        `mode` can be either ``"snap"`` (since frame or sequency acquisition) or ``"sequence"`` (continuous acquisition).
        `nframes` determines number of frames to acquire in ``"snap"`` mode, or size of the ring buffer in the ``"sequence"`` mode (by default, 100).
        """
        acq_modes=["sequence","snap"]
        funcargparse.check_parameter_range(mode,"mode",acq_modes)
        if nframes:
            self._allocate_buffer(nframes)
        elif not self._alloc_nframes:
            self._allocate_buffer(self._default_nframes)
        lib.dcamcap_start(self.handle,0 if mode=="snap" else -1)
        self._last_frame=-1
        self._acq_mode=(mode,nframes)
    def stop_acquisition(self):
        """Stop acquisition"""
        lib.dcamcap_stop(self.handle)
        self._acq_mode=None
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
    def get_status(self):
        """
        Get acquisition status.

        Can be ``"busy"`` (capturing in progress), ``"ready"`` (ready for capturing),
        ``"stable"`` (not prepared for capturing), ``"unstable"`` (can't be prepared for capturing), or ``"error"`` (some other error).
        """
        status=["error","busy","ready","stable","unstable"]
        return status[lib.dcamcap_status(self.handle)]
    def get_transfer_info(self):
        """
        Get frame transfer info.

        Return tuple ``(last_buff, frame_count)``, where ``last_buff`` is the index of the last filled buffer,
        and ``frame_count`` is the total number of acquired frames.
        """
        return tuple(lib.dcamcap_transferinfo(self.handle,0))
    def get_new_images_range(self):
        """
        Get the range of the new images.
        
        Return tuple ``(first, last)`` with images range (inclusive).
        If no images are available, return ``None``.
        If some images were in the buffer were overwritten, exclude them from the range.
        """
        if self._last_frame is None:
            return None
        _,frame_count=self.get_transfer_info()
        oldest_frame=max(self._last_frame+1,frame_count-self.get_buffer_size())
        if oldest_frame==frame_count:
            return None
        return oldest_frame,frame_count-1



    def read_multiple_images(self, rng=None, return_info=False, peek=False):
        """
        Read multiple images specified by `rng` (by default, all un-read images).

        If ``return_info==True``, return tuple ``(data, info)``, where info is the :class:`FrameInfo` instance
        describing frame index and timestamp, camera stamp, frame location on the sensor, and pixel type.
        If ``peek==True``, return images but not mark them as read.
        """
        if rng is None:
            rng=self.get_new_images_range()
        dim=self.get_data_dimensions()
        if rng is None:
            return np.zeros((0,dim[0],dim[1]))
        frames=[self.get_frame(n%self._alloc_nframes,return_info=True) for n in range(rng[0],rng[1]+1)]
        images,infos=list(zip(*frames))
        images=np.array(images)
        if not peek:
            self._last_frame=max(self._last_frame,rng[1])
        return (images,infos) if return_info else images
    def wait_for_frame(self, since="lastread", timeout=20., period=1E-3):
        """
        Wait for a new camera frame.

        `since` specifies what constitutes a new frame.
        Can be ``"lastread"`` (wait for a new frame after the last read frame), ``"lastwait"`` (wait for a new frame after last :meth:`wait_for_frame` call),
        or ``"now"`` (wait for a new frame acquired after this function call).
        If `timeout` is exceeded, raise :exc:`DCAMTimeoutError`.
        """
        funcargparse.check_parameter_range(since,"since",{"lastread","lastwait","now"})
        if since=="lastwait":
            ctd=general.Countdown(timeout)
            while True:
                try:
                    lib.dcamwait_start(self.dcamwait.hwait,0x02,0) # default timeout doesn't work, it's either 0 (for timeout=0) or infinite (for timeout>0)
                    return
                except DCAMLibError as e:
                    if e.text_code=="DCAMERR_TIMEOUT":
                        if ctd.passed():
                            raise_from(DCAMTimeoutError,None)
                    else:
                        raise
                time.sleep(period)
        elif since=="lastread":
            while self.get_new_images_range() is None:
                self.wait_for_frame(since="lastwait",timeout=timeout)
        else:
            rng=self.get_new_images_range()
            last_img=rng[1] if rng else None
            while True:
                self.wait_for_frame(since="lastwait",timeout=timeout)
                rng=self.get_new_images_range()
                if rng and (last_img is None or rng[1]>last_img):
                    return

    def snap(self, nframes=None, return_info=False):
        """Snap a single image (with preset image read mode parameters)"""
        readframes=nframes or 1
        self.start_acquisition("snap",nframes=readframes)
        while self.get_new_images_range()!=(0,readframes-1):
            self.wait_for_frame(since="lastwait")
        frames=self.read_multiple_images(return_info=return_info)
        if nframes is None:
            frames=(frames[0][0],frames[1][0]) if return_info else frames[0]
        return frames