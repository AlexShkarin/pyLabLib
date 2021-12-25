"""
Collection of small utilities.
"""

import time
import threading
import os, signal
import sys
import subprocess
import functools
import collections
import contextlib
import cProfile
from . import functions



### Setting/getting multiple properties

def set_props(obj, prop_names, props):
    """
    Set multiple attributes of `obj`.
    
    Names are given by `prop_names` list and values are given by `props` list. 
    """
    for (n,p) in zip(prop_names,props):
        setattr(obj,n,p)
def get_props(obj, prop_names):
    """
    Get multiple attributes of `obj`.
    
    Names are given by `prop_names` list.
    """
    return [getattr(obj,p) for p in prop_names]



### Defaulting to method call in a function ###

def using_method(func, method_name=None, inherit_signature=True):
    """
    Decorator that makes the function attempt to call the first argument's method instead of `func`.
    
    Before calling the function, try and call a method of the first argument named `method_name` (`func` name by default).
    If the method exists, call it instead of the wrapped function.
    If ``inherit_signature==True``, completely copy the signature of the wrapped method (name, args list, docstring, etc.).
    """
    if method_name is None:
        method_name=func.__name__
    def wrapped(*args, **kwargs):
        if args:
            self,args=args[0],args[1:]
            if "self" in kwargs:
                raise TypeError("{}() got multiple values for keyword argument 'self'".format(func.__name__))
        elif kwargs:
            if "self" not in kwargs:
                raise TypeError("{}() requires keyword argument 'self'".format(func.__name__))
            self=kwargs.pop("self")
        try:
            return getattr(self,method_name)(*args,**kwargs)
        except AttributeError:
            return func(self,*args,**kwargs)
    if inherit_signature:
        wrapped=functions.getargsfrom(func)(wrapped)
    else:
        wrapped.__doc__=func.__doc__
    return wrapped



### Predicates ###

def to_predicate(x):
    """
    Turn `x` into a predicate.
    
    If `x` is callable, it will be called with a single argument and returned value determines if the argument passes.
    If `x` is a container, an argument passes if it's contained in `x`.
    """
    if hasattr(x,"__call__"):
        return x
    if hasattr(x,"__contains__"):
        return lambda e: e in x
    raise ValueError("can't build predicate for {0}".format(x))



### Container routines ###

def map_container(value, func):
    """
    Map values  in the container.
    
    `value` can be a ``tuple``, a ``list`` or a ``dict`` (mapping is applied to the values)
    raises :exc:`ValueError` if it's something else.
    """
    if isinstance(value,tuple):
        return as_container(tuple(func(v) for v in value),type(value))
    if isinstance(value,list):
        return list(func(v) for v in value)
    if isinstance(value,dict):
        return dict([(k,func(v)) for k,v in value.items()])
    raise ValueError("value {} is not a container")
def as_container(val, t):
    """
    Turn iterable into a container of type `t`.

    Can handle named tuples, which have different constructor signature.
    """
    if issubclass(t,tuple) and hasattr(t,"_asdict"): # namedtuple
        return t(*val)
    else:
        return t(val)
def recursive_map(value, func):
    """
    Map container recursively.
    
    `value` can be a ``tuple``, a ``list`` or a ``dict`` (mapping is applied to the values).
    """
    if isinstance(value,tuple):
        return tuple(recursive_map(v,func) for v in value)
    if isinstance(value,list):
        return list(recursive_map(v,func) for v in value)
    if isinstance(value,dict):
        return dict([(k,recursive_map(v,func)) for k,v in value.items()])
    return func(value)
