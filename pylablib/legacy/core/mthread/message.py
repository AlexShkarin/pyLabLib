import threading
from . import threadprop, notifier
from ..utils import general, funcargparse, functions, py3

_depends_local=["..utils.general"]

       

class CallNotifier(notifier.ISkippableNotifier):
    """
    Wrapper for :class:`.notifier.ISkippableNotifier`, with external functions provided for ``_do_wait`` and ``_do_notify`` methods.

    Args:
        wait (callable): function to be called for waiting; if ``None``, nothing is called.
        notify (callable): function to be called for notifying; if ``None``, nothing is called.
        skippable (bool): if ``True``, allows for skippable wait events
            (if :meth:`.notifier.ISkippableNotifier.notify` is called before :meth:`.notifier.ISkippableNotifier.wait`, neither methods are actually called).
    """
    def __init__(self, wait=None, notify=None, skippable=False):
        notifier.ISkippableNotifier.__init__(self,skippable=skippable)
        self._wait=wait
        self._notify=notify
        
    def _do_wait(self, timeout=None):
        if self._wait:
            functions.call_cut_args(self._wait,timeout=timeout)
    def _do_notify(self):
        if self._notify:
            self._notify()


_sync_types={"message","wait","wait_event","none"}
_sync_nothread_substitutes={"message":"none","wait":"wait_event"}
def build_notifier(note_tag, note_value, sync, notification_controller):
    """
    Build a notifier object.

    `sync` can be:
        - a callable object, in which case it is called as a notifier (waiting is absent);
        - a tuple ``(note_tag, note_value)``, in which case it is interpreted as a ``"message"`` notifier with the corresponding tags (see below),
            while the `note_tag` and `note_value` arguments are ignored;
        - a string, in which case it determines a synchronization primitive type. Possible types are:
            - ``"none"``: 'dummy' synchronizer (no waiting, return immediately);
            - ``"wait_event"``: standard wait-notify pattern (`wait()` call waits until the `notify()` is called from a different thread).
                Waiting is implemented using the standard python `threading.Event` primitive (completely synchronous, can't be interrupted; should be used carefully);
            - ``"wait"``: standard wait-notify pattern (`wait()` call waits until the `notify()` is called from a different thread).
                Waiting is implemented using the thread message queue; (synchronous, but still responds to interrupts);
            - ``"message"``: send notifying message, but don't do any waiting (asynchronous)

            `note_tag` and `note_value` arguments are used for ``"wait"`` and ``"message"`` synchronizers
            
    `notification_controller` is a thread controller for the thread to be waiting/notified using this primitive.
    If it's a `no_thread_controller`, `sync` types are coerced: ``"wait"`` is interpreted as ``"wait_even"``, and ``"message"`` is interpreted as ``"none"``.
    """
    if isinstance(sync,tuple):
        note_tag,note_value=sync
        sync="message"
    if isinstance(sync,py3.textstring):
        funcargparse.check_parameter_range(sync,"sync_type",_sync_types)
        if notification_controller is threadprop.no_thread_controller:
            sync=_sync_nothread_substitutes.get(sync,sync)
        if sync in {"message","wait"}:
            if sync=="wait":
                def wait(timeout=None):
                    notification_controller.wait_for_message(note_tag,filt=lambda msg: msg.value==note_value,timeout=timeout,discard_on_timeout=True)
                skippable=True
            else:
                wait=None
                skippable=False
            notify=lambda: notification_controller.add_new_message(note_tag,note_value,schedule_sync="wait_event",receive_sync="none",on_broken="ignore")
            return CallNotifier(wait,notify,skippable=skippable)
        elif sync=="wait_event":
            evt=threading.Event()
            evt.clear()
            return CallNotifier(evt.wait,evt.set,skippable=True)
        else:
            return CallNotifier()
    elif hasattr(sync,"__call__"):
        return CallNotifier(None,sync,skippable=False)
    else:
        raise ValueError("unapplicable synchronizer: {}".format(sync))
            
            
class Message(object):
    """
    A message object.

    Args:
        tags (str): message tag (used for control in the message queue).
        value: message value (if appropriate).
        priority (int): message priority (standard is 0).
        sender: sender controller.
        schedule_sync (CallNotifier): object which is notified when the message is scheduled (``None`` means no notifier).
        receive_sync (CallNotifier): object which is notified when the message is received (``None`` means no notifier).
    """
    _uid_gen=general.UIDGenerator(thread_safe=True)
    def __init__(self, tag="", value=None, priority=0, sender=None, schedule_sync=None, receive_sync=None):
        object.__init__(self)
        self.tag=tag
        self.value=value
        self.priority=priority
        self.sender=sender
        self.schedule_sync=schedule_sync
        self.receive_sync=receive_sync
        self.uid=self._uid_gen()
    def scheduled(self):
        """
        Notify the message of being scheduled.

        Called internally by the message queue.
        """
        if self.schedule_sync:
            self.schedule_sync.notify()
    def received(self):
        """
        Notify the message of being received.

        Called internally by the message queue.
        """
        if self.receive_sync:
            self.receive_sync.notify()
    def sync(self):
        """
        Wait until this message is scheduled and received by the target thread.
        """
        if self.schedule_sync:
            self.schedule_sync.wait()
        if self.receive_sync:
            self.receive_sync.wait()
            
    def __repr__(self):
        return "Message({0}: {1})".format(self.tag,self.value)