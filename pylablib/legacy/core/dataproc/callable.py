from future.utils import viewitems
from builtins import zip

from ..utils import functions as function_utils #@UnresolvedImport
import numpy as np

class ICallable(object):
    """
    Fit function generalization.
    
    Has a set of mandatory argument with no default values and
    a set of parameters with default values (there may or may not be an explicit list of them).
    
    All the arguments are passed explicitly by name. Passed value supersede default values.
    Extra arguments (not used in the calculations) are ignored.
    
    Assumed (but not enforced) to be immutable: changes after creation can break the behavior.
    
    Implements (possibly; depends on subclasses) call namelist binding boosting:
    if the function is to be called many times with the same parameter names list,
    one can first bind parameters list, and then call bound function with the corresponding arguments.
    This way, ``callable(**p)`` should be equivalent to ``callable.bind(p.keys())(*p.values())``.
    """
    def __init__(self):
        object.__init__(self)
    def has_arg(self, arg_name):
        """Determine if the function has an argument `arg_name` (of all 3 categories)."""
        raise NotImplementedError("ICallable.has_arg")
    def filter_args_dict(self, args):
        """Filter argument names dictionary to leave only the arguments that are used."""
        return dict((k,v) for (k,v) in viewitems(args) if self.has_arg(k))
    def get_mandatory_args(self):
        """Return list of mandatory arguments (these are the ones without default values)."""
        raise NotImplementedError("ICallable.get_mandatory_args")
    def is_mandatory_arg(self, arg_name):
        """Check if the argument `arg_name` is mandatory.""" 
        return arg_name in self.get_mandatory_args()
    def get_arg_default(self, arg_name):
        """
        Return default value of the argument `arg_name`.
        
        Raise :exc:`KeyError` if the argument is not defined or :exc:`ValueError` if it has no default value.
        """
        raise NotImplementedError("ICallable.get_arg_default")
    
    def __call__(self, **params):
        raise NotImplementedError("ICallable.__call__")
    def bind(self, arg_names, **bound_params):
        """Bind function to a given parameters set, leaving `arg_names` as free parameters (in the given order)."""
        bound_params=bound_params.copy()
        covered_args=set(bound_params)
        covered_args.update(arg_names)
        uncovered_mand_args=self.get_mandatory_args().difference(covered_args)
        if len(uncovered_mand_args)>0:
            raise TypeError("mandatory parameters not supplied: {0}".format(list(uncovered_mand_args)))
        def bound_call(*args, **call_params):
            params=bound_params.copy()
            params.update(call_params)
            params.update(zip(arg_names,args))
            return self(**params)
        return bound_call
        #sig=FunctionSignature(arg_names=arg_names,kwarg_name="kwargs")
        #return sig.wrap_function(bound_call)
    
    class NamesBoundCall(object):
        def __init__(self, func, names, bound_params):
            object.__init__(self)
            self._func=func
            self._names=names
            self._bound_params=bound_params
        def __call__(self, *params):
            self._bound_params.update(zip(self._names,params))
            return self._func(self._bound_params)
    def bind_namelist(self, arg_names, **bound_params):
        """
        Bind namelist to boost subsequent calls.
        
        Similar to ``bind(arg_names)``, but bound function doesn't accept additional parameters and can be boosted.
        """
        bound_call=self.NamesBoundCall(self,arg_names,bound_params)
        return bound_call
        #sig=FunctionSignature(arg_names=arg_names,kwarg_name="kwargs")
        #return sig.wrap_function(bound_call)
    
    


def _join_list_results(res_vec, join_method="stack"):
    if len(res_vec)>0 and np.ndim(res_vec[0])>0:
        if join_method=="list":
            return res_vec
        elif join_method=="stack":
            return np.column_stack(res_vec)
        elif join_method=="concatenate":
            return np.concatenate(res_vec)
        else:
            raise ValueError("unrecognized joining method: {0}".format(join_method))
    else:
        return np.array(res_vec)
    
    
