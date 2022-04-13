from ...core.thread import controller
from ...core.dataproc import filters

from ...devices.interface import camera as camera_utils
from . import stream_manager, stream_message

import numpy as np
import time
import collections

########## Frame processing ##########

class FrameBinningThread(controller.QTaskThread):
    """
    Full frame binning thread: receives frames and re-emit them after binning along time or space axes.

    Setup args:
        - ``src``: name of the source thread (usually, a camera)
        - ``tag_in``: receiving multicast tag (for the source multicast)
        - ``tag_out``: emitting multicast tag (for the multicast emitted by the processor); by default, same as ``tag_in``

    Multicasts:
        - ``<tag_out>``: emitted with binned frames

    Variables:
        - ``params/spat``: spatial binning parameters: ``"bin"`` for binning size (a 2-tuple) and ``"mode"`` for binning mode
        - ``params/time``: temporal binning parameters: ``"bin"`` for binning size and ``"mode"`` for binning mode
        - ``params/dtype``: resulting frames type (see :meth:`setup_binning` for parameters)
        - ``enabled``: indicates whether binning has been enabled

    Commands:
        - ``enable_binning``: enable or disable the binning
        - ``setup_binning``: setup binning parameters
    """
    def setup_task(self, src, tag_in, tag_out=None):  # pylint: disable=arguments-differ
        self.subscribe_commsync(self.process_input_frames,srcs=src,tags=tag_in,limit_queue=2,on_full_queue="wait")
        self.tag_out=tag_out or tag_in
        self.v["params/spat"]={"bin":(1,1),"mode":"skip"}
        self.v["params/time"]={"bin":1,"mode":"skip"}
        self.v["params/dtype"]=None
        self.v["enabled"]=False
        self._recv_acc=stream_message.FramesAccumulator()
        self._clear_buffer()
        self.cnt=stream_manager.StreamIDCounter()
        self.add_command("setup_binning")
        self.add_command("enable_binning")

    def enable_binning(self, enabled=True):
        """Enable or disable the binning"""
        self.v["enabled"]=enabled
    def setup_binning(self, spat_bin, spat_bin_mode, time_bin, time_bin_mode, dtype=None):
        """
        Setup binning parameters.

        Arg:
            spat_bin: tuple ``(i_bin, j_bin)`` with the binning factors along the two spatial axes.
            spat_bin_mode: mode for spatial binning; can be ``"skip"`` (simply take every n'th pixel), ``"sum"``, ``"min"``, ``"max"``, or ``"mean"``.
            time_bin: binning factor for the time axis
            time_bin_mode: same as `spat_bin_mode`, but for the time axis
            dtype: if not ``None``, the resulting frames are converted to the given type;
                otherwise, they are converted into the same type as the source frames;
                note that if the source type is integer and binning mode is ``"mean"`` or ``"sum"``, some information might be lost through rounding or integer overflow;
                for the purposes of ``"mean"`` and ``"sum"`` binning the frames are always temporarily converted to float
        """
        par=self.v["params"]
        if spat_bin!=par["spat/bin"] or spat_bin_mode!=par["spat/mode"] or time_bin!=par["time/bin"] or time_bin_mode!=par["time/mode"]:
            self._clear_buffer()
        self.v["params/spat"]={"bin":spat_bin,"mode":spat_bin_mode}
        self.v["params/time"]={"bin":time_bin,"mode":time_bin_mode}
        self.v["params/dtype"]=dtype

    def _clear_buffer(self):
        self.acc_frame=None
        self.acc_frame_num=0
        self._recv_acc.clear()
    def _bin_spatial(self, frames, n, dec, status_line):
        if n!=(1,1):
            sl=camera_utils.extract_status_line(frames,status_line,copy=False)
            if n[0]>1:
                frames=filters.decimate(frames,n[0],dec=dec,axis=-2)
            if n[1]>1:
                frames=filters.decimate(frames,n[1],dec=dec,axis=-1)
            if sl is not None:
                frames=camera_utils.insert_status_line(frames,status_line,sl,copy=(dec=="skip"))
        return frames
    def _decimate_with_status_line(self, frames, n, dec, status_line):
        res=filters.decimate(frames,n,dec=dec,axis=0)
        if dec!="skip" and status_line is not None:
            binned_n=n*(len(frames)//n)
            sl=camera_utils.extract_status_line(frames[:binned_n:n],status_line,copy=False)
            res=camera_utils.insert_status_line(res,status_line,sl,copy=False)
        return res
    def _decimate_full_with_status_line(self, frames, dec, status_line):
        res=filters.decimate_full(frames,dec)
        if dec!="skip" and status_line is not None:
            sl=camera_utils.extract_status_line(frames[0],status_line,copy=False)
            res=camera_utils.insert_status_line(res,status_line,sl,copy=False)
        return res
    def _update_buffer(self, frames, status_line):
        par=self.v["params"]
        if frames.ndim==2:
            frames=frames[None]
        dtype=frames.dtype if par["dtype"] is None else par["dtype"]
        frames=self._bin_spatial(frames,par["spat/bin"],par["spat/mode"],status_line)
        time_bin,time_bin_mode=par["time/bin"],par["time/mode"]
        if time_bin>1:
            if self.acc_frame is not None and frames.shape[-2:]!=self.acc_frame.shape:
                self._clear_buffer()
            binned_frames=[]
            time_dec_mode=time_bin_mode if time_bin_mode!="mean" else "sum"
            if time_dec_mode=="sum":
                frames=frames.astype("float")
            if self.acc_frame is not None and self.acc_frame_num+len(frames)>=time_bin: # complete current chunk
                chunk=frames[:time_bin-self.acc_frame_num]
                frames=frames[time_bin-self.acc_frame_num:]
                chunk=filters.decimate_full(chunk,time_dec_mode) if len(chunk)>1 else chunk[0]
                if self.acc_frame is not None:
                    chunk=self._decimate_full_with_status_line([self.acc_frame,chunk],time_dec_mode,status_line)
                binned_frames.append(chunk)
                self.acc_frame=None
                self.acc_frame_num=0
            if len(frames):
                binned_frames+=list(self._decimate_with_status_line(frames,time_bin,time_dec_mode,status_line)) # decimate all complete chunks
            frames_left=len(frames)%time_bin
            if frames_left: # update accumulator
                chunk=frames[-frames_left:]
                chunk=self._decimate_full_with_status_line(chunk,time_dec_mode,status_line) if len(chunk)>1 else chunk[0]
                if self.acc_frame is not None:
                    chunk=self._decimate_full_with_status_line([self.acc_frame,chunk],time_dec_mode,status_line)
                self.acc_frame=chunk
                self.acc_frame_num+=frames_left
            frames=np.asarray(binned_frames)
            if time_bin_mode=="mean" and binned_frames:
                if status_line is None:
                    frames/=time_bin
                else:
                    sl=camera_utils.extract_status_line(frames,status_line,copy=True)
                    frames/=time_bin
                    frames=camera_utils.insert_status_line(frames,status_line,sl,copy=False)
        frames=frames.astype(dtype)
        return frames

    # TODO: direct subscription + command for no-overhead forwarding?
    def process_input_frames(self, src, tag, msg):  # pylint: disable=unused-argument
        """Process multicast message with input frames"""
        if not self.v["enabled"]:
            self.send_multicast(dst="any",tag=self.tag_out,value=msg)
            return
        if self.cnt.receive_message(msg):
            self._clear_buffer()
        time_bin=self.v["params/time/bin"]
        self._recv_acc.add_message(msg)
        frames=[]
        for chunk in msg.frames:
            proc_chunk=self._update_buffer(chunk,msg.metainfo.get("status_line"))
            l=len(proc_chunk)
            if l:
                frames.append(proc_chunk if msg.chunks else proc_chunk[0])
        _,indices,frame_info=self._recv_acc.get_slice(0,(-(time_bin-1) or None),step=time_bin,flatten=True)
        self._recv_acc.cut_to_size(self.acc_frame_num,from_end=True)
        if frames:
            if msg.chunks:
                frames=np.concatenate(frames,axis=0)
                indices=np.asarray(indices)
                frame_info=np.asarray(frame_info) if frame_info is not None else None
            if "roi" in msg.metainfo:
                spat_bin=self.v["params/spat/bin"]
                roi=msg.mi.roi+(1,1)
                roi=roi[:4]+(roi[4]*spat_bin[1],roi[5]*spat_bin[0])
                mi={"roi":roi}
            else:
                mi={}
            msg=msg.copy(frames=frames,indices=indices,frame_info=frame_info,source=self.name,step=msg.mi.step*self.v["params/time/bin"],metainfo=mi)
            self.send_multicast(dst="any",tag=self.tag_out,value=msg)





class FrameSlowdownThread(controller.QTaskThread):
    """
    Frame slowdown thread: receives frames and re-emits them with reduced FPS.

    Setup args:
        - ``src``: name of the source thread (usually, a camera)
        - ``tag_in``: receiving multicast tag (for the source multicast)
        - ``tag_out``: emitting multicast tag (for the multicast emitted by the processor); by default, same as ``tag_in``

    Multicasts:
        - ``<tag_out>``: emitted with slowed frames; emitted with the maximal period controlled by the :meth:`set_output_period`,
            or on every input message if ``output_period`` is ``None``

    Variables:
        - ``enabled``: indicate whether the slowdown is on
        - ``output_period``: period for outputting the slowed frame; if ``None``, output on every input message
        - ``buffer/filled``: the number of frames in the buffer
        - ``buffer/used``: the number of frames in the buffer which have already been shown
        - ``buffer/empty``: indicates whether the buffer has already been completely filled and used
          (in this case further frames are not shown, and the processor must be stopped)
        - ``fps/in``: FPS of the incoming stream
        - ``fps/out``: FPS of the outgoing stream

    Commands:
        - ``enable``: enable or disable slowdown mode
        - ``setup_slowdown``: setup slowdown parameters
        - ``set_output_period``: set the period of output frames generation
    """
    def setup_task(self, src, tag_in, tag_out=None):  # pylint: disable=arguments-differ
        self.subscribe_commsync(self.process_input_frames,srcs=src,tags=tag_in,limit_queue=10)
        self.tag_out=tag_out or tag_in
        self.frames_buffer=[]
        self.buffer_size=1
        self.v["enabled"]=False
        self.v["output_period"]=None
        self.v["buffer/filled"]=0
        self.v["buffer/used"]=0
        self.v["buffer/empty"]=False
        self._last_emitted_time=None
        self._in_fps_calc=[None,0]
        self._out_fps_calc=[None,0]
        self.fps_period=1.
        self.v["fps/in"]=0
        self.v["fps/out"]=0
        self.add_command("enable")
        self.add_command("setup_slowdown")
        self.add_job("output_frame",self.output_frame,1.)

    def _reset(self):
        self.frames_buffer=[]
        self.v["buffer/filled"]=0
        self.v["buffer/used"]=0
        self.v["buffer/empty"]=False
        self._reset_fps(self._out_fps_calc,"fps/out")
        self._last_emitted_time=None
    def _update_fps(self, fps_calc, key, nframes):
        t=time.time()
        if fps_calc[0] is None:
            fps_calc[0]=t
        else:
            fps_calc[1]+=nframes
            if t-fps_calc[0]>self.fps_period:
                dt=t-fps_calc[0]
                self.v[key]=fps_calc[1]/dt
                fps_calc[:]=[t,0]
    def _reset_fps(self, fps_calc, key):
        fps_calc[:]=[None,0]
        self.v[key]=0

    def enable(self, enabled=True):
        """Enable or disable the slowdown"""
        if enabled!=self.v["enabled"]:
            self._reset()
            self.v["enabled"]=enabled
    def setup_slowdown(self, target_fps, buffer_size):
        """
        Setup slowdown parameters.

        Arg:
            target_fps: target output FPS
            buffer_size: size of the slowdown buffer
        """
        if buffer_size!=self.buffer_size:
            self._reset()
        self.buffer_size=buffer_size
        self.target_fps=target_fps

    def _emit_frames(self):
        t=time.time()
        if self._last_emitted_time is None:
            self._last_emitted_time=t
            return
        nframes=int((t-self._last_emitted_time)*self.target_fps)
        if nframes>0:
            while nframes>0 and self.frames_buffer:
                if self.frames_buffer[0].nframes()>nframes:
                    out_msg=self.frames_buffer[0].copy()
                    out_msg.cut_to_size(nframes)
                    self.frames_buffer[0].cut_to_size(self.frames_buffer[0].nframes()-nframes,from_end=True)
                else:
                    out_msg=self.frames_buffer.pop(0)
                nframes_out=out_msg.nframes()
                nframes-=nframes_out
                self.v["buffer/used"]+=nframes_out
                self._update_fps(self._out_fps_calc,"fps/out",nframes_out)
                self.send_multicast(dst="any",tag=self.tag_out,value=out_msg)
            if not self.frames_buffer and self.v["buffer/filled"]==self.buffer_size:
                self.v["buffer/empty"]=True
            self._last_emitted_time=t

    def set_output_period(self, period=None):
        """
        Set the period of the display frame generation.
        
        If ``None``, output on every input frame message.
        """
        self.v["output_period"]=period
        self.change_job_period("output_frame",1. if period is None else period)
    def output_frame(self):
        if self.v["output_period"] is not None:
            self._emit_frames()
    def process_input_frames(self, src, tag, msg):  # pylint: disable=unused-argument
        """Process multicast message with input frames"""
        self._update_fps(self._in_fps_calc,"fps/in",msg.nframes())
        msg=msg.copy(mid=None)
        if not self.v["enabled"]:
            self.send_multicast(dst="any",tag=self.tag_out,value=msg)
            return
        if self.v["buffer/filled"]<self.buffer_size:
            self.frames_buffer.append(msg.copy(source=self.name))
            if msg.nframes()>self.buffer_size-self.v["buffer/filled"]:
                self.frames_buffer[-1].cut_to_size(self.buffer_size-self.v["buffer/filled"])
            self.v["buffer/filled"]+=self.frames_buffer[-1].nframes()
        if self.v["output_period"] is None:
            self._emit_frames()





class BackgroundSubtractionThread(controller.QTaskThread):
    """
    Frame background subtraction thread: receives frame streams and re-emits individual frames after background subtraction.

    Not all frames are re-emitted, so the stream is generally only useful for display.

    Setup args:
        - ``src``: name of the source thread (usually, a camera)
        - ``tag_in``: receiving multicast tag (for the source multicast)
        - ``tag_out``: emitting multicast tag (for the multicast emitted by the processor) for frames intended to be shown;
            by default, ``tag_in+"/show"``

    Multicasts:
        - ``<tag_out>``: emitted with background-subtracted frames; emitted with the maximal period controlled by the :meth:`set_output_period`,
            or on every input message if ``output_period`` is ``None``

    Variables:
        - ``enabled``: whether processing is enabled (if disabled, the display frame is emitted without any background subtraction)
        - ``overridden``: whether the thread is overridden (if it is, the display frame message is not emitted at all)
        - ``method``: subtraction method: either ``'snapshot"``, or ``"running"``
        - ``output_period``: maximal period for outputting the processed frame; if ``None``, output on every input message
        - ``snapshot/parameters``: parameters of the snapshot background subtraction: ``"count"`` for number of frames to combine for the background,
            ``"mode"`` for the combination mode (``"min"``, ``"mean"``, etc.), ``"dtype"`` for the final dtype, ``"offset"`` to enable or disable background offset
        - ``snapshot/grabbed``: number of grabbed frames in the snapshot background buffer
        - ``snapshot/background``: status of the snapshot background: ``"frame"`` for the final frame and ``"offset"`` for the final offset,
            ``"buffer"`` for the whole background buffer, ``"state"`` for the buffer state, and ``"saving"`` for the saving method;
            state can be ``"none"`` (none acquired), ``"acquiring"`` (accumulation in progress), ``"valid"`` (acquired and valid), or ``"wrong_size"`` (size mismatch);
            saving method can be  ``"none"`` (don't save background), ``"only_bg"`` (only save background frame), or ``"all"`` (save background + all comprising frames).
        - ``running/parameters``: parameters of the snapshot background subtraction: ``"count"`` for number of frames to combine for the background,
            ``"mode"`` for the combination mode (``"min"``, ``"mean"``, etc.), ``"dtype"`` for the final dtype, ``"offset"`` to enable or disable background offset
        - ``running/grabbed``: number of grabbed frames in the running background buffer
        - ``running/background``: status of the running background: ``"frame"`` for the final frame and ``"offset"`` for the final offset

    Commands:
        - ``setup_snapshot_subtraction``: setup snapshot background calculation parameters
        - ``grab_snapshot_background``: initiate snapshot background grab
        - ``setup_snapshot_saving``: setup snapshot background saving method
        - ``setup_running_subtraction``: setup parameters for the running background subtraction
        - ``setup_subtraction_method``: set the subtraction method (running or snapshot) and whether the subtraction is enabled at all
        - ``set_output_period``: set the period of output frames generation
    """
    TStoredFrame=collections.namedtuple("TStoredFrame",["frame","index","info","status_line","metainfo"])
    def setup_task(self, src, tag_in, tag_out=None):  # pylint: disable=arguments-differ
        self.frames_src=stream_manager.StreamSource(builder=stream_message.FramesMessage,use_mid=False)
        self.subscribe_commsync(self.process_input_frames,srcs=src,tags=tag_in,limit_queue=20,on_full_queue="skip_oldest")
        self.tag_out=tag_out or tag_in+"/show"
        self.v["enabled"]=False
        self.v["overridden"]=False
        self.v["method"]="snapshot"
        self.last_frame=self.TStoredFrame(None,None,None,None,None)
        self._new_show_frame=False
        self.snapshot_buffer=[]
        self._snapshot_frame_offset=0
        self.v["snapshot/parameters"]={"count":1,"step":1,"mode":"mean","dtype":None,"offset":False}
        self.v["snapshot/grabbed"]=0
        self.v["snapshot/background/frame"]=None
        self.v["snapshot/background/offset"]=None
        self.v["snapshot/background/buffer"]=None
        self.v["snapshot/background/state"]="none"
        self.v["snapshot/background/saving"]="none"
        self.running_buffer=[]
        self._running_frame_offset=0
        self.v["running/parameters"]={"count":1,"step":1,"mode":"mean","dtype":None,"offset":False}
        self.v["running/grabbed"]=0
        self.v["running/background/frame"]=None
        self.v["running/background/offset"]=None
        self.status_line_policy="duplicate"
        self.add_command("setup_snapshot_subtraction")
        self.add_command("grab_snapshot_background")
        self.add_command("setup_snapshot_saving")
        self.add_command("setup_running_subtraction")
        self.add_command("setup_subtraction_method")
        self.add_command("set_output_period")
        self.v["output_period"]=None
        self.add_job("output_frame",self.output_frame,1.)

    def _calculate_background(self, buffer, mode, dtype, use_offset):
        if dtype is None:
            dtype="i4" if buffer[0].dtype.kind in "ui" else "f"
        background=filters.decimate_full(buffer,mode,axis=0)
        background=background.astype(dtype)
        status_line=self.last_frame.status_line
        if status_line is not None:
            background=camera_utils.remove_status_line(background,status_line,"zero",copy=False)
        if use_offset:
            offset=np.median(background).astype(dtype)
            if status_line is not None:
                background=camera_utils.remove_status_line(background,status_line,"value",value=offset,copy=False)
        else:
            offset=0
        return background,offset
    def _calculate_snapshot_background(self, buffer):
        par=self.v["snapshot/parameters"]
        background,offset=self._calculate_background(buffer,par["mode"],par["dtype"],par["offset"])
        self.v["snapshot/background/frame"]=background
        self.v["snapshot/background/offset"]=offset
        if self.v["snapshot/background/state"]=="acquiring":
            self.v["snapshot/background/state"]="valid"

    def _update_snapshot_buffer(self, msg):
        """Update snapshot background buffer and calculate the background if the buffer is filled"""
        if self.v["snapshot/background/state"]=="acquiring":
            count=self.v["snapshot/parameters/count"]
            step=self.v["snapshot/parameters/step"]
            if len(self.snapshot_buffer)<count:
                self.snapshot_buffer+=msg.get_frames_stack((count-len(self.snapshot_buffer))*step)[self._snapshot_frame_offset::step]
                if self.snapshot_buffer[0].shape!=self.snapshot_buffer[-1].shape:
                    self.snapshot_buffer=[]
            self.snapshot_buffer=self.snapshot_buffer[:count]
            self.v["snapshot/grabbed"]=len(self.snapshot_buffer)
            if len(self.snapshot_buffer)==count:
                self.v["snapshot/background/buffer"]=self.snapshot_buffer
                self._calculate_snapshot_background(self.snapshot_buffer)
                self.snapshot_buffer=[]
            self._snapshot_frame_offset=(self._snapshot_frame_offset-msg.nframes())%step
    def setup_snapshot_subtraction(self, n=1, mode="mean", step=1, dtype=None, offset=False, update_buffer_count=False):
        """
        Setup snapshot background parameters.

        Args:
            n: number of frames in the buffer
            mode: calculation mode; can be ``"mean"``, ``"median"``, ``"min"``, or ``"max"``
            step: the distance between the frames are taken from the stream to form a background
            dtype: numpy dtype of the final background and the output frames; ``None`` means ``int32`` for integer input frames and ``float`` otherwise
            offset: if ``True``, subtract the median background value from it, so that the background subtracted frames stay roughly in the same
                range as the original; otherwise, keep it the same, which shifts the background subtracted frames range towards zero.
            update_buffer_count: if ``True`` and `n` was changed, cut the buffer down to `n` if it was longer, or initiate grab if it was shorter;
                otherwise, keep the background buffer the same until the grab is explicitly initiated
        """
        new_parameters={"count":n,"step":step,"mode":mode,"dtype":dtype,"offset":offset}
        updated={p for p,v in new_parameters.items() if self.v["snapshot/parameters",p]!=v}
        if not updated:
            return
        self.v["snapshot/parameters"]=new_parameters
        if "step" in updated:
            self.grab_snapshot_background()
            self._snapshot_frame_offset=0
        elif self.v["snapshot/background/frame"] is not None:
            if update_buffer_count:
                buffer=self.v["snapshot/background/buffer"]
                if len(buffer)>=n:
                    buffer=self.v["snapshot/background/buffer"][-n:]
                else:
                    self.grab_snapshot_background()
            if self.v["snapshot/background/frame"] is not None:
                self._calculate_snapshot_background(self.v["snapshot/background/buffer"])
    def grab_snapshot_background(self):
        """Initiate snapshot background acquisition"""
        self.v["snapshot/grabbed"]=0
        self.v["snapshot/background/frame"]=None
        self.v["snapshot/background/state"]="acquiring"
    def setup_snapshot_saving(self, mode):
        """
        Enable snapshot background subtraction and saving
        
        `mode` can be ``"none"`` (don't save background), ``"only_bg"`` (only save background frame), or ``"all"`` (save background + all comprising frames).
        """
        self.v["snapshot/background/saving"]=mode
    def get_background_to_save(self):
        """Get the background to save, taking saving parameters into account"""
        enabled=self._is_enabled() and (self.v["method"]=="snapshot")
        background=self.v["snapshot/background"]
        snapshot_background=background["frame"]
        background_saving=background["saving"] if enabled else "none"
        if background_saving=="none" or snapshot_background is None:
            return None
        else:
            return [snapshot_background]+(background["buffer"] if background_saving=="all" else [])

    def _update_running_buffer(self, msg):
        count=self.v["running/parameters/count"]
        step=self.v["running/parameters/step"]
        self._running_frame_offset=(self._running_frame_offset-msg.nframes())%step
        # need to take one extra frame, since the last frame in the buffer shouldn't be subtracted
        updated_frames=msg.get_frames_stack((count+1)*step,reverse=True)[step-self._running_frame_offset-1::step]
        if self.running_buffer and updated_frames and self.running_buffer[0].shape!=updated_frames[0].shape:
            self.running_buffer=[]
        if len(updated_frames)==count+1:
            self.running_buffer=updated_frames
        else:
            self.running_buffer=updated_frames+self.running_buffer[:count+1-len(updated_frames)]
        self.v["running/grabbed"]=max(len(self.running_buffer)-1,0)
    def setup_running_subtraction(self, n=1, mode="mean", step=1, dtype=None, offset=False):
        """
        Setup running background parameters.

        Args:
            n: number of frames in the buffer
            mode: calculation mode; can be ``"mean"``, ``"median"``, ``"min"``, or ``"max"``
            step: the distance between the frames are taken from the stream to form a background
            dtype: numpy dtype of the final background and the output frames; ``None`` means ``int32`` for integer input frames and ``float`` otherwise
            offset: if ``True``, subtract the median background value from it, so that the background subtracted frames stay roughly in the same
                range as the original; otherwise, keep it the same, which shifts the background subtracted frames range towards zero.
        """
        step_updated=self.v["running/parameters/step"]!=step
        self.v["running/parameters"]={"count":n,"step":step,"mode":mode,"dtype":dtype,"offset":offset}
        if step_updated:
            self.running_buffer=[]
            self._running_frame_offset=0
    
    def setup_subtraction_method(self, method=None, enabled=None, overridden=None):
        """
        Set the subtraction method, whether the background subtraction is enabled, and whether it is overridden.

        Values set to ``None`` are unchanged.
        """
        if method is not None:
            if method not in {"snapshot","running"}:
                raise ValueError("unrecognized subtraction method: {}".format(method))
            self.v["method"]=method
        if enabled is not None:
            self.v["enabled"]=enabled
        if overridden is not None:
            self.v["overridden"]=overridden
    def _is_enabled(self):
        return self.v["enabled"] and not self.v["overridden"]

    def set_output_period(self, period=None):
        """
        Set the period of the display frame generation.
        
        If ``None``, output on every input frame message.
        """
        self.v["output_period"]=period
        self.change_job_period("output_frame",1. if period is None else period)

    def process_frame(self, frame, status_line=None):
        """
        Process a frame (or stack of frames).

        `status_line` is a status line descriptor (defined in :class:`FramesMessage`)
        """
        method=self.v["method"]
        enabled=self._is_enabled()
        background,offset=None,None
        if self.v["snapshot/background/frame"] is not None:
            if self.v["snapshot/background/frame"].shape!=frame.shape:
                self.v["snapshot/background/state"]="wrong_size"
            else:
                self.v["snapshot/background/state"]="valid"
                if enabled and method=="snapshot":
                    background,offset=self.v["snapshot/background/frame"],self.v["snapshot/background/offset"]
        if enabled and method=="running":
            par=self.v["running/parameters"]
            if len(self.running_buffer)==par["count"]+1:
                background,offset=self._calculate_background(self.running_buffer[1:],par["mode"],par["dtype"],par["offset"])
                if background.shape!=frame.shape:
                    background,offset=None,None
            self.v["running/background/frame"]=background
            self.v["running/background/offset"]=offset
        if background is not None:
            frame=frame-(background-offset)
        if status_line is not None:
            frame=camera_utils.remove_status_line(frame,status_line,policy=self.status_line_policy)
        return frame

    def output_frame(self):
        """Process and emit new frame"""
        if self._new_show_frame and not self.v["overridden"]:
            show_frame=self.process_frame(self.last_frame.frame,status_line=self.last_frame.status_line)
            self.send_multicast(dst="any",tag=self.tag_out,value=self.frames_src.build_message(show_frame,self.last_frame.index,[self.last_frame.info],
                source=self.name,metainfo=self.last_frame.metainfo))
        self._new_show_frame=False

    def process_input_frames(self, src, tag, msg):   # pylint: disable=unused-argument
        """Process multicast message with input frames"""
        if self.frames_src.receive_message(msg):
            self._snapshot_frame_offset=self._running_frame_offset=0
        self.last_frame=self.TStoredFrame(msg.last_frame(),msg.last_frame_index(),msg.last_frame_info(),msg.metainfo.get("status_line"),msg.metainfo.copy())
        self._update_running_buffer(msg)
        self._update_snapshot_buffer(msg)
        if self.v["output_period"] is None:
            self._new_show_frame=True
            self.output_frame()
        else:
            self._new_show_frame=True