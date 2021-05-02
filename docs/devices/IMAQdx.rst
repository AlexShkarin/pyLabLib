.. _cameras_imaqdx:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`

NI IMAQdx interface
=======================

NI IMAQdx is the interface provided by  National Instruments and which supports a wide variety of cameras. It is completely separate from IMAQ, and it supports other interfaces: USB, Ethernet and FireWire. It has been tested with ???.

The code is located in :mod:`pylablib.devices.IMAQdx`, and the main camera class is :class:`pylablib.devices.IMAQdx.IMAQdxCamera<.IMAQdx.IMAQdxCamera>`.

Software requirements
----------------------

These cameras require ``imaqdx.dll``, which is installed with the freely available `Vision Acquisition Software <https://www.ni.com/en-us/support/downloads/drivers/download.vision-acquisition-software.html>`__. However, the IMAQdx part of the software is proprietary, and requires purchase to use. After installation, the DLL is automatically added to the ``System32`` folder, where pylablib looks for it by default. If the DLL is located elsewhere, the path can be specified using the library parameter ``devices/dlls/niimaqdx``::

    import pylablib as pll
    pll.par["devices/dlls/niimaqdx"] = "path/to/dlls"
    from pylablib.devices import IMAQdx
    cam = IMAQdx.IMAQdxCamera()


Connection
----------------------

The cameras are identified by their name, which usually looks like ``"cam0"``. To get the list of all cameras, you can use NI MAX (Measurement and Automation Explorer), or :func:`.IMAQdx.list_cameras`::

    >> from pylablib.devices import IMAQdx
    >> IMAQdx.list_cameras()
    [`cam0`, `cam1`]
    >> cam1 = IMAQdx.IMAQdxCamera('cam0')
    >> cam2 = IMAQdx.IMAQdxCamera('cam1')
    >> cam1.close()
    >> cam2.close()


Operation
------------------------

The operation of these cameras is relatively standard. They support all the standard methods for dealing with ROI and exposure, starting and stopping acquisition, and operating the frame reading loop. The SDK also provides a universal interface for getting and setting various camera properties using their name. You can use :meth:`.IMAQdxCamera.get_value` and :meth:`.IMAQdxCamera.set_value` for that, as well as ``.v`` attribute which gives a dictionary-like access::

    >> cam = IMAQdx.IMAQdxCamera()
    >> cam.get_value("StatusInformation/AcqInProgress")  # check if the camera is acquiring
    0
    >> cam.set_value("Width", 512)  # set the ROI width to 512px
    >> cam.v["Width"]  # get the exposure; could also use cam.get_value("Width")
    512

To get a dictionary of all available property values, you can call :meth:`.IMAQdxCamera.get_all_values`. In addition, you can use :meth:`.IMAQdxCamera.list_attributes` and ``attributes`` object attribute to get a list with all attribute objects. In addition to getting and setting values (same as :meth:`.IMAQdxCamera.get_value` and :meth:`.IMAQdxCamera.set_value`) they provide additional information: attribute kind (integer, enum, string, etc.), range (either numerical range, or selection for values for enum attributes), description string, etc.