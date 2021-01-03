from pylablib.aux_libs.gui import helpers
from pylablib.core.gui.qt.thread import controller
from pylablib.core.dataproc import image
from pylablib.core.utils import dictionary

import time
import numpy as np
import collections

from ..devthread.constants import device_sync_timeout
from . import framestream




########## Data stream combining / accumulating / transforming ##########

class StreamFormer(helpers.StreamFormerThread):
    """
    Specific stream former thread which is set up based on the settings file.

    Remote calls:
        configure_daq_channels: turn DAQ channels on or off, or reset their queue
        configure_cam_channels: turn camera channels on or off, or reset their queue
        pause: pause signal sending
        reset: reset the channels and the acquired rows
    
    Signals:
        point: sent when a new data block is acquired; value is a dictionary of columns
        reset: sent when the stream former is reset
    """
    def get_internal_channel(self, name):
        """Internal channel sources"""
        if name=="timestamp":
            return time.time()
        if name=="idx":
            self.idx+=1
            return self.idx-1
        if name=="elapsed_time":
            return time.time()-self.start_time
    def _internal_channel_source(self, name):
        return lambda : self.get_internal_channel(name)
    
    def setup_custom_channel(self, channel):
        pass

    def _parse_daq(self, src, tag, value):
        return dict([ (name,value[kind][i]) for (name,kind,i) in self.daq_channels ])
    def _parse_frame(self, src, tag, value):
        return value.get_frames_stack(add_indices=True)
    def _parse_cam(self, src, tag, value):
        cam_name=tag.split("/",maxsplit=1)[1]
        if cam_name in self.cam_channels:
            return dict([ (name,value[i]) for (name,i) in self.cam_channels[cam_name] ])
        return {}
    _max_queue_len=2000
    def setup(self, settings, daq_thread_name="daq", cam_channel_thread_name="camera_channels"):
        """
        Setup all the channels based on the settings file.

        `daq_thread_name` and `cam_channel_thread_name` specify respectively :class:`.NIDAQThread` and :class:`CamChannelGenerator` threads
        used as data sources (since their signals need to be parsed and processed in a special way)
        """
        self.add_command("configure_daq_channels")
        self.add_command("configure_cam_channels")
        self.add_command("reset")
        self.add_command("pause")

        self.idx=0
        self.start_time=time.time()
        self.daq_channels=[]
        self.cam_channels={}
        daq=controller.get_controller(daq_thread_name)
        daq.sync_exec("run",timeout=device_sync_timeout)
        daq_channels=(daq["channels/input/combined/names"],daq["channels/special/names"],daq["channels/external/names"])
        channel_settings=settings["streaming/channels"]
        for idx in channel_settings.keys(ordered=True): # setup all channels
            ch=channel_settings[idx]
            name=ch["name"]
            ch_type=ch["source/type"]
            enabled=ch.get("start_enabled",True)
            required=ch.get("start_sync","auto")
            background=ch.get("background",False)
            expand_list=ch.get("expand_list",False)
            default=ch.get("default",0)
            if ch_type=="custom": # custom channel (currently not used)
                self.setup_custom_channel(ch)
            elif ch_type=="device_parameter": # channel based on a thread variable of a device thread (e.g., temperature)
                def make_getter(dev, par):
                    return lambda: dev[par]
                dev_ctl=controller.get_controller(ch["source/device"],timeout=device_sync_timeout)
                dev_ctl.sync_exec("run",timeout=device_sync_timeout)
                getter=make_getter(dev_ctl,ch["source/parameter"])
                self.add_channel(name,func=getter,enabled=enabled,max_queue_len=self._max_queue_len)
            elif ch_type=="signal": # channel based on a signal from a device thread (e.g., camera frames)
                dev_ctl=controller.get_controller(ch["source/device"],timeout=device_sync_timeout)
                dev_ctl.sync_exec("run",timeout=device_sync_timeout)
                self.add_channel(name,enabled=enabled,required=required,background=background,max_queue_len=self._max_queue_len,default=default,expand_list=expand_list)
                signal_kind=ch.get("source/signal_kind","simple")
                parse=self._parse_frame if signal_kind=="frame" else None
                self.subscribe_source(name,srcs=ch["source/device"],tags=ch["source/signal"],parse=parse)
            elif ch_type=="internal": # internal channels (index, timestamp, elapsed time)
                int_chan=ch["source/internal_channel"]
                pure_func=(int_chan!="idx")
                self.add_channel(name,func=self._internal_channel_source(int_chan),enabled=enabled,max_queue_len=self._max_queue_len,pure_func=pure_func)
            elif ch_type=="daq": # daq channel (daq signal is already subscribed, here just add channel description)
                chan_kinds={"input":0,"special":1,"external":2}
                chan_kind=chan_kinds.get(ch.get("source/channel_kind","input"),0)
                chan_name=ch["source/channel_name"]
                self.daq_channels.append((name,chan_kind,daq_channels[chan_kind].index(chan_name)))
                self.add_channel(name,enabled=enabled,background=background,max_queue_len=self._max_queue_len,expand_list=True)
            elif ch_type=="cam_channel": # camera channel
                cam_name=ch["source/camera"]
                chan_name=ch["source/channel_name"]
                if cam_name not in self.cam_channels:
                    self.cam_channels[cam_name]=[]
                    self.subscribe_source("camera_channels",srcs=cam_channel_thread_name,tags="channel/"+cam_name,parse=self._parse_cam)
                self.cam_channels[cam_name].append((name,chan_name))
                self.add_channel(name,enabled=enabled,max_queue_len=self._max_queue_len,required=ch.get("start_sync",False),
                    background=ch.get("background",False),default=default,expand_list=True)
            else:
                raise ValueError("unrecognized channel type: {}".format(ch_type))
        self.subscribe_source("daq",srcs=daq_thread_name,tags="values/input",parse=self._parse_daq)
        self.subscribe(lambda *_: self._update_block_period(daq,settings),srcs=daq_thread_name,dsts="any",tags="settings/update/streaming")
        
        self._update_block_period(daq,settings)
        self.reset()
        self.pause(False)

    def configure_daq_channels(self, enable=True, required="auto", clear=True):
        """Configure all daq channels (usually, turn on or off)"""
        for name,_ in self.daq_channels:
            self.configure_channel(name,enable=enable,required=required,clear=clear)
    def configure_cam_channels(self, camera=None, enable=True, required="auto", clear=True):
        """Configure all camera channels belogning to the same camera (usually, turn on or off)"""
        if camera is None:
            for camera in self.cam_channels:
                self.configure_cam_channels(camera,enable=enable,required=required,clear=clear)
        else:
            for name,_ in self.cam_channels.get(camera,{}):
                self.configure_channel(name,enable=enable,required=required,clear=clear)

    def _update_block_period(self, daq, settings):
        daq_rate,ext_clk=daq["settings/clock"]
        if "streaming/rate" in settings and not ext_clk:
            point_block_size=daq["settings/streaming/point_block_size"]
            streaming_rate=settings["streaming/rate"]
            self.block_period=int(np.ceil(daq_rate/point_block_size/streaming_rate)) # for high daq rates increase block size to reduce signal rate
        else:
            self.block_period=1
    def on_new_block(self):
        """Overloaded function called every time a new complete block is formed"""
        data=self.pop_data()
        if not self.paused:
            data["Frequency"]=[0. if isinstance(d,str) else d for d in data["Frequency"]] # filter wavemeter ``"over"`` and ``"under"`` entries
            self.send_signal(tag="points",value=data)
    def reset(self):
        """
        Reset the stream former.

        Clear all queues, reset counters, send reset signal (used in :class:`.TableAccumulator`)
        """
        self.idx=0
        self.start_time=time.time()
        self.clear_all()
        self.send_signal(tag="reset")
    
    def pause(self, paused=True):
        self.paused=paused








