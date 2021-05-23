"""
Single column classes. Used in `ColumnDataTableStorage`.
"""

import numpy as np

from ..utils import numclass, strdump#@UnresolvedImport
from ..utils import iterator as iterator_utils #@UnresolvedImport
from . import indexing
from .datatable_utils import as_array

_depends_local=["..utils.numclass","..utils.strdump"]


##### Data column #####

class IDataColumn(numclass.NumClass):
    
    ## Indexing ##
    def _get_item(self, idx):
        """
        Return value(s) at `idx` as a number or a numpy array (copying isn't required).
        """
        raise NotImplementedError("IDataColumn._get_item")
    def _get_single_item(self, idx):
        """
        Return value at `idx` as a number; `idx` is a single index.
        """
        return self._get_item(idx)
    def _set_item(self, idx, val):
        """
        Assign value(s) at `idx` to `val`.
        
        `val` can be a single value, a numpy array or another column.
        Return a :class:`IDataColumn` object (usually it's self, but can be expanded if the current class doesn't support assigning values).
        """
        raise NotImplementedError("IDataColumn._set_item")
    def _del_item(self, idx):
        """
        Delete value(s) at `idx`.
        
        Return a :class:`IDataColumn` object (usually it's self, but can be expanded if the current class doesn't support deleting values).
        """
        raise NotImplementedError("IDataColumn._set_item")
    def _add_item(self, idx, val):
        """
        Only supports adding at a single specific location.
        """
        raise NotImplementedError("IDataColumn._add_item")
    def expand(self, length):
        """
        Expand column. Usually fill with zeros, unless the column values can be auto-predicted.
        """
        self.insert(None,np.zeros(length))
        return self
    def subcolumn(self, idx, force_copy=False):
        """
        Return value(s) at `idx` as a column object.
        """
        if force_copy:
            if indexing.covers_all(idx,self.nrows()):
                return self.copy()
            else:
                return ArrayDataColumn(as_array(self._get_item(idx),force_copy=force_copy))
        else:
            if indexing.covers_all(idx,self.nrows()):
                return self
            else:
                return ArrayDataColumn(self._get_item(idx))
        
    def __getitem__(self, idx):
        return self._get_item(idx)
    def __setitem__(self, idx, val):
        if self._set_item(idx,val) is not self:
            raise ValueError("can't set items while preserving column type")
    def __delitem__(self, idx):
        if self._del_item(idx) is not self:
            raise ValueError("can't delete items while preserving column type")
    def insert(self, idx, val):
        """
        Add a value `val` to the column at a position given by `idx`.
        """
        if idx is None:
            idx=self.nrows()
        if self._add_item(idx,val) is not self:
            raise ValueError("can't insert items while preserving column type")
    def append(self, val):
        """
        Append a value to the column
        """
        self.insert(None,val)
    
    
    ## Casting to NumPy array ##
    def as_array(self, force_copy=False):
        """
        Turn the column into a numpy array
        """
        if force_copy:
            return self[:].copy()
        else:
            return self[:]
    ## Numpy ufunc support ##
    def __array__(self): # property for compatibility with np.ufuncs
        return self.as_array()
    def __array_wrap__(self, arr, context=None):
        return ArrayDataColumn(arr) if np.ndim(arr)==1 else arr
        
    ## Copying ##
    def copy(self):
        raise NotImplementedError("IDataColumn.copy")
    
    ## Shape ##
    @property
    def shape(self):
        raise NotImplementedError("IDataColumn.shape")
    def nrows(self):
        return self.shape[0]
    @property
    def ndim(self):
        return 1
    def __len__(self):
        return self.nrows()
    
    ## Iterators ##
    def __iter__(self):
        return iterator_utils.AccessIterator(self)
    
    ## Repr ##
    def __str__(self):
        return str(self.as_array())
    def __repr__(self):
        return "{0}({1})".format(type(self).__name__,str(self))

    ## Arithmetics ##
    _numops_impl=numclass.NumClass._numops_all
    def _perform_numop(self, x, op_func, _):
        return ArrayDataColumn(op_func(self.as_array(),x))
    def _perform_numop_comp(self, x, op_func, _): # often used for indexing, so want to return plain numpy array
        return op_func(self.as_array(),x)
    
    ## External functions adding ##
    @classmethod
    def add_array_function(cls, func, alias=None, wrap_into_column=False, as_property=False, doc=None):
        """
        Turns a function into a method, which is automatically applied to the array representation.

        Arguments:
            func (callable): a function which takes the column converted into a numpy array as a first argument, and then the rest if the supplied arguments
            alias (str): the method name; by default, it's ``func.__name__``
            wrap_into_column (bool): if ``True``, the returned result is wrapped into :class:`ArrayDataColumn`
            as_property (bool): if ``True``, the function is added as a property getter instead
            doc (str): the method docstring; by default, it's ``func.__doc__``
        """
        if alias is None:
            alias=func.__name__
        if wrap_into_column:
            def self_func(self, *args, **vargs):
                return ArrayDataColumn(func(self.as_array(force_copy=False),*args,**vargs))
        else:
            def self_func(self, *args, **vargs):
                return func(self.as_array(force_copy=False),*args,**vargs)
        if doc is None:
            try:
                self_func.__doc__=func.__doc__
            except AttributeError:
                pass
        else:
            self_func.__doc__=doc
        if as_property:
            setattr(cls,alias,property(self_func))
        else:
            setattr(cls,alias,self_func)
        
