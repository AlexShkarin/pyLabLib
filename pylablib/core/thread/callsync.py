from . import threadprop
from .synchronizing import QThreadNotifier, QMultiThreadNotifier
from ..utils import funcargparse, functions as func_utils

import threading
import time
import collections


### Remote call results ###

class QCallResultSynchronizer(QThreadNotifier):
    def get_progress(self):
        """
        Get the progress of the call execution.

        Can be ``"waiting"`` (call is not done executing), ``"done"`` (call done successfully),
        ``"fail"`` (call failed, probably due to thread being stopped), ``"skip"`` (call was skipped),
        or ``"exception"`` (call raised an exception).
        """
        value=self.value
        if value is None:
            return "waiting"
        tag=value[0]
        if tag=="result":
            return "done"
        return tag
    def is_call_done(self):
        """Check if the call is done"""
        return self.get_progress()=="done"
    def skipped(self):
        """Check if the call was skipped"""
        return self.get_progress()=="skip"
    def failed(self):
        """Check if the call failed"""
        return self.get_progress()=="fail"
    def get_value_sync(self, timeout=None, default=None, error_on_fail=True, error_on_skip=True, pass_exception=True):  # pylint: disable=arguments-differ
        """
        Wait (with the given `timeout`) for the value passed by the notifier

        If ``error_on_fail==True`` and the controlled thread notifies of a fail (usually, if it's stopped before it executed the call),
        raise :exc:`.threadprop.NoControllerThreadError`; otherwise, return `default`.
        If ``error_on_skip==True`` and the call was skipped (e.g., due to full call queue), raise :exc:`.threadprop.SkippedCallError`; otherwise, return `default`.
        If ``pass_exception==True`` and the returned value represents exception, re-raise it in the caller thread; otherwise, return `default`.
        """
        res=super().get_value_sync(timeout=timeout)
        if res is not None:
            kind,value=res  # pylint: disable=unpacking-non-sequence
            if kind=="result":
                return value
            elif kind=="exception":
                if pass_exception:
                    raise value
                else:
                    return default
            elif kind=="skip":
                if error_on_skip:
                    raise threadprop.SkippedCallError()
                return default
            elif kind=="fail":
                if error_on_fail:
                    raise threadprop.NoControllerThreadError("failed executing remote call: controller is stopped")
                return default
            else:
                raise ValueError("unrecognized return value kind: {}".format(kind))
        else:
            if error_on_fail:
                raise threadprop.TimeoutThreadError
            return default

class QDummyResultSynchronizer:
    """Dummy result synchronizer for call which don't require result synchronization (e.g., multicasts)"""
    _not_synchronizer=True
    def notify(self, value):
        pass
dummy_synchronizer=QDummyResultSynchronizer()

class QDirectResultSynchronizer:
    """
    Result "synchronizer" for direct calls.

    Behaves as a regular result synchronizer with an already executed call.
    """
    def __init__(self, value):
        self.value=value
    def get_progress(self):
        """Get the progress of the call execution (always return ``"done"``)"""
        return "done"
    def is_call_done(self):
        """Check if the call is done (always return ``True``)"""
        return True
    def skipped(self):
        """Check if the call was skipped (always return ``False``)"""
        return False
    def failed(self):
        """Check if the call failed (always return ``False``)"""
        return False
    def get_value(self):
        """Return stored value"""
        return self.value
    def get_value_sync(self, timeout=None, default=None, error_on_fail=True, error_on_skip=True, pass_exception=True):  # pylint: disable=unused-argument
        """
        Return stored value.

        Parameters are only for compatibility with :class:`QCallResultSynchronizer`.
        """
        return self.value
    def wait(self, *args, **kwargs):
        """Do nothing (present only for compatibility with :class:`QCallResultSynchronizer`)"""
    def notify(self, *args, **kwargs):
        """Do nothing (present only for compatibility with :class:`QCallResultSynchronizer`)"""
    def waiting(self):
        """Check if waiting is in progress (always return ``False``)"""
        return False
    def done_wait(self):
        """Check if waiting is done (always return ``True``)"""
        return True
    def success_wait(self):
        """Check if waiting is done successfully (always return ``True``)"""
        return True
    def done_notify(self):
        """Check if notifying is done (always return ``True``)"""
        return True
    def waiting_state(self):
        return "done"
    def notifying_state(self):
        return "done"




