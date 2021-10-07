.. _sensors_ophir:

.. note::
    General sensor communication concepts are described on the corresponding :ref:`page <basic_sensors_basics>`

Ophir power meters
==============================

Ophir produces a variety of power and energy meters with different controllers and measurement heads. The class has been tested with Ophir Vega controller with a photodiode head.

The main device classes are :class:`pylablib.devices.Ophir.OphirDevice<.Ophir.base.OphirDevice>` for a generic device and :class:`pylablib.devices.Ophir.VegaPowerMeter<.Ophir.base.VegaPowerMeter>` for Vega power meter.


Software requirements
-----------------------

The device provides a bare RS232 interface, so any appropriate USB-to-RS232 adapter should work.


Connection
-----------------------

Since the devices are identified as COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``) and the baudrate, if it is different from the standard one (9600 baud)::

    >> from pylablib.devices import Ophir
    >> meter1 = Ophir.VegaPowerMeter("COM5")  # default connection assumes 9600 baud
    >> meter2 = Ophir.VegaPowerMeter(("COM6", 19200))  # if the second power meter has a different baudrate
    >> meter1.close()
    >> meter2.close()


Operation
-----------------------

The operation of the power meter is fairly straightforward, but there is a couple of points to keep in mind:

    - On the Vega controller the results can be sent at most 15 times a second. However, they are not necessarily updated at this rate, so several consecutive request might yield the same result.
    - The device provides the way to change the communication baud rate. If the rate is changed, the device is automatically disconnected, and the new object needs to be instantiated with the updated baudrate.
    - The device might return ``"over"`` instead of the power reading on overexposure. To fix that, you can adjust the measurement range using :meth:`.VegaPowerMeter.set_range_idx`.