"""
Fetching, storing and recalling different script and library configurations.
"""

# from io import open
from builtins import range

from . import files as file_utils #@UnresolvedImport
from . import string as string_utils #@UnresolvedImport
from . import module as module_utils #@UnresolvedImport
from .. import version #@UnresolvedImport

import os.path
import datetime
import time
import filecmp

_depends_local=[".string"]


_storage_folder=".versions"
def _shelf_folder(shelf, coverage=None):
    """Get the shelf folder for the given coverage."""
    if coverage is None:
        return os.path.join(_storage_folder,shelf)
    else:
        return os.path.join(_storage_folder,shelf,coverage)
def _shelf_content(shelf, coverage=None, full_path=False):
    """Get the content of the shelf folder for the given coverage."""
    shelf_folder=_shelf_folder(shelf,coverage)
    files=file_utils.list_dir(shelf_folder,file_filter=r".*\.zip$").files
    if full_path:
        files=[os.path.join(shelf_folder,f) for f in files]
    return files
def _store_file_path(shelf, label=None, coverage="full"):
    """Store file with the given label in the shelf folder for the given coverage."""
    shelf_folder=_shelf_folder(shelf,coverage)
    file_utils.ensure_dir(shelf_folder)
    prefix=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if label is not None:
        prefix=prefix+"_"+label
    return file_utils.generate_prefix_filename(os.path.join(shelf_folder,prefix),".zip")
def _recall_file_path(shelf, coverage, name):
    shelf_folder=_shelf_folder(shelf,coverage)
    return os.path.join(shelf_folder,name)


def _temp_folder(name):
    """Empty the temporary folder and return its path."""
    temp_dir=os.path.join(_storage_folder,".tmp",name)
    file_utils.retry_remove_dir(temp_dir,error_on_file=False)
    file_utils.retry_ensure_dir(temp_dir)
    return temp_dir
def _unpack_temp(store_path):
    """Unpack a zip archive into the temp folder."""
    temp_dir=_temp_folder("unpacked")
    file_utils.unzip_folder(store_path,temp_dir)
    return temp_dir
def _open_temp_file():
    """Create and open the temp file."""
    temp_dir=os.path.join(_storage_folder,".tmp","files")
    file_utils.retry_ensure_dir(temp_dir)
    return file_utils.TempFile(folder=temp_dir)



def _cleanup_shelf(shelf, coverage, max_items):
    """
    Clean the shelf by removing zip files so that there are at most `max_items` stored (leave the most recent files).
    """
    if max_items<=0:
        return 0
    file_list=_shelf_content(shelf,coverage,full_path=True)
    if len(file_list)<=max_items:
        return 0
    to_remove=len(file_list)-max_items
    file_list.sort(key=file_utils.get_file_creation_time)
    for f in file_list[:to_remove]:
        file_utils.retry_remove(f)
    return to_remove




def generate_version_idx():
    """
    Generate a unique string id based on the current time and a random number.
    """
    t=int(time.time()*1E3)
    r=os.urandom(10)
    r="".join(["{:02x}".format(ord(c)) for c in r])
    return "{:012x}".format(t)+r
