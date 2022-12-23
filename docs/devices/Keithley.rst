.. _keithley:


Keithley (currently absorbed by Tektronix) manufactures a large variety of precision electrical test and measurement equipment.

.. _keithley_multimeter:

Keithley multimeters
==============================

.. note::
    Basic sensors communication concepts are described on the corresponding :ref:`page <basic_sensors_basics>`

There are different series of multimeters with somewhat different capabilities. The code has been tested with Keithley 2110 multimeter, but it should also be able to work with 2100 and 2010 series.

The main device class is :class:`pylablib.devices.Keithley.Keithley2110<.Keithley.multimeter.Keithley2110>`.


Software requirements
-----------------------

These multimeters use NI VISA communication interface. Hence, it requires NI VISA Runtime, which is freely available from the `National Instruments website <https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html>`__


Connection
-----------------------

The devices are identified by their VISA connection strings, which typically start with ``USB0::0x05E6``, e.g., ``"USB0::0x05E6::0x2110::0000001::INSTR"``. To get a list of all connected VISA-enabled devices, you can run ``pylablib.list_backend_resources("visa")``::

    >> import pylablib as pll
    >> pll.list_backend_resources("visa")
    ('USB0::0x05E6::0x2110::0000001::INSTR',)
    >> from pylablib.devices import Keithley
    >> meter = Keithley.Keithley2110("USB0::0x05E6::0x2110::0000001::INSTR")
    >> meter.close()



Operation
-----------------------

The operation of this multimeter is fairly straightforward, but there is a couple of points to keep in mind:

    - While all measurement modes are, in principle, supported, only some of them have implemented specific parameter changing (e.g., range or resolution): voltage and current (AC and DC), resistance (2-wire and 4-wire), capacitance, frequency and period (voltage and current). These methods allow for changing of specific parameters using methods like :meth:`.Keithley2110.get_vcr_function_parameters` (get voltage, current, or resistance measurement parameters) or :meth:`.Keithley2110.set_cap_function_parameters` (set capacitance measurement parameters).
    - At the same time, more universal :meth:`.Keithley2110.get_configuration` and :meth:`.Keithley2110.set_configuration` methods allow for changing basic parameters (range and resolution) for all of the applicable measurement functions (excluded are continuity, diode, and temperature modes).