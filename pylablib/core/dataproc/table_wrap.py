"""
Utilities for uniform treatment of pandas tables and numpy arrays for functions which can deal with them both.
"""

from ..utils.general import AccessIterator
from ..utils.array_utils import get_shape
from ..utils.indexing import ListIndex

import numpy as np
import pandas as pd


class IGenWrapper:
    """
    The interface for a wrapper that gives a uniform access to basic methods of wrapped objects'.
    """
    def __init__(self, container):
        self.cont=container
    def __getitem__(self, idx):
        return self.cont[idx]
    def __setitem__(self, idx, val):
        self.cont[idx]=val
    def __iter__(self):
        return self.cont.__iter__()
    def get_type(self):
        """Get a string representing the wrapped object type"""
        raise NotImplementedError("IGenWrapper.get_type")
    def copy(self, wrapped=False):
        """
        Copy the object.
        
        If ``wrapped==True``, return a new wrapper containing the object copy; otherwise, just return the copy.
        """
        raise NotImplementedError("IGenWrapper.copy")
    def ndim(self):
        return self.cont.ndim
    def shape(self):
        return self.cont.shape
    def __len__(self):
        return self.shape()[0]
    
    
class I1DWrapper(IGenWrapper):
    """
    A wrapper containing a 1D object (a 1D numpy array or a pandas Series object).

    Provides a uniform access to basic methods of a wrapped object.
    """
    def __init__(self, container):
        IGenWrapper.__init__(self,container)
        self.r=self.Accessor(self)
        self.t=self.Accessor(self)
    class Accessor:
        """
        An accessor: creates a simple uniform interface to treat the wrapped object element-wise (get/set/iterate over elements).

        Generated automatically for each table on creation, doesn't need to be created explicitly.
        """
        def __init__(self, wrapper):
            self._wrapper=wrapper
        def __iter__(self):
            return self._wrapper.__iter__()
        def __getitem__(self, idx):
            return self._wrapper.subcolumn(idx)
        def __setitem__(self, idx, val):
            self._wrapper[idx]=val
    def subcolumn(self, idx, wrapped=False):
        """
        Return a subcolumn at index `idx`.

        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        raise NotImplementedError("I1DWrapper.subtable")
    @staticmethod
    def from_array(array, index=None, force_copy=False, wrapped=False):
        """
        Build a new object of the type corresponding to the wrapper from the supplied `array` (a 1D numpy array or a list).

        If ``force_copy==True``, make a copy of supplied array.
        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        raise NotImplementedError("I1DWrapper.from_array")
    @classmethod
    def from_columns(cls, columns, column_names=None, index=None, wrapped=False):  # pylint: disable=unused-argument
        """
        Build a new object of the type corresponding to the wrapper from the supplied `columns` (a list of columns; only length-1 lists is supported).

        `column_names` parameter is ignored.
        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        if len(columns)!=1:
            raise ValueError("Array1DWrapper only supports single columns, got {} columns".format(len(columns)))
        return cls.from_array(columns[0],index=index,wrapped=wrapped)
    def array_replaced(self, array, force_copy=False, preserve_index=False, wrapped=False):  # pylint: disable=unused-argument
        """
        Return a copy of the column with the data replaced by `array`.

        All of the parameters are the same as in :meth:`from_array`.
        """
        return self.from_array(array,index=self.get_index() if preserve_index else None,force_copy=force_copy,wrapped=wrapped)
    def get_index(self):
        """Get index of the given 1D trace, or ``None`` if none is available"""
        return None
    def get_type(self):
        """Get a string representing the wrapped object type"""
        raise NotImplementedError("I1DWrapper.get_type")
    def copy(self, wrapped=False):
        """
        Copy the object.
        
        If ``wrapped==True``, return a new wrapper containing the object copy; otherwise, just return the copy.
        """
        raise NotImplementedError("I1DWrapper.copy")
    def ndim(self):
        return 1
    
class Array1DWrapper(I1DWrapper):
    """
    A wrapper for a 1D numpy array.

    Provides a uniform access to basic methods of a wrapped object.
    """
    def __init__(self, container):
        container=np.asarray(container)
        if container.ndim!=1:
            raise ValueError("Array1DWrapper only supports 1D arrays, got {}D array".format(container.ndim))
        I1DWrapper.__init__(self,container)
    
    def get_deleted(self, idx, wrapped=False):
        """
        Return a copy of the column with the data at index `idx` deleted.

        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        new_cont=np.delete(self.cont,idx,axis=0)
        return Array1DWrapper(new_cont) if wrapped else new_cont
    def __delitem__(self, idx):
        self.cont=self.get_deleted(idx)
    def get_inserted(self, idx, val, wrapped=False):
        """
        Return a copy of the column with the data `val` added at index `idx`.
        
        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        new_cont=np.insert(self.cont,idx,val,axis=0)
        return Array1DWrapper(new_cont) if wrapped else new_cont
    def insert(self, idx, val):
        """Add data `val` to index `idx`"""
        self.cont=self.get_inserted(idx,val)
    def get_appended(self, val, wrapped=False):
        """
        Return a copy of the column with the data `val` appended at the end.
        
        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        new_cont=np.append(self.cont,val,axis=0)
        return Array1DWrapper(new_cont) if wrapped else new_cont
    def append(self, val):
        """Append data `val` to the end"""
        self.cont=self.get_appended(val)
    def subcolumn(self, idx, wrapped=False):
        """
        Return a subcolumn at index `idx`.

        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        return Array1DWrapper(self.cont[idx]) if wrapped else self.cont[idx]
    @staticmethod
    def from_array(array, index=None, force_copy=False, wrapped=False):
        """
        Build a new object of the type corresponding to the wrapper from the supplied `array` (a 1D numpy array or a list).

        If ``force_copy==True``, make a copy of supplied array.
        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        new_cont=np.array(array) if force_copy else np.asarray(array)
        return Array1DWrapper(new_cont) if wrapped else new_cont
    def get_type(self):
        """Get a string representing the wrapped object type"""
        return "1d.array"
    def copy(self, wrapped=False):
        """
        Copy the object.
        
        If ``wrapped==True``, return a new wrapper containing the object copy; otherwise, just return the copy.
        """
        new_cont=self.cont.copy()
        return Array1DWrapper(new_cont) if wrapped else new_cont
    

