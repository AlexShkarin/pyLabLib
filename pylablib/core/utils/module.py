"""
Library for dealing with python module properties.
"""

try:
    from importlib import reload
except ImportError:
    from imp import reload  # pylint: disable=deprecated-module

try:
    from importlib import metadata
except ImportError:
    metadata=None
try:
    import importlib.resources as pkg_resources
except ImportError:
    pkg_resources=None
import sys
import subprocess
import os
import inspect

from . import general, files as file_utils



def get_package_version(pkg):
    """
    Get the version of the package.
    
    If the package version is unavailable, return ``None``.
    """
    if metadata is not None:
        try:
            return metadata.metadata(pkg)["version"]
        except metadata.PackageNotFoundError:
            return None
    try:
        return pkg_resources.get_distribution(pkg).version
    except (pkg_resources.DistributionNotFound,pkg_resources.VersionConflict):
        return None

def _tryint(v):
    try:
        return int(v)
    except ValueError:
        return v
def cmp_versions(ver1, ver2, default="?"):
    """
    Compare two package versions.
    
    Return ``'<'`` if the first version is older (smaller), ``'>'`` if it's younger (larger) or ``'='`` if it's the same.
    If the versions are not comparable (e.g., have different format), return `default`.
    """
    ver1=[_tryint(v.strip()) for v in str(ver1).split(".")]
    ver2=[_tryint(v.strip()) for v in str(ver2).split(".")]
    try:
        if ver1>ver2:
            return ">"
        if ver1<ver2:
            return "<"
        return "="
    except TypeError:
        return default
def cmp_package_version(pkg, ver):
    """
    Compare current package version to `ver`.
    
    `ver` should be a name of the package (rather than the module).
    Return ``'<'`` if current version is older (smaller), ``'>'`` if it's younger (larger) or ``'='`` if it's the same.
    If the package version is unavailable, return ``None``.
    """
    cver=get_package_version(pkg)
    if cver is None:
        return None
    if ver=="":
        return ">"
    return cmp_versions(cver,ver)



def expand_relative_path(module_name, rel_path):
    """
    Turn a relative module path into an absolute one.
    
    `module_name` is the absolute name of the reference module, `rel_path` is the path relative to this module.
    """
    module_path=module_name.split(".")
    if not rel_path.startswith("."):
        return rel_path
    else:
        while rel_path.startswith("."):
            rel_path=rel_path[1:]
            module_path=module_path[:-1]
        return ".".join(module_path)+"."+rel_path


def get_loaded_package_modules(pkg_name):
    """
    Get all modules in the package `pkg_name`.
    
    Returns a dict ``{name: module}``.
    """
    prefix=pkg_name+"."
    return dict([(name,module) for name,module in sys.modules.items() if (name.startswith(prefix) or name==pkg_name) and module is not None])
def get_imported_modules(module, explicit=False):
    """
    Get modules imported within a given module.

    If ``explicit==True``, take into account only toplevel objects which are modules (corresponds to ``import module`` or ``from package import module`` statements)
    If ``explicit==False``, also include all modules containing toplevel objects (corresponds to ``from module import Class`` or ``from package import function`` statements).
    Return a dictionary ``{name: module}`` (modules with the same name are considered to be the same).
    """
    imported={}
    for n in module.__dict__:
        v=getattr(module,n,None)
        if v is not None:
            if inspect.ismodule(v):
                imported[v.__name__]=v
            elif not explicit:
                cm=inspect.getmodule(v)
                if cm is not None and cm is not module:
                    imported[cm.__name__]=cm
    return imported

def get_reload_order(modules):
    """
    Find reload order for modules which respects dependencies (a module is loaded before its dependents).
    
    `modules` is a dict ``{name: module}``.
    
    The module dependencies (i.e., the modules which the current module depends on) are determined based on imported modules and modules containing toplevel module objects.
    """
    deps={}
    for name,module in modules.items():
        deps[name]=deps.get(name,set())|{m for m in get_imported_modules(module) if m in modules}
        for ch_name in modules:
            if ch_name.startswith(name+"."):
                deps.setdefault(name,set()).add(ch_name)
    for name in deps:
        deps[name]=set(deps[name])
    order=general.topological_order(deps)
    order=[name for name in modules if not name in order]+order
    return order
def reload_package_modules(pkg_name, ignore_errors=False):
    """
    Reload package `pkg_name`, while respecting dependencies of its submodules.
    
    If ``ignore_errors=True``, ignore :exc:`ImportError` exceptions during the reloading process.
    """
    modules=get_loaded_package_modules(pkg_name)
    order=get_reload_order(modules)
    for name in order:
        try:
            reload(modules[name])
        except ImportError:
            if not ignore_errors:
                raise
def unload_package_modules(pkg_name, ignore_errors=False):
    """
    Reload package `pkg_name`, while respecting dependencies of its submodules.
    
    If ``ignore_errors=True``, ignore :exc:`ImportError` exceptions during the reloading process.
    """
    modules=get_loaded_package_modules(pkg_name)
    order=get_reload_order(modules)
    for name in order:
        try:
            del sys.modules[name]
        except IndexError:
            if not ignore_errors:
                raise
            
            
def get_library_path():
    """
    Get a filesystem path for the pyLabLib library (the one containing current the module).
    """
    module_path=sys.modules[__name__].__file__
    module_path=file_utils.normalize_path(module_path)
    return os.path.join(*file_utils.fullsplit(module_path)[:-3])  # pylint: disable=no-value-for-parameter


def get_library_name():
    """
    Get the name for the pyLabLib library (the one containing current the module).
    """
    module_name=__name__
    return ".".join(module_name.split(".")[:-3])

def get_executable(console=False):
    """
    Get Python executable.

    If ``console==True`` and the current executable is windowed (i.e., ``"pythonw.exe"``), return the corresponding ``"python.exe"`` instead.
    """
    folder,file=os.path.split(sys.executable)
    if file.lower()=="pythonw.exe" and console:
        return os.path.join(folder,"python.exe")
    return sys.executable
def get_python_folder():
    """Return Python interpreter folder (the folder containing the python executable)"""
    return os.path.split(os.path.abspath(sys.executable))[0]


def pip_install(pkg, upgrade=False):
    """
    Call ``pip install`` for a given package.
    
    If ``upgrade==True``, call with ``--upgrade`` key (upgrade current version if it is already installed).
    """
    if upgrade:
        subprocess.call([get_executable(console=True), "-m", "pip", "install", "--upgrade", pkg])
    else:
        subprocess.call([get_executable(console=True), "-m", "pip", "install", pkg])

def install_if_older(pkg, min_ver="", ignore_frozen=True):
    """
    Install `pkg` from the default PyPI repository if its version is lower that `min_ver`
    
    If `min_ver` is ``None``, upgrade to the newest version regardless; if ``min_ver==""``, install only if no version is installed.
    Return ``True`` if the package has just been installed.
    If `ignore_frozen` is ``True`` and the code is running in a frozen package (e.g., PyInstaller), always return ``False`` and do not try to install anything.
    """
    if ignore_frozen and getattr(sys,"frozen",False):
        return False
    if get_package_version(pkg) is None or cmp_package_version(pkg,min_ver)=="<":
        pip_install(pkg,upgrade=True)
        return True
    return False
