"""
Utilities for working with the file system: creating/removing/listing folders, comparing folders and files, working with zip archives.
"""

# from io import open
from builtins import range

from . import general, string, funcargparse

try:
    from Tkinter import Tk
    from tkFileDialog import askopenfilename, asksaveasfilename, askdirectory
except ImportError:
    try:
        from tkinter import Tk
        from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
    except ImportError:
        pass

import os
import os.path
import errno
import stat
import filecmp
import shutil
import datetime
import time
import zipfile
import collections




### General routines ###
def eof(f, strict=False):
    """
    Standard EOF function.
    
    Return ``True`` if the the marker is at the end of the file.
    If ``strict==True``, only return ``True`` if the marker is exactly at the end of file; otherwise, return ``True`` if it's at the end of further.
    """
    p=f.tell()
    f.seek(0,2)
    ep=f.tell()
    f.seek(p)
    return (ep==p) or (ep<=p and not strict)
    
def get_file_creation_time(path, timestamp=True):
    """
    Try to find a file creation time. Return current time if an error occurs.
    
    If ``timestamp==True``, return UNIX timestamp; otherwise, return :class:`datetime.datetime`.
    """
    if not timestamp:
        return datetime.datetime.fromtimestamp(get_file_creation_time(path,timestamp=True))
    try:
        return os.path.getctime(path)
    except:
        return time.time()
def get_file_modification_time(path, timestamp=True):
    """
    Try to find a file modification time. Return current time if an error occurs.
    
    If ``timestamp==True``, return UNIX timestamp; otherwise, return :class:`datetime.datetime`
    """
    if not timestamp:
        return datetime.datetime.fromtimestamp(get_file_modification_time(path,timestamp=True))
    try:
        return os.path.getmtime(path)
    except:
        return time.time()

def touch(fname, times=None):
    """
    Update file access and modification times.
    
    Args:
        times(tuple): Access and modification times; if `times` is ``None``, use current time. 
    """
    with open(fname,'ab'):
        os.utime(fname,times)

### Working with paths ###
def generate_indexed_filename(name_format, idx_start=0, folder=""):
    """
    Generate an unused indexed filename in `folder`.
    
    The name has `name_format` (using standard Python :func:`format()` rules), with index starting with `idx_start`.
    """
    while True:
        name=name_format.format(idx_start)
        if not os.path.exists(os.path.join(folder,name)):
            return name
        idx_start=idx_start+1
def generate_prefix_filename(prefix="", suffix="", idx_start=None, folder=""):
    """
    Generate an unused filename in `folder` with the given prefix and suffix.
    
    The format is ``prefix_{:d}_suffix``, where the parameter is the index starting with `idx_start`.
    If `idx_start` is ``None`` first check ``prefix+suffix`` name before using numbered indices. 
    """
    if idx_start is None:
        name=prefix+suffix
        if not os.path.exists(os.path.join(folder,name)):
            return name
        idx_start=0
    return generate_indexed_filename(prefix+"_{:d}"+suffix,idx_start=idx_start,folder=folder)
def generate_temp_filename(prefix="__tmp__", idx_start=0, idx_template="d", folder=""):
    """
    Generate a temporary filename with a given prefix. 
    
    `idx_template` is the number index format (only the parameter itself, not the whole string).
    """
    name_format=prefix+"{:"+idx_template+"}"
    return generate_indexed_filename(name_format=name_format,idx_start=idx_start,folder=folder)
        
def fullsplit(path, ignore_empty=True):
    """
    Split path into list.
    
    If ``ignore_empty==True``, omit empty folder names.
    """
    names=[]
    while True:
        path,name=os.path.split(path)
        if name!="" or not ignore_empty:
            names.append(name)
        if path=="" or path[-1] in "\\/":
            if not all([e in "\\/" for e in path]):
                names.append(path)
            break
    return names[::-1]

def normalize_path(p):
    """Normalize filesystem path (case and origin). If two paths are identical, they should be equal when normalized."""
    return os.path.normcase(os.path.abspath(p))
def case_sensitive_path():
    """Check if OS path names are case-sensitive (e.g., Linux)"""
    return os.path.normcase("TEMP")!="temp"
def paths_equal(a, b):
    """
    Determine if the two paths are equal (can be local or have different case).
    """
    a_norm=normalize_path(a)
    b_norm=normalize_path(b)
    return a_norm==b_norm