### Remote call ###

class QScheduledCall:
    """
    Object representing a scheduled remote call.

    Can be executed, skipped, or failed in the target thread, in which case it notifies the result synchronizer (if supplied).

    Args:
        func: callable to be invoked in the destination thread
        args: arguments to be passed to `func`
        kwargs: keyword arguments to be passed to `func`
        silent: if ``True``, silence the exception in the execution thread and simply pass it to the caller thread;
            otherwise, the exception is raised in both threads
        result_synchronizer: result synchronizer object; can be ``None`` (create new :class:`QCallResultSynchronizer`),
            ``"async"`` (no result synchronization), or a :class:`QCallResultSynchronizer` object. 
    """
    Callback=collections.namedtuple("Callback",["func","pass_result","call_on_exception","call_on_unschedule"])
    def __init__(self, func, args=None, kwargs=None, silent=False, result_synchronizer=None):
        self.func=func
        self.args=args or []
        self.kwargs=kwargs or {}
        self.silent=silent
        if result_synchronizer=="async":
            result_synchronizer=dummy_synchronizer
        elif result_synchronizer is None:
            result_synchronizer=QCallResultSynchronizer()
        self.result_synchronizer=result_synchronizer
        self.callbacks=[]
        self._notified=[0] # hack to avoid use of locks ([0] is False, [] is True, use .pop() to atomically check and change)
        self.state="wait"
    def _check_notified(self):
        try:
            self._notified.pop()
            return False
        except IndexError:
            return True
    def execute(self, silent=None):
        """Execute the call and notify the result synchronizer (invoked by the destination thread)"""
        if self._check_notified():
            return
        try:
            res=("fail",None)
            res=("result",self.func(*self.args,**self.kwargs))
        except Exception as e:  # pylint: disable=broad-except
            res=("exception",e)
            if not (self.silent if silent is None else silent):
                raise
        finally:
            self.state=res[0]
            for c in self.callbacks:
                if c.call_on_exception or c.call_on_unschedule or res[0]=="result":
                    if c.pass_result:
                        c.func(res[1] if res[0]=="result" else None)
                    else:
                        c.func()
            self.result_synchronizer.notify(res)
    def add_callback(self, callback, pass_result=True, call_on_exception=False, call_on_unschedule=False, front=False):
        """
        Set the callback to be executed after the main call is done.
        
        If ``pass_result==True``, pass function result to the callback (or ``None`` if call failed); otherwise, pass no arguments.
        If ``call_on_exception==True``, call it even if the original call raised an exception.
        If ``call_on_unschedule==True``, call it for any call unscheduling event, including using :meth:`skip` or :meth:`fail` methods
        (this effectively ignores `call_on_exception`, since the callback is called regardless of the exception).
        If ``front==True``, add the callback in the front of the line (executes first).
        """
        cb=self.Callback(callback,pass_result,call_on_exception,call_on_unschedule)
        if front:
            self.callbacks.insert(0,cb)
        else:
            self.callbacks.append(cb)
    def fail(self):
        """Notify that the call is failed (invoked by the destination thread)"""
        if self._check_notified():
            return
        self.state="fail"
        for c in self.callbacks:
            if c.call_on_unschedule:
                c.func()
        self.result_synchronizer.notify(("fail",None))
    def skip(self):
        """Notify that the call is skipped (invoked by the destination thread)"""
        if self._check_notified():
            return
        self.state="skip"
        for c in self.callbacks:
            if c.call_on_unschedule:
                c.func()
        self.result_synchronizer.notify(("skip",None))




### Call schedulers ###

