from . import threadprop, message_queue, tag_queue, sync_primitives
from ..utils import funcargparse, general

import threading

_depends_local=["..utils.general"]
    
### Global thread inventory ###
# _running_threads_condition=sync_primitives.Condition(lock=sync_primitives.Lock(blocking_sync=True),blocking_sync=True)
# _running_threads_condition=sync_primitives.Condition(lock=threading.Lock(),blocking_sync=True)
_running_threads_condition=sync_primitives.Condition()
_running_threads={}
_thread_uids=general.NamedUIDGenerator(thread_safe=True)



class IThreadController(object):
    """
    Generic thread controller.

    Deals with correctly initializing and destroying the message queue, processing standard messages, and synchronizing with other threads.

    Args:
        name(str): thread name (can be used to, e.g., get the controller from a different thread).
    """
    def __init__(self, name=None):
        object.__init__(self)
        self.name=name or _thread_uids(type(self).__name__)
        self.message_queue=message_queue.MessageQueue(self)
        self.running_thread=None
        self.running_thread_lock=threading.RLock()
        self.start_event=sync_primitives.Event(False)
        self.stop_event=sync_primitives.Event(False)
        self._clear_on_stop=True
        self._stage="created"
        self._dependent_threads=[]
        self._daemon=False
    
    ### Message queue ###
    def limit_queue_length(self, tag, length):
        """
        Set length limit for a given tag.
        """
        self.message_queue.limit_length(tag,length)
        
    ### Instant messages processing ###
    # These are overloaded methods, which shouldn't be called from the outside
    def process_interrupt(self, msg):
        """
        Process interrupt message (automatically called for all messages with tag starting with ``"interrupt"``).

        Automatically called by the controller; to be overridden in subclasses.
        """
        if msg.tag=="interrupt.control":
            if msg.value=="stop":
                self._stop_self()
        elif msg.tag=="interrupt.execute":
            msg.value()
    def process_message(self, _):
        """
        Instant message processing.

        If return value is ``True``, the message is assumed to be processed internally (i.e., it doesn't get explicitly received).

        Automatically called by the controller; to be overridden in subclasses.
        """
        return False
    def _process_any_message(self, msg):
        if msg.tag.startswith("sync"):
            return False # always pass sync messages directly
        if msg.tag.startswith("interrupt"):
            self.process_interrupt(msg)
            return True # always silence interrupts
        if msg.tag=="execute":
            msg.value()
            return True
        return self.process_message(msg)
    
    
    ### Receiving messages ###
    def _build_message_filter(self, tags=None, filt=None):
        return tag_queue.build_filter(tags,filt,["interrupt"])
    def exhaust_messages(self, tags=None, filt=None):
        """
        Read and return (instantaneously) all available messages which satisfy the filter `filt`.

        Called from the controlled thread.
        """
        filt=self._build_message_filter(tags,filt)
        return self.message_queue.exhaust_messages(filt,self._process_any_message)
    def wait_for_message(self, tags=None, timeout=None, filt=None, exhaust=False, discard_on_timeout=False):
        """
        Wait for a message with given `tags` and satisfying the filter `filt`.

        if `exhaust` is ``True``, returns list of all messages satisfying `filt`, if several of them are available immediately.
        if `discard_on_timeout` is ``True`` and the wait timed out, mark the message for discarding using `filt` (see :meth:`.tag_queue.TaggedQueue.get`).

        Called from the controlled thread.
        """
        discard_filt=filt
        filt=self._build_message_filter(tags,filt)
        return self.message_queue.wait_for_message(filt,self._process_any_message,timeout,exhaust=exhaust,discard_on_timeout=discard_on_timeout,discard_filt=discard_filt)
    def check_interrupt(self):
        """
        Check for interrupt messages.

        Useful to insert in the middle of computationally-heavy code with no synchronization, to respond to interrupts from other threads (e.g., stopping requests).

        Called from the controlled thread.
        """
        self.wait_for_message([],timeout=0)
    def sleep(self, delay):
        """
        Sleep while still receiving interrupts.

        Called from the controlled thread.
        """
        self.wait_for_message([],timeout=delay)
        
        
    ### Thread function ###
    # These are overloaded methods, which shouldn't be called from the outside
    
    def run(self):
        """
        Body of the thread.

        Automatically called by the controller; to be overridden in subclasses.
        """
        raise NotImplementedError("IThreadController.run")
    def finalize(self):
        """
        Finalize the thread execution (regardless of the stopping reason).

        Automatically called by the controller; to be overridden in subclasses.
        """
        pass
    
    # Event functions called at changes in state.
    def _on_restart(self):
        self.message_queue.fix()
        self.start_event.clear()
        self.stop_event.clear()
    def _on_start(self):
        with _running_threads_condition:
            if self.name in _running_threads:
                raise RuntimeError("thread with name {} is already running".format(self.name))
            _running_threads[self.name]=self
            _running_threads_condition.notify_all()
        if _check_daemon_threads():
            self._stop_self()
        self.start_event.set()
    def _on_stop(self):
        self.stop_event.set()
        with _running_threads_condition:
            del _running_threads[self.name]
            _running_threads_condition.notify_all()
        with self.running_thread_lock:
            for th in self._dependent_threads:
                threadprop.kill_thread(th,sync=True)
        _check_daemon_threads()
        
            
    def _run_full(self, stop_after=True):
        """
        Full run routine (including state transitions and events).
        """
        if self._stage=="broken": # reinitialize message queue
            self._stage="created"
            self._on_restart()
        try:
            self._stage="starting"
            self._on_start()
            self._stage="running"
            self.run()
        except threadprop.InterruptExceptionStop:
            stop_after=True
        finally:
            if stop_after:
                self.finalize()
                self._stage="stopping"
                self._on_stop()
                self._stage="cleaning" # at this point the thread can't use its queue
                if self._clear_on_stop:
                    self.message_queue.clear()
                self.running_thread=None
                self._stage="broken"
    
    
    ### External calls ###
    def add_message(self, msg, sync=True, on_broken="error"):
        """
        Add the message to the queue.

        If `sync` is ``True``, do the synchronization (wait for receiving and scheduling) after sending the message.
        `on_broken` decides what happens if thethread is stopped or hasn't started yet (see :func:`.threadprop.on_error`).

        Called from any thread.
        """
        try:
            return self.message_queue.add_message(msg,sync=sync)
        except tag_queue.BrokenQueueError as e:
            if self.passed_stage("stopping") or not self.passed_stage("created"):
                e=threadprop.NotRunningThreadError("can't send message to a non-running thread")
            return threadprop.on_error(on_broken,e)
    def add_new_message(self, tag, value=None, priority=0, schedule_sync="wait", receive_sync="none", sync=True, timeout=None, on_broken="error"):
        """
        Create a new message, add it to the thread's queue, and return it.

        If `sync` is ``True``, do the synchronization (wait for receiving and scheduling) after sending the message.
        `on_broken` decides what happens if thethread is stopped or hasn't started yet (see :func:`.threadprop.on_error`).

        Called from any thread.
        """
        msg=self.message_queue.build_message(tag,value,priority,schedule_sync,receive_sync)
        return self.add_message(msg,sync=sync,on_broken=on_broken)# TODO: add timeout to messaging routines
    send_message=add_new_message
            
    def start(self, as_dependent=False, as_daemon=False):
        """
        Start the controller.

        if `as_dependent` is ``True``, the new thread becomes dependent on the caller thread (it stops when the caller thread stops).
        if `as_deamon` is ``True``, the new thread becomes a daemon (if only daemon threads are running, they get stopped).
        """
        with self.running_thread_lock:
            if self.running():
                raise RuntimeError("current thread is already running")
            self.running_thread=threading.Thread(target=self._run_full,name=self.name)
            self.running_thread.thread_controller=self
            if as_dependent:
                self.set_as_dependent()
            self._daemon=as_daemon
            self.running_thread.start()
    def start_continuing(self, stop_after_run=True):
        """
        Start the current controller in the current non-controlled thread.

        If `stop_after_run` is ``True``, the controller is stopped after the :meth:`run` function is done;
        otherwise, th controller continues (e.g., :meth:`run` can be empty, which means that this function simply initializes the controller).
        """
        with self.running_thread_lock:
            if self.running():
                raise RuntimeError("current thread is already running")
            if threadprop.current_controller() is threadprop.no_thread_controller:
                self.running_thread=threading.current_thread()
                self.running_thread.thread_controller=self
            else:
                raise RuntimeError("current thread already has a controller")
        self._run_full(stop_after=stop_after_run)
        
    def interrupt(self, subclass, value, sync=True, priority=0, timeout=None, on_broken="error"):
        """
        Send an interrupt with the given `subclass` and `value`.

        If `sync` is ``True``, wait until the interrupt is received (with the given `timeout`).
        `on_broken` decides what happens if thethread is stopped or hasn't started yet (see :func:`.threadprop.on_error`).

        Called from any thread.
        """
        tag="interrupt"
        if subclass is not None:
            tag="{0}.{1}".format(tag,subclass)
        receive_sync="wait" if sync else "none"
        self.add_new_message(tag,value,priority=priority,receive_sync=receive_sync,timeout=timeout,on_broken=on_broken)
        
    def _ask_for_call(self, call, sync=True, as_interrupt=False, priority=0, on_broken="error"):
        tag="interrupt.execute" if as_interrupt else "execute"
        receive_sync="wait" if sync else "none"
        return self.add_new_message(tag,call,priority=priority,receive_sync=receive_sync,on_broken=on_broken)
    def call_from_thread(self, func, args=None, kwargs=None, sync_recv=True, sync_done=False, as_interrupt=False, priority=0, on_broken="error"):
        """
        Call a function `func` with the arguments (`args` and `kwargs`) in in this controller thread.

        Called from any thread.
        """
        if sync_done:
            call=sync_primitives.SyncCall(func,args,kwargs)
            self._ask_for_call(call,sync=sync_recv,as_interrupt=as_interrupt,priority=priority,on_broken=on_broken)
            return call.value()
        else:
            args=args or []
            kwargs=kwargs or {}
            def call():
                func(*args,**kwargs)
            self._ask_for_call(call,sync=sync_recv,as_interrupt=as_interrupt,priority=priority,on_broken=on_broken)
    def _stop_self(self):
        if self.passed_stage("created") and not self.passed_stage("running"): 
            raise threadprop.InterruptExceptionStop()
    def stop(self, sync=True):
        """
        Stop the thread.

        If called from the current thread, stop self.
        If called from a different thread, send a stop interrupt. In this case, if `sync` is ``True``, wait until the thread received the message.
        """
        if threadprop.current_controller() is self:
            self._stop_self()
        else:
            self.interrupt("control","stop",sync=sync,priority=10)
    def sync(self, point="interrupt", timeout=None, on_broken="error"):
        """
        Synchronize with the thread.

        `point` determines where the synchronization happens. Can be either ``"interrupt"`` (sync on any interrupt),
        ``"start"`` (synchronize with the thread after its start), or ``"stop"`` (synchronize with the thread after its stop).

        Called from a non-controlled thread.
        """
        funcargparse.check_parameter_range(point,"point",{"interrupt","start","stop"})
        if point=="interrupt":
            self.interrupt("control","sync",sync=True,timeout=timeout,on_broken=on_broken)
        elif point=="start":
            self.start_event.wait(timeout=timeout)
        elif point=="stop":
            self.stop_event.wait(timeout=timeout)
        
        
    def add_dependent_thread(self, dependent=None):
        """
        Add a dependent thread (caller's thread by default) to this controller.

        A dependent thread is automatically stopped after this thread is stopped.

        Called from a non-controlled thread.
        """
        if dependent is self:
            return
        dependent=dependent or threadprop.current_controller()
        with self.running_thread_lock:
            if (dependent is not threadprop.no_thread_controller) and (dependent is not self):
                if not (dependent in self._dependent_threads):
                    self._dependent_threads.append(dependent)
    def set_as_dependent(self):
        """
        Set this thread as a dependent for the caller thread.

        A dependent thread is automatically stopped after the caller thread is stopped.

        Called from a non-controlled thread.
        """
        current_ctrl=threadprop.current_controller()
        if current_ctrl is not threadprop.no_thread_controller:
            current_ctrl.add_dependent_thread(self)
            
    ### Thread properties ###
    _stage_order={"created":0,"starting":1,"running":2,"stopping":3,"cleaning":4,"broken":5}
    def current_stage(self):
        """
        Return current stage of the process.
        
        Can have following values:
            - ``"created"``: thread is created, but not started
            - ``"starting"``: thread is starting, but is not running yet (notifying waiting threads)
            - ``"running"``: thread is executing its run code
            - ``"stopping"``: thread has done running and is currently stopping (notifying waiting threads, cleaning up dependent threads and daemons)
            - ``"cleaning"``: cleaning the message queue; communication is impossible at this point
            - ``"broken"``: thread is finished executing  

        Called from any thread.
        """
        return self._stage
    def passed_stage(self, stage):
        """
        Check if the thread passed the given `stage`.

        For stage description, see :meth:`current_stage`.

        Called from any thread.
        """
        return self._stage_order[self._stage]>self._stage_order[stage]
    def running(self):
        """
        Check if the thread is running,

        Called from any thread.
        """
        return self._stage=="running"
    
    def is_daemon(self):
        """
        Check if the thread is daemon,

        Called from any thread.
        """
        return self._daemon




