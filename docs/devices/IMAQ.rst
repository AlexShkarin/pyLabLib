.. _cameras_imaq:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras>`

IMAQ frame grabbers interface
===============================

IMAQ is the interface from National Instruments, which is used in a variety of frame grabber. It has been tested with NI PCI-1430 and PCI-1433 frame grabbers together with PhotonFocus MV-D1024E camera.

The code is located in :mod:`pylablib.devices.IMAQ`, and the main camera class is :mod:`pylablib.devices.IMAQ.IMAQCamera`.

DLL requirements
-----------------------

This interfaces requires ``imaq.dll``, which is installed with the freely available `Vision Acquisition Software <https://www.ni.com/en-us/support/downloads/drivers/download.vision-acquisition-software.html>`_, which also includes all the necessary drivers. After installation, the DLL is automatically added to the ``System32`` folder, where pylablib looks for it by default. If the DLL is located elsewhere, the path can be specified using the library parameter ``devices/dlls/niimaq``::

    import pylablib as pll
    pll.par["devices/dlls/niimaq"] = "path/to/dlls"
    from pylablib.devices import IMAQ
    cam = IMAQ.IMAQCamera()


Connection
-----------------------

The cameras are identified by their name, which usually looks like ``"img0"``. To get the list of all cameras, you can use NI MAX (Measurement and Automation Explorer), or :func:`IMAQ.list_cameras`::

    >> from pylablib.devices import IMAQ
    >> IMAQ.list_cameras()
    [`img0`, `img1`]
    >> cam1 = IMAQ.IMAQCamera('img0')
    >> cam2 = IMAQ.IMAQCamera('img1')
    >> cam1.close()
    >> cam2.close()


Operation
------------------------

Unlike most cameras, the frame grabber interface only deals with the frame transfer between the camera and the PC over the CameraLink interface. Therefore, in can not directly control camera parameters such as exposure, frame rate, triggering, ROI, etc. Some similar-looking parameters are still present, but they have a different meaning:

    - External trigger controls frame *transfer*, not frame *acquisition*, which is controlled by the camera. By default (internal trigger), this rate is controller by the camera, so every frame gets transferred. However, is the external trigger is used and it is out of sync with the camera, it can result in duplicate or missing frames.
    - ROI is defined withing the transferred image, whose size itself is determined by the camera ROI. Hence, e.g., if the camera chip is 1024x1024px and its roi is 512x512, then the frame grabber ROI can go only up to 512x512. Any attempts to set it higher result in the frozen acquisition, as the frame grabber expects a larger frame than it receives, and waits forever to get the rest.

The SDK also provides a universal interface for getting and setting various camera attributes using their name. You can use :meth:`IMAQCamera.get_attribute_value` and :meth:`IMAQCamera.set_attribute_value` for that::

    >> cam = IMAQ.IMAQCamera()
    >> cam.get_value("FRAMEWAIT_MSEC")  # frame read request timeout
    1000

To get a all available attributes as a dictionary, you can call :meth:`IMAQCamera.get_all_attributes`. Their meaning, as well as descriptions of trigger modes and other settings, is explained in the manual supplied with the `Vision Acquisition Software <https://www.ni.com/en-us/support/downloads/drivers/download.vision-acquisition-software.html>`_.


Communication with the camera and camera files
--------------------------------------------------

The frame grabber needs some basic information about the camera (sensor size, bit depth, timeouts, aux lines mapping), which are contained in the camera files. These files can be assigned to cameras in the NI MAX, and are usually supplied by NI or by the camera manufacturer. In addition, NI MAX allows one to adjust some settings within these files, which are read-only within the NI IMAQ software. These include frame timeout and camera bit depth.

The communication with the camera itself greatly varies between different cameras. Some will have additional connection to control the parameters. However, most use serial communication built into the CameraLink interface. This communication can be set up with :meth:`IMAQCamera.setup_serial_params` and used via :meth:`IMAQCamera.serial_read` and  :meth:`IMAQCamera.serial_write`. The communication protocols are camera-dependent. Yet some other cameras (e.g., Photon Focus) use proprietary communication protocol. In this case, the provide their own DLLs, which independently use NI-provided DLLs for serial communication (most notably, ``clallserial.dll``). In this case, one needs to maintain two independent connections: one directly to the NI frame grabber to obtain the frame data, and one to the manufacturer library to control the camera. This is the way it is implemented in PhotonFocus camera interface.


Known issues
--------------------

- Sometimes when the acquisition is stopped and restarted without being cleared, the acquired frame counter does not refresh. This might show up as the software not reporting any new frames. It has been tracked down to a very low (~1ms) frame read timeout. Hence, it is recommended to keep this timeout at least at 500ms.
- If you are unable to access full camera sensor size, check the camera file (it can be opened in the text editor). ``MaxImageSize`` parameter defines the maximal allowed image size, and it should be equal to the camera sensor size.
- Same goes for bitness. If the camera bitness is higher than set up in the frame grabber, a single camera pixel gets treated as several pixels by the frame grabber, typically resulting in 1px-wide lines on the image. In the opposite case, the frame grabber expects for bytes than the camera sends, it never receives the full frame, and the acquisition times out.
- Keep in mind that as long as the frame grabber is accessed in NI MAX, it is blocked from use in any other software. Hence, you need to close NI MAX before running your code.
- As mentioned above, ROI is defined within a frame transferred by the camera. Hence, if it includes pixels with positions outside of the transferred frame, the acquisition will time out. For example, suppose the camera sensor is 1024x1024px, and the *camera* ROI is selected to be central 512x512 region. As far as the frame grabber is concerned, now the camera sensor size is 512x512px. Hence, if you try to set the same *frame grabber* ROI in the (i.e., 512x512 starting at 256,256), it will expect 768x768px frame. Since the frame is, actually, 512x512px, the acquisition will time out. The correct solution is to set frame grabber ROI from 0 to 512px on both axes. In general, it is a good idea to always follow this pattern: control ROI only on camera, and always set frame grabber ROI to cover the whole transfer frame.