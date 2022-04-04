.. _cameras_basics:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

Cameras control basics
======================================

Basic examples
--------------------------------------

Basic camera usage is fairly straightforward::

    from pylablib import Andor
    cam = Andor.AndorSDK3Camera()  # connect to the camera
    cam.set_exposure(10E-3)  # set 10ms exposure
    cam.set_roi(0,128,0,128)  # set 128x128px ROI in the upper left corner
    images = cam.grab(10)  # grab 10 frames
    cam.close()

In case you need to grab and process frames continuously, the example is a bit more complicated::

    with Andor.AndorSDK2Camera() as cam: # to close the camera automatically
        cam.start_acquisition()  # start acquisition (automatically sets it up as well)
        while True:  # acquisition loop
            cam.wait_for_frame()  # wait for the next available frame
            frame=cam.read_oldest_image()  # get the oldest image which hasn't been read yet
            # ... process frame ...

Some concepts are explained below in more detail.

Basic concepts
--------------------------------------

Frames buffer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In most cases, the frames acquired by the camera are first temporarily stored in the local camera and / or frame grabber memory, from which they are transferred to the PC RAM by the camera drivers. Afterwards, this memory is made available to all other applications. In principle, it should be enough to store only the most recent frame in RAM, and for the user software to continuously wait for a new frame, immediately read it from RAM and process it. However, such approach is very demanding to the user code: if the new frame is acquired before the previous one is processed or copied, then the RAM data is overwritten, and the old frame is lost. Hence, it is more practical to have a *buffer* of several most recently acquired frames to account for inevitable interruptions in the user wait-read-process loop caused by OS scheduling and by other jobs. In this case, the frames get lost only when the buffer is completely filled, and the oldest frames starts getting overwritten.

When using the camera classes provided by pylablib, you do not need to worry about setting up the buffer yourself, since it is done behind the scene either by the manufacturer's code or by the device class. However, it is important to keep in mind the existence of the buffer when setting up the acquisition, interpreting the buffer and acquired frames status, or identifying the skipped frames.

The size of the buffer can almost always be selected by the user. Typically it is a good idea to have at least 100ms worth of frames there, although, depending on the other jobs performed by the software, it can be larger.


Acquisition setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setting up an acquisition process might take a lot of time (up to 10s in more extreme cases). This happens mostly because of the buffer allocation and setting up internal API structures; initiating the acquisition process itself is fairly fast. Hence, it is useful to separate setting up / cleaning up and starting / stopping.

The first two procedures correspond to ``setup_acquisition`` and ``clear_acquisition`` method, which are slow, but rarely called. Usually, they only need to be invoked right after connecting to the camera, or when the acquired image size is changed (e.g., due to a change in binning or ROI). Since these methods deal with buffer allocation, in almost all cases they take a parameter specifying buffer size (typically called ``nframes``).

The other two procedures correspond to ``start_acquisition`` and ``stop_acquisition`` methods. These try to be as fast as possible, as they need to be called any time the acquisition is started or stopped, or when minor parameters (frame rate, exposure, trigger mode) are called.


Region of interest (ROI) and binning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most cameras allow the user to select only a part of the whole sensor for readout and transfer. Since the readout speed is usually the factor limiting the frame rate, selecting smaller ROI frequently lets you achieve higher frame rate. In addition, it also reduces the size of the frame buffer and the data transfer load. Same goes for binning: many cameras can combine values of several consecutive pixels in the same row or column (or both), which results in smaller images and, depending on the camera architecture, higher signal-to-noise ratio compared to binning in post-processing. Much less frequently you can set up subsampling instead of binning, which skips pixels instead of averaging them together.

Both operations depend very strongly on the exact hardware, so there are typically many associated restriction. The most common are minimal sizes in width and height, positions and sizes being factors of some power of 2 (up to 32 for some cameras), or equal binning for both axes. Device classes will typically round the ROI to the nearest allowed value. Furthermore, the scaling of the maximal frame rate with the ROI size is also hardware-dependent; for example, in many sCMOS chips readout speed only depends on the vertical extent, since the readout is done simultaneously for the whole row. In most cases, it takes some experiments to get a hang of the camera behavior.


Exposure and frame rate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Almost all scientific cameras let user change the exposure, typically in a wide range (down to sub-ms). Frequently they also allow to separately change the frame period (inverse of the frame rate). Usually (but not always) the minimal frame period is set by the exposure plus some readout time, which depends on the ROI and some additional parameters such as pixel clock or simultaneous readout mode. Usually exposure takes priority over the frame period, i.e., if the frame period is set too short, it is automatically adjusted. Notable exception from this rule is :ref:`Uc480 <cameras_uc480>` interface, where this dependence in reversed.