def wait_for_thread_name(name): # TODO: doesn't work? (thread owner problems in _running_threads_condition.wait())
    """
    Wait until a thread with the given name starts.
    """
    with _running_threads_condition:
        while True:
            if name in _running_threads:
                return _running_threads[name]
            _running_threads_condition.wait()
            
def _check_daemon_threads(allow_non_controlled=True):
    """
    Check all threads. If only daemon threads are left, kill them in sync way.
    """
    with _running_threads_condition:
        all_daemon=all([d.is_daemon() for d in _running_threads.values()])
        if allow_non_controlled:
            all_threads=threading.enumerate()
            has_non_controlled=any([not t.isDaemon() and not threadprop.has_controller(t) for t in all_threads])
            all_daemon=all_daemon and not has_non_controlled
    if all_daemon:
        threadprop.kill_all(sync=True, include_current=False)
    return all_daemon






                    
class SimpleThreadController(IThreadController):
    """
    Simple thread.
    
    Runs a single task, with a possible cleanup after the end.

    Args:
        name(str): thread name (can be used to, e.g., get the controller from a different thread).
        job(callable): function to be executed in the thread.
        cleanup(callable): if not ``None``, function to be called when the thread is stopped (regardless of the stopping reason).
        args(list): arguments for `job` and `cleanup` functions.
        kwargs(dict): keyword arguments for `job` and `cleanup` functions.
        self_as_arg(bool): if ``True``, pass this controller as a first argument to the `job` and `cleanup` functions.
    """
    def __init__(self, name, job, cleanup=None, args=None, kwargs=None, self_as_arg=False):
        IThreadController.__init__(self,name)
        self.job=job
        self.cleanup=cleanup
        self.args=args or []
        if self_as_arg:
            self.args=[self]+self.args
        self.kwargs=kwargs or {}
    def run(self):
        self.job(*self.args,**self.kwargs)
    def finalize(self):
        if self.cleanup:
            self.cleanup(*self.args,**self.kwargs)




