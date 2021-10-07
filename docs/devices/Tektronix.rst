.. _oscilloscopes_tektronix:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

Tektronix oscilloscopes
=======================

Tektronix produces a large number of very widespread oscilloscopes. They have strongly overlapping, though not entirely identical, interfaces. The library has been tested with TDS2002B, TDS2004B, and DBO2014B.

The generic oscilloscope class is :class:`pylablib.devices.Tektronix.ITektronixScope<.Tektronix.base.ITektronixScope>`, and the derived classes for specific devices are :class:`pylablib.devices.Tektronix.TDS2000<.Tektronix.base.TDS2000>` of TDS2000 series and :class:`pylablib.devices.Tektronix.DPO2000<.Tektronix.base.DPO2000>` for DPO2000/MSO2000 series.

Software requirements
-----------------------

These oscilloscopes use NI VISA communication interface. Hence, it requires NI VISA Runtime, which is freely available from the `National Instruments website <https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html>`__


Connection
-----------------------

The devices are identified by their VISA connection strings, which typically start with ``USB0::0x0699``, e.g., ``"USB0::0x0699::0x0364::C000001::INSTR"``. To get a list of all connected VISA-enabled devices, you can run ``pylablib.list_backend_resources("visa")``::

    >> import pylablib as pll
    >> pll.list_backend_resources("visa")
    ('USB0::0x0699::0x0364::C000001::INSTR',)
    >> from pylablib.devices import Tektronix
    >> osc = Tektronix.TDS2000("USB0::0x0699::0x0364::C000001::INSTR")
    >> osc.close()


Operation
------------------------

The method names are usually pretty self-explanatory. A typical operation involves setting up channels, scales, and trigger options, acquiring a waveform, and reading the result::

    from pylablib.devices import Tektronix
    osc = Tektronix.TDS2000("USB0::0x0699::0x0364::C000001::INSTR")  # connect to the oscilloscope
    osc.enable_channel([1,2])  # enable channels
    osc.set_horizontal_span(0.1)  # set up horizontal and vertical spans
    osc.set_vertical_span("CH1", 1)
    osc.set_vertical_span("CH2", 0.1)
    osc.setup_edge_trigger("CH1", 0., "dc", "rise")  # set up edge trigger on channel 1 at 0V threshold
    osc.grab_single(wait_timeout=10.)  # grab a single waveform and wait for up to 10s to finish acquisition
    sweeps = osc.read_multiple_sweeps([1,2])  # read out the waveforms
    osc.close()

However, there is a couple of points to keep in mind:

    - The acquisition is controlled using ``grab_`` methods. Generally, the most convenient way is to use :meth:`.ITektronixScope.grab_single` to acquire a single waveform (analogous to pressing a ``Single`` button on the oscilloscope panel). By default, this method waits until the acquisition is complete (i.e., the oscilloscope is triggered and the waveform is completely acquired) before continuing. You can also set ``wait=False`` to perform other operations in the meantime. The acquisition status can be queried via :meth:`.ITektronixScope.is_grabbing`, which returns ``True`` while the trigger is armed or while the data is recording, and ``False`` after the acquisition is done.
    - It appears that the software trigger does not work some time (~500 ms) after the acquisition is set up. If it is invoked in :meth:`.ITektronixScope.grab_single` method by supplying ``software_trigger=True``, a 300ms delay is added automatically. However, if you invoke it manually using :meth:`.ITektronixScope.force_trigger`, you should keep it in mind.
    - The waveform transfer is usually performed via :meth:`.ITektronixScope.read_sweep` or :meth:`.ITektronixScope.read_multiple_sweeps` methods. Since the waveform is transferred in raw form, it requires a preamble data (vertical and horizontal scales and offsets, data format, etc.) to translate into physical units. By default, it is acquired every time before the waveform transfer, which takes some time (up to ~200ms). Alternatively, one can acquire a preamble once and use it in subsequent reading. This method is faster, but will result in an incorrect scaling if the parameters are changed in the meantime (either remotely, or directly on the oscilloscope)::

        >> wfmpres = osc.osc.get_wfmpre([1,2])
        >> %time sweeps = osc.read_multiple_sweeps([1,2])
        Wall time: 2.2 s
        >> %time sweeps = osc.read_multiple_sweeps([1,2], wfmpres=wfmpres)
        Wall time: 450 ms

    - The device class attempts to determine the number of channels automatically on connection, based on which requests raise device errors. However, this process takes some time, and sometimes can raise errors on not fully SCPI-compliant devices. If that is the case, it is always possible to supply the number of channels on construction::

        >> osc = Tektronix.TDS2000("USB0::0x0699::0x0364::C000001::INSTR")  # use autodetection
        >> osc.get_channels_number()
        2
        >> osc.close()
        >> osc = Tektronix.TDS2000("USB0::0x0699::0x0364::C000001::INSTR", nchannels=2)  # specify manually