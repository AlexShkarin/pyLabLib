from . import tag_queue, message, threadprop
from ..utils import general


class MessageQueue(object):
    """
    Mostly a wrapper around :class:`.tag_queue.TaggedQueue`, with several routines specifically for dealing with messages.

    Args:
        owner: owner thread controller.
    """
    def __init__(self, owner):
        object.__init__(self)
        self.queue=tag_queue.TaggedQueue()
        self.owner=owner
        
    def limit_length(self, tag, length):
        """
        Set length limit for a given tag.
        """
        self.queue.limit_length(tag,length)
    
    _message_sync_tag="sync.message"
    @staticmethod
    def build_notifier(uid, sync, event_type, notification_controller):
        """
        Create a notifier for a message with an ID `uid`.

        If `sync` is a tuple ``(tag, value)``, it specifies the notifier message parameters (see :func:`.message.build_notifier`).
        Otherwise, they are determined by the `uid`.

        Called from the sender thread.
        """
        if isinstance(sync,tuple):
            tag,value=sync
        else:
            tag="{0}.{1}".format(MessageQueue._message_sync_tag,event_type)
            value=uid
        return message.build_notifier(tag,value,sync,notification_controller)
    
    # Adding messages
    @staticmethod
    def build_message(tag, value=None, priority=0, schedule_sync="wait", receive_sync="none", sender=None):
        """
        Create a message.

        `tag` and `value` determine the message contents, `priority` is its priority for scheduling.
        `schedule_sync` and `receive_sync` specify synchronizers for scheduling and receiving this message (see :func:`.message.build_notifier`).
        `sender` is the sender thread controller (current controller by default).

        Called from a sender thread.
        """
        sender=sender or threadprop.current_controller()
        msg=message.Message(tag,value,priority=priority,sender=sender)
        msg.schedule_sync=MessageQueue.build_notifier(msg.uid,schedule_sync,"schedule",sender)
        msg.receive_sync=MessageQueue.build_notifier(msg.uid,receive_sync,"receive",sender)
        return msg
    def add_message(self, msg, sync=True):
        """
        Add the message to the queue.

        If `sync` is ``True``, do the synchronization (wait for receiving and scheduling) after sending the message.

        Called from a sender thread.
        """
        self.queue.put(msg)
        if sync:
            msg.sync()
        return msg
        
    # Receiving messages
    def _read_process_loop(self, filt, interrupt_check, timeout, discard_on_timeout=False, discard_filt=None):
        countdown=general.Countdown(timeout)
        while True:
            msg=self.queue.get(filt,timeout=countdown.time_left(),discard_on_timeout=discard_on_timeout,discard_filt=discard_filt)
            if msg is not None:
                if not interrupt_check(msg):
                    return msg
            else:
                return None
    def exhaust_messages(self, filt, interrupt_check):
        """
        Read and return (instantaneously) all available messages which satisfy the filter `filt`.

        `interrupt_check` is an interrupt filter function, which pre-processes the message and return ``True`` if it was an interrupt
        (in which case it's omitted in the output).

        Called from the receiver thread.
        """
        recv_msg=[]
        while True:
            new_msg=self._read_process_loop(filt,interrupt_check,0)
            if new_msg is None:
                return recv_msg
            else:
                recv_msg.append(new_msg)
        return recv_msg
    def wait_for_message(self, filt, interrupt_check, timeout=None, exhaust=False, discard_on_timeout=False, discard_filt=None):
        """
        Wait for a message satisfying the filter `filt`.

        `interrupt_check` is an interrupt filter function, which pre-processes the message and return ``True`` if it was an interrupt
        (in which case the waiting continues). 
        if `exhaust` is ``True``, returns list of all messages satisfying `filt`, if several of them are available immediately.
        if `discard_on_timeout` is ``True`` and the wait timed out, mark the message for discarding using `discard_filt` (see :meth:`.tag_queue.TaggedQueue.get`).

        Called from the receiver thread.
        """
        if exhaust:
            msg=self.exhaust_messages(filt,interrupt_check)
            if len(msg)>0:
                return msg
        msg=self._read_process_loop(filt,interrupt_check,timeout,discard_on_timeout=discard_on_timeout,discard_filt=discard_filt)
        if exhaust:
            return [] if msg is None else [msg]
        else:
            return msg
        
    # Clearing
    def clear(self, notify_all=True, ignore_exceptions=True, mark_broken=True):
        """
        Clear the queue.

        See :meth:`.tag_queue.TaggedQueue.clear`
        """
        self.queue.clear(notify_all,ignore_exceptions,mark_broken)
    def broken(self):
        """
        Check if the queue is broken.

        See :meth:`.tag_queue.TaggedQueue.broken`
        """
        return self.queue.broken()
    def fix(self):
        """
        Fix broken queue.

        See :meth:`.tag_queue.TaggedQueue.fix`
        """
        return self.queue.fix()
    
    
    
### Send message to a thread ###
def send_message(dest, tag, value=None, priority=0, schedule_sync="wait", receive_sync="none", sync=True, on_broken="error"):
    """
    Send a message to the thread `dest` from the current thread.

    See :meth:`MessageQueue.add_message`.
    """
    try:
        dest=threadprop.as_controller(dest)
        return dest.send_message(tag,value,priority,schedule_sync,receive_sync,sync=sync,on_broken=on_broken)
    except threadprop.NoControllerThreadError as e:
        return threadprop.on_error(on_broken,e)


### Receive messages (only for threads with controllers) ###
def exhaust_messages(tags=None, filt=None):
    """
    Exhaust messages for the current thread.

    See :meth:`MessageQueue.exhaust_messages`.
    """
    return threadprop.current_controller(True).exhaust_messages(tags=tags,filt=filt)
def wait_for_message(tags=None, timeout=None, filt=None, exhaust=False, discard_on_timeout=False):
    """
    Wait for a message for the current thread.

    See :meth:`MessageQueue.wait_for_message`.
    """
    return threadprop.current_controller(True).wait_for_message(tags=tags,timeout=timeout,filt=filt,exhaust=exhaust,discard_on_timeout=discard_on_timeout)