.. _changelog:

Change log
============================

This is a list of changes between each version.


Version 1.x
----------------------------

Transitioning from version 0.x to version 1.x saw lots of interface changes which break backward compatibility. The previous version of the library can be either obtained on PyPi using ``pip install "pylablib<1"``, or by using ``legacy`` module. Hence, instead of

.. code-block:: python

    import pylablib as pll
    from pylablib.aux_libs.devices import Lakeshore

you can write

.. code-block:: python

    import pylablib.legacy as pll
    from pylablib.legacy.aux_libs.devices import Lakeshore

1.4.4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Devices

    * Added several devices:
    
        + Rigol DG1020Z arbitrary waveform generator
        + Lakeshore 235 temperature controller
        + Agilent E5071C vector network analyzer

    * Improved Linux library loading support

1.4.3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Devices

    * Added multiple devices:
    
        + Agilent XGS600 pressure gauge controller
        + Hubner Cobolt lasers (tested with Cobolt MLD 06-01 laser)
        + Omron E5_C temperature controllers (tested with E5GC-QX1A6M-015 controller)
        + Thorlabs Kinesis Piezo controllers (tested with KPZ101)

    * Extended device support:

        + Multi-axis Trinamic TMCM controllers (tested with TMCM6110)
        + Matisse Commander server support for Sirah Matisse lasers
        + Added trigger mode selection for uc480/uEye cameras

    * Bug fixes and improved support of specific models:
    
        + Thorlabs Scientific Cameras monochrome bug
        + Fixed minor Thorlabs Kinesis enumeration bugs and KIM101 channel selection bug

- Minor additional functions and bugfixes
    * Fixed module versioning bug which prevented the use of PyInstaller
    * GUI additions: button-selector widgets (alternative to combo box), tab hiding, widget tags for finer GUI control

1.4.2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Devices

    * Added multiple devices:
    
        + Andor Shamrock spectrographs
        + ElektorAutomatick PS2000B power supply
        + Keithley 2110 multimeter
        + Lumel RE72 temperature controller (via Modbus RTU protocol)
        + M2 Solstis EMM (external mixing module)
        + Mightex S-Series cameras
        + Generic NKT lasers Interbus protocol support (tested with NKT SuperK with Select spectral filter)
        + Generic Modbus RTU protocol
        + PhysikInstrumente E-515 piezo controller
        + Rigol DP1116A power supply
        + SmarAct MCS2 stage controller
        + Standa 8SMC5 motion controller
        + Thorlabs PM160 power meter
        + Voltcraft VC-7055BT multimeter

    * Extended device support:

        + Thorlabs Scientific Cameras (Zelux, Kiralux) color mode
        + Thorlabs APT/Kinesis motor controllers
        + Trinamic TMCM1110 homing

    * Added HID device communication backend
    * Switched some camera code to Cython to support higher frame rates.
    * Multiple bug fixes and improved support of specific models:
    
        + Selection of RTS cycling for Arduino boards (better support for newer boards such as Leonardo)
        + Support for SiliconSoftware microEnable 5 (Basler microEnable 5 marathon)
        + Improved Sirah Matisse tuning support for frequency tuning and stitched scans based on HighFinesse wavemeters feedback.

- Switched to Cython code in several places for minor plotting speedups.
- Minor additional functions
    * Added time tracker class for simple profiling
    * Added CRC calculation methods

1.4.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Devices

    * Added Basler pylon-compatible cameras, BitFlow frame grabbers, AlliedVision Bonito cameras, Thorlabs Elliptec stages, PI-E516 piezo controller, and Sirah Matisse laser.
    * Minor additions to Cryocon temperature controller, Cryomagnetics LM510 level meters, and NI DAQmx DAQs. Improved performance of PCO cameras at high frame rates.
    * Multiple minor bug fixes and improved support of specific models.

- Added encoding argument to file loading.
- Improved color images support in image plotter, minor additions to trace plotter.
- Added real-time binning and debounce filters.


1.4.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Added Photometrics cameras and Cryocon temperature controllers.
- More consistent cameras interface: attributes properties, fast chunks (former ``fastbuff``) readout, frame info formats.
- Added new simple GUI elements: multiline edits, enum labels.
- Expanded image and trace plotting widgets.
- Added linear transforms to data processing.
- Minor bugfixes in threading, GUI, devices.

1.3.3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Numpy ``loads`` bugfix (fixes compatibility with ``numpy>=1.22``).

1.3.2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Added Leybold ITR90 and KJL300 pressure gauges.
- Minor bugfixes in threading and devices.

1.3.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Added expandable edit boxes and dialog containers.
- Improved Thorlabs devices compliance.
- Additional minor bugfixes in threading, GUI, devices.

1.3.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- General

    * Minor speedups through calls caching.
    * Changed ``muxcall`` signature to allow multiple special argument values.

