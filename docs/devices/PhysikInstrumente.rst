.. _stages_PI:

.. note::
    General stage communication concepts are described on the corresponding :ref:`page <stages_basics>`

Physik Instrumente (PI) controllers
===================================

Physik Instrumente produces a variety of piezo, servo, and slider controller. So far, only PI E-516 is supported and tested via a standard serial connection.

The main device class is :class:`pylablib.devices.PhysikInstrumente.PIE516<.PhysikInstrumente.base.PIE516>`.


Software requirements
-----------------------

The devices provide a bare RS232 interface, so any appropriate USB-to-RS232 adapter should work.


Connection
-----------------------

Since the devices are identified as COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import PhysikInstrumente
    >> stage1 = PhysikInstrumente.PIE516("COM5")
    >> stage2 = PhysikInstrumente.PIE516("COM8")
    >> stage1.close()
    >> stage2.close()


Operation
-----------------------

This controller has several features and differences compared to most other stages and sliders:

    - The controller supports either servo (position feedback) or direct voltage output modes, controlled with :meth:`.PIE516.enable_servo` method. In the servo mode it is more similar to a stage controller, and you can use, e.g., :meth:`.PIE516.move_to` and :meth:`.PIE516.stop` methods. In the direct voltage mode you can use :meth:`.PIE516.set_voltage` to set the voltage directly.
    - The controller only accepts commands from the PC when it is in the "online" (i.e., remote) mode, in which case external voltage controls are ignored. This mode is enabled automatically upon connection if ``auto_online=True`` is supplied upon creation (default), and can be connected via :meth:`.PIE516.enable_online` method. Note that in this case manual servo switches should be turned off, since otherwise the device is permanently in the servo mode.