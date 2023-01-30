.. _sensors_cryomagnetics:

.. note::
    Basic sensors communication concepts are described on the corresponding :ref:`page <basic_sensors_basics>`

Cryomagnetics level monitor
==============================

Cryomagnetics manufactures cryogenic liquid level monitors, which are used for monitoring liquid nitrogen or helium levels inside cryostats. The two level meters supported in the package are LM-500 and LM-510; despite difference in appearance, their functionalities are very similar, so their interfaces are nearly identical.

The main device classes are :class:`pylablib.devices.Cryomagnetics.LM500<.Cryomagnetics.base.LM500>` and :class:`pylablib.devices.Cryomagnetics.LM500<.Cryomagnetics.base.LM510>`.


Software requirements
-----------------------

LM-500 provides a bare RS232 interface, so any appropriate USB-to-RS232 adapter should work. LM-510 has a USB interface with a built-in USB-to-RS232 adapter, which is automatically recognized as a serial port, so no additional software is required.


Connection
-----------------------

Since the devices are identified as COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import Cryomagnetics
    >> sensor = Cryomagnetics.LM510("COM5")
    >> sensor.close()



Operation
-----------------------


The operation of this temperature sensor is fairly straightforward, but there is a couple of points to keep in mind:

    - Upon connection the devices are automatically switched into the remote mode, which disables manual controls. If this mode is manually switched off (e.g., using ``Local`` button in LM-510), the device will no longer obey the remote commands, even though the readout would still work.
    - There are no specific commands for stopping a refill or resetting the timeout state after a timed-out refill. However, both can be achieved using :meth:`.LM500.reset` method.
    - Only LM-510 supports switching the automated refill option on and off using :meth:`.LM510.set_control_mode` method.
    - Like most similar devices, querying the level using :meth:`.LM500.get_level` immediately returns the most recently measured value. Re-measurement is periodically initiated by the devices itself, or can be initiated manually using :meth:`.LM500.start_measurement` or :meth:`.LM500.measure_level`.