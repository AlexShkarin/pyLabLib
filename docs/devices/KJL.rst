.. _sensors_kjl:

.. note::
    Basic sensors communication concepts are described on the corresponding :ref:`page <basic_sensors_basics>`

Kurt J. Lesker pressure gauges
==============================

KJL manufactures a range of pressure gauges and controllers with several different standards and communication protocols. The code has been tested with KJL300 pressure gauge using its built-in RS232 connection.

The main device classes are :class:`pylablib.devices.KJL.KJL300<.KJL.base.KJL300>`.


Software requirements
-----------------------

The devices provide a bare RS232 interface, so any appropriate USB-to-RS232 adapter should work.


Connection
-----------------------

Since the devices are identified as COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import KJL
    >> gauge = KJL.KJL300("COM5")
    >> gauge.close()


Operation
-----------------------

KJL300
~~~~~~~~~~~~~~~~~~~~~~~

The operation of this gauge is fairly straightforward, but there is a couple of points to keep in mind:

    - Even standard RS232 operation requires specifying the device RS485 address. IT can be specified using ``addr`` parameter on creation. By default, the class assumes the factory default of 1, but if it is ever changed on the device, it needs to be specified correctly.
    - By default, the pressure is always returned and set in Pa regardless of the display units.