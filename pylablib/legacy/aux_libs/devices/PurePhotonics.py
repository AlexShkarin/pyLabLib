from builtins import range

from ...core.devio import SCPI, units  #@UnresolvedImport
from ...core.utils import numerical,general,funcargparse  #@UnresolvedImport

_depends_local=["...core.devio.SCPI"]


class CBDX1(SCPI.SCPIDevice):
    """
    CBDX1 controller for the PurePhotonics PPCL200 laser.
    """
    def __init__(self, addr, read_echo=True, comm_delay=.5, mode_wait_time=5., offset_wait_time=5., connect_on_operation=True):
        backend_params={"connect_on_operation":connect_on_operation}
        SCPI.SCPIDevice.__init__(self,(addr,115200),backend="serial",backend_params=backend_params)
        self.instr.set_timeout(6.)
        self.instr.term_read=[";","\r","\n"]
        self.max_wavelength_step=50E-12
        self.power_range=(4E-3,63E-3)
        self._ask_delay=comm_delay
        self._set_delay=comm_delay
        self._wait_poll_period=comm_delay*2
        self._read_echo_delay=comm_delay
        self._mode_wait_time=mode_wait_time
        self._offset_wait_time=offset_wait_time
        self._read_echo=read_echo
        self._add_settings_node("power_on",self.get_output,None)
        self._add_settings_node("power",self.get_output_level,self.set_output_level)
        self._add_settings_node("wavelength",self.get_wavelength,self.set_wavelength)
        self._add_settings_node("offset",self.get_offset,self.set_offset)
        self._add_settings_node("offset_wavelength",self.get_offset_wavelength,None)
        self._add_settings_node("mode",self.get_mode,self.set_mode)
        self.initialize()
    
    
    def initialize(self):
        with self.instr.single_op():
            self.write("pass coherent",read_echo=True,read_echo_delay=self._read_echo_delay)
            self.flush()
        
    def reset_output(self):
        with self.instr.single_op():
            mode=self.get_mode()
            on=self.get_output()
            self._set_output_raw(False,wait=True)
            self.set_mode("standard",wait=True)
            self._set_output_raw(on,wait=True)
            self.set_mode(mode,wait=True)
    def ensure_output(self):        
        with self.instr.single_op():
            on=self.get_output()
            if not on:
                self._set_output_raw(True,wait=True)
            mode=self.get_mode()
            if mode!="whisper":
                self.set_mode("whisper",wait=True)
        
    def write_register(self, addr, value):
        value=int(value)
        value=min((2<<15)-1,max(-(2<<15),value))
        command="byp 1,1,1,1,{:02x},{:02x},{:02x}".format(int(addr)&0xFF,(value>>8)&0xFF,value&0xFF)
        with self.instr.single_op():
            self.write(command,read_echo=True,read_echo_delay=self._read_echo_delay)
            self.flush()
    def read_register(self, addr):
        command="byp 1,1,1,0,{:02x},0,0".format(addr&0xFF)
        with self.instr.single_op():
            resp=self.ask(command,delay=self._ask_delay,read_echo=self._read_echo)
        reg=[int(d.strip(),base=16) for d in resp.split(",")[2:]]
        return reg[0]*(1<<8)+reg[1]
    
    def is_busy(self):
        with self.instr.single_op():
            return self.ask("BUSY?","bool",delay=self._ask_delay,read_echo=self._read_echo)
    def wait_sync(self, timeout=None):
        timeout=self._wait_sync_timeout if timeout is None else timeout
        countdown=general.Countdown(timeout)
        while True:
            if not self.is_busy():
                return True
            if countdown.passed():
                return False
            self.sleep(self._wait_poll_period)
            
    def get_mode(self):
        mode=self.read_register(0x90)
        if mode==0:
            return "standard"
        elif mode==1:
            return "no_dither"
        elif mode==2:
            return "whisper"
        else:
            raise self.instr.Error("can't recognize mode {} returned py the device".format(mode))
    _modes={"standard":0,"no_dither":1,"whisper":2}
    def set_mode(self, mode, wait=True):
        funcargparse.check_parameter_range(mode,"mode",self._modes)
        self.write_register(0x90,self._modes[mode])
        if wait:
            self.sleep(self._set_delay)
            self.wait_sync()
    
    def _check_mode(self):
        mode=self.get_mode()
        if mode!="standard":
            self.set_mode("standard")
            self.sleep(self._mode_wait_time/2.)
        return mode
    
    def get_output(self):
        return bool(self.read_register(0x32)&0x08)
    def _set_output_raw(self, enabled=True, wait=True):
        self.write_register(0x32,8 if enabled else 0)
        if wait:
            self.sleep(self._set_delay)
            self.wait_sync()
    def set_output(self, enabled=True, wait=True):
        if enabled and wait:
            mode=self.get_mode()
            self.set_mode("standard",wait=True)
            self._set_output_raw(enabled=enabled,wait=wait)
            self.set_mode(mode,wait=True)
        else:
            self._set_output_raw(enabled=enabled,wait=wait)
        return self.get_output()
    def get_output_level(self):
        with self.instr.single_op():
            value,unit=self.ask("POWER?","value",delay=self._ask_delay,read_echo=self._read_echo)
        return units.convert_power_units(value,unit or "dBm","W",case_sensitive=False)
    def set_output_level(self, level, wait=True, check_mode=True):
        wait=wait or check_mode
        if level is None:
            self._set_output_raw(False,wait=wait)
            return None
        else:
            with self.instr.single_op():
                if check_mode:
                    is_on=self.get_output()
                    mode=self._check_mode()
                level=numerical.limit_to_range(level,*self.power_range)
                level=units.convert_power_units(level,"W","dBm")
                self.write("POWER",level,"float",read_echo=True,read_echo_delay=self._read_echo_delay)
                self.flush()
                if wait:
                    self.sleep(self._set_delay)
                    self.wait_sync()
                if check_mode and (mode!="standard"):
                    self.set_mode(mode)
                    self.sleep(self._mode_wait_time)
                    if is_on:
                        self.ensure_output()
                return self.get_output_level()
    
    def get_wavelength(self):
        with self.instr.single_op():
            value,unit=self.ask("WAVELENGTH?","value",delay=self._ask_delay,read_echo=self._read_echo)
        return units.convert_length_units(value,unit or "nm","m",case_sensitive=False)
    def set_wavelength(self, wavelength, wait=True, check_mode=True):
        wait=wait or check_mode
        with self.instr.single_op():
            wavelength=units.convert_length_units(wavelength,"m","nm")    
            if check_mode:
                mode=self._check_mode()
            self.write("WAVELENGTH",wavelength,"float",read_echo=True,read_echo_delay=self._read_echo_delay)
            self.flush()
            if wait:
                self.sleep(self._set_delay)
                self.wait_sync()
            if check_mode and (mode!="standard"):
                self.set_mode(mode)
                self.sleep(self._mode_wait_time)
                self.ensure_output()
            return self.get_wavelength()
        
    def get_offset(self):
        with self.instr.single_op():
            value,unit=self.ask("OFFSET?","value",delay=self._ask_delay,read_echo=self._read_echo)
        return units.convert_frequency_units(value,unit or "GHz","Hz",case_sensitive=True)
    def set_offset(self, offset, wait=True):
        with self.instr.single_op():
            offset=units.convert_frequency_units(offset,"Hz","MHz")
            if wait:
                self.sleep(self._set_delay)
                self.wait_sync()
            self.write_register(0x62,offset)
            if wait:
                self.sleep(self._set_delay)
                self.wait_sync()
                self.sleep(self._offset_wait_time)
            return self.get_offset()
        
    def step_wavelength(self, step):
        if abs(step)<=self.max_wavelength_step:
            return self.set_wavelength(self.get_wavelength()+step)
        else:
            return self.get_wavelength()
    def sweep_wavelength(self, start, step_size, steps_number, delay):
        self.set_wavelength(start)
        for _ in range(steps_number):
            self.sleep(delay)
            self.step_wavelength(step_size)
        return self.get_wavelength()
    def cycle_wavelength(self, step):
        self.step_wavelength(step)
        return self.step_wavelength(-step)
    
    def step_offset(self, step):
        return self.set_offset(self.get_offset()+step)
        
    def get_offset_wavelength(self):
        with self.instr.single_op():
            wavelength=self.get_wavelength()
            freq=3E8/wavelength
            offset=self.get_offset()
            return 3E8/(freq+offset)
        
    def apply_settings(self, settings):
        if "power_on" in settings and not settings["power_on"]:
            self.set_output(False)
        SCPI.SCPIDevice.apply_settings(self,settings)
        if "power_on" in settings and settings["power_on"]:
            self.set_output(True)
        return self.get_settings()
