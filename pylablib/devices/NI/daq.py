from ...core.devio import interface, comm_backend
from ...core.devio.comm_backend import reraise
from ...core.utils import general, funcargparse

import time
import numpy as np
import collections
import re

class NIError(comm_backend.DeviceError):
    """Generic NI error"""
class NIDAQmxError(NIError,comm_backend.DeviceBackendError):
    """NI DAQmx backend operation error"""

try:
    import nidaqmx
    DaqError=nidaqmx.DaqError
except ImportError:
    nidaqmx=None
    DaqError=None



def _check_nidaqmx():
    if nidaqmx is None:
        msg=(   "operation requires Python nidaqmx library. You can install it via PyPi as 'pip install nidaqmx'. "
                "If it is installed, check if it imports correctly by running 'import nidaqmx'")
        raise ImportError(msg)


TDeviceInfo=collections.namedtuple("TDeviceInfo",["name","model","serial_number"])
TVoltageOutputClockParameters=collections.namedtuple("TVoltageOutputClockParameters",["rate","sync_with_ai","continuous","samps_per_chan","autoloop"])
def get_device_info(name):
    """
    Get device info.

    Return tuple ``(name, model, serial)``.
    """
    _check_nidaqmx()
    d=nidaqmx.system.Device(name)
    return TDeviceInfo(d.name,d.product_type,"{:08X}".format(d.dev_serial_num or 0))
def list_devices():
    """List all connected NI DAQ devices"""
    _check_nidaqmx()
    s=nidaqmx.system.System()
    return [get_device_info(d.name) for d in s.devices]

