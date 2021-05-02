from ...core.devio import interface, comm_backend
from ...core.utils import general, funcargparse, py3
from .base import ThorlabsError, ThorlabsTimeoutError, ThorlabsBackendError

from ..interface.stage import IStage

import struct
import warnings

import re
import time

import collections



def list_kinesis_devices(filter_ids=True):
    """
    List all Thorlabs APT/Kinesis devices connected ot this PC.

    Return list of tuples ``(conn, description)``.
        If ``filter_ids==True``, only leave devices with Tholabs-like IDs (8-digit numbers).
        Otherwise, show all devices (some of them might not be Thorlabs-related).
    """
    return KinesisDevice.list_devices(filter_ids=filter_ids)



TDeviceInfo=collections.namedtuple("TDeviceInfo",["serial_no","model_no","fw_ver","hw_type","hw_ver","mod_state","nchannels","notes"])
class BasicKinesisDevice(comm_backend.ICommBackendWrapper):
    """
    Generic Kinesis device.

    Implements FTDI chip connectivity via pyft232 (virtual serial interface).

    Args:
        conn: serial connection parameters (usually an 8-digit device serial number).
    """
    Error=ThorlabsError
    def __init__(self, conn, timeout=3.):
        conn=comm_backend.FT232DeviceBackend.combine_conn(conn,(None,115200))
        self.conn=conn
        instr=comm_backend.FT232DeviceBackend(conn,term_write=b"",term_read=b"",timeout=timeout,reraise_error=ThorlabsBackendError)
        instr.setup_cooldown(write=0.003)
        comm_backend.ICommBackendWrapper.__init__(self,instr)
        self._add_info_variable("device_info",self.get_device_info)
        self._bg_msg_counters={}

    @staticmethod
    def list_devices(filter_ids=True):
        """
        List all connected devices.

        Return list of tuples ``(conn, description)``.
        If ``filter_ids==True``, only leave devices with Tholabs-like IDs (8-digit numbers).
        Otherwise, show all devices (some of them might not be Thorlabs-related).
        """
        def _is_thorlabs_id(did):
            return re.match(r"^\d{8}$",did[0]) is not None
        dids=comm_backend.FT232DeviceBackend.list_resources(desc=True)
        if filter_ids:
            ids=[did for did in dids if _is_thorlabs_id(did)]
        return ids
    def send_comm(self, messageID, param1=0x00, param2=0x00, source=0x01, dest=0x50):
        """
        Send a message with no associated data.

        For details, see APT communications protocol.
        """
        msg=struct.pack("<HBBBB",messageID,param1,param2,dest,source)
        self.instr.write(msg)
    def send_comm_data(self, messageID, data, source=0x01, dest=0x50):
        """
        Send a message with associated data.

        For details, see APT communications protocol.
        """
        msg=struct.pack("<HHBB",messageID,len(data),dest|0x80,source)
        self.instr.write(msg+data)

    CommShort=collections.namedtuple("CommShort",["messageID","param1","param2","source","dest"])
    CommData=collections.namedtuple("CommData",["messageID","data","source","dest"])
    def recv_comm(self, expected_id=None):
        """
        Receive a message.

        Return either :class:`CommShort` or :class:`CommData` depending on the message type
        (fixed length with two parameters, or variable length with associated data).
        If `expected_id` is not ``None`` and the received message ID is different from `expected_id`, raise an error.
        For details, see APT communications protocol.
        """
        while True:
            msg=self.instr.read(6)
            messageID,_,dest,source=struct.unpack("<HHBB",msg[:6])
            if dest&0x80:
                dest=dest&0x7F
                datalen,=struct.unpack("<H",msg[2:4])
                data=self.instr.read(datalen)
                comm=self.CommData(messageID,data,source,dest)
            else:
                param1,param2=struct.unpack("<BB",msg[2:4])
                comm=self.CommShort(messageID,param1,param2,source,dest)
            if messageID in self._bg_msg_counters:
                cnt,_=self._bg_msg_counters[messageID]
                self._bg_msg_counters[messageID]=(cnt+1,comm)
            else:
                if expected_id is not None and messageID!=expected_id:
                    raise ThorlabsError("unexpected command received: expected 0x{:04x}, got 0x{:04x}".format(expected_id,messageID))
                return comm
    def query(self, messageID, param1=0, param2=0, source=0x01, dest=0x50, replyID=-1):
        """
        Send a query to the device and receive the reply.

        A combination of :meth:`send_comm` and :meth:`recv_comm`.
        If `replyID` is not ``None``, specifies the exepected reply message ID; if -1 (default), set to te be ``messageID+1`` (the standard convention).
        """
        if replyID<0:
            replyID=messageID+1
        self.send_comm(messageID,param1=param1,param2=param2,source=source,dest=dest)
        return self.recv_comm(expected_id=replyID)
    def add_background_comm(self, messageID):
        """
        Mark given messageID as a 'background' message, which can be sent at any point without prompt (e.g., some operation confirmation).

        If it is received instead during ``recv_comm_`` operations, it is ignored, and the corresponding counter is increased.
        """
        self._bg_msg_counters.setdefault(messageID,(0,None))
    def check_background_comm(self, messageID):
        """Return message counter and the last message value (``None`` if not message received yet) of a given 'background' message."""
        return self._bg_msg_counters[messageID]

    _device_SN={   20:"BSC001", 21:"BPC001", 22:"BNT001", 25:"BMS001", 26:"KST101", 27:"KDC101", 28:"KBD101", 29:"KPZ101",
                    30:"BSC002", 31:"BPC002", 33:"BDC101", 35:"BMS002", 37:"MFF10." ,
                    40:"BSC101", 41:"BPC101", 43:"BDC101", 44:"PPC001", 45:"LTS"   , 48:"MMR"   , 49:"MLJ"   ,
                    50:"MST60" , 51:"MPZ601", 52:"MNA601", 55:"K10CR1", 56:"KLS101", 57:"KNA101", 59:"KSG101",
                    60:"0ST001", 63:"ODC001", 64:"TLD001", 65:"TIM001", 67:"TBD001", 68:"KSC101", 69:"KPA101",
                    70:"BSC.03", 71:"BPC.03", 72:"BPS103", 73:"BBD103", 
                    80:"TST001", 81:"TPZ001", 82:"TNZ001", 83:"TDC001", 84:"TSG001", 85:"TSC001", 86:"TLS001", 87:"TTC001", 89:"TQD001", 
                    90:"SCC101", 91:"PCC101", 93:"DCC101", 94:"BCC101", 95:"PPC102", 96:"PCC102"}
    def _get_device_model(self):
        addr=str(self.conn.get("port",""))
        if len(addr)==8 and addr.isdigit():
            msn=int(addr[:2])
            return msn,self._device_SN.get(msn,None)
        return None,None
    def _model_match(self, model_no, port_model_no):
        if port_model_no is None:
            return True
        if model_no.startswith(port_model_no):
            return True
        if re.match("^"+port_model_no+"$",model_no):
            return True
        return False
    def get_device_info(self, dest=0x50):
        """
        Get device info.
        """
        data=self.query(0x0005,dest=dest).data
        serial_no,=struct.unpack("<I",data[:4])
        model_no=data[4:12].decode().strip("\x00")
        port,port_model_no=self._get_device_model()
        if not self._model_match(model_no,port_model_no):
            warnings.warn("model number {} doesn't match the device ID prefix {}({})".format(model_no,port,port_model_no))
        fw_ver="{}.{}.{}".format(*struct.unpack("<BBB",data[14:17])[::-1])
        hw_type,=struct.unpack("<H",data[12:14])
        hw_ver,mod_state,nchannels=struct.unpack("<HHH",data[78:84])
        notes=py3.as_str(data[18:66]).strip("\x00")
        return TDeviceInfo(serial_no,model_no,fw_ver,hw_type,hw_ver,mod_state,nchannels,notes)
    def get_number_of_channels(self):
        """Get number of channels on the device"""
        return self.get_device_info().nchannels

    def blink(self, channel=1, dest=0x50):
        """Identify the physical device (by, e.g., blinking status LED or screen)"""
        self.send_comm(0x0223,channel,dest=dest)

    def _store_as_default(self, messageID, channel=1):
        self.send_comm(0x04B9,channel,messageID>>8,messageID&0xFF)










