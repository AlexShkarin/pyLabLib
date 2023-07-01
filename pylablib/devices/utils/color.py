from ...core.utils import nbtools

import numpy as np
import numba as nb

import functools


@functools.lru_cache(1024)
def _bayer_interpolate_nb(tsrc="u2", tdst=None, par=False, nogil=True):
    if tdst is None:
        tdst=tsrc
    if isinstance(tsrc,np.dtype):
        tsrc="{}{}".format(tsrc.kind,tsrc.itemsize)
    if isinstance(tdst,np.dtype):
        tdst="{}{}".format(tdst.kind,tdst.itemsize)
    ain=nbtools.c_array(base=tsrc,ndim=3,readonly=True)
    aout=nbtools.c_array(base=tdst,ndim=3,readonly=False,contiguous="A")
    @nb.njit(nb.void(ain,aout,nb.u8,nb.u8,nb.u8,nb.u8),parallel=par,nogil=nogil)
    def interpolate(src, dst, ioff=0, joff=0, mode=0, roff=0): # mode=0 is 1 pixel per square (RB), mode=1 is 2 pixels per square (G)
        n,r,c=src.shape
        if mode==0:
            for f in nb.prange(n):  # pylint: disable=not-an-iterable
                for i in range(r):
                    for j in range(c):
                        if i%2==ioff and j%2==joff:
                            dst[f,i,j]=src[f,i,j]
                        elif (i+1)%2==ioff and j%2==joff:
                            if i==0:
                                dst[f,i,j]=src[f,i+1,j]
                            elif i==r-1:
                                dst[f,i,j]=src[f,i-1,j]
                            else:
                                dst[f,i,j]=(src[f,i-1,j]+src[f,i+1,j]+roff)/2
                        elif i%2==ioff and (j+1)%2==joff:
                            if j==0:
                                dst[f,i,j]=src[f,i,j+1]
                            elif j==c-1:
                                dst[f,i,j]=src[f,i,j-1]
                            else:
                                dst[f,i,j]=(src[f,i,j-1]+src[f,i,j+1]+roff)/2
                        else:
                            if i==0:
                                if j==0:
                                    dst[f,i,j]=src[f,i+1,j+1]
                                elif j==c-1:
                                    dst[f,i,j]=src[f,i+1,j-1]
                                else:
                                    dst[f,i,j]=(src[f,i+1,j-1]+src[f,i+1,j+1]+roff)/2
                            elif i==r-1:
                                if j==0:
                                    dst[f,i,j]=src[f,i-1,j+1]
                                elif j==c-1:
                                    dst[f,i,j]=src[f,i-1,j-1]
                                else:
                                    dst[f,i,j]=(src[f,i-1,j-1]+src[f,i-1,j+1]+roff)/2
                            else:
                                if j==0:
                                    dst[f,i,j]=(src[f,i-1,j+1]+src[f,i+1,j+1]+roff)/2
                                elif j==c-1:
                                    dst[f,i,j]=(src[f,i-1,j-1]+src[f,i+1,j-1]+roff)/2
                                else:
                                    dst[f,i,j]=(src[f,i-1,j+1]+src[f,i+1,j+1]+src[f,i-1,j-1]+src[f,i+1,j-1]+roff*2)/4
        if mode==1:
            for f in nb.prange(n):  # pylint: disable=not-an-iterable
                for i in range(r):
                    for j in range(c):
                        if (i%2==ioff and j%2==joff) or ((i+1)%2==ioff and (j+1)%2==joff):
                            dst[f,i,j]=src[f,i,j]
                        else:
                            if i==0:
                                if j==0:
                                    dst[f,i,j]=(src[f,i+1,j]+src[f,i,j+1]+roff)/2
                                elif j==c-1:
                                    dst[f,i,j]=(src[f,i+1,j]+src[f,i,j-1]+roff)/2
                                else:
                                    dst[f,i,j]=(src[f,i+1,j]+src[f,i,j+1]+src[f,i,j-1]+roff)/3
                            elif i==r-1:
                                if j==0:
                                    dst[f,i,j]=(src[f,i-1,j]+src[f,i,j+1]+roff)/2
                                elif j==c-1:
                                    dst[f,i,j]=(src[f,i-1,j]+src[f,i,j-1]+roff)/2
                                else:
                                    dst[f,i,j]=(src[f,i-1,j]+src[f,i,j+1]+src[f,i,j-1]+roff)/3
                            else:
                                if j==0:
                                    dst[f,i,j]=(src[f,i-1,j]+src[f,i+1,j]+src[f,i,j+1]+roff)/3
                                elif j==c-1:
                                    dst[f,i,j]=(src[f,i-1,j]+src[f,i+1,j]+src[f,i,j-1]+roff)/3
                                else:
                                    dst[f,i,j]=(src[f,i-1,j]+src[f,i+1,j]+src[f,i,j-1]+src[f,i,j+1]+roff*2)/4
    return interpolate

def bayer_interpolate(src, off=(0,0)):
    """
    Interpolate Bayer-filtered source image.

    The algorithm is the straightforward linear nearest neighbor interpolation.
    The Bayer pattern is assume to be ``[RG|GB]``, and `off` specifies the red pixel position with respect to the image origin.
    """
    oshape=src.shape
    if src.ndim<2:
        raise ValueError("src should have at least 2 dimensions")
    if src.ndim==2:
        src=src[None,:,:]
    elif src.ndim>3:
        src=src.reshape((-1,)+src.shape[-2:])
    dst=np.zeros(src.shape+(3,),dtype=src.dtype)
    interpolate=_bayer_interpolate_nb(src.dtype,dst.dtype)
    interpolate(src,dst[:,:,:,0],ioff=off[0]%2,joff=off[1]%2,mode=0,roff=0)
    interpolate(src,dst[:,:,:,1],ioff=(off[0]+1)%2,joff=off[1]%2,mode=1,roff=0)
    interpolate(src,dst[:,:,:,2],ioff=(off[0]+1)%2,joff=(off[1]+1)%2,mode=0,roff=0)
    return dst.reshape(oshape+(3,))




def linear_to_sRGB(v, base=1, A=2.4, P=0.055):
    """
    Convert the linear sRGB color space to the sRGB.

    `base` specifies the full color range (e.g., 65535 for 16-bit color values), and `A` and `P` are the two conversion parameters.
    """
    nv=v/base
    if np.isscalar(v):
        return (nv**(1/A)*(1+P)-P)*base if nv>0 else 0
    result=(nv**(1/A)*(1+P)-P)*base
    result[nv<=0]=0
    return result
def sRGB_to_linear(v, base=1, A=2.4, P=0.055):
    """
    Convert the sRGB color space to the linear sRGB.

    `base` specifies the full color range (e.g., 65535 for 16-bit color values), and `A` and `P` are the two conversion parameters.
    """
    nv=v/base
    if np.isscalar(v):
        return ((nv+P)/(1+P))**A*base if nv>0 else 0
    result=((nv+P)/(1+P))**A*base
    result[nv<=0]=0
    return result