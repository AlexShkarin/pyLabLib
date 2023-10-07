import contextlib

pyd_load_error_msg="could not load C extensions: {}\nInstall the package from the appropriate binary distribution, or install an appropriate C compiler if you use the source distribution"
pyd_load_warn_msg="could not load C extensions: {}\nUsing a fallback instead, which might hurt the performance.\nTo avoid, install the package from the appropriate binary distribution, or install an appropriate C compiler if you use the source distribution"

@contextlib.contextmanager
def try_import_cext():
    """Context manager for trying to import a possibly missing C extension; if an error arises, re-raises with a more detailed message"""
    try:
        yield
    except ImportError as err:
        raise ImportError(pyd_load_error_msg.format(err))