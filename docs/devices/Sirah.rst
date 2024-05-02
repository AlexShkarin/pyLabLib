.. _lasers_sirah:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

Sirah Matisse laser
=======================

Matisse is a family of Ti:Saph and dye ring lasers produces by Sirah.

The main laser class is :class:`pylablib.devices.Sirah.SirahMatisse<.Sirah.Matisse.SirahMatisse>`.

Software requirements
-----------------------

The device requires Matisse Commander software supplied by the manufacturer. When it is installed, it shows up as a VISA resource and can be accessed without further requirements.


Connection
-----------------------

The laser is identified by its VISA address, typically looking like ``"USB0::0x17E7::0x0102::01-01-10::INSTR"``::

    >> import pylablib as pll
    >> pll.list_backend_resources("visa")
    ('USB0::0x17E7::0x0102::01-01-10::INSTR',)
    >> from pylablib.devices import Sirah
    >> laser = Sirah.SirahMatisse("USB0::0x17E7::0x0102::01-01-10::INSTR")
    >> laser.close()

Alternatively, one can use a network connection to the Matisse Commander server, if it is enabled in the Matisse Commander communication Options::

    >> import pylablib as pll
    >> from pylablib.devices import Sirah
    >> laser = Sirah.SirahMatisse(("127.0.0.1",30000))  # local server on the default port 30000
    >> laser.close()

Operation
------------------------

The method names are pretty self-explanatory, and mostly correspond directly to the operations in the Matisse Commander. However, only the basic tuning and scanning functions supplied by the interface are provided, and the more advanced once like scanning BRF/etalon or interfacing with a wavemeter need to be implemented by the user based on the defined methods.

Note that depending on the specific model not all methods are available, e.g., reference cell locking is not available in TR/DR configuration.