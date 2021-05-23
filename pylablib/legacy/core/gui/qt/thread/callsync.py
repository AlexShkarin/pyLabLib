from . import threadprop
from .synchronizing import QThreadNotifier, QMultiThreadNotifier
from ....utils import general, funcargparse

import threading, time, collections

_depends_local=[".synchronizing"]

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
    def skipped(self):
        """Check if the call was skipped"""
        return self.get_progress()=="skip"
    def failed(self):
        """Check if the call failed"""
        return self.get_progress()=="fail"
    def get_value_sync(self, timeout=None, default=None, error_on_fail=True, error_on_skip=True, pass_exception=True):
        """
        Wait (with the given `timeout`) for the value passed by the notifier

        If ``error_on_fail==True`` and the controlled thread notifies of a fail (usually, if it's stopped before it executed the call),
        raise :exc:`.qt.thread.threadprop.NoControllerThreadError`; otherwise, return `default`.
        If ``error_on_skip==True`` and the call was skipped (e.g., due to full call queue), raise :exc:`.qt.thread.threadprop.SkippedCallError`; otherwise, return `default`.
        If ``pass_exception==True`` and the returned value represents exception, re-raise it in the caller thread; otherwise, return `default`.
        """
        res=QThreadNotifier.get_value_sync(self,timeout=timeout)
        if res is not None:
            kind,value=res
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

class QDummyResultSynchronizer(object):
    """Dummy result synchronizer for call which don't require result synchronization (e.g., signals)"""
    def notify(self, value):
        pass

class QScheduledCall(object):
    """
    Object representing a scheduled remote call.

    Args:
        func: callable to be invoked in the destination thread
        args: arguments to be passed to `func`
        kwargs: keyword arguments to be passed to `func`
        result_synchronizer: result synchronizer object; can be ``None`` (create new :class:`QCallResultSynchronizer`),
            ``"async"`` (no result synchronization), or a :class:`QCallResultSynchronizer` object. 
    """
    TCallback=collections.namedtuple("TCallback",["func","pass_result","call_on_fail"])
    def __init__(self, func, args=None, kwargs=None, result_synchronizer=None):
        object.__init__(self)
        self.func=func
        self.args=args or []
        self.kwargs=kwargs or {}
        if result_synchronizer=="async":
            result_synchronizer=QDummyResultSynchronizer()
        elif result_synchronizer is None:
            result_synchronizer=QCallResultSynchronizer()
        self.result_synchronizer=result_synchronizer
        self.callbacks=[]
        self._notified=[0] # hack to avoid use of locks ([0] is False, [] is True, use .pop() to atomically check and change)
    def _check_notified(self):
        try:
            self._notified.pop()
            return False
        except IndexError:
            return True
    def __call__(self):
        if self._check_notified():
            return
        try:
            res=("fail",None)
            res=("result",self.func(*self.args,**self.kwargs))
        except Exception as e:
            res=("exception",e)
            raise
        finally:
            for c in self.callbacks:
                if c.call_on_fail or res[0]=="result":
                    if c.pass_result:
                        c.func(res[1] if res[0]=="result" else None)
                    else:
                        c.func()
            self.result_synchronizer.notify(res)
    def add_callback(self, callback, pass_result=True, call_on_fail=False, position=None):
        """
        Set the callback to be executed after the main call is done.
        
        Callback is not provided with any arguments.
        If ``pass_result==True``, pass function result to the callback (or ``None`` if call failed); otherwise, pass no arguments.
        If ``callback_on_fail==True``, call it even if the original call raised an exception.
        `position` specifies callback position in the call list (by default, end of the list).
        """
        cb=self.TCallback(callback,pass_result,call_on_fail)
        if position is None:
            self.callbacks.append(cb)
        else:
            self.callbacks.insert(position,cb)
    def fail(self):
        """Notify that the call is failed (invoked by the destination thread)"""
        if self._check_notified():
            return
        self.result_synchronizer.notify(("fail",None))
    def skip(self):
        """Notify that the call is skipped (invoked by the destination thread)"""
        if self._check_notified():
            return
        self.result_synchronizer.notify(("skip",None))




### Call schedulers ###

