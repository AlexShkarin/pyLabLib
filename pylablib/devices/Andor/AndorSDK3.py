from .base import AndorError, AndorTimeoutError, AndorNotSupportedError
from . import atcore_lib
from .atcore_lib import lib, AndorSDK3LibError, feature_types, nb_read_uint12

from ...core.utils import py3, dictionary
from ...core.devio import interface
from ..interface import camera
from ..utils import load_lib

import numpy as np
import collections
import ctypes
import threading
import struct



class LibraryController(load_lib.LibraryController):
    def _do_uninit(self):
        self.lib.AT_FinaliseLibrary()
libctl=LibraryController(lib)
def restart_lib():
    libctl.shutdown()


def get_cameras_number():
    """Get number of connected Andor cameras"""
    libctl.preinit()
    lib.AT_InitialiseLibrary()
    return lib.AT_GetInt(1,"DeviceCount")



TDeviceInfo=collections.namedtuple("TDeviceInfo",["camera_model","serial_number","firmware_version","software_version"])
TMissedFramesStatus=collections.namedtuple("TMissedFramesStatus",["skipped","overflows"])
TMetaData=collections.namedtuple("TMetaData",["timestamp_dev","size","pixeltype","stride"])
TFrameInfo=collections.namedtuple("TFrameInfo",["frame_index","metadata"])
class AndorSDK3Camera(camera.IBinROICamera, camera.IExposureCamera):
    """
    Andor SDK3 camera.

    Args:
        idx(int): camera index (use :func:`get_cameras_number` to get the total number of connected cameras)
    """
    Error=AndorError
    TimeoutError=AndorTimeoutError
    def __init__(self, idx=0):
        super().__init__()
        lib.initlib()
        self.idx=idx
        self.handle=None
        self._opid=None
        self._buffer_padding=10
        self._buffer_mgr=self.BufferManager(self)
        self._reg_cb=None
        self.open()
        self.v=dictionary.ItemAccessor(self.get_value,self.set_value)
        self._overflow_behavior="error"
        self._overflows_counter=0

        self._device_var_ignore_error={"get":(AndorNotSupportedError,),"set":(AndorNotSupportedError,)}
        self._add_info_variable("device_info",self.get_device_info)
        self._add_info_variable("values",self.get_all_values,priority=-5)
        self._add_settings_variable("trigger_mode",self.get_trigger_mode,self.set_trigger_mode)
        self._add_settings_variable("shutter",self.get_shutter,self.set_shutter)
        self._add_settings_variable("temperature",self.get_temperature_setpoint,self.set_temperature)
        self._add_status_variable("temperature_monitor",self.get_temperature)
        self._add_settings_variable("cooler",self.is_cooler_on,self.set_cooler)
        self._add_settings_variable("metadata_enabled",self.is_metadata_enabled,self.enable_metadata)
        self._add_settings_variable("frame_period",self.get_frame_period,self.set_frame_period)
        self._add_status_variable("missed_frames",self.get_missed_frames_status)



    def _get_connection_parameters(self):
        return self.idx
    def open(self):
        """Open connection to the camera"""
        self.close()
        ncams=get_cameras_number()
        if self.idx>=ncams:
            raise AndorError("camera index {} is not available ({} cameras exist)".format(self.idx,ncams))
        self.handle=lib.AT_Open(self.idx)
        self._opid=libctl.open().opid
        self._register_events()
    def close(self):
        """Close connection to the camera"""
        if self.handle is not None:
            self.clear_acquisition()
            self._unregister_events()
            lib.AT_Close(self.handle)
            libctl.close(self._opid)
        self.handle=None
        self._opid=None
    def is_opened(self):
        """Check if the device is connected"""
        return self.handle is not None

    def is_feature_available(self, name):
        """Check if given feature is available"""
        return lib.AT_IsImplemented(self.handle,name)
    def is_feature_readable(self, name):
        """Check if given feature is available"""
        return lib.AT_IsImplemented(self.handle,name) and lib.AT_IsReadable(self.handle,name) 
    def is_feature_writable(self, name):
        """Check if given feature is available"""
        return lib.AT_IsImplemented(self.handle,name) and lib.AT_IsWritable(self.handle,name) 
    def _check_feature(self, name, writable=False):
        if not self.is_feature_available(name) or (writable and not self.is_feature_writable(name)):
            raise AndorNotSupportedError("feature {} is not supported by camera {}".format(name,self.get_device_info().camera_model))
    def get_value(self, name, kind="auto", enum_str=True, default="error"):
        """
        Get current value of the given feature.
        
        `kind` determines feature kind, can be ``"int"``, ``"float"``, ``"str"``, ``"bool"`` or ``"enum``";
        by default (``"auto"``), auto-determine value kind (might not work for newer features).
        If ``enum_str==True``, return enum values as strings; otherwise, return as indices.
        If ``default=="error"``, raise :exc:`.AndorError` if the feature is not implemented; otherwise, return `default` if it is not implemented.
        """
        if kind=="auto":
            if name in feature_types:
                kind=feature_types[name]
            else:
                raise AndorError("can't determine feature kind: {}".format(name))
        if not lib.AT_IsImplemented(self.handle,name):
            if default=="error":
                raise AndorError("feature is not implemented: {}".format(name))
            else:
                return default
        if not lib.AT_IsReadable(self.handle,name):
            raise AndorError("feature is not readable: {}".format(name))
        if kind=="int":
            return lib.AT_GetInt(self.handle,name)
        if kind=="float":
            return lib.AT_GetFloat(self.handle,name)
        if kind=="str":
            strlen=lib.AT_GetStringMaxLength(self.handle,name)
            return lib.AT_GetString(self.handle,name,strlen)
        if kind=="bool":
            return bool(lib.AT_GetBool(self.handle,name))
        if kind=="enum":
            val=lib.AT_GetEnumIndex(self.handle,name)
            if enum_str:
                val=lib.AT_GetEnumStringByIndex(self.handle,name,val,512)
            return val
        raise AndorError("can't read feature '{}' with kind '{}'".format(name,kind))
    def set_value(self, name, value, kind="auto", not_implemented_error=True):
        """
        Set current value of the given feature.
        
        `kind` determines feature kind, can be ``"int"``, ``"float"``, ``"str"``, ``"bool"`` or ``"enum``";
        by default (``"auto"``), auto-determine value kind (might not work for newer features).

        If ``not_implemented_error==True`` and the feature is not implemented, raise :exc:`.AndorError`; otherwise, do nothing.
        """
        if kind=="auto":
            if name in feature_types:
                kind=feature_types[name]
            else:
                raise AndorError("can't determine feature kind: {}".format(name))
        if not lib.AT_IsImplemented(self.handle,name):
            if not_implemented_error:
                raise AndorError("feature is not implemented: {}".format(name))
            else:
                return
        if not lib.AT_IsWritable(self.handle,name):
            raise AndorError("feature is not writable: {}".format(name))
        if kind=="int":
            lib.AT_SetInt(self.handle,name,int(value))
        elif kind=="float":
            lib.AT_SetFloat(self.handle,name,float(value))
        elif kind=="str":
            lib.AT_SetString(self.handle,name,value)
        elif kind=="bool":
            lib.AT_SetBool(self.handle,name,bool(value))
        elif kind=="enum":
            if isinstance(value,py3.anystring):
                lib.AT_SetEnumString(self.handle,name,value)
            else:
                lib.AT_SetEnumIndex(self.handle,name,int(value))
        else:
            raise AndorError("can't read feature '{}' with kind '{}'".format(name,kind))
    def call_command(self, name):
        """Execute the given command"""
        if not lib.AT_IsImplemented(self.handle,name):
            raise AndorError("command is not implemented: {}".format(name))
        lib.AT_Command(self.handle,name)
    def get_value_range(self, name, kind="auto", enum_str=True):
        """
        Get allowed range of the given value.
        
        `kind` determines feature kind, can be ``"int"``, ``"float"``, ``"str"``, ``"bool"`` or ``"enum``";
        by default (``"auto"``), auto-determine value kind (might not work for newer features).

        For ``"int"`` or ``"float"`` values return tuple ``(min, max)`` (inclusive); for ``"enum"`` return list of possible values
        (if ``enum_str==True``, return list of string values, otherwise return list of indices).
        For all other value kinds return ``None``.
        """
        if kind=="auto":
            if name in feature_types:
                kind=feature_types[name]
            else:
                raise AndorError("can't determine feature kind: {}".format(name))
        if not lib.AT_IsImplemented(self.handle,name):
            raise AndorError("feature is not implemented: {}".format(name))
        if kind=="int":
            return (lib.AT_GetIntMin(self.handle,name),lib.AT_GetIntMax(self.handle,name))
        if kind=="float":
            return (lib.AT_GetFloatMin(self.handle,name),lib.AT_GetFloatMax(self.handle,name))
        if kind=="enum":
            count=lib.AT_GetEnumCount(self.handle,name)
            available=[i for i in range(count) if lib.AT_IsEnumIndexAvailable(self.handle,name,i)]
            if enum_str:
                available=[lib.AT_GetEnumStringByIndex(self.handle,name,i,512) for i in available]
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
        for v in feature_types:
            if feature_types[v]!="comm" and lib.AT_IsImplemented(self.handle,v) and lib.AT_IsReadable(self.handle,v):
                try:
                    values[v]=self.get_value(v,enum_str=enum_str)
                except AndorSDK3LibError:
                    pass
        return values


    def get_device_info(self):
        """
        Get camera info.

        Return tuple ``(camera_model, serial_number, firmware_version, software_version)``.
        """
        camera_model=self.get_value("CameraModel")
        serial_number=self.get_value("SerialNumber")
        firmware_version=self.get_value("FirmwareVersion")
        strlen=lib.AT_GetStringMaxLength(1,"SoftwareVersion")
        software_version=lib.AT_GetString(1,"SoftwareVersion",strlen)
        return TDeviceInfo(camera_model,serial_number,firmware_version,software_version)
        

    _p_trigger_mode=interface.EnumParameterClass("trigger_mode",
        {"int":"Internal","ext":"External","software":"Software","ext_start":"External start","ext_exp":"External Exposure"},match_prefix=False)
    @interface.use_parameters(_returns="trigger_mode")
    def get_trigger_mode(self):
        """
        Get trigger mode.

        Can be ``"int"`` (internal), ``"ext"`` (external), ``"software"`` (software trigger),
            ``"ext_start"`` (external start), or ``"ext_exp"`` (external exposure).
        """
        return self.get_value("TriggerMode")
    @camera.acqstopped
    @interface.use_parameters(mode="trigger_mode")
    def set_trigger_mode(self, mode):
        """
        Set trigger mode.

        Can be ``"int"`` (internal), ``"ext"`` (external), or ``"software"`` (software trigger).
        """
        self.set_value("TriggerMode",mode)
        return self.get_trigger_mode()

    _p_shutter_mode=interface.EnumParameterClass("shutter_mode",{"open":"Open","closed":"Closed","auto":"Auto"})
    @interface.use_parameters(_returns="shutter_mode")
    def get_shutter(self):
        """Get current shutter mode"""
        self._check_feature("ShutterMode")
        return self.get_value("ShutterMode")
    @interface.use_parameters(mode="shutter_mode")
    def set_shutter(self, mode):
        """
        Set trigger mode.

        Can be ``"open"``, ``"closed"``, or ``"auto"``.
        """
        self._check_feature("ShutterMode")
        self.set_value("ShutterMode",mode)
        return self.get_shutter()

    def is_cooler_on(self):
        """Check if the cooler is on"""
        self._check_feature("SensorCooling")
        return self.get_value("SensorCooling")
    @camera.acqstopped
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
    @camera.acqstopped
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
    def set_exposure(self, exposure):
        """Set camera exposure"""
        self.set_frame_period(0)
        exposure=self.limit_value("ExposureTime",exposure)
        self.set_value("ExposureTime",exposure)
        return self.get_exposure()
    def get_frame_period(self):
        return 1./self.get_value("FrameRate")
    def set_frame_period(self, frame_period):
        if not self.is_feature_writable("FrameRate"):
            return
        fr_rng=self.get_value_range("FrameRate")
        ro_rng=1./fr_rng[1],1./fr_rng[0]
        frame_period=max(min(frame_period,ro_rng[1]),ro_rng[0])
        self.set_value("FrameRate",1./frame_period)
        return self.get_frame_period()
    def get_frame_timings(self):
        return self._TAcqTimings(self.get_exposure(),self.get_frame_period())

    def is_metadata_enabled(self):
        """Check if the metadata enabled"""
        return self.get_value("MetadataEnable",default=False)
    def enable_metadata(self, enable=True):
        """Enable or disable metadata streaming"""
        self.set_value("MetadataEnable",enable,not_implemented_error=False)
        return self.is_metadata_enabled()
    
    ### Frame management ###
    class BufferManager:
        """Buffer manager: stores, constantly reads and re-schedules buffers, keeps track of acquired frames and buffer overflow events"""
        def __init__(self, cam):
            self.buffers=None
            self.queued_buffers=0
            self.size=0
            self.overflow_detected=False
            self.stop_requested=False
            self.cam=cam
            self._cnt_lock=threading.RLock()
            self._frame_notifier=camera.FrameNotifier()
            self._buffer_loop_thread=None
        def allocate_buffers(self, nbuff, size, queued_buffers=None):
            """
            Allocate and queue buffers.

            `queued_buffers`` specifies number of allocated buffers to keep queued at a given time (by default, all of them)
            """
            with self._cnt_lock:
                self.deallocate_buffers()
                self.buffers=[ctypes.create_string_buffer(size) for _ in range(nbuff)]
                self.queued_buffers=queued_buffers or len(self.buffers)
                self.size=size
                for b in self.buffers[:self.queued_buffers]:
                    lib.AT_QueueBuffer(self.cam.handle,ctypes.cast(b,ctypes.POINTER(ctypes.c_uint8)),self.size)
        def deallocate_buffers(self):
            """Deallocated buffers (flushing should be done manually)"""
            with self._cnt_lock:
                if self.buffers:
                    self.stop_loop()
                    self.buffers=None
                    self.size=0
        def reset(self):
            """Reset counter (on frame acquisition)"""
            self._frame_notifier.reset()
            self.overflow_detected=False
        def _acq_loop(self):
            while not self.stop_requested:
                try:
                    _,size=lib.AT_WaitBuffer(self.cam.handle,300)
                    if size!=self.size:
                        raise AndorError("unexpected buffer size: expected {}, got {}".format(self.size,size))
                except AndorSDK3LibError as e:
                    if e.code!=atcore_lib.AT_ERR.AT_ERR_TIMEDOUT:
                        raise
                    continue
                next_buff=self.buffers[(self._frame_notifier.counter+self.queued_buffers)%len(self.buffers)]
                lib.AT_QueueBuffer(self.cam.handle,ctypes.cast(next_buff,ctypes.POINTER(ctypes.c_uint8)),self.size)
                self._frame_notifier.inc()
        def read(self, idx):
            """Return the oldest available acquired but not read buffer, and mark it as read"""
            buff_idx=idx%len(self.buffers)
            return ctypes.string_at(self.buffers[buff_idx],self.size)
        def start_loop(self):
            """Start buffer scheduling loop"""
            self.stop_loop()
            self.reset()
            self.stop_requested=False
            self._buffer_loop_thread=threading.Thread(target=self._acq_loop,daemon=True)
            self._buffer_loop_thread.start()
        def stop_loop(self):
            """Stop buffer scheduling loop"""
            if self._buffer_loop_thread is not None:
                self.stop_requested=True
                self._buffer_loop_thread.join()
                self._buffer_loop_thread=None
        def wait_for_frame(self, idx=None, timeout=None):
            """Wait for a new frame acquisition"""
            self._frame_notifier.wait(idx=idx,timeout=timeout)
        def on_overflow(self):
            """Process buffer overflow event"""
            with self._cnt_lock:
                self.overflow_detected=True
        def new_overflow(self):
            with self._cnt_lock:
                return self.overflow_detected
        def get_status(self):
            """Get counter status: tuple ``(acquired, total_length)``"""
            with self._cnt_lock:
                return self._frame_notifier.counter,len(self.buffers or [])
    def _register_events(self):
        self._unregister_events()
        self.set_value("EventSelector","BufferOverflowEvent")
        self.set_value("EventEnable",True)
        buff_cb=lib.AT_RegisterFeatureCallback(self.handle,"BufferOverflowEvent",lambda *args: self._buffer_mgr.on_overflow())
        self._reg_cb=buff_cb
        self._buffer_mgr.reset()
    def _unregister_events(self):
        if self._reg_cb is not None:
            lib.AT_UnregisterFeatureCallback(self.handle,"BufferOverflowEvent",self._reg_cb)
            self.set_value("EventSelector","BufferOverflowEvent")
            self.set_value("EventEnable",False)
            self._reg_cb=None
            self._buffer_mgr.reset()
    def _allocate_buffers(self, nframes):
        """
        Create and set up a new ring buffer.

        If a ring buffer is already allocated, remove it and create a new one.
        """
        self._deallocate_buffers()
        frame_size=self.get_value("ImageSizeBytes")
        self._buffer_mgr.allocate_buffers(nframes+self._buffer_padding,frame_size,queued_buffers=nframes)
    def _deallocate_buffers(self):
        """Remove the ring buffer and clean up the memory"""
        lib.flush_buffers(self.handle)
        self._buffer_mgr.deallocate_buffers()


    @interface.use_parameters(mode="acq_mode")
    def setup_acquisition(self, mode="sequence", nframes=100):
        """
        Setup acquisition.

        `mode` can be either ``"snap"`` (since frame or sequency acquisition) or ``"sequence"`` (continuous acquisition).
        `nframes` determines number of frames to acquire in the single mode, or size of the ring buffer in the ``"sequence"`` mode (by default, 100).
        """
        super().setup_acquisition(mode=mode,nframes=nframes)
    def clear_acquisition(self):
        self.stop_acquisition()
        self._deallocate_buffers()
        self.reset_overflows_counter()
        super().clear_acquisition()

    def start_acquisition(self, *args, **kwargs):
        self.stop_acquisition()
        super().start_acquisition(*args,**kwargs)
        nframes=self._acq_params["nframes"]
        if self._acq_params["mode"]=="snap":
            self.set_value("CycleMode","Fixed")
            self.set_value("FrameCount",nframes)
        else:
            # self.set_value("CycleMode","Continuous") # Zyla bug doesn't allow continuous mode with >1000 FPS
            self.set_value("CycleMode","Fixed")
            self.set_value("FrameCount",self.get_value_range("FrameCount")[1])
        self._allocate_buffers(nframes)
        self._frame_counter.reset(nframes)
        self._buffer_mgr.reset()
        self._buffer_mgr.start_loop()
        self.call_command("AcquisitionStart")
    def stop_acquisition(self):
        if self.get_value("CameraAcquiring"):
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
            self.call_command("AcquisitionStop")
            self._buffer_mgr.stop_loop()
    def acquisition_in_progress(self):
        return self.get_value("CameraAcquiring")
    


    def _get_acquired_frames(self):
        return self._buffer_mgr.get_status()[0]
    def get_missed_frames_status(self):
        """
        Get missed frames status.

        Return tuple ``(skipped, overflows)`` with the number skipped frames (sent from camera to the PC, but not read and overwritten)
        and number of buffer overflows (events when the frame rate is too for the data transfer, so some unknown number of frames is skipped).
        """
        skipped_frames=self.get_frames_status().skipped
        return TMissedFramesStatus(skipped_frames,self._overflows_counter)
    def reset_overflows_counter(self):
        """Reset buffer overflows counter"""
        self._overflows_counter=0
    _p_overflow_behavior=interface.EnumParameterClass("overflow_behavior",["error","restart","ignore"])
    @interface.use_parameters(behavior="overflow_behavior")
    def set_overflow_behavior(self, behavior):
        """
        Choose the camera behavior if buffer overflow is encountered when waiting for a new frame.

        Can be ``"error"`` (raise ``AndorError``), ``"restart"`` (restart the acquisition), or ``"ignore"`` (ignore the overflow, which will cause the wait to time out).
        """
        self._overflow_behavior=behavior


    def _parse_metadata_section(self, cid, data):
        if cid==1:
            return struct.unpack("<Q",data)[0]
        if cid==7:
            data=struct.unpack("<HBBHH",data)
            return (data[0],data[1],data[3],data[4])
        return data
    def _parse_metadata(self, metadata):
        c1=metadata.get(1,None)
        c7=metadata.get(7,(None,)*4)
        return TMetaData(c1,(c7[2],c7[3]),c7[1],c7[0])
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
                cid,clen=struct.unpack("<II",img[imlen-read_len-8:imlen-read_len])
                chunks[cid]=img[imlen-read_len-clen-4:imlen-read_len-8]
                read_len+=clen+4
            if 0 not in chunks:
                raise AndorError("missing image data")
            img=chunks.pop(0)
            metadata=chunks
        else:
            metadata={}
        metadata={cid:self._parse_metadata_section(cid,data) for (cid,data) in metadata.items()}
        metadata=self._parse_metadata(metadata)
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
            dtype="<u{}".format(int(bpp))
            if stride==bpp*width:
                img=np.frombuffer(img,dtype=dtype,count=width*height).reshape(height,width)
            elif stride%bpp==0:
                img=np.frombuffer(img,dtype=dtype,count=(stride//bpp)*height).reshape(height,-1)[:,:width]
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
        img=self._convert_indexing(img,"rct")
        return img,metadata

    def _get_data_dimensions_rc(self):
        return self.get_value("AOIHeight"),self.get_value("AOIWidth")
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
    @camera.acqstopped
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        """
        Set current ROI.

        By default, all non-supplied parameters take extreme values. Binning is the same for both axes.
        """
        det_size=self.get_detector_size()
        hend=min(hend or det_size[0],det_size[0])
        vend=min(vend or det_size[1],det_size[1])
        hbin=max(hbin,1)
        vbin=max(vbin,1)
        self.set_value("AOILeft",1)
        self.set_value("AOITop",1)
        self.set_value("AOIHBin",1)
        self.set_value("AOIVBin",1)
        minw=self.get_value_range("AOIWidth")[0]
        minh=self.get_value_range("AOIHeight")[0]
        self.set_value("AOIWidth",minw)
        self.set_value("AOIHeight",minh)
        self.set_value("AOIHBin",hbin)
        self.set_value("AOIVBin",vbin)
        hbin=self.get_value("AOIHBin")
        vbin=self.get_value("AOIVBin")
        minw=self.get_value_range("AOIWidth")[0]
        minh=self.get_value_range("AOIHeight")[0]
        hstart=min(hstart,det_size[0]-minw*hbin)
        vstart=min(vstart,det_size[1]-minh*vbin)
        self.set_value("AOILeft",hstart+1)
        self.set_value("AOITop",vstart+1)
        self.set_value("AOIWidth",max((hend-hstart)//hbin,minw))
        self.set_value("AOIHeight",max((vend-vstart)//vbin,minh))
        return self.get_roi()
    def get_roi_limits(self):
        params=["AOILeft","AOITop","AOIWidth","AOIHeight","AOIHBin","AOIVBin"]
        minp,maxp=[list(p) for p in zip(*[self.get_value_range(p) for p in params])]
        bins=[self.get_value(p) for p in params[-2:]]
        for i in range(2):
            minp[i]-=1
            maxp[i]-=1
        for i in range(4):
            minp[i]*=bins[i%2]
            maxp[i]*=bins[i%2]
        min_roi=(0,minp[2],0,minp[3])+tuple(minp[4:])
        max_roi=(maxp[2]-minp[2],maxp[2],maxp[3]-minp[3],maxp[3],maxp[4],maxp[5])
        return (min_roi,max_roi)
    
    def _check_buffer_overflow(self):
        if self._buffer_mgr.new_overflow():
            self._overflows_counter+=1
            if self._overflow_behavior=="ignore":
                return False
            if self._overflow_behavior=="error":
                self.stop_acquisition()
                raise AndorError("buffer overflow")
            self.start_acquisition()
            return True
        return False
    def _wait_for_next_frame(self, timeout=20., idx=None):
        if self._check_buffer_overflow():
            raise AndorTimeoutError("buffer overflow while waiting for a new frame")
        self._buffer_mgr.wait_for_frame(idx=idx,timeout=timeout)
    def _read_frames(self, rng, return_info=False):
        data=[self._parse_image(self._buffer_mgr.read(i)) for i in range(*rng)]
        return [d[0] for d in data],[TFrameInfo(n,d[1]) for (n,d) in zip(range(*rng),data)]
    def _zero_frame(self, n):
        dim=self.get_data_dimensions()
        bpp=self.get_value("BytesPerPixel")
        dt="<u{}".format(int(np.ceil(bpp))) # can be fractional (e.g., 1.5)
        return np.zeros((n,)+dim,dtype=dt)
    def read_multiple_images(self, rng=None, peek=False, missing_frame="skip", return_info=False):
        """
        Read multiple images specified by `rng` (by default, all un-read images).

        If no new frames are available, return an empty list; if no acquisition is running, return ``None``.
        If ``peek==True``, return images but not mark them as read.
        `missing_frame` determines what to do with frames which are out of range (missing or lost):
        can be ``"none"`` (replacing them with ``None``), ``"zero"`` (replacing them with zero-filled frame), or ``"skip"`` (skipping them).
        If ``return_info==True``, return tuple ``(frames, infos)``, where ``infos`` is a list of :class:`TFrameInfo` instances
        describing frame index and frame metadata, which contains timestamp, image size, pixel format, and row stride;
        if some frames are missing and ``missing_frame!="skip"``, the corresponding frame info is ``None``.
        """
        return super().read_multiple_images(rng=rng,peek=peek,missing_frame=missing_frame,return_info=return_info)