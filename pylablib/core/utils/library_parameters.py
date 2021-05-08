"""Storage for global library parameters"""

import contextlib

from . import dictionary
library_parameters=dictionary.Dictionary()


@contextlib.contextmanager
def temp_library_parameters(restore=None):
    """
    Context manager, which restores library parameters upon exit.

    If ``rester is not None``, it can specify a list of parameters to be restored (by default, all parameters).
    """
    if restore is None:
        params=library_parameters.copy()
    else:
        no_params=[p for p in restore if p not in library_parameters]
        params={p:library_parameters[p] for p in restore if p in library_parameters}
    try:
        yield
    finally:
        if restore is None:
            library_parameters[""]=params
        else:
            for np in no_params:
                if np in library_parameters:
                    del library_parameters[np]
            for k,v in params.items():
                library_parameters[k]=v