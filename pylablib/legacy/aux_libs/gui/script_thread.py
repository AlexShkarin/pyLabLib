from ...core.gui.qt.thread import controller, signal_pool
from ...core.utils import general, functions

from PyQt5 import QtCore

import collections
import traceback



class ScriptStopException(Exception):
    """Exception for stopping script execution"""

class ScriptThread(controller.QTaskThread):
    """
    A script thread.
    
    Designed to provide means of writing code which interacts with multiple device threads,
    but reads similar to a standard single-threaded script.
    To do that, it provides a mechanism of signal montors: one can suspend execution until a signal with certain properties has been received.
    This can be used to implement, e.g., waiting until the next stream_format/daq sample or a next camera frame.

    Args:
        name (str): thread name
        setupargs: args supplied to :math:`setup_script` method
        setupkwargs: keyword args supplied to :math:`setup_script` method
        signal_pool: :class:`.SignalPool` for this thread (by default, use the default common pool)

    Attributes:
        executing (bool): shows whether the script is executing right now;
            useful in :meth:`interrupt_script` to check whether it is while the script is running and is done / stopped by user / terminated (then it would be ``True``),
            or if the script was waiting to be executed / done executing (then it would be ``False``)
            Duplicates ``interrupt_reason`` attribute (``executing==False`` if and only if ``interrupt_reason=="shutdown"``)
        stop_request (bool): shows whether stop has been requested from another thread (by calling :meth:`stop_execution`).
        interrupt_reason (str): shows the reason for calling :meth:`interrupt_script`;
            can be ``"done"`` (called in the end of regularly executed script), ``"stopped"`` (called if the script is forcibly stopped),
            ``"failed"`` (called if the thread is shut down while the script is active,
            e.g., due to error in the script or any other thread, or if the application is closing),
            or ``"shutdown"`` (called when the script is shut down while being inactive)

    Methods to overload:
        setup_script: executed on the thread startup (between synchronization points ``"start"`` and ``"run"``)
        finalize_script: executed on thread cleanup (attempts to execute in any case, including exceptions); by default, call :meth:`interrupt_script`
        run_script: execute the script (can be run several times per script lifetime)
        interrupt_script: executed when the script is finished or forcibly shut down (including due to exception or application shutdown)
    """
    def __init__(self, name=None, setupargs=None, setupkwargs=None, signal_pool=None):
        controller.QTaskThread.__init__(self,name=name,setupargs=setupargs,setupkwargs=setupkwargs,signal_pool=signal_pool)
        self._monitor_signal.connect(self._on_monitor_signal)
        self._monitored_signals={}
        self.executing=False
        self.interrupt_reason="shutdown"
        self.stop_request=False
        self.add_command("start_script",self._start_script)

    def process_message(self, tag, value):
        if tag=="control.start":
            self.c.start_script()
            if self.executing:
                self.stop_request=True
        if tag=="control.stop":
            self.stop_request=True
        return False

    def setup_script(self, *args, **kwargs):
        """Setup script thread (to be overloaded in subclasses)"""
        pass
    def finalize_script(self):
        """
        Finalize script thread (to be overloaded in subclasses)
        
        By default, calls :meth:`interrupt_script`.
        """
        self.interrupt_script()
    def run_script(self):
        """Execute script (to be overloaded in subclasses)"""
        pass
    def interrupt_script(self, kind="default"):
        """Finalize script execution (the thread is still running, i.e., the script might be started again)"""
        pass
    def check_stop(self, check_messages=True):
        """
        Check if the script stop is requested.

        If it is, raise :exc:`ScriptStopException` which effectively stops execution past this point
        (the exception is properly caught and processed elsewhere in the service code).
        To only check if the stop has been requested without exception raising, use ``stop_request`` attribute.
        If ``check_messages==True``, check for new messages from other threads first.
        """
        if check_messages:
            self.check_messages()
        if self.stop_request:
            self.stop_request=False
            raise ScriptStopException()



    def setup_task(self, *args, **kwargs):
        functions.call_cut_args(self.setup_script,*args,**kwargs)
    def finalize_task(self):
        self.finalize_script()

    def _start_script(self):
        self.executing=True
        self.stop_request=False
        try:
            self.interrupt_reason="done"
            self.run_script()
            self.interrupt_script()
            self.interrupt_reason="shutdown"
            self.executing=False
        except ScriptStopException:
            self.interrupt_reason="stopped"
            self.interrupt_script()
            self.interrupt_reason="shutdown"
            self.executing=False
        except:
            self.interrupt_reason="failed"
            raise

    _monitor_signal=QtCore.pyqtSignal("PyQt_PyObject")
    @QtCore.pyqtSlot("PyQt_PyObject")
    def _on_monitor_signal(self, value):
        mon,msg=value
        try:
            signal=self._monitored_signals[mon]
            if not signal.paused:
                signal.messages.append(msg)
        except KeyError:
            pass
    
    class MonitoredSignal(object):
        def __init__(self, uid):
            object.__init__(self)
            self.uid=uid
            self.messages=[]
            self.paused=True
    def add_signal_monitor(self, mon, srcs="any", dsts="any", tags=None, filt=None):
        """
        Add a new signal monitor.

        The monitoring isn't started until :meth:`start_monitoring` is called.
        `mon` specifies monitor name; the rest of the arguments are the same as :meth:`.SignalPool.subscribe`
        """
        if mon in self._monitored_signals:
            raise KeyError("signal monitor {} already exists".format(mon))
        uid=self.subscribe_nonsync(lambda *msg: self._monitor_signal.emit((mon,signal_pool.TSignal(*msg))),srcs=srcs,dsts=dsts,tags=tags,filt=filt)
        self._monitored_signals[mon]=self.MonitoredSignal(uid)
    def remove_signal_monitor(self, mon):
        """Remove signal monitor with a given name"""
        if mon not in self._monitored_signals:
            raise KeyError("signal monitor {} doesn't exist".format(mon))
        uid,_=self._monitored_signals.pop(mon)
        self.unsubscribe(uid)
    TWaitResult=collections.namedtuple("TWaitResult",["monitor","message"])
    def wait_for_signal_monitor(self, mons, timeout=None):
        """
        Wait for a signal to be received on a given monitor or several monitors 
        
        If several monitors are given (`mon` is a list), wait for a signal on any of them.
        After waiting is done, pop and return signal value (see :meth:`pop_monitored_signal`).
        """
        if not isinstance(mons,(list,tuple)):
            mons=[mons]
        for mon in mons:
            if mon not in self._monitored_signals:
                raise KeyError("signal monitor {} doesn't exist".format(mon))
        ctd=general.Countdown(timeout)
        while True:
            for mon in mons:
                if self._monitored_signals[mon].messages:
                    return self.TWaitResult(mon,self._monitored_signals[mon].messages.pop(0))
            self.wait_for_any_message(ctd.time_left())
    def new_monitored_signals_number(self, mon):
        """Get number of received signals at a given monitor"""
        if mon not in self._monitored_signals:
            raise KeyError("signal monitor {} doesn't exist".format(mon))
        return len(self._monitored_signals[mon].messages)
    def pop_monitored_signal(self, mon, n=None):
        """
        Pop data from the given signal monitor queue.

        `n` specifies number of signals to pop (by default, only one).
        Each signal is a tuple ``(mon, sig)`` of monitor name and signal,
        where `sig` is in turn tuple ``(src, tag, value)`` describing the signal.
        """
        if self.new_monitored_signals_number(mon):
            if n is None:
                return self._monitored_signals[mon].messages.pop(0)
            else:
                return [self._monitored_signals[mon].messages.pop(0) for _ in range(n)]
        return None
    def reset_monitored_signal(self, mon):
        """Reset monitored signal (clean its received signals queue)"""
        self._monitored_signals[mon].messages.clear()
    def pause_monitoring(self, mon, paused=True):
        """Pause or un-pause signal monitoring"""
        self._monitored_signals[mon].paused=paused
    def start_monitoring(self, mon):
        """Start signal monitoring"""
        self.pause_monitoring(mon,paused=False)


    def start_execution(self):
        """Request starting script execution"""
        self.send_message("control.start",None)
    def stop_execution(self):
        """Request stopping script execution"""
        self.send_message("control.stop",None)