"""
Generic utilities for dealing with numerical arrays.
"""

from .table_wrap import wrap
from ..utils import general as general_utils
from ..utils import numerical

import numpy as np
import pandas as pd



##### Trace properties #####

def is_ascending(trace):
    """
    Check the if the trace is ascending.
    
    If it has more than 1 dimension, check all lines along 0'th axis.
    """
    if len(trace)<2:
        return True
    wrapped=wrap(trace)
    return np.all(wrapped[1:]-wrapped[:-1]>=0)
def is_descending(trace):
    """
    Check if the trace is descending.
    
    If it has more than 1 dimension, check all lines along 0'th axis.
    """
    if len(trace)<2:
        return True
    wrapped=wrap(trace)
    return np.all(wrapped[1:]-wrapped[:-1]<=0)
def is_ordered(trace):
    """
    Check if the trace is ordered (ascending or descending).
    
    If it has more than 1 dimension, check all lines along 0'th axis.
    """
    return is_ascending(trace) or is_descending(trace)
def is_linear(trace):
    """
    Check if the trace is linear (values go with a constant step).
    
    If it has more than 1 dimension, check all lines along 0'th axis (with the same step for all).
    """
    if len(trace)<2:
        return True
    wrapped=wrap(trace)
    diff=wrapped[1:]-wrapped[:-1]
    return np.all(diff==diff[(0,)*np.ndim(diff)])



##### Columns access #####

def get_x_column(t, x_column=None, idx_default=False):
    """
    Get x column of the table.
    
    `x_column` can be
        - an array: return as is;
        - ``'#'``: return index array;
        - ``None``: equivalent to '#' for 1D data if ``idx_default==False``, or to ``0`` otherwise;
        - integer: return the column with this index.
    """
    if np.ndim(x_column)>0:
        return x_column
    if x_column=="#":
        return np.asarray(t.index) if isinstance(t,pd.DataFrame) or isinstance(t,pd.Series) else np.arange(len(t))
    elif np.ndim(t)==1:
        if x_column is None and idx_default:
            return np.arange(len(t))
        return t
    else:
        if x_column is None:
            x_column=0
        try:
            return wrap(t)[:,x_column]
        except ValueError:
            return np.asarray(t[x_column])
    
def get_y_column(t, y_column=None):
    """
    Get y column of the table.
    
    `y_column` can be
        - an array: return as is;
        - ``'#'``: return index array;
        - ``None``: return `t` for 1D data, or the column ``1`` otherwise;
        - integer: return the column with this index.
    """
    if np.ndim(y_column)>0:
        return y_column
    if y_column=="#":
        return t.index if isinstance(t,pd.DataFrame) or isinstance(t,pd.Series) else np.arange(len(t))
    elif np.ndim(t)==1:
        return t
    else:
        if y_column is None:
            y_column=1
        try:
            return wrap(t)[:,y_column]
        except ValueError:
            return np.asarray(t[y_column])
    


##### Sorting #####

try:
    np.argsort([],kind="stable")
    _stable_sort="stable"
except ValueError:
    _stable_sort="mergesort"
def sort_by(t, x_column=None, reverse=False, stable=False):
    """
    Sort a table using selected column as a key and preserving rows.
    
    If ``reverse==True``, sort in descending order. `x_column` values are described in :func:`.get_x_column`.
    If ``stable==True``, use stable sort (could be slower and uses more memory, but preserves the order of elements for the same key)
    """
    x_column=get_x_column(t,x_column)
    if reverse:
        return wrap(t).t[x_column.argsort(kind=_stable_sort if stable else "quicksort"),::-1]
    else:
        return wrap(t).t[x_column.argsort(kind=_stable_sort if stable else "quicksort")]



##### Filtering #####

def filter_by(t, columns=None, pred=None, exclude=False):
    """
    Filter 1D or 2D array using a predicate.
    
    If the data is 2D, `columns` contains indices of columns to be passed to the `pred` function.
    If ``exclude==False``, drop all of the rows satisfying `pred` rather than keep them.
    """
    if pred is None:
        return t
    pred=general_utils.to_predicate(pred)
    wrapped=wrap(t)
    if wrapped.ndim()==1:
        sat=np.array([pred(r) for r in wrapped]).astype(bool)
    else:
        if columns is None:
            columns=slice(None)
        wrapped_subtable=wrapped.subtable((slice(None),columns),wrapped=True)
        sat=np.array([pred(*r) for r in wrapped_subtable.r]).astype(bool)
    return wrapped.t[~sat if exclude else sat]

