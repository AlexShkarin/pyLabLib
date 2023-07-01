.. _cameras_thorlabs_tlcamera:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`

Thorlabs Scientific Cameras interface
====================================================

This is the interface used in Thorlabs scientific sCMOS cameras such as Kiralux or Zelux. It has been tested with Thorlabs Kiralux camera.

The code is located in :mod:`pylablib.devices.Thorlabs`, and the main camera class is :class:`pylablib.devices.Thorlabs.ThorlabsTLCamera<.TLCamera.ThorlabsTLCamera>`.

Software requirements
-----------------------

These cameras require ``thorlabs_tsi_camera_sdk.dll``, as well as several additional DLLs: ``thorlabs_unified_sdk_kernel.dll``, ``thorlabs_unified_sdk_main.dll``, ``thorlabs_tsi_usb_driver.dll``, ``thorlabs_tsi_usb_hotplug_monitor.dll``, ``thorlabs_tsi_cs_camera_device.dll``, ``tsi_sdk.dll``, ``tsi_usb.dll``. All of them is automatically installed with the freely available `ThorCam <https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=ThorCam>`__ tools. By default, the library searches for DLLs in ``Thorlabs/Scientific Imaging/ThorCam`` folder in ``Program Files`` folder (or ``Program files (x86)``, if 32-bit version of Python is running), as well as in the folder containing the script. If the DLLs are located elsewhere, the path can be specified using the library parameter ``devices/dlls/thorlabs_tlcam``::

    import pylablib as pll
    pll.par["devices/dlls/thorlabs_tlcam"] = "path/to/dlls"
    from pylablib.devices import Thorlabs
    cam = Thorlabs.ThorlabsTLCamera()


Connection
-----------------------

The cameras are identified by their serial number. To list all of the connected cameras, you can run :func:`Thorlabs.list_cameras_tlcam<.TLCamera.list_cameras>`::

    >> from pylablib.devices import Thorlabs
    >> Thorlabs.list_cameras_tlcam()
    ['12001', '12002']
    >> cam1 = Thorlabs.ThorlabsTLCamera(serial="12001")
    >> cam2 = Thorlabs.ThorlabsTLCamera(serial="12002")
    >> cam1.close()
    >> cam2.close()

If no serial is provided, the software connects to the first available camera.

Operation
------------------------

The operation of these cameras is relatively standard. They support all the standard methods for dealing with ROI and exposure, starting and stopping acquisition, and operating the frame reading loop.

For color cameras, several readout modes are available, which can be set up using :meth:`.ThorlabsTLCamera.set_color_format` method. By default, the color cameras output the frames in the linear RGB format (each frame is a 3D array with the last axis encoding color channel).

.. warning::
    The library appears to be not entirely stable: every time acquisition start is issued, there is small (0.1-1%) chance that it will not actually start, which results in timeout errors. Furthermore, there are occasional crashes on the SDK unloading (i.e., camera closing), especially when acquisition has been started and stopped multiple times. It is unclear, what is the cause of this behavior, but it seems to originate from the manufacturer's DLL (bare-bones example and the native Python library reproduce this behavior). Hence, it might be different with different DLL versions.

.. note::
    The DLL prints some debug information in the console when camera list is requested and when the camera is opened. At the moment, it is unclear how to get rid of it.