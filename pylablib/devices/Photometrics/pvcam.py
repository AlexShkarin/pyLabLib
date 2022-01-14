from .pvcam_lib import wlib as lib, PvcamError, PvcamLibError
from . import pvcam_defs

from ...core.utils import py3
from ...core.devio import interface
from ..utils import load_lib
from ..interface import camera

import numpy as np
import numba as nb
import ctypes
import collections


class PvcamTimeoutError(PvcamError):
    "Pvcam frame timeout error"


class LibraryController(load_lib.LibraryController):
    def _do_init(self):
        lib.pl_pvcam_init()
    def _do_uninit(self):
        lib.pl_pvcam_uninit()
libctl=LibraryController(lib)


def list_cameras():
    """List all cameras available through Pvcam interface"""
    with libctl.temp_open():
        n=lib.pl_cam_get_total()
        return [py3.as_str(lib.pl_cam_get_name(i)) for i in range(n)]

def get_cameras_number():
    """Get number of connected Pvcam cameras"""
    return len(list_cameras())


def _lstrip(s, pfx):
    if s.startswith(pfx):
        return s[len(pfx):]
    return s
class PvcamAttribute:
    """
    Object representing an Pvcam camera parameter.

    Allows to query and set values and get additional information.
    Usually created automatically by an :class:`PvcamCamera` instance, but could be created manually.

    Args:
        handle: camera handle
        pid: parameter id of the attribute

    Attributes:
        name: attribute name
        kind: attribute kind (e.g., ``"INT8"`` or ``"FLT32"``)
        available (bool): whether attribute is available on the current hardware
        readable (bool): whether attribute is readable
        writable (bool): whether attribute is writable
        min (float or int): minimal attribute value (if applicable)
        max (float or int): maximal attribute value (if applicable)
        inc (float or int): minimal attribute increment value (if applicable)
        values: list of possible attribute numerical values (if applicable)
        labels: list ``{label: number}`` which shows all possible values of an enumerated attribute and their corresponding numerical values
        lvalues: list ``{number: label}`` which shows labels corresponding to numerical values of an enumerated attribute
        default: default values of the attribute
    """
    def __init__(self, handle, pid, cam=None):
        self.handle=handle
        self.pid=pid
        self.cam=cam
        self.name=_lstrip(pvcam_defs.drPARAM.get(pid,"UNKNOWN"),"PARAM_")
        self._attr_type_n=lib.get_param(self.handle,self.pid,pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_TYPE,pvcam_defs.PARAM_TYPE.TYPE_UNS16)
        self.kind=_lstrip(pvcam_defs.drPARAM_TYPE.get(self._attr_type_n,"UNKNOWN"),"TYPE_")
        self.available=lib.get_param(self.handle,self.pid,pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_AVAIL,pvcam_defs.PARAM_TYPE.TYPE_BOOLEAN)
        self._value_access_n=lib.get_param(self.handle,self.pid,pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_ACCESS,pvcam_defs.PARAM_TYPE.TYPE_UNS16)
        self.value_access=_lstrip(pvcam_defs.drPL_PARAM_ACCESS.get(self._value_access_n,"UNKNOWN"),"ACC_")
        self.readable=self.value_access in {"READ_ONLY","READ_WRITE"}
        self.writable=self.value_access in {"WRITE_ONLY","READ_WRITE"}
        
        self.min=self.max=self.inc=None
        self._cache=None
        self.values=[]
        self.labels={}
        self.lvalues={}
        self.update_limits()
        self.default=self._get_default_value() if self.available else None

    def update_limits(self):
        """Update attribute constraints"""
        if not self.available:
            return
        if self._attr_type_n==pvcam_defs.PARAM_TYPE.TYPE_ENUM:
            n=lib.get_param(self.handle,self.pid,pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_COUNT,pvcam_defs.PARAM_TYPE.TYPE_UNS32)
            evals=[lib.get_enum_value(self.handle,self.pid,v) for v in range(n)]
            self.values=list([iv for iv,_ in evals])
            self.labels={py3.as_str(sv):iv for iv,sv in evals}
            self.lvalues={iv:py3.as_str(sv) for iv,sv in evals}
        if self._attr_type_n in lib.numeric_params:
            try:
                self.min=lib.get_param(self.handle,self.pid,pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_MIN,self._attr_type_n)
                self.max=lib.get_param(self.handle,self.pid,pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_MAX,self._attr_type_n)
                self.inc=lib.get_param(self.handle,self.pid,pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_INCREMENT,self._attr_type_n)
            except PvcamLibError:
                self.min=self.max=self.inc=None
    def truncate_value(self, value):
        """Truncate value to lie within attribute limits"""
        self.update_limits()
        if self._attr_type_n in lib.numeric_params:
            if value<self.min:
                value=self.min
            elif value>self.max:
                value=self.max
            else:
                if self.inc>0:
                    value=((value-self.min)//self.inc)*self.inc+self.min
        return value

    def _get_default_value(self, enum_as_str=True):
        try:
            value=lib.get_param(self.handle,self.pid,param_attribute=pvcam_defs.PL_PARAM_ATTRIBUTES.ATTR_DEFAULT,typ=self._attr_type_n)
        except PvcamLibError:
            return None
        if enum_as_str and self._attr_type_n==pvcam_defs.PARAM_TYPE.TYPE_ENUM:
            value=self.lvalues.get(value,value)
        if self._attr_type_n==pvcam_defs.PARAM_TYPE.TYPE_BOOLEAN:
            value=bool(value)
        return value
    def get_value(self, enum_as_str=True, error_on_noacq=True):
        """
        Get attribute value.
        
        If ``enum_as_str==True``, return enum-style values as strings; otherwise, return corresponding integer values.
        """
        if self.cam is not None and self.cam.acquisition_in_progress():
            if self._cache is None:
                return None
            value=self._cache
        else:
            try:
                value=lib.get_param(self.handle,self.pid,typ=self._attr_type_n)
            except PvcamLibError as err:
                if not error_on_noacq and err.code==188: # PL_ERR_ACQUISITION_SETUP_REQUIRED
                    self._cache=None
                    return
                raise
            self._cache=value
        if enum_as_str and self._attr_type_n==pvcam_defs.PARAM_TYPE.TYPE_ENUM:
            value=self.lvalues[value]
        if self._attr_type_n==pvcam_defs.PARAM_TYPE.TYPE_BOOLEAN:
            value=bool(value)
        return value
    def set_value(self, value, truncate=True):
        """
        Set attribute value.
        
        If ``truncate==True``, automatically truncate value to lie within allowed range.
        """
        if self.cam is not None and self.cam.acquisition_in_progress():
            raise PvcamError("can not set attribute values during acquisition")
        if truncate:
            value=self.truncate_value(value)
        value=self.labels.get(value,value)
        lib.set_param(self.handle,self.pid,value,typ=self._attr_type_n)

    def __repr__(self):
        return "{}(name='{}', kind='{}')".format(self.__class__.__name__,self.name,self.kind)








TDeviceInfo=collections.namedtuple("TDeviceInfo",["vendor","product","chip","system","part","serial"])
TFrameInfo=collections.namedtuple("TFrameInfo",["frame_index","timestamp_start_ns","timestamp_end_ns","framestamp","flags","exposure_ns"])
class PvcamCamera(camera.IBinROICamera, camera.IExposureCamera, camera.IAttributeCamera):
    """
    Generic Pvcam camera interface.

    Args:
        serial_number: camera serial number; if ``None``, connect to the first non-used camera
    """
    Error=PvcamError
    TimeoutError=PvcamTimeoutError
    _TFrameInfo=TFrameInfo
    _frameinfo_fields=TFrameInfo._fields
    _clear_pausing_acquisition=True
    def __init__(self, name=None):
        super().__init__()
        self.name=name
        self.handle=None
        self._buffer=None
        self._frame_bytes=None
        self._buffer_frames=None
        self._acq_in_progress=False
        self._cb=None
        self.open()
        self._add_info_variable("device_info",self.get_device_info)
        self._add_info_variable("pixel_size",self.get_pixel_size)
        self._add_info_variable("pixel_distance",self.get_pixel_distance)
        self._add_info_variable("binning_modes",self.get_supported_binning_modes)
        self._add_settings_variable("metadata_enabled",self.is_metadata_enabled,self.enable_metadata)
        self._update_device_variable_order("exposure")
        self._add_status_variable("frame_period",self.get_frame_period)


    def _get_connection_parameters(self):
        return self.name
    def open(self):
        """Open connection to the camera"""
        if self.handle is not None:
            return
        with libctl.temp_open():
            cams=list_cameras()
            if not cams:
                raise PvcamError("no cameras are avaliable")
            if self.name is None:
                self.name=cams[0]
            elif self.name not in cams:
                raise PvcamError("camera with name {} isn't present among available cameras: {}".format(self.name,cams))
            self.handle=lib.pl_cam_open(self.name,pvcam_defs.PL_OPEN_MODES.OPEN_EXCLUSIVE)
            self._opid=libctl.open().opid
            try:
                self._update_attributes()
                self._setup_full_roi()
                self._setup_bin_ranges()
            except self.Error:
                self.close()
                raise
    def close(self):
        """Close connection to the camera"""
        if self.handle is not None:
            self.clear_acquisition()
            lib.pl_cam_close(self.handle)
            self.handle=None
            libctl.close(self._opid)
    def is_opened(self):
        """Check if the device is connected"""
        return self.handle is not None

    def _list_attributes(self):
        atts=[PvcamAttribute(self.handle,p,cam=self) for p in pvcam_defs.PARAM]
        return [a for a in atts if a.available and a._attr_type_n in lib.supported_params]
    def get_attribute_value(self, name, error_on_missing=True, error_on_noacq=False, default=None, enum_as_str=True):  # pylint: disable=arguments-differ
        """
        Get value of an attribute with the given name.
        
        If the value doesn't exist or can not be read and ``error_on_missing==True``, raise error; otherwise, return `default`.
        If `default` is not ``None``, assume that ``error_on_missing==False``.
        If `name` points at a dictionary branch, return a dictionary with all values in this branch.
        If ``enum_as_str==True``, return enum-style values as strings; otherwise, return corresponding integer values.
        """
        return super().get_attribute_value(name,error_on_missing=error_on_missing,default=default,error_on_noacq=error_on_noacq,enum_as_str=enum_as_str)
    def set_attribute_value(self, name, value, truncate=True, error_on_missing=True):  # pylint: disable=arguments-differ
        """
        Set value of an attribute with the given name.
        
        If the value doesn't exist or can not be written and ``error_on_missing==True``, raise error; otherwise, do nothing.
        If `name` points at a dictionary branch, set all values in this branch (in this case `value` must be a dictionary).
        If ``truncate==True``, truncate value to lie within attribute range.
        """
        return super().set_attribute_value(name,value,truncate=truncate,error_on_missing=error_on_missing)
    def get_all_attribute_values(self, root="", enum_as_str=True, error_on_noacq=False):  # pylint: disable=arguments-differ
        """Get values of all attributes with the given `root`"""
        return super().get_all_attribute_values(root=root,enum_as_str=enum_as_str,error_on_noacq=error_on_noacq)
    def set_all_attribute_values(self, settings, root="", truncate=True):  # pylint: disable=arguments-differ
        """
        Set values of all attributes with the given `root`.
        
        If ``truncate==True``, truncate value to lie within attribute range.
        """
        return super().set_all_attribute_values(settings,root=root,truncate=truncate)

    def get_device_info(self):
        """
        Get camera information.

        Return tuple ``(vendor, product, chip, system, part, serial)``.
        """
        atts=["VENDOR_NAME","PRODUCT_NAME","CHIP_NAME","SYSTEM_NAME","CAMERA_PART_NUMBER","HEAD_SER_NUM_ALPHA"]
        return TDeviceInfo(*[self.get_attribute_value(n,error_on_missing=False) for n in atts])

    def get_pixel_size(self):
        """Get camera pixel size (in m)"""
        return tuple([self.get_attribute_value(v,error_on_missing=False,default=0)*1E-9 for v in ["PIX_SER_SIZE","PIX_PAR_SIZE"]])
    def get_pixel_distance(self):
        """Get camera pixel distance (in m)"""
        return tuple([self.get_attribute_value(v,error_on_missing=False,default=0)*1E-9 for v in ["PIX_SER_DIST","PIX_PAR_DIST"]])

    def is_metadata_enabled(self, individual=False):
        """Check if metadata is enabled"""
        return self.get_attribute_value("METADATA_ENABLED",error_on_missing=False,default=False)
    @camera.acqcleared
    def enable_metadata(self, enable=True):
        """Enable or disable metadata"""
        self.set_attribute_value("METADATA_ENABLED",enable,error_on_missing=False)
        return self.is_metadata_enabled()
    
    _exp_res={  pvcam_defs.PL_EXP_RES_MODES.EXP_RES_ONE_SEC:1,
                pvcam_defs.PL_EXP_RES_MODES.EXP_RES_ONE_MILLISEC:1E-3,
                pvcam_defs.PL_EXP_RES_MODES.EXP_RES_ONE_MICROSEC:1E-6}
    def _get_exp_res(self):
        exp_res=self.get_attribute_value("EXP_RES",error_on_missing=False,default=0,enum_as_str=False)
        return self._exp_res[exp_res]
    def _set_min_exp_res(self):
        if "EXP_RES" in self.ca:
            att=self.ca["EXP_RES"]
            for er in [pvcam_defs.PL_EXP_RES_MODES.EXP_RES_ONE_MICROSEC,pvcam_defs.PL_EXP_RES_MODES.EXP_RES_ONE_MILLISEC,pvcam_defs.PL_EXP_RES_MODES.EXP_RES_ONE_SEC]:
                if er in att.values:
                    att.set_value(er)
                    break
    def get_exposure(self):
        return self.cav["EXPOSURE_TIME"]*self._get_exp_res()
    def set_exposure(self, exposure):
        self._set_min_exp_res()
        self._setup_acquisition(exposure=int(exposure/self._get_exp_res()))
        return self.get_exposure()
    def get_frame_timings(self):
        exp=self.get_exposure()
        return self._TAcqTimings(exp,self.cav["READOUT_TIME"]*1E-6+exp)



    def _get_data_dimensions_rc(self):
        roi=self.get_roi()
        w,h=(roi[1]-roi[0])//roi[4],(roi[3]-roi[2])//roi[5]
        return h,w
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        return self.cav["SER_SIZE"],self.cav["PAR_SIZE"]
    def _setup_full_roi(self):
        w,h=self.get_detector_size()
        self._roi=(0,w,0,h,1,1)
        self._setup_acquisition()
    def _setup_bin_ranges(self):
        try:
            binss=list(self.ca["BINNING_SER"].labels)
            def s2t(s):
                h,v=s.split("x")
                return int(h),int(v)
            self._hvbins=sorted([s2t(s) for s in binss])
        except KeyError:
            self._hvbins=None
    def get_roi(self):
        return self._roi
    def _limit_bin(self, hb, vb):
        if self._hvbins is None:
            return hb,vb
        hvb=self._hvbins[0]
        for (thb,tvb) in self._hvbins:
            if (hb,vb)==(thb,tvb):
                return (hb,vb)
            if thb<=hb and tvb<=vb:
                hvb=(thb,tvb)
        return hvb
    @camera.acqcleared
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        hbin,vbin=self._limit_bin(hbin,vbin)
        hlim,vlim=self.get_roi_limits(hbin,vbin)
        hstart,hend,_=self._roi=camera.truncate_roi_axis((hstart,hend,hbin),hlim)
        vstart,vend,_=self._roi=camera.truncate_roi_axis((vstart,vend,vbin),vlim)
        self._roi=(hstart,hend,vstart,vend,hbin,vbin)
        self._setup_acquisition()
        return self.get_roi()
    def get_roi_limits(self, hbin=1, vbin=1):
        wdet,hdet=self.get_detector_size()
        hlim=camera.TAxisROILimit(max(2*hbin,4),wdet,hbin,hbin,max([hb for hb,_ in self._hvbins]))
        vlim=camera.TAxisROILimit(max(2*vbin,4),hdet,vbin,vbin,max([vb for _,vb in self._hvbins]))
        return hlim,vlim
    def get_supported_binning_modes(self):
        """Get all possible binning combinations as a list ``[(hbin, vbin)]``"""
        return self._hvbins if self._hvbins is not None else None
    

    def _allocate_buffer(self, frame_bytes, nframes):
        self._deallocate_buffer()
        self._frame_bytes=frame_bytes
        self._buffer_frames=nframes
        self._buffer=ctypes.create_string_buffer(frame_bytes*nframes)
    def _deallocate_buffer(self):
        self._buffer=None
    def _on_callback(self, frame_info, context):
        pass
    def _register_callback(self):
        self._deregister_callback()
        self._cb=lib.pl_cam_register_callback_ex3(self.handle,pvcam_defs.PL_CALLBACK_EVENT.PL_CALLBACK_EOF,self._on_callback,wrap=False)
    def _deregister_callback(self):
        if self._cb is not None:
            lib.pl_cam_deregister_callback(self.handle,pvcam_defs.PL_CALLBACK_EVENT.PL_CALLBACK_EOF)
            self._cb=None
    def _setup_acquisition(self, roi=None, exp_mode=None, exposure=None):
        if roi is None:
            roi=self._roi
        if exposure is None:
            exposure=self.cav["EXPOSURE_TIME"]
        if exp_mode is None:
            exp_mode=self.get_attribute_value("EXPOSURE_MODE",enum_as_str=False)
        r0,r1,c0,c1,rb,cb=roi
        return lib.pl_exp_setup_cont(self.handle,[(r0,r1-1,rb,c0,c1-1,cb)],exp_mode,exposure,pvcam_defs.PL_CIRC_MODES.CIRC_OVERWRITE) # TODO: snap mode

    @interface.use_parameters(mode="acq_mode")
    def setup_acquisition(self, mode="sequence", nframes=100):  # pylint: disable=arguments-differ
        """
        Setup acquisition mode.

        `mode` can be either ``"snap"`` (single frame or a fixed number of frames) or ``"sequence"`` (continuous acquisition).
        `nframes` sets up number of frame buffers.
        """
        self.clear_acquisition()
        super().setup_acquisition(mode=mode,nframes=nframes)
        buffsize=self._setup_acquisition()
        self._allocate_buffer(buffsize,self._acq_params["nframes"])
    def clear_acquisition(self):
        self.stop_acquisition()
        self._deallocate_buffer()
        super().clear_acquisition()
    def start_acquisition(self, *args, **kwargs):
        self.stop_acquisition()
        super().start_acquisition(*args,**kwargs)
        self._frame_counter.reset(self._acq_params["nframes"])
        self.get_all_attribute_values()
        lib.pl_exp_start_cont(self.handle,self._buffer,len(self._buffer)) # TODO: snap mode
        self._acq_in_progress=True
    def stop_acquisition(self):
        if self.acquisition_in_progress():
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
            lib.pl_exp_abort(self.handle,pvcam_defs.PL_CCS_ABORT_MODES.CCS_HALT_CLOSE_SHTR)
            self._acq_in_progress=False
        super().stop_acquisition()
    def acquisition_in_progress(self):
        return self._acq_in_progress
    def _get_acquired_frames(self):
        status=lib.pl_exp_check_cont_status_ex(self.handle) # TODO: snap mode
        frame_info=status[-1]
        return frame_info.FrameNr
    


    def _get_frame_params(self):
        bypp=(self.cav["BIT_DEPTH"]-1)//8+1
        shape=self._get_data_dimensions_rc()
        return shape,bypp
    def _parse_frame(self, ptr, shape, bypp):
        height,width=shape
        imsize=height*width*bypp
        img=np.ctypeslib.as_array(ctypes.cast(ptr,ctypes.POINTER(ctypes.c_ubyte)),shape=(imsize,))
        dtype="<u{}".format(bypp)
        img=img.view(dtype).reshape((height,width)).copy()
        img=self._convert_indexing(img,"rct")
        return img
    def _parse_md_frame(self, ptr):
        pheader=ctypes.cast(ptr,pvcam_defs.Pmd_frame_header)
        if pheader.contents.version==3:
            pheader=ctypes.cast(ptr,pvcam_defs.Pmd_frame_header_v3)
        header=pheader.contents
        ptr+=ctypes.sizeof(header)
        ptr+=header.extendedMdSize  # skip extended metadata
        rois=[]
        bypp=(header.bitDepth-1)//8+1
        for _ in range(header.roiCount):
            proi_header=ctypes.cast(ptr,pvcam_defs.Pmd_frame_roi_header)
            roi_header=proi_header.contents
            rgn=roi_header.roi
            rgn_shape=(rgn.p2-rgn.p1+1)//rgn.pbin,(rgn.s2-rgn.s1+1)//rgn.sbin
            byte_size=rgn_shape[0]*rgn_shape[1]*bypp
            if header.version>1:
                header_byte_size=roi_header.roiDataSize
                if byte_size!=header_byte_size:
                    raise PvcamError("received frame size {} does not agree with {}x{}x{}={} size from the header".format(header_byte_size,rgn_shape[0],rgn_shape[1],bypp,byte_size))
            ptr+=ctypes.sizeof(pvcam_defs.md_frame_roi_header)
            frame=self._parse_frame(ptr,rgn_shape,bypp)
            ptr+=byte_size+roi_header.extendedMdSize
            rois.append((roi_header,frame))
        return header,rois
    def _md_to_frame_info(self, header, roi_header, frame_index):
        if header.version<3:
            timestamp_start_ns=int(header.timestampBOF)*int(header.timestampResNs)
            timestamp_end_ns=int(header.timestampEOF)*int(header.timestampResNs)
            exposure_ns=int(header.exposureTime)*int(header.exposureTimeResNs)
        else:
            timestamp_start_ns=int(header.timestampBOF)//1000
            timestamp_end_ns=int(header.timestampEOF)//1000
            exposure_ns=int(header.exposureTime)//1000
        flags=header.flags
        framestamp=header.frameNr
        return self._convert_frame_info(TFrameInfo(frame_index,timestamp_start_ns,timestamp_end_ns,framestamp,flags,exposure_ns))
    def _parse_md_frame_info(self, ptr, frame_index):
        header,rois=self._parse_md_frame(ptr)
        return rois[0][1],self._md_to_frame_info(header,rois[0][0],frame_index)
    def _read_frames(self, rng, return_info=False):
        shape,bypp=self._get_frame_params()
        base=ctypes.addressof(self._buffer)
        if self.is_metadata_enabled():
            data=[self._parse_md_frame_info(base+(i%self._buffer_frames)*self._frame_bytes,i) for i in range(*rng)]
            frames=[f for f,_ in data]
            frame_info=[i for _,i in data]
        else:
            frames=[self._parse_frame(base+(i%self._buffer_frames)*self._frame_bytes,shape,bypp=bypp) for i in range(*rng)]
            frame_info=[None]*len(frames)
        return frames,frame_info
    def _zero_frame(self, n):
        dim=self.get_data_dimensions()
        _,bypp=self._get_frame_params()
        dt="<u{}".format(bypp)
        return np.zeros((n,)+dim,dtype=dt)
    def read_multiple_images(self, rng=None, peek=False, missing_frame="skip", return_info=False):
        """
        Read multiple images specified by `rng` (by default, all un-read images).

        If `rng` is specified, it is a tuple ``(first, last)`` with images range (first inclusive).
        If no new frames are available, return an empty list; if no acquisition is running, return ``None``.
        If ``peek==True``, return images but not mark them as read.
        `missing_frame` determines what to do with frames which are out of range (missing or lost):
        can be ``"none"`` (replacing them with ``None``), ``"zero"`` (replacing them with zero-filled frame), or ``"skip"`` (skipping them).
        If ``return_info==True``, return tuple ``(frames, infos)``, where ``infos`` is a list of :class:`TFrameInfo` instances
        describing frame index and frame metadata, which contains start and stop timestamps, framestamp, frame flags, and exposure;
        if some frames are missing and ``missing_frame!="skip"``, the corresponding frame info is ``None``.
        """
        return super().read_multiple_images(rng=rng,peek=peek,missing_frame=missing_frame,return_info=return_info)





@nb.njit
def copy_strided(src, dst, n, size, stride):
    ipos=nb.uint64(0)
    opos=nb.uint64(0)
    n=nb.uint64(n)
    size=nb.uint64(size)
    stride=nb.uint64(stride)
    for _ in range(n):
        for p in range(size):
            dst[opos+p]=src[ipos+p]
        opos+=size
        ipos+=stride