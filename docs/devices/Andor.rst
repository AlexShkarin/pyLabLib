.. _cameras_andor:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`

Andor cameras
=======================

Andor implements two completely separate interfaces for different cameras. The older one, called SDK2, or simply SDK, provides interface for the older cameras: iXon, iKon, iStart, iDus, iVac, Luca, Newton. The details of this SDK are available in the `manual <https://andor.oxinst.com/downloads/uploads/Andor_Software_Development_Kit_2.pdf>`__.

The newer SDK, called SDK3, covers newer cameras: Zyla, Neo, Apogee, Sona, Marana, and Balor. The `manual <https://andor.oxinst.com/downloads/uploads/Andor_SDK3_Manual.pdf>`__ describes the cameras and capabilities in more details.

The required DLLs are distributed with `Andor Solis <https://andor.oxinst.com/products/solis-software/>`__ or the corresponding `Andor SKD <https://andor.oxinst.com/products/software-development-kit/>`__. In most cases, you have Andor Solis already installed to provide the drivers and to communicate with the cameras to begin with.


.. _cameras_andor_sdk2:

Andor SDK 2
-----------------------

This is an older SDK, which mainly involves older cameras. It has been tested with Andor iXon, Luca, and Newton.

The code is located in :mod:`pylablib.devices.Andor`, and the main camera class is :class:`pylablib.devices.Andor.AndorSDK2Camera<.AndorSDK2.AndorSDK2Camera>`.

Software requirements
~~~~~~~~~~~~~~~~~~~~~~~

The required DLL can have different names depending on the Solis version and SDK bitness. For 64-bit version it will be called ``atmcd64d.dll`` or ``atmcd64d_legacy.dll``. For 32-bit version, correspondingly, ``atmcd32d.dll`` or ``atmcd32d_legacy.dll``. By default, library searches for DLLs in ``Andor Solis`` and ``Andor SDK`` folder in ``Program Files`` folder (or ``Program files (x86)``, if 32-bit version of Python is running), as well as in the folder containing the script. If the DLLs are located elsewhere, the path can be specified using the library parameter ``devices/dlls/andor_sdk2``::

    import pylablib as pll
    pll.par["devices/dlls/andor_sdk2"] = "path/to/dlls"
    from pylablib.devices import Andor
    cam = Andor.AndorSDK2Camera()

Connection
~~~~~~~~~~~~~~~~~~~~~~~

The cameras are identified by their index, starting from zero. To get the total number of cameras, you can run :func:`Andor.get_cameras_number_SDK2<.AndorSDK2.get_cameras_number>`::

    >> from pylablib.devices import Andor
    >> Andor.get_cameras_number_SDK2()
    2
    >> cam1 = Andor.AndorSDK2Camera(idx=0)
    >> cam2 = Andor.AndorSDK2Camera(idx=1)
    >> cam1.close()
    >> cam2.close()

.. warning::
    It is important to close all camera connections before finishing your script. Otherwise, DLL resources might become permanently blocked, and the only way to solve it would be to restart the PC.

Operation
~~~~~~~~~~~~~~~~~~~~~~~~

The operation of these cameras is relatively standard. They support all the standard methods for dealing with ROI and exposure, starting and stopping acquisition, and operating the frame reading loop. However, there's a couple of differences from the standard libraries worth highlighting:

    - Since the manufacturer DLLs do not provide methods to get most of the camera parameters (such as exposure or ROI), it is impossible to know them when connecting the camera. To get around it, the camera is put into a "default" state any time the connection is opened.
    - When applicable, it is important to properly set the cooling setpoint and the fan mode. By default, the fan is turned off, and the cooling is set to the 20'th percentile of the whole range (e.g., -80C for Andor iXon). It is possible to pass these parameters on camera creation::

        cam = Andor.AndorSDK2Camera(temperature=-50, fan_mode="on")
    
    - Often cameras have a lot of different readout parameters: channel, amplifier, vertical and horizontal scan speed, etc. These parameters greatly affect the camera sensitivity and readout speed. Upon the connection, the parameter are typically set to the slowest mode. To get the list of all possible parameter combinations, you can use :meth:`.AndorSDK2Camera.get_all_amp_modes` and :meth:`.AndorSDK2Camera.get_max_vsspeed`. Afterwards, you can set them using :meth:`.AndorSDK2Camera.set_amp_mode` and :meth:`.AndorSDK2Camera.set_vsspeed`.
    - The default shutter parameter is ``"closed"``. This preserves camera from possible high illumination, but can lead to confusion, if you expect to see some image.
    - This SDK does not allow for specifying number of frames in the frames buffer. However, the parameters chosen by the SDK are usually reasonable (at least a second worth of acquisition).
    - Some cameras (e.g., iXon) have lots of readout (full frame, ROI, full vertical binning, etc.) and acquisition modes (single, continuous, accumulating, kinetic cycle, etc.). They are described in details in the `manual <https://andor.oxinst.com/downloads/uploads/Andor_Software_Development_Kit_2.pdf>`__.





