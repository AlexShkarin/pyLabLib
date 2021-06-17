from ...core.utils import general, funcargparse
from ...core.thread import controller

import threading
import collections

from . import stream_message




class StreamIDCounter:
    """
    Counter which keeps track of the session and message IDs for incoming or generated messages.

    Args:
        use_mid: if ``False``, do not use ``mid`` counter and always return ``mid=None``
        sid_ooo: behavior if supplied session ID in :meth:`next_session` or :meth:`update` is out of order (lower than the current count);
            can be ``"ignore"`` (keep the current counter value), ``"set"`` (set the value to the new smaller one), or ``"error"`` (raise an exception)
        mid_ooo: behavior if supplied message ID in :meth:`next_message` or :meth:`update` is out of order (lower than the current count);
            can be ``"ignore"`` (keep the current counter value), ``"set"`` (set the value to the new smaller one), or ``"error"`` (raise an exception)
    """
    def __init__(self, use_mid=True, sid_ooo="ignore", mid_ooo="ignore"):
        funcargparse.check_parameter_range(sid_ooo,"sid_ooo",["ignore","set","error"])
        funcargparse.check_parameter_range(mid_ooo,"mid_ooo",["ignore","set","error"])
        self.sid_gen=general.UIDGenerator()
        self.sid=self.sid_gen()
        self.use_mid=use_mid
        self.mid_gen=general.UIDGenerator() if self.use_mid else lambda: None
        self.mid=self.mid_gen()
        self.sid_ooo=sid_ooo
        self.mid_ooo=mid_ooo
        self.cutoff=(0,0)
    
    def update_session(self, sid):
        """
        Update the session counter.

        If `sid` is ``None``, keep the counter the same. If `sid` is ``"next"``, advance the current counter.
        If the session ID value was increased, reset the message ID counter.
        Return the new session ID.
        """
        if sid is None:
            return self.sid
        if sid=="next":
            return self.next_session()
        csid=self.sid
        if sid>=csid:
            self.sid_gen.reset(sid)
        elif self.sid_ooo=="set":
            self.sid_gen.reset(sid)
        elif self.sid_ooo=="error":
            raise ValueError("next session id {} is before the current id {}".format(sid,self.sid))
        self.sid=self.sid_gen()
        if self.sid>csid:
            self.mid_gen=general.UIDGenerator() if self.use_mid else lambda: None
            self.mid=self.mid_gen()
        return self.sid
    def next_session(self):
        """Mark the start of the next session and reset message ID counter"""
        self.sid=self.sid_gen()
        self.mid_gen=general.UIDGenerator() if self.use_mid else lambda: None
        self.mid=self.mid_gen()
        return self.sid
    def update_message(self, mid):
        """
        Update the message counter.

        If `mid` is ``None``, keep the counter the same. If `mid` is ``"next"``, advance the current counter.
        Return the new message ID.
        """
        if mid is None or not self.use_mid:
            return self.mid
        if mid=="next":
            return self.next_message()
        if mid>=self.mid:
            self.mid_gen.reset(mid)
        elif self.mid_ooo=="set":
            self.mid_gen.reset(mid)
        elif self.mid_ooo=="error":
            raise ValueError("next message id {} is before the current id {}".format(mid,self.mid))
        self.mid=self.mid_gen()
        return self.mid
    def next_message(self):
        """Mark the next message"""
        self.mid=self.mid_gen()
        return self.mid
    def update(self, sid=None, mid=None):
        """
        Update counters to the ones supplied.

        Return ``True`` if the session ID was incremented as a result.
        """
        csid=self.sid
        self.update_session(sid)
        self.update_message(mid)
        return self.sid>csid
    def receive_message(self, msg, sn=None):
        """
        Update counters to the ones stored in the message.

        `sn` specifies the stream name within the message.
        Return ``True`` if the session ID was incremented as a result.
        """
        return self.update(*msg.get_ids(sn))
    def get_ids(self):
        """Get stored IDs as a tuple ``(sid, mid)``"""
        return self.sid,self.mid
    def set_cutoff(self, sid=None, mid=0):
        """
        Set the ID cutoff.

        Used in conjunction with :meth:`check_cutoff` to check if session and message IDs are above the cutoff.
        A value of ``None`` keeps the current value.
        Since IDs are normally non-negative, setting `sid` and `mid` to 0 effectively removes the cutoff.
        Return the updated cutoff value.
        """
        csid,cmid=self.cutoff
        self.cutoff=(csid if sid is None else sid),(cmid if mid is None else mid)
        return self.cutoff
    def check_cutoff(self, sid=None, mid=None):
        """
        Check if the supplied IDs pass the cutoff (i.e., above or equal to it).

        Values of ``None`` are not checked, i.e., assumed to always pass.
        """
        if sid is not None and sid<self.cutoff[0]:
            return False
        if mid is not None and mid<self.cutoff[1]:
            return False
        return True

