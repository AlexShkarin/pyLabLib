import threading
import time
from ..utils import funcargparse, py3

### Errors ###
class ThreadError(RuntimeError):
    """
    Generic thread error.
    """
    def __init__(self, msg=None):
        msg=msg or "thread error"
        RuntimeError.__init__(self, msg)
        
class NotRunningThreadError(ThreadError):
    """
    Thread error for a case of a missing or stopped thread.
    """
    def __init__(self, msg=None):
        msg=msg or "thread is not running"
        ThreadError.__init__(self, msg)
class NoControllerThreadError(ThreadError):
    """
    Thread error for a case of thread having no conrollers.
    """
    def __init__(self, msg=None):
        msg=msg or "thread has no controller"
        ThreadError.__init__(self, msg)
        
        
def on_error(action, error_object=None):
    """
    React to an error depending on the `action`.

    `action` can be ``'error'`` (raise `error_object` if it's supplied, or :exc:`ThreadError` by default),
    ``'stop'`` (raise an appropriate exception to stop the thread), ``'return_error'`` (return `error_object`) or ``'ignore'`` (do nothing).
    """
    funcargparse.check_parameter_range(action,"action",{"error","ignore","stop","return_error"})
    if action=="error":
        raise error_object or ThreadError()
    elif action=="stop":
        stop()
    elif action=="ignore":
        return
    elif action=="return_error":
        return error_object
        
        
### Interrupts ###
class InterruptException(Exception):
    """
    Generic interrupt exception (raised by some function to signal interrupts from other threads).
    """
    def __init__(self, msg=None):
        msg=msg or "thread interrupt"
        Exception.__init__(self, msg)
class InterruptExceptionStop(InterruptException):
    """
    Interrupt exception denoting thread stop request.
    """
    def __init__(self, msg=None):
        msg=msg or "thread interrupt: stop"
        InterruptException.__init__(self, msg)
        


### Thread controller ###
class NoThreadController(object):
    """
    A 'dummy' thread controller implementing the most standard function for a thread without any explicitly created controller.
    """
    def __init__(self):
        object.__init__(self)
        self.name="no_thread_controller"
    def add_message(self, msg, sync=True, on_broken="error"):
        raise NoControllerThreadError("can't add message without a thread controller")
    def add_new_message(self, tag, value=None, priority=0, schedule_sync="wait", receive_sync="none", sender=None, sync=True, on_broken="error"):
        raise NoControllerThreadError("can't add message without a thread controller")
    def sleep(self, delay):
        """
        Sleep for `delay` seconds.
        """
        time.sleep(delay)
    def stop(self):
        """
        Stop the thread.
        """
        raise SystemExit()
no_thread_controller=NoThreadController()

def current_controller(require_controller=False):
    """
    Return the controller of the current thread.

    If the thread has no controller and ``require_controller==False``, return a :class:`NoThreadController` object; otherwise, raise :exc:`NoControllerThreadError`.
    """
    controller=getattr(threading.current_thread(),"thread_controller",no_thread_controller)
    if require_controller and controller is no_thread_controller:
        raise NoControllerThreadError("current thread has no controller")
    return controller
def has_controller(thread):
    """Check if the current thread has a controller."""
    return hasattr(thread,"thread_controller")
def all_controllers():
    """Return a list of all the available thread controllers."""
    threads=threading.enumerate()
    return [t.thread_controller for t in threads if has_controller(t)]
def controller_by_name(name, require_controller=False):
    """
    Return a controller for a given name.

    If the controller is not found and ``require_controller==False``, return a :class:`NoThreadController` object; otherwise, raise :exc:`NoControllerThreadError`.
    """
    controllers=all_controllers()
    for c in controllers:
        if c.name==name:
            return c
    if require_controller:
        raise NoControllerThreadError("can't find controller with name {}".format(name))
    return no_thread_controller
def as_controller(ctrl, require_controller=False):
    """
    Return a controller corresponding to `ctrl`.

    `ctrl` can be ``None`` (return current thread controller), a thread name, or a  thread controller instance.
    If the cooresponding controller doesn't exist and ``require_controller==False``, return a :class:`NoThreadController` object; otherwise, raise :exc:`NoControllerThreadError`.
    """
    if ctrl is None:
        return current_controller(require_controller=require_controller)
    if isinstance(ctrl,py3.textstring):
        return controller_by_name(ctrl,require_controller=require_controller)
    if isinstance(ctrl,threading.Thread):
        try:
            return ctrl.thread_controller
        except AttributeError:
            if require_controller:
                return no_thread_controller
            else:
                raise NoControllerThreadError("thread has no controller")
    if ctrl is no_thread_controller and require_controller:
        raise NoControllerThreadError("thread has no controller")
    return ctrl


### Message queue ###
class NoMessageQueue(object):
    def __init__(self, owner):
        object.__init__(self)
        self.owner=owner
        owner.message_queue=self
no_message_queue=NoMessageQueue(no_thread_controller)
def current_message_queue(require_queue=False):
    """
    Return a message queue corresponding to the current thread.

    If the queue doesn't exist and ``require_queue==False``, return a :class:`NoMessageQueue` object; otherwise, raise :exc:`NoControllerThreadError`.
    """
    controller=current_controller(require_queue)
    return controller.message_queue



### Common functions ###

def sleep(delay):
    """
    Sleep for `delay` seconds.

    Behavior depends on whether the thread has a controller.
    """
    current_controller().sleep(delay)
def stop():
    """
    Stop the current thread by raising an appropriate interrupt exception.

    Behavior depends on whether the thread has a controller.
    """
    current_controller().stop()

def kill_thread(th, sync=True):
    """
    Stop thread `th` (can be a thread controller, or the thread name).

    If ``sync==True``, return only after the thread is stopped.
    Ignore any errors if the thread is already stopped.
    """
    try:
        controller=as_controller(th,require_controller=True)
        controller.stop(sync=sync)
    except (NotRunningThreadError,NoControllerThreadError):
        pass
def kill_all(sync=True, include_current=True):
    """
    Stop all threads.

    If ``sync==True``, return only after all threads are stopped.
    If ``include_current==True``, stop the current as well.
    """
    controllers=all_controllers()
    cc=current_controller()
    for c in controllers:
        if c is not cc:
            try:
                c.stop(sync=sync)
            except (NotRunningThreadError, NoControllerThreadError):
                pass
    if include_current:
        stop()