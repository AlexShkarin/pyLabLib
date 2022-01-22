### Interface for a generic device class ###

from ..utils import functions, dictionary, general, py3, funcargparse
from .base import DeviceError
import functools
import contextlib
import collections

_device_var_kinds=["settings","status","info"]

class IDevice:
    """
    A base class for an instrument.

    Contains some useful functions for dealing with device settings.
    """
    def __init__(self):
        super().__init__()
        self._device_var_ignore_error={"get":(),"set":()}
        self._device_vars=dict([(ik,{}) for ik in _device_var_kinds])
        self._device_vars_order=dict([(ik,[]) for ik in _device_var_kinds])
        self._add_info_variable("cls",lambda: self.__class__.__name__)
        self._add_info_variable("conn",self._get_connection_parameters,ignore_error=NotImplementedError)
        self.dv=dictionary.ItemAccessor(getter=self.get_device_variable,setter=self.set_device_variable)
        self._setup_parameter_classes()
        self._wap=self.NoParameterCaller(self,"wap")
        self._wip=self.NoParameterCaller(self,"wip")
        self._wop=self.NoParameterCaller(self,"wop")

    def open(self):
        """Open the connection"""
    def close(self):
        """Close the connection"""
    def is_opened(self):
        """Check if the device is connected"""
        return True
    def __bool__(self):
        return self.is_opened()
    def __enter__(self):
        return self
    def __exit__(self, *args, **vargs):
        self.close()
        return False
    @contextlib.contextmanager
    def _close_on_error(self):
        """Context manager, which closes the device if the code inside raises an error"""
        try:
            yield
        except getattr(self,"Error",DeviceError):
            self.close()
            raise
    
    def _get_connection_parameters(self):
        raise NotImplementedError("IDevice._get_connection_parameters")
    
    def _setup_parameter_classes(self):
        """Collect all class-wide parameter classes into a local dictionary"""
        self._parameters={}
        for n in dir(type(self)):
            v=getattr(self,n)
            if isinstance(v,IParameterClass) and v.name:
                self._add_parameter_class(v)
    def _as_parameter_class(self, par):
        return self._parameters.get(par,par)
    def _add_parameter_class(self, par_class):
        """
        Add a parameter class.

        `par_class` should be an instance of :class:`IParameterClass`.
        If the class with this name is already defined, raise an error.
        """
        if par_class.name in self._parameters:
            raise ValueError("parameter {} is already defined".format(par_class.name))
        self._parameters[par_class.name]=par_class
    def _replace_parameter_class(self, pc):
        """
        Replace a parameter class.

        `par_class` should be an instance of :class:`IParameterClass`.
        If the class with this name does not exist, add an error.
        """
        if pc.name not in self._parameters:
            raise ValueError("parameter {} does not exist".format(pc.name))
        self._parameters[pc.name]=pc
    def _call_without_parameters(self, name, kind, args, kwargs):
        """
        Call a method with the given name without making parameter substitutions.
        
        `kind` can be ``"wip"`` (no input parameter substitutions), ``"wip"`` (no input parameter substitutions),
        or ``"wap"`` (no parameter substitutions at all).
        """
        funcargparse.check_parameter_range(kind,"kind",["wap","wip","wop"])
        method=getattr(self,name)
        wpmethod="_{}_method".format(kind)
        if hasattr(method,wpmethod):
            return getattr(method,wpmethod)(self,*args,**kwargs) # supply self, since the unwrapped methods are unbound
        else:
            return method(*args,**kwargs)
    class NoParameterCaller:
        """Class to simplify calling functions without a parameter"""
        def __init__(self, device, kind):
            self.device=device
            self.kind=kind
        def __getattr__(self, name):
            return lambda *args,**kwargs: self.device._call_without_parameters(name,self.kind,args,kwargs)
    @staticmethod
    def _multiplex_func(func, choices, arg_pos=0, multiarg=True):
        def func_mux(args=None):
            res=[]
            if args:
                for a,ch in zip(args,choices):
                    margs=list(a) if (multiarg and isinstance(a,tuple)) else [a]
                    margs.insert(arg_pos,ch)
                    res.append(func(tuple(margs)))
                return res
            else:
                return [func(ch) for ch in choices]
        return func_mux
    def _update_device_variable_order(self, path, kind=None):
        """Shift the order of the device variable to the current position"""
        if kind is None:
            for k,v in self._device_vars.items():
                if path in v:
                    kind=k
                    break
        if kind not in self._device_vars:
            raise ValueError("unrecognized device variable kind: {}".format(kind))
        if path not in self._device_vars[kind]:
            raise ValueError("variable {} does not exist".format(path))
        order=self._device_vars_order[kind]
        del order[order.index(path)]
        order.append(path)
    def _add_device_variable(self, path, kind, getter=None, setter=None, ignore_error=(), mux=None, multiarg=True, priority=0):
        """
        Adds a device variable.
         
        Args:
            path: variable name.
            kind(str): can be ``"settings"`` (device settings parameter), ``"status"`` (device status variable) or ``"info"`` (device info variable).
            getter: methods for getting this variable. Can be ``None``, meaning that this variable is ignored when executing :meth:`get_settings`/:meth:`get_full_status`/:meth:`get_full_info`.
            setter: methods for setting this variable. Can be ``None``, meaning that this variable is ignored when executing :meth:`apply_settings`.
            ignore_error(tuple): is a list of exception classes; if raised during getter/setter call, they are ignored.
            mux(tuple): 1- or 2-tuple with parameters for function multiplexing (calling several times and combining result in a list).
                The first element is an iterable of argument values to be iterated over,
                the second argument is the position where this argument is inserted in the setter (by default, 0); the getter always received mux parameter as a single argument
            multiarg(bool): if ``True`` and the setter argument is a tuple, interpret it as a tuple of arguments and expand it; otherwise, keep it as a single tuple argument.
            priority(int): variable priority between -10 and 10;
                when querying all variables using :meth:`get_settings`, :meth:`get_full_status`, or :meth:`get_full_info`,
                only values with a priority equal to higher then specified (0 by default) are returned.
        """
        if kind not in self._device_vars:
            raise ValueError("unrecognized device variable kind: {}".format(kind))
        if priority<-10 or priority>10:
            raise ValueError("priority should be between -10 and 10")
        if not isinstance(ignore_error,tuple):
            ignore_error=(ignore_error,)
        if multiarg and setter:
            osetter=setter
            setter=lambda v: functions.call_cut_args(osetter,*v) if isinstance(v,tuple) else osetter(v)
        if mux:
            getter=self._multiplex_func(getter,*mux[:2],multiarg=multiarg) if getter else None
            setter=self._multiplex_func(setter,*mux[:2],multiarg=multiarg) if setter else None
        self._device_vars[kind][path]=(getter,setter,ignore_error,priority)
        if path not in self._device_vars_order[kind]:
            self._device_vars_order[kind].append(path)
    def _add_info_variable(self, path, getter=None, ignore_error=(), mux=None, priority=0):
        return self._add_device_variable(path,"info",getter=getter,ignore_error=ignore_error,mux=mux,priority=priority)
    def _add_status_variable(self, path, getter=None, ignore_error=(), mux=None, priority=0):
        return self._add_device_variable(path,"status",getter=getter,ignore_error=ignore_error,mux=mux,priority=priority)
    def _add_settings_variable(self, path, getter=None, setter=None, ignore_error=(), mux=None, multiarg=True, priority=0):
        return self._add_device_variable(path,"settings",getter=getter,setter=setter,ignore_error=ignore_error,mux=mux,multiarg=multiarg,priority=priority)
    def _get_device_variables(self, kinds, include=0):
        """
        Get dict ``{name: value}`` containing all the device settings.
         
        `kinds` is the list of info variables kinds to be included in the info.
        `include` specifies either a list of variables (only these variables are returned),
        a priority threshold (only values with the priority equal or higher are returned), or ``"all"`` (all available variables).
        Since the lowest priority is -10, setting ``include=-10`` queries all available variables, which is equivalent to ``include="all"``.
        """
        for kind in kinds:
            if kind not in self._device_vars:
                raise ValueError("unrecognized device variable kind: {}".format(kind))
        info={}
        if include=="all":
            include=-10
        variables,priority=(None,include) if isinstance(include,int) else (include,None)
        for kind in kinds:
            for k in self._device_vars_order[kind]:
                if variables is None or k in variables:
                    g,_,err,pr=self._device_vars[kind][k]
                    if (g is not None) and (priority is None or pr>=priority):
                        all_err=err+self._device_var_ignore_error["get"]
                        try:
                            info[k]=g()
                        except all_err:
                            pass
        return info
    def _remove_device_variable(self, path, kind=None):
        """Remove a device variable"""
        if kind is None:
            for k,v in self._device_vars.items():
                if path in v:
                    kind=k
                    break
        if kind not in self._device_vars:
            raise ValueError("unrecognized device variable kind: {}".format(kind))
        if path not in self._device_vars[kind]:
            raise ValueError("variable {} does not exist".format(path))
        del self._device_vars[kind][path]
        order=self._device_vars_order[kind]
        del order[order.index(path)]
    def get_settings(self, include=0):
        """
        Get dict ``{name: value}`` containing all the device settings.
        
        `include` specifies either a list of variables (only these variables are returned),
        a priority threshold (only values with the priority equal or higher are returned), or ``"all"`` (all available variables).
        Since the lowest priority is -10, setting ``include=-10`` queries all available variables, which is equivalent to ``include="all"``.
        """
        return self._get_device_variables(["settings"],include=include)
    def get_full_status(self, include=0):
        """
        Get dict ``{name: value}`` containing the device status (including settings).
        
        `include` specifies either a list of variables (only these variables are returned),
        a priority threshold (only values with the priority equal or higher are returned), or ``"all"`` (all available variables).
        Since the lowest priority is -10, setting ``include=-10`` queries all available variables, which is equivalent to ``include="all"``.
        """
        return self._get_device_variables(["settings","status"],include=include)
    def get_full_info(self, include=0):
        """
        Get dict ``{name: value}`` containing full device information (including status and settings).
        
        `include` specifies either a list of variables (only these variables are returned),
        a priority threshold (only values with the priority equal or higher are returned), or ``"all"`` (all available variables).
        Since the lowest priority is -10, setting ``include=-10`` queries all available variables, which is equivalent to ``include="all"``.
        """
        return self._get_device_variables(["settings","status","info"],include=include)
    def apply_settings(self, settings):
        """
        Apply the settings.
         
        `settings` is the dict ``{name: value}`` of the device available settings.
        Non-applicable settings are ignored.
        """
        for k in self._device_vars_order["settings"]:
            _,s,err,_=self._device_vars["settings"][k]
            all_err=err+self._device_var_ignore_error["set"]
            if s and (k in settings):
                try:
                    s(settings[k])
                except all_err:
                    pass
    def get_device_variable(self, key):
        """Get the value of a settings, status, or full info parameter"""
        for kind in _device_var_kinds:
            if key in self._device_vars[kind]:
                g=self._device_vars[kind][key][0]
                if g:
                    return g()
                raise ValueError("no getter for value '{}'".format(key))
        raise KeyError("no property '{}'".format(key))
    def set_device_variable(self, key, value):
        """Set the value of a settings parameter"""
        if key in self._device_vars["settings"]:
            s=self._device_vars["settings"][key][1]
            if s:
                return s(value)
            raise ValueError("no setter for value '{}'".format(key))
        raise KeyError("no property '{}'".format(key))








