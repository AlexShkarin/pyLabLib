##########   This file is generated automatically based on pfcam.h, pftypes.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class PropertyFlag(enum.IntEnum):
    F_PRIVATE  = _int32(0x02)
    F_BIG      = _int32(0x04)
    F_RW       = _int32(0x00)
    F_RO       = _int32(0x10)
    F_WO       = _int32(0x20)
    F_INACTIVE = _int32(0x40)
dPropertyFlag={a.name:a.value for a in PropertyFlag}
drPropertyFlag={a.value:a.name for a in PropertyFlag}





##### TYPE DEFINITIONS #####


BYTE=ctypes.c_ubyte
PBYTE=ctypes.POINTER(BYTE)
CHAR=ctypes.c_char
PCHAR=ctypes.c_char_p
UCHAR=ctypes.c_ubyte
PUCHAR=ctypes.POINTER(UCHAR)
ULONG_PTR=ctypes.c_uint64
LONG_PTR=ctypes.c_int64
WORD=ctypes.c_ushort
LPWORD=ctypes.POINTER(WORD)
LONGLONG=ctypes.c_int64
LPLONG=ctypes.POINTER(ctypes.c_long)
HANDLE=ctypes.c_void_p
LPHANDLE=ctypes.POINTER(HANDLE)
HWND=ctypes.c_void_p
HGLOBAL=ctypes.c_void_p
HINSTANCE=ctypes.c_void_p
HDC=ctypes.c_void_p
HMODULE=ctypes.c_void_p
HKEY=ctypes.c_void_p
PVOID=ctypes.c_void_p
LPVOID=ctypes.c_void_p
class PropertyType(enum.IntEnum):
    PF_INVALID =_int32(0)
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
dPropertyType={a.name:a.value for a in PropertyType}
drPropertyType={a.value:a.name for a in PropertyType}


class PFValue(ctypes.Structure):
    _fields_=[  ("ui",ctypes.c_ulong),
                ("type",ctypes.c_int),
                ("len",ctypes.c_int) ]
PPFValue=ctypes.POINTER(PFValue)
class CPFValue(ctypes_wrap.CStructWrapper):
    _struct=PFValue


FeedbackFuncP=ctypes.c_void_p
MirEGLNativeWindowType=ctypes.c_void_p
MirEGLNativeDisplayType=ctypes.c_void_p



##### FUNCTION DEFINITIONS #####





def addfunc(lib, name, restype, argtypes=None, argnames=None):
    if getattr(lib,name,None) is None:
        setattr(lib,name,None)
    else:
        func=getattr(lib,name)
        func.restype=restype
        if argtypes is not None:
            func.argtypes=argtypes
        if argnames is not None:
            func.argnames=argnames

