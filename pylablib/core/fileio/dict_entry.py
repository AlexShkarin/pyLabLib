"""
Classes for dealing with the :class:`.Dictionary` entries with special conversion rules when saved or loaded.
Used to redefine how certain objects (e.g., tables) inside dictionaries are written into files and read from files.
"""


from ..utils import dictionary, py3
from . import location, parse_csv
from .loadfile_utils import InlineTable

import numpy as np
import pandas as pd



def is_dict_entry_branch(branch):
    """
    Check if the dictionary branch contains a dictionary entry which needs to be specially converted.
    """
    try:
        return "__data_type__" in branch
    except TypeError:
        return False



def _is_data_valid(data, pred):
    if pred is None:
        return None
    elif isinstance(pred,(type,tuple)):
        return isinstance(data,pred)
    else:
        return pred(data)
def _is_branch_valid(branch, pred):
    bdt=branch["__data_type__"]
    if pred is None:
        return None
    elif isinstance(pred,tuple):
        return bdt in pred
    elif isinstance(pred,py3.textstring):
        return bdt in pred
    else:
        return pred(bdt)






##### Entry builders and parsers #####

class DictEntryBuilder:
    """
    Object for building dictionary entries from objects.

    Args:
        entry_cls: dictionary entry class
        pred: method used to check if an object can be turned into the corresponding entry;
            if ``None``, use the default entry class checker (``entry_class.is_data_valid``)
        kwargs: keyword arguments passed to the entry constructor along with the data
    """
    def __init__(self, entry_cls, pred=None, **kwargs):
        self.entry_cls=entry_cls
        self.pred=pred
        self.kwargs=kwargs
    def is_data_valid(self, data):
        """Check if a data object can be wrapped by the current entry class"""
        if self.pred:
            return _is_data_valid(data,self.pred)
        else:
            return self.entry_cls.is_data_valid(data)
    def from_data(self, data):
        """Build a dictionary entry from the data"""
        return self.entry_cls(data,**self.kwargs)

class DictEntryParser:
    """
    Object for building dictionary entries from dictionary branches.

    Args:
        entry_cls: dictionary entry class
        pred: method used to check if a dictionary branch can be turned into the corresponding entry;
            if ``None``, use the default entry class checker (``entry_class.is_branch_valid``)
        kwargs: keyword arguments passed to the entry ``from_dict`` class method along with the branch
    """
    def __init__(self, entry_cls, pred=None, **kwargs):
        self.entry_cls=entry_cls
        self.pred=pred
        self.kwargs=kwargs
    def is_branch_valid(self, branch):
        """Check if a branch can be parsed by the current entry class"""
        if self.pred:
            return _is_branch_valid(branch,self.pred)
        else:
            return self.entry_cls.is_branch_valid(branch)
    def from_dict(self, dict_ptr, loc):
        """Build a dictionary entry from the branch and the file location"""
        return self.entry_cls.from_dict(dict_ptr,loc,**self.kwargs)


_default_builders=[]
_default_parsers=[]
def add_dict_entry_builder(builder):
    """Add an entry builder to the global list of builders"""
    _default_builders.append(builder)
def add_dict_entry_parser(parser):
    """Add an entry parser to the global list of parsers"""
    _default_parsers.append(parser)
def add_dict_entry_class(cls):
    """
    Add an entry class.

    Automatically registers builder and parser, which take no additional arguments and use default class method
    to determine if an object/branch can be converted into an entry.
    """
    add_dict_entry_builder(DictEntryBuilder(cls))
    add_dict_entry_parser(DictEntryParser(cls))

def from_data(data, builders=None):
    """
    Build a dictionary entry from the data.

    `builders` can contain an additional list of builder to try before using the default ones.
    """
    if isinstance(data, IDictionaryEntry):
        return data
    builders=(builders or [])+_default_builders
    for b in builders:
        if b.is_data_valid(data):
            return b.from_data(data)
    return None