class IParameterClass:
    """
    A generic parameter class.

    Deals with converting device interface representation and the 'internal' representation (e.g., names used in SCPI commands or integer indices).
    Also responsible for validating the user-passed and device-returned parameters.

    Needs to define to methods: ``__call__`` for converting user parameters ('alias') into the device parameters ('value')
    and :meth:`i` for the opposite conversion.
    In addition, it provides :meth:`using_device` context manager to temporarily change the ``device`` attribute,
    which can be used by some parameter classes for device-dependent conversions.

    Args:
        name: parameter class name; used to match method arguments with corresponding classes.
    """
    def __init__(self, name):
        self.name=name
        self.device=None

    @contextlib.contextmanager
    def using_device(self, device):
        """Context manager for temporarily changing the ``device`` attribute to the given device instance"""
        current_device,self.device=self.device,device
        try:
            yield
        finally:
            self.device=current_device
    def docstring(self):
        """Get a parameter docstring"""
        return "generic parameter '{}'".format(self.name)
    def __call__(self, alias, device=None):
        """
        Convert user parameter value into a corresponding device parameter value.
        
        If not ``None``, `device` specifies the corresponding device instance for device-dependent conversion.
        """
        return alias
    def i(self, value, device=None):  # pylint: disable=unused-argument
        """
        Convert device parameter value into a corresponding use parameter value
        
        If not ``None``, `device` specifies the corresponding device instance for device-dependent conversion.
        """
        return value


