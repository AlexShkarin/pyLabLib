from ...core.devio import SCPI, interface
from ...core.utils import py3
from .base import GenericKeithleyError, GenericKeithleyBackendError

import collections


TGenericFunctionParameters=collections.namedtuple("TGenericFunctionParameters",["rng","resolution","autorng"])
TFrequencyFunctionParameters=collections.namedtuple("TFrequencyFunctionParameters",["rng","aperture"])
TConfigurationParameters=collections.namedtuple("TConfigurationParameters",["function","rng","resolution"])
TAveragingParameters=collections.namedtuple("TAveragingParameters",["mode","count","enabled"])
class Keithley2110(SCPI.SCPIDevice):
    """
    Keithley 2110 bench-top multimeter.

    Args:
        addr: device address (usually a VISA name).
    """
    Error=GenericKeithleyError
    ReraiseError=GenericKeithleyBackendError
    def __init__(self, addr):
        super().__init__(addr)
        with self._close_on_error():
            self.get_id()
        self._add_settings_variable("configuration",self.get_configuration,self.set_configuration,ignore_error=(self.Error,))
        self._add_settings_variable("functions",lambda: self.get_function("all"), lambda v: self.set_function(v,channel="all"),multiarg=False)
        def add_funcpar_settings(f):
            self._add_settings_variable("parameters/"+f,lambda: self.get_function_parameters(function=f),lambda v: self.set_function_parameters(f,*v),multiarg=False,priority=-2)
        for f in self._supported_parameter_functions:
            add_funcpar_settings(f)
        self._add_settings_variable("averaging",self.get_averaging_parameters,self.setup_averaging)
        self._add_status_variable("readings",lambda: self.get_reading("all"))

    _p_function=interface.EnumParameterClass("function",
        {"volt_dc":"VOLT:DC","volt_ac":"VOLT:AC","curr_dc":"CURR:DC","curr_ac":"CURR:AC","cap":"CAP","volt_ratio":"VOLT:DC:RAT","res":"RES","fres":"FRES",
            "freq_volt":"FREQ:VOLT","freq_curr":"FREQ:CURR","per_volt":"PER:VOLT","per_curr":"PER:CURR","cont":"CONT","diode":"DIOD","temp":"TEMP","tcouple":"TCO","none":"NONE"})
    def _normalize_function(self, func):
        func=func.strip('"').upper().split(":")
        alias={"CURRENT":"CURR","VOLTAGE":"VOLT","CAPACITANCE":"CAP","RESISTANCE":"RES","FRESISTANCE":"FRES","RATIO":"RAT",
            "FREQUENCY":"FREQ","PERIOD":"PER","CONTINUITY":"CONT","DIODE":"DIOD","TCOUPLE":"TCO","TEMPERATURE":"TEMP"}
        func=[alias.get(p,p) for p in func]
        if len(func)==1:
            if func[0] in ["CURR","VOLT"]:
                func=func+["DC"]
            elif func[0] in ["FREQ","PER"]:
                func=func+["VOLT"]
        elif func==["VOLT","RAT"]:
            func=["VOLT","DC","RAT"]
        return ":".join(func)
    def _get_function_kind(self, function):
        if function in ["VOLT:DC","VOLT:AC","CURR:DC","CURR:AC","VOLT:DC:RAT"]:
            return "iv"
        if function in ["RES","FRES"]:
            return "res"
        if function=="CAP":
            return "cap"
        if function in ["FREQ:VOLT","FREQ:CURR","PER:VOLT","PER:CURR"]:
            return "freq"
        if function=="TEMP":
            return "temp"
        if function=="TCO":
            return "tcoup"
        return "misc"
    def _check_function_kind(self, function, include, msg):
        fkind=self._get_function_kind(function)
        if fkind not in include:
            function=self._as_parameter_class("function").i(function)
            raise ValueError("this method only supports {} functions; got {}".format(msg,function))
    def _value_to_text(self, value, extra=("MIN","MAX","DEF"),):
        if isinstance(value,py3.textstring):
            value=value.upper()
            if value not in extra:
                extra=", ".join("'{}'".format(v) for v in extra)
                raise ValueError("unsupported parameter: '{}'; allowed values are {}".format(value,extra))
        else:
            value="{:.8E}".format(value)
        return value


    _p_reading_channel=interface.EnumParameterClass("reading_channel",{"primary":1,"secondary":2})
    _reading_channels=["primary","secondary"]
    @interface.use_parameters(_returns="function",channel="reading_channel")
    def _get_single_function(self, channel):
        return self._normalize_function(self.ask(":SENS:FUNC{}?".format(channel)))
    def get_function(self, channel="primary"):
        """Get measurement function for the given measurement channel (``"primary"`` or ``"secondary"``, or ``"all"`` for both channels)"""
        if channel=="all":
            return tuple(self._get_single_function(k) for k in self._reading_channels)
        return self._get_single_function(channel)
    @interface.use_parameters(function="function",channel="reading_channel")
    def _set_single_function(self, function, channel):
        self.write(":SENS:FUNC{}".format(channel),'"{}"'.format(function))
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
    
    _supported_parameter_functions=["volt_dc","volt_ac","curr_dc","curr_ac","volt_ratio","res","fres","cap","freq_volt","freq_curr","per_volt","per_curr"]
    def _get_all_function_parameters(self, function, include):
        result={}
        if function=="VOLT:DC:RAT":
            function="VOLT:DC"
        if "rng" in include:
            result["rng"]=self.ask(":SENS:{}:RANG?".format(function),"float")
        if "resolution" in include:
            result["resolution"]=self.ask(":SENS:{}:RES?".format(function),"float")
        if "autorng" in include:
            result["autorng"]=self.ask(":SENS:{}:RANG:AUTO?".format(function),"bool")
        if "aperture" in include:
            result["aperture"]=self.ask(":SENS:{}:APER?".format(function.split(":")[0]),"float")
        return result
    @interface.use_parameters(function="function")
    def get_vcr_function_parameters(self, function=None):
        """
        Get parameters for the given voltage, current or resistance measurement function.
        
        Supported functions are ``"volt_dc"``, ``"volt_ac"``, ``"curr_dc"``, ``"curr_ac"``, ``"res"``, and ``"fres"``.
        Return tuple ``(rng, resolution, autorng)`` with, correspondingly, measurement range, resolution, and whether autorange is enabled.
        """
        function=self._wop._get_single_function() if function is None else function
        self._check_function_kind(function,["iv","res"],"current, voltage and resistance")
        return TGenericFunctionParameters(**self._get_all_function_parameters(function,["rng","resolution","autorng"]))
    @interface.use_parameters(function="function")
    def get_cap_function_parameters(self, function=None):
        """
        Get parameters for the given capacitance measurement function.
        
        The only supported function is ``"cap"``.
        Return tuple ``(rng, autorng)`` with, correspondingly, measurement range and whether autorange is enabled.
        """
        function=self._wop._get_single_function() if function is None else function
        self._check_function_kind(function,["cap"],"capacitance")
        return TGenericFunctionParameters(resolution=None,**self._get_all_function_parameters(function,["rng","autorng"]))
    @interface.use_parameters(function="function")
    def get_freq_function_parameters(self, function=None):
        """
        Set parameters for the given frequency or period measurement function.
        
        Supported functions are ``"freq_volt"``, ``"freq_curr"``, ``"per_volt"``, ``"per_curr"``.
        Return tuple ``(rng, aperture)`` with, correspondingly, measurement range, and the averaging aperture.
        """
        function=self._wop._get_single_function() if function is None else function
        self._check_function_kind(function,["freq"],"frequency and period")
        return TFrequencyFunctionParameters(**self._get_all_function_parameters(function,["rng","aperture"]))
    @interface.use_parameters(function="function")
    def get_function_parameters(self, function=None):
        """
        Get function parameters for any supported function.

        Result depends on the function kind. See :meth:`get_vcr_function_parameters`, :meth:`get_cap_function_parameters` and :meth:`get_freq_function_parameters` for details.
        """
        if function is None:
            function=self._wop._get_single_function()
        fkind=self._get_function_kind(function)
        if fkind in ["iv","res"]:
            return self._wip.get_vcr_function_parameters(function)
        if fkind=="cap":
            return self._wip.get_cap_function_parameters(function)
        if fkind=="freq":
            return self._wip.get_freq_function_parameters(function)
        function=self._as_parameter_class("function").i(function)
        raise ValueError("only current, voltage, resistance, capacitance, frequency and period functions are supported; got {}".format(function))

    def _set_all_function_parameters(self, function, rng=None, resolution=None, autorng=None, aperture=None):
        if function=="VOLT:DC:RAT":
            function="VOLT:DC"
        if rng is not None:
            self.write(":SENS:{}:RANG".format(function),self._value_to_text(rng))
        if resolution is not None:
            self.write(":SENS:{}:RES".format(function),self._value_to_text(resolution))
        if autorng is not None:
            self.write(":SENS:{}:RANG:AUTO".format(function),autorng,"bool")
        if aperture is not None:
            self.write(":SENS:{}:APER".format(function),self._value_to_text(aperture))
    @interface.use_parameters(function="function")
    def set_vcr_function_parameters(self, function=None, rng=None, resolution=None, autorng=None):
        """
        Set parameters for the given voltage, current or resistance measurement function.
        
        Supported functions are ``"volt_dc"``, ``"volt_ac"``, ``"curr_dc"``, ``"curr_ac"``, ``"res"``, and ``"fres"``.
        `rng`, `resolution` and `autorng` are correspondingly, measurement range, resolution, and whether autorange is enabled.
        `rng` and `resolution` can also have values ``"min"``, ``"max"`` or ``"def"`` for, correspondingly, minimal possible, maximal possible, and default value.
        """
        function=self._wop._get_single_function() if function is None else function
        self._check_function_kind(function,["iv","res"],"current, voltage and resistance")
        self._set_all_function_parameters(function,rng=rng,resolution=resolution,autorng=autorng)
        return self._wip.get_vcr_function_parameters(function=function)
    @interface.use_parameters(function="function")
    def set_cap_function_parameters(self, function=None, rng=None, autorng=None):
        """
        Set parameters for the given capacitance measurement function.
        
        The only supported function is ``"cap"``.
        `rng` and `autorng` are correspondingly, measurement range and whether autorange is enabled.
        `rng` can also have values ``"min"``, ``"max"`` or ``"def"`` for, correspondingly, minimal possible, maximal possible, and default value.
        """
        function=self._wop._get_single_function() if function is None else function
        self._check_function_kind(function,["cap"],"capacitance")
        self._set_all_function_parameters(function,rng=rng,autorng=autorng)
        return self._wip.get_cap_function_parameters(function=function)
    @interface.use_parameters(function="function")
    def set_freq_function_parameters(self, function=None, rng=None, aperture=None):
        """
        Set parameters for the given frequency or period measurement function.
        
        Supported functions are ``"freq_volt"``, ``"freq_curr"``, ``"per_volt"``, ``"per_curr"``.
        `rng` and `aperture` are correspondingly, measurement range and the averaging aperture.
        `rng` and `aperture` can also have values ``"min"``, ``"max"`` or ``"def"`` for, correspondingly, minimal possible, maximal possible, and default value.
        """
        function=self._wop._get_single_function() if function is None else function
        self._check_function_kind(function,["freq"],"frequency and period")
        self._set_all_function_parameters(function,rng=rng,aperture=aperture)
        return self._wip.get_cap_function_parameters(function=function)
    @interface.use_parameters(function="function")
    def set_function_parameters(self, function=None, **kwargs):
        """
        Set function parameters for any supported function.

        Arguments depend on the function kind. See :meth:`set_vcr_function_parameters`, :meth:`set_cap_function_parameters` and :meth:`set_freq_function_parameters` for details.
        """
        if function is None:
            function=self._wop._get_single_function()
        fkind=self._get_function_kind(function)
        if fkind in ["iv","res"]:
            return self._wip.set_vcr_function_parameters(function,**kwargs)
        if fkind=="cap":
            return self._wip.set_cap_function_parameters(function,**kwargs)
        if fkind=="freq":
            return self._wip.set_freq_function_parameters(function,**kwargs)
        function=self._as_parameter_class("function").i(function)
        raise ValueError("only current, voltage, resistance, capacitance, frequency and period functions are supported; got {}".format(function))

    @interface.use_parameters(_returns=["function",None,None])
    def get_configuration(self):
        """
        Get current measurement configuration on the primary channel.

        Return tuple ``(function, rng, resolution)`` with, correspondingly, measurement function, measurement range and resolution.
        """
        res=self.ask(":CONF?")
        res=res.strip('"').split()
        if len(res)==1:
            func,rng,prec=res[0],None,None
        else:
            func,par=res
            par=par.split(",")
            if len(par)==1:
                rng,prec=float(par),None
            else:
                rng,prec=float(par[0]),float(par[1])
        return TConfigurationParameters(self._normalize_function(func),rng,prec)
    @interface.use_parameters(function="function")
    def set_configuration(self, function=None, rng=None, resolution=None):
        """
        Set current measurement configuration on the primary channel.

        `function`, `rng` and `resolution` are, correspondingly, measurement function, measurement range and resolution.
        """
        cfg=self._wop.get_configuration()
        function=cfg.function if function is None else function
        if function!=cfg.function:
            rng=self._value_to_text("DEF" if rng is None else rng)
            resolution=self._value_to_text("DEF" if resolution is None else resolution)
        else:
            rng=self._value_to_text(cfg.rng if rng is None else rng)
            if rng!=cfg.rng:
                resolution=self._value_to_text("DEF" if resolution is None else resolution)
            else:
                resolution=self._value_to_text(cfg.resolution if resolution is None else resolution)
        if function in ["CONT","DIOD","TEMP","TCO"]:
            self.write(":CONF:{}".format(function))
        else:
            self.write(":CONF:{} {},{}".format(function,rng,resolution))
        return self.get_configuration()
    

    @interface.use_parameters(channel="reading_channel")
    def _get_single_reading(self, channel):
        if channel==2 and self.get_function("secondary")=="none":
            return None
        return self.ask("READ{}?".format(channel),"float")
    def get_reading(self, channel="primary"):
        """Initiate and return the reading of the given measurement channel (``"primary"``, ``"secondary"``, or ``"all"`` for both channels)"""
        if channel=="all":
            return tuple(self._get_single_reading(k) for k in self._reading_channels)
        return self._get_single_reading(channel)
    
    _p_averaging_mode=interface.EnumParameterClass("averaging_mode",{"moving":"MOV","repeat":"REP"})
    @interface.use_parameters(_returns=["averaging_mode",None,None])
    def get_averaging_parameters(self):
        """
        Get result averaging parameters.

        Return tuple ``(mode, count, enabled)`` with, correspondingly, averaging mode (``"moving"`` or ``"repeat"``), number of counts to average, and whether it is enabled.
        """
        mode=self.ask(":AVER:TCON?")
        count=self.ask(":AVER:COUN?","int")
        enabled=self.ask(":AVER:STAT?","bool")
        return TAveragingParameters(mode,count,enabled)
    @interface.use_parameters(mode="averaging_mode")
    def setup_averaging(self, mode=None, count=None, enabled=None):
        """
        Set result averaging parameters.

        `mode`, `count` and `enabled` are , correspondingly, averaging mode (``"moving"`` or ``"repeat"``), number of counts to average, and whether it is enabled.
        """
        if mode is not None:
            self.write(":AVER:TCON",mode)
        if count is not None:
            self.write(":AVER:COUN",count,"int")
        if enabled is not None:
            self.write(":AVER:STATE",enabled,"bool")
        return self.get_averaging_parameters()