from . import fgrab_prototyp_lib
from .fgrab_prototyp_defs import FgAppletIntProperty, FgAppletStringProperty, FgAppletIteratorSource, FgParamTypes, FgProperty, Fg_Info_Selector, drFg_Info_Selector
from .fgrab_prototyp_defs import MeCameraLinkFormat
from .fgrab_define_defs import FG_STATUS, FG_GETSTATUS, FG_ACQ, FG_IMGFMT, FG_PARAM
from .fgrab_prototyp_lib import wlib as lib, SiliconSoftwareError, SIFgrabLibError

from ...core.utils import py3, dictionary
from ...core.devio import interface
from ..interface import camera

import numpy as np
import collections
import ctypes
import struct




class SiliconSoftwareTimeoutError(SiliconSoftwareError):
    "Silicon Software frame timeout error"

# TODO: serial interface
# TODO: trigger

TBoardInfo=collections.namedtuple("TBoardInfo",["name","full_name"])
def get_board_info(board):
    """Get board info for a given index (starting from 0)"""
    bt=lib.Fg_getBoardType(board)
    return TBoardInfo(*[py3.as_str(lib.Fg_getBoardNameByType(bt,short)) for short in [1,0]])
def list_boards():
    """List all boards available through Silicon Software interface"""
    lib.initlib()
    boards=[]
    i=0
    try:
        while True:
            boards.append(get_board_info(i))
            i+=1
    except SIFgrabLibError as err:
        if err.code!=FG_STATUS.FG_INVALID_BOARD_NUMBER:
            raise
    return boards
def get_boards_number():
    """List number of connected Silicon Software boards"""
    return len(list_boards())

TAppletInfo=collections.namedtuple("TAppletInfo",["name","file"])
_applet_string_props={  "uid":FgAppletStringProperty.FG_AP_STRING_APPLET_UID,
                        "name":FgAppletStringProperty.FG_AP_STRING_APPLET_NAME,
                        "desc":FgAppletStringProperty.FG_AP_STRING_DESCRIPTION,
                        "category":FgAppletStringProperty.FG_AP_STRING_CATEGORY,
                        "platform":FgAppletStringProperty.FG_AP_STRING_SUPPORTED_PLATFORMS,
                        "tags":FgAppletStringProperty.FG_AP_STRING_TAGS,
                        "version":FgAppletStringProperty.FG_AP_STRING_VERSION,
                        "path":FgAppletStringProperty.FG_AP_STRING_APPLET_PATH,
                        "file":FgAppletStringProperty.FG_AP_STRING_APPLET_FILE,}
_applet_int_props={ "flags":FgAppletIntProperty.FG_AP_INT_FLAGS,
                    "info":FgAppletIntProperty.FG_AP_INT_INFO,}
TFullAppletInfo=collections.namedtuple("TFullAppletInfo",["name","uid","desc","category","platform","tags","version","path","file","flags","info"])
def _get_applet_item_info(item, full_desc=False):
    props=TFullAppletInfo._fields if full_desc else TAppletInfo._fields
    values=[]
    for p in props:
        if p in _applet_string_props:
            values.append(py3.as_str(lib.Fg_getAppletStringProperty(item,_applet_string_props[p])))
        else:
            values.append(lib.Fg_getAppletIntProperty(item,_applet_int_props[p]))
    return TFullAppletInfo(*values) if full_desc else TAppletInfo(*values)
def list_applets(board, full_desc=False, valid=True, on_board=False):
    """
    List all applets available for this board.

    `board` is the board index (starting from 0) given by its position in the list returned by :func:`list_boards`.
    If ``full_desc==True``, return full description for each applet; otherwise, return only name and file name.
    If ``valid==True``, list only valid and compatible applets; otherwise, list all applets.
    If ``on_board==True``, list applets running on board; otherwise, list all applets contained in the system.
    """
    lib.initlib()
    # 0x157 is all valid and compatible flags: FG_AF_IS_AVAILABLE, FG_AF_IS_CORRECT_PLATFORM, FG_AF_IS_VALID_LICENSE, 
    # FG_AF_IS_LOADABLE, FG_AF_IS_COMPATIBLE, FG_AF_IS_SUPPORTED_BY_RUNTIME
    flag=0x157 if valid else 0
    src=FgAppletIteratorSource.FG_AIS_BOARD if on_board else FgAppletIteratorSource.FG_AIS_FILESYSTEM
    appn,appiter=lib.Fg_getAppletIterator(board,src,flag)
    infos=[]
    try:
        for i in range(appn):
            item=lib.Fg_getAppletIteratorItem(appiter,i)
            infos.append(_get_applet_item_info(item,full_desc=full_desc))
    finally:
        lib.Fg_freeAppletIterator(appiter)
    return infos