_version_config_file="version_config.txt"
_dependencies_file="dependencies.txt"
_store_files_filter=string_utils.get_string_filter(exclude=r"\.|.*\.pyc$|make\.bat$|conf\.py$|Makefile$|.*\.rst$")
_store_folder_filter=string_utils.get_string_filter(exclude=r"\.|__.*__$")
_scripts_template=r".*\.py$"
class VersionConfig(object):
    """
    Current version configuration.

    Combines information about included library packages, additional scripts, package versions, and comments.

    Args:
        store_path(str): root folder of the configuration
        lib_path(str): library path inside the root folder
        libs(list or None): included packages inside the library (any package includes all of its sub-packages);
            by default, includes the ``'core'`` package and all individual ``'aux_libs'`` sub-packages
        additional_scripts(list or None): additional scripts (outside of the included libraries); by default, none are included
        versions(dict): list of versions of versions (e.g., of library packages); by default, none are supplied
        comments(str): config comment.
    """
    def __init__(self, store_path=".", lib_path="lib", libs=None, additional_scripts=None, versions=None, comments=None):
        object.__init__(self)
        self.store_path=store_path
        self.lib_path=lib_path
        if libs is None:
            libs_path=self.get_lib_path("aux_libs")
            libs=["aux_libs."+l for l in file_utils.list_dir(libs_path,folder_filter=_store_folder_filter).folders]
            if os.path.exists(self.get_lib_path("core")):
                libs=["core"]+libs
        self.libs=libs
        self.additional_scripts=additional_scripts or []
        self.versions=versions or {}
        self.comments=comments or ""
    
    @staticmethod
    def _join_list(l):
        return "; ".join(sorted(l))
    @staticmethod
    def _split_list(s):
        return [e.strip() for e in s.split(";")]
    @staticmethod
    def _join_dict(d):
        return "; ".join(["{}:{}".format(k,v) for k,v in sorted(d.items())])
    @staticmethod
    def _split_dict(s):
        pairs=[e.split(":",1) for e in s.split(";")]
        return dict([ (k.strip(),v.strip()) for k,v in pairs ])
    
    def to_file(self, f):
        """
        Save the config data to a file.
        """
        if self.lib_path is not None:
            f.write("lib_path\t{}\n".format(self.lib_path))
        if self.libs:
            f.write("libs\t{}\n".format(self._join_list(self.libs)))
        if self.additional_scripts:
            f.write("additional_scripts\t{}\n".format(self._join_list(self.additional_scripts)))
        if self.versions:
            f.write("versions\t{}\n".format(self._join_dict(self.versions)))
        if self.comments:
            f.write("comments\t{}\n".format(self.comments.replace("\n"," ")))
    @staticmethod
    def from_path(path, **additional_args):
        """
        Build the config data from the folder.

        `additional_args` include arguments supplied to the :class:`VersionConfig` constructor overriding the ones extracted from the config file (if it's present).
        """
        if os.path.isdir(path):
            store_path=path
            config_path=os.path.join(path,_version_config_file)
        else:
            store_path=os.path.split(path)[0]
            config_path=path
        data={}
        if os.path.exists(config_path):
            with open(config_path,"r") as f:
                for line in f:
                    name,value=line.strip().split(None,1)
                    data[name.lower()]=value
        if "libs" in data:
            data["libs"]=VersionConfig._split_list(data["libs"].lower())
        if "additional_scripts" in data:
            data["additional_scripts"]=VersionConfig._split_list(data["additional_scripts"].lower())
        if "versions" in data:
            data["versions"]=VersionConfig._split_dict(data["versions"])
        data["store_path"]=store_path
        data.update(additional_args)
        return VersionConfig(**data)
    
    def update(self, other, override=True):
        """
        Merge this config with the other one.

        Combine information about libraries, comments, and additional scripts.
        If ``override==True``, the priority versions data is taken from the other config; otherwise, it's taken from this config.
        """
        libs=list(set(self.libs+other.libs))
        additional_scripts=list(set(self.additional_scripts+other.additional_scripts))
        if override:
            versions=self.versions.copy()
            versions.update(other.versions)
        else:
            versions=other.versions.copy()
            versions.update(self.versions)
        if self.comments.find(other.comments)==-1:
            comments=self.comments+"  "+other.comments
        else:
            comments=self.comments
        return VersionConfig(self.store_path,self.lib_path,libs,additional_scripts,versions,comments)
    def copy(self):
        return VersionConfig(self.store_path,self.lib_path,list(self.libs),list(self.additional_scripts),self.versions.copy(),self.comments)
    def update_versions(self, parts, force_update=True):
        """
        Update versions to a new unique idx.
        """
        v=generate_version_idx()
        for p in parts:
            if force_update:
                self.versions[p]=v
            else:
                self.versions.setdefault(p,v)
    def includes(self, other):
        """
        Check if this config includes the other one.
        """
        if self.lib_path!=other.lib_path:
            return False
        if not (set(self.libs)>=set(other.libs)):
            return False
        if not (set(self.additional_scripts)>=set(other.additional_scripts)):
            return False
        return True

    def get_lib_path(self, spec_lib="", relative=False):
        """
        Generate a library path in this version config.
        """
        if relative:
            return os.path.join(self.lib_path,*spec_lib.split("."))
        else:
            return os.path.join(self.store_path,self.lib_path,*spec_lib.split("."))
    def common_lib_folders(self):
        """
        Return all of the libs folders, including intermediate containing folders. 
        """
        if len(self.libs)==0:
            return set()
        common_folders={""}
        for l in self.libs:
            l_path=l.split(".")
            for i in range(1,len(l_path)):
                common_folders.add(os.path.join(*l_path[:i]))
        return list(common_folders)
    def common_lib_files(self, path_type="absolute"):
        """
        Return all of the files in lib folders and intermediate containing folders (i.e., all files potentially used by libs). 
        """
        files=[]
        for lf in self.common_lib_folders():
            folder_files=file_utils.list_dir(os.path.join(self.get_lib_path(),lf),file_filter=_store_files_filter).files
            files=files+[os.path.join(lf,ff) for ff in folder_files]
        if path_type=="name":
            return files
        elif path_type=="relative":
            return [os.path.join(self.lib_path,f) for f in files]
        else:
            return [os.path.join(self.store_path,self.lib_path,f) for f in files]
    def template_script_files(self):
        """
        Get all script files in the main folder.
        """
        return file_utils.list_dir(self.store_path,file_filter=_scripts_template)[1]
    def script_files(self):
        """
        Get all included standalone script files (all script files in the main folder and the additional scripts).
        """
        if self.lib_path=="": # library source config; no non-library scripts
            return []
        template_files=self.template_script_files()
        return list(set(template_files+self.additional_scripts))
    def exists(self):
        """
        Check if this configuration exists on the hard drive.
        """
        libs_exist=any([os.path.exists(self.get_lib_path(l)) for l in self.libs])
        scripts_exist=any([os.path.exists(f) for f in self.script_files()])
        return libs_exist or scripts_exist