IDataColumn.add_array_function(np.argsort,doc="Same as :func:`numpy.argsort`.")
IDataColumn.add_array_function(np.argmin,doc="Same as :func:`numpy.argmin`.")
IDataColumn.add_array_function(np.argmax,doc="Same as :func:`numpy.argmax`.")
IDataColumn.add_array_function(np.min,"min",doc="Same as :func:`numpy.amin`.")
IDataColumn.add_array_function(np.max,"max",doc="Same as :func:`numpy.amax`.")
IDataColumn.add_array_function(np.mean,doc="Same as :func:`numpy.mean`.")
IDataColumn.add_array_function(np.std,doc="Same as :func:`numpy.std`.")
IDataColumn.add_array_function(np.sum,doc="Same as :func:`numpy.sum`.")
IDataColumn.add_array_function(np.nonzero,doc="Same as :func:`numpy.nonzero`.")
IDataColumn.add_array_function(np.unique,doc="Same as :func:`numpy.unique`.")
IDataColumn.add_array_function(np.real,wrap_into_column=True,as_property=True,doc="Same as :func:`numpy.real`.")
IDataColumn.add_array_function(np.imag,wrap_into_column=True,as_property=True,doc="Same as :func:`numpy.imag`.")
IDataColumn.add_array_function(np.conjugate,"conjugate",wrap_into_column=True,doc="Same as :obj:`numpy.conj`.")



class WrapperDataColumn(IDataColumn):
    """
    Wraps potentially mutable column types and proxies all the requests to them.

    Used when the underlying column object can change in the runtime (e.g., to accommodate a new element type).
    """
    def __init__(self, column):
        IDataColumn.__init__(self)
        self._column=column
        
    ## Indexing ##
    def _get_item(self, idx):
        return self._column._get_item(idx)
    def _get_single_item(self, idx):
        return self._column._get_single_item(idx)
    def _set_item(self, idx, val):
        self._column=self._column._set_item(idx,val)
        return self
    def _del_item(self, idx):
        self._column=self._column._del_item(idx)
        return self
    def _add_item(self, idx, val):
        self._column=self._column._add_item(idx,val)
        return self
    insert=_add_item
    def expand(self, length):
        """
        Expand column. Usually fill with zeros, unless the column values can be auto-predicted.
        """
        self._column=self._column.expand(length)
        return self
    def subcolumn(self, idx, force_copy=False, wrap=True):
        """
        Return value(s) at `idx` as a column object.
        """
        if wrap:
            if not force_copy and indexing.covers_all(idx,self.nrows()):
                return self
            else:
                return WrapperDataColumn(self._column.subcolumn(idx,force_copy))
        else:
            self._column.subcolumn(idx,force_copy)
    ## Casting to NumPy array ##
    def as_array(self, force_copy=False):
        """
        Turn the column into a numpy array
        """
        return self._column.as_array(force_copy=force_copy)
    ## Copying ##
    def copy(self):
        return WrapperDataColumn(self._column.copy())
    ## Shape ##
    @property
    def shape(self):
        return self._column.shape
    ## Arithmetics ##
    def _test_op_impl(self, op_sym):
        return self._column._test_op_impl(op_sym)
    def _perform_numop(self, x, op_func, op_sym):
        return WrapperDataColumn(self._column._perform_numop(x,op_func,op_sym))
    
    @property
    def real(self):
        return self._column.real
    @property
    def imag(self):
        return self._column.imag
    def conjugate(self):
        """Return the complex-conjugate of the column"""
        return self._column.conjugate()

    



    
    
