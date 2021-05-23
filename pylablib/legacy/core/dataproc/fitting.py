"""
Universal function fitting interface.
"""

from __future__ import division
from ..utils.py3 import textstring

from ..utils import general as general_utils #@UnresolvedImport
from ..utils import funcargparse #@UnresolvedImport
from ..dataproc import callable #@UnresolvedImport
import numpy as np
import scipy.optimize


class Fitter(object):
    """
    Fitter object.
    
    Can handle variety of different functions, complex arguments or return values, array arguments.
    
    Args:
        func(callable): Fit function. Can be anything callable (function, method, object with ``__call__`` method, etc.).
        xarg_name(str or list): Name (or multiple names) for x arguments. These arguments are passed to `func` (as named arguments) when calling for fitting.
            Can be a string (single argument) or a list (arbitrary number of arguments, including zero).
        fit_parameters (dict): Dictionary ``{name: value}`` of parameters to be fitted (`value` is the starting value for the fitting procedure).
            If `value` is ``None``, try and get the default value from the `func`.
        fixed_parameters (dict): Dictionary ``{name: value}`` of parameters to be fixed during the fitting procedure.
            If `value` is ``None``, try and get the default value from the `func`.
        scale (dict): Defines typical scale of fit parameters (used to normalize fit parameters supplied of :func:`scipy.optimize.least_squares`).
                Note: for complex parameters scale must also be a complex number, with re and im parts of the scale variable corresponding to the scale of the re and im part.
        limits (dict): Boundaries for the fit parameters (missing entries are assumed to be unbound). Each boundary parameter is a tuple ``(lower, upper)``.
            ``lower`` or ``upper`` can be ``None``, ``numpy.nan`` or ``numpy.inf`` (with the appropriate sign), which implies no bounds in the given direction.
            Note: for compound data types (such as lists) the entries are still tuples of 2 elements,
            each of which is either ``None`` (no bound for any sub-element) or has the same structure as the full parameter.
            Note: for complex parameters limits must also be complex numbers (or ``None``), with re and im parts of the limits variable corresponding to the limits of the re and im part.
    """
    def __init__(self, func, xarg_name=None, fit_parameters=None, fixed_parameters=None, scale=None, limits=None):
        object.__init__(self)
        self.func=callable.to_callable(func)
        self.set_xarg_name(xarg_name or [])
        self.set_fixed_parameters(fixed_parameters)
        self.set_fit_parameters(fit_parameters)
        self._default_scale=scale
        self._default_limits=limits

    def _prepare_parameters(self, fit_parameters):
        """Normalize fit_parameters"""
        fit_parameters=general_utils.to_pairs_list(fit_parameters)
        parameters={}
        for name,val in fit_parameters:
            if isinstance(val,textstring) and val=="complex":
                val=complex(self.func.get_arg_default(name))
            elif val is None:
                val=self.func.get_arg_default(name)
            parameters[name]=val
        return parameters
    @staticmethod
    def _pack_parameters(value):
        """Pack parameters into an array of floats"""
        if funcargparse.is_sequence(value,"array"):
            return [p for v in value for p in Fitter._pack_parameters(v)]
        if np.iscomplexobj(value):
            return [np.real(value),np.imag(value)]
        try:
            return value.as_float_array() # function is assumed to take no arguments and return a float array
        except AttributeError:
            return [value]
    @staticmethod
    def _build_unpacker_single(packed, template):
        """
        Build a function that unpacks and array of floats into a parameters array.

        Return 2 values: function and the number of consumed array elements.
        """
        if funcargparse.is_sequence(template,"array"):
            ufs=[]
            uns=[]
            n=0
            for pv in template:
                uf,un=Fitter._build_unpacker_single(packed[n:],pv)
                ufs.append(uf)
                uns.append(n)
                n+=un
            def unpack(p):
                return [uf(p[un:]) for uf,un in zip(ufs,uns)]
            return unpack,n
        if np.iscomplexobj(template):
            return (lambda p: p[0]+1j*p[1]), 2
        try:
            v,n=template.from_float_array(packed) # function is assumed to take 1 argument (float array) and return 2 values: the unpacked element and the number of consumed floats
            return (lambda p: template.from_float_array(p)[0]),n
        except AttributeError:
            return (lambda p: p[0]), 1
    @staticmethod
    def _build_unpacker(template):
        """Build a function that unpacks an array of floats into a parameters array given the template"""
        packed=Fitter._pack_parameters(template)
        unpacker,n=Fitter._build_unpacker_single(packed,template)
        if n!=len(packed):
            raise RuntimeError("part of the array hasn't been unpacked: processed {} out of {} elements".format(n,len(packed)))
        return unpacker
    
    def set_xarg_name(self, xarg_name):
        """
        Set names of x arguments.
        
        Can be a string (single argument) or a list (arbitrary number of arguments, including zero).
        """
        if isinstance(xarg_name,list) or isinstance(xarg_name,tuple):
            self.xarg_name=xarg_name
            self.single_xarg=False
        else:
            self.xarg_name=[xarg_name]
            self.single_xarg=True
    def use_xarg(self):
        """Return ``True`` if the function requires x arguments."""
        return len(self.xarg_name)>0
    def set_fixed_parameters(self, fixed_parameters):
        """Change fixed parameters."""
        self.fixed_parameters=dict(fixed_parameters or {})
    def update_fixed_parameters(self, fixed_parameters):
        """Update the dictionary of fixed parameters."""
        self.fixed_parameters.update(fixed_parameters)
    def del_fixed_parameters(self, fixed_parameters):
        """Remove fixed parameters."""
        for name in fixed_parameters:
            self.fixed_parameters.pop(name,None)
    def set_fit_parameters(self, fit_parameters):
        """Change fit parameters."""
        self.fit_parameters=self._prepare_parameters(fit_parameters)
    def update_fit_parameters(self, fit_parameters):
        """Update the dictionary of fit parameters."""
        fit_parameters=self._prepare_parameters(fit_parameters)
        self.fit_parameters.update(fit_parameters)
    def del_fit_parameters(self, fit_parameters):
        """Remove fit parameters."""
        for name in fit_parameters:
            self.fit_parameters.pop(name,None)
            
    def _get_unaccounted_parameters(self, fixed_parameters, fit_parameters):
        supplied_names=set(self.xarg_name)|set(fixed_parameters)|set(fit_parameters)
        unaccounted_names=set.difference(self.func.get_mandatory_args(),supplied_names)
        return unaccounted_names
    
    def fit(self, x=None, y=0, fit_parameters=None, fixed_parameters=None, scale="default", limits="default", weight=1., parscore=None, return_stderr=False, return_residual=False, **kwargs):
        """
        Fit the data.
        
        Args:
            x: x arguments. If the function has single x argument, `x` is an array-like object;
                otherwise, `x` is a list of array-like objects (can be ``None`` if there are no x parameters).
            y: Target function values.
            fit_parameters (dict): Adds to the default `fit_parameters` of the fitter (has priority on duplicate entries).
            fixed_parameters (dict): Adds to the default `fixed_parameters` of the fitter (has priority on duplicate entries).
            scale (dict): Defines typical scale of fit parameters (used to normalize fit parameters supplied of :func:`scipy.optimize.least_squares`).
                Note: for complex parameters scale must also be a complex number, with re and im parts of the scale variable corresponding to the scale of the re and im part.
                If value is ``"default"``, use the value supplied on the fitter creation.
            limits (dict): Boundaries for the fit parameters (missing entries are assumed to be unbound). Each boundary parameter is a tuple ``(lower, upper)``.
                ``lower`` or ``upper`` can be ``None``, ``numpy.nan`` or ``numpy.inf`` (with the appropriate sign), which implies no bounds in the given direction.
                Note: for compound data types (such as lists) the entries are still tuples of 2 elements,
                each of which is either ``None`` (no bound for any sub-element) or has the same structure as the full parameter.
                Note: for complex parameters limits must also be complex numbers (or ``None``), with re and im parts of the limits variable corresponding to the limits of the re and im part.
                If value is ``"default"``, use the value supplied on the fitter creation.
            weight (list or numpy.ndarray): Determines the weights of y-points.
                Can be either an array broadcastable to `y` (e.g., a scalar or an array with the same shape as `y`),
                in which case it's interpreted as list of individual point weights (which multiply residuals before they are squared).
                Or it can be an array with number of elements which is square of the number of elements in `y`,
                in which case it's interpreted as a weight matrix (which matrix-multiplies residuals before they are squared).
            parscore(callable): parameter score function, whose value is added to the mean-square error (sum of all residuals squared) after applying weights.
                Takes the same parameters as the fit function, only without the x-arguments, and return an array-like value. Can be used for, e.g., 'soft' fit parameter constraining.
            return_stderr (bool): If ``True``, append `stderr` to the output.
            return_residual: If not ``False``, append `residual` to the output.
            **kwargs: arguments passed to :func:`scipy.optimize.least_squares` function.
        
        Returns:
            tuple: ``(params, bound_func[, stderr][, residual])``:
                - `params`: a dictionary ``{name: value}`` of the parameters supplied to the function (both fit and fixed).
                - `bound_func`: the fit function with all the parameters bound (i.e., it only requires x parameters).
                - `stderr`: a dictionary ``{name: error}`` of standard deviation for fit parameters to the return parameters.
                    If the fitting routine returns no residuals (usually for a bad or an underconstrained fit), all residuals are set to NaN.
                - `residual`: either a full array of residuals ``func(x,**params)-y`` (if ``return_residual=='full'``),
                    a mean magnitude of the residuals ``mean(abs(func(x,**params)-y)**2)`` (if ``return_residual==True`` or ``return_residual=='mean'``),
                    or the total residuals including weights ``mean(abs((func(x,**params)-y)*weight)**2)`` (if ``return_residual=='weighted'``).
        """
        # Applying order: self.fixed_parameters < self.fit_parameters < fixed_parameters < fit_parameters
        fit_parameters=self._prepare_parameters(fit_parameters)
        filtered_fit_paremeters=general_utils.filter_dict(fixed_parameters,self.fit_parameters,exclude=True) # to ensure self.fit_parameters < fixed_parameters
        fit_parameters=general_utils.merge_dicts(filtered_fit_paremeters,fit_parameters)
        fixed_parameters=general_utils.merge_dicts(self.fixed_parameters,fixed_parameters)
        if scale=="default":
            scale=self._default_scale
        if limits=="default":
            limits=self._default_limits
        unaccounted_parameters=self._get_unaccounted_parameters(fixed_parameters,fit_parameters)
        if len(unaccounted_parameters)>0:
            raise ValueError("Some of the function parameters are not supplied: {0}".format(unaccounted_parameters))
        x=x if x is not None else []
        if self.single_xarg:
            x=[np.asarray(x)]
        else:
            x=[np.asarray(e) for e in x]
        y=np.asarray(y)
        weight=np.asarray(weight)
        wkind=None
        try:
            if y.shape==(y*weight).shape:
                wkind="point"
        except ValueError:
            pass
        if wkind is None:
            if np.prod(weight.shape)==np.prod(y.shape)**2:
                wkind="matrix"
                wmat_dim=np.prod(y.shape)
                wmat=weight.reshape((wmat_dim,wmat_dim))
            else:
                raise ValueError("weight shape {} is incompatible with y shape {}".format(weight.shape,y.shape))
        p_names=list(fit_parameters.keys())
        bound_func=self.func.bind_namelist(self.xarg_name+p_names,**fixed_parameters)
        props=[fit_parameters[name] for name in p_names]
        init_p=self._pack_parameters(props)
        unpacker=self._build_unpacker(props)
        if scale: # setup scale-related parameters
            scale_default=dict(zip(p_names,unpacker([np.nan]*len(init_p))))
            scale_default.update(scale)
            p_scale=self._pack_parameters([scale_default[name] for name in p_names])
            if len(p_scale)!=len(init_p):
                raise ValueError("inconsistent shapes of fit parameters and scale argument")
            x_scale=np.array([1. if np.isnan(sc) else abs(float(sc)) for sc in p_scale])
            offset_p=init_p-x_scale
            init_p=np.ones(len(init_p))
        else:
            x_scale=1
            offset_p=0
        if limits: # setup bounds
            p_bounds=[]
            for (idx,default) in [(0,-np.inf),(1,+np.inf)]:
                ibounds=dict([ (n,limits[n][idx]) for n in limits if limits[n][idx] is not None])
                ibounds_default=dict(zip(p_names,unpacker([default]*len(init_p))))
                ibounds_default.update(ibounds)
                p_ibounds=self._pack_parameters([ibounds_default[name] for name in p_names])
                if len(p_ibounds)!=len(init_p):
                    raise ValueError("inconsistent shapes of fit parameters and {} bounds argument".format("lower" if idx==0 else "upper"))
                p_ibounds=[default if (b is None or np.isnan(b)) else b for b in p_ibounds]
                p_ibounds=(np.array(p_ibounds)-offset_p)/x_scale
                p_bounds.append(p_ibounds)
            kwargs.setdefault("bounds",p_bounds)
        if parscore:
            parscore=callable.to_callable(parscore)
        def calc_residuals(raw_res):
            if wkind=="point":
                return (np.asarray(raw_res)*weight).flatten()
            elif wkind=="matrix":
                y_diff_uw=np.asarray(raw_res).flatten()
                return np.dot(wmat,y_diff_uw)
        def fit_func(fit_p):
            fit_p=fit_p*x_scale+offset_p
            up=x+unpacker(fit_p)
            y_diff=calc_residuals(y-np.asarray(bound_func(*up)))
            if np.iscomplexobj(y_diff):
                y_diff=np.concatenate((y_diff.real,y_diff.imag))
            if parscore:
                fitpar=dict(zip(p_names,up[len(x):]))
                score=parscore(**fitpar)
                y_diff=np.append(y_diff,score)
            return y_diff
        lsqres=scipy.optimize.least_squares(fit_func,init_p,**kwargs)
        res,jac,tot_err=lsqres.x,lsqres.jac,lsqres.fun
        res=res*x_scale+offset_p
        try:
            cov=np.linalg.inv(np.dot(jac.transpose(),jac))*(np.sum(tot_err**2)/(len(tot_err)-len(res)))
        except np.linalg.LinAlgError: # singular matrix
            cov=None
        res=unpacker(res)
        fit_dict=dict(zip(p_names,res))
        params_dict=fixed_parameters.copy()
        params_dict.update(fit_dict)
        bound_func=self.func.bind(self.xarg_name,**params_dict)
        if cov is None: # singular or close to singular covariance matrix; usually means either degenerate fit parameters, or vastly (~1E8) different error scales
            stderr=dict(zip(p_names,unpacker([np.nan]*len(init_p))))
        else:
            stderr=unpacker(np.diag(cov)**0.5*x_scale)
            stderr=dict(zip(p_names,stderr))
        return_val=params_dict,bound_func
        if return_stderr:
            return_val=return_val+(stderr,)
        if return_residual:
            if return_residual=="full":
                residual=y-bound_func(*x)
            elif return_residual=="weighted":
                residual_w=calc_residuals(y-np.asarray(bound_func(*x)))
                residual=(abs(residual_w)**2).sum()
            else:
                residual=(abs(y-bound_func(*x))**2).mean()
            return_val=return_val+(residual,)
        return return_val
    def initial_guess(self, fit_parameters=None, fixed_parameters=None, return_stderr=False, return_residual=False):
        """
        Return the initial guess for the fitting.
        
        Args:
            fit_parameters (dict): Overrides the default `fit_parameters` of the fitter.
            fixed_parameters (dict): Overrides the default `fixed_parameters` of the fitter.
            return_stderr (bool): If ``True``, append `stderr` to the output.
            return_residual: If not ``False``, append `residual` to the output.
        
        Returns:
            tuple: ``(params, bound_func)``.
            
                - `params`: a dictionary ``{name: value}`` of the parameters supplied to the function (both fit and fixed).
                - `bound_func`: the fit function with all the parameters bound (i.e., it only requires x parameters).
                - `stderr`: a dictionary ``{name: error}`` of standard deviation for fit parameters to the return parameters.
                    Always zero, added for better compatibility with :meth:`fit`.
                - `residual`: either a full array of residuals ``func(x,**params)-y`` (if ``return_residual=='full'``) or
                    a mean magnitude of the residuals ``mean(abs(func(x,**params)-y)**2)`` (if ``return_residual==True`` or ``return_residual=='mean'``).
                    Always zero, added for better compatibility with :meth:`fit`.
        """
        fit_parameters=self._prepare_parameters(fit_parameters)
        params_dict=general_utils.merge_dicts(self.fit_parameters,fit_parameters,self.fixed_parameters,fixed_parameters)
        bound_func=self.func.bind_namelist(self.xarg_name,**params_dict)
        return_val=params_dict,bound_func
        if return_stderr:
            p_names=list(params_dict.keys())
            props=[params_dict[name] for name in p_names]
            init_p=self._pack_parameters(props)
            unpacker=self._build_unpacker(props)
            stderr=dict(zip(p_names,unpacker([0]*len(init_p))))
            return_val=return_val+(stderr,)
        if return_residual:
            return_val=return_val+(0,)
        return return_val
    
def huge_error(x, factor=100.):
    if np.iscomplex(x):
        return (1+1j)*factor*abs(x)
    else:
        return abs(x)*factor
    
def get_best_fit(x, y, fits):
    """
    Select the best (lowest residual) fit result.
    
    `x` and `y` are the argument and the value of the bound fit function. `fits` is the list of fit results (tuples returned by :meth:`Fitter.fit`).
    """
    errors=[(abs(y-f[1](x))**2).mean() for f in fits]
    min_error_idx=np.argmin(errors)
    return fits[min_error_idx]