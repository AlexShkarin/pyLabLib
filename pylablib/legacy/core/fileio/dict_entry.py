"""
Classes for dealing with the :class:`.Dictionary` entries with special conversion rules when saved or loaded.
Used to redefine how certain objects (e.g., tables) are written into files and read from files.
"""


from ..utils import dictionary, py3 #@UnresolvedImport
from ..datatable import table as datatable #@UnresolvedImport
from . import location, parse_csv

import numpy as np
import pandas as pd



def special_load_rules(branch):
    """
    Detect if the branch requires special conversion rules.
    """
    try:
        return "__data_type__" in branch
    except TypeError:
        return False


class InlineTable(object):
    """Simple marker class that denotes that the wrapped numpy 2D array should be written inline"""
    def __init__(self, table):
        object.__init__(self)
        self.table=table


### General description ###

class IDictionaryEntry(object):
    """
    A generic `Dictionary` entry.
    """
    def __init__(self, data=None):
        object.__init__(self)
        self.set_data(data)
        
    def set_data(self, data=None):
        """
        Set internal data.
        """
        self.data=data
    def get_data(self):
        """
        Get internal data.
        """
        return self.data
    
    def to_dict(self, dict_ptr, loc):
        """
        Convert data to a dictionary branch on saving.
        
        Virtual method, to be defined in subclasses.
        
        Args:
            dict_ptr (~core.utils.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
            loc: Location for the data to be saved.
        """
        raise NotImplementedError("IDictionaryEntry.to_dict")
    
    
    @classmethod
    def build_entry(cls, data, **kwargs):
        """
        Create a `DictionaryEntry` object based on the supplied data and arguments.
        
        Args:
            data: Data to be saved.
        """
        return None
    
    @classmethod
    def from_dict(cls, dict_ptr, loc, **kwargs):
        """
        Convert a dictionary branch to a specific `DictionaryEntry` object.
        
        Args:
            dict_ptr (~core.utils.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
            loc: Location for the data to be loaded.
        """
        return cls(dict_ptr)



_entry_classes=[]
def add_entry_class(cls, branch_predicate, object_predicate=None):
    """
    Add an entry class which is automatically used in the :func:`build_entry` and :func:`from_dict` functions
    to delegate work for converting objects and dictionary branches into dictionary entries.

    Args:
        cls: the :class:`IDictionaryEntry` subclass whose `:meth:`build_entry` and :meth:`from_dict` methods will be used
        branch_predicate: predicate used to determine whether the specified subclass is used in`:func:`from_dict` function;
            it is a function which takes a single argument (dictionary branch) and returns ``True`` if the conversion should be delegated to the `subclass`
            can be a string or a tuple of strings, in which case it is interpreted as passing branches with a given ``"_data_type__"`` value.
        object_predicate: predicate used to determine whether the specified subclass is used in`:func:`build_entry` function;
            it is a function which takes a single argument (an object to be converted) and returns ``True`` if the conversion should be delegated to the `subclass`
            can be a type or a tuple of types, in which case it is interpreted as passing object of the given type;
            can also be ``None``, which means that the predicate always returns ``False``
            (i.e., this dictionary entries aren't created automatically on dictionary saving, but need to be created manually)
    """
    if isinstance(branch_predicate, (tuple,list)):
        bp=lambda branch: branch.get("__data_type__") in branch_predicate
    elif isinstance(branch_predicate, py3.textstring):
        bp=lambda branch: branch.get("__data_type__")==branch_predicate
    else:
        bp=branch_predicate
    if isinstance(object_predicate, (type, tuple)):
        op=lambda obj: isinstance(obj,object_predicate)
    elif object_predicate is None:
        op=lambda obj: False
    else:
        op=object_predicate
    _entry_classes.append((cls,op,bp))

