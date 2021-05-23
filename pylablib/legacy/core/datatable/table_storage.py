"""
Data table storage.
Does not implement any indexing or iterator interface (it's delegated to `IDataTable`).
Should not be accessed directly by users of `DataTable`.
"""

from builtins import range
from ..utils.py3 import textstring

from . import indexing
from . import column
from .datatable_utils import get_shape, as_array

import numpy as np
import pandas as pd

class IDataTableStorage(object):
    def __init__(self):
        object.__init__(self)
    ## Shape ##
    @property   # property for compatibility with np.shape
    def shape(self):
        raise NotImplementedError("IDataTableStorage.shape")
    @property   # property for compatibility with np.ndim
    def ndim(self):
        return 2
    
    ## Casting to NumPy array ##
    def as_array(self, force_copy=False):
        """
        Turn the storage into a numpy array.

        If ``force_copy==True``, ensure that the result is a copy of the data.
        """
        if self.shape[1]==0:
            return np.zeros((0,0))
        if force_copy:
            return self.get_item(slice(None)).copy()
        else:
            return self.get_item(slice(None))
    def __array__(self): # property for compatibility with np.ufuncs
        return self.as_array()
    def as_pandas(self, force_copy=False):
        """
        Turn the storage into a pandas DataFrame.

        If ``force_copy==True``, ensure that the result is a copy of the data.
        """
        return pd.DataFrame(self.as_array(force_copy=False),columns=self.get_column_names(),copy=force_copy)
    ## Indexing ##
    # numpy-like; accept 1D or 2D numpy style index
    def get_item(self, idx): # ; return np.array, unless single element is accessed
        """Return the data at the index `idx` (1D or 2D) as a numpy array."""
        raise NotImplementedError("IDataTableStorage.get_item")
    def set_item(self, idx, val): # accept 1D or 2D index numpy-style 
        """Return the data at the index `idx` (1D or 2D)  to `val`."""
        raise NotImplementedError("IDataTableStorage.set_item")
    # column-wise; accept 1D index suitable for columns
    def get_columns(self, idx): # return column object  or list of column objects
        """Return a column or a list of columns at the index `idx` (1D)."""
        raise NotImplementedError("IDataTableStorage.get_columns")
    def get_single_column(self, idx): # same as get_columns, but only accept single number as an index
        """
        Return a single column at the index `idx` (1D).
        
        Same as :meth:`get_columns`, but only accepts single column index.
        """
        return self.get_columns(idx)
    def set_columns(self, idx, val): # accepts column object (or list of column objects) or iterable (or 2D iterable)
        """Set a column or a list of columns at the index `idx` (1D) to `val`."""
        raise NotImplementedError("IDataTableStorage.set_columns")
    def add_columns(self, idx, val, names, transposed, force_copy=False): # accepts column object (or list of column objects) or iterable (or 2D iterable);
        """
        Add new columns at index `idx` (1D).
        
        Columns data is given by `val` and their names are given by `names` (a string for a single column, or a list of strings for multiple columns).
        If ``transposed==True``, `val` is assumed to be arranged column-wise (list of columns).
        If ``transposed==False``, `val` is assumed to be arranged row-wise (list of rows).
        If ``transposed=="auto"``, it is assumed to be ``True`` if `val` is a 2D numpy array, and ``False`` otherwise.
        If ``force_copy==True``, make sure that `val` data is copied.
        """
        #if transposed="auto" and argument is 2D numpy array, effectively transposes it to enforce standard notation (column is second idx)
        raise NotImplementedError("IDataTableStorage.add_columns")
    def del_columns(self, idx):
        """Delete a column or a list of columns at the index `idx` (1D)"""
        raise NotImplementedError("IDataTableStorage.del_columns")
    # row-wise; accept 1D index suitable for rows
    def get_rows(self, idx): # return each row as tuple (i.e., return tuple or list of tuples) (for numpy arrays use _get_item)
        """
        Return a row or a list of rows at the index `idx` (1D).
        
        Each row is represented as a tuple.
        """
        raise NotImplementedError("IDataTableStorage.get_rows")
    def get_single_row(self, idx): # same as get_rows, but only accept single number as an index
        """
        Return a single row at the index `idx` (1D) as a tuple.
        
        Same as :meth:`get_rows`, but only accepts single column index.
        """
        return self.get_rows(idx)
    def get_single_row_item(self, idx): # same as get_item, but only accept single number as an (row) index
        """
        Return a single row at the index `idx` (1D) as a numpy array.
        
        Same as :meth:`get_item`, but only accepts single column index.
        """
        return self.get_item(idx)
    def set_rows(self, idx, val): # accepts iterable (or 2D iterable)
        """
        Set a row or a list of rows at the index `idx` (1D) to `val`.
        """
        self.set_item((idx,slice(None)),val)
    def add_rows(self, idx, val): # accepts iterable (or 2D iterable)
        """
        Add new rows at index `idx` (1D).
        """
        raise NotImplementedError("IDataTableStorage.add_rows")
    def del_rows(self, idx):
        """Delete a row or a list of rows at the index `idx` (1D)"""
        raise NotImplementedError("IDataTableStorage.del_rows")
    # table-wise
    def get_subtable(self, idx):
        """Return the data at the index `idx` (1D or 2D) as an `IDataTableStorage` object of the same type."""
        raise NotImplementedError("IDataTableStorage.get_subtable")
    def expand(self, length):
        """
        Expand the table by `length`. Usually fill with zeros, unless the column values can be auto-predicted.
        """
        raise NotImplementedError("IDataTableStorage.expand")
    
    ## Columns indexing ##
    def get_column_names(self, idx=None):
        """Return the list of column names at index `idx` (by default, all of the names)."""
        raise NotImplementedError("IDataTableStorage.get_column_names")
    def get_column_indices(self, idx=None):
        """Return the list of column numerical indices corresponding to the index `idx`."""
        raise NotImplementedError("IDataTableStorage.get_column_indices")
    def set_column_names(self, new_names):
        """Set new column names."""
        raise NotImplementedError("IDataTableStorage.change_column_name")
    def swap_columns(self, idx1, idx2):
        """Swap two columns at indices `idx1` and `idx2`."""
        raise NotImplementedError("IDataTableStorage.swap_columns")
    
    ## Copying ##
    def copy(self):
        raise NotImplementedError("IDataTableStorage.copy")
    
    ## Repr ##
    def __str__(self):
        return self.as_array().__str__()
    def __repr__(self):
        s=str(self).replace("\n ","\n"+" "*6)
        return "{0}(columns={1},\ndata={2})".format(type(self).__name__,str(self.get_column_names()),s)







    
    
    
    