class MultiplexedCallable(ICallable):
    """
    Multiplex a single callable based on a single parameter.
    
    If the function is called with this parameter as an iterable,
    then the underlying callable will be called for each value of the parameter separately,
    and the results will be joined into a single array
    (if return the values are scalar, they're joined in 1D array; otherwise, they're joined using `join_method`).
    
    Args:
        func (callable): Function to be parallelized.
        multiplex_by (str): Name of the argument to be multiplexed by.
        join_method (str): Method for combining individual results together if they're non-scalars.
            Can be either ``'list'`` (combine the results in a single list),
            ``'stack'`` (combine using :func:`numpy.column_stack`, i.e., add dimension to the result),
            or ``'concatenate'`` (concatenate the return values; the dimension of the result stays the same).
    
    Multiplexing also makes use of call signatures for underlying function even if ``__call__`` is used.
    
    Note that this operation is slow, and should be used only for high-dimensional multiplexing;
    for 1D case it's much better to just use numpy arrays as arguments and rely on numpy parallelizing.
    """
    def __init__(self, func, multiplex_by, join_method="stack"):
        ICallable.__init__(self)
        self._func=to_callable(func)
        self._mvar=multiplex_by
        self._join_method=join_method
        if not func.has_arg(multiplex_by):
            raise ValueError("can't multiplex by non-existing arguments: {0}".format(multiplex_by))
    def has_arg(self, arg_name):
        return self._func.has_arg(arg_name)
    def get_mandatory_args(self):
        return self._func.get_mandatory_args()
    def get_arg_default(self, arg_name):
        return self._func.get_arg_default(arg_name)
    
    class NamesBoundCall(object):
        def __init__(self, func, names, bound_params):
            object.__init__(self)
            self._join_method=func._join_method
            if func._mvar in names:
                self._mvar_source=names.index(func._mvar)
                self._subfunc_bound=func._func.bind_namelist(names,**bound_params)
            else:
                self._mvar_source='default'
                if func._mvar in bound_params:
                    bound_params=bound_params.copy()
                    self._mvar_default=bound_params.pop(func._mvar)
                else:
                    self._mvar_default=func.get_arg_default(func._mvar)
                self._subfunc_bound=func._func.bind_namelist(names+[func._mvar],**bound_params)
        def __call__(self, *params):
            subfunc=self._subfunc_bound
            if self._mvar_source=='default':
                if np.isscalar(self._mvar_default):
                    return subfunc(*(list(params)+[self._mvar_default]))
                else:
                    res_vec=[]
                    params=list(params)+[None]
                    for m in self._mvar_default:
                        params[-1]=m
                        res_vec.append(subfunc(*params))
                    return _join_list_results(res_vec,join_method=self._join_method)
            else:
                m_source=self._mvar_source
                if np.isscalar(params[m_source]):
                    return subfunc(*params)
                else:
                    res_vec=[]
                    params=list(params)
                    for m in params[m_source]:
                        params[m_source]=m
                        res_vec.append(subfunc(*params))
                    return _join_list_results(res_vec,join_method=self._join_method)
    def __call__(self, **params):
        return self.bind_namelist([],**params)()
            
            
            
class JoinedCallable(ICallable):
    """
    Join several callables sharing the same arguments list.
    
    The results will be joined into a single array
    (if return the values are scalar, they're joined in 1D array; otherwise, they're joined using `join_method`).
    
    Args:
        funcs ([callable]): List of functions to be joined together.
        join_method (str): Method for combining individual results together if they're non-scalars.
            Can be either ``'list'`` (combine the results in a single list),
            ``'stack'`` (combine using :func:`numpy.column_stack`, i.e., add dimension to the result),
            or ``'concatenate'`` (concatenate the return values; the dimension of the result stays the same).
    """
    def __init__(self, funcs, join_method="stack"):
        ICallable.__init__(self)
        if len(funcs)==0:
            raise ValueError("can't joint zero functions")
        self._funcs=[to_callable(f) for f in funcs]
        self._mand_args=set()
        for f in funcs:
            self._mand_args.update(f.get_mandatory_args())
        self._join_method=join_method
    def has_arg(self, arg_name):
        for f in self._funcs:
            if f.has_arg(arg_name):
                return True
        return False
    def get_mandatory_args(self):
        return self._mand_args
    def get_arg_default(self, arg_name):
        for f in self._funcs:
            if f.has_arg(arg_name):
                return f.get_arg_default(arg_name)
        raise KeyError("no argument with name {0}".format(arg_name))
    
    def __call__(self, **params):
        return _join_list_results([f(**params) for f in self._funcs],join_method=self._join_method)
    
    class NamesBoundCall(object):
        def __init__(self, func, names, bound_params):
            object.__init__(self)
            self._join_method=func._join_method
            self._funcs=[f.bind_namelist(names,**bound_params) for f in func._funcs]
        def __call__(self, *params):
            return _join_list_results([f(*params) for f in self._funcs],join_method=self._join_method)
    
    




