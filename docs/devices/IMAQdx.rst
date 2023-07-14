.. _cameras_imaqdx:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`

NI IMAQdx cameras interface
===========================

NI IMAQdx is the interface provided by National Instruments and which supports a wide variety of cameras. It is completely separate from IMAQ, and it supports different communication interfaces: USB, Ethernet and FireWire. It has been tested with Ethernet-connected PhotonFocus HD1-D1312 camera.

The code is located in :mod:`pylablib.devices.IMAQdx`, and the main camera class is :class:`pylablib.devices.IMAQdx.IMAQdxCamera<.IMAQdx.IMAQdxCamera>`.

Software requirements
----------------------

These cameras require ``imaqdx.dll``, which is installed with the freely available `Vision Acquisition Software <https://www.ni.com/en-us/support/downloads/drivers/download.vision-acquisition-software.html>`__. However, the IMAQdx part of the software is proprietary, and requires purchase to use. If the software license is invalid, then any attempt to communicate with cameras will result in ``License not activated`` error (although simply listing the cameras still works). After installation, the DLL is automatically added to the ``System32`` folder, where pylablib looks for it by default. If the DLL is located elsewhere, the path can be specified using the library parameter ``devices/dlls/niimaqdx``::

    import pylablib as pll
    pll.par["devices/dlls/niimaqdx"] = "path/to/dlls"
    from pylablib.devices import IMAQdx
    cam = IMAQdx.IMAQdxCamera()


Connection
----------------------

The cameras are identified by their name, which usually looks like ``"cam0"``. To get the list of all cameras, you can use NI MAX (Measurement and Automation Explorer), or :func:`.IMAQdx.list_cameras`::

    >> from pylablib.devices import IMAQdx
    >> IMAQdx.list_cameras()
    ['cam0', 'cam1']
    >> cam1 = IMAQdx.IMAQdxCamera('cam0')
    >> cam2 = IMAQdx.IMAQdxCamera('cam1')
    >> cam1.close()
    >> cam2.close()


Operation
------------------------

The operation of these cameras is relatively standard. They support all the standard methods for dealing with ROI, starting and stopping acquisition, and operating the frame reading loop. The SDK also provides a universal interface for getting and setting various :ref:`camera attributes <cameras_basics_attributes>` using their name. You can use :meth:`.IMAQdxCamera.get_attribute_value` and :meth:`.IMAQdxCamera.set_attribute_value` for that, as well as ``.cav`` attribute which gives a dictionary-like access::

    >> cam = IMAQdx.IMAQdxCamera()
    >> cam.get_attribute_value("StatusInformation/AcqInProgress")  # check if the camera is acquiring
    0
    >> cam.set_attribute_value("Width", 512)  # set the ROI width to 512px
    >> cam.cav["Width"]  # get the exposure; could also use cam.get_attribute_value("Width")
    512

To see all available attributes, you can call :meth:`.IMAQdxCamera.get_all_attributes` to get a dictionary with attribute objects, and :meth:`.IMAQdxCamera.get_all_attribute_values` to get the dictionary of attribute values. The attribute objects provide additional information: attribute kind (integer, enum, string, etc.), range (either numerical range, or selection of values for enum attributes), description string, etc.::

    >> cam = IMAQdx.IMAQdxCamera()
    >> attr = cam.get_attribute("Width")
    >> attr.description
    'Width of the Image provided by the device (in pixels).'
    >> attr.writable
    True
    >> (attr.min, attr.max)
    (448, 1312)

Since these properties vary a lot between different cameras, it is challenging to write a universal class covering a large range of cameras. Hence, currently the universal class only has the basic camera parameter control such as ROI (without binning) and acquisition status. For many specific cameras you might need to explore the attributes tree (either using the Python class and, e.g., a console, or via NI MAX) and operate them directly in your code.


Known issues
--------------------

- It seems like sometimes the camera communication settings might be interfering with its operation. It can show up in an unexpected way, e.g., as an ``Attribute value is out of range`` error when starting acquisition. If it looks like this might be the case, it is a good idea to open the camera in NI MAX (note that Ethernet cameras are listed under ``Network Devices``, not in the general device list) and try to snap a single frame. NI MAX might report some problems with the settings and suggest resolution methods. Once the camera is operational, you can close NI MAX and save the camera settings (request is shown upon closing).
- In general, Ethernet cameras work better with larger packet sizes. However, packets above 1500 bits (so-called jumbo packets) are not supported by all network adapters by default. If this is the case, any attempt to acquire images causes ``IMAQdxErrorTestPacketNotReceived`` error. One way to deal with that is to set the packet size to 1500, which is done automatically when ``small_packet=True`` is supplied upon the camera creation. The other is to enable jumbo packets in the adapter properties (in Windows this is done in Device Manager).
- Currently only the basic unpacked monochrome pixel formats are supported: ``Mono8``, ``Mono10``, ``Mono12``, ``Mono16``, and ``Mono32``. The reason is that even nominally well-defined types (e.g., ``Mono12Packed``) have different formats for different cameras. Currently any unsupported format will raise an error on readout by default. It it still possible to read these out as raw frame data in the form of 1D or 2D numpy ``'u1'`` array by enabling raw frame readout using :meth:`.IMAQdxCamera.enable_raw_readout` method::

    >> cam = IMAQdx.IMAQdxCamera()
    >> cam.get_detector_size()  # 1280px x 1024px frame
    (1280, 1024)
    >> cam.set_attribute_value("PixelFormat", "BGRA 8 Packed")  # unsupported format
    >> cam.snap().shape
    ...
    IMAQdxError: pixel format BGRA 8 Packed is not supported
    >> cam.enable_raw_readout("frame")  # frame data is returned as a flat array
    >> cam.snap().shape  # 1280 * 1024 * 4 = 5242880 bytes
    (5242880,)