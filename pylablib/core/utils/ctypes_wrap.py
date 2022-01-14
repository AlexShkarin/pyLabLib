from . import functions, py3
from ..devio import data_format
from .funcargparse import getdefault

import numpy as np

import ctypes
import collections

def _default_argnames(argtypes):
    return ["arg{}".format(i+1) for i in range(len(argtypes))]

def get_value(rval):
    """Get value of a ctypes variable"""
    if isinstance(rval,(ctypes.c_voidp)):
        return rval
    if isinstance(rval,ctypes.Array):
        return rval[:]
    try:
        return rval.value
    except AttributeError:
        return rval

def setup_func(func, argtypes, restype=None, errcheck=None):
    """
    Setup a ctypes function.

    Assign argtypes (list of argument types), restype (return value type) and errcheck (error checking function called for the return value).
    """
    func.argtypes=argtypes
    if restype is not None:
        func.restype=restype
    if errcheck is not None:
        func.errcheck=errcheck

def _default_argprep(arg, argtype):
    """Prepare `arg` to be convertible to the ctypes type `argtype`"""
    if isinstance(arg,argtype):
        return arg
    if issubclass(argtype,ctypes.Array):
        if isinstance(arg,(list,tuple)):
            arg=[_default_argprep(v,argtype._type_) for v in arg]
            val=argtype()
            val[:]=arg
            return val
        else:
            return _default_argprep(arg,argtype._type_)
    if argtype in [ctypes.c_int8,ctypes.c_int16,ctypes.c_int32,ctypes.c_int64,
                    ctypes.c_uint8,ctypes.c_uint16,ctypes.c_uint32,ctypes.c_uint64]:
        return int(arg)
    if argtype in [ctypes.c_float,ctypes.c_double]:
        return float(arg)
    if argtype==ctypes.c_char_p and isinstance(arg,py3.anystring):
        return py3.as_builtin_bytes(arg)
    if argtype==ctypes.c_wchar_p and isinstance(arg,py3.anystring):
        return py3.as_str(arg)
    return arg

def _is_pointer_type(argtype, include_voidp=False, include_charp=False):
    """Check if the given ctypes type is a pointer type"""
    if issubclass(argtype,ctypes._Pointer):
        return True
    if argtype is ctypes.c_void_p:
        return include_voidp
    if (argtype is ctypes.c_char_p) or (argtype is ctypes.c_wchar):
        return include_charp
    return False