def build_entry(data, **kwargs):
    """
    Create a `DictionaryEntry` object based on the supplied data and arguments.
    
    Args:
        data: Data to be saved.
        dict_ptr (~core.utils.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
        loc: Location for the data to be saved.
    """
    if isinstance(data, IDictionaryEntry):
        return data
    for cls,op,_ in _entry_classes:
        if op(data):
            return cls.build_entry(data,**kwargs)
    return None

def from_dict(dict_ptr, loc, **kwargs):
    """
    Convert a dictionary branch to a specific `DictionaryEntry` object.
    
    Args:
        dict_ptr (~core.utils.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
        loc: Location for the data to be loaded.
    """
    for cls,_,bp in _entry_classes:
        if bp(dict_ptr):
            return cls.from_dict(dict_ptr,loc,**kwargs)
    return IDictionaryEntry(dict_ptr)




###  Table formatters  ###

class ITableDictionaryEntry(IDictionaryEntry):
    """
    A generic table Dictionary entry.
    
    Args:
        data: Table data.
        columns (list): If not ``None``, list of column names (if ``None`` and data is a DataTable object, get column names from that). 
    """
    
    def __init__(self, data=None, columns=None):
        IDictionaryEntry.__init__(self,data)
        self.columns=columns
        
    def _prepare_desc_data(self):
        data=self.data
        desc=dictionary.Dictionary()
        desc["__data_type__"]="table"
        columns=self.columns
        if isinstance(data,datatable.DataTable):
            desc["__cont_type__"]="table"
            if columns is None:
                columns=data.get_column_names()
            elif len(data.get_column_names())!=len(columns):
                raise ValueError("supplied columns length {} doesn't agree with the data columns length {}".format(len(columns),len(data.get_column_names())))
        elif isinstance(data,pd.DataFrame):
            desc["__cont_type__"]="pandas"
            desc["column_multiindex"]=False
            if columns is None:
                columns=data.columns.tolist()
                desc["column_multiindex"]=data.columns.nlevels>1
            elif len(data.columns)!=len(columns):
                raise ValueError("supplied columns length {} doesn't agree with the data columns length {}".format(len(columns),len(data.columns)))
            default_idx=data.index.equals(pd.RangeIndex(stop=len(data)))
            if not default_idx:
                desc["index_columns"]=list(data.index.names)
                data=data.reset_index() # allow index/column name clashes to raise errors
                columns=data.columns.tolist()
                if desc["column_multiindex"]:
                    data.columns=columns
        else:
            desc["__cont_type__"]="array"
            data=np.asarray(data)
        if columns is not None:
            desc["columns"]=columns
        return desc, data

    @classmethod
    def _parse_desc_data(cls, desc, data=None, out_type="table"):
        columns=desc.get("columns",None)
        data=desc.get("data",data)
        out_type=desc.get("__cont_type__",out_type)
        if out_type=="datatable":
            out_type="table"
        if data is None:
            raise ValueError("can't load {0} with format {1}".format(desc,"inline"))
        if len(data)==0:
            data=parse_csv.columns_to_table([],columns=columns,out_type="table")
        if out_type=="table":
            if columns:
                data.set_column_names(columns)
        elif out_type=="pandas":
            column_data=[c._column for c in data.c]
            if columns is None:
                columns=data.get_column_names()
            data=pd.DataFrame(dict(zip(columns,column_data)),columns=columns)
            if "index_columns" in desc:
                index_width=len(desc["index_columns"])
                data=data.set_index(columns[:index_width])
                data.index.names=desc["index_columns"]
                columns=columns[index_width:]
            if desc.get("column_multiindex",False):
                data.columns=pd.MultiIndex.from_tuples(columns)
        else:
            if columns and len(columns)!=data.shape[1]:
                raise ValueError("columns number doesn't agree with the table size")
            data=np.asarray(data)
        return data,columns
        
    @classmethod
    def build_entry(cls, data, table_format="inline", **kwargs):
        """
        Create a DictionaryEntry object based on the supplied data and arguments.
        
        Args:
            data: Data to be saved.
            dict_ptr (~core.utils.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
            loc: Location for the data to be saved.
            table_format (str): Method of saving the table. Can be either
                ``'inline'`` (table is saved directly in the dictionary file),
                ``'csv'`` (table is saved in an external CSV file) or
                ``'bin'`` (table is saved in an external binary file).
        """
        if isinstance(table_format,ITableDictionaryEntry):
            table_format.set_data(data)
            return table_format
        if table_format=="inline":
            return InlineTableDictionaryEntry(data,**kwargs)
        elif table_format in {"csv","bin"}:
            if table_format in {"csv"}:
                return ExternalTextTableDictionaryEntry(data,file_format=table_format,**kwargs)
            else:
                return ExternalBinTableDictionaryEntry (data,file_format=table_format,**kwargs)
        else:
            raise ValueError("unrecognized table format: {0}".format(table_format))
    @classmethod
    def from_dict(cls, dict_ptr, loc, out_type="table", **kwargs):
        """
        Convert a dictionary branch to a specific DictionaryEntry object.
        
        Args:
            dict_ptr (~core.utils.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
            loc: Location for the data to be loaded.
            out_type (str): Output format of the data (``'array'`` for numpy arrays or ``'table'`` for :class:`.DataTable` objects). 
        """
        table_type=dict_ptr.get("__table_type__",None)
        if table_type is None:
            if "data" in dict_ptr:
                table_type="inline"
            elif "file_path" in dict_ptr:
                table_type="external"
            else:
                raise ValueError("unrecognized table format: {0}".format(dict_ptr))
        if table_type=="inline":
            return InlineTableDictionaryEntry.from_dict(dict_ptr,loc,out_type=out_type,**kwargs)
        else:
            return IExternalTableDictionaryEntry.from_dict(dict_ptr,loc,out_type=out_type,**kwargs)