Triggering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usually the cameras will have several different options for triggering, i.e., choosing when to start acquiring a new frame or a new batch of frames. The default option is the internal trigger, which means that the internal timer generates trigger event at a constant rate (frame rate). Many cameras will also take an external trigger signal to synchronize acquisition to external events or other cameras. Typically, a rising edge from 0 to 5V on the input will initiate the frame acquisition, but more exotic options (different polarities or levels, exposure control with pulse width, line-readout trigger) can be present.




Application notes and examples
-------------------------------------------

Here we talk more practically about performing tasks common to most cameras.

Simple acquisition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Frame acquisition is, understandably, the most important part of the camera. Basic acquisition can be done without explicitly setting up the acquisition loop, simply by using :meth:`.ICamera.snap` and :meth:`.ICamera.grab` methods which, correspondingly, grab a single frame or a given number of frames::

    from pylablib import Andor
    cam = Andor.AndorSDK3Camera()  # connect to the camera
    img = cam.snap()  # grab a single frame
    images = cam.grab(10)  # grab 10 frames (return a list of frames)
    cam.close()

These allow for quick tests of whether the camera works properly, and for occasional frames acquisition. However, these methods have to start and stop acquisition every time they are called, which for some cameras can take about a second. Hence, if continuous acquisition and high frame rate are required, you would need to set up the acquisition loop.


Acquisition loop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A typical simple acquisition loop has already been shown above::

    # nframes=100 relates to the size of the frame buffer; the acquisition will continue indefinitely
    cam.setup_acquisition(mode="sequence", nframes=100)  # could be combined with start_acquisition, or kept separate
    cam.start_acquisition()
    while True:  # acquisition loop
        cam.wait_for_frame()  # wait for the next available frame
        frame = cam.read_oldest_image()  # get the oldest image which hasn't been read yet
        # ... process frame ...
        if time_to_stop:
            break
    cam.stop_acquisition()

It relies on 3 sets of methods. First, starting and stopping acquisition using ``start_acquisition`` and ``stop_acquisition``. As explained above, one also has an option to setup the acquisition first using ``setup_acquisition``, which makes the subsequent ``start_acquisition`` call faster. However, one can also supply the same setup parameters to ``start_acquisition`` method, which automatically sets up the acquisition if it is not set up yet, or if any parameters are different from the current ones.

Second are the methods for checking on the acquisition process. The method used above is ``wait_for_frame``, which by default waits until there is at least one unread frame in the buffer (i.e., it exits immediately if there is already a frame available). Its arguments modify this behavior by changing the point from which the new frame is acquired (e.g., from the current call), or the minimal required number of frames. Alternatively, there is a method ``get_new_images_range``, which returns a range of the frame indices which have been acquired but not read. This method allows for a quick check of a number of unread frames without pausing the acquisition.

Finally, there are methods for reading out the frames. The simplest method is ``read_oldest_image``, which return the oldest image which hasn't been read yet, and marks it as read. A more powerful is the ``read_multiple_images`` method, which can return a range of images (by default, all unread images). Both of these methods also take a ``peek`` argument, which allows one to read the frames without marking them as read.


Returned frame format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:meth:`.ICamera.read_multiple_images` method described above has several different formats for returning the frames, which can be controlled using :meth:`.ICamera.set_frame_format` and checked :meth:`.ICamera.get_frame_format`. The default format is ``"list"``, which returns a list of individual frames. The second possibility is ``"array"``, which returns a single 3D numpy array with all the frames. Finally, ``"chunks"`` returns a list of 3D arrays, each containing several consecutive frames.

While ``"chunks"`` format is the hardest to work with, it provides the best performance. First, it does not require any extra memory copies, which negatively affect performance at very high data rates, above ~1Gb/s. Second, it can combine multiple small frames together into a single array, which makes further processing faster, as it does require explicit Python loop over every frame. This usually becomes important at frames rates above ~10kFPS, where treating each frame as an individual 2D array leads to significant overhead.


Frame indexing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Different areas and libraries adopt different indexing convention for 2D arrays. The two most common ones are coordinate-like ``xy`` (the first index is the ``x`` coordinate, the second is ``y`` coordinate, and the origin is in the lower left corner) and matrix-like ``ij`` (the first index is row, the second index is column, the origin is int the upper right corner). Almost all cameras adopt the ``ij`` convention. The only exception is Andor SDK2, which uses similar row-column indexing, but counting from the bottom.