class ColumnDataTableStorage(IDataTableStorage):
    """
    Table storage which stores the data as a list of columns (defined in :mod:`.datatable.column`).

    More flexible compared to the :class:`ArrayDataTableStorage`, but potentially slower.

    Args:
        columns: table data; can be a numpy array, a list of columns, or a 2D list
        names(list): list of column names; by default, the column names are autogenerated: ``"col00"``, ``"col01"``, etc.
        transposed: if ``True``, the `columns` arguments is assumed to be column-wise (list of columns)
            if ``False``, the `columns` arguments is assumed to be row-wise (list of rows)
            if ``"auto"``, assumed to be ``False`` for numpy arrays and ``True`` otherwise
        force_copy (bool): if ``True``, make sure that the supplied data is copied
    """
    def __init__(self, columns=None, names=None, transposed="auto", force_copy=True):
        IDataTableStorage.__init__(self)
        self._columns=[]
        self._column_names=[]
        self._column_uid=0
        if columns is not None:
            self.add_columns(0,columns,names,transposed=transposed,force_copy=force_copy)
    
    ## Shape ##
    @property
    def shape(self):
        ncols=len(self._columns)
        if ncols==0:
            return (0,0)
        else:
            return (len(self._columns[0]),ncols)
    def _added_shape_valid(self, shape, direction="column"):
        """
        Check if adding data doesn't violate shape rectangleness.
        direction can be "column" or "row".
        """
        if self.shape[1]==0:
            return True
        else:
            if direction=="column":
                return self.shape[0]==shape[0]
            else:
                return self.shape[1]==shape[1]

    def as_pandas(self, force_copy=False):
        """
        Turn the storage into a pandas DataFrame.

        If ``force_copy==True``, ensure that the result is a copy of the data.
        """
        columns=[]
        for c in self._columns:
            if isinstance(c,column.ListDataColumn):
                c=c._column
            else:
                c=c.as_array(force_copy=False)
            columns.append(c)
        columns=dict(zip(self.get_column_names(),columns))
        return pd.DataFrame(columns,columns=self.get_column_names(),copy=force_copy)
    
    ## Columns indexing ##
    def get_column_names(self, idx=None):
        """Return the list of column names."""
        if idx is None:
            return self._column_names
        else:
            ndim,idx=indexing.to_list_idx_noslice(idx,self._column_names).tup()
            if ndim==0:
                return self._column_names[idx]
            else:
                return [self._column_names[i] for i in idx]
    def get_column_indices(self, idx=None):
        """Return the list of column numerical indices corresponding to the index `idx`."""
        if idx is None:
            return list(range(len(self._columns)))
        else:
            return indexing.to_list_idx_noslice(idx,self._column_names).idx
    def set_column_names(self, new_names):
        """Set new column names."""
        if len(new_names)!=len(self._columns):
            raise ValueError("wrong number of column names: expected {0}, got {1}".format(len(self._columns),len(new_names)))
        self._check_name_clashes(new_names,adding=False)
        self._column_names=new_names
    def swap_columns(self, idx1, idx2):
        """Swap two columns at indices `idx1` and `idx2`."""
        ndim1,idx1=indexing.to_list_idx_noslice(idx1,self.get_column_names()).tup()
        ndim2,idx2=indexing.to_list_idx_noslice(idx2,self.get_column_names()).tup()
        if ndim1!=0 or ndim2!=0:
            raise ValueError("Can only swap one pair at a time")
        self._column_names[idx1],self._column_names[idx2]=self._column_names[idx2],self._column_names[idx1]
        self._columns[idx1],self._columns[idx2]=self._columns[idx2],self._columns[idx1]
        
    def _check_name_clashes(self, names, adding=True):
        if isinstance(names,textstring):
            names=[names]
        for i,n in enumerate(names): # check collisions in the supplied array
            if n in names[i+1:]:
                raise KeyError("duplicate column name: {0}".format(n))
        if adding: # check collisions with the current columns
            for n in names:
                try:
                    indexing.string_list_idx(n,self._column_names,only_exact=True)
                except KeyError:
                    continue
                raise KeyError("duplicate column name: {0}".format(n))
    def _gen_unique_name(self):
        while True:
            name="col{:02}".format(self._column_uid)
            self._column_uid=self._column_uid+1
            try:
                self._check_name_clashes(name,adding=True)
                return name
            except KeyError:
                pass
    ## Copying ##
    def copy(self):
        return ColumnDataTableStorage([c.copy() for c in self._columns],list(self._column_names))
    
    ## Column modification ##
    def _set_item_column(self, c_idx, r_idx, val):
        self._columns[c_idx]=self._columns[c_idx]._set_item(r_idx,val)
    def _add_item_column(self, c_idx, r_idx, val):
        self._columns[c_idx]=self._columns[c_idx]._add_item(r_idx,val)
    
    
    ## Indexing ##
    ## numpy-like return type ##
    def get_item(self, idx):
        """Return the data at the index `idx` (1D or 2D) as a numpy array."""
        if not self._columns:
            raise IndexError("no columns in the table")
        r_idx,c_idx=indexing.to_double_index(idx,self.get_column_names())
        c_ndim,c_idx=c_idx.tup()
        if c_ndim==0:
            return self._columns[c_idx][r_idx.idx]
        else:
            if r_idx.ndim==0:
                return np.array([self._columns[c][r_idx] for c in c_idx])
            else:
                return np.column_stack([self._columns[c][r_idx] for c in c_idx])
    def set_item(self, idx, val):
        """Return the data at the index `idx` (1D or 2D) to `val`."""
        if not self._columns:
            raise IndexError("no columns in the table")
        r_idx,c_idx=indexing.to_double_index(idx,self.get_column_names())
        c_ndim,c_idx=c_idx.tup()
        v_shape=get_shape(val)
        v_ndim=len(v_shape)
        if v_ndim==0:
            if c_ndim==0:
                self._set_item_column(c_idx,r_idx,val)
            else:
                for c in c_idx:
                    self._set_item_column(c,r_idx,val)
        elif v_ndim==1:
            if c_ndim==0:
                if r_idx.ndim==0:
                    raise ValueError("can't assign array to element")
                else:
                    self._set_item_column(c_idx,r_idx,val)
            else:
                if v_shape[0]!=len(c_idx):
                    raise ValueError("wrong dimension of assigned value")
                for i,c in enumerate(c_idx):
                    self._set_item_column(c,r_idx,val[i])
        elif v_ndim==2:
            if c_ndim*r_idx.ndim!=1:
                raise ValueError("can't assign array to element")
            else:
                if isinstance(val,list):
                    for i,c in enumerate(c_idx):
                        self._set_item_column(c,r_idx, [val[r][i] for r in range(len(val))] )
                else:
                    for i,c in enumerate(c_idx):
                        self._set_item_column(c,r_idx,val[:,i])
        else:
            raise ValueError("can't assign multidimensional arrays with d>2")
        
    ## column-wise ##
    def get_columns(self, idx): # return column object  or list of column objects
        """Return a column or a list of columns at the index `idx` (1D)."""
        ndim,idx=indexing.to_list_idx_noslice(idx,self.get_column_names()).tup()
        if ndim==0:
            return self._columns[idx]
        else:
            return [self._columns[i] for i in idx]
    def get_single_column(self, idx):
        """
        Return a single column at the index `idx` (1D).
        
        Same as :meth:`get_columns`, but only accepts single column index.
        """
        return self._columns[idx]
    def set_columns(self, idx, val, force_copy=False): # accepts column object (or list of column objects) or iterable (or 2D iterable)
        """Set a column or a list of columns at the index `idx` (1D) to `val`."""
        c_ndim,idx=indexing.to_list_idx_noslice(idx,self.get_column_names()).tup()
        v_shape=get_shape(val)
        v_ndim=len(v_shape)
        if v_ndim==0:
            if c_ndim==0:
                self._columns[idx][:]=val
            else:
                for c in idx:
                    self._columns[c][:]=val
        elif v_ndim==1:
            if not self._added_shape_valid((v_shape[0],1)):
                raise ValueError("wrong length for the new columns")
            if c_ndim==0:
                self._columns[idx]=column.as_column(val,False,force_copy=force_copy)
            else:
                val=column.as_column(val,False,force_copy=force_copy)
                if len(idx)>0:
                    self._columns[idx[0]]=val
                    for c in idx[:-1]:
                        self._columns[c]=val.copy()
        elif v_ndim==2:
            if not self._added_shape_valid(v_shape[::-1]):
                raise ValueError("wrong length for the new columns")
            if c_ndim==0:
                raise ValueError("can't assign array to element")
            else:
                for i,c in enumerate(idx):
                    self._columns[c]=column.as_column(val[i],False,force_copy=force_copy)
        else:
            raise ValueError("can't assign multidimensional arrays with d>2")
    def add_columns(self, idx, val, names, transposed="auto", force_copy=False): # accepts column object (or list of column objects) or iterable (or 2D iterable)
        """
        Add new columns at index `idx` (1D).
        
        Columns data is given by `val` and their names are given by `names` (a string for a single column, or a list of strings for multiple columns).
        If ``transposed==True``, `val` is assumed to be arranged column-wise (list of columns).
        If ``transposed==False``, `val` is assumed to be arranged row-wise (list of rows).
        If ``transposed=="auto"``, it is assumed to be ``False`` if `val` is a 2D numpy array, and ``True`` otherwise.
        If ``force_copy==True``, make sure that `val` data is copied.
        """
        c_ndim,idx=indexing.to_list_idx_noslice(idx,self.get_column_names()).tup()
        if c_ndim==1:
            raise ValueError("can only insert items in a single location")
        if isinstance(names,textstring) or names is None:
            names=[names]
        v_shape=get_shape(val)
        v_ndim=len(v_shape)
        if v_ndim==0:
            if len(self._columns)==0:
                raise ValueError("can't add number to an empty table")
            else:
                try:
                    val+0
                    val=[column.LinearDataColumn(self.shape[0],val,0) for _ in names] # duplicate for several new columns
                except TypeError: #non-numeric val; create list column instead
                    val=[column.ListDataColumn([val]*self.shape[0]) for _ in names]
                v_shape=(len(val),self.shape[0])
        elif v_ndim==1:
            if (transposed=="auto" and len(self._columns)==0 and len(names)==len(val)) or (transposed==True): # row is supplied
                val=[column.as_column([v],False,force_copy=force_copy) for v in val]
                v_shape=(v_shape[0],1)
            else:
                val=[column.as_column(val,False,force_copy=force_copy) for _ in names] # duplicate for several new columns
                v_shape=(len(names),v_shape[0])
        elif v_ndim==2:
            if transposed=="auto":
                transposed=(isinstance(val,list) or isinstance(val,tuple))
            if transposed:
                val=[column.as_column(c,False,force_copy=force_copy) for c in val]
            else:
                v_shape=(v_shape[::-1])
                if isinstance(val,np.ndarray):
                    val=[column.as_column(val[:,c],False,force_copy=force_copy) for c in range(v_shape[0])]
                else:
                    val=[column.as_column( [val[r][c] for r in range(v_shape[1])] ,False,force_copy=force_copy) for c in range(v_shape[0])]
        else:
            raise ValueError("can't assign multidimensional arrays with d>2")
        if not self._added_shape_valid(v_shape[::-1]):
            raise ValueError("invalid shape of added columns")
        if names==[None]:
            names=[self._gen_unique_name() for _ in range(len(val))]
        if len(names)!=len(val):
            raise ValueError("invalid column names number: expected {0}, got {1}".format(len(val),len(names)))
        self._check_name_clashes(names,adding=True)
        self._columns[idx:idx]=val
        self._column_names[idx:idx]=names
    def del_columns(self, idx):
        """Delete a column or a list of columns at the index `idx` (1D)"""
        ndim,idx=indexing.to_list_idx_noslice(idx,self.get_column_names()).tup()
        if ndim==0:
            idx=[idx]
        cols=[c for c in range(len(self._columns)) if not (c in idx)]
        self._columns=[self._columns[c] for c in cols]
        self._column_names=[self._column_names[c] for c in cols]
        
    ## row-wise ##
    def get_rows(self, idx): # return each row as tuple (i.e., return tuple or list of tuples) (for numpy arrays use _get_item)
        """
        Return a row or a list of rows at the index `idx` (1D).
        
        Each row is represented as a tuple.
        """
        if not self._columns:
            raise IndexError("no columns in the table")
        r_idx=indexing.to_numpy_idx(idx)
        if r_idx.ndim==0:
            return tuple([c[r_idx] for c in self._columns])
        else:
            cols=[c[r_idx] for c in self._columns]
            return zip(*cols)
    def get_single_row(self, idx): # same as get_rows, but only accept single number as an index
        """
        Return a single row at the index `idx` (1D) as a tuple.
        
        Same as :meth:`get_rows`, but only accepts single column index.
        """
        if not self._columns:
            raise IndexError("no columns in the table")
        return tuple([c._get_single_item(idx) for c in self._columns])
    def get_single_row_item(self, idx): # same as get_item, but only accept single number as an (row) index
        """
        Return a single row at the index `idx` (1D) as a numpy array.
        
        Same as :meth:`get_item`, but only accepts single column index.
        """
        if not self._columns:
            raise IndexError("no columns in the table")
        return as_array([c._get_single_item(idx) for c in self._columns])
    def add_rows(self, idx, val): # accepts iterable (or 2D iterable)
        """
        Add new rows at index `idx` (1D).
        """
        if not self._columns:
            raise IndexError("no columns in the table")
        r_idx=indexing.to_numpy_idx(idx)
        if r_idx.ndim==1:
            raise ValueError("can only insert items in a single location")
        v_shape=get_shape(val)
        v_ndim=len(v_shape)
        if v_ndim==0:
            val=[[val]*len(self._columns)]
            v_shape=(1,len(val))
        elif v_ndim==1:
            val=[val]
            v_shape=(1,v_shape[0])
        elif v_ndim!=2:
            raise ValueError("can't assign multidimensional arrays with d>2")
        if not self._added_shape_valid(v_shape,"row"):
            raise ValueError("invalid shape of added rows")
        if isinstance(val,list):
            for c in range(len(self._columns)):
                self._add_item_column(c,r_idx,[val[r][c] for r in range(len(val))] )
        else:
            for c in range(len(self._columns)):
                self._add_item_column(c,r_idx,val[:,c])
    def del_rows(self, idx):
        """Delete a row or a list of rows at the index `idx` (1D)"""
        if not self._columns:
            raise IndexError("no columns in the table")
        r_idx=indexing.to_numpy_idx(idx)
        self._columns=[c._del_item(r_idx) for c in self._columns]
        
    # table-wise
    def get_subtable(self, idx, force_copy=False):
        """Return the data at the index `idx` (1D or 2D) as an `IDataTableStorage` object of the same type."""
        if not self._columns:
            raise IndexError("no columns in the table")
        r_idx,c_idx=indexing.to_double_index(idx,self.get_column_names())
        c_ndim,c_idx=c_idx.tup()
        if c_ndim==0:
            c_idx=[c_idx]
        new_column_names=[self._column_names[c] for c in c_idx]
        new_columns=[self._columns[c].subcolumn(r_idx,force_copy=force_copy) for c in c_idx]
        return ColumnDataTableStorage(new_columns, new_column_names)
    
    def expand(self, length):
        """
        Expand the table. Usually fill with zeros, unless the column values can be auto-predicted.
        """
        self._columns=[c.expand(length) for c in self._columns]


    ## Repr ##
    def __str__(self):
        try:
            return self.as_array().__str__()
        except ValueError: # complicated shape
            return str([ list(self.get_rows(r)) for r in range(self.shape[0]) ])
        










