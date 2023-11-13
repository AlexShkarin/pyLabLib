##########   This file is generated automatically based on ShamrockCIF.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class SHAMROCK_ERR(enum.IntEnum):
    SHAMROCK_COMMUNICATION_ERROR = _int32(20201)
    SHAMROCK_SUCCESS             = _int32(20202)
    SHAMROCK_P1INVALID           = _int32(20266)
    SHAMROCK_P2INVALID           = _int32(20267)
    SHAMROCK_P3INVALID           = _int32(20268)
    SHAMROCK_P4INVALID           = _int32(20269)
    SHAMROCK_P5INVALID           = _int32(20270)
    SHAMROCK_NOT_INITIALIZED     = _int32(20275)
    SHAMROCK_NOT_AVAILABLE       = _int32(20292)
dSHAMROCK_ERR={a.name:a.value for a in SHAMROCK_ERR}
drSHAMROCK_ERR={a.value:a.name for a in SHAMROCK_ERR}


class SHAMROCK_CONST(enum.IntEnum):
    SHAMROCK_ACCESSORYMIN       = _int32(0)
    SHAMROCK_ACCESSORYMAX       = _int32(1)
    SHAMROCK_FILTERMIN          = _int32(1)
    SHAMROCK_FILTERMAX          = _int32(6)
    SHAMROCK_TURRETMIN          = _int32(1)
    SHAMROCK_TURRETMAX          = _int32(3)
    SHAMROCK_GRATINGMIN         = _int32(1)
    SHAMROCK_SLITWIDTHMIN       = _int32(10)
    SHAMROCK_SLITWIDTHMAX       = _int32(2500)
    SHAMROCK_I24SLITWIDTHMAX    = _int32(24000)
    SHAMROCK_SHUTTERMODEMIN     = _int32(0)
    SHAMROCK_SHUTTERMODEMAX     = _int32(2)
    SHAMROCK_DET_OFFSET_MIN     = _int32(-240000)
    SHAMROCK_DET_OFFSET_MAX     = _int32(240000)
    SHAMROCK_GRAT_OFFSET_MIN    = _int32(-20000)
    SHAMROCK_GRAT_OFFSET_MAX    = _int32(20000)
    SHAMROCK_SLIT_INDEX_MIN     = _int32(1)
    SHAMROCK_SLIT_INDEX_MAX     = _int32(4)
    SHAMROCK_INPUT_SLIT_SIDE    = _int32(1)
    SHAMROCK_INPUT_SLIT_DIRECT  = _int32(2)
    SHAMROCK_OUTPUT_SLIT_SIDE   = _int32(3)
    SHAMROCK_OUTPUT_SLIT_DIRECT = _int32(4)
    SHAMROCK_FLIPPER_INDEX_MIN  = _int32(1)
    SHAMROCK_FLIPPER_INDEX_MAX  = _int32(2)
    SHAMROCK_PORTMIN            = _int32(0)
    SHAMROCK_PORTMAX            = _int32(1)
    SHAMROCK_INPUT_FLIPPER      = _int32(1)
    SHAMROCK_OUTPUT_FLIPPER     = _int32(2)
    SHAMROCK_DIRECT_PORT        = _int32(0)
    SHAMROCK_SIDE_PORT          = _int32(1)
dSHAMROCK_CONST={a.name:a.value for a in SHAMROCK_CONST}
drSHAMROCK_CONST={a.value:a.name for a in SHAMROCK_CONST}





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
DWORD=ctypes.c_ulong
LPWORD=ctypes.POINTER(WORD)
LONG=ctypes.c_long
LONGLONG=ctypes.c_int64
LPLONG=ctypes.POINTER(ctypes.c_long)
HANDLE=ctypes.c_void_p
LPHANDLE=ctypes.POINTER(HANDLE)
PHANDLE=ctypes.POINTER(HANDLE)
HWND=ctypes.c_void_p
HGLOBAL=ctypes.c_void_p
HINSTANCE=ctypes.c_void_p
HDC=ctypes.c_void_p
HMODULE=ctypes.c_void_p
HKEY=ctypes.c_void_p
PVOID=ctypes.c_void_p
LPVOID=ctypes.c_void_p
class RECT(ctypes.Structure):
    _fields_=[  ("left",LONG),
                ("top",LONG),
                ("right",LONG),
                ("bottom",LONG) ]