By default, the frames returned by the camera are indexed in the preferred convention, to reduce the overhead on re-indexing the frames. It is possible to check and change it using :meth:`.ICamera.get_image_indexing` and :meth:`.ICamera.set_image_indexing` methods::

    >> cam.set_roi(0,256,0,128)  # 256px horizontally, 128 vertically
    >> cam.snap().shape  # 128 rows, 256 columns
    (128, 256)
    >> cam.set_image_indexing("xyb")  # standard xy indexing, starting from the bottom
    >> cam.snap().shape
    (256, 128)


ROI, detector size and frame shape
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both ROI and binning are controlled by one pair of methods ``get_roi`` and ``set_roi`` which, depending on whether camera supports binning, take (and return) 4 or 6 arguments: start and stop positions of ROI along both axes and, optionally, binning along the axes::

    cam.set_roi(0,128,0,256)  # set 128x256px (width x height) ROI in the (typically) upper left controller
    cam.set_roi(0,128)  # set roi with 128px width and full height (non-supplied arguments take extreme values)
    cam.set_roi(0,128,0,128,2,2)  # set 128x128px ROI with 2x2 binning; the resulting image size is 64x64

Regardless of the frame indexing, the first pair of arguments always controls horizontal span, the second pair controls vertical span, and the last pair controls horizontal and vertical binning (if applicable).

In addition, there is a couple of methods to acquire the detector and frame size. The first method is ``get_detector_size``. It always returns the full camera detector size as a tuple ``(width, height)`` and, therefore, is not affected by ROI, binning, and indexing. The second method is ``get_data_dimensions``, which returns the shape of the returned frame given the currently set up indexing. The results of this method do depend on the ROI, binning, and indexing::

    >> cam.get_detector_size()  # (width, height)
    (2560, 1920)
    >> cam.get_data_dimensions()  # (rows, columns), i.e., (height, width)
    (1920, 2560)

    >> cam.set_roi(0,256,0,128,2,2)  # 256px horizontally, 128 vertically, 2x2 binning
    >> cam.get_detector_size()  # unaffected
    (2560, 1920)
    >> cam.get_data_dimensions()  # depends on ROI
    (64, 128)

    >> cam.set_image_indexing("xyb")
    >> cam.get_detector_size()  # unaffected
    (2560, 1920)
    >> cam.get_data_dimensions()  # depends on indexing
    (128, 64)


Exposure and frame period
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In pylablib these parameters are normally controlled by ``get_exposure``/``set_exposure`` and, correspondingly ``get_frame_period``/``set_frame_period`` methods. In addition, ``get_frame_timings`` method provides an overview of all the relevant times. Exposure typically takes priority over frame period: if the frame period is set too small, it becomes the smallest possible for the given exposure; at the same time, if the exposure is set too big, it is still applied, and the frame period becomes the smallest possible with this exposure::

    >> cam.get_frame_timings()  # frame period is a usually bit larger due to the readout time
    TAcqTimings(exposure=0.1, frame_period=0.12)

    >> cam.set_exposure(0.01)
    >> cam.get_frame_timings()  # smaller exposure is still compatible with this frame period
    TAcqTimings(exposure=0.01, frame_period=0.12)

    >> cam.set_frame_period(0)  # effectively means "set the highest possible frame rate"
    >> cam.get_frame_timings()
    TAcqTimings(exposure=0.01, frame_period=0.03)

    >> cam.set_exposure(0.2)
    >> cam.get_frame_timings()  # frame period is increased accordingly
    TAcqTimings(exposure=0.2, frame_period=0.22)

There are exceptions for some camera types, which are discussed separately.


.. _cameras_basics_attributes:

Camera attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some camera interfaces, e.g., :ref:`Thorlabs Scientific Cameras <cameras_thorlabs_tlcamera>`, :ref:`PCO SC2 <cameras_pco_sc2>`, or :ref:`NI IMAQ <cameras_imaq>` are fairly specific, and only apply to a handful of devices with very similar capabilities. In this case, pylablib usually attempts to implement as much of the functionality as possible given the available hardware, and to present it via the camera object methods.

In other cases, e.g., :ref:`NI IMAQdx <cameras_imaqdx>`, :ref:`Andor SDK3 <cameras_andor_sdk3>`, or :ref:`DCAM <cameras_dcam>`, the same interface deals with many fairly different cameras. This is especially true for IMAQdx, which covers hundreds of cameras from dozens of manufacturers, all with very different capabilities and purpose. Since managing such cameras can not usually be conformed to a small set of functions, it is implemented through camera attributes mechanism. That is, for each camera the interface defines a set of attributes (sometimes also called properties or features), which can be queried or set by their names, and whose exact meaning and possible values depend on the specific camera.

