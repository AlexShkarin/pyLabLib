from ...core.devio import interface, comm_backend
from ...core.dataproc import image as image_utils
from ...core.utils import functions as function_utils, general as general_utils, dictionary

import numpy as np
import collections
import contextlib
import time
import functools
import threading



class DefaultFrameTransferError(comm_backend.DeviceError):
    """Generic frame transfer error"""

TFramesStatus=collections.namedtuple("TFramesStatus",["acquired","unread","skipped","buffer_size"])
TFrameSize=collections.namedtuple("TFrameSize",["width","height"])
TFramePosition=collections.namedtuple("TFramePosition",["left","top"])
TFrameInfo=collections.namedtuple("TFrameInfo",["frame_index"])
class ICamera(interface.IDevice):
    """
    Generic camera class.

    Provides a consistent common interface for the most frequently encountered camera functions.
    """
    _default_image_indexing="rct"
    _default_frameinfo_format="namedtuple"
    _default_image_dtype="<u2"
    _clear_pausing_acquisition=False
    Error=comm_backend.DeviceError
    TimeoutError=comm_backend.DeviceError
    FrameTransferError=DefaultFrameTransferError
    def __init__(self):
        super().__init__()
        self._acq_params=None
        self._default_acq_params=function_utils.funcsig(self.setup_acquisition).defaults
        self._frame_counter=FrameCounter()
        self._image_indexing=self._default_image_indexing
        self._frameinfo_format=self._default_frameinfo_format
        self._add_status_variable("buffer_size",lambda: self.get_frames_status().buffer_size)
        self._add_status_variable("acquired_frames",lambda: self.get_frames_status().acquired)
        self._add_status_variable("acquisition_in_progress",self.acquisition_in_progress)
        self._add_status_variable("frames_status",self.get_frames_status)
        self._add_status_variable("data_dimensions",self.get_data_dimensions)
        self._add_info_variable("detector_size",self.get_detector_size)
        self._add_settings_variable("image_indexing",self.get_image_indexing,self.set_image_indexing)
        self._add_settings_variable("frame_info_format",self.get_frame_info_format,self.set_frame_info_format)


    ### Acquisition control ###
    def is_acquisition_setup(self):
        """
        Check if acquisition is set up.

        If the camera does not support separate acquisition setup, always return ``True``.
        """
        return self._acq_params is not None
    def get_acquisition_parameters(self):
        """
        Get acquisition parameters.

        Return dictionary ``{name: value}``
        """
        return self._acq_params.copy() if self._acq_params is not None else None
    def _get_updated_acquisition_parameters(self, *args, **kwargs):
        """
        Check how the currently set up acquisition parameters should be updated with the new ones.
        
        Return tuple ``(updated, full)``, where ``updated`` is a dictionary of parameters which are different from the ones set up,
        and ``full`` is the full dictionary of acquisition parameters after applying.
        """
        kwargs=function_utils.funcsig(self.setup_acquisition).as_kwargs(args,kwargs,add_defaults=False)
        if self._acq_params is None:
            full=self._default_acq_params.copy()
            full.update(kwargs)
            return full,full
        else:
            full=self._acq_params.copy()
            updated={}
            for k,v in kwargs.items():
                if (k not in full) or (full[k]!=v):
                    updated[k]=v
            full.update(updated)
            return updated,full
    def _ensure_acquisition_parameters(self, *args, **kwargs):
        """Update acquisition parameters if needed, and return the full currently parameters"""
        updated_acq_params,full_acq_params=self._get_updated_acquisition_parameters(*args,**kwargs)
        if updated_acq_params:
            self.setup_acquisition(**full_acq_params)
        return full_acq_params
    
    _p_acq_mode=interface.EnumParameterClass("acq_mode",["sequence","snap"])
    def setup_acquisition(self, **kwargs):
        """
        Setup acquisition.
        
        Any non-specified acquisition parameters are assumed to be the same as previously set (or default, if not explicitly set before).
        Return the new acquisition parameters.
        """
        if self._acq_params is None:
            self._acq_params=self._default_acq_params.copy()
        self._acq_params.update(kwargs)
        return self._acq_params
    def clear_acquisition(self):
        """Clear acquisition settings"""
        self._frame_counter.reset()
        self._acq_params=None
    def start_acquisition(self, *args, **kwargs):
        """
        Start acquisition.
        
        Can take the same keyword parameters as `:meth:``setup_acquisition`.
        If the acquisition is not set up yet, set it up using the supplied parameters (use default of :meth:`setup_acquisition`,if the parameter is ``None``).
        Otherwise, if any supplied parameters are different from the current ones, change them and reset the acquisition.
        """
        self._ensure_acquisition_parameters(*args,**kwargs)
    def stop_acquisition(self):
        """Stop acquisition"""
    def acquisition_in_progress(self):
        """Check if acquisition is in progress"""
        raise NotImplementedError("ICamera.acquisition_in_progress")

    @contextlib.contextmanager
    def pausing_acquisition(self, clear=None):
        """
        Context manager which temporarily pauses acquisition during execution of ``with`` block.

        Useful for applying certain settings which can't be changed during the acquisition.
        If ``clear==True``, clear acquisition in addition to pausing (by default, use the class default specified as ``_clear_pausing_acquisition`` attribute).
        Yields tuple ``(acq_in_progress, acq_params)``, which indicates whether acquisition is currently in progress, and what are the current acquisition parameters.
        """
        if clear is None:
            clear=self._clear_pausing_acquisition
        acq_in_progress=self.acquisition_in_progress()
        acq_params=self.get_acquisition_parameters()
        self.stop_acquisition()
        if clear:
            self.clear_acquisition()
        try:
            yield acq_in_progress, acq_params
        finally:
            if clear and acq_params is not None and self.get_acquisition_parameters() is None:
                self.setup_acquisition(**acq_params)
            if acq_in_progress and not self.acquisition_in_progress():
                start_params=acq_params if self.get_acquisition_parameters() is None else {}
                self.start_acquisition(**start_params)

    ### Camera info ###
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        raise NotImplementedError("ICamera.get_detector_size")


    ### Buffer status ###
    def _get_acquired_frames(self):
        """Return number of acquired frames; can also return ``None`` if the acquisition is not set up"""
        raise NotImplementedError("ICamera._get_acquired_frames")
    _TFramesStatus=TFramesStatus
    def get_frames_status(self):
        """
        Get acquisition and buffer status.

        Return tuple ``(acquired, unread, skipped, size)``, where ``acquired`` is the total number of acquired frames,
        ``unread`` is the number of acquired but not read frames, ``skipped`` is the number of skipped (not read and then written over) frames,
        and ``buffer_size`` is the total buffer size (in frames).
        """
        if self.acquisition_in_progress():
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
        return TFramesStatus(*self._frame_counter.get_frames_status())

    ### Frame waiting ###
    _p_frame_wait_mode=interface.EnumParameterClass("frame_wait_mode",["lastread","lastwait","now","start"])
    _wait_sleep_period=1E-3
    def _wait_for_next_frame(self, timeout=20., idx=None):  # pylint: disable=unused-argument
        """
        Wait for a single frame with the given index for a given amount of time.
        
        If timeout is reached, raise ``TimeoutError`` or simply return.
        Can also return without a next frame acquired (but should still wait for a small amount of time to avoid high CPU load).
        """
        sleep_time=min(self._wait_sleep_period,timeout) if timeout is not None else self._wait_sleep_period
        time.sleep(sleep_time)
    @interface.use_parameters(since="frame_wait_mode")
    def wait_for_frame(self, since="lastread", nframes=1, timeout=20., error_on_stopped=False):
        """
        Wait for one or several new camera frames.

        `since` specifies the reference point for waiting to acquire `nframes` frames;
        can be "lastread"`` (from the last read frame), ``"lastwait"`` (wait for the last successful :meth:`wait_for_frame` call),
        ``"now"`` (from the start of the current call), or ``"start"`` (from the acquisition start, i.e., wait until `nframes` frames have been acquired).
        `timeout` can be either a number, ``None`` (infinite timeout), or a tuple ``(timeout, frame_timeout)``,
        in which case the call times out if the total time exceeds ``timeout``, or a single frame wait exceeds ``frame_timeout``.
        If the call times out, raise ``TimeoutError``.
        If ``error_on_stopped==True`` and the acquisition is not running, raise ``Error``;
        otherwise, simply return ``False`` without waiting.
        """
        wait_started=False
        if isinstance(timeout,tuple):
            timeout,frame_timeout=timeout
        else:
            frame_timeout=None
        ctd=general_utils.Countdown(timeout)
        frame_ctd=general_utils.Countdown(frame_timeout)
        if not self.acquisition_in_progress():
            if error_on_stopped:
                raise self.Error("waiting for a frame while acquisition is stopped")
            else:
                return False
        last_acquired_frames=None
        while True:
            acquired_frames=self._get_acquired_frames()
            if acquired_frames is None:
                if error_on_stopped:
                    raise self.Error("waiting for a frame while acquisition is stopped")
                else:
                    return False
            if acquired_frames!=last_acquired_frames:
                frame_ctd.reset()
            last_acquired_frames=acquired_frames
            if not wait_started:
                self._frame_counter.wait_start(acquired_frames)
                wait_started=True
            if self._frame_counter.is_wait_done(acquired_frames,since=since,nframes=nframes):
                break
            to,fto=ctd.time_left(),frame_ctd.time_left()
            if fto is not None:
                to=fto if to is None else min(to,fto)
            if to is not None and to<=0:
                raise self.TimeoutError
            self._wait_for_next_frame(timeout=to,idx=acquired_frames)
        self._frame_counter.wait_done()
        return True


    ### Frames indexing and readout ###
    def get_image_indexing(self):
        """
        Get indexing for the returned images.

        Can be ``"rct"`` (first index row, second index column, rows counted from the top), ``"rcb"`` (same as ``"rc"``, rows counted from the bottom),
        ``"xyt"`` (first index column, second index row, rows counted from the top), or ``"xyb"`` (same as ``"xyt"``, rows counted from the bottom)
        """
        return self._image_indexing
    _p_indexing=interface.EnumParameterClass("frame_indexing",["rct","rcb","xyt","xyb"])
    @interface.use_parameters(indexing="frame_indexing")
    def set_image_indexing(self, indexing):
        """
        Set up indexing for the returned images.

        Can be ``"rct"`` (first index row, second index column, rows counted from the top), ``"rcb"`` (same as ``"rc"``, rows counted from the bottom),
        ``"xyt"`` (first index column, second index row, rows counted from the top), or ``"xyb"`` (same as ``"xyt"``, rows counted from the bottom)
        """
        self._image_indexing=indexing
        return self._image_indexing
    def _convert_indexing(self, data, src_indexing, axes=(0,1)):
        """Convert data from the given source indexing to the camera indexing"""
        if src_indexing==self._image_indexing or data is None:
            return data
        if isinstance(data,list):
            return [self._convert_indexing(d,src_indexing,axes=axes) for d in data]
        return image_utils.convert_image_indexing(data,src_indexing,self._image_indexing,axes=axes)
    def _get_data_dimensions_rc(self):
        raise NotImplementedError("ICamera._get_data_dimensions_rc")
    def get_data_dimensions(self):
        """Get readout data dimensions (in pixels) as a tuple ``(width, height)``; take indexing mode into account"""
        return image_utils.convert_shape_indexing(self._get_data_dimensions_rc(),"rc",self._image_indexing)
    
    def get_frame_info_format(self):
        """
        Get format of the frame info.

        Can be ``"namedtuple"`` (potentially nested named tuples; convenient to get particular values),
        ``"list"`` (flat list of values, with field names are given by :meth:`get_frame_info_fields`; convenient for building a table),
        or ``"dict"`` (flat dictionary with the same fields as the ``"list"`` format; more resilient to future format changes)
        """
        return self._frameinfo_format
    _p_frameinfo_format=interface.EnumParameterClass("frame_info_format",["namedtuple","list","dict"])
    @interface.use_parameters(fmt="frame_info_format")
    def set_frame_info_format(self, fmt):
        """
        Set format of the frame info.

        Can be ``"namedtuple"`` (potentially nested named tuples; convenient to get particular values),
        ``"list"`` (flat list of values, with field names are given by :meth:`get_frame_info_fields`; convenient for building a table),
        or ``"dict"`` (flat dictionary with the same fields as the ``"list"`` format; more resilient to future format changes)
        """
        self._frameinfo_format=fmt
        return self._frameinfo_format
    def get_frame_info_fields(self):
        """
        Get the names of frame info fields.

        Applicable when frame info format (set by :meth:`set_frame_info_format`) is ``"list"``.
        """
        return list(self._frameinfo_fields)
    def _convert_frame_info(self, info, fmt=None):
        if info is None:
            return None
        if fmt is None:
            fmt=self._frameinfo_format
        if fmt=="namedtuple":
            return info
        if fmt=="list":
            return list(general_utils.flatten_list(info))
        return dict(zip(self._frameinfo_fields,general_utils.flatten_list(info)))

    def get_new_images_range(self):
        """
        Get the range of the new images.
        
        Return tuple ``(first, last)`` with images range (first inclusive).
        If no images are available, return ``None``.
        If some images were in the buffer were overwritten, exclude them from the range.
        """
        acquired_frames=self._get_acquired_frames()
        if acquired_frames is None:
            return None
        rng=self._frame_counter.get_new_frames_range(acquired_frames)
        return rng if (rng and rng[1]>rng[0]) else None
    def _trim_images_range(self, rng):
        """
        Trim the given frame range to lie within the buffer.

        If acquisition is stopped, return ``None``. If not frames are within this range, return a 0-length range ``(last_frame,last_frame)``.
        If ``rng is None``, return the new images range.
        """
        acquired_frames=self._get_acquired_frames()
        if acquired_frames is None:
            return None
        self._frame_counter.update_acquired_frames(acquired_frames)
        if rng is None:
            return self._frame_counter.get_new_frames_range(),0
        else:
            return self._frame_counter.trim_frames_range(rng)
    def _read_frames(self, rng, return_info=False):  # pylint: disable=unused-argument
        """
        Read and return frames given the range.
        
        The range is always a tuple with at least a single frame in it, and is guaranteed to already be valid.
        Always return tuple ``(frames, infos)``; if ``return_info==False``, ``infos`` value is ignored, so it can be anything (e.g., ``None``).
        """
        return [],[]
    def _zero_frame(self, n):
        """Return `n` zero frames (as a list or 3D numpy array) for padding the :meth:`read_multiple_images` output when ``missing_frame=="zero"``"""
        return np.zeros((n,)+self.get_data_dimensions(),dtype=self._default_image_dtype)
    _TFrameInfo=TFrameInfo
    _frameinfo_fields=TFrameInfo._fields
    _p_missing_frame=interface.EnumParameterClass("missing_frame",["none","zero","skip"])
    @interface.use_parameters
    def read_multiple_images(self, rng=None, peek=False, missing_frame="skip", return_info=False):
        """
        Read multiple images specified by `rng` (by default, all un-read images).

        If `rng` is specified, it is a tuple ``(first, last)`` with images range (first inclusive).
        If no new frames are available, return an empty list; if no acquisition is running, return ``None``.
        If ``peek==True``, return images but not mark them as read.
        `missing_frame` determines what to do with frames which are out of range (missing or lost):
        can be ``"none"`` (replacing them with ``None``), ``"zero"`` (replacing them with zero-filled frame), or ``"skip"`` (skipping them).
        If ``return_info==True``, return tuple ``(frames, infos)``, where ``infos`` is a list of frame info tuples (camera-dependent, by default, only the frame index);
        if some frames are missing and ``missing_frame!="skip"``, the corresponding frame info is ``None``.
        """
        rng,skipped_frames=self._trim_images_range(rng)
        if rng is None:
            return (None,None) if return_info else None
        images,info=self._read_frames(rng,return_info=return_info)
        if skipped_frames and missing_frame!="skip":
            if missing_frame=="zero":
                images=list(self._zero_frame(skipped_frames))+images
            else:
                images=[None]*skipped_frames+images
            if return_info:
                info=[None]*skipped_frames+info
        if not peek:
            self._frame_counter.advance_read_frames(rng)
        return (images,info) if return_info else images
    def read_oldest_image(self, peek=False, return_info=False):
        """
        Read the oldest un-read image.

        If no un-read frames are available, return ``None``.
        If ``peek==True``, return the image but not mark it as read.
        If ``return_info==True``, return tuple ``(frame, info)``, where ``info`` is an info tuples (camera-dependent, see :meth:`read_multiple_images`).
        """
        rng=self.get_new_images_range()
        if rng is None or rng[0]==rng[1]:
            return None
        res=self.read_multiple_images(rng=(rng[0],rng[0]+1),peek=peek,return_info=return_info)
        frame,info=res if return_info else (res,[None])
        if frame:
            return (frame[0],info[0]) if return_info else frame[0]
        else:
            return None
    def read_newest_image(self, peek=False, return_info=False):
        """
        Read the newest un-read image.

        If no un-read frames are available, return ``None``.
        If ``peek==True``, return the image but not mark it as read.
        If ``return_info==True``, return tuple ``(frame, info)``, where ``info`` is an info tuples (camera-dependent, see :meth:`read_multiple_images`).
        """
        rng=self.get_new_images_range()
        if rng is None or rng[0]==rng[1]:
            return None
        res=self.read_multiple_images(rng=(rng[1]-1,rng[1]),peek=peek,return_info=return_info)
        frame,info=res if return_info else (res,[None])
        if frame:
            return (frame[0],info[0]) if return_info else frame[0]
        else:
            return None


    ### Combined functions ###
    def _get_grab_acquisition_parameters(self, nframes, buff_size):
        if buff_size is None:
            buff_size=self._default_acq_params.get("nframes",100)
        if nframes<=buff_size:
            return {"nframes":nframes,"mode":"snap"}
        else:
            return {"nframes":buff_size,"mode":"sequence"}
    def grab(self, nframes=1, frame_timeout=5., missing_frame="none", return_info=False, buff_size=None):
        """
        Snap `nframes` images (with preset image read mode parameters)
        
        `buff_size` determines buffer size (if ``None``, use the default size).
        Timeout is specified for a single-frame acquisition, not for the whole acquisition time.
        `missing_frame` determines what to do with frames which have been lost:
        can be ``"none"`` (replacing them with ``None``), ``"zero"`` (replacing them with zero-filled frame),
        or ``"skip"`` (skipping them, while still keeping total returned frames number to `n`).
        If ``return_info==True``, return tuple ``(frames, infos)``, where ``infos`` is a list of frame info tuples (camera-dependent);
        if some frames are missing and ``missing_frame!="skip"``, the corresponding frame info is ``None``.
        """
        acq_params=self._get_grab_acquisition_parameters(nframes,buff_size)
        frames,info=[],[]
        self.start_acquisition(**acq_params)
        try:
            while len(frames)<nframes:
                self.wait_for_frame(timeout=frame_timeout)
                if return_info:
                    new_frames,new_info=self.read_multiple_images(missing_frame=missing_frame,return_info=True)
                    frames+=new_frames
                    info+=new_info
                else:
                    frames+=self.read_multiple_images(missing_frame=missing_frame,return_info=False)
            return (frames[:nframes],info[:nframes]) if return_info else frames[:nframes]
        finally:
            self.stop_acquisition()
    def snap(self, timeout=5., return_info=False):
        """Snap a single frame"""
        res=self.grab(frame_timeout=timeout,return_info=return_info)
        if return_info:
            return res[0][0],res[1][0]
        else:
            return res[0]



