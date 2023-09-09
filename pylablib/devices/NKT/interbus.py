from ...core.utils import py3, crc, general, funcargparse
from ...core.devio import comm_backend, interface

import numpy as np

import struct
import collections
import contextlib
import threading



class InterbusError(comm_backend.DeviceError):
    """Generic Interbus device error"""
class InterbusBackendError(InterbusError,comm_backend.DeviceBackendError):
    """Generic Interbus backend communication error"""



TInterbusTelegram=collections.namedtuple("TInterbusTelegram",("dest","src","typ","payload"))
class GenericInterbusDevice(comm_backend.ICommBackendWrapper):
    """
    Generic Interbus-connected device.

    Args:
        conn: serial connection parameters (usually port, a tuple containing port and baudrate,
            or a tuple with full specification such as ``("COM1", 9600, 8, 'N', 1)``)
    """
    Error=InterbusError
    def __init__(self, conn):
        instr=comm_backend.new_backend(conn,"serial",term_read=b"\x0A",term_write="",defaults={"serial":("COM1",115200)},reraise_error=InterbusBackendError)
        self._ib_src=0x40
        self._instr_lock=threading.Lock()
        super().__init__(instr)
    
    def _ib_get_dest(self, dest):
        if dest is None:
            return self.ib_dest
        return dest
    def ib_get_default_address(self):
        """Get destination address used by default in Interbus methods"""
        return self.ib_dest
    def ib_set_default_address(self, dest):
        """Set destination address used by default in Interbus methods"""
        self.ib_dest=dest
    @contextlib.contextmanager
    def ib_using_address(self, dest):
        """Context manager for temporary using a different default destination address"""
        cdest=self.ib_dest
        self.ib_dest=dest
        try:
            yield
        finally:
            self.ib_dest=cdest

    def _ib_crc(self, msg):
        return crc.crc(msg,0x1021)
    _ib_echar={0x0A,0x0D,0x5E}
    _ib_eechar={0x4A,0x4D,0x9E}
    def _ib_wrap_escape(self, msg):
        res=[0x0D]
        for c in msg:
            if c in self._ib_echar:
                res.append(0x5E)
                res.append(c+0x40)
            else:
                res.append(c)
        res.append(0x0A)
        return bytes(res)
    def _ib_unescape(self, msg):
        res=[]
        esc=False
        for c in msg:
            if esc:
                if c not in self._ib_eechar:
                    ebytes=", ".join("0x{:02X}".format(v) for v in self._ib_eechar)
                    raise InterbusError("faulty escape sequence: got byte 0x{:02X}, expected bytes {}".format(c,ebytes))
                res.append(c-0x40)
                esc=False
                continue
            if c==0x5E:
                esc=True
            else:
                res.append(c)
        if esc:
            raise InterbusError("faulty escape sequence: escape character is not followed by any other character")
        return bytes(res)
    def _ib_build_telegram(self, dest, src, typ, payload):
        msg=struct.pack("BBB",dest,src,typ)+py3.as_bytes(payload)
        crcv=struct.pack(">H",self._ib_crc(msg))
        return self._ib_wrap_escape(msg+crcv)
    def _ib_send_telegram(self, dest, src, typ, payload):
        msg=self._ib_build_telegram(dest,src,typ,payload)
        self.instr.write(msg)
    def _ib_recv_telegram(self):
        c=self.instr.read(1)
        if c!=b"\x0D":
            raise InterbusError("wrong telegram start: expected 0x{:02X}, got 0x{:02X}".format(0x0D,c[0]))
        msg=self.instr.readline()
        msg=self._ib_unescape(msg)
        if len(msg)<5:
            raise InterbusError("telegram should be at least 5 bytes long; got {}".format(len(msg)))
        ecrc=self._ib_crc(msg[:-2])
        rcrc,=struct.unpack(">H",msg[-2:])
        if ecrc!=rcrc:
            raise InterbusError("CRC error: expected 0x{:04X}, got 0x{:04X}".format(ecrc,rcrc))
        return TInterbusTelegram(msg[0],msg[1],msg[2],msg[3:-2])
    _ib_telegram_typs={0:"faulty_telegram",1:"crc_error",2:"busy",3:"ack",4:"read",5:"write",8:"reply"}
    def _ib_check_telegram(self, telegram, src=None, dest=None, typ=None):
        if src is not None and telegram.src!=src:
            raise InterbusError("unexpected telegram source: expected 0x{:02x}, got 0x{:02x}".format(src,telegram.src))
        if dest is not None and telegram.dest!=dest:
            raise InterbusError("unexpected telegram destination: expected 0x{:02x}, got 0x{:02x}".format(dest,telegram.dest))
        if telegram.typ==0:
            raise InterbusError("device has not understood telegram {}".format(repr(telegram.payload)))
        if telegram.typ==1:
            raise InterbusError("device reports CRC error for telegram {}".format(repr(telegram.payload)))
        if telegram.typ==2:
            raise InterbusError("device is busy and can not process telegram {}".format(repr(telegram.payload)))
        if typ is not None and telegram.typ!=typ:
            raise InterbusError("unexpected telegram destination: expected {}({}), got {}({})".format(
                    typ,self._ib_telegram_typs.get(typ,"unknown"),telegram.typ,self._ib_telegram_typs.get(telegram.typ,"unknown")))
    _p_ib_dtype=interface.EnumParameterClass("ib_dtype",{"raw":"raw","str":"str","u8":"B","u16":"<H","u32":"<I","i8":"b","i16":"<h","i32":"<i"})
    @interface.use_parameters(dtype="ib_dtype")
    def ib_get_reg(self, dest, address, dtype="raw", array="auto"):
        """
        Get register value at the given destination device and register address.

        `dtype` is the register type, which can be ``"raw"`` (raw bytes), ``"str"`` (string),
        ``"u8"``, ``"u16"``, ``"u32"``, ``"i8"``, ``"i16"``, ``"i32"`` (different integer values).
        """
        with self._instr_lock:
            self._ib_send_telegram(dest,self._ib_src,4,struct.pack("B",address))
            tg=self._ib_recv_telegram()
        self._ib_check_telegram(tg,src=dest,dest=self._ib_src,typ=8)
        if len(tg.payload)<1:
            raise InterbusError("request returned zero payload")
        if tg.payload[0]!=address:
            raise InterbusError("request returned unexpected address: expected 0x{:02x}, got 0x{:02x}".format(address,tg.payload[0]))
        val=tg.payload[1:]
        if dtype=="raw":
            return val
        if dtype=="str":
            return py3.as_str(val)
        l={"B":1,"b":1,"<H":2,"<h":2,"<I":4,"<i":4}[dtype]
        if array=="auto":
            array=len(val)>l
        if array and len(val)%l:
            raise InterbusError("register type {} expects multiple of {} bytes, got {}".format(self._p_ib_dtype.i(dtype),l,len(val)))
        if (not array) and len(val)!=l:
            raise InterbusError("register type {} expects {} bytes, got {}".format(self._p_ib_dtype.i(dtype),l,len(val)))
        if array:
            return [struct.unpack(dtype,val[i:i+l])[0] for i in range(0,len(val),l)]
        else:
            return struct.unpack(dtype,val)[0]
    _p_ib_dtype=interface.EnumParameterClass("ib_dtype",{"raw":"raw","str":"str","u8":"B","u16":"<H","u32":"<I","i8":"b","i16":"<h","i32":"<i"})
    @interface.use_parameters(dtype="ib_dtype")
    def ib_set_reg(self, dest, address, value, dtype="raw", array="auto", echo=True):
        """
        Set register value at the given destination device and register address.

        `dtype` is the register type, which can be ``"raw"`` (raw bytes), ``"str"`` (string),
        ``"u8"``, ``"u16"``, ``"u32"``, ``"i8"``, ``"i16"``, ``"i32"`` (different integer values).

        If ``echo==True``, return the subsequent value of the register.
        """
        if array=="auto":
            array=funcargparse.is_sequence(value)
        if dtype in {"raw","str"}:
            value=bytes(value)
        else:
            if array:
                value=b"".join([struct.pack(dtype,int(v)) for v in value])
            else:
                value=struct.pack(dtype,int(value))
        with self._instr_lock:
            self._ib_send_telegram(dest,self._ib_src,5,struct.pack("B",address)+value)
            tg=self._ib_recv_telegram()
        self._ib_check_telegram(tg,src=dest,dest=self._ib_src,typ=3)
        if len(tg.payload)<1:
            raise InterbusError("request returned zero payload")
        if tg.payload[0]!=address:
            raise InterbusError("request returned unexpected address: expected 0x{:02x}, got 0x{:02x}".format(address,tg.payload[0]))
        if echo:
            return self.ib_get_reg(dest,address,dtype=dtype,array=array)

    def ib_scan_devices(self, dests="all", timeout=0.05):
        """
        Scan for devices on the bus and return their addresses and types.

        `dests` is a list of addresses to check (``"all"`` means all addresses from 1 to 48 inclusive)
        `timeout` is the timeout to wait for each device reply.
        `func` and `payload` specify the message to send (by default, 'read coil' command with no arguments, which should always return and error)
        Since the addresses are polled consecutively, this function can take a long time (~25s for the default settings).
        """
        if dests=="all":
            dests=range(1,49)
        detected={}
        with self._instr_lock:
            with self.instr.using_timeout(timeout):
                for d in dests:
                    self._ib_send_telegram(d,self._ib_src,4,b"\x61")
                    try:
                        tg=self._ib_recv_telegram()
                        self._ib_check_telegram(tg,src=d,dest=self._ib_src,typ=8)
                        if len(tg.payload)>=2 and tg.payload[0]==0x61:
                            detected[tg.src]=tg.payload[1]
                    except InterbusError:
                        pass
        return detected







