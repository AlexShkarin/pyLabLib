from . import pfcam_lib
from .pfcam_lib import wlib as lib, PFCamError, PFCamLibError

from ..IMAQ.IMAQ import IMAQFrameGrabber
from ..SiliconSoftware.fgrab import SiliconSoftwareFrameGrabber
from ...core.utils import py3, dictionary
from ...core.devio.comm_backend import DeviceError
from ..interface import camera
from ..utils import load_lib

import numpy as np
import collections
import re
import warnings




class LibraryController(load_lib.LibraryController):
    def _do_preinit(self):
        super()._do_preinit()
        lib.pfPortInit()
libctl=LibraryController(lib)




def query_camera_name(port):
    """Query cameras name at a given port in PFCam interface"""
    libctl.preinit()
    try:
        lib.pfDeviceOpen(port)
        raw_name=lib.pfProperty_GetName(port,lib.pfDevice_GetRoot(port))
        value=py3.as_str(raw_name) if raw_name is not None else None
        lib.pfDeviceClose(port)
        return value
    except PFCamLibError:
        try:
            lib.pfDeviceClose(port)
        except PFCamLibError:
            pass
    return None
TCameraInfo=collections.namedtuple("TCameraInfo",["manufacturer","port","version","type"])
def list_cameras(only_supported=True):
    """
    List all cameras available through PFCam interface.
    
    If ``only_supported==True``, only return cameras which support PFCam protocol
    (this check only works if the camera is not currently accessed by some other software).
    Return a list ``[(port, info)]``, where ``port`` is the pfcam port given to :class:`IPhotonFocusCamera` and its subclasses,
    and ``info`` is the information returned by :func:`query_camera_name`.
    """
    libctl.preinit()
    ports=range(lib.pfPortInit())
    if only_supported:
        ports=[p for p in ports if query_camera_name(p) is not None]
    infos=[lib.pfPortInfo(p) for p in ports]
    infos=[TCameraInfo(py3.as_str(manu),py3.as_str(port),version,typ) for manu,port,version,typ in infos]
    return list(zip(ports,infos))
def get_cameras_number(only_supported=True):
    """Get the total number of connected PFCam cameras"""
    return len(list_cameras(only_supported=only_supported))
def get_port_index(manufacturer, port):
    """Find PhotonFocus port index based on the manufacturer and port"""
    cams=list_cameras(only_supported=False)
    for p,d in cams:
        if d.manufacturer==manufacturer and d.port==port:
            return p