class FunctionCallable(ICallable):
    """
    Callable based on a function or a method.
    
    Args:
        func: Function to be wrapped.
        function_signature: A :class:`~.functions.FunctionSignature` object supplying information
            about function's argument names and default values, if they're different from what's extracted from its signature.
        defaults (dict): A dictionary ``{name: value}`` of additional default parameters values. Override the defaults from the signature.
            All default values must be pass-able to the function as a parameter
        alias (dict): A dictionary ``{alias: original}`` for renaming some of the original arguments.
            Original argument names can't be used if aliased (though, multi-aliasing can be used explicitly, e.g., ``alias={'alias':'arg','arg':'arg'}``).
            A name can be blocked (its usage causes error) if it's aliased to None (``alias={'blocked_name':None}``).
    
    Optional non-named arguments in the form ``*args`` are not supported, since all the arguments are passed to the function by keywords.
    
    Optional named arguments in the form ``**kwargs`` are supported only if their default values are explicitly provided in defaults
    (otherwise it would be unclear whether argument should be added into ``**kwargs`` or ignored altogether).
    """
    def __init__(self, func, function_signature=None, defaults=None, alias=None):
        ICallable.__init__(self)
        self._func=func
        self._set_alias(alias)
        if function_signature is None:
            function_signature=function_utils.FunctionSignature.from_function(func)
        self._defaults=function_signature.defaults.copy()
        if defaults is not None:
            self._defaults.update(self._apply_unalias_dict(defaults))
        self._declared_args=set(function_signature.arg_names)
        self._mand_args=set([a for a in function_signature.arg_names if not a in self._defaults])
        self._mand_args_alias=set(self._apply_alias(self._mand_args))
        self._use_keywords=function_signature.kwarg_name is not None
    def _set_alias(self, alias):
        self._alias=alias
        self._masked=set()
        if alias is not None:
            self._masked.update(alias.values())
            self._rev_alias=dict((v,k) for (k,v) in viewitems(self._alias) if v is not None)
        else:
            self._rev_alias=None
    def _apply_alias(self, params):
        if self._alias is None:
            return params
        try:
            return [self._rev_alias.get(p,p) for p in params]
        except TypeError:
            return self._rev_alias.get(params,params)
    def _apply_unalias(self, param):
        if self._alias is None:
            return param
        if param in self._alias:
            return self._alias[param]
        elif param in self._masked:
            raise KeyError("no argument with name {0}".format(param))
        else:
            return param
    def _apply_unalias_dict(self, params):
        if self._alias is None:
            return params
        alias=self._alias
        masked=self._masked
        unalias_params={}
        for k,v in viewitems(params):
            if k in alias:
                unalias_params[alias[k]]=v
            elif k in masked:
                raise KeyError("no argument with name {0}".format(k))
            else:
                unalias_params[k]=v
        return unalias_params
        
    def has_arg(self, arg_name):
        if self._use_keywords:
            return True # assume that any parameter works
        arg_name=self._apply_unalias(arg_name)
        return arg_name in self._declared_args
    def get_mandatory_args(self):
        return self._mand_args_alias
    def get_arg_default(self, arg_name):
        arg_name=self._apply_unalias(arg_name)
        if arg_name in self._defaults:
            return self._defaults[arg_name]
        if arg_name in self._mand_args:
            raise ValueError("argument {0} has no default value".format(arg_name))
        else:
            raise KeyError("no argument with name {0}".format(arg_name))
    def __call__(self, **params):
        for n in self._mand_args:
            if not n in params:
                raise TypeError("mandatory parameter not supplied: {0}".format(n))
        named_params=self._defaults.copy()
        named_params.update(self._apply_unalias_dict(params))
        named_params=self.filter_args_dict(named_params)
        return self._func(**named_params)
    
    class NamesBoundCall(object):
        def __init__(self, func, names, bound_params):
            object.__init__(self)
            for n in func._mand_args:
                if not (n in bound_params or n in names):
                    raise TypeError("mandatory parameter not supplied: {0}".format(n))
            self._func=func._func
            self._names_dest=[]
            for n in names:
                un=func._apply_unalias(n)
                if func.has_arg(n):
                    dest=("named",un)
                else:
                    dest=("unused",)
                self._names_dest.append(dest)
            self._named_params=func._defaults.copy()
            self._named_params.update(func._apply_unalias_dict(bound_params))
        def __call__(self, *params):
            n_par=self._named_params
            for p,d in zip(params,self._names_dest):
                if d[0]=='named':
                    n_par[d[1]]=p
            return self._func(**n_par)
                    




