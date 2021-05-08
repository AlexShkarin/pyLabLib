"""
Digital recursive infinite impulse response filter.

Implemented using Numba library (JIT high-performance compilation) if possible.
"""

import numpy as np
import warnings

NBError=ImportError
try:
    import numba as nb
    NBError=nb.errors.NumbaError
    @nb.njit(fastmath=False,parallel=False)
    def iir_apply_complex(trace, xcoeff, ycoeff):
        """
        Apply digital, (possibly) recursive filter with coefficients `xcoeff` and `ycoeff` along the first axis.

        Result is filtered signal `y` with ``y[n]=sum_j x[n-j]*xcoeff[j] + sum_k y[n-k-1]*ycoeff[k]``.
        """
        new_trace=np.zeros(trace.shape,dtype=trace.dtype)
        if len(xcoeff)==0:
            return new_trace
        nx=len(xcoeff)
        ny=len(ycoeff)
        tstart=max(nx-1,ny)
        new_trace[:tstart]=trace[:tstart]
        for i in range(tstart,len(trace)):
            for xi in range(nx):
                new_trace[i]+=trace[i-xi]*xcoeff[xi]
            for yi in range(ny):
                new_trace[i]+=new_trace[i-yi-1]*ycoeff[yi]
        return new_trace
except NBError:
    def iir_apply_complex(trace, xcoeff, ycoeff):
        """
        Apply digital, (possibly) recursive filter with coefficients `xcoeff` and `ycoeff` along the first axis.

        Result is filtered signal `y` with ``y[n]=sum_j x[n-j]*xcoeff[j] + sum_k y[n-k-1]*ycoeff[k]``.
        """
        warnings.warn("Numba is missing, so the IIR filter is implemented via pure Python; the performance might suffer")
        new_trace=np.zeros_like(trace)
        xcoeff=np.asarray(xcoeff)
        ycoeff=np.asarray(ycoeff)
        if len(xcoeff)==0:
            return new_trace
        nx=len(xcoeff)
        ny=len(ycoeff)
        tstart=max(nx-1,ny)
        new_trace[:tstart]=trace[:tstart]
        rxcoeff=xcoeff[::-1]
        rycoeff=ycoeff[::-1]
        for i in range(tstart,len(trace)):
            new_trace[i]=np.sum(trace[i-nx+1:i+1]*rxcoeff,axis=0)+np.sum(new_trace[i-ny:i]*rycoeff,axis=0)
        return new_trace