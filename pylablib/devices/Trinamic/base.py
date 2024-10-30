from ...core.devio import comm_backend, interface
from ...core.utils import general

from ..interface import stage

import collections
import time
import struct
import math

class TrinamicError(comm_backend.DeviceError):
    """Generic Trinamic error"""
class TrinamicBackendError(TrinamicError,comm_backend.DeviceBackendError):
    """Generic Trinamic backend communication error"""
class TrinamicTimeoutError(TrinamicError):
    """Generic Trinamic timeout error"""

TLimitSwitchParams=collections.namedtuple("TLimitSwitchParams",["left_enable","right_enable"])
TVelocityParams=collections.namedtuple("TVelocityParams",["speed","accel","pulse_divisor","ramp_divisor"])
THomeParams=collections.namedtuple("THomeParams",["mode","search_speed","switch_speed"])
TTMCM1110ReplyData=collections.namedtuple("TTMCM1110ReplyData",["comm","status","value","addr","module"])
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
        self._add_settings_variable("home_parameters",self.get_home_parameters,self.setup_home)
        self._add_status_variable("current_parameters",self.get_current_parameters)
        self._add_status_variable("limit_switches_state",self.get_limit_switches_state)
        self._add_status_variable("velocity_factor",self.get_velocity_factor)
        self._add_status_variable("acceleration_factor",self.get_acceleration_factor)
        self._add_status_variable("microstep_resolution",self.get_microstep_resolution)
        self._add_status_variable("current_speed",self.get_current_speed)
        self._add_status_variable("moving",self.is_moving)
        self._add_status_variable("homing",self.is_homing)
        self._add_status_variable("last_home_position",self.get_last_home_position,ignore_error=TrinamicError)
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
        return TTMCM1110ReplyData(comm,status,value,addr,module)
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

    def get_axis_parameter(self, parameter, result_format="i", axis=0, addr=0):
        """Get a given axis parameter at the given axis and device address"""
        return self.query(6,parameter,0,result_format=result_format,bank=axis,addr=addr).value
    def set_axis_parameter(self, parameter, value, axis=0, addr=0):
        """Set a given axis parameter at the given axis and device address (volatile; resets on power cycling)"""
        self.query(5,parameter,value,bank=axis,addr=addr)
    def store_axis_parameter(self, parameter, value=None, axis=0, addr=0):
        """Store a given axis parameter in EEPROM at the given axis and device address (by default, value is the current value)"""
        if value is not None:
            self.set_axis_parameter(parameter,value,axis=axis,addr=addr)
        self.query(7,parameter,0,bank=axis,addr=addr)
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

    def move_to(self, position, axis=0, addr=0):
        """Move to a given position"""
        self.query(4,0,position,bank=axis,addr=addr)
    def move_by(self, steps=1, axis=0, addr=0):
        """Move by a given number of steps"""
        self.query(4,1,steps,bank=axis,addr=addr)
    def get_position(self, axis=0, addr=0):
        """Get the current axis position"""
        return self.get_axis_parameter(1,axis=axis,addr=addr)
    def set_position_reference(self, pos=0, axis=0, addr=0):
        """Set the current axis position as a reference (the actual motor position stays the same)"""
        self.set_axis_parameter(1,pos,axis=axis,addr=addr)
        return self.get_position(axis=axis,addr=addr)
    @interface.use_parameters
    def jog(self, direction, speed=None, axis=0, addr=0):
        """
        Jog in a given direction with a given speed.
        
        `direction` can be either ``"-"`` (negative, left) or ``"+"`` (positive, right).
        The motion continues until it is explicitly stopped, or until a limit is hit.
        If ``speed is None``, use the standard speed value.
        """
        if speed is None:
            speed=self.get_velocity_parameters(axis=axis,addr=addr)[0]
        self.query(1 if direction else 2,0,speed,bank=axis,addr=addr)
    def stop(self, axis=0, addr=0):
        """Stop motion"""
        self.query(3,0,0,bank=axis,addr=addr)

    def get_microstep_resolution(self, axis=0, addr=0):
        """Get the number of microsteps per full step (always a power of 2)"""
        return 2**self.get_axis_parameter(140,axis=axis,addr=addr)
    def set_microstep_resolution(self, resolution, axis=0, addr=0):
        """Set the number of microsteps per full step (rounded to a nearest power of 2)"""
        lresolution=round(math.log2(resolution))
        self.set_axis_parameter(140,lresolution,axis=axis,addr=addr)
        return self.get_microstep_resolution(axis=axis,addr=addr)
    
    def get_current_parameters(self, max_current=1, axis=0, addr=0):
        """
        Return diving current parameter ``(drive_current, standby_current)``.

        ``drive_current`` is the maximal drive current, which is given as a fraction of the `max_current`
        (which is either 1A or 2.8A depending on the hardware jumper).
        ``standby_current`` is given as a fraction of ``drive_current``.
        """
        return self.get_axis_parameter(6,axis=axis,addr=addr)/255.*max_current, self.get_axis_parameter(7,axis=axis,addr=addr)/255.*max_current
    def setup_current(self, drive_current=None, standby_current=None, max_current=1., axis=0, addr=0):
        """
        Set drive and standby currents.

        WARNING: too high of a setting might damage the motor.
        ``drive_current`` is the maximal drive current, which is given as a fraction of the `max_current`
        (which is either 1A or 2.8A depending on the hardware jumper, as described in the hardware manual).
        ``standby_current`` is given as a fraction of ``drive_current``.
        Any ``None`` parameters are left unchanged.
        """
        if drive_current is not None:
            drive_current=int(min(max(0,drive_current/max_current),1)*255)
        if standby_current is not None:
            standby_current=int(min(max(0,standby_current/max_current),1)*255)
        curr_standby_current=self.get_axis_parameter(7,axis=axis,addr=addr)
        if standby_current is not None and standby_current<curr_standby_current:
            self.set_axis_parameter(7,standby_current,axis=axis,addr=addr)
        if drive_current is not None:
            self.set_axis_parameter(6,drive_current,axis=axis,addr=addr)
        if standby_current is not None and standby_current>curr_standby_current:
            self.set_axis_parameter(7,standby_current,axis=axis,addr=addr)
        return self.get_current_parameters(max_current=max_current,axis=axis,addr=addr)

    def get_limit_switches_parameters(self, axis=0, addr=0):
        """Return limit switch parameters ``(left_enable, right_enable)``"""
        return TLimitSwitchParams(self.get_axis_parameter(13,axis=axis,addr=addr)==0, self.get_axis_parameter(12,axis=axis,addr=addr)==0)
    def setup_limit_switches(self, left_enable=None, right_enable=None, axis=0, addr=0):
        """Setup limit switch parameters"""
        if left_enable is not None:
            self.set_axis_parameter(13,0 if left_enable else 1,axis=axis,addr=addr)
        if right_enable is not None:
            self.set_axis_parameter(12,0 if right_enable else 1,axis=axis,addr=addr)
        return self.get_limit_switches_parameters(axis=axis,addr=addr)
    def get_limit_switches_state(self, axis=0, addr=0):
        """Get the state of the left and right limit switches"""
        return bool(self.get_axis_parameter(11,axis=axis,addr=addr)),bool(self.get_axis_parameter(10,axis=axis,addr=addr))
    def get_switch_polarity(self, axis=0, addr=0):
        """
        Get end switch polarity (``False`` for normal, ``True`` for reversed).
        
        Note that for 3-axis controller (TMCM-3110) the polarity is the same for all axes,
        and for 6-axis controller (TMCM-6110) it has to be the same for the first 3 and the last 3 axes
        """
        pol=self.get_global_parameter(79,addr=addr)
        mask=0x01 if axis<3 else 0x02
        return bool(pol&mask)
    def set_switch_polarity(self, polarity=False, axis=0, addr=0):
        """
        Set end switch polarity (``False`` for normal, ``True`` for reversed).
        
        Note that for 3-axis controller (TMCM-3110) the polarity is the same for all axes,
        and for 6-axis controller (TMCM-6110) it has to be the same for the first 3 and the last 3 axes
        """
        pol=self.get_global_parameter(79,addr=addr)
        mask=0x01 if axis<3 else 0x02
        pol=(pol&~mask)|(mask if polarity else 0)
        self.set_global_parameter(79,pol,addr=addr)
        return self.get_switch_polarity(axis=axis,addr=addr)
    
    _p_home_mode=interface.EnumParameterClass("home_mode",
        {"lim_left":1,"lim_right_left":2,"lim_right_left_bothsides":3,"lim_left_bothsides":4,
        "lim_right":65,"lim_left_right":66,"lim_left_right_bothsides":67,"lim_right_bothsides":68,
        "home_neg_switch":5,"home_pos_switch":6,"home_pos":7,"home_neg":8,
        "home_neg_switch_inv":133,"home_pos_switch_inv":134,"home_pos_inv":135,"home_neg_inv":136})
    @interface.use_parameters(_returns=("home_mode",None,None))
    def get_home_parameters(self, axis=0, addr=0):
        """
        Return homing parameters ``(mode, search_speed, switch_speed)``.

        ``mode`` is one of 16 different values, which can start with ``"lim_"`` indicating reliance on limit switches,
        or with ``"home_"`` indicating usage of home switches. Home-based switches can also be inverted (with ``"_inv"`` in the end),
        indicating that the homing switch function is inverted (0 instead of 1 means that the switch is engaged). More details can be found in the manual.
        ``search_speed`` and ``switch_speed`` describe, respectively, the initial speed while searching for the switch,
        and the final homing speed while searching for the edge of the switch action. Both are given in *internal* units.
        """
        mode=self.get_axis_parameter(193,axis=axis,addr=addr)
        search_speed=self.get_axis_parameter(194,axis=axis,addr=addr)
        switch_speed=self.get_axis_parameter(195,axis=axis,addr=addr)
        return THomeParams(mode,search_speed,switch_speed)
    @interface.use_parameters(mode="home_mode")
    def setup_home(self, home_mode=None, search_speed=None, switch_speed=None, axis=0, addr=0):
        """
        Setup homing parameters ``(mode, search_speed, switch_speed)``.

        ``mode`` is one of 16 different values, which can start with ``"lim_"`` indicating reliance on limit switches,
        or with ``"home_"`` indicating usage of home switches. Home-based switches can also be inverted (with ``"_inv"`` in the end),
        indicating that the homing switch function is inverted (0 instead of 1 means that the switch is engaged). More details can be found in the manual.
        ``search_speed`` and ``switch_speed`` describe, respectively, the initial speed while searching for the switch,
        and the final homing speed while searching for the edge of the switch action. Both are given in *internal* units.
        """
        if home_mode is not None:
            self.set_axis_parameter(193,home_mode,axis=axis,addr=addr)
        if search_speed is not None:
            self.set_axis_parameter(194,search_speed,axis=axis,addr=addr)
        if switch_speed is not None:
            self.set_axis_parameter(195,switch_speed,axis=axis,addr=addr)
        return self.get_home_parameters(axis=axis,addr=addr)
    
    def home(self, wait=True, timeout=30., axis=0, addr=0):
        """
        Home the given axis.

        If ``wait==True``, wait until the homing is complete or until `timeout` is passed.
        Note that homing affects the velocity parameters, which need to be re-established after the homing is complete.
        This is done automatically when ``wait==True``, but needs to be done manually otherwise.
        """
        velpar=self.get_velocity_parameters(axis=axis,addr=addr)
        self.query(13,0,0,bank=axis,addr=addr)
        if wait:
            ctd=general.Countdown(timeout)
            try:
                while self.is_homing(axis=axis):
                    if ctd.passed():
                        raise TrinamicTimeoutError("timeout while homing the stage at address {}".format(addr))
                    time.sleep(0.05)
            finally:
                self.query(13,1,0,bank=axis,addr=addr)
                self.setup_velocity(*velpar,axis=axis,addr=addr)
    def is_homing(self, axis=0, addr=0):
        """Check if homing is in progress at the given address"""
        return bool(self.query(13,2,0,bank=axis,addr=addr).value)
    def get_last_home_position(self, axis=0, addr=0):
        """Get the last readout position when the homing operation was complete (0 upon startup)"""
        return self.get_axis_parameter(197,axis=axis,addr=addr)

    def get_velocity_parameters(self, axis=0, addr=0):
        """
        Return velocity parameters ``(speed, accel, pulse_divisor, ramp_divisor)``.
        
        ``speed`` and ``accel`` denote, correspondingly, maximal (i.e., steady regime) moving speed and acceleration in *internal* units.
        ``pulse_divisor`` is the driver pulse divisor, which defines how internal velocity units translate into microsteps/s (see :meth:`get_velocity_factor`);
        can only be a power of 2, higher values mean slower motion.
        ``ramp_divisor`` is the driver ramp divisor, which, together with the pulse divisor,
        defines how internal acceleration units translate into microsteps/s^2 (see :meth:`get_acceleration_factor`);
        rounded to the nearest power of 2, higher values mean slower acceleration.
        """
        return TVelocityParams(self.get_axis_parameter(4,axis=axis,addr=addr),self.get_axis_parameter(5,axis=axis,addr=addr),
                            2**self.get_axis_parameter(154,axis=axis,addr=addr),2**self.get_axis_parameter(153,axis=axis,addr=addr))
    def setup_velocity(self, speed=None, accel=None, pulse_divisor=None, ramp_divisor=None, axis=0, addr=0):
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
            self.set_axis_parameter(4,speed,axis=axis,addr=addr)
        if accel is not None:
            self.set_axis_parameter(5,accel,axis=axis,addr=addr)
        if pulse_divisor is not None:
            lpulse_divisor=round(math.log2(pulse_divisor))
            self.set_axis_parameter(154,lpulse_divisor,axis=axis,addr=addr)
        if ramp_divisor is not None:
            lramp_divisor=round(math.log2(ramp_divisor))
            self.set_axis_parameter(153,lramp_divisor,axis=axis,addr=addr)
        return self.get_velocity_parameters(axis=axis,addr=addr)

    def get_velocity_factor(self, axis=0, addr=0):
        """Get the ratio between the real speed (in microsteps/s) and the internal units"""
        return 16E6/(2**self.get_axis_parameter(154,axis=axis,addr=addr)*2048*32)
    def get_acceleration_factor(self, axis=0, addr=0):
        """Get the ratio between the real acceleration (in microsteps/s^2) and the internal units"""
        return 16E6**2/2**(self.get_axis_parameter(153,axis=axis,addr=addr)+self.get_axis_parameter(154,axis=axis,addr=addr)+29)

    def get_current_speed(self, axis=0, addr=0):
        """Get the instantaneous speed in internal units"""
        return self.get_axis_parameter(3,axis=axis,addr=addr)
    def is_moving(self, axis=0, addr=0):
        """Check if the motor is moving"""
        return bool(self.get_current_speed(axis=axis,addr=addr))
    def wait_move(self, axis=0, addr=0):
        """Wait until motion is done"""
        while self.get_current_speed(axis=axis,addr=addr):
            time.sleep(0.01)



