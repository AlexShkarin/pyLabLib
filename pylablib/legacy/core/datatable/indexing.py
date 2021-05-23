"""
Processing and normalization of different indexing styles.  
"""

from builtins import range
from ..utils.py3 import textstring

import numpy as np
from ..utils import string as string_utils #@UnresolvedImport



def _single_idx(name, names_list, only_exact):
    if isinstance(name,int) or name is None:
        return name
    if only_exact:
        return string_utils.find_list_string(name,names_list,case_sensitive=True,as_prefix=False)[0]
    else:
        try:
            return string_utils.find_list_string(name,names_list,case_sensitive=True,as_prefix=False)[0]
        except KeyError:
            return string_utils.find_list_string(name,names_list,case_sensitive=True,as_prefix=True)[0]
def string_list_idx(names_to_find, names_list, only_exact=False):
    """
    Index through a list of strings in `names_list`.

    Return corresponding numerical indices.
    Case sensitive; first look for exact matching, then for prefix matching (unless ``only_exact=True``).
    """
    if isinstance(names_to_find,list):
        return [_single_idx(n,names_list,only_exact) for n in names_to_find]
    else:
        return _single_idx(names_to_find,names_list,only_exact)


def is_slice(idx):
    """
    Check if `idx` is slice.
    """
    #return isinstance(idx,slice)
    return type(idx)==slice
def is_range(idx):
    """
    Check if `idx` is iterable (list, numpy array, or `builtins.range`).
    """
    if isinstance(idx,list):
        return len(idx)==0 or isinstance(idx[0],int)
    if isinstance(idx,np.ndarray):
        return idx.dtype=="int"
    return isinstance(idx,range)
def is_bool_array(idx):
    """
    Check if `idx` is a boolean array.
    """
    if isinstance(idx,list):
        return len(idx)>0 and isinstance(idx[0],bool)
    if isinstance(idx,np.ndarray):
        return idx.dtype=="bool"
    return False
def to_range(idx, length):
    """
    Turn list, array, builtins.range, slice into an iterable.
    """
    if is_slice(idx):
        return range(*idx.indices(length))
    else:
        return idx

def covers_all(idx, length, strict=False, ordered=True):
    """
    Check if `idx` covers all of the elements (indices from 0 to `length`).

    If ``strict==True``, strictly checks the condition;
    otherwise may return ``False`` even if `idx` actually covers everything, but takes less time (i.e., can be used for optimization).
    If ``ordered==True``, only returns ``True`` when indices follow in order.
    """
    if is_slice(idx):
        rng=idx.indices(length)
        return rng==(0,length,1) or ((not ordered) and rng==(length-1,-1,-1))
    elif isinstance(idx,range):
        return (idx[0]==0 and idx[-1]==length-1) or ((not ordered) and (idx[0]==length-1 and idx[-1]==0))
    elif is_bool_array(idx):
            return len(idx)>=length and np.asarray(idx)[:length].all()
    elif strict:
        if is_range(idx):
            if len(idx)<length:
                    return False
            if ordered:
                for i,j in enumerate(idx[:length]):
                    if i!=j:
                        return False
                return True
            else:
                included=np.zeros(length,dtype="bool")
                for i in idx:
                    if i<length:
                        included[i]=True
                return included.all()
        return False
    else:
        return False
    
    

# Index transformers.
#     Allowed input types:
#         scalar: integer, string
#         vector: integer lists or numpy arrays, bool lists or numpy arrays, string lists or numpy arrays, builtin.ranges, slices and string slices
class IIndex(object):
    """
    A generic index object.

    Used to transform a variety of indexes into a subset applicable for specific objects (numpy arrays or lists).
    
    Allowed input index types:
        - scalar: integer, string
        - vector: integer lists or numpy arrays, bool lists or numpy arrays, string lists or numpy arrays, builtin.ranges, slices and string slices
    """
    def tup(self):
        """
        Represent index as a tuple for easy unpacking.
        """
        return (self.ndim,self.idx)