TDefaultCallInfo=collections.namedtuple("TDefaultCallInfo",["call_time"])
class QScheduler:
    """
    Generic call scheduler.

    Two methods are used by the external scheduling routines: :meth:`build_call` to create a :class:`QScheduledCall` with appropriate parameters,
    and :meth:`schedule`, which takes a call and schedules it.
    The :meth:`schedule` method should return ``True`` if the scheduling was successful (at least, for now), and ``False`` otherwise.

    Args:
        call_info_argname: if not ``None``, supplies a name of a keyword argument
            via which call info (generated by :meth:`build_call_info`) is passed on function call
    """
    def __init__(self, call_info_argname=None):
        self.call_info_argname=call_info_argname
    def build_call_info(self):
        """Build call info tuple which can be passed to scheduled calls"""
        return TDefaultCallInfo(time.time())
    def build_call(self, func, args=None, kwargs=None, callback=None, pass_result=True, callback_on_exception=True, sync_result=True):
        """
        Build :class:`QScheduledCall` for subsequent scheduling.

        Args:
            func: function to be called
            args: arguments to be passed to `func`
            kwargs: keyword arguments to be passed to `func`
            callback: optional callback to be called when `func` is done
            pass_result (bool): if ``True``, pass `func` result as a single argument to the callback; otherwise, give no arguments
            callback_on_exception (bool): if ``True``, execute the callback on call fail or skip (if it requires an argument, ``None`` is supplied);
                otherwise, only execute it if the call was successful
            sync_result: if ``True``, the call has a default result synchronizer; otherwise, no synchronization is made.
        """
        result_synchronizer=None if sync_result else "async"
        scheduled_call=QScheduledCall(func,args,kwargs,result_synchronizer=result_synchronizer)
        if self.call_info_argname:
            scheduled_call.kwargs[self.call_info_argname]=self.build_call_info()
        if callback is not None:
            scheduled_call.add_callback(callback,pass_result=pass_result,call_on_exception=callback_on_exception)
        return scheduled_call
    def schedule(self, call):  # pylint: disable=unused-argument
        """Schedule the call"""
        return False
    def clear(self):
        """Clear the scheduler"""
        pass



class QDirectCallScheduler(QScheduler):
    """
    Simplest call scheduler: directly executes the calls on scheduling in the scheduling thread.

    Args:
        call_info_argname: if not ``None``, supplies a name of a keyword argument
            via which call info (generated by :meth:`QScheduler.build_call_info`) is passed on function call
    """
    def build_call(self, func, args=None, kwargs=None, callback=None, pass_result=True, callback_on_exception=True, sync_result=False):
        return super().build_call(func,args=args,kwargs=kwargs,
            callback=callback,pass_result=pass_result,callback_on_exception=callback_on_exception,sync_result=sync_result)
    def schedule(self, call):
        call.execute()
        return True



