from ...core.devio import SCPI, units, backend  #@UnresolvedImport
from ...core.utils import strpack, general, funcargparse

import re
import time
try:
    import ft232
except (ImportError,NameError,OSError):
    pass

import collections

_depends_local=["...core.devio.SCPI"]


class PM100D(SCPI.SCPIDevice):
    """
    Thorlabs PM100D optical Power Meter.

    Args:
        addr: connection address (usually, a VISA connection string)
    """
    def __init__(self, addr):
        SCPI.SCPIDevice.__init__(self,addr)
        self._add_status_node("power",self.get_power)
    
    def setup_power_measurement(self):
        """Switch the device into power measurement mode"""
        self.write(":CONFIGURE:SCALAR:POWER")
        
    def get_power(self):
        """Get the power readings"""
        self.write(":MEASURE:POWER")
        value,unit=self.ask(":read?","value")
        return units.convert_power_units(value,unit or "W","W",case_sensitive=False)


class ThorlabsInterface(SCPI.SCPIDevice):
    """
    Generic Thorlabs device interface using Serial communication.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    _default_operation_cooldown=0.01
    _default_failsafe=True
    _allow_concatenate_write=False
    def __init__(self, conn):
        conn=backend.SerialDeviceBackend.combine_conn(conn,("COM1",115200))
        SCPI.SCPIDevice.__init__(self,conn,backend="serial",term_read=["\r","\n"],term_write="\r",timeout=5.)

    def open(self):
        SCPI.SCPIDevice.open(self)
        self.instr.flush_read()
    
    def _instr_write(self, msg):
        self.instr.flush_read()
        return self.instr.write(msg,read_echo=True)
    def _instr_read(self, raw=False):
        data=""
        while not data:
            data=self.instr.readline(remove_term=True).strip()
            while data[:1]==b">":
                data=data[1:].strip()
        return data


class FW(ThorlabsInterface):
    """
    Thorlabs FW102/202 motorized filter wheels.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
        respect_bound(bool): if ``True``, avoid crossing the boundary between the first and the last position in the wheel
    """
    def __init__(self, conn, respect_bound=True):
        ThorlabsInterface.__init__(self,conn)
        self._add_settings_node("pos",self.get_position,self.set_position)
        self._add_settings_node("pcount",self.get_pcount,self.set_pcount)
        self._add_settings_node("speed",self.get_speed,self.set_speed)
        self.pcount=self.get_pcount()
        self.respect_bound=respect_bound

    _id_comm="*idn?"
    def get_position(self):
        """Get the wheel position (starting from 1)"""
        self.flush()
        return self.ask("pos?","int")
    def set_position(self, pos):
        """Set the wheel position (starting from 1)"""
        if self.respect_bound: # check if the wheel could go through zero; if so, manually go around instead
            cur_pos=self.get_position()
            if abs(pos-cur_pos)>=self.pcount//2: # could switch by going through zero
                medp1=(2*cur_pos+pos)//3
                medp2=(cur_pos+2*pos)//3
                self.write("pos={}".format(medp1))
                self.write("pos={}".format(medp2))
                self.write("pos={}".format(pos))
            else:
                self.write("pos={}".format(pos))
        else:
            self.write("pos={}".format(pos))
        return self.get_position()

    def get_pcount(self):
        """Get the number of wheel positions (6 or 12)"""
        self.flush()
        return self.ask("pcount?","int")
    def set_pcount(self, pcount):
        self.write("pcount={}".format(pcount))
        self.pcount=self.get_pcount()
        return self.pcount

    def get_speed(self):
        """Get the motion speed"""
        self.flush()
        return self.ask("speed?","int")
    def set_speed(self, speed):
        """Set the motion speed"""
        self.write("speed={}".format(speed))
        return self.get_speed()




class MDT69xA(ThorlabsInterface):
    """
    Thorlabs MDT693/4A high-voltage source.

    Uses MDT693A program interface, so should be compatible with both A and B versions.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    def __init__(self, conn):
        ThorlabsInterface.__init__(self,conn)
        self._add_settings_node("voltage",self.get_voltage,self.set_voltage,mux=("xyz",1))
        self._add_status_node("voltage_range",self.get_voltage_range)
        try:
            self.get_id(timeout=2.)
        except self.instr.Error as e:
            self.close()
            raise self.instr.BackendOpenError(e)

    _id_comm="I"
    def get_voltage(self, channel="x"):
        """Get the output voltage in Volts at a given channel"""
        self.flush()
        if not channel.lower() in "xyz":
            raise ValueError("unrecognized channel name: {}".format(channel))
        resp=self.ask(channel.upper()+"R?")
        resp=resp.strip()[2:-1].strip()
        return float(resp)
    def set_voltage(self, voltage, channel="x"):
        """Set the output voltage in Volts at a given channel"""
        if not channel.lower() in "xyz":
            raise ValueError("unrecognized channel name: {}".format(channel))
        self.write(channel.upper()+"V{:.3f}".format(voltage))
        return self.get_voltage(channel=channel)

    def get_voltage_range(self):
        """Get the selected voltage range in Volts (75, 100 or 150)."""
        resp=self.ask("%")
        resp=resp.strip()[2:-1].strip()
        return float(resp)