class MultiStreamIDCounter:
    """
    Combination of several counters for different streams.
    """
    def __init__(self):
        self.cnts={}
    def add_counter(self, sn, use_mid=True, sid_ooo="ignore", mid_ooo="ignore"):
        """
        Add a single counter associated with the given stream name `sn`.

        Args:
            use_mid: if ``False``, do not use ``mid`` counter and always return ``mid=None``
            sid_ooo: behavior if supplied session ID in :meth:`next_session` or :meth:`update` is out of order (lower than the current count);
                can be ``"ignore"`` (keep the current counter value), ``"set"`` (set the value to the new smaller one), or ``"error"`` (raise an exception)
            mid_ooo: behavior if supplied message ID in :meth:`next_message` or :meth:`update` is out of order (lower than the current count);
                can be ``"ignore"`` (keep the current counter value), ``"set"`` (set the value to the new smaller one), or ``"error"`` (raise an exception)
        """
        self.cnts[sn]=StreamIDCounter(use_mid=use_mid,sid_ooo=sid_ooo,mid_ooo=mid_ooo)
    def update_session(self, sn, sid):
        """
        Update the session counter for the given stream name.

        If `sid` is ``None``, keep the counter the same. If `sid` is ``"next"``, advance the current counter.
        If the session ID value was increased, reset the message ID counter.
        Return the new session ID.
        """
        return self.cnts[sn].update_session(sid)
    def next_session(self, sn):
        """Mark the start of the next session and reset message ID counter for the given stream name"""
        return self.cnts[sn].next_session()
    def update_message(self, sn, mid):
        """
        Update the message counter for the given stream name.

        If `mid` is ``None``, keep the counter the same. If `mid` is ``"next"``, advance the current counter.
        Return the new message ID.
        """
        return self.cnts[sn].update_message(mid)
    def next_message(self, sn):
        """Mark the next messagefor the given stream name"""
        return self.cnts[sn].next_message()
    def receive_message(self, msg, sn=None):
        """
        Update all stored IDs according to the given message.

        If `sn` is ``None`` or ``"all"``, update all stored counters for all the session in the message.
        Otherwise, update only the IDs specified by `sn` (can be a single name or a list of names).
        """
        if sn not in [None,"all"]:
            if not isinstance(sn,list):
                sn=[sn]
            new_sid=False
            for n in sn:
                new_sid=new_sid or self.cnts[n].receive_message(msg,sn=n)
            return new_sid
        sid,mid=msg.get_ids("all")
        if isinstance(sid,dict):
            new_sid=False
            for n,s in sid.items():
                if n in self.cnts:
                    m=None if mid is None else mid[n]
                    new_sid=new_sid or self.cnts[n].update(s,m)
            return new_sid
        raise ValueError("name should be provided for anonymous stream messages")
    def get_ids(self, sn=None):
        """
        Get stored IDs.
        
        If `sn` is ``None`` or ``"all"``, return a tuple of dictionaries ``({sn:sid}, {sn:mid})`` with all IDs;
        otherwise, a tuple ``(sid, mid)`` for the given `sn`
        """
        if sn is None or sn=="all":
            ids={n:c.get_ids() for n,c in self.cnts.items()}
            return {n:i[0] for n,i in ids.items()},{n:i[1] for n,i in ids.items()}
        return self.cnts[sn].get_ids()
    def set_cutoff(self, sn, sid=None, mid=0):
        """
        Set the ID cutoff for a stream with the given name.

        Used in conjunction with :meth:`check_cutoff` to check if session and message IDs are above the cutoff.
        A value of ``None`` keeps the current value.
        Since IDs are normally non-negative, setting `sid` and `mid` to 0 effectively removes the cutoff.
        Return the updated cutoff value.
        """
        return self.cnts[sn].set_cutoff(sid,mid)
    def check_cutoff(self, msg, sn=None):
        """
        Check if the IDs in the supplied message pass all the cutoffs.

        If `sn` is ``None`` or ``"all"``, check cutoffs of all appropriate counters;
        otherwise, check only cutoffs specified by `sn` (can be a single name or a list of names).
        """
        if sn not in [None,"all"]:
            if not isinstance(sn,list):
                sn=[sn]
            for n in sn:
                if not self.cnts[n].check_cutoff(*msg.get_ids(n)):
                    return False
            return True
        sid,mid=msg.get_ids("all")
        if isinstance(sid,dict):
            for n,s in sid.items():
                if n in self.cnts:
                    m=None if mid is None else mid[n]
                    if not self.cnts[n].check_cutoff(s,m):
                        return False
            return True
        raise ValueError("name should be provided for anonymous stream messages")




