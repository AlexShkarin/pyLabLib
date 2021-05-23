from builtins import range

from ...core.devio import SCPI, units, data_format  #@UnresolvedImport
from ...core.utils import general, funcargparse  #@UnresolvedImport

import numpy as np

_depends_local=["...core.devio.SCPI"]





class AWG33220A(SCPI.SCPIDevice):
    """
    Agilent AWG33220A Arbitrary Wave Generator.

    Also partially works with compatible AWGs such as Agilent 33500, Rigol D1000, etc.
    """
    def __init__(self, addr):
        SCPI.SCPIDevice.__init__(self,addr,term_write="\n")
        self._add_settings_node("output_on",self.get_output,None)
        self._add_scpi_parameter("output_polarity",":OUTPUT:POLARITY",kind="enum",options={"NORM":"norm","INV":"inv"},add_node=True)
        self._add_scpi_parameter("output_sync",":OUTPUT:SYNC",kind="bool",add_node=True)
        self._add_settings_node("range",self.get_range,self.set_range,multiarg=False)
        self._add_settings_node("load",self.get_load,self.set_load)
        self._add_settings_node("frequency",self.get_frequency,self.set_frequency)
        self._add_settings_node("phase",self.get_phase,self.set_phase)
        functions={"SIN":"sine","SQU":"square","RAMP":"ramp","PULS":"pulse","NOIS":"noise","PRBS":"prbs","DC":"DC","USER":"user","ARB":"arb"}
        self._add_scpi_parameter("function",":FUNCTION",kind="enum",options=functions,add_node=True)
        self._add_scpi_parameter("duty_cycle",":FUNCTION:SQUARE:DCYCLE",add_node=True)
        self._add_scpi_parameter("ramp_symmetry",":FUNCTION:RAMP:SYMMETRY",add_node=True)
        self._add_scpi_parameter("burst_enabled",":BURST:STATE",kind="bool",add_node=True)
        self._add_scpi_parameter("burst_mode",":BURST:MODE",kind="enum",options={"TRIG":"trig","GAT":"gate"},add_node=True)
        self._add_settings_node("burst_ncycles",self.get_burst_ncycles,self.set_burst_ncycles)
        self._add_scpi_parameter("gate_polarity",":BURST:GATE:POL",kind="enum",options={"NORM":"norm","INV":"inv"},add_node=True)
        self._add_scpi_parameter("trigger_source",":TRIG:SOURCE",kind="enum",options={"IMM":"imm","EXT":"ext","BUS":"bus"},add_node=True)
        self._add_scpi_parameter("trigger_slope",":TRIG:SLOPE",kind="enum",options={"POS":"pos","NEG":"neg"},add_node=True)
        self._add_scpi_parameter("trigger_output",":OUTPUT:TRIG",kind="bool",add_node=True)
        self._add_scpi_parameter("output_trigger_slope",":OUTPUT:TRIG:SLOPE",kind="enum",options={"POS":"pos","NEG":"neg"},add_node=True)
    
    def get_output(self):
        """Check if the output is enabled"""
        return self.ask(":OUTPUT?","bool")
    def set_output(self, enabled=True):
        """Turn the output on or off"""
        self.write(":OUTPUT",enabled)
        return self.get_output()

    
    def get_output_polarity(self):
        """
        Get output polarity.

        Can be either ``"norm"`` or ``"inv"``.
        """
        return self._get_scpi_parameter("output_polarity")
    def set_output_polarity(self, polarity="norm"):
        """
        Set output polarity.

        Can be either ``"norm"`` or ``"inv"``.
        """
        return self._set_scpi_parameter("output_polarity",polarity)
    def is_sync_output_enabled(self):
        """Check if SYNC output is enabled"""
        return self._get_scpi_parameter("sync_output")
    def enable_sync_output(self, enabled=True):
        """Enable or disable SYNC output"""
        return self._set_scpi_parameter("sync_output",enabled)
        
    def get_load(self):
        """Get the output load"""
        return self.ask("OUTPUT:LOAD?","float")
    def set_load(self, load=None):
        """Set the output load (``None`` means High-Z)"""
        if load is None:
            self.write("OUTPUT:LOAD INF")
        else:
            self.write("OUTPUT:LOAD",load,"float")
        return self.get_load()
        
    def get_function(self):
        """
        Get output function.

        Can be one of the following: ``"sine"``, ``"square"``, ``"ramp"``, ``"pulse"``, ``"noise"``, ``"prbs"``, ``"DC"``, ``"user"``, ``"arb"``.
        Not all functions can be available, depending on the particular model of the generator.
        """
        return self._get_scpi_parameter("function")
    def set_function(self, func):
        """
        Set output function.

        Can be one of the following: ``"sine"``, ``"square"``, ``"ramp"``, ``"pulse"``, ``"noise"``, ``"prbs"``, ``"DC"``, ``"user"``, ``"arb"``.
        Not all functions can be available, depending on the particular model of the generator.
        """
        return self._set_scpi_parameter("function",func)
    
    def get_amplitude(self):
        """Get output amplitude"""
        self.write(":VOLTAGE:UNIT VPP")
        return self.ask(":VOLTAGE?","float")/2.
    def set_amplitude(self, amplitude):
        """Set output amplitude"""
        self.write(":VOLTAGE",amplitude*2.,"float",unit="Vpp")
        return self.get_amplitude()
    def get_offset(self):
        """Get output offset"""
        return self.ask(":VOLTAGE:OFFSET?","float")
    def set_offset(self, offset):
        """Set output offset"""
        return self.write(":VOLTAGE:OFFSET",offset,"float")
    def get_range(self):
        """
        Get output voltage range.
        
        Return tuple ``(vmin, vmax)`` with the low and high voltage values (i.e., ``offset-amplitude`` and ``offset+amplitude``).
        """
        return self.ask(":VOLTAGE:LOW?","float"),self.ask(":VOLTAGE:HIGH?","float")
    def set_range(self, rng):
        """
        Set output voltage range.
        
        If span is less than ``1E-4``, automatically switch to DC mode.
        """
        try:
            low,high=min(rng),max(rng)
        except TypeError:
            low,high=rng,rng
        if abs(high-low)<1E-4:
            self.set_function("DC")
            self.set_amplitude(10E-3)
            self.set_offset((high+low)/2.)
        else:
            curr_rng=self.get_range()
            if low<curr_rng[1]:
                self.write("VOLTAGE:LOW",low,"float")
                self.write("VOLTAGE:HIGH",high,"float")
            else:
                self.write("VOLTAGE:HIGH",high,"float")
                self.write("VOLTAGE:LOW",low,"float")
        return self.get_range()
    
    def get_frequency(self):
        """Get output frequency"""
        value,unit=self.ask(":FREQUENCY?","value")
        return units.convert_frequency_units(value,unit or "Hz","Hz")
    def set_frequency(self, frequency):
        """Set output frequency"""
        self.write(":FREQUENCY",frequency,"float",unit="Hz")
        return self.get_frequency()
    def get_phase(self):
        """Get output phase (in degrees)"""
        self.write(":UNIT:ANGLE DEG")
        return self.ask(":PHASE?","float")
    def set_phase(self, phase):
        """Set output phase (in degrees)"""
        self.write(":UNIT:ANGLE DEG")
        self.write(":PHASE",phase,"float")
        return self.get_phase()
    
    def get_duty_cycle(self):
        """
        Get output duty cycle (in percent).

        Only applies to ``"square"`` output function.
        """
        return self._get_scpi_parameter("duty_cycle")
    def set_duty_cycle(self, dcycle):
        """
        Set output duty cycle (in percent).

        Only applies to ``"square"`` output function.
        """
        return self._set_scpi_parameter("duty_cycle",dcycle)
    def get_ramp_symmetry(self):
        """
        Get output ramp symmetry (in percent).

        Only applies to ``"ramp"`` output function.
        """
        return self._get_scpi_parameter("ramp_symmetry")
    def set_ramp_symmetry(self, rsymm):
        """
        Set output ramp symmetry (in percent).

        Only applies to ``"ramp"`` output function.
        """
        return self._set_scpi_parameter("ramp_symmetry",rsymm)

    def is_burst_enabled(self):
        """Check if the burst mode is enabled"""
        return self._get_scpi_parameter("burst_enabled")
    def enable_burst(self, enabled=True):
        """Enable burst mode"""
        return self._set_scpi_parameter("burst_enabled",enabled)
    def get_burst_mode(self):
        """
        Get burst mode.

        Can be either ``"trig"`` or ``"gate"``.
        """
        return self._get_scpi_parameter("burst_mode")
    def set_burst_mode(self, mode):
        """
        Set burst mode.

        Can be either ``"trig"`` or ``"gate"``.
        """
        return self._set_scpi_parameter("burst_mode",mode)
    def get_burst_ncycles(self):
        """
        Get burst mode ncycles.

        Infinite corresponds to a large value (>1E37).
        """
        return self.ask(":BURST:NCYC?","float")
    def set_burst_ncycles(self, ncycles=1):
        """
        Set burst mode ncycles.

        Infinite corresponds to ``None``
        """
        if ncycles is None or ncycles>1E37:
            self.write(":BURST:NCYC INF")
        else:
            self.write(":BURST:NCYC",ncycles)
        return self.get_burst_ncycles()
    def get_gate_polarity(self):
        """
        Get burst gate polarity.

        Can be either ``"norm"`` or ``"inv"``.
        """
        return self._get_scpi_parameter("gate_polarity")
    def set_gate_polarity(self, polarity="norm"):
        """
        Set burst gate polarity.

        Can be either ``"norm"`` or ``"inv"``.
        """
        return self._set_scpi_parameter("gate_polarity",polarity)
    
    
    def get_trigger_source(self):
        """
        Get trigger source.

        Can be either ``"imm"``, ``"ext"``, or ``"bus"``.
        """
        return self._get_scpi_parameter("trigger_source")
    def set_trigger_source(self, src):
        """
        Set trigger source.

        Can be either ``"imm"``, ``"ext"``, or ``"bus"``.
        """
        return self._set_scpi_parameter("trigger_source",src)
    def get_trigger_slope(self):
        """
        Get trigger slope.

        Can be either ``"pos"``, or ``"neg"``.
        """
        return self._get_scpi_parameter("trigger_slope")
    def set_trigger_slope(self, slope):
        """
        Set trigger slope.

        Can be either ``"pos"``, or ``"neg"``.
        """
        return self._set_scpi_parameter("trigger_slope",slope)
    def is_trigger_output_enabled(self):
        """Check if the trigger output is enabled"""
        return self._get_scpi_parameter("trigger_output")
    def enable_trigger_output(self, enabled=True):
        """Enable trigger output"""
        return self._set_scpi_parameter("trigger_output",enabled)
    def get_output_trigger_slope(self):
        """
        Get output trigger slope.

        Can be either ``"pos"``, or ``"neg"``.
        """
        return self._get_scpi_parameter("output_trigger_slope")
    def set_output_trigger_slope(self, slope):
        """
        Set output trigger slope.

        Can be either ``"pos"``, or ``"neg"``.
        """
        return self._set_scpi_parameter("output_trigger_slope",slope)


        
    def apply_settings(self, settings):
        if "output_on" in settings and not settings["output_on"]:
            self.set_output(False)
        SCPI.SCPIDevice.apply_settings(self,settings)
        if "output_on" in settings and settings["output_on"]:
            self.set_output(True)
        return self.get_settings()





