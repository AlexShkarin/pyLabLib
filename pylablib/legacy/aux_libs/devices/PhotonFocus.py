from ...core.utils import dictionary, py3, general
from ...core.devio import data_format, interface
from ...core.dataproc import image as image_utils

import numpy as np
import contextlib
import time
import collections
import re

from .IMAQdx import IMAQdxPhotonFocusCamera as PhotonFocusIMAQdxCamera
from .IMAQ import IMAQCamera, IMAQError, lib as IMAQ_lib
from . import pfcam_lib
lib=pfcam_lib.lib
try:
    lib.initlib()
except (ImportError, OSError):
    pass
PfcamError=pfcam_lib.PfcamLibError
class PFGenericError(RuntimeError):
    "Generic IMAQ camera error."

_depends_local=[".pfcam_lib",".IMAQ",".IMAQdx","...core.devio.interface"]

class PfcamProperty(object):
    """
    Object representing a pfcam camera property.

    Allows to query and set values and get additional information.
    Usually created automatically by an :class:`PhotonFocusIMAQCamera` instance, but could be created manually.

    Attributes:
        name: attribute name
        readable (bool): whether property is readable
        writable (bool): whether property is writable
        is_command (bool): whether property is a command
        min (float or int): minimal property value (if applicable)
        max (float or int): maximal property value (if applicable)
        values: list of possible property values (if applicable)
    """
    def __init__(self, port, name):
        object.__init__(self)
        self.port=port
        self.name=py3.as_str(name)
        self._token=lib.pfProperty_ParseName(port,self.name)
        if self._token==pfcam_lib.PfInvalidToken:
            raise PFGenericError("property {} doesn't exist".format(name))
        self._type=pfcam_lib.lib.get_ptype_dicts(port)[0][lib.pfProperty_GetType(port,self._token)]
        if self._type not in pfcam_lib.ValuePropertyTypes|{"PF_COMMAND"}:
            raise PFGenericError("property type {} not supported".format(self._type))
        self._flags=lib.pfProperty_GetFlags(port,self._token)
        if self._flags&0x02:
            raise PFGenericError("property {} is private".format(self.name))
        self.is_command=self._type=="PF_COMMAND"
        self.readable=not (self._flags&0x20 or self.is_command)
        self.writable=not (self._flags&0x10 or self.is_command)
        if self._type in {"PF_INT","PF_UINT","PF_FLOAT"}:
            self.min=lib.get_property_by_name(port,self.name+".Min")
            self.max=lib.get_property_by_name(port,self.name+".Max")
        else:
            self.min=self.max=None
        if self._type=="PF_MODE":
            self._values_dict={}
            self._values_dict_inv={}
            nodes=lib.collect_properties(port,self._token,backbone=False)
            for tok,val in nodes:
                val=py3.as_str(val)
                if lib.pfProperty_GetType(port,tok)==2: # integer token, means one of possible values
                    ival=lib.pfDevice_GetProperty(port,tok)
                    self._values_dict[val]=ival
                    self._values_dict_inv[ival]=val
            self.values=list(self._values_dict)
        else:
            self._values_dict=self._values_dict_inv={}
            self.values=None
    
    def update_minmax(self):
        """Update minimal and maximal property limits"""
        if self._type in {"PF_INT","PF_UINT","PF_FLOAT"}:
            self.min=lib.get_property_by_name(self.port,self.name+".Min")
            self.max=lib.get_property_by_name(self.port,self.name+".Max")
    def truncate_value(self, value):
        """Truncate value to lie within property limits"""
        self.update_minmax()
        if self.min is not None and value<self.min:
            value=self.min
        if self.max is not None and value>self.max:
            value=self.max
        return value

    def get_value(self, enum_as_str=True):
        """
        Get property value.
        
        If ``enum_as_str==True``, return enum-style values as strings; otherwise, return corresponding integer values.
        """
        if not self.readable:
            raise PFGenericError("property {} is not readable".format(self.name))
        val=lib.pfDevice_GetProperty(self.port,self._token)
        if self._type=="PF_MODE" and enum_as_str:
            val=self._values_dict_inv[val]
        return val
    def set_value(self, value, truncate=True):
        """
        Get property value.
        
        If ``truncate==True``, automatically truncate value to lie within allowed range.
        """
        if not self.writable:
            raise PFGenericError("property {} is not writable".format(self.name))
        if truncate:
            value=self.truncate_value(value)
        if isinstance(value,py3.anystring) and self._type=="PF_MODE":
            value=self._values_dict[value]
        lib.pfDevice_SetProperty(self.port,self._token,value)
        return self.get_value()
    def call_command(self, arg=0):
        """If property is a command, call it with a given argument; otherwise, raise an error."""
        if not self.is_command:
            raise PFGenericError("{} is not a PF_COMMAND property".format(self.name))
        lib.pfDevice_SetProperty(self.port,self._token,arg)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,self.name)