class IInterbusModule(interface.IDevice):
    """
    Specific Interbus module.

    Deals with specific registers available for this module.

    Args:
        ib_device: instance of the generic Interbus controller used to access the module.
        dest: module address on the bus.
    """
    def __init__(self, ib_device, dest):
        super().__init__()
        self.ib_device=ib_device
        self.dest=dest
        with self._close_on_error():
            self.dtype=self.get_register("type")
            self.serial=self.get_register("serial")
            if self._ib_type is not None and self.dtype!=self._ib_type:
                raise InterbusError("device at destination 0x{:02X} has unexpected type: expected 0x{:02X}, got 0x{:02X}".format(dest,self._ib_type,self.dtype))
        def make_getter(r):
            return lambda: self.get_register(r)
        for r in self._ib_registers:
            self._add_info_variable(r,make_getter(r))
        if "status_bits" in self._ib_registers:
            self._add_info_variable("status",self.get_status)
    def _get_connection_parameters(self):
        return self.ib_device._get_connection_parameters(),self.dest
    _ib_type=None
    _ib_registers={  # name: (addr, dtype, fmt=None, array=False)
        "type":(0x61,"u8"),
        "serial":(0x65,"str"),
        "status_bits":(0x66,"u16"),
        }
    _ib_registers_defaults={}
    _ib_status_bits={0x0001:"emission", 0x0002:"interlock_off", 
                    0x0010:"disabled", 0x0020:"supply_low", 0x0040:"module_temperature_out_of_range",
                    0x8000:"error_present"}
    def get_register(self, name):
        """Get value of the given register based on its name"""
        if name not in self._ib_registers:
            raise ValueError("unrecognized register: {}".format(name))
        rdesc=self._ib_registers[name]
        addr,dtype,fmt,arr=rdesc+(None,False)[len(rdesc)-2:]
        try:
            value=self.ib_device.ib_get_reg(self.dest,addr,dtype,array=bool(arr))
        except InterbusError:
            if name in self._ib_registers_defaults:
                return self._ib_registers_defaults[name]
            raise
        if arr:
            value=np.array(value)
        if fmt is not None:
            if fmt[0]=="fact":
                value=value*fmt[1]
            if fmt[0]=="map":
                value=fmt[1](value)
        return value
    def get_all_registers(self):
        """Get values of all defined registers"""
        return {n:self.get_register(n) for n in self._ib_registers}
    def set_register(self, name, value):
        """Set value of the given register based on its name"""
        if name not in self._ib_registers:
            raise ValueError("unrecognized register: {}".format(name))
        rdesc=self._ib_registers[name]
        addr,dtype,fmt,arr=rdesc+(None,False)[len(rdesc)-2:]
        if arr:
            if arr=="auto" and not funcargparse.is_sequence(value):
                value=[value]
            value=np.asarray(value)
        if fmt is not None:
            if fmt[0]=="fact":
                value=value/fmt[1]
        self.ib_device.ib_set_reg(self.dest,addr,value,dtype,array=bool(arr),echo=False)
        return self.get_register(name)
    
    def get_status(self):
        """Get device status as a set of set bits"""
        status=self.get_register("status_bits")
        return [n for m,n in self._ib_status_bits.items() if status&m]
    def __repr__(self):
        return "{}(dest = {}, type = 0x{:02X}, serial = '{}')".format(type(self).__name__,self.dest,self.dtype,self.serial)



