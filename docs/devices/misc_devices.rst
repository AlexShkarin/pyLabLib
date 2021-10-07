.. _misc_devices:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

Miscellaneous devices
==============================

There are several miscellaneous device classes, which are collected in this page. All of them implement straightforward serial communication protocol, so the software requirements and the connection approach is the same for all of them.


Software requirements
-----------------------

All the devices provide either a bare RS232 interface, or a USB connection with a built-in USB-to-RS232 chip. In either way, they are automatically recognized as serial ports, and no additional software is required.


Connection
-----------------------

The devices are identified as COM ports, so they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import Conrad
    >> dev = Conrad.RelayBoard("COM5")
    >> dev.close()

Operation
-----------------------

.. _misc_devices_conrad_relay:

Conrad relay board
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a board, which has several externally-controlled relays.

The class is proved as :class:`pylablib.devices.Conrad.RelayBoard<.Conrad.base.RelayBoard>`. It simply lets the user query and set the relay states. It also in principle supports communication with several daisy-chained boards, but it has never been tested.


.. _misc_devices_arduino:

Generic Arduino class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The class is proved as :class:`pylablib.devices.Arduino.IArduinoDevice<.Arduino.base.IArduinoDevice>`. It implements basic serial communication; the exact command protocol depends on the particular Arduino software written and uploaded by the user.

The main difference from directly using a serial backend is in handling of DTR line, which signal reset to the Arduino board. Unlike the standard backend, connection will not restart the board; instead, there is an explicit :meth:`.IArduinoDevice.reset_board` which pulses the DTR line to reset the board.