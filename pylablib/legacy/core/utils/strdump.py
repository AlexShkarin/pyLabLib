"""
Utils for converting variables into standard python objects (lists, dictionaries, strings, etc.) and back (e.g., for a more predictable LAN transfer).
Provides an extension for pickle for more customized classes (numpy arrays, Datatable, Dictionary).
"""

from future.utils import viewitems

import pickle
import collections

import numpy as np

class StrDumper(object):
    """
    Class for dumping and loading an object.
    
    Stores procedures for dumping and loading, i.e.,
    conversion from complex classes (such as :class:`.Dictionary`) to simple built-in classes (such as :class:`dict` or :class:`str`).
    """
    def __init__(self):
        object.__init__(self)
        self._classes={}
        self.add_class(tuple,name="t",loadf=lambda t: tuple(self.load(v) for v in t)) # to distinguish from packed value tuples
    
    _ClassRecord=collections.namedtuple("_ClassRecord",["cls","dump","load","allow_subclass","recursive"])
    def add_class(self, cls, dumpf=None, loadf=None, name=None, allow_subclass=True, recursive=False):
        """
        Add a rule for dumping/loading an object of class `cls`.
        
        Args:
            cls
            dumpf (callable): Function for dumping an object of the class; ``None`` means identity function.
            loadf (callable): Function for loading an object of the class; ``None`` means identity function.
            name (str): Name of class, which is stored in the packed data (``cls.__name__`` by default).
            allow_subclass (bool): If ``True``, this rule is also used for subclasses of this class.
            recursive (bool): If ``True``, the functions are given a second argument, which is a dumping/loading function for their sub-elements.
        """
        if name is None:
            name=cls.__name__
        if name in self._classes:
            raise ValueError("class {} is already registered".format(name))
        self._classes[name]=self._ClassRecord(cls,dumpf,loadf,allow_subclass,recursive)
        
    def _find_cls(self, obj):
        ocls=type(object)
        found=None
        for n,v in viewitems(self._classes):
            cls=v.cls
            if v.allow_subclass:
                sat=isinstance(obj,cls)
            else:
                sat=(ocls is cls)
            if sat:
                if found is None:
                    found=n,cls
                elif issubclass(cls,found[1]):
                    found=n,cls
                elif not issubclass(found[1],cls):
                    raise ValueError("both {} and {} satisfy for a base class of {}".format(n,found[0],obj))
        return None if found is None else found[0]
    
    def _dump_recursive(self, value):
        if isinstance(value,tuple):
            return tuple(self.dump(v) for v in value)
        elif isinstance(value,list):
            return list(self.dump(v) for v in value)
        elif isinstance(value,dict):
            return dict([(k,self.dump(v)) for k,v in viewitems(value)])
        return value
    def dump(self, obj):
        """
        Convert an object into a dumped value.
        """
        obj=self._dump_recursive(obj)
        reg=self._find_cls(obj)
        if reg is None:
            return obj
        else:
            cls=self._classes[reg]
            if cls.dump is None:
                value=obj
            elif not cls.recursive:
                value=cls.dump(obj)
            else:
                value=cls.dump(obj,self.dump)
            return (reg,value)
    
    def _load_recursive(self, obj):
        if isinstance(obj,tuple):
            return tuple(self.load(v) for v in obj)
        if isinstance(obj,list):
            return list(self.load(v) for v in obj)
        if isinstance(obj,dict):
            return dict([(k,self.load(v)) for k,v in viewitems(obj)])
        return obj
    def load(self, obj):
        """
        Convert a dumped value into an object.
        """
        if not isinstance(obj,tuple):
            return self._load_recursive(obj)
        name,value=obj
        if name in self._classes:
            cls=self._classes[name]
            if cls.load is None:
                return value
            elif not cls.recursive:
                return cls.load(value)
            else:
                return cls.load(value,self.load)
        else:
            raise KeyError("class {} is not registered".format(name))
        
    def loads(self, s):
        """
        Convert a pickled string of a damped object into an object.
        """
        value=pickle.loads(s)
        return self.load(value)
    def dumps(self, obj):
        """
        Dumps an object into a pickled string.
        """
        value=self.dump(obj)
        return pickle.dumps(value,protocol=-1)
    
    
dumper=StrDumper()
"""
Default dumper for converting  into standard Python classes and pickling.

Converts :class:`numpy.ndarray`, :class:`.Dictionary` and :class:`.DataTable` objects
(these conversion routines are defined when corresponding modules are imported).
The converted values include non-printable characters (conversion uses :func:`numpy.ma.loads` and :func:`numpy.ma.dumps`),
so they can't be saved into text files. However, they're suited for pickling.
"""


### Numpy array ###
dumper.add_class(np.ndarray,np.ndarray.dumps,np.loads,"np")



def dump(obj):
    """
    Convert obj into standard Python classes using default dumper.
    """
    return dumper.dump(obj)
def load(s):
    """
    Convert standard Python class representation `s` into an object using default dumper.
    """
    return dumper.load(s)

def dumps(obj):
    """
    Convert obj into a pickled string using default dumper.
    """
    return dumper.dumps(obj)
def loads(s):
    """
    Convert a pickled string into an object. using default dumper
    """
    return dumper.loads(s)