class ServiceThreadController(IThreadController):
    """
    Service thread.

    Receives and processes messages, and replies using a ``reply`` function.

    Args:
        name(str): thread name (can be used to, e.g., get the controller from a different thread).
        reply(callable): message processing function; if it returns a tuple, interpret it as tag and value for a reply message.
        setup(callable): if not ``None``, function to be called when the thread is starting.
        cleanup(callable): if not ``None``, function to be called when the thread is stopped (regardless of the stopping reason).
        args(list): arguments for `reply`, `startup` and `cleanup` functions.
        kwargs(dict): keyword arguments for `reply`, `startup` and `cleanup` functions.
        stopped_recipient_action(str): action to take if the reply recipient has stopped;
            can be ``"error"`` (raise an error), ``"stop"`` (stop the thread; similar to th previous) or ``"ignore"`` (ignore and continue).
    """
    def __init__(self, name, reply, setup=None, cleanup=None, args=None, kwargs=None, stopped_recipient_action="ignore"):
        funcargparse.check_parameter_range(stopped_recipient_action,"stopped_recipient_action",{"error","ignore","stop"})
        IThreadController.__init__(self,name)
        self.reply=reply
        self.setup=setup
        self.cleanup=cleanup
        self.stopped_recipient_action=stopped_recipient_action
        self.args=args or []
        self.kwargs=kwargs or {}
            
    def process_request(self, tag, value):
        return self.reply(tag,value,*self.args,**self.kwargs)
    def run(self):
        if self.setup:
            self.setup(*self.args,**self.kwargs)
        while True:
            msg=self.wait_for_message()
            reply=self.process_request(msg.tag,msg.value)
            if reply is not None:
                message_queue.send_message(msg.sender,reply[0],reply[1],on_broken=self.stopped_recipient_action)
    def finalize(self):
        if self.cleanup:
            self.cleanup(*self.args,**self.kwargs)
            
            
            
            
