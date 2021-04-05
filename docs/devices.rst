.. _devices:

=======================
Specific device classes
=======================

.. note::
    Some device dlls are only available on GitHub. See :ref:`install-github` for how to install it.

----------------
General concepts
----------------

Most devices share common methods and approach to make them more predictable and easier to use.

First, the device identifier / address needs to be provided by user during the device object creation, and it is automatically connected. The devices have ``open`` and ``close`` methods but the device also works as a resource (with Python ``with`` statement), so these usually aren't used explicitly.

The devices usually have ``get_settings`` and ``apply_settings`` methods which return Python dictionaries with the most common settings or take these dictionaries and apply them.
In addition, there are ``get_full_status`` and ``get_full_info`` functions, which return progressively more information (``get_full_status`` adds variable status information which cannot be changed by user, and ``get_full_info`` adds constant device information, such as model name and serial number).
``get_full_info`` can be particularly useful to check the device status and see if it is connected and working properly.

Devices of the same kind (e.g., cameras or translation stages) aim to have consistent overlapping interfaces (where it makes sense), so different devices are fairly interchangeable in simple applications.

--------
Examples
--------

Connecting to a Cryomagnetics LM500 level meter and reading out the level at the first channel::

    from pylablib.aux_libs.devices import Cryomagnetics  # import the device library
    # Next, create the device object and connect to the device;
    #   the connection is automatically opened on creation, and closed when the ``with`` block is ended
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


