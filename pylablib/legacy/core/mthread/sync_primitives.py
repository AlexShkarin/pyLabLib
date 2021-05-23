from . import threadprop, notifier
from ..utils import general, observer_pool, py3

import threading

_depends_local=["..utils.general","..utils.observer_pool"]




_defualt_value_sync_tag="sync.notify.value"
class ValueSynchronizer(notifier.ISkippableNotifier):
    _uid_gen=general.UIDGenerator(thread_safe=True)
    def __init__(self, sync=True, note=None, receiver=None):
        notifier.ISkippableNotifier.__init__(self,skippable=True)
        self._receiver=receiver
        self._uid=self._uid_gen()
        if sync is True:
            sync=_defualt_value_sync_tag
        self._sync=sync
        if isinstance(note,py3.textstring):
            def note_func(value):
                try:
                    threadprop.as_controller(self._receiver).add_new_message(note,value,receive_sync="none",schedule_sync="wait_event",on_broken="ignore")
                except (threadprop.NotRunningThreadError,threadprop.NoControllerThreadError):
                    pass
        else:
            note_func=note
        self._note_func=note_func
        self._notify_lock=threading.Lock()
        self._waiting="init"
        self._notifying="init"
        self._blocking_sync=(self._sync=="event")
        if self._sync and (self._blocking_sync or (receiver is threadprop.no_thread_controller) or (receiver is None)):
            self._sync_event=threading.Event()
        else:
            self._sync_event=None
        self._value=None
        
    def _pre_wait(self, *args, **kwargs):
        self._receiver=self._receiver or threadprop.current_controller()
        return True
    def _do_wait(self, timeout=None):
        if self._sync:
            if self._blocking_sync or (self._receiver is threadprop.no_thread_controller):
                return self._sync_event.wait(timeout=timeout)
            else:
                if threadprop.current_controller() is not self._receiver:
                    raise RuntimeError("only receiver can wait for the synchronizer")
                msg=self._receiver.wait_for_message([self._sync],timeout=timeout,filt=(lambda msg: msg.value==self._uid),discard_on_timeout=True)
                return (msg is not None)
        else:
            return True
        
    def _pre_notify(self, value=None):
        self._value=value
    def _post_notify(self, value=None):
        if self._note_func:
            self._note_func(value)
    def _do_notify(self, value=None):
        if self._sync:
            if self._blocking_sync or (self._receiver is threadprop.no_thread_controller):
                self._sync_event.set()
            else:
                try:
                    dest=threadprop.as_controller(self._receiver)
                    dest.add_new_message(self._sync,self._uid,receive_sync="none",schedule_sync="wait_event",on_broken="ignore")
                except (threadprop.NotRunningThreadError,threadprop.NoControllerThreadError):
                    pass
            
    def wait(self, timeout=None):
        return notifier.ISkippableNotifier.wait(self,timeout)
    def notify(self, value=None):
        return notifier.ISkippableNotifier.notify(self,value)
    def get_value(self):
        with self._notify_lock:
            if self._notifying=="init":
                raise RuntimeError("value hasn't been set")
            return self._value
    def uid(self):
        return self._uid


class SyncCall(object):
    def __init__(self, func, args=None, kwargs=None, sync=True, note=None):
        object.__init__(self)
        self.func=func
        self.args=args or []
        self.kwargs=kwargs or {}
        self.synchronizer=ValueSynchronizer(sync=sync,note=note,receiver=threadprop.current_controller())
    def __call__(self):
        res=self.func(*self.args,**self.kwargs)
        self.synchronizer.notify(res)
    def value(self, sync=True, timeout=None, default=None):
        if sync:
            if self.synchronizer.wait(timeout):
                return self.synchronizer.get_value()
            else:
                return default
        else:
            return self.synchronizer
    def wait(self, timeout=None):
        return self.synchronizer.wait(timeout)
    def done(self):
        return self.synchronizer.done_wait()






