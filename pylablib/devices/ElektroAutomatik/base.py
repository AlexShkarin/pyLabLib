from ...core.utils import py3, funcargparse
from ...core.devio import comm_backend

import collections
import struct



class ElektroAutomatikError(comm_backend.DeviceError):
    """Generic Elektro Automatik device error"""
class ElektroAutomatikBackendError(ElektroAutomatikError,comm_backend.DeviceBackendError):
    """Generic Elektro Automatik backend communication error"""



TDeviceInfo=collections.namedtuple("TDeviceInfo",["model","manufacturer","serial_no","article_no","sw_ver"])
TOutputLimits=collections.namedtuple("TOutputLimits",["voltage","current","power"])
TStatus=collections.namedtuple("TStatus",["enabled","mode","ovp","ocp","opp","otp"])
class PS2000B(comm_backend.ICommBackendWrapper):
    """
    Elektro Automatik PS2000B series power supply.

    Args:
        conn: serial connection parameters (usually, COM-port address)
        remote_mode: approach to setting the remote mode; can be ``"force"`` (enable on connection, disable on disconnection)
            or ``"manual"`` (do nothing about it, should be enabled or disabled automatically).
            In the remote mode the device is controlled from the PC (front panel controls are disabled),
            while in the local mode it can only be queried remotely, but not changed.
    """
    Error=ElektroAutomatikError
    def __init__(self, conn, remote_mode="force"):
        funcargparse.check_parameter_range(remote_mode,"remote_mode",["force","manual"])
        self._remote_mode="manual"
        instr=comm_backend.new_backend(conn,"serial",term_read="",term_write="",defaults={"serial":("COM1",115200,8,"O",1)},reraise_error=ElektroAutomatikBackendError)
        super().__init__(instr)
        self._add_info_variable("device_info",self.get_device_info)
        self._add_info_variable("output_limits",self.get_output_limits)
        self._add_settings_variable("remote",self.is_remote_enabled,self.enable_remote)
        self._add_settings_variable("enabled",self.is_output_enabled,self.enable_output)
        self._add_status_variable("status",self.get_status)
        self._add_settings_variable("ocp_threshold",self.get_ocp_threshold,self.set_ocp_threshold)
        self._add_settings_variable("ovp_threshold",self.get_ovp_threshold,self.set_ovp_threshold)
        self._add_settings_variable("voltage_setpoint",self.get_voltage_setpoint,self.set_voltage)
        self._add_status_variable("voltage",self.get_voltage)
        self._add_settings_variable("current_setpoint",self.get_current_setpoint,self.set_current)
        self._add_status_variable("current",self.get_current)
        self._remote_mode=remote_mode
        with self._close_on_error():
            self._output_limits=self.get_output_limits()
            self._setup_remote("open")

    def _build_telegram(self, obj, data=None, dlen=None, dnode=0x00, ctype=0x01, ttype=0x01, direction=0x01):
        if data is None:
            data=b""
        else:
            data=data[:16]
            dlen=len(data)
        data=data[:16]
        sd=(dlen-1)|((direction&0x01)<<4)|((ctype&0x01)<<5)|((ttype&0x03)<<6)
        body=struct.pack("BBB",sd,dnode,obj)+py3.as_builtin_bytes(data)
        cs=sum(list(body))
        return body+struct.pack(">H",cs)
    TTelegram=collections.namedtuple("TTelegram",["obj","data","dnode"])
    def _read_telegram(self):
        sd,dnode,obj=struct.unpack("BBB",self.instr.read(3))
        dlen=(sd&0x0F)+1
        if (sd>>4)&0x01:
            raise ElektroAutomatikError("error in the received telegram direction field: expected 0, got 1")
        if (sd>>5)&0x01:
            raise ElektroAutomatikError("error in the received telegram broadcast field: expected 0, got 1")
        if (sd>>6)&0x03!=0x02:
            raise ElektroAutomatikError("error in the received telegram transmission type field: expected 2, got {}".format(sd>>6)&0x03)
        # if (sd>>4)&0x01:
        #     raise ElektroAutomatikError("error in the received telegram direction field: expected 0, got 1")
        data=self.instr.read(dlen)
        cs,=struct.unpack(">H",self.instr.read(2))
        ecs=sum(list(data))+sd+dnode+obj
        if cs!=ecs:
            raise ElektroAutomatikError("error in the received telegram checksum: expected 0x{:04X}, got 0x{:04X}".format(ecs,cs))
        return self.TTelegram(obj,data,dnode)
    _error_desc={0x03:"check sum incorrect",0x04:"start delimiter incorrect",0x05:"wrong output address",0x07:"object not defined",0x08:"object length incorrect",
        0x09:"no read/write permission",0x0F:"device is in lock state",0x30:"upper limit exceeded",0x31:"lower limit exceeded"}
    def _check_ack(self, reply):
        v=reply.data[0]
        if not v:
            return
        if v in self._error_desc:
            desc=self._error_desc[v]
        else:
            desc="unknown (0x{:02X})".format(v)
        raise ElektroAutomatikError("query or command returned an error: {}".format(desc))
    
    def _setup_remote(self, event):
        if self.is_opened() and self._remote_mode=="force":
            if event=="open":
                self.enable_remote(True)
            if event=="close":
                self.enable_remote(False)
    def open(self):
        super().open()
        self._setup_remote("open")
    def close(self):
        self._setup_remote("close")
        return super().close()

    def query(self, obj, dlen, dnode=0, kind="raw"):
        """
        Query value of the given object.

        `dlen` specifies the value length and `dnode` sets the device node (only relevant for multi-source models).
        `kind` specifies the result kind; can be ``"raw"`` (raw bytes), ``"str"`` (string), ``"int"`` (2-byte integer) or ``"float"`` (r-byte float).
        """
        funcargparse.check_parameter_range(kind,"kind",["raw","str","int","float"])
        tg=self._build_telegram(obj,dlen=dlen,dnode=dnode)
        self.instr.write(tg)
        reply=self._read_telegram()
        if reply.obj==0xFF:
            return self._check_ack(reply)
        if reply.obj!=obj:
            raise ElektroAutomatikError("error in the received object: expected {}, got {}".format(obj,reply.obj))
        if reply.dnode!=dnode:
            raise ElektroAutomatikError("error in the received device node: expected {}, got {}".format(dnode,reply.dnode))
        if kind=="raw":
            return reply.data
        if kind=="str":
            return py3.as_str(reply.data.rstrip(b"\x00"))
        if kind=="int":
            if len(reply.data)%2:
                raise ElektroAutomatikError("'int' field length should be divisible by 2; got {}".format(len(reply.data)))
            values=struct.unpack(">"+"H"*(len(reply.data)//2),reply.data)
            return values[0] if len(values)==1 else values
        if kind=="float":
            if len(reply.data)%4:
                raise ElektroAutomatikError("'float' field length should be divisible by 4; got {}".format(len(reply.data)))
            values=struct.unpack(">"+"f"*(len(reply.data)//4),reply.data)
            return values[0] if len(values)==1 else values
    def comm(self, obj, value, dnode=0, kind="int"):
        """
        Set value of the given object.

        `dnode` sets the device node (only relevant for multi-source models).
        `kind` specifies the value kind; can be ``"raw"`` (raw bytes), or ``"int"`` (2-byte integer).
        """
        funcargparse.check_parameter_range(kind,"kind",["raw","int"])
        if kind=="int":
            value=struct.pack(">H",value)
        tg=self._build_telegram(obj,data=value,dnode=dnode,ttype=3)
        self.instr.write(tg)
        reply=self._read_telegram()
        self._check_ack(reply)
    
    def get_device_info(self):
        """
        Get device information.

        Return tuple ``(model, manufacturer, serial_no, article_no, sw_ver)``.
        """
        model=self.query(0,16,kind="str")
        manufacturer=self.query(8,16,kind="str")
        serial_no=self.query(1,16,kind="str")
        article_no=self.query(6,16,kind="str")
        sw_ver=self.query(9,16,kind="str")
        return TDeviceInfo(model,manufacturer,serial_no,article_no,sw_ver)
    def get_output_limits(self):
        """
        Get nominal output limits.

        Return tuple ``(voltage, current, power)``.
        """
        voltage=self.query(2,4,kind="float")
        current=self.query(3,4,kind="float")
        power=self.query(4,4,kind="float")
        return TOutputLimits(voltage,current,power)
    
    def is_remote_enabled(self):
        """Check if the remote-control mode is enabled (if it is disabled, output and limit values can be read but not set)"""
        return (self.query(71,2,kind="int")[0]>>8)&0x03==0x01
    def enable_remote(self, enable=True):
        """Enable or disable the remote-control mode (if it is disabled, output and limit values can be read but not set)"""
        if enable!=self.is_remote_enabled():
            self.comm(54,b"\x10"+(b"\x10" if enable else b"\x00"),kind="raw")
        return self.is_remote_enabled()

    def is_output_enabled(self):
        """Check if the output is enabled"""
        return bool(self.query(71,2,kind="int")[0]&0x01)
    def enable_output(self, enable=True):
        """Enable or disable the output"""
        self.comm(54,b"\x01"+(b"\x01" if enable else b"\x00"),kind="raw")
        return self.is_output_enabled()

    def get_status(self):
        """
        Get device status.

        Return tuple ``(mode, ovp, ocp, opp, otp)``, where ``mode`` is the output mode (``"cv"`` or ``"cc"``)
        and the rest of the values show if the corresponding protection is tripped.
        """
        stat=self.query(71,6,kind="raw")[1]
        enabled=bool(stat&0x01)
        mode={0x00:"cv",0x01:"cc"}.get((stat>>1)&0x03,"unknown")
        ovp=bool((stat>>4)&0x01)
        ocp=bool((stat>>5)&0x01)
        opp=bool((stat>>6)&0x01)
        otp=bool((stat>>7)&0x01)
        return TStatus(enabled,mode,ovp,ocp,opp,otp)
    
    def get_voltage_setpoint(self):
        """Get output voltage setpoint"""
        return self.query(50,2,kind="int")/256/100*self._output_limits.voltage
    def get_voltage(self):
        """Get the actual output voltage"""
        return self.query(71,6,kind="int")[1]/256/100*self._output_limits.voltage
    def set_voltage(self, value):
        """Set output voltage setpoint"""
        value=min(int(value/self._output_limits.voltage*100*256),100*256)
        self.comm(50,value)
        return self.get_voltage_setpoint()
    def get_current_setpoint(self):
        """Get output current setpoint"""
        return self.query(51,2,kind="int")/256/100*self._output_limits.current
    def get_current(self):
        """Get the actual output current"""
        return self.query(71,6,kind="int")[2]/256/100*self._output_limits.current
    def set_current(self, value):
        """Set output current setpoint"""
        value=min(int(value/self._output_limits.current*100*256),100*256)
        self.comm(51,value)
        return self.get_current_setpoint()
    
    def get_ovp_threshold(self):
        """Get over-voltage protection threshold"""
        return self.query(38,2,kind="int")/256/100*self._output_limits.voltage
    def set_ovp_threshold(self, value):
        """Set over-voltage protection threshold"""
        value=min(int(value/self._output_limits.voltage*100*256),110*256)
        self.comm(38,value)
        return self.get_ovp_threshold()
    def get_ocp_threshold(self):
        """Get over-current protection threshold"""
        return self.query(39,2,kind="int")/256/100*self._output_limits.current
    def set_ocp_threshold(self, value):
        """Set over-current protection threshold"""
        value=min(int(value/self._output_limits.current*100*256),110*256)
        self.comm(39,value)
        return self.get_ocp_threshold()