def make_flat_namedtuple(nt, fields=None, name=None, subfield_fmt="{field:}_{subfield:}"):
    """
    Turn a nested structure of named tuples into a single flat namedtuple.

    Args:
        nt: toplevel namedtuple class to be flattened
        fields: a dictionary ``{name: desc}`` of the fields, where ``name`` is the named tuple name,
            and ``desc`` is either a nested namedtuple class, or a list of arguments which are passed to the
            recursive call to this function (e.g., ``[TTuple, {"field": TNestedTuple}]``).
            Any tuple field which is present in this dictionary gets recursively flattened,
            and the field names of the corresponding returned tuple are added to the full list of fields
        name: name of the resulting tuple
        subfield_fmt: format string, which describes how the combined field name is built
            out of the original field name and the subtuple field name;
            by default, connect with ``"_"``, i.e., ``t.field.subfiled`` turns into ``t.field_subfield``.
    
    Return:
        a new namedtuple class, which describes the flattened structure
    """
    if name is None:
        name=nt.__name__
    field_names=[]
    for f in nt._fields:
        if fields and f in fields:
            sf=fields[f]
            sargs=sf if isinstance(sf,list) else [sf]
            subnames=make_flat_namedtuple(*sargs)._fields
            subnames=[subfield_fmt.format(field=f,subfield=sf) for sf in subnames]
            field_names+=subnames
        else:
            field_names.append(f)
    return collections.namedtuple(name,field_names)



### Dictionary routines ###

def any_item(d):
    """Return arbitrary tuple ``(key, value)`` contained in the dictionary (works both in Python 2 and 3)"""
    return next(iter(d.items()))
def merge_dicts(*dicts):
    """
    Combine multiple ``dict`` objects together.
    
    If multiple dictionaries have the same keys, later arguments have higher priority.
    """
    res={}
    for d in dicts:
        if d is not None:
            res.update(d)
    return res
def filter_dict(pred, d, exclude=False):
    """
    Filter dictionary based on a predicate.
    
    `pred` can be a callable or a container (in which case the predicate is true if a value is in the container).
    If ``exclude==True``, the predicate is inverted.
    """
    if pred is None:
        return d.copy() if exclude else {}
    pred=to_predicate(pred)
    filtered={}
    for k,v in d.items():
        if ( (not exclude) and pred(k) ) or ( exclude and not pred(k) ):
            filtered[k]=v
    return filtered
def map_dict_keys(func, d):
    """Map dictionary keys with `func`"""
    return dict((func(k),v) for k,v in d.items())
def map_dict_values(func, d):
    """Map dictionary values with `func`"""
    return dict((k,func(v)) for k,v in d.items())
def to_dict(d, default=None):
    """
    Convert a ``dict`` or a ``list`` of pairs or single keys (or mixed) into a ``dict``.
    
    If a list element is single, `default` value is used.
    """
    if d is None:
        return {}
    if isinstance(d,dict):
        return d
    res={}
    for e in d:
        if isinstance(e,list) or isinstance(e,tuple):
            res[d[0]]=d[1]
        else:
            res[d[0]]=default
    return res
def to_pairs_list(d, default=None):
    """
    Convert a ``dict`` or a ``list`` of pairs or single keys (or mixed) into a ``list`` of pairs.
    
    If a list element is single, `default` value is used.
    When converting ``list`` into ``list``, the order is preserved.
    """
    if d is None:
        return []
    if isinstance(d,dict):
        collection=d.items()
    else:
        collection=d
    res=[]
    for e in collection:
        if isinstance(e,list) or isinstance(e,tuple):
            res.append((e[0],e[1]))
        else:
            res.append((e,default))
    return res
def invert_dict(d, kmap=None):
    """
    Invert dictionary (switch keys and values).

    If `kmap` is supplied, it's a function mapping dictionary values into inverted dictionary keys (identity by default).
    """
    return dict([(kmap(v),k) for (k,v) in d.items()]) if kmap else dict([(v,k) for (k,v) in d.items()])



### List routines ###

def flatten_list(l):
    """
    Flatten nested ``list``/``tuple`` structure into a single list.
    """
    for el in l:
        if isinstance(el, list) or isinstance(el, tuple):
            for sub in flatten_list(el):
                yield sub
        else:
            yield el