class BasicSynchronizer(object):
    _sync_tag="sync.notify"
    _uid_gen=general.UIDGenerator(thread_safe=True)
    def __init__(self, receiver=None, blocking_sync=False):
        object.__init__(self)
        self._receiver=receiver
        self._uid=self._uid_gen()
        self._notify_lock=threading.Lock()
        self._waiting=False
        self._notified=False
        self._blocking_sync=blocking_sync
        if self._blocking_sync or (receiver is threadprop.no_thread_controller) or (receiver is None):
            self._sync_event=threading.Event()
        else:
            self._sync_event=None
        
    def _do_wait(self, timeout=None):
        if (self._receiver is threadprop.no_thread_controller) or self._blocking_sync:
            return self._sync_event.wait(timeout=timeout)
        else:
            msg=self._receiver.wait_for_message([self._sync_tag],timeout=timeout,filt=(lambda msg: msg.value==self._uid),discard_on_timeout=True)
            return (msg is not None)
    def _do_notify(self):
        if (self._receiver is threadprop.no_thread_controller) or self._blocking_sync:
            self._sync_event.set()
        else:
            try:
                dest=threadprop.as_controller(self._receiver)
                dest.add_new_message(self._sync_tag,self._uid,receive_sync="none",schedule_sync="wait_event",on_broken="ignore")
            except threadprop.NoControllerThreadError:
                pass
    def wait(self, timeout=None):
        with self._notify_lock:
            if self._notified or self._waiting:
                return True
            self._waiting=True
            self._receiver=self._receiver or threadprop.current_controller()
        return self._do_wait(timeout)
    def notify(self):
        with self._notify_lock:
            if self._notified:
                return
            self._notified=True
            if not self._waiting:
                return
        self._do_notify()
    def uid(self):
        return self._uid





class PendingSynchronizerPool(object):
    def __init__(self, wait_func, notify_func, blocking_sync=False, recursive_calls=False):
        self._wait_func=wait_func
        self._notify_func=notify_func
        self._blocking_sync=blocking_sync
        self._pending={}
        self._state_lock=threading.RLock() if recursive_calls else threading.Lock() 
        
    def pending_num(self):
        with self._state_lock:
            return len(self._pending)
        
    def _extract_pending(self, uid=None):
        if len(self._pending)==0:
            return None
        if uid is None:
            return self._pending.popitem()[1]
        else:
            return self._pending.pop(uid,None)
    def _extract_and_notify(self, uid=None):
        with self._state_lock:
            syncher=self._extract_pending(uid)
        if syncher:
            syncher.notify()
            return True
        return False
    
    def _create_synchronizer(self, blocking_sync=None):
        if blocking_sync is None:
            return BasicSynchronizer(blocking_sync=self._blocking_sync)
        else:
            return BasicSynchronizer(blocking_sync=blocking_sync)
    def wait(self, blocking=True, timeout=None, blocking_sync=None, *args, **vargs):
        with self._state_lock:
            if self._wait_func(*args,**vargs):
                return True
            elif not blocking:
                return False
            else:
                syncher=self._create_synchronizer(blocking_sync)
                self._pending[syncher.uid()]=syncher
        raised_error=True
        try:
            syncher.wait(timeout)
            raised_error=False
        finally:
            notified=not self._extract_and_notify(syncher.uid())
            if notified and raised_error: # has been notified in notify, but raised an error in parallel
                self._extract_and_notify()
        return notified
    def notify(self, *args, **vargs):
        with self._state_lock:
            n=self._notify_func(*args,**vargs)
            if not n:
                return False
            if n<0:
                n=len(self._pending)
            synchers=[self._extract_pending() for _ in range(n)]
        for s in synchers:
            if s:
                s.notify()
        return True
    
    
class ResourceSynchronizerPool(object):
    def __init__(self, grab_func, free_func, blocking_sync=False, recursive_calls=False):
        self._grab_func=grab_func
        self._free_func=free_func
        self._blocking_sync=blocking_sync
        self._pending={}
        self._state_lock=threading.RLock() if recursive_calls else threading.Lock()
        
    def pending_num(self):
        with self._state_lock:
            return len(self._pending)
        
    def _extract_pending(self, uid=None):
        if len(self._pending)==0:
            return None
        if uid is None:
            return self._pending.popitem()[1]
        else:
            return self._pending.pop(uid,None)
    def _extract_and_notify(self, uid=None):
        with self._state_lock:
            syncher=self._extract_pending(uid)
        if syncher:
            syncher.notify()
            return True
        return False
    
    def _create_synchronizer(self, blocking_sync=None):
        if blocking_sync is None:
            return BasicSynchronizer(blocking_sync=self._blocking_sync)
        else:
            return BasicSynchronizer(blocking_sync=blocking_sync)
    def grab(self, blocking=True, timeout=None, blocking_sync=None, *args, **vargs):
        countdown=general.Countdown(timeout)
        while True:
            if countdown.passed():
                blocking=False
            with self._state_lock:
                res=self._grab_func(*args,**vargs)
                if res:
                    return res
                elif not blocking:
                    return False
                else:
                    syncher=self._create_synchronizer(blocking_sync)
                    self._pending[syncher.uid()]=syncher
            raised_error=True
            try:
                if not syncher.wait(countdown.time_left()):
                    blocking=False
                raised_error=False
            finally:
                notified=not self._extract_and_notify(syncher.uid())
                if notified and raised_error: # has been notified in notify, but raised an error in parallel
                    self._extract_and_notify()
    def free(self, *args, **vargs):
        with self._state_lock:
            n=self._free_func(*args,**vargs)
            if not n:
                return False
            if n<0:
                n=len(self._pending)
            synchers=[self._extract_pending() for _ in range(n)]
        for s in synchers:
            if s is not None:
                s.notify()
        return True






