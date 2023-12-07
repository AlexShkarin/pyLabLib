.. _lasers_hubner:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

Hubner Cobolt laser
=======================

Cobolt is a series of diode and diode-pumped lasers produces by Hubner Photonics. They might have several connection options (e.g., USB or direct serial RS232), but they implement the same command protocol and can be used interchangeably. The code has been tested with Cobolt 06-01 series laser using a USB connection,

The main laser class is :class:`pylablib.devices.Hubner.Cobolt<.Cobolt.Cobolt>`.

Software requirements
-----------------------

When using a bare RS232 interface, any appropriate USB-to-RS232 adapter should work. When using a USB connection, one might need to install manufacturer-provided drivers. In any case, the device will be identified by the OS as a serial port.


Connection
-----------------------

Since the devices are identified as COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import Hubner
    >> laser = Hubner.Cobolt("COM5")
    >> laser.close()

Operation
------------------------

The method names are pretty self-explanatory. The device typically lets one enable or disable the output, query key switch and interlock status, set up the operation mode (constant power/current, modulation, etc.), set up output power or current, and query some statistics (temperatures, operation hours, LED states). Note that, depending on the model, not all methods are supported.