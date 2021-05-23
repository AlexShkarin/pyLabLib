"""
Class for building common iterators
"""

class AccessIterator(object):
    """
    Simple sequential access iterator with customizable access function (by default it's 1D indexing).
    
    Determines end of iterations by :exc:`IndexError`.
    
    Args:
        obj: Container to be iterated over.
        access_function (callable): A function which takes two parameteres `obj` and `idx`
            and either returns the element or raises :exc:`IndexError`. By default, a simple ``__getitem__`` operation.
    """
    def __init__(self, obj, access_function=None):
        object.__init__(self)
        self.obj=obj
        self.idx=0
        if access_function is None:
            access_function=lambda obj, idx: obj[idx]
        self.access_function=access_function
    def __iter__(self):
        return self
    def __next__(self):
        try:
            result=self.access_function(self.obj,self.idx)
            self.idx=self.idx+1
            return result
        except IndexError:
            raise StopIteration()
    next=__next__