class ICheckingParameterClass(IParameterClass):
    """
    Parameter class which separately handles checking and conversion.

    Specifies six methods: :meth:`check_value`, :meth:`to_alias` and ``_value_error_str`` for handling value-to-alias conversion,
    and :meth:`check_alias`, :meth:`to_value` and ``_alias_error_str`` for handling alias-to-value conversion.
    """
    def check_alias(self, alias):  # pylint: disable=unused-argument
        """Check if the alias is valid"""
        return True
    def check_value(self, value):  # pylint: disable=unused-argument
        """Check if the device value is valid"""
        return True
    def to_value(self, alias):
        """Convert the alias into a device value"""
        return alias
    def to_alias(self, value):
        """Convert the device value into an alias"""
        return value

    def _alias_error_str(self, alias):
        """Generate error message string on the alias check failure"""
        return "invalid value {} for the {}".format(repr(alias),self.name)
    def _value_error_str(self, value):
        """Generate error message string on the device value check failure"""
        return self._alias_error_str(value)

    def __call__(self, alias, device=None):
        with self.using_device(device):
            if not self.check_alias(alias):
                raise ValueError(self._alias_error_str(alias))
            return self.to_value(alias)
    def i(self, value, device=None):
        with self.using_device(device):
            if not self.check_value(value):
                raise ValueError(self._value_error_str(value))
            return self.to_alias(value)


