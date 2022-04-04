from pylablib.core.utils import funcargparse
from . import NIIMAQdx_lib
from .NIIMAQdx_lib import IMAQdxAttributeType, IMAQdxAttributeVisibility, IMAQdxCameraControlMode, IMAQdxBufferNumberMode
from .NIIMAQdx_lib import wlib as lib, IMAQdxError, IMAQdxLibError  # pylint: disable=unused-import

from ...core.utils import py3, dictionary
from ...core.devio import interface
from ..interface import camera

import numpy as np
import collections
import time


class IMAQdxTimeoutError(IMAQdxError):
    "IMAQdx frame timeout error"







TCameraInfo=collections.namedtuple("TCameraInfo",["name","type","version","flags","serial_number","bus","vendor","model","camera_file","attr_url"])
def _parse_camera_info(info):
    name=py3.as_str(info.InterfaceName)
    ctype=info.Type
    version=info.Version
    flags=info.Flags
    serial_number="{:016X}".format((info.SerialNumberHi<<32)+info.SerialNumberLo)
    try:
        bus=NIIMAQdx_lib.IMAQdxBusType(info.BusType).name[len("IMAQdxBusType"):]
    except ValueError:
        bus=info.BusType
    vendor=py3.as_str(info.VendorName)
    model=py3.as_str(info.ModelName)
    camera_file=py3.as_str(info.CameraFileName)
    attr_url=py3.as_str(info.CameraAttributeURL)
    return TCameraInfo(name,ctype,version,flags,serial_number,bus,vendor,model,camera_file,attr_url)
def list_cameras(connected=True, desc=True):
    """
    List all cameras available through IMAQdx interface
    
    If ``desc==True``, return complete camera descriptions; otherwise, simply return the names.
    """
    lib.initlib()
    cams=lib.IMAQdxEnumerateCameras(connected)
    infos=[_parse_camera_info(c) for c in cams]
    return infos if desc else [inf.name for inf in infos]

def get_cameras_number():
    """Get number of connected dx cameras"""
    return len(list_cameras())




