from ...core.utils import files, dictionary

import platform
import ctypes
import sys
import os.path
import os


_module_parameters={"devices/dlls":dictionary.Dictionary()}

def get_os_lib_folder():
    """Get default Windows DLL folder (``System32`` or ``SysWOW64``, depending on Python and Windows bitness)"""
    if sys.platform!="win32":
        return ""
    arch=platform.architecture()[0]
    winarch="64bit" if platform.machine().endswith("64") else "32bit"
    if winarch==arch:
        return os.path.join(os.environ["WINDIR"],"System32")
    else: # 32 bit Python on 64 but OS (the reverse is impossible)
        return os.path.join(os.environ["WINDIR"],"SysWOW64")
os_lib_folder=get_os_lib_folder()

def get_program_files_folder():
    """Get default Windows Program Files folder (``Program Files`` or ``Program Files (x86)``, depending on Python and Windows bitness)"""
    arch=platform.architecture()[0]
    winarch="64bit" if platform.machine().endswith("64") else "32bit"
    if arch=="32bit" and winarch=="64bit":
        return os.environ.get("PROGRAMFILES(X86)",r"C:\Program Files (x86)")
    else:
        return os.environ.get("PROGRAMFILES",r"C:\Program Files")
program_files_folder=get_program_files_folder()



def load_lib(name, locations=("global",), call_conv="cdecl", locally=False, error_message=None, check_order="location"):
    """
    Load DLL.

    Args:
        name: name or path of the library (can also be a list or a tuple with several names, which are tried in that order).
        locations: list or tuple of locations to search for a library; the function tries locations in order and returns the first successfully loaded library
            a location is a string which can be a path to the containing folder,
            ``"parameter/*"`` (the remaining part is a subpath inside ``"devices/dlls"`` library parameters; if this parameter is defined, it names folder or file for the dll),
            or ``"global"`` (load path as is; also searches in the standard OS specified locations determined by ``PATH`` variable, e.g., ``System32`` folder).
        locally(bool): if ``True``, prepend path to the DLL containing folder to the environment ``PATH`` folders;
            this is usually required, if the loaded DLL imports other DLLs in the same folder
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
    if not isinstance(locations,(list,tuple)):
        locations=[locations]
    if check_order=="location":
        check_order=[(loc,n) for loc in locations for n in name]
    elif check_order=="name":
        check_order=[(loc,n) for n in name for loc in locations]
    for loc,n in check_order:
        if loc=="global":
            folder=""
        else:
            if loc.startswith("parameter/"):
                par_name=loc[len("parameter/"):]
                dll_paths=_module_parameters["devices/dlls"]
                if par_name in dll_paths:
                    loc=dll_paths[par_name]
                else:
                    continue
            if loc.lower().endswith(".dll"):
                folder,n=os.path.split(loc)
            else:
                folder=loc
        path=os.path.join(folder,n)
        print(path)
        if locally:
            loc_folder,loc_name=os.path.split(path)
            old_env_path=os.environ["PATH"]
            env_paths=old_env_path.split(";")
            if not any([files.paths_equal(loc_folder,ep) for ep in env_paths if ep]):
                os.environ["PATH"]=files.normalize_path(loc_folder)+";"+os.environ["PATH"]+";"+files.normalize_path(loc_folder)+";"
            path=loc_name if folder=="" else "./"+loc_name
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