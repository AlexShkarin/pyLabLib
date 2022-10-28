##########   This file is generated automatically based on NewClassic_USBCamera_SDK.h   ##########

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


SDK_RETURN_CODE=ctypes.c_int
class TImageControl(ctypes.Structure):
    _fields_=[  ("Revision",ctypes.c_int),
                ("Resolution",ctypes.c_int),
                ("ExposureTime",ctypes.c_int),
                ("GpioConfigByte",ctypes.c_ubyte),
                ("GpioCurrentSet",ctypes.c_ubyte) ]
PTImageControl=ctypes.POINTER(TImageControl)
class CTImageControl(ctypes_wrap.CStructWrapper):
    _struct=TImageControl


class TProcessedDataProperty(ctypes.Structure):
    _fields_=[  ("CameraID",ctypes.c_int),
                ("Row",ctypes.c_int),
                ("Column",ctypes.c_int),
                ("Bin",ctypes.c_int),
                ("XStart",ctypes.c_int),
                ("YStart",ctypes.c_int),
                ("ExposureTime",ctypes.c_int),
                ("RedGain",ctypes.c_int),
                ("GreenGain",ctypes.c_int),
                ("BlueGain",ctypes.c_int),
                ("TimeStamp",ctypes.c_int),
                ("TriggerOccurred",ctypes.c_int),
                ("TriggerEventCount",ctypes.c_int),
                ("ProcessFrameType",ctypes.c_int) ]
PTProcessedDataProperty=ctypes.POINTER(TProcessedDataProperty)
class CTProcessedDataProperty(ctypes_wrap.CStructWrapper):
    _struct=TProcessedDataProperty


