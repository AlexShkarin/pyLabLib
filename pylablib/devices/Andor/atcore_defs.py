##########   This file is generated automatically based on atcore.h   ##########


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class AT_ERR(enum.IntEnum):
    AT_SUCCESS                     = _int32(0)
    AT_ERR_NOTINITIALISED          = _int32(1)
    AT_ERR_NOTIMPLEMENTED          = _int32(2)
    AT_ERR_READONLY                = _int32(3)
    AT_ERR_NOTREADABLE             = _int32(4)
    AT_ERR_NOTWRITABLE             = _int32(5)
    AT_ERR_OUTOFRANGE              = _int32(6)
    AT_ERR_INDEXNOTAVAILABLE       = _int32(7)
    AT_ERR_INDEXNOTIMPLEMENTED     = _int32(8)
    AT_ERR_EXCEEDEDMAXSTRINGLENGTH = _int32(9)
    AT_ERR_CONNECTION              = _int32(10)
    AT_ERR_NODATA                  = _int32(11)
    AT_ERR_INVALIDHANDLE           = _int32(12)
    AT_ERR_TIMEDOUT                = _int32(13)
    AT_ERR_BUFFERFULL              = _int32(14)
    AT_ERR_INVALIDSIZE             = _int32(15)
    AT_ERR_INVALIDALIGNMENT        = _int32(16)
    AT_ERR_COMM                    = _int32(17)
    AT_ERR_STRINGNOTAVAILABLE      = _int32(18)
    AT_ERR_STRINGNOTIMPLEMENTED    = _int32(19)
    AT_ERR_NULL_FEATURE            = _int32(20)
    AT_ERR_NULL_HANDLE             = _int32(21)
    AT_ERR_NULL_IMPLEMENTED_VAR    = _int32(22)
    AT_ERR_NULL_READABLE_VAR       = _int32(23)
    AT_ERR_NULL_READONLY_VAR       = _int32(24)
    AT_ERR_NULL_WRITABLE_VAR       = _int32(25)
    AT_ERR_NULL_MINVALUE           = _int32(26)
    AT_ERR_NULL_MAXVALUE           = _int32(27)
    AT_ERR_NULL_VALUE              = _int32(28)
    AT_ERR_NULL_STRING             = _int32(29)
    AT_ERR_NULL_COUNT_VAR          = _int32(30)
    AT_ERR_NULL_ISAVAILABLE_VAR    = _int32(31)
    AT_ERR_NULL_MAXSTRINGLENGTH    = _int32(32)
    AT_ERR_NULL_EVCALLBACK         = _int32(33)
    AT_ERR_NULL_QUEUE_PTR          = _int32(34)
    AT_ERR_NULL_WAIT_PTR           = _int32(35)
    AT_ERR_NULL_PTRSIZE            = _int32(36)
    AT_ERR_NOMEMORY                = _int32(37)
    AT_ERR_DEVICEINUSE             = _int32(38)
    AT_ERR_DEVICENOTFOUND          = _int32(39)
    AT_ERR_HARDWARE_OVERFLOW       = _int32(100)
dAT_ERR={a.name:a.value for a in AT_ERR}
drAT_ERR={a.value:a.name for a in AT_ERR}


class AT_HANDLE(enum.IntEnum):
    AT_HANDLE_UNINITIALISED = _int32(-1)
    AT_HANDLE_SYSTEM        = _int32(1)
dAT_HANDLE={a.name:a.value for a in AT_HANDLE}
drAT_HANDLE={a.value:a.name for a in AT_HANDLE}





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
PVOID=ctypes.c_void_p
LPVOID=ctypes.c_void_p
HWND=ctypes.c_void_p
AT_H=ctypes.c_int
AT_BOOL=ctypes.c_int
AT_64=ctypes.c_longlong
AT_U8=ctypes.c_ubyte
AT_WC=ctypes.c_wchar
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
PVOID=ctypes.c_void_p
LPVOID=ctypes.c_void_p
HWND=ctypes.c_void_p
FeatureCallback=ctypes.c_void_p



##### FUNCTION DEFINITIONS #####