def partition_list(pred, l):
    """
    Split the lis` `l` into two parts based on the predicate.
    """
    t=[]
    f=[]
    pred=to_predicate(pred)
    for e in l:
        if pred(e):
            t.append(e)
        else:
            f.append(e)
    return t,f
def split_in_groups(key_func, l, continuous=True, max_group_size=None):
    """
    Split the list `l` into groups according to the `key_func`.
    
    Go over the list and group the elements with the same key value together.
    If ``continuous==False``, groups all elements with the same key together regardless of where they are in the list.
    otherwise, group only continuous sequences of the elements with the same key together (element with different key in the middle will result in two groups).
    If ``continuous==True`` and `max_group_size` is not ``None``, it determines the maximal size of a group; larger groups are split into separate groups. 
    """
    if continuous:
        if len(l)==0:
            return []
        groups=[]
        g=[l[0]]
        key=key_func(l[0])
        for e in l[1:]:
            ek=key_func(e)
            if ek!=key or (max_group_size is not None and len(g)>=max_group_size):
                key=ek
                groups.append(g)
                g=[]
            g.append(e)
        groups.append(g)
        return groups
    else:
        groups={}
        for e in l:
            groups.get(key_func(e),[]).append(e)
        return list(groups.values())
def sort_set_by_list(s, l, keep_duplicates=True):
    """
    Convert the set `s` into a list ordered by a list `l`.
    
    Elements in `s` which are not in `l` are omitted.
    If ``keep_duplicates==True``, keep duplicate occurrences in `l` in the result; otherwise, only keep the first occurrence.
    """
    if keep_duplicates:
        return [e for e in l if e in s]
    else:
        res=[]
        s=s.copy()
        for e in l:
            if e in s:
                res.append(e)
                s.remove(e)
        return res
def compare_lists(l1, l2, sort_lists=False, keep_duplicates=True):
    """
    Return three lists ``(l1 and l2, l1-l2, l2-l1)``.
    
    If ``sort_lists==True``, sort the first two lists by `l1`, and the last one by `l2`; otherwise, the order is undefined.
    If ``sort_lists==True``, `keep_duplicated` determines if duplicate elements show up in the result.
    """
    s1,s2=set(l1),set(l2)
    diff_12=set.difference(s1,s2)
    diff_21=set.difference(s2,s1)
    both=set.intersection(s1,s2)
    if sort_lists:
        return sort_set_by_list(both,l1,keep_duplicates),sort_set_by_list(diff_12,l1,keep_duplicates),sort_set_by_list(diff_21,l2,keep_duplicates)
    else:
        return list(both),list(diff_12),list(diff_21)
        


### Tree routines ###

def _topological_order_dfs(graph, start, path=None, visited=None, order=None, priority=None):
    path=set(start) if path is None else path
    order=[] if order is None else order
    visited=set() if visited is None else visited
    children=graph.get(start,[])
    if priority is not None:
        children=sorted(children,key=lambda c: priority.get(c,None))
    for child in children:
        if child in path:
            raise ValueError("graph contains loop; topological order is impossible")
        if child in visited:
            continue
        path.add(child)
        _topological_order_dfs(graph,child,path,visited,order)
        path.remove(child)
    order.append(start)
    visited.add(start)
    return order
        
def topological_order(graph, visit_order=None):
    """
    Get a topological order of a graph.
    
    Return a list of nodes where each node is listed after its children.
    If `visit_order` is not ``None``, it is a list specifying nodes visiting order (nodes earlier in the list are visited first). Otherwise, the visit order is undefined.
    `graph` is a dictionary ``{node: [children]}``.
    If graph contains loops, raise :exc:`ValueError`.
    """
    order=[]
    visited=set()
    if visit_order is None:
        nodes=set(graph)
        while len(nodes)>0:
            start=nodes.pop()
            _topological_order_dfs(graph,start,visited=visited,order=order)
            nodes.difference_update(visited)
    else:
        vo_set=set(visit_order)
        nodes=visit_order+[n for n in graph if n not in vo_set]
        priority=dict([(v,i) for i,v in enumerate(nodes)])
        while len(nodes)>0:
            start=nodes.pop(0)
            _topological_order_dfs(graph,start,visited=visited,order=order,priority=priority)
            nodes=[n for n in nodes if n not in visited]
    return order