def define_functions(lib):
    #  ctypes.c_int pfPortInit(ctypes.POINTER(ctypes.c_int) numOfPorts)
    addfunc(lib, "pfPortInit", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["numOfPorts"] )
    #  ctypes.c_int pfPortInfo(ctypes.c_int port, ctypes.c_char_p manu, ctypes.POINTER(ctypes.c_int) mBytes, ctypes.c_char_p name, ctypes.POINTER(ctypes.c_int) nBytes, ctypes.POINTER(ctypes.c_int) version, ctypes.POINTER(ctypes.c_int) type)
    addfunc(lib, "pfPortInfo", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["port", "manu", "mBytes", "name", "nBytes", "version", "type"] )
    #  ctypes.c_int pfIsBaudRateSupported(ctypes.c_int port, ctypes.c_int baudrate)
    addfunc(lib, "pfIsBaudRateSupported", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["port", "baudrate"] )
    #  ctypes.c_int pfGetBaudRate(ctypes.c_int port, ctypes.POINTER(ctypes.c_int) baudrate)
    addfunc(lib, "pfGetBaudRate", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["port", "baudrate"] )
    #  ctypes.c_int pfSetBaudRate(ctypes.c_int port, ctypes.c_int baudrate)
    addfunc(lib, "pfSetBaudRate", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["port", "baudrate"] )
    #  ctypes.c_int pfDeviceOpen(ctypes.c_int port)
    addfunc(lib, "pfDeviceOpen", restype = ctypes.c_int,
            argtypes = [ctypes.c_int],
            argnames = ["port"] )
    #  ctypes.c_int pfDeviceClose(ctypes.c_int port)
    addfunc(lib, "pfDeviceClose", restype = ctypes.c_int,
            argtypes = [ctypes.c_int],
            argnames = ["port"] )
    #  ctypes.c_char_p pfDeviceGetDllVersion(ctypes.c_int port, ctypes.POINTER(ctypes.c_int) major, ctypes.POINTER(ctypes.c_int) minor)
    addfunc(lib, "pfDeviceGetDllVersion", restype = ctypes.c_char_p,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["port", "major", "minor"] )
    #  ctypes.c_ulong pfDevice_GetRoot(ctypes.c_int port)
    addfunc(lib, "pfDevice_GetRoot", restype = ctypes.c_ulong,
            argtypes = [ctypes.c_int],
            argnames = ["port"] )
    #  ctypes.c_ulong pfProperty_Select(ctypes.c_int port, ctypes.c_ulong parent, ctypes.c_ulong prev)
    addfunc(lib, "pfProperty_Select", restype = ctypes.c_ulong,
            argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong],
            argnames = ["port", "parent", "prev"] )
    #  ctypes.c_ulong pfProperty_ParseName(ctypes.c_int port, ctypes.c_char_p propname)
    addfunc(lib, "pfProperty_ParseName", restype = ctypes.c_ulong,
            argtypes = [ctypes.c_int, ctypes.c_char_p],
            argnames = ["port", "propname"] )
    #  ctypes.c_char_p pfProperty_GetName(ctypes.c_int port, ctypes.c_ulong p)
    addfunc(lib, "pfProperty_GetName", restype = ctypes.c_char_p,
            argtypes = [ctypes.c_int, ctypes.c_ulong],
            argnames = ["port", "p"] )
    #  ctypes.c_int pfProperty_GetType(ctypes.c_int port, ctypes.c_ulong p)
    addfunc(lib, "pfProperty_GetType", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_ulong],
            argnames = ["port", "p"] )
    #  ctypes.c_ulong pfProperty_GetFlags(ctypes.c_int port, ctypes.c_ulong p)
    addfunc(lib, "pfProperty_GetFlags", restype = ctypes.c_ulong,
            argtypes = [ctypes.c_int, ctypes.c_ulong],
            argnames = ["port", "p"] )
    #  ctypes.c_int pfDevice_GetProperty(ctypes.c_int port, ctypes.c_ulong p, ctypes.POINTER(PFValue) value)
    addfunc(lib, "pfDevice_GetProperty", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.POINTER(PFValue)],
            argnames = ["port", "p", "value"] )
    #  ctypes.c_int pfDevice_GetProperty_String(ctypes.c_int port, ctypes.c_ulong p, ctypes.c_char_p outs, ctypes.c_int len)
    addfunc(lib, "pfDevice_GetProperty_String", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.c_char_p, ctypes.c_int],
            argnames = ["port", "p", "outs", "len"] )
    #  ctypes.c_int pfDevice_SetProperty(ctypes.c_int port, ctypes.c_ulong p, ctypes.POINTER(PFValue) value)
    addfunc(lib, "pfDevice_SetProperty", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.POINTER(PFValue)],
            argnames = ["port", "p", "value"] )
    #  ctypes.c_int pfDevice_SetProperty_String(ctypes.c_int port, ctypes.c_ulong p, ctypes.c_char_p string)
    addfunc(lib, "pfDevice_SetProperty_String", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.c_char_p],
            argnames = ["port", "p", "string"] )
    #  ctypes.c_int pfWrite(ctypes.c_int port, ctypes.c_ushort addr, ctypes.POINTER(ctypes.c_ubyte) buf, ctypes.c_uint size)
    addfunc(lib, "pfWrite", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_ushort, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint],
            argnames = ["port", "addr", "buf", "size"] )
    #  ctypes.c_int pfRead(ctypes.c_int port, ctypes.c_ushort addr, ctypes.POINTER(ctypes.c_ubyte) buf, ctypes.c_int size)
    addfunc(lib, "pfRead", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_ushort, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int],
            argnames = ["port", "addr", "buf", "size"] )
    #  ctypes.c_int pfWrite2(ctypes.c_int port, ctypes.c_ulong addr, ctypes.POINTER(ctypes.c_ubyte) buf, ctypes.c_uint size)
    addfunc(lib, "pfWrite2", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint],
            argnames = ["port", "addr", "buf", "size"] )
    #  ctypes.c_int pfRead2(ctypes.c_int port, ctypes.c_ulong addr, ctypes.POINTER(ctypes.c_ubyte) buf, ctypes.c_int size)
    addfunc(lib, "pfRead2", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int],
            argnames = ["port", "addr", "buf", "size"] )
    #  ctypes.c_char_p pfGetErrorString(ctypes.c_int error)
    addfunc(lib, "pfGetErrorString", restype = ctypes.c_char_p,
            argtypes = [ctypes.c_int],
            argnames = ["error"] )
    #  ctypes.c_int pfValue_ToString(ctypes.POINTER(PFValue) val, ctypes.c_char_p outs, ctypes.c_int len)
    addfunc(lib, "pfValue_ToString", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PFValue), ctypes.c_char_p, ctypes.c_int],
            argnames = ["val", "outs", "len"] )
    #  FeedbackFuncP pfSetFeedback(ctypes.c_int port, FeedbackFuncP func)
    addfunc(lib, "pfSetFeedback", restype = FeedbackFuncP,
            argtypes = [ctypes.c_int, FeedbackFuncP],
            argnames = ["port", "func"] )


