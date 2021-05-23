from ...core.devio import backend, units  #@UnresolvedImport

_depends_local=["...core.devio.backend"]

class EDFA_NP2000(backend.IBackendWrapper):
    """
    NuPhoton NP2000 EDFA (optical amplifier).
    """
    def __init__(self, port_addr, timeout=5.):
        instr=backend.SerialDeviceBackend((port_addr,19200),timeout=timeout,term_write="\n",connect_on_operation=True)
        backend.IBackendWrapper.__init__(self,instr)
        self._add_status_node("status",self.get_status)
        self._add_settings_node("enabled",lambda: self.get_status()["on"],self.set_output)
    
    def _parse_response(self, comm, resp):
        resp=[s.strip() for s in resp.splitlines() if s.strip()]
        if resp and (resp[0]==comm):
            resp=resp[1:]
        if not resp:
            raise RuntimeError("Malformed response {} to the command {}".format(resp,comm))
        if resp[-1]!="S":
            raise RuntimeError("Command {} returned an error: {}".format(comm,resp))
        return resp[:-1]
    def query(self, comm):
        comm=comm.strip()
        with self.instr.single_op():
            self.instr.flush_read()
            self.instr.write(comm)
            resp=self.instr.read_multichar_term("\r\nNP2000:>")
            self.instr.flush_read()
        return self._parse_response(comm,resp)
    
    def set_output(self, output=True):
        if output:
            self.query("edfa on")
        else:
            self.query("edfa off")
    
    def get_status_string(self):
        return self.query("fline")[0]
    
    def _parse_status_string(self, s):
        status={}
        status["full"]=s
        s=s.upper().split("  ")[0].split()
        status["mode"]=s[1]
        status["on"]=(s[2]=="LDON")
        status["ld_current"]=0. if s[7]=="LOW" else float(s[7])*1E-3
        status["ld_power"]=0. if s[6]=="LOW" else float(s[6])*1E-3
        if s[5]=="OPA":
            status["out_power"]=0.
        else:
            status["out_power"]=units.convert_power_units(float(s[5]),"dBm","W")
        status["PTemp"]=float(s[3])
        status["CTemp"]=float(s[8])
        status["TECC"]=float(s[10])
        return status
    def get_status(self):
        return self._parse_status_string(self.get_status_string())