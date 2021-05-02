.. _cameras_photonfocus:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`.

Photon Focus pfcam interface
============================

Photon Focus cameras transfer their data to the PC using frame grabbers (e.g., via :ref:`NI IMAQ <cameras_imaq>` interface). Hence, the camera control is done through the serial port built into the CameraLink interface. However, the cameras use a closed binary protocol, so one needs to use a pfcam library provided by Photon Focus. It relies on the libraries exposed by the frame grabber manufacturers (e.g., the standard ``cl*serial.dll``) to communicate with the camera directly, meaning that the pfcam user simply calls its method, and all the communication happens behind the scenes.

In principle, pfcam can work with any frame grabber. However, so far it has only been developed and tested in conjunction with National Instruments frame grabbers using the :ref:`NI IMAQ <cameras_imaq>` interface. Hence, the main camera class :class:`pylablib.devices.PhotonFocus.PhotonFocusIMAQCamera<.PhotonFocus.PhotonFocusIMAQCamera>` already incorporates IMAQ functionality. This makes it easier to use, but restricts the use of pfcam to IMAQ-compatible frame grabbers.

Software requirements
-----------------------

These cameras require ``pfcam.dll``, which is installed with `PFInstaller <https://www.photonfocus.com/support/software/>`__, which is freely available, but requires a registration. After installation, the DLL is automatically added to the ``System32`` folder, where pylablib looks for it by default. If the DLL is located elsewhere, the path can be specified using the library parameter ``devices/dlls/pfcam``::

    import pylablib as pll
    pll.par["devices/dlls/pfcam"] = "path/to/dlls"
    from pylablib.devices import PhotonFocus
    cam = PhotonFocus.PhotonFocusIMAQCamera()


Connection
-----------------------

The camera class requires two pieces of information. First is the NI IMAQ interface name (e.g., ``"img0"``), identified as described in the :ref:`NI IMAQ <cameras_imaq>` documentation. The second is the pfcam port, which is a number starting from zero. To list all of the connected pfcam-compatible cameras, you can run :func:`.PhotonFocus.list_cameras`:

    >> from pylablib.devices import PhotonFocus, IMAQ
    >> IMAQ.list_cameras()  # get all IMAQ frame grabber devices
    ['img0.iid']
    >> PhotonFocus.list_cameras()  # by default, get only the ports which support pfcam interface
    [(0, TCameraInfo(manufacturer='National Instruments', port='port0', version=5, type=0))]
    >> cam = PhotonFocus.PhotonFocus.PhotonFocusIMAQCamera(imaq_name="img0.iid", pfcam_port=0)
    >> cam.close()


Operation
------------------------

The operation of these cameras is relatively standard. They support all the standard methods for dealing with ROI and exposure, starting and stopping acquisition, and operating the frame reading loop. However, there's a couple of differences from the standard libraries worth highlighting:

    - The SDK also provides a universal interface for getting and setting various camera properties using their name. You can use :meth:`.PhotonFocusIMAQCamera.get_value` and :meth:`.PhotonFocusIMAQCamera.set_value` for that, as well as ``.v`` attribute which gives a dictionary-like access::

        >> cam = PhotonFocus.PhotonFocusIMAQCamera()
        >> cam.get_value("Window/W")  # get the ROI width
        256
        >> cam.set_value("ExposureTime", 0.1)  # set the exposure to 100ms
        >> cam.v["ExposureTime"]  # get the exposure; could also use cam.get_value("ExposureTime")
        0.1

      Some values (e.g., ``Window.Max`` or ``Reset``) serve as commands; these can be invoked using :meth:`.PhotonFocusIMAQCamera.call_command` method. To get values of all available properties, you can call :meth:`.PhotonFocusIMAQCamera.get_all_properties`. In addition, `PhotonFocusIMAQCamera.properties` is a dictionary of all camera properties presented as objects of class :class:`.PhotonFocus.PFCamProperty`. In addition to getting and setting property values, it also allows to query its type, range, and possible values (for enum properties).

    - Being a subclass of :class:`.IMAQ.IMAQCamera` class, it supports all of its features, such as trigger control and fast buffer acquisition. Some methods have been modified to make them more convenient: e.g., :meth:`.PhotonFocusIMAQCamera.set_roi` method sets the camera ROI and automatically adjusts the frame grabber ROI to match.
    - The camera supports a status line, which replaces the bottom one or two rows of the frame with the encoded frame-related data such as frame number and timestamp. You can use :func:`.PhotonFocus.get_status_lines` function to identify and extract the data in the status lines from the supplied frames. In addition, you can use :func:`.PhotonFocus.remove_status_line` to remove the status lines in several possible ways: zeroing out, masking with the previous frame, cutting off entirely, etc.