class KinesisError(RuntimeError):
    """Generic Kinesis device error."""
class KinesisTimeoutError(KinesisError):
    """Kinesis timeout error."""

def list_kinesis_devices(filter_ids=True):
    """
    List all Thorlabs Kinesis devices connected ot this PC.

    Return list of tuples ``(conn, description)``.
        If ``filter_ids==True``, only leave devices with Tholabs-like IDs (8-digit numbers).
        Otherwise, show all devices (some of them might not be Thorlabs-related).
    """
    return KinesisDevice.list_devices(filter_ids=filter_ids)

class KinesisDevice(backend.IBackendWrapper):
    """
    Generic Kinesis device.

    Implements FTDI chip connectivity via pyft232 (virtual serial interface).

    Args:
        conn: serial connection parameters (usually 8-digit device serial number).
    """
    def __init__(self, conn, timeout=3.):
        conn=backend.FT232DeviceBackend.combine_conn(conn,(None,115200))
        instr=backend.FT232DeviceBackend(conn,term_write=b"",term_read=b"",timeout=timeout)
        instr._operation_cooldown=0.01
        backend.IBackendWrapper.__init__(self,instr)
        self._add_full_info_node("device_info",self.get_info)
        self._bg_msg_counters={}

    @staticmethod
    def list_devices(filter_ids=True):
        """
        List all connected devices.

        Return list of tuples ``(conn, description)``.
        If ``filter_ids==True``, only leave devices with Tholabs-like IDs (8-digit numbers).
        Otherwise, show all devices (some of them might not be Thorlabs-related).
        """
        def _is_thorlabs_id(id):
            return re.match(br"^\d{8}$",id[0]) is not None
        ids=backend.FT232DeviceBackend.list_resources(desc=True)
        if filter_ids:
            ids=[id for id in ids if _is_thorlabs_id(id)]
        return ids
    def send_comm_nodata(self, messageID, param1=0x00, param2=0x00, source=0x01, dest=0x50):
        """
        Send a message with no associated data.

        For details, see APT communications protocol.
        """
        msg=strpack.pack_uint(messageID,2,"<")+strpack.pack_uint(param1,1)+strpack.pack_uint(param2,1)+strpack.pack_uint(dest,1)+strpack.pack_uint(source,1)
        self.instr.write(msg)
    def send_comm_data(self, messageID, data, source=0x01, dest=0x50):
        """
        Send a message with associated data.

        For details, see APT communications protocol.
        """
        msg=strpack.pack_uint(messageID,2,"<")+strpack.pack_uint(len(data),2,"<")+strpack.pack_uint(dest|0x80,1)+strpack.pack_uint(source,1)
        self.instr.write(msg+data)

    CommNoData=collections.namedtuple("CommNoData",["messageID","param1","param2","source","dest"])
    CommData=collections.namedtuple("CommData",["messageID","data","source","dest"])
    def recv_comm(self):
        """
        Receive a message.

        Return either :class:`CommNoData` or :class:`CommData` depending on the message type
        (fixed length with two parameters, or variable length with associated data).
        For details, see APT communications protocol.
        """
        while True:
            msg=self.instr.read(6)
            messageID=strpack.unpack_uint(msg[0:2],"<")
            source=strpack.unpack_uint(msg[5:6])
            dest=strpack.unpack_uint(msg[4:5])
            if dest&0x80:
                dest=dest&0x7F
                datalen=strpack.unpack_uint(msg[2:4],"<")    
                data=self.instr.read(datalen)
                comm=self.CommData(messageID,data,source,dest)
            else:
                param1=strpack.unpack_uint(msg[2:3])
                param2=strpack.unpack_uint(msg[3:4])    
                comm=self.CommNoData(messageID,param1,param2,source,dest)
            if messageID in self._bg_msg_counters:
                cnt,_=self._bg_msg_counters[messageID]
                self._bg_msg_counters[messageID]=(cnt+1,comm)
            else:
                return comm
    def recv_comm_nodata(self):
        """
        Receive a fixed-length message with two parameters and no associated data.

        If the next message is variable-length, raise error.
        For details, see APT communications protocol.
        """
        msg=self.recv_comm()
        if isinstance(msg,self.CommData):
            raise KinesisError("expected fixed length message, got variable length: {}".format(msg))
        return msg
    def recv_comm_data(self):
        """
        Receive a variable-length message with associated data.

        If the next message is fixed-length, raise error.
        For details, see APT communications protocol.
        """
        msg=self.recv_comm()
        if isinstance(msg,self.CommNoData):
            raise KinesisError("expected variable length message, got fixed length: {}".format(msg))
        return msg
    def add_background_comm(self, messageID):
        """
        Mark given messageID as a 'background' message, which can be sent at any point without prompt (e.g., some operation confirmation).

        If it is received instead during ``recv_comm_`` operations, it is ignored, and the corresponding counter is increased.
        """
        self._bg_msg_counters.setdefault(messageID,(0,None))
    def check_background_comm(self, messageID):
        """Return message counter and the last message value (``None`` if not message received yet) of a given 'background' message."""
        return self._bg_msg_counters[messageID]

    DeviceInfo=collections.namedtuple("DeviceInfo",["serial_no","model_no","fw_ver","hw_type","hw_ver","mod_state","nchannels"])
    def get_info(self, dest=0x50):
        """
        Get device info.
        """
        self.send_comm_nodata(0x0005,dest=dest)
        data=self.recv_comm_data().data
        serial_no=strpack.unpack_uint(data[:4],"<")
        model_no=data[4:12].decode().strip("\x00")
        fw_ver="{}.{}.{}".format(strpack.unpack_uint(data[16:17]),strpack.unpack_uint(data[15:16]),strpack.unpack_uint(data[14:15]))
        hw_type=strpack.unpack_uint(data[12:14],"<")
        hw_ver=strpack.unpack_uint(data[78:80],"<")
        mod_state=strpack.unpack_uint(data[80:82],"<")
        nchannels=strpack.unpack_uint(data[82:84],"<")
        return self.DeviceInfo(serial_no,model_no,fw_ver,hw_type,hw_ver,mod_state,nchannels)

    def blink(self, dest=0x50):
        """Identify the physical device (by, e.g., blinking status LED or screen)"""
        self.send_comm_nodata(0x0223,dest=dest)


