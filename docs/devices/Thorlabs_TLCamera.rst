.. _cameras_thorlabs_tlcamera:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras>`

Thorlabs Scientific Cameras interface [TODO: finish]
====================================================

This is the interface used in Thorlabs scientific sCMOS cameras such as Kiralux or Zelux. It has been tested with Thorlabs Kiralux camera.

The code is located in :mod:`pylablib.devices.Thorlabs`, and the main camera class is :class:`pylablib.devices.Thorlabs.ThorlabsTLCamera<.TLCamera.ThorlabsTLCamera>`.

DLL requirements
-----------------------

These cameras require ``thorlabs_tsi_camera_sdk.dll``, which is automatically installed with the freely available `Thorcam <https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=ThorCam>`__ tools. By default, the library searches for DLLs in ``Thorlabs/Scientific Imaging/ThorCam`` folder in ``Program Files`` folder (or ``Program files (x86)``, if 32-bit version of Python is running), as well as in the folder containing the script. If the DLLs are located elsewhere, the path can be specified using the library parameter ``devices/dlls/thorlabs_tlcam``::

    import pylablib as pll
    pll.par["devices/dlls/thorlabs_tlcam"] = "path/to/dlls"
    from pylablib.devices import Thorlabs
    cam = Thorlabs.ThorlabsTLCamera()


Connection
-----------------------

The cameras are identified by their serial number. To list all of the connected cameras, you can run :func:`Thorlabs.list_cameras_tlcam<.TLCamera.list_cameras>`::

    >> from pylablib.devices import Thorlabs
    >> Thorlabs.list_cameras_tlcam()
    [???]
    >> cam1 = Thorlabs.ThorlabsTLCamera()
    >> cam2 = Thorlabs.ThorlabsTLCamera()
    >> cam1.close()
    >> cam2.close()

If not serial is provided, the software connects to the first available camera.

Operation
------------------------

The operation of these cameras is relatively standard. They support all the standard methods for dealing with ROI and exposure, starting and stopping acquisition, and operating the frame reading loop.