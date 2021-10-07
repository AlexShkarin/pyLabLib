.. _sensors_pfeiffer:

.. note::
    Basic sensors communication concepts are described on the corresponding :ref:`page <basic_sensors_basics>`

Pfeiffer pressure gauges
==============================

Pfeiffer manufactures a range of pressure gauges and controllers with several different standards and communication protocols. The code has been tested with Pfeiffer TPG260 series controller (specifically, TPG261) and Pfeiffer DPG202 controller.

The main device classes are :class:`pylablib.devices.Pfeiffer.TPG260<.Pfeiffer.base.TPG260>` and :class:`pylablib.devices.Pfeiffer.DPG202<.Pfeiffer.base.DPG202>`.


Software requirements
-----------------------

The devices provide a bare RS232 interface, so any appropriate USB-to-RS232 adapter should work.


Connection
-----------------------

Since the devices are identified as COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import Pfeiffer
    >> gauge = Pfeiffer.TPG260("COM5")
    >> gauge.close()


Operation
-----------------------

TPG260 series
~~~~~~~~~~~~~~~~~~~~~~~

The operation of this gauge is fairly straightforward, but there is a couple of points to keep in mind:

    - On measurement error :meth:`.TPG260.get_pressure` returns ``None``. To get the underlying issue, you can use :meth:`.TPG260.get_channel_status`
    - By default, the pressure is always returned in Pa regardless of the display units. This behavior can be overridden by setting ``display_units=True`` in :meth:`.TPG260.get_pressure`.
    - In case an error occurs, you can use :meth:`.TPG260.get_current_errors` to get the list of currently active errors and :meth:`.TPG260.reset_error` to reset them.
    - This communication protocol for 350-series gauges (361, 362 and 366) is similar, so the device class should also be able to work with them. However, it has not been tested.

DPG202/TPG202 controller
~~~~~~~~~~~~~~~~~~~~~~~~

There is a variety of different controllers which implement a similar protocol: DPG202 and TPG202, as well as a variety of RS485-controlled gauges (e.g., CPT200). It is based on requesting parameters with certain 3-digit numbers. These are fairly consistent between the devices, for example, ``312`` stands for the software version, ``740`` for pressure, and ``349`` for the device name. However, different devices implement different subsets of these parameters. The supplied class provides a generic interface through :meth:`.DPG202.get_value` and :meth:`.DPG202.comm` methods, which, correspondingly, request or set a value of a given parameter given its number (e.g., ``740``) and datatype (e.g., ``"string"``, ``"u_expo_new"``, or ``"u_short_int"``). Both of these pieces of information are usually provided in the controller or gauge manual in the ``Parameter overview`` (or similar-named) section. Currently the device class provides only the most basic functionality::

    >> from pylablib.devices import Pfeiffer
    >> gauge = Pfeiffer.DPG202("COM5")
    >> gauge.get_pressure()  # pressure in Pa
    9.78E4
    >> gauge.get_value(740,"u_expo_new")  # request the parameter directly, yields pressure in mBar
    9.78E2
    >> gauge.close()