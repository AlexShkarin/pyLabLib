"""
Utilities for writing data files.
"""

from . import datafile
from . import location
from . import dict_entry

from ..utils import string as string_utils
from ..utils import dictionary

import numpy as np
import pandas as pd
import datetime




def _is_file(value):
    return isinstance(value,datafile.DataFile)

def _is_table(value, allow_1D=False):
    return (isinstance(value, np.ndarray) and (value.ndim==2 or (allow_1D and value.ndim==1)) ) \
        or (isinstance(value, pd.DataFrame))
def _table_row_iterator(value):
    if isinstance(value, pd.DataFrame):
        return value.itertuples(index=False)
    else:
        return value



##### FILE FORMAT #####

class IOutputFileFormat:
    """
    Generic class for an output file format.
    
    Args:
        format_name (str): The name of the format (to be defined in subclasses).
    """
    def __init__(self, format_name):
        self.format_name=format_name
    
    def write_file(self, location_file, to_save):
        raise NotImplementedError("IOutputFileFormat.write_file")
    def write_data(self, location_file, data):
        raise NotImplementedError("IOutputFileFormat.write_data")
    
    def write(self, location_file, data):
        if not _is_file(data):
            data=datafile.DataFile(data)
        self.write_file(location_file,data)




class ITextOutputFileFormat(IOutputFileFormat):  # pylint: disable=abstract-method
    """
    Generic class for a text output file format.
    
    Args:
        format_name (str): The name of the format (to be defined in subclasses).
        save_props (bool): If ``True`` and saving :class:`.datafile.DataFile` object, save its props metainfo.
        save_comments (bool): If ``True`` and saving :class:`.datafile.DataFile` object, save its comments metainfo.
        save_time (bool): If ``True``, append the file creation time in the end.
        new_time (bool): If saving :class:`.datafile.DataFile` object, determines if the time should be updated to the current time.
    """
    def __init__(self, format_name, save_props=True, save_comments=True, save_time=True, new_time=True):
        IOutputFileFormat.__init__(self,format_name)
        self.save_props=save_props
        self.save_comments=save_comments
        self.save_time=save_time
        self.new_time=new_time
    
    def make_comment_line(self, comment):
        return "# "+string_utils.escape_string(comment,location="parameter")
    def make_prop_line(self, name, value):
        return "# {0} :\t{1}".format(name,string_utils.to_string(value,"parameter"))
    def make_savetime_line(self, time):
        return "# Saved on {0}".format(time.strftime("%Y/%m/%d %H:%M:%S"))
    
    @staticmethod
    def write_line(stream, line):
        if line is not None:
            stream.write(line+"\n")
    def write_comments(self, stream, comments):
        if self.save_comments and len(comments)>0:
            self.write_line(stream,"")
            for c in comments:
                self.write_line(stream,self.make_comment_line(c))
    def write_props(self, stream, props):
        if self.save_props and len(props)>0:
            self.write_line(stream,"")
            for name,value in props.items():
                self.write_line(stream,self.make_prop_line(name,value))
    def write_savetime(self, stream, time):
        if self.save_time:
            self.write_line(stream,"")
            self.write_line(stream,self.make_savetime_line(time))
    def write_file(self, location_file, to_save):
        with location_file.open("w") as stream:
            self.write_data(location_file,to_save.data)
            self.write_props(stream,to_save.props)
            self.write_comments(stream,to_save.comments)
            self.write_savetime(stream,datetime.datetime.now() if self.new_time else to_save.creation_time)
        