add_entry_class(ITableDictionaryEntry,"table",(np.ndarray,datatable.DataTable,pd.DataFrame))
 
class InlineTableDictionaryEntry(ITableDictionaryEntry):
    """
    An inlined table Dictionary entry.
    
    Args:
        data: Table data.
        columns (list): If not ``None``, a list of column names (if ``None`` and data is a DataTable object, get column names from that). 
    """
    def to_dict(self, dict_ptr, loc):
        """
        Convert the data to a dictionary branch and write the table to the file.
        """
        if self.data is None:
            raise ValueError("can't build entry for empty table")
        d,table=self._prepare_desc_data()
        d["__table_type__"]="inline"
        d["data"]=InlineTable(table)
        return d
    @classmethod
    def from_dict(cls, dict_ptr, loc, out_type="table", **kwargs):
        """
        Build an :class:`InlineTableDictionaryEntry` object from the dictionary and read the inlined data.
        
        Args:
            dict_ptr (~core.utils.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
            loc: Location for the data to be loaded.
            out_type (str): Output format of the data (``'array'`` for numpy arrays or ``'table'`` for :class:`.DataTable` objects).
        """
        data,columns=cls._parse_desc_data(dict_ptr,out_type=out_type)
        return InlineTableDictionaryEntry(data,columns)

class IExternalTableDictionaryEntry(ITableDictionaryEntry):
    def __init__(self, data, file_format, name, columns, force_name=True, **kwargs):
        from . import savefile
        data,file_format=savefile.get_output_format(data,file_format,**kwargs)
        ITableDictionaryEntry.__init__(self,data,columns)
        self.file_format=file_format
        self.name=location.LocationName.from_object(name)
        self.force_name=force_name
    def _get_name(self, dict_ptr, loc):
        name=self.name
        if name.get_path()=="":
            name=location.LocationName("_".join(dict_ptr.get_path()),name.ext)
        if not self.force_name:
            name=loc.generate_new_name(name,idx=None)
        return name
    @classmethod
    def from_dict(cls, dict_ptr, loc, out_type="table", **kwargs):
        file_type=dict_ptr.get("file_type",None)
        if not (file_type in {"bin","csv"}): # TODO:  add autodetect
            raise ValueError("can't load {0} with format {1}".format(dict_ptr,"external"))
        if file_type=="csv":
            return ExternalTextTableDictionaryEntry.from_dict(dict_ptr,loc,out_type=out_type,**kwargs)
        else:
            return ExternalBinTableDictionaryEntry.from_dict (dict_ptr,loc,out_type=out_type,**kwargs)