def define_functions(lib):
    #  ctypes.c_int AT_InitialiseLibrary()
    lib.AT_InitialiseLibrary.restype=ctypes.c_int
    lib.AT_InitialiseLibrary.argtypes=[]
    lib.AT_InitialiseLibrary.argnames=[]
    #  ctypes.c_int AT_FinaliseLibrary()
    lib.AT_FinaliseLibrary.restype=ctypes.c_int
    lib.AT_FinaliseLibrary.argtypes=[]
    lib.AT_FinaliseLibrary.argnames=[]
    #  ctypes.c_int AT_Open(ctypes.c_int CameraIndex, ctypes.POINTER(AT_H) Hndl)
    lib.AT_Open.restype=ctypes.c_int
    lib.AT_Open.argtypes=[ctypes.c_int, ctypes.POINTER(AT_H)]
    lib.AT_Open.argnames=["CameraIndex", "Hndl"]
    #  ctypes.c_int AT_Close(AT_H Hndl)
    lib.AT_Close.restype=ctypes.c_int
    lib.AT_Close.argtypes=[AT_H]
    lib.AT_Close.argnames=["Hndl"]
    #  ctypes.c_int AT_RegisterFeatureCallback(AT_H Hndl, ctypes.c_wchar_p Feature, FeatureCallback EvCallback, ctypes.c_void_p Context)
    lib.AT_RegisterFeatureCallback.restype=ctypes.c_int
    lib.AT_RegisterFeatureCallback.argtypes=[AT_H, ctypes.c_wchar_p, FeatureCallback, ctypes.c_void_p]
    lib.AT_RegisterFeatureCallback.argnames=["Hndl", "Feature", "EvCallback", "Context"]
    #  ctypes.c_int AT_UnregisterFeatureCallback(AT_H Hndl, ctypes.c_wchar_p Feature, FeatureCallback EvCallback, ctypes.c_void_p Context)
    lib.AT_UnregisterFeatureCallback.restype=ctypes.c_int
    lib.AT_UnregisterFeatureCallback.argtypes=[AT_H, ctypes.c_wchar_p, FeatureCallback, ctypes.c_void_p]
    lib.AT_UnregisterFeatureCallback.argnames=["Hndl", "Feature", "EvCallback", "Context"]
    #  ctypes.c_int AT_IsImplemented(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.POINTER(AT_BOOL) Implemented)
    lib.AT_IsImplemented.restype=ctypes.c_int
    lib.AT_IsImplemented.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.POINTER(AT_BOOL)]
    lib.AT_IsImplemented.argnames=["Hndl", "Feature", "Implemented"]
    #  ctypes.c_int AT_IsReadable(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.POINTER(AT_BOOL) Readable)
    lib.AT_IsReadable.restype=ctypes.c_int
    lib.AT_IsReadable.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.POINTER(AT_BOOL)]
    lib.AT_IsReadable.argnames=["Hndl", "Feature", "Readable"]
    #  ctypes.c_int AT_IsWritable(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.POINTER(AT_BOOL) Writable)
    lib.AT_IsWritable.restype=ctypes.c_int
    lib.AT_IsWritable.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.POINTER(AT_BOOL)]
    lib.AT_IsWritable.argnames=["Hndl", "Feature", "Writable"]
    #  ctypes.c_int AT_IsReadOnly(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.POINTER(AT_BOOL) ReadOnly)
    lib.AT_IsReadOnly.restype=ctypes.c_int
    lib.AT_IsReadOnly.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.POINTER(AT_BOOL)]
    lib.AT_IsReadOnly.argnames=["Hndl", "Feature", "ReadOnly"]
    #  ctypes.c_int AT_SetInt(AT_H Hndl, ctypes.c_wchar_p Feature, AT_64 Value)
    lib.AT_SetInt.restype=ctypes.c_int
    lib.AT_SetInt.argtypes=[AT_H, ctypes.c_wchar_p, AT_64]
    lib.AT_SetInt.argnames=["Hndl", "Feature", "Value"]
    #  ctypes.c_int AT_GetInt(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.POINTER(AT_64) Value)
    lib.AT_GetInt.restype=ctypes.c_int
    lib.AT_GetInt.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.POINTER(AT_64)]
    lib.AT_GetInt.argnames=["Hndl", "Feature", "Value"]
    #  ctypes.c_int AT_GetIntMax(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.POINTER(AT_64) MaxValue)
    lib.AT_GetIntMax.restype=ctypes.c_int
    lib.AT_GetIntMax.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.POINTER(AT_64)]
    lib.AT_GetIntMax.argnames=["Hndl", "Feature", "MaxValue"]
    #  ctypes.c_int AT_GetIntMin(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.POINTER(AT_64) MinValue)
    lib.AT_GetIntMin.restype=ctypes.c_int
    lib.AT_GetIntMin.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.POINTER(AT_64)]
    lib.AT_GetIntMin.argnames=["Hndl", "Feature", "MinValue"]
    #  ctypes.c_int AT_SetFloat(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.c_double Value)
    lib.AT_SetFloat.restype=ctypes.c_int
    lib.AT_SetFloat.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.c_double]
    lib.AT_SetFloat.argnames=["Hndl", "Feature", "Value"]
    #  ctypes.c_int AT_GetFloat(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.POINTER(ctypes.c_double) Value)
    lib.AT_GetFloat.restype=ctypes.c_int
    lib.AT_GetFloat.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_double)]
    lib.AT_GetFloat.argnames=["Hndl", "Feature", "Value"]
    #  ctypes.c_int AT_GetFloatMax(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.POINTER(ctypes.c_double) MaxValue)
    lib.AT_GetFloatMax.restype=ctypes.c_int
    lib.AT_GetFloatMax.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_double)]
    lib.AT_GetFloatMax.argnames=["Hndl", "Feature", "MaxValue"]
    #  ctypes.c_int AT_GetFloatMin(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.POINTER(ctypes.c_double) MinValue)
    lib.AT_GetFloatMin.restype=ctypes.c_int
    lib.AT_GetFloatMin.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_double)]
    lib.AT_GetFloatMin.argnames=["Hndl", "Feature", "MinValue"]
    #  ctypes.c_int AT_SetBool(AT_H Hndl, ctypes.c_wchar_p Feature, AT_BOOL Value)
    lib.AT_SetBool.restype=ctypes.c_int
    lib.AT_SetBool.argtypes=[AT_H, ctypes.c_wchar_p, AT_BOOL]
    lib.AT_SetBool.argnames=["Hndl", "Feature", "Value"]
    #  ctypes.c_int AT_GetBool(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.POINTER(AT_BOOL) Value)
    lib.AT_GetBool.restype=ctypes.c_int
    lib.AT_GetBool.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.POINTER(AT_BOOL)]
    lib.AT_GetBool.argnames=["Hndl", "Feature", "Value"]
    #  ctypes.c_int AT_SetEnumIndex(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.c_int Value)
    lib.AT_SetEnumIndex.restype=ctypes.c_int
    lib.AT_SetEnumIndex.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.c_int]
    lib.AT_SetEnumIndex.argnames=["Hndl", "Feature", "Value"]
    #  ctypes.c_int AT_SetEnumString(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.c_wchar_p String)
    lib.AT_SetEnumString.restype=ctypes.c_int
    lib.AT_SetEnumString.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.c_wchar_p]
    lib.AT_SetEnumString.argnames=["Hndl", "Feature", "String"]
    #  ctypes.c_int AT_GetEnumIndex(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.POINTER(ctypes.c_int) Value)
    lib.AT_GetEnumIndex.restype=ctypes.c_int
    lib.AT_GetEnumIndex.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_int)]
    lib.AT_GetEnumIndex.argnames=["Hndl", "Feature", "Value"]
    #  ctypes.c_int AT_GetEnumCount(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.POINTER(ctypes.c_int) Count)
    lib.AT_GetEnumCount.restype=ctypes.c_int
    lib.AT_GetEnumCount.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_int)]
    lib.AT_GetEnumCount.argnames=["Hndl", "Feature", "Count"]
    #  ctypes.c_int AT_IsEnumIndexAvailable(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.c_int Index, ctypes.POINTER(AT_BOOL) Available)
    lib.AT_IsEnumIndexAvailable.restype=ctypes.c_int
    lib.AT_IsEnumIndexAvailable.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.c_int, ctypes.POINTER(AT_BOOL)]
    lib.AT_IsEnumIndexAvailable.argnames=["Hndl", "Feature", "Index", "Available"]
    #  ctypes.c_int AT_IsEnumIndexImplemented(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.c_int Index, ctypes.POINTER(AT_BOOL) Implemented)
    lib.AT_IsEnumIndexImplemented.restype=ctypes.c_int
    lib.AT_IsEnumIndexImplemented.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.c_int, ctypes.POINTER(AT_BOOL)]
    lib.AT_IsEnumIndexImplemented.argnames=["Hndl", "Feature", "Index", "Implemented"]
    #  ctypes.c_int AT_GetEnumStringByIndex(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.c_int Index, ctypes.c_wchar_p String, ctypes.c_int StringLength)
    lib.AT_GetEnumStringByIndex.restype=ctypes.c_int
    lib.AT_GetEnumStringByIndex.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.c_int, ctypes.c_wchar_p, ctypes.c_int]
    lib.AT_GetEnumStringByIndex.argnames=["Hndl", "Feature", "Index", "String", "StringLength"]
    #  ctypes.c_int AT_Command(AT_H Hndl, ctypes.c_wchar_p Feature)
    lib.AT_Command.restype=ctypes.c_int
    lib.AT_Command.argtypes=[AT_H, ctypes.c_wchar_p]
    lib.AT_Command.argnames=["Hndl", "Feature"]
    #  ctypes.c_int AT_SetString(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.c_wchar_p String)
    lib.AT_SetString.restype=ctypes.c_int
    lib.AT_SetString.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.c_wchar_p]
    lib.AT_SetString.argnames=["Hndl", "Feature", "String"]
    #  ctypes.c_int AT_GetString(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.c_wchar_p String, ctypes.c_int StringLength)
    lib.AT_GetString.restype=ctypes.c_int
    lib.AT_GetString.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_int]
    lib.AT_GetString.argnames=["Hndl", "Feature", "String", "StringLength"]
    #  ctypes.c_int AT_GetStringMaxLength(AT_H Hndl, ctypes.c_wchar_p Feature, ctypes.POINTER(ctypes.c_int) MaxStringLength)
    lib.AT_GetStringMaxLength.restype=ctypes.c_int
    lib.AT_GetStringMaxLength.argtypes=[AT_H, ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_int)]
    lib.AT_GetStringMaxLength.argnames=["Hndl", "Feature", "MaxStringLength"]
    #  ctypes.c_int AT_QueueBuffer(AT_H Hndl, ctypes.POINTER(AT_U8) Ptr, ctypes.c_int PtrSize)
    lib.AT_QueueBuffer.restype=ctypes.c_int
    lib.AT_QueueBuffer.argtypes=[AT_H, ctypes.POINTER(AT_U8), ctypes.c_int]
    lib.AT_QueueBuffer.argnames=["Hndl", "Ptr", "PtrSize"]
    #  ctypes.c_int AT_WaitBuffer(AT_H Hndl, ctypes.POINTER(ctypes.POINTER(AT_U8)) Ptr, ctypes.POINTER(ctypes.c_int) PtrSize, ctypes.c_uint Timeout)
    lib.AT_WaitBuffer.restype=ctypes.c_int
    lib.AT_WaitBuffer.argtypes=[AT_H, ctypes.POINTER(ctypes.POINTER(AT_U8)), ctypes.POINTER(ctypes.c_int), ctypes.c_uint]
    lib.AT_WaitBuffer.argnames=["Hndl", "Ptr", "PtrSize", "Timeout"]
    #  ctypes.c_int AT_Flush(AT_H Hndl)
    lib.AT_Flush.restype=ctypes.c_int
    lib.AT_Flush.argtypes=[AT_H]
    lib.AT_Flush.argnames=["Hndl"]