def unique_slices(t, u_column):
    """
    Split a table into subtables with different values in a given column.
    
    Return a list of `t` subtables, each of which has a different (and equal among all rows in the subtable) value in `u_column`.
    """
    wrapped=wrap(t)
    u_column=get_y_column(t,u_column)
    vals=np.unique(u_column)
    return [(v,wrapped.t[u_column==v]) for v in vals]



##### Merging #####

def _get_common_type(types):
    counts={"2d.pandas":0,"2d.array":0,"1d.series":0,"1d.array":0}
    for t in types:
        counts[t]=counts[t]+1
    if counts["2d.array"]>0 or counts["1d.series"]>0 or counts["1d.array"]>0:
        return "array"
    else:
        return "pandas"
def merge(ts, idx=None, as_array=True):
    """
    Merge several tables column-wise.
    
    If `idx` is not ``None``, then it is a list of index columns (one column per table) used for merging.
    The rows that have the same value in the index columns are merged; if some values aren't contained in all the `ts`, the corresponding rows are omitted.
    If `idx` is ``None``, just join the tables together (they must have the same number of rows).

    If ``as_array==True``, return a simple numpy array as a result; otherwise, return a pandas DataFrame if applicable
    (note that in this case all column names in all tables must be different to avoid conflicts)
    """
    if idx is not None:
        if isinstance(idx,list) or isinstance(idx,tuple):
            if len(idx)!=len(ts):
                raise ValueError("idx length is different from tables length")
        else:
            idx=[idx]*len(ts)
    wrapped=[wrap(t) for t in ts]
    result_type="array" if as_array else _get_common_type([w.get_type() for w in wrapped])
    if idx is not None: # select common indices
        idx_cols=[w.c[c] if w.ndim()==2 else w.cont for c,w in zip(idx,wrapped)]
        common_idx=set.intersection(*[set(i) for i in idx_cols])
        common_idx=np.sort(np.array(list(common_idx)))
        cut=[wrap(common_idx)]
        for c,w in zip(idx,wrapped):
            if w.ndim()==2:
                t=sort_by(filter_by(w.cont,c,common_idx),c)
                t=wrap(t).c.get_deleted(c,wrapped,wrapped=True)
                cut.append(t)
        wrapped=cut
    if result_type=="array":
        ts=[np.column_stack((w[:])) if w.ndim()==1 else w[:,:] for w in wrapped]  # pylint: disable=not-callable
        return np.concatenate(ts,axis=1)
    else:
        columns,names=zip(*[(n,v) for w in wrapped for n,v in zip(w.c.get_names(),w.c)])
        return pd.DataFrame(dict(zip(names,columns)),columns=names)



##### Limits and ranges #####