class PFCamAttribute:
    """
    PFCam camera attribute.

    Allows to query and set values and get additional information.
    Usually created automatically by a PhotonFocus camera instance, but could also be created manually.

    Args:
        sid: camera session ID
        name: attribute text name

    Attributes:
        name: attribute name
        kind: attribute kind; can be ``"INT"``, ``"UINT"``, ``"FLOAT"``, ``"BOOL"``, ``"MODE"``, ``"STRING"``, or ``"COMMAND"``
        readable (bool): whether attribute is readable
        writable (bool): whether attribute is writable
        is_command (bool): whether attribute is a command
        min (float or int): minimal attribute value (if applicable)
        max (float or int): maximal attribute value (if applicable)
        ivalues: list of possible integer values for enum attributes
        values: list of possible text values for enum attributes
        labels: dict ``{label: index}`` which shows all possible values of an enumerated attribute and their corresponding numerical values
        ilabels: dict ``{index: label}`` which shows labels corresponding to numerical values of an enumerated attribute
    """
    def __init__(self, port, name):
        self.port=port
        self.name=py3.as_str(name)
        self._token=lib.pfProperty_ParseName(port,self.name)
        if self._token==pfcam_lib.PfInvalidToken:
            raise PFCamError("attribute {} doesn't exist".format(name))
        self._type=lib.get_ptype_name(port,lib.pfProperty_GetType(port,self._token))
        if self._type not in pfcam_lib.ValuePropertyTypes|{"PF_COMMAND"}:
            raise PFCamError("attribute type {} not supported".format(self._type))
        self.kind=self._type[3:]
        self._flags=lib.pfProperty_GetFlags(port,self._token)
        if self._flags&0x02:
            raise PFCamError("attribute {} is private".format(self.name))
        self.is_command=self._type=="PF_COMMAND"
        self.readable=not (self._flags&0x20 or self.is_command)
        self.writable=not (self._flags&0x10 or self.is_command)
        if self._type in {"PF_INT","PF_UINT","PF_FLOAT"}:
            self.min=lib.get_property_by_name(port,self.name+".Min")
            self.max=lib.get_property_by_name(port,self.name+".Max")
        else:
            self.min=self.max=None
        self.values=[]
        self.ivalues=[]
        self.labels={}
        self.ilabels={}
        if self._type=="PF_MODE":
            self._update_enum_limits()
    
    def _update_enum_limits(self):
        nodes=lib.collect_properties(self.port,self._token,backbone=False)
        for tok,val in nodes:
            val=py3.as_str(val)
            if lib.pfProperty_GetType(self.port,tok)==2: # integer token, means one of possible values
                ival=lib.pfDevice_GetProperty(self.port,tok)
                self.values.append(val)
                self.ivalues.append(ival)
        self.labels=dict(zip(self.values,self.ivalues))
        self.ilabels=dict(zip(self.ivalues,self.values))
    def update_limits(self):
        """Update minimal and maximal attribute limits and return tuple ``(min, max)``"""
        if self._type in {"PF_INT","PF_UINT","PF_FLOAT"}:
            self.min=lib.get_property_by_name(self.port,self.name+".Min")
            self.max=lib.get_property_by_name(self.port,self.name+".Max")
            return (self.min,self.max)
        if self._type=="PF_MODE":
            self._update_enum_limits()
    def truncate_value(self, value):
        """Truncate value to lie within attribute limits"""
        self.update_limits()
        if self.min is not None and value<self.min:
            value=self.min
        if self.max is not None and value>self.max:
            value=self.max
        return value

    def get_value(self, enum_as_str=True):
        """
        Get attribute value.
        
        If ``enum_as_str==True``, return enum-style values as strings; otherwise, return corresponding integer values.
        """
        if not self.readable:
            raise PFCamError("attribute {} is not readable".format(self.name))
        val=lib.pfDevice_GetProperty(self.port,self._token)
        if self._type=="PF_MODE" and enum_as_str:
            val=self.ilabels[val]
        return val
    def set_value(self, value, truncate=True):
        """
        Get attribute value.
        
        If ``truncate==True``, automatically truncate value to lie within allowed range.
        """
        if not self.writable:
            raise PFCamError("attribute {} is not writable".format(self.name))
        if truncate:
            value=self.truncate_value(value)
        if isinstance(value,py3.anystring) and self._type=="PF_MODE":
            value=self.labels[value]
        for t in range(2):
            try:
                lib.pfDevice_SetProperty(self.port,self._token,value)
            except PFCamLibError as err:
                if not (truncate and t==0 and err.code==-994): # parameter out of range (some version of pfcam library raise an error once if value is too close to the allowed edge)
                    raise
        return self.get_value()
    def call_command(self, arg=0):
        """If attribute is a command, call it with a given argument; otherwise, raise an error"""
        if not self.is_command:
            raise PFCamError("{} is not of PF_COMMAND type".format(self.name))
        lib.pfDevice_SetProperty(self.port,self._token,arg)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,self.name)







