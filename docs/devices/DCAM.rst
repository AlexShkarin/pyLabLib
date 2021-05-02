.. _cameras_dcam:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`.

DCAM cameras interface
=======================

DCAM is the interface used in Hamamatsu cameras. It has been tested with Hamamatsu Orca Flash and ImagEM.

The code is located in :mod:`pylablib.devices.DCAM`, and the main camera class is :class:`pylablib.devices.DCAM.DCAMCamera<.DCAM.DCAMCamera>`.

Software requirements
-----------------------

These cameras require ``dcamapi.dll``, which is installed with most of Hamamatsu software (such as HoKaWo or HiPic), as well as with the freely available `DCAM API <https://dcam-api.com/>`__, which also includes all the necessary drivers. After installation, the DLL is automatically added to the ``System32`` folder, where pylablib looks for it by default. If the DLL is located elsewhere, the path can be specified using the library parameter ``devices/dlls/dcamapi``::

    import pylablib as pll
    pll.par["devices/dlls/dcamapi"] = "path/to/dlls"
    from pylablib.devices import DCAM
    cam = DCAM.DCAMCamera()


Connection
-----------------------

The cameras are identified by their index, starting from zero. To get the total number of cameras, you can run :func:`.DCAM.get_cameras_number`::

    >> from pylablib.devices import DCAM
    >> DCAM.get_cameras_number()
    2
    >> cam1 = DCAM.DCAMCamera(idx=0)
    >> cam2 = DCAM.DCAMCamera(idx=1)
    >> cam1.close()
    >> cam2.close()


Operation
------------------------

The operation of these cameras is relatively standard. They support all the standard methods for dealing with ROI and exposure, starting and stopping acquisition, and operating the frame reading loop. The SDK also provides a universal interface for getting and setting various camera properties using their name. You can use :meth:`.DCAMCamera.get_value` and :meth:`.DCAMCamera.set_value` for that, as well as ``.v`` attribute which gives a dictionary-like access::

    >> cam = DCAM.DCAMCamera()
    >> cam.get_value("BINNING")  # get the camera binning (no binning, by default)
    1
    >> cam.set_value("EXPOSURE TIME", 0.1)  # set the exposure to 100ms
    >> cam.v["EXPOSURE TIME"]  # get the exposure; could also use cam.get_value("EXPOSURE TIME")
    0.1

To get a all available properties, you can call :meth:`.DCAMCamera.list_properties` to get a list with all property names and :meth:`.DCAMCamera.get_all_properties` to get the dictionary of all properties, both as text and as integer values.

Additionally, there's a couple of differences from the standard libraries worth highlighting:
    - The library supports only symmetric binning, i.e., the binning factor is the same in both directions. For compatibility :meth:`.DCAMCamera.get_roi` and :meth:`.DCAMCamera.set_roi` still return and accept both binnings independently, but they are always the same when returned, and ``vbin`` is ignored when set.
    - By default, the SDK does not provide independent control of the frame period and the exposure. Hence, ``set_frame_period`` method is unavailable, and the frame rate is defined solely by the exposure.