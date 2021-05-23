"""
Generic utilities for dealing with numerical arrays.
"""

from __future__ import division

import numpy as np
import pandas as pd
import math

from ..datatable import column #@UnresolvedImport
from ..datatable import table #@UnresolvedImport
from ..datatable.wrapping import wrap #@UnresolvedImport
from ..utils import general as general_utils #@UnresolvedImport
from ..utils import numerical #@UnresolvedImport


_depends_local=["..datatable.column","..datatable.table"]


##### Properties #####
@general_utils.try_method_wrapper
def is_ascending(wf):
    """
    Check the if waveform is ascending.
    
    If it has more than 1 dimension, check all lines along 0'th axis.
    """
    if len(wf)<2:
        return True
    return (wf[1:]-wf[:-1]>=0).all()
@general_utils.try_method_wrapper
def is_descending(wf):
    """
    Check if the waveform is descending.
    
    If it has more than 1 dimension, check all lines along 0'th axis.
    """
    if len(wf)<2:
        return True
    return (wf[1:]-wf[:-1]>0).all()
def is_ordered(wf):
    """
    Check if the waveform is ordered (ascending or descending).
    
    If it has more than 1 dimension, check all lines along 0'th axis.
    """
    return is_ascending(wf) or is_descending(wf)
@general_utils.try_method_wrapper
def is_linear(wf):
    """
    Check if the waveform is linear (values go with a constant step).
    
    If it has more than 1 dimension, check all lines along 0'th axis (with the same step for all).
    """
    if len(wf)<2:
        return True
    diff=wf[1:]-wf[:-1]
    return (diff==diff[(0,)*np.ndim(diff)]).all()
column.IDataColumn.add_array_function(is_ascending)
column.IDataColumn.add_array_function(is_descending)
column.IDataColumn.add_array_function(is_linear)
column.IDataColumn.is_ordered=is_ordered
column.LinearDataColumn.is_ascending = lambda col: col.step>=0
column.LinearDataColumn.is_descending = lambda col: col.step<=0
column.LinearDataColumn.is_linear = lambda _: True




##### Columns access #####
@general_utils.try_method_wrapper
def get_x_column(wf, x_column=None, idx_default=False):
    """
    Get x column of the waveform.
    
    `x_column` can be
        - an array: return as is;
        - ``'#'``: return index array;
        - ``None``: equivalent to '#' for 1D data if ``idx_default==False``, or to ``0`` otherwise;
        - integer: return the column with this index.
    """
    if np.ndim(x_column)>0:
        return x_column
    if x_column=="#":
        return wf.index if isinstance(wf,pd.DataFrame) or isinstance(wf,pd.Series) else column.LinearDataColumn(len(wf))
    elif np.ndim(wf)==1:
        if x_column is None and idx_default:
            return column.LinearDataColumn(len(wf))
        return wf
    else:
        if x_column is None:
            x_column=0
        return wrap(wf)[:,x_column]
    
def get_y_column(wf, y_column=None):
    """
    Get y column of the waveform.
    
    `y_column` can be
        - an array: return as is;
        - ``'#'``: return index array;
        - ``None``: return `wf` for 1D data, or the column ``1`` otherwise;
        - integer: return the column with this index.
    """
    if np.ndim(y_column)>0:
        return y_column
    if y_column=="#":
        return wf.index if isinstance(wf,pd.DataFrame) or isinstance(wf,pd.Series) else column.LinearDataColumn(len(wf))
    elif np.ndim(wf)==1:
        return wf
    else:
        if y_column is None:
            y_column=1
        return wrap(wf)[:,y_column]
    

##### Sorting #####
try:
    np.argsort([],kind="stable")
    _stable_sort="stable"
except ValueError:
    _stable_sort="mergesort"
def sort_by(wf, x_column=None, reverse=False, stable=False):
    """
    Sort 2D array using selected column as a key and preserving rows.
    
    If ``reverse==True``, sort in descending order. `x_column` values are described in :func:`.waveforms.get_x_column`.
    If ``stable==True``, use stable sort (could be slower and uses more memory)
    """
    x_column=get_x_column(wf,x_column)
    if reverse:
        return wrap(wf).t[x_column.argsort(kind=_stable_sort if stable else "quicksort"),::-1]
    else:
        return wrap(wf).t[x_column.argsort(kind=_stable_sort if stable else "quicksort")]
table.DataTable.sort_by=sort_by


