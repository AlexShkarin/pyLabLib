# pylint: disable=wrong-spelling-in-comment

from . import sc2_camexport_defs
from .sc2_camexport_defs import define_functions
from .PCO_err_defs import PCO_ERR, drPCO_ERR  # pylint: disable=unused-import
from .sc2_sdkstructures_defs import PCO_INTERFACE  # pylint: disable=unused-import
from . import sc2_defs_defs as sc2_defs  # pylint: disable=unused-import
from .sc2_defs_defs import CAPS1, CAPS3  # pylint: disable=unused-import

from ...core.utils import ctypes_wrap, py3
from ...core.devio.comm_backend import DeviceError
from ..utils import load_lib

import ctypes


class PCOSC2Error(DeviceError):
    """Generic PCO SC2 error"""
class PCOSC2LibError(PCOSC2Error):
    """Generic PCO SC2 library error"""
    def __init__(self, func, code, lib=None):
        self.func=func
        self.code=code%2**32
        err=0xFF00FFFF&self.code
        dev=0x00FF0000&self.code
        lay=0x0000F000&self.code
        serr="UNKNOWN"
        serr=drPCO_ERR.get(err,serr)
        serr=drPCO_ERR.get(err&0xFF000FFF,serr)
        self.name="{}|{}|{}".format(drPCO_ERR.get(dev,"UNKNOWN"),drPCO_ERR.get(lay,"UNKNOWN"),serr)
        try:
            if lib is not None:
                self.desc=py3.as_str(lib.GetErrorText(self.code))
        except PCOSC2LibError:
            pass
        self.msg="function '{}' raised error 0x{:08X}({}): {}".format(func,self.code,self.name,self.desc)
        PCOSC2Error.__init__(self,self.msg)
    def same_as(self, err):
        """Check if the error code agrees with the given error, taking only error bits into account"""
        return (self.code&0xFF000FFF)==(err&0xFF000FFF)