class RangeParameterClass(ICheckingParameterClass):
    """
    Parameter class for numerical values constrained to a certain range.

    Args:
        name: parameter class name
        minval: minimal allowed value (inclusive); ``None`` means no lower limit
        maxval: maximal allowed value (inclusive); ``None`` means no upper limit
        out_of_range: action if an out-of-range value is supplied; can be either ``"error"`` (raise an error), or ``"truncate"`` (truncate to the nearest limit).
    """
    def __init__(self, name, minval=None, maxval=None, out_of_range="error"):
        ICheckingParameterClass.__init__(self,name=name)
        funcargparse.check_parameter_range(out_of_range,"out_of_range",["error","truncate"])
        if minval is not None and maxval is not None:
            minval,maxval=sorted([minval,maxval])
        self._rng=(minval,maxval)
        self._out_of_range=out_of_range
    def check_value(self, value):
        if self._out_of_range=="truncate":
            return True
        minval,maxval=self._rng
        if minval is not None and value<minval:
            return False
        if maxval is not None and value>maxval:
            return False
        return True
    def check_alias(self, alias):
        return self.check_value(alias)
    def to_value(self, alias):
        minval,maxval=self._rng
        if minval is not None and alias<minval:
            return minval
        if maxval is not None and alias>maxval:
            return maxval
        return alias
    def _alias_error_str(self, alias):
        errs=ICheckingParameterClass._alias_error_str(self,alias)
        if self._rng==(None,None):
            return errs
        minval,maxval=self._rng
        if minval is None:
            return "{}; values should be not greater than {}".format(errs,maxval)
        if maxval is None:
            return "{}; values should be not smaller than {}".format(errs,minval)
        return "{}; values should be between {} and {} (inclusive)".format(errs,minval,maxval)
    def docstring(self):
        return "numeric parameter '{}' with the range {}".format(self.name,self._rng)



def _first_priority_dict(lst):
    res={}
    for k,v in lst:
        res.setdefault(k,v)
    return res
