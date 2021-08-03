import os
from .core.utils import module as module_utils
from .core.utils import library_parameters
from .core.fileio import loadfile
par=library_parameters.library_parameters
temp_par=library_parameters.temp_library_parameters

from .core.dataproc.__export__ import *
from .core.devio.__export__ import *
from .core.fileio.__export__ import *
from .core.gui.__export__ import *
from .core.thread.__export__ import *
from .core.utils.__export__ import *

_load_path=os.path.abspath(os.curdir)

__version__=module_utils.get_package_version("pylablib") or module_utils.get_package_version("pylablib-lightweight")

def reload_all(from_load_path=True, keep_parameters=True):
    """
    Reload all loaded modules.

    If ``keep_parameters==True``, keep the current library parameters (``pylablib.par``); otherwise, reset them to default.
    """
    if keep_parameters:
        old_par=library_parameters.library_parameters.as_dict("flat")
    if from_load_path:
        cur_dir=os.path.abspath(os.curdir)
        os.chdir(_load_path)
        try:
            module_utils.reload_package_modules(__name__)
        finally:
            os.chdir(cur_dir)
    else:
        module_utils.reload_package_modules(__name__)
    if keep_parameters:
        library_parameters.library_parameters[""]=old_par

def unload_all():
    """
    Reload all loaded modules.
    """
    module_utils.unload_package_modules(__name__)

def load_par(path):
    """Load library parameters from a file"""
    lpar=loadfile.load_dict(path)
    for k,v in lpar.items():
        par[k]=v