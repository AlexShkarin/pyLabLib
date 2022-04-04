from ..utils import general, funcargparse, dictionary, functions as func_utils, py3
from . import multicast_pool as mpool, threadprop, synchronizing, callsync

from ..gui import QtCore, Slot, Signal

import threading
import contextlib
import time
import sys
import traceback
import heapq
import collections
import atexit

_default_multicast_pool=mpool.MulticastPool()

_created_threads={}
_running_threads={}
_stopped_threads=set()
_running_threads_lock=threading.Lock()
_running_threads_notifier=synchronizing.QMultiThreadNotifier()
_running_threads_stopping=False
_restart_request=False


_exception_print_lock=threading.Lock()

_debug_mode=False
_debug_threads=[]

_exception_hooks={}

@contextlib.contextmanager
def exint(error_msg_template="{}:", pass_stop_exception=False):
    """Context that intercepts exceptions and stops the execution in a controlled manner (quitting the main thread)"""
    try:
        yield
    except threadprop.InterruptExceptionStop:
        if pass_stop_exception:
            raise
    except:  # pylint: disable=bare-except
        with _exception_print_lock:
            ctl_name=None
            try:
                ctl_name=get_controller(sync=False).name
                print(error_msg_template.format("Exception raised in thread '{}'".format(ctl_name)),file=sys.stderr)
            except threadprop.NoControllerThreadError:
                print(error_msg_template.format("Exception raised in an uncontrolled thread"),file=sys.stderr)
            traceback.print_exc()
            if _debug_mode:
                running_threads=", ".join(["'{}'".format(k) for k in _running_threads])
                print("\nRunning threads: {}\n\n".format(running_threads),file=sys.stderr)
                for thread_id,frame in sys._current_frames().items():
                    ctl=_find_controller_by_id(thread_id)
                    if ctl and ctl.name!=ctl_name and (not _debug_threads or ctl.name in _debug_threads):
                        print("\n\n\nStack trace of thread '{}':".format(ctl.name),file=sys.stderr)
                        traceback.print_stack(frame,file=sys.stderr)
            sys.stderr.flush()
            hooks=[h for h,_ in _exception_hooks.values()]
            for hn in list(_exception_hooks):
                if _exception_hooks[hn][1]:
                    del _exception_hooks[hn]
        try:
            for h in hooks:
                h()
        finally:
            try:
                stop_controller("gui",code=1,sync=False,require_controller=True)
            except threadprop.NoControllerThreadError:
                with _exception_print_lock:
                    print("Can't stop GUI thread; quitting the application",file=sys.stderr)
                    sys.stderr.flush()
                sys.exit(1)
            except threadprop.InterruptExceptionStop:
                pass

def add_exception_hook(name, func, single_call=False):
    """
    Add an exception hook, which is called whenever exception is caught via :func:`exint` wrapper.
    
    If ``single_call==True``, the hook is removed from the set when it is called.
    """
    if name in _exception_hooks:
        raise ValueError("exception hook {} is already defined".format(name))
    _exception_hooks[name]=(func,single_call)
def remove_exception_hook(name):
    """Remove the exception hook with the given name"""
    del _exception_hooks[name]

def exsafe(func):
    """Decorator that intercepts exceptions raised by `func` and stops the execution in a controlled manner (quitting the main thread)"""
    error_msg_template="{{}} executing function '{}':".format(func.__name__)
    @func_utils.getargsfrom(func,hide_outer_obj=True) # Qt slots don't work well with bound methods
    def safe_func(*args, **kwargs):
        with exint(error_msg_template=error_msg_template):
            return func(*args,**kwargs)
    return safe_func
def exsafeSlot(*slargs, **slkwargs):
    """Wrapper around Qt slot which intercepts exceptions and stops the execution in a controlled manner"""
    def wrapper(func):
        return Slot(*slargs,**slkwargs)(exsafe(func))
    return wrapper
def _toploop(func):
    @func_utils.getargsfrom(func,hide_outer_obj=True) # slots don't work well with bound methods
    def tlfunc(*args, **kwargs):
        ctl=threadprop.current_controller()
        if not ctl._postpone_call("toploop",lambda: func(*args,**kwargs)):
            func(*args,**kwargs)
    return tlfunc
def toploopSlot(*slargs, **slkwargs):
    """Wrapper around Qt slot which intercepts exceptions and stops the execution in a controlled manner"""
    def wrapper(func):
        slot=Slot(*slargs,**slkwargs)(_toploop(exsafe(func)))
        return slot
    return wrapper







class QThreadControllerThread(QtCore.QThread):
    finalized=Signal()
    _stop_request=Signal()
    def __init__(self, controller):
        super().__init__()
        self.moveToThread(self)
        self.controller=controller
        self._stop_request.connect(self._do_quit)
        self._stop_requested=False
        self.thread_id=None
    def run(self):
        self.thread_id=threading.current_thread().ident
        with exint():
            try:
                self.exec_() # main execution event loop
            finally:
                self.finalized.emit()
                self.exec_() # finalizing event loop (exited after finalizing event is processed)
                self.controller._kill_poke_timer()
    @Slot()
    def _do_quit(self):
        if self.isRunning() and not self._stop_requested:
            self.controller.request_stop() # signal controller to stop
            self.quit() # quit the first event loop
            self._stop_requested=True
    def quit_sync(self):
        self._stop_request.emit()


def remote_call(func):
    """Decorator that turns a controller method into a remote call (call from a different thread is passed synchronously)"""
    @func_utils.getargsfrom(func)
    def rem_func(self, *args, **kwargs):
        return self.call_in_thread_sync(func,args=(self,)+args,kwargs=kwargs,sync=True,same_thread_shortcut=True)
    return rem_func

def call_in_thread(thread_name, interrupt=True, pass_exception=True, silent=False, sync=True):
    """Decorator that turns any function into a remote call in a thread with a given name (call from a different thread is passed synchronously)"""
    def wrapper(func):
        @func_utils.getargsfrom(func)
        def rem_func(*args, **kwargs):
            thread=get_controller(thread_name)
            return thread.call_in_thread_sync(func,args=args,kwargs=kwargs,sync=sync,same_thread_shortcut=True,interrupt=interrupt,pass_exception=pass_exception,silent=silent)
        return rem_func
    return wrapper
def call_in_gui_thread(func=None, interrupt=True, pass_exception=True, silent=False, sync=True):
    """Decorator that turns any function into a remote call in a GUI thread (call from a different thread is passed synchronously)"""
    if func is not None:
        return call_in_gui_thread(interrupt=interrupt,pass_exception=pass_exception,silent=silent)(func)
    def wrapper(func):
        @func_utils.getargsfrom(func)
        def rem_func(*args, **kwargs):
            if not threadprop.is_gui_thread():
                return get_gui_controller().call_in_thread_sync(func,args=args,kwargs=kwargs,sync=sync,same_thread_shortcut=False,interrupt=interrupt,pass_exception=pass_exception,silent=silent)
            return func(*args,**kwargs)
        return rem_func
    return wrapper
def gui_thread_method(func):
    """Decorator for an object's method that checks if the object's ``gui_thread_safe`` attribute is true, in which case the call is routed to the GUI thread"""
    @func_utils.getargsfrom(func)
    def rem_func(self, *args, **kwargs):
        if getattr(self,"gui_thread_safe",False) and not threadprop.is_gui_thread():
            return get_gui_controller().call_in_thread_sync(func,args=(self,)+args,kwargs=kwargs,sync=True,same_thread_shortcut=False)
        return func(self,*args,**kwargs)
    return rem_func









