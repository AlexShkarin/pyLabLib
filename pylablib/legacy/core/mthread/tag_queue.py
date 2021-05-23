"""
Tagged queue with priority and size limitation (set tag-wise).
"""

import threading
from ..utils import general


class BrokenQueueError(RuntimeError):
    """
    An error signalizing that the queue is in a broken (shut down) state.
    """
    def __init__(self, msg=None):
        msg=msg or "access to a broken TaggedQueue"
        RuntimeError.__init__(self,msg)
class TaggedQueue(object):
    """
    Tagged queue with priority and size limitation (set tag-wise).

    Supports multi-thread adding, but only single-thread extracting (receiving function is completely synchronous).
    Item is assumed to have ``tag`` and ``priority`` properties, and ``scheduled()`` and ``received()`` methods (callbacks).

    Extraction and discarding is based on filter functions. These should be as simple as possible and have short determined runtime (no synchronization or locks) to prevent deadlocks.
    When item is scheduled (i.e., added and passes length limitation), ``item.scheduled()`` method is called;
    when item is extracted, ``item.received()`` method is called;
    under various circumstances, both of these methods may be called in either adding thread, or extracting thread.
    It is guaranteed that ``scheduled()`` is called before ``received()``, and both methods are called eventually if the message is ever extracted or discarded.
    """
    def __init__(self):
        object.__init__(self)
        self._queue=[]
        self._unscheduled={}
        self._lengths={}
        self._lock=threading.Lock()
        self._broken_lock=threading.Lock()
        self._getting_lock=threading.RLock()
        self._new_item_event=threading.Event()
        self._to_discard=[]
        self._broken_put=False
        self._broken_get=False
        
    def limit_length(self, tag, length):
        """
        Set length limit for a given tag.
        """
        self._lengths[tag]=length
        
    @staticmethod
    def _find_max_priority_idx(queue):
        max_idx=0
        max_priority=queue[max_idx].priority
        for i in range(1,len(queue)):
            if queue[i].priority>max_priority:
                max_idx=i
                max_priority=queue[i].priority
        return max_idx
    
    def _check_discarding(self, item):
        for i,filt in enumerate(self._to_discard):
            if filt(item):
                self._to_discard.pop(i)
                return True
        return False
    
    def _schedule_item(self, item, check_discarding=True):
        tag=item.tag
        if self._lengths.get(tag,0)>0:
            cnt=len([m for m in self._queue if m.tag==tag])
            if cnt>=self._lengths[tag]:
                self._unscheduled.setdefault(tag,[]).append(item)
                return "unscheduled"
        if check_discarding and self._check_discarding(item):
            return "discarded"
        else:
            self._queue.append(item)
            return "scheduled"
    def _check_unscheduled(self, tag):
        discarded=[]
        while len(self._unscheduled.get(tag,[]))>0:
            unscheduled=self._unscheduled[tag]
            new_msg_idx=self._find_max_priority_idx(unscheduled)
            item=unscheduled.pop(new_msg_idx)
            if self._check_discarding(item):
                discarded.append(item)
            else:
                return item,discarded
        return None,discarded
        
    def _find_item(self, filt, start=0):
        found=[(i+start,item) for (i,item) in enumerate(self._queue[start:]) if filt(item)]
        if not found:
            return None
        found_idx,found_items=zip(*found)
        idx=self._find_max_priority_idx(found_items)
        return self._queue.pop(found_idx[idx])
    def _wait_for_item(self, filt, timeout=None, discard_on_timeout=False, discard_filt=None):
        start=0
        countdown=general.Countdown(timeout)
        while True:
            with self._lock:
                if self._broken_get:
                    raise BrokenQueueError()
                item=self._find_item(filt,start)
                if item is not None:
                    new_scheduled,discarded=self._check_unscheduled(item.tag)
                    if new_scheduled is not None:
                        if self._schedule_item(new_scheduled,check_discarding=False)!="scheduled":
                            new_scheduled=None
                    return item,(new_scheduled,discarded)
                start=len(self._queue)
                self._new_item_event.clear()
                if countdown.passed():
                    if discard_on_timeout:
                        discard_filt=discard_filt or filt
                        self._to_discard.append(discard_filt)
                    return None,(None,[])
            self._new_item_event.wait(countdown.time_left())
    
    def put(self, item):
        """
        Put an item in the queue.

        This function doesn't perform synchronization waits as long as ``scheduled()`` and ``received()`` methods of `item` don't perfrom them.
        """
        with self._lock:
            if self._broken_put:
                raise BrokenQueueError()
            res=self._schedule_item(item)
            if res=="scheduled":
                self._new_item_event.set()
        if res in {"scheduled","discarded"}:
            item.scheduled()
        if res=="discarded":
            item.received()
        return res
            
    def get(self, filt=None, timeout=None, discard_on_timeout=False, discard_filt=None):
        """
        Extract an item from the queue which satisfies `filt` filter function.

        If `timeout` is not ``None``, it determines the wait time. If it is passed before an item has been acquired, the return ``None``.
        If `discard_on_timeout` is ``True`` and `timeout` is passed, marks `discard_filt` (same as `filt` by default) for discarding;
        this means that the next time a single message satisfying `discard_filt` is scheduled (either directly during :meth:`put`, or from scheduling queue during :meth:`get`),
        it is silently 'received' (notified of scheduling and receiving, but never explicitly passed to the destination thread).
        """
        if filt is None:
            filt=lambda _: True
        with self._getting_lock:
            item,(new_scheduled,discarded)=self._wait_for_item(filt,timeout=timeout,discard_on_timeout=discard_on_timeout,discard_filt=discard_filt)
            if new_scheduled:
                new_scheduled.scheduled()
            if item is not None:
                item.received()
            for d_item in discarded:
                d_item.scheduled()
                d_item.received()
        return item
    @staticmethod
    def _del_item_from_list(item, lst):
        for n,i in enumerate(lst):
            if i is item:
                del lst[n]
                return True
        return False
    def remove(self, item, only_unscheduled=False):
        """
        Remove the item if it is in the queue without calling its ``scheduled`` or ``received`` methods.

        Return ``True`` if removal is successful, and ``False`` otherwise.
        If ``only_unscheduled==True``, only remove item if it hasn't been scheduled yet.
        """
        res=None
        if only_unscheduled:
            with self._lock:
                if self._broken_get:
                    raise BrokenQueueError()
                if self._del_item_from_list(item,self._unscheduled[item.tag]):
                    res="unscheduled"
        else:
            with self._getting_lock:
                with self._lock:
                    if self._broken_get:
                        raise BrokenQueueError()
                    if self._del_item_from_list(item,self._queue):
                        res="scheduled"
                    elif self._del_item_from_list(item,self._unscheduled[item.tag]):
                        res="unscheduled"
        if res=="unscheduled":
            item.scheduled()
            item.received()
        elif res=="scheduled":
            item.received()
        return (res is not None)
    def clear(self, notify_all=True, ignore_exceptions=True, mark_broken=True):
        """
        Clear the queue.

        If ``notify_all==True``, behave as if all the messages are received or discarded; otherwise, just remove them silently (equivalent to :meth:`remove` method).
        If ``ignore_exceptions==True``, ignore exceptions on scheduling and receiving (e.g., if the notified thread is stopped); the queue is cleaned regardless.
        If ``mark_broken==True``, mark the queue as broken (any subsequent calls to its methods raise :exc:`BrokenQueueError`).
        """
        with self._broken_lock:
            if notify_all:
                if mark_broken:
                    with self._lock:
                        self._broken_put=True
                try:
                    while True:
                        try:
                            if self.get(timeout=0) is None:
                                return
                        except RuntimeError:
                            if not ignore_exceptions:
                                raise
                finally:
                    self._queue=[]
                    self._unscheduled={}
                    self._to_discard=[]
                    if mark_broken:
                        with self._lock:
                            self._broken_get=True
                            self._new_item_event.set()
            else:
                with self._lock:
                    self._queue=[]
                    self._unscheduled={}
                    self._to_discard=[]
                    self._new_item_event.set()
                    self._broken_get=self._broken_get and mark_broken
                    self._broken_put=self._broken_put and mark_broken
    def broken(self):
        """
        Check if the queue is broken.
        """
        with self._broken_lock:
            return self._broken_get and self._broken_put
    def fix(self):
        """
        Fix broken queue.
        
        Should be used carefully, since it can introduce problems with outside logic that relies on a broken queue staying broken.
        """
        with self._broken_lock:
            self._broken_get=False
            self._broken_put=False
                
                


