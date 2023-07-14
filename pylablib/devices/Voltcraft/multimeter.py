from .base import GenericVoltcraftError, GenericVoltcraftBackendError
from ...core.utils import py3
from ...core.devio import SCPI, comm_backend, interface

import re
import struct
import collections
import numpy as np




class VC7055(SCPI.SCPIDevice):
    """
    Voltcraft VC-7055BT bench-top multimeter.

    Args:
        addr: device connection (usually a COM-port name such as ``"COM1"``).
    """
    Error=GenericVoltcraftError
    ReraiseError=GenericVoltcraftBackendError
    def __init__(self, addr):
        backend_defaults={"serial":("COM1",115200,8,'N',1)}
        super().__init__(addr,backend_defaults=backend_defaults)
        with self._close_on_error():
            self.get_id()
        self._add_settings_variable("functions",lambda: self.get_function("all"), lambda v: self.set_function(v,channel="all"),multiarg=False)
        self._add_settings_variable("range",self.get_range,self.set_range)
        self._add_settings_variable("autorange",self.is_autorange_enabled,self.enable_autorange)
        self._add_settings_variable("measurement_rate",self.get_measurement_rate,self.set_measurement_rate)
        self._add_status_variable("readings",lambda: self.get_reading("all"))

    def _read_echo(self, delay=0.):
        self.sleep(delay)
        self.instr.read(1)
        self.sleep(1E-2)
        self.instr.read()
    _p_function=interface.EnumParameterClass("function",
        {"volt_dc":"VOLT:DC","volt_ac":"VOLT:AC","curr_dc":"CURR:DC","curr_ac":"CURR:AC","cap":"CAP","res":"RES","fres":"FRES",
            "freq":"FREQ","per":"PER","cont":"CONT","diode":"DIOD","temp":"TEMP","none":"NONE"})
    def _normalize_function(self, func):
        func=func.strip('"').upper().split()
        if len(func)==1:
            if func[0] in ["CURR","VOLT"]:
                func=func+["DC"]
        return ":".join(func)


    _p_reading_channel=interface.EnumParameterClass("reading_channel",{"primary":1,"secondary":2})
    _reading_channels=["primary","secondary"]
    @interface.use_parameters(_returns="function",channel="reading_channel")
    def _get_single_function(self, channel):
        return self._normalize_function(self.ask("FUNC{}?".format(channel)))
    def get_function(self, channel="primary"):
        """Get measurement function for the given measurement channel (``"primary"`` or ``"secondary"``, or ``"all"`` for both channels)"""
        if channel=="all":
            return tuple(self._get_single_function(k) for k in self._reading_channels)
        return self._get_single_function(channel)
    @interface.use_parameters(function="function",channel="reading_channel")
    def _set_single_function(self, function, channel):
        if self._wap._get_single_function(channel)!=function:
            if channel==1:
                self.write("CONF:{}".format(function),read_echo=True)
            else:
                self.write("FUNC2",'"{}"'.format(function),read_echo=True)
        return self._wip._get_single_function(channel=channel)
    def set_function(self, function, channel="primary", reset_secondary=True):
        """
        Set measurement function for the given measurement channel (``"primary"``, ``"secondary"``, or ``"all"`` for both channels).
        
        If ``reset_secondary==True`` and the primary function is changed, set the secondary function to ``"none"`` to avoid conflicts.
        """
        if channel=="all" or isinstance(function,(tuple,list)):
            self._set_single_function("none","secondary")
            return tuple(self._set_single_function(f,k) for f,k in zip(function,self._reading_channels))
        if reset_secondary and channel=="primary" and self.get_function()!=function:
            self._set_single_function("none","secondary")
        return self._set_single_function(function,channel)
    
    _range_indices={"VOLT:DC":[50E-3,500E-3,5,50,500,1E3],"VOLT:AC":[500E-3,5,50,500,750],
        "CURR:DC":[500E-6,5E-3,50E-3,500E-3,5,10],"CURR:AC":[500E-6,5E-3,50E-3,500E-3,5,10],
        "RES":[500,5E3,50E3,500E3,5E6,50E6],"FRES":[500,5E3,50E3],"CAP":[50E-9,500E-9,5E-6,50E-6,500E-6,5E-3,50E-3]}
    _si_pfx={"G":1E9,"M":1E6,"k":1E3,"K":1E3,"":1,"m":1E-3,"u":1E-6,"n":1E-9,"p":1E-12}
    def get_range(self):
        """Get the present measurement range"""
        f=self._wop._get_single_function("primary")
        if f not in self._range_indices:
            return None
        rng=self.ask("RANGE?","raw").strip()[:-1]
        if rng[-2:]==b"\xa6\xcc":  # micro-range glitch for capacitance
            v,p=rng[:-2],"u"
        else:
            m=re.match(r"(\d+)\s*(G|M|k|K||m|u|n|p)",py3.as_str(rng))
            if m is None:
                raise GenericVoltcraftError("unrecognized range value: {}".format(rng))
            v,p=m.groups()
        return float(v)*self._si_pfx[p]
    def set_range(self, rng):
        """Set the present measurement range"""
        f=self._wop._get_single_function("primary")
        if f not in self._range_indices:
            return None
        rngvals=np.array(self._range_indices[f])
        closest_idx=abs(np.log(rngvals)-np.log(rng)).argmin() if rng>0 else 0
        self.write("RANGE",closest_idx+1,"int",read_echo=True,read_echo_delay=0.1)
        return self.get_range()
    
    def is_autorange_enabled(self):
        """Check if autoscaling is enabled"""
        return self.ask("AUTO?","bool")
    def enable_autorange(self, enable=True):
        """Enable or disable autoscaling"""
        if enable:
            self.write("AUTO",read_echo=True,read_echo_delay=0.1)
        else:
            self.set_range(self.get_range())
        return self.is_autorange_enabled()
    
    _p_measurement_rate=interface.EnumParameterClass("measurement_rate",{"fast":"F","med":"M","slow":"S"})
    @interface.use_parameters(_returns="measurement_rate")
    def get_measurement_rate(self):
        """Get measurement update rate (``"fast""``, ``"med"``, or ``"slow"``)"""
        return self.ask("RATE?")
    @interface.use_parameters(rate="measurement_rate")
    def set_measurement_rate(self, rate):
        """Set measurement update rate (``"fast""``, ``"med"``, or ``"slow"``)"""
        if self._wop.get_measurement_rate()!=rate:
            self.write("RATE",rate,read_echo=True,read_echo_delay=0.2)
        return self.get_measurement_rate()
    
    @interface.use_parameters(channel="reading_channel")
    def _get_single_reading(self, channel):
        if channel==2 and self.get_function("secondary")=="none":
            return None
        return self.ask("MEAS{}?".format(channel),"float")
    def get_reading(self, channel="primary"):
        """Return the latest reading of the given measurement channel (``"primary"``, ``"secondary"``, or ``"all"`` for both channels)"""
        if channel=="all":
            return tuple(self._get_single_reading(k) for k in self._reading_channels)
        return self._get_single_reading(channel)