class IMAQdxAttribute:
    """
    Object representing an IMAQdx camera parameter.

    Allows to query and set values and get additional information.
    Usually created automatically by an :class:`IMAQdxCamera` instance, but could be created manually.

    Args:
        sid: camera session ID
        name: attribute text name

    Attributes:
        name: attribute name
        kind: attribute kind; can be ``"u32"``, ``"i64"``, ``"f64"``, ``"str"``, ``"enum"``,
            ``"bool"``, ``"command"``, or ``"blob"``
        display_name: attribute display name (short description name)
        tooltip: longer attribute description
        description: full attribute description (usually, same as `tooltip`)
        units: attribute units (if applicable)
        visibility: attribute visibility (``"simple"``, ``"intermediate"``, or ``"advanced"``)
        readable (bool): whether attribute is readable
        writable (bool): whether attribute is writable
        min (float or int): minimal attribute value (if applicable)
        max (float or int): maximal attribute value (if applicable)
        inc (float or int): minimal attribute increment value (if applicable)
        ivalues: list of possible integer values for enum attributes
        values: list of possible text values for enum attributes
        labels: dict ``{label: index}`` which shows all possible values of an enumerated attribute and their corresponding numerical values
        ilabels: dict ``{index: label}`` which shows labels corresponding to numerical values of an enumerated attribute
    """
    _attr_types={   IMAQdxAttributeType.IMAQdxAttributeTypeU32:"u32",
                    IMAQdxAttributeType.IMAQdxAttributeTypeI64:"i64",
                    IMAQdxAttributeType.IMAQdxAttributeTypeF64:"f64",
                    IMAQdxAttributeType.IMAQdxAttributeTypeString:"str",
                    IMAQdxAttributeType.IMAQdxAttributeTypeEnum:"enum",
                    IMAQdxAttributeType.IMAQdxAttributeTypeBool:"bool",
                    IMAQdxAttributeType.IMAQdxAttributeTypeCommand:"command",
                    IMAQdxAttributeType.IMAQdxAttributeTypeBlob:"blob"}
    _vis_types={    IMAQdxAttributeVisibility.IMAQdxAttributeVisibilitySimple:"simple",
                    IMAQdxAttributeVisibility.IMAQdxAttributeVisibilityIntermediate:"intermediate",
                    IMAQdxAttributeVisibility.IMAQdxAttributeVisibilityAdvanced:"advanced"}
    def __init__(self, sid, name):
        self.sid=sid
        self.name=py3.as_str(name)
        self.display_name=py3.as_str(lib.IMAQdxGetAttributeDisplayName(sid,name))
        self.tooltip=py3.as_str(lib.IMAQdxGetAttributeTooltip(sid,name))
        self.description=py3.as_str(lib.IMAQdxGetAttributeDescription(sid,name))
        self.visibility=self._vis_types[lib.IMAQdxGetAttributeVisibility(sid,name)]
        self.units=py3.as_str(lib.IMAQdxGetAttributeUnits(sid,name))
        self.readable=lib.IMAQdxIsAttributeReadable(sid,name)
        self.writable=lib.IMAQdxIsAttributeWritable(sid,name)
        self._attr_type_n=lib.IMAQdxGetAttributeType(sid,name)
        self.kind=self._attr_types[self._attr_type_n]
        self.min=None
        self.max=None
        self.inc=None
        self.values=[]
        self.ivalues=[]
        self.labels={}
        self.ilabels={}
        self.update_limits()
    
    def update_limits(self):
        """Update minimal and maximal attribute limits and return tuple ``(min, max, inc)``"""
        if self._attr_type_n in lib.numeric_attr_types:
            self.min=lib.IMAQdxGetAttributeMinimum(self.sid,self.name,self._attr_type_n)
            self.max=lib.IMAQdxGetAttributeMaximum(self.sid,self.name,self._attr_type_n)
            self.inc=lib.IMAQdxGetAttributeIncrement(self.sid,self.name,self._attr_type_n)
            return (self.min,self.max,self.inc)
        if self._attr_type_n==IMAQdxAttributeType.IMAQdxAttributeTypeEnum:
            attr_values=lib.IMAQdxEnumerateAttributeValues(self.sid,self.name)
            self.values=[av.Name for av in attr_values]
            self.ivalues=[av.Value for av in attr_values]
            self.labels=dict(zip(self.values,self.ivalues))
            self.ilabels=dict(zip(self.ivalues,self.values))
    def truncate_value(self, value):
        """Truncate value to lie within attribute limits"""
        self.update_limits()
        if self._attr_type_n in lib.numeric_attr_types:
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
        if not self.readable:
            raise IMAQdxError("Attribute {} is not readable".format(self.name))
        val=lib.IMAQdxGetAttribute(self.sid,self.name,self._attr_type_n)
        if self._attr_type_n==IMAQdxAttributeType.IMAQdxAttributeTypeEnum:
            val=val.Name if enum_as_str else val.Value
        return val
    def set_value(self, value, truncate=True):
        """
        Get attribute value.
        
        If ``truncate==True``, automatically truncate value to lie within allowed range.
        """
        if not self.writable:
            raise IMAQdxError("Attribute {} is not writable".format(self.name))
        if truncate:
            value=self.truncate_value(value)
        return lib.IMAQdxSetAttribute(self.sid,self.name,value,None)

    def __repr__(self):
        return "{}(name='{}', kind='{}')".format(self.__class__.__name__,self.name,self.kind)




