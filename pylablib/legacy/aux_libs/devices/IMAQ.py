from ...core.utils import dictionary, py3, general, funcargparse
from ...core.devio import data_format, interface
from ...core.dataproc import image as image_utils

import numpy as np
import contextlib
import time
import collections
import ctypes
from future.utils import raise_from


from . import IMAQ_lib
lib=IMAQ_lib.lib
try:
    lib.initlib()
except (ImportError, OSError):
    pass
IMAQError=IMAQ_lib.IMAQLibError
class IMAQGenericError(RuntimeError):
    "Generic IMAQ camera error."
class IMAQTimeoutError(IMAQGenericError):
    "Timeout while waiting."

_depends_local=[".IMAQ_lib","...core.devio.interface"]



def list_cameras():
    """List all cameras available through IMAQ interface"""
    cameras=[]
    i=0
    try:
        while True:
            if_name=lib.imgInterfaceQueryNames(i)
            cameras.append(py3.as_str(if_name))
            i+=1
    except IMAQError:
        pass
    return cameras


class IMAQCamera(interface.IDevice):
    """
    Generic IMAQ camera interface.

    Args:
        name: interface name (can be learned by :func:`list_cameras`; usually, but not always, starts with ``"cam"``)
    """
    def __init__(self, name="img0"):
        interface.IDevice.__init__(self)
        self.init_done=False
        self.name=name
        self.ifid=None
        self.sid=None
        self.image_indexing="rct"
        self._buffers=[]
        self._buffer_allocation_size=2**20
        self._frame_size=None
        self._buffer_frames=None
        self._last_read_frame=None
        self._start_acq_count=None
        self._last_wait_frame=None
        self._lost_frames=None
        self._acq_params=None
        self.init_done=True
        self._triggers_in={}
        self._triggers_out={}
        self._serial_term_write=""
        self._serial_datatype="bytes"

        self.open()

        self._add_full_info_node("model_data",self.get_model_data)
        self._add_full_info_node("interface_name",lambda: self.name)
        self._add_status_node("buffer_size",lambda: self.get_buffer_status().size)
        self._add_status_node("buffer_status",self.get_buffer_status)
        self._add_settings_node("acquisition_parameters",self.get_acquisition_parameters,self.setup_acquisition)
        self._add_status_node("data_dimensions",self.get_data_dimensions)
        self._add_full_info_node("detector_size",self.get_detector_size)
        self._add_settings_node("roi",self.get_roi,self.set_roi)
        self._add_status_node("roi_limits",self.get_roi_limits)
        self._add_settings_node("triggers_in_cfg",self._get_triggers_in_cfg,self._set_triggers_in_cfg)
        self._add_settings_node("triggers_out_cfg",self._get_triggers_out_cfg,self._set_triggers_out_cfg)

        
    def open(self):
        """Open connection to the camera"""
        self.ifid=lib.imgInterfaceOpen(self.name)
        self.sid=lib.imgSessionOpen(self.ifid)
        self.post_open()
    def close(self):
        """Close connection to the camera"""
        if self.sid is not None:
            lib.imgClose(self.sid)
            self.sid=None
            lib.imgClose(self.ifid)
            self.ifid=None
    def reset(self):
        """Reset connection to the camera"""
        if self.ifid is not None:
            lib.imgClose(self.sid)
            self.sid=None
            lib.imgInterfaceReset(self.ifid)
            self.sid=lib.imgSessionOpen(self.ifid)
    def is_opened(self):
        """Check if the device is connected"""
        return self.sid is not None

    def post_open(self):
        """Action to automatically call on opening"""
        pass

    def _norm_attr(self, attr):
        if attr not in IMAQ_lib.IMAQ_attrs_inv and ("IMG_ATTR_"+attr) in IMAQ_lib.IMAQ_attrs_inv:
            return "IMG_ATTR_"+attr
        return attr
    def get_int_value(self, attr, default=None):
        """Get value of an integer attribute with a given name"""
        try:
            return lib.imgGetAttribute_uint32(self.sid,self._norm_attr(attr))
        except IMAQError:
            if default is None:
                raise
            return default
    def set_int_value(self, attr, value):
        """Set value of an integer attribute with a given name"""
        lib.imgSetAttribute2_uint32(self.sid,self._norm_attr(attr),value)
        return lib.imgGetAttribute_uint32(self.sid,self._norm_attr(attr))
    def get_float_value(self, attr, default=None):
        """Get value of a floating point attribute with a given name"""
        try:
            return lib.imgGetAttribute_double(self.sid,self._norm_attr(attr))
        except IMAQError:
            if default is None:
                raise
            return default
    def set_float_value(self, attr, value):
        """Set value of a floating point attribute with a given name"""
        lib.imgSetAttribute2_double(self.sid,self._norm_attr(attr),value)
        return lib.imgGetAttribute_double(self.sid,self._norm_attr(attr))
    
    ModelData=collections.namedtuple("ModelData",["serial"])
    def get_model_data(self):
        """
        Get camera model data.

        Return tuple ``(serial,)``.
        """
        serial=self.get_int_value("GETSERIAL")
        return self.ModelData(serial)

    def _get_data_dimensions_rc(self):
        return self.get_int_value("ROI_HEIGHT"),self.get_int_value("ROI_WIDTH")
    def get_data_dimensions(self):
        """Get the current data dimension (taking ROI and binning into account)"""
        return image_utils.convert_shape_indexing(self._get_data_dimensions_rc(),"rc",self.image_indexing)
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        _,_,mw,mh=lib.imgSessionFitROI(self.sid,0,0,0,2**31-1,2**31-1)
        return mw,mh
    def get_roi(self):
        """
        Get current ROI.

        Return tuple ``(hstart, hend, vstart, vend)``.
        """
        t,l,h,w=lib.imgSessionGetROI(self.sid)
        return l,l+w,t,t+h
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None):
        """
        Setup camera ROI.

        By default, all non-supplied parameters take extreme values.
        """
        
        det_size=self.get_detector_size()
        if hend is None:
            hend=det_size[0]
        if vend is None:
            vend=det_size[1]
        fit_roi=lib.imgSessionFitROI(self.sid,0,vstart,hstart,max(vend-vstart,1),max(hend-hstart,1))
        if lib.imgSessionGetROI(self.sid)!=fit_roi:
            lib.imgSessionConfigureROI(self.sid,*fit_roi)
        return self.get_roi()
    def get_roi_limits(self):
        """
        Get the minimal and maximal ROI parameters.

        Return tuple ``(min_roi, max_roi)``, where each element is in turn 4-tuple describing the ROI.
        """
        minp=lib.imgSessionFitROI(self.sid,0,0,0,1,1)
        detsize=self.get_detector_size()
        min_roi=(0,0)+minp[2:]
        max_roi=(detsize[0]-minp[2],detsize[1]-minp[3])+detsize
        return (min_roi,max_roi)

    _trigger_pol={"high":"IMG_TRIG_POLAR_ACTIVEH","low":"IMG_TRIG_POLAR_ACTIVEL"}
    _trigger_type={"none":"IMG_SIGNAL_NONE","ext":"IMG_SIGNAL_EXTERNAL","rtsi":"IMG_SIGNAL_RTSI","iso_in":"IMG_SIGNAL_ISO_IN",
        "iso_out":"IMG_SIGNAL_ISO_OUT","status":"IMG_SIGNAL_STATUS","software":"IMG_SIGNAL_SOFTWARE_TRIGGER"}
    _trigger_action={"none":"IMG_TRIG_ACTION_NONE","capture":"IMG_TRIG_ACTION_CAPTURE",
        "bufflist":"IMG_TRIG_ACTION_BUFLIST","buffer":"IMG_TRIG_ACTION_BUFFER","stop":"IMG_TRIG_ACTION_STOP"}
    _trigger_drive={"disable":"IMG_TRIG_DRIVE_DISABLED","acq_in_progress":"IMG_TRIG_DRIVE_AQ_IN_PROGRESS","acq_done":"IMG_TRIG_DRIVE_AQ_DONE",
        "unasserted":"IMG_TRIG_DRIVE_UNASSERTED","asserted":"IMG_TRIG_DRIVE_ASSERTED",
        "hsync":"IMG_TRIG_DRIVE_HSYNC","vsync":"IMG_TRIG_DRIVE_VSYNC","frame_start":"IMG_TRIG_DRIVE_FRAME_START","frame_done":"IMG_TRIG_DRIVE_FRAME_DONE"}


    def configure_trigger_in(self, trig_type, trig_line=0, trig_pol="high", action="none", timeout=None):
        """
        Configure input trigger.

        Args:
            trig_type(str): trigger source type; can be ``"ext"``, ``"rtsi"``, ``"iso_in"``, or ``"software"``
            trig_line(int): trigger line number
            trig_pol(str): trigger polarity; can be ``"high"`` or ``"low"``
            action(str): trigger action; can be ``"none"`` (disable trigger), ``"capture"`` (start capturing), ``"stop"`` (stop capturing),
                ``"buffer"`` (capture a single frame), or ``"bufflist"`` (capture the whole buffer list once)
            timeout(float): timeout in seconds; ``None`` means not timeout.
        """
        funcargparse.check_parameter_range(trig_type,"trig_type",{"ext","rtsi","iso_in","software"})
        funcargparse.check_parameter_range(trig_pol,"trig_pol",{"high","low"})
        funcargparse.check_parameter_range(action,"action",list(self._trigger_action))
        itrig_type=IMAQ_lib.IMAQ_signal_type_inv[self._trigger_type.get(trig_type,trig_type)]
        itrig_pol=IMAQ_lib.IMAQ_trig_pol_inv[self._trigger_pol.get(trig_pol,trig_pol)]
        iaction=IMAQ_lib.IMAQ_trig_action_inv[self._trigger_action.get(action,action)]
        timeout=int(timeout*1E3) if timeout is not None else IMAQ_lib.IMAQInfiniteTimout
        lib.imgSessionTriggerConfigure2(self.sid,itrig_type,trig_line,itrig_pol,timeout,iaction)
        self._triggers_in[(trig_type,trig_line)]=(trig_pol,action,timeout)
    def _get_triggers_in_cfg(self):
        return sorted(list(self._triggers_in.items()))
    def _set_triggers_in_cfg(self, cfg):
        for (tt,tl),(tp,act,to) in cfg:
            self.configure_trigger_in(tt,tl,tp,act,to)

    def configure_trigger_out(self, trig_type, trig_line=0, trig_pol="high", trig_drive="disable"):
        """
        Configure trigger output.

        Args:
            trig_type(str): trigger drive destination type; can be ``"ext"``, ``"rtsi"``, or ``"iso_out"``
            trig_line(int): trigger line number
            trig_pol(str): trigger polarity; can be ``"high"`` or ``"low"``
            trig_drive(str): trigger output signal; can be ``"disable"`` (disable drive),
                ``"acq_in_progress"`` (asserted when acquisition is started),``"acq_done"`` (asserted when acquisition is done),
                ``"unasserted"`` (force unasserted level), ``"asserted"`` (force asserted level),
                ``"hsync"`` (asserted on start of a single line start), ``"vsync"`` (asserted on start of a frame scan),
                ``"frame_start"`` (asserted when a single frame is captured), or ``"frame_done"`` (asserted when a single frame is done)
        """
        funcargparse.check_parameter_range(trig_type,"trig_type",{"ext","rtsi","iso_out"})
        funcargparse.check_parameter_range(trig_pol,"trig_pol",{"high","low"})
        funcargparse.check_parameter_range(trig_drive,"trig_drive",list(self._trigger_drive))
        itrig_type=IMAQ_lib.IMAQ_signal_type_inv[self._trigger_type.get(trig_type,trig_type)]
        itrig_pol=IMAQ_lib.IMAQ_trig_pol_inv[self._trigger_pol.get(trig_pol,trig_pol)]
        itrig_drive=IMAQ_lib.IMAQ_trig_drive_src_inv[self._trigger_drive.get(trig_drive,trig_drive)]
        lib.imgSessionTriggerDrive2(self.sid,itrig_type,trig_line,itrig_pol,itrig_drive)
        self._triggers_out[(trig_type,trig_line)]=(trig_pol,trig_drive)
    def _get_triggers_out_cfg(self):
        return sorted(list(self._triggers_out.items()))
    def _set_triggers_out_cfg(self, cfg):
        for (tt,tl),(tp,td) in cfg:
            self.configure_trigger_out(tt,tl,tp,td)

    def read_trigger(self, trig_type, trig_line=0, trig_pol="high"):
        """
        Read current value of a trigger (input or output).

        Args:
            trig_type(str): trigger drive destination type; can be ``"ext"``, ``"rtsi"``, ``"iso_in"``, or ``"iso_out"``
            trig_line(int): trigger line number
            trig_pol(str): trigger polarity; can be ``"high"`` or ``"low"``
        """
        funcargparse.check_parameter_range(trig_type,"trig_type",{"ext","rtsi","iso_in","iso_out"})
        funcargparse.check_parameter_range(trig_pol,"trig_pol",{"high","low"})
        itrig_type=IMAQ_lib.IMAQ_signal_type_inv[self._trigger_type.get(trig_type,trig_type)]
        itrig_pol=IMAQ_lib.IMAQ_trig_pol_inv[self._trigger_pol.get(trig_pol,trig_pol)]
        return lib.imgSessionTriggerRead2(self.sid,itrig_type,trig_line,itrig_pol)

    def clear_all_triggers(self):
        """Disable all triggers of the session"""
        lib.imgSessionTriggerClear(self.sid)
        self._triggers_in={}
        self._triggers_out={}


    def setup_serial_params(self, write_term="", datatype="bytes"):
        """
        Setup default serial communication parameters.

        Args:
            write_term: default termintor character to be added to the sent messages
            datatype: type of the result of read commands; can be ``"bytes"`` (return raw bytes), or ``"str"`` (convert into UTF-8 string)
        """
        self._serial_term_write=write_term
        self._serial_datatype=datatype
    def serial_write(self, msg, timeout=3., term=None):
        """
        Write message into CameraLink serial port.
        
        Args:
            timeout: operation timeout (in seconds)
            term: additional write terminator character to add to the message;
                if ``None``, use the value set up using :meth:`setup_serial_params` (by default, no additional terminator)
        """
        try:
            if term is None:
                term=self._serial_term_write
            msg=py3.as_builtin_bytes(msg)+py3.as_builtin_bytes(term)
            return lib.imgSessionSerialWrite(self.sid,msg,int(timeout*1000))
        except IMAQError as e:
            if e.name=="IMG_ERR_SERIAL_WRITE_TIMEOUT":
                raise_from(IMAQTimeoutError(),None)
            else:
                raise
    def serial_read(self, n, timeout=3., datatype=None):
        """
        Read specified number of bytes from CameraLink serial port.
        
        Args:
            n: number of bytes to read
            timeout: operation timeout (in seconds)
            datatype: return datatype; can be ``"bytes"`` (return raw bytes), or ``"str"`` (convert into UTF-8 string)
                if ``None``, use the value set up using :meth:`setup_serial_params` (by default, ``"bytes"``)
        """
        try:
            msg,_=lib.imgSessionSerialReadBytes(self.sid,int(timeout*1000),n)
            datatype=datatype or self._serial_datatype
            return msg if datatype=="bytes" else py3.as_str(msg)
        except IMAQError as e:
            if e.name=="IMG_ERR_SERIAL_READ_TIMEOUT":
                raise_from(IMAQTimeoutError(),None)
            else:
                raise
    def serial_readline(self, timeout=3., datatype=None):
        """
        Read bytes from CameraLink serial port until the termination character (defined in camera file) is encountered.
        
        Args:
            timeout: operation timeout (in seconds)
            datatype: return datatype; can be ``"bytes"`` (return raw bytes), or ``"str"`` (convert into UTF-8 string)
                if ``None``, use the value set up using :meth:`setup_serial_params` (by default, ``"bytes"``)
        """
        try:
            msg,_=lib.imgSessionSerialRead(self.sid,int(timeout*1000))
            datatype=datatype or self._serial_datatype
            return msg if datatype=="bytes" else py3.as_str(msg)
        except IMAQError as e:
            if e.name=="IMG_ERR_SERIAL_READ_TIMEOUT":
                raise_from(IMAQTimeoutError(),None)
            else:
                raise
    def serial_flush(self):
        """Flush CameraLink serial port"""
        lib.imgSessionSerialFlush(self.sid)


    def _get_ctypes_buffer(self):
        if self._buffers:
            cbuffs=(ctypes.c_char_p*self._buffer_frames)()
            frames_per_buff=len(self._buffers[0])//self._frame_size
            for i,b in enumerate(self._buffers):
                for j in range(frames_per_buff):
                    cbuffs[i*frames_per_buff+j]=ctypes.addressof(b)+j*self._frame_size
            return cbuffs
        else:
            return None
    def _deallocate_buffers(self):
        self._buffers=[]
        self._buffer_frames=None
        self._frame_size=None
        self._last_read_frame=None
        self._start_acq_count=None
        self._lost_frames=None
    def _allocate_buffers(self, n):
        self._deallocate_buffers()
        self._frame_size=self._get_buffer_size()
        frames_per_buff=max(self._buffer_allocation_size//self._frame_size,1)
        nbuffs=(n-1)//frames_per_buff+1
        if nbuffs==1:
            frames_per_buff=n
        self._buffers=[ctypes.create_string_buffer(frames_per_buff*self._frame_size) for _ in range(nbuffs)]
        self._buffer_frames=nbuffs*frames_per_buff
    def _acquired_frames(self):
        if self._start_acq_count is None:
            return 0
        return self.get_int_value("FRAME_COUNT",0)-self._start_acq_count
    def _get_buffer_num(self, frame):
        if not self._buffers:
            return -1
        return frame%self._buffer_frames
        


    def setup_acquisition(self, continuous, frames):
        """
        Setup acquisition mode.

        `continuous` determines whether acquisition runs continuously, or stops after the given number of frames
        (note that :meth:`.IMAQCamera.acquisition_in_progress` would still return ``True`` in this case, even though new frames are no longer acquired).
        `frames` sets up number of frame buffers.
        If ``start==True``, start acquisition directly after setup.
        """
        self.clear_acquisition()
        self._allocate_buffers(frames)
        cbuffs=self._get_ctypes_buffer()
        if continuous:
            lib.imgRingSetup(self.sid,len(cbuffs),cbuffs,0,0)
        else:
            skips=(ctypes.c_uint32*len(cbuffs))(0)
            lib.imgSequenceSetup(self.sid,len(cbuffs),cbuffs,skips,0,0)
        self._acq_params=(continuous,frames)
        self._last_read_frame=-1
        self._start_acq_count=0
        self._lost_frames=0
        self._last_wait_frame=-1
    def clear_acquisition(self):
        """Clear all acquisition details and free all buffers"""
        if self._acq_params:
            self.stop_acquisition()
            lib.imgSessionAbort(self.sid)
            self.clear_all_triggers()
            self._deallocate_buffers()
            self._acq_params=None
    def get_acquisition_parameters(self):
        """Return acquisition parameters ``(continuous, frames_buffer)``."""
        return self._acq_params
    def start_acquisition(self):
        """Start acquisition"""
        self.stop_acquisition()
        if self._acq_params is None:
            self.setup_acquisition(True,100)
        self._start_acq_count=self.get_int_value("FRAME_COUNT",0)
        self._last_read_frame=-1
        self._lost_frames=0
        lib.imgSessionStartAcquisition(self.sid)
    def stop_acquisition(self):
        """Stop acquisition"""
        lib.imgSessionStopAcquisition(self.sid)
        self._last_wait_frame=-1
    def acquisition_in_progress(self):
        """Check if acquisition is in progress"""
        return bool(lib.imgSessionStatus(self.sid)[0])
    
    @contextlib.contextmanager
    def pausing_acquisition(self):
        """
        Context manager which temporarily pauses acquisition during execution of ``with`` block.

        Useful for applying certain settings which can't be changed during the acquisition (e.g., ROI or bit depth).
        """
        acq_params=self._acq_params
        acq_in_progress=self.acquisition_in_progress()
        try:
            self.clear_acquisition()
            yield
        finally:
            if acq_params:
                self.setup_acquisition(*acq_params)
            if acq_in_progress:
                self.start_acquisition()

    TBufferStatus=collections.namedtuple("TBufferStatus",["unread","lost","size"])
    def get_buffer_status(self):
        """
        Get buffer fill status.

        Return tuple ``(unread, lost, size)``, where ``unread`` is the number of acquired but not read frames,
        ``lost`` is the number of lost (written over) frames and ``size`` is the total buffer size (in frames).
        """
        rng=self.get_new_images_range()
        unread=0 if rng is None else rng[1]-rng[0]+1
        if rng is not None:
            lost_frames=self._lost_frames+max(0,rng[1]-self._buffer_frames-self._last_read_frame)
        else:
            lost_frames=0
        return self.TBufferStatus(unread,lost_frames,self._buffer_frames)
    def get_new_images_range(self):
        """
        Get the range of the new images.
        
        Return tuple ``(first, last)`` with images range (inclusive).
        If no images are available, return ``None``.
        """
        frame_cnt=self._acquired_frames()
        if not self._buffers or frame_cnt<=0:
            return None
        if self._last_read_frame+1>=frame_cnt:
            return None
        if self._last_read_frame<frame_cnt-self._buffer_frames:
            return (frame_cnt-self._buffer_frames,frame_cnt-1)
        return (self._last_read_frame+1,frame_cnt-1)
    def wait_for_frame(self, since="lastread", timeout=20.):
        """
        Wait for a new camera frame.

        `since` specifies what constitutes a new frame.
        Can be ``"lastread"`` (wait for a new frame after the last read frame),
        ``"lastwait"`` (wait for a new frame after last :meth:`wait_for_frame` call),
        or ``"now"`` (wait for a new frame acquired after this function call).
        If `timeout` is exceeded, raise :exc:`.IMAQLibError`.
        `period` specifies camera polling period.
        """
        if not self.acquisition_in_progress():
            return
        last_acq_frame=self._acquired_frames()-1
        if since=="lastread" and last_acq_frame>self._last_read_frame:
            self._last_wait_frame=last_acq_frame
            return
        if since=="lastwait" and last_acq_frame>self._last_wait_frame:
            self._last_wait_frame=last_acq_frame
            return
        try:
            lib.imgSessionWaitSignal2(self.sid,4,11,0,int(timeout*1000))
        except IMAQError as e:
            if e.name=="IMG_ERR_TIMEOUT":
                raise_from(IMAQTimeoutError(),None)
            elif e.name=="IMG_ERR_BOARD_NOT_RUNNING" and not self.acquisition_in_progress():
                pass
            else:
                raise
        self._last_wait_frame=self._acquired_frames()-1
        return
        

    def _read_frame_data_raw(self, buffer_frame_num):
        """Return raw bytes string corresponding to the given buffer frame number"""
        frames_per_buff=len(self._buffers[0])//self._frame_size
        ibuff=buffer_frame_num//frames_per_buff
        jbuff=buffer_frame_num%frames_per_buff
        return self._buffers[ibuff][jbuff*self._frame_size:jbuff*self._frame_size+self._frame_size]
    def _read_buff_data_raw(self, buffer_frame_num, max_nframes):
        """
        Read raw bytes string containing one or several frames starting with the given buffer frame number.
        
        Read all the frames up to the end of the buffer containing given frame, or up to `max_nframes` frames, whichever is smaller.
        Return tuple ``(number_returned, raw_data)``, where `number_returned` is the total number of returned frames (between 1 and `max_n_frames`),
        and `raw_data` is a binary string of the size ``self._frame_size*number_returned``.

        Function exists only to speed up reading of large number of small frames.
        """
        frames_per_buff=len(self._buffers[0])//self._frame_size
        ibuff=buffer_frame_num//frames_per_buff
        jbuff=buffer_frame_num%frames_per_buff
        nread=min(max_nframes,frames_per_buff-jbuff)
        return nread,self._buffers[ibuff][jbuff*self._frame_size:(jbuff+nread)*self._frame_size]
    
    def _get_buffer_bpp(self):
        return self.get_int_value("BYTESPERPIXEL",1)
    def _get_buffer_dtype(self):
        return "<u{}".format(self._get_buffer_bpp())
    def _get_buffer_size(self):
        bpp=self._get_buffer_bpp()
        roi=self.get_roi()
        w,h=roi[1]-roi[0],roi[3]-roi[2]
        return w*h*bpp
    def _parse_buffer(self, buffer, dim=None, bpp=None, nframes=1):
        r,c=dim or self._get_data_dimensions_rc()
        bpp=bpp or self.get_int_value("BYTESPERPIXEL",1)
        if len(buffer)!=nframes*r*c*bpp:
            raise ValueError("wrong buffer size: expected {}x{}x{}x{}={}, got {}".format(nframes,r,c,bpp,nframes*r*c*bpp,len(buffer)))
        dt="<u{}".format(bpp)
        return np.frombuffer(buffer,dtype=dt).reshape((nframes,r,c))
    def _read_multiple_images_raw(self, rng=None, peek=False, missing_frame="skip"):
        """
        Read multiple images specified by `rng` (by default, all un-read images).

        If ``peek==True``, return images but not mark them as read.
        `missing_frame` determines what to do with frames which are out of range (missing or lost):
        can be ``"none"`` (replacing them with ``None``), ``"zero"`` (same as ``None``, added for compatibility with :meth:`read_multiple_images`),
        or ``"skip"`` (skipping them).
        """
        if not self._buffers:
            return None
        last_acq_frame=self._acquired_frames()-1
        last_valid_buffer=last_acq_frame-self._buffer_frames
        if rng is None:
            rng=self.get_new_images_range()
        if rng[1]<last_valid_buffer:
            read_rng=0,-1
        else:
            read_rng=max(rng[0],last_valid_buffer),rng[1]
        raw_frames=[self._read_frame_data_raw(self._get_buffer_num(n)) for n in range(read_rng[0],read_rng[1]+1)]
        if missing_frame=="none":
            raw_frames=[None]*(rng[1]-rng[0]-len(raw_frames))+raw_frames
        if not peek:
            if rng[1]>self._last_read_frame:
                passed_frames=rng[1]-self._last_read_frame
                read_frames=read_rng[1]-read_rng[0]+1
                if passed_frames>read_frames:
                    self._lost_frames+=passed_frames-read_frames
                self._last_read_frame=rng[1]
        return raw_frames
    def _read_multiple_images_raw_fastbuff(self, rng=None):
        """
        Read multiple images specified by `rng` (by default, all un-read images).

        Some frames in the result are "stuck together" in a single buffer, if their memory locations are continuous.
        Return list ``[(number_of_frames, raw_data)]``, where `number_of_frames` specifies number of frames in a given array element,
        and `raw_data` is the binary string corresponding to these frames (of the size ``self._frame_size*number_returned``).
        Compared to :meth:`_read_multiple_images_raw`, always assumes ``peek==False`` and ``missing_frame="skip"`` (default values).

        Function exists only to speed up reading of large number of small frames.
        """
        if not self._buffers:
            return None
        last_acq_frame=self._acquired_frames()-1
        last_valid_buffer=last_acq_frame-self._buffer_frames
        if rng is None:
            rng=self.get_new_images_range()
        if rng[1]<last_valid_buffer:
            read_rng=0,-1
        else:
            read_rng=max(rng[0],last_valid_buffer),rng[1]
        raw_frames=[]
        i=rng[0]
        while i<rng[1]+1:
            nread,data=self._read_buff_data_raw(self._get_buffer_num(i),rng[1]+1-i)
            i+=nread
            raw_frames.append((nread,data))
        if rng[1]>self._last_read_frame:
            passed_frames=rng[1]-self._last_read_frame
            read_frames=read_rng[1]-read_rng[0]+1
            if passed_frames>read_frames:
                self._lost_frames+=passed_frames-read_frames
            self._last_read_frame=rng[1]
        return raw_frames
    def read_multiple_images(self, rng=None, peek=False, missing_frame="skip"):
        """
        Read multiple images specified by `rng` (by default, all un-read images).

        If ``peek==True``, return images but not mark them as read.
        `missing_frame` determines what to do with frames which are out of range (missing or lost):
        can be ``"none"`` (replacing them with ``None``), ``"zero"`` (replacing them with zero-filled frame),
        or ``"skip"`` (skipping them).
        """
        raw_data=self._read_multiple_images_raw(rng=rng,peek=peek,missing_frame=missing_frame)
        if raw_data is None:
            return None
        dim=self._get_data_dimensions_rc()
        bpp=self.get_int_value("BYTESPERPIXEL",1)
        parsed_data=[(self._parse_buffer(b,dim=dim,bpp=bpp) if b is not None else None) for b in raw_data]
        if missing_frame=="zero":
            dt=self._get_buffer_dtype()
            parsed_data=[(np.zeros(dim,dtype=dt) if f is None else f) for f in parsed_data]
        if self.image_indexing!="rct":
            parsed_data=[(None if f is None else image_utils.convert_image_indexing(f,"rct",self.image_indexing)) for f in parsed_data]
        return parsed_data
    def read_multiple_images_fastbuff(self, rng=None):
        """
        Read multiple images specified by `rng` (by default, all un-read images).
        
        Some frames in the result are "stuck together" in a single buffer, if their memory locations are continuous.
        Return list ``[(number_of_frames, raw_data)]``, where `number_of_frames` specifies number of frames in a given array element,
        and `raw_data` is the binary string corresponding to these frames (of the size ``self._frame_size*number_returned``).
        Compared to :meth:`read_multiple_images`, always assumes ``peek==False`` and ``missing_frame="skip"`` (default values).
        Also, always return frames in ``"rct"`` format (row-first indexing, going from the top).

        Function exists only to speed up reading of large number of small frames.
        """
        raw_data=self._read_multiple_images_raw_fastbuff(rng=rng)
        if raw_data is None:
            return None
        dim=self._get_data_dimensions_rc()
        bpp=self.get_int_value("BYTESPERPIXEL",1)
        parsed_data=[(nread,self._parse_buffer(b,dim=dim,bpp=bpp,nframes=nread)) for (nread,b) in raw_data]
        return parsed_data

    def snap(self, timeout=20.):
        """Snap a single image (with preset image read mode parameters)"""
        return self.grab(1,frame_timeout=timeout)[0]

    def grab(self, n, buff_frames=5000, frame_timeout=20., missing_frame="none", return_buffer_status=False):
        """
        Snap `n` images (with preset image read mode parameters)
        
        `buff_frames` determines buffer size.
        Timeout is specified for a single-frame acquisition, not for the whole acquisition time.
        `missing_frame` determines what to do with frames which have been lost:
        can be ``"none"`` (replacing them with ``None``), ``"zero"`` (replacing them with zero-filled frame),
        or ``"skip"`` (skipping them, while still keeping total frames number to `n`).
        """
        buff_frames=min(n,buff_frames)
        frames=[]
        self.setup_acquisition(1 if buff_frames<n else 0,buff_frames)
        self.start_acquisition()
        try:
            while len(frames)<n:
                self.wait_for_frame(timeout=frame_timeout)
                frames+=self.read_multiple_images(missing_frame=missing_frame)
            return (frames[:n],self.get_buffer_status()) if return_buffer_status else frames[:n]
        finally:
            self.clear_acquisition()