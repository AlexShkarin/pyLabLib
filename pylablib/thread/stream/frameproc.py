# from pylablib.aux_libs.gui import helpers

from ...core.thread import controller
from ...core.utils import dictionary
from ...core.dataproc import filters, image

from . import framestream

import numpy as np
import time

_depends_local=["...core.thread.controller"]

########## Frame processing ##########

class FramePreprocessorThread(controller.QTaskThread):
    """
    Frame preprocessor thread: receives frames and re-emit them after some simple preprocessing (binning in time or space).

    Setup args:
        src: name of the source thread (usually, a camera)
        tag_in: receiving announcement tag (for the source announcement)
        tag_out: emitting announcement tag (for the announcement emitted by the processor)

    Signals:
        ``<tag_out>``: emitted with pre-processed frames

    Variables:
        ``bin_params``: full binning parameters: tuple ``(spat_bin, spat_bin_mode, time_bin, time_bin_mode)``
        ``result_type``: resulting frames type (see :meth:`setup_binning` for parameters)
        ``enabled``: indicates whether binning has been enabled

    Commands:
        enable_binning: enable or disable the binning
        setup_binning: setup binning parameters
    """
    def setup_task(self, src, tag_in, tag_out=None):
        self.subscribe_commsync(self.process_announcement,srcs=src,dsts="any",tags=tag_in,limit_queue=1,on_full_queue="wait",priority=-1)
        self.tag_out=tag_out or tag_in
        self.spat_bin=(1,1)
        self.spat_bin_mode="skip"
        self.time_bin=1
        self.time_bin_mode="skip"
        self._setup_bin_params()
        self.acc_frame=None
        self.acc_frame_num=0
        self.result_type=None
        self["enabled"]=False
        self.add_command("setup_binning")
        self.add_command("enable_binning")

    def _setup_bin_params(self):
        self["bin_params"]=(self.spat_bin,self.spat_bin_mode,self.time_bin,self.time_bin_mode)
        self["result_type"]=self.result_type
    def enable_binning(self, enabled=True):
        """Enable or disable the binning"""
        self["enabled"]=enabled
    def setup_binning(self, spat_bin, spat_bin_mode, time_bin, time_bin_mode, result_type=None):
        """
        Setup binning parameters.

        Arg:
            spat_bin: tuple ``(i_bin, j_bin)`` with the binning factors along the two spatial axes.
            spat_bin_mode: mode for spatial binning; can be ``"skip"`` (simply take every n'th pixel), ``"sum"``, ``"min"``, ``"max"``, or ``"mean"``.
            time_bin: binning factor for the time axis
            time_bin_mode: same as `spat_bin_mode`, but for the time axis
            result_type: if not ``None``, the resulting frames are converted to the given type;
                otherwise, they are converted into the same type as the source frames;
                note that if the source type is integer and binning mode is ``"mean"`` or ``"sum"``, some information might be lost through rounding or integer overflow;
                for the purposes of ``"mean"`` and ``"sum"`` binning the frames are always temporarily converted to float
        """
        if spat_bin!=self.spat_bin or spat_bin_mode!=self.spat_bin_mode or time_bin!=self.time_bin or time_bin_mode!=self.time_bin_mode:
            self._clear_buffer()
        self.spat_bin=spat_bin
        self.spat_bin_mode=spat_bin_mode
        self.time_bin=time_bin
        self.time_bin_mode=time_bin_mode
        self.result_type=result_type
        self._setup_bin_params()

    def _clear_buffer(self):
        self.acc_frame=None
        self.acc_frame_num=0
    def _bin_spatial(self, frames, status_line):
        if self.spat_bin!=(1,1):
            sl=framestream.extract_status_line(frames,status_line,copy=False)
            if self.spat_bin[0]>1:
                frames=filters.decimate(frames,self.spat_bin[0],dec_mode=self.spat_bin_mode,axis=1)
            if self.spat_bin[1]>1:
                frames=filters.decimate(frames,self.spat_bin[1],dec_mode=self.spat_bin_mode,axis=2)
            if sl is not None:
                sl=sl[:,:frames.shape[1],:frames.shape[2]]
                frames=framestream.insert_status_line(frames,status_line,sl,copy=(self.spat_bin_mode=="skip"))
        return frames
    def _decimate_with_status_line(self, frames, dec_mode, status_line):
        res=filters.decimate(frames,self.time_bin,dec_mode=dec_mode,axis=0)
        if dec_mode!="skip" and status_line is not None:
            binned_n=self.time_bin*(len(frames)//self.time_bin)
            sl=framestream.extract_status_line(frames[:binned_n:self.time_bin],status_line,copy=False)
            res=framestream.insert_status_line(res,status_line,sl,copy=False)
        return res
    def _decimate_full_with_status_line(self, frames, dec_mode, status_line):
        res=filters.decimate_full(frames,dec_mode)
        if dec_mode!="skip" and status_line is not None:
            sl=framestream.extract_status_line(frames[0],status_line,copy=False)
            res=framestream.insert_status_line(res,status_line,sl,copy=False)
        return res
    def _update_buffer(self, frames, status_line):
        res_dtype=frames.dtype if self.result_type is None else self.result_type
        frames=self._bin_spatial(frames,status_line)
        if self.time_bin>1:
            if self.acc_frame is not None and frames.shape[1:]!=self.acc_frame.shape:
                self._clear_buffer()
            binned_frames=[]
            time_dec_mode=self.time_bin_mode if self.time_bin_mode!="mean" else "sum"
            if time_dec_mode=="sum":
                frames=frames.astype("float")
            if self.acc_frame is not None and self.acc_frame_num+len(frames)>=self.time_bin: # complete current chunk
                chunk=frames[:self.time_bin-self.acc_frame_num]
                frames=frames[self.time_bin-self.acc_frame_num:]
                chunk=filters.decimate_full(chunk,time_dec_mode) if len(chunk)>1 else chunk[0]
                if self.acc_frame is not None:
                    chunk=self._decimate_full_with_status_line([self.acc_frame,chunk],time_dec_mode,status_line)
                binned_frames.append(chunk)
                self._clear_buffer()
            if len(frames):
                binned_frames+=list(self._decimate_with_status_line(frames,time_dec_mode,status_line)) # decimate all complete chunks
            frames_left=len(frames)%self.time_bin
            if frames_left: # update accumulator
                chunk=frames[-frames_left:]
                chunk=self._decimate_full_with_status_line(chunk,time_dec_mode,status_line) if len(chunk)>1 else chunk[0]
                if self.acc_frame is not None:
                    chunk=self._decimate_full_with_status_line([self.acc_frame,chunk],time_dec_mode,status_line)
                self.acc_frame=chunk
                self.acc_frame_num+=frames_left
            frames=np.asarray(binned_frames)
            if self.time_bin_mode=="mean" and binned_frames:
                if status_line is None:
                    frames/=self.time_bin
                else:
                    sl=framestream.extract_status_line(frames,status_line,copy=True)
                    frames/=self.time_bin
                    frames=framestream.insert_status_line(frames,status_line,sl,copy=False)
        frames=frames.astype(res_dtype)
        return frames
            
    def process_announcement(self, src, tag, msg):
        """Process frame announcement from the camera"""
        if not self["enabled"]:
            self.send_announcement(dst="any",tag=self.tag_out,value=msg)
            return
        processed=[]
        if msg.first_frame_index()==0:
            self._clear_buffer()
        for idx,chunk in zip(msg.indices,msg.frames):
            frames_in_acc=self.acc_frame_num
            proc_chunk=self._update_buffer(chunk,msg.status_line)
            if len(proc_chunk):
                processed.append((idx-frames_in_acc,proc_chunk)) # actual time bin chunk started `frames_in_acc` before
        if processed:
            indices,frames=list(zip(*processed))
            msg=msg.copy(frames=frames,indices=indices,source="preprocessor",step=self.time_bin)
            self.send_announcement(dst="any",tag=self.tag_out,value=msg)





class FrameSlowdownThread(controller.QTaskThread):
    """
    Frame slowdown thread: receives frames and re-emit them with throttling FPS.

    Setup args:
        src: name of the source thread (usually, a camera)
        tag_in: receiving announcement tag (for the source announcement)
        tag_out: emitting show announcement tag (for the announcement emitted by the processor)

    Signals:
        ``<tag_out>``: emitted with slowed frames

    Variables:
        ``buffer/filled``: the number of frames in the buffer
        ``buffer/used``: the number of frames in the buffer which have already meen shown
        ``buffer/empty``: indicates whether the buffer has already been completely filled and used
            (in this case further frames are not shown, and the processor must be stopped)
        ``enabled``: indicate whether the slowdown is on
        ``fps/in``: FPS of the incoming stream
        ``fps/out``: FPS of the outgoing stream

    Commands:
        enable_slowdown: enable or disable slowdown mode
        setup_slowdown: setup slowdown parameters
    """
    def setup_task(self, src, tag_in, tag_out=None):
        self.subscribe_commsync(self.process_announcement,srcs=src,dsts="any",tags=tag_in,limit_queue=1)
        self.tag_out=tag_out or tag_in
        self.frames_buffer=[]
        self.buffer_size=1
        self["buffer/filled"]=0
        self["buffer/used"]=0
        self["buffer/empty"]=False
        self["enabled"]=False
        self._last_emitted_time=None
        self._in_fps_calc=[None,0]
        self._out_fps_calc=[None,0]
        self.fps_period=1.
        self["fps/in"]=0
        self["fps/out"]=0
        self.add_command("enable_slowdown")
        self.add_command("setup_slowdown")

    def _reset(self):
        self.frames_buffer=[]
        self["buffer/filled"]=0
        self["buffer/used"]=0
        self["buffer/empty"]=False
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
                self[key]=fps_calc[1]/dt
                fps_calc[:]=[t,0]
    def _reset_fps(self, fps_calc, key):
        fps_calc[:]=[None,0]
        self[key]=0

    def enable_slowdown(self, enabled=True):
        """Enable or disable the slowdown"""
        if enabled!=self["enabled"]:
            self._reset()
            self["enabled"]=enabled
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
            
    def process_announcement(self, src, tag, msg):
        """Process frame announcement from the camera"""
        self._update_fps(self._in_fps_calc,"fps/in",msg.nframes())
        if not self["enabled"]:
            self.send_announcement(dst="any",tag=self.tag_out,value=msg)
            return
        if self["buffer/filled"]<self.buffer_size:
            self.frames_buffer.append(msg.copy(source="slowdown"))
            if msg.nframes()>self.buffer_size-self["buffer/filled"]:
                self.frames_buffer[-1].cut_to_size(self.buffer_size-self["buffer/filled"])
            self["buffer/filled"]+=self.frames_buffer[-1].nframes()
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
                    self.frames_buffer[0].cut_to_size(self.frames_buffer[0].nframes()-nframes,reversed=True)
                else:
                    out_msg=self.frames_buffer.pop(0)
                nframes_out=out_msg.nframes()
                nframes-=nframes_out
                self["buffer/used"]+=nframes_out
                self._update_fps(self._out_fps_calc,"fps/out",nframes_out)
                self.send_announcement(dst="any",tag=self.tag_out,value=out_msg)
            if not self.frames_buffer and self["buffer/filled"]==self.buffer_size:
                self["buffer/empty"]=True
            self._last_emitted_time=t






# ##### Camera channel calculation #####

# class CamChannelAccumulator(controller.QTaskThread):
#     """
#     Camera channel accumulator.

#     Receives frames from a source, calculate time series and accumulates in a table together with the frame indices.

#     Setup args:
#         src: name of the source thread (usually, a camera)
#         tag: receiving announcement tag (for the source announcement)
#         settings: dictionary with the accumulator settings

#     Commands:
#         enable: enable or disable accumulation
#         add_source: add a frame source
#         select_source: select one of frame sources for calculation
#         setup_processing: setup processing paramters
#         setup_roi: setup averaging ROI
#         reset_roi: reset averaging ROI to the whole image
#         get_data: get the accumulated data as a dictionary of 1D numpy arrays
#         reset: clear the accumulation table
#     """
#     def setup_task(self, settings=None):
#         self.settings=settings or {}
#         self.frame_channels=["idx","mean"]
#         self.memsize=self.settings.get("memsize",100000)
#         self.table_accum=helpers.TableAccumulator(channels=self.frame_channels,memsize=self.memsize)
#         self.enabled=False
#         self.current_source=None
#         self.sources={}
#         self.skip_count=1
#         self._skip_accum=0
#         self.reset_time=time.time()
#         self.roi=None
#         self.roi_enabled=False
#         self._last_roi=None
#         self.add_command("enable")
#         self.add_command("add_source")
#         self.add_command("select_source")
#         self.add_command("setup_processing")
#         self.add_command("setup_roi")
#         self.add_command("reset_roi")
#         self.add_command("get_data")
#         self.add_command("reset")

#     def enable(self, enabled=True):
#         """Enable or disable trace accumulation"""
#         self.enabled=enabled
#         self._skip_accum=0
#     def setup_processing(self, skip_count=1):
#         """
#         Setup processing parameters.

#         Args:
#             skip_count: the accumulated values are calculated for every `skip_count` frame.
#         """
#         self.skip_count=skip_count
#         self._skip_accum=0

#     TSource=collections.namedtuple("TSource",["src","tag","kind","sync"])
#     def add_source(self, name, src, tag, sync=False, kind="raw"):
#         """
#         Add a frame source.

#         Args:
#             name: source name (used for switching source)
#             src: frame announcement source
#             tag: frame announcement tag
#             sync: if ``True``, the subscription is synchronized to the source (i.e, if processing takes too much time, the frame source waits);
#                 otherwise, the subscription is not synchronized (if processing takes too much time, frames are skipped)
#             kind: source kind; can be ``"raw"`` (plotted vs. frame index, reset on source restart), ``"show"`` (plotted vs. time, only reset explicitly),
#                 or ``"points"`` (source sends directly a dictionary of trace values rather than frames)
#         """
#         self.sources[name]=self.TSource(src,tag,kind,sync)
#         callback=lambda s,t,v: self.process_source(s,t,v,source=name)
#         if sync:
#             self.subscribe_commsync(callback,srcs=src,dsts="any",tags=tag,limit_queue=2,on_full_queue="wait")
#         else:
#             self.subscribe_commsync(callback,srcs=src,dsts="any",tags=tag,limit_queue=10)
#     def select_source(self, name):
#         """Select a source with a given name"""
#         if self.current_source!=name:
#             self.reset()
#             self.current_source=name
#             if self.sources[name].kind in {"raw","show"}:
#                 self.table_accum.change_channels(self.frame_channels)
#             else:
#                 self.table_accum.change_channels([])
    
#     def setup_roi(self, center=None, size=None, enabled=True):
#         """
#         Setup averaging ROI parameters.

#         `center` and `size` specify ROI parameters (if ``None``, keep current values).
#         `enabled` specifies whether ROI is applied for averaging (``enabled==True``), or the whole frame is averaged (``enabled==False``)
#         Return the new ROI (or ``None`` if no ROI can be specified).
#         """
#         if center is not None or size is not None:
#             if center is None and self.roi is not None:
#                 center=self.roi.center()
#             if size is None and self.roi is not None:
#                 size=self.roi.size()
#             if center is not None and size is not None:
#                 self.roi=image.ROI.from_centersize(center,size)
#         self.roi_enabled=enabled
#         return self.roi
#     def reset_roi(self):
#         """
#         Reset ROI to the whole image

#         Return the new ROI (or ``None`` if no frames have been acquired, so no ROI can specified)
#         """
#         self.roi=self._last_roi
#         return self.roi
#     def process_frame(self, value, kind):
#         """Process raw frames data"""
#         if not value.has_frames():
#             return
#         if value.first_frame_index()==0 and kind=="raw":
#             self.reset()
#         for i,f in zip(value.indices,value.frames):
#             if len(f)+self._skip_accum>=self.skip_count:
#                 start=self.skip_count-self._skip_accum-1
#                 calc_frames=f[start::self.skip_count]
#                 calc_roi=self.roi if (self.roi and self.roi_enabled) else image.ROI(0,calc_frames.shape[1],0,calc_frames.shape[2])
#                 sums,area=image.get_region_sum(calc_frames,calc_roi.center(),calc_roi.size())
#                 if value.status_line:
#                     sl_roi=get_status_line_roi(calc_frames,value.status_line)
#                     sl_roi=image.ROI.intersect(sl_roi,calc_roi)
#                     if sl_roi:
#                         sl_sums,sl_area=image.get_region_sum(calc_frames,sl_roi.center(),sl_roi.size())
#                         sums-=sl_sums
#                         area-=sl_area
#                 means=sums/area if area>0 else sums
#                 if kind=="raw":
#                     x_axis=np.arange(i+start,i+len(f)*value.step,value.step*self.skip_count)
#                 else:
#                     x_axis=[time.time()-self.reset_time]*len(means)
#                 self.table_accum.add_data([x_axis,means])
#             self._skip_accum=(self._skip_accum+len(f))%self.skip_count
#         shape=value.first_frame().shape
#         self._last_roi=image.ROI(0,shape[0],0,shape[1])
#     def process_points(self, value):
#         """Process trace dictionary data"""
#         table={}
#         min_len=None
#         for k in value:
#             v=value[k]
#             if not isinstance(v,(list,np.ndarray)):
#                 v=[v]
#             table[k]=v
#             min_len=len(v) if min_len is None else min(len(v),min_len)
#         if min_len>0:
#             for k in table:
#                 table[k]=table[k][:min_len]
#             if "idx" not in table:
#                 table["idx"]=[time.time()-self.reset_time]*min_len
#             if not self.table_accum.channels:
#                 self.table_accum.change_channels(list(table.keys()))
#             self.table_accum.add_data(table)
#     def process_source(self, src, tag, value, source):
#         """Receive the source data (frames or traces), process and add to the accumulator table"""
#         if not self.enabled or source!=self.current_source:
#             return
#         kind=self.sources[source].kind
#         if kind in {"raw","show"}:
#             self.process_frame(value,kind)
#         elif kind=="points":
#             self.process_points(value)
#     def get_data(self, maxlen=None):
#         """
#         Get the accumulated data as a dictionary of 1D numpy arrays.
        
#         If `maxlen` is specified, get at most `maxlen` datapoints from the end.
#         """
#         return self.table_accum.get_data_dict(maxlen=maxlen)
#     def reset(self):
#         """Clear all data in the table"""
#         self.table_accum.reset_data()
#         self._skip_accum=0
#         self.reset_time=time.time()