def acqstopped(*args, **kwargs):
    """Decorator which temporarily stops acquisition for the function call"""
    if len(args)>0:
        return acqstopped(**kwargs)(args[0])
    error=kwargs.get("error",False)
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):
            if error and self.acquisition_in_progress():
                raise self.Error("method {} can not be called when the acquisition is in progress".format(func.__name__))
            with self.pausing_acquisition(clear=False):
                return func(self,*args,**kwargs)
        return wrapped
    return wrapper
def acqcleared(*args, **kwargs):
    """Decorator which temporarily clears acquisition for the function call"""
    if len(args)>0:
        return acqcleared(**kwargs)(args[0])
    error=kwargs.get("error",False)
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):
            if error and self.is_acquisition_setup() is not None:
                raise self.Error("method {} can not be called when the acquisition is set up".format(func.__name__))
            with self.pausing_acquisition(clear=True):
                return func(self,*args,**kwargs)
        return wrapped
    return wrapper





class FrameCounter:
    """
    Frame counter.

    Keeps track of the buffer occupation, acquired/missed frames, last read and wait buffers, etc.
    """
    def __init__(self):
        self.reset()
    
    def reset(self, buffer_size=None):
        """
        Reset the counters.

        If ``buffer_size is None``, assume the the buffer is deallocated.
        Otherwise, it specifies the frame buffer size (in frames).
        """
        self.buffer_size=buffer_size
        self.wait_start_frame=None
        self.last_acquired_frame=-1
        self.last_wait_frame=-1
        self.last_read_frame=-1
        self.first_valid_frame=-1
        self.skipped_frames=0
    def update_acquired_frames(self, acquired_frames):
        """Update the counter of acquired frames (needs to be called by the camera whenever necessary)"""
        if self.buffer_size is None:
            return
        if acquired_frames is not None:
            self.last_acquired_frame=acquired_frames-1

    def wait_start(self, acquired_frames):
        """Set up waiting routine (called in the beginning of :meth:`ICamera.wait_for_frame`)"""
        if self.buffer_size is None:
            return
        self.update_acquired_frames(acquired_frames)
        self.wait_start_frame=self.last_acquired_frame
    def is_wait_done(self, acquired_frames=None, since="lastread", nframes=1):
        """
        Check if the waiting condition is satisfied based on the counter values:

        If not ``None``, `acquired_frames` specifies the most recent number of acquired frames (the internal counters is automatically updated).
        `since` and `nframes` have the same meaning as in :meth:`ICamera.wait_for_frame`.
        """
        if self.buffer_size is None:
            return True
        self.update_acquired_frames(acquired_frames)
        if since=="lastread" and self.last_acquired_frame>=self.last_read_frame+nframes:
            return True
        if since=="lastwait" and self.last_acquired_frame>=self.last_wait_frame+nframes:
            return True
        if since=="now" and self.last_acquired_frame>=self.wait_start_frame+nframes:
            return True
        if since=="start" and self.last_acquired_frame>=nframes-1:
            return True
        return False
    def wait_done(self):
        """Clean up waiting routine (called in the end of :meth:`ICamera.wait_for_frame`)"""
        if self.buffer_size is None:
            return
        self.last_wait_frame=self.last_acquired_frame
        self.wait_start_frame=None

    def get_frames_status(self, acquired_frames=None):
        """
        Get status of the internal counters.

        Return tuple ``(acquired, unread, skipped, buffer_size)``.
        If the buffer is not allocated, all counters are 0.
        """
        if self.buffer_size is None:
            return (0,0,0,0)
        self.update_acquired_frames(acquired_frames)
        full_unread=self.last_acquired_frame-self.last_read_frame
        valid_chunk=max(0,min(self.buffer_size,self.last_acquired_frame-self.first_valid_frame))
        unread=min(full_unread,valid_chunk)
        skipped=self.skipped_frames+(full_unread-unread)
        return (self.last_acquired_frame+1,unread,skipped,self.buffer_size)

    def get_new_frames_range(self, acquired_frames=None):
        """Get the range of the new frames (acquired but not read)"""
        if self.buffer_size is None:
            return None
        self.update_acquired_frames(acquired_frames)
        return self.trim_frames_range((self.last_read_frame+1,self.last_acquired_frame+1))[0]
    def trim_frames_range(self, rng):
        """Trim the given frames range to only contains frames which are still in the buffer (i.e., remove the frames which are too old and have been overwritten)"""
        if self.buffer_size is None:
            return None
        rng=list(rng)
        acquired_frames=self.last_acquired_frame+1
        if rng[0] is None:
            rng[0]=self.last_read_frame+1
        elif rng[0]<0:
            rng[0]+=acquired_frames
        if rng[1] is None:
            rng[1]=acquired_frames
        elif rng[1]<0:
            rng[1]+=acquired_frames
        rng[0]=min(rng[0],acquired_frames)
        rng[1]=min(rng[1],acquired_frames)
        if rng[1]<=rng[0]:
            rng=rng[0],rng[0]
        oldest_valid_frame=max(self.first_valid_frame,self.last_acquired_frame-self.buffer_size+1)
        if rng[1]<=oldest_valid_frame:
            return (oldest_valid_frame,oldest_valid_frame),rng[1]-rng[0]
        else:
            start=max(rng[0],oldest_valid_frame)
            return (start,rng[1]),start-rng[0]
    def advance_read_frames(self, rng):
        """Mark the specified frames range as read and advance the last read counter"""
        if self.buffer_size is None:
            return
        self.skipped_frames+=max(rng[0]-1-self.last_read_frame,0)
        self.last_read_frame=max(self.last_read_frame,rng[1]-1)
    def set_first_valid_frame(self, first_valid_frame):
        """Set the first valid frame; all frames older than it are considered invalid when calculating skipped frames and trimming ranges"""
        if self.buffer_size is not None:
            self.first_valid_frame=first_valid_frame