class MFF(KinesisDevice):
    """
    MFF (Motorized Filter Flip Mount) device.

    Implements FTDI chip connectivity via pyft232 (virtual serial interface).

    Args:
        conn: serial connection parameters (usually 8-digit device serial number).
    """
    def __init__(self, conn):
        KinesisDevice.__init__(self,conn)
        self._add_settings_node("position",self.get_position,self.set_position)
    def set_position(self, pos, channel=0):
        """Set the flip mount position (either 0 or 1)"""
        self.send_comm_nodata(0x046A,channel,2 if pos else 1)
    def get_position(self, channel=0):
        """
        Get the flip mount position (either 0 or 1).

        Return ``None`` if the mount is current moving.
        """
        self.send_comm_nodata(0x0429,channel)
        data=self.recv_comm_data().data
        status=strpack.unpack_uint(data[2:6],"<")
        if status&0x01: # low limit
            return 0
        if status&0x02: # high limit
            return 1
        if status&0x2F0: # moving
            return None
        raise RuntimeError("error getting MF10x position: status {:08x}".format(status))


class KDC101(KinesisDevice):
    """
    Thorlabs KDC101 DC servo motor controller.

    Implements FTDI chip connectivity via pyft232 (virtual serial interface).

    Args:
        conn(str): serial connection parameters (usually 8-digit device serial number).
    """
    def __init__(self, conn):
        KinesisDevice.__init__(self,conn)
        self._forward_pos=False
        self.add_background_comm(0x0464) # move completed
        self.add_background_comm(0x0466) # move stopped
        self.add_background_comm(0x0444) # homed
        self._add_status_node("position",self.get_position)
        self._add_status_node("status",self.get_status)
        self._add_settings_node("velocity_params",self.get_velocity_params,self.set_velocity_params)

    def get_status_n(self):
        """
        Get numerical status of the device.

        For details, see APT communications protocol.
        """
        self.send_comm_nodata(0x0429,0x01)
        data=self.recv_comm_data().data
        return strpack.unpack_uint(data[2:6],"<")
    status_bits=[(1<<0,"sw_bk_lim"),(1<<1,"sw_fw_lim"),
                (1<<4,"moving_bk"),(1<<5,"moving_fw"),(1<<6,"jogging_bk"),(1<<7,"jogging_fw"),
                (1<<9,"homing"),(1<<10,"homed"),(1<<12,"tracking"),(1<<13,"settled"),
                (1<<14,"motion_error"),(1<<24,"current_limit"),(1<<31,"enabled")]
    def get_status(self):
        """
        Get device status.

        Return list of status strings, which can include ``"sw_fw_lim"`` (forward limit switch reached),``"sw_bk_lim"`` (backward limit switch reached),
        ``"moving_fw"`` (moving forward), ``"moving_bk"`` (moving backward),
        ``"homing"`` (homing), ``"homed"`` (homing done), ``"tracking"``, ``"settled"``,
        ``"motion_error"`` (excessive position error), ``"current_limit"`` (motor current limit exceeded), or ``"enabled"`` (motor is enabled).
        """
        status_n=self.get_status_n()
        return [s for (m,s) in self.status_bits if status_n&m]
    def wait_for_status(self, status, enabled, timeout=None, period=0.05):
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
            curr_status=self.get_status()
            if enabled and any([s in curr_status for s in status]):
                return
            if (not enabled) and all([s not in curr_status for s in status]):
                return
            if ctd.passed():
                raise KinesisTimeoutError
            time.sleep(period)

    def home(self, sync=True, force=False, timeout=None):
        """
        Home the device.

        If ``sync==True``, wait until homing is done (with the given timeout).
        If ``force==False``, only home if the device isn't homed already.
        """
        if self.is_homed() and not force:
            return
        self.send_comm_nodata(0x0443,1)
        if sync:
            self.wait_for_home(timeout=timeout)
    def is_homing(self):
        """Check if homing is in progress"""
        return "homing" in self.get_status()
    def is_homed(self):
        """Check if the device is homed"""
        return "homed" in self.get_status()
    def wait_for_home(self, timeout=None):
        """Wait until the device is homes"""
        return self.wait_for_status("homed",True,timeout=timeout)

    _time_conv=2048/6E6 # time conversion factor
    def get_velocity_params(self, scale=True):
        """
        Get current velocity parameters ``(max_velocity, acceleration)``
        
        If ``scale==True``, return these in counts/sec and counts/sec^2 respectively; otherwise, return in internal units.
        """
        self.send_comm_nodata(0x0414,1)
        msg=self.recv_comm_data()
        data=msg.data
        acceleration=strpack.unpack_int(data[6:10],"<")
        max_velocity=strpack.unpack_int(data[10:14],"<")
        if scale:
            acceleration/=(self._time_conv**2*2**16)
            max_velocity/=(self._time_conv*2**16)
        return max_velocity,acceleration
    def set_velocity_params(self, max_velocity, acceleration=None):
        """
        Set current velocity parameters.
        
        The parameters are given in counts/sec and counts/sec^2 respectively (as returned by :meth:`get_velocity_params` with ``scale=True``).
        If `acceleration` is ``None``, use current value.
        """
        if acceleration is None:
            acceleration=self.get_velocity_params(scale=False)[1]
        else:
            acceleration*=self._time_conv**2*2**16
        max_velocity*=(self._time_conv*2**16)
        data=b"\x01\x00"+b"\x00\x00\x00\x00"+strpack.pack_int(int(acceleration),4,"<")+strpack.pack_int(int(max_velocity),4,"<")
        self.send_comm_data(0x0413,data)
        return self.get_velocity_params()
    def get_position(self):
        """Get current position"""
        self.send_comm_nodata(0x0411,1)
        msg=self.recv_comm_data()
        data=msg.data
        return strpack.unpack_int(data[2:6],"<")
    def set_position_reference(self, position=0):
        """Set position reference (actual motor position stays the same)"""
        self.send_comm_data(0x0410,b"\x01\x00"+strpack.pack_int(int(position),4,"<"))
        return self.get_position()
    def move(self, steps=1):
        """Move by `steps` (positive or negative) from the current position"""
        self.send_comm_data(0x0448,b"\x01\x00"+strpack.pack_int(int(steps),4,"<"))
    def move_to(self, position):
        """Move to `position` (positive or negative)"""
        self.send_comm_data(0x0453,b"\x01\x00"+strpack.pack_int(int(position),4,"<"))
    def jog(self, direction):
        """Jog in the given direction (``"+"`` or ``"-"``)"""
        if not direction: # 0 or False also mean left
            direction="-"
        if direction in [1, True]:
            direction="+"
        if direction not in ["+","-"]:
            raise KinesisError("unrecognized direction: {}".format(direction))
        _jog_fw=(self._forward_pos and direction=="+") or ( (not self._forward_pos) and direction=="-")
        self.send_comm_nodata(0x0457,1,1 if _jog_fw else 2)
    _moving_status=["moving_fw","moving_bk","jogging_fw","jogging_bk"]
    def is_moving(self):
        """Check if motion is in progress"""
        curr_status=self.get_status()
        return any([s in curr_status for s in self._moving_status])
    def wait_for_move(self, timeout=None):
        """Wait until motion is done"""
        return self.wait_for_status(self._moving_status,False,timeout=timeout)

    def stop(self, immediate=False, sync=True, timeout=None):
        """
        Stop the motion.

        If ``immediate==True`` make an abrupt stop; otherwise, slow down gradually.
        If ``sync==True``, wait until the motion is stopped.
        """
        self.send_comm_nodata(0x0465,1,1 if immediate else 2)
        if sync:
            self.wait_for_stop(timeout=timeout)
    def wait_for_stop(self, timeout=None):
        """Wait until stopping operation is done"""
        return self.wait_for_status(self._moving_status+["homing"],False,timeout=timeout)


