.. _changelog:

==========
Change log
==========

This is a list of changes between each version.


-----
0.4.1
-----

**Interface changes**

- Slightly changed representations of complex number in to-string conversions depending on the conversion rules (``"python"`` vs ``"text"``).

**Additions**

- Devices

    * Added Thorlabs K10CR1 rotational stage (:class:`.devices.Thorlabs.K10CR1`)
    * Added Andor Shamrock spectrographs (:mod:`.devices.AndorShamrock`)
    * Expanded Agilent AWG class
    * Added more 32bit dlls
    * Added ``list_resources`` method to every backend class, which lists available connections for this backend (not available for every backend; so far only works in :class:`.VisaDeviceBackend`, :class:`.SerialDeviceBackend`, and :class:`.FT232BackendOpenError`.

- GUI and threading

    * Added :meth:`.TableAccumulatorThread.preprocess_data` method to pre-process incoming data before adding it to the table
    * Added ``update_only_on_visible`` argument to :meth:`.TracePlotter.setupUi` method, and :meth:`.TracePlotter.get_required_channels` method.



-----
0.4.0
-----

**Interface changes**

- Dictionary entries (:mod:`.core.fileio.dict_entry`) system has been slightly redesigned: building entries from stored objects has been moved from :meth:`.dict_entry.IDictionaryEntry.build_entry` class method to a dedicated function :func:`.dict_entry.build_entry`, and entry classes have been added.
- :class:`.aux_libs.gui.helpers.StreamFormerThread` architecture changes, so that it can accumulates several rows before adding them into the storage; this lead to replacement of :meth:`.helpers.StreamFormerThread.prepare_new_row` method by :meth:`.helpers.StreamFormerThread.prepare_new_data`.

**Additions**

- General

    * Added pandas support in a bunch of places: loading/saving tables and dictionaries; data processing routines in :mod:`.core.dataproc`; conversion of :class:`.DataTable` and :class:`.Dictionary` object to/from pandas dataframes.
    * Expanded string conversion to support more explicit variable classes. For example, a numpy array ``np.array([1,2,3])`` can be converted into a string ``'array([1, 2, 3])'`` instead of a more ambiguous string ``'[1, 2, 3]'`` (which can also be a list). This behavior is controlled by a new argument ``use_classes`` in string conversion functions (such as :func:`.string.to_string` and :func:`.string.from_string`) and an argument ``use_rep_classes`` in file saving (:func:`.savefile.save`)
    * Added general library parameters, which can be accessed via ``pylablib.par`` (works as a dictionary object). So far there's only one supported parameter: the default return type of the CSV file reading (can be ``"pandas"`` for pandas dataframe, ``"table"`` for :class:`.DataTable` object, or ``"array"`` for raw numpy array).

- Devices

    * Added LaserQuantum Finesse device class (:mod:`.devices.LaserQuantum`)
    * NI DAQ now supports output of waveforms
    * Added :func:`.PCO_SC2.reset_api` and :meth:`.PCO_SC2.PCOSC2Camera.reboot` methods for resetting API and cameras
    * Added :func:`.Thorlabs.list_kinesis_devices` function to list connected Kinesis devices
    * Added serial communication methods for IMAQ cameras (:class:`.IMAQ.IMAQCamera`)

- GUI and threading

    * Added line plotter (:mod:`.aux_libs.gui.widgets.line_plotter`) and trace plotter (:mod:`.aux_libs.gui.widgets.trace_plotter`) widgets
    * Added virtual elements to value tables and parameter tables
    * Added ``gui_thread_safe`` parameter to value tables and parameter tables. Enabling it make most common methods thread-safe (i.e., transparently called from the GUI thread)
    * Added a corresponding :func:`.controller.gui_thread_method` wrapper to implement the change above
    * Added functional thread variables (:meth:`.controller.QThreadController.set_func_variable`)

- File saving / loading

    * Added notation for dictionary files to include nested structures ('prefix blocks'). This lets one avoid common path prefix in stored dictionary files. For example, a file ::

            some/long/prefix/x  1
            some/long/prefix/y  2
            some/long/prefix/y  3

      can be represented as ::

            //some/long/prefix
                x   1
                y   2
                z   3
            ///

      The meaningful elements are ``//some/long/prefix`` line denoting that following elements have the given prefix, and ``///`` line denoting that the prefix block is done (indentation is only added for clarity).
      
    * New dictionary entries: :class:`.dict_entry.ExternalNumpyDictionaryEntry` (external numpy array, can have arbitrary number of dimensions) and :class:`.dict_entry.ExpandedContainerDictionaryEntry` (turns lists, tuples and dicts into dictionary branches, so that their content can benefit from the automatic table inlining, dictionary entry classes, etc.).

- Data processing

    * :class:`.fitting.Fitter` now takes default scale and limit as constructor arguments.
    * :func:`.feature.multi_scale_peakdet` has new ``norm_ratio`` argument.
    * :func:`.image.get_region` and :func:`.image.get_region_sum` take ``axis`` argument.

- Miscellaneous

    * Functions introspection module now supports Python 3 - style functions, and added a new function :func:`.functions.funcsig`
    * :class:`.utils.general.StreamFileLogger` supports multiple destination paths
    * New network function :func:`.utils.net.get_all_local_addr` (return list of all local addresses on all interfaces) and :func:`.utils.net.get_local_hostname`