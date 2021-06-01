from ...core.utils import numerical
from ...core.devio import interface, comm_backend

import re

class OZOpticsError(comm_backend.DeviceError):
    """Generic OZOptics devices error"""
class OZOpticsBackendError(OZOpticsError,comm_backend.DeviceBackendError):
    """Generic OZOptics backend communication error"""


class OZOpticsDevice(comm_backend.ICommBackendWrapper):
    """
    Generic OZOptics device.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    Error=OZOpticsError
    def __init__(self, conn, timeout=20.):
        instr=comm_backend.new_backend(conn,"serial",term_write="\r\n",timeout=timeout,datatype="str",defaults={"serial":("COM1",9600)},reraise_error=OZOpticsBackendError)
        super().__init__(instr)
        self._add_status_variable("configuration",self.get_config)
        
    def _parse_response(self, comm, resp):
        resp=[s.strip() for s in resp.splitlines() if s.strip()]
        if resp and (resp[0]==comm):
            resp=resp[1:]
        if resp and (resp[0].startswith("Error")):
            raise OZOpticsError("command {} returned error: {}".format(comm,resp))
        return resp
    def query(self, comm, prefix=None, prefix_line=None, timeout=None):
        """
        Query the device.

        If `prefix` is not ``None``, it can specify a string which should be at the beginning of the `prefix_line` line of the reply.
        If it is present, it is removed and the rest of that line is returned; otherwise, an error is raised.
        If `prefix_line` is ``None``, return the first reply line beginning with the given prefix value (or raise an error if not such line is present).
        """
        comm=comm.strip()
        self.instr.flush_read()
        self.instr.write(comm)
        resp=self.instr.read_multichar_term(["Done\r\n","Error!\r\n"],timeout=timeout)
        resp=self._parse_response(comm,resp)
        if prefix:
            if prefix_line is None:
                for ln in resp:
                    ln=ln.upper()
                    if ln.startswith(prefix.upper()):
                        return ln[len(prefix):].strip()
            else:
                ln=resp[prefix_line].upper()
                if ln.startswith(prefix.upper()):
                    return ln[len(prefix):].strip()
            raise OZOpticsError("unexpected reply: {}".format(resp))
        return resp
    
    def restart(self):
        """Restart the device"""
        return self.query("RST",timeout=40.)
    def get_config(self):
        """Get device configuration"""
        return self.query("CD")
    


class TF100(OZOpticsDevice):
    """
    OZOptics TF100 tunable filter.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    def __init__(self, conn, timeout=20.):
        super().__init__(conn,timeout=timeout)
        self._add_settings_variable("wavelength",self.get_wavelength,self.set_wavelength)
        self._add_settings_variable("wavelength_correction",self.get_wavelength_correction, self.set_wavelength_correction)
        self.wshift=0.
        self.wscale=1.
    
    # wavelength_device = wavelength_real*scale+shift
    def get_wavelength_correction(self):
        """
        Get the current wavelength correction parameters ``(shift, scale)``.

        The relation between the set/get wavelength and the wavelength set to the device is calculated as
        ``device_wavelength = set_wavelength*scale + shift``
        """
        return self.wshift,self.wscale
    def set_wavelength_correction(self, shift=0., scale=1.):
        """
        Set the wavelength correction parameters.

        The relation between the set/get wavelength and the wavelength set to the device is calculated as
        ``device_wavelength = set_wavelength*scale + shift``
        """
        self.wshift=shift
        self.wscale=scale
        
    def home(self):
        """Home the motor (needs to be called first after startup)"""
        return self.query("H",timeout=40.)
    
    def get_wavelength(self):
        """Get the currently set wavelength (or ``None`` if unknown / not homed)"""
        resp=self.query("W?")
        if resp[0].lower()=="unknown":
            return None
        return (float(resp[0])/1E9-self.wshift)/self.wscale
    def set_wavelength(self, wavelength):
        """Set the current wavelength"""
        self.query("W{:.2f}".format( (wavelength*self.wscale+self.wshift)*1E9 ))
        return self.get_wavelength()
    
    
    

