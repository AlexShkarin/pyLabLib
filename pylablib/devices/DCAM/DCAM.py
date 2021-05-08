from . import dcamapi4_lib
from .dcamapi4_lib import lib, DCAMError, DCAMLibError

from ...core.devio import interface
from ...core.utils import py3, dictionary
from ..interface import camera
from ..utils import load_lib

import numpy as np
import collections
import ctypes


class DCAMTimeoutError(DCAMError):
    "DCAM frame timeout error"


class LibraryController(load_lib.LibraryController):
    def _do_uninit(self):
        self.lib.dcamapi_uninit()
libctl=LibraryController(lib)
def restart_lib():
    libctl.shutdown()



def get_cameras_number():
    """Get number of connected DCAM cameras"""
    libctl.preinit()
    try:
        return lib.dcamapi_init()
    except DCAMError:
        return 0





TDeviceInfo=collections.namedtuple("TDeviceInfo",["vendor","model","serial_number","camera_version"])
TFrameInfo=collections.namedtuple("TFrameInfo",["frame_index","framestamp","timestamp_us","camerastamp","position","pixeltype"])
class DCAMCamera(camera.IBinROICamera, camera.IExposureCamera):
    Error=DCAMError
    TimeoutError=DCAMTimeoutError
    def __init__(self, idx=0):
        super().__init__()
        self.idx=idx
        self.handle=None
        self._opid=None
        self.dcamwait=None
        self.properties={}
        self._alloc_nframes=0
        self.open()
        self.v=dictionary.ItemAccessor(self.get_value,self.set_value)

        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("properties",self.get_all_properties,priority=-5)
        self._add_settings_variable("trigger_mode",self.get_trigger_mode,self.set_trigger_mode)
        self._add_settings_variable("ext_trigger",self.get_ext_trigger_parameters,self.setup_ext_trigger)
        self._add_settings_variable("readout_speed",self.get_readout_speed,self.set_readout_speed)
        self._add_status_variable("readout_time",self.get_frame_readout_time)
        self._add_status_variable("acq_status",self.get_status)
        self._add_status_variable("transfer_info",self.get_transfer_info)
        
    def _get_connection_parameters(self):
        return self.idx
    def open(self):
        """Open connection to the camera"""
        if self.handle is not None:
            return
        ncams=get_cameras_number()
        if self.idx>=ncams:
            raise DCAMError("camera index {} is not available ({} cameras exist)".format(self.idx,ncams))
        try:
            self.handle=lib.dcamdev_open(self.idx)
            self._opid=libctl.open().opid
            self.dcamwait=lib.dcamwait_open(self.handle)
            self._update_properties_list()
        except DCAMError:
            self.close()
            raise
    def close(self):
        """Close connection to the camera"""
        if self.handle:
            self.clear_acquisition()
            lib.dcamwait_close(self.dcamwait.hwait)
            lib.dcamdev_close(self.handle)
            libctl.close(self._opid)
        self.handle=None
        self._opid=None
    def is_opened(self):
        """Check if the device is connected"""
        return self.handle is not None


    def get_device_info(self):
        """
        Get camera model data.

        Return tuple ``(vendor, model, serial_number, camera_version)``.
        """
        vendor=py3.as_str(lib.dcamdev_getstring(self.handle,dcamapi4_lib.DCAM_IDSTR.DCAM_IDSTR_VENDOR))
        model=py3.as_str(lib.dcamdev_getstring(self.handle,dcamapi4_lib.DCAM_IDSTR.DCAM_IDSTR_MODEL))
        serial_number=py3.as_str(lib.dcamdev_getstring(self.handle,dcamapi4_lib.DCAM_IDSTR.DCAM_IDSTR_CAMERAID))
        camera_version=py3.as_str(lib.dcamdev_getstring(self.handle,dcamapi4_lib.DCAM_IDSTR.DCAM_IDSTR_CAMERAVERSION))
        return TDeviceInfo(vendor,model,serial_number,camera_version)


    class Property(object):
        """Camera property handler"""
        def __init__(self, cam_handle, name, pid, vmin, vmax, step, default, unit):
            object.__init__(self)
            self.cam_handle=cam_handle
            self.name=name
            self.pid=pid
            self.vmin=vmin
            self.vmax=vmax
            self.step=step
            self.default=default
            self.unit=unit
        def as_text(self, value=None):
            """Get property value as text (by default, current value)"""
            if value is None:
                value=self.get_value()
            return lib.dcamprop_getvaluetext(self.cam_handle,self.pid,value)
        def get_value(self):
            """Get current property value"""
            return lib.dcamprop_getvalue(self.cam_handle,self.pid)
        def set_value(self, value):
            """Set property value"""
            return lib.dcamprop_setgetvalue(self.cam_handle,self.pid,value)
        def __repr__(self):
            return "{}(name='{}', id={}, min={}, max={}, unit={})".format(self.__class__.__name__,self.name,self.pid,self.vmin,self.vmax,self.unit)

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
            except DCAMError:
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

    _p_trigger_mode=interface.EnumParameterClass("trigger_mode",{"int":1,"ext":2,"software":3})
    @camera.acqstopped
    @interface.use_parameters(mode="trigger_mode")
    def set_trigger_mode(self, mode):
        """
        Set trigger mode.

        Can be ``"int"`` (internal), ``"ext"`` (external), or ``"software"`` (software trigger).
        """
        self.set_value("TRIGGER SOURCE",mode)
        return self.get_trigger_mode()
    @interface.use_parameters(_returns="trigger_mode")
    def get_trigger_mode(self):
        """
        Get trigger mode.

        Can be ``"int"`` (internal), ``"ext"`` (external), or ``"software"`` (software trigger).
        """
        return int(self.get_value("TRIGGER SOURCE"))
    def setup_ext_trigger(self, invert=False, delay=0.):
        """Setup external trigger (inversion and delay)"""
        self.set_value("TRIGGER POLARITY",2 if invert else 1)
        self.set_value("TRIGGER DELAY",delay,error_on_missing=False)
        return self.get_ext_trigger_parameters()
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
    _p_readout_speed=interface.EnumParameterClass("readout_speed",{"slow":1,"fast":2})
    @camera.acqcleared
    @interface.use_parameters(speed="readout_speed")
    def set_readout_speed(self, speed="fast"):
        """Set readout speed (can be ``"fast"`` or ``"slow"``)"""
        self.set_value("READOUT SPEED",speed,error_on_missing=False)
        return self.get_readout_speed()
    @interface.use_parameters(_returns="readout_speed")
    def get_readout_speed(self):
        """Set current readout speed"""
        return self.get_value("READOUT SPEED",default=2,error_on_missing=False)
    def get_frame_readout_time(self):
        """Set current frame readout time"""
        return self.get_value("TIMING READOUT TIME")
    def get_frame_timings(self):
        """
        Get acquisition timing.

        Return tuple ``(exposure, frame_period)``.
        """
        exposure=self.get_exposure()
        return self._TAcqTimings(exposure,max(exposure,self.get_frame_readout_time()))
    def get_defect_correct_mode(self):
        """Check if the defect pixel correction mode is on"""
        return self.get_value("DEFECT CORRECT MODE",error_on_missing=False,default=1)==2
    @camera.acqstopped
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
    def _read_buffer(self, buffer):
        return lib.dcambuf_lockframe(self.handle,buffer)
    def _buffer_to_array(self, buffer): # TODO: different packing / color modes (generic for all cameras)
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
        return self._convert_indexing(img,"rct")

    def _get_data_dimensions_rc(self):
        return int(self.get_value("IMAGE HEIGHT")),int(self.get_value("IMAGE WIDTH"))
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        return (int(self.properties["SUBARRAY HSIZE"].vmax),int(self.properties["SUBARRAY VSIZE"].vmax))
    def get_roi(self):
        """
        Get current ROI.

        Return tuple ``(hstart, hend, vstart, vend, hbin, vbin)``.
        """
        hstart=int(self.get_value("SUBARRAY HPOS"))
        hend=hstart+int(self.get_value("SUBARRAY HSIZE"))
        vstart=int(self.get_value("SUBARRAY VPOS"))
        vend=vstart+int(self.get_value("SUBARRAY VSIZE"))
        hvbin=int(self.get_value("BINNING"))
        return (hstart,hend,vstart,vend,hvbin,hvbin)
    @camera.acqcleared
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        """
        Set current ROI.

        By default, all non-supplied parameters take extreme values.
        Binning is the same for both axes, so value of `vbin` is ignored (it is left for compatibility).
        """
        self.set_value("SUBARRAY MODE",2)
        hmax=self.properties["SUBARRAY HSIZE"].vmax
        hend=max(0,min(hend,hmax)) if hend else hmax
        vmax=self.properties["SUBARRAY VSIZE"].vmax
        vend=max(0,min(vend,vmax)) if vend else vmax
        min_roi,max_roi=self.get_roi_limits()
        if hbin<=1:  # TODO: other bin values?
            hbin=1
        elif hbin in {2,3}:
            hbin=2
        else:
            hbin=4
        hstart=max(0,min(hstart,hend-min_roi[1]))
        hstart=(hstart//min_roi[1])*min_roi[1]
        hend=(hend//min_roi[1])*min_roi[1]
        self.set_value("SUBARRAY HSIZE",min_roi[1])
        self.set_value("SUBARRAY HPOS",hstart)
        self.set_value("SUBARRAY HSIZE",max(hend-hstart,min_roi[1]))
        vstart=max(0,min(vstart,vend-min_roi[3]))
        vstart=(vstart//min_roi[3])*min_roi[3]
        vend=(vend//min_roi[3])*min_roi[3]
        self.set_value("SUBARRAY VSIZE",min_roi[3])
        self.set_value("SUBARRAY VPOS",(vstart//min_roi[3])*min_roi[3])
        self.set_value("SUBARRAY VSIZE",max(vend-vstart,min_roi[3]))
        self.set_value("BINNING",min(hbin,max_roi[4]))
        return self.get_roi()
    def get_roi_limits(self):
        params=["SUBARRAY HPOS","SUBARRAY VPOS","SUBARRAY HSIZE","SUBARRAY VSIZE","BINNING"]
        minp=tuple([self.properties[p].vmin for p in params])
        maxp=tuple([self.properties[p].vmax for p in params])
        min_roi=(0,minp[2],0,minp[3],minp[4],minp[4])
        max_roi=(maxp[0],maxp[2],maxp[1],maxp[3],maxp[4],maxp[4])
        return (min_roi,max_roi)

    @interface.use_parameters(mode="acq_mode")
    def setup_acquisition(self, mode="sequence", nframes=100):
        """
        Setup acquisition.

        `mode` can be either ``"snap"`` (single frame or a fixed number of frames) or ``"sequence"`` (continuous acquisition).
        `nframes` determines number of frames to acquire in the single mode, or size of the ring buffer in the ``"sequence"`` mode (by default, 100).
        """
        super().setup_acquisition(mode=mode,nframes=nframes)
        if self._acq_params["nframes"]!=self._alloc_nframes:
            self._allocate_buffer(nframes)
    def clear_acquisition(self):
        self.stop_acquisition()
        self._deallocate_buffer()
        super().clear_acquisition()

    def start_acquisition(self, *args, **kwargs):
        self.stop_acquisition()
        super().start_acquisition(*args,**kwargs)
        lib.dcamcap_start(self.handle,-1 if self._acq_params["mode"]=="sequence" else 0)
        self._frame_counter.reset(self._alloc_nframes)
    def stop_acquisition(self):
        if self.acquisition_in_progress():
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
            lib.dcamcap_stop(self.handle)

    _p_acq_status=interface.EnumParameterClass("acq_status",{
        "error":dcamapi4_lib.DCAMCAP_STATUS.DCAMCAP_STATUS_ERROR,
        "busy":dcamapi4_lib.DCAMCAP_STATUS.DCAMCAP_STATUS_BUSY,
        "ready":dcamapi4_lib.DCAMCAP_STATUS.DCAMCAP_STATUS_READY,
        "stable":dcamapi4_lib.DCAMCAP_STATUS.DCAMCAP_STATUS_STABLE,
        "unstable":dcamapi4_lib.DCAMCAP_STATUS.DCAMCAP_STATUS_UNSTABLE,
        })
    @interface.use_parameters(_returns="acq_status")
    def get_status(self):
        """
        Get acquisition status.

        Can be ``"busy"`` (capturing in progress), ``"ready"`` (ready for capturing),
        ``"stable"`` (not prepared for capturing), ``"unstable"`` (can't be prepared for capturing), or ``"error"`` (some other error).
        """
        return lib.dcamcap_status(self.handle)
    def acquisition_in_progress(self):
        return self.get_status()=="busy"
    def get_transfer_info(self):
        """
        Get frame transfer info.

        Return tuple ``(last_buff, frame_count)``, where ``last_buff`` is the index of the last filled buffer,
        and ``frame_count`` is the total number of acquired frames.
        """
        return tuple(lib.dcamcap_transferinfo(self.handle,0))
    def _get_acquired_frames(self):
        return self.get_transfer_info()[1]


    def _wait_for_next_frame(self, timeout=20., idx=None):
        if timeout is None or timeout>0.1:
            timeout=0.1
        try:
            eventmask=dcamapi4_lib.DCAMWAIT_EVENT.DCAMWAIT_CAPEVENT_FRAMEREADY
            lib.dcamwait_start(self.dcamwait.hwait,eventmask,int(timeout*1000))
            return
        except DCAMLibError as e:
            if e.code!=dcamapi4_lib.DCAMERR.DCAMERR_TIMEOUT:
                raise
    def _get_single_frame(self, buffer):
        """
        Get a frame at the given buffer index.

        If ``return_info==True``, return tuple ``(data, info)``, where info is the :class:`TFrameInfo` instance
        describing frame index, timestamp, camera stamp, frame location on the sensor, and pixel type.
        Does not advance the read frames counter.
        """
        sframe=self._read_buffer(buffer%self._alloc_nframes)
        info=TFrameInfo(buffer,sframe.framestamp,sframe.timestamp[0]*10**6+sframe.timestamp[1],sframe.camerastamp,(sframe.left,sframe.top),sframe.type)
        data=self._buffer_to_array(sframe)
        return data,info
    def _read_frames(self, rng, return_info=False):
        data=[self._get_single_frame(n) for n in range(rng[0],rng[1])]
        return [d[0] for d in data],[d[1] for d in data]
    def _zero_frame(self, n):
        dim=self.get_data_dimensions()
        bpp=int(self.get_value("BIT PER CHANNEL",8))
        dt="<u{}".format((bpp-1)//8+1)
        return np.zeros((n,)+dim,dtype=dt)
    def read_multiple_images(self, rng=None, peek=False, missing_frame="skip", return_info=False):
        """
        Read multiple images specified by `rng` (by default, all un-read images).

        If no new frames are available, return an empty list; if no acquisition is running, return ``None``.
        If ``peek==True``, return images but not mark them as read.
        `missing_frame` determines what to do with frames which are out of range (missing or lost):
        can be ``"none"`` (replacing them with ``None``), ``"zero"`` (replacing them with zero-filled frame), or ``"skip"`` (skipping them).
        If ``return_info==True``, return tuple ``(frames, infos)``, where ``infos`` is a list of :class:`TFrameInfo` instances
        describing frame index, framestamp and timestamp, camera stamp, frame location on the sensor, and pixel type;
        if some frames are missing and ``missing_frame!="skip"``, the corresponding frame info is ``None``.
        """
        return super().read_multiple_images(rng=rng,peek=peek,missing_frame=missing_frame,return_info=return_info)