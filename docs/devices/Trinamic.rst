.. _stages_trinamic:

.. note::
    General stage communication concepts are described on the corresponding :ref:`page <stages_basics>`

Trinamic TMCM-x110 controller
==============================

TMCM-x110 are universal stepper motor controller from Trinamic (currently Analog Devices), which include single-axis TMCM-1110 and multi-axis TMCM-3110 and TMCM-6110. It provides multiple connection options, but so far has only been tested with USB connection.

The main device classes are :class:`pylablib.devices.Trinamic.TMCMx110<.Trinamic.base.TMCMx110>` for multi-axis devices and :class:`pylablib.devices.Trinamic.TMCM1110<.Trinamic.base.TMCM1110>` for a single-axis TMCM-1110 (``TMCMx110`` can also be used with TMCM-1110, but many of the device variable will be dictionaries ``{axis: value}`` instead of single values).


Software requirements
-----------------------

USB connection needs drivers, which are supplied with the freely-available `TMCL-IDE <https://www.analog.com/en/resources/evaluation-hardware-and-software/motor-motion-control-software/tmcl-ide.html#latest>`__. With those drivers installed (and even frequently already without them), the controllers show up as virtual COM ports. Note that when several devices are connected, they sometimes get assigned conflicting (i.e., overlapping) COM ports. In this case, you might need to manually reassign these in the Device Manager.


Connection
-----------------------

Since the devices are identified as virtual COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import Trinamic
    >> stage1 = Trinamic.TMCMx110("COM5")
    >> stage2 = Trinamic.TMCM1110("COM8")
    >> stage1.close()
    >> stage2.close()


Operation
-----------------------

This controller has several features and differences compared to most other stages and sliders:

    - The controller allows one to control the number of microsteps per step using :meth:`.TMCM1110.get_microstep_resolution` and :meth:`.TMCM1110.set_microstep_resolution`. Hence, the calibration of the real position to the controller readout position depends on this resolution. Furthermore, changing this resolution does not affect the step counter, meaning that changing it, performing a move, and changing it back will result in a different position. Hence, it is not recommended to change it after homing or referencing the position.
    - Similarly, the controller has variable frequency divisors, which control the ratio between internal and real units for the velocity and the acceleration. They are set up together with the maximal velocity and acceleration using :meth:`.TMCM1110.setup_velocity` and :meth:`.TMCM1110.get_velocity_parameters`, and the conversion factors can be obtained using :meth:`.TMCM1110.get_acceleration_factor` and :meth:`.TMCM1110.get_velocity_factor`.
    - The device has an option of controlling maximal output current using :meth:`.TMCM1110.setup_current` and :meth:`.TMCM1110.get_current_parameters`. Change them carefully, since the values which are too large can damage the motor. Also take into account, that the currents are defined relative to the maximal output current, which is controlled using the physical jumper on the board (on TMCM-1110).
    - The only real difference between :class:`pylablib.devices.Trinamic.TMCMx110<.Trinamic.base.TMCMx110>` and :class:`pylablib.devices.Trinamic.TMCM1110<.Trinamic.base.TMCM1110>` is in how axis parameters are handled in device variables. In ``TMCM1110`` the values are turned as scalars, e.g., ``stage.dv["position"]`` can simply return ``1234``. In contrast, ``TMCMx110`` returns dictionary, so ``stage.dv["position"]`` will return ``{0: 1234}``.