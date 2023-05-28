from ...core.utils import funcargparse, py3
from ...core.devio import interface

from ..Modbus import GenericModbusRTUDevice

import struct
import collections


TDeviceInfo=collections.namedtuple("TDeviceInfo",["model"])
class LumelRE72Controller(GenericModbusRTUDevice):
    """
    Lumel RE72 temperature controller.

    Args:
        conn: serial connection parameters for RS485 adapter (usually port, a tuple containing port and baudrate,
            or a tuple with full specification such as ``("COM1", 9600, 8, 'N', 1)``)
        daddr: default device Modbus address
    """
    def __init__(self, conn, daddr=1):
        super().__init__(conn,daddr=daddr)
        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("measurementf",self.get_measurementf)
        self._add_status_variable("measurementi",self.get_measurementi)
        self._add_status_variable("outputf",self.get_outputf)
        self._add_status_variable("setpointf",self.get_setpointf)
        self._add_settings_variable("setpointi",self.get_setpointi,self.set_setpointi)
        self._add_settings_variable("all_setpointi",lambda: tuple([self.get_setpointi(i+1) for i in range(4)]),lambda v: [self.set_setpointi(s,i+1) for i,s in enumerate(v)])

    def get_device_info(self):
        """Return device info as a tuple ``(model)``"""
        return py3.as_str(self.mb_get_device_id()[2:]).strip()
    
    def get_reg(self, address, kind="auto"):
        """
        Get value of a register at the given address.
        
        `kind` is a register kind and can be ``"int"`` (2-byte signed integer), ``"uint"`` (2-byte unsigned integer), ``"float"`` (4-byte float),
        or ``"auto"`` (either signed integer or float depending on the address).
        """
        if kind=="auto":
            kind="float" if address>=7000 else "int"
        funcargparse.check_parameter_range(kind,"kind",["int","uint","float"])
        if kind=="int":
            return struct.unpack(">h",self.mb_read_holding_registers(address,1))[0]
        if kind=="uint":
            return struct.unpack(">H",self.mb_read_holding_registers(address,1))[0]
        return struct.unpack(">f",self.mb_read_holding_registers(address,2))[0]
    def set_reg(self, address, value):
        """Set value of an integer register at the given address"""
        self.mb_write_single_holding_register(address,int(value))
        return self.get_reg(address,"int")
    
    _p_setpoint_kind=interface.EnumParameterClass("setpoint_kind",[None,1,2,3,4])
    def get_measurementf(self):
        """
        Return measurement value as a floating point number.
        
        The result is returned in the current display units.
        """
        return self.get_reg(7000)
    @interface.use_parameters(setpoint="setpoint_kind")
    def get_setpointf(self, setpoint=None):
        """
        Get setpoint value as a floating point number.
        
        The result is returned in the current display units.
        `setpoint` specifies the setpoint kind and can be ``None`` (current), 1, or 2.
        """
        return self.get_reg(7004 if setpoint is None else 7008+setpoint*2)
    _p_output_kind=interface.EnumParameterClass("output_kind",[1,2])
    @interface.use_parameters(output="output_kind")
    def get_outputf(self, output=1):
        """
        Get output value in percents.
        
        `output` specifies the output channel and can be 1 or 2.
        """
        return self.get_reg(7006 if output==1 else 7008)
    
    
    def get_measurementi(self):
        """
        Return measurement value as an integer number
        
        The result is returned in the current display units.
        For temperature units (C and F) this value is degrees multiplied by 10, while for the physical units (A, V) this relation is determined by the decimal point position.
        """
        return self.get_reg(4006)
    @interface.use_parameters(setpoint="setpoint_kind")
    def get_setpointi(self, setpoint=None):
        """
        Get setpoint value as an integer point number.
        
        The result is returned in the current display units.
        For temperature units (C and F) this value is degrees multiplied by 10, while for the physical units (A, V) this relation is determined by the decimal point position.
        `setpoint` specifies the setpoint kind and can be ``None`` (current), or an integer from 1 to 4.
        """
        return self.get_reg(4008 if setpoint is None else 4083+setpoint)
    @interface.use_parameters(setpoint="setpoint_kind")
    def set_setpointi(self, value, setpoint=None):
        """
        Get setpoint value as an integer point number.
        
        The result is returned in the current display units.
        For temperature units (C and F) this value is degrees multiplied by 10, while for the physical units (A, V) this relation is determined by the decimal point position.
        `setpoint` specifies the setpoint kind and can be ``None`` (current), or an integer from 1 to 4.
        """
        if setpoint is None:
            setpoint=self.get_reg(4042)+1
        return self.set_reg(4083+setpoint,value)