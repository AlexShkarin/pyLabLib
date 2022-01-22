"""
Utilities for reading data files.
"""

from . import datafile, location, dict_entry, parse_csv, loadfile_utils
from ..utils import funcargparse, library_parameters

import numpy as np

library_parameters.library_parameters.update({"fileio/loadfile/csv/out_type":"pandas"},overwrite=False)
library_parameters.library_parameters.update({"fileio/loadfile/dict/inline_out_type":"pandas"},overwrite=False)


##### File formats #####


class IInputFileFormat:
    """
    Generic class for an input file format.
    
    Based on `file_format` or autodetection, calls one of its subclasses to read the file.

    Defines a single static method
    """
    @staticmethod
    def detect_file_format(location_file):
        with location_file.open("rb") as stream:
            is_binary=loadfile_utils.detect_binary_file(stream)
        if is_binary:
            return BinaryTableInputFileFormatter
        else:
            return ITextInputFileFormat.detect_file_format(location_file)
    def read(self, location_file):
        """Read a file at a given location"""
        raise NotImplementedError("{}.{}".format(self.__class__.__name__,"read"))
    
    
class ITextInputFileFormat(IInputFileFormat):  # pylint: disable=abstract-method
    """
    Generic class for a text input file format.
    
    Based on `file_format` or autodetection, calls one of its subclasses to read the file.
    """
    @staticmethod
    def detect_file_format(location_file):
        with location_file.open("r") as stream:
            txt_type=loadfile_utils.detect_textfile_type(stream)
        if txt_type=="table":
            return CSVTableInputFileFormat
        elif txt_type=="dict":
            return DictionaryInputFileFormat
        else:
            raise IOError("can't detect file type")
            
            
