##########   This file is generated automatically based on ArcusPerformaxDriver.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




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
usb_dev_handle=None
AR_BOOL=ctypes.c_int
AR_DWORD=ctypes.c_long
AR_VOID=None
AR_HANDLE=ctypes.c_void_p



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
    #  AR_BOOL fnPerformaxComGetNumDevices(ctypes.POINTER(AR_DWORD) numDevices)
    addfunc(lib, "fnPerformaxComGetNumDevices", restype = AR_BOOL,
            argtypes = [ctypes.POINTER(AR_DWORD)],
            argnames = ["numDevices"] )
    #  AR_BOOL fnPerformaxComGetProductString(AR_DWORD dwNumDevice, ctypes.c_void_p lpDeviceString, AR_DWORD dwOptions)
    addfunc(lib, "fnPerformaxComGetProductString", restype = AR_BOOL,
            argtypes = [AR_DWORD, ctypes.c_void_p, AR_DWORD],
            argnames = ["dwNumDevice", "lpDeviceString", "dwOptions"] )
    #  AR_BOOL fnPerformaxComOpen(AR_DWORD dwDeviceNum, ctypes.POINTER(AR_HANDLE) pHandle)
    addfunc(lib, "fnPerformaxComOpen", restype = AR_BOOL,
            argtypes = [AR_DWORD, ctypes.POINTER(AR_HANDLE)],
            argnames = ["dwDeviceNum", "pHandle"] )
    #  AR_BOOL fnPerformaxComClose(AR_HANDLE pHandle)
    addfunc(lib, "fnPerformaxComClose", restype = AR_BOOL,
            argtypes = [AR_HANDLE],
            argnames = ["pHandle"] )
    #  AR_BOOL fnPerformaxComSetTimeouts(AR_DWORD dwReadTimeout, AR_DWORD dwWriteTimeout)
    addfunc(lib, "fnPerformaxComSetTimeouts", restype = AR_BOOL,
            argtypes = [AR_DWORD, AR_DWORD],
            argnames = ["dwReadTimeout", "dwWriteTimeout"] )
    #  AR_BOOL fnPerformaxComSendRecv(AR_HANDLE Handle, ctypes.c_void_p wBuffer, AR_DWORD dwNumBytesToWrite, AR_DWORD dwNumBytesToRead, ctypes.c_void_p rBuffer)
    addfunc(lib, "fnPerformaxComSendRecv", restype = AR_BOOL,
            argtypes = [AR_HANDLE, ctypes.c_void_p, AR_DWORD, AR_DWORD, ctypes.c_void_p],
            argnames = ["Handle", "wBuffer", "dwNumBytesToWrite", "dwNumBytesToRead", "rBuffer"] )
    #  AR_BOOL fnPerformaxComFlush(AR_HANDLE Handle)
    addfunc(lib, "fnPerformaxComFlush", restype = AR_BOOL,
            argtypes = [AR_HANDLE],
            argnames = ["Handle"] )


