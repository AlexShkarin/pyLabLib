from . import PCO_SC2_lib
from .PCO_SC2_lib import lib, PCOSC2LibError, named_tuple_to_dict

from ...core.devio.interface import IDevice
from ...core.utils import funcargparse, py3, dictionary, general
from ...core.dataproc import image as image_utils

_depends_local=[".PCO_SC2_lib","...core.devio.interface"]

import numpy as np
import collections
import contextlib
import ctypes
import time
import threading

class PCOSC2Error(RuntimeError):
    "Generic PCO SC2 camera error."
class PCOSC2TimeoutError(PCOSC2Error):
    "Timeout while waiting."
class PCOSC2NotSupportedError(PCOSC2Error):
    "Option not supported."

def get_cameras_number():
    """Get number of connected PCOSC2 cameras"""
    lib.initlib()
    cams=[]
    try:
        while True:
            cams.append(lib.PCO_OpenCamera(0))
    except PCOSC2LibError:
        pass
    ncams=len(cams)
    for c in cams:
        try:
            lib.PCO_CloseCamera(c)
        except PCOSC2LibError:
            pass
    return ncams

def reset_api():
    """
    Reset API.
    
    All cameras must be closed; otherwise, the prompt to reboot will appear.
    """
    lib.initlib()
    lib.PCO_ResetLib()

