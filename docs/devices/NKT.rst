.. _lasers_nkt:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

NKT lasers
=======================

NKT Photonics produces a variety of light sources (predominantly fiber-coupled lasers), which are frequently arranges as multi-stage modular systems. These systems consist of individual modules, which can be controlled via the main module using the common Interbus connection. The main laser class is :class:`pylablib.devices.NKT.GenericInterbusDevice<.NKT.interbus.GenericInterbusDevice>` for a generic Interbus-connected system. The code has been tested with SuperK EXTREME white light laser equipped with SuperK SELECT tunable filter.

Software requirements
-----------------------

The controllers have a built-in USB-to-RS232 adapter, which is automatically recognized as a serial port by the OS, so no additional software is required. If the device is not recognized, the drivers can be obtained from the `manufacturer website <https://www.nktphotonics.com/support/>`__.


Connection
-----------------------

The whole Interbus system is identified as a COM port, so it uses the standard :ref:`connection method <devices_connection>`, and all you need to know is its COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import NKT
    >> laser = NKT.GenericInterbusDevice("COM3")
    >> laser.close()

Within each Interbus system, there is a set of modules which can be accessed individually using their address (a number between 1 and 48). To automatically detect all available modules, you can use :meth:`.GenericInterbusDevice.ib_scan_devices`. Note that it typically takes relatively long time (about 25s for the full scan), so you should generally only do it when you change the Interbus arrangement by connecting or disconnecting devices or changing their addresses.

To identify, which address corresponds to which device, there are several methods. First, you can use the returned device type (also an integer between 0 and 255). You can look up the types in the SDK manual, which is freely available on the `manufacturer website <https://www.nktphotonics.com/support/>`__ (you need to download ``SDK`` zip file, inside which ``SDK Instruction manual.pdf`` provides the necessary information). In addition, some devices either have standard addresses (e.g., Koheras BasiK K80-1 has address 10 and type 33, while SuperK EXTREME has address 15 and type 96), or allow for setting their address using switches (e.g., SuperK SELECT).

Operation
------------------------

All of the device control is done by querying and setting values of internal registers. Similar to modules themselves, registers within each module are also identified by their numerical addresses. The list of the device registers and their meaning is provided in the same SDK file as mentioned above. To access the registers, you can use :meth:`.GenericInterbusDevice.ib_get_reg` and :meth:`.GenericInterbusDevice.ib_set_reg` methods. By default these methods work with raw binary values, but you can provide the register kind (e.g., ``"i16"`` or ``"u8"``) to these methods. You can learn the kind of the registers and their precise meaning from the register files, which are available after installing the SDK. These files are located in the ``Register Files`` folder within the SDK, and their names correspond to the device kind in hex (e.g., the file corresponding to Koheras BasiK K80-1 will be name ``21.txt``). Given this information, you can control your system. For example, the following code connects to the SuperK EXTREME module, queries its inlet temperature, sets the power setpoint and turns on the emission::

    from pylablib.devices import NKT
    laser = NKT.GenericInterbusDevice("COM3")
    print(laser.ib_get_reg(15,0x11,"i16")/10)  # the register is temperature in 0.1C
    laser.ib_set_reg(15,0x37,600,"u16")  # set power to 60% (the register is power level in 0.1%)
    laser.ib_set_reg(15,0x30,3,"u8")  # turn on the output (3 for on, 0 for off)