class ArrayDataTableStorage(IDataTableStorage):
    """
    Table storage which stores the data as a 2D numpy array.

    Faster, but less flexible than :class:`ColumnDataTableStorage`.
    Indexing is only numpy-style or column-wise.
    All columns have the same datatype and are stored in the same array.
    All columns and rows are returned as numpy arrays.

    Args:
        columns: table data; can be a numpy array, a list of columns, or a 2D list
        names(list): list of column names; by default, the column names are autogenerated: ``"col00"``, ``"col01"``, etc.
        transposed: if ``True``, the `columns` arguments is assumed to be column-wise (list of columns)
            if ``False``, the `columns` arguments is assumed to be row-wise (list of rows)
            if ``"auto"``, assumed to be ``False`` for numpy arrays and ``True`` otherwise
        force_copy (bool): if ``True``, make sure that the supplied data is copied
    """
    def __init__(self, columns=None, names=None, transposed="auto", force_copy=True):
        IDataTableStorage.__init__(self)
        self._data=None
        self._column_names=[]
        self._column_uid=0
        if columns is not None:
            self.add_columns(0,columns,names,transposed=transposed,force_copy=force_copy)
    
    ## Shape ##
    @property
    def shape(self):
        if self._data is None:
            return (0,0)
        else:
            return self._data.shape
    def _added_shape_valid(self, shape, direction="column"):
        """
        Check if adding data doesn't violate shape rectangleness.
        direction can be "column" or "row".
        """
        if self.shape[0]==0:
            return True
        else:
            if direction=="column":
                return self.shape[0]==shape[0]
            else:
                return self.shape[0]==shape[1]
    
    ## Columns indexing ##
    def get_column_names(self, idx=None):
        """Return the list of column names."""
        if idx is None:
            return self._column_names
        else:
            ndim,idx=indexing.to_list_idx_noslice(idx,self._column_names).tup()
            if ndim==0:
                return self._column_names[idx]
            else:
                return [self._column_names[i] for i in idx]
    def get_column_indices(self, idx=None):
        """Return the list of column numerical indices corresponding to the index `idx`."""
        if idx is None:
            return list(range(len(self._column_names)))
        else:
            return indexing.to_list_idx_noslice(idx,self._column_names).idx
    def set_column_names(self, new_names):
        """Set new column names."""
        if len(new_names)!=self.shape[1]:
            raise ValueError("wrong number of column names")
        self._check_name_clashes(new_names)
        self._column_names=new_names
    def swap_columns(self, idx1, idx2):
        """Swap two columns at indices `idx1` and `idx2`."""
        ndim1,idx1=indexing.to_list_idx_noslice(idx1,self.get_column_names()).tup()
        ndim2,idx2=indexing.to_list_idx_noslice(idx2,self.get_column_names()).tup()
        if ndim1!=0 or ndim2!=0:
            raise ValueError("Can only swap one pair at a time")
        self._column_names[idx1],self._column_names[idx2]=self._column_names[idx2],self._column_names[idx1]
        self._data[:,idx1],self._data[:,idx2]=self._data[:,idx2].copy(),self._data[:,idx1].copy()
        
    def _check_name_clashes(self, names, adding=True):
        if isinstance(names,textstring):
            names=[names]
        for i,n in enumerate(names): # check collisions in the supplied array
            if n in names[i+1:]:
                raise KeyError("duplicate column name: {0}".format(n))
        if adding: # check collisions with the current columns
            for n in names:
                try:
                    indexing.string_list_idx(n,self._column_names,only_exact=True)
                except KeyError:
                    continue
                raise KeyError("duplicate column name: {0}".format(n))
    def _gen_unique_name(self):
        while True:
            name="col{:02}".format(self._column_uid)
            self._column_uid=self._column_uid+1
            try:
                self._check_name_clashes(name)
                return name
            except KeyError:
                pass
            
    ## Copying ##
    def copy(self):
        return ArrayDataTableStorage(self._data.copy(),list(self._column_names))
    
    ## Type expanding ##
    def _expand_type(self, val):
        """
        Expand type of stored column to accommodate value (int < float < complex).
        """
        if val.dtype>self._data.dtype:
            if not val.dtype in ["int","float","complex"]:
                raise ValueError("don't support numpy arrays other than int, float or complex")
            self._data=self._data.astype(val.dtype)
    ## Indexing ##
    def _to_column_index(self, idx):
        if isinstance(idx,textstring) or (isinstance(idx,list) and isinstance(idx[0],textstring)):
            return indexing.string_list_idx(idx,self.get_column_names())
        if isinstance(idx,slice) and (isinstance(idx.start,textstring) or isinstance(idx.stop,textstring)):
            start_stop=indexing.string_list_idx([idx.start,idx.stop],self.get_column_names())
            return slice(start_stop[0],start_stop[1],idx.step)
        return None
    ## numpy like ##
    def get_item(self, idx):
        """Return the data at the index `idx` (1D or 2D) as a numpy array."""
        column_idx=self._to_column_index(idx)
        if column_idx is None:
            return self._data[idx]
        else:
            return self._data[:,column_idx]
    def set_item(self, idx, val):
        """Return the data at the index `idx` (1D or 2D) to `val`."""
        val=as_array(val)
        self._expand_type(val)
        column_idx=self._to_column_index(idx)
        if column_idx is None:
            self._data[idx]=val
        else:
            self._data[:,column_idx]=val
    ## column-wise ##
    def get_columns(self, idx):
        """Return a column or a list of columns at the index `idx` (1D)."""
        column_idx=self._to_column_index(idx)
        if column_idx is not None:
            idx=column_idx
        res=self._data[:,idx]
        if res.ndim==1:
            return column.ArrayDataColumn(res)
        else:
            return [ column.ArrayDataColumn(res[:,i]) for i in range(res.shape[1]) ]
    def get_single_column(self, idx):
        """
        Return a single column at the index `idx` (1D).
        
        Same as :meth:`get_columns`, but only accepts single column index.
        """
        return self._data[:,idx]
    def set_columns(self, idx, val, force_copy=False):
        """Set a column or a list of columns at the index `idx` (1D) to `val`."""
        force_copy # unused
        val=as_array(val)
        self._expand_type(val)
        column_idx=self._to_column_index(idx)
        if column_idx is None:
            self._data[:,idx]=val
        else:
            self._data[:,column_idx]=val
    def add_columns(self, idx, val, names, transposed="auto", force_copy=False): # accepts column object (or list of column objects) or iterable (or 2D iterable)
        """
        Add new columns at index `idx` (1D).
        
        Columns data is given by `val` and their names are given by `names` (a string for a single column, or a list of strings for multiple columns).
        If ``transposed==True``, `val` is assumed to be arranged column-wise (list of columns).
        If ``transposed==False``, `val` is assumed to be arranged row-wise (list of rows).
        If ``transposed=="auto"``, it is assumed to be ``True`` if `val` is a 2D numpy array, and ``False`` otherwise.
        If ``force_copy==True``, make sure that `val` data is copied.
        """
        if (not np.isscalar(idx)) or isinstance(idx,slice):
            raise ValueError("can only insert items in a single location")
        column_idx=self._to_column_index(idx)
        if column_idx is not None:
            idx=column_idx
        if isinstance(names,textstring) or names is None:
            names=[names]
        v_ndim=np.ndim(val)
        if v_ndim==0:
            if self.shape[1]==0:
                raise ValueError("can't add number to an empty table")
            else:
                val=np.zeros((self.shape[0],len(names)))+val
        elif v_ndim==1:
            val=np.expand_dims(as_array(val),len(names))
        elif v_ndim==2:
            if transposed=="auto":
                transposed=(isinstance(val,list) or isinstance(val,tuple))
            if transposed:
                val=as_array(val).transpose()
            else:
                val=as_array(val)
        else:
            raise ValueError("can't assign multidimensional arrays with d>2")
        if not self._added_shape_valid(val.shape):
            raise ValueError("invalid shape of added columns")
        if names==[None]:
            names=[self._gen_unique_name() for _ in range(val.shape[1])]
        if len(names)!=val.shape[1]:
            raise ValueError("invalid column names number")
        self._check_name_clashes(names,adding=True)
        if self._data is None:
            if force_copy:
                self._data=val.copy()
            else:
                self._data=val
        else:
            self._data=np.concatenate((self._data[:,:idx],val,self._data[:,idx:]),axis=1)
        self._column_names[idx:idx]=names
    def del_columns(self, idx):
        """Delete a column or a list of columns at the index `idx` (1D)"""
        column_idx=self._to_column_index(idx)
        if column_idx is not None:
            idx=column_idx
        if indexing.is_slice(idx):
            idx=indexing.to_range(idx,self.shape[1])
        if np.isscalar(idx):
            idx=[idx]
        self._data=np.delete(self._data,idx,axis=1)
        self._column_names=[c for i,c in enumerate(self._column_names) if not i in idx]
    ## row-wise ##
    get_rows=get_item
    def get_single_row(self, idx): # same as get_rows, but only accept single number as an index
        """
        Return a single row at the index `idx` (1D) as a tuple.
        
        Same as :meth:`get_rows`, but only accepts single column index.
        """
        return self._data[idx]
    def get_single_row_item(self, idx): # same as get_item, but only accept single number as an (row) index
        """
        Return a single row at the index `idx` (1D) as a numpy array.
        
        Same as :meth:`get_item`, but only accepts single column index.
        """
        return self._data[idx]
    def add_rows(self, idx, val): # accepts iterable (or 2D iterable)
        """
        Add new rows at index `idx` (1D).
        """
        if (not np.isscalar(idx)) or isinstance(idx,slice):
            raise ValueError("can only insert items in a single location")
        v_ndim=np.ndim(val)
        if v_ndim==0:
            if self.shape[1]==0:
                raise ValueError("can't add number to an empty table")
            else:
                val=np.zeros((1,self.shape[1]))+val
        elif v_ndim==1:
            val=np.expand_dims(as_array(val),0)
        elif v_ndim==2:
            val=as_array(val)
        else:
            raise ValueError("can't assign multidimensional arrays with d>2")
        if self._data is None:
            self._data=val
        else:
            self._data=np.concatenate((self._data[:idx,:],val,self._data[idx:,:]),axis=0)
    def del_rows(self, idx):
        """Delete a row or a list of rows at the index `idx` (1D)"""
        self._data=np.delete(self._data,idx,axis=0)
        
    # table-wise
    def get_subtable(self, idx, force_copy=True):
        """Return the data at the index `idx` (1D or 2D) as an `IDataTableStorage` object of the same type."""
        force_copy # unused
        r_idx,c_idx=indexing.to_double_index(idx,self.get_column_names())
        c_ndim,c_idx=c_idx.tup()
        r_idx=r_idx.idx
        if c_ndim==0:
            c_idx=[c_idx]
        new_column_names=[self._column_names[c] for c in c_idx]
        new_columns=np.column_stack([self._data[:,c][r_idx] for c in c_idx])
        return ArrayDataTableStorage(new_columns, new_column_names)
    
    def expand(self, length):
        """
        Expand the table. Usually fill with zeros, unless the column values can be auto-predicted.
        """
        if self.shape[1]!=0:
            self.add_rows(self.shape[0],np.zeros((length,self.shape[1])))