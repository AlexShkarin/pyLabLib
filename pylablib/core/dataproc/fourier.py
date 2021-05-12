"""
Routines for Fourier transform.
"""

from .table_wrap import wrap
from . import utils, specfunc
import numpy as np
import numpy.fft as fft


_prev_len_cache={}
_default_maxprime=7
def get_prev_len(l, maxprime=_default_maxprime):
    """
    Get the largest number less or equal to `l`, which is composed of prime factors up to `maxprime`.

    So far, only `maxprime` of 2, 3, 5, 7 and 11 are supported.
    `maxprime` of 5 gives less than 15% length reduction (and less than 6% for lengths above 400).
    `maxprime` of 11 gives less than 8% length reduction (and less than 4% for lengths above 300).
    """
    if maxprime not in {2,3,5,7,11}:
        raise ValueError("only factors of 2, 3, 5, 7 and 11 are supported")
    if l<=maxprime:
        return l
    if (maxprime,l) in _prev_len_cache:
        return _prev_len_cache[maxprime,l]
    if maxprime==2:
        res=2**(l.bit_length()-1)
    elif maxprime==3:
        res=1
        p3=1
        while p3<=l:
            r=l//p3
            p23=2**(r.bit_length()-1)*p3
            res=max(res,p23)
            p3*=3
    elif maxprime==5:
        res=1
        p5=1
        while p5<=l:
            p35=p5
            while p35<=l:
                r=l//p35
                p235=2**(r.bit_length()-1)*p35
                res=max(res,p235)
                p35*=3
            p5*=5
    else:
        prevprime=5 if maxprime==7 else 7
        res=1
        pm=1
        while pm<=l:
            res=max(res,get_prev_len(l//pm,prevprime)*pm)
            pm*=maxprime
    if l<1E5 or len(_prev_len_cache)<1E5:
        _prev_len_cache[maxprime,l]=res
    return res
def truncate_trace(trace, maxprime=_default_maxprime):
    """
    Truncate trace length to the nearest smaller length which is composed of prime factors up to `maxprime`.
    
    So far, only `maxprime` of 2, 3, 5, 7 and 11 are supported.
    `maxprime` of 5 gives less than 15% length reduction (and less than 6% for lengths above 400).
    `maxprime` of 11 gives less than 8% length reduction (and less than 4% for lengths above 300).
    """
    if not maxprime:
        return trace
    if maxprime==True:
        maxprime=_default_maxprime
    l=get_prev_len(len(trace),maxprime=maxprime)
    return wrap(trace).t[:l]


def normalize_fourier_transform(ft, normalization="none", df=None, copy=False):
    """
    Normalize the Fourier transform data.
    
    `ft` is a 1D trace or a 2D array with 2 columns: frequency and complex amplitude.
    `normalization` can be ``'none'`` (standard numpy normalization), ``'sum'`` (the power sum is preserved: ``sum(abs(ft)**2)==sum(abs(trace)**2)``),
    ``'rms'`` (the power sum is equal to the trace RMS power: ``sum(abs(ft)**2)==mean(abs(trace)**2)``),
    ``'density'`` (power spectral density normalization, ``sum(abs(ft[:,1])**2)*df==mean(abs(trace[:,1])**2)``),
    or ``'dBc'`` (same as ``'density'``, but normalized by the mean of the trace)
    If ``normalization=='density'``, then `df` can specify the frequency step between two consecutive bins;
    if `df` is ``None``, it is extracted from the first two points of the frequency axis (or set to 1, if `ft` is a 1D trace)
    """
    if normalization=="none":
        return ft
    l=len(ft)
    ft=wrap(ft)
    if copy:
        ft=ft.copy(wrapped=True)
    if df is None:
        df=ft[1,0]-ft[0,0] if ft.ndim()==2 else 1
    if normalization=="sum":
        norm=1/np.sqrt(l)
    elif normalization in {"mean","rms"}:
        norm=1/l
    elif normalization=="density" or normalization=="dBc":
        norm=1/(l*np.sqrt(abs(df)))
        if normalization=="dBc":
            dc_value=ft[len(ft)//2,1] if ft.ndim()==2 else ft[len(ft)//2]
            norm/=dc_value/l
    else:
        raise ValueError("unrecognized normalization mode: {0}".format(normalization))
    if ft.ndim()==2:
        ft[:,1]=ft[:,1]*norm
    else:
        ft[:]=ft[:]*norm
    return ft.cont
def apply_window(trace_values, window="rectangle", window_power_compensate=True):
    """
    Apply FT window to the trace.
    
    If ``window_power_compensate==True``, multiply the data is multiplied by a compensating factor to preserve power in the spectrum.
    """
    if window=="rectangle":
        return trace_values
    window=specfunc.get_window_func(window)
    window_trace=window(np.arange(len(trace_values)),len(trace_values),ft_compensated=window_power_compensate)
    return trace_values*window_trace
def _get_trace_values(wrapped_trace, index_column):
    """Get trace values from a 1D or 2D trace depending on its shape and on whether the index (time or frequency) column is present"""
    if wrapped_trace.ndim()==1:
        return wrapped_trace[:]
    if wrapped_trace.shape()[1]==1:
        return wrapped_trace[:,0]
    if wrapped_trace.shape()[1]==(2 if index_column else 1):
        return wrapped_trace[:,-1]
    if wrapped_trace.shape()[1]==(3 if index_column else 2):
        return wrapped_trace[:,-2]+1j*wrapped_trace[:,-1]
    raise ValueError("function does not work for an array with shape {0}".format(wrapped_trace.shape()))
def fourier_transform(trace, dt=None, truncate=False, normalization="none", single_sided=False, window="rectangle", window_power_compensate=True, raw=False):
    """
    Calculate a fourier transform of the trace.
    
    Args:
        trace: Time trace to be transformed. It can be a 1D trace of values, a 2-column trace, or a 3-column trace.
            If `dt` is ``None``, then the first column is assumed to be time (only support uniform time step),
            and the other columns are either the trace values (for a single data column) or real and imaginary parts of the trace (for two data columns).
            If `dt` is not ``None``, then the time column is assumed to be missing, so the two columns are assumed to be the real and the imaginary parts.
        dt: if not ``None``, can specify the time step between the consecutive samples, in which case it is assumed that the time column is missing from the trace;
            otherwise, try to get it from the time column of the trace if it exists, or set to 1 otherwise.
        truncate (bool or int): Determines whether to truncate the trace to the nearest product of small primes (speeds up FFT algorithm);
            can be ``False`` (no truncation), an integer 2, 3, 5, 7, or 11 (truncate to a product of primes up to and including this number),
            or ``True`` (default prime factorization, currently set to 7)
        normalization (str): Fourier transform normalization:
            - ``'none'``: no (i.e., default numpy) normalization;
            - ``'sum'``: the norm of the data is conserved (``sum(abs(ft[:,1])**2)==sum(abs(trace[:,1])**2)``);
            - ``'rms'``: sum of the PSD is equal to the RMS trace amplitude squared (``sum(abs(ft[:,1])**2)==mean(abs(trace[:,1])**2)``);
            - ``'density'``: power spectral density normalization, in ``x/rtHz`` (``sum(abs(ft[:,1])**2)*df==mean(abs(trace[:,1])**2)``);
            - ``'dBc'``: like ``'density'``, but normalized to the mean trace value.
        single_sided (bool): If ``True``, only leave positive frequency side of the transform.
        window (str): FT window. Can be ``'rectangle'`` (essentially, no window), ``'hann'`` or ``'hamming'``.
        window_power_compensate (bool): If ``True``, the data is multiplied by a compensating factor to preserve power in the spectrum.
        raw (bool): if ``True``, return a simple 1D trace with the result.
    
    Returns:
        a two-column array of the same kind as the input, where the first column is frequency, and the second is complex FT data.
    """
    wrapped=wrap(trace)
    column_names=["frequency","ft_data"]
    trace_values=_get_trace_values(wrapped,index_column=dt is None)
    if len(trace_values)==0:
        return np.array([]) if raw else wrapped.from_array(np.zeros((0,2)),column_names)
    if len(trace_values)==1:
        return np.array([]) if raw else wrapped.from_array(np.array([[0,trace_values[0]]]),column_names)
    trace_values=truncate_trace(trace_values,maxprime=truncate)
    trace_values=apply_window(trace_values,window,window_power_compensate=window_power_compensate)
    ft=fft.fftshift(fft.fft(trace_values))
    if dt is None:
        dt=1. if wrapped.ndim()==1 or wrapped.shape()[1]==1 else wrapped[1,0]-wrapped[0,0]
    df=1./(abs(np.real(dt))*len(ft))
    if not raw:
        frequencies=(np.arange(len(ft))-len(ft)//2)*df
        ft=wrapped.from_columns([frequencies,ft],column_names) if wrapped.ndim()>1 else np.column_stack((frequencies,ft))
    ft=normalize_fourier_transform(ft,normalization,df=df)
    if single_sided:
        if raw:
            ft=ft[len(ft)//2:]
        else:
            ft=wrap(ft).t[len(ft)//2:,:]
            ft[0,0]=0 # numerical error compensation
    return ft
def flip_fourier_transform(ft):
    """
    Flip the fourier transform (analogous to making frequencies negative and flipping the order).
    """
    ft=wrap(ft).copy(wrapped=True)
    if len(ft)%2==1:
        ft[:,1]=ft[::-1,1]
    else:
        ft[1::,1]=ft[:0:-1,1]
    return ft.cont

def inverse_fourier_transform(ft, df=None, truncate=False, zero_loc=None, symmetric_time=False, raw=False):
    """
    Calculate an inverse fourier transform of the trace.
    
    Args:
        ft: Fourier transform data to be inverted. It can be a 1D trace of values, a 2-column trace, or a 3-column trace.
            If `df` is ``None``, then the first column is assumed to be frequency (only support uniform frequency step),
            and the other columns are either the trace values (for a single data column) or real and imaginary parts of the trace (for two data columns).
            If `df` is not ``None``, then the frequency column is assumed to be missing, so the two columns are assumed to be the real and the imaginary parts.
        df: if not ``None``, can specify the frequency step between the consecutive samples; otherwise, try to get it from the frequency column of the trace
            if it exists, or set to 1 otherwise.
        truncate (bool or int): Determines whether to truncate the trace to the nearest product of small primes (speeds up FFT algorithm);
            can be ``False`` (no truncation), an integer 2, 3, 5, 7, or 11 (truncate to a product of primes up to and including this number),
            or ``True`` (default prime factorization, currently set to 7)
        zero_loc (bool): Location of the zero frequency point.
            Can be ``None`` (the one with the value of f-axis closest to zero, or the first point if the frequency column is missing),
            ``'center'`` (mid-point), or an integer index.
        symmetric_time (bool): If ``True``, make time axis go from ``(-0.5/df, 0.5/df)`` rather than ``(0, 1./df)``.
        raw (bool): if ``True``, return a simple 1D trace with the result.

    Returns:
        a two-column array, where the first column is frequency, and the second is the complex-valued trace data.
    """
    wrapped=wrap(ft)
    column_names=["time","data"]
    ft_values=_get_trace_values(wrapped,index_column=df is None)
    if len(ft)==0:
        return np.array([]) if raw else wrapped.from_array(np.zeros((0,2)),column_names)
    if len(ft)==1:
        return np.array([ft_values[0]]) if raw else wrapped.from_array(np.array([[0,ft_values[0]]]),column_names)
    if zero_loc is None:
        if df is not None or wrapped.ndim()==1 or wrapped.shape()[1]==1:
            zero_freq_point=0
        else:
            zero_freq_point=utils.find_closest_arg(wrapped.c[0],0,ordered=True)
            if zero_freq_point is None:
                raise ValueError("can't find zero frequency point; closest is {0}".format(wrapped[zero_freq_point,0]))
    elif zero_loc=="center":
        zero_freq_point=len(ft)//2
    else:
        zero_freq_point=zero_loc
    if zero_freq_point!=0:
        ft_values=np.concatenate(( ft_values[zero_freq_point:], ft_values[:zero_freq_point] ))
    ft_values=truncate_trace(ft_values,maxprime=truncate)
    trace=fft.ifft(ft_values)
    l=len(trace)
    if symmetric_time:
        trace=np.concatenate((trace[l//2:],trace[:l//2]))
    if raw:
        return trace
    if df is None:
        df=1. if wrapped.ndim()==1 or wrapped.shape()[1]==1 else wrapped[1,0]-wrapped[0,0]
    dt=1./(abs(np.real(df))*l)
    times=np.arange(len(ft))*dt
    if symmetric_time:
        times-=times[l//2]
    if wrapped.ndim()==1:
        return np.column_stack((times,trace))
    else:
        return wrapped.from_columns([times,trace],column_names)

def power_spectral_density(trace, dt=None, truncate=False, normalization="density", single_sided=False, window="rectangle", window_power_compensate=True, raw=False):
    """
    Calculate a power spectral density of the trace.
    
    Args:
        trace: Time trace to be transformed. It can be a 1D trace of values, a 2-column trace, or a 3-column trace.
            If `dt` is ``None``, then the first column is assumed to be time (only support uniform time step),
            and the other columns are either the trace values (for a single data column) or real and imaginary parts of the trace (for two data columns).
            If `dt` is not ``None``, then the time column is assumed to be missing, so the two columns are assumed to be the real and the imaginary parts.
        dt: if not ``None``, can specify the time step between the consecutive samples; otherwise, try to get it from the time column of the trace
            if it exists, or set to 1 otherwise.
        truncate (bool or int): Determines whether to truncate the trace to the nearest product of small primes (speeds up FFT algorithm);
            can be ``False`` (no truncation), an integer 2, 3, 5, 7, or 11 (truncate to a product of primes up to and including this number),
            or ``True`` (default prime factorization, currently set to 7)
        normalization (str): Fourier transform normalization:
            - ``'none'``: no (i.e., default numpy) normalization;
            - ``'sum'``: the norm of the data is conserved (``sum(PSD[:,1])==sum(abs(trace[:,1])**2)``);
            - ``'rms'``: sum of the PSD is equal to the RMS trace amplitude squared (``sum(PSD[:,1])==mean(abs(trace[:,1])**2)``);
            - ``'density'``: power spectral density normalization, in ``x/rtHz`` (``sum(PSD[:,1])*df==mean(abs(trace[:,1])**2)``);
            - ``'dBc'``: like ``'density'``, but normalized to the mean trace value.
        single_sided (bool): If ``True``, only leave positive frequency side of the PSD.
        window (str): FT window. Can be ``'rectangle'`` (essentially, no window), ``'hann'`` or ``'hamming'``.
        window_power_compensate (bool): If ``True``, the data is multiplied by a compensating factor to preserve power in the spectrum.
        raw (bool): if ``True``, return a simple 1D trace with the result.
    
    Returns:
        a two-column array, where the first column is frequency, and the second is positive PSD.
    """
    column_names=["frequency","PSD"]
    ft=fourier_transform(trace,dt=dt,truncate=truncate,normalization=normalization,
                single_sided=single_sided,window=window,window_power_compensate=window_power_compensate,raw=True)
    if raw:
        return abs(ft)**2
    wrapped=wrap(trace)
    if dt is None:
        dt=1. if wrapped.ndim()==1 or wrapped.shape()[1]==1 else wrapped[1,0]-wrapped[0,0]
    df=1./(dt*len(ft))
    frequencies=(np.arange(len(ft))-len(ft)//2)*df
    if wrapped.ndim()==1:
        return np.column_stack((frequencies,abs(ft)**2))
    else:
        return wrapped.from_columns((frequencies,abs(ft)**2),column_names)



def get_real_part_ft(ft):
    """
    Get the fourier transform of the real part only from the fourier transform of a complex variable.
    """
    re_ft=wrap(ft).copy(wrapped=True)
    re_ft[1:,1]=(ft[1:,1]+ft[:0:-1,1].conjugate())*0.5
    re_ft[0,1]=np.real(ft[0,1])
    return re_ft.cont

def get_imag_part_ft(ft):
    """
    Get the fourier transform of the imaginary part only from the fourier transform of a complex variable.
    """
    im_ft=wrap(ft).copy(wrapped=True)
    im_ft[1:,1]=(im_ft[1:,1]-im_ft[:0:-1,1].conjugate())/2.j
    im_ft[0,1]=im_ft[0,1].imag
    return im_ft.cont

def get_correlations_ft(ft_a, ft_b, zero_mean=True, normalization="none"):
    """
    Calculate the correlation function of the two variables given their fourier transforms.
    
    Args:
        ft_a: first variable fourier transform
        ft_b: second variable fourier transform
        zero_mean (bool): If ``True``, the value corresponding to the zero frequency is set to zero (only fluctuations around means of ``a`` and ``b`` are calculated).
        normalization (str): Can be ``'whole'`` (correlations are normalized by product of PSDs derived from `ft_a` and `ft_b`)
            or ``'individual'`` (normalization is done for each frequency individually, so that the absolute value is always 1).
    """
    if len(ft_a)!=len(ft_b):
        raise ValueError("transforms should be of the same length")
    corr=ft_a.copy()
    corr[:,1]=corr[:,1]*ft_b[:,1].conjugate()
    if (zero_mean):
        corr[len(corr)/2,1]=0.
    if normalization=="whole":
        norm_a=(abs(ft_a[:,1])**2).sum()-abs(ft_a[len(ft_a)/2,1])**2
        norm_b=(abs(ft_b[:,1])**2).sum()-abs(ft_b[len(ft_b)/2,1])**2
        corr[:,1]=corr[:,1]/(norm_a*norm_b)**.5
    elif normalization=="individual":
        norm_factors=abs(ft_a[:,1]*ft_b[:,1])
        corr[:,1]=corr[:,1]/norm_factors
    elif normalization!="none":
        raise ValueError("unrecognized normalization method: {0}".format(normalization))
    return corr