class K10CR1(KinesisDevice):
    """
    Thorlabs K10CR1 rotation stage.

    Implements FTDI chip connectivity via pyft232 (virtual serial interface).

    Args:
        conn(str): serial connection parameters (usually 8-digit device serial number).
    """
    #  Implemented by Manuel Meierhofer
    def __init__(self, conn):
        KinesisDevice.__init__(self,conn)
        self._forward_pos=False
        self.add_background_comm(0x0464) # move completed
        self.add_background_comm(0x0466) # move stopped
        self.add_background_comm(0x0444) # homed
        self._add_status_node("position",self.get_position)
        self._add_status_node("status",self.get_status)
        self._add_settings_node("velocity_params",self.get_velocity_params,self.set_velocity_params)

    def get_status_n(self):
        """
        Get numerical status of the device.

        For details, see APT communications protocol.
        """
        self.send_comm_nodata(0x0429,0x01)
        data=self.recv_comm_data().data
        return strpack.unpack_uint(data[2:6],"<")
    status_bits=[(1<<0,"sw_bk_lim"),(1<<1,"sw_fw_lim"),
                (1<<4,"moving_bk"),(1<<5,"moving_fw"),(1<<6,"jogging_bk"),(1<<7,"jogging_fw"),
                (1<<9,"homing"),(1<<10,"homed"),(1<<12,"tracking"),(1<<13,"settled"),
                (1<<14,"motion_error"),(1<<24,"current_limit"),(1<<31,"enabled")]
    
    def get_status(self):
        """
        Get device status.

        Return list of status strings, which can include ``"sw_fw_lim"`` (forward limit switch reached),``"sw_bk_lim"`` (backward limit switch reached),
        ``"moving_fw"`` (moving forward), ``"moving_bk"`` (moving backward),
        ``"homing"`` (homing), ``"homed"`` (homing done), ``"tracking"``, ``"settled"``,
        ``"motion_error"`` (excessive position error), ``"current_limit"`` (motor current limit exceeded), or ``"enabled"`` (motor is enabled).
        """
        status_n=self.get_status_n()
        return [s for (m,s) in self.status_bits if status_n&m]
    
    def wait_for_status(self, status, enabled, timeout=None, period=0.05):
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
            curr_status=self.get_status()
            if enabled and any([s in curr_status for s in status]):
                return
            if (not enabled) and all([s not in curr_status for s in status]):
                return
            if ctd.passed():
                raise KinesisTimeoutError
            time.sleep(0.05)

    def home(self, sync=True, force=False, timeout=None):
        """
        Home the device.

        If ``sync==True``, wait until homing is done (with the given timeout).
        If ``force==False``, only home if the device isn't homed already.
        """
        if self.is_homed() and not force:
            return
        self.send_comm_nodata(0x0443,1)
        if sync:
            self.wait_for_home(timeout=timeout)
    def is_homing(self):
        """Check if homing is in progress"""
        return "homing" in self.get_status()
    def is_homed(self):
        """Check if the device is homed"""
        return "homed" in self.get_status()
    def wait_for_home(self, timeout=None):
        """Wait until the device is homes"""
        return self.wait_for_status("homed",True,timeout=timeout)
    
    # Conversion between real and device units (see APT communications protocol, page 38)
    _pos_conv = 136533 # in microsteps per degree
    _vel_conv = 7329109 # in microsteps per degree
    _acc_conv = 1502 # in microsteps per degree
    
    def get_velocity_params(self, scale=True):
        """
        Get current velocity parameters ``(max_velocity, acceleration)``
        
        If ``scale==True``, return these in degree/sec and degree/sec^2 respectively; otherwise, return in internal units.
        """
        self.send_comm_nodata(0x0414,1)
        msg=self.recv_comm_data()
        data=msg.data
        acceleration=strpack.unpack_int(data[6:10],"<")
        max_velocity=strpack.unpack_int(data[10:14],"<")
        if scale:
            acceleration/=self._acc_conv
            max_velocity/=self._vel_conv
        return max_velocity,acceleration
    
    def set_velocity_params(self, max_velocity, acceleration=None):
        """
        Set current velocity parameters.
        
        The parameters are given in counts/sec and counts/sec^2 respectively (as returned by :meth:`get_velocity_params` with ``scale=True``).
        If `acceleration` is ``None``, use current value.
        """
        if acceleration is None:
            acceleration=self.get_velocity_params(scale=False)[1]
        else:
            acceleration*=self._acc_conv
        max_velocity*=self._vel_conv
        data=b"\x01\x00"+b"\x00\x00\x00\x00"+strpack.pack_int(int(acceleration),4,"<")+strpack.pack_int(int(max_velocity),4,"<")
        self.send_comm_data(0x0413,data)
        return self.get_velocity_params()
    
    def get_position(self):
        """Get current position (in degrees)"""
        self.send_comm_nodata(0x0411,1)
        msg=self.recv_comm_data()
        data=msg.data
        position = strpack.unpack_int(data[2:6],"<")/self._pos_conv
        return position
    def set_position_reference(self, position=0):
        """Set position reference (actual motor position stays the same)"""
        self.send_comm_data(0x0410,b"\x01\x00"+strpack.pack_int(int(position),4,"<"))
        return self.get_position()
    def move(self, angle=1):
        """Move by `angle` (degree, positive or negative) from the current position"""
        steps = angle*self._pos_conv
        steps = round(steps)
        self.send_comm_data(0x0448,b"\x01\x00"+strpack.pack_int(int(steps),4,"<"))
    
    def move_to(self, position):
        """Move to `position` (degree, positive or negative)"""
        position*=self._pos_conv
        self.send_comm_data(0x0453,b"\x01\x00"+strpack.pack_int(int(position),4,"<"))
    def jog(self, direction):
        """Jog in the given direction (``"+"`` or ``"-"``)"""
        if not direction: # 0 or False also mean left
            direction="-"
        if direction in [1, True]:
            direction="+"
        if direction not in ["+","-"]:
            raise KinesisError("unrecognized direction: {}".format(direction))
        _jog_fw=(self._forward_pos and direction=="+") or ( (not self._forward_pos) and direction=="-")
        self.send_comm_nodata(0x0457,1,1 if _jog_fw else 2)
    _moving_status=["moving_fw","moving_bk","jogging_fw","jogging_bk"]
    def is_moving(self):
        """Check if motion is in progress"""
        curr_status=self.get_status()
        return any([s in curr_status for s in self._moving_status])
    def wait_for_move(self, timeout=None):
        """Wait until motion is done"""
        return self.wait_for_status(self._moving_status,False,timeout=timeout)

    def stop(self, immediate=False, sync=True, timeout=None):
        """
        Stop the motion.

        If ``immediate==True`` make an abrupt stop; otherwise, slow down gradually.
        If ``sync==True``, wait until the motion is stopped.
        """
        self.send_comm_nodata(0x0465,1,1 if immediate else 2)
        if sync:
            self.wait_for_stop(timeout=timeout)
    def wait_for_stop(self, timeout=None):
        """Wait until stopping operation is done"""
        return self.wait_for_status(self._moving_status+["homing"],False,timeout=timeout)