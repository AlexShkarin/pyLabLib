import numpy as np

from ...core.devio import SCPI, interface

from .base import AgilentError,AgilentBackendError

class AgilentE5071C(SCPI.SCPIDevice):
    """
    Agilent E5071C vector network analyzer.
    
    Args:
        addr: device address; usually a VISA address string such as ``"USB0::0x0957::0x0D09::MY00000000::0::INSTR"``
    """
    _default_backend_timeout=10.
    Error=AgilentError
    ReraiseError=AgilentBackendError

    _sens_channel_rng=(1,36)
    _source_channel_rng=(1,160)
    def __init__(self, addr):
        super().__init__(addr)
        self._sens_channel=self._sens_channel_rng[0]
        self._source_channel=self._source_channel_rng[0]
        self._add_settings_variable("sens_channel",self.get_sens_channel,self.set_sens_channel)
        self._add_settings_variable("source_channel",self.get_source_channel,self.set_source_channel)
        self._add_settings_variable("enabled",self.is_output_enabled,self.enable_output)
        self._add_settings_variable("output_level",self.get_output_level,self.set_output_level)
        self._add_settings_variable("bandwidth",self.get_bandwidth,self.set_bandwidth)
        self._add_settings_variable("averaging",self.get_averaging_parameters,self.setup_averaging)
        self._add_settings_variable("frequency_range",self.get_frequency_range,self.set_frequency_range)
        self._add_settings_variable("trace_format",self.get_trace_format,self.set_trace_format)

    def _check_channel(self, channel, rng, default):
        if channel is None:
            return default
        if channel<rng[0] or channel>rng[1]:
            raise ValueError("channel value {} if out of range [{}, {}]".format(channel,*rng))
        return channel
    def _make_sens_comm(self, comm, channel):
        channel=self._check_channel(channel,self._sens_channel_rng,self._sens_channel)
        return ":SENS{}:{}".format(channel,comm)
    def _write_sens(self, comm, arg=None, arg_type=None, channel=None):
        return self.write(self._make_sens_comm(comm,channel),arg=arg,arg_type=arg_type)
    def _query_sens(self, comm, data_type="string", channel=None):
        return self.ask(self._make_sens_comm(comm,channel),data_type=data_type)
    def get_sens_channel(self):
        """Return the current default sens channel"""
        return self._sens_channel
    def set_sens_channel(self, channel=1):
        """Set the default sens channel"""
        self._sens_channel=self._check_channel(channel,self._sens_channel_rng,self._sens_channel)

    def _make_source_comm(self, comm, channel):
        channel=self._check_channel(channel,self._source_channel_rng,self._source_channel)
        return ":SOURCE{}:{}".format(channel,comm)
    def _write_source(self, comm, arg=None, arg_type=None, channel=None):
        return self.write(self._make_source_comm(comm,channel),arg=arg,arg_type=arg_type)
    def _query_source(self, comm, data_type="string", channel=None):
        return self.ask(self._make_source_comm(comm,channel),data_type=data_type)
    def get_source_channel(self):
        """Return the current default source channel"""
        return self._source_channel
    def set_source_channel(self, channel=1):
        """Set the default source channel"""
        self._source_channel=self._check_channel(channel,self._source_channel_rng,self._source_channel)

    def is_output_enabled(self):
        """Check if the output is enabled"""
        return self.ask(":OUTP:STATE?","bool")
    def enable_output(self, enable=True):
        """Enable or disable the output"""
        self.write(":OUTP:STATE",bool(enable))
        return self.is_output_enabled()
    def get_output_level(self, channel=None):
        """Get the power level the the given source channel (in dB)"""
        return self._query_source("POWER?","float",channel=channel)
    def set_output_level(self, level, channel=None):
        """Set the power level the the given source channel (in dB)"""
        self._write_source("POWER",level,channel=channel)
        return self.get_output_level(channel=channel)

    def get_bandwidth(self, channel=None):
        """Get the IF bandwidth at the given channel"""
        return self._query_sens("BWID?","float",channel=channel)
    def set_bandwidth(self, bandwidth, channel=None):
        """Set the IF bandwidth at the given channel"""
        self._write_sens("BWID",float(bandwidth),channel=channel)
        return self.get_bandwidth(channel=channel)

    def get_averaging_parameters(self, channel=None):
        """Get the averaging parameters ``(enabled, number)``"""
        return self._query_sens("AVER:STATE?","bool",channel=channel),self._query_sens("AVER:COUNT?","int",channel=channel)
    def setup_averaging(self, enabled=None, number=None, channel=None):
        """Set up whether the averaging is enabled and the number of traces to average"""
        if enabled is not None:
            self._write_sens("AVER:STATE",bool(enabled),channel=channel)
        if number is not None:
            self._write_sens("AVER:COUNT",int(number),channel=channel)
        return self.get_averaging_parameters(channel=channel)
    def reset_averaging(self, channel=None):
        """Reset averaging at the given channel"""
        self._write_sens("AVER:CLEAR",channel=channel)
    
    def get_frequency_range(self, channel=None):
        """Get current sweep frequency range"""
        return tuple(self._query_sens("FREQ:{}?".format(c),"float",channel=channel) for c in ["START","STOP"])
    def set_frequency_range(self, rng, channel=None):
        """Set the current frequency range"""
        crng=self.get_frequency_range(channel)
        order=[("START",rng[0]),("STOP",rng[1])]
        if rng[0]>crng[1]:
            order=order[::-1]
        for c,v in order:
            self._write_sens("FREQ:{}".format(c),float(v))
        return self.get_frequency_range(channel=channel)
    
    _p_data_format=interface.EnumParameterClass("data_format",{"ascii":"ASC","float64":"REAL","float32":"REAL32"})
    _p_data_border=interface.EnumParameterClass("data_border",{"normal":"NORM","swapped":"SWAP"})
    @interface.use_parameters(_returns=("data_format","data_border"))
    def get_trace_format(self):
        """Return trace data format as a tuple ``(data_format, data_border)``"""
        return self.ask(":FORM:DATA?"),self.ask(":FORM:BORDER?")
    @interface.use_parameters()
    def set_trace_format(self, data_format=None, data_border=None):
        """
        Set trace data format and byte order.
        
        `data_format` can be ``"ascii"``, ``"float64"``, or ``"float32"``, and `data_border` can be ``"normal"`` or ``"swapped"``
        """
        if data_format is not None:
            self.write(":FORM:DATA",data_format)
        if data_border is not None:
            self.write(":FORM:BORDER",data_border)
        return self.get_trace_format()
    def _read_trace(self, fmt):
        if fmt[0]=="ascii":
            data=self.read()
            return np.array([float(v) for v in data.split(",")])
        data=self.read_binary_array_data()
        dtype="{}f{}".format(("<" if fmt[1]=="swapped" else ">"),(8 if fmt[0]=="float64" else 4))
        return np.frombuffer(data,dtype=dtype)
    def _query_trace(self, comm, fmt=None):
        if fmt is None:
            fmt=self.get_trace_format()
        self.write(comm)
        return self._read_trace(fmt)
    def read_frequency_trace(self, fmt=None, channel=None):
        """Get the frequency trace for the given channel"""
        return self._query_trace(self._make_sens_comm("FREQ:DATA?",channel=channel),fmt=fmt)
    def read_S_parameters(self, param=("S11","S12","S21","S22"), add_frequency=False, fmt=None, channel=None):
        """
        Get the S parameters trace for the given channel.
        
        `param` can be either a single string specifying the parameters (e.g., ``"S12"``), or a tuple or list of strings.
        `add_frequency` specifies whether the frequency axis should be added to the result.
        If ``raw==True``, return the raw (un-corrected) parameters; otherwise, return corrected parameters.

        If ``add_frequency==False``, return a single 1D complex array for the single channel, or a multi-column complex array for several channels.
        If ``add_frequency==True``, return a multi-column array, where the first column is the frequency, and the rest are the parameters.
        """
        if isinstance(param,(tuple,list)):
            sparam=", ".join(param)
            data=self._query_trace(self._make_sens_comm('CORR:DATA:CDATA? "{}"'.format(sparam),channel),fmt=fmt)
            param=(data[::2]+1j*data[1::2]).reshape((len(param),-1)).transpose()
        else:
            data=self._query_trace(self._make_sens_comm("DATA:CORR? {}".format(param),channel),fmt=fmt)
            param=data[::2]+1j*data[1::2]
        if add_frequency:
            freqs=self.read_frequency_trace(fmt=fmt,channel=channel)
            return np.column_stack([freqs,param])
        return param