def from_dict(dict_ptr, loc, parsers=None):
    """
    Build a dictionary entry from the dictionary branch and the file location.

    `parsers` can contain an additional list of parsers to try before using the default ones.
    """
    parsers=(parsers or [])+_default_parsers
    for p in parsers:
        if p.is_branch_valid(dict_ptr):
            return p.from_dict(dict_ptr,loc)
    return None









### General description ###

class IDictionaryEntry:
    """
    A generic `Dictionary` entry.

    Contains data represented by the node, as well as the way to represent this data as a dictionary branch.

    Args:
        data: data to be wrapped

    Methods:
        is_data_valid (class method): check if a data object can be wrapped by the current entry class
        is_branch_valid (class method): check if a branch can be parsed by the current entry class
        from_dict (class method): create a dictionary entry of a given class from the dictionary branch
        to_dict: convert the entry to a dictionary branch
    """
    _data_type=None # data type marker (a string marker of the entry class which is saved in the dictionary under ``__data_type__```)
    _obj_type=None
    def __init__(self, data):
        self.data=data

    @classmethod
    def is_data_valid(cls, data):
        """Check if a data object can be wrapped by the current entry class"""
        return _is_data_valid(data,cls._obj_type)
    @classmethod
    def is_branch_valid(cls, branch):
        """Check if a branch can be parsed by the current entry class"""
        return _is_branch_valid(branch,cls._data_type)
    
    @classmethod
    def from_dict(cls, dict_ptr, loc):  # pylint: disable=unused-argument
        """
        Convert a dictionary branch to a specific :class:`IDictionaryEntry` object.
        
        Args:
            dict_ptr (.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
            loc: Location for the data to be loaded.
        """
        return cls(None) if cls.is_branch_valid(dict_ptr) else None
    def to_dict(self, dict_ptr, loc):  # pylint: disable=unused-argument
        """
        Convert data to a dictionary branch on saving.
        
        Args:
            dict_ptr (.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
            loc: File location for the data to be saved.
        """
        return dictionary.Dictionary({"__data_type__":self._data_type})






###  Table formatters  ###

def parse_stored_table_data(desc=None, data=None, out_type="pandas"):
    """
    Parse table data corresponding to the given description dictionary and data.

    Args:
        desc: description dictionary; can be ``None``, if no description is given
        data: separately loaded data; can be ``None``, if no data is given (in this case assume that it is stored in the description dictionary);
            can be a tuple ``(column_data, column_names)`` (such as the one returned by :func:`.parse_csv.read_table`),
            or a an :class:`.InlineTable` object containing such tuple.
        out_type (str): Output format of the data (``'array'`` for numpy arrays or  ``'pandas'`` for pandas DataFrame objects).
    
    Return:
        tuple ``(data, columns)``, where ``data`` is the data table in the specified format, and ``columns`` is the list of columns
    """
    desc=desc or {}
    data=desc.get("data",data)
    if data is None:
        raise ValueError("can't load {0} with format {1}".format(desc,"inline"))
    if isinstance(data,InlineTable):
        data=data.table
    data,columns=data
    columns=desc.get("columns",columns)
    out_type=desc.get("__cont_type__",out_type)
    if out_type in {"datatable","table"}: # legacy file formats
        out_type="pandas"
    if len(data)==0:
        data=parse_csv.columns_to_table([],columns=columns,out_type=out_type)
    if out_type=="pandas":
        data=pd.DataFrame(dict(zip(columns,data)),columns=columns)
        if "index_columns" in desc:
            index_width=len(desc["index_columns"])
            data=data.set_index(columns[:index_width])
            data.index.names=desc["index_columns"]
            columns=columns[index_width:]
        if desc.get("column_multiindex",False):
            data.columns=pd.MultiIndex.from_tuples(columns)
    else:
        if columns and len(columns)!=len(data):
            raise ValueError("columns number doesn't agree with the table size")
        data=np.column_stack(data)
    return data,columns

