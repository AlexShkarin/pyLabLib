"""
Numerical functions that don't deal with sequences (those are contained in waveforms.general).
"""
from __future__ import division
from builtins import range

import math

def gcd(*numbers):
    """Euclid's algorithm for GCD. Arguments are cast to integer."""
    def gcd2(a,b):
        a=abs(int(a))
        b=abs(int(b))
        a,b = max(a,b), min(a,b)
        while b>0:
            a,b=b,a%b
        return a
    if len(numbers)==0:
        return 1
    res=numbers[0]
    for n in numbers[1:]:
        res=gcd2(n,res)
    return res
        
def integer_distance(x):
    """Get distance to the closes integer"""
    return abs(x-round(x))

def gcd_approx(a, b, min_fraction=1E-8, tolerance=1E-5):
    """
    Approximate Euclid's algorithm for possible non-integer values.
    
    Try to find a number `d` such that ``a/d`` and ``b/d`` are less than `tolerance` away from a closest integer.
    If GCD becomes less than ``min_fraction * min(a, b)``, raise :exc:`ArithmeticError`.
    """
    a=abs(a)
    b=abs(b)
    a,b = max(a,b), min(a,b)
    a0,b0 = a,b
    if b==0:
        raise ArithmeticError("Can't find GCD if one of numbers is 0")
    min_gcd=b*min_fraction
    while b>=min_gcd:
        if (integer_distance(a0/b)+integer_distance(b0/b))<=tolerance:
            return b
        a,b = b,a%b
    raise ArithmeticError("Can't find approximate GCD for numbers",a0,b0)


def round_significant(x, n):
    """
    Rounds `x` to `n` significant digits (not the same as `n` decimal places!).
    """
    if x==0.:
        return 0.
    exp10=10**int(math.ceil(math.log10(abs(x))))
    return exp10*round(x/exp10,n)



def limit_to_range(x, min_val=None, max_val=None, default=0):
    """
    Confine `x` to the given limit.
    
    Default limit values are ``None``, which means no limit.
    """
    if (min_val is None) and (max_val is None):
        return x if x is not None else default
    if min_val is None:
        return min(max_val,x) if x is not None else max_val
    if max_val is None:
        return max(min_val,x) if x is not None else min_val
    return sorted([min_val,x,max_val])[1] if x is not None else (max_val+min_val)/2.


class infinite_list(object):
    """
    Mimics the behavior of the usual list, but is infinite and immutable.
    
    Supports accessing elements, slicing (including slices giving infinite lists) and iterating. 
    Iterating over it naturally leads to an infinite loop, so it should only be used either for finite slices or for loops with break condition.
    
    Args:
        start: The first element of the list.
        step: List step. 
    """
    def __init__(self, start=0, step=1):
        object.__init__(self)
        self.start=start
        self.step=step
    def __len__(self):
        raise ValueError("Can't express length of an infinite list")
    def __getitem__(self, idx):
        if isinstance(idx,slice):
            start,stop,step=idx.start,idx.stop,idx.step
            if step is None:
                step=1
            if step==0:
                raise ValueError("Slice step can't be zero")
            if stop is None:
                stop=-1
            if step<0:
                if start is None or start<0:
                    raise ValueError("Can't reverse infinite list")
                return [self[i] for i in range(start,stop,step)]
            else:
                if start is None:
                    start=0
                if stop<0:
                    return infinite_list(self[start],self.step*step)
                else:
                    return [self[i] for i in range(start,stop,step)]
        else:
            if idx<0:
                raise ValueError("Can't access tail element of an infinite list")
            return self.start+self.step*idx
    def __setitem__(self, *args):
        raise ValueError("Can't change element of an immutable list")
    def __delitem__(self, *args):
        raise ValueError("Can't delete element of an immutable list")
    def __contains__(self, value):
        if self.step==0:
            return value==self.start
        else:
            return ((value-self.start)*self.step>=0) and ((value-self.start)%self.step==0)
        
    class counter(object):
        def __init__(self, lst):
            object.__init__(self)
            self.lst=lst
            self.idx=0
        def __iter__(self):
            return self
        def __next__(self):
            elt=self.lst[self.idx]
            self.idx=self.idx+1
            return elt
        next=__next__
    def __iter__(self):
        return self.counter(self)
    
    def __str__(self):
        return "[{0}, {1}, {2}, ...]".format(self[0],self[1],self[2])
    def __repr__(self):
        return "infinite_list("+str(self)+")"
    
    
    
### Various arithmetic functions for map/sort routines.
def unity():
    """Return a unity function"""
    return lambda x:x

def constant(c):
    """
    Return a function which returns a constant `c`.
    
    `c` can only be either a scalar, or an array-like object with the shape matching the expected argument.
    """
    return lambda x:x*0+c

def polynomial(coeffs):
    """
    Return a polynomial function which with coefficients `coeffs`.
    
    Coefficients are list lowest-order first, so that ``coeffs[i]`` is the coefficient in front of ``x**i``.
    """
    if len(coeffs)==0:
        return lambda x:x*0
    def f(x):
        y=(x*0)+coeffs[0]
        for p,c in enumerate(coeffs[1:]):
            y=y+c*x**(p+1)
        return y
    return f