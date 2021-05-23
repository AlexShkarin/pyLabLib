"""
Utilities for reading data files.
"""

from builtins import bytes, range

from . import datafile, location, dict_entry, parse_csv  #@UnresolvedImport

from ..utils import dictionary, funcargparse, string  #@UnresolvedImport

import datetime
import re
import numpy as np

_depends_local=[".parse_csv"]
_module_parameters={"fileio/loadfile/csv/out_type":"table"}

##### File type detection #####

def _is_unprintable_character(chn):
    return chn<8 or 13<chn<27 or 27<chn<32
def _detect_binary_file(stream):
    pos=stream.tell()
    chunk=bytes(stream.read(4096))
    stream.seek(pos)
    for c in chunk:
        if _is_unprintable_character(c):
            return True
    return False

_dict_line_soft=r"^[\S]*(/[\S]*)*\s+"
_dict_line_soft_regexp=re.compile(_dict_line_soft)
_dict_line_hard=r"^[\w]*(/[\w]*)+\s+"
_dict_line_hard_regexp=re.compile(_dict_line_hard)
_dicttable_line=r"^#+\s*table\s+(start|end)"
_dicttable_line_regexp=re.compile(_dicttable_line)
## single comma with whitespaces, or just whitespaces, but no less than 3 spaces in a row
##_table_delimiters_hard=r"\s*(,|   )\s*|[\f\n\r\t\v]+"
##_table_delimiters_hard_regexp=re.compile(_table_delimiters_hard)
def _try_row_type(line):
    """
    Try to determine whether the line is a comment line, a numerical data row, a dictionary row or an unrecognized row.
    
    Doesn't distinguish with a great accuracy; useful only for trying to guess file format. 
    """
    line=line.strip().lower()
    if line=="":
        return "empty"
    if _dicttable_line_regexp.match(line):
        return "dict_table"
    if line[0]=="#":
        return "comment"
    if _dict_line_hard_regexp.match(line):
        return "dict"
    split_line=parse_csv._table_delimiters_regexp.split(line)
    split_line=[el for el in split_line if el!=""]
    try:
        for e in split_line:
            if not e in {"","nan",'inf',"+inf","-inf"}:
                complex(e.replace("i","j"))
        return "numerical"
    except ValueError:
        return "unrecognized"
def _detect_textfile_type(stream):
    line_type_count={"empty":0,"dict":0,"dict_table":0,"comment":0,"numerical":0,"unrecognized":0}
    pos=stream.tell()
    data_lines=0
    while data_lines<20:
        l=stream.readline()
        if l=="":
            break
        line_type=_try_row_type(l)
        line_type_count[line_type]=line_type_count[line_type]+1
        if line_type in {"dict","numerical"}:
            data_lines=data_lines+1
    stream.seek(pos)
    if line_type_count["dict_table"]>0 and data_lines>2:
        return "dict"
    if data_lines<5 and data_lines<line_type_count["unrecognized"]*2:
        return "unrecognized"
    if line_type_count["dict"]>line_type_count["numerical"]:
        return "dict"
    else:
        return "table"
    
_time_expr=r"(\d+)\s*/\s*(\d+)\s*/\s*(\d+)\s+(\d+)\s*:\s*(\d+)\s*:\s*(\d+)(.\d+)?"
_time_comment=r"(?:saved|created)\s+(?:on|at)\s*"+_time_expr
_time_comment_regexp=re.compile(_time_comment,re.IGNORECASE)
def _try_time_comment(line):
    m=_time_comment_regexp.match(line)
    if m is None:
        return None
    else:
        year,month,day,hour,minute,second,usec=m.groups()
        usec=usec or 0
        return datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second),int(float(usec)*1E6))
def _try_columns_line(line, row_size):
    split_line=string.from_row_string(line,parse_csv._table_delimiters_regexp)
    if len(split_line)!=row_size:
        return None
    try:
        for e in split_line:
            complex(e.replace("i","j"))
        return None # all numerical, can't be column names
    except (ValueError, AttributeError):
        return split_line
def _find_columns_lines(corrupted, comments, row_size):
    if len(corrupted["type"])>0:
        return corrupted["type"][0],None
    for i,l in enumerate(comments):
        columns=_try_columns_line(l,row_size)
        if columns is not None:
            return columns,i
    return None,None



def _parse_dict_line(line):
    s=line.split(None,1)
    if len(s)==0:
        return None
    if len(s)==1:
        return tuple(s)
    key,value=tuple(s)
    value=string.from_string(value)
    return key,value

