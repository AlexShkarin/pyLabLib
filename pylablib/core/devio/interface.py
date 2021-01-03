### Interface for a generic device class ###

from ..utils import functions, dictionary
 
_device_var_kinds=["settings","status","info"]

class IDevice:
    """
    A base class for an instrument.
     
    Contains some useful functions for dealing with device settings.
    """
    def __init__(self):
        self._device_var_ignore_error={"get":(),"set":()}
        self._device_vars=dict([(ik,{}) for ik in _device_var_kinds])
        self._device_vars_order=dict([(ik,[]) for ik in _device_var_kinds])
        self._add_status_variable("cls",lambda: self.__class__.__name__)
        self.v=dictionary.ItemAccessor(getter=self.get_device_variable,setter=self.set_device_variable)
         
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
    def _add_device_variable(self, path, kind, getter=None, setter=None, ignore_error=(), mux=None, multiarg=True):
        """
        Adds a device variable.
         
        Args:
            path: variable name.
            kind(str): can be ``"settings"`` (device settings parameter), ``"status"`` (device status variable) or ``"info"`` (device info variable).
            getter: methods for getting this variable. Can be ``None``, meaning that this variable is ignored when executing :meth:`get_settings`/:meth:`get_full_status`/:meth:`get_full_info`.
            setter: methods for setting this variable. Can be ``None``, meaning that this variable is ignored when executing :meth:`apply_settings`.
            ignore_error(tuple): is a list of exception classes; if raised during getter/setter call, they are ignored.
            mux(tuple): 1- or 2-tuple with parameters for function multiplexing (calling several times and combining result in a list).
                The first element is an iterable of argument values to be iterated over, the second argument is the position where this argument is inserted (by default, 0)
            multiarg(bool): if ``True`` and the setter argument is a tuple, interpret it as a tuple of arguments and expand it; otherwise, keep it as a single tuple argument.
        """
        if kind not in self._device_vars:
            raise ValueError("unrecognized info node kind: {}".format(kind))
        if not isinstance(ignore_error,tuple):
            ignore_error=(ignore_error,)
        if multiarg and setter:
            osetter=setter
            setter=lambda v: functions.call_cut_args(osetter,*v) if isinstance(v,tuple) else osetter(v)
        if mux:
            getter=self._multiplex_func(getter,*mux[:2],multiarg=multiarg) if getter else None
            setter=self._multiplex_func(setter,*mux[:2],multiarg=multiarg) if setter else None
        self._device_vars[kind][path]=(getter,setter,ignore_error)
        if path not in self._device_vars_order[kind]:
            self._device_vars_order[kind].append(path)
    def _add_info_variable(self, path, getter=None, ignore_error=(), mux=None):
        return self._add_device_variable(path,"info",getter=getter,ignore_error=ignore_error,mux=mux)
    def _add_status_variable(self, path, getter=None, ignore_error=(), mux=None):
        return self._add_device_variable(path,"status",getter=getter,ignore_error=ignore_error,mux=mux)
    def _add_settings_variable(self, path, getter=None, setter=None, ignore_error=(), mux=None, multiarg=True):
        return self._add_device_variable(path,"settings",getter=getter,setter=setter,ignore_error=ignore_error,mux=mux,multiarg=multiarg)
    def _get_device_variables(self, kinds, variables=None):
        """
        Get dict ``{name: value}`` containing all the device settings.
         
        `kinds` is the list of info variables kinds to be included in the info.
        `variables` specifies variables to acquire.
        """
        for kind in kinds:
            if kind not in self._device_vars:
                raise ValueError("unrecognized info node kind: {}".format(kind))
        info={}
        for kind in kinds:
            for k in self._device_vars_order[kind]:
                if (variables is None or k in variables):
                    g,_,err=self._device_vars[kind][k]
                    all_err=err+self._device_var_ignore_error["get"]
                    if g:
                        try:
                            info[k]=g()
                        except all_err:
                            pass
        return info
    def get_settings(self, variables=None):
        """
        Get dict ``{name: value}`` containing all the device settings.
        
        `variables` specifies variables to acquire.
        """
        return self._get_device_variables(["settings"],variables=variables)
    def get_full_status(self, variables=None):
        """
        Get dict ``{name: value}`` containing the device status (including settings).
        
        `variables` specifies variables to acquire.
        """
        return self._get_device_variables(["settings","status"],variables=variables)
    def get_full_info(self, variables=None):
        """
        Get dict ``{name: value}`` containing full device information (including status and settings).
        
        `variables` specifies variables to acquire.
        """
        return self._get_device_variables(["settings","status","info"],variables=variables)
    def apply_settings(self, settings):
        """
        Apply the settings.
         
        `settings` is the dict ``{name: value}`` of the device available settings.
        Non-applicable settings are ignored.
        """
        for k in self._device_vars_order["settings"]:
            _,s,err=self._device_vars["settings"][k]
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