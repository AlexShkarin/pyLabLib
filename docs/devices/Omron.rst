.. _misc_omron:

.. note::
    Basic Modbus protocol concepts are described on the corresponding :ref:`page <protocols_modbus>`

Omron automation electronics
==============================

Omron manufactures a range of automation electronics (sensors, relays, controllers, etc.), which frequently can be remotely controlled using Modbus protocol. In addition to the :ref:`generic Modbus control <protocols_modbus>`, pylablib implements E5_C (e.g., E5GC) temperature controller in a bit more detail. The code has been tested with E5GC-QX1A6M-015 controller and generic USB to RS485 converter.

The main device classes are :class:`pylablib.devices.Omron.OmronE5xCController<.Omron.base.OmronE5xCController>`.


Software requirements
-----------------------

Basic Omron devices implement Modbus protocol over RS485 physical layer. If one uses a dedicated USB to RS485 controller or a USB to RS232 controller with RS232 to RS485 adapter, then it shows up as a serial port in the OS, and no additional software is required.


Connection
-----------------------

Generally, you would need to know a serial port of the RS485 controller, the serial connection parameters (by default it's 9600 baud, 8 data bits, even parity bit, one stop bit) and the controller Modbus address (1 by default). For details, see :ref:`Modbus protocol description <protocols_modbus>`.


Operation
-----------------------

.. _misc_omron_E5xC:

E5_C
~~~~~~~~~~~~~~~~~~~~~~~

There are two sets of methods implemented. The first are the generic methods for getting and setting values of internal registers: :meth:`.OmronE5xCController.get_reg` and :meth:`.OmronE5xCController.set_reg`. These allow full control over the device. The description of the registers is given in the controller communication manual (``Communications Data for Modbus`` section).

The second set of methods provides the basic temperature readout, as well as the setpoint control. Currently only the most basic methods for getting the current temperature (:meth:`.OmronE5xCController.get_measurementi`) and controlling the setpoint (:meth:`.OmronE5xCController.get_setpointi` and :meth:`.OmronE5xCController.set_setpointi`) are implemented