TDeviceInfo=collections.namedtuple("TDeviceInfo",["model","serial_number","grabber_info"])
class IPhotonFocusCamera(camera.IAttributeCamera): # pylint: disable=abstract-method
    """
    Generic PFCam interface to a PhotonFocus camera.
    Does not handle frames acquisition, so needs to be mixed with a frame grabber class to be fully operational.
    In this mixing, the class attribute ``GrabberClass`` should be set to this frame grabber class.

    Args:
        pfcam_port: port number for pfcam interface (can be learned by :func:`list_cameras`; port number is the first element of the camera data tuple)
            can also be a tuple ``(manufacturer, port)``, e.g., ``("National Instruments", "port0")``.
        kwargs: keyword arguments passed to the frame grabber initialization
    """
    Error=DeviceError
    GrabberClass=None
    def __init__(self, pfcam_port=0, **kwargs):
        if isinstance(pfcam_port,tuple):
            pfcam_port=get_port_index(*pfcam_port)
        self.pfcam_port=pfcam_port
        self.pfcam_opened=False
        self.ucav=dictionary.ItemAccessor(self.get_attribute_value,self.update_attribute_value)
        super().__init__(do_open=False,**kwargs)

        self._add_status_variable("baudrate",self.get_baudrate)
        self._add_settings_variable("trigger_interleave",self.get_trigger_interleave,self.set_trigger_interleave)
        self._add_settings_variable("cfr",self.is_CFR_enabled,self.enable_CFR)
        self._add_settings_variable("status_line",self.is_status_line_enabled,self.enable_status_line)
        self._add_settings_variable("bl_offset",self.get_black_level_offset,self.set_black_level_offset)
        self._add_settings_variable("exposure",self.get_exposure,self.set_exposure)
        self._add_settings_variable("frame_period",self.get_frame_period,self.set_frame_period)
        self._add_status_variable("frame_timings",self.get_frame_timings)
    
        self.open()
    
    def setup_max_baudrate(self):
        """Setup the maximal available baudrate"""
        brs=[921600,460800,230400,115200,57600,38400,19200,9600,4800,2400,1200]
        try:
            for br in brs:
                if lib.pfIsBaudRateSupported(self.pfcam_port,br):
                    lib.pfSetBaudRate(self.pfcam_port,br)
                    return
        except PFCamLibError: # pfSetBaudRate sometimes raises unknown error
            pass
    def get_baudrate(self):
        """Get the current baud rate"""
        return lib.pfGetBaudRate(self.pfcam_port)
    def open(self):
        """Open connection to the camera"""
        super().open()
        try:
            libctl.preinit()
            if not self.pfcam_opened:
                lib.pfDeviceOpen(self.pfcam_port)
                self.pfcam_opened=True
                self.setup_max_baudrate()
                self._update_attributes()
                self._update_grabber_roi()
                self._hstep=self._get_roi_step("h")
                self._vstep=self._get_roi_step("v")
        except self.Error:
            super().close()
            raise
    def close(self):
        """Close connection to the camera"""
        super().close()
        if self.pfcam_opened:
            lib.pfDeviceClose(self.pfcam_port)
            self.pfcam_opened=False
    def _get_connection_parameters(self):
        grabber_params=(self.GrabberClass._get_connection_parameters(self),) if self.GrabberClass else ()
        return (self.pfcam_port,)+grabber_params

    def _normalize_attribute_name(self, name):
        return name.replace(".","/")
    def _list_attributes(self):
        root=lib.pfDevice_GetRoot(self.pfcam_port)
        props=lib.collect_properties(self.pfcam_port,root,include_types=pfcam_lib.ValuePropertyTypes|{"PF_COMMAND"})
        pfprops=[]
        for (_,name) in props:
            try:
                pfprops.append(PFCamAttribute(self.pfcam_port,name))
            except PFCamError:
                pass
        return pfprops

    def get_attribute_value(self, name, enum_as_str=True, error_on_missing=True, default=None):  # pylint: disable=arguments-differ
        """
        Get value of an attribute with the given name.
        
        If the value doesn't exist or can not be read and ``error_on_missing==True``, raise error; otherwise, return `default`.
        If `default` is not ``None``, assume that ``error_on_missing==False``.
        If ``enum_as_str==True``, try to represent enums as their string values;
        If `name` points at a dictionary branch, return a dictionary with all values in this branch.
        """
        return super().get_attribute_value(name,enum_as_str=enum_as_str,error_on_missing=error_on_missing,default=default)
    def set_attribute_value(self, name, value, truncate=True, error_on_missing=True):  # pylint: disable=arguments-differ
        """
        Set value of an attribute with the given name.
        
        If the value doesn't exist or can not be written and ``error_on_missing==True``, raise error; otherwise, do nothing.
        If `name` points at a dictionary branch, set all values in this branch (in this case `value` must be a dictionary).
        If ``truncate==True``, truncate value to lie within attribute range.
        """
        return super().set_attribute_value(name,value,truncate=truncate,error_on_missing=error_on_missing)
    def get_all_attribute_values(self, root="", enum_as_str=True):  # pylint: disable=arguments-differ
        """Get values of all attributes with the given `root`"""
        return super().get_all_attribute_values(root=root,enum_as_str=enum_as_str)
    def set_all_attribute_values(self, settings, root="", truncate=True):  # pylint: disable=arguments-differ
        """
        Set values of all attributes with the given `root`.
        
        If ``truncate==True``, truncate value to lie within attribute range.
        """
        return super().set_all_attribute_values(settings,root=root,truncate=truncate)
    def update_attribute_value(self, name, value, error_on_missing=True, truncate=True):
        """
        Set value of the attribute with a given name, but only if it's different from the current value.
        
        Can take less time on some version of PFRemote (where single attribute setting is about 50ms).
        Arguments are the same as :meth:`set_attribute_value`.
        """
        if self.get_attribute_value(name)!=value:
            self.set_attribute_value(name,value,error_on_missing=error_on_missing,truncate=truncate)
    def call_command(self, name, arg=0, error_on_missing=True):
        """
        Execute the given command with the given argument.
        
        If the command doesn't exist and ``error_on_missing==True``, raise error; otherwise, do nothing.
        """
        attr=self.get_attribute(name,error_on_missing=error_on_missing)
        if attr:
            attr.call_command(arg=arg)


    def get_device_info(self):
        """
        Get camera model data.

        Return tuple ``(model, serial_number, grabber_info)``.
        """
        model=py3.as_str(lib.pfProperty_GetName(self.pfcam_port,lib.pfDevice_GetRoot(self.pfcam_port)))
        serial_number=self.get_attribute_value("Header/Serial",default=0)
        grabber_info=tuple(self.GrabberClass.get_device_info(self)) if self.GrabberClass else None
        return TDeviceInfo(model,serial_number,grabber_info)


    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        return self.ca["Window/W"].max,self.ca["Window/H"].max # pylint: disable=no-member
    def _get_pf_data_dimensions_rc(self):
        return self.cav["Window/H"],self.cav["Window/W"]
    def _update_grabber_roi(self):
        if self.GrabberClass:
            r,c=self._get_pf_data_dimensions_rc()
            self.GrabberClass.set_roi(self,0,c,0,r)
    def get_roi(self):
        """
        Get current ROI.

        Return tuple ``(hstart, hend, vstart, vend)``.
        """
        ox=self.get_attribute_value("Window/X",default=0)
        oy=self.get_attribute_value("Window/Y",default=0)
        w=self.cav["Window/W"]
        h=self.cav["Window/H"]
        return ox,ox+w,oy,oy+h
    def fast_shift_roi(self, hstart=0, vstart=0):
        """
        Shift ROI by only changing its origin, but keeping the shape the same.

        Note that if the ROI is invalid, it won't be truncated (as is the standard behavior of :meth:`set_roi`), which might lead to errors later.
        """
        self.cav["Window/X"]=hstart
        self.cav["Window/Y"]=vstart
    def _get_roi_step(self, kind="h"):
        sname="Window/"+("W" if kind=="h" else "H")
        sprop=self.ca[sname]
        sprop.update_limits()
        pname="Window/"+("X" if kind=="h" else "Y")
        pprop=self.get_attribute(pname,error_on_missing=False)
        if pprop is None:
            return sprop.max
        sprev=sprop.get_value()
        pprev=pprop.get_value()
        sprop.set_value(0)
        step=None
        v=1
        while v<=sprop.min and v+sprop.min<sprop.max:
            if pprop.set_value(v)==v:
                step=v
                break
            v*=2
        pprop.set_value(pprev)
        sprop.set_value(sprev)
        return sprop.max if step is None else step
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None):
        """
        Setup camera ROI.

        By default, all non-supplied parameters take extreme values.
        """
        for a in ["Window/X","Window/Y","Window/W","Window/H"]:
            attr=self.get_attribute(a,error_on_missing=False)
            if attr is None or not attr.writable:
                return
        det_size=self.get_detector_size()
        if self.GrabberClass:
            grabber_detector_size=self.GrabberClass.get_detector_size(self)
        else:
            grabber_detector_size=det_size
        if hend is None:
            hend=det_size[0]
        if vend is None:
            vend=det_size[1]
        self.ucav["Window/W"]=min(hend-hstart,grabber_detector_size[0])
        self.ucav["Window/H"]=min(vend-vstart,grabber_detector_size[1])
        self.ucav["Window/X"]=hstart
        self.ucav["Window/Y"]=vstart
        self.ucav["Window/W"]=min(hend-hstart,grabber_detector_size[0]) # in case the previous assignment truncated
        self.ucav["Window/H"]=min(vend-vstart,grabber_detector_size[1])
        self._update_grabber_roi()
        return self.get_roi()
    def get_roi_limits(self, hbin=1, vbin=1): # pylint: disable=unused-argument
        params=[self.ca[p] for p in ["Window/W","Window/H"]]
        minp,maxp=[list(p) for p in zip(*[p.update_limits() for p in params])]
        hlim=camera.TAxisROILimit(minp[0],maxp[0],self._hstep,minp[0],1)
        vlim=camera.TAxisROILimit(minp[1],maxp[1],self._vstep,minp[1],1)
        return hlim,vlim

    def _get_buffer_bpp(self):
        bpp=self.GrabberClass._get_buffer_bpp(self) if self.GrabberClass else 1
        ppbpp=self._get_camera_bytepp()
        if ppbpp is not None:
            bpp=(ppbpp-1)//8+1
        return bpp
    def _get_camera_bytepp(self):
        fmt=self.get_attribute_value("DataResolution",error_on_missing=False)
        if fmt is None:
            return None
        m=re.match(r"(?:res)?(\d+)bit",fmt.lower())
        if m:
            return int(m[1])
        return None
    def _set_camera_bytepp(self, bpp):
        fmt=self.get_attribute_value("DataResolution",error_on_missing=False)
        if fmt:
            m=re.match(r"^([^\d]*)(\d+)([^\d]*)$",fmt)
            if m:
                fmt="{}{}{}".format(m[1],bpp,m[3])
                self.cav["DataResolution"]=fmt
    def _get_data_dimensions_rc(self):
        roi=self.get_roi()
        w,h=roi[1]-roi[0],roi[3]-roi[2]
        return h,w

    def get_exposure(self):
        """Get current exposure"""
        return self.cav["ExposureTime"]*1E-3
    def set_exposure(self, exposure):
        """Set current exposure"""
        self.cav["ExposureTime"]=exposure*1E3
        return self.get_exposure()

    def get_frame_period(self):
        """Get frame period (time between two consecutive frames in the internal trigger mode)"""
        attr=self.get_attribute("FrameTime",error_on_missing=False)
        if attr:
            return attr.get_value()*1E-3
        else:
            return 1./float(self.cav["FrameRate"])
    def set_frame_period(self, frame_period):
        """Set frame period (time between two consecutive frames in the internal trigger mode)"""
        self.set_attribute_value("FrameTime",frame_period*1E3,error_on_missing=False)
        return self.get_frame_period()
    _TAcqTimings=camera.TAcqTimings
    def get_frame_timings(self):
        """
        Get acquisition timing.

        Return tuple ``(exposure, frame_period)``.
        """
        return self._TAcqTimings(self.get_exposure(),self.get_frame_period())

    def is_CFR_enabled(self):
        """Check if the constant frame rate mode is enabled"""
        return self.get_attribute_value("Trigger/CFR",default=False)
    def enable_CFR(self, enabled=True):
        """Enable constant frame rate mode"""
        self.set_attribute_value("Trigger/CFR",enabled,error_on_missing=False)
        return self.is_CFR_enabled()

    def get_trigger_interleave(self):
        """Check if the trigger interleave is on"""
        return self.get_attribute_value("Trigger/Interleave",default=False)
    def set_trigger_interleave(self, enabled):
        """Set the trigger interleave option on or off"""
        if self.get_trigger_interleave()!=enabled:
            if self.is_CFR_enabled():
                ft=self.get_frame_period()
                self.enable_CFR(False)
                self.set_attribute_value("Trigger/Interleave",enabled,error_on_missing=False)
                self.enable_CFR(True)
                self.set_frame_period(ft)
            else:
                self.set_attribute_value("Trigger/Interleave",enabled,error_on_missing=False)
        return self.get_trigger_interleave()

    def is_status_line_enabled(self):
        """Check if the status line is on"""
        return self.get_attribute_value("EnStatusLine",default=False)
    def enable_status_line(self, enabled=True):
        """Enable or disable status line"""
        self.set_attribute_value("EnStatusLine",enabled,error_on_missing=False)
        return self.is_status_line_enabled()

    def get_black_level_offset(self):
        """Get the black level offset"""
        return self.get_attribute_value("Voltages/BlackLevelOffset",default=0)
    def set_black_level_offset(self, offset):
        """Set the black level offset"""
        self.set_attribute_value("Voltages/BlackLevelOffset",offset,error_on_missing=False)
        return self.get_black_level_offset()






