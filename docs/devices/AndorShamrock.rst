.. _spectr_andor:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

Andor Shamrock spectrometers
============================

In addition to cameras, Andor has a set of spectrometers primarily designed to work with and communicate through those cameras. Among these Kymera and Shamrock spectrographs have a common configuration and API.

The code is located in :mod:`pylablib.devices.Andor`, and the main device class is :class:`pylablib.devices.Andor.ShamrockSpectrograph<.Shamrock.ShamrockSpectrograph>`.
It has been tested with Kymera 328i spectrograph connected via an Andor Newton camera through I2C interface.


Software requirements
-----------------------

Unfortunately, there is a large variety of different hardware setups and DLL combinations, which relate to each other in very non-obvious way. The possible adjustable parameters are

- Spectrograph connection: either via camera's I2C interface, or directly to the PC via a USB interface
- Camera AndorSDK2 DLL: on 64-bit systems it can be named ``atmcd64d.dll`` or ``atmcd64d_legacy.dll``, and it can come from Andor Solis or Andor SDK2.
- Spectrometer DLL; on 64-bit systems it can be named ``atspectrograph.dll``, ``ShamrockCIF.dll``, or ``ShamrockCIF64.dll``, and it might require Andor SDK2 DLLs (``atmcd64d.dll``, ``atmcd64d_legacy.dll``, ``atshamrock.dll``, ``atshamrock64.dll``) to be located in the same folder. it can come from Andor Solis, Andor SDK2 or MicroManager plugin available on Andor/Oxford website.

As mentioned above, there are three main sources of these libraries:

- Andor Solis, which can be obtained either with the camera, or from the `website <https://andor.oxinst.com/products/solis-software/>`__ upon registration.
- Andor SDK2, similarly obtained from the `website <https://andor.oxinst.com/products/software-development-kit/>`__ (the most recent version is `2.104.30084 <https://andor.oxinst.com/downloads/view/andor-sdk-2.104.30084.0>`__)
- MicroManager plugin, also obtained from the `website <https://andor.oxinst.com/products/spectrographs-solutions>`__ (``Software`` section; here is the `direct link <https://andor.oxinst.com/assets/uploads/downloads/mm-microspectroscopyplugin-1.0.0.zip>`__).

In general, it makes sense to try different combinations of DLLs and connection methods and see what works. To specify the exact DLL sources, you use the corresponding library parameters ``devices/dlls/andor_sdk2`` and ``devices/dlls/andor_shamrock``::

    import pylablib as pll
    pll.par["devices/dlls/andor_shamrock"] = "path/to/shamrock/dlls"
    pll.par["devices/dlls/andor_sdk2"] = "path/to/sdk2/dlls"
    from pylablib.devices import Andor
    cam = Andor.AndorSDK2Camera()
    spec = Andor.ShamrockSpectrograph()

Possible issues might include

- Not being able to find camera, spectrograph, or both. You can check for this by examining the outputs of ``Andor.get_cameras_number_SDK2()`` and ``Andor.list_shamrock_spectrographs()``
- Not being able to connect both to the camera and the spectrograph simultaneously. It might be possible to connect to one of them individually, but once one connection is opened, the other one gets blocked. You can check for this directly by trying to open both the camera and the spectrograph and making sure that it works (if it does not, it will look the same as if the camera/spectrograph disappear as soon as spectrograph/camera is connected). It might be less of an issue if the spectrograph is connected directly via USB rather than via I2C through the camera.
- In some cases (especially when using libraries from the MicroManager plugin), spectrograph is identified correctly and can be connected to, but the connection is corrupted, and queries return nonsense values.
- Rarely, the spectrometer state might get corrupted, and it would stop being identified even in Andor Solis. In this case, you can try power cycling the spectrometer, camera and PC, as well as temporarily changing the spectrometer connection method (USB generally seems more stable). Just as a precaution, it is recommended to store a backup of the spectrograph EEPROM configuration, which can be done through Andor Solis. To do that, you need to go to the ``Hardware -> Spectrograph Setup`` window in the top menu, there click on the ``System Configuration`` button, and there export the EEPROM state via ``Save to File...`` button.

Connection
-----------------------

The spectrographs are identified by their index, starting from zero. To list the connected spectrographs, you can run :func:`Andor.list_shamrock_spectrographs<.Shamrock.list_spectrographs>`::

    >> from pylablib.devices import Andor
    >> Andor.list_shamrock_spectrographs()
    ["KY-1234"]
    >> spec = Andor.ShamrockSpectrograph(idx=0)
    >> spec.close()

In addition, in order to acquire the spectra you need to establish the connection to the corresponding camera using :ref:`Andor cameras interface <cameras_andor>`. It is generally recommended to open the camera connection before the spectrograph to avoid software conflicts.

Operation
~~~~~~~~~~~~~~~~~~~~~~~~

The operation of these spectrographs is relatively straightforward. Note that they only allow for control of the spectrometer part of the setup (e.g., gratings, slits, filters) and for calculation of the wavelength calibration, i.e., the wavelength corresponding to each camera pixel column. In order to actually acquire and image, you would need to establish a separate camera connection and acquire images from it independently (typically in the full vertical binning, FVB, mode)::

    >> from pylablib.devices import Andor
    >> cam = Andor.AndorSDK2Camera()  # camera should be connected first
    >> spec = Andor.ShamrockSpectrograph()
    >> spec.set_wavelength(600E-9)  # set 600nm center wavelength
    >> spec.setup_pixels_from_camera(cam)  # setup camera sensor parameters (number and size of pixels) for wavelength calibration
    >> wavelengths = spec.get_calibration()  # return array of wavelength corresponding to each pixel
    >> cam.set_image_mode("fvb")
    >> spectrum = cam.snap()[0]  # 1D array of the corresponding spectrum intensities
    >> cam.close()
    >> spec.close()