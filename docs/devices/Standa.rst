.. _stages_standa:

.. note::
    General stage communication concepts are described on the corresponding :ref:`page <stages_basics>`

Standa motorized stages
==============================

Standa produces a variety of motorized stages and positions, which are generally controlled by a single controller model 8SCM4 (older version) or 8SMC5 (newer version).

The main device class are :class:`pylablib.devices.Standa.Standa8SMC<.Standa.base.Standa8SMC>`. The code has been tested with 8SMC4-USB single-axis controller and 8MT167-25 stepper motor stage.


Software requirements
-----------------------

The controllers have a built-in USB-to-RS232 adapter, which is automatically recognized as a serial port by the OS, so no additional software is required.

Connection
-----------------------

Since the devices are identified as COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import Standa
    >> stage = Standa.Standa8SMC("COM3")
    >> stage.close()


Operation
-----------------------

This controller has several features and differences compared to most other stages and sliders:

    - The controllers provide a large set of methods for checking and adjusting various motion parameters, controlling different accessories, etc. So far only a basic subset of these commands is implemented, which allows one to start and stop the motion, home the stage, set up basic velocity parameters, and query the status. If you need advanced functionality, you can examine the list of commands in the `documentation <https://doc.xisupport.com/en/8smc4-usb/8SMCn-USB/Programming/Communication_protocol_specification.html#all-controller-commands>`__ and implement them in your code using :meth:`.Standa8SMC.query` method.
    - All commands dealing with distances (e.g., moving, getting position, velocity, etc.) use internal units. For DC motors these are steps (derived from the rotational encoder), while for stepper motors these are microsteps, whose resolution can be found using :meth:`.Standa8SMC.get_stepper_motor_calibration`. This means that, e.g., given a stepper motor with 200 steps per revolution and 256 microsteps per step, one can rotate it by a full turn (before taking a possible gearbox into account) by calling ``stage.move_by(200*256)``.
    - Some stages can come with a built-in linear encoder. In this case, the position can be accessed both using :meth:`.Standa8SMC.get_position` method like for all other stages, and using :meth:`.Standa8SMC.get_encoder` method. If there is not linear encoder, :meth:`.Standa8SMC.get_encoder` will return zero.