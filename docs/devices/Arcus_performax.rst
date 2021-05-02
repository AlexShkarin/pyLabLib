.. _stages_arcus_performax:

.. note::
    General stage communication concepts are described on the corresponding :ref:`page <stages_basics>`

Arcus Performax positioners
==============================

Arcus has several motor controllers and drivers, which are mainly different in their number of axes, communication possibilities, and driving function. They are also distributed under different names, e.g., Nippon Pulse America (NPA) or Newmark Systems. However, the models nomenclature is the same: there is 4EX for 4-axis controllers with USB and RS485 connection, 2EX/2ED for 2-axis controllers with USB and RS485 connections, and 4ET for 4-axis controllers with Ethernet connection. The class has been tested with 4EX and (partially) 2ED controllers with USB connectivity mode, but other controllers and modes mentioned above should also work.

The main device classes are :class:`pylablib.devices.Arcus.Performax4EXStage<.performax.Performax4EXStage>` or 4-axis controllers and :class:`pylablib.devices.Arcus.Performax2EXStage<.performax.Performax2EXStage>` for 2-axis controllers (they have several syntax differences, so one can not substitute for the other).


Software requirements
-----------------------

The controller has several communication modes: USB, R485, and Ethernet. USB mode requires a driver supplied with the operation software: `Arcus Drivers and Tools <https://www.arcus-technology.com/support/downloads/download-info/drivers-and-tools-installer/>`__, `Performax Series Installer <https://www.arcus-technology.com/support/downloads/download-info/performax-series-installer/>`__, and `Performax USB Setup <https://www.arcus-technology.com/support/downloads/download-info/performax-usb-setup/>`__ (all obtained at `Arcus website <https://www.arcus-technology.com/support/downloads/>`__).  Installing all three seem to be sufficient. Once the appropriate USB drivers are installed, one can connect the device directly via its USB port and use the manufacturer DLLs ``PerformaxCom.dll`` and ``SiUSBXp.dll`` to communicate with the device. They can be obtained on the manufacturer's `website <https://www.arcus-technology.com/support/downloads/download-info/usb-64-bit-dll/>`__ and placed in the folder with the script, or in the ``System32`` Windows folder. If the DLL is located elsewhere, the path can be specified using the library parameter ``devices/dlls/arcus_performax``::

    import pylablib as pll
    pll.par["devices/dlls/arcus_performax"] = "path/to/dll"
    from pylablib.devices import Arcus
    stage = Arcus.Performax4EXStage()

The controller has only been tested with USB communication.


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


Operation
-----------------------

This controller has several features and differences compared to most other stages and sliders:

    - The controller is inherently multi-axis, hence it always take the axis as the first argument. The axes are labeled with letter starting with ``"x"``. The list of all axes is related to the exact controller, an can be obtained using :meth:`.Performax4EXStage.get_all_axes`.
    - Different axes can be enabled and disabled using :meth:`.ANC350.enable_axis`. Note that *disabled axes still behave similarly to the enabled ones*; e.g., their step position will increment with the usual speed, when ``move_to`` is called.
    - In the default controller configuration the limit errors are enabled. In this case, once a single axes reaches the limit switch during motion, it is put into an error state, which immediately stops this an all other axes. Any further motion command on this axis will raise an error, although it is still possible to restart motion on other axes. The axis motion can only be resumed by calling :meth:`.Performax4EXStage.clear_limit_error`. If, however, limit errors are disabled, then only the axis which reached the limit is stopped, and all other axes are unaffected. Furthermore, the motion on the offending axis can be resumed without clearing its error status.
      In many cases the default limit error behavior is undesirable, so the class turns it off upon connection. It can be subsequently turned on and off using :meth:`.Performax4EXStage.enable_limit_errors`, and checked using :meth:`.Performax4EXStage.limit_errors_enabled`.
    - The controllers also have analog and digital inputs and digital outputs, which can be queried and set with the corresponding commands.
    - The controller has an option to connect the encoder for a separate position readout. By default, all of the commands (e.g., for moving, getting position, getting current speed, etc.) still work in the step-counting mode, and the encoder values are only accessed via :meth:`.Performax4EXStage.get_encoder`/:meth:`.Performax4EXStage.set_encoder_reference`. In principle, there is a closed-loop mode call ``StepNLoop``, but it is not currently supported in the code.
    - The built-in motion command has 2 modes: relative and absolute. The code sets the absolute mode on connection and assumes it in all commands. However, if the mode changes for any reason, the move commands will stop working properly.