class QThreadController(QtCore.QObject):
    """
    Generic Qt thread controller.

    Responsible for all inter-thread synchronization. There is one controller per thread, and 

    Args:
        name(str): thread name (by default, generate a new unique name);
            this name can be used to obtain thread controller via :func:`get_controller`
        kind(str): thread kind; can be ``"loop"`` (thread is running in the Qt message loop; behavior is implemented in :meth:`process_message` and remote calls),
            ``"run"`` (thread executes :meth:`run` method and quits after it is complete), or ``"main"`` (can only be created in the main GUI thread)
        multicast_pool: :class:`.MulticastPool` for this thread (by default, use the default common pool)

    Methods to overload:
        - :meth:`on_start`: executed on the thread startup (between synchronization points ``"start"`` and ``"run"``)
        - :meth:`on_finish`: executed on thread cleanup (attempts to execute in any case, including exceptions)
        - :meth:`run`: executed once per thread; thread is stopped afterwards (only if ``kind=="run"``)
        - :meth:`process_message`: function that takes 2 arguments (tag and value) of the message and processes it; returns ``True`` if the message has been processed and ``False`` otherwise
            (in which case it is stored and can be recovered via :meth:`wait_for_message`/:meth:`pop_message`); by default, always return ``False``
        - :meth:`process_interrupt`: function that tales 2 arguments (tag and value) of the interrupt message (message with a tag starting with ``"interrupt."``) and processes it;
            by default, assumes that any value with tag ``"execute"`` is a function and executes it
    
    Signals:
        - ``started``: emitted on thread start (after :meth:`on_start` is executed)
        - ``finished``: emitted on thread finish (before :meth:`on_finish` is executed)
    """
    def __init__(self, name=None, kind="loop", multicast_pool=None):
        super().__init__()
        funcargparse.check_parameter_range(kind,"kind",{"loop","run","main"})
        if kind=="main":
            name="gui"
        self.name=name or threadprop.thread_uids(type(self).__name__)
        self.thread_kind=kind
        # register thread
        _store_created_controller(self)
        if self.thread_kind=="main":
            if not threadprop.is_gui_thread():
                raise threadprop.ThreadError("GUI thread controller can only be created in the main thread")
            if threadprop.current_controller(require_controller=False):
                raise threadprop.DuplicateControllerThreadError()
            self.thread=threadprop.get_gui_thread()
            self.thread.thread_id=threading.current_thread().ident
            threadprop.local_data.controller=self
            threadprop.local_data.controller_name=self.name
            threadprop.local_data.is_gui=True
            _register_controller(self)
        else:
            self.thread=QThreadControllerThread(self)

        # set up message processing
        self._wait_timer=QtCore.QBasicTimer()
        self._poke_timer_id=None
        self._loop_depth=0
        self._toploop_depth=0
        self._postponed_calls={}
        self._blocked_message_kinds=set()
        self._ignored_message_kinds=set()
        self._message_queue={}
        self._message_uid=0
        self._sync_queue={}
        self._sync_clearance=set()
        self._call_queue=[]
        self._next_place_call_counter=0
        self._next_execute_call_counter=0
        self._call_counter_lock=threading.Lock()
        # set up variable and methods handling
        self._params_val=dictionary.Dictionary()
        self._params_val_lock=threading.Lock()
        self._params_exp={}
        self._params_exp_lock=threading.Lock()
        self._params_funcs=dictionary.Dictionary()
        self._thread_methods={}
        self.v=dictionary.ItemAccessor(getter=lambda name:self.get_variable(name,missing_error=True),
            setter=self.set_variable,deleter=self.delete_variable,contains_checker=self._has_variable)
        self.sv=dictionary.ItemAccessor(getter=lambda name:self.get_variable(name,missing_error=True,simple=True),
            setter=lambda name,value:self.set_variable(name,value,simple=True))
        # set up high-level synchronization
        self._exec_notes={}
        self._exec_notes_lock=threading.Lock()
        self._multicast_pool=multicast_pool or _default_multicast_pool
        self._multicast_pool_sids=set()
        self._stop_notifiers=[]
        # set up life control
        self._stop_requested=(self.thread_kind!="main")
        self._suspend_stop_request=False
        self._lifetime_state_lock=threading.Lock()
        self._lifetime_state="stopped"
        # set up signals
        self.moveToThread(self.thread)
        self._control_sent.connect(self._recv_control,QtCore.Qt.QueuedConnection)
        self._thread_call_request.connect(self._on_call_in_thread,QtCore.Qt.QueuedConnection)
        self._check_postponed_signals.connect(self._process_postponed_signals,QtCore.Qt.QueuedConnection)
        if self.thread_kind=="main":
            threadprop.get_app().aboutToQuit.connect(self._on_finish_event,type=QtCore.Qt.DirectConnection)
            threadprop.get_app().lastWindowClosed.connect(self._on_last_window_closed,type=QtCore.Qt.DirectConnection)
            self._recv_started_event.connect(self._on_start_event,type=QtCore.Qt.QueuedConnection) # invoke delayed start event (call in the main loop)
            self._recv_started_event.emit()
            self._lifetime_state="setup"
        else:
            self.thread.started.connect(self._on_start_event,type=QtCore.Qt.QueuedConnection)
            self.thread.finalized.connect(self._on_finish_event,type=QtCore.Qt.QueuedConnection)
    
    ### Special signals processing ###
    _control_sent=Signal(object)
    @exsafeSlot(object)
    def _recv_control(self, ctl): # control signal processing
        kind,tag,priority,value=ctl
        if kind=="message":
            if self._postpone_call(("toploop","message"),lambda: self._recv_control(ctl)):
                return
            if self.process_message(tag,value):
                return
            mq=self._message_queue.setdefault(tag,[])
            heapq.heappush(mq,(priority,self._message_uid,value))
            self._message_uid+=1
        elif kind=="interrupt":
            if self.process_interrupt(tag,value):
                return
            mq=self._message_queue.setdefault(tag,[])
            heapq.heappush(mq,(priority,self._message_uid,value))
            self._message_uid+=1
        elif kind=="sync":
            if (tag,value) in self._sync_clearance:
                self._sync_clearance.remove((tag,value))
            else:
                self._sync_queue.setdefault(tag,set()).add(value)
        elif kind=="stop":
            if self._postpone_call("stop",lambda: self._recv_control(ctl)):
                return
            with self._lifetime_state_lock:
                if self._lifetime_state!="finishing":
                    self._stop_requested=True
    def _get_next_call_counter(self):
        with self._call_counter_lock:
            cnt=self._next_place_call_counter
            self._next_place_call_counter+=1
        return cnt
    def _execute_queued_call(self, new_call=None):
        if new_call is not None:
            heapq.heappush(self._call_queue,new_call)
        while self._call_queue and self._call_queue[0][0]==self._next_execute_call_counter:
            _,call=heapq.heappop(self._call_queue)
            self._next_execute_call_counter+=1
            call.execute()
    _thread_call_request=Signal(object)
    @exsafeSlot(object)
    def _on_call_in_thread(self, call): # call signal processing
        kind=("toploop","call") if not call[2] else "call" # call=(cnt,func,interrupt)
        if not self._postpone_call(kind,lambda: self._execute_queued_call(call[:2])):
            self._execute_queued_call(call[:2])

    ### Execution starting / finishing ###
    _recv_started_event=Signal()
    started=Signal()
    """This signal is emitted after the thread has started (after the setup code has been executed, before its lifetime state is changed)"""
    @exsafeSlot()
    def _on_start_event(self):
        self._stop_requested=False
        with self._lifetime_state_lock:
            self._lifetime_state="setup"
        try:
            if self.thread_kind!="main":
                threadprop.local_data.controller=self
                threadprop.local_data.controller_name=self.name
                _register_controller(self)
            with self._lifetime_state_lock:
                self._lifetime_state="starting"
            self._poke_timer_id=self.startTimer(100) # start periodic poking timer to handle occasional event loop weirdness (getting stuck, or ignoring processed messages)
            self.notify_exec_point("start")
            self.on_start()
            self.started.emit()
            with self._lifetime_state_lock:
                self._lifetime_state="running"
            self.notify_exec_point("run")
            if self.thread_kind=="run":
                try:
                    with exint(pass_stop_exception=True):
                        self._do_run()
                finally:
                    self.thread.quit_sync()
        except threadprop.InterruptExceptionStop:
            self.thread.quit_sync()
        finally:
            if self._lifetime_state=="starting": # thread failed in self.on_start, need to notify waiting threads
                self.fail_exec_point("run")
            self.poke()  # add a message into the event loop, so that it executed and detects that the thread.quit was called
    finished=Signal()
    """This signal is emitted before the thread has finished (before the cleanup code has been executed, after its lifetime state is changed)"""
    def _kill_poke_timer(self):
        if self._poke_timer_id is not None:
            self.killTimer(self._poke_timer_id)
            self._poke_timer_id=None
    @toploopSlot()
    def _on_finish_event(self):
        with self._lifetime_state_lock:
            self._lifetime_state="finishing"
        self.notify_exec_point("cleanup")
        self._stop_requested=False
        self.finished.emit()
        try:
            with exint():
                self.check_messages()
                self.on_finish()
                self.check_messages()
        finally:
            if self.thread_kind=="main":
                stop_all_controllers(stop_self=False)
            with self._lifetime_state_lock:
                self._lifetime_state="cleanup"
            for sn in self._stop_notifiers:
                sn()
            self._stop_notifiers=[]
            for sid in self._multicast_pool_sids:
                self._multicast_pool.unsubscribe(sid)
            self._multicast_pool_sids=set()
            self.notify_exec_point("stop")
            _unregister_controller(self)
            self.thread.quit() # stop event loop (no regular messages processed after this call)
            self.poke()  # add a message into the event loop, so that it executed and detects that the thread.quit was called
            with self._lifetime_state_lock:
                self._lifetime_state="stopped"
            if self.thread_kind=="main":
                threadprop.get_app().aboutToQuit.disconnect(self._on_finish_event)
                threadprop.get_app().lastWindowClosed.disconnect(self._on_last_window_closed)
    @Slot()
    def _on_last_window_closed(self):
        if threadprop.get_app().quitOnLastWindowClosed():
            self.request_stop()



    ##########  LOCAL CALLS  ##########
    ## Methods to be called by functions executing in the controlled thread ##

    ### Message loop management ###
    def _do_run(self):
        self.run()
    def _is_postponed_executable(self, kind):
        if isinstance(kind,(tuple,frozenset)):
            return all(self._is_postponed_executable(k) for k in kind)
        if kind=="toploop":
            return self._loop_depth<=self._toploop_depth
        return kind not in self._blocked_message_kinds
    def _is_postponed_ignored(self, kind):
        if isinstance(kind,(tuple,frozenset)):
            return any(self._is_postponed_ignored(k) for k in kind)
        return kind not in self._ignored_message_kinds
    def _postpone_call(self, kind, call):
        if self._is_postponed_executable(kind):
            return False
        if not self._is_postponed_ignored(kind):
            self._postponed_calls.setdefault(frozenset(kind),[]).append(call)
        return True
    _check_postponed_signals=Signal()
    @exsafeSlot()
    def _process_postponed_signals(self):
        to_call=[]
        for kind,calls in self._postponed_calls.items():
            if calls and self._is_postponed_executable(kind):
                to_call+=calls
                calls.clear()
        for c in to_call:
            c()
    def _followup_postponed_signals(self):
        if any(calls and self._is_postponed_executable(kind) for kind,calls in self._postponed_calls.items()):
            self._check_postponed_signals.emit()
    @contextlib.contextmanager
    def allowing_toploop(self, depth=1):
        """
        Context manager which temporarily treats the current loop level and several deeper levels as a top loop.

        All event loops which lie up to `depth` below this one are treated as top loops.
        """
        toploop_depth=self._toploop_depth
        self._toploop_depth=self._loop_depth+depth
        self._followup_postponed_signals()
        try:
            yield
        finally:
            self._toploop_depth=toploop_depth
            self._followup_postponed_signals()
    @contextlib.contextmanager
    def _inner_loop(self, as_toploop=False):
        self._loop_depth+=1
        toploop_depth=self._toploop_depth
        if as_toploop:
            self._toploop_depth=max(self._toploop_depth,self._loop_depth)
            self._followup_postponed_signals()
        try:
            yield
        finally:
            self._loop_depth-=1
            if as_toploop:
                self._toploop_depth=toploop_depth
            self._followup_postponed_signals()
    @contextlib.contextmanager
    def blocking_control_signals(self, kinds="all", ignore=None):
        """
        Context manager which temporarily blocks external control signals.

        After leaving the wrapped code segment, all of the blocked but not ignored calls are executed.
        `kind` determines the kind of calls to block; it is a collection of elements among
        ``"message"``, ``"stop"``, and ``"call"`` and blocks, correspondingly, messages, stop signals,
        and any ``call_in_thread``-related requests; can be also be ``"all"``, which includes all of these categories.
        `ignore` specifies kinds which are completely ignored if sent during the blocking interval;
        can also be ``"all"``, which includes all of the `kinds` categories.
        Useful to temporarily "suspend" the thread communication with other threads, especially for the main GUI thread (e.g., to show a blocking message box).
        Local call method.
        """
        if kinds=="all":
            kinds={"message","stop","call"}
        if ignore=="all":
            ignore=kinds
        blocked_message_kinds=self._blocked_message_kinds
        self._blocked_message_kinds=blocked_message_kinds|set(kinds)
        ignored_message_kinds=self._ignored_message_kinds
        if ignore:
            self._ignored_message_kinds=ignored_message_kinds|(set(ignore)&set(kinds))
        try:
            yield
        finally:
            self._blocked_message_kinds=blocked_message_kinds
            self._ignored_message_kinds=ignored_message_kinds
            self._followup_postponed_signals()

    def _wait_in_process_loop(self, done_check, timeout=None, as_toploop=False):
        with self._inner_loop(as_toploop=as_toploop):
            ctd=general.Countdown(timeout)
            while True:
                self._check_stop_request()
                if timeout is not None:
                    time_left=ctd.time_left()
                    if time_left:
                        self._wait_timer.start(max(int(time_left*1E3),1),self)
                        threadprop.get_app().processEvents(QtCore.QEventLoop.AllEvents|QtCore.QEventLoop.WaitForMoreEvents)
                        self._wait_timer.stop()
                    else:
                        self.check_messages()
                        raise threadprop.TimeoutThreadError()
                else:
                    threadprop.get_app().processEvents(QtCore.QEventLoop.AllEvents|QtCore.QEventLoop.WaitForMoreEvents)
                # looks like sometimes processEvents(QtCore.QEventLoop.WaitForMoreEvents) returns and marks event (signal) as processed, but only processes it on the next processEvents call
                # therefore, need extra call to make sure all events are processed
                threadprop.get_app().processEvents(QtCore.QEventLoop.AllEvents)
                done,value=done_check()
                if done:
                    return value
    def wait_for_message(self, tag, timeout=None, top_loop=False):
        """
        Wait for a single message with a given tag.

        Return value of a received message with this tag.
        If timeout is passed, raise :exc:`.threadprop.TimeoutThreadError`.
        If ``top_loop==True``, treat the waiting as the top message loop (i.e., any top loop message or signal can be executed here).
        Local call method.
        """
        def done_check():
            if self._message_queue.setdefault(tag,[]):
                value=heapq.heappop(self._message_queue[tag])[-1]
                return True,value
            return False,None
        return self._wait_in_process_loop(done_check,timeout=timeout,as_toploop=top_loop)
    def new_messages_number(self, tag):
        """
        Get the number of queued messages with a given tag.
        
        Local call method.
        """
        return len(self._message_queue.setdefault(tag,[]))
    def pop_message(self, tag):
        """
        Pop the latest message with the given tag.

        Select the message with the highest priority, and among those the oldest one.
        If no messages are available, raise :exc:`.threadprop.NoMessageThreadError`.
        Local call method.
        """
        if self.new_messages_number(tag):
            return heapq.heappop(self._message_queue[tag])[-1]
        raise threadprop.NoMessageThreadError("no messages with tag '{}'".format(tag))
    def wait_for_sync(self, tag, uid, timeout=None):
        """
        Wait for synchronization signal with the given tag and UID.

        This method is rarely invoked directly, and is usually used by synchronizers code.
        If timeout is passed, raise :exc:`.threadprop.TimeoutThreadError`.
        Local call method.
        """
        def done_check():
            if uid in self._sync_queue.setdefault(tag,set()):
                self._sync_queue[tag].remove(uid)
                return True,None
            return False,None
        try:
            self._wait_in_process_loop(done_check,timeout=timeout)
        except threadprop.TimeoutThreadError:
            self._sync_clearance.add((tag,uid))
            raise
    def wait_for_any_message(self, timeout=None, top_loop=False):
        """
        Wait for any message (including synchronization messages or pokes).

        If timeout is passed, raise :exc:`.threadprop.TimeoutThreadError`.
        If ``top_loop==True``, treat the waiting as the top message loop (i.e., any top loop message or signal can be executed here).
        Local call method.
        """
        self._wait_in_process_loop(lambda: (True,None),timeout=timeout,as_toploop=top_loop)
    def wait_until(self, check, timeout=None, top_loop=False):
        """
        Wait until a given condition is true.

        Condition is given by the `check` function, which is called after every new received message and should return ``True`` if the condition is met.
        If ``top_loop==True``, treat the waiting as the top message loop (i.e., any top loop message or signal can be executed here).
        If timeout is passed, raise :exc:`.threadprop.TimeoutThreadError`.
        Local call method.
        """
        self._wait_in_process_loop(lambda: (check(),None),timeout=timeout,as_toploop=top_loop)
    def check_messages(self, top_loop=False):
        """
        Receive new messages.

        Runs the underlying message loop to process newly received message and signals (and place them in corresponding queues if necessary).
        This method is rarely invoked, and only should be used periodically during long computations to not 'freeze' the thread.
        If ``top_loop==True``, treat the waiting as the top message loop (i.e., any top loop message or signal can be executed here).
        Local call method.
        """
        with self._inner_loop(as_toploop=top_loop):
            threadprop.get_app().processEvents(QtCore.QEventLoop.AllEvents)
        self._check_stop_request()
    def sleep(self, timeout, wake_on_message=False, top_loop=False):
        """
        Sleep for a given time (in seconds).

        Unlike :func:`time.sleep`, constantly checks the event loop for new messages (e.g., if stop or interrupt commands are issued).
        In addition, if ``wake_on_message==True``, wake up if any message has been received;
        it this case. return ``True`` if the wait has been completed, and ``False`` if it has been interrupted by a message.
        If ``top_loop==True``, treat the waiting as the top message loop (i.e., any top loop message or signal can be executed here).
        If ``timeout is None``, wait forever (usually, until the application is closed, or some interrupt message raises and error).
        Local call method.
        """
        try:
            self._wait_in_process_loop(lambda: (wake_on_message,None),timeout=timeout,as_toploop=top_loop)
            return False
        except threadprop.TimeoutThreadError:
            return True
    def _check_stop_request(self):
        if self._stop_requested and not self._suspend_stop_request:
            raise threadprop.InterruptExceptionStop
    @contextlib.contextmanager
    def no_stopping(self):
        """
        Context manager, which temporarily suspends stop requests (:exc:`.InterruptExceptionStop` exceptions).

        If the stop request has been made within this block, raise the exception on exit.
        Note that :meth:`stop` method and, correspondingly, :func:`stop_controller` still work, when called from the controlled thread.
        """
        try:
            suspend_stop_request=self._suspend_stop_request
            self._suspend_stop_request=True
            yield
        finally:
            self._suspend_stop_request=suspend_stop_request
        self._check_stop_request()


    ### Overloaded methods for thread events ###
    def process_interrupt(self, tag, value):
        """
        Process a new interrupt.

        If the function returns ``False``, the interrupt is put in the corresponding queue.
        Otherwise, the the message is interrupt to be already, and it gets 'absorbed'.
        Local call method, called automatically.
        """
        if tag=="execute":
            value()
            return True
    def process_message(self, tag, value):  # pylint: disable=unused-argument
        """
        Process a new message.

        If the function returns ``False``, the message is put in the corresponding queue.
        Otherwise, the the message is considered to be already, and it gets 'absorbed'.
        Local call method, called automatically.
        """
        return False
    def on_start(self):
        """
        Method invoked on the start of the thread.

        Local call method, called automatically.
        """
    def on_finish(self):
        """
        Method invoked in the end of the thread.
        
        Called regardless of the stopping reason (normal finishing, exception, application finishing).
        Local call method, called automatically.
        """
    def run(self):
        """
        Method called to run the main thread code (only for ``"run"`` thread kind).

        Local call method, called automatically.
        """


    ### Managing multicast pool interaction ###
    def subscribe_sync(self, callback, srcs="any", tags=None, dsts="any", filt=None, subscription_priority=0, limit_queue=None, call_interrupt=True, add_call_info=False, return_result=False, sid=None):
        """
        Subscribe a synchronous callback to a multicast.

        If a multicast is sent, `callback` is called from the `dest_controller` thread (by default, thread which is calling this function)
        via the thread call mechanism (:meth:`.QThreadController.call_in_thread_callback`).
        In Qt, analogous to making a signal connection with a queued call.
        By default, the subscribed destination is the thread's name.
        Local call method.

        Args:
            callback: callback function, which takes 3 arguments: source, tag, and value.
            srcs(str or [str]): multicast source name or list of source names to filter the subscription;
                can be ``"any"`` (any source) or ``"all"`` (only multicasts specifically having ``"all"`` as a source).
            tags: multicast tag or list of tags to filter the subscription (any tag by default);
                can also contain Unix shell style pattern (``"*"`` matches everything, ``"?"`` matches one symbol, etc.)
            dsts(str or [str]): multicast destination name or list of destination names to filter the subscription;
                can be ``"any"`` (any destination) or ``"all"`` (only source specifically having ``"all"`` as a destination).
            filt(callable): additional filter function which takes 4 arguments: source, destination, tag, and value,
                and checks whether multicast passes the requirements.
            subscription_priority(int): subscription priority (higher priority subscribers are called first).
            limit_queue(int): limits the maximal number of scheduled calls
                (if the multicast is sent while at least `limit_queue` callbacks are already in queue to be executed, ignore it)
                0 or negative value means no limit (not recommended, as it can increase the queue indefinitely if the multicast rate is high enough)
            call_interrupt: whether the call is an interrupt (call inside any loop, e.g., during waiting or sleeping), or it should be called in the main event loop
            add_call_info(bool): if ``True``, add a fourth argument containing a call information (tuple with a single element, a timestamps of the call).
            return_result: if ``True``, use a result synchronizer to return the result of the subscribed call; otherwise, ignore the result
            sid(int): subscription ID (by default, generate a new unique name).
        """
        if self._multicast_pool:
            scheduler=callsync.QMulticastThreadCallScheduler(thread=self,limit_queue=limit_queue,
                interrupt=call_interrupt,call_info_argname="call_info" if add_call_info else None)
            return self.subscribe_direct(callback,srcs=srcs,dsts=dsts,tags=tags,filt=filt,subscription_priority=subscription_priority,scheduler=scheduler,return_result=return_result,sid=sid)
    def subscribe_direct(self, callback, srcs="any", tags=None, dsts="any", filt=None, subscription_priority=0, scheduler=None, return_result=False, sid=None):
        """
        Subscribe asynchronous callback to a multicast.
        
        If a multicast is sent, `callback` is called from the sending thread (not subscribed thread). Therefore, should be used with care.
        In Qt, analogous to making a signal connection with a direct call.
        By default, the subscribed destination is the thread's name.
        Local call method.

        Args:
            callback: callback function, which takes 3 arguments: source, tag, and value.
            srcs(str or [str]): multicast source name or list of source names to filter the subscription;
                can be ``"any"`` (any source) or ``"all"`` (only multicasts specifically having ``"all"`` as a source).
            tags: multicast tag or list of tags to filter the subscription (any tag by default);
                can also contain Unix shell style pattern (``"*"`` matches everything, ``"?"`` matches one symbol, etc.)
            dsts(str or [str]): multicast destination name or list of destination names to filter the subscription;
                can be ``"any"`` (any destination) or ``"all"`` (only source specifically having ``"all"`` as a destination).
            filt(callable): additional filter function which takes 4 arguments: source, destination, tag, and value,
                and checks whether multicast passes the requirements.
            subscription_priority(int): subscription priority (higher priority subscribers are called first).
            scheduler: if defined, multicast call gets scheduled using this scheduler instead of being called directly (which is the default behavior)
            return_result: if ``True``, use a result synchronizer to return the result of the subscribed call; otherwise, ignore the result
            sid(int): subscription ID (by default, generate a new unique id and return it).
        """
        if self._multicast_pool:
            sid=self._multicast_pool.subscribe_direct(callback,srcs=srcs,dsts=dsts or self.name,tags=tags,filt=filt,priority=subscription_priority,scheduler=scheduler,return_result=return_result,sid=sid)
            self._multicast_pool_sids.add(sid)
            return sid
    def unsubscribe(self, sid):
        """
        Unsubscribe from a subscription with a given ID.
        
        Note that multicasts which are already emitted but not processed will remain in the queue;
        if they need to be ignored, it should be handled explicitly.
        Local call method.
        """
        self._multicast_pool_sids.remove(sid)
        self._multicast_pool.unsubscribe(sid)
    def send_multicast(self, dst="any", tag=None, value=None, src=None, filter_results=True):
        """
        Send a multicast to the multicast pool.

        By default, the multicast source is the thread's name.
        Return result synchronizers for all executed subscribed methods.
        Local call method.

        Args:
            dst(str): multicast destination; can be a name, ``"all"`` (will pass all subscribers' destination filters),
                or ``"any"`` (will only be passed to subscribers specifically subscribed to multicast with ``"any"`` destination).
            tag(str): multicast tag.
            value: multicast value.
            src(str): multicast source; can be ``None`` (current thread name), a specific name, ``"all"`` (will pass all subscribers' source filters),
                or ``"any"`` (will only be passed to subscribers specifically subscribed to multicast with ``"any"`` source).
            filter_results: if ``True``, filter the results to exclude dummy synchronizers, which correspond to calls which do not return anything
        """
        result=self._multicast_pool.send(src or self.name,dst,tag,value)
        if filter_results:
            result=[r for r in result if not getattr(r,"_not_synchronizer",False)]
        return result
    def send_multicast_sync(self, dst="any", tag=None, value=None, src=None, timeout=None, default_result=None, pass_exception=True):
        """
        Send a multicast to the multicast pool and synchronize the results, if available.

        By default, the multicast source is the thread's name.
        Results are collected and synchronized only from the subscriptions which return them (i.e., set ``return_result=True``).
        Local call method.

        Args:
            dst(str): multicast destination; can be a name, ``"all"`` (will pass all subscribers' destination filters),
                or ``"any"`` (will only be passed to subscribers specifically subscribed to multicast with ``"any"`` destination).
            tag(str): multicast tag.
            value: multicast value.
            src(str): multicast source; can be ``None`` (current thread name), a specific name, ``"all"`` (will pass all subscribers' source filters),
                or ``"any"`` (will only be passed to subscribers specifically subscribed to multicast with ``"any"`` source).
            timeout: synchronization timeout (``None`` means waiting forever)
            default_result: default result value if synchronization failed (timed out, thread stopped, etc.)
            pass_exception: if ``True`` and the signal processor raised an exception, raise it in this thread as well
                If ``pass_exception==True`` and the returned value represents exception, re-raise it in the caller thread; otherwise, return `default`.
        """
        syncs=self.send_multicast(dst=dst,tag=tag,value=value,src=src)
        return [s.get_value_sync(timeout=timeout,default=default_result,pass_exception=pass_exception) for s in syncs]


    ### Variable management ###
    _variable_change_tag="#sync.wait.variable"
    def set_variable(self, name, value, update=False, notify=False, notify_tag="changed/*", simple=False):
        """
        Set thread variable.

        Can be called in any thread (controlled or external).
        If ``notify==True``, send an multicast with the given `notify_tag` (where ``"*"`` symbol is replaced by the variable name).
        If ``update==True`` and the value is a dictionary, update the branch rather than overwrite it.
        If ``simple==True``, assume that the result is a single atomic variable, in which case the lock is not used;
        note that in this case the threads waiting on this variable (or branches containing it) will not be notified.
        Local call method.
        """
        if simple:
            if update:
                self._params_val.merge(value,name)
            else:
                self._params_val.add_entry(name,value,force=True)
        else:
            split_name=tuple(dictionary.normalize_path(name))
            notify_list=[]
            with self._params_val_lock:
                if name in self._params_funcs:
                    del self._params_funcs[name]
                if update:
                    self._params_val.merge(value,name)
                else:
                    self._params_val.add_entry(name,value,force=True)
                for exp_name in self._params_exp:
                    if exp_name==split_name[:len(exp_name)] or split_name==exp_name[:len(split_name)]:
                        notify_list.append((self._params_val[exp_name],self._params_exp[exp_name]))
            for val,lst in notify_list:
                for ctl in lst:
                    ctl.send_interrupt(self._variable_change_tag,val)
        if notify:
            notify_tag=notify_tag.replace("*",name)
            self.send_multicast("any",notify_tag,value)
    def delete_variable(self, name, missing_error=False):
        """
        Delete thread variable.

        If ``missing_error==False`` and no variable exists, do nothing; otherwise, raise and error.
        Local call method.
        """
        with self._params_val_lock:
            if name in self._params_val:
                del self._params_val[name]
            elif name in self._params_funcs:
                del self._params_funcs[name]
            elif not missing_error:
                raise KeyError("no thread variable {}".format(name))
    def set_func_variable(self, name, func, use_lock=True):
        """
        Set a 'function' variable.

        Acts as a thread variable to the external user, but instead of reading a stored value, it executed a function instead.
        Note, that the function is executed in the caller thread (i.e., the thread which tries to access the variable),
        so use of synchronization methods (commands, signals, locks) is highly advised.

        If ``use_lock==True``, then the function call will be wrapped into the usual variable lock,
        i.e., it won't run concurrently with other variable access.
        Local call method.
        """
        with self._params_val_lock:
            self._params_funcs[name]=func,use_lock
            if name in self._params_val:
                del self._params_val[name]
    def _has_variable(self, name):
        with self._params_val_lock:
            return name in self._params_val


    ### Thread methods management ###
    def add_thread_method(self, name, method, interrupt=True):
        """
        Add a thread method.

        Adds a named method to the thread, which can be called later using :meth:`call_thread_method`.
        This method will be called in this thread.
        
        Useful for GUI thread to set up some global access methods, which other threads can safely use.
        For :class:`QTaskThread` threads it's a better idea to set up a command instead.
        Local call method.
        """
        self._thread_methods[name]=lambda *args,**kwargs: self.call_in_thread_sync(method,args=args,kwargs=kwargs,sync=True,same_thread_shortcut=True,interrupt=interrupt)
    def delete_thread_method(self, name):
        """
        Delete a thread method.
        
        Local call method.
        """
        del self._thread_methods[name]
    def call_thread_method(self, name, *args, **kwargs):
        """
        Call a thread method.
        
        Method needs to be set up beforehand using :meth:`add_thread_method`. It is always executed in the current thread.
        Local call method.
        """
        return self._thread_methods[name](*args,**kwargs)

    ##########  EXTERNAL CALLS  ##########
    ## Methods to be called by functions executing in other thread ##

    ### Request synchronization ###
    def send_message(self, tag, value, priority=0):
        """
        Send a message to the thread with a given tag, value and priority.
        
        External call method.
        """
        self._control_sent.emit(("message",tag,priority,value))
    def send_interrupt(self, tag, value, priority=0):
        """
        Send an interrupt message to the thread with a given tag, value and priority.
        
        External call method.
        """
        self._control_sent.emit(("interrupt",tag,priority,value))
    def send_sync(self, tag, uid):
        """
        Send a synchronization signal with the given tag and UID.

        This method is rarely invoked directly, and is usually used by synchronizers code (e.g., :class:`.QThreadNotifier`).
        External call method.
        """
        self._control_sent.emit(("sync",tag,0,uid))


    ### Variables access ###
    def get_variable(self, name, default=None, copy_branch=True, missing_error=False, simple=False):
        """
        Get thread variable.

        If ``missing_error==False`` and no variable exists, return `default`; otherwise, raise and error.
        If ``copy_branch==True`` and the variable is a :class:`.Dictionary` branch, return its copy to ensure that it stays unaffected on possible further variable assignments.
        If ``simple==True``, assume that the result is a single atomic variable, in which case the lock is not used;
        this only works with actual variables and not function variables.
        Universal call method.
        """
        if simple:
            return self._params_val[name] if missing_error else self._params_val.get(name,default)
        with self._params_val_lock:
            if name in self._params_val:
                var=self._params_val[name]
                if copy_branch and dictionary.is_dictionary(var):
                    var=var.copy()
            elif name in self._params_funcs:
                func,use_lock=self._params_funcs[name]
                if use_lock:
                    with self._params_val_lock:
                        var=func()
                else:
                    var=func()
            elif missing_error:
                raise KeyError("no thread variable {}".format(name))
            else:
                var=default
        return var
    def sync_variable(self, name, pred, timeout=None):
        """
        Wait until thread variable with the given `name` satisfies the condition given by `pred`.
        
        `pred` can be a variable values, a container (list, set, tuple) of possible values,
        or a function which takes one argument (variable value) and returns whether the condition is satisfied.
        It is executed in the caller thread.
        External call method.
        """
        if not hasattr(pred,"__call__"):
            v=pred
            if isinstance(pred,(tuple,list,set,dict)):
                pred=lambda x: x in v
            else:
                pred=lambda x: x==v
        ctl=threadprop.current_controller()
        split_name=tuple(dictionary.normalize_path(name))
        with self._params_exp_lock:
            self._params_exp.setdefault(split_name,[]).append(ctl)
        ctd=general.Countdown(timeout)
        try:
            value=self.get_variable(name)
            while True:
                if pred(value):
                    return value
                value=ctl.wait_for_message(self._variable_change_tag,timeout=ctd.time_left())
        finally:
            with self._params_exp_lock:
                self._params_exp[split_name].remove(ctl)
                if not self._params_exp[split_name]:
                    del self._params_exp[split_name]


    ### Thread execution control ###
    def start(self):
        """
        Start the thread.

        External call method.
        """
        self.thread.start()
    def request_stop(self):
        """
        Request thread stop (send a stop command).
        
        External call method.
        """
        self._control_sent.emit(("stop",None,0,None))
    def stop(self, code=0, sync=False):
        """
        Stop the thread.

        If called from the thread, stop immediately by raising a :exc:`.threadprop.InterruptExceptionStop` exception. Otherwise, schedule thread stop.
        If the thread kind is ``"main"``, stop the whole application with the given exit code. Otherwise, stop the thread.
        If ``sync==True`` and the thread is not main or current, wait until it is completely stopped.
        Universal call method.
        """
        if self.thread_kind=="main":
            def exit_main():
                threadprop.get_app().exit(code)
                self.request_stop()
            self.call_in_thread_callback(exit_main)
        else:
            self.thread.quit_sync()
        if self.is_in_controlled():
            raise threadprop.InterruptExceptionStop
        elif sync and self.thread_kind!="main":
            self.sync_stop()
    def sync_stop(self):
        """
        Wait until the controller and the thread are stopped.
        
        External call method.
        """
        self.sync_exec_point("stop")
        self.thread.wait()
    def poke(self):
        """
        Send a dummy message to the thread.
        
        A cheap way to notify the thread that something happened (useful for, e.g., making thread leave :meth:`wait_for_any_message` method).
        External call method.
        """
        self._control_sent.emit(("poke",None,0,None))
    def running(self):
        """Check if the thread is running"""
        return self._lifetime_state in {"starting","running","finishing"}
    def finishing(self):
        """Check if the thread is finishing"""
        return self._lifetime_state in {"finishing"}
    def _check_running(self, error=True):
        """Check if the thread is running, raise an exception if it is not"""
        if not self.running():
            if error:
                raise threadprop.NoControllerThreadError("thread {} is not running".format(self.name))
            return False
        return True


    ### Notifier access ###
    def _get_exec_note(self, point):
        with self._exec_notes_lock:
            if point not in self._exec_notes:
                self._exec_notes[point]=synchronizing.QMultiThreadNotifier()
            return self._exec_notes[point]
    def notify_exec_point(self, point):
        """
        Mark the given execution point as passed.
        
        Automatically invoked points include ``"start"`` (thread starting), ``"run"`` (thread setup and ready to run),
        ``"cleanup"`` (thread stopping is invoked, starting to clean up) and ``"stop"`` (thread finished).
        Can be extended for arbitrary points.
        Local call method.
        """
        self._get_exec_note(point).notify()
    def fail_exec_point(self, point):
        """
        Mark the given execution point as failed.
        
        Automatically invoked for ``"run"`` (thread setup and ready to run) if the startup raised an error before the thread properly started
        (``"start"``, ``"cleanup"``, and ``"stop"`` are notified in any case)
        Can be extended for arbitrary points.
        Local call method.
        """
        self._get_exec_note(point).fail()
    def get_exec_counter(self, point):
        """
        Get the counter (number of notifications) for the given point.

        See :meth:`sync_exec_point` for details.
        External call.
        """
        return self._get_exec_note(point).wait(-1)-1
    def sync_exec_point(self, point, timeout=None, counter=1):
        """
        Wait for the given execution point.
        
        Automatically invoked points include ``"start"`` (thread starting), ``"run"`` (thread setup and ready to run),
        ``"cleanup"`` (thread stopping is invoked, starting to clean up) and ``"stop"`` (thread finished).
        If timeout is passed, raise :exc:`.threadprop.TimeoutThreadError`.
        `counter` specifies the minimal number of pre-requisite :meth:`notify_exec_point` calls to finish the waiting (by default, a single call is enough).
        Return actual number of notifier calls up to date.
        External call method.
        """
        return self._get_exec_note(point).wait(timeout=timeout,state=counter)-1
    def add_stop_notifier(self, func, call_if_stopped=True):
        """
        Add stop notifier: a function which is called when the thread is about to be stopped (left the main message loop).

        The supplied function is called in the controlled thread close to its shutdown, so it should be short, non-blocking, and thread-safe.
        If the thread is already stopped and ``call_if_stopped==True``, call `func` immediately (from the caller's thread).
        Return ``True`` if the thread is still running and the notifier is added, and ``False`` otherwise.
        Local call method.
        """
        with self._lifetime_state_lock:
            if self._lifetime_state not in {"cleanup","stopped"}:
                if func not in self._stop_notifiers:
                    self._stop_notifiers.append(func)
                return True
        if call_if_stopped:
            func()
        return False
    def remove_stop_notifier(self, func):
        """
        Remove the stop notifier from this controller.

        Return ``True`` if the notifier was in this thread and is now removed, and ``False`` otherwise.
        Local call method.
        """
        with self._lifetime_state_lock:
            try:
                self._stop_notifiers.remove(func)
                return True
            except ValueError:
                return False


    ### Simple inquiring methods ###
    def is_in_controlled(self):
        """Check if the thread executing this code is controlled by this controller"""
        return threadprop.current_controller(require_controller=False) is self
    

    ### External call management ###
    def _place_call(self, call, tag=None, priority=0, interrupt=True):
        if tag is None:
            cnt=self._get_next_call_counter()
            self._thread_call_request.emit((cnt,call,interrupt))
        else:
            if interrupt:
                self.send_interrupt(tag,call,priority=priority)
            else:
                self.send_message(tag,call,priority=priority)
    def call_in_thread_callback(self, func, args=None, kwargs=None, callback=None, tag=None, priority=0, interrupt=True):
        """
        Call a function in this thread with the given arguments.

        If `callback` is supplied, call it with the result as a single argument (call happens in the controller thread).
        If `tag` is supplied, send the call in a message with the given tag; otherwise, use the interrupt call (generally, higher priority method).
        If ``interrupt==True``, method can be called inside any control loop (either main loop, or during waiting); otherwise, only call it in the top loop.
        Universal call method.
        """
        call=callsync.QScheduledCall(func,args,kwargs,result_synchronizer="async")
        if callback:
            call.add_callback(callback,pass_result=True,call_on_exception=False)
        self._place_call(call,tag=tag,priority=priority,interrupt=interrupt)
    def call_in_thread_sync(self, func, args=None, kwargs=None, sync=True, callback=None, timeout=None, default_result=None, pass_exception=True, silent=False, tag=None, priority=0, interrupt=True, error_on_stopped=True, same_thread_shortcut=True):
        """
        Call a function in this thread with the given arguments.

        If ``sync==True``, calling thread is blocked until the controlled thread executes the function, and the function result is returned
        (in essence, the fact that the function executes in a different thread is transparent).
        Otherwise, exit call immediately, and return a synchronizer object (:class:`.QCallResultSynchronizer`),
        which can be used to check if the call is done (method `is_done`) and obtain the result (method :meth:`.QCallResultSynchronizer.get_value_sync`).
        If `callback` is not ``None``, call it after the function is successfully executed (from the target thread), with a single parameter being function result.
        If ``pass_exception==True`` and `func` raises an exception, re-raise it in the caller thread (applies only if ``sync==True``).
        If ``silent==True`` and `func` raises an exception, silence it in the execution thread and only re-raise it in the caller thread;
        note that if ``pass_exception==False`` and ``silent==True``, the exception is ignored in both threads.
        If `tag` is supplied, send the call in a message with the given tag and priority; otherwise, use the interrupt call (generally, higher priority method).
        If ``interrupt==True``, method can be called inside any control loop (either main loop, or during waiting); otherwise, only call it in the top loop.
        If ``error_on_stopped==True`` and the controlled thread is stopped before it executed the call, raise :exc:`.threadprop.NoControllerThreadError`; otherwise, return `default_result`.
        If ``same_thread_shortcut==True`` (default), the call is synchronous, and the caller thread is the same as the controlled thread, call the function directly.
        Universal call method.
        """
        if same_thread_shortcut and tag is None and sync and self.is_in_controlled():
            res=func(*(args or []),**(kwargs or {}))
            if callback:
                callback(res)
            return res
        call=callsync.QScheduledCall(func,args,kwargs,silent=silent)
        if callback:
            call.add_callback(callback,pass_result=True,call_on_exception=False)
        if self.add_stop_notifier(call.fail):
            call.add_callback(lambda: self.remove_stop_notifier(call.fail),call_on_exception=True,pass_result=False)
        self._place_call(call,tag=tag,priority=priority,interrupt=interrupt)
        result=call.result_synchronizer
        if sync:
            result=result.get_value_sync(timeout=timeout,default=default_result,pass_exception=pass_exception,error_on_fail=error_on_stopped)
        return result










