.. _stages_attocube:

.. note::
    General stage communication concepts are described on the corresponding :ref:`page <stages_basics>`

Attocube positioners
=======================

Attocube has two main positioner controllers: ANC300 and ANC350. These cover different but somewhat overlapping positioner classes, and have fairly different programming interfaces.


.. _stages_attocube_anc300:

Attocube ANC300
-----------------------

This controller is aimed at open-loop (i.e., no position readout) positioners. It is a chassis with a single PC communication module and up to 7 individual piezo control modules: ANM150 (only stepping), ANM200 (only scanning), or ANM250 (stepping and scanning).

The device class is :class:`pylablib.devices.Attocube.ANC300<.anc300.ANC300>`.


Software requirements
~~~~~~~~~~~~~~~~~~~~~~~

The controller has several communication modes: USB, RS232, and Ethernet. USB mode requires a driver supplied with the controller (or downloaded from the controller itself using its Ethernet connection and HTTP port), which makes ANC300 appear as a virtual COM port. RS232 requires a USB-to-RS232 adapter, which usually manifests in the same way. Finally, Ethernet connection works like any other networks device. The controller has been tested with USB and Ethernet communication modes (RS232 is identical to USB, so it should operate as well).

Of all of these modes only USB requires specialized drivers, and the other two are usually available purely through the built-in OS capabilities.


Connection
~~~~~~~~~~~~~~~~~~~~~~~

The device is identified by its communication address. It can be either a serial port (e.g., ``"COM5"``), or an IP address (e.g., ``"192.168.1.100"``); see :ref:`connection description <devices_connection>` for more information. The backend is chosen automatically based on the connection parameter. Additionally, Ethernet connection requires a password; by default, the standard Attocube password ``"123456"`` is used, but if you specified a custom password, you need to provide it upon connection::

    >> from pylablib.devices import Attocube
    >> atc1 = Attocube.ANC300("COM5")  # USB or RS232 connection
    >> atc2 = Attocube.ANC300("192.168.1.1", pwd="root")  # Ethernet connection; no need to provide a password, if it is default
    >> atc1.close()
    >> atc2.close()

Note that since Ethernet inherently supports multiple connections, it is possible to control the same devices in multiple scripts at the same time.


Operation
~~~~~~~~~~~~~~~~~~~~~~~~

This controller has several features and differences compared to most other stages and sliders:

    - The controller is inherently multi-axis, hence it always take the axis as the first argument. The axes are numbered starting from 1, and are addressed according to the chassis spaces, so some can be skipped or missing. To update the list of connected axes, use :meth:`.ANC300.update_available_axes` (called automatically on connection).
    - Different control modules provide different functionality. Hence, not all methods would work for all axes: offset voltage commands such as :meth:`.ANC300.set_offset` do not work with ANM150 module, while stepping commands such as :meth:`.ANC300.move_by` do not work with ANM200 module. To get the module kinds and serial numbers, use :meth:`.ANC300.get_axis_serial`.
    - The most important stepping parameters are step voltage amplitude and step frequency (number of steps per second). These can be controlled with, correspondingly, :meth:`.ANC300.get_voltage`/:meth:`.ANC300.set_voltage` and :meth:`.ANC300.get_frequency`/:meth:`.ANC300.set_frequency`.
    - Different axes can be enabled and disabled (i.e., connected or grounded) using :meth:`.ANC300.enable_axis` and :meth:`.ANC300.disable_axis`. Disabling an axis completely shuts off the connection to the positioner, which usually reduces the noise. In addition, there can be different operation modes for only offset, only stepping, or combination of the two.
    - It is possible to measure the positioner capacitance using :meth:`.ANC300.get_capacitance`, which is useful in identifying breaks or shorts in the wiring or faults in the piezos. By default, this method simply returns the last measured value. To re-measure, call it with ``measure=True``. Note that after the measurement is done, the axis is automatically disabled, and needs to be enabled explicitly::

        >> atc = ANC300("COM5")
        >> atc.get_capacitance(1, measure=True)  # get the capacitance (in F) on the first axis; the method waits until the measurement is done (about 1s)
        200E-9
        >> atc.is_enabled(1)
        False
    
      Note that this is also the only way to know if there is an actual positioner connected to the given control module.




