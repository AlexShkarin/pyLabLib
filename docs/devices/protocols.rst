.. _protocols:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

Generic protocols
=======================

There exist generic mid-level communication protocols built on top of the existing communication channels. These are not specific to any particular device, but simply provide a level of abstraction to implement specific devices later.


.. _protocols_modbus:

Modbus
-----------------------

This is one of the standard industrial communication protocols. It has several different implementations depending on the underlying protocol (UART, TCP). Currently only Modbus RTU (binary protocol over UART) is supported.

The code is located in :mod:`pylablib.devices.Modbus`, and the main camera class is :class:`pylablib.devices.Modbus.GenericModbusRTUDevice<.modbus.GenericModbusRTUDevice>`.

Software requirements
~~~~~~~~~~~~~~~~~~~~~~~

The requirements depend on the underlying transfer layer. Most common is the RS485 physical layer, where one normally uses either a dedicated USB to RS485 controller, or a USB to RS232 controller with RS232 to RS485 adapter. In this case, the RS485 controller shows up as a serial port in the OS, and no additional software is required.

Connection
~~~~~~~~~~~~~~~~~~~~~~~

To successfully communicate with a device, several pieces of information are needed. First, one needs to know the serial port of the RS485 controller (e.g., ``"COM1"`` or ``"dev/ttyUSB0"``). Next are the serial port parameters, such as the baud rate, number of data bits, parity bits, and stop bits (the most common is 9600 baud with ``8N1`` format, i.e., 8 data bits, one parity bit, 1 stop bit). Finally, since several Modbus devices can be connected to the same controller, one needs to know the specific device address, which is an integer between 1 and 247. Both the serial port parameters and the device address are set at the device or specified in its documentation::

    >> from pylablib.devices import modbus
    >> dev = modbus.GenericModbusRTUDevice(("COM3", 19200), daddr=5)  # 19200 baud serial interface, default device address 5
    >> dev.close()

.. note::
    Serial ports are exclusive OS resources, which means that only one instance of :class:`.modbus.GenericModbusRTUDevice` can be opened at the same port, even if several devices are connected to the same RS485 controller. One can choose which device is addressed either by using ``daddr`` parameter in the methods, or by using :meth:`.GenericModbusRTUDevice.mb_set_default_address` method.
    

Operation
~~~~~~~~~~~~~~~~~~~~~~~~

The code implements the most basic Modbus methods for setting and reading coils, discrete inputs, and registers. All relevant methods are prefixed with ``mb_``, e.g., :meth:`.GenericModbusRTUDevice.mb_read_holding_registers` or :meth:`.GenericModbusRTUDevice.mb_write_single_coil`. In addition, it implements a basic device scanning method, which sends the same command to all possible addresses and notes which of them reply.