class FrameNotifier:
    """
    Notifier for a new available frame.

    Used when the camera runs a separate polling thread or a callback, which needs to notify the main thread that a new frame has been acquired.

    Args:
        strict: determines whether :meth:`wait` waits for a specified frame index, or just for any new frame (which is checked later)
    """
    def __init__(self, strict=False):
        self.cond=threading.Condition()
        self.counter=0
        self.strict=strict
    def reset(self):
        """Reset the internal frame counter"""
        with self.cond:
            self.counter=0
            self.cond.notify_all()
    def inc(self):
        """Increment the internal frame counter, notify the waiting threads, and return the counter value"""
        with self.cond:
            self.counter+=1
            self.cond.notify_all()
            return self.counter
    def wait(self, idx=None, timeout=None):
        """Wait for a new frame with a given index (if ``None``, for the next acquired frame)"""
        ctd=general_utils.Countdown(timeout)
        while True:
            with self.cond:
                if idx is None:
                    idx=self.counter+1
                if self.counter>idx:
                    return
                self.cond.wait(ctd.time_left())
            if not self.strict:
                return






class IAttributeCamera(ICamera):
    """
    Camera class which supports camera attributes.

    The method ``_list_attributes`` must be defined in a subclass;
    it should produce a list of camera attributes, which have ``name`` attribute for placing them into a dictionary.
    Attributes can also have ``readable`` and ``writable`` attributes, which are used in
    :meth:`get_all_attribute_values` and :meth:`set_all_attribute_values` to determine if the attribute values should be collected or set.
    Method ``_update_attributes`` should be called on opening to populate the dictionary of available attributes.

    One can also define ``_normalize_attribute_name``, which normalizes the attribute name into a dictionary name
    (e.g., replaces separators, removes spaces, or normalizes case).
    """
    def __init__(self):
        super().__init__()
        self.attributes=dictionary.Dictionary()
        self._add_status_variable("camera_attributes",self.get_all_attribute_values,priority=-5)
        self.ca=dictionary.ItemAccessor(self.get_attribute,missing_error=self.Error)
        self.cav=dictionary.ItemAccessor(self.get_attribute_value,self.set_attribute_value,missing_error=self.Error)
    
    def _normalize_attribute_name(self, name):
        return name
    def _list_attributes(self):
        raise NotImplementedError("IAttributeCamera._list_attributes")
    def _update_attributes(self, replace=False):
        """Update ``attributes`` dictionary; if ``replace==True``, replace it entirely, otherwise, simply update it"""
        attrs=self._list_attributes()
        attrs_dict=dictionary.Dictionary({self._normalize_attribute_name(p.name):p for p in attrs})
        if replace:
            self.attributes=attrs_dict
        else:
            self.attributes.update(attrs_dict)
    def get_attribute(self, name, error_on_missing=True):
        """Get the camera attribute with the given name"""
        name=self._normalize_attribute_name(name)
        if name in self.attributes:
            return self.attributes[name]
        if error_on_missing:
            raise self.Error("attribute {} is missing".format(name))
    def get_all_attributes(self, copy=False):
        """
        Return a dictionary of all available attributes.
        
        If ``copy==True``, copy the dictionary; otherwise, return the internal dictionary structure (should not be modified).
        """
        return self.attributes.copy() if copy else self.attributes

    def get_attribute_value(self, name, error_on_missing=True, default=None, **kwargs):
        """
        Get value of an attribute with the given name.
        
        If the value doesn't exist and ``error_on_missing==True``, raise error; otherwise, return `default`.
        If `default` is not ``None``, automatically assume that ``error_on_missing==False``.
        If `name` points at a dictionary branch, return a dictionary with all values in this branch.
        Additional arguments are passed to ``get_value`` methods of the individual attribute.
        """
        error_on_missing=error_on_missing and (default is None)
        attr=self.get_attribute(name,error_on_missing=error_on_missing)
        if dictionary.is_dictionary(attr):
            return self.get_all_attribute_values(root=name,**kwargs)
        return default if attr is None else attr.get_value(**kwargs)
    def set_attribute_value(self, name, value, error_on_missing=True, **kwargs):
        """
        Set value of an attribute with the given name.
        
        If the value doesn't exist and ``error_on_missing==True``, raise error; otherwise, do nothing.
        If `name` points at a dictionary branch, set all values in this branch (in this case `value` must be a dictionary).
        Additional arguments are passed to ``set_value`` methods of the individual attribute.
        """
        attr=self.get_attribute(name,error_on_missing=error_on_missing)
        if dictionary.is_dictionary(attr):
            return self.set_all_attribute_values(value,root=name,**kwargs)
        if attr is not None:
            attr.set_value(value,**kwargs)
    
    def get_all_attribute_values(self, root="", **kwargs):
        """
        Get values of all attributes with the given `root`.

        Additional arguments are passed to ``get_value`` methods of individual attributes.
        """
        attributes=self.get_attribute(root)
        return attributes.copy().filter_self(lambda a: getattr(a,"readable",True)).map_self(lambda a: a.get_value(**kwargs))
    def set_all_attribute_values(self, settings, root="", **kwargs):
        """
        Set values of all attributes with the given `root`.

        Additional arguments are passed to ``set_value`` methods of individual attributes.
        """
        attributes=self.get_attribute(root)
        settings=dictionary.as_dict(settings,style="flat",copy=False)
        for k,v in settings.items():
            k=self._normalize_attribute_name(k)
            if k in attributes and getattr(attributes[k],"writable",True):
                attributes[k].set_value(v,**kwargs)