def relative_path(a, b, check_paths=True):
    """
    Determine return path `a` as seen from `b`.
    
    If ``check_paths==True``, check if `a` is contained in `b` and raise the :exc:OSError if it isn't.
    """
    a_split=fullsplit(os.path.abspath(a))
    b_split=fullsplit(os.path.abspath(b))
    blen=len(b_split)
    if check_paths and not ( paths_equal(os.path.join(*a_split[:blen]),os.path.join(*b_split)) and len(a_split)>=blen ):
        raise OSError("path {0} is not contained in a path {1}".format(a,b))
    if len(a_split)==blen:
        return ""
    return os.path.join(*a_split[blen:])
    


### Temp file ###
class TempFile(object):
    """
    Temporary file context manager.
    
    Upon creation, generate an unused temporary filename.
    Upon entry, create the file using supplied mode and return self.
    Upon exit, close and remove the file.
    
    Args:
        folder (str): Containing folder.
        name (str): File name. If ``None``, generate new temporary name.
        mode (str): File opening mode.
        wait_time (float): Waiting time between attempts to create the file if the first try fails.
        rep_time (int): Number of attempts to create the file if the first try fails. 
        
    Attributes:
        f: File object.
        name (str): File name.
        full_name (str): File name including containing folder.
    """
    _default_wait_time=0.3
    _default_rep_time=5
    def __init__(self, folder="", name=None, mode="w", wait_time=None, rep_time=None):
        self.folder=folder
        if name is None:
            name=generate_temp_filename(folder=folder)
        self.name=name
        self.full_name=os.path.join(self.folder,self.name)
        self.wait_time=self._default_wait_time if wait_time is None else wait_time
        self.rep_time=self._default_rep_time if rep_time is None else rep_time
        self.mode=mode
        self.f=None
    def __enter__(self):
        self.f=general.retry_wait(lambda: open(self.full_name,mode=self.mode),self.rep_time,self.wait_time)
        self.f=self.f.__enter__()
        if self.wait_time!=0:
            time.sleep(self.wait_time)
        return self
    def __exit__(self, *args, **vargs):
        res=self.f.__exit__(*args,**vargs)
        retry_remove(self.full_name,self.rep_time,self.wait_time)
        return res


### Moving and copying files ###
def copy_file(source, dest, overwrite=True, cmp_on_overwrite=True):
    """
    Copy file, creating a containing folder if necessary. Return ``True`` if the operation was performed.
    
    Args:
        overwrite (bool): If ``True``, overwrite existing file.
        cmp_on_overwrite (bool): If ``True`` and the two files are compared to be the same, don't perform overwrite.
    """
    if paths_equal(source,dest):
        return False
    if os.path.exists(dest):
        if not overwrite or (cmp_on_overwrite and filecmp.cmp(source,dest,shallow=False)):
            return False
    else:
        ensure_dir(os.path.split(dest)[0])
    shutil.copy(source,dest)
    return True
def move_file(source, dest, overwrite=True, cmp_on_overwrite=True, preserve_if_not_move=False):
    """
    Move file, creating a containing folder if necessary. Returns ``True`` if the operation was performed.
    
    Args:
        overwrite (bool): If ``True``, overwrite existing file (if the existing file isn't overwritten, preserve the original).
        cmp_on_overwrite (bool): If ``True`` and the two files are compared to be the same, don't perform overwrite.
        preserve_if_not_move (bool): If ``True`` and the files are identical, preserve the original.
    """
    if paths_equal(source,dest):
        return
    if os.path.exists(dest):
        if not overwrite or (cmp_on_overwrite and filecmp.cmp(source,dest,shallow=False)):
            if not preserve_if_not_move:
                os.remove(source)
            return
    else:
        ensure_dir(os.path.split(dest)[0])
    shutil.move(source,dest)
    
### Creating directories ###
def ensure_dir_singlelevel(path, error_on_file=True):
    if os.path.exists(path):
        if not os.path.isdir(path):
            if error_on_file:
                raise OSError("path {0} is not a directory".format(path))
    else:
        os.mkdir(path)
def ensure_dir(path, error_on_file=True):
    """
    Ensure that the folder exists (create a new one if necessary). 
    
    If ``error_on_file==True``, raise :exc:`OSError` if there's a file with the same name.
    """
    dirs=fullsplit(path)
    for i in range(len(dirs)):
        ensure_dir_singlelevel(os.path.join(*dirs[:i+1]),error_on_file=error_on_file)
        
