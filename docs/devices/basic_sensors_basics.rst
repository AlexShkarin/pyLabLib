.. _basic_sensors_basics:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

Basics of sensors communication
======================================

Basic example
--------------------------------------

Basic sensors usually only implement a handful of functions related to reading out the measurements (possibly on different channels) and setting up measurements modes::

    >> gauge = Pfeiffer.TPG260("COM1")  # connect to the gauge
    >> gauge.enable(1)  # enable the first channel (usually it's already enabled)
    >> gauge.get_pressure()  # read pressure at the default channel (1)
    100E3
    >> gauge.close()


Application notes and examples
-------------------------------------------

Here we talk more practically about using pylablib to perform commons sensor tasks.


Readout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The main readout methods almost always start with ``get_`` prefix, e.g., ``get_pressure``, ``get_temperature``, or ``get_level``. In some cases there would be two different measurement modes: one which just reads the latest measurement result, and one which initializes the measurement, waits until it's done, and returns the result. These two approaches may be implemented differently in different devices, and it is addressed in their description::

    >> meter = Cryomagnetics.LM500("COM1")
    >> meter.get_level(1)  # immediately return the latest reading
    20.0
    >> meter.get_level(1)  # return the same reading
    20.0
    >> meter.measure_level(1)  # initialize a new measurement; takes some time
    19.8


Non-numerical values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases the readout method would return a non-numerical values. This usually happens when the sensor readings are outside of its range, or if it is in a wrong state (off, warming up, error, etc.) These cases are documented in the querying method description::

    >> meter = Ophir.VegaPowerMeter("COM1")
    >> meter.get_power()  # power is higher than the current range
    'over'
    >> meter.set_range_idx(0)  # set the maximal power range
    >> meter.get_power()  # now the reading is numerical
    10E-3


Units
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unless absolutely necessary and obvious, all the readout values are specified in SI units (even, e.g., laser frequency in Hz, or pressure in Pa). In rare cases when the devices allows for selection of readout units (e.g., Pfeiffer TPG260 gauges), it only affects the displayed value, but not the results returned by the corresponding methods::

    >> gauge = Pfeiffer.TPG260("COM1")
    >> gauge.set_units("pa")
    >> gauge.get_pressure()
    100E3
    >> gauge.set_units("mbar")
    >> gauge.get_pressure()  # pressure still in Pa
    100E3
    >> gauge.get_pressure(display_units=True)  # pressure in display units
    1000


Channel selection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some gauges support simultaneous readout on several channels. In this case, all of their methods take an additional ``channel`` (in most cases) argument, which specify the read channel.

The channels are usually specified by their index starting from 0 or 1, although some devices adopt more complicated labeling schemes (e.g., Lakeshore 218 temperature sensor can only assign a sensor type to a group of 4 sensors, which is labeled ``"A"`` or ``"B"``). The exact specification is given in the specific class description.


Currently supported sensors
-------------------------------------------
.. include:: basic_sensors_list.txt