class CamChannelGenerator(controller.QThreadController):
    """
    Camera channel generator.

    A stream transformer thread which receives signals from cameras and emits signals with 'camera channels'
    (integrated intensity in specified rectangular areas)
    """
    def __init__(self, name=None, settings=None, sources=None):
        controller.QThreadController.__init__(self,name=name,kind="loop")
        self.settings=settings
        self.channel_params=dictionary.Dictionary()
        self.setup_channels()
        self.sources=sources

    def on_start(self):
        controller.QThreadController.on_start(self)
        self.subscribe(self.on_frame,srcs=list(self.sources.keys()),dsts="any",tags="frames/new",limit_queue=10)
    def on_frame(self, src, tag, value):
        """Frame signal processor (calculates channel values and send the signal)"""
        src=self.sources.get(src,src)
        channels=self.get_channels(value.get_frames_stack(),src)
        self.send_signal(tag="channel/"+src,value=channels)

    def setup_channels(self):
        """Setup all channels based on settings"""
        cam_channels=self.settings.get("cam_channels",{})
        for dev in cam_channels:
            for ch in cam_channels[dev]:
                self["roi",dev,ch]=self.channel_params[dev,ch,"roi"]=image.ROI(0,0,0,0)
    @staticmethod
    def get_roi_avg(img, roi):
        """Get average of an image or a stack of images inside a given ROI"""
        img_sum,img_area=image.get_region_sum(img,roi.center(),roi.size())
        if img.ndim>2:
            return list(img_sum/img_area) if np.all(img_area) else [0]*len(img)
        else:
            return img_sum/img_area if img_area else 0
    @controller.remote_call
    def get_channels(self, img, source):
        """Calculated channel values for given image (or array of images) and source (camera thread name)"""
        cam_channels=self.channel_params.get(source,{})
        img=np.asarray(img)
        result={}
        for ch in cam_channels:
            roi=cam_channels[ch,"roi"]
            result[ch]=self.get_roi_avg(img,roi)
        return result

    @controller.remote_call
    def set_roi(self, name, center, size):
        """Set ROI if a channel with a given name"""
        if name in self.channel_params:
            self["roi",name]=self.channel_params[name,"roi"]=image.ROI.from_centersize(center,size)
        else:
            raise ValueError("unrecognized channel: {}".format(name))







