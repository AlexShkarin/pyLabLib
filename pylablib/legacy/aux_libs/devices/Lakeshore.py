from ...core.devio import backend, SCPI #@UnresolvedImport
from ...core.utils import funcargparse  #@UnresolvedImport

_depends_local=["...core.devio.SCPI"]


class Lakeshore218(SCPI.SCPIDevice):
    """
    Lakeshore 218 temperature controller.

    All channels are enumerated from 0.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    def __init__(self, conn):
        conn=backend.SerialDeviceBackend.combine_conn(conn,("COM1",9600,7,'E',1))
        SCPI.SCPIDevice.__init__(self,conn,backend="serial",term_write="\r\n",term_read="\r\n")
        self._add_settings_node("enabled",self.is_enabled,self.set_enabled,mux=(range(8),0))
        self._add_settings_node("sensor_type",self.get_sensor_type,self.set_sensor_type,mux=("AB",1))
        self._add_status_node("temperature",self.get_all_temperatures)
        try:
            self.get_id(timeout=2.)
        except self.instr.Error as e:
            self.close()
            raise self.instr.BackendOpenError(e)
    
    def is_enabled(self, channel):
        """Check if a given channel is enabled"""
        return self.ask("INPUT? {}".format(channel+1),"bool")
    def set_enabled(self, channel, enabled=True):
        """Enable or disable a given channel"""
        self.write("INPUT {} {}".format(channel+1, 1 if enabled else 0))
        return self.is_enabled(channel)
        
    def get_sensor_type(self, group):
        """
        Get sensort type for a given group (``"A"`` or ``"B"``).

        For type descriptions, see Lakeshore 218 programming manual.
        """
        return self.ask("INTYPE? {}".format(group),"int")
    def set_sensor_type(self, group, type):
        """
        Set sensort type for a given group (``"A"`` or ``"B"``).

        For type descriptions, see Lakeshore 218 programming manual.
        """
        self.write("INTYPE {} {}".format(group, type))
        return self.get_sensor_type(group)
    
    def get_temperature(self, channel):
        """Get readings (in Kelvin) on a given channel"""
        return self.ask("KRDG? {}".format(channel+1),"float")
    def get_all_temperatures(self):
        """Get readings (in Kelvin) on all channels"""
        data=self.ask("KRDG? 0")
        return [float(x.strip()) for x in data.strip().split(",")]


class Lakeshore370(SCPI.SCPIDevice):
    """
    Lakeshore 370 temperature controller.

    All channels are enumerated from 0.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    def __init__(self, conn):
        SCPI.SCPIDevice.__init__(self,conn)
        try:
            self.get_id(timeout=2.)
        except self.instr.Error as e:
            self.close()
            raise self.instr.BackendOpenError(e)
    
    def get_resistance(self, channel):
        """Get resistance readings (in Ohm) on a given channel"""
        return self.ask("RDGR? {:2d}".format(channel),"float")
    def get_sensor_power(self, channel):
        """Get dissipated power (in W) on a given channel"""
        return self.ask("RDGPWR? {:2d}".format(channel),"float")
    
    def select_channel(self, channel):
        """Select measurement channel"""
        self.write("SCAN {:2d},0".format(channel))
    def get_channel(self):
        """Get current measurement channel"""
        return int(self.ask("SCAN?").split(",")[0].strip())
    def setup_channel(self, channel=None, mode="V", exc_range=1, res_range=22, autorange=True):
        """
        Setup a measurement channel (current channel by default).

        `mode` is the excitation mode (``"I"`` or ``"V"``), `exc_range` is the excitation range, `res_range` is the resistance range.
        For range descriptions, see Lakeshore 370 programming manual.
        """
        funcargparse.check_parameter_range(mode,"mode","IV")
        channel=0 if channel is None else channel
        mode=0 if mode=="V" else 1
        autorange=1 if autorange else 0
        self.write("RDGRNG {:2d},{},{:2d},{:2d},{},0".format(channel,mode,exc_range,res_range,autorange))
    
    def setup_heater_openloop(self, heater_range, heater_percent, heater_res=100.):
        """
        Setup a heater in the open loop mode.

        `heater_range` is the heating range, `heater_percent` is the excitation percentage within the range, `heater_res` is the heater resistance (in Ohm).
        For range descriptions, see Lakeshore 370 programming manual.
        """
        self.write("CMODE 3")
        self.write("CSET 1,0,1,25,1,{},{:f}".format(heater_range,heater_res))
        self.write("HTRRNG {}".format(heater_range))
        self.write("MOUT {:f}".format(heater_percent))
    def get_heater_settings_openloop(self):
        """
        Get heater settings in the open loop mode.

        Return tuple ``(heater_range, heater_percent, heater_res)``, where `heater_range` is the heating range,
        `heater_percent` is the excitation percentage within the range, `heater_res` is the heater resistance (in Ohm).
        For range descriptions, see Lakeshore 370 programming manual.
        """
        cset_reply=[s.strip() for s in self.ask("CSET?").split(",")]
        heater_percent=self.ask("MOUT?","float")
        heater_range=self.ask("HTRRNG?","int")
        #return int(cset_reply[5]),heater_percent,float(cset_reply[6])
        return heater_range,heater_percent,float(cset_reply[6])
    
    def set_analog_output(self, channel, value):
        """Set analog output value at a given channel"""
        if value==0:
            self.write("ANALOG {},0,0,1,1,500.,0,0.".format(channel))
        else:
            self.write("ANALOG {},0,2,1,1,500.,0,{:f}".format(channel,value))
        return self.get_analog_output(channel)
    def get_analog_output(self, channel):
        """Get analog output value at a given channel"""
        return self.ask("AOUT? {}".format(channel),"float")