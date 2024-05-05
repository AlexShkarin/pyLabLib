from ...core.devio import comm_backend, interface

from .base import HubnerError, HubnerBackendError

import collections

TDeviceInfo=collections.namedtuple("TDeviceInfo",["serial","model","name","firmware_version","firmware_date","firmware_build_date"])
class Cobolt(comm_backend.ICommBackendWrapper):
    """
    Hubner Cobolt MLD/DPL lasers.

    Args:
        conn: serial connection parameters (usually port)
    """
    Error=HubnerError
    def __init__(self, conn):
        instr=comm_backend.new_backend(conn,"serial",term_read="\r\n",term_write="\r\n",datatype="str",defaults={"serial":("COM1",115200)},reraise_error=HubnerBackendError)
        super().__init__(instr)
        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("temperature_baseplate",self.get_baseplate_temperature,ignore_error=(HubnerError,))
        self._add_status_variable("temperature_head",self.get_head_temperature,ignore_error=(HubnerError,))
        self._add_status_variable("error_state",self.get_error_state)
        self._add_status_variable("operating_mode",self.get_operating_mode,ignore_error=(HubnerError,))
        self._add_status_variable("interlock",self.get_interlock,ignore_error=(HubnerError,))
        self._add_status_variable("key_switch",self.get_key_switch,ignore_error=(HubnerError,))
        self._add_status_variable("output_power",self.get_output_power,ignore_error=(HubnerError,))
        self._add_settings_variable("output_power",self.get_output_power_setpoint,lambda v: self.set_output_power(v,set_mode=False),ignore_error=(HubnerError,))
        self._add_info_variable("max_output_power",self.get_max_output_power,ignore_error=(HubnerError,))
        self._add_status_variable("output_current",self.get_output_current,ignore_error=(HubnerError,))
        self._add_settings_variable("output_current",self.get_output_current_setpoint,lambda v: self.set_output_current(v,set_mode=False),ignore_error=(HubnerError,))
        self._add_info_variable("max_output_current",self.get_max_output_current,ignore_error=(HubnerError,))
        self._add_settings_variable("analog_modulation",self.is_analog_modulation_enabled,self.enable_analog_modulation,ignore_error=(HubnerError,))
        self._add_settings_variable("digital_modulation",self.is_digital_modulation_enabled,self.enable_digital_modulation,ignore_error=(HubnerError,))
        self._add_settings_variable("modulation_power",self.get_modulation_power_setpoint,self.set_modulation_power,ignore_error=(HubnerError,))
        self._add_settings_variable("analog_modulation_impedance",self.get_analog_modulation_impedance,self.set_analog_modulation_impedance,ignore_error=(HubnerError,))
        self._add_settings_variable("enabled",self.is_enabled,self.enable)
    
    def query(self, comm, data_type="string", **kwargs):
        """Send a query to the device and parse the reply"""
        try:
            result=self.instr.ask(comm)
        except HubnerBackendError:
            if "default" in kwargs:
                return kwargs["default"]
            raise
        if result.lower().startswith("syntax error"):
            raise HubnerError(result)
        if data_type=="string":
            return result
        if data_type=="int":
            return int(result)
        if data_type=="float":
            return float(result)
        if data_type=="bool":
            return bool(int(result))
        raise ValueError("unrecognized data type: {}".format(data_type))

    def get_device_info(self):
        """Get device information (serial number)"""
        serial=self.query("gsn?")
        model=self.query("glm?")
        name=self.query("gcn?")
        firmware_version=self.query("gfv?")
        firmware_date=self.query("gfd?")
        firmware_build_date=self.query("gfbd?")
        return TDeviceInfo(serial,model,name,firmware_version,firmware_date,firmware_build_date)
    def get_work_hours(self):
        """Return device operation hours"""
        return self.query("hrs?","float")
    def get_baseplate_temperature(self):
        """Return device base plate temperature (in C)"""
        return self.query("rbpt?","float")
    def get_head_temperature(self):
        """Return device head (TEC) temperature (in C)"""
        return self.query("rtect?","float",default=None)
    
    def abort_autostart(self):
        """Abort autostart sequence"""
        return self.query("abort")
    def restart_autostart(self):
        """Restart autostart sequence"""
        return self.query("restart")
    def is_autostart_enabled(self):
        """Return whether the autostart sequence is enabled"""
        return self.query("@cobas?","bool")
    
    _p_error_state=interface.EnumParameterClass("error_state",{"none":0,"temperature_error":1,"interlock_error":3,"constant_power_timeout":4},allowed_value="all")
    @interface.use_parameters(_returns="error_state")
    def get_error_state(self):
        """Return the current error (fault) state"""
        return self.query("f?","int")
    def clear_error(self):
        """Clear the error state"""
        self.query("cf")
        return self.get_error_state()
    _p_operating_mode=interface.EnumParameterClass("operating_mode",{"off":0,"wait_key":1,"continuous":2,"on_off_mod":3,"mod":4,"fault":5,"abort":6},allowed_value="all")
    @interface.use_parameters(_returns="operating_mode")
    def get_operating_mode(self):
        """Return the operating mode"""
        return self.query("gom?","int")
    
    def enable(self, enabled=True, autostart="auto"):
        """
        Enable or disable the output.
        
        `autostart` determines whether the autostart-enabled command is used or not (if ``"auto"``, try both and ignore the errors).
        Note that if ``enabled==True``, this command does not usually turn on the laser, and requires the key switch to be turned off and back on.
        """
        comms=("l1","@cob1") if enabled else ("l0","@cob0")
        if autostart=="auto":
            try:
                return self.query(comms[1])
            except HubnerError:
                return self.query(comms[0])
        return self.query(comms[1] if autostart else comms[0])
    def is_enabled(self):
        """Check if the output is on"""
        return self.query("l?","bool")
    
    def get_key_switch(self):
        """Get the key switch state (``True`` is on, ``False`` is off)"""
        return self.query("@cobasks?","bool")
    def get_interlock(self):
        """Get the interlock state (``True`` is closed, ``False`` is open/fault)"""
        return not self.query("ilk?","bool")
    
    _p_output_mode=interface.EnumParameterClass("output_mode",["cpower","ccurrent","mod"])
    @interface.use_parameters(mode="output_mode")
    def set_output_mode(self, mode):
        """Set output mode (`"ccurrent"`` for constant current, ``"cpower"`` for constant power, ``"mod"`` for modulation)"""
        self.query({"cpower":"cp","ccurrent":"ci","mod":"em"}[mode])
        return self.get_output_mode()
    def get_output_mode(self):
        """
        Get output mode (`"ccurrent"`` for constant current, ``"cpower"`` for constant power, ``"mod"`` for modulation)
        
        Can also return ``None`` if the mode can not be queried.
        """
        vals=self.query("ra?",default="").split()
        if len(vals)>7 and vals[7].isdigit():
            om=int(vals[7])
            if om==0:
                return "ccurrent"
            if om==1:
                return "cpower"
            if om==2:
                return "mod"
        return None
    def get_output_power_setpoint(self):
        """Get output power setpoint (in W) in the constant power mode"""
        return self.query("p?","float")
    def set_output_power(self, setpoint, set_mode=True):
        """
        Set output power setpoint (in W).
        
        If ``set_mode==True``, switch the device to the constant power mode.
        """
        self.query("p {}".format(float(setpoint)))
        if set_mode:
            self.set_output_mode("cpower")
    def get_max_output_power(self):
        """Get the maximal output power"""
        return self.query("gmlp?","float",default=None)/1E3
    def get_output_current_setpoint(self):
        """Get output current setpoint (in A) in the constant current mode"""
        return self.query("glc?","float")
    def set_output_current(self, setpoint, set_mode=True):
        """
        Set output current setpoint (in A).
        
        If ``set_mode==True``, switch the device to the constant current mode.
        """
        self.query("slc {}".format(float(setpoint)))
        if set_mode:
            self.set_output_mode("ccurrent")
    def get_max_output_current(self):
        """Get the maximal output current"""
        return self.query("gmlc?","float",default=None)/1E3
    def get_output_power(self):
        """Get actual current output power (in W)"""
        return self.query("pa?","float")
    def get_output_current(self):
        """Get actual current drive current (in A)"""
        return self.query("rlc?","float")
    
    def is_analog_modulation_enabled(self):
        """Check if the analog modulation is enabled"""
        return self.query("games?","bool")
    def enable_analog_modulation(self, enabled=True):
        """Enable or disable the analog modulations"""
        self.query("sames {}".format(1 if enabled else 0))
        return self.is_analog_modulation_enabled()
    def is_digital_modulation_enabled(self):
        """Check if the digital modulation is enabled"""
        return self.query("gdmes?","bool")
    def enable_digital_modulation(self, enabled=True):
        """Enable or disable the digital modulations"""
        self.query("sdmes {}".format(1 if enabled else 0))
        return self.is_digital_modulation_enabled()
    
    def get_modulation_power_setpoint(self):
        """Get power setpoint (in W) in the modulation mode"""
        return self.query("glmp?","float")/1E3
    def set_modulation_power(self, setpoint):
        """Set power setpoint (in W) in the modulation mode"""
        self.query("slmp? {}".format(float(setpoint)*1E3))
        return self.get_modulation_power_setpoint()
    
    _p_analog_modulation_impedance=interface.EnumParameterClass("analog_modulation_impedance",{"highZ":0,"50ohm":1})
    @interface.use_parameters(_returns="analog_modulation_impedance")
    def get_analog_modulation_impedance(self):
        """Get analog modulation input impedance (``"50ohm"`` or ``"highZ"``)"""
        return self.query("galis?","int")
    @interface.use_parameters(impedance="analog_modulation_impedance")
    def set_analog_modulation_impedance(self, impedance):
        """Set analog modulation input impedance (``"50ohm"`` or ``"highZ"``)"""
        return self.query("salis? {}".format(impedance))