# class FrameAverageCalculator:
#     """
#     Calculator and accumulator of average frame values, potentially with ROI.

#     Args:
#         roi: ROI for mean calculation (:class:`.image.ROI` object), or ``"full"`` (use full frame mean)
#         x_source: source for the x-axis; can be ``"index"`` (frame index), or ``"time"`` (time of the incoming frame message)
#         calc_period: preiodicity for frames for which mean is calculated (e.g., with ``calc_period=3`` only every 3rd frame is used)
#         accum_size: size of the trace accumulator; can also be ``None``, which means that no accumulator is used
#     """
#     def __init__(self, roi="full", x_source="index", calc_period=1, accum_size=None):
#         self.calc_period=calc_period
#         self._skip_accum=0
#         self.roi=roi
#         self._last_frame_size=None
#         self.x_source=None
#         self.x_channel="idx"
#         self.setup_accum(accum_size)
#         self.setup_x_source(x_source)

#     def setup_period(self, calc_period):
#         """Set new calc period"""
#         self.calc_period=calc_period
#         self.reset()
#     def setup_roi(self, roi="full"):
#         """Set new ROI"""
#         self.roi=roi
#     def get_last_frame_size(self):
#         """Get size of the last received frame"""
#         return self._last_frame_size
#     def get_fit_roi(self):
#         """
#         Get fit ROI.

#         If ``roi`` is defined, return it; if not (i.e., ``roi=="full"``), return size of the last frame (or ``None``, if no frames have been received)
#         """
#         if self.roi=="full":
#             if self._last_frame_size is not None:
#                 return image.ROI(imax=self._last_frame_size[0],jmax=self._last_frame_size[1])
#             else:
#                 return None
#         return self.roi
#     def setup_accum(self, accum_size):
#         """Set new accumulator size"""
#         self.accum=helpers.TableAccumulator(channels=[self.x_channel,"mean"],memsize=accum_size) if accum_size else None
#     def setup_x_source(self, x_source):
#         """Set new x-axis source"""
#         if x_source not in ["index","time"]:
#             raise ValueError("unrecognized x source: {}".format(x_source))
#         if self.x_source!=x_source:
#             self.x_source=x_source
#             self.reset()

#     def reset(self):
#         """Reset accumulator and internal counters"""
#         self.reset_time=time.time()
#         self._skip_accum=0
#         if self.accum:
#             self.accum.reset_data()
#     def __call__(self, frames):
#         """
#         Receive new frames message.

