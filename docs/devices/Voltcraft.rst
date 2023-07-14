.. _voltcraft:


Voltcraft produces different basic measurement and electronic devices including multimeters, oscilloscopes, signal generators, power supplies, and environment sensors.

.. _voltcraft_multimeter:

Voltcraft multimeters
==============================

.. note::
    Basic sensors communication concepts are described on the corresponding :ref:`page <basic_sensors_basics>`

There are different series of multimeters with somewhat different capabilities and fairly different communication methods and protocols. There are currently two different supported protocols. The firs has been designed with Voltcraft VC-7055BT multimeter, but it might also be able to work with other 7000 series multimeters such as 7060 and 7200. The second was designed with VC880, but might also work with VC650T.

The main device classes are :class:`pylablib.devices.Voltcraft.VC7055<.Voltcraft.multimeter.VC7055>` and :class:`pylablib.devices.Voltcraft.VC880<.Voltcraft.multimeter.VC880>`.


Software requirements
-----------------------

VC7055 multimeters provides a bare RS232 interface, so any appropriate USB-to-RS232 adapter should work. VC880 multimeters show up as a standard HID device and are automatically supported by Windows.


Connection
-----------------------

VC7055 devices are identified as COM ports, so use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import Voltcraft
    >> meter = Voltcraft.VC7055("COM1")
    >> meter.close()

VC880 devices are identified either via their HID path (a fairly long and complicated string of symbols such as ``\\?\hid#vid_10c4&pid_ea80#7&0000000&1&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}``), and they can be identified either using this string, or an integer index (Starting from 0) which selects one of the potentially suitable devices in the system::

    >> from pylablib.devices import Voltcraft
    >> meter1 = Voltcraft.VC880()  # try to connect to the first available multimeter
    >> meter2 = Voltcraft.VC880(idx=1)  # try to connect to the second available multimeter
    >> meter1.close()
    >> meter2.close()


Operation
-----------------------

The operation of this multimeter is fairly straightforward, but there is a couple of points to keep in mind:

    - The documentation from VC7055 multimeter does not always correctly reflect the communication protocol, and the device behavior is sometimes strange (e.g., it return non-ASCII symbols or strange replies to commands). The communication protocol is implemented as observed in reality, not as documented. Therefore, it is not guaranteed, that the provided code will work with related models, such as other 7000-series multimeters, or even with different revisions of the same model.
    - Keep in mind that VC880 should be manually activated for PC communication by pressing ``PC`` button on the front panel, and this needs to be done every time the device is turned on. Otherwise it is detected by the OS and can be connected to, but it will not send updates or react to commands.