- Devices

    * Added Princeton Instruments cameras, IDS uEye cameras (as an option in uc480 cameras backend), Thorlabs Kinesis piezo motor controllers (e.g., KIM101) and quadrature photo-detector controllers (e.g., KPA101).
    * Added RS485 Arcus connection and a simple single-motor stage (DMX-J-SA).
    * Improved reliability if errors are encountered upon connection.
    * Multiple minor bug fixes and improved support of specific models.

- GUI

    * Added widgets: menu dropdown button, scroll area container, area highlighter.
    * Added querying element position and layout shape in layout widgets.
    * Added more utilities methods: querying containing layout, querying top-level parent, deleting widget.

- Threading

    * Added simple profiling through ``yappi``.

1.2.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- General

    * Added restarting methods for regular and threaded applications.

- Threading

    * Bugfixes in cameras and camera threads.
    * Bugfixes in streaming.

1.2.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- General

    * Added ``timing`` context manager for simple code timing checks.
    * Improved RPyC wrapper logging and reliability.
    * Added Anaconda support.
    * Added minor network and file functions.

- Devices

    * Added Newport Picomotor 8742 motor controller, Toptica iBeam Smart laser, older version of Thorlabs FW motorized filter wheel.
    * Added camera frame output format (list or array).
    * Added ``use_cavity`` option to M2 Solstis laser.
    * Added method for auto-detecting associations between PhotonFocus cameras and frame grabbers.
    * Updated some generic classes (DCAM cameras, Thorlabs TLCamera cameras).
    * Updated SCPI failsafe operation, improved Thorlabs FW reliability.
    * Fixed several minor bugs.

- GUI

    * Rewritten GUI values handling to pass calls in a hierarchical manner. This makes the operation more predictable and overloading the behavior a bit easier.
    * Added out-of-range value action for combo boxes.
    * Fixed ``ImagePlotter`` incompatibility with the newer pyqtgraph versions, added separate x and y axis line cuts selection.
    * Minor layout handling bugfixes.

- Threading

    * Released advanced threading functionality: table/frame streaming, device threads, basic frame processing.
    * Task thread additions: delayed batch job stopping, context manager for task loop pausing.
    * Added argument-dependent call queue limit.
    * Improved threading speed and stability.


1.1.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- General

    * Reorganized the core modules import structure: now ``__init__.py`` modules are mostly empty, and all the necessary imports are either exposed directly in ``pylablib`` (e.g., ``pylablib.Fitter``), or should be accessed directly by the module (e.g. ``pll.core.dataproc.fitting.Fitter``). Intermediate access (e.g., ``pll.core.dataproc.Fitter``) is no longer supported.
    * File IO functions (e.g., ``read_csv``) can now take file-like objects in addition to paths.

- Devices
    
    * Added Silicon Software frame grabbers interface and rearranged PhotonFocus code to include both IMAQ and SiliconSoftware frame grabbers.
    * Fixed various compatibility bugs arising for specific versions of Python or dependency modules: Kinesis error with specific pyft232 versions, some DLL-dependent devices errors with Python 3.8+, DLL types in 32-bit Python.
    * Addressed issue with occasional uc480 acquisition restarts, fixed M2 communication report errors.

- GUI and threading

    * Added container and layout management classes in addition to parameter tables for more consistent GUI structure organization.
    * Added ``pylablib.widgets`` module which combines all custom widgets for the ease of using in layout managers or custom applications.
    * Fixed  support for ``PySide2`` Qt5 backed.
    * Renamed ``setupUi`` -> ``setup`` for all widgets, and changed the GUI setup organization for many of them (the functioning stayed the same).
    * Reorganized scheduling in ``QTaskThread`` to treat jobs, commands, and subscriptions more consistently.
    * Added basic data stream management.



1.0.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There have been too many alterations to list here comprehensively. Below is the list of the largest changes.

- General

    * Removed built-in ``DataTable`` class (together with ``core.datatable`` subpackage) in favor of pandas.
    * Renamed file IO functions: instead of generic ``load`` and ``save`` methods there are now more specific :func:`.loadfile.load_csv`, :func:`.loadfile.load_dict`, etc.
    * Removed some legacy modules which are not used in the rest of the library.
    * Renamed or moved certain modules: ``core.utils.rpyc`` -> ``core.utils.rpyc_utils``, ``core.fileio.logfile`` -> ``core.fileio.table_stream``, ``core.fileio.binio`` -> ``core.utils.binio`` , ``core.devio.backend`` -> ``core.devio.backencd_comm``, ``core.devio.untis`` -> ``core.utils.units``, ``core.dataproc.waveforms`` -> ``core.dataproc.utils``