class CSVTableOutputFileFormat(ITextOutputFileFormat):
    """
    Class for CSV output file format.
    
    Args:
        delimiters (str): Used to separate entries in a row.
        value_formats (str): If not ``None``, defines value formats to be passed to :func:`.utils.string.to_string` function.
        use_rep_classes (bool): If ``True``, use representation classes for Dictionary entries (e.g., numpy arrays will be represented as ``"array([1, 2, 3])"`` instead of just ``"[1, 2, 3]"``);
            This improves storage fidelity, but makes result harder to parse (e.g., by external string parsers).
        save_columns (bool): If ``True``, save column names as a comment line in the beginning of the file.
        save_props (bool): If ``True`` and saving :class:`.datafile.DataFile` object, save its props metainfo.
        save_comments (bool): If ``True`` and saving :class:`.datafile.DataFile` object, save its comments metainfo.
        save_time (bool): If ``True``, append the file creation time in the end.
    """
    def __init__(self, delimiters="\t", value_formats=None, use_rep_classes=False, save_columns=True, save_props=True, save_comments=True, save_time=True):
        ITextOutputFileFormat.__init__(self,"csv",save_props,save_comments,save_time)
        self.delimiters=delimiters
        self.value_formats=value_formats
        self.use_rep_classes=use_rep_classes
        self.save_columns=save_columns
        
    def get_table_line(self, line):
        line=[string_utils.to_string(e,"entry",value_formats=self.value_formats,use_classes=self.use_rep_classes) for e in line]
        return self.delimiters.join(line)
    def get_columns_line(self, columns):
        if self.save_columns:
            return "# "+self.get_table_line(columns)
        else:
            return None
    def write_data(self, location_file, data):
        """
        Write data to a CSV file.
        
        Args:
            location_file: Location of the destination.
            data: Data to be saved. Can be a pandas DataFrame or an arbitrary 2D array (numpy array, 2D list, etc.);
                if the data is not DataFrame or numpy 2D array, it gets converted into a DataFrame using the standard constructor (i.e., 2D list is interpreted as a list of rows)
        """
        if not _is_table(data):
            data=pd.DataFrame(data)
        stream=location_file.stream
        if isinstance(data, pd.DataFrame):
            self.write_line(stream,self.get_columns_line(data.columns))
        for line in _table_row_iterator(data):
            self.write_line(stream,self.get_table_line(line))
        
        




class DictionaryOutputFileFormat(ITextOutputFileFormat):
    """
    Class for Dictionary output file format.
    
    Args:
        param_formats (str): If not ``None``, defines value formats to be passed to :func:`.utils.string.to_string` function when writing Dictionary entries.
        use_rep_classes (bool): If ``True``, use representation classes for Dictionary entries (e.g., numpy arrays will be represented as ``"array([1, 2, 3])"`` instead of just ``"[1, 2, 3]"``);
            This improves storage fidelity, but makes result harder to parse (e.g., by external string parsers).
        table_format (str): Default format for table (numpy arrays or pandas DataFrames) entries. Can be
            ``'inline'`` (table is written inside the file),
            ``'csv'`` (external CSV file) or
            ``'bin'`` (external binary file).
        inline_delimiters (str): Used to separate entries in a row for inline tables.
        inline_formats (str): If not ``None``, defines value formats to be passed to :func:`.utils.string.to_string` function when writing inline tables.
        save_props (bool): If ``True`` and saving :class:`.datafile.DataFile` object, save its props metainfo.
        save_comments (bool): If ``True`` and saving :class:`.datafile.DataFile` object, save its comments metainfo.
        save_time (bool): If ``True``, append the file creation time in the end.
    """
    def __init__(self, param_formats=None, use_rep_classes=False, table_format="inline", inline_delimiters="\t", inline_formats=None, save_props=True, save_comments=True, save_time=True):
        ITextOutputFileFormat.__init__(self,"dict",save_props,save_comments,save_time)
        self.param_formats=param_formats
        self.inline_delimiters=inline_delimiters
        self.table_format=table_format
        self.inline_formats=inline_formats
        self.use_rep_classes=use_rep_classes
    
    def get_dictionary_line(self, path, value):
        path=string_utils.escape_string("/".join(path),location="entry",escape_convertible=False)
        value=string_utils.to_string(value,"parameter",value_formats=self.param_formats,use_classes=self.use_rep_classes)
        return "{0}\t{1}".format(path,value)
    def _write_table_inline(self, stream, table):
        self.write_line(stream,"## Table start ##")
        for line in _table_row_iterator(table):
            line=[string_utils.to_string(e,"entry",value_formats=self.inline_formats,use_classes=self.use_rep_classes) for e in line]
            line=self.inline_delimiters.join(line)
            self.write_line(stream,line)
        self.write_line(stream,"## Table end ##")
    def write_data(self, location_file, data):
        """
        Write data to a Dictionary file.
        
        Args:
            location_file: Location of the destination.
            data: Data to be saved. Should be object of class :class:`.Dictionary`.
        """
        if not dictionary.is_dictionary(data):
            raise ValueError("format '{0}' can't save data {1}".format(self.format_name,data))
        loc=location_file.loc
        stream=location_file.stream
        table_builder=dict_entry.table_entry_builder(self.table_format)
        for path, value in data.iternodes(ordered=True,to_visit="leafs",include_path=True):
            if string_utils.is_convertible(value):
                self.write_line(stream,self.get_dictionary_line(path,value))
            elif isinstance(value,dict_entry.InlineTable):
                self.write_line(stream,self.get_dictionary_line(path,"table"))
                self._write_table_inline(stream,value.table)
            else:
                rel_path=path[len(data.get_path()):]
                dict_ptr=data.branch_pointer(rel_path)
                table_entry=dict_entry.from_data(value,[table_builder])
                if table_entry is None:
                    self.write_line(stream,self.get_dictionary_line(path,value))
                else:
                    d=table_entry.to_dict(dict_ptr,loc)
                    br=data.detach(rel_path)
                    data.add_entry(rel_path,d,branch_option="attach")
                    try:
                        self.write_data(location_file,data.branch_pointer(rel_path))
                    finally:
                        data.detach(rel_path)
                        data.add_entry(rel_path,br,branch_option="attach")
                
                
                


