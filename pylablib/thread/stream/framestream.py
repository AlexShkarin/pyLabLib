from ...misc.file_formats import cam
# from pylablib.aux_libs.devices import PhotonFocus
# from pylablib.aux_libs.gui import helpers

from ...core.thread import controller
from ...core.utils import dictionary, files as file_utils
from ...core.dataproc import image
from ...core.fileio import savefile, loadfile

import time
import collections
import numpy as np
import imageio
import os



########## Generic frames message ##########

class FramesMessage:
    """
    A message containing a frame bundle and associated information (indices, etc.).

    Also has methods for simple data extraction/modification.

    Args:
        frames: list of frames (2D or 3D numpy arrays for 1 or more frames)
        indices: list of frame indices (if a corresponding array contains several frames, it is the index of the first frame)
        metainfo: additional metainfo dictionary; the contents is arbitrary, but it's assumed to be message-wide, i.e., common for all frames in the message;
            common keys are ``"source"`` (frames source, e.g., camera or processor), ``"rate"`` (frame rate), ``"time"`` (creation time), or ``"tag"`` (additional batch tag)
        step: presumed index step between different frames (used for data consistency check)
        status_line: if status line is present, it is a tuple ``(kind, area)``, where ``kind`` is the status line kind (depends on the camera),
            and ``area`` is a 4-tuple ``(rstart, rend, cstart, cend)`` with the status line area (start and stop both inclusive; can be negative)
    """
    def __init__(self, frames, indices, metainfo=None, step=1, status_line=None):
        if isinstance(frames,tuple):
            frames=list(frames)
        elif not isinstance(frames,list):
            frames=[frames]
        self.frames=[f[None] if f.ndim==2 else f for f in frames]
        if isinstance(indices,tuple):
            indices=list(indices)
        elif not isinstance(indices,list):
            indices=[indices]
        self.indices=indices
        if len(self.frames)!=len(self.indices):
            raise ValueError("frames and indices array lengths don't agree: {} vs {}".format(len(frames),len(indices)))
        self.metainfo=metainfo or {}
        self.step=step
        self.status_line=status_line
        self._expand_indices()

    def _expand_indices(self):
        for i,f in enumerate(self.frames):
            idx=self.indices[i]
            if np.ndim(idx)==0:
                self.indices[i]=np.arange(idx,idx+f.shape[0]*self.step,self.step)
            elif len(f)!=len(idx):
                raise ValueError("frames and indices array lengths don't agree: {} vs {}".format(len(f),len(idx)))

    def copy(self, **kwargs):
        """
        Make a copy of the message
        
        Any specified keword parameter replaces the current message parameter.
        Frames and indices are not deep copied.
        """
        kwargs.setdefault("frames",self.frames)
        kwargs.setdefault("indices",self.indices)
        kwargs.setdefault("step",self.step)
        kwargs.setdefault("metainfo",self.metainfo)
        kwargs.setdefault("status_line",self.status_line)
        return FramesMessage(**kwargs)

    def has_frames(self):
        """Check if the message has frames"""
        return len(self.frames)>0
    def __bool__(self):
        return self.has_frames()
    def nframes(self):
        """Get total number of frames (taking into account that 3D array elements contain multiple frames)"""
        return sum([len(f) for f in self.frames])
    def nbytes(self):
        """Get total size of the frames in the message in bytes"""
        return sum([f.nbytes for f in self.frames])

    def missing_frames(self, last_frame=None):
        """
        Check the message for missing frames.

        If `last_frame` is not ``None``, it should be the index of the frame preceding this block.
        Return number of missing frames.
        """
        missing=0
        for i,f in zip(self.indices,self.frames):
            if last_frame is not None:
                missing+=i[0]-last_frame-self.step
            last_frame=i[-1]
        return missing
    
    def get_frames_stack(self, n=None, reverse=False, add_indices=False, copy=True):
        """
        Get a list of at most `n` frames from the message (if ``None``, return all frames).

        If ``reverse==True``, return last `n` frames (in the reversed order); otherwise, return first `n` frames.
        If ``add_indices==True``, elements of the list are tuples ``(index, img)``; otherwise, they are just images.
        If ``copy==True``, copy frames (otherwise changing the returned frames can affect the stored frames).
        """
        if n==0:
            return []
        if n is None:
            n=self.nframes()
        frames=[]
        indices=[]
        if reverse:
            for i,f in zip(self.indices[::-1],self.frames[::-1]):
                chunk=f[:-(n-len(frames))-1:-1]
                add_frames=list(chunk.copy()) if copy else list(chunk)
                frames+=add_frames
                if add_indices:
                    indices+=list(i[:-(n-len(frames))-1:-1])
                if len(frames)>=n:
                    break
        else:
            for i,f in zip(self.indices,self.frames):
                chunk=f[:n-len(frames)]
                add_frames=list(chunk.copy()) if copy else list(chunk)
                frames+=add_frames
                if add_indices:
                    indices+=list(i[:n-len(frames)])
                if len(frames)>=n:
                    break
        return list(zip(indices,frames)) if add_indices else frames
    def cut_to_size(self, n, reverse=False):
        """
        Cut contained data to contain at most `n` frames.

        If ``reverse==True``, leave last `n` frames; otherwise, leave first `n` frames.
        Return ``True`` if there are `n` frames after the cut, and ``False`` if there are less than `n`.
        """
        if n==0:
            self.frames=[]
            self.indices=[]
            return True
        end=None
        size=0
        if reverse:
            self.frames=self.frames[::-1]
            self.indices=self.indices[::-1]
        for i,f in enumerate(self.frames):
            if size+len(f)>n:
                end=i
                break
            size+=len(f)
        if end is None:
            return size<n
        new_frames=self.frames[:end]
        if size<n:
            if not reverse:
                new_frames.append(self.frames[end][:n-size])
            else:
                new_frames.append(self.frames[end][-(n-size):])
        self.frames=new_frames
        self.indices=self.indices[:len(self.frames)]
        if reverse:
            self.frames=self.frames[::-1]
            self.indices=self.indices[::-1]
            self.indices[0]=self.indices[0][-len(self.frames[0]):]
        return True
        
    def first_frame_index(self):
        """Get index of the first frame (or ``None`` if there are no frames)"""
        if not self.has_frames():
            return None
        return self.indices[0][0]
    def last_frame_index(self):
        """Get index of the last frame (or ``None`` if there are no frames)"""
        if not self.has_frames():
            return None
        return self.indices[-1][-1]
    def first_frame(self, copy=True):
        """Get the first frame (or ``None`` if there are no frames)"""
        if not self.has_frames():
            return None
        return self.frames[0][0].copy() if copy else self.frames[0][0]
    def last_frame(self, copy=True):
        """Get the last frame (or ``None`` if there are no frames)"""
        if not self.has_frames():
            return None
        return self.frames[-1][-1].copy() if copy else self.frames[-1][-1]



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
        frame=frame[None,:,:]
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
    return image.ROI(r0,r1+1,c0,c1+1)











