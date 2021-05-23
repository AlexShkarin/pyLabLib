### Interface for a generic device class ###

from ..utils import functions
 
_info_node_kinds=["settings","status","full_info"]

class IDevice(object):
    """
    A base class for an instrument.
     
    Contains some useful functions for dealing with device settings.
    """
    def __init__(self):
        object.__init__(self)
        self._nodes_ignore_error={"get":(),"set":()}
        self._info_nodes=dict([(ik,{}) for ik in _info_node_kinds])
        self._info_nodes_order=dict([(ik,[]) for ik in _info_node_kinds])
        self._add_full_info_node("cls",lambda: self.__class__.__name__)
         
    def open(self):
        """Open the connection"""
        pass
    def close(self):
        """Close the connection"""
        pass
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
    def _add_info_node(self, path, kind, getter=None, setter=None, ignore_error=(), mux=None, multiarg=True):
        """
        Adds an info parameter.
         
        Args:
            path: parameter name.
            kind(str): can be ``"settings"`` (device settings parameter), ``"status"`` (device status parameter) or ``"full_info"`` (full device info).
            getter: methods for getting this parameter. Can be ``None``, meaning that this parameter is ignored when executing :meth:`get_settings`/:meth:`get_full_status`/:meth:`get_full_info`.
            setter: methods for setting this parameter. Can be ``None``, meaning that this parameter is ignored when executing :meth:`apply_settings`.
            ignore_error(tuple): is a list of exception classes; if raised during getter/setter call, they are ignored.
            mux(tuple): 1- or 2-tuple with parameters for function multiplexing (calling several times and combining result in a list).
                The first element is an iterable of argument values to be iterated over, the second argument is the position where this argument is inserted (by default, 0)
            multiarg(bool): if ``True`` and the setter argument is a tuple, interpret it as a tuple of arguments and expand it; otherwise, keep it as a single tuple argument.
        """
        if kind not in self._info_nodes:
            raise ValueError("unrecognized info node kind: {}".format(kind))
        if not isinstance(ignore_error,tuple):
            ignore_error=(ignore_error,)
        if multiarg and setter:
            osetter=setter
            setter=lambda v: functions.call_cut_args(osetter,*v) if isinstance(v,tuple) else osetter(v)
        if mux:
            getter=self._multiplex_func(getter,*mux[:2],multiarg=multiarg) if getter else None
            setter=self._multiplex_func(setter,*mux[:2],multiarg=multiarg) if setter else None
        self._info_nodes[kind][path]=(getter,setter,ignore_error)
        self._info_nodes_order[kind].append(path)
    def _add_full_info_node(self, path, getter=None, ignore_error=(), mux=None):
        return self._add_info_node(path,"full_info",getter=getter,ignore_error=ignore_error,mux=mux)
    def _add_status_node(self, path, getter=None, ignore_error=(), mux=None):
        return self._add_info_node(path,"status",getter=getter,ignore_error=ignore_error,mux=mux)
    def _add_settings_node(self, path, getter=None, setter=None, ignore_error=(), mux=None, multiarg=True):
        return self._add_info_node(path,"settings",getter=getter,setter=setter,ignore_error=ignore_error,mux=mux,multiarg=multiarg)
    def _get_info(self, kinds, nodes=None):
        """
        Get dict ``{name: value}`` containing all the device settings.
         
        `kinds` is the list of info nodes kinds to be included in the info.
        `nodes` specifies nodes to acquire.
        """
        for kind in kinds:
            if kind not in self._info_nodes:
                raise ValueError("unrecognized info node kind: {}".format(kind))
        info={}
        for kind in kinds:
            for k in self._info_nodes_order[kind]:
                if (nodes is None or k in nodes):
                    g,_,err=self._info_nodes[kind][k]
                    if g:
                        try:
                            info[k]=g()
                        except err+self._nodes_ignore_error["get"]:
                            pass
        return info
    def get_settings(self, nodes=None):
        """
        Get dict ``{name: value}`` containing all the device settings.
        
        `nodes` specifies nodes to acquire.
        """
        return self._get_info(["settings"],nodes=nodes)
    def get_full_status(self, nodes=None):
        """
        Get dict ``{name: value}`` containing the device status (including settings).
        
        `nodes` specifies nodes to acquire.
        """
        return self._get_info(["settings","status"],nodes=nodes)
    def get_full_info(self, nodes=None):
        """
        Get dict ``{name: value}`` containing full device information (including status and settings).
        
        `nodes` specifies nodes to acquire.
        """
        return self._get_info(["settings","status","full_info"],nodes=nodes)
    def apply_settings(self, settings):
        """
        Apply the settings.
         
        `settings` is the dict ``{name: value}`` of the device available settings.
        Non-applicable settings are ignored.
        """
        for k in self._info_nodes_order["settings"]:
            _,s,err=self._info_nodes["settings"][k]
            if s and (k in settings):
                try:
                    s(settings[k])
                except err+self._nodes_ignore_error["set"]:
                    pass
    def __getitem__(self, key):
        """Get the value of a settings, status, or full info parameter."""
        for kind in _info_node_kinds:
            if key in self._info_nodes[kind]:
                g=self._info_nodes[kind][key][0]
                if g:
                    return g()
                raise ValueError("no getter for value '{}'".format(key))
        raise KeyError("no property '{}'".format(key))
    def __setitem__(self, key, value):
        """Set the value of a settings parameter."""
        if key in self._info_nodes["settings"]:
            s=self._info_nodes["settings"][key][1]
            if s:
                return s(value)
            raise ValueError("no setter for value '{}'".format(key))
        raise KeyError("no property '{}'".format(key))