class ITableDictionaryEntry(IDictionaryEntry):
    """
    A generic table Dictionary entry.
    
    Args:
        data: Table data.
        columns (list): If not ``None``, list of column names (if ``None`` and data is a pandas DataFrame object, get column names from that). 
    """
    
    _data_type="table" # data type marker (a string marker of the entry class which is saved in the dictionary under ``__data_type__```)
    def __init__(self, data, columns=None):
        IDictionaryEntry.__init__(self,data)
        self.columns=columns

    @classmethod
    def is_data_valid(cls, data):
        """Check if a data object can be wrapped by the current entry class"""
        return isinstance(data,pd.DataFrame) or (isinstance(data,np.ndarray) and data.ndim==2)
        
    def _prepare_desc_data(self):
        data=self.data
        desc=dictionary.Dictionary()
        desc["__data_type__"]="table"
        columns=self.columns
        if isinstance(data,pd.DataFrame):
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
    def from_dict(cls, dict_ptr, loc, out_type="pandas"):  # pylint: disable=arguments-differ
        """
        Convert a dictionary branch to a specific DictionaryEntry object.
        
        Args:
            dict_ptr (.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
            loc: Location for the data to be loaded.
            out_type (str): Output format of the data (``'array'`` for numpy arrays or ``'pandas'`` for pandas DataFrame objects),
                used only if the dictionary doesn't provide the format.
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
            return InlineTableDictionaryEntry.from_dict(dict_ptr,loc,out_type=out_type)
        else:
            return IExternalTableDictionaryEntry.from_dict(dict_ptr,loc,out_type=out_type)
        
add_dict_entry_class(ITableDictionaryEntry)

class InlineTableDictionaryEntry(ITableDictionaryEntry):
    """
    An inlined table Dictionary entry.
    
    Args:
        data: Table data.
        columns (list): If not ``None``, a list of column names (if ``None`` and data is a pandas DataFrame object, get column names from that). 
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
    def from_dict(cls, dict_ptr, loc, out_type="pandas"):
        """
        Build an :class:`InlineTableDictionaryEntry` object from the dictionary and read the inlined data.
        
        Args:
            dict_ptr (.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
            loc: Location for the data to be loaded.
            out_type (str): Output format of the data (``'array'`` for numpy arrays or ``'pandas'`` for pandas DataFrame objects).
        """
        data,columns=parse_stored_table_data(dict_ptr,out_type=out_type)
        return InlineTableDictionaryEntry(data,columns)

class IExternalTableDictionaryEntry(ITableDictionaryEntry):
    def __init__(self, data, file_format, name, columns, force_name=True):
        from . import savefile
        data,file_format=savefile.get_output_format(data,file_format)
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
    def from_dict(cls, dict_ptr, loc, out_type="pandas"):
        file_type=dict_ptr.get("file_type",None)
        if not (file_type in {"bin","csv"}): # TODO:  add autodetect
            raise ValueError("can't load {0} with format {1}".format(dict_ptr,"external"))
        if file_type=="csv":
            return ExternalTextTableDictionaryEntry.from_dict(dict_ptr,loc,out_type=out_type)
        else:
            return ExternalBinTableDictionaryEntry.from_dict (dict_ptr,loc,out_type=out_type)
class ExternalTextTableDictionaryEntry(IExternalTableDictionaryEntry):
    """
    An external text table Dictionary entry.
    
    Args:
        data: Table data.
        file_format (str): Output file format.
        name (str): Name template for the external file (default is the full path connected with ``"_"`` symbol).
        columns (list): If not ``None``, a list of column names (if ``None`` and data is a pandas DataFrame object, get column names from that).
        force_name (bool): If ``False`` and the target file already exists, generate a new unique name; otherwise, overwrite the file.
    """
    def __init__(self, data=None, file_format="csv", name="", columns=None, force_name=True):
        IExternalTableDictionaryEntry.__init__(self,data,file_format,name,columns,force_name=force_name)
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
        d["file_path"]=save_file.name.to_string()
        return d
    @classmethod
    def from_dict(cls, dict_ptr, loc, out_type="pandas"):
        """
        Build an :class:`ExternalTextTableDictionaryEntry` object from the dictionary and load the external data.
        
        Args:
            dict_ptr (.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
            loc: Location for the data to be loaded.
            out_type (str): Output format of the data (``'array'`` for numpy arrays or ``'pandas'`` for pandas DataFrame objects).
        """
        from . import loadfile
        file_path=dict_ptr["file_path"]
        file_type=dict_ptr.get("file_type","csv")
        out_type=dict_ptr.get("__cont_type__",out_type)
        load_file=location.LocationFile(loc,file_path)
        file_out_type="array" if out_type=="array" else "columns"
        data=loadfile.build_file_format(load_file,file_format=file_type,out_type=file_out_type,dtype="generic").read(load_file).data
        data,_=parse_stored_table_data(dict_ptr,data=data,out_type=out_type)
        return ExternalTextTableDictionaryEntry(data,name=load_file.name)
