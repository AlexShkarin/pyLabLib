.. _cameras_bitflow:

.. note::
    General camera communication concepts are described on the corresponding :ref:`page <cameras_basics>`

BitFlow Axion frame grabbers interface
======================================

BitFlow manufacturers several kinds of camera interface cards, including CameraLink. Currently, only newer CameraLink Axion family is supported. It has been tested with NI BitFlow Axion 1xB frame grabbers together with PhotonFocus MV-D1024E camera.

The code is located in :mod:`pylablib.devices.BitFlow`, and the main camera class is :class:`pylablib.devices.BitFlow.BitFlowCamera<.BitFlow.BitFlowCamera>`.

Software requirements
-----------------------

This interfaces requires two pieces of software, both freely available on the `BitFlow website <https://www.bitflow.com/current-downloads/>`__. First, you need `BitFlow SDK 6.5 <https://www.bitflow.com/downloads/bfsdk65.zip>`__, which also includes all the necessary drivers. The free version does not provide any headers and documentation to the DLLs, so yo use it you also need to install the manufacturer-provided Python packages, either for `Python 3.6.6 <https://www.bitflow.com/downloads/BFPython36_Release.zip>`__, or for `Python 3.8.10 <https://www.bitflow.com/downloads/BFPython38_Release.zip>`__. Note that only these two Python versions are officially supported.

After installation, the DLL locations are automatically added to the ``PATH`` environment variable. To facilitate proper package import and DLL loading on Python 3.8, it is recommended to install BitFlow SDK into its default library, or at least leave ``BitFlow`` in the folder name.

Connection
-----------------------

The cameras are identified by their index, starting from 0. To get the list of all cameras, you can use :func:`.BitFlow.list_cameras`::

    >> from pylablib.devices import BitFlow
    >> cam = BitFlow.BitFlowCamera(bitflow_idx=0)
    >> cam.close()


Operation
------------------------

Unlike most camera classes, the frame grabber interface only deals with the frame transfer between the camera and the PC over the CameraLink interface. Therefore, in can not directly control camera parameters such as exposure, frame rate, triggering, ROI, etc. Some similar-looking parameters are still present, but they have a different meaning:

    - ROI is defined within the transferred image, whose size itself is determined by the camera ROI. Hence, e.g., if the camera chip is 1024x1024px and its roi is 512x512, then the frame grabber ROI can go only up to 512x512. Any attempts to set it higher result in the frozen acquisition, as the frame grabber expects a larger frame than it receives, and waits forever to get the rest.


Fast buffer readout and frames merging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At high frame rates (above ~10kFPS) dealing with each frame individually becomes too slow for Python. Hence, there is an option to read out and process frames in larger 'chunks', which are 3D numpy arrays with the first axis enumerating the frame index. This approach leverages the ability to store several frame buffers in the contiguous memory locations (resulting in a single 3D array), and it essentially eliminates the overhead for dealing with multiple frames at high frame rates, as long as the total data rate is manageable (typically below 600Mb/s).

This option can be accessed by calling using :meth:`.BitFlowCamera.set_frame_format` method to set frames format to ``"chunks"``. In this case, instead of a list of individual frames (which is the standard behavior), the method returns list of chunks of varying size, which contain several consecutive frames.

On top of that, due to unavoidable Python loop required by the BitFlow Python interface, the frame rate is usually limited to about 2-4kFPS. However, there is a way to overcome this by merging ``n`` consecutive frames to a single "super-frame" with ``n`` times larger height. This merging can be specified by ``frame_merge`` parameter in the :meth:`.BitFlowCamera.setup_acquisition` or :meth:`.BitFlowCamera.start_acquisition` methods (by default it is 1, meaning no merging). Adjusting the frame grabber ROI and splitting the resulting files is done transparently for the user; the only difference is that frames always arrive in batches, e.g., with ``frame_merge=10`` and 10FPS rate the frames will arrive once a second in batches of 10. Therefore, it makes sense to adjust the merging to keep the "merged" frame rate high enough for real-time operations but lower than the 2kFPS limit (e.g., around 100FPS).


Communication with the camera and camera files
--------------------------------------------------

The frame grabber needs some basic information about the camera: sensor size, bit depth, data transfer format, timeouts, aux lines mapping, etc. This information is contained in the so-called camera files, which for Axion cameras have ``.bfml`` extension. These files can be assigned to cameras using ``SysReg`` utility located in the ``Bin64`` folder of your BitFlow installation (by default, ``C:\BitFlow SDK 6.5\Bin64``).

In addition, due to limitations of the provided Python interfaces, some operations such as changing ROI and bitness can only be done by altering the camera file. Hence, there is an option to create a temporary camera file and alter it to control these parameters. However, it needs the original camera file to serve as a template (this original file is only used as source and not modified). Since there is no possibility to get a path to this file within the Python interface, it should be provided using ``camfile`` parameter upon creation.


Known issues
--------------------

- As mentioned above, ROI is defined within a frame transferred by the camera. Hence, if it includes pixels with positions outside of the transferred frame, the acquisition will time out. For example, suppose the camera sensor is 1024x1024px, and the *camera* ROI is selected to be central 512x512 region. As far as the frame grabber is concerned, now the camera sensor size is 512x512px. Hence, if you try to set the same *frame grabber* ROI (i.e., 512x512 starting at 256,256), it will expect at least 768x768px frame. Since the frame is, actually, 512x512px, the acquisition will time out. The correct solution is to set frame grabber ROI from 0 to 512px on both axes. In general, it is a good idea to always follow this pattern: control ROI only on camera, and always set frame grabber ROI to cover the whole transfer frame.