.. _cameras_photonfocus:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`.

Photon Focus pfcam interface
============================

Photon Focus CameraLink cameras transfer their data to the PC using frame grabbers (e.g., via :ref:`NI IMAQ <cameras_imaq>` or :ref:`Silicon Software <cameras_siso>` interfaces). Hence, the camera control is done through the serial port built into the CameraLink interface. However, the cameras use a closed binary protocol, so all the control is done through the pfcam library provided by Photon Focus. It relies on the libraries exposed by the frame grabber manufacturers (e.g., the standard ``cl*serial.dll``) to communicate with the camera directly, meaning that the pfcam user simply calls its method, and all the communication happens behind the scenes.

In principle, pfcam can work with any frame grabber. Because of that, there are two different kinds of classes for this camera. To start with, there is :class:`.PhotonFocus.IPhotonFocusCamera<.PhotonFocus.IPhotonFocusCamera>`, which provides interface for addressing camera properties, but can not handle actual frame acquisition. Using this class directly leads to errors in any frame data related methods (e.g., ``wait_for_frame``, or ``read_multiple_images``), and it is mostly intended to serve as a base class to be combined with the actual frame grabber. Two such combined classes are already provided: :class:`.PhotonFocus.PhotonFocusIMAQCamera<.PhotonFocus.PhotonFocusIMAQCamera>` for National Instruments frame grabbers using the :ref:`NI IMAQ <cameras_imaq>` interface, :class:`.PhotonFocus.PhotonFocusSiSoCamera<.PhotonFocus.PhotonFocusSiSoCamera>` for :ref:`Silicon Software <cameras_siso>` frame grabbers, and :class:`.PhotonFocus.PhotonFocusBitFlowCamera<.PhotonFocus.PhotonFocusBitFlowCamera>` for :ref:`BitFlow <cameras_bitflow>` frame grabbers. All classes are complete and ready to use. In addition to combining camera and frame grabber control, they also implement basic consistency support, such as automatic adjustment of frame grabber ROI and data transfer format.

Software requirements
-----------------------

These cameras require ``pfcam.dll``, which is installed with freely available (upon registration) `PFInstaller <https://www.photonfocus.com/support/software/>`__. In addition, this DLL requires ``comdll.dll`` and the DLLs referring to a particular camera, e.g., ``mv_d1024e_160.dll``. After installation, the path to the DLLs (all located by default in ``Photonfocus/PFRemote/bin`` folder in ``Program Files``) is automatically added to system ``PATH`` variable, which is one of the places where pylablib looks for it by default. If the DLLs are located elsewhere, the path can be specified using the library parameter ``devices/dlls/pfcam``::

    import pylablib as pll
    pll.par["devices/dlls/pfcam"] = "path/to/dlls"
    from pylablib.devices import PhotonFocus
    cam = PhotonFocus.PhotonFocusIMAQCamera()


Connection
-----------------------

The camera class requires two pieces of information. First is the frame grabber interface connection, e.g., NI IMAQ interface name (e.g., ``"img0"``) identified as described in the :ref:`NI IMAQ <cameras_imaq>` documentation, or Silicon Software board and applet described in :ref:`Silicon Software <cameras_siso>` documentation. The second piece of information is the pfcam port, which is either a number starting from zero indexing the port in the ports list, or a tuple ``(manufacturer, port)``, e.g., ``("National Instruments", "port0")``. To list all of the connected pfcam-compatible cameras, you can use the PFRemote software (the interface number is given in parentheses after every connection option in the list) or run :func:`.PhotonFocus.list_cameras`::

    >> from pylablib.devices import PhotonFocus, IMAQ
    >> IMAQ.list_cameras()  # get all IMAQ frame grabber devices
    ['img0.iid']
    >> PhotonFocus.list_cameras()  # by default, get only the ports which support pfcam interface
    [(1, TCameraInfo(manufacturer='National Instruments', port='port0', version=5, type=0))]
    >> cam = PhotonFocus.PhotonFocus.PhotonFocusIMAQCamera(imaq_name="img0.iid", pfcam_port=("National Instruments", "port0"))
    >> cam.close()
    >> cam = PhotonFocus.PhotonFocus.PhotonFocusIMAQCamera(imaq_name="img0.iid", pfcam_port=1)  # same effect as above
    >> cam.close()


Operation
------------------------

The operation of these cameras is relatively standard. They support all the standard methods for dealing with ROI and exposure, starting and stopping acquisition, and operating the frame reading loop. However, there's a couple of differences from the standard libraries worth highlighting:

    - The SDK also provides a universal interface for getting and setting various :ref:`camera attributes <cameras_basics_attributes>` (called "properties" in the documentation) using their name. You can use :meth:`.IPhotonFocusCamera.get_attribute_value` and :meth:`.IPhotonFocusCamera.set_attribute_value` for that, as well as ``.cav`` attribute which gives a dictionary-like access::

        >> cam = PhotonFocus.PhotonFocusIMAQCamera()
        >> cam.get_attribute_value("Window/W")  # get the ROI width
        256
        >> cam.set_attribute_value("ExposureTime", 0.1)  # set the exposure to 100ms
        >> cam.cav["ExposureTime"]  # get the exposure; could also use cam.get_attribute_value("ExposureTime")
        0.1

      Some values (e.g., ``Window.Max`` or ``Reset``) serve as commands; these can be invoked using :meth:`.PhotonFocusIMAQCamera.call_command` method. To see all available attributes, you can call :meth:`.IPhotonFocusCamera.get_all_attributes` to get a dictionary with attribute objects, and :meth:`.IPhotonFocusCamera.get_all_attribute_values` to get the dictionary of attribute values. The attribute objects provide additional information: attribute range, step, and units::

        >> cam = PhotonFocus.PhotonFocusIMAQCamera()
        >> attr = cam.get_attribute("Window/W")
        >> attr.writable
        True
        >> (attr.min, attr.max)
        (16, 1024)

    - :class:`.PhotonFocus.PhotonFocusIMAQCamera` supports all of :class:`.IMAQ.IMAQCamera` features, such as trigger control and fast buffer acquisition. Some methods have been modified to make them more convenient: e.g., :meth:`.PhotonFocusIMAQCamera.set_roi` method sets the camera ROI and automatically adjusts the frame grabber ROI to match.
    - Same is true for :class:`.PhotonFocus.PhotonFocusSiSoCamera`, which, e.g., provides access to all of the frame grabber variables.
    - The camera supports a status line, which replaces the bottom one or two rows of the frame with encoded frame-related data such as frame number and timestamp. You can use :func:`.PhotonFocus.get_status_lines` function to identify and extract the data in the status lines from the supplied frames. In addition, you can use :func:`.PhotonFocus.remove_status_line` to remove the status lines in several possible ways: zeroing out, masking with the previous frame, cutting off entirely, etc.
    - If several PhotonFocus cameras are connected, you need to correctly associate different PFCam ports with the corresponding frame grabbers. To do that, you can use the function :func:`.PhotonFocus.check_grabber_association`.