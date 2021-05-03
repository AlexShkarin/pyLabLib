.. _devices_basics:

Basics of device communication
======================================

The devices are represented as Python objects, in most cases, one per device.


.. _devices_connection:

Connection
--------------------------------------

The device identifier or address needs to be provided upon the device object creation, after which the devices automatically connect. Getting the address usually depends on the kind of device:

    - Simple message-style devices, such as AWG, oscilloscopes, sensors and gauges, require an address, which depends on the exact connection protocol. For example, serial devices addresses look like ``"COM1"``, Visa addresses as ``"USB0::0x1313::0x8070::000000::INSTR"``, and network addresses take IP and, possibly, port ``"192.168.1.3:7230"``. To get the list of all connected devices, you can run :func:`.comm_backend.list_backend_resources`::

        >> import pylablib as pll
        >> pll.list_backend_resources("serial")  # list serial port resources
        ['COM38', 'COM1', 'COM36', 'COM3']
        >> pll.list_backend_resources("visa")  # note that, by default, visa also includes all the COM ports
        ('USB0::0x1313::0x8070::000000::INSTR',
        'ASRL1::INSTR',
        'ASRL3::INSTR',
        'ASRL10::INSTR',
        'ASRL36::INSTR',
        'ASRL38::INSTR')
      
      Network devices do not easily provide such functionality (also, there are, in principle, lots of devices connected to the networks), so you might need to learn the device IP elsewhere (usually, it is set on the device front panel or using some kind of configuration tool).

      In most cases, the connection address is all you need. However, sometimes the connection might require some additional information. The most common situations are ports for the network connection and baud rates for the serial connections. Ports can be supplied either as a part of the string ``"192.168.1.3:7230"``, or as a tuple ``("192.168.1.3", 7230)``. The baud rates are, similarly, provided as a tuple: ``("COM1", 19200)``. By default, the devices would use the baud rate which is most common for them, but in some cases (e.g., if the device baud rate can be changed), you might need to provide it explicitly. If it is provided incorrectly, then no communication can be done, and any request will return a timeout error::

        >> from pylablib.devices import Ophir
        >> meter = Ophir.VegaPowerMeter("COM3")  # for this power meter 9600 baud are used by default
        >> meter.get_power()  # let us assume that the devices is currently set up with 38400 baud
        ...
        OphirBackendError: backend exception: 'timeout during read'
        >> meter.close()  # need to close the connection before reopening
        >> meter = Ophir.VegaPowerMeter(("COM3",38400))  # explicitly specifying the correct baud rate
        >> meter.get_power()
        1E-6

    - More complicated devices using custom DLLs (usually cameras or translation stages) will have more unique methods of addressing individual devices: serial number, device index, device ID, etc. In most cases such devices come with ``list_devices`` or ``get_devices_number`` functions, which give the necessary information.

After communication is done, the connection needs to be closed, since in most cases it can only be opened in one program or part of the script at a time. It also implies that usually it's impossible to connect to the device while its manufacturer software is still running.

The devices have ``open`` and ``close`` methods, but they can also work in together with Python ``with`` statements::

    # import Thorlabs device classes
    from pylablib.devices import Thorlabs

    # connect to FW102 motorized filter wheel
    wheel = Thorlabs.FW("COM1")
    # set the position
    wheel.set_position(1)
    # close the connection (until that it's impossible to establish a different connection to this device)
    wheel.close()

    # a better approach
    with Thorlabs.FW("COM1") as wheel: # connection is closed automatically when leaving the with-block
        wheel.set_position(1)

Because the devices are automatically connected on creation. ``open`` method is almost never called explicitly.


Operation
--------------------------------------

The devices are controlled by calling their methods; attributes and properties are very rarely used. Effort is made to maintain consistent naming conventions, e.g., most getter-methods will start with ``get_`` and setter methods with ``set_`` or ``setup_`` (depending on the complexity of the method). It is also common for setter methods to return the new value as a result, which is useful in CLI operation and debugging. Devices of the same kind have the same names for similar or identical functions: most stages have ``move_by``, ``jog`` and ``stop`` methods, and cameras have ``wait_for_frame`` and ``read_multiple_images`` methods. Whenever it makes sense, these methods will also have the same signatures.

Multi-threading
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For simplicity of usage and construction, devices interfaces are designed to be synchronous and single-threaded. Asynchronous operation can be achieved by explicit usage of Python multi-threading. Furthermore, it is not recommended to use the same device simultaneously from two separate threads; however, non-simultaneous calling device methods from different threads (e.g., using locks) and simultaneous usage of several separate devices of the same class is supported.


Error handling
--------------------------------------

Errors raised by the devices are usually specific to the device and manufacturer, e.g., :exc:`.AttocubeError` or :exc:`.TrinamicError`. These can be obtained from the module containing the device class, or from the class itself as ``Error`` attribute::

    >> from pylablib.devices import Attocube
    >> atc = Attocube.ANC300("192.168.1.1")
    >> atc.disable_axis(1)
    >> atc.move_by(1,10)  # move on A disabled axis raises an error for ANC300
    ...
    AttocubeError: Axis in wrong mode
    >> try:
    ..     atc.move_by(1,10)
    .. except atc.Error:  # could also write   "except Attocube.AttocubeError"
    ..     print("Can not move")
    Can not move

All of the device errors inherit from :exc:`.DeviceError`, which in turn is a subclass of :exc:`RuntimeError`. Therefore, one can also use those exception classes instead::

    >> import pylablib as pll
    >> try:
    ..     atc.move_by(1,10)
    .. except pll.DeviceError:
    ..     print("Can not move")
    Can not move


Getting more information
--------------------------------------