def _as_multiaxis_get_method(func, naxes):
    def wrapped():
        return {ax:func(axis=ax) for ax in range(naxes)}
    return wrapped
def _as_multiaxis_set_method(func, naxes):
    def wrapped(par):
        if not isinstance(par,dict):
            par={ax:par for ax in range(naxes)}
        return {ax:func(*par[ax],axis=ax) for ax in range(naxes)}
    return wrapped
class TMCMx110(TMCM1110,stage.IMultiaxisStage):
    """
    Trinamic multi-axis stepper motor controller TMCM-x110 (1110, 3110, 6110) controlled using TMCL Firmware.

    The main difference from the single-axis TMCM1110 is that it determines the number of axes upon the connection,
    and that the device variables return dictionaries ``{axis: value}`` instead of a single value (even for single-axis controller for consistency).

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
        naxes: maximal number of axes to check for upon connection; if the actual number is larger, use only first `naxes` axes
    """
    Error=TrinamicError
    def __init__(self, conn, naxes=None):
        super().__init__(conn=conn)
        with self._close_on_error():
            self._update_axes(list(range(self._detect_axes_number(nmax=naxes or 12))))
            naxes=len(self._axes)
        self._add_status_variable("position",_as_multiaxis_get_method(self.get_position,naxes))
        self._add_settings_variable("velocity_parameters",_as_multiaxis_get_method(self.get_velocity_parameters,naxes),_as_multiaxis_set_method(self.setup_velocity,naxes))
        self._add_settings_variable("limit_switches_parameters",_as_multiaxis_get_method(self.get_limit_switches_parameters,naxes),_as_multiaxis_set_method(self.setup_limit_switches,naxes))
        self._add_settings_variable("home_parameters",_as_multiaxis_get_method(self.get_home_parameters,naxes),_as_multiaxis_set_method(self.setup_home,naxes))
        self._add_status_variable("current_parameters",_as_multiaxis_get_method(self.get_current_parameters,naxes))
        self._add_status_variable("velocity_factor",_as_multiaxis_get_method(self.get_velocity_factor,naxes))
        self._add_status_variable("acceleration_factor",_as_multiaxis_get_method(self.get_acceleration_factor,naxes))
        self._add_status_variable("microstep_resolution",_as_multiaxis_get_method(self.get_microstep_resolution,naxes))
        self._add_status_variable("current_speed",_as_multiaxis_get_method(self.get_current_speed,naxes))
        self._add_status_variable("moving",_as_multiaxis_get_method(self.is_moving,naxes))

    def _detect_axes_number(self, nmax):
        for i in range(nmax):
            try:
                self.get_axis_parameter(0,axis=i)
            except TrinamicError:
                return i
        return nmax