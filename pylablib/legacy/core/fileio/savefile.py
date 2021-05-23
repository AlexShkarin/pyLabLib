"""
Utilities for writing data files.
"""

from future.utils import viewitems

from . import datafile
from . import location
from . import dict_entry

from ..utils import string as string_utils  #@UnresolvedImport
from ..utils import files as file_utils  #@UnresolvedImport
from ..utils import general as general_utils  #@UnresolvedImport
from ..utils import dictionary  #@UnresolvedImport
from ..utils import log #@UnresolvedImport
from ..datatable import table as datatable  #@UnresolvedImport

import numpy as np
import pandas as pd
import datetime




def _is_file(value):
    return isinstance(value,datafile.DataFile)

def _is_table(value, allow_1D=False):
    return isinstance(value, datatable.DataTable) \
        or (isinstance(value, np.ndarray) and (value.ndim==2 or (allow_1D and value.ndim==1)) ) \
        or (isinstance(value, pd.DataFrame))
def _table_row_iterator(value):
    if isinstance(value, datatable.DataTable):
        return value.r
    elif isinstance(value, pd.DataFrame):
        return value.itertuples(index=False)
    else:
        return value



##### FILE FORMAT #####

class IOutputFileFormat(object):
    """
    Generic class for an output file format.
    
    Args:
        format_name (str): The name of the format (to be defined in subclasses).
        default_kwargs (dict): Default `**kwargs` values for the :meth:`write` method.
    """
    def __init__(self, format_name, default_kwargs=None):
        object.__init__(self)
        self.format_name=format_name
        self.default_kwargs=default_kwargs or {}
    
    def write_file(self, location_file, to_save, *args, **kwargs):
        raise NotImplementedError("IOutputFileFormat.write_file")
    
    def write(self, location_file, data, *args, **kwargs):
        if not _is_file(data):
            data=datafile.DataFile(data)
        self.write_file(location_file,data,*args,**general_utils.merge_dicts(self.default_kwargs,kwargs))




class ITextOutputFileFormat(IOutputFileFormat):
    """
    Generic class for a text output file format.
    
    Args:
        format_name (str): The name of the format (to be defined in subclasses).
        save_props (bool): If ``True`` and saving `~datafile.DataFile` object, save its props metainfo.
        save_comments (bool): If ``True`` and saving `~datafile.DataFile` object, save its comments metainfo.
        save_time (bool): If ``True``, append the file creation time in the end.
        new_time (bool): If saving `~datafile.DataFile` object, determines if the time should be updated to the current time.
        default_kwargs (dict): Default `**kwargs` values for the :meth:`IOutputFileFormat.write` method.
    """
    def __init__(self, format_name, save_props=True, save_comments=True, save_time=True, new_time=True, default_kwargs=None):
        IOutputFileFormat.__init__(self,format_name,default_kwargs)
        self.save_props=save_props
        self.save_comments=save_comments
        self.save_time=save_time
        self.new_time=new_time
    
    def get_comment_line(self, comment):
        return "# "+string_utils.escape_string(comment,"parameter")
    def get_prop_line(self, name, value):
        return "# {0} :\t{1}".format(name,string_utils.to_string(value,"parameter"))
    def get_time_line(self, time):
        return "# Saved on {0}".format(time.strftime("%Y/%m/%d %H:%M:%S"))
    
    @staticmethod
    def write_line(stream, line):
        if line is not None:
            stream.write(line+"\n")
    def write_comments(self, stream, comments):
        if self.save_comments and len(comments)>0:
            self.write_line(stream,"")
            for c in comments:
                self.write_line(stream,self.get_comment_line(c))
    def write_props(self, stream, props):
        if self.save_props and len(props)>0:
            self.write_line(stream,"")
            for name,value in viewitems(props):
                self.write_line(stream,self.get_prop_line(name,value))
    def write_time(self, stream, time):
        if self.save_time:
            self.write_line(stream,"")
            self.write_line(stream,self.get_time_line(time))
    def write_file(self, location_file, to_save, *args, **vargs):
        with location_file.opening(mode="write",data_type="text"):
            self.write_data(location_file,to_save.data,*args,**vargs)
            self.write_props(location_file.stream,to_save.props)
            self.write_comments(location_file.stream,to_save.comments)
            self.write_time(location_file.stream,datetime.datetime.now() if self.new_time else to_save.creation_time)
    def write_data(self, location_file, data, **kwargs):
        raise NotImplementedError("ITextOutputFileFormat.write_data")
        