class CFunctionWrapper:
    """
    Wrapper object for ctypes function.

    The main methods are :meth:`wrap_annotated` and :meth:`wrap_bare`, which wrap a ctypes function and returns a Python function with a proper signature.
    These methods can also handle some standard use cases such as passing parameters by reference, or setting up the function arguments, or parsing the results.
    These methods can also be invoked when the wrapper is used as a callable; in this case, the exact method is determined by the presence
    of ``.argtypes`` attribute in the supplied function.
    
    Args:
        restype: default type of the function return value when calling :meth:`wrap_bare` and ``restype`` is not supplied there explicitly (defaults to ``ctypes.int``)
        errcheck: default error-checking function which is automatically called for the return value; can also be overridden explicitly when calling wrapping methods
            if ``None``, no error checking method
        tuple_single_retval (bool): determines if a single return values gets turned into a single-element tuple
        return_res (bool): determined if the function result gets returned; only used when list of return arguments (``rvals``) to wrapping functions is not explicitly supplied;
            can also be set to ``"auto"`` (default), which means that function returns its return value when no other rvals are found, and omits it otherwise.
        default_rvals: default value for ``rvals`` in :meth:`wrap_annotated` and :meth:`wrap_bare`, if it is specified as ``None`` (default for those methods).
        pointer_byref (bool): if ``True``, use explicit pointer creation instead of byref (in rare cases use of byref crashes the call).
    """
    def __init__(self, restype=None, errcheck=None, tuple_single_retval=False, return_res="auto", default_rvals="rest", pointer_byref=False):
        self.restype=restype
        self.errcheck=errcheck
        self.return_res=return_res
        self.default_rvals=default_rvals
        self.tuple_single_retval=tuple_single_retval
        self.pointer_byref=pointer_byref
    
    @staticmethod
    def _default_name(pfx, n):
        return "{}{}".format(pfx,n+1)
    @staticmethod
    def _unique_default_name(pfx, n, names):
        sfx=""
        while True:
            res=CFunctionWrapper._default_name(pfx+sfx,n)
            if res not in names:
                return res
            sfx+="_"
    @staticmethod
    def _default_names_list(pfx, n):
        return [CFunctionWrapper._default_name(pfx,i) for i in range(n)]

    def byref(self, value):
        return ctypes.pointer(value) if self.pointer_byref else ctypes.byref(value)
    def wrap_bare(self, func, argtypes, argnames=None, restype=None, args="nonrval", rvals="default", argprep=None, rconv=None, byref="all", errcheck=None):
        """
        Annotate and wrap bare C function in a Python call.

        Same as :meth:`wrap_annotated`, but annotates the function first.

        Args:
            func: C function
            argtypes: list of ctypes types corresponding to function arguments; gets assigned as ``func.argtypes``
            argnames: list of argument names; if not supplied, generated automatically as ``"arg1"``, ``"arg2"``, etc. Same for names which are defined as ``None``.
            restype: type of the function return value; if ``None``, use the value supplied to the wrapper constructor (defaults to ``ctypes.int``)
            args: names of Python function arguments; can also be ``"all"`` (all C function arguments in that order), or ``"nonrval"`` (same, but with return value arguments excluded)
                by default, use ``"nonrval"``
            rvals: names of return value arguments; can include either a C function argument name, or ``None`` (which means the function return value);
                can also be ``"rest"`` (listsall the arguments not included into ``args``; if ``args=="nonrval"``, assume that there are no rvals),
                ``"pointer"`` (assume that all pointer arguments are rvals; this does not include ``c_void_p``, ``c_char_p``, or ``c_wchar_p``);
                by default, use the value supplied on the wrapper creation (``"rest"`` by default)
            argprep: dictionary ``{name: prep}`` of ways to prepare of C function arguments;
                each ``prep`` can be a value (which is assumed to be default argument value), or a callable, which is given values of Python function arguments
            rconv:  dictionary ``{name: conv}`` of converters of the return values;
                each ``conv`` is a function which takes 3 arguments: unconverted ctypes value, dictionary of all C function arguments, and dictionary of all Python function arguments
                if ``conv`` takes less than 3 argument, then the arguments list is trimmed (e.g., if it takes only one argument, it will be an unconverted value)
                ``conv`` can also be ``"ctypes"`` (return raw ctypes value), or ``"raw"`` (return raw value for buffers).
            byref: list of all argument names which should by passed by reference; by default, it includes all arguments listed in ``rvals``
            errcheck: error-checking function which is automatically called for the return value;
                if ``None``, use the value supplied to the wrapper constructor (none by default)
        """
        if func is None:
            return None
        restype=getdefault(restype,self.restype)
        if argnames is None:
            argnames=self._default_names_list("arg",len(argtypes))
        else:
            for i in range(len(argnames)):
                if argnames[i] is None:
                    argnames[i]=self._unique_default_name("arg",i,argnames)
        if len(argnames)!=len(argtypes):
            raise ValueError("argnames and argtypes have different length: {} ({}) vs. {} ({})".format(len(argnames),argnames,len(argtypes),argtypes))
        setup_func(func,argtypes,restype=restype,errcheck=errcheck)
        func.argnames=argnames
        return self.wrap_annotated(func,args=args,rvals=rvals,argprep=argprep,rconv=rconv,byref=byref,errcheck=errcheck)

    @staticmethod
    def _prepare_arguments(argnames, argtypes, kwargs, argprep):
        args=[]
        for n,t in zip(argnames,argtypes):
            if n in argprep:
                p=argprep[n]
                v=functions.call_cut_args(p,**kwargs) if hasattr(p,"__call__") else p
            elif n in kwargs:
                v=kwargs[n]
            else:
                v=None
            if v is None:
                cv=t()
            elif t=="P" or isinstance(v,t): # t=="P" means that it is c_voidp argument supplied with byref
                cv=v
            elif t is ctypes.c_voidp: # these get converted later, immediately before passing
                cv=v
            else:
                pv=_default_argprep(v,t)
                cv=pv if isinstance(pv,t) else t(pv)
            args.append(cv)
        return args
    @staticmethod
    def _convert_results(rvals, cargs, retval, kwargs, rconv):
        res=[]
        for n in rvals:
            v=retval if n is None else cargs[n]
            if n in rconv:
                if rconv[n]=="raw":
                    v=v.raw
                elif rconv[n]!="ctypes":
                    v=functions.call_cut_args(rconv[n],v,cargs,kwargs)
            else:
                v=get_value(v)
            res.append(v)
        return tuple(res)
    def wrap_annotated(self, func, args="nonrval", rvals="default", alias=None, argprep=None, rconv=None, byref="all", errcheck=None):
        """
        Wrap annotated C function in a Python call.

        Assumes that the functions has defined ``.argtypes`` (list of argument types) and ``.argnames`` (list of argument names) attributes.

        Args:
            func: C function
            args: names of Python function arguments; can also be ``"all"`` (all C function arguments in that order), or ``"nonrval"`` (same, but with return value arguments excluded);
                by default, use ``"nonrval"``
            rvals: names of return value arguments; can include either a C function argument name, or ``None`` (which means the function return value);
                can also be ``"rest"`` (listsall the arguments not included into ``args``; if ``args=="nonrval"``, assume that there are no rvals),
                ``"pointer"`` (assume that all pointer arguments are rvals; this does not include ``c_void_p``, ``c_char_p``, or ``c_wchar_p``);
                by default, use the value supplied on the wrapper creation (``"rest"`` by default)
            alias: either a list of argument names which replace ``.argnames``, or a dictionary ``{argname: alias}`` which transforms names;
                all names in all other parameters (``rvals``, ``argprep``, ``rconv``, and ``byref``) take aliased names
            argprep: dictionary ``{name: prep}`` of ways to prepare of C function arguments;
                each ``prep`` can be a value (which is assumed to be default argument value), or a callable, which is given values of Python function arguments
            rconv:  dictionary ``{name: conv}`` of converters of the return values;
                each ``conv`` is a function which takes 3 arguments: unconverted ctypes value, dictionary of all C function arguments, and dictionary of all Python function arguments
                if ``conv`` takes less than 3 argument, then the arguments list is trimmed (e.g., if it takes only one argument, it will be an unconverted value)
            byref: list of all argument names which should by passed by reference; by default, it includes all arguments listed in ``rvals``
            errcheck: error-checking function which is automatically called for the return value;
                if ``None``, use the value supplied to the wrapper constructor (none by default)
        """
        if func is None:
            return None
        if isinstance(alias,(list,tuple)):
            argnames=list(alias)
        else:
            alias=alias or {}
            fargnames=getattr(func,"argnames",self._default_names_list("arg",len(func.argtypes)))
            argnames=[alias.get(n,n) for n in fargnames]
        if rvals=="default":
            rvals=self.default_rvals
        if rvals=="pointer":
            rvals=[n for (n,t) in zip(argnames,func.argtypes) if _is_pointer_type(t,include_charp=False,include_voidp=False)]
            # if args!="all":
            #     rvals=[n for n in rvals if n not in args]
            return_res=(len(rvals)==0) if self.return_res=="auto" else self.return_res
            if return_res:
                rvals=[None]+rvals
        if args=="all" or (args=="nonrval" and rvals=="rest"):
            args=argnames
        elif args=="nonrval":
            args=[a for a in argnames if a not in rvals]
        if rvals=="rest":
            rvals=[n for n in argnames if n not in args]
            return_res=(len(rvals)==0) if self.return_res=="auto" else self.return_res
            if return_res:
                rvals=[None]+rvals
        argprep=argprep or {}
        rconv=rconv or {}
        if byref=="all":
            byref=[v for v in rvals if v is not None]
        byref=byref or []
        for n in rvals:
            if not ((n is None) or (n in argnames)):
                raise ValueError("rval parameter '{}' is not among the function arguments {}".format(n,argnames))
        for n in byref:
            if n not in argnames:
                raise ValueError("byref parameter '{}' is not among the arguments {}".format(n,argnames))
        for n in argprep:
            if n not in argnames:
                raise ValueError("argprep parameter '{}' is not among the arguments {}".format(n,argnames))
        for n in rconv:
            if n not in rvals:
                raise ValueError("rconv parameter '{}' is not among the return values {}".format(n,rvals))
        errcheck=getdefault(errcheck,self.errcheck)
        if errcheck is not None:
            func.errcheck=errcheck
        prep_argtypes=[t._type_ if n in byref else t for (n,t) in zip(argnames,func.argtypes)]
        doc="Wrapped C function.\n\nC function arguments: {}\n\nPassed by reference: {}".format(
                ", ".join(["{} {}".format(t.__name__,n) for n,t in zip(argnames,func.argtypes)]),", ".join(list(byref)))
        sign=functions.FunctionSignature(args,name=func.__name__,doc=doc)
        def wrapped_func(*vargs, **kwargs):
            kwargs.update(dict(zip(args,vargs)))
            func_args=self._prepare_arguments(argnames,prep_argtypes,kwargs,argprep)
            def _to_call_arg(n, t, a):
                if n in byref:
                    return self.byref(a)
                elif t is ctypes.c_voidp:
                    return ctypes.cast(a,ctypes.c_voidp)
                else:
                    return a
            call_args=[_to_call_arg(n,t,a) for (n,t,a) in zip(argnames,prep_argtypes,func_args)]
            retval=func(*call_args)
            res=self._convert_results(rvals or [None],dict(zip(argnames,func_args)),retval,kwargs,rconv)
            if (not self.tuple_single_retval) and len(res)==0:
                return None
            elif (not self.tuple_single_retval) and len(res)==1:
                return res[0]
            return res
        return sign.wrap_function(wrapped_func)

    def __call__(self, func, *args, **kwargs):
        if func is None:
            return None
        elif hasattr(func,"argtypes"):
            return self.wrap_annotated(func,*args,**kwargs)
        else:
            return self.wrap_bare(func,*args,**kwargs)