#         `frames` is :class:`.FramesMessage` object
#         """
#         if not frames.has_frames():
#             return
#         if frames.first_frame_index()==0 and self.x_source=="index":
#             self.reset()
#         new_points=[]
#         for i,f in zip(frames.indices,frames.frames):
#             if len(f)+self._skip_accum>=self.calc_period:
#                 start=self.calc_period-self._skip_accum-1
#                 calc_frames=f[start::self.calc_period]
#                 calc_roi=self.roi if self.roi!="full" else image.ROI(0,calc_frames.shape[1],0,calc_frames.shape[2])
#                 sums,area=image.get_region_sum(calc_frames,calc_roi.center(),calc_roi.size())
#                 if frames.status_line:
#                     sl_roi=framestream.get_status_line_roi(calc_frames,frames.status_line)
#                     sl_roi=image.ROI.intersect(sl_roi,calc_roi)
#                     if sl_roi:
#                         sl_sums,sl_area=image.get_region_sum(calc_frames,sl_roi.center(),sl_roi.size())
#                         sums-=sl_sums
#                         area-=sl_area
#                 means=sums/area if area>0 else sums
#                 if self.x_source=="index":
#                     x_axis=np.arange(i+start,i+len(f)*frames.step,frames.step*self.calc_period)
#                 else:
#                     x_axis=[time.time()-self.reset_time]*len(means)
#                 new_points.append([x_axis,means])
#             self._skip_accum=(self._skip_accum+len(f))%self.calc_period
#         self._last_frame_size=frames.first_frame().shape
#         if new_points:
#             new_points=np.concatenate(new_points,axis=1)
#             if self.accum:
#                 self.accum.add_data(new_points)
#         else:
#             new_points=np.zeros((2,0))
#         return new_points.T
    
#     def get_data(self, channels=None, maxlen=None, fmt="rows"):
#         """
#         Get accumulated table data.
        
#         Args:
#             channels: list of channels (the two available channels are ``"idx"`` and ``"mean"``)
#             maxlen: maximal column length (if stored length is larger, return last `maxlen` rows)
#             fmt (str): return format; can be ``"rows"`` (list of rows), ``"columns"`` (list of columns), or ``"dict"`` (dictionary of named columns)
#         """
#         if self.accum is None:
#             return None
#         if fmt=="columns":
#             return self.accum.get_data_columns(channels=channels,maxlen=maxlen)
#         elif fmt=="rows":
#             return self.accum.get_data_rows(channels=channels,maxlen=maxlen)
#         elif fmt=="dict":
#             return self.accum.get_data_dict(channels=channels,maxlen=maxlen)
#         else:
#             raise ValueError("unrecognized data format: {}".format(fmt))





# class PointSourceAccumulator:
#     """
#     Accumulator of incoming multi-stream data.

#     Args:
#         channels: channels in the incoming data; can also be ``None``, in which case channels are extracted from the data when it's received
#         x_source: source for the x-axis; can be ``"index"`` (frame index), ``"time"`` (time of the incoming points), or ``"none"`` (no additional x-channel is added)
#         x_channel: name of the added x-channel (by default it's ``"idx"`` with an added index axis; for ``x_source=="none"`` it can be any of the incoming channel names)
#         calc_period: preiodicity for data points which are accumulated (e.g., with ``calc_period=3`` only every 3rd datapoint is used)
#         accum_size: size of the trace accumulator
#         autoupdate_channels: if ``True`` and incoming data channels are different from the stored ones, re-create the accumulator with the new channels;
#             otherwise, keep the accumulator, which ignores extra columns and raises errors if some are missing
#     """
#     def __init__(self, channels=None, x_source="index", x_channel="idx", calc_period=1, accum_size=100000, autoupdate_channels=True):
#         self.calc_period=calc_period
#         self.x_source="none"
#         self.x_channel=x_channel
#         self.autoupdate_channels=autoupdate_channels
#         self.accum=None
#         self.setup_channels(channels)
#         self.accum_size=accum_size
#         self.setup_accum()
#         self.setup_x_source(x_source)

#     def setup_period(self, calc_period):
#         """Set new calculation period"""
#         self.calc_period=calc_period
#         self.reset()
#     def setup_channels(self, channels):
#         """Set new list of channels"""
#         if channels is not None and self.x_source!="none" and self.x_channel not in channels:
#             channels=[self.x_channel]+list(channels)
#         self.channels=channels
#         if self.accum is not None:
#             self.setup_accum()
#     def setup_accum(self, accum_size=None):
#         """
#         Set new accumulator size.
        
#         If the size is ``None``, simply re-create the accumulator with the current channels.
#         """
#         if accum_size is not None:
#             self.accum_size=accum_size
#         if self.channels is not None:
#             self.accum=helpers.TableAccumulator(channels=self.channels,memsize=self.accum_size)
#         else:
#             self.accum=None
#     def setup_x_source(self, x_source):
#         """Set new x-axis source"""
#         if x_source not in ["index","time","none"]:
#             raise ValueError("unrecognized x source: {}".format(x_source))
#         if self.x_source!=x_source:
#             self.x_source=x_source
#             self.reset()