class IStoredDataColumn(IDataColumn):
    """
    Abstract class to distinguish data columns with stored data, as opposed to the ones with generated data.
    """
    pass
    
    
    
    
    
class ArrayDataColumn(IStoredDataColumn):
    """
    Column which stores its data in a numpy array.

    Automatically expands the stored data type (int -> float -> complex) if needed.
    """
    def __init__(self, column):
        IStoredDataColumn.__init__(self)
        self._column=np.asarray(column)
        if self._column.ndim!=1:
            raise ValueError("can't create column from {0}-dimensional object: {1}".format(self._column.ndim,column))
        
    ## Type expanding ##
    def _expand_type(self, val):
        """
        Expand the type of the stored column to accommodate `val` (``int`` < ``float`` < ``complex``).
        """
        if val.dtype>self._column.dtype:
            if not val.dtype in ["int","float","complex"]:
                raise ValueError("ArrayDataColumn doesn't support numpy arrays other than int, float or complex")
            self._column=self._column.astype(val.dtype)
    ## Indexing ##
    def _get_item(self, idx):
        idx=indexing.to_numpy_idx(idx).idx
        return self._column[idx]
    def _get_single_item(self, idx):
        return self._column[idx]
    def _set_item(self, idx, val):
        idx=indexing.to_numpy_idx(idx).idx
        val=np.asarray(val)
        self._expand_type(val)
        self._column[idx]=val
        return self
    def _del_item(self, idx):
        idx=indexing.to_list_idx(idx).idx
        self._column=np.delete(self._column,idx)
        return self
    def _add_item(self, idx, val):
        ndim,idx=indexing.to_numpy_idx(idx).tup()
        if ndim==0:
            val=np.asarray(val)
            self._expand_type(val)
            self._column=np.append(np.append(self._column[:idx],val),self._column[idx:])
        else:
            raise ValueError("can only insert item in a single location")
        return self
    ## Copying ##
    def copy(self):
        return ArrayDataColumn(self._column.copy())
    ## Shape ##
    @property
    def shape(self):
        return (len(self._column),)
    ## Arithmetics ##
    def _perform_numop_i(self, x, op_func, _):
        op_func(self._column,x)
        return self

def _dump_array_col(col, dumpf):
    return dumpf(col._column)[1]
def _load_array_col(val, loadf):
    val=loadf(("np",val))
    return ArrayDataColumn(val)
strdump.dumper.add_class(ArrayDataColumn,_dump_array_col,_load_array_col,"column.array",recursive=True)




class ListDataColumn(IStoredDataColumn):
    """
    Column which stores its data in a list.
    """
    def __init__(self, column):
        IStoredDataColumn.__init__(self)
        if isinstance(column,list):
            self._column=column
        else:
            self._column=list(column)
        
    ## Indexing ##
    def _get_sublist(self, idx):
        if indexing.is_slice(idx):
            return self._column[idx]
        else:
            return [self._column[i] for i in idx]
    def _get_item(self, idx):
        ndim,idx=indexing.to_list_idx(idx).tup()
        if ndim==0:
            return self._column[idx]
        else:
            return as_array(self._get_sublist(idx))
    def _get_single_item(self, idx):
        return self._column[idx]
    def _set_item(self, idx, val):
        ndim,idx=indexing.to_list_idx(idx).tup()
        if np.isscalar(val):
            if ndim==0:
                self._column[idx]=val
            else:
                l=len(self._column)
                if indexing.covers_all(idx,l):
                    self._column=[val]*l
                else:
                    for i in indexing.to_range(idx,l):
                        self._column[i]=val
        elif ndim==1:
            if indexing.is_slice(idx):
                self._column[idx]=val
            else:
                for i,r in enumerate(idx):
                    self._column[r]=val[i]
        else:
            raise ValueError("can't assign the value")
        return self
    def _del_item(self, idx):
        ndim,idx=indexing.to_list_idx(idx).tup()
        if ndim==0 or indexing.is_slice(idx):
            del self._column[idx]
        else:
            save=np.ones(self.nrows())
            for i in idx:
                save[i]=False
            self._column=[self._column[i] for i,s in enumerate(save) if s]
        return self
    def _add_item(self, idx, val):
        ndim,idx=indexing.to_list_idx(idx).tup()
        if np.isscalar(val):
            val=[val]
        if ndim==0:
            self._column[idx:idx]=val
        else:
            raise ValueError("can only insert item in a single location")
        return self
    def subcolumn(self, idx, force_copy=False):
        """
        Return value(s) at `idx` as a column object.
        """
        ndim,idx=indexing.to_list_idx(idx).tup()
        if not force_copy and indexing.covers_all(idx,self.nrows()):
            return self
        else:
            if ndim==0:
                return ListDataColumn([self._column[idx]])
            else:
                return ListDataColumn(self._get_sublist(idx))
    ## Casting to NumPy array ##
    def as_array(self, force_copy=False):
        """
        Turn the column into a numpy array
        """
        return as_array(self._column,force_copy=force_copy)
    ## Copying ##
    def copy(self):
        return ListDataColumn(list(self._column))
    ## Shape ##
    @property
    def shape(self):
        return (len(self._column),)
    ## Arithmetics ##
    def _perform_numop_i(self, x, op_func, _):
        self._column=[op_func(e,x) for e in self._column]
        return self
    def _perform_numop(self, x, op_func, _):
        return ListDataColumn([op_func(e,x) for e in self._column])
    ## Repr ##
    def __str__(self):
        return str(self._column)
    
    @property
    def real(self):
        return ListDataColumn([np.real(e) for e in self._column])
    @property
    def imag(self):
        return ListDataColumn([np.imag(e) for e in self._column])
    def conjugate(self):
        """Return the complex-conjugate of the column"""
        return ListDataColumn([np.conjugate(e) for e in self._column])
    