def _handleRemoveReadonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir,os.remove) and excvalue.errno==errno.EACCES:
        os.chmod(path,stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO) # 0777
        func(path)
    else:
        raise
def remove_dir(path, error_on_file=True):
    """
    Remove the folder recursively if it exists.
    
    If ``error_on_file==True``, raise :exc:`OSError` if there's a file with the same name.
    """
    if os.path.exists(path):
        if not os.path.isdir(path):
            if error_on_file:
                raise IOError("path {0} is not a directory".format(path))
            else:
                for _ in range(10):
                    os.remove(path)
                    if not os.path.exists(path):
                        return True
        for _ in range(10):
            shutil.rmtree(path,ignore_errors=False,onerror=_handleRemoveReadonly)
            if not os.path.exists(path):
                return True
    else:
        return False
def remove_dir_if_empty(path, error_on_file=True):
    """
    Remove the folder only if it's empty.
    
    If ``error_on_file==True``, raise :exc:`OSError` if there's a file with the same name.
    """
    if os.path.exists(path) and dir_empty(path,error_on_file=error_on_file):
        return remove_dir(path)
    else:
        return False
def clean_dir(path, error_on_file=True):
    """
    Remove the folder and then recreate it.
    
    If ``error_on_file==True``, raise :exc:`OSError` if there's a file with the same name.
    """
    remove_dir(path,error_on_file=error_on_file)
    ensure_dir(path,error_on_file=error_on_file)


### Folder walking, extension of os.walk ###
class FolderList(collections.namedtuple("FolderList",["folders","files"])): # making Sphinx autodoc generate correct docstring
    """
    Describes folder content.
    """

def list_dir(folder="", folder_filter=None, file_filter=None, separate_kinds=True, error_on_file=True):
    """
    Return folder content filtered by `folder_filter` and `file_filter`.
    
    Args:
        folder (str): Path to the folder.
        folder_filter: Folder filter function (more description at :func:`.string.get_string_filter`).
        file_filter: File filter function (more description at :func:`.string.get_string_filter`).
        separate_kinds (bool): if ``True``, return :class:`FolderList` with files and folder separate; otherwise, return a single list (works much faster).
        error_on_file (bool): if ``True``, raise :exc:`OSError` if there's a file with the same name as the target folder.
    """
    folder=folder or "."
    if not os.path.exists(folder):
        return FolderList([], [])
    if not os.path.isdir(folder):
        if error_on_file:
            raise IOError("path {0} is not a directory".format(folder))
        else:
            return FolderList([], [])
    elements=os.listdir(folder)
    elements.sort()
    file_filter=string.get_string_filter(file_filter,match_case=case_sensitive_path())
    folder_filter=string.get_string_filter(folder_filter,match_case=case_sensitive_path())
    if separate_kinds:
        folders,files=general.partition_list(lambda p: os.path.isdir(os.path.join(folder,p)), elements)
        files=string.filter_string_list(files,file_filter)
        folders=string.filter_string_list(folders,folder_filter)
        return FolderList(folders, files)
    else:
        elements=string.filter_string_list(elements,folder_filter)
        elements=string.filter_string_list(elements,file_filter)
        return elements
def dir_empty(folder, folder_filter=None, file_filter=None, level="single", error_on_file=True):
    """
    Check if the folder is empty (only checks content filtered by `folder_filter` and `file_filter`).
    
    Args:
        folder (str): Path to the folder.
        folder_filter: Folder filter function (more description at :func:`.string.get_string_filter`).
        file_filter: File filter function (more description at :func:`.string.get_string_filter`).
        level (str): if ``'single'``, check only immediate folder content; if ``'recursive'``, follow recursively in all folders passing `folder_filter`.
        error_on_file (bool): if ``True``, raise :exc:`OSError` if there's a file with the same name as the target folder.
    """
    funcargparse.check_parameter_range(level,"level",{"single","recursive"})
    folders,files=list_dir(folder,folder_filter,file_filter,error_on_file=error_on_file)
    if level=="single":
        return len(folders)==0 and len(files)==0
    else:
        if len(files)!=0:
            return False
        for f in folders:
            if not dir_empty(os.path.join(folder,f),folder_filter=folder_filter,file_filter=file_filter,level="recursive"):
                return False
        return True
