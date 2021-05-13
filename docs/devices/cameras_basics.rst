.. _cameras_basics:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

Cameras control basics
======================================

Basic examples
--------------------------------------

Basic camera usage is fairly straightforward::

    from pylablib import Andor
    cam = Andor.AndorSDK2Camera()  # connect to the camera
    cam.set_exposure(10E-3)  # set 10ms exposure
    cam.set_roi(0,128,0,128)  # set 128x128px ROI in the upper right corner
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

In most cases, the frames acquired by the camera are first temporarily stored in the local camera and / or frame grabber memory, from which they are transferred to the PC RAM by the camera drivers. Afterwards, this memory is made available to all other applications. In principle, it should be enough to store only the most recent frame in RAM, and for the user software to continuously read and process it. However, such approach is very demanding to the user code: if the new frame is acquired before the previous one is processed, the RAM data is overwritten, and the old frame is lost. Hence, it is more practical to have a *buffer* of several most recently acquired frames to account for interruptions caused by OS scheduling and by other jobs performed in the user software. In this case, the frames get lost only when the buffer is completely filled, and the oldest frames starts getting overwritten.

When using the camera classes provided by pylablib, you do not need to worry about setting up the buffer yourself, since it is done behind the scene either by the manufacturer's code or by pylablib. However, it is important to keep in mind the existence of the buffer when setting up the acquisition, interpreting the buffer and acquired frames status, or identifying the skipped frames.

The size of the buffer can almost always be selected by the user. Typically it is a good idea to have at least 100ms worth of frames there, although, depending on the other jobs performed by the thread, it can be larger.


Acquisition setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setting up an acquisition process might take a lot of time (up to 10s in more extreme cases). This happens mostly because of the buffer allocation and setting up internal API structures, while starting the acquisition process itself is fairly fast. Hence, it is useful to separate setting up / cleaning up and starting / stopping.

The first two procedures correspond to ``setup_acquisition`` and ``clear_acquisition`` method, which are slow, but rarely called. Usually, they only need to be invoked right after connection to the camera, or when the acquired image size is change (e.g., due to binning or ROI). Since these methods deal with buffer allocation, in almost all cases they take a parameter specifying buffer size (typically called ``nframes``).

The other two procedures correspond to ``start_acquisition`` and ``stop_acquisition`` methods. These try to be as fast as possible, as they need to be called any time the acquisition is started or stopped, or when minor parameters (frame rate, exposure, trigger mode) are called.


Region of interest (ROI) and binning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most cameras allow the user to select only part of the whole sensor for readout and transfer. Since the readout speed is usually the factor limiting the frame rate, selecting small ROI lets you achieve high frame rate. In addition, it also reduces the size of the frame buffer and the data transfer load. Same goes for binning: many cameras can add values of several consecutive pixels in the same row or column (or both), which results in smaller images and, depending on the camera architecture, higher signal-to-noise ratio. Much less frequently you can set up subsampling instead of binning, which skips pixels instead of averaging them together.

Both operations very strongly depend on the exact hardware, so there are typically many associated restriction. The most common are minimal sizes in width and height, positions and sizes being factors of some power of 2 (up to 32 for some cameras), or equal binning for both axes. The library will typically round the ROI to the nearest allowed value. Furthermore, the scaling of the maximal frame rate on the ROI is also hardware-dependent; for example, in many sCMOS chips readout speed only cares about vertical extent (since the readout is done simultaneously for the whole row). In most cases, it takes some experiments to get a hang of the camera behavior.


Exposure and frame rate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Almost all scientific cameras let user change the exposure, typically in a wide range (down to sub-ms). Frequently they also also to separately change the frame period (inverse of the frame rate). Usually (but not always) the minimal frame period is set by the exposure plus some readout time, which depends on the ROI and some additional parameters such as pixel clock or simultaneous readout mode.


Triggering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usually the cameras will have several different options for triggering, i.e., choosing when to start acquiring a new frame. The default option is the internal trigger, which means that the internal timer generates trigger event at a constant rate (frame rate). Many cameras will also take an external trigger signal to synchronize acquisition to external events or other cameras. Typically, a rising edge from 0 to 5V on the input will initiate the frame acquisition, but more exotic options (different polarities, exposure control with pulse width, line-readout trigger) can be present.




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

    cam.setup_acquisition(nframes=100)  # could be combined with start_acquisition, or kept separate
    cam.start_acquisition()
    while True:  # acquisition loop
        cam.wait_for_frame()  # wait for the next available frame
        frame = cam.read_oldest_image()  # get the oldest image which hasn't been read yet
        # ... process frame ...
        if time_to_stop:
            break
    cam.stop_acquisition()

