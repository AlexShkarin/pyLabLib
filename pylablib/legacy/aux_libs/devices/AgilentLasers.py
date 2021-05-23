from __future__ import print_function
from builtins import range

from ...core.devio import SCPI, units  #@UnresolvedImport

_depends_local=["...core.devio.SCPI"]


class HP8168F(SCPI.SCPIDevice):
    """
    HP8168F tunable laser.
    """
    _allow_concatenate_write=False
    def __init__(self, addr):
        SCPI.SCPIDevice.__init__(self,addr)
        self.max_wavelength_step=100E-12
        self._add_settings_node("power_on",self.get_output,None)
        self._add_settings_node("power",self.get_output_level,self.set_output_level)
        self._add_settings_node("wavelength",self.get_wavelength,self.set_wavelength)
    
    def get_output(self):
        return self.ask(":OUTPUT:STATE?","bool")
    def set_output(self, enabled=True, force=False):
        if not force:
            if self.get_output()==enabled:
                return enabled
        self.write(":OUTPUT:STATE",enabled)
        return self.get_output()
    def get_output_level(self):
        value,unit=self.ask(":SOURCE:POWER:LEVEL:IMM:AMP?","value")
        return units.convert_power_units(value,unit or "W","W",case_sensitive=False)
    def set_output_level(self, level, force=False):
        if level is None:
            self.set_output(False,force=force)
            return None
        else:
            if not force:
                result=self.get_output_level()
                if abs(result-level)<1E-6:
                    return result
            self.write(":SOURCE:POWER:LEVEL:IMM:AMP",level,"float",unit="W")
            return self.get_output_level()
    
    def get_wavelength(self):
        value,unit=self.ask(":SOURCE:WAVELENGTH?","value")
        return units.convert_length_units(value,unit or "m","m",case_sensitive=False)
    def set_wavelength(self, wavelength, force=False):
        if not force:
            result=self.get_wavelength()
            if abs(result-wavelength)<0.5E-12:
                return result
        self.write(":SOURCE:WAVELENGTH",wavelength,"float",unit="M")
        result=self.get_wavelength()
        if abs(result-wavelength)>0.5E-12:
            raise ValueError("can't set wavelength {}; the device is set at {}".format(wavelength,result))
        return result
    def step_wavelength(self, step):
        if abs(step)<=self.max_wavelength_step:
            return self.set_wavelength(self.get_wavelength()+step)
        else:
            return self.get_wavelength()
    def sweep_wavelength(self, start, step_size, steps_number, delay, print_period=None):
        self.set_wavelength(start)
        for n in range(steps_number):
            self.sleep(delay)
            wl=self.step_wavelength(step_size)
            if print_period is not None and (n+1)%print_period==0:
                print("Wavelength is {:.3f}nm".format(wl*1E9))
        return self.get_wavelength()
    def cycle_wavelength(self, step):
        self.step_wavelength(step)
        return self.step_wavelength(-step)
        
        
    def apply_settings(self, settings):
        if "power_on" in settings and not settings["power_on"]:
            self.set_output(False)
        SCPI.SCPIDevice.apply_settings(self,settings)
        if "power_on" in settings and settings["power_on"]:
            self.set_output(True)
        return self.get_settings()