class RevisionDiff(object):
    """
    Describes the difference between two different script folder states.

    Args:
        lib_diffs (dict): dictionary with four entries:
            - ``"+"`` - list of libraries which are added in the first state compared to the second one;
            - ``"-"`` - list of libraries which are removed in the first state compared to the second one;
            - ``"*"`` - list of libraries which are changed in the first state compared to the second one;
            - ``"="`` - list of libraries which are the same in both states;
        common_lib_files_diff (str): difference in the common library files (files in the folders containing library subfolders).
            Can be ``"+"``, ``"-"``, ``"*"``, or ``"="``; the meaning is the same as for `lib_diffs`.
        scripts_diff (str): difference in the script files (files outside of the root library folder); the meaning is the same as for `common_lib_files_diff`.
    """
    def __init__(self, libs_diff=None, common_lib_files_diff="=", scripts_diff="="):
        self.libs_diff={"+":[],"-":[],"*":[],"=":[]} # additional, missing, modified, same
        if libs_diff:
            self.libs_diff.update(libs_diff) 
        self.scripts_diff=scripts_diff
        self.common_lib_files_diff=common_lib_files_diff
    def all_libs_diff(self):
        """
        Combine all library difference into one verdict.
        """
        diff_lens=dict([(k,len(v)) for k,v in self.libs_diff.items()])
        diff_lens[self.common_lib_files_diff]=diff_lens[self.common_lib_files_diff]+1
        if diff_lens["*"]>0 or (diff_lens["-"]>0 and diff_lens["+"]>0):
            return "*"
        if diff_lens["-"]>0:
            return "-"
        if diff_lens["+"]==0:
            return "+"
        return "="
    def all_diff(self):
        """
        Combine all differences (libraries and files) into one verdict.
        """
        return file_utils.combine_diff(self.all_libs_diff(),self.scripts_diff)
    def coverage(self, replace=True):
        """
        Get the coverage required to store changes of the first revision if it is to be replaced with the second one.

        Return either ``'script'`` (only store scripts, libraries are the same) or ``'full'`` (store both scripts and libraries).
        If ``replace==True``, assume that the new revision completely replaces the current one; otherwise, assume that it's added
        (i.e., if the current revision is larger than the new one, no need to store it).
        """
        if replace:
            if self.all_libs_diff()!="=":
                return "full"
            if self.scripts_diff!="=":
                return "script"
            return None
        else:
            if self.all_libs_diff() in "*-":
                return "full"
            if self.scripts_diff in "*-":
                return "script"
            return None
