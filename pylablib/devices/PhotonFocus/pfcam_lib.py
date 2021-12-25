# pylint: disable=wrong-spelling-in-comment

from . import pfcam_defs  # pylint: disable=unused-import
from .pfcam_defs import define_functions

from ...core.utils import ctypes_wrap, py3
from ...core.devio.comm_backend import DeviceError
from ..utils import load_lib

import ctypes
import enum


class PFCamError(DeviceError):
    """Generic PFCam error"""
class PFCamLibError(PFCamError):
    """Generic PFCam library error"""
    def __init__(self, func, code, lib=None):
        self.func=func
        self.code=code
        self.desc=""
        try:
            if lib is not None:
                self.desc=py3.as_str(lib.pfGetErrorString(code))
        except PFCamLibError:
            pass
        self.msg="function '{}' raised error {}: {}".format(func,code,self.desc)
        PFCamError.__init__(self,self.msg)
def errcheck(passing=None, lib=None, pass_positive=False):
    """
    Build an error checking function.

    Return a function which checks return codes of PFCam library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    If ``pass_positive==True``, any positive value is allowed.
    """
    if passing is None:
        passing={0}
    def errchecker(result, func, arguments):  # pylint: disable=unused-argument
        if not (result in passing or (pass_positive and result>=0)):
            raise PFCamLibError(func.__name__,result,lib=lib)
        return result
    return errchecker




## There are at least two different version of SDK DLLs around, with the only difference being mapping of PropertyType (specifically, the position of PF_UINT)
## They can be detected by querying a type of "Header" property, which should be PF_STRUCT (9 in v1, 10 in v2)
class PropertyType_v1(enum.IntEnum):
    PF_INVALID =0
    PF_ROOT    =enum.auto()
    PF_INT     =enum.auto()
    PF_FLOAT   =enum.auto()
    PF_BOOL    =enum.auto()
    PF_MODE    =enum.auto()
    PF_REGISTER=enum.auto()
    PF_STRING  =enum.auto()
    PF_BUFFER  =enum.auto()
    PF_STRUCT  =enum.auto()
    PF_ARRAY   =enum.auto()
    PF_COMMAND =enum.auto()
    PF_EVENT   =enum.auto()
    PF_UINT    =enum.auto()
dPropertyType_v1={a.name:a.value for a in PropertyType_v1}
drPropertyType_v1={a.value:a.name for a in PropertyType_v1}
class PropertyType_v2(enum.IntEnum):
    PF_INVALID =0
    PF_ROOT    =enum.auto()
    PF_INT     =enum.auto()
    PF_UINT    =enum.auto()
    PF_FLOAT   =enum.auto()
    PF_BOOL    =enum.auto()
    PF_MODE    =enum.auto()
    PF_REGISTER=enum.auto()
    PF_STRING  =enum.auto()
    PF_BUFFER  =enum.auto()
    PF_STRUCT  =enum.auto()
    PF_ARRAY   =enum.auto()
    PF_COMMAND =enum.auto()
    PF_EVENT   =enum.auto()
dPropertyType_v2={a.name:a.value for a in PropertyType_v2}
drPropertyType_v2={a.value:a.name for a in PropertyType_v2}

class PFValueUI(ctypes.Union):
    _fields_=[  ("pvalue",ctypes.c_void_p),
                ("ivalue",ctypes.c_long),
                ("uvalue",ctypes.c_ulong),
                ("fvalue",ctypes.c_float)]
class PFValue(ctypes.Structure):
    _fields_=[  ("ui",PFValueUI),
                ("type",ctypes.c_int),
                ("len",ctypes.c_int) ]
PPFValue=ctypes.POINTER(PFValue)
class CPFValue(ctypes_wrap.CStructWrapper):
    _struct=PFValue




PFCAM_MAX_API_STRING_LENGTH=512
ValuePropertyTypes={"PF_INT","PF_FLOAT","PF_BOOL","PF_MODE","PF_STRING","PF_UINT"}
PfInvalidToken=0