class CSVTableOutputFileFormat(ITextOutputFileFormat):
    """
    Class for CSV output file format.
    
    Args:
        save_props (bool): If ``True`` and saving `~datafile.DataFile` object, save its props metainfo.
        save_comments (bool): If ``True`` and saving `~datafile.DataFile` object, save its comments metainfo.
        save_time (bool): If ``True``, append the file creation time in the end.
        columns_delimiter (str): Used to separate entries in a row.
        custom_reps (str): If not ``None``, defines custom representations to be passed to :func:`.utils.string.to_string` function.
        use_rep_classes (bool): If ``True``, use representation classes for Dictionary entries (e.g., numpy arrays will be represented as ``"array([1, 2, 3])"`` instead of just ``"[1, 2, 3]"``);
            This improves storage fidelity, but makes result harder to parse (e.g., by external string parsers).
        **kwargs (dict): Default `**kwargs` values for the :meth:`IOutputFileFormat.write` method.
    """
    def __init__(self, save_props=True, save_comments=True, save_time=True, save_columns=True, columns_delimiter="\t", custom_reps=None, use_rep_classes=False, **kwargs):
        ITextOutputFileFormat.__init__(self,"csv",save_props,save_comments,save_time,default_kwargs=kwargs)
        self.save_columns=save_columns
        self.columns_delimiter=columns_delimiter
        self.custom_reps=custom_reps
        self.use_rep_classes=use_rep_classes
        
    def get_table_line(self, line):
        line=[string_utils.to_string(e,"entry",self.custom_reps,use_classes=self.use_rep_classes) for e in line]
        return self.columns_delimiter.join(line)
    def get_columns_line(self, columns):
        if self.save_columns:
            return "# "+self.get_table_line(columns)
        else:
            return None
    def write_data(self, location_file, data, columns=None, **kwargs):
        """
        Write data to a CSV file.
        
        Args:
            location_file: Location of the destination.
            data: Data to be saved. Can be :class:`.DataTable` or an arbitrary 2D array (numpy array, 2D list, etc.).
            columns ([str]): If not ``None``, the list of column names.
                If ``None`` and data is of type :class:`.DataTable`, use its columns names.
                If ``None`` and data is of other type, don't put the column line in the output.
        """
        if not _is_table(data):
            data=datatable.DataTable(data)
            #raise ValueError("format '{0}' can't save data {1}".format(self.format_name,data))
        stream=location_file.stream
        if columns is None and data is not None:
            if isinstance(data, datatable.DataTable):
                columns=data.get_column_names()
            elif isinstance(data, pd.DataFrame):
                columns=data.columns
        if columns is not None:
            self.write_line(stream,self.get_columns_line(columns))
        for line in _table_row_iterator(data):
            self.write_line(stream,self.get_table_line(line))
        
        