def walk_dir(folder, folder_filter=None, file_filter=None, rel_path=True, topdown=True, visit_folder_filter=None, max_depth=None):
    """
    Modification of :func:`os.walk` function.
    
    Acts in a similar way, but `followlinks` is always ``False`` and errors of :func:`os.listdir` are always passed.
    
    Args:
        folder (str): Path to the folder.
        folder_filter: Folder filter function (more description at :func:`.string.get_string_filter`).
        file_filter: File filter function (more description at :func:`.string.get_string_filter`).
        rel_path (bool): If ``True``, the returned folder path is specified relative to the initial path.
        topdown (bool): If ``True``, return folder before its subfolders.
        visit_folder_filter: Filter for visiting folders (more description at :func:`.string.get_string_filter`).
            If not ``None``, specifies filter for visiting folders which is different from  `folder_filter` (filter for returned folders).
        max_depth (int): If not ``None``, limits the recursion depth.
    
    Yields:
        For each folder (including the original) yields a tuple ``(folder_path, folders, files)``,
            where `folder_path` is the containing folder name and `folders` and `files` are its content (similar to :func:`list_dir`). 
    """
    folder=folder or "."
    if max_depth is not None and max_depth<0:
        return
    if not os.path.exists(folder):
        return
    if not os.path.isdir(folder):
        raise OSError("path {0} is not a directory".format(folder))
    if visit_folder_filter is not None:
        all_folders,files=list_dir(folder,file_filter=file_filter)
        file_filter=string.get_string_filter(file_filter,match_case=case_sensitive_path())
        folder_filter=string.get_string_filter(folder_filter,match_case=case_sensitive_path())
        return_folders=string.filter_string_list(all_folders,folder_filter)
        walk_folders=string.filter_string_list(all_folders,visit_folder_filter)
    else:
        walk_folders,files=list_dir(folder,folder_filter=folder_filter,file_filter=file_filter)
        return_folders=walk_folders
    def process_folders():
        for f in walk_folders:
            for path,dirs,files in walk_dir(os.path.join(folder,f),folder_filter,file_filter,rel_path=True,topdown=topdown,
                                            visit_folder_filter=visit_folder_filter,max_depth=None if (max_depth is None) else max_depth-1):
                if path=="":
                    path=f
                else:
                    path=os.path.join(f,path)
                if not rel_path:
                    path=os.path.join(folder,path)
                yield path,dirs,files
    if topdown:
        yield ("" if rel_path else folder), return_folders, files
        for t in process_folders():
            yield t
    else:
        for t in process_folders():
            yield t
        yield ("" if rel_path else folder), return_folders, files
def list_dir_recursive(folder, folder_filter=None, file_filter=None, topdown=True, visit_folder_filter=None, max_depth=None):
    """
    Recursive walk analog of :func:`list_dir`.
    
    Parameters are the same as :func:`walk_dir`.
    
    Returns:
        :class:`FolderList`
    """
    all_folders=[]
    all_files=[]
    for cf, folders, files in walk_dir(folder,folder_filter,file_filter,topdown=topdown,visit_folder_filter=visit_folder_filter,max_depth=max_depth):
        all_folders=all_folders+[os.path.join(cf,f) for f in folders]
        all_files=all_files+[os.path.join(cf,f) for f in files]
    return FolderList(all_folders,all_files)
def copy_dir(source, dest, folder_filter=None, file_filter=None, overwrite=True, cmp_on_overwrite=True):
    """
    Copy files satisfying the filtering conditions.
    
    Args:
        source (str): Source path.
        dest (str): Destination path.
        folder_filter: Folder filter function (more description at :func:`.string.get_string_filter`).
        file_filter: File filter function (more description at :func:`.string.get_string_filter`).
        overwrite (bool): If ``True``, overwrite existing files.
        cmp_on_overwrite (bool): If ``True`` and the two files are compared to be the same, don't perform overwrite.
    """
    if paths_equal(source,dest):
        return
    for path,_,files in walk_dir(source,folder_filter=folder_filter,file_filter=file_filter):
        source_dir=os.path.join(source,path)
        dest_dir=os.path.join(dest,path)
        ensure_dir(dest_dir)
        for f in files:
            source_path=os.path.join(source_dir,f)
            dest_path=os.path.join(dest_dir,f)
            copy_file(source_path,dest_path,overwrite=overwrite,cmp_on_overwrite=cmp_on_overwrite)
