"""
Contains utilities for simplifying emulation of numerical classes.
"""

from __future__ import division


def iadd(a, b):
    a+=b
    return a
def isub(a, b):
    a-=b
    return a
def imul(a, b):
    a*=b
    return a
def idiv(a, b):
    a/=b
    return a
def ipow(a, b):
    a**=b
    return a
def ifloordiv(a, b):
    a//=b
    return a
def imod(a, b):
    a%=b
    return a
def ilshift(a, b):
    a<<=b
    return a
def irshift(a, b):
    a>>=b
    return a
def iand(a, b):
    a&=b
    return a
def ior(a, b):
    a|=b
    return a
def ixor(a, b):
    a^=b
    return a


class NumClass(object):
    """
    Simplifies numerical class emulation.
    
    Defines all of the built-in arithmetic functions and generic methods for handling them.
    
    The most generic method is
    
    .. automethod:: _perform_numop
    
    The other more specialized methods are (by default they all invoke :meth:`_perform_numop`):
    
    Methods:
        _perform_numop_l: Binary operations with the object as the first argument (e.g., ``obj + x``).
        _perform_numop_r: Binary operations with the object as the second argument (e.g., ``x + obj``).
        _perform_numop_i: Binary in-place operations (e.g., ``obj += x``).
        _perform_numop_u: Unary operations (e.g., ``-obj``).
        _perform_numop_comp: Binary comparison operation (e.g., ``obj < x``).
        
    A class-level set `_numops_impl` contains symbols for operations which are implemented.
    By default, the operations not contained in `_numops_impl` raise :exc:`NotImplementedError`.
        
    The operation symbols are:
        - arithmetic binary operations with the object as the first argument:
            ``'l+'``, ``'l-'``, ``'l*'``, ``'l/'``, ``'l**'``, ``'l//'``, ``'l%'``
            (contained in constant `_numops_arith_l`)
        - arithmetic binary operations with the object as the second argument:
            ``'r+'``, ``'r-'``, ``'r*'``, ``'r/'``, ``'r**'``, ``'r//'``, ``'r%'``
            (contained in constant `_numops_arith_r`)
        - arithmetic binary in-place operations:
            ``'i+'``, ``'i-'``, ``'i*'``, ``'i/'``, ``'i**'``, ``'i//'``, ``'i%'``
            (contained in constant `_numops_arith_i`)
        - arithmetic unary operations:
            ``'u+'``, ``'u-'``, ``'uabs'``
            (contained in constant `_numops_arith_u`)
        - bitwise binary operations with the object as the first argument:
            ``'l<<'``, ``'l>>'``, ``'l&'``, ``'l|'``, ``'l^'``
            (contained in constant `_numops_bitwise_l`)
        - bitwise binary operations with the object as the second argument:
            ``'r<<'``, ``'r>>'``, ``'r&'``, ``'r|'``, ``'r^'``
            (contained in constant `_numops_bitwise_r`)
        - bitwise binary in-place operations:
            ``'i<<'``, ``'i>>'``, ``'i&'``, ``'i|'``, ``'i^'``
            (contained in constant `_numops_bitwise_i`)
        - bitwise unary operations:
            ``'u~'``
            (contained in constant `_numops_bitwise_u`)
        - comparison operations:
            ``'<'``, ``'<='``, ``'>'``, ``'>='``, ``'=='``, ``'!='``
            (contained in constant `_numpos_comp`)
    """
    _numops_impl=set()
    
    
    _numops_arith_l={"l+","l-","l*","l/","l**","l//","l%"}
    _numops_arith_r={"r+","r-","r*","r/","r**","r//","r%"}
    _numops_arith_i={"i+","i-","i*","i/","i**","i//","i%"}
    _numops_arith_u={"u+","u-","uabs"}
    _numops_bitwise_l={"l<<","l>>","l&","l|","l^"}
    _numops_bitwise_r={"r<<","r>>","r&","r|","r^"}
    _numops_bitwise_i={"i<<","i>>","i&","i|","i^"}
    _numops_bitwise_u={"u~"}
    _numpos_comp={"<","<=","==","!=",">",">="}
    _numops_l=set.union(_numops_arith_l,_numops_bitwise_l)
    _numops_r=set.union(_numops_arith_r,_numops_bitwise_r)
    _numops_i=set.union(_numops_arith_i,_numops_bitwise_i)
    _numops_arith=set.union(_numops_arith_l,_numops_arith_r,_numops_arith_i,_numops_arith_u)
    _numops_bitwise=set.union(_numops_bitwise_l,_numops_bitwise_r,_numops_bitwise_i,_numops_bitwise_u)
    _numops_all=set.union(_numops_arith,_numops_bitwise,_numpos_comp)
    
    
    def _perform_numop(self, x, op_func, op_sym):
        """
        Perform a numeric operation.
        
        Abstract method, has to be overloaded in subclasses.
        
        Args:
            x: A second argument (``None`` if the operation is unary).
            op_func (callable): A default function which performs the operation
                (e.g., ``lambda (x, y): x + y`` for addition).
            op_sym (str): A symbol for the operation. 
        """
        raise NotImplementedError("NumClass._perform_numop")
    def _perform_numop_l(self, x, op_func, op_sym):
        """_perform_numop_l docstring"""
        return self._perform_numop(x,op_func,op_sym)
    def _perform_numop_r(self, x, op_func, op_sym):
        return self._perform_numop(x,op_func,op_sym)
    def _perform_numop_i(self, x, op_func, op_sym):
        return self._perform_numop(x,op_func,op_sym)
    def _perform_numop_u(self, op_func, op_sym):
        return self._perform_numop(None,op_func,op_sym)
    def _perform_numop_comp(self, x, op_func, op_sym):
        return self._perform_numop(x,op_func,op_sym)
    
    def _test_op_impl(self, op_sym):
        if not op_sym in self._numops_impl:
            raise NotImplementedError("{}.{}".format(type(self).__name__,op_sym))
    
    def _call_numop_l(self, x, op_func, op_sym):
        self._test_op_impl(op_sym)
        return self._perform_numop_l(x,op_func,op_sym)
    def _call_numop_r(self, x, op_func, op_sym):
        self._test_op_impl(op_sym)
        return self._perform_numop_r(x,op_func,op_sym)
    def _call_numop_i(self, x, op_func, op_sym):
        self._test_op_impl(op_sym)
        return self._perform_numop_i(x,op_func,op_sym)
    def _call_numop_u(self, op_func, op_sym):
        self._test_op_impl(op_sym)
        return self._perform_numop_u(op_func,op_sym)
    def _call_numop_comp(self, x, op_func, op_sym):
        self._test_op_impl(op_sym)
        return self._perform_numop_comp(x,op_func,op_sym)
            
            
            
    def __add__(self, x): return self._call_numop_l(x,lambda a,b: a+b, "l+")
    def __sub__(self, x): return self._call_numop_l(x,lambda a,b: a-b, "l-")
    def __mul__(self, x): return self._call_numop_l(x,lambda a,b: a*b, "l*")
    def __div__(self, x): return self._call_numop_l(x,lambda a,b: a/b, "l/")
    __truediv__=__div__
    def __pow__(self, x): return self._call_numop_l(x,lambda a,b: a**b, "l**")
    def __floordiv__(self, x): return self._call_numop_l(x,lambda a,b: a//b, "l//")
    def __mod__(self, x): return self._call_numop_l(x,lambda a,b: a%b, "l%")
    def __divmod__(self, x):  return (self.__floordiv__(x), self.__mod__(x))
    
    def __radd__(self, x): return self._call_numop_r(x,lambda a,b: b+a, "r+")
    def __rsub__(self, x): return self._call_numop_r(x,lambda a,b: b-a, "r-")
    def __rmul__(self, x): return self._call_numop_r(x,lambda a,b: b*a, "r*")
    def __rdiv__(self, x): return self._call_numop_r(x,lambda a,b: b/a, "r/")
    __rtruediv__=__rdiv__
    def __rpow__(self, x): return self._call_numop_r(x,lambda a,b: b**a, "r**")
    def __rfloordiv__(self, x): return self._call_numop_r(x,lambda a,b: b//a, "r//")
    def __rmod__(self, x): return self._call_numop_r(x,lambda a,b: b%a, "r%")
    def __rdivmod__(self, x):  return (self.__rfloordiv__(x), self.__rmod__(x))
    
    def __iadd__(self, x): return self._call_numop_i(x,iadd, "i+")
    def __isub__(self, x): return self._call_numop_i(x,isub, "i-")
    def __imul__(self, x): return self._call_numop_i(x,imul, "i*")
    def __idiv__(self, x): return self._call_numop_i(x,idiv, "i/")
    __itruediv__=__idiv__
    def __ipow__(self, x): return self._call_numop_i(x,ipow, "i**")
    def __ifloordiv__(self, x): return self._call_numop_i(x,ifloordiv, "i//")
    def __imod__(self, x): return self._call_numop_i(x,imod, "i%")
    
    def __pos__(self): return self._call_numop_u(lambda a,_=None: +a, "u+")
    def __neg__(self): return self._call_numop_u(lambda a,_=None: -a, "u-")
    def __abs__(self): return self._call_numop_u(lambda a,_=None: abs(a), "uabs")
    
    def __lshift__(self, x): return self._call_numop_l(x,lambda a,b: a<<b, "l<<")
    def __rshift__(self, x): return self._call_numop_l(x,lambda a,b: a>>b, "l>>")
    def __and__(self, x): return self._call_numop_l(x,lambda a,b: a&b, "l&")
    def __or__(self, x): return self._call_numop_l(x,lambda a,b: a|b, "l|")
    def __xor__(self, x): return self._call_numop_l(x,lambda a,b: a^b, "l^")
    
    def __rlshift__(self, x): return self._call_numop_r(x,lambda a,b: b<<a, "r<<")
    def __rrshift__(self, x): return self._call_numop_r(x,lambda a,b: b>>a, "r>>")
    def __rand__(self, x): return self._call_numop_r(x,lambda a,b: b&a, "r&")
    def __ror__(self, x): return self._call_numop_r(x,lambda a,b: b|a, "r|")
    def __rxor__(self, x): return self._call_numop_r(x,lambda a,b: b^a, "r^")
    
    def __ilshift__(self, x): return self._call_numop_i(x,ilshift, "i<<")
    def __irshift__(self, x): return self._call_numop_i(x,irshift, "i>>")
    def __iand__(self, x): return self._call_numop_i(x,iand, "i&")
    def __ior__(self, x): return self._call_numop_i(x,ior, "i|")
    def __ixor__(self, x): return self._call_numop_i(x,ixor, "i^")
    
    def __invert__(self): return self._call_numop_u(lambda a,_=None: ~a, "u~")
    
    def __lt__(self, x): return self._call_numop_comp(x,lambda a,b: a< b, "<")
    def __le__(self, x): return self._call_numop_comp(x,lambda a,b: a<=b, "<=")
    def __eq__(self, x): return self._call_numop_comp(x,lambda a,b: a==b, "==")
    def __ne__(self, x): return self._call_numop_comp(x,lambda a,b: a!=b, "!=")
    def __gt__(self, x): return self._call_numop_comp(x,lambda a,b: a> b, ">")
    def __ge__(self, x): return self._call_numop_comp(x,lambda a,b: a>=b, ">=")