class GenericInterbusModule(IInterbusModule):
    _ib_name="generic"
    _ib_status_bits={(1<<i):"bit{:02d}".format(i) for i in range(16)}


class SuperKExtremeInterbusModule(IInterbusModule):
    _ib_type=0x60
    _ib_name="superK_extreme"
    _ib_registers=general.merge_dicts(IInterbusModule._ib_registers, {
        "system_type":(0x6B,"u8"),
        "emission":(0x30,"u8"),
        "setup":(0x31,"u16"),
        "interlock":(0x32,"u16"),
        "pulse_picker_ratio":(0x34,"u16"),
        "watchdog_interval":(0x36,"u8"),
        "temperature_inlet":(0x11,"i16",("fact",0.1)),
        "power":(0x37,"u16",("fact",0.1)),
        "current":(0x38,"u16",("fact",0.1)),
        "nim_delay":(0x39,"u16",("fact",9E-12)),
    })
    _ib_registers_defaults={"system_type":0}
    _ib_status_bits=general.merge_dicts(IInterbusModule._ib_status_bits, {
        0x0004: "interlock_power_fail", 0x0008:"interlock_loop_off",  0x0080: "clock_battery_low_voltage",
        0x2000: "crc_startup_error", 0x4000: "log_error"
    })

class SuperKFrontPanelInterbusModule(IInterbusModule):
    _ib_name="superK_front_panel"
    _ib_type=0x61
    _ib_registers=general.merge_dicts(IInterbusModule._ib_registers, {
        "panel_lock":(0x3D,"u8"),
        "display_text":(0x72,"str",("map",lambda v: "".join((c if ord(c)<128 else "#") for c in v)))
    })
    del _ib_registers["status_bits"]

