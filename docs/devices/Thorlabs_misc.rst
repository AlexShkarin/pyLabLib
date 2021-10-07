.. _misc_thorlabs:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

Miscellaneous Thorlabs devices
==============================

Thorlabs has a variety of devices implementing different serial communication protocols, mostly related to optomechanics. Their requirements and general approach are still fairly similar, so they are all collected here.


Software requirements
-----------------------

Most devices provide either a bare RS232 interface, or a USB connection with a built-in USB-to-RS232 chip. In either case, they are automatically recognized as serial ports, and no additional software is required. The only exception on this page is MFF101/102 motorized flip mount, which belongs to the :ref:`Kinesis devices <stages_thorlabs_kinesis>` and requires APT software.


Connection
-----------------------

Most of the devices are identified as COM ports, so they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import Thorlabs
    >> wheel = Thorlabs.FW102("COM5")
    >> wheel.close()

The only exception is MFF101/102, which is identified by its serial number (more details are given at the :ref:`Kinesis devices page <stages_thorlabs_kinesis>`).

Operation
-----------------------

.. _misc_thorlabs_mff:

MFF101/102 flip mount
~~~~~~~~~~~~~~~~~~~~~~~

The class is provided as :class:`pylablib.devices.Thorlabs.MFF<.Thorlabs.kinesis.MFF>`. It allows for control of the flip mirror position, as well as changing its motion parameters and designations of its digital input and output.


.. _misc_thorlabs_fw:

FW102/212 filter wheel
~~~~~~~~~~~~~~~~~~~~~~~~

The class is proved as :class:`pylablib.devices.Thorlabs.FW<.Thorlabs.serial.FW>`.

In addition to setting the position, it allows to adjust speed settings and turn the indicator LED off to minimize light contamination. By default, the wheel also "respects bound" between the first and the last position. Usually, when one orders a move from, e.g., position 2 to 6 on a 6-position wheel, it would go along the shortest route, i.e., position 1. If this is an ND filter wheel (e.g., FW102CNEB), this leads to momentary increase of the transmitted power by ND0.5 (about factor of 3) compared to start and stop positions. To avoid that, the class breaks this move into several shorter (no longer than 1/3 of the wheel) moves, which never cross the boundary between the first and the last position. This takes a bit longer (as it requires several consecutive moves), but is generally safer. This behavior can be turned off by setting ``respect_bound=False`` on class creation.

Note that older version (1.0) of the filter wheel do not support the full range of options and operate on a slightly different protocol. This leads to crashes on at least some of the methods, e.g., :meth:`.FW.get_position`. If this is the case, you can try :class:`pylablib.devices.Thorlabs.FWv1<.Thorlabs.serial.FWv1>` instead.


.. _misc_thorlabs_mdt693:

MDT693/694 high-voltage source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The class is proved as :class:`pylablib.devices.Thorlabs.MDT69xA<.Thorlabs.serial.MDT69xA>`.

The class provides the ability to set and query the voltage on the three channels, as well as to query the total voltage range (it is set by a physical switch on the back panel, and can not be altered remotely).