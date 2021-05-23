"""
Classes for describing a generic file location.
"""

# from io import open

from ..utils import files as file_utils
from ..utils import dictionary

import os.path
import contextlib

class LocationName(object):
    """
    File name inside a location.
    
    Args:
        path: Path inside the location. Gets normalized according to the Dictionary rules (not case-sensitive; ``'/'`` and ``'\\'`` are the delimiters).
        ext (str): Name extension (``None`` is default).
    """
    def __init__(self, path=None, ext=None):
        object.__init__(self)
        self.path=self._normalize_path(path)
        self.ext=str(ext).lower() if ext is not None else None
    def _normalize_path(self, path):
        if path is None:
            return None
        return tuple(dictionary.normalize_path(path,omit_empty=True,case_sensitive=False,case_normalization="lower",sep=r"[/\\]"))
    def get_path(self, default_path="", sep="/"):
        """
        Get the string path.
        
        If the object's `path` is ``None``, use `default_path` instead.
        If `sep` is not ``None``, use it to join the path entries; otherwise, return the path in a list form.
        """
        path=self.path or (self._normalize_path(default_path) or [])
        if sep is None:
            return path
        return sep.join(path)
    def get_ext(self, default_ext=""):
        """
        Get the extension.
        
        If the object's `ext` is ``None``, use `default_ext` instead.
        """
        return self.ext if self.ext is not None else (default_ext or "")
    def to_string(self, default_path="", default_ext="", path_sep="/", ext_sep="|", add_empty_ext=True):
        """
        Convert the path to a string representation.
        
        Args:
            default_path (str): Use it as path if the object's `path` is ``None``.
            default_ext (str): Use it as path if the object's `ext` is ``None``.
            path_sep (str): Use it to join the path entries.
            ext_sep (str): Use it to join path and extension.
            add_empty_ext (str): If ``False`` and the extension is empty, don't add `ext_sep` in the end.
        """
        path=self.get_path(default_path,path_sep)
        ext=self.get_ext(default_ext)
        if ext=="" and not add_empty_ext:
            return path
        return ext_sep.join((path,ext))
    def to_path(self, default_path="", default_ext="", ext_sep="|", add_empty_ext=True):
        """
        Convert the path to a list representation.
        
        Extension is added with `ext_sep` to the last entry in the path.
        
        Args:
            default_path (str): Use it as path if the object's `path` is ``None``.
            default_ext (str): Use it as path if the object's `ext` is ``None``.
            ext_sep (str): Use it to join path and extension.
            add_empty_ext (str): If ``False`` and the extension is empty, don't add `ext_sep` in the end.
        """
        path=self.get_path(default_path,sep=None)
        ext=self.get_ext(default_ext)
        if ext=="" and not add_empty_ext:
            return path
        if not path:
            return [ext_sep+ext]
        return tuple(list(path[:-1])+[ext_sep.join((path[-1],ext))])
    def __str__(self):
        return self.to_string()
    def __repr__(self):
        return "{0}('{1}')".format(type(self).__name__,str(self))
    @staticmethod
    def from_string(expr, ext_sep="|"):
        """
        Create a :class:`LocationName` object from a string representation.
        
        `ext_sep` defines extension separator; the path separators are ``'/'`` and ``'\\'``.
        Empty path or extension translate into ``None``.
        """
        expr=expr.split(ext_sep)
        if len(expr)==0:
            expr=(None,None)
        elif len(expr)==1:
            expr=(expr[0],None)
        elif len(expr)>2:
            raise ValueError("can't parse path {0}".format(expr))
        expr=[None if s=="" else s for s in expr]
        return LocationName(*expr)
    @staticmethod
    def from_object(obj):
        """
        Create a :class:`LocationName` object from an object.
        
        `obj` can be a :class:`LocationName` (return unchanged), tuple or list (use as construct arguments),
        string (treat as a string representation) or ``None`` (return empty name).
        """
        if isinstance(obj,LocationName):
            return obj
        elif isinstance(obj,tuple) or isinstance(obj,list):
            return LocationName(*obj)
        elif obj is None:
            return LocationName()
        else:
            return LocationName.from_string(obj)
    def copy(self):
        return LocationName(self.path,self.ext)
    
    
