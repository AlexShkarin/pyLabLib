.. _stages_arcus_performax:

.. note::
    General stage communication concepts are described on the corresponding :ref:`page <stages_basics>`

Arcus Performax positioners
==============================

Arcus has several motor controllers and drivers, which are mainly different in their number of axes, communication possibilities, and driving function. They are also distributed under different names, e.g., Nippon Pulse America (NPA) or Newmark Systems. However, the models nomenclature is the same: there is 4EX for 4-axis controllers with USB and RS485 connection, 2EX/2ED for 2-axis controllers with USB and RS485 connections, and 4ET for 4-axis controllers with Ethernet connection. The class has been tested with 4EX and (partially) 2ED controllers with USB and RS-485 connectivity mode, but other controllers mentioned above should also work.

The main device classes are :class:`pylablib.devices.Arcus.Performax4EXStage<.performax.Performax4EXStage>` or 4-axis controllers, :class:`pylablib.devices.Arcus.Performax2EXStage<.performax.Performax2EXStage>` for 2-axis controllers, and :class:`pylablib.devices.Arcus.PerformaxDMXJSAStage<.performax.PerformaxDMXJSAStage>` for simple single-axis controller (DMX-J-SA). In addition to a different number of axes, they have several syntax differences, so one can not substitute for the other.

In addition, there is also a generic Performax stage class :class:`pylablib.devices.Arcus.GenericPerformaxStage<.performax.GenericPerformaxStage>`, which implements only the most basic functions: ASCII communication with the device and basic methods such as device name request. It can be used with new or not currently supported Arcus stages to directly control them using the ASCII control language (usually described in the stage manual).


Software requirements
-----------------------

The controller has several communication modes: USB, RS485, and Ethernet. USB mode requires a driver supplied with the operation software: `Arcus Drivers and Tools <https://www.arcus-technology.com/support/downloads/download-info/drivers-and-tools-installer/>`__, `Performax Series Installer <https://www.arcus-technology.com/support/downloads/download-info/performax-series-installer/>`__, and `Performax USB Setup <https://www.arcus-technology.com/support/downloads/download-info/performax-usb-setup/>`__ (all obtained at `Arcus website <https://www.arcus-technology.com/support/downloads/>`__). Installing all three seem to be sufficient. Once the appropriate USB drivers are installed, one can connect the device directly via its USB port and use the manufacturer DLLs ``PerformaxCom.dll`` and ``SiUSBXp.dll`` to communicate with the device. They can be obtained on the manufacturer's `website <https://www.arcus-technology.com/support/downloads/download-info/usb-64-bit-dll/>`__ and placed in the folder with the script, or in the ``System32`` Windows folder. If the DLL is located elsewhere, the path can be specified using the library parameter ``devices/dlls/arcus_performax``::

    import pylablib as pll
    pll.par["devices/dlls/arcus_performax"] = "path/to/dll"
    from pylablib.devices import Arcus
    stage = Arcus.Performax4EXStage()

.. warning::
    There appear to be some issues for USB-controlled devices with Python 3.6 which result in out-of-bounds write, memory corruption, and undefined behavior. Hence, Python 3.7+ is required to work with this device.

RS-485 connection does not require any device-specific drivers or DLLs, but it does need RS-485 controller connected to the PC. Such controllers usually show up as virtual COM ports, and they typically do not need any additional drivers.


Connection
-----------------------

When using the USB connection, the device is identified by its index, starting from 0. To get the list of all the connected devices, you can use :func:`Arcus.list_usb_performax_devices<.performax.list_usb_performax_devices>`::

    >> from pylablib.devices import Arcus
    >> Arcus.list_usb_performax_devices()
    [(0, '4ex01', 'Performax USB',
     '\\\\?\\usb#vid_1589&pid_a101#4ex01#{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}', '1589', 'a101'),
     (1, '4ex21', 'Performax USB',
     '\\\\?\\usb#vid_1589&pid_a101#4ex21#{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}', '1589', 'a101')]
    >> stage1 = Arcus.Performax4EXStage()
    >> stage2 = Arcus.Performax2EXStage(idx=1)
    >> stage1.close()
    >> stage2.close()