class QTaskThread(QThreadController):
    """
    Thread which allows to set up and run jobs and batch jobs with a certain time period, and execute commands in the meantime.

    Args:
        name(str): thread name (by default, generate a new unique name)
        args: args supplied to :meth:`setup_task` method
        kwargs: keyword args supplied to :meth:`setup_task` method
        multicast_pool: :class:`.MulticastPool` for this thread (by default, use the default common pool)

    Attributes:
        ca: asynchronous command accessor, which makes calls more function-like;
            ``ctl.ca.comm(*args,**kwarg)`` is equivalent to ``ctl.call_command("comm",args,kwargs,sync=False)``
        cai: asynchronous command accessor which ignores and silences any exceptions (including missing /stopped controller)
            useful for sending queries during thread finalizing / application shutdown, when it's not guaranteed that the command recipient is running
            ``ctl.cai.comm(*args,**kwarg)`` is equivalent to ``ctl.call_command("comm",args,kwargs,sync=False,ignore_errors=True)``
        cad: asynchronous command accessor returning a result synchronizer, which makes calls more function-like;
            ``ctl.cad.comm(*args,**kwarg)`` is equivalent to ``ctl.call_command("comm",args,kwargs,sync="delayed")``
        cs: synchronous command accessor, which makes calls more function-like;
            ``ctl.cs.comm(*args,**kwarg)`` is equivalent to ``ctl.call_command("comm",args,kwargs,sync=True)``
        css: synchronous command accessor which is made 'exception-safe' via :func:`exsafe` wrapper (i.e., safe to directly connect to slots)
            ``ctl.css.comm(*args,**kwarg)`` is equivalent to ``with exint(): ctl.call_command("comm",args,kwargs,sync=True)``
        csi: synchronous command accessor which ignores and silences any exceptions (including missing /stopped controller)
            useful for sending queries during thread finalizing / application shutdown, when it's not guaranteed that the command recipient is running
        m: method accessor; directly calls the method corresponding to the command;
            ``ctl.m.comm(*args,**kwarg)`` is equivalent to ``ctl.call_command("comm",*args,**kwargs)``, which is often also equivalent to ``ctl.comm(*args,**kwargs)``;
            for most practical purposes it's the same as directly invoking the class method, but it makes intent more explicit
            (as command methods are usually not called directly from other threads), and it doesn't invoke warning about calling method instead of command from another thread.

    Methods to overload:
        - :meth:`setup_task`: executed on the thread startup (between synchronization points ``"start"`` and ``"run"``)
        - :meth:`finalize_task`: executed on thread cleanup (attempts to execute in any case, including exceptions)
    """
    ## Action performed when another thread explicitly calls a method corresponding to a command (which is usually a typo)
    ## Can be used to overload default behavior in children classes or instances
    ## Can be ``"warning"``, which prints warning about this call (default),
    ## or one of the accessor names (e.g., ``"c"`` or ``"q"``), which routes the call through this accessor
    _direct_comm_call_action="warning"
    _loop_wait_period=1. # time to wait in the main loop between scheduling events, if no events come; exact value does not affect anything
    TBatchJob=collections.namedtuple("TBatchJob",["job","cleanup","min_run_time","priority"])
    TCommand=collections.namedtuple("TCommand",["command","scheduler","priority"])
    def __init__(self, name=None, args=None, kwargs=None, multicast_pool=None):
        super().__init__(name=name,kind="run",multicast_pool=multicast_pool)
        self.sync_period=0 # minimal time to check on the Qt event loop while running the internal scheduling loop
        self.min_schedule_time=0. # minimal time to sleep between scheduling checks; acts as a quantum of scheduling
        self._last_sync_time=0
        self.jobs={}
        self._jobs_list=[]
        self.batch_jobs={}
        self._batch_jobs_args={}
        self._batch_jobs_stopreq=set()
        self._batch_jobs_namegen=general.NamedUIDGenerator()
        self.args=args or []
        self.kwargs=kwargs or {}
        self._commands={}
        self._in_command_loop=False
        self._poked=False
        self._priority_queues={}
        self._priority_queues_order=[]
        self._priority_queues_lock=threading.Lock()
        self._command_warned=set()
        self._pause_lock=synchronizing.QLockNotifier()
        self.ca=self.CommandAccess(self,sync=False)
        self.cai=self.CommandAccess(self,sync=False,ignore_errors=True)
        self.cad=self.CommandAccess(self,sync="delayed")
        self.cs=self.CommandAccess(self,sync=True)
        self.css=self.CommandAccess(self,sync=True,safe=True)
        self.csi=self.CommandAccess(self,sync=True,safe=True,ignore_errors=True)
        self.m=self.CommandAccess(self,sync=True,direct=True)

    ### Job handling ###
    # Called only in the controlled thread #

    class Job:
        """
        A single job loop.

        Deals with scheduling, time counting, pausing, and cleanup.

        Args:
            job: job function
            period: job period
            queue: thread controller's scheduling queue, to which the job must be added
            jobs_order: thread controller's job queue which determines the jobs scheduling order
        """
        def __init__(self, job, period, queue, jobs_order):
            self.job=job
            self.ctd=general.Countdown(period)
            self.queue=queue
            self.jobs_order=jobs_order
            self.jobs_order.append(self)
            self.paused=False
            self.call=None
            self.scheduled=False
        def schedule(self):
            """Schedule the job"""
            if self.scheduled:
                raise RuntimeError("job is already scheduled")
            self.call=self.queue.build_call(self.job,sync_result=False)
            self.call.add_callback(self.mark_unscheduled,pass_result=False,call_on_unschedule=True)
            self.scheduled=True
            self.queue.schedule(self.call)
            self.jobs_order.remove(self)
            self.jobs_order.append(self)
            self.ctd.add_time(self.ctd.timeout)
        def mark_unscheduled(self):
            """
            Mark the job as unscheduled.

            Called automatically on job completion.
            """
            self.call=None
            self.scheduled=False
        def unschedule(self):
            """Manually unschedule the job (e.g., when paused or removed)"""
            if not self.scheduled:
                raise RuntimeError("unscheduled job can't be unscheduled")
            self.queue.unschedule(self.call)
            self.call=None
            self.scheduled=False
        def clear(self):
            """Clear the job and remove it from the jobs list"""
            if self.scheduled:
                self.unschedule()
            self.jobs_order.remove(self)
        def change_period(self, period):
            """Change the job period"""
            self.ctd.set_timeout(period)
        def pause(self, paused=True, unschedule=True):
            """
            Pause or resume the job.

            If pausing and ``unschedule==True``, remove already scheduled job from the queue.
            """
            if not self.paused and paused and unschedule:
                self.unschedule()
            self.paused=paused
        def time_left(self, t=None):
            """Get the amount of time left till the next call, or ``None`` if the job is paused"""
            if self.paused:
                return None
            return self.ctd.time_left(t)
        

    def add_job(self, name, job, period, initial_call=True, priority=-10):
        """
        Add a recurrent `job` which is called every `period` seconds.

        The job starts running automatically when the main thread loop start executing.
        If ``initial_call==True``, call `job` once immediately after adding.
        `priority` specifies the call priority in the scheduling queue;
        by default, it is lower than the command and multicasts (0).
        Local call method.
        """
        if name in self.jobs:
            raise ValueError("job {} already exists".format(name))
        self.jobs[name]=self.Job(job,period,self._get_priority_queue(priority),self._jobs_list)
        if initial_call:
            job()
    def change_job_period(self, name, period):
        """
        Change the period of the job `name`.
        
        Local call method.
        """
        if name not in self.jobs:
            raise ValueError("job {} doesn't exists".format(name))
        self.jobs[name].change_period(period)
    def remove_job(self, name):
        """
        Remove the job `name` from the job list.
        
        Local call method.
        """
        if name not in self.jobs:
            raise ValueError("job {} doesn't exists".format(name))
        self.jobs[name].clear()
        del self.jobs[name]
        
    def add_batch_job(self, name, job, cleanup=None, min_runtime=0, priority=-10):
        """
        Add a batch `job` which is executed once, but with continuations.

        After this call the job is just created, but is not running. To start it, call :meth:`start_batch_job`.
        If specified, `cleanup` is a finalizing function which is called both when the job terminates normally,
        and when it is forcibly stopped (including thread termination).
        `min_runtime` specifies minimal expected runtime of a job; if a job executes faster than this time,
        it is repeated again unless at least `min_runtime` seconds passed; useful for high-throughput jobs,
        as it reduces overhead from the job scheduling mechanism (repeating within `min_runtime` time window is fast)

        Unlike the usual recurrent jobs, here `job` is a generator (usually defined by a function with ``yield`` statement).
        When the job is running, the generator is periodically called until it raises :exc:`StopIteration` exception, which signifies that the job is finished.
        From generator function point of view, after the job is started, the function is executed normally,
        but every time ``yield`` statement is encountered, the execution is suspended for `period` seconds (specified in :meth:`start_batch_job`).
        `priority` specifies the call priority in the scheduling queue;
        by default, it is lower than the command and multicasts (0).
        Local call method.
        """
        if name in self.jobs or name in self.batch_jobs:
            raise ValueError("job {} already exists".format(name))
        self.batch_jobs[name]=self.TBatchJob(job,cleanup,min_runtime,priority)
    def change_batch_job_parameters(self, name, job="keep", cleanup="keep", min_runtime="keep", priority="keep", stop=False, restart=False):
        """
        Change parameters (main body, cleanup function, and minimal runtime) of the batch job.

        The parameters are the same as for :meth:`add_batch_job`. If any of them are ``"keep"``, don't change them.
        If ``stop==True``, stop the job before changing the parameters;
        otherwise the job is continued with the previous parameters (including cleanup) until it is stopped and restarted.
        If ``restart==True``, restart the job after changing the parameters.
        Local call method.
        """
        if name not in self.batch_jobs:
            raise ValueError("batch job {} doesn't exists".format(name))
        running=self.is_batch_job_running(name)
        if (stop or restart) and running:
            period,args,kwargs,_=self._batch_jobs_args[name]
            self.stop_batch_job(name,error_on_stopped=False)
        if job=="keep":
            job=self.batch_jobs[name].job
        if cleanup=="keep":
            cleanup=self.batch_jobs[name].cleanup
        if min_runtime=="keep":
            min_runtime=self.batch_jobs[name].min_runtime
        if priority=="keep":
            priority=self.batch_jobs[name].priority
        self.batch_jobs[name]=self.TBatchJob(job,cleanup,min_runtime,priority)
        if restart and running:
            self.start_batch_job(name,period,*args,**kwargs)
    def remove_batch_job(self, name):
        """
        Remove the batch job `name`, stopping it if necessary.
        
        Local call method.
        """
        self.stop_batch_job(name)
        del self.batch_jobs[name]
    def start_batch_job(self, name, period, *args, start_immediate=True, **kwargs):
        """
        Start the batch job with the given name.

        `period` specifies suspension period. Optional arguments are passed to the job and the cleanup functions.
        If ``start_immediate==True``, start the job (i.e., run the first iteration) immediately during the call;
        otherwise, start it only when it is scheduled, after the currently running call is complete.
        Local call method.
        """
        if name not in self.batch_jobs:
            raise ValueError("job {} doesn't exists".format(name))
        if name in self.jobs:
            self.stop_batch_job(name)
        if name in self._batch_jobs_stopreq:
            self._batch_jobs_stopreq.remove(name)
        job,cleanup,min_runtime,priority=self.batch_jobs[name]
        self._batch_jobs_args[name]=(period,args,kwargs,cleanup)
        gen=job(*args,**kwargs)
        def do_step():
            cnt=general.Countdown(min_runtime) if min_runtime else None
            try:
                while True:
                    if name in self._batch_jobs_stopreq:
                        self._batch_jobs_stopreq.remove(name)
                        raise StopIteration
                    p=next(gen)
                    if p is not None:
                        self.change_job_period(name,p)
                    if cnt is None or cnt.passed():
                        return
            except StopIteration:
                pass
            self.stop_batch_job(name)
        self.add_job(name,do_step,period,priority=priority,initial_call=start_immediate)
    def is_batch_job_running(self, name):
        """
        Check if a given batch job running.
        
        Local call method.
        """
        if name not in self.batch_jobs:
            raise ValueError("job {} doesn't exists".format(name))
        return name in self.jobs
    def stop_batch_job(self, name, stop_immediate=True, error_on_stopped=False):
        """
        Stop a given batch job.
        
        If ``error_on_stopped==True`` and the job is not currently running, raise an error. Otherwise, do nothing.
        If ``stop_immediate==True``, stop the job (i.e., unschedule it and run the cleanup code) immediately during the call;
        otherwise, stop it when its next iteration is called.
        Local call method.
        """
        if name not in self.batch_jobs:
            raise ValueError("job {} doesn't exists".format(name))
        if name not in self.jobs:
            if error_on_stopped:
                raise ValueError("job {} is not running".format(name))
            return
        if not stop_immediate:
            self._batch_jobs_stopreq.add(name)
            return
        self.remove_job(name)
        _,args,kwargs,cleanup=self._batch_jobs_args.pop(name)
        if cleanup:
            cleanup(*args,**kwargs)
    def restart_batch_job(self, name, start_immediate=True, error_on_stopped=False):
        """
        Restart the running batch job with its current arguments.

        If ``error_on_stopped==True`` and the job is not currently running, raise an error. Otherwise, do nothing.
        Local call method.
        """
        period,args,kwargs,_=self._batch_jobs_args[name]
        self.stop_batch_job(name,stop_immediate=True,error_on_stopped=error_on_stopped)
        self.start_batch_job(name,period,*args,start_immediate=start_immediate,**kwargs)
    def run_as_batch_job(self, job, period, cleanup=None, name=None, priority=-10, start_immediate=True, args=None, kwargs=None):
        """
        Create a temporarily batch job and immediately run it.

        If `name` is ``None``, generate a new unique name.
        The job is removed after it is complete (i.e., after cleanup).
        Note that this implies, that it can not be restarted using :meth:`restart_batch_job`, as it will be removed after the stopping before the restart.
        All the parameters are the same as for :meth:`add_batch_job` and :meth:`start_batch_job`.
        Return the batch job name (either supplied or newly generated).
        """
        if name is None:
            while True:
                name=self._batch_jobs_namegen("temp_job")
                if name not in self.batch_jobs:
                    break
        if cleanup is None:
            def full_cleanup(*args, **kwargs):  # pylint: disable=unused-argument
                self.remove_batch_job(name)
        else:
            def full_cleanup(*args, **kwargs):
                cleanup(*args,**kwargs)
                self.remove_batch_job(name)
        self.add_batch_job(name,job,cleanup=full_cleanup,priority=priority)
        self.start_batch_job(name,period,*(args or []),start_immediate=start_immediate,**(kwargs or {}))
        return name

    def _get_priority_queue(self, priority):
        """Get the queue with the given priority, creating one if it does not exist"""
        if priority not in self._priority_queues:
            with self._priority_queues_lock:
                q=callsync.QQueueScheduler()
                self._priority_queues[priority]=q
                self._priority_queues_order=[self._priority_queues[p] for p in sorted(self._priority_queues,reverse=True)]
        return self._priority_queues[priority]
    def _check_priority_queues(self):
        """
        Check all priority queues for pending calls.

        If calls are available, execute the oldest highest priority call and return ``True``; otherwise, return ``False``.
        """
        for scheduler in self._priority_queues_order:
            call=scheduler.pop_call()
            if call is not None:
                with self._pause_lock:
                    call.execute()
                return True
        return False
    def _schedule_pending_jobs(self, t=None):
        """
        Check if there are any pending jobs and schedule them.

        Return the time to wait until the next job needs to be scheduled.
        Return time is 0 if a job has been scheduled during that call,
        and ``None`` if there are not jobs to schedule.
        """
        wait_time=None
        t=t or time.time()
        for job in self._jobs_list:
            if not job.scheduled:
                l=job.time_left(t)
                if l is not None:
                    if l<=0:
                        job.schedule()
                    wait_time=l if wait_time is None else min(wait_time,l)
        return wait_time
    def _exhaust_queued_calls(self):
        """Keep extracting and executing queued calls (commands, jobs, multicasts) as long as there are any available"""
        self._in_command_loop=True
        while True:
            self._schedule_pending_jobs()
            called=self._check_priority_queues()
            if not called:
                break
            if self.sync_period<=0:
                self.check_messages(top_loop=True)
            else:
                t=time.time()
                if t>self._last_sync_time+self.sync_period:
                    self._last_sync_time=t
                    self.check_messages(top_loop=True)
        self._in_command_loop=False
        self._poked=False
        self._check_priority_queues()
    def _command_poke(self):
        if not self._in_command_loop and not self._poked:
            self.poke()
            self._poked=True
    
    ### Start/run/stop control (called automatically) ###

    def run(self):
        if not self.is_in_controlled():
            raise RuntimeError("calling 'run' methods from a non-controlled thread; did you mean 'start' instead?")
        schedule_time=0
        while True:
            ct=time.time()
            to=self._schedule_pending_jobs(ct)
            sleep_time=self._loop_wait_period if to is None else min(self._loop_wait_period,to)
            if schedule_time<=0 and sleep_time>=0:
                if self._poked:
                    self.check_messages()
                else:
                    self.sleep(sleep_time,wake_on_message=True)
            self._poked=False
            self._exhaust_queued_calls()
            schedule_time=ct+self.min_schedule_time-time.time()
            if schedule_time>0:
                self.sleep(schedule_time)

    def on_start(self):
        super().on_start()
        self.add_command("add_job",priority=10)
        self.add_command("change_job_period",priority=10)
        self.add_command("remove_job",priority=10)
        self.add_command("add_batch_job",priority=10)
        self.add_command("change_batch_job_parameters",priority=10)
        self.add_command("remove_batch_job",priority=10)
        self.add_command("start_batch_job",priority=10)
        self.add_command("is_batch_job_running",priority=10)
        self.add_command("stop_batch_job",priority=10)
        self.add_command("restart_batch_job",priority=10)
        self.add_command("run_as_batch_job",priority=10)
        self.add_command("add_command",priority=10)
        self.add_command("subscribe_commsync",priority=10)
        self.add_command("unsubscribe",priority=10)
        self.setup_task(*self.args,**self.kwargs)
    def on_finish(self):
        super().on_finish()
        for n in self.batch_jobs:
            if n in self.jobs:
                self.stop_batch_job(n)
        try:
            self.finalize_task()
        finally:
            for q in self._priority_queues.values():
                q.clear()


    ### Command call methods ###

    def _call_command_method(self, name, original_method, args, kwargs):
        """Call given method taking into account ``_direct_comm_call_action``"""
        if not self.is_in_controlled():
            action=self._direct_comm_call_action
            if action=="warning":
                if name not in self._command_warned:
                    print("Warning: direct call of command '{}' of thread '{}' from a different thread '{}'".format(
                            name,self.name,threadprop.current_controller().name),file=sys.stderr)
                    self._command_warned.add(name)
            else:
                accessor=getattr(self,action)
                return accessor.__getattr__(name)(*args,**kwargs)
        return original_method(*args,**kwargs)
    def _override_command_method(self, name):
        """Replace given method with the one that checks conflicts with the command names"""
        method=getattr(self,name,None)
        if method is not None:
            @func_utils.getargsfrom(method)
            def new_method(*args, **kwargs):
                return self._call_command_method(name,method,args,kwargs)
            setattr(self,name,new_method)

    ### Functions to be overloaded in subclasses ###
    def setup_task(self, *args, **kwargs):
        """
        Setup the thread (called before the main task loop).
        
        Local call method, called automatically.
        """
    def finalize_task(self):
        """
        Finalize the thread (always called on thread termination, regardless of the reason).
        
        Local call method, called automatically.
        """

    ### Status update function ###
    def update_status(self, kind, status, text=None, notify=True):
        """
        Update status represented in thread variables.

        `kind` is the status kind and `status` is its value.
        Status variable name is ``"status/"+kind``.
        If ``text is not None``, it specifies new status text stored in ``"status/"+kind+"_text"``.
        If ``notify==True``, send an multicast about the status change.
        Local call method.
        """
        status_str="status/"+kind if kind else "status"
        self.v[status_str]=status
        if notify:
            self.send_multicast("any",status_str,status)
        if text:
            self.set_variable(status_str+"_text",text)
            self.send_multicast("any",status_str+"_text",text)

    ### Command control ###
    
    def add_command(self, name, command=None, scheduler=None, limit_queue=None, on_full_queue="skip_current", priority=0):
        """
        Add a new command to the command set.

        Return scheduler, which can be used for adding another command (if the same queue should be used for several commands).
        Local call method.

        Args:
            name: command name
            command: command function; if ``None``, look for the method with the given `name`.
            scheduler: a command scheduler; by default, it is a :class:`.QQueueLengthLimitScheduler`,
                which maintains a call queue with the given length limit and full queue behavior;
                can also be a name of a different command, with which it will share a single queue with the same limitations;
                if supplied, `limit_queue` and `on_full_queue` parameters are ignored
            limit_queue: command call queue limit; ``None`` means no limit
            on_full_queue: action to be taken if the call can't be scheduled (the queue is full); can be
                ``"skip_current"`` (skip the call which is being scheduled),
                ``"skip_newest"`` (skip the most recent call; place the current)
                ``"skip_oldest"`` (skip the oldest call in the queue; place the current),
                ``"call_current"`` (execute the call which is being scheduled immediately in the caller thread),
                ``"call_newest"`` (execute the most recent call immediately in the caller thread), 
                ``"call_oldest"`` (execute the oldest call in the queue immediately in the caller thread), or
                ``"wait"`` (wait until the call can be scheduled, which is checked after every call removal from the queue; place the call)
            priority: command priority; higher-priority multicasts and commands are always executed before the lower-priority ones.
        """
        if name in self._commands:
            raise ValueError("command {} already exists".format(name))
        if command is None:
            command=getattr(self,name)
        psch=self._get_priority_queue(priority)
        if scheduler is None and limit_queue is not None:
            scheduler=callsync.QQueueLengthLimitScheduler(max_len=limit_queue or 0,on_full_queue=on_full_queue)
        elif isinstance(scheduler,py3.textstring):
            multischeduler=self._commands[scheduler].scheduler
            scheduler=multischeduler.schedulers[0]
        multischeduler=callsync.QMultiQueueScheduler([psch] if scheduler is None else [scheduler,psch],[self._command_poke])
        self._commands[name]=self.TCommand(command,multischeduler,priority)
        self._override_command_method(name)
        return scheduler
    def add_direct_call_command(self, name, command=None, error_on_async=True):
        """
        Add a direct method call which appears as a command.

        Unlike regular commands, the call is executed directly in the caller thread (i.e., it is identical to the direct method call).
        Useful for lightweight and/or lock-wrapped methods, which can be called in a thread-safe way, but which still use command interface for consistency.
        Note that this kind of commands doesn't have the same level of synchronization as regular commands
        (e.g., it can be executed during execution of another command, or commsync multicast method).
        Local call method.

        Args:
            name: command name
            command: command function; if ``None``, look for the method with the given `name`.
            error_on_async: if ``True`` and the command is called asynchronously, raise an error; otherwise, substitute for a synchronous call
        """
        if name in self._commands:
            raise ValueError("command {} already exists".format(name))
        if command is None:
            command=getattr(self,name)
        self._commands[name]=self.TCommand(command,"direct_sync" if error_on_async else "direct",None)

    def subscribe_commsync(self, callback, srcs="any", tags=None, dsts="any", filt=None, subscription_priority=0, scheduler=None, limit_queue=None, on_full_queue="skip_current", priority=0, add_call_info=False, return_result=False, sid=None):
        """
        Subscribe a callback to a multicast which is synchronized with commands and jobs execution.

        Unlike the standard :meth:`.QThreadController.subscribe_sync` method, the subscribed callback will only be executed between jobs or commands, not during one of these.
        Local call method.
        
        Args:
            callback: callback function, which takes 3 arguments: source, tag, and value.
            srcs(str or [str]): multicast source name or list of source names to filter the subscription;
                can be ``"any"`` (any source) or ``"all"`` (only multicasts specifically having ``"all"`` as a source).
            tags: multicast tag or list of tags to filter the subscription (any tag by default);
                can also contain Unix shell style pattern (``"*"`` matches everything, ``"?"`` matches one symbol, etc.)
            dsts(str or [str]): multicast destination name or list of destination names to filter the subscription;
                can be ``"any"`` (any destination) or ``"all"`` (only source specifically having ``"all"`` as a destination).
            filt(callable): additional filter function which takes 4 arguments: source, destination, tag, and value,
                and checks whether multicast passes the requirements.
            subscription_priority(int): subscription priority (higher priority subscribers are called first).
            scheduler: if defined, multicast call gets scheduled using this scheduler;
                by default, create a new call queue scheduler with the given `limit_queue`, `on_full_queue` and `add_call_info` arguments.
            limit_queue(int): limits the maximal number of scheduled calls
                (if the multicast is sent while at least `limit_queue` callbacks are already in queue to be executed, ignore it)
                0 or negative value means no limit (not recommended, as it can increase the queue indefinitely if the multicast rate is high enough)
            on_full_queue: action to be taken if the call can't be scheduled (the queue is full); can be
                ``"skip_current"`` (skip the call which is being scheduled),
                ``"skip_newest"`` (skip the most recent call; place the current)
                ``"skip_oldest"`` (skip the oldest call in the queue; place the current),
                ``"call_current"`` (execute the call which is being scheduled immediately in the caller thread),
                ``"call_newest"`` (execute the most recent call immediately in the caller thread), 
                ``"call_oldest"`` (execute the oldest call in the queue immediately in the caller thread), or
                ``"wait"`` (wait until the call can be scheduled, which is checked after every call removal from the queue; place the call)
            add_call_info(bool): if ``True``, add a fourth argument containing a call information (tuple with a single element, a timestamps of the call).
            return_result: if ``True``, use a result synchronizer to return the result of the subscribed call; otherwise, ignore the result
            sid(int): subscription ID (by default, generate a new unique id and return it).
        """
        if self._multicast_pool:
            psch=self._get_priority_queue(priority)
            if scheduler is None and (limit_queue is not None or add_call_info):
                scheduler=callsync.QQueueLengthLimitScheduler(max_len=limit_queue or 0,on_full_queue=on_full_queue,call_info_argname="call_info" if add_call_info else None)
            multischeduler=callsync.QMultiQueueScheduler([psch] if scheduler is None else [scheduler,psch],[self._command_poke])
            sid=self.subscribe_direct(callback,srcs=srcs,tags=tags,dsts=dsts or self.name,filt=filt,subscription_priority=subscription_priority,scheduler=multischeduler,return_result=return_result,sid=sid)
            return sid

    ##########  EXTERNAL CALLS  ##########
    ## Methods to be called by functions executing in other thread ##

    ### Request calls ###
    def _schedule_comm(self, name, args, kwargs, callback=None, sync_result=True):
        comm,sched,_=self._commands[name]
        call=sched.build_call(comm,args,kwargs,callback=callback,pass_result=True,callback_on_exception=False,sync_result=sync_result)
        sched.schedule(call)
        return call.result_synchronizer
    def call_command_direct(self, name, args=None, kwargs=None):
        """
        Invoke a command directly and immediately in the current thread.

        Universal call method.
        """
        self._check_running()
        comm=self._commands[name].command
        return comm(*(args or []),**(kwargs or {}))
    def call_command(self, name, args=None, kwargs=None, sync=False, callback=None, timeout=None, ignore_errors=False):
        """
        Invoke command call with the given name and arguments
        
        If `callback` is not ``None``, call it after the command is successfully executed (from the target thread), with a single parameter being the command result.
        If ``sync==True``, pause caller thread execution (for at most `timeout` seconds) until the command has been executed by the target thread, and then return the command result.
        If ``sync=="delayed"``, return :class:`.QCallResultSynchronizer` object which can be used to wait for and read the command result;
        otherwise, return ``None``.
        In the ``sync==True`` case, if ``ignore_errors==True``, ignore all possible problems with the call (controller stopped, call raised an exception, call was skipped)
        and return ``None`` instead; otherwise, these problems raise exceptions in the caller thread.
        Universal call method.
        """
        if not self._check_running(error=not ignore_errors):
            return
        sch=self._commands[name].scheduler
        if self.is_in_controlled() and sync!=False:
            sch="direct"
        if sch in ["direct","direct_sync"]:
            if sch=="direct_sync" and not sync:
                raise RuntimeError("direct call command {} can only be called synchronously".format(name))
            value=self.call_command_direct(name,args=args,kwargs=kwargs)
            if sync=="delayed":
                return callsync.QDirectResultSynchronizer(value)
            if sync:
                return value
            return None
        synchronizer=self._schedule_comm(name,args,kwargs,callback=callback,sync_result=bool(sync))
        if sync=="delayed":
            return synchronizer
        elif sync:
            return synchronizer.get_value_sync(timeout=timeout,error_on_fail=not ignore_errors,error_on_skip=not ignore_errors,pass_exception=not ignore_errors)
    def call_in_thread_commsync(self, func, args=None, kwargs=None, sync=True, timeout=None, priority=0, ignore_errors=False, same_thread_shortcut=True):
        """
        Call a function in this thread such that it is synchronous with other commands, and jobs.

        Mostly equivalent to calling a command, only the command function is supplied instead of its name, and the advanced scheduling
        (maximal schedule size, sharing with different commands, etc.) is not used.
        `args` and `kwargs` specify the function arguments.
        If ``sync==True``, pause caller thread execution (for at most `timeout` seconds) until the command has been executed by the target thread, and then return the command result.
        If ``sync=="delayed"``, return :class:`.QCallResultSynchronizer` object which can be used to wait for and read the command result;
        otherwise, return ``None``.
        `priority` sets the call priority (by default, the same as the standard commands).
        In the ``sync==True`` case, if ``ignore_errors==True``, ignore all possible problems with the call (controller stopped, call raised an exception, call was skipped)
        and return ``None`` instead; otherwise, these problems raise exceptions in the caller thread.
        If ``same_thread_shortcut==True`` (default) and the caller thread is the same as the controlled thread, call the function directly.
        Universal call method.
        """
        if not self._check_running(error=not ignore_errors):
            return
        if same_thread_shortcut and self.is_in_controlled():
            value=func(*(args or []),**(kwargs or {}))
            if sync=="delayed":
                return callsync.QDirectResultSynchronizer(value)
            if sync:
                return value
            return None
        sched=self._get_priority_queue(priority)
        call=sched.build_call(func,args,kwargs,pass_result=True,callback_on_exception=False,sync_result=bool(sync))
        sched.schedule(call)
        synchronizer=call.result_synchronizer
        if sync=="delayed":
            return synchronizer
        elif sync:
            return synchronizer.get_value_sync(timeout=timeout,error_on_fail=not ignore_errors,error_on_skip=not ignore_errors,pass_exception=not ignore_errors)
    def comm_paused(self):
        """Context manager, which allows to temporarily pause all calls (commands, jobs, etc.)"""
        return self._pause_lock

    class CommandAccess:
        """
        Accessor object designed to simplify command syntax.

        Automatically created by the thread, so doesn't need to be invoked externally.
        """
        def __init__(self, parent, sync, direct=False, timeout=None, safe=False, ignore_errors=False):
            self.parent=parent
            self.sync=sync
            self.direct=direct
            self.timeout=timeout
            self.safe=safe
            self.ignore_errors=ignore_errors
            self._calls={}
        def __getattr__(self, name):
            if name not in self._calls:
                parent=self.parent
                def remcall(*args, **kwargs):
                    if self.direct:
                        return self.call_command_direct(name,*args,**kwargs)
                    else:
                        return parent.call_command(name,args,kwargs,sync=self.sync,timeout=self.timeout,ignore_errors=self.ignore_errors)
                if self.safe:
                    remcall=exsafe(remcall)
                self._calls[name]=remcall
            return self._calls[name]