class ExternalBinTableDictionaryEntry(IExternalTableDictionaryEntry):
    """
    An external binary table Dictionary entry.
    
    Args:
        data: Table data.
        file_format (str): Output file format.
        name (str): Name template for the external file (default is the full path connected with ``"_"`` symbol).
        columns (list): If not ``None``, a list of column names (if ``None`` and data is a pandas DataFrame object, get column names from that).
        force_name (bool): If ``False`` and the target file already exists, generate a new unique name; otherwise, overwrite the file.
    """
    def __init__(self, data=None, file_format="bin", name="", columns=None, force_name=True):
        IExternalTableDictionaryEntry.__init__(self,data,file_format,name,columns,force_name=force_name)
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
        d.merge(self.file_format.get_preamble(save_file,table),"preamble")
        d["file_path"]=save_file.name.to_string()
        return d
    @classmethod
    def from_dict(cls, dict_ptr, loc, out_type="pandas"):
        """
        Build an :class:`ExternalBinTableDictionaryEntry` object from the dictionary and load the external data.
        
        Args:
            dict_ptr (.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
            loc: Location for the data to be loaded.
            out_type (str): Output format of the data (``'array'`` for numpy arrays or  ``'pandas'`` for pandas DataFrame objects).
        """
        from . import loadfile
        file_path=dict_ptr["file_path"]
        file_type=dict_ptr.get("file_type","bin")
        preamble=dict_ptr.get("preamble",None)
        out_type=dict_ptr.get("__cont_type__",out_type)
        load_file=location.LocationFile(loc,file_path)
        file_out_type="array" if out_type=="array" else "columns"
        data=loadfile.build_file_format(load_file,file_format=file_type,preamble=preamble,out_type=file_out_type).read(load_file).data
        if out_type=="pandas" and len(data[0]):
            data=[(c.astype(c.dtype.type,copy=False) if isinstance(c,np.ndarray) else c) for c in data[0]],data[1] # convert data to native byteorder (required for pandas indexing)
        data,_=parse_stored_table_data(dict_ptr,data=data,out_type=out_type)
        return ExternalBinTableDictionaryEntry(data,name=load_file.name)

def table_entry_builder(table_format="inline"):
    """
    Make an entry builder for tables depending on the table format.

    Args:
        table_format (str): Default format for table (numpy arrays or pandas DataFrames) entries. Can be
            ``'inline'`` (table is written inside the file),
            ``'csv'`` (external CSV file) or
            ``'bin'`` (external binary file).
    """
    if table_format=="inline":
        return DictEntryBuilder(InlineTableDictionaryEntry)
    elif table_format=="csv":
        return DictEntryBuilder(ExternalTextTableDictionaryEntry)
    elif table_format=="bin":
        return DictEntryBuilder(ExternalBinTableDictionaryEntry)
    else:
        raise ValueError("unrecognized table format: {}".format(table_format))