def _compare_source_folders(a, b):
    return file_utils.cmp_dirs(a,b,folder_filter=_store_folder_filter,file_filter=_store_files_filter,return_difference=True)
def _compare_source_files(a, a_dir, b, b_dir):
    """
    Compare two sets of files in different folders.

    `a` and `b` are two lists of files located in `a_dir` and `b_dir` respectively.
    """
    a=[os.path.normcase(n) for n in a]
    a.sort()
    b=[os.path.normcase(n) for n in b]
    b.sort()
    for s in set.intersection(set(a),set(b)):
        if not filecmp.cmp(os.path.join(a_dir,s),os.path.join(b_dir,s)):
            return "*"
    if a!=b:
        if set(a)>set(b):
            return "+"
        if set(a)<set(b):
            return "-"
        return "*"
    return "="
def _compare_revisions(a_config, b_config):
    """
    Compare two configs and return :class:`RevisionDiff` describing the difference.
    """
    diff=RevisionDiff()
    all_libs=set(a_config.libs+b_config.libs)
    for l in all_libs:
        cmp_res=_compare_source_folders(a_config.get_lib_path(l),b_config.get_lib_path(l))
        diff.libs_diff[cmp_res].append(l)
    diff.common_lib_files_diff=_compare_source_files(a_config.common_lib_files(path_type="name"),a_config.get_lib_path(),
                                                     b_config.common_lib_files(path_type="name"),b_config.get_lib_path())
    diff.scripts_diff=_compare_source_files(a_config.script_files(),a_config.store_path,
                                            b_config.script_files(),b_config.store_path)
    return diff







_full_history_size=40
_script_history_size=200
def set_history_size(full=None, script=None):
    """
    Set the size of the history shelf.
    
    If not ``None``, `full` and `script` define the size of the corresponding coverage shelves.
    Values ``<=0`` mean no limit.
    """
    global _full_history_size
    global _script_history_size
    if full is not None:
        _full_history_size=full
    if script is not None:
        _script_history_size=script
def get_history_size():
    """
    Get the sizes of the history shelves.
    
    Returns tuple ``(full_history_size, script_history_size)``.
    Values ``<=0`` mean no limit.
    """
    return _full_history_size, _script_history_size
def store(shelf, label=None, coverage="full", source_path=".", cleanup_shelf=False, **config_params):
    """
    Store the code to the shelf with a given label.
    
    Args:
        shelf (str): Storage shelf (folder).
        label (str): Snapshot label to be appended to the default filename (date and time of creation).
        coverage (str): Either ``'script'`` (include only application scripts) or ``'full'`` (include libraries as well).
        source_path (str): The code root folder.
        cleanup_shelf (bool): If ``True`` and the shelf size is above the limit, remove the oldest entries.
    
    ``**config_params`` are passed to the version config parameters.
    """
    if not coverage in ["full","script"]:
        raise ValueError("unrecognized coverage level: {0}".format(coverage))
    store_path=_store_file_path(shelf,label,coverage)
    version_config=VersionConfig.from_path(source_path,**config_params)
    if coverage=="full": # libraries
        for l in version_config.libs:
            source_lib_path=version_config.get_lib_path(l,relative=False)
            dest_lib_path=version_config.get_lib_path(l,relative=True)
            file_utils.zip_folder(store_path,source_lib_path,inside_path=dest_lib_path,folder_filter=_store_folder_filter,file_filter=_store_files_filter)
        for sf,df in zip(version_config.common_lib_files(path_type="absolute"),version_config.common_lib_files(path_type="relative")):
            file_utils.zip_file(store_path,sf,df)
    for f in version_config.script_files(): # scripts
        file_utils.zip_file(store_path,os.path.join(source_path,f),f)
    with _open_temp_file() as f: # version config
        version_config.to_file(f.f)
        f.f.flush()
        file_utils.zip_file(store_path,f.full_name,_version_config_file)
    with _open_temp_file() as f: # package versions
        version.write_version(f.f)
        f.f.flush()
        file_utils.zip_file(store_path,f.full_name,_dependencies_file)
    if cleanup_shelf:
        _cleanup_shelf(shelf,coverage,_full_history_size if coverage=="full" else _script_history_size)
            