class PhotonFocusIMAQCamera(IPhotonFocusCamera,IMAQFrameGrabber):
    """
    IMAQ+PFCam interface to a PhotonFocus camera.

    Args:
        imaq_name: IMAQ interface name (can be learned by :func:`.IMAQ.list_cameras`; usually, but not always, starts with ``"img"``)
        pfcam_port: port number for pfcam interface (can be learned by :func:`list_cameras`; port number is the first element of the camera data tuple)
            can also be a tuple ``(manufacturer, port)``, e.g., ``("National Instruments", "port0")``.
    """
    Error=DeviceError
    GrabberClass=IMAQFrameGrabber
    def __init__(self, imaq_name="img0", pfcam_port=0):
        super().__init__(pfcam_port=pfcam_port,name=imaq_name)

    def open(self):
        super().open()
        self._ensure_pixel_format()

    def _ensure_pixel_format(self):
        fgbpp=self.get_grabber_attribute_value("BITSPERPIXEL")
        ppbpp=self._get_camera_bytepp()
        if ppbpp is not None and ppbpp!=fgbpp:
            msg=(   "PhotonFocus pixel format {} does not agree with the frame grabber {} bits per pixel; "
                    "changing PhotonFocus pixel format accordingly; to use the original format, alter the camera file".format(self.cav["DataResolution"],fgbpp))
            warnings.warn(msg)
            self._set_camera_bytepp(fgbpp)



