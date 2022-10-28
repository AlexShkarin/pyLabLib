.. _cameras_mightex:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`

Mightex cameras interface
===========================

Mightex manufactures a set of USB2 and USB3-interfaced cameras with several somewhat different APIs. Currently only S-series cameras are implemented and tested.

The code is located in :mod:`pylablib.devices.Mightex`, and the main camera class is :class:`pylablib.devices.Mightex.MightexSSeriesCamera<.MightexSSeries.MightexSSeriesCamera>`.

Software requirements
----------------------

These cameras require ``MT_USBCamera_SDK_DS.dll`` and accompanying ``MtUsbLib.dll``, which can be obtained in the freely available `S-series camera software package <https://www.mightexsystems.com/product/s-series-ultra-compact-usb2-0-color-3mp-cmos-cameras/>`__ (the current latest version is from `2019.01.04 <https://mightex.wpenginepowered.com/wp-content/uploads/2019/04/Mightex_SCX_CDROM_20190104.zip>`__). This software does not require installation, and the required DLLs are contained in the ``DirectShow/MightexClassicCameraEngine`` folder withing the archive (do not confuse them with the regular ``MT_USBCamera_SDK.dll`` library, which is similar, but has some downsides regarding threading). Since these DLLs are not registered anywhere OS-wide, you should either specify them using the library parameter ``devices/dlls/mightex_sseries`` (both the containing folder path and the direct file path work), or copy the two DLL files to the folder containing your script::

    import pylablib as pll
    pll.par["devices/dlls/mightex_sseries"] = "path/to/dlls"
    from pylablib.devices import Mightex
    cam = Mightex.MightexSSeriesCamera()



Connection
----------------------

The cameras are identified by their index among the present cameras (starting from 1). To get the list of all cameras, you can use :func:`Mightex.list_cameras_s<.MightexSSeries.list_cameras>`::

    >> import pylablib as pll
    >> pll.par["devices/dlls/mightex_sseries"] = "path/to/dlls"
    >> from pylablib.devices import Mightex
    >> Mightex.list_cameras_s()
    [TCameraInfo(idx=1, model='SCE-B013-U', serial='13-160000-001')]
    >> cam = Mightex.MightexSSeriesCamera()  # by default, connect to the camera with index 1
    >> cam.close()


Operation
------------------------

The operation of these cameras is relatively standard. They support all the standard methods for dealing with ROI, starting and stopping acquisition, and operating the frame reading loop. However, there's a couple of differences from the standard libraries worth highlighting:

    - The multi-camera support from the SDK is fairly poor, e.g., only a single OS process can communicate with cameras (even if different processes try to access different cameras), and several cameras are always polled in sequence, meaning that the slowest camera determines the overall frame rate. Therefore, only the single camera operation is supported, although one can still select specific camera if several are connected to the same PC.
    - In some cases ROIs with extreme aspect ratios (e.g., ``32x1024`` px) can freeze the camera, such that it only start operating again after the software restart. Therefore, there should be generally be avoided.
    - Colored cameras are in principle supported, but the returned image is not debayered, meaning that it is still a monochrome image with different pixels within ``2x2`` sub-squares corresponding to different colors.