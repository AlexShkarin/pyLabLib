from ...core.devio import interface, comm_backend
from ...core.utils import general, funcargparse, py3
from .base import ThorlabsError, ThorlabsTimeoutError, ThorlabsBackendError

from ..interface.stage import IMultiaxisStage, muxaxis

import struct
import warnings
import contextlib

import re
import time

import collections



def list_kinesis_devices(filter_ids=True):
    """
    List all Thorlabs APT/Kinesis devices connected to this PC.

    Return list of tuples ``(conn, description)``.
        If ``filter_ids==True``, only leave devices with Thorlabs-like IDs (8-digit numbers).
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
        is_rack_system: specify whether the device is a rack system or a standalone USB device (default mode).
    """
    Error=ThorlabsError
    def __init__(self, conn, timeout=3., is_rack_system=False):
        defaults={"serial":{"baudrate":115200,"rtscts":True}, "ft232":{"baudrate":115200,"rtscts":True}}
        instr=comm_backend.new_backend(conn,backend=("auto","ft232"),term_write=b"",term_read=b"",timeout=timeout,
            defaults=defaults,reraise_error=ThorlabsBackendError)
        instr.setup_cooldown(write=0.003)
        try:
            self._cycle_rts(instr)
        except ThorlabsBackendError:
            instr.close()
            raise
        super().__init__(instr)
        self._add_info_variable("device_info",self.get_device_info)
        self._bg_msg_counters={}
        self._is_rack_system=is_rack_system

    @staticmethod
    def _cycle_rts(instr):
        be=instr.get_backend_name()
        if be=="ft232":
            instr.instr._flow=256  # SIO_RTS_CTS_HS
            instr.instr._setFlowControl()
            time.sleep(0.05)
            instr.instr.flushInput()
            instr.instr.flushOutput()
            time.sleep(0.05)
            instr.instr._flow=0
            instr.instr._setFlowControl()
            time.sleep(0.05)
        elif be=="serial":
            instr.instr.setRTS(1)
            time.sleep(0.05)
            instr.instr.flushInput()
            instr.instr.flushOutput()
            time.sleep(0.05)
            instr.instr.setRTS(0)
            time.sleep(0.05)
        else:
            warnings.warn("could not cycle RTS with backend '{}'; some devices might not work properly".format(be))
    def _make_dest(self, dest):
        if dest=="host":
            return 0x11 if self._is_rack_system else 0x50
        if isinstance(dest,tuple) and len(dest)==2 and dest[0]=="channel":
            return 0x20+dest[1] if self._is_rack_system else 0x50
        return dest
    def _make_channel(self, channel):
        return channel if not self._is_rack_system else 1
    def _find_bays(self):
        return [b for b in range(10) if self.query(0x0060,b).param2==0x01]
    @staticmethod
    def list_devices(filter_ids=True):
        """
        List all connected devices.

        Return list of tuples ``(conn, description)``.
        If ``filter_ids==True``, only leave devices with Thorlabs-like IDs (8-digit numbers).
        Otherwise, show all devices (some of them might not be Thorlabs-related).
        """
        def _is_thorlabs_id(did):
            return re.match(r"^\d{8,}$",did[0]) is not None
        ids=comm_backend.FT232DeviceBackend.list_resources(desc=True)
        if filter_ids:
            ids=[did for did in ids if _is_thorlabs_id(did)]
        return ids
    def send_comm(self, messageID, param1=0x00, param2=0x00, source=0x01, dest="host"):
        """
        Send a message with no associated data.

        For details, see APT communications protocol.
        """
        msg=struct.pack("<HBBBB",messageID,param1,param2,self._make_dest(dest),source)
        self.instr.write(msg)
    def send_comm_data(self, messageID, data, source=0x01, dest="host"):
        """
        Send a message with associated data.

        For details, see APT communications protocol.
        """
        msg=struct.pack("<HHBB",messageID,len(data),self._make_dest(dest)|0x80,source)
        self.instr.write(msg+data)

    CommShort=collections.namedtuple("CommShort",["messageID","param1","param2","source","dest"])
    CommData=collections.namedtuple("CommData",["messageID","data","source","dest"])
    def recv_comm(self, expected_id=None, timeout=None):
        """
        Receive a message.

        Return either :class:`BasicKinesisDevice.CommShort` or :class:`BasicKinesisDevice.CommData` depending on the message type
        (fixed length with two parameters, or variable length with associated data).
        If `expected_id` is not ``None`` and the received message ID is different from `expected_id`, raise an error.
        If `timeout` is not ``None``, it can specify the timeout to read the command header (the rest is done with the usual timeout).
        For details, see APT communications protocol.
        """
        while True:
            with self.instr.using_timeout(timeout):
                b=self.instr.read(1)
            msg=b+self.instr.read(5)
            messageID,_,dest,source=struct.unpack("<HHBB",msg[:6])
            if dest&0x80:
                dest=dest&0x7F
                datalen,=struct.unpack("<H",msg[2:4])
                data=self.instr.read(datalen)
                comm=self.CommData(messageID,data,source,dest)
            else:
                param1,param2=struct.unpack("<BB",msg[2:4])
                comm=self.CommShort(messageID,param1,param2,source,dest)
            if messageID in self._bg_msg_counters and messageID!=expected_id:
                cnt,_=self._bg_msg_counters[messageID]
                self._bg_msg_counters[messageID]=(cnt+1,comm)
            else:
                if expected_id is not None and messageID!=expected_id:
                    raise ThorlabsError("unexpected command received: expected 0x{:04x}, got 0x{:04x}".format(expected_id,messageID))
                return comm
    def flush_comm(self, nmax=1000):
        """
        Flush any commands in the queue.

        if `nmax` is not ``None``, it specifies the maximal number of commands to flush.
        """
        comms=[]
        try:
            while True:
                comms.append(self.recv_comm(timeout=0))
                if nmax is not None and len(comms)>=nmax:
                    break
        except self.instr.Error:
            pass
        return comms
    def query(self, messageID, param1=0, param2=0, source=0x01, dest="host", replyID=-1, flush="auto"):
        """
        Send a query to the device and receive the reply.

        A combination of :meth:`send_comm` and :meth:`recv_comm`.
        If `replyID` is not ``None``, specifies the expected reply message ID; if -1 (default), set to te be ``messageID+1`` (the standard convention).
        `flush` specifies whether input queue will be flushed before reading; ``"auto"`` means that it will be flushed if the expected reply is among the background
        messages, i.e., it could be already present in the queue.
        """
        if replyID<0:
            replyID=messageID+1
        if flush=="auto":
            flush=replyID in self._bg_msg_counters
        if flush:
            self.flush_comm()
        self.send_comm(messageID,param1=param1,param2=param2,source=source,dest=dest)
        return self.recv_comm(expected_id=replyID)
    def add_background_comm(self, messageID):
        """
        Mark given messageID as a 'background' message, which can be sent at any point without prompt (e.g., some operation confirmation).

        If it is received instead during ``recv_comm_`` operations, it is ignored, and the corresponding counter is increased.
        """
        self._bg_msg_counters.setdefault(messageID,(0,None))
    def check_background_comm(self, messageID):
        """Return message counter and the last message value (``None`` if not message received yet) of a given 'background' message"""
        return self._bg_msg_counters[messageID]

    _device_SN={   20:"BSC001", 21:"BPC001", 22:"BNT001", 25:"BMS001", 26:"KST101", 27:"KDC101", 28:"KBD101", 29:"KPZ101",
                    30:"BSC002", 31:"BPC002", 33:"BDC101", 35:"BMS002", 37:"MFF10." ,
                    40:"(BSC101|SSC201)", 41:"BPC101", 43:"BDC101", 44:"PPC001", 45:"LTS", 48:"MMR", 49:"MLJ",
                    50:"MST60" , 51:"MPZ601", 52:"MNA601", 55:"K10CR1", 56:"KLS101", 57:"KNA101", 59:"KSG101",
                    60:"0ST001", 63:"ODC001", 64:"TLD001", 65:"TIM001", 67:"TBD001", 68:"KSC101", 69:"KPA101",
                    70:"BSC.03", 71:"BPC.03", 72:"BPS103", 73:"BBD103", 
                    80:"TST001", 81:"TPZ001", 82:"TNZ001", 83:"TDC001", 84:"TSG001", 85:"TSC001", 86:"TLS001", 87:"TTC001", 89:"TQD001", 
                    90:"SCC101", 91:"PCC101", 93:"DCC101", 94:"BCC101", 95:"PPC102", 96:"PCC102"}
    def _get_device_model(self):
        addr=str(self._connection_parameters.get("port",""))
        if len(addr)==8 and addr.isdigit():
            msn=int(addr[:2])
            return msn,self._device_SN.get(msn,None)
        return None,None
    def _model_match(self, model_no, port_model_no):
        if port_model_no is None:
            return True
        if model_no.startswith(port_model_no):
            return True
        for model in port_model_no.split("|"):
            if re.match("^"+port_model_no+"$",model_no):
                return True
        return False
    def get_device_info(self, dest="host"):
        """
        Get device info.

        Return tuple ``(serial_no, model_no, fw_ver, hw_type, hw_ver, mod_state, nchannels, notes)``.
        """
        data=self.query(0x0005,dest=dest).data
        serial_no,=struct.unpack("<I",data[:4])
        model_no=data[4:12].decode().strip("\x00").strip()
        port,port_model_no=self._get_device_model()
        if not self._model_match(model_no,port_model_no):
            warnings.warn("model number {} doesn't match the device ID prefix {}({})".format(model_no,port,port_model_no))
        fw_ver="{}.{}.{}".format(*struct.unpack("<BBB",data[14:17])[::-1])
        hw_type,=struct.unpack("<H",data[12:14])
        hw_ver,mod_state,nchannels=struct.unpack("<HHH",data[78:84])
        notes=py3.as_str(data[18:64]).strip("\x00").strip()
        return TDeviceInfo(serial_no,model_no,fw_ver,hw_type,hw_ver,mod_state,nchannels,notes)
    def get_number_of_channels(self):
        """Get number of channels on the device"""
        return self.get_device_info().nchannels

    def blink(self, channel=1, dest="host"):
        """Identify the physical device (by, e.g., blinking status LED or screen)"""
        self.send_comm(0x0223,channel,dest=dest)