TVelocityParams=collections.namedtuple("TVelocityParams",["min_velocity","acceleration","max_velocity"])
TJogParams=collections.namedtuple("TJogParams",["mode","step_size","min_velocity","acceleration","max_velocity","stop_mode"])
TGenMoveParams=collections.namedtuple("TGenMoveParams",["backlash_distance"])
THomeParams=collections.namedtuple("THomeParams",["home_direction","limit_switch","velocity","offset_distance"])
TLimitSwitchParams=collections.namedtuple("TLimitSwitchParams",["hw_kind_cw","hw_kind_ccw","hw_swapped","sw_position_cw","sw_position_ccw","sw_kind"])
class KinesisDevice(BasicKinesisDevice,IStage):
    def __init__(self, conn, timeout=3.):
        super().__init__(conn,timeout=timeout)
        self._forward_positive=False
    def _get_status_n(self, channel=1):
        """
        Get numerical status of the device.

        For details, see APT communications protocol.
        """
        data=self.query(0x0429,channel).data
        return struct.unpack("<I",data[2:6])[0]
    status_bits=[(1<<0,"sw_bk_lim"),(1<<1,"sw_fw_lim"),
                (1<<4,"moving_bk"),(1<<5,"moving_fw"),(1<<6,"jogging_bk"),(1<<7,"jogging_fw"),
                (1<<9,"homing"),(1<<10,"homed"),(1<<12,"tracking"),(1<<13,"settled"),
                (1<<14,"motion_error"),(1<<24,"current_limit"),(1<<31,"enabled")]
    def _get_status(self, channel=1):
        """
        Get device status.

        Return list of status strings, which can include ``"sw_fw_lim"`` (forward limit switch reached), ``"sw_bk_lim"`` (backward limit switch reached),
        ``"moving_fw"`` (moving forward), ``"moving_bk"`` (moving backward), ``"jogging_fw"`` (jogging forward), ``"jogging_bk"`` (jogging backward),
        ``"homing"`` (homing), ``"homed"`` (homing done), ``"tracking"``, ``"settled"``,
        ``"motion_error"`` (excessive position error), ``"current_limit"`` (motor current limit exceeded), or ``"enabled"`` (motor is enabled).
        """
        status_n=self._get_status_n(channel=channel)
        return [s for (m,s) in self.status_bits if status_n&m]
    def _wait_for_status(self, status, enabled, channel=1, timeout=None, period=0.05):
        """
        Wait until the given status (or list of status bits) is in the desired state.

        `status` is a string or a list of strings describing the status bits to monitor; for possible values, see :meth:`get_status`.
        If ``enabled==True``, wait until one of the given statuses is enabled; otherwise, wait until all given statuses are disabled.
        `period` specifies status checking period (in s).
        """
        status=funcargparse.as_sequence(status)
        for s in status:
            funcargparse.check_parameter_range(s,"status",[s for _,s in self.status_bits])
        ctd=general.Countdown(timeout)
        while True:
            curr_status=self._get_status(channel=channel)
            if enabled and any([s in curr_status for s in status]):
                return
            if (not enabled) and all([s not in curr_status for s in status]):
                return
            if ctd.passed():
                raise ThorlabsTimeoutError
            time.sleep(period)

    def _home(self, sync=True, force=False, channel=1, timeout=None):
        """
        Home the device.

        If ``sync==True``, wait until homing is done (with the given timeout).
        If ``force==False``, only home if the device isn't homed already.
        """
        if self._is_homed() and not force:
            return
        self.send_comm(0x0443,channel)
        if sync:
            self._wait_for_home(channel=channel,timeout=timeout)
    def _is_homing(self, channel=1):
        """Check if homing is in progress"""
        return "homing" in self._get_status(channel=channel)
    def _is_homed(self, channel=1):
        """Check if the device is homed"""
        return "homed" in self._get_status(channel=channel)
    def _wait_for_home(self, channel=1, timeout=None):
        """Wait until the device is homed"""
        return self._wait_for_status("homed",True,channel=channel,timeout=timeout)
    
    def _get_scale(self):
        """Get 3-tuple with scaling for position, velocity, and acceleration (ratio of device units to physical units)"""
        return (1,1,1)
    def _p2d(self, value, kind, scale=True):
        """
        Convert value from physical units to device units.

        `kind` is either ``"p"`` (position), ``"v"`` (velocity), or ``'a"`` (acceleration).
        If ``scale==False``, keep the supplied value as is (but convert it to integer).
        """
        idx="pva".index(kind)
        scale=self._get_scale()[idx] if scale else 1
        if scale!=1:
            value*=scale
        return int(value)
    def _d2p(self, value, kind, scale=True):
        """
        Convert value from device units to physical units.

        `kind` is either ``"p"`` (position), ``"v"`` (velocity), or ``'a"`` (acceleration).
        If ``scale==False``, keep the supplied value as is.
        """
        idx="pva".index(kind)
        scale=self._get_scale()[idx] if scale else 1
        if scale!=1:
            value/=scale
        return value
    def _get_position(self, channel=1, scale=True):
        """
        Get current position.
        
        If ``scale==True``, return value in the physical units (see class description); otherwise, return it in the device internal units (steps).
        """
        data=self.query(0x0411,channel).data
        pos=struct.unpack("<i",data[2:6])[0]
        return self._d2p(pos,"p",scale=scale)
    def _set_position_reference(self, position=0, channel=1, scale=True):
        """
        Set position reference (actual motor position stays the same).
        
        If ``scale==True``, assume that the position is in the physical units (see class description); otherwise, assume it is in the device internal units (steps).
        """
        self.send_comm_data(0x0410,struct.pack("<Hi",channel,self._p2d(position,"p",scale=scale)))
        return self._get_position(channel=channel)
    def _move_by(self, distance=1, channel=1, scale=True):
        """
        Move by a given amount (positive or negative) from the current position.
        
        If ``scale==True``, assume that the distance is in the physical units (see class description); otherwise, assume it is in the device internal units (steps).
        """
        self.send_comm_data(0x0448,struct.pack("<Hi",channel,self._p2d(distance,"p",scale=scale)))
    def _move_to(self, position, channel=1, scale=True):
        """Move to `position` (positive or negative).
        
        If ``scale==True``, assume that the position is in the physical units (see class description); otherwise, assume it is in the device internal units (steps).
        """
        self.send_comm_data(0x0453,struct.pack("<Hi",channel,self._p2d(position,"p",scale=scale)))
    @interface.use_parameters
    def _jog(self, direction, channel=1, kind="continuous"):
        """
        Jog in the given direction (``"+"`` or ``"-"``).
        
        If ``kind=="continuous"``, simply start motion in the given direction at the maximal speed
        until either the motor is stopped explicitly, or the limit is reached (this uses ``MOT_MOVE_VELOCITY`` command).
        If ``kind=="builtin"``, use the built-in ``MOT_MOVE_JOG`` command, whose parameters are specified by :meth:`get_jog_parameters`.
        """
        funcargparse.check_parameter_range(kind,"kind",["continuous","builtin"])
        _jog_fw=(self._forward_positive==bool(direction))
        comm=0x0457 if kind=="continuous" else 0x046A
        self.send_comm(comm,channel,1 if _jog_fw else 2)
    _moving_status=["moving_fw","moving_bk","jogging_fw","jogging_bk"]
    def _is_moving(self, channel=1):
        """Check if motion is in progress"""
        curr_status=self._get_status(channel=channel)
        return any([s in curr_status for s in self._moving_status])
    def _wait_move(self, channel=1, timeout=None):
        """Wait until motion command is done"""
        return self._wait_for_status(self._moving_status,False,channel=channel,timeout=timeout)

    def _stop(self, immediate=False, sync=True, channel=1, timeout=None):
        """
        Stop the motion.

        If ``immediate==True`` make an abrupt stop; otherwise, slow down gradually.
        If ``sync==True``, wait until the motion is stopped.
        """
        self.send_comm(0x0465,channel,1 if immediate else 2)
        if sync:
            self._wait_for_stop(channel=channel,timeout=timeout)
    def _wait_for_stop(self, channel=1, timeout=None):
        """Wait until motion or homing is done"""
        return self._wait_for_status(self._moving_status+["homing"],False,channel=channel,timeout=timeout)


    def _get_velocity_parameters(self, channel=1, scale=True):
        """
        Get current velocity parameters ``(min_velocity, acceleration, max_velocity)``
        
        If ``scale==True``, return values in the physical units (see class description); otherwise, return it in the device internal units.
        """
        data=self.query(0x0414,channel).data
        min_velocity,acceleration,max_velocity=struct.unpack("<iii",data[2:14])
        min_velocity=self._d2p(min_velocity,"v",scale=scale)
        acceleration=self._d2p(acceleration,"a",scale=scale)
        max_velocity=self._d2p(max_velocity,"v",scale=scale)
        return TVelocityParams(min_velocity,acceleration,max_velocity)
    def _setup_velocity(self, min_velocity=None, acceleration=None, max_velocity=None, channel=1, scale=True):
        """
        Set velocity parameters.
        
        If any parameter is ``None``, use the current value.
        If ``scale==True``, assume that the specified values are in the physical units (see class description); otherwise, assume it is in the device internal units.
        """
        current_parameters=self._get_velocity_parameters(channel=channel,scale=False)
        min_velocity=current_parameters.min_velocity if min_velocity is None else self._p2d(min_velocity,"v",scale=scale)
        acceleration=current_parameters.acceleration if acceleration is None else self._p2d(acceleration,"a",scale=scale)
        max_velocity=current_parameters.max_velocity if max_velocity is None else self._p2d(max_velocity,"v",scale=scale)
        data=struct.pack("<Hiii",channel,min_velocity,acceleration,max_velocity)
        self.send_comm_data(0x0413,data)
        return self._get_velocity_parameters(channel=channel,scale=scale)

    _p_jog_mode=interface.EnumParameterClass("jog_mode",{"continuous":1,"step":2})
    _p_stop_mode=interface.EnumParameterClass("jog_stop_mode",{"immediate":1,"profiled":2})
    @interface.use_parameters(_returns=["jog_mode",None,None,None,None,"jog_stop_mode"])
    def _get_jog_parameters(self, channel=1, scale=True):
        """
        Get current jog parameters ``(mode, step_size, min_velocity, acceleration, max_velocity, stop_mode)``
        
        If ``scale==True``, return values in the physical units (see class description); otherwise, return it in the device internal units.
        """
        data=self.query(0x0417,channel).data
        mode,step_size,min_velocity,acceleration,max_velocity,stop_mode=struct.unpack("<HiiiiH",data[2:22])
        step_size=self._d2p(step_size,"p",scale=scale)
        min_velocity=self._d2p(min_velocity,"v",scale=scale)
        acceleration=self._d2p(acceleration,"a",scale=scale)
        max_velocity=self._d2p(max_velocity,"v",scale=scale)
        return TJogParams(mode,step_size,min_velocity,acceleration,max_velocity,stop_mode)
    @interface.use_parameters(mode="jog_mode",stop_mode="jog_stop_mode")
    def _setup_jog(self, mode=None, step_size=None, min_velocity=None, acceleration=None, max_velocity=None, stop_mode=None, channel=1, scale=True):
        """
        Set jog parameters.
        
        If any parameter is ``None``, use the current value.
        If ``scale==True``, assume that the specified values are in the physical units (see class description); otherwise, assume it is in the device internal units.
        """
        current_parameters=self._wap._get_jog_parameters(channel=channel,scale=False)
        mode=current_parameters.mode if mode is None else mode
        step_size=current_parameters.step_size if step_size is None else self._p2d(step_size,"p",scale=scale)
        min_velocity=current_parameters.min_velocity if min_velocity is None else self._p2d(min_velocity,"v",scale=scale)
        acceleration=current_parameters.acceleration if acceleration is None else self._p2d(acceleration,"a",scale=scale)
        max_velocity=current_parameters.max_velocity if max_velocity is None else self._p2d(max_velocity,"v",scale=scale)
        stop_mode=current_parameters.stop_mode if stop_mode is None else stop_mode
        data=struct.pack("<HHiiiiH",channel,mode,step_size,min_velocity,acceleration,max_velocity,stop_mode)
        self.send_comm_data(0x0416,data)
        return self._get_jog_parameters(channel=channel,scale=scale)

    def _get_adc_inputs(self, channel=1, scale=True):
        """
        Get current adc input voltages ``(input1, input2)``.
        
        If ``scale==True``, return values in volts; otherwise, return in internal units (0 to 32768).
        """
        data=self.query(0x042B,channel).data
        input1,input2=struct.unpack("<HH",data[2:6])
        if scale:
            input1/=2**15/5.
            input2/=2**15/5.
        return (input1,input2)

    def _get_gen_move_parameters(self, channel=1, scale=True):
        """
        Get general move parameters parameters ``(backlash_distance)``
        
        If ``scale==True``, return values in the physical units (see class description); otherwise, return it in the device internal units.
        """
        data=self.query(0x043B,channel).data
        backlash_distance,=struct.unpack("<i",data[2:6])
        backlash_distance=self._d2p(backlash_distance,"p",scale=scale)
        return TGenMoveParams(backlash_distance)
    def _setup_gen_move(self, backlash_distance=None, channel=1, scale=True):
        """
        Set jog parameters.
        
        If any parameter is ``None``, use the current value.
        If ``scale==True``, assume that the specified value is in the physical units (see class description); otherwise, assume it is in the device internal units.
        """
        current_parameters=self._get_gen_move_parameters(channel=channel,scale=False)
        backlash_distance=current_parameters.backlash_distance if backlash_distance is None else self._p2d(backlash_distance,"p",scale=scale)
        data=struct.pack("<Hi",channel,backlash_distance)
        self.send_comm_data(0x043A,data)
        return self._get_gen_move_parameters(channel=channel,scale=scale)

    _p_home_direction=interface.EnumParameterClass("home_direction",{"forward":1,"reverse":2})
    _p_limit_switch=interface.EnumParameterClass("limit_switch",{"reverse":1,"forward":4})
    @interface.use_parameters(_returns=["home_direction","limit_switch",None,None])
    def _get_homing_parameters(self, channel=1, scale=True):
        """
        Get current homing parameters ``(home_direction, limit_switch, velocity, offset_distance)``
        
        If ``scale==True``, return values are in the physical units (see class description); otherwise, return it in the device internal units.
        """
        data=self.query(0x0441,channel).data
        home_direction,limit_switch,velocity,offset_distance=struct.unpack("<HHii",data[2:14])
        velocity=self._d2p(velocity,"v",scale=scale)
        offset_distance=self._d2p(offset_distance,"p",scale=scale)
        return THomeParams(home_direction,limit_switch,velocity,offset_distance)
    @interface.use_parameters
    def _setup_homing(self, home_direction=None, limit_switch=None, velocity=None, offset_distance=None, channel=1, scale=True):
        """
        Set homing parameters.
        
        If any parameter is ``None``, use the current value.
        If ``scale==True``, assume that the specified values are in the physical units (see class description); otherwise, assume it is in the device internal units.
        """
        current_parameters=self._wap._get_homing_parameters(channel=channel,scale=False)
        home_direction=current_parameters.home_direction if home_direction is None else home_direction
        limit_switch=current_parameters.limit_switch if limit_switch is None else limit_switch
        velocity=current_parameters.velocity if velocity is None else self._p2d(velocity,"v",scale=scale)
        offset_distance=current_parameters.offset_distance if offset_distance is None else self._p2d(offset_distance,"p",scale=scale)
        data=struct.pack("<HHHii",channel,home_direction,limit_switch,velocity,offset_distance)
        self.send_comm_data(0x0440,data)
        return self._get_homing_parameters(channel=channel,scale=scale)

    _p_hw_limit_kind=interface.EnumParameterClass("hw_limit_kind",{"ignore":1,"make":2,"break":3,"make_home":4,"break_home":5,"index_mark":6})
    _p_sw_limit_kind=interface.EnumParameterClass("sw_limit_kind",{"ignore":1,"stop_imm":2,"stop_prof":3})
    @interface.use_parameters(_returns=["hw_limit_kind","hw_limit_kind",None,None,None,"sw_limit_kind"])
    def _get_limit_switch_parameters(self, channel=1, scale=True):
        """
        Get current limit switch parameters ``(hw_kind_cw, hw_kind_ccw, hw_flipped, sw_position_cw, sw_position_ccw, sw_kind)``
        
        If ``scale==True``, return values in the physical units (see class description); otherwise, return it in the device internal units (steps).
        """
        data=self.query(0x0424,channel).data
        hw_kind_cw,hw_kind_ccw,sw_position_cw,sw_position_ccw,sw_kind=struct.unpack("<HHiiH",data[2:16])
        swapped_cw=bool(hw_kind_cw&0x80)
        swapped_ccw=bool(hw_kind_ccw&0x80)
        if swapped_cw!=swapped_ccw:
            warnings.warn("swapped bit is different for the two axes; assume that the switches are not swapped")
        sw_position_cw=self._d2p(sw_position_cw,"p",scale=scale)
        sw_position_ccw=self._d2p(sw_position_ccw,"p",scale=scale)
        return TLimitSwitchParams(hw_kind_cw&0x7F,hw_kind_ccw&0x7F,swapped_cw,sw_position_cw,sw_position_ccw,sw_kind&0x7F)
    @interface.use_parameters(hw_kind_cw="hw_limit_kind",hw_kind_ccw="hw_limit_kind",sw_kind="sw_limit_kind")
    def _setup_limit_switch(self, hw_kind_cw=None, hw_kind_ccw=None, hw_swapped=None, sw_position_cw=None, sw_position_ccw=None, sw_kind=None, channel=1, scale=True):
        """
        Set home parameters.
        
        If any parameter is ``None``, use the current value.
        If ``scale==True``, assume that the specified values are in the physical units (see class description); otherwise, assume it is in the device internal units (Steps).
        """
        current_parameters=self._wap._get_limit_switch_parameters(channel=channel,scale=False)
        hw_kind_cw=current_parameters.hw_kind_cw if hw_kind_cw is None else hw_kind_cw
        hw_kind_ccw=current_parameters.hw_kind_ccw if hw_kind_ccw is None else hw_kind_ccw
        if hw_swapped is not None:
            hw_kind_cw=(hw_kind_cw&0x7F)|(0x80 if hw_swapped else 0x00)
            hw_kind_ccw=(hw_kind_ccw&0x7F)|(0x80 if hw_swapped else 0x00)
        sw_position_cw=current_parameters.sw_position_cw if sw_position_cw is None else self._p2d(sw_position_cw,"p",scale=scale)
        sw_position_ccw=current_parameters.sw_position_ccw if sw_position_ccw is None else self._p2d(sw_position_ccw,"p",scale=scale)
        sw_kind=current_parameters.sw_kind if sw_kind is None else sw_kind
        data=struct.pack("<HHHiiH",channel,hw_kind_cw,hw_kind_ccw,sw_position_cw,sw_position_ccw,sw_kind)
        self.send_comm_data(0x0423,data)
        return self._get_limit_switch_parameters(channel=channel,scale=scale)









