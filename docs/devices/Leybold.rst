.. _sensors_leybold:

.. note::
    Basic sensors communication concepts are described on the corresponding :ref:`page <basic_sensors_basics>`

Leybold pressure gauges
==============================

Leybold manufactures a range of pressure gauges and controllers with several different standards and communication protocols. The code has been tested with Leybold ITR90 pressure gauge using its built-in RS232 connection.

The main device classes are :class:`pylablib.devices.Leybold.ITR90<.Leybold.base.ITR90>`.


Software requirements
-----------------------

The devices provide a bare RS232 interface, so any appropriate USB-to-RS232 adapter should work.


Connection
-----------------------

Since the devices are identified as COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import Leybold
    >> gauge = Leybold.ITR90("COM5")
    >> gauge.close()


Operation
-----------------------

ITR90
~~~~~~~~~~~~~~~~~~~~~~~

The operation of this gauge is fairly straightforward, but there is a couple of points to keep in mind:

    - Device operates by constantly streaming its status updates. To get the most recent and most consistent data, you can use :meth:`.ITR90.get_update`. This is also how you access the gauge status and error states.
    - By default, the pressure is always returned in Pa regardless of the display units. This behavior can be overridden by setting ``display_units=True`` in :meth:`.ITR90.get_pressure`.