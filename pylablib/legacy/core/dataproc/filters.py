"""
Routines for filtering arrays (mostly 1D data).
"""

from __future__ import division
from builtins import range

from . import fourier
from ..datatable import column #@UnresolvedImport
from ..datatable import table #@UnresolvedImport
from ..datatable.wrapping import wrap #@UnresolvedImport
from ..utils import funcargparse, general as general_utils #@UnresolvedImport
from . import waveforms, specfunc, iir_transform

import numpy as np
import scipy.ndimage as ndimage

_depends_local=["..datatable.column","..datatable.table",".waveforms"]



##### Convolution filters #####

def convolve1d(wf, kernel, mode="reflect", cval=0.):
    """
    Convolution filter.
    
    Convolves `wf` with the given `kernel` (1D array). `mode` and `cval` determine how the endpoints are handled.
    Simply a wrapper around the standard :func:`scipy.ndimage.convolve` that handles complex arguments.
    """
    wf=np.asarray(wf)
    kernel=np.asarray(kernel)
    wf_complex=np.iscomplexobj(wf) or np.iscomplexobj(cval)
    kernel_complex=np.iscomplexobj(kernel)
    if wf_complex and kernel_complex:
        cval=complex(cval)
        real_part=ndimage.convolve1d(wf.real, kernel.real, mode=mode, cval=cval.real)-ndimage.convolve1d(wf.imag, kernel.imag, mode=mode, cval=cval.imag)
        imag_part=ndimage.convolve1d(wf.real, kernel.imag, mode=mode, cval=cval.real)+ndimage.convolve1d(wf.imag, kernel.real, mode=mode, cval=cval.imag)
        res=real_part+1j*imag_part
    elif wf_complex:
        cval=complex(cval)
        res=ndimage.convolve1d(wf.real, kernel, mode=mode, cval=cval.real)+1j*ndimage.convolve1d(wf.imag, kernel, mode=mode, cval=cval.imag)
    elif kernel_complex:
        res=ndimage.convolve1d(wf, kernel.real, mode=mode, cval=cval)+1j*ndimage.convolve1d(wf, kernel.imag, mode=mode, cval=cval)
    else:
        res=ndimage.convolve1d(wf, kernel, mode=mode, cval=cval)
    return wrap(wf).array_replaced(res,wrapped=False)
        
def convolution_filter(wf, width=1., kernel="gaussian", kernel_span="auto", mode="reflect", cval=0., kernel_height=None):
    """
    Convolution filter.
    
    Args:
        wf: Waveform for filtering.
        width (float): Kernel width (second parameter to the kernel function).
        kernel: Either a string defining the kernel function (see :func:`.specfunc.get_kernel_func` for possible kernels),
            or a function taking 3 arguments ``(pos, width, height)``, where `height` can be ``None`` (assumes normalization by area). 
        kernel_span: The cutoff for the kernel function. Either an integer (number of points) or ``'auto'``.
        mode (str): Convolution mode (see :func:`scipy.ndimage.convolve`).
        cval (float): Convolution fill value (see :func:`scipy.ndimage.convolve`).
        kernel_height: Height parameter to be passed to the kernel function. ``None`` means normalization by area.
    """
    wrapped=wrap(wf)
    if wrapped.ndim()==2:
        return wrapped.columns_replaced([convolution_filter(wrapped.c[i],width=width,kernel=kernel,kernel_span=kernel_span,mode=mode,cval=cval,kernel_height=kernel_height)
            for i in range(wrapped.shape()[1])],wrapped=False)
    elif wrapped.ndim()!=1:
        raise ValueError("this function accepts only 1D or 2D arrays")
    if kernel_span=="auto":
        if kernel=="gaussian":
            kernel_span=int(np.ceil(width*6))
        elif kernel=="rectangle":
            kernel_span=int(np.ceil(width))
        elif kernel=="exp_decay":
            kernel_span=int(np.ceil(width*18)) #accuracy of 10^(-6)
        else:
            kernel_span=len(wf)
    if kernel_span>len(wf):
        kernel_span=len(wf)
    kernel=specfunc.get_kernel_func(kernel)
    kernel_wf=kernel(np.arange(-kernel_span,kernel_span+1.),width,kernel_height)
    if kernel_height is None:
        kernel_wf=kernel_wf/kernel_wf.sum() #normalize kernel; non-normalized kernel might be useful e.g. for low-pass filtering when width is close len(wf)
    return wrap(wf).from_array(convolve1d(wf, kernel_wf, mode=mode, cval=cval),wrapped=False)

