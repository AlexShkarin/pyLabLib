from . import threadprop
from .notifier import ISkippableNotifier
from ..utils import general

import threading


class QThreadNotifier(ISkippableNotifier):
    """
    Wait-notify thread synchronizer for controlled Qt threads based on :class:`.notifier.ISkippableNotifier`.

    Like :class:`.notifier.ISkippableNotifier`, the main functions are :meth:`.ISkippableNotifier.wait` (wait in a message loop until notified or until timeout expires)
    and :meth:`.ISkippableNotifier.notify` (notify the waiting thread). Both of these can only be called once and will raise and error on repeating calls.
    Along with notifying a variable can be passed, which can be accessed using :meth:`get_value` and :meth:`get_value_sync`.

    Args:
        skippable (bool): if ``True``, allows for skippable wait events
            (if :meth:`.ISkippableNotifier.notify` is called before :meth:`.ISkippableNotifier.wait`, neither methods are actually called).
    """
    _uid_gen=general.UIDGenerator(thread_safe=True)
    _notify_tag="#sync.notifier"
    def __init__(self, skippable=True):
        super().__init__(skippable=skippable)
        self._uid=None
        self.value=None
    def _pre_wait(self, *args, **kwargs):  # pylint: disable=unused-argument
        self._controller=threadprop.current_controller(require_controller=True)
        self._uid=self._uid_gen()
        return True
    def _do_wait(self, timeout=None):  # pylint: disable=arguments-differ
        try:
            self._controller.wait_for_sync(self._notify_tag,self._uid,timeout=timeout)
            return True
        except threadprop.TimeoutThreadError:
            return False
    def _pre_notify(self, value=None):  # pylint: disable=arguments-differ
        self.value=value
    def _do_notify(self, *args, **kwargs):  # pylint: disable=unused-argument
        self._controller.send_sync(self._notify_tag,self._uid)
        return True
    def get_value(self):
        """Get the value passed by the notifier (doesn't check if it has been passed already)"""
        return self.value
    def get_value_sync(self, timeout=None):
        """Wait (with the given `timeout`) for the value passed by the notifier"""
        if not self.done_wait():
            self.wait(timeout=timeout)
        return self.get_value()


class QMultiThreadNotifier:
    """
    Wait-notify thread synchronizer that can be used for multiple threads and called multiple times.

    Performs similar function to conditional variables.
    The synchronizer has an internal counter which is increased by 1 every time it is notified.
    The wait functions have an option to wait until the counter reaches the specific counter value (usually, 1 above the last wait call).
    """
    def __init__(self):
        self._lock=threading.Lock()
        self._cnt=0
        self._failed=False
        self._notifiers={}
    def wait(self, state=1, timeout=None):
        """
        Wait until notifier counter is equal to at least `state`
        
        Return current counter state plus 1, which is the next smallest value resulting in waiting.
        """
        with self._lock:
            if self._failed:
                raise threadprop.NoControllerThreadError("synchronizer failed")
            if self._cnt>=state:
                return self._cnt+1
            n=QThreadNotifier()
            self._notifiers.setdefault(state,[]).append(n)
        success=n.wait(timeout=timeout)
        if success:
            value=n.get_value()
            if value is None:
                raise threadprop.NoControllerThreadError("synchronizer failed")
            return value
        raise threadprop.TimeoutThreadError("synchronizer timed out")
    def wait_until(self, condition, timeout=None):
        """
        Wait until `condition` is met.

        `condition` is a function which is called (in the waiting thread) every time the synchronizer is notified.
        If it return non-``False``, the waiting is complete and its result is returned.
        """
        ctd=general.Countdown(timeout)
        cnt=1
        while True:
            res=condition()
            if res:
                return res
            cnt=self.wait(cnt,timeout=ctd.time_left())
    def notify(self):
        """Notify all waiting threads"""
        with self._lock:
            self._cnt+=1
            ncnt=self._cnt+1
            notifiers=[]
            for k in list(self._notifiers):
                if k<=self._cnt:
                    notifiers+=self._notifiers.pop(k)
        for n in notifiers:
            n.notify(ncnt)
    def fail(self):
        """
        Mark notifier as fails
        
        Fails all waiting notifiers.
        All subsequent wait calls raise an error
        """
        with self._lock:
            self._failed=True
            notifiers=[n for nlist in self._notifiers.values() for n in nlist]
            self._notifiers={}
        for n in notifiers:
            n.notify(None)


class QLockNotifier:
    """
    Resource lock.

    Behaves similarly to the regular lock, but waiting is done in the message loop, which still allows interrupts.
    """
    def __init__(self):
        self.lock=threading.Lock()
        self._lock_ctl=None
        self._notifiers=[]
    def acquire(self, timeout=None):
        ctl=threadprop.current_controller()
        with self.lock:
            if self._lock_ctl is None:
                self._lock_ctl=ctl
                return
            if self._lock_ctl is ctl:
                raise RuntimeError("attempting to acquire the same lock twice in the same thread")
            if timeout is not None and timeout<=0:
                raise threadprop.TimeoutThreadError("synchronizer timed out")
            notifier=QThreadNotifier()
            self._notifiers.append(notifier)
        notifier.wait(timeout=timeout)
        with self.lock:
            self._notifiers.pop(self._notifiers.index(notifier))
            if notifier.get_value():
                self._lock_ctl=ctl
            else:
                raise threadprop.TimeoutThreadError("synchronizer timed out")
    def release(self):
        ctl=threadprop.current_controller()
        with self.lock:
            if self._lock_ctl is None:
                raise RuntimeError("can not release non-acquired lock")
            if self._lock_ctl is not ctl:
                raise RuntimeError("can not release lock acquired with a different controller")
            if self._notifiers:
                self._notifiers[0].notify(True)
            else:
                self._lock_ctl=None
    def __enter__(self):
        self.acquire()
    def __exit__(self, etype, error, etrace):
        self.release()