def strprep(l, ctype=None, unicode=False):
    """
    Make a string preparation function.
    
    Return a function which creates a string with a fixed length of `l` bytes and returns a pointer to it.
    `ctype` can specify the type of the result (by default, :class:`ctypes.c_char_p`).
    """
    if unicode:
        ctype=ctype or ctypes.c_wchar_p
        def prep(*args, **kwargs):  # pylint: disable=unused-argument
            return ctypes.cast(ctypes.create_unicode_buffer(l),ctype)
    else:
        ctype=ctype or ctypes.c_char_p
        def prep(*args, **kwargs):  # pylint: disable=unused-argument
            return ctypes.cast(ctypes.create_string_buffer(l),ctype)
    return prep

def buffprep(size_arg_pos, dtype):
    """
    Make a buffer preparation function.
    
    Return a function which creates a string with a variable size (specified by an argument at a position `size_arg_pos`).
    The buffer size is given in elements. `dtype` specifies the datatype of the buffer, whose size is used to determine buffer size in bytes.
    """
    el_size=data_format.DataFormat.from_desc(dtype).size
    def prep(*args, **kwargs):  # pylint: disable=unused-argument
        n=args[size_arg_pos]
        return ctypes.create_string_buffer(n*el_size)
    return prep
def buffconv(size_arg_pos, dtype):
    """
    Make a buffer conversion function.
    
    Return a function which converts a pointer of a variable size (specified by an argument at a position `size_arg_pos`) into a numpy array.
    The buffer size is given in elements. `dtype` specifies the datatype of the resulting array.
    """
    dformat=data_format.DataFormat.from_desc(dtype)
    def conv(buff, *args, **kwargs):  # pylint: disable=unused-argument
        n=args[size_arg_pos]
        data=ctypes.string_at(buff,n*dformat.size)
        return np.require(np.frombuffer(data,dtype=dformat.to_desc("numpy")),requirements="W")
    return conv





