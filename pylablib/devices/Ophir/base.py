from ...core.devio import comm_backend, interface
from ...core.utils import py3, units

import collections

class OphirError(comm_backend.DeviceError):
    """Generic Ophir device error"""
class OphirBackendError(OphirError,comm_backend.DeviceBackendError):
    """Generic Ophir backend communication error"""

class OphirDevice(comm_backend.ICommBackendWrapper):
    """
    Generic Ophir device.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    Error=OphirError
    def __init__(self, conn):
        instr=comm_backend.new_backend(conn,"serial",term_read="\r\n",term_write="\r\n",defaults={"serial":("COM1",9600)},reraise_error=OphirBackendError)
        comm_backend.ICommBackendWrapper.__init__(self,instr)
    
    def _parse_response(self, comm, resp):
        resp=resp.strip()
        if resp.startswith(b"?"):
            raise OphirError("Command {} returned error: {}".format(comm,resp[1:].strip()))
        if resp.startswith(b"*"):
            return py3.as_str(resp[1:].strip())
        raise OphirError("Command {} returned unrecognized response: {}".format(comm,resp))
    def query(self, comm):
        """Send a query to the device and parse the reply"""
        comm=comm.strip()
        with self.instr.single_op():
            self.instr.flush_read()
            self.instr.write(comm)
            resp=self.instr.readline()
        return self._parse_response(comm,resp)


THeadInfo=collections.namedtuple("THeadInfo",["type","serial","name","capabilities"])
TDeviceInfo=collections.namedtuple("TDeviceInfo",["id","serial","name","rom_version"])
TWavelengthInfo=collections.namedtuple("TWavelengthInfo",["mode","rng","curr_idx","presets","curr_wavelength"])
TRangeInfo=collections.namedtuple("TRangeInfo",["curr_idx","ranges","curr_range"])
class VegaPowerMeter(OphirDevice):
    """
    Ophir Vega power meter.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    def __init__(self, conn):
        OphirDevice.__init__(self,conn)
        self._add_info_variable("head_info",self.get_head_info)
        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("power",self.get_power,ignore_error=OphirError)
        self._add_status_variable("energy",self.get_energy,ignore_error=OphirError)
        self._add_status_variable("frequency",self.get_frequency,ignore_error=OphirError)
        self._add_status_variable("units",self.get_units)
        self._add_settings_variable("wavelength",self.get_wavelength,self.set_wavelength,ignore_error=OphirError)
        self._add_status_variable("wavelength_info",self.get_wavelength_info,ignore_error=OphirError)
        self._add_status_variable("range_info",self.get_range_info,ignore_error=OphirError)
        self._add_status_variable("battery_condition",self.get_battery_condition,priority=-5)
        self._add_status_variable("baudrate",self.get_baudrate,priority=-2)
        self._add_status_variable("supported_baudrates",self.get_supported_baudrates,priority=-5)
        self._add_settings_variable("range_idx",self.get_range_idx,self.set_range_idx)
        self._add_settings_variable("filter_in",self.is_filter_in,self.set_filter,ignore_error=OphirError)
        self._add_settings_variable("diffuser_in",self.is_diffuser_in,self.set_diffuser,ignore_error=OphirError)

    _head_cap_bits={0:"power",1:"energy",18:"temperature",31:"frequency"}
    _head_types={"TH":"thermopile","BC":"BC20","TP":"temperature_probe","SI":"photodiode","LX":"CIE","RP":"RP","PY":"pyroelectric","NJ":"nanojoule","XX":"no_head"}
    def get_head_info(self):
        """
        Get head information.

        Return tuple ``(type, serial, name, capabilities)``.
        """
        htype,hserial,hname,hcaps=self.query("$HI").split()
        htype=self._head_types.get(htype,htype)
        hcaps=int(hcaps,base=16)
        caps=tuple([v for b,v in self._head_cap_bits.items() if hcaps&(1<<b)])
        return THeadInfo(htype,int(hserial),hname,caps)
    def get_device_info(self):
        """
        Get device information.

        Return tuple ``(id, serial, name, rom_version)``.
        """
        did,dserial,dname=self.query("$II").split()
        rver=self.query("$VE")
        return TDeviceInfo(did,int(dserial),dname,rver)

    def reset(self):
        """Reset the device"""
        self.query("$RE")

    def get_power(self):
        """
        Get the current power readings.
        
        Return either measured power, or ``"over"``, if the power is overrange.
        """
        power=self.query("$SP")
        if power.lower()=="over":
            return "over"
        return float(power)
    def get_energy(self):
        """
        Get the current energy readings.
        
        Return either measured energy, or ``"over"``, if the energy is overrange.
        """
        energy=self.query("$SE")
        if energy.lower()=="over":
            return "over"
        return float(energy)
    def get_frequency(self):
        """
        Get the current frequency readings.
        
        Return either measured frequency, or ``"over"``, if the power is overrange.
        """
        freq=self.query("$SF")
        if freq.lower()=="over":
            return "over"
        return float(freq)
    def get_units(self):
        """Get device reading units"""
        return self.query("$SI")

    def get_wavelength_info(self):
        """
        Get wavelength setting info.

        Return tuple ``(mode, rng, curr_idx, presets, curr_wavelength)``, where
        `mode` is the measurement mode (``"continuous"`` or ``"discrete"``),
        `rng` is a 2-tuple with the full wavelength range (in m) for continuous mode or a set of all wavelengths for discrete mode,
        `curr_idx` is the current wavelength preset index,
        `presets` is the list of all preset wavelengths (in m) for continuous mode or a set of all wavelengths for discrete mode,
        and `curr_wavelength` is the current measurement wavelength (in m) for continuous mode or the current wavelength name for discrete mode.
        """
        info=[i.strip() for i in self.query("$AW").split() if i.strip()]
        mode=info[0].lower()
        if mode=="continuous":
            rng=(float(info[1])*1E-9,float(info[2])*1E-9)
            curr_idx=int(info[3])
            presets=[float(w)*1E-9 for w in info[4:] if w.upper()!="NONE"]
            return TWavelengthInfo(mode,rng,curr_idx-1,presets,presets[curr_idx-1])
        else:
            curr_idx=int(info[1])
            rng=info[2:]
            return TWavelengthInfo(mode,rng,curr_idx-1,rng,rng[curr_idx-1])
    def get_wavelength(self):
        """Get current wavelength"""
        return self.get_wavelength_info().curr_wavelength
    def set_wavelength(self, wavelength):
        """
        Set current wavelength.
        
        `wavelength` is either a wavelength (in m) for the continuous mode, or a wavelength preset (as a string) for a discrete mode.
        """
        if isinstance(wavelength,py3.anystring):
            self.query("$WW {}".format(wavelength.upper()))
        else:
            self.query("$WL{:d}".format(int(wavelength*1E9)))
        return self.get_wavelength()

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
        return TRangeInfo(curr_idx,ranges,curr_range)
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
        The corresponding ranges are given by :meth:`get_range_info`.
        """
        self.query("$WN{:d}".format(rng_idx))
        return self.get_range_idx()

    def get_battery_condition(self):
        """Check if the batter is OK"""
        return bool(int(self.query("$BC")))
    
    _p_baudrate=interface.EnumParameterClass("baudrate",{9600:1,19200:2,38400:3,300:4,1200:5,4800:6})
    @interface.use_parameters(_returns="baudrate")
    def get_baudrate(self):
        """Get current baud rate"""
        br=self.query("$BR0")
        return int(br.split()[0])
    def get_supported_baudrates(self):
        """Get a list of all supported baud rates"""
        br=self.query("$BR0")
        return [int(v) for v in br.split()[1:]]
    @interface.use_parameters
    def set_baudrate(self, baudrate):
        """
        Set current baud rate.
        
        If the baudrate is different from the current one, close the device connection.
        The device object will need to be re-created with the newly specified baud rate.
        """
        curr_baudrate=self._wap.get_baudrate()
        self.query("$BR{}".format(baudrate))
        if curr_baudrate!=baudrate:
            self.close()

    def is_filter_in(self):
        """Check if the filter is set to be on at the power meter"""
        return int(self.query("$FQ").split()[0])==2
    def set_filter(self, filter_in=True):
        """Change the filter setting at the power meter (on or off)"""
        self.query("$FQ{:d}".format(2 if filter_in else 1))
        return self.is_filter_in()
    def is_diffuser_in(self):
        """Check if the diffuser is set to be on at the power meter"""
        return int(self.query("$DQ").split()[0])==2
    def set_diffuser(self, diffuser_in=True):
        """Change the diffuser setting at the power meter (on or off)"""
        self.query("$dQ{:d}".format(2 if diffuser_in else 1))
        return self.is_diffuser_in()