def _clean_revision(version_config, diff=None):
    """
    Clean all parts of revision that are different from the target state (defined by diff).
    """
    for l in version_config.libs:
        if diff is None or l in (diff.libs_diff["*"]+diff.libs_diff["+"]):
            file_utils.retry_remove_dir(version_config.get_lib_path(l))
    if diff is None or diff.common_lib_files_diff in "*+":
        for f in version_config.common_lib_files():
            file_utils.retry_remove(f)
    if file_utils.dir_empty(version_config.get_lib_path(),folder_filter=_store_folder_filter,file_filter=_store_files_filter,level="recursive"):
        file_utils.retry_remove_dir(version_config.get_lib_path())
    if diff is None or diff.scripts_diff in "*+":
        for f in version_config.script_files():
            file_utils.retry_remove(f)
def _modify_revision(current_config, new_config):
    """
    Clean all parts of the revision to match the target state (defined by `new_config`).

    This includes removing unused libraries and changing the library folder.
    """
    for l in current_config.libs:
        source=current_config.get_lib_path(l)
        if l in new_config.libs:
            dest=new_config.get_lib_path(l)
            file_utils.retry_move_dir(source, dest)
        else:
            file_utils.retry_remove_dir(source)
    for f,source in zip(current_config.common_lib_files("name"),current_config.common_lib_files("absolute")):
        dest=os.path.join(new_config.get_lib_path(),f)
        if os.path.exists(os.path.split(dest)[0]): # check of the file is used by any libraries 
            file_utils.retry_move(source,dest)
        else:
            file_utils.retry_remove(source)
    file_utils.retry_remove_dir_if_empty(current_config.get_lib_path())
    template_files=current_config.template_script_files()
    for f in current_config.script_files(): # move scripts
        source=os.path.join(current_config.store_path,f)
        if (f in template_files) or (f in new_config.additional_scripts):
            dest=os.path.join(new_config.store_path,f)
            file_utils.retry_move(source,dest)
        else: 
            file_utils.retry_remove(source)
    current_lib_path=current_config.get_lib_path()
    if not file_utils.paths_equal(current_lib_path,new_config.get_lib_path()): #cleanup initial folder
        if file_utils.dir_empty(current_lib_path,folder_filter=_store_folder_filter,file_filter=_store_files_filter,level="recursive"):
            file_utils.retry_remove_dir(current_lib_path)
def _copy_revision(source_config, dest_config, overwrite=False):
    """
    Copy the new revision on top of the old one.
    """
    for l in set.intersection(set(source_config.libs),set(dest_config.libs)):
        source_path=source_config.get_lib_path(l)
        dest_path=dest_config.get_lib_path(l)
        if os.path.exists(dest_path) and not overwrite: # don't even add new files
            pass
        if os.path.exists(source_path):
            file_utils.retry_copy_dir(source_path,dest_path,folder_filter=_store_folder_filter,file_filter=_store_files_filter,overwrite=overwrite)
    source_files=[os.path.join(source_config.get_lib_path(),f) for f in source_config.common_lib_files(path_type="name")]
    source_files=source_files+[os.path.join(source_config.store_path,f) for f in source_config.script_files()]
    dest_files  =[os.path.join(  dest_config.get_lib_path(),f) for f in source_config.common_lib_files(path_type="name")]
    dest_files  =dest_files  +[os.path.join(  dest_config.store_path,f) for f in source_config.script_files()]
    for source_path,dest_path in zip(source_files,dest_files):
        if os.path.exists(source_path):
            file_utils.retry_copy(source_path,dest_path,overwrite=overwrite)
