.. _awg_generic:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

Generic AWGs
=======================

There is a large variety of Arbitrary Waveform Generators, which have very similar characteristics and communication interface. 

The generic AWG class is :class:`pylablib.devices.AWG.GenericAWG<.AWG.generic.GenericAWG>`, and the derived classes for specific devices are :class:`pylablib.devices.AWG.Agilent33500<.AWG.specific.Agilent33500>` and :class:`pylablib.devices.AWG.Agilent33220A<.AWG.specific.Agilent33220A>` for two different Agilent AWGs, :class:`pylablib.devices.AWG.RigolDG1000<.AWG.specific.RigolDG1000>` for Rigol DG1000 series, :class:`pylablib.devices.AWG.RigolDG1020Z<.AWG.specific.RigolDG1020Z>` for Rigol DG1020Z series, :class:`pylablib.devices.AWG.TektronixAFG1000<.AWG.specific.TektronixAFG1000>` for Tektronix AFG1000 series, :class:`pylablib.devices.AWG.InstekAFG2000<.AWG.specific.InstekAFG2000>` for Instek GW 2000 series, :class:`pylablib.devices.AWG.RSInstekAFG21000<.AWG.specific.RSInstekAFG21000>` for Iso-Tech 21000 series (a clone of Instek AFG2000, but with a couple of bugs which needs to be worked around), and :class:`pylablib.devices.AWG.InstekAFG2225<.AWG.specific.InstekAFG2225>` for Instek GW 2225 (slightly advanced two-channel version of Instek AFG2000).

Software requirements
-----------------------

Most of these AWGs use NI VISA communication interface. Hence, they require NI VISA Runtime, which is freely available from the `National Instruments website <https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html>`__. However, Instek and Iso-Tech AWGs show up as virtual COM ports, so they require no additional software.


Connection
-----------------------

The devices are identified by their VISA connection strings, (e.g., ``"USB0::0x0699::0x0364::C000001::INSTR"``) or COM-port (e.g., ``"COM5"``). To get a list of all connected VISA-enabled devices, you can run ``pylablib.list_backend_resources("visa")``::

    >> import pylablib as pll
    >> pll.list_backend_resources("visa")
    ('USB0::0x09C4::0x0400::DG1D150200000::INSTR',)
    >> from pylablib.devices import AWG
    >> dev = AWG.RigolDG1000("USB0::0x09C4::0x0400::DG1D150200000::INSTR")
    >> dev.close()


Operation
------------------------

The method names are usually pretty self-explanatory. A typical operation involves setting up the function, its parameters, and controlling output::

    from pylablib.devices import AWG
    dev = AWG.RigolDG1000("USB0::0x09C4::0x0400::DG1D150200000::INSTR")  # connect to the device
    dev.set_function("square", 2)  # set up square waveform on the second channel
    dev.set_duty_cycle(20, 2)
    dev.set_output_range((-1, 1), 2)  # set output span from -1V to 1V
    dev.enable_output(channel=2)  # enable output
    dev.close()

However, there is a couple of points to keep in mind:

    - Since the same general class architecture supports both single-channel and multichannel devices, the channel argument is usually close to the end of the argument list and is not mandatory. If it is not supplied, it is chosen to be the current default channel (1 upon creation), which can be set using :meth:`.GenericAWG.select_current_channel`. Hence, int the example above we can write::

        dev.select_current_channel(2)  # now all methods assume channel 2
        dev.set_function("square")
        dev.set_duty_cycle(20)
        dev.set_output_range((-1, 1))
        dev.enable_output()
    
    - Similarly, some methods can be present but not applicable to the particular AWG (e.g., burst trigger related methods, phase synchronization methods, etc.) If this is the case, they will cause an error when called.