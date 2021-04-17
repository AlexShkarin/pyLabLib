from . import NIIMAQdx_lib
from .NIIMAQdx_lib import IMAQdxAttributeType, IMAQdxAttributeVisibility, IMAQdxCameraControlMode, IMAQdxBufferNumberMode
from .NIIMAQdx_lib import lib, IMAQdxError, IMAQdxLibError

from ...core.utils import dictionary, py3
from ...core.devio import interface
from ..interface import camera

import numpy as np
import collections
import time


class IMAQdxTimeoutError(IMAQdxError):
    "IMAQdx frame timeout error"



class IMAQdxAttribute:
    """
    Object representing an IMAQdx camera parameter.

    Allows to query and set values and get additional information.
    Usually created automatically by an :class:`IMAQdxCamera` instance, but could be created manually.

    Attributes:
        name: attribute name
        display_name: attribute display name (short description name)
        tooltip: longer attribute description
        description: full attribute description (usually, same as `tooltip`)
        units: attribute units (if applicable)
        readable (bool): whether attribute is readable
        writable (bool): whether attribute is writable
        min (float or int): minimal attribute value (if applicable)
        max (float or int): maximal attribute value (if applicable)
        inc (float or int): minimal attribute increment value (if applicable)
        values: list of possible attribute values (if applicable)
    """
    _attr_types={   IMAQdxAttributeType.IMAQdxAttributeTypeU32:"u32",
                    IMAQdxAttributeType.IMAQdxAttributeTypeI64:"i64",
                    IMAQdxAttributeType.IMAQdxAttributeTypeF64:"f64",
                    IMAQdxAttributeType.IMAQdxAttributeTypeString:"str",
                    IMAQdxAttributeType.IMAQdxAttributeTypeEnum:"enum",
                    IMAQdxAttributeType.IMAQdxAttributeTypeBool:"bool",
                    IMAQdxAttributeType.IMAQdxAttributeTypeCommand:"command",
                    IMAQdxAttributeType.IMAQdxAttributeTypeBlob:"blob"}
    def __init__(self, sid, name):
        self.sid=sid
        self.name=py3.as_str(name)
        self.display_name=py3.as_str(lib.IMAQdxGetAttributeDisplayName(sid,name))
        self.tooltip=py3.as_str(lib.IMAQdxGetAttributeTooltip(sid,name))
        self.description=py3.as_str(lib.IMAQdxGetAttributeDescription(sid,name))
        self.units=py3.as_str(lib.IMAQdxGetAttributeUnits(sid,name))
        self.readable=lib.IMAQdxIsAttributeReadable(sid,name)
        self.writable=lib.IMAQdxIsAttributeWritable(sid,name)
        self._attr_type_n=lib.IMAQdxGetAttributeType(sid,name)
        self.type=self._attr_types[self._attr_type_n]
        if self._attr_type_n in lib.numeric_attr_types:
            self.min=lib.IMAQdxGetAttributeMinimum(sid,name,self._attr_type_n)
            self.max=lib.IMAQdxGetAttributeMaximum(sid,name,self._attr_type_n)
            self.inc=lib.IMAQdxGetAttributeIncrement(sid,name,self._attr_type_n)
        else:
            self.min=self.max=self.inc=None
        if self._attr_type_n==IMAQdxAttributeType.IMAQdxAttributeTypeEnum:
            self.values=lib.IMAQdxEnumerateAttributeValues(sid,name)
        else:
            self.values=None
    
    def update_minmax(self):
        """Update minimal and maximal attribute limits"""
        if self._attr_type_n in lib.numeric_attr_types:
            self.min=lib.IMAQdxGetAttributeMinimum(self.sid,self.name,self._attr_type_n)
            self.max=lib.IMAQdxGetAttributeMaximum(self.sid,self.name,self._attr_type_n)
            self.inc=lib.IMAQdxGetAttributeIncrement(self.sid,self.name,self._attr_type_n)
    def truncate_value(self, value):
        """Truncate value to lie within attribute limits"""
        self.update_minmax()
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
        if self._attr_type_n==IMAQdxAttributeType.IMAQdxAttributeTypeEnum and enum_as_str:
            val=val.Name
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
        return "{}({})".format(self.__class__.__name__,self.name)





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




