.. _stages_smaract:

.. note::
    General stage communication concepts are described on the corresponding :ref:`page <stages_basics>`

SmarAct positioners
=======================

SmarAct has multiple different controller covering different slider kinds. So far only simple controllers (CU/HCU/SCU) are implemented.


.. _stages_smaract_scu:

SmarAct CU/HCU/SCU
-----------------------

This is a simple controller, which is mostly aimed at open-loop (i.e., no position readout) positioners. It can control up to 3 axes, and connects to the PC via the USB port.

The device class is :class:`pylablib.devices.SmarAct.SCU3D<.scu3d.SCU3D>`. Currently only open-loop controllers are supported.


Software requirements
~~~~~~~~~~~~~~~~~~~~~~~

The controller shows up as a virtual COM port, and it has a standard FTDI chip, so it does not need any special drivers. However, to communicate with the device, it still needs ``SCU3DControl.dll`` library. It is supplied on a CD together with the device, although it might also be possible to request it from SmarAct.


Connection
~~~~~~~~~~~~~~~~~~~~~~~

The devices are identified by their index starting from 0. To get the list of all the connected devices, you can use :func:`SmarAct.list_scu_devices<.scu3d.list_devices>`::

    >> from pylablib.devices import SmarAct
    >> SmarAct.list_scu_devices()
    [TDeviceInfo(device_id=0, firmware_version='1.3.0.0', dll_version='4.3.0.0')]
    >> stage = SmarAct.SCU3D(idx=0)  # connect to the first device in the list
    >> stage.close()

Due to the manufacturer's API organization, it is currently only possible to "reserve" all connected stages of the same type simultaneously in one application. This means that no other application can connect to any of the stages as long as at least one stage is being controlled (though it does not make any difference if only one stage is connected).

In addition, currently there is no check on whether the stage is already controlled in the other part of the code. This is in contrast with the vast majority of the devices, which issue a unique handle making it impossible to create two different device objects even within the same application. Hence, one needs to be careful to not connect to the same device twice, which can lead to confusing behavior.

Operation
~~~~~~~~~~~~~~~~~~~~~~~

This controller has several features and differences compared to most other stages and sliders:

    - The motion is generally executed in "macrosteps", which is a sequence of several "microsteps" with a given amplitude, frequency, and number. A single macrostep with the defined parameters can be performed with :meth:`.SCU3D.move_macrostep`, while :meth:`.SCU3D.move_by` executes a series of these macrosteps with one of the predefined sizes (from 0 to 20). These sizes are configured to roughly correspond to the step sizes selectable by the controller, although the agreement is not exact.




.. _stages_smaract_mcs:

SmarAct MCS2 stages
-----------------------

This is an advanced controller, which can control multiple open-loop and closed-loop stages using multiple sensor modules. It connects to the PC via the USB or the Ethernet port.

The device class is :class:`pylablib.devices.SmarAct.MCS2<.MCS2.MCS2>`. It has been tested with an Ethernet-connected MCS module with several SLx stages.


Software requirements
~~~~~~~~~~~~~~~~~~~~~~~

The controller requires libraries supplied with the SmarAct MCS2 software, which is usually distributed with the device. The required DLL is called ``SmarActCTL.dll`` and is located in the MCS2 folder (either ``MCS/SDK/lib64`` for 64-bit systems). By default, pyLabLib searches for these DLLs in the default MCS2 software location (``C:/SmarAct/MCS2``), in the folder defined by the corresponding environment variable upon installation (``MCS2_SDK``), as well as in the folder containing the script. If the DLLs are located elsewhere, the path can be specified using the library parameter ``devices/dlls/smaract_mcs2``::

    import pylablib as pll
    pll.par["devices/dlls/smaract_mcs2"] = "path/to/MCS2/dlls"
    from pylablib.devices import SmarAct
    stage = SmarAct.MCS2("network:sn:MCS2-00000001")


Connection
~~~~~~~~~~~~~~~~~~~~~~~

The devices are identified by their locator string, which may look like, e.g., ``"network:sn:MCS2-00000001"`` or ``"usb:sn:MCS2-00000001"``. To get the list of all the connected devices, you can use :func:`SmarAct.list_mcs2_devices<.MCS2.list_devices>`::

    >> from pylablib.devices import SmarAct
    >> SmarAct.list_msc2_devices()
    ["usb:sn:MCS2-00000123"]
    >> stage = SmarAct.MCS2("usb:sn:MCS2-00000123")
    >> stage.close()

Operation
~~~~~~~~~~~~~~~~~~~~~~~

This controller has several features and differences compared to most other stages and sliders:

    - The provided class implements the basic functionality required for the regular levels of automation: movement, accessing position and status, setting up basic parameters (velocity, acceleration, step frequency, etc.), homing. However, it does not cover more advanced and rarely used functions like details of the sensor operation, auxiliary IO, triggering, operation modes (normal, low noise, etc.), PID parameters, and so on. These can still be accessed using :meth:`.MCS2.get_property` and :meth:`.MCS2.set_property` methods, but the interpretation of the property values is up to the user.