class StreamSource:
    """
    Data stream source.

    Keeps track of the message and session IDs, and creates new messages using the builder method.

    Args:
        builder: method to build the message (should take ``mid`` and ``sid`` as two keyword arguments)
            by default, use :class:`.GenericDataStreamMessage`
        use_mid: if ``True``, keep track of message ID as well as session ID; otherwise, set message ID to ``None``
    """
    def __init__(self, builder=None, use_mid=True, sn=None):
        self.builder=stream_message.GenericDataStreamMessage if builder is None else builder
        self.cnt=StreamIDCounter(use_mid=use_mid)
        self.sn=sn

    def get_ids(self, as_dict=False):
        """Get current ID counter values either as a tuple, or a dictionary"""
        sid,mid=self.cnt.sid,self.cnt.mid
        if as_dict:
            return {"sid":sid,"mid":mid}
        return sid,mid
    def next_session(self):
        """
        Mark the start of the next session.

        If the session ID value was changed, reset the message ID counter.
        Return the new session ID.
        """
        return self.cnt.next_session()
    def next_message(self):
        """
        Mark sending of the next message.

        Return the new message ID.
        """
        return self.cnt.next_message()
    def build_message(self, *args, **kwargs):
        """
        Create a new message with the given arguments.
        
        Arguments are passed to the builder, along with the values of the session and message IDs.
        """
        kwargs.update(self.get_ids(as_dict=True))
        kwargs.setdefault("sn",self.sn)
        msg=self.builder(*args,**kwargs)
        self.next_message()
        return msg
    def receive_message(self, msg, sn=None):
        """
        Update counters to the ones stored in the message.

        `sn` specifies the stream name within the message.
        Return ``True`` if the session ID was incremented as a result.
        """
        return self.cnt.receive_message(msg,sn=sn)







