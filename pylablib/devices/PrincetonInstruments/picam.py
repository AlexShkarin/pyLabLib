from .picam_lib import PicamEnumeratedType, PicamValueType, picam_defs
from .picam_lib import wlib as lib, PicamError, PicamLibError

from ...core.utils import py3
from ...core.devio import interface
from ..utils import load_lib
from ..interface import camera

import bisect
import numpy as np
import struct
import ctypes
import collections


class PicamTimeoutError(PicamError):
    "Picam frame timeout error"


class LibraryController(load_lib.LibraryController):
    def _do_init(self):
        lib.Picam_InitializeLibrary()
    def _do_uninit(self):
        lib.Picam_UninitializeLibrary()
libctl=LibraryController(lib)



def _get_str(stype, value):
    return py3.as_str(lib.Picam_GetEnumerationString(stype,value))

TCameraInfo=collections.namedtuple("TCameraInfo",["name","serial_number","model","interface"])
def _parse_camid(camid):
    name=py3.as_str(camid.sensor_name)
    serial_number=py3.as_str(camid.serial_number)
    model=_get_str(PicamEnumeratedType.PicamEnumeratedType_Model,camid.model)
    computer_interface=_get_str(PicamEnumeratedType.PicamEnumeratedType_ComputerInterface,camid.computer_interface)
    return TCameraInfo(name,serial_number,model,computer_interface)
def list_cameras():
    """List all cameras available through Picam interface"""
    with libctl.temp_open():
        camids=lib.Picam_GetAvailableCameraIDs()
        return [_parse_camid(ci) for ci in camids]

def get_cameras_number():
    """Get number of connected Picam cameras"""
    return len(list_cameras())



