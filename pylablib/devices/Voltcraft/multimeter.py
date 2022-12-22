from .base import GenericVoltcraftError, GenericVoltcraftBackendError
from ...core.utils import py3
from ...core.devio import SCPI, interface

import re
import numpy as np




class VC7055(SCPI.SCPIDevice):
    """
    Voltcraft VC-7055BT bench-top multimeter.

    Args:
        addr: device connection (usually a COM-port name such as ``"COM1"``).
    """
    Error=GenericVoltcraftError
    ReraiseError=GenericVoltcraftBackendError
    def __init__(self, addr):
        backend_defaults={"serial":("COM1",115200,8,'N',1)}
        super().__init__(addr,backend_defaults=backend_defaults)
        with self._close_on_error():
            self.get_id()
        self._add_settings_variable("functions",lambda: self.get_function("all"), lambda v: self.set_function(v,channel="all"),multiarg=False)
        self._add_settings_variable("range",self.get_range,self.set_range)
        self._add_settings_variable("autorange",self.is_autorange_enabled,self.enable_autorange)
        self._add_settings_variable("measurement_rate",self.get_measurement_rate,self.set_measurement_rate)
        self._add_status_variable("readings",lambda: self.get_reading("all"))

    def _read_echo(self, delay=0.):
        self.sleep(delay)
        self.instr.read(1)
        self.sleep(1E-2)
        self.instr.read()
    _p_function=interface.EnumParameterClass("function",
        {"volt_dc":"VOLT:DC","volt_ac":"VOLT:AC","curr_dc":"CURR:DC","curr_ac":"CURR:AC","cap":"CAP","res":"RES","fres":"FRES",
            "freq":"FREQ","per":"PER","cont":"CONT","diode":"DIOD","temp":"TEMP","none":"NONE"})
    def _normalize_function(self, func):
        func=func.strip('"').upper().split()
        if len(func)==1:
            if func[0] in ["CURR","VOLT"]:
                func=func+["DC"]
        return ":".join(func)


    _p_reading_channel=interface.EnumParameterClass("reading_channel",{"primary":1,"secondary":2})
    _reading_channels=["primary","secondary"]
    @interface.use_parameters(_returns="function",channel="reading_channel")
    def _get_single_function(self, channel):
        return self._normalize_function(self.ask("FUNC{}?".format(channel)))
    def get_function(self, channel="primary"):
        """Get measurement function for the given measurement channel (``"primary"`` or ``"secondary"``, or ``"all"`` for both channels)"""
        if channel=="all":
            return tuple(self._get_single_function(k) for k in self._reading_channels)
        return self._get_single_function(channel)
    @interface.use_parameters(function="function",channel="reading_channel")
    def _set_single_function(self, function, channel):
        if self._wap._get_single_function(channel)!=function:
            if channel==1:
                self.write("CONF:{}".format(function),read_echo=True)
            else:
                self.write("FUNC2",'"{}"'.format(function),read_echo=True)
        return self._wip._get_single_function(channel=channel)
    def set_function(self, function, channel="primary", reset_secondary=True):
        """
        Set measurement function for the given measurement channel (``"primary"``, ``"secondary"``, or ``"all"`` for both channels).
        
        If ``reset_secondary==True`` and the primary function is changed, set the secondary function to ``"none"`` to avoid conflicts.
        """
        if channel=="all" or isinstance(function,(tuple,list)):
            self._set_single_function("none","secondary")
            return tuple(self._set_single_function(f,k) for f,k in zip(function,self._reading_channels))
        if reset_secondary and channel=="primary" and self.get_function()!=function:
            self._set_single_function("none","secondary")
        return self._set_single_function(function,channel)
    
    _range_indices={"VOLT:DC":[50E-3,500E-3,5,50,500,1E3],"VOLT:AC":[500E-3,5,50,500,750],
        "CURR:DC":[500E-6,5E-3,50E-3,500E-3,5,10],"CURR:AC":[500E-6,5E-3,50E-3,500E-3,5,10],
        "RES":[500,5E3,50E3,500E3,5E6,50E6],"FRES":[500,5E3,50E3],"CAP":[50E-9,500E-9,5E-6,50E-6,500E-6,5E-3,50E-3]}
    _si_pfx={"G":1E9,"M":1E6,"k":1E3,"K":1E3,"":1,"m":1E-3,"u":1E-6,"n":1E-9,"p":1E-12}
    def get_range(self):
        """Get the present measurement range"""
        f=self._wop._get_single_function("primary")
        if f not in self._range_indices:
            return None
        rng=self.ask("RANGE?","raw").strip()[:-1]
        if rng[-2:]==b"\xa6\xcc":  # micro-range glitch for capacitance
            v,p=rng[:-2],"u"
        else:
            m=re.match(r"(\d+)\s*(G|M|k|K||m|u|n|p)",py3.as_str(rng))
            if m is None:
                raise GenericVoltcraftError("unrecognized range value: {}".format(rng))
            v,p=m.groups()
        return float(v)*self._si_pfx[p]
    def set_range(self, rng):
        """Set the present measurement range"""
        f=self._wop._get_single_function("primary")
        if f not in self._range_indices:
            return None
        rngvals=np.array(self._range_indices[f])
        closest_idx=abs(np.log(rngvals)-np.log(rng)).argmin() if rng>0 else 0
        self.write("RANGE",closest_idx+1,"int",read_echo=True,read_echo_delay=0.1)
        return self.get_range()
    
    def is_autorange_enabled(self):
        """Check if autoscaling is enabled"""
        return self.ask("AUTO?","bool")
    def enable_autorange(self, enable=True):
        """Enable or disable autoscaling"""
        if enable:
            self.write("AUTO",read_echo=True,read_echo_delay=0.1)
        else:
            self.set_range(self.get_range())
        return self.is_autorange_enabled()
    
    _p_measurement_rate=interface.EnumParameterClass("measurement_rate",{"fast":"F","med":"M","slow":"S"})
    @interface.use_parameters(_returns="measurement_rate")
    def get_measurement_rate(self):
        """Get measurement update rate (``"fast""``, ``"med"``, or ``"slow"``)"""
        return self.ask("RATE?")
    @interface.use_parameters(rate="measurement_rate")
    def set_measurement_rate(self, rate):
        """Set measurement update rate (``"fast""``, ``"med"``, or ``"slow"``)"""
        if self._wop.get_measurement_rate()!=rate:
            self.write("RATE",rate,read_echo=True,read_echo_delay=0.2)
        return self.get_measurement_rate()
    
    @interface.use_parameters(channel="reading_channel")
    def _get_single_reading(self, channel):
        if channel==2 and self.get_function("secondary")=="none":
            return None
        return self.ask("MEAS{}?".format(channel),"float")
    def get_reading(self, channel="primary"):
        """Return the latest reading of the given measurement channel (``"primary"``, ``"secondary"``, or ``"all"`` for both channels)"""
        if channel=="all":
            return tuple(self._get_single_reading(k) for k in self._reading_channels)
        return self._get_single_reading(channel)