##### Filtering #####
def filter_by(wf, columns=None, pred=None, exclude=False):
    """
    Filter 1D or 2D array using a predicate.
    
    If the data is 2D, `columns` contains indices of columns to be passed to the `pred` function.
    If ``exclude==False``, drop all of the rows satisfying `pred` rather than keep them.
    """
    if pred is None:
        return wf
    pred=general_utils.to_predicate(pred)
    wrapped=wrap(wf)
    if wrapped.ndim()==1:
        sat=np.array([pred(r) for r in wrapped]).astype(bool)
    else:
        if columns is None:
            columns=slice(None)
        wrapped_subtable=wrapped.subtable((slice(None),columns))
        sat=np.array([pred(*r) for r in wrapped_subtable.r]).astype(bool)
    return wrapped.t[~sat if exclude else sat]
table.DataTable.filter_by=filter_by

def unique_slices(wf, u_column):
    """
    Split a table into subtables with different values in a given column.
    
    Return a list of `wf` subtables, each of which has a different (and equal among all rows in the subtable) value in `u_column`.
    """
    wrapped=wrap(wf)
    u_column=get_y_column(wf,u_column)
    vals=np.unique(u_column)
    return [(v,wrapped.t[u_column==v]) for v in vals]
table.DataTable.unique_slices=unique_slices


##### Merging #####
def _get_common_type(types):
    counts={"2d.table":0,"2d.array":0,"1d.column":0,"1d.array":0}
    for t in types:
        counts[t]=counts[t]+1
    if counts["2d.array"]>0 or counts["1d.column"]>0 or counts["1d.array"]>0:
        return "array"
    else:
        return "table"
def merge(wfs, idx=None):
    """
    Merge several tables column-wise.
    
    If `idx` is not ``None``, then it is a list of index columns (one column per table) used for merging.
    The rows that have the same value in the index columns are merged; if some values aren't contained in all the `wfs`, the corresponding rows are omitted.
    
    If `idx` is ``None``, just join the tables together (they must have the same number of rows).
    """
    if idx is not None:
        if isinstance(idx,list) or isinstance(idx,tuple):
            if len(idx)!=len(wfs):
                raise ValueError("idx length is different from tables length")
        else:
            idx=[idx]*len(wfs)
    wrapped=[wrap(wf) for wf in wfs]
    result_type=_get_common_type([w.get_type() for w in wrapped])
    if idx is not None: # select common indices
        idx_cols=[w.c[c] if w.ndim()==2 else w.cont for c,w in zip(idx,wrapped)]
        common_idx=set.intersection(*[set(i) for i in idx_cols])
        common_idx=np.sort(np.array(list(common_idx)))
        cut=[wrap(common_idx)]
        for c,w in zip(idx,wrapped):
            if w.ndim()==2:
                wf=sort_by(filter_by(w.cont,c,common_idx),c)
                wf=wrap(wf).c.get_deleted(c,wrapped)
                cut.append(wf)
        wrapped=cut
    if result_type=="array":
        wfs=[np.column_stack((w[:])) if w.ndim()==1 else w[:,:] for w in wrapped]
        return np.concatenate(wfs,axis=1)
    else:
        columns=[]
        column_names=[]
        if idx is not None:
            idx_name=wfs[0].get_column_names(idx[0])
            wrapped[0]=wrap(table.DataTable(wrapped[0].cont,idx_name))
        for w in wrapped:
            columns=columns+w.c[:]
            column_names=column_names+w.c.get_names()
        return table.DataTable(columns,column_names)
            

##### Limits and ranges #####
class Range(object):
    """
    Single data range.
    
    If `start` or `stop` are ``None``, it's implied that they're at infinity (i.e., Range(None,None) is infinite).
    If the range object is ``None``, it's implied that the range is empty
    """
    def __init__(self, start=None, stop=None):
        object.__init__(self)
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
        """Check if `x` is in the range."""
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
        diff_array=xs-x
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
        if xs.ndim!=1:
            raise ValueError("ordered method is only applicable to 1D arrays")
        if len(xs)==0:
            return None
        lb,hb=0,len(xs)-1
        if xs[0]>xs[-1]: # must be reverse ordered
            arg_rev=find_closest_arg(xs[::-1],x,approach=approach,ordered=True)
            return len(xs)-1-arg_rev if arg_rev is not None else arg_rev
        if xs[lb]>x:
            if approach=="bottom":
                return None
            else:
                return lb
        if xs[hb]<x:
            if approach=="top":
                return None
            else:
                return hb
        while hb-lb>1:
            i=(lb+hb)//2
            el=xs[i]
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
            if abs(xs[lb]-x)<abs(xs[hb]-x):
                return lb
            else:
                return hb