When using the RS-485 connection, you need to specify the serial port corresponding to your RS-485 connection and, possibly, its baud rate::
    
    stage = Arcus.Performax4EXStage(conn = "COM5")
    stage2 = Arcus.Performax4EXStage(conn = ("COM5",38400)) # specify a baud rate

The baud rate is 9600 by default, which is the standard value for the controllers. However, it can be changed using :meth:`.Performax4EXStage.set_baudrate` method, in which case you would need to explicitly specify it during the next connection.

In RS-485 mode ``idx`` parameter is still used, and it specifies the device number connected to this controller. By default this number is 0, and it can be queried (using USB connection) via :meth:`.Performax4EXStage.get_device_number`. It can also be set using :meth:`.Performax4EXStage.set_device_number`, although the changes takes effect only after the device is power cycled. Although in principle ``idx`` can be used to distinguish several Arcus controllers connected to the same bus (i.e., sharing the same RS-485 COM port), currently only single device connection is supported.

To switch between USB and RS-485 control modes, you need to plug or unplug USB connection. It is strongly recommended to power cycle the device after that, since otherwise it might stop responding to RS-485 commands.


Operation
-----------------------

This controller has several features and differences compared to most other stages and sliders:

    - The 4-axis and 2-axis controllers are inherently multi-axis, hence they always take the axis as the first argument. The axes are labeled with letters ``"x"``, ``"y"`` for a 2-axis version, or ``"x"``, ``"y"``, ``"z"``, ``"u"`` for a 4-axis one. The list of all axes is related to the exact controller, an can be obtained using :meth:`.Performax4EXStage.get_all_axes`. A single-axis controller does not take an axis argument.
    - Different axes can be enabled and disabled using :meth:`.Performax4EXStage.enable_axis`. Note that disabled axes still behave the same as the enabled ones; e.g., their position will increment as usual, when ``move_to`` is called. This can lead to some confusion, as the axis appears mostly operational, but the motor does not move.
    - In the default controller configuration the limit errors are enabled. In this case, once a single axes reaches the limit switch during motion, it is put into an error state, which immediately stops this an all other axes. Any further motion command on this axis will raise an error, although it is still possible to restart motion on other axes. The axis motion can only be resumed by calling :meth:`.Performax4EXStage.clear_limit_error`. If, however, limit errors are disabled, then only the axis which reached the limit is stopped, and all other axes are unaffected. Furthermore, the motion on the offending axis can be resumed without clearing its error status.
      In many cases the default limit error behavior is undesirable, so the class turns it off upon connection. It can be subsequently turned on and off using :meth:`.Performax4EXStage.enable_limit_errors`, and checked using :meth:`.Performax4EXStage.limit_errors_enabled`.
    - Since simplified single-axis controller (DMX-J-SA) always has limit errors disabled, its behavior is specified a bit differently. Upon connection you can specify ``autoclear`` argument (``True`` by default), which indicates that before every movement command the limit error should be automatically cleared.
    - The controllers also have analog and digital inputs and digital outputs, which can be queried and set with the corresponding commands.
    - The controller has an option to connect an encoder for a separate position readout. By default, all of the commands (e.g., for moving, getting position, getting current speed, etc.) still work in the step-counting mode, and the encoder values are only accessed via :meth:`.Performax4EXStage.get_encoder`/:meth:`.Performax4EXStage.set_encoder_reference`. In principle, there is a closed-loop mode call ``StepNLoop``, but it is not currently supported in the code.
    - The built-in motion command has 2 modes: relative and absolute. The code sets the absolute mode on connection and assumes it in all commands. However, if the mode changes for any reason, the move commands will stop working properly.