class MethodCallable(FunctionCallable):
    """
    Similar to :class:`FunctionCallable`, but accepts class method instead of a function.
    
    The only addition is that now object's attributes can also parameters to the function:
    all the parameters which are not explicitly mentioned in the method signature are assumed to be object's attributes.
    
    The parameters are affected by alias, but NOT affected by defaults 
    (since it's impossible to ensure that all object's attributes are kept constant,
    and it's impractical to reset them all to default values at every function call).
    
    Args:
        method: Method to be wrapped.
        function_signature: A :class:`~.FunctionSignature` object supplying information
            about function's argument names and default values, if they're different from what's extracted from its signature.
            If it's assumed that the first self argument is already excluded.
        defaults (dict): A dictionary ``{name: value}`` of additional default parameters values. Override the defaults from the signature.
            All default values must be pass-able to the function as a parameter
        alias (dict): A dictionary ``{alias: original}`` for renaming some of the original arguments.
            Original argument names can't be used if aliased (though, multi-aliasing can be used explicitly, e.g., ``alias={'alias':'arg','arg':'arg'}``).
            A name can be blocked (its usage causes error) if it's aliased to None (``alias={'blocked_name':None}``).
            
    This callable is implemented largely to be used with ``TheoryCalculator`` class (currently deprecated).
    """
    def __init__(self, method, function_signature=None, defaults=None, alias=None):
        if method.__self__ is None:
            raise ValueError("supplied method is unbound; use FunctionCallable instead")
        if function_signature is None:
            function_signature=function_utils.FunctionSignature.from_function(method)
        del function_signature.arg_names[0] # remove self
        FunctionCallable.__init__(self,method,function_signature,defaults,alias)
        self._obj=function_signature.obj
    def has_arg(self, arg_name):
        if self._use_keywords:
            return True # assume that any parameter works
        arg_name=self._apply_unalias(arg_name)
        return (arg_name in self._declared_args) or (hasattr(self._obj,arg_name))
    def get_arg_default(self, arg_name):
        arg_name=self._apply_unalias(arg_name)
        if arg_name in self._defaults:
            return self._defaults[arg_name]
        if hasattr(self._obj,arg_name):
            return getattr(self._obj,arg_name)
        if arg_name in self._mand_args:
            raise ValueError("argument {0} has no default value".format(arg_name))
        else:
            raise KeyError("no argument with name {0}".format(arg_name))
    def _is_func_arg(self, arg_name): # arg_name is assumed to be un-aliased
        return arg_name in self._declared_args
    def __call__(self, **params):
        for n in self._mand_args:
            if not n in params:
                raise TypeError("mandatory parameter not supplied: {0}".format(n))
        named_params=self._defaults.copy()
        named_params.update(self._apply_unalias_dict(params))
        for n in list(named_params):
            if not self._is_func_arg(n):
                if hasattr(self._obj,n):
                    setattr(self._obj,n,named_params.pop(n))
                elif not self._use_keywords:
                    named_params.pop(n)
        return self._func(**named_params)
    
    class NamesBoundCall(object):
        def __init__(self, func, names, bound_params):
            object.__init__(self)
            for n in func._mand_args:
                if not (n in bound_params or n in names):
                    raise TypeError("mandatory parameter not supplied: {0}".format(n))
            self._func=func._func
            self._obj=func._obj
            self._names_dest=[]
            for n in names:
                un=func._apply_unalias(n)
                if func._is_func_arg(un):
                    dest=('named',un)
                elif hasattr(func._obj,un):
                    dest=('attr',un)
                else:
                    dest=('unused',)
                self._names_dest.append(dest)
            named_params=func._defaults.copy()
            named_params.update(func._apply_unalias_dict(bound_params))
            self._object_params=[]
            self._named_params={}
            for n,p in viewitems(named_params):
                if func._is_func_arg(n):
                    self._named_params[n]=p
                elif hasattr(func._obj,n):
                    self._object_params.append((n,p))
        def __call__(self, *params):
            obj=self._obj
            for n,p in self._object_params:
                setattr(obj,n,p)
            n_par=self._named_params
            for p,d in zip(params,self._names_dest):
                if d[0]=='named':
                    n_par[d[1]]=p
                elif d[0]=='attr':
                    setattr(obj,d[1],p)
            return self._func(**n_par)
        
def to_callable(func):
    """
    Convert a function to an :class:`ICallable` instance.
    
    If it's already :class:`ICallable`, return unchanged.
    Otherwise, return :class:`FunctionCallable` or :class:`MethodCallable` depending on whether it's a function or a bound method.
    """
    if isinstance(func, ICallable):
        return func
    else:
        if getattr(func,"__self__",None) is None:
            return FunctionCallable(func)
        else:
            return MethodCallable(func)