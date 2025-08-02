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



.. _vnas_agilent:

Agilent VNAs
==============================

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

Agilent produces a large number of different vector network analyzers (VNAs). The library currently supports Agilent E5071C VNA.

The main device class is :class:`pylablib.devices.Agilent.VNA.E5071C<.Agilent.vna.E5071C>`.

Software requirements
-----------------------

These VNAs use NI VISA communication interface. Hence, it requires NI VISA Runtime, which is freely available from the `National Instruments website <https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html>`__


Connection
-----------------------

The devices are identified by their VISA connection strings, which typically start with ``USB0::0x0699``, e.g., ``"USB0::0x0957::0x0D09::MY00000000::0::INSTR"``. To get a list of all connected VISA-enabled devices, you can run ``pylablib.list_backend_resources("visa")``::

    >> import pylablib as pll
    >> pll.list_backend_resources("visa")
    ('USB0::0x0957::0x0D09::MY00000000::0::INSTR',)
    >> from pylablib.devices import Agilent
    >> vna = Agilent.VNA.E5071C("USB0::0x0957::0x0D09::MY00000000::0::INSTR")
    >> vna.close()

Operation
------------------------

The method names are self-explanatory. Currently only basic operations are supported: frequency range, IF bandwidth and averaging setup, output level and status setup, S parameter acquisition.