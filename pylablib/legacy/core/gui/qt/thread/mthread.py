from ....mthread import threadprop, controller, sync_primitives
from ....utils import funcargparse

from PyQt5 import QtCore, QtWidgets

import threading
import sys
    
_depends_local=["....mthread.controller"]

def get_app():
    """
    Get current application instance.
    """
    return QtCore.QCoreApplication.instance()
def is_gui_running():
    """
    Check if GUI is running.
    """
    return get_app() is not None
def is_gui_thread():
    """
    Check if the current thread is the one running the GUI loop.
    """
    app=get_app()
    return (app is not None) and (QtCore.QThread.currentThread() is app.thread())
def is_gui_controlled_thread():
    """
    Check if the current thread is controlled by a GUI controller.
    """
    return isinstance(threadprop.current_controller(),GUIThreadController)

class CallerObject(QtCore.QObject):
    """
    Auxiliary object for making remote calls in the GUI thread.
    """
    call_signal=QtCore.pyqtSignal("PyQt_PyObject")
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.call_signal.connect(self.on_call)
        self.lock=threading.Lock()
        self.app_stopped=False
    def on_call(self, func):
        func()
    def on_app_stop(self):
        with self.lock:
            self.app_stopped=True
    def call_after(self, func):
        with self.lock:
            if self.app_stopped:
                raise threadprop.NotRunningThreadError("GUI thread is not running")
            self.call_signal.emit(func)
def setup_call_after(): # needs to be called from the main thread
    """
    Setup the :func:`call_after` functionality.

    Needs to be called once in the GUI thread.
    """
    app=get_app()
    if app is None:
        raise threadprop.NotRunningThreadError("GUI thread is not running")
    if not hasattr(app,"_caller_object"):
        app._caller_object=CallerObject()
        app.aboutToQuit.connect(app._caller_object.on_app_stop)
def call_after(func, *args, **kwargs):
    """
    Call the function `func` with the given arguments in a GUI thread.

    Return immediately. If synchronization is needed, use :func:`call_in_gui_thread`.
    Analogue of ``wx.CallAfter``.
    """
    app=get_app()
    if app is None:
        raise threadprop.NotRunningThreadError("GUI thread is not running")
    app._caller_object.call_after(lambda: func(*args,**kwargs))

def call_in_gui_thread(func, args=None, kwargs=None, to_return="result", note=None, on_stopped="error"):
    """
    Call the function `func` with the given arguments in a GUI thread.

    `to_return` specifies the return value parameters:
        - ``"none"``: execute immediately, return nothing, no synchronization is performed;
        - ``"syncher"``: execute immediately, return a synchronizer object (:class:`.ValueSynchronizer`),
            which can be used to check if the execution is done and to obtain the result.
        - ``"result"``: pause until the function has been executed, return the result. Mostly equivalent to a simple function call.

    If `note` is not ``None``, it specific a callback function to be called after the execution is done, or (if it's a string), a message tag which is sent after the execution is done.
    """
    funcargparse.check_parameter_range(to_return,"to_return",{"none","result","syncher"})
    if is_gui_thread():
        if to_return=="syncher":
            raise ValueError("can't return syncher for the gui thread")
        res=func(*(args or []),**(kwargs or {}))
        return res if to_return=="result" else True
    if to_return!="none" or note is not None:
        call=sync_primitives.SyncCall(func,args,kwargs,sync=(None if to_return=="none" else True),note=note)
        try:
            call_after(call)
        except threadprop.NotRunningThreadError:
            return bool(threadprop.on_error(on_stopped,threadprop.NotRunningThreadError("GUI thread is not running")))
        value=call.value(sync=(to_return=="result"),default=None if to_return=="result" else False)
        return value
    else:
        call_after(func,*(args or []),**(kwargs or {}))
    
def gui_func(to_return="result", note=None, on_stopped="error"): #decorator
    """
    Decorator for a function which makes it execute through a :func:`call_in_gui_thread` call.

    Effectively, makes a GUI-realted function thread-safe (can be called from any thread, but the execution is done in the GUI thread).
    """
    def wrapper(func):
        def wrapped(*args, **kwargs):
            return call_in_gui_thread(func,args,kwargs,to_return=to_return,note=note,on_stopped=on_stopped)
        return wrapped
    return wrapper
gui_func_sync=gui_func()
    



class GUIThreadController(controller.IThreadController):
    """
    Thread controller optimized for a GUI thread (uses GUI message loop).

    Args:
        name(str): thread name (can be used to, e.g., get the controller from a different thread).
        setup(callable): if not ``None``, function to be called when the thread is starting.
        cleanup(callable): if not ``None``, function to be called when the thread is stopped (regardless of the stopping reason).

    Any thread creation and synchronization should be done after the controller has started, hence, it should be put into the `setup` function.
    """
    def __init__(self, name="gui", setup=None, cleanup=None):
        controller.IThreadController.__init__(self,name)
        self.setup=setup
        self.cleanup=cleanup
        self.app=get_app() or QtWidgets.QApplication(sys.argv)
        if hasattr(self.app,"_controller"):
            raise threadprop.ThreadError("a GUI thread controller already exists")
        self.app._controller=self
        setup_call_after()

    @staticmethod
    def get_current():
        app=get_app()
        if app is not None:
            return getattr(app,"_controller",None)
    
    def check_messages(self, tags=None, filt=None, on_broken="error"):
        if threadprop.current_controller() is self:
            self.exhaust_messages(tags,filt)
        else:
            call_in_gui_thread(self.check_messages,tags,filt,on_stopped=on_broken)
    def add_message(self, msg, sync=True, on_broken="error", request_message_check="none"):
        funcargparse.check_parameter_range(request_message_check,"request_message_check",{"none","empty","tag"})
        msg=controller.IThreadController.add_message(self,msg,sync=False,on_broken=on_broken)
        if msg:
            if request_message_check!="none":
                self.check_messages(([msg.tag] if request_message_check=="tag" else []),on_broken=on_broken)
            if sync:
                msg.sync()
        return msg
    def add_new_message(self, tag, value=None, priority=0, schedule_sync="wait", receive_sync="none", sync=True, timeout=None, on_broken="error", request_message_check="auto"):
        msg=self.message_queue.build_message(tag,value,priority,schedule_sync,receive_sync)
        if request_message_check=="auto":
            request_message_check="tag" if (receive_sync in {"wait_even","wait"}) else "none"
        self.add_message(msg,sync=sync,on_broken=on_broken,request_message_check=request_message_check)
    def _ask_for_call(self, call, sync=True, as_interrupt=False, priority=0, on_broken="error"):
        if sync:
            tag="interrupt.execute" if as_interrupt else "execute"
            request_message_check="empty" if as_interrupt else "tag"
            return self.add_new_message(tag,call,priority=priority,receive_sync="wait",sync=True,request_message_check=request_message_check,on_broken=on_broken)
        else:
            call_in_gui_thread(call,on_stopped=on_broken)
    
    def _on_start(self):
        call_after(controller.IThreadController._on_start,self) # delay until gui message loop is running
    def run(self):
        if self.setup:
            self.setup_res=self.setup()
        self.app.exec_()
    def finalize(self):
        if self.cleanup:
            self.cleanup_res=self.cleanup()
    def start(self, setup=None):
        self.setup=setup or self.setup
        controller.IThreadController.start_continuing(self)
    def _stop_self(self):
        if self.passed_stage("created") and not self.passed_stage("running"): 
            self.app.exit()