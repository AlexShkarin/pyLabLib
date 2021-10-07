.. _stages_newport_picomotor:

.. note::
    General stage communication concepts are described on the corresponding :ref:`page <stages_basics>`

Newport Picomotor controller
==============================

Newport Picomotor is a series of actuators, usually in a screw format, based on the slip-stick piezo actuation mechanism (similar to, e.g., Attocubes). Operating them requires a driver/controller to output specific voltage pulses. The basic modern open-loop controller is Newport 8742, which can drive up to 4 actuators (but only one at a time), supports connection via USB or Ethernet, and can be daisy-chained to communicate with several controllers through one connection. The class has been tested with this controller and a single standard actuator.

The device class is :class:`pylablib.devices.Newport.Picomotor8742<.picomotor.Picomotor8742>`.


Software requirements
-----------------------

The controller has two communication modes: USB, and Ethernet. USB mode requires a driver supplied with the freely available `PicomotorApp software <https://www.newport.com/p/8742-4-KIT>`__, while Ethernet connection works like any other networks device and does not require any additional software. The controller has been tested both with USB and Ethernet communication modes.


Connection
-----------------------

When using the USB connection, the device is identified by its index, starting from 0. To get the number of connected devices, you can use :func:`Newport.get_usb_devices_number_picomotor<.picomotor.get_usb_devices_number>`::

    >> from pylablib.devices import Newport
    >> Newport.get_usb_devices_number_picomotor()
    2
    >> stage1 = Newport.Picomotor8742()
    >> stage2 = Newport.Picomotor8742(1)
    >> stage1.close()
    >> stage2.close()

Ethernet connection requires a host name or an IP address. Both can be set up by first connecting the device via USB or by using the PicomotorApp software (in the ``Setup -> Ethernet`` menu). After that, they can be supplied to the class instead of index::

    >> from pylablib.devices import Newport
    >> stage1 = Newport.Picomotor8742("8742-12345")  # by default, all host names start with 8742
    >> stage1.close()


Operation
-----------------------

This controller has several features and differences compared to most other stages and sliders:

    - The controller is inherently multi-axis, hence it always take the axis as the first argument. The axes are labeled numerically starting from 1 (i.e., 1, 2, 3, and 4). The list of all axes is related to the exact controller, an can be obtained using :meth:`.Picomotor8742.get_all_axes`.
    - There is an option to auto-detect motors and their kind using :meth:`.Picomotor8742.autodetect_motors` method. However, since it involves stepping the motor, it usually makes more sense to detect them once and then store them into the non-volatile (i.e., power-independent) memory using :meth:`.Picomotor8742.save_parameters`.
    - Even open-loop controllers support absolute positioning, which is achieved simply by counting steps in both directions. However, unlike stepper motors or encoders, these steps can be different depending on the direction, position, instantaneous load, speed, etc. Hence, the absolute positions quickly become unreliable. It is, therefore, recommended to generally use relative positioning using :meth:`.Picomotor8742.move_by` method.
    - As mentioned above, the controller support daisy-chaining using RS-485 connections. It allows to connect several controllers together while still only using a single PC connection. In this case, it is recommended to supply ``multiaddr=True`` upon connecting to the device. If, in addition ``scan=True`` is set (default), then upon connection the controller scans for all other connected devices, resolves their address conflicts, and builds the list of the available addresses (address is a number between 1 and 31). The list can later be read using :meth:`.Picomotor8742.get_addr_map`, and the network rescanned using :meth:`.Picomotor8742.scan_devices`. To refer to a specific device, its address should be specified using ``addr`` parameter of a method; by default it is set to ``None``, which selects the device connected to the PC.