- Devices

    * Some legacy devices have been removed, since without access to the hardware it is hard to maintain and expand them. These include most of Agilent devices (33502A amplifier, N9310A microwave generator, HP 8712B and HP 8722D network analyzers, HP 8168F laser), Rigol DSA1030A spectrum analyzer, Tektronix MDO3000 oscilloscope, Vaunix LabBrick generators, Zurich Instruments HF2 and UHF, Andor Shamrock spectrographs (should be restored in future releases), NuPhoton NP2000 EDFA, PurePhotonics PPCL200 laser, Sirah Matisse laser (should be restored in future releases), Thorlabs PM100 power meter (should be restored in future releases), Lakeshore 370 resistance bridge (should be restored in future releases), MKS 900-series pressure gauges, and some custom devices (Arduino and Olimex AVR boards and Janis-related hardware).
    * The main devices package has been moved from ``pylablib.aux_libs.devices`` (which now refers to the legacy code) to ``pylablib.devices``. Module organization has also changed slightly. To find the required modules and device class names, see the :ref:`devices list <devices_root>`.
    * Lots of devices' interface has varied slightly, to make the interface more uniform and compatible between different kinds of devices. The changes are usually fairly straightforward (e.g., ``move_to`` instead of ``move``). In many cases the interface was also expanded to include additional available methods.
    * Several devices have been added, generalized, or restructured:
    
      + Combined Thorlabs KDC101 and K10CR1 into a single class :class:`pylablib.devices.Thorlabs.BasicKinesisDevice<.kinesis.BasicKinesisDevice>`, which also accommodates similar kinds of devices.
      + Added Arcus Performax2EXStage device for 2-axis controller with a slightly different interface (:class:`pylablib.devices.Arcus.Performax2EXStage<.performax.Performax2EXStage>`)
      + Added :ref:`several more AWGs <awg_generic>` with similar interfaces

    * Simplified the way external DLLs are :ref:`handled <devices_external_dependencies>`
    * Unified the :ref:`error handling <devices_error_handling>`

- GUI and threading

    * Changed module structure
      
      + threading and GUI are now separate sub-packages ``core.thread`` and ``core.gui``
      + all widgets are available simply through ``pylablib.widgets`` (simplifies integration with Qt Designer)
      + moved parameter tables widgets to the core library

    * Renamed some widgets to remove the ``LV`` prefix.
    * Interfaces changes in some of the classes: thread controllers, parameter tables, value tables. The changes are mostly cosmetics and involve names and parameters order. Most important changes:

      + thread controller methods: ``subscribe`` -> ``subscribe_sync``, ``sync_exec`` -> ``sync_exec_point``, 
      + thread controller command/query shortcut: ``.c`` -> ``.ca``, ``.q`` -> ``.cs``, ``.qi`` -> ``.csi``, ``.qs`` -> ``.css``
      + thread controller variable access uses ``.v`` shortcut, i.e., instead of ``ctl[name]`` it is now ``ctl.v[name]``
      + GUI value storage ``ValuesTable``/``IndicatorValuesTable`` are now combined and named as ``GUIValues``
      + ``ParamTable`` and ``GUIValues`` uses ``.h`` shortcut to access value handlers, i.e., instead of ``table[name]`` it is now ``table.h[name]``
      + ``ParamTable``, ``ImagePlotterCtl``, ``TracePlotterCtl`` constructor arguments: ``display_table`` -> ``gui_values``, ``display_table_root`` -> ``gui_values_root``
      + value-changed signal names in ``ParamTable`` and ``GUIValues``: ``changed_event`` -> ``get_value_changed_signal``
      + value-changed signal names in value handlers: ``value_changed_signal`` -> ``get_value_changed_signal``
      + ``ParamTable`` methods: ``lock`` -> ``set_enabled``, ``add_button(checkable=True)`` -> ``add_toggle_button``
      + ``NumEdit`` and ``NumLabel`` methods: ``set_number_format`` -> ``set_formatter``, ``set_number_limit`` -> ``set_limiter`` (the call signature also changed)
      + renamed signals to multicasts to avoid confusion with built-in Qt signals. Leads to ``ThreadController.send_signal`` -> ``send_multicast``, ``ThreadController.process_signal`` -> ``process_multicast``, ``ThreadController`` constructor argument ``signal_pool`` -> ``multicast_pool``, class ``SignalPool`` -> ``MulticastPool``, ``QSignalThreadCallScheduler`` -> QMulticastThreadCallScheduler.


Version 0.x
----------------------------

0.4.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Interface changes**

- Slightly changed representations of complex number in to-string conversions depending on the conversion rules (``"python"`` vs ``"text"``).

**Additions**

