.. _stages_thorlabs_kinesis:

.. note::
    General stage communication concepts are described on the corresponding :ref:`page <stages>`

Thorlabs APT/Kinesis devices
==============================

Thorlabs has a variety of APT/Kinesis devices for various motion-related functionality (mostly motor controllers and piezo drivers), which share the same API. The library uses an older and more low-level APT protocol to communicate with these devices. So far it has been only implemented for motor controllers and some :ref:`specialized devices <misc_thorlabs_optomechanics>` and tested with KDC101 and K10CR1 controllers.

The main device classes are :class:`pylablib.devices.Thorlabs.BasicKinesisDevice<.kinesis.BasicKinesisDevice>` for a generic Kinesis/APT devices and :class:`pylablib.devices.Thorlabs.KinesisMotor<.kinesis.KinesisMotor>` aimed at motor controllers such as K10CR1 or KDC101.


Software requirements
-----------------------

The connection is done using Thorlabs APT protocol, so it need the corresponding APT `drivers <https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=1>`__. Pylablib communicates directly with the FTDI USB-to-RS232 using `pyft232 <https://github.com/lsgunth/pyft232>`__ chip inside the controller, so it bypasses most of the Thorlabs software. This means that it does not need any Thorlabs-supplied DLLs, but it also means that it can not work with the simulated devices (they are simulated on a level above the direct serial communication).


Connection
-----------------------

The devices are identified by their address, which correspond to their serial numbers. To get the list of all the connected devices, you can use :func:`Thorlabs.list_kinesis_devices<.kinesis.list_kinesis_devices>`::

    >> from pylablib.devices import Thorlabs
    >> Thorlabs.list_kinesis_devices()
    **TODO**
    >> stage = Thorlabs.KinesisMotor("")
    >> stage.close()


Operation
-----------------------

This controller has several features and differences compared to most other stages and sliders:

    - There are several different ways to specify the stage calibration, which are controlled by the ``scale`` parameter supplied upon the connection. By default, it attempts to autodetect the motor and the connected stage and determine the scale in physical units (mm or degrees).