"""
Current version and function that defines compatibility with previous version.
To be changed in future packages.
"""
from future.utils import viewitems

import sys
from .utils import module as module_utils #@UnresolvedImport


full_version=(0,2,0)
def is_compatible(v, package=None, module=None):
    return full_version>=v

### Additional packages routines ###
_required_packages_names=["future","rpyc", # generic required packages
                          "numpy","scipy","matplotlib","numba","pandas", # standard scientific packages
                          "pyusb","python-usbtmc","pywinusb","pyserial","pyvisa","pyft232","websocket-client", # general device communication:
                            # USB (generic USB, requires libusb library), USB-MTC (VISA-like package for Linux), pywinusb(USB HID talking), Serial port, VISA wrapper
                          "nidaqmx" # special device communication: NIDAQmx, ZurichInstrument (2 different versions)
                          ] # non-standard packages
required_packages=dict([ (name,module_utils.get_package_version(name)) for name in _required_packages_names ])
_python_version_full=sys.version_info
python_version="{}.{}.{}".format(*_python_version_full)


def write_version(f):
    f.write("Python version: "+python_version+"\n\n")
    f.write("Non-standard packages:\n")
    for p_name,p_version in viewitems(required_packages):
        if p_version is not None:
            f.write("  {0:20s} {1}\n".format(p_name,p_version))
    f.write("\nCore library version: {}.{}.{}\n".format(*full_version))