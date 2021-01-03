"""
Digital recursive filter.

Implemented using Numba library (JIT high-performance compilation); used to be a precompiled C-package.
"""

import numpy as np
import numba as nb


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