########## Frame saving ##########

TPretriggerBufferStatus=collections.namedtuple("TPretriggerBufferStatus",["frames","skipped","nbytes","size"])
class PretriggerBuffer:
    """
    Pretrigger buffer.

    Keeps track of the added frames and the total size, finds skips frames.

    Args:
        size: maximal buffer size
        strict_size: if ``True``, the number of the frames in the buffer is never greater than `size`;
            otherwise, the frame number is quantized to the whole frame messages, so the size might be larger.
        clear_on_reset: if ``True`` and a message with the reset signature (zero start index) is added, clear the buffer before adding.
    """
    def __init__(self, size, strict_size=True, clear_on_reset=True):
        self.size=size
        self.buffer=[]
        self.current_size=0
        self.strict_size=strict_size
        self.clear_on_reset=clear_on_reset
    
    def add_frame_message(self, msg):
        """Add a new frame message"""
        if not msg.has_frames():
            return
        if not msg.first_frame_index() and self.clear_on_reset:
            self.clear()
        self.buffer.append(msg)
        self.current_size+=msg.nframes()
        while self.buffer and self.current_size-self.buffer[0].nframes()>=self.size:
            self.current_size-=self.buffer[0].nframes()
            del self.buffer[0]
        if self.strict_size and self.current_size>self.size:
            extra_frames=self.current_size-self.size
            self.buffer[0].cut_to_size(self.buffer[0].nframes()-extra_frames,reversed=True)
            self.current_size-=extra_frames
    def pop_frame_message(self):
        """Pop the latest frame message"""
        if self.buffer:
            self.current_size-=self.buffer[0].nframes()
            return self.buffer.pop(0)
    def clear(self):
        """Clear all frames in the buffer"""
        self.buffer=[]
        self.current_size=0
    def copy(self):
        """Return copy of the buffer"""
        buff=PretriggerBuffer(self.size,self.strict_size,self.clear_on_reset)
        buff.buffer=list(self.buffer)
        buff.current_size=self.current_size
        return buff

    def has_frames(self):
        """Check if there are frames in the buffer"""
        return bool(self.buffer)
    def nframes(self):
        """Get total number of frames"""
        return sum([m.nframes() for m in self.buffer])
    def nbytes(self):
        """Get total size of the frames in bytes"""
        return sum([m.nbytes() for m in self.buffer])
    def get_status(self):
        """
        Get buffer status.

        Return tuple ``(frames, skipped, nbytes, size)`` with, correspondingly, number of frames in the buffer, number of skipped frames amongst them,
        size of the buffer in bytes, and maximal buffer size.
        """ 
        last_frame_idx=None
        nframes=self.nframes()
        nbytes=self.nbytes()
        skipped=0
        for m in self.buffer:
            skipped+=m.get_missed_frames(last_frame_idx if m.first_frame_index() else None) # don't count reset as skip
            last_frame_idx=m.last_frame_index()
        return TPretriggerBufferStatus(nframes,skipped,nbytes,self.size)
    