class LocationFile(object):
    """
    A file at a location.
    
    Can be opened for reading or writing.
    
    Args:
        loc: File location.
        name: File's name inside the location.
    """
    def __init__(self, loc, name=None):
        object.__init__(self)
        self.loc=loc
        self.name=LocationName.from_object(name)
        self.opened=False
        self.stream=None
        self.mode=None
        self.data_type=None
    def get_path(self):
        """
        Get file path in a string representation.
        """
        return self.name.to_string()
    _default_modes={"r":("read","text"),"rb":("read","binary"),"w":("write","text"),"wb":("write","binary"),"a":("append","text"),"ab":("append","binary")}
    def open(self, mode="read", data_type="text"):
        """
        Open the file.
        
        Args:
            mode (str): Opening mode. Can be ``'read'``, ``'write'`` or ``'append'``.
            data_type (str): Either ``'text'`` or ``'binary'``.
        """
        if self.opened:
            raise RuntimeError("opening file {0} twice".format(self.get_path()))
        mode,data_type=self._default_modes.get(mode,(mode,data_type))
        self.stream=self.loc.open_file(mode,self.name,data_type)
        self.mode=mode
        self.data_type=data_type
        self.opened=True
    def close(self):
        """Close the file."""
        if not self.opened:
            raise RuntimeError("closing non-opened file {0}".format(self.get_path()))
        self.loc.close_file(self.name)
        self.stream=None
        self.opened=False
    @contextlib.contextmanager
    def opening(self, mode="read", data_type="text"):
        """
        Context for working with opened file (file is closed automatically on exitting a ``with`` block),
        
        Args:
            mode (str): Opening mode. Can be ``'read'``, ``'write'`` or ``'append'``.
            data_type (str): Either ``'text'`` or ``'binary'``.
        """
        try:
            self.open(mode=mode,data_type=data_type)
            yield self.stream
        finally:
            if self.opened:
                self.close()




class IDataLocation(object):
    """
    Generic location.
    """
    def __init__(self):
        object.__init__(self)
    
    def is_name_free(self, name=None):
        """Check if the name is unoccupied."""
        raise NotImplementedError("IDataLocation.is_name_free")
    def generate_new_name(self, prefix_name, idx=0):
        """
        Generate a new name inside the location using the given prefix and starting index.
        
        If `idx` is ``None``, check just the `prefix_name` first before starting to append indices.
        """
        prefix_name=LocationName.from_object(prefix_name)
        if idx is None:
            if self.is_name_free(prefix_name):
                return prefix_name
            idx=0
        while True:
            path="{0}_{1:03d}".format(prefix_name.get_path(),idx)
            name=LocationName(path,prefix_name.ext)
            if self.is_name_free(name):
                return name
            idx=idx+1
        return 
    
    def open_file(self, mode, name=None, data_type="text"):
        """
        Open a location file.
        
        Args:
            mode (str): Opening mode. Can be ``'read'``, ``'write'`` or ``'append'``.
            name: File name inside the location.
            data_type (str): Either ``'text'`` or ``'binary'``.
        """
        raise NotImplementedError("IDataLocation.open_write")
    def close_file(self, name):
        """Close a location file. """
        raise NotImplementedError("IDataLocation.close")
    def get_opened_files(self):
        """Get a list for files opened in that location."""
        raise NotImplementedError("IDataLocation.get_open_files")
    


class IFileSystemDataLocation(IDataLocation):
    """
    A generic filesystem data location.
    
    A single file name describes a single file in the filesystem.
    """
    def __init__(self):
        IDataLocation.__init__(self)
        self.opened_files={}
    def get_filesystem_path(self, name=None, path_type="absolute"):
        """
        Get the filesystem path corresponding to a given name.
        
        `path_type` can be ``'absolute'`` (return absolute path),
        ``'relative'`` (return relative path; level depends on the location) or
        ``'name'`` (only return path inside the location).
        """
        raise NotImplementedError("IFileSystemDataLocation.get_filesystem_path")
    @staticmethod
    def _name_to_filesystem_path(name, default_path=None, default_ext=None):
        split_name=name.to_path(default_path=default_path,default_ext=default_ext,ext_sep=".",add_empty_ext=False)
        return os.path.join(*split_name) if split_name else ""
    def __call__(self, name=None, path_type="absolute"):
        return self.get_filesystem_path(name,path_type)
    def is_name_free(self, name=None):
        """Check if the name is unoccupied."""
        path=self.get_filesystem_path(name,path_type="absolute")
        return not os.path.exists(path)
    def _open_file_stream(self, mode, name, data_type):
        name=LocationName.from_object(name)
        name_str=name.to_string()
        if name_str in self.opened_files:
            raise ValueError("file {0} is already opened".format(name_str))
        file_path=self.get_filesystem_path(name,path_type="absolute")
        if data_type=="binary":
            mode=mode+"b"
        elif data_type!="text":
            raise ValueError("unrecognized data type: {0}".format(data_type))
        f=open(file_path,mode)
        self.opened_files[name_str]=f
        return f
    def open_file(self, mode, name=None, data_type="text"):
        """
        Open a location file.
        
        See :meth:`IDataLocation.open_file` for arguments.
        """
        if mode=="read":
            s=self._open_file_stream("r",name,data_type)
        elif mode=="write":
            s=self._open_file_stream("w",name,data_type)
        elif mode=="append":
            s=self._open_file_stream("a",name,data_type)
            s.seek(0,2)
        else:
            raise ValueError("unrecognized open mode: {0}".format(mode))
        return s
    def close_file(self, name):
        """Close a location file."""
        name_str=LocationName.from_object(name).to_string()
        if not name_str in self.opened_files:
            raise ValueError("name {0} is not opened".format(self.get_filesystem_path(name,"relative")))
        self.opened_files.pop(name_str).close()
    def get_opened_files(self):
        """Get a list for files opened in that location."""
        return self.opened_files

