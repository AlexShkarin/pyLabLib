.. _sensors_thorlabs:


.. note::
    General sensor communication concepts are described on the corresponding :ref:`page <basic_sensors_basics>`

Thorlabs PM100/PM160 series power meters
========================================

Thorlabs produces several different models of power and energy meters with different controllers and measurement heads, but relatively similar interfaces. The class has been tested with PM160 standalone power VegaPowerMeter.

The main device class :class:`pylablib.devices.Thorlabs.PM160<.Thorlabs.misc.PM160>`.


Software requirements
-----------------------

The drivers for USB devices are provided in the `Thorlabs Optical Power Monitor software <https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=OPM>`__ software. PyLabLib uses NI VISA communication interface to communicate with this device. Hence, it also requires NI VISA Runtime, which is freely available from the `National Instruments website <https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html>`__. Finally, to make the devices run with VISA interface, you need to run Power Meter Driver Switcher (comes with the Optical Power Monitor software) and switch all the desired power meters to PM100D mode (it is called PM100D even for other power meters such as PM160).

Devices with pure RS232 interface do not require Thorlabs software, and only need an appropriate USB-to-RS232 adapter with its own drivers.

.. Devices with bluetooth connection can be used on Windows via a bluetooth COM port. For that you need to go ``Bluetooth and other devices settings``, open ``More Bluetooth options`` (in the panel on the right side) and at the ``COM Ports`` tab click on the ``Add...`` button. There make sure that ``Incoming`` option is selected, and click ``OK``. This will add a COM port to your PC, whose name is shown in the list. After that you simply need to pair and connect your PC to the power meter. To check if the connection was successful, you can go to the ``COM Ports`` tab again and make sure that the COM port there now has an associated name corresponding to your power meter (e.g., ``PM160 400000``).

Devices with bluetooth connection can be used on Windows via a bluetooth COM port. For that, first you need co connect the power meter to your PC by making sure it is active (i.e., the display is lit up), and then adding a new bluetooth device in ``Bluetooth and other devices settings`` (the power meter should show up in the list of discovered devices). After that, you need to open ``More Bluetooth options`` (in the panel on the right side) and navigate to the ``COM Ports`` tab. There should already be several COM ports in the list corresponding to the added power meter. You are interested in the one marked with ``Outgoing`` direction, with the name containing ``'SPP'`` (e.g., ``Thorlabs PM160 400000 'SPP'``). The corresponding COM port (e.g., ``COM5``) is the one you need to use for communication.

Connection
-----------------------

Depending on the protocol used (VISA or RS232/bluetooth), you will need to supply either a VISA name (e.g., ``"USB0::0x1313::0x807B::400000::INSTR"``) or a COM port name (e.g., ``"COM5"``), potentially with the baud rate if it is different from the standard 115200 baud (e.g., ``("COM5", 19200)``; only applies to RS232 devices, not bluetooth)::

    >> from pylablib.devices import Thorlabs
    >> meter1 = Thorlabs.PM160("USB0::0x1313::0x807B::400000::INSTR")  # USB connection uses VISA interface
    >> meter2 = Thorlabs.PM160("COM3")  # bluetooth connection uses a COM port
    >> meter1.close()
    >> meter2.close()


Operation
-----------------------

The operation of the power meter is fairly straightforward, but there is a couple of points to keep in mind:

    - Bluetooth communication tends to go to a sleep mode after about a second of inactivity (i.e., lack of communication with the PC). When in this mode, it takes about a second for the device to reply to the first command, after which it switches in the active mode and replies significantly fast (about 20ms per command) until it goes back into the sleep mode. Hence, to keep the device responsive, it is important to poll it at least 2-3 times a second (e.g., using method :meth:`.PM160.get_reading` with ``measure=False``, which immediately returns the currently displayed value).