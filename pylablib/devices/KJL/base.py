from ...core.devio import comm_backend

import collections
import re
import time



class KJLError(comm_backend.DeviceError):
    """Generic KJL device error"""
class KJLBackendError(KJLError,comm_backend.DeviceBackendError):
    """Generic KJL backend communication error"""



TKJL300DeviceInfo=collections.namedtuple("TKJL300DeviceInfo",["swver"])
class KJL300(comm_backend.ICommBackendWrapper):
    """
    KJL300 series pressure gauge.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
        addr: RS485 address (required both for RS-485 and for RS-232 communication; factory default is 1)
    """
    Error=KJLError
    def __init__(self, conn, addr=1):
        instr=comm_backend.new_backend(conn,"serial",term_read="\r",term_write="\r",defaults={"serial":("COM1",19200)},datatype="str",reraise_error=KJLBackendError)
        comm_backend.ICommBackendWrapper.__init__(self,instr)
        self.addr=addr
        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("pressure",self.get_pressure,priority=5)
        self._add_settings_variable("relay_setpoints",self.get_relay_setpoints,self.set_relay_setpoints,mux=((1,2),))
        try:
            self.query("VER")
        except self.instr.Error:
            self.close()
            raise
    
    def _make_msg(self, msg):
        return "#{:02X}{}".format(self.addr,msg)
    _reply_re=re.compile(r"^(\*|\?)(\d{2}) (.*)$")
    def _parse_reply(self, msg):
        m=self._reply_re.match(msg)
        if m is None:
            raise self.Error("can not parse the reply: {}".format(msg))
        if int(m[2])!=self.addr:
            raise self.Error("reply address {} does not agree with the set address {}".format(int(m[1]),self.addr))
        if m[1]=="?":
            raise self.Error("request raised an error: {}".format(m[3]))
        return m[3]
    def comm(self, msg):
        """Send a command to the device"""
        fmsg=self._make_msg(msg)
        freply=self.instr.ask(fmsg)
        reply=self._parse_reply(freply)
        if reply!="PROGM OK":
            raise self.Error("unexpected command reply: '{}' (expect '{}')".format(reply,"PROGM OK"))
    def query(self, msg):
        fmsg=self._make_msg(msg)
        freply=self.instr.ask(fmsg)
        return self._parse_reply(freply)
    
    def get_device_info(self):
        """Get device info (a tuple ``(swver)``)"""
        return TKJL300DeviceInfo(self.query("VER"))

    def reset(self, confirm_addr=False):
        """
        Reset the controller.
        
        If ``confirm_addr==True``, set current RS485 address again (required for resetting after some commands).
        """
        if confirm_addr:
            self.comm("SA{:02X}".format(self.addr))
        fmsg=self._make_msg("RST")
        self.instr.write(fmsg)
        time.sleep(50E-3)
    
    def _toPa(self, v):
        return float(v)*133.322 # return and set values are always in Torr
    def _fromPa(self, v):
        return "{:0.2E}".format(v/133.322) # return and set values are always in Torr
    def get_pressure(self):
        """Get current pressure in Pa"""
        return self._toPa(self.query("RD"))
    
    def get_relay_setpoints(self, relay=1):
        """
        Get relay setpoints (in Pa).
        
        `relay` is the relay index (either 1 or 2).
        Return tuple ``(on, off)`` for on-below and off-above pressures (``on`` is always smaller than ``off``)
        """
        q="RL" if relay==1 else "RH"
        return self._toPa(self.query("{}+".format(q))),self._toPa(self.query("{}-".format(q)))
    def set_relay_setpoints(self, relay=1, on=None, off=None, reset=True):
        """
        Set relay setpoints (in Pa).
        
        `relay` is the relay index (either 1 or 2). `on` and `off` are on-below and off-above pressures (``on`` is always smaller than ``off``).
        If ``reset==True``, reset the device after changing the setpoints (required to take effect).
        ``None`` values are left unchanged.
        """
        q="SL" if relay==1 else "SH"
        if on is not None:
            self.comm("{}+{}".format(q,self._fromPa(on)))
        if off is not None:
            self.comm("{}-{}".format(q,self._fromPa(off)))
        if reset:
            self.reset(confirm_addr=True)
        return self.get_relay_setpoints()
    def set_zero(self, pressure=0):
        """Set vacuum calibration point (in Pa)"""
        self.comm("TZ{}".format(self._fromPa(pressure)))
    def set_span(self, pressure=1E5):
        """Set atmosphere calibration point (in Pa)"""
        self.comm("TS{}".format(self._fromPa(pressure)))