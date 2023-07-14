.. _stages_PI:

.. note::
    General stage communication concepts are described on the corresponding :ref:`page <stages_basics>`

Physik Instrumente (PI) controllers
===================================

Physik Instrumente produces a variety of piezo, servo, and slider controller. So far, only PI E-515 and PI E-516 are supported and tested via a standard serial connection.

The main device classes are :class:`pylablib.devices.PhysikInstrumente.PIE515<.PhysikInstrumente.base.PIE515>` and :class:`pylablib.devices.PhysikInstrumente.PIE516<.PhysikInstrumente.base.PIE516>`.


Software requirements
-----------------------

The devices provide a bare RS232 interface, so any appropriate USB-to-RS232 adapter should work. 

Note that these devices frequently require cross-cable (also called null-modem cable), in which connections between Rx and Tx lines are switched. In addition, one might need to activate RS-232 communication in the front panel menu, as otherwise the device would not respond.


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

These controllers has several features and differences compared to most other stages and sliders:

    - The controllers support either servo (position feedback) or direct voltage output modes, controlled with :meth:`.PIE516.enable_servo` method. In the servo mode they are more similar to a stage controller, and you can use, e.g., :meth:`.PIE516.move_to` and :meth:`.PIE516.stop` (only for E-516) methods. In the direct voltage mode you can use :meth:`.PIE516.set_voltage` to set the voltage directly.
    - The controllers only accepts commands from the PC when it is in the "online" (i.e., remote) mode, in which case external voltage controls are ignored. This mode is enabled automatically upon connection if ``auto_online=True`` is supplied upon creation (default), and can be connected via :meth:`.PIE516.enable_online` method. Note that in this case manual servo switches should be turned off, since otherwise the device is permanently in the servo mode.
    - PI E-515 bring additional complications due to its mechanism of switching between the manual and online modes:
  
      - First, the online mode is only accessible when the servo mode switches on the front panel are off. At the same time, even when online mode is not enabled (and the voltages/positions can not be controlled remotely), it is still possible to switch the servo mode on and off remotely, so one must be careful when calling :meth:`.PIE515.enable_servo`.
      - Second, when switching to the online mode, all of the voltages and positions are set to the last time they were updated (or zero, if they have not been changed since the device was turned on). It is possible to set the remote voltages to match the local ones before switching the modes, which is done automatically when ``safe=True`` is supplied to :meth:`.PIE515.enable_online`. The same can not be done for servo positions, since these can only be changed when the servo mode is on.
      - Finally, when the online mode is turned back off, the output voltages go back to the values set by manual knobs, which can be different from the current remote settings.

      As a result, one should expect and look out for sudden changes in the stage positions when switching between online and offline modes, and when switching the servo on and off.