class QQueueScheduler(QScheduler):
    """
    Call scheduler with a builtin call queue.

    Supports placing the calls and retrieving them (from the destination thread).
    Has ability to skip some calls if, e.g., the queue is too full. Whether the call should be skipped is determined
    by :meth:`can_schedule` (should be overloaded in subclasses). 
    Used as a default command scheduler.

    Args:
        on_full_queue: action to be taken if the call can't be scheduled (i.e., :meth:`can_schedule` returns ``False``); can be
            ``"skip_current"`` (skip the call which is being scheduled),
            ``"skip_newest"`` (skip the most recent call; place the current)
            ``"skip_oldest"`` (skip the oldest call in the queue; place the current),
            ``"call_current"`` (execute the call which is being scheduled immediately in the caller thread),
            ``"call_newest"`` (execute the most recent call immediately in the caller thread), 
            ``"call_oldest"`` (execute the oldest call in the queue immediately in the caller thread), or
            ``"wait"`` (wait until the call can be scheduled, which is checked after every call removal from the queue; place the call)
        call_info_argname: if not ``None``, supplies a name of a keyword argument
            via which call info (generated by :meth:`QScheduler.build_call_info`) is passed on function call

    Methods to overload:
        - :meth:`can_schedule`: check if the call can be scheduled
        - :meth:`call_added`: called when a new call has been added to the queue
        - :meth:`call_popped`: called when a call has been removed from the queue (either for execution, or for skipping)
    """
    def __init__(self, on_full_queue="skip_current", call_info_argname=None):
        super().__init__(call_info_argname=call_info_argname)
        self.call_queue=collections.deque()
        funcargparse.check_parameter_range(on_full_queue,"on_full_queue",{"skip_current","skip_newest","skip_oldest","call_current","call_newest","call_oldest","wait"})
        self.on_full_queue=on_full_queue
        self.lock=threading.Lock()
        self.call_popped_notifier=QMultiThreadNotifier() if on_full_queue=="wait" else None
        self.working=True
        self._last_popped=[None]
    def can_schedule(self, call):  # pylint: disable=unused-argument
        """Check if the call can be scheduled"""
        return True
    def call_added(self, call):
        """Called whenever `call` has been added to the queue"""
    def call_popped(self, call, idx):
        """
        Called whenever `call` has been removed from the queue
        
        `idx` determines the call position within the queue.
        """
    def _add_call(self, call):
        self.call_queue.append(call)
        self.call_added(call)
    def _pop_call(self, head=False):
        try:
            call=self.call_queue.popleft() if head else self.call_queue.pop()
            if self.call_popped_notifier is not None:
                self.call_popped_notifier.notify()
            self.call_popped(call,0 if head else -1)
            self._last_popped=[self._last_popped[-1],call]
            return call
        except IndexError:
            return None
    def schedule(self, call):
        """Schedule a call"""
        if not self.working:
            call.fail()
            return
        if self.on_full_queue=="wait":
            while True:
                with self.lock:
                    if self.can_schedule(call):
                        self._add_call(call)
                        return True
                    elif not self.working:
                        return
                    wait_n=self.call_popped_notifier.wait(-1)
                self.call_popped_notifier.wait(wait_n)
        scheduled=True
        skipped_call=None
        execute_call=None
        with self.lock:
            if self.can_schedule(call):
                self._add_call(call)
            elif self.on_full_queue=="skip_newest":
                skipped_call=self._pop_call()
                self._add_call(call)
            elif self.on_full_queue=="skip_oldest":
                skipped_call=self._pop_call(head=True)
                self._add_call(call)
            elif self.on_full_queue=="skip_current":
                skipped_call=call
                scheduled=False
            elif self.on_full_queue=="call_newest":
                execute_call=self._pop_call()
                self._add_call(call)
            elif self.on_full_queue=="call_oldest":
                execute_call=self._pop_call(head=True)
                self._add_call(call)
            elif self.on_full_queue=="call_current":
                execute_call=call
            else:
                scheduled=False
        if skipped_call is not None:
            skipped_call.skip()
        if execute_call is not None:
            execute_call.execute()
        return scheduled
    def pop_call(self):
        """
        Pop the call from the queue head.

        If the queue is empty, return ``None``
        """
        with self.lock:
            return self._pop_call(head=True)
    def unschedule(self, call):
        """
        Unschedule a given call.

        Designed for joint queue operation, so the call is not notified (assume that it has been already notified elsewhere).
        """
        if call in self._last_popped:
            return False
        with self.lock:
            try:
                idx=self.call_queue.index(call)
                del self.call_queue[idx]
                if self.call_popped_notifier is not None:
                    self.call_popped_notifier.notify()
                self.call_popped(call,idx)
                return True
            except ValueError:
                return False
    def has_calls(self):
        """Check if there are queued calls"""
        return bool(self.call_queue)
    def __len__(self):
        return len(self.call_queue)
    def clear(self, close=True):  # pylint: disable=arguments-differ
        """
        Clear the call queue.

        If ``close==True``, mark the queue as closed (any attempt to schedule more calls fails automatically) and fail all calls in the queue;
        otherwise, skip all calls currently in the queue.
        """
        if close:
            self.working=False
        with self.lock:
            all_calls=[]
            c=self._pop_call(head=True)
            while c is not None:
                all_calls.append(c)
                c=self._pop_call()
        for c in all_calls:
            if close:
                c.fail()
            else:
                c.skip()
        if self.call_popped_notifier is not None:
            self.call_popped_notifier.notify()
                
