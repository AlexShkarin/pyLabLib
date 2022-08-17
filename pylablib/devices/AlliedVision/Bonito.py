from ..IMAQ.IMAQ import IMAQFrameGrabber
from ..interface import camera
from ...core.devio import interface
from ...core.devio.comm_backend import DeviceError
from ...core.utils import funcargparse, py3

import numpy as np
import collections
import re



class BonitoError(DeviceError):
    """Generic AlliedVision Bonito error"""



TDeviceInfo=collections.namedtuple("TDeviceInfo",["version","serial_number","grabber_info"])
class IBonitoCamera(camera.ICamera): # pylint: disable=abstract-method
    Error=DeviceError
    GrabberClass=None
    def __init__(self, **kwargs):
        super().__init__(do_open=False,**kwargs)

        self._frame_period=None
        self._add_settings_variable("status_line",self.is_status_line_enabled,self.enable_status_line)
        self._add_settings_variable("bl_offset",self.get_black_level_offset,self.set_black_level_offset)
        self._add_settings_variable("digital_gain",self.get_digital_gain,self.set_digital_gain)
        self._add_settings_variable("exposure",self.get_exposure,self.set_exposure)
        self._add_settings_variable("frame_period",self.get_frame_period,self.set_frame_period)
        self._add_settings_variable("exposure_control_mode",self.get_exposure_control_mode,self.set_exposure_control_mode)
        self._add_status_variable("frame_timings",self.get_frame_timings)
    
        self.open()
    
    def open(self):
        super().open()
        with self._close_on_error():
            self.setup_serial_params(write_term="\r",datatype="str")  # pylint: disable=no-member
            self.set_roi()
            self._frame_period=self.get_frame_period()
            self.set_exposure(self.get_exposure())
            self._max_nbuff=2**16-1

    
    def serial_query(self, query, timeout=3.):
        self.serial_flush()  # pylint: disable=no-member
        self.serial_write(query)  # pylint: disable=no-member
        reply=self.serial_readline(timeout=timeout,maxn=2**16)  # pylint: disable=no-member
        if not reply.endswith("\r\n>"):
            raise BonitoError("unexpected reply: {}; expect to end with '\\r\\n>'".format(reply))
        if reply.startswith(query+"\r\r\n"):
            reply=reply[len(query)+3:]
        reply=reply[:-1].strip()
        return reply

    def get_serial_parameter(self, comm, kind="int", timeout=3.):
        funcargparse.check_parameter_range(kind,"kind",["int","str"])
        reply=self.serial_query(comm+"=?",timeout=timeout)
        if not re.match(r"=[A-Fa-f0-9]+",reply):
            raise BonitoError("unexpected reply to command {}: {}".format(comm,reply))
        reply=reply[1:]
        if kind=="int":
            return int(reply,base=16)
        return reply
    def set_serial_parameter(self, comm, value):
        if isinstance(value,(int,float)):
            value=max(value,0)
            value="{:X}".format(int(value))
        return self.serial_query("{}={}".format(comm,value))


    
    def get_device_info(self):
        """
        Get camera model data.

        Return tuple ``(model, serial_number, grabber_info)``.
        """
        version=self.serial_query("V")
        serial=self.get_serial_parameter("a")
        grabber_info=tuple(self.GrabberClass.get_device_info(self)) if self.GrabberClass else None
        return TDeviceInfo(version,serial,grabber_info)


    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``; as the camera does not provide this information, use the frame grabber parameters"""
        return self.get_grabber_detector_size()  # pylint: disable=no-member
    def _get_cam_data_dimensions_rc(self):
        return self.get_serial_parameter("N")+1,self.get_detector_size()[0]
    def _update_grabber_roi(self, hstart=0, hend=None):
        if self.GrabberClass:
            r,c=self._get_cam_data_dimensions_rc()
            if hend is None:
                hend=c
            if self.get_grabber_roi()!=(hstart,hend,0,r):
                self.set_grabber_roi(hstart,hend,0,r)
    def get_roi(self):
        """
        Get current ROI.

        Return tuple ``(hstart, hend, vstart, vend)``.
        """
        hstart,hend=self.get_grabber_roi()[:2]  # pylint: disable=no-member
        f=self.get_serial_parameter("A")
        n=self.get_serial_parameter("N")
        return hstart,hend,f,f+n+1
    def _set_cam_roi(self, vstart, vend):
        self.set_serial_parameter("D",0)
        self.set_serial_parameter("I",1)
        self.set_serial_parameter("A",vstart)
        self.set_serial_parameter("N",vend-vstart-1)
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None):
        """
        Setup camera ROI.

        By default, all non-supplied parameters take extreme values.
        """
        hlim,vlim=self.get_roi_limits()
        hstart,hend=self._truncate_roi_axis((hstart,hend),hlim)  # pylint: disable=no-member
        vstart,vend=self._truncate_roi_axis((vstart,vend),vlim)  # pylint: disable=no-member
        self.set_serial_parameter("D",0)
        self.set_serial_parameter("I",1)
        self.set_serial_parameter("A",vstart)
        self.set_serial_parameter("N",vend-vstart-1)
        self._update_grabber_roi(hstart,hend)
        return self.get_roi()
    def get_roi_limits(self, hbin=1, vbin=1): # pylint: disable=unused-argument
        w,h=self.get_detector_size()
        hlim,_=self.get_grabber_roi_limits(hbin=hbin,vbin=vbin) if self.GrabberClass else camera.TAxisROILimit(w,w,w,w,1)
        vlim=camera.TAxisROILimit(1,min(h,2048),1,1,1)
        return hlim,vlim
    def setup_acquisition(self, mode="sequence", nframes=100):  # pylint: disable=arguments-differ
        settings=self.get_settings(include=["status_line","bl_offset","digital_gain","exposure"])
        roi=self.get_roi()
        result=super().setup_acquisition(mode=mode,nframes=nframes)
        self._set_cam_roi(*roi[2:4])
        self.apply_settings(settings)
        return result

    _short_line_duration=84
    _default_prescaler=_short_line_duration*2
    def _get_line_duration(self):
        camlink_mode=self.get_serial_parameter("S")
        return self._short_line_duration*(2 if camlink_mode==0 else 1)
    _p_exposure_timing_mode=interface.EnumParameterClass("exposure_timing_mode",
        {"continuous":0,"iod":1,"iod_exposure":2,"iod_frame_time":3})
    _p_exposure_feature_mode=interface.EnumParameterClass("exposure_feature_mode",
        {"standard":0,"full_well":0x10,"permanent":0x20})
    @interface.use_parameters(_returns=("exposure_timing_mode","exposure_feature_mode"))
    def get_exposure_control_mode(self):
        """
        Get the exposure control mode.

        Return tuple ``(timing_mode, feature_mode)``, where ``timing_mode`` determines how the exposure and
        frame period are timed (continuous, external trigger control, internal control, etc.),
        and ``feature_mode`` controls additional features (permanent exposure, enhanced full well mode).
        See documentation for details.
        """
        mode=self.get_serial_parameter("M")
        timing_mode=mode&0x03
        feature_mode=mode&0x30
        return (timing_mode,feature_mode)
    @interface.use_parameters(timing_mode="exposure_timing_mode",feature_mode="exposure_feature_mode")
    def set_exposure_control_mode(self, timing_mode=None, feature_mode=None):
        """
        Set the exposure control mode.

        `timing_mode` determines how the exposure and frame period are timed (continuous, external trigger control, internal control, etc.),
        and `feature_mode` controls additional features (permanent exposure, enhanced full well mode).
        See documentation for details.
        """
        mode=self.get_serial_parameter("M")
        if timing_mode is not None:
            mode=(mode&0xFC)|timing_mode
        if feature_mode is not None:
            mode=(mode&0xCF)|feature_mode
        mode&=0xF3
        self.set_serial_parameter("M",mode)
        return self.get_exposure_control_mode()
        
    def get_exposure(self):
        """
        Get current exposure.
        
        Note that the actual exposure might be different, depending on the exposure control mode.
        """
        psc=self.get_serial_parameter("K")+1
        exp=self.get_serial_parameter("E")
        return psc*exp/56E6
    def set_exposure(self, exposure, setup_mode=True):
        """
        Set current exposure.
        
        Note that the actual exposure might be different, depending on the exposure control mode.
        If ``setup_mode==True``, automatically set the exposure mode to take the given exposure value into account.
        """
        self.set_serial_parameter("K",self._default_prescaler-1)
        exp=max(int(exposure*56E6),self.get_serial_parameter("N")*self._get_line_duration())
        self.set_serial_parameter("E",exp//self._default_prescaler)
        self._set_device_frame_period(setup_mode=setup_mode)
        return self.get_exposure()

    def get_frame_period(self):
        """
        Get frame period (time between two consecutive frames in the internal trigger mode).
        
        Note that the actual frame period might be different, depending on the exposure control mode.
        """
        psc=self.get_serial_parameter("K")+1
        per=self.get_serial_parameter("F")
        return psc*per/56E6
    def _set_device_frame_period(self, frame_period=None, setup_mode=True):
        if frame_period is None:
            frame_period=self._frame_period
        self.set_serial_parameter("K",self._default_prescaler-1)
        per=int(frame_period*56E6/self._default_prescaler)
        exp=self.get_serial_parameter("E")
        self.set_serial_parameter("F",max(per,exp+2))
        if setup_mode:
            self.set_exposure_control_mode(timing_mode="iod_frame_time",feature_mode="standard")
    def set_frame_period(self, frame_period, setup_mode=True):
        """
        Set frame period (time between two consecutive frames in the internal trigger mode).
        
        Note that the actual frame period might be different, depending on the exposure control mode.
        If ``setup_mode==True``, automatically set the exposure mode to take the given exposure value into account.
        """
        self._frame_period=frame_period
        self._set_device_frame_period(setup_mode=setup_mode)
        return self.get_frame_period()
    _TAcqTimings=camera.TAcqTimings
    def get_frame_timings(self):
        """
        Get acquisition timing.

        Return tuple ``(exposure, frame_period)``.
        """
        return self._TAcqTimings(self.get_exposure(),self.get_frame_period())

    def is_status_line_enabled(self):
        """Check if the status line is on"""
        return bool(self.get_serial_parameter("U")&0x01)
    def enable_status_line(self, enabled=True):
        """Enable or disable status line"""
        v=self.get_serial_parameter("U")
        v=(v&0xFE)|(0x01 if enabled else 0x00)
        self.set_serial_parameter("U",v)
        return self.is_status_line_enabled()

    def get_black_level_offset(self):
        """Get the black level offset"""
        return self.get_serial_parameter("W")
    def set_black_level_offset(self, offset):
        """Set the black level offset"""
        offset=int(min(offset,255))
        self.set_serial_parameter("W",offset)
        return self.get_black_level_offset()

    def get_digital_gain(self):
        """Get the digital gain (0 for 1x, 1 for 2x, 2 for 4x)"""
        return self.get_serial_parameter("G")
    def set_digital_gain(self, gain):
        """Get the digital gain (0 for 1x, 1 for 2x, 2 for 4x)"""
        self.set_serial_parameter("G",int(gain))
        return self.get_digital_gain()


class BonitoIMAQCamera(IBonitoCamera,IMAQFrameGrabber):
    """
    IMAQ+PFCam interface to a AlliedVision Bonito camera.

    Args:
        imaq_name: IMAQ interface name (can be learned by :func:`.IMAQ.list_cameras`; usually, but not always, starts with ``"img"``)
    """
    Error=DeviceError
    GrabberClass=IMAQFrameGrabber
    def __init__(self, imaq_name="img0"):
        super().__init__(imaq_name=imaq_name)




def check_grabber_association(cam):
    """
    Check if the given IMAQ frame grabber corresponds to Bonito camera.
    
    `cam` should be an opened instance of :class:`.IMAQCamera`.
    """
    try:
        cam.serial_flush()
        cam.serial_write("s=?\r")
        res=cam.serial_read(4,timeout=0.1)
        if res!=b"s=?\r":
            return False
        rest=cam.serial_readline(timeout=0.1)
        if not rest.endswith(b"\r\n>"):
            return False
        if not re.match(r"\s+=[A-Za-z0-9]+\s+>",py3.as_str(rest)):
            return False
        return True
    except cam.Error:
        return False



TStatusLine=collections.namedtuple("TStatusLine",["framestamp"])
def get_status_lines(frames):
    """
    Get frame info from the binary status line.

    `frames` can be 2D array (one frame), 3D array (stack of frames, first index is frame number), or list of 1D or 2D arrays.
    Assume that the status line is present; if it isn't, the returned frame info will be a random noise.
    Return a 1D or 2D numpy array, where the first axis (if present) is the frame number, and the last is the status line entry.
    """
    if isinstance(frames,list):
        return [get_status_lines(f) for f in frames]
    sline=frames[...,0,:8].astype("u1").view("<i4")
    if np.all(sline[...,0]==0x4C344D43): # backwards hex for "CM4L", magic for Bonito cameras status line
        return sline[...,1:2]
    return None



class BonitoStatusLineChecker(camera.StatusLineChecker):
    def get_framestamp(self, frames):
        slines=get_status_lines(frames)
        return slines[...,0] if slines is not None else None