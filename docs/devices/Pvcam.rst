.. _cameras_pvcam:
 
.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`

Photometrics PVCAM cameras
===================================

PVCAM is the interface provided by Teledyne Photometrics and which supports a set of their cameras. It has been tested with Prime 95B camera.

The code is located in :mod:`pylablib.devices.Photometrics`, and the main camera class is :class:`pylablib.devices.Photometrics.PvcamCamera<.pvcam.PvcamCamera>`.

Software requirements
----------------------

These cameras require ``pvcam32.dll`` or ``pvcam64.dll``, which is installed with the freely available (upon registration) `PVCAM software <https://www.photometrics.com/support/download/pvcam>`__. By default, the library searches for DLL is automatically added to the ``System32`` folder, where pylablib looks for them by default. If the DLL is located elsewhere, the path can be specified using the library parameter ``devices/dlls/pvcam``::

    import pylablib as pll
    pll.par["devices/dlls/pvcam"] = "path/to/dlls"
    from pylablib.devices import Photometrics
    cam = Photometrics.PvcamCamera()


Connection
----------------------

The cameras are identified by their name, which can look like ``"PMUSBCam00"``. To get the list of all cameras, you can use :func:`.Photometrics.list_cameras<.pvcam.list_cameras>`::

    >> from pylablib.devices import Photometrics
    >> Photometrics.list_cameras()
    ['PMUSBCam00', 'PMUSBCam01']
    >> cam1 = Photometrics.PvcamCamera('PMUSBCam00')
    >> cam2 = Photometrics.PvcamCamera('PMUSBCam01')
    >> cam1.close()
    >> cam2.close()

If no name is supplied, the first camera in the list is connected.


Operation
------------------------

The operation of these cameras is relatively standard. They support all the standard methods for dealing with ROI, starting and stopping acquisition, and operating the frame reading loop. The SDK also provides a universal interface for getting and setting various :ref:`camera attributes <cameras_basics_attributes>` using their name. You can use :meth:`.PvcamCamera.get_attribute_value` and :meth:`.PvcamCamera.set_attribute_value` for that, as well as ``.cav`` attribute which gives a dictionary-like access::

    >> cam = Photometrics.PvcamCamera()
    >> cam.get_attribute_value("EXPOSURE_MODE")  # get the current exposure mode
    'Internal Trigger'
    >> cam.set_attribute_value("METADATA_ENABLED", True)  # enable frame metadata
    >> cam.cav["METADATA_ENABLED"]  # check if metadata is enabled; could also use cam.get_attribute_value("METADATA_ENABLED")
    True

To see all available attributes, you can call :meth:`.PvcamCamera.get_all_attributes` to get a dictionary with attribute objects, and :meth:`.PvcamCamera.get_all_attribute_values` to get the dictionary of attribute values. The attribute objects provide additional information: attribute kind (integer, enum, float, etc.), range (either numerical range, or selection of values for enum attributes), default value, etc.::

    >> cam = Photometrics.PvcamCamera()
    >> attr = cam.get_attribute("EXPOSURE_TIME")
    >> attr.default
    0
    >> attr.readable
    True
    >> (attr.min, attr.max)
    (0, 10000)

Since these properties vary a lot between different cameras, it is challenging to write a universal class covering a large range of cameras. Hence, currently the universal class only has the basic camera parameter control such as ROI (without binning), exposure, and acquisition status. For many specific cameras you might need to explore the attributes tree using the Python class and operate them directly in your code.


Fast buffer readout mode
~~~~~~~~~~~~~~~~~~~~~~~~

At high frame rates (above ~10kFPS) dealing with each frame individually becomes too slow for Python. Hence, there is an option to read out and process frames in larger 'chunks', which are 3D numpy arrays with the first axis enumerating the frame index. This approach leverages the ability to store several frame buffers in the contiguous memory locations (resulting in a single 3D array), and it essentially eliminates the overhead for dealing with multiple frames at high frame rates, as long as the total data rate is manageable (typically below 600Mb/s).

This option can be accessed by calling using :meth:`.PvcamCamera.set_frame_format` method to set frames format to ``"chunks"``. In this case, instead of a list of individual frames (which is the standard behavior), the method returns list of chunks, which contain several consecutive frames.

Known issues
--------------------

- Frame period obtained using :meth:`.PvcamCamera.get_frame_period` can be an underestimate (i.e., it can overestimate the frame rate), especially for USB-connected devices.
- While the cameras support multiple ROIs, only single-ROI readout is currently supported.
- Exposure time, exposure mode, and ROI are configured using special methods separately from other camera attributes. Therefore, their corresponding attributes are read-only.
- Not all horizontal and vertical binning combinations are supported. The allowed combinations can be queries using :meth:`.PvcamCamera.get_supported_binning_modes`. If the combination is not supported, it is truncated down to the smallest supported one.