class SuperKSelectDriverInterbusModule(IInterbusModule):
    _ib_name="superK_select_driver"
    _ib_type=0x66
    _ib_registers=general.merge_dicts(IInterbusModule._ib_registers, {
        "power_on":(0x30,"u8"),
        "setup":(0x31,"u16",None),
        "min_wavelength":(0x34,"u32",("fact",1E-12)),
        "max_wavelength":(0x35,"u32",("fact",1E-12)),
        "temperature_crystal":(0x38,"i16",("fact",0.1)),
        "fsk_mode":(0x3B,"u8"),
        "internal_ctl":(0x3C,"u8"),
        "crystal":(0x75,"u8"),
    })
    for i in range(8):
        _ib_registers["wavelength{}".format(i)]=(0x90+i,"u32",("fact",1E-12),"auto")
    for i in range(8):
        _ib_registers["amplitude{}".format(i)]=(0xB0+i,"u16",("fact",0.1),"auto")
    for i in range(8):
        _ib_registers["modgain{}".format(i)]=(0xC0+i,"u16",("fact",0.1))
    _ib_status_bits=general.merge_dicts(IInterbusModule._ib_status_bits, {
        0x2000: "aod_comm_timeout", 0x4000: "need_crystal_info"
    })

class SuperKSelectInterbusModule(IInterbusModule):
    _ib_name="superK_select"
    _ib_type=0x67
    _ib_registers=general.merge_dicts(IInterbusModule._ib_registers, {
        "mon_input1":(0x10,"u16",("fact",0.1)),
        "mon_input2":(0x11,"u16",("fact",0.1)),
        "mon_input1_gain":(0x32,"u8"),
        "mon_input2_gain":(0x33,"u8"),
        "rf_switch":(0x34,"u8"),
        "mon_switch":(0x35,"u8"),
        "min_wavelength1":(0x90,"u32",("fact",1E-12)),
        "max_wavelength1":(0x91,"u32",("fact",1E-12)),
        "min_wavelength2":(0xA0,"u32",("fact",1E-12)),
        "max_wavelength2":(0xA1,"u32",("fact",1E-12)),
    })
    _ib_registers_defaults={"mon_input1_gain":0,"mon_input2_gain":0}
    _ib_status_bits=general.merge_dicts(IInterbusModule._ib_status_bits, {
        0x0004: "interlock_loop_in", 0x0008:"interlock_loop_out",  0x0080: "clock_battery_low_voltage",
        0x0100: "shutter_sensor1", 0x0200: "shutter_sensor2", 0x0400: "new_temperature1", 0x0800: "new_temperature2", 
    })


_ib_modules={m._ib_type:m for m in [SuperKExtremeInterbusModule,SuperKFrontPanelInterbusModule,SuperKSelectDriverInterbusModule,SuperKSelectInterbusModule]}








class InterbusSystem(GenericInterbusDevice):
    """
    A collection of NKT modules connected to the same Interbus.

    Args:
        conn: serial connection parameters (usually port, a tuple containing port and baudrate,
            or a tuple with full specification such as ``("COM1", 9600, 8, 'N', 1)``)
        modules: Interbus modules identifiers; can be ``"auto"`` (detect all connected modules),
            a list of module addresses, or a dictionary ``{addr: name}`` of the aliases for the modules
            (e.g., ``{'laser':15, 'varia':18}``)
    
    Attributes:
        m: dictionary of modules, defined either by their address or by their name (if provided upon creation)
    """
    def __init__(self, conn, modules="auto"):
        super().__init__(conn)
        self.m=self._find_modules(modules)
        self._add_info_variable("module_dests",lambda: list(self.m))
        self._add_info_variable("all_registers",self.get_all_module_registers)
    
    def __getitem__(self, key):
        return self.m[key]
    def __contains__(self, key):
        return key in self.m
    def _find_modules(self, modules):
        names=modules if isinstance(modules,dict) else {}
        modules=self.ib_scan_devices(dests="all" if modules=="auto" else modules)
        return {names.get(m,m):_ib_modules.get(t,GenericInterbusModule)(self,m) for m,t in modules.items()}
    def get_all_module_registers(self):
        """Get all registers"""
        return {m:d.get_all_registers() for m,d in self.m.items()}