.. _install:

Installation
=========================

.. _install-standard:

Standard install
-------------------------

You can install the library from PyPi:

.. code-block:: none

    pip install pylablib

If you already have it installed, you can upgrade it to get the newest version:

.. code-block:: none

    pip install -U pylablib

This will install the full set of dependencies: basic dependencies and computing packages (``numpy``, ``scipy``, ``pandas``, ``numba``, ``rpyc``), basic device communication packages (``pyft232``, ``pyvisa``, ``pyserial``, ``pyusb``), and PyQt5-based GUI (``pyqt5`` and ``pyqtgraph``). You can also install additional device library dependencies (``nidaqmx`` and ``websocket-client``) using the extra requirements feature of pip:

.. code-block:: none

    pip install -U pylablib[devio-full]

.. _install-minimal:

Minimal install
-------------------------

In case you do not want some of these packages installed, or they are unavailable on your platform, you can install a lightweight version of pylablib called ``pylablib-lightweight``. It contains exactly the same code, but has only the most basic dependencies (``numpy``, ``scipy``, and ``pandas``):

.. code-block:: none

    pip install -U pylablib-lightweight

With this, the basic functionality (such as data processing or file IO) will work, but more advanced features such as device communication and GUI, will require additional packages. In most cases, the raised errors will notify which packages are missing. These can be installed either manually, or using the extra requirements:

    - ``[extra]`` extra packages used in some situations: ``numba`` (speeds up some data processing) and ``rpyc`` (communication between different PCs)
    - ``[devio]`` basic devio packages: ``pyft232``, ``pyvisa``, ``pyserial``, and ``pyusb``
    - ``[devio-extra]`` additional devio packages: ``nidaqmx`` and ``websocket-client``
    - ``[gui-pyqt5]`` `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/>`_-based GUI: ``pyqt5`` and ``pyqtgraph``. Should not be used together with ``[gui-pyside2]``
    - ``[gui-pyside2]`` `PySide2 <https://www.pyside.org/>`_-based GUI: ``pyside2`` and ``pyqtgraph``. Should not be used together with ``[gui-pyqt5]``

The options can be combined. For example, 

.. code-block:: none

    pip install pylablib-lightweight[extra,devio,gui-pyside2]

installs the dependencies as the usual pylablib distribution, but with PySide2 Qt5 backend instead of PyQt5.

.. _install-anaconda:

Anaconda install
-------------------------

The package is also available on Anaconda via ``conda-forge`` channel. To install it, run

.. code-block:: none

    conda install -c conda-forge pylablib

in the Anaconda prompt.

The Anaconda version of pylablib comes with all the standard dependencies except for ``pyft232`` , ``nidaqmx`` and ``websocket-client``, which are not available on ``conda-forge`` channel. This means, that :ref:`Thorlabs APT/Kinesis <stages_thorlabs_kinesis>`, :ref:`NI DAQs <daqs_nidaq>`, and some functionality of :ref:`M2 Solstis laser <lasers_m2>` are not accessible. To use those, it is recommended to either install those packages explicitly via ``pip`` (keep in mind that it can break Anaconda environment), or use a standalone Python distribution.



.. _install-usage:

Usage
-------------------------

To access to the most common features simply import the library::

    import pylablib as pll
    # Create a parameter dictionary (e.g., for some processing script)
    parameters = pll.Dictionary({"par/x":1, "par/y":2, "par/z":[3,4,5], "out":"result"})
    pll.save_dict(parameters, "parameters.dat")  # save parameters to a text file

More advanced features (e.g., :ref:`device communication <devices_basics>`) should be imported directly::

    from pylablib.devices import Andor  # import Andor devices module
    cam = Andor.AndorSDK2Camera()  # connect to Andor SDK2 camera (e.g., iXon)
    cam.set_exposure(0.1)  # set exposure to 100ms
    frame = cam.snap()  # grab a single frame
    cam.close()  # close the connection

.. _install-requirements:

Dependencies and requirements
------------------------------

The basic package dependencies are `NumPy <https://docs.scipy.org/doc/numpy/>`_ for basic computations and overall array interface, `SciPy <https://docs.scipy.org/doc/scipy/reference/>`_ for advanced computations (interpolation, optimization, special functions), and `pandas <https://pandas.pydata.org/>`_ for heterogeneous tables (``DataFrame``). In addition, it is recommended to have `Numba <https://numba.pydata.org/>`_ package to speed up some computations. Finally, if you use options for remote computing and communication between different PCs, you need to install `RPyC <https://rpyc.readthedocs.io/en/latest/>`_. Note that when installed directly from pip, ``numpy`` comes with the OpenBLAS version of the linear algebra library; if other version (e.g., Intel MKL) is preferred, it is a good idea to have ``numpy`` already installed before installing pylablib.