def move_dir(source, dest, folder_filter=None, file_filter=None, overwrite=True, cmp_on_overwrite=True, preserve_if_not_move=False):
    """
    Move files satisfying the filtering conditions.
    
    Args:
        source (str): Source path.
        dest (str): Destination path.
        folder_filter: Folder filter function (more description at :func:`.string.get_string_filter`).
        file_filter: File filter function (more description at :func:`.string.get_string_filter`).
        overwrite (bool): If ``True``, overwrite existing files (if the existing file isn't overwritten, preserve the original).
        cmp_on_overwrite (bool): If ``True`` and the two files are compared to be the same, don't perform overwrite.
        preserve_if_not_move (bool): If ``True`` and the files are identical, preserve the original.
    """
    if paths_equal(source,dest):
        return
    for path,folders,files in walk_dir(source,folder_filter=folder_filter,file_filter=file_filter,topdown=False):
        source_dir=os.path.join(source,path)
        dest_dir=os.path.join(dest,path)
        ensure_dir(dest_dir)
        for f in files:
            source_path=os.path.join(source_dir,f)
            dest_path=os.path.join(dest_dir,f)
            move_file(source_path,dest_path,overwrite=overwrite,cmp_on_overwrite=cmp_on_overwrite,preserve_if_not_move=preserve_if_not_move)
        for f in folders:
            if dir_empty(f):
                remove_dir(f)

def _diff_from_cnt(c1, c2):
    if c1 and c2:
        return "*"
    if c1:
        return "+"
    if c2:
        return "-"
    return "="
def combine_diff(d1, d2):
    if d1=="=":
        return d2
    if d2=="=":
        return d1
    return d1 if (d1==d2) else "*"
def _diff_dirs(a, b, folder_filter=None, file_filter=None, shallow=True):
    list_a=list_dir(a,folder_filter=folder_filter,file_filter=file_filter)
    list_b=list_dir(b,folder_filter=folder_filter,file_filter=file_filter)
    files_both,files_a_only,files_b_only=general.compare_lists(list_a.files,list_b.files,sort_lists=True)
    diff=_diff_from_cnt(files_a_only,files_b_only)
    if diff=="*":
        return diff
    for f in files_both:
        if not filecmp.cmp(os.path.join(a,f),os.path.join(b,f),shallow=shallow):
            return "*"
    folders_both,folders_a_only,folders_b_only=general.compare_lists(list_a.folders,list_b.folders,sort_lists=True)
    diff=combine_diff(diff,_diff_from_cnt(folders_a_only,folders_b_only))
    if diff=="*":
        return diff
    for f in folders_both:
        sub_diff=_diff_dirs(os.path.join(a,f),os.path.join(b,f),shallow=shallow,folder_filter=folder_filter,file_filter=file_filter)
        diff=combine_diff(diff,sub_diff)
        if diff=="*":
            return "*"
    return diff
def cmp_dirs(a, b, folder_filter=None, file_filter=None, shallow=True, return_difference=False):
    """
    Compare the folders based on the content filtered by `folder_filter` and `file_filter`.
    
    Args:
        a (str): First folder path
        b (str): Second folder path
        folder_filter: Folder filter function (more description at :func:`.string.get_string_filter`).
        file_filter: File filter function (more description at :func:`.string.get_string_filter`).
        shallow: If ``True``, do shallow comparison of the files (see :func:`filecmp.cmp`).
        return_difference: If ``False``, simply return `bool`; otherwise, return difference type (``'='``, ``'+'``, ``'-'`` or ``'*'``). 
    """
    if return_difference:
        return _diff_dirs(a,b,folder_filter=folder_filter,file_filter=file_filter,shallow=shallow)
    list_a=list_dir(a,folder_filter=folder_filter,file_filter=file_filter)
    list_b=list_dir(b,folder_filter=folder_filter,file_filter=file_filter)
    files_both,files_a_only,files_b_only=general.compare_lists(list_a.files,list_b.files,sort_lists=True)
    if len(files_a_only)!=0 or len(files_b_only)!=0:
        return False
    for f in files_both:
        if not filecmp.cmp(os.path.join(a,f),os.path.join(b,f),shallow=shallow):
            return False
    folders_both,folders_a_only,folders_b_only=general.compare_lists(list_a.folders,list_b.folders,sort_lists=True)
    if len(folders_a_only)!=0 or len(folders_b_only)!=0:
        return False
    for f in folders_both:
        if not cmp_dirs(os.path.join(a,f),os.path.join(b,f),shallow=shallow,return_difference=False,folder_filter=folder_filter,file_filter=file_filter):
            return False
    return True