class NumpyIndex(IIndex):
    """
    NumPy compatible index: allows for integers, slices, numpy integer or boolean arrays, integer lists or builtin.ranges
    """
    def __init__(self, idx, ndim=None):
        IIndex.__init__(self)
        if ndim is None:
            if is_slice(idx):
                if isinstance(idx.start,textstring) or isinstance(idx.stop,textstring):
                    raise ValueError("can't accept string index for numpy object")
                self.ndim=1
            else:
                try:
                    if len(idx)==0:
                        self.ndim=1
                        idx=np.asarray(idx)
                    else:
                        val=idx[0]
                        if isinstance(val,textstring):
                            raise ValueError("can't accept string index for numpy object")
                        if isinstance(val,bool):
                            idx=np.asarray(idx)
                        self.ndim=1
                except (IndexError,TypeError,AttributeError):
                    self.ndim=0
            self.idx=idx
        else:
            self.ndim=ndim
            self.idx=idx
def to_numpy_idx(idx):
    # Assuming that idx is either raw or NumpyIndex
    if not isinstance(idx,IIndex):
        return NumpyIndex(idx)
    else:
        return idx 
    
class ListIndex(IIndex):
    """
    List compatible index: allows for integers, slices, numpy integer arrays, integer lists or builtin.ranges;
    """
    def __init__(self, idx, names=None, ndim=None):
        IIndex.__init__(self)
        if ndim is None:
            if is_slice(idx):
                if names is not None and (isinstance(idx.start,textstring) or isinstance(idx.stop,textstring)):
                    start_stop=string_list_idx([idx.start,idx.stop],names)
                    idx=slice(start_stop[0],start_stop[1],idx.step) # crash later if names is None
                self.ndim=1
            else:
                try:
                    if len(idx)==0:
                        self.ndim=1
                        idx=[]
                    else:
                        val=idx[0]
                        if isinstance(val,textstring):
                            if names:
                                idx=string_list_idx(idx,names)
                                if type(idx)==list:
                                    self.ndim=1
                                else:
                                    self.ndim=0
                            else:
                                raise ValueError("can't accept string index for list")
                        else:
                            if isinstance(val,bool) or isinstance(val,np.bool_):
                                idx=[i for i,v in enumerate(idx) if v]
                            self.ndim=1
                except (IndexError,TypeError,AttributeError):
                    self.ndim=0
            self.idx=idx
        else:
            self.ndim=ndim
            self.idx=idx
def to_list_idx(idx, names=None):
    # Assuming that idx is either raw or NumpyIndex
    if not isinstance(idx,IIndex):
        return ListIndex(idx,names=names)
    try:
        if idx.idx.dtype=="bool":
            return ListIndex([i for i,v in enumerate(idx.idx) if v],ndim=idx.ndim)
    except (TypeError,AttributeError):
        pass
    return ListIndex(idx.idx,ndim=idx.ndim)

class ListIndexNoSlice(ListIndex):
    """
    List compatible index with slice unwrapped into bultin.range: allows for integers, numpy integer arrays, integer lists or builtin.ranges;
    """
    def __init__(self, idx, names=None, length=None, ndim=None):
        if ndim is None:
            ListIndex.__init__(self,idx,names)
            if is_slice(self.idx):
                length=len(names) if length is None else length
                self.idx=range(*self.idx.indices(length))
        else:
            self.ndim=ndim
            self.idx=idx
def to_list_idx_noslice(idx, names=None, length=None):
    # Assuming that idx is either raw or ListIndex
    if not isinstance(idx,IIndex):
        return ListIndexNoSlice(idx,names=names)
    if is_slice(idx.idx):
        length=len(names) if length is None else length
        return ListIndexNoSlice(range(*idx.idx.indices(length)),ndim=idx.ndim)
    return ListIndexNoSlice(idx.idx,ndim=idx.ndim)
        
        
def to_double_index(idx, names):
    if type(idx)==tuple:
        try:
            idx1=NumpyIndex(idx[0])
            idx2=ListIndexNoSlice(idx[1],names)
            return idx1,idx2
        except ValueError:
            idx1=NumpyIndex(idx[1])
            idx2=ListIndexNoSlice(idx[0],names)
            return idx1,idx2
    else:
        try:
            return NumpyIndex(idx),ListIndexNoSlice(range(len(names)),ndim=1)
        except ValueError:
            return ListIndex(slice(None),ndim=1),ListIndexNoSlice(idx,names)