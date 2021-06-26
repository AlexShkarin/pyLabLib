"""
Routines for filtering arrays (mostly 1D data).
"""


from . import fourier
from .table_wrap import wrap
from ..utils import funcargparse
from . import utils, specfunc, iir_transform

import numpy as np
import scipy.ndimage as ndimage




##### Convolution filters #####

def convolve1d(trace, kernel, mode="reflect", cval=0.):
    """
    Convolution filter.
    
    Convolves `trace` with the given `kernel` (1D array). `mode` and `cval` determine how the endpoints are handled.
    Simply a wrapper around the standard :func:`scipy.ndimage.convolve1d` that handles complex arguments.
    """
    wrapped=wrap(trace)
    trace=np.asarray(trace)
    kernel=np.asarray(kernel)
    wf_complex=np.iscomplexobj(trace) or np.iscomplexobj(cval)
    kernel_complex=np.iscomplexobj(kernel)
    if wf_complex and kernel_complex:
        cval=complex(cval)
        real_part=ndimage.convolve1d(trace.real,kernel.real,mode=mode,cval=cval.real)-ndimage.convolve1d(trace.imag,kernel.imag,mode=mode,cval=cval.imag)
        imag_part=ndimage.convolve1d(trace.real,kernel.imag,mode=mode,cval=cval.real)+ndimage.convolve1d(trace.imag,kernel.real,mode=mode,cval=cval.imag)
        res=real_part+1j*imag_part
    elif wf_complex:
        cval=complex(cval)
        res=ndimage.convolve1d(trace.real,kernel,mode=mode,cval=cval.real)+1j*ndimage.convolve1d(trace.imag,kernel,mode=mode,cval=cval.imag)
    elif kernel_complex:
        trace=trace.astype(np.find_common_type([trace.dtype,float],[]))
        res=ndimage.convolve1d(trace,kernel.real,mode=mode,cval=cval)+1j*ndimage.convolve1d(trace,kernel.imag,mode=mode,cval=cval)
    else:
        trace=trace.astype(np.find_common_type([trace.dtype,kernel.dtype],[]))
        res=ndimage.convolve1d(trace,kernel,mode=mode,cval=cval)
    return wrapped.array_replaced(res,preserve_index=True)
        
def convolution_filter(a, width, kernel="gaussian", kernel_span="auto", mode="reflect", cval=0., kernel_height=None):
    """
    Convolution filter.
    
    Args:
        a: array for filtering.
        width (float): kernel width (second parameter to the kernel function).
        kernel: either a string defining the kernel function (see :func:`.specfunc.get_kernel_func` for possible kernels),
            or a function taking 3 arguments ``(pos, width, height)``, where `height` can be ``None`` (assumes normalization by area). 
        kernel_span: the cutoff for the kernel function. Either an integer (number of points)
            or ``'auto'`` (autodetect for ``"gaussian"``, ``"rectangle"`` and ``"exp_decay"``, full trace width for all other kernels).
        mode (str): convolution mode (see :func:`scipy.ndimage.convolve`).
        cval (float): convolution fill value (see :func:`scipy.ndimage.convolve`).
        kernel_height: height parameter to be passed to the kernel function. ``None`` means normalization by area.
    """
    wrapped=wrap(a)
    if wrapped.ndim()==2:
        return wrapped.columns_replaced([convolution_filter(wrapped.c[i],width=width,kernel=kernel,kernel_span=kernel_span,mode=mode,cval=cval,kernel_height=kernel_height)
            for i in range(wrapped.shape()[1])])
    elif wrapped.ndim()!=1:
        raise ValueError("this function accepts only 1D or 2D arrays")
    a=np.asarray(a)
    if kernel=="rectangle":
        width=int(np.ceil(width))
        kernel_wf=np.ones(width)*(kernel_height or 1)
    else:
        if kernel_span=="auto":
            if kernel=="gaussian":
                kernel_span=int(np.ceil(width*6))
            elif kernel=="exp_decay":
                kernel_span=int(np.ceil(width*18)) #accuracy of 10^(-6)
            else:
                kernel_span=len(a)
        if kernel_span>len(a):
            kernel_span=len(a)
        kernel=specfunc.get_kernel_func(kernel)
        kernel_wf=kernel(np.arange(-kernel_span,kernel_span+1.),width,kernel_height) # pylint: disable=invalid-unary-operand-type
    if kernel_height is None:
        kernel_wf=kernel_wf/kernel_wf.sum() #normalize kernel; non-normalized kernel might be useful e.g. for low-pass filtering when width is close len(a)
    return wrapped.array_replaced(convolve1d(a,kernel_wf,mode=mode,cval=cval),preserve_index=True)