It relies on 3 sets of methods. First, starting and stopping acquisition using ``start_acquisition`` and ``stop_acquisition``. As explained above, one also has an option to setup the acquisition first using ``setup_acquisition```, which makes subsequent ``start_acquisition`` call much faster. In other cases, ``start_acquisition`` takes the same parameters and sets up the acquisition if necessary (if any parameters are different from the current ones).

Second, checking the acquisition process. The method used above is ``wait_for_frame``, which by default waits until there is at least one unread frame in the buffer (i.e., it exits immediately if there is already a frame available). Its arguments modify this behavior by changing the point from which the new frame is acquired (e.g., from the current call), or the minimal required number of frames. Alternatively, there is a method ``get_new_images_range``, which returns a range of the frame indices (from the start of acquisition) which have been acquired but not read.

Finally, there are methods for reading out the frames. The simplest method is ``read_oldest_image``, which return the oldest image which hasn't been read yet, and marks it as read. A more powerful is the ``read_multiple_images`` method, which can return a range of images (by default, all unread images). Both of these methods also take a ``peek`` argument, which allows one to read the frames without marking them as read.


Frame indexing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Different areas and libraries adopt different indexing convention for 2D arrays. The two most common ones are coordinate-like ``xy`` (the first index is the ``x`` coordinate, the second is ``y`` coordinate, and the origin is in the lower left corner) and matrix-like ``ij`` (the first index is row, the second index is column, the origin is int the upper right corner). Almost all cameras adopt the ``ij`` convention. The only exception is Andor SDK2, which uses similar row-column indexing, but counting from the bottom.

By default, the frames returned by the camera are indexed in the preferred convention, to reduce the overhead on re-indexing the frames. It is possible to check and change it using ``get_image_indexing`` and ``set_image_indexing`` methods::

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

In addition, there is a couple of methods to acquire the detector and frame size. The first method is ``get_detector_size``. It always returns the full frame size as a tuple with width first and hight second, and therefore is not affected by ROI, binning, and indexing. The second method is ``get_data_dimensions``, which returns the shape of the returned frame given the currently set up indexing. The results of this method do depend on the ROI, binning, and indexing::

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

In pylablib these parameters are controlled by ``get_exposure``/``set_exposure`` and, correspondingly ``get_frame_period``/``set_frame_period`` methods. Some cameras can provide finer control over these parameters. In addition, ``get_frame_timings`` method provides an overview of all the relevant times. Exposure typically takes priority over frame period: if the frame period is set too small, it becomes the smallest possible for the given exposure; at the same time, if the exposure is set too big, it is still applied, and the frame period becomes the smallest possible with this exposure::

    >> cam.get_frame_timings()  # frame period is a usually bit larger due to the readout time
    TAcqTimings(exposure=0.1, frame_period=0.12)

    >> cam.set_exposure(0.01)
    >> cam.get_frame_timings()  # smaller exposure is still compatible with this frame period
    TAcqTimings(exposure=0.01, frame_period=0.12)

    >> cam.set_frame_period(0)  # effectively means "set highest possible frame rate"
    >> cam.get_frame_timings()
    TAcqTimings(exposure=0.01, frame_period=0.03)

    >> cam.set_exposure(0.2)
    >> cam.get_frame_timings()  # frame period is increased accordingly
    TAcqTimings(exposure=0.2, frame_period=0.22)

There are exceptions for some camera types, which are discussed separately


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

Many cameras supply additional information together with the frames. Most frequently it includes the internal framestamp and timestamp (which are useful for tracking missing frames), but sometimes it also includes additional information such as frame size or location, status, or auxiliary input bits. To get this information, you can supply the argument ``return_info=True`` to the ``read_multiple_images`` method. In this case, instead of a single list of frames, it will return a tuple of two lists, where the second list contains this metainfo. Each frame's metainfo is represented by a named tuple, whose structure differs for different cameras.


Currently supported cameras
-------------------------------------------
.. include:: cameras_list.txt