TFlipperParameters=collections.namedtuple("TFlipperParameters",["transit_time","io1_oper_mode","io1_sig_mode","io1_pulse_width","io2_oper_mode","io2_sig_mode","io2_pulse_width"])
class MFF(KinesisDevice):
    """
    MFF (Motorized Filter Flip Mount) device.

    Implements FTDI chip connectivity via pyft232 (virtual serial interface).

    Args:
        conn: serial connection parameters (usually 8-digit device serial number).
    """
    def __init__(self, conn):
        KinesisDevice.__init__(self,conn)
        self._add_settings_variable("state",self.get_state,self.move_to_state)

    get_status_n=KinesisDevice._get_status_n
    get_status=KinesisDevice._get_status
    wait_for_status=KinesisDevice._wait_for_status
    
    def move_to_state(self, state, channel=0):
        """Move to the given flip mount state (either 0 or 1)"""
        self.send_comm(0x046A,channel,2 if state else 1)
    def get_state(self, channel=0):
        """
        Get the flip mount state (either 0 or 1).

        Return ``None`` if the mount is current moving (i.e., the state os undefined)
        """
        status=self.get_status_n(channel=channel)
        if status&0x01: # low limit
            return 0
        if status&0x02: # high limit
            return 1
        if status&0x2F0: # moving
            return None
        raise ThorlabsError("error getting MFF position: status {:08x}".format(status))

    _p_io_oper_mode=interface.EnumParameterClass("io_oper_mode",{"in_toggle":1,"in_position":2,"out_position":3,"out_motion":4})
    _p_io_sig_mode=interface.EnumParameterClass("io_sig_mode",{"in_button":0x01,"in_voltage":0x02,"in_button_inf":0x05,"in_voltage_inv":0x06,
                                                                "out_edge":0x10,"out_pulse":0x20,"out_edge_inv":0x50,"out_pulse_inv":0x60})
    @interface.use_parameters(_returns=[None,"io_oper_mode","io_sig_mode",None,"io_oper_mode","io_sig_mode",None])
    def get_flipper_parameters(self, channel=1):
        """
        Get current flipper parameters ``(transit_time, io1_oper_mode, io1_sig_mode, io1_pulse_width, io2_oper_mode, io2_sig_mode, io2_pulse_width)``
        
        ``transit_time`` specifies transit time (in seconds between 0.3 and 2.8);
        ``io*_oper_mode`` specifies operation mode (in vs. out and position vs. motion input/indication),
        ``io*_sig_mode`` specifies signal mode (button input, voltage edge input, edge output or pulse output).
        ``io*_pulse_width`` specifies output pulse width if the corresponding output mode is selected.
        For detailed mode description, see the flip mirror or APT manual.
        """
        data=self.query(0x0511,channel).data
        transit_time,_,io1_oper_mode,io1_sig_mode,io1_pulse_width,io2_oper_mode,io2_sig_mode,io2_pulse_width=struct.unpack("<iiHHiHHi",data[2:26])
        return TFlipperParameters(transit_time*1E-3,io1_oper_mode,io1_sig_mode,io1_pulse_width*1E-3,io2_oper_mode,io2_sig_mode,io2_pulse_width*1E-3)
    @interface.use_parameters(io1_oper_mode="io_oper_mode",io1_sig_mode="io_sig_mode",io2_oper_mode="io_oper_mode",io2_sig_mode="io_sig_mode")
    def setup_flipper(self, transit_time=None, io1_oper_mode=None, io1_sig_mode=None, io1_pulse_width=None, io2_oper_mode=None, io2_sig_mode=None, io2_pulse_width=None, channel=1):
        """
        Set flipper parameters.
        
        ``transit_time`` specifies transit time (in seconds between 0.3 and 2.8);
        ``io*_oper_mode`` specifies operation mode (in vs. out and position vs. motion input/indication),
        ``io*_sig_mode`` specifies signal mode (button input, voltage edge input, edge output or pulse output).
        ``io*_pulse_width`` specifies output pulse width if the corresponding output mode is selected.
        If any parameter is ``None``, use the current value.
        For detailed mode description, see the flip mirror or APT manual.
        """
        current_parameters=self._wap.get_flipper_parameters(channel=channel)
        transit_time=current_parameters.transit_time if transit_time is None else transit_time
        transit_time=int(transit_time*1E3)
        transit_time_adc=int(1E7*transit_time**-1.591)
        io1_oper_mode=current_parameters.io1_oper_mode if io1_oper_mode is None else io1_oper_mode
        io1_sig_mode=current_parameters.io1_sig_mode if io1_sig_mode is None else io1_sig_mode
        io1_pulse_width=current_parameters.io1_pulse_width if io1_pulse_width is None else io1_pulse_width
        io1_pulse_width=int(io1_pulse_width*1E3)
        io2_oper_mode=current_parameters.io2_oper_mode if io2_oper_mode is None else io2_oper_mode
        io2_sig_mode=current_parameters.io2_sig_mode if io2_sig_mode is None else io2_sig_mode
        io2_pulse_width=current_parameters.io2_pulse_width if io2_pulse_width is None else io2_pulse_width
        io2_pulse_width=int(io2_pulse_width*1E3)
        data=struct.pack("<HiiHHiHHi",channel,transit_time,transit_time_adc,io1_oper_mode,io1_sig_mode,io1_pulse_width,io2_oper_mode,io2_sig_mode,io2_pulse_width)
        self.send_comm_data(0x0510,data+b"\x00"*8)
        return self.get_flipper_parameters(channel=channel)


    