Typically, cameras dealing with attributes will implement :meth:`.IAttributeCamera.get_attribute_value` and :meth:`.IAttributeCamera.set_attribute_value` for querying and setting the attributes, as well as dictionary-like ``.cav`` (stands for "camera attribute value") interface to do the same thing::

    >> cam = Andor.AndorSDK3Camera()
    >> cam.get_attribute_value("CameraAcquiring")  # check if the camera is acquiring
    0
    >> cam.set_attribute_value("ExposureTime", 0.1)  # set the exposure to 100ms
    >> cam.cav["ExposureTime"]  # get the exposure; could also use cam.get_attribute_value("ExposureTime")
    0.1

Additionally, there are :meth:`.IAttributeCamera.get_all_attribute_values` and :meth:`.IAttributeCamera.set_all_attribute_values` which get and set all camera attributes (possibly only within the given branch, if camera attributes form a hierarchy). Finally, methods :meth:`.IAttributeCamera.get_attribute` and :meth:`.IAttributeCamera.get_all_attributes`, together with the corresponding ``.ca`` interface, allow to query specific attribute objects, which provide additional information about the attributes: whether they are writable or readable, their range, description, possible values, types, etc.::

    >> cam = DCAM.DCAMCamera()
    >> attr=cam.ca["EXPOSURE TIME"]  # get the exposure attribute
    DCAMAttribute(name='EXPOSURE TIME', id=2031888, min=0.001, max=10.0, unit=1)
    >> attr.max
    10.0
    >> attr.set_value(0.1)  # same as cam.set_attribute_value("EXPOSURE TIME", 0.1)

Note that, depending on the camera, the attribute properties (especially minimal and maximal value) can depend on the other camera attributes. For example, minimal exposure can depend on the frame size::

    >> cam = DCAM.DCAMCamera()
    >> attr=cam.ca["EXPOSURE TIME"]  # get the exposure attribute
    DCAMAttribute(name='EXPOSURE TIME', id=2031888, min=0.001, max=10.0, unit=1)
    >> attr.min
    0.001
    >> cam.set_roi(0, 0, 0, 0)  # set the minimal possible ROI
    (0, 4, 0, 4, 1, 1)
    >> attr.min  # minimal value hasn't been updated yet
    0.001
    >> attr.update_limits()  # update the property limits
    >> attr.min  # now the minimal possible exposure is smaller
    7.795e-05

If the documentation is not available (as is the case for, e.g., some IMAQdx cameras), the best way to learn about the attributes is to use the native software (whenever available) to modify camera settings and then check how the attributes change. Besides that, it is always useful to check attribute description (available for IMAQdx parameter), their range, and the available values for enum attributes.


Trigger setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The trigger is usually set up using ``set_trigger_mode`` method, although it might be different if more specialized modes are used. When external trigger is involved, most of the code (such as acquisition set up and start) stays the same. The only difference is the rate at which the frames are generated::

    frame = cam.snap()  # starts acquiring immediately, returns after a single frame
    cam.set_trigger_mode("ext") # set up the trigger mode
    frame = cam.snap()
    #  after cam.snap() is called, the execution will wait
    #  for an external trigger pulse to acquire the frame and return


Frame metainfo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many cameras supply additional information together with the frames. Most frequently it contains the internal framestamp and timestamp (which are useful for tracking missing frames), but sometimes it also includes additional information such as frame size or location, status, or auxiliary input bits. To get this information, you can supply the argument ``return_info=True`` to the ``read_multiple_images`` method. In this case, instead of a single list of frames, it will return a tuple of two lists, where the second list contains this metainfo.

There are several slightly different metainfo formats, which can be set using :meth:`.ICamera.set_frame_info_format` method. The default representation is a (possibly nested) named tuple, but it is also possible to represent it as a flat list, flat dictionary, or a numpy array. The exact structure and values depend on the camera.

Keep in mind, that for some camera interfaces (e.g., :ref:`Uc480 <cameras_uc480>` or :ref:`Silicon Software <cameras_siso>`) obtaining the additional information might take relatively long, even longer than the proper frame readout. Hence, at higher frame rates it might become a bottleneck, and would need to be turned off.


Related projects
-------------------------

`Pylablib cam-control <https://github.com/AlexShkarin/pylablib-cam-control>`__ is a standalone software package which builds on camera classes included in pylablib. It provides an easy way to detect and control many different cameras and acquire their data. In addition, it supports custom on-line image processing, flexible data acquisition, and control by external software using a TCP/IP server.


Currently supported cameras
-------------------------------------------
.. include:: cameras_list.txt