class PhotonFocusSiSoCamera(IPhotonFocusCamera,SiliconSoftwareFrameGrabber):
    """
    IMAQ+PFCam interface to a PhotonFocus camera.

    Args:
        siso_board: Silicon Software board index, starting from 0; available boards can be learned by :func:`.fgrab.list_boards`
        siso_applet: Silicon Software applet name, which can be learned by :func:`.fgrab.list_applets`;
            usually, a simple applet like ``"DualLineGray16"`` or ``"MediumLineGray16`` are most appropriate;
            can be either an applet name, or a direct path to the applet DLL
        siso_port: Silicon Software port number, if several ports are supported by the camera and the applet
        pfcam_port: port number for pfcam interface (can be learned by :func:`list_cameras`; port number is the first element of the camera data tuple)
            can also be a tuple ``(manufacturer, port)``, e.g., ``("National Instruments", "port0")``.
    """
    Error=DeviceError
    GrabberClass=SiliconSoftwareFrameGrabber
    def __init__(self, siso_board, siso_applet, siso_port=0, pfcam_port=0):
        super().__init__(pfcam_port=pfcam_port,siso_board=siso_board,siso_applet=siso_applet,siso_port=siso_port)

    def open(self):
        super().open()
        self._ensure_pixel_format()

    def _ensure_pixel_format(self):
        ppbpp=self._get_camera_bytepp()
        if ppbpp is not None:
            self.setup_camlink_pixel_format(ppbpp,2)



