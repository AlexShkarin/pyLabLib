.. _stages_thorlabs_kinesis:

.. note::
    General stage communication concepts are described on the corresponding :ref:`page <stages_basics>`

Thorlabs APT/Kinesis devices
==============================

Thorlabs has a variety of APT/Kinesis devices for various motion-related functionality (mostly motor controllers and piezo drivers), which share the same API. The library uses an older and more low-level APT protocol to communicate with these devices. So far it has been only implemented for motor controllers and some :ref:`specialized devices <misc_thorlabs>` and tested with KDC101, KST101, K10CR1, and BSC201 motor controllers, KIM101 piezo motor controller, KPZ101 piezo output controller, and TPA101 quadrature sensor controller.

The main device classes are :class:`pylablib.devices.Thorlabs.BasicKinesisDevice<.kinesis.BasicKinesisDevice>` for a generic Kinesis/APT devices :class:`pylablib.devices.Thorlabs.KinesisMotor<.kinesis.KinesisMotor>` aimed at motor controllers such as K10CR1 or KDC101, :class:`pylablib.devices.Thorlabs.KinesisPiezoMotor<.kinesis.KinesisPiezoMotor>` for piezo drivers such as KIM and TIM, and :class:`pylablib.devices.Thorlabs.KinesisPiezoController<.kinesis.KinesisPiezoController>` for piezo controllers such as KPZ and TPZ.


Software requirements
-----------------------

The connection is done using Thorlabs APT protocol, so it needs the corresponding APT `drivers <https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=1>`__. Pylablib communicates directly with the FTDI USB-to-RS232 using `pyft232 <https://github.com/lsgunth/pyft232>`__ chip inside the controller, so it bypasses most of the Thorlabs software. This means that it does not need any Thorlabs-supplied DLLs, but it also means that it can not work with the simulated devices, since these are simulated on a level above the direct serial communication.

In some cases ``pyft232`` library can not find the required ``ftd2xx.dll`` library, which leads to an error. There are several ways to get around this. First, you can install the FTDI drivers from the `manufacturer's website <https://ftdichip.com/drivers/d2xx-drivers/>`__. Setup executable for Windows automatically places the necessary DLL into the ``System32`` folder, where ``pyft232`` can discover them. Alternatively, you can copy the DLLs there yourself from the Thorlabs APT installation. Their default location is ``Program Files\Thorlabs\APT\Drivers\APT\USB Driver\amd64`` for 64-bit version or ``Program Files\Thorlabs\APT\Drivers\APT\USB Driver\i386`` for 32-bit version. Note that in the first case the file is called ``ftd2xx64.dll``, and you will need to rename it to ``ftd2xx.dll`` when copying to the ``System32`` folder.


Connection
-----------------------

On Windows devices are identified by their address, which correspond to their serial numbers. To get the list of all the connected devices, you can use :func:`Thorlabs.list_kinesis_devices<.kinesis.list_kinesis_devices>`::

    >> from pylablib.devices import Thorlabs
    >> Thorlabs.list_kinesis_devices()
    [('27500001', 'Kinesis K-Cube  DC Driver')]
    >> stage = Thorlabs.KinesisMotor("27500001")
    >> stage.close()

On Linux they directly appear as virtual serial ports, e.g., ``/dev/ttyUSB0``. Hence, there you need to identify which device file corresponds your device (e.g., by unplugging and plugging it back in to see which device shows up). After that, you can use this name as the device address::

    >> from pylablib.devices import Thorlabs
    >> stage = Thorlabs.KinesisMotor("/dev/ttyUSB0")
    >> stage.close()

Note that on Linux :func:`Thorlabs.list_kinesis_devices<.kinesis.list_kinesis_devices>` will not produce a correct list, since it uses a different API. In the worst case, it can crash the process.

Operation
-----------------------

Standard motors
=======================