class ISyncObject(object):
    def __init__(self):
        object.__init__(self)
    
    def __enter__(self):
        self.acquire()
        return self
    def __exit__(self, *args):
        try:
            self.release()
        except RuntimeError:
            pass
        return False
    def acquire(self, blocking=True, timeout=None, blocking_sync=None):
        raise NotImplementedError("ISyncObject.acquire")
    def release(self):
        raise NotImplementedError("ISyncObject.release")
    
    
class IResourceSyncObject(ISyncObject):
    def __init__(self, blocking_sync=False):
        ISyncObject.__init__(self)
        self._resource=ResourceSynchronizerPool(self._try_acquire,self._try_release,blocking_sync=blocking_sync)
    def _try_acquire(self):
        raise NotImplementedError("IResourceSyncObject._try_acquire")
    def _try_release(self):
        raise NotImplementedError("IResourceSyncObject._try_release")
    def acquire(self, blocking=True, timeout=None, blocking_sync=None):
        return self._resource.grab(blocking=blocking,timeout=timeout,blocking_sync=blocking_sync)
    def release(self):
        return self._resource.free()
    
            
class Lock(IResourceSyncObject):
    def __init__(self, blocking_sync=False):
        IResourceSyncObject.__init__(self,blocking_sync=blocking_sync)
        self._locked=False
    
    def _try_acquire(self):
        if self._locked:
            return False
        self._locked=True
        return True
    def _try_release(self):
        if not self._locked:
            raise RuntimeError("attempting to release a free lock")
        self._locked=False
        return 1
        
        
class RLock(IResourceSyncObject):
    def __init__(self, blocking_sync=False):
        IResourceSyncObject.__init__(self,blocking_sync=blocking_sync)
        self._locked=False
        self._locked_cnt=0
        self._locked_owner=None
    
    def _try_acquire(self):
        cth=threading.current_thread()
        if not self._locked:
            self._locked=True
            self._locked_cnt=1
            self._locked_owner=cth
            return True
        elif self._locked_owner==cth:
            self._locked_cnt=self._locked_cnt+1
            return True
        return False
    def _try_release(self):
        cth=threading.current_thread()
        if not self._locked:
            raise RuntimeError("attempting to release a free lock")
        if cth is not self._locked_owner:
            raise RuntimeError("attempting to release a lock from a non-owner thread")
        self._locked_cnt=self._locked_cnt-1
        if self._locked_cnt>0:
            return 0
        self._locked=False
        self._locked_owner=None
        return 1
    
    def recursion_depth(self):
        return self._locked_cnt
    def full_release(self):
        n=0
        while not self.release():
            n=n+1
        return n+1
    def full_acquire(self, n, blocking=True, timeout=None):
        for _ in range(n):
            self.acquire(blocking=blocking,timeout=timeout)
    
    
class Semaphore(IResourceSyncObject):
    def __init__(self, value, upper_bound=None, blocking_sync=False):
        IResourceSyncObject.__init__(self,blocking_sync=blocking_sync)
        self._value=value
        self._upper_bound=upper_bound
    
    def _try_acquire(self):
        if self._value>0:
            self._value=self._value-1
            return True
        return False
    def _try_release(self):
        if self._upper_bound is not None and self._upper_bound<=self._value:
            raise ValueError("increasing semaphore above upper bound")
        self._value=self._value+1
        return 1
    

class Event(object):
    def __init__(self, flag=False, blocking_sync=False):
        object.__init__(self)
        self._event_state=PendingSynchronizerPool(self._get_flag,self._set_flag,blocking_sync=blocking_sync)
        self._flag=flag
    
    def _get_flag(self):
        return self._flag
    def _set_flag(self, flag):
        self._flag=flag
        return -1 if self._flag else 0
    
    def wait(self, blocking=True, timeout=None, blocking_sync=None):
        return self._event_state.wait(blocking=blocking,timeout=timeout,blocking_sync=blocking_sync)
    def set(self):
        self._event_state.notify(flag=True)
    def clear(self):
        self._event_state.notify(flag=False)
        
        
