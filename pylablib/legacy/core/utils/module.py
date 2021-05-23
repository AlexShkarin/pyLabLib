"""
Library for dealing with python module properties.
"""

try:
    from importlib import reload
except ImportError:
    from imp import reload

import pkg_resources
import sys
import subprocess
import os.path
from . import general, files as file_utils

def get_package_version(pkg):
    """
    Get the version of the package.
    
    If the package version is unavailable, return ``None``.
    """
    try:
        return pkg_resources.get_distribution(pkg).version
    except pkg_resources.DistributionNotFound:
        return None

def _tryint(v):
    try:
        return int(v)
    except ValueError:
        return v
def cmp_versions(ver1, ver2):
    """
    Compare two package versions.
    
    Return ``'<'`` if the first version is older (smaller), ``'>'`` if it's younger (larger) or ``'='`` if it's the same.
    """
    ver1=[_tryint(v.strip()) for v in ver1.split(".")]
    ver2=[_tryint(v.strip()) for v in ver2.split(".")]
    if ver1>ver2:
        return ">"
    if ver1<ver2:
        return "<"
    return "="
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
    return cmp_versions(ver,cver)
            


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

def get_reload_order(modules):
    """
    Find reload order for modules which respects dependencies (a module is loaded before its dependants).
    
    `modules` is a dict ``{name: module}``.
    
    The module dependencies (i.e., the modules which the current module depends on) are described in the variable ``_depends_local`` defined at its toplevel
    (missing variable means no dependencies).
    """
    deps={}
    for name,module in modules.items():
        try:
            deps[name]=[expand_relative_path(name,dep) for dep in module._depends_local]
        except AttributeError:
            pass
        for ch_name in modules:
            if ch_name.startswith(name+"."):
                deps.setdefault(name,[]).append(ch_name)
    for name in deps:
        deps[name]=list(set(deps[name]))
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
    return os.path.join(*file_utils.fullsplit(module_path)[:-3])


def get_library_name():
    """
    Get the name for the pyLabLib library (the one containing current the module).
    """
    module_name=__name__
    return ".".join(module_name.split(".")[:-3])


def pip_install(pkg, upgrade=True):
    """
    Call ``pip install`` for a given package.
    
    If ``upgrade==True``, call with ``--upgrade`` key (upgrade current version if it is already installed).
    """
    if upgrade:
        subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", pkg])
    else:
        subprocess.call([sys.executable, "-m", "pip", "install", pkg])

def install_if_older(pkg, min_ver=""):
    """
    Install `pkg` from the default PyPI repository if its version is lower that `min_ver`
    
    If `min_ver` is ``None``, upgrade to the newest version regardless; if ``min_ver==""``, install only if no version is installed
    """
    if get_package_version(pkg) is None or cmp_package_version(pkg,min_ver)=="<":
        pip_install(pkg,upgrade=True)