def gaussian_filter(a, width, mode="reflect", cval=0.):
    """
    Simple gaussian filter. Can handle complex data.
    
    Equivalent to a convolution with a gaussian. Equivalent to :func:`scipy.ndimage.gaussian_filter1d`, uses :func:`convolution_filter`.
    """
    return convolution_filter(a,width,kernel="gaussian",mode=mode,cval=cval)

def gaussian_filter_nd(a, width, mode="reflect", cval=0.):
    """
    Simple gaussian filter. Can't handle complex data.
    
    Equivalent to a convolution with a gaussian. Wrapper around :func:`scipy.ndimage.gaussian_filter`. 
    """
    aa=np.asarray(a,dtype=float)
    if aa.ndim==1:
        res=ndimage.gaussian_filter(aa,width,mode=mode,cval=cval)
        return wrap(a).array_replaced(res,preserve_index=True)
    else:
        res=[ndimage.gaussian_filter(aa[:,c],width,mode=mode,cval=cval) for c in range(aa.shape[1])]
        return wrap(a).columns_replaced(res,preserve_index=True)




##### IIR filters #####

def low_pass_filter(trace, t, mode="reflect", cval=0.):
    """
    Simple single-pole low-pass filter.
    
    `t` is the filter time constant, `mode` and `cval` are the trace expansion parameters (only from the left).
    Implemented as a recursive digital filter, so its performance doesn't depend strongly on `t`.
    Works only for 1D arrays.
    """
    expand_size=min(int(np.ceil(t*20)),len(trace))
    wrapped=wrap(trace)
    trace=utils.pad_trace(np.asarray(trace),pad=(expand_size,0),mode=mode,cval=cval)
    beta=np.exp(np.double(-1.)/np.double(t))
    alpha=np.double(1.)-beta
    trace=iir_transform.iir_apply_complex(trace,np.array([alpha]),np.array([beta]))
    return wrapped.array_replaced(trace[expand_size:],preserve_index=True)
    
def high_pass_filter(trace, t, mode="reflect", cval=0.):
    """
    Simple single-pole high-pass filter (equivalent to subtracting a low-pass filter).
    
    `t` is the filter time constant, `mode` and `cval` are the trace expansion parameters (only from the left).
    Implemented as a recursive digital filter, so its performance doesn't depend strongly on `t`.
    Works only for 1D arrays.
    """
    atrace=np.asarray(trace)
    return wrap(trace).array_replaced(atrace-low_pass_filter(atrace,t,mode,cval),preserve_index=True)
def integrate(trace):
    """
    Calculate the integral of the trace.
    
    Alias for :func:`numpy.cumsum`.
    """
    return np.cumsum(trace,axis=0)
def differentiate(trace):
    """
    Calculate the differential of the trace.
    
    Note that since the data dimensions are changed (length is reduced by 1), the index is not preserved for pandas DataFrames.
    """
    wrapped=wrap(trace)
    trace=np.asarray(trace)
    return wrapped.array_replaced(trace[1:]-trace[:-1])




##### Sliding filters #####

def sliding_average(a, width, mode="reflect", cval=0.):
    """
    Simple sliding average filter
    
    Equivalent to convolution with a rectangle peak function.
    """
    return convolution_filter(a,width,kernel="rectangle",mode=mode,cval=cval)

def median_filter(a, width, mode="reflect", cval=0.):
    """
    Median filter.
    
    Wrapper around :func:`scipy.ndimage.median_filter`.
    """
    if wrap(a).ndim()==2:
        width=(width,1)
    res=ndimage.median_filter(a,width,mode=mode,cval=cval)
    return wrap(a).array_replaced(res,preserve_index=True)