def gaussian_filter(wf, width=1., mode="reflect", cval=0.):
    """
    Simple gaussian filter. Can handle complex data.
    
    Equivalent to a convolution with a gaussian. Equivalent to :func:`scipy.ndimage.gaussian_filter1d`, uses :func:`convolution_filter`.
    """
    return convolution_filter(wf,width,kernel="gaussian",mode=mode,cval=cval)

def gaussian_filter_nd(wf, width=1., mode="reflect", cval=0.):
    """
    Simple gaussian filter. Can't handle complex data.
    
    Equivalent to a convolution with a gaussian. Wrapper around :func:`scipy.ndimage.gaussian_filter`. 
    """
    res=ndimage.gaussian_filter(wf*1., width, mode=mode, cval=cval)
    return wrap(wf).array_replaced(res,wrapped=False)


##### IIR filters #####

def low_pass_filter(wf, t=1., mode="reflect", cval=0.):
    """
    Simple single-pole low-pass filter.
    
    `t` is the filter time constant, `mode` and `cval` are the waveform expansion parameters (only from the left).
    Implemented as a recursive digital filter, so its performance doesn't depend strongly on `t`.
    Works only for 1D arrays.
    """
    expand_size=min(int(np.ceil(t*20)),len(wf))
    wf=waveforms.expand_waveform(wf, size=expand_size, mode=mode, cval=cval, side="left")
    beta=np.exp(np.double(-1.)/np.double(t))
    alpha=np.double(1.)-beta
    filtered_wf=iir_transform.iir_apply_complex(wf,np.array([alpha]),np.array([beta]))
    return wrap(wf).array_replaced(filtered_wf).t[expand_size:]
    
def high_pass_filter(wf, t=1., mode="reflect", cval=0.):
    """
    Simple single-pole high-pass filter (equivalent to subtracting a low-pass filter).
    
    `t` is the filter time constant, `mode` and `cval` are the waveform expansion parameters (only from the left).
    Implemented as a recursive digital filter, so its performance doesn't depend strongly on `t`.
    Works only for 1D arrays.
    """
    return wf-low_pass_filter(wf,t,mode,cval)
def integrate(wf):
    """
    Calculate the integral of the waveform.
    
    Works only for 1D arrays.
    """
    return iir_transform.iir_apply_complex(wf,np.array([1]),np.array([1]))
def differentiate(wf):
    """
    Calculate the differential of the waveform.
    
    Works only for 1D arrays.
    """
    wf=wf.copy()
    if len(wf)>=2:
        wf[1:]=wf[1:]-wf[:-1]
        wf[0]=wf[1]
    elif len(wf)==1:
        wf[0]=0
    return wf


##### Sliding filters #####

def sliding_average(wf, width=1., mode="reflect", cval=0.):
    """
    Simple sliding average filter
    
    Equivalent to convolution with a rectangle peak function.
    """
    return convolution_filter(wf, width, kernel="rectangle", mode=mode, cval=cval)

def median_filter(wf, width=1, mode="reflect", cval=0.):
    """
    Median filter.
    
    Wrapper around :func:`scipy.ndimage.median_filter`.
    """
    res=ndimage.median_filter(wf,width,mode=mode,cval=cval)
    return wrap(wf).array_replaced(res,wrapped=False)