class QQueueLengthLimitScheduler(QQueueScheduler):
    """
    Queued call scheduler with a length limit.

    Args:
        max_len: maximal queue length; non-positive values are interpreted as no limit
            can also be a tuple ``(arg_name, max_len)``, in which case the length is calculated separately
            for every value of the parameter ``arg_name`` supplied to the method
        on_full_queue: action to be taken if the call can't be scheduled (the queue is full); can be
            ``"skip_current"`` (skip the call which is being scheduled),
            ``"skip_newest"`` (skip the most recent call; place the current)
            ``"skip_oldest"`` (skip the oldest call in the queue; place the current),
            ``"call_current"`` (execute the call which is being scheduled immediately in the caller thread),
            ``"call_newest"`` (execute the most recent call immediately in the caller thread), 
            ``"call_oldest"`` (execute the oldest call in the queue immediately in the caller thread), or
            ``"wait"`` (wait until the call can be scheduled, which is checked after every call removal from the queue; place the call)
        call_info_argname: if not ``None``, supplies a name of a keyword argument
            via which call info (generated by :meth:`QScheduler.build_call_info`) is passed on function call
    """
    def __init__(self, max_len=1, on_full_queue="skip_current", call_info_argname=None):
        super().__init__(on_full_queue=on_full_queue,call_info_argname=call_info_argname)
        self.max_len_arg,self.max_len=max_len if isinstance(max_len,tuple) else (None,max_len)
        self._arg_lens={}
        self._arg_par=None
    def change_max_len(self, max_len):
        """Change maximal length of the call queue (doesn't affect already scheduled calls)"""
        self.max_len_arg,self.max_len=max_len if isinstance(max_len,tuple) else (None,max_len)
    def get_current_len(self):
        """Get current number of calls in the queue"""
        return len(self.call_queue)
    def _get_arg_value(self, call, name):
        if self._arg_par is None or self._arg_par[0] is not call.func:
            sig=func_utils.funcsig(call.func)
            self._arg_par=(call.func,sig)
        try:
            return self._arg_par[1].arg_value(name,args=call.args,kwargs=call.kwargs)
        except TypeError:
            return None
    def call_added(self, call):
        if self.max_len_arg is not None:
            arg_val=self._get_arg_value(call,self.max_len_arg)
            self._arg_lens[arg_val]=self._arg_lens.get(arg_val,0)+1
    def call_popped(self, call, idx):
        if self.max_len_arg is not None:
            arg_val=self._get_arg_value(call,self.max_len_arg)
            self._arg_lens[arg_val]-=1
    def can_schedule(self, call):
        if self.max_len<=0:
            return True
        if self.max_len_arg is not None:
            arg_val=self._get_arg_value(call,self.max_len_arg)
            l=self._arg_lens.setdefault(arg_val,0)
        else:
            l=len(self.call_queue)
        return l<self.max_len

class QQueueSizeLimitScheduler(QQueueScheduler):
    """
    Queued call scheduler with a generic size limit; similar to :class:`QQueueLengthLimitScheduler`,
    but more flexible and can implement more restrictions (e.g., queue length and arguments RAM size).

    Args:
        max_size: maximal total size of the arguments; can be either a single number, or a tuple (if several different size metrics are involved);
            non-positive values are interpreted as no limit
        size_calc: function that takes a single argument (call to be placed) and returns its size; can be either a single number,
            or a tuple (if several different size metrics are involved);
            by default, simply returns 1, which makes the scheduler behavior identical to :class:`QQueueLengthLimitScheduler`
        on_full_queue: action to be taken if the call can't be scheduled (the queue is full); can be
            ``"skip_current"`` (skip the call which is being scheduled),
            ``"skip_newest"`` (skip the most recent call; place the current)
            ``"skip_oldest"`` (skip the oldest call in the queue; place the current),
            ``"call_current"`` (execute the call which is being scheduled immediately in the caller thread),
            ``"call_newest"`` (execute the most recent call immediately in the caller thread), 
            ``"call_oldest"`` (execute the oldest call in the queue immediately in the caller thread), or
            ``"wait"`` (wait until the call can be scheduled, which is checked after every call removal from the queue; place the call)
        call_info_argname: if not ``None``, supplies a name of a keyword argument
            via which call info (generated by :meth:`QScheduler.build_call_info`) is passed on function call
    """
    def __init__(self, max_size=1, size_calc=None, on_full_queue="skip_current", call_info_argname=None):
        super().__init__(on_full_queue=on_full_queue,call_info_argname=call_info_argname)
        self.max_size=funcargparse.as_sequence(max_size)
        self.size_queues=tuple([[] for _ in self.max_size])
        self.size_calc=size_calc
    def change_max_size(self, max_size):
        """Change size restrictions"""
        self.max_size=funcargparse.as_sequence(max_size)
    def get_current_size(self):
        """Get current size metrics"""
        return tuple([sum(q) for q in self.size_queues])
    def _get_size(self, call):
        if self.size_calc is not None:
            return self.size_calc(call)
        return 1
    def call_added(self, call):
        size=funcargparse.as_sequence(self._get_size(call))
        for s,q in zip(size,self.size_queues):
            q.append(s)
    def call_popped(self, call, idx):
        for q in self.size_queues:
            q.pop(idx)
    def can_schedule(self, call):
        for ms,q in zip(self.max_size,self.size_queues):
            if ms>0 and sum(q)>=ms:
                return False
        return True



