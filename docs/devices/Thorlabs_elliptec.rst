.. _stages_thorlabs_elliptec:

.. note::
    General stage communication concepts are described on the corresponding :ref:`page <stages_basics>`

Thorlabs Elliptec devices
==============================

Thorlabs has a line of basic resonant piezoelectric motor stages from Elliptec, which include several rotational and linear stages and feature step-motion and position readout. The library has been tested with ELL18 and ELL14 rotational mounts.

The main device class is :class:`pylablib.devices.Thorlabs.ElliptecMotor<.elliptec.ElliptecMotor>`.


Software requirements
-----------------------

The connection is done using a USB connection together with a built-in USB-to-RS232 chip. It is automatically recognized as a serial port, and no additional software is required. In case the device is not recognized as a serial port, you can fix it by installing freely available `Thorlabs Elliptec software <https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=ELL>`__.


Connection
-----------------------

Since the devices are identified as COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import Thorlabs
    >> stage = Thorlabs.ElliptecMotor("COM5")
    >> stage.close()


Operation
-----------------------

These devices have several features and differences compared to most other stages and sliders:

    - There is a possibility to have several (up to 16) devices connected to the same controller board (i.e., the same serial port address) using bus distributor. However, since they all use the same serial port, they are all controlled from a single :class:`.ElliptecMotor` instance. Hence, in order to refer to specific devices, each communication requires an address (integer from 0 to 15), which is specified by ``addr`` argument available in almost all methods. When this argument is ``None`` (which is the default value), the so-called default address is used, which can be accessed via :meth:`.ElliptecMotor.get_default_addr` and :meth:`.ElliptecMotor.set_default_addr` methods. By default, all connected devices are discovered up the connection, and the first available devices is used as default; therefore, if only a single devices is connected, ``addr`` argument does not have to be used.
    - Compared to most motor controllers, Elliptec devices have some limitation related to their inability to communicate while the motor is moving. Therefore, there are no methods to query whether the motor is moving, or stop the motion once initiated. To address that and to simplify the library and the user code, all motion-related methods (:meth:`.ElliptecMotor.move_to`, :meth:`.ElliptecMotor.move_by`, and :meth:`.ElliptecMotor.home`) are made synchronous, i.e., the execution is paused until the motion is complete. Note that this is true even when several devices are connected to the same port.
    - There are several different ways to specify the stage calibration, which are controlled by the ``scale`` parameter supplied upon the connection. By default (``scale = "stage"``), the internal device calibration is used, so all of the positions are expressed in device-specific units (deg or mm). If ``scale = "step"``, all of the position are specified in internal device steps instead. Finally, if ``scale`` is a number, it is the proportionality coefficient between the position units and the internal steps, i.e., the position in user-defined units is multiplied by it to specify the position in steps. The scale for individually addressed devices can be set using :meth:`.ElliptecMotor.get_scale` and :meth:`.ElliptecMotor.set_scale` methods.