def _sliding_func(wf, filtering_function, width=1, mode="reflect", cval=0.):
    """
    Perform a sliding filtering of a 1D waveform with the given `filtering_function`.
    
    mode ('drop' or 'leave') determines whether to drop the last bin if it's not full
    Works only with arrays (no columns or tables).
    """
    wrapped=wrap(wf)
    if wrapped.ndim()==2:
        return wrapped.columns_replaced([_sliding_func(wrapped.c[i],filtering_function=filtering_function,mode=mode,cval=cval)
            for i in range(wrapped.shape()[1])],wrapped=False)
    elif wrapped.ndim()!=1:
        raise ValueError("this function accepts only 1D or 2D arrays")
    if width is None or width<=1:
        return wf
    l=len(wf)
    width=(int(width)//2)*2+1
    wf=waveforms.expand_waveform(wf,width//2,mode,cval)
    return np.array([filtering_function(wf[i-width//2:i+width//2+1]) for i in range(width//2,l+width//2)])

def _sliding_filter(wf, n=1, dec_mode="bin", mode="reflect", cval=0.):
    """
    Perform sliding filtering on the data.
    
    Args:
        wf: 1D array-like object.
        n (int): bin width.
        dec_mode (str):
            Decimation mode. Can be
                - ``'bin'`` or ``'mean'`` - do a binning average;
                - ``'sum'`` - sum points;
                - ``'min'`` - leave min point;
                - ``'max'`` - leave max point;
                - ``'median'`` - leave median point (works as a median filter).
        mode (str): Expansion mode. Can be ``'constant'`` (added values are determined by `cval`), ``'nearest'`` (added values are endvalues of the waveform),
            ``'reflect'`` (reflect waveform wrt its endpoint) or ``'wrap'`` (wrap the values from the other size).
        cval (float): If ``mode=='constant'``, determines the expanded values.
    """
    wrapper=wrap(wf)
    wf=np.asarray(wf)
    if dec_mode=="bin" or dec_mode=="mean":
        res=_sliding_func(wf,np.mean,n,mode=mode,cval=cval)
    elif dec_mode=="sum":
        res=_sliding_func(wf,np.sum,n,mode=mode,cval=cval)
    elif dec_mode=="min":
        res=_sliding_func(wf,np.min,n,mode=mode,cval=cval)
    elif dec_mode=="max":
        res=_sliding_func(wf,np.max,n,mode=mode,cval=cval)
    elif dec_mode=="median":
        res=_sliding_func(wf,np.median,n,mode=mode,cval=cval)
    else:
        raise ValueError("unrecognized decimation type: {0}".format(dec_mode))
    return wrapper.array_replaced(res,wrapped=False)
sliding_filter=general_utils.try_method_wrapper(_sliding_filter,method_name="sliding_filter")
column.IDataColumn.sliding_filter=_sliding_filter
table.DataTable.add_columnwise_function(sliding_filter,alias="sliding_filter",collection_type="table",column_arg_name="column")


##### Decimation filters #####

def _decimation_filter(wf, decimation_function, width=1, axis=0, mode="drop"):
    """
    Perform a decimation filtering with the given `decimation_function`.
    
    mode ('drop' or 'leave') determines whether to drop the last bin if it's not full
    Works only with arrays (no columns or tables).
    """
    if width is None or width<=1:
        return wf
    if not mode in ["drop", "leave"]:
        raise ValueError("unrecognized binning mode: "+mode)
    width=int(width)
    shape=np.shape(wf)
    actual_len=shape[axis]
    dec_len=int(actual_len/width)*width
    if mode=="drop":
        cropped_slices=[slice(s) for s in shape]
        cropped_slices[axis]=slice(dec_len)
        dec_shape=shape[:axis]+(-1,width)+shape[axis+1:]
        return decimation_function(np.reshape(wf[tuple(cropped_slices)],dec_shape),axis+1)
    elif mode=="leave":
        dec_wf=_decimation_filter(wf,decimation_function,width,axis=axis,mode="drop")
        if dec_len==actual_len:
            return dec_wf
        rest_indices=np.arange(dec_len,actual_len)
        dec_rest=decimation_function(np.take(wf,rest_indices,axis=axis),axis=axis)
        return np.append(dec_wf,dec_rest,axis=axis)
        

def _decimate(wf, n=1, dec_mode="skip", axis=0, mode="drop"):
    """
    Decimate the data.
    
    Args:
        wf: Data.
        n (int): Decimation factor.
        dec_mode (str): Decimation mode. Can be
                - ``'skip'`` - just leave every n'th point while completely omitting everything else;
                - ``'bin'`` or ``'mean'`` - do a binning average;
                - ``'sum'`` - sum points;
                - ``'min'`` - leave min point;
                - ``'max'`` - leave max point;
                - ``'median'`` - leave median point (works as a median filter).
        axis (int): Axis along which to perform the decimation.
        mode (str): Determines what to do with the last bin if it's incomplete. Can be either ``'drop'`` (omit the last bin) or ``'leave'`` (keep it).
    """
    wf,wf_orig=np.asarray(wf),wf
    wrapper=wrap(wf_orig) if wf.ndim<3 else None
    if dec_mode=="bin" or dec_mode=="mean":
        res=_decimation_filter(wf,np.mean,n,axis=axis,mode=mode)
    elif dec_mode=="sum":
        res=_decimation_filter(wf,np.sum,n,axis=axis,mode=mode)
    elif dec_mode=="min":
        res=_decimation_filter(wf,np.min,n,axis=axis,mode=mode)
    elif dec_mode=="max":
        res=_decimation_filter(wf,np.max,n,axis=axis,mode=mode)
    elif dec_mode=="median":
        res=_decimation_filter(wf,np.median,n,axis=axis,mode=mode)
    elif dec_mode=="skip":
        def _dec_fun(wf, axis):
            slices=[slice(s) for s in np.shape(wf)]
            slices[axis]=0
            return wf[tuple(slices)]
        res=_decimation_filter(wf,_dec_fun,n,axis=axis,mode=mode)
    else:
        raise ValueError("unrecognized decimation type: {0}".format(dec_mode))
    return wrapper.array_replaced(res,wrapped=False) if res.ndim<3 else res
decimate=general_utils.try_method_wrapper(_decimate,method_name="decimate")
column.IDataColumn.decimate=_decimate
table.DataTable.add_columnwise_function(decimate,alias="decimate",collection_type="table",column_arg_name="column")
def _decimate_linear(wf, n=1, dec_mode="skip", axis=0, mode="drop"):
    """
    Decimate a linear column data.
    
    For parameters, see :func:`.filters.decimate`.
    """
    if n is None or n<=1:
        return wf
    if mode=="leave" or dec_mode=="sum":
        return _decimate(wf,n,dec_mode=dec_mode,axis=axis,mode=mode)
    n=int(n)
    length,start,step=wf.length,wf.start,wf.step
    if dec_mode=="skip":
        return column.LinearDataColumn(length//n,start,step*n)
    elif dec_mode=="min":
        if step>=0:
            return column.LinearDataColumn(length//n,start,step*n)
        else:
            return column.LinearDataColumn(length//n,start+(n-1)*step,step*n)
    elif dec_mode=="max":
        if step>=0:
            return column.LinearDataColumn(length//n,start+(n-1)*step,step*n)
        else:
            return column.LinearDataColumn(length//n,start,step*n)
    elif dec_mode=="median" or dec_mode=="bin" or dec_mode=="mean":
        return column.LinearDataColumn(length//n,start+(n-1)*step/2.,step*n)
    else:
        raise ValueError("unrecognized decimation type: {0}".format(dec_mode))
column.LinearDataColumn.decimate=_decimate_linear

def binning_average(wf, width=1, axis=0, mode="drop"):
    """
    Binning average filter.
    
    Equivalent to :func:`decimate` with ``dec_mode=='bin'``.
    """
    return decimate(wf,width,"mean",axis=axis,mode=mode)

def decimate_full(wf, dec_mode="skip", axis=0):
    """
    Completely decimate the data along a given axis
    
    Args:
        wf: Data.
        dec_mode (str):
            Decimation mode. Can be
                - ``'skip'`` - just leave every n'th point while completely omitting everything else;
                - ``'bin'`` or ``'mean'`` - do a binning average;
                - ``'sum'`` - sum points;
                - ``'min'`` - leave min point;
                - ``'max'`` - leave max point;
                - ``'median'`` - leave median point (works as a median filter).
        axis (int): Axis along which to perform the decimation.
    """
    wf=np.asarray(wf)
    if dec_mode=="bin" or dec_mode=="mean":
        return np.mean(wf,axis=axis)
    elif dec_mode=="sum":
        return np.sum(wf,axis=axis)
    elif dec_mode=="min":
        return np.min(wf,axis=axis)
    elif dec_mode=="max":
        return np.max(wf,axis=axis)
    elif dec_mode=="median":
        return np.median(wf,axis=axis)
    elif dec_mode=="skip":
        slices=[slice(s) for s in np.shape(wf)]
        slices[axis]=0
        return wf[tuple(slices)]
    else:
        raise ValueError("unrecognized decimation type: {0}".format(dec_mode))


def decimate_datasets(wfs, dec_mode="mean"):
    """
    Decimate datasets with the same shape element-wise (works only for 1D or 2D arrays).
    
    `dec_mode` has the same values and meaning as in :func:`decimate`.
    """
    if len(wfs)==0:
        raise ValueError("can't decimate an empty list of datasets")
    if len(wfs)==1:
        return wfs[0]
    wrapped=wrap(wfs[0])
    shape=wrapped.shape()
    if wrapped.ndim()==1:
        dec_array=[]
        for wf in wfs:
            w=wrap(wf)
            if w.shape()!=shape:
                raise ValueError("can't decimate arrays of different shape")
            dec_array.append(wf)
        decimated=decimate(np.column_stack(dec_array),n=len(wfs),dec_mode=dec_mode,axis=1)[:,0]
        return wrapped.array_replaced(decimated,wrapped=False)
    else:
        column_arrays=[[] for _ in range(shape[1])]
        for wf in wfs:
            w=wrap(wf)
            if w.shape()!=shape:
                raise ValueError("can't decimate arrays of different shape")
            for i,c in enumerate(w.c):
                column_arrays[i].append(c)
        decimated=[]
        for c in column_arrays:
            decimated_column=decimate(np.column_stack(c),n=len(wfs),dec_mode=dec_mode,axis=1)
            decimated.append(decimated_column[:,0])
        return wrapped.columns_replaced(decimated,wrapped=False)

    
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

def fourier_filter(trace, response, preserve_real=True):
    """
    Apply filter to a trace in frequency domain.
    
    `response` is a (possibly) complex function with single 1D real numpy array as a frequency argument.
    
    If ``preserve_real==True``, then the `response` for negative frequencies is automatically taken to be
    complex conjugate of the `response` for positive frequencies (so that the real trace stays real).
    """
    ft=fourier.fourier_transform(trace, truncate=False)
    if preserve_real:
        freq=wrap(ft).c[0]
        zero_idx=waveforms.find_closest_arg(freq,0,ordered=True)
        ft[zero_idx:,1]=ft[zero_idx:,1]*response(ft[zero_idx:,0])
        ft[:zero_idx,1]=ft[:zero_idx,1]*response(-ft[:zero_idx,0]).conjugate()
        ft[zero_idx,1]=ft[zero_idx,1]*np.real(response(ft[zero_idx,0]))
    else:
        ft[:,1]=ft[:,1]*response(ft[:,0])
    trace_f=fourier.inverse_fourier_transform(ft, truncate=False)
    if wrap(trace_f).get_type()=="2d.table":
        trace_f.set_column_names(trace.get_column_names()[:2])
        if preserve_real:
            trace_f.c[1]=trace_f.c[1].real
    elif preserve_real:
        trace_f=trace_f.real
    return trace_f
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