### Retrying os modifying calls ###
def retry_copy(source, dest, overwrite=True, cmp_on_overwrite=True, try_times=5, delay=0.3):
    """
    Retrying version of :func:`copy_file`.
    
    If the operation raises error, wait for `delay` (in seconds) and call it again.
    Try total of `try_times` times.
    """
    general.retry_wait(lambda: copy_file(source,dest,overwrite,cmp_on_overwrite), try_times, delay)
def retry_move(source, dest, overwrite=True, cmp_on_overwrite=True, preserve_if_not_move=False, try_times=5, delay=0.3):
    """
    Retrying version of :func:`move_file` (see :func:`retry_copy` for details on retrying).
    """
    general.retry_wait(lambda: move_file(source,dest,overwrite,cmp_on_overwrite,preserve_if_not_move), try_times, delay)
def retry_remove(path, try_times=5, delay=0.3):
    """
    Retrying version of :func:`os.remove` (see :func:`retry_copy` for details on retrying).
    """
    general.retry_wait(lambda: os.remove(path), try_times, delay)

def retry_ensure_dir(path, error_on_file=True, try_times=5, delay=0.3):
    """
    Retrying version of :func:`ensure_dir` (see :func:`retry_copy` for details on retrying).
    """
    general.retry_wait(lambda: ensure_dir(path,error_on_file=error_on_file), try_times, delay)
def retry_copy_dir(source, dest, folder_filter=None, file_filter=None, overwrite=True, cmp_on_overwrite=True, try_times=5, delay=0.3):
    """
    Retrying version of :func:`copy_dir` (see :func:`retry_copy` for details on retrying).
    """
    general.retry_wait(lambda: copy_dir(source,dest,folder_filter,file_filter,overwrite,cmp_on_overwrite), try_times, delay)
def retry_move_dir(source, dest, folder_filter=None, file_filter=None, overwrite=True, cmp_on_overwrite=True, preserve_if_not_move=False, try_times=5, delay=0.3):
    """
    Retrying version of :func:`move_dir` (see :func:`retry_copy` for details on retrying).
    """
    general.retry_wait(lambda: move_dir(source,dest,folder_filter,file_filter,overwrite,cmp_on_overwrite,preserve_if_not_move), try_times, delay)
def retry_remove_dir(path, error_on_file=True, try_times=5, delay=0.3):
    """
    Retrying version of :func:`remove_dir` (see :func:`retry_copy` for details on retrying).
    """
    general.retry_wait(lambda: remove_dir(path,error_on_file=error_on_file), try_times, delay)
def retry_remove_dir_if_empty(path, error_on_file=True, try_times=5, delay=0.3):
    """
    Retrying version of :func:`remove_dir_if_empty` (see :func:`retry_copy` for details on retrying).
    """
    general.retry_wait(lambda: remove_dir_if_empty(path,error_on_file=error_on_file), try_times, delay)
def retry_clean_dir(path, error_on_file=True, try_times=5, delay=0.3):
    """
    Retrying version of :func:`clean_dir` (see :func:`retry_copy` for details on retrying).
    """
    retry_remove_dir(path,error_on_file,try_times,delay)
    retry_ensure_dir(path,error_on_file,try_times,delay)
    
    
    
### Archiving zip files ###
def zip_folder(zip_path, source_path, inside_path="", folder_filter=None, file_filter=None, mode="a", compression=zipfile.ZIP_DEFLATED):
    """
    Add a folder into a zip archive.
    
    Args:
        zip_path (str): Path to the .zip file.
        source_path (str): Path to the source folder.
        inside_path (str): Destination path inside the zip archive.
        folder_filter: Folder filter function (more description at :func:`.string.get_string_filter`).
        file_filter: File filter function (more description at :func:`.string.get_string_filter`).
        mode (str): Zip archive adding mode (see :class:`zipfile.ZipFile`).
        compression: Zip archive compression (see :class:`zipfile.ZipFile`).
    """
    with zipfile.ZipFile(zip_path, mode=mode, compression=compression) as zf:
        for containing_folder,_,files in walk_dir(source_path,rel_path=True,folder_filter=folder_filter,file_filter=file_filter):
            for f in files:
                zf.write(os.path.join(source_path,containing_folder,f),os.path.join(inside_path,containing_folder,f),compress_type=compression)