class Range:
    """
    Single data range.
    
    If `start` or `stop` are ``None``, it's implied that they're at infinity (i.e., Range(None,None) is infinite).
    If the range object is ``None``, it's implied that the range is empty
    """
    def __init__(self, start=None, stop=None):
        if isinstance(start,(list,tuple)):
            start,stop=start
        self._rng=[start,stop]
        self._reorder()
    
    def _reorder(self):
        if (self._rng[0] is not None) and (self._rng[1] is not None): 
            self._rng=[min(*self._rng),max(*self._rng)]
    @property
    def start(self): return self._rng[0]
    @start.setter
    def start(self, val):
        self._rng[0]=val
        self._reorder()
    @property
    def stop(self): return self._rng[1]
    @stop.setter
    def stop(self, val):
        self._rng[1]=val
        self._reorder()
    def __getitem__(self, i):
        return self._rng[i]
    def __setitem__(self, i, val):
        self._rng[i]=val
        self._reorder()
    def __len__(self): return 2
    def __str__(self): return "({0}, {1})".format(*self._rng)
    def __repr__(self): return "Range({0}, {1})".format(*self._rng)
    def contains(self, x):
        """Check if `x` is in the range"""
        if self is None:
            return (x!=x) # all False
        if (self._rng[0] is not None) and (self._rng[1] is not None):
            return (x>=self._rng[0])&(x<=self._rng[1])
        elif self._rng[0] is not None:
            return (x>=self._rng[0])
        elif self._rng[1] is not None:
            return (x<=self._rng[1])
        else:
            return (x==x) # all True
    @staticmethod
    def _min(a,b):
        if a is None:
            return b
        elif b is None:
            return a
        return min(a,b)
    @staticmethod
    def _max(a,b):
        if a is None:
            return b
        elif b is None:
            return a
        return max(a,b)
    def _intersect_two(self, rng):
        if rng is None:
            return None
        left=self._max(self._rng[0],rng._rng[0])
        right=self._min(self._rng[1],rng._rng[1])
        if (left is not None) and (right is not None) and left>right:
            return None
        return Range(left,right)
    def intersect(self, *rngs):
        """
        Find an intersection of multiple ranges.
        
        If the intersection is empty, return ``None``.
        """
        rng=self
        for r in rngs:
            if rng is None:
                return None
            rng=rng._intersect_two(r)
        return rng
    def rescale(self, mult=1., shift=0.):
        for i in [0,1]:
            self._rng[i]=None if self._rng[i] is None else self._rng[i]*mult+shift
        if mult<0:
            self._rng=self._rng[::-1]
        self._reorder()
        return self
    def tup(self):
        return tuple(self._rng)
    
    
def find_closest_arg(xs, x, approach="both", ordered=False):
    """
    Find the index of a value in `xs` that is closest to `x`.
    
    `approach` can take values ``'top'``, ``'bottom'`` or ``'both'`` and denotes from which side should array elements approach `x`
    (meaning that the found array element should be ``>x``, ``<x`` or just the closest one).
    If there are no elements lying on the desired side of `x` (e.g. ``approach=='top'`` and all elements of `xs` are less than `x`), the function returns ``None``. 
    if ``ordered==True``, then `xs` is assumed to be in ascending or descending order, and binary search is implemented (works only for 1D arrays).
    if there are recurring elements, return any of them.
    """
    if not (approach in ["top","bottom","both"]):
        raise ValueError("unrecognized approaching mode: {0}".format(approach))
    try:
        return xs.find_closest_arg(x,approach=approach,ordered=ordered)
    except AttributeError:
        pass
    if not ordered:
        diff_array=np.asarray(xs)-x
        if approach=="top":
            threshold=diff_array>=0
            if threshold.any():
                diff_array=diff_array*threshold+(diff_array.max()+1.)*(~threshold)
                return diff_array.argmin()
            else:
                return None
        elif approach=="bottom":
            threshold=diff_array<=0
            if threshold.any():
                diff_array=diff_array*threshold+(diff_array.min()-1.)*(~threshold)
                return diff_array.argmax()
            else:
                return None
        else:
            return abs(diff_array).argmin()
    else:
        wxs=wrap(xs)
        if wxs.ndim()!=1:
            raise ValueError("ordered method is only applicable to 1D arrays")
        if len(xs)==0:
            return None
        lb,hb=0,len(xs)-1
        if wxs[0]>wxs[-1]: # must be reverse ordered
            arg_rev=find_closest_arg(xs[::-1],x,approach=approach,ordered=True)
            return len(xs)-1-arg_rev if arg_rev is not None else arg_rev
        if wxs[lb]>x:
            if approach=="bottom":
                return None
            else:
                return lb
        if wxs[hb]<x:
            if approach=="top":
                return None
            else:
                return hb
        while hb-lb>1:
            i=(lb+hb)//2
            el=wxs[i]
            if el<x:
                lb=i
            elif el>x:
                hb=i
            else:
                return i
        if approach=="top":
            return hb
        elif approach=="bottom":
            return lb
        else:
            if abs(wxs[lb]-x)<abs(wxs[hb]-x):
                return lb
            else:
                return hb

def find_closest_value(xs, x, approach="both", ordered=False):
    return wrap(xs)[find_closest_arg(xs,x,approach=approach,ordered=ordered)]

