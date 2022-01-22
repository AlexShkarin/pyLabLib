from ...core.devio import comm_backend
from ...core.utils import general, py3

from .base import TopticaError, TopticaBackendError

import re
import collections
import time


def muxchan(*args, **kwargs):
    """Multiplex the function over its addr argument"""
    if len(args)>0:
        return muxchan(**kwargs)(args[0])
    def chan_func(self, *_, **__):
        return list(range(1,self._channels_number+1))
    return general.muxcall("channel",special_args={"all":chan_func},mux_argnames=kwargs.get("mux_argnames",None),return_kind="list",allow_partial=True)
TDeviceInfo=collections.namedtuple("TDeviceInfo",["serial","version"])
TWorkHours=collections.namedtuple("TWorkHours",["power_up","laser_on"])
TTemperatures=collections.namedtuple("TTemperatures",["diode","baseplate"])
class TopticaIBeam(comm_backend.ICommBackendWrapper):
    """
    Toptica iBeam smart laser controller.

    Args:
        conn: connection parameters - index of the Attocube ANC350 in the system (for a single controller leave 0)
        timeout(float): default operation timeout
    """
    Error=TopticaError
    def __init__(self, conn="COM1"):
        instr=comm_backend.new_backend(conn,"serial",term_read=["\r\n","CMD> "],term_write="\r\n",timeout=3.,defaults={"serial":("COM1",115200)},reraise_error=TopticaBackendError)
        super().__init__(instr)
        self._channels_number=1
        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("hours",self.get_work_hours)
        self._add_status_variable("temperatures",self.get_temperatures)
        self._add_status_variable("full_data",self.get_full_data,priority=-5)
        self._add_info_variable("channels_number",self.get_channels_number)
        self._add_settings_variable("enabled",self.is_enabled,self.enable)
        self._add_settings_variable("channel_enabled",self.is_channel_enabled, lambda v: self.enable_channel("all",v))
        self._add_settings_variable("channel_power",self.get_channel_power,lambda v: self.set_channel_power("all",v))
        self._add_status_variable("output_power",self.get_output_power)
        self._add_status_variable("drive_current",self.get_drive_current)
        self._add_status_variable("current_limits",self.get_current_limits)
        self.open()

    def open(self):
        res=super().open()
        try:
            self._flush_read()
            self.query("echo off",multiline=True,reply=False)
            self._channels_number=self._detect_channels_number()
            return res
        except self.Error:
            self.close()
            raise TopticaError("error connecting to the Toptica laser controller")
    
    _err_re=re.compile(r"%SYS-(\w)",flags=re.IGNORECASE)
    def _flush_read(self):
        self.instr.flush_read()
        time.sleep(0.005)
    def _do_query(self, comm, multiline=False, keep_whitespace=False, check_error="FEW", reply=True):
        self._flush_read()
        self.instr.write(comm)
        lines=[]
        while True:
            ln=py3.as_str(self.instr.readline(skip_empty=False,remove_term=False))
            if not keep_whitespace:
                ln=ln.strip()
            else:
                ln=ln.rstrip()
            if ln.strip() in ["[OK]","CMD>"]:
                break
            if ln or keep_whitespace:
                lines.append(ln)
        if lines and check_error:
            merr=self._err_re.match(lines[0])
            if merr and merr[1] in check_error:
                raise TopticaError("command {} resulted in error: {}".format(comm,lines[0]))
        if reply and not lines:
            raise TopticaError("expected single line, but got no response")
        if multiline:
            return lines
        elif len(lines)>1:
            raise TopticaError("expected single line, but got response {} with {} lines".format("\n".join(lines),len(lines)))
        return lines[-1] if lines else None
    def query(self, comm, multiline=False, keep_whitespace=False, check_error="FEW", reply=True):
        ntries=5
        error_delay=0.5
        for i in range(ntries):
            try:
                return self._do_query(comm,multiline=multiline,keep_whitespace=keep_whitespace,check_error=check_error,reply=reply)
            except TopticaError:
                if i==ntries-1:
                    raise
                time.sleep(error_delay)
    
    def reboot(self):
        """Reboot the laser system"""
        self.query("reset system",reply=False)
    
    def get_device_info(self):
        """Get the device info of the laser system: ``(serial, version)``"""
        serial=self.query("show serial",multiline=True)[-1]
        if serial.startswith("SN: "):
            serial=serial[4:]
        version=self.query("version")
        return TDeviceInfo(serial,version)
    def get_full_data(self, formatted=False):
        """Return the comprehensive device data"""
        ram=self.query("show data",keep_whitespace=formatted,multiline=True)
        return "\n".join(ram) if formatted else ram
    def get_work_hours(self):
        """Get the work hours (power on time and laser on time)"""
        reply=self.query("status uptime",multiline=True)
        hours={}
        for ln in reply:
            m=re.match(r"(.*):\s*(\d+)\s*h\s*\+\s*(\d+)\s*s",ln,flags=re.IGNORECASE)
            if m:
                hours[m[1].lower()]=float(m[2])+float(m[2])/3600
        return TWorkHours(hours.get("powerup",None),hours.get("laseron",None))
    
    def _detect_channels_number(self):
        return len(self._get_all_channel_powers())
    def get_channels_number(self):
        """Get number of supported laser channels"""
        return self._channels_number

    def is_enabled(self):
        """Check if the output is enabled"""
        return self.query("status laser").upper()=="ON"  # pylint: disable=no-member
    def enable(self, enabled=True):
        """Turn the output on or off"""
        self.query("laser {}".format("on" if enabled else "off"),reply=False)
        return self.is_enabled()

    @muxchan
    def is_channel_enabled(self, channel="all"):
        """Check if the specific channel is enabled"""
        return self.query("status channel {}".format(channel)).upper()=="ON"  # pylint: disable=no-member
    @muxchan(mux_argnames="enabled")
    def enable_channel(self, channel, enabled=True):
        """Turn the specific channel on or off"""
        self.query("{} {}".format("enable" if enabled else "disable",channel),reply=False)
        return self.is_channel_enabled(channel)
    
    def _get_all_channel_powers(self):
        reply=self.query("show level power",multiline=True)
        powers={}
        for ln in reply:
            m=re.match(r"CH(\d+),\s*PWR:\s*([\d.]+)\s*(mW|uW)",ln,flags=re.IGNORECASE)
            if m:
                p=float(m[2])*(1E-3 if m[3].lower()=="mw" else 1E-6)
                powers[int(m[1])]=p
        return powers
    @muxchan
    def get_channel_power(self, channel="all"):
        """Get specified channel power (in W)"""
        return self._get_all_channel_powers()[channel]
    @muxchan(mux_argnames="power")
    def set_channel_power(self, channel, power):
        """Set channel power (in W)"""
        self.query("channel {} power {:.0f} micro".format(channel,power*1E6),reply=False)
        return self.get_channel_power(channel)
    
    def get_output_power(self):
        """Get current output power (in W)"""
        p=self.query("show power",multiline=True)[-1]
        m=re.match(r"PIC\s*=\s*([\d.]+)\s*(mW|uW)",p,flags=re.IGNORECASE)
        if m:
            return float(m[1])*(1E-3 if m[2].lower()=="mw" else 1E-6)
        raise TopticaError("can not parse reply '{}' to query '{}'".format(p,"show power"))
    
    def get_drive_current(self):
        """Get current diode drive current (in A)"""
        p=self.query("show current",multiline=True)[-1]
        m=re.match(r"LDC\s*=\s*([\d.]+)\s*mA",p,flags=re.IGNORECASE)
        if m:
            return float(m[1])*1E-3
        raise TopticaError("can not parse reply '{}' to query '{}'".format(p,"show current"))
    def get_current_limits(self):
        """Get settings of all current limits (in A) as a dictionary"""
        reply=self.query("show limit",multiline=True)
        limits={}
        for ln in reply:
            m=re.match(r"(.*):\s*([\d.]+)\s*mA",ln,flags=re.IGNORECASE)
            if m:
                limits[m[1].lower()]=float(m[2])*1E-3
        return limits
    def get_temperatures(self):
        """Get settings of all current limits (in A) as a dictionary"""
        temperatures=[]
        for q in ["show temperature","show temperature system"]:
            reply=self.query(q,multiline=True)[-1]
            m=re.match(r"TEMP\s*=\s*([\d.]+)\s*C",reply,flags=re.IGNORECASE)
            if m:
                temperatures.append(float(m[1]))
            else:
                raise TopticaError("can not parse reply '{}' to query '{}'".format(reply,q))
        return TTemperatures(*temperatures)