class IBinaryOutputFileFormat(IOutputFileFormat):  # pylint: disable=abstract-method
    def get_preamble(self, location_file, data):  # pylint: disable=unused-argument
        return dictionary.Dictionary()
    
    
class TableBinaryOutputFileFormat(IBinaryOutputFileFormat):
    """
    Class for binary output file format.
    
    Args:
        dtype: a string with numpy dtype (e.g., ``"<f8"``) used to save the data. By default, use little-endian (``"<"``) variant kind of the supplied data array dtype
        transposed (bool): If ``False``, write the data row-wise; otherwise, write it column-wise.
    """
    def __init__(self, dtype=None, transposed=False):
        IBinaryOutputFileFormat.__init__(self,"bin")
        self.dtype=dtype
        self.transposed=transposed
    
    def get_dtype(self, table):
        if self.dtype is None:
            return np.asarray(table).dtype.newbyteorder("<").str
        else:
            return self.dtype
    def get_preamble(self, location_file, data):
        """
        Generate a preamble (dictionary describing the file format).
        
        The parameters are ``'dtype'``, ``'packing'`` (``'transposed'`` or ``'flatten'``, depending on the `transposed` attribute),
        ``'ncol'`` (number of columns) and ``'nrows'`` (number of rows). 
        """
        preamble=dictionary.Dictionary()
        preamble["nrows"]=data.shape[0]
        preamble["ncols"]=data.shape[1]
        preamble["dtype"]=self.get_dtype(data)
        if self.transposed:
            preamble["packing"]="transposed"
        else:
            preamble["packing"]="flatten"
        return preamble
    def write_data(self, location_file, data):
        """
        Write data to a binary file.
        
        Args:
            location_file: Location of the destination.
            data: Data to be saved. Can be a pandas DataFrame or an arbitrary 2D array (numpy array, 2D list, etc.)
                Converted to numpy array before saving.
        """
        stream=location_file.stream
        data=np.asarray(data)
        dtype=self.get_dtype(data)
        if self.transposed:
            data=data.transpose()
        data.flatten().astype(dtype).tofile(stream,format=dtype)
    def write_file(self, location_file, to_save):
        data=to_save.data
        if _is_table(data):
            with location_file.open("wb"):
                self.write_data(location_file,data)
        else:
            raise ValueError("can't save data {}".format(data))
        
        
        
        
        