def get_range_indices(xs, xs_range, ordered=False):
    """
    Find trace indices corresponding to the given range.
    
    The range is defined as ``xs_range[0]:xs_range[1]``, or infinite if ``xs_range=None`` (so the data is returned unchanged in that case).
    If ``ordered==True``, then the function assumes that `xs` in ascending or descending order.
    """
    if xs_range is not None:
        xs_range=Range(*xs_range)
        wrapped=wrap(xs)
        if ordered and len(wrapped)>10:
            if wrapped[1]>wrapped[0]:
                if xs_range.start is None:
                    min_i=0
                else:
                    min_i=find_closest_arg(xs,xs_range.start,approach="top",ordered=True)
                if xs_range.stop is None:
                    max_i=len(xs)
                else:
                    max_i=find_closest_arg(xs,xs_range.stop,approach="bottom",ordered=True)
            else:
                if xs_range.start is None:
                    max_i=len(xs)
                else:
                    max_i=find_closest_arg(xs,xs_range.start,approach="top",ordered=True)
                if xs_range.stop is None:
                    min_i=0
                else:
                    min_i=find_closest_arg(xs,xs_range.stop,approach="bottom",ordered=True)
            if min_i is None or max_i is None:
                return slice(0)
            else:
                return slice(min_i,max_i+1)
        else:
            return xs_range.contains(np.asarray(xs))
    else:
        return slice(0)

      
def cut_to_range(t, xs_range, x_column=None, ordered=False):
    """
    Cut the table to the given range based on `x_column`.
    
    The range is defined as ``xs_range[0]:xs_range[1]``, or infinite if ``xs_range=None``.
    `x_column` is used to determine which column's values to use to check if the point is in range (see :func:`.get_x_column`).
    If ``ordered_x==True``, then the function assumes that `x_column` in ascending order.
    """
    x_column=get_x_column(t,x_column)
    indices=get_range_indices(x_column,xs_range,ordered=ordered)
    return wrap(t).t[indices]

def cut_out_regions(t, regions, x_column=None, ordered=False, multi_pass=True):
    """
    Cut the regions out of the `t` based on `x_column`.
    
    `x_column` is used to determine which column's values to use to check if the point is in range (see :func:`.get_x_column`).
    If ``ordered_x==True``, then the function assumes that `x_column` in ascending order.
    If ``multi_pass==False``, combine all indices before deleting the data in a single operation (works faster, but only for non-intersecting regions). 
    """
    if not regions:
        return t
    wrapped=wrap(t).copy(wrapped=True)
    x_column=np.asarray(get_x_column(t,x_column,idx_default=True))
    if multi_pass:
        for r in regions:
            idx=get_range_indices(x_column,r,ordered=ordered)
            x_column=np.delete(x_column,idx)
            del wrapped.r[idx]
    else:
        all_idx=[]
        for r in regions:
            idx=get_range_indices(x_column,r,ordered=ordered)
            if isinstance(idx,slice):
                idx=range(*idx.indices(len(x_column)))
            all_idx=all_idx+list(idx)
        del wrapped.r[all_idx]
    return wrapped.cont



##### Unwrapping #####

def find_discrete_step(trace, min_fraction=1E-8, tolerance=1E-5):
    """
    Try to find a minimal divisor of all steps in a 1D trace.
    
    `min_fraction` is the minimal possible size of the divisor (relative to the minimal non-zero step size).
    `tolerance` is the tolerance of the division.
    Raise an :exc:`ArithmeticError` if no such value was found.
    """
    trace=np.asarray(trace)
    if len(trace)<2:
        raise ValueError('trace length should be at least 2')
    diffs=trace[1:]-trace[:-1]
    diffs=diffs[np.abs(diffs)!=0]
    if len(diffs)==0:
        return 0
    q=abs(diffs[0])
    for d in diffs[1:]:
        if d!=0:
            q=numerical.gcd_approx(q,abs(d),min_fraction,tolerance)
    return q