TDeviceInfo=collections.namedtuple("TDeviceInfo",["vendor","model","serial_number","bus_type"])
class IMAQdxCamera(camera.IROICamera, camera.IAttributeCamera):
    """
    Generic IMAQdx camera interface.

    Args:
        name: interface name (can be learned by :func:`list_cameras`; usually, but not always, starts with ``"cam"``)
        mode: connection mode; can be ``"controller"`` (full control) or ``"listener"`` (only reading)
        visibility: attribute visibility when listing attributes;
            can be ``"simple"``, ``"intermediate"`` or ``"advanced"`` (higher mode exposes more attributes).
    """
    Error=IMAQdxError
    TimeoutError=IMAQdxTimeoutError
    def __init__(self, name="cam0", mode="controller", visibility="advanced"):
        super().__init__()
        lib.initlib()
        self.name=name
        self.mode=mode
        self.visibility=visibility
        self.sid=None
        self.open()
        self._raw_readout_format=False
        self._add_info_variable("device_info",self.get_device_info)


    _p_connection_mode=interface.EnumParameterClass("connection_mode",{
        "controller":IMAQdxCameraControlMode.IMAQdxCameraControlModeController,
        "listener":IMAQdxCameraControlMode.IMAQdxCameraControlModeListener})
    _p_visibility=interface.EnumParameterClass("visibility",{
        "simple":IMAQdxAttributeVisibility.IMAQdxAttributeVisibilitySimple,
        "intermediate":IMAQdxAttributeVisibility.IMAQdxAttributeVisibilityIntermediate,
        "advanced":IMAQdxAttributeVisibility.IMAQdxAttributeVisibilityAdvanced})
    def _get_connection_parameters(self):
        return self.name
    def open(self):
        """Open connection to the camera"""
        if self.sid is not None:
            return
        mode=self._p_connection_mode(self.mode)
        self.sid=lib.IMAQdxOpenCamera(self.name,mode)
        with self._close_on_error():
            self._update_attributes()
            self.post_open()
    def close(self):
        """Close connection to the camera"""
        if self.sid is not None:
            try:
                self.clear_acquisition()
            finally:
                lib.IMAQdxCloseCamera(self.sid)
                self.sid=None
    def reset(self):
        """Reset connection to the camera"""
        self.close()
        lib.IMAQdxResetCamera(self.name,False)
        self.open()
    def is_opened(self):
        """Check if the device is connected"""
        return self.sid is not None

    def post_open(self):
        """Additional setup after camera opening"""
        att=self.get_attribute("PixelFormat",error_on_missing=False)
        if att and att.writable:
            att.set_value(att.get_value())  # there seems to be occasional de-synchronization between the read and the actual value

    _builtin_attrs=["OffsetX","OffsetY","Width","Height","PixelFormat","PayloadSize","StatusInformation::LastBufferNumber","AcquisitionAttributes::BitsPerPixel"]
    def _normalize_attribute_name(self, name):
        return name.replace("::","/")
    def _list_attributes(self):
        visibility=self._p_visibility(self.visibility)
        attrs=lib.IMAQdxEnumerateAttributes2(self.sid,"",visibility)
        attr_names=[a.Name for a in attrs]
        for a in self._builtin_attrs:
            if a not in attr_names:
                try:
                    lib.IMAQdxGetAttributeDisplayName(self.sid,a)
                    attr_names.append(a)
                except IMAQdxError:
                    pass
        return [IMAQdxAttribute(self.sid,a) for a in attr_names]

    def get_attribute_value(self, name, error_on_missing=True, default=None, enum_as_str=True):  # pylint: disable=arguments-differ
        """
        Get value of an attribute with the given name.
        
        If the value doesn't exist or can not be read and ``error_on_missing==True``, raise error; otherwise, return `default`.
        If `default` is not ``None``, assume that ``error_on_missing==False``.
        If `name` points at a dictionary branch, return a dictionary with all values in this branch.
        If ``enum_as_str==True``, return enum-style values as strings; otherwise, return corresponding integer values.
        """
        return super().get_attribute_value(name,error_on_missing=error_on_missing,default=default,enum_as_str=enum_as_str)
    def set_attribute_value(self, name, value, truncate=True, error_on_missing=True):  # pylint: disable=arguments-differ
        """
        Set value of an attribute with the given name.
        
        If the value doesn't exist or can not be written and ``error_on_missing==True``, raise error; otherwise, do nothing.
        If `name` points at a dictionary branch, set all values in this branch (in this case `value` must be a dictionary).
        If ``truncate==True``, truncate value to lie within attribute range.
        """
        return super().set_attribute_value(name,value,truncate=truncate,error_on_missing=error_on_missing)
    def get_all_attribute_values(self, root="", enum_as_str=True, ignore_errors=True):  # pylint: disable=arguments-differ
        """Get values of all attributes with the given `root`"""
        values=dictionary.Dictionary()
        for n,att in self.get_attribute(root).as_dict("flat").items():
            if att.readable:
                try:
                    values[n]=att.get_value(enum_as_str=enum_as_str)
                except IMAQdxLibError:  # sometimes nominally implemented features still raise errors
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

        Return tuple ``(vendor, model, serial_number, bus_type)``.
        """
        cam_info=self.cav["CameraInformation"]
        serial="{:016X}".format((cam_info["SerialNumberHigh"]<<32)+cam_info["SerialNumberLow"])
        return TDeviceInfo(cam_info["VendorName"],cam_info["ModelName"],serial,cam_info["BusType"])

    def _get_data_dimensions_rc(self):
        return self.cav["Height"],self.cav["Width"]
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
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
    

    @interface.use_parameters(mode="acq_mode")
    def setup_acquisition(self, mode="sequence", nframes=100):  # pylint: disable=arguments-differ
        """
        Setup acquisition mode.

        `mode` can be either ``"snap"`` (single frame or a fixed number of frames) or ``"sequence"`` (continuous acquisition).
        (note that :meth:`.IMAQdxCamera.acquisition_in_progress` would still return ``True`` in this case, even though new frames are no longer acquired).
        `nframes` sets up number of frame buffers.
        """
        self.clear_acquisition()
        super().setup_acquisition(mode=mode,nframes=nframes)
        lib.IMAQdxConfigureAcquisition(self.sid,mode=="sequence",nframes)
    def clear_acquisition(self):
        self.stop_acquisition()
        lib.IMAQdxUnconfigureAcquisition(self.sid)
        super().clear_acquisition()
    def start_acquisition(self, *args, **kwargs):
        self.stop_acquisition()
        super().start_acquisition(*args,**kwargs)
        self._frame_counter.reset(self._acq_params["nframes"])
        lib.IMAQdxStartAcquisition(self.sid)
    def stop_acquisition(self):
        if self.acquisition_in_progress():
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
            lib.IMAQdxStopAcquisition(self.sid)
        super().stop_acquisition()
    def acquisition_in_progress(self):
        """Check if acquisition is in progress"""
        return self.cav["StatusInformation/AcqInProgress"]
    def refresh_acquisition(self, delay=0.005):
        """Stop and restart the acquisition, waiting `delay` seconds in between"""
        self.stop_acquisition()
        self.clear_acquisition()
        self.setup_acquisition(0,1)
        self.start_acquisition()
        time.sleep(delay)
        self.stop_acquisition()
        self.clear_acquisition()
    def _get_acquired_frames(self):
        last_buffer=self.cav["StatusInformation/LastBufferNumber"]
        if last_buffer>=2**31:
            last_buffer=-1
        # newest_buffer=-1
        # try:
        #     newest_buffer=lib.IMAQdxGetImageData(self.sid,None,0,IMAQdxBufferNumberMode.IMAQdxBufferNumberModeLast,0)
        # except IMAQdxLibError as e:
        #     if e.code!=NIIMAQdx_lib.IMAQdxErrorCode.IMAQdxErrorCameraNotRunning:
        #         raise
        return last_buffer+1

    def _read_data_raw(self, buffer_num, size_bytes, dtype="<u1", mode=IMAQdxBufferNumberMode.IMAQdxBufferNumberModeBufferNumber):
        """Return raw bytes string from the given buffer number"""
        dtype=np.dtype(dtype)
        if size_bytes%dtype.itemsize:
            raise IMAQdxError("specified buffer size {} is not divisible by the element size {}".format(size_bytes,dtype.itemsize))
        arr=np.empty(size_bytes//dtype.itemsize,dtype)
        lib.IMAQdxGetImageData(self.sid,arr.ctypes.data,size_bytes,mode,buffer_num)
        return arr
    def _parse_data(self, data, shape, pixel_format):
        if self._raw_readout_format=="frame":
            return data
        if self._raw_readout_format=="rows":
            return data.reshape((shape[0],-1))
        supported_formats=["Mono8","Mono10","Mono12","Mono16","Mono32"]
        if pixel_format not in supported_formats:
            sf_string=", ".join(supported_formats)
            raise IMAQdxError("pixel format {} is not supported, only [{}] are supported; raw data readout can be enabled via enable_raw_readout method".format(pixel_format,sf_string))
        if pixel_format=="Mono8":
            return data.reshape(shape)
        elif pixel_format in ["Mono10","Mono12","Mono16"]:
            return data.view("<u2").reshape(shape)
        else:
            return data.view("<u4").reshape(shape)
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

    def _read_frames(self, rng, return_info=False):  # TODO: add parsing and pixel format
        indices=range(*rng)
        size_bytes=self.cav["PayloadSize"]
        shape=self.cav["Height"],self.cav["Width"]
        pixel_format=self.cav["PixelFormat"]
        frames=[self._read_data_raw(b,size_bytes) for b in indices]
        frames=[self._parse_data(f,shape,pixel_format) for f in frames]
        if not self._raw_readout_format:
            frames=[self._convert_indexing(f,"rct") for f in frames]
        return frames,None












class EthernetIMAQdxCamera(IMAQdxCamera):
    """
    LAN-controlled IMAQdx camera.

    Compared to the standard camera, has an option of automatically switching to a smaller TCP/IP packet size
    (can be useful if the PC network adapter can't handle jumbo packets).

    Args:
        name: interface name (can be learned by :func:`list_cameras`; usually, but not always, starts with ``"cam"``)
        mode: connection mode; can be ``"controller"`` (full control) or ``"listener"`` (only reading)
        visibility: default attribute visibility when listing attributes;
            can be ``"simple"``, ``"intermediate"`` or ``"advanced"`` (higher mode exposes more attributes).
        small_packet: if ``True``, automatically set small packet size (1500 bytes).
    """
    def __init__(self, name="cam0", mode="controller", visibility="advanced", small_packet=False):
        self.small_packet=small_packet
        super().__init__(name=name,mode=mode,visibility=visibility)
    def post_open(self):
        super().post_open()
        if self.small_packet:
            self.set_attribute_value("AcquisitionAttributes/PacketSize",1500,error_on_missing=False)