def zip_file(zip_path, source_path, inside_name=None, mode="a", compression=zipfile.ZIP_DEFLATED): 
    """
    Add a file into a zip archive.
    
    Args:
        zip_path (str): Path to the .zip file.
        source_path (str): Path to the source file.
        inside_name (str): Destination file name inside the zip archive (source name on the top level by default).
        mode (str): Zip archive adding mode (see :class:`zipfile.ZipFile`).
        compression: Zip archive compression (see :class:`zipfile.ZipFile`). 
    """
    if inside_name is None:
        inside_name=os.path.split(source_path)[1]
    with zipfile.ZipFile(zip_path, mode=mode, compression=compression) as zf:
        zf.write(source_path,inside_name,compress_type=compression)
def zip_multiple_files(zip_path, source_paths, inside_names=None, mode="a", compression=zipfile.ZIP_DEFLATED): 
    """
    Add a multiple files into a zip archive.
    
    Args:
        zip_path (str): Path to the .zip file.
        source_paths ([str]): List of path to the source files.
        inside_names ([str] or None): List of destination file names inside the zip archive (source name on the top level by default).
        mode (str): Zip archive adding mode (see :class:`zipfile.ZipFile`).
        compression: Zip archive compression (see :class:`zipfile.ZipFile`). 
    """
    if inside_names is None:
        inside_names=[None]*len(source_paths)
    for sp,inm in zip(source_paths,inside_names):
        zip_file(zip_path,sp,inside_name=inm,mode=mode,compression=compression)
def unzip_folder(zip_path, dest_path, inside_path="", folder_filter=None, file_filter=None):
    """
    Extract a folder from a zip archive (create containing folder if necessary).
    
    Args:
        zip_path (str): Path to the .zip file.
        dest_path (str): Path to the destination folder.
        inside_path (str): Source path inside the zip archive; extracted data paths are relative (i.e., they don't include `inside_path`).
        folder_filter: Folder filter function (more description at :func:`.string.get_string_filter`).
        file_filter: File filter function (more description at :func:`.string.get_string_filter`).
    """
    with zipfile.ZipFile(zip_path, mode="r") as zf:
        if inside_path=="" and folder_filter is None and file_filter is None:
            zf.extractall(dest_path)
        else:
            folder_filter=string.get_string_filter(folder_filter)
            file_filter=string.get_string_filter(file_filter)
            inside_path=fullsplit(inside_path)
            for f in zf.filelist:
                path=fullsplit(f.filename)
                if path[:len(inside_path)]==inside_path and file_filter(path[-1]) and all([folder_filter(p) for p in path[:-1]]):
                    if len(inside_path)==0:
                        zf.extract(f,dest_path)
                    else:
                        dest_filepath=os.path.join(dest_path,*path[len(inside_path):])
                        with zf.open(f,"r") as source_file:
                            ensure_dir(os.path.split(dest_filepath)[0])
                            with open(dest_filepath,"wb") as dest_file:
                                shutil.copyfileobj(source_file,dest_file)
def unzip_file(zip_path, dest_path, inside_path):
    """
    Extract a file from a zip archive (create containing folder if necessary).
    
    Args:
        zip_path (str): Path to the .zip file.
        dest_path (str): Destination file path.
        inside_path (str): Source path inside the zip archive.
    """
    with zipfile.ZipFile(zip_path, mode="r") as zf:
        with zf.open(inside_path,"r") as source_file:
            ensure_dir(os.path.split(dest_path)[0])
            with open(dest_path,"wb") as dest_file:
                shutil.copyfileobj(source_file,dest_file)



### File-related dialog windows ###
## Use default Tkinter window manager
def openfiledialog(**options):
    """
    Open file dialog, wrapper for tkFileDialog.
    """
    main=Tk()
    main.withdraw()
    path=askopenfilename(**options)
    main.quit()
    return path
def savefiledialog(**options):
    """
    Save file dialog, wrapper for tkFileDialog.
    """
    main=Tk()
    main.withdraw()
    path=asksaveasfilename(**options)
    main.quit()
    return path
def opendirdialog(**options):
    """
    Open directory dialog, wrapper for tkFileDialog.
    """
    main=Tk()
    main.withdraw()
    path=askdirectory(**options)
    main.quit()
    return path