class SingleFileSystemDataLocation(IFileSystemDataLocation):
    """
    A location describing a single file.
    
    Any use of a non-default name raises :exc:`ValueError`.
    
    Args:
        file_path (str): The path to the file.
    """
    def __init__(self, file_path):
        IFileSystemDataLocation.__init__(self)
        self.rel_path=file_path
        self.abs_path=os.path.abspath(file_path)
        file_utils.retry_ensure_dir(os.path.split(file_path)[0])
    def get_filesystem_path(self, name=None, path_type="absolute"):
        name=LocationName.from_object(name)
        if name.path is None and name.ext is None:
            if path_type=="absolute":
                return self.abs_path
            elif path_type=="relative":
                return self.rel_path
            elif path_type=="name":
                return os.path.split(self.rel_path)[1]
            else:
                raise ValueError("unrecognized path type: {0}".format(path_type))
        else:
            raise ValueError("SingleFileSystemDataLocation can only generate default path")
class PrefixedFileSystemDataLocation(IFileSystemDataLocation):
    """
    A location describing a set of prefixed files.
    
    Args:
        file_path (str): A master path. Its name is used as a prefix, and its extension is used as a default.
        prefix_template (str): A :meth:`str.format` string for generating prefixed files. Has two arguments:
            the first is the master name, the second is the sub_location.
    
    Multi-level paths translate into nested folders (the top level folder is combined from the `file_path` prefix and the first path entry).
    """
    def __init__(self, file_path, prefix_template="{0}_{1}"):
        IFileSystemDataLocation.__init__(self)
        self.rel_path,self.master_name=os.path.split(file_path)
        self.abs_path=os.path.abspath(self.rel_path)
        self.master_prefix, self.master_ext=os.path.splitext(self.master_name)
        if self.master_ext[1:]=="": # remove leading .
            self.master_ext=None
        else:
            self.master_ext=self.master_ext[1:]
        self.prefix_template=prefix_template
        file_utils.retry_ensure_dir(os.path.split(file_path)[0])
    def get_filesystem_path(self, name=None, path_type="absolute"):
        name=LocationName.from_object(name)
        if not path_type in {"absolute", "relative","name"}:
            raise ValueError("unrecognized path type: {0}".format(path_type))
        if name.path is None:
            fsname=self.master_prefix
        else:
            fsname=self.prefix_template.format(self.master_prefix,os.path.join(*name.get_path(sep=None)))
        if name.get_ext(self.master_ext):
            fsname="{0}.{1}".format(fsname,name.get_ext(self.master_ext))
        if path_type=="absolute":
            return os.path.join(self.abs_path,fsname)
        elif path_type=="relative":
            return os.path.join(self.rel_path,fsname)
        else:
            return fsname
class FolderFileSystemDataLocation(IFileSystemDataLocation):
    """
    A location describing a single folder.
    
    Args:
        folder_path (str): A path to the folder.
        default_name (str): The default file name.
        default_ext (str): The default file extension.
    
    Multi-level paths translate into nested subfolders.
    """
    def __init__(self, folder_path, default_name="", default_ext=""):
        IFileSystemDataLocation.__init__(self)
        self.rel_path=folder_path
        self.abs_path=os.path.abspath(folder_path)
        self.default_name=default_name
        self.default_ext=default_ext
        file_utils.retry_ensure_dir(self.abs_path)
    def get_filesystem_path(self, name=None, path_type="absolute"):
        name=LocationName.from_object(name)
        if not path_type in {"absolute", "relative", "name"}:
            raise ValueError("unrecognized path type: {0}".format(path_type))
        fsname=self._name_to_filesystem_path(name,self.default_name,self.default_ext)
        if path_type=="absolute":
            return os.path.join(self.abs_path,fsname)
        elif path_type=="relative":
            return os.path.join(self.rel_path,fsname)
        else:
            return fsname
        
    

def get_location(loc, path, *args, **kwargs):
    """
    Build a location.
    
    If `loc` or `path` are instances of :class:`IDataLocation`, return them unchanged.
    If `loc` is a string, it describes location kind:
    
        - ``'single_file'``: :class:`SingleFileSystemDataLocation` with the given `path`.
        - ``'file'`` or ``'prefixed_file'``: :class:`PrefixedFileSystemDataLocation` with the given `path` as a master path.
        - ``'folder'``: :class:`FolderFileSystemDataLocation` with the given folder `path`.
    
    Any additional arguments are relayed to the constructors.
    """
    if isinstance(loc,IDataLocation):
        return loc
    elif isinstance(path,IDataLocation):
        return path
    elif loc=="single_file":
        return SingleFileSystemDataLocation(path,*args,**kwargs)
    elif loc=="file" or loc=="prefixed_file":
        return PrefixedFileSystemDataLocation(path,*args,**kwargs)
    elif loc=="folder":
        return FolderFileSystemDataLocation(path,*args,**kwargs)
    else:
        raise ValueError("unrecognized location: {}".format(loc))