TVelocityParams=collections.namedtuple("TVelocityParams",["min_velocity","acceleration","max_velocity"])
TJogParams=collections.namedtuple("TJogParams",["mode","step_size","min_velocity","acceleration","max_velocity","stop_mode"])
TGenMoveParams=collections.namedtuple("TGenMoveParams",["backlash_distance"])
THomeParams=collections.namedtuple("THomeParams",["home_direction","limit_switch","velocity","offset_distance"])
TPolCtlParams=collections.namedtuple("TPolCtlParams",["velocity","home_position","jog1","jog2","jog3"])
TLimitSwitchParams=collections.namedtuple("TLimitSwitchParams",["hw_kind_cw","hw_kind_ccw","hw_swapped","sw_position_cw","sw_position_ccw","sw_kind"])
TKCubeTrigIOParams=collections.namedtuple("TKCubeTrigIOParams",["trig1_mode","trig1_pol","trig2_mode","trig2_pol"])
TKCubeTrigPosParams=collections.namedtuple("TKCubeTrigPosParams",["start_fw","step_fw","num_fw","start_bk","step_bk","num_bk","width","ncycles"])
TPZMotorDriveParams=collections.namedtuple("TPZMotorDriveParams",["max_voltage","velocity","acceleration"])
TPZMotorJogParams=collections.namedtuple("TPZMotorJogParams",["mode","step_size_fw","step_size_bk","velocity","acceleration"])
muxchannel=lambda *args,**kwargs: muxaxis(*args,argname="channel",**kwargs)
class KinesisDevice(IMultiaxisStage,BasicKinesisDevice):
    """
    Overarching Kinesis class containing all of the necessary private methods.

    Subclasses are expected to make some of them visible by renaming, and to define device variables and opening behavior accordingly.

    Args:
        conn: serial connection parameters (usually an 8-digit device serial number).
        timeout: device communication timeout.
        default_channel: starting default channel used when no channel is supplied to a channel-level command (such as ``move_to`` or ``get_position``).
        is_rack_system: specify whether the device is a rack system or a standalone USB device (default mode).
    """
    def __init__(self, conn, timeout=3., default_channel=1, is_rack_system=False):
        super().__init__(conn,timeout=timeout,is_rack_system=is_rack_system,default_axis=default_channel)
        self._remove_device_variable("axes")
        self._add_info_variable("channel",self.get_all_channels)
        with self._close_on_error():
            self._model=self.get_device_info().model_no
            self._setup_comm_parameters()
    _axes=[1]
    def get_all_channels(self):
        """Get the list of all available channels; alias of ``get_all_axes`` method"""
        return super().get_all_axes()
    def set_default_channel(self, channel):
        """Set the default channel for all channel-related methods"""
        self._default_axis=channel
    @contextlib.contextmanager
    def using_channel(self, channel):
        """Context manager for temporarily using a different default channel"""
        current_channel=self._default_axis
        self._default_axis=channel
        try:
            yield
        finally:
            self._default_axis=current_channel
    def _set_supported_channels(self, channels=1):
        """
        Set the channels in the device.

        Can be either a list of channels, a single number defining the number of channels numbered from 1 to ``channels`` (inclusive).
        """
        if not isinstance(channels,list):
            channels=list(range(1,channels+1))
        self._update_axes(channels)
    def _setup_comm_parameters(self, status_comm="auto", move_by_mode="auto"):
        """
        Setup miscellaneous communication parameters.

        `status_comm` is the status request command; can be ``0x0480``, ``0x0490``, ``0x0429``, or ``"auto"`` (autodetect based on the model number).
        `move_by_mode` is the mode of ``move_by`` method; can be ``"builtin"`` (use built-in method),
        ``"move_to"`` (use position readout and ``move_to``), or ``"auto"`` (autodetect based on the model number).
        """
        if status_comm=="auto":
            status_comm=0x0490 if self._model.startswith("MPC") else 0x0429
        self._status_comm=status_comm
        if move_by_mode=="auto":
            move_by_mode="move_to" if self._model.startswith("MPC") else "builtin"
        self._move_by_mode=move_by_mode

    @muxchannel
    def _get_status_n(self, channel=None):
        """
        Get numerical status of the device.

        For details, see APT communications protocol.
        """
        data=self.query(self._status_comm,self._make_channel(channel),dest=("channel",channel)).data
        status_bits=data[16:20] if self._status_comm==0x0480 else data[-4:]
        return struct.unpack("<I",status_bits)[0]
    status_bits=[(1<<0,"hw_bk_lim"),(1<<1,"hw_fw_lim"),(1<<2,"sw_bk_lim"),(1<<3,"sw_fw_lim"),
                (1<<4,"moving_bk"),(1<<5,"moving_fw"),(1<<6,"jogging_bk"),(1<<7,"jogging_fw"),
                (1<<8,"connected"),(1<<9,"homing"),(1<<10,"homed"),(1<<11,"initializing"),(1<<12,"tracking"),(1<<13,"settled"),
                (1<<14,"motion_error"),(1<<15,"instr_error"),(1<<16,"interlock"),(1<<17,"overtemp"),(1<<18,"volt_supply_fault"),(1<<19,"commutation_error"),
                (1<<20,"digio1"),(1<<21,"digio2"),(1<<22,"digio3"),(1<<23,"digio4"),
                (1<<24,"current_limit"),(1<<25,"encoder_fault"),(1<<26,"overcurrent"),(1<<27,"curr_supply_fault"),
                (1<<28,"power_ok"),(1<<29,"active"),(1<<30,"error"),(1<<31,"enabled")]
    @muxchannel
    def _get_status(self, channel=None):
        """
        Get device status.

        Return list of status strings, which can include ``"hw_fw_lim"`` (forward hardware limit switch reached), ``"hw_bk_lim"`` (backward hardware limit switch reached),
        ``"sw_fw_lim"`` (forward software limit switch reached), ``"sw_bk_lim"`` (backward software limit switch reached),
        ``"moving_fw"`` (moving forward), ``"moving_bk"`` (moving backward), ``"jogging_fw"`` (jogging forward), ``"jogging_bk"`` (jogging backward),
        ``"connected"`` (motor is connected), ``"homing"`` (homing), ``"homed"`` (homing done), ``"initializing"`` (3-phase motor phase initialization),
        ``"tracking"`` (position is within trajectory), ``"settled"`` (position has been stable),
        ``"motion_error"`` (excessive position error), ``"instr_error"`` (legacy instrument command error), ``"interlock"`` (interlock is on), ``"overtemp"`` (temperature above limit),
        ``"volt_supply_fault"`` (supply voltage is too low), ``"commutation_error"`` (3-phase motor commutation error),
        ``"digio1"`` (state of digital input 1), ``"digio2"`` (state of digital input 2), ``"digio3"`` (state of digital input 3), ``"digio4"`` (state of digital input 4),
        ``"current_limit"`` (motor current limit exceeded for a long time), ``"encoder_fault"`` (encoder problems), ``"overcurrent"`` (motor current limit exceeded temporarily),
        ``"curr_supply_fault"`` (current drawn from supply is too high), ``"power_ok"`` (power is ok), ``"active"`` (moving), ``"error"`` (any error), ``"enabled"`` (motor is enabled).
        """
        status_n=self._get_status_n(channel=channel)
        return [s for (m,s) in self.status_bits if status_n&m]
    _default_get_status=_get_status
    @muxchannel
    def _wait_for_status(self, status, enabled, channel=None, timeout=None, period=0.05):
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
            curr_status=self._default_get_status(channel=channel)
            if enabled and any([s in curr_status for s in status]):
                return
            if (not enabled) and all([s not in curr_status for s in status]):
                return
            if ctd.passed():
                raise ThorlabsTimeoutError
            time.sleep(period)

    @muxchannel
    def _home(self, sync=True, force=False, channel=None, timeout=None):
        """
        Home the device.

        If ``sync==True``, wait until homing is done (with the given timeout).
        If ``force==False``, only home if the device isn't homed already.
        """
        if self._is_homed() and not force:
            return
        self.send_comm(0x0443,self._make_channel(channel),dest=("channel",channel))
        if sync:
            self._wait_for_home(channel=channel,timeout=timeout)
    @muxchannel
    def _is_homing(self, channel=None):
        """Check if homing is in progress"""
        return "homing" in self._default_get_status(channel=channel)
    @muxchannel
    def _is_homed(self, channel=None):
        """Check if the device is homed"""
        return "homed" in self._default_get_status(channel=channel)
    def _wait_for_home(self, channel=None, timeout=None):
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
    @muxchannel
    def _get_position(self, channel=None, scale=True):
        """
        Get current position.
        
        If ``scale==True``, return value in the physical units (see class description); otherwise, return it in the device internal units (steps).
        """
        data=self.query(0x0490 if self._status_comm==0x0490 else 0x0411,self._make_channel(channel),dest=("channel",channel)).data
        pos=struct.unpack("<i",data[2:6])[0]
        return self._d2p(pos,"p",scale=scale)
    @muxchannel(mux_argnames="position")
    def _set_position_reference(self, position=0, channel=None, scale=True):
        """
        Set position reference (actual motor position stays the same).
        
        If ``scale==True``, assume that the position is in the physical units (see class description); otherwise, assume it is in the device internal units (steps).
        """
        self.send_comm_data(0x0410,struct.pack("<Hi",self._make_channel(channel),self._p2d(position,"p",scale=scale)),dest=("channel",channel))
        return self._get_position(channel=channel)
    @muxchannel(mux_argnames="distance")
    def _move_by(self, distance=1, channel=None, scale=True):
        """
        Move by a given amount (positive or negative) from the current position.
        
        If ``scale==True``, assume that the distance is in the physical units (see class description); otherwise, assume it is in the device internal units (steps).
        """
        if self._move_by_mode=="move_to":
            self._move_to(self._get_position(channel=channel,scale=scale)+distance,channel=channel,scale=scale)
        else:
            self.send_comm_data(0x0448,struct.pack("<Hi",self._make_channel(channel),self._p2d(distance,"p",scale=scale)),dest=("channel",channel))
    @muxchannel(mux_argnames="position")
    def _move_to(self, position, channel=None, scale=True):
        """Move to `position` (positive or negative).
        
        If ``scale==True``, assume that the position is in the physical units (see class description); otherwise, assume it is in the device internal units (steps).
        """
        self.send_comm_data(0x0453,struct.pack("<Hi",self._make_channel(channel),self._p2d(position,"p",scale=scale)),dest=("channel",channel))
    _forward_positive=False
    @muxchannel(mux_argnames="direction")
    @interface.use_parameters
    def _jog(self, direction, channel=None, kind="continuous"):
        """
        Jog in the given direction (``"+"`` or ``"-"``).
        
        If ``kind=="continuous"``, simply start motion in the given direction at the maximal speed
        until either the motor is stopped explicitly, or the limit is reached (this uses ``MOT_MOVE_VELOCITY`` command).
        If ``kind=="builtin"``, use the built-in ``MOT_MOVE_JOG`` command, whose parameters are specified by :meth:`get_jog_parameters`.
        """
        funcargparse.check_parameter_range(kind,"kind",["continuous","builtin"])
        _jog_fw=(self._forward_positive==bool(direction))
        comm=0x0457 if kind=="continuous" else 0x046A
        self.send_comm(comm,self._make_channel(channel),1 if _jog_fw else 2,dest=("channel",channel))
    _moving_status=["moving_fw","moving_bk","jogging_fw","jogging_bk","active"]
    @muxchannel
    def _is_moving(self, channel=None):
        """Check if motion is in progress"""
        curr_status=self._default_get_status(channel=channel)
        return any([s in curr_status for s in self._moving_status])
    def _wait_move(self, channel=None, timeout=None):
        """Wait until motion command is done"""
        return self._wait_for_status(self._moving_status,False,channel=channel,timeout=timeout)

    @muxchannel
    def _stop(self, immediate=False, sync=True, channel=None, timeout=None):
        """
        Stop the motion.

        If ``immediate==True`` make an abrupt stop; otherwise, slow down gradually.
        If ``sync==True``, wait until the motion is stopped.
        """
        self.send_comm(0x0465,self._make_channel(channel),1 if immediate else 2,dest=("channel",channel))
        if sync:
            self._wait_for_stop(channel=channel,timeout=timeout)
    def _wait_for_stop(self, channel=None, timeout=None):
        """Wait until motion or homing is done"""
        return self._wait_for_status(self._moving_status+["homing"],False,channel=channel,timeout=timeout)


    @muxchannel
    def _get_velocity_parameters(self, channel=None, scale=True):
        """
        Get current velocity parameters ``(min_velocity, acceleration, max_velocity)``
        
        Note that, according to the documentation, the minimal velocity is always zero.
        If ``scale==True``, return values in the physical units (see class description); otherwise, return it in the device internal units.
        """
        data=self.query(0x0414,self._make_channel(channel),dest=("channel",channel)).data
        min_velocity,acceleration,max_velocity=struct.unpack("<iii",data[2:14])
        min_velocity=self._d2p(min_velocity,"v",scale=scale)
        acceleration=self._d2p(acceleration,"a",scale=scale)
        max_velocity=self._d2p(max_velocity,"v",scale=scale)
        return TVelocityParams(min_velocity,acceleration,max_velocity)
    @muxchannel(mux_argnames=["min_velocity","acceleration","max_velocity"])
    def _setup_velocity(self, min_velocity=None, acceleration=None, max_velocity=None, channel=None, scale=True):
        """
        Set velocity parameters.
        
        If any parameter is ``None``, use the current value.
        Note that, according to the documentation, the minimal velocity is always zero, so changing it has no effect.
        If ``scale==True``, assume that the specified values are in the physical units (see class description); otherwise, assume it is in the device internal units.
        """
        current_parameters=self._get_velocity_parameters(channel=channel,scale=False)
        min_velocity=current_parameters.min_velocity if min_velocity is None else self._p2d(min_velocity,"v",scale=scale)
        acceleration=current_parameters.acceleration if acceleration is None else self._p2d(acceleration,"a",scale=scale)
        max_velocity=current_parameters.max_velocity if max_velocity is None else self._p2d(max_velocity,"v",scale=scale)
        data=struct.pack("<Hiii",self._make_channel(channel),min_velocity,acceleration,max_velocity)
        self.send_comm_data(0x0413,data,dest=("channel",channel))
        return self._get_velocity_parameters(channel=channel,scale=scale)

    _p_jog_mode=interface.EnumParameterClass("jog_mode",{"continuous":1,"step":2})
    _p_stop_mode=interface.EnumParameterClass("jog_stop_mode",{"immediate":1,"profiled":2})
    @muxchannel
    @interface.use_parameters(_returns=["jog_mode",None,None,None,None,"jog_stop_mode"])
    def _get_jog_parameters(self, channel=None, scale=True):
        """
        Get current jog parameters ``(mode, step_size, min_velocity, acceleration, max_velocity, stop_mode)``
        
        If ``scale==True``, return values in the physical units (see class description); otherwise, return it in the device internal units.
        """
        data=self.query(0x0417,self._make_channel(channel),dest=("channel",channel)).data
        mode,step_size,min_velocity,acceleration,max_velocity,stop_mode=struct.unpack("<HiiiiH",data[2:22])
        step_size=self._d2p(step_size,"p",scale=scale)
        min_velocity=self._d2p(min_velocity,"v",scale=scale)
        acceleration=self._d2p(acceleration,"a",scale=scale)
        max_velocity=self._d2p(max_velocity,"v",scale=scale)
        return TJogParams(mode,step_size,min_velocity,acceleration,max_velocity,stop_mode)
    @muxchannel(mux_argnames=["mode","step_size","min_velocity","acceleration","max_velocity","stop_mode"])
    @interface.use_parameters(mode="jog_mode",stop_mode="jog_stop_mode")
    def _setup_jog(self, mode=None, step_size=None, min_velocity=None, acceleration=None, max_velocity=None, stop_mode=None, channel=None, scale=True):
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
        data=struct.pack("<HHiiiiH",self._make_channel(channel),mode,step_size,min_velocity,acceleration,max_velocity,stop_mode)
        self.send_comm_data(0x0416,data,dest=("channel",channel))
        return self._get_jog_parameters(channel=channel,scale=scale)

    @muxchannel
    def _get_adc_inputs(self, channel=None, scale=True):
        """
        Get current adc input voltages ``(input1, input2)``.
        
        If ``scale==True``, return values in volts; otherwise, return in internal units (0 to 32768).
        """
        data=self.query(0x042B,self._make_channel(channel),dest=("channel",channel)).data
        input1,input2=struct.unpack("<HH",data[2:6])
        if scale:
            input1/=2**15/5.
            input2/=2**15/5.
        return (input1,input2)

    @muxchannel
    def _get_gen_move_parameters(self, channel=None, scale=True):
        """
        Get general move parameters parameters ``(backlash_distance)``
        
        If ``scale==True``, return values in the physical units (see class description); otherwise, return it in the device internal units.
        """
        data=self.query(0x043B,self._make_channel(channel),dest=("channel",channel)).data
        backlash_distance,=struct.unpack("<i",data[2:6])
        backlash_distance=self._d2p(backlash_distance,"p",scale=scale)
        return TGenMoveParams(backlash_distance)
    @muxchannel(mux_argnames=["backlash_distance"])
    def _setup_gen_move(self, backlash_distance=None, channel=None, scale=True):
        """
        Set jog parameters.
        
        If any parameter is ``None``, use the current value.
        If ``scale==True``, assume that the specified value is in the physical units (see class description); otherwise, assume it is in the device internal units.
        """
        current_parameters=self._get_gen_move_parameters(channel=channel,scale=False)
        backlash_distance=current_parameters.backlash_distance if backlash_distance is None else self._p2d(backlash_distance,"p",scale=scale)
        data=struct.pack("<Hi",self._make_channel(channel),backlash_distance)
        self.send_comm_data(0x043A,data,dest=("channel",channel))
        return self._get_gen_move_parameters(channel=channel,scale=scale)

    _p_home_direction=interface.EnumParameterClass("home_direction",{"forward":1,"reverse":2})
    _p_limit_switch=interface.EnumParameterClass("limit_switch",{"reverse":1,"forward":4})
    @muxchannel
    @interface.use_parameters(_returns=["home_direction","limit_switch",None,None])
    def _get_homing_parameters(self, channel=None, scale=True):
        """
        Get current homing parameters ``(home_direction, limit_switch, velocity, offset_distance)``
        
        If ``scale==True``, return values are in the physical units (see class description); otherwise, return it in the device internal units.
        """
        data=self.query(0x0441,self._make_channel(channel),dest=("channel",channel)).data
        home_direction,limit_switch,velocity,offset_distance=struct.unpack("<HHii",data[2:14])
        velocity=self._d2p(velocity,"v",scale=scale)
        offset_distance=self._d2p(offset_distance,"p",scale=scale)
        return THomeParams(home_direction,limit_switch,velocity,offset_distance)
    @muxchannel(mux_argnames=["home_direction","limit_switch","velocity","offset_distance"])
    @interface.use_parameters
    def _setup_homing(self, home_direction=None, limit_switch=None, velocity=None, offset_distance=None, channel=None, scale=True):
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
        data=struct.pack("<HHHii",self._make_channel(channel),home_direction,limit_switch,velocity,offset_distance)
        self.send_comm_data(0x0440,data,dest=("channel",channel))
        return self._get_homing_parameters(channel=channel,scale=scale)

    _p_hw_limit_kind=interface.EnumParameterClass("hw_limit_kind",{"ignore":1,"make":2,"break":3,"make_home":4,"break_home":5,"index_mark":6})
    _p_sw_limit_kind=interface.EnumParameterClass("sw_limit_kind",{"ignore":1,"stop_imm":2,"stop_prof":3,"full_move_only":0})
    @muxchannel
    @interface.use_parameters(_returns=["hw_limit_kind","hw_limit_kind",None,None,None,"sw_limit_kind"])
    def _get_limit_switch_parameters(self, channel=None, scale=True):
        """
        Get current limit switch parameters ``(hw_kind_cw, hw_kind_ccw, hw_flipped, sw_position_cw, sw_position_ccw, sw_kind)``
        
        If ``scale==True``, return values in the physical units (see class description); otherwise, return it in the device internal units (steps).
        """
        data=self.query(0x0424,self._make_channel(channel),dest=("channel",channel)).data
        hw_kind_cw,hw_kind_ccw,sw_position_cw,sw_position_ccw,sw_kind=struct.unpack("<HHiiH",data[2:16])
        swapped_cw=bool(hw_kind_cw&0x80)
        swapped_ccw=bool(hw_kind_ccw&0x80)
        if swapped_cw!=swapped_ccw:
            warnings.warn("swapped bit is different for the two axes; assume that the switches are not swapped")
        sw_position_cw=self._d2p(sw_position_cw,"p",scale=scale)
        sw_position_ccw=self._d2p(sw_position_ccw,"p",scale=scale)
        return TLimitSwitchParams(hw_kind_cw&0x7F,hw_kind_ccw&0x7F,swapped_cw,sw_position_cw,sw_position_ccw,sw_kind&0x7F)
    @muxchannel(mux_argnames=["hw_kind_cw","hw_kind_ccw","hw_swapped","sw_position_cw","sw_position_ccw","sw_kind"])
    @interface.use_parameters(hw_kind_cw="hw_limit_kind",hw_kind_ccw="hw_limit_kind",sw_kind="sw_limit_kind")
    def _setup_limit_switch(self, hw_kind_cw=None, hw_kind_ccw=None, hw_swapped=None, sw_position_cw=None, sw_position_ccw=None, sw_kind=None, channel=None, scale=True):
        """
        Set limit switch parameters.
        
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
        data=struct.pack("<HHHiiH",self._make_channel(channel),hw_kind_cw,hw_kind_ccw,sw_position_cw,sw_position_ccw,sw_kind)
        self.send_comm_data(0x0423,data,dest=("channel",channel))
        return self._get_limit_switch_parameters(channel=channel,scale=scale)

    _p_kcube_trigio_mode=interface.EnumParameterClass("kcube_trigio_mode",{"off":0x00,
        "in_gpio":0x01,"in_relmove":0x02,"in_absmove":0x03,"in_home":0x04,
        "out_gpio":0x0A,"out_in_motion":0x0B,"out_maxvel":0x0C,"out_pulse_fw":0x0D,"out_pulse_bk":0x0E,"out_pulse_move":0x0F,
        "out_lim_fw":0x10,"out_lim_bk":0x11,"out_lim_both":0x12})
    @interface.use_parameters(_returns=["kcube_trigio_mode",None,"kcube_trigio_mode",None])
    def _get_kcube_trigio_parameters(self):
        """Get KCube trigger IO parameters ``(trig1_mode, trig1_pol, trig2_mode, trig2_pol)``"""
        data=self.query(0x0524,0x01).data
        trig1_mode,trig1_pol,trig2_mode,trig2_pol=struct.unpack("<HHHH",data[2:10])
        return TKCubeTrigIOParams(trig1_mode,bool(trig1_pol),trig2_mode,bool(trig2_pol))
    @interface.use_parameters(trig1_mode="kcube_trigio_mode",trig2_mode="kcube_trigio_mode")
    def _setup_kcube_trigio(self, trig1_mode=None, trig1_pol=None, trig2_mode=None, trig2_pol=None):
        """
        Set KCube trigger IO parameters.
        
        If any parameter is ``None``, use the current value.
        """
        current_parameters=self._wap._get_kcube_trigio_parameters()
        trig1_mode=current_parameters.trig1_mode if trig1_mode is None else trig1_mode
        trig1_pol=current_parameters.trig1_pol if trig1_pol is None else trig1_pol
        trig2_mode=current_parameters.trig2_mode if trig2_mode is None else trig2_mode
        trig2_pol=current_parameters.trig2_pol if trig2_pol is None else trig2_pol
        data=struct.pack("<HHHHH",0x01,trig1_mode,trig1_pol,trig2_mode,trig2_pol)
        self.send_comm_data(0x0523,data)
        return self._get_kcube_trigio_parameters()

    def _get_kcube_trigpos_parameters(self, scale=True):
        """
        Get KCube trigger position parameters ``(start_fw, step_fw, num_fw, start_bk, step_bk, num_bk, width, ncycles)``.
        
        If ``scale==True``, return positions and steps in the physical units (see class description); otherwise, return it in the device internal units (steps).
        Pulse ``width`` is always defined in seconds.
        """
        data=self.query(0x0527,0x01).data
        start_fw,step_fw,num_fw,start_bk,step_bk,num_bk,width,ncycles=struct.unpack("<iiiiiiii",data[2:34])
        start_fw=self._d2p(start_fw,"p",scale=scale)
        step_fw=self._d2p(step_fw,"p",scale=scale)
        start_bk=self._d2p(start_bk,"p",scale=scale)
        step_bk=self._d2p(step_bk,"p",scale=scale)
        return TKCubeTrigPosParams(start_fw,step_fw,num_fw,start_bk,step_bk,num_bk,width/1E6,ncycles)
    def _setup_kcube_trigpos(self, start_fw=None, step_fw=None, num_fw=None, start_bk=None, step_bk=None, num_bk=None, width=None, ncycles=None, scale=True):
        """
        Set KCube trigger IO parameters.
        
        If any parameter is ``None``, use the current value.
        
        If ``scale==True``, return positions and steps in the physical units (see class description); otherwise, return it in the device internal units (steps).
        Pulse ``width`` is always defined in seconds.
        """
        current_parameters=self._wap._get_kcube_trigpos_parameters(scale=False)
        start_fw=current_parameters.start_fw if start_fw is None else self._p2d(start_fw,"p",scale=scale)
        step_fw=current_parameters.step_fw if step_fw is None else self._p2d(step_fw,"p",scale=scale)
        num_fw=current_parameters.num_fw if num_fw is None else num_fw
        start_bk=current_parameters.start_bk if start_bk is None else self._p2d(start_bk,"p",scale=scale)
        step_bk=current_parameters.step_bk if step_bk is None else self._p2d(step_bk,"p",scale=scale)
        num_bk=current_parameters.num_bk if num_bk is None else num_bk
        width=current_parameters.width if width is None else int(width*1E6)
        ncycles=current_parameters.ncycles if ncycles is None else ncycles
        data=struct.pack("<Hiiiiiiii",0x01,start_fw,step_fw,num_fw,start_bk,step_bk,num_bk,width,ncycles)
        self.send_comm_data(0x0526,data)
        return self._get_kcube_trigpos_parameters()

    def _get_polctl_parameters(self, scale=True):
        """
        Get current polarizer controller parameters ``(velocity, home_position, jog1, jog2, jog3)``
        
        If ``scale==True``, return values in the physical units (see class description); otherwise, return it in the device internal units.
        ``velocity`` is always returned in percent units (0 to 100).
        """
        data=self.query(0x0531).data
        velocity,home_position,jog1,jog2,jog3=struct.unpack("<HHHHH",data[2:12])
        home_position=self._d2p(home_position,"p",scale=scale)
        jog1=self._d2p(jog1,"p",scale=scale)
        jog2=self._d2p(jog2,"p",scale=scale)
        jog3=self._d2p(jog3,"p",scale=scale)
        return TPolCtlParams(velocity,home_position,jog1,jog2,jog3)
    def _setup_polctl(self, velocity=None, home_position=None, jog1=None, jog2=None, jog3=None, scale=True):
        """
        Set polarizer controller parameters.
        
        If any parameter is ``None``, use the current value.
        If ``scale==True``, assume that the specified values are in the physical units (see class description); otherwise, assume it is in the device internal units.
        ``velocity`` is always set in percent units (0 to 100).
        """
        current_parameters=self._get_polctl_parameters(scale=False)
        velocity=current_parameters.velocity if velocity is None else velocity
        home_position=current_parameters.home_position if home_position is None else self._p2d(home_position,"p",scale=scale)
        jog1=current_parameters.jog1 if jog1 is None else self._p2d(jog1,"p",scale=scale)
        jog2=current_parameters.jog2 if jog2 is None else self._p2d(jog2,"p",scale=scale)
        jog3=current_parameters.jog3 if jog3 is None else self._p2d(jog3,"p",scale=scale)
        data=b"\x00\x00"+struct.pack("<HHHHH",velocity,home_position,jog1,jog2,jog3)
        self.send_comm_data(0x0530,data)
        return self._get_polctl_parameters(scale=scale)

    _p_channel_id=interface.EnumParameterClass("channel_id",{1:0x01,2:0x02,3:0x04,4:0x08})
    @muxchannel
    @interface.use_parameters(channel="channel_id")
    def _is_channel_enabled(self, channel=None):  # seems to not work for most devices when tested
        """Check if the given channel is enabled"""
        msg=self.query(0x0211,self._make_channel(channel),dest=("channel",channel))
        self.instr.read()  # sometimes extra \x00 bits are appended
        return msg.param2==0x01
    @muxchannel(mux_argnames="enabled")
    @interface.use_parameters(channel="channel_id")
    def _enable_channel(self, enabled=True, channel=None):  # seems to not work for most devices when tested
        """Enable or disable the given channel"""
        self.send_comm(0x0210,self._make_channel(channel),0x01 if enabled else 0x02,dest=("channel",channel))
        return self._wip._is_channel_enabled(channel)


    _pzmot_kind=None
    def _pzmot_get_kind(self):
        if self._pzmot_kind is None:
            self._pzmot_kind=self._model[:3].upper()
        return self._pzmot_kind
    @muxchannel
    def _pzmot_get_status_n(self, channel=None):
        """
        Get numerical status of the piezo motor.

        For details, see APT communications protocol.
        """
        data=self.query(0x08E0).data
        status=[struct.unpack("<I",data[i*14+10:i*14+14])[0] for i in range(4)]
        return status[channel-1]
    @muxchannel
    def _pzmot_get_status(self, channel=None):
        """
        Get piezo motor status.

        Return list of status strings, which can include ``"sw_fw_lim"`` (forward limit switch reached), ``"sw_bk_lim"`` (backward limit switch reached),
        ``"moving_fw"`` (moving forward), ``"moving_bk"`` (moving backward), ``"jogging_fw"`` (jogging forward), ``"jogging_bk"`` (jogging backward),
        ``"homing"`` (homing), ``"homed"`` (homing done), ``"tracking"``, ``"settled"``,
        ``"motion_error"`` (excessive position error), ``"current_limit"`` (motor current limit exceeded), or ``"enabled"`` (motor is enabled).
        """
        status_n=self._pzmot_get_status_n(channel=channel)
        return [s for (m,s) in self.status_bits if status_n&m]
    @interface.use_parameters(channel="channel_id")
    def _pzmot_req(self, subid, channel):
        """Perform PZMOT request (applicable to KIMx01/TIMx01)"""
        data=self.query(0x08C1,subid,channel).data
        rsubid,rchannel=struct.unpack("<HH",data[:4])
        if rchannel!=channel:
            raise RuntimeError("unexpected channel in the reply: expected 0x{:02x}, got 0x{:02x}".format(channel,rchannel))
        if rsubid!=subid:
            raise RuntimeError("unexpected submessage ID in the reply: expected 0x{:02x}, got 0x{:02x}".format(subid,rsubid))
        return data[4:]
    @interface.use_parameters(channel="channel_id")
    def _pzmot_set(self, subid, channel, data):
        """Perform PZMOT set (applicable to KIMx01/TIMx01)"""
        data=struct.pack("<HH",subid,channel)+data
        self.send_comm_data(0x08C0,data)
    @muxchannel
    def _pzmot_get_position(self, channel=None):
        """Get current piezo-motor position"""
        data=self._pzmot_req(0x05,channel)
        return struct.unpack("<ii",data)[0]
    @muxchannel(mux_argnames="position")
    def _pzmot_set_position_reference(self, position=0, channel=None):
        """Set piezo-motor position reference (actual position stays the same)"""
        self._pzmot_set(0x05,channel,struct.pack("<ii",position,0))
        return self._pzmot_get_position(channel)
    @muxchannel
    def _pzmot_get_drive_parameters(self, channel=None):
        """
        Get current piezo-motor drive parameters ``(max_voltage, velocity, acceleration)``
        
        Voltage is defined in volts, velocity in steps/s, and acceleration in steps/s^2.
        """
        data=self._pzmot_req(0x07,channel)
        return TPZMotorDriveParams(*struct.unpack("<HII",data))
    @muxchannel(mux_argnames=["max_voltage","velocity","acceleration"])
    def _pzmot_setup_drive(self, max_voltage=None, velocity=None, acceleration=None, channel=None):
        """
        Set piezo-motor drive parameters.
        
        If any parameter is ``None``, use the current value.
        Voltage is defined in volts, velocity in steps/s, and acceleration in steps/s^2.
        """
        current_parameters=self._pzmot_get_drive_parameters(channel=channel)
        max_voltage=current_parameters.max_voltage if max_voltage is None else max_voltage
        velocity=current_parameters.velocity if velocity is None else velocity
        acceleration=current_parameters.acceleration if acceleration is None else acceleration
        data=struct.pack("<HII",max_voltage,velocity,acceleration)
        self._pzmot_set(0x07,channel,data)
        return self._pzmot_get_drive_parameters(channel)
    @muxchannel
    @interface.use_parameters(_returns=["jog_mode",None,None,None,None])
    def _pzmot_get_jog_parameters(self, channel=None):
        """
        Get current piezo-motor jog parameters ``(mode, step_size_fw, step_size_bk, velocity, acceleration)``
        
        Step size is defined in piezo steps, velocity in steps/s, and acceleration in step/s^2.
        """
        if self._pzmot_get_kind()=="TIM":
            data=self._pzmot_req(0x09 if self._pzmot_kind=="TIM" else 0x0D,channel)
            par=struct.unpack("<HIII",data)
            return TPZMotorJogParams(par[0],par[1],*par[1:])
        else:
            data=self._pzmot_req(0x2D,channel)
            return TPZMotorJogParams(*struct.unpack("<HIIII",data))
    @muxchannel(mux_argnames=["mode","step_size_fw","step_size_bk","velocity","acceleration"])
    @interface.use_parameters(mode="jog_mode")
    def _pzmot_setup_jog(self, mode=None, step_size_fw=None, step_size_bk=None, velocity=None, acceleration=None, channel=None):
        """
        Set piezo-motor jog parameters.
        
        If any parameter is ``None``, use the current value.
        Step size is defined in piezo steps, velocity in steps/s, and acceleration in step/s^2.
        TIM-series controllers do not support separate step size, so `step_size_bk` is ignored for them.
        """
        current_parameters=self._wop._pzmot_get_jog_parameters(channel)
        mode=current_parameters.mode if mode is None else mode
        step_size_fw=current_parameters.step_size_fw if step_size_fw is None else step_size_fw
        step_size_bk=current_parameters.step_size_bk if step_size_bk is None else step_size_bk
        velocity=current_parameters.velocity if velocity is None else velocity
        acceleration=current_parameters.acceleration if acceleration is None else acceleration
        if self._pzmot_get_kind()=="TIM":
            data=struct.pack("<HIII",mode,step_size_fw,velocity,acceleration)
            self._pzmot_set(0x09,channel,data)
        else:
            data=struct.pack("<HIIII",mode,step_size_fw,step_size_bk,velocity,acceleration)
            self._pzmot_set(0x2D,channel,data)
        return self._pzmot_get_jog_parameters(channel)


    _p_pzmot_channel_enabled=interface.EnumParameterClass("pzmot_channel_enabled",{False:0,None:0,1:1,2:2,3:3,4:4,(1,):1,(2,):2,(3,):3,(4,):4,(1,2):5,(3,4):6})
    @interface.use_parameters(_returns="pzmot_channel_enabled")
    def _pzmot_get_enabled_channels(self):
        """
        Check which specific piezo motor channels are enabled.

        Can be ``None`` (none enabled), or a tuple with either one or two channels:
        ``(1,)`` to ``(4,)``, ``(1,2)`` or ``(3,4)``.
        """
        data=self.query(0x08C1,0x2B).data
        return struct.unpack("<HH",data)[1]
    @interface.use_parameters(channel="pzmot_channel_enabled")
    def _pzmot_enable_channels(self, channel):
        """
        Enable specific piezo motor channel.

        Can be ``None`` (none enabled), and integer 1 to 4,
        or a tuple ``(1,2)`` or ``(3,4)`` (enable 2 channel simultaneously).
        """
        data=struct.pack("<HH",0x2B,channel)
        self.send_comm_data(0x08C0,data)
        return self._pzmot_get_enabled_channels()
    def _pzmot_autoenable(self, channel, auto_enable=True):
        if auto_enable:
            enabled=self._pzmot_get_enabled_channels()
            if channel not in enabled:
                self._pzmot_enable_channels(channel)

    @muxchannel(mux_argnames="position")
    @interface.use_parameters(channel="channel_id")
    def _pzmot_move_to(self, position, auto_enable=True, channel=None):
        """Move piezo-motor to `position` (positive or negative)"""
        self._pzmot_autoenable({0x01:1,0x02:2,0x04:3,0x08:4}[channel],auto_enable)
        self.send_comm_data(0x08D4,struct.pack("<Hi",channel,int(position)))
    @muxchannel(mux_argnames="distance")
    def _pzmot_move_by(self, distance=1, auto_enable=True, channel=None):
        """Move piezo-motor by a given `distance` (positive or negative)"""
        self._pzmot_move_to(self._pzmot_get_position(channel)+distance,auto_enable=auto_enable,channel=channel)
    @muxchannel(mux_argnames="direction")
    @interface.use_parameters
    def _pzmot_jog(self, direction, kind="continuous", auto_enable=True, channel=None):
        """
        Jog piezo motor in the given direction (``"+"`` or ``"-"``).

        If ``kind=="continuous"``, simply start motion in the given direction at the standard jog speed
        until either the motor is stopped explicitly, or the limit is reached.
        If ``kind=="builtin"``, use the built-in jog command, whose parameters are specified by :meth:`get_jog_parameters`.
        Note that ``kind=="continuous"`` is still implemented through the builtin jog, so it changes its parameters;
        hence, afterwards the jog parameters need to be manually restored.
        """
        funcargparse.check_parameter_range(kind,"kind",["continuous","builtin"])
        self._pzmot_autoenable(channel,auto_enable)
        if kind=="continuous":
            self._pzmot_setup_jog(mode="continuous",channel=channel)
        _jog_fw=(self._forward_positive==bool(direction))
        self.send_comm(0x08D9,channel,1 if _jog_fw else 2)
    @muxchannel
    @interface.use_parameters
    def _pzmot_stop(self, channel=None, sync=True):
        """Stop the piezo motor motion"""
        self._pzmot_move_by(0,channel=channel,auto_enable=False)
        if sync:
            self._wait_for_status(self._moving_status,False,channel=channel)
    def _pzmot_wait_for_status(self, status, enabled, timeout=None, period=0.05, channel=None):
        return self._wait_for_status(status,enabled,channel=channel,timeout=timeout,period=period)

    @muxchannel
    def _pzctl_get_status_n(self, channel=None):
        """
        Get numerical status of the piezo controller.

        For details, see APT communications protocol.
        """
        data=self.query(0x0660,channel).data
        return struct.unpack("<I",data[6:10])[0]
    _pzctl_status_bits=[(1<<0,"stage_connected"),(1<<4,"zeroed"),(1<<5,"zeroing"),(1<<8,"gauge_connected"),(1<<10,"closed_loop"),(1<<29,"active"),(1<<31,"enabled")]
    @muxchannel
    def _pzctl_get_status(self, channel=None):
        """
        Get piezo motor status.

        Return list of status strings, which can include ``"stage_connected"`` (actuator is connected),
        ``"zeroed"`` (position readout actuator is zeroed), ``"zeroing"`` (position readout actuator is zeroing),
        ``"gauge_connected"`` (strain gauge is connected), ``"closed_loop"`` (operating in the closed loop mode)
        ``"active"`` (unit is active), ``"enabled"`` (output is enabled).
        """
        status_n=self._pzctl_get_status_n(channel=channel)
        return [s for (m,s) in self._pzctl_status_bits if status_n&m]
    @muxchannel
    @interface.use_parameters(channel="channel_id")
    def _pzctl_is_channel_enabled(self, channel=None):
        """Check if the given channel is enabled"""
        return "enabled" in self._pzctl_get_status(channel=channel)
    @muxchannel(mux_argnames="enabled")
    @interface.use_parameters(channel="channel_id")
    def _pzctl_enable_channel(self, enabled=True, channel=None):  # seems to not work for most devices when tested
        """Enable or disable the given channel"""
        self.send_comm(0x0210,self._make_channel(channel),0x01 if enabled else 0x02,dest=("channel",channel))
        return self._wip._pzctl_is_channel_enabled(channel)
    _p_pzctl_voltage_range=interface.EnumParameterClass("pzctl_voltage_range",{75:0x01,100:0x02,150:0x03})
    @muxchannel
    @interface.use_parameters(_returns="pzctl_voltage_range")
    def _pzctl_get_voltage_range(self, channel=None):
        """Get piezo controller output voltage range (in V)"""
        data=self.query(0x07D5,channel).data
        return struct.unpack("<H",data[2:4])[0]
    @muxchannel
    @interface.use_parameters(rng="pzctl_voltage_range")
    def _pzctl_set_voltage_range(self, rng, channel=None):
        """Set piezo controller output voltage range (in V)"""
        data=self.query(0x07D5,channel).data
        data=data[:2]+struct.pack("<H",rng)+data[4:]
        self.send_comm_data(0x07D4,data)
        return self._pzctl_get_voltage_range(channel)
    
    _p_pzctl_voltage_units=interface.EnumParameterClass("pzctl_voltage_units",["V","perc"])
    def _pzctl_voltage_u2d(self, v, units, channel):
        span=100. if units=="perc" else self._pzctl_get_voltage_range(channel)
        return max(-2**15,min(int(v/span*(2**15-1)),2**15-1))
    def _pzctl_voltage_d2u(self, v, units, channel):
        span=100. if units=="perc" else self._pzctl_get_voltage_range(channel)
        return v/(2**15-1)*span
    @muxchannel
    @interface.use_parameters(units="pzctl_voltage_units")
    def _pzctl_get_output_voltage(self, units="V", channel=None):
        """Get piezo controller output voltage"""
        data=self.query(0x0644,channel).data
        return self._pzctl_voltage_d2u(struct.unpack("<Hh",data)[1],units,channel)
    @muxchannel
    @interface.use_parameters(units="pzctl_voltage_units")
    def _pzctl_set_output_voltage(self, voltage, units="V", channel=None):
        """Set piezo controller output voltage"""
        voltage=self._pzctl_voltage_u2d(voltage,units,channel)
        self.send_comm_data(0x0643,struct.pack("<Hh",channel,voltage))
        return self._pzctl_get_output_voltage(units,channel)

    _pzctl_voltage_src_bits={"software":0x00,"ext_in":0x01,"pot":0x02}
    @muxchannel
    @interface.use_parameters
    def _pzctl_get_voltage_source(self, channel=None):
        """Get piezo controller input voltage source"""
        data=self.query(0x0653,channel).data
        src=struct.unpack("<HH",data)[1]
        return [s for (s,m) in self._pzctl_voltage_src_bits.items() if src&m==m]
    @muxchannel
    @interface.use_parameters
    def _pzctl_set_voltage_source(self, src="software", channel=None):
        """Set piezo controller input voltage source"""
        if not isinstance(src,(tuple,list)):
            src=[src]
        for s in src:
            funcargparse.check_parameter_range(s,"src",self._pzctl_voltage_src_bits)
        src=sum([self._pzctl_voltage_src_bits[s] for s in src])
        self.send_comm_data(0x0652,struct.pack("<HH",channel,src))
        return self._pzctl_get_voltage_source(channel)



TFlipperParameters=collections.namedtuple("TFlipperParameters",["transit_time","io1_oper_mode","io1_sig_mode","io1_pulse_width","io2_oper_mode","io2_sig_mode","io2_pulse_width"])
class MFF(KinesisDevice):
    """
    MFF (Motorized Filter Flip Mount) device.

    Implements FTDI chip connectivity via pyft232 (virtual serial interface).

    Args:
        conn: serial connection parameters (usually 8-digit device serial number).
    """
    def __init__(self, conn):
        super().__init__(conn)
        self._add_settings_variable("state",self.get_state,self.move_to_state)

    get_status_n=KinesisDevice._get_status_n
    get_status=KinesisDevice._get_status
    wait_for_status=KinesisDevice._wait_for_status
    
    @muxchannel
    def move_to_state(self, state, channel=None):
        """Move to the given flip mount state (either 0 or 1)"""
        self.send_comm(0x046A,channel,2 if state else 1)
    @muxchannel
    def get_state(self, channel=None):
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
    _p_io_sig_mode=interface.EnumParameterClass("io_sig_mode",{"in_button":0x01,"in_voltage":0x02,"in_button_inv":0x05,"in_voltage_inv":0x06,
                                                                "out_edge":0x10,"out_pulse":0x20,"out_edge_inv":0x50,"out_pulse_inv":0x60})
    @muxchannel
    @interface.use_parameters(_returns=[None,"io_oper_mode","io_sig_mode",None,"io_oper_mode","io_sig_mode",None])
    def get_flipper_parameters(self, channel=None):
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
    @muxchannel(mux_argnames=["transit_time","io1_oper_mode","io1_sig_mode","io1_pulse_width","io2_oper_mode","io2_sig_mode","io2_pulse_width"])
    @interface.use_parameters(io1_oper_mode="io_oper_mode",io1_sig_mode="io_sig_mode",io2_oper_mode="io_oper_mode",io2_sig_mode="io_sig_mode")
    def setup_flipper(self, transit_time=None, io1_oper_mode=None, io1_sig_mode=None, io1_pulse_width=None, io2_oper_mode=None, io2_sig_mode=None, io2_pulse_width=None, channel=None):
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
        default_channel: starting default channel used when no channel is supplied to a channel-level command (such as ``move_to`` or ``get_position``).
        is_rack_system: specify whether the device is a rack system or a standalone USB device (default mode).
    """
    def __init__(self, conn, scale="step", default_channel=1, is_rack_system=False):
        super().__init__(conn,default_channel=default_channel,is_rack_system=is_rack_system)
        self.add_background_comm(0x0464) # move completed
        self.add_background_comm(0x0466) # move stopped
        self.add_background_comm(0x0444) # homed
        self.add_background_comm(0x0491) # status update
        self._add_info_variable("scale_units",self.get_scale_units)
        self._add_info_variable("scale",self.get_scale)
        self._add_info_variable("stage",self.get_stage)
        self._add_status_variable("position",self.get_position)
        self._add_status_variable("status",self.get_status)
        if not self._model.startswith("MPC"):
            self._add_settings_variable("velocity_parameters",self.get_velocity_parameters,self.setup_velocity)
            self._add_settings_variable("jog_parameters",self.get_jog_parameters,self.setup_jog)
            self._add_settings_variable("homing_parameters",self.get_homing_parameters,self.setup_homing)
            self._add_settings_variable("gen_move_parameters",self.get_gen_move_parameters,self.setup_gen_move)
            self._add_settings_variable("limit_switch_parameters",self.get_limit_switch_parameters,self.setup_limit_switch)
        else:
            self._add_settings_variable("polctl_parameter",self.get_polctl_parameters,self.setup_polctl)
        if self._model in ["KDC101","KST101","KBD101"]:
            if self._model!="KST101":
                self._add_settings_variable("kcube_trigio_parameters",self.get_kcube_trigio_parameters,self.setup_kcube_trigio)
            self._add_settings_variable("kcube_trigpos_parameters",self.get_kcube_trigpos_parameters,self.setup_kcube_trigpos)
        with self._close_on_error():
            self.send_comm(0x0012) # disable automatic update
            self.send_comm(0x0005)
            while self.recv_comm().messageID!=0x0006:
                pass
            self._stage=self._get_stage(scale)
            self._scale,self._scale_units=self._calculate_scale(scale)
    
    def _autodetect_stage(self):
        info=self.query(0x0005).data
        stage_id,=struct.unpack("<H",info[76:78])
        if self._model in ["KDC101","TDC001","ODC001"]:
            stages={2:"Z706",3:"Z712",4:"Z725",5:"CR1-Z7",6:"PRM1-Z8",
                    7:"MTS25-Z8",8:"MTS50-Z8",9:"Z825",10:"Z812",11:"Z806"}
            return stages.get(stage_id,None)
        if self._model=="K10CR1" or self._model.startswith(("MPC", "M30", "KVS30")):
            return self._model
        return None
    def _get_stage(self, scale):
        if scale=="stage":
            return self._autodetect_stage()
        return scale if isinstance(scale,py3.textstring) else None
    def _get_step_scale(self, stage):
        if stage is None:
            warnings.warn("can't recognize the stage; assuming step scale of 1")
            return 1,None
        stage=stage.strip().upper()
        if stage=="STEP":
            return 1,"step"
        if self._model.startswith("M30"):
            return 1E7, "m"
        if stage in {"MTS25-Z8","MTS50-Z8","Z806","Z812","Z825"}:
            return 34304E3,"m"
        if stage in {"Z606","Z612","Z625"}:
            return 24600E3,"m"
        if stage in {"PRM1-Z8","PRM1TZ8"}:
            return 1919.6418578623391,"deg" # that's what it says in the manual...
        if stage in {"CR1-Z7"}:
            return 12288E3,"m"
        if stage in {"DDSM50","DDSM100"}:
            return 2000E3,"m"
        if stage in {"DDS220","DDS300","DDS600","MLS203"} or self._model.startswith("KVS30"):
            return 20000E3,"m"
        if stage=="DDR100":
            return 3276800/360,"deg"
        if stage=="DDR05":
            return 2000000/360,"deg"
        if stage=="DDR25":
            return 1440000/360,"deg"
        if stage=="HDR50":
            return 75091/0.99997,"deg"
        if self._model in ["TST001","MST601"] or self._model.startswith(("BSC00", "BSC10")):
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
        if self._model in ["TST101","KST101","MST602","K10CR1"] or self._model.startswith(("BSC20", "SSC20")):
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
        if self._model.startswith("MPC"):
            return 1370/170,"deg"
        warnings.warn("can't recognize the stage name {}; assuming step scale of 1".format(stage))
        return 1,"step"
    def _calculate_scale(self, scale):
        if isinstance(scale,tuple):
            return scale,"user"
        if scale=="stage":
            scale=self._stage
        if isinstance(scale,py3.textstring) or scale is None:
            ssc,units=self._get_step_scale(scale)
        else:
            ssc,units=scale,"user_step"
        if self._model in ["KDC101","TDC001"]:
            time_conv=2048/6E6
            return (ssc,ssc*time_conv*2**16,ssc*time_conv**2*2**16),units
        if self._model in ["TBD001","KBD101"] or self._model.startswith("BBD10") or self._model.startswith("BBD20"):
            time_conv=102.4E-6
            return (ssc,ssc*time_conv*2**16,ssc*time_conv**2*2**16),units
        if self._model in ["TST001","MST601"] or self._model.startswith(("BSC", "MPC", "M30", "KVS30")):
            return (ssc,ssc,ssc),units
        if self._model in ["TST101","KST101","MST602","K10CR1"]:
            vpr=53.68
            avr=204.94E-6
            return (ssc,ssc*vpr,ssc*vpr*avr),units
        if self._model.startswith("BSC20") or self._model.startswith("SCC20"):
            vpr=8.26
            avr=204.94E-6
            return (ssc,ssc*vpr,ssc*vpr*avr),units
        warnings.warn("can't recognize motor model {}; setting all scales to internal units".format(self._model))
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

    set_supported_channels=KinesisDevice._set_supported_channels

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
    get_kcube_trigio_parameters=KinesisDevice._get_kcube_trigio_parameters
    setup_kcube_trigio=KinesisDevice._setup_kcube_trigio
    get_kcube_trigpos_parameters=KinesisDevice._get_kcube_trigpos_parameters
    setup_kcube_trigpos=KinesisDevice._setup_kcube_trigpos
    get_polctl_parameters=KinesisDevice._get_polctl_parameters
    setup_polctl=KinesisDevice._setup_polctl






