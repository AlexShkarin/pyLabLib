from ...core.devio import backend  #@UnresolvedImport

_depends_local=["...core.devio.backend"]


class PfeifferError(RuntimeError):
    """
    Pfiffer devices reading error.
    """
    pass

class TPG261(backend.IBackendWrapper):
    """
    TPG 261 series pressure gauge.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    def __init__(self, conn):
        conn=backend.SerialDeviceBackend.combine_conn(conn,("COM1",9600))
        instr=backend.SerialDeviceBackend(conn,term_write="",term_read="\r\n")
        backend.IBackendWrapper.__init__(self,instr)
        self._add_status_node("pressure",self.get_pressure,ignore_error=(PfeifferError,))
        self._add_status_node("channel_status",self.get_channel_status)
        try:
            self.query("BAU")
        except self.instr.Error as e:
            self.close()
            raise self.instr.BackendOpenError(e)
    
    def comm(self, msg):
        """Send a command to the device"""
        self.instr.write(msg+"\r\n")
        rsp=self.instr.readline()
        if len(rsp)==1:
            if rsp[:1]==b"\x15":
                raise PfeifferError("device returned negative acknowledgement")
            elif rsp[:1]==b"\x06":
                return
        raise PfeifferError("device returned unexpected acknowledgement: {}".format(rsp))
    def query(self, msg):
        """Send a query to the device and return the reply"""
        self.comm(msg)
        self.instr.write(b"\05")
        return self.instr.readline()
        
    _pstats=["OK","underrange","overrange","sensor error","sensor off","no sensor","ID error"]
    def get_channel_status(self, channel=1):
        resp=self.query("PR{}".format(channel))
        stat=resp.split(b",")[0].strip()
        return self._pstats[int(stat)]
    def get_pressure(self, channel=1):
        """Get pressure at a given channel"""
        resp=self.query("PR{}".format(channel))
        stat,press=[s.strip() for s in resp.split(b",")]
        stat=int(stat)
        if stat:
            raise PfeifferError("pressure reading error: status {} ({})".format(stat,self._pstats[stat]))
        return float(press)