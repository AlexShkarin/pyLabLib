import numpy as np
from ..utils import funcargparse


_default_indexing={"rc":"rcb","xy":"xyt"}
def convert_shape_indexing(shape, src, dst):
    """
    Convert image indexing style.

    `shape` is the source image shape (2-tuple), `src` and `dst` are current format and desired format.
    Formats can be ``"rcb"`` (first index is row, second is column, rows count from the bottom), ``"rct"`` (same, but rows count from the top).
    ``"xyb"`` (first index is column, second is row, rows count from the bottom), or ``"xyt"`` (same but rows count form the top).
    ``"rc"`` is interpreted as ``"rct"``, ``"xy"`` as ``"xyt"``
    """
    src=_default_indexing.get(src,src)
    dst=_default_indexing.get(dst,dst)
    funcargparse.check_parameter_range(src,"src",["rcb","rct","xyb","xyt"])
    funcargparse.check_parameter_range(dst,"dst",["rcb","rct","xyb","xyt"])
    if src[:2]==dst[:2]:
        return shape
    else:
        return shape[::-1]
    

def convert_image_indexing(img, src, dst):
    """
    Convert image indexing style.

    `img` is the source image (2D numpy array), `src` and `dst` are current format and desired format.
    Formats can be ``"rcb"`` (first index is row, second is column, rows count from the bottom), ``"rct"`` (same, but rows count from the top).
    ``"xyb"`` (first index is column, second is row, rows count from the bottom), or ``"xyt"`` (same but rows count form the top).
    ``"rc"`` is interpreted as ``"rct"``, ``"xy"`` as ``"xyt"``
    """
    src=_default_indexing.get(src,src)
    dst=_default_indexing.get(dst,dst)
    funcargparse.check_parameter_range(src,"src",["rcb","rct","xyb","xyt"])
    funcargparse.check_parameter_range(dst,"dst",["rcb","rct","xyb","xyt"])
    if src==dst:
        return img
    if src[:2]==dst[:2]: # same order, different row direction
        return img[::-1,:] if src[:2]=="rc" else img[:,::-1]
    if src[2]==dst[2]: # same row direction, different order
        if src[2]=="t":
            return img.T
        if src=="rcb":
            return (img[::-1,:].T)[:,::-1]
        else:
            return (img[:,::-1].T)[::-1,:]
    # different row direction, different order
    if src=="rcb": # dst=="xyt"
        return img[::-1,:].T
    if src=="rct": # dst=="xyb"
        return img.T[:,::-1]
    if src=="xyb": # dst=="rct"
        return img[:,::-1].T
    if src=="xyt": # dst=="rcb"
        return img.T[::-1,:]
    

class ROI(object):
    def __init__(self, imin=0, imax=None, jmin=0, jmax=None):
        object.__init__(self)
        self.imin=imin
        self.imax=imax
        self.jmin=jmin
        self.jmax=jmax
        self._order()

    def _order(self):
        if self.imax is not None:
            self.imin,self.imax=sorted((self.imin,self.imax))
        if self.jmax is not None:
            self.jmin,self.jmax=sorted((self.jmin,self.jmax))
    def _get_limited(self, shape=None):
        if shape is None:
            if self.imax is None or self.jmax is None:
                raise ValueError("one of the ROI dimensions is unconstrained")
            return self.imin,self.imax,self.jmin,self.jmax
        imin=max(self.imin,0)
        imax=shape[0] if self.imax is None else min(self.imax,shape[0])
        jmin=max(self.jmin,0)
        jmax=shape[1] if self.jmax is None else min(self.jmax,shape[1])
        return sorted((imin,imax))+sorted((jmin,jmax))

    def copy(self):
        return ROI(self.imin,self.imax,self.jmin,self.jmax)
    def __repr__(self):
        return "{}{}".format(self.__class__.__name__,self.tup())

    def center(self, shape=None):
        imin,imax,jmin,jmax=self._get_limited(shape)
        return (imin+imax)/2, (jmin+jmax)/2
    def size(self, shape=None):
        imin,imax,jmin,jmax=self._get_limited(shape)
        return (imax-imin), (jmax-jmin)
    def area(self, shape=None):
        size=self.size(shape)
        return size[0]*size[1]
    def tup(self, shape=None):
        return self._get_limited(shape)
    def ispan(self, shape=None):
        return self.tup(shape)[0:2]
    def jspan(self, shape=None):
        return self.tup(shape)[2:4]

    @classmethod
    def from_centersize(cls, center, size, shape=None):
        size=funcargparse.as_sequence(size,2)
        imin,imax=int(round(center[0]-abs(size[0])/2)),int(round(center[0]+abs(size[0])/2))
        jmin,jmax=int(round(center[1]-abs(size[1])/2)),int(round(center[1]+abs(size[1])/2))
        res=cls(imin,imax,jmin,jmax)
        if shape is not None:
            res.limit(shape)
        return res

    @classmethod
    def intersect(cls, *args):
        imin=max(r.imin for r in args)
        imax=min(r.imax for r in args)
        jmin=max(r.jmin for r in args)
        jmax=min(r.jmax for r in args)
        if imin>=imax or jmin>=jmax:
            return None
        return cls(imin,imax,jmin,jmax)

    def limit(self, shape):
        self.imin,self.imax,self.jmin,self.jmax=self._get_limited(shape)
        return self


def get_region(image, center, size, axis=(-2,-1)):
    """
    Get part of the image with the given center and size (both are tuples ``(i, j)``).

    The region is automatically reduced if a part of it is outside of the image.
    """
    roi=ROI.from_centersize(center,size,shape=(image.shape[axis[0]],image.shape[axis[1]]))
    ispan,jspan=roi.ispan(),roi.jspan()
    index=[slice(None)]*image.ndim
    index[axis[0]]=slice(ispan[0],ispan[1])
    index[axis[1]]=slice(jspan[0],jspan[1])
    return image[tuple(index)]

def get_region_sum(image, center, size, axis=(-2,-1)):
    """
    Sum part of the image with the given center and size (both are tuples ``(i, j)``).
    
    The region is automatically reduced if a part of it is outside of the image.
    Return tuple ``(sum, area)``, where area is the actual summer region are (in pixels).
    """
    roi=ROI.from_centersize(center,size,shape=(image.shape[axis[0]],image.shape[axis[1]]))
    ispan,jspan=roi.ispan(),roi.jspan()
    index=[slice(None)]*image.ndim
    index[axis[0]]=slice(ispan[0],ispan[1])
    index[axis[1]]=slice(jspan[0],jspan[1])
    return np.sum(image[tuple(index)],axis=axis), roi.area()