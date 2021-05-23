"""
Library for binary data encoding/decoding for device communication.
"""


import numpy as np
import re

from ..utils import py3

class DataFormat(object):
    """
    Describes data encoding for device communications.
    
    Args:
        size (int): Size of a single element (in bytes).
        kind (str): Kind of the element. Can be
            ``'i'`` (integer), ``'u'`` (unsigned integer), ``'f'`` (floating point) or ``'ascii'`` (text representation).
        byteorder (str): Byte order: ``'>'`` is big-endian (MSB first), ``'>'`` is little-endian (LSB first). 
    """
    _native_byteorder="<"
    def __init__(self, size, kind, byteorder):
        object.__init__(self)
        self.size=size and int(size)
        self.kind=kind
        self.byteorder=byteorder
    
    def flip_byteorder(self):
        """Flip byteorder of the description."""
        if self.byteorder is not None:
            self.byteorder="<" if self.byteorder==">" else ">"
    
    def is_ascii(self):
        """Check of the format is textual."""
        return self.kind=="ascii"
    @staticmethod
    def from_desc(desc, str_type="numpy"):
        """
        Build the format from the string description.
        
        `str_type` is the description format. Can be
        ``'numpy'`` (numpy dtype description),
        ``'struct'`` (:mod:`struct` description) or
        ``'SCPI'`` (the standard SCPI description).
        """
        if isinstance(desc, DataFormat):
            return desc
        if desc.lower()=="ascii":
            return DataFormat(None,"ascii",None)
        if str_type=="numpy":
            dtype=np.dtype(desc)
            if not dtype.kind in "uif":
                raise ValueError("can't describe data format: {0}".format(desc))
            byteorder=DataFormat._native_byteorder if dtype.byteorder in "=|" else dtype.byteorder
            return DataFormat(dtype.itemsize,dtype.kind,byteorder)
        elif str_type=="struct":
            if desc[:1]=="@":
                desc="="+desc[1:]
            return DataFormat.from_desc(desc,"numpy")
        elif str_type=="SCPI":
            return DataFormat.from_desc_SCPI(desc)
        else:
            raise ValueError("unrecognized format type: {0}".format(str_type))
    @staticmethod
    def from_desc_SCPI(desc, border="norm"):
        """
        Build the format from the string SCPI description.
        
        `border` describes byte order (either ``'norm'`` or ``'swap'``). 
        """
        desc=desc.lower().strip()
        border=border.lower().strip()[:4]
        if border=="norm":
            byteorder=">"
        elif border=="swap":
            byteorder="<"
        else:
            raise ValueError("unrecognized SCPI border: {0}".format(border))
        if desc[:3]=="asc":
            # split_desc=desc.split(",")
            # if len(desc)>=2:
            #     size=int(desc[1])
            # else:
            #     size=None
            # return DataFormat(size,"ascii",None)
            return DataFormat(None,"ascii",None)
        split_desc=desc.split(",")
        if len(split_desc)<2:
            raise ValueError("can't determine SCPI format: {0}".format(desc))
        bitlen=int(split_desc[1])
        if bitlen%8!=0 or bitlen==0:
            raise ValueError("wrong bitlength in SCPI format: {0}".format(desc))
        if desc[:4]=="real":
            kind="f"
        elif desc[:3]=="int":
            kind="i"
        else:
            raise ValueError("can't determine SCPI format: {0}".format(desc))
        return DataFormat(bitlen//8,kind,byteorder)
    
    _struct_descriptors={("i",1):"b",("i",2):"h",("i",4):"i",("i",8):"q",
                         ("u",1):"B",("u",2):"H",("u",4):"I",("u",8):"Q",
                         ("f",4):"f",("f",8):"d"}
    _SCPI_descriptors={"i":"int","u":"int","f":"real"}
    def to_desc(self, str_type="auto"):
        """
        Build a description string of this format.
        
        `str_type` can be ``'auto'`` (similar to ``'numpy'``, but also accepts ``'ascii'``),
        ``'numpy'``, ``'struct'`` or ``'SCPI'`` (return tuple ``(desc, border)``).
        """
        if self.is_ascii():
            if str_type=="auto":
                return "ascii"
            elif str_type=="SCPI":
                return "ascii", "norm"
            else:
                raise ValueError("can't represent format 'ascii' as {0}".format(str_type))
        if str_type in ["numpy","auto"]:
            return self.byteorder+self.kind+str(self.size)
        elif str_type=="struct":
            if (self.kind,self.size) in self._struct_descriptors:
                desc=self._struct_descriptors[(self.kind,self.size)]
            else:
                raise ValueError("can't represent format {0} as struct".format(self))
            return self.byteorder+desc
        elif str_type=="SCPI":
            desc=self._SCPI_descriptors[self.kind]
            border="norm" if self.byteorder==">" else "swap"
            return "{0},{1}".format(desc,self.size*8), border
        else:
            raise ValueError("unrecognized format type: {0}".format(str_type))
    def __str__(self):
        return self.to_desc()
    def __repr__(self):
        return "{0}('{1}')".format(self.__class__.__name__,self.__str__())
    
    def convert_from_str(self, data):
        """Convert the string data into an array."""
        if self.is_ascii():
            if isinstance(data,py3.bytestring):
                data=[e.strip() for e in re.split(br"\s*,\s*|\s+",data)]
            else:
                data=[e.strip() for e in re.split(r"\s*,\s*|\s+",data)]
            return np.array([float(e) for e in data if e])
        else:
            return np.fromstring(data,dtype=self.to_desc("numpy"))
    def convert_to_str(self, data, ascii_format=".5f"):
        """
        Convert the array into a string data.
        
        `ascii_format` is the :meth:`str.format` string for textual representation.
        """
        if self.is_ascii():
            fmt="{:"+ascii_format+"}"
            return ",".join([fmt.format(e) for e in data])
        else:
            return np.asarray(data).astype(self.to_desc("numpy")).tostring()