class FramesWriter:
    def __init__(self):
        self.path=None

    def open(self, path, append=False):
        self.path=path
        self.append=append
        return self
    def close(self):
        self.path=None
    def add(self, frames):
        pass
    
    def __bool__(self):
        return self.path is not None
    def __enter__(self):
        return self
    def __exit__(self, *args, **vargs):
        self.close()
        return False

class BinFramesWriter(FramesWriter):
    def __init__(self, dtype=None, byteorder="<"):
        FramesWriter.__init__(self)
        self.dtype=dtype
        self.byteorder=byteorder
    def open(self, path, append=False):
        FramesWriter.open(self,path,append=append)
        self.f=open(path,mode="ab" if append else "wb")
        return self
    def close(self):
        if self.f is not None:
            self.f.close()
            self.f=None
        FramesWriter.close(self)
    def add(self, frames):
        dtype=(self.dtype or frames.dtype).newbyteorder(self.byteorder)
        frames.astype(dtype).tofile(self.f)
    
class TiffFramesWriter(FramesWriter):
    def __init__(self):
        FramesWriter.__init__(self)
        self.writer=None
    def open(self, path, append=False):
        FramesWriter.open(self,path,append=append)
        self.writer=imageio.get_writer(path,format="tiff",mode="V")
        return self
    def close(self):
        if self.writer is not None:
            self.writer.close()
            self.writer=None
        FramesWriter.close(self)
    def add(self, frames):
        if frames.ndim==3 and len(frames) in [3,4]: # can be confused with color-channel data
            self.writer.append_data(frames[:2])
            self.writer.append_data(frames[2:])
        else:
            self.writer.append_data(frames)
    
class CamFramesWriter(FramesWriter):
    def open(self, path, append=False):
        FramesWriter.open(self,path,append=append)
        self.started=False
    def add(self, frames):
        append=self.append or self.started
        cam.save_cam(frames,self.path,append=append)
        self.started=True