class CSVTableInputFileFormat(ITextInputFileFormat):
    """
    Class for CSV input file format.

    Args:
        out_type (str): type of the result: ``'array'`` for numpy array, ``'pandas'`` for pandas DataFrame,
            or ``'default'`` (determined by the library default; ``'pandas'`` by default)
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
    def __init__(self, out_type="default", dtype="numeric", columns=None, delimiters=None, empty_entry_substitute=None, ignore_corrupted_lines=True, skip_lines=0):
        ITextInputFileFormat.__init__(self)
        self.out_type=library_parameters.library_parameters["fileio/loadfile/csv/out_type"] if out_type=="default" else out_type
        self.dtype=dtype
        self.columns=columns
        self.delimiters=delimiters or parse_csv._table_delimiters
        self.empty_entry_substitute=empty_entry_substitute
        self.ignore_corrupted_lines=ignore_corrupted_lines
        self.skip_lines=skip_lines
    def read(self, location_file):
        with location_file.open("r") as stream:
            for _ in range(self.skip_lines):
                stream.readline()
            data,comments,corrupted=parse_csv.read_table(stream,dtype=self.dtype,columns=self.columns,out_type=self.out_type,
                            delimiters=self.delimiters,empty_entry_substitute=self.empty_entry_substitute,ignore_corrupted_lines=self.ignore_corrupted_lines)
        if self.out_type in {"pandas"} and not funcargparse.is_sequence(self.columns,"builtin;nostring") and len(data)>0:
            columns,comment_idx=loadfile_utils.find_columns_lines(corrupted,comments,data.shape[1])
            if comment_idx is not None:
                del comments[comment_idx]
            if columns is not None:
                data.columns=columns
        creation_time=loadfile_utils.find_savetime_comment(comments)
        return datafile.DataFile(data=data,comments=comments,creation_time=creation_time,filetype="csv")
    

class DictionaryInputFileFormat(ITextInputFileFormat):
    """
    Class for Dictionary input file format.
        
    Args:
        location_file: Location of the data.
        case_normalization (str): If ``None``, the dictionary paths are case-sensitive;
            otherwise, defines the way the entries are normalized (``'lower'`` or ``'upper'``).
        inline_dtype (str): dtype for inlined tables.
        inline_out_type (str): type of the result of the inline table:
            ``'array'`` for numpy array, ``'pandas'`` for pandas DataFrame,
            ``'raw'`` for raw :class:`.InlineTable` data containing tuple ``(column_data, column_names)``,
            or ``'default'`` (determined by the library default; ``'pandas'`` by default).
        entry_format (str): Determines the way for dealing with :class:`.dict_entry.IDictionaryEntry` objects
            (objects transformed into dictionary branches with special recognition rules). Can be
            ``'branch'`` (don't attempt to recognize those object, leave dictionary as in the file),
            ``'dict_entry'`` (recognize and leave as :class:`.dict_entry.IDictionaryEntry` objects) or
            ``'value'`` (recognize and keep the value).
        allow_duplicate_keys (bool): if ``False`` and the same key is mentioned twice in the file, raise and error
        skip_lines (int): Number of lines to skip from the beginning of the file.
    """
    def __init__(self, case_normalization=None, inline_dtype="generic", inline_out_type="default", entry_format="value", allow_duplicate_keys=False, skip_lines=0):
        ITextInputFileFormat.__init__(self)
        self.case_normalization=case_normalization
        self.inline_dtype=inline_dtype
        self.inline_out_type=library_parameters.library_parameters["fileio/loadfile/dict/inline_out_type"] if inline_out_type=="default" else inline_out_type
        if not entry_format in {"branch","dict_entry","value"}:
            raise ValueError("unrecognized entry format: {0}".format(entry_format))
        self.entry_format=entry_format
        self.allow_duplicate_keys=allow_duplicate_keys
        self.skip_lines=skip_lines
    def read(self, location_file):
        with location_file.open("r") as stream:
            for _ in range(self.skip_lines):
                stream.readline()
            data,comments=loadfile_utils.read_dict_and_comments(stream,inline_dtype=self.inline_dtype,
                case_normalization=self.case_normalization,allow_duplicate_keys=self.allow_duplicate_keys)
        creation_time=loadfile_utils.find_savetime_comment(comments)
        def map_entries(ptr):
            if dict_entry.is_dict_entry_branch(ptr):
                entry=dict_entry.from_dict(ptr,location_file.loc)
                if self.entry_format=="value":
                    entry=entry.data
                return entry
            else:
                return ptr
        if self.entry_format!="branch":
            data.map_self(map_entries,to_visit="branches",topdown=False)
        def map_inline_tables(ptr):
            if not dict_entry.is_dict_entry_branch(ptr):  # check if there is an inline table not in the entry
                for k,v in ptr.items():
                    if isinstance(v,loadfile_utils.InlineTable):
                        ptr[k],_=dict_entry.parse_stored_table_data(data=v,out_type=self.inline_out_type)
            return ptr
        if self.inline_out_type!="raw":
            data.map_self(map_inline_tables,to_visit="branches",topdown=False)
        if len(data)==1 and list(data.keys())==["__data__"]: # special case of files with preamble
            data=data["__data__"]
        return datafile.DataFile(data=data,comments=comments,creation_time=creation_time,filetype="dict")
    
    
class BinaryTableInputFileFormatter(IInputFileFormat):
    """
    Class for binary input file format.

    Args:
        location_file: Location of the data.
        out_type (str): type of the result: ``'array'`` for numpy array, ``'pandas'`` for pandas DataFrame,
            or ``'default'`` (determined by the library default; ``'pandas'`` by default)
        dtype: :class:`numpy.dtype` describing the data.
        columns: either number if columns, or a list of columns names.
        packing (str): The way the 2D array is packed. Can be either
            ``'flatten'`` (data is stored row-wise) or
            ``'transposed'`` (data is stored column-wise).
        preamble (dict): If not ``None``, defines binary file parameters that supersede the parameters supplied to the function.
            The defined parameters are ``'dtype'``, ``'packing'``, ``'ncols'`` (number of columns) and ``'nrows'`` (number of rows).
        skip_bytes (int): Number of bytes to skip from the beginning of the file.
    """
    def __init__(self, out_type="default", dtype="<f8", columns=None, packing="flatten", preamble=None, skip_bytes=0):
        IInputFileFormat.__init__(self)
        self.out_type=library_parameters.library_parameters["fileio/loadfile/csv/out_type"] if out_type=="default" else out_type
        self.preamble=preamble or {}
        self.dtype=self.preamble.get("dtype",dtype)
        try:
            self.columns_num=len(columns)
            self.columns=columns
        except TypeError:
            self.columns_num=columns
            self.columns=None
        self.packing=self.preamble.get("packing",packing)
        self.skip_bytes=skip_bytes
        self.preamble_columns_num=self.preamble.get("ncols",None)
        if self.columns_num is None:
            self.columns_num=self.preamble_columns_num
        elif self.preamble_columns_num is not None and self.preamble_columns_num!=self.columns_num:
            raise ValueError("supplied columns number {0} disagrees with extracted form preamble {1}".format(self.columns_num,self.preamble_columns_num))
        self.preamble_rows_num=self.preamble.get("nrows",None)
    def read(self, location_file):
        with location_file.open("rb") as stream:
            if self.skip_bytes:
                stream.seek(self.skip_bytes,1)
            data=np.fromfile(stream,dtype=self.dtype)
        if self.columns_num is not None:
            if self.packing=="flatten":
                data=data.reshape((-1,self.columns_num))
            elif self.packing=="transposed":
                data=data.reshape((self.columns_num,-1)).transposed()
            else:
                raise ValueError("unrecognized packing method: {0}".format(self.packing))
        else:
            data=data[None,:]
        if self.preamble_rows_num is not None and len(data)!=self.preamble_rows_num:
            raise ValueError("supplied rows number {0} disagrees with extracted form preamble {1}".format(len(data),self.preamble_rows_num))
        if self.out_type=="pandas":
            data=data.astype(data.dtype.type,copy=False) # convert to native byteorder (required for pandas indexing)
        data=parse_csv.columns_to_table([data[:,i] for i in range(data.shape[1])],columns=self.columns,out_type=self.out_type)
        return datafile.DataFile(data=data,filetype="bin")
        




def build_file_format(location_file, file_format="generic", **kwargs):
    """
    Create file format (:class:`IInputFileFormat` instance) for given parameters and file locations.

    If ``file_format`` is already an instance of :class:`IInputFileFormat`, return unchanged.
    If ``file_format`` is generic (e.g., ``"generic"`` or ``"test"``), attempt to autodetect it from the file.
    ``**kwargs`` are passed to the file format constructor.
    """
    if isinstance(file_format,IInputFileFormat):
        return file_format
    if file_format in {"generic",None}:
        return IInputFileFormat.detect_file_format(location_file)(**kwargs)
    elif file_format=="text":
        return ITextInputFileFormat.detect_file_format(location_file)(**kwargs)
    elif file_format=="csv":
        return CSVTableInputFileFormat(**kwargs)
    elif file_format=="dict":
        return DictionaryInputFileFormat(**kwargs)
    elif file_format=="bin":
        return BinaryTableInputFileFormatter(**kwargs)
    else:
        raise ValueError("unrecognized file format: {}".format(file_format))






def load_csv(path=None, out_type="default", dtype="numeric", columns=None, delimiters=None, empty_entry_substitute=None, ignore_corrupted_lines=True, skip_lines=0, loc="file", return_file=False):
    """
    Load data table from a CSV/table file.

    Args:
        path (str): path to the file of a file-like object
        out_type (str): type of the result: ``'array'`` for numpy array, ``'pandas'`` for pandas DataFrame,
            or ``'default'`` (determined by the library default; ``'pandas'`` by default)
        dtype: dtype of entries; can be either a single type, or a list of types (one per column).
            Possible dtypes are: ``'int'``, ``'float'``, ``'complex'``,
            ``'numeric'`` (tries to coerce to minimal possible numeric type, raises error if data can't be converted to `complex`),
            ``'generic'`` (accept arbitrary types, including lists, dictionaries, escaped strings, etc.),
            ``'raw'`` (keep raw string).
        columns: either a number if columns, or a list of columns names
        delimiters (str): regex string which recognizes entries delimiters (by default ``r"\\s*,\\s*|\\s+"``, i.e., commas and whitespaces)
        empty_entry_substitute: substitute for empty table entries. If ``None``, all empty table entries are skipped
        ignore_corrupted_lines (bool): if ``True``, skip corrupted (e.g., non-numeric for numeric dtype, or with too few entries) lines;
            otherwise, raise :exc:`ValueError`
        skip_lines (int): number of lines to skip from the beginning of the file
        loc (str): location type (``"file"`` means the usual file location; see :func:`.location.get_location` for details)
        return_file (bool): if ``True``, return :class:`.DataFile` object (contains some metainfo); otherwise, return just the file data
    """
    location_file=location.LocationFile(location.get_location(path,loc))
    file_format=CSVTableInputFileFormat(out_type=out_type,dtype=dtype,columns=columns,delimiters=delimiters,
        empty_entry_substitute=empty_entry_substitute,ignore_corrupted_lines=ignore_corrupted_lines,skip_lines=skip_lines)
    data_file=file_format.read(location_file)
    return data_file if return_file else data_file.data

def load_csv_desc(path=None, loc="file", return_file=False):
    """
    Load data from the extended CSV table file.

    Analogous to :func:`load_dict`, but doesn't allow any additional parameters (which don't matter in this case).

    Args:
        path (str): path to the file of a file-like object
        loc (str): location type (``"file"`` means the usual file location; see :func:`.location.get_location` for details)
        return_file (bool): if ``True``, return :class:`.DataFile` object (contains some metainfo); otherwise, return just the file data
    """
    return load_dict(path=path,loc=loc,return_file=return_file)

def load_bin(path=None, out_type="default", dtype="<f8", columns=None, packing="flatten", preamble=None, skip_bytes=0, loc="file", return_file=False):
    """
    Load data from the binary file.

    Args:
        path (str): path to the file of a file-like object
        out_type (str): type of the result: ``'array'`` for numpy array, ``'pandas'`` for pandas DataFrame,
            or ``'default'`` (determined by the library default; ``'pandas'`` by default)
        dtype: :class:`numpy.dtype` describing the data.
        columns: either number if columns, or a list of columns names.
        packing (str): The way the 2D array is packed. Can be either
            ``'flatten'`` (data is stored row-wise) or
            ``'transposed'`` (data is stored column-wise).
        preamble (dict): If not ``None``, defines binary file parameters that supersede the parameters supplied to the function.
            The defined parameters are ``'dtype'``, ``'packing'``, ``'ncols'`` (number of columns) and ``'nrows'`` (number of rows).
        skip_bytes (int): Number of bytes to skip from the beginning of the file.
        loc (str): location type (``"file"`` means the usual file location; see :func:`.location.get_location` for details)
        return_file (bool): if ``True``, return :class:`.DataFile` object (contains some metainfo); otherwise, return just the file data
    """
    location_file=location.LocationFile(location.get_location(path,loc))
    file_format=BinaryTableInputFileFormatter(out_type=out_type,dtype=dtype,columns=columns,packing=packing,
        preamble=preamble,skip_bytes=skip_bytes)
    data_file=file_format.read(location_file)
    return data_file if return_file else data_file.data

def load_bin_desc(path=None, loc="file", return_file=False):
    """
    Load data from the binary file with a description.

    Analogous to :func:`load_dict`, but doesn't allow any additional parameters (which don't matter in this case).

    Args:
        path (str): path to the file of a file-like object
        loc (str): location type (``"file"`` means the usual file location; see :func:`.location.get_location` for details)
        return_file (bool): if ``True``, return :class:`.DataFile` object (contains some metainfo); otherwise, return just the file data
    """
    return load_dict(path=path,loc=loc,return_file=return_file)

def load_dict(path=None, case_normalization=None, inline_dtype="generic", entry_format="value", inline_out_type="default", skip_lines=0, allow_duplicate_keys=False, loc="file", return_file=False):
    """
    Load data from the dictionary file.

    Args:
        path (str): path to the file of a file-like object
        case_normalization (str): If ``None``, the dictionary paths are case-sensitive;
            otherwise, defines the way the entries are normalized (``'lower'`` or ``'upper'``).
        inline_dtype (str): dtype for inlined tables.
        inline_out_type (str): type of the result of the inline table:
            ``'array'`` for numpy array, ``'pandas'`` for pandas DataFrame,
            ``'raw'`` for raw :class:`.InlineTable` data containing tuple ``(column_data, column_names)``,
            or ``'default'`` (determined by the library default; ``'pandas'`` by default).
        entry_format (str): Determines the way for dealing with :class:`.dict_entry.IDictionaryEntry` objects
            (objects transformed into dictionary branches with special recognition rules). Can be
            ``'branch'`` (don't attempt to recognize those object, leave dictionary as in the file),
            ``'dict_entry'`` (recognize and leave as :class:`.dict_entry.IDictionaryEntry` objects) or
            ``'value'`` (recognize and keep the value).
        allow_duplicate_keys (bool): if ``False`` and the same key is mentioned twice in the file, raise and error
        skip_lines (int): Number of lines to skip from the beginning of the file.
        loc (str): location type (``"file"`` means the usual file location; see :func:`.location.get_location` for details)
        return_file (bool): if ``True``, return :class:`.DataFile` object (contains some metainfo); otherwise, return just the file data
    """
    location_file=location.LocationFile(location.get_location(path,loc))
    file_format=DictionaryInputFileFormat(case_normalization=case_normalization,
        inline_dtype=inline_dtype,inline_out_type=inline_out_type,
        entry_format=entry_format,skip_lines=skip_lines,allow_duplicate_keys=allow_duplicate_keys)
    data_file=file_format.read(location_file)
    return data_file if return_file else data_file.data




def load_generic(path=None, file_format=None, loc="file", return_file=False, **kwargs):
    """
    Load data from the file.
    
    Args:
        path (str): path to the file of a file-like object
        file_format (str): input file format; if ``None``, attempt to auto-detect file format (same as ``'generic'``);
            can also be an :class:`IInputFileFormat` instance for specific reading method
        loc (str): location type (``"file"`` means the usual file location; see :func:`.location.get_location` for details)
        return_file (bool): if ``True``, return :class:`.DataFile` object (contains some metainfo); otherwise, return just the file data
    
    `**kwargs` are passed to the file formatter used to read the data
    (see :class:`CSVTableInputFileFormat`, :class:`DictionaryInputFileFormat` and :class:`BinaryTableInputFileFormatter` for the possible arguments).
    The default format names are:
    
        - ``'generic'``: Generic file format. Attempt to autodetect, raise :exc:`IOError` if unsuccessful;
        - ``'txt'``: Generic text file. Attempt to autodetect, raise :exc:`IOError` if unsuccessful
        - ``'csv'``: CSV file, corresponds to :class:`CSVTableInputFileFormat`;
        - ``'dict'``: Dictionary file, corresponds to :class:`DictionaryInputFileFormat`;
        - ``'bin'``: Binary  file, corresponds to :class:`BinaryTableInputFileFormatter`
    """
    location_file=location.LocationFile(location.get_location(path,loc))
    file_format=build_file_format(location_file,file_format=file_format,**kwargs)
    data_file=file_format.read(location_file)
    return data_file if return_file else data_file.data