def unwrap_mod_data(trace, wrap_range):
    """
    Unwrap data given `wrap_range`.
    
    Assume that every jump greater than ``0.5*wrap_range`` is not real and is due to value being restricted.
    Can be used to, e.g., unwrap the phase data.
    """
    trace=np.asarray(trace)
    if len(trace)<2:
        return trace
    res=trace.copy()
    wraps=0
    prev=trace[0]
    for (i,v) in enumerate(trace[1:]):
        if abs(v-prev)>wrap_range*.5:
            wraps=wraps-round((v-prev)/wrap_range)*wrap_range
        res[i+1]=v+wraps
        prev=v
    return res



##### Trace expansion on the edges #####

def pad_trace(trace, pad, mode="constant", cval=0.):
    """
    Expand 1D trace or a multi-column table for different convolution techniques.
    
    Wrapper around :func:`numpy.pad`, but can handle pandas dataframes or multi-column arrays.
    Note that the index data is not preserved.

    Args:
        trace: 1D array-like object.
        pad (int or tuple): Expansion size. Can be an integer, if pad on both sides is equal, or a 2-tuple ``(left, right)`` for pads on opposite sides.
        mode (str): Expansion mode. Takes the same values as :func:`numpy.pad`.
            Common values are ``'constant'`` (added values are determined by `cval`), ``'edge'`` (added values are end values of the trace),
            ``'reflect'`` (reflect trace with respect to its endpoint) or ``'wrap'`` (wrap the values from the other size).
        cval (float): If ``mode=='constant'``, determines the expanded values.
    """
    wrapped=wrap(trace)
    if wrapped.ndim()==2:
        return wrapped.columns_replaced([pad_trace(wrapped.c[i],pad=pad,mode=mode,cval=cval)
            for i in range(wrapped.shape()[1])])
    elif wrapped.ndim()!=1:
        raise ValueError("this function accepts only 1D or 2D arrays")
    if len(trace)==0 or pad==0:
        return trace
    kwargs={"constant_values":cval} if mode=="constant" else {}
    res=np.pad(trace,pad,mode=mode,**kwargs)
    return wrapped.array_replaced(res)



##### Representation transformations #####

def xy2c(t):
    """
    Convert a trace or a table from xy representation to a single complex data.
    
    `t` is a 2D array with either 2 columns (x and y) or 3 columns (index, x and y).
    Return 2D array with either 1 column (c) or 2 columns (index and c).
    """
    wrapped=wrap(t)
    if wrapped.ndim()!=2:
        raise ValueError("xy representation should be 2D")
    if wrapped.shape()[1] not in [2,3]:
        raise ValueError("xy representation can only have 2 or 3 columns")
    if wrapped.shape()[1]==2:
        if wrapped.get_type=="1d.array":
            return wrapped[:,0]+1j*wrapped[:,1]
        else:
            return pd.DataFrame({"c":wrapped[:,0]+1j*wrapped[:,1]},index=wrapped.get_index())
        return 
    else:
        c=wrapped[:,1]+1j*wrapped[:,2]
        return wrapped.from_columns([t[:,0],c],column_names=[wrapped.c.get_names()[0],"c"],index=wrapped.get_index())
    
def c2xy(t):
    """
    Convert the a trace or a table from complex representation to a split x and y data.
    
    `t` is either 1D array (c data) or a 2D array with either 1 column (c) or 2 columns (index and c).
    Return 2D array with either 2 column (x and y) or 3 columns (index, x and y).
    """
    wrapped=wrap(t)
    t=np.asarray(t)
    if wrapped.ndim()==1:
        if wrapped.get_type=="1d.array":
            return np.column_stack((t.real,t.imag))
        else:
            return pd.DataFrame({"x":t.real,"t":t.imag},index=wrapped.get_index())
    if wrapped.shape()[1]==1:
        columns=[t[:,0].real,t[:,0].imag]
        return wrapped.from_columns(columns,column_names=["x","y"],index=wrapped.get_index())
    if wrapped.shape()[1]==2:
        columns=[t[:,0].real,t[:,1].real,t[:,1].imag]
        return wrapped.from_columns(columns,column_names=[wrapped.c.get_names()[0],"x","y"],index=wrapped.get_index())
    else:
        raise ValueError("2D c representation can only have 2 columns")