.. _sensors_highfinesse:

.. note::
    General sensor communication concepts are described on the corresponding :ref:`page <basic_sensors_basics>`

HighFinesse wavemeters
==============================

HighFinesse produces a variety of fiber-coupled wavelength meters. Currently pylablib only deals with WS series which uses a USB connection. The code has been tested with several WS6 and WS7 wavemeters.

The main device class is :class:`pylablib.devices.HighFinesse.WLM<.wlm.WLM>`.


Software requirements
-----------------------

HighFinesse employs a fairly unique control system.

First, one needs to install the control software, which is uniquely tied to a particular wavemeter and is supplied with it. In theory, software from another wavemeter might still work, but the results are not guaranteed.

Second, this control software runs an application server which processes all requests from third-party software. This means, that the main application needs to be running to perform any device communication from the code. The code has an option of automatically starting it, but on some occasions it might fail, in which case it is necessary to either manually start it, or supply the location of the executable file.

.. note:: The control software should keep running the whole time. As soon as it is closed, the device will raise an error.

Finally, one needs the DLL to communicate with this software. It is usually named ``wlmData.dll``, and it is located in the main controller software folder either in ``Com-Test`` (for 32-bit applications) or ``Projects/64`` (for 64-bit applications).

Connection
-----------------------

The device class makes an attempt to search for the DLL and executable in the standard installation folders, as well as use the DLL in the standard location and its executable auto-detection capabilities. However, depending on the number of installed wavemeters and their installation locations, one needs to provide up to 3 arguments on connection. First, the wavemeter ID, which simply a 1 to 5-digit number (e.g. 1234). It is used to identify the correct instance of the control software, either by searching for the correct folder, or via DLL autostart capabilities. Second, one might need to provide the path to ``wlmData.dll`` (either including the name, or simply the containing folder). Its location is described in the above section. Finally, you might also need to give the path to the application executable, which is located in the main installation folder and is named ``wlm_ws*.exe``, where ``*`` is the wavemeter generation (e.g., ``wlm_ws7.exe`` for WS7 wavemeters). Hence, the fully qualified (and, therefore, most robust) instantiation looks like this::

    >> import os
    >> from pylablib.devices import HighFinesse
    >> app_folder = r"C:\Program Files\HighFinesse\Wavelength Meter WS7 1234"
    >> dll_path = os.path.join(app_folder, "Projects", "64")
    >> app_path = os.path.join(app_folder, "wlm_ws7.exe")
    >> wm = HighFinesse.WLM(1234, dll_path=dll_path, app_path=app_path)
    >> wm.close()

A unique property of this device is the ability to control it simultaneously from several applications. Keep this in mind, since it might cause confusion or strange results if the control attempts are not synchronized.

.. warning:: Communication with several simultaneously running wavemeters from a single application has not been tested, and might not work correctly.


Operation
-----------------------

The operation of the wavemeter is fairly straightforward, but there is a couple of points to keep in mind:

    - By default, the main measurement functions (:meth:`.WLM.get_frequency` and :meth:`.WLM.get_wavelength`) raise an error on over- or under-exposure. If this is undesirable (e.g., the laser has power jumps), one can instead make it return ``"over"`` or ``"under"`` on these occasions.
    - The measurement result is returned immediately, but it is updated only about every 15-30ms (+ exposure time). Hence, fast consecutive calls to :meth:`.WLM.get_frequency` and :meth:`.WLM.get_wavelength` will return the same value.
    - Multi-channel devices have two working modes: single-channel (when only one channel is enabled at a time) and cycling (the wavemeter constantly cycles through several channels for quasi-simultaneous measurements). Some methods only make sense in one of this modes, e.g., :meth:`.WLM.set_active_channel` only works in the single-channel mode, while :meth:`.WLM.enable_switcher_channel` only in the multi-channel mode. By default, these methods will automatically switch to the corresponding mode.
    - Due to a minor control software bug, change in the exposure on some channels might not be reported until the control software is switched to the corresponding channel's exposure control tab (in the upper right corner). By default, the device class performs this switching any time the exposure value is queried, which solves the issue. However, it does take about 10ms. If it is critical, it's possible to turn of this behavior by setting ``auto_channel_tab`` attribute to ``False``.