class DictionaryOutputFileFormat(ITextOutputFileFormat):
    """
    Class for Dictionary output file format.
    
    Args:
        save_props (bool): If ``True`` and saving `~datafile.DataFile` object, save its props metainfo.
        save_comments (bool): If ``True`` and saving `~datafile.DataFile` object, save its comments metainfo.
        save_time (bool): If ``True``, append the file creation time in the end.
        table_format (str): Default format for table (numpy arrays or :class:`.DataTable` objects) entries. Can be
            ``'inline'`` (table is written inside the file),
            ``'csv'`` (external CSV file) or
            ``'bin'`` (external binary file).
        inline_columns_delimiter (str): Used to separate entries in a row for inline tables.
        inline_reps (str): If not ``None``, defines custom representations to be passed to :func:`.utils.string.to_string` function when writing inline tables.
        param_reps (str): If not ``None``, defines custom representations to be passed to :func:`.utils.string.to_string` function when writing Dictionary entries.
        use_rep_classes (bool): If ``True``, use representation classes for Dictionary entries (e.g., numpy arrays will be represented as ``"array([1, 2, 3])"`` instead of just ``"[1, 2, 3]"``);
            This improves storage fidelity, but makes result harder to parse (e.g., by external string parsers).
        **kwargs (dict): Default `**kwargs` values for the :meth:`IOutputFileFormat.write` method.
    """
    def __init__(self, save_props=True, save_comments=True, save_time=True, table_format="inline", inline_columns_delimiter="\t", inline_reps=None, param_reps=None, use_rep_classes=False, **kwargs):
        ITextOutputFileFormat.__init__(self,"dict",save_props,save_comments,save_time,default_kwargs=kwargs)
        self.inline_columns_delimiter=inline_columns_delimiter
        self.table_format=table_format
        self.inline_reps=inline_reps
        self.param_reps=param_reps
        self.use_rep_classes=use_rep_classes
    
    def get_dictionary_line(self, path, value):
        path="/".join(path)
        value=string_utils.to_string(value,"parameter",self.param_reps,use_classes=self.use_rep_classes)
        return "{0}\t{1}".format(path,value)
    def _write_table_inline(self, stream, table):
        self.write_line(stream,"## Table start ##")
        for line in _table_row_iterator(table):
            line=[string_utils.to_string(e,"entry",self.inline_reps) for e in line]
            line=self.inline_columns_delimiter.join(line)
            self.write_line(stream,line)
        self.write_line(stream,"## Table end ##")
    def write_data(self, loc_file, data, **kwargs):
        """
        Write data to a Dictionary file.
        
        Args:
            location_file: Location of the destination.
            data: Data to be saved. Can be :class:`.DataTable` or an arbitrary 2D array (numpy array, 2D list, etc.).
        """
        if not dictionary.is_dictionary(data):
            raise ValueError("format '{0}' can't save data {1}".format(self.format_name,data))
        loc=loc_file.loc
        stream=loc_file.stream
        for path, value in data.iternodes(ordered=True,to_visit="leafs",include_path=True):
            if string_utils.is_convertible(value):
                self.write_line(stream,self.get_dictionary_line(path,value))
            elif isinstance(value,dict_entry.InlineTable):
                self.write_line(stream,self.get_dictionary_line(path,"table"))
                self._write_table_inline(stream,value.table)
            else:
                rel_path=path[len(data.get_path()):]
                dict_ptr=data.branch_pointer(rel_path)
                table_entry=dict_entry.build_entry(value,table_format=self.table_format)
                if table_entry is None:
                    log.default_log.info("No formatter for {0}".format(value),origin="fileio/savefile",level="warning")
                    self.write_line(stream,self.get_dictionary_line(path,value))
                else:
                    d=table_entry.to_dict(dict_ptr,loc)
                    br=data.detach_branch(rel_path)
                    data.add_entry(rel_path,d,branch_option="attach")
                    try:
                        self.write_data(loc_file,data.branch_pointer(rel_path),**kwargs)
                    finally:
                        data.detach_branch(rel_path)
                        data.add_entry(rel_path,br,branch_option="attach")
                
                
                


class IBinaryOutputFileFormat(IOutputFileFormat):
    def __init__(self, format_name, default_kwargs=None):
        IOutputFileFormat.__init__(self,format_name,default_kwargs)
    def get_preamble(self, loc_file, data):
        return dictionary.Dictionary()
    
    
