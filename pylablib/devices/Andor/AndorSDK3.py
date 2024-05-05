from .base import AndorError, AndorTimeoutError, AndorFrameTransferError, AndorNotSupportedError
from .atcore_lib import wlib as lib, AndorSDK3LibError, feature_types, read_uint12

from ...core.utils import py3, dictionary, general, funcargparse
from ...core.devio import interface
from ...core.utils.ctypes_tools import funcaddressof, as_ctypes_array
from ..interface import camera
from ..utils import load_lib
from ...core.utils.cext_tools import try_import_cext
with try_import_cext():
    from .utils import looper, copyframes  # pylint: disable=no-name-in-module

import numpy as np
import collections
import ctypes
import threading



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





class AndorSDK3Attribute:
    """
    Andor SDK3 camera attribute.

    Allows to query and set values and get additional information.
    Usually created automatically by a Andor SDK3 camera instance, but could also be created manually.

    Args:
        handle: Andor SDK3 camera handle
        pid: attribute id
        kind: attribute kind; can be ``"float"``, ``"int"``, ``"str"``, ``"bool"``, ``"enum"``, or ``"comm"`` (command);
            can also be ``"auto"`` (default), in which case it is obtained from the stored feature table;
            newer features might be missing, in which case kind needs to be supplied explicitly, or it raises an error

    Attributes:
        name: attribute name
        kind: attribute kind; can be ``"float"``, ``"int"``, ``"str"``, ``"bool"``, ``"enum"``, or ``"comm"`` (command)
        implemented (bool): whether attribute is implemented
        readable (bool): whether attribute is readable
        writable (bool): whether attribute is writable
        min (float or int): minimal attribute value (if applicable)
        max (float or int): maximal attribute value (if applicable)
        ivalues: list of possible integer values for enum attributes
        values: list of possible text values for enum attributes
        labels: dict ``{label: index}`` which shows all possible values of an enumerated attribute and their corresponding numerical values
        ilabels: dict ``{index: label}`` which shows labels corresponding to numerical values of an enumerated attribute
        is_command (bool): whether attribute is a command (same as ``kind=="comm"``)
    """
    def __init__(self, handle, name, kind="auto"):
        self.handle=handle
        self.name=py3.as_str(name)
        self.implemented=bool(lib.AT_IsImplemented(self.handle,self.name))
        if kind=="auto":
            if self.name not in feature_types:
                raise AndorError("can't determine feature kind: {}".format(self.name))
            kind=feature_types[self.name]
        funcargparse.check_parameter_range(kind,"kind",{"float","int","str","bool","enum","comm"})
        self.kind=kind
        self.is_command=self.kind=="comm"
        self.readable=self.implemented and not self.is_command and bool(lib.AT_IsReadable(self.handle,self.name))
        self.writable=self.implemented and not self.is_command and bool(lib.AT_IsWritable(self.handle,self.name))
        self.min=None
        self.max=None
        self.values=[]
        self.ivalues=[]
        self.labels={}
        self.ilabels={}
        if self.kind in {"int","float"}:
            try:
                self.min,self.max=self.get_range()
            except AndorError:
                pass
        elif self.kind=="enum":
            try:
                self._update_enum_limits()
            except AndorError:
                pass
    def __repr__(self):
        return "{}(name='{}', kind='{}')".format(self.__class__.__name__,self.name,self.kind)

    def update_properties(self):
        """Update all attribute properties: implemented, readable, writable, limits"""
        self.implemented=bool(lib.AT_IsImplemented(self.handle,self.name))
        self.readable=self.implemented and not self.is_command and bool(lib.AT_IsReadable(self.handle,self.name))
        self.writable=self.implemented and not self.is_command and bool(lib.AT_IsWritable(self.handle,self.name))
        try:
            self.update_limits()
        except AndorError:
            pass
    def get_value(self, enum_as_str=True, not_implemented_error=True, default=None):
        """
        Get current value.
        
        If ``enum_as_str==True``, return enum values as strings; otherwise, return as indices.
        If ``not_implemented_error==True`` and the feature is not implemented, raise :exc:`.AndorError`;
        otherwise, return `default` if it is not implemented.
        """
        if not self.implemented:
            if not_implemented_error:
                raise AndorError("feature is not implemented: {}".format(self.name))
            else:
                return default
        if not self.readable:
            raise AndorError("feature is not readable: {}".format(self.name))
        if self.kind=="int":
            return lib.AT_GetInt(self.handle,self.name)
        if self.kind=="float":
            return lib.AT_GetFloat(self.handle,self.name)
        if self.kind=="str":
            strlen=lib.AT_GetStringMaxLength(self.handle,self.name)
            return lib.AT_GetString(self.handle,self.name,strlen)
        if self.kind=="bool":
            return bool(lib.AT_GetBool(self.handle,self.name))
        if self.kind=="enum":
            val=lib.AT_GetEnumIndex(self.handle,self.name)
            if enum_as_str:
                val=lib.AT_GetEnumStringByIndex(self.handle,self.name,val,512)
            return val
        raise AndorError("can't read feature '{}' with kind '{}'".format(self.name,self.kind))
    def set_value(self, value, not_implemented_error=True):
        """
        Set current value.

        If ``not_implemented_error==True`` and the feature is not implemented, raise :exc:`.AndorError`; otherwise, do nothing.
        """
        if not self.implemented:
            if not_implemented_error:
                raise AndorError("feature is not implemented: {}".format(self.name))
            else:
                return
        if not self.writable:
            raise AndorError("feature is not writable: {}".format(self.name))
        if self.kind=="int":
            lib.AT_SetInt(self.handle,self.name,int(value))
        elif self.kind=="float":
            lib.AT_SetFloat(self.handle,self.name,float(value))
        elif self.kind=="str":
            lib.AT_SetString(self.handle,self.name,value)
        elif self.kind=="bool":
            lib.AT_SetBool(self.handle,self.name,bool(value))
        elif self.kind=="enum":
            if isinstance(value,py3.anystring):
                lib.AT_SetEnumString(self.handle,self.name,value)
            else:
                lib.AT_SetEnumIndex(self.handle,self.name,int(value))
        else:
            raise AndorError("can't set feature '{}' with kind '{}'".format(self.name,self.kind))
    def call_command(self):
        """Execute the given command"""
        if not self.implemented:
            raise AndorError("command is not implemented: {}".format(self.name))
        lib.AT_Command(self.handle,self.name)
    def get_range(self, enum_as_str=True):
        """
        Get allowed range of the given value.
        
        For ``"int"`` or ``"float"`` values return tuple ``(min, max)`` (inclusive); for ``"enum"`` return list of possible values
        (if ``enum_as_str==True``, return list of string values, otherwise return list of indices).
        For all other value kinds return ``None``.
        """
        if not self.implemented:
            raise AndorError("feature is not implemented: {}".format(self.name))
        if self.kind=="int":
            return (lib.AT_GetIntMin(self.handle,self.name),lib.AT_GetIntMax(self.handle,self.name))
        if self.kind=="float":
            return (lib.AT_GetFloatMin(self.handle,self.name),lib.AT_GetFloatMax(self.handle,self.name))
        if self.kind=="enum":
            count=lib.AT_GetEnumCount(self.handle,self.name)
            available=[i for i in range(count) if lib.AT_IsEnumIndexAvailable(self.handle,self.name,i)]
            if enum_as_str:
                available=[lib.AT_GetEnumStringByIndex(self.handle,self.name,i,512) for i in available]
            return available
    def _update_enum_limits(self):
        self.values=self.get_range()
        self.ivalues=self.get_range(enum_as_str=False)
        self.labels=dict(zip(self.values,self.ivalues))
        self.ilabels=dict(zip(self.ivalues,self.values))
    def update_limits(self):
        """Update minimal and maximal attribute limits and return tuple ``(min, max)``"""
        if self.kind in {"int","float"}:
            self.min,self.max=self.get_range()
            return (self.min,self.max)
        elif self.kind=="enum":
            self._update_enum_limits()
    def truncate_value(self, value):
        """Limit value to lie within the allowed range"""
        if self.kind in {"int","float"}:
            vmin,vmax=self.update_limits()
            value=min(max(value,vmin),vmax)
        return value