class IExternalFileDictionaryEntry(IDictionaryEntry):
    """
    Generic dictionary entry for data in an external file.

    Args:
        data: Stored data.
        name (str): Name template for the external file (default is the full path connected with ``"_"`` symbol).
        force_name (bool): If ``False`` and the target file already exists, generate a new unique name; otherwise, overwrite the file.
    """
    _data_type="external_file" # data type marker (a string marker of the entry class which is saved in the dictionary under ``__data_type__```)
    def __init__(self, data, name="", force_name=True):
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
        """Convert the data to a dictionary branch and save the data to an external file"""
        name=self._get_name(dict_ptr,loc)
        d=dictionary.Dictionary()
        d["__data_type__"]="external_file"
        d["file_type"]=self.file_format
        save_file=location.LocationFile(loc,name)
        self.save_file(save_file)
        d.merge(self.get_preamble(),"preamble")
        d["file_path"]=save_file.name.to_string()
        return d
    @classmethod
    def from_dict(cls, dict_ptr, loc):
        """
        Build an :class:`IExternalFileDictionaryEntry` object from the dictionary and load the external data.
        
        Args:
            dict_ptr (.dictionary.DictionaryPointer): Pointer to the dictionary location for the entry.
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
        data=subclass.load_file(load_file,preamble)
        return subclass(data,name=load_file.name)
    def get_preamble(self):
        """Generate preamble (dictionary with supplementary data which allows to load the data from the file)"""
        return {}
    def save_file(self, location_file):
        """
        Save stored data into the given location.

        Virtual method, should be overloaded in subclasses
        """
        raise NotImplementedError("IExternalFileDictionaryEntry.save_file")
    @classmethod
    def load_file(cls, location_file, preamble):
        """
        Load stored data from the given location, using the supplied preamble.

        Virtual method, should be overloaded in subclasses
        """
        raise NotImplementedError("IExternalFileDictionaryEntry.load_file")
add_dict_entry_class(IExternalFileDictionaryEntry)



class ExternalNumpyDictionaryEntry(IExternalFileDictionaryEntry):
    """
    A dictionary entry which stores the numpy array data into an external file in binary format.

    Args:
        data: Numpy array data.
        name (str): Name template for the external file (default is the full path connected with ``"_"`` symbol).
        force_name (bool): If ``False`` and the target file already exists, generate a new unique name; otherwise, overwrite the file.
        dtype: numpy dtype to load/save the data (by default, dtype of the supplied data).
    """
    def __init__(self, data, name="", force_name=True, dtype=None):
        IExternalFileDictionaryEntry.__init__(self,np.asarray(data,dtype=dtype),name=name,force_name=force_name)
    file_format="numpy"
    def get_preamble(self):
        """Generate preamble (dictionary with supplementary data which allows to load the data from the file)"""
        return {"shape":self.data.shape,"dtype":self.data.dtype.str}
    def save_file(self, location_file):
        """Save stored data into the given location"""
        with location_file.open("wb") as stream:
            self.data.tofile(stream)
    @classmethod
    def load_file(cls, location_file, preamble):
        """Load stored data from the given location, using the supplied preamble"""
        with location_file.open("rb") as stream:
            return np.fromfile(stream,dtype=preamble["dtype"]).reshape(preamble["shape"])
IExternalFileDictionaryEntry.add_file_format(ExternalNumpyDictionaryEntry)






class ExpandedContainerDictionaryEntry(IDictionaryEntry):
    """
    A dictionary entry which expands containers (lists, tuples, dictionaries) into subdictionaries.

    Useful when the data in the containers is complex, so writing it into one line (as is default for lists and tuples) wouldn't work.

    Args:
        data: Container data.
    """
    _data_type="exp_container" # data type marker (a string marker of the entry class which is saved in the dictionary under ``__data_type__```)
    def to_dict(self, dict_ptr, loc):
        """Convert the stored container to a dictionary branch"""
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
    def from_dict(cls, dict_ptr, loc):
        """Build an :class:`ExpandedContainerDictionaryEntry` object from the dictionary"""
        clabel=dict_ptr["container_type"]
        if clabel in ["list","tuple"]:
            value=[dict_ptr[k] for k in range(len(dict_ptr)-2)]
            if clabel=="tuple":
                value=tuple(value)
        else:
            value={dict_ptr[k,"k"]:dict_ptr[k,"v"] for k in range(len(dict_ptr)-2)}
        return cls(value)
add_dict_entry_class(ExpandedContainerDictionaryEntry)