class ExternalTextTableDictionaryEntry(IExternalTableDictionaryEntry):
    """
    An external text table Dictionary entry.
    
    Args:
        data: Table data.
        file_format (str): Output file format.
        name (str): Name template for the external file (default is the full path connected with ``"_"`` symbol).
        columns (list): If not ``None``, a list of column names (if ``None`` and data is a DataTable object, get column names from that).
        force_name (bool): If ``False`` and the target file already exists, generate a new unique name; otherwise, overwrite the file.
    """
    def __init__(self, data=None, file_format="csv", name="", columns=None, force_name=True, **kwargs):
        IExternalTableDictionaryEntry.__init__(self,data,file_format,name,columns,force_name=force_name,**kwargs)
    def to_dict(self, dict_ptr, loc):
        """
        Convert the data to a dictionary branch and save the table to an external file.
        """
        if self.data is None:
            raise ValueError("can't build entry for empty table")
        d,table=self._prepare_desc_data()
        name=self._get_name(dict_ptr,loc)
        d["__table_type__"]="external"
        d["file_type"]=self.file_format.format_name
        save_file=location.LocationFile(loc,name)
        self.file_format.write(save_file,table,columns=d.get("columns",None))
        d["file_path"]=save_file.get_path()
        return d
    @classmethod
    def from_dict(cls, dict_ptr, loc, out_type="table"):
        """
        Build an :class:`ExternalTextTableDictionaryEntry` object from the dictionary and load the external data.
        
        Args:
            dict_ptr (~core.utils.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
            loc: Location for the data to be loaded.
            out_type (str): Output format of the data (``'array'`` for numpy arrays or ``'table'`` for :class:`.DataTable` objects).
        """
        from . import loadfile
        file_path=dict_ptr["file_path"]
        file_type=dict_ptr.get("file_type","csv")
        out_type=dict_ptr.get("__cont_type__",out_type)
        load_file=location.LocationFile(loc,file_path)
        file_out_type="table" if out_type=="pandas" else out_type
        data=loadfile.IInputFileFormat.read_file(load_file,file_format=file_type,out_type=file_out_type,dtype="generic").data # TODO: autodetect data dtype when saving
        data,_=cls._parse_desc_data(dict_ptr,data=data,out_type=out_type)
        return ExternalTextTableDictionaryEntry(data,name=load_file.name)
