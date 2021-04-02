##########   This file is generated automatically based on ArcusPerformaxDriver.h   ##########


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### TYPE DEFINITIONS #####


BYTE=ctypes.c_ubyte
PBYTE=ctypes.POINTER(BYTE)
CHAR=ctypes.c_char
PCHAR=ctypes.POINTER(CHAR)
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
usb_dev_handle=None
AR_BOOL=ctypes.c_int
AR_DWORD=ctypes.c_long
AR_VOID=None
AR_HANDLE=ctypes.POINTER(usb_dev_handle)



##### FUNCTION DEFINITIONS #####





def define_functions(lib):
    #  AR_BOOL fnPerformaxComGetNumDevices(ctypes.POINTER(AR_DWORD) numDevices)
    lib.fnPerformaxComGetNumDevices.restype=AR_BOOL
    lib.fnPerformaxComGetNumDevices.argtypes=[ctypes.POINTER(AR_DWORD)]
    lib.fnPerformaxComGetNumDevices.argnames=["numDevices"]
    #  AR_BOOL fnPerformaxComGetProductString(AR_DWORD dwNumDevice, ctypes.c_void_p lpDeviceString, AR_DWORD dwOptions)
    lib.fnPerformaxComGetProductString.restype=AR_BOOL
    lib.fnPerformaxComGetProductString.argtypes=[AR_DWORD, ctypes.c_void_p, AR_DWORD]
    lib.fnPerformaxComGetProductString.argnames=["dwNumDevice", "lpDeviceString", "dwOptions"]
    #  AR_BOOL fnPerformaxComOpen(AR_DWORD dwDeviceNum, ctypes.POINTER(AR_HANDLE) pHandle)
    lib.fnPerformaxComOpen.restype=AR_BOOL
    lib.fnPerformaxComOpen.argtypes=[AR_DWORD, ctypes.POINTER(AR_HANDLE)]
    lib.fnPerformaxComOpen.argnames=["dwDeviceNum", "pHandle"]
    #  AR_BOOL fnPerformaxComClose(AR_HANDLE pHandle)
    lib.fnPerformaxComClose.restype=AR_BOOL
    lib.fnPerformaxComClose.argtypes=[AR_HANDLE]
    lib.fnPerformaxComClose.argnames=["pHandle"]
    #  AR_BOOL fnPerformaxComSetTimeouts(AR_DWORD dwReadTimeout, AR_DWORD dwWriteTimeout)
    lib.fnPerformaxComSetTimeouts.restype=AR_BOOL
    lib.fnPerformaxComSetTimeouts.argtypes=[AR_DWORD, AR_DWORD]
    lib.fnPerformaxComSetTimeouts.argnames=["dwReadTimeout", "dwWriteTimeout"]
    #  AR_BOOL fnPerformaxComSendRecv(AR_HANDLE Handle, ctypes.c_void_p wBuffer, AR_DWORD dwNumBytesToWrite, AR_DWORD dwNumBytesToRead, ctypes.c_void_p rBuffer)
    lib.fnPerformaxComSendRecv.restype=AR_BOOL
    lib.fnPerformaxComSendRecv.argtypes=[AR_HANDLE, ctypes.c_void_p, AR_DWORD, AR_DWORD, ctypes.c_void_p]
    lib.fnPerformaxComSendRecv.argnames=["Handle", "wBuffer", "dwNumBytesToWrite", "dwNumBytesToRead", "rBuffer"]
    #  AR_BOOL fnPerformaxComFlush(AR_HANDLE Handle)
    lib.fnPerformaxComFlush.restype=AR_BOOL
    lib.fnPerformaxComFlush.argtypes=[AR_HANDLE]
    lib.fnPerformaxComFlush.argnames=["Handle"]


