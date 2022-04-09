from . import sc2_camexport_lib
from .sc2_camexport_lib import wlib as lib, PCO_ERR, PCOSC2Error, PCOSC2LibError, PCO_INTERFACE, sc2_defs, CAPS1, MAX_SCHEDULED_BUFFERS

from ...core.utils import dictionary, py3, general, nbtools
from ...core.utils.ctypes_wrap import class_tuple_to_dict
from ...core.devio import interface
from ..interface import camera

import numpy as np
import collections
import time
import ctypes
import threading
import warnings



class PCOSC2TimeoutError(PCOSC2Error):
    "PCO SC2 frame timeout error"
class PCOSC2NotSupportedError(PCOSC2Error):
    """Option not supported error"""

_cam_interface_names={
    PCO_INTERFACE.PCO_INTERFACE_FW:"firewire",
    PCO_INTERFACE.PCO_INTERFACE_CL_MTX:"cl_mix",
    PCO_INTERFACE.PCO_INTERFACE_CL_ME3:"cl_sis_me3",
    PCO_INTERFACE.PCO_INTERFACE_CL_NAT:"cl_ni",
    PCO_INTERFACE.PCO_INTERFACE_GIGE:"gige",
    PCO_INTERFACE.PCO_INTERFACE_USB:"usb2",
    PCO_INTERFACE.PCO_INTERFACE_CL_ME4:"cl_sis_me4",
    PCO_INTERFACE.PCO_INTERFACE_USB3:"usb3",
    PCO_INTERFACE.PCO_INTERFACE_WLAN:"wlan",
    PCO_INTERFACE.PCO_INTERFACE_CLHS:"clhs" }
_cam_interface_names_inv=general.invert_dict(_cam_interface_names)
def list_cameras(cam_interface=None):
    """
    List camera connections (interface kind and camera index).
    
    If `cam_interface` is supplied, it defines one of camera interfaces to check (e.g., ``"usb3"`` or ``"clhs"``).
    Otherwise, check all interfaces.
    """
    if cam_interface is None:
        return [c for cam_interface in _cam_interface_names for c in list_cameras(cam_interface)]
    if cam_interface in _cam_interface_names_inv:
        cam_interface=_cam_interface_names_inv[cam_interface]
    elif not isinstance(cam_interface,int):
        raise ValueError("unrecognized interface: {}".format(cam_interface))
    lib.initlib()
    fails=0
    idx=0
    cams=[]
    while True:
        try:
            ch,desc=lib.PCO_OpenCameraEx(cam_interface,idx)
            lib.PCO_CloseCamera(ch)
            intf,num=desc.wInterfaceType,desc.wCameraNumAtInterface
            cams.append((_cam_interface_names.get(intf,intf),num))
            fails=0
        except PCOSC2LibError:
            fails+=1
            if idx==0 or fails>1:
                break
        idx+=1
    return cams
def get_cameras_number(cam_interface=None):
    """
    Get the total number of connected PCOSC2 cameras.
    
    If `cam_interface` is supplied, it defines one of camera interfaces to check (e.g., ``"usb3"`` or ``"clhs"``).
    Otherwise, check all interfaces.
    """
    return len(list_cameras(cam_interface=cam_interface))

def reset_api():
    """
    Reset API.

    All cameras must be closed; otherwise, the prompt to reboot will appear.
    """
    lib.initlib()
    lib.PCO_ResetLib()




