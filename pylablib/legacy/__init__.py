import warnings
warnings.warn("legacy (pre 1.0) code will be removed in future versions",FutureWarning)

import os
import os.path
from .core.utils import module as module_utils, library_parameters  #@UnresolvedImport

from .core import *

_load_path=os.path.abspath(os.curdir)

par=library_parameters.LibraryParametersStorage(__name__)
def reload_all(from_load_path=True, keep_parameters=True):
    """
    Reload all loaded modules.

    If ``keep_parameters==True``, keep the current library parameters (``pylablib.par``); otherwise, reset them to default.
    """
    if keep_parameters:
        old_par=par[""].as_dict("flat")
    if from_load_path:
        cur_dir=os.path.abspath(os.curdir)
        os.chdir(_load_path)
        try:
            module_utils.reload_package_modules(__name__)
        finally:
            os.chdir(cur_dir)
    else:
        module_utils.reload_package_modules(__name__)
    par.refresh()
    if keep_parameters:
        for k,v in old_par.items():
            try:
                par[k]=v
            except KeyError:
                pass

def unload_all():
    """
    Reload all loaded modules.
    """
    module_utils.unload_package_modules(__name__)