class ExternalBinTableDictionaryEntry(IExternalTableDictionaryEntry):
    """
    An external binary table Dictionary entry.
    
    Args:
        data: Table data.
        file_format (str): Output file format.
        name (str): Name template for the external file (default is the full path connected with ``"_"`` symbol).
        columns (list): If not ``None``, a list of column names (if ``None`` and data is a DataTable object, get column names from that).
        force_name (bool): If ``False`` and the target file already exists, generate a new unique name; otherwise, overwrite the file.
    """
    def __init__(self, data=None, file_format="bin", name="", columns=None, force_name=True, **kwargs):
        IExternalTableDictionaryEntry.__init__(self,data,file_format,name,columns,force_name=force_name, **kwargs)
    def to_dict(self, dict_ptr, loc):
        """
        Convert the data to a dictionary branch and save the table to an external file.
        """
        if self.data is None:
            raise ValueError("can't build entry for empty table")
        d,table=self._prepare_desc_data()
        name=self._get_name(dict_ptr,loc)
        d["__table_type__"]="external"
        d["file_type"]=self.file_format.format_name
        save_file=location.LocationFile(loc,name)
        self.file_format.write(save_file,table)
        d.merge_branch(self.file_format.get_preamble(save_file,table),"preamble")
        d["file_path"]=save_file.get_path()
        return d
    @classmethod
    def from_dict(cls, dict_ptr, loc, out_type="table", **kwargs):
        """
        Build an :class:`ExternalBinTableDictionaryEntry` object from the dictionary and load the external data.
        
        Args:
            dict_ptr (~core.utils.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
            loc: Location for the data to be loaded.
            out_type (str): Output format of the data (``'array'`` for numpy arrays or ``'table'`` for :class:`.DataTable` objects).
        """
        from . import loadfile
        file_path=dict_ptr["file_path"]
        file_type=dict_ptr.get("file_type","bin")
        preamble=dict_ptr.get("preamble",None)
        out_type=dict_ptr.get("__cont_type__",out_type)
        load_file=location.LocationFile(loc,file_path)
        file_out_type="table" if out_type=="pandas" else out_type
        data=loadfile.IInputFileFormat.read_file(load_file,file_format=file_type,preamble=preamble,out_type=file_out_type).data
        if out_type=="pandas" and data.shape[1]>0:
            npdata=data[:]
            data=datatable.DataTable(npdata.astype(npdata.dtype.type)) # convert to native byteorder (required for pandas indexing)
        data,_=cls._parse_desc_data(dict_ptr,data=data,out_type=out_type)
        return ExternalBinTableDictionaryEntry(data,name=load_file.name)



class IExternalFileDictionaryEntry(IDictionaryEntry):
    """
    Generic dictionary entry for data in an external file.

    Args:
        data: Stored data.
        name (str): Name template for the external file (default is the full path connected with ``"_"`` symbol).
        force_name (bool): If ``False`` and the target file already exists, generate a new unique name; otherwise, overwrite the file.
    """
    def __init__(self, data, name="", force_name=True, **kwargs):
        IDictionaryEntry.__init__(self,data)
        self.name=location.LocationName.from_object(name)
        self.force_name=force_name
    file_format=None
    _file_formats={}
    @staticmethod
    def add_file_format(subclass):
        """
        Register an :class:`IExternalFileDictionaryEntry` as a possible stored file format.

        Used to automatically invoke a correct loader when loading the dictionary file.
        Only needs to be done once after the subclass declaration.
        """
        IExternalFileDictionaryEntry._file_formats[subclass.file_format]=subclass

    def _get_name(self, dict_ptr, loc):
        name=self.name
        if name.get_path()=="":
            name=location.LocationName("_".join(dict_ptr.get_path()),name.ext)
        if not self.force_name:
            name=loc.generate_new_name(name,idx=None)
        return name
    def to_dict(self, dict_ptr, loc):
        """Convert the data to a dictionary branch and save the data to an external file."""
        name=self._get_name(dict_ptr,loc)
        d=dictionary.Dictionary()
        d["__data_type__"]="external_file"
        d["file_type"]=self.file_format
        save_file=location.LocationFile(loc,name)
        self.save_file(save_file)
        d.merge_branch(self.get_preamble(),"preamble")
        d["file_path"]=save_file.get_path()
        return d
    @classmethod
    def from_dict(cls, dict_ptr, loc, **kwargs):
        """
        Build an :class:`IExternalFileDictionaryEntry` object from the dictionary and load the external data.
        
        Args:
            dict_ptr (~core.utils.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
            loc: Location for the data to be loaded.
        """
        file_path=dict_ptr["file_path"]
        file_type=dict_ptr.get("file_type",None)
        preamble=dict_ptr.get("preamble",{})
        load_file=location.LocationFile(loc,file_path)
        try:
            subclass=cls._file_formats[file_type]
        except KeyError:
            raise ValueError("unrecognized file type: {}".format(file_type))
        data=subclass.load_file(load_file,preamble,**kwargs)
        return subclass(data,name=load_file.name)
    def get_preamble(self):
        """Generate preamble (dictionary with supplementary data which allows to load the data from the file)"""
        return {}
    def save_file(self, loc_file):
        """
        Save stored data into the given location.

        Virtual method, should be overloaded in subclasses
        """
        raise NotImplementedError("IExternalFileDictionaryEntry.save_file")
    @classmethod
    def load_file(cls, loc_file, preamble, **kwargs):
        """
        Load stored data from the given location, using the supplied preamble.

        Virtual method, should be overloaded in subclasses
        """
        raise NotImplementedError("IExternalFileDictionaryEntry.load_file")
