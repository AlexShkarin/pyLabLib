.. _cameras_picam:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`

Princeton Instruments Picam cameras
===================================

Picam is the interface provided by Teledyne Princeton Instruments and which supports a set of their cameras. It has been tested with PIXIS 400 camera.

The code is located in :mod:`pylablib.devices.PrincetonInstruments`, and the main camera class is :class:`pylablib.devices.PrincetonInstruments.PicamCamera<.picam.PicamCamera>`.

Software requirements
----------------------

These cameras require ``picam.dll``, which is installed with the freely available `PICam software <https://www.princetoninstruments.com/products/software-family/pi-cam>`__. By default, the library searches for DLLs in ``Princeton Instruments/PICam/Runtime`` folder in ``Program Files`` folder (or ``Program files (x86)``, if 32-bit version of Python is running), as well as in the folder containing the script. If the DLL is located elsewhere, the path can be specified using the library parameter ``devices/dlls/picam``::

    import pylablib as pll
    pll.par["devices/dlls/picam"] = "path/to/dlls"
    from pylablib.devices import PrincetonInstruments
    cam = PrincetonInstruments.PicamCamera()


Connection
----------------------

The cameras are identified by their serial number, which can look like ``"2800000001"``. To get the list of all cameras, you can use :func:`.PrincetonInstruments.list_cameras<.picam.list_cameras>`::

    >> from pylablib.devices import PrincetonInstruments
    >> PrincetonInstruments.list_cameras()
    [TCameraInfo(name='E2V 1340 x 400 (CCD 36)(B)(R)', serial_number='2800000001', model='PIXIS: 400BR', interface='USB 2.0'),
     TCameraInfo(name='E2V 1340 x 400 (CCD 36)(B)(R)', serial_number='2800000002', model='PIXIS: 400BR', interface='USB 2.0')]
    >> cam1 = PrincetonInstruments.PicamCamera('2800000001')
    >> cam2 = PrincetonInstruments.PicamCamera('2800000002')
    >> cam1.close()
    >> cam2.close()

If no serial number is supplied, the first available camera is connected.


Operation
------------------------

The operation of these cameras is relatively standard. They support all the standard methods for dealing with ROI, starting and stopping acquisition, and operating the frame reading loop. The SDK also provides a universal interface for getting and setting various :ref:`camera attributes <cameras_basics_attributes>` using their name. You can use :meth:`.PicamCamera.get_attribute_value` and :meth:`.PicamCamera.set_attribute_value` for that, as well as ``.cav`` attribute which gives a dictionary-like access::

    >> cam = PrincetonInstruments.PicamCamera()
    >> cam.get_attribute_value("Pixel Format")  # get the current pixel format
    'Monochrome 16-bit'
    >> cam.set_attribute_value("Exposure Time", 10)  # set the exposure time to 10 ms
    >> cam.cav["Exposure Time"]  # get the exposure; could also use cam.get_attribute_value("Exposure Time")
    10.0

To see all available attributes, you can call :meth:`.PicamCamera.get_all_attributes` to get a dictionary with attribute objects, and :meth:`.PicamCamera.get_all_attribute_values` to get the dictionary of attribute values. The attribute objects provide additional information: attribute kind (integer, enum, float, etc.), range (either numerical range, or selection of values for enum attributes), default value, etc.::

    >> cam = PrincetonInstruments.PicamCamera()
    >> attr = cam.get_attribute("Exposure Time")
    >> attr.default
    100.0
    >> attr.writable
    True
    >> (attr.min, attr.max)
    (0.0, 8355840.0)

Since these properties vary a lot between different cameras, it is challenging to write a universal class covering a large range of cameras. Hence, currently the universal class only has the basic camera parameter control such as ROI (without binning), exposure, and acquisition status. For many specific cameras you might need to explore the attributes tree using the Python class and operate them directly in your code.


Known issues
--------------------

- Frame period obtained using :meth:`.PicamCamera.get_frame_period` can be an underestimate (i.e., it can overestimate the frame rate).
- While the cameras support multiple ROIs, only single-ROI readout is currently supported.
- Changing readout mode (``"Readout Control Mode"``) to ``"Kinetics"`` might invalidate the current ROI, if it was originally too large. Therefore, you would need to call ``set_roi`` again after setting this mode.
- In principle, the cameras support a variety of different metainfos which can be enabled or disabled separately. However, for simplicity only two modes are supported in the camera class: either no metainfo, or full "standard" metainfo (frame stamp, and start and stop timestamps). Any time the metainfo is enabled, disabled, or queried, it is automatically "truncated" to one of these two modes.