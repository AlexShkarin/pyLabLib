.. _cameras_pco_sc2:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`

PCO SC2 cameras interface
=========================

SC2 is the interface used with PCO cameras. It has been tested with pco.edge cameras with CLHS and regular CameraLink interfaces, and with pco.pixelfly usb cameras. A detailed description of the interface is given in the `manual <https://www.pco.de/fileadmin/fileadmin/user_upload/pco-manuals/pco.sdk_manual.pdf>`__.

The code is located in :mod:`pylablib.devices.PCO`, and the main camera class is :class:`pylablib.devices.PCO.PCOSC2Camera<.SC2.PCOSC2Camera>`.

Software requirements
-----------------------

These cameras require ``SC2_Cam.dll``, which is installed with the freely available `pco.camware <https://www.pco.de/software/camera-control-software/pcocamware/>`__ and `pco.sdk <https://www.pco.de/software/development-tools/pcosdk/>`__ tools. By default, the library searches for DLLs in ``Digital Camera Toolbox/Camware4`` and ``PCO Digital Camera Toolbox/pco.sdk/bin`` folder in ``Program Files`` folder (or ``Program files (x86)``, if 32-bit version of Python is running), as well as in the folder containing the script. If the DLLs are located elsewhere, the path can be specified using the library parameter ``devices/dlls/pco_sc2``::

    import pylablib as pll
    pll.par["devices/dlls/pco_sc2"] = "path/to/dlls"
    from pylablib.devices import PCO
    cam = PCO.PCOSC2Camera()


Connection
-----------------------

The cameras are identified by their index, starting from zero, and, possibly, by their interface. To get the total number of connected cameras, you can run :func:`PCO.get_cameras_number<.SC2.get_cameras_number>`::

    >> from pylablib.devices import PCO
    >> PCO.get_cameras_number()
    2
    >> cam1 = PCO.PCOSC2Camera(idx=0)
    >> cam2 = PCO.PCOSC2Camera(idx=1)
    >> cam1.close()
    >> cam2.close()


Operation
------------------------

The operation of these cameras is relatively standard. They support all the standard methods for dealing with ROI and exposure, starting and stopping acquisition, and operating the frame reading loop. The class also provides read-access to all of the relevant camera data using :meth:`.PCOSC2Camera.get_full_camera_data`. This method returns data in the internal manufacturer format; to interpret it, you should consult the `manual <https://www.pco.de/fileadmin/fileadmin/user_upload/pco-manuals/pco.sdk_manual.pdf>`__.


Known issues
--------------------

- Some cameras support only ROIs which are symmetric with respect to vertical flip. In other words, if the camera detector has vertical size of 2160px, the vertical ROI should always have the form ``(x0, 2160-x0)``. It is still possible to set non-symmetric ROI, but it is achieved by the software clipping, while the camera still reads out the smallest symmetric ROI contained the selected one. As a result, the readout time for the same ROI size strongly depends on the ROI position. For example, while vertical ROI of ``(0, 8)`` has only 8 pixel rows, it is not symmetric, and requires reading the whole frame; hence, it will be as slow as the full-frame acquisition. On the other hand, ROI of ``(1076, 1084)`` is symmetric, so the camera does read out only 8 rows. This results in vastly faster readout time. You can use :meth:`.PCOSC2Camera.requires_symmetric_roi` to check if the symmetric ROI is required.