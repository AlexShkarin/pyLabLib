from ...core.utils import general, py3, ctypes_wrap
from .misc import load_lib
from .IMAQ_lib import IMAQLibError

import numpy as np
import ctypes
import collections

_depends_local=["...core.utils.ctypes_wrap"]

class PfcamLibError(RuntimeError):
    """Generic pfcam library error."""
    def __init__(self, func, code, lib=None):
        self.func=func
        self.code=code
        self.desc=""
        try:
            if lib is not None:
                self.desc=py3.as_str(lib.pfGetErrorString(code))
        except IMAQLibError:
            pass
        self.msg="function '{}' raised error {}: {}".format(func,code,self.desc)
        RuntimeError.__init__(self,self.msg)
def errcheck(passing=None, lib=None, pass_positive=False):
    """
    Build an error checking function.

    Return a function which checks return codes of IMAQ library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    if passing is None:
        passing={0}
    def checker(result, func, arguments):
        if not (result in passing or (pass_positive and result>=0)):
            raise PfcamLibError(func.__name__,result,lib=lib)
        return result
    return checker



TPfcamError=ctypes.c_int
TPfPort=ctypes.c_int
TPfToken=ctypes.c_int
PfInvalidToken=0
TPfPropertyFlags=ctypes.c_long
TPfPropertyType=ctypes.c_int

PFCAM_MAX_API_STRING_LENGTH=512



## There are at least two different version of SDK DLLs around, with the only difference being mapping of TPropertyType (specifically, the position of PF_UINT)
## Can be detected by querying a type of "Header" property, which should be PF_STRUCT (9 in v1, 10 in v2)
TPropertyType_v1 = {
	0: "PF_INVALID",
	1: "PF_ROOT",
	2: "PF_INT",
	3: "PF_FLOAT",
	4: "PF_BOOL",
	5: "PF_MODE",
	6: "PF_REGISTER",
	7: "PF_STRING",
	8: "PF_BUFFER",
	9: "PF_STRUCT",
	10: "PF_ARRAY",
	11: "PF_COMMAND",
	12: "PF_EVENT",
	13: "PF_UINT"
}
TPropertyType_v2 = {
	0: "PF_INVALID",
	1: "PF_ROOT",
	2: "PF_INT",
	3: "PF_UINT",
	4: "PF_FLOAT",
	5: "PF_BOOL",
	6: "PF_MODE",
	7: "PF_REGISTER",
	8: "PF_STRING",
	9: "PF_BUFFER",
	10: "PF_STRUCT",
	11: "PF_ARRAY",
	12: "PF_COMMAND",
	13: "PF_EVENT"
}
TPropertyType_inv_v1=general.invert_dict(TPropertyType_v1)
TPropertyType_inv_v2=general.invert_dict(TPropertyType_v2)
ValuePropertyTypes={"PF_INT","PF_FLOAT","PF_BOOL","PF_MODE","PF_STRING","PF_UINT"}
def _get_ptype_dicts(ptype_v=1):
    if ptype_v==2:
        return TPropertyType_v2,TPropertyType_inv_v2
    else:
        return TPropertyType_v1,TPropertyType_inv_v1

TPropertyFlag = {
    0x02: "F_PRIVATE",
    0x04: "F_BIG",
    0x00: "F_RW",
    0x10: "F_RO",
    0x20: "F_WO",
    0x40: "F_INACTIVE",
}

class CPFValue_val(ctypes.Union):
    _fields_=[  ("pvalue",ctypes.c_void_p),
                ("ivalue",ctypes.c_long),
                ("uvalue",ctypes.c_ulong),
                ("fvalue",ctypes.c_float)]
class CPFValue(ctypes.Structure):
    _fields_=[  ("val",CPFValue_val),
                ("ptype",TPfPropertyType),
                ("plen",ctypes.c_int)]

def _autodetect_ptype(value):
    if isinstance(value,int):
        return "PF_INT"
    if isinstance(value, float):
        return "PF_FLOAT"
    if isinstance(value, bool):
        return "PF_BOOL"
    if isinstance(value,py3.anystring):
        return "PF_STRING"
    raise ValueError("can't autodetect value {}".format(value))
def build_pf_value(value, ptype="auto", buffer=None, ptype_v=1):
    TPropertyType,TPropertyType_inv=_get_ptype_dicts(ptype_v)
    if ptype=="auto":
        ptype=_autodetect_ptype(value)
    ptype=TPropertyType.get(ptype,ptype)
    plen=0
    if ptype in {"PF_INT","PF_BOOL","PF_MODE","PF_COMMAND"}:
        value=CPFValue_val(ivalue=int(value))
    elif ptype=="PF_UINT":
        value=CPFValue_val(uvalue=int(value))
    elif ptype=="PF_FLOAT":
        value=CPFValue_val(fvalue=float(value))
    elif ptype=="PF_STRING":
        value=py3.as_builtin_bytes(str(value))
        if buffer is None or len(buffer)<len(value)+1:
            raise ValueError("buffer is not suppled or too short")
        buffer[:len(value)]=value
        buffer[len(value)]=b"\x00"
        plen=len(value)+1
        value=CPFValue_val(pvalue=ctypes.addressof(buffer))
    elif ptype in {"PF_INVALID","PF_ROOT","PF_STRUCT"}:
        raise ValueError("can't build PFValue for value type {}".format(ptype))
    else:
        raise ValueError("don't know how to build PFValue for value type {}".format(ptype))
    iptype=TPropertyType_inv.get(ptype,ptype)
    return CPFValue(val=value,ptype=iptype,plen=plen)
def allocate_pf_value(ptype, buffer=None, ptype_v=1):
    TPropertyType,TPropertyType_inv=_get_ptype_dicts(ptype_v)
    ptype=TPropertyType.get(ptype,ptype)
    plen=0
    if ptype in {"PF_INT","PF_UINT","PF_BOOL","PF_MODE","PF_COMMAND","PF_FLOAT"}:
        value=CPFValue_val(ivalue=0)
    elif ptype=="PF_STRING":
        if buffer is None:
            raise ValueError("buffer is not suppled")
        value=CPFValue_val(pvalue=ctypes.addressof(buffer))
        plen=len(buffer)
    elif ptype in {"PF_INVALID","PF_ROOT","PF_STRUCT"}:
        raise ValueError("can't build PFValue for value type {}".format(ptype))
    else:
        raise ValueError("don't know how to build PFValue for value type {}".format(ptype))
    iptype=TPropertyType_inv.get(ptype,ptype)
    return CPFValue(val=value,ptype=iptype,plen=plen)
def parse_pf_value(pf_value, ptype_v=1):
    TPropertyType,_=_get_ptype_dicts(ptype_v)
    iptype=pf_value.ptype
    ptype=TPropertyType[iptype]
    value=pf_value.val
    if ptype in {"PF_INT","PF_BOOL","PF_MODE","PF_COMMAND"}:
        value=int(value.ivalue)
        if ptype=="PF_BOOL":
            value=bool(value)
    elif ptype=="PF_UINT":
        value=int(value.uvalue)
    elif ptype=="PF_FLOAT":
        value=float(value.fvalue)
    elif ptype=="PF_STRING":
        l=pf_value.plen
        if l<=0:
            raise ValueError("zero-length string")
        value=ctypes.string_at(value.pvalue)
        value=py3.as_str(value[:-1])
    elif ptype in {"PF_INVALID","PF_ROOT","PF_STRUCT"}:
        raise ValueError("can't parse PFValue for value type {}".format(ptype))
    else:
        raise ValueError("don't know how to parse PFValue for value type {}".format(ptype))
    return value


class PfcamLib(object):
    def __init__(self):
        object.__init__(self)
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return
        error_message="The library is automatically supplied with PhotonFocus PFRemote software"
        self.lib=load_lib("pfcam.dll",error_message=error_message)
        lib=self.lib

        generic_wrapper=ctypes_wrap.CTypesWrapper()
        wrapper=ctypes_wrap.CTypesWrapper(restype=TPfcamError, return_res=False, errcheck=errcheck(lib=self,pass_positive=True))
        twrapper=ctypes_wrap.CTypesWrapper(restype=TPfToken, return_res=True, errcheck=errcheck(lib=self,pass_positive=True))
        strprep=ctypes_wrap.strprep(PFCAM_MAX_API_STRING_LENGTH)
        self.string_buffer=ctypes.create_string_buffer(PFCAM_MAX_API_STRING_LENGTH)

        self.pfGetErrorString=generic_wrapper.wrap(lib.pfGetErrorString, [ctypes.c_int], ["code"], restype=ctypes.c_char_p)

        self.pfPortInit=wrapper.wrap(lib.pfPortInit, [ctypes.c_int], [None])
        self.pfPortInfo=wrapper.wrap(lib.pfPortInfo, [TPfPort,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_int,ctypes.c_int],
            ["port",None,None,None,None,None,None], rvprep=[strprep,None,strprep,None,None,None],
            rvref=[False,True,False,True,True,True], rvnames=["manu",None,"port",None,"ver","ctype"])
        self.pfIsBaudRateSupported=wrapper.wrap(lib.pfIsBaudRateSupported, [TPfPort,ctypes.c_int], ["port","rate"], return_res=True, errcheck=errcheck(lib=self,passing={0,1}))
        self.pfGetBaudRate =wrapper.wrap(lib.pfGetBaudRate , [TPfPort,ctypes.c_int], ["port",None])
        self.pfSetBaudRate =wrapper.wrap(lib.pfSetBaudRate , [TPfPort,ctypes.c_int], ["port","rate"])
        self.pfDeviceOpen=wrapper.wrap(lib.pfDeviceOpen, [TPfPort], ["port"])
        self.pfDeviceClose=wrapper.wrap(lib.pfDeviceClose, [TPfPort], ["port"])

        self.pfDevice_GetRoot=twrapper.wrap(lib.pfDevice_GetRoot, [TPfPort], ["port"])
        self.pfProperty_GetName=generic_wrapper.wrap(lib.pfProperty_GetName, [TPfPort,TPfToken], ["port","token"], restype=ctypes.c_char_p)
        self.pfProperty_ParseName=twrapper.wrap(lib.pfProperty_ParseName, [TPfPort,ctypes.c_char_p], ["port","name"])
        self.pfProperty_GetFlags=generic_wrapper.wrap(lib.pfProperty_GetFlags, [TPfPort,TPfToken], ["port","token"], restype=TPfPropertyFlags, errcheck=errcheck(lib=self,pass_positive=True))
        self.pfProperty_GetType=generic_wrapper.wrap(lib.pfProperty_GetType, [TPfPort,TPfToken], ["port","token"], restype=TPfPropertyType, errcheck=errcheck(lib=self,pass_positive=True))
        self.pfProperty_Select=twrapper.wrap(lib.pfProperty_Select, [TPfPort,TPfToken,TPfToken], ["port","parent","prev"])


        self.pfDevice_GetProperty_lib=wrapper.wrap(lib.pfDevice_GetProperty, [TPfPort,TPfToken,CPFValue],
            ["port","token",None], rvprep=[lambda *args:args[-1]], addargs=["value"])
        self.pfDevice_SetProperty_lib=wrapper.wrap(lib.pfDevice_SetProperty, [TPfPort,TPfToken,CPFValue],
            ["port","token",None], rvprep=[lambda *args:args[-1]], addargs=["value"])
        self.pfDevice_GetProperty_String=wrapper.wrap(lib.pfDevice_GetProperty_String, [TPfPort,TPfToken,ctypes.c_char_p,ctypes.c_int],
            ["port","token",None,None], rvref=[False,False], rvprep=[strprep, lambda *args: PFCAM_MAX_API_STRING_LENGTH], rvnames=["val",None])
        self.pfDevice_SetProperty_String=wrapper.wrap(lib.pfDevice_SetProperty_String, [TPfPort,TPfToken,ctypes.c_char_p], ["port","token","value"])

        self.ptype_v=None

        self._initialized=True
    
    def get_ptype_v(self, port):
        if self.ptype_v is None:
            header_tok=self.pfProperty_ParseName(port,"Header")
            header_type=self.pfProperty_GetType(port,header_tok)
            if header_type==9:
                self.ptype_v=1
            elif header_type==10:
                self.ptype_v=2
            else:
                raise RuntimeError("can't determine pflib version")
        return self.ptype_v
    def get_ptype_dicts(self, port):
        return _get_ptype_dicts(self.get_ptype_v(port))
    
    def pfDevice_GetProperty(self, port, token, ptype=None):
        if isinstance(token,py3.anystring):
            token=self.pfProperty_ParseName(port,token)
        if ptype is None:
            ptype=self.pfProperty_GetType(port,token)
        value=allocate_pf_value(ptype,buffer=self.string_buffer,ptype_v=self.get_ptype_v(port))
        ret_value=self.pfDevice_GetProperty_lib(port,token,value)
        return parse_pf_value(ret_value,ptype_v=self.get_ptype_v(port))
    def pfDevice_SetProperty(self, port, token, value, ptype=None):
        if isinstance(token,py3.anystring):
            token=self.pfProperty_ParseName(port,token)
        if ptype is None:
            ptype=self.pfProperty_GetType(port,token)
        value=build_pf_value(value,ptype,buffer=self.string_buffer,ptype_v=self.get_ptype_v(port))
        ret_value=self.pfDevice_SetProperty_lib(port,token,value)
        return parse_pf_value(ret_value,ptype_v=self.get_ptype_v(port))

    def get_property_by_name(self, port, name, ptype=None, default=None):
        token=self.pfProperty_ParseName(port,name)
        if token==PfInvalidToken:
            return default
        return self.pfDevice_GetProperty(port,token,ptype=ptype)
    def collect_properties(self, port, root=0, backbone=True, pfx="", include_types=None):
        TPropertyType,_=self.get_ptype_dicts(port)
        tok=root
        props=[]
        while True:
            tok=self.pfProperty_Select(port,root,tok)
            if tok==PfInvalidToken:
                break
            name=py3.as_str(self.pfProperty_GetName(port,tok))
            if pfx:
                name=pfx+"."+name
            ptype=TPropertyType[self.pfProperty_GetType(port,tok)]
            if ptype!="PF_STRUCT" and (include_types is None or ptype in include_types):
                props.append((tok,name))
            if ptype=="PF_STRUCT" or not backbone:
                props+=self.collect_properties(port,tok,backbone=backbone,pfx=name,include_types=include_types)
        return props



lib=PfcamLib()