def get_output_format(data, output_format, **kwargs):
    if isinstance(output_format, IOutputFileFormat):
        return data,output_format
    if output_format=="csv":
        return data,CSVTableOutputFileFormat(**kwargs)
    elif output_format=="csv_desc":
        data=dict_entry.InlineTableDictionaryEntry(data,**kwargs)
        data=dictionary.Dictionary({"__data__":data})
        return data,DictionaryOutputFileFormat()
    elif output_format=="dict":
        return dictionary.as_dictionary(data),DictionaryOutputFileFormat(**kwargs)
    elif output_format=="bin":
        return data,TableBinaryOutputFileFormat(**kwargs)
    elif output_format=="bin_desc":
        data=dict_entry.ExternalBinTableDictionaryEntry(data,name="data|bin",force_name=True,**kwargs)
        data=dictionary.Dictionary({"__data__":data})
        return data,DictionaryOutputFileFormat()
    else:
        raise ValueError("unknown output file format: {0}".format(output_format))




def save_csv(data, path, delimiters="\t", value_formats=None, use_rep_classes=False, save_columns=True, save_props=True, save_comments=True, save_time=True, loc="file"):
    """
    Save data to a CSV file.
    
    Args:
        data: Data to be saved (2D numpy array, pandas DataFrame, or a :class:`.datafile.DataFile` object containing this data).
        path (str): Path to the file or a file-like object.
        delimiters (str): Used to separate entries in a row.
        value_formats (str): If not ``None``, defines value formats to be passed to :func:`.utils.string.to_string` function.
        use_rep_classes (bool): If ``True``, use representation classes for Dictionary entries (e.g., numpy arrays will be represented as ``"array([1, 2, 3])"`` instead of just ``"[1, 2, 3]"``);
            This improves storage fidelity, but makes result harder to parse (e.g., by external string parsers).
        save_columns (bool): If ``True``, save column names as a comment line in the beginning of the file.
        save_props (bool): If ``True`` and saving :class:`.datafile.DataFile` object, save its props metainfo.
        save_comments (bool): If ``True`` and saving :class:`.datafile.DataFile` object, save its comments metainfo.
        save_time (bool): If ``True``, append the file creation time in the end.
        loc (str): Location type.
    """
    data,output_format=get_output_format(data,"csv",delimiters=delimiters,value_formats=value_formats,use_rep_classes=use_rep_classes,save_columns=save_columns,
        save_props=save_props,save_comments=save_comments,save_time=save_time)
    f=location.LocationFile(location.get_location(path,loc))
    output_format.write(f,data)

def save_csv_desc(data, path, loc="file"):
    """
    Save data table to a dictionary file with an inlined table.

    Compared to :func:`save_csv`, supports more pandas features (index, column multi-index), but can only be directly read by pylablib.
    
    Args:
        data: Data to be saved (2D numpy array, pandas DataFrame, or a :class:`.datafile.DataFile` object containing this data).
        path (str): Path to the file or a file-like object.
        loc (str): Location type.
    """
    data,output_format=get_output_format(data,"csv_desc")
    f=location.LocationFile(location.get_location(path,loc))
    output_format.write(f,data)

def save_bin(data, path, dtype=None, transposed=False, loc="file"):
    """
    Save data to a binary file.
    
    Args:
        data: Data to be saved (2D numpy array, pandas DataFrame, or a :class:`.datafile.DataFile` object containing this data).
        path (str): Path to the file or a file-like object.
        dtype: :class:`numpy.dtype` describing the data. By default, use little-endian (``"<"``) variant kind of the supplied data array dtype.
        transposed (bool): If ``False``, write the data row-wise; otherwise, write it column-wise.
        loc (str): Location type.
    """
    data,output_format=get_output_format(data,"bin",dtype=dtype,transposed=transposed)
    f=location.LocationFile(location.get_location(path,loc))
    output_format.write(f,data)

def save_bin_desc(data, path, loc="file"):
    """
    Save data to a binary file with an additional description file, which contains all of the data related to loading (shape, dtype, columns, etc.)
    
    Args:
        data: Data to be saved (2D numpy array, pandas DataFrame, or a :class:`.datafile.DataFile` object containing this data).
        path (str): Path to the file or a file-like object.
        loc (str): Location type.
    """
    data,output_format=get_output_format(data,"bin_desc")
    f=location.LocationFile(location.get_location(path,loc))
    output_format.write(f,data)