def _recall_config(source_config, current_config, merged_config, replace=False, overwrite=True):
    """
    Recall code from the `source_config` to the place of `current_config` to form `merged_config`.

    Store history of the current config if necessary.
    If ``replace==True``, remove all parts of the dest revision which are different from the source; otherwise, source is added to dest.
    """
    if current_config.exists(): 
        diff=_compare_revisions(a_config=current_config,b_config=source_config)
        diff_coverage=diff.coverage(replace)
        if diff_coverage:
            store("history",coverage=diff_coverage,source_path=current_config.store_path,cleanup_shelf=True)
        if not replace:
            if diff.all_diff() in "+=" and current_config.includes(merged_config):
                return
            _modify_revision(current_config,merged_config)
        else:
            _clean_revision(current_config)
            _modify_revision(current_config,merged_config)
    _copy_revision(source_config,merged_config,overwrite=overwrite)
    with open(os.path.join(merged_config.store_path,_version_config_file),"w") as f:
        merged_config.to_file(f)
        
def recall_from_folder(source_path, dest_path=".", replace=False, overwrite=True, source_config_params=None, recall_config_params=None):
    """
    Recall code from the source folder to the dest folder.

    If the configuration is changed, store the current state on the history shelf before changing it.
    
    Args:
        source_path (str): Path to the source folder.
        dest_path (str): Path to the destination folder.
        replace (bool): If ``True``, remove all parts of the dest revision which are different from the source; otherwise, source is added to dest.
        overwrite (bool): If ``True``, overwrite the old files.
        source_config_params (dict): Overrides source version config parameters.
        recall_config_params (dict): Overrides merged version config parameters.
    """
    source_config=VersionConfig.from_path(source_path,**(source_config_params or {}))
    current_config=VersionConfig.from_path(dest_path)
    merged_config=VersionConfig.from_path(source_path,**(recall_config_params or {}))
    merged_config.store_path=dest_path
    if not replace:
        merged_config=merged_config.update(source_config,override=True)
    _recall_config(source_config,current_config,merged_config,replace=replace,overwrite=overwrite)
    
def recall_from_file(file_name, dest_path=".", replace=False, overwrite=True, source_config_params=None, recall_config_params=None):
    """
    Recall code from the zip file.

    If the configuration is changed, store the current state on the history shelf before changing it.
    
    Arguments are the same as in :func:`recall_from_folder`, only instead of folder path it's zip file path.
    """
    if not os.path.exists(file_name):
        raise IOError("recalling path {0} does not exist".format(file_name))
    unpacked=_unpack_temp(file_name)
    recall_from_folder(unpacked,dest_path,replace=replace,overwrite=overwrite,
                       source_config_params=source_config_params,recall_config_params=recall_config_params)
    file_utils.retry_remove_dir(unpacked)
def recall_from_shelf(shelf, name, coverage, dest_path=".", replace=False, overwrite=True, source_config_params=None, recall_config_params=None):
    """
    Recall code from the shelf.

    If the configuration is changed, store the current state on the history shelf before changing it.
    
    Arguments are the same as in :func:`recall_from_file`, only instead of a path the file is specified by shelf, name and coverage.
    """
    store_path=_recall_file_path(shelf,coverage,name)
    recall_from_file(store_path,dest_path,replace=replace,overwrite=overwrite,
                       source_config_params=source_config_params,recall_config_params=recall_config_params)
def recall(shelf, name, coverage=None, replace=False, overwrite=True, **recall_config_params):
    """
    Alias for :func:`recall_from_shelf`.
    """
    recall_from_shelf(shelf,name,coverage,replace=replace,overwrite=overwrite,recall_config_params=recall_config_params)
