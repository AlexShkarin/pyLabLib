.. _install:

============
Installation
============

You can install the library using pip::

    pip install pylablib

This will install only the minimal subset of dependencies. To add packages needed for device communication, you can specify ``devio`` extra (on non-Windows systems use ``devio-basic``, as some of the packages are not available there). To add packages needed for GUI, you can specify ``gui`` extra (note that one of the required packages is ``PyQt5``, which is not available on pip for Python 2.7; hence, it needs to be installed prior to installing pyLabLib). To grab full set of required packages, call::

    pip install pylablib[devio,gui]

-----
Usage
-----

To access to the most common functions simply import the library::

    import pylablib as pll
    data = pll.load("data.csv","csv")

------------
Requirements
------------

The package requires `numpy <http://docs.scipy.org/doc/numpy/>`_, `scipy <http://docs.scipy.org/doc/scipy/reference/>`_, `matplotlib <http://matplotlib.org/>`_, `pandas <https://pandas.pydata.org/>`_ and `numba <http://numba.pydata.org/>`_ modules for computations. Note that when installed directly from pip, ``numpy`` comes with the OpenBLAS version of the linear algebra library; if other version (e.g., Intel MKL) is preferred, it is a good idea to ``numpy`` already installed before installing ``pyLabLib``. All other packages can be safely installed from pip.

`PyVISA <https://pyvisa.readthedocs.io/en/master/>`_ and `pySerial <https://pythonhosted.org/pyserial/>`_ are the main packages used for the device communication. For some specific devices you might require ``pyft232``, ``pywinusb``, ``websocket-client``, or `nidaqmx <https://nidaqmx-python.readthedocs.io/en/latest/>`_ (keep in mind that it's different from the ``PyDAQmx`` package). Some devices have additional requirements (devices software or drivers installed, or some particular dlls), which are specified in their description.

The package has been tested with Python 3.6 and Python 3.7. Python 2.7 might not be fully compatible anymore (although effort is made to preserve the compatibility, testing with Python 2.7 is far less extensive). The last version officially supporting Python 2.7 is 0.4.0.

.. _install-github:

-----------------------
Installing from  GitHub
-----------------------

The most recent and extensive, but less documented, version of this library is available on GitHub at https://github.com/AlexShkarin/pyLabLib/. To simply get the most recent version, you can download it as a zip-file and unpack it into any appropriate place (can be folder of the project you're working on, Python site-packages folder, or any folder added to Python path variable).

To download the code of a specific version, you can choose it in the dropdown `Branch` menu under `Tags` tab. This is the same code as available on pip, but with additional device dlls.

Keep in mind that required packages will not be automatically installed, so this has to be done manually::

    pip install future numpy scipy matplotlib pandas numba rpyc
    pip install pyft232 pyvisa pyserial nidaqmx pywinusb websocket-client
    pip install pyqt5 sip pyqtgraph

In order to easily get updates, you can clone the repository to your computer. For that, you need to install Git (https://git-scm.com/), and use the following commands in the command line (in the folder where you want to store the library)::

    git clone https://github.com/AlexShkarin/pyLabLib
    cd ./pyLabLib

Whenever you want to update to the most recent version, simply type ::
    
    git pull

in the library folder. Keep in mind that any changes that you make to the library code might conflict with the new version that you pull from GitHub, so you should not modify anything in this folder if possible.