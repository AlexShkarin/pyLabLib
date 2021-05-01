from .generic import GenericAWG


class Agilent33500(GenericAWG):
    """
    Agilent 33500 AWG.

    Args:
        channels_number: number of channels; if ``"auto"``, try to determine automatically (by certain commands causing errors)
    """
    def __init__(self, addr, channels_number="auto"):
        self._channels_number=channels_number
        GenericAWG.__init__(self,addr)


class Agilent33220A(GenericAWG):
    """
    Agilent 33220A AWG.
    """
    pass





class InstekAFG2225(GenericAWG):
    """
    Instek AFG2225 AWG.

    Compared to 2000/2100 series, has one extra channel and a bit more capabilities
    (burst trigger, pulse function)
    """
    _exclude_commands={"output_polarity","output_sync","trigger_output","output_trigger_slope"}
    _supported_functions={"sine","square","noise","ramp","pulse","user"}
    _set_angle_unit=False
    _force_channel_source_pfx=True
    _channels_number=2
    def __init__(self, addr):
        GenericAWG.__init__(self,addr)
        for ch in range(1,self._channels_number+1):
            self._add_scpi_parameter("duty_cycle","SQUARE:DCYCLE",channel=ch,add_variable=True)
            self._add_scpi_parameter("ramp_symmetry","RAMP:SYMMETRY",channel=ch,add_variable=True)
            self._add_scpi_parameter("pulse_width","PULSE:WIDTH",channel=ch,add_variable=True)
            self._add_scpi_parameter("trigger_source","BURST:TRIG:SOURCE",kind="param",parameter="trigger_source",channel=ch,add_variable=True)
            self._add_scpi_parameter("trigger_slope","BURST:TRIG:SLOPE",kind="param",parameter="slope",channel=ch,add_variable=True)
    def get_amplitude(self, channel=None):
        """Get output amplitude"""
        if self._ask_channel("VOLTAGE:UNIT?",name="voltage_unit",channel=channel).upper()!="VPP":
            self._write_channel("VOLTAGE:UNIT","VPP",name="voltage_unit",channel=channel)
        return self._ask_channel("AMPLITUDE?","float",name="amplitude",channel=channel)/2.
    def set_amplitude(self, amplitude, channel=None):
        """Set output amplitude"""
        if self._ask_channel("VOLTAGE:UNIT?",name="voltage_unit",channel=channel).upper()!="VPP":
            self._write_channel("VOLTAGE:UNIT","VPP",name="voltage_unit",channel=channel)
            self._write_channel("AMPLITUDE",amplitude*2,"float",name="amplitude",channel=channel)
            self.sleep(1) # it looks like one needs to wait some time after setting the amplitude; otherwise, there's no response to the next command
        else:
            self._write_channel("AMPLITUDE",amplitude*2,"float",name="amplitude",channel=channel)
        return self.get_amplitude(channel=channel)
    def get_offset(self, channel=None):
        """Get output offset"""
        return self._ask_channel("DCOFFSET?","float",name="offset",channel=channel)
    def set_offset(self, offset, channel=None):
        """Set output offset"""
        self._write_channel("DCOFFSET",offset,"float",name="offset",channel=channel)
        return self.get_offset(channel=channel)
    def get_range(self, channel=None):
        """
        Get output voltage range.
        
        Return tuple ``(vmin, vmax)`` with the low and high voltage values (i.e., ``offset-amplitude`` and ``offset+amplitude``).
        """
        amp=self.get_amplitude(channel=channel)
        off=self.get_offset(channel=channel)
        return off-amp,off+amp
    def set_range(self, rng, channel=None):
        """
        Set output voltage range.
        
        If span is less than ``1E-4``, automatically switch to DC mode.
        """
        try:
            low,high=min(rng),max(rng)
        except TypeError:
            low,high=rng,rng
        if abs(high-low)<1E-4:
            self.set_function("DC",channel=channel)
            self.set_amplitude(10E-3,channel=channel)
            self.set_offset((high+low)/2.,channel=channel)
        else:
            amp,off=(rng[1]-rng[0])/2,(rng[1]+rng[0])/2
            curr_amp=self.get_amplitude(channel=channel)
            if curr_amp>=amp:
                self.set_amplitude(amp,channel=channel)
                self.set_offset(off,channel=channel)
            else:
                self.set_offset(off,channel=channel)
                self.set_amplitude(amp,channel=channel)
        return self.get_range(channel=channel)


class InstekAFG2000(InstekAFG2225):
    """
    Instek AFG2000/2100 series AWG.

    Compared to AFG2225, has only one channel and fewer capabilities.
    """
    _channels_number=1
    _supported_functions=InstekAFG2225._supported_functions-{"pulse"}
    _exclude_commands=InstekAFG2225._exclude_commands|{"pulse_width",
        "burst_enabled","burst_mode","burst_ncycles","gate_polarity",
        "trigger_source","trigger_slope"}





class RigolDG1000(GenericAWG):
    """
    Rigol DG1000 AWG.
    """
    _default_operation_cooldown={"write":1E-2}
    _channels_number=2
    _single_channel_commands={  "output_sync",
                                "burst_enabled","burst_mode","burst_ncycles","gate_polarity",
                                "trigger_source","trigger_slope","trigger_output","output_trigger_slope"}
    _set_angle_unit=False
    def __init__(self, addr):
        GenericAWG.__init__(self,addr)
        for ch in range(1,self._channels_number+1):
            self._add_scpi_parameter("pulse_width","PULSE:WIDTH",channel=ch,add_variable=True)
    def _instr_read(self, raw=False, size=None):
        data=GenericAWG._instr_read(self,raw=raw,size=size)
        if not raw:
            for pfx in [b"CH1:",b"CH2:"]:
                if data.startswith(pfx):
                    data=data[len(pfx):].strip()
                    break
        return data
    def _build_channel_command(self, comm, channel, kind="source"):
        """Build channel-specific command"""
        channel=self._get_channel(channel)
        sfx=""
        if comm.endswith("?"):
            sfx="?"
            comm=comm[:-1]
        if kind=="output":
            comm="OUTPUT:"+comm if comm else "OUTPUT"
        if channel==2:
            comm=comm+":CH2"
        return comm+sfx
    def sync_phase(self):
        """Synchronize phase between two channels"""
        self.write("PHASE:ALIGN")