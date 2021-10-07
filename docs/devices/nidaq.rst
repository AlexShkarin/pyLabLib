.. _daqs_nidaq:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

NI DAQmx interface
=======================

National Instruments produces lots of different data acquisition devices, which support digital and analog input and output, both immediate and clocked (depending on the exact device). They are controlled via a very universal `NI DAQmx <https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z000000P8baSAC>`__ interface. This interface is implemented in `python-nidaqmx <https://nidaqmx-python.readthedocs.io/en/latest/>`__ package, which provides a fairly close to original functionality, but with much more convenient Python wrappers. Pylablib implements a relatively thin wrapper around this package to present it in a way similar to the other device classes, and to simplify common tasks such as setting up voltage and counter input channels.

The main daq class is :class:`pylablib.devices.NI.NIDAQ<.NI.daq.NIDAQ>`. It has been tested with NI PCIe-6323, NI USB-6008, and NI USB-6363.

Software requirements
-----------------------

This interface uses NI DAQmx library, which is freely available on the `National Instruments website <https://www.ni.com/en-us/support/downloads/drivers/download.ni-daqmx.html>`__. Additionally, it needs `python-nidaqmx <https://nidaqmx-python.readthedocs.io/en/latest/>`__ package (not to be confused with pydaqmx). It is not automatically installed with the base version of pylablib, and can be obtained from PyPi either separately as

.. code-block:: none

    pip install nidaqmx

or with the expanded pylablib version

.. code-block:: none

    pip install pylablib[devio-full]


Connection
-----------------------

The devices are identified by their name, such as ``"Dev1"``. To list all of the connected devices together with their basic information, you can run :func:`NI.list_nidaqmx_devices<.NI.daq.list_devices>`::

    >> from pylablib.devices import NI
    >> NI.list_nidaqmx_devices()
    [TDeviceInfo(name='Dev1', model='USB-6008', serial_number='01234567')]
    >> daq = NI.NIDAQ("Dev1")
    >> daq.close()


Operation
------------------------

The typical use case involves setting up different input and output channels, starting acquisition, and acquiring some number of samples::

    from pylablib.devices import NI
    daq = NI.NIDAQ("Dev1")
    daq.add_voltage_input("vin", "ai0")  # add voltage input named "vin" on the terminal "ai0"
    daq.add_voltage_input("vin2", "ai1", rng=(-1,1))  # add second channel with a smaller range of +/- 1V
    daq.add_digital_input("din", "port0/line0")
    daq.setup_clock(100)  # setup 100Hz sampling clock
    trace = daq.read(100)  # start acquisition, read finite number of samples, and stop it again
    # now do continuous acquisition + processing loop
    nsamples = 0
    daq.start()  # start continuous acquisition
    while nsamples<1000:
        sample = daq.read()
        ... process sample
        nsamples+=1
    daq.stop()

The class provide basic methods to set up analog, digital, and counter inputs, and analog and digital outputs. All the analog and digital inputs are synchronized to the same clock, which is the default analog input sample clock (``ai/SampleClock``) by default. It is also possible to set up the external clock via :meth:`.NIDAQ.setup_clock` and export the sampling clock via :meth:`.NIDAQ.export_clock`. Not that not all devices support clocked digital inputs, which means that setting up digital inputs there would raise an error.

By default, the counter inputs are synchronized to the same clock, although it is possible to change that. The counter inputs have 3 modes for output values: bare counter (accumulates the number of counts), differential (number of new counts between the two sampling points), and rate (same as differential, but normalized by the sampling rate). In case of external clock, when the sampling rate is a priori unknown, it might be useful to setup a clock rate counter input to determine this clock rate via :meth:`.NIDAQ.add_clock_period_input`.

Acquisition is controlled with :meth:`.NIDAQ.start` and :meth:`.NIDAQ.stop` methods, and the readout is performed via :meth:`.NIDAQ.read`. The result of this is always a 2D numpy array, where the first index corresponds to samples and the second to channels. The order of channels can be obtained from :meth:`.NIDAQ.get_input_channels`.

The outputs can be either analog or digital. The digital outputs are always immediate, i.e., they immediately produce and hold the latest output value. The analog outputs can work in two modes: either immediate, or clocked. The mode is set up via :meth:`.NIDAQ.setup_voltage_output_clock`. In this case, it is possible to output a list of values, which produces a waveform clocked according to the specified clock: either a separate clock source (default), or the analog input clock, which makes voltage input and output synchronized.