class TableBinaryOutputFileFormat(IBinaryOutputFileFormat):
    """
    Class for binary output file format.
    
    Args:
        dtype: :class:`numpy.dtype` describing the data. By default, ``'>f8'`` for real data and ``'>c16'`` for complex data.
        transposed (bool): If ``False``, write the data row-wise; otherwise, write it column-wise.
        **kwargs (dict): Default `**kwargs` values for the :meth:`IOutputFileFormat.write` method.
    """
    def __init__(self, dtype=None, transposed=False, **kwargs):
        IBinaryOutputFileFormat.__init__(self,"bin",default_kwargs=kwargs)
        self.dtype=dtype
        self.transposed=transposed
    
    def get_dtype(self, table):
        if self.dtype is None:
            if np.iscomplexobj(table):
                return ">c16"
            else:
                return ">f8"
        else:
            return self.dtype
    def get_preamble(self, loc_file, data):
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
    def write_table(self, location_file, data):
        """
        Write data to a binary file.
        
        Args:
            location_file: Location of the destination.
            data: Data to be saved. Can be :class:`.DataTable` or an arbitrary 2D array (numpy array, 2D list, etc.).
                Converted to numpy array before saving.
        """
        stream=location_file.stream
        dtype=self.get_dtype(data)
        data=np.asarray(data)
        if self.transposed:
            data=data.transpose()
        data.flatten().astype(dtype).tofile(stream,format=dtype)
    def write_file(self, location_file, to_save, **kwargs):
        data=to_save.data
        if _is_table(data):
            with location_file.opening(mode="write",data_type="binary"):
                self.write_table(location_file,data)
        else:
            raise ValueError("Can't save data {}".format(data))
        
        
        
        
        
def get_output_format(data, output_format, **kwargs):
    if isinstance(output_format, IOutputFileFormat):
        return data,output_format
    if output_format=="csv":
        return data,CSVTableOutputFileFormat(**kwargs)
    elif output_format=="dict":
        return data,DictionaryOutputFileFormat(**kwargs)
    elif output_format=="bin":
        return data,TableBinaryOutputFileFormat(**kwargs)
    elif output_format=="bin_desc":
        data=dict_entry.ExternalBinTableDictionaryEntry(data,name="data|bin",force_name=True,**kwargs)
        data=dictionary.Dictionary({"data":data})
        return data,DictionaryOutputFileFormat()
    else:
        raise ValueError("unknown output file format: {0}".format(output_format))
        
        
        
        
def save(data, path="", output_format=None, loc="file", **kwargs):
    """
    Save data to a file.
    
    Args:
        data: Data to be saved.
        path (str): Path to the file.
        output_format (str): Output file format. Can be either
            ``None`` (defaults to ``'csv'`` for table data and ``'dict'`` for Dictionary data),
            a string with one of the default format names, or 
            an already prepared :class:`IOutputFileFormat` object. 
        loc (str): Location type.
    
    `**kwargs` are passed to the file formatter constructor
    (see :class:`CSVTableOutputFileFormat`, :class:`DictionaryOutputFileFormat` and :class:`TableBinaryOutputFileFormat` for the possible arguments).
    The default format names are:
    
        - ``'csv'``: CSV file, corresponds to :class:`CSVTableOutputFileFormat`;
        - ``'dict'``: Dictionary file, corresponds to :class:`DictionaryOutputFileFormat`;
        - ``'bin'``: Binary  file, corresponds to :class:`TableBinaryOutputFileFormat`
    """
    if output_format is None:
        if _is_table(data,allow_1D=True) or (_is_file(data) and _is_table(data.data)):
            output_format="csv"
        elif dictionary.is_dictionary(data) or (_is_file(data) and dictionary.is_dictionary(data.data)):
            output_format="dict"
        else:
            raise ValueError("can't determine output file format for data: {}".format(data))
    data,output_format=get_output_format(data,output_format,**kwargs)
    loc=location.get_location(loc,path)
    f=location.LocationFile(loc)
    output_format.write(f,data)