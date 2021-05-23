"""
A simple observer pool (notification pool) implementeation.
"""

import collections
from . import general

_depends_local=[".general"]

class ObserverPool(object):
    """
    An observer pool.

    Stores notification functions (callbacks), and calls them whenever :meth:`notify` is called.
    The callbacks can have priority (higher priority ones are called first) and filter (observer is only called if the filter function passes the notification tag).

    Args:
        expand_tuple(bool): if ``True`` and the notification value is a tuple, treat it as an argument list for the callback functions.
    """
    def __init__(self, expand_tuple=True):
        object.__init__(self)
        self._observers={}
        self._observers_uncacheable={}
        self._expand_tuple=expand_tuple
        self._call_cache={}
    
    _names_generator=general.NamedUIDGenerator(thread_safe=True)
    Observer=collections.namedtuple("Observer",["filt","callback","priority","attr","cacheable"])
    def add_observer(self, callback, name=None, filt=None, priority=0, attr=None, cacheable=False):
        """
        Add the observer callback.

        Args:
            callback(callable): callback function; takes at least one argument (notification tag), and possible more depending on the notification value.
            name(str): stored callback name; by default, a unique name is auto-generated
            filt(callable or None): a filter function for this observer (the observer is called only if the :meth:`notify` function tag and value pass the filter); by default, all tags are accepted
            priority(int): callback priority; higher priority callback are invoked first.
            attr: additional observer attributes (can be used by :class:`ObserverPool` subclasses to change their behavior).
            cacheable(bool): if ``True``, assumes that the filter function only depends on the tag, so its calls can be cached.
        Returns:
            callback name (equal to `name` if supplied; an automatically generated name otherwise).
        """
        if name is None:
            name=self._names_generator("observer")
        elif name in self._observers:
            raise ValueError("observer {} is already subscribed".format(name))
        self._observers[name]=self.Observer(filt,callback,priority,attr,cacheable)
        if not cacheable:
            self._observers_uncacheable[name]=self._observers[name]
        self._call_cache={}
        return name
    def remove_observer(self, name):
        """Remove the observer callback with the given name."""
        obs=self._observers.pop(name)
        if not obs.cacheable:
            del self._observers_uncacheable[name]
        self._call_cache={}
    
    def find_observers(self, tag, value):
        try:
            to_call=self._call_cache[tag]
        except KeyError:
            to_call=[]
            for n,o in self._observers.items():
                if (o.filt is None) or o.filt(tag,value):
                    to_call.append((n,o))
            to_call.sort(key=lambda x: -x[1].priority)
            self._call_cache[tag]=to_call
        found_uncachable=False
        for n,o in self._observers_uncacheable.items():
            if (o.filt is None) or o.filt(tag,value):
                to_call.append((n,o))
                found_uncachable=True
        if found_uncachable:
            to_call.sort(key=lambda x: -x[1].priority)
        return to_call
    def _call_observer(self, callback, tag, value):
        if self._expand_tuple and isinstance(value,tuple):
            return callback(tag,*value)
        else:
            return callback(tag,value)
    def notify(self, tag, value=()):
        """
        Notify the obserevers by calling their callbacks.

        Return a dictionary of the callback results.
        By default the value is an empty tuple: for ``expand_tuple==True`` this means that only one argument (`tag`) is passed to the callbacks.
        """
        to_call=self.find_observers(tag,value)
        results=[(n,self._call_observer(o.callback,tag,value)) for n,o in to_call]
        return dict(results)