def _to_case(value, case):
    if case is None or not isinstance(value,py3.textstring):
        return value
    return value.lower() if case=="lower" else value.upper()
class IEnumParameterClass(ICheckingParameterClass):
    """
    Parameter class for a generic enum (i.e., predefined values) parameter.

    Defines two methods for handling conversion:
        - ``_get_value_map`` which returns a dictionary for converting device values into aliases,
        - ``_get_alias_map`` which returns a dictionary for converting aliases into device values.

    These methods need to be redefined in subclasses.

    Args:
        name: parameter class name
        allowed_alias: specifies a range of allowed aliases; can be ``"exact"`` (only exact map matches are allowed),
            ``"device_value"`` (exact map matches and raw device values are allowed), or ``"all"`` (all values are allowed);
            in the latter two cases the value not in the map are passed as is.
        allowed_value: specifies a range of allowed device values; can be ``"exact"`` (only exact map matches are allowed),
            or ``"all"`` (all values are allowed); in the latter case the value not in the map is passed as is.
        alias_case: default alias parameter case for string values; can be ``None`` (no case normalization),
            or ``"lower"`` or ``"upper"`` (any received or returned alias will be normalized into this case)
        value_case: default value parameter case for string values; can be ``None`` (no case normalization),
            or ``"lower"`` or ``"upper"`` (any received or returned device value will be normalized into this case)
        match_prefix: if ``True``, then the keys in the value map (returned by ``_get_value_map`` method) are interpreted as prefixes,
            so in the value-to-alias conversion the converted value matches the map value if it just starts with it;
            in the case of ambiguity (several map values are prefixes for the same converted value), the exact match takes priority;
            useful for some SCPI devices, where the shorter version of the value can sometimes be returned.
    """
    def __init__(self, name, allowed_alias="device_values", allowed_value="exact", alias_case=None, value_case=None, match_prefix=False):
        funcargparse.check_parameter_range(alias_case,"alias_case",["lower","upper",None])
        funcargparse.check_parameter_range(value_case,"value_case",["lower","upper",None])
        funcargparse.check_parameter_range(allowed_alias,"allowed_alias",["exact","device_values","all"])
        funcargparse.check_parameter_range(allowed_value,"allowed_value",["exact","all"])
        ICheckingParameterClass.__init__(self,name=name)
        self._allowed_alias=allowed_alias
        self._allowed_value=allowed_value
        self._match_prefix=match_prefix
        self._alias_case=alias_case
        self._value_case=value_case

    def _get_value_map(self):
        return {}
    def _get_alias_map(self):
        return {}
        
    def check_value(self, value):
        value=_to_case(value,self._value_case)
        if self._allowed_value=="all":
            return True
        if self._match_prefix and isinstance(value,py3.textstring):
            for v in self._get_value_map():
                if isinstance(v,py3.textstring) and value.startswith(v):
                    return True
            return False
        else:
            return value in self._get_value_map()
    def check_alias(self, alias):
        if self._allowed_alias=="all":
            return True
        if _to_case(alias,self._alias_case) in self._get_alias_map():
            return True
        if (self._allowed_alias=="device_values") and _to_case(alias,self._value_case) in self._get_value_map():
            return True
        return False
    def to_value(self, alias):
        alias=_to_case(alias,self._alias_case)
        value=self._get_alias_map().get(alias,alias)
        return _to_case(value,self._value_case)
    def to_alias(self, value):
        value=_to_case(value,self._value_case)
        vmap=self._get_value_map()
        if value in vmap:
            return vmap[value]
        if self._match_prefix and isinstance(value,py3.textstring):
            for v,a in vmap.items():
                if isinstance(v,py3.textstring) and value.startswith(v):
                    return a
        if self._allowed_value=="all":
            return _to_case(value,self._alias_case)
        raise KeyError("can not convert value {}".format(value))
    def _alias_error_str(self, alias):
        errs=ICheckingParameterClass._alias_error_str(self,alias)
        allowed_str=", ".join(repr(v) for v in self._get_alias_map())
        return "{}; allowed values are {}".format(errs,allowed_str)
    def _value_error_str(self, value):
        errs=ICheckingParameterClass._alias_error_str(self,value)
        allowed_str=", ".join(repr(v) for v in self._get_value_map())
        return "{}; allowed values are {}".format(errs,allowed_str)