def _store_created_controller(controller):
    """
    Register a newly created controller.

    Called automatically on controller creation.
    """
    with _running_threads_lock:
        if _running_threads_stopping:
            raise threadprop.InterruptExceptionStop
        name=controller.name
        if (name in _running_threads) or (name in _created_threads):
            raise threadprop.DuplicateControllerThreadError("thread with name {} already exists".format(name))
        _created_threads[name]=controller
def _register_controller(controller):
    """
    Register a controller as running.

    Called automatically on thread start.
    """
    with _running_threads_lock:
        if _running_threads_stopping:
            raise threadprop.InterruptExceptionStop
        name=controller.name
        if name in _running_threads:
            raise threadprop.DuplicateControllerThreadError("thread with name {} already exists".format(name))
        if name not in _created_threads:
            raise threadprop.NoControllerThreadError("thread with name {} hasn't been created".format(name))
        _running_threads[name]=controller
        del _created_threads[name]
    _running_threads_notifier.notify()
def _unregister_controller(controller):
    """
    Remove a controller from the list of running controller.

    Called automatically from the controlled thread on its finish.
    """
    with _running_threads_lock:
        name=controller.name
        if name not in _running_threads:
            raise threadprop.NoControllerThreadError("thread with name {} doesn't exist".format(name))
        _stopped_threads.add(name)
        del _running_threads[name]
    _running_threads_notifier.notify()


