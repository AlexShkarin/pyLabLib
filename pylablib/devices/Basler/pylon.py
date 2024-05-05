from pylablib.core.utils import funcargparse
from . import pylonC_lib
from .pylonC_lib import EGenApiNodeType, EGenApiAccessMode, EGenApiRepresentation, EGenApiVisibility, EGenApiNameSpace, PYLONC_ACCESS  # pylint: disable=unused-import
from .pylonC_lib import wlib as lib, BaslerError, BaslerLibError  # pylint: disable=unused-import

from ...core.utils import py3, dictionary
from ...core.devio import interface
from ..interface import camera
from ..utils import load_lib
from ...core.utils.ctypes_tools import funcaddressof, as_ctypes_array
from ...core.utils.cext_tools import try_import_cext
with try_import_cext():
    from .utils import looper  # pylint: disable=no-name-in-module

import numpy as np
import collections
import ctypes
import threading


class BaslerTimeoutError(BaslerError):
    "Basler frame timeout error"


class LibraryController(load_lib.LibraryController):
    def _do_init(self):
        lib.PylonInitialize()
    def _do_uninit(self):
        lib.PylonTerminate()
libctl=LibraryController(lib)
def restart_lib():
    libctl.shutdown()





_camera_info_alias={"FullName":"name", "ModelName":"model", "SerialNumber":"serial", "DeviceClass":"devclass", "DeviceVersion":"devversion",
    "VendorName":"vendor","FriendlyName":"friendly_name", "UserDefinedName":"user_name"}
TCameraInfo=collections.namedtuple("TCameraInfo",["name","model","serial","devclass","devversion","vendor","friendly_name","user_name","props"])
def _parse_device_info(info, info_handle=None):
    cam_info={"props":{}}
    for n,a in _camera_info_alias.items():
        cam_info[a]=py3.as_str(getattr(info,n))
    if info_handle is not None:
        nprop=lib.PylonDeviceInfoGetNumProperties(info_handle)
        for i in range(nprop):
            pname=py3.as_str(lib.PylonDeviceInfoGetPropertyName(info_handle,i))
            pval=py3.as_str(lib.PylonDeviceInfoGetPropertyValueByIndex(info_handle,i))
            if pname in _camera_info_alias:
                iname=_camera_info_alias[pname]
                if not cam_info[iname]:
                    cam_info[iname]=pval
            else:
                cam_info["props"][pname]=pval
    return TCameraInfo(**cam_info)
def get_device_info(index):
    """Get Pylon camera info for a camera with the given index"""
    info=lib.PylonGetDeviceInfo(index)
    info_handle=lib.PylonGetDeviceInfoHandle(index)
    return _parse_device_info(info,info_handle=info_handle)
def list_cameras(desc=True):
    """
    List all cameras available through Basler Pylon interface
    
    If ``desc==True``, return complete camera descriptions; otherwise, simply return the names.
    """
    with libctl.temp_open():
        ndev=lib.PylonEnumerateDevices()
        infos=[get_device_info(i) for i in range(ndev)]
        return infos if desc else [inf.name for inf in infos]
def _find_camera(cameras, **kwargs):
    for i,c in enumerate(cameras):
        match=True
        for k,v in kwargs.items():
            if getattr(c,k)!=v:
                match=False
                break
        if match:
            return i
    return None

def get_cameras_number():
    """Get number of connected Basler Pylon cameras"""
    return len(list_cameras(desc=False))




