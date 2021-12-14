from ...core.devio import comm_backend, interface

import collections
import struct



class LeyboldError(comm_backend.DeviceError):
    """Generic Leybold device error"""
class LeyboldBackendError(LeyboldError,comm_backend.DeviceBackendError):
    """Generic Leybold backend communication error"""



TDeviceInfo=collections.namedtuple("TDeviceInfo",["sensor","page","swver"])
TUpdateValue=collections.namedtuple("TUpdateValue",["value","display_units","status","error","device_info"])
class GenericITR(comm_backend.ICommBackendWrapper):
    """
    Generic Leybold ITR pressure gauge.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    Error=LeyboldError
    def __init__(self, conn):
        instr=comm_backend.new_backend(conn,"serial",term_read="",term_write="",defaults={"serial":("COM1",9600)},reraise_error=LeyboldBackendError)
        comm_backend.ICommBackendWrapper.__init__(self,instr)
        with self._close_on_error():
            self.get_update()
        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("units",self.get_units)
        self._add_status_variable("pressure",self.get_pressure)
        self._add_status_variable("latest_update",self.get_update)
    
    _update_page=5
    def _is_update(self, update, l0=None):
        if len(update)<2 or (l0 is not None and len(update)!=l0):
            return False
        if update[0]!=len(update)-2:
            return False
        if update[1]!=self._update_page:
            return False
        if sum(list(update[1:-1]))&0xFF!=update[-1]:
            return False
        return True

    _status_emission={0:"emission_off",1:"emission_25uA",2:"emission_5mA",3:"degas"}
    def _parse_status(self, status):
        return status
    def _parse_error(self, err):
        return err
    _p_units=interface.EnumParameterClass("units",{"mbar":0,"torr":1,"pa":2})
    @interface.use_parameters(_returns="units")
    def _get_units(self, status):
        return (status>>4)&0x03
    def _parse_value(self, value, units):
        if units=="mbar":
            return 10**(value/4E3-12.5)*100
        elif units=="torr":
            return 10**(value/4E3-12.625)*133.322
        return 10**(value/4E3-10.5)
    def _parse_update(self, update):
        l,page,status,err,value,swver,sensor,checksum=struct.unpack(">BBBBHBBB",update)
        el=len(update)-2
        if l!=el:
            raise LeyboldError("declared length {} does not agree with the message length {}".format(l,el))
        echecksum=sum(list(update[1:-1]))&0xFF
        if checksum!=echecksum:
            raise LeyboldError("declared checksum {} does not agree with the calculated checksum {}".format(checksum,echecksum))
        device_info=TDeviceInfo(sensor,page,"{:.1f}".format(swver/20))
        units=self._get_units(status)
        status=self._parse_status(status)
        err=self._parse_error(err)
        value=self._parse_value(value,units)
        return TUpdateValue(value,units,status,err,device_info)
    def _read_last_update(self):
        update=self.instr.read()[-9:]
        while True:
            if self._is_update(update,9):
                break
            update=(update+self.instr.read(1))[-9:]
        return update

    def get_update(self, refresh=True):
        """
        Get device state update.

        Return tuple ``(value, display_units, status, error, device_info)``, where ``value`` is the pressure in Pa,
        ``display_units`` are display units (``"pa"``, ``"mbar"``, or ``"torr"``),
        ``status`` is the devices status (e.g., emission status), ``error`` is the device error (``"ok"`` if no errors),
        and ``device_info`` is a tuple ``(sensor, page, swver)`` with the sensor kind ID, data page, and software version.

        If ``refresh==True``, get the latest update value; otherwise, get the latest read value.
        """
        if refresh:
            update=self._read_last_update()
            update=self._parse_update(update)
            self._last_update=update
        return self._last_update
    def send_command(self, byte1, byte2, byte3):
        """
        Send command to the device.
        
        Arguments represent the three command bytes. Values of these bytes for different commands are described in the manual.
        """
        bs=[b&0xFF for b in [byte1,byte2,byte3]]
        checksum=sum(bs)&0xFF
        msg=struct.pack("BBBBB",3,bs[0],bs[1],bs[2],checksum)
        self.instr.write(msg)

    def get_device_info(self):
        """
        Get device info.
        
        Return tuple ``(sensor, page, swver)`` with the sensor kind ID, data page, and software version.
        """
        return self.get_update(refresh=False).device_info
    def get_units(self):
        """Get device readout units (``"mbar"``, ``"pa"``, or ``"torr"``)"""
        return self.get_update().display_units
    def get_pressure(self, display_units=False):
        """
        Get pressure.
        
        If ``display_units==False``, return result in Pa; otherwise, use display units obtained using :meth:`get_units`.
        """
        up=self.get_update()
        if display_units:
            factor={"pa":1,"mbar":100,"torr":133.322}[up.display_units]
            return up.value/factor
        return up.value



TITR90Status=collections.namedtuple("TITR90Status",["emission","atm_adj"])
class ITR90(GenericITR):
    """
    Leybold ITR90 pressure gauge.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    def _parse_status(self, status):
        return TITR90Status(self._status_emission[status&0x03],bool(status&0x04))
    _error_values={0:"ok",5:"pirani_misadjusted",8:"BA_error",9:"pirani_error"}
    def _parse_error(self, err):
        return self._error_values[err&0x0F]
    @interface.use_parameters
    def set_units(self, units, store=True):
        """
        Get device readout units (``"mbar"``, ``"pa"``, or ``"torr"``).
        
        If ``store==True``, store the value in the non-volatile power-independent memory.
        """
        self.send_command(16,62,units)
        if store:
            self.send_command(32,62,62)
        return self.get_units()
    def start_degas(self):
        """Start degas (turns off automatically after 3 minutes)"""
        self.send_command(16,93,148)
    def stop_degas(self):
        """Stop degas"""
        self.send_command(16,93,105)