class DD100(OZOpticsDevice):
    """
    OZOptics DD100 variable attenuator.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    def __init__(self, conn, timeout=20.):
        super().__init__(conn,timeout=timeout)
        self._add_settings_variable("attenuation",self.get_attenuation,self.set_attenuation)
        self._add_info_variable("max_attenuation",self.get_max_attenuation)
        self._add_info_variable("min_attenuation",self.get_min_attenuation)
    
    def home(self):
        """Home the motor (needs to be called first after startup)"""
        return self.query("H",timeout=40.)
    
    def get_min_attenuation(self):
        """Get the minimal possible attenuation (i.e., insertion loss)"""
        return float(self.query("CD",prefix="IL:"))
    def get_max_attenuation(self):
        """Get the maximal possible possible attenuation in dB"""
        return float(self.query("CD",prefix="MAX ATTEN:"))
    def get_attenuation(self):
        """Get the current attenuation in dB"""
        return float(self.query("D",prefix="ATTEN:"))
    def set_attenuation(self, att):
        """Set the current attenuation in dB"""
        try:
            self.query("A{:.2f}".format(att))
        except OZOpticsError:
            att=numerical.limit_to_range(att,self.get_min_attenuation(),self.get_max_attenuation())
            self.query("A{:.2f}".format(att))
        return self.get_attenuation()



class EPC04(comm_backend.ICommBackendWrapper):
    """
    OZOptics EPC04 polarization controller.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    Error=OZOpticsError
    _voltage_limits=(-5.,5.)
    _frequency_limits=(0,100)
    def __init__(self, conn, timeout=20.):
        instr=comm_backend.new_backend(conn,"serial",term_write="\r\n",timeout=timeout,datatype="str",defaults={"serial":("COM1",9600)},reraise_error=OZOpticsBackendError)
        super().__init__(instr)
        self._add_settings_variable("voltages",self.get_voltages,self.set_all_voltages)
        self._add_settings_variable("mode",self.get_mode,self.set_mode)
        self._add_settings_variable("frequencies",self.get_frequencies,self.set_all_frequencies)
        self._add_settings_variable("wavefrom",self.get_waveform,self.set_waveform)
    
    def _parse_response(self, comm, resp):
        resp=[s.strip() for s in resp.splitlines() if s.strip()]
        if resp and (resp[0]==comm):
            resp=resp[1:]
        if resp and (resp[-1].endswith("Error!")):
            raise OZOpticsError("Command {} returned error: {}".format(comm,resp))
        resp=resp[:-1]
        return resp
    def query(self, comm):
        comm=comm.strip()
        self.instr.flush_read()
        self.instr.write(comm)
        resp=self.instr.read_multichar_term(["Done\r\n","Error!\r\n"],remove_term=False)
        return self._parse_response(comm,resp)
    
    def get_voltages(self):
        """Get all voltages"""
        resp=self.query("V?")[0]
        Vs=re.findall(r"CH\d\s*([\d+-]+)",resp)
        if len(Vs)!=4:
            raise OZOpticsError("unexpected voltage query response: {}".format(resp))
        return [float(V)/1E3 for V in Vs]
    def set_voltage(self, channel, voltage):
        """Set voltage at a given channel (0 through 3)"""
        voltage=numerical.limit_to_range(voltage,*self._voltage_limits)
        self.query("V{:d},{:04d}".format(channel+1,int(voltage*1E3)))
        return self.get_voltages()[channel]
    def set_all_voltages(self, voltages):
        """
        Set all channel voltages.

        `voltages` is a list of size 4 containing the voltage values.
        """
        for ch,v in enumerate(voltages):
            self.set_voltage(ch,v)
        return self.get_voltages()
    def step_voltage(self, channel, step):
        """Step voltage at the given channel by the given step"""
        v=self.get_voltages()[channel]
        return self.set_voltage(channel,v+step)
    
    _p_operating_mode=interface.EnumParameterClass("operating_mode",["ac","dc"],value_case="upper")
    @interface.use_parameters(_returns="operating_mode")
    def get_mode(self):
        """
        Get current operating mode.

        Can be ``"dc"`` (constant voltage) or ``"ac"`` (scrambling).
        """
        resp=self.query("M?")[0]
        for p,v in [(" DC","dc"),(" AC","ac"),("DC","dc"),("AC","ac"),("dc","dc"),("ac","ac")]:
            if resp.find(p)>=0 or resp.lower().find(p)>=0:
                return v
        raise OZOpticsError("can't determine the operating mode: {}".format(resp))
    @interface.use_parameters(mode="operating_mode")
    def set_mode(self, mode="dc"):
        """
        Set current operating mode.

        Can be ``"dc"`` (constant voltage) or ``"ac"`` (scrambling).
        """
        self.query("M{}".format(mode))
        return self.get_mode()

    def get_frequencies(self):
        """Get all scrambling frequencies"""
        resp=self.query("F?")[0]
        fs=re.findall(r"CH\d\s*([\d+-]+)",resp)
        if len(fs)!=4:
            raise OZOpticsError("unexpected frequency query response: {}".format(resp))
        return [float(f) for f in fs]
    def set_frequency(self, channel, frequency):
        """Set scrambling frequency a given channel (0 through 3)"""
        frequency=numerical.limit_to_range(frequency,*self._frequency_limits)
        self.query("F{:d},{:04d}".format(channel+1,int(frequency)))
        return self.get_frequencies()[channel]
    def set_all_frequencies(self, frequencies):
        """
        Set all channel scrambling frequencies.

        `frequencies` is a list of size 4 containing the frequency values.
        """
        for ch,v in enumerate(frequencies):
            self.set_frequency(ch,v)
        return self.get_frequencies()

    _p_waveform=interface.EnumParameterClass("waveform",["sin","tri"],match_prefix=True)
    @interface.use_parameters(_returns="waveform")
    def get_waveform(self):
        """
        Get current scrambling waveform.

        Can be ``"sin"`` (sine wave) or ``"tri"`` (triangle wave).
        """
        resp=self.query("WF?")[0]
        return resp.split()[-1].lower()
    @interface.use_parameters
    def set_waveform(self, waveform):
        """
        Set current scrambling waveform.

        Can be ``"sin"`` (sine wave) or ``"tri"`` (triangle wave).
        """
        self.query("WF{}".format(1 if waveform=="sin" else 2))
        return self.get_waveform()
    
    def save_preset(self):
        """Save current state as a power-up preset"""
        self.query("SAVE")