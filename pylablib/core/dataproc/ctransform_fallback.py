import numpy as np

_meye=np.eye(2,dtype="float")
_mt=np.array([[0,1],[1,0]])
_szero=np.zeros(2,dtype="float")
class CLinear2DTransform:
    """Pure Python implementation of Cython-based linear 2D transform"""
    def __init__(self, m=None, s=None):
        self.m=_meye.copy() if m is None else m
        self.s=_szero.copy() if s is None else s
        self._set_inv()
    
    def _set_inv(self):
        d=self.m[0,0]*self.m[1,1]-self.m[0,1]*self.m[1,0]
        self.mi=np.array([[self.m[1,1],-self.m[0,1]],[-self.m[1,0],self.m[0,0]]])/d
        self.si=np.array([-(self.mi[0,0]*self.s[0]+self.mi[0,1]*self.s[1]),-(self.mi[1,0]*self.s[0]+self.mi[1,1]*self.s[1])])
    def copy(self):
        """Copy the transform"""
        return CLinear2DTransform(self.m,self.s)
    def _multiply(self, m, preceded):
        if preceded:
            self.m=np.dot(self.m,m)
        else:
            self.m=np.dot(m,self.m)
            self.s=np.dot(m,self.s)
        self._set_inv()
    def _shift(self, s, preceded):
        if preceded:
            self.s+=np.dot(self.m,s)
        else:
            self.s+=s
        self._set_inv()
    @property
    def tmatr(self, copy=False):
        """Transform matrix as a 2x2 numpy array"""
        return self.m.copy() if copy else self.m
    @property
    def svec(self, copy=False):
        """Transform vector as a numpy array"""
        return self.s.copy() if copy else self.s

    def invert(self):
        """Invert the transform"""
        self.m=self.mi
        self.s=self.si
        self._set_inv()
        return self
    def precede(self, trans):
        """Precede the transform with a different transform"""
        self.s+=np.dot(self.m,trans.s)
        self.m=np.dot(self.m,trans.m)
        self._set_inv()
        return self
    def follow(self, trans):
        """Follow the transform with a different transform"""
        self.s=np.dot(trans.m,self.s)+self.s
        self.m=np.dot(trans.m,self.m)
        self._set_inv()
        return self

    def __call__(self, x, y):
        """Apply the transform to the given point"""
        return list(np.dot(self.m,np.array([x,y]))+self.s)
    def i(self, x,y):
        """Apply the inverse transform to the given point"""
        return list(np.dot(self.mi,np.array([x,y]))+self.si)
    
    def shift(self, s1, s2, preceded=False):
        """Apply a shift transform before or after (default) the given transform"""
        self._shift(np.array([s1,s2]),preceded)
        return self
    
    def multiply(self, m11, m12, m21, m22, preceded=False):
        """Apply a matrix multiplication transform before or after (default) the given transform"""
        self._multiply(np.array([[m11,m12],[m21,m22]]),preceded)
        return self
    def scale(self, s1, s2, preceded=False):
        """Apply a scale transform before or after (default) the given transform"""
        self._multiply(np.array([[s1,0],[0,s2]]),preceded)
        return self
    def transpose(self, preceded=False):
        """Apply a transpose transform before or after (default) the given transform"""
        self._multiply(_mt,preceded)
        return self
    
    @classmethod
    def from_matr_shift(cls, matr, shift):
        """Build a transform from a 2x2 transform matrix and a shift vector"""
        return cls(matr,shift)