def errcheck(passing=None, lib=None):
    """
    Build an error checking function.

    Return a function which checks return codes of PCO SC2 library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    if passing is None:
        passing={0,None} # including void functions
    def errchecker(result, func, arguments):  # pylint: disable=unused-argument
        if result not in passing:
            raise PCOSC2LibError(func.__name__,result,lib=lib)
        return result
    return errchecker



def conv_arr(*args):
    return args[0][:]
def build_arr(ctype, n=None):
    if n is None:
        def build_func(arr):
            carr=(ctype*len(arr))
            for i in range(len(arr)):
                carr[i]=arr[i]
            return carr
    else:
        def build_func(arr):
            carr=(ctype*n)
            for i in range(min(n,len(arr))):
                carr[i]=arr[i]
            return carr
    return build_func



##### Structures #####

class CPCO_OpenStruct(sc2_camexport_defs.CPCO_OpenStruct):
    _tup_exc={"wSize","ZZwDummy"}
    _tup={"wOpenFlags":conv_arr,"dwOpenFlags":conv_arr,"wOpenPtr":conv_arr}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct

class CPCO_SC2_Hardware_DESC(sc2_camexport_defs.CPCO_SC2_Hardware_DESC):
    _tup_exc={"ZZwDummy"}
    _tup={"szName":ctypes.string_at}

class CPCO_SC2_Firmware_DESC(sc2_camexport_defs.CPCO_SC2_Firmware_DESC):
    _tup_exc={"ZZwDummy"}
    _tup={"szName":ctypes.string_at}

class CPCO_HW_Vers(sc2_camexport_defs.CPCO_HW_Vers):
    def tup(self):
        return [CPCO_SC2_Hardware_DESC.tup_struct(s) for s in self.Board[:self.BoardNum]] # pylint: disable=no-member
class CPCO_FW_Vers(sc2_camexport_defs.CPCO_FW_Vers):
    def tup(self):
        return [CPCO_SC2_Firmware_DESC.tup_struct(s) for s in self.Device[:self.DeviceNum]] # pylint: disable=no-member

class CPCO_CameraType(sc2_camexport_defs.CPCO_CameraType):
    _tup_exc={"wSize","ZZwDummy"}
    _tup={"strHardwareVersion":CPCO_HW_Vers.tup_struct,"strFirmwareVersion":CPCO_FW_Vers.tup_struct}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct


class CPCO_General(sc2_camexport_defs.CPCO_General):
    _tup_exc={"wSize","ZZwAlignDummy1","ZZwDummy"}
    _tup={"strCamType":CPCO_CameraType.tup_struct}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        struct.strCamType=CPCO_CameraType.prep_struct(struct.strCamType)
        return struct


class CPCO_Description(sc2_camexport_defs.CPCO_Description):
    _tup_exc={"wSize","ZZwDummycv","ZZdwDummypr","ZZdwDummy","wDummy1","wDummy2"}
    _tup={"dwPixelRateDESC":conv_arr,"wConvFactDESC":conv_arr,"sCoolingSetpoints":conv_arr,"dwExtSyncFrequency":conv_arr}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct

class CPCO_Description2(sc2_camexport_defs.CPCO_Description2):
    _tup_exc={"wSize","ZZwAlignDummy1","dwReserved","ZZdwDummy"}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct

class CPCO_Description_Intensified(sc2_camexport_defs.CPCO_Description_Intensified):
    _tup_exc={"wSize","ZZdwDummy"}
    _tup={"szIntensifierTypeDESC": ctypes.string_at}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct

NUM_SIGNAL_NAMES=4
class CPCO_Single_Signal_Desc(sc2_camexport_defs.CPCO_Single_Signal_Desc):
    _tup_exc={"wSize","ZZwAlignDummy1","dwDummy"}
    _tup={"strSignalName": lambda s: [ctypes.string_at(ctypes.addressof(s[i])) for i in range(NUM_SIGNAL_NAMES) if s[i][0]!=b'\x00']}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct
NUM_MAX_SIGNALS=20
class CPCO_Signal_Description(sc2_camexport_defs.CPCO_Signal_Description):
    _tup_exc={"wSize","dwDummy"}
    def tup(self):
        return [CPCO_Single_Signal_Desc.tup_struct(s) for s in self.strSingeSignalDesc[:self.wNumOfSignals]] # pylint: disable=no-member
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        for i in range(NUM_MAX_SIGNALS):
            struct.strSingeSignalDesc[i]=CPCO_Single_Signal_Desc.prep_struct(struct.strSingeSignalDesc[i])
        return struct


class CPCO_Sensor(sc2_camexport_defs.CPCO_Sensor):
    _tup_exc={"wSize","ZZwAlignDummy1","ZZdwDummy2","ZZwDummy","ZZdwDummy"}
    _tup={	"strDescription": CPCO_Description.tup_struct,
            "strDescription2": CPCO_Description2.tup_struct,
            "strDescriptionIntensified": CPCO_Description_Intensified.tup_struct,
            "strSignalDesc": CPCO_Signal_Description.tup_struct,}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        struct.strDescription=CPCO_Description.prep_struct(struct.strDescription)
        struct.strDescription2=CPCO_Description2.prep_struct(struct.strDescription2)
        struct.strDescriptionIntensified=CPCO_Description_Intensified.prep_struct(struct.strDescriptionIntensified)
        struct.strSignalDesc=CPCO_Signal_Description.prep_struct(struct.strSignalDesc)
        return struct

class CPCO_APIBuffer(sc2_camexport_defs.CPCO_APIBuffer):
    _tup_exc={"wSize","ZZwAlignDummy1","ZZdwDummyFill","ZZwDummy"}
    _tup={"dwParameter":conv_arr,"dwSignalFunctionality":conv_arr}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct

class CPCO_APIManagement(sc2_camexport_defs.CPCO_APIManagement):
    _tup_exc={"wSize","ZZstrDummyBuf","ZZwDummy"}
    _tup={"pSC2IFFunc":conv_arr,"dwIF_param":conv_arr,"wImageTransferParam":conv_arr,"strPCOBuf":lambda *args: [CPCO_APIBuffer.tup_struct(s) for s in args[0]]}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct


class CPCO_ImageTiming(sc2_camexport_defs.CPCO_ImageTiming):
    _tup_exc={"wSize","wDummy","ZZdwDummy"}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct

class CPCO_Signal(sc2_camexport_defs.CPCO_Signal):
    _tup_exc={"wSize","ZZwReserved","ZZdwReserved"}
    _tup={"dwParameter":conv_arr,"dwSignalFunctionality":conv_arr}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct

class CPCO_Timing(sc2_camexport_defs.CPCO_Timing):
    _tup_exc={"wSize","ZZdwDummy1","ZZdwDummy2","ZZdwDummy3","ZZwDummy3","ZZwDummy"}
    _tup={"dwDelayTable":conv_arr,"dwExposureTable":conv_arr,"strSignal":lambda *args: [CPCO_Signal.tup_struct(s) for s in args[0]]}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        for i in range(NUM_MAX_SIGNALS):
            struct.strSignal[i]=CPCO_Signal.prep_struct(struct.strSignal[i])
        return struct

class CPCO_Storage(sc2_camexport_defs.CPCO_Storage):
    _tup_exc={"wSize","ZZwAlignDummy1","ZZwAlignDummy4","ZZdwDummyrs","ZZwDummy"}
    _tup={"dwRamSegSize":conv_arr}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct

class CPCO_Recording(sc2_camexport_defs.CPCO_Recording):
    _tup_exc={"wSize","ZZwDummy1","ZZwDummy","dwAcquModeExReserved"}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct

class CPCO_Segment(sc2_camexport_defs.CPCO_Segment):
    _tup_exc={"wSize","ZZwAlignDummy1","ZZwDummy"}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct

class CPCO_Image_ColorSet(sc2_camexport_defs.CPCO_Image_ColorSet):
    _tup_exc={"wSize","ZZwDummy"}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct

PCO_RAMSEGCNT=4
class CPCO_Image(sc2_camexport_defs.CPCO_Image):
    _tup_exc={"wSize","ZZwAlignDummy1","ZZstrDummySeg","ZZwDummy"}
    _tup={"strSegment":lambda *args: [CPCO_Segment.tup_struct(s) for s in args[0]],"strColorSet":CPCO_Image_ColorSet.tup_struct}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        for i in range(PCO_RAMSEGCNT):
            struct.strSegment[i]=CPCO_Segment.prep_struct(struct.strSegment[i])
        for i in range(14):
            struct.ZZstrDummySeg[i]=CPCO_Segment.prep_struct(struct.ZZstrDummySeg[i])
        struct.strColorSet=CPCO_Image_ColorSet.prep_struct(struct.strColorSet)
        return struct

class CPCO_Buflist(sc2_camexport_defs.CPCO_Buflist):
    _tup_exc={"ZZwAlignDummy"}

class CPCO_METADATA_STRUCT(sc2_camexport_defs.CPCO_METADATA_STRUCT):
    _tup_exc={"wSize"}
    _tup={"bIMAGE_COUNTER_BCD":conv_arr,"bIMAGE_TIME_US_BCD":conv_arr}
    def prep(self, struct):
        struct.wSize=ctypes.sizeof(struct)
        return struct

DWORD=sc2_camexport_defs.DWORD
HANDLE=sc2_camexport_defs.HANDLE
BOOL=ctypes.c_int

MAX_SCHEDULED_BUFFERS=32


class PCOSC2Lib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return

        camware_path=load_lib.get_program_files_folder("Digital Camera Toolbox/Camware4")
        sdk_path=load_lib.get_program_files_folder("PCO Digital Camera Toolbox/pco.sdk/bin") # TODO: check folder; bin/bin64; may also be in 32-bit program files folder
        error_message="The library is supplied with pco.camware or pco.sdk software\n"+load_lib.par_error_message.format("pco_sc2")
        self.lib=load_lib.load_lib("SC2_Cam.dll",locations=("parameter/pco_sc2",camware_path,sdk_path,"global"),error_message=error_message,call_conv="stdcall")
        lib=self.lib
        define_functions(lib)

        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(lib=self),default_rvals="pointer")
        max_strlen=512
        strprep=ctypes_wrap.strprep(max_strlen)

        #  None PCO_GetErrorText(DWORD dwerr, ctypes.c_char_p pbuf, DWORD dwlen)
        self.PCO_GetErrorText=wrapper(lib.PCO_GetErrorText, args=["dwerr"], rvals=["pbuf"],
            argprep={"pbuf":strprep,"dwlen":max_strlen}, byref=[])
        #  None PCO_GetErrorTextSDK(DWORD dwError, ctypes.c_char_p pszErrorString, DWORD dwErrorStringLength)
        self.PCO_GetErrorTextSDK=wrapper(lib.PCO_GetErrorTextSDK, args=["dwError"], rvals=["pszErrorString"],
            argprep={"pszErrorString":strprep,"dwErrorStringLength":max_strlen}, byref=[])
        self.GetErrorText=self.PCO_GetErrorTextSDK or self.PCO_GetErrorText

        #  ctypes.c_int PCO_OpenCamera(ctypes.POINTER(HANDLE) ph, WORD wCamNum)
        self.PCO_OpenCamera=wrapper(lib.PCO_OpenCamera, args=[]) # parameter is ignored
        #  ctypes.c_int PCO_OpenCameraEx(ctypes.POINTER(HANDLE) ph, ctypes.POINTER(PCO_OpenStruct) strOpenStruct)
        def prep_open_struct(wInterfaceType, wCameraNumber):
            return CPCO_OpenStruct.prep_struct_args(wInterfaceType=wInterfaceType,wCameraNumber=wCameraNumber)
        self.PCO_OpenCameraEx=wrapper(lib.PCO_OpenCameraEx, args=["wInterfaceType","wCameraNumber"],
            argprep={"strOpenStruct":prep_open_struct}, rconv={"strOpenStruct":CPCO_OpenStruct.tup_struct})
        #  ctypes.c_int PCO_CloseCamera(HANDLE ph)
        self.PCO_CloseCamera=wrapper(lib.PCO_CloseCamera)
        #  ctypes.c_int PCO_ResetSettingsToDefault(HANDLE ph)
        self.PCO_ResetSettingsToDefault=wrapper(lib.PCO_ResetSettingsToDefault)
        #  ctypes.c_int PCO_RebootCamera(HANDLE ph)
        self.PCO_RebootCamera=wrapper(lib.PCO_RebootCamera)
        #  ctypes.c_int PCO_ResetLib()
        self.PCO_ResetLib=wrapper(lib.PCO_ResetLib)
        #  ctypes.c_int PCO_CheckDeviceAvailability(HANDLE ph, WORD wNum)
        self.PCO_CheckDeviceAvailability=wrapper(lib.PCO_CheckDeviceAvailability)

        #  ctypes.c_int PCO_GetCameraDescription(HANDLE ph, ctypes.POINTER(PCO_Description) strDescription)
        self.PCO_GetCameraDescription=wrapper(lib.PCO_GetCameraDescription,
            argprep={"strDescription":CPCO_Description.prep_struct}, rconv={"strDescription":CPCO_Description.tup_struct})
        #  ctypes.c_int PCO_GetGeneral(HANDLE ph, ctypes.POINTER(PCO_General) strGeneral)
        self.PCO_GetGeneral=wrapper(lib.PCO_GetGeneral,
            argprep={"strGeneral":CPCO_General.prep_struct}, rconv={"strGeneral":CPCO_General.tup_struct})
        #  ctypes.c_int PCO_GetCameraName(HANDLE ph, ctypes.c_char_p szCameraName, WORD wSZCameraNameLen)
        self.PCO_GetCameraName=wrapper(lib.PCO_GetCameraName, args=["ph"], rvals=["szCameraName"],
            argprep={"szCameraName":strprep,"wSZCameraNameLen":max_strlen}, byref=[])
        #  ctypes.c_int PCO_GetCameraType(HANDLE ph, ctypes.POINTER(PCO_CameraType) strCamType)
        self.PCO_GetCameraType=wrapper(lib.PCO_GetCameraType,
            argprep={"strCamType":CPCO_CameraType.prep_struct}, rconv={"strCamType":CPCO_CameraType.tup_struct})
        #  ctypes.c_int PCO_GetCameraHealthStatus(HANDLE ph, ctypes.POINTER(DWORD) dwWarn, ctypes.POINTER(DWORD) dwErr, ctypes.POINTER(DWORD) dwStatus)
        self.PCO_GetCameraHealthStatus=wrapper(lib.PCO_GetCameraHealthStatus)
        #  ctypes.c_int PCO_GetTemperature(HANDLE ph, ctypes.POINTER(SHORT) sCCDTemp, ctypes.POINTER(SHORT) sCamTemp, ctypes.POINTER(SHORT) sPowTemp)
        self.PCO_GetTemperature=wrapper(lib.PCO_GetTemperature)
        #  ctypes.c_int PCO_GetInfoString(HANDLE ph, DWORD dwinfotype, ctypes.c_char_p buf_in, WORD size_in)
        self.PCO_GetInfoString=wrapper(lib.PCO_GetInfoString, args=["ph","dwinfotype"], rvals=["buf_in"],
            argprep={"buf_in":strprep,"size_in":max_strlen}, byref=[])
        #  ctypes.c_int PCO_GetFirmwareInfo(HANDLE ph, WORD wDeviceBlock, ctypes.POINTER(PCO_FW_Vers) pstrFirmWareVersion)
        self.PCO_GetFirmwareInfo=wrapper(lib.PCO_GetFirmwareInfo,
            argprep={"pstrFirmWareVersion":CPCO_FW_Vers.prep_struct}, rconv={"pstrFirmWareVersion":CPCO_FW_Vers.tup_struct})
        #  ctypes.c_int PCO_GetAPIManagement(HANDLE ph, ctypes.POINTER(WORD) wFlags, ctypes.POINTER(PCO_APIManagement) pstrApi)
        self.PCO_GetAPIManagement=wrapper(lib.PCO_GetAPIManagement,
            argprep={"pstrApi":CPCO_APIManagement.prep_struct}, rconv={"pstrApi":CPCO_APIManagement.tup_struct})

        #  ctypes.c_int PCO_ArmCamera(HANDLE ph)
        self.PCO_ArmCamera=wrapper(lib.PCO_ArmCamera)
        #  ctypes.c_int PCO_SetImageParameters(HANDLE ph, WORD wxres, WORD wyres, DWORD dwflags, ctypes.c_void_p param, ctypes.c_int ilen)
        self.PCO_SetImageParameters=wrapper(lib.PCO_SetImageParameters, args=["ph","wxres","wyres","dwflags"])
        #  ctypes.c_int PCO_SetTimeouts(HANDLE ph, ctypes.c_void_p buf_in, ctypes.c_uint size_in)
        self.PCO_SetTimeouts=wrapper(lib.PCO_SetTimeouts, args=["ph","buf_in"],
            argprep={"size_in":3*ctypes.sizeof(ctypes.c_uint)})
        # self.PCO_SetTimeouts=wrapper(lib.PCO_SetTimeouts, args=["ph","setup_type","setup","setup_len"],
        #     argprep={"size_in":3*ctypes.sizeof(ctypes.c_uint), "buf_in": lambda setup_type,setup,setup_len: [setup_type,setup,setup_len]})
        #  ctypes.c_int PCO_GetCameraSetup(HANDLE ph, ctypes.POINTER(WORD) wType, ctypes.POINTER(DWORD) dwSetup, ctypes.POINTER(WORD) wLen)
        self.PCO_GetCameraSetup=wrapper(lib.PCO_GetCameraSetup,
            argprep={"dwSetup":(DWORD*4), "wLen":4}, rconv={"dwSetup": lambda v:v[:4]}, byref=["wType","wLen"])
        #  ctypes.c_int PCO_SetCameraSetup(HANDLE ph, WORD wType, ctypes.POINTER(DWORD) dwSetup, WORD wLen)
        self.PCO_SetCameraSetup=wrapper(lib.PCO_SetCameraSetup, args=["ph","dwSetup"],
            argprep={"dwSetup": lambda dwSetup: build_arr(DWORD,4)(dwSetup), "wLen":4}, rconv={"dwSetup": lambda v:v[:4]}, byref=["wType","wLen"])  # pylint: disable=unnecessary-lambda
        #  ctypes.c_int PCO_GetSensorStruct(HANDLE ph, ctypes.POINTER(PCO_Sensor) strSensor)
        self.PCO_GetSensorStruct=wrapper(lib.PCO_GetSensorStruct,
            argprep={"strSensor":CPCO_Sensor.prep_struct}, rconv={"strSensor":CPCO_Sensor.tup_struct})
        #  ctypes.c_int PCO_SetSensorStruct(HANDLE ph, ctypes.POINTER(PCO_Sensor) strSensor)
        self.PCO_SetSensorStruct=wrapper(lib.PCO_SetSensorStruct, args="all",
            rconv={"strSensor":CPCO_Sensor.tup_struct})
        #  ctypes.c_int PCO_GetSensorSignalStatus(HANDLE hCam, ctypes.POINTER(DWORD) dwStatus, ctypes.POINTER(DWORD) dwImageCount, ctypes.POINTER(DWORD) dwReserved1, ctypes.POINTER(DWORD) dwReserved2)
        self.PCO_GetSensorSignalStatus=wrapper(lib.PCO_GetSensorSignalStatus)
        #  ctypes.c_int PCO_GetDeviceStatus(HANDLE ph, WORD wNum, ctypes.POINTER(DWORD) dwStatus, WORD wStatusLen)
        self.PCO_GetDeviceStatus=wrapper(lib.PCO_GetDeviceStatus, args=["ph","wNum"],
            argprep={"dwStatus":(DWORD*2), "wStatusLen":2}, rconv={"dwStatus": lambda v:v[:2]}, byref=[])


        #  ctypes.c_int PCO_GetPowerSaveMode(HANDLE ph, ctypes.POINTER(WORD) wMode, ctypes.POINTER(WORD) wDelayMinutes)
        self.PCO_GetPowerSaveMode=wrapper(lib.PCO_GetPowerSaveMode)
        #  ctypes.c_int PCO_SetPowerSaveMode(HANDLE ph, WORD wMode, WORD wDelayMinutes)
        self.PCO_SetPowerSaveMode=wrapper(lib.PCO_SetPowerSaveMode)
        #  ctypes.c_int PCO_GetBatteryStatus(HANDLE ph, ctypes.POINTER(WORD) wBatteryType, ctypes.POINTER(WORD) wBatteryLevel, ctypes.POINTER(WORD) wPowerStatus, ctypes.POINTER(WORD) wReserved, WORD wNumReserved)
        self.PCO_GetBatteryStatus=wrapper(lib.PCO_GetBatteryStatus, args=["ph"], rvals=["wBatteryType","wBatteryLevel","wPowerStatus"])
        #  ctypes.c_int PCO_GetFanControlParameters(HANDLE hCam, ctypes.POINTER(WORD) wMode, ctypes.POINTER(WORD) wValue, ctypes.POINTER(WORD) wReserved, WORD wNumReserved)
        self.PCO_GetFanControlParameters=wrapper(lib.PCO_GetFanControlParameters, args=["ph"], rvals=["wMode","wValue"])
        #  ctypes.c_int PCO_SetFanControlParameters(HANDLE hCam, WORD wMode, WORD wValue, WORD wReserved)
        self.PCO_SetFanControlParameters=wrapper(lib.PCO_SetFanControlParameters, args=["ph","wMode","wValue"])
        #  ctypes.c_int PCO_GetSizes(HANDLE ph, ctypes.POINTER(WORD) wXResAct, ctypes.POINTER(WORD) wYResAct, ctypes.POINTER(WORD) wXResMax, ctypes.POINTER(WORD) wYResMax)
        self.PCO_GetSizes=wrapper(lib.PCO_GetSizes)
        #  ctypes.c_int PCO_GetSensorFormat(HANDLE ph, ctypes.POINTER(WORD) wSensor)
        self.PCO_GetSensorFormat=wrapper(lib.PCO_GetSensorFormat)
        #  ctypes.c_int PCO_SetSensorFormat(HANDLE ph, WORD wSensor)
        self.PCO_SetSensorFormat=wrapper(lib.PCO_SetSensorFormat)
        #  ctypes.c_int PCO_GetROI(HANDLE ph, ctypes.POINTER(WORD) wRoiX0, ctypes.POINTER(WORD) wRoiY0, ctypes.POINTER(WORD) wRoiX1, ctypes.POINTER(WORD) wRoiY1)
        self.PCO_GetROI=wrapper(lib.PCO_GetROI)
        #  ctypes.c_int PCO_SetROI(HANDLE ph, WORD wRoiX0, WORD wRoiY0, WORD wRoiX1, WORD wRoiY1)
        self.PCO_SetROI=wrapper(lib.PCO_SetROI)
        #  ctypes.c_int PCO_GetBinning(HANDLE ph, ctypes.POINTER(WORD) wBinHorz, ctypes.POINTER(WORD) wBinVert)
        self.PCO_GetBinning=wrapper(lib.PCO_GetBinning)
        #  ctypes.c_int PCO_SetBinning(HANDLE ph, WORD wBinHorz, WORD wBinVert)
        self.PCO_SetBinning=wrapper(lib.PCO_SetBinning)
        #  ctypes.c_int PCO_GetPixelRate(HANDLE ph, ctypes.POINTER(DWORD) dwPixelRate)
        self.PCO_GetPixelRate=wrapper(lib.PCO_GetPixelRate)
        #  ctypes.c_int PCO_SetPixelRate(HANDLE ph, DWORD dwPixelRate)
        self.PCO_SetPixelRate=wrapper(lib.PCO_SetPixelRate)
        #  ctypes.c_int PCO_GetConversionFactor(HANDLE ph, ctypes.POINTER(WORD) wConvFact)
        self.PCO_GetConversionFactor=wrapper(lib.PCO_GetConversionFactor)
        #  ctypes.c_int PCO_SetConversionFactor(HANDLE ph, WORD wConvFact)
        self.PCO_SetConversionFactor=wrapper(lib.PCO_SetConversionFactor)
        #  ctypes.c_int PCO_GetDoubleImageMode(HANDLE ph, ctypes.POINTER(WORD) wDoubleImage)
        self.PCO_GetDoubleImageMode=wrapper(lib.PCO_GetDoubleImageMode)
        #  ctypes.c_int PCO_SetDoubleImageMode(HANDLE ph, WORD wDoubleImage)
        self.PCO_SetDoubleImageMode=wrapper(lib.PCO_SetDoubleImageMode)
        #  ctypes.c_int PCO_GetADCOperation(HANDLE ph, ctypes.POINTER(WORD) wADCOperation)
        self.PCO_GetADCOperation=wrapper(lib.PCO_GetADCOperation)
        #  ctypes.c_int PCO_SetADCOperation(HANDLE ph, WORD wADCOperation)
        self.PCO_SetADCOperation=wrapper(lib.PCO_SetADCOperation)
        #  ctypes.c_int PCO_GetIRSensitivity(HANDLE ph, ctypes.POINTER(WORD) wIR)
        self.PCO_GetIRSensitivity=wrapper(lib.PCO_GetIRSensitivity)
        #  ctypes.c_int PCO_SetIRSensitivity(HANDLE ph, WORD wIR)
        self.PCO_SetIRSensitivity=wrapper(lib.PCO_SetIRSensitivity)
        #  ctypes.c_int PCO_GetCoolingSetpoints(HANDLE ph, WORD wBlockID, ctypes.POINTER(WORD) wNumSetPoints, ctypes.POINTER(SHORT) sCoolSetpoints)
        self.PCO_GetCoolingSetpoints=wrapper(lib.PCO_GetCoolingSetpoints, args=["ph","wBlockID"],
            argprep={"sCoolSetpoints":(DWORD*10), "wNumSetPoints":10}, rconv={"sCoolSetpoints": lambda v:v[:10]}, byref=["wNumSetPoints"])
        #  ctypes.c_int PCO_GetCoolingSetpointTemperature(HANDLE ph, ctypes.POINTER(SHORT) sCoolSet)
        self.PCO_GetCoolingSetpointTemperature=wrapper(lib.PCO_GetCoolingSetpointTemperature)
        #  ctypes.c_int PCO_SetCoolingSetpointTemperature(HANDLE ph, SHORT sCoolSet)
        self.PCO_SetCoolingSetpointTemperature=wrapper(lib.PCO_SetCoolingSetpointTemperature)
        #  ctypes.c_int PCO_GetOffsetMode(HANDLE ph, ctypes.POINTER(WORD) wOffsetRegulation)
        self.PCO_GetOffsetMode=wrapper(lib.PCO_GetOffsetMode)
        #  ctypes.c_int PCO_SetOffsetMode(HANDLE ph, WORD wOffsetRegulation)
        self.PCO_SetOffsetMode=wrapper(lib.PCO_SetOffsetMode)
        #  ctypes.c_int PCO_GetNoiseFilterMode(HANDLE ph, ctypes.POINTER(WORD) wNoiseFilterMode)
        self.PCO_GetNoiseFilterMode=wrapper(lib.PCO_GetNoiseFilterMode)
        #  ctypes.c_int PCO_SetNoiseFilterMode(HANDLE ph, WORD wNoiseFilterMode)
        self.PCO_SetNoiseFilterMode=wrapper(lib.PCO_SetNoiseFilterMode)
        #  ctypes.c_int PCO_GetCameraBusyStatus(HANDLE ph, ctypes.POINTER(WORD) wCameraBusyState)
        self.PCO_GetCameraBusyStatus=wrapper(lib.PCO_GetCameraBusyStatus)
        #  ctypes.c_int PCO_GetPowerDownMode(HANDLE ph, ctypes.POINTER(WORD) wPowerDownMode)
        self.PCO_GetPowerDownMode=wrapper(lib.PCO_GetPowerDownMode)
        #  ctypes.c_int PCO_SetPowerDownMode(HANDLE ph, WORD wPowerDownMode)
        self.PCO_SetPowerDownMode=wrapper(lib.PCO_SetPowerDownMode)
        #  ctypes.c_int PCO_GetUserPowerDownTime(HANDLE ph, ctypes.POINTER(DWORD) dwPowerDownTime)
        self.PCO_GetUserPowerDownTime=wrapper(lib.PCO_GetUserPowerDownTime)
        #  ctypes.c_int PCO_SetUserPowerDownTime(HANDLE ph, DWORD dwPowerDownTime)
        self.PCO_SetUserPowerDownTime=wrapper(lib.PCO_SetUserPowerDownTime)
        #  ctypes.c_int PCO_GetCDIMode(HANDLE ph, ctypes.POINTER(WORD) wCDIMode)
        self.PCO_GetCDIMode=wrapper(lib.PCO_GetCDIMode)
        #  ctypes.c_int PCO_SetCDIMode(HANDLE ph, WORD wCDIMode)
        self.PCO_SetCDIMode=wrapper(lib.PCO_SetCDIMode)
        #  ctypes.c_int PCO_ControlCommandCall(HANDLE ph, ctypes.c_void_p buf_in, ctypes.c_uint size_in, ctypes.c_void_p buf_out, ctypes.c_uint size_out)
        self.PCO_ControlCommandCall=wrapper(lib.PCO_ControlCommandCall, args=["ph","buf_in","size_out"], rvals=["buf_out"],
            argprep={"size_in":lambda buf_in:len(buf_in), "buf_out": lambda size_out: ctypes.create_string_buffer(size_out)}, byref=[])  # pylint: disable=unnecessary-lambda

        
        #  ctypes.c_int PCO_GetTimingStruct(HANDLE ph, ctypes.POINTER(PCO_Timing) strTiming)
        self.PCO_GetTimingStruct=wrapper(lib.PCO_GetTimingStruct,
            argprep={"strTiming":CPCO_Timing.prep_struct}, rconv={"strTiming":CPCO_Timing.tup_struct})
        #  ctypes.c_int PCO_SetTimingStruct(HANDLE ph, ctypes.POINTER(PCO_Timing) strTiming)
        self.PCO_SetTimingStruct=wrapper(lib.PCO_SetTimingStruct, args="all",
            rconv={"strTiming":CPCO_Timing.tup_struct})
        #  ctypes.c_int PCO_GetCOCRuntime(HANDLE ph, ctypes.POINTER(DWORD) dwTime_s, ctypes.POINTER(DWORD) dwTime_ns)
        self.PCO_GetCOCRuntime=wrapper(lib.PCO_GetCOCRuntime)
        #  ctypes.c_int PCO_GetDelayExposureTime(HANDLE ph, ctypes.POINTER(DWORD) dwDelay, ctypes.POINTER(DWORD) dwExposure, ctypes.POINTER(WORD) wTimeBaseDelay, ctypes.POINTER(WORD) wTimeBaseExposure)
        self.PCO_GetDelayExposureTime=wrapper(lib.PCO_GetDelayExposureTime)
        #  ctypes.c_int PCO_SetDelayExposureTime(HANDLE ph, DWORD dwDelay, DWORD dwExposure, WORD wTimeBaseDelay, WORD wTimeBaseExposure)
        self.PCO_SetDelayExposureTime=wrapper(lib.PCO_SetDelayExposureTime)
        #  ctypes.c_int PCO_GetDelayExposureTimeTable(HANDLE ph, ctypes.POINTER(DWORD) dwDelay, ctypes.POINTER(DWORD) dwExposure, ctypes.POINTER(WORD) wTimeBaseDelay, ctypes.POINTER(WORD) wTimeBaseExposure, WORD wCount)
        countprep=lambda wCount: (DWORD*wCount)()
        countconv=lambda v,_,kwargs: v[:kwargs["wCount"]]
        self.PCO_GetDelayExposureTimeTable=wrapper(lib.PCO_GetDelayExposureTimeTable,
            argprep={"dwDelay": countprep, "dwExposure":countprep}, rconv={"dwDelay": countconv, "dwExposure":countconv}, byref=["wTimeBaseDelay","wTimeBaseExposure"])
        #  ctypes.c_int PCO_SetDelayExposureTimeTable(HANDLE ph, ctypes.POINTER(DWORD) dwDelay, ctypes.POINTER(DWORD) dwExposure, WORD wTimeBaseDelay, WORD wTimeBaseExposure, WORD wCount)
        self.PCO_SetDelayExposureTimeTable=wrapper(lib.PCO_SetDelayExposureTimeTable, args="all",
            argprep={"dwDelay":lambda dwDelay: build_arr(DWORD)(dwDelay), "dwExposure":lambda dwExposure: build_arr(DWORD)(dwExposure),  # pylint: disable=unnecessary-lambda
            "wCount":lambda dwDelay,dwExposure: max(len(dwDelay),len(dwExposure))})
        #  ctypes.c_int PCO_GetFrameRate(HANDLE ph, ctypes.POINTER(WORD) wFrameRateStatus, ctypes.POINTER(DWORD) dwFrameRate, ctypes.POINTER(DWORD) dwFrameRateExposure)
        self.PCO_GetFrameRate=wrapper(lib.PCO_GetFrameRate)
        #  ctypes.c_int PCO_SetFrameRate(HANDLE ph, ctypes.POINTER(WORD) wFrameRateStatus, WORD wFrameRateMode, ctypes.POINTER(DWORD) dwFrameRate, ctypes.POINTER(DWORD) dwFrameRateExposure)
        self.PCO_SetFrameRate=wrapper(lib.PCO_SetFrameRate, args=["ph","wFrameRateMode","dwFrameRate"])
        #  ctypes.c_int PCO_GetFPSExposureMode(HANDLE ph, ctypes.POINTER(WORD) wFPSExposureMode, ctypes.POINTER(DWORD) dwFPSExposureTime)
        self.PCO_GetFPSExposureMode=wrapper(lib.PCO_GetFPSExposureMode)
        #  ctypes.c_int PCO_SetFPSExposureMode(HANDLE ph, WORD wFPSExposureMode, ctypes.POINTER(DWORD) dwFPSExposureTime)
        self.PCO_SetFPSExposureMode=wrapper(lib.PCO_SetFPSExposureMode)
        #  ctypes.c_int PCO_GetTriggerMode(HANDLE ph, ctypes.POINTER(WORD) wTriggerMode)
        self.PCO_GetTriggerMode=wrapper(lib.PCO_GetTriggerMode)
        #  ctypes.c_int PCO_SetTriggerMode(HANDLE ph, WORD wTriggerMode)
        self.PCO_SetTriggerMode=wrapper(lib.PCO_SetTriggerMode)
        #  ctypes.c_int PCO_ForceTrigger(HANDLE ph, ctypes.POINTER(WORD) wTriggered)
        self.PCO_ForceTrigger=wrapper(lib.PCO_ForceTrigger)
        #  ctypes.c_int PCO_GetModulationMode(HANDLE ph, ctypes.POINTER(WORD) wModulationMode, ctypes.POINTER(DWORD) dwPeriodicalTime, ctypes.POINTER(WORD) wTimebasePeriodical, ctypes.POINTER(DWORD) dwNumberOfExposures, ctypes.POINTER(LONG) lMonitorOffset)
        self.PCO_GetModulationMode=wrapper(lib.PCO_GetModulationMode)
        #  ctypes.c_int PCO_SetModulationMode(HANDLE ph, WORD wModulationMode, DWORD dwPeriodicalTime, WORD wTimebasePeriodical, DWORD dwNumberOfExposures, LONG lMonitorOffset)
        self.PCO_SetModulationMode=wrapper(lib.PCO_SetModulationMode)
        #  ctypes.c_int PCO_GetHWIOSignalCount(HANDLE ph, ctypes.POINTER(WORD) wNumSignals)
        self.PCO_GetHWIOSignalCount=wrapper(lib.PCO_GetHWIOSignalCount)
        #  ctypes.c_int PCO_GetHWIOSignalDescriptor(HANDLE ph, WORD wSignalNum, ctypes.POINTER(PCO_Single_Signal_Desc) pstrSignal)
        self.PCO_GetHWIOSignalDescriptor=wrapper(lib.PCO_GetHWIOSignalDescriptor,
            argprep={"pstrSignal":CPCO_Single_Signal_Desc.prep_struct}, rconv={"pstrSignal":CPCO_Single_Signal_Desc.tup_struct})
        #  ctypes.c_int PCO_GetHWIOSignal(HANDLE ph, WORD wSignalNum, ctypes.POINTER(PCO_Signal) pstrSignal)
        self.PCO_GetHWIOSignal=wrapper(lib.PCO_GetHWIOSignal,
            argprep={"pstrSignal":CPCO_Signal.prep_struct}, rconv={"pstrSignal":CPCO_Signal.tup_struct})
        #  ctypes.c_int PCO_SetHWIOSignal(HANDLE ph, WORD wSignalNum, ctypes.POINTER(PCO_Signal) pstrSignal)
        self.PCO_SetHWIOSignal=wrapper(lib.PCO_SetHWIOSignal, args="all",
            rconv={"pstrSignal":CPCO_Signal.tup_struct})
        #  ctypes.c_int PCO_GetImageTiming(HANDLE ph, ctypes.POINTER(PCO_ImageTiming) pstrImageTiming)
        self.PCO_GetImageTiming=wrapper(lib.PCO_GetImageTiming,
            argprep={"pstrImageTiming":CPCO_ImageTiming.prep_struct}, rconv={"pstrImageTiming":CPCO_ImageTiming.tup_struct})
        #  ctypes.c_int PCO_GetCameraSynchMode(HANDLE ph, ctypes.POINTER(WORD) wCameraSynchMode)
        self.PCO_GetCameraSynchMode=wrapper(lib.PCO_GetCameraSynchMode)
        #  ctypes.c_int PCO_SetCameraSynchMode(HANDLE ph, WORD wCameraSynchMode)
        self.PCO_SetCameraSynchMode=wrapper(lib.PCO_SetCameraSynchMode)
        #  ctypes.c_int PCO_GetFastTimingMode(HANDLE hCam, ctypes.POINTER(WORD) wFastTimingMode)
        self.PCO_GetFastTimingMode=wrapper(lib.PCO_GetFastTimingMode)
        #  ctypes.c_int PCO_SetFastTimingMode(HANDLE hCam, WORD wFastTimingMode)
        self.PCO_SetFastTimingMode=wrapper(lib.PCO_SetFastTimingMode)
        #  ctypes.c_int PCO_GetExpTrigSignalStatus(HANDLE ph, ctypes.POINTER(WORD) wExpTrgSignal)
        self.PCO_GetExpTrigSignalStatus=wrapper(lib.PCO_GetExpTrigSignalStatus)

        #  ctypes.c_int PCO_GetRecordingStruct(HANDLE ph, ctypes.POINTER(PCO_Recording) strRecording)
        self.PCO_GetRecordingStruct=wrapper(lib.PCO_GetRecordingStruct,
            argprep={"strRecording":CPCO_Recording.prep_struct}, rconv={"strRecording":CPCO_Recording.tup_struct})
        #  ctypes.c_int PCO_SetRecordingStruct(HANDLE ph, ctypes.POINTER(PCO_Recording) strRecording)
        self.PCO_SetRecordingStruct=wrapper(lib.PCO_SetRecordingStruct, args="all",
            rconv={"strRecording":CPCO_Recording.tup_struct})
        #  ctypes.c_int PCO_GetRecordingState(HANDLE ph, ctypes.POINTER(WORD) wRecState)
        self.PCO_GetRecordingState=wrapper(lib.PCO_GetRecordingState)
        #  ctypes.c_int PCO_SetRecordingState(HANDLE ph, WORD wRecState)
        self.PCO_SetRecordingState=wrapper(lib.PCO_SetRecordingState)
        #  ctypes.c_int PCO_GetStorageMode(HANDLE ph, ctypes.POINTER(WORD) wStorageMode)
        self.PCO_GetStorageMode=wrapper(lib.PCO_GetStorageMode)
        #  ctypes.c_int PCO_SetStorageMode(HANDLE ph, WORD wStorageMode)
        self.PCO_SetStorageMode=wrapper(lib.PCO_SetStorageMode)
        #  ctypes.c_int PCO_GetRecorderSubmode(HANDLE ph, ctypes.POINTER(WORD) wRecSubmode)
        self.PCO_GetRecorderSubmode=wrapper(lib.PCO_GetRecorderSubmode)
        #  ctypes.c_int PCO_SetRecorderSubmode(HANDLE ph, WORD wRecSubmode)
        self.PCO_SetRecorderSubmode=wrapper(lib.PCO_SetRecorderSubmode)
        #  ctypes.c_int PCO_GetAcquireMode(HANDLE ph, ctypes.POINTER(WORD) wAcquMode)
        self.PCO_GetAcquireMode=wrapper(lib.PCO_GetAcquireMode)
        #  ctypes.c_int PCO_SetAcquireMode(HANDLE ph, WORD wAcquMode)
        self.PCO_SetAcquireMode=wrapper(lib.PCO_SetAcquireMode)
        #  ctypes.c_int PCO_GetAcquireModeEx(HANDLE ph, ctypes.POINTER(WORD) wAcquMode, ctypes.POINTER(DWORD) dwNumberImages, ctypes.POINTER(DWORD) dwReserved)
        self.PCO_GetAcquireModeEx=wrapper(lib.PCO_GetAcquireModeEx)
        #  ctypes.c_int PCO_SetAcquireModeEx(HANDLE ph, WORD wAcquMode, DWORD dwNumberImages, ctypes.POINTER(DWORD) dwReserved)
        self.PCO_SetAcquireModeEx=wrapper(lib.PCO_SetAcquireModeEx)
        #  ctypes.c_int PCO_GetAcqEnblSignalStatus(HANDLE ph, ctypes.POINTER(WORD) wAcquEnableState)
        self.PCO_GetAcqEnblSignalStatus=wrapper(lib.PCO_GetAcqEnblSignalStatus)
        #  ctypes.c_int PCO_GetMetaDataMode(HANDLE ph, ctypes.POINTER(WORD) wMetaDataMode, ctypes.POINTER(WORD) wMetaDataSize, ctypes.POINTER(WORD) wMetaDataVersion)
        self.PCO_GetMetaDataMode=wrapper(lib.PCO_GetMetaDataMode)
        #  ctypes.c_int PCO_SetMetaDataMode(HANDLE ph, WORD wMetaDataMode, ctypes.POINTER(WORD) wMetaDataSize, ctypes.POINTER(WORD) wMetaDataVersion)
        self.PCO_SetMetaDataMode=wrapper(lib.PCO_SetMetaDataMode)
        #  ctypes.c_int PCO_GetRecordStopEvent(HANDLE ph, ctypes.POINTER(WORD) wRecordStopEventMode, ctypes.POINTER(DWORD) dwRecordStopDelayImages)
        self.PCO_GetRecordStopEvent=wrapper(lib.PCO_GetRecordStopEvent)
        #  ctypes.c_int PCO_SetRecordStopEvent(HANDLE ph, WORD wRecordStopEventMode, DWORD dwRecordStopDelayImages)
        self.PCO_SetRecordStopEvent=wrapper(lib.PCO_SetRecordStopEvent)
        #  ctypes.c_int PCO_StopRecord(HANDLE ph, ctypes.POINTER(WORD) wReserved0, ctypes.POINTER(DWORD) dwReserved1)
        self.PCO_StopRecord=wrapper(lib.PCO_StopRecord)
        #  ctypes.c_int PCO_SetDateTime(HANDLE ph, BYTE ucDay, BYTE ucMonth, WORD wYear, WORD wHour, BYTE ucMin, BYTE ucSec)
        self.PCO_SetDateTime=wrapper(lib.PCO_SetDateTime)
        #  ctypes.c_int PCO_GetTimestampMode(HANDLE ph, ctypes.POINTER(WORD) wTimeStampMode)
        self.PCO_GetTimestampMode=wrapper(lib.PCO_GetTimestampMode)
        #  ctypes.c_int PCO_SetTimestampMode(HANDLE ph, WORD wTimeStampMode)
        self.PCO_SetTimestampMode=wrapper(lib.PCO_SetTimestampMode)
        
        #  ctypes.c_int PCO_GetStorageStruct(HANDLE ph, ctypes.POINTER(PCO_Storage) strStorage)
        self.PCO_GetStorageStruct=wrapper(lib.PCO_GetStorageStruct,
            argprep={"strStorage":CPCO_Storage.prep_struct}, rconv={"strStorage":CPCO_Storage.tup_struct})
        #  ctypes.c_int PCO_SetStorageStruct(HANDLE ph, ctypes.POINTER(PCO_Storage) strStorage)
        self.PCO_SetStorageStruct=wrapper(lib.PCO_SetStorageStruct, args="all",
            rconv={"strStorage":CPCO_Storage.tup_struct})
        #  ctypes.c_int PCO_GetCameraRamSize(HANDLE ph, ctypes.POINTER(DWORD) dwRamSize, ctypes.POINTER(WORD) wPageSize)
        self.PCO_GetCameraRamSize=wrapper(lib.PCO_GetCameraRamSize)
        #  ctypes.c_int PCO_GetCameraRamSegmentSize(HANDLE ph, ctypes.POINTER(DWORD) dwRamSegSize)
        self.PCO_GetCameraRamSegmentSize=wrapper(lib.PCO_GetCameraRamSegmentSize,
            argprep={"dwRamSegSize":(DWORD*4)}, rconv={"dwRamSegSize": lambda v:v[:4]}, byref=[])
        #  ctypes.c_int PCO_SetCameraRamSegmentSize(HANDLE ph, ctypes.POINTER(DWORD) dwRamSegSize)
        self.PCO_SetCameraRamSegmentSize=wrapper(lib.PCO_SetCameraRamSegmentSize, args="all",
            argprep={"dwRamSegSize": lambda dwRamSegSize: build_arr(DWORD,4)(dwRamSegSize)}, rconv={"dwRamSegSize": lambda v:v[:4]}, byref=[])  # pylint: disable=unnecessary-lambda
        #  ctypes.c_int PCO_ClearRamSegment(HANDLE ph)
        self.PCO_ClearRamSegment=wrapper(lib.PCO_ClearRamSegment)
        #  ctypes.c_int PCO_GetActiveRamSegment(HANDLE ph, ctypes.POINTER(WORD) wActSeg)
        self.PCO_GetActiveRamSegment=wrapper(lib.PCO_GetActiveRamSegment)
        #  ctypes.c_int PCO_SetActiveRamSegment(HANDLE ph, WORD wActSeg)
        self.PCO_SetActiveRamSegment=wrapper(lib.PCO_SetActiveRamSegment)
        #  ctypes.c_int PCO_SetTransferParameter(HANDLE ph, ctypes.c_void_p buffer, ctypes.c_int ilen)
        self.PCO_SetTransferParameter_lib=wrapper(lib.PCO_SetTransferParameter)
        #  ctypes.c_int PCO_GetTransferParameter(HANDLE ph, ctypes.c_void_p buffer, ctypes.c_int ilen)
        self.PCO_GetTransferParameter_lib=wrapper(lib.PCO_GetTransferParameter)
        #  ctypes.c_int PCO_SetTransferParametersAuto(HANDLE ph, ctypes.c_void_p buffer, ctypes.c_int ilen)
        self.PCO_SetTransferParametersAuto=wrapper(lib.PCO_SetTransferParametersAuto, args=["ph"], rvals=[])
        #  ctypes.c_int PCO_GetActiveLookupTable(HANDLE ph, ctypes.POINTER(WORD) wIdentifier, ctypes.POINTER(WORD) wParameter)
        self.PCO_GetActiveLookupTable=wrapper(lib.PCO_GetActiveLookupTable)
        #  ctypes.c_int PCO_SetActiveLookupTable(HANDLE ph, ctypes.POINTER(WORD) wIdentifier, ctypes.POINTER(WORD) wParameter)
        self.PCO_SetActiveLookupTable=wrapper(lib.PCO_SetActiveLookupTable, args="all")
        #  ctypes.c_int PCO_GetLookupTableInfo(HANDLE ph, WORD wLUTNum, ctypes.POINTER(WORD) wNumberOfLuts, ctypes.c_char_p Description, WORD wDescLen, ctypes.POINTER(WORD) wIdentifier, ctypes.POINTER(BYTE) bInputWidth, ctypes.POINTER(BYTE) bOutputWidth, ctypes.POINTER(WORD) wFormat)
        self.PCO_GetLookupTableInfo=wrapper(lib.PCO_GetLookupTableInfo, args=["ph","wLUTNum"], rvals=["wNumberOfLuts","Description","wIdentifier","bInputWidth","bOutputWidth","wFormat"],
            argprep={"Description":strprep,"wDescLen":max_strlen}, byref=["wNumberOfLuts","wIdentifier","bInputWidth","bOutputWidth","wFormat"])
        #  ctypes.c_int PCO_GetCmosLineTiming(HANDLE hCam, ctypes.POINTER(WORD) wParameter, ctypes.POINTER(WORD) wTimeBase, ctypes.POINTER(DWORD) dwLineTime, ctypes.POINTER(DWORD) dwReserved, WORD wReservedLen)
        self.PCO_GetCmosLineTiming=wrapper(lib.PCO_GetCmosLineTiming)
        #  ctypes.c_int PCO_SetCmosLineTiming(HANDLE hCam, WORD wParameter, WORD wTimeBase, DWORD dwLineTime, ctypes.POINTER(DWORD) dwReserved, WORD wReservedLen)
        self.PCO_SetCmosLineTiming=wrapper(lib.PCO_SetCmosLineTiming, args=["hCam","wTimeBase","dwLineTime"])
        #  ctypes.c_int PCO_GetCmosLineExposureDelay(HANDLE hCam, ctypes.POINTER(DWORD) dwExposureLines, ctypes.POINTER(DWORD) dwDelayLines, ctypes.POINTER(DWORD) dwReserved, WORD wReservedLen)
        self.PCO_GetCmosLineExposureDelay=wrapper(lib.PCO_GetCmosLineExposureDelay)
        #  ctypes.c_int PCO_SetCmosLineExposureDelay(HANDLE hCam, DWORD dwExposureLines, DWORD dwDelayLines, ctypes.POINTER(DWORD) dwReserved, WORD wReservedLen)
        self.PCO_SetCmosLineExposureDelay=wrapper(lib.PCO_SetCmosLineExposureDelay, args=["hCam","dwExposureLines","dwDelayLines"], rvals=[])
        
        #  ctypes.c_int PCO_GetImageStruct(HANDLE ph, ctypes.POINTER(PCO_Image) strImage)
        self.PCO_GetImageStruct=wrapper(lib.PCO_GetImageStruct,
            argprep={"strImage":CPCO_Image.prep_struct}, rconv={"strImage":CPCO_Image.tup_struct})
        #  ctypes.c_int PCO_GetSegmentStruct(HANDLE ph, WORD wSegment, ctypes.POINTER(PCO_Segment) strSegment)
        self.PCO_GetSegmentStruct=wrapper(lib.PCO_GetSegmentStruct,
            argprep={"strSegment":CPCO_Segment.prep_struct}, rconv={"strSegment":CPCO_Segment.tup_struct})
        #  ctypes.c_int PCO_GetSegmentImageSettings(HANDLE ph, WORD wSegment, ctypes.POINTER(WORD) wXRes, ctypes.POINTER(WORD) wYRes, ctypes.POINTER(WORD) wBinHorz, ctypes.POINTER(WORD) wBinVert, ctypes.POINTER(WORD) wRoiX0, ctypes.POINTER(WORD) wRoiY0, ctypes.POINTER(WORD) wRoiX1, ctypes.POINTER(WORD) wRoiY1)
        self.PCO_GetSegmentImageSettings=wrapper(lib.PCO_GetSegmentImageSettings)
        #  ctypes.c_int PCO_GetNumberOfImagesInSegment(HANDLE ph, WORD wSegment, ctypes.POINTER(DWORD) dwValidImageCnt, ctypes.POINTER(DWORD) dwMaxImageCnt)
        self.PCO_GetNumberOfImagesInSegment=wrapper(lib.PCO_GetNumberOfImagesInSegment)
        #  ctypes.c_int PCO_GetBitAlignment(HANDLE ph, ctypes.POINTER(WORD) wBitAlignment)
        self.PCO_GetBitAlignment=wrapper(lib.PCO_GetBitAlignment)
        #  ctypes.c_int PCO_SetBitAlignment(HANDLE ph, WORD wBitAlignment)
        self.PCO_SetBitAlignment=wrapper(lib.PCO_SetBitAlignment)
        #  ctypes.c_int PCO_GetHotPixelCorrectionMode(HANDLE ph, ctypes.POINTER(WORD) wHotPixelCorrectionMode)
        self.PCO_GetHotPixelCorrectionMode=wrapper(lib.PCO_GetHotPixelCorrectionMode)
        #  ctypes.c_int PCO_SetHotPixelCorrectionMode(HANDLE ph, WORD wHotPixelCorrectionMode)
        self.PCO_SetHotPixelCorrectionMode=wrapper(lib.PCO_SetHotPixelCorrectionMode)
        #  ctypes.c_int PCO_GetColorCorrectionMatrix(HANDLE ph, ctypes.POINTER(ctypes.c_double) pdMatrix)
        self.PCO_GetColorCorrectionMatrix=wrapper(lib.PCO_GetColorCorrectionMatrix,
            argprep={"pdMatrix":(ctypes.c_double*9)()}, rconv={"pdMatrix": lambda v: v[:9]}, byref=[])

        #  ctypes.c_int PCO_AllocateBuffer(HANDLE ph, ctypes.POINTER(SHORT) sBufNr, DWORD size, ctypes.POINTER(ctypes.POINTER(WORD)) wBuf, ctypes.POINTER(HANDLE) hEvent)
        self.PCO_AllocateBuffer=wrapper(lib.PCO_AllocateBuffer, args="all")
        #  ctypes.c_int PCO_GetBuffer(HANDLE ph, SHORT sBufNr, ctypes.POINTER(ctypes.POINTER(WORD)) wBuf, ctypes.POINTER(HANDLE) hEvent)
        self.PCO_GetBuffer=wrapper(lib.PCO_GetBuffer)
        #  ctypes.c_int PCO_FreeBuffer(HANDLE ph, SHORT sBufNr)
        self.PCO_FreeBuffer=wrapper(lib.PCO_FreeBuffer)
        #  ctypes.c_int PCO_GetBufferStatus(HANDLE ph, SHORT sBufNr, ctypes.POINTER(DWORD) dwStatusDll, ctypes.POINTER(DWORD) dwStatusDrv)
        self.PCO_GetBufferStatus=wrapper(lib.PCO_GetBufferStatus)
        
        #  ctypes.c_int PCO_GetImageEx(HANDLE ph, WORD wSegment, DWORD dw1stImage, DWORD dwLastImage, SHORT sBufNr, WORD wXRes, WORD wYRes, WORD wBitPerPixel)
        self.PCO_GetImageEx=wrapper(lib.PCO_GetImageEx)
        #  ctypes.c_int PCO_AddBufferEx(HANDLE ph, DWORD dw1stImage, DWORD dwLastImage, SHORT sBufNr, WORD wXRes, WORD wYRes, WORD wBitPerPixel)
        self.PCO_AddBufferEx=wrapper(lib.PCO_AddBufferEx)
        #  ctypes.c_int PCO_AddBufferExtern(HANDLE ph, HANDLE hEvent, WORD wActSeg, DWORD dw1stImage, DWORD dwLastImage, DWORD dwSynch, ctypes.c_void_p pBuf, DWORD dwLen, ctypes.POINTER(DWORD) dwStatus)
        self.PCO_AddBufferExtern=wrapper(lib.PCO_AddBufferExtern, args="all", rvals=[], byref=[])
        #  ctypes.c_int PCO_CancelImages(HANDLE ph)
        self.PCO_CancelImages=wrapper(lib.PCO_CancelImages)
        #  ctypes.c_int PCO_GetPendingBuffer(HANDLE ph, ctypes.POINTER(ctypes.c_int) count)
        self.PCO_GetPendingBuffer=wrapper(lib.PCO_GetPendingBuffer)
        #  ctypes.c_int PCO_WaitforBuffer(HANDLE ph, ctypes.c_int nr_of_buffer, ctypes.POINTER(PCO_Buflist) bl, ctypes.c_int timeout)
        self.PCO_WaitforBuffer_lib=wrapper(lib.PCO_WaitforBuffer)
        #  ctypes.c_int PCO_EnableSoftROI(HANDLE ph, WORD wSoftROIFlags, ctypes.c_void_p unnamed_argument_001, ctypes.c_int unnamed_argument_002)
        self.PCO_EnableSoftROI=wrapper(lib.PCO_EnableSoftROI, args=["ph","wSoftROIFlags"])
        #  ctypes.c_int PCO_GetMetaData(HANDLE ph, SHORT sBufNr, ctypes.POINTER(PCO_METADATA_STRUCT) pMetaData, DWORD dwReserved1, DWORD dwReserved2)
        self.PCO_GetMetaData=wrapper(lib.PCO_GetMetaData, args=["ph","sBufNr","pMetaData"],
            argprep={"pMetaData":CPCO_METADATA_STRUCT.prep_struct}, rconv={"pMetaData":CPCO_METADATA_STRUCT.tup_struct})

        #  ctypes.c_int PCO_InitLensControl(HANDLE hCamera, ctypes.POINTER(HANDLE) phLensControl)
        self.PCO_InitLensControl=wrapper(lib.PCO_InitLensControl, args="all")
        #  ctypes.c_int PCO_CleanupLensControl()
        self.PCO_CleanupLensControl=wrapper(lib.PCO_CleanupLensControl)
        #  ctypes.c_int PCO_CloseLensControl(HANDLE hLensControl)
        self.PCO_CloseLensControl=wrapper(lib.PCO_CloseLensControl)
        #  ctypes.c_int PCO_GetLensFocus(HANDLE hLens, ctypes.POINTER(LONG) lFocusPos, ctypes.POINTER(DWORD) dwflags)
        self.PCO_GetLensFocus=wrapper(lib.PCO_GetLensFocus)
        #  ctypes.c_int PCO_SetLensFocus(HANDLE hLens, ctypes.POINTER(LONG) lFocusPos, DWORD dwflagsin, ctypes.POINTER(DWORD) dwflagsout)
        self.PCO_SetLensFocus=wrapper(lib.PCO_SetLensFocus, args=["hLens","lFocusPos","dwflagsin"])
        #  ctypes.c_int PCO_GetAperture(HANDLE hLens, ctypes.POINTER(WORD) wAperturePos, ctypes.POINTER(DWORD) dwflags)
        self.PCO_GetAperture=wrapper(lib.PCO_GetAperture)
        #  ctypes.c_int PCO_SetAperture(HANDLE hLens, ctypes.POINTER(WORD) wAperturePos, DWORD dwflagsin, ctypes.POINTER(DWORD) dwflagsout)
        self.PCO_SetAperture=wrapper(lib.PCO_SetAperture, args=["hLens","wAperturePos","dwflagsin"])
        #  ctypes.c_int PCO_GetApertureF(HANDLE hLens, ctypes.POINTER(DWORD) dwfAperturePos, ctypes.POINTER(WORD) wAperturePos, ctypes.POINTER(DWORD) dwflags)
        self.PCO_GetApertureF=wrapper(lib.PCO_GetApertureF)
        #  ctypes.c_int PCO_SetApertureF(HANDLE hLens, ctypes.POINTER(DWORD) dwfAperturePos, DWORD dwflagsin, ctypes.POINTER(DWORD) dwflagsout)
        self.PCO_SetApertureF=wrapper(lib.PCO_SetApertureF, args=["hLens","dwfAperturePos","dwflagsin"])

        #  ctypes.c_int PCO_GetFlimModulationParameter(HANDLE ph, ctypes.POINTER(WORD) wSourceSelect, ctypes.POINTER(WORD) wOutputWaveform, ctypes.POINTER(WORD) wReserved1, ctypes.POINTER(WORD) wReserved2)
        self.PCO_GetFlimModulationParameter=wrapper(lib.PCO_GetFlimModulationParameter)
        #  ctypes.c_int PCO_SetFlimModulationParameter(HANDLE ph, WORD wSourceSelect, WORD wOutputWaveform, WORD wReserved1, WORD wReserved2)
        self.PCO_SetFlimModulationParameter=wrapper(lib.PCO_SetFlimModulationParameter, args=["ph","wSourceSelect","wOutputWaveform"])
        #  ctypes.c_int PCO_GetFlimPhaseSequenceParameter(HANDLE ph, ctypes.POINTER(WORD) wPhaseNumber, ctypes.POINTER(WORD) wPhaseSymmetry, ctypes.POINTER(WORD) wPhaseOrder, ctypes.POINTER(WORD) wTapSelect, ctypes.POINTER(WORD) wReserved1, ctypes.POINTER(WORD) wReserved2)
        self.PCO_GetFlimPhaseSequenceParameter=wrapper(lib.PCO_GetFlimPhaseSequenceParameter)
        #  ctypes.c_int PCO_SetFlimPhaseSequenceParameter(HANDLE ph, WORD wPhaseNumber, WORD wPhaseSymmetry, WORD wPhaseOrder, WORD wTapSelect, WORD wReserved1, WORD wReserved2)
        self.PCO_SetFlimPhaseSequenceParameter=wrapper(lib.PCO_SetFlimPhaseSequenceParameter, args=["ph","wPhaseNumber","wPhaseSymmetry","wPhaseOrder","wTapSelect"])
        #  ctypes.c_int PCO_GetFlimImageProcessingFlow(HANDLE ph, ctypes.POINTER(WORD) wAsymmetryCorrection, ctypes.POINTER(WORD) wCalculationMode, ctypes.POINTER(WORD) wReferencingMode, ctypes.POINTER(WORD) wThresholdLow, ctypes.POINTER(WORD) wThresholdHigh, ctypes.POINTER(WORD) wOutputMode, ctypes.POINTER(WORD) wReserved1, ctypes.POINTER(WORD) wReserved2, ctypes.POINTER(WORD) wReserved3, ctypes.POINTER(WORD) wReserved4)
        self.PCO_GetFlimImageProcessingFlow=wrapper(lib.PCO_GetFlimImageProcessingFlow)
        #  ctypes.c_int PCO_SetFlimImageProcessingFlow(HANDLE ph, WORD wAsymmetryCorrection, WORD wCalculationMode, WORD wReferencingMode, WORD wThresholdLow, WORD wThresholdHigh, WORD wOutputMode, WORD wReserved1, WORD wReserved2, WORD wReserved3, WORD wReserved4)
        self.PCO_SetFlimImageProcessingFlow=wrapper(lib.PCO_SetFlimImageProcessingFlow,
            args=["ph","wAsymmetryCorrection","wCalculationMode","wReferencingMode","wThresholdLow","wThresholdHigh","wOutputMode"])
        #  ctypes.c_int PCO_GetFlimMasterModulationFrequency(HANDLE ph, ctypes.POINTER(DWORD) dwFrequency)
        self.PCO_GetFlimMasterModulationFrequency=wrapper(lib.PCO_GetFlimMasterModulationFrequency)
        #  ctypes.c_int PCO_SetFlimMasterModulationFrequency(HANDLE ph, DWORD dwFrequency)
        self.PCO_SetFlimMasterModulationFrequency=wrapper(lib.PCO_SetFlimMasterModulationFrequency)
        #  ctypes.c_int PCO_GetFlimRelativePhase(HANDLE ph, ctypes.POINTER(DWORD) dwPhaseMilliDeg)
        self.PCO_GetFlimRelativePhase=wrapper(lib.PCO_GetFlimRelativePhase)
        #  ctypes.c_int PCO_SetFlimRelativePhase(HANDLE ph, DWORD dwPhaseMilliDeg)
        self.PCO_SetFlimRelativePhase=wrapper(lib.PCO_SetFlimRelativePhase)

        self.kernel32=ctypes.windll.kernel32
        wrapper=ctypes_wrap.CFunctionWrapper()
        self.CreateEventA=wrapper.wrap_bare(self.kernel32.CreateEventA, [ctypes.c_void_p,BOOL,BOOL,ctypes.c_char_p], ["attr","man_reset","init_state","name"], restype=HANDLE)
        self.CloseHandle=wrapper.wrap_bare(self.kernel32.CloseHandle, [HANDLE], ["handle"], restype=BOOL)
        self.ResetEvent=wrapper.wrap_bare(self.kernel32.ResetEvent, [HANDLE], ["handle"], restype=BOOL)
        self.SetEvent=wrapper.wrap_bare(self.kernel32.SetEvent, [HANDLE], ["handle"], restype=BOOL)
        self.WaitForSingleObject=wrapper.wrap_bare(self.kernel32.WaitForSingleObject, [HANDLE, DWORD], ["handle","timeout"], restype=DWORD)
        self.WaitForMultipleObjects=wrapper.wrap_bare(self.kernel32.WaitForMultipleObjects, [DWORD, ctypes.POINTER(HANDLE), BOOL, DWORD], ["count","handles","wait_all","timeout"], restype=DWORD)

        self._initialized=True

        return

        ### Obsolete ###
        #  ctypes.c_int PCO_CamLinkSetImageParameters(HANDLE ph, WORD wxres, WORD wyres)
        #  ctypes.c_int PCO_GetImage(HANDLE ph, WORD wSegment, DWORD dw1stImage, DWORD dwLastImage, SHORT sBufNr)
        #  ctypes.c_int PCO_AddBuffer(HANDLE ph, DWORD dw1stImage, DWORD dwLastImage, SHORT sBufNr)
        #  ctypes.c_int PCO_RemoveBuffer(HANDLE ph)

        ### Hard to adequately test (complicated interface and no access to hardware) ###
        #  ctypes.c_int PCO_GetImageTransferMode(HANDLE ph, ctypes.c_void_p param, ctypes.c_int ilen)
        #  ctypes.c_int PCO_SetImageTransferMode(HANDLE ph, ctypes.c_void_p param, ctypes.c_int ilen)
        #  ctypes.c_int PCO_SendBirgerCommand(HANDLE hLens, ctypes.POINTER(PCO_Birger) pstrBirger, ctypes.c_char_p szcmd, ctypes.c_int inumdelim)
        #  ctypes.c_int PCO_PlayImagesFromSegmentHDSDI(HANDLE ph, WORD wSegment, WORD wInterface, WORD wMode, WORD wSpeed, DWORD dwRangeLow, DWORD dwRangeHigh, DWORD dwStartPos)
        #  ctypes.c_int PCO_GetPlayPositionHDSDI(HANDLE ph, ctypes.POINTER(WORD) wStatus, ctypes.POINTER(DWORD) dwPlayPosition)
        #  ctypes.c_int PCO_GetInterfaceOutputFormat(HANDLE ph, ctypes.POINTER(WORD) wDestInterface, ctypes.POINTER(WORD) wFormat, ctypes.POINTER(WORD) wReserved1, ctypes.POINTER(WORD) wReserved2)
        #  ctypes.c_int PCO_SetInterfaceOutputFormat(HANDLE ph, WORD wDestInterface, WORD wFormat, WORD wReserved1, WORD wReserved2)
        #  ctypes.c_int PCO_SetColorSettings(HANDLE ph, ctypes.POINTER(PCO_Image_ColorSet) strColorSet)
        #  ctypes.c_int PCO_GetColorSettings(HANDLE ph, ctypes.POINTER(PCO_Image_ColorSet) strColorSet)
        #  ctypes.c_int PCO_DoWhiteBalance(HANDLE ph, WORD wMode, ctypes.POINTER(WORD) wParam, WORD wParamLen)
        
        ### Not documented in the manual (only in .h file) ###
        #  ctypes.c_int PCO_GetDSNUAdjustMode(HANDLE ph, ctypes.POINTER(WORD) wDSNUAdjustMode, ctypes.POINTER(WORD) wReserved)
        #  ctypes.c_int PCO_SetDSNUAdjustMode(HANDLE ph, WORD wDSNUAdjustMode, WORD wReserved)
        #  ctypes.c_int PCO_InitDSNUAdjustment(HANDLE ph, WORD wDSNUAdjustMode, WORD wReserved)
        #  ctypes.c_int PCO_GetIntensifiedGatingMode(HANDLE ph, ctypes.POINTER(WORD) wIntensifiedGatingMode, ctypes.POINTER(WORD) wReserved)
        #  ctypes.c_int PCO_SetIntensifiedGatingMode(HANDLE ph, WORD wIntensifiedGatingMode, WORD wReserved)
        #  ctypes.c_int PCO_GetIntensifiedMCP(HANDLE ph, ctypes.POINTER(WORD) wIntensifiedVoltage, ctypes.POINTER(WORD) wReserved, ctypes.POINTER(DWORD) dwIntensifiedPhosphorDecay_us, ctypes.POINTER(DWORD) dwReserved1, ctypes.POINTER(DWORD) dwReserved2)
        #  ctypes.c_int PCO_SetIntensifiedMCP(HANDLE ph, WORD wIntensifiedVoltage, WORD wFlags, WORD wReserved, DWORD dwIntensifiedPhosphorDecay_us, DWORD dwReserved1, DWORD dwReserved2)
        #  ctypes.c_int PCO_GetIntensifiedLoopCount(HANDLE hCam, ctypes.POINTER(WORD) wIntensifiedLoopCount, ctypes.POINTER(WORD) wReserved)
        #  ctypes.c_int PCO_SetIntensifiedLoopCount(HANDLE hCam, WORD wIntensifiedLoopCount, WORD wReserved)

        ### Unnecessary ###
        # All description can be obtained using PCO_GetSensorStruct
        #  ctypes.c_int PCO_GetCameraDescriptionEx(HANDLE ph, ctypes.POINTER(PCO_DescriptionEx) strDescription, WORD wType)
        
	
    def PCO_WaitforBuffer(self, handle, nums, timeout):
        buffs=(sc2_camexport_defs.PCO_Buflist*len(nums))()
        for i,n in enumerate(nums):
            buffs[i].sBufNr=n
        self.PCO_WaitforBuffer_lib(handle,len(nums),buffs,timeout)
        return [CPCO_Buflist.tup_struct(b) for b in buffs]

    def CreateEvent(self, man_reset=True, init_state=False):
        return self.CreateEventA(None,man_reset,init_state,None)



wlib=PCOSC2Lib()