def _tag_match_p(tags, tag_separator=None):
    if tag_separator is None:
        def filt(item):
            for t in tags:
                if item.tag.startswith(t):
                    return True
            return False
    else:
        def filt(item):
            for t in tags:
                if (item.tag==t) or (item.tag.startswith(t+tag_separator)):
                    return True
            return False
    return filt
def build_filter(tags=None, filt=None, uncond_tags=None, tag_separator=None):
    """
    Build a filter function.

    Args:
        tags ([str]): list of prefixes that match message tags.
        filt (callable): an additional filter function which needs to be satisfied (checking, e.g., message content to decide if it should be extracted).
        uncond_tags ([str]): works like tags, but independently of `filt` function (allows message even if `filt` returns ``False``).
        tag_separator (str): a separator used to divide tag levels (usually ``'.'`` or ``'/'``).
            If it's not ``None``, tags are matched only either exactly, or if they're followed by tag separator (i.e., each tag level is treated as an indivisible word).
    """
    if tags is None:
        tags_p=lambda _: True
    else:
        tags=set(tags)
        tags_p=_tag_match_p(tags,tag_separator)
    uncond_tags=set(uncond_tags or [])
    uncond_tags_p=_tag_match_p(uncond_tags,tag_separator)
    if filt is None:
        filt=lambda _: True
    return lambda item: uncond_tags_p(item) or (tags_p(item) and filt(item))