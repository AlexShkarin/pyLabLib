.. _sensors_agilent:

Agilent pressure gauges
==============================

.. note::
    Basic sensors communication concepts are described on the corresponding :ref:`page <basic_sensors_basics>`

Among other things, Agilent manufactures a range of pressure gauges and controllers. The code has been tested with Agilent XGS-600 controller with an analog board and FRG700 gauge.

The main device class is :class:`pylablib.devices.Agilent.XGS600<.Agilent.pressure.XGS600>`.


Software requirements
-----------------------

The devices provide a bare RS232 interface, so any appropriate USB-to-RS232 adapter should work.


Connection
-----------------------

Since the devices are identified as COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import Agilent
    >> gauge = Agilent.XGS600("COM5")
    >> gauge.close()


Operation
-----------------------

XGS-600 series controller
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The operation of this controller is fairly straightforward, but there is a couple of points to keep in mind:

    - The list of pressures returned by :meth:`.XGS600.get_all_pressures` only includes the installed boards, so it will changed when boards are installed or removed. On the other hand, the order does not depend on whether gauges are connected, since it return ``"nocbl"`` for any connectors without gauges.
    - By default, the pressure is always returned in Pa regardless of the display units. This behavior can be overridden by setting ``display_units=True`` in :meth:`.XGS600.get_all_pressures`.