def _find_controller_by_id(thread_id):
    """Get a running thread for a given thread ID, or ``None`` if no thread is found"""
    with _running_threads_lock:
        for t in _running_threads.values():
            if t.thread.thread_id==thread_id:
                return t
def get_controller(name=None, sync=True, timeout=None, sync_point=None):
    """
    Find a controller with a given name.

    If `name` is not supplied, yield current controller instead.
    If `name` is of ``int`` type, interpret it as a thread id.
    If the controller is not present and ``sync==True``, wait (with the given timeout) until the controller is running;
    otherwise, raise error if the controller is not running.
    If `sync_point` is not ``None``, synchronize to the thread `sync_point` point (by default, ``"run"``, i.e., after the setup is done) before returning.
    """
    if name is None:
        return threadprop.current_controller()
    def get_specified_controller():
        if isinstance(name,int):
            for ctl in _running_threads.values():
                if ctl.thread.thread_id==name:
                    return ctl
        if name in _stopped_threads:
            raise threadprop.NoControllerThreadError("thread {} is stopped".format(name))
        return _running_threads.get(name,None)
    with _running_threads_lock:
        ctl=get_specified_controller()
        if ctl is None and not sync:
            raise threadprop.NoControllerThreadError("thread {} doesn't exist".format(name))
        if ctl is not None and sync_point is None:
            return ctl
    def wait_cond():
        with _running_threads_lock:
            ctl=get_specified_controller()
            if ctl is not None:
                return ctl
    thread=_running_threads_notifier.wait_until(wait_cond,timeout=timeout)
    if sync_point is not None:
        thread.sync_exec_point(sync_point,timeout=timeout)
    return thread