class VersionEvent(object):
    def __init__(self, blocking_sync=False):
        object.__init__(self)
        self._event_state=ResourceSynchronizerPool(self._check_version,self._update_version,blocking_sync=blocking_sync)
        self._version=0
    
    def _check_version(self, version):
        return self._version>=version
    def _update_version(self):
        self._version=self._version+1
        return -1
    
    def current_version(self):
        with self._event_state._state_lock:
            return self._version
    def wait(self, version=None, blocking=True, timeout=None, blocking_sync=None):
        if version is None:
            version=self.current_version()+1
        return self._event_state.grab(version=version,blocking=blocking,timeout=timeout,blocking_sync=blocking_sync)
    def update(self):
        self._event_state.free()
        
        
class TaskSet(object):
    def __init__(self, blocking_sync=None):
        object.__init__(self)
        self._event_state=PendingSynchronizerPool(self._tasks_done,self._tasks_change,blocking_sync=blocking_sync)
        self._tasks_num=0
    
    def _tasks_done(self):
        return self._tasks_num==0
    def _tasks_change(self, delta=0, value=None):
        new_val=self._tasks_num+delta if value is None else value
        if new_val<0:
            raise ValueError("decreasing number of tasks below zero")
        self._tasks_num=new_val
        return 0 if new_val>0 else -1
    
    def wait(self, blocking=True, timeout=None, blocking_sync=None):
        return self._event_state.wait(blocking=blocking,timeout=timeout,blocking_sync=blocking_sync)
    def set(self, value):
        self._event_state.notify(value=value)
    def get(self):
        return self._tasks_num
    def done(self, number=1):
        self._event_state.notify(delta=-number)
    def add(self, number=1):
        self._event_state.notify(delta=number)
    
    
class Condition(ISyncObject):
    _waiting_uid_gen=general.UIDGenerator(thread_safe=True)
    def __init__(self, lock=None, blocking_sync=False):
        ISyncObject.__init__(self)
        lock=lock or RLock()
        self._condition_lock=lock
        self._owner_lock=threading.Lock()
        self._lock_owner=None
        self._waiting_synch=PendingSynchronizerPool(lambda: False, lambda n: n, blocking_sync=blocking_sync)
    
    def acquire(self, blocking=True, timeout=None, blocking_sync=None):
        if self._condition_lock.acquire(blocking,timeout,blocking_sync=blocking_sync):
            with self._owner_lock:
                self._lock_owner=threading.current_thread()
            return True
        return False
    def release(self):
        with self._owner_lock:
            if self._condition_lock.release():
                self._lock_owner=None
    
    def _acq_cond_lock(self, n):
        if isinstance(self._condition_lock,RLock):
            self._condition_lock.full_acquire(n)
        else:
            self._condition_lock.acquire()
        with self._owner_lock:
            assert self._lock_owner is None # if the lock was acquired, there should be no owner
            self._lock_owner=threading.current_thread()
    def _rel_cond_lock(self):
        with self._owner_lock:
            self._lock_owner=None
        if isinstance(self._condition_lock,RLock):
            return self._condition_lock.full_release()
        else:
            self._condition_lock.release()
    def _check_owner(self):
        cth=threading.current_thread()
        with self._owner_lock:
            if self._lock_owner is not cth:
                raise RuntimeError("method can only be called by the owner of the lock")
    def wait(self, timeout=None, blocking_sync=None):
        self._check_owner()
        n=self._rel_cond_lock()
        result=self._waiting_synch.wait(timeout=timeout,blocking_sync=blocking_sync)
        self._acq_cond_lock(n)
        return result
    def notify(self, n=1):
        self._check_owner()
        self._waiting_synch.notify(n=n)
    def notify_all(self):
        self._check_owner()
        self._waiting_synch.notify(n=-1)
        

class BrokenBarrierError(Exception):
    def __init__(self, msg=None):
        msg=msg or "trying to wait for a broken barrier"
        Exception.__init__(self, msg)
