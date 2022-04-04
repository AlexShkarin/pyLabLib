from . import dcamapi4_lib, dcamprop_defs
from .dcamapi4_lib import wlib as lib, DCAMError, DCAMLibError

from ...core.devio import interface
from ...core.utils import py3, general
from ..interface import camera
from ..utils import load_lib

import numpy as np
import collections
import ctypes
import warnings


class DCAMTimeoutError(DCAMError):
    "DCAM frame timeout error"


class LibraryController(load_lib.LibraryController):
    def __init__(self, lib):  # pylint: disable=redefined-outer-name
        super().__init__(lib)
        self.cameras=0
    def _do_init(self):
        self.cameras=self.lib.dcamapi_init()
    def _do_uninit(self):
        self.lib.dcamapi_uninit()
        self.cameras=None
libctl=LibraryController(lib)
def restart_lib():
    libctl.shutdown()



def get_cameras_number():
    """Get number of connected DCAM cameras"""
    try:
        with libctl.temp_open():
            return libctl.cameras
    except DCAMError:
        return 0





class DCAMAttribute:
    """
    DCAM camera attribute.

    Allows to query and set values and get additional information.
    Usually created automatically by a DCAM camera instance, but could also be created manually.

    Args:
        handle: DCAM camera handle
        pid: attribute id

    Attributes:
        name: attribute name
        kind (str): attribute kind; can be ``"int"``, ``"float"``, ``"enum"``, or ``"none"`` (can't determine)
        readable (bool): whether attribute is readable
        writable (bool): whether attribute is writable
        min (float): minimal attribute value (if applicable)
        max (float): maximal attribute value (if applicable)
        step (float): attribute value step (if applicable)
        unit (int): attribute units (index value)
        ivalues: list of possible integer values for enum attributes
        values: list of possible text values for enum attributes
        labels: dict ``{label: index}`` which shows all possible values of an enumerated attribute and their corresponding numerical values
        ilabels: dict ``{index: label}`` which shows labels corresponding to numerical values of an enumerated attribute
    """
    def __init__(self, handle, pid):
        self.handle=handle
        self.pid=pid
        self.name=py3.as_str(lib.dcamprop_getname(self.handle,pid))
        props=lib.dcamprop_getattr(self.handle,pid)
        self.min=props.valuemin
        self.max=props.valuemax
        self.step=props.valuestep
        self.default=props.valuedefault
        self.unit=props.iUnit
        self._attributes_n=props.attribute%0x100000000
        self.readable=bool(self._attributes_n&dcamprop_defs.DCAMPROPATTRIBUTE.DCAMPROP_ATTR_READABLE)
        self.writable=bool(self._attributes_n&dcamprop_defs.DCAMPROPATTRIBUTE.DCAMPROP_ATTR_WRITABLE)
        kinds={dcamprop_defs.DCAMPROPATTRIBUTE.DCAMPROP_TYPE_LONG:"int",dcamprop_defs.DCAMPROPATTRIBUTE.DCAMPROP_TYPE_REAL:"float",dcamprop_defs.DCAMPROPATTRIBUTE.DCAMPROP_TYPE_MODE:"enum"}
        self.kind=kinds.get(self._attributes_n&dcamprop_defs.DCAMPROPATTRIBUTE.DCAMPROP_TYPE_MASK,"none")
        self.values=[]
        self.ivalues=[]
        self.labels={}
        self.ilabels={}
        if self.kind=="enum":
            self._update_enum_limits()
        if self.kind in ["enum","int"]:
            self.min=int(self.min)
            self.max=int(self.max)
            self.step=int(self.step)
            self.default=int(self.default)
    def as_text(self, value=None):
        """Get the given attribute value as text (by default, current value)"""
        if value is None:
            return self.get_value(enum_as_str=True)
        return py3.as_str(lib.dcamprop_getvaluetext(self.handle,self.pid,value))
    def _update_enum_limits(self):
        self.values=[]
        self.ivalues=[]
        for v in range(int(self.min),int(self.max)+1):
            try:
                tv=self.as_text(v)
                self.values.append(tv)
                self.ivalues.append(v)
            except DCAMLibError:
                pass
        self.labels=dict(zip(self.values,self.ivalues))
        self.ilabels=dict(zip(self.ivalues,self.values))
    def update_limits(self):
        """Update minimal and maximal attribute limits and return tuple ``(min, max)``"""
        props=lib.dcamprop_getattr(self.handle,self.pid)
        self.min=props.valuemin
        self.max=props.valuemax
        if self.kind=="enum":
            self._update_enum_limits()
        return (self.min,self.max)
    def get_value(self, enum_as_str=False):
        """
        Get current attribute value.
        
        If ``enum_as_str==True``, try to represent enums as their string values;
        otherwise, return their integer values (only integers can be used for setting).
        """
        value=lib.dcamprop_getvalue(self.handle,self.pid)
        if self.kind in ["enum","int"]:
            value=int(value)
        if enum_as_str:
            try:
                return self.as_text(value)
            except DCAMLibError:
                pass
        return value
    def set_value(self, value):
        """Set attribute value"""
        return lib.dcamprop_setgetvalue(self.handle,self.pid,value)
    def __repr__(self):
        return "{}(name='{}', kind={}, id={}, min={}, max={}, unit={})".format(self.__class__.__name__,self.name,self.kind,self.pid,self.min,self.max,self.unit)



