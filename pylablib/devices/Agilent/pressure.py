from ...core.utils import py3
from ...core.devio import comm_backend, interface

import collections


from .base import AgilentError, AgilentBackendError


TXGS600DeviceInfo=collections.namedtuple("TXGS600DeviceInfo",["main_board_rev","boards_rev"])
class XGS600(comm_backend.ICommBackendWrapper):
    """
    Agilent XGS-600 pressure gauge controller.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
        addr: device address if RS485 communication is used (for RS232 must be kept 0)
    """
    Error=AgilentError
    def __init__(self, conn, addr=0):
        instr=comm_backend.new_backend(conn,"serial",term_read="\r",term_write="\r",defaults={"serial":("COM1",9600)},timeout=3.,reraise_error=AgilentBackendError)
        super().__init__(instr)
        self.addr=addr
        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("all_pressures",self.get_all_pressures,priority=5)
        self._add_status_variable("boards",self.list_boards)
        self._add_status_variable("units",self.get_units)
        with self._close_on_error():
            self.get_device_info()
    
    def query(self, comm, arg=""):
        """Send the command (with an optional arguments) to the device and return the result"""
        comms="#{:02d}{:02X}".format(self.addr,comm)+str(arg)
        result=py3.as_str(self.instr.ask(comms))
        if result[0]=="?":
            raise AgilentError("query {} with arguments '{}' returned an error: {}".format(comm,arg,result[1:].strip()))
        if result[0]==">":
            return result[1:].strip()
        raise AgilentError("can not parse reply: {}".format(result))
    
    def get_device_info(self):
        """Get device info as a tuple ``(main_board_rev, boards_rev)``"""
        revs=self.query(0x05).split(",")
        revs=["{}.{}".format(r[:2],r[2:]) for r in revs]
        return TXGS600DeviceInfo(revs[0],revs[1:])
    
    _board_code={0x10:"HFIG",0x3A:"IMG",0x40:"CNV",0x4C:"analog",0xFE:"none"}
    def list_boards(self):
        """
        Return a list of the board types installed.
        
        The type can be ``"HFIG"``, ``"IMG"``, ``"CNV"``, ``"analog"``, or ``"none"``.
        """
        boards=self.query(0x01)
        codes=[boards[i:i+2] for i in range(0,len(boards),2)]
        codes=[int(c,16) if c else -1 for c in codes]
        return [self._board_code.get(c,c) for c in codes]
    
    _p_unit=interface.EnumParameterClass("units",{"torr":0,"mbar":1,"pa":2})
    @interface.use_parameters(_returns="units")
    def get_units(self):
        """Get device units for indication/reading (``"mbar"``, ``"torr"``, or ``"pa"``)"""
        return int(self.query(0x13))
    @interface.use_parameters
    def set_units(self, units):
        """Set device units for indication/reading (``"mbar"``, ``"torr"``, or ``"pa"``)"""
        self.query(0x10+units)
        return self.get_units()
    _p_conv_factor={"mbar":1E2,"torr":133.322,"pa":1}
    def to_Pa(self, value, units=None):
        """
        Convert value in the given units to Pa.

        If `units` is ``None``, use the current display units.
        """
        units=units or self.get_units()
        return value*self._p_conv_factor[units]
    def from_Pa(self, value, units=None):
        """
        Convert value in the given units from Pa.

        If `units` is ``None``, use the current display units.
        """
        units=units or self.get_units()
        return value/self._p_conv_factor[units]
    
    def _p2f(self, p):
        try:
            return float(p)
        except ValueError:
            return p.lower()
    def get_all_pressures(self, display_units=False):
        """
        Get pressures of all available gauges as a list.
        
        Includes pressures from all the connected cards from left to right (front view).
        If the gauge is not connected, the value is ``"nocbl"``.
        """
        pressures=[self._p2f(p) for p in self.query(0x0F).split(",")]
        if not display_units:
            f=self._p_conv_factor[self.get_units()]
            return [f*p if isinstance(p,float) else p for p in pressures]