class BaslerPylonAttribute:
    """
    Object representing an Pylon GenAPI attribute.

    Allows to query and set values and get additional information.
    Usually created automatically by an :class:`BaslerPylonCamera` instance.

    Args:
        node: pylon GenApi node handler
        full_name: if supplied, attribute's full name, including the tree structure

    Attributes:
        name: attribute name
        kind: attribute kind; can be ``"int"``, ``"float"``, ``"bool"``, ``"enum"``, ``"str"``, 
            ``"command"``, ``"category"``, or ``"unknown"``
        display_name: attribute display name (short description name)
        tooltip: longer attribute description
        description: full attribute description (usually, same as `tooltip`)
        visibility: attribute visibility; can be ``"simple"``, ``"intermediate"``, ``"advanced"``, ``"invisible"``, or ``"unknown"``
        access: attribute access level; can be ``"read_only"``, ``"write_only"``, ``"read_write"``,
            ``"na"`` (not applicable, e.g., command), or ``"not_implemented"``
        readable (bool): whether attribute is readable
        writable (bool): whether attribute is writable
        implemented (bool): whether the attribute is implemented in the given camera (normally always ``True``)
        available (bool): whether the attribute can be changed or called
        min (float or int): minimal attribute value (if applicable)
        max (float or int): maximal attribute value (if applicable)
        inc (float or int): minimal attribute increment value (if applicable)
        units: attribute units (if applicable)
        repr: shows what a numerical unit represents; can be ``"lin"``, ``"log"``, ``"bool"``, ``"pure"``, ``"hex"``, or ``"unknown"``
        ivalues: list of possible integer values for enum attributes
        values: list of possible text values for enum attributes
        labels: dict ``{label: index}`` which shows all possible values of an enumerated attribute and their corresponding numerical values
        ilabels: dict ``{index: label}`` which shows labels corresponding to numerical values of an enumerated attribute
    """
    _attr_types={   EGenApiNodeType.IntegerNode:"int",
                    EGenApiNodeType.FloatNode:"float",
                    EGenApiNodeType.BooleanNode:"bool",
                    EGenApiNodeType.EnumerationNode:"enum",
                    EGenApiNodeType.StringNode:"str",
                    EGenApiNodeType.CommandNode:"command",
                    EGenApiNodeType.Category:"category",
                    EGenApiNodeType._UnknownNodeType:"unknown"}
    _vis_types={    EGenApiVisibility.Beginner:"simple",
                    EGenApiVisibility.Expert:"intermediate",
                    EGenApiVisibility.Guru:"advanced",
                    EGenApiVisibility.Invisible:"invisible",
                    EGenApiVisibility._UndefinedVisibility:"unknown"}
    _acc_types={    EGenApiAccessMode.RO:"read_only",
                    EGenApiAccessMode.WO:"write_only",
                    EGenApiAccessMode.RW:"read_write",
                    EGenApiAccessMode.NA:"na",
                    EGenApiAccessMode.NI:"not_implemented",
                    EGenApiAccessMode._UndefinedAccesMode:"unknown"}
    _repr_type={    EGenApiRepresentation.Linear:"lin",
                    EGenApiRepresentation.Logarithmic:"log",
                    EGenApiRepresentation.Boolean:"bool",
                    EGenApiRepresentation.PureNumber:"pure",
                    EGenApiRepresentation.HexNumber:"hex",
                    EGenApiRepresentation._UndefinedRepresentation:"unknown"}
    def __init__(self, node, full_name=None):
        self.node=node
        self.name=py3.as_str(lib.GenApiNodeGetName(node))
        self.full_name=full_name or self.name
        self.kind=self._attr_types[lib.GenApiNodeGetType(node)]
        self.display_name=py3.as_str(lib.GenApiNodeGetDisplayName(node))
        self.tooltip=py3.as_str(lib.GenApiNodeGetToolTip(node))
        self.description=py3.as_str(lib.GenApiNodeGetDescription(node))
        self.visibility=self._vis_types[lib.GenApiNodeGetVisibility(node)]
        self.access=self._acc_types[lib.GenApiNodeGetAccessMode(node)]
        self.implemented=bool(lib.GenApiNodeIsImplemented(node))
        self.available=bool(lib.GenApiNodeIsAvailable(node))
        self.readable=bool(lib.GenApiNodeIsReadable(node))
        self.writable=bool(lib.GenApiNodeIsWritable(node))
        self.units=None
        self.min=None
        self.max=None
        self.inc=None
        self.repr=None
        self._value_nodes=None
        self.values=[]
        self.ivalues=[]
        self.labels={}
        self.ilabels={}
        self._fill_info()
    
    def _fill_info(self):
        if self.kind=="int":
            self.repr=self._repr_type[lib.GenApiIntegerGetRepresentation(self.node)]
        elif self.kind=="float":
            self.repr=self._repr_type[lib.GenApiFloatGetRepresentation(self.node)]
            self.units=py3.as_str(lib.GenApiFloatGetUnit(self.node))
        elif self.kind=="enum":
            nenum=lib.GenApiEnumerationGetNumEntries(self.node)
            self._value_nodes=[lib.GenApiEnumerationGetEntryByIndex(self.node,i) for i in range(nenum)]
        self.update_limits()
    def update_limits(self):
        """Update minimal and maximal attribute limits and return tuple ``(min, max, inc)``"""
        if self.kind=="int":
            self.min=lib.GenApiIntegerGetMin(self.node)
            self.max=lib.GenApiIntegerGetMax(self.node)
            self.inc=lib.GenApiIntegerGetInc(self.node)
            return (self.min,self.max,self.inc)
        elif self.kind=="float":
            self.min=lib.GenApiFloatGetMin(self.node)
            self.max=lib.GenApiFloatGetMax(self.node)
            return (self.min,self.max,self.inc)
        elif self.kind=="enum":
            self.values=[py3.as_str(lib.GenApiEnumerationEntryGetSymbolic(n)) for n in self._value_nodes]
            self.ivalues=[lib.GenApiEnumerationEntryGetValue(n) for n in self._value_nodes]
            self.labels=dict(zip(self.values,self.ivalues))
            self.ilabels=dict(zip(self.ivalues,self.values))
    def truncate_value(self, value):
        """Truncate value to lie within attribute limits"""
        self.update_limits()
        if self.kind in ["int","float"]:
            if value<self.min:
                value=self.min
            elif value>self.max:
                value=self.max
            else:
                if self.inc and self.inc>0:
                    value=((value-self.min)//self.inc)*self.inc+self.min
        return value

    def get_value(self, enum_as_str=True):
        """
        Get attribute value.
        
        If ``enum_as_str==True``, return enum-style values as strings; otherwise, return corresponding integer values.
        """
        if self.kind=="command":
            return bool(lib.GenApiCommandIsDone(self.node))
        if not self.readable:
            raise BaslerError("attribute {} is not readable".format(self.name))
        if self.kind=="int":
            return lib.GenApiIntegerGetValue(self.node)
        if self.kind=="float":
            return lib.GenApiFloatGetValue(self.node)
        if self.kind=="bool":
            return lib.GenApiBooleanGetValue(self.node)
        if self.kind=="str":
            return py3.as_str(lib.GenApiNodeToString(self.node))
        if self.kind=="enum":
            value=py3.as_str(lib.GenApiNodeToString(self.node))
            if not enum_as_str:
                value=self.labels[value]
            return value
        if self.kind=="unknown":
            return None
        raise BaslerError("attribute {} of kind {} can not be read".format(self.name,self.kind))
    def set_value(self, value, truncate=True):
        """
        Set attribute value.
        
        If ``truncate==True``, automatically truncate value to lie within allowed range.
        """
        if not self.writable:
            raise BaslerError("attribute {} is not writable".format(self.name))
        if truncate:
            value=self.truncate_value(value)
        if self.kind=="int":
            lib.GenApiIntegerSetValue(self.node,int(value))
        elif self.kind=="float":
            lib.GenApiFloatSetValue(self.node,float(value))
        elif self.kind=="bool":
            lib.GenApiBooleanSetValue(self.node,bool(value))
        elif self.kind=="str":
            lib.GenApiNodeFromString(self.node,str(value))
        elif self.kind=="enum":
            value=self.ilabels.get(value,value)
            lib.GenApiNodeFromString(self.node,str(value))
        elif self.kind!="unknown":
            raise BaslerError("attribute {} of kind {} can not be set".format(self.name,self.kind))
    def call_command(self):
        """Execute the given command"""
        if self.kind=="command":
            if not self.implemented:
                raise BaslerError("command is not implemented: {}".format(self.name))
            lib.GenApiCommandExecute(self.node)
        else:
            raise BaslerError("attribute {} is not a command".format(self.name))

    def __repr__(self):
        return "{}(name='{}', kind='{}')".format(self.__class__.__name__,self.name,self.kind)




TDeviceInfo=collections.namedtuple("TDeviceInfo",TCameraInfo._fields)
class BaslerPylonCamera(camera.IROICamera, camera.IAttributeCamera, camera.IExposureCamera):
    """
    Generic Basler pylon camera interface.

    Args:
        idx: camera index among the cameras listed using :func:`list_cameras`
        name: camera name; if specified, then `idx` is ignored and the camera is determined based on the provided name
    """
    Error=BaslerError
    TimeoutError=BaslerTimeoutError
    def __init__(self, idx=0, name=None):
        super().__init__()
        lib.initlib()
        self.idx=idx
        self.name=name
        self.hdev=None
        self.strm=None
        self._buffer_mgr=None
        self._looper=self.ScheduleLooper()
        self.open()
        self._raw_readout_format=False
        self._add_info_variable("device_info",self.get_device_info)
        self._add_settings_variable("exposure",self.get_exposure,self.set_exposure,ignore_error=BaslerError)
        self._update_device_variable_order("exposure")
        self._add_settings_variable("frame_period",self.get_frame_period,self.set_frame_period,ignore_error=BaslerError)


    def _get_connection_parameters(self):
        return (self.idx,self.name)
    def open(self):
        """Open connection to the camera"""
        if self.hdev is not None:
            return
        with libctl.temp_open():
            cams=list_cameras()
            if self.name is not None:
                idx=_find_camera(cams,name=self.name)
                if idx is None:
                    names=", ".join(["'{}'".format(c.name) for c in cams])
                    raise BaslerError("could not find camera with name {}; available cameras are {}".format(self.name,names))
            else:
                idx=self.idx
            if idx>=len(cams):
                raise BaslerError("camera index {} is not available ({} cameras exist)".format(idx,len(cams)))
            with self._close_on_error():
                self.hdev=lib.PylonCreateDeviceByIndex(idx)
                lib.PylonDeviceOpen(self.hdev,PYLONC_ACCESS.PYLONC_ACCESS_MODE_MONITOR|PYLONC_ACCESS.PYLONC_ACCESS_MODE_CONTROL|PYLONC_ACCESS.PYLONC_ACCESS_MODE_STREAM)
                self.strm=lib.PylonDeviceGetStreamGrabber(self.hdev,0)
                self._opid=libctl.open().opid
                self._update_attributes()
                self.post_open()
    def close(self):
        """Close connection to the camera"""
        if self.hdev is not None:
            try:
                self.clear_acquisition()
            finally:
                try:
                    lib.PylonDeviceClose(self.hdev)
                    lib.PylonDestroyDevice(self.hdev)
                finally:
                    self.hdev=None
                    libctl.close(self._opid)
                    self._opid=None
    def is_opened(self):
        return (self.hdev is not None) and bool(lib.PylonDeviceIsOpen(self.hdev))

    def post_open(self):
        """Additional setup after camera opening"""

    _builtin_attrs=["OffsetX","OffsetY","Width","Height","PixelFormat","PayloadSize","AcquisitionStart","AcquisitionStop"]
    def _list_attributes(self):
        nmap=lib.PylonDeviceGetNodeMap(self.hdev)
        root=lib.GenApiNodeMapGetNode(nmap,"Root")
        nodes=lib.collect_nodes(root,add_branch=False)
        nodes={(n[5:] if n.startswith("Root/") else n):v for n,v in nodes.items()}
        attrs=[BaslerPylonAttribute(node,full_name=n) for n,node in nodes.items()]
        for n in self._builtin_attrs:
            node=lib.GenApiNodeMapGetNode(nmap,n)
            if node:
                attrs.append(BaslerPylonAttribute(node,full_name=n))
        return attrs

    def get_attribute_value(self, name, error_on_missing=True, default=None, enum_as_str=True):  # pylint: disable=arguments-differ
        """
        Get value of an attribute with the given name.
        
        If the value doesn't exist or can not be read and ``error_on_missing==True``, raise error; otherwise, return `default`.
        If `default` is not ``None``, assume that ``error_on_missing==False``.
        If `name` points at a dictionary branch, return a dictionary with all values in this branch.
        If ``enum_as_str==True``, return enum-style values as strings; otherwise, return corresponding integer values.
        """
        return super().get_attribute_value(name,error_on_missing=error_on_missing,default=default,enum_as_str=enum_as_str)
    def set_attribute_value(self, name, value, truncate=True, error_on_missing=True):  # pylint: disable=arguments-differ, arguments-renamed
        """
        Set value of an attribute with the given name.
        
        If the value doesn't exist or can not be written and ``error_on_missing==True``, raise error; otherwise, do nothing.
        If `name` points at a dictionary branch, set all values in this branch (in this case `value` must be a dictionary).
        If ``truncate==True``, truncate value to lie within attribute range.
        """
        return super().set_attribute_value(name,value,truncate=truncate,error_on_missing=error_on_missing)
    def call_command(self, name):
        """Execute the given command"""
        self.ca[name].call_command()
    def get_all_attribute_values(self, root="", enum_as_str=True, ignore_errors=True):  # pylint: disable=arguments-differ
        """Get values of all attributes with the given `root`"""
        values=dictionary.Dictionary()
        for n,att in self.get_attribute(root).as_dict("flat").items():
            if att.readable:
                try:
                    values[n]=att.get_value(enum_as_str=enum_as_str)
                except BaslerError:  # sometimes nominally implemented features still raise errors
                    if not ignore_errors:
                        raise
        return values
    def set_all_attribute_values(self, settings, root="", truncate=True):  # pylint: disable=arguments-differ
        """
        Set values of all attributes with the given `root`.
        
        If ``truncate==True``, truncate value to lie within attribute range.
        """
        return super().set_all_attribute_values(settings,root=root,truncate=truncate)

    def get_device_info(self):
        """
        Get camera information.

        Return tuple ``(name, model, serial, devclass, devversion, vendor, friendly_name, user_name, props)``.
        """
        info=lib.PylonDeviceGetDeviceInfo(self.hdev)
        info_handle=lib.PylonDeviceGetDeviceInfoHandle(self.hdev)
        return TCameraInfo(*_parse_device_info(info,info_handle))

    def _get_data_dimensions_rc(self):
        return self.cav["Height"],self.cav["Width"]
    def get_detector_size(self):
        return self.ca["Width"].max,self.ca["Height"].max
    def get_roi(self):
        ox=self.get_attribute_value("OffsetX",default=0)
        oy=self.get_attribute_value("OffsetY",default=0)
        w=self.cav["Width"]
        h=self.cav["Height"]
        return ox,ox+w,oy,oy+h
    @camera.acqcleared
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None):
        for a in ["Width","Height","OffsetX","OffsetY"]:
            if a not in self.ca or not self.ca[a].writable:
                return self.get_roi()
        det_size=self.get_detector_size()
        if hend is None:
            hend=det_size[0]
        if vend is None:
            vend=det_size[1]
        with self.pausing_acquisition():
            self.cav["Width"]=self.ca["Width"].min
            self.cav["Height"]=self.ca["Height"].min
            self.cav["OffsetX"]=hstart
            self.cav["OffsetY"]=vstart
            self.cav["Width"]=max(self.cav["Width"],hend-hstart)
            self.cav["Height"]=max(self.cav["Height"],vend-vstart)
        return self.get_roi()
    def get_roi_limits(self, hbin=1, vbin=1):
        params=["Width","Height","OffsetX","OffsetY"]
        minp=tuple([(self.ca[p].min if p in self.ca else 0) for p in params])
        maxp=tuple([(self.ca[p].max if p in self.ca else 0) for p in params])
        incp=tuple([(self.ca[p].inc if p in self.ca else 0) for p in params])
        hlim=camera.TAxisROILimit(minp[0] or maxp[0],maxp[0],incp[2] or maxp[0],incp[0] or maxp[0],1)
        vlim=camera.TAxisROILimit(minp[1] or maxp[1],maxp[1],incp[3] or maxp[1],incp[1] or maxp[1],1)
        return hlim,vlim

    _exposure_time_properties=["ExposureTimeAbs","ExposureTime"]
    def get_exposure(self):
        for p in self._exposure_time_properties:
            exp=self.get_attribute_value(p,error_on_missing=False)
            if exp is not None:
                return exp/1E6  # in us by default
        bexp=self.get_attribute_value("ExposureTimeBaseAbs",error_on_missing=False)
        rexp=self.get_attribute_value("ExposureTimeRaw",error_on_missing=False)
        if bexp is not None and rexp is not None:
            return bexp*rexp/1E6
        raise BaslerError("camera does not support exposure")
    def set_exposure(self, exposure):
        for p in self._exposure_time_properties:
            if p in self.attributes:
                self.cav[p]=exposure*1E6
                return self.get_exposure()
        if "ExposureTimeBaseAbs" in self.attributes and "ExposureTimeRaw" in self.attributes:
            self.cav["ExposureTimeRaw"]=(exposure/self.cav["ExposureTimeBaseAbs"])*1E6
        else:
            raise BaslerError("camera does not support exposure")
        return self.get_exposure()
    def get_frame_period(self):
        fps_ena=self.get_attribute_value("AcquisitionFrameRateEnable",error_on_missing=False)
        fps=self.get_attribute_value("AcquisitionFrameRateAbs",error_on_missing=False)
        if fps is not None:
            period=1./fps if (fps_ena or fps_ena is None) else 0
            try:
                exposure=self.get_exposure()
                return max(exposure,period)
            except BaslerError:
                return period
        try:
            return self.get_exposure()
        except BaslerError:
            raise BaslerError("camera does not support frame period")
    def set_frame_period(self, frame_period):
        """Set frame period (time between two consecutive frames in the internal trigger mode)"""
        if "AcquisitionFrameRateAbs" in self.attributes:
            self.cav["AcquisitionFrameRateAbs"]=1./frame_period if frame_period>0 else self.attributes["AcquisitionFrameRateAbs"].max
            if "AcquisitionFrameRateEnable" in self.attributes:
                self.cav["AcquisitionFrameRateEnable"]=frame_period>0
        else:
            raise BaslerError("camera does not support frame period")
        return self.get_frame_period()
    def get_frame_timings(self):
        return self._TAcqTimings(self.get_exposure(),self.get_frame_period())

    class BufferManager:
        """Buffer manager, which deals with buffer memory allocation, registering and deregistering, and retrieving the result and the leftovers"""
        def __init__(self, strm, size, nbuff):
            self.strm=strm
            self.size=size
            self.nbuff=nbuff
            self._full_buffer=ctypes.create_string_buffer(self.size*nbuff)
            buff_ptr=ctypes.addressof(self._full_buffer)
            self._buffers=[buff_ptr+self.size*i for i in range(nbuff)]
            self._handles=None
            self._ret_rdy=ctypes.c_ubyte()
            self._ret_val=pylonC_lib.PylonGrabResult_t()
        def register(self):
            """Register buffers"""
            self.deregister()
            self._handles=[lib.PylonStreamGrabberRegisterBuffer(self.strm,b,self.size) for b in self._buffers]
        def deregister(self):
            """Deregister buffers"""
            if self._handles:
                for h in self._handles:
                    lib.PylonStreamGrabberDeregisterBuffer(self.strm,h)
                self._handles=None
        def get_buffer(self, fidx):
            """Get buffer corresponding to the given frame index"""
            return self._buffers[fidx%self.nbuff]
        def get_handle(self, fidx):
            """Get buffer handle corresponding to the given frame index"""
            return self._handles[fidx%self.nbuff]
        def get_all_handles(self):
            """Get all buffer handles as a ctypes array"""
            return as_ctypes_array(self._handles,ctypes.c_void_p)
        def queue(self, fidx=None):
            """Queue a buffer with the given index or all buffers"""
            if fidx is None:
                for h in self._handles:
                    lib.PylonStreamGrabberQueueBuffer(self.strm,h,None)
            else:
                lib.PylonStreamGrabberQueueBuffer(self.strm,self._handles[fidx%self.nbuff],None)
        def retrieve(self):
            """Retrieve the next buffer and return its info and whether it is ready"""
            return lib.PylonStreamGrabberRetrieveResult(self.strm)
        def flush(self):
            """Retrieve all leftover buffers"""
            while True:
                _,rdy=self.retrieve()
                if not rdy:
                    break
    
    class ScheduleLooper:
        """
        Cython-based schedule loop manager.
        
        Runs the loop function and provides callback storage.
        """
        def __init__(self):
            self.evt=threading.Event()
            self._thread=None
            self.looping=ctypes.c_ulong(0)
            self.nread=ctypes.c_ulong(0)
            self._buff_mgr=None
        def start_loop(self, buff_mgr):
            """Start loop serving the given buffer manager"""
            self.stop_loop()
            self.evt.clear()
            self.looping.value=1
            self.nread.value=0
            self._buff_mgr=buff_mgr
            self._thread=threading.Thread(target=self._loop,daemon=True)
            self._thread.start()
            self.evt.wait()
        def stop_loop(self):
            """Stop the loop thread"""
            if self._thread is not None:
                self.looping.value=0
                self._thread.join()
                self._thread=None
                self._buff_mgr=None
        def _loop(self):
            self.evt.set()
            hbuffers=self._buff_mgr.get_all_handles()
            nbuff=len(hbuffers)
            strm=self._buff_mgr.strm
            wtobj=lib.PylonStreamGrabberGetWaitObject(strm)
            looper(strm.value,wtobj.value,nbuff,ctypes.addressof(hbuffers),
                    ctypes.addressof(self.looping),ctypes.addressof(self.nread),
                    funcaddressof(lib.lib.PylonStreamGrabberRetrieveResult),funcaddressof(lib.lib.PylonStreamGrabberQueueBuffer),funcaddressof(lib.lib.PylonWaitObjectWait))
        def is_looping(self):
            """Check if the loop is running"""
            return self.looping.value
        def get_status(self):
            """Get the current loop status, which is the tuple ``(acquired,)``"""
            return (self.nread.value,)

    def _allocate_buffers(self, nbuff):
        self._deallocate_buffers()
        size=lib.PylonStreamGrabberGetPayloadSize(self.hdev,self.strm)
        nbuff=min(nbuff,2**30//size)
        self._buffer_mgr=self.BufferManager(self.strm,size,nbuff)
        lib.PylonStreamGrabberSetMaxBufferSize(self.strm,size)
        lib.PylonStreamGrabberSetMaxNumBuffer(self.strm,nbuff)
        return nbuff
    def _deallocate_buffers(self):
        if self._buffer_mgr is not None:
            self._buffer_mgr.deregister()
            self._buffer_mgr=None

    @interface.use_parameters(mode="acq_mode")
    def setup_acquisition(self, mode="sequence", nframes=100):  # pylint: disable=arguments-differ
        """
        Setup acquisition mode.

        `mode` can be either ``"snap"`` (single frame or a fixed number of frames) or ``"sequence"`` (continuous acquisition).
        `nframes` sets up number of frame buffers.
        """
        self.clear_acquisition()
        self.set_attribute_value("AcquisitionMode","Continuous",error_on_missing=False)
        lib.PylonStreamGrabberOpen(self.strm)
        nframes=self._allocate_buffers(nbuff=nframes)
        lib.PylonStreamGrabberPrepareGrab(self.strm)
        self._buffer_mgr.register()
        super().setup_acquisition(mode=mode,nframes=nframes)
    def clear_acquisition(self):
        self.stop_acquisition()
        if self._buffer_mgr is not None:
            self._deallocate_buffers()
            lib.PylonStreamGrabberFinishGrab(self.strm)
            lib.PylonStreamGrabberClose(self.strm)
        super().clear_acquisition()
    def start_acquisition(self, *args, **kwargs):
        self.stop_acquisition()
        super().start_acquisition(*args,**kwargs)
        self._frame_counter.reset(self._acq_params["nframes"])
        self._buffer_mgr.queue()
        lib.PylonStreamGrabberStartStreamingIfMandatory(self.strm)
        self._looper.start_loop(self._buffer_mgr)
        self.call_command("AcquisitionStart")
    def stop_acquisition(self):
        if self.acquisition_in_progress():
            self.call_command("AcquisitionStop")
            self._looper.stop_loop()
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
            lib.PylonStreamGrabberStopStreamingIfMandatory(self.strm)
            lib.PylonStreamGrabberFlushBuffersToOutput(self.strm)
            self._buffer_mgr.flush()
        super().stop_acquisition()
    def acquisition_in_progress(self):
        return self._looper.is_looping()
    def _get_acquired_frames(self):
        return self._looper.get_status()[0]

    def enable_raw_readout(self, enable="rows"):
        """
        Enable raw frame transfer.

        Should be used if the camera uses unsupported pixel format.
        Can be ``"frame"`` (return the whole frame as a 1D ``"u1"`` numpy array),
        ``"rows"`` (return a 2D array, where each row corresponds to a single image row),
        or ``False`` (convert to image data, or raise an error if the format is not supported; default)
        """
        funcargparse.check_parameter_range(enable,"enable",{False,"rows","frame"})
        self._raw_readout_format=enable

    def _parse_buffer(self, buff, size, shape, pixel_format, n=1):
        data=np.ctypeslib.as_array(ctypes.cast(buff,ctypes.POINTER(ctypes.c_ubyte)),shape=(n,size))
        if self._raw_readout_format=="frame":
            return data[:,None,:]
        if self._raw_readout_format=="rows":
            return data.reshape((n,shape[0],-1))
        supported_formats=["Mono8","Mono10","Mono12","Mono16","Mono32"]
        if pixel_format not in supported_formats:
            sf_string=", ".join(supported_formats)
            raise BaslerError("pixel format {} is not supported, only [{}] are supported; raw data readout can be enabled via enable_raw_readout method".format(pixel_format,sf_string))
        if pixel_format=="Mono8":
            return data.reshape((n,)+shape)
        elif pixel_format in ["Mono10","Mono12","Mono16"]:
            return data.view("<u2").reshape((n,)+shape)
        else:
            return data.view("<u4").reshape((n,)+shape)
    _support_chunks=True
    def _read_frames(self, rng, return_info=False):
        size=self._buffer_mgr.size
        shape=self.cav["Height"],self.cav["Width"]
        pixel_format=self.cav["PixelFormat"]
        nbuff=self._buffer_mgr.nbuff
        i0,i1=rng
        if (i1-1)//nbuff==i0//nbuff:
            chunks=[(i0,i1-i0)]
        else:
            cut=(i1//nbuff)*nbuff
            chunks=[(i0,cut-i0),(cut,i1-cut)]
        frames=[self._parse_buffer(self._buffer_mgr.get_buffer(b),size,shape,pixel_format,n=n) for b,n in chunks]
        if not self._raw_readout_format:
            frames=[self._convert_indexing(f,"rct",axes=(-2,-1)) for f in frames]
        return frames,None