class AMP33502A(SCPI.SCPIDevice):
    """
    Agilent AMP3350A amplifier.
    """
    def __init__(self, addr):
        SCPI.SCPIDevice.__init__(self,addr)
    
    def get_output(self, channel=None):
        return self.ask("OUTPUT{}:STATE?".format(channel+1),"bool")
    def set_output(self, channel, enabled=True):
        self.write("OUTPUT{}:STATE".format(channel+1),enabled)
        return self.get_output(channel)
    def get_path(self, channel):
        return self.ask("ROUTE{}:PATH?".format(channel+1),"string").lower()
    def set_path(self, channel, path):
        funcargparse.check_parameter_range(path,"path",{"dir","ampl"})
        self.write("ROUTE{}:PATH".format(channel+1),path.upper())
        return self.get_path(channel)
        
    def get_coupling(self, channel):
        return self.ask("INPUT{}:COUPLING?".format(channel+1),"string").lower()
    def set_coupling(self, channel, coupling):
        funcargparse.check_parameter_range(coupling,"coupling",{"ac","dc"})
        self.write("INPUT{}:COUPLING".format(channel+1),coupling.upper())
        return self.get_coupling(channel)
    def get_impedance(self, channel):
        return self.ask("INPUT{}:IMPEDANCE?".format(channel+1),"float")
    def set_impedance(self, channel, impedance):
        self.write("INPUT{}:IMPEDANCE".format(channel+1),impedance)
        return self.get_impedance(channel)
        
    
    def get_settings(self):
        settings=SCPI.SCPIDevice.get_settings(self)
        settings["output_on"]=[self.get_output(ch) for ch in [0,1]]
        settings["path"]=[self.get_path(ch) for ch in [0,1]]
        settings["coupling"]=[self.get_coupling(ch) for ch in [0,1]]
        settings["impedance"]=[self.get_impedance(ch) for ch in [0,1]]
        return settings
    def apply_settings(self, settings):
        for ch in [0,1]:
            ch_settings={}
            for k in {"output_on","path","coupling","impedance"}:
                if k in settings:
                    if isinstance(settings[k],list):
                        ch_settings[k]=settings[k][ch]
                    else:
                        ch_settings[k]=settings[k]
            if "output_on" in ch_settings and not ch_settings["output_on"]:
                self.set_output(False)
            if "path" in ch_settings:
                self.set_path(ch,ch_settings["path"])
            if "coupling" in ch_settings:
                self.set_coupling(ch,ch_settings["coupling"])
            if "impedance" in ch_settings:
                self.set_impedance(ch,ch_settings["impedance"])
            if "output_on" in ch_settings and ch_settings["output_on"]:
                self.set_output(True)
        return self.get_settings()





