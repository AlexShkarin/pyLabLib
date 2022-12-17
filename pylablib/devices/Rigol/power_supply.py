from ...core.devio import SCPI, interface
from .base import GenericRigolError, GenericRigolBackendError


class DP1116A(SCPI.SCPIDevice):
    """
    Rigol DP1116A DC power supply.

    Args:
        addr: device address (usually a VISA name).
    """
    Error=GenericRigolError
    ReraiseError=GenericRigolBackendError
    def __init__(self, addr):
        super().__init__(addr)
        with self._close_on_error():
            self.get_id()
        self._add_scpi_parameter("output_range","OUTP:RANG",kind="param",parameter="output_range")
        self._add_scpi_parameter("output_enabled","OUTP:STATE",kind="bool")
        self._add_scpi_parameter("ovp_enabled","OUTP:OVP:STATE",kind="bool")
        self._add_scpi_parameter("ovp_threshold","OUTP:OVP")
        self._add_scpi_parameter("ocp_enabled","OUTP:OCP:STATE",kind="bool")
        self._add_scpi_parameter("ocp_threshold","OUTP:OCP")
        self._add_scpi_parameter("voltage_setpoint","SOURCE:VOLT")
        self._add_scpi_parameter("current_setpoint","SOURCE:CURR")
        self._add_scpi_parameter("voltage","MEAS:VOLT")
        self._add_scpi_parameter("current","MEAS:CURR")
        self._add_scpi_parameter("power","MEAS:POWER")
        
        self._add_settings_variable("enabled",self.is_output_enabled,self.enable_output)
        self._add_settings_variable("output_range",self.get_output_range,self.set_output_range)
        self._add_settings_variable("ovp_threshold",self.get_ovp_threshold,self.set_ovp_threshold)
        self._add_status_variable("ovp_enabled",self.is_ovp_enabled,self.enable_ovp)
        self._add_settings_variable("ocp_threshold",self.get_ocp_threshold,self.set_ocp_threshold)
        self._add_status_variable("ocp_enabled",self.is_ocp_enabled,self.enable_ocp)
        self._add_settings_variable("voltage_setpoint",self.get_voltage_setpoint,self.set_voltage)
        self._add_status_variable("voltage",self.get_voltage)
        self._add_settings_variable("current_setpoint",self.get_current_setpoint,self.set_current)
        self._add_status_variable("current",self.get_current)
        self._add_status_variable("power",self.get_power)

    _bool_selector=("OFF","ON")
    _float_fmt="{:.4f}"
    _p_output_range=interface.EnumParameterClass("output_range",{"16V":"16V","32V":"32V"})

    def is_output_enabled(self):
        """Check if the output is enabled"""
        return self._get_scpi_parameter("output_enabled")
    def enable_output(self, enable=True):
        """Enable or disable the output"""
        return self._set_scpi_parameter("output_enabled",enable,result=True)
    def get_output_range(self):
        """
        Get output range.

        Can be either ``"16V"`` (16V/10A) or ``"32V"`` (32V/5A).
        """
        return self._get_scpi_parameter("output_range")
    def set_output_range(self, value="16V"):
        """
        Set output range.

        Can be either ``"16V"`` (16V/10A) or ``"32V"`` (32V/5A).
        """
        return self._set_scpi_parameter("output_range",value,result=True)
    
    def get_voltage_setpoint(self):
        """Get output voltage setpoint"""
        return self._get_scpi_parameter("voltage_setpoint")
    def get_voltage(self):
        """Get the actual output voltage"""
        return self._get_scpi_parameter("voltage")
    def set_voltage(self, value):
        """Set output voltage setpoint"""
        return self._set_scpi_parameter("voltage",value,result=True)
    def get_current_setpoint(self):
        """Get output current setpoint"""
        return self._get_scpi_parameter("current_setpoint")
    def get_current(self):
        """Get the actual output current"""
        return self._get_scpi_parameter("current")
    def set_current(self, value):
        """Set output current setpoint"""
        return self._set_scpi_parameter("current",value,result=True)
    def get_power(self):
        """Get the actual output power"""
        return self._get_scpi_parameter("power")
    
    def get_ovp_threshold(self):
        """Get over-voltage protection threshold"""
        return self._get_scpi_parameter("ovp_threshold")
    def set_ovp_threshold(self, value):
        """Set over-voltage protection threshold"""
        return self._set_scpi_parameter("ovp_threshold",value,result=True)
    def is_ovp_enabled(self):
        """Check if the over-voltage protection is enabled"""
        return self._get_scpi_parameter("ovp_enabled")
    def enable_ovp(self, enable=True):
        """Enable or disable the over-voltage protection"""
        return self._set_scpi_parameter("ovp_enabled",enable,result=True)
    def get_ocp_threshold(self):
        """Get over-current protection threshold"""
        return self._get_scpi_parameter("ocp_threshold")
    def set_ocp_threshold(self, value):
        """Set over-current protection threshold"""
        return self._set_scpi_parameter("ocp_threshold",value,result=True)
    def is_ocp_enabled(self):
        """Check if the over-current protection is enabled"""
        return self._get_scpi_parameter("ocp_enabled")
    def enable_ocp(self, enable=True):
        """Enable or disable the over-current protection"""
        return self._set_scpi_parameter("ocp_enabled",enable,result=True)