.. _stages_attocube_anc350:

Attocube ANC350
-----------------------

This controller is aimed at closed-loop (i.e., with position readout) positioners. It can control up to 3 positioners.

The device class is :class:`pylablib.devices.Attocube.ANC350<.anc350.ANC350>`.


Software requirements
~~~~~~~~~~~~~~~~~~~~~~~

The controller has USB and Ethernet modes. USB mode requires a driver supplied with the controller. The communication is done via `PyUSB <https://pyusb.github.io/pyusb/>`__, which means that it does not require any additional Attocube DLLs, although you might need to install libusb (see `PyUSB <https://pyusb.github.io/pyusb/>`__ for more details). Ethernet control is supplied as an additional purchasable option and can be configured using the supplied Daisy control software.

This device has only been tested with a USB connection.


Connection
~~~~~~~~~~~~~~~~~~~~~~~

When using a USB connection, the device is identified by its index among all the connected ANC350 devices. To get the total number of devices, you can use :func:`Attocube.get_usb_devices_number_ANC350<.anc350.get_usb_devices_number>`::

    >> from pylablib.devices import Attocube
    >> Attocube.get_usb_devices_number_ANC350()
    2
    >> atc1 = Attocube.ANC350()  # use 0 index by default
    >> atc2 = Attocube.ANC350(1)
    >> atc1.close()
    >> atc2.close()

Ethernet connection should work in the same manner as any other similar devices, i.e., the address and, possibly, the port should be provided.


Operation
~~~~~~~~~~~~~~~~~~~~~~~~

This controller has several features and differences compared to most other stages and sliders:

    - The controller is inherently multi-axis, hence it always take the axis as the first argument. The axes are numbered 0 through 2. You can check if the slide is connected to the given axis using :meth:`.ANC350.is_connected`.
    - Different axes can be enabled and disabled (i.e., connected or grounded) using :meth:`.ANC300.enable_axis` and :meth:`.ANC300.disable_axis`. Disabling an axis completely shuts off the connection to the positioner, which usually reduces the noise.
    - It is also possible to control the sensor voltage using :meth:`.ANC350.get_sensor_voltage`/:meth:`.ANC350.set_sensor_voltage` methods. Reducing this voltage lowers the heating produced by the sensor, which becomes especially important at very low (<1K) temperatures.
    - The most important stepping parameters are step voltage amplitude and step frequency (number of steps per second). These can be controlled with, correspondingly, :meth:`.ANC350.get_voltage`/:meth:`.ANC350.set_voltage` and :meth:`.ANC350.get_frequency`/:meth:`.ANC350.set_frequency`.
    - It is possible to measure the positioner capacitance using :meth:`.ANC350.get_capacitance`, which is useful in identifying breaks or shorts in the wiring. By default, this method simply returns the last measured value. To re-measure, call it with ``measure=True``.
    - Fine positioning is performed using the position readout and the feedback loop. Then a ``move_to``/``move_by`` command is issued, this feedback loop is activated, and the positioner tries to reach and stay at the current position. You can use :meth:`.ANC350.is_target_reached` to check if the target is reached, :meth:`.ANC350.get_target_position` to get the target, and :meth:`.ANC350.get_precision`/:meth:`.ANC350.set_precision` to control the target precision.
    - In addition, there is a method :meth:`.ANC350.move_by_steps`, which mimics :meth:`.ANC300.move_by` by moving for a given number of steps instead of a given distance. However, due to implementation limitations, this method is synchronous, i.e., it waits until all steps are performed. Nevertheless, :meth:`.ANC350.jog` is still asynchronous.