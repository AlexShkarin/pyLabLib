from ...core.utils import files

import platform
import ctypes
import sys
import os.path
import os


def get_default_lib_folder(absolute=True):
    """
    Get default DLL folder withing the package, depending on the Python bitness
    
    If ``absolute==True``, get absolute path (including pyLabLib folder); otherwise, get subfolder within pyLabLib folder.
    """
    arch=platform.architecture()[0]
    if arch=="32bit":
        archfolder="x32"
    elif arch=="64bit":
        archfolder="x64"
    else:
        raise ImportError("Unexpected system architecture: {0}".format(arch))
    module_folder=os.path.split(files.normalize_path(sys.modules[__name__].__file__))[0] if absolute else os.path.join("aux_libs","devices")
    return os.path.join(module_folder,"libs",archfolder)
default_lib_folder=get_default_lib_folder()
default_rel_lib_folder=get_default_lib_folder(absolute=False)

def get_os_lib_folder():
    """Get default Windows DLL folder (``System32`` or ``SysWOW64``, depending on Python and Windows bitness)"""
    if sys.platform!="win32":
        return ""
    arch=platform.architecture()[0]
    winarch="64bit" if platform.machine().endswith("64") else "32bit"
    if winarch==arch:
        return os.path.join(os.environ["WINDIR"],"System32")
    else:
        return os.path.join(os.environ["WINDIR"],"SysWOW64")
default_placing_message="The libraries should be placed in {} or in {}".format(default_lib_folder,get_os_lib_folder())

def load_lib(name, locations=("global",), call_conv="cdecl", locally=False, error_message=None, check_order="location"):
    """
    Load DLL.

    Args:
        name: name or path of the library (can also be a list or a tuple with several names, which are tried in that order).
        locations: list or tuple of locations to search for a library; the function tries locations in order and returns the first successfully loaded library
            a location is a string which can be a path to the containing folder, ``"local"`` (local package path given by :func:`get_default_lib_folder`),
            or ``"global"`` (load path as is; also searches in the standard OS specified locations determined by ``PATH`` variable, e.g., ``System32`` folder)
        locally(bool): if ``True``, change local path to allow loading of dependent DLLs
        call_conv(str): DLL call convention; can be either ``"cdecl"`` (corresponds to ``ctypes.cdll``) or ``"stdcall"`` (corresponds to ``ctypes.windll``)
        error_message(str): error message to add in addition to the default error message shown when the DLL is not found
        check_order(str): determines the order in which possible combinations of names and locations are looped over;
            can be ``"location"`` (loop over locations, and for each location loop over names), ``"name"``  (loop over names, and for each name loop over locations),
            or a list of tuples ``[(loc,name)]`` specifying order of checking
            (in the latter case, `name` and `location` arguments are ignored, except for generating error mesage).
    """
    if platform.system()!="Windows":
        raise OSError("DLLs are not available on non-Windows platform")
    if not isinstance(name,(list,tuple)):
        name=[name]
    if check_order=="location":
        check_order=[(loc,n) for loc in locations for n in name]
    elif check_order=="name":
        check_order=[(loc,n) for n in name for loc in locations]
    for loc,n in check_order:
        if loc=="local":
            folder=default_lib_folder
        elif loc=="global":
            folder=""
        else:
            if loc.lower().endswith(".dll"):
                folder,n=os.path.split(loc)
            else:
                folder=loc
        path=os.path.join(folder,n)
        if locally:
            loc_folder,loc_name=os.path.split(path)
            old_env_path=os.environ["PATH"]
            env_paths=old_env_path.split(";")
            if not any([files.paths_equal(loc_folder,ep) for ep in env_paths if ep]):
                os.environ["PATH"]=files.normalize_path(loc_folder)+";"+os.environ["PATH"]+";"+files.normalize_path(loc_folder)+";"
            path=loc_name
        try:
            if call_conv=="cdecl":
                return ctypes.cdll.LoadLibrary(path)
            elif call_conv=="stdcall":
                return ctypes.windll.LoadLibrary(path)
            else:
                raise ValueError("unrecognized call convention: {}".format(call_conv))
        except OSError:
            if locally:
                os.environ["PATH"]=old_env_path
    error_message="\n"+error_message if error_message else ""
    raise OSError("can't import module {}".format(" or ".join(name))+error_message)