class N9310A(SCPI.SCPIDevice):
    """
    Agilent N9310A microwave generator.
    """
    def __init__(self, addr):
        SCPI.SCPIDevice.__init__(self,addr)
        self._add_settings_node("power_on",self.get_output,None)
        self._add_settings_node("power",self.get_output_level,self.set_output_level)
        self._add_settings_node("frequency",self.get_frequency,self.set_frequency)
    
    def get_output(self):
        return self.ask(":RFOUTPUT:STATE?","bool")
    def set_output(self, enabled=True):
        self.write(":RFOUTPUT:STATE",enabled)
    def get_output_level(self):
        value,unit=self.ask(":AMPLITUDE:CW?","value")
        return units.convert_power_units(value,unit or "dBm","dBm")
    def set_output_level(self, level):
        if level is None:
            self.set_output(False)
            return None
        else:
            self.write(":AMPLITUDE:CW",level,"float",unit="dBm")
            return self.get_output_level()
    
    def get_frequency(self):
        value,unit=self.ask(":FREQUENCY:CW?","value")
        return units.convert_frequency_units(value,unit or "Hz","Hz")
    def set_frequency(self, frequency):
        self.write(":FREQUENCY:CW",frequency/1E3,"float",unit="kHz")
        return self.get_frequency()
        
    def apply_settings(self, settings):
        if "power_on" in settings and not settings["power_on"]:
            self.set_output(False)
        SCPI.SCPIDevice.apply_settings(self,settings)
        if "power_on" in settings and settings["power_on"]:
            self.set_output(True)
        return self.get_settings()





