.. _cameras_basler:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`

Basler cameras interface
===========================

Basler manufactures a wide variety of cameras, which implement GenICam-based interface through its pylon API. It has been tested with pylon-provided emulated camera.

The code is located in :mod:`pylablib.devices.Basler`, and the main camera class is :class:`pylablib.devices.Basler.BaslerPylonCamera<.pylon.BaslerPylonCamera>`.

Software requirements
----------------------

These cameras require ``PylonC_vX_Y.dll`` (where ``X`` and ``Y`` is the pylon version, e.g., ``PylonC_V7_1.dll``), which is installed with the freely available upon registration `Basler pylon Camera Software Suite <https://www.baslerweb.com/en/downloads/software-downloads/>`__ (the current latest version is `7.1.0 <https://www.baslerweb.com/en/downloads/software-downloads/software-pylon-7-1-0-windows/>`__). Note that the DLLs are contained in the pylon SDK, which is only included in the "developer" version of the suite, and not in the "camera user" (default) version. After installation, the path to the DLL (for pylon 7.1.0 located by default in ``Basler/pylon 7/Runtime/x64`` folder in ``Program Files``) is automatically added to system ``PATH`` variable, which is one of the places where pylablib looks for it by default. If the DLLs are located elsewhere, the path (either to the DLL file, or to the containing folder) can be specified using the library parameter ``devices/dlls/basler_pylon``::

    import pylablib as pll
    pll.par["devices/dlls/basler_pylon"] = "path/to/dlls"
    from pylablib.devices import Basler
    cam = Basler.BaslerPylonCamera()



Connection
----------------------

The cameras are identified either by their index among the present cameras (starting from 0), or by their name. To get the list of all cameras, you can use pylon Viewer, or :func:`Basler.list_cameras<.pylon.list_cameras>`::

    >> from pylablib.devices import Basler
    >> Basler.list_cameras()
    [TCameraInfo(name='Emulation (0815-0000)', model='Emulation', serial='0815-0000', devclass='BaslerCamEmu', devversion='', vendor='Basler', friendly_name='Basler Emulation (0815-0000)', user_name='', props={'DeviceFactory': 'CamEmu/BaslerCamEmu 7.1.0.19126', 'InterfaceID': 'DefaultInterface', 'TLType': 'CamEmu'})]
    >> cam = Basler.BaslerPylonCamera()  # by default, connect to the first available camera
    >> cam.close()
    >> cam = Basler.BaslerPylonCamera(name="Emulation (0815-0000)")
    >> cam.close()


Operation
------------------------

The operation of these cameras is relatively standard. They support all the standard methods for dealing with ROI, starting and stopping acquisition, and operating the frame reading loop. The SDK also provides a universal interface for getting and setting various :ref:`camera attributes <cameras_basics_attributes>` using their name. You can use :meth:`.BaslerPylonCamera.get_attribute_value` and :meth:`.BaslerPylonCamera.set_attribute_value` for that, as well as ``.cav`` attribute which gives a dictionary-like access::

    >> cam = Basler.BaslerPylonCamera()
    >> cam.get_attribute_value("StatusInformation/AcqInProgress")  # check if the camera is acquiring
    0
    >> cam.set_attribute_value("Width", 512)  # set the ROI width to 512px
    >> cam.cav["Width"]  # get the exposure; could also use cam.get_attribute_value("Width")
    512

To see all available attributes, you can call :meth:`.BaslerPylonCamera.get_all_attributes` to get a dictionary with attribute objects, and :meth:`.BaslerPylonCamera.get_all_attribute_values` to get the dictionary of attribute values. The attribute objects provide additional information: attribute kind (integer, enum, string, etc.), range (either numerical range, or selection of values for enum attributes), description string, etc.::

    >> cam = Basler.BaslerPylonCamera()
    >> attr = cam.get_attribute("Width")
    >> attr.description
    'This value sets the width of the area of interest in pixels.'
    >> attr.writable
    True
    >> (attr.min, attr.max)
    (1, 4096)

Since these properties vary a lot between different cameras, it is challenging to write a universal class covering a large range of cameras. Hence, currently the universal class only has the basic camera parameter control such as ROI (without binning), acquisition status, and exposure (if present). For many specific cameras you might need to explore the attributes tree (either using the Python class and, e.g., a console, or via pylon Viewer) and operate them directly in your code.


Known issues
--------------------

- Currently only the basic unpacked monochrome pixel formats are supported: ``Mono8``, ``Mono10``, ``Mono12``, ``Mono16``, and ``Mono32``. The reason is that even nominally well-defined types (e.g., ``Mono12Packed``) have different formats for different cameras. Currently any unsupported format will raise an error on readout by default. It it still possible to read these out as raw frame data in the form of 1D or 2D numpy ``'u1'`` array by enabling raw frame readout using :meth:`.BaslerPylonCamera.enable_raw_readout` method::

    >> cam = Basler.BaslerPylonCamera()
    >> cam.get_detector_size()  # 1024px x 1024px frame
    (1024, 1024)
    >> cam.set_attribute_value("PixelFormat", "BGRA8Packed")  # unsupported format
    >> cam.snap().shape
    ...
    BaslerError: pixel format BGRA8Packed is not supported
    >> cam.enable_raw_readout("frame")  # frame data is returned as a flat array
    >> cam.snap().shape  # 1024 * 1024 * 4 = 4194304 bytes
    (1, 4194304)