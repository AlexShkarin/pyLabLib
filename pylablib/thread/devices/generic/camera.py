from ... import device_thread
from ...stream import stream_manager, stream_message
from ....core.utils import dictionary, funcargparse
from ....devices.interface import camera as cam_utils

import numpy as np

import collections
import contextlib
import time


class RateCalculator:
    """
    Calculator of the rate of the events averaged over some period of time.
    
    Args:
        period: averaging period; if ``None``, calculate every time :meth:`update` is called
    """
    def __init__(self, period=None):
        self.period=period
        self.reset()
    def reset(self):
        """Reset the count value"""
        self.last_time=None
        self.last_count=None
        self.rate=None
    def update(self, count):
        """
        Update the event count to the new value.

        Return the resulting rate.
        If ``period is None`` on creation, the rate is re-calculated
        every ``period`` seconds; otherwise, it is recalculated on every call.
        """
        t=time.time()
        if self.last_time is None:
            self.last_time=t
            self.last_count=count
        else:
            if self.period is None or t-self.last_time>self.period:
                dt=t-self.last_time
                dc=count-self.last_count
                self.rate=dc/dt
                self.last_time=t
                self.last_count=count
        return self.rate



class GenericCameraThread(device_thread.DeviceThread):
    """
    Generic camera device thread.

    Methods to overload:
        - ``connect_device``: create the device class and assign it to ``.device`` attribute; if connection failed, can leave the attribute ``None``

    Variables:
        - ``"status/acquisition"``: acquisition status; can be ``"stopped"`` (acquisition stopped) or ``"acquiring"`` (acquisition is in progress)
        - ``"frames/acquired"``: number of acquired frames (according to the camera interface)
        - ``"frames/read"``: number of read and sent frames (can be less than the acquired number if some frames were missed)
        - ``"frames/buffer_filled"``: number of frames in the buffer at the last readout
        - ``"frames/fps"``: calculated frame streaming fps (averaged over 1 second)
        - ``"frames/last_idx"``: index of the last acquired frame
        - ``"frames/last_frame"``: last acquired frame
        - ``"parameters"``: camera settings

    Multicasts:
        - ``"frames/new"``: newly acquired frames; a list of tuples ``(idx, frame)`` of frame index and frame value (except for :class:`IMAQPhotonFocusCameraThread`)

    External methods (deal with synchronization, so should be called directly):
        - ``wait_acq``: wait until streaming is in a given state (started or stopped)
        - ``wait_for_next_frame``: wait until a new frame is acquired and return it

    Commands:
        - ``apply_parameters``: apply camera parameters; parameters correspond to settings defined in the camera class
            (i.e., ``apply_parameters`` corresponds to ``apply_settings`` of the camera device class)
        - ``acq_start``: start camera acquisition loop
        - ``acq_stop``: stop camera acquisition loop
        - ``wait_acq``: wait until a given acquisition status (used for waiting until the camera enters or exits the acquisition loop)
        - ``wait_for_next_frame``: wait unit the next frame is acquired
    """
    parameter_variables={"frame_info_fields"} # list of settings to be updated when camera thread is running (to be overloaded in subclasses)
    parameter_freeze_running={} # list of settings which do not need to be updated when running
    TAcqLoop=collections.namedtuple("TAcqLoop",["loop","finalize"])
    _default_min_buffer_size=(1.,100)
    _default_min_poll_period=0.05
    _default_parameters_update_time=1.
    _default_updated_camera_attributes={}
    _update_camera_attribute_limits=True
    _frameinfo_include_fields=None
    TimeoutError=cam_utils.ICamera.TimeoutError
    FrameTransferError=cam_utils.ICamera.FrameTransferError
    def setup_task(self, remote=None, misc=None):  # pylint: disable=arguments-differ
        super().setup_task()
        self.misc=dictionary.Dictionary(misc)
        self.frames_src=stream_manager.StreamSource(stream_message.FramesMessage,sn=self.name)
        self.remote=remote
        self._max_chunk_size_bytes=2**20
        self._acquisition_loops={}
        self._running_loop=None
        self.min_poll_period=self.misc.get("loop/min_poll_period",self._default_min_poll_period)
        self.parameters_update_time=self.misc.get("loop/parameters_update_time",self._default_parameters_update_time)
        self._on_attribute_error="error"
        self._last_obtained_parameters={}
        def_time,def_frames=self._default_min_buffer_size
        self.min_buffer_size=self.misc.get("buffer/min_size/time",def_time),self.misc.get("buffer/min_size/frames",def_frames)
        self.fps_calc=RateCalculator(1.)
        self.open()
        self.add_job("update_parameters",self.update_parameters,self.parameters_update_time)
        self._update_aux_parameters()
        self.add_command("add_acq_loop",self.add_acq_loop)
        self.add_command("remove_acq_loop",self.remove_acq_loop)
        self.add_command("acq_start",self.acq_start)
        self.add_command("acq_stop",self.acq_stop)
        self.add_command("modify_updated_camera_attributes",self.modify_updated_camera_attributes)
        self.add_command("set_camera_attributes_error_action",self.set_camera_attributes_error_action)
        self.add_command("clear_camera_attributes_error",self.clear_camera_attributes_error)
        self.add_batch_job("acq_loop",self.acq_loop,self.acq_finalize)
        self.add_acq_loop("regular",self.acq_loop_regular,self.acq_finalize_regular)
        self.v["stream/sn"]=self.name
        self.v["stream"]=self.frames_src.get_ids(as_dict=True)
        self.acq_finalize_regular()

    def setup_open_device(self):
        super().setup_open_device()
        self.TimeoutError=self.rpyc_obtain(self.device.TimeoutError)
        self.FrameTransferError=self.rpyc_obtain(self.device.FrameTransferError)
        self.v["parameters/add_info"]=False
        if self._default_updated_camera_attributes=="all":
            self._updated_camera_attributes={a:True for a in self.device.get_all_attributes()}
        else:
            self._updated_camera_attributes=dict(self._default_updated_camera_attributes)
        self.update_parameters()
        self._update_aux_parameters()
        self._set_acquisition_status("stopped")
    def close_device(self):
        try:
            self.acq_stop()
        except ValueError:
            pass
        self.v["parameters"]=None
        self._reset_frame_counters()
        self.v["frames/last_frame"]=None
        super().close_device()

    
    def _set_acquisition_status(self, status, text=None):
        status_names={"stopped":"Stopped", "setup":"Setting up...", "acquiring":"In progress", "cleanup":"Cleaning up..."}
        self.update_status("acquisition",status,text or status_names.get(status))
    def setup_acquisition(self, *args, force_setup=False, **kwargs):
        status=self.sv["status/acquisition"]
        if not self.device.is_acquisition_setup() or force_setup:
            self._set_acquisition_status("setup")
            self.device.setup_acquisition(*args,**kwargs)
        self._set_acquisition_status(status)
    def clear_acquisition(self):
        if self.device.is_acquisition_setup():
            self._set_acquisition_status("cleanup")
            self.device.clear_acquisition()
        self._set_acquisition_status("stopped")
    @contextlib.contextmanager
    def _pausing_acq(self, kind="default"):
        if kind=="none":
            with self.device.pausing_acquisition(clear=False,stop=False) as (acq_in_progress,acq_params):
                yield (acq_in_progress,acq_params)
        else:
            self._reset_frame_counters()
            clear={"default":None,"pause":False,"clear":True}[kind]
            with self.device.pausing_acquisition(clear=clear) as (acq_in_progress,acq_params):
                yield (acq_in_progress,acq_params)
    def _update_frozen_parameters(self, parameters):
        for k,v in self._last_obtained_parameters.items():
            if k not in parameters:
                parameters.add_entry(k,v,force=True)
        self._last_obtained_parameters={k:parameters[k] for k in self.parameter_freeze_running if k in parameters}
    def _update_additional_parameters(self, parameters):
        pass
    def _get_camera_attributes(self, **kwargs):
        attrs={k for k,v in self._updated_camera_attributes.items() if v}
        self._updated_camera_attributes.update({k:False for k,v in self._updated_camera_attributes.items() if v=="single"})
        return {a:self.device.get_attribute_value(a,**kwargs) for a in attrs if getattr(self.device.ca[a],"readable",True)}
    def _get_camera_attribute_descriptions(self):
        attrs=self.device.ca[""]
        if self._update_camera_attribute_limits:
            for a in attrs.values():
                if hasattr(a,"update_limits"):
                    a.update_limits()
        return attrs
    def modify_updated_camera_attributes(self, attributes="all", mode=True):
        """
        Change attribute update properties.

        `attributes` can be either a list of modified attributes or ``"all"``.
        `mode` can be ``True`` (always update with other parameters), ``False`` (never update),
        or ``"single"`` (update once at the next parameter update).
        """
        if attributes=="all":
            attributes=list(self.device.get_all_attributes()) if self.device is not None else list(self._updated_camera_attributes)
        if not isinstance(attributes,(tuple,list,set)):
            attributes={attributes}
        funcargparse.check_parameter_range(mode,"mode",[True,False,"single"])
        self._updated_camera_attributes.update({a:mode for a in attributes})
    def set_camera_attributes_error_action(self, action="error"):
        """
        Set action of the attribute assignment error.

        Can be ``"error"`` (raise the error as usual), or ``"report"``
        (set the corresponding ``"parameters/errors/camera_attributes/<att>"`` thread variable to the raised error value).
        """
        funcargparse.check_parameter_range(action,"action",["error","report"])
        self._on_attribute_error=action
    def clear_camera_attributes_error(self, attributes):
        """Clear reported error states for the given attributes"""
        if not isinstance(attributes,(tuple,list,set)):
            attributes={attributes}
        for att in attributes:
            self.v["parameters/errors/camera_attributes",att]=None
    def _get_parameters(self, pause="none"):  # pylint: disable=arguments-differ
        if self.device:
            include=self.parameter_variables
            if self.device.acquisition_in_progress() and pause=="none":
                include=set(include)-(set(self.parameter_freeze_running)&set(self._last_obtained_parameters))
            with self._pausing_acq(kind=pause):
                parameters=self.device.get_full_info(include=include)
                parameters.update({"camera_attributes":self._get_camera_attributes()})
            parameters=dictionary.Dictionary(self.rpyc_obtain(parameters))
            parameters.filter_self(lambda x: x is not None)
            self._update_frozen_parameters(parameters)
            self._update_additional_parameters(parameters)
            return parameters
        else:
            return dictionary.Dictionary()
    def _update_aux_parameters(self):
        aux_info=dictionary.Dictionary()
        if self.device and hasattr(self.device,"ca"):
            aux_info["camera_attributes_desc"]=self._get_camera_attribute_descriptions()
        self.set_variable("parameters/aux",aux_info,update=True)
    def _get_aux_full_info(self):
        aux_info=super()._get_aux_full_info()
        if self.device:
            if hasattr(self.device,"ca"):
                aux_info.update({"camera_attributes_desc":self.device.ca[""]})
        return aux_info

    def _reset_frame_counters(self):
        self.v["frames/acquired"]=0
        self.v["frames/read"]=0
        self.v["frames/buffer_filled"]=0
        self.v["frames/fps"]=0
        self.v["frames/last_idx"]=0
        self.fps_calc.reset()
        self.frames_src.next_session()
        self.v["stream"]=self.frames_src.get_ids(as_dict=True)
        return self.v["stream/sid"]
    def _estimate_buffers_num(self):
        if self.device:
            n_fixed=self.min_buffer_size[1]
            n_rate=self.min_buffer_size[0]/self.device.get_frame_period()
            return int(max(n_fixed,n_rate))
        return None
    def _prepare_applied_parameters(self, parameters):
        pass
    def _set_camera_attribute(self, name, value):
        self.device.cav[name]=value
    def _apply_additional_parameters(self, parameters):
        for k in ["add_info"]:
            if k in parameters:
                self.v["parameters",k]=parameters.pop(k)
        parameters=dictionary.Dictionary(parameters)
        if "camera_attributes" in parameters:
            for attr,val in parameters["camera_attributes"].as_dict("flat").items():
                try:
                    self._set_camera_attribute(attr,val)
                    if self._on_attribute_error=="report":
                        self.v["parameters/errors/camera_attributes",attr]=None
                except self.device.Error as err:
                    if self._on_attribute_error=="error":
                        raise
                    if self._on_attribute_error=="report":
                        self.v["parameters/errors/camera_attributes",attr]=err
    def apply_parameters(self, parameters, update=True, pause="default"):  # pylint: disable=arguments-differ
        """
        Apply camera parameters.

        Might interrupt camera acquisition loop, if required.
        """
        if self.device:
            status=self.sv["status/acquisition"]
            self._set_acquisition_status("setup")
            with self._pausing_acq(kind=pause) as (_,acq_params):
                self._prepare_applied_parameters(parameters)
                super().apply_parameters(parameters,update=False)
                self._apply_additional_parameters(parameters)
                nframes=self._estimate_buffers_num()
                acq_nframes=acq_params.get("nframes") if acq_params else None
                if nframes and (acq_nframes is None or acq_nframes<nframes*0.9 or acq_nframes>nframes*2):
                    self._reset_frame_counters()
                    self.setup_acquisition(nframes=nframes,force_setup=True)
                if update:
                    self.update_parameters()
                    self._update_aux_parameters()
            if "buffer_size" in self.parameter_variables:
                self.v["parameters/buffer_size"]=self.device.dv["buffer_size"]
            self._set_acquisition_status(status)
            parameters=dictionary.Dictionary(parameters)
            if "tag" in parameters:
                self.v["parameters/tag"]=parameters["tag"]

    def _get_metainfo(self, frames, indices, infos):  # pylint: disable=unused-argument
        metainfo={}
        parameters=self.v["parameters"]
        if parameters["add_info"]:
            fields=parameters["frame_info_fields"]
            metainfo["frame_info_fields"]=fields[:1]+["acq_timestamp_ms","width","height"]+fields[1:]
        if "roi" in parameters:
            metainfo["roi"]=parameters["roi"]
        return metainfo
    def _build_chunks(self, frames, infos, max_size=None):
        if infos is not None and not all(isinstance(inf,np.ndarray) for inf in infos):
            return frames,infos
        if any(f.ndim==3 for f in frames):
            return frames,infos
        max_size=max_size or self._max_chunk_size_bytes
        chunks=[]
        s=None
        curr_size=0
        for i,f in enumerate(frames):
            if s is None:
                s=i
            elif curr_size>max_size or frames[s].shape!=f.shape or (infos is not None and infos[s].shape!=infos[i].shape):
                chunks.append((s,i))
                s=i
                curr_size=0
            curr_size+=f.nbytes
        if s is not None:
            chunks.append((s,len(frames)))
        frames=[np.asarray(frames[s:e]) for s,e in chunks]
        if infos is not None:
            infos=[np.asarray(infos[s:e]) for s,e in chunks]
        return frames,infos
    def _expand_frame_infos(self, frames, indices, infos):  # pylint: disable=unused-argument
        if infos is None:
            return None
        timestamp=int(time.time()*1E3)
        infos=[np.column_stack([i[:,0],[timestamp]*len(i),[f.shape[-1]]*len(i),[f.shape[-2]]*len(i),i[:,1:]]) for i,f in zip(infos,frames)]
        infos=[i[0] if f.ndim==2 else i for i,f in zip(infos,frames)]
        return infos
    def _read_send_images(self):
        """Read and send new available images"""
        rng=self.device.get_new_images_range()
        nsent=0
        frame_fmt=self.device.get_frame_format()
        if rng:
            if self.v["parameters/add_info"]:
                frames,infos=self.device.read_multiple_images(rng,return_info=self.v["parameters/add_info"])
                if frame_fmt=="array":
                    infos=[self.rpyc_obtain(infos)]
                else:
                    infos=self.rpyc_obtain(infos)
            else:
                frames=self.device.read_multiple_images(rng)
                infos=None
            if frame_fmt=="array":
                frames=[self.rpyc_obtain(frames)]
            else:
                frames=self.rpyc_obtain(frames)
            frames,infos=self._build_chunks(frames,infos)
            if frames and frames[0].ndim==3:
                lch=np.array([len(f) for f in frames])
                nread=int(sum(lch))
                indices=[rng[1]-nread]+list(np.cumsum(lch[:-1])+rng[1]-nread)
            else:
                nread=len(frames)
                indices=list(range(rng[1]-nread,rng[1]))
            infos=self._expand_frame_infos(frames,indices,infos)
            self.v["frames/acquired"]=rng[1]
            self.v["frames/read"]+=nread
            self.v["frames/buffer_filled"]=rng[1]-rng[0]
            self.v["frames/last_idx"]=rng[1]-1
            nsent=len(frames)
            if nsent:
                msg=self.frames_src.build_message(frames,indices,infos,source="camera",metainfo=self._get_metainfo(frames,indices,infos),sn=self.name)
                self.send_multicast("any","frames/new",msg)
                self.v["frames/last_frame"]=frames[-1] if frames[-1].ndim==2 else frames[-1][-1]
        return nsent

    def add_acq_loop(self, name, loop, finalize=None):
        """
        Add a new acquisition loop to be potentially used instead of the regular one
        
        `loop` must be a generator function (with ``yield`` statement) which defines the batch job for the loop.
        Optional `finalize` function is called whenever loop is finished (through normal execution, interruption, or error)
        """
        if name in self._acquisition_loops:
            raise ValueError("acquisition loop {} already exists".format(name))
        self._acquisition_loops[name]=self.TAcqLoop(loop,finalize)
    def remove_acq_loop(self, name):
        """Remove an existing acquisition loop"""
        if self._running_loop==name:
            self.stop_acquisition()
        del self._acquisition_loops[name]
    def acq_start(self, name="regular", period=0., **kwargs):
        """Start an acquisition loop with a given name (default loop by default) and period (zero period, i.e., as fast as possible by default)"""
        if self.device:
            self.acq_stop()
            self.start_batch_job("acq_loop",period,name,**kwargs)
    def acq_stop(self):
        """Stop acquisition loop"""
        self.stop_batch_job("acq_loop")
    def acq_loop(self, name, **kwargs):
        """Run the named acquisition loop with the given parameters"""
        loop=self._acquisition_loops[name].loop
        self._running_loop=name
        for v in loop(**kwargs):
            yield v
    def acq_finalize(self, name, **kwargs):
        finalize=self._acquisition_loops[name].finalize
        self._running_loop=None
        if finalize is not None:
            finalize(**kwargs)


    def acq_loop_regular(self):
        """Regular acquisition loop"""
        self.device.stop_acquisition()
        if self.rpyc_serv is not None:
            self.device.set_frame_format("array")
        else:
            self.device.set_frame_format("try_chunks")
        self.device.set_frame_info_format("array",include_fields=self._frameinfo_include_fields)
        self.update_parameters()
        self._update_aux_parameters()
        self.device.start_acquisition()
        if "buffer_size" in self.parameter_variables:
            self.v["parameters/buffer_size"]=self.device.dv["buffer_size"]
        self._set_acquisition_status("acquiring")
        yield
        while True:
            t0=time.time()
            try:
                self.device.wait_for_frame(timeout=0.1)
                self._read_send_images()
            except self.TimeoutError:  # pylint: disable=catching-non-exception
                pass
            except self.FrameTransferError:  # pylint: disable=catching-non-exception
                self.device.clear_acquisition()
                self.restart_batch_job("acq_loop",start_immediate=False)
                yield
            dt=time.time()-t0
            if dt<self.min_poll_period:
                self.sleep(self.min_poll_period-dt)
            self.v["frames/fps"]=self.fps_calc.update(self.v["frames/acquired"])
            yield
    def acq_finalize_regular(self):
        """Finalize regular acquisition loop"""
        if self.device:
            self._read_send_images()
            self.device.stop_acquisition()
        self._reset_frame_counters()
        self.v["frames/last_frame"]=None
        self._set_acquisition_status("stopped")


    def wait_acq(self, state="acquiring"):
        """
        Wait until streaming is in the given state.

        State can be ``"stopped"`` (acquisition stopped) or ``"acquiring"`` (acquisition is in progress)
        """
        self.sync_variable("status/acquisition",state)
    def wait_for_next_frame(self, n=1, start=None, timeout=None):
        """
        Wait until `n` frames have been acquired starting from the `start` (current moment by default).

        Return the new frame.
        If `timeout` is defined, it is the waiting timeout; if it's passed, raise :exc:`.threadprop.TimeoutThreadError`.
        Should only be called from an external thread. Camera acquisition loop must be running for this method to finish.
        """
        if start is None:
            start=self.v["frames/last_idx"]
        self.sync_variable("frames/last_idx", lambda idx: idx>=start+n, timeout=timeout)
        return self.v["frames/last_frame"]