class HP8712B(SCPI.SCPIDevice):
    """
    HP8712B Vector Network Analyzer.
    """
    def __init__(self, addr):
        SCPI.SCPIDevice.__init__(self,addr)
        self.channel=1
        self.data_fmt="<f4"
        self._add_settings_node("power_on",self.get_output,None)
        self._add_settings_node("power",self.get_output_level,self.set_output_level)
        self._add_settings_node("frequency_range",self.get_frequency_range,self.set_frequency_range)
        self._add_settings_node("bandwidth",self.get_bandwidth,self.set_bandwidth)
        self._add_settings_node("sweep_points",self.get_sweep_points,self.set_sweep_points)
        self._add_settings_node("avg",self.get_avg,self.set_avg)
        self._add_settings_node("channel_format",self.get_channel_format,self.set_channel_format)
        self._add_settings_node("electrical_delay",self.get_electrical_delay,self.set_electrical_delay)
        self._add_settings_node("channel_format",self.get_phase_offset,self.set_phase_offset)
        
    def select_channel(self, channel):
        self.channel=channel
    def current_channel(self):
        return self.channel
    
    def sweep_single(self, wait_type="sync", count=1):
        if count is None:
            count=1
        self.write(":ABORT;:INIT:CONT OFF;")
        for _ in range(count):
            self.write(":INIT")
            self.wait(wait_type)
    def sweep_reset(self, wait_type="sync"):
        self.write(":ABORT;:INIT")
        self.wait(wait_type)
    def sweep_continuous(self, enable=True):
        self.write(":INIT:CONT",enable)
        if not enable:
            self.write(":ABORT")
    def is_continuous(self):
        return self.ask(":INIT:CONT?","bool")
        
        
    def get_output(self):
        return self.ask(":OUTPUT?","bool")
    def set_output(self, enabled=True):
        self.write(":OUTPUT",enabled)
    def get_output_level(self):
        return self.ask(":SOURCE:POWER?","float")
    def set_output_level(self, level):
        if level is None:
            self.set_output(False)
            return None
        else:
            self.write("SOURCE:POWER",level)
            return self.get_output_level()
    
    
    def get_avg(self):
        avg_on=self.ask(":SENSE{0}:AVERAGE?".format(self.channel),"bool")
        avg_samples=self.ask(":SENSE{0}:AVERAGE:COUNT?".format(self.channel),"int")
        return (avg_on,avg_samples)
    def restart_avg(self):
        self.write(":SENSE{0}:AVERAGE:CLEAR".format(self.channel))
    def set_avg(self, avg=None):
        try:
            avg_on,avg_samples=avg
        except TypeError:
            if (not avg) or avg<=1:
                avg_on=False
                avg_samples=None
            else:
                avg_on=True
                avg_samples=None if avg is True else avg
        self.write(":SENSE{0}:AVERAGE".format(self.channel),avg_on)
        if avg_samples is not None:
            self.write(":SENSE{0}:AVERAGE:COUNT".format(self.channel),avg)
        return self.get_avg()
            
        
    def get_frequency_range(self):
        start=self.ask(":SENSE:FREQ:START?","float")
        stop=self.ask(":SENSE:FREQ:STOP?","float")
        return start,stop
    def set_frequency_range(self, frequency):
        try:
            start,stop=min(frequency),max(frequency)
        except TypeError:
            start,stop=frequency,frequency
        self.write(":SENSE:FREQ:START {0:E};:SENSE:FREQ:STOP {1:E}".format(start,stop))
        return self.get_frequency_range()
    
    def get_sweep_points(self):
        return self.ask(":SENSE:SWEEP:POINTS?","int")
    def set_sweep_points(self, pts):
        self.write(":SENSE:SWEEP:POINTS",int(pts))
        return self.get_sweep_points()
        
    def get_bandwidth(self):
        return self.ask(":SENSE:BWIDTH?","float")
    def set_bandwidth(self, bwidth):
        self.write(":SENSE:BWIDTH",bwidth)
        return self.get_bandwidth()
        
    def get_channel_format(self):
        return self.ask(":CALC{0}:FORMAT?".format(self.channel)).lower()
    def set_channel_format(self, chan_fmt):
        self.write(":CALC{0}:FORMAT {1}".format(self.channel, chan_fmt))
        return self.get_channel_format()
    
    def get_phase_offset(self):
        return self.ask("SENSE{0}:CORR:OFFS:PHAS?","float")
    def set_phase_offset(self, offset):
        self.write("SENSE{0}:CORR:OFFS:PHAS",offset)
        return self.get_phase_offset()
    def get_electrical_delay(self):
        return self.ask("SENSE{0}:CORR:EDEL:TIME?".format(self.channel),"float")
    def set_electrical_delay(self, delay):
        self.write("SENSE{0}:CORR:EDEL:TIME".format(self.channel),delay)
        return self.get_electrical_delay()
        
    
    
    def set_data_format(self, fmt=None):
        fmt=funcargparse.getdefault(fmt,self.data_fmt)
        fmt=data_format.DataFormat.from_desc(fmt)
        if not (fmt.is_ascii() or fmt.to_desc()[1:] in ["f4","f8","i2"]):
            raise ValueError("Format {0} isn't supported".format(fmt))
        self.write(":FORMAT:DATA {0};:FORMAT:BORDER {1}".format(*fmt.to_desc("SCPI")))
    def get_data_format(self):
        enc=self.ask(":FORMAT:DATA?")
        border=self.ask(":FORMAT:BORDER?")
        return data_format.DataFormat.from_desc_SCPI(enc,border).to_desc()
    def request_data(self, source="data", fmt=None):
        fmt=funcargparse.getdefault(fmt,self.data_fmt)
        self.set_data_format(fmt)
        if source=="data":
            data=self.ask(":TRACE:DATA? CH{0}FDATA".format(self.channel),"raw")
        elif source=="memory":
            data=self.ask(":TRACE:DATA? CH{0}FDMEM".format(self.channel),"raw")
        return self.parse_trace_data(data,fmt)
            
            
    def read_sweep(self, transfer_fmt="xy"):
        original_channel_fmt=self.get_channel_format()
        if transfer_fmt=="xy":
            channel_fmts=["real","imag"]
        elif transfer_fmt=="rp":
            channel_fmts=["mlin","phase"]
        else:
            raise ValueError("unrecognized read format: {0}".format(transfer_fmt))
        pts=self.get_sweep_points()
        data=[]
        for chf in channel_fmts:
            self.set_channel_format(chf)
            trace=self.request_data()
            if len(trace)!=pts:
                raise RuntimeError("received data length {0} is not equal to the number of points {1}".format(len(trace),pts))
            data.append(trace)
        freq_range=self.get_frequency_range()
        freqs=np.linspace(freq_range[0],freq_range[1],pts)
        data=np.column_stack(( freqs,data[0],data[1] ))
        self.set_channel_format(original_channel_fmt)
        return data
    def grab_single_sweep(self, transfer_fmt="xy", count=None):
        self.wait()
        if count is None:
            do_avg,avg_count=self.get_avg()
            count=avg_count if do_avg else 1
        cont=self.is_continuous()
        self.sweep_single(count=count)
        data=self.read_sweep(transfer_fmt=transfer_fmt)
        self.sweep_continuous(cont)
        return data
        
    
    def apply_settings(self, settings):
        if "power_on" in settings and not settings["power_on"]:
            self.set_output(False)
        SCPI.SCPIDevice.apply_settings(self,settings)
        if "power_on" in settings and settings["power_on"]:
            self.set_output(True)
        self.wait()
        return self.get_settings()





