PyLabLib: Python package for device control and experiment automation
============================================================================

PyLabLib aims to provide support for device control and experiment automation. It interfaces with lots of different :ref:`devices <devices_root>`, including several different :ref:`camera interfaces <cameras_root>`, :ref:`translational stages <stages_root>`, :ref:`oscilloscopes <oscilloscopes_tektronix>`, :ref:`AWGs <awg_generic>`, :ref:`sensors <basic_sensors_root>`, and more. The interface is implemented in a natural way through Python objects, and is easy to understand. For example, here is a complete script which steps :ref:`Thorlabs KDC101 <stages_thorlabs_kinesis>` stage by 10000 steps ten times, and each time grabs a frame with :ref:`Andor iXon camera <cameras_andor_sdk2>`::

   from pylablib.devices import Thorlabs, Andor  # import the device libraries
   import numpy as np  # import numpy for saving

   # connect to the devices
   with Thorlabs.KinesisMotor("27000000") as stage, Andor.AndorSDK2Camera() as cam:
      # change some camera parameters
      cam.set_exposure(50E-3)
      cam.set_roi(0, 128, 0, 128, hbin=2, vbin=2)
      # start the stepping loop
      images = []
      for _ in range(10):
         stage.move_by(10000)  # initiate a move
         stage.wait_move()  # wait until it's done
         img = cam.snap()  # grab a single frame
         images.append(img)

   np.array(images).astype("<u2").tofile("frames.bin")  # save frames as raw binary

The list of the devices is constantly expanding.

Additional utilities are added to simplify data acquisition, storage, and processing:

    - Simplified data processing utilities: convenient :ref:`fitting <dataproc_fitting>`, :ref:`filtering <dataproc_filtering>`, :ref:`feature detection <dataproc_feature>`, :ref:`FFT <dataproc_fourier>` (mostly wrappers around NumPy and SciPy).
    - Universal multi-level :ref:`dictionaries <storage_dictionary>` which are convenient for :ref:`storing <storage_fileio_dict>` heterogeneous data and settings in human-readable format.
    - Assorted functions for dealing with :ref:`file system <misc_utils_files>` (creating, moving and removing folders, zipping/unzipping, path normalization), :ref:`network <misc_utils_net>` (simplified interface for client and server sockets), :ref:`strings <misc_utils_string>` (conversion of various Python objects to and from string), and more.
    - Tools for GUI generation and advanced multi-threading built on top of Qt5 *(still in development stage: the documentation is incomplete, and the interfaces can change in later versions)*

The library only works on Python 3, and has been most extensively tested on Windows 10 with 64-bit Python. Linux is, in principle, supported, but devices which require manufacturer-provided DLLs (mostly cameras) might, potentially, have problems.

.. note::
   This is documentation for the newer **1.x** version of the library. The older **0.x** documentation can be found at https://pylablib-v0.readthedocs.io/en/latest/ .


Related projects
-------------------------

`Pylablib cam-control <https://github.com/AlexShkarin/pylablib-cam-control>`__ - software for universal camera control and camera data acquisition.


Citation
-------------------------

If you found this package useful in your scientific work, you can cite via `Zenodo <https://doi.org/10.5281/zenodo.7324875>`__ either referencing to the package in general using the DOI ``10.5281/zenodo.7324875``, or to a specific version, as found on the `Zenodo <https://doi.org/10.5281/zenodo.7324875>`__ page.


.. toctree::
   :maxdepth: 2
   :includehidden:
   :caption: Contents:

   install
   devices/devices_root
   dataproc
   storage
   misc_utils
   changelog
   API reference <.apidoc/modules>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