class Series1DWrapper(I1DWrapper):
    """
    A wrapper for a pandas Series object.

    Provides a uniform access to basic methods of a wrapped object.
    """
    def __init__(self, container):
        if not isinstance(container,pd.Series):
            container=pd.Series(container)
        I1DWrapper.__init__(self,container)
    
    def __getitem__(self, idx):
        return self.cont.iloc[idx]
    def __setitem__(self, idx, val):
        self.cont.iloc[idx]=val
    def get_deleted(self, idx, wrapped=False):
        """
        Return a copy of the column with the data at index `idx` deleted.

        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        new_cont=self.cont.drop(self.cont.index[idx])
        return Series1DWrapper(new_cont) if wrapped else new_cont
    def __delitem__(self, idx):
        self.cont.drop(self.cont.index[idx],inplace=True)
    def get_inserted(self, idx, val, wrapped=False):
        """
        Return a copy of the column with the data `val` added at index `idx`.
        
        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        new_cont=pd.concat([self.cont.iloc[:idx],pd.Series(val,copy=False),self.cont.iloc[idx:]])
        return Series1DWrapper(new_cont) if wrapped else new_cont
    def get_appended(self, val, wrapped=False):
        """
        Return a copy of the column with the data `val` appended at the end.
        
        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        new_cont=self.cont.append(val)
        return Series1DWrapper(new_cont) if wrapped else new_cont
    def subcolumn(self, idx, wrapped=False):
        """
        Return a subcolumn at index `idx`.

        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        return Series1DWrapper(self.cont.iloc[idx]) if wrapped else self.cont.iloc[idx]
    @staticmethod
    def from_array(array, index=None, force_copy=False, wrapped=False):
        """
        Build a new object of the type corresponding to the wrapper from the supplied `array` (a 1D numpy array or a list).

        If ``force_copy==True``, make a copy of supplied array.
        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        new_cont=pd.Series(array,index=index,copy=force_copy)
        return Series1DWrapper(new_cont) if wrapped else new_cont
    def get_index(self):
        """Get index of the given 1D trace, or ``None`` if none is available"""
        return self.cont.index
    def get_type(self):
        """Get a string representing the wrapped object type"""
        return "1d.series"
    def copy(self, wrapped=False):
        """
        Copy the object.
        
        If ``wrapped==True``, return a new wrapper containing the object copy; otherwise, just return the copy.
        """
        new_cont=self.cont.copy()
        return Series1DWrapper(new_cont) if wrapped else new_cont
    
    
    
    
    
    
class I2DWrapper(IGenWrapper):
    """
    A wrapper containing a 2D object (a 2D numpy array or a pandas DataFrame object).

    Provides a uniform access to basic methods of a wrapped object.
    """
    def __init__(self, container, r=None, c=None, t=None):
        IGenWrapper.__init__(self,container)
        self.r=r
        self.c=c
        self.t=t
    @classmethod
    def from_columns(cls, columns, column_names=None, index=None, wrapped=False):
        """
        Build a new object of the type corresponding to the wrapper from the supplied `columns` (a list of columns).

        `column_names` supplies names of the columns (only relevant for :class:`DataFrame2DWrapper`).
        If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
        """
        raise NotImplementedError("I2DWrapper.from_columns")
    def columns_replaced(self, columns, preserve_index=False, wrapped=False):
        """
        Return copy of the object with the data replaced by `columns`.
        
        If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
        """
        return self.from_columns(columns,self.c.get_names(),index=self.get_index() if preserve_index else None,wrapped=wrapped)
    @staticmethod
    def from_array(array, column_names=None, index=None, force_copy=False, wrapped=False):
        """
        Build a new object of the type corresponding to the wrapper from the supplied `array` (a list of rows or a 2D numpy array).

        `column_names` supplies names of the columns (only relevant for :class:`DataFrame2DWrapper`).
        If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
        """
        raise NotImplementedError("I2DWrapper.from_array")
    def array_replaced(self, array, preserve_index=None, force_copy=False, wrapped=False):
        """
        Return a copy of the column with the data replaced by `array`.

        All of the parameters are the same as in :meth:`from_array`.
        """
        return self.from_array(array,self.c.get_names(),index=self.get_index() if preserve_index else None,force_copy=force_copy,wrapped=wrapped)
    def get_index(self):
        """Get index of the given 2D table, or ``None`` if none is available"""
        return None
    def get_type(self):
        """Get a string representing the wrapped object type"""
        raise NotImplementedError("I2DWrapper.get_type")
    def copy(self, wrapped=False):
        """
        Copy the object.
        
        If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
        """
        raise NotImplementedError("I2DWrapper.copy")
    def column(self, idx, wrapped=False):
        """
        Get a column at index `idx`.

        Return a 1D numpy array for a 2D numpy array object, and an Series object for a pandas DataFrame.
        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        raise NotImplementedError("I2DWrapper.column")
    def subtable(self, idx, wrapped=False):
        """
        Return a subtable at index `idx`.
        
        If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
        """
        raise NotImplementedError("I2DWrapper.subtable")
    def ndim(self):
        return 2
    
    
    
