import threading

class ISkippableNotifier(object):
    """
    Generic skippable notifier.

    The main methods are :meth:`wait` (wait until the event happend) and :meth:`notify` (notify that the event happend).
    Only calls underlying waiting and notifying methods once, duplicate calls are ignored.

    Args:
        skippable (bool): if ``True``, allows for skippable wait events
            (if :meth:`notify` is called before :meth:`wait`, neither methods are actually called).
    """
    def __init__(self, skippable=False):
        object.__init__(self)
        self._lock=threading.Lock()
        self._waiting="init"
        self._notifying="init"
        self._skippable=skippable # if skippable and Notifier.notify() is called before Notifier.wait(), doesn't call the internal _notify and _wait functions
    
    def _pre_wait(self, *args, **kwargs):
        """
        Check if the waiting initialization is successfull.

        Called inside an internal lock section, so should be short and preferably non-blocking.
        If return value is ``False``, waiting aborts and returns `False``, and the waiting status is marked as ``"failed"``.
        """
        return True
    def _do_wait(self, *args, **kwargs):
        """
        Main waiting routine.

        If return value is ``False``, waiting returns `False``, and the waiting status is marked as ``"failed"``.
        """
        return True
    def _post_wait(self, *args, **kwargs):
        """
        Perform post-waiting actions.

        Only called if the :meth:`_pre_wait` was successfull.
        """
        pass
    def wait(self, *args, **kwargs):
        """
        Wait for the notification.

        Can only be called once per notifier lifetime.
        If the notifier allows skipping, and this method is called after :meth:`notify`, return immediately.
        """
        with self._lock:
            if self._waiting!="init":
                raise RuntimeError("waiting can only be called once")
            success=self._pre_wait(*args,**kwargs)
            if not success:
                self._waiting="fail"
                return False
            if self._notifying=="skip":
                self._waiting="skip"
            else:
                self._waiting="proc"
        if self._waiting=="proc":
            success=self._do_wait(*args,**kwargs)
            with self._lock:
                self._waiting="done" if success else "fail"
        self._post_wait(*args,**kwargs)
        return success
    
    def _pre_notify(self, *args, **kwargs):
        """
        Perform pre-notification actions.

        Called inside an internal lock section, so should be short and preferably non-blocking.
        """
        pass        
    def _do_notify(self):
        """
        Main notification routine.
        """
        pass
    def _post_notify(self, *args, **kwargs):
        """
        Perform post-notification actions.
        """
        pass
    def notify(self, *args, **kwargs):
        """
        Notify the waiting process.

        Can only be called once per notifier lifetime.
        If the notifier allows skipping, and this method is called before :meth:`wait`, return immediately.
        """
        with self._lock:
            if self._notifying!="init":
                raise RuntimeError("notifier can only be called once")
            self._pre_notify(*args,**kwargs)
            if self._skippable and self._waiting=="init":
                self._notifying="skip"
            else:
                self._notifying="proc"
        if self._notifying=="proc":
            self._do_notify(*args,**kwargs)
            with self._lock:
                self._notifying="done"
        self._post_notify(*args,**kwargs)
            
    def waiting(self):
        """Check if waiting is in progress."""
        with self._lock:
            return self._waiting=="proc"
    def done_wait(self):
        """Check if waiting is done."""
        with self._lock:
            return self._waiting in {"skip","done","fail"}
    def success_wait(self):
        """Check if waiting is done successfully."""
        with self._lock:
            return self._waiting in {"skip","done"}
    def done_notify(self):
        """Check if notifying is done."""
        with self._lock:
            return self._notifying in {"done","skip"}
    def waiting_state(self):
        return self._waiting
    def notifying_state(self):
        return self._notifying