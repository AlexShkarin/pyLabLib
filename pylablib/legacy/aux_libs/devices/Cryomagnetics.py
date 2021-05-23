from ...core.utils.py3 import textstring
from ...core.devio import SCPI, backend  #@UnresolvedImport

_depends_local=["...core.devio.SCPI"]


class LM500(SCPI.SCPIDevice):
    """
    Cryomagnetics LM500/510 level monitor.

    Channels are enumerated from 1.
    To abort filling or reset a timeout, call :meth:`.SCPIDevice.reset` method.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    def __init__(self, conn):
        conn=backend.SerialDeviceBackend.combine_conn(conn,("COM1",9600))
        SCPI.SCPIDevice.__init__(self,conn,backend="serial")
        self.instr.term_read="\n"
        self.instr.term_write="\n"
        try:
            self.write("ERROR 0")
            self.write("REMOTE")
        except self.instr.Error:
            self.close()
        self._add_settings_node("interval",self.get_interval,self.set_interval,ignore_error=(RuntimeError,))
        self._add_status_node("level",self.get_level,mux=([1,2],))
        self._add_status_node("fill_status",self.get_fill_status,mux=([1,2],))
        self._add_settings_node("high_level",self.get_high_level,self.set_high_level,mux=([1,2],1))
        self._add_settings_node("low_level",self.get_low_level,self.set_low_level,mux=([1,2],1))

    def close(self):
        """Close connection to the device"""
        try:
            self.write("LOCAL")
        finally:
            SCPI.SCPIDevice.close(self)
    _reset_comm="*RST;REMOTE"

    def _instr_write(self, msg):
        return self.instr.write(msg,read_echo=True,read_echo_delay=0.1)
    def _instr_read(self, raw=False):
        data=""
        while not data:
            data=self.instr.readline(remove_term=True).strip()
        return data

    def get_channel(self):
        """Get current measurement channel"""
        return self.ask("CHAN?","int")
    def set_channel(self, channel=1):
        """Set current measurement channel"""
        self.write("CHAN",channel)
        return self.get_channel()

    def get_type(self, channel=1):
        """Get channel type (``"LHe"`` or ``"LN"``)"""
        chan_type=self.ask("TYPE? {}".format(channel),"int")
        return ["LHe","LN"][chan_type]
    def _check_channel_LHe(self, op, channel=None):
        if channel is None:
            channel=self.get_channel()
        if self.get_type(channel)=="LN":
            raise RuntimeError("LN channel doesn't support {}".format(op))
    
    def get_mode(self):
        """Get measurement mode at the current channel (``"S"`` for sample/hold, ``"C"`` for continuous)"""
        self._check_channel_LHe("measurement modes")
        return self.ask("MODE?").upper()
    def set_mode(self, mode):
        """Set measurement mode at the current channel (``"S"`` for sample/hold, ``"C"`` for continuous)"""
        self._check_channel_LHe("measurement modes")
        self.write("MODE",mode)
        return self.get_mode()

    @staticmethod
    def _str_to_sec(s):
        s=s.strip().split(":")
        s=[int(n.strip()) for n in s]
        return s[0]*60**2+s[1]*60+s[2]
    @staticmethod
    def _sec_to_str(s):
        return "{:02d}:{:02d}:{:02d}".format(int(s/60.**2),int((s/60.)%60.),int(s%60.))
    def get_interval(self):
        """Get measurement interval in sample/hold mode (in seconds)"""
        self._check_channel_LHe("measurement intervals")
        return self._str_to_sec(self.ask("INTVL?"))
    def set_interval(self, intvl):
        """Set measurement interval in sample/hold mode (in seconds)"""
        self._check_channel_LHe("measurement intervals")
        if not isinstance(intvl,textstring):
            intvl=self._sec_to_str(intvl)
        self.write("INTVL",intvl)
        return self.get_interval()
    
    def start_meas(self, channel=1):
        """Initialize measurement on a given channel"""
        self.write("MEAS",channel)
    def _get_stb(self):
        return self.ask("*STB?","int")
    def wait_meas(self, channel=1):
        """Wait for a measurement on a given channel to finish"""
        mask=0x01 if channel==1 else 0x04
        while not self._get_stb()&mask:
            self.sleep(0.1)
    def get_level(self, channel=1):
        """Get level reading on a given channel"""
        res=self.ask("MEAS? {}".format(channel))
        return float(res.split()[0])
    def measure_level(self, channel=1):
        """Measure the level (initialize a measurement and return the result) on a given channel"""
        self.start_meas(channel=channel)
        self.wait_meas(channel=channel)
        return self.get_level(channel=channel)

    def start_fill(self, channel=1):
        """Initialize filling at a given channels"""
        self.write("FILL",channel)
    def get_fill_status(self, channel=1):
        """
        Get filling status at a given channels.
        
        Return either ``"off"`` (filling is off), ``"timeout"`` (filling timed out) or a float (time since filling started, in seconds)
        """
        res=self.ask("FILL? {}".format(channel)).lower()
        if res in {"off","timeout"}:
            return res
        spres=res.split()
        if len(spres)==1 or spres[1] in ["m","min"]:
            return float(spres[0])*60.
        if spres[1] in ["s","sec"]:
            return float(spres[0])
        raise ValueError("unexpected response: {}".format(res))

    def get_low_level(self, channel=1):
        """Get low level setting on a given channel"""
        self.set_channel(channel)
        return float(self.ask("LOW?").split()[0])
    def set_low_level(self, level, channel=1):
        """Set low level setting on a given channel"""
        self.set_channel(channel)
        self.write("LOW",level)
    def get_high_level(self, channel=1):
        """Get high level setting on a given channel"""
        self.set_channel(channel)
        return float(self.ask("HIGH?").split()[0])
    def set_high_level(self, level, channel=1):
        """Set high level setting on a given channel"""
        self.set_channel(channel)
        self.write("HIGH",level)