def fetch(source_path, dest_path=".", overwrite=True, preserve_libs=True, **recall_config_params):
    """
    Fetch code library.

    If the configuration is changed, store the current state on the history shelf before changing it.
    
    Args:
        source_path (str): Path to the library root.
        dest_path (str): Path to the destination folder.
        overwrite (bool): If ``True``, overwrite the old files.
        preserve_libs (bool): If ``True``, preserve sub-libraries even if they are not specified in the `recall_config_params`.
        recall_config_params (dict): Overrides merged version config parameters (see :class:`VersionConfig`).
    """
    source_config=VersionConfig.from_path(source_path,lib_path="",libs=recall_config_params.get("libs",None))
    current_config=VersionConfig.from_path(dest_path)
    if preserve_libs and "libs" in recall_config_params:
        recall_config_params["libs"]=list(set(recall_config_params["libs"]+current_config.libs))
    merged_config=VersionConfig.from_path(dest_path,**recall_config_params).update(source_config,override=True)
    _recall_config(source_config,current_config,merged_config,replace=False,overwrite=overwrite)
    
def diff_from_latest(store_path=".", coverage=None):
    """
    Compare current revision with the latest item on the history shelf.
    
    Args:
        store_path (str): Path to the revision to check.
        coverage (str): Defines coverage levels to check. ``None`` means both ``'script'`` and ``'full'``.
    """
    if coverage in ["full","script"]:
        stored=_shelf_content("history",coverage,full_path=True)
    else:
        stored=_shelf_content("history","full",full_path=True)+_shelf_content("history","script",full_path=True)
    if len(stored)==0:
        vc=VersionConfig.from_path(store_path)
        return RevisionDiff({"+":list(vc.libs)}, "=" if len(vc.common_lib_files())==0 else "+", "=" if len(vc.script_files())==0 else "+")
    stored.sort(key=file_utils.get_file_creation_time)
    latest=stored[-1]
    unpacked=_unpack_temp(latest)
    diff=_compare_revisions(VersionConfig.from_path(store_path),VersionConfig.from_path(unpacked))
    file_utils.retry_remove_dir(unpacked)
    return diff
def store_script_if_changed(store_path=".", coverage=None):
    """
    Store script files (not library) if they are different from the latest revision.
    
    When storing changes, the shelves sizes are limited, and if the limit is exceeded, the oldest entries are deleted.
    For more details, see :func:`get_history_size` and :func:`set_history_size`.
    
    Args:
        store_path (str): Path to the revision to check.
        coverage (str): Defines coverage levels to check. ``None`` means both ``'script'`` and ``'full'``.
    """
    diff=diff_from_latest(store_path,coverage)
    if diff.scripts_diff!="=":
        store("history",coverage="script",source_path=store_path,cleanup_shelf=True)
        
_fetched=False
def fetch_and_store_script(source_path=None, dest_path=".", overwrite=True, once_per_run=True, preserve_libs=True, **recall_config_params):
    """
    Fetch code library from the `source_path` (current library path by default); store any recent changes of script or library on the history shelf.
    
    When storing changes, the shelves sizes are limited, and if the limit is exceeded, the oldest entries are deleted.
    For more details, see :func:`get_history_size` and :func:`set_history_size`.
    
    Args:
        source_path (str): Path to the library root. ``None`` means the current library path (library containing this module).
        dest_path (str): Path to the destination folder.
        overwrite (bool): If ``True``, overwrite the old files.
        once_per_run (bool): If ``True``, only perform operation once per run of the script. All subsequent call will return immediately.
        preserve_libs (bool): If ``True``, preserve sub-libraries even if they are not specified in the `recall_config_params`.
        recall_config_params (dict): Overrides merged version config parameters (see :class:`VersionConfig`).
    """
    global _fetched
    if (once_per_run and _fetched):
        return
    if source_path is None:
        source_path=module_utils.get_library_path()
    fetch(source_path,dest_path,overwrite,preserve_libs=preserve_libs,**recall_config_params)
    store_script_if_changed(dest_path)
    _fetched=True