class Barrier(object):
    def __init__(self, parties, blocking_sync=None):
        object.__init__(self)
        self._barrier_state=PendingSynchronizerPool(self._start_waiting,self._stop_waiting,blocking_sync=blocking_sync,recursive_calls=True)
        self._parties=parties
        self._waiting=0
        self._broken=False
        self._state_lock=threading.Lock()
        self._sync_state=None
        self._res_idx=0
    
    def _start_waiting(self):
        self._waiting=self._waiting+1
        if self._waiting==self._parties:
            self._barrier_state.notify()
        return self._waiting==self._parties
    def _stop_waiting(self):
        self._waiting=0
        return -1
    
    class SyncState(object):
        def __init__(self):
            object.__init__(self)
            self.event=threading.Event()
            self.idx=0
            self.notified=0
    def wait(self, blocking=True, timeout=None, blocking_sync=None):
        if self._broken:
            raise BrokenBarrierError()
        with self._state_lock:
            if self._sync_state is None or self._sync_state.idx==self._parties:
                self._sync_state=self.SyncState()
            sync_state=self._sync_state
            idx=sync_state.idx
            sync_state.idx=sync_state.idx+1
        try:
            res=False # so that it's set in the finally block
            res=self._barrier_state.wait(blocking=blocking,timeout=timeout,blocking_sync=blocking_sync)
        finally:
            if not res:
                self._broken=True
                self._barrier_state.notify()
                sync_state.event.set()
        if self._broken:
            sync_state.event.set()
            raise BrokenBarrierError()
        with self._state_lock:
            sync_state.notified=sync_state.notified+1
            if sync_state.notified==self._parties:
                sync_state.event.set()
        sync_state.event.wait()
        if self._broken:
            raise BrokenBarrierError()
        return idx
        

        

class QueueEmptyError(Exception):
    def __init__(self, msg=None):
        msg=msg or "queue empty"
        Exception.__init__(self, msg)
class QueueFullError(Exception):
    def __init__(self, msg=None):
        msg=msg or "queue full"
        Exception.__init__(self, msg)
class Queue(object):
    def __init__(self, max_size=None, blocking_sync=False):
        object.__init__(self)
        self._queue=[]
        self._max_size=max_size
        self._space_res=ResourceSynchronizerPool(self._grab_space, lambda: 1, blocking_sync=blocking_sync)
        self._item_res=ResourceSynchronizerPool(self._grab_item, lambda: 1, blocking_sync=blocking_sync)
    
    def qsize(self):
        return len(self._queue)
    def empty(self):
        return len(self._queue)==0
    def full(self):
        return self._max_size is not None and len(self._queue)>=self._max_size

    def _grab_item(self):
        if len(self._queue)>0:
            res=self._queue.pop(0)
            return (res,)
        else:
            return False
    def _grab_space(self, item):
        if not self.full():
            self._queue.append(item)
            return True
        return False
    
    def get(self, blocking=True, timeout=None, blocking_sync=None):
        item=self._item_res.grab(blocking,timeout,blocking_sync=blocking_sync)
        if item:
            self._space_res.free()
            return item[0]
        else:
            raise QueueEmptyError()
    def put(self, item, blocking=True, timeout=None, blocking_sync=None):
        if self._space_res.grab(blocking,timeout,blocking_sync=blocking_sync,item=item):
            self._item_res.free()
        else:
            raise QueueFullError()
        
        

class ThreadObserverPool(observer_pool.ObserverPool):
    def add_observer(self, callback, name=None, filt=None, priority=0, attr=None, cacheable=False):
        """
        Add the observer callback.

        Same as :meth:`.observer_pool.ObserverPool.add_observer`, but callback can be a string,
        in which case it's interpreted as sending a message to a thread with the given name.
        """
        if isinstance(callback,py3.textstring):
            controller=threadprop.current_controller(require_controller=True)
            callback=controller.add_new_message
        return observer_pool.ObserverPool.add_observer(self,callback,name=name,filt=filt,priority=priority,attr=attr,cacheable=cacheable)
        
        
class StateUIDGenerator(object):
    def __init__(self, thread_safe=True):
        self._value=0
        if thread_safe:
            self._lock=threading.Lock()
        else:
            self._lock=general.DummyResource()
        self._enabled=True
        self._enabled_evt=Event(True)
        
    def disable(self):
        with self._lock:
            self._enabled_evt.clear()
            self._enabled=False
    def enable(self):
        with self._lock:
            self._enabled=True
            self._enabled_evt.set()
    def is_enabled(self):
        with self._lock:
            return self._enabled
    def wait_enabled(self, timeout=None):
        return self._enabled_evt.wait(blocking=(timeout!=0),timeout=timeout)
        
    def up(self, enable=True):
        with self._lock:
            self._value=self._value+1
            if enable:
                self._enabled=True
                self._enabled_evt.set()
            return self._value
    def check(self, value, allow_disabled=False):
        with self._lock:
            if not (self._enabled or allow_disabled):
                return False
            return value is None or self._value==value
    def __call__(self, timeout=None):
        timed_out=(timeout!=0)
        while True:
            with self._lock:
                if self._enabled:
                    return self._value
                if timed_out:
                    return -1
            timed_out=not self.wait_enabled(timeout)