_dicttable_start=r"^#+\s*(table\s+start|start\s+table)"
_dicttable_start_regexp=re.compile(_dicttable_start,re.IGNORECASE)
_dicttable_end=r"^#+\s*(table\s+end|end\s+table)"
_dicttable_end_regexp=re.compile(_dicttable_end,re.IGNORECASE)
def _load_dict_and_comments(f, case_normalization=None, inline_dtype="generic"):
    case_sensitive=case_normalization is None
    data=dictionary.Dictionary(case_sensitive=case_sensitive, case_normalization=case_normalization or "lower")
    comment_lines=[]
    line=f.readline()
    root_keys=[]
    prev_key=None
    while line:
        line=line.strip()
        if line!="":
            if line[:1]!='#': #dict row
                parsed=_parse_dict_line(line)
                if parsed is not None:
                    if len(parsed)==1:
                        key=parsed[0]
                        if key.startswith("///"): # root key one level up
                            root_keys=root_keys[:-1]
                        elif key.startswith("//"): # new nested root key
                            root_keys.append(key[2:])
                        else:
                            if root_keys:
                                key="/".join(root_keys)+"/"+key
                            prev_key=(key,) # single-key line possibly means that an inline table follows
                    else:
                        key,value=parsed
                        if root_keys:
                            key="/".join(root_keys)+"/"+key
                        data[key]=value
                        prev_key=key
            else:
                if _dicttable_start_regexp.match(line[1:]) is not None:
                    table,comments,corrupted=parse_csv.load_table(f,dtype=inline_dtype,stop_comment=_dicttable_end_regexp)
                    columns,comment_idx=_find_columns_lines(corrupted,comments,table.shape[1])
                    if comment_idx is not None:
                        del comments[comment_idx]
                    if columns is not None:
                        table.set_column_names(columns)
                    comment_lines=comment_lines+comments
                    if prev_key is not None:
                        data[prev_key]=table
                    else:
                        raise IOError("inline table isn't attributed to any dict node")
                else:
                    comment_lines.append(line.lstrip("# \t"))
        line=f.readline()
    return (data,comment_lines)


##### Data normalization #####

def _extract_savetime_comment(comments):
    if len(comments)==0:
        return None
    for i,c in enumerate(comments):
        creation_time=_try_time_comment(c)
        if creation_time is not None:
            break
    if i<len(comments):
        del comments[i]
    return creation_time
def _determine_columns_comment(comment):
    pass





##### File formats #####


class IInputFileFormat(object):
    """
    Generic class for an input file format.
    
    Based on `file_format` or autodetection, calls one of its subclasses to read the file.
    """
    def __init__(self):
        object.__init__(self)
    
    @staticmethod
    def read_file(location_file, file_format, **kwargs):
        file_format=file_format or "generic"
        if file_format in {"txt","csv","dict"}:
            return ITextInputFileFormat.read_file(location_file,file_format=file_format,**kwargs)
        if file_format in {"bin"}:
            return BinaryTableInputFileFormatter.read_file(location_file,file_format=file_format,**kwargs)
        if file_format in {"generic"}:
            with location_file.opening(mode="read",data_type="binary"):
                is_binary=_detect_binary_file(location_file.stream)
            if is_binary:
                return BinaryTableInputFileFormatter.read_file(location_file,file_format="bin",**kwargs)
            else:
                return ITextInputFileFormat.read_file(location_file,file_format="txt",**kwargs)
    
    
    
class ITextInputFileFormat(IInputFileFormat):
    """
    Generic class for a text input file format.
    
    Based on `file_format` or autodetection, calls one of its subclasses to read the file.
    """
    def __init__(self):
        IInputFileFormat.__init__(self)
    
    @staticmethod
    def read_file(location_file, file_format, **kwargs):
        if file_format in {"csv"}:
            return CSVTableInputFileFormat.read_file(location_file,file_format=file_format,**kwargs)
        if file_format in {"dict"}:
            return DictionaryInputFileFormat.read_file(location_file,file_format=file_format,**kwargs)
        if file_format in {"txt"}:
            with location_file.opening(mode="read",data_type="text"):
                txt_type=_detect_textfile_type(location_file.stream)
            if txt_type=="table":
                return CSVTableInputFileFormat.read_file(location_file,file_format="csv",**kwargs)
            elif txt_type=="dict":
                return DictionaryInputFileFormat.read_file(location_file,file_format="dict",**kwargs)
            else:
                raise IOError("can't determine file type")
            
            