### Dummy resource ###

class DummyResource:
    """
    Object that acts as a resource (has ``__enter__`` and ``__exit__`` methods), but doesn't do anything.
    
    Analog of::
    
        @contextlib.contextmanager
        def dummy_resource():
            yield
    """
    def __enter__(self):
        return None
    def __exit__(self, etype, error, etrace):
        return False



### Errors handling / retrying ###

class RetryOnException:
    """
    Wrapper for repeating the same block of code several time if an exception occurs
    
    Useful for filesystem or communication operations, where retrying a failed operation is a valid option.
    
    Args:
        tries (int): Determines how many time will the chunk of code execute before re-raising the exception;
            ``None`` (default) means no limit
        exceptions (Exception or list): A single exception class or a ``list`` of exception classes which are going to be silenced.
        
    Example::
    
        for t in RetryOnException(tries,exceptions):
            with t:
                ... do stuff ...
                
    is analogue of::
    
        for i in range(tries):
            try:
                ... do stuff ...
            except exceptions:
                if i==tries-1:
                    raise
    """
    def __init__(self, tries=None, exceptions=None):
        self.tries=tries
        if isinstance(exceptions, type) and issubclass(exceptions, Exception):
            exceptions=(exceptions,)
        self.exceptions=exceptions or (Exception,)
    class ExceptionCatcher:
        def __init__(self, retrier, try_number):
            self.silent=retrier.tries is None or try_number+1<retrier.tries
            self.try_number=try_number
            self.retrier=retrier
        def __enter__(self):
            return self
        def __exit__(self, etype, error, etrace):
            self.etype=etype
            self.error=error
            self.etrace=etrace
            if etype is None:
                return True
            if not self.silent:
                return False
            for et in self.retrier.exceptions:
                if isinstance(error,et):
                    return True
            return False
        def reraise(self):
            raise self.error
    def __iter__(self):
        cnt=0
        while True:
            yield self.ExceptionCatcher(self,cnt)
            cnt=cnt+1
            
def retry_wait(func, try_times=1, delay=0., exceptions=None):
    """
    Try calling function (with no arguments) at most `try_times` as long as it keeps raising exception.
    
    If `exceptions` is not ``None``, it specifies which exception types should be silenced.
    If an exception has been raised, wait `delay` seconds before retrying.
    """
    for t in RetryOnException(try_times,exceptions):
        with t:
            return func()
        if delay>0:
            time.sleep(delay)
            
class SilenceException:
    """
    Context which silences exceptions raised in a block of code.
    
    Args:
        exceptions (Exception or list): A single exception class or a list of exception classes which are going to be silenced.
        on_exception (callable): A callback to be invoked if an exception occurs.
        reraise (bool): Defines if the exception is re-raised after the callback has been invoked.
        
    A simple bit of syntax sugar. The code::
    
        with SilenceException(exceptions,on_exception,reraise):
            ... do stuff ...
            
    is exactly analogous to::
    
        try:
            ... do stuff ...
        except exceptions:
            on_exception()
            if reraise:
                raise
    """
    def __init__(self, exceptions=None, on_exception=None, reraise=False):
        self.on_exception=on_exception
        self.reraise=reraise
        if isinstance(exceptions, type) and issubclass(exceptions, Exception):
            exceptions=(exceptions,)
        self.exceptions=exceptions or (Exception,)
    def __enter__(self):
        return self
    def __exit__(self, etype, error, etrace):
        if etype is None:
            return True
        for et in self.exceptions:
            if isinstance(error,et):
                if self.on_exception:
                    return self.on_exception()
        return not self.reraise
    
    
    