#     def reset(self):
#         """Reset accumulator and internal counters"""
#         self._reset_time=time.time()
#         self._skip_accum=0
#         self._idx_counter=0
#         if self.accum:
#             self.accum.reset_data()
#     def __call__(self, points):
#         """
#         Receive new frames message.

#         `points` is a dictionary of lists or 1D numpy arrays, which contain columns data
#         All lists/arrays should have the same length.
#         """
#         if not points:
#             return
#         k0=list(points)[0]
#         points={k:(v if np.ndim(v)>0 else [v]) for k,v in points.items()}
#         for k,v in points.items():
#             if len(v)!=len(points[k0]):
#                 raise ValueError("columns {} and {} have different length: {} and {}".format(k0,k,len(points[k0]),len(v)))
#         l0=len(points[k0])
#         if self.calc_period>1:
#             points={k:v[self._skip_accum::self.calc_period] for k,v in points.items()}
#             self._skip_accum=(self._skip_accum+l0)%self.calc_period
#         l0=len(points[k0])
#         if self.x_source=="index":
#             points[self.x_channel]=np.arange(self._idx_counter,self._idx_counter+l0)
#             self._idx_counter+=l0
#         elif self.x_source=="time":
#             points[self.x_channel]=[time.time()-self._reset_time]*l0
#         if self.channels is None or (self.autoupdate_channels and set(self.channels)!=set(points)):
#             self.setup_channels(list(points))
#             self.setup_accum()
#         self.accum.add_data(points)
    
#     def get_data(self, channels=None, maxlen=None, fmt="rows"):
#         """
#         Get accumulated table data.
        
#         Args:
#             channels: list of returned channels (if ``None``, return all channels)
#             maxlen: maximal column length (if stored length is larger, return last `maxlen` rows)
#             fmt (str): return format; can be ``"rows"`` (list of rows), ``"columns"`` (list of columns), or ``"dict"`` (dictionary of named columns)
#         """
#         if self.accum is None:
#             return None
#         if fmt=="columns":
#             return self.accum.get_data_columns(channels=channels,maxlen=maxlen)
#         elif fmt=="rows":
#             return self.accum.get_data_rows(channels=channels,maxlen=maxlen)
#         elif fmt=="dict":
#             return self.accum.get_data_dict(channels=channels,maxlen=maxlen)
#         else:
#             raise ValueError("unrecognized data format: {}".format(fmt))





# class PlotManager(controller.QTaskThread):
#     """
#     Thread for controlling and accumulating plotting data.

#     Each plot data consists of plot (main joining element which needs to be added first, includes general properties such as caption), source (e.g., signal or direct update call),
#         processor of th esource (mean frame, accumulate points, direct update), and appearance (trace labels, x- and y-axis labels, plot visibility).
#     These four parts are set up and removed using separate commands:
#         ``add_plot``/``delete_plot``: add and delete plots; the plot needs to be added before settings up other elements (source, processor, appearence); deleting the plot also deletes the associated elements
#         ``setup_source``/``delete_source``: setup and delete source; if the source is not set up, no data is fed to the processor
#         ``setup_processor``/``delete_processor``: setup and delete processor; if the processor is not set up, the incoming data is not processed and is ignored
#         ``setup_appearance``/``delete_appearance``: setup and delete appearance; if the processor is not set up, default apperance is used (generic axes labels, plot names are the same as channel names)
#     In addition, there are several specific command for different elements:
#         ``get_plot_parameters``: get generic plot parameters (e.g., plot caption)
#         ``get_processor_parameters``: get specific processor parameters (e.g., accumulator size)
#         ``reset_processor``: reset accumulating processor state
#         ``get_appearance``: get appearence parameters; can be incomplete, since the channel names might not be know at this point (for complete appearance, use ``get_data`` with ``appearance=True``)
#         ``get_data``: get data of the given plot (can also return the corresponding appearance)
#         ``enable``/``disable``: since source processing can take considerable resources, this allows to pause it in case it's not needed
#     """
#     def setup_task(self, settings=None):
#         self.settings=settings or {}
#         self.memsize=self.settings.get("memsize",100000)
#         self.plots={}
#         self.sources={}
#         self.processors={}
#         self.appearance={}
#         self.source_enabled={}
#         self.add_command("add_plot")
#         self.add_command("get_plot_parameters")
#         self.add_command("delete_plot")
#         self.add_command("setup_source")
#         self.add_command("delete_source")
#         self.add_command("setup_processor")
#         self.add_command("get_processor_parameters")
#         self.add_command("reset_processor")
#         self.add_command("delete_processor")
#         self.add_command("setup_appearance")
#         self.add_command("get_appearance")
#         self.add_command("delete_appearance")
#         self.add_command("get_data")
#         self.add_command("enable")
#         self.add_command("disable")


