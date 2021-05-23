from ...core.devio import SCPI  #@UnresolvedImport
from ...core.utils import general, py3

import re
import time

_depends_local=["...core.devio.SCPI"]

class SirahError(RuntimeError):
    """Generic Sirah error"""
class SirahTimeoutError(SirahError):
    """Sirah waiting timeout error"""

class SirahInterface(SCPI.SCPIDevice):
    """
    Generic Sirah device interface using Visa communication.

    Args:
        conn: VISA connection string (something like ``"USB0::0x17E7::<DEVICE_ID>::<DEVICE_SN>::INSTR"``)
    """
    _default_failsafe=False
    def __init__(self, conn):
        SCPI.SCPIDevice.__init__(self,conn,backend="visa",timeout=3.)
    
    def open(self):
        SCPI.SCPIDevice.open(self)
        self.get_error_codes()

    _reset_comm="RESET"
    def _instr_read(self, raw=False):
        data=SCPI.SCPIDevice._instr_read(self,raw=raw)
        if not raw:
            data=py3.as_str(data)
            m=re.match(r"^:[\w:]+:",data)
            if m:
                data=data[m.end():].strip()
        return data
    _float_fmt=".3f"

    def get_error_codes(self, clear=True):
        """
        Return errors raised by the Matisse controller.

        If ``clear==True``, clear the errors on the controller (otherwise, it doesn't execute new commands).
        """
        codes=[int(c) for c in self.ask("ERROR:CODE?").split() if c]
        if clear:
            self.write("ERROR:CLEAR",read_echo=True)
        return codes



class SirahMatisse(SirahInterface):
    """
    Sirah Matisse device interface using Visa communication.

    Args:
        conn: VISA connection string (something like ``"USB0::0x17E7::0x0102::<DEVICE_ID>::INSTR"``)
    """
    def brf_home(self):
        """Home BRF motor"""
        self.write("MOTBI:HOME",read_echo=True)
    def brf_halt(self):
        """Stop BRF motor (smoothly)"""
        self.write("MOTBI:HALT",read_echo=True)
    def get_brf_status_n(self):
        """
        Get BRF motor status as an integer
        
        For the meaning, see Matisse Programmer's Guide
        """
        return self.ask("MOTBI:STATUS?","int")
    def is_brf_moving(self):
        """Check if BRF motor is moving"""
        return bool(self.get_brf_status_n()&0x100)
    def wait_for_brf(self, timeout=30., wait_step=0.3):
        """Wait until BRF motor is stopped"""
        ctd=general.Countdown(timeout)
        while True:
            if not self.is_brf_moving():
                return
            if ctd.passed():
                raise SirahTimeoutError()
            time.sleep(wait_step)
    def get_brf_position(self):
        """Get BRF motor position"""
        return self.ask("MOTBI:POS?","int")
    def set_brf_position(self, position):
        """Move BRF motor to a new position"""
        self.write("MOTBI:POS",int(position),read_echo=True)
        return self.get_brf_position()

    def thinet_home(self):
        """Home thin etalon motor"""
        self.write("MOTTE:HOME",read_echo=True)
    def thinet_halt(self):
        """Stop thin etalon motor (smoothly)"""
        self.write("MOTTE:HALT",read_echo=True)
    def get_thinet_status_n(self):
        """
        Get thin etalon motor status as an integer
        
        For the meaning, see Matisse Programmer's Guide
        """
        return self.ask("MOTTE:STATUS?","int")
    def is_thinet_moving(self):
        """Check if thin etalon motor is moving"""
        return bool(self.get_thinet_status_n()&0x100)
    def wait_for_thinet(self, timeout=30., wait_step=0.3):
        """Wait until thin etalon motor is stopped"""
        ctd=general.Countdown(timeout)
        while True:
            if not self.is_thinet_moving():
                return
            if ctd.passed():
                raise SirahTimeoutError()
            time.sleep(wait_step)
    def get_thinet_position(self):
        """Get thin etalon motor position"""
        return self.ask("MOTTE:POS?","int")
    def set_thinet_position(self, position):
        """Move thin etalon motor to a new position"""
        self.write("MOTTE:POS",int(position),read_echo=True)
        return self.get_thinet_position()

    def get_piezoet_position(self):
        """Get piezo etalon position"""
        return self.ask("PZETL:BASE?","float")
    def set_piezoet_position(self, position):
        """Change piezo etalon position"""
        self.write("PZETL:BASE",float(position),read_echo=True)
        return self.get_piezoet_position()