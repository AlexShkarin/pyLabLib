"""
Routines for Fourier transform.
"""

from __future__ import division

from ..datatable.wrapping import wrap
from ..datatable import column
from . import waveforms, specfunc
import numpy as np
import numpy.fft as fft        



def truncate_len_pow2(trace, truncate_power=None):
    """
    Truncate trace length to the the nearest power of 2.
    
    If `truncate_power` is not ``None``, it determines the minimal power of 2 that has to divide the length.
    (if it is ``None``, than it's the maximal possible power).
    """
    if truncate_power==0:
        return trace
    if truncate_power<0:
        truncate_power=None
    l=len(trace)
    chunk_l=1
    power=0
    while chunk_l*2<=l:
        chunk_l=chunk_l*2
        power=power+1
        if truncate_power is not None and power>=truncate_power:
            break
    l=(l//chunk_l)*chunk_l
    return wrap(trace).t[:l]
def normalize_fourier_transform(ft, normalization="none"):
    """
    Normalize the Fourier transform data.
    
    `ft` is a 2D data with 2 columns: frequency and complex amplitude.
    `normalization` can be ``'none'`` (none done), ``'sum'`` (the power sum is preserved: ``sum(abs(ft)**2)==sum(abs(trace)**2)``)
    or ``'density'`` (power spectral density normalization).
    """
    l=len(ft)
    if normalization=="sum":
        ft=wrap(ft).copy()
        ft[:,1]=ft[:,1]/np.sqrt(l)
        ft=ft.cont
    elif normalization=="density" or normalization=="dBc":
        ft=wrap(ft).copy()
        norm=np.sqrt(l**2*abs(ft[1,0]-ft[0,0]))
        if normalization=="dBc":
            norm=norm*ft[len(ft)//2,1]/l
        ft[:,1]=ft[:,1]/norm
        ft=ft.cont
    elif normalization!="none":
        raise ValueError("unrecognized normalization mode: {0}".format(normalization))
    return ft
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
def fourier_transform(trace, truncate=False, truncate_power=None, normalization="none", no_time=False, single_sided=False, window="rectangle", window_power_compensate=True):
    """
    Calculate a fourier transform of the trace.
    
    Args:
        trace: Time trace to be transformed. Either an ``Nx2`` array, where ``trace[:,0]`` is time and ``trace[:,1]`` is data (real or complex),
            or an ``Nx3`` array, where ``trace[:,0]`` is time, ``trace[:,1]`` is the real part of the signal and ``trace[:,2]`` is the imaginary part.
        truncate (bool): If ``True``, cut the data to the power of 2.
        truncate_power: If ``None``, cut to the nearest power of 2; otherwise, cut to the largest possible length that divides ``2**truncate_power``.
            Only relevant if ``truncate==True``.
        normalization (str): Fourier transform normalization:
        
            - ``'none'``: no normalization;
            - ``'sum'``: then norm of the data is conserved (``sum(abs(ft[:,1])**2)==sum(abs(trace[:,1])**2)``);
            - ``'density'``: power spectral density normalization, in ``x/rtHz`` (``sum(abs(ft[:,1])**2)*df==mean(abs(trace[:,1])**2)``);
            - ``'dBc'``: like ``'density'``, but normalized to the mean trace value.
        no_time (bool): If ``True``, assume that the time axis is missing and use the standard index instead (if trace is 1D data, `no_time` is always ``True``).
        single_sided (bool): If ``True``, only leave positive frequency side of the transform.
        window (str): FT window. Can be ``'rectangle'`` (essentially, no window), ``'hann'`` or ``'hamming'``.
        window_power_compensate (bool): If ``True``, the data is multiplied by a compensating factor to preserve power in the spectrum.
    
    Returns:
        a two-column array, where the first column is frequency, and the second is complex FT data.
    """
    wrapped=wrap(trace)
    column_names=["frequency","ft_data"]
    if trace.ndim==1:
        trace_values=wrapped[:]
    else:
        if wrapped.shape()[1]==(1 if no_time else 2):
            trace_values=wrapped[:,-1]
        elif wrapped.shape()[1]==(2 if no_time else 3):
            trace_values=wrapped[:,-2]+1j*wrapped[:,-1]
        else:
            raise ValueError("fourier_transform doesn't work for an array with shape {0}".format(wrapped.shape()))
    dt=1. if (no_time or wrapped.ndim()==1) else wrapped[1,0]-wrapped[0,0]
    if len(trace_values)==0:
        return wrapped.from_array(np.zeros((0,2)),column_names,wrapped=False)
    if len(trace_values)==1:
        return wrapped.from_array(np.array([[0,trace_values[0]]]),column_names,wrapped=False)
    if truncate:
        trace_values=truncate_len_pow2(trace_values,truncate_power=truncate_power)
    trace_values=apply_window(trace_values,window,window_power_compensate=window_power_compensate)
    ft=fft.fftshift(fft.fft(trace_values))
    df=1./(dt*len(ft))
    frequencies=column.crange(-len(ft)/2.,len(ft)/2.)*df
    ft=wrapped.from_columns([frequencies.as_array(),ft],column_names,wrapped=False) if wrapped.ndim()>1 else np.column_stack((frequencies,ft))
    ft=normalize_fourier_transform(ft,normalization)
    if single_sided:
        ft=wrap(ft).t[len(ft)//2:,:]
        ft[0,0]=0 # numerical error compensation
    return ft
def flip_fourier_transform(ft):
    """
    Flip the fourier transform (analogous to making frequencies negative and flipping the order).
    """
    ft=wrap(ft).copy()
    if len(ft)%2==1:
        ft[:,1]=ft[::-1,1]
    else:
        ft[1::,1]=ft[:0:-1,1]
    return ft.cont

def inverse_fourier_transform(ft, truncate=False, truncate_power=None, no_freq=False, zero_loc=None, symmetric_time=False):
    """
    Calculate an inverse fourier transform of the trace.
    
    Args:
        ft: Fourier transform data to be inverted. Is an ``Nx2`` array, where ``ft[:,0]`` is frequency and ``ft[:,1]`` is fourier transform (real or complex).
        truncate (bool): If ``True``, cut the data to the power of 2.
        truncate_power: If ``None``, cut to the nearest power of 2; otherwise, cut to the largest possible length that divides ``2**truncate_power``.
            Only relevant if ``truncate==True``.
        no_freq (bool): If ``True``, assume that the frequency axis is missing and use the standard index instead (if trace is 1D data, `no_freq` is always ``True``).
        zero_loc (bool): Location of the zero frequency point. Can be ``None`` (the one with the value of f-axis closest to zero), ``'center'`` (mid-point)
            or an integer index.
        symmetric_time (bool): If ``True``, make time axis go from ``(-0.5/df, 0.5/df)`` rather than ``(0, 1./df)``.

    Returns:
        a two-column array, where the first column is frequency, and the second is the complex-valued trace data.
    """
    wrapped=wrap(ft)
    column_names=["time","data"]
    if len(ft)==0:
        return wrapped.from_array(np.zeros((0,2)),column_names,wrapped=False)
    if len(ft)==1:
        return wrapped.from_array(np.array([[0,wrapped[:,0]]]),column_names,wrapped=False)
    no_freq=no_freq or wrapped.ndim()==1
    if zero_loc is None:
        if no_freq:
            zero_freq_point=0
        else:
            zero_freq_point=waveforms.find_closest_arg(wrapped.c[0],0,ordered=True)
            if zero_freq_point is None:
                raise ValueError("can't find zero frequency point; closest is {0}".format(wrapped[zero_freq_point,0]))
    elif zero_loc=="center":
        zero_freq_point=len(ft)//2
    else:
        zero_freq_point=zero_loc
    if wrapped.ndim()==1:
        ft_ordered=np.concatenate(( wrapped[zero_freq_point:], wrapped[:zero_freq_point] ))
    else:
        ft_ordered=np.concatenate(( wrapped[zero_freq_point:,-1], wrapped[:zero_freq_point,-1] ))
    if truncate:
        ft_ordered=truncate_len_pow2(ft_ordered,truncate_power=truncate_power)
    trace=fft.ifft(ft_ordered)
    l=len(trace)
    df=1. if no_freq else wrapped[1,0]-wrapped[0,0]
    dt=1./(df*l)
    times=column.crange(len(ft))*dt
    if symmetric_time:
        times=times-times[l//2]
        trace=np.concatenate((trace[l//2:],trace[:l//2]))
    if wrapped.ndim()==1:
        return np.column_stack((times,trace))
    else:
        return wrapped.from_columns([times.as_array(),trace],column_names,wrapped=False)

def power_spectral_density(trace, truncate=False, truncate_power=None, normalization="density", no_time=False, single_sided=False, window="rectangle", window_power_compensate=True):
    """
    Calculate a power spectral density of the trace.
    
    Args:
        trace: Time trace to be transformed. Either an ``Nx2`` array, where ``trace[:,0]`` is time and ``trace[:,1]`` is data (real or complex),
            or an ``Nx3`` array, where ``trace[:,0]`` is time, ``trace[:,1]`` is the real part of the signal and ``trace[:,2]`` is the imaginary part.
        truncate (bool): If ``True``, cut the data to the power of 2.
        truncate_power: If ``None``, cut to the nearest power of 2; otherwise, cut to the largest possible length that divides ``2**truncate_power``.
            Only relevant if ``truncate==True``.
        normalization (str): Fourier transform normalization:
        
            - ``'none'``: no normalization;
            - ``'sum'``: then norm of the data is conserved (``sum(PSD[:,1]))==sum(abs(trace[:,1])**2)``);
            - ``'density'``: power spectral density normalization, in ``x/rtHz`` (``sum(PSD[:,1])*df==mean(abs(trace[:,1])**2)``);
            - ``'dBc'``: like ``'density'``, but normalized to the mean trace value.
        no_time (bool): If ``True``, assume that the time axis is missing and use the standard index instead (if trace is 1D data, `no_time` is always ``True``).
        single_sided (bool): If ``True``, only leave positive frequency side of the PSD.
        window (str): FT window. Can be ``'rectangle'`` (essentially, no window), ``'hann'`` or ``'hamming'``.
        window_power_compensate (bool): If ``True``, the data is multiplied by a compensating factor to preserve power in the spectrum.
    
    Returns:
        a two-column array, where the first column is frequency, and the second is positive PSD.
    """
    column_names=["frequency","PSD"]
    ft=fourier_transform(trace, truncate=truncate, truncate_power=truncate_power, normalization=normalization, no_time=no_time, single_sided=single_sided, window=window, window_power_compensate=window_power_compensate)
    wrapped=wrap(ft)
    PSD=wrapped.from_columns((wrapped.c[0].real,abs(wrapped.c[1])**2),column_names,wrapped=False)
    return PSD



def get_real_part(ft):
    """
    Get the fourier transform of the real part only from the fourier transform of a complex variable.
    """
    re_ft=wrap(ft).copy()
    re_ft[1:,1]=(ft[1:,1]+ft[:0:-1,1].conjugate())*0.5
    re_ft[0,1]=np.real(ft[0,1])
    return re_ft.cont

def get_imag_part(ft):
    """
    Get the fourier transform of the imaginary part only from the fourier transform of a complex variable.
    """
    im_ft=wrap(ft).copy()
    im_ft[1:,1]=(im_ft[1:,1]-im_ft[:0:-1,1].conjugate())/2.j
    im_ft[0,1]=im_ft[0,1].imag
    return im_ft.cont

def get_correlations(ft_a, ft_b, zero_mean=True, normalization="none"):
    """
    Calculate the correlation function of the two variables given their fourier transforms.
    
    Args:
        ft_a: first variable fourier transform
        ft_b: second variable fourier transform
        zero_mean (bool): If ``True``, the value corresponding to the zero frequency is set to zero (only fluctuations around means of a and b are calculated).
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