def sync_controller(name, sync_point="run", timeout=None):
    """
    Find a controller with a given name and synchronize to the given point.

    If the controller is not present and ``sync==True``, wait (with the given timeout) until the controller is running;
    otherwise, raise error if the controller is not running.
    Analogous to ``get_controller(name, sync=True, timeout=timeout, sync_point=sync_point)``.
    """
    return get_controller(name,sync=True,timeout=timeout,sync_point=sync_point)
def get_gui_controller(sync=False, timeout=None, create_if_missing=True):
    """
    Get GUI thread controller.

    If the controller is not present and ``sync==True``, wait (with the given timeout) until the controller is running.
    If the controller is still not present and ``create_if_missing==True``, initialize the standard GUI controller.
    """
    try:
        gui_ctl=get_controller("gui",sync=sync,timeout=timeout)
    except threadprop.NoControllerThreadError:
        if create_if_missing:
            gui_ctl=QThreadController("gui",kind="main")
        else:
            raise
    return gui_ctl


def stop_controller(name=None, code=0, sync=True, require_controller=False):
    """
    Stop a controller with a given name (current controller by default).

    `code` specifies controller exit code (only applies to the main thread controller).
    If ``require_controller==True`` and the controller is not present, raise and error; otherwise, do nothing.
    If ``sync==True``, wait until the controller is stopped.
    """
    try:
        controller=get_controller(name,sync=False)
        controller.stop(code=code,sync=sync)
        return controller
    except threadprop.NoControllerThreadError:
        if require_controller:
            raise
