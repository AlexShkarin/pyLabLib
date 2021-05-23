from ...core.devio import backend  #@UnresolvedImport
from ...core.utils import py3, funcargparse

_depends_local=["...core.devio.backend"]

class Finesse(backend.IBackendWrapper):
    """
    Laser Quantum Finesse pump laser

    Args:
        conn: serial connection parameters (usually port)
    """
    def __init__(self, conn):
        conn=backend.SerialDeviceBackend.combine_conn(conn,("COM1",19200))
        instr=backend.SerialDeviceBackend(conn,term_read="\n",term_write="\r\n")
        backend.IBackendWrapper.__init__(self,instr)
        self._add_full_info_node("device_info",self.get_device_info)
        self._add_full_info_node("status",self.get_device_status)
        self._add_status_node("interlock",self.get_interlock_status)
        self._add_status_node("shutter",self.get_shutter_status)
        self._add_status_node("hours",self.get_work_hours)
        self._add_status_node("output_mode",self.get_output_mode)        
        self._add_settings_node("output",self.get_output,self.set_output)
        self._add_status_node("output_level",self.get_output_level)
        self._add_settings_node("output_setpoint",self.get_output_setpoint,self.set_output_level)
    
    def _parse_response(self, comm, resp):
        resp=py3.as_str(resp).strip()
        if comm[-1]=="?":
            if resp.startswith(comm[:-1]+"="):
                return resp[len(comm):]
            elif comm[:-1] in ["POWER","SERIAL","STATUS","HTEMP","PSUTEMP","CALDATE","SOFTVER","INTERLOCK","SETPOWER"]:
                return resp
            elif comm[:-1] =="SHUTTER":
                return resp[len("SHUTTER "):]
            elif comm[:-1] == "TIMERS":
                resp_all=[]
                resp_all.append(int(resp[-13:-5])/60)
                resp=self.instr.readline()
                resp=py3.as_str(resp).strip()
                resp_all.append(int(resp[-13:-5])/60)
                resp=self.instr.readline()
                resp=py3.as_str(resp).strip()
                resp_all.append(int(resp[-13:-5])/60)
                return resp_all
            else:
                raise RuntimeError("Command {} returned unexpected response: {}".format(comm,resp))
        else:
            if resp=="0":
                return resp
            raise RuntimeError("Command {} returned unexpected response: {}".format(comm,resp))
    def query(self, comm):
        """Send a query to the device and parse the reply"""
        comm=comm.strip().upper()        
        with self.instr.single_op():
            self.instr.flush_read()
            self.instr.write(comm)
            resp=self.instr.readline()
            if comm[-1]=="?":
                return self._parse_response(comm,resp)
    def get_device_info(self):
        """Get device information (serial number, software version, calibration date)"""
        return self.query("SERIAL?"),self.query("SOFTVER?"),self.query("CALDATE?") 
    def get_device_status(self):
        """Get device status, head and PSU temperature"""
        return self.query("STATUS?"),self.query("HTEMP?"),self.query("PSUTEMP?")
    def get_work_hours(self):
        """ Get the PSU run time, the Above Threshold and the Enabled time in minutes"""   
        return self.query("TIMERS?")    

    def get_interlock_status(self):
        """Get manual interlock status"""
        return self.query("INTERLOCK?")
    def get_shutter_status(self):
        """Get manual shutter status"""
        return self.query("SHUTTER?")
    def get_output_mode(self):
        """
        Get output mode.

        Can be ``"enabled"``, ``"disabled"``        
        """
        mode=self.query("STATUS?").upper()
        return mode.lower()
    def get_output(self):
        """Check if the output is enabled."""
        return self.get_output_mode()=="enabled"
    def set_output_mode(self, mode="on"):
        """
        Set output mode.

        `mode` can be ``"on"`` or ``"off"``
        """
        funcargparse.check_parameter_range(mode,"mode",["on","off"])
        self.query(mode.upper())
        return self.get_output_mode()
    def set_output(self, enabled=True):
        """Turn the output on or off"""
        return self.set_output_mode("on" if enabled else "off")
    def get_output_level(self):
        """Get the output power (in Watts)"""
        return float(self.query("POWER?")[:-1])

    def get_output_setpoint(self):
        """Get the output setpoint power (in Watts)"""
        return float(self.query("SETPOWER?")[:-1])
    def set_output_level(self, level):
        """Get the output power setpoint (in Watts)"""
        self.query("POWER={:05.2f}".format(level))
        return self.get_output_setpoint()