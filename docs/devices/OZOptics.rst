.. _misc_ozoptics:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

OZ Optics devices
==============================

OZ Optics provides a variety of mostly fiber-optics related devices. Pylablib covers some of its fiber optomechanics solutions: polarization controller, tunable filter and variable attenuator. Their requirements and general approach are fairly similar, so they are all collected here.


Software requirements
-----------------------

All the devices provide either a bare RS232 interface, or a USB connection with built-in USB-to-RS232 chip. In either case, they are automatically recognized as serial ports, and no additional software is required.


Connection
-----------------------

The devices are identified as COM ports, so they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import OZOptics
    >> ctl = OZOptics.EPC04("COM5")
    >> ctl.close()

Operation
-----------------------

.. _misc_ozoptics_epc04:

EPC04 fiber polarization controller
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The class is proved as :class:`pylablib.devices.OZOptics.EPC04<.OZOptics.base.EPC04>`. It lets the user change the 4 control voltages, switch between DC and AC (scrambling) modes, and change the AC frequency.


.. _misc_ozoptics_dd100:

DD100 fiber attenuator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The class is proved as :class:`pylablib.devices.OZOptics.DD100<.OZOptics.base.DD100>`. It simply lets the user query and change the attenuation, as well as home the device. Note that homing is required once after the device power up, and it might in general sweep over the whole range of attenuations.


.. _misc_ozoptics_tf100:

TF100 fiber filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The class is proved as :class:`pylablib.devices.OZOptics.TF100<.OZOptics.base.TF100>`. It simply lets the user query and change the central wavelength, as well as home the device. Note that homing is required once after the device power up, and it might in general sweep over the whole range of wavelengths.