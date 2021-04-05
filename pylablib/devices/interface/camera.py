from ...core.devio import interface
from ...core.dataproc import image_utils
from ...core.utils import function_utils, general_utils

import numpy as np
import collections
import contextlib
import time
import functools
import threading


TFramesStatus=collections.namedtuple("TFramesStatus",["acquired","unread","skipped","buffer_size"])
class ICamera(interface.IDevice):
    """
    Generic camera class.

    Provides a consistent common interface for the most frequently encountered camera functions.
    """
    _default_image_indexing="rct"
    _default_image_dtype="<u2"
    _clear_pausing_acquisition=False
    Error=RuntimeError
    TimeoutError=RuntimeError
    def __init__(self):
        super().__init__()
        self._acq_params=None
        self._default_acq_params=function_utils.funcsig(self.setup_acquisition).defaults
        self._frame_counter=FrameCounter()
        self._image_indexing=self._default_image_indexing
        self._add_status_variable("buffer_size",lambda: self.get_frames_status().buffer_size)
        self._add_status_variable("acquired_frames",lambda: self.get_frames_status().acquired)
        self._add_status_variable("acquisition_in_progress",self.acquisition_in_progress)
        self._add_status_variable("frames_status",self.get_frames_status)
        self._add_status_variable("data_dimensions",self.get_data_dimensions)
        self._add_info_variable("detector_size",self.get_detector_size)


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
        
        Return tuple ``(updated, full)``, where ``updated`` is a dictionary of parametes which are different from the ones set up,
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

        If necessary, set it up first.
        Any non-specified acquisition parameters are assumed to be the same as previously set (or default, if not explicitly set before).
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
        """
        if clear is None:
            clear=self._clear_pausing_acquisition
        acq_in_progress=self.acquisition_in_progress()
        self.stop_acquisition()
        if clear:
            acq_params=self.get_acquisition_parameters()
            self.clear_acquisition()
        try:
            yield
        finally:
            if clear and acq_params:
                self.setup_acquisition(**acq_params)
            if acq_in_progress:
                self.start_acquisition()

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
        can be "lastread"`` (from the last read frame), ``"lastwait"`` (wait for the last successfull :meth:`wait_for_frame` call),
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
    _p_indexing=interface.EnumParameterClass("indexing",["rct","rcb","xyt","xyb"])
    @interface.use_parameters
    def set_image_indexing(self, indexing):
        """
        Set up indexing for the returned images.

        Can be ``"rct"`` (first index row, second index column, rows counted from the top), ``"rcb"`` (same as ``"rc"``, rows counted from the bottom),
        ``"xyt"`` (first index column, second index row, rows counted from the top), or ``"xyb"`` (same as ``"xyt"``, rows counted from the bottom)
        """
        self._image_indexing=indexing
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
    

    def get_new_images_range(self):
        """
        Get the range of the new images.
        
        Return tuple ``(first, last)`` with images range (inclusive).
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
    _p_missing_frame=interface.EnumParameterClass("missing_frame",["none","zero","skip"])
    @interface.use_parameters
    def read_multiple_images(self, rng=None, peek=False, missing_frame="skip", return_info=False):
        """
        Read multiple images specified by `rng` (by default, all un-read images).

        If no new frames are available, return an empty list; if no acquisition is running, return ``None``.
        If ``peek==True``, return images but not mark them as read.
        `missing_frame` determines what to do with frames which are out of range (missing or lost):
        can be ``"none"`` (replacing them with ``None``), ``"zero"`` (replacing them with zero-filled frame), or ``"skip"`` (skipping them).
        If ``return_info==True``, return tuple ``(frames, infos)``, where ``infos`` is a list of frame info tuples (camera-dependent);
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
        If ``return_info==True``, return tuple ``(frame, info)``, where ``info`` is an info tuples (camera-dependent).
        """
        rng=self.get_new_images_range()
        if rng is None or rng[0]==rng[1]:
            return None
        res=self.read_multiple_images(rng=rng,peek=peek,return_info=return_info)
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

        If ``buffer_size is None``, assume the the buffer is dealocated.
        Otherwise, it specifies the frame buffer size (in frames).
        """
        self.buffer_size=buffer_size
        self.wait_start_frame=None
        self.last_acquired_frame=-1
        self.last_wait_frame=-1
        self.last_read_frame=-1
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
        unread=min(full_unread,self.buffer_size)
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
        oldest_valid_frame=self.last_acquired_frame-self.buffer_size+1
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
    def get_roi_limits(self):
        """
        Get the minimal and maximal ROI parameters.

        Return tuple ``(min_roi, max_roi)``, where each element is in turn a 4-tuple describing the ROI (as described in :meth:`get_roi`).
        """
        w,h=self.get_detector_size()
        return (0,w,0,h),(0,w,0,h)


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
    def get_roi_limits(self):
        """
        Get the minimal and maximal ROI parameters.

        Return tuple ``(min_roi, max_roi)``, where each element is in turn a 4-tuple describing the ROI (as described in :meth:`get_roi`).
        """
        w,h=self.get_detector_size()
        return (0,w,0,h,1,1),(0,w,0,h,1,1)