class NIDAQ(interface.IDevice):
    """
    National Instruments DAQ device interface (wrapper around nidaqmx library).

    Simplified interface to NI DAQ devices.
    Supports voltage, digital, and counter inputs (all synchronized to the same clock), and digital and voltage outputs (asynchronous).

    Args:
        dev_name(str): root device name.
        rate(float): analog input sampling rate (can be adjusted later).
        buffer_size(int): size of the input buffer.
        reset(int): if ``True``, reset the device upon connection.
    """
    Error=NIError
    ReraiseError=NIDAQmxError
    BackendError=DaqError
    def __init__(self, dev_name="dev0", rate=1E2, buffer_size=1E5, reset=False):
        _check_nidaqmx()
        super().__init__()
        self.dev_name=dev_name.strip("/")
        self.dev=nidaqmx.system.Device(self.dev_name)
        if reset:
            self.dev.reset_device()
        self.rate=rate
        self.clk_src=None
        self.buffer_size=buffer_size
        self.ai_task=None
        self.ai_channels={}
        self.ci_tasks={}
        self.ci_counters={}
        self.di_channels={}
        self.do_channels={}
        self.ao_channels={}
        self.ao_values={}
        self.ao_array=None
        self.ao_array_single=None
        self.ao_autoloop=True
        self.co_tasks={}
        self._ao_written=0
        self.cpi_counter=0
        self.clk_channel_base=20E6
        self.max_ao_write_rate=1000 # maximal rate of repeating ao waveform with continuous repetition
        self.open()
        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("input_channels",lambda: self.get_input_channels(include=("ai","ci","di","cpi")))
        self._add_status_variable("voltage_input_parameters",self.get_voltage_input_parameters)
        self._add_status_variable("counter_input_parameters",self.get_counter_input_parameters)
        self._add_status_variable("digital_input_parameters",self.get_digital_input_parameters)
        self._add_status_variable("clock_period_input_parameters",self.get_clock_period_input_parameters)
        self._add_status_variable("digital_output_parameters",self.get_digital_output_parameters)
        self._add_status_variable("digital_output_values",self.get_digital_outputs)
        self._add_status_variable("voltage_output_parameters",self.get_voltage_output_parameters)
        self._add_status_variable("voltage_output_values",self.get_voltage_outputs)
        self._add_status_variable("pulse_output_parameters",self.get_pulse_output_parameters)
        self._add_settings_variable("clock_cfg",self.get_clock_parameters,self.setup_clock)
        self._add_settings_variable("clock_export",self.get_export_clock_terminal,self.export_clock)
        self._add_settings_variable("voltage_output_clock_cfg",self.get_voltage_output_clock_parameters,self.setup_voltage_output_clock)
        
    def _get_connection_parameters(self):
        return self.dev_name
    @reraise
    def open(self):
        if self.ai_task is not None:
            return
        self.ai_task=nidaqmx.Task()
        self.di_task=nidaqmx.Task()
        self.do_task=nidaqmx.Task()
        self.ao_task=nidaqmx.Task()
        self.cpi_task=nidaqmx.Task()
        self._update_channel_names()
        self._running=False
    @reraise
    def close(self):
        if self.ai_task is not None:
            self.ai_task.close()
        self.ai_task=None
        self.ai_channels={}
        for t in self.ci_tasks.values():
            t[0].close()
        self.ci_tasks={}
        if self.di_task is not None:
            self.di_task.close()
        self.di_task=None
        if self.do_task is not None:
            self.do_task.close()
        self.do_task=None
        self.do_channels={}
        if self.ao_task is not None:
            self.ao_task.close()
        self.ao_task=None
        self.ao_channels={}
        self.ao_values={}
        self.ao_array=None
        self.ao_array_single=None
        self.ao_autoloop=True
        self._ao_written=0
        for t in self.co_tasks.values():
            t[0].close()
        self.co_tasks={}
        if self.cpi_task is not None:
            self.cpi_task.close()
        self.cpi_task=None
        self._update_channel_names()
    def is_opened(self):
        return self.ai_task is not None
    @reraise
    def reset(self):
        """Reset the device. All channels will be removed"""
        self.close()
        self.dev.reset_device()
        self.open()
    def get_device_info(self):
        """
        Get device info.

        Return tuple ``(name, model, serial)``.
        """
        return get_device_info(self.dev_name)

    def _build_channel_name(self, channel):
        channel=channel.lower().strip("/")
        if channel.startswith("dev") or self.dev_name is None:
            return "/"+channel
        return "/"+self.dev_name+"/"+channel
    def _strip_channel_name(self, channel):
        channel=channel.lower().strip("/")
        if channel.startswith(self.dev_name.lower()):
            return channel[len(self.dev_name):].strip("/")
        return channel
    def _update_channel_names(self):
        self.ai_names=list(self.ai_channels.keys())
        self.ai_names.sort(key=lambda n: self.ai_channels[n][1])
        self.ci_names=list(self.ci_tasks.keys())
        self.ci_names.sort(key=lambda n: self.ci_tasks[n][1])
        self.di_names=list(self.di_channels.keys())
        self.di_names.sort(key=lambda n: self.di_channels[n][1])
        self.do_names=list(self.do_channels.keys())
        self.do_names.sort(key=lambda n: self.do_channels[n][1])
        self.ao_names=list(self.ao_channels.keys())
        self.ao_names.sort(key=lambda n: self.ao_channels[n][1])
        self.co_names=list(self.co_tasks.keys())
        self.co_names.sort(key=lambda n: self.co_tasks[n][1])

    @reraise
    def _cfg_clock(self, finite=None):
        sample_mode=nidaqmx.constants.AcquisitionType.FINITE if finite else nidaqmx.constants.AcquisitionType.CONTINUOUS
        samps_per_chan=finite if finite else int(self.buffer_size)
        samps_per_chan=max(samps_per_chan,2)
        if self.ai_task.ai_channels:
            self.ai_task.timing.cfg_samp_clk_timing(self.rate,source=self.clk_src or "",sample_mode=sample_mode,samps_per_chan=samps_per_chan)
        if self.di_task.di_channels:
            self.di_task.timing.cfg_samp_clk_timing(self.rate,source="ai/SampleClock",sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,samps_per_chan=int(self.buffer_size))
    def setup_clock(self, rate, src=None):
        """
        Setup analog input clock (which is the main system clock).

        If ``src==None``, use internal clock with the given rate; otherwise use `src` terminal as a clock source
        (in this case, `rate` should be higher than the expected source rate).
        """
        self.rate=rate
        self.clk_src=src
        self._cfg_clock()
    def get_clock_parameters(self):
        """
        Get analog input clock configuration.

        Return tuple ``(rate, src)``.
        """
        return self.rate,self.clk_src
    @reraise
    def export_clock(self, terminal):
        """
        Export system clock to the given terminal (``None`` to disconnect all terminals)
        
        Only terminal one can be active at a time.
         """
        terminal=self._strip_channel_name(terminal or "")
        self.ai_task.export_signals.export_signal(nidaqmx.constants.Signal.SAMPLE_CLOCK,terminal)
    @reraise
    def get_export_clock_terminal(self):
        """Return terminal which outputs system clock (``None`` if none is connected)"""
        if not self.ai_channels:
            return None
        term=self.ai_task.export_signals.samp_clk_output_term
        return self._strip_channel_name(term) if term else None

    if nidaqmx is not None:
        _voltage_input_terminal_cfgs={  "default":nidaqmx.constants.TerminalConfiguration.DEFAULT,
                                        "rse":nidaqmx.constants.TerminalConfiguration.RSE,
                                        "nrse":nidaqmx.constants.TerminalConfiguration.NRSE,
                                        "diff":general.getattr_multivar(nidaqmx.constants.TerminalConfiguration,["DIFFERENTIAL","BAL_DIFF","DIFF"],default=10106),
                                        "pseudodiff":general.getattr_multivar(nidaqmx.constants.TerminalConfiguration,["PSEUDODIFFERENTIAL","PSEUDO_DIFF"],default=12529)}
    else:
        _voltage_input_terminal_cfgs={}
    _p_voltage_input_terminal_cfg=interface.EnumParameterClass("voltage_input_terminal_cfg",_voltage_input_terminal_cfgs)
    @reraise
    @interface.use_parameters(terminal_cfg="voltage_input_terminal_cfg")
    def add_voltage_input(self, name, channel, rng=(-10,10), terminal_cfg="default"):
        """
        Add analog voltage input.

        Readout is synchronized to the system clock.

        Args:
            name(str): channel name to refer to it later.
            channel(str): terminal name (e.g., ``"ai0"``).
            rng: voltage range
            terminal_cfg: terminal configuration; can be ``"default"``,
                ``"rse"`` (single-ended, referenced to AI SENSE input), ``"nrse"`` (single-ended, referenced to AI GND),
                ``"diff"`` (differential), or ``"pseudodiff"`` (see NI DAQ manual for details).
        """
        channel=self._build_channel_name(channel)
        self.ai_task.ai_channels.add_ai_voltage_chan(channel,name,terminal_config=terminal_cfg,min_val=rng[0],max_val=rng[1])
        self._cfg_clock()
        self.ai_channels[name]=(channel,len(self.ai_task.ai_channels))
        self._update_channel_names()
    _p_counter_output_format=interface.EnumParameterClass("counter_output_format",["rate","diff","acc"])
    @reraise
    @interface.use_parameters(output_format="counter_output_format")
    def add_counter_input(self, name, counter, terminal, clk_src="ai/SampleClock", output_format="rate"):
        """
        Add counter input (value is related to the number of counts).

        Readout is synchronized to the system clock.
        
        Args:
            name(str): channel name.
            counter(str): on-board counter name (e.g., ``"ctr0"``).
            terminal(str): terminal name (e.g., ``"pfi0"``).
            clk_src(str): source of the counter sampling clock. By default it is the analog input clock,
                which requires at least one voltage input channel (could be a dummy channel) to be set up first.
            output_format(str): output format. Can be ``"acc"`` (return accumulated number of counts since the sampling start),
                ``"diff"`` (return number of counts passed between the two consecutive sampling points; essentially, a derivative of ``"acc"``),
                or ``"rate"`` (return count rate based on the ``"diff"`` samples).
        """
        if name in self.ci_tasks:
            self.ci_tasks[name][0].close()
        task=nidaqmx.Task()
        counter=self._build_channel_name(counter)
        terminal=self._build_channel_name(terminal)
        ch=task.ci_channels.add_ci_count_edges_chan(counter)
        ch.ci_count_edges_term=terminal
        task.timing.cfg_samp_clk_timing(self.rate,self._build_channel_name(clk_src),sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,samps_per_chan=int(self.buffer_size))
        self.ci_tasks[name]=(task,len(self.ci_tasks),output_format)
        self._update_channel_names()
    @reraise
    def add_clock_period_input(self, counter, clk_src="ai/SampleClock"):
        """
        Add clock period counter.

        Useful when using external sample clock with unknown period.
        The clock input can be returned during :meth:`read` operation, and it is used to calculate counter inputs in ``"rate"`` mode.
        Readout is synchronized to the system clock.
        
        Args:
            counter(str): on-board counter name (e.g., ``"ctr0"``) to be used for clock measure.
            clk_src(str): source of the counter sampling clock. By default it is the analog input clock,
                which requires at least one voltage input channel (could be dummy channel) to operate.
        """
        counter=self._build_channel_name(counter)
        if self.cpi_task.ci_channels:
            self.cpi_task.close()
            self.cpi_task=nidaqmx.Task()
        ch=self.cpi_task.ci_channels.add_ci_count_edges_chan(counter)
        ch.ci_count_edges_term="20MHzTimebase"
        self.cpi_task.timing.cfg_samp_clk_timing(self.rate,self._build_channel_name(clk_src),sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,samps_per_chan=int(self.buffer_size))
    @reraise
    def add_digital_input(self, name, channel):
        """
        Add digital input.

        Readout is synchronized to the system clock.
        Args:
            name(str): channel name.
            channel(str): terminal name (e.g., ``"port0/line12"``).
        """
        channel=self._build_channel_name(channel)
        self.di_task.di_channels.add_di_chan(channel,name)
        self._cfg_clock()
        self.di_channels[name]=(channel,len(self.di_task.di_channels))
        self._update_channel_names()
    def get_input_channels(self, include=("ai","ci","di")):
        """
        Get names of all input channels (voltage input and counter input).
        
        `include` specifies which channel types to include into the list
        (``"ai"`` for voltage inputs, ``"ci"`` for counter inputs, ``"di"`` for digital inputs, ``"cpi"`` for clock period channel).
        The channels order is always fixed: first voltage inputs, then counter inputs, then digital inputs.
        """
        return (self.ai_names if "ai" in include else [])+(self.ci_names if "ci" in include else [])+(self.di_names if "di" in include else [])+(["clk_period"] if "cpi" in include else [])
    def get_voltage_input_parameters(self):
        """Get parameters (names, channels, output ranges, and terminal configurations) of all analog voltage input channels"""
        params=[]
        for n in self.ai_names:
            ch=[ch for ch in self.ai_task.ai_channels if ch.name==n][0]
            term=self._strip_channel_name(ch.physical_channel.name)
            rng=(ch.ai_min,ch.ai_max)
            cfg=ch.ai_term_cfg.name.lower()
            params.append((n,term,rng,cfg))
        return params
    def get_counter_input_parameters(self):
        """Get parameters (names, counters, terminals, clock sources, and output formats) of all counter input channels"""
        params=[]
        for n in self.ci_names:
            task=self.ci_tasks[n][0]
            ch=task.ci_channels[0]
            counter=self._strip_channel_name(ch.physical_channel.name)
            term=self._strip_channel_name(ch.ci_count_edges_term)
            clk_src=self._strip_channel_name(task.timing.samp_clk_src)
            output_format=self.ci_tasks[n][2]
            params.append((n,counter,term,clk_src,output_format))
        return params
    def get_digital_input_parameters(self):
        """Get parameters (names and channels) of all digital input channels"""
        return [(n,self._strip_channel_name(self.di_channels[n][0])) for n in self.di_names]
    def get_clock_period_input_parameters(self):
        """Get parameters (counter input) of the clock period input channel"""
        return self._strip_channel_name(self.cpi_task.ci_channels[0].physical_channel.name) if self.cpi_task.ci_channels else None
    

    @reraise
    def start(self, flush_read=0, finite=None):
        """
        Start the sampling and output task.
        
        `flush_read` specifies number of samples to read and discard after start.
        If `finite` is not ``None``, it specifies finite number of sample to acquire before stopping.

        If counter channels are used, the first sample is usually unreliable, so ``flush_read=1`` is recommended;
        however, if exactly `finite` pulses are required at the clock export channel, ``flush_read=0`` is needed (the total number of pulses is ``flush_read+finite``).
        """
        for cit in self.ci_tasks:
            self.ci_tasks[cit][0].start()
            self.ci_counters[cit]=0
        if self.di_task.di_channels:
            self.di_task.start()
        if self.cpi_task.ci_channels:
            self.cpi_task.start()
            self.cpi_counter=0
        self._cfg_clock(finite=finite+flush_read if finite else None)
        self.ai_task.start()
        self._running=True
        if flush_read:
            self.read(flush_read)
    @reraise
    def stop(self):
        """Stop the sampling task"""
        self.ai_task.stop()
        self.di_task.stop()
        for cit in self.ci_tasks:
            self.ci_tasks[cit][0].stop()
            self.ci_counters[cit]=0
            self.cpi_counter=0
        self.cpi_task.stop()
        self._running=False
    def is_running(self):
        """Check if the task is running"""
        return self._running
    @reraise
    def available_samples(self):
        """Get number of available samples to read (return 0 if the task is not running)"""
        if not self._running:
            return 0
        return self.ai_task.in_stream.avail_samp_per_chan
    @reraise
    def get_buffer_size(self):
        """Get the sampling buffer size"""
        return self.ai_task.in_stream.input_buf_size if len(self.ai_task.ai_channels) else 0
    @reraise
    def wait_for_sample(self, num=1, timeout=10., wait_time=0.001):
        """
        Wait until at least `num` samples are available.
        
        If they are not available immediately, loop while checking every `wait_time` interval until enough samples are accumulated.
        Return the number of available samples if successful, or 0 if the execution timed out.
        """
        if not self._running:
            return 0
        if self.available_samples()>=num:
            return self.available_samples()
        ctd=general.Countdown(timeout)
        while not ctd.passed():
            time.sleep(wait_time)
            if self.available_samples()>=num:
                return self.available_samples()
        return 0
    @reraise
    def read(self, n=1, flush_read=0, timeout=10., include=("ai","ci","di")):
        """
        Read `n` samples. If the task is not running, automatically start before reading and stop after.

        Args:
            n(int): number of samples to read. If ``n<=0``, read all available samples.
            flush_read(int): number of initial samples to skip if the task is currently stopped and needs to be started.
                If counter channels are used, the first sample is usually unreliable, so ``flush_read=1`` is recommended;
                however, if exactly `n` pulses are required at the clock export channel, ``flush_read=0`` is needed.
            include(tuple): specifies which channel types to include into the list
                (``"ai"`` for voltage inputs, ``"ci"`` for counter inputs, ``"di"`` for digital inputs, ``"cpi"`` for clock period channel).
        
        Returns:
            2D numpy array of values arranged according to :meth:`get_input_channels` order with the given `include` parameter.
        """
        running=True
        if not self._running:
            running=False
            self.start(flush_read=flush_read,finite=n)
        try:
            if n is None or n<=0:
                n=self.available_samples()
            else:
                n=int(n)
            ais=self.ai_task.read(n,timeout=timeout)
            if len(self.ai_task.ai_channels)==1:
                ais=[ais]
            cis=[np.array(self.ci_tasks[ci][0].read(n),dtype="u4") for ci in self.ci_names]
            if self.cpi_task.ci_channels:
                clk_counts=np.array(self.cpi_task.read(n),dtype="u4")
                last_cnt=clk_counts[-1]
                clk_counts[1:]-=clk_counts[:-1]
                clk_counts[0]=(int(clk_counts[0])-self.cpi_counter)%int(2**32)
                self.cpi_counter=int(last_cnt)
                clk_periods=clk_counts/self.clk_channel_base
            else:
                clk_periods=np.repeat(1./self.rate,n) if ("cpi" in include) else 1./self.rate
            if "ci" in include:
                for i,ci in enumerate(self.ci_names):
                    if self.ci_tasks[ci][2]!="acc":
                        last_cnt=cis[i][-1]
                        cis[i][1:]-=cis[i][:-1]
                        cis[i][0]=(int(cis[i][0])-self.ci_counters[ci])%int(2**32)
                        self.ci_counters[ci]=int(last_cnt)
                        if self.ci_tasks[ci][2]=="rate":
                            cis[i]=cis[i]/clk_periods
            if self.di_task.di_channels:
                dis=self.di_task.read(n)
                if len(self.di_task.di_channels)==1:
                    dis=[dis]
            else:
                dis=[]
            return np.column_stack((ais if "ai" in include else [])+(cis if "ci" in include else [])+(dis if "di" in include else [])+([clk_periods] if "cpi" in include else []))
        finally:
            if not running:
                self.stop()

    @reraise
    def add_digital_output(self, name, channel):
        """
        Add digital output.

        Args:
            name(str): channel name.
            channel(str): terminal name (e.g., ``"do0"``).
        """
        channel=self._build_channel_name(channel)
        self.do_task.do_channels.add_do_chan(channel,name)
        self.do_channels[name]=(channel,len(self.do_task.do_channels))
        self._update_channel_names()
    def get_digital_output_channels(self):
        """Get names of all digital output channels"""
        return self.do_names
    def get_digital_output_parameters(self):
        """Get parameters (names and channels) of all digital output channels"""
        return [(n,self._strip_channel_name(self.do_channels[n][0])) for n in self.do_names]
    @reraise
    def set_digital_outputs(self, names, values):
        """
        Set values of one or several digital outputs.

        Args:
            names(str or [str]): name or list of names of outputs.
            values: output value or list of values.
        """
        names=funcargparse.as_sequence(names,allowed_type="array")
        values=funcargparse.as_sequence(values,allowed_type="array")
        values_dict=dict(zip(names,values))
        ch_names=set([ch.name for ch in self.do_task.do_channels])
        for n in names:
            if n not in ch_names:
                raise ValueError("channel '{}' doesn't exist".format(n))
        curr_vals=self.do_task.read()
        if len(self.do_task.do_channels)==1:
            curr_vals=[curr_vals]
        for i,ch in enumerate(self.do_task.do_channels):
            if ch.name in values_dict:
                curr_vals[i]=bool(values_dict[ch.name])
        self.do_task.write(curr_vals)
    @reraise
    def get_digital_outputs(self, names=None):
        """
        Get values of one or several digital outputs.

        Args:
            names(str or [str] or None): name or list of names of outputs (``None`` means all outputs).

        Return list of values ordered by `names` (or by :meth:`get_digital_output_channels` if ``names==None``).
        """
        if not self.do_names:
            return []
        if names is None:
            names=self.do_names
        else:
            names=funcargparse.as_sequence(names,allowed_type="array")
        values_dict=dict(zip(names,[None]*len(names)))
        curr_vals=self.do_task.read()
        if len(self.do_task.do_channels)==1:
            curr_vals=[curr_vals]
        for i,ch in enumerate(self.do_task.do_channels):
            if ch.name in values_dict:
                values_dict[ch.name]=curr_vals[i]
        return [values_dict[n] for n in names]

    @reraise
    def add_voltage_output(self, name, channel, rng=(-10,10), initial_value=0.):
        """
        Add analog voltage output.

        Args:
            name(str): channel name.
            channel(str): terminal name (e.g., ``"ao0"``).
            rng: voltage range.
            initial_value(float): initial output value (has to be initialized).
        """
        channel=self._build_channel_name(channel)
        self.ao_task.ao_channels.add_ao_voltage_chan(channel,name,min_val=rng[0],max_val=rng[1])
        self.ao_channels[name]=(channel,len(self.ao_task.ao_channels),rng)
        self.ao_values[name]=initial_value
        self._update_channel_names()
        self.set_voltage_outputs([],[])
    def get_voltage_output_channels(self):
        """Get names of all analog voltage output channels"""
        return self.ao_names
    def get_voltage_output_parameters(self):
        """Get parameters (names, channels and output ranges) of all analog voltage output channels"""
        params=[]
        for n in self.ao_names:
            ch=[ch for ch in self.ao_task.ao_channels if ch.name==n][0]
            term=self._strip_channel_name(ch.physical_channel.name)
            rng=(ch.ao_min,ch.ao_max)
            params.append((n,term,rng))
        return params
    def _update_voltage_output_values(self, names, values, single_shot=0):
        if not funcargparse.is_sequence(names,"array"):
            names=[names]
            values=[values]
        for n in names:
            if n not in self.ao_values:
                raise ValueError("channel '{}' doesn't exist".format(n))
        for n,v in zip(names,values):
            self.ao_values[n]=v
        val=[self.ao_values[ch.name] for ch in self.ao_task.ao_channels]
        ls=[len(v) for v in val if np.ndim(v)==1]
        if not np.all([l==ls[0] for l in ls]):
            raise ValueError("output channels have different lengths: {}".format(dict(zip(self.ao_task.ao_channels,ls))))
        if not np.all([np.ndim(v)==np.ndim(val[0]) for v in val]):
            val=[(v if np.ndim(v)==1 else [v]*ls[0]) for v in val]
        val=np.array(val)
        self.ao_array=val[...,single_shot:]
        self.ao_array_single=val[...,:single_shot] if single_shot else None
    def _write_voltage_output_values(self, minsamp=0, force_restart=True):
        val=self.ao_array
        sval=self.ao_array_single
        self.ao_array_single=None
        if val is None:
            return
        if sval is None:
            svshape=(val.shape[0],0) if val.ndim==2 else (0,)
            sval=np.zeros(svshape,dtype=val.dtype)
        waveform_output=self.ao_task.timing.samp_timing_type!=nidaqmx.constants.SampleTimingType.ON_DEMAND
        if waveform_output:
            min_out_len=max(2,int(self.ao_task.timing.samp_clk_rate//self.max_ao_write_rate)+1,minsamp)
            if val.ndim==1:
                val=np.column_stack([val]*min_out_len)
            elif sval.shape[1]+val.shape[1]<min_out_len:
                nreps=(min_out_len-sval.shape[1])//val.shape[1]+1
                val=np.concatenate([sval]+[val]*nreps,axis=1)
            elif sval.shape[-1]:
                val=np.concatenate([sval,val],axis=1)
            if self.ao_task.timing.samp_quant_samp_mode==nidaqmx.constants.AcquisitionType.FINITE:
                max_out_len=self.ao_task.timing.samp_quant_samp_per_chan
                val=val[:,:max_out_len]
            nval=val.shape[1]
        elif val.ndim==2:
            val=val[:,0]
        val=np.require(val,requirements=["C","W"])
        val=val[0] if len(val)==1 else val
        if waveform_output and (force_restart or self.ao_autoloop):
            self.ao_task.stop()
            self.ao_task.write(val,auto_start=True)
            self._ao_written=nval
        else:
            self.ao_task.write(val)
            if waveform_output:
                self._ao_written+=nval
    @reraise
    def set_voltage_outputs(self, names, values, minsamp=1, force_restart=True, single_shot=0):
        """
        Set values of one or several analog voltage outputs.

        Args:
            names(str or [str]): name or list of names of outputs.
            values: output value or list values.
                These can be single numbers, or arrays if the output clock is setup (see :meth:`setup_voltage_output_clock`).
                In the latter case it sets up the output waveforms; note that waveforms for all channels must have the same length
                (a single number signifying a constant output is also allowed)
                If the analog output is set up to the finite mode (``continuous==False``), the finite waveform output happens right away,
                with the number of samples determined by `samps_per_channel` parameter of :meth:`setup_voltage_output_clock`.
                In this case, if the supplied waveform is shorter than the number of samples, it gets repeated; if it's longer, it gets cut off.
            minsamp: in non-autoloop mode, specifies the minimal number of samples to write to the output buffer; if the length of `values` is
                less than this number, than the waveform is repeated by a required integer number of times to produce at least `minsamp` samples
            force_restart: if ``True``, restart the output after writing to immediately start outputting the new waveforms;
                otherwise, add it to the end of the buffer; only applies in non-autoloop mode (autoloop mode always restarts)
            single_shot: specifies some number of samples from the start as "single-shot", so whenever the waveform is repeated
                (either to reach `minsamp` samples, or when :meth:`fill_voltage_output_buffer` is called), this part is ignored, and only the rest is repeated
        """
        self._update_voltage_output_values(names,values,single_shot=single_shot)
        if self.ao_autoloop or force_restart:
            self._write_voltage_output_values(minsamp=minsamp or 0,force_restart=force_restart)
        else:
            self.fill_voltage_output_buffer(minsamp=minsamp)
    def get_voltage_output_buffer_fill(self):
        """
        Get the number of samples still in the output buffer.

        Only applies to non-autoloop mode, and return ``None`` otherwise.
        """
        try:
            if not self.ao_autoloop:
                ngen=self.ao_task.out_stream.total_samp_per_chan_generated
                return self._ao_written-ngen
        except self.BackendError:
            pass
    @reraise
    def fill_voltage_output_buffer(self, minsamp=1):
        """
        Add samples to the output buffer until there are at least `minsamp` samples there.

        Only applies to non-autoloop mode, and does nothing otherwise. The added samples are determined based
        on the last data written by :meth:`set_voltage_outputs` and the ``single_shot`` argument specified there.
        """
        curr_fill=self.get_voltage_output_buffer_fill()
        if curr_fill is not None and minsamp is not None and curr_fill<minsamp:
            self._write_voltage_output_values(minsamp-curr_fill,force_restart=False)


    def get_voltage_outputs(self, names=None):
        """
        Get values of one or several analog voltage outputs.

        Args:
            names(str or [str] or None): name or list of names of outputs (``None`` means all outputs).

        Return list of values ordered by `names` (or by :meth:`get_voltage_output_channels` if ``names==None``).
        For continuous waveforms, return the array containing a single repetition of the waveform.
        For finite waveforms, repeat the array containing the last outputted waveform.
        """
        if names is None:
            names=self.ao_names
        else:
            names=funcargparse.as_sequence(names,allowed_type="array")
        return [self.ao_values[n] for n in names]
    @reraise
    def setup_voltage_output_clock(self, rate=0, sync_with_ai=False, continuous=True, samps_per_chan=1000, autoloop=True, minsamp=1):
        """
        Setup analog output clock configuration.

        Args:
            rate: clock rate; if 0, assume constant voltage output (default)
            sync_with_ai: if ``True``, the clock is synchronized to the analog input clock (the main clock);
                note that in this case output changes only when the analog read task is running
            continuous: if ``True``, any written waveform gets repeated continuously; otherwise, it outputs written waveform only once,
                and then latches the output on the last value
            samps_per_chan: if ``continuous==False``, it determines number of samples to output before stopping;
                otherwise, it determines the size of the output buffer
            autoloop: if it is ``True``, then the specified output waveforms are automatically repeated to create a periodic output signal
                (referred to as "regeneration mode" in NI DAQ terminology); otherwise, written output data is "exhausted" once sent to the output,
                so the application needs to continuously write output waveforms to avoid output buffer from running empty (which causes an error).
                This mode gives better control over the output and allows to seamlessly adjust it in real time, but it is more demanding on the application.
            minsamp: if the waveform has been specified before, this argument sets the minimal number of samples to write to the output buffer
                after the clock is set up and the output is restarted
        """
        if not len(self.ao_task.ao_channels):
            return
        self.ao_task.stop()
        sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS if continuous else nidaqmx.constants.AcquisitionType.FINITE
        if rate==0 and not sync_with_ai:
            self.ao_task.timing.samp_timing_type=nidaqmx.constants.SampleTimingType.ON_DEMAND
        elif sync_with_ai:
            self.ao_task.timing.cfg_samp_clk_timing(self.rate,source="ai/SampleClock",samps_per_chan=int(samps_per_chan),sample_mode=sample_mode)
        else:
            self.ao_task.timing.cfg_samp_clk_timing(rate,source="",samps_per_chan=int(samps_per_chan),sample_mode=sample_mode)
        self.ao_autoloop=True
        self.ao_task.out_stream.regen_mode=nidaqmx.constants.RegenerationMode.ALLOW_REGENERATION
        if self.ao_task.timing.samp_timing_type!=nidaqmx.constants.SampleTimingType.ON_DEMAND:
            if continuous:
                if not autoloop:
                    self.ao_autoloop=False
                    self.ao_task.out_stream.regen_mode=nidaqmx.constants.RegenerationMode.DONT_ALLOW_REGENERATION
                self.set_voltage_outputs(self.ao_names,[self.ao_values[n] for n in self.ao_names],minsamp=minsamp)
    @reraise
    def get_voltage_output_clock_parameters(self):
        """
        Get analog output clock configuration.

        Return tuple ``(rate, sync_with_ai, continuous, samps_per_chan, autoloop)``.
        """
        if (not self.ao_channels) or self.ao_task.timing.samp_timing_type==nidaqmx.constants.SampleTimingType.ON_DEMAND:
            return TVoltageOutputClockParameters(0,False,1000,True,True)
        sync_with_ai=self.ao_task.timing.samp_clk_src.endswith("ai/SampleClock")
        rate=self.ao_task.timing.samp_clk_rate
        samps_per_chan=self.ao_task.timing.samp_quant_samp_per_chan
        continuous=self.ao_task.timing.samp_quant_samp_mode!=nidaqmx.constants.AcquisitionType.FINITE
        return TVoltageOutputClockParameters(rate,sync_with_ai,continuous,samps_per_chan,self.ao_autoloop)
    

    def _find_co_timebase(self):
        tbterms=[t for t in self.dev.terminals if t.lower().endswith("Timebase")]
        maxtb=self.dev.co_max_timebase
        for t in tbterms:
            m=re.match(r"(\d+)(khz|mhz)timebase",t,flags=re.IGNORECASE)
            if m:
                tr=float(m[1])*(1E3 if m[2].lower()=="khz" else 1E6)
                if abs(tr/t-1)<1E-3:
                    return t
        raise NIDAQmxError("could not find the maximal rate timebase with rate {} Hz among terminals {}".format(maxtb,tbterms))
    def _disconnect_co_channel(self, ch):
        term,ch.co_pulse_term=ch.co_pulse_term,None
        nidaqmx.system.System().tristate_output_term(term)
    _p_counter_output_kind=interface.EnumParameterClass("counter_output_kind",["time","ticks"])
    @reraise
    @interface.use_parameters(kind="counter_output_kind")
    def add_pulse_output(self, name, counter, terminal, kind="time", on=1E-3, off=1E-3, clk_src=None, continuous=True, samps=1000):
        """
        Add counter pulse input.
        
        Args:
            name(str): channel name.
            counter(str): on-board counter name (e.g., ``"ctr0"``).
            terminal(str): output terminal name (e.g., ``"pfi0"``).
            kind(str): pulse output kind; can be either ``"time"`` (use internal timebase; specify the pulse on and off times in seconds)
                or ``"ticks"`` (use internal or external timebase; specify the pulse on and off times in number of ticks of the clock)
            on: on time or number of ticks for the pulse
            off: off time or number of ticks for the pulse
            clk_src(str): source of the counter sampling clock. By default it is the device timebase (usually 100MHz);
                can be a name of an external terminal (e.g., ``"pfi1"``), or ``"ai"`` to use the analog input sampling clock
            continuous(bool): if ``True``, the pulses are generated as long as the output is running;
                otherwise, output the number of samples specified in `samps` and then stop
            samps: number of samples to output if ``continuous==False``
        """
        if name in self.co_tasks:
            self._disconnect_co_channel(self.co_tasks[name][0].co_channels[0])
            self.co_tasks[name][0].close()
        task=nidaqmx.Task()
        counter=self._build_channel_name(counter)
        terminal=self._build_channel_name(terminal)
        if kind=="time":
            ch=task.co_channels.add_co_pulse_chan_time(counter,low_time=off,high_time=on)
        else:
            if clk_src is None:
                clk=self._find_co_timebase()
            elif clk_src=="ai":
                clk="ai/SampleClock"
            else:
                clk=clk_src
            ch=task.co_channels.add_co_pulse_chan_ticks(counter,source_terminal=clk,low_ticks=off,high_ticks=on)
        ch.co_pulse_term=terminal
        sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS if continuous else nidaqmx.constants.AcquisitionType.FINITE
        task.timing.cfg_implicit_timing(sample_mode,samps_per_chan=samps)
        self.co_tasks[name]=(task,kind,clk_src)
        self._update_channel_names()
    def get_pulse_output_channels(self):
        """Get names of all pulse output channels"""
        return self.co_names
    def _get_co_parameters(self, name):
        task,kind,clk_src=self.co_tasks[name]
        ch=task.co_channels[0]
        counter=self._strip_channel_name(ch.physical_channel.name)
        term=self._strip_channel_name(ch.co_pulse_term)
        if kind=="time":
            on,off=ch.co_pulse_high_time,ch.co_pulse_low_time
        else:
            on,off=ch.co_pulse_high_ticks,ch.co_pulse_low_ticks
        cont=task.timing.samp_quant_samp_mode==nidaqmx.constants.AcquisitionType.CONTINUOUS
        samps=task.timing.samp_quant_samp_per_chan
        return counter,term,kind,on,off,clk_src,cont,samps
    def get_pulse_output_parameters(self):
        """Get parameters (names, counters, terminals, kinds, on times, off times, clock sources, continuous, number of samples) of all pulse output channels"""
        params=[]
        for n in self.co_names:
            par=self._get_co_parameters(n)
            params.append((n,)+par)
        return params
    def set_pulse_output(self, name, on=None, off=None, continuous=None, samps=None, terminal=None, restart=True):
        """
        Change pulse output parameters.
        
        Parameter meanings are the same as in :meth:`add_pulse_output`. Parameters with values if ``None`` are left unchanged.
        If any parameters are not ``None``, the output pulse task is stopped before parameter changing.
        If the task is currently running and ``restart==True``, restart the task after changing the parameters.
        """
        if not any(v is not None for v in [on,off,continuous,samps,terminal]):
            return
        task,kind=self.co_tasks[name][:2]
        ch=task.co_channels[0]
        running=not task.is_task_done()
        task.stop()
        if kind=="time":
            if on is not None:
                ch.co_pulse_high_time=on
            if off is not None:
                ch.co_pulse_low_time=off
        else:
            if on is not None:
                ch.co_pulse_high_ticks=on
            if off is not None:
                ch.co_pulse_low_ticks=off
        if continuous is not None:
            task.timing.samp_quant_samp_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS if continuous else nidaqmx.constants.AcquisitionType.FINITE
        if samps is not None:
            task.timing.samp_quant_samp_per_chan=samps
        if terminal is not None:
            self._disconnect_co_channel(ch)
            terminal=self._build_channel_name(terminal)
            ch.co_pulse_term=terminal
        if running and restart:
            task.start()
    def start_pulse_output(self, names=None, autostop=True):
        """Start specified pulse output or a set of outputs (by default, all of them)"""
        if names is None:
            names=self.co_names
        elif not funcargparse.is_sequence(names,"array"):
            names=[names]
        if autostop:
            for n in names:
                self.co_tasks[n][0].stop()
        for n in names:
            self.co_tasks[n][0].start()
    def stop_pulse_output(self, names=None):
        """Stop specified pulse output or a set of outputs (by default, all of them)"""
        if names is None:
            names=self.co_names
        elif not funcargparse.is_sequence(names,"array"):
            names=[names]
        for n in names:
            self.co_tasks[n][0].stop()
    def is_pulse_output_running(self, names=None):
        """Check if pulse outputs with the given name or set of names are running"""
        if names is None:
            names=self.co_names
        if funcargparse.is_sequence(names,"array"):
            return {n:not self.co_tasks[n][0].is_task_done() for n in names}
        return not self.co_tasks[names][0].is_task_done()