PImageCtl=ctypes.POINTER(TImageControl)
DeviceFaultCallBack=ctypes.c_void_p
FrameDataCallBack=ctypes.c_void_p



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
    #  SDK_RETURN_CODE NewClassicUSB_InitDevice()
    addfunc(lib, "NewClassicUSB_InitDevice", restype = SDK_RETURN_CODE,
            argtypes = [],
            argnames = [] )
    #  SDK_RETURN_CODE NewClassicUSB_UnInitDevice()
    addfunc(lib, "NewClassicUSB_UnInitDevice", restype = SDK_RETURN_CODE,
            argtypes = [],
            argnames = [] )
    #  SDK_RETURN_CODE NewClassicUSB_GetModuleNoSerialNo(ctypes.c_int DeviceID, ctypes.c_char_p ModuleNo, ctypes.c_char_p SerialNo)
    addfunc(lib, "NewClassicUSB_GetModuleNoSerialNo", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p],
            argnames = ["DeviceID", "ModuleNo", "SerialNo"] )
    #  SDK_RETURN_CODE NewClassicUSB_AddDeviceToWorkingSet(ctypes.c_int DeviceID)
    addfunc(lib, "NewClassicUSB_AddDeviceToWorkingSet", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int],
            argnames = ["DeviceID"] )
    #  SDK_RETURN_CODE NewClassicUSB_RemoveDeviceFromWorkingSet(ctypes.c_int DeviceID)
    addfunc(lib, "NewClassicUSB_RemoveDeviceFromWorkingSet", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int],
            argnames = ["DeviceID"] )
    #  SDK_RETURN_CODE NewClassicUSB_ActiveDeviceInWorkingSet(ctypes.c_int DeviceID, ctypes.c_int Active)
    addfunc(lib, "NewClassicUSB_ActiveDeviceInWorkingSet", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["DeviceID", "Active"] )
    #  SDK_RETURN_CODE NewClassicUSB_StartCameraEngine(HWND ParentHandle, ctypes.c_int CameraBitOption)
    addfunc(lib, "NewClassicUSB_StartCameraEngine", restype = SDK_RETURN_CODE,
            argtypes = [HWND, ctypes.c_int],
            argnames = ["ParentHandle", "CameraBitOption"] )
    #  SDK_RETURN_CODE NewClassicUSB_StopCameraEngine()
    addfunc(lib, "NewClassicUSB_StopCameraEngine", restype = SDK_RETURN_CODE,
            argtypes = [],
            argnames = [] )
    #  SDK_RETURN_CODE NewClassicUSB_SetCameraWorkMode(ctypes.c_int DeviceID, ctypes.c_int WorkMode)
    addfunc(lib, "NewClassicUSB_SetCameraWorkMode", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["DeviceID", "WorkMode"] )
    #  SDK_RETURN_CODE NewClassicUSB_StartFrameGrab(ctypes.c_int TotalFrames)
    addfunc(lib, "NewClassicUSB_StartFrameGrab", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int],
            argnames = ["TotalFrames"] )
    #  SDK_RETURN_CODE NewClassicUSB_StopFrameGrab()
    addfunc(lib, "NewClassicUSB_StopFrameGrab", restype = SDK_RETURN_CODE,
            argtypes = [],
            argnames = [] )
    #  SDK_RETURN_CODE NewClassicUSB_ShowFactoryControlPanel(ctypes.c_int DeviceID, ctypes.c_char_p passWord)
    addfunc(lib, "NewClassicUSB_ShowFactoryControlPanel", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_char_p],
            argnames = ["DeviceID", "passWord"] )
    #  SDK_RETURN_CODE NewClassicUSB_HideFactoryControlPanel()
    addfunc(lib, "NewClassicUSB_HideFactoryControlPanel", restype = SDK_RETURN_CODE,
            argtypes = [],
            argnames = [] )
    #  SDK_RETURN_CODE NewClassicUSB_SetBayerFilterType(ctypes.c_int FilterType)
    addfunc(lib, "NewClassicUSB_SetBayerFilterType", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int],
            argnames = ["FilterType"] )
    #  SDK_RETURN_CODE NewClassicUSB_SetResolution(ctypes.c_int deviceID, ctypes.c_int Resolution, ctypes.c_int Bin)
    addfunc(lib, "NewClassicUSB_SetResolution", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["deviceID", "Resolution", "Bin"] )
    #  SDK_RETURN_CODE NewClassicUSB_SetCustomizedResolution(ctypes.c_int deviceID, ctypes.c_int RowSize, ctypes.c_int ColSize, ctypes.c_int Bin)
    addfunc(lib, "NewClassicUSB_SetCustomizedResolution", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["deviceID", "RowSize", "ColSize", "Bin"] )
    #  SDK_RETURN_CODE NewClassicUSB_SetExposureTime(ctypes.c_int DeviceID, ctypes.c_int exposureTime)
    addfunc(lib, "NewClassicUSB_SetExposureTime", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["DeviceID", "exposureTime"] )
    #  SDK_RETURN_CODE NewClassicUSB_SetXYStart(ctypes.c_int deviceID, ctypes.c_int XStart, ctypes.c_int YStart)
    addfunc(lib, "NewClassicUSB_SetXYStart", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["deviceID", "XStart", "YStart"] )
    #  SDK_RETURN_CODE NewClassicUSB_SetGains(ctypes.c_int deviceID, ctypes.c_int RedGain, ctypes.c_int GreenGain, ctypes.c_int BlueGain)
    addfunc(lib, "NewClassicUSB_SetGains", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["deviceID", "RedGain", "GreenGain", "BlueGain"] )
    #  SDK_RETURN_CODE NewClassicUSB_SetGamma(ctypes.c_int Gamma, ctypes.c_int Contrast, ctypes.c_int Bright, ctypes.c_int Sharp)
    addfunc(lib, "NewClassicUSB_SetGamma", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["Gamma", "Contrast", "Bright", "Sharp"] )
    #  SDK_RETURN_CODE NewClassicUSB_SetBWMode(ctypes.c_int BWMode, ctypes.c_int H_Mirror, ctypes.c_int V_Flip)
    addfunc(lib, "NewClassicUSB_SetBWMode", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["BWMode", "H_Mirror", "V_Flip"] )
    #  SDK_RETURN_CODE NewClassicUSB_SetMinimumFrameDelay(ctypes.c_int IsMinimumFrameDelay)
    addfunc(lib, "NewClassicUSB_SetMinimumFrameDelay", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int],
            argnames = ["IsMinimumFrameDelay"] )
    #  SDK_RETURN_CODE NewClassicUSB_SoftTrigger(ctypes.c_int DeviceID)
    addfunc(lib, "NewClassicUSB_SoftTrigger", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int],
            argnames = ["DeviceID"] )
    #  SDK_RETURN_CODE NewClassicUSB_SetSensorFrequency(ctypes.c_int DeviceID, ctypes.c_int Frequency)
    addfunc(lib, "NewClassicUSB_SetSensorFrequency", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["DeviceID", "Frequency"] )
    #  SDK_RETURN_CODE NewClassicUSB_SetHBlankingExtension(ctypes.c_int DeviceID, ctypes.c_int HBlanking)
    addfunc(lib, "NewClassicUSB_SetHBlankingExtension", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["DeviceID", "HBlanking"] )
    #  SDK_RETURN_CODE NewClassicUSB_InstallFrameHooker(ctypes.c_int FrameType, FrameDataCallBack FrameHooker)
    addfunc(lib, "NewClassicUSB_InstallFrameHooker", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, FrameDataCallBack],
            argnames = ["FrameType", "FrameHooker"] )
    #  SDK_RETURN_CODE NewClassicUSB_InstallUSBDeviceHooker(DeviceFaultCallBack USBDeviceHooker)
    addfunc(lib, "NewClassicUSB_InstallUSBDeviceHooker", restype = SDK_RETURN_CODE,
            argtypes = [DeviceFaultCallBack],
            argnames = ["USBDeviceHooker"] )
    #  ctypes.POINTER(ctypes.c_ubyte) NewClassicUSB_GetCurrentFrame(ctypes.c_int FrameType, ctypes.c_int deviceID, ctypes.POINTER(BYTE) FramePtr)
    addfunc(lib, "NewClassicUSB_GetCurrentFrame", restype = ctypes.POINTER(ctypes.c_ubyte),
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(BYTE)],
            argnames = ["FrameType", "deviceID", "FramePtr"] )
    #  SDK_RETURN_CODE NewClassicUSB_GetDevicesErrorState()
    addfunc(lib, "NewClassicUSB_GetDevicesErrorState", restype = SDK_RETURN_CODE,
            argtypes = [],
            argnames = [] )
    #  SDK_RETURN_CODE NewClassicUSB_SetGPIOConfig(ctypes.c_int DeviceID, ctypes.c_ubyte ConfigByte)
    addfunc(lib, "NewClassicUSB_SetGPIOConfig", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_ubyte],
            argnames = ["DeviceID", "ConfigByte"] )
    #  SDK_RETURN_CODE NewClassicUSB_SetGPIOInOut(ctypes.c_int DeviceID, ctypes.c_ubyte OutputByte, ctypes.POINTER(ctypes.c_ubyte) InputBytePtr)
    addfunc(lib, "NewClassicUSB_SetGPIOInOut", restype = SDK_RETURN_CODE,
            argtypes = [ctypes.c_int, ctypes.c_ubyte, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["DeviceID", "OutputByte", "InputBytePtr"] )