TDeviceInfo=collections.namedtuple("TDeviceInfo",["model","interface","sensor","serial_number"])
TCameraStatus=collections.namedtuple("TCameraStatus",["status","warnings","errors"])
TInternalBufferStatus=collections.namedtuple("TInternalBufferStatus",["scheduled","scheduled_max","overruns"])
# TFrameInfo=collections.namedtuple("TFrameInfo",["frame_index","raw_metadata"])
TFrameInfo=collections.namedtuple("TFrameInfo",["frame_index"])
class PCOSC2Camera(camera.IBinROICamera, camera.IExposureCamera):
    """
    PCO SC2 camera.

    Args:
        idx(int): camera index (use :func:`get_cameras_number` to get the total number of connected cameras)
        cam_interface: camera interface; if it is ``None``, get the first available connected camera (in this case `idx` is ignored);
            if not, then value of `idx` is used to connect to a particular camera (interfaces and indices can be obtain from :func:`list_cameras`)
        reboot_on_fail(bool): if ``True`` and the camera raised an error during initialization (but after opening), reboot the camera and try to connect again
            useful when the camera is in a broken state (e.g., wrong ROI or pixel clock settings)
    """
    Error=PCOSC2Error
    TimeoutError=PCOSC2TimeoutError
    _TFrameInfo=TFrameInfo
    def __init__(self, idx=0, cam_interface=None, reboot_on_fail=True):
        super().__init__()
        lib.initlib()
        self.interface=cam_interface
        self.idx=idx
        self.handle=None
        self.reboot_on_fail=reboot_on_fail
        self._full_camera_data=dictionary.Dictionary()
        self._buffers=None
        self._full_buffer=None
        self._buffer_looping=False
        self._buffer_loop_thread=None
        self._next_schedule_buffer=0
        self._frame_notifier=camera.FrameNotifier()
        self._buffer_overruns=None
        self._status_line_enabled=False
        self.v=dictionary.ItemAccessor(lambda n:self._full_camera_data[n])
        self.open()

        self._device_var_ignore_error={"get":(PCOSC2NotSupportedError,),"set":()}
        self._add_info_variable("device_info",self.get_device_info)
        self._add_info_variable("capabilities",self.get_capabilities)
        self._add_info_variable("full_data",self.get_full_camera_data,priority=-8)
        self._add_status_variable("temperature_monitor",self.get_temperature)
        self._add_settings_variable("trigger_mode",self.get_trigger_mode,self.set_trigger_mode)
        self._add_settings_variable("frame_delay",self.get_frame_delay,self.set_frame_delay)
        self._add_settings_variable("frame_period",self.get_frame_period,self.set_frame_period)
        self._add_status_variable("internal_buffer_status",self.get_internal_buffer_status)
        self._add_settings_variable("bit_alignment",self.get_bit_alignment,self.set_bit_alignment)
        self._add_settings_variable("hotpixel_correction",self.is_pixel_correction_enabled,self.enable_pixel_correction)
        self._add_settings_variable("noise_filter",self.get_noise_filter_mode,self.set_noise_filter_mode)
        self._add_settings_variable("status_line",self.get_status_line_mode,self.set_status_line_mode)
        self._add_settings_variable("metadata_mode",self.get_metadata_mode,self.set_metadata_mode)
        self._add_settings_variable("pixel_rate",self.get_pixel_rate,self.set_pixel_rate)
        self._add_info_variable("all_pixel_rates",self.get_available_pixel_rates)
        self._add_info_variable("requires_symmetric_roi",self.requires_symmetric_roi)
        self._add_info_variable("conversion_factor",self.get_conversion_factor)
        self._add_status_variable("camera_status",self.get_camera_status)

    def _get_connection_parameters(self):
        return self.idx,self.interface
    _p_open_interface=interface.EnumParameterClass("open_interface",_cam_interface_names_inv)
    def open(self):
        """Open connection to the camera"""
        if self.handle is not None:
            return
        for t in range(2):
            if self.interface is None:
                self.handle=lib.PCO_OpenCamera()
            else:
                self.handle=lib.PCO_OpenCameraEx(self._p_open_interface(interface),self.idx)
            try:
                self.update_full_data()
                self.set_roi(*self.get_roi()) # ensure ROI
                return
            except PCOSC2Error:
                if self.reboot_on_fail and t==0:
                    self.reboot()
                else:
                    self.close()
                    raise
    def close(self):
        """Close connection to the camera"""
        if self.handle is not None:
            try:
                self.clear_acquisition()
            except PCOSC2LibError:
                pass
            lib.PCO_CloseCamera(self.handle)
        self.handle=None
    def is_opened(self):
        """Check if the device is connected"""
        return self.handle is not None
    def reboot(self, wait=True):
        """
        Reboot the camera.

        If ``wait==True``, wait for the recommended time (10 seconds) after reboot for the camera to fully restart;
        attempt to open the camera before that can lead to an error.
        """
        if self.handle is not None:
            lib.PCO_RebootCamera(self.handle)
            lib.PCO_CloseCamera(self.handle)
            self.handle=None
            if wait:
                time.sleep(10.)

    def get_full_camera_data(self):
        """Get a dictionary the all camera data available through the SDK"""
        cam_data=dictionary.Dictionary()
        for (i,name) in enumerate(["interface","camera","sensor","serial_number","fw_build","fw_rev"]):
            try:
                cam_data["info_strings",name]=py3.as_str(lib.PCO_GetInfoString(self.handle,i))
            except PCOSC2LibError as e:
                if not e.same_as(PCO_ERR.PCO_ERROR_FIRMWARE_VALUE_OUT_OF_RANGE):
                    raise
        cam_data["general"]=class_tuple_to_dict(lib.PCO_GetGeneral(self.handle),expand_lists=True)
        cam_data["sensor"]=class_tuple_to_dict(lib.PCO_GetSensorStruct(self.handle),expand_lists=True)
        cam_data["img_timing"]=class_tuple_to_dict(lib.PCO_GetImageTiming(self.handle),expand_lists=True)
        cam_data["timing"]=class_tuple_to_dict(lib.PCO_GetTimingStruct(self.handle),expand_lists=True)
        cam_data["storage"]=class_tuple_to_dict(lib.PCO_GetStorageStruct(self.handle),expand_lists=True)
        cam_data["recording"]=class_tuple_to_dict(lib.PCO_GetRecordingStruct(self.handle),expand_lists=True)
        cam_data["image"]=class_tuple_to_dict(lib.PCO_GetImageStruct(self.handle),expand_lists=True)
        signal_num=len(cam_data["sensor/strSignalDesc"])
        for k in list(cam_data["timing/strSignal"].keys()):
            if int(k)>=signal_num:
                del cam_data["timing/strSignal",k]
        for k in list(cam_data["image/strSegment"].keys()):
            if cam_data["image/strSegment",k,"dwMaxImageCnt"]==0:
                del cam_data["image/strSegment",k]
        if "info_strings/serial_number" not in cam_data:
            cam_data["info_strings/serial_number"]=str(cam_data["general/strCamType/dwSerialNumber"])
        return cam_data
    
    def update_full_data(self):
        """
        Update internal full camera data settings.
        
        Takes some time (about 50ms), so more specific function are preferable for specific parameters.
        """
        self._arm()
        self._full_camera_data=self.get_full_camera_data()
        self._ncaps={n:self.v["sensor/strDescription/dwGeneralCapsDESC{}".format(n)] for n in [1,2,3,4]}
    def _arm(self):
        lib.PCO_ArmCamera(self.handle)

    _interface_codes={1:"firewire",2:"cl",3:"usb2",4:"gige",5:"serial",6:"usb3",7:"clhs"}
    def get_device_info(self):
        """
        Get camera model data.

        Return tuple ``(model, interface, sensor, serial_number)``.
        """
        intf=self._interface_codes.get(self.v["general/strCamType/wInterfaceType"],"unknown")
        return TDeviceInfo(self.v["info_strings/camera"],intf,self.v["info_strings/sensor"],self.v["info_strings/serial_number"])

    def _parse_flag_bits(self, value, caps):
        return [c.name for c in caps if value&c]
    def get_capabilities(self):
        """
        Get camera capabilities.

        For description of the capabilities, see PCO SC2 manual.
        """
        return self._parse_flag_bits(self._ncaps[1],CAPS1)
    def _has_option(self, option, caps=1):
        return bool(self._ncaps[caps]&option)
    def _check_option(self, option, caps=1, value=True):
        has_option=self._has_option(option,caps)
        if has_option!=value:
            name=getattr(option,"name",option)
            raise PCOSC2NotSupportedError("option {} is not supported by {}".format(name,self.get_device_info().model))
        return has_option
    def _is_pco_edge(self):
        return (self.v["general/strCamType/wCamType"]&0xFF00)==0x1300
    def _is_camlink(self):
        return self.v["general/strCamType/wInterfaceType"] in [2,7] # CL and CLHS
        

    ### Generic controls ###
    def _apply_timebase(self, value, timebase):
        return value*[1E-9,1E-6,1E-3][timebase]
    def _extract_timebase(self, value):
        if value<1.:
            return (int(value*1E9),0)
        elif value<1E3:
            return (int(value*1E6),1)
        else:
            return (int(value*1E3),2)
    def get_camera_status(self, full=False):
        """
        Get camera status.

        If ``full==True``, return current camera status as a set of enabled status states;
        otherwise, return tuple ``(status, warnings, errors)`` with additional information about warnings and error.
        """
        warn,err,stat=lib.PCO_GetCameraHealthStatus(self.handle)
        if full:
            return TCameraStatus(self._parse_flag_bits(stat,sc2_defs.STATUS),self._parse_flag_bits(warn,sc2_defs.WARNING),self._parse_flag_bits(err,sc2_defs.ERROR))
        else:
            return self._parse_flag_bits(stat,sc2_defs.STATUS)

    def get_temperature(self):
        """
        Get the current camera temperature
        
        Return tuple ``(CCD, cam, power)`` with temperatures of the sensor, camera, and power supply respectively.
        """
        tccd,tcam,tpow=lib.PCO_GetTemperature(self.handle)
        return (tccd/10.,tcam,tpow)
    def get_conversion_factor(self):
        """Get camera conversion factor (electrons per pixel value)"""
        return lib.PCO_GetConversionFactor(self.handle)/100.
    
    ### Trigger controls ###
    _trigger_mode={    "int":sc2_defs.TRIGGER.TRIGGER_MODE_AUTOTRIGGER,
                    "software":sc2_defs.TRIGGER.TRIGGER_MODE_SOFTWARETRIGGER,
                    "ext":sc2_defs.TRIGGER.TRIGGER_MODE_EXTERNALTRIGGER,
                    "ext_exp":sc2_defs.TRIGGER.TRIGGER_MODE_EXTERNALEXPOSURECONTROL,
                    "ext_sync":sc2_defs.TRIGGER.TRIGGER_MODE_EXTERNAL_SYNCHRONIZED,
                    "ext_exp_fast":sc2_defs.TRIGGER.TRIGGER_MODE_FAST_EXTERNALEXPOSURECONTROL,
                    "ext_cds":sc2_defs.TRIGGER.TRIGGER_MODE_EXTERNAL_CDS,
                    "ext_exp_slow":sc2_defs.TRIGGER.TRIGGER_MODE_SLOW_EXTERNALEXPOSURECONTROL,
                    "ext_sync_hdsdi":sc2_defs.TRIGGER.TRIGGER_MODE_SOURCE_HDSDI}
    _p_trigger_mode=interface.EnumParameterClass("trigger_mode",_trigger_mode)
    @interface.use_parameters(_returns="trigger_mode")
    def get_trigger_mode(self):
        """Get current trigger mode (see :meth:`set_trigger_mode` for description)"""
        return lib.PCO_GetTriggerMode(self.handle)
    @interface.use_parameters(mode="trigger_mode")
    def set_trigger_mode(self, mode):
        """
        Set trigger mode.

        Can be ``"int"`` (internal), ``"software"`` (software), ``"ext"`` (external+software), ``"ext_exp"`` (external exposure), ``"ext_sync"`` (external PLL sync),
        ``"ext_exp_fast"`` (fast external exposure), ``"ext_cds"`` (external CDS control),
        ``"ext_exp_slow"`` (slow external exposure)`, or ``"ext_sync_hdsdi"`` (external synchronized SD/HDI).

        For description, see PCO SDK manual.
        """
        lib.PCO_SetTriggerMode(self.handle,mode)
        self._arm()
        return self.get_trigger_mode()
    def send_software_trigger(self):
        """Send software trigger signal"""
        return bool(lib.PCO_ForceTrigger(self.handle))

    ### Acquisition controls ###
    class Buffer:
        """Single frame buffer object, which controls setup, cleanup, and synchronization"""
        def __init__(self, buff, size, metadata_size=0):
            self.buff=buff
            self.event=lib.CreateEvent()
            self.size=size
            self.status=sc2_camexport_lib.DWORD()
            self.metadata_size=metadata_size
            self.lock=threading.Lock()
        def wait(self, timeout):
            if not self.lock.acquire(timeout=(-1 if timeout is None else timeout)):
                return False
            wait_res=lib.WaitForSingleObject(self.event,(-1 if timeout is None else np.int32(timeout*1000)))==0
            self.lock.release()
            return wait_res
        def is_done(self):
            return lib.WaitForSingleObject(self.event,0)==0
        def reset(self):
            with self.lock:
                lib.ResetEvent(self.event)
        def release(self):
            if self.buff is not None:
                lib.CloseHandle(self.event)
                self.buff=None
                self.event=None
    def _get_buffer_size(self):
        dim=self._get_data_dimensions_rc()
        mm_size=self._get_metadata_size()
        if mm_size>0:
            mm_size=((mm_size-1)//(dim[1]*2)+1)*(dim[1]*2)
        return dim[0]*dim[1]*2,mm_size
    def _allocate_buffers(self, n):
        frame_size,metadata_size=self._get_buffer_size()
        self._full_buffer=ctypes.create_string_buffer((frame_size+metadata_size)*n)
        buff_ptr=ctypes.addressof(self._full_buffer)
        self._buffers=[self.Buffer(buff_ptr+(frame_size+metadata_size)*i,frame_size+metadata_size,metadata_size=metadata_size) for i in range(n)]
        self._frame_notifier.reset()
        self._next_schedule_buffer=0
        return n
    def _schedule_buffer(self, buff, n=0):
        lib.PCO_AddBufferExtern(self.handle,buff.event,0,n,n,0,buff.buff,buff.size,ctypes.pointer(buff.status))
    def _schedule_all_buffers(self, n=None, set_idx=False):
        if self._buffers:
            if n is None:
                n=min(len(self._buffers),MAX_SCHEDULED_BUFFERS)
            for i,b in enumerate(self._buffers[:n]):
                self._schedule_buffer(b,i+1 if set_idx else 0)
                self._next_schedule_buffer+=1
    def _unschedule_all_buffers(self):
        if self._buffers:
            lib.PCO_CancelImages(self.handle)
    def _deallocate_buffers(self):
        if self._buffers is not None:
            for b in self._buffers:
                b.release()
            self._buffers=None
            self._full_buffer=None
    def _get_acquired_frames(self):
        return self._frame_notifier.counter
        
    def _loop_schedule_refresh_buffers(self):
        nbuff=len(self._buffers)
        nsched=min(nbuff,MAX_SCHEDULED_BUFFERS) # API limit on actually scheduled buffers
        while self._buffer_looping:
            actioned=False
            if self._frame_notifier.counter<self._next_schedule_buffer: # scheduled buffers available
                buff=self._buffers[self._frame_notifier.counter%nbuff]
                succ=buff.wait(timeout=0.001)
                if succ:
                    self._frame_notifier.inc()
                actioned=True
            if self._next_schedule_buffer<self._frame_notifier.counter+nsched:
                buff=self._buffers[self._next_schedule_buffer%nbuff]
                buff.reset()
                self._schedule_buffer(buff)
                self._next_schedule_buffer+=1
                actioned=True
            if not actioned:
                time.sleep(0.001)
    def _start_reading_loop(self):
        self._stop_reading_loop()
        self._buffer_overruns=0 if self._status_line_enabled else None
        self._buffer_loop_thread=threading.Thread(target=self._loop_schedule_refresh_buffers,daemon=True)
        self._buffer_looping=True
        self._buffer_loop_thread.start()
    def _stop_reading_loop(self):
        if self._buffer_loop_thread is not None:
            self._buffer_looping=False
            self._buffer_loop_thread.join()
            self._buffer_loop_thread=None
    def get_internal_buffer_status(self):
        """Get the status of the internal smaller API buffer, showing the number of scheduled frames there, and the maximal number that can be scheduled"""
        if self._buffers is None:
            return TInternalBufferStatus(0,0,0)
        size=len(self._buffers)
        scheduled=self._next_schedule_buffer-self._frame_notifier.counter
        scheduled_max=min(size,MAX_SCHEDULED_BUFFERS)
        return TInternalBufferStatus(scheduled,scheduled_max,self._buffer_overruns)
        
    

    def _get_full_timings(self):
        timings=lib.PCO_GetImageTiming(self.handle)
        exp=timings.ExposureTime_s+timings.ExposureTime_ns*1E-9
        frame_delay=timings.TriggerDelay_s+timings.TriggerDelay_ns*1E-9
        frame_time=timings.FrameTime_s+timings.FrameTime_ns*1E-9
        return exp,frame_delay,frame_time
    def _set_exposure_delay(self, exposure, frame_delay):
        exposure=max(exposure,self.v["sensor/strDescription/dwMinExposureDESC"]*1E-9)
        exposure=min(exposure,self.v["sensor/strDescription/dwMaxExposureDESC"]*1E-3)
        frame_delay=max(frame_delay,self.v["sensor/strDescription/dwMinDelayDESC"]*1E-9)
        frame_delay=min(frame_delay,self.v["sensor/strDescription/dwMaxDelayDESC"]*1E-3)
        ev,eb=self._extract_timebase(exposure)
        dv,db=self._extract_timebase(frame_delay)
        lib.PCO_SetDelayExposureTime(self.handle,dv,ev,db,eb)
        self._arm()
    def set_exposure(self, exposure):
        """Set camera exposure"""
        self._set_exposure_delay(exposure,self.get_frame_delay())
        return self.get_exposure()
    def get_exposure(self):
        """Get current exposure"""
        return self._get_full_timings()[0]
    def set_frame_delay(self, frame_delay):
        """Set camera frame delay"""
        self._set_exposure_delay(self.get_exposure(),frame_delay)
        return self.get_frame_delay()
    def get_frame_delay(self):
        """Get current frame delay"""
        return self._get_full_timings()[1]
    def set_frame_period(self, frame_time=0, adjust_exposure=False):
        """
        Set frame time (frame acquisition period).

        If the time can't be achieved even with zero frame delay and ``adjust_exposure==True``, try to reduce the exposure to get the desired frame time;
        otherwise, keep the exposure the same.
        """
        exposure,frame_delay,curr_frame_time=self._get_full_timings()
        if curr_frame_time-frame_delay<=frame_time:
            frame_delay=frame_delay+frame_time-curr_frame_time
        else:
            frame_delay=0
            if adjust_exposure:
                exposure=max(0,frame_delay+frame_time-curr_frame_time+exposure)
        self._set_exposure_delay(exposure,frame_delay)
        return self.get_frame_period()
    def get_frame_period(self):
        """Get current frame time (frame acquisition period)"""
        return self._get_full_timings()[2]
    def get_frame_timings(self):
        exp,_,frame_time=self._get_full_timings()
        return self._TAcqTimings(exp,frame_time)

    def get_pixel_rate(self):
        """Get camera pixel rate (in Hz)"""
        return lib.PCO_GetPixelRate(self.handle)
    def get_available_pixel_rates(self):
        """Get all available pixel rates"""
        rates=self.v["sensor/strDescription/dwPixelRateDESC"]
        rlist=[rates[k] for k in rates if rates[k]>0]
        return sorted(rlist)
    def set_pixel_rate(self, rate=None):
        """
        Set camera pixel rate (in Hz)

        The rate is always rounded to the closest available.
        If `rate` is ``None``, set the maximal possible rate.
        """
        rates=self.get_available_pixel_rates()
        if rate is None:
            rate=rates[-1]
        else:
            rate=sorted(rates,key=lambda r: abs(r-rate))[0]
        lib.PCO_SetPixelRate(self.handle,rate)
        if self.v["general/strCamType/wCamType"]==0x1300: # pco.edge 5.5 CL
            lib.PCO_SetTransferParametersAuto(self.handle)
        self._arm()
        return self.get_pixel_rate()


    ### Acquisition process controls ###
    def setup_acquisition(self, nframes=100):  # pylint: disable=arguments-differ
        """
        Setup acquisition.

        `nframes` determines number of size of the ring buffer (by default, 100).
        """
        super().setup_acquisition(nframes=nframes)
    def start_acquisition(self, *args, **kwargs):
        self.stop_acquisition()
        super().start_acquisition(*args,**kwargs)
        self._allocate_buffers(n=self._acq_params["nframes"])
        self._arm()
        self._status_line_enabled=self.get_status_line_mode()[0]
        if self._is_pco_edge() and self._is_camlink():
            self._schedule_all_buffers(set_idx=True)
            self._start_reading_loop()
            lib.PCO_SetRecordingState(self.handle,1)
        else:
            lib.PCO_SetRecordingState(self.handle,1)
            self._schedule_all_buffers(set_idx=False)
            self._start_reading_loop()
        self._frame_counter.reset(self._acq_params["nframes"])
    def stop_acquisition(self):
        """
        Stop acquisition.

        Clears buffers as well, so any readout afterwards is impossible.
        """
        self._stop_reading_loop()
        self._unschedule_all_buffers()
        lib.PCO_SetRecordingState(self.handle,0)
        self._deallocate_buffers()
        self._frame_counter.reset()
    def acquisition_in_progress(self):
        """Check if the acquisition is in progress"""
        return bool(lib.PCO_GetRecordingState(self.handle))
    def clear_acquisition(self):
        self.stop_acquisition()
        super().clear_acquisition()

    # ### Image settings and transfer controls ###
    def _get_data_dimensions_rc(self):
        sizes=lib.PCO_GetSizes(self.handle)
        return sizes[1],sizes[0]
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        return self.v["sensor/strDescription/wMaxHorzResStdDESC"],self.v["sensor/strDescription/wMaxVertResStdDESC"]
    def _adj_bin(self, binval, maxbin, binmode):
        binval=max(binval,1)
        binval=min(binval,maxbin)
        if binmode!=1:
            binval=int(2**np.floor(np.log2(binval)))
        return binval
    def _truncate_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1, soft_roi=False):
        hlim,vlim=self.get_roi_limits()
        hstart,hend,_=self._truncate_roi_axis((hstart,hend,hbin),hlim)
        vstart,vend,_=self._truncate_roi_axis((vstart,vend,vbin),vlim)
        hbinmode=self.v["sensor/strDescription/wBinHorzSteppingDESC"]
        hbin=self._adj_bin(hbin,hlim.maxbin,hbinmode)
        vbinmode=self.v["sensor/strDescription/wBinVertSteppingDESC"]
        vbin=self._adj_bin(vbin,vlim.maxbin,vbinmode)
        hlim,vlim=self.get_roi_limits(hbin=hbin,vbin=vbin)
        vsymm=self._has_option(CAPS1.GENERALCAPS1_ROI_VERT_SYMM_TO_HORZ_AXIS) or (self._is_pco_edge() and not soft_roi) # pco.edge must be symmetric, can with soft ROI activated it can be asymmetric for output
        hsymm=self._has_option(CAPS1.GENERALCAPS1_ROI_HORZ_SYMM_TO_VERT_AXIS)
        hstart,hend,_=self._truncate_roi_axis((hstart,hend,hbin),hlim,symmetric=hsymm)
        vstart,vend,_=self._truncate_roi_axis((vstart,vend,vbin),vlim,symmetric=vsymm)
        return hstart,hend,vstart,vend,hbin,vbin
    def get_roi(self):
        roi=lib.PCO_GetROI(self.handle)
        bins=lib.PCO_GetBinning(self.handle)
        return ((roi[0]-1)*bins[0],roi[2]*bins[0],(roi[1]-1)*bins[1],roi[3]*bins[1],bins[0],bins[1])
    @camera.acqcleared
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1, symmetric=False):  # pylint: disable=arguments-differ
        """
        Setup camera ROI.

        `hstart` and `hend` specify horizontal image extent, `vstart` and `vend` specify vertical image extent
        (start is inclusive, stop is exclusive, starting from 0), `hbin` and `vbin` specify binning.
        By default, all non-supplied parameters take extreme values (0 for start, maximal for end, 1 for binning).
        If ``symmetric==True`` and camera requires symmetric ROI (see :meth:`requires_symmetric_roi`), respect this symmetry in the resulting ROI;
        otherwise, try to use software ROI feature to set up the required ranges
        (note: while software ROI does affect the size of the read out frame, it does not change the readout time, which would be the same as with ``symmetric==True``).
        """
        roi=hstart,hend,vstart,vend,hbin,vbin
        hstart,hend,vstart,vend,hbin,vbin=self._truncate_roi(*roi)
        lib.PCO_EnableSoftROI(self.handle,0)
        self._arm()
        lib.PCO_SetROI(self.handle,hstart//hbin+1,vstart//vbin+1,hend//hbin,vend//vbin)
        lib.PCO_SetBinning(self.handle,hbin,vbin)
        self._arm()
        if not symmetric:
            try:
                lib.PCO_EnableSoftROI(self.handle,1)
                self._arm()
                hstart,hend,vstart,vend,hbin,vbin=self._truncate_roi(*roi,soft_roi=True)
                lib.PCO_SetROI(self.handle,hstart//hbin+1,vstart//vbin+1,hend//hbin,vend//vbin)
                self._arm()
            except PCOSC2LibError:
                pass
        dim=self._get_data_dimensions_rc()
        lib.PCO_SetImageParameters(self.handle,dim[1],dim[0],1)
        if self.v["general/strCamType/wCamType"]==0x1300: # pco.edge 5.5 CL
            lib.PCO_SetTransferParametersAuto(self.handle)
        return self.get_roi()
    def requires_symmetric_roi(self):
        """
        Check if the camera requires horizontally or vertically symmetric ROI.

        Return a tuple ``(horizontal, vertical)``.
        If ``True``, one might still set up an asymmetric ROI for some cameras using the software ROI feature, but it does not affect camera readout rate
        """
        hsymm=self._has_option(CAPS1.GENERALCAPS1_ROI_HORZ_SYMM_TO_VERT_AXIS)
        vsymm=self._has_option(CAPS1.GENERALCAPS1_ROI_VERT_SYMM_TO_HORZ_AXIS) or self._is_pco_edge()
        return hsymm,vsymm
    def get_roi_limits(self, hbin=1, vbin=1):
        wdet,hdet=self.get_detector_size()
        minsize=(self.v["sensor/strDescription/wMinSizeHorzDESC"],self.v["sensor/strDescription/wMinSizeVertDESC"])
        maxbin=self.v["sensor/strDescription/wMaxBinHorzDESC"],self.v["sensor/strDescription/wMaxBinVertDESC"]
        hstep,vstep=self.v["sensor/strDescription/wRoiHorStepsDESC"],self.v["sensor/strDescription/wRoiVertStepsDESC"]
        if self.v["general/strCamType/wCamType"]==0x1340: # pco.edge CLHS
            hstep=16 # seems to be the case (property says 4, but the documentation says 16)
        if hstep==0 or vstep==0:
            hlim=camera.TAxisROILimit(wdet,wdet,wdet,wdet,maxbin[0])
            vlim=camera.TAxisROILimit(hdet,hdet,hdet,hdet,maxbin[1])
        else:
            hlim=camera.TAxisROILimit(minsize[0]*hbin,wdet,hstep*hbin,hstep*hbin,maxbin[0])
            vlim=camera.TAxisROILimit(minsize[1]*vbin,hdet,vstep*vbin,vstep*vbin,maxbin[1])
        return hlim,vlim

    def enable_pixel_correction(self, enable=True):
        """Enable or disable hotpixel correction"""
        self._check_option(CAPS1.GENERALCAPS1_HOT_PIXEL_CORRECTION)
        lib.PCO_SetHotPixelCorrectionMode(self.handle,1 if enable else 0)
        self._arm()
        return self.is_pixel_correction_enabled()
    def is_pixel_correction_enabled(self):
        """Check if hotpixel correction is enabled"""
        self._check_option(CAPS1.GENERALCAPS1_HOT_PIXEL_CORRECTION)
        return bool(lib.PCO_GetHotPixelCorrectionMode(self.handle))
    _p_noise_filter_mode=interface.EnumParameterClass("noise_filter_mode",{"off":0,"on":1,"on_hpc":0x101})
    @interface.use_parameters(returns="noise_filter_mode")
    def get_noise_filter_mode(self):
        """Get the noise filter mode (for details, see :meth:`set_noise_filter_mode`)"""
        return lib.PCO_GetNoiseFilterMode(self.handle)
    @interface.use_parameters(mode="noise_filter_mode")
    def set_noise_filter_mode(self, mode="on"):
        """
        Set the noise filter mode.
        
        Can be ``"off"``, ``"on"``, or ``"on_hpc"`` (on + hot pixel correction).
        """
        self._check_option(CAPS1.GENERALCAPS1_NOISE_FILTER)
        lib.PCO_SetNoiseFilterMode(self.handle,mode)
        self._arm()
        return self.get_noise_filter_mode()
    def set_status_line_mode(self, binary=True, text=False):
        """
        Set status line mode.

        `binary` determines if the binary line is present (it occupies first 14 pixels of the image).
        `text` determines if the text line is present (it is plane text timestamp, which takes first 8 rows and about 300 columns).

        It is recommended to always have `binary` option on, since it is used to determine frame index for checking if there are any missing frames.
        """
        if binary:
            mode=2 if text else 1
        else:
            mode=3 if text else 0
        if not self._has_option(CAPS1.GENERALCAPS1_TIMESTAMP_ASCII_ONLY) and mode==3:
            mode=2
        lib.PCO_SetTimestampMode(self.handle,mode)
        self._arm()
        return self.get_status_line_mode()
    def get_status_line_mode(self):
        """
        Get status line mode.

        Return tuple ``(binary, text)`` (see :meth:`set_status_line_mode` for description)
        """
        mode=lib.PCO_GetTimestampMode(self.handle)
        return mode in {1,2}, mode in {2,3}

    def get_bit_alignment(self):
        """
        Get data bit alignment
        
        Can be ``"LSB"`` (normal alignment) or ``"MSB"`` (if camera data is less than 16 bit, it is padded with zeros on the right to match 16 bit).
        """
        return "LSB" if lib.PCO_GetBitAlignment(self.handle) else "MSB"
    def set_bit_alignment(self, mode):
        """
        Get data bit alignment
        
        Can be ``"LSB"`` (normal alignment) or ``"MSB"`` (if camera data is less than 16 bit, it is padded with zeros on the right to match 16 bit).
        """
        lib.PCO_SetBitAlignment(self.handle,mode=="LSB")
        self._arm()
        return self.get_bit_alignment()
    def set_metadata_mode(self, mode=True):
        """Set metadata mode"""
        self._check_option(CAPS1.GENERALCAPS1_METADATA)
        lib.PCO_SetMetaDataMode(self.handle,1 if mode else 0)
        self._arm()
        return self.get_metadata_mode()
    def get_metadata_mode(self):
        """
        Get metadata mode.
        
        Return tuple ``(enabled, size, version)``
        """
        self._check_option(CAPS1.GENERALCAPS1_METADATA)
        return tuple(lib.PCO_GetMetaDataMode(self.handle))
    def _get_metadata_size(self):
        if self._has_option(CAPS1.GENERALCAPS1_METADATA):
            mm=self.get_metadata_mode()
            return (mm[1]*2 if mm[0] else 0)
        else:
            return 0

    def _wait_for_next_frame(self, timeout=20., idx=None):
        self._frame_notifier.wait(idx=idx,timeout=timeout)
    _support_chunks=True
    def _parse_frames_data(self, ptr, nframes, shape):
        stride=self._buffers[0].size
        buffer=np.ctypeslib.as_array(ctypes.cast(ptr,ctypes.POINTER(ctypes.c_ubyte)),shape=(stride*nframes,))
        size=shape[0]*shape[1]*2
        framedata=np.empty(nframes*size,dtype="u1")
        copy_strided(buffer,framedata,nframes,size,stride,0)
        frames=framedata.view("<u2").reshape((nframes,)+shape)
        frames=self._convert_indexing(frames,"rct",axes=(1,2))
        return frames
    def _read_frames(self, rng, return_info=False):
        shape=self._get_data_dimensions_rc()
        base=ctypes.addressof(self._full_buffer)
        stride=self._buffers[0].size
        buffer_frames=len(self._buffers)
        start=rng[0]%buffer_frames
        stop=start+(rng[1]-rng[0])
        if stop<=buffer_frames:
            chunks=[(rng[0],start,stop-start)]
        else:
            l0=buffer_frames-start
            chunks=[(rng[0],start,l0),(rng[0]+l0,0,stop-start-l0)]
        frames=[self._parse_frames_data(base+s*stride,l,shape) for (_,s,l) in chunks]
        if self._status_line_enabled and frames and len(frames[-1]):
            self._buffer_overruns=max(self._buffer_overruns,get_status_line(frames[-1][-1,:,:]).framestamp-rng[-1]-1)
        return frames,None

    def _get_grab_acquisition_parameters(self, nframes, buff_size):
        if buff_size is None:
            buff_size=self._default_acq_params.get("nframes",100)
        return {"nframes":buff_size}


copy_strided=nbtools.copy_array_strided(par=False)







TStatusLine=collections.namedtuple("TStatusLine",["framestamp"])
def get_status_line(frame):
    """
    Get frame info from the binary status line.

    Assume that the status line is present; if it isn't, the returned frame info will be a random noise.
    """
    warnings.warn(DeprecationWarning("PCO.get_status_line will be removed soon; use PCO.get_status_lines instead"))
    if frame.ndim==3:
        return [get_status_line(f) for f in frame]
    sline=frame[0,:14]
    sline=(sline&0x0F)+(sline>>4)*10
    framestamp=sline[0]*10**6+sline[1]*10**4+sline[2]*10**2+sline[3]
    return TStatusLine(framestamp-1)

def get_status_lines(frames):
    """
    Get frame info from the binary status line.

    `frames` can be 2D array (one frame), 3D array (stack of frames, first index is frame number), or list of 1D or 2D arrays.
    Assume that the status line is present; if it isn't, the returned frame info will be a random noise.
    Return a 1D or 2D numpy array, where the first axis (if present) is the frame number, and the last is the status line entry.
    """
    if isinstance(frames,list):
        return [get_status_lines(f) for f in frames]
    sline=frames[...,0,:14].astype("i4")
    sline=(sline&0x0F)+(sline>>4)*10
    framestamp=sline[...,0]*10**6+sline[...,1]*10**4+sline[...,2]*10**2+sline[...,3]
    return (framestamp-1)[...,None]



class StatusLineChecker(camera.StatusLineChecker):
    def get_framestamp(self, frames):
        return get_status_lines(frames)[...,0]
    def _prepare_dfs(self, dfs):
        dfs[dfs==-99999998]=1  # overflow from 99999999 to 1
        return dfs