TDeviceInfo=collections.namedtuple("TDeviceInfo",["vendor","model","serial_number","bus_type"])
class IMAQdxCamera(camera.IROICamera):
    """
    Generic IMAQdx camera interface.

    Args:
        name: interface name (can be learned by :func:`list_cameras`; usually, but not always, starts with ``"cam"``)
        mode: connection mode; can be ``"controller"`` (full control) or ``"listener"`` (only reading)
        default_visibility: default attribute visibility when listing attributes;
            can be ``"simple"``, ``"intermediate"`` or ``"advanced"`` (higher mode exposes more attributes).
    """
    Error=IMAQdxError
    TimeoutError=IMAQdxTimeoutError
    def __init__(self, name="cam0", mode="controller", default_visibility="advanced"):
        super().__init__()
        lib.initlib()
        self.init_done=False
        self.name=name
        self.mode=mode
        self.default_visibility=default_visibility
        self.sid=None
        self.open()
        self.image_indexing="rct"
        try:
            attrs=self.list_attributes()
            self.attributes=dictionary.Dictionary(dict([ (a.name.replace("::","/"),a) for a in attrs ]))
        except Exception:
            self.close()
            raise
        self.init_done=True
        self.acq_params=None
        self.frame_counter=0
        self.last_wait_frame=-1
        self.buffers_num=0
        self.v=dictionary.ItemAccessor(self.get_value,self.set_value)

        self._add_info_variable("device_info",self.get_device_info)
        self._add_info_variable("interface_name",lambda: self.name)
        self._add_status_variable("values",self.get_all_values,priority=-5)
        self._add_status_variable("buffer_size",lambda: self.buffers_num)
        self._add_status_variable("read_frames",lambda: self.frame_counter)

    _p_connection_mode=interface.EnumParameterClass("connection_mode",{
        "controller":IMAQdxCameraControlMode.IMAQdxCameraControlModeController,
        "listener":IMAQdxCameraControlMode.IMAQdxCameraControlModeListener})
    _p_visibility=interface.EnumParameterClass("visibility",{
        "simple":IMAQdxAttributeVisibility.IMAQdxAttributeVisibilitySimple,
        "intermediate":IMAQdxAttributeVisibility.IMAQdxAttributeVisibilityIntermediate,
        "advanced":IMAQdxAttributeVisibility.IMAQdxAttributeVisibilityAdvanced})
    def open(self):
        """Open connection to the camera"""
        mode=self._p_connection_mode(self.mode)
        self.sid=lib.IMAQdxOpenCamera(self.name,mode)
    def close(self):
        """Close connection to the camera"""
        if self.sid is not None:
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

    _builtin_attrs=["OffsetX","OffsetY","Width","Height","PixelFormat","PayloadSize","StatusInformation::LastBufferNumber","AcquisitionAttributes::BitsPerPixel"]
    def list_attributes(self, root="", visibility=None, add_builtin=True):
        """
        List all attributes at a given root.

        Return list of :class:`IMAQdxAttribute` objects, which allow querying and settings values
        and getting additional information (description, limits, increment).
        """
        visibility=self._p_visibility(visibility or self.default_visibility)
        root=root.replace("/","::")
        attrs=lib.IMAQdxEnumerateAttributes2(self.sid,root,visibility)
        attr_names=[a.Name for a in attrs]
        if add_builtin:
            builtin_attrs=[]
            for a in self._builtin_attrs:
                if a not in attr_names:
                    try:
                        lib.IMAQdxGetAttributeDisplayName(self.sid,a)
                        builtin_attrs.append(a)
                    except IMAQdxError:
                        pass
            attr_names+=builtin_attrs
        return [IMAQdxAttribute(self.sid,a) for a in attr_names]

    def get_value(self, name, default=None):
        """Get value of the attribute with a given name"""
        name=name.replace("::","/")
        if (default is not None) and (name not in self.attributes):
            return default
        if self.attributes.is_dictionary(self.attributes[name]):
            return self.get_all_values(root=name)
        return self.attributes[name].get_value()
    def set_value(self, name, value, ignore_missing=False, truncate=True):
        """
        Set value of the attribute with a given name.
        
        If ``truncate==True``, truncate value to lie within attribute range.
        """
        name=name.replace("::","/")
        if (name in self.attributes) or (not ignore_missing):
            if self.attributes.is_dictionary(self.attributes[name]):
                self.set_all_values(value,root=name)
            else:
                self.attributes[name].set_value(value,truncate=truncate)

    def get_all_values(self, root="", as_dict=False):
        """
        Get values of all attributes with the given `root`.

        If ``as_dict==True``, return ``dict`` object; otherwise, return :class:`.Dictionary` object.
        """
        settings=self.attributes[root].copy().filter_self(lambda a: a.readable).map_self(lambda a: a.get_value())
        return settings.as_dict(style="flat") if as_dict else settings
    def set_all_values(self, settings, root="", truncate=True):
        """
        Set values of all attributes with the given `root`.
        
        If ``truncate==True``, truncate value to lie within attribute range.
        """
        settings=dictionary.as_dict(settings,style="flat",copy=False)
        for k in settings:
            if k in self.attributes[root] and self.attributes[root,k].writable: # pylint: disable=no-member
                self.attributes[root,k].set_value(settings[k],truncate=truncate) # pylint: disable=no-member

    def get_device_info(self):
        """
        Get camera information.

        Return tuple ``(vendor, model, serial_number, bus_type)``.
        """
        cam_info=self.v["CameraInformation"]
        serial="{:016X}".format((cam_info["SerialNumberHigh"]<<32)+cam_info["SerialNumberLow"])
        return TDeviceInfo(cam_info["VendorName"],cam_info["ModelName"],serial,cam_info["BusType"])

    def _get_data_dimensions_rc(self):
        return self.v["Height"],self.v["Width"]
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        return self.attributes["Width"].max,self.attributes["Height"].max # pylint: disable=no-member
    def get_roi(self):
        ox=self.v.get("OffsetX",0)
        oy=self.v.get("OffsetY",0)
        w=self.v["Width"]
        h=self.v["Height"]
        return ox,ox+w,oy,oy+h
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None):
        for a in ["Width","Height","OffsetX","OffsetY"]:
            if a not in self.attributes or not self.attributes[a].writable:
                return
        det_size=self.get_detector_size()
        if hend is None:
            hend=det_size[0]
        if vend is None:
            vend=det_size[1]
        with self.pausing_acquisition():
            self.v["Width"]=self.attributes["Width"].min # pylint: disable=no-member
            self.v["Height"]=self.attributes["Height"].min # pylint: disable=no-member
            self.v["OffsetX"]=hstart
            self.v["OffsetY"]=vstart
            self.v["Width"]=max(self.v["Width"],hend-hstart)
            self.v["Height"]=max(self.v["Height"],vend-vstart)
        return self.get_roi()
    def get_roi_limits(self):
        params=["OffsetX","OffsetY","Width","Height"]
        minp=tuple([(self.attributes[p].min if p in self.attributes else 0) for p in params])
        maxp=tuple([(self.attributes[p].max if p in self.attributes else 0) for p in params])
        min_roi=(0,minp[2],0,minp[3])
        max_roi=(maxp[0],maxp[2],maxp[1],maxp[3])
        return (min_roi,max_roi)
    

    @interface.use_parameters(mode="acq_mode")
    def setup_acquisition(self, mode="sequence", nframes=100):
        """
        Setup acquisition mode.

        `mode` can be either ``"snap"`` (since frame or sequency acquisition) or ``"sequence"`` (continuous acquisition).
        (note that :meth:`.IMAQdxCamera.acquisition_in_progress` would still return ``True`` in this case, even though new frames are no longer acquired).
        `nframes` sets up number of frame buffers.
        """
        self.clear_acquisition()
        super().setup_acquisition(mode=mode,nframes=nframes)
        lib.IMAQdxConfigureAcquisition(self.sid,mode=="sequence",nframes)
    def clear_acquisition(self):
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
        return self.v["StatusInformation/AcqInProgress"]
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
        last_buffer=self.v["StatusInformation/LastBufferNumber"]
        if last_buffer>=2**31:
            last_buffer=-1
        # newest_buffer=-1
        # try:
        #     newest_buffer=lib.IMAQdxGetImageData(self.sid,None,0,IMAQdxBufferNumberMode.IMAQdxBufferNumberModeLast,0)
        # except IMAQdxLibError as e:
        #     if e.code!=NIIMAQdx_lib.IMAQdxErrorCode.IMAQdxErrorCameraNotRunning:
        #         raise
        return last_buffer+1

    def _read_data_raw(self, size_bytes, dtype="<u1", mode=IMAQdxBufferNumberMode.IMAQdxBufferNumberModeBufferNumber, buffer_num=0):
        """Return raw bytes string from the given buffer number"""
        dtype=np.dtype(dtype)
        if size_bytes%dtype.itemsize:
            raise IMAQdxError("specified buffer size {} is not divisible by the element size {}".format(size_bytes,dtype.itemsize))
        arr=np.empty(size_bytes//dtype.itemsize,dtype)
        lib.IMAQdxGetImageData(self.sid,arr.ctypes.get_data(),size_bytes,mode,buffer_num)
        return self._convert_indexing(arr,"rct")

    def _read_frames(self, rng, return_info=False):
        indices=range(*rng)
        frames=[self._read_data_raw(b) for b in indices]
        return frames,list(indices)