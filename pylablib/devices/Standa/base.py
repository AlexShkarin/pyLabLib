from ...core.utils import py3, crc, general, funcargparse
from ...core.devio import comm_backend, interface
from ..interface import stage

import struct
import collections
import time



class StandaError(comm_backend.DeviceError):
    """Generic Standa device StandaError"""
class StandaBackendError(StandaError,comm_backend.DeviceBackendError):
    """Generic Standa backend communication error"""



TEngineType=collections.namedtuple("TEngineType",["engine","driver"])
TStepperMotorCalibration=collections.namedtuple("TStepperMotorCalibration",["steps_per_rev","usteps_per_step"])
TFullState=collections.namedtuple("TFullState",["smov","scmd","spwr","senc","swnd","position","encoder","speed","ivpwr","ivusb","temp","flags","gpio"])
TMoveParams=collections.namedtuple("TMoveParams",["speed","accel","decel","antiplay"])
TPowerParams=collections.namedtuple("TPowerParams",["hold_current","reduct_enabled","reduct_delay","off_enabled","off_delay","ramp_enabled","ramp_time"])
class Standa8SMC(comm_backend.ICommBackendWrapper,stage.IStage):
    """
    Generic Standa 8SMC4/8SMC5 controller device.

    Args:
        conn: serial connection parameters (usually port, a tuple containing port and baudrate,
            or a tuple with full specification such as ``("COM1", 115200, 8, 'N', 2)``)
    """
    Error=StandaError
    def __init__(self, conn):
        instr=comm_backend.new_backend(conn,"serial",term_read="",term_write="",defaults={"serial":("COM1",115200,8,'N',2)},timeout=1.,reraise_error=StandaBackendError)
        super().__init__(instr)
        self._add_info_variable("engine_type",self.get_engine_type)
        self._add_info_variable("stepper_motor_calibration",self.get_stepper_motor_calibration)
        self._add_status_variable("status",self.get_status)
        self._add_status_variable("position",self.get_position)
        self._add_status_variable("encoder",self.get_encoder)
        self._add_settings_variable("move_parameters",self.get_move_parameters,self.setup_move)
        with self._close_on_error():
            self._engine_type=self.get_engine_type()
            self._stepper_motor_calibration=self.get_stepper_motor_calibration()
    

    def _crc(self, msg):
        return crc.crc(msg,0x8005,refin=True,refout=True,init=0xFFFF)
    def _build_msg(self, cmd, data=b""):
        if len(cmd)!=4:
            raise ValueError("command is supposed to be 4 bytes long; got {}".format(len(cmd)))
        if data:
            return py3.as_builtin_bytes(cmd)+py3.as_builtin_bytes(data)+struct.pack("<H",self._crc(data))
        return py3.as_builtin_bytes(cmd)
    _error_cmd={"errc":"unrecognized command","errd":"invalid CRC","errv":"value out of range"}
    def _parse_msg(self, msg, ecmd=None):
        if len(msg)<7 and len(msg)!=4:
            self._resync()
            raise StandaError("incoming message should be 4 bytes long or at least 7 bytes long; got {}".format(len(msg)))
        cmd=py3.as_str(msg[:4])
        if cmd in self._error_cmd:
            self._resync()
            raise StandaError("command {}returned an error '{}' ({})".format("" if ecmd is None else ecmd+" ",cmd,self._error_cmd[cmd]))
        if ecmd is not None and cmd!=ecmd:
            self._resync()
            raise StandaError("expected reply with command {}; got {}".format(ecmd,cmd))
        if len(msg)>4:
            data=msg[4:-2]
            mcrc,=struct.unpack("<H",msg[-2:])
            ecrc=self._crc(data)
            if ecrc!=mcrc:
                self._resync()
                raise StandaError("invalid CRC: expected 0x{:04X}, got 0x{:04X}".format(ecrc,mcrc))
            return data
    _full_reply_delay=10E-3
    def query(self, cmd, data=b"", retlen=None):
        msg=self._build_msg(cmd,data)
        self.instr.write(msg)
        while True:
            b=self.instr.read(1)
            if b!=b"\x00":
                if retlen is None:
                    time.sleep(self._full_reply_delay)
                    reply=b+self.instr.read()
                else:
                    reply=b+self.instr.read(retlen+5 if retlen else 3)
                break
        return self._parse_msg(reply,cmd)
    _comms={"gent":(None, (8,"BB")),
            "gpos":(None, (20,"<ihq")),
            "spos":((20,"<ihqB"), None),
            "move":((12,"<ih"), None),
            "movr":((12,"<ih"), None),
            "gets":(None,(48,"<BBBBBihqihhhhhhIIB")),
            "gmov":(None,(24,"<IBHHIB")),
            "smov":((24,"<IBHHIB"),None),
            "gpwr":(None,(14,"<BHHHB")),
            "spwr":((14,"<BHHHB"),None),
            }
    def pquery(self, cmd, *args):
        if cmd not in self._comms:
            raise ValueError("command {} is not among defined commands".format(cmd))
        arg,rval=self._comms[cmd]
        if arg is not None:
            data=struct.pack(arg[1],*args)
            data+=b"\x00"*(arg[0]-len(data))
        else:
            data=b""
        reply=self.query(cmd,data,retlen=0 if rval is None else rval[0])
        if rval is not None:
            return struct.unpack(rval[1],reply[:struct.calcsize(rval[1])])
    
    def _resync(self):
        for _ in range(250):
            self.instr.write(b"\x00")
            time.sleep(1E-3)
            res=self.instr.read()
            if res and res==b"\x00"*len(res):
                return True
        return False

    _p_eng_type=interface.EnumParameterClass("eng_type",{"none":0,"dc":1,"dc2":2,"step":3,"test":4,"brushless":5})
    _p_drv_type=interface.EnumParameterClass("drv_type",{"fet":1,"integr":2,"ext":3})
    @interface.use_parameters(_returns=("eng_type","drv_type"))
    def get_engine_type(self):
        """Get engine and driver type"""
        return TEngineType(*self.pquery("gent"))
    def get_stepper_motor_calibration(self):
        """
        Get stepper motor calibration parameters.

        Return tuple ``(steps_per_rev, usteps_per_step)``.
        """
        fusps,spr=struct.unpack("<BH",self.query("geng")[13:16])
        usps=(1<<(fusps-1)) if fusps>0 else 1
        return TStepperMotorCalibration(spr,usps)
    def _pup2p(self, stp, ustp):
        usps=self._stepper_motor_calibration.usteps_per_step
        if self._engine_type.engine=="step":
            return stp*usps+ustp
        return stp
    def _p2pup(self, stp):
        usps=self._stepper_motor_calibration.usteps_per_step
        if self._engine_type.engine=="step":
            s=1 if stp>=0 else -1
            return s*int(abs(stp)//usps),s*int(abs(stp)%usps)
        return stp
    
    _p_state_cmd=interface.EnumParameterClass("state_cmd",{"unknown":0,"move":1,"movr":2,"left":3,"right":4,"stop":5,"home":6,"loft":7,"sstp":8})
    _p_state_pwr=interface.EnumParameterClass("state_pwr",{"unknown":0,"off":1,"norm":3,"reduct":4,"max":5})
    _p_state_enc=interface.EnumParameterClass("state_enc",{"absent":0,"unknown":1,"malfunc":2,"referse":3,"ok":4})
    _p_state_wnd=interface.EnumParameterClass("state_wnd",{"absent":0,"unknown":1,"malfunc":2,"ok":3})
    _move_flags={"moving":0x01,"target_speed":0x02,"antiplay":0x04}
    _cmd_flags={"error":0x40,"running":0x80}
    def get_status(self):
        """
        Get device status.

        Return tuple ``(smov, scmd, spwr, senc, swnd, position, encoder, speed, ivpwr, ivusb, temp, flags, gpio)``
        with the moving state (whether motor is moving, reached speed, etc.), command state (last issued command and its status),
        power state, encoder state, winding state (currently not used), step position, encoder position, current speed,
        current and voltage of the power supply, current and voltage of the USB source, temperature (in C), and additional state and GPIO flags.
        """
        stat=self.pquery("gets")
        smov=tuple(f for f,m in self._move_flags.items() if stat[0]&m)
        if stat[1]&self._cmd_flags["running"]:
            cmdstate="running"
        elif stat[1]&self._cmd_flags["error"]:
            cmdstate="error"
        else:
            cmdstate="success"
        scmd=(self._parameters["state_cmd"].i(stat[1]&0x3F),cmdstate)
        spwr=self._parameters["state_pwr"].i(stat[2])
        senc=self._parameters["state_enc"].i(stat[3])
        swnd=(self._parameters["state_wnd"].i(stat[4]&0x0F),self._parameters["state_wnd"].i(stat[4]>>4))
        position=self._pup2p(*stat[5:7])
        encoder=stat[7]
        speed=self._pup2p(*stat[8:10])
        ivpwr=stat[10]/1E3,stat[11]/100
        ivusb=stat[12]/1E3,stat[13]/100
        temp=stat[14]/10
        flags=stat[15]
        gpio=stat[16]
        return TFullState(smov,scmd,spwr,senc,swnd,position,encoder,speed,ivpwr,ivusb,temp,flags,gpio)
    def is_moving(self):
        """Check if the motor is moving"""
        stat=self.pquery("gets")
        return bool(stat[0]&0x01) or bool(stat[1]&0x80)
    def wait_move(self, timeout=None):
        """Wait until motion is done"""
        ctd=general.Countdown(timeout)
        while self.is_moving():
            if ctd.passed():
                raise StandaError("timeout waiting for move")
            time.sleep(10E-3)

    def get_position(self):
        """Return step position (in steps for a DC motor, in microsteps for a stepper motor)"""
        return self._pup2p(*self.pquery("gpos")[:2])
    def get_encoder(self):
        """Return encoder position"""
        return self.pquery("gpos")[2]
    def set_position_reference(self, position=0):
        """
        Set position reference (in steps for a DC motor, in microsteps for a stepper motor).
        
        Actual motor position stays the same.
        """
        stp,ustp=self._p2pup(position)
        self.pquery("spos",stp,ustp,0,0x02)
        return self.get_position()
    def set_encoder_reference(self, position=0):
        """
        Set encoder reference.
        
        Actual motor position stays the same.
        """
        self.pquery("spos",0,0,position,0x01)
        return self.get_encoder()
    def move_to(self, position):
        """Move to the given position (in steps for a DC motor, in microsteps for a stepper motor)"""
        self.pquery("move",*self._p2pup(position))
    def move_by(self, distance):
        """Move by the given distance (in steps for a DC motor, in microsteps for a stepper motor)"""
        self.pquery("movr",*self._p2pup(distance))
    def stop(self, immediate=False):
        self.query("stop" if immediate else "sstp")
    def power_off(self, stop="soft"):
        funcargparse.check_parameter_range(stop,"stop",["soft","immediate","none"])
        if stop!="none" and self.is_moving():
            self.stop(immediate=(stop=="immediate"))
        self.query("pwof")
    @interface.use_parameters
    def jog(self, direction):
        """Start moving in a given direction (``"+"`` or ``"-"``)"""
        self.query("rigt" if direction else "left")
    def home(self, sync=True, timeout=30.):
        """
        Home the motor.
        
        If ``sync==True``, wait until the homing is complete, or until `timeout` expires.
        """
        self.query("home")
        time.sleep(10E-3)
        if sync:
            self.wait_move(timeout)
    
    def get_move_parameters(self):
        """
        Get moving parameters.
        
        Return tuple ``(speed, accel, decel, antiplay)``.
        """
        par=self.pquery("gmov")
        return TMoveParams(self._pup2p(*par[:2]),self._pup2p(par[2],0),self._pup2p(par[3],0),self._pup2p(*par[4:6]))
    def setup_move(self, speed=None, accel=None, decel=None, antiplay=None):
        """
        Setup moving parameters.
        
        If any parameter is ``None``, use the current value.
        """
        par=self.get_move_parameters()
        speed=par.speed if speed is None else int(speed)
        accel=par.accel if accel is None else int(accel)
        decel=par.decel if decel is None else int(decel)
        antiplay=par.antiplay if antiplay is None else int(antiplay)
        par=self._p2pup(speed)+(self._p2pup(accel)[0],self._p2pup(decel)[0])+self._p2pup(antiplay)
        self.pquery("smov",*par)
        return self.get_move_parameters()
    
    def get_power_parameters(self):
        """
        Get power parameters.
        
        Return tuple ``(hold_current, reduct_enabled, reduct_delay, off_enabled, off_delay, ramp_enabled, ramp_time)``.
        """
        par=self.pquery("gpwr")
        return TPowerParams(par[0],bool(par[4]&0x01),par[1]/1E3,bool(par[4]&0x02),par[2]/1E3,bool(par[4]&0x04),par[3]/1E3)
    def setup_power(self, hold_current=None, reduct_enabled=None, reduct_delay=None, off_enabled=None, off_delay=None, ramp_enabled=None, ramp_time=None):
        """
        Setup power parameters.
        
        If any parameter is ``None``, use the current value.
        """
        par=self.get_power_parameters()
        hold_current=par.hold_current if hold_current is None else hold_current
        reduct_enabled=par.reduct_enabled if reduct_enabled is None else reduct_enabled
        reduct_delay=par.reduct_delay if reduct_delay is None else reduct_delay
        off_enabled=par.off_enabled if off_enabled is None else off_enabled
        off_delay=par.off_delay if off_delay is None else off_delay
        ramp_enabled=par.ramp_enabled if ramp_enabled is None else ramp_enabled
        ramp_time=par.ramp_time if ramp_time is None else ramp_time
        flags=(0x01 if reduct_enabled else 0x00)|(0x02 if off_enabled else 0x00)|(0x04 if ramp_enabled else 0x00)
        self.pquery("spwr",int(hold_current),int(reduct_delay*1E3),int(off_delay*1E3),int(ramp_time*1E3),flags)
        return self.get_power_parameters()