add_entry_class(IExternalFileDictionaryEntry,"external_file")



class ExternalNumpyDictionaryEntry(IExternalFileDictionaryEntry):
    """
    A dictionary entry which stores the numpy array data into an external file in binary format.

    Args:
        data: Numpy array data.
        name (str): Name template for the external file (default is the full path connected with ``"_"`` symbol).
        force_name (bool): If ``False`` and the target file already exists, generate a new unique name; otherwise, overwrite the file.
        dtype: numpy dtype to load/save the data (by default, dtype of the supplied data).
    """
    def __init__(self, data, name="", force_name=True, dtype=None, **kwargs):
        data=np.asarray(data,dtype=dtype)
        IExternalFileDictionaryEntry.__init__(self,data,name=name,force_name=force_name,**kwargs)
    file_format="numpy"
    def get_preamble(self):
        """Generate preamble (dictionary with supplementary data which allows to load the data from the file)"""
        return {"shape":self.data.shape,"dtype":self.data.dtype.str}
    def save_file(self, loc_file):
        """Save stored data into the given location."""
        with loc_file.opening("wb") as f:
            self.data.tofile(f)
    @classmethod
    def load_file(cls, loc_file, preamble, **kwargs):
        """Load stored data from the given location, using the supplied preamble."""
        with loc_file.opening("rb") as f:
            return np.fromfile(f,dtype=preamble["dtype"]).reshape(preamble["shape"])
IExternalFileDictionaryEntry.add_file_format(ExternalNumpyDictionaryEntry)



class ExpandedContainerDictionaryEntry(IDictionaryEntry):
    """
    A dictionary entry which expands containers (lists, tuples, dictionaries) into subdictionaries.

    Useful when the data in the containers is complex, so writing it into one line (as is default for lists and tuples) wouldn't work.

    Args:
        data: Container data.
    """
    def __init__(self, data, **kwargs):
        IDictionaryEntry.__init__(self,data)

    def to_dict(self, dict_ptr, loc):
        """Convert the stored container to a dictionary branch."""
        if isinstance(self.data,list):
            clabel="list"
        elif isinstance(self.data,tuple):
            clabel="tuple"
        elif isinstance(self.data,dict):
            clabel="dict"
        else:
            raise ValueError("unrecognized container type of {}".format(self.data))
        d=dictionary.Dictionary()
        d["__data_type__"]="exp_container"
        d["container_type"]=clabel
        if isinstance(self.data,dict):
            ldata=[{"k":k,"v":v} for (k,v) in self.data.items()]
        else:
            ldata=self.data
        for i,v in enumerate(ldata):
            d[i]=v
        return d
    @classmethod
    def from_dict(cls, dict_ptr, loc, **kwargs):
        """Build an :class:`ExpandedContainerDictionaryEntry` object from the dictionary."""
        clabel=dict_ptr["container_type"]
        if clabel in ["list","tuple"]:
            value=[dict_ptr[k] for k in range(len(dict_ptr)-2)]
            if clabel=="tuple":
                value=tuple(value)
        else:
            value={dict_ptr[k,"k"]:dict_ptr[k,"v"] for k in range(len(dict_ptr)-2)}
        return cls(value)
add_entry_class(ExpandedContainerDictionaryEntry,"exp_container")