TAcqTimings=collections.namedtuple("TAcqTimings",["exposure","frame_period"])
class IExposureCamera(ICamera):
    def __init__(self):
        super().__init__()
        self._add_settings_variable("exposure",self.get_exposure,self.set_exposure)
        self._add_status_variable("frame_timings",self.get_frame_timings)
    def get_exposure(self):
        """Get current exposure"""
        return self.get_frame_timings().exposure
    def set_exposure(self, exposure):
        """Set camera exposure"""
        raise NotImplementedError("ICamera.set_exposure")
    def get_frame_period(self):
        """Get frame period (time between two consecutive frames in the internal trigger mode)"""
        return self.get_frame_timings().frame_period
    _TAcqTimings=TAcqTimings
    def get_frame_timings(self):
        """
        Get acquisition timing.

        Return tuple ``(exposure, frame_period)``.
        """
        raise NotImplementedError("ICamera.get_frame_timings")





TAxisROILimit=collections.namedtuple("TAxisROILimit",["min","max","pstep","sstep","maxbin"])
def _validate_roi_limit(lim, symmetric=False):
    smin,smax,sstep,pstep,_=lim
    if smin%pstep:
        raise ValueError("minimal size {} should be divisible by pstep {}".format(smin,pstep))
    if smin%sstep:
        raise ValueError("minimal size {} should be divisible by sstep {}".format(smin,sstep))
    if (pstep%sstep) and (sstep%pstep):
        raise ValueError("pstep {} should be divisible by sstep {} or vice versa".format(pstep,sstep))
    if symmetric and smax%2:
        raise ValueError("maximal size {} should be even for symmetric ROI".format(smax))
    if symmetric and smax%pstep:
        raise ValueError("maximal size {} should be divisible by pstep {} in symmetric mode".format(smax,pstep))
    if symmetric and smax%sstep:
        raise ValueError("maximal size {} should be divisible by sstep {} in symmetric mode".format(smax,sstep))
