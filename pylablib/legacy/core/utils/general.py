"""
Collection of small utilities.
"""

from builtins import input
from future.utils import viewitems, viewvalues

import time
import threading
import os, signal
from . import functions

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


def try_method_wrapper(func, method_name=None, inherit_signature=True):
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
                raise TypeError("{}() reqiqres jeyword argument 'self'".format(func.__name__))
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
        return tuple(func(v) for v in value)
    if isinstance(value,list):
        return list(func(v) for v in value)
    if isinstance(value,dict):
        return dict([(k,func(v)) for k,v in viewitems(value)])
    raise ValueError("value {} is not a container")
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
        return dict([(k,recursive_map(v,func)) for k,v in viewitems(value)])
    return func(value)

### Dictionary routines ###
def any_item(d):
    """Return arbitrary tuple ``(key, value)`` contained in the dictionary (works both in Python 2 and 3)"""
    return next(iter(viewitems(d)))
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
    for k,v in viewitems(d):
        if ( (not exclude) and pred(k) ) or ( exclude and not pred(k) ):
            filtered[k]=v
    return filtered
def map_dict_keys(func, d):
    """Map dictionary keys with `func`"""
    return dict((func(k),v) for k,v in viewitems(d))
def map_dict_values(func, d):
    """Map dictionary values with `func`"""
    return dict((k,func(v)) for k,v in viewitems(d))
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
        collection=viewitems(d)
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
    return dict([(kmap(v),k) for (k,v) in viewitems(d)]) if kmap else dict([(v,k) for (k,v) in viewitems(d)])

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
        return list(viewvalues(groups))
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


### Dummy resource ###

class DummyResource(object):
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

class RetryOnException(object):
    """
    Wrapper for repeating the same block of code several time if an exception occurs
    
    Useful for filesystem or communication operations, where retrying a failed operation is a valid option.
    
    Args:
        tries (int): Determines how many time will the chunk of code execute before re-rasing the exception;
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
        object.__init__(self)
        self.tries=tries
        if isinstance(exceptions, type) and issubclass(exceptions, Exception):
            exceptions=(exceptions,)
        self.exceptions=exceptions or (Exception,)
    class ExceptionCatcher(object):
        def __init__(self, retrier, try_number):
            object.__init__(self)
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
            
class SilenceException(object):
    """
    Context which silences exceptions raised in a block of code.
    
    Args:
        exceptions (Exception or list): A single exception class or a list of exception classes which are going to be silenced.
        on_exception (callable): A callback to be invoked if an exception occurs.
        reraise (bool): Defines if the exception is re-rased after the callback has been invoked.
        
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
        object.__init__(self)
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




### UID generator ###

class UIDGenerator(object):
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
    def __call__(self, inc=True):
        """
        Return a new unique numeric ID.
        
        If ``inc==False``, don't increase the internal counter (the next call will return the same ID). 
        """
        with self._lock:
            if inc:
                self._value=self._value+1
            return self._value
            
class NamedUIDGenerator(object):
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



### Skipped calling wrapper ###

def call_every(func, times=1, cooldown=0., default=None):
    """
    Wrap `func` such that calls to it are forwarded only under certain conditions.

    If ``times>1``, then `func` is called after at least `times` calls to the wrapped function.
    If ``cooldown>0``, then `func` is called after at least `cooldown` seconds passed since the last call.
    If both conditions are specified, they should be satisfied simultaneously.
    `default` specifies return value if `func` wasn't called.
    """
    state=[times,-cooldown] # counter, last_call_time
    @functions.getargsfrom(func)
    def wrapped(*args, **kwargs):
        curr_t=time.time()
        if (state[0]>=times-1) and (curr_t>state[1]+cooldown):
            state[1]=curr_t
            state[0]=0
            res=func(*args,**kwargs)
        else:
            state[0]+=1
            res=default
        return res
    return wrapped

def call_limit(func, times=1, cooldown=0., limit=None, default=None):
    """
    Wrap `func` such that calls to it are forwarded only under certain conditions.

    If ``times>1``, then `func` is called after at least `times` calls to the wrapped function.
    If ``cooldown>0``, then `func` is called after at least `cooldown` seconds passed since the last call.
    if ``limit is not None``, then `func` is called only first `limit` times.
    If several conditions are specified, they should be satisfied simultaneously.
    `default` specifies return value if `func` wasn't called.
    Returned function also has an added method ``reset``, which resets the internal call and time counters.
    """
    state=[times,0,-cooldown] # misses since last call, successfull calls, last call time
    @functions.getargsfrom(func)
    def wrapped(*args, **kwargs):
        curr_t=time.time()
        if (state[0]>=times-1) and (curr_t>state[1]+cooldown) and (limit is None or state[2]<limit):
            state[:]=0,curr_t,state[2]+1
            res=func(*args,**kwargs)
        else:
            state[0]+=1
            res=default
        return res
    def reset():
        state[:]=times,0,-cooldown
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



### Countdown ###

class Countdown(object):
    """
    Object for convenient handling of timeouts and countdowns with interrupts.
    
    Args:
        timeout (float): Countdown timeout; if ``None``, assumed to be infinite.
    """
    def __init__(self, timeout):
        self.timeout=timeout
        self.reset()
    def reset(self):
        self.start=time.time()
        if self.timeout is None:
            self.end=None
        else:
            self.end=self.timeout+self.start
    def time_left(self, bound_below=True):
        """
        Return the amount of time left. For infinite timeout, return ``None``.
        
        If ``bound_below==True``, instead of negative time return zero.
        """
        if self.timeout==0 or self.timeout is None:
            return self.timeout
        dtime=self.end-time.time()
        if bound_below:
            dtime=max(dtime,0.)
        return dtime
    def time_passed(self):
        """
        Return the amount of time passed since the countdown start/reset.
        """
        return time.time()-self.start
    def passed(self):
        """
        Check if the timeout has passed.
        """
        if self.timeout is None:
            return False
        elif self.timeout==0:
            return True
        else:
            t=time.time()
            return self.end<=t

class Timer(object):
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

class StreamFileLogger(object):
    """
    Steam logger that replaces standard output stream (usually stdout or stderr) and logs them into a file.

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
        object.__init__(self)
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
    except Exception:
        import pdb
        return pdb.set_trace


### Misc ###

def wait_for_keypress(message="Waiting..."):
    input(message)