class EnumParameterClass(IEnumParameterClass):
    """
    Parameter class for a enum (i.e., predefined values) parameter with the specified mapping.

    Args:
        name: parameter class name
        alias_map: mapping of aliases to device values; can be a dictionary, or a list of ``(alias,value)`` tuples
            (in the latter case non-tuple values are also allowed, indicating that value is the same as the alias);
            the list representation is useful in cases where the same alias maps to more than one value, so the map inversion is impossible
        value_map: mapping of device values to aliases; can only be a dictionary or ``None``, which means that the alias map is automatically inverted
        allowed_alias: specifies a range of allowed aliases; can be ``"exact"`` (only exact map matches are allowed),
            ``"device_value"`` (exact map matches and raw device values are allowed), or ``"all"`` (all values are allowed);
            in the latter two cases the value not in the map are passed as is.
        allowed_value: specifies a range of allowed device values; can be ``"exact"`` (only exact map matches are allowed),
            or ``"all"`` (all values are allowed); in the latter case the value not in the map is passed as is.
        alias_case: default alias parameter case for string values; can be ``None`` (no case normalization),
            or ``"lower"`` or ``"upper"`` (any received or returned alias will be normalized into this case)
        value_case: default value parameter case for string values; can be ``None`` (no case normalization),
            or ``"lower"`` or ``"upper"`` (any received or returned device value will be normalized into this case)
        match_prefix: if ``True``, then the keys in the value map (or values in the alias map, if only it is provided) are assumed to br prefixes,
            so in the value-to-alias conversion the converted value matches the map value if it just starts with it;
            useful for some SCPI devices, where the shorter version of the value can sometimes be returned.
    """
    def __init__(self, name, alias_map, value_map=None, allowed_alias="device_values", allowed_value="exact", alias_case=None, value_case=None, match_prefix=False):
        IEnumParameterClass.__init__(self,name=name,allowed_alias=allowed_alias,allowed_value=allowed_value,alias_case=alias_case,value_case=value_case,match_prefix=match_prefix)
        if isinstance(alias_map,dict):
            self._alias_map=alias_map
            self._value_map=value_map or general.invert_dict(alias_map)
        elif isinstance(alias_map,list):
            alias_map=[p if isinstance(p,(list,tuple)) else (p,p) for p in alias_map]
            self._alias_map=_first_priority_dict(alias_map)
            self._value_map=value_map or _first_priority_dict([(v,a) for a,v in alias_map])
        else:
            raise ValueError("unclear alias map: {}".format(alias_map))
        self._alias_map={_to_case(a,alias_case):_to_case(v,value_case) for (a,v) in self._alias_map.items()}
        self._value_map={_to_case(v,value_case):_to_case(a,alias_case) for (v,a) in self._value_map.items()}
    def _get_value_map(self):
        return self._value_map
    def _get_alias_map(self):
        return self._alias_map
class FunctionParameterClass(ICheckingParameterClass):
    """
    Parameter class which uses supplied methods for checking, conversion, and generating error messages.

    The arguments correspond to the parameter methods with the same names.
    When not supplied, checking methods always return ``True``, conversion methods leave value intact, and error string methods generate the default error messages.
    """
    def __init__(self, name, to_alias=None, to_value=None, check_value=None, check_alias=None, alias_err=None, value_err=None):
        ICheckingParameterClass.__init__(self,name=name)
        def_conv=lambda v: v
        def_check=lambda v: True
        def_err=self._alias_error_str
        self._value_func=(to_alias or def_conv, check_value or def_check,value_err or def_err)
        self._alias_func=(to_value or def_conv, check_alias or def_check,alias_err or def_err)
    def check_value(self, value):
        return self._value_func[1](value)
    def check_alias(self, alias):
        return self._alias_func[1](alias)
    def to_alias(self, value):
        return self._value_func[0](value)
    def to_value(self, alias):
        return self._alias_func[0](alias)
    def _alias_error_str(self, alias):
        return self._alias_func[2](alias)
    def _value_error_str(self, value):
        return self._value_func[2](value)