#     TPlot=collections.namedtuple("TPlot",["name","label"])
#     def add_plot(self, name, label=None):
#         """
#         Add a new plot with the given name and optional label.

#         Should be called before setting up other properties (source, processor, etc.)
#         """
#         if name is None:
#             raise ValueError("name ``None`` is not allowed")
#         if name in self.plots:
#             raise ValueError("plot {} is already defined".format(name))
#         if label is None:
#             label=name
#         self.plots[name]=self.TPlot(name,label)
#     def get_plot_parameters(self, name):
#         """Get plot parameters as a dictionary"""
#         self._check_plot(name)
#         return {"name":name,"label":self.plots[name].label}
#     def _check_plot(self, name):
#         if name not in self.plots:
#             raise ValueError("plot {} is not defined".format(name))
#     TSource=collections.namedtuple("TSource",["kind","params"])
#     TSignalSource=collections.namedtuple("TSignalSource",["sid"])
#     def setup_signal_source(self, name, src, tag, sync=False):
#         """
#         Setup signal source for a plot with a given name.

#         `src` and `tag` set up signal parameters.
#         If ``sync==True``, the callback is set up as synchronous, i.e., the source must wait if the queue is full; otherwise, messages might be skipped if the processing is too slow.
#         """
#         if name in self.sources:
#             self.delete_source(name)
#         callback=lambda s,t,v: self.process_source(name,v)
#         if sync:
#             sid=self.subscribe_commsync(callback,srcs=src,dsts="any",tags=tag,limit_queue=2,on_full_queue="wait")
#         else:
#             sid=self.subscribe_commsync(callback,srcs=src,dsts="any",tags=tag,limit_queue=10)
#         src_params=self.TSignalSource(sid)
#         self.sources[name]=self.TSource("signal",src_params)
#         self.setup_appearance(name)
#     def setup_source(self, name, kind, **kwargs):
#         """
#         Setup source for a plot with a given name.

#         `kind` is the source kind. Can be ``"signal"`` (see :meth:`setup_signal_source`), or ``None`` (keep the current processor, if it's already set up)
#         """
#         self._check_plot(name)
#         if kind is None:
#             if name in self.sources:
#                 kind=self.sources[name].kind
#             else:
#                 raise ValueError("can't determine kind for source {}".format(name))
#         if kind=="signal":
#             self.setup_signal_source(name,**kwargs)
#         else:
#             raise ValueError("kind {} is not defined".format(kind))
#     def _delete_signal_source(self, name):
#         sid=self.sources[name].src_params.sid
#         self.unsubscribe(sid)
#     def delete_source(self, name):
#         """Delete source parameters for a plot with a given name"""
#         self._check_plot(name)
#         if name in self.sources:
#             src=self.sources[name].src
#             if src=="signal":
#                 self._delete_signal_source(name)
#             del self.sources[name]
#             del self.source_enabled[name]

#     TProcessor=collections.namedtuple("TProcessor",["kind","proc"])
#     def setup_frame_mean_processor(self, name, roi=None, x_source=None, calc_period=None):
#         """
#         Setup frame mean processor for a plot with a given name.

#         Some parameters can be missing, which keeps their previous value (if the processor is already set up), or uses default values (if it's created new)
#         If the source produces frame messages, then this processor generates means of the frames inside a given optional ROI.
#         Args:
#             roi: ROI for mean calculation (:class:`.image.ROI` object), or ``"full"`` (use full frame mean)
#             x_source: source for the x-axis; can be ``"index"`` (frame index), or ``"time"`` (time of the incoming frame message)
#             calc_period: preiodicity for frames for which mean is calculated (e.g., with ``calc_period=3`` only every 3rd frame is used)
#         """
#         if name not in self.processors or self.processors[name][0]!="frame/roi_mean":
#             self.delete_processor(name)
#             self.processors[name]=self.TProcessor("frame/roi_mean",FrameAverageCalculator(accum_size=self.memsize))
#         calc=self.processors[name][1]
#         if calc_period is not None:
#             calc.setup_period(calc_period)
#         if roi is not None:
#             calc.setup_roi(roi)
#         if x_source is not None:
#             calc.setup_x_source(x_source)
#     def setup_point_accum_processor(self, name, channels=None, x_source=None, x_channel=None, calc_period=None, autoupdate_channels=True):
#         """
#         Setup point accumulator processor for a plot with a given name.

