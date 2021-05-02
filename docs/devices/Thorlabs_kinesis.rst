.. _stages_thorlabs_kinesis:

.. note::
    General stage communication concepts are described on the corresponding :ref:`page <stages>`

Thorlabs APT/Kinesis devices
==============================

Thorlabs has a variety of APT/Kinesis devices for various motion-related functionality (mostly motor controllers and piezo drivers), which share the same API. The library uses an older and more low-level APT protocol to communicate with these devices. So far it has been only implemented for motor controllers and some :ref:`specialized devices <misc_thorlabs>` and tested with KDC101 and K10CR1 controllers.

The main device classes are :class:`pylablib.devices.Thorlabs.BasicKinesisDevice<.kinesis.BasicKinesisDevice>` for a generic Kinesis/APT devices and :class:`pylablib.devices.Thorlabs.KinesisMotor<.kinesis.KinesisMotor>` aimed at motor controllers such as K10CR1 or KDC101.


Software requirements
-----------------------

The connection is done using Thorlabs APT protocol, so it need the corresponding APT `drivers <https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=1>`__. Pylablib communicates directly with the FTDI USB-to-RS232 using `pyft232 <https://github.com/lsgunth/pyft232>`__ chip inside the controller, so it bypasses most of the Thorlabs software. This means that it does not need any Thorlabs-supplied DLLs, but it also means that it can not work with the simulated devices (they are simulated on a level above the direct serial communication).


Connection
-----------------------

The devices are identified by their address, which correspond to their serial numbers. To get the list of all the connected devices, you can use :func:`Thorlabs.list_kinesis_devices<.kinesis.list_kinesis_devices>`::

    >> from pylablib.devices import Thorlabs
    >> Thorlabs.list_kinesis_devices()
    [('27500001', 'Kinesis K-Cube  DC Driver')]
    >> stage = Thorlabs.KinesisMotor("27500001")
    >> stage.close()


Operation
-----------------------

This controller has several features and differences compared to most other stages and sliders:

    - There are several different ways to specify the stage calibration, which are controlled by the ``scale`` parameter supplied upon the connection. By default (``scale = "step"``), it accepts and returns position in motor steps, velocity in steps/s and acceleration in steps/s^2 (scaling coefficients for the latter two are determined from the controller model). If ``scale = "stage"``, the class attempts to autodetect the stage and use meters or degrees instead of steps; in addition you can supply the stage name (e.g., ``"MTS25-Z8"``) as a scale instead of relying on the autodetection. If there is not calibration for the stage you have, you can supply a single number which specifies number of steps per unit (e.g., for ``"MTS25-Z8"`` stage and mm units, one would supply ``scale = 34304``). The stage scaling can be obtained from the `APT <https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=1>`__ manual. Finally, one can supply a 3-tuple of scales for position, velocity and acceleration (all relative to the internal units). The details are given in the APT manual. To ensure that the units have been applied and/or autodetected correctly, you can use :meth:`.KinesisMotor.get_scale`, :meth:`.KinesisMotor.get_scale_units` and :meth:`.KinesisMotor.get_stage` methods.
    - By default, the controllers are treated as single-axis. If several axes are supported, they can be specified using ``channel`` argument.
    - The motor power-up parameters for homing, jogging, limit switches, etc., can be different from the parameters showing up in the APT/Kinesis controller. This can lead to problems if, e.g., homing speed is too low, so the motor appears stationary while homing. You should make sure to check those parameters using :meth:`.KinesisMotor.get_velocity_parameters`, :meth:`.KinesisMotor.get_jog_parameters`, :meth:`.KinesisMotor.get_homing_parameters`, :meth:`.KinesisMotor.get_gen_move_parameters`, and :meth:`.KinesisMotor.get_limit_switch_parameters`.