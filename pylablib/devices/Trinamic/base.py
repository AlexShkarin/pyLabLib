from ...core.devio import comm_backend, interface

from ..interface import stage

import collections
import time
import struct
import math

class TrinamicError(comm_backend.DeviceError):
    """Generic Trinamic error"""
class TrinamicBackendError(TrinamicError,comm_backend.DeviceBackendError):
    """Generic Trinamic backend communication error"""

class TMCM1110(comm_backend.ICommBackendWrapper,stage.IStage):
    """
    Trinamic stepper motor controller TMCM-1110 controlled using TMCL Firmware.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    Error=TrinamicError
    def __init__(self, conn):
        instr=comm_backend.new_backend(conn,"serial",term_read="",term_write="",timeout=3.,defaults={"serial":("COM1",9600)},reraise_error=TrinamicBackendError)
        super().__init__(instr)
        self._add_status_variable("position",self.get_position)
        self._add_settings_variable("velocity_parameters",self.get_velocity_parameters,self.setup_velocity)
        self._add_settings_variable("limit_switches_parameters",self.get_limit_switches_parameters,self.setup_limit_switches)
        self._add_status_variable("current_parameters",self.get_current_parameters)
        self._add_status_variable("velocity_factor",self.get_velocity_factor)
        self._add_status_variable("acceleration_factor",self.get_acceleration_factor)
        self._add_status_variable("microstep_resolution",self.get_microstep_resolution)
        self._add_status_variable("current_speed",self.get_current_speed)
        self._add_status_variable("moving",self.is_moving)
        self.open()

    def open(self):
        res=super().open()
        self.instr.flush_read()
        self.instr.setup_cooldown(write=0.01)
        return res
    
    @staticmethod
    def _build_command(comm, comm_type, value, bank=0, addr=0):
        data_str=struct.pack(">BBBBi",addr,comm,comm_type,bank,int(value))
        chksum=sum([b for b in data_str])%0x100
        return data_str+struct.pack("<B",chksum)
    ReplyData=collections.namedtuple("ReplyData",["comm","status","value","addr","module"])
    @staticmethod
    def _parse_reply(reply, result_format="i"):
        reply=bytes(reply)
        data_str=reply[:8]
        chksum=sum([b for b in data_str])%0x100
        if chksum!=reply[8]:
            raise TrinamicError("Communication error: incorrect checksum")
        addr,module,status,comm=struct.unpack("<BBBB",reply[:4])
        if result_format=="str":
            value=reply[4:8]
        else:
            value,=struct.unpack(">I" if result_format=="u" else ">i",reply[4:8])
        return TMCM1110.ReplyData(comm,status,value,addr,module)
    _status_codes={100:"Success", 101:"Command loaded", 1:"Wrong checksum", 2:"Invalid command", 3:"Wrong type", 4:"Invalid value", 5:"EEPROM locked", 6:"Command not available"}
    @classmethod
    def _check_status(cls, status):
        if status not in cls._status_codes:
            raise TrinamicError("unrecognized status: {}".format(status))
        if status<100:
            raise TrinamicError("error status: {} ({})".format(status,cls._status_codes[status]))
    def query(self, comm, comm_type, value, result_format="i", bank=0, addr=0):
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

    def get_axis_parameter(self, parameter, result_format="i", addr=0):
        """Get a given axis parameter"""
        return self.query(6,parameter,0,result_format=result_format,addr=addr).value
    def set_axis_parameter(self, parameter, value, addr=0):
        """Set a given axis parameter (volatile; resets on power cycling)"""
        self.query(5,parameter,value,addr=addr)
    def store_axis_parameter(self, parameter, value=None, addr=0):
        """Store a given axis parameter in EEPROM (by default, value is the current value)"""
        if value is not None:
            self.set_axis_parameter(parameter,value,addr=addr)
        self.query(7,parameter,value,addr=addr)
    def get_global_parameter(self, parameter, result_format="i", bank=0, addr=0):
        """Get a given global parameter"""
        return self.query(10,parameter,0,result_format=result_format,bank=bank,addr=addr).value
    def set_global_parameter(self, parameter, value, bank=0, addr=0):
        """Set a given global parameter"""
        self.query(9,parameter,value,bank=bank,addr=addr)
    
    def get_general_input(self, port=0, bank=0, addr=0):
        """
        Get value of an input at a given bank (0-2) and port.
        
        Bank 0 is digital input (7 ports), bank 1 is analog input (1 port, value from 0 to 2**16-1), bank 2 is digital output (8 ports).
        For port assignments, see TMCM-1110 firmware manual.
        """
        return self.query(15,port,bank=bank,value=0,addr=addr)
    def set_general_output(self, value, port=0, bank=2, addr=0):
        """
        Set value of a digital input at a given bank (only bank 2 is available) and port.
        
        For port assignments, see TMCM-1110 firmware manual.
        """
        self.query(14,port,bank=bank,value=1 if value else 0,addr=addr)

    def move_to(self, position, addr=0):
        """Move to a given position"""
        self.query(4,0,position,addr=addr)
    def move_by(self, steps=1, addr=0):
        """Move by a given number of steps"""
        self.query(4,1,steps,addr=addr)
    def get_position(self, addr=0):
        """Get the current axis position"""
        return self.get_axis_parameter(1,addr=addr)
    def set_position_reference(self, pos=0, addr=0):
        """Set the current axis position as a reference (the actual motor position stays the same)"""
        self.set_axis_parameter(1,pos,addr=addr)
        return self.get_position(addr=addr)
    @interface.use_parameters
    def jog(self, direction, speed=None, addr=0):
        """
        Jog in a given direction with a given speed.
        
        `direction` can be either ``"-"`` (negative, left) or ``"+"`` (positive, right).
        The motion continues until it is explicitly stopped, or until a limit is hit.
        If ``speed is None``, use the standard speed value.
        """
        if speed is None:
            speed=self.get_velocity_parameters(addr=addr)[0]
        self.query(1 if direction else 2,0,speed,addr=addr)
    def stop(self, addr=0):
        """Stop motion"""
        self.query(3,0,0,addr=addr)

    def get_microstep_resolution(self, addr=0):
        """Get the number of microsteps per full step (always a power of 2)"""
        return 2**self.get_axis_parameter(140,addr=addr)
    def set_microstep_resolution(self, resolution, addr=0):
        """Set the number of microsteps per full step (rounded to a nearest power of 2)"""
        lresolution=round(math.log2(resolution))
        self.set_axis_parameter(140,lresolution,addr=addr)
        return self.get_microstep_resolution(addr=addr)
    
    def get_current_parameters(self, addr=0):
        """
        Return diving current parameter ``(drive_current, standby_current)``.

        ``drive_current`` is the maximal drive current, which is given as a fraction of the maximal generated current current
        (which is either 1A or 2.8A depending on the hardware jumper).
        ``standby_current`` is given as a fraction of ``drive_current``.
        """
        return self.get_axis_parameter(6,addr=addr)/255., self.get_axis_parameter(7,addr=addr)/255.
    def setup_current(self, drive_current=None, standby_current=None, addr=0):
        """
        Set drive and standby currents.

        WARNING: too high of a setting might damage the motor.
        ``drive_current`` is the maximal drive current, which is given as a fraction of the maximal generated current current
        (which is either 1A or 2.8A depending on the hardware jumper).
        ``standby_current`` is given as a fraction of ``drive_current``.
        Any ``None`` parameters are left unchanged.
        """
        if drive_current is not None:
            drive_current=int(min(max(0,drive_current),1)*255)
        if standby_current is not None:
            standby_current=int(min(max(0,standby_current),1)*255)
        curr_standby_current=self.get_axis_parameter(7,addr=addr)
        if standby_current is not None and standby_current<curr_standby_current:
            self.set_axis_parameter(7,standby_current,addr=addr)
        if drive_current is not None:
            self.set_axis_parameter(6,drive_current,addr=addr)
        if standby_current is not None and standby_current>curr_standby_current:
            self.set_axis_parameter(7,standby_current,addr=addr)
        return self.get_current_parameters()

    def get_limit_switches_parameters(self, addr=0):
        """Return limit switch parameters ``(left_enable, right_enable)``"""
        return bool(self.get_axis_parameter(13,addr=addr)), bool(self.get_axis_parameter(12,addr=addr))
    def setup_limit_switches(self, left_enable=None, right_enable=None, addr=0):
        """Setup limit switch parameters"""
        if left_enable is not None:
            self.set_axis_parameter(13,1 if left_enable else 0,addr=addr)
        if right_enable is not None:
            self.set_axis_parameter(12,1 if right_enable else 0,addr=addr)
        return self.get_limit_switches_parameters(addr=addr)

    def get_velocity_parameters(self, addr=0):
        """
        Return velocity parameters ``(speed, accel, pulse_divisor, ramp_divisor)``.
        
        ``speed`` and ``accel`` denote, correspondingly, maximal (i.e., steady regime) moving speed and acceleration in *internal* units.
        ``pulse_divisor`` is the driver pulse divisor, which defines how internal velocity units translate into microsteps/s (see :meth:`get_velocity_factor`);
        can only be a power of 2, higher values mean slower motion.
        ``ramp_divisor`` is the driver ramp divisor, which, together with the pulse divisor,
        defines how internal acceleration units translate into microsteps/s^2 (see :meth:`get_acceleration_factor`);
        rounded to the nearest power of 2, higher values mean slower acceleration.
        """
        return self.get_axis_parameter(4,addr=addr),self.get_axis_parameter(5,addr=addr),2**self.get_axis_parameter(154,addr=addr),2**self.get_axis_parameter(153,addr=addr)
    def setup_velocity(self, speed=None, accel=None, pulse_divisor=None, ramp_divisor=None, addr=0):
        """
        Setup velocity parameters ``(speed, accel, pulse_divisor, ramp_divisor)``.
        
        ``speed`` and ``accel`` denote, correspondingly, maximal (i.e., steady regime) moving speed and acceleration in *internal* units.
        ``pulse_divisor`` is the driver pulse divisor, which defines how internal velocity units translate into microsteps/s (see :meth:`get_velocity_factor`);
        rounded to the nearest power of 2, higher values mean slower motion.
        ``ramp_divisor`` is the driver ramp divisor, which, together with the pulse divisor,
        defines how internal acceleration units translate into microsteps/s^2 (see :meth:`get_acceleration_factor`);
        rounded to the nearest power of 2, higher values mean slower acceleration.
        ``None`` values are left unchanged.
        """
        if speed is not None:
            self.set_axis_parameter(4,speed,addr=addr)
        if accel is not None:
            self.set_axis_parameter(5,accel,addr=addr)
        if pulse_divisor is not None:
            lpulse_divisor=round(math.log2(pulse_divisor))
            self.set_axis_parameter(154,lpulse_divisor,addr=addr)
        if ramp_divisor is not None:
            lramp_divisor=round(math.log2(ramp_divisor))
            self.set_axis_parameter(153,lramp_divisor,addr=addr)
        return self.get_velocity_parameters()

    def get_velocity_factor(self, addr=0):
        """Get the ratio between the real speed (in microsteps/s) and the internal units"""
        return 16E6/(2**self.get_axis_parameter(154,addr=addr)*2048*32)
    def get_acceleration_factor(self, addr=0):
        """Get the ratio between the real acceleration (in microsteps/s^2) and the internal units"""
        return 16E6**2/2**(self.get_axis_parameter(153,addr=addr)+self.get_axis_parameter(154,addr=addr)+29)

    def get_current_speed(self, addr=0):
        """Get the instantaneous speed in internal units"""
        return self.get_axis_parameter(3,addr=addr)
    def is_moving(self, addr=0):
        """Check if the motor is moving"""
        return bool(self.get_current_speed(addr=addr))
    def wait_move(self, addr=0):
        """Wait until motion is done"""
        while self.get_current_speed(addr=addr):
            time.sleep(0.01)