class KinesisPiezoMotor(KinesisDevice):
    """
    Thorlabs piezo motor (TIM/KIM series) controller.

    Implements FTDI chip connectivity via pyft232 (virtual serial interface).

    Args:
        conn(str): serial connection parameters (usually an 8-digit device serial number).
    """
    def __init__(self, conn, default_channel=1, is_rack_system=False):
        super().__init__(conn,default_channel=default_channel,is_rack_system=is_rack_system)
        self.add_background_comm(0x08D6) # move completed
        self._add_status_variable("enabled_channels",self.get_enabled_channels,self.enable_channels)
        self._add_status_variable("position",lambda: self.get_position(channel="all"))
        self._add_status_variable("status",lambda: self.get_status(channel="all"))
        self._add_settings_variable("drive_parameters",lambda: self.get_drive_parameters(channel="all"), lambda v: self.setup_drive(v,channel="all"))
        self._add_settings_variable("jog_parameters",lambda: self.get_jog_parameters(channel="all"), lambda v: self.setup_jog(v,channel="all"))
        with self._close_on_error():
            self._autodetect_axes()
    def _autodetect_axes(self):
        if self._model in ["TIM001","KIM001"]:
            self._update_axes([1])
        elif self._model in ["TIM101","KIM101"]:
            self._update_axes([1,2,3,4])
        else:
            warnings.warn("unexpected piezo motor model: {}; assuming one axis".format(self._model))
            self._update_axes([1])
    _forward_positive=True
    _default_get_status=KinesisDevice._pzmot_get_status

    get_enabled_channels=KinesisDevice._pzmot_get_enabled_channels
    enable_channels=KinesisDevice._pzmot_enable_channels

    get_status_n=KinesisDevice._pzmot_get_status_n
    get_status=KinesisDevice._pzmot_get_status
    wait_for_status=KinesisDevice._pzmot_wait_for_status

    get_position=KinesisDevice._pzmot_get_position
    set_position_reference=KinesisDevice._pzmot_set_position_reference
    move_by=KinesisDevice._pzmot_move_by
    move_to=KinesisDevice._pzmot_move_to
    jog=KinesisDevice._pzmot_jog
    is_moving=KinesisDevice._is_moving
    wait_move=KinesisDevice._wait_move
    stop=KinesisDevice._pzmot_stop

    get_drive_parameters=KinesisDevice._pzmot_get_drive_parameters
    setup_drive=KinesisDevice._pzmot_setup_drive
    get_jog_parameters=KinesisDevice._pzmot_get_jog_parameters
    setup_jog=KinesisDevice._pzmot_setup_jog