def _dump_list_col(col, dumpf):
    return dumpf(col._column)
def _load_list_col(val, loadf):
    return ListDataColumn(loadf(val))
strdump.dumper.add_class(ListDataColumn,_dump_list_col,_load_list_col,"column.list",recursive=True)
    


class LinearDataColumn(IDataColumn):
    """
    A linear data column.

    Represents a linear data (essentially, a range object). Doesn't store the full data, just the length, start and step.
    Automatically increments upon expansion.
    """
    def __init__(self, length, start=0, step=1):
        IDataColumn.__init__(self)
        self.start=start
        self.length=length
        self.step=step
        
    def _calc_item(self, idx):
        if np.any(idx>=self.length) or np.any(idx<0):
            raise IndexError("index {} is out of bounds".format(idx))
        return idx*self.step+self.start
    
    ## Indexing ##
    def _get_item(self, idx):
        ndim,idx=indexing.to_list_idx(idx).tup()
        if indexing.is_slice(idx):
            idx=np.arange(*idx.indices(self.length))
        if ndim==0:
            return self._calc_item(idx)
        else:
            return self._calc_item(np.asarray(idx))
    def _get_single_item(self, idx):
        return self._calc_item(idx)
    def _set_item(self, idx, val):
        array_column=ArrayDataColumn(self.as_array())
        array_column._set_item(idx,val)
        return array_column
    def _del_item(self, idx):
        d_idx=indexing.to_list_idx(idx)
        idx=d_idx.idx
        if indexing.is_slice(idx):
            idx=idx.indices(self.length)
            if idx[2]==-1:
                idx=(idx[1]+1,idx[0]-1,1)
            if idx[2]==1:
                if idx[0]==0:
                    self.start=self.start+self.step*idx[1]
                    self.length=self.length-(idx[1]-idx[0])
                    return self
                elif idx[1]==self.length:
                    self.length=self.length-(idx[1]-idx[0])
                    return self
        array_column=ArrayDataColumn(self.as_array())
        array_column._del_item(d_idx)
        return array_column
    def _add_item(self, idx, val):
        array_column=ArrayDataColumn(self.as_array())
        array_column._add_item(idx,val)
        return array_column
    def expand(self, length):
        """
        Expand column. Usually fill with zeros, unless the column values can be auto-predicted.
        """
        self.length=self.length+length
        return self
    def subcolumn(self, idx, force_copy=False):
        """
        Return value(s) at `idx` as a column object.
        """
        ndim,idx=indexing.to_list_idx(idx).tup()
        if force_copy:
            return IDataColumn.subcolumn(self,idx,True)
        if indexing.covers_all(idx,self.nrows()):
            return self
        if ndim==0:
            return LinearDataColumn(1,self._calc_item(idx))
        if indexing.is_slice(idx):
            indices=idx.indices(self.length)
            if (indices[1]-indices[0])%indices[2]==0:
                new_len=(indices[1]-indices[0])//indices[2]
            else:
                new_len=(indices[1]-indices[0])//indices[2]+1
            return LinearDataColumn(new_len,self._calc_item(indices[0]),self.step*indices[2])
        else:
            return IDataColumn.subcolumn(self,idx)
    ## Casting to NumPy array ##
    def as_array(self, force_copy=False):
        """
        Turn the column into a numpy array
        """
        return self._calc_item(np.arange(self.length))
    ## Copying ##
    def copy(self):
        return LinearDataColumn(self.length,self.start,self.step)
    ## Shape ##
    @property
    def shape(self):
        return (self.length,)
    ## Arithmetics ##
    _numops_perf_i={"i+","i-","i*","i/"}
    def _perform_numop_i(self, x, op_func, op_sym):
        if op_sym in self._numops_perf_i and np.isscalar(x):
            if op_sym=="i/" and not np.iscomplexobj(x): # override integer division
                x=float(x)
            new_start=op_func(self.start,x)
            new_step=op_func(self.start+self.step,x)-op_func(self.start,x)
            self.start,self.step=new_start,new_step
            return self
        return IDataColumn._perform_numop(self,x,op_func,op_sym)
    _numops_perf_lru={"l+","l-","l*","l/","r+","r-","r*","u+","u-"}
    def _perform_numop(self, x, op_func, op_sym):
        if op_sym in self._numops_perf_lru and np.isscalar(x):
            if op_sym=="l/" and not np.iscomplex(x): # override integer division
                x=float(x)
            new_start=op_func(self.start,x)
            new_step=op_func(self.start+self.step,x)-op_func(self.start,x)
            return LinearDataColumn(self.length,new_start,new_step)
        return IDataColumn._perform_numop(self,x,op_func,op_sym)
    
    @property
    def real(self):
        return LinearDataColumn(self.length,np.real(self.start),np.real(self.step))
    @property
    def imag(self):
        return LinearDataColumn(self.length,np.imag(self.start),np.imag(self.step))
    def conjugate(self):
        """Return the complex-conjugate of the column"""
        return LinearDataColumn(self.length,np.conjugate(self.start),np.conjugate(self.step))