TDefaultCallInfo=collections.namedtuple("TDefaultCallInfo",["call_time"])
class QScheduler(object):
    """
    Generic call scheduler.

    Two methods are used by the external scheduling routines: :meth:`build_call` to create a :class:`QScheduledCall` with appropriate parameters,
    and :meth:`schedule`, which takes a call and schedules it.
    The :meth:`schedule` method should return ``True`` if the scheduling was successfull (at least, for now), and ``False`` otherwise.

    Args:
        call_info_argname: if not ``None``, supplies a name of a keyword argument
            via which call info (generated by :meth:`build_call_info`) is passed on function call
    """
    def __init__(self, call_info_argname=None):
        object.__init__(self)
        self.call_info_argname=call_info_argname
    def build_call_info(self):
        """Build call info tuple which can be passed to scheduled calls"""
        return TDefaultCallInfo(time.time())
    def build_call(self, func, args=None, kwargs=None, callback=None, pass_result=True, callback_on_fail=True, sync_result=True):
        """
        Build :class:`QScheduledCall` for subsequent scheduling.

        Args:
            func: function to be called
            args: arguments to be passed to `func`
            kwargs: keyword arguments to be passed to `func`
            callback: optional callback to be called when `func` is done
            pass_result (bool): if ``True``, pass `func` result as a single argument to the callback; otherwise, give no arguments
            callback_on_fail (bool): if ``True``, execute the callback on call fail or skip (if it requires an argument, ``None`` is supplied);
                otherwise, only execute it if the call was successfull
            sync_result: if ``True``, the call has a default result synchronizer; otherwise, no synchronization is made.
        """
        result_synchronizer=None if sync_result else "async"
        scheduled_call=QScheduledCall(func,args,kwargs,result_synchronizer=result_synchronizer)
        if self.call_info_argname:
            scheduled_call.kwargs[self.call_info_argname]=self.build_call_info()
        if callback is not None:
            scheduled_call.add_callback(callback,pass_result=pass_result,call_on_fail=callback_on_fail)
        return scheduled_call
    def schedule(self, call):
        """Schedule the call"""
        return False
    def clear(self):
        """Clear the scheduler"""
        pass



class QDirectCallScheduler(QScheduler):
    """
    Simplest call scheduler: directly executes the calls on scheduling

    Args:
        call_info_argname: if not ``None``, supplies a name of a keyword argument
            via which call info (generated by :meth:`QScheduler.build_call_info`) is passed on function call
    """
    def build_call(self, func, args=None, kwargs=None, callback=None, pass_result=True, callback_on_fail=True, sync_result=False):
        return QScheduler.build_call(self,func,args=args,kwargs=kwargs,
            callback=callback,pass_result=pass_result,callback_on_fail=callback_on_fail,sync_result=sync_result)
    def schedule(self, call):
        call()
        return True