A lot of information about the devices can be gained just from their method names and descriptions (docstrings). There are several ways of getting these:

    - In many cases your IDE (PyCharm, Spyder, VS Code with installed Python extension) supports code inspection. In this case, the list of methods will usually pop up after you time the device object name and a dot (such as ``cam.``), and the method docstring will show up after you type the method name and parenthesis (such as ``cam.get_roi(``). However, sometimes it might take a while for these pop-ups to show up.
    - You can use console, such as Jupyter QtConsole, Jupyter Notebook, or a similar console built into the IDE. Here the list of methods can be obtained using the autocomplete feature: type name of the class or object with a dot (such as ``cam.``) and then press ``Tab``. The list of all methods should appear. To get the description of a particular class or method, type it with a question mark (such as ``cam?`` or ``cam.get_roi?``) and execute the result (``Enter`` or ``Shift-Enter``, depending on the console). A description should appear with the argument names and the description.
    - You can also use the auto-generated documentation within this manual through the search bar: simply type the name of the class or the method (such as ``AndorSDK3Camera`` or ``AndorSDK3Camera.get_roi``) and look through the results. However, the formatting of the auto-generated documentation might be a bit overwhelming.


Universal settings access
--------------------------------------

All devices have ``get_settings`` and ``apply_settings`` methods which, correspondingly, return Python dictionaries with the most common settings or take these dictionaries and apply the contained settings. These can be used to easily store and re-apply device configuration within a script.

Additionally, there is ``get_full_info`` method, which return as complete information as possible. It is particularly useful to check the device status and see if it is connected and working properly, and to save the devices configuration when, e.g., acquiring the data. Finally, the settings can also be accessed through ``.dv`` attribute, which provides dictionary-like interface::

    >>> wheel = Thorlabs.FW("COM1")  # connect to FW102 motorized filter wheel
    >>> wheel.get_position()
    1
    >>> wheel.get_settings()
    {'pcount': 6,
    'pos': 1,
    'sensors_mode': 'off',
    'speed_mode': 'high',
    'trigger_mode': 'in'}
    >>> wheel.dv["pos"]
    1
    >>> wheel.apply_settings({"pos":2})
    >>> wheel.get_position()
    2
    >>> wheel.dv["pos"] = 3
    >>> wheel.get_position()
    3
    >>> wheel.close()


Dependencies and external software
--------------------------------------

Many devices require external software not provided with this package. 

The simpler devices using serial connection (either with an external USB-to-Serial adapter, or a similar built-in chip) only need the drivers (either standard adapter drivers, or, e.g., Thorlabs APT software). If they already show up as serial communication devices in the OS, no additional software is normally needed. Similarly, devices using Ethernet connection do not need any external drives, as long as they are properly connected to the network. Finally, devices using Visa connection require NI VISA Runtime, which is freely available from the `National Instruments website <https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html>`__. See also `PyVISA <https://pyvisa.readthedocs.io/en/master/>`__ for details.

Devices which require manufacturer DLLs are harder to set up. For most of them, at the very least, you need to install the manufacturer-provided software for communication. Frequently it already includes the necessary libraries, which means that nothing else is required. However, sometimes you would need to download either an additional SDK package, or DLLs directly from the website. Since these libraries take a lot of space and are often proprietary, they are not distributed with the pylablib.

Note that DLLs can have 32-bit and 64-bit version, and it should agree with the Python version that you use. Unless you have a really good reason to do otherwise, it is strongly recommended to use 64-bit Python, which means that you would need 64-bit DLLs (which is the standard in most cases these days). To check your Python bitness, you can read the prompt when running the Python console, or run ``python -c "import platform; print(platform.architecture()[0])"`` in the command line.

In addition, you need to provide pylablib with the path to the DLLs. In many cases it checks the standard locations such as the default ``System32`` folder (used, e.g., in DCAM or IMAQ cameras) or defaults paths for manufacturer software (such as ``C:/Program Files/Andor SOLIS`` for Andor cameras). If the software path is different, or if you choose to obtain DLLs elsewhere, you can also explicitly provide path by setting the library parameter::

    import pylablib as pll
    pll.par["devices/dlls/andor_sdk3"] = "path/to/dlls"
    from pylablib.devices import Andor
    cam = Andor.AndorSDK3Camera()

All of these requirements are described in detail for the specific devices.


Advanced examples
--------------------------------------

Connecting to a Cryomagnetics LM500 level meter and reading out the level at the first channel::

    from pylablib.devices import Cryomagnetics  # import the device library
    with Cryomagnetics.LM500("COM1") as lm:
        level = lm.get_level(1)  # read the level

Stepping the M Squared laser wavelength and recording an image from the Andor IXON camera at each step::

    from pylablib.aux_libs.devices import M2, Andor  # import the device libraries
    with M2.M2ICE("192.168.0.1", 39933) as laser, Andor.AndorCamera() as cam:  # connect to the devices
        # change some camera parameters
        cam.set_shutter("open")
        cam.set_exposure(50E-3)
        cam.set_amp_mode(preamp=2)
        cam.set_EMCCD_gain(128)
        cam.setup_image_mode(vbin=2, hbin=2)
        # setup acquisition mode
        cam.set_acquisition_mode("cont")
        cam.setup_cont_mode()
        # start camera acquisition
        cam.start_acquisition()
        wavelength = 740E-9  # initial wavelength (in meters)
        images = []
        while wavelength < 770E-9:
            laser.tune_wavelength_table(wavelength)  # tune the laser frequency (using coarse tuning)
            time.sleep(0.5)  # wait until the laser stabilizes
            cam.wait_for_frame()  # ensure that there's a frame in the camera queue
            frame = cam.read_newest_image()
            images.append(frame)
            wavelength += 0.5E-9


Available devices
--------------------------------------

.. include:: all_devices_list.txt