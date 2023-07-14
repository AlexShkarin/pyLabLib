.. _cameras_allvis:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`.

Allied Vision Bonito cameras
============================

Allied Vision manufactures a variety of cameras with different interfaces: USB, GigE, and CameraLink. Currently, only CameraLink Bonito cameras using NI IMAQ frame grabber are supported. It has been tested with Bonito CL-400B/C and NI IMAQ frame grabber.

The code is located in :mod:`pylablib.devices.AlliedVision`, and the main camera class is :class:`pylablib.devices.AlliedVision.BonitoIMAQCamera<.Bonito.BonitoIMAQCamera>`.

Software requirements
-----------------------

Since the camera control is done purely through the frame grabber interface, the requirements are the same as for generic :ref:`IMAQ cameras <cameras_imaq>`. However, the correct camera file still needs to be specified to determine the correct serial communication parameters (especially the termination character)


Connection
-----------------------

The cameras are identified by their name, which usually looks like ``"img0"``. To get the list of all cameras, you can use NI MAX (Measurement and Automation Explorer), or :func:`.IMAQ.list_cameras`::

    >> from pylablib.devices import IMAQ, AlliedVision
    >> IMAQ.list_cameras()
    ['img0']
    >> cam = AlliedVision.BonitoIMAQCamera('img0')
    >> cam.close()


Operation
------------------------

The operation of these cameras is relatively standard. They support all the standard methods for dealing with ROI and exposure, starting and stopping acquisition, and operating the frame reading loop. However, there's a couple of differences from the standard libraries worth highlighting:

    - :class:`.Bonito.BonitoIMAQCamera` supports all of :class:`.IMAQ.IMAQCamera` features, such as trigger control and fast buffer acquisition. Some methods have been modified to make them more convenient: e.g., :meth:`.Bonito.BonitoIMAQCamera.set_roi` method sets the camera ROI and automatically adjusts the frame grabber ROI to match.
    - Internally the camera only supports vertical ROI (number of rows), so the horizontal ROI is set via the frame grabber. This means that regardless of the horizontal ROI settings the whole rows are always transmitted between the camera and the frame grabber, so it does not affect, e.g., the maximal frame rate.
    - The camera supports a status line, which replaces the first 8 pixels in the upper row encoded frame number. You can use :func:`.AlliedVision.Bonito.get_status_lines` function to identify and extract the data in the status lines from the supplied frames. Note that due to the full row transfer mentioned earlier, the status line is only available if the horizontal ROI span starts from zero; otherwise, it will be partially or completely cut off.
    - You can use the function :func:`.AlliedVision.Bonito.check_grabber_association` to check if the given IMAQ camera is a Bonito model by sending several standard Bonito commands and checking replies.