class CombinedParameterClass(IParameterClass):
    """
    A multi-stage combined parameter class, which performs several conversion/check stages.

    Args:
        name: parameter class name
        parameters: list of parameters classes which are combined;
            the order is from the 'most alias' to the 'most device parameter',
            i.e., when converting an alias to a device parameter, it is first passed to the first class, then the second, etc.
            (the reverse is done when converting device values into aliases)
    """
    def __init__(self, name, parameters):
        IParameterClass.__init__(self,name=name)
        self.parameters=parameters
    def __call__(self, alias, device=None):
        for p in self.parameters:
            alias=p(alias,device=device)
        return alias
    def i(self, value, device=None):
        for p in self.parameters[::-1]:
            value=p.i(value,device=device)
        return value




TRawParameterValue=collections.namedtuple("TRawParameterValue",["value"])
def pval(value):
    """Mark that the value has already been treated by the parameter class"""
    return TRawParameterValue(value)

def use_parameters(*args, **kwargs):
    """
    Wrapper to indicate that a device class method uses device parameter classes.

    The corresponding parameters classes are automatically determined if the argument name matches the parameter class name.
    The parameters classes can also be defined explicitly using keywords arguments ``arg=parameter`` supplied to the wrapper,
    where ``arg`` is the argument, and ``parameter`` is either a parameter class instance, or a parameter class name (the more preferable way).
    In addition, an argument ``_returns`` can be used to define the parameter class for the return value;
    it can also be a list or a tuple of parameter classes, indicating that the returned value is also a list or a tuple.
    """
    if len(args)>0:
        return use_parameters(**kwargs)(args[0])
    params=kwargs
    returns=params.get("_returns")
    def wrapper(func):
        sig=functions.funcsig(func)
        default_none={n for n,v in sig.defaults.items() if v is None}
        def parse_args(args, kwargs):
            device=None
            if sig.arg_names and sig.arg_names[0]=="self":
                device=args[0] if args else kwargs["self"]
            obj_params=getattr(device,"_parameters",{})
            all_args=sig.as_kwargs(args,kwargs,add_defaults=True)
            if "*" in all_args:
                raise ValueError("can't handle *args arguments")
            for n in all_args:
                if n in default_none and all_args[n] is None: # allow None if it is the method's default
                    continue
                if isinstance(all_args[n],TRawParameterValue): # marked as raw value
                    all_args[n]=all_args[n].value
                    continue
                if n in params:
                    if params[n] is not None:
                        par=obj_params.get(params[n],params[n])
                        all_args[n]=par(all_args[n],device=device)
                elif obj_params.get(n) is not None:
                    all_args[n]=obj_params[n](all_args[n],device=device)
            return all_args
        def parse_reply(res, args, kwargs):
            device=None
            if sig.arg_names and sig.arg_names[0]=="self":
                device=args[0] if args else kwargs["self"]
            obj_params=getattr(device,"_parameters",{})
            if returns is not None:
                if isinstance(returns,(tuple,list)):
                    if len(returns)!=len(res):
                        raise ValueError("length of the result {} is different from the number of specified parameters {}".format(len(returns),len(res)))
                    par=[obj_params.get(p,p) for p in returns]
                    lres=[(v if p is None else p.i(v,device=device)) for p,v in zip(par,res)]
                    res=general.as_container(lres,type(res))
                else:
                    par=obj_params.get(returns,returns)
                    res=par.i(res,device=device)
            return res
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            all_args=parse_args(args,kwargs)
            res=func(**all_args)
            return parse_reply(res,args,kwargs)
        def wrapped_wip(*args, **kwargs):
            res=func(*args,**kwargs)
            return parse_reply(res,args,kwargs)
        def wrapped_wop(*args, **kwargs):
            all_args=parse_args(args,kwargs)
            return func(**all_args)
        wrapped._wap_method=func
        wrapped._wip_method=wrapped_wip
        wrapped._wop_method=wrapped_wop
        return wrapped
    return wrapper