def schedule_multiple_queues(call, queues):
    """
    Schedule the call simultaneously in several queues.

    Go through queues in the given order and schedule call in every one of them.
    If one of the schedules failed or the call has been executed there, unschedule it from all the previous queues
    and return ``False``; otherwise, return ``True``.
    """
    if len(queues)==0:
        return True
    if len(queues)==1:
        return queues[0].schedule(call) and call.state=="wait"
    def queue_unscheduler(queue):
        return lambda: queue.unschedule(call)
    added=[]
    complete=False
    try:
        for q in queues:
            call.add_callback(queue_unscheduler(q),pass_result=False,call_on_unschedule=True,front=True)
            q.schedule(call)
            if call.state!="wait": # skipped or executed
                return False
            added.append(q)
        complete=True
        return True
    finally:
        if not complete and added:
            added[-1].unschedule(call) # the previous ones should be unscheduled via the callback


class QMultiQueueScheduler:
    """
    Wrapper around :func:`schedule_multiple_queues` which acts as a single scheduler.

    Support additional notifiers, which are called if the scheduling is successful
    (e.g., to notify and wake up the destination thread).
    """
    def __init__(self, schedulers, notifiers):
        self.schedulers=schedulers
        self.notifiers=notifiers
    def build_call(self, *args, **kwargs):
        return self.schedulers[0].build_call(*args,**kwargs)
    def schedule(self, call):
        if schedule_multiple_queues(call,self.schedulers):
            for n in self.notifiers:
                n()


class QThreadCallScheduler(QScheduler):
    """
    Call scheduler via thread calls (:meth:`.QThreadController.call_in_thread_callback`)

    Args:
        thread: destination thread (by default, thread which creates the scheduler)
        tag: if supplied, send the call in a message with the given tag; otherwise, use the interrupt call (generally, higher priority method).
        priority: message priority (only when `tag` is not ``None``)
        interrupt: whether the call is an interrupt (call inside any loop, e.g., during waiting or sleeping), or it should be called in the main event loop
        call_info_argname: if not ``None``, supplies a name of a keyword argument
            via which call info (generated by :meth:`QScheduler.build_call_info`) is passed on function call
    """
    def __init__(self, thread=None, tag=None, priority=0, interrupt=True, call_info_argname=None):
        super().__init__(call_info_argname=call_info_argname)
        self.thread=thread or threadprop.current_controller()
        self.tag=tag
        self.priority=priority
        self.interrupt=interrupt
    def schedule(self, call):
        self.thread._place_call(call,tag=self.tag,priority=self.priority,interrupt=self.interrupt)
        return True

class QMulticastThreadCallScheduler(QThreadCallScheduler):
    """
    Extended call scheduler via thread calls, which can limit number of queued calls.

    Args:
        thread: destination thread (by default, thread which creates the scheduler)
        limit_queue: call queue limit (non-positive numbers are interpreted as no limit)
        tag: if supplied, send the call in a message with the given tag; otherwise, use the interrupt call (generally, higher priority method).
        priority: message priority (only when `tag` is not ``None``)
        interrupt: whether the call is an interrupt (call inside any loop, e.g., during waiting or sleeping), or it should be called in the main event loop
        call_info_argname: if not ``None``, supplies a name of a keyword argument
            via which call info (generated by :meth:`QScheduler.build_call_info`) is passed on function call
    """
    def __init__(self, thread=None, limit_queue=1, tag=None, priority=0, interrupt=True, call_info_argname=None):
        super().__init__(thread,tag=tag,priority=priority,interrupt=interrupt,call_info_argname=call_info_argname)
        self.limit_queue=limit_queue or 0
        self.queue_cnt=0
        self.queue_cnt_lock=threading.Lock()
    def _call_done(self):
        with self.queue_cnt_lock:
            self.queue_cnt-=1
    def schedule(self, call):
        if self.limit_queue<=0 or self.queue_cnt<self.limit_queue:
            with self.queue_cnt_lock:
                self.queue_cnt+=1
            call.add_callback(self._call_done,pass_result=False,call_on_exception=True,front=True)
            return super().schedule(call)
        else:
            call.skip()
            return False