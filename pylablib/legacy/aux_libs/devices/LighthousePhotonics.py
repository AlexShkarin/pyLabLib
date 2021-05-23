from ...core.devio import backend  #@UnresolvedImport
from ...core.utils import py3, funcargparse

_depends_local=["...core.devio.backend"]

class SproutG(backend.IBackendWrapper):
    """
    Lighthouse Photonics Sprout G laser.

    Args:
        conn: serial connection parameters (usually port)
    """
    def __init__(self, conn):
        conn=backend.SerialDeviceBackend.combine_conn(conn,("COM1",19200))
        instr=backend.SerialDeviceBackend(conn,term_read="\r",term_write="\r\n")
        instr._operation_cooldown=0.02
        backend.IBackendWrapper.__init__(self,instr)
        self._add_full_info_node("device_info",self.get_device_info)
        self._add_full_info_node("device_config",self.get_device_config)
        self._add_status_node("warning",self.get_warning_status)
        self._add_status_node("interlock",self.get_interlock_status)
        self._add_status_node("shutter",self.get_shutter_status)
        self._add_status_node("output_mode",self.get_output_mode)
        self._add_status_node("hours",self.get_work_hours)
        self._add_settings_node("output",self.get_output,self.set_output)
        self._add_status_node("output_level",self.get_output_level)
        self._add_settings_node("output_setpoint",self.get_output_setpoint,self.set_output_level)
    
    def _parse_response(self, comm, resp, allowed_resp=None):
        resp=py3.as_str(resp).strip()
        if comm[-1]=="?":
            if not resp.startswith(comm[:-1]+"="):
                raise RuntimeError("Command {} returned unexpected response: {}".format(comm,resp))
            return resp[len(comm):]
        else:
            allowed_resp=allowed_resp or ["0"]
            if resp in allowed_resp:
                return resp
            raise RuntimeError("Command {} returned unexpected response: {}".format(comm,resp))
    def query(self, comm, allowed_resp=None):
        """
        Send a query to the device and parse the reply.
        
        `allowed_resp` is a list of valid responses (by default, only ``"0"``).
        """
        comm=comm.strip().upper()
        with self.instr.single_op():
            self.instr.flush_read()
            self.instr.write(comm)
            resp=self.instr.readline()
        return self._parse_response(comm,resp,allowed_resp=allowed_resp)

    def get_device_info(self):
        """Get device information (product name, product version, serial number)"""
        return self.query("PRODUCT?"),self.query("VERSION?"),self.query("SERIALNUMBER?")
    def get_device_config(self):
        """Get laser configuration (color and maximal power)"""
        return self.query("CONFIG?")
        
    def get_warning_status(self):
        """Get device warnings"""
        return self.query("WARNING?")
    def get_interlock_status(self):
        """Get manual interlock status"""
        return self.query("INTERLOCK?")
    def get_shutter_status(self):
        """Get manual shutter status"""
        return self.query("SHUTTER?")
    def get_work_hours(self):
        """Return device operation hours (controller on) and run hours (laser on)"""
        return self.query("HOURS?"),self.query("RUN HOURS?")

    def get_output_mode(self):
        """
        Get output mode.

        Can be ``"on"``, ``"off"``, ``"idle"`` (power standby mode), ``"calibrate"``,
        ``"interlock"`` (manual interlock is off), ``"warmup"`` (warmup mode), or ``"calibration"`` (calibration mode).
        """
        mode=self.query("OPMODE?").upper()
        return mode.lower()
    def get_output(self):
        """Check if the output is on."""
        return self.get_output_mode()=="on"
    def set_output_mode(self, mode="on"):
        """
        Set output mode.

        `mode` can be ``"on"``, ``"off"``, ``"idle"`` (power standby mode), or ``"calibrate"`` (calibration mode).
        """
        funcargparse.check_parameter_range(mode,"mode",["on","off","idle","calibrate"])
        self.query("OPMODE="+mode.upper())
        return self.get_output_mode()
    def set_output(self, enabled=True):
        """Turn the output on or off"""
        return self.set_output_mode("on" if enabled else "off")

    def get_output_level(self):
        """Set the actual output power (in Watts)"""
        return float(self.query("POWER?"))
    def get_output_setpoint(self):
        """Get the output setpoint power (in Watts)"""
        return float(self.query("POWER SET?"))
    def set_output_level(self, level):
        """Get the output power setpoint (in Watts)"""
        self.query("POWER SET={:.2d}".format(level))
        return self.get_output_setpoint()