class RepeatingThreadController(IThreadController):
    """
    Recurring task thread.

    Periodically repeats a single function.

    Args:
        name(str): thread name (can be used to, e.g., get the controller from a different thread).
        job(callable): periodically called function.
        delay(float): calling period.
        setup(callable): if not ``None``, function to be called when the thread is starting.
        cleanup(callable): if not ``None``, function to be called when the thread is stopped (regardless of the stopping reason).
        args(list): arguments for `job`, `startup` and `cleanup` functions.
        kwargs(dict): keyword arguments for `job`, `startup` and `cleanup` functions.
        self_as_arg(bool): if ``True``, pass this controller as a first argument to the `job` and `cleanup` functions.
    """
    def __init__(self, name, job, delay=0, setup=None, cleanup=None, args=None, kwargs=None, self_as_arg=False):
        IThreadController.__init__(self, name)
        self.job=job
        self.setup=setup
        self.cleanup=cleanup
        self.delay=delay
        self.paused=False
        self.single_shot=False
        self.args=args or []
        if self_as_arg:
            self.args=[self]+self.args
        self.kwargs=kwargs or {}
        
    def execute(self):
        self.job(*self.args,**self.kwargs)
    
    def process_message(self, msg):
        if msg.tag=="control":
            if msg.value=="pause":
                self.paused=True
            elif msg.value=="resume":
                self.paused=False
            elif msg.value=="single":
                self.single_shot=True
                self.paused=True
            elif msg.value!="trigger":
                return True # ignore everything else, keep polling
        return False
    def run(self):
        if self.setup:
            self.setup(*self.args,**self.kwargs)
        while True:
            countdown=general.Countdown(self.delay)
            if ((not self.paused) or (self.single_shot)) and not self.skip:
                self.execute()
            self.single_shot=False
            self.skip=False
            timeout=None if self.paused else countdown.time_left()
            self.wait_for_message(["control","execute"],timeout=timeout,exhaust=True)
    def finalize(self):
        if self.cleanup:
            self.cleanup(*self.args,**self.kwargs)
    
    ##### External calls #####
    def control(self, value, sync=True, priority=0):
        """
        Send a control signal to the thread.

        If `sync` is ``True``, wait until the signal is received before continuing.

        Called from a non-controlled thread.
        """
        receive_sync="wait" if sync else "none"
        self.add_new_message("control",value,priority=priority,receive_sync=receive_sync)
    def pause(self, do_pause=True, sync=True):
        """
        Pause or resume the thread (depending on `do_pause` value).
        """
        if do_pause:
            self.control("pause",sync=sync)
        else:
            self.control("resume",sync=sync)
    def resume(self, sync=True):
        """
        Resume the thread execution if it's paused.
        """
        self.pause(False,sync=sync)
    def trigger(self, sync=True):
        """
        Trigger an execution cycle immediately (without waiting for the required delay).
        
        The execution is only performed if the thread is not paused.
        """
        self.control("trigger",sync=sync)
    def single(self, sync=True):
        """
        Trigger a single execution cycle and pause afterwards.
        """
        self.control("single",sync=sync)
    def sync(self, point="waiting"):
        funcargparse.check_parameter_range(point,"point",{"interrupt","start","stop","waiting"})
        if point=="waiting":
            self.control("sync",sync=True)
        else:
            IThreadController.sync(self,point=point)
    def set_delay(self, delay):
        """
        Set the repetition delay.
        """
        self.delay=delay
        
    def start(self, as_dependent=False, as_daemon=False, paused=False, skip_first=None):
        """
        Start the thread.

        if `as_dependent` is ``True``, the new thread becomes dependent on the caller thread (it stops when the caller thread stops).
        if `as_deamon` is ``True``, the new thread becomes a daemon (if only daemon threads are running, they get stopped).
        If `paused` is ``True``, the thread starts in a paused state (but it will still execute the first cycle, unless `skip_first` is ``True``).
        If `skip_first` is ``True``, skip the first cycle execution (by default ``True`` if ``paused==True`` and ``False`` otherwise).
        """
        self.paused=paused
        self.skip=paused if (skip_first is None) else skip_first
        IThreadController.start(self,as_dependent=as_dependent,as_daemon=as_daemon)



