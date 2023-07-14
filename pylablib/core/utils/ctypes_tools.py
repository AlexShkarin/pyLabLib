import ctypes
import sys


##### Windows types #####

BOOL=ctypes.c_int
BOOLEAN=ctypes.c_ubyte

BYTE=ctypes.c_ubyte
PBYTE=ctypes.POINTER(BYTE)

CHAR=ctypes.c_char
PCHAR=ctypes.c_char_p
UCHAR=ctypes.c_ubyte
PUCHAR=ctypes.POINTER(UCHAR)
PSTR=PCSTR=LPSTR=LPCSTR=ctypes.c_char_p

WCHAR=ctypes.c_wchar
PWCHAR=ctypes.c_wchar_p
PWSTR=PCWSTR=LPWSTR=LPCWSTR=ctypes.c_wchar_p

SHORT=ctypes.c_short
USHORT=ctypes.c_ushort
WORD=ctypes.c_short
PWORD=LPWORD=ctypes.POINTER(WORD)

DWORD=ctypes.c_ulong
PDWORD=LPDWORD=ctypes.POINTER(DWORD)
LONG=ctypes.c_long
PLONG=LPLONG=ctypes.POINTER(LONG)
ULONG=ctypes.c_long
PULONG=LPULONG=ctypes.POINTER(ULONG)

is_64bit=sys.maxsize>2**32
if is_64bit:
    LONG_PTR=ctypes.c_int64
    ULONG_PTR=ctypes.c_uint64
else:
    LONG_PTR=ctypes.c_long
    ULONG_PTR=ctypes.c_ulong
PLONG_PTR=ctypes.POINTER(LONG_PTR)
PULONG_PTR=ctypes.POINTER(ULONG_PTR)

PVOID=LPVOID=ctypes.c_void_p
HANDLE=ctypes.c_void_p
PHANDLE=LPHANDLE=ctypes.POINTER(HANDLE)
HWND=ctypes.c_void_p



##### Windows structures #####

class GUID(ctypes.Structure):
    _fields_=[  ("Data1",ctypes.c_ulong),
                ("Data2",ctypes.c_short),
                ("Data3",ctypes.c_short),
                ("Data4",ctypes.c_char*8) ]
LPGUID=ctypes.POINTER(GUID)


class OVERLAPPED(ctypes.Structure):
    _fields_=[  ("Internal",ULONG_PTR),
                ("InternalHigh",ULONG_PTR),
                ("Offset",DWORD),
                ("OffsetHigh",DWORD),
                ("hEvent",HANDLE) ]
LPOVERLAPPED=ctypes.POINTER(OVERLAPPED)


class COMMTIMEOUTS(ctypes.Structure):
    _fields_=[  ("ReadIntervalTimeout",DWORD),
                ("ReadTotalTimeoutMultiplier",DWORD),
                ("ReadTotalTimeoutConstant",DWORD),
                ("WriteTotalTimeoutMultiplier",DWORD),
                ("WriteTotalTimeoutConstant",DWORD) ]
LPCOMMTIMEOUTS=ctypes.POINTER(COMMTIMEOUTS)


class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_=[  ("nLength",DWORD),
                ("lpSecurityDescriptor",LPVOID),
                ("bInheritHandle",BOOL) ]
LPSECURITY_ATTRIBUTES=ctypes.POINTER(SECURITY_ATTRIBUTES)




##### Basic helper methods #####

def decorate(func, restype=None, argtypes=None, argnames=None, errcheck=None):
    """
    Decorate a ctypes function with the given result type, argument types,
    argument names (used for :mod:`.ctypes_wrap` wrapper) and error checker.

    Any ``None`` parameters are removed from the function.
    """
    func.restype=restype
    func.argtypes=argtypes or []
    if argnames is not None:
        func.argnames=argnames
    elif hasattr(func,"argnames"):
        del func.argnames
    if errcheck is not None:
        func.errcheck=errcheck
    elif hasattr(func,"errcheck"):
        del func.errcheck
    return func

def funcaddressof(func):
    """Get address of the given ctypes-wrapped function"""
    return ctypes.cast(ctypes.c_voidp(ctypes.addressof(func)),ctypes.POINTER(ctypes.c_voidp))[0]

def as_ctypes_array(lst, ctype):
    """Turn list of objects into a ctypes array of the given type"""
    v=(ctype*len(lst))()
    v[:]=lst[:]
    return v