.. _cameras_siso:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`

Silicon Software frame grabbers interface
=========================================

Silicon Software produces a range of frame grabbers, which can be used to control different cameras with a CameraLink interface. It has been tested with microEnable IV AD4-CL frame grabber together with PhotonFocus MV-D1024E camera.

The code is located in :mod:`pylablib.devices.SiliconSoftware`, and the main camera class is :class:`pylablib.devices.SiliconSoftware.SiliconSoftwareCamera<.fgrab.SiliconSoftwareCamera>`.

Software requirements
-----------------------

This interfaces requires ``fglib5.dll``, which is installed with the freely available (upon registration) `Silicon Software Runtime Environment <https://www.baslerweb.com/en/sales-support/downloads/software-downloads/#type=framegrabbersoftware;language=all;version=all;os=windows64bit>`__ (the newest version for 64-bit Windows is `5.7.0 <https://www.baslerweb.com/en/sales-support/downloads/software-downloads/complete-installation-for-windows-64bit-ver-5-7-0/>`__), which also includes all the necessary drivers. After installation, the path to the DLL (located by default in ``SiliconSoftware/Runtime5.7.0/bin`` folder in ``Program Files``) is automatically added to system ``PATH`` variable, which is one of the places where pylablib looks for it by default. If the DLL is located elsewhere, the path can be specified using the library parameter ``devices/dlls/sisofgrab``::

    import pylablib as pll
    pll.par["devices/dlls/sisofgrab"] = "path/to/dlls"
    from pylablib.devices import SiliconSoftware
    cam = SiliconSoftware.SiliconSoftwareCamera()


Connection
-----------------------

Figuring out the connection parameters is a multi-stage process. First, one must identify one of several boards. The boards can be identified using :func:`SiliconSoftware.list_boards<.fgrab.list_boards>` function. Second, one must select an applet. These provide different board readout modes and, for Advanced Applets, various post-processing capabilities. These applets can be identified using :func:`SiliconSoftware.list_applets<.fgrab.list_applets>` method, or directly from the Silicon Software RT microDisplay software supplied with the runtime. The choice depends on the color mode (color vs. gray-scale and different bitness), readout mode (area or line), and camera connection (single, double, or quad). Finally, depending on the board and the camera connection, one of several ports must be selected. For example, if the frame grabber has two connectors, but the camera only uses a single interface, then the double camera applet (e.g., ``DualAreaGray16``) must be selected, and the port should specify the board connector (0 for ``A``, 1 for ``B``)::

    >> from pylablib.devices import SiliconSoftware
    >> SiliconSoftware.list_boards()  # first list the connected boards
    [TBoardInfo(name='mE4AD4-CL', full_name='microEnable IV AD4-CL')]
    >> SiliconSoftware.list_applets(0)  # list all applets on the first board
    [ ...,
    TAppletInfo(name='DualAreaGray16', file='DualAreaGray16.dll'),
    ... ]
    >> cam = SiliconSoftware.SiliconSoftwareCamera(0, 'DualAreaGray16')  # connect to the first board (port 0 by default)
    >> cam.close()

Note that currently the code is organized in such a way, that only one port on a single board can be in use at one time.

Operation
------------------------

Unlike most camera classes, the frame grabber interface only deals with the frame transfer between the camera and the PC over the CameraLink interface. Therefore, in can not directly control camera parameters such as exposure, frame rate, triggering, ROI, etc. Some similar-looking parameters are still present, but they have a different meaning:

    - External trigger controls frame *transfer*, not frame *acquisition*, which is defined by the camera. By default, when the internal frame grabber trigger is used, the frame grabber transfer rate is synchronized to the camera, so every frame gets transferred. However, if the external transfer trigger is used and it is out of sync with the camera, it can result in duplicate or missing frames.
    - ROI is defined within the transferred image, whose size itself is determined by the camera ROI. Hence, e.g., if the camera chip is 1024x1024px and its roi is 512x512, then the frame grabber ROI can go only up to 512x512. Any attempts to set it higher result in frame being misshapen or having random data outside of the image area.

