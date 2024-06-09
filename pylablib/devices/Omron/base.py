from ...core.utils import funcargparse, py3
from ...core.devio import interface

from ..Modbus import GenericModbusRTUDevice, ModbusError

import struct
import collections
import time


TDeviceInfo=collections.namedtuple("TDeviceInfo",["model"])
class OmronE5xCController(GenericModbusRTUDevice):
    """
    Omron E5_C temperature controller.

    Args:
        conn: serial connection parameters for RS485 adapter (usually port, a tuple containing port and baudrate,
            or a tuple with full specification such as ``("COM1", 9600, 8, 'E', 1)``)
        daddr: default device Modbus address
    """
    def __init__(self, conn, daddr=1):
        super().__init__(conn,daddr=daddr,conn_defaults=("COM1",9600,8,"E",1))
        self.instr.set_timeout(1.)
        # self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("measurementi",self.get_measurementi)
        self._add_settings_variable("setpointi",self.get_setpointi,self.set_setpointi)

    def get_device_info(self):
        """Return device info as a tuple ``(model)``"""
        return py3.as_str(self.mb_get_device_id()[2:]).strip()
    
    _retry_n=5
    _retry_wait=1.
    _reg_fmts={("int",2):">h",("int",4):">i",("uint",2):">H",("uint",4):">I"}
    def get_reg(self, address, kind="int", nbytes=2):
        """
        Get value of a register at the given address.
        
        `kind` is a register kind and can be ``"int"`` (signed integer) or ``"uint"`` (unsigned integer).
        `nbytes` is the size of the register and can be 2 or 4.
        """
        funcargparse.check_parameter_range(kind,"kind",["int","uint"])
        funcargparse.check_parameter_range(nbytes,"nbytes",[2,4])
        for i in range(self._retry_n):
            try:
                return struct.unpack(self._reg_fmts[kind,nbytes],self.mb_read_holding_registers(address,nbytes//2))[0]
            except ModbusError as err:
                if i==self._retry_n-1:
                    raise
                print("retry {} error {}".format(i,err))
                time.sleep(self._retry_wait)
    def set_reg(self, address, value):
        """Set value of an integer register at the given address"""
        self.mb_write_single_holding_register(address,int(value))
        return self.get_reg(address,"int")
    
    def get_measurementi(self):
        """
        Return measurement value as an integer number
        
        The result is returned in the current display units.
        For temperature units (C and F) this value is degrees, while for the physical units (A, V) this relation is determined by the decimal point position.
        """
        return self.get_reg(0x2000)
    def get_setpointi(self):
        """
        Get setpoint value as an integer point number.
        
        The result is returned in the current display units.
        """
        return self.get_reg(0x2103)
    @interface.use_parameters(setpoint="setpoint_kind")
    def set_setpointi(self, value):
        """
        Get setpoint value as an integer point number.
        
        The value is specified and the result is returned in the current display units.
        """
        return self.set_reg(0x2103,value)