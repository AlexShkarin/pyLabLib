from ...core.devio import comm_backend
from ...core.utils import py3, funcargparse

import collections


class LighthousePhotonicsError(comm_backend.DeviceError):
    """Generic Lighthouse Photonics devices error"""
class LighthousePhotonicsBackendError(LighthousePhotonicsError,comm_backend.DeviceBackendError):
    """Generic Lighthouse Photonics backend communication error"""

TDeviceInfo=collections.namedtuple("TDeviceInfo",["product","version","serial","configuration"])
TWorkHours=collections.namedtuple("TWorkHours",["controller","laser"])
class SproutG(comm_backend.ICommBackendWrapper):
    """
    Lighthouse Photonics Sprout G laser.

    Args:
        conn: serial connection parameters (usually port)
    """
    Error=LighthousePhotonicsError
    def __init__(self, conn):
        instr=comm_backend.new_backend(conn,"serial",term_read="\r",term_write="\r\n",defaults={"serial":("COM1",19200)},reraise_error=LighthousePhotonicsBackendError)
        instr.setup_cooldown(write=0.02)
        comm_backend.ICommBackendWrapper.__init__(self,instr)
        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("hours",self.get_work_hours)
        self._add_status_variable("warning",self.get_warning_status)
        self._add_status_variable("interlock",self.get_interlock_status)
        self._add_status_variable("shutter_status",self.get_shutter_status)
        self._add_status_variable("output_mode",self.get_output_mode)
        self._add_settings_variable("enabled",self.is_enabled,self.enable)
        self._add_settings_variable("output_setpoint",self.get_output_setpoint,self.set_output_power)
        self._add_status_variable("output_power",self.get_output_power)
    
    def _parse_response(self, comm, resp, allowed_replies=("0",)):
        resp=py3.as_str(resp).strip()
        if comm[-1]=="?":
            if not resp.startswith(comm[:-1]+"="):
                raise LighthousePhotonicsError("Command {} returned unexpected response: {}".format(comm,resp))
            return resp[len(comm):]
        else:
            if resp not in allowed_replies:
                raise LighthousePhotonicsError("Command {} returned unexpected response: {}".format(comm,resp))
            return resp
    def query(self, comm, allowed_replies=("0",)):
        """Send a query to the device and parse the reply"""
        comm=comm.upper()
        with self.instr.single_op():
            self.instr.flush_read()
            self.instr.write(comm)
            resp=self.instr.readline()
        return self._parse_response(comm,resp,allowed_replies=allowed_replies)

    def get_device_info(self):
        """Get device information (product name, product version, serial number, configuration)"""
        return TDeviceInfo(self.query("PRODUCT?"),self.query("VERSION?"),self.query("SERIALNUMBER?"),self.query("CONFIG?"))
    def get_work_hours(self):
        """Return device operation hours (controller on) and run hours (laser on)"""
        return TWorkHours(self.query("HOURS?"),self.query("RUN HOURS?"))
        
    def get_warning_status(self):
        """Get device warnings"""
        return self.query("WARNING?")
    def get_interlock_status(self):
        """Get manual interlock status"""
        return self.query("INTERLOCK?")
    def get_shutter_status(self):
        """Get manual shutter status (``"open"`` or ``"close"``)"""
        return self.query("SHUTTER?")

    def get_output_mode(self):
        """
        Get output mode.

        Can be ``"on"``, ``"off"``, ``"idle"`` (power standby mode), ``"calibrate"``,
        ``"interlock"`` (manual interlock is off), ``"warmup"`` (warmup mode), or ``"calibration"`` (calibration mode).
        """
        return self.query("OPMODE?").lower()
    def set_output_mode(self, mode="on"):
        """
        Set output mode.

        `mode` can be ``"on"``, ``"off"``, ``"idle"`` (power standby mode), or ``"calibrate"`` (calibration mode).
        """
        funcargparse.check_parameter_range(mode,"mode",["on","off","idle","calibrate"])
        self.query("OPMODE={}".format(mode.upper()),allowed_replies=["0","1"])
        return self.get_output_mode()
    def is_enabled(self):
        """Check if the output is on (idle or warmup don't count as on)"""
        return self.get_output_mode()=="on"
    def enable(self, enabled=True):
        """Turn the output on or off"""
        return self.set_output_mode("on" if enabled else "off")

    def get_output_power(self):
        """Set the actual output power (in Watts)"""
        return float(self.query("POWER?"))
    def get_output_setpoint(self):
        """Get the output setpoint power (in Watts)"""
        return float(self.query("POWER SET?"))
    def set_output_power(self, level):
        """Get the output power setpoint (in Watts)"""
        self.query("POWER SET={:.2f}".format(level))
        return self.get_output_setpoint()