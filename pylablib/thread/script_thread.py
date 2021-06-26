from ..core.thread import controller
from ..core.utils import functions

import collections



class ScriptStopException(Exception):
    """Exception for stopping script execution"""

TMulticastWaitResult=collections.namedtuple("TMulticastWaitResult",["monitor","message"])
class ScriptThread(controller.QTaskThread):
    """
    A script thread.
    
    Designed to provide means of writing code which interacts with multiple device threads,
    but reads similar to a standard single-threaded script.
    To do that, it provides a mechanism of multicast monitors: one can suspend execution until a multicast with certain properties has been received.
    This can be used to implement, e.g., waiting until the next stream_format/daq sample or a next camera frame.

    Attributes:
        - ``executing`` (bool): shows whether the script is executing right now;
            useful in :meth:`interrupt_script` to check whether it is while the script is running and is done / stopped by user / terminated (then it would be ``True``),
            or if the script was waiting to be executed / done executing (then it would be ``False``)
            Duplicates ``interrupt_reason`` attribute (``executing==False`` if and only if ``interrupt_reason=="shutdown"``)
        - ``stop_request`` (bool): shows whether stop has been requested from another thread (by calling :meth:`stop_execution`).
        - ``interrupt_reason`` (str): shows the reason for calling :meth:`interrupt_script`;
            can be ``"done"`` (called in the end of regularly executed script), ``"stopped"`` (called if the script is forcibly stopped),
            ``"failed"`` (called if the thread is shut down while the script is active,
            e.g., due to error in the script or any other thread, or if the application is closing),
            or ``"shutdown"`` (called when the script is shut down while being inactive)

    Methods to overload:
        - :meth:`setup_script`: executed on the thread startup (between synchronization points ``"start"`` and ``"run"``)
        - :meth:`finalize_script`: executed on thread cleanup (attempts to execute in any case, including exceptions); by default, call :meth:`interrupt_script`
        - :meth:`run_script`: execute the script (can be run several times per script lifetime)
        - :meth:`interrupt_script`: executed when the script is finished or forcibly shut down (including due to exception or application shutdown)
    """
    def __init__(self, name=None, args=None, kwargs=None, multicast_pool=None):
        super().__init__(name=name,args=args,kwargs=kwargs,multicast_pool=multicast_pool)
        self.executing=False
        self.interrupt_reason="shutdown"
        self.stop_request=False
        self.add_command("start_script",self._start_script)

    def process_interrupt(self, tag, value):
        if super().process_interrupt(tag,value):
            return True
        if tag=="control.start":
            self.ca.start_script()
            if self.executing:
                self.stop_request=True
            return True
        if tag=="control.stop":
            self.stop_request=True
            return True
        return False

    def setup_script(self, *args, **kwargs):
        """Setup script thread (to be overloaded in subclasses)"""
    def finalize_script(self):
        """
        Finalize script thread (to be overloaded in subclasses)
        
        By default, calls :meth:`interrupt_script`.
        """
        self.interrupt_script()
    def run_script(self):
        """Execute script (to be overloaded in subclasses)"""
    def interrupt_script(self, kind="default"):
        """Finalize script execution (the thread is still running, i.e., the script might be started again)"""
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


    def start_execution(self):
        """Request starting script execution"""
        self.send_interrupt("control.start",None)
    def stop_execution(self):
        """Request stopping script execution"""
        self.send_interrupt("control.stop",None)