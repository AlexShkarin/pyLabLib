.. _rigol:


Rigol manufactures a large variety of electrical test and measurement equipment, including signal generators, oscilloscopes, multimeters, power supplies, etc.

.. _rigol_power_supply:

Rigol laboratory power supplies
===============================

There are different kinds of power supplies with somewhat different capabilities. The code has been tested with Rigol DP1116A.

The main device class is :class:`pylablib.devices.Rigol.DP1116A<.Rigol.power_supply.DP1116A>`.


Software requirements
-----------------------

These power supplies use NI VISA communication interface. Hence, it requires NI VISA Runtime, which is freely available from the `National Instruments website <https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html>`__


Connection
-----------------------

The devices are identified by their VISA connection strings, which typically start with ``USB0::0x1AB1``, e.g., ``"USB0::0x1AB1::0x0E10::DP1A000000000::INSTR"``. To get a list of all connected VISA-enabled devices, you can run ``pylablib.list_backend_resources("visa")``::

    >> import pylablib as pll
    >> pll.list_backend_resources("visa")
    ('USB0::0x1AB1::0x0E10::DP1A000000000::INSTR',)
    >> from pylablib.devices import Rigol
    >> supply = Rigol.DP1116A("USB0::0x1AB1::0x0E10::DP1A000000000::INSTR")
    >> supply.close()



Operation
-----------------------

The operation of this multimeter is fairly straightforward, but there is are some points to keep in mind:

    - Note that the supply supports different output ranges (for DP1116A it's ``"16V"`` or ``"32V"``), which trike different balance between output voltage and current. Other power supplies might support different output ranges, in which case the related method will raise an error or lead to communication timeout.