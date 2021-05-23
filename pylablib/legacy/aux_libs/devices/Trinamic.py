from ...core.utils import strpack
from ...core.devio import backend, data_format

from builtins import bytes
import collections
import time

_depends_local=["...core.devio.backend"]

class TrinamicError(RuntimeError):
    """Generic Trinamic error."""

i4_conv=data_format.DataFormat.from_desc(">i4")
class TMCM1100(backend.IBackendWrapper):
    """
    Trinamic stepper motor controller.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    def __init__(self, conn):
        conn=backend.SerialDeviceBackend.combine_conn(conn,(None,9600))
        instr=backend.SerialDeviceBackend(conn,term_write="",term_read="",timeout=3.)
        backend.IBackendWrapper.__init__(self,instr)
        self._add_status_node("position",self.get_position)
        self._add_settings_node("speed",self.get_speed,self.set_speed)
        self._add_status_node("current_speed",self.get_current_speed)
        self._add_status_node("moving",self.is_moving)
        self.open()

    def open(self):
        backend.IBackendWrapper.open(self)
        self.instr.flush_read()
        self.instr._operation_cooldown=0.01
    
    @staticmethod
    def _build_command(comm, comm_type, value, bank=0, addr=0):
        val_str=i4_conv.convert_to_str(value)
        data_str=bytes(strpack.pack_uint(addr,1)+strpack.pack_uint(comm,1)+strpack.pack_uint(comm_type,1)+strpack.pack_uint(bank,1)+val_str)
        chksum=sum([b for b in data_str])%0x100
        return data_str+strpack.pack_uint(chksum,1)
    ReplyData=collections.namedtuple("ReplyData",["comm","status","value","addr","module"])
    @staticmethod
    def _parse_reply(reply, result_format="u4"):
        reply=bytes(reply)
        data_str=reply[:8]
        chksum=sum([b for b in data_str])%0x100
        if chksum!=reply[8]:
            raise TrinamicError("Communication error: incorrect checksum")
        addr=strpack.unpack_uint(reply[0:1])
        module=strpack.unpack_uint(reply[1:2])
        status=strpack.unpack_uint(reply[2:3])
        comm=strpack.unpack_uint(reply[3:4])
        if result_format=="str":
            value=reply[4:8]
        else:
            value=data_format.DataFormat.from_desc(">"+result_format).convert_from_str(reply[4:8])[-1]
        return TMCM1100.ReplyData(comm,status,value,addr,module)
    _status_codes={100:"Success", 101:"Command loaded", 1:"Wrong checksum", 2:"Invalid command", 3:"Wrong type", 4:"Invalid value", 5:"EEPROM locked", 6:"Command not available"}
    @classmethod
    def _check_status(cls, status):
        if status not in cls._status_codes:
            raise TrinamicError("unrecognized status: {}".format(status))
        if status<100:
            raise TrinamicError("error status: {} ({})".format(status,cls._status_codes[status]))
    def query(self, comm, comm_type, value, result_format="i4", bank=0, addr=0):
        """
        Send a query to the stage and return the reply.
        
        For details, see TMCM-1110 firmware manual.
        """
        command=self._build_command(comm,comm_type,value,bank=bank,addr=addr)
        self.instr.write(command)
        reply_str=self.instr.read(9)
        reply=self._parse_reply(reply_str,result_format=result_format)
        self._check_status(reply.status)
        return reply

    def get_axis_parameter(self, parameter, result_format="i4", addr=0):
        """Get a given axis parameter"""
        return self.query(6,parameter,0,result_format=result_format,addr=addr).value
    def set_axis_parameter(self, parameter, value, addr=0):
        """Set a given axis parameter (volatile; resets on power cycling)"""
        return self.query(5,parameter,value,addr=addr)
    def store_axis_parameter(self, parameter, value=None, addr=0):
        """Store a given axis parameter in EEPROM (by default, value is the current value)"""
        if value is not None:
            self.set_axis_parameter(parameter,value,addr=addr)
        return self.query(7,parameter,value,addr=addr)
    def get_global_parameter(self, parameter, result_format="i4", bank=0, addr=0):
        """Get a given global parameter"""
        return self.query(10,parameter,0,result_format=result_format,bank=bank,addr=addr).value
    def set_global_parameter(self, parameter, value, bank=0, addr=0):
        """Set a given global parameter"""
        return self.query(9,parameter,value,bank=bank,addr=addr)

    def move_to(self, position, addr=0):
        """Move to a given position"""
        return self.query(4,0,position,addr=addr)
    def move(self, steps=1, addr=0):
        """Move for a given number of steps"""
        return self.query(4,1,steps,addr=addr)
    def get_position(self, addr=0):
        """Get the current axis position"""
        return self.get_axis_parameter(1,addr=addr)
    def jog(self, direction, speed):
        """
        Jog in a given direction with a given speed.
        
        `direction` can be either ``"-"`` (negative) or ``"+"`` (positive).
        The motion continues until it is explicitly stopped, or until a limit is hit.
        """
        if not direction: # 0 or False also mean left
            direction="-"
        if direction in [1, True]:
            direction="+"
        if direction not in ["+","-"]:
            raise TrinamicError("unrecognized direction: {}".format(direction))
        return self.query(1 if direction=="+" else 2,0,speed)
    def stop(self, addr=0):
        """Stop motion"""
        return self.query(3,0,0,addr=addr)

    def get_speed(self, addr=0):
        """Get the speed setting"""
        return self.get_axis_parameter(4,addr=addr)
    def set_speed(self, speed, addr=0):
        """Set the speed setting"""
        return self.set_axis_parameter(4,speed,addr=addr)

    def get_current_speed(self, addr=0):
        """Get the current speed"""
        return self.get_axis_parameter(3,addr=addr)
    def is_moving(self, addr=0):
        """Check if the motor is moving"""
        return bool(self.get_current_speed(addr=addr))
    def wait_for_axis(self, addr=0):
        """Wait for the motor to stop moving"""
        while self.get_current_speed(addr=addr):
            time.sleep(0.02)