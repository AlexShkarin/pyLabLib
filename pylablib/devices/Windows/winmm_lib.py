from ...core.devio.comm_backend import DeviceError
from ...core.utils import ctypes_wrap, ctypes_tools as ctt

import ctypes


drMMRESULT={
    0: "MMSYSERR_NOERROR",
    1: "MMSYSERR_ERROR",
    2: "MMSYSERR_BADDEVICEID",
    3: "MMSYSERR_NOTENABLED",
    4: "MMSYSERR_ALLOCATED",
    5: "MMSYSERR_INVALHANDLE",
    6: "MMSYSERR_NODRIVER",
    7: "MMSYSERR_NOMEM",
    8: "MMSYSERR_NOTSUPPORTED",
    9: "MMSYSERR_BADERRNUM",
    10: "MMSYSERR_INVALFLAG",
    11: "MMSYSERR_INVALPARAM",
    12: "MMSYSERR_HANDLEBUSY",
    13: "MMSYSERR_INVALIDALIAS",
    14: "MMSYSERR_BADDB",
    15: "MMSYSERR_KEYNOTFOUND",
    16: "MMSYSERR_READERROR",
    17: "MMSYSERR_WRITEERROR",
    18: "MMSYSERR_DELETEERROR",
    19: "MMSYSERR_VALNOTFOUND",
    20: "MMSYSERR_NODRIVERCB",
}
class WinMMError(DeviceError):
    """Generic WinMM error"""
    def __init__(self, func, code):
        self.func=func
        self.code=code
        self.name=drMMRESULT.get(self.code,"UNKNOWN")
        self.msg="function '{}' raised error {}({})".format(func,code,self.name)
        super().__init__(self.msg)
def errchecker():
    """A WinMM error checking function"""
    def errcheck(result, func, arguments):  # pylint: disable=unused-argument
        if result:
            raise WinMMError(func.__name__,result)
        return result
    return errcheck

MAXPNAMELEN=32
MAX_JOYSTICKOEMVXDNAME=260

class JOYCAPSA(ctypes.Structure):
    _fields_=[("wMid",ctt.WORD),
              ("wPid",ctt.WORD),
              ("szPname",ctypes.c_char*MAXPNAMELEN),
              ("wXmin",ctypes.c_uint),
              ("wXmax",ctypes.c_uint),
              ("wYmin",ctypes.c_uint),
              ("wYmax",ctypes.c_uint),
              ("wZmin",ctypes.c_uint),
              ("wZmax",ctypes.c_uint),
              ("wNumButtons",ctypes.c_uint),
              ("wPeriodMin",ctypes.c_uint),
              ("wPeriodMax",ctypes.c_uint),
              ("wRmin",ctypes.c_uint),
              ("wRmax",ctypes.c_uint),
              ("wUmin",ctypes.c_uint),
              ("wUmax",ctypes.c_uint),
              ("wVmin",ctypes.c_uint),
              ("wVmax",ctypes.c_uint),
              ("wCaps",ctypes.c_uint),
              ("wMaxAxes",ctypes.c_uint),
              ("wNumAxes",ctypes.c_uint),
              ("wMaxButtons",ctypes.c_uint),
              ("szRegKey",ctypes.c_char*MAXPNAMELEN),
              ("szOEMVxD",ctypes.c_char*MAX_JOYSTICKOEMVXDNAME),]
class CJOYCAPSA(ctypes_wrap.CStructWrapper):
    _struct=JOYCAPSA
class JOYINFO(ctypes.Structure):
    _fields_=[("wXpos",ctypes.c_uint),
              ("wYpos",ctypes.c_uint),
              ("wZpos",ctypes.c_uint),
              ("wButtons",ctypes.c_uint),]
class CJOYINFO(ctypes_wrap.CStructWrapper):
    _struct=JOYINFO
class JOYINFOEX(ctypes.Structure):
    _fields_=[("dwSize",ctt.DWORD),
              ("dwFlags",ctt.DWORD),
              ("dwXpos",ctt.DWORD),
              ("dwYpos",ctt.DWORD),
              ("dwZpos",ctt.DWORD),
              ("dwRpos",ctt.DWORD),
              ("dwUpos",ctt.DWORD),
              ("dwVpos",ctt.DWORD),
              ("dwButtons",ctt.DWORD),
              ("dwButtonNumber",ctt.DWORD),
              ("dwPOV",ctt.DWORD),
              ("dwReserved1",ctt.DWORD),
              ("dwReserved2",ctt.DWORD),]
class CJOYINFOEX(ctypes_wrap.CStructWrapper):
    _struct=JOYINFOEX

class WinMMLib:
    def __init__(self):
        self.lib=ctypes.cdll.winmm
        self.errcheck=errchecker()
        ctt.decorate(self.lib.joyGetNumDevs,restype=ctypes.c_uint,argtypes=[])
        ctt.decorate(self.lib.joyGetDevCapsA,restype=ctypes.c_uint,argtypes=[ctypes.c_uint,ctypes.POINTER(JOYCAPSA),ctypes.c_uint],errcheck=self.errcheck)
        ctt.decorate(self.lib.joyGetPos,restype=ctypes.c_uint,argtypes=[ctypes.c_uint,ctypes.POINTER(JOYINFO)],errcheck=self.errcheck)
        ctt.decorate(self.lib.joyGetPosEx,restype=ctypes.c_uint,argtypes=[ctypes.c_uint,ctypes.POINTER(JOYINFOEX)],errcheck=self.errcheck)
        self._caps=CJOYCAPSA.prep_struct()
        self._info=CJOYINFO.prep_struct()
        self._infoex=CJOYINFOEX.prep_struct()
    def joyGetNumDevs(self):
        return self.lib.joyGetNumDevs()
    def joyGetDevCapsA(self, idx):
        self.lib.joyGetDevCapsA(idx,ctypes.byref(self._caps),ctypes.sizeof(self._caps))
        return CJOYCAPSA.tup_struct(self._caps)
    def joyGetPos(self, idx):
        self.lib.joyGetPos(idx,ctypes.byref(self._info))
        return CJOYINFO.tup_struct(self._info)
    def joyGetPosEx(self, idx):
        self.lib.joyGetPosEx(idx,ctypes.byref(self._infoex))
        return CJOYINFOEX.tup_struct(self._infoex)