def check_grabber_association(cam):
    """
    Check if PhotonFocus camera has correct association between the frame grabber and the PFRemote interface.
    
    `cam` should be an opened instance of :class:`PhotonFocusIMAQCamera` or :class:`PhotonFocusSiSoCamera`.
    Note that this function changes camera parameters such as exposure, frame period, ROI, trigger source, and status line.
    """
    try:
        if hasattr(cam,"gav") and "CAMSTATUS" in cam.gav and not cam.gav["CAMSTATUS"]:
            return False
        cam.clear_acquisition()
        cam.set_exposure(0)
        cam.set_frame_period(0)
        try:
            cam.clear_all_triggers()
        except AttributeError:
            pass
        cam.cav["Trigger/Source"]=0
        cam.set_roi(0,64,0,64)
        cam.enable_status_line()
        img=cam.snap(timeout=1)
        if get_status_lines(img) is None:
            return False
        cam.enable_status_line(False)
        img=cam.snap(timeout=1)
        if get_status_lines(img) is not None:
            return False
        return True
    except cam.Error:
        return False

##### Dealing with status line #####

_status_line_magic=0x55AA00FF
def _check_magic(line):
    """Check if the status line satisfies the magic 4-byte requirement"""
    if line.ndim==1:
        return line[0]==_status_line_magic
    else:
        return np.all(line[:,0]==_status_line_magic)
