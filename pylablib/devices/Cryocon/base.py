from ...core.devio import SCPI, interface, comm_backend


class CryoconError(comm_backend.DeviceError):
    """Generic Cryocon devices error"""
class CryoconBackendError(CryoconError,comm_backend.DeviceBackendError):
    """Generic Lakeshore backend communication error"""

class Cryocon1x(SCPI.SCPIDevice):
    """
    Cryocon 1x series (12C, 14C, 18C) temperature controller.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    _default_write_sync=True
    Error=CryoconError
    ReraiseError=CryoconBackendError
    def __init__(self, conn, nchannels="auto"):
        SCPI.SCPIDevice.__init__(self,conn,backend="serial",term_write="\n",term_read="\r\n",backend_defaults={"serial":("COM1",9600,8,'N',1)})
        channels={n:n for n in range(8)}
        channels.update({"ABCDEFGH"[n]:n for n in range(8)})
        channels.update({"CH"+"ABCDEFGH"[n]:n for n in range(8)})
        self._add_parameter_class(interface.EnumParameterClass("channel",channels))
        with self._close_on_error():
            self.get_id(timeout=2)
            if nchannels=="auto":
                nchannels=max(n for n in range(8) if self._is_channel_connected(n))+1
            self._nchannels=nchannels
        channels=range(self._nchannels)
        self._add_status_variable("temperature",self.get_all_temperatures)
    
    @interface.use_parameters
    def _is_channel_connected(self, channel):
        return self.ask("INP {}:ALARM?".format(channel))!="NAK"
    def get_number_of_channels(self):
        """Return total number of channels in the device (2, 4, or 8)"""
        return self._nchannels
    
    _p_display_units=interface.EnumParameterClass("units",{"K":"K","C":"C","F":"F","S":"S"})
    @interface.use_parameters
    def get_display_units(self, channel):
        return self.ask("INP {}:UNIT?".format(channel))
    @interface.use_parameters
    def set_display_units(self, channel, units):
        self.write("INP {}:UNIT".format(channel),units)
        return self.get_display_units(channel)
    def _read_raw_temperature(self, channel):
        value=self.ask("INP? {}".format(channel))
        return None if all(c in ".-" for c in value) else float(value)
    @interface.use_parameters
    def get_temperature(self, channel, display_units=False):
        """
        Get a reading on a given channel.
        
        If ``display_units==True``, return reading in the display units; otherwise, return reading in Kelvin.
        If in this case the display units are ``"S"`` (sensor), set them to Kelvin to get the reading.
        If sensor is disconnected, return ``None``.
        """
        if display_units:
            return self._read_raw_temperature(channel)
        units=self.get_display_units(channel)
        if units=="S":
            self.set_display_units(channel,"K")
            units="K"
        value=self._read_raw_temperature(channel)
        if value is None:
            return None
        if units=="K":
            return value
        if units=="C":
            return value+273.15
        if units=="F":
            return (value-32)*(5/9)+273.15
    def get_all_temperatures(self, display_units=False):
        """
        Get readings on all channels.
        
        If ``display_units==True``, return reading in the display units; otherwise, return reading in Kelvin.
        If in this case the display units are ``"S"`` (sensor), set them to Kelvin to get the reading.
        If sensor is disconnected, return ``None``.
        """
        return [self.get_temperature(ch,display_units=display_units) for ch in range(self._nchannels)]