column.IDataColumn.add_array_function(find_closest_arg)
def find_closest_arg_linear(params, x, approach="both"):
    """
    Same as :func:`find_closest_arg`, but works for linear column data.
    """
    if not (approach in ["top","bottom","both"]):
        raise ValueError("unrecognized approaching mode: {0}".format(approach))
    start,length,step=params
    if length==0:
        return None
    if step>=0:
        if x<start:
            if approach=="bottom":
                return None
            else:
                return 0
        if x>start+(length-1)*step:
            if approach=="top":
                return None
            else:
                return length-1
        i=(x-start)/float(step)
        if approach=="bottom":
            return int(math.floor(i))
        elif approach=="top":
            return int(math.ceil(i))
        else:
            return int(round(i))
    else:
        flipped_approach={"top":"bottom","bottom":"top","both":"both"}
        return length-1-find_closest_arg_linear((start+(length-1)*step,length,-step),x,approach=flipped_approach[approach])
def _col_linear_find_closest_arg(self, x, approach="both", ordered=None):
    return find_closest_arg_linear((self.start,self.length,self.step),x,approach=approach)
column.LinearDataColumn.find_closest_arg=_col_linear_find_closest_arg

def find_closest_value(xs, x, approach="both", ordered=False):
    return xs[find_closest_arg(xs,x,approach=approach,ordered=ordered)]


def get_range_indices(xs, xs_range, ordered=False):
    """
    Find waveform indices correspoding to the given range.
    
    The range is defined as ``xs_range[0]:xs_range[1]``, or infinite if ``xs_range=None`` (so the data is returned unchanged in that case).
    If ``ordered_x==True``, then the function assumes that `x_column` in ascending order.
    """
    # TODO: change ascending to arbitrary ordered
    # TODO: add x_column argument (?)
    if xs_range is not None:
        xs_range=Range(*xs_range)
        if ordered:
            if xs_range.start is None:
                min_i=0
            else:
                min_i=find_closest_arg(xs,xs_range.start,approach="top",ordered=True)
            if xs_range.stop is None:
                max_i=len(xs)
            else:
                max_i=find_closest_arg(xs,xs_range.stop,approach="bottom",ordered=True)
            if min_i is None or max_i is None:
                return slice(0)
            else:
                return slice(min_i,max_i+1)
        else:
            return xs_range.contains(xs[:])
    else:
        return slice(0)
column.IDataColumn.get_range_indices=get_range_indices
def _col_get_range_indices_linear(self, xs_range, ordered=None):
    return get_range_indices(self,xs_range,ordered=True)
column.LinearDataColumn.get_range_indices=_col_get_range_indices_linear

      
def _cut_to_range(wf, xs_range, x_column=None, ordered=False):
    """
    Cut the waveform to the given range based on `x_column`.
    
    The range is defined as ``xs_range[0]:xs_range[1]``, or infinite if ``xs_range=None``.
    `x_column` is used to determine which colmn's values to use to check if the point is in range (see :func:`.waveforms.get_x_column`).
    If ``ordered_x==True``, then the function assumes that `x_column` in ascending order.
    """
    x_column=get_x_column(wf,x_column)
    indices=get_range_indices(x_column,xs_range,ordered=ordered)
    return wrap(wf).t[indices]
cut_to_range=general_utils.try_method_wrapper(_cut_to_range,method_name="cut_to_range")
column.IDataColumn.cut_to_range=_cut_to_range
table.DataTable.cut_to_range=_cut_to_range

def _cut_out_regions(wf, regions, x_column=None, ordered=False, multi_pass=True):
    """
    Cut the regions out of the `wf` based on `x_column`.
    
    `x_column` is used to determine which colmn's values to use to check if the point is in range (see :func:`.waveforms.get_x_column`).
    If ``ordered_x==True``, then the function assumes that `x_column` in ascending order.
    If ``multi_pass==False``, combine all indices before deleting the data in a single operation (works faster, but only for non-intersecting regions). 
    """
    if not regions:
        return wf
    wrapped=wrap(wf).copy(wrapped=True)
    x_column=np.asarray(get_x_column(wf,x_column,idx_default=True))
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
cut_out_regions=general_utils.try_method_wrapper(_cut_out_regions,method_name="cut_out_regions")
column.IDataColumn.cut_out_regions=_cut_out_regions
table.DataTable.cut_out_regions=_cut_out_regions





##### Unwrapping #####

def find_discrete_step(wf, min_fraction=1E-8, tolerance=1E-5):
    """
    Try to find a minimal divisor of all steps in a 1D waveform.
    
    `min_fraction` is the minimal possible size of the divisor (relative to the minimal non-zero step size).
    `tolerance` is the tolerance of the division.
    Raise an :exc:`ArithmeticError` if no such value was found.
    """
    if len(wf)<2:
        raise ValueError('waveform length should be at least 2')
    diffs=wf[1:]-wf[:-1]
    q=diffs[0]
    for d in diffs[1:]:
        if d!=0:
            q=numerical.gcd_approx(q, abs(d), min_fraction, tolerance)
    return q