.. _cameras_andor_sdk3:

Andor SDK 3
-----------------------

This is a newer SDK, which covers the newer cameras. It has been tested with Andor Zyla, Neo and Marana.

The code is located in :mod:`pylablib.devices.Andor`, and the main camera class is :class:`pylablib.devices.Andor.AndorSDK3Camera<.AndorSDK3.AndorSDK3Camera>`.

Software requirements
~~~~~~~~~~~~~~~~~~~~~~~

This library requires several DLLs all located in the same folder: ``atcore.dll``, ``atblkbx.dll``, ``atcl_bitflow.dll``, ``atdevapogee.dll``, ``atdevregcam.dll``, ``atusb_libusb.dll``, ``atusb_libusb10.dll``. Same as for SDK2, pylablib looks for DLLs in ``Andor Solis`` and ``Andor SDK3`` folders in ``Program Files`` folder (or ``Program files (x86)``, if 32-bit version of Python is running), as well as in the folder containing the script. A custom DLLs path can be specified using the library parameter ``devices/dlls/andor_sdk3``::

    import pylablib as pll
    pll.par["devices/dlls/andor_sdk3"] = "path/to/SDK3/dlls"
    from pylablib.devices import Andor
    cam = Andor.AndorSDK3Camera()

Connection
~~~~~~~~~~~~~~~~~~~~~~~

The cameras are identified by their index, starting from zero. To get the total number of cameras, you can run :func:`Andor.get_cameras_number_SDK3<.AndorSDK3.get_cameras_number>`::

    >> from pylablib.devices import Andor
    >> Andor.get_cameras_number_SDK3()
    2
    >> cam1 = Andor.AndorSDK3Camera(idx=0)
    >> cam2 = Andor.AndorSDK3Camera(idx=1)
    >> cam1.close()
    >> cam2.close()

Operation
~~~~~~~~~~~~~~~~~~~~~~~~

The operation of these cameras is also relatively standard. They support all the standard methods for dealing with ROI and exposure, starting and stopping acquisition, and operating the frame reading loop. However, there's a couple of differences from the standard libraries worth highlighting:

    - The SDK also provides a universal interface for getting and setting various :ref:`camera attributes <cameras_basics_attributes>` (called "features" in the documentation) using their name. You can use :meth:`.AndorSDK3Camera.get_attribute_value` and :meth:`.AndorSDK3Camera.set_attribute_value` for that, as well as ``.cav`` attribute which gives a dictionary-like access::

        >> cam = Andor.AndorSDK3Camera()
        >> cam.get_attribute_value("CameraAcquiring")  # check if the camera is acquiring
        0
        >> cam.set_attribute_value("ExposureTime", 0.1)  # set the exposure to 100ms
        >> cam.cav["ExposureTime"]  # get the exposure; could also use cam.get_attribute_value("ExposureTime")
        0.1

      Some values serve as commands; these can be invoked using :meth:`.AndorSDK3Camera.call_command` method. To see all available attributes, you can call :meth:`.AndorSDK3Camera.get_all_attributes` to get a dictionary with attribute objects, and :meth:`.AndorSDK3Camera.get_all_attribute_values` to get the dictionary of attribute values. The attribute objects provide additional information: their kind, whether they are implemented, readable, or writable, what are their limits or possible values, etc::

        >> cam = Andor.AndorSDK3Camera()
        >> attr = cam.get_attribute("SensorTemperature")
        >> attr.readable
        True
        >> attr.writable
        False
        >> (attr.min, attr.max)
        (-100.0, 50.0)
      
      The description of the attributes is given in `manual <https://andor.oxinst.com/downloads/uploads/Andor_SDK3_Manual.pdf>`__.
    
    - USB cameras can, in principle, generate data at higher rate than about 320Mb/s that the USB3 bus supports. For example, Andor Zyla with 16 bit readout has a single full frame size of 8Mb, which puts the maximal USB throughput at about 40FPS. At the same time, the camera itself is capable of reading up to 100FPS at the full frame. Hence, it is possible to overflow the camera internal buffer (size on the order of 1Gb) regardless of the PC performance. If this happens, the acquisition process halts and needs to be restarted. You can check the number of buffer overflows using :meth:`.AndorSDK3Camera.get_missed_frames_status`, and reset this counter using :meth:`.AndorSDK3Camera.reset_overflows_counter`; the counter is also automatically resets on acquisition clearing, but not stopping.

      Furthermore, the class implements different strategies when encountering overflow while waiting for a new frame. The specific strategy is selected using :meth:`.AndorSDK3Camera.set_overflow_behavior`, and it can be ``"error"`` (raise :exc:`.AndorFrameTransferError`, which is the default behavior), ``"restart"`` (restart the acquisition and immediately raise timeout error), or ``"ignore"`` (ignore the overflow, which will eventually lead to a timeout error, as the new frames are no longer generated).