class PCOSC2Camera(IDevice):
    """
    PCO SC2 camera.

    Args:
        idx(int): camera index (use :func:`get_cameras_number` to get the total number of connected cameras)
        reboot_on_fail(bool): if ``True`` and the camera raised an error during initialization (but after opening), reboot the camera and try to connect again
            useful when the camera is in a broken state (e.g., wrong ROI or pixel clock settings)
    """
    def __init__(self, idx=0, reboot_on_fail=True):
        IDevice.__init__(self)
        lib.initlib()
        self.idx=idx
        self.handle=None
        self.reboot_on_fail=reboot_on_fail
        self._full_camera_data=dictionary.Dictionary()
        self._capabilities=[]
        self._model_data=None
        self._buffers=None
        self._default_nframes=100
        self._buffer_looping=False
        self._buffer_loop_thread=None
        self._next_wait_buffer=0
        self._next_read_buffer=0
        self._next_schedule_buffer=0
        self._next_buffer=0
        self._last_wait_frame=0
        self.image_indexing="rct"
        self.v=dictionary.ItemAccessor(lambda n:self._full_camera_data[n])
        self.open()

        self._nodes_ignore_error={"get":(PCOSC2NotSupportedError,),"set":()}
        self._add_full_info_node("model_data",self.get_model_data)
        self._add_full_info_node("capabilities",self.get_capabilities)
        self._add_status_node("temperature_monitor",self.get_temperature)
        self._add_settings_node("trigger_mode",self.get_trigger_mode,self.set_trigger_mode)
        self._add_settings_node("exposure",self.get_exposure,self.set_exposure)
        self._add_settings_node("frame_delay",self.get_frame_delay,self.set_frame_delay)
        self._add_status_node("timings",self.get_timings)
        self._add_settings_node("frame_time",self.get_frame_time,self.set_frame_time)
        self._add_status_node("buffer_size",self.get_buffer_size)
        self._add_status_node("buffer_status",self.get_buffer_status)
        self._add_status_node("data_dimensions",self.get_data_dimensions)
        self._add_settings_node("bit_alignment",self.get_bit_aligment,self.set_bit_aligment)
        self._add_settings_node("hotpixel_correction",self.is_pixel_correction_enabled,self.enable_pixel_correction)
        self._add_settings_node("noise_filter",self.get_noise_filter_mode,self.set_noise_filter_mode)
        self._add_settings_node("status_line",self.get_status_line_mode,self.set_status_line_mode)
        self._add_settings_node("metadata_mode",self.get_metadata_mode,self.set_metadata_mode)
        self._add_settings_node("pixel_rate",self.get_pixel_rate,self.set_pixel_rate)
        self._add_full_info_node("all_pixel_rates",self.get_available_pixel_rates)
        self._add_full_info_node("conversion_factor",self.get_conversion_factor)
        self._add_full_info_node("detector_size",self.get_detector_size)
        self._add_settings_node("roi",self.get_roi,self.set_roi)
        self._add_status_node("roi_limits",self.get_roi_limits)
        self._add_status_node("acq_status",self.get_status)
        self._add_status_node("acq_in_progress",self.acquisition_in_progress)
        self._add_full_info_node("full_data",self.get_full_camera_data)

    def open(self):
        """Open connection to the camera"""
        for t in range(2):
            self.handle=lib.PCO_OpenCamera(self.idx)
            try:
                self.update_full_data()
                return
            except:
                if self.reboot_on_fail and t==0:
                    self.reboot()
                else:
                    self.close()
                    raise
    def close(self):
        """Close connection to the camera"""
        if self.handle is not None:
            try:
                self.stop_acquisition()
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
            if wait:
                time.sleep(10.)

    def get_full_camera_data(self):
        """Get a dictionary the all camera data available through the SDK."""
        cam_data=dictionary.Dictionary()
        for (i,name) in enumerate(["interface","camera","sensor","serial_number","fw_build","fw_rev"]):
            cam_data["info_strings",name]=py3.as_str(lib.PCO_GetInfoString(self.handle,i))
        cam_data["general"]=named_tuple_to_dict(lib.PCO_GetGeneral(self.handle),expand_lists=True)
        cam_data["sensor"]=named_tuple_to_dict(lib.PCO_GetSensorStruct(self.handle),expand_lists=True)
        cam_data["img_timing"]=named_tuple_to_dict(lib.PCO_GetImageTiming(self.handle),expand_lists=True)
        cam_data["timing"]=named_tuple_to_dict(lib.PCO_GetTimingStruct(self.handle),expand_lists=True)
        cam_data["storage"]=named_tuple_to_dict(lib.PCO_GetStorageStruct(self.handle),expand_lists=True)
        cam_data["recording"]=named_tuple_to_dict(lib.PCO_GetRecordingStruct(self.handle),expand_lists=True)
        cam_data["image"]=named_tuple_to_dict(lib.PCO_GetImageStruct(self.handle),expand_lists=True)
        signal_num=len(cam_data["sensor/strSignalDesc"])
        for k in list(cam_data["timing/strSignal"].keys()):
            if int(k)>=signal_num:
                del cam_data["timing/strSignal",k]
        for k in list(cam_data["image/strSegment"].keys()):
            if cam_data["image/strSegment",k,"dwMaxImageCnt"]==0:
                del cam_data["image/strSegment",k]
        return cam_data
    
    def update_full_data(self):
        """
        Update internal full camera data settings.
        
        Takes some time (about 50ms), so more specific function are preferrables for specific parameters.
        """
        self._arm()
        self._full_camera_data=self.get_full_camera_data()
        self._capabilities=self.get_capabilities()
        self._model_data=self.get_model_data()
    def _arm(self):
        lib.PCO_ArmCamera(self.handle)

    ModelData=collections.namedtuple("ModelData",["model","interface","sensor","serial_number"])
    _interface_codes={1:"firewire",2:"camlink",3:"usb2",4:"gige",5:"serial",6:"usb3",7:"clhs"}
    def get_model_data(self):
        """
        Get camera model data.

        Return tuple ``(model, interface, sensor, serial_number)``.
        """
        intf=self._interface_codes.get(self.v["general/strCamType/wInterfaceType"],"unknown")
        return self.ModelData(self.v["info_strings/camera"],intf,self.v["info_strings/sensor"],self.v["info_strings/serial_number"])

    def _parse_flag_bits(self, value, desc):
        result=set()
        b=1
        for v in desc:
            if isinstance(v,tuple):
                v,b=v
            if value&b:
                result.add(v)
            b<<=1
        return result
    _caps_desc1=[   "noise_filter","hotpix_filter","hotpix_with_noise_only","timestamp_ascii_only",
                    "dataformat2x12","record_stop","hot_pixel_correction","no_extexpctl",
                    "no_timestamp","no_acq_mode","dataformat4x16","dataformat5x16",
                    "no_record","fast_timing","metadata","set_framerate",
                    "cdi_mode","ccm","ext_sync","no_global_shutter",
                    "global_reset_mode","ext_acq","fan_ctl","symm_vert_roi",
                    "symm_hor_roi","cooling_setp"]
    def get_capabilities(self):
        """
        Get camera capabilities.

        For description of the capabilities, see PCO SC2 manual.
        """
        caps=self.v["sensor/strDescription/dwGeneralCapsDESC1"]
        return self._parse_flag_bits(caps,self._caps_desc1)
    def _has_option(self, option):
        return option in self._capabilities
    def _check_option(self, option, value=True):
        has_option=self._has_option(option)
        if has_option!=value:
            raise PCOSC2NotSupportedError("option {} is not supported by {}".format(option,self.get_model_data().model))
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
    _status_bits=[  "default_state","settings_valid","recording_on","readout_on",
                    "frame_rate_dominant","stop_triggered","ext_sync_locked","battery_on",
                    "power_save_on","power_save_left","irig_locked"]
    _warning_bits=["power_supply_voltage","power_supply_temp","camera_temp","sensor_temp","battery","offset_reg"]
    _error_bits=["power_supply_voltage","power_supply_temp","camera_temp","sensor_temp","battery",("interface",0x10000),"ram_module","main_board","head_board"]
    CameraStatus=collections.namedtuple("CameraStatus",["status","warnings","errors"])
    def get_status(self, full=False):
        """
        Get camera status.

        If ``full==True``, return current camera status as a set of enabled status states;
        otherwise, return tuple ``(status, warnings, errors)`` with additional information about warnings and error.
        """
        warn,err,stat=lib.PCO_GetCameraHealthStatus(self.handle)
        if full:
            return self.CameraStatus(self._parse_flag_bits(stat,self._status_bits),self._parse_flag_bits(warn,self._warning_bits),self._parse_flag_bits(err,self._error_bits))
        else:
            return self._parse_flag_bits(stat,self._status_bits)

    def get_temperature(self):
        """
        Get the current camera temperature
        
        Return tuple ``(CCD, cam, power)`` with temperatures of the sensor, camera, and power supply respectively.
        """
        temp=lib.PCO_GetTemperature(self.handle)
        return (temp.ccd/10.,temp.cam,temp.pow)
    def get_conversion_factor(self):
        """Get camera conversion factor (electrons per pixel value)"""
        return lib.PCO_GetConversionFactor(self.handle)/100.
    
    ### Trigger controls ###
    _trigger_modes={"int":0,"soft":1,"ext":2,"ext_exp":3,"ext_sync":4,"ext_exp_fast":5,"ext_cds":6,"ext_exp_slow":7,"ext_sync_hdsdi":0x102}
    _trigger_modes_inv=general.invert_dict(_trigger_modes)
    def get_trigger_mode(self):
        """Get current trigger mode (see :meth:`set_trigger_mode` for description)"""
        mode=lib.PCO_GetTriggerMode(self.handle)
        return self._trigger_modes_inv[mode]
    def set_trigger_mode(self, mode):
        """
        Set trigger mode.

        Can be ``"int"`` (internal), ``"soft"`` (software), ``"ext"`` (external+software), ``"ext_exp"`` (external exposure), ``"ext_sync"`` (external PLL sync),
        ``"ext_exp_fast"`` (fast external exposure), ``"ext_cds"`` (external CDS control),
        ``"ext_exp_slow"`` (slow external exposure)`, or ``"ext_sync_hdsdi"`` (external synchronized SD/HDI).

        For description, see PCO SDK manual.
        """
        funcargparse.check_parameter_range(mode,"mode",self._trigger_modes.keys())
        lib.PCO_SetTriggerMode(self.handle,self._trigger_modes[mode])
        self._arm()
        return self.get_trigger_mode()
    def send_software_trigger(self):
        """Send software trigger signal"""
        return bool(lib.PCO_ForceTrigger(self.handle))

    ### Acquisition controls ###
    class Buffer(object):
        """Single frame buffer object, which controls setup, cleanup, and synchronization"""
        def __init__(self, size, metadata_size=0):
            object.__init__(self)
            self.buff=ctypes.create_string_buffer(size)
            self.event=lib.CreateEvent()
            self.size=size
            self.status=PCO_SC2_lib.DWORD()
            self.metadata_size=metadata_size
            self.lock=threading.Lock()
        def wait(self, timeout):
            if not self.lock.acquire(timeout=(-1 if timeout is None else timeout)):
                return False
            wait_res=lib.WaitForSingleObject(self.event,(-1 if timeout is None else np.int(timeout*1000)))==0
            self.lock.release()
            return wait_res
        def reset(self):
            with self.lock:
                lib.ResetEvent(self.event)
        def release(self):
            if self.buff is not None:
                lib.CloseHandle(self.event)
                self.buff=None
                self.event=None
    def _allocate_buffers(self, n):
        self.stop_acquisition()
        frame_size,metadata_size=self._get_buffer_size()
        self._buffers=[self.Buffer(frame_size+metadata_size,metadata_size=metadata_size) for _ in range(n)]
        self._next_wait_buffer=0
        self._next_read_buffer=0
        self._next_schedule_buffer=0
        self._last_wait_frame=0
        return n
    def _schedule_buffer(self, buff):
        lib.PCO_AddBufferExtern(self.handle,buff.event,0,0,0,0,buff.buff,buff.size,ctypes.byref(buff.status))
    def _schedule_all_buffers(self, n=None):
        if self._buffers:
            if n is None:
                n=min(len(self._buffers),32)
            for b in self._buffers[:n]:
                self._schedule_buffer(b)
                self._next_schedule_buffer+=1
    def _unschedule_all_buffers(self):
        if self._buffers:
            lib.PCO_CancelImages(self.handle)
    def _deallocate_buffers(self):
        if self._buffers is not None:
            for b in self._buffers:
                b.release()
            self._buffers=None
        
    def _loop_schedule_refresh_buffers(self):
        nbuff=len(self._buffers)
        nsched=min(nbuff,32)
        while self._buffer_looping:
            actioned=False
            if self._next_wait_buffer<self._next_schedule_buffer: # scheduled buffers available
                buff=self._buffers[self._next_wait_buffer%nbuff]
                succ=buff.wait(timeout=0.001)
                if succ:
                    self._next_wait_buffer+=1
                actioned=True
            if self._next_schedule_buffer<self._next_wait_buffer+nsched and self._next_schedule_buffer<self._next_read_buffer+nbuff: # more scheduling space and buffer space
                buff=self._buffers[self._next_schedule_buffer%nbuff]
                buff.reset()
                self._schedule_buffer(buff)
                self._next_schedule_buffer+=1
                actioned=True
            if not actioned:
                time.sleep(0.001)
    def _stop_reading_loop(self):
        if self._buffer_loop_thread is not None:
            self._buffer_looping=False
            self._buffer_loop_thread.join()
            self._buffer_loop_thread=None
    def _start_reading_loop(self):
        self._stop_reading_loop()
        self._buffer_loop_thread=threading.Thread(target=self._loop_schedule_refresh_buffers,daemon=True)
        self._buffer_looping=True
        self._buffer_loop_thread.start()

    def _read_next_buffer(self, npx=None):
        if self._buffers is None or self._next_read_buffer>=self._next_wait_buffer:
            return None
        buff=self._buffers[self._next_read_buffer%len(self._buffers)]
        if npx is None:
            npx=len(buff.buff)//2
        frame=np.frombuffer(buff.buff,dtype="<u2",count=npx).copy()
        metadata=buff.buff[-buff.metadata_size:] if buff.metadata_size>0 else None
        self._next_read_buffer+=1
        return frame,metadata
    def _wait_for_next_buffer(self, timeout=None):
        if self._buffers is None:
            return False
        if self._next_wait_buffer>self._next_read_buffer:
            return True
        buff=self._buffers[self._next_read_buffer%len(self._buffers)]
        return buff.wait(timeout)
    

    AcqTimes=collections.namedtuple("AcqTimes",["exposure","frame_delay","frame_time"])
    def get_timings(self):
        """
        Get acquisition timing.

        Return tuple ``(exposure, frame_delay, frame_time)``.
        """
        timings=lib.PCO_GetImageTiming(self.handle)
        exp=timings.ExposureTime_s+timings.ExposureTime_ns*1E-9
        frame_delay=timings.TriggerDelay_s+timings.TriggerDelay_ns*1E-9
        frame_time=timings.FrameTime_s+timings.FrameTime_ns*1E-9
        return self.AcqTimes(exp,frame_delay,frame_time)
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
        return self.get_timings().exposure
    def set_frame_delay(self, frame_delay):
        """Set camera frame delay"""
        self._set_exposure_delay(self.get_exposure(),frame_delay)
        return self.get_frame_delay()
    def get_frame_delay(self):
        """Get current frame delay"""
        return self.get_timings().frame_delay
    def set_frame_time(self, frame_time=0, adjust_exposure=False):
        """
        Set frame time (frame acquisition period).

        If the time can't be achieved even with zero frame delay and ``adjust_exposure==True``, try to reduce the exposure to get the desired frame time;
        otherwise, keep the exposure the same.
        """
        exposure,frame_delay,curr_frame_time=self.get_timings()
        if curr_frame_time-frame_delay<=frame_time:
            frame_delay=frame_delay+frame_time-curr_frame_time
        else:
            frame_delay=0
            if adjust_exposure:
                exposure=max(0,frame_delay+frame_time-curr_frame_time+exposure)
        self._set_exposure_delay(exposure,frame_delay)
        return self.get_frame_time()
    def get_frame_time(self):
        """Get current frame time (frame acquisition period)"""
        return self.get_timings().frame_time
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
    def start_acquisition(self, buffn=None):
        """
        Start camera acquisition.

        `buffn` specifies number of frames in the ring buffer (automatically capped at 32, which is the SDK limit)
        """
        self.stop_acquisition()
        self._allocate_buffers(n=buffn or self._default_nframes)
        self._arm()
        if self._is_pco_edge() and self._is_camlink():
            self._schedule_all_buffers()
            self._start_reading_loop()
            lib.PCO_SetRecordingState(self.handle,1)
        else:
            lib.PCO_SetRecordingState(self.handle,1)
            self._schedule_all_buffers()
            self._start_reading_loop()
    def stop_acquisition(self):
        """
        Stop acquisition.

        Clears buffers as well, so any readout after acquisition stop is impossible.
        """
        self._stop_reading_loop()
        self._unschedule_all_buffers()
        lib.PCO_SetRecordingState(self.handle,0)
        self._deallocate_buffers()
    def acquisition_in_progress(self):
        """Check if the acquisition is in progress"""
        return bool(lib.PCO_GetRecordingState(self.handle))
    def wait_for_frame(self, since="lastread", timeout=20., period=1E-3):
        """
        Wait for a new camera frame.

        `since` specifies what constitutes a new frame.
        Can be ``"lastread"`` (wait for a new frame after the last read frame), ``"lastwait"`` (wait for a new frame after last :meth:`wait_for_frame` call),
        or ``"now"`` (wait for a new frame acquired after this function call).
        If `timeout` is exceeded, raise :exc:`.PCOSC2TimeoutError`.
        `period` specifies camera polling period.
        """
        if not self.acquisition_in_progress():
            return
        last_acq_frame=self._next_wait_buffer-1
        last_read_frame=self._next_read_buffer-1
        if since=="lastread" and last_acq_frame>last_read_frame:
            self._last_wait_frame=last_acq_frame
            return
        if since=="lastwait" and last_acq_frame>self._last_wait_frame:
            self._last_wait_frame=last_acq_frame
            return
        ctd=general.Countdown(timeout)
        while not ctd.passed():
            new_valid=self._next_wait_buffer>self._next_read_buffer
            if new_valid:
                break
            time.sleep(0.001)
        if not new_valid:
            raise PCOSC2TimeoutError()
        self._last_wait_frame=self._next_wait_buffer-1
    @contextlib.contextmanager
    def pausing_acquisition(self):
        """
        Context manager which temporarily pauses acquisition during execution of ``with`` block.

        Useful for applying certain settings which can't be changed during the acquisition (any settings except for exposure).
        """
        acq=self.acquisition_in_progress()
        try:
            self.stop_acquisition()
            yield
        finally:
            if acq:
                self.start_acquisition()

    # ### Image settings and transfer controls ###
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        return self.v["sensor/strDescription/wMaxHorzResStdDESC"],self.v["sensor/strDescription/wMaxVertResStdDESC"]
    def _adj_roi_axis(self, start, end, minsize, detsize, step, symm):
        end=min(end,detsize)
        start=min(start,detsize)
        start-=start%step
        end-=end%step
        if end-start<minsize:
            end=start+minsize
        if end>detsize:
            end=detsize
            start=detsize-minsize
        if symm:
            cdist=max(abs(start-detsize//2),abs(end-detsize//2))
            start=min(start,detsize//2-cdist)
            start-=start%step
            end=detsize-start
        return start,end
    def _adj_bin(self, bin, maxbin, binmode):
        bin=max(bin,1)
        bin=min(bin,maxbin)
        if binmode!=1:
            bin=int(2**np.floor(np.log2(bin)))
        return bin
    def _trunc_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1, soft_roi=False):
        xdet,ydet=self.get_detector_size()
        if hend is None:
            hend=xdet
        if vend is None:
            vend=ydet
        hbinmax=self.v["sensor/strDescription/wMaxBinHorzDESC"]
        hbinmode=self.v["sensor/strDescription/wBinHorzSteppingDESC"]
        hbin=self._adj_bin(hbin,hbinmax,hbinmode)
        vbinmax=self.v["sensor/strDescription/wMaxBinVertDESC"]
        vbinmode=self.v["sensor/strDescription/wBinVertSteppingDESC"]
        vbin=self._adj_bin(vbin,vbinmax,vbinmode)
        hstep=self.v["sensor/strDescription/wRoiHorStepsDESC"]
        vstep=self.v["sensor/strDescription/wRoiVertStepsDESC"]
        if hstep==0 or vstep==0: # no ROI
            hstart,hend,vstart,vend=0,xdet,0,ydet
        else:
            if self.v["general/strCamType/wCamType"]==0x1340: # pco.edge CLHS
                hstep=16 # seems to be the case (property says 4, but the documentation says 16)
            hminsize=self.v["sensor/strDescription/wMinSizeHorzDESC"]*hbin
            vsymm="symm_vert_roi" in self._capabilities or (self._is_pco_edge() and not soft_roi) # pco.edge must be symmetric, can with soft ROI activated it can be asymmetric for output
            hsymm="symm_hor_roi" in self._capabilities
            hstart,hend=self._adj_roi_axis(hstart,hend,hminsize,xdet,hstep*hbin,hsymm)
            vminsize=self.v["sensor/strDescription/wMinSizeVertDESC"]*vbin
            vstart,vend=self._adj_roi_axis(vstart,vend,vminsize,ydet,vstep*vbin,vsymm)
        return hstart,hend,vstart,vend,hbin,vbin
    def get_roi(self):
        """
        Get current ROI.

        Return tuple ``(hstart, hend, vstart, vend, hbin, vbin)``.
        """
        roi=lib.PCO_GetROI(self.handle)
        bin=lib.PCO_GetBinning(self.handle)
        return ((roi[0]-1)*bin[0],roi[2]*bin[0],(roi[1]-1)*bin[1],roi[3]*bin[1],bin[0],bin[1])
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        """
        Setup camera ROI.

        `hstart` and `hend` specify horizontal image extent, `vstart` and `vend` specify vertical image extent
        (start are inclusive, stop are exclusive, starting from 0), `hbin` and `vbin` specify binning.
        By default, all non-supplied parameters take extreme values.
        """
        roi=hstart,hend,vstart,vend,hbin,vbin
        hstart,hend,vstart,vend,hbin,vbin=self._trunc_roi(*roi)
        lib.PCO_EnableSoftROI(self.handle,0)
        self._arm()
        lib.PCO_SetROI(self.handle,hstart//hbin+1,vstart//vbin+1,hend//hbin,vend//vbin)
        lib.PCO_SetBinning(self.handle,hbin,vbin)
        self._arm()
        try:
            lib.PCO_EnableSoftROI(self.handle,1)
            self._arm()
            hstart,hend,vstart,vend,hbin,vbin=self._trunc_roi(*roi,soft_roi=True)
            lib.PCO_SetROI(self.handle,hstart//hbin+1,vstart//vbin+1,hend//hbin,vend//vbin)
            self._arm()
        except PCOSC2LibError:
            pass
        dim=self._get_data_dimensions_rc()
        lib.PCO_SetImageParameters(self.handle,dim[1],dim[0],1)
        if self.v["general/strCamType/wCamType"]==0x1300: # pco.edge 5.5 CL
            lib.PCO_SetTransferParametersAuto(self.handle)
        return self.get_roi()
    def get_roi_limits(self):
        """
        Get the minimal and maximal ROI parameters.

        Return tuple ``(min_roi, max_roi)``, where each element is in turn 6-tuple describing the ROI.
        """
        xdet,ydet=self.get_detector_size()
        min_size=(self.v["sensor/strDescription/wMinSizeHorzDESC"],self.v["sensor/strDescription/wMinSizeVertDESC"])
        maxbin=self.v["sensor/strDescription/wMaxBinHorzDESC"],self.v["sensor/strDescription/wMaxBinVertDESC"]
        min_roi=(0,0,min_size[0],min_size[1],1,1)
        max_roi=(xdet-min_size[0],ydet-min_size[1],xdet,ydet,maxbin[0],maxbin[1])
        return (min_roi,max_roi)

    def get_bit_aligment(self):
        """
        Get data bit alignment
        
        Can be ``"LSB"`` (normal alignment) or ``"MSB"`` (if camera data is less than 16 bit, it is padded with zeros on the right to match 16 bit).
        """
        return "LSB" if lib.PCO_GetBitAlignment(self.handle) else "MSB"
    def set_bit_aligment(self, mode):
        """
        Get data bit alignment
        
        Can be ``"LSB"`` (normal alignment) or ``"MSB"`` (if camera data is less than 16 bit, it is padded with zeros on the right to match 16 bit).
        """
        lib.PCO_SetBitAlignment(self.handle,mode=="LSB")
        self._arm()
        return self.get_bit_aligment()
    def enable_pixel_correction(self, enable=True):
        """Enable or disable hotpixel correction"""
        self._check_option("hot_pixel_correction")
        lib.PCO_SetHotPixelCorrectionMode(self.handle,1 if enable else 0)
        self._arm()
        return self.is_pixel_correction_enabled()
    def is_pixel_correction_enabled(self):
        """Check if hotpixel correction is enabled"""
        self._check_option("hot_pixel_correction")
        return bool(lib.PCO_GetHotPixelCorrectionMode(self.handle))
    _noise_filter_mode={0:"off",1:"on",0x101:"on_hpc"}
    _noise_filter_mode_inv=general.invert_dict(_noise_filter_mode)
    def get_noise_filter_mode(self):
        """Get the noise filter mode (for details, see :meth:`set_noise_filter_mode`)"""
        mode=lib.PCO_GetNoiseFilterMode(self.handle)
        return self._noise_filter_mode[mode]
    def set_noise_filter_mode(self, mode="on"):
        """
        Set the noise filter mode.
        
        Can be ``"off"``, ``"on"``, or ``"on_hpc"`` (on + hot pixel correction).
        """
        funcargparse.check_parameter_range(mode,"mode",self._noise_filter_mode_inv.keys())
        self._check_option("noise_filter")
        lib.PCO_SetNoiseFilterMode(self.handle,self._noise_filter_mode_inv[mode])
        self._arm()
        return self.get_noise_filter_mode()
    def set_status_line_mode(self, binary=True, ascii=False):
        """
        Set status line mode.

        `binary` determines if the binary line is present (it occupies first 14 pixels of the image).
        `ascii` determines if the ascii line is present (it is plane text timestamp, which takes first 8 rows and about 300 columns).

        It is recommended to always have `binary` option on, since it is used to determine frame index for checking if there are any missing frames.
        """
        if binary:
            mode=2 if ascii else 1
        else:
            mode=3 if ascii else 0
        if not self._has_option("timestamp_ascii_only") and mode==3:
            mode=2
        lib.PCO_SetTimestampMode(self.handle,mode)
        self._arm()
        return self.get_status_line_mode()
    def get_status_line_mode(self):
        """
        Get status line mode.

        Return tuple ``(binary, ascii)`` (see :meth:`set_status_line_mode` for description)
        """
        mode=lib.PCO_GetTimestampMode(self.handle)
        return mode in {1,2}, mode in {2,3}
    def set_metadata_mode(self, mode=True):
        """
        Set metadata mode
        """
        self._check_option("metadata")
        lib.PCO_SetMetaDataMode(self.handle,1 if mode else 0)
        self._arm()
        return self.get_metadata_mode()
    def get_metadata_mode(self):
        """
        Get metadata mode
        
        Return tuple ``(enabled, size, version)``
        """
        self._check_option("metadata")
        return lib.PCO_GetMetaDataMode(self.handle)
    def _get_metadata_size(self):
        if self._has_option("metadata"):
            mm=self.get_metadata_mode()
            return (mm.size*2 if mm.mode else 0)
        else:
            return 0

    def _get_data_dimensions_rc(self):
        sizes=lib.PCO_GetSizes(self.handle)
        return sizes[1],sizes[0]
    def get_data_dimensions(self):
        """Get readout data dimensions"""
        return image_utils.convert_shape_indexing(self._get_data_dimensions_rc(),"rc",self.image_indexing)
    def _get_buffer_size(self):
        dim=self._get_data_dimensions_rc()
        mm_size=self._get_metadata_size()
        if mm_size>0:
            mm_size=((mm_size-1)//(dim[1]*2)+1)*(dim[1]*2)
        return dim[0]*dim[1]*2,mm_size
    
    def get_buffer_size(self):
        """Get number of frames in the ring buffer"""
        return len(self._buffers) if self._buffers is not None else 0
    TBufferStatus=collections.namedtuple("TBufferStatus",["unread","size","scheduled","scheduled_max"])
    def get_buffer_status(self):
        if self._buffers is None:
            return self.TBufferStatus(0,0,0,0)
        unread=self._next_wait_buffer-self._next_read_buffer
        size=len(self._buffers)
        scheduled=self._next_schedule_buffer-self._next_wait_buffer
        scheduled_max=min(size,32)
        return self.TBufferStatus(unread,size,scheduled,scheduled_max)
    def get_new_images_range(self):
        """
        Get the range of the new images.
        
        Return tuple ``(first, last)`` with images range (inclusive).
        If no images are available, return ``None``.
        """
        if self._next_read_buffer==self._next_wait_buffer:
            return None
        return (self._next_read_buffer,self._next_wait_buffer-1)
    def read_multiple_images(self, rng=None, return_info=False):
        """
        Read multiple images specified by `rng` (by default, all un-read images).

        If ``return_info==True``, return tuple ``(images, info)``, where ``images`` is a list of frames,
        and ``info`` is a list of frame info tuples extracted from the binary status line (with only one member, frame index).
        Note that if the binary status line is not activated, frame info will be an arbitrary noise.
        If ``return_info==False``, just return a list of frames.

        Fro technical reasons, frames should be read in successively, and every frame can only be read ones.
        Hence, if `rng` is specified, it can lead to either skipping unread frames (if `rng` starts after the first unread frame),
        or reduced number of frames compared to request (if `rng` attempts to read non-acquired or already-read frames).
        """
        new_images_rng=self.get_new_images_range()
        if rng is None:
            rng=new_images_rng
        dim=self._get_data_dimensions_rc()
        if rng is None:
            return np.zeros((0,dim[0],dim[1]))
        rng=list(rng)
        if rng[0]<new_images_rng[0]:
            rng[0]=new_images_rng[0]
        if rng[1]>new_images_rng[1]:
            rng[1]=new_images_rng[1]
        if rng[0]>rng[1]:
            return np.zeros((0,dim[0],dim[1]))
        if rng[0]>new_images_rng[0]:
            for _ in range(rng[0]-new_images_rng[0]):
                self._read_next_buffer(npx=0)
            rng[0]=new_images_rng[0]
        npx=dim[0]*dim[1]
        imgs,_=list(zip(*[self._read_next_buffer(npx=npx) for _ in range(rng[1]-rng[0]+1)]))
        imgs=[image_utils.convert_image_indexing(im.reshape(dim),"rct",self.image_indexing) for im in imgs]
        if return_info:
            infos=[get_frame_info(f) for f in imgs]
            return imgs,infos
        else:
            return imgs

    ### Combined functions ###
    def snap(self):
        """Snap a single image"""
        self.start_acquisition()
        self.wait_for_frame()
        frame=self.read_multiple_images()[0]
        self.stop_acquisition()
        return frame



TFrameInfo=collections.namedtuple("TFrameInfo",["framestamp"])
def get_frame_info(frame):
    """
    Get frame info from the binary status line.

    Assume that the status line is present; if it isn't, the returned frame info will be a random noise.
    """
    if frame.ndim==3:
        return [get_frame_info(f) for f in frame]
    sline=frame[0,:14]
    sline=(sline&0x0F)+(sline>>4)*10
    framestamp=sline[0]*10**6+sline[1]*10**4+sline[2]*10**2+sline[3]
    return TFrameInfo(framestamp-1)