class FrameSaveThread(controller.QTaskThread):
    """
    Frame saving thread

    Receives frame announcements, and saves the frames to the disk.

    Setup args:
        src: frames source
        tag: frames announcement tag
        settings_mgr: :class:`.SettingsManager` thread name (used to save settings file on saving start)
        frame_processor: frame processor thread name (used to get snapshot background to save to the file, if appropriate)

    Attributes:
        chunks_per_save: number of saving queue chunks to write to disk in one dump job (by default, one chunk)
        chunk_period (float): duration of a single saving queue chunk (in seconds); by default, 0.5 seconds
        dumping_period (float): period of queue dump job; by default, 0.1 seconds

    Variables:
        path: saving path
        batch_size: saving batch size (limit on the total number of frames saved)
        received: total frames received since the saving started
        scheduled: total frames scheduled for saving since the saving started (received frame is scheduled unless queue RAM is overflowing)
        saved: total frames saved since the saving started
        missed: total number of frames missed in saving since the saving stated (based on frames indices)
        pretrigger_status: tuple with the pretrigger status (see :meth:`PretriggerBuffer.get_status`), or ``None`` if pretrigger is disabled
        queue_ram: current occupied queue RAM size
        max_queue_ram: maximal queue RAM size
        status_line_check: status line check status; can be ``"off"`` (check is off), ``"none"`` (frames don't have status line), ``"na"`` (no frames have been received yet),
            ``"ok"`` (status line check is ok), ``"missing"`` (missing frames), ``"still"`` (repeating frames), or ``"out_of_order"`` (later frames have lower index).

    Commands:
        save_start: start streaming
        save_stop: stop streaming
        setup_pretrigger: setup pretrigger buffer
        clear_pretrigger: clear pretrigger buffer
        setup_queue_ram: setup maximal saving queue RAM
    """
    def setup_task(self, src, tag, settings_mgr=None, frame_processor=None):
        self.subscribe_commsync(self.receive_frames,srcs=src,dsts="any",tags=tag,limit_queue=100)
        self.settings_mgr=settings_mgr
        self._cam_settings_time="before" # ``"before"`` - get full camera settings in the beginning of saving; ``"after"`` - get them in the end of saving
        self.frame_processor=frame_processor
        self._save_queue=None
        self._pretrigger_buffer=None
        self._clear_pretrigger_on_write=True
        self._saving=False
        self._stopping=False
        self.sync_period=0.1
        self["path"]=None
        self["batch_size"]=None
        self["saved"]=0
        self["received"]=0
        self["scheduled"]=0
        self["missed"]=0
        self["pretrigger_status"]=None
        self.append=False
        self.filesplit=None
        self.fmt="raw"
        self.frame_writers={"raw":BinFramesWriter,"bin":BinFramesWriter,"tiff":TiffFramesWriter,"cam":CamFramesWriter}
        self._writer=None
        self.background_desc={}
        self._last_frame_idx=None
        self._file_idx=0
        self.chunks_per_save=1
        self.chunk_period=0.2
        self.dumping_period=0.02
        self._event_log_started=False
        self._start_time=None
        self._first_frame_recvd=None
        self._first_frame_idx=None
        self._last_frame_recvd=None
        self._last_frame=None
        self._last_chunk_start=0
        self._tiff_writer=None
        self["max_queue_ram"]=2**30*4
        self._update_queue_ram(0)
        self["status_line_check"]="off"
        self._last_frame_statusline_idx=None
        self._perform_status_check=False
        self.update_status("saving","stopped",text="Saving done")
        self.add_command("save_start",self.save_start)
        self.add_command("save_stop",self.save_stop)
        self.add_command("setup_queue_ram",self.setup_queue_ram)
        self.add_command("write_event_log",self.write_event_log)
        self.add_command("setup_pretrigger",self.setup_pretrigger)
        self.add_command("clear_pretrigger",self.clear_pretrigger)
        self.add_job("dump_queue",self.dump_queue,self.dumping_period)
    def finalize_task(self, *args, **kwargs):
        if self._saving:
            self._finalize_saving()
    
    def setup_pretrigger(self, size, enabled=True, preserve_frames=True, clear_on_write=True):
        """
        Setup pretrigger.

        Args:
            size (int): maximal pretrigger size
            enabled (bool): whether pretrigger is enabled
            preserve_frames (bool): if ``True``, preserve frames already in the buffer when changing its size; otherwise, clear the buffer.
            clear_on_write (bool): if ``True``, the buffer frames are removed from it when they are saved (default behavior); otherwise, the buffer state is preserved
                keep in mind that it's not updated during save (so there will be a gap for newly-added frames);
                generally, only makes sense to set ``clear_on_write=False`` for single-frame buffers
        """
        if enabled:
            if not (self._pretrigger_buffer and self._pretrigger_buffer.size==size):
                curr_buffer=self._pretrigger_buffer
                self._pretrigger_buffer=PretriggerBuffer(size)
                if curr_buffer and preserve_frames:
                    while curr_buffer.has_frames():
                        self._pretrigger_buffer.add_frame_message(curr_buffer.pop_frame_message())
        else:
            self._pretrigger_buffer=None
        self._clear_pretrigger_on_write=clear_on_write
        self["pretrigger_status"]=self._pretrigger_buffer.get_status() if self._pretrigger_buffer else None
    def clear_pretrigger(self):
        """Clear the pretrigger buffer"""
        if self._pretrigger_buffer:
            self._pretrigger_buffer.clear()
            self["pretrigger_status"]=self._pretrigger_buffer.get_status()
    def setup_queue_ram(self, max_queue_ram):
        self["max_queue_ram"]=max_queue_ram
        # self._frame_scheduler.change_max_size((self._frame_scheduler.max_size[0],self["max_queue_ram"]))
    def _update_queue_ram(self, queue_ram=None):
        if queue_ram is not None:
            self["queue_ram"]=queue_ram
        # self._frame_scheduler.change_max_size((self._frame_scheduler.max_size[0],self["max_queue_ram"]-self["queue_ram"]))
    def dump_queue(self):
        """Dump one or several chunks from the saving queue to the disk"""
        queue_empty=False
        path=self["path"]
        append=(self["saved"]>0) or self.append
        for _ in range(self.chunks_per_save):
            new_chunk=self._save_queue.pop(0) if self._save_queue else []
            queue_empty=not self._save_queue
            if new_chunk:
                if self._first_frame_idx is None:
                    self._first_frame_idx=new_chunk[0].first_frame_index()
                chunk_size=sum([msg.nbytes() for msg in new_chunk])
                self._update_queue_ram(self["queue_ram"]-chunk_size)
                flat_chunk=[f for m in new_chunk for f in m.frames]
                if self._perform_status_check:
                    if self["status_line_check"] in {"ok","na"}:
                        self["status_line_check"]=self._check_status_line(flat_chunk,step=new_chunk[0].step)
                self._write_frames(flat_chunk,path,append=append)
                self["saved"]+=sum([msg.nframes() for msg in new_chunk])
                append=True
            if queue_empty:
                if self._stopping:
                    self._finalize_saving()
                    self._saving=False
                    self._stopping=False
                    self.update_status("saving","stopped",text="Saving done")
                else:
                    self.sleep(0.02)
                break
    def _finalize_saving(self):
        self._write_finish()
        if self._event_log_started:
            self.write_event_log("Recording stopped")
        self.finalize_settings()

    def _gen_path(self, path):
        """Generate save path based on prefix"""
        if self._file_idx is None:
            return path
        name,ext=os.path.splitext(path)
        return "{}_{:04d}{}".format(name,self._file_idx,ext)
    def _clean_path(self, path):
        """Clean saving path (remove file with this path if it exists)"""
        path=self._gen_path(path)
        if os.path.exists(path):
            file_utils.retry_remove(path)
    def _get_settings_path(self, path):
        """Generate save path for settings file"""
        name,_=os.path.splitext(path)
        return "{}_settings.dat".format(name)
    def _get_settings(self):
        """Get settings dictionary for the saver thread"""
        return {"path":file_utils.normalize_path(self["path"]),
                "batch_size":self["batch_size"],
                "chunk_size":self.filesplit or self["batch_size"],
                "append":self.append,
                "format":self.fmt,
                "background":self.background_desc,
                "start_timestamp":time.time(),
                "pretrigger_status/start":self["pretrigger_status"]}
    def _get_finalized_settings(self):
        """Get finalized settings (additional info at the end of saving process)"""
        settings={}
        for s in ["saved","scheduled","missed","received","status_line_check"]:
            settings[s]=self[s]
        settings["first_frame_timestamp"]=self._first_frame_recvd
        settings["first_frame_index"]=self._first_frame_idx
        settings["last_frame_timestamp"]=self._last_frame_recvd
        settings["stop_timestamp"]=time.time()
        settings["pretrigger_status/stop"]=self["pretrigger_status"]
        if self._last_frame is not None:
            settings["frame/shape"]=self._last_frame.shape
            settings["frame/dtype"]=self._last_frame.dtype.str
        return settings
    def _get_manager_settings(self, include=None, exclude=None, alias=None):
        if self.settings_mgr:
            try:
                settings_mgr=controller.get_controller(self.settings_mgr,sync=False)
                return settings_mgr.cs.get_all_settings(include=include,exclude=exclude,alias=alias)
            except controller.threadprop.NoControllerThreadError:
                pass
        return {}
    def write_settings(self, extra_settings=None):
        """Collect full settings dictionary and save it to the disk"""
        if self._cam_settings_time=="before":
            settings=self._get_manager_settings(exclude=["cam/settings"]) or dictionary.Dictionary()
        else:
            settings=self._get_manager_settings(exclude=["cam"],alias={"cam/settings":"cam/settings_start"}) or dictionary.Dictionary()
        settings["save"]=self._get_settings()
        if extra_settings is not None:
            settings["extra"]=extra_settings
        savefile.save_dict(settings,self._get_settings_path(self["path"]))
    def finalize_settings(self):
        """Save finalized settings to the file"""
        path=self._get_settings_path(self["path"])
        if os.path.exists(path):
            settings=loadfile.load_dict(path)
            settings.update(self._get_finalized_settings(),"save")
            if self._cam_settings_time!="before":
                settings.merge_branch(self._get_manager_settings(include=["cam"]).get("cam",{}),branch="cam")
            settings.merge_branch(self._get_manager_settings(include=["cam/cnt"]).get("cam/cnt",{}),branch="cam/cnt_after")
            savefile.save_dict(settings,path)

    def _get_background_path(self, path):
        """Generate save path for background file"""
        name,_=os.path.splitext(path)
        return "{}_background.bin".format(name)
    def _get_snapshot_background_parameters(self):
        if self.frame_processor:
            try:
                frame_processor=controller.get_controller(self.frame_processor,sync=False)
                return frame_processor.get_background_to_save(),frame_processor["snapshot_mode"]
            except controller.threadprop.NoControllerThreadError:
                pass
        return None,None
    def write_background(self):
        """Get background from the frame processor and save it to the disk"""
        background,mode=self._get_snapshot_background_parameters()
        if background is not None:
            background=np.array(background)
            save_dtype="<f8" if background.dtype.kind=="f" else "<u2"
            with open(self._get_background_path(self["path"]),"wb") as f:
                np.asarray(background,save_dtype).tofile(f)
            bg_saving_mode="only_bg" if len(background)==1 else "all"
            self.background_desc={"size":len(background),"dtype":save_dtype,"shape":background.shape[1:],"format":"bin","bg_mode":mode,"saving_mode":bg_saving_mode}
        else:
            self.background_desc={"saving_mode":"none"}

    
    def _get_event_log_path(self, path):
        """Generate save path for event log file"""
        name,_=os.path.splitext(path)
        return "{}_eventlog.dat".format(name)
    def write_event_log(self, msg):
        """Write a text message into the event log"""
        if self._saving:
            path=self._get_event_log_path(self["path"])
            preamble=""
            if not self._event_log_started:
                if os.path.exists(path):
                    if self.append:
                        preamble="\n\n"
                    else:
                        file_utils.retry_remove(path)
                        preamble="# Timestamp\tElapsed\tFrame\tMessage\n"
                preamble+="{:.3f}\t{:.3f}\t{:d}\t{}\n".format(self._start_time,0,self._first_frame_idx or 0,"Recording started")
            with open(path,"a") as f:
                t=time.time()
                line="{:.3f}\t{:.3f}\t{:d}\t{}\n".format(t,t-self._start_time,self._last_frame_idx or 0,msg)
                if preamble:
                    f.write(preamble)
                f.write(line)
            self._event_log_started=True

    def _check_status_line(self, frames, step=1):
        for f in frames:
            lines=PhotonFocus.get_status_lines(f,check_transposed=False)
            if lines is None or lines.shape[1]<2:
                return "none"
            indices=lines[:,1]
            if self._last_frame_statusline_idx is not None:
                indices=np.insert(indices,0,self._last_frame_statusline_idx)
            dfs=(indices[1:]-indices[:-1])%(2**24) # the internal counter is only 24-bit
            if np.any(dfs>2**23) or np.any((dfs>0)&(dfs<step)): # negative
                return "out_of_oder"
            if np.any(dfs==0):
                return "still"
            if np.any(dfs<step): # step smaller than should be
                return "out_of_oder"
            if np.any(dfs>step):
                return "skip"
            self._last_frame_statusline_idx=indices[-1]
        return "ok"

    def _write_frames(self, frames, path, append=True):
        """Write frames to the given path"""
        nsaved=self["saved"]
        if frames:
            self._last_frame=frames[-1][-1,:].copy()
        if self.filesplit is None:
            with self._writer.open(path,append=append):
                for frm in frames:
                    self._writer.add(frm)
        else: # file splitting mechanics
            for frm in frames:
                frm_size=len(frm)
                frm_saved=0
                while frm_saved<frm_size:
                    lchunk=(-nsaved-1)%self.filesplit+1
                    frm_to_save=min(lchunk,frm_size-frm_saved)
                    if not self._writer:
                        self._writer.open(self._gen_path(path),append=append)
                    self._writer.add(frm[frm_saved:frm_saved+frm_to_save])
                    frm_saved+=frm_to_save
                    nsaved+=frm_to_save
                    if nsaved%self.filesplit==0:
                        self._writer.close()
                        self._file_idx+=1
                        self._clean_path(path)
    def _write_finish(self):
        """Finalize writing (applies only for tiff files)"""
        if self._writer:
            self._writer.close()
            self._writer=None



    def save_start(self, path, batch_size=None, append=True, fmt="raw", filesplit=None, save_settings=False, perform_status_check=False, extra_settings=None):
        """
        Start saving routine.

        Args:
            path (str): saving path (suffix can be appended if `filesplit` is defined)
            batch_size: maximal number of frames to save (by default, no limit)
            append (bool): if ``True`` and the destination file already exists, append data to it; otherwise, remove it before saving
            fmt (str): file format; can be ``"raw"`` or ``"bin"`` (raw binary in ``"<u2"`` format), ``"cam"`` (.cam file), or ``"tiff"`` (tiff format)
            filesplit: maximal number of frames per file (by default, all frames are in one file); if defined, file names acquire numerical suffix
            save_settings (bool): if ``True``, save all application setting to the file
            perform_status_check (bool): if ``True`` and frames have status line (applies only to Photon Focus cameras), check status line to ensure no missing frames
            extra_settings: can be a dictionary with additional settings to save to the settings file (saved in branch ``"extra"``)
        """
        if self._saving:
            self._finalize_saving()
            self.update_status("saving","stopped",text="Saving done")
        self["path"]=path
        self["batch_size"]=batch_size
        self.append=append or (filesplit is not None)
        if fmt not in ["cam","raw","bin","tiff"]:
            raise ValueError("unrecognized fmt: {}".format(fmt))
        self.fmt=fmt
        self._writer=self.frame_writers[self.fmt]
        self.filesplit=filesplit
        self["saved"]=0
        self["scheduled"]=0
        self["received"]=0
        self["missed"]=0
        self._save_queue=[]
        self._event_log_started=False
        self._start_time=time.time()
        self._first_frame_recvd=None
        self._first_frame_idx=None
        self._last_frame_recvd=None
        self._last_chunk_start=0
        self._update_queue_ram(0)
        self._stopping=False
        self._saving=True
        self._last_frame_idx=None
        self._file_idx=0
        self["status_line_check"]="na" if perform_status_check else "off"
        self._last_frame_statusline_idx=None
        self._perform_status_check=perform_status_check
        file_utils.ensure_dir(os.path.split(path)[0])
        if filesplit is not None:
            self._clean_path(path)
        self.write_background()
        if save_settings:
            self.write_settings(extra_settings=extra_settings)
        self.update_status("saving","in_progress",text="Saving in progress")
        if self._pretrigger_buffer is not None:
            if not self._clear_pretrigger_on_write:
                old_buffer=self._pretrigger_buffer.copy()
            while self._pretrigger_buffer.has_frames():
                msg=self._pretrigger_buffer.pop_frame_message()
                scheduled=self.schedule_message(msg)
                if not scheduled:
                    break
            if not self._clear_pretrigger_on_write:
                self._pretrigger_buffer=old_buffer
        self["pretrigger_status"]=self._pretrigger_buffer.get_status() if self._pretrigger_buffer else None
    def save_stop(self):
        """Stop saving routine"""
        self._stopping=True
        self.update_status("saving","stopping",text="Finishing saving")


    def _append_queue(self, msg):
        """Append frames to the saving queue"""
        last_chunk=[]
        if msg.creation_time-self._last_chunk_start>self.chunk_period:
            self._last_chunk_start=msg.creation_time
        elif self._save_queue:
            last_chunk=self._save_queue.pop()
        last_chunk.append(msg)
        self._save_queue.append(last_chunk)
    def schedule_message(self, msg):
        """
        Add frame message to the saving queue.

        Return ``True`` if the message was scheduled and ``False`` otherwise (number of frames reached the desired file size).
        """
        scheduled=False
        if self._saving and not self._stopping:
            if self["batch_size"] is not None:
                max_frames=self["batch_size"]-self["scheduled"]
                msg.cut_to_size(max_frames)
            tot_frames=msg.nframes()
            if tot_frames:
                if self._first_frame_recvd is None:
                    self._first_frame_recvd=msg.creation_time
                self._last_frame_recvd=msg.creation_time
                if self["queue_ram"]<=self["max_queue_ram"]:
                    self._append_queue(msg)
                    self._update_queue_ram(self["queue_ram"]+msg.nbytes())
                    self["missed"]+=msg.get_missed_frames(self._last_frame_idx if msg.first_frame_index() else None) # don't count reset as skip
                    self["scheduled"]+=tot_frames
                else:
                    self["missed"]+=msg.last_frame_index()-self._last_frame_idx if (self._last_frame_idx is not None) else msg.nframes()
                self._last_frame_idx=msg.last_frame_index()
                self["received"]+=tot_frames
                scheduled=True
            if self["batch_size"] and self["scheduled"]>=self["batch_size"]:
                self.save_stop()
        return scheduled
    def receive_frames(self, src, tag, msg):
        """Process frame receive announcement"""
        scheduled=self.schedule_message(msg)
        if not scheduled and self._pretrigger_buffer is not None:
            self._pretrigger_buffer.add_frame_message(msg)
            self["pretrigger_status"]=self._pretrigger_buffer.get_status() if self._pretrigger_buffer else None