class CSVTableInputFileFormat(ITextInputFileFormat):
    """
    Class for CSV input file format.
    """
    def __init__(self):
        ITextInputFileFormat.__init__(self)
    @staticmethod
    def read_file(location_file, out_type="default", dtype="numeric", columns=None, delimiters=None, empty_entry_substitute=None, ignore_corrupted_lines=True, skip_lines=0, **kwargs):
        """
        Read CSV file.
        
        See :func:`.parse_csv.load_table` for more description.
        
        Args:
            location_file: Location of the data.
            out_type (str): type of the result: ``'array'`` for numpy array, ``'pandas'`` for pandas DataFrame, ``'table'`` for :class:`.DataTable` object,
                or ``'default'`` (determined by the library default; ``'table'`` by default)
            dtype: dtype of entries; can be either a single type, or a list of types (one per column).
                Possible dtypes are: ``'int'``, ``'float'``, ``'complex'``,
                ``'numeric'`` (tries to coerce to minimal possible numeric type, raises error if data can't be converted to `complex`),
                ``'generic'`` (accept arbitrary types, including lists, dictionaries, escaped strings, etc.),
                ``'raw'`` (keep raw string).
            columns: either a number if columns, or a list of columns names.
            delimiters (str): Regex string which recognizes entries delimiters (by default ``r"\\s*,\\s*|\\s+"``, i.e., commas and whitespaces).
            empty_entry_substitute: Substitute for empty table entries. If ``None``, all empty table entries are skipped.
            ignore_corrupted_lines (bool): If ``True``, skip corrupted (e.g., non-numeric for numeric dtype, or with too few entries) lines;
                otherwise, raise :exc:`ValueError`.
            skip_lines (int): Number of lines to skip from the beginning of the file.
        """
        if out_type=="default":
            out_type=_module_parameters["fileio/loadfile/csv/out_type"]
        if delimiters is None:
            delimiters=parse_csv._table_delimiters
        with location_file.opening(mode="read",data_type="text"):
            for _ in range(skip_lines):
                location_file.stream.readline()
            data,comments,corrupted=parse_csv.load_table(location_file.stream,dtype=dtype,columns=columns,out_type=out_type,
                            delimiters=delimiters,empty_entry_substitute=empty_entry_substitute,ignore_corrupted_lines=ignore_corrupted_lines)
        if out_type in {"table","pandas"} and not funcargparse.is_sequence(columns,"builtin;nostring") and len(data)>0:
            columns,comment_idx=_find_columns_lines(corrupted,comments,data.shape[1])
            if comment_idx is not None:
                del comments[comment_idx]
            if columns is not None:
                if out_type=="table":
                    data.set_column_names(columns)
                else:
                    data.columns=columns
        creation_time=_extract_savetime_comment(comments)
        return datafile.DataFile(data=data,comments=comments,creation_time=creation_time,filetype="csv")
    
class DictionaryInputFileFormat(ITextInputFileFormat):
    """
    Class for Dictionary input file format.
    """
    def __init__(self):
        ITextInputFileFormat.__init__(self)
    @staticmethod
    def read_file(location_file, case_normalization=None, inline_dtype="generic", entry_format="value", skip_lines=0, **kwargs):
        """
        Read Dictionary file.
        
        Args:
            location_file: Location of the data.
            case_normalization (str): If ``None``, the dictionary paths are case-sensitive;
                otherwise, defines the way the entries are normalized (``'lower'`` or ``'upper'``).
            inline_dtype (str): dtype for inlined tables.
            entry_format (str): Determines the way for dealing with :class:`.dict_entry.IDictionaryEntry` objects
                (objects transformed into dictionary branches with special recognition rules). Can be
                ``'branch'`` (don't attempt to recognize those object, leave dictionary as in the file),
                ``'dict_entry'`` (recognize and leave as :class:`.dict_entry.IDictionaryEntry` objects) or
                ``'value'`` (recognize and keep the value).
            skip_lines (int): Number of lines to skip from the beginning of the file.
        """
        if not entry_format in {"branch","dict_entry","value"}:
            raise ValueError("unrecognized entry format: {0}".format(entry_format))
        with location_file.opening(mode="read",data_type="text"):
            for _ in range(skip_lines):
                location_file.stream.readline()
            data,comments=_load_dict_and_comments(location_file.stream,inline_dtype=inline_dtype,case_normalization=case_normalization)
        creation_time=_extract_savetime_comment(comments)
        def map_entries(ptr):
            if dict_entry.special_load_rules(ptr):
                entry=dict_entry.from_dict(ptr,location_file.loc)
                if entry_format=="value":
                    entry=entry.data
                return entry
            else:
                return ptr
        if entry_format!="branch":
            data.map_self(map_entries,to_visit="branches",topdown=False)
        if len(data)==1 and list(data.keys())==["__data__"]: # special case of files with preamble
            data=data["__data__"]
        return datafile.DataFile(data=data,comments=comments,creation_time=creation_time,filetype="dict")
    
    
    
    
    