### Process handling ###

def full_exit(code=signal.SIGTERM):
    """
    Terminate the current process and all of its threads.
    
    Doesn't perform any cleanup or resource release; should only be used if the process is irrevocably damaged.
    """
    os.kill(os.getpid(),code)
    os._exit(code)



### UID generator ###

class UIDGenerator:
    """
    Generator of unique numeric IDs.
    
    Args:
        thread_safe (bool): If ``True``, using lock to ensure that simultaneous calls from different threads are handled properly.
    """
    def __init__(self, thread_safe=False):
        self._value=0
        if thread_safe:
            self._lock=threading.Lock()
        else:
            self._lock=DummyResource()
    def reset(self, value=0):
        """Reset the generator to the given value"""
        with self._lock:
            self._value=value
    def __call__(self, inc=True):
        """
        Return a new unique numeric ID.
        
        If ``inc==False``, don't increase the internal counter (the next call will return the same ID). 
        """
        with self._lock:
            value=self._value
            if inc:
                self._value=self._value+1
            return value
            
class NamedUIDGenerator:
    """
    Generator of unique string IDs based on a name.
    
    Args:
        name_template (str): Format string with two parameters (name and numeric ID) used to generate string IDs.
        thread_safe (bool): If ``True``, using lock to ensure that simultaneous calls from different threads are handled properly.
    """
    def __init__(self, name_template="{0}{1:03d}", thread_safe=False):
        self._uids={}
        self._name_template=name_template
        if thread_safe:
            self._lock=threading.Lock()
        else:
            self._lock=DummyResource()
    def __call__(self, name):
        """
        Return a new unique string ID with the given `name`.
        """
        with self._lock:
            uid=self._uids.setdefault(name,UIDGenerator(thread_safe=False))()
        return self._name_template.format(name,uid)



### Wrappers for skipping calls based on number/time ###

def call_limit(func, period=1, cooldown=0., limit=None, default=None):
    """
    Wrap `func` such that calls to it are forwarded only under certain conditions.

    If ``period>1``, then `func` is called after at least `period` calls to the wrapped function.
    If ``cooldown>0``, then `func` is called after at least `cooldown` seconds passed since the last call.
    if ``limit is not None``, then `func` is called only first `limit` times.
    If several conditions are specified, they should be satisfied simultaneously.
    `default` specifies return value if `func` wasn't called.
    Returned function also has an added method ``reset``, which resets the internal call and time counters.
    """
    state=[period,0,-cooldown] # misses since last call, successful calls, last call time
    @functions.getargsfrom(func)
    def wrapped(*args, **kwargs):
        curr_t=time.time()
        if (state[0]>=period-1) and (curr_t>state[1]+cooldown) and (limit is None or state[2]<limit):
            state[:]=0,curr_t,state[2]+1
            res=func(*args,**kwargs)
        else:
            state[0]+=1
            res=default
        return res
    def reset():
        state[:]=period,0,-cooldown
    wrapped.reset=reset
    return wrapped



### Docstring inheritance ###

def doc_inherit(parent):
    """
    Wrapper for inheriting docstrings from parent classes.
    
    Takes parent class as an argument and replaces the docstring of the wrapped function
    by the docstring of the same-named function from the parent class (if available).
    """
    def wrapper(func):
        if hasattr(parent,func.__name__):
            func.__doc__=getattr(parent,func.__name__).__doc__
        return func
    return wrapper



### Countdown / timer ###

