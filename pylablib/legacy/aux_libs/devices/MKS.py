from ...core.devio import backend  #@UnresolvedImport


class MKS9xx(backend.IBackendWrapper):
    """
    MKS 9xx series pressure gauge.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
        dev_addr (int): device address within a given controller (by default, communicate with all devices)
        timeout (float): communication operations timeout
    """
    def __init__(self, conn, dev_addr=254, timeout=10.):
        conn=backend.SerialDeviceBackend.combine_conn(conn,("COM1",115200))
        instr=backend.SerialDeviceBackend(conn,timeout=timeout,term_write="",term_read="")
        backend.IBackendWrapper.__init__(self,instr)
        self.dev_addr=dev_addr
        self._add_status_node("pressure",self.get_pressure,ignore_error=(self.instr.Error,))
    
    def query(self, reg):
        """Send a query to the device and return the reply"""
        query="@{:03d}{}?;FF".format(self.dev_addr,reg)
        self.instr.write(query)
        resp=self.instr.read_multichar_term(";FF")
        if resp[4:].startswith("NAK"):
            raise self.instr.Error("device replied with error '{}' to query '{}'".format(resp,query))
        elif resp[4:].startswith("ACK"):
            return resp[7:]
        else:
            raise self.instr.Error("unrecognized response '{}' to query '{}'".format(resp,query)) 
    def comm(self, reg, value):
        """Send a command to the device"""
        query="@{:03d}{}!{};FF".format(self.dev_addr,reg,value)
        self.instr.write(query)
        
    def get_pressure(self, chan=3):
        """Get pressure at a given channel"""
        resp=self.query("PR{}".format(chan))
        return float(resp)