---------------
List of devices
---------------
..
    ===================================    ==============================    =================================================================================    =======================================================================================
    Device                                 Kind                              Module                                                                               Comments
    ===================================    ==============================    =================================================================================    =======================================================================================
    M Squared ICE BLOC                     Laser                             :mod:`M2 <pylablib.aux_libs.devices.M2>`
    Pure Photonics PPCL200                 Laser                             :mod:`PurePhotonics <pylablib.aux_libs.devices.PurePhotonics>`                       In CBDX1 chassis
    Lighthouse Photonics SproutG           Laser                             :mod:`LighthousePhotonics <pylablib.aux_libs.devices.LighthousePhotonics>`
    LaserQuantum Finesse laser             Laser                             :mod:`LaserQuantum <pylablib.aux_libs.devices.LaserQuantum>`
    Agilent HP8168F                        Laser                             :mod:`AgilentLasers <pylablib.aux_libs.devices.AgilentLasers>`
    Nuphoton NP2000                        EDFA                              :mod:`NuPhoton <pylablib.aux_libs.devices.NuPhoton>`
    HighFinesse WS/6 and WS/7              Wavemeter                         :mod:`HighFinesse <pylablib.aux_libs.devices.HighFinesse>`
    Andor Shamrock                         Spectrometer                      :mod:`Andor <pylablib.aux_libs.devices.AndorShamrock>`                               Tested with Andor SR-303i
    Andor SDK2 interface                   Camera                            :mod:`Andor <pylablib.aux_libs.devices.Andor>`                                       Tested with Andor IXON and Luca
    Andor SDK3 interface                   Camera                            :mod:`Andor <pylablib.aux_libs.devices.Andor>`                                       Tested with Andor Zyla
    Hamamatsu DCAM interface               Camera                            :mod:`DCAM <pylablib.aux_libs.devices.DCAM>`                                         Tested with ORCA-Flash 4.0 (C11440-22CU)
    NI IMAQdx interface                    Camera                            :mod:`IMAQdx <pylablib.aux_libs.devices.IMAQdx>`                                     Tested with Photon Focus HD1-D1312 with GigE connection
    NI IMAQ interface                      Camera                            :mod:`IMAQ <pylablib.aux_libs.devices.IMAQ>`                                         Tested with NI PCI-1430 frame grabber
    Photon Focus PFCam interface           Camera                            :mod:`PhotonFocus <pylablib.aux_libs.devices.PhotonFocus>`                           Tested with MV-D1024E and CameraLink connection with NI PCIe-1433 frame grabber (via IMAQ)
    PCO SC2 interface                      Camera                            :mod:`PCO_SC2 <pylablib.aux_libs.devices.PCO_SC2>`                                   Tested with PCO.edge 5.5 CL and PCO.edge CLHS
    Ophir Vega                             Optical power meter               :mod:`Ophir <pylablib.aux_libs.devices.Ophir>`
    Thorlabs PM100D                        Optical power meter               :mod:`Thorlabs <pylablib.aux_libs.devices.Thorlabs>`
    OZ Optics TF100                        Tunable optical filter            :mod:`OZOptics <pylablib.aux_libs.devices.OZOptics>`
    OZ Optics DD100                        Variable optical attenuator       :mod:`OZOptics <pylablib.aux_libs.devices.OZOptics>`
    OZ Optics EPC04                        Polarization controller           :mod:`OZOptics <pylablib.aux_libs.devices.OZOptics>`
    Agilent AWG33220A                      Arbitrary waveform generator      :mod:`AgilentElectronics <pylablib.aux_libs.devices.GenericAWGs>`
    Agilent AWG33500                       Arbitrary waveform generator      :mod:`AgilentElectronics <pylablib.aux_libs.devices.GenericAWGs>`                    Tested with Agilent 33509B
    Rigol DG1000                           Arbitrary waveform generator      :mod:`AgilentElectronics <pylablib.aux_libs.devices.GenericAWGs>`                    Tested with DG1022
    Instek AFG-2225                        Arbitrary waveform generator      :mod:`AgilentElectronics <pylablib.aux_libs.devices.GenericAWGs>`                    Tested with Instek AFG-2225
    Agilent N9310A                         Microwave generator               :mod:`AgilentElectronics <pylablib.aux_libs.devices.AgilentElectronics>`
    Vaunix LMS (Lab Brick)                 Microwave generator               :mod:`Vaunix <pylablib.aux_libs.devices.Vaunix>`
    Thorlabs MDT693/4A                     High voltage source               :mod:`Thorlabs <pylablib.aux_libs.devices.Thorlabs>`
    Agilent AMP33502A                      DC amplifier                      :mod:`AgilentElectronics <pylablib.aux_libs.devices.AgilentElectronics>`
    Rigol DSA1030A                         Microwave spectrum analyzer       :mod:`Rigol <pylablib.aux_libs.devices.Rigol>`
    Agilent HP8712B, HP8722D               Vector network analyzers          :mod:`AgilentElectronics <pylablib.aux_libs.devices.AgilentElectronics>`
    Tektronix DPO2014, TDS2000, MDO3000    Oscilloscopes                     :mod:`Tektronix <pylablib.aux_libs.devices.Tektronix>`
    NI DAQ interface                       NI DAQ devices                    :mod:`NI <pylablib.aux_libs.devices.NI>`                                             Wrapper around the `nidaqmx <https://nidaqmx-python.readthedocs.io/en/latest/>`_ package. Tested with NI USB-6008 and NI PCIe-6323
    Zurich Instruments HF2 / UHF           Lock-in amplifiers                :mod:`ZurichInstruments <pylablib.aux_libs.devices.ZurichInstruments>`
    Arcus PerforMax                        Translation stage                 :mod:`Arcus <pylablib.aux_libs.devices.Arcus>`                                       Tested with PMX-4EX-SA stage.
    SmarAct SCU3D                          Translation stage                 :mod:`SmarAct <pylablib.aux_libs.devices.SmarAct>`
    Attocube ANC300                        Piezo slider controller           :mod:`Attocube <pylablib.aux_libs.devices.Attocube>`                                 Only tested with Ethernet or Serial connection
    Attocube ANC350                        Piezo slider controller           :mod:`Attocube <pylablib.aux_libs.devices.Attocube>`                                 Only tested with USB connection
    Trinamic TMCM1110                      Stepper motor controller          :mod:`Trinamic <pylablib.aux_libs.devices.Trinamic>`
    Thorlabs KDC101                        DC servo motor controller         :mod:`Thorlabs <pylablib.aux_libs.devices.Thorlabs>`
    Thorlabs K10CR1                        Motorized rotation mount          :mod:`Thorlabs <pylablib.aux_libs.devices.Thorlabs>`
    Thorlabs FW102/202                     Motorized filter wheel            :mod:`Thorlabs <pylablib.aux_libs.devices.Thorlabs>`
    Thorlabs MFF                           Motorized flip mount              :mod:`Thorlabs <pylablib.aux_libs.devices.Thorlabs>`
    Cryomagnetics LM500/510                Cryogenic level meter             :mod:`Cryomagnetics <pylablib.aux_libs.devices.Cryomagnetics>`
    Lakeshore 218 and 370                  Temperature controllers           :mod:`Lakeshore <pylablib.aux_libs.devices.Lakeshore>`
    MKS 9xx                                Pressure gauge                    :mod:`MKS <pylablib.aux_libs.devices.MKS>`
    Pfeiffer TPG261                        Pressure gauge                    :mod:`Pfeiffer <pylablib.aux_libs.devices.Pfeiffer>`
    ===================================    ==============================    =================================================================================    =======================================================================================