### strdump definitions ###    
def _dump_linear_col(col):
    return col.length,col.start,col.step
def _load_linear_col(val):
    length,start,step=val
    return LinearDataColumn(length,start,step)
strdump.dumper.add_class(LinearDataColumn,_dump_linear_col,_load_linear_col,"column.linear")




def as_linear_column(column):
    """
    Try and turn a column into a linear column.

    If it is not linear, raise :exc:`ValueError`.
    """
    if len(column)==0:
        return LinearDataColumn(0)
    elif len(column)==1:
        return LinearDataColumn(1,column[0])
    else:
        column=np.asarray(column)
        diff=column[1:]-column[:-1]
        if (diff==diff[0]).all():
            return LinearDataColumn(len(column),column[0],diff[0])
        else:
            raise ValueError("column can't be represented as a linear data")
def as_column(column, force_numpy=True, try_linear=False, force_copy=False):
    """
    Turn an object into a column.

    If `column` is a list and ``force_numpy==True``, turn it into a numpy array and return :class:`ArrayDataColumn`
    (by default lists are wrapped into :class:`ListDataColumn`).
    If ``try_linear==True``, try to represent it as a linear data first.
    If ``force_copy==True``, create the copy of the data.
    """
    if isinstance(column,IDataColumn):
        if force_copy:
            return column.copy()
        else:
            return column
    else:
        if try_linear:
            try:
                return as_linear_column(column)
            except ValueError:
                pass
        if isinstance(column,list) and not force_numpy:
            if force_copy:
                return ListDataColumn(list(column))
            else:
                return ListDataColumn(column)
        else:
            return ArrayDataColumn(np.asarray(column))
        
def crange(*args):
    """
    [start,] stop[, step]

    Analogue of `range` which creates a linear data column.
    """
    start=0
    step=1
    if len(args)==1:
        stop=args[0]
    elif len(args)==2:
        start=args[0]
        stop=args[1]
    elif len(args)==3:
        start=args[0]
        stop=args[1]
        step=args[2]
    else:
        raise ValueError("crange accepts between 1 and 3 arguments")
    length=np.int(np.ceil((stop-start)/float(step)))
    return LinearDataColumn(length,start,step)
def zeros(length):
    """
    Create a column of the given length filled with zeros.
    """
    return LinearDataColumn(length,0,0)