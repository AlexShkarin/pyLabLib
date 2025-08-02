.. _sensors_lakeshore:

.. note::
    Basic sensors communication concepts are described on the corresponding :ref:`page <basic_sensors_basics>`

Lakeshore temperature sensors
==============================

Lakeshore manufactures a range of temperature sensor controllers and resistance bridges, which are also used for temperature sensing. There is some overlap between different products, but they still use fairly distinct interfaces and interaction patterns. The code has been tested with Lakeshore 218 and Lakeshore 235 temperature controllers.

The main device classes are :class:`pylablib.devices.Lakeshore.Lakeshore218<.Lakeshore.base.Lakeshore218>` and :class:`pylablib.devices.Lakeshore.Lakeshore235<.Lakeshore.base.Lakeshore235>`.


Software requirements
-----------------------

The device provides a bare RS232 interface, so any appropriate USB-to-RS232 adapter should work.


Connection
-----------------------

Since the devices are identified as COM ports, they use the standard :ref:`connection method <devices_connection>`, and all you need to know is their COM-port address (e.g., ``COM5``)::

    >> from pylablib.devices import Lakeshore
    >> sensor = Lakeshore.Lakeshore218("COM5")
    >> sensor.close()

Note that the connection uses the standard which is fairly different from most RS232 controllers: 7 data bits, 1 parity bit, and 1 stop bit (as opposed to 8 data bits and no parity bit for most controllers). Hence, it is possible that not all RS232 controllers can communicate with it. In addition, they might need a null-modem (crossed Rx and Tx lines) RS232 cable.



Operation
-----------------------

.. Lakeshore 218
.. ~~~~~~~~~~~~~~~~~~~~~~~

The operation of this temperature sensor is fairly straightforward, but there is a couple of points to keep in mind:

    - Like most similar devices, querying temperature using :meth:`.Lakeshore218.get_temperature` immediately returns the most recently measured value. Re-measurement is periodically initiated by the devices itself.
    - It is possible to specify custom response curves by using :meth:`.Lakeshore218.set_curve_header` and :meth:`.Lakeshore218.set_curve`. However, you need to be careful, as it overwrites the stored user curves.