TDeviceInfo=collections.namedtuple("TDeviceInfo",["vendor","model","serial_number","camera_version"])
TFrameInfo=collections.namedtuple("TFrameInfo",["frame_index","framestamp","timestamp_us","camerastamp","position","pixeltype"])
class DCAMCamera(camera.IBinROICamera, camera.IExposureCamera, camera.IAttributeCamera):
    Error=DCAMError
    TimeoutError=DCAMTimeoutError
    _TFrameInfo=TFrameInfo
    _frameinfo_fields=general.make_flat_namedtuple(TFrameInfo,fields={"position":camera.TFramePosition})._fields
    def __init__(self, idx=0):
        super().__init__()
        self.idx=idx
        self.handle=None
        self._opid=None
        self.dcamwait=None
        self._alloc_nframes=0
        self._readout_speeds={}
        self._trigger_modes={}
        self.open()

        self._add_camera_parameters()
        self._add_info_variable("device_info",self.get_device_info)
        self._add_settings_variable("trigger_mode",self.get_trigger_mode,self.set_trigger_mode,ignore_error=ValueError)
        self._add_info_variable("all_trigger_modes",self.get_all_trigger_modes)
        self._add_settings_variable("ext_trigger",self.get_ext_trigger_parameters,self.setup_ext_trigger)
        self._add_settings_variable("readout_speed",self.get_readout_speed,self.set_readout_speed,ignore_error=ValueError)
        self._add_info_variable("all_readout_speeds",self.get_all_readout_speeds)
        self._add_settings_variable("defect_correct_mode",self.get_defect_correct_mode,self.set_defect_correct_mode,ignore_error=ValueError)
        self._add_status_variable("readout_time",self.get_frame_readout_time)
        self._add_status_variable("acq_status",self.get_status)
        self._add_status_variable("transfer_info",self.get_transfer_info)
        self._update_device_variable_order("exposure")
        self._add_status_variable("frame_period",self.get_frame_period)
        
    def _get_connection_parameters(self):
        return self.idx
    def open(self):
        """Open connection to the camera"""
        if self.handle is not None:
            return
        with libctl.temp_open():
            ncams=get_cameras_number()
            if self.idx>=ncams:
                raise DCAMError("camera index {} is not available ({} cameras exist)".format(self.idx,ncams))
            try:
                self.handle=lib.dcamdev_open(self.idx)
                self._opid=libctl.open().opid
                self.dcamwait=lib.dcamwait_open(self.handle)
                self._update_attributes()
                self._valid_binnings=self._get_valid_binnings()
            except DCAMError:
                self.close()
                raise
    def close(self):
        """Close connection to the camera"""
        if self.handle:
            self.clear_acquisition()
            lib.dcamwait_close(self.dcamwait.hwait)
            lib.dcamdev_close(self.handle)
            libctl.close(self._opid)
        self.handle=None
        self._opid=None
    def is_opened(self):
        """Check if the device is connected"""
        return self.handle is not None

    def _add_camera_parameters(self):
        rsprop=self.get_attribute("READOUT SPEED",error_on_missing=False)
        rspar=interface.RangeParameterClass("readout_speed",1,None)
        if rsprop is not None:
            if rsprop.max==1:
                self._readout_speeds={"fast":1}
            if rsprop.max==2:
                self._readout_speeds={"slow":1,"fast":2}
            elif rsprop.max==3:
                self._readout_speeds={"slow":1,"normal":2,"fast":3}
            rspar=interface.EnumParameterClass("readout_speed",self._readout_speeds)
        self._add_parameter_class(rspar)
        tsprop=self.get_attribute("TRIGGER SOURCE",error_on_missing=False)
        tspar=interface.RangeParameterClass("trigger_mode",1,None)
        if tsprop is not None and tsprop.max<=4:
            self._trigger_modes={"int":1,"ext":2,"software":3,"master_pulse":4}
            tspar=interface.EnumParameterClass("trigger_mode",self._trigger_modes)
        self._add_parameter_class(tspar)
                
        

    def get_device_info(self):
        """
        Get camera model data.

        Return tuple ``(vendor, model, serial_number, camera_version)``.
        """
        vendor=py3.as_str(lib.dcamdev_getstring(self.handle,dcamapi4_lib.DCAM_IDSTR.DCAM_IDSTR_VENDOR))
        model=py3.as_str(lib.dcamdev_getstring(self.handle,dcamapi4_lib.DCAM_IDSTR.DCAM_IDSTR_MODEL))
        serial_number=py3.as_str(lib.dcamdev_getstring(self.handle,dcamapi4_lib.DCAM_IDSTR.DCAM_IDSTR_CAMERAID))
        camera_version=py3.as_str(lib.dcamdev_getstring(self.handle,dcamapi4_lib.DCAM_IDSTR.DCAM_IDSTR_CAMERAVERSION))
        return TDeviceInfo(vendor,model,serial_number,camera_version)

    def _list_attributes(self):
        ids=lib.dcamprop_getallids(self.handle,0)
        return [DCAMAttribute(self.handle,pid) for pid in ids]
    def _normalize_attribute_name(self, name):
        return name.lower().replace(" ","_")
    def get_attribute_value(self, name, enum_as_str=False, error_on_missing=True, default=None):  # pylint: disable=arguments-differ
        """
        Get value of an attribute with the given name.
        
        If the value doesn't exist or can not be read and ``error_on_missing==True``, raise error; otherwise, return `default`.
        If `default` is not ``None``, assume that ``error_on_missing==False``.
        If ``enum_as_str==True``, try to represent enums as their string values;
        otherwise, return their integer values (only integers can be used for setting).
        """
        return super().get_attribute_value(name,enum_as_str=enum_as_str,error_on_missing=error_on_missing,default=default)
    def set_attribute_value(self, name, value, error_on_missing=True):  # pylint: disable=arguments-differ
        """
        Set value of an attribute with the given name.
        
        If the value doesn't exist or can not be written and ``error_on_missing==True``, raise error; otherwise, do nothing.
        """
        return super().set_attribute_value(name,value,error_on_missing=error_on_missing)
    def get_all_attribute_values(self, root="", enum_as_str=False):  # pylint: disable=arguments-differ, arguments-renamed
        """
        Get values of all attributes.

        If ``enum_as_str==True``, try to represent enums as their string values;
        otherwise, return their integer values (only integers can be used for setting).
        """
        return super().get_all_attribute_values(root=root,enum_as_str=enum_as_str)
    def set_all_attribute_values(self, settings):  # pylint: disable=arguments-differ
        """Set values of all attribute in the given dictionary"""
        return super().set_all_attribute_values(settings)

    @camera.acqstopped
    @interface.use_parameters(mode="trigger_mode")
    def set_trigger_mode(self, mode):
        """
        Set trigger mode.

        Can be ``"int"`` (internal), ``"ext"`` (external), or ``"software"`` (software trigger).
        """
        self.cav["TRIGGER SOURCE"]=mode
        return self.get_trigger_mode()
    @interface.use_parameters(_returns="trigger_mode")
    def get_trigger_mode(self):
        """
        Get trigger mode.

        Can be ``"int"`` (internal), ``"ext"`` (external), or ``"software"`` (software trigger).
        """
        return int(self.cav["TRIGGER SOURCE"])
    def get_all_trigger_modes(self):
        """Return the list of all available trigger modes"""
        return list(self._trigger_modes)
    def setup_ext_trigger(self, invert=False, delay=0.):
        """Setup external trigger (inversion and delay)"""
        self.cav["TRIGGER POLARITY"]=2 if invert else 1
        self.set_attribute_value("TRIGGER DELAY",delay,error_on_missing=False)
        return self.get_ext_trigger_parameters()
    def get_ext_trigger_parameters(self):
        """Return external trigger parameters (inversion and delay)"""
        invert=self.cav["TRIGGER POLARITY"]==2
        delay=self.get_attribute_value("TRIGGER DELAY",default=0)
        return invert,delay
    def send_software_trigger(self):
        """Send software trigger signal"""
        lib.dcamcap_firetrigger(self.handle)
    def set_exposure(self, exposure):
        """Set camera exposure"""
        self.cav["EXPOSURE TIME"]=exposure
        return self.get_exposure()
    def get_exposure(self):
        """Set current exposure"""
        return self.cav["EXPOSURE TIME"]
    @camera.acqcleared
    @interface.use_parameters(speed="readout_speed")
    def set_readout_speed(self, speed="fast"):
        """Set readout speed (can be ``"fast"`` or ``"slow"``)"""
        self.set_attribute_value("READOUT SPEED",speed,error_on_missing=False)
        return self.get_readout_speed()
    @interface.use_parameters(_returns="readout_speed")
    def get_readout_speed(self):
        """Set current readout speed"""
        return self.get_attribute_value("READOUT SPEED",default=1)
    def get_all_readout_speeds(self):
        """Return the list of all available readout speeds"""
        return list(self._readout_speeds)
    def get_frame_readout_time(self):
        """Set current frame readout time"""
        return self.cav["TIMING READOUT TIME"]
    def get_frame_timings(self):
        """
        Get acquisition timing.

        Return tuple ``(exposure, frame_period)``.
        """
        exposure=self.get_exposure()
        return self._TAcqTimings(exposure,max(exposure,self.get_frame_readout_time()))
    def get_defect_correct_mode(self):
        """Check if the defect pixel correction mode is on"""
        return self.get_attribute_value("DEFECT CORRECT MODE",default=1)==2
    @camera.acqstopped
    def set_defect_correct_mode(self, enabled=True):
        """Enable or disable the defect pixel correction mode"""
        self.set_attribute_value("DEFECT CORRECT MODE",2 if enabled else 1,error_on_missing=False)
        return self.get_defect_correct_mode()

    def _allocate_buffer(self, nframes):
        self._deallocate_buffer()
        if nframes:
            lib.dcambuf_alloc(self.handle,nframes)
        self._alloc_nframes=nframes
    def _deallocate_buffer(self):
        if self._alloc_nframes:
            lib.dcambuf_release(self.handle,0)
            self._alloc_nframes=0
    def _read_buffer(self, buffer):
        return lib.dcambuf_lockframe(self.handle,buffer)
    def _buffer_to_array(self, buffer): # TODO: different packing / color modes (generic for all cameras)
        bpp=int(buffer.bpp)
        if bpp==1:
            ct=ctypes.c_uint8*buffer.btot
        elif bpp==2:
            ct=ctypes.c_uint16*(buffer.btot//2)
        elif bpp==4:
            ct=ctypes.c_uint32*(buffer.btot//4)
        else:
            raise DCAMError("can't convert data with {} BBP into an array".format(bpp))
        data=ct.from_address(buffer.buf)
        img=np.array(data).reshape((buffer.height,buffer.width))
        return self._convert_indexing(img,"rct")

    def _get_data_dimensions_rc(self):
        return int(self.cav["IMAGE HEIGHT"]),int(self.cav["IMAGE WIDTH"])
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        return (int(self.get_attribute("SUBARRAY HSIZE").max),int(self.get_attribute("SUBARRAY VSIZE").max))
    def get_roi(self):
        """
        Get current ROI.

        Return tuple ``(hstart, hend, vstart, vend, hbin, vbin)``.
        """
        hstart=int(self.cav["SUBARRAY HPOS"])
        hend=hstart+int(self.cav["SUBARRAY HSIZE"])
        vstart=int(self.cav["SUBARRAY VPOS"])
        vend=vstart+int(self.cav["SUBARRAY VSIZE"])
        hvbin=int(self.cav["BINNING"])
        return (hstart,hend,vstart,vend,hvbin,hvbin)
    def _get_valid_binnings(self):
        bmax=min(self.get_detector_size())
        valid_bins=[]
        p=self.get_attribute("BINNING")
        for b in range(1,bmax+1):
            try:
                p.as_text(b)
                valid_bins.append(b)
            except DCAMLibError:
                if b>4 and b>valid_bins[-1]*4:
                    break
        return valid_bins
    def _truncate_roi_binning(self, binv):
        return max([b for b in self._valid_binnings if b<=binv]) if binv>=1 else 1
    @camera.acqcleared
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        """
        Set current ROI.

        By default, all non-supplied parameters take extreme values.
        Binning is the same for both axes, so value of `vbin` is ignored (it is left for compatibility).
        """
        self.cav["SUBARRAY MODE"]=2
        hlim,vlim=self.get_roi_limits()
        hbin=self._truncate_roi_binning(hbin)
        hstart,hend,hbin=self._truncate_roi_axis((hstart,hend,hbin),hlim)
        vstart,vend,vbin=self._truncate_roi_axis((vstart,vend,hbin),vlim)
        chstart,_,cvstart,_=self.get_roi()[:4]
        self.cav["BINNING"]=1
        if hstart<=chstart:
            self.cav["SUBARRAY HPOS"]=hstart
            self.cav["SUBARRAY HSIZE"]=hend-hstart
        else:
            self.cav["SUBARRAY HSIZE"]=hend-hstart
            self.cav["SUBARRAY HPOS"]=hstart
        if vstart<=cvstart:
            self.cav["SUBARRAY VPOS"]=vstart
            self.cav["SUBARRAY VSIZE"]=vend-vstart
        else:
            self.cav["SUBARRAY VSIZE"]=vend-vstart
            self.cav["SUBARRAY VPOS"]=vstart
        self.cav["BINNING"]=hbin
        return self.get_roi()
    def get_roi_limits(self, hbin=1, vbin=1):
        params=[self.ca[p] for p in ["SUBARRAY HPOS","SUBARRAY VPOS","SUBARRAY HSIZE","SUBARRAY VSIZE"]]
        minp=tuple([int(p.min) for p in params])
        maxp=tuple([int(p.max) for p in params])
        stepp=tuple([int(p.step) for p in params])
        hlim=camera.TAxisROILimit(minp[2],maxp[2],stepp[0],stepp[2],self._valid_binnings[-1])
        vlim=camera.TAxisROILimit(minp[3],maxp[3],stepp[1],stepp[3],self._valid_binnings[-1])
        return hlim,vlim

    @interface.use_parameters(mode="acq_mode")
    def setup_acquisition(self, mode="sequence", nframes=100):  # pylint: disable=arguments-differ
        """
        Setup acquisition.

        `mode` can be either ``"snap"`` (single frame or a fixed number of frames) or ``"sequence"`` (continuous acquisition).
        `nframes` determines number of frames to acquire in the single mode, or size of the ring buffer in the ``"sequence"`` mode (by default, 100).
        """
        super().setup_acquisition(mode=mode,nframes=nframes)
        if self._acq_params["nframes"]!=self._alloc_nframes:
            self.stop_acquisition()
            self._allocate_buffer(nframes)
    def clear_acquisition(self):
        self.stop_acquisition()
        self._deallocate_buffer()
        super().clear_acquisition()

    def start_acquisition(self, *args, **kwargs):
        self.stop_acquisition()
        super().start_acquisition(*args,**kwargs)
        lib.dcamcap_start(self.handle,-1 if self._acq_params["mode"]=="sequence" else 0)
        self._frame_counter.reset(self._alloc_nframes)
    def stop_acquisition(self):
        if self.acquisition_in_progress():
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
            lib.dcamcap_stop(self.handle)

    _p_acq_status=interface.EnumParameterClass("acq_status",{
        "error":dcamapi4_lib.DCAMCAP_STATUS.DCAMCAP_STATUS_ERROR,
        "busy":dcamapi4_lib.DCAMCAP_STATUS.DCAMCAP_STATUS_BUSY,
        "ready":dcamapi4_lib.DCAMCAP_STATUS.DCAMCAP_STATUS_READY,
        "stable":dcamapi4_lib.DCAMCAP_STATUS.DCAMCAP_STATUS_STABLE,
        "unstable":dcamapi4_lib.DCAMCAP_STATUS.DCAMCAP_STATUS_UNSTABLE,
        })
    @interface.use_parameters(_returns="acq_status")
    def get_status(self):
        """
        Get acquisition status.

        Can be ``"busy"`` (capturing in progress), ``"ready"`` (ready for capturing),
        ``"stable"`` (not prepared for capturing), ``"unstable"`` (can't be prepared for capturing), or ``"error"`` (some other error).
        """
        return lib.dcamcap_status(self.handle)
    def acquisition_in_progress(self):
        return self.get_status()=="busy"
    def get_transfer_info(self):
        """
        Get frame transfer info.

        Return tuple ``(last_buff, frame_count)``, where ``last_buff`` is the index of the last filled buffer,
        and ``frame_count`` is the total number of acquired frames.
        """
        return tuple(lib.dcamcap_transferinfo(self.handle,0))
    def _get_acquired_frames(self):
        return self.get_transfer_info()[1]


    def _wait_for_next_frame(self, timeout=20., idx=None):
        if timeout is None or timeout>0.1:
            timeout=0.1
        try:
            eventmask=dcamapi4_lib.DCAMWAIT_EVENT.DCAMWAIT_CAPEVENT_FRAMEREADY
            lib.dcamwait_start(self.dcamwait.hwait,eventmask,int(timeout*1000))
            return
        except DCAMLibError as e:
            if e.code==dcamapi4_lib.DCAMERR.DCAMERR_LOSTFRAME: # occasionally comes up; 
                warnings.warn("lost DCAM frame")
            elif e.code!=dcamapi4_lib.DCAMERR.DCAMERR_TIMEOUT:
                raise
    def _frame_info_to_namedtuple(self, info):
        return self._TFrameInfo(info[0],info[1],info[2],info[3],camera.TFramePosition(info[4:6]),info[6])
    def _get_single_frame(self, buffer):
        """
        Get a frame at the given buffer index.

        If ``return_info==True``, return tuple ``(data, info)``, where info is the :class:`TFrameInfo` instance
        describing frame index, timestamp, camera stamp, frame location on the sensor, and pixel type.
        Does not advance the read frames counter.
        """
        sframe=self._read_buffer(buffer%self._alloc_nframes)
        position=camera.TFramePosition(sframe.left,sframe.top)
        info=TFrameInfo(buffer,sframe.framestamp,sframe.timestamp[0]*10**6+sframe.timestamp[1],sframe.camerastamp,position,sframe.type)
        data=self._buffer_to_array(sframe)
        return data,info
    def _read_frames(self, rng, return_info=False):
        data=[self._get_single_frame(n) for n in range(rng[0],rng[1])]
        return [d[0] for d in data],[d[1] for d in data]
    def _zero_frame(self, n):
        dim=self.get_data_dimensions()
        bpp=int(self.get_attribute_value("BIT PER CHANNEL",default=8))
        dt="<u{}".format((bpp-1)//8+1)
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
        describing frame index, framestamp and timestamp, camera stamp, frame location on the sensor, and pixel type;
        if some frames are missing and ``missing_frame!="skip"``, the corresponding frame info is ``None``.
        if ``return_rng==True``, return the range covered resulting frames; if ``missing_frame=="skip"``, the range can be smaller
        than the supplied `rng` if some frames are skipped.
        """
        return super().read_multiple_images(rng=rng,peek=peek,missing_frame=missing_frame,return_info=return_info,return_rng=return_rng)