All the modules are located in :mod:`pylablib.devices`.

------------------------
Additional requirements
------------------------

First, any device using ``PyVISA`` require NI VISA to be installed. See `PyVISA <https://pyvisa.readthedocs.io/en/master/>`_ for details.

Second, some devices need dlls supplied by the manufacturer:

    - Andor SDK2 cameras: require `atmcd.dll` (currently supplied for x64 and x86). Can be obtained with Andor Solis software. If Andor Solis is installed in the default location, these dlls are accessed automatically. It might be called `atmcd64d_legacy.dll` or `atmcd32d_legacy.dll` (depending on the Solis version and Python bitness), but it needs to be renamed to `atmcd.dll` when placed into `aux_libs/devices/libs/x64` (or `x32`) folder.
    - Andor SDK3 cameras: require several `at*.dll`: `atcore.dll`, `atblkbx.dll`, `atcl_bitflow.dll`, `atdevapogee.dll`, `atdevregcam.dll`, `atusb_libusb.dll`, `atusb_libusb10.dll` (currently supplied only for x64). Has potential incompatibilities between different versions of Windows; tested with Windows 7 x64 and Andor Solis 4.30.30034.0. Can be obtained with Andor Solis software. If Andor Solis is installed in the default location, these dlls are accessed automatically.
    - PCO SC2 cameras: require several `SC2_*.dll`: `SC2_Cam.dll`, `sc2_cl_me4.dll`, `sc2_cl_mtx.dll`, `sc2_cl_nat.dll`, `sc2_cl_ser.dll`, `sc2_clhs.dll`. These are provided with pco.sdk.
    - Arcus PerforMax translation stages: require `PerformaxCom.dll` and `SiUSBXp.dll`.
    - HighFinesse WS/6 and WS/7 wavemeters: require `wlmData.dll`. Each device needs a unique dll supplied by the manufacturer. Currently generic version for WS/6 and WS/7 are given, but they are not guaranteed to not work properly. One can either supply DLL path on creation of the device class, or place it into `aux_libs/devices/libs/x64` (or `x32`) folder; in the latter case, it should be renamed to `wlmData6.dll` or `wlmData7.dll` depending on the wavemeter model (WS/6 or WS/7).
    - SmarAct SCU3D translation stage controller: requires `SCU3DControl.dll`.

Many of these are supplied with this library (only on GitHub), but they can be removed in future versions (e.g., for compatibility or legal reasons), and not all of them are present for x86 applications. If you installed the library using `pip`, you can download the dll's on GitHub (they are located in ``pylablib/aux_libs/devices/libs/``) and place them into the package folder (correspondingly, into ``aux_libs/devices/libs/`` inside the main package folder, which is usually something like ``Python36/Lib/site-packages/pylablib/``).

Third, some devices need additional software installed:

    - IMAQ cameras: National Instruments IMAQ library.
    - IMAQdx cameras: National Instruments IMAQdx library.
    - Photon Focus cameras: Photon Focus PFRemote software.
    - Hamamatsu DCAM cameras: DCAM software (Hamamatsu HOKAWO) and drivers.
    - Andor cameras: Andro Solis software and drivers
    - NI DAQs: National Instruments NI-DAQmx library (with C support; just Runtime is sufficient).
    - HighFinesse: manufacturer-provided drivers and software (specific to the particular wavemeter).
    - Thorlabs MFF: Kinesis/APT software.
    - Trinamic hardware: Trinamic TMCL-IDE (needed to install device drivers)
    - Arcus PerforMax software: Arcus Drivers and Tools, Arcus USB Series and Arcus Performax Series software (needed to install device drivers).
    - Zurich Instruments: manufacturer provided software and Python libraries.

The list might be incomplete, and it does not include drivers for all USB devices.