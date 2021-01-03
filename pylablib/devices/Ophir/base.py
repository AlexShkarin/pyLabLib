from ...core.devio import comm_backend
from ...core.utils import py3, units
import collections

_depends_local=["...core.devio.comm_backend"]

class OphirDevice(comm_backend.ICommBackendWrapper):
    """
    Generic Ophir device.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    def __init__(self, conn):
        conn=comm_backend.SerialDeviceBackend.combine_conn(conn,("COM1",9600))
        instr=comm_backend.SerialDeviceBackend(conn,term_read="\r\n",term_write="\r\n")
        comm_backend.ICommBackendWrapper.__init__(self,instr)
    
    def _parse_response(self, comm, resp):
        resp=resp.strip()
        if resp.startswith(b"?"):
            raise RuntimeError("Command {} returned error: {}".format(comm,resp[1:].strip()))
        if resp.startswith(b"*"):
            return py3.as_str(resp[1:].strip())
        raise RuntimeError("Command {} returned unrecognized response: {}".format(comm,resp))
    def query(self, comm):
        """Send a query to the device and parse the reply"""
        comm=comm.strip()
        with self.instr.single_op():
            self.instr.flush_read()
            self.instr.write(comm)
            resp=self.instr.readline()
        return self._parse_response(comm,resp)


class VegaPowerMeter(OphirDevice):
    """
    Ophir Vega power meter.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    def __init__(self, conn):
        OphirDevice.__init__(self,conn)
        self._add_device_variable("power",self.get_power)
        self._add_settings_variable("wavelength",self.get_wavelength,self.set_wavelength)
        self._add_device_variable("wavelength_info",self.get_wavelength_info)
        self._add_device_variable("range_info",self.get_range_info)
        self._add_settings_variable("range_idx",self.get_range_idx,self.set_range_idx)
        self._add_settings_variable("filter_in",self.is_filter_in,self.set_filter)

    def get_power(self):
        """Get the current power readings"""
        power=self.query("$SP")
        if power.lower()=="over":
            return "over"
        return float(power)

    WavelengthInfo=collections.namedtuple("WavelengthInfo",["mode","rng","curr_idx","presets","curr_wavelength"])
    def get_wavelength_info(self):
        """
        Get wavelength setting info.

        Return tuple ``(mode, rng, curr_idx, presets, curr_wavelength)``, where
        `mode` is the measurement mode (``"CONTINUOUS"`` or ``"HOLD"``), `rng` is full wavelength range (in m),
        `curr_idx` is the current wavelength preset index, `presets` is the list of all preset wavelengths (in m),
        and `curr_wavelength` is the current measurement wavelength (in m).
        """
        info=[i.strip() for i in self.query("$AW").split() if i.strip()]
        mode=info[0]
        rng=(float(info[1])*1E-9,float(info[2])*1E-9)
        curr_idx=int(info[3])
        presets=[float(w)*1E-9 for w in info[4:] if w.upper()!="NONE"]
        return self.WavelengthInfo(mode,rng,curr_idx-1,presets,presets[curr_idx-1])
    def get_wavelength(self):
        """Get current calibration wavelength"""
        return self.get_wavelength_info().curr_wavelength
    def set_wavelength(self, wavelength):
        """Set current calibration wavelength"""
        self.query("$WL{:d}".format(int(wavelength*1E9)))
        return self.get_wavelength()

    RangeInfo=collections.namedtuple("RangeInfo",["curr_idx","ranges","curr_range"])
    def get_range_info(self):
        """
        Get power range info.

        Return tuple ``(curr_idx, ranges, curr_range)``, where `curr_idx` is the current power range index,
        `ranges` is the list of ranges (in W) for all indices and `curr_range` is the current range (in W).
        """
        info=[i.strip() for i in self.query("$AR").split() if i.strip()]
        curr_idx=int(info[0])
        ranges=[units.convert_power_units(*units.split_units(r),result_unit="W") for r in info[3:]]
        if curr_idx<0:
            curr_range=info[3+curr_idx]
        else:
            curr_range=ranges[curr_idx]
        return self.RangeInfo(curr_idx,ranges,curr_range)
    def get_range(self):
        """Get current power range (maximal power in W)"""
        return self.get_range_info().curr_range
    def get_range_idx(self):
        """
        Get current power range index

        Index goes from 0 (highest) to maximal (lowest); auto-ranging is -1.
        """
        
        return self.get_range_info().curr_idx
    def set_range_idx(self, rng_idx):
        """
        Set current range index.

        `rng_idx` is the range index from 0 (highest) to maximal (lowest); auto-ranging is -1.
        """
        self.query("$WN{:d}".format(rng_idx))
        return self.get_range_idx()

    def is_filter_in(self):
        """Check if the filter is set to be on at the power meter"""
        return int(self.query("$FQ").split()[0].strip())==2
    def set_filter(self, filter_in=True):
        """Change the filter setting at the power meter (on or off)"""
        self.query("$FQ{:d}".format(2 if filter_in else 1))
        return self.is_filter_in()