def stop_all_controllers(sync=True, concurrent=True, stop_self=True):
    """
    Stop all running threads.

    If ``sync==True``, wait until the all of the controller are stopped.
    If ``sync==True`` and ``concurrent==True`` stop threads in concurrent manner (first issue stop messages to all of them, then wait until all are stopped).
    If ``sync==True`` and ``concurrent==False`` stop threads in consecutive manner (wait for each thread to stop before stopping the next one).
    If ``stop_self==True`` stop current thread after stopping all other threads.
    """
    global _running_threads_stopping  # pylint: disable=global-statement
    with _running_threads_lock:
        _running_threads_stopping=True
        names=list(_running_threads.keys())
    current_ctl=get_controller().name
    if concurrent and sync:
        ctls=[]
        for n in names:
            if n!=current_ctl:
                ctls.append(stop_controller(n,sync=False))
        for ctl in ctls:
            if ctl:
                ctl.sync_stop()
    else:
        for n in names:
            if (n!=current_ctl):
                stop_controller(n,sync=sync)
    if stop_self:
        stop_controller(current_ctl,sync=True)
def stop_app(code=0, sync=False):
    """
    Initialize stopping the application.
    
    Do this either by stopping the GUI controller (if it exists), or by stopping all controllers.
    If `sync` is ``True`` and the thread is not the main one, wait at this point until the process is stopped during the app shutdown;
    otherwise, the execution will continue as normal, and the thread will be stopped at a later time during the app shutdown.
    """
    try:
        get_gui_controller(create_if_missing=False).stop(code=code)
        if sync:
            try:
                get_controller(sync=False).sleep(timeout=None)
            except threadprop.NoControllerThreadError:
                pass
    except threadprop.NoControllerThreadError:
        stop_all_controllers(sync=False)
def restart_app(code=0, sync=False):
    """
    Restart the application.

    Equivalent to :func:`stop_app` followed by the scrip restart.
    If `sync` is ``True`` and the thread is not the main one, wait at this point until the process is stopped during the app shutdown;
    otherwise, the execution will continue as normal, and the thread will be stopped at a later time during the app shutdown.
    """
    global _restart_request  # pylint: disable=global-statement
    _restart_request=True
    stop_app(code,sync=sync)
def _check_restart():
    if _restart_request:
        threadprop.get_app().closeAllWindows()
        general.restart()
atexit.register(_check_restart)