def get_applet_info(board, **kwargs):
    """Return full information for an applet with the given parameters (e.g., name, or full path)"""
    applets=list_applets(board,full_desc=True)
    for app in applets:
        if all([getattr(app,k)==v for k,v in kwargs.items()]):
            return app
    raise KeyError("could not fine applet with the parameters {}".format(kwargs))




class FGrabAttribute:
    """
    Object representing an Silicon Software frame grabber parameter.

    Allows to query and set values and get additional information.
    Usually created automatically by an :class:`` instance, but could be created manually.

    Args:
        fg: opened frame grabber handle
        aid: attribute ID
        port: camera port within the frame grabber
        system: if ``True``, this is a system attribute; otherwise, it is a camera attribute

    Attributes:
        name: attribute name
        kind: attribute kind; can be ``"i32"``, ``"i64"``, ``"u32"``, ``"u64"``, ``"f64"``, or ``"str"``
        min (float or int): minimal attribute value (if applicable)
        max (float or int): maximal attribute value (if applicable)
        inc (float or int): minimal attribute increment value (if applicable)
        ivalues: list of possible integer values for enum attributes
        values: list of possible text values for enum attributes
        labels: dict ``{label: index}`` which shows all possible values of an enumerated attribute and their corresponding numerical values
        ilabels: dict ``{index: label}`` which shows labels corresponding to numerical values of an enumerated attribute
    """
    _attr_types={   FgParamTypes.FG_PARAM_TYPE_INT32_T: "i32",
                    FgParamTypes.FG_PARAM_TYPE_UINT32_T: "u32",
                    FgParamTypes.FG_PARAM_TYPE_INT64_T: "i64",
                    FgParamTypes.FG_PARAM_TYPE_UINT64_T: "u64",
                    FgParamTypes.FG_PARAM_TYPE_DOUBLE: "f64",
                    FgParamTypes.FG_PARAM_TYPE_CHAR_PTR: "str",
                    FgParamTypes.FG_PARAM_TYPE_SIZE_T: "size",
                    FgParamTypes.FG_PARAM_TYPE_STRUCT_FIELDPARAMACCESS: "fp_acc",
                    FgParamTypes.FG_PARAM_TYPE_STRUCT_FIELDPARAMINT: "fp_i32",
                    FgParamTypes.FG_PARAM_TYPE_STRUCT_FIELDPARAMINT64:  "fp_i64",
                    FgParamTypes.FG_PARAM_TYPE_STRUCT_FIELDPARAMDOUBLE:  "fp_f64", }
    def __init__(self, fg, aid, port=0, system=False):
        self.fg=fg
        self.siso_port=port
        self.aid=aid
        self.system=system
        if system:
            self.name=drFg_Info_Selector.get(aid,None)
        else:
            self.name=py3.as_str(lib.Fg_getParameterNameById(fg,aid,self.siso_port))
        self._attr_type_n=int(self._get_property(FgProperty.PROP_ID_DATATYPE))
        self.kind=self._attr_types[self._attr_type_n]
        self.min=None
        self.max=None
        self.inc=None
        self.values=[]
        self.ivalues=[]
        self.labels={}
        self.ilabels={}
        if not self.system:
            self.ilabels=self._get_enum_values()
            self.ivalues=list(self.ilabels)
            self.values=[self.ilabels[i] for i in self.ivalues]
            self.labels=dict(zip(self.values,self.ivalues))
            self.update_limits()
    
    def _get_property(self, prop):
        if self.system:
            return lib.Fg_getSystemInformation(self.fg,self.aid,prop,0)
        return lib.Fg_getParameterPropertyEx(self.fg,self.aid,prop,self.siso_port)
    def update_limits(self):
        """Update minimal and maximal attribute limits and return tuple ``(min, max, inc)``"""
        if self.kind in ["i32","u32","i64","u64"]:
            self.min=int(self._get_property(FgProperty.PROP_ID_MIN))
            self.max=int(self._get_property(FgProperty.PROP_ID_MAX))
            self.inc=int(self._get_property(FgProperty.PROP_ID_STEP))
        if self.kind=="f64":
            self.min=float(self._get_property(FgProperty.PROP_ID_MIN))
            self.max=float(self._get_property(FgProperty.PROP_ID_MAX))
            self.inc=float(self._get_property(FgProperty.PROP_ID_STEP))
        return (self.min,self.max,self.inc)
    def _get_enum_values(self):
        try:
            self._get_property(FgProperty.PROP_ID_IS_ENUM)
        except fgrab_prototyp_lib.SIFgrabLibError as err:
            if err.code!=FG_STATUS.FG_INVALID_TYPE:
                raise
            return {}
        vstr=self._get_property(FgProperty.PROP_ID_ENUM_VALUES)
        values={}
        while vstr:
            ival,=struct.unpack("<I",vstr[:4])
            if ival==0xFFFFFFFF:
                break
            vstr=vstr[4:]
            p=vstr.find(b"\x00")
            sval=py3.as_str(vstr[:p])
            values[ival]=sval
            vstr=vstr[p+1:]
        return values
    def truncate_value(self, value):
        """Truncate value to lie within attribute limits"""
        self.update_limits()
        if self.kind in ["i32","u32","i64","u64","f64"] and not self.values:
            if value<self.min:
                value=self.min
            elif value>self.max:
                value=self.max
            else:
                inc=self.inc
                if inc>0:
                    value=((value-self.min)//inc)*inc+self.min
        return value

    def get_value(self, enum_as_str=True):
        """
        Get attribute value.
        
        If ``enum_as_str==True``, return enum-style values as strings; otherwise, return corresponding integer values.
        """
        if self.system:
            val=self._get_property(FgProperty.PROP_ID_VALUE)
            if self.kind in ["i32","i64","u32","u64"]:
                if val.startswith(b"0x"):
                    val=int(val[2:],base=16)
                val=int(val)
            elif self.kind=="f64":
                val=float(val)
        else:
            val=lib.Fg_getParameterWithType_auto(self.fg,self.aid,self.siso_port,ptype=self._attr_type_n)
        if self.kind=="str":
            val=py3.as_str(val)
        if enum_as_str and self.ilabels:
            val=self.ilabels.get(val,val)
        return val
    def set_value(self, value, truncate=True):
        """
        Get attribute value.
        
        If ``truncate==True``, automatically truncate value to lie within allowed range.
        """
        if self.system:
            raise ValueError("system property {} can not be set".format(self.name))
        if truncate:
            value=self.truncate_value(value)
        if self.labels:
            value=self.labels.get(value,value)
        lib.Fg_setParameterWithType_auto(self.fg,self.aid,value,self.siso_port,ptype=self._attr_type_n)

    def __repr__(self):
        return "{}(name='{}', kind='{}')".format(self.__class__.__name__,self.name,self.kind)







TDeviceInfo=collections.namedtuple("TDeviceInfo",["applet_info","system_info","software_version"])
TFrameInfo=collections.namedtuple("TFrameInfo",["frame_index","framestamp","timestamp","timestamp_long"])
class SiliconSoftwareFrameGrabber(camera.IGrabberAttributeCamera,camera.IROICamera):
    """
    Generic Silicon Software frame grabber interface.

    Compared to :class:`SiliconSoftwareCamera`, has more permissive initialization arguments,
    which simplifies its use as a base class for expanded cameras.

    Args:
        siso_board: board index, starting from 0; available boards can be learned by :func:`list_boards`
        siso_applet: applet name, which can be learned by :func:`list_applets`;
            usually, a simple applet like ``"DualLineGray16"`` or ``"MediumLineGray16`` are most appropriate;
            can be either an applet name, or a direct path to the applet DLL
        siso_port: port number, if several ports are supported by the camera and the applet
        siso_detector_size: if not ``None``, can specify the maximal detector size;
            by default, use the maximal available for the frame grabber (usually, 16384x16384)
    """
    Error=SiliconSoftwareError
    TimeoutError=SiliconSoftwareTimeoutError
    _TFrameInfo=TFrameInfo
    _adjustable_frameinfo_period=True
    def __init__(self, siso_board=0, siso_applet="DualAreaGray16", siso_port=0, siso_detector_size=None, do_open=True, **kwargs):
        super().__init__(**kwargs)
        lib.initlib()
        self.siso_board=siso_board
        self.siso_applet=siso_applet
        self.siso_port=siso_port
        try:
            self.siso_applet_path=get_applet_info(self.siso_board,name=self.siso_applet).path
        except KeyError:
            self.siso_applet_path=self.siso_applet
        self.fg=None
        self._buffer_mgr=camera.ChunkBufferManager()
        self._buffer_head=None
        self._frame_merge=1
        self._acq_in_progress=False
        self._system_info=None
        self.siso_detector_size=siso_detector_size

        self._add_info_variable("device_info",self.get_device_info)
        self._add_info_variable("camlink_pixel_formats",self.get_available_camlink_pixel_formats)
        self._add_status_variable("pixel_format",self.get_camlink_pixel_format,ignore_error=SiliconSoftwareError)

        if do_open:
            self.open()


    def _normalize_grabber_attribute_name(self, name):
        if name.startswith("FG_"):
            return name[3:]
        return name
    _fixed_parameters=[FG_PARAM.FG_CAMSTATUS,FG_PARAM.FG_IMAGE_TAG,FG_PARAM.FG_TIMEOUT,FG_PARAM.FG_TIMESTAMP,FG_PARAM.FG_TIMESTAMP_LONG,FG_PARAM.FG_TRANSFER_LEN,FG_PARAM.FG_GLOBAL_ACCESS]
    def _list_grabber_attributes(self):
        pnum=lib.Fg_getNrOfParameter(self.fg)
        attrs=[FGrabAttribute(self.fg,lib.Fg_getParameterId(self.fg,i),port=self.siso_port) for i in range(pnum)]
        attrs+=[FGrabAttribute(self.fg,aid,port=self.siso_port) for aid in self._fixed_parameters]
        return [a for a in attrs if a.kind in ["i32","u32","i64","u64","f64","str"]]
    def _get_connection_parameters(self):
        return self.siso_board,self.siso_applet,self.siso_port,self.siso_applet_path
    def open(self):
        """Open connection to the camera"""
        super().open()
        if self.fg is None:
            self.fg=lib.Fg_Init(self.siso_applet_path,self.siso_board)
            self._update_grabber_attributes()
    def close(self):
        """Close connection to the camera"""
        if self.fg is not None:
            self.clear_acquisition()
            try:
                self.fg=lib.Fg_FreeGrabber(self.fg)
            finally:
                self.fg=None
        super().close()
    def is_opened(self):
        """Check if the device is connected"""
        return self.fg is not None

    
    def get_all_grabber_attribute_values(self, root="", **kwargs):
        grabber_attributes=self.get_grabber_attribute(root)
        values=dictionary.Dictionary()
        for n,a in grabber_attributes.items():
            try:
                values[n]=a.get_value(**kwargs)
            except SiliconSoftwareError:
                pass
        return values
    def set_all_grabber_attribute_values(self, settings, root="", **kwargs):
        grabber_attributes=self.get_grabber_attribute(root)
        settings=dictionary.as_dict(settings,style="flat",copy=False)
        for k,v in settings.items():
            k=self._normalize_grabber_attribute_name(k)
            if k in grabber_attributes:
                try:
                    grabber_attributes[k].set_value(v,**kwargs)
                except SiliconSoftwareError:
                    pass
    
    def get_system_info(self):
        """Get the dictionary with all system information parameters"""
        if self._system_info is None:
            self._system_info={}
            for aid in Fg_Info_Selector:
                try:
                    attr=FGrabAttribute(self.fg,aid.value,system=True)
                    self._system_info[attr.name]=attr.get_value()
                except SiliconSoftwareError:
                    pass
        return self._system_info
    def get_genicam_info_xml(self):
        """Get description in Genicam-compatible XML format"""
        return py3.as_str(lib.Fg_getParameterInfoXML(self.fg,self.siso_port))
    
    def get_device_info(self):
        """
        Get camera model data.

        Return tuple ``(applet_info, system_info, software_version)`` with the board serial number and an the interface type (e.g., ``"1430"`` for NI PCIe-1430)
        """
        system_info=self.get_system_info()
        applet_info=get_applet_info(self.siso_board,path=self.siso_applet_path)
        software_version=py3.as_str(lib.Fg_getSWVersion())
        return TDeviceInfo(applet_info,system_info,software_version)


    def set_frame_merge(self, frame_merge=1):
        if self._frame_merge!=frame_merge:
            roi=self.get_grabber_roi()
            self.clear_acquisition()
            self._frame_merge=frame_merge
            self.set_grabber_roi(*roi)
    def _get_data_dimensions_rc(self):
        return self.gav["HEIGHT"]//self._frame_merge,self.gav["WIDTH"]
    def get_detector_size(self):
        return self.siso_detector_size or (self.get_grabber_attribute("WIDTH").max,self.get_grabber_attribute("HEIGHT").max)
    get_grabber_detector_size=get_detector_size
    def get_roi(self):
        w,h=self.gav["WIDTH"],self.gav["HEIGHT"]//self._frame_merge
        l,t=self.gav["XOFFSET"],self.gav["YOFFSET"]
        return l,l+w,t,t+h
    get_grabber_roi=get_roi
    @camera.acqcleared
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None):
        hlim,vlim=self.get_grabber_roi_limits()
        if hend is None:
            hend=hlim.max
        if vend is None:
            vend=vlim.max
        hstart,hend=self._truncate_roi_axis((hstart,hend),hlim)
        vstart,vend=self._truncate_roi_axis((vstart,vend),vlim)
        if self._frame_merge!=1 and vstart!=0:
            raise ValueError("frame merging is only supported with full vertical frame size")
        self.gav["XOFFSET"]=0
        self.gav["WIDTH"]=hend-hstart
        self.gav["XOFFSET"]=hstart
        self.gav["YOFFSET"]=0
        self.gav["HEIGHT"]=(vend-vstart)*self._frame_merge
        self.gav["YOFFSET"]=vstart  # non-zero only if self._frame_merge==1
        return self.get_grabber_roi()
    set_grabber_roi=set_roi
    def get_roi_limits(self, hbin=1, vbin=1):
        w,h=self.get_grabber_attribute("WIDTH"),self.get_grabber_attribute("HEIGHT")
        x,y=self.get_grabber_attribute("XOFFSET"),self.get_grabber_attribute("YOFFSET")
        detsize=self.get_detector_size()
        hlim=camera.TAxisROILimit(w.min,detsize[1],x.inc,w.inc,1)
        vlim=camera.TAxisROILimit(h.min,detsize[0],y.inc,h.inc,1)
        return hlim,vlim
    get_grabber_roi_limits=get_roi_limits


    def _get_acquired_frames(self):
        if not self.acquisition_in_progress():
            return None
        return lib.Fg_getStatusEx(self.fg,FG_GETSTATUS.NUMBER_OF_GRABBED_IMAGES,0,self.siso_port,self._buffer_head)*self._frame_merge
        
    def _setup_buffers(self, nframes):
        self._clear_buffers()
        nbuff=(nframes-1)//self._frame_merge+1
        buffer_size=self._get_buffer_size()
        self._buffer_mgr.allocate(nbuff,buffer_size)
        self._buffer_head=lib.Fg_AllocMemHead(self.fg,nbuff*buffer_size,nbuff)
        cbuffs=self._buffer_mgr.get_ctypes_frames_list(ctype=ctypes.c_void_p)
        for i,b in enumerate(cbuffs):
            lib.Fg_AddMem(self.fg,b,buffer_size,i,self._buffer_head)
    def _clear_buffers(self):
        if self._buffer_mgr:
            cbuffs=self._buffer_mgr.get_ctypes_frames_list(ctype=ctypes.c_void_p)
            for i,_ in enumerate(cbuffs):
                lib.Fg_DelMem(self.fg,self._buffer_head,i)
            lib.Fg_FreeMemHead(self.fg,self._buffer_head)
            self._buffer_head=None
            self._buffer_mgr.deallocate()
    def _ensure_buffers(self):
        nbuff=self._buffer_mgr.nframes
        buffer_size=self._get_buffer_size()
        if buffer_size!=self._buffer_mgr.frame_size:
            self._setup_buffers(nbuff)

    _camlink_fmts={ ( 8,1):MeCameraLinkFormat.FG_CL_SINGLETAP_8_BIT,
                    (10,1):MeCameraLinkFormat.FG_CL_SINGLETAP_10_BIT,
                    (12,1):MeCameraLinkFormat.FG_CL_SINGLETAP_12_BIT,
                    (14,1):MeCameraLinkFormat.FG_CL_SINGLETAP_14_BIT,
                    (16,1):MeCameraLinkFormat.FG_CL_SINGLETAP_16_BIT,
                    ( 8,2):MeCameraLinkFormat.FG_CL_DUALTAP_8_BIT,
                    (10,2):MeCameraLinkFormat.FG_CL_DUALTAP_10_BIT,
                    (12,2):MeCameraLinkFormat.FG_CL_DUALTAP_12_BIT,}
    def setup_camlink_pixel_format(self, bits_per_pixel=8, taps=1, output_fmt=None, fmt=None):
        """
        Set up CameraLink pixel format.
        
        If `fmt` is ``None``, use supplied `bits_per_pixel` (8, 10, 12, 14, or 16) and `taps` (1 or 2) to figure out the format;
        otherwise, `fmt` should be a numerical (e.g., ``210``) or string (e.g., ``"FG_CL_MEDIUM_10_BIT"``) format.
        `output_fmt` specifies the result frame format; if ``None``, use grayscale with the given `bits_per_pixel`
        if `fmt` is ``None``, or 16 bit grayscale otherwise.
        """
        if fmt is None:
            try:
                fmt=self._camlink_fmts[bits_per_pixel,taps]
                if output_fmt is None:
                    if bits_per_pixel<=8:
                        output_fmt=FG_IMGFMT.FG_GRAY
                    elif bits_per_pixel<=16:
                        output_fmt=FG_IMGFMT.FG_GRAY16
                    else:
                        output_fmt=FG_IMGFMT.FG_GRAY32
            except KeyError:
                raise KeyError("combination for {} bits per pixel and {} taps is not supported".format(bits_per_pixel,taps))
        else:
            if output_fmt is None:
                output_fmt=FG_IMGFMT.FG_GRAY16
        self.gav["CAMERA_LINK_CAMTYP"]=fmt
        self.gav["FORMAT"]=output_fmt
    def get_camlink_pixel_format(self):
        """Get CamLink pixel format and the output pixel format as a tuple"""
        try:
            return (self.gav["CAMERA_LINK_CAMTYP"],self.gav["FORMAT"])
        except KeyError:
            return None
    def get_available_camlink_pixel_formats(self):
        """Get all available CamLink pixel formats and the output pixel formats as a tuple of 2 lists"""
        try:
            clfmts=list(self.get_grabber_attribute("CAMERA_LINK_CAMTYP").values)
        except KeyError:
            clfmts=None
        try:
            pxfmts=list(self.get_grabber_attribute("FORMAT").values)
        except KeyError:
            pxfmts=None
        return pxfmts,clfmts


    @interface.use_parameters(mode="acq_mode")
    def setup_acquisition(self, mode="sequence", nframes=100):  # pylint: disable=arguments-differ
        """
        Setup acquisition mode.

        `mode` can be either ``"snap"`` (single frame or a fixed number of frames) or ``"sequence"`` (continuous acquisition).
        (note that :meth:`.IMAQCamera.acquisition_in_progress` would still return ``True`` in this case, even though new frames are no longer acquired).
        `nframes` sets up number of frame buffers.
        """
        self.clear_acquisition()
        super().setup_acquisition(mode=mode,nframes=nframes)
        self._setup_buffers(nframes)
    def clear_acquisition(self):
        """Clear all acquisition details and free all buffers"""
        if self._acq_params:
            self.stop_acquisition()
            self._clear_buffers()
            super().clear_acquisition()
    def start_acquisition(self, *args, **kwargs):
        self.stop_acquisition()
        super().start_acquisition(*args,**kwargs)
        self._ensure_buffers()
        mode=self._acq_params["mode"]
        nframes=self._acq_params["nframes"] if mode=="snap" else -1
        self._frame_counter.reset(self._buffer_mgr.nframes*self._frame_merge)
        lib.Fg_AcquireEx(self.fg,self.siso_port,nframes,FG_ACQ.ACQ_STANDARD,self._buffer_head)
        self._acq_in_progress=True
    def stop_acquisition(self):
        if self.acquisition_in_progress():
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
            lib.Fg_stopAcquireEx(self.fg,self.siso_port,self._buffer_head,FG_ACQ.ACQ_STANDARD)
            self._acq_in_progress=False
    def acquisition_in_progress(self):
        return self._acq_in_progress


    
    def _wait_for_next_frame(self, timeout=20., idx=None):
        if timeout is None or timeout>0.1:
            timeout=0.1
        try:
            if idx is None:
                idx=self._frame_counter.last_acquired_frame+1
            lib.Fg_getLastPicNumberBlockingEx(self.fg,idx,self.siso_port,int(timeout*1000),self._buffer_head)
        except SIFgrabLibError as err:
            if err.code==FG_STATUS.FG_TIMEOUT_ERR:
                pass
            elif err.code in [FG_STATUS.FG_INVALID_MEMORY,FG_STATUS.FG_TRANSFER_NOT_ACTIVE] and not self.acquisition_in_progress():
                raise

    
    def _get_buffer_bpp(self):
        bpp=self.gav["PIXELDEPTH"]
        return (bpp-1)//8+1
    def _get_buffer_dtype(self):
        return "<u{}".format(self._get_buffer_bpp())
    def _get_buffer_size(self):
        bpp=self._get_buffer_bpp()
        roi=self.get_grabber_roi()
        w,h=roi[1]-roi[0],roi[3]-roi[2]
        return w*h*bpp*self._frame_merge
    def _parse_buffer(self, buffer, nframes=1):
        r,c=self._get_data_dimensions_rc()
        dt=self._get_buffer_dtype()
        cdt=ctypes.POINTER(np.ctypeslib.as_ctypes_type(dt))
        data=np.ctypeslib.as_array(ctypes.cast(buffer,cdt),shape=((nframes*self._frame_merge,r,c)))
        return data.copy()
    def _trim_images_range(self, rng):
        acquired_frames=self._get_acquired_frames()
        if acquired_frames is None:
            return None
        self._frame_counter.update_acquired_frames(acquired_frames)
        if rng is None:
            rng,skipped=self._frame_counter.get_new_frames_range(),0
            rng=(rng[0]//self._frame_merge)*self._frame_merge,((rng[1]-1)//self._frame_merge+1)*self._frame_merge
        else:
            rng=(rng[0]//self._frame_merge)*self._frame_merge,((rng[1]-1)//self._frame_merge+1)*self._frame_merge
            rng,skipped=self._frame_counter.trim_frames_range(rng)
        return rng,skipped
    _support_chunks=True
    def _read_frames(self, rng, return_info=False):
        raw_frames=self._buffer_mgr.get_frames_data(rng[0]//self._frame_merge,rng[1]//self._frame_merge-rng[0]//self._frame_merge) if rng[1]>rng[0] else []
        if return_info:
            params=[FG_PARAM.FG_IMAGE_TAG,FG_PARAM.FG_TIMESTAMP,FG_PARAM.FG_TIMESTAMP_LONG]
            frame_info=[]
            chn=[n for n,_ in raw_frames]
            chidx=np.cumsum([rng[0]]+chn[:-1])
            frng=range(rng[0]//self._frame_merge,rng[1]//self._frame_merge)
            frame_info=[np.array(frng)*self._frame_merge]
            for p in params:
                try:
                    frame_info.append([lib.Fg_getParameterEx_auto(self.fg,p,self.siso_port,self._buffer_head,i+1) if i%self._frameinfo_period==0 else 0 for i in frng])
                except SIFgrabLibError:
                    frame_info.append([0]*len(frng))
            frame_info=np.array(frame_info)
            frame_info[1:,frame_info[0]%self._frameinfo_period!=0]=-1
            frame_info=[frame_info[:,i:i+n].T for i,n in zip(chidx-chidx[0],chn)]
        else:
            frame_info=None
        parsed_frames=[self._convert_indexing(self._parse_buffer(b,nframes=n),"rct",axes=(-2,-1)) for n,b in raw_frames]
        return parsed_frames,frame_info






class SiliconSoftwareCamera(SiliconSoftwareFrameGrabber):
    """
    Generic Silicon Software frame grabber interface.

    Args:
        board: board index, starting from 0; available boards can be learned by :func:`list_boards`
        applet: applet name, which can be learned by :func:`list_applets`;
            usually, a simple applet like ``"DualLineGray16"`` or ``"MediumLineGray16`` are most appropriate;
            can be either an applet name, or a direct path to the applet DLL
        port: port number, if several ports are supported by the camera and the applet
        detector_size: if not ``None``, can specify the maximal detector size;
            by default, use the maximal available for the frame grabber (usually, 16384x16384)
    """
    def __init__(self, board, applet, port=0, detector_size=None):
        super().__init__(siso_board=board,siso_applet=applet,siso_port=port,siso_detector_size=detector_size)