class MultiRepeatingThreadController(IThreadController):
    _new_jobs_check_period=0.1
    def __init__(self, name, setup=None, cleanup=None, args=None, kwargs=None, self_as_arg=False):
        IThreadController.__init__(self, name)
        self.setup=setup
        self.cleanup=cleanup
        self.paused=False
        self.single_shot=False
        self.args=args or []
        if self_as_arg:
            self.args=[self]+self.args
        self.kwargs=kwargs or {}
        self.jobs={}
        self.timers={}
        self._jobs_list=[]
        
    def add_job(self, name, job, period):
        if name in self.jobs:
            raise ValueError("job {} already exists".format(name))
        self.jobs[name]=(job,period)
        self.timers[name]=general.Timer(period)
        self._jobs_list.append(name)
    
    def _get_next_job(self):
        if not self._jobs_list:
            return None,None
        idx=None
        left=None
        for i,n in enumerate(self._jobs_list):
            t=self.timers[n]
            l=t.time_left()
            if l==0:
                idx,left=i,0
                break
            elif (left is None) or (l<left):
                idx=i
                left=l
        n=self._jobs_list.pop(idx)
        self._jobs_list.append(n)
        return n,left
        
    def run(self):
        if self.setup:
            self.setup(*self.args,**self.kwargs)
        while True:
            name,to=self._get_next_job()
            if name is None:
                self.sleep(self._new_jobs_check_period)
            else:
                self.sleep(to)
                job=self.jobs[name][0]
                self.timers[name].acknowledge(nmin=1)
                job(*self.args,**self.kwargs)
    def finalize(self):
        if self.cleanup:
            self.cleanup(*self.args,**self.kwargs)
        
        
        
