from ...core.devio import interface, comm_backend
from ...core.utils import py3, general
from .base import ThorlabsError, ThorlabsBackendError

import contextlib
import collections
import time





def muxaddr(*args, argname="addr", **kwargs):
    """Multiplex the function over its addr argument"""
    if len(args)>0:
        return muxaddr(**kwargs)(args[0])
    def all_addr_func(self, *_, **__):
        return self._addrs
    def def_addr_func(self, *_, **__):
        return self._default_addr
    return general.muxcall(argname,special_args={"all":all_addr_func,None:def_addr_func},mux_argnames=kwargs.get("mux_argnames",None),return_kind="dict",allow_partial=True)

TDeviceInfo=collections.namedtuple("TDeviceInfo",["serial_no","model_no","year","fw_ver","hw_ver","travel","pulse"])
TMotorInfo=collections.namedtuple("TMotorInfo",["loop","motor","current","ramp_up","ramp_down","fw_freq","bk_freq"])
class ElliptecMotor(comm_backend.ICommBackendWrapper):
    """
    Basic Elliptec stage device.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
        addrs: list of device addresses (between 0 and 15) connected to this serial port; if ``"all"``, automatically detect all connected devices
        default_addr: address used by default when not supplied; by default, use the first address among the connected
        scale: scale of the position units to the internals units;
            can be ``"stage"`` (use stage units such as mm or deg based on its internal calibration),
            ``"step"`` (directly use step units), or a number which multiplies user-supplied units to produce steps
        timeout: default communication timeout
        valid_status: status which are considered valid and do not raise an error on status check
    """
    Error=ThorlabsError
    def __init__(self, conn, addrs="all", default_addr=None, scale="stage", timeout=3., valid_status=("ok","mech_timeout")):
        defaults={"serial":{"baudrate":9600}}
        instr=comm_backend.new_backend(conn,backend=("auto","serial"),term_write=b"",term_read=b"\r\n",timeout=timeout,
            defaults=defaults,reraise_error=ThorlabsBackendError)
        instr.setup_cooldown(write=0.01)
        super().__init__(instr)
        self._bg_msg_counters={}
        self.add_background_comm("BO")
        self.add_background_comm("BS")
        self._valid_status=valid_status
        self._requested_addrs=addrs
        self._default_addr=None
        self._default_scale=scale
        if not (scale in ["stage","step"] or isinstance(scale,(int,float))):
            raise ValueError("scale can be 'stage', 'step', or a number converting step units into the desired user units; supplied value is {}".format(scale))
        with self._close_on_error():
            self.update_connected_addrs()
        self._default_addr=(self._addrs[0] if self._addrs else 0) if default_addr is None else default_addr
        self._add_info_variable("device_info",lambda: self.get_device_info(addr="all"))
        self._add_info_variable("addrs",lambda: self._addrs)
        self._add_info_variable("scale",lambda: self.get_scale(addr="all"))
        self._add_status_variable("status",lambda: self.get_status(addr="all"))
        self._add_status_variable("position",lambda: self.get_position(addr="all"))
        self._add_status_variable("velocity",lambda: self.get_velocity(addr="all"))
        self._add_status_variable("motor_info",lambda: self._get_all_motor_info(addr="all"))
    
    _pre_move_delay=0.1
    def _detect_devices(self, addrs="all", timeout=0.5, delay=0.1):
        if addrs=="all":
            addrs=list(range(16))
        for a in addrs:
            self.send_comm("gs",addr=a)
            time.sleep(delay)
        valid=set()
        with self.instr.using_timeout(timeout=timeout):
            try:
                for _ in range(len(addrs)):
                    comm=self.recv_comm()
                    valid.add(comm.addr)
            except self.Error:
                pass
        return sorted(valid)
    def get_connected_addrs(self):
        """Get a list of all connected device addresses"""
        return list(self._addrs)
    def update_connected_addrs(self, addrs=None):
        """Update the list of connected device addresses"""
        if addrs is not None:
            self._requested_addrs=addrs
        self._model_no={}
        self._stage_scale={}
        self._addrs=self._detect_devices(self._requested_addrs)
        if self._requested_addrs and not self._addrs:
            raise self.Error("could not detect any connected devices among the ones specified ({})".format(addrs))
        for a in self._addrs:
            dev_info=self.get_device_info(addr=a)
            self._model_no[a]=dev_info.model_no
            self._stage_scale[a]=dev_info.pulse/dev_info.travel if dev_info.pulse>0 else 1
        self._scale={a:self._default_scale for a in self._addrs}
        if self._default_addr is not None and self._default_addr not in self._addrs:
            self._default_addr=self._addrs[0] if self._addrs else 0
    def _change_addr(self, addr, newaddr):
        if addr in self._addrs:
            self._addrs[self._addrs.index(addr)]=newaddr
            if self._default_addr==addr:
                self._default_addr=newaddr
            for d in [self._model_no,self._stage_scale,self._scale]:
                d[newaddr]=d.pop(addr)
    def get_default_addr(self):
        """Get the current default address"""
        return self._default_addr
    def set_default_addr(self, addr):
        """Set the current default address"""
        self._default_addr=addr
    def _get_addr(self, addr):
        return self._default_addr if addr is None else addr
    @contextlib.contextmanager
    def using_default_addr(self, addr):
        """Context manager which temporarily changes the default address"""
        curr_addr,self._default_addr=self._default_addr,addr
        try:
            yield
        finally:
            self._default_addr=curr_addr

    def send_comm(self, comm, data="", addr=None):
        """
        Send a message with the given data to the devices at a given address.

        For details, see ELLx communications protocol.
        """
        msg="{:01X}{}{}".format(self._get_addr(addr),comm,data)
        self.instr.write(msg)
    CommData=collections.namedtuple("CommData",["comm","data","addr"])
    _default_data_lengths={"IN":30,"GS":2,"I1":22,"I2":22,"I3":22,"PO":8,"HO":8,"GJ":8,"GV":2,"BS":2,"BO":8}
    def _read_single_comm(self, datalen="auto", timeout=None):
        with self.instr.using_timeout(timeout):
            header=self.instr.read(3)
        haddr=int(header[0:1],16)
        hcomm=py3.as_str(header[1:3])
        bgcomm=hcomm in self._bg_msg_counters
        data=self.instr.readline()
        if (datalen=="auto") or bgcomm:
            datalen=self._default_data_lengths.get(hcomm,None)
        if datalen is not None and len(data)!=datalen:
            raise ThorlabsError("unexpected reply data length for command {}: expected {}, got {}".format(hcomm,datalen,len(data)))
        return self.CommData(hcomm,data,haddr),bgcomm
    def recv_comm(self, comm=None, addr=None, datalen="auto", timeout=None):
        """
        Receive a message.

        `comm`, `addr`, and `datalen` can specify the expected return command, address, or the length of the data field
        (if ``"auto"``, determine based on the return command).
        `timeout` specifies the waiting timeout (by default, same as supplied upon the device connection).

        For details, see ELLx communications protocol.
        """
        while True:
            reply,bgcomm=self._read_single_comm(datalen=datalen, timeout=timeout)
            if bgcomm:
                cnt,_=self._bg_msg_counters[reply.comm].get(reply.addr,(0,None))
                self._bg_msg_counters[reply.comm][reply.addr]=cnt+1,reply
            else:
                if addr is not None and reply.addr!=addr:
                    raise ThorlabsError("unexpected reply address: expected {:01X}, got {:01X}".format(addr,reply.addr))
                if comm is not None:
                    if not isinstance(comm,(list,tuple,set)):
                        comm=[comm]
                    if reply.comm not in comm:
                        raise ThorlabsError("unexpected reply command: expected {}, got {}".format(comm,reply.comm))
                return reply
    def query(self, comm, data="", addr=None, reply_comm=None, reply_addr="auto", reply_datalen="auto", timeout=None):
        """
        Send a query to the device and receive the reply.

        A combination of :meth:`send_comm` and :meth:`recv_comm`.
        """
        addr=self._get_addr(addr)
        self.instr.read()
        self.send_comm(comm,data=data,addr=addr)
        if reply_addr=="auto":
            reply_addr=addr
        return self.recv_comm(comm=reply_comm,addr=reply_addr,datalen=reply_datalen,timeout=timeout)
    def add_background_comm(self, comm):
        """
        Mark given `comm` as a 'background' message, which can be sent by the device at any point without prompt (e.g., some operation confirmation).

        If it is received instead during ``recv_comm`` or ``query`` operations, it is ignored, and the corresponding counter is increased.
        """
        self._bg_msg_counters.setdefault(comm,{})
    def check_background_comm(self, comm, addr=None):
        """Return message counter and the last message value (``None`` if not message received yet) of a given 'background' message received from the given address"""
        return self._bg_msg_counters[comm].get(addr,(0,None))
    
    @muxaddr
    def change_addr(self, newaddr, addr=None):
        """Change the device address to a new value (between 0 and 15)"""
        reply=self.query("ca",data="{:01X}".format(newaddr),addr=addr,reply_comm="GS",reply_addr=newaddr)
        result=self._check_status_reply(reply)
        self._change_addr(addr,newaddr)
        return result
    @muxaddr
    def store_parameters(self, addr=None):
        """Store current device parameters (e.g., frequencies) to the energy-independent memory"""
        reply=self.query("us",addr=addr,reply_comm="GS")
        return self._check_status_reply(reply)
    
    @muxaddr
    def get_device_info(self, addr=None):
        """
        Get device info.

        Return tuple ``(serial_no, model_no, year, fw_ver, hw_ver, travel, pulse)``.
        """
        reply=self.query("in",addr=addr,reply_comm="IN")
        model_no=int(reply.data[:2],16)
        serial_no=py3.as_str(reply.data[2:10])
        year=int(reply.data[10:14])
        fw_ver=int(reply.data[14:16],16)
        hw_ver=int(reply.data[16:18],16)
        travel=int(reply.data[18:22],16)
        pulse=int(reply.data[22:30],16)
        return TDeviceInfo(serial_no,model_no,year,fw_ver,hw_ver,travel,pulse)
    
    _status_codes={0:"ok",1:"comm_timeout",2:"mech_timeout",3:"not_supported",4:"value_out_of_range",
        5:"isolated",6:"out_of_isolation",7:"init_error",8:"therm_error",9:"busy",10:"sens_error",11:"motor_error",12:"out_of_range",13:"overcurrent"}
    def _parse_status(self, status, check=True, clear_status=True):
        status=self._status_codes.get(status,"reserved")
        if check and status not in self._valid_status:
            if clear_status:
                self.query("gs")  # clear the fault status (otherwise it is returned as the next status result)
            raise ThorlabsError("faulty status: {}".format(status))
        return status
    def _check_status_reply(self, reply, check=True, clear_status=True):
        if reply.comm!="GS":
            return
        return self._parse_status(int(reply.data,16),check=check,clear_status=clear_status)
    @muxaddr
    def get_status(self, addr=None):
        """Get device status"""
        reply=self.query("gs",addr=addr,reply_comm="GS",timeout=10)
        return self._check_status_reply(reply,check=False)
    
    _p_motor=interface.EnumParameterClass("motor",[1,2,3,"all"])
    @muxaddr
    def _get_all_motor_info(self, addr=None):
        info=[]
        for m in range(1,4):
            try:
                info.append(self.get_motor_info(motor=m,addr=addr))
            except ThorlabsError:
                pass
        return info
    @muxaddr
    @interface.use_parameters
    def get_motor_info(self, motor=1, addr=None):
        """
        Get info for a given motor (between 1 and 3).
        
        Return tuple ``(loop_ena, motor_ena, current, ramp_up, ramp_down, fw_freq, bk_freq)``.
        """
        comm="i{}".format(motor)
        reply=self.query(comm,addr=addr,reply_comm=[comm.upper(),"GS"])
        self._check_status_reply(reply)
        loop_ena=bool(int(reply.data[0]))
        motor_ena=bool(int(reply.data[1]))
        current=int(reply.data[2:6],16)/1866
        ramp_up=int(reply.data[6:10],16)
        ramp_down=int(reply.data[10:14],16)
        fw_freq=14740000/int(reply.data[14:18],16)
        bk_freq=14740000/int(reply.data[18:22],16)
        return TMotorInfo(loop_ena,motor_ena,current,ramp_up,ramp_down,fw_freq,bk_freq)
    
    @muxaddr
    def get_scale(self, addr=None):
        """
        Get scale parameter for the specified address.
        
        Can be ``"stage"``, ``"step"``, or a proportionality coefficient.
        """
        return self._scale[addr]
    @muxaddr
    def set_scale(self, scale, addr=None):
        """
        Set scale parameter for the specified address.
        
        Can be ``"stage"``, ``"step"``, or a proportionality coefficient.
        """
        if not (scale in ["stage","step"] or isinstance(scale,(int,float))):
            raise ValueError("scale can be 'stage', 'step', or a number converting step units into the desired user units; suppleid value is {}".format(scale))
        self._scale[addr]=scale
        return self._scale[addr]
    def _to_steps_data(self, v, addr):
        addr=self._get_addr(addr)
        if self._scale[addr]=="stage":
            v=v*self._stage_scale[addr]
        elif self._scale[addr]!="step":
            v=v*self._scale[addr]
        v=int(v)%2**32
        return "{:08X}".format(v)
    def _from_steps_data(self, v, addr):
        addr=self._get_addr(addr)
        v=int(v,16)
        v=(v+2**31)%2**32-2**31
        if self._scale[addr]=="stage":
            return v/self._stage_scale[addr]
        if self._scale[addr]!="step":
            return v/self._scale[addr]
        return v
    _p_home_dir=interface.EnumParameterClass("home_dir",{"cw":0,"ccw":1})
    @muxaddr
    @interface.use_parameters
    def home(self, home_dir="cw", paddles="all", addr=None):
        """
        Home the device.

        The operation is synchronous, i.e., it will not finish until the homing is done.
        If the device is a rotary stage, then `home_dir` specifies homing direction (``"cw"`` or ``"ccw"``).
        If the device is a paddle polarization controller, then `paddles` is a list of all paddle indices (1 to 3) to home (``"all"`` is the same as ``[1,2,3]``).
        """
        if self._model_no[addr]==3:
            paddles=[1,2,3] if paddles=="all" else [p for p in paddles if 1<=p<=3]
            data="{:01X}".format(sum(1<<(p-1) for p in paddles))
        else:
            data="{:01X}".format(home_dir)
        reply=self.query("ho",data=data,addr=addr,reply_comm=["GS","PO"])
        self._check_status_reply(reply)
        return reply.comm=="PO"
    @muxaddr
    def get_home_offset(self, addr=None):
        """Get homing offset"""
        reply=self.query("go",addr=addr,reply_comm="HO")
        return self._from_steps_data(reply.data,addr)
    @muxaddr
    def set_home_offset(self, offset, addr=None):
        """Set homing offset (note: the manufacturer advises against it)"""
        reply=self.query("so",data=self._to_steps_data(offset,addr),addr=addr,reply_comm="GS")
        self._check_status_reply(reply)
        return self.get_home_offset(addr=addr)
    
    @muxaddr
    def get_velocity(self, addr=None):
        """Get velocity as a percentage from the maximal velocity (0 to 100)"""
        reply=self.query("gv",addr=addr,reply_comm="GV")
        return int(reply.data,16)
    @muxaddr
    def set_velocity(self, velocity=100, addr=None):
        """Set velocity as a percentage from the maximal velocity (0 to 100)"""
        reply=self.query("sv",data="{:02X}".format(int(velocity)),addr=addr,reply_comm="GS")
        self._check_status_reply(reply)
        return self.get_velocity(addr=addr)

    @muxaddr
    def get_frequency(self, motor=1, addr=None):
        """Get frequencies at a given motor as a tuple ``(fw_freq, bk_freq)``"""
        mi=self.get_motor_info(motor=motor,addr=addr)
        return mi.fw_freq,mi.bk_freq
    @muxaddr
    @interface.use_parameters
    def set_frequency(self, fw_freq=None, bk_freq=None, motor=1, addr=None):
        """
        Set frequencies at a given motor.

        Values set as ``None`` stay the same.
        """
        for pfx,freq in [("f",fw_freq),("b",bk_freq)]:
            if freq is not None:
                comm="{}{}".format(pfx,motor)
                reply=self.query(comm,data="{:04X}".format(int(round(14740000/freq))),addr=addr,reply_comm="GS")
                self._check_status_reply(reply)
        return self.get_frequency(motor=motor,addr=addr)
    @muxaddr
    @interface.use_parameters
    def search_frequency(self, motor=1, addr=None):
        """
        Run the automated frequency search on a given motor.
        
        The position might change slightly throughout the process.
        """
        comm="s{}".format(motor)
        reply=self.query(comm,addr=addr,reply_comm="GS",timeout=10)
        self._check_status_reply(reply)
        return self.get_frequency(motor=motor,addr=addr)
    
    @muxaddr
    def get_position(self, addr=None):
        """Get the current position"""
        reply=self.query("gp",addr=addr,reply_comm="PO")
        return self._from_steps_data(reply.data,addr)
    @muxaddr
    def move_to(self, position, addr=None, timeout=30.):
        """
        Move to the given position.

        The operation is synchronous, i.e., it will not finish until the motion is stopped.
        Return ``True`` if the position was reached successfully or ``False`` otherwise.
        """
        time.sleep(self._pre_move_delay)  # if the move command is issued to soon after a previous one, it can move to 0 instead
        reply=self.query("ma",data=self._to_steps_data(position,addr),addr=addr,reply_comm=["GS","PO"],timeout=timeout)
        self._check_status_reply(reply)
        return reply.comm=="PO"
    @muxaddr
    def move_by(self, distance, addr=None, timeout=30.):
        """
        Move by the given distance.

        The operation is synchronous, i.e., it will not finish until the motion is stopped.
        Return ``True`` if the position was reached successfully or ``False`` otherwise.
        """
        time.sleep(self._pre_move_delay)  # if the move command is issued to soon after a previous one, it can move to 0 instead
        reply=self.query("mr",data=self._to_steps_data(distance,addr),addr=addr,reply_comm=["GS","PO"],timeout=timeout)
        self._check_status_reply(reply)
        return reply.comm=="PO"