#         Some parameters can be missing, which keeps their previous value (if the processor is already set up), or uses default values (if it's created new)
#         If the source produces named data messages (dictionaries of channel values), then this processor accumulates them into a single table.
#         Args:
#             channels: channels in the incoming data; can also be ``None``, in which case channels are extracted from the data when it's received
#             x_source: source for the x-axis; can be ``"index"`` (frame index), ``"time"`` (time of the incoming points), or ``None`` (no additional x-channel is added)
#             x_channel: name of the added x-channel (by default it's ``"idx"`` with an added index axis; for ``x_source==None`` it can be any of the incoming channel names)
#             calc_period: preiodicity for data points which are accumulated (e.g., with ``calc_period=3`` only every 3rd datapoint is used)
#             autoupdate_channels: if ``True`` and incoming data channels are different from the stored ones, re-create the accumulator with the new channels;
#                 otherwise, keep the accumulator, which ignores extra columns and raises errors if some are missing
#         """
#         if name not in self.processors or self.processors[name][0]!="point/accum":
#             self.delete_processor(name)
#             self.processors[name]=self.TProcessor("point/accum",PointSourceAccumulator(accum_size=self.memsize,autoupdate_channels=autoupdate_channels))
#         calc=self.processors[name][1]
#         if channels is not None:
#             calc.setup_channels(channels)
#         if x_source is not None:
#             calc.setup_x_source(x_source)
#         if calc_period is not None:
#             calc.setup_period(calc_period)
#         if x_channel is not None:
#             calc.setup_x_source(x_channel)
#     def setup_processor(self, name, kind=None, **kwargs):
#         """
#         Setup processor for a plot with a given name.

#         `kind` is the processor kind. Can be ``"frame/roi_mean"`` (see :meth:`setup_frame_mean_processor`), ``"point/accum"`` (see :meth:`setup_point_accum_processor`),
#         or ``None`` (keep the current processor, if it's already set up)
#         """
#         self._check_plot(name)
#         if kind is None:
#             if name in self.processors:
#                 kind=self.processors[name].kind
#             else:
#                 raise ValueError("can't determine kind for processor {}".format(name))
#         if kind=="frame/roi_mean":
#             self.setup_frame_mean_processor(name,**kwargs)
#         elif kind=="point/accum":
#             self.setup_point_accum_processor(name,**kwargs)
#         else:
#             raise ValueError("kind {} is not defined".format(kind))
#     def delete_processor(self, name):
#         """Delete processor for a plot with a given name"""
#         if name in self.processors:
#             del self.processors[name]
#     def reset_processor(self, name):
#         """Reset processor (e.g., clear accumulated buffer) for a plot with a given name"""
#         self._check_plot(name)
#         if name in self.processors:
#             kind,proc=self.processors[name]
#             if kind in {"frame/roi_mean","point/accum"}:
#                 proc.reset()
#     def get_processor_parameters(self, name):
#         """Get processor parameters as dictionary for a plot with a given name"""
#         self._check_plot(name)
#         if name not in self.processors:
#             return None
#         kind,proc=self.processors[name]
#         params={"kind":kind}
#         if kind=="frame/roi_mean":
#             params.update({"calc_period":proc.calc_period,"x_source":proc.x_source,"x_channel":proc.x_channel
#                 ,"roi":proc.roi,"fit_roi":proc.get_fit_roi(),"frame_size":proc.get_last_frame_size()})
#         elif kind=="frame/roi_mean":
#             params.update({"calc_period":proc.calc_period,"x_source":proc.x_source,"x_channel":proc.x_channel,"channels":proc.channels})
#         return params

#     def setup_appearance(self, name, x_label=None, y_label=None, plot_labels=None, visible=None):
#         """
#         Setup appearance for a plot with a given name.

