from ...core.devio import comm_backend
from ...core.utils import py3

import re
import collections


class LaserQuantumError(comm_backend.DeviceError):
    """Generic Laser Quantum devices error"""
class LaserQuantumBackendError(LaserQuantumError,comm_backend.DeviceBackendError):
    """Generic Laser Quantum backend communication error"""

TDeviceInfo=collections.namedtuple("TDeviceInfo",["serial","software_version","cal_date"])
TWorkHours=collections.namedtuple("TWorkHours",["psu","laser_enabled","laser_threshold"])
TTemperatures=collections.namedtuple("TTemperatures",["head","psu"])
class Finesse(comm_backend.ICommBackendWrapper):
    """
    Laser Quantum Finesse pump laser.

    Args:
        conn: serial connection parameters (usually port)
    """
    Error=LaserQuantumError
    def __init__(self, conn):
        instr=comm_backend.new_backend(conn,"serial",term_read="\n",term_write="\r\n",defaults={"serial":("COM1",19200)},reraise_error=LaserQuantumBackendError)
        instr.setup_cooldown(write=0.01)
        comm_backend.ICommBackendWrapper.__init__(self,instr)
        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("hours",self.get_work_hours)
        self._add_status_variable("temperatures",self.get_temperatures)
        self._add_status_variable("output_status",self.get_output_status)
        self._add_status_variable("interlock",self.get_interlock_status)
        self._add_status_variable("shutter_status",self.get_shutter_status)
        self._add_settings_variable("shutter",self.is_shutter_opened,self.set_shutter)
        self._add_settings_variable("enabled",self.is_enabled,self.enable)
        self._add_settings_variable("output_setpoint",self.get_output_setpoint,self.set_output_power,ignore_error=LaserQuantumError)
        self._add_status_variable("output_power",self.get_output_power)
        self._add_status_variable("drive_current",self.get_current,ignore_error=LaserQuantumError)
    
    def _parse_response(self, comm, resp):
        resp=py3.as_str(resp).strip()
        if comm.startswith("Error"):
            raise LaserQuantumError("command returned error: '{}'".format(resp[5:]))
        if comm[-1]=="?":
            if comm.startswith("SHUTTER") and resp.startswith("SHUTTER"):
                resp=resp[len("SHUTTER"):].strip()
        return resp
    def query(self, comm, reply_lines=1):
        """
        Send a query to the device and read the reply.
        
        `reply_lines` specify the number of lines to read as a reply (almost all queries have only one line).
        """
        with self.instr.single_op():
            self.instr.flush_read()
            self.instr.write(comm.upper())
            resp=[self._parse_response(comm,self.instr.readline()) for _ in range(reply_lines)]
            return resp[0] if reply_lines==1 else resp

    def get_device_info(self):
        """Get device information ``(serial, software_version, cal_date)``"""
        return TDeviceInfo(self.query("SERIAL?"),self.query("SOFTVER?"),self.query("CALDATE?"))
    def _parse_work_hours(self, s):
        m=re.match(r".*=\s*(\d+)\s*mins$",s.lower())
        if m is None:
            raise LaserQuantumError("can't parse work hours string: {}".format(s))
        return float(m[1])/60.
    def get_work_hours(self):
        """Get the work hours (PSU run time, laser run time, laser above threshold time)"""
        return TWorkHours(*[self._parse_work_hours(ln) for ln in self.query("TIMERS?",reply_lines=3)])
    def get_temperatures(self):
        """Get device status, head temperature, and PSU temperature"""
        return TTemperatures(float(self.query("HTEMP?")[:-1]),float(self.query("PSUTEMP?")[:-1]))

    def get_output_status(self):
        """
        Get output status.

        Can be ``"enabled"`` or ``"disabled"``.
        """
        return self.query("STATUS?").lower()
    def get_interlock_status(self):
        """Get manual interlock status"""
        return self.query("INTERLOCK?").lower()
    def get_shutter_status(self):
        """Get the shutter status"""
        return self.query("SHUTTER?").lower()
    def is_shutter_opened(self):
        """Check if shutter is opened"""
        return self.get_shutter_status()=="opened"
    def set_shutter(self, opened=True):
        """Open or close the shutter"""
        self.query("SHUTTER {}".format("OPEN" if opened else "CLOSE"))
        return self.get_shutter_status()

    def is_enabled(self):
        """Check if the output is enabled"""
        return self.get_output_status()=="enabled"
    def enable(self, enabled=True):
        """Turn the output on or off"""
        self.query("ON" if enabled else "OFF")
        return self.is_enabled()
    def get_output_power(self):
        """Get the output power (in Watts)"""
        return float(self.query("POWER?")[:-1])
    def get_output_setpoint(self):
        """Get the output setpoint power (in Watts)"""
        return float(self.query("SETPOWER?")[:-1])
    def set_output_power(self, level):
        """Set the output power setpoint (in Watts)"""
        self.query("POWER={:05.2f}".format(level))
        return self.get_output_setpoint()
    def get_current(self):
        """Get the laser drive current (in %)"""
        return float(self.query("CURRENT?")[:-1])