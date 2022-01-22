from ...core.devio import SCPI, interface, comm_backend
from ...core.utils import units

import numpy as np

class GenericAWGError(comm_backend.DeviceError):
    """Generic AWG error"""
class GenericAWGBackendError(GenericAWGError,comm_backend.DeviceBackendError):
    """AWG backend communication error"""

class GenericAWG(SCPI.SCPIDevice):
    """
    Generic arbitrary wave generator, based on Agilent 33500.

    With slight modifications works for many other AWGs using largely the same syntax.
    """
    _exclude_commands=set()
    _single_channel_commands=set()
    _all_channel_commands=set()
    _set_angle_unit=True
    _default_angle_unit="deg"
    _force_channel_source_pfx=False
    _default_operation_cooldown={"write":1E-2}
    _channels_number=1
    _default_load=50
    _inf_load=1E6
    _range_mode="high_low"  # range setting mode; can be "high_low", "amp_off", or "both" (set both, return "amp_off")
    _function_aliases={"sine":"SIN","square":"SQU","ramp":"RAMP","pulse":"PULS","noise":"NOIS","prbs":"PRBS","dc":"DC","user":"USER","arb":"ARB"}
    _supported_functions=list(_function_aliases)
    Error=GenericAWGError
    ReraiseError=GenericAWGBackendError
    _bool_selector=("OFF","ON")
    def __init__(self, addr):
        super().__init__(addr)
        self._channels_number=self._detect_channels_number()
        self._add_info_variable("channels_number",self.get_channels_number)
        functions={k:v for (k,v) in self._function_aliases.items() if k in self._supported_functions}
        if "*" in self._supported_functions:
            self._add_parameter_class(interface.EnumParameterClass("function",functions,allowed_alias="all",allowed_value="all",match_prefix=True))
        else:
            self._add_parameter_class(interface.EnumParameterClass("function",functions,match_prefix=True))
        for ch in range(1,self._channels_number+1):
            self._add_scpi_parameter("output_on","",kind="bool",channel=ch,comm_kind="output",add_variable=True)
            self._add_scpi_parameter("output_polarity","POLARITY",kind="param",parameter="polarity",channel=ch,comm_kind="output",add_variable=True)
            self._add_scpi_parameter("output_sync","SYNC",kind="bool",channel=ch,comm_kind="output",add_variable=True)
            self._add_scpi_parameter("output_load","LOAD",kind="string",channel=ch,comm_kind="output",add_variable=False)
            self._add_settings_variable("output_load",self.get_load,self.set_load,channel=ch)
            self._add_settings_variable("output_range",self.get_output_range,self.set_output_range,multiarg=False,channel=ch)
            self._add_scpi_parameter("amplitude","VOLTAGE",kind="float",channel=ch)
            self._add_scpi_parameter("offset","VOLTAGE:OFFSET",kind="float",channel=ch)
            self._add_settings_variable("frequency",self.get_frequency,self.set_frequency,channel=ch)
            self._add_settings_variable("phase",self.get_phase,self.set_phase,channel=ch)
            self._add_scpi_parameter("phase","PHASE",kind="float",channel=ch)
            self._add_scpi_parameter("function","FUNCTION",kind="param",parameter="function",channel=ch,add_variable=True)
            self._add_scpi_parameter("duty_cycle","FUNCTION:SQUARE:DCYCLE",channel=ch,add_variable=True)
            self._add_scpi_parameter("ramp_symmetry","FUNCTION:RAMP:SYMMETRY",channel=ch,add_variable=True)
            self._add_scpi_parameter("pulse_width","FUNCTION:PULSE:WIDTH",channel=ch,add_variable=True)
            self._add_scpi_parameter("burst_enabled","BURST:STATE",kind="bool",channel=ch,add_variable=True)
            self._add_scpi_parameter("burst_mode","BURST:MODE",kind="param",parameter="burst_mode",channel=ch,add_variable=True)
            self._add_settings_variable("burst_ncycles",self.get_burst_ncycles,self.set_burst_ncycles,channel=ch)
            self._add_scpi_parameter("gate_polarity","BURST:GATE:POL",kind="param",parameter="polarity",channel=ch,set_delay=0.1,add_variable=True)
            self._add_scpi_parameter("trigger_source","TRIG:SOURCE",kind="param",parameter="trigger_source",channel=ch,add_variable=True)
            self._add_scpi_parameter("trigger_slope","TRIG:SLOPE",kind="param",parameter="slope",channel=ch,add_variable=True)
            self._add_scpi_parameter("trigger_output","OUTPUT:TRIG",kind="bool",channel=ch,add_variable=True)
            self._add_scpi_parameter("output_trigger_slope","OUTPUT:TRIG:SLOPE",kind="param",parameter="slope",channel=ch,add_variable=True)
        self._add_scpi_parameter("voltage_unit","VOLTAGE:UNIT",kind="string")
        self._add_scpi_parameter("phase_unit","UNIT:ANGLE",kind="string")
        self._current_channel=1
        if self._range_mode=="both":  # synchronize amp/off and high/low settings
            for ch in range(1,self._channels_number+1):
                self.set_output_range(self.get_output_range(channel=ch),channel=ch)
    _all_parameters={   "output_on","output_polarity","output_sync","output_load",
                        "amplitude","offset","frequency","phase","voltage_unit","phase_unit",
                        "function","duty_cycle","ramp_symmetry","pulse_width",
                        "burst_enabled","burst_mode","burst_ncycles","gate_polarity",
                        "trigger_source","trigger_slope","trigger_output","output_trigger_slope"}  # not used, but good for reference / use in derived classes

    _p_polarity=interface.EnumParameterClass("polarity",["norm","inv"],value_case="upper",match_prefix=True)
    _p_burst_mode=interface.EnumParameterClass("burst_mode",["trig","gate"],value_case="upper",match_prefix=True)
    _p_trigger_source=interface.EnumParameterClass("trigger_source",["imm","ext","bus"],value_case="upper",match_prefix=True)
    _p_slope=interface.EnumParameterClass("slope",["pos","neg"],value_case="upper",match_prefix=True)
    def _detect_channels_number(self):
        if self._channels_number=="auto":
            return 2 if self._is_command_valid("OUTPUT2?") else 1
        else:
            return self._channels_number
    def get_channels_number(self):
        """Get the number of channels"""
        return self._channels_number
    def _can_add_command(self, name, channel=1):
        return not (name in self._exclude_commands or (name in self._single_channel_commands and channel>1))
    def _check_command(self, name, channel=1, raise_error=True):
        channel=self._get_channel(channel)
        if not self._can_add_command(name,channel=channel):
            if raise_error:
                raise self.Error("option '{}' for channel {} is not supported by this device".format(name,channel))
            return False
        return True
    def _add_scpi_parameter(self, name, comm, kind="float", parameter=None, set_delay=0, channel=None, comm_kind="source", add_variable=False):  # pylint: disable=arguments-differ
        if channel is not None and name not in self._all_channel_commands:
            if not self._can_add_command(name,channel):
                return
            name=self._build_variable_name(name,channel)
            comm=self._build_channel_command(comm,channel,kind=comm_kind)
        return super()._add_scpi_parameter(name,comm,kind=kind,parameter=parameter,set_delay=set_delay,add_variable=add_variable)
    def _modify_scpi_parameter(self, name, comm, kind=None, parameter=None, set_delay=0, channel=None, comm_kind="source"):  # pylint: disable=arguments-differ
        if channel is not None and name not in self._all_channel_commands:
            if not self._can_add_command(name,channel):
                return
            name=self._build_variable_name(name,channel)
            comm=self._build_channel_command(comm,channel,kind=comm_kind)
        return super()._modify_scpi_parameter(name,comm,kind=kind,parameter=parameter,set_delay=set_delay)
    def _add_settings_variable(self, path, getter=None, setter=None, ignore_error=(), mux=None, multiarg=True, channel=None):  # pylint: disable=arguments-differ, arguments-renamed
        if channel is not None and path not in self._all_channel_commands:
            if not self._can_add_command(path,channel):
                return
            path=self._build_variable_name(path,channel)
            if getter is not None:
                ogetter=getter
                getter=lambda *args: ogetter(*args,channel=channel)
            if getter is not None:
                osetter=setter
                setter=lambda *args: osetter(*args,channel=channel)
        return super()._add_settings_variable(path,getter=getter,setter=setter,ignore_error=ignore_error,mux=mux,multiarg=multiarg)
    def _get_channel_scpi_parameter(self, name, channel=None):
        self._check_command(name,channel=channel)
        if name in self._all_channel_commands:
            return self._get_scpi_parameter(name)
        channel=self._get_channel(channel)
        return self._get_scpi_parameter(self._build_variable_name(name,channel))
    def _set_channel_scpi_parameter(self, name, value, channel=None, result=False):
        self._check_command(name,channel=channel)
        if name in self._all_channel_commands:
            return self._set_scpi_parameter(name,value,result=result)
        channel=self._get_channel(channel)
        return self._set_scpi_parameter(self._build_variable_name(name,channel),value,result=result)
    def _get_scpi_parameter(self, name):
        try:
            return super()._get_scpi_parameter(name)
        except KeyError:
            raise self.Error("option '{}' is not supported by this device".format(name))
    def _set_scpi_parameter(self, name, value, result=False):
        try:
            return super()._set_scpi_parameter(name,value,result=result)
        except KeyError:
            raise self.Error("option '{}' is not supported by this device".format(name))
    def _ask_channel(self, msg, data_type="string", delay=0., timeout=None, read_echo=False, name=None, channel=None, comm_kind="source"):
        self._check_command(name,channel=channel)
        if name not in self._all_channel_commands:
            msg=self._build_channel_command(msg,channel,kind=comm_kind)
        return super().ask(msg,data_type=data_type,delay=delay,timeout=timeout,read_echo=read_echo)
    def _write_channel(self, msg, arg=None, arg_type=None, unit=None, bool_selector=("OFF","ON"), wait_sync=None, read_echo=False, read_echo_delay=0., name=None, channel=None, comm_kind="source"):
        self._check_command(name,channel=channel)
        if name not in self._all_channel_commands:
            msg=self._build_channel_command(msg,channel,kind=comm_kind)
        return super().write(msg,arg=arg,arg_type=arg_type,unit=unit,bool_selector=bool_selector,wait_sync=wait_sync,read_echo=read_echo,read_echo_delay=read_echo_delay)

    def _build_variable_name(self, name, channel):
        """Build channel-specific settings variable name"""
        if self._channels_number==1:
            return name
        else:
            return "ch{}/{}".format(channel,name)
    def _build_channel_command(self, comm, channel, kind="source"):
        """Build channel-specific command"""
        channel=self._get_channel(channel)
        if kind=="source":
            if self._channels_number==1:
                return "SOURCE:{}".format(comm) if self._force_channel_source_pfx else comm
            return "SOURCE{}:{}".format(channel,comm)
        elif kind=="output":
            if self._channels_number==1:
                pfx="OUTPUT"
            else:
                pfx="OUTPUT{}".format(channel)
            return pfx+":"+comm if comm else pfx
    def _check_ch(self, channel=None):
        if channel is not None and (channel<1 or channel>self._channels_number):
            raise ValueError("invalid channel: {}".format(channel))
    def _get_channel(self, channel=None):
        self._check_ch(channel)
        return self._current_channel if channel is None else channel

    def get_current_channel(self):
        """Get current channel"""
        return self._current_channel
    def select_current_channel(self, channel):
        """Select current default channel"""
        self._check_ch(channel)
        self._current_channel=channel
    
    def is_output_enabled(self, channel=None):
        """Check if the output is enabled"""
        return self._get_channel_scpi_parameter("output_on",channel=channel)
    def enable_output(self, enabled=True, channel=None):
        """Turn the output on or off"""
        return self._set_channel_scpi_parameter("output_on",enabled,channel=channel,result=True)

    
    def get_output_polarity(self, channel=None):
        """
        Get output polarity.

        Can be either ``"norm"`` or ``"inv"``.
        """
        return self._get_channel_scpi_parameter("output_polarity",channel=channel)
    def set_output_polarity(self, polarity="norm", channel=None):
        """
        Set output polarity.

        Can be either ``"norm"`` or ``"inv"``.
        """
        return self._set_channel_scpi_parameter("output_polarity",polarity,channel=channel,result=True)
    def is_sync_output_enabled(self, channel=None):
        """Check if SYNC output is enabled"""
        return self._get_channel_scpi_parameter("output_sync",channel=channel)
    def enable_sync_output(self, enabled=True, channel=None):
        """Enable or disable SYNC output"""
        return self._set_channel_scpi_parameter("output_sync",enabled,channel=channel,result=True)
        
    def get_load(self, channel=None):
        """Get the output load"""
        value=self._get_channel_scpi_parameter("output_load",channel=channel)
        if value.lower()=="def":
            return self._default_load
        if value.lower()=="inf":
            return self._inf_load
        return min(float(value),self._inf_load)
    def set_load(self, load=None, channel=None):
        """Set the output load (``None`` means High-Z)"""
        load="INF" if load is None else load
        self._set_channel_scpi_parameter("output_load",str(load),channel=channel)
        return self.get_load(channel=channel)
        
    def get_function(self, channel=None):
        """
        Get output function.

        Can be one of the following: ``"sine"``, ``"square"``, ``"ramp"``, ``"pulse"``, ``"noise"``, ``"prbs"``, ``"DC"``, ``"user"``, ``"arb"``.
        Not all functions can be available, depending on the particular model of the generator.
        """
        return self._get_channel_scpi_parameter("function",channel=channel)
    def set_function(self, func, channel=None):
        """
        Set output function.

        Can be one of the following: ``"sine"``, ``"square"``, ``"ramp"``, ``"pulse"``, ``"noise"``, ``"prbs"``, ``"DC"``, ``"user"``, ``"arb"``.
        Not all functions can be available, depending on the particular model of the generator.
        """
        return self._set_channel_scpi_parameter("function",func,channel=channel,result=True)
    
    def get_amplitude(self, channel=None):
        """Get output amplitude (i.e., half of the span)"""
        self._set_scpi_parameter("voltage_unit","VPP")
        return self._get_channel_scpi_parameter("amplitude",channel=channel)/2
    def set_amplitude(self, amplitude, channel=None):
        """Set output amplitude (i.e., half of the span)"""
        self._set_scpi_parameter("voltage_unit","VPP")
        return self._set_channel_scpi_parameter("amplitude",amplitude*2,channel=channel,result=True)/2
    def get_offset(self, channel=None):
        """Get output offset"""
        return self._get_channel_scpi_parameter("offset",channel=channel)
    def set_offset(self, offset, channel=None):
        """Set output offset"""
        return self._set_channel_scpi_parameter("offset",offset,channel=channel,result=True)
    def get_output_range(self, channel=None):
        """
        Get output voltage range.
        
        Return tuple ``(vmin, vmax)`` with the low and high voltage values (i.e., ``offset-amplitude`` and ``offset+amplitude``).
        """
        if self._range_mode=="high_low":
            low=self._ask_channel("VOLTAGE:LOW?","float",name="voltage",channel=channel)
            high=self._ask_channel("VOLTAGE:HIGH?","float",name="voltage",channel=channel)
            return low,high
        else:
            amp=self.get_amplitude(channel=channel)
            off=self.get_offset(channel=channel)
            return off-amp,off+amp
    def set_output_range(self, rng, channel=None):
        """
        Set output voltage range.
        
        If span is less than ``1E-4``, automatically switch to DC mode.
        """
        try:
            low,high=min(rng),max(rng)
        except TypeError:
            low,high=rng,rng
        if abs(high-low)<1E-4 and "dc" in self._supported_functions:
            self.set_function("DC",channel=channel)
            self.set_amplitude(10E-3,channel=channel)
            self.set_offset((high+low)/2.,channel=channel)
        else:
            if self._range_mode in {"high_low","both"}:
                curr_rng=self.get_output_range(channel=channel)
                if low<curr_rng[1]:
                    self._write_channel("VOLTAGE:LOW",low,"float",name="voltage",channel=channel)
                    self._write_channel("VOLTAGE:HIGH",high,"float",name="voltage",channel=channel)
                else:
                    self._write_channel("VOLTAGE:HIGH",high,"float",name="voltage",channel=channel)
                    self._write_channel("VOLTAGE:LOW",low,"float",name="voltage",channel=channel)
            if self._range_mode in {"amp_off","both"}:
                amp,off=(rng[1]-rng[0])/2,(rng[1]+rng[0])/2
                curr_amp=self.get_amplitude(channel=channel)
                if curr_amp>=amp:
                    self.set_amplitude(amp,channel=channel)
                    self.set_offset(off,channel=channel)
                else:
                    self.set_offset(off,channel=channel)
                    self.set_amplitude(amp,channel=channel)
        return self.get_output_range(channel=channel)
    
    def get_frequency(self, channel=None):
        """Get output frequency"""
        value,unit=self._ask_channel("FREQUENCY?","value",name="frequency",channel=channel)
        return units.convert_frequency_units(value,unit or "Hz","Hz")
    def set_frequency(self, frequency, channel=None):
        """Set output frequency"""
        self._write_channel("FREQUENCY",frequency,"float",name="frequency",channel=channel)
        return self.get_frequency(channel=channel)
    def get_phase(self, channel=None):
        """Get output phase (in degrees)"""
        if self._channels_number==1:
            return None
        if self._set_angle_unit:
            self._set_scpi_parameter("phase_unit","DEG")
        fact=360/(2*np.pi) if self._default_angle_unit=="rad" else 1
        return self._get_channel_scpi_parameter("phase",channel=channel)*fact
    def set_phase(self, phase, channel=None):
        """Set output phase (in degrees)"""
        if self._channels_number==1:
            return None
        if self._set_angle_unit:
            self._set_scpi_parameter("phase_unit","DEG")
        fact=360/(2*np.pi) if self._default_angle_unit=="rad" else 1
        return self._set_channel_scpi_parameter("phase",phase/fact,channel=channel,result=True)*fact
    def sync_phase(self):
        """Synchronize phase between two channels"""
        if self._channels_number>1:
            self.write("SOURCE1:PHASE:SYNC")
    
    def get_duty_cycle(self, channel=None):
        """
        Get output duty cycle (in percent).

        Only applies to ``"square"`` output function.
        """
        return self._get_channel_scpi_parameter("duty_cycle",channel=channel)
    def set_duty_cycle(self, dcycle, channel=None):
        """
        Set output duty cycle (in percent).

        Only applies to ``"square"`` output function.
        """
        return self._set_channel_scpi_parameter("duty_cycle",dcycle,channel=channel,result=True)
    def get_ramp_symmetry(self, channel=None):
        """
        Get output ramp symmetry (in percent).

        Only applies to ``"ramp"`` output function.
        """
        return self._get_channel_scpi_parameter("ramp_symmetry",channel=channel)
    def set_ramp_symmetry(self, rsymm, channel=None):
        """
        Set output ramp symmetry (in percent).

        Only applies to ``"ramp"`` output function.
        """
        return self._set_channel_scpi_parameter("ramp_symmetry",rsymm,channel=channel,result=True)
    def get_pulse_width(self, channel=None):
        """
        Get output pulse width (in seconds).

        Only applies to ``"pulse"`` output function.
        """
        return self._get_channel_scpi_parameter("pulse_width",channel=channel)
    def set_pulse_width(self, width, channel=None):
        """
        Set output pulse width (in seconds).

        Only applies to ``"pulse"`` output function.
        """
        return self._set_channel_scpi_parameter("pulse_width",width,channel=channel,result=True)

    def is_burst_enabled(self, channel=None):
        """Check if the burst mode is enabled"""
        return self._get_channel_scpi_parameter("burst_enabled",channel=channel)
    def enable_burst(self, enabled=True, channel=None):
        """Enable burst mode"""
        return self._set_channel_scpi_parameter("burst_enabled",enabled,channel=channel,result=True)
    def get_burst_mode(self, channel=None):
        """
        Get burst mode.

        Can be either ``"trig"`` or ``"gate"``.
        """
        return self._get_channel_scpi_parameter("burst_mode",channel=channel)
    def set_burst_mode(self, mode, channel=None):
        """
        Set burst mode.

        Can be either ``"trig"`` or ``"gate"``.
        """
        return self._set_channel_scpi_parameter("burst_mode",mode,channel=channel,result=True)
    def get_burst_ncycles(self, channel=None):
        """
        Get burst mode ncycles.

        Infinite corresponds to a large value (>1E37).
        """
        return self._ask_channel("BURST:NCYC?","int",name="burst_ncycles",channel=channel)
    def set_burst_ncycles(self, ncycles=1, channel=None):
        """
        Set burst mode ncycles.

        Infinite corresponds to ``None``
        """
        ncycles="INF" if ncycles is None or ncycles>1E37 else ncycles
        self._write_channel("BURST:NCYC",int(ncycles),"int",name="burst_ncycles",channel=channel)
        self.sleep(0.1)
        return self.get_burst_ncycles(channel=channel)
    def get_gate_polarity(self, channel=None):
        """
        Get burst gate polarity.

        Can be either ``"norm"`` or ``"inv"``.
        """
        return self._get_channel_scpi_parameter("gate_polarity",channel=channel)
    def set_gate_polarity(self, polarity="norm", channel=None):
        """
        Set burst gate polarity.

        Can be either ``"norm"`` or ``"inv"``.
        """
        return self._set_channel_scpi_parameter("gate_polarity",polarity,channel=channel,result=True)
    
    
    def get_trigger_source(self, channel=None):
        """
        Get trigger source.

        Can be either ``"imm"``, ``"ext"``, or ``"bus"``.
        """
        return self._get_channel_scpi_parameter("trigger_source",channel=channel)
    def set_trigger_source(self, src, channel=None):
        """
        Set trigger source.

        Can be either ``"imm"``, ``"ext"``, or ``"bus"``.
        """
        return self._set_channel_scpi_parameter("trigger_source",src,channel=channel,result=True)
    def get_trigger_slope(self, channel=None):
        """
        Get trigger slope.

        Can be either ``"pos"``, or ``"neg"``.
        """
        return self._get_channel_scpi_parameter("trigger_slope",channel=channel)
    def set_trigger_slope(self, slope, channel=None):
        """
        Set trigger slope.

        Can be either ``"pos"``, or ``"neg"``.
        """
        return self._set_channel_scpi_parameter("trigger_slope",slope,channel=channel,result=True)
    def is_trigger_output_enabled(self, channel=None):
        """Check if the trigger output is enabled"""
        return self._get_channel_scpi_parameter("trigger_output",channel=channel)
    def enable_trigger_output(self, enabled=True, channel=None):
        """Enable trigger output"""
        return self._set_channel_scpi_parameter("trigger_output",enabled,channel=channel,result=True)
    def get_output_trigger_slope(self, channel=None):
        """
        Get output trigger slope.

        Can be either ``"pos"``, or ``"neg"``.
        """
        return self._get_channel_scpi_parameter("output_trigger_slope",channel=channel)
    def set_output_trigger_slope(self, slope, channel=None):
        """
        Set output trigger slope.

        Can be either ``"pos"``, or ``"neg"``.
        """
        return self._set_channel_scpi_parameter("output_trigger_slope",slope,channel=channel,result=True)
