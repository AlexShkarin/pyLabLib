"""
Specific useful functions.
"""

from __future__ import division
from ..utils.py3 import textstring


import numpy as np

### Kernels ###

def gaussian_k(x, sigma=1., height=None):
    """
    Gaussian kernel function.
    
    Normalized by the area if `height` is ``None``, otherwise `height` is the value at 0.
    """
    if height is None:
        return 1./np.sqrt(2*np.pi*sigma**2)*np.exp(-(x**2)/(2.*sigma**2))
    else:
        return np.exp(-x**2/(2.*sigma**2))*height

def rectangle_k(x, width=1., height=None):
    """"
    Symmetric rectangle kernel function.
    
    Normalized by the area if `height` is ``None``, otherwise `height` is the value at 0.
    """
    if height is None:
        return (abs(x)<width)/(2.*width)
    else:
        return (abs(x)<width)*height

def lorentzian_k(x, gamma=1., height=None):
    """
    Lorentzian kernel function
    
    Normalized by the area if `height` is ``None``, otherwise `height` is the value at 0.
    """
    if (height is None):
        return gamma/(x**2+(gamma/2.)**2)/np.pi
    else:
        return (gamma/2.)**2/(x**2+(gamma/2.)**2)*height
    
def complex_lorentzian_k(x, gamma=1., amplitude=1.j):
    """
    Complex Lorentzian kernel function.
    """
    return (gamma/2.)/(gamma/2.+1j*x)*amplitude
    

def exp_decay_k(x, width=1., height=None, mode="causal"):
    """
    Exponential decay kernel function
    
    Normalized by area if ``height=None`` (if possible), otherwise `height` is the value at 0.
    
    Mode determines value for ``x<0``:
        - ``'causal'`` - it's 0 for ``x<0``;
        - ``'step'`` - it's constant for ``x<=0``;
        - ``'continue'`` - it's a continuous decaying exponent;
        - ``'mirror'`` - function is symmetric: ``exp(-|x|/width)``.
    """
    if mode=="causal":
        if height is None:
            return (x>=0)*np.exp(-x/float(width))/width
        else:
            return (x>=0)*np.exp(-x/float(width))*height
    elif mode=="step":
        if height is None:
            return ((x>=0)*np.exp(-x/float(width))+(x<0)*1.)/width
        else:
            return ((x>=0)*np.exp(-x/float(width))+(x<0)*1.)*height
    elif mode=="continue":
        if height is None:
            return np.exp(-x/float(width))/width
        else:
            return np.exp(-x/float(width))*height
    elif mode=="mirror":
        if height is None:
            return np.exp(-np.abs(x)/float(width))/width
        else:
            return np.exp(-np.abs(x)/float(width))*height
        
        
_kernel_functions={"gaussian":gaussian_k, "rectangle":rectangle_k, "lorentzian":lorentzian_k, "exp_decay":exp_decay_k, 
                   "complex_lorentzian":complex_lorentzian_k}
def get_kernel_func(kernel):
    """
    Get a kernel function by its name.
    
    Available functions are: ``'gaussian'``, ``'rectangle'``, ``'lorentzian'``, ``'exp_decay'``, ``'complex_lorentzian'``.
    """
    if isinstance(kernel,textstring):
        try:
            return _kernel_functions[kernel]
        except KeyError:
            raise ValueError("unrecognized kernel name: "+kernel)
    else:
        return kernel



### Windows ###
# TODO: different compensations (total power, peak height, etc.?)
def rectangle_w(x, N, ft_compensated=False):
    """
    Rectangle FT window function.
    """
    return x*0+1

def gen_hamming_w(x, N, alpha, beta, ft_compensated=False):
    """
    Generalized Hamming FT window function.
    
    If ``ft_compensated==True``, multiply the window function by a compensating factor to preserve power in the spectrum.
    """
    if ft_compensated:
        return (alpha-beta*np.cos(2*np.pi*x/(N-1)))/np.sqrt(alpha**2+beta**2/2.)
    else:
        return alpha-beta*np.cos(2*np.pi*x/(N-1))

def hann_w(x, N, ft_compensated=False):
    """
    Hann FT window function.
    
    If ``ft_compensated==True``, multiply the window function by a compensating factor to preserve power in the spectrum.
    """
    return gen_hamming_w(x,N,0.5,0.5,ft_compensated=ft_compensated)

def hamming_w(x, N, ft_compensated=False):
    """
    Specific Hamming FT window function.
    
    If ``ft_compensated==True``, multiply the window function by a compensating factor to preserve power in the spectrum.
    """
    return gen_hamming_w(x,N,0.54,0.46,ft_compensated=ft_compensated)


_window_functions={"hamming":hamming_w, "rectangle":rectangle_w, "hann":hann_w}
def get_window_func(window):
    """
    Get a window function by its name.
    
    Available functions are: ``'hamming'``, ``'rectangle'``, ``'hann'``.
    """
    if isinstance(window,textstring):
        try:
            return _window_functions[window]
        except KeyError:
            raise ValueError("unrecognized window name: "+window)
    else:
        return window
    

def gen_hamming_w_ft(f, t, alpha, beta):
    """
    Get Fourier Transform of a generalized Hamming FT window function.
    
    `f` is the argument, `t` is the total window size.
    """
    lim=beta/(2.*alpha)
    gen=np.sinc(f*t)*(1-(f*t)**2 *(alpha-beta)/alpha)/(1-(f*t)**2)
    if isinstance(gen,np.ndarray):
        return np.where(f*t==1,lim,gen)
    return lim if f*t==1 else gen

def rectangle_w_ft(f, t):
    """
    Get Fourier Transform of the rectangle FT window function.
    
    `f` is the argument, `t` is the total window size.
    """
    return gen_hamming_w_ft(f,t,1.,0.)

def hann_w_ft(f, t):
    """
    Get Fourier Transform of the Hann FT window function.
    
    `f` is the argument, `t` is the total window size.
    """
    return gen_hamming_w_ft(f,t,.5,.5)

def hamming_w_ft(f, t):
    """
    Get Fourier Transform of the specific Hamming FT window function.
    
    `f` is the argument, `t` is the total window size.
    """
    return gen_hamming_w_ft(f,t,.54,.46)

_window_ft_functions={"hamming":hamming_w_ft, "rectangle":rectangle_w_ft, "hann":hann_w_ft}
def get_window_ft_func(window):
    """
    Get a Fourier Transform of a window function by its name.
    
    Available functions are: ``'hamming'``, ``'rectangle'``, ``'hann'``.
    """
    if isinstance(window,textstring):
        try:
            return _window_ft_functions[window]
        except KeyError:
            raise ValueError("unrecognized window name: "+window)
    else:
        return window