class PFCamLib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return
        error_message="The library is automatically supplied with PhotonFocus PFRemote software\n"+load_lib.par_error_message.format("pfcam")
        self.lib=load_lib.load_lib("pfcam.dll",locations=("parameter/pfcam","global"),error_message=error_message,call_conv="cdecl",locally=True)
        lib=self.lib
        define_functions(lib)

        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(lib=self,pass_positive=True),default_rvals="pointer")
        strprep=ctypes_wrap.strprep(PFCAM_MAX_API_STRING_LENGTH)
        self.ptype_v=None
        self.string_buffer=ctypes.create_string_buffer(PFCAM_MAX_API_STRING_LENGTH)

        #  ctypes.c_char_p pfGetErrorString(ctypes.c_int error)
        self.pfGetErrorString=ctypes_wrap.CFunctionWrapper()(lib.pfGetErrorString)

        #  ctypes.c_int pfPortInit(ctypes.POINTER(ctypes.c_int) numOfPorts)
        self.pfPortInit=wrapper(lib.pfPortInit)
        #  ctypes.c_int pfPortInfo(ctypes.c_int port, ctypes.c_char_p manu, ctypes.POINTER(ctypes.c_int) mBytes, ctypes.c_char_p name, ctypes.POINTER(ctypes.c_int) nBytes, ctypes.POINTER(ctypes.c_int) version, ctypes.POINTER(ctypes.c_int) type)
        self.pfPortInfo=wrapper(lib.pfPortInfo, args=["port"], rvals=["manu","name","version","type"],
            argprep={"manu":strprep,"name":strprep}, byref=["mBytes","nBytes","version","type"])
        #  ctypes.c_int pfIsBaudRateSupported(ctypes.c_int port, ctypes.c_int baudrate)
        self.pfIsBaudRateSupported=wrapper(lib.pfIsBaudRateSupported, errcheck=errcheck(lib=self,passing={0,1}))
        #  ctypes.c_int pfGetBaudRate(ctypes.c_int port, ctypes.POINTER(ctypes.c_int) baudrate)
        self.pfGetBaudRate=wrapper(lib.pfGetBaudRate)
        #  ctypes.c_int pfSetBaudRate(ctypes.c_int port, ctypes.c_int baudrate)
        self.pfSetBaudRate=wrapper(lib.pfSetBaudRate)
        #  ctypes.c_int pfDeviceOpen(ctypes.c_int port)
        self.pfDeviceOpen=wrapper(lib.pfDeviceOpen)
        #  ctypes.c_int pfDeviceClose(ctypes.c_int port)
        self.pfDeviceClose=wrapper(lib.pfDeviceClose)
        
        #  ctypes.c_ulong pfDevice_GetRoot(ctypes.c_int port)
        self.pfDevice_GetRoot=wrapper(lib.pfDevice_GetRoot)
        #  ctypes.c_ulong pfProperty_Select(ctypes.c_int port, ctypes.c_ulong parent, ctypes.c_ulong prev)
        self.pfProperty_Select=wrapper(lib.pfProperty_Select)
        #  ctypes.c_ulong pfProperty_ParseName(ctypes.c_int port, ctypes.c_char_p propname)
        self.pfProperty_ParseName=wrapper(lib.pfProperty_ParseName)
        #  ctypes.c_char_p pfProperty_GetName(ctypes.c_int port, ctypes.c_ulong p)
        self.pfProperty_GetName=ctypes_wrap.CFunctionWrapper()(lib.pfProperty_GetName)
        #  ctypes.c_int pfProperty_GetType(ctypes.c_int port, ctypes.c_ulong p)
        self.pfProperty_GetType=wrapper(lib.pfProperty_GetType)
        #  ctypes.c_ulong pfProperty_GetFlags(ctypes.c_int port, ctypes.c_ulong p)
        self.pfProperty_GetFlags=wrapper(lib.pfProperty_GetFlags)

        #  ctypes.c_int pfDevice_GetProperty_String(ctypes.c_int port, ctypes.c_ulong p, ctypes.c_char_p outs, ctypes.c_int len)
        self.pfDevice_GetProperty_String=wrapper(lib.pfDevice_GetProperty_String, rvals=["outs"],
            argprep={"outs":strprep, "len":PFCAM_MAX_API_STRING_LENGTH}, byref=[])
        #  ctypes.c_int pfDevice_SetProperty_String(ctypes.c_int port, ctypes.c_ulong p, ctypes.c_char_p string)
        self.pfDevice_SetProperty_String=wrapper(lib.pfDevice_SetProperty_String)
        #  ctypes.c_int pfDevice_GetProperty(ctypes.c_int port, ctypes.c_ulong p, ctypes.POINTER(PFValue) value)
        lib.pfDevice_GetProperty.argtypes=[ctypes.c_int, ctypes.c_ulong, ctypes.POINTER(PFValue)]
        self.pfDevice_GetProperty_lib=wrapper(lib.pfDevice_GetProperty, args="all", rvals=[],
            argprep={"value": lambda value: ctypes.pointer(value)}, byref=[])  # pylint: disable=unnecessary-lambda
        #  ctypes.c_int pfDevice_SetProperty(ctypes.c_int port, ctypes.c_ulong p, ctypes.POINTER(PFValue) value)
        lib.pfDevice_SetProperty.argtypes=[ctypes.c_int, ctypes.c_ulong, ctypes.POINTER(PFValue)]
        self.pfDevice_SetProperty_lib=wrapper(lib.pfDevice_SetProperty, args="all", rvals=[],
            argprep={"value": lambda value: ctypes.pointer(value)}, byref=[])  # pylint: disable=unnecessary-lambda
        #  ctypes.c_int pfValue_ToString(ctypes.POINTER(PFValue) val, ctypes.c_char_p outs, ctypes.c_int len)
        lib.pfValue_ToString.argtypes=[ctypes.POINTER(PFValue), ctypes.c_char_p, ctypes.c_int]
        self.pfValue_ToString=wrapper(lib.pfValue_ToString, args="all", rvals=["outs"],
            argprep={"outs":strprep, "len":PFCAM_MAX_API_STRING_LENGTH, "val": lambda val: ctypes.pointer(val)}, byref=[])  # pylint: disable=unnecessary-lambda

        self._initialized=True

        ### Undocumented ####
        #  ctypes.c_int pfWrite(ctypes.c_int port, ctypes.c_ushort addr, ctypes.POINTER(ctypes.c_ubyte) buf, ctypes.c_uint size)
        #  ctypes.c_int pfRead(ctypes.c_int port, ctypes.c_ushort addr, ctypes.POINTER(ctypes.c_ubyte) buf, ctypes.c_int size)
        #  ctypes.c_int pfWrite2(ctypes.c_int port, ctypes.c_ulong addr, ctypes.POINTER(ctypes.c_ubyte) buf, ctypes.c_uint size)
        #  ctypes.c_int pfRead2(ctypes.c_int port, ctypes.c_ulong addr, ctypes.POINTER(ctypes.c_ubyte) buf, ctypes.c_int size)
        #  ctypes.c_char_p pfDeviceGetDllVersion(ctypes.c_int port, ctypes.POINTER(ctypes.c_int) major, ctypes.POINTER(ctypes.c_int) minor)
        
        ### Unused ###
        #  FeedbackFuncP pfSetFeedback(ctypes.c_int port, FeedbackFuncP func)


    def get_ptype_v(self, port):
        """Get `PropertyType` version"""
        if self.ptype_v is None:
            header_tok=self.pfProperty_ParseName(port,"Header")
            header_type=self.pfProperty_GetType(port,header_tok)
            if header_type==9:
                self.ptype_v=1
            elif header_type==10:
                self.ptype_v=2
            else:
                raise PFCamError("can't determine pfcam version")
        return self.ptype_v
    def get_ptype_dicts(self, port):
        """Get the correct `PropertyType` version"""
        if self.get_ptype_v(port)==2:
            return dPropertyType_v2,drPropertyType_v2
        else:
            return dPropertyType_v1,drPropertyType_v1
    def get_ptype_name(self, port, iptype):
        """Get PropertyType name by its ID"""
        _,drPropertyType=self.get_ptype_dicts(port)
        return drPropertyType.get(iptype,iptype)
    def get_ptype_id(self, port, ptype):
        """Get PropertyType ID by its name"""
        dPropertyType,_=self.get_ptype_dicts(port)
        return dPropertyType.get(ptype,ptype)

    def _autodetect_ptype(self, value):
        if isinstance(value,int):
            return "PF_INT"
        if isinstance(value, float):
            return "PF_FLOAT"
        if isinstance(value, bool):
            return "PF_BOOL"
        if isinstance(value,py3.anystring):
            return "PF_STRING"
        raise ValueError("can't autodetect value {}".format(value))
    def build_pf_value(self, port, value, ptype="auto", buffer=None):
        """Build a :class:`PFValue` structure given the Python value"""
        dPropertyType,drPropertyType=self.get_ptype_dicts(port)
        if ptype=="auto":
            ptype=self._autodetect_ptype(value)
        ptype=drPropertyType.get(ptype,ptype)
        plen=0
        if ptype in {"PF_INT","PF_BOOL","PF_MODE","PF_COMMAND"}:
            value=PFValueUI(ivalue=int(value))
        elif ptype=="PF_UINT":
            value=PFValueUI(uvalue=int(value))
        elif ptype=="PF_FLOAT":
            value=PFValueUI(fvalue=float(value))
        elif ptype=="PF_STRING":
            value=py3.as_builtin_bytes(str(value))
            if buffer is None or len(buffer)<len(value)+1:
                raise PFCamError("buffer is not supplied or too short")
            buffer[:len(value)]=value
            buffer[len(value)]=b"\x00"
            plen=len(value)+1
            value=PFValueUI(pvalue=ctypes.addressof(buffer))
        elif ptype in {"PF_INVALID","PF_ROOT","PF_STRUCT"}:
            raise PFCamError("can't build PFValue for value type {}".format(ptype))
        else:
            raise PFCamError("don't know how to build PFValue for value type {}".format(ptype))
        iptype=dPropertyType[ptype]
        return PFValue(ui=value,type=iptype,len=plen)

    def allocate_pf_value(self, port, ptype, buffer=None):
        """Build a new :class:`PFValue` of the given type"""
        dPropertyType,drPropertyType=self.get_ptype_dicts(port)
        ptype=drPropertyType.get(ptype,ptype)
        plen=0
        if ptype in {"PF_INT","PF_UINT","PF_BOOL","PF_MODE","PF_COMMAND","PF_FLOAT"}:
            value=PFValueUI(ivalue=0)
        elif ptype=="PF_STRING":
            if buffer is None:
                raise PFCamError("buffer is not supplied")
            value=PFValueUI(pvalue=ctypes.addressof(buffer))
            plen=len(buffer)
        elif ptype in {"PF_INVALID","PF_ROOT","PF_STRUCT"}:
            raise PFCamError("can't build PFValue for value type {}".format(ptype))
        else:
            raise PFCamError("don't know how to build PFValue for value type {}".format(ptype))
        iptype=dPropertyType[ptype]
        return PFValue(ui=value,type=iptype,len=plen)
        
    def parse_pf_value(self, port, pf_value):
        """Parse :class:`PFValue` and return the corresponding Python value"""
        _,drPropertyType=self.get_ptype_dicts(port)
        iptype=pf_value.type
        ptype=drPropertyType[iptype]
        value=pf_value.ui
        if ptype in {"PF_INT","PF_BOOL","PF_MODE","PF_COMMAND"}:
            value=int(value.ivalue)
            if ptype=="PF_BOOL":
                value=bool(value)
        elif ptype=="PF_UINT":
            value=int(value.uvalue)
        elif ptype=="PF_FLOAT":
            value=float(value.fvalue)
        elif ptype=="PF_STRING":
            l=pf_value.len
            if l<=0:
                raise PFCamError("zero-length string")
            value=ctypes.string_at(value.pvalue)
            value=py3.as_str(value[:-1])
        elif ptype in {"PF_INVALID","PF_ROOT","PF_STRUCT"}:
            raise PFCamError("can't parse PFValue for value type {}".format(ptype))
        else:
            raise PFCamError("don't know how to parse PFValue for value type {}".format(ptype))
        return value


    def pfDevice_GetProperty(self, port, token, ptype=None):
        if isinstance(token,py3.anystring):
            token=self.pfProperty_ParseName(port,token)
        if ptype is None:
            ptype=self.pfProperty_GetType(port,token)
        value=self.allocate_pf_value(port,ptype,buffer=self.string_buffer)
        self.pfDevice_GetProperty_lib(port,token,value)
        return self.parse_pf_value(port,value)
    def pfDevice_SetProperty(self, port, token, value, ptype=None):
        if isinstance(token,py3.anystring):
            token=self.pfProperty_ParseName(port,token)
        if ptype is None:
            ptype=self.pfProperty_GetType(port,token)
        value=self.build_pf_value(port,value,ptype,buffer=self.string_buffer)
        self.pfDevice_SetProperty_lib(port,token,value)
        return self.parse_pf_value(port,value)

    def get_property_by_name(self, port, name, ptype=None, default=None):
        """Get property value by its name"""
        token=self.pfProperty_ParseName(port,name)
        if token==PfInvalidToken:
            return default
        return self.pfDevice_GetProperty(port,token,ptype=ptype)
    def collect_properties(self, port, root=0, backbone=True, pfx="", include_types=None):
        """Build a list of all available properties"""
        _,drPropertyType=self.get_ptype_dicts(port)
        tok=root
        props=[]
        while True:
            tok=self.pfProperty_Select(port,root,tok)
            if tok==PfInvalidToken:
                break
            name=py3.as_str(self.pfProperty_GetName(port,tok))
            if pfx:
                name=pfx+"."+name
            ptype=drPropertyType[self.pfProperty_GetType(port,tok)]
            if ptype!="PF_STRUCT" and (include_types is None or ptype in include_types):
                props.append((tok,name))
            if ptype=="PF_STRUCT" or not backbone:
                props+=self.collect_properties(port,tok,backbone=backbone,pfx=name,include_types=include_types)
        return props



wlib=PFCamLib()