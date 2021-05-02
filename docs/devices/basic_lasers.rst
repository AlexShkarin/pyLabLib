.. _basic_lasers:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

Basic lasers
======================================

Basic example
--------------------------------------

Basic lasers (such as pump lasers) usually only have very basic power-related functionality: turning it on and off, setting power, and controlling and/or requesting the shutter state::

    >> laser = LaserQuantum.Finesse("COM1")  # connect to the laser
    >> laser.set_output_power(10.)  # set 10W output power
    >> laser.enable()  # enable the laser
    >> laser.get_output_power()  # laser hasn't ramped up up yet
    0.1
    >> time.sleep(30.)  # wait until the ramp up is done
    >> laser.get_output_power()
    10.0
    >> laser.enable(False)
    >> laser.close()


.. _basic_lasers_lp_sprout:

Lighthouse Photonics Sprout
--------------------------------------

Lighthouse Photonics Sprout laser implements the same basic functionality, with some small additions like reading the interlock status, output mode, temperatures, etc.

The device class is :class:`pylablib.devices.LighthousePhotonics.SproutG<.LighthousePhotonics.base.SproutG>`.

Since the device shows up as a COM port, it uses the standard :ref:`connection method <devices_connection>`, and all you need to know to connect is its COM-port address::

    from pylablib.devices import LighthousePhotonics
    laser = LighthousePhotonics.SproutG("COM1")
    laser.close()


.. _basic_lasers_lq_finesse:

Laser Quantum Finesse
--------------------------------------

Laser Quantum Finesse laser implements the same basic functionality, with some small additions like controlling the shutter, reading the driving current, temperatures, etc.

The device class is :class:`pylablib.devices.LaserQuantum.Finesse<.LaserQuantum.base.Finesse>`.

Since the device shows up as a COM port, it uses the standard :ref:`connection method <devices_connection>`, and all you need to know to connect is its COM-port address::

    from pylablib.devices import LaserQuantum
    laser = LaserQuantum.Finesse("COM1")
    laser.close()