def unwrap_mod_data(wf, wrap_range):
    """
    Unwrap data given `wrap_range`.
    
    Assume that every jump greater than ``0.5*wrap_range`` is not real and is due to value being restricted.
    Can be used to, e.g., unwrap the phase data.
    """
    if len(wf)<2:
        return wf
    res=wf.copy()
    wraps=0
    prev=wf[0]
    for (i,v) in enumerate(wf[1:]):
        if abs(v-prev)>wrap_range*.5:
            wraps=wraps-round((v-prev)/wrap_range)*wrap_range
        res[i+1]=v+wraps
        prev=v
    return res





##### Waveform expansion on the edges #####

def expand_waveform(wf, size=0, mode="constant", cval=0., side="both"):
    """
    Expand 1D waveform for different convolution techniques.
    
    Args:
        wf: 1D array-like object.
        size (int): Expansion size. Can't be greater than ``len(wf)`` (truncated automatically).
        mode (str): Expansion mode. Can be ``'constant'`` (added values are determined by `cval`), ``'nearest'`` (added values are endvalues of the waveform),
            ``'reflect'`` (reflect waveform wrt its endpoint) or ``'wrap'`` (wrap the values from the other size).
        cval (float): If ``mode=='constant'``, determines the expanded values.
        side (str): Expansion side. Can be ``'left'``, ``'right'`` or ``'both'``.
    """
    wrapped=wrap(wf)
    if wrapped.ndim()==2:
        return wrapped.columns_replaced([expand_waveform(wrapped.c[i],size=size,mode=mode,cval=cval,side=side)
            for i in range(wrapped.shape()[1])],wrapped=False)
    elif wrapped.ndim()!=1:
        raise ValueError("this function accepts only 1D or 2D arrays")
    if len(wf)==0 or size==0:
        return wf
    if size>len(wf):
        size=len(wf)
    if mode=="constant":
        left_part=column.LinearDataColumn(size,0,0)+cval
        right_part=left_part
    elif mode=="nearest":
        left_part=column.LinearDataColumn(size,0,0)+wf[0]
        right_part=column.LinearDataColumn(size,0,0)+wf[-1]
    elif mode=="reflect":
        left_part=wf[size-1::-1]
        right_part=wf[-1:-size-1:-1]
    elif mode=="wrap":
        left_part=wf[-size:]
        right_part=wf[:size]
    else:
        raise ValueError("unrecognized boundary mode '{0}'".format(mode))
    if side=="left":
        res=np.concatenate(( left_part,wf ))
    elif side=="right":
        res=np.concatenate(( left_part,wf,right_part ))
    elif side=="both":
        res=np.concatenate(( left_part,wf,right_part ))
    else:
        raise ValueError("unrecognized side mode: {0}".format(side))
    return wrapped.array_replaced(res,wrapped=False)




##### Representation transformations #####

def xy2c(wf):
    """
    Convert the waveform from xy representation to a single complex data.
    
    `wf` is a 2D array with either 2 columns (x and y) or 3 columns (index, x and y).
    Return 2D array with either 1 column (c) or 2 columns (index and c).
    """
    wrapped=wrap(wf)
    if wrapped.ndim()!=2:
        raise ValueError("xy representation should be 2D")
    if wrapped.shape()[1] not in [2,3]:
        raise ValueError("xy representation can only have 2 or 3 columns")
    if wrapped.shape()[1]==2:
        return wrapped[:,0]+1j*wrapped[:,1]
    else:
        c=wrapped[:,1]+1j*wrapped[:,2]
        return wrapped.from_columns([wf[:,0],c],column_names=[wrapped.c.get_names()[0],"c"],wrapped=False)
    
def c2xy(wf):
    """
    Convert the waveform from c representation to a split x and y data.
    
    `wf` is either 1D array (c data) or a 2D array with either 1 column (c) or 2 columns (index and c).
    Return 2D array with either 2 column (x and y) or 3 columns (index, x and y).
    """
    wrapped=wrap(wf)
    if wrapped.ndim()==1:
        return np.column_stack((wf.real,wf.imag))
    if wrapped.shape()[1]==2:
        columns=[wf[:,0].real,wf[:,1].real,wf[:,1].imag]
        return wrapped.from_columns(columns,column_names=[wrapped.c.get_names()[0],"x","y"],wrapped=False)
    else:
        raise ValueError("2D c representation can only have 2 columns")