TDeviceInfo=collections.namedtuple("TDeviceInfo",["camera_name","camera_model","serial_number","firmware_version","software_version"])
TMissedFramesStatus=collections.namedtuple("TMissedFramesStatus",["skipped","overflows"])
TFrameInfo=collections.namedtuple("TFrameInfo",["frame_index","timestamp_dev","size","pixeltype","stride"])
class AndorSDK3Camera(camera.IBinROICamera, camera.IExposureCamera, camera.IAttributeCamera):
    """
    Andor SDK3 camera.

    Args:
        idx(int): camera index (use :func:`get_cameras_number` to get the total number of connected cameras)
    """
    Error=AndorError
    TimeoutError=AndorTimeoutError
    FrameTransferError=AndorFrameTransferError
    _TFrameInfo=TFrameInfo
    _frameinfo_fields=general.make_flat_namedtuple(TFrameInfo,fields={"size":camera.TFrameSize})._fields
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
        self._overflow_behavior="error"
        self._overflows_counter=0

        self._device_var_ignore_error={"get":(AndorNotSupportedError,),"set":(AndorNotSupportedError,)}
        self._add_info_variable("device_info",self.get_device_info)
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
        self._update_attributes()
        self._register_events()
        self.clear_acquisition()
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

    def _list_attributes(self):
        return [AndorSDK3Attribute(self.handle,v) for v in feature_types]
    def add_attribute(self, name, kind):
        """
        Add a new attribute which is not currently present in the dictionary.

        `kind` can be ``"float"``, ``"int"``, ``"str"``, ``"bool"``, ``"enum"``, or ``"comm"`` (command).
        """
        self.attributes[name]=AndorSDK3Attribute(self.handle,name,kind=kind)
    def get_attribute(self, name, update_properties=False, error_on_missing=True):  # pylint: disable=arguments-differ, arguments-renamed
        """
        Get the camera attribute with the given name.
        
        If ``update_properties==True``, automatically update all attribute properties.
        """
        att=super().get_attribute(name,error_on_missing=error_on_missing)
        if att is not None and update_properties:
            att.update_properties()
        return att
    def get_attribute_value(self, name, enum_as_str=True, update_properties=False, error_on_missing=True, default=None):  # pylint: disable=arguments-differ, arguments-renamed
        """
        Get value of an attribute with the given name.
        
        If ``update_properties==True``, automatically update all attribute properties before settings.
        If the value doesn't exist or can not be read and ``error_on_missing==True``, raise error; otherwise, return `default`.
        If `default` is not ``None``, assume that ``error_on_missing==False``.
        """
        error_on_missing=error_on_missing and (default is None)
        attr=self.get_attribute(name,update_properties=update_properties,error_on_missing=error_on_missing)
        return default if attr is None else attr.get_value(not_implemented_error=error_on_missing,enum_as_str=enum_as_str,default=default)
    def set_attribute_value(self, name, value, update_properties=True, error_on_missing=True):  # pylint: disable=arguments-differ, arguments-renamed
        """
        Set value of an attribute with the given name.
        
        If the value doesn't exist or can not be written and ``error_on_missing==True``, raise error; otherwise, do nothing.
        If ``update_properties==True``, automatically update all attribute properties before settings.
        """
        attr=self.get_attribute(name,update_properties=update_properties,error_on_missing=error_on_missing)
        if attr is not None:
            attr.set_value(value,not_implemented_error=error_on_missing)
    def get_all_attribute_values(self, root="", enum_as_str=True, update_properties=False):  # pylint: disable=arguments-differ, arguments-renamed, unused-argument
        """
        Get values of all attributes.
        
        If ``update_properties==True``, automatically update all attribute properties before settings.
        """
        values=dictionary.Dictionary()
        for n,att in self.attributes.as_dict("flat").items():
            if update_properties:
                att.update_properties()
            if att.readable:
                try:
                    values[n]=att.get_value(enum_as_str=enum_as_str)
                except AndorSDK3LibError:  # sometimes nominally implemented features still raise errors
                    pass
        return values
    def set_all_attribute_values(self, settings, update_properties=True):  # pylint: disable=arguments-differ, arguments-renamed
        """
        Set values of all attribute in the given dictionary.
        
        If ``update_properties==True``, automatically update all attribute properties before settings.
        """
        settings=dictionary.as_dict(settings,style="flat",copy=False)
        for k,v in settings.items():
            k=self._normalize_attribute_name(k)
            attr=self.get_attribute(k,update_properties=update_properties,error_on_missing=False)
            if attr is not None and attr.writable:
                attr.set_value(v)

    def _get_feature(self, name, writable=False):
        """
        Check if the feature is available and return the corresponding attribute.

        If ``writable==True``, also check if it's writable.
        """
        if name in self.attributes:
            attr=self.attributes[name]
            attr.update_properties()
            if attr.implemented and (attr.writable or not writable):
                return attr
        raise AndorNotSupportedError("feature {} is not supported by camera {}".format(name,self.get_device_info().camera_model))

    def call_command(self, name):
        """Execute the given command"""
        self._get_feature(name).call_command()


    def get_device_info(self):
        """
        Get camera info.

        Return tuple ``(camera_name, camera_model, serial_number, firmware_version, software_version)``.
        """
        camera_name=self.cav["CameraName"]
        camera_model=self.cav["CameraModel"]
        serial_number=self.cav["SerialNumber"]
        firmware_version=self.cav["FirmwareVersion"]
        strlen=lib.AT_GetStringMaxLength(1,"SoftwareVersion")
        software_version=lib.AT_GetString(1,"SoftwareVersion",strlen)
        return TDeviceInfo(camera_name,camera_model,serial_number,firmware_version,software_version)
        

    _p_trigger_mode=interface.EnumParameterClass("trigger_mode",
        {"int":"Internal","ext":"External","software":"Software","ext_start":"External Start","ext_exp":"External Exposure"})
    @interface.use_parameters(_returns="trigger_mode")
    def get_trigger_mode(self):
        """
        Get trigger mode.

        Can be ``"int"`` (internal), ``"ext"`` (external), ``"software"`` (software trigger),
            ``"ext_start"`` (external start), or ``"ext_exp"`` (external exposure).
        """
        return self.cav["TriggerMode"]
    @camera.acqstopped
    @interface.use_parameters(mode="trigger_mode")
    def set_trigger_mode(self, mode):
        """
        Set trigger mode.

        Can be ``"int"`` (internal), ``"ext"`` (external), or ``"software"`` (software trigger).
        """
        self.cav["TriggerMode"]=mode
        return self.get_trigger_mode()

    _p_shutter_mode=interface.EnumParameterClass("shutter_mode",{"open":"Open","closed":"Closed","auto":"Auto"})
    @interface.use_parameters(_returns="shutter_mode")
    def get_shutter(self):
        """Get current shutter mode"""
        return self._get_feature("ShutterMode").get_value()
    @interface.use_parameters(mode="shutter_mode")
    def set_shutter(self, mode):
        """
        Set trigger mode.

        Can be ``"open"``, ``"closed"``, or ``"auto"``.
        """
        self._get_feature("ShutterMode").set_value(mode)
        return self.get_shutter()

    def is_cooler_on(self):
        """Check if the cooler is on"""
        return self._get_feature("SensorCooling").get_value()
    @camera.acqstopped
    def set_cooler(self, on=True):
        """Set the cooler on or off"""
        self._get_feature("SensorCooling").set_value(on)
        return self.is_cooler_on()

    def get_temperature(self):
        """Get the current camera temperature"""
        return self._get_feature("SensorTemperature").get_value()
    def get_temperature_setpoint(self):
        """Get current temperature setpoint"""
        return self._get_feature("TargetSensorTemperature").get_value()
    @camera.acqstopped
    def set_temperature(self, temperature, enable_cooler=True):
        """
        Change the temperature setpoint.

        If ``enable_cooler==True``, turn the cooler on automatically.
        """
        p_target=self._get_feature("TargetSensorTemperature")
        if p_target.get_value()!=temperature:
            p_target.set_value(temperature)
        if enable_cooler:
            self.set_cooler(True)
        return p_target.get_value()


    def get_exposure(self):
        """Get current exposure"""
        return self._get_feature("ExposureTime").get_value()
    def set_exposure(self, exposure):
        """Set camera exposure"""
        self.set_frame_period(0)
        p_exposure=self._get_feature("ExposureTime")
        exposure=p_exposure.truncate_value(exposure)
        p_exposure.set_value(exposure)
        return self.get_exposure()
    def get_frame_period(self):
        return 1./self.cav["FrameRate"]
    def set_frame_period(self, frame_period):
        """Set frame period (time between two consecutive frames in the internal trigger mode)"""
        p_frame_rate=self.get_attribute("FrameRate",update_properties=True,error_on_missing=False)
        if p_frame_rate is None or not p_frame_rate.writable:
            return
        ro_rng=1./p_frame_rate.max,1./p_frame_rate.min
        frame_period=max(min(frame_period,ro_rng[1]),ro_rng[0])
        self.cav["FrameRate"]=1./frame_period
        return self.get_frame_period()
    def get_frame_timings(self):
        return self._TAcqTimings(self.get_exposure(),self.get_frame_period())

    def is_metadata_enabled(self):
        """Check if the metadata enabled"""
        return self.get_attribute_value("MetadataEnable",error_on_missing=False,default=False)
    def enable_metadata(self, enable=True):
        """Enable or disable metadata streaming"""
        updated=self.get_attribute_value("MetadataEnable",error_on_missing=False,default=enable)!=enable
        if updated:
            with self.pausing_acquisition(clear=True):
                self.set_attribute_value("MetadataEnable",enable,error_on_missing=False)
        return self.is_metadata_enabled()
    
    ### Frame management ###
    class BufferManager:
        """
        Cython-based schedule loop manager.
        
        Runs the loop function and provides callback storage.
        """
        def __init__(self, cam):
            self.buffers=None
            self.hbuffers=None
            self.queued_buffers=0
            self.size=0
            self.overflow_detected=False
            self.cam=cam
            self._cnt_lock=threading.RLock()
            self._buffer_loop_thread=None
            self.evt=threading.Event()
            self.looping=ctypes.c_ulong(0)
            self.nread=ctypes.c_ulong(0)
        def allocate_buffers(self, nbuff, size, queued_buffers=None):
            """
            Allocate and queue buffers.

            `queued_buffers`` specifies number of allocated buffers to keep queued at a given time (by default, all of them)
            """
            with self._cnt_lock:
                self.deallocate_buffers()
                self.buffers=[ctypes.create_string_buffer(size) for _ in range(nbuff)]
                self.hbuffers=as_ctypes_array([ctypes.addressof(b) for b in self.buffers],ctypes.c_void_p)
                self.queued_buffers=queued_buffers if queued_buffers is not None else len(self.buffers)
                self.size=size
                for b in self.buffers[:self.queued_buffers]:
                    lib.AT_QueueBuffer(self.cam.handle,ctypes.cast(b,ctypes.POINTER(ctypes.c_uint8)),self.size)
        def deallocate_buffers(self):
            """Deallocated buffers (flushing should be done manually)"""
            with self._cnt_lock:
                if self.buffers:
                    self.stop_loop()
                    self.buffers=None
                    self.hbuffers=None
                    self.size=0
        def readn(self, idx, n, size=None, off=0):
            """Return `n` buffers starting from `idx`, taking `size` bytes from each"""
            if size is None:
                size=self.size
            data=np.empty((n,size),dtype="u1")
            copyframes(len(self.hbuffers),ctypes.addressof(self.hbuffers),int(size),idx%len(self.hbuffers),n,off,data.ctypes.data)
            return data
        def reset(self):
            """Reset counter (on frame acquisition)"""
            self.nread.value=0
            self.overflow_detected=False
        def start_loop(self):
            """Start loop serving the given buffer manager"""
            self.stop_loop()
            self.evt.clear()
            self.looping.value=1
            self.nread.value=0
            self._buffer_loop_thread=threading.Thread(target=self._loop,daemon=True)
            self._buffer_loop_thread.start()
            self.evt.wait()
        def stop_loop(self):
            """Stop the loop thread"""
            if self._buffer_loop_thread is not None:
                self.looping.value=0
                self._buffer_loop_thread.join()
                self._buffer_loop_thread=None
        def _loop(self):
            self.evt.set()
            looper(self.cam.handle,len(self.hbuffers),ctypes.addressof(self.hbuffers),self.size,self.queued_buffers,
                    ctypes.addressof(self.looping),ctypes.addressof(self.nread),
                    funcaddressof(lib.lib.AT_WaitBuffer),funcaddressof(lib.lib.AT_QueueBuffer))
        def get_status(self):
            """Get the current loop status, which is the tuple ``(acquired,)``"""
            return (self.nread.value,)
        def on_overflow(self):
            """Process buffer overflow event"""
            with self._cnt_lock:
                self.overflow_detected=True
        def new_overflow(self):
            with self._cnt_lock:
                return self.overflow_detected
    def _register_events(self):
        self._unregister_events()
        if self.get_attribute_value("EventEnable",error_on_missing=False) is not None:
            self.cav["EventSelector"]="BufferOverflowEvent"
            self.cav["EventEnable"]=True
            buff_cb=lib.AT_RegisterFeatureCallback(self.handle,"BufferOverflowEvent",lambda *args: self._buffer_mgr.on_overflow())
            self._reg_cb=buff_cb
            self._buffer_mgr.reset()
    def _unregister_events(self):
        if self._reg_cb is not None:
            lib.AT_UnregisterFeatureCallback(self.handle,"BufferOverflowEvent",self._reg_cb)
            self.cav["EventSelector"]="BufferOverflowEvent"
            self.cav["EventEnable"]=False
            self._reg_cb=None
            self._buffer_mgr.reset()
    def _allocate_buffers(self, nframes):
        """
        Create and set up a new ring buffer.

        If a ring buffer is already allocated, remove it and create a new one.
        """
        self._deallocate_buffers()
        frame_size=self.cav["ImageSizeBytes"]
        self._buffer_mgr.allocate_buffers(nframes+self._buffer_padding,frame_size,queued_buffers=nframes)
    def _deallocate_buffers(self):
        """Remove the ring buffer and clean up the memory"""
        lib.flush_buffers(self.handle)
        self._buffer_mgr.deallocate_buffers()


    @interface.use_parameters(mode="acq_mode")
    def setup_acquisition(self, mode="sequence", nframes=100):  # pylint: disable=arguments-differ
        """
        Setup acquisition.

        `mode` can be either ``"snap"`` (single frame or a fixed number of frames) or ``"sequence"`` (continuous acquisition).
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
            self.cav["CycleMode"]="Fixed"
            self.cav["FrameCount"]=nframes
        else:
            # self.cav["CycleMode"]="Continuous" # Zyla bug doesn't allow continuous mode with >1000 FPS
            self.cav["CycleMode"]="Fixed"
            p_frame_count=self.get_attribute("FrameCount",update_properties=True)
            p_frame_count.set_value(p_frame_count.max)
        self._allocate_buffers(nframes)
        self._frame_counter.reset(nframes)
        self._buffer_mgr.reset()
        self._buffer_mgr.start_loop()
        self.call_command("AcquisitionStart")
    def stop_acquisition(self):
        if self.cav["CameraAcquiring"]:
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
            self.call_command("AcquisitionStop")
            self._buffer_mgr.stop_loop()
    def acquisition_in_progress(self):
        return self.cav["CameraAcquiring"]
    


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

        Can be ``"error"`` (raise ``AndorFrameTransferError``), ``"restart"`` (restart the acquisition), or ``"ignore"`` (ignore the overflow, which will cause the wait to time out).
        """
        self._overflow_behavior=behavior

    def _get_data_dimensions_rc(self):
        return self.cav["AOIHeight"],self.cav["AOIWidth"]
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        return int(self.cav["SensorWidth"]),int(self.cav["SensorHeight"])
    def get_roi(self):
        """
        Get current ROI.

        Return tuple ``(hstart, hend, vstart, vend, hbin, vbin)``.
        """
        hbin=int(self.get_attribute_value("AOIHBin",default=1))
        vbin=int(self.get_attribute_value("AOIVBin",default=1))
        hstart=int(self.cav["AOILeft"])-1
        hend=hstart+int(self.cav["AOIWidth"])*hbin
        vstart=int(self.cav["AOITop"])-1
        vend=vstart+int(self.cav["AOIHeight"])*vbin
        return (hstart,hend,vstart,vend,hbin,vbin)
    @camera.acqcleared
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        """
        Set current ROI.

        By default, all non-supplied parameters take extreme values. Binning is the same for both axes.
        """
        hlim,vlim=self.get_roi_limits()
        hbin=min(max(hbin,1),hlim.maxbin)
        vbin=min(max(vbin,1),vlim.maxbin)
        self.cav["AOILeft"]=1
        self.cav["AOITop"]=1
        self.cav["AOIWidth"]=hlim.min
        self.cav["AOIHeight"]=vlim.min
        self.set_attribute_value("AOIHBin",hbin,error_on_missing=False)
        self.set_attribute_value("AOIVBin",vbin,error_on_missing=False)
        hbin=int(self.get_attribute_value("AOIHBin",default=1))
        vbin=int(self.get_attribute_value("AOIVBin",default=1))
        hlim,vlim=self.get_roi_limits(hbin=hbin,vbin=vbin)
        hstart,hend,_=self._truncate_roi_axis((hstart,hend,hbin),hlim)
        vstart,vend,_=self._truncate_roi_axis((vstart,vend,vbin),vlim)
        self.cav["AOIWidth"]=(hend-hstart)//hbin
        self.cav["AOIHeight"]=(vend-vstart)//vbin
        self.cav["AOILeft"]=hstart+1
        self.cav["AOITop"]=vstart+1
        return self.get_roi()
    def get_roi_limits(self, hbin=1, vbin=1):
        """
        Get the minimal and maximal ROI parameters.

        Return tuple ``(hlim, vlim)``, where each element is in turn a limit 5-tuple
        ``(min, max, pstep, sstep, maxbin)`` with, correspondingly, minimal and maximal size,
        position and size step, and the maximal binning.

        Note that the minimal ROI size depends on the current (not just supplied) binning settings.
        For more accurate results, is it only after setting up the binning.
        """
        wdet,hdet=self.get_detector_size()
        try:
            wmin=self._get_feature("AOIWidth").min or wdet
        except AndorNotSupportedError:
            wmin=wdet
        try:
            hmin=self._get_feature("AOIHeight").min or hdet
        except AndorNotSupportedError:
            hmin=hdet,hdet
        try:
            hbinmax=self._get_feature("AOIHBin").max or 1
        except AndorNotSupportedError:
            hbinmax=1
        try:
            vbinmax=self._get_feature("AOIVBin").max or 1
        except AndorNotSupportedError:
            vbinmax=1
        hlim=camera.TAxisROILimit(wmin*hbin,wdet,1,hbin,hbinmax)
        vlim=camera.TAxisROILimit(hmin*vbin,hdet,1,vbin,vbinmax)
        return hlim,vlim
    
    def _check_buffer_overflow(self):
        if self._buffer_mgr.new_overflow():
            self._overflows_counter+=1
            if self._overflow_behavior=="ignore":
                return False
            if self._overflow_behavior=="error":
                self.stop_acquisition()
                raise self.FrameTransferError("buffer overflow while waiting for a new frame")
            self.start_acquisition()
            return True
        return False
    def _wait_for_next_frame(self, timeout=20., idx=None):
        if self._check_buffer_overflow():
            raise AndorTimeoutError("buffer overflow while waiting for a new frame")
        super()._wait_for_next_frame(timeout=timeout,idx=idx)
    def _frame_info_to_namedtuple(self, info):
        return self._TFrameInfo(info[0],info[1],camera.TFrameSize(*info[2:4]),*info[4:])
    
    _support_chunks=True
    def _arrange_metadata(self, chunks, nframes):
        metadata=np.zeros((nframes,6),dtype="i8")-1
        if 1 in chunks:
            metadata[:,1]=chunks[1].view("i8")[:,0]
        if 7 in chunks:
            metadata[:,2]=chunks[7].view("<u2")[:,2]
            metadata[:,3]=chunks[7].view("<u2")[:,3]
            metadata[:,4]=chunks[7][:,2]
            metadata[:,5]=chunks[7].view("<u2")[:,0]
        return metadata
    def _read_frames_metadata(self, start, nframes):
        size=self._buffer_mgr.size
        chunks={}
        read_len=0
        cid=None
        while read_len<size:
            if size<read_len+8:
                raise AndorError("unexpected size of the last section: {}, larger than the required 8 header bytes".format(size-read_len))
            cid,clen=self._buffer_mgr.readn(start,1,8,off=size-read_len-8).view("<u4")[0]
            if read_len+clen+4>size:
                raise AndorError("unexpected section {} size: {}, larger than the remaining block size {}".format(cid,clen+4,size-read_len))
            chunks[cid]=self._buffer_mgr.readn(start,nframes,clen-4,off=size-read_len-4-clen).reshape((nframes,clen-4))
            read_len+=clen+4
        if 0 not in chunks:
            raise AndorError("missing image data")
        img=chunks.pop(0)
        return img,self._arrange_metadata(chunks,nframes)
    def _read_frames(self, rng, return_info=False):
        height,width=self._get_data_dimensions_rc()
        bpp=self.cav["BytesPerPixel"]
        stride=self.cav["AOIStride"]
        if bpp not in [1,1.5,2,4]:
            raise ValueError("unexpected pixel byte size: {}".format(bpp))
        if stride<int(np.ceil(bpp*width)):
            raise AndorError("unexpected stride: expected at least {}x{}={}, got {}".format(width,bpp,int(np.ceil(width*bpp)),stride))
        nframes=rng[1]-rng[0]
        if self.is_metadata_enabled() and return_info:
            img,metadata=self._read_frames_metadata(rng[0],nframes)
            exp_len=height*stride
            if img.shape[1]!=exp_len:
                if img.shaoe[1]<exp_len or img.shaoe[1]>exp_len+8+stride: # sometimes image size gets rounded to nearest 4/8/stride (CL) bytes
                    raise AndorError("unexpected image byte size: expected {}x{}={}, got {}".format(stride,height,exp_len,img.shaoe[1]))
                img=img[:,:exp_len]
            metadata[:,0]=np.arange(rng[0],rng[0]+nframes)
        else:
            img=self._buffer_mgr.readn(rng[0],nframes,size=height*stride)
            metadata=None
        if bpp==1.5:
            img=read_uint12(img.reshape(-1,stride),width=width).reshape((nframes,height,width))
        else:
            bpp=int(bpp)
            dtype="<u{}".format(bpp)
            if stride%bpp==0:
                img=img.view(dtype).reshape(nframes,height,-1)[:,:width]
            else: # only possible with bpp==2 or 4 and non-divisible stride
                img=img.reshape((nframes,height,stride))[:,:,:width*bpp].view(dtype)
        img=self._convert_indexing(img,"rct",axes=(-2,-1))
        return [img],([metadata] if metadata is not None else None)
    def _zero_frame(self, n):
        dim=self.get_data_dimensions()
        bpp=self.cav["BytesPerPixel"]
        dt="<u{}".format(int(np.ceil(bpp))) # can be fractional (e.g., 1.5)
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
        describing frame index and frame metadata, which contains timestamp, image size, pixel format, and row stride;
        if some frames are missing and ``missing_frame!="skip"``, the corresponding frame info is ``None``.
        if ``return_rng==True``, return the range covered resulting frames; if ``missing_frame=="skip"``, the range can be smaller
        than the supplied `rng` if some frames are skipped.
        """
        return super().read_multiple_images(rng=rng,peek=peek,missing_frame=missing_frame,return_info=return_info,return_rng=return_rng)