class CStructWrapper:
    """
    Wrapper around a ctypes structure, which allows for easier creation of parsing of these structures.

    When created, all structure fields can be accessed/modified as attributes of the wrapper object.
    It can also be converted into tuple using :meth:`tup` method, or back into C structure using :meth:`to_struct` method.
    
    Class variable ``_struct`` should be set to the ctypes structure which is being wrapped.
    Several other class variables determine the behavior when generating and parsing:
    
        - ``_prep``: dictionary ``{name: prep}`` of methods to prepare individual structure parameters;
          can be either a value or a function (which takes as ordered arguments all structure fields as ctypes values)
        - ``_conv``: dictionary ``{name: conv}`` of methods to convert individual structure parameters when parsing a C structure;
          can be either a function (which takes ctypes value of the field as a single argument) or a value;
          also can be used as a source of default values on wrapper creation
        - ``_tup``: dictionary ``{name: conv}`` of functions to convert structure values when generating a tuple
        - ``_tup_exc``: list of values to exclude from the resulting tuple
        - ``_tup_inc``: list of values to include in the resulting tuple (if ``None``, include all)
        - ``_tup_add``: list of values to add to the resulting tuple (these values must then exist either as attributes, or as entries in ``_tup`` dictionary)
        - ``_tup_order``: order of fields in the returned tuple (by default, same as structure order)
    
    Also specifies two overloaded methods for a more flexible preparation/conversion of structures.
    :meth:`.conv` takes no arguments and is called in the end of wrapper creation to finish setting up attributes.
    :meth:`.prep` takes a single argument (C structure) and is called when converting into a C structure to finish setting up the fields (e.g., size field).

    Args:
        struct: C structure to wrap (if ``None``, create a new 'blank' structure).
    """
    class _struct(ctypes.Structure):
        _fields_=[]
    _prep={}
    _conv={}
    _tup={} # functions for struct-to-tuple conversion
    _tup_exc=[] # fields to exclude in struct-to-tuple conversion
    _tup_inc=None # fields to include in struct-to-tuple conversion (if not specified, include all)
    _tup_add=[] # fields to add in struct-to-tuple conversion
    _tup_order=None # tuple fields order in struct-to-tuple conversion (by default, same as in the struct)
    def __init__(self, struct=None):
        struct=struct or self._struct()
        if not isinstance(struct,self._struct):
            raise ValueError("source should be of type {}".format(self._struct.__name__))
        fnames,_=zip(*self._struct._fields_)
        for f in fnames:
            cv=getattr(struct,f)
            if f in self._conv:
                c=self._conv[f]
                v=c(cv) if hasattr(c,"__call__") else c
            else:
                v=get_value(cv)
            setattr(self,f,v)
        self.conv()
    def to_struct(self):
        """Convert wrapper into a C structure"""
        params={}
        fnames,_=zip(*self._struct._fields_)
        for f in fnames:
            if f not in params:
                params[f]=getattr(self,f)
        ordparams=[params[f] for f in fnames]
        cparams={}
        for f,ct in self._struct._fields_:
            if f in self._prep:
                p=self._prep[f]
                cv=p(*ordparams) if hasattr(p,"__call__") else p
            else:
                cv=params[f]
            cparams[f]=_default_argprep(cv,ct)
        return self.prep(self._struct(**cparams))

    def prep(self, struct):
        """Prepare C structure after creation (by default, do nothing)"""
        return struct
    def conv(self):
        """Prepare wrapper after setting up the fields from the wrapped structure"""
        pass
    @classmethod
    def _get_tcls(cls, fnames):
        if getattr(cls,"fnames",None)!=fnames:
            cls.fnames=fnames
            cls.tcls=collections.namedtuple(cls.__name__,[("f_"+n if n.startswith("_") else n) for n in fnames])
        return cls.tcls
    def tup(self):
        """Convert wrapper into a named tuple"""
        params={}
        fnames,_=zip(*self._struct._fields_)
        fnames=[f for f in fnames if f not in self._tup_exc]
        fnames+=self._tup_add
        if self._tup_inc is not None:
            fnames=[f for f in fnames if f in self._tup_inc]  # pylint: disable=unsupported-membership-test
        if self._tup_order is not None:
            def key(name):
                try:
                    return self._tup_order.index(name)
                except ValueError:
                    return len(self._tup_order)
            fnames.sort(key=key)
        for f in fnames:
            if f not in params:
                params[f]=getattr(self,f)
            if f in self._tup:
                params[f]=self._tup[f](params[f])
            elif isinstance(params[f],ctypes.Array):
                params[f]=params[f][:]
        vals=[params[f] for f in fnames]
        tcls=self._get_tcls(fnames)
        return tcls(*vals)

    @classmethod
    def prep_struct(cls, *args, **kwargs):  # pylint: disable=unused-argument
        """Prepare a blank C structure"""
        return cls().to_struct()
    @classmethod
    def prep_struct_args(cls, *args, **kwargs):
        """Prepare a C structure with the given supplied fields"""
        s=cls()
        if args:
            kwargs=kwargs.copy()
            kwargs.update({n:v for (n,_),v in zip(cls._struct._fields_,args)})
        for k,v in kwargs.items():
            setattr(s,k,v)
        return s.to_struct()
    @classmethod
    def tup_struct(cls, struct, *args, **kwargs):  # pylint: disable=unused-argument
        """Convert C structure into a named tuple"""
        return cls(struct).tup()


def class_tuple_to_dict(val, norm_strings=True, expand_lists=False):
    """
    Convert a named tuple (usually, a tuple returned by :meth:`CStructWrapper.tup`) into a dictionary.

    Iterate recursively over all named tuple elements as well.
    If ``norm_strings==True``, automatically translate byte strings into regular ones.
    If ``expand_lists==True``, iterate recursively over lists members.
    """
    if isinstance(val,py3.bytestring) and norm_strings:
        return py3.as_str(val)
    elif isinstance(val,list) and expand_lists:
        val=[class_tuple_to_dict(el,norm_strings=norm_strings,expand_lists=expand_lists) for el in val]
        return dict(enumerate(val))
    elif hasattr(val,"_asdict"):
        val=val._asdict()
        for k in val:
            val[k]=class_tuple_to_dict(val[k],norm_strings=norm_strings,expand_lists=expand_lists)
        return val
    else:
        return val