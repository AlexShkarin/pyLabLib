from ..utils import observer_pool, py3, general
from . import callsync
from .utils import ReadChangeLock

import collections
import fnmatch
import re


def _as_name_list(lst):
    if lst is None:
        return None
    elif isinstance(lst,py3.textstring):
        return [lst]
    return lst
def _split_pattern_list(lst):
    vals,pvals=general.partition_list(lambda s: s.find("*")>=0,lst)
    pvals=[re.compile(fnmatch.translate(v)) for v in pvals]
    return vals,pvals
def _match_pattern_list(lst, v):
    for p in lst:
        if p.match(v):
            return True
    return False
TMulticast=collections.namedtuple("TMulticast",["src","tag","value"])
class MulticastPool:
    """
    Multicast dispatcher (somewhat similar in functionality to Qt signals).

    Manages dispatching multicasts between sources and destinations (callback functions).
    Each multicast has defined source, destination (both can also be ``"all"`` or ``"any"``, see methods descriptions for details), tag and value.
    Any thread can send a multicast or subscribe for a multicast with given filters (source, destination, tag, additional filters).
    If a multicast is emitted, it is checked against filters for all subscribers, and the passing ones are then called.
    """
    def __init__(self):
        self._pool=observer_pool.ObserverPool()
        self._pool_lock=ReadChangeLock()

    def subscribe_direct(self, callback, srcs="any", dsts="any", tags=None, filt=None, priority=0, scheduler=None, return_result=False, sid=None):
        """
        Subscribe an asynchronous callback to a multicast.

        If a multicast is sent, `callback` is called from the sending thread (not subscribed thread). Therefore, should be used with care.
        In Qt, analogous to making a signal connection with a direct call.

        Args:
            callback: callback function, which takes 3 arguments: source, tag, and value.
            srcs(str or [str]): multicast source name or list of source names to filter the subscription;
                can be ``"any"`` (any source) or ``"all"`` (only multicasts specifically having ``"all"`` as a source).
            dsts(str or [str]): multicast destination name or list of destination names to filter the subscription;
                can be ``"any"`` (any destination) or ``"all"`` (only source specifically having ``"all"`` as a destination).
            tags: multicast tag or list of tags to filter the subscription (any tag by default);
                can also contain Unix shell style pattern (``"*"`` matches everything, ``"?"`` matches one symbol, etc.)
            filt(callable): additional filter function which takes 4 arguments: source, destination, tag, and value,
                and checks whether multicast passes the requirements.
            priority(int): subscription priority (higher priority subscribers are called first).
            scheduler: if defined, multicast call gets scheduled using this scheduler instead of being called directly (which is the default behavior)
            return_result: if ``True``, use a result synchronizer to return the result of the subscribed call; otherwise, ignore the result
            sid(int): subscription ID (by default, generate a new unique name).

        Returns:
            subscription ID, which can be used to unsubscribe later.
        """
        srcs=_as_name_list(srcs)
        dsts=_as_name_list(dsts)
        tags=_as_name_list(tags)
        if tags is not None:
            tags,ptags=_split_pattern_list(tags)
        src_any="any" in srcs
        dst_any="any" in dsts
        def full_filt(tag, value):
            src,dst,tag=tag
            if (tags is not None) and (tag is not None):
                match=(tag in tags) or _match_pattern_list(ptags,tag)
                if not match:
                    return False
            if (not src_any) and (src!="all") and (src not in srcs):
                return False
            if (not dst_any) and (dst!="all") and (dst not in dsts):
                return False
            return filt(src,dst,tag,value) if (filt is not None) else True
        if scheduler is not None:
            _orig_callback=callback
            def schedule_call(*args, **kwargs):
                call=scheduler.build_call(_orig_callback,args,kwargs,sync_result=return_result)
                scheduler.schedule(call)
                return call.result_synchronizer
            callback=schedule_call
        elif return_result:
            _orig_callback=callback
            def sync_call(*args, **kwargs):
                result=_orig_callback(*args,**kwargs)
                return callsync.QDirectResultSynchronizer(result)
            callback=sync_call
        with self._pool_lock.changing():
            sid=self._pool.add_observer(callback,name=sid,filt=full_filt,priority=priority,cacheable=(filt is None))
        return sid
    def unsubscribe(self, sid):
        """Unsubscribe from a subscription with a given ID"""
        with self._pool_lock.changing():
            self._pool.remove_observer(sid)

    def send(self, src, dst="any", tag=None, value=None):
        """
        Send a multicast.

        Args:
            src(str): multicast source; can be a name, ``"all"`` (will pass all subscribers' source filters),
                or ``"any"`` (will only be passed to subscribers specifically subscribed to multicasts with ``"any"`` source).
            dst(str): multicast destination; can be a name, ``"all"`` (will pass all subscribers' destination filters),
                or ``"any"`` (will only be passed to subscribers specifically subscribed to multicasts with ``"any"`` destination).
            tag(str): multicast tag.
            value: multicast value.
        """
        with self._pool_lock.reading():
            to_call=self._pool.find_observers(TMulticast(src,dst,tag),value)
        return [obs.callback(src,tag,value) for _,obs in to_call]