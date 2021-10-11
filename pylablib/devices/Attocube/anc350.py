from ...core.devio import comm_backend, interface
from ...core.utils import general
from ...core.utils.strpack import unpack_int

import collections
import time
import struct

from ..interface import stage
from .base import AttocubeError, AttocubeBackendError


def get_usb_devices_number():
    """Get the number of controllers connected via USB"""
    devs=comm_backend.PyUSBDeviceBackend.list_resources(idVendor=0x16C0,idProduct=0x055B)
    return len(devs)

class ANC350(comm_backend.ICommBackendWrapper,stage.IMultiaxisStage):
    """
    Attocube ANC350 controller.

    Args:
        conn: connection parameters - index of the Attocube ANC350 in the system (for a single controller leave 0)
        timeout(float): default operation timeout
    """
    Error=AttocubeError
    _axes=[0,1,2]
    def __init__(self, conn=0, timeout=5.):
        if isinstance(conn,int):
            conn=(0x16C0,0x055B,conn,0x86,0x02,"libusb0") # default device IDs
        instr=comm_backend.new_backend(conn,backend="pyusb",timeout=timeout,check_read_size=False,reraise_error=AttocubeBackendError)
        self._corr_number=0
        self._tell_telegrams={}
        super().__init__(instr)
        self.open()
        self.instr.flush_read()
        try:
            self.get_hardware_id()
        except instr.Error:
            self.close()
            raise AttocubeError("error connecting to the ANC350 controller")
        self.set_value(0x000A,0,0) # sync request
        self.enable_updates(False)
        self._add_info_variable("hardware_id",self.get_hardware_id)
        self._add_settings_variable("voltages",self.get_voltage,lambda v: self.set_voltage("all",v))
        self._add_settings_variable("offsets",self.get_offset,lambda v: self.set_offset("all",v))
        self._add_settings_variable("frequencies",self.get_frequency,lambda v: self.set_frequency("all",v))
        self._add_status_variable("status",self.get_status)
        self._add_status_variable("positions",self.get_position)
        self._add_status_variable("target_positions",self.get_target_position)
        self._add_status_variable("sensor_voltage",self.get_sensor_voltage)
        self._add_status_variable("capacitance",lambda: self.get_capacitance(measure=False),priority=-5)
    def _make_telegram(self, opcode, address, index=0, data=b"", add_corr=True):
        data=data[:(len(data)//4)*4]
        l=16+len(data)
        if add_corr:
            self._corr_number=(self._corr_number%0xFFFF)+1
            corr_number=self._corr_number
        else:
            corr_number=0
        return struct.pack("<IIIII",l,opcode,address,index,corr_number)+data
    Telegram=collections.namedtuple("Telegram",["opcode","address","index","data","corr_number"])
    def _parse_telegram(self, telegram):
        if len(telegram)<20:
            raise ValueError("data is too short: {}".format(len(telegram)))
        l,opcode,address,index,corr_number=struct.unpack("<IIIII",telegram[:20])
        if len(telegram)!=l+4:
            raise ValueError("wrong telegram length: expected {}, got {}".format(l+4,len(telegram)))
        return self.Telegram(opcode,address,index,telegram[20:],corr_number)
    
    def _read_telegram(self, corr_number=None):
        ctd=general.Countdown(self.instr.timeout)
        while True:
            tg=self._parse_telegram(self.instr.read(512))
            if tg.opcode==3: # ACK
                if corr_number is None or tg.corr_number==corr_number:
                    return tg
                raise AttocubeError("got unexpected correlation number: {}, expected {}".format(tg.corr_number,corr_number))
            elif tg.opcode==4: # TELL
                # if (tg.address>>8)!=0x0F:
                self._tell_telegrams[(tg.address,tg.index)]=tg
            else:
                raise AttocubeError("unexpected opcode: {}".format(tg.opcode))
            if ctd.passed():
                raise AttocubeError("timeout while read")
    Reply=collections.namedtuple("Reply",["address","index","reason","data"])
    def _write(self, opcode, address, index=0, data=b""):
        if isinstance(data, int):
            data=struct.pack("<i",data)
        tg=self._make_telegram(opcode,address,index,data,add_corr=False)
        self.instr.write(tg)
    def _query(self, opcode, address, index=0, data=b""):
        if isinstance(data, int):
            data=struct.pack("<i",data)
        tg=self._make_telegram(opcode,address,index,data)
        self.instr.write(tg)
        resp=self._read_telegram(self._corr_number)
        reason,=struct.unpack("<I",resp.data[:4])
        return self.Reply(resp.address,resp.index,reason,resp.data[4:])

    def check_tell(self, timeout=0.01):
        """Check for queued TELL (periodic value update) commands"""
        try:
            with self.instr.using_timeout(timeout):
                self._read_telegram()
        except (AttocubeError,self.instr.Error):
            pass
    def _check_reason(self, reason):
        if reason==1:
            raise AttocubeError("invalid address")
        if reason==2:
            raise AttocubeError("value out of range")
        if reason==3:
            raise AttocubeError("telegram was ignored")
        if reason==4:
            raise AttocubeError("verify of data failed")
        if reason==5:
            raise AttocubeError("wrong type of data")
        if reason==99:
            raise AttocubeError("unknown error")
        elif reason!=0:
            raise AttocubeError("unknown reason: {}".format(reason))
    def set_value(self, address, index, value, ack=False):
        """
        Set device value at the given address and index.
        
        If ``ack==True``, request ACK responds and return its value; otherwise, return immediately after set.
        """
        if ack:
            resp=self._query(0,address,index,value)
            res=resp.data
            if isinstance(value,int):
                res=unpack_int(res,"<")
            self._check_reason(resp.reason)
            return res
        else:
            self._write(0,address,index,value)
    def get_value(self, address, index, as_int=True):
        """
        Get device value at the given address and index.
        
        If ``as_int==True``, convert the result into a signed integer; otherwise return raw byte string.
        """
        resp=self._query(1,address,index)
        res=resp.data
        self._check_reason(resp.reason)
        if as_int:
            res=unpack_int(res,"<")
        return res
    def _read_register(self, address):
        idx=0
        res=b""
        while True:
            data=self.get_value(address,idx,as_int=False)
            eoln_pos=data.find(b"\x00")
            if eoln_pos>=0:
                res+=data[:eoln_pos]
                return res
            res+=data
            idx+=1


    def enable_updates(self, enabled=True):
        """Enable or disable periodic TELL updates"""
        self.set_value(0x0145,0,1 if enabled else 0)
    def get_hardware_id(self):
        """Return device HWID (by default -1)"""
        return self.get_value(0x0168,0)
    def set_hardware_id(self, hwid, persist=False):
        """
        Set device HWID (can be used to identify different devices).

        If ``persist==True``, the value persists after power cycling.
        """
        self.set_value(0x016A,0,hwid)
        if persist:
            self.set_value(0x016F,0,0x1234)
    
    @stage.muxaxis
    @interface.use_parameters
    def is_connected(self, axis="all"):
        """Check if axis is connected"""
        return bool(self.get_value(0x3002,axis))
    @stage.muxaxis
    @interface.use_parameters
    def is_enabled(self, axis="all"):
        """Check if axis is enabled"""
        return bool(self.get_value(0x3030,axis))
    @stage.muxaxis(mux_argnames="enabled")
    @interface.use_parameters
    def enable_axis(self, axis="all", enabled=True):
        """Enable a specific axis or all axes"""
        self.set_value(0x3030,axis,1 if enabled else 0)
    @stage.muxaxis
    @interface.use_parameters
    def disable_axis(self, axis="all"):
        """Disable a specific axis or all axes"""
        self.set_value(0x3030,axis,0)
    
    @stage.muxaxis
    @interface.use_parameters
    def is_moving(self, axis="all"):
        """Move a given axis for a given number of steps"""
        return bool(self.get_value(0x302E,axis))
    @stage.muxaxis
    @interface.use_parameters
    def check_limit(self, axis="all"):
        """
        Check if the ent of travel has been reached.

        Return ``None`` if no limits are reached, ``"fwd"`` if forward limit is reached,
        ``"bwd"`` if backward limit is reached, or ``"both"`` if both are reached together (normally shouldn't happen).
        """
        flim=self.get_value(0x3039,axis)
        blim=self.get_value(0x303A,axis)
        return [None,"fwd","bwd","both"][flim+blim*2]
    @stage.muxaxis
    @interface.use_parameters
    def get_status_n(self, axis="all"):
        """
        Get numerical status of the axis.

        For details, see ANC350 protocol.
        """
        return self.get_value(0x0404,axis)
    status_bits=[(0x001,"running"),(0x002,"limit"),(0x100,"sens_err"),(0x400,"sens_disconn"),(0x800,"ref_valid")]
    @stage.muxaxis
    def get_status(self, axis="all"):
        """
        Get device status.

        Return list of status strings, which can include ``"running"`` (axis is moving), ``"limit"`` (one of the limits is reached),
        ``"sens_err"`` (sensor error), ``"sens_disconn"`` (sensor disconnected), or ``"ref_valid"`` (reference is valid).
        """
        status_n=self.get_status_n(axis=axis)
        return [s for (m,s) in self.status_bits if status_n&m]
    @stage.muxaxis
    @interface.use_parameters
    def get_target_position(self, axis="all"):
        """Get the target position for the given axis (the position towards which it is moving)"""
        return self.get_value(0x0408,axis)*1E-9
    @stage.muxaxis
    @interface.use_parameters
    def get_precision(self, axis="all"):
        """Get the axis precision in m (used for checking if the target is reached)"""
        return self.get_value(0x3036,axis)*1E-9
    @stage.muxaxis(mux_argnames="precision")
    @interface.use_parameters
    def set_precision(self, axis="all", precision=1E-6):
        """Set the axis precision in m (used for checking if the target is reached)"""
        self.set_value(0x3036,axis,int(precision*1E9))
        return self._wip.get_precision(axis)
    @stage.muxaxis
    @interface.use_parameters
    def is_target_reached(self, axis="all", precision=None):
        """
        Check if the target position is reached.
        
        If `precision` is not ``None``, it sets final position tolerance (in m).
        """
        if precision is not None:
            self._wip.set_precision(axis,precision)
        self.set_value(0x3036,axis,int(precision*1E9))
        return self.get_value(0x3037,axis)
    def get_sensor_voltage(self):
        """Get position sensor voltage in Volts"""
        return self.get_value(0x0526,0)*1E-3
    def set_sensor_voltage(self, voltage):
        """Set position sensor voltage in Volts"""
        self.set_value(0x0526,0,int(voltage*1E3))
        return self.get_sensor_voltage()

    @stage.muxaxis
    @interface.use_parameters
    def get_voltage(self, axis="all"):
        """Get axis step voltage in Volts"""
        return self.get_value(0x0400,axis)*1E-3
    @stage.muxaxis(mux_argnames="voltage")
    @interface.use_parameters
    def set_voltage(self, axis, voltage):
        """Set axis step voltage in Volts"""
        self.set_value(0x0400,axis,int(voltage*1E3))
        return self._wip.get_voltage(axis)
    @stage.muxaxis
    @interface.use_parameters
    def get_offset(self, axis="all"):
        """Get axis offset voltage in Volts"""
        return self.get_value(0x0514,axis)*1E-3
    @stage.muxaxis(mux_argnames="voltage")
    @interface.use_parameters
    def set_offset(self, axis, voltage):
        """Set axis offset voltage in Volts"""
        self.set_value(0x0514,axis,int(voltage*1E3))
        return self._wip.get_offset(axis)
    @stage.muxaxis
    @interface.use_parameters
    def get_frequency(self, axis="all"):
        """Get axis step frequency in Hz"""
        return self.get_value(0x0401,axis)
    @stage.muxaxis(mux_argnames="freq")
    @interface.use_parameters
    def set_frequency(self, axis, freq):
        """Set axis step frequency in Hz"""
        self.set_value(0x0401,axis,int(freq))
        return self._wip.get_frequency(axis)
    @stage.muxaxis
    @interface.use_parameters
    def get_capacitance(self, axis="all", measure=False, delay=0.5):
        """
        Get axis capacitance in F.

        If ``measure==True``, initialize the measurement and get the result after the measurement `delay`.
        Otherwise, return the last measured value.
        """
        if measure:
            self.set_value(0x051E,axis,1)
            time.sleep(delay)
        return self.get_value(0x0569,axis)*1E-12

    @stage.muxaxis
    @interface.use_parameters
    def get_position(self, axis="all"):
        """Get axis position (in m)"""
        return self.get_value(0x0415,axis)*1E-9
    @interface.use_parameters
    def move_to(self, axis, position, precision=None):
        """
        Move to target position (in m).
        
        If `precision` is not ``None``, it sets final position tolerance.
        """
        self.set_value(0x0408,axis,int(position*1E9))
        if precision is not None:
            self._wip.set_precision(axis,precision)
        self.set_value(0x040D,axis,1)
    def move_by(self, axis, dist):
        """Move along a given axis by a given distance (in m)"""
        self.move_to(axis,self.get_position(axis)+dist)
    @interface.use_parameters
    def move_by_steps(self, axis, steps=1):
        """Move along a given axis by a given number of steps"""
        steps=int(steps)
        if steps>=0:
            tg=self._make_telegram(0,0x0410,axis,b"\x01\x00\x00\x00",add_corr=False)
        else:
            tg=self._make_telegram(0,0x0411,axis,b"\x01\x00\x00\x00",add_corr=False)
            steps=-steps
        for _ in range(steps):
            self.instr.write(tg)

    def wait_move(self, axis, precision=1E-6, timeout=10., period=0.01):
        """
        Wait for a given axis to stop moving or to reach target position.

        If the motion is not finished after `timeout` seconds, raise a backend error.
        Precision sets the final positioning precision (in m).
        """
        if axis=="all":
            for ax in self.get_all_axes():
                self.wait_move(ax,timeout=timeout)
            return
        ctd=general.Countdown(timeout)
        while True:
            if (not self.is_moving(axis)) or self.is_target_reached(axis,precision=precision):
                return
            if ctd.passed():
                raise AttocubeError("axis waiting timeout error")
            time.sleep(period)

    
    @stage.muxaxis
    @interface.use_parameters
    def stop(self, axis="all"):
        """Stop motion of a given axis"""
        self.set_value(0x040E,axis,0)
    
    @interface.use_parameters
    def jog(self, axis, direction):
        """
        Jog a given axis in a given direction.
        
        `direction` can be either ``"-"`` (negative) or ``"+"`` (positive).
        The motion continues until it is explicitly stopped, or until a limit is hit.
        """
        if direction:
            self.set_value(0x040E,axis,1)
        else:
            self.set_value(0x040F,axis,1)