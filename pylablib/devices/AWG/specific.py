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
    _range_mode="amp_off"
    _amplitude_opc_check=True
    def __init__(self, addr):
        GenericAWG.__init__(self,addr)
        for ch in range(1,self._channels_number+1):
            self._modify_scpi_parameter("offset","DCOFFSET",channel=ch)
            self._modify_scpi_parameter("duty_cycle","SQUARE:DCYCLE",channel=ch)
            self._modify_scpi_parameter("ramp_symmetry","RAMP:SYMMETRY",channel=ch)
            self._modify_scpi_parameter("pulse_width","PULSE:WIDTH",channel=ch)
            self._modify_scpi_parameter("trigger_source","BURST:TRIG:SOURCE",channel=ch)
            self._modify_scpi_parameter("trigger_slope","BURST:TRIG:SLOPE",channel=ch)
    def _set_vpp_unit(self, channel=None):
        if self._check_command("voltage_unit",channel,raise_error=False):
            if self._ask_channel("VOLTAGE:UNIT?",name="voltage_unit",channel=channel).upper()!="VPP":
                self._write_channel("VOLTAGE:UNIT","VPP",name="voltage_unit",channel=channel)
    def get_offset(self, channel=None):
        self._set_vpp_unit(channel=channel)
        return self._ask_channel("DCOFFSET?","float",name="offset",channel=channel)
    def set_offset(self, offset, channel=None):
        self._set_vpp_unit(channel=channel)
        if self._amplitude_opc_check:
            self._write_channel("DCOFFSET {:.3f};*OPC?".format(offset),name="offset",channel=channel)
            self.read()
        else:
            self._write_channel("DCOFFSET",offset,"float",name="offset",channel=channel)
        return self.get_offset(channel=channel)
    def get_amplitude(self, channel=None):
        self._set_vpp_unit(channel=channel)
        return self._ask_channel("AMPLITUDE?","float",name="amplitude",channel=channel)/2.
    def set_amplitude(self, amplitude, channel=None):
        self._set_vpp_unit(channel=channel)
        if self._amplitude_opc_check:
            self._write_channel("AMPLITUDE {:.3f};*OPC?".format(amplitude*2),name="amplitude",channel=channel)
            self.read()
        else:
            self._write_channel("AMPLITUDE",amplitude*2,"float",name="amplitude",channel=channel)
        return self.get_amplitude(channel=channel)


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
    _amplitude_opc_check=False


class RSInstekAFG21000(InstekAFG2000):
    """
    RS Instek AFG21000 series AWG.

    Compared to Instek AFG2000, it takes care of the amplitude output bug.
    """
    def get_offset(self, channel=None):
        inf_load=self.get_load(channel=channel)>1E3
        off=InstekAFG2000.get_offset(self,channel=channel)
        return off*2 if inf_load else off # seems to be the case, that returned values are not adjusted for highZ load (set values are, though)
    def get_amplitude(self, channel=None):
        inf_load=self.get_load(channel=channel)>1E3
        amp=InstekAFG2000.get_amplitude(self,channel=channel)
        return amp*2 if inf_load else amp # seems to be the case, that returned values are not adjusted for highZ load (set values are, though)




class TektronixAFG1000(GenericAWG):
    _function_aliases=GenericAWG._function_aliases.copy()
    _function_aliases["noise"]="PRN"
    _supported_functions={"sine","square","ramp","pulse","noise","user","*"}
    _single_channel_commands={"burst_enabled","burst_mode","burst_ncycles"}
    _exclude_commands={ "duty_cycle","ramp_symmetry",
                        "output_polarity","output_sync","voltage_unit","phase_unit",
                        "gate_polarity","trigger_source","trigger_slope","trigger_output","output_trigger_slope"}
    _range_mode="amp_off"
    _set_angle_unit=False
    _default_angle_unit="rad"
    def __init__(self, addr, channels_number="auto"):
        self._channels_number=channels_number
        GenericAWG.__init__(self,addr)
        for ch in range(1,self._channels_number+1):
            self._modify_scpi_parameter("output_load","IMPEDANCE",comm_kind="output",channel=ch)
            self._add_scpi_parameter("pulse_duty_cycle","PULSE:DCYCLE",channel=ch,add_variable=False)
            self._add_settings_variable("pulse_width",self.get_pulse_width,self.set_pulse_width,channel=ch)
    def get_pulse_width(self, channel=None):
        dcycle=self._get_channel_scpi_parameter("pulse_duty_cycle",channel=channel)
        return (1./self.get_frequency(channel=channel))*(dcycle/100)
    def set_pulse_width(self, width, channel=None):
        dcycle=width*self.get_frequency(channel=channel)*100
        self._set_channel_scpi_parameter("pulse_duty_cycle",dcycle,channel=channel)
        return self.get_pulse_width(channel=channel)



class RigolDG1000(GenericAWG):
    """
    Rigol DG1000 AWG.
    """
    _channels_number=2
    _supported_functions={"sine","square","noise","ramp","pulse","dc","user"}
    _single_channel_commands={  "output_sync",
                                "burst_enabled","burst_mode","burst_ncycles","gate_polarity",
                                "trigger_source","trigger_slope","trigger_output","output_trigger_slope"}
    _range_mode="both"
    _set_angle_unit=False
    def __init__(self, addr):
        GenericAWG.__init__(self,addr)
        for ch in range(1,self._channels_number+1):
            self._modify_scpi_parameter("pulse_width","PULSE:WIDTH",channel=ch)
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