def _sliding_func(trace, filtering_function, width, mode="reflect", cval=0.):
    """
    Perform a sliding filtering of a 1D trace with the given `filtering_function`.
    
    mode ('drop' or 'leave') determines whether to drop the last bin if it's not full
    Works only with arrays (no columns or tables).
    """
    wrapped=wrap(trace)
    if wrapped.ndim()==2:
        return wrapped.columns_replaced([_sliding_func(wrapped.c[i],filtering_function=filtering_function,width=width,mode=mode,cval=cval)
            for i in range(wrapped.shape()[1])])
    elif wrapped.ndim()!=1:
        raise ValueError("this function accepts only 1D or 2D arrays")
    if width is None or width<=1:
        return trace
    l=len(trace)
    width=(int(width)//2)*2+1
    trace=utils.pad_trace(np.asarray(trace),pad=width//2,mode=mode,cval=cval)
    return np.array([filtering_function(trace[i-width//2:i+width//2+1]) for i in range(width//2,l+width//2)])

def sliding_filter(trace, n, dec="bin", mode="reflect", cval=0.):
    """
    Perform sliding filtering on the data.
    
    Args:
        trace: 1D array-like object.
        n (int): bin width.
        dec (str): decimation method. Can be
                - ``'bin'`` or ``'mean'`` - do a binning average;
                - ``'sum'`` - sum points;
                - ``'min'`` - leave min point;
                - ``'max'`` - leave max point;
                - ``'median'`` - leave median point (works as a median filter).
                - a function which takes a single 1D array and compresses it into a number
        mode (str): Expansion mode. Can be ``'constant'`` (added values are determined by `cval`), ``'nearest'`` (added values are end values of the trace),
            ``'reflect'`` (reflect trace with respect to its endpoint) or ``'wrap'`` (wrap the values from the other size).
        cval (float): If ``mode=='constant'``, determines the expanded values.
    """
    wrapped=wrap(trace)
    trace=np.asarray(trace)
    if dec=="bin" or dec=="mean":
        res=_sliding_func(trace,np.mean,n,mode=mode,cval=cval)
    elif dec=="sum":
        res=_sliding_func(trace,np.sum,n,mode=mode,cval=cval)
    elif dec=="min":
        res=_sliding_func(trace,np.min,n,mode=mode,cval=cval)
    elif dec=="max":
        res=_sliding_func(trace,np.max,n,mode=mode,cval=cval)
    elif dec=="median":
        res=_sliding_func(trace,np.median,n,mode=mode,cval=cval)
    elif hasattr(dec,"__call__"):
        res=_sliding_func(trace,dec,n,mode=mode,cval=cval)
    else:
        raise ValueError("unrecognized decimation method: {0}".format(dec))
    return wrapped.array_replaced(res,preserve_index=True)




##### Decimation filters #####

def _decimation_filter(a, decimation_function, width, axis=0, mode="drop"):
    """
    Perform a decimation filtering with the given `decimation_function`.
    
    mode ('drop' or 'leave') determines whether to drop the last bin if it's not full
    Works only with arrays (no columns or tables).
    """
    if width is None or width<=1:
        return a
    if not mode in ["drop", "leave"]:
        raise ValueError("unrecognized binning mode: "+mode)
    width=int(width)
    shape=np.shape(a)
    if axis<0:
        axis=max(axis+len(shape),0)
    actual_len=shape[axis]
    dec_len=int(actual_len/width)*width
    if mode=="drop":
        cropped_slices=[slice(s) for s in shape]
        cropped_slices[axis]=slice(dec_len)
        dec_shape=shape[:axis]+(-1,width)+shape[axis+1:]
        return decimation_function(np.reshape(a[tuple(cropped_slices)],dec_shape),axis+1)
    elif mode=="leave":
        dec_wf=_decimation_filter(a,decimation_function,width,axis=axis,mode="drop")
        if dec_len==actual_len:
            return dec_wf
        rest_indices=np.arange(dec_len,actual_len)
        dec_rest=decimation_function(np.take(a,rest_indices,axis=axis),axis=axis)
        return np.append(dec_wf,dec_rest,axis=axis)
        

def decimate(a, n, dec="skip", axis=0, mode="drop"):
    """
    Decimate the data.
    
    Note that since the data dimensions are changed, the index is not preserved for pandas DataFrames.

    Args:
        a: data array.
        n (int): decimation factor.
        dec (str): decimation method. Can be
                - ``'skip'`` - just leave every n'th point while completely omitting everything else;
                - ``'bin'`` or ``'mean'`` - do a binning average;
                - ``'sum'`` - sum points;
                - ``'min'`` - leave min point;
                - ``'max'`` - leave max point;
                - ``'median'`` - leave median point (works as a median filter).
                - a function which takes two arguments (nD numpy array and an axis) and compresses the array along the given axis
        axis (int): axis along which to perform the decimation; can also be a tuple, in which case the same decimation is performed sequentially along several axes.
        mode (str): determines what to do with the last bin if it's incomplete. Can be either ``'drop'`` (omit the last bin) or ``'leave'`` (keep it).
    """
    if isinstance(axis,tuple):
        result=a
        for ax in axis:
            result=decimate(result,n=n,dec=dec,axis=ax,mode=mode)
        return result
    a,wf_orig=np.asarray(a),a
    wrapped=wrap(wf_orig) if a.ndim<3 else None
    if dec=="bin" or dec=="mean":
        res=_decimation_filter(a,np.mean,n,axis=axis,mode=mode)
    elif dec=="sum":
        res=_decimation_filter(a,np.sum,n,axis=axis,mode=mode)
    elif dec=="min":
        res=_decimation_filter(a,np.min,n,axis=axis,mode=mode)
    elif dec=="max":
        res=_decimation_filter(a,np.max,n,axis=axis,mode=mode)
    elif dec=="median":
        res=_decimation_filter(a,np.median,n,axis=axis,mode=mode)
    elif dec=="skip":
        def _dec_fun(a, axis):
            slices=[slice(s) for s in np.shape(a)]
            slices[axis]=0
            return a[tuple(slices)]
        res=_decimation_filter(a,_dec_fun,n,axis=axis,mode=mode)
    elif hasattr(dec,"__call__"):
        res=_decimation_filter(a,dec,n,axis=axis,mode=mode)
    else:
        raise ValueError("unrecognized decimation function: {0}".format(dec))
    return wrapped.array_replaced(res) if res.ndim<3 else res

def binning_average(a, width, axis=0, mode="drop"):
    """
    Binning average filter.
    
    Equivalent to :func:`decimate` with ``dec=='bin'``.
    """
    return decimate(a,width,"bin",axis=axis,mode=mode)

def decimate_full(a, dec="skip", axis=0):
    """
    Completely decimate the data along a given axis.
    
    Args:
        a: data array.
        dec (str): decimation method. Can be
                - ``'skip'`` - just leave every n'th point while completely omitting everything else;
                - ``'bin'`` or ``'mean'`` - do a binning average;
                - ``'sum'`` - sum points;
                - ``'min'`` - leave min point;
                - ``'max'`` - leave max point;
                - ``'median'`` - leave median point (works as a median filter).
                - a function which takes two arguments (nD numpy array and an axis) and compresses the array along the given axis
        axis (int): axis along which to perform the decimation; can also be a tuple, in which case the same decimation is performed along several axes.
    """
    a=np.asarray(a)
    if dec=="bin" or dec=="mean":
        return np.mean(a,axis=axis)
    elif dec=="sum":
        return np.sum(a,axis=axis)
    elif dec=="min":
        return np.min(a,axis=axis)
    elif dec=="max":
        return np.max(a,axis=axis)
    elif dec=="median":
        return np.median(a,axis=axis)
    elif dec=="skip":
        slices=[slice(s) for s in np.shape(a)]
        slices[axis]=0
        return a[tuple(slices)]
    elif hasattr(dec,"__call__"):
        return dec(a,axis)
    else:
        raise ValueError("unrecognized decimation method: {0}".format(dec))


def decimate_datasets(arrs, dec="mean"):
    """
    Decimate datasets with the same shape element-wise (works only for 1D or 2D arrays).
    
    Note that the index data is taken from the first array in the list.
    
    `dec` has the same values and meaning as in :func:`decimate`.
    The format of the output (numpy or pandas, and the name of columns in pandas DataFrame) is determined by the first array in the list.
    """
    if len(arrs)==0:
        raise ValueError("can't decimate an empty list of datasets")
    if len(arrs)==1:
        return arrs[0]
    wrapped=wrap(arrs[0])
    shape=wrapped.shape()
    if wrapped.ndim()==1:
        dec_array=[]
        for a in arrs:
            w=wrap(a)
            if w.shape()!=shape:
                raise ValueError("can't decimate arrays of different shape")
            dec_array.append(a)
        decimated=decimate_full(dec_array,dec=dec)
        return wrapped.array_replaced(decimated,preserve_index=True)
    else:
        column_arrays=[[] for _ in range(shape[1])]
        for a in arrs:
            w=wrap(a)
            if w.shape()!=shape:
                raise ValueError("can't decimate arrays of different shape")
            for i,c in enumerate(w.c):
                column_arrays[i].append(c)
        decimated=[]
        for c in column_arrays:
            decimated_column=decimate_full(c,dec=dec,axis=0)
            decimated.append(decimated_column)
        return wrapped.columns_replaced(decimated,preserve_index=True)



##### Bins routines #####

def collect_into_bins(values, distance, preserve_order=False, to_return="value"):
    """
    Collect all values into bins separated at least by `distance`.
    
    Return the extent of each bin.
    If ``preserve_order==False``, values are sorted before splitting.
    If ``to_return="value"``, the extent is given in values;
    if ``to_return="index"``, it is given in indices (only useful if ``preserve_order=True``, as otherwise the indices correspond to a sorted array).
    If `distance` is a tuple, then it denotes the minimal and the maximal separation between consecutive elements;
    otherwise, it is a single number denoting maximal absolute distance (i.e., it corresponds to a tuple ``(-distance,distance)``).
    """
    if np.ndim(values)!=1:
        raise ValueError("function only works with 1D arrays")
    funcargparse.check_parameter_range(to_return,"to_return",{"value","index"})
    if len(values)==0:
        return []
    if not funcargparse.is_sequence(distance):
        distance=(-distance,distance)
    else:
        distance=min(distance),max(distance)
    if not preserve_order:
        values=np.sort(values)
    start=0
    bins=[]
    for i in range(1,len(values)): #TODO: numpy speedup
        dx=values[i]-values[i-1]
        if dx<distance[0] or dx>distance[1]:
            bins.append((start,i-1))
            start=i
    bins.append((start,len(values)-1))
    if to_return=="value":
        bins=[ (values[f],values[l]) for (f,l) in bins ]
    return bins

def split_into_bins(values, max_span, max_size=None):
    """
    Split values into bins of the span at most `max_span` and number of elements at most `max_size`.
    
    If `max_size` is ``None``, it's assumed to be infinite.
    Return array of indices for each bin. Values are sorted before splitting.
    """
    if np.ndim(values)!=1:
        raise ValueError("function only works with 1D arrays")
    bins=[]
    current_bin=[]
    start=None
    idx=np.argsort(values)
    values=np.sort(values)
    for i,x in zip(idx,values):
        if current_bin:
            if x-start>max_span:
                bins.append(current_bin)
                current_bin=[]
        if len(current_bin)==0:
            start=x
        current_bin.append(i)
        if max_size and len(current_bin)>=max_size:
            bins.append(current_bin)
            current_bin=[]
    if current_bin:
        bins.append(current_bin)
    return bins
    


##### Fourier filters #####

def fourier_filter(trace, response, dt=1, preserve_real=True):
    """
    Apply filter to a trace in the frequency domain.
    
    `response` is a (possibly) complex function with single 1D real numpy array as a frequency argument.
    `dt` specifies time step between consecutive points.
    Note that in case of a multi-column data the filter is applied column-wise;
    this is in contrast with the Fourier transform methods, which would assume the first column to be times.
    
    If ``preserve_real==True``, then the `response` for negative frequencies is automatically taken to be
    complex conjugate of the `response` for positive frequencies (so that the real trace stays real).
    """
    wrapped=wrap(trace)
    if wrapped.ndim()==2:
        return wrapped.columns_replaced([fourier_filter(wrapped.c[i],response=response,dt=dt,preserve_real=preserve_real)
            for i in range(wrapped.shape()[1])])
    trace=np.asarray(trace)
    ft=fourier.fourier_transform(trace,dt=dt,truncate=False)
    if preserve_real:
        freq=ft[:,0]
        zero_idx=utils.find_closest_arg(freq,0,ordered=True)
        ft[zero_idx:,1]=ft[zero_idx:,1]*response(ft[zero_idx:,0])
        ft[:zero_idx,1]=ft[:zero_idx,1]*response(-ft[:zero_idx,0]).conjugate()
        ft[zero_idx,1]=ft[zero_idx,1]*np.real(response(ft[zero_idx,0]))
    else:
        ft[:,1]=ft[:,1]*response(ft[:,0])
    trace_f=fourier.inverse_fourier_transform(ft,truncate=False,raw=True)
    if preserve_real:
        trace_f=trace_f.real
    return wrapped.array_replaced(trace_f,preserve_index=True)
def fourier_make_response_real(response):
    """
    Turn a frequency filter function into a real one (in the time domain).
    
    Done by reflecting and complex conjugating positive frequency part to negative frequencies.
    `response` is a function with a single argument (frequency), return value is a modified function.
    """
    def real_response(freq):
        abs_response=response(abs(freq))
        return abs_response*(freq>0)+abs_response.conjugate()*(freq<0)+abs_response.real*(freq==0)
    return real_response
def fourier_filter_bandpass(pass_range_min, pass_range_max):
    """
    Generate a bandpass filter function (hard cutoff).
    
    The function is symmetric, so that it corresponds to a real response in time domain.
    """
    def response(freq):
        return (abs(freq)<pass_range_max)*(abs(freq)>=pass_range_min)
    return response
def fourier_filter_bandstop(stop_range_min, stop_range_max):
    """
    Generate a bandstop filter function (hard cutoff).
    
    The function is symmetric, so that it corresponds to a real response in time domain.
    """
    def response(freq):
        return (abs(freq)<stop_range_min)+(abs(freq)>=stop_range_max)
    return response