PRECT=ctypes.POINTER(RECT)
class CRECT(ctypes_wrap.CStructWrapper):
    _struct=RECT


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_=[  ("biSize",DWORD),
                ("biWidth",LONG),
                ("biHeight",LONG),
                ("biPlanes",WORD),
                ("biBitCount",WORD),
                ("biCompression",DWORD),
                ("biSizeImage",DWORD),
                ("biXPelsPerMeter",LONG),
                ("biYPelsPerMeter",LONG),
                ("biClrUsed",DWORD),
                ("biClrImportant",DWORD) ]
PBITMAPINFOHEADER=ctypes.POINTER(BITMAPINFOHEADER)
class CBITMAPINFOHEADER(ctypes_wrap.CStructWrapper):
    _struct=BITMAPINFOHEADER





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
    #  ctypes.c_uint ShamrockInitialize(ctypes.c_char_p IniPath)
    addfunc(lib, "ShamrockInitialize", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p],
            argnames = ["IniPath"] )
    #  ctypes.c_uint ShamrockClose()
    addfunc(lib, "ShamrockClose", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint ShamrockGetNumberDevices(ctypes.POINTER(ctypes.c_int) nodevices)
    addfunc(lib, "ShamrockGetNumberDevices", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["nodevices"] )
    #  ctypes.c_uint ShamrockGetFunctionReturnDescription(ctypes.c_int error, ctypes.c_char_p description, ctypes.c_int MaxDescStrLen)
    addfunc(lib, "ShamrockGetFunctionReturnDescription", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int],
            argnames = ["error", "description", "MaxDescStrLen"] )
    #  ctypes.c_uint ShamrockGetSerialNumber(ctypes.c_int device, ctypes.c_char_p serial)
    addfunc(lib, "ShamrockGetSerialNumber", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_char_p],
            argnames = ["device", "serial"] )
    #  ctypes.c_uint ShamrockEepromSetOpticalParams(ctypes.c_int device, ctypes.c_float FocalLength, ctypes.c_float AngularDeviation, ctypes.c_float FocalTilt)
    addfunc(lib, "ShamrockEepromSetOpticalParams", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_float],
            argnames = ["device", "FocalLength", "AngularDeviation", "FocalTilt"] )
    #  ctypes.c_uint ShamrockEepromGetOpticalParams(ctypes.c_int device, ctypes.POINTER(ctypes.c_float) FocalLength, ctypes.POINTER(ctypes.c_float) AngularDeviation, ctypes.POINTER(ctypes.c_float) FocalTilt)
    addfunc(lib, "ShamrockEepromGetOpticalParams", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)],
            argnames = ["device", "FocalLength", "AngularDeviation", "FocalTilt"] )
    #  ctypes.c_uint ShamrockSetGrating(ctypes.c_int device, ctypes.c_int grating)
    addfunc(lib, "ShamrockSetGrating", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["device", "grating"] )
    #  ctypes.c_uint ShamrockGetGrating(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) grating)
    addfunc(lib, "ShamrockGetGrating", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "grating"] )
    #  ctypes.c_uint ShamrockWavelengthReset(ctypes.c_int device)
    addfunc(lib, "ShamrockWavelengthReset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["device"] )
    #  ctypes.c_uint ShamrockGetNumberGratings(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) noGratings)
    addfunc(lib, "ShamrockGetNumberGratings", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "noGratings"] )
    #  ctypes.c_uint ShamrockGetGratingInfo(ctypes.c_int device, ctypes.c_int Grating, ctypes.POINTER(ctypes.c_float) Lines, ctypes.c_char_p Blaze, ctypes.POINTER(ctypes.c_int) Home, ctypes.POINTER(ctypes.c_int) Offset)
    addfunc(lib, "ShamrockGetGratingInfo", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "Grating", "Lines", "Blaze", "Home", "Offset"] )
    #  ctypes.c_uint ShamrockSetDetectorOffset(ctypes.c_int device, ctypes.c_int offset)
    addfunc(lib, "ShamrockSetDetectorOffset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["device", "offset"] )
    #  ctypes.c_uint ShamrockGetDetectorOffset(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) offset)
    addfunc(lib, "ShamrockGetDetectorOffset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "offset"] )
    #  ctypes.c_uint ShamrockSetDetectorOffsetPort2(ctypes.c_int device, ctypes.c_int offset)
    addfunc(lib, "ShamrockSetDetectorOffsetPort2", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["device", "offset"] )
    #  ctypes.c_uint ShamrockGetDetectorOffsetPort2(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) offset)
    addfunc(lib, "ShamrockGetDetectorOffsetPort2", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "offset"] )
    #  ctypes.c_uint ShamrockSetDetectorOffsetEx(ctypes.c_int device, ctypes.c_int entrancePort, ctypes.c_int exitPort, ctypes.c_int offset)
    addfunc(lib, "ShamrockSetDetectorOffsetEx", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["device", "entrancePort", "exitPort", "offset"] )
    #  ctypes.c_uint ShamrockGetDetectorOffsetEx(ctypes.c_int device, ctypes.c_int entrancePort, ctypes.c_int exitPort, ctypes.POINTER(ctypes.c_int) offset)
    addfunc(lib, "ShamrockGetDetectorOffsetEx", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "entrancePort", "exitPort", "offset"] )
    #  ctypes.c_uint ShamrockSetGratingOffset(ctypes.c_int device, ctypes.c_int Grating, ctypes.c_int offset)
    addfunc(lib, "ShamrockSetGratingOffset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["device", "Grating", "offset"] )
    #  ctypes.c_uint ShamrockGetGratingOffset(ctypes.c_int device, ctypes.c_int Grating, ctypes.POINTER(ctypes.c_int) offset)
    addfunc(lib, "ShamrockGetGratingOffset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "Grating", "offset"] )
    #  ctypes.c_uint ShamrockGratingIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
    addfunc(lib, "ShamrockGratingIsPresent", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "present"] )
    #  ctypes.c_uint ShamrockSetTurret(ctypes.c_int device, ctypes.c_int Turret)
    addfunc(lib, "ShamrockSetTurret", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["device", "Turret"] )
    #  ctypes.c_uint ShamrockGetTurret(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) Turret)
    addfunc(lib, "ShamrockGetTurret", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "Turret"] )
    #  ctypes.c_uint ShamrockSetWavelength(ctypes.c_int device, ctypes.c_float wavelength)
    addfunc(lib, "ShamrockSetWavelength", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_float],
            argnames = ["device", "wavelength"] )
    #  ctypes.c_uint ShamrockGetWavelength(ctypes.c_int device, ctypes.POINTER(ctypes.c_float) wavelength)
    addfunc(lib, "ShamrockGetWavelength", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["device", "wavelength"] )
    #  ctypes.c_uint ShamrockGotoZeroOrder(ctypes.c_int device)
    addfunc(lib, "ShamrockGotoZeroOrder", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["device"] )
    #  ctypes.c_uint ShamrockAtZeroOrder(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) atZeroOrder)
    addfunc(lib, "ShamrockAtZeroOrder", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "atZeroOrder"] )
    #  ctypes.c_uint ShamrockGetWavelengthLimits(ctypes.c_int device, ctypes.c_int Grating, ctypes.POINTER(ctypes.c_float) Min, ctypes.POINTER(ctypes.c_float) Max)
    addfunc(lib, "ShamrockGetWavelengthLimits", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)],
            argnames = ["device", "Grating", "Min", "Max"] )
    #  ctypes.c_uint ShamrockWavelengthIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
    addfunc(lib, "ShamrockWavelengthIsPresent", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "present"] )
    #  ctypes.c_uint ShamrockSetAutoSlitWidth(ctypes.c_int device, ctypes.c_int index, ctypes.c_float width)
    addfunc(lib, "ShamrockSetAutoSlitWidth", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_float],
            argnames = ["device", "index", "width"] )
    #  ctypes.c_uint ShamrockGetAutoSlitWidth(ctypes.c_int device, ctypes.c_int index, ctypes.POINTER(ctypes.c_float) width)
    addfunc(lib, "ShamrockGetAutoSlitWidth", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["device", "index", "width"] )
    #  ctypes.c_uint ShamrockAutoSlitReset(ctypes.c_int device, ctypes.c_int index)
    addfunc(lib, "ShamrockAutoSlitReset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["device", "index"] )
    #  ctypes.c_uint ShamrockAutoSlitIsPresent(ctypes.c_int device, ctypes.c_int index, ctypes.POINTER(ctypes.c_int) present)
    addfunc(lib, "ShamrockAutoSlitIsPresent", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "index", "present"] )
    #  ctypes.c_uint ShamrockSetAutoSlitCoefficients(ctypes.c_int device, ctypes.c_int index, ctypes.c_int x1, ctypes.c_int y1, ctypes.c_int x2, ctypes.c_int y2)
    addfunc(lib, "ShamrockSetAutoSlitCoefficients", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["device", "index", "x1", "y1", "x2", "y2"] )
    #  ctypes.c_uint ShamrockGetAutoSlitCoefficients(ctypes.c_int device, ctypes.c_int index, ctypes.POINTER(ctypes.c_int) x1, ctypes.POINTER(ctypes.c_int) y1, ctypes.POINTER(ctypes.c_int) x2, ctypes.POINTER(ctypes.c_int) y2)
    addfunc(lib, "ShamrockGetAutoSlitCoefficients", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "index", "x1", "y1", "x2", "y2"] )
    #  ctypes.c_uint ShamrockSetSlitZeroPosition(ctypes.c_int device, ctypes.c_int index, ctypes.c_int offset)
    addfunc(lib, "ShamrockSetSlitZeroPosition", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["device", "index", "offset"] )
    #  ctypes.c_uint ShamrockGetSlitZeroPosition(ctypes.c_int device, ctypes.c_int index, ctypes.POINTER(ctypes.c_int) offset)
    addfunc(lib, "ShamrockGetSlitZeroPosition", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "index", "offset"] )
    #  ctypes.c_uint ShamrockSetSlit(ctypes.c_int device, ctypes.c_float width)
    addfunc(lib, "ShamrockSetSlit", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_float],
            argnames = ["device", "width"] )
    #  ctypes.c_uint ShamrockGetSlit(ctypes.c_int device, ctypes.POINTER(ctypes.c_float) width)
    addfunc(lib, "ShamrockGetSlit", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["device", "width"] )
    #  ctypes.c_uint ShamrockSlitReset(ctypes.c_int device)
    addfunc(lib, "ShamrockSlitReset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["device"] )
    #  ctypes.c_uint ShamrockSlitIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
    addfunc(lib, "ShamrockSlitIsPresent", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "present"] )
    #  ctypes.c_uint ShamrockSetSlitCoefficients(ctypes.c_int device, ctypes.c_int x1, ctypes.c_int y1, ctypes.c_int x2, ctypes.c_int y2)
    addfunc(lib, "ShamrockSetSlitCoefficients", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["device", "x1", "y1", "x2", "y2"] )
    #  ctypes.c_uint ShamrockGetSlitCoefficients(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) x1, ctypes.POINTER(ctypes.c_int) y1, ctypes.POINTER(ctypes.c_int) x2, ctypes.POINTER(ctypes.c_int) y2)
    addfunc(lib, "ShamrockGetSlitCoefficients", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "x1", "y1", "x2", "y2"] )
    #  ctypes.c_uint ShamrockSetOutputSlit(ctypes.c_int device, ctypes.c_float width)
    addfunc(lib, "ShamrockSetOutputSlit", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_float],
            argnames = ["device", "width"] )
    #  ctypes.c_uint ShamrockGetOutputSlit(ctypes.c_int device, ctypes.POINTER(ctypes.c_float) width)
    addfunc(lib, "ShamrockGetOutputSlit", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["device", "width"] )
    #  ctypes.c_uint ShamrockOutputSlitReset(ctypes.c_int device)
    addfunc(lib, "ShamrockOutputSlitReset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["device"] )
    #  ctypes.c_uint ShamrockOutputSlitIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
    addfunc(lib, "ShamrockOutputSlitIsPresent", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "present"] )
    #  ctypes.c_uint ShamrockSetShutter(ctypes.c_int device, ctypes.c_int mode)
    addfunc(lib, "ShamrockSetShutter", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["device", "mode"] )
    #  ctypes.c_uint ShamrockGetShutter(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) mode)
    addfunc(lib, "ShamrockGetShutter", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "mode"] )
    #  ctypes.c_uint ShamrockIsModePossible(ctypes.c_int device, ctypes.c_int mode, ctypes.POINTER(ctypes.c_int) possible)
    addfunc(lib, "ShamrockIsModePossible", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "mode", "possible"] )
    #  ctypes.c_uint ShamrockShutterIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
    addfunc(lib, "ShamrockShutterIsPresent", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "present"] )
    #  ctypes.c_uint ShamrockSetFilter(ctypes.c_int device, ctypes.c_int filter)
    addfunc(lib, "ShamrockSetFilter", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["device", "filter"] )
    #  ctypes.c_uint ShamrockGetFilter(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) filter)
    addfunc(lib, "ShamrockGetFilter", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "filter"] )
    #  ctypes.c_uint ShamrockGetFilterInfo(ctypes.c_int device, ctypes.c_int Filter, ctypes.c_char_p Info)
    addfunc(lib, "ShamrockGetFilterInfo", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p],
            argnames = ["device", "Filter", "Info"] )
    #  ctypes.c_uint ShamrockSetFilterInfo(ctypes.c_int device, ctypes.c_int Filter, ctypes.c_char_p Info)
    addfunc(lib, "ShamrockSetFilterInfo", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p],
            argnames = ["device", "Filter", "Info"] )
    #  ctypes.c_uint ShamrockFilterReset(ctypes.c_int device)
    addfunc(lib, "ShamrockFilterReset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["device"] )
    #  ctypes.c_uint ShamrockFilterIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
    addfunc(lib, "ShamrockFilterIsPresent", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "present"] )
    #  ctypes.c_uint ShamrockSetFlipperMirror(ctypes.c_int device, ctypes.c_int flipper, ctypes.c_int port)
    addfunc(lib, "ShamrockSetFlipperMirror", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["device", "flipper", "port"] )
    #  ctypes.c_uint ShamrockGetFlipperMirror(ctypes.c_int device, ctypes.c_int flipper, ctypes.POINTER(ctypes.c_int) port)
    addfunc(lib, "ShamrockGetFlipperMirror", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "flipper", "port"] )
    #  ctypes.c_uint ShamrockFlipperMirrorReset(ctypes.c_int device, ctypes.c_int flipper)
    addfunc(lib, "ShamrockFlipperMirrorReset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["device", "flipper"] )
    #  ctypes.c_uint ShamrockFlipperMirrorIsPresent(ctypes.c_int device, ctypes.c_int flipper, ctypes.POINTER(ctypes.c_int) present)
    addfunc(lib, "ShamrockFlipperMirrorIsPresent", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "flipper", "present"] )
    #  ctypes.c_uint ShamrockGetCCDLimits(ctypes.c_int device, ctypes.c_int port, ctypes.POINTER(ctypes.c_float) Low, ctypes.POINTER(ctypes.c_float) High)
    addfunc(lib, "ShamrockGetCCDLimits", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)],
            argnames = ["device", "port", "Low", "High"] )
    #  ctypes.c_uint ShamrockSetFlipperMirrorPosition(ctypes.c_int device, ctypes.c_int flipper, ctypes.c_int position)
    addfunc(lib, "ShamrockSetFlipperMirrorPosition", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["device", "flipper", "position"] )
    #  ctypes.c_uint ShamrockGetFlipperMirrorPosition(ctypes.c_int device, ctypes.c_int flipper, ctypes.POINTER(ctypes.c_int) position)
    addfunc(lib, "ShamrockGetFlipperMirrorPosition", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "flipper", "position"] )
    #  ctypes.c_uint ShamrockGetFlipperMirrorMaxPosition(ctypes.c_int device, ctypes.c_int flipper, ctypes.POINTER(ctypes.c_int) max)
    addfunc(lib, "ShamrockGetFlipperMirrorMaxPosition", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "flipper", "max"] )
    #  ctypes.c_uint ShamrockSetPort(ctypes.c_int device, ctypes.c_int port)
    addfunc(lib, "ShamrockSetPort", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["device", "port"] )
    #  ctypes.c_uint ShamrockGetPort(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) port)
    addfunc(lib, "ShamrockGetPort", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "port"] )
    #  ctypes.c_uint ShamrockFlipperReset(ctypes.c_int device)
    addfunc(lib, "ShamrockFlipperReset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["device"] )
    #  ctypes.c_uint ShamrockFlipperIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
    addfunc(lib, "ShamrockFlipperIsPresent", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "present"] )
    #  ctypes.c_uint ShamrockSetAccessory(ctypes.c_int device, ctypes.c_int Accessory, ctypes.c_int State)
    addfunc(lib, "ShamrockSetAccessory", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["device", "Accessory", "State"] )
    #  ctypes.c_uint ShamrockGetAccessoryState(ctypes.c_int device, ctypes.c_int Accessory, ctypes.POINTER(ctypes.c_int) state)
    addfunc(lib, "ShamrockGetAccessoryState", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "Accessory", "state"] )
    #  ctypes.c_uint ShamrockAccessoryIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
    addfunc(lib, "ShamrockAccessoryIsPresent", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "present"] )
    #  ctypes.c_uint ShamrockSetFocusMirror(ctypes.c_int device, ctypes.c_int focus)
    addfunc(lib, "ShamrockSetFocusMirror", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["device", "focus"] )
    #  ctypes.c_uint ShamrockGetFocusMirror(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) focus)
    addfunc(lib, "ShamrockGetFocusMirror", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "focus"] )
    #  ctypes.c_uint ShamrockGetFocusMirrorMaxSteps(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) steps)
    addfunc(lib, "ShamrockGetFocusMirrorMaxSteps", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "steps"] )
    #  ctypes.c_uint ShamrockFocusMirrorReset(ctypes.c_int device)
    addfunc(lib, "ShamrockFocusMirrorReset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["device"] )
    #  ctypes.c_uint ShamrockFocusMirrorIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
    addfunc(lib, "ShamrockFocusMirrorIsPresent", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "present"] )
    #  ctypes.c_uint ShamrockSetPixelWidth(ctypes.c_int device, ctypes.c_float Width)
    addfunc(lib, "ShamrockSetPixelWidth", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_float],
            argnames = ["device", "Width"] )
    #  ctypes.c_uint ShamrockSetNumberPixels(ctypes.c_int device, ctypes.c_int NumberPixels)
    addfunc(lib, "ShamrockSetNumberPixels", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["device", "NumberPixels"] )
    #  ctypes.c_uint ShamrockGetPixelWidth(ctypes.c_int device, ctypes.POINTER(ctypes.c_float) Width)
    addfunc(lib, "ShamrockGetPixelWidth", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["device", "Width"] )
    #  ctypes.c_uint ShamrockGetNumberPixels(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) NumberPixels)
    addfunc(lib, "ShamrockGetNumberPixels", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "NumberPixels"] )
    #  ctypes.c_uint ShamrockGetCalibration(ctypes.c_int device, ctypes.POINTER(ctypes.c_float) CalibrationValues, ctypes.c_int NumberPixels)
    addfunc(lib, "ShamrockGetCalibration", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_int],
            argnames = ["device", "CalibrationValues", "NumberPixels"] )
    #  ctypes.c_uint ShamrockGetPixelCalibrationCoefficients(ctypes.c_int device, ctypes.POINTER(ctypes.c_float) A, ctypes.POINTER(ctypes.c_float) B, ctypes.POINTER(ctypes.c_float) C, ctypes.POINTER(ctypes.c_float) D)
    addfunc(lib, "ShamrockGetPixelCalibrationCoefficients", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)],
            argnames = ["device", "A", "B", "C", "D"] )
    #  ctypes.c_uint ShamrockIrisIsPresent(ctypes.c_int device, ctypes.c_int iris, ctypes.POINTER(ctypes.c_int) present)
    addfunc(lib, "ShamrockIrisIsPresent", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "iris", "present"] )
    #  ctypes.c_uint ShamrockSetIris(ctypes.c_int device, ctypes.c_int iris, ctypes.c_int value)
    addfunc(lib, "ShamrockSetIris", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["device", "iris", "value"] )
    #  ctypes.c_uint ShamrockGetIris(ctypes.c_int device, ctypes.c_int iris, ctypes.POINTER(ctypes.c_int) value)
    addfunc(lib, "ShamrockGetIris", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "iris", "value"] )
    #  ctypes.c_uint ShamrockFocusMirrorTiltIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
    addfunc(lib, "ShamrockFocusMirrorTiltIsPresent", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "present"] )
    #  ctypes.c_uint ShamrockSetFocusMirrorTilt(ctypes.c_int device, ctypes.c_int tilt)
    addfunc(lib, "ShamrockSetFocusMirrorTilt", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["device", "tilt"] )
    #  ctypes.c_uint ShamrockGetFocusMirrorTilt(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) tilt)
    addfunc(lib, "ShamrockGetFocusMirrorTilt", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "tilt"] )
    #  ctypes.c_uint ShamrockSetFocusMirrorTiltOffset(ctypes.c_int device, ctypes.c_int entrancePort, ctypes.c_int exitPort, ctypes.c_int offset)
    addfunc(lib, "ShamrockSetFocusMirrorTiltOffset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["device", "entrancePort", "exitPort", "offset"] )
    #  ctypes.c_uint ShamrockGetFocusMirrorTiltOffset(ctypes.c_int device, ctypes.c_int entrancePort, ctypes.c_int exitPort, ctypes.POINTER(ctypes.c_int) offset)
    addfunc(lib, "ShamrockGetFocusMirrorTiltOffset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["device", "entrancePort", "exitPort", "offset"] )
    #  ctypes.c_uint ShamrockMoveTurretToSafeChangePosition(ctypes.c_int device)
    addfunc(lib, "ShamrockMoveTurretToSafeChangePosition", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["device"] )