def truncate_roi_axis(roi, lim, symmetric=False):
    """
    Truncate ROI to conform to the given ROI limits.
    
    `roi` is a tuple ``(start, stop, bin)``,
    and `lim` is a tuple ``(min, max, pstep, sstep, maxbin)``.
    Assume that ``pstep`` and ``sstep`` divide ``min`` and ``max``,
    and that either ``pstep`` divides ``sstep`` or the other way around.
    If ``symmetric==True``, then ``max`` should be even.
    """
    smin,smax,pstep,sstep,maxbin=lim
    _validate_roi_limit(lim,symmetric=symmetric)
    start,end,cbin=roi
    cbin=max(1,min(cbin,maxbin))
    if end is None:
        end=smax
    end=min(end,smax)
    start=max(0,start)
    start-=start%pstep
    end-=end%pstep
    end-=(end-start)%sstep
    if end-start<smin:
        end=start+smin
    if end>smax:
        start=smax-smin
        start-=start%pstep
        end=start+smin
    if symmetric:
        smin=smin*2 if smin%2 else smin
        sstep=sstep*2 if sstep%2 else sstep
        ds,de=start,smax-end
        if ds!=de:
            d=min(ds,de)
            start=d
            start-=start%pstep
            mid=smax//2
            if (mid-start)%(sstep//2):
                start+=(mid-start)%(sstep//2)-(sstep//2)
            end=smax-start
    return (start,end,cbin)
class IROICamera(ICamera):
    def __init__(self):
        super().__init__()
        self._add_settings_variable("roi",self.get_roi,self.set_roi)
        self._add_status_variable("roi_limits",self.get_roi_limits)
    def get_roi(self):
        """
        Get current ROI.

        Return tuple ``(hstart, hend, vstart, vend)``.
        `hstart` and `hend` specify horizontal image extent, `vstart` and `vend` specify vertical image extent
        (start is inclusive, stop is exclusive, starting from 0).
        """
        w,h=self.get_detector_size()
        return (0,w,0,h)
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None):
        """
        Setup camera ROI.

        `hstart` and `hend` specify horizontal image extent, `vstart` and `vend` specify vertical image extent
        (start is inclusive, stop is exclusive, starting from 0).
        By default, all non-supplied parameters take extreme values (0 for start, maximal for end).
        """
        raise NotImplementedError("ICamera.set_roi")
    def _truncate_roi_axis(self, roi, lim, symmetric=False):
        """Truncate ROI ``(start, end)`` to conform to `lim`"""
        return truncate_roi_axis(roi,lim+(1,),symmetric=symmetric)[:2]
    def get_roi_limits(self, hbin=1, vbin=1):  # pylint: disable=unused-argument
        """
        Get the minimal and maximal ROI parameters.

        Return tuple ``(hlim, vlim)``, where each element is in turn a limit 5-tuple
        ``(min, max, pstep, sstep, maxbin)`` with, correspondingly, minimal and maximal size,
        position and size step, and the maximal binning (fixed to 1 if not binning is allowed).
        In some cameras, the step and the minimal size depend on the binning, which can be supplied.
        """
        w,h=self.get_detector_size()
        return TAxisROILimit(w,w,w,w,1),TAxisROILimit(h,h,h,h,1)


class IBinROICamera(ICamera):
    def __init__(self):
        super().__init__()
        self._add_settings_variable("roi",self.get_roi,self.set_roi)
        self._add_status_variable("roi_limits",self.get_roi_limits)
    def get_roi(self):
        """
        Get current ROI.

        Return tuple ``(hstart, hend, vstart, vend, hbin, vbin)``.
        `hstart` and `hend` specify horizontal image extent, `vstart` and `vend` specify vertical image extent
        (start is inclusive, stop is exclusive, starting from 0), `hbin` and `vbin` specify binning.
        """
        w,h=self.get_detector_size()
        return (0,w,0,h,1,1)
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        """
        Setup camera ROI.

        `hstart` and `hend` specify horizontal image extent, `vstart` and `vend` specify vertical image extent
        (start is inclusive, stop is exclusive, starting from 0), `hbin` and `vbin` specify binning.
        By default, all non-supplied parameters take extreme values (0 for start, maximal for end, 1 for binning).
        """
        raise NotImplementedError("ICamera.set_roi")
    def _truncate_roi_axis(self, roi, lim, symmetric=False):
        """Truncate ROI ``(start, end, bin)`` to conform to `lim`"""
        return truncate_roi_axis(roi,lim,symmetric=symmetric)
    def get_roi_limits(self, hbin=1, vbin=1):  # pylint: disable=unused-argument
        """
        Get the minimal and maximal ROI parameters.

        Return tuple ``(hlim, vlim)``, where each element is in turn a limit 5-tuple
        ``(min, max, pstep, sstep, maxbin)`` with, correspondingly, minimal and maximal size,
        position and size step, and the maximal binning.
        In some cameras, the step and the minimal size depend on the binning, which can be supplied.
        """
        w,h=self.get_detector_size()
        return TAxisROILimit(w,w,w,w,1),TAxisROILimit(h,h,h,h,1)






def _get_partial_frame(frame, excl_area):
    nr,nc=frame.shape[-2:]
    r0,r1,c0,c1=excl_area
    is_row=r1-r0<c1-c0
    row_edge=(r0==0) or (r1==nr-1)
    col_edge=(c0==0) or (c1==nc-1)
    if not (row_edge or col_edge):
        return None
    if (is_row and row_edge) or (not is_row and not col_edge):
        return frame[:,r1+1:,:] if r0==0 else frame[:,:r0,:]
    else:
        return frame[:,:,c1+1:] if c0==0 else frame[:,:,:c0]

def _normalize_sline_pos(status_line, shape):
    _,(r0,r1,c0,c1)=status_line
    nr,nc=shape[-2:]
    r0=r0%nr if r0<0 else min(r0,nr)
    r1=r1%nr if r1<0 else min(r1,nr)
    c0=c0%nc if c0<0 else min(c0,nc)
    c1=c1%nc if c1<0 else min(c1,nc)
    return r0,r1,c0,c1
def remove_status_line(frame, status_line, policy="duplicate", copy=True, value=0):
    """
    Remove status line, if present.

    Args:
        frame: a frame to process (2D or 3D numpy array; if 3D, the first axis is the frame number)
        status_line: status line descriptor (from the frames message)
        policy: determines way to deal with the status line;
            can be ``"keep"`` (keep as is), ``"cut"`` (cut off the status-line-containing row/column), ``"zero"`` (set it to zero), ``"value"`` (set it to a given value),
            ``"median"`` (set it to the image median), or ``"duplicate"`` (set it equal to the previous row; default)
            ``"cut"`` is only possible of the status line is on the edge of the image.
        copy: if ``True``, make copy of the original frames; otherwise, attempt to remove the line in-place
    """
    if copy:
        frame=frame.copy()
    if status_line is None:
        return frame
    if frame.ndim==2:
        frame_2d=True
        frame=frame[None]
    else:
        frame_2d=False
    nr,nc=frame.shape[-2:]
    r0,r1,c0,c1=_normalize_sline_pos(status_line,frame.shape)
    is_row=r1-r0<c1-c0
    if policy=="duplicate" and r0==0 and r1==nr-1 and c0==0 and c1==nc-1:
        policy="zero"
    if policy=="zero":
        policy="value"
        value=0
    if policy=="median":
        pframe=_get_partial_frame(frame,(r0,r1,c0,c1))
        if pframe is None or any([d==0 for d in pframe.shape]):
            med=np.median(frame,axis=(1,2))
        else:
            med=np.median(pframe,axis=(1,2))
        frame[:,r0:r1+1,c0:c1+1]=med[:,None,None]
    elif policy=="value":
        frame[:,r0:r1+1,c0:c1+1]=value
    elif policy=="cut":
        pframe=_get_partial_frame(frame,(r0,r1,c0,c1))
        if pframe is not None:
            frame=pframe
    elif policy=="duplicate":
        if is_row and not (r0==0 and r1==nr-1):
            graft=frame[:,r0-1,c0:c1+1] if r0>0 else frame[:,r1+1,c0:c1+1]
            frame[:,r0:r1+1,c0:c1+1]=graft[:,None,:]
        else:
            graft=frame[:,r0:r1+1,c0-1] if c0>0 else frame[:,r0:r1+1,c1+1]
            frame[:,r0:r1+1,c0:c1+1]=graft[:,:,None]
    return frame[0] if frame_2d else frame
def extract_status_line(frame, status_line, copy=True):
    """
    Extract status line, if present.

    Args:
        frame: a frame to process (2D or 3D numpy array; if 3D, the first axis is the frame number)
        status_line: status line descriptor (from the frames message)
        copy: if ``True``, make copy of the original status line data.
    """
    if status_line is None:
        return None
    if frame.ndim==2:
        frame_2d=True
        frame=frame[None,:,:]
    else:
        frame_2d=False
    r0,r1,c0,c1=_normalize_sline_pos(status_line,frame.shape)
    sline=frame[:,r0:r1+1,c0:c1+1]
    if copy:
        sline=sline.copy()
    return sline[0] if frame_2d else sline
def insert_status_line(frame, status_line, value, copy=True):
    """
    Insert status line, if present.

    Args:
        frame: a frame to process (2D or 3D numpy array; if 3D, the first axis is the frame number)
        status_line: status line descriptor (from the frames message)
        value: status line value
        copy: if ``True``, make copy of the original status line data.
    """
    if status_line is None:
        return frame.copy() if copy else frame
    r0,r1,c0,c1=_normalize_sline_pos(status_line,frame.shape)
    if value.ndim==2:
        value=value[None,:,:]
    value=value[:,:r1-r0+1,:c1-c0+1]
    return remove_status_line(frame,status_line,policy="value",value=value,copy=copy)
def get_status_line_roi(frame, status_line):
    """Return ROI taken by the status line in the given frame"""
    if status_line is None:
        return None
    r0,r1,c0,c1=_normalize_sline_pos(status_line,frame.shape)
    return image_utils.ROI(r0,r1+1,c0,c1+1)