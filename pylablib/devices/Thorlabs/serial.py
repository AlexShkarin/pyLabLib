from ...core.devio import SCPI, interface
from ...core.utils import py3
from .base import ThorlabsError, ThorlabsBackendError



class ThorlabsSerialInterface(SCPI.SCPIDevice):
    """
    Generic Thorlabs device interface using Serial communication.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    _allow_concatenate_write=False
    Error=ThorlabsError
    ReraiseError=ThorlabsBackendError
    _validate_echo=False  # if true; check if the echo matches the written command and raise an error (and re-run the command) if it does not
    _default_failsafe=True
    _default_retry_delay=0.5
    def __init__(self, conn):
        super().__init__(conn,backend="serial",term_read=["\r","\n"],term_write="\r",timeout=5.,backend_defaults={"serial":("COM1",115200)})

    def open(self):
        super().open()
        self.instr.flush_read()
    
    def _check_reply(self, reply, msg=None):
        return reply.find(b"CMD_")<0 and reply.find(b"Error")<0
    def _instr_write(self, msg):
        self.instr.flush_read()
        if self._validate_echo:
            self.instr.write(msg)
            res=self._instr_read()
            if res.strip()==py3.as_bytes(msg.strip()):
                return
            raise self.Error("request {} returned unexpected echo: {}".format(py3.as_bytes(msg.strip()),res))
        self.instr.write(msg,read_echo=True)
    def _instr_read(self, raw=False, size=None):
        if size:
            data=self.instr.read(size=size)
        elif raw:
            data=self.instr.readline(remove_term=False)
        else:
            data=""
            while not data:
                data=self.instr.readline(remove_term=True).strip()
                while data[:1]==b">":
                    data=data[1:].strip()
        return data


class FW(ThorlabsSerialInterface):
    """
    Thorlabs FW102/212 motorized filter wheels.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
        respect_bound(bool): if ``True``, avoid crossing the boundary between the first and the last position in the wheel
    """
    _validate_echo=True
    def __init__(self, conn, respect_bound=True):
        super().__init__(conn)
        self._add_settings_variable("pos",self.get_position,self.set_position)
        self._add_settings_variable("pcount",self.get_pcount,self.set_pcount)
        self._add_settings_variable("speed_mode",self.get_speed_mode,self.set_speed_mode)
        self._add_settings_variable("trigger_mode",self.get_trigger_mode,self.set_trigger_mode)
        self._add_settings_variable("sensors_mode",self.get_sensor_mode,self.set_sensor_mode)
        with self._close_on_error():
            self.pcount=self.get_pcount()
        self.respect_bound=respect_bound

    _id_comm="*idn?"
    def ask(self, msg, data_type="string", delay=0., timeout=None, read_echo=False):
        self.flush()
        return super().ask(msg,data_type=data_type,delay=delay,timeout=timeout,read_echo=read_echo)
    def get_position(self):
        """Get the wheel position (starting from 1)"""
        return self.ask("pos?","int")
    def set_position(self, pos):
        """Set the wheel position (starting from 1)"""
        if self.respect_bound: # check if the wheel could go through zero; if so, manually go around instead
            cur_pos=self.get_position()
            if abs(pos-cur_pos)>=self.pcount//2: # could switch by going through zero
                medp1=(2*cur_pos+pos)//3
                medp2=(cur_pos+2*pos)//3
                self.write("pos={}".format(medp1))
                self.write("pos={}".format(medp2))
                self.write("pos={}".format(pos))
            else:
                self.write("pos={}".format(pos))
        else:
            self.write("pos={}".format(pos))
        return self.get_position()

    def get_pcount(self):
        """Get the number of wheel positions (6 or 12)"""
        return self.ask("pcount?","int")
    def set_pcount(self, pcount):
        """Set the number of wheel positions (6 or 12)"""
        self.write("pcount={}".format(pcount))
        self.pcount=self.get_pcount()
        return self.pcount

    _p_speed_mode=interface.EnumParameterClass("speed_mode",{"low":0,"high":1})
    @interface.use_parameters(_returns="speed_mode")
    def get_speed_mode(self):
        """Get the motion speed mode (``"low"`` or ``"high"``)"""
        return self.ask("speed?","int")
    @interface.use_parameters
    def set_speed_mode(self, speed_mode):
        """Set the motion speed mode (``"low"`` or ``"high"``)"""
        self.write("speed={}".format(speed_mode))
        return self.get_speed_mode()

    _p_trigger_mode=interface.EnumParameterClass("trigger_mode",{"in":0,"out":1})
    @interface.use_parameters(_returns="trigger_mode")
    def get_trigger_mode(self):
        """Get the trigger mode (``"in"`` to input external trigger, ``"out"`` to output trigger)"""
        return self.ask("trig?","int")
    @interface.use_parameters
    def set_trigger_mode(self, trigger_mode):
        """Set the trigger mode (``"in"`` to input external trigger, ``"out"`` to output trigger)"""
        self.write("trig={}".format(trigger_mode))
        return self.get_trigger_mode()

    _p_sensor_mode=interface.EnumParameterClass("sensor_mode",{"off":0,"on":1})
    @interface.use_parameters(_returns="sensor_mode")
    def get_sensor_mode(self):
        """Get the sensor mode (``"off"`` to turn off when idle to eliminate stray light, ``"on"`` to remain on)"""
        return self.ask("sensors?","int")
    @interface.use_parameters
    def set_sensor_mode(self, sensor_mode):
        """Set the sensor mode (``"off"`` to turn off when idle to eliminate stray light, ``"on"`` to remain on)"""
        self.write("sensors={}".format(sensor_mode))
        return self.get_sensor_mode()

    def store_settings(self):
        """Store current settings as default"""
        self.write("save")


class FWv1(ThorlabsSerialInterface):
    """
    Thorlabs FW102/212 v1.0 (older version) motorized filter wheels.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
        pcount: number of positions in the wheel
        respect_bound(bool): if ``True``, avoid crossing the boundary between the first and the last position in the wheel
    """
    _validate_echo=True
    def __init__(self, conn, pcount=6, respect_bound=True):
        super().__init__(conn)
        self.pcount=pcount
        self._add_settings_variable("pos",self.get_position,self.set_position)
        self._add_info_variable("pcount",self.get_pcount)
        self._add_settings_variable("trigger_mode",self.get_trigger_mode,self.set_trigger_mode)
        self.respect_bound=respect_bound

    def _instr_write(self, msg):
        self.instr.flush_read()
        self.instr.write(">")
        try:
            self._instr_read()
        except self.Error:
            pass
        super()._instr_write(msg)

    _id_comm="*idn?"
    def ask(self, msg, data_type="string", delay=0., timeout=None, read_echo=False):
        self.flush()
        return super().ask(msg,data_type=data_type,delay=delay,timeout=timeout,read_echo=read_echo)
    def get_position(self):
        """Get the wheel position (starting from 1)"""
        return self.ask("pos?","int")
    def set_position(self, pos):
        """Set the wheel position (starting from 1)"""
        if self.respect_bound: # check if the wheel could go through zero; if so, manually go around instead
            cur_pos=self.get_position()
            if abs(pos-cur_pos)>=self.pcount//2: # could switch by going through zero
                medp1=(2*cur_pos+pos)//3
                medp2=(cur_pos+2*pos)//3
                self.write("pos={}".format(medp1))
                self.write("pos={}".format(medp2))
                self.write("pos={}".format(pos))
            else:
                self.write("pos={}".format(pos))
        else:
            self.write("pos={}".format(pos))
        return self.get_position()

    def get_pcount(self):
        """Get the number of wheel positions (6 or 12)"""
        return self.pcount

    _p_trigger_mode=interface.EnumParameterClass("trigger_mode",{"in":0,"out":1})
    @interface.use_parameters(_returns="trigger_mode")
    def get_trigger_mode(self):
        """Get the trigger mode (``"in"`` to input external trigger, ``"out"`` to output trigger)"""
        return self.ask("trig?","int")
    @interface.use_parameters
    def set_trigger_mode(self, trigger_mode):
        """Set the trigger mode (``"in"`` to input external trigger, ``"out"`` to output trigger)"""
        self.write("trig={}".format(trigger_mode))
        return self.get_trigger_mode()






class MDT69xA(ThorlabsSerialInterface):
    """
    Thorlabs MDT693A/4A high-voltage source.

    Uses MDT693A program interface, so should be compatible with both A and B versions
    (though it doesn't support all functions of MDT693B/4B)

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    def __init__(self, conn):
        super().__init__(conn)
        self._add_settings_variable("voltage",self.get_voltage,self.set_voltage,mux=("xyz",1))
        self._add_status_variable("voltage_range",self.get_voltage_range)
        with self._close_on_error():
            self.get_id(timeout=2.)

    _id_comm="I"
    _p_channel=interface.EnumParameterClass("channel",["x","y","z"])
    @interface.use_parameters
    def get_voltage(self, channel="x"):
        """Get the output voltage in Volts at a given channel"""
        resp=self.ask(channel.upper()+"R?")
        resp=resp.strip()[2:-1].strip()
        return float(resp)
    @interface.use_parameters
    def set_voltage(self, voltage, channel="x"):
        """Set the output voltage in Volts at a given channel"""
        self.write(channel.upper()+"V{:.3f}".format(voltage))
        return self._wip.get_voltage(channel=channel)

    def get_voltage_range(self):
        """Get the selected voltage range in Volts (75, 100 or 150)"""
        resp=self.ask("%")
        resp=resp.strip()[2:-1].strip()
        return float(resp)