class KinesisPiezoController(KinesisDevice):
    """
    Thorlabs piezo controller (TPZ/KPZ series).

    Implements FTDI chip connectivity via pyft232 (virtual serial interface).

    Args:
        conn(str): serial connection parameters (usually an 8-digit device serial number).
    """
    def __init__(self, conn, is_rack_system=False):
        super().__init__(conn,is_rack_system=is_rack_system)
        self.add_background_comm(0x0654) # randomly returned occasionally on enabling/disabling channels
        self._add_status_variable("enabled",self.is_channel_enabled,self.enable_channel)
        self._add_settings_variable("output",self.get_output_voltage,self.set_output_voltage)
        self._add_settings_variable("output_range",self.get_voltage_range,self.set_voltage_range)
        self._add_settings_variable("output_source",self.get_voltage_source,self.set_voltage_source)
        self._add_status_variable("status",lambda: self.get_status(channel="all"))
    _default_get_status=KinesisDevice._pzctl_get_status

    is_channel_enabled=KinesisDevice._pzctl_is_channel_enabled
    enable_channel=KinesisDevice._pzctl_enable_channel

    get_status_n=KinesisDevice._pzctl_get_status_n
    get_status=KinesisDevice._pzctl_get_status
    
    get_output_voltage=KinesisDevice._pzctl_get_output_voltage
    set_output_voltage=KinesisDevice._pzctl_set_output_voltage
    get_voltage_range=KinesisDevice._pzctl_get_voltage_range
    set_voltage_range=KinesisDevice._pzctl_set_voltage_range
    get_voltage_source=KinesisDevice._pzctl_get_voltage_source
    set_voltage_source=KinesisDevice._pzctl_set_voltage_source