TROIConstraints=collections.namedtuple("TROIConstraints",["flags","nrois","xrng","wrng","xbins","yrng","hrng","ybins"])
class PicamAttribute:
    """
    Object representing an Picam camera parameter.

    Allows to query and set values and get additional information.
    Usually created automatically by an :class:`PicamCamera` instance, but could be created manually.

    Args:
        handle: camera handle
        pid: parameter id of the attribute

    Attributes:
        name: attribute name
        kind: attribute kind; can be ``"Integer"``, ``"Large Integer"``, ``"Floating Point"``,
            ``"Enumeration"``, ``"Boolean"``, or ``"Rois"``
        exists (bool): whether attribute is available on the current hardware
        relevant (bool): whether attribute value is applicable to the hardware
        read_directly (bool): whether value can be read directly from the device;
            if ``True``, then :meth:`get_value` will automatically use the appropriate method
        value_access (str): value access kind, which shows whether value can be written
        writable (bool): whether value is read-only
        default: default parameter value (only for writable parameters)
        can_set_online (bool): whether value can be changed during acquisition
        cons_type (str): constraint type, e.g., ``"Collection"``, ``"Range"``, or ``"None"``
        cons_permanent (bool): whether the constraint is permanent, or dependent on other parameters;
            if ``False``, then use :meth:`update_limits` to update the constraints
        cons_error (bool): whether setting the out-of-range parameter causes error or just warning
        cons_novalid (bool): whether no parameter value is valid
        min (float or int): minimal attribute value (if applicable)
        max (float or int): maximal attribute value (if applicable)
        inc (float or int): minimal attribute increment value (if applicable)
        cons_excluded: list of special parameters which are within the range but are excluded
        cons_included: list of special parameters which are outside the range but are included
        ivalues: list of possible integer values for enum attributes
        values: list of possible text values for enum attributes
        labels: dict ``{label: index}`` which shows all possible values of an enumerated attribute and their corresponding numerical values
        ilabels: dict ``{index: label}`` which shows labels corresponding to numerical values of an enumerated attribute
    """
    def __init__(self, handle, pid):
        self.handle=handle
        self.pid=pid
        self.name=_get_str(PicamEnumeratedType.PicamEnumeratedType_Parameter,pid)
        self._attr_type_n=lib.Picam_GetParameterValueType(handle,pid)
        self.kind=_get_str(PicamEnumeratedType.PicamEnumeratedType_ValueType,self._attr_type_n)
        self.exists=bool(lib.Picam_DoesParameterExist(handle,pid))
        self.relevant=bool(lib.Picam_IsParameterRelevant(handle,pid))
        self.read_directly=bool(lib.Picam_CanReadParameter(handle,pid))
        self._value_access_n=lib.Picam_GetParameterValueAccess(handle,pid)
        self.value_access=_get_str(PicamEnumeratedType.PicamEnumeratedType_ValueAccess,self._value_access_n)
        self.writable=self._value_access_n!=picam_defs.PicamValueAccess.PicamValueAccess_ReadOnly
        self.can_set_online=self.writable and lib.Picam_CanSetParameterOnline(handle,pid)
        if self.kind=="Enumeration":
            self._enum_type_n=lib.Picam_GetParameterEnumeratedType(handle,pid)
            self.enum_type=_get_str(PicamEnumeratedType.PicamEnumeratedType_EnumeratedType,self._enum_type_n)
        else:
            self._enum_type_n=self.enum_type=None
        self.default=self._as_text(self._get_default_value())

        self._cons_type_n=lib.Picam_GetParameterConstraintType(handle,pid)
        self.cons_type=_get_str(PicamEnumeratedType.PicamEnumeratedType_ConstraintType,self._cons_type_n)
        self.cons_permanent=True
        self.cons_error=True
        self.cons_novalid=False
        self.min=self.max=self.inc=None
        self.cons_excluded=[]
        self.cons_included=[]
        self.values=[]
        self.ivalues=[]
        self.labels={}
        self.ilabels={}
        self.cons_roi=None
        self.update_limits(force=True)


    _int_kinds={PicamValueType.PicamValueType_Integer, PicamValueType.PicamValueType_Enumeration}
    _bool_kinds={PicamValueType.PicamValueType_Boolean}
    _enum_kinds={PicamValueType.PicamValueType_Enumeration}
    _large_int_kinds={PicamValueType.PicamValueType_LargeInteger}
    _float_kinds={PicamValueType.PicamValueType_FloatingPoint}
    _roi_kinds={PicamValueType.PicamValueType_Rois}
    def _get_value(self):
        if self._attr_type_n in self._int_kinds:
            return lib.Picam_GetParameterIntegerValue(self.handle,self.pid)
        if self._attr_type_n in self._bool_kinds:
            return bool(lib.Picam_GetParameterIntegerValue(self.handle,self.pid))
        if self._attr_type_n in self._large_int_kinds:
            return lib.Picam_GetParameterLargeIntegerValue(self.handle,self.pid)
        if self._attr_type_n in self._float_kinds:
            return lib.Picam_GetParameterFloatingPointValue(self.handle,self.pid)
        if self._attr_type_n in self._roi_kinds:
            return lib.Picam_GetParameterRoisValue(self.handle,self.pid)
    def _get_default_value(self):
        if not self.writable:
            return None
        if self._attr_type_n in self._int_kinds:
            return lib.Picam_GetParameterIntegerDefaultValue(self.handle,self.pid)
        if self._attr_type_n in self._bool_kinds:
            return bool(lib.Picam_GetParameterIntegerDefaultValue(self.handle,self.pid))
        if self._attr_type_n in self._large_int_kinds:
            return lib.Picam_GetParameterLargeIntegerDefaultValue(self.handle,self.pid)
        if self._attr_type_n in self._float_kinds:
            return lib.Picam_GetParameterFloatingPointDefaultValue(self.handle,self.pid)
        if self._attr_type_n in self._roi_kinds:
            return lib.Picam_GetParameterRoisDefaultValue(self.handle,self.pid)
    def _read_value(self):
        if self._attr_type_n in self._int_kinds:
            return lib.Picam_ReadParameterIntegerValue(self.handle,self.pid)
        if self._attr_type_n in self._bool_kinds:
            return bool(lib.Picam_ReadParameterIntegerValue(self.handle,self.pid))
        if self._attr_type_n in self._float_kinds:
            return lib.Picam_ReadParameterFloatingPointValue(self.handle,self.pid)
    def _as_text(self, value):
        if value is not None and self._attr_type_n==PicamValueType.PicamValueType_Enumeration:
            return _get_str(self._enum_type_n,int(value))
        return value
    def _as_type(self, value):
        if self._attr_type_n==PicamValueType.PicamValueType_Enumeration:
            value=self.labels.get(value,value)
        if self._attr_type_n in [PicamValueType.PicamValueType_Integer,
                                PicamValueType.PicamValueType_LargeInteger,
                                PicamValueType.PicamValueType_Enumeration]:
            return int(value)
        if self._attr_type_n==PicamValueType.PicamValueType_FloatingPoint:
            return float(value)
        if self._attr_type_n==PicamValueType.PicamValueType_Boolean:
            return bool(value)
        return value
    def _set_value(self, value):
        if self._attr_type_n in self._int_kinds:
            lib.Picam_SetParameterIntegerValue(self.handle,self.pid,int(value))
        if self._attr_type_n in self._bool_kinds:
            lib.Picam_SetParameterIntegerValue(self.handle,self.pid,1 if value else 0)
        if self._attr_type_n in self._large_int_kinds:
            lib.Picam_SetParameterLargeIntegerValue(self.handle,self.pid,int(value))
        if self._attr_type_n in self._float_kinds:
            lib.Picam_SetParameterFloatingPointValue(self.handle,self.pid,float(value))
        if self._attr_type_n in self._roi_kinds:
            lib.Picam_SetParameterRoisValue(self.handle,self.pid,value)

    def update_limits(self, force=False):
        """
        Update attribute constraints.

        If ``force==False`` and the constraints are permanent, skip the update.
        """
        if self.cons_permanent and not force:
            return
        if self.cons_type=="Range":
            cons=lib.Picam_GetParameterRangeConstraint(self.handle,self.pid,picam_defs.PicamConstraintCategory.PicamConstraintCategory_Required)
            self.cons_permanent=(cons[0]==picam_defs.PicamConstraintScope.PicamConstraintScope_Independent)
            self.cons_error=(cons[1]==picam_defs.PicamConstraintSeverity.PicamConstraintSeverity_Error)
            self.cons_novalid=bool(cons[2])
            self.min=self._as_type(cons[3])
            self.max=self._as_type(cons[4])
            self.inc=self._as_type(cons[5])
            self.cons_excluded=[self._as_type(v) for v in cons[6]]
            self.cons_included=[self._as_type(v) for v in cons[7]]
        elif self.cons_type=="Collection":
            cons=lib.Picam_GetParameterCollectionConstraint(self.handle,self.pid,picam_defs.PicamConstraintCategory.PicamConstraintCategory_Required)
            self.cons_permanent=(cons[0]==picam_defs.PicamConstraintScope.PicamConstraintScope_Independent)
            self.cons_error=(cons[1]==picam_defs.PicamConstraintSeverity.PicamConstraintSeverity_Error)
            self.ivalues=[self._as_type(v) for v in cons[2]]
            self.values=[self._as_text(v) for v in self.ivalues]
            self.labels=dict(zip(self.values,self.ivalues))
            self.ilabels=dict(zip(self.ivalues,self.values))
        elif self.cons_type=="ROIs":
            cons=lib.Picam_GetParameterRoisConstraint(self.handle,self.pid,picam_defs.PicamConstraintCategory.PicamConstraintCategory_Required)
            self.cons_permanent=(cons[0]==picam_defs.PicamConstraintScope.PicamConstraintScope_Independent)
            self.cons_error=(cons[1]==picam_defs.PicamConstraintSeverity.PicamConstraintSeverity_Error)
            self.cons_novalid=bool(cons[2])
            self.cons_roi=TROIConstraints(cons[3],cons[4],
                tuple(int(v) for v in cons[5][3:6]),tuple(int(v) for v in cons[6][3:6]),cons[7] or None,
                tuple(int(v) for v in cons[8][3:6]),tuple(int(v) for v in cons[9][3:6]),cons[10] or None)
        elif self.cons_type=="None" and self.kind=="Enumeration":
            i=0
            while True:
                try:
                    t=self._as_text(i)
                    self.values.append(t)
                    self.ivalues.append(self._as_type(i))
                except PicamLibError:
                    if i>10:
                        break
                i+=1
            self.labels=dict(zip(self.values,self.ivalues))
            self.ilabels=dict(zip(self.ivalues,self.values))
    def truncate_value(self, value):
        """Truncate value to lie within attribute limits"""
        self.update_limits()
        if self.cons_type=="Range":
            if value not in self.cons_included:
                if value<self.min:
                    value=self.min
                elif value>self.max:
                    value=self.max
                else:
                    if self.inc>0:
                        value=((value-self.min)//self.inc)*self.inc+self.min
        return value

    def get_value(self, enum_as_str=True):
        """
        Get attribute value.
        
        If ``enum_as_str==True``, return enum-style values as strings; otherwise, return corresponding integer values.
        """
        value=self._read_value() if self.read_directly else self._get_value()
        if enum_as_str:
            value=self._as_text(value)
        return value
    def set_value(self, value, truncate=True):
        """
        Get attribute value.
        
        If ``truncate==True``, automatically truncate value to lie within allowed range.
        """
        value=self._as_type(value)
        if truncate:
            value=self.truncate_value(value)
        self._set_value(value)

    def __repr__(self):
        return "{}(name='{}', kind='{}')".format(self.__class__.__name__,self.name,self.kind)








TDeviceInfo=collections.namedtuple("TDeviceInfo",["name","serial_number","model","interface"])
TFrameInfo=collections.namedtuple("TFrameInfo",["frame_index","timestamp_start","timestamp_end","framestamp"])
class PicamCamera(camera.IBinROICamera, camera.IExposureCamera, camera.IAttributeCamera):
    """
    Generic Picam camera interface.

    Args:
        serial_number: camera serial number; if ``None``, connect to the first non-used camera
    """
    Error=PicamError
    TimeoutError=PicamTimeoutError
    _TFrameInfo=TFrameInfo
    def __init__(self, serial_number=None):
        super().__init__()
        self.serial_number=serial_number
        self.handle=None
        self.devhandle=None
        self._buffer=None
        self._readout_bytes=None
        self._frame_bytes=None
        self._frames_per_readout=1
        self._buffer_readouts=None
        self._waited_readouts=0
        self.open()
        self._add_info_variable("device_info",self.get_device_info)
        self._add_info_variable("pixel_size",self.get_pixel_size)
        self._add_settings_variable("metadata_enabled",self.is_metadata_enabled,self.enable_metadata)
        self._update_device_variable_order("exposure")
        self._add_status_variable("frame_period",self.get_frame_period)


    def _get_connection_parameters(self):
        return self.get_device_info().serial_number
    def open(self):
        """Open connection to the camera"""
        if self.handle is not None:
            return
        with libctl.temp_open():
            cams=list_cameras()
            serials=[c.serial_number for c in cams]
            if not serials:
                raise PicamError("no cameras are avaliable")
            if self.serial_number is None:
                self.serial_number=serials[0]
            elif self.serial_number not in serials:
                raise PicamError("camera with serial number {} isn't present among available cameras: {}".format(self.serial_number,serials))
            self.handle=lib.Picam_OpenCamera_BySerial(py3.as_bytes(self.serial_number))
            self.devhandle=lib.PicamAdvanced_GetCameraDevice(self.handle)
            self._opid=libctl.open().opid
            try:
                self._update_attributes()
            except self.Error:
                self.close()
                raise
    def close(self):
        """Close connection to the camera"""
        if self.handle is not None:
            self.clear_acquisition()
            lib.Picam_CloseCamera(self.handle)
            self.handle=None
            self.devhandle=None
            libctl.close(self._opid)
    def is_opened(self):
        """Check if the device is connected"""
        return self.handle is not None

    def _list_attributes(self):
        return [PicamAttribute(self.handle,p) for p in lib.Picam_GetParameters(self.handle)]
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
    def get_all_attribute_values(self, root="", enum_as_str=True):  # pylint: disable=arguments-differ
        """Get values of all attributes with the given `root`"""
        return super().get_all_attribute_values(root=root,enum_as_str=enum_as_str)
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
        cam_info=_parse_camid(lib.Picam_GetCameraID(self.handle))
        return TDeviceInfo(*cam_info)

    def get_pixel_size(self):
        """Get camera pixel size (in m)"""
        return tuple([self.cav[v]*1E-6 for v in ["Pixel Width","Pixel Height"]])

    _ts_exposure_start=picam_defs.PicamTimeStampsMask.PicamTimeStampsMask_ExposureStarted
    _ts_exposure_end=picam_defs.PicamTimeStampsMask.PicamTimeStampsMask_ExposureEnded
    @camera.acqcleared
    def enable_metadata(self, enable=True):
        """Enable or disable metadata"""
        tsattr=self.ca["Time Stamps"]
        tsval=self._ts_exposure_start|self._ts_exposure_end
        tsattr.set_value(tsval if enable and (tsval in tsattr.ivalues) else 0)
        fsattr=self.ca["Track Frames"]
        fsattr.set_value(True if enable and (True in fsattr.ivalues) else False)
        self.set_attribute_value("Gate Tracking",False,error_on_missing=False)
        self.set_attribute_value("Modulation Tracking",False,error_on_missing=False)
    def is_metadata_enabled(self, individual=False):
        """
        Check if metadata is enabled.

        If ``individual==True``, return individual metadata info
        ``(time_stamp_start, time_stamp_end, frame_stamp, gate_delay, modulation_phase)``.
        Otherwise, return simply ``True`` or ``False`` depending on whether the basic group (time- and frame-stamps) is enabled.
        In this case, if the value is inconsistent with either for the groups, fix this to be consistent.
        """
        if individual:
            return (bool(self.get_attribute_value("Time Stamps",enum_as_str=False)&self._ts_exposure_start),
                    bool(self.get_attribute_value("Time Stamps",enum_as_str=False)&self._ts_exposure_end),
                    self.cav["Track Frames"],
                    self.get_attribute_value("Gate Tracking",error_on_missing=False,default=False),
                    self.get_attribute_value("Modulation Tracking",error_on_missing=False,default=False))
        ind=self.is_metadata_enabled(individual=True)
        if ind not in [(False,)*5,(True,True,True,False,False)]:
            self.enable_metadata(any(ind[:3]))
        return any(ind[:3])
    def _get_metadata_sizes(self, ensure_complete=True):
        fs=self.get_attribute_value("Time Stamps",enum_as_str=False)
        fss=(self.cav["Time Stamp Bit Depth"]-1)//8+1
        ts=self.cav["Track Frames"]
        tss=(self.cav["Frame Tracking Bit Depth"]-1)//8+1
        sizes=(fss if fs&self._ts_exposure_start else 0), (fss if fs&self._ts_exposure_end else 0), (tss if ts else 0)
        return sizes if all(sizes) or not ensure_complete else None
    
    def get_exposure(self):
        return self.cav["Exposure Time"]*1E-3
    def set_exposure(self, exposure):
        self.cav["Exposure Time"]=exposure*1E3
        return self.get_exposure()
    def get_frame_period(self, per_readout=False):  # pylint: disable=arguments-differ
        """
        Get frame period (time between two consecutive frames in the internal trigger mode)

        If ``per_readout==True``, return time difference between readouts, which can contain more than one frame;
        otherwise, return average time per frame (keep in mind that the frames still come in single unbroken readout).
        """
        period=1./self.cav["Readout Rate Calculation"]
        return period if per_readout else period/self.cav["Frames per Readout"]
    def get_frame_timings(self, per_readout=False):  # pylint: disable=arguments-differ
        """
        Get acquisition timing.

        Return tuple ``(exposure, frame_period)``.
        If ``per_readout==True``, frame period difference between readouts, which can contain more than one frame;
        otherwise, it is the time per frame (keep in mind that the frames still come in single unbroken readout).
        """
        return self._TAcqTimings(self.cav["Exposure Time"]*1E-3,self.get_frame_period(per_readout=per_readout))



    def _get_data_dimensions_rc(self):
        roi=self.get_roi()
        w,h=(roi[1]-roi[0])//roi[4],(roi[3]-roi[2])//roi[5]
        return h,w
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        return self.cav["Sensor Active Width"],self.cav["Sensor Active Height"]
    def get_roi(self):
        rois=self.cav["ROIs"]
        if len(rois)>1:
            raise PicamError("only single ROI is supported")
        x,w,xb,y,h,yb=rois[0]
        return x,x+w,y,y+h,xb,yb
    def _limit_bin(self, b, bins, maxbin):
        if not bins:
            return max(1,min(b,maxbin))
        return min(bins[max(bisect.bisect_right(sorted(bins),b)-1,0)],maxbin)
    @camera.acqcleared
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        rcons=self.ca["ROIs"].cons_roi
        wdet,hdet=self.get_detector_size()
        hbin=self._limit_bin(hbin,rcons.xbins,wdet)
        vbin=self._limit_bin(vbin,rcons.ybins,hdet)
        hlim,vlim=self.get_roi_limits(hbin,vbin)
        hstart,hend,_=self._truncate_roi_axis((hstart,hend,hbin),hlim)
        vstart,vend,_=self._truncate_roi_axis((vstart,vend,vbin),vlim)
        self.cav["ROIs"]=[(hstart,hend-hstart,hbin,vstart,vend-vstart,vbin)]
        return self.get_roi()
    def get_roi_limits(self, hbin=1, vbin=1):
        wdet,hdet=self.get_detector_size()
        self.ca["ROIs"].update_limits()
        c=self.ca["ROIs"].cons_roi
        hlim=camera.TAxisROILimit(c.wrng[0]*hbin,c.wrng[1],c.xrng[2],c.wrng[2]*hbin,(max(c.xbins) if c.xbins else wdet))
        vlim=camera.TAxisROILimit(c.hrng[0]*vbin,c.hrng[1],c.yrng[2],c.hrng[2]*vbin,(max(c.ybins) if c.ybins else hdet))
        return hlim,vlim
    

    def _commit_parameters(self):
        failed=lib.Picam_CommitParameters(self.handle)
        if failed:
            failed=[_get_str(PicamEnumeratedType.PicamEnumeratedType_Parameter,p) for p in failed]
            raise PicamError("failed to commit following parameters: {}".format(failed))
    def _allocate_buffer(self, readout_bytes, frame_bytes, nreadouts):
        self._deallocate_buffer()
        self._readout_bytes=readout_bytes
        self._frame_bytes=frame_bytes
        self._buffer_readouts=nreadouts
        self._buffer=ctypes.create_string_buffer(readout_bytes*nreadouts)
        lib.PicamAdvanced_SetAcquisitionBuffer(self.devhandle,ctypes.addressof(self._buffer),readout_bytes*nreadouts)
    def _deallocate_buffer(self):
        lib.PicamAdvanced_SetAcquisitionBuffer(self.devhandle,0,0)
        self._buffer=None
    @interface.use_parameters(mode="acq_mode")
    def setup_acquisition(self, mode="sequence", nframes=100):  # pylint: disable=arguments-differ
        """
        Setup acquisition mode.

        `mode` can be either ``"snap"`` (single frame or a fixed number of frames) or ``"sequence"`` (continuous acquisition).
        `nframes` sets up number of frame buffers. If there are multiple frames per readout, it still means the number of frames,
        and the number of readouts is set up to contain all required frames (e.g., 10 frames per readout and 15 frames result in 2 readouts).
        """
        self.clear_acquisition()
        super().setup_acquisition(mode=mode,nframes=nframes)
        self._frames_per_readout=self.cav["Frames per Readout"]
        nreadouts=(nframes-1)//self._frames_per_readout+1
        self._allocate_buffer(self.cav["Readout Stride"],self.cav["Frame Stride"],nreadouts)
        if mode=="snap":
            self.cav["Readout Count"]=nreadouts
        else:
            self.cav["Readout Count"]=0
    def clear_acquisition(self):
        self.stop_acquisition()
        self._deallocate_buffer()
        super().clear_acquisition()
    def start_acquisition(self, *args, **kwargs):
        self.stop_acquisition()
        if self._readout_bytes!=self.cav["Readout Stride"] or self._frame_bytes!=self.cav["Frame Stride"]:
            self.clear_acquisition()
        super().start_acquisition(*args,**kwargs)
        self._waited_readouts=0
        self._frame_counter.reset(self._buffer_readouts*self._frames_per_readout)
        self._commit_parameters()
        lib.Picam_StartAcquisition(self.handle)
    def stop_acquisition(self):
        if self.acquisition_in_progress():
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
            self._waited_readouts=0
            lib.Picam_StopAcquisition(self.handle)
            while True:
                try:
                    _,status=lib.Picam_WaitForAcquisitionUpdate(self.handle,10)
                    if not status.running:
                        break
                except PicamLibError as err:
                    if err.code!=picam_defs.PicamError.PicamError_TimeOutOccurred:
                        raise
                    break
        super().stop_acquisition()
    def acquisition_in_progress(self):
        return lib.Picam_IsAcquisitionRunning(self.handle)
    def _wait_for_acquisition_update(self, timeout=0, reps=1):
        if self.acquisition_in_progress():
            for _ in range(reps):
                try:
                    avail,_=lib.Picam_WaitForAcquisitionUpdate(self.handle,timeout)
                    if avail.initial_readout is not None:
                        expected_next_frame=ctypes.addressof(self._buffer)+(self._waited_readouts%self._buffer_readouts)*self._readout_bytes
                        if expected_next_frame!=avail.initial_readout:
                            expected_next_buffer=(expected_next_frame-ctypes.addressof(self._buffer))/self._readout_bytes
                            got_next_buffer=(avail.initial_readout-ctypes.addressof(self._buffer))/self._readout_bytes
                            raise RuntimeError("expected address {} (buffer {}), got address {} (buffer {})".format(expected_next_frame,expected_next_buffer,avail.initial_readout,got_next_buffer))
                        self._waited_readouts+=avail.readout_count
                except PicamLibError as err:
                    if err.code!=picam_defs.PicamError.PicamError_TimeOutOccurred:
                        raise
                    break
    def _get_acquired_frames(self):
        self._wait_for_acquisition_update(reps=3)
        return self._waited_readouts*self._frames_per_readout

    def _wait_for_next_frame(self, timeout=20, idx=None):
        self._wait_for_acquisition_update(100)
    


    _struct_vals={1:"B",2:"<H",4:"<I",8:"<Q"}
    def _parse_metadata(self, ptr, sizes):
        vals=[]
        for s in sizes:
            if s:
                v,=struct.unpack(self._struct_vals[s],ctypes.string_at(ptr,s))
                vals.append(v)
                ptr+=s
        return vals
    def _parse_readout(self, ptr, shape, bpp=None, metadata_sizes=None, subrng=None):
        height,width=shape
        imsize=height*width*bpp
        if subrng is None:
            subrng=(0,self._frames_per_readout)
        imgs=[]
        metadatas=[]
        for i in range(*subrng):
            if metadata_sizes is not None:
                metadata=self._parse_metadata(ptr+imsize+i*self._frame_bytes,metadata_sizes)
            else:
                metadata=None
            metadatas.append(metadata)
            img=np.ctypeslib.as_array(ctypes.cast(ptr+i*self._frame_bytes,ctypes.POINTER(ctypes.c_ubyte)),shape=(imsize,))
            dtype="<u{}".format(bpp)
            imgs.append(img.view(dtype).reshape((height,width)).copy())
        imgs=[self._convert_indexing(img,"rct") for img in imgs]
        return imgs,metadatas
    def _read_frames(self, rng, return_info=False):
        if rng[1]<=rng[0]:
            return [],[]
        metadata_sizes=self._get_metadata_sizes() if return_info else None
        shape=self._get_data_dimensions_rc()
        base=ctypes.addressof(self._buffer)
        bpp=(self.cav["Pixel Bit Depth"]-1)//8+1
        fpr=self._frames_per_readout
        rostart=rng[0]//fpr
        roend=(rng[1]-1)//fpr
        if roend==rostart:
            readout_par=[(rostart,(rng[0]%fpr,(rng[1]-1)%fpr+1))]
        else:
            readout_par=[(rostart,(rng[0]%fpr,fpr))]+[(i,None) for i in range(rostart+1,roend)]+[(roend,(0,(rng[1]-1)%fpr+1))]
        readouts=[self._parse_readout(base+(i%self._buffer_readouts)*self._readout_bytes,shape,bpp=bpp,metadata_sizes=metadata_sizes,subrng=subrng)
            for i,subrng in readout_par]
        frames=[f for d in readouts for f in d[0]]
        if metadata_sizes is not None:
            raw_frame_info=[fi for d in readouts for fi in d[1]]
            frame_info=[TFrameInfo(n,*fi) for (n,fi) in zip(range(*rng),raw_frame_info)]
        else:
            frame_info=None
        return frames,frame_info
    def _zero_frame(self, n):
        dim=self.get_data_dimensions()
        bpp=(self.cav["Pixel Bit Depth"]-1)//8+1
        dt="<u{}".format(bpp)
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
        describing frame index and frame metadata, which contains start and stop timestamps, and framestamp;
        if some frames are missing and ``missing_frame!="skip"``, the corresponding frame info is ``None``.
        if ``return_rng==True``, return the range covered resulting frames; if ``missing_frame=="skip"``, the range can be smaller
        than the supplied `rng` if some frames are skipped.
        """
        return super().read_multiple_images(rng=rng,peek=peek,missing_frame=missing_frame,return_info=return_info,return_rng=return_rng)