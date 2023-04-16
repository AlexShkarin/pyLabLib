import cython

import numpy as np
cimport numpy as np
np.import_array()

ctypedef double _vec_t[2]
ctypedef fused vectype:
    int
    float
    double

cdef inline nptype(vectype *x=NULL):
    if vectype is int:
        return np.intc
    if vectype is double:
        return np.double
    if vectype is float:
        return np.float


@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline as_vec(vectype *v, size_t l):
    """Convert C 1D array into numpy array"""
    res=np.empty(l,dtype=nptype[vectype]())
    for i in range(l):
        res[i]=v[0]
        v+=1
    return res
@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline as_matr(vectype *v, size_t l1, size_t l2):
    """Convert C 2D array into numpy array"""
    res=np.empty((l1,l2),dtype=nptype[vectype]())
    for i in range(l1):
        for j in range(l2):
            res[i,j]=v[0]
            v+=1
    return res



cdef void _vadd(double v[2], double v2[2]):
    v2[0]+=v[0]
    v2[1]+=v[1]
cdef void _vdot(double m[2][2], double v2[2]):
    cdef double t=m[0][0]*v2[0]+m[0][1]*v2[1]
    v2[1]=m[1][0]*v2[0]+m[1][1]*v2[1]
    v2[0]=t
cdef void _mldot(double m[2][2], double m2[2][2]):
    cdef double m00=m[0][0]*m2[0][0]+m[0][1]*m2[1][0]
    cdef double m01=m[0][0]*m2[0][1]+m[0][1]*m2[1][1]
    cdef double m10=m[1][0]*m2[0][0]+m[1][1]*m2[1][0]
    cdef double m11=m[1][0]*m2[0][1]+m[1][1]*m2[1][1]
    m2[0][0]=m00
    m2[0][1]=m01
    m2[1][0]=m10
    m2[1][1]=m11
cdef void _mrdot(double m2[2][2], double m[2][2]):
    cdef double m00=m2[0][0]*m[0][0]+m2[0][1]*m[1][0]
    cdef double m01=m2[0][0]*m[0][1]+m2[0][1]*m[1][1]
    cdef double m10=m2[1][0]*m[0][0]+m2[1][1]*m[1][0]
    cdef double m11=m2[1][0]*m[0][1]+m2[1][1]*m[1][1]
    m2[0][0]=m00
    m2[0][1]=m01
    m2[1][0]=m10
    m2[1][1]=m11


cdef class CLinear2DTransform:
    """Cython-based linear 2D transform"""
    cdef double m[2][2]
    cdef double s[2]
    cdef double mi[2][2]
    cdef double si[2]
    def __cinit__(self):
        self.m[0][0]=1.
        self.m[1][1]=1.
        self.mi[0][0]=1.
        self.mi[1][1]=1.
    
    @property
    def tmatr(self):
        """Get transform matrix as a numpy array"""
        return as_matr[double](&(self.m[0][0]),2,2)
    @property
    def svec(self):
        """Get shift vector as a numpy array"""
        return as_vec(self.s,2)
    
    @cython.cdivision(True)
    cdef void _set_inv(self):
        cdef double d=self.m[0][0]*self.m[1][1]-self.m[0][1]*self.m[1][0]
        self.mi[0][0]=self.m[1][1]/d
        self.mi[0][1]=-self.m[0][1]/d
        self.mi[1][0]=-self.m[1][0]/d
        self.mi[1][1]=self.m[0][0]/d
        self.si[0]=-(self.mi[0][0]*self.s[0]+self.mi[0][1]*self.s[1])
        self.si[1]=-(self.mi[1][0]*self.s[0]+self.mi[1][1]*self.s[1])
    
    cdef CLinear2DTransform _from_ms(self, double m[2][2], double s[2]):
        r=CLinear2DTransform()
        for i in range(2):
            r.s[i]=s[i]
        for j in range(4):
            r.m[j]=m[j]
        r._set_inv()
        return r
    cpdef CLinear2DTransform copy(self):
        """Copy the transform"""
        return self._from_ms(self.m,self.s)
    cdef _multiply(self, double m[2][2], int preceded):
        if preceded:
            _mrdot(self.m,m)
        else:
            _mldot(m,self.m)
            _vdot(m,self.s)
    cdef void _shift(self, double s1, double s2, int preceded):
        if preceded:
            self.s[0]+=self.m[0][0]*s1+self.m[0][1]*s2
            self.s[1]+=self.m[1][0]*s1+self.m[1][1]*s2
        else:
            self.s[0]+=s1
            self.s[1]+=s2
        self._set_inv()

    def invert(self):
        """Invert the transform"""
        for i in range(2):
            self.s[i]=self.si[i]
            for j in range(2):
                self.m[i][j]=self.mi[i][j]
        self._set_inv()
        return self
    def precede(self, CLinear2DTransform trans):
        """Precede the transform with a different transform"""
        cdef double[2] s=[trans.s[0],trans.s[1]]
        _vdot(self.m,s)
        _vadd(s,self.s)
        _mrdot(self.m,trans.m)
        self._set_inv()
        return self
    def follow(self, CLinear2DTransform trans):
        """Follow the transform with a different transform"""
        _vdot(trans.m,self.s)
        _vadd(trans.s,self.s)
        _mldot(trans.m,self.m)
        self._set_inv()
        return self

    def __call__(self, double x, double y):
        """Apply the transform to the given point"""
        cdef double[2] vec=[x,y]
        _vdot(self.m,vec)
        vec[0]+=self.s[0]
        vec[1]+=self.s[1]
        return vec
    def i(self, double x, double y):
        """Apply the inverse transform to the given point"""
        cdef double[2] vec=[x,y]
        _vdot(self.mi,vec)
        vec[0]+=self.si[0]
        vec[1]+=self.si[1]
        return vec
    
    def shift(self, double s1, double s2, int preceded=False):
        """Apply a shift transform before or after (default) the given transform"""
        self._shift(s1,s2,preceded)
        return self
    
    def scale(self, double s1, double s2, int preceded=False):
        """Apply a scale transform before or after (default) the given transform"""
        self._multiply([[s1,0],[0,s2]],preceded)
        self._set_inv()
        return self
    def transpose(self, preceded=False):
        """Apply a transpose transform before or after (default) the given transform"""
        self._multiply([[0,1],[1,0]],preceded)
        self._set_inv()
        return self