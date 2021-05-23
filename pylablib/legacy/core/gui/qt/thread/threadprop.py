from ....utils import general

from PyQt5 import QtCore

import threading

local_data=threading.local()

thread_uids=general.NamedUIDGenerator(thread_safe=True)

### Errors ###
class ThreadError(RuntimeError):
    """Generic thread error."""
    def __init__(self, msg=None):
        msg=msg or "thread error"
        RuntimeError.__init__(self, msg)
        
class NoControllerThreadError(ThreadError):
    """Thread error for a case of thread having no conrollers."""
    def __init__(self, msg=None):
        msg=msg or "thread has no controller"
        ThreadError.__init__(self, msg)
class DuplicateControllerThreadError(ThreadError):
    """Thread error for a case of a duplicate thread controller."""
    def __init__(self, msg=None):
        msg=msg or "trying to create a duplicate thread controller"
        ThreadError.__init__(self, msg)
class TimeoutThreadError(ThreadError):
    """Thread error for a case of a wait timeout."""
    def __init__(self, msg=None):
        msg=msg or "waiting has timed out"
        ThreadError.__init__(self, msg)
class NoMessageThreadError(ThreadError):
    """Thread error for a case of trying to get a non-existant message."""
    def __init__(self, msg=None):
        msg=msg or "no message available"
        ThreadError.__init__(self, msg)
class SkippedCallError(ThreadError):
    """Thread error for a case of external call getting skipped (unscheduled)."""
    def __init__(self, msg=None):
        msg=msg or "call has been skipped"
        ThreadError.__init__(self, msg)

### Interrupts ###
class InterruptException(Exception):
    """Generic interrupt exception (raised by some function to signal interrupts from other threads)."""
    def __init__(self, msg=None):
        msg=msg or "thread interrupt"
        Exception.__init__(self, msg)
class InterruptExceptionStop(InterruptException):
    """Interrupt exception denoting thread stop request."""
    def __init__(self, msg=None):
        msg=msg or "thread interrupt: stop"
        InterruptException.__init__(self, msg)


def get_app():
    """Get current application instance."""
    return QtCore.QCoreApplication.instance()
def get_gui_thread():
    """Get main (GUI) thread, or ``None`` if Application is not running."""
    app=get_app()
    return app and app.thread()
def is_gui_running():
    """Check if GUI is running."""
    return get_app() is not None
def is_gui_thread():
    """Check if the current thread is the one running the GUI loop."""
    app=get_app()
    return (app is not None) and (QtCore.QThread.currentThread() is app.thread())
def current_controller(require_controller=True):
    """
    Get controller of the current thread.

    If the current thread has not controller `and `require_controller==True``, raise an error; otherwise, return ``None``.
    """
    controller=getattr(local_data,"controller",None)
    if require_controller and (controller is None):
        raise NoControllerThreadError("current thread has no controller")
    return controller