class QQueueScheduler(QScheduler):
    """
    Call scheduler with a builtin call queue.

    Supports placing the calls and retrieving them (from the destination thread).
    Has ability to skip some calls if, e.g., the queue is too full. Whether the call should be skipped is determined
    by :meth:`can_schedule` (should be overloaded in subclasses). 
    Used as a default command scheduler.

    Args:
        on_full_queue: action to be taken if the call can't be scheduled (i.e., :meth:`can_schedule` returns ``False``);
            can be ``"skip_current"`` (skip the call which is being scheduled), ``"skip_newest"`` (skip the most recent call; place the current)
            ``"skip_oldest"`` (skip the oldest call in the queue; place the current),
            ``"wait"`` (wait until the call can be scheduled, which is checked after every call removal from the queue; place the call),
            or ``"call"`` (execute the call directly in the calling thread; should be used with caution).
        call_info_argname: if not ``None``, supplies a name of a keyword argument
            via which call info (generated by :meth:`QScheduler.build_call_info`) is passed on function call

    Methods to overload:
        ``can_schedule``: check if the call can be scheduled
        ``call_added``: called when a new call has been added to the queue
        ``call_popped``: called when a call has been removed from the queue (either for execution, or for skipping)
    """
    def __init__(self, on_full_queue="current", call_info_argname=None):
        QScheduler.__init__(self,call_info_argname=call_info_argname)
        self.call_queue=collections.deque()
        funcargparse.check_parameter_range(on_full_queue,"on_full_queue",{"skip_current","skip_newest","skip_oldest","call","wait"})
        self.on_full_queue=on_full_queue
        self.lock=threading.Lock()
        self.call_popped_notifier=QMultiThreadNotifier() if on_full_queue=="wait" else None
        self.working=True
    def can_schedule(self, call):
        """Check if the call can be scheduled"""
        return True
    def call_added(self, call):
        """Called whenever `call` has been added to the queue"""
        pass
    def call_popped(self, call, head):
        """
        Called whenever `call` has been removed from the queue
        
        `head` determines whether the call has been removed from the queue head, or from the queue tail.
        """
        pass
    def _add_call(self, call):
        self.call_queue.append(call)
        self.call_added(call)
    def _pop_call(self, head=False):
        try:
            call=self.call_queue.popleft() if head else self.call_queue.pop()
            if self.call_popped_notifier is not None:
                self.call_popped_notifier.notify()
            self.call_popped(call,head)
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
            else:
                scheduled=False
        if skipped_call is not None:
            skipped_call.skip()
        if self.on_full_queue=="call" and not scheduled:
            call()
            scheduled=True
        return scheduled
    def pop_call(self):
        """
        Pop the call from the queue head.

        If the queue is empty, return ``None``
        """
        with self.lock:
            return self._pop_call(head=True)
    def has_calls(self):
        """Check if there are queued calls"""
        return bool(self.call_queue)
    def clear(self, close=True):
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
        on_full_queue: action to be taken if the call can't be scheduled (the queue is full);
            can be ``"skip_current"`` (skip the call which is being scheduled), ``"skip_newest"`` (skip the most recent call; place the current)
            ``"skip_oldest"`` (skip the oldest call in the queue; place the current), ``"wait"`` (wait until the queue has space; place the call),
            or ``"call"`` (execute the call directly in the calling thread; should be used with caution).
        call_info_argname: if not ``None``, supplies a name of a keyword argument
            via which call info (generated by :meth:`QScheduler.build_call_info`) is passed on function call
    """
    def __init__(self, max_len=1, on_full_queue="skip_current", call_info_argname=None):
        QQueueScheduler.__init__(self,on_full_queue=on_full_queue,call_info_argname=call_info_argname)
        self.max_len=max_len
    def change_max_len(self, max_len):
        """Change maximal length of the call queue (doesn't affect already scheduled calls)"""
        self.max_len=max_len
    def get_current_len(self):
        """Get current number of calls in the queue"""
        return len(self.call_queue)
    def can_schedule(self, call):
        return self.max_len<=0 or len(self.call_queue)<self.max_len

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
        on_full_queue: action to be taken if the call can't be scheduled (the queue is full);
            can be ``"skip_current"`` (skip the call which is being scheduled), ``"skip_newest"`` (skip the most recent call; place the current)
            ``"skip_oldest"`` (skip the oldest call in the queue; place the current), ``"wait"`` (wait until the queue has space; place the call),
            or ``"call"`` (execute the call directly in the calling thread; should be used with caution).
        call_info_argname: if not ``None``, supplies a name of a keyword argument
            via which call info (generated by :meth:`QScheduler.build_call_info`) is passed on function call
    """
    def __init__(self, max_size=1, size_calc=None, on_full_queue="skip_current", call_info_argname=None):
        QQueueScheduler.__init__(self,on_full_queue=on_full_queue,call_info_argname=call_info_argname)
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
    def call_popped(self, call, head):
        for q in self.size_queues:
            q.pop(0 if head else -1)
    def can_schedule(self, call):
        for ms,q in zip(self.max_size,self.size_queues):
            if ms>0 and sum(q)>=ms:
                return False
        return True




class QThreadCallScheduler(QScheduler):
    """
    Call scheduler via thread calls (:meth:`.QThreadController.call_in_thread_callback`)

    Args:
        thread: destination thread (by default, thread which creates the scheduler)
        tag: if supplied, send the call in a message with the given tag; otherwise, use the interrupt call (generally, higher priority method).
        priority: message priority (only when `tag` is not ``None``)
        call_info_argname: if not ``None``, supplies a name of a keyword argument
            via which call info (generated by :meth:`QScheduler.build_call_info`) is passed on function call
    """
    def __init__(self, thread=None, tag=None, priority=0, call_info_argname=None):
        QScheduler.__init__(self,call_info_argname=call_info_argname)
        self.thread=thread or threadprop.current_controller()
        self.tag=tag
        self.priority=priority
    def schedule(self, call):
        self.thread._place_call(call,tag=self.tag,priority=self.priority)
        return True

class QSignalThreadCallScheduler(QThreadCallScheduler):
    """
    Extended call scheduler via thread calls, which can limit number of queued calls.

    Args:
        thread: destination thread (by default, thread which creates the scheduler)
        limit_queue: call queue limit (non-positive numbers are interpreted as no limit)
        tag: if supplied, send the call in a message with the given tag; otherwise, use the interrupt call (generally, higher priority method).
        priority: message priority (only when `tag` is not ``None``)
        call_info_argname: if not ``None``, supplies a name of a keyword argument
            via which call info (generated by :meth:`QScheduler.build_call_info`) is passed on function call
    """
    def __init__(self, thread=None, limit_queue=1, tag=None, priority=0, call_info_argname=None):
        QThreadCallScheduler.__init__(self,thread,tag=tag,priority=priority,call_info_argname=call_info_argname)
        self.limit_queue=limit_queue
        self.queue_cnt=0
        self.queue_cnt_lock=threading.Lock()
    def _call_done(self):
        with self.queue_cnt_lock:
            self.queue_cnt-=1
    def schedule(self, call):
        if self.limit_queue<=0 or self.queue_cnt<self.limit_queue:
            with self.queue_cnt_lock:
                self.queue_cnt+=1
            call.add_callback(self._call_done,pass_result=False,call_on_fail=True,position=0)
            return QThreadCallScheduler.schedule(self,call)
        else:
            call.skip()
            return False