class HP8722D(SCPI.SCPIDevice):
    """
    HP8722D Vector Network Analyzer.
    """
    def __init__(self, addr):
        SCPI.SCPIDevice.__init__(self,addr)
        self.data_fmt="<f4"
        self._add_settings_node("power_on",self.get_output,None)
        self._add_settings_node("power",self.get_output_level,self.set_output_level)
        self._add_settings_node("frequency_range",self.get_frequency_range,self.set_frequency_range)
        self._add_settings_node("bandwidth",self.get_bandwidth,self.set_bandwidth)
        self._add_settings_node("sweep_points",self.get_sweep_points,self.set_sweep_points)
        self._add_settings_node("avg",self.get_avg,self.set_avg)
        self._add_settings_node("channel_format",self.get_channel_format,self.set_channel_format)
        self._add_settings_node("measurement",self.get_measurement,self.set_measurement)
        self._add_settings_node("electrical_delay",self.get_electrical_delay,self.set_electrical_delay)
        self._add_settings_node("phase_offset",self.get_phase_offset,self.set_phase_offset)
        
    def select_channel(self, channel):
        self.write("CHAN{:d}".format(channel))
        self.wait_sync()
    def current_channel(self):
        for ch in range(1,5):
            if self.ask("CHAN{:d}?".format(ch),bool):
                return ch
        return None
    
    _wait_sync_comm="OPC?;NOOP"
    def wait_dev(self):
        raise NotImplementedError("HP8722D.wait_dev")
        
        
    def sweep_single(self, wait_type="sync", count=1):
        if count is None:
            count=1
        self.write("NUMG",count)
        self.wait(wait_type)
    def sweep_continuous(self, enable=True):
        if enable:
            self.write("CONT")
        else:
            self.write("HOLD")
    def is_continuous(self):
        return self.ask("CONT?","bool")
        
        
    
    def get_output(self):
        return self.ask("SOUP?","bool")
    def set_output(self, enabled=True):
        self.write("SOUP",enabled)
        return self.get_output() if self._setter_echo else None
    def get_output_level(self):
        return self.ask("POWE?","float")
    def set_output_level(self, level):
        if level is None:
            self.set_output(False)
            return None
        else:
            self.write("PWRR ON;POWE",level)
            return self.get_output_level() if self._setter_echo else None
            
    def set_measurement(self, meas):
        self.write(meas)
        return self.get_measurement() if self._setter_echo else None
    def get_measurement(self):
        for meas in ["S11","S12","S21","S22"]:
            if self.ask(meas+"?","bool"):
                return meas
        return None
            
            
    def get_avg(self):
        avg_on=self.ask("AVERO?","bool")
        avg_samples=self.ask("AVERFACT?","int")
        return (avg_on,avg_samples)
    def restart_avg(self):
        self.write("AVERREST")
    def set_avg(self, avg=None):
        try:
            avg_on,avg_samples=avg
        except TypeError:
            if avg is True:
                avg_on=True
                avg_samples=None
            elif (not avg) or avg<=1:
                avg_on=False
                avg_samples=None
            else:
                avg_on=True
                avg_samples=avg
        self.write("AVERO",avg_on)
        if avg_samples is not None:
            self.write("AVERFACT",avg)
        return self.get_avg() if self._setter_echo else None
            
    def get_frequency_range(self):
        start=self.ask("STAR?","float")
        stop=self.ask("STOP?","float")
        return start,stop
    def set_frequency_range(self, frequency):
        try:
            start,stop=min(frequency),max(frequency)
        except TypeError:
            start,stop=frequency,frequency
        self.write("LINFREQ; STAR {0:E};STOP {1:E}".format(start,stop))
        return self.get_frequency_range() if self._setter_echo else None
        
    def get_sweep_points(self):
        return self.ask("POIN?","int")
    def set_sweep_points(self, pts):
        self.write("POIN",int(pts))
        return self.get_sweep_points() if self._setter_echo else None
        
    def get_bandwidth(self):
        return self.ask("IFBW?","float")
    def set_bandwidth(self, bwidth):
        self.write("IFBW",bwidth)
        return self.get_bandwidth() if self._setter_echo else None
        
    _channel_formats={"real":"REAL","imag":"IMAG","mlin":"LINM","mlog":"LOGM","phase":"PHAS"}
    def get_channel_format(self):
        for fmt,comm in self._channel_format.items():
            if self.ask(comm+"?","bool"):
                return fmt
        return None
    def set_channel_format(self, chan_fmt):
        self.write(self._channel_formats[chan_fmt])
        return self.get_channel_format() if self._setter_echo else None
    
    def get_phase_offset(self):
        return self.ask("PHAO?","float")
    def set_phase_offset(self, offset):
        self.write("PHAO",offset)
        return self.get_phase_offset() if self._setter_echo else None
    def get_electrical_delay(self):
        return self.ask("ELED?","float")
    def set_electrical_delay(self, delay):
        self.write("ELED",delay)
        return self.get_electrical_delay() if self._setter_echo else None
        
        
        
    def set_data_format(self, fmt=None):
        fmt=funcargparse.getdefault(fmt,self.data_fmt)
        fmt=data_format.DataFormat.from_desc(fmt)
        if fmt.is_ascii():
            self.write("FORM4")
        elif fmt.to_desc()[1:]=="f4":
            self.write("FORM2")
        elif fmt.to_desc()[1:]=="f8":
            self.write("FORM3")
        else:
            raise ValueError("Format {0} isn't supported".format(fmt))
    @staticmethod
    def parse_trace_data(data, fmt):
        fmt=data_format.DataFormat.from_desc(fmt)
        if fmt.is_ascii():
            return fmt.convert_from_str(data)
        fmt.byteorder=">" # the only byteorder the device understands
        if data[:2]!=b"#A":
            raise ValueError("malformatted data")
        length=data_format.DataFormat.from_desc(">i2").convert_from_str(data[2:4])
        data=data[4:]
        if len(data)!=length:
            raise ValueError("data length {0} doesn't agree with declared length {1}".format(len(data),length))
        return fmt.convert_from_str(data)
    def request_data(self, fmt=None):
        fmt=funcargparse.getdefault(fmt,self.data_fmt)
        self.set_data_format(fmt)
        data=self.ask("OUTPDATA","raw")
        return self.parse_trace_data(data,fmt)
        
        
    def read_sweep(self):
        pts=self.get_sweep_points()
        trace=self.request_data().reshape((-1,2))
        freq_range=self.get_frequency_range()
        freqs=np.linspace(freq_range[0],freq_range[1],pts)
        ctrace=trace[:,0]+1j*trace[:,1]
        ctrace=ctrace*np.exp(1j*2*np.pi*(freqs*self.get_electrical_delay()-self.get_phase_offset()/360.)) # manual offset; network analyzer doesn't do it for OUTPDATA
        data=np.column_stack(( freqs,ctrace.real,ctrace.imag ))
        return data
    def grab_single_sweep(self, count=None):
        self.wait()
        if count is None:
            do_avg,avg_count=self.get_avg()
            count=avg_count if do_avg else 1
        cont=self.is_continuous()
        self.sweep_single(count=count)
        data=self.read_sweep()
        self.sweep_continuous(cont)
        return data
        
        
    def apply_settings(self, settings):
        if "power_on" in settings and not settings["power_on"]:
            self.set_output(False)
        SCPI.SCPIDevice.apply_settings(self,settings)
        if "power_on" in settings and settings["power_on"]:
            self.set_output(True)
        self.wait()