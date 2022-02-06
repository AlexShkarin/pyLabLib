from . import niimaq_lib
from .niimaq_lib import wlib as lib, IMAQError, IMAQLibError

from ...core.utils import py3, funcargparse
from ...core.devio import interface
from ..interface import camera

import numpy as np
import collections
import ctypes
import warnings


class IMAQTimeoutError(IMAQError):
    "IMAQ frame timeout error"



def list_cameras():
    """List all cameras available through IMAQ interface"""
    lib.initlib()
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

def get_cameras_number():
    """Get number of connected IMAQ cameras"""
    return len(list_cameras())




TDeviceInfo=collections.namedtuple("TDeviceInfo",["serial_number","interface"])
class IMAQFrameGrabber(camera.IROICamera):
    """
    Generic IMAQ frame grabber interface.

    Compared to :class:`IMAQCamera`, has more permissive initialization arguments,
    which simplifies its use as a base class for expanded cameras.

    Args:
        imaq_name: interface name (can be learned by :func:`list_cameras`; usually, but not always, starts with ``"cam"`` or ``"img"``)
        do_open: if ``False``, skip the last step of opening the device (should be opened in a subclass)
    """
    Error=IMAQError
    TimeoutError=IMAQTimeoutError
    def __init__(self, imaq_name="img0", do_open=True, **kwargs):
        super().__init__(**kwargs)
        lib.initlib()
        self.imaq_name=imaq_name
        self.ifid=None
        self.sid=None
        self._buffer_mgr=camera.ChunkBufferManager()
        self._max_nbuff=None
        self._start_acq_count=None
        self._triggers_in={}
        self._triggers_out={}
        self._serial_term_write=""
        self._serial_datatype="bytes"

        self._add_info_variable("device_info",self.get_device_info)
        self._add_info_variable("grabber_attributes",self.get_all_grabber_attribute_values,priority=-5)
        self._add_settings_variable("serial_params",self.get_serial_params,self.setup_serial_params)
        self._add_settings_variable("triggers_in_cfg",self._get_triggers_in_cfg,self._set_triggers_in_cfg)
        self._add_settings_variable("triggers_out_cfg",self._get_triggers_out_cfg,self._set_triggers_out_cfg)

        if do_open:
            self.open()


    def _get_connection_parameters(self):
        return self.imaq_name
    def open(self):
        """Open connection to the camera"""
        super().open()
        if self.sid is None:
            self.ifid=lib.imgInterfaceOpen(self.imaq_name)
            self.sid=lib.imgSessionOpen(self.ifid)
            self._check_grabber_attributes()
    def close(self):
        """Close connection to the camera"""
        if self.sid is not None:
            self.clear_acquisition()
            lib.imgClose(self.sid,1)
            self.sid=None
            lib.imgClose(self.ifid,1)
            self.ifid=None
        super().close()
    def reset(self):
        """Reset connection to the camera"""
        if self.ifid is not None:
            lib.imgClose(self.sid,1)
            self.sid=None
            lib.imgInterfaceReset(self.ifid)
            self.sid=lib.imgSessionOpen(self.ifid)
    def is_opened(self):
        """Check if the device is connected"""
        return self.sid is not None

    def _check_grabber_attributes(self):
        timeout=self.get_grabber_attribute_value("FRAMEWAIT_MSEC",1000)
        if timeout<500:
            msg=(   "frame timeout is set too low ({} ms), which may results in problems on acquisition restart; "
                    "recommend setting it to at least 500 ms in NI-MAX (Acquisition Attributes -> Timeout)".format(timeout))
            warnings.warn(msg)
    def _get_attr_index(self, attr):
        if isinstance(attr,py3.textstring):
            if attr in niimaq_lib.dIMG_ATTR:
                return niimaq_lib.dIMG_ATTR[attr]
            if "IMG_ATTR_"+attr in niimaq_lib.dIMG_ATTR:
                return niimaq_lib.dIMG_ATTR["IMG_ATTR_"+attr]
        return attr
    def _get_attr_kind(self, attr):
        attr_name=niimaq_lib.IMG_ATTR(attr).name
        if attr_name in niimaq_lib.IMG_ATTR_DOUBLE:
            return "double"
        if attr_name in niimaq_lib.IMG_ATTR_UINT64:
            return "uint64"
        if attr_name in niimaq_lib.IMG_ATTR_NA:
            return None
        return "uint32"
    _p_attr_kind=interface.EnumParameterClass("attr_kind",["uint32","uint64","double","auto"])
    @interface.use_parameters(kind="attr_kind")
    def get_grabber_attribute_value(self, attr, default=None, kind="auto"):
        """
        Get value of an attribute with a given name or index.
        
        If `default` is not ``None``, return `default` if the attribute is not supported; otherwise, raise an error.
        `kind` is the attribute kind, and it can be ``"uint32"``, ``"uint64"``, ``"double"``,
        or ``"auto"`` (autodetect based on the stored list of attribute kinds).
        """
        attr=self._get_attr_index(attr)
        if kind=="auto":
            kind=self._get_attr_kind(attr)
        try:
            if kind=="uint32":
                return lib.imgGetAttribute_uint32(self.sid,attr)
            if kind=="uint64":
                return lib.imgGetAttribute_uint64(self.sid,attr)
            elif kind=="double":
                return lib.imgGetAttribute_double(self.sid,attr)
        except IMAQError:
            if default is None:
                raise
            return default
    @interface.use_parameters(kind="attr_kind")
    def set_grabber_attribute_value(self, attr, value, kind="int32"):
        """
        Set value of an attribute with a given name or index.
        
        `kind` is the attribute kind, and it can be ``"uint32"``, ``"uint64"``, ``"double"``,
        or ``"auto"`` (autodetect based on the stored list of attribute kinds).
        """
        attr=self._get_attr_index(attr)
        if kind=="auto":
            kind=self._get_attr_kind(attr)
        if kind=="uint32":
            lib.imgSetAttribute2_uint32(self.sid,attr,value)
            return lib.imgGetAttribute_uint32(self.sid,attr)
        if kind=="uint64":
            lib.imgSetAttribute2_uint64(self.sid,attr,value)
            return lib.imgGetAttribute_uint64(self.sid,attr)
        elif kind=="double":
            lib.imgSetAttribute2_double(self.sid,attr,value)
            return lib.imgGetAttribute_double(self.sid,attr)
    def get_all_grabber_attribute_values(self):
        """
        Get a dictionary of all readable attributes.

        The attributes types are autodetected, and some of the types of uncommon attributes may be misrepresented.
        """
        values={}
        for k,v in niimaq_lib.dIMG_ATTR.items():
            if self._get_attr_kind(v) is None:
                continue
            try:
                values[k]=self.get_grabber_attribute_value(v)
            except IMAQError:
                pass
        return values
    
    def get_device_info(self):
        """
        Get camera model data.

        Return tuple ``(serial, interface)`` with the board serial number and an the interface type (e.g., ``"1430"`` for NI PCIe-1430)
        """
        serial_number=self.get_grabber_attribute_value("GETSERIAL")
        interface_type=self.get_grabber_attribute_value("INTERFACE_TYPE")
        return TDeviceInfo("{:08X}".format(serial_number),"{:04x}".format(interface_type))

    def _get_data_dimensions_rc(self):
        return self.get_grabber_attribute_value("ROI_HEIGHT"),self.get_grabber_attribute_value("ROI_WIDTH")
    def get_detector_size(self):
        _,_,mw,mh=lib.imgSessionFitROI(self.sid,0,0,0,2**31-1,2**31-1)
        return mw,mh
    get_grabber_detector_size=get_detector_size
    def get_roi(self):
        t,l,h,w=lib.imgSessionGetROI(self.sid)
        return l,l+w,t,t+h
    get_grabber_roi=get_roi
    @camera.acqcleared
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None):
        det_size=self.get_detector_size()
        if hend is None:
            hend=det_size[0]
        if vend is None:
            vend=det_size[1]
        fit_roi=lib.imgSessionFitROI(self.sid,0,vstart,hstart,max(vend-vstart,1),max(hend-hstart,1))
        if lib.imgSessionGetROI(self.sid)!=fit_roi:
            lib.imgSessionConfigureROI(self.sid,*fit_roi)
        return self.get_roi()
    set_grabber_roi=set_roi
    def get_roi_limits(self, hbin=1, vbin=1):
        minp=lib.imgSessionFitROI(self.sid,0,0,0,1,1)
        detsize=self.get_detector_size()
        hlim=camera.TAxisROILimit(minp[2],detsize[0],1,1,1)
        vlim=camera.TAxisROILimit(minp[3],detsize[1],1,1,1)
        return hlim,vlim
    get_grabber_roi_limits=get_roi_limits

    _trig_pol={ "high":niimaq_lib.IMG_TRIG_POL.IMG_TRIG_POLAR_ACTIVEH,
                "low":niimaq_lib.IMG_TRIG_POL.IMG_TRIG_POLAR_ACTIVEL}
    _p_trig_pol=interface.EnumParameterClass("trig_pol",_trig_pol)
    _trig_type={    "none":niimaq_lib.IMG_SIGNAL_TYPE.IMG_SIGNAL_RTSI,
                    "ext":niimaq_lib.IMG_SIGNAL_TYPE.IMG_SIGNAL_EXTERNAL,
                    "rtsi":niimaq_lib.IMG_SIGNAL_TYPE.IMG_SIGNAL_RTSI,
                    "iso_in":niimaq_lib.IMG_SIGNAL_TYPE.IMG_SIGNAL_ISO_IN,
                    "iso_out":niimaq_lib.IMG_SIGNAL_TYPE.IMG_SIGNAL_ISO_OUT,
                    "status":niimaq_lib.IMG_SIGNAL_TYPE.IMG_SIGNAL_STATUS,
                    "software":niimaq_lib.IMG_SIGNAL_TYPE.IMG_SIGNAL_SOFTWARE_TRIGGER}
    _p_trig_type=interface.EnumParameterClass("trig_type",_trig_type)
    _trig_action={  "none":niimaq_lib.IMG_TRIG_ACTION.IMG_TRIG_ACTION_NONE,
                    "capture":niimaq_lib.IMG_TRIG_ACTION.IMG_TRIG_ACTION_CAPTURE,
                    "bufflist":niimaq_lib.IMG_TRIG_ACTION.IMG_TRIG_ACTION_BUFLIST,
                    "buffer":niimaq_lib.IMG_TRIG_ACTION.IMG_TRIG_ACTION_BUFFER,
                    "stop":niimaq_lib.IMG_TRIG_ACTION.IMG_TRIG_ACTION_STOP}
    _p_trig_action=interface.EnumParameterClass("trig_action",_trig_action)
    _trig_drive={   "disable":niimaq_lib.IMG_TRIG_DRIVE.IMG_TRIG_DRIVE_DISABLED,
                    "acq_in_progress":niimaq_lib.IMG_TRIG_DRIVE.IMG_TRIG_DRIVE_AQ_IN_PROGRESS,
                    "acq_done":niimaq_lib.IMG_TRIG_DRIVE.IMG_TRIG_DRIVE_AQ_DONE,
                    "unasserted":niimaq_lib.IMG_TRIG_DRIVE.IMG_TRIG_DRIVE_UNASSERTED,
                    "asserted":niimaq_lib.IMG_TRIG_DRIVE.IMG_TRIG_DRIVE_ASSERTED,
                    "hsync":niimaq_lib.IMG_TRIG_DRIVE.IMG_TRIG_DRIVE_HSYNC,
                    "vsync":niimaq_lib.IMG_TRIG_DRIVE.IMG_TRIG_DRIVE_VSYNC,
                    "frame_start":niimaq_lib.IMG_TRIG_DRIVE.IMG_TRIG_DRIVE_FRAME_START,
                    "frame_done":niimaq_lib.IMG_TRIG_DRIVE.IMG_TRIG_DRIVE_FRAME_DONE}
    _p_trig_drive=interface.EnumParameterClass("trig_drive",_trig_drive)
    @interface.use_parameters
    def configure_trigger_in(self, trig_type, trig_line=0, trig_pol="high", trig_action="none", timeout=None, reset_acquisition=True):
        """
        Configure input trigger.

        Args:
            trig_type(str): trigger source type; can be ``"ext"``, ``"rtsi"``, ``"iso_in"``, or ``"software"``
            trig_line(int): trigger line number
            trig_pol(str): trigger polarity; can be ``"high"`` or ``"low"``
            trig_action(str): trigger action; can be ``"none"`` (disable trigger), ``"capture"`` (start capturing), ``"stop"`` (stop capturing),
                ``"buffer"`` (capture a single frame), or ``"bufflist"`` (capture the whole buffer list once)
            timeout(float): timeout in seconds; ``None`` means not timeout.
            reset_acquisition(bool): if the input triggers configuration has been changed, acquisition needs to be restart;
                if ``True``, perform it automatically
        """
        funcargparse.check_parameter_range(self._parameters["trig_type"].i(trig_type),"trig_type",{"ext","rtsi","iso_in","software"})
        timeout=int(timeout*1E3) if timeout is not None else niimaq_lib.IMAQ_INF_TIMEOUT
        lib.imgSessionTriggerConfigure2(self.sid,trig_type,trig_line,trig_pol,timeout,trig_action)
        self._triggers_in[(self._parameters["trig_type"].i(trig_type),trig_line)]=(
                self._parameters["trig_pol"].i(trig_pol),self._parameters["trig_action"].i(trig_action),timeout)
        if reset_acquisition:
            self._reset_acquisition()
    def _get_triggers_in_cfg(self):
        return sorted(list(self._triggers_in.items()))
    def _set_triggers_in_cfg(self, cfg):
        for (tt,tl),(tp,act,to) in cfg:
            self.configure_trigger_in(tt,tl,tp,act,to,reset_acquisition=False)
    def send_software_trigger(self):
        """Send software trigger signal"""
        self.set_grabber_attribute_value("SEND_SOFTWARE_TRIGGER",1)
    @interface.use_parameters
    def configure_trigger_out(self, trig_type, trig_line=0, trig_pol="high", trig_drive="disable"):
        """
        Configure trigger output.

        Args:
            trig_type(str): trigger drive destination type; can be ``"ext"``, ``"rtsi"``, or ``"iso_out"``
            trig_line(int): trigger line number
            trig_pol(str): trigger polarity; can be ``"high"`` or ``"low"``
            trig_drive(str): trigger output signal; can be ``"disable"`` (disable drive),
                ``"acq_in_progress"`` (asserted when acquisition is started), ``"acq_done"`` (asserted when acquisition is done),
                ``"unasserted"`` (force unasserted level), ``"asserted"`` (force asserted level),
                ``"hsync"`` (asserted on start of a single line start), ``"vsync"`` (asserted on start of a frame scan),
                ``"frame_start"`` (asserted when a single frame is captured), or ``"frame_done"`` (asserted when a single frame is done)
        """
        funcargparse.check_parameter_range(self._parameters["trig_type"].i(trig_type),"trig_type",{"ext","rtsi","iso_out"})
        lib.imgSessionTriggerDrive2(self.sid,trig_type,trig_line,trig_pol,trig_drive)
        self._triggers_out[(self._parameters["trig_type"].i(trig_type),trig_line)]=(
                self._parameters["trig_pol"].i(trig_pol),self._parameters["trig_drive"].i(trig_drive))
    def _get_triggers_out_cfg(self):
        return sorted(list(self._triggers_out.items()))
    def _set_triggers_out_cfg(self, cfg):
        for (tt,tl),(tp,td) in cfg:
            self.configure_trigger_out(tt,tl,tp,td)
    @interface.use_parameters
    def read_trigger(self, trig_type, trig_line=0, trig_pol="high"):
        """
        Read current value of a trigger (input or output).

        Args:
            trig_type(str): trigger drive destination type; can be ``"ext"``, ``"rtsi"``, ``"iso_in"``, or ``"iso_out"``
            trig_line(int): trigger line number
            trig_pol(str): trigger polarity; can be ``"high"`` or ``"low"``
        """
        funcargparse.check_parameter_range(self._parameters["trig_type"].i(trig_type),"trig_type",{"ext","rtsi","iso_in","iso_out"})
        return lib.imgSessionTriggerRead2(self.sid,trig_type,trig_line,trig_pol)
    def clear_all_triggers(self, reset_acquisition=True):
        """
        Disable all triggers of the session
        
        If the input triggers configuration has been changed, acquisition needs to be restart; if ``reset_acquisition==True``, perform it automatically.
        """
        lib.imgSessionTriggerClear(self.sid)
        self._triggers_in={}
        self._triggers_out={}
        if reset_acquisition:
            self._reset_acquisition()


    def setup_serial_params(self, write_term="", datatype="bytes"):
        """
        Setup default serial communication parameters.

        Args:
            write_term: default terminator character to be added to the sent messages
            datatype: type of the result of read commands; can be ``"bytes"`` (return raw bytes), or ``"str"`` (convert into UTF-8 string)
        """
        self._serial_term_write=write_term
        self._serial_datatype=datatype
    def get_serial_params(self):
        """Return serial parameters as a tuple ``(write_term, datatype)``"""
        return self._serial_term_write,self._serial_datatype
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
        except IMAQLibError as e:
            if e.code==niimaq_lib.IMG_ERR_CODE.IMG_ERR_SERIAL_WRITE_TIMEOUT:
                raise IMAQTimeoutError from e
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
            msg,_=lib.imgSessionSerialReadBytes(self.sid,n,int(timeout*1000))
            datatype=datatype or self._serial_datatype
            return msg if datatype=="bytes" else py3.as_str(msg)
        except IMAQLibError as e:
            if e.code==niimaq_lib.IMG_ERR_CODE.IMG_ERR_SERIAL_READ_TIMEOUT:
                raise IMAQTimeoutError from e
            else:
                raise
    def serial_readline(self, timeout=3., datatype=None, maxn=1024):
        """
        Read bytes from CameraLink serial port until the termination character (defined in camera file) is encountered.
        
        Args:
            timeout: operation timeout (in seconds)
            datatype: return datatype; can be ``"bytes"`` (return raw bytes), or ``"str"`` (convert into UTF-8 string)
                if ``None``, use the value set up using :meth:`setup_serial_params` (by default, ``"bytes"``)
            maxn: maximal number of bytes to read
        """
        try:
            msg,_=lib.imgSessionSerialRead(self.sid,maxn,int(timeout*1000))
            datatype=datatype or self._serial_datatype
            return msg if datatype=="bytes" else py3.as_str(msg)
        except IMAQLibError as e:
            if e.code==niimaq_lib.IMG_ERR_CODE.IMG_ERR_SERIAL_READ_TIMEOUT:
                raise IMAQTimeoutError from e
            else:
                raise
    def serial_flush(self):
        """Flush CameraLink serial port"""
        lib.imgSessionSerialFlush(self.sid)


    def _get_acquired_frames(self):
        if self._start_acq_count is None:
            return None
        return max(self.get_grabber_attribute_value("FRAME_COUNT",0)-self._start_acq_count,-1)
    def _find_max_nbuff(self):
        frame_size=self._get_buffer_size()
        buff=ctypes.create_string_buffer(frame_size)
        baddr=ctypes.addressof(buff)
        def try_size(n):
            bl=lib.imgCreateBufList(n)
            try:
                lib.imgSetBufferElement2(bl,0,niimaq_lib.IMG_BUFF.IMG_BUFF_SIZE,frame_size)
                lib.imgSetBufferElement2(bl,0,niimaq_lib.IMG_BUFF.IMG_BUFF_ADDRESS,ctypes.c_void_p(baddr))
                lib.imgSetBufferElement2(bl,0,niimaq_lib.IMG_BUFF.IMG_BUFF_COMMAND,niimaq_lib.IMG_CMD.IMG_CMD_NEXT)
                lib.imgSessionConfigure(self.sid,bl)
                return 1
            except IMAQLibError as e:
                if e.code==niimaq_lib.IMG_ERR_CODE.IMG_ERR_TOO_MANY_BUFFERS:
                    return 0
                else:
                    raise
            finally:
                lib.imgDisposeBufList(bl,1)
                lib.imgSessionAbort(self.sid)
        n=1
        while n<2**30:
            if not try_size(n):
                break
            n*=2
        if try_size(n-1):
            n=n-1
        else:
            while not try_size(n):
                n=int(n*0.99)
        return n
        

    @interface.use_parameters(mode="acq_mode")
    def setup_acquisition(self, mode="sequence", nframes=100):  # pylint: disable=arguments-differ
        """
        Setup acquisition mode.

        `mode` can be either ``"snap"`` (single frame or a fixed number of frames) or ``"sequence"`` (continuous acquisition).
        (note that :meth:`.IMAQCamera.acquisition_in_progress` would still return ``True`` in this case, even though new frames are no longer acquired).
        `nframes` sets up number of frame buffers.
        """
        self.clear_acquisition()
        super().setup_acquisition(mode=mode,nframes=nframes)
        if self._max_nbuff is None:
            self._max_nbuff=self._find_max_nbuff()
        nframes=min(nframes,self._max_nbuff)
        self._buffer_mgr.allocate(nframes,self._get_buffer_size())
        cbuffs=self._buffer_mgr.get_ctypes_frames_list(ctype=ctypes.c_char_p)
        self._set_triggers_in_cfg(self._get_triggers_in_cfg()) # reapply trigger settings
        if mode=="sequence":
            lib.imgRingSetup(self.sid,len(cbuffs),cbuffs,0,0)
        else:
            skips=(ctypes.c_uint32*len(cbuffs))(0)
            lib.imgSequenceSetup(self.sid,len(cbuffs),cbuffs,skips,0,0)
        self._start_acq_count=0
    def clear_acquisition(self):
        """Clear all acquisition details and free all buffers"""
        if self._acq_params:
            self.stop_acquisition()
            lib.imgSessionAbort(self.sid)
            self._buffer_mgr.deallocate()
            self._start_acq_count=None
            super().clear_acquisition()
    def _reset_acquisition(self):
        """Clear the acquisition and set it up again with the same parameters"""
        acq_params=self._acq_params
        if acq_params:
            self.clear_acquisition()
            self.setup_acquisition(**acq_params)
    def start_acquisition(self, *args, **kwargs):
        self.stop_acquisition()
        super().start_acquisition(*args,**kwargs)
        self._start_acq_count=self.get_grabber_attribute_value("FRAME_COUNT",0)
        self._frame_counter.reset(self._buffer_mgr.nframes)
        lib.imgSessionStartAcquisition(self.sid)
    def stop_acquisition(self):
        if self.acquisition_in_progress():
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
            lib.imgSessionStopAcquisition(self.sid)
    def acquisition_in_progress(self):
        return bool(lib.imgSessionStatus(self.sid)[0])


    
    def _wait_for_next_frame(self, timeout=20., idx=None):
        if timeout is None or timeout>0.1:
            timeout=0.1
        try:
            lib.imgSessionWaitSignal2(self.sid,
                niimaq_lib.IMG_SIGNAL_TYPE.IMG_SIGNAL_STATUS,niimaq_lib.IMG_INT_SIG.IMG_BUF_COMPLETE,niimaq_lib.IMG_SIGNAL_STATE.IMG_SIGNAL_STATE_RISING,
                int(timeout*1000))
        except IMAQLibError as e:
            if e.code==niimaq_lib.IMG_ERR_CODE.IMG_ERR_TIMEOUT:
                pass
            elif e.code==niimaq_lib.IMG_ERR_CODE.IMG_ERR_BOARD_NOT_RUNNING and not self.acquisition_in_progress():
                pass
            else:
                raise

    
    def _get_buffer_bpp(self):
        return self.get_grabber_attribute_value("BYTESPERPIXEL",1)
    def _get_buffer_dtype(self):
        return "<u{}".format(self._get_buffer_bpp())
    def _get_buffer_size(self):
        bpp=self._get_buffer_bpp()
        roi=self.get_roi()
        w,h=roi[1]-roi[0],roi[3]-roi[2]
        return w*h*bpp
    def _parse_buffer(self, buffer, nframes=1):
        r,c=self._get_data_dimensions_rc()
        dt=self._get_buffer_dtype()
        # bpp=dt.itemsize
        # if len(buffer)!=nframes*r*c*bpp:
        #     raise ValueError("wrong buffer size: expected {}x{}x{}x{}={}, got {}".format(nframes,r,c,bpp,nframes*r*c*bpp,len(buffer)))
        # return np.frombuffer(buffer,dtype=dt).reshape((nframes,r,c))
        cdt=ctypes.POINTER(np.ctypeslib.as_ctypes_type(dt))
        data=np.ctypeslib.as_array(ctypes.cast(buffer,cdt),shape=((nframes,r,c)))
        return data.copy()
    
    _support_chunks=True
    def _read_frames(self, rng, return_info=False):
        raw_frames=self._buffer_mgr.get_frames_data(rng[0],rng[1]-rng[0])
        parsed_frames=[self._convert_indexing(self._parse_buffer(b,nframes=n),"rct",axes=(-2,-1)) for n,b in raw_frames]
        return parsed_frames,None


    def _get_grab_acquisition_parameters(self, nframes, buff_size):
        acq_params=super()._get_grab_acquisition_parameters(nframes,buff_size)
        if acq_params["mode"]=="snap": # sometimes when single mode is used, the frame grabber only acquires half of the buffer frames
            acq_params["nframes"]*=2
        return acq_params






class IMAQCamera(IMAQFrameGrabber):
    """
    Generic IMAQ camera interface.

    Args:
        name: interface name (can be learned by :func:`list_cameras`; usually, but not always, starts with ``"cam"`` or ``"img"``)
    """
    def __init__(self, name="img0"):
        super().__init__(imaq_name=name)