class BinaryTableInputFileFormatter(IInputFileFormat):
    """
    Class for binary input file format.
    """
    def __init__(self):
        IInputFileFormat.__init__(self)
    
    @staticmethod
    def read_file(location_file, out_type="default", dtype=">f8", columns=None, packing="flatten", preamble=None, skip_bytes=0, **kwargs):
        
        """
        Read binary file.
        
        Args:
            location_file: Location of the data.
            out_type (str): type of the result: ``'array'`` for numpy array, ``'pandas'`` for pandas DataFrame, ``'table'`` for :class:`.DataTable` object,
                or ``'default'`` (determined by the library default; ``'table'`` by default)
            dtype: :class:`numpy.dtype` describing the data.
            columns: either number if columns, or a list of columns names.
            packing (str): The way the 2D array is packed. Can be either
                ``'flatten'`` (data is stored row-wise) or
                ``'transposed'`` (data is stored column-wise).
            preamble (dict): If not ``None``, defines binary file parameters that supersede the parameteres supplied to the function.
                The defined parameters are ``'dtype'``, ``'packing'``, ``'ncols'`` (number of columns) and ``'nrows'`` (number of rows).
            skip_bytes (int): Number of bytes to skip from the beginning of the file.
        """
        if out_type=="default":
            out_type=_module_parameters["fileio/loadfile/csv/out_type"]
        preamble=preamble or {}
        dtype=preamble.get("dtype",dtype)
        packing=preamble.get("packing",packing)
        preamble_columns_num=preamble.get("ncols",None)
        preamble_rows_num=preamble.get("nrows",None)
        with location_file.opening(mode="read",data_type="binary"):
            if skip_bytes:
                location_file.stream.seek(skip_bytes,1)
            data=np.fromfile(location_file.stream,dtype=dtype)
        try:
            columns_num=len(columns)
        except TypeError:
            columns_num=columns
            columns=None
        if columns_num is None:
            columns_num=preamble_columns_num
        elif preamble_columns_num is not None and preamble_columns_num!=columns_num:
            raise ValueError("supplied columns number {0} disagrees with extracted form preamble {1}".format(columns_num,preamble_columns_num))
        if columns_num is not None:
            if packing=="flatten":
                data=data.reshape((-1,columns_num))
            elif packing=="transposed":
                data=data.reshape((columns_num,-1)).transposed()
            else:
                raise ValueError("unrecognized packing method: {0}".format(packing))
        else:
            data=np.column_stack([data])
        if preamble_rows_num is not None and len(data)!=preamble_rows_num:
            raise ValueError("supplied rows number {0} disagrees with extracted form preamble {1}".format(len(data),preamble_rows_num))
        data=parse_csv.columns_to_table([data[:,i] for i in range(data.shape[1])],columns=columns,out_type=out_type)
        return datafile.DataFile(data=data,filetype="bin")
        
        


def load(path=None, input_format=None, loc="file", return_file=False, **kwargs):
    """
    Load data from the file.
    
    Args:
        path (str): Path to the file.
        input_format (str): Input file format. If ``None``, attempt to auto-detect file format (same as ``'generic'``).
        loc (str): Location type.
        return_file (bool): If ``True``, return :class:`.DataFile` object (contains some metainfo);
            otherwise, return just the file data.
    
    `**kwargs` are passed to the file formatter used to read the data
    (see :meth:`CSVTableInputFileFormat.read_file`, :meth:`DictionaryInputFileFormat.read_file` and :meth:`BinaryTableInputFileFormatter.read_file` for the possible arguments).
    The default format names are:
    
        - ``'generic'``: Generic file format. Attempt to autodetect, raise :exc:`IOError` if unsuccessful;
        - ``'txt'``: Generic text file. Attempt to autodetect, raise :exc:`IOError` if unsuccessful
        - ``'csv'``: CSV file, corresponds to :class:`CSVTableInputFileFormat`;
        - ``'dict'``: Dictionary file, corresponds to :class:`DictionaryInputFileFormat`;
        - ``'bin'``: Binary  file, corresponds to :class:`BinaryTableInputFileFormatter`
    """
    loc=location.get_location(loc,path)
    location_file=location.LocationFile(loc)
    data_file=IInputFileFormat.read_file(location_file,file_format=input_format,**kwargs)
    if return_file:
        return data_file
    else:
        return data_file.data