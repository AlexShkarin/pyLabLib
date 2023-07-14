.. _elektroautomatik_sources:

.. note::
    Basic sensors communication concepts are described on the corresponding :ref:`page <basic_sensors_basics>`

Elektro Automatik sources
==============================

Elektro Automatik manufactures a range of lab power supplies. The code has been tested with PS-2000B series controller (specifically, PS 2042-06B).

The main device class is :class:`pylablib.devices.ElektroAutomatik.PS2000B<.ElektroAutomatik.base.PS2000B>`.


Software requirements
-----------------------

The devices provide a USB connection with a built-in USB-to-RS232 chip. They are automatically recognized as serial ports by the operating system, and no additional software is required.


Connection
-----------------------

Since the devices are identified as COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import ElektroAutomatik
    >> src = ElektroAutomatik.PS2000B("COM3")
    >> src.close()


Operation
-----------------------

The operation of this gauge is fairly straightforward, but there is a couple of points to keep in mind:

    - The source can operate in the manual or in the remote mode. In the manual mode the device is controlled using the front panel, but the values can still be read out. In the remote mode the outputs are controlled from the PC, and the front panel controls are disabled. Upon creation one can specify the remote mode handling for the device: either ``"manual"`` (it has to be enabled or disabled explicitly, and disabled by default) or ``"force"`` (remote mode is enabled upon connection and disabled upon disconnection).