This controller has several features and differences compared to most other stages and sliders:

    - There are two different classes of devices which require slightly different communication approach: generic USB devices and rack-bay devices. These are hard to detect a priori, so by default generic USB device (which covers the majority of equipment) is assumed. If this assumption is incorrect, the communication becomes impossible, and an attempt to connect to the device raises a communication error ``ThorlabsBackendError: backend exception: 'read returned less data than expected' ('read returned less data than expected')``. If you experience this error, you should first power-cycle the device, as it often gets stuck in a non-communicable state, and then double-check that the standard Thorlabs software (Kinesis or APT) can detect and control it. If this is the case, you should supply ``is_rack_system=True`` to the controller::

        stage = Thorlabs.KinesisMotor("70000001", is_rack_system=True)

    - There are several different ways to specify the stage calibration, which are controlled by the ``scale`` parameter supplied upon the connection. By default (``scale = "step"``), it accepts and returns position in motor steps, velocity in steps/s and acceleration in steps/s^2 (scaling coefficients for the latter two are determined from the controller model). If ``scale = "stage"``, the class attempts to autodetect the stage and use meters or degrees instead of steps; in addition you can supply the stage name (e.g., ``"MTS25-Z8"``) as a scale instead of relying on the autodetection. If there is no calibration for the stage that you have, you can instead supply a single scaling factor, which specifies the number of steps per physical unit (e.g., for ``"MTS25-Z8"`` stage and mm units, one would supply ``scale = 34304``). The stage scaling can be obtained from the `APT <https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=1>`__ manual. Finally, one can supply a 3-tuple of scales for position, velocity and acceleration (all relative to the internal units). The details are given in the APT manual. To ensure that the units have been applied and/or autodetected correctly, you can use :meth:`.KinesisMotor.get_scale`, :meth:`.KinesisMotor.get_scale_units` and :meth:`.KinesisMotor.get_stage` methods.
    - By default, the controllers are treated as single-axis. If several axes are supported, they can be specified using ``channel`` argument in the corresponding methods such as ``move_to`` or ``get_status``. In addition, you can specify the number of channels using :meth:`.KinesisMotor.set_supported_channels` method, in which case settings ``channel="all"`` in the method would act on all the channels.
    - The motor power-up parameters for homing, jogging, limit switches, etc., can be different from the parameters showing up in the APT/Kinesis controller. This can lead to problems if, e.g., homing speed is too low, so the motor appears stationary while homing. You should make sure to check those parameters using :meth:`.KinesisMotor.get_velocity_parameters`, :meth:`.KinesisMotor.get_jog_parameters`, :meth:`.KinesisMotor.get_homing_parameters`, :meth:`.KinesisMotor.get_gen_move_parameters`, and :meth:`.KinesisMotor.get_limit_switch_parameters`.


Piezo motors
=======================

This controller has several features and differences compared to most other stages and sliders:

    - The controllers are treated as multi-axis. However, to be compatible with other Kinesis motor, the channel argument is not required, and it defaults to the currently selected "default" channel (1 in the beginning). To control different channels, you can either supply ``channel`` argument explicitly, or specify a different default channel using :meth:`.KinesisPiezoMotor.set_default_channel` or :meth:`.KinesisPiezoMotor.using_channel`.
    - The motor power-up parameters for jogging and drive can be different from the parameters showing up in the APT/Kinesis controller. This can lead to problems if, e.g., speed is too low. You should make sure to check those parameters using :meth:`.KinesisPiezoMotor.get_drive_parameters` and :meth:`.KinesisPiezoMotor.get_jog_parameters`.
    - Even open-loop controllers support absolute positioning, which is achieved simply by counting steps in both directions. However, unlike stepper motors or encoders, these steps can be different depending on the direction, position, instantaneous load, speed, etc. Hence, the absolute positions quickly become unreliable. It is, therefore, recommended to generally use relative positioning using :meth:`.KinesisPiezoMotor.move_by` method.


Piezo controllers
=======================

This controller acts more as a voltage amplifier than as a stage. Therefore, it does not have any motion-related commands (such as ``move_to``), and instead is mainly operated through :meth:`.KinesisPiezoController.enable_channel` and :meth:`.KinesisPiezoController.set_output_voltage` methods to control the output. In addition, it supports controlling the full output range (:meth:`.KinesisPiezoController.set_voltage_range`) and the voltage source (:meth:`.KinesisPiezoController.set_voltage_source`).


.. _stages_thorlabs_kinesis_quad:

Quadrature detector
=======================

These are fairly different from the other discussed devices, since they are more related to sensors than to motors. This controller takes signal from a quadrature photodetector and implements a PI control loop to feed back to some control device (e.g., a piezo driver or a galvo mirror). Hence, all of its methods are fairly distinct from the usual motors. Nevertheless, it is described here, since it still belongs to the APT/Kinesis family of devices and shares their detection and connection approach. The device is implemented in the :class:`pylablib.devices.Thorlabs.KinesisQuadDetector<.kinesis.KinesisQuadDetector>` class.

The operation is fairly straightforward: it implements control of PID parameters, output parameters (such as limits), operation mode (open/close loop), allows for reading current state and setting outputs in the open-loop mode.