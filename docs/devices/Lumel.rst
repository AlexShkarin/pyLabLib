.. _misc_lumel:

.. note::
    Basic Modbus protocol concepts are described on the corresponding :ref:`page <protocols_modbus>`

Lumel automation electronics
==============================

Lumel manufactures a range of automation electronics (sensors, relays, etc.), which frequently can be remotely controlled using Modbus protocol. In addition to the :ref:`generic Modbus control <protocols_modbus>`, pylablib implements RE72 temperature controller in a bit more detail. The code has been tested with RE72-122200E0 controller and generic USB to RS485 converter.

The main device classes are :class:`pylablib.devices.Lumel.LumelRE72Controller<.Lumel.base.LumelRE72Controller>`.


Software requirements
-----------------------

Basic Lumel devices implement Modbus protocol over RS485 physical layer. If one uses a dedicated USB to RS485 controller or a USB to RS232 controller with RS232 to RS485 adapter, then it shows up as a serial port in the OS, and no additional software is required.


Connection
-----------------------

Generally, you would need to know a serial port of the RS485 controller, the serial connection parameters (by default it's 9600 baud, 8 data bits, no parity bit, one stop bit) and the controller Modbus address (1 by default). For details, see :ref:`Modbus protocol description <protocols_modbus>`.


Operation
-----------------------

.. _misc_lumel_RE72:

RE72
~~~~~~~~~~~~~~~~~~~~~~~

There are two sets of methods implemented. The first are the generic methods for getting and setting values of internal registers: :meth:`.LumelRE72Controller.get_reg` and :meth:`.LumelRE72Controller.set_reg`. These allow full control over the device. The description of the registers is given in the user's manual (``RS-485 INTERFACE`` section).

The second set of methods provides the basic temperature readout, as well as the setpoint control. These are implemented in two varieties, floating point and integer, according to the two kinds of registers on the device. The integer methods (ending with ``i``, e.g., :meth:`.LumelRE72Controller.get_measurementi`) return integer value, whose interpretation depends on the measurement units and other parameters (e.g., for temperature this is the value in 1/10th of the current degree unit, C or F). The floating point methods return value in a more straightforward way (e.g., directly in degrees), but they do not allow for setting of the temperature setpoint.