class KinesisMotor(KinesisDevice):
    """
    Thorlabs motor controller.

    Implements FTDI chip connectivity via pyft232 (virtual serial interface).

    The physical units are encoder steps for position (ratio to m or degrees depends on the connected stage),
    steps/sec for velocity, and steps/sec^2 for acceleration.

    Args:
        conn(str): serial connection parameters (usually an 8-digit device serial number).
        scale: scale of the position, velocity, and acceleration units to the internals units;
            can be ``"stage"`` (attempt to autodetect motor and stage parameters),
            a string with the name of the stage, e.g., ``"MTS50-Z8"`` or ``"DDR100"``
            (use the stage name to extract the scale; determine velocity and acceleration from this scale and the motor model),
            ``"step"`` (use encoder/motor steps as units; determine velocity and acceleration from this scale and the motor model),
            a single number (use this as the ratio of internal steps to physical units; determine velocity and acceleration from this scale and the motor model),
            or a 3-tuple of numbers ``(position_scale, velocity_scale, acceleration_scale)`` which gives the ratio of internal units to physical units
            (useful for new or unrecognized controllers or stages, as no autodetection is required);
            in the case of unrecognized devices, use internal units (same as setting ``scale=(1,1,1)``);
            if the scale can't be autodetected, it can be obtained from the APT manual knowing the device and the stage model
    """
    def __init__(self, conn, scale="step"):
        KinesisDevice.__init__(self,conn)
        self.add_background_comm(0x0464) # move completed
        self.add_background_comm(0x0466) # move stopped
        self.add_background_comm(0x0444) # homed
        self._add_info_variable("scale_units",self.get_scale_units)
        self._add_info_variable("scale",self.get_scale)
        self._add_info_variable("stage",self.get_stage)
        self._add_status_variable("position",self.get_position)
        self._add_status_variable("status",self.get_status)
        self._add_settings_variable("velocity_parameters",self.get_velocity_parameters,self.setup_velocity)
        self._add_settings_variable("jog_parameters",self.get_jog_parameters,self.setup_jog)
        self._add_settings_variable("homing_parameters",self.get_homing_parameters,self.setup_homing)
        self._add_settings_variable("gen_move_parameters",self.get_gen_move_parameters,self.setup_gen_move)
        self._add_settings_variable("limit_switch_parameters",self.get_limit_switch_parameters,self.setup_limit_switch)
        self._stage=self._get_stage(scale)
        self._scale,self._scale_units=self._calculate_scale(scale)
    
    def _autodetect_stage(self, model):
        info=self.query(0x0005).data
        stage_id,=struct.unpack("<H",info[76:78])
        if model in ["KDC101","TDC101","ODC001"]:
            stages={2:"Z706",3:"Z712",4:"Z725",5:"CR1-Z7",6:"PRM1-Z8",
                    7:"MTS25-Z8",8:"MTS50-Z8",9:"Z825",10:"Z812",11:"Z806"}
            return stages.get(stage_id,None)
        if model=="K10CR1":
            return "K10CR1"
        return None
    def _get_stage(self, scale):
        model=self.get_device_info().model_no
        if scale=="stage":
            return self._autodetect_stage(model)
        return scale if isinstance(scale,py3.textstring) else None
    def _get_step_scale(self, model, stage):
        if stage is None:
            warnings.warn("can't recognize the stage; assuming step scale of 1")
            return 1,None
        stage=stage.strip().upper()
        if stage=="STEP":
            return 1,"step"
        if stage in {"MTS25-Z8","MTS50-Z8","Z806","Z812","Z825"}:
            return 34304E3,"m"
        if stage in {"Z606","Z612","Z625"}:
            return 24600E3,"m"
        if stage in {"PRM1-Z8","PRM1TZ8"}:
            return 1919.6418578623391E3,"m" # that's what it says in the manual...
        if stage in {"CR1-Z7"}:
            return 12288E3,"m"
        if stage in {"DDSM50","DDSM100"}:
            return 2000E3,"m"
        if stage in {"DDS220","DDS300","DDS600","MLS203"}:
            return 20000E3,"m"
        if stage=="DDR100":
            return 3276800/360,"deg"
        if stage=="DDR05":
            return 2000000/360,"deg"
        if stage=="DDR25":
            return 1440000/360,"deg"
        if stage=="HDR50":
            return 75091/0.99997,"deg"
        if model in ["TST001","MST601"] or model.startswith("BSC00") or model.startswith("BSC10"):
            if stage.startswith("ZST"):
                return 125540.35E3,"m"
            if stage.startswith("ZFS"):
                return 136533.33E3,"m"
            if stage=="DRV001":
                return 51200E3,"m"
            if stage in {"DRV013","DRV014","NRT100","NRT150","LTS150","LTS300"}:
                return 25600E3,"m"
            if stage in {"DRV113","DRV114"}:
                return 20480E3,"m"
            if stage=="FW103":
                return 25600/360,"deg"
            if stage=="NR360":
                return 25600/(360/66),"deg"
        if model in ["TST101","KST101","MST602","K10CR1"] or model.startswith("BSC20"):
            if stage.startswith("ZST"):
                return 2008645.63E3,"m"
            if stage.startswith("ZFS"):
                return 2184533.33E3,"m"
            if stage=="DRV001":
                return 819200E3,"m"
            if stage in {"DRV013","DRV014","NRT100","NRT150","LTS150","LTS300"}:
                return 409600E3,"m"
            if stage in {"DRV113","DRV114"}:
                return 327680E3,"m"
            if stage=="FW103":
                return 409600/360,"deg"
            if stage=="NR360":
                return 409600/(360/66),"deg"
            if stage=="K10CR1":
                return 409600/3,"deg"
        warnings.warn("can't recognize the stage name {}; assuming step scale of 1".format(stage))
        return 1,"step"
    def _calculate_scale(self, scale):
        if isinstance(scale,tuple):
            return scale,"user"
        model=self.get_device_info().model_no
        if scale is None:
            scale=self._autodetect_stage(model)
        if isinstance(scale,py3.textstring) or scale is None:
            ssc,units=self._get_step_scale(model,scale)
        else:
            ssc,units=scale,"user_step"
        if model in ["KDC101","TDC101"]:
            time_conv=2048/6E6
            return (ssc,ssc*time_conv*2**16,ssc*time_conv**2*2**16),units
        if model in ["TBD001","KBD101"] or model.startswith("BBD10") or model.startswith("BBD20"):
            time_conv=102.4E-6
            return (ssc,ssc*time_conv*2**16,ssc*time_conv**2*2**16),units
        if model in ["TST001","MST601"] or model.startswith("BSC00") or model.startswith("BSC10"):
            return (ssc,ssc,ssc),units
        if model in ["TST101","KST101","MST602","K10CR1"] or model.startswith("BSC20"):
            vpr=53.68
            avr=204.94E-6
            return (ssc,ssc*vpr,ssc*vpr*avr),units
        warnings.warn("can't recognize motor model {}; setting all scales to internal units".format(model))
        return (1,1,1),"internal"
    def _get_scale(self):
        """
        Get the scaling coefficients.
        
        Return a tuple ``(position_scale, velocity_scale, acceleration_scale)`` for scaling of the physical units in terms of internal units.
        To get the coefficients source and physical units, use :meth:`get_scale_units`.
        """
        return self._scale
    get_scale=_get_scale
    def get_scale_units(self):
        """
        Get units used for calculating scaled position, velocity and acceleration values.

        Can be ``"deg"`` (autodetected rotational stage: deg, deg/s and deg/s^2),
        ``"m"`` (autodetected translational stage: m, m/sec and m/sec^2),
        ``"step"`` (autodetected driver but not detected step scale: steps, steps/sec and steps/sec^2)
        ``"user_step"`` (autodetected driver and user supplied step scale: user-supplied step scale for position,
        same units per sec or sec^2 for velocity and acceleration), ``'user"`` (all three scales are supplied by user),
        or ``"internal"`` (no scales are supplied or detected, use device internal units)
        """
        return self._scale_units
    def get_stage(self):
        """
        Return the name of the stage which was supplied by the usr or autodetected.

        If the stake is unknown, return ``None``
        """
        return self._stage

    get_status_n=KinesisDevice._get_status_n
    get_status=KinesisDevice._get_status
    wait_for_status=KinesisDevice._wait_for_status

    home=KinesisDevice._home
    is_homing=KinesisDevice._is_homing
    is_homed=KinesisDevice._is_homed
    wait_for_home=KinesisDevice._wait_for_home

    get_position=KinesisDevice._get_position
    set_position_reference=KinesisDevice._set_position_reference
    move_by=KinesisDevice._move_by
    move_to=KinesisDevice._move_to
    jog=KinesisDevice._jog
    is_moving=KinesisDevice._is_moving
    wait_move=KinesisDevice._wait_move
    stop=KinesisDevice._stop
    wait_for_stop=KinesisDevice._wait_for_stop

    get_velocity_parameters=KinesisDevice._get_velocity_parameters
    setup_velocity=KinesisDevice._setup_velocity
    get_jog_parameters=KinesisDevice._get_jog_parameters
    setup_jog=KinesisDevice._setup_jog
    get_homing_parameters=KinesisDevice._get_homing_parameters
    setup_homing=KinesisDevice._setup_homing
    get_gen_move_parameters=KinesisDevice._get_gen_move_parameters
    setup_gen_move=KinesisDevice._setup_gen_move
    get_limit_switch_parameters=KinesisDevice._get_limit_switch_parameters
    setup_limit_switch=KinesisDevice._setup_limit_switch