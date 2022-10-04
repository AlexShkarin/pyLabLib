.. _sensors_cryocon:

.. note::
    Basic sensors communication concepts are described on the corresponding :ref:`page <basic_sensors_basics>`

CryoCon temperature sensors
==============================

CryoCon manufactures a range of temperature sensor controllers and resistance bridges, which are also used for temperature sensing. The code has been tested with CryoCon 14C temperature controller.

The main device class is :class:`pylablib.devices.Cryocon.Cryocon1x<.Cryocon.base.Cryocon1x>`.


Software requirements
-----------------------

The device provides a bare RS232 interface, so any appropriate USB-to-RS232 adapter should work.


Connection
-----------------------

Since the devices are identified as COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import Cryocon
    >> sensor = Cryocon.Cryocon1x("COM5")
    >> sensor.close()



Operation
-----------------------


The operation of this temperature sensor is fairly straightforward, but there is a couple of points to keep in mind:

    - Like most similar devices, querying temperature using :meth:`.Cryocon1x.get_temperature` immediately returns the most recently measured value. Re-measurement is periodically initiated by the devices itself.