def save_dict(data, path, param_formats=None, use_rep_classes=False, table_format="inline", inline_delimiters="\t", inline_formats=None, save_props=True, save_comments=True, save_time=True, loc="file"):
    """
    Save dictionary to a text file.
    
    Args:
        data: Data to be saved.
        path (str): Path to the file or a file-like object.
        param_formats (str): If not ``None``, defines value formats to be passed to :func:`.utils.string.to_string` function when writing Dictionary entries.
        use_rep_classes (bool): If ``True``, use representation classes for Dictionary entries (e.g., numpy arrays will be represented as ``"array([1, 2, 3])"`` instead of just ``"[1, 2, 3]"``);
            This improves storage fidelity, but makes result harder to parse (e.g., by external string parsers).
        table_format (str): Default format for table (numpy arrays or pandas DataFrames) entries. Can be
            ``'inline'`` (table is written inside the file),
            ``'csv'`` (external CSV file) or
            ``'bin'`` (external binary file).
        inline_delimiters (str): Used to separate entries in a row for inline tables.
        inline_formats (str): If not ``None``, defines value formats to be passed to :func:`.utils.string.to_string` function when writing inline tables.
        save_props (bool): If ``True`` and saving :class:`.datafile.DataFile` object, save its props metainfo.
        save_comments (bool): If ``True`` and saving :class:`.datafile.DataFile` object, save its comments metainfo.
        save_time (bool): If ``True``, append the file creation time in the end.
        loc (str): Location type.
    """
    data,output_format=get_output_format(data,"dict",param_formats=param_formats,use_rep_classes=use_rep_classes,table_format=table_format,inline_delimiters=inline_delimiters,
        inline_formats=inline_formats,save_props=save_props,save_comments=save_comments,save_time=save_time)
    f=location.LocationFile(location.get_location(path,loc))
    output_format.write(f,data)





def save_generic(data, path, output_format=None, loc="file", **kwargs):
    """
    Save data to a file.
    
    Args:
        data: Data to be saved.
        path (str): Path to the file or a file-like object.
        output_format (str): Output file format. Can be either
            ``None`` (defaults to ``'csv'`` for table data and ``'dict'`` for Dictionary data),
            a string with one of the default format names, or 
            an already prepared :class:`IOutputFileFormat` object. 
        loc (str): Location type.
    
    `**kwargs` are passed to the file formatter constructor
    (see :class:`CSVTableOutputFileFormat`, :class:`DictionaryOutputFileFormat` and :class:`TableBinaryOutputFileFormat` for the possible arguments).
    The default format names are:
    
        - ``'csv'``: CSV file, corresponds to :class:`CSVTableOutputFileFormat` and :func:`save_csv`;
        - ``'csv'``: CSV file with an additional dictionary containing format description, corresponds to :class:`DictionaryOutputFileFormat` and :func:`save_csv_desc`;
        - ``'bin'``: Binary file, corresponds to :class:`TableBinaryOutputFileFormat` and :func:`save_bin`;
        - ``'bin_desc'``: Binary file with an additional dictionary containing format description, corresponds to :class:`DictionaryOutputFileFormat` and :func:`save_bin_desc`;
        - ``'dict'``: Dictionary file, corresponds to :class:`DictionaryOutputFileFormat` and :func:`save_dict`
    """
    if output_format is None:
        if _is_table(data,allow_1D=True) or (_is_file(data) and _is_table(data.data)):
            output_format="csv"
        elif dictionary.is_dictionary(data) or isinstance(data,dict) or (_is_file(data) and (dictionary.is_dictionary(data.data) or isinstance(data.data,dict))):
            output_format="dict"
        else:
            raise ValueError("can't determine output file format for data: {}".format(data))
    data,output_format=get_output_format(data,output_format,**kwargs)
    loc=location.get_location(path,loc)
    f=location.LocationFile(loc)
    output_format.write(f,data)