- Devices

    * Added Thorlabs K10CR1 rotational stage (``legacy.aux_libs.devices.Thorlabs.K10CR1``)
    * Added Andor Shamrock spectrographs (``legacy.aux_libs.devices.AndorShamrock``)
    * Expanded Agilent AWG class
    * Added more 32bit dlls
    * Added ``list_resources`` method to every backend class, which lists available connections for this backend (not available for every backend; so far only works in ``legacy.core.devio.backed.VisaDeviceBackend``, ``legacy.core.devio.backed.SerialDeviceBackend``, and ``legacy.core.devio.backed.FT232BackendOpenError``.

- GUI and threading

    * Added ``legacy.aux_libs.gui.helpers.TableAccumulatorThread.preprocess_data`` method to pre-process incoming data before adding it to the table
    * Added ``update_only_on_visible`` argument to ``legacy.aux_libs.gui.widgets.trace_plotter.TracePlotter.setupUi`` method, and ``legacy.aux_libs.gui.widgets.trace_plotter.TracePlotter.get_required_channels`` method.



0.4.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Interface changes**

- Dictionary entries (``legacy.core.fileio.dict_entry``) system has been slightly redesigned: building entries from stored objects has been moved from ``legacy.core.fileio.dict_entry.IDictionaryEntry.build_entry`` class method to a dedicated function ``legacy.core.fileio.dict_entry.build_entry``, and entry classes have been added.
- ``legacy.aux_libs.gui.helpers.StreamFormerThread`` architecture changes, so that it can accumulates several rows before adding them into the storage; this lead to replacement of ``legacy.aux_libs.gui.helpers.StreamFormerThread.prepare_new_row`` method by ``legacy.aux_libs.gui.helpers.StreamFormerThread.prepare_new_data``.

**Additions**

- General

    * Added pandas support in a bunch of places: loading/saving tables and dictionaries; data processing routines in ``legacy.core.dataproc``; conversion of ``legacy.core.dataproc.datatable.DataTable`` and ``legacy.core.utils.dictionary.Dictionary`` object to/from pandas dataframes.
    * Expanded string conversion to support more explicit variable classes. For example, a numpy array ``np.array([1,2,3])`` can be converted into a string ``'array([1, 2, 3])'`` instead of a more ambiguous string ``'[1, 2, 3]'`` (which can also be a list). This behavior is controlled by a new argument ``use_classes`` in string conversion functions (such as ``legacy.core.utils.string.to_string`` and ``legacy.core.utils.string.from_string``) and an argument ``use_rep_classes`` in file saving (``legacy.core.fileio.savefile.save``)
    * Added general library parameters, which can be accessed via ``pylablib.par`` (works as a dictionary object). So far there's only one supported parameter: the default return type of the CSV file reading (can be ``"pandas"`` for pandas dataframe, ``"table"`` for ``legacy.core.dataproc.datatable.DataTable`` object, or ``"array"`` for raw numpy array).

- Devices

    * Added LaserQuantum Finesse device class (``legacy.aux_libs.devices.devices.LaserQuantum``)
    * NI DAQ now supports output of waveforms
    * Added ``legacy.aux_libs.devices.PCO_SC2.reset_api`` and ``legacy.aux_libs.devices.PCO_SC2.PCOSC2Camera.reboot`` methods for resetting API and cameras
    * Added ``legacy.aux_libs.devices.Thorlabs.list_kinesis_devices`` function to list connected Kinesis devices
    * Added serial communication methods for IMAQ cameras (``legacy.aux_libs.devices.IMAQ.IMAQCamera``)

- GUI and threading

    * Added line plotter (``legacy.aux_libs.gui.widgets.line_plotter``) and trace plotter (``legacy.aux_libs.gui.widgets.trace_plotter``) widgets
    * Added virtual elements to value tables and parameter tables
    * Added ``gui_thread_safe`` parameter to value tables and parameter tables. Enabling it make most common methods thread-safe (i.e., transparently called from the GUI thread)
    * Added a corresponding ``legacy.core.gui.qt.thread.controller.gui_thread_method`` wrapper to implement the change above
    * Added functional thread variables (``legacy.core.gui.qt.thread.controller.QThreadController.set_func_variable``)

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

    * ``legacy.core.dataproc.fitting.Fitter`` now takes default scale and limit as constructor arguments.
    * ``legacy.core.dataproc.feature.multi_scale_peakdet`` has new ``norm_ratio`` argument.
    * ``legacy.core.dataproc.image.get_region`` and ``legacy.core.dataproc.image.get_region_sum`` take ``axis`` argument.

- Miscellaneous

    * Functions introspection module now supports Python 3 - style functions, and added a new function ``legacy.core.utils.functions.funcsig``
    * ``legacy.core.utils.general.StreamFileLogger`` supports multiple destination paths
    * New network function ``legacy.core.utils.net.get_all_local_addr`` (return list of all local addresses on all interfaces) and ``legacy.core.utils.net.get_local_hostname``