The main device communication packages are `PyVISA <https://pyvisa.readthedocs.io/en/master/>`_ and `pySerial <https://pythonhosted.org/pyserial/>`_, which cover the majority of devices. Several devices (e.g., :ref:`Thorlabs Kinesis <stages_thorlabs_kinesis>` and :ref:`Attocube ANC 350 <stages_attocube_anc350>`) require additional communication packages: `pyft232 <https://github.com/lsgunth/pyft232>`_ and `PyUSB <https://pyusb.github.io/pyusb/>`_. Finally, some particular devices completely or partially rely on specific packages: `NI-DAQmx <https://nidaqmx-python.readthedocs.io/en/latest/>`_ for :ref:`NIDAQ <daqs_nidaq>` and `websocket-client <https://websocket-client.readthedocs.io/en/latest/>`_ for additional :ref:`M2 Solstis <lasers_m2>` functionality.

Finally, GUI and advanced multi-threading relies on Qt5, which has two possible options. The first (default) option is `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/>`_ with `sip <https://www.riverbankcomputing.com/software/sip/>`_ for some memory management functionality. Note that while newer PyQt5 versions ``>=5.11`` already come with ``PyQt5-sip``, older versions require a separate ``sip`` installation. Hence, if you use an older ``PyQt5`` version, you need to install ``sip`` separately. The second possible Qt5 option is `PySide2 <https://www.pyside.org/>`_ with `shiboken2 <https://wiki.qt.io/Qt_for_Python/Shiboken>`_. Both PyQt5 and PySide2 should work equally well, and the choice mostly depends on what is already installed, because having both PyQt5 and PySide2 might lead to conflicts. Finally, plotting relies on `pyqtgraph <http://www.pyqtgraph.org/>`_, which, starting with version 0.11m is compatible with both PySide2 and PyQt5.

The package has been tested with Python 3.6 through 3.9, and is incompatible with Python 2. The last version officially supporting Python 2.7 is 0.4.0. Furthermore, testing has been mostly performed on 64-bit Python. This is the recommended option, as 32-bit version limitations (most notably, limited amount of accessible RAM) mean that it should only be used when absolutely necessary, e.g., when some required packages or libraries are only available in 32-bit version.

.. _install-github:

Installing from GitHub
-------------------------

The most recent and extensive, but less tested and documented, version of this library is available on GitHub at https://github.com/AlexShkarin/pyLabLib/. There are several versions of installing it:

    - Install using pip using GitHub as a library source:
    
      .. code-block:: none

        pip install -U git+https://github.com/AlexShkarin/pyLabLib.git

    - Download it as a zip-file and unpack it into any appropriate place (can be folder of the project you're working on, Python ``site-packages`` folder, or any folder added to ``PATH`` or ``PYTHONPATH`` variable).

      To download the code of a specific version, you can choose it in the dropdown `Branch` menu under `Tags` tab. This is the same code as available on PyPi.

      Keep in mind that, unlike the first method, the required packages will not be automatically installed, so this has to be done manually:

      .. code-block:: none

        pip install numpy scipy pandas numba rpyc
        pip install pyft232 pyvisa pyserial pyusb nidaqmx websocket-client
        pip install pyqt5 pyqtgraph
    
    - Clone the repository to your computer In order to easily get updates in order to easily get updates. For that, you need to install Git (https://git-scm.com/), and use the following commands in the command line (in the folder where you want to store the library):

      .. code-block:: none

        git clone https://github.com/AlexShkarin/pyLabLib
        cd ./pyLabLib

      Whenever you want to update to the most recent version, simply type
    
      .. code-block:: none

        git pull

      in the library folder. Keep in mind that any changes that you make to the library code might conflict with the new version that you pull from GitHub, so you should not modify anything in this folder if possible.

.. _install-feedback:

Support and feedback
-------------------------

If you have any issues, suggestions, or feedback, you can either raise an issue on GitHub at https://github.com/AlexShkarin/pyLabLib/issues, or send an e-mail to pylablib@gmail.com.