class Countdown:
    """
    Object for convenient handling of timeouts and countdowns with interrupts.
    
    Args:
        timeout (float): Countdown timeout; if ``None``, assumed to be infinite.
        start (bool): if ``True``, automatically start the countdown; otherwise, wait until :meth:`trigger` is called explicitly
    """
    def __init__(self, timeout, start=True):
        self.timeout=timeout
        self.reset(start=start)
    def reset(self, start=True):
        """Restart the countdown from the current moment"""
        self.start=time.time() if start else None
        self.set_timeout(self.timeout)
    def trigger(self, restart=True):  # pylint: disable=redefined-outer-name
        """
        Trigger the countdown.

        If ``restart==True``, restart the countdown if it's running; otherwise, do nothing in that situation.
        """
        if restart or self.start is None:
            self.reset()
    def running(self):
        """Check if the countdown is running"""
        return self.start is not None
    def stop(self):
        """Stop the timer if currently running"""
        self.reset(start=False)
    def time_left(self, t=None, bound_below=True):
        """
        Return the amount of time left. For infinite timeout, return ``None``.
        
        If ``bound_below==True``, instead of negative time return zero.
        If `t` is supplied, it indicates the current time; otherwise, use ``time.time()``.
        """
        if self.start is None:
            return None
        if self.timeout==0 or self.timeout is None:
            return self.timeout
        t=t or time.time()
        dtime=self.end-t
        if bound_below:
            dtime=max(dtime,0.)
        return dtime
    def add_time(self, dt, t=None, bound_below=True):
        """
        Add a given amount of time (positive or negative) to the start time (timeout stays the same).

        If ``bound_below==True``, do not let the end time (start time plus timeout) to get below the current time.
        If `t` is supplied, it indicates the current time; otherwise, use ``time.time()``.
        """
        if self.start is None:
            return
        self.start+=dt
        if self.end is not None:
            self.end+=dt
            if bound_below:
                t=t or time.time()
                self.end=max(self.end,t)
    def set_timeout(self, timeout):
        """Change the timer timeout"""
        self.timeout=timeout
        if self.timeout is None or self.start is None:
            self.end=None
        else:
            self.end=self.timeout+self.start
    def time_passed(self):
        """Return the amount of time passed since the countdown start/reset, or ``None`` if it is not started"""
        return None if self.start is None else time.time()-self.start
    def passed(self):
        """Check if the timeout has passed"""
        if self.timeout is None or self.start is None:
            return False
        elif self.timeout==0:
            return True
        else:
            t=time.time()
            return self.end<=t