TQuadDetectorPIDParams=collections.namedtuple("TQuadDetectorPIDParams",["p","i","d"])
TQuadDetectorSetpoint=collections.namedtuple("TQuadDetectorSetpoint",["xpos","ypos"])
TQuadDetectorReadings=collections.namedtuple("TQuadDetectorReadings",["xdiff","ydiff","sum","xpos","ypos"])
TQuadDetectorOutputParams=collections.namedtuple("TQuadDetectorOutputParams",["xmin","xmax","ymin","ymax","xgain","ygain","route","open_loop_out"])
class KinesisQuadDetector(BasicKinesisDevice):
    """
    Kinesis quadrature detectors: KPA101, TPA101, TQD001.

    Implements FTDI chip connectivity via pyft232 (virtual serial interface).

    Args:
        conn(str): serial connection parameters (usually an 8-digit device serial number).
    """
    def __init__(self, conn, timeout=3.):
        super().__init__(conn,timeout=timeout)
        self._add_settings_variable("pid_parameters",self.get_pid_parameters,self.set_pid_parameters)
        self._add_settings_variable("manual_output",self.get_manual_output,self.set_manual_output)
        self._add_status_variable("readings",self.get_readings)
        self._add_settings_variable("operation_mode",self.get_operation_mode,self.set_operation_mode)
        self._add_settings_variable("output_parameters",self.get_output_parameters,self.set_output_parameters)
    
    _invert_xdiff=True  # apparently, all returned (but not set) values for xdiff and xpos are inverted
    def _quad_req(self, subid):
        """Perform QUAD request (applicable to TQD/TPA/KPA detectors)"""
        data=self.query(0x0871,subid).data
        rsubid,=struct.unpack("<H",data[:2])
        if rsubid!=subid:
            raise RuntimeError("unexpected submessage ID in the reply: expected 0x{:02x}, got 0x{:02x}".format(subid,rsubid))
        return data[2:]
    def _quad_set(self, subid, data):
        """Perform QUAD set (applicable to TQD/TPA/KPA detectors)"""
        data=struct.pack("<H",subid)+data
        self.send_comm_data(0x0870,data)
    def get_pid_parameters(self):
        """Get current PID gain parameters ``(p, i, d)``"""
        data=self._quad_req(0x01)
        par=struct.unpack("<HHH",data)
        return TQuadDetectorPIDParams(*[v/32767 for v in par])
    def set_pid_parameters(self, p=None, i=None, d=None):
        """
        Set current PID gain parameters ``(p, i, d)``.
        
        If any parameter is ``None``, use the current value.
        """
        current_parameters=self.get_pid_parameters()
        p=current_parameters.p if p is None else p
        i=current_parameters.i if i is None else i
        d=current_parameters.d if d is None else d
        par=[int(v*32767) for v in [p,i,d]]
        par=[max(0,min(v,32767)) for v in par]
        data=struct.pack("<HHH",*par)
        self._quad_set(0x01,data)
        return self.get_pid_parameters()
    def get_manual_output(self):
        """Get current manual output values ``(xpos, ypos)`` (used in open loop mode)"""
        data=self._quad_req(0x0D)
        par=struct.unpack("<hh",data)
        par=[v/32767*10 for v in par]
        if self._invert_xdiff:
            par[0]*=-1
        return TQuadDetectorSetpoint(*par)
    def set_manual_output(self, xpos=None, ypos=None):
        """
        Set current manual output values (used in open loop mode).
        
        If any parameter is ``None``, use the current value.
        """
        current_parameters=self.get_manual_output()
        xpos=current_parameters.xpos if xpos is None else xpos
        ypos=current_parameters.ypos if ypos is None else ypos
        par=[int(v/10*32767) for v in [xpos,ypos]]
        par=[max(-32768,min(v,32767)) for v in par]
        data=struct.pack("<hh",*par)
        self._quad_set(0x0D,data)
        return self.get_manual_output()
    def get_readings(self):
        """Get current readings ``(xdiff, ydiff, sum, xpos, ypos)``"""
        data=self._quad_req(0x03)
        par=struct.unpack("<hhHhh",data)
        par=[v/32767*10 for v in par]
        par[2]*=2 # sum has double the scaling
        if self._invert_xdiff:
            par[0]*=-1
            par[3]*=-1
        return TQuadDetectorReadings(*par)
    _p_quad_oper_mode=interface.EnumParameterClass("quad_oper_mode",{"monitor":1,"open_loop":2,"closed_loop":3,"auto_loop":4})
    @interface.use_parameters(_returns="quad_oper_mode")
    def get_operation_mode(self):
        """Get current operation mode: ``"monitor"``, ``"open_loop"``, ``"closed_loop"``, or ``"auto_loop"``"""
        data=self._quad_req(0x07)
        mode,=struct.unpack("<H",data)
        return mode
    @interface.use_parameters(mode="quad_oper_mode")
    def set_operation_mode(self, mode):
        """Set current operation mode: ``"monitor"``, ``"open_loop"``, ``"closed_loop"``, or ``"auto_loop"``"""
        data=struct.pack("<H",mode)
        self._quad_set(0x07,data)
        return self.get_operation_mode()
    _p_quad_route=interface.EnumParameterClass("quad_route",{"sma_only":1,"sma_hub":2})
    _p_quad_open_loop_out=interface.EnumParameterClass("quad_open_loop_out",{"zero":1,"fixed":2})
    @interface.use_parameters(_returns=[None,None,None,None,None,None,"quad_route","quad_open_loop_out"])
    def get_output_parameters(self):
        """Get current output parameters ``(xmin, xmax, ymin, ymax, xgain, ygain, route, open_loop_out)``"""
        data=self._quad_req(0x05)
        par=struct.unpack("<hhhhHHhh",data)
        lims=[v/32767*10 for v in par[:4]]
        gains=[v/32767 for v in par[6:8]]
        return TQuadDetectorOutputParams(lims[0],lims[2],lims[1],lims[3],gains[0],gains[1],par[4],par[5])
    @interface.use_parameters(route="quad_route",open_loop_out="quad_open_loop_out")
    def set_output_parameters(self, xmin=None, xmax=None, ymin=None, ymax=None, xgain=None, ygain=None, route=None, open_loop_out=None):
        """
        Set current PID gain parameters ``(xmin, xmax, ymin, ymax, xgain, ygain, route, open_loop_out)``.
        
        `xmin`, `xmax`, `ymin`, and `ymax` specify output limits, `xgain` and `ygain` specify additional separate gain (between -1 and 1),
        `route` sets where output is routed in the closed loop mode (either ``"sma_only"`` or ``"sma_hub"``),
        `open_loop_out` specifies the output source in the open loop mode (either ``"zero"`` or ``"fixed"``).
        If any parameter is ``None``, use the current value.
        """
        current_parameters=self._wop.get_output_parameters()
        def v2i(v, scale=10):
            return max(-32768,min(32767,int(v/scale*32767)))
        xmin=v2i(current_parameters.xmin if xmin is None else xmin)
        xmax=v2i(current_parameters.xmax if xmax is None else xmax)
        ymin=v2i(current_parameters.ymin if ymin is None else ymin)
        ymax=v2i(current_parameters.ymax if ymax is None else ymax)
        xgain=v2i(current_parameters.xgain if xgain is None else xgain,scale=1)
        ygain=v2i(current_parameters.ygain if ygain is None else ygain,scale=1)
        route=current_parameters.route if route is None else route
        open_loop_out=current_parameters.open_loop_out if open_loop_out is None else open_loop_out
        data=struct.pack("<hhhhHHhh",xmin,ymin,xmax,ymax,route,open_loop_out,xgain,ygain)
        self._quad_set(0x05,data)
        return self.get_output_parameters()
