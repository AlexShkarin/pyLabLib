from ...core.devio import backend  #@UnresolvedImport
from ...core.utils import numerical, funcargparse  #@UnresolvedImport

import re

_depends_local=["...core.devio.backend"]


class OZOpticsDevice(backend.IBackendWrapper):
    """
    Generic OZOptics device.
    """
    def __init__(self, port_addr, timeout=20.):
        instr=backend.SerialDeviceBackend((port_addr,9600),timeout=timeout,term_write="\r\n",connect_on_operation=True,datatype="str")
        backend.IBackendWrapper.__init__(self,instr)
    
    def _parse_response(self, comm, resp):
        resp=[s.strip() for s in resp.splitlines() if s.strip()]
        if resp and (resp[0]==comm):
            resp=resp[1:]
        if resp and (resp[0].startswith("Error")):
            raise RuntimeError("Command {} returned error: {}".format(comm,resp))
        return resp
    def _get_prepended_response(self, query, prefix, line=0):
        resp=self.query(query)
        ln=resp[line].upper()
        if ln.startswith(prefix.upper()):
            return ln[len(prefix):].strip()
        else:
            raise ValueError("unexpected reply: {}".format(resp))
    def query(self, comm, timeout=None):
        comm=comm.strip()
        with self.instr.single_op():
            self.instr.flush_read()
            self.instr.write(comm)
            resp=self.instr.read_multichar_term("Done\r\n",timeout=timeout)
            self.instr.flush_read()
        return self._parse_response(comm,resp)
    
    def restart(self):
        return self.query("RST",timeout=40.)
    def get_config(self):
        return self.query("CD")
    
    

class TF100(OZOpticsDevice):
    """
    OZOptics TF100 tunable filter.
    """
    def __init__(self, port_addr, timeout=20.):
        OZOpticsDevice.__init__(self,port_addr,timeout)
        self._add_settings_node("wavelength",self.get_wavelength,self.set_wavelength)
        self._add_settings_node("wavelength_correction",self.get_wavelength_correction, self.set_wavelength_correction)
        self.wshift=0.
        self.wscale=1.
        self.set_wavelength_correction(24.75E-9,0.984643) # experimentally measured; redefine for different devices
    
    # wavelength_device = wavelength_real*scale+shift
    def get_wavelength_correction(self):
        return self.wshift, self.wscale
    def set_wavelength_correction(self, shift=0., scale=1.):
        self.wshift=shift
        self.wscale=scale
        
    def home(self):
        return self.query("H",timeout=40.)
    
    def get_wavelength(self):
        resp=self.query("W?")
        if resp[0]=="Unknown":
            return None
        return (float(resp[0])/1E9-self.wshift)/self.wscale
    def set_wavelength(self, wavelength):
        self.query("W{:.2f}".format( (wavelength*self.wscale+self.wshift)*1E9 ))
        return self.get_wavelength()
    
    
    

class DD100(OZOpticsDevice):
    """
    OZOptics DD100 variable attenuator.
    """
    def __init__(self, port_addr, timeout=20.):
        OZOpticsDevice.__init__(self,port_addr,timeout)
        self._add_settings_node("attenuation",self.get_attenuation,self.set_attenuation)
        self._add_full_info_node("max_attenuation",self.get_max_attenuation)
        self._add_full_info_node("min_attenuation",self.get_min_attenuation)
    
    def home(self):
        return self.query("H",timeout=40.)
    
    def get_min_attenuation(self):
        return float(self._get_prepended_response("CD","IL:",9))
    def get_max_attenuation(self):
        return float(self._get_prepended_response("CD","MAX ATTEN:",3))
    def get_attenuation(self):
        return float(self._get_prepended_response("D","ATTEN:",1))
    def set_attenuation(self, att_dB):
        try:
            self.query("A{:.2f}".format(att_dB))
        except RuntimeError:
            att_dB=numerical.limit_to_range(att_dB,self.get_min_attenuation(),self.get_max_attenuation())
            self.query("A{:.2f}".format(att_dB))
        return self.get_attenuation()
    
    
    
    
    

class EPC04(backend.IBackendWrapper):
    """
    OZOptics EPC04 polarization controller.
    """
    def __init__(self, port_addr, timeout=20.):
        instr=backend.SerialDeviceBackend((port_addr,9600),timeout=timeout,term_write="\r\n",connect_on_operation=True)
        backend.IBackendWrapper.__init__(self,instr)
        self._add_settings_node("voltages",self.get_voltages,self.set_all_voltages)
        self._add_settings_node("mode",self.get_mode,self.set_mode)
        self._voltage_limts=(-5.,5.)
    
    def _parse_response(self, comm, resp):
        resp=[s.strip() for s in resp.splitlines() if s.strip()]
        if resp and (resp[0]==comm):
            resp=resp[1:]
        if resp and (resp[-1].endswith("Error!")):
            raise RuntimeError("Command {} returned error: {}".format(comm,resp))
        resp=resp[:-1]
        return resp
    def query(self, comm):
        comm=comm.strip()
        with self.instr.single_op():
            self.instr.flush_read()
            self.instr.write(comm)
            resp=self.instr.read_multichar_term(["Done\r\n","Error!\r\n"],remove_term=False)
            self.instr.flush_read()
        return self._parse_response(comm,resp)
    
    def get_voltages(self):
        resp=self.query("V?")[0]
        Vs=re.findall(r"CH\d\s*([\d+-]+)",resp)
        if len(Vs)!=4:
            raise RuntimeError("unexpected voltage query response: {}".format(resp))
        return [float(V)/1E3 for V in Vs]
    def set_voltage(self, channel, value):
        value=numerical.limit_to_range(value,*self._voltage_limts)
        self.query("V{:d},{:04d}".format(channel+1,int(value*1E3)))
        return self.get_voltages()[channel]
    def set_all_voltages(self, value):
        for ch,v in enumerate(value):
            self.set_voltage(ch,v)
        return self.get_voltages()
    def step_voltage(self, channel, step):
        v=self.get_voltages()[channel]
        return self.set_voltage(channel,v+step)
    
    def get_mode(self):
        resp=self.query("M?")[0]
        return resp[-2:]
    def set_mode(self, mode="DC"):
        funcargparse.check_parameter_range(mode,"mode",{"AC","DC"})
        if mode=="AC":
            self.query("MAC")
        else:
            self.query("MDC")
        return self.get_mode()
    
    def save_preset(self):
        self.query("SAVE")