class Array2DWrapper(I2DWrapper):
    """
    A wrapper for a 2D numpy array.

    Provides a uniform access to basic methods of a wrapped object.
    """
    def __init__(self, container):
        container=np.asarray(container)
        if container.ndim!=2:
            raise ValueError("Array2DWrapper only supports 2D arrays, got {}D array".format(container.ndim))
        I2DWrapper.__init__(self,container,
                self.RowAccessor(self,container),self.ColumnAccessor(self,container),self.TableAccessor(container))
    
    def set_container(self,cont):
        self.cont=cont
        self.r._storage=cont
        self.c._storage=cont
        self.t._storage=cont
    class RowAccessor:
        """
        A row accessor: creates a simple uniform interface to treat the wrapped object row-wise (append/insert/delete/iterate over rows).

        Generated automatically for each table on creation, doesn't need to be created explicitly.
        """
        def __init__(self, wrapper, storage):
            self._wrapper=wrapper
            self._storage=storage
        def __iter__(self):
            return AccessIterator(self._storage,lambda obj,idx: obj[idx])
        def __getitem__(self, idx):
            return self._storage[idx]
        def __setitem__(self, idx, val):
            self._storage[idx]=val
        def get_deleted(self, idx, wrapped=False):
            """
            Return a new table with the rows at `idx` deleted.

            If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
            """
            new_cont=np.delete(self._storage,idx,axis=0)
            return Array2DWrapper(new_cont) if wrapped else new_cont
        def __delitem__(self, idx):
            self._wrapper.set_container(self.get_deleted(idx))
        def get_inserted(self, idx, val, wrapped=False):
            """
            Return a new table with new rows given by `val` inserted at `idx`.

            If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
            """
            new_cont=np.insert(self._storage,idx,val,axis=0)
            return Array2DWrapper(new_cont) if wrapped else new_cont
        def insert(self, idx, val):
            """
            Insert new rows given by `val` at index `idx`.
            """
            self._wrapper.set_container(self.get_inserted(idx,val))
        def get_appended(self, val, wrapped=False):
            """
            Return a new table with new rows given by `val` appended to the end of the table.

            If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
            """
            new_cont=np.append(self._storage,val,axis=0)
            return Array2DWrapper(new_cont) if wrapped else new_cont
        def append(self, val):
            """Insert new rows given by `val` to the end of the table"""
            self._wrapper.set_container(self.get_appended(val))
    
    class ColumnAccessor:
        """
        A column accessor: creates a simple uniform interface to treat the wrapped object column-wise (append/insert/delete/iterate over columns).

        Generated automatically for each table on creation, doesn't need to be created explicitly.
        """
        def __init__(self, wrapper, storage):
            self._wrapper=wrapper
            self._storage=storage
        def __iter__(self):
            return AccessIterator(self._storage,lambda obj,idx: obj[:,idx])
        def __getitem__(self, idx):
            return self._storage[:,idx]
        def __setitem__(self, idx, val):
            self._storage[:,idx]=val
        def get_deleted(self, idx, wrapped=False):
            """
            Return a new table with the columns at `idx` deleted.

            If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
            """
            new_cont=np.delete(self._storage,idx,axis=1)
            return Array2DWrapper(new_cont) if wrapped else new_cont
        def __delitem__(self, idx):
            self._wrapper.set_container(self.get_deleted(idx))
        def get_inserted(self, idx, val, wrapped=False):
            """
            Return a new table with new columns given by `val` inserted at `idx`.

            If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
            """
            new_cont=np.insert(self._storage,idx,val,axis=1)
            return Array2DWrapper(new_cont) if wrapped else new_cont
        def insert(self, idx, val):
            """
            Insert new columns given by `val` at index `idx`.
            """
            self._wrapper.set_container(self.get_inserted(idx,val))
        def get_appended(self, val, wrapped=False):
            """
            Return a new table with new columns given by `val` appended to the end of the table.

            If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
            """
            new_cont=np.append(self._storage,val,axis=1)
            return Array2DWrapper(new_cont) if wrapped else new_cont
        def append(self, val):
            """Insert new columns given by `val` to the end of the table"""
            self._wrapper.set_container(self.get_appended(val))
        def set_names(self, names):
            """Set column names (does nothing)"""
        def get_names(self):
            """Get column names (all names are ``None``)"""
            return [None]*self._storage.shape[1]
        def get_column_index(self, idx):
            """Get number index for a given column index"""
            return (idx if idx>=0 else self._storage.shape[1]-idx)
    
    class TableAccessor:
        """
        A table accessor: accessing the table data through this interface returns an object of the appropriate type
        (numpy array for numpy wrapped object, and a DataFrame for a pandas DataFrame wrapped object).

        Generated automatically for each table on creation, doesn't need to be created explicitly.
        """
        def __init__(self, storage):
            self._storage=storage
        def __iter__(self):
            return AccessIterator(self)
        def __getitem__(self, idx):
            return self._storage[idx]
        def __setitem__(self, idx, val):
            self._storage[idx]=val
    
    def subtable(self, idx, wrapped=False):
        """
        Return a subtable at index `idx` of the appropriate type (2D numpy array).
        
        If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
        """
        return Array2DWrapper(self.cont[idx]) if wrapped else self.cont[idx]
    def column(self, idx, wrapped=False):
        """
        Get a column at index `idx` as a 1D numpy array.

        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        return Array1DWrapper(self.cont[:,idx]) if wrapped else self.cont[:,idx]
    @classmethod
    def from_columns(cls, columns, column_names=None, index=None, wrapped=False):
        """
        Build a new object of the type corresponding to the wrapper from the supplied `columns` (a list of columns).

        If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
        `column_names` parameter is ignored.
        """
        new_cont=np.column_stack(columns)
        return Array2DWrapper(new_cont) if wrapped else new_cont
    @staticmethod
    def from_array(array, column_names=None, index=None, force_copy=False, wrapped=False):
        """
        Build a new object of the type corresponding to the wrapper from the supplied `array` (a list of rows or a 2D numpy array).

        If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
        `column_names` parameter is ignored.
        """
        new_cont=np.array(array) if force_copy else np.asarray(array)
        return Array2DWrapper(new_cont) if wrapped else new_cont
    def get_type(self):
        """Get a string representing the wrapped object type"""
        return "2d.array"
    def copy(self, wrapped=False):
        """
        Copy the object.
        
        If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
        """
        new_cont=self.cont.copy()
        return Array2DWrapper(new_cont) if wrapped else new_cont
    

class DataFrame2DWrapper(I2DWrapper):
    """
    A wrapper for a pandas DataFrame object.

    Provides a uniform access to basic methods of a wrapped object.
    """
    def __init__(self, container):
        if not isinstance(container,pd.DataFrame):
            container=pd.DataFrame(container,copy=False)
        if container.ndim!=2:
            raise ValueError("DataFrame2DWrapper only supports 2D arrays, got {}D array".format(container.ndim))
        I2DWrapper.__init__(self,container,
                    self.RowAccessor(self,container),self.ColumnAccessor(self,container),self.TableAccessor(container))

    def __getitem__(self, idx):
        res=self.cont.iloc[idx]
        return np.asarray(res) if len(get_shape(res))>0 else res
    def __setitem__(self, idx, val):
        self.cont.iloc[idx]=val
    
    class RowAccessor:
        """
        A row accessor: creates a simple uniform interface to treat the wrapped object row-wise (append/insert/delete/iterate over rows).

        Generated automatically for each table on creation, doesn't need to be created explicitly.
        """
        def __init__(self, wrapper, storage):
            self._wrapper=wrapper
            self._storage=storage
        def __iter__(self):
            return self._storage.__iter__()
        def __getitem__(self, idx):
            return self._storage.iloc[idx]
        def __setitem__(self, idx, val):
            self._storage.iloc[idx]=val
        def get_deleted(self, idx, wrapped=False):
            """
            Return a copy of the column with the data at index `idx` deleted.

            If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
            """
            new_cont=self._storage.drop(self._storage.index[idx])
            return DataFrame2DWrapper(new_cont) if wrapped else new_cont
        def __delitem__(self, idx):
            self._storage.drop(self._storage.index[idx],inplace=True)
        def get_inserted(self, idx, val, wrapped=False):
            """
            Return a new table with new rows given by `val` inserted at `idx`.

            If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
            """
            new_cont=pd.concat([self._storage.iloc[:idx],pd.DataFrame(val,copy=False),self._storage.iloc[idx:]])
            return DataFrame2DWrapper(new_cont) if wrapped else new_cont
        def insert(self, idx, val):
            """
            Insert new rows given by `val` at index `idx`.
            """
            self._wrapper.set_container(self.get_inserted(idx,val))
        def get_appended(self, val, wrapped=False):
            """
            Return a new table with new rows given by `val` appended to the end of the table.

            If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
            """
            new_cont=self._storage.append(val)
            return DataFrame2DWrapper(new_cont) if wrapped else new_cont
        def append(self, val):
            """Insert new rows given by `val` to the end of the table"""
            self._wrapper.set_container(self.get_appended(val))
            
    class ColumnAccessor:
        """
        A column accessor: creates a simple uniform interface to treat the wrapped object column-wise (append/insert/delete/iterate over columns).

        Generated automatically for each table on creation, doesn't need to be created explicitly.
        """
        def __init__(self, wrapper, storage):
            self._wrapper=wrapper
            self._storage=storage
        def __iter__(self):
            for _,c in self._storage.iteritems():
                yield c
        def __getitem__(self, idx):
            return self._storage.iloc[:,idx]
        def __setitem__(self, idx, val):
            self._storage.iloc[:,idx]=val
        def get_deleted(self, idx, wrapped=False):
            """
            Return a new table with the columns at `idx` deleted.

            If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
            """
            try:
                new_cont=self._storage.drop(idx,axis="columns")
            except (TypeError,KeyError):
                new_cont=self._storage.drop(self._storage.columns[idx],axis="columns")
            return DataFrame2DWrapper(new_cont) if wrapped else new_cont
        def __delitem__(self, idx):
            try:
                self._storage.drop(idx,axis="columns",inplace=True)
            except (TypeError,KeyError):
                self._storage.drop(self._storage.columns[idx],axis="columns",inplace=True)
        def get_inserted(self, idx, val, column_name=None, wrapped=False):
            """
            Return a new table with new columns given by `val` inserted at `idx`.

            If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
            """
            new_wrap=self._wrapper.copy()
            new_wrap.insert(idx,val,column_name=column_name)
            return new_wrap if wrapped else new_wrap.cont
        def insert(self, idx, val, column_name=None):
            """Insert new columns given by `val` at index `idx`"""
            if column_name is None:
                column_name=self._storage.shape[1]
                while column_name in self._storage.columns:
                    column_name+=1
            self._storage.insert(idx,column_name,val)
        def get_appended(self, val, column_name=None, wrapped=False):
            """
            Return a new table with new columns given by `val` appended to the end of the table.

            If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
            """
            return self.get_inserted(-1,val,column_name=column_name,wrapped=wrapped)
        def append(self, val, column_name=None):
            """Insert new columns given by `val` to the end of the table"""
            return self.insert(-1,val,column_name=column_name)
        def set_names(self, names):
            """Set column names"""
            self._storage.columns=names
        def get_names(self):
            """Get column names"""
            return list(self._storage.columns)
        def get_column_index(self, idx):
            """Get number index for a given column index"""
            idx=ListIndex(idx,self.get_names()).idx
            return (idx if idx>=0 else self._storage.shape[1]-idx)
    
    class TableAccessor:
        """
        A table accessor: accessing the table data through this interface returns an object of the appropriate type
        (numpy array for numpy wrapped object, and a DataFrame for a pandas DataFrame wrapped object).

        Generated automatically for each table on creation, doesn't need to be created explicitly.
        """
        def __init__(self, storage):
            self._storage=storage
        def __iter__(self):
            return self._storage.iloc.__iter__()
        def __getitem__(self, idx):
            return self._storage.iloc[idx]
        def __setitem__(self, idx, val):
            self._storage.iloc[idx]=val
    
    def _get_df_columns(self, idx):
        try:
            return self.cont.loc(axis="columns")[idx]
        except (TypeError,KeyError):
            return self.cont.iloc(axis="columns")[idx]
    def subtable(self, idx, wrapped=False):
        """
        Return a subtable at index `idx` of the appropriate type (pandas DataFrame).
        
        If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
        """
        return DataFrame2DWrapper(self._get_df_columns(idx)) if wrapped else self._get_df_columns(idx)
    def column(self, idx, wrapped=False):
        """
        Get a column at index `idx` as a pandas Series object.

        If ``wrapped==True``, return a new wrapper containing the column; otherwise, just return the column.
        """
        return Series1DWrapper(self._get_df_columns(idx)) if wrapped else self._get_df_columns(idx)
    @classmethod
    def from_columns(cls, columns, column_names=None, index=None, wrapped=False):
        """
        Build a new object of the type corresponding to the wrapper from the supplied `columns` (a list of columns).

        `column_names` supplies names of the columns (only relevant for :class:`DataFrame2DWrapper`).
        If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
        """
        if column_names is None:
            column_names=list(range(len(columns)))
        new_cont=pd.DataFrame(dict(zip(column_names,columns)),columns=column_names,index=index)
        return DataFrame2DWrapper(new_cont) if wrapped else new_cont
    @staticmethod
    def from_array(array, column_names=None, index=None, force_copy=False, wrapped=False):
        """
        Build a new object of the type corresponding to the wrapper from the supplied `array` (a list of rows or a 2D numpy array).

        `column_names` supplies names of the columns (only relevant for :class:`DataFrame2DWrapper`).
        If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table.
        """
        new_cont=pd.DataFrame(array,columns=column_names,index=index,copy=force_copy)
        return DataFrame2DWrapper(new_cont) if wrapped else new_cont
    def get_index(self):
        """Get index of the given 2D table, or ``None`` if none is available"""
        return self.cont.index
    def get_type(self):
        """Get a string representing the wrapped object type"""
        return "2d.pandas"
    def copy(self, wrapped=False):
        """Copy the object. If ``wrapped==True``, return a new wrapper containing the table; otherwise, just return the table"""
        new_cont=self.cont.copy()
        return DataFrame2DWrapper(new_cont) if wrapped else new_cont
    

def wrap1d(container):
    """Wrap a 1D container (a 1D numpy array or or a pandas Series) into an appropriate wrapper"""
    if isinstance(container,pd.Series):
        return Series1DWrapper(container)
    return Array1DWrapper(container)
def wrap2d(container):
    """Wrap a 2D container (a 2D numpy array or a pandas DataFrame) into an appropriate wrapper"""
    if isinstance(container,pd.DataFrame):
        return DataFrame2DWrapper(container)
    return Array2DWrapper(container)
def wrap(container):
    """Wrap container (a numpy array, a pandas Series or a pandas DataFrame) into an appropriate wrapper"""
    if isinstance(container,IGenWrapper):
        return container
    ndim=len(get_shape(container))
    if ndim==1:
        return wrap1d(container)
    elif ndim==2:
        return wrap2d(container)
    else:
        raise ValueError("wrap only supports 1D and 2D arrays, got {}D".format(ndim))