class VC880ParseError(GenericVoltcraftError):
    """Voltcraft VC880 message parse error"""
TVC880Reading=collections.namedtuple("TVC880Reading",["func","kind","value","unit","disps","d2func"])
class VC880(comm_backend.ICommBackendWrapper):
    """
    Voltcraft VC880/VC650BT series multimeter.

    Args:
        conn: device connection (usually, either a HID path, or an integer 0-based index indicating the devices among the ones connected)
    """
    Error=GenericVoltcraftError
    def __init__(self, conn=0):
        if isinstance(conn,int):
            hid_devices=comm_backend.list_backend_resources("hid",desc=True)
            vc_devices=[dev for dev in hid_devices if (dev.vendor_id,dev.product_id)==(0x10C4,0xEA80)]
            if conn>=len(vc_devices):
                raise GenericVoltcraftError("could not find devices with index {}; {} devices available".format(conn,len(vc_devices)))
            path=vc_devices[conn].path
        else:
            path=conn
        instr=comm_backend.new_backend(path,"hid",defaults={"hid":("rep_fmt","lenpfx")},timeout=3.,reraise_error=GenericVoltcraftBackendError)
        super().__init__(instr)
        self._add_status_variable("reading",self.get_reading)
    
    _header_magic=b"\xAB\xCD"
    TMessage=collections.namedtuple("TMessage",["typ","payload"])
    def _read_single_message(self):
        hdr=self.instr.read(4)
        for _ in range(100):
            if hdr[:2]==self._header_magic:
                break
            hdr=hdr[1:]+self.instr.read(1)
        if hdr[:2]!=self._header_magic:
            raise VC880ParseError("could not find the header 0x{:02X}{:02X}".format(*self._header_magic))
        l,typ=struct.unpack("BB",hdr[2:])
        if l<3:
            raise VC880ParseError("error in the received message length: expect at least 3 bytes, got {}".format(l))
        msg_pending=self.instr.get_pending()>l-1
        msg=self.instr.read(l-1)
        payload=msg[:-2]
        rcsum,=struct.unpack(">H",msg[-2:])
        ccsum=sum(hdr)+sum(payload)
        if ccsum!=rcsum:
            raise VC880ParseError("error in the received message check sum: received at 0x{:04X}, calculated 0x{:04X}".format(rcsum,ccsum))
        return self.TMessage(typ,payload),msg_pending
    def read_message(self, tries=10):
        """Read the oldest message in the queue"""
        for t in range(tries):
            try:
                return self._read_single_message()[0]
            except VC880ParseError:
                if t==tries-1:
                    raise
    def exhaust_messages(self, nmax=100000, tries=10):
        """
        Read all messages in the queue and return them
        
        `nmax` specifies the maximal number of messages to read (``None`` means reading until available).
        """
        received=[]
        t=0
        while nmax is None or len(received)<nmax:
            try:
                msg,pending=self._read_single_message()
                received.append(msg)
                if not pending:
                    break
                t=0
            except VC880ParseError:
                t+=1
                if t==tries:
                    break
        return received
    def _build_message(self, comm, data=b""):
        hdr=self._header_magic+struct.pack("BB",len(data)+3,comm)
        csum=struct.pack(">H",sum(hdr)+sum(data))
        return hdr+data+csum
    def send_message(self, comm, data=b"", pre_exhaust=True, reps=1, post_read=0):
        """
        Send a message containing the given command and data.
        
        If ``pre_exhaust==True``, empty the read queue before sending the message (improves chances of delivery).
        `reps` specifies the number of exhaust/send cycle repetitions (improves chances of delivery).
        If `post_read` is more than 0, it specifies the number of messages to read after the command is sent.
        """
        for _ in range(reps):
            if pre_exhaust:
                self.exhaust_messages()
            self.instr.write(self._build_message(comm,data=data))
        return [self.read_message() for _ in range(post_read)]

    _functions={
        0x00:("DCV","V","V","volt_dc"),  # function, units, range_kind, function_kind
        0x01:("ACDCV","V","V","volt_acdc"),
        0x02:("DCmV","V","mV","volt_dc"),
        0x03:("freq","Hz","Hz","freq"),
        0x04:("duty_cycl","perc","perc","duty_cycl"),
        0x05:("ACV","V","V","volt_ac"),
        0x06:("res","Ohm","Ohm","res"),
        0x07:("diod","V","V","diod"),
        0x08:("short","Ohm","Ohm","short"),
        0x09:("cap","F","F","cap"),
        0x0A:("t_cels","dC","dC","temp"),
        0x0B:("t_fahr","dF","dF","temp"),
        0x0C:("DCuA","A","uA","curr_dc"),
        0x0D:("ACuA","A","uA","curr_ac"),
        0x0E:("DCmA","A","mA","curr_dc"),
        0x0F:("ACmA","A","mA","curr_ac"),
        0x10:("DCA","A","A","curr_dc"),
        0x11:("ACA","A","A","curr_ac"),
        0x12:("low_pass","V","V","low_pass")}
    _ranges={   "V":[4,40,400,1000],
                "mV":[4e-1],
                "A":[10],
                "mA":[4E-2,4E-1],
                "uA":[4E-4,4E-3],
                "Ohm":[4E2,4E3,4E4,4E5,4E6,4E7],
                "F":[4E-8,4E-7,4E-6,4E-5,4E-4,4E-3,4E-2],
                "Hz":[4E1,4E2,4E3,4E4,4E5,4E6,4E7,4E8]}
    def _decode_live(self, data):
        func,rng=data[:2]
        if func not in self._functions:
            raise GenericVoltcraftError("unrecognized function index: {:02X}".format(func))
        func,unit,rngk,kind=self._functions[func]
        rng=self._ranges.get(rngk,[1])[rng-0x30]
        pfxord=int(np.log10(rng*.99)//3)
        val=py3.as_str(data[2:9]).strip()
        stat=list(data[26:33])
        def parse_val(val):
            if val=="-"*len(val):
                return None
            elif val.upper().find("OL")>=0:
                return"over"
            else:
                return float(val)*10**(pfxord*3)
        val=parse_val(val)
        disps=[]
        for ds,de,c in [(9,16,parse_val),(16,23,int),(23,26,int)]:
            d=py3.as_str(data[ds:de]).strip()
            try:
                d=c(d) if d else None
            except ValueError:
                pass
            disps.append(d)
        d2func=None
        if stat[1]&0x08:
            d2func="max"
        elif stat[1]&0x04:
            d2func="min"
        elif stat[1]&0x02:
            d2func="avg"
        elif stat[1]&0x01:
            d2func="rel"
        return TVC880Reading(func,kind,val,unit,tuple(disps),d2func)
    _p_reading_kind=interface.EnumParameterClass("reading_kind",["latest","oldest","all"])
    @interface.use_parameters(kind="reading_kind")
    def get_reading(self, kind="latest"):
        """
        Get the multimeter reading.

        `kind` can be ``"latest"`` (return the most recent reading), ``"oldest"`` (return the oldest reading),
        or ``"all"`` (return all readings in the read queue).
        Return tuple ``(func, kind, val, unit, disps, d2func)`` with, correspondingly, specific selected function (e.g., ``"DCuA"`` or ``"res"``),
        function kind (e.g., ``"curr_dc"`` or ``"res"``), displayed value (in SI units), value units (e.g., ``"V"`` or ``"Ohm"``),
        values of the other 3 auxiliary displays (upper right min/max/avg/rel display, upper left memory display, bottom linear scale display),
        and the kind of function on the upper right display (``"min"``, ``"max"``, ``"avg"``, or ``"rel"``).
        """
        if kind=="all":
            return [self._decode_live(m.payload) for m in self.exhaust_messages() if m.type==0x01]
        if kind=="latest":
            msgs=self.exhaust_messages()
            for m in msgs[::-1]:
                if m.typ==0x01:
                    return self._decode_live(m.payload)
        for _ in range(100):
            m=self.read_message()
            if m.typ==0x01:
                return self._decode_live(m.payload)
        raise GenericVoltcraftError("could not receive a live update message")
    def enable_autorange(self, enable=True):
        """Enable or disable autorange"""
        if enable:
            self.send_message(0x47,reps=3)
        else:
            self.send_message(0x46,reps=1)