#         Args:
#             x_label: label of x-axis (default is ``"Index"``)
#             y_label: label of y-axis (default is ``"Value"``)
#             plot_labels: dictionary ``{name:label}`` with labels of channels with corresponding names; can also be ``"auto"``, in which case labels are the same as channel names (default)
#             visible: dictionary ``{name:visible}`` which defines if trace s are visible;  can also be ``"auto"``, in which case all traces are visible (default)
#         """
#         self._check_plot(name)
#         if name not in self.appearance:
#             self.appearance[name]=self.get_appearance(name)
#         if x_label is not None:
#             self.appearance[name]["x_label"]=x_label
#         if y_label is not None:
#             self.appearance[name]["y_label"]=y_label
#         if plot_labels is not None:
#             self.appearance[name]["plot_labels"]=plot_labels
#         if visible is not None:
#             self.appearance[name]["visible"]=visible
#     def get_appearance(self, name, channels=None, x_channel=None):
#         """Get appearance parameters as dictionary for a plot with a given name"""
#         self._check_plot(name)
#         default_appearance={"x_label":"Index","y_label":"Value","plot_labels":"auto","visible":"auto"}
#         app=self.appearance.get(name,default_appearance).copy()
#         if channels is not None:
#             if x_channel is not None:
#                 app["x_channel"]=x_channel
#             dchannels=[ch for ch in channels if ch!=x_channel]
#             pl=app["plot_labels"]
#             if pl=="auto":
#                 app["plot_labels"]={ch:ch for ch in dchannels}
#             else:
#                 if isinstance(pl,list):
#                     pl=dict(zip(dchannels,pl))
#                 for ch in dchannels:
#                     pl.setdefault(ch,ch)
#                 if x_channel in pl:
#                     pl[x_channel]=None
#                 app["plot_labels"]={ch:l for ch,l in pl.items() if ch in channels}
#             vis=app["visible"]
#             if vis=="auto":
#                 app["visible"]={ch:True for ch in dchannels}
#             else:
#                 if isinstance(vis,list):
#                     vis=dict(zip(dchannels,vis))
#                 for ch in dchannels:
#                     vis.setdefault(ch,True)
#                 if x_channel in vis:
#                     vis[x_channel]=False
#                 app["visible"]={ch:v for ch,v in vis.items() if ch in channels}
#         return app
#     def delete_appearance(self, name):
#         """Delte (i.e., reset to default) appearance parameters as dictionary for a plot with a given name"""
#         if name in self.appearance:
#             del self.appearance[name]

#     def delete_plot(self, name):
#         """Delte a plot with a given name, together with all its elements"""
#         self._check_plot(name)
#         self.delete_source(name)
#         self.delete_processor(name)
#         self.delete_appearance(name)
#         del self.plots[name]


#     def process_source(self, name, value):
#         """Receive the source data (frames or traces), process and add to the accumulator table"""
#         if self.source_enabled.get(name,False):
#             if name in self.processors:
#                 kind,proc=self.processors[name]
#                 if kind in {"frame/roi_mean","point/accum"}:
#                     proc(value)


#     def get_data(self, name, maxlen=None, appearance=True):
#         """
#         Get the accumulated data as a dictionary of 1D numpy arrays.
        
#         If `maxlen` is specified, get at most `maxlen` datapoints from the end.
#         If ``appearance==True``, return 2-tuple ``(data,appearance)``, where ``appearance`` are complete appearance parameters applying to this data
#         """
#         if name is None:
#             raise ValueError("name ``None`` is not allowed")
#         if name in self.processors:
#             kind,proc=self.processors[name]
#             x_channel=None
#             if kind in {"frame/roi_mean","point/accum"}:
#                 data=proc.get_data(maxlen=maxlen,fmt="dict")
#                 x_channel=proc.x_channel
#             if data is not None:
#                 if appearance:
#                     return data,self.get_appearance(name,channels=list(data) if data else None,x_channel=x_channel)
#                 else:
#                     return data
#         return (None,None) if appearance else None

#     def disable(self, name=None):
#         """
#         Disable a plot with a given name.

#         If ``name==None``, disable all plots.
#         """
#         if name is not None:
#             if name in self.sources:
#                 self.source_enabled[n]=False
#         else:
#             for n in self.sources:
#                 self.source_enabled[n]=False
#     def enable(self, name, single=False, reset_on_change=True):
#         """
#         Disable a plot with a given name.

#         If ``single==True``, then in addition diable all other plots.
#         If ``reset_on_change==True`` and the enabled plot has been previously disabled, reset its processor.
#         """
#         if name is None:
#             raise ValueError("name ``None`` is not allowed")
#         if name in self.sources:
#             if not self.source_enabled[name]:
#                 self.source_enabled[name]=True
#                 if reset_on_change:
#                     self.reset_processor(name)
#         if single:
#             for n in self.sources:
#                 if n!=name:
#                     self.source_enabled[n]=False