class Timer:
    """
    Object for keeping time of repeating tasks.
    
    Args:
        period (float): Timer period.
    """
    def __init__(self, period, skip_first=False):
        self.period=period
        self.reset(skip_first=skip_first)
    def change_period(self, period, method="current"):
        """
        Change the timer period.

        `method` specifies the changing method. Could be ``"current"`` (change the period of the ongoing tick), ``"next"`` (change the period starting from the next tick),
        ``"reset_skip"`` (reset the timer and skip the first tick) or ``"reset_noskip"`` (reset the timer and don't skip the first tick).
        """
        if method not in {"current","next","reset_skip","reset_noskip"}:
            raise ValueError("unrecognized changing method: {}".format(method))
        old_period=self.period
        self.period=period
        if method=="reset_noskip":
            self.reset(skip_first=False)
        elif method=="reset_skip":
            self.reset(skip_first=True)
        elif method=="current":
            self.next+=(period-old_period)
    def reset(self, skip_first=False):
        """
        Reset the timer.

        If ``skip_first==False``, timer ticks immediately; otherwise, it starts ticking only after one period.
        """
        start=time.time()
        self.next=start+self.period if skip_first else start
    def time_left(self, t=None, bound_below=True):
        """
        Return the amount of time left before the next tick.
        
        If ``bound_below==True``, instead of negative time return zero.
        """
        t=t or time.time()
        dtime=self.next-t
        if bound_below:
            dtime=max(dtime,0.)
        return dtime
    def passed(self, t=None):
        """
        Return the number of ticks passed.

        If timer period is zero, always return 1.
        """
        t=t or time.time()
        return int((t-self.next)//self.period)+1 if self.period>0 else 1
    def acknowledge(self, n=None, nmin=0):
        """
        Acknowledge the timer tick.

        `n` specifies the number of tick to acknowledge (by default, all passed).
        Return number of actually acknowledged ticks (0 if the timer hasn't ticked since the last acknowledgement).
        """
        npassed=max(self.passed(),nmin)
        if n is None:
            nack=npassed
        else:
            nack=min(npassed,n)
        self.next+=self.period*nack
        return nack



### Stream redirection ###

class StreamFileLogger:
    """
    Stream logger that replaces standard output stream (usually stdout or stderr) and logs them into a file.

    Args:
        path: path to the destination logfile. The file is always appended.
        stream: an optional output stream into which the output will be duplicated; usually, the original stream which is being replaced
        lock: a thread lock object, which is used for any file writing operation;
            necessary if replacing standard streams (such as ``sys.stdout`` or ``sys.stderr``) in a multithreading environment.
        autoflush: if ``True``, flush after any write operation into `stream`

    It is also possible to subclass the file and overload :meth:`write_header` method to write a header before the first file write operation during the execution.
    
    The intended use is to log stdout or stderr streams::

        import sys, threading
        sys.stderr = StreamFileLogger("error_log.txt", stream=sys.stderr, lock=threading.Lock())
    """
    def __init__(self, path, stream=None, lock=None, autoflush=False):
        self.paths=path if isinstance(path,list) else [path]
        self.stream=stream
        self.header_done=False
        self.lock=lock or DummyResource()
        self.autoflush=autoflush
    def write_header(self, f):
        """Write header to file stream `f`"""
        pass
    def add_path(self, path):
        """Add another logging path to the list"""
        with self.lock:
            if path not in self.paths:
                self.paths.append(path)
    def remove_path(self, path):
        """Remove logging path to the list"""
        with self.lock:
            if path in self.paths:
                del self.paths[self.paths.index(path)]
                return True
            else:
                return False
    def write(self, s):
        with self.lock:
            for p in self.paths:
                try:
                    for t in RetryOnException(5,exceptions=IOError):
                        with t:
                            with open(p,"a") as f:
                                if not self.header_done:
                                    self.write_header(f)
                                    self.header_done=True
                                f.write(s)
                            break
                        time.sleep(0.1)
                except IOError:
                    pass
            if self.stream is not None:
                self.stream.write(s)
                if self.autoflush:
                    self.stream.flush()
    def flush(self):
        with self.lock:
            if self.stream is not None:
                self.stream.flush()



### Debugging ###

@functions.delaydef
def setbp():
    try:
        try:
            from traitlets.config.configurable import MultipleInstanceError
        except ImportError:
            from IPython.config.configurable import MultipleInstanceError
        try:
            import ipdb
            return ipdb.set_trace
        except (ImportError, MultipleInstanceError):
            from IPython.core.debugger import Tracer
            return Tracer()
    except:  # pylint: disable=bare-except
        import pdb
        return pdb.set_trace

@contextlib.contextmanager
def timing(n=1, name=None, profile=False):
    """
    Context manager for timing a piece of code.
    
    Measures the time it takes to execute the wrapped code and prints the result.
    
    Args:
        n: can specify the number of repetitions, which is used to show time per single repetition.
        name: name which is printed alongside the time
        profile: if ``True``, use ``cProfile`` and print its output instead of a simple timing
    """
    if profile:
        p=cProfile.Profile()
        p.enable()
    n=max(n,1)
    t0=time.time()
    yield n
    dt=(time.time()-t0)/n
    if dt>1:
        ts="{:.4}s".format(dt)
    elif dt>1E-3:
        ts="{:.4}ms".format(dt*1E3)
    else:
        ts="{:.4}us".format(dt*1E6)
    print("{}: {}".format(name or "none",ts))
    if profile:
        p.disable()
        p.print_stats(sort=2)

### Iterators ###

class AccessIterator:
    """
    Simple sequential access iterator with customizable access function (by default it's 1D indexing).
    
    Determines end of iterations by :exc:`IndexError`.
    
    Args:
        obj: Container to be iterated over.
        access_function (callable): A function which takes two parameters `obj` and `idx`
            and either returns the element or raises :exc:`IndexError`. By default, a simple ``__getitem__`` operation.
    """
    def __init__(self, obj, access_function=None):
        self.obj=obj
        self.idx=0
        if access_function is None:
            access_function=lambda obj, idx: obj[idx]
        self.access_function=access_function
    def __iter__(self):
        return self
    def __next__(self):
        try:
            result=self.access_function(self.obj,self.idx)
            self.idx=self.idx+1
            return result
        except IndexError:
            raise StopIteration()
    next=__next__



def muxcall(argname, special_args=None, mux_argnames=None, return_kind="list", allow_partial=False):
    """
    Wrap a function such that it can become multiplexable over a given argument.

    Args:
        argname: name of the argument to loop over
        special_args: if not ``None``, defines a dictionary ``{arg: func}`` for special values of the argument
            (e.g., ``"all"``, ``None``, etc.), where ``arg`` is its value, and ``func`` is the method taking the same arguments
            as the called function and returning the substitute argument (e.g., a list of all arguments)
        mux_argnames: names of additional arguments which, when supplied list or dict values, and when the `argname` value is a list,
            specify different values for different calls
        return_kind: method to combined multiple returned values; can be ``"list"``, ``"dict"`` (return dict ``{arg: result}``),
            or ``"none"`` (simply return ``None``)
        allow_partial: if ``True`` and some of `mux_argnames` argument do not specify value for the full range of `argname` value,
            do not call the function for those unspecified values; otherwise (`allow_partial` is ``True``), the error will be raised
    """
    if return_kind not in ["list","dict","none"]:
        raise ValueError("unrecognized return type: {}; can be 'list', 'dict', or 'none'".format(return_kind))
    if mux_argnames is None:
        mux_argnames=()
    elif not isinstance(mux_argnames,(tuple,list)):
        mux_argnames=(mux_argnames,)
    def wrapper(func):
        sig=functions.funcsig(func)
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            all_args=sig.as_kwargs(args,kwargs,add_defaults=True)
            marg=all_args[argname]
            while True:
                try:
                    marg=special_args[marg](*args,**kwargs)
                except (KeyError,TypeError): # including non-hashable marg
                    break
            if isinstance(marg,list):
                mux_args={}
                for n in mux_argnames:
                    a=all_args[n]
                    if isinstance(a,list):
                        mux_args[n]=dict(zip(marg,a))
                    elif isinstance(a,dict):
                        mux_args[n]=a
                if allow_partial:
                    marg=[a for a in marg if all(a in ma for ma in mux_args.values())]
                res=[]
                for a in marg:
                    all_args[argname]=a
                    for n,ma in mux_args.items():
                        all_args[n]=ma[a]
                    res.append(func(**all_args))
                if return_kind=="dict":
                    res=dict(zip(marg,res))
                elif return_kind=="none":
                    res=None
            else:
                all_args[argname]=marg
                res=func(**all_args)
            return res
        return wrapped
    return wrapper



### Misc ###

def wait_for_keypress(message="Waiting..."):
    input(message)

def restart():
    """
    Restart the script.
    
    Execution will not resume after this call.
    Note: due to Windows limitations, this function does not replace the current process with a new one,
    but rather calls a new process and makes the current one wait for its execution.
    Hence, each nested call adds an additional loaded application into the memory.
    Therefore, nesting restart calls (i.e., calling several restarts in a row) should be avoided.
    """
    p=subprocess.Popen([sys.executable]+sys.argv)
    sys.exit(p.wait())