class IStreamReceiver:
    """
    Generic data stream receiver.

    Can be subscribed to a data source multicast.
    Calls :meth:`recv_message` method (overloaded in subclasses) whenever a new stream message arrives.
    """
    _sid_gen=general.NamedUIDGenerator(thread_safe=True)
    def __init__(self, ctl=None):
        self.ctl=ctl or controller.get_controller()
        self.subid=None
        self.lock=threading.Lock()
    
    def recv_message(self, src, tag, msg):
        """Process the reception of the new message"""
    def subscribe(self, srcs, tags, dsts=None, filt=None):
        """Subscribe to the data stream with the given source, tag, destination, and filter function"""
        if self.subid is not None:
            raise ValueError("stream is already subscribed")
        subid=self._sid_gen("stream_receiver")
        def func(src, tag, msg):
            if self.subid is subid:
                with self.lock:
                    self.recv_message(src,tag,msg)
        self.ctl.subscribe_direct(func,srcs=srcs,tags=tags,dsts=dsts,filt=filt,sid=subid)
        self.subid=subid
        return subid
    def unsubscribe(self):
        """Unsubscribe from the data stream"""
        if self.subid is None:
            raise KeyError("stream is not subscribed")
        self.ctl.unsubscribe()
        self.subid=None




TStreamEvent=collections.namedtuple("TStreamEvent",["src","tag","msg","ids"])
class AccumulatorStreamReceiver(IStreamReceiver):
    """
    Accumulator data stream receiver.

    Automatically accumulates all received stream messages in a list, which can be subsequently read out.
    Also has methods to wait for new messages (or for a message with specific session or message ID),
    and for ignoring messages with IDs below a threshold (useful to reject messages from "old" streams, which have been stopped).

    Args:
        ctl: thread controller which manages subscription and waiting (by default, the current controller)
        sn: specifies stream name for the incoming stream messages; used for counting IDs and applying cutoff
        paused: if ``True``, the receiver strats paused, and needs to be started using :meth:`pause` method with `
        only_valid: 
        only_ids: if ``True``, any messages which do not support IDs (i.e., do not have ``get_ids`` method) are ignored;
            otherwise, they are still placed in the queue with automatically generated session and message IDs (increment the message ID of the previous message by 1).
    """
    def __init__(self, ctl=None, sn=None, paused=False, only_valid=True):
        super().__init__(ctl)
        self.reset()
        self.sn=sn
        self.only_valid=only_valid
        self.cutoff_ids=(0,0)
        self.paused=paused
        self.waiting=False
        self.cnt=StreamIDCounter()

    def reset(self):
        """Reset the message queue"""
        with self.lock:
            self.last_read=None
            self.last_wait=None
            self.last_recv=None
            self.last_evt=None
            self.acc=[]
    def pause(self, paused=True, reset=True):
        """
        Pause or resume the receiver.

        While paused, all the received messages will be ignored.
        If ``reset==True``, reset the queue on un-pausing.
        """
        reset=reset and self.paused and not paused
        if reset:
            self.reset()
        self.paused=paused
    def resume(self, reset=True):
        """
        Resume the receiver operation after the pause.

        If ``reset==True`` and the receiver is currently paused, reset the queue.
        Analogouse to ``self.pause(paused=False)``
        """
        self.pause(paused=False,reset=reset)

    def current_ids(self):
        """Get the current IDs (the last received message IDs)"""
        return self.cnt.sid,self.cnt.mid
    def set_cutoff(self, sid=None, mid=0):
        """
        Set cutoffs for session and message IDs.

        Any arriving messages with IDs below the cutoff will be ignored,
        and such messages currently in the queue are removed.
        If `sid` or `mid` are ``None``, it implies no threshold.
        """
        cutoff=self.cnt.set_cutoff(sid,mid)
        with self.lock:
            ncut=len(self.acc)
            for i,evt in enumerate(self.acc):
                if evt.ids>=cutoff:
                    ncut=i
                    break
            del self.acc[:ncut]
            if self.last_read is not None and self.last_read<cutoff:
                self.last_read=self.acc[0].ids if self.acc else None
            if self.last_wait is not None and self.last_wait<cutoff:
                self.last_wait=None
            if self.last_recv is not None and self.last_recv<cutoff:
                self.last_recv=None
        return cutoff

    def recv_message(self, src, tag, msg):
        if self.paused:
            return
        try:
            sid,mid=msg.get_ids(self.sn)
        except (AttributeError,KeyError):
            if self.only_valid:
                return
            sid,mid=None,None
        if sid is None:
            sid=self.cnt.next_session()
            mid=None
        else:
            self.cnt.update_session(sid)
        if mid is None:
            mid=self.cnt.next_message()
        else:
            self.cnt.update_message(mid)
        if not self.cnt.check_cutoff(sid,mid):
            return
        self.last_recv=self.cnt.get_ids()
        self.acc.append(TStreamEvent(src,tag,msg,(sid,mid)))
        if self.waiting:
            self.ctl.poke()

    def __len__(self):
        return len(self.acc)
    def _normalize_since(self, since):
        if since=="lastread":
            return self.last_read
        if since=="lastwait":
            return self.last_wait
        if since=="now":
            return self.last_recv
        return since
    def get_checker(self, since="lastread", cond=None):
        since=self._normalize_since(since)
        self.last_evt=None
        def check():
            if not self.acc:
                return False
            evt=self.acc[-1]
            if evt is self.last_evt:
                return False
            self.last_evt=evt
            if since is not None and evt.ids<=since:
                return False
            if cond is not None and not cond(*evt):
                return False
            return True
        return check
    def wait(self, since="lastread", cond=None, timeout=None):
        """
        Wait for a new message satisfying a specific condition.

        `since` can be ``"lastread"`` (wait until a new unread message is present),
        ``"lastwait"`` (wait until a new message since the last time this method was called),
        ``"now"`` (wait for a new message since the current moment in time),
        or a tuple ``(sid, mid)`` (wait for a new message with the IDs larger than the given IDs).
        """
        since=self._normalize_since(since)
        with self.lock:
            if self.last_recv is not None and (since is None or self.last_recv>since):
                if cond is not None:
                    for evt in self.acc[::-1]:
                        if evt.ids<=since:
                            break
                        if cond(*evt):
                            do_wait=False
                            self.last_evt=evt
                            break
                else:
                    do_wait=False
                    self.last_evt=self.acc[-1]
            else:
                do_wait=True
                self.waiting=True
        try:
            if do_wait:
                check=self.get_checker(since=since,cond=cond)
                self.ctl.wait_until(check,timeout=timeout)
        finally:
            self.waiting=False
        self.last_wait=self.last_evt.ids
        return self.last_evt
    def _get_acc_rng(self, i0, i1, peek, as_event):
        if i1 is not None and i1<=i0 or not self.acc:
            return []
        with self.lock:
            if i1 is None:
                i1=len(self.acc)
            evts=self.acc[i0:i1]
            if not peek:
                del self.acc[:i1]
                self.last_read=evts[-1].ids
        return evts if as_event else [evt.msg for evt in evts]
    def get_oldest(self, n=1, peek=False, as_event=False):
        """
        Get the oldest `n` messages from the accumulator queue.

        If `n` is ``None``, return all messages.
        If there are less than `n` message in the queue, return all of them.
        If ``peek==True``, just return the messages; otherwise, pop the from the queue in mark the as read.
        If ``as_event==True``, each message is represented as a tuple ``(src, tag, msg, ids)`` describing the received event;
        otherwise, just messages are returned.
        """
        return self._get_acc_rng(0,n,peek=peek,as_event=as_event)
    def get_newest(self, n=1, peek=True, as_event=False):
        """
        Get the newest `n` messages from the accumulator queue.

        If there are less than `n` message in the queue, return all of them.
        If ``peek==True``, just return the messages; otherwise, clear the queue after reading.
        If ``as_event==True``, each message is represented as a tuple ``(src, tag, msg, ids)`` describing the received event;
        otherwise, just messages are returned.
        """
        if n<=0:
            return []
        return self._get_acc_rng(-n,-1,peek=peek,as_event=as_event)