The SDK also provides a universal interface for getting and setting various :ref:`attributes <cameras_basics_attributes>` using their name. You can use :meth:`.SiliconSoftwareCamera.get_grabber_attribute_value` and :meth:`.SiliconSoftwareCamera.set_grabber_attribute_value` for that, as well as ``.gav`` attribute which gives a dictionary-like access::

    >> cam = SiliconSoftware.SiliconSoftwareCamera()
    >> cam.get_grabber_attribute_value("CAMERA_LINK_CAMTYP")  # get the camera data format
    'FG_CL_SINGLETAP_8_BIT'
    >> cam.set_grabber_attribute_value("WIDTH", 512)  # set the readout frame width to 512px
    >> cam.gav["WIDTH"]  # get the width; could also use cam.get_grabber_attribute_value("WIDTH")
    512

To see all available attributes, you can call :meth:`.SiliconSoftwareCamera.get_all_grabber_attributes` to get a dictionary with attribute objects, and :meth:`.SiliconSoftwareCamera.get_all_grabber_attribute_values` to get the dictionary of attribute values. The attribute objects provide additional information: attribute kind (integer, string, etc.), range (either numerical range, or selection of values for enum attributes), description string, etc.::

    >> cam = SiliconSoftware.SiliconSoftwareCamera()
    >> attr = cam.get_grabber_attribute("BITALIGNMENT")
    >> attr.values
    {1: 'FG_LEFT_ALIGNED', 0: 'FG_RIGHT_ALIGNED'}

The parameter can also be inspected in the Silicon Software RT microDisplay software.

Fast buffer readout mode
~~~~~~~~~~~~~~~~~~~~~~~~

At high frame rates (above ~10kFPS) dealing with each frame individually becomes too slow for Python. Hence, there is an option to read out and process frames in larger 'chunks', which are 3D numpy arrays with the first axis enumerating the frame index. This approach leverages the ability to store several frame buffers in the contiguous memory locations (resulting in a single 3D array), and it essentially eliminates the overhead for dealing with multiple frames at high frame rates, as long as the total data rate is manageable (typically below 600Mb/s).

This option can be accessed by calling using :meth:`.SiliconSoftwareCamera.set_frame_format` method to set frames format to ``"chunks"`` (former way of supplying ``fastbuff=True`` in :meth:`.SiliconSoftwareCamera.read_multiple_images` is now deprecated). In this case, instead of a list of individual frames (which is the standard behavior), the method returns list of chunks about 1Mb in size, which contain several consecutive frames.


Communication with the camera
--------------------------------------------------

The frame grabber needs some basic information about the camera: sensor size, bit depth, data transfer format, timeouts, aux lines mapping. This information can be specified using the grabber attributes. The most important transfer parameters are the number of taps and the bitness of the transferred data, which can be set up using :meth:`.SiliconSoftwareCamera.setup_camlink_pixel_format`. The values for this parameters can usually be obtained from the camera manuals.


Known issues
--------------------

- The maximal frame rate is limited for some boards (at least for the tested microEnable IV AD4-CL board) by about 20kFPS. It seems to be relatively independent of the frame size, i.e., it is not the data transfer rate issue. One possible way to get around it is to use line readout applet, e.g., ``DualLineGray16``, and set the frame height to be the integer multiple of the camera frame. This will combine several camera frames into a single frame-grabber frame, effectively lowering the frame rate at avoiding the issue. However, this sometimes leads to incorrect frame splitting: the top line of the "combined" frame does not coincide with the top line of the original camera frame, so all frames are shifted cyclically by some number of rows. Hence, it might require some post-processing with frames merging and re-splitting.
- As mentioned above, ROI is defined within a frame transferred by the camera. Therefore, if it includes pixels with positions outside of the transferred frame, the acquisition will be faulty. For example, suppose the camera sensor is 1024x1024px, and the *camera* ROI is selected to be central 512x512 region. As far as the frame grabber is concerned, now the camera sensor size is 512x512px. Hence, if you try to set the same *frame grabber* ROI (i.e., 512x512 starting at 256,256), it will expect 768x768px frame. Since the frame is, actually, 512x512px, the returned frame will partially contain random data. The correct solution is to set frame grabber ROI from 0 to 512px on both axes. In general, it is a good idea to always follow this pattern: control ROI only on camera, and always set frame grabber ROI to cover the whole transfer frame.