class TimerThreadController(RepeatingThreadController):
    """
    Timer thread.

    Simplified version of the :class:`RepeatingThreadController`. Doesn't require a name, starts as a dependent and a daemon by default.

    Args:
        period(float): calling period.
        callback(callable): periodically called function.
        setup(callable): if not ``None``, function to be called when the thread is starting.
        cleanup(callable): if not ``None``, function to be called when the thread is stopped (regardless of the stopping reason).
        name(str): thread name (can be used to, e.g., get the controller from a different thread). By default, a unique identifier.
    """
    def __init__(self, period, callback, setup=None, cleanup=None, name=None):
        name=name or _thread_uids("timer")
        RepeatingThreadController.__init__(self,name,callback,period,setup=setup,cleanup=cleanup)
    def start(self, as_dependent=True, as_daemon=True, skip_first=None, single=False):
        """
        Start the thread.

        if `as_dependent` is ``True``, the new thread becomes dependent on the caller thread (it stops when the caller thread stops).
        if `as_deamon` is ``True``, the new thread becomes a daemon (if only daemon threads are running, they get stopped).
        If `skip_first` is ``True``, skip the first cycle execution.
        If `single` is ``True``, start in a single mode (only execute once). In combination with ``skip_first=True``, performs one callback function call after the `period` delay.
        """
        RepeatingThreadController.start(self,as_dependent=as_dependent,as_daemon=as_daemon,paused=single,skip_first=skip_first)
        if single:
            self.single()
        
def timer_message_notifier(period, tag="timer", listener=None, queue_limit=None, name=None):
    """
    Build a timer notifier thread.
    
    This thread (:class:`TimerThreadController`) sends notification messages to a `listener` thread (caller thread by default) with a given `period`.
    `tag` specifies the message tag. If `queue_limit` is not ``None``, sets the limit to how many notification messages can be in the queue at a given time.
    """
    listener=listener or threadprop.current_controller(require_controller=True)
    # if isinstance(listener, py3.textstring):
    #     listener=wait_for_thread_name(listener)
    def callback():
        message_queue.send_message(listener,tag,on_broken="stop")
    if queue_limit is not None:
        threadprop.as_controller(listener,require_controller=True).limit_queue_length(tag,queue_limit)
    return TimerThreadController(period,callback,name=name)