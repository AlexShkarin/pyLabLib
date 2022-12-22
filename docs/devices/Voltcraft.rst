.. _voltcraft:


Voltcraft produces different basic measurement and electronic devices including multimeters, oscilloscopes, signal generators, power supplies, and environment sensors.

.. _voltcraft_multimeter:

Voltcraft multimeters
==============================

.. note::
    Basic sensors communication concepts are described on the corresponding :ref:`page <basic_sensors_basics>`

There are different series of multimeters with somewhat different capabilities and fairly different communication methods and protocols. The code has been tested with Volcraft VC-7055BT multimeter, but it might also be able to work with other 7000 series multimeters such as 7060 and 7200.

The main device class is :class:`pylablib.devices.Voltcraft.VC7055<.Voltcraft.multimeter.VC7055>`.


Software requirements
-----------------------

These multimeters provides a bare RS232 interface, so any appropriate USB-to-RS232 adapter should work.


Connection
-----------------------

Since the devices are identified as COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import Voltcraft
    >> meter = Voltcraft.VC7055("COM1")
    >> meter.close()



Operation
-----------------------

The operation of this multimeter is fairly straightforward, but there is a couple of points to keep in mind:

    - The documentation does not always correctly reflect the communication protocol, and the device behavior is sometimes strange (e.g., it return non-ASCII symbols or strange replies to commands). The communication protocol is implemented as observed in reality, not as documented. Therefore, it is not guaranteed, that the provided code will work with related models, such as other 7000-series multimeters, or even with different revisions of the same model.