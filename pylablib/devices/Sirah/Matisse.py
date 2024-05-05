from ...core.devio import SCPI, interface, comm_backend
from ...core.utils import py3, general
from .base import GenericSirahError, GenericSirahBackendError

import time
import collections
import warnings
import struct


TThinetCtlParameters=collections.namedtuple("TThinetCtlParameters",["setpoint","P","I","avg"])
TPiezoetDriveParameters=collections.namedtuple("TPiezoetDriveParameters",["amplitude","rate","oversamp"])
TPiezoetFeedbackParameters=collections.namedtuple("TPiezoetFeedbackParameters",["P","avg","phase"])
TPiezoetFeedforwardParameters=collections.namedtuple("TPiezoetFeedforwardParameters",["ampl","phase"])
TSlowpiezoCtlParameters=collections.namedtuple("TSlowpiezoCtlParameters",["setpoint","P","I","freeP"])
TFastpiezoCtlParameters=collections.namedtuple("TFastpiezoCtlParameters",["setpoint","I","lockpoint"])
TRefcellWaveformParameters=collections.namedtuple("TRefcellWaveformParameters",["lower_limit","upper_limit","oversamp","mode"])
TScanMode=collections.namedtuple("TScanMode",["falling","stop_lower","stop_upper"])
TScanParameters=collections.namedtuple("TScanParameters",["device","mode","lower_limit","upper_limit","rise_speed","fall_speed"])
class SirahMatisse(SCPI.SCPIDevice):
    """
    Sirah Matisse laser control.

    Args:
        addr: device address (usually a VISA name).
        use_mc_server: determines whether Matisse Commander server is used for the communication (it has somewhat different command format);
            if ``"auto"``, assumed to be ``True`` for network connections and ``False`` otherwise
    """
    Error=GenericSirahError
    ReraiseError=GenericSirahBackendError
    _bool_selector=("FALSE","TRUE")
    def __init__(self, addr, use_mc_server="auto"):
        if use_mc_server=="auto":
            use_mc_server=comm_backend.autodetect_backend(addr)=="network"
        self._use_mc_server=use_mc_server
        if self._use_mc_server:
            super().__init__(addr,term_read=b"",term_write=b"",backend_params={"datatype":"bytes"})
        else:
            super().__init__(addr)
        with self._close_on_error():
            self.get_id()
        self._add_scpi_parameter("diode_power","DPOW:DC")
        self._add_scpi_parameter("diode_power_waveform","DPOW:WAVTAB",kind="string")
        self._add_scpi_parameter("diode_power_lowlevel","DPOW:LOW",set_echo=True)
        self._add_scpi_parameter("thinet_power","TE:DC")
        self._add_scpi_parameter("refcell_waveform","REFCELL:TABLE",kind="string")
        self._add_scpi_parameter("bifi_position","MOTBI:POS",kind="int",set_echo=True)
        self._add_scpi_parameter("bifi_status","MOTBI:STA",kind="int")
        self._add_scpi_parameter("bifi_position_max","MOTBI:MAX",kind="int")
        self._add_scpi_parameter("thinet_position","MOTTE:POS",kind="int",set_echo=True)
        self._add_scpi_parameter("thinet_status","MOTTE:STA",kind="int")
        self._add_scpi_parameter("thinet_position_max","MOTTE:MAX",kind="int")
        self._add_scpi_parameter("thinet_ctl_status","TE:CNTRSTA",kind="param",parameter="lock_ctl_status",set_echo=True)
        self._add_scpi_parameter("thinet_ctl_errsig","TE:CNTRERR",kind="float")
        self._add_scpi_parameter("thinet_ctl_setpoint","TE:CNTRSP",kind="float",set_echo=True)
        self._add_scpi_parameter("thinet_ctl_P","TE:CNTRPROP",kind="float",set_echo=True)
        self._add_scpi_parameter("thinet_ctl_I","TE:CNTRINT",kind="float",set_echo=True)
        self._add_scpi_parameter("thinet_ctl_avg","TE:CNTRAVG",kind="int",set_echo=True)
        self._add_scpi_parameter("piezoet_ctl_status","PZETL:CNTRSTA",kind="param",parameter="lock_ctl_status",set_echo=True)
        self._add_scpi_parameter("piezoet_baseline","PZETL:BASE",kind="float",set_echo=True)
        self._add_scpi_parameter("piezoet_drv_amp","PZETL:AMP",kind="float",set_echo=True)
        self._add_scpi_parameter("piezoet_drv_rate","PZETL:SRATE",kind="param",parameter="piezoet_drv_rate",set_echo=True)
        self._add_scpi_parameter("piezoet_drv_oversamp","PZETL:OVER",kind="int",set_echo=True)
        self._add_scpi_parameter("piezoet_fb_P","PZETL:CNTRPROP",kind="float",set_echo=True)
        self._add_scpi_parameter("piezoet_fb_avg","PZETL:CNTRAVG",kind="int",set_echo=True)
        self._add_scpi_parameter("piezoet_fb_phase","PZETL:CNTRPHSF",kind="int",set_echo=True)
        self._add_scpi_parameter("piezoet_ff_amp","FEF:AMP",kind="float",set_echo=True)
        self._add_scpi_parameter("piezoet_ff_phase","FEF:PHSF",kind="int",set_echo=True)
        self._add_scpi_parameter("slowpiezo_value","SPZT:NOW",kind="float",set_echo=True)
        self._add_scpi_parameter("slowpiezo_ctl_status","SPZT:CNTRSTA",kind="param",parameter="lock_ctl_status",set_echo=True)
        self._add_scpi_parameter("slowpiezo_ctl_setpoint","SPZT:CNTRSP",kind="float",set_echo=True)
        self._add_scpi_parameter("slowpiezo_ctl_P","SPZT:LPROP",kind="float",set_echo=True)
        self._add_scpi_parameter("slowpiezo_ctl_I","SPZT:LINT",kind="float",set_echo=True)
        try:
            self.ask("SPZT:FRSP?")
            self._add_scpi_parameter("slowpiezo_ctl_freeP","SPZT:FRSP",kind="float",set_echo=True)
        except GenericSirahError:
            self._add_scpi_parameter("slowpiezo_ctl_freeP","SPZT:FPROP",kind="float",set_echo=True)
        self._add_scpi_parameter("fastpiezo_value","FPZT:NOW",kind="float",set_echo=True)
        self._add_scpi_parameter("fastpiezo_ctl_status","FPZT:CNTRSTA",kind="param",parameter="lock_ctl_status",set_echo=True)
        self._add_scpi_parameter("fastpiezo_ctl_setpoint","FPZT:CNTRSP",kind="float",set_echo=True)
        self._add_scpi_parameter("fastpiezo_ctl_lockpoint","FPZT:LKP",kind="float",set_echo=True)
        self._add_scpi_parameter("fastpiezo_ctl_I","FPZT:CNTRINT",kind="float",set_echo=True)
        self._add_scpi_parameter("fastpiezo_ctl_locked","FPZT:LOCK",kind="bool")
        self._add_scpi_parameter("refcell_value","REFCELL:NOW",kind="float",set_echo=True)
        self._add_scpi_parameter("refcell_wave_lowlim","REFCELL:LLM",kind="float",set_echo=True)
        self._add_scpi_parameter("refcell_wave_upplim","REFCELL:ULM",kind="float",set_echo=True)
        self._add_scpi_parameter("refcell_wave_oversamp","REFCELL:OVER",kind="int",set_echo=True)
        self._add_scpi_parameter("refcell_wave_mode","REFCELL:MODE",kind="param",parameter="refcell_wave_mode",set_echo=True)
        self._add_scpi_parameter("scan_status","SCAN:STA",kind="param",parameter="lock_ctl_status",set_echo=True)
        self._add_scpi_parameter("scan_value","SCAN:NOW",kind="float",set_echo=True)
        self._add_scpi_parameter("scan_device","SCAN:DEV",kind="param",parameter="scan_device",set_echo=True)
        self._add_scpi_parameter("scan_mode","SCAN:MODE",kind="int",set_echo=True)
        self._add_scpi_parameter("scan_lowlim","SCAN:LLM",kind="float",set_echo=True)
        self._add_scpi_parameter("scan_upplim","SCAN:ULM",kind="float",set_echo=True)
        self._add_scpi_parameter("scan_risespd","SCAN:RSPD",kind="float",set_echo=True)
        self._add_scpi_parameter("scan_fallspd","SCAN:FSPD",kind="float",set_echo=True)

        self._add_status_variable("diode_power",self.get_diode_power)
        self._add_status_variable("diode_power_lowlevel",self.get_diode_power_lowlevel)
        self._add_status_variable("thinet_power",self.get_thinet_power)
        self._add_status_variable("bifi_position",self.bifi_get_position)
        self._add_status_variable("bifi_range",self.bifi_get_range)
        self._add_status_variable("bifi_status",self.bifi_get_status)
        self._add_status_variable("thinet_position",self.thinet_get_position)
        self._add_status_variable("thinet_range",self.thinet_get_range)
        self._add_status_variable("thinet_status",self.thinet_get_status)
        self._add_settings_variable("thinet_ctl_status",self.get_thinet_ctl_status,self.set_thinet_ctl_status)
        self._add_settings_variable("thinet_ctl_params",self.get_thinet_ctl_params,self.set_thinet_ctl_params)
        self._add_status_variable("piezoet_position",self.get_piezoet_position)
        self._add_settings_variable("piezoet_ctl_status",self.get_piezoet_ctl_status,self.set_piezoet_ctl_status)
        self._add_settings_variable("piezoet_drive_params",self.get_piezoet_drive_params,self.set_piezoet_drive_params)
        self._add_settings_variable("piezoet_feedback_params",self.get_piezoet_feedback_params,self.set_piezoet_feedback_params)
        self._add_settings_variable("piezoet_feedforward_params",self.get_piezoet_feedforward_params,self.set_piezoet_feedforward_params)
        self._add_status_variable("slowpiezo_position",self.get_slowpiezo_position)
        self._add_settings_variable("slowpiezo_ctl_status",self.get_slowpiezo_ctl_status,self.set_slowpiezo_ctl_status)
        self._add_settings_variable("slowpiezo_ctl_params",self.get_slowpiezo_ctl_params,self.set_slowpiezo_ctl_params)
        self._add_status_variable("fastpiezo_position",self.get_fastpiezo_position)
        self._add_status_variable("fastpiezo_locked",self.is_fastpiezo_locked)
        self._add_settings_variable("fastpiezo_ctl_status",self.get_fastpiezo_ctl_status,self.set_fastpiezo_ctl_status,ignore_error=GenericSirahError)
        self._add_settings_variable("fastpiezo_ctl_params",self.get_fastpiezo_ctl_params,self.set_fastpiezo_ctl_params,ignore_error=GenericSirahError)
        self._add_status_variable("refcell_position",self.get_refcell_position,ignore_error=GenericSirahError)
        self._add_settings_variable("refcell_waveform_params",self.get_refcell_waveform_params,self.set_refcell_waveform_params,ignore_error=(GenericSirahError,ValueError))
        self._add_settings_variable("scan_status",self.get_scan_status,self.set_scan_status)
        self._add_settings_variable("scan_position",self.get_scan_position,self.set_scan_position)
        self._add_settings_variable("scan_params",self.get_scan_params,self.set_scan_params)

    _id_comm="IDN?"
    _float_fmt="{:.8f}"
    def _instr_read(self, raw=False, size=None):
        if self._use_mc_server:
            l,=struct.unpack(">I",self.instr.read(4))
            res=self.instr.read(l)
        else:
            res=super()._instr_read(raw=raw,size=size)
        if not raw:
            res=res.strip()
            if res.startswith(b":"):
                sres=res.split(maxsplit=1)
                res=sres[1] if len(sres)>1 else b""
            elif res.upper().startswith(b"!ERROR"):
                raise GenericSirahError("device replied with an error: {}".format(py3.as_str(res[6:]).strip()))
        return res
    def _instr_write(self, msg):
        if self._use_mc_server:
            self.instr.write(struct.pack(">I",len(msg)))
            return self.instr.write(py3.as_bytes(msg))
        else:
            return super()._instr_write(msg)
    def close(self):
        if self._use_mc_server and self.instr:
            self.write(b"Close_Network_Connection")
            time.sleep(0.5)
        super().close()
    
    _ask_err_ntries=3
    _ask_err_delay=1.
    _ask_err_verbose=False
    def ask(self, *args, **kwargs):
        for i in range(self._ask_err_ntries):
            try:
                return super().ask(*args,**kwargs)
            except GenericSirahError as err:
                if self._ask_err_verbose:
                    warnings.warn("Sirah Matisse error: {}".format(err))
                if not err.args:
                    raise
                msg=err.args[0]
                hdr="device replied with an error:"
                if not msg.startswith(hdr):
                    raise
                emsg=msg[len(hdr):].strip()
                if not emsg.startswith("12,"):
                    raise
                if i==self._ask_err_ntries-1:
                    raise
                time.sleep(self._ask_err_delay)
                self.reconnect()
                time.sleep(self._ask_err_delay)

    def _parse_status(self, status_n, code_length, bits, codes, errs):
        bits=[v for b,v in bits.items() if status_n&b]
        code_mask=(1<<code_length)-1
        if "error" in bits:
            code=errs.get(status_n&code_mask,"unknown")
        else:
            code=codes.get(status_n&code_mask,"unknown")
        return code,bits
    def _wait_for_status_bit(self, getstat, bit, enabled, timeout=30.):
        countdown=general.Countdown(timeout)
        while True:
            _,curr_bits=getstat()
            bit_enabled=bit in curr_bits
            if bool(enabled)==bit_enabled:
                return
            if countdown.passed():
                raise GenericSirahError("status waiting timed out")
            time.sleep(1E-3)


    def get_diode_power(self):
        """Get the current laser resonator power"""
        return self._get_scpi_parameter("diode_power")
    def get_diode_power_waveform(self):
        """Get the current laser resonator power waveform"""
        values=self._get_scpi_parameter("diode_power_waveform")
        return [float(v) for v in values.split()]
    def get_diode_power_lowlevel(self):
        """Get the low-level cutoff current laser resonator power"""
        return self._get_scpi_parameter("diode_power_lowlevel")
    def set_diode_power_lowlevel(self, cutoff):
        """Set the low-level cutoff current laser resonator power"""
        self._set_scpi_parameter("diode_power_lowlevel",cutoff)
        return self.get_diode_power_lowlevel()
    
    def get_thinet_power(self):
        """Get the current thin etalon reflex power"""
        return self._get_scpi_parameter("thinet_power")

    def get_refcell_waveform(self):
        """Get the reference cell signal waveform"""
        values=self._get_scpi_parameter("refcell_waveform")
        return [float(v) for v in values.split()]


    def bifi_get_position(self):
        """Get the current position of the birefringent filter motor"""
        return self._get_scpi_parameter("bifi_position")
    def bifi_get_range(self):
        """Get the maximum position of the birefringent filter motor"""
        return self._get_scpi_parameter("bifi_position_max")
    def bifi_get_status_n(self):
        """Get the numerical status of the birefringent filter motor"""
        return self._get_scpi_parameter("bifi_status")
    _bifi_bits={(1<<7):"error",(1<<8):"moving",(1<<9):"off",(1<<10):"invalid_position",(1<<11):"limit_sw1",(1<<12):"limit_sw2",(1<<13):"home_sw",(1<<14):"manual"}
    _bifi_codes={0x00:"undefined",0x01:"init",0x02:"idle",0x03:"button_pressed",0x04:"moving_short_manual",0x05:"moving_long_manual",
        0x06:"deccel",0x07:"finishing",0x08:"moving_abs",0x09:"moving_rel",0x10:"calc_accel_table"}
    _bifi_errs={0x00:"none",0x01:"undef_command",0x02:"frequency_out_of_range",0x03:"ramp_length_invald",0x04:"limit_sw",0x05:"hold_current_off",0x06:"hold_current_off",
        0x07:"position_out_of_range",0x08:"ignored_because_running",0x20:"internal",0x21:"watchdog",0x22:"memory_write_error",0x23:"checksum"}
    def bifi_get_status(self):
        """
        Get the parsed status of the birefringent filter motor.
        
        Return tuple ``(code, bits)`` with, correspondingly, the general status/error code (e.g., ``"idle"``, ``"moving_abs"``, or ``"position_out_of_range"``),
        and a set of active status bits (e.g., ``"moving"``, ``"error"``, or ``"limit_sw1"``).
        """
        return self._parse_status(self.bifi_get_status_n(),7,self._bifi_bits,self._bifi_codes,self._bifi_errs)
    def bifi_clear_errors(self):
        """Clear the indicated errors of the birefringent filter motor"""
        self.ask("MOTBI:CL")

    def bifi_is_moving(self):
        """Check if the birefringent filter is moving"""
        return "moving" in self.bifi_get_status()[1]
    def bifi_wait_move(self, timeout=30.):
        """Wait until birefringent filter is done moving"""
        self._wait_for_status_bit(self.bifi_get_status,"moving",enabled=False,timeout=timeout)
    def bifi_move_to(self, position, wait=True, wait_timeout=30.):
        """Move the birefringent filter to the current position"""
        self._set_scpi_parameter("bifi_position",position)
        if wait:
            self.bifi_wait_move(timeout=wait_timeout)
    def bifi_stop(self):
        """Stop the birefringent filter motor"""
        self.ask("MOTBI:HALT")
        self.bifi_wait_move()
    def bifi_home(self, wait=True, wait_timeout=30.):
        """Home the birefringent filter motor"""
        self.ask("MOTBI:HOME")
        if wait:
            self.bifi_wait_move(timeout=wait_timeout)


    def thinet_get_position(self):
        """Get the current position of the thin etalon motor"""
        return self._get_scpi_parameter("thinet_position")
    def thinet_get_range(self):
        """Get the maximum position of the thin etalon motor"""
        return self._get_scpi_parameter("thinet_position_max")
    def thinet_get_status_n(self):
        """Get the numerical status of the thin etalon motor"""
        return self._get_scpi_parameter("thinet_status")
    _thinet_bits={(1<<7):"error",(1<<8):"moving",(1<<9):"off",(1<<10):"invalid_position",(1<<11):"limit_sw1",(1<<12):"limit_sw2",(1<<13):"home_sw",(1<<14):"manual"}
    _thinet_codes={0x00:"undefined",0x01:"init",0x02:"idle",0x03:"button_pressed",0x04:"moving_short_manual",0x05:"moving_long_manual",
        0x06:"deccel",0x07:"finishing",0x08:"moving_abs",0x09:"moving_rel",0x10:"calc_accel_table"}
    _thinet_errs={0x00:"none",0x01:"undef_command",0x02:"frequency_out_of_range",0x03:"ramp_length_invald",0x04:"limit_sw",0x05:"hold_current_off",0x06:"hold_current_off",
        0x07:"position_out_of_range",0x08:"ignored_because_running",0x20:"internal",0x21:"watchdog",0x22:"memory_write_error",0x23:"checksum"}
    def thinet_get_status(self):
        """
        Get the parsed status of the thin etalon motor.
        
        Return tuple ``(code, bits)`` with, correspondingly, the general status/error code (e.g., ``"idle"``, ``"moving_abs"``, or ``"position_out_of_range"``),
        and a set of active status bits (e.g., ``"moving"``, ``"error"``, or ``"limit_sw1"``).
        """
        return self._parse_status(self.thinet_get_status_n(),7,self._thinet_bits,self._thinet_codes,self._thinet_errs)
    def thinet_clear_errors(self):
        """Clear the indicated errors of the thin etalon motor"""
        self.ask("MOTTE:CL")

    def thinet_is_moving(self):
        """Check if the thin etalon is moving"""
        return "moving" in self.thinet_get_status()[1]
    def thinet_wait_move(self, timeout=30.):
        """Wait until thin etalon is done moving"""
        self._wait_for_status_bit(self.thinet_get_status,"moving",enabled=False,timeout=timeout)
    def thinet_move_to(self, position, wait=True, wait_timeout=30.):
        """Move the thin etalon to the current position"""
        self._set_scpi_parameter("thinet_position",position)
        if wait:
            self.thinet_wait_move(timeout=wait_timeout)
    def thinet_stop(self):
        """Stop the thin etalon motor"""
        self.ask("MOTTE:HALT")
        self.thinet_wait_move()
    def thinet_home(self, wait=True, wait_timeout=30.):
        """Home the thin etalon motor"""
        self.ask("MOTTE:HOME")
        if wait:
            self.thinet_wait_move(timeout=wait_timeout)
    
    _p_lock_ctl_status=interface.EnumParameterClass("lock_ctl_status",[("run","RUN"),("run","RU"),("run","TRUE"),("stop","STOP"),("stop","ST"),("stop","FALSE")])
    def get_thinet_ctl_status(self):
        """Get thin etalon lock status (``"run"`` or ``"stop"``)"""
        return self._get_scpi_parameter("thinet_ctl_status")
    def set_thinet_ctl_status(self, status="run"):
        """Set thin etalon lock status (``"run"`` or ``"stop"``)"""
        self._set_scpi_parameter("thinet_ctl_status",status)
        return self.get_thinet_ctl_status()
    def get_thinet_error_signal(self):
        """Get error signal of the thin etalon lock (emulated when not available on older firmware)"""
        try:
            return self._get_scpi_parameter("thinet_ctl_errsig")
        except GenericSirahError:
            return self._get_scpi_parameter("thinet_ctl_setpoint")-self.get_thinet_power()/self.get_diode_power()
    def get_thinet_ctl_params(self):
        """
        Get thin etalon lock control parameters.
        
        Return tuple ``(setpoint, P, I, avg)``.
        """
        return TThinetCtlParameters(*[self._get_scpi_parameter(n) for n in ["thinet_ctl_setpoint","thinet_ctl_P","thinet_ctl_I","thinet_ctl_avg"]])
    def set_thinet_ctl_params(self, setpoint=None, P=None, I=None, avg=None):
        """
        Set thin etalon lock control parameters.
        
        Any parameters which are ``None`` remain unchanged.
        """
        for n,v in zip(["thinet_ctl_setpoint","thinet_ctl_P","thinet_ctl_I","thinet_ctl_avg"],[setpoint,P,I,avg]):
            if v is not None:
                self._set_scpi_parameter(n,v)
        return self.get_thinet_ctl_params()
    
    def get_piezoet_ctl_status(self):
        """Get piezo etalon lock status (``"run"`` or ``"stop"``)"""
        return self._get_scpi_parameter("piezoet_ctl_status")
    def set_piezoet_ctl_status(self, status="run"):
        """Set piezo etalon lock status (``"run"`` or ``"stop"``)"""
        self._set_scpi_parameter("piezoet_ctl_status",status)
        return self.get_piezoet_ctl_status()
    def get_piezoet_position(self):
        """Get piezo etalon DC position"""
        return self._get_scpi_parameter("piezoet_baseline")
    def set_piezoet_position(self, value):
        """Set piezo etalon lock DC position"""
        self._set_scpi_parameter("piezoet_baseline",value)
        return self.get_piezoet_position()
    _p_piezoet_drv_rate=interface.EnumParameterClass("piezoet_drv_rate",{"8k":"0","32k":"1","48k":"2","96k":"3"})
    def get_piezoet_drive_params(self):
        """
        Get piezo etalon drive parameters.
        
        Return tuple ``(amplitude, rate, oversamp)``.
        """
        return TPiezoetDriveParameters(*[self._get_scpi_parameter(n) for n in ["piezoet_drv_amp","piezoet_drv_rate","piezoet_drv_oversamp"]])
    def set_piezoet_drive_params(self, amplitude=None, rate=None, oversamp=None):
        """
        Set piezo etalon drive parameters.
        
        `oversamp` should be between 8 and 32.
        `rate` can take values ``"8k"``, ``"32k"``, ``"48k"``, or ``"96k"``.
        Any parameters which are ``None`` remain unchanged.
        """
        for n,v in zip(["piezoet_drv_amp","piezoet_drv_rate","piezoet_drv_oversamp"],[amplitude,rate,oversamp]):
            if v is not None:
                self._set_scpi_parameter(n,v)
        return self.get_piezoet_drive_params()
    def get_piezoet_feedback_params(self):
        """
        Get piezo etalon feedback parameters.
        
        Return tuple ``(P, avg, phase)`` (phase is integer between 0 and oversampling).
        """
        return TPiezoetFeedbackParameters(*[self._get_scpi_parameter(n) for n in ["piezoet_fb_P","piezoet_fb_avg","piezoet_fb_phase"]])
    def set_piezoet_feedback_params(self, P=None, avg=None, phase=None):
        """
        Set piezo etalon feedback parameters.
        
        Phase is integer between 0 and oversampling.
        Any parameters which are ``None`` remain unchanged.
        """
        for n,v in zip(["piezoet_fb_P","piezoet_fb_avg","piezoet_fb_phase"],[P,avg,phase]):
            if v is not None:
                self._set_scpi_parameter(n,v)
        return self.get_piezoet_feedback_params()
    def get_piezoet_feedforward_params(self):
        """
        Get piezo etalon feedforward parameters.
        
        Return tuple ``(amp, phase)`` (phase is integer between 0 and oversampling).
        """
        return TPiezoetFeedforwardParameters(*[self._get_scpi_parameter(n) for n in ["piezoet_ff_amp","piezoet_ff_phase"]])
    def set_piezoet_feedforward_params(self, amp=None, phase=None):
        """
        Set piezo etalon feedforward parameters.
        
        Phase is integer between 0 and oversampling.
        Any parameters which are ``None`` remain unchanged.
        """
        for n,v in zip(["piezoet_ff_amp","piezoet_ff_phase"],[amp,phase]):
            if v is not None:
                self._set_scpi_parameter(n,v)
        return self.get_piezoet_feedforward_params()

    def get_slowpiezo_ctl_status(self):
        """Get slow piezo lock status (``"run"`` or ``"stop"``)"""
        return self._get_scpi_parameter("slowpiezo_ctl_status")
    def set_slowpiezo_ctl_status(self, status="run"):
        """Set slow piezo lock status (``"run"`` or ``"stop"``)"""
        self._set_scpi_parameter("slowpiezo_ctl_status",status)
        return self.get_slowpiezo_ctl_status()
    def get_slowpiezo_position(self):
        """Get slow piezo DC position"""
        return self._get_scpi_parameter("slowpiezo_value")
    def set_slowpiezo_position(self, value):
        """Set slow piezo DC position"""
        self._set_scpi_parameter("slowpiezo_value",value)
        return self.get_slowpiezo_position()
    def get_slowpiezo_ctl_params(self):
        """
        Get slow piezo lock control parameters.
        
        Return tuple ``(setpoint, P, I, freeP)``.
        """
        return TSlowpiezoCtlParameters(*[self._get_scpi_parameter(n) for n in ["slowpiezo_ctl_setpoint","slowpiezo_ctl_P","slowpiezo_ctl_I","slowpiezo_ctl_freeP"]])
    def set_slowpiezo_ctl_params(self, setpoint=None, P=None, I=None, freeP=None):
        """
        Set slow piezo lock control parameters.
        
        Any parameters which are ``None`` remain unchanged.
        """
        for n,v in zip(["slowpiezo_ctl_setpoint","slowpiezo_ctl_P","slowpiezo_ctl_I","slowpiezo_ctl_freeP"],[setpoint,P,I,freeP]):
            if v is not None:
                self._set_scpi_parameter(n,v)
        return self.get_slowpiezo_ctl_params()

    def get_fastpiezo_ctl_status(self):
        """Get fast piezo lock status (``"run"`` or ``"stop"``)"""
        return self._get_scpi_parameter("fastpiezo_ctl_status")
    def set_fastpiezo_ctl_status(self, status="run"):
        """Set fast piezo lock status (``"run"`` or ``"stop"``)"""
        self._set_scpi_parameter("fastpiezo_ctl_status",status)
        return self.get_fastpiezo_ctl_status()
    def is_fastpiezo_locked(self):
        """Check if the fast piezo is locked (output is between 5% and 95%)"""
        return self.get_fastpiezo_ctl_status()=="run" and self._get_scpi_parameter("fastpiezo_ctl_locked")
    def get_fastpiezo_position(self):
        """Get fast piezo DC position between 0 and 1"""
        return self._get_scpi_parameter("fastpiezo_value")
    def set_fastpiezo_position(self, value):
        """Set fast piezo DC position between 0 and 1"""
        self._set_scpi_parameter("fastpiezo_value",value)
        return self.get_fastpiezo_position()
    def get_fastpiezo_ctl_params(self):
        """
        Get fast piezo lock control parameters.
        
        Return tuple ``(setpoint, I, lockpoint)``.
        """
        return TFastpiezoCtlParameters(*[self._get_scpi_parameter(n) for n in ["fastpiezo_ctl_setpoint","fastpiezo_ctl_I","fastpiezo_ctl_lockpoint"]])
    def set_fastpiezo_ctl_params(self, setpoint=None, I=None, lockpoint=None):
        """
        Set fast piezo lock control parameters.
        
        Any parameters which are ``None`` remain unchanged.
        """
        for n,v in zip(["fastpiezo_ctl_setpoint","fastpiezo_ctl_I","fastpiezo_ctl_lockpoint"],[setpoint,I,lockpoint]):
            if v is not None:
                self._set_scpi_parameter(n,v)
        return self.get_fastpiezo_ctl_params()
    
    _p_refcell_wave_mode=interface.EnumParameterClass("refcell_wave_mode",{"none":"0","avg":"1","min":"2","max":"3"})
    def get_refcell_position(self):
        """Get reference cell DC position between 0 and 1"""
        return self._get_scpi_parameter("refcell_value")
    def set_refcell_position(self, value):
        """Set reference cell DC position between 0 and 1"""
        self._set_scpi_parameter("refcell_value",value)
        return self.get_refcell_position()
    def get_refcell_waveform_params(self):
        """
        Get reference cell waveform parameters.
        
        Return tuple ``(lower_limit, upper_limit, oversamp, mode)``.
        ``mode`` can be ``"none"``, ``"avg"``, ``"min"``, or ``"max"``.
        """
        return TRefcellWaveformParameters(*[self._get_scpi_parameter(n) for n in ["refcell_wave_lowlim","refcell_wave_upplim","refcell_wave_oversamp","refcell_wave_mode"]])
    def set_refcell_waveform_params(self, lower_limit=None, upper_limit=None, oversamp=None, mode=None):
        """
        Set reference cell waveform parameters.
        
        Any parameters which are ``None`` remain unchanged.
        `mode` can be ``"none"``, ``"avg"``, ``"min"``, or ``"max"``.
        `oversamp` should be between 4 and 512.
        """
        for n,v in zip(["refcell_wave_lowlim","refcell_wave_upplim","refcell_wave_oversamp","refcell_wave_mode"],[lower_limit,upper_limit,oversamp,mode]):
            if v is not None:
                self._set_scpi_parameter(n,v)
        return self.get_fastpiezo_ctl_params()
    
    def get_scan_status(self):
        """Get scan status (``"run"`` or ``"stop"``)"""
        return self._get_scpi_parameter("scan_status")
    def set_scan_status(self, status="run"):
        """Set scan status (``"run"`` or ``"stop"``)"""
        self._set_scpi_parameter("scan_status",status)
        return self.get_scan_status()
    def wait_scan(self, timeout=None):
        """Wait until scan is stopped"""
        countdown=general.Countdown(timeout)
        while self.get_scan_status()=="run":
            if countdown.passed():
                raise GenericSirahError("status waiting timed out")
            time.sleep(1E-3)
    def get_scan_position(self):
        """Get scan position"""
        return self._get_scpi_parameter("scan_value")
    def set_scan_position(self, value):
        """Set scan position"""
        self._set_scpi_parameter("scan_value",value)
        return self.get_scan_position()
    _p_scan_device=interface.EnumParameterClass("scan_device",{"none":"0","slow_piezo":"1","ref_cell":"2"})
    def get_scan_params(self):
        """
        Get scan parameters.
        
        Return tuple ``(device, mode, lower_limit, upper_limit, rise_speed, fall_speed)``.
        ``device`` can be ``"none"``, ``"slow_piezo"``, or ``"ref_cell"``.
        ``mode`` is a tuple ``(falling, stop_lower, stop_upper)``.
        """
        params=[self._get_scpi_parameter(n) for n in ["scan_device","scan_mode","scan_lowlim","scan_upplim","scan_risespd","scan_fallspd"]]
        params[1]=TScanMode(*[bool(params[1]&m) for m in [0x01,0x02,0x04]])
        return TScanParameters(*params)
    def set_scan_params(self, device=None, mode=None, lower_limit=None, upper_limit=None, rise_speed=None, fall_speed=None):
        """
        Set slow piezo lock control parameters.
        
        `device` can be ``"none"``, ``"slow_piezo"``, or ``"ref_cell"``.
        `mode` is a tuple ``(falling, stop_lower, stop_upper)``.
        Any parameters which are ``None`` remain unchanged.
        """
        if isinstance(mode,(tuple,list)):
            mode=sum([m for m,v in zip([0x01,0x02,0x04],mode) if v])
        for n,v in zip(["scan_device","scan_mode","scan_lowlim","scan_upplim","scan_risespd","scan_fallspd"],[device,mode,lower_limit,upper_limit,rise_speed,fall_speed]):
            if v is not None:
                self._set_scpi_parameter(n,v)
        return self.get_scan_params()