def _extract_line(frames, preferred_line=True):
    lsz=min(frames.shape[-1]//4,6)
    if frames.ndim==2:
        if (frames.shape[1]>=36) == preferred_line:
            return np.frombuffer(frames[-1,:lsz*4].astype("<u1").tobytes(),"<u4") if frames.shape[0]>0 else np.zeros((lsz,1))
        else:
            return np.frombuffer(frames[-2,:lsz*4].astype("<u1").tobytes(),"<u4") if frames.shape[0]>1 else np.zeros((lsz,1))
    else:
        if (frames.shape[2]>=36) == preferred_line:
            return np.frombuffer((frames[:,-1,:lsz*4].astype("<u1").tobytes()),"<u4").reshape((-1,lsz)) if frames.shape[1]>0 else np.zeros((len(frames),lsz,1))
        else:
            return np.frombuffer((frames[:,-2,:lsz*4].astype("<u1").tobytes()),"<u4").reshape((-1,lsz)) if frames.shape[1]>1 else np.zeros((len(frames),lsz,1))
def get_status_lines(frames, check_transposed=True, drop_magic=True):
    """
    Extract status lines (up to first 6 entries) from the given frames.
    
    `frames` can be 2D array (one frame), 3D array (stack of frames, first index is frame number), or list of 1D or 2D arrays.
    Automatically check if the status line is present; return ``None`` if it's not.
    If ``check_transposed==True``, check for the case where the image is transposed (i.e., line becomes a column).
    If ``drop_magic==True``, remove the first status line entry, which is simply a special number marking the status line presence.
    Return a 1D or 2D numpy array, where the first axis (if present) is the frame number, and the last is the status line entry
    The entries after the magic are the frame index, timestamp (in us), missed trigger counters (up to 255),
    average frame value, and the integration time (in pixel clock cycles, which depend on the camera).
    """
    if isinstance(frames,list):
        return [get_status_lines(f,check_transposed=check_transposed,drop_magic=drop_magic) for f in frames]
    if frames.shape[-1]>=4:
        s=1 if drop_magic else 0
        lines=_extract_line(frames,True)
        if _check_magic(lines):
            return lines[...,s:]
        lines=_extract_line(frames,False)
        if _check_magic(lines):
            return lines[...,s:]
    if check_transposed:
        tframes=frames.T if frames.ndim==2 else frames.transpose((0,2,1))
        return get_status_lines(tframes,check_transposed=False,drop_magic=drop_magic)
    return None
def get_status_line_position(frame, check_transposed=True):
    """
    Check whether status line is present in the frame, and return its location.
    
    Return tuple ``(row, transposed)``, where `row` is the status line row (can be ``-1`` or ``-2``)
    and `transposed` is ``True`` if the line is present in the transposed image.
    If no status line is found, return ``None``.
    If ``check_transposed==True``, check for the case where the image is transposed (i.e., line becomes a column).
    """
    if frame.shape[-1]>=4:
        line=_extract_line(frame,True)
        if _check_magic(line):
            return (-1 if frame.shape[1]>=36 else -2),False
        lines=_extract_line(frame,False)
        if _check_magic(lines):
            return (-2 if frame.shape[1]>=36 else -1),False
    if check_transposed:
        res=get_status_line_position(frame.T,check_transposed=False)
        if res:
            return res[0],True
    return None

def remove_status_line(frame, sl_pos="calculate", policy="duplicate", copy=True):
    """
    Remove status line from the frame.
    
    Args:
        frame: a frame to process (2D or 3D numpy array; if 3D, the first axis is the frame number)
        sl_pos: status line position (returned by :func:`get_status_line_position`); if equal to ``"calculate"``, calculate here;
            for a 3D array, assumed to be the same for all frames
        policy: determines way to deal with the status line;
            can be ``"keep"`` (keep as is), ``"cut"`` (cut off the status line row), ``"zero"`` (set it to zero),
            ``"median"`` (set it to the image median), or ``"duplicate"`` (set it equal to the previous row; default)
        copy: if ``True``, make copy of the original frames; otherwise, attempt to remove the line in-place
    """
    if sl_pos=="calculate":
        sl_pos=get_status_line_position(frame) if frame.ndim==2 else get_status_line_position(frame[0])
    if sl_pos and policy!="keep":
        if copy:
            frame=frame.copy()
        if frame.ndim==2:
            if sl_pos[1]:
                frame=frame.T
            if policy=="median":
                frame[sl_pos[0]:,:]=np.median(frame[:,:sl_pos[0]]) if frame.shape[0]>abs(sl_pos[0]) else 0
            elif policy=="zero":
                frame[sl_pos[0]:,:]=0
            elif policy=="cut":
                frame=frame[:sl_pos[0],:]
            else:
                frame[sl_pos[0]:,:]=frame[sl_pos[0]-1,:].reshape((1,-1)) if frame.shape[0]>abs(sl_pos[0]) else 0
            if sl_pos[1]:
                frame=frame.T
        else:
            if sl_pos[1]:
                frame=frame.transpose((0,2,1))
            if policy=="median":
                frame[:,sl_pos[0]:,:]=np.median(frame[:,:sl_pos[0],:],axis=(1,2)).reshape((-1,1,1)) if frame.shape[1]>abs(sl_pos[0]) else 0
            elif policy=="zero":
                frame[:,sl_pos[0]:,:]=0
            elif policy=="cut":
                frame=frame[:,:sl_pos[0],:]
            else:
                frame[:,sl_pos[0]:,:]=frame[:,sl_pos[0]-1,:].reshape((len(frame),1,-1)) if frame.shape[1]>abs(sl_pos[0]) else 0
            if sl_pos[1]:
                frame=frame.transpose((0,2,1))
    return frame


def find_skipped_frames(lines, step=1):
    """
    Check if there are skipped frames based on status line reading.

    `step` specifies expected index step between neighboring frames.

    Return list ``[(idx, skipped)]``, where `idx` is the index after which `skipped` frames were skipped.
    """
    dfs=(lines[1:,0]-lines[:-1,0])%(2**24) # the internal counter is only 24-bit
    skipped_idx=(dfs!=step)
    skipped_idx=skipped_idx.nonzero()[0]
    return list(zip(skipped_idx,dfs[skipped_idx])) if len(skipped_idx) else []


class StatusLineChecker(camera.StatusLineChecker):
    def get_framestamp(self, frames):
        lines=get_status_lines(frames,check_transposed=False)
        return None if lines is None or lines.shape[-1]<1 else lines[...,0].astype("i4")
    def _prepare_dfs(self, dfs):
        return (dfs+2**23)%2**24-2**23