def query_camera_name(port):
    """Query cameras name at a given port in pfcam interface"""
    lib.pfPortInit()
    try:
        lib.pfDeviceOpen(port)
        raw_name=lib.pfProperty_GetName(port,lib.pfDevice_GetRoot(port))
        value=py3.as_str(raw_name) if raw_name is not None else None
        lib.pfDeviceClose(port)
        return value
    except PfcamError:
        try:
            lib.pfDeviceClose(port)
        except PfcamError:
            pass
    return None
def list_cameras(supported=False):
    """
    List all cameras available through pfcam interface
    
    If ``supported==True``, only return cameras which support pfcam protocol.
    """
    ports=range(lib.pfPortInit())
    if supported:
        ports=[p for p in ports if query_camera_name(p) is not None]
    return [(p,lib.pfPortInfo(p)) for p in ports]







class PhotonFocusIMAQCamera(IMAQCamera):
    """
    IMAQ+PFcam interface to a PhotonFocus camera.

    Args:
        imaq_name: IMAQ interface name (can be learned by :func:`.IMAQ.list_cameras`; usually, but not always, starts with ``"img"``)
        pfcam_port: port number for pfcam interface (can be learned by :func:`list_cameras`; port number is the first element of the camera data tuple)
    """
    def __init__(self, imaq_name="img0", pfcam_port=0):
        self.pfcam_port=pfcam_port
        self.pfcam_opened=False
        self.v=dictionary.ItemAccessor(self.get_value,self.set_value)
        try:
            IMAQCamera.__init__(self,imaq_name)
        except Exception:
            self.close()
            raise

        self._add_full_info_node("model_data",self.get_model_data)
        self._add_full_info_node("interface_name",lambda: self.name)
        self._add_full_info_node("pfcam_port",lambda: self.pfcam_port)
        self._add_status_node("properties",self.get_all_properties)
        self._add_settings_node("trigger_interleave",self.get_trigger_interleave,self.set_trigger_interleave)
        self._add_settings_node("cfr",self.is_CFR_enabled,self.enable_CFR)
        self._add_settings_node("status_line",self.is_status_line_enabled,self.enable_status_line)
        self._add_settings_node("bl_offset",self.get_black_level_offset,self.set_black_level_offset)
        self._add_settings_node("exposure",self.get_exposure,self.set_exposure)
        self._add_settings_node("frame_time",self.get_frame_time,self.set_frame_time)
    
    def setup_max_baudrate(self):
        brs=[115200,57600,38400,19200,9600,4800,2400,1200]
        try:
            for br in brs:
                if lib.pfIsBaudRateSupported(self.pfcam_port,br):
                    lib.pfSetBaudRate(self.pfcam_port,br)
                    return
        except PfcamError: # pfSetBaudRate sometimes raises unknown error
            pass
    def open(self):
        """Open connection to the camera"""
        IMAQCamera.open(self)
        if not self.pfcam_opened:
            lib.pfPortInit()
            lib.pfDeviceOpen(self.pfcam_port)
            self.pfcam_opened=True
            self.setup_max_baudrate()
            self.properties=dictionary.Dictionary(dict([ (p.name.replace(".","/"),p) for p in self.list_properties() ]))
            self._update_imaq()
    def close(self):
        """Close connection to the camera"""
        IMAQCamera.close(self)
        if self.pfcam_opened:
            lib.pfDeviceClose(self.pfcam_port)
            self.pfcam_opened=False

    def post_open(self):
        """Action to automatically call on opening"""
        pass

    def list_properties(self, root=""):
        """
        List all properties at a given root.

        Return list of :class:`PfcamProperty` objects, which allow querying and settings values
        and getting additional information (limits, values).
        """
        root=root.replace("/",".")
        pfx=root
        if root=="":
            root=lib.pfDevice_GetRoot(self.pfcam_port)
        else:
            root=lib.pfProperty_ParseName(self.pfcam_port,root)
        props=lib.collect_properties(self.pfcam_port,root,pfx=pfx,include_types=pfcam_lib.ValuePropertyTypes|{"PF_COMMAND"})
        pfprops=[]
        for (_,name) in props:
            try:
                pfprops.append(PfcamProperty(self.pfcam_port,name))
            except PFGenericError:
                pass
        return pfprops

    def get_value(self, name, default=None):
        """Get value of the property with a given name"""
        name=name.replace(".","/")
        if (default is not None) and (name not in self.properties):
            return default
        if self.properties.is_dictionary(self.properties[name]):
            return self.get_all_properties(root=name)
        v=self.properties[name].get_value()
        return v
    def _get_value_direct(self, name):
        return lib.get_property_by_name(self.pfcam_port,name)
    def set_value(self, name, value, ignore_missing=False, truncate=True):
        """
        Set value of the property with a given name.
        
        If ``truncate==True``, truncate value to lie within property range.
        """
        name=name.replace(".","/")
        if (name in self.properties) or (not ignore_missing):
            if self.properties.is_dictionary(self.properties[name]):
                self.set_all_properties(value,root=name)
            else:
                self.properties[name].set_value(value,truncate=truncate)
    def call_command(self, name, arg=0, ignore_missing=False):
        """If property is a command, call it with a given argument; otherwise, raise an error."""
        name=name.replace(".","/")
        if (name in self.properties) or (not ignore_missing):
            self.properties[name].call_command(arg=arg)

    def get_all_properties(self, root="", as_dict=False):
        """
        Get values of all properties with the given `root`.

        If ``as_dict==True``, return ``dict`` object; otherwise, return :class:`.Dictionary` object.
        """
        settings=self.properties[root].copy().filter_self(lambda a: a.readable).map_self(lambda a: a.get_value())
        return settings.as_dict(style="flat") if as_dict else settings
    def set_all_properties(self, settings, root="", truncate=True):
        """
        Set values of all properties with the given `root`.
        
        If ``truncate==True``, truncate value to lie within attribute range.
        """
        settings=dictionary.as_dict(settings,style="flat",copy=False)
        for k in settings:
            if k in self.properties[root] and self.properties[root,k].writable:
                self.properties[root,k].set_value(settings[k],truncate=truncate)


    ModelData=collections.namedtuple("ModelData",["model","serial_number"])
    def get_model_data(self):
        """
        Get camera model data.

        Return tuple ``(model, serial_number)``.
        """
        model=py3.as_str(lib.pfProperty_GetName(self.pfcam_port,lib.pfDevice_GetRoot(self.pfcam_port)))
        serial_number=self.get_value("Header.Serial",0)
        return self.ModelData(model,serial_number)


    def get_detector_size(self):
        return self.properties["Window/W"].max,self.properties["Window/H"].max
    def _get_pf_data_dimensions_rc(self):
        return self.v["Window/H"],self.v["Window/W"]
    def _update_imaq(self):
        r,c=self._get_pf_data_dimensions_rc()
        IMAQCamera.set_roi(self,0,c,0,r)
    def get_roi(self):
        """
        Get current ROI.

        Return tuple ``(hstart, hend, vstart, vend)``.
        """
        ox=self.v.get("Window/X",0)
        oy=self.v.get("Window/Y",0)
        w=self.v["Window/W"]
        h=self.v["Window/H"]
        return ox,ox+w,oy,oy+h
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None):
        """
        Setup camera ROI.

        By default, all non-supplied parameters take extreme values.
        """
        for a in ["Window/X","Window/Y","Window/W","Window/H"]:
            if a not in self.properties or not self.properties[a].writable:
                return
        det_size=self.get_detector_size()
        imaq_detector_size=IMAQCamera.get_detector_size(self)
        if hend is None:
            hend=det_size[0]
        if vend is None:
            vend=det_size[1]
        self.v["Window/W"]=min(hend-hstart,imaq_detector_size[0])
        self.v["Window/H"]=min(vend-vstart,imaq_detector_size[1])
        self.v["Window/X"]=hstart
        self.v["Window/Y"]=vstart
        self._update_imaq()
        return self.get_roi()
    def get_roi_limits(self):
        """
        Get the minimal and maximal ROI parameters.

        Return tuple ``(min_roi, max_roi)``, where each element is in turn 4-tuple describing the ROI.
        """
        params=["Window/X","Window/Y","Window/W","Window/H"]
        for p in params:
            self.properties[p].update_minmax()
        minp=tuple([(self.properties[p].min if p in self.properties else 0) for p in params])
        maxp=tuple([(self.properties[p].max if p in self.properties else 0) for p in params])
        min_roi=(0,0)+minp[2:]
        max_roi=maxp
        return (min_roi,max_roi)

    def _get_buffer_bpp(self):
        bpp=IMAQCamera._get_buffer_bpp(self)
        if "DataResolution" in self.properties:
            res=self.v["DataResolution"]
            m=re.match(r"Res(\d+)Bit",res)
            if m:
                bpp=(int(m.group(1))-1)//8+1
        return bpp
    def _get_data_dimensions_rc(self):
        roi=self.get_roi()
        w,h=roi[1]-roi[0],roi[3]-roi[2]
        return h,w

    def get_exposure(self):
        """Get current exposure"""
        return self.v["ExposureTime"]*1E-3
    def set_exposure(self, exposure):
        """Set current exposure"""
        self.v["ExposureTime"]=exposure*1E3
        return self.get_exposure()

    def get_frame_time(self):
        """Get current frame time"""
        if "FrameTime" in self.properties:
            return self.v["FrameTime"]*1E-3
        else:
            return 1./float(self.v["FrameRate"])
    def set_frame_time(self, frame_time):
        """Set current frame time"""
        if "FrameTime" in self.properties:
            self.v["FrameTime"]=frame_time*1E3
        return self.get_frame_time()

    def is_CFR_enabled(self):
        """Check if the constant frame rate mode is enabled"""
        return self.get_value("Trigger/CFR",False)
    def enable_CFR(self, enabled=True):
        """Enable constant frame rate mode"""
        self.set_value("Trigger/CFR",enabled,ignore_missing=True)
        return self.is_CFR_enabled()

    def get_trigger_interleave(self):
        """Check if the trigger interleave is on"""
        return self.get_value("Trigger/Interleave",False)
    def set_trigger_interleave(self, enabled):
        """Set the trigger interleave option on or off"""
        if self.get_trigger_interleave()!=enabled:
            if self.is_CFR_enabled():
                ft=self.get_frame_time()
                self.enable_CFR(False)
                self.set_value("Trigger/Interleave",enabled,ignore_missing=True)
                self.enable_CFR(True)
                self.set_frame_time(ft)
            else:
                self.set_value("Trigger/Interleave",enabled,ignore_missing=True)
        return self.get_trigger_interleave()

    def is_status_line_enabled(self):
        """Check if the status line is on"""
        return self.get_value("EnStatusLine",False)
    def enable_status_line(self, enabled=True):
        """Enable or disable status line"""
        self.set_value("EnStatusLine",enabled,ignore_missing=True)
        return self.is_status_line_enabled()

    def get_black_level_offset(self):
        """Get the black level offset"""
        return self.get_value("Voltages/BlackLevelOffset",0)
    def set_black_level_offset(self, offset):
        """Set the black level offset"""
        self.set_value("Voltages/BlackLevelOffset",offset,ignore_missing=True)
        return self.get_black_level_offset()







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
def get_status_lines(frames, check_transposed=True):
    """
    Extract status lines from the given frames.
    
    `frames` can be 2D array (one frame), 3D array (stack of frames, first index is frame number), or list of array.
    Automatically check if the status line is present; return ``None`` if it's not.
    If ``check_transposed==True``, check for the case where the image is transposed (i.e., line becomes a column).
    """
    if isinstance(frames,list):
        return [get_status_lines(f,check_transposed=check_transposed) for f in frames]
    if frames.shape[-1]>=4:
        lines=_extract_line(frames,True)
        if _check_magic(lines):
            return lines
        lines=_extract_line(frames,False)
        if _check_magic(lines):
            return lines
    if check_transposed:
        tframes=frames.T if frames.ndim==2 else frames.transpose((0,2,1))
        return get_status_lines(tframes,check_transposed=False)
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
    if sl_pos is "calculate":
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
    dfs=(lines[1:,1]-lines[:-1,1])%(2**24) # the internal counter is only 24-bit
    skipped_idx=(dfs!=step)
    skipped_idx=skipped_idx.nonzero()[0]
    return list(zip(skipped_idx,dfs[skipped_idx])) if len(skipped_idx) else []