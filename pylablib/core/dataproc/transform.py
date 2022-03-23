import numpy as np



class LinearTransform:
    """
    A generic linear transform which combines an affine transform with a given matrix and an additional shift.

    Args:
        tmatr: translational matrix (if ``None``, use a unity matrix)
        shift: added shift (if ``None``, use a zero shift)
        ndim: if both `tmatr` and `shift` are ``None``, specifies the dimensionality of the transform; otherwise, ignored
    """
    def __init__(self, tmatr=None, shift=None, ndim=2):
        tmatr=np.asarray(tmatr) if tmatr is not None else None
        shift=np.asarray(shift) if shift is not None else None
        if tmatr is not None:
            ndim=tmatr.shape[0]
        elif shift is not None:
            ndim=shift.shape[0]
        self.tmatr=tmatr if tmatr is not None else np.eye(ndim)
        self.shift=shift if shift is not None else np.zeros(ndim)
        if self.tmatr.ndim!=2 or self.tmatr.shape[0]!=self.tmatr.shape[1]:
            raise ValueError("transformation matrix should be a 2D square array")
        if self.shift.ndim!=1:
            raise ValueError("shift should be a 1D array")
        if self.tmatr.shape[0]!=self.shift.shape[0]:
            raise ValueError("transformation matrix and shift should have the same size")
    
    def _build_new(self, tmatr, shift):
        return type(self)(tmatr,shift)
    def __call__(self, coord, shift=True):
        coord=np.asarray(coord)
        return np.dot(self.tmatr,coord)+self.shift if shift else np.dot(self.tmatr,coord)
    def i(self, coord, shift=True):
        tmatr=np.linalg.inv(self.tmatr)
        return np.dot(tmatr,coord)-np.dot(tmatr,self.shift) if shift else np.dot(tmatr,coord)
    def _check_ndim(self, ndims):
        if self.tmatr.shape[0] not in ndims:
            raise ValueError("method only applies to dimensions {}".format(ndims))
    
    def inverted(self):
        """Return inverted transformation"""
        tmatr=np.linalg.inv(self.tmatr)
        shift=-np.dot(tmatr,self.shift)
        return self._build_new(tmatr,shift)
    def preceded(self, trans):
        """Return a combined transformation which result from applying this transformation followed by `trans`"""
        return trans.followed(self)
    def followed(self, trans):
        """Return a combined transformation which result from applying `trans` followed by this transformation"""
        tmatr=np.dot(trans.tmatr,self.tmatr)
        shift=trans.shift+np.dot(trans.tmatr,self.shift)
        return self._build_new(tmatr,shift)
    def _combined(self, trans, preceded):
        return self.preceded(trans) if preceded else self.followed(trans)
    
    def shifted(self, shift, preceded=False):
        """Return a transform with an added shift before or after (depending of `preceded`) the current one"""
        return self._combined(LinearTransform(shift=shift),preceded)
    def multiplied(self, mult, preceded=False):
        """
        Return a transform with an added scaling before or after (depending of `preceded`) the current one.

        `mult` can be a single number (scale), a 1D vector (scaling for each axis independently), or a matrix.
        """
        if np.ndim(mult)==0:
            tmatr=np.eye(self.tmatr.shape[0])*mult
        elif np.ndim(mult)==1:
            tmatr=np.diag(mult)
        else:
            tmatr=np.asarray(mult)
        return self._combined(LinearTransform(tmatr),preceded)
    def rotated2d(self, deg, preceded=False):
        """
        Return a transform with an added rotation before or after (depending of `preceded`) the current one.

        Only applies to 2D transforms.
        """
        self._check_ndim(2)
        rad=deg*np.pi/180
        tmatr=[[np.cos(rad),-np.sin(rad)],[np.sin(rad),np.cos(rad)]]
        return self.multiplied(tmatr,preceded=preceded)




class Indexed2DTransform(LinearTransform):
    """
    A restriction of :class:`LinearTransform` which only applies to 2D and only allows rotations by multiples of 90 degrees.

    Args:
        tmatr: translational matrix (if ``None``, use a unity matrix)
        shift: added shift (if ``None``, use a zero shift)
        rigid: if ``True``, only allow orthogonal transforms, i.e., no scaling
    """
    def __init__(self, tmatr=None, shift=None, rigid=False):
        super().__init__(tmatr=tmatr,shift=shift,ndim=2)
        self.rigid=rigid
        self._check_tmatr()
    def _check_tmatr(self):
        if self.tmatr.shape[0]!=2:
            raise ValueError("only 2D transform are allowed")
        if not (self.tmatr[0,0]==self.tmatr[1,1]==0 or self.tmatr[0,1]==self.tmatr[1,0]==0):
            raise ValueError("only 90 degree rotations and inversions are allowed")
        if self.rigid:
            pmatr=np.dot(self.tmatr.T,self.tmatr)
            if not np.all(pmatr==np.eye(2)):
                raise ValueError("only orthogonal transformations are allowed")
    def _build_new(self, tmatr, shift):
        return type(self)(tmatr,shift,rigid=self.rigid)
    def rotated2d(self, deg, preceded=False):
        deg=deg%360
        if deg%90!=0:
            raise ValueError("only 90 degree rotations are allowed")
        if deg==0:
            tmatr=[[1,0],[0,1]]
        elif deg==90:
            tmatr=[[0,-1],[1,0]]
        elif deg==180:
            tmatr=[[-1,0],[0,-1]]
        else:
            tmatr=[[0,1],[-1,0]]
        return self.multiplied(tmatr,preceded=preceded)