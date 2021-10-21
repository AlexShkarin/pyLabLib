# pylint: disable=wrong-spelling-in-comment

from . import uc480_defs
from .uc480_defs import ERROR, drERROR  # pylint: disable=unused-import
from .uc480_defs import UC480_CAMERA_INFO
from .uc480_defs import define_functions

from ...core.utils import ctypes_wrap
from ..utils import load_lib
from ...core.devio.comm_backend import DeviceError

import ctypes
import platform


class uc480Error(DeviceError):
    """Generic uc480 error"""
class uc480LibError(uc480Error):
    """Generic uc480 library error"""
    def __init__(self, func, code):
        self.func=func
        self.code=code
        self.name=drERROR.get(self.code,"UNKNOWN")
        self.msg="function '{}' raised error {}({})".format(func,code,self.name)
        uc480Error.__init__(self,self.msg)
def errcheck(simple=False):
    """
    Build an error checking function.

    Return a function which checks return codes of uc480 library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    def errchecker(result, func, arguments):  # pylint: disable=unused-argument
        if result<0 or (not simple and result!=0):
            raise uc480LibError(func.__name__,result)
        return result
    return errchecker


class CBOARDINFO(uc480_defs.CBOARDINFO):
    _tup_exc={"Reserved"}

class CUC480_CAMERA_INFO(uc480_defs.CUC480_CAMERA_INFO):
    _tup_exc={"dwReserved","dwReserved2"}

class CSENSORINFO(uc480_defs.CSENSORINFO):
    _tup_exc={"Reserved"}

class CUC480TIME(uc480_defs.CUC480TIME):
    _tup_exc={"byReserved"}

class CUC480IMAGEINFO(uc480_defs.CUC480IMAGEINFO):
    _tup_exc={"byReserved1","dwReserved3"}
    _tup={"TimestampSystem":CUC480TIME.tup_struct}

class CUC480_CAPTURE_STATUS_INFO(uc480_defs.CUC480_CAPTURE_STATUS_INFO):
    _tup_exc={"reserved"}



class uc480Lib:
    def __init__(self, backend="uc480"):
        self.backend=backend
        self._initialized=False

    @staticmethod
    def _load_dll(backend):
        if backend=="uc480":
            lib_name="uc480.dll" if platform.architecture()[0][:2]=="32" else "uc480_64.dll"
            thorcam_path=load_lib.get_program_files_folder("Thorlabs/Scientific Imaging/ThorCam")
            error_message="The library is automatically supplied with Thorcam software\n"+load_lib.par_error_message.format("uc480")
            return load_lib.load_lib(lib_name,locations=("parameter/uc480",thorcam_path,"global"),error_message=error_message,call_conv="cdecl")
        elif backend=="ueye":
            lib_name="ueye_api.dll" if platform.architecture()[0][:2]=="32" else "ueye_api_64.dll"
            ueye_path=load_lib.get_program_files_folder("IDS/uEye/USB driver package")
            ids_path=load_lib.get_program_files_folder("IDS/uEye/develop/bin")
            error_message="The library is automatically supplied with IDS uEye or IDS Software Suite\n"+load_lib.par_error_message.format("ueye")
            return load_lib.load_lib(lib_name,locations=("parameter/ueye",ueye_path,ids_path,"global"),error_message=error_message,call_conv="cdecl")
        else:
            raise RuntimeError("unrecognized backend: {}".format(backend))

    def initlib(self):
        if self._initialized:
            return
        self.lib=self._load_dll(self.backend)
        lib=self.lib
        define_functions(lib)

        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(),default_rvals="pointer")
        rwrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(simple=True))

        #  INT is_GetError(HCAM hCam, ctypes.POINTER(INT) pErr, ctypes.POINTER(ctypes.c_char_p) ppcErr)
        self.is_GetError=wrapper(lib.is_GetError)
        #  INT is_SetErrorReport(HCAM hCam, INT Mode)
        self.is_SetErrorReport=rwrapper(lib.is_SetErrorReport)
        #  INT is_EnableMessage(HCAM hCam, INT which, HWND hWnd)
        self.is_EnableMessage=wrapper(lib.is_EnableMessage)

        #  INT is_GetNumberOfCameras(ctypes.POINTER(INT) pnNumCams)
        self.is_GetNumberOfCameras=wrapper(lib.is_GetNumberOfCameras)
        #  INT is_GetCameraList(PUC480_CAMERA_LIST pucl)
        lib.is_GetCameraList.argtypes=[ctypes.c_void_p]
        self.is_GetCameraList_lib=wrapper(lib.is_GetCameraList, args="all")
        #  INT is_InitCamera(ctypes.POINTER(HCAM) phCam, HWND hWnd)
        self.is_InitCamera=wrapper(lib.is_InitCamera, args="all")
        #  INT is_ExitCamera(HCAM hCam)
        self.is_ExitCamera=wrapper(lib.is_ExitCamera)
        #  INT is_GetCameraInfo(HCAM hCam, PBOARDINFO pInfo)
        self.is_GetCameraInfo=wrapper(lib.is_GetCameraInfo,
            rconv={"pInfo":CBOARDINFO.tup_struct})
        #  INT is_GetSensorInfo(HCAM hCam, PSENSORINFO pInfo)
        self.is_GetSensorInfo=wrapper(lib.is_GetSensorInfo,
            rconv={"pInfo":CSENSORINFO.tup_struct})
        #  INT is_GetDLLVersion()
        self.is_GetDLLVersion=rwrapper(lib.is_GetDLLVersion)
        #  ULONG is_CameraStatus(HCAM hCam, INT nInfo, ULONG ulValue)
        self.is_CameraStatus=self.wrap_setget_func(lib.is_CameraStatus)
        #  INT is_CaptureStatus(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
        self.is_CaptureStatus=rwrapper(lib.is_CaptureStatus)
        #  INT is_GetBusSpeed(HCAM hCam)
        self.is_GetBusSpeed=self.wrap_setget_func(lib.is_GetBusSpeed)
        #  INT is_ResetToDefault(HCAM hCam)
        self.is_ResetToDefault=wrapper(lib.is_ResetToDefault)

        #  INT is_GetFrameTimeRange(HCAM hCam, ctypes.POINTER(ctypes.c_double) min, ctypes.POINTER(ctypes.c_double) max, ctypes.POINTER(ctypes.c_double) intervall)
        self.is_GetFrameTimeRange=wrapper(lib.is_GetFrameTimeRange)
        #  INT is_SetFrameRate(HCAM hCam, ctypes.c_double FPS, ctypes.POINTER(ctypes.c_double) newFPS)
        self.is_SetFrameRate=wrapper(lib.is_SetFrameRate)
        #  INT is_GetFramesPerSecond(HCAM hCam, ctypes.POINTER(ctypes.c_double) dblFPS)
        self.is_GetFramesPerSecond=wrapper(lib.is_GetFramesPerSecond)
        #  INT is_PixelClock(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        self.is_PixelClock=self.wrap_parfunc(lib.is_PixelClock)
        #  INT is_GetVsyncCount(HCAM hCam, ctypes.POINTER(ctypes.c_long) pIntr, ctypes.POINTER(ctypes.c_long) pActIntr)
        self.is_GetVsyncCount=wrapper(lib.is_GetVsyncCount)
        #  INT is_Exposure(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        self.is_Exposure=self.wrap_parfunc(lib.is_Exposure)
        #  INT is_SetSubSampling(HCAM hCam, INT mode)
        self.is_SetSubSampling=self.wrap_setget_func(lib.is_SetSubSampling)
        #  INT is_SetBinning(HCAM hCam, INT mode)
        self.is_SetBinning=self.wrap_setget_func(lib.is_SetBinning)
        #  INT is_AOI(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT SizeOfParam)
        self.is_AOI=self.wrap_parfunc(lib.is_AOI)
        #  INT is_SetColorMode(HCAM hCam, INT Mode)
        self.is_SetColorMode=self.wrap_setget_func(lib.is_SetColorMode)
        #  INT is_GetColorDepth(HCAM hCam, ctypes.POINTER(INT) pnCol, ctypes.POINTER(INT) pnColMode)
        self.is_GetColorDepth=wrapper(lib.is_GetColorDepth)
        #  INT is_Blacklevel(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        self.is_Blacklevel=self.wrap_parfunc(lib.is_Blacklevel)
        #  INT is_SetSaturation(HCAM hCam, INT ChromU, INT ChromV)
        self.is_SetSaturation=self.wrap_setget_func(lib.is_SetSaturation)
        #  INT is_GetUsedBandwidth(HCAM hCam)
        self.is_GetUsedBandwidth=self.wrap_setget_func(lib.is_GetUsedBandwidth)
        #  INT is_SetHardwareGain(HCAM hCam, INT nMaster, INT nRed, INT nGreen, INT nBlue)
        self.is_SetHardwareGain=self.wrap_setget_func(lib.is_SetHardwareGain)
        #  INT is_SetGainBoost(HCAM hCam, INT mode)
        self.is_SetGainBoost=self.wrap_setget_func(lib.is_SetGainBoost)
        #  INT is_SetHWGainFactor(HCAM hCam, INT nMode, INT nFactor)
        self.is_SetHWGainFactor=self.wrap_setget_func(lib.is_SetHWGainFactor)
        #  INT is_SetHardwareGamma(HCAM hCam, INT nMode)
        self.is_SetHardwareGamma=self.wrap_setget_func(lib.is_SetHardwareGamma)
        #  INT is_SetCameraID(HCAM hCam, INT nID)
        self.is_SetCameraID=self.wrap_setget_func(lib.is_SetCameraID)
        #  INT is_HotPixel(HCAM hCam, UINT nMode, ctypes.c_void_p pParam, UINT SizeOfParam)
        self.is_HotPixel=self.wrap_parfunc(lib.is_HotPixel)

        #  INT is_SetExternalTrigger(HCAM hCam, INT nTriggerMode)
        self.is_SetExternalTrigger=self.wrap_setget_func(lib.is_SetExternalTrigger)
        #  INT is_SetTriggerCounter(HCAM hCam, INT nValue)
        self.is_SetTriggerCounter=self.wrap_setget_func(lib.is_SetTriggerCounter)
        #  INT is_SetTriggerDelay(HCAM hCam, INT nTriggerDelay)
        self.is_SetTriggerDelay=self.wrap_setget_func(lib.is_SetTriggerDelay)
        #  INT is_ForceTrigger(HCAM hCam)
        self.is_ForceTrigger=wrapper(lib.is_ForceTrigger)

        #  INT is_FreezeVideo(HCAM hCam, INT Wait)
        self.is_FreezeVideo=wrapper(lib.is_FreezeVideo)
        #  INT is_CaptureVideo(HCAM hCam, INT Wait)
        self.is_CaptureVideo=self.wrap_setget_func(lib.is_CaptureVideo)
        #  INT is_StopLiveVideo(HCAM hCam, INT Wait)
        self.is_StopLiveVideo=wrapper(lib.is_StopLiveVideo)
        #  INT is_HasVideoStarted(HCAM hCam, ctypes.POINTER(BOOL) pbo)
        self.is_HasVideoStarted=wrapper(lib.is_HasVideoStarted)
        #  INT is_IsVideoFinish(HCAM hCam, ctypes.POINTER(INT) pValue)
        self.is_IsVideoFinish=wrapper(lib.is_IsVideoFinish)
        
        #  INT is_AllocImageMem(HCAM hCam, INT width, INT height, INT bitspixel, ctypes.POINTER(ctypes.c_char_p) ppcImgMem, ctypes.POINTER(ctypes.c_int) pid)
        self.is_AllocImageMem=wrapper(lib.is_AllocImageMem,
            rconv={"ppcImgMem":"ctypes"})
        #  INT is_SetImageMem(HCAM hCam, ctypes.c_char_p pcMem, ctypes.c_int id)
        self.is_SetImageMem=wrapper(lib.is_SetImageMem)
        #  INT is_GetImageMem(HCAM hCam, ctypes.POINTER(ctypes.c_void_p) pMem)
        self.is_GetImageMem=wrapper(lib.is_GetImageMem)
        #  INT is_GetActiveImageMem(HCAM hCam, ctypes.POINTER(ctypes.c_char_p) ppcMem, ctypes.POINTER(ctypes.c_int) pnID)
        self.is_GetActiveImageMem=wrapper(lib.is_GetActiveImageMem,
            rconv={"ppcMem":"ctypes"})
        #  INT is_FreeImageMem(HCAM hCam, ctypes.c_char_p pcMem, ctypes.c_int id)
        self.is_FreeImageMem=wrapper(lib.is_FreeImageMem)
        #  INT is_GetImageMemPitch(HCAM hCam, ctypes.POINTER(INT) pPitch)
        self.is_GetImageMemPitch=wrapper(lib.is_GetImageMemPitch)
        #  INT is_SetAllocatedImageMem(HCAM hCam, INT width, INT height, INT bitspixel, ctypes.c_char_p pcImgMem, ctypes.POINTER(ctypes.c_int) pid)
        self.is_SetAllocatedImageMem=wrapper(lib.is_SetAllocatedImageMem)
        #  INT is_CopyImageMem(HCAM hCam, ctypes.c_char_p pcSource, ctypes.c_int nID, ctypes.c_char_p pcDest)
        self.is_CopyImageMem=wrapper(lib.is_CopyImageMem)
        #  INT is_CopyImageMemLines(HCAM hCam, ctypes.c_char_p pcSource, ctypes.c_int nID, ctypes.c_int nLines, ctypes.c_char_p pcDest)
        self.is_CopyImageMemLines=wrapper(lib.is_CopyImageMemLines)
        #  INT is_InquireImageMem(HCAM hCam, ctypes.c_char_p pcMem, ctypes.c_int nID, ctypes.POINTER(ctypes.c_int) pnX, ctypes.POINTER(ctypes.c_int) pnY, ctypes.POINTER(ctypes.c_int) pnBits, ctypes.POINTER(ctypes.c_int) pnPitch)
        self.is_InquireImageMem=wrapper(lib.is_InquireImageMem)
        #  INT is_GetImageInfo(HCAM hCam, INT nImageBufferID, ctypes.POINTER(UC480IMAGEINFO) pImageInfo, INT nImageInfoSize)
        self.is_GetImageInfo=wrapper(lib.is_GetImageInfo, args=["hCam","nImageBufferID"],
            argprep={"nImageInfoSize":ctypes.sizeof(uc480_defs.UC480IMAGEINFO)}, rconv={"pImageInfo":CUC480IMAGEINFO.tup_struct})
        
        #  INT is_AddToSequence(HCAM hCam, ctypes.c_char_p pcMem, INT nID)
        self.is_AddToSequence=wrapper(lib.is_AddToSequence)
        #  INT is_ClearSequence(HCAM hCam)
        self.is_ClearSequence=wrapper(lib.is_ClearSequence)
        #  INT is_GetActSeqBuf(HCAM hCam, ctypes.POINTER(INT) pnNum, ctypes.POINTER(ctypes.c_char_p) ppcMem, ctypes.POINTER(ctypes.c_char_p) ppcMemLast)
        self.is_GetActSeqBuf=wrapper(lib.is_GetActSeqBuf,
            rconv={"ppcMem":"ctypes","ppcMemLast":"ctypes"})
        #  INT is_LockSeqBuf(HCAM hCam, INT nNum, ctypes.c_char_p pcMem)
        self.is_LockSeqBuf=wrapper(lib.is_LockSeqBuf)
        #  INT is_UnlockSeqBuf(HCAM hCam, INT nNum, ctypes.c_char_p pcMem)
        self.is_UnlockSeqBuf=wrapper(lib.is_UnlockSeqBuf)
        
        #  INT is_InitImageQueue(HCAM hCam, INT nMode)
        self.is_InitImageQueue=wrapper(lib.is_InitImageQueue)
        #  INT is_ExitImageQueue(HCAM hCam)
        self.is_ExitImageQueue=wrapper(lib.is_ExitImageQueue)
        #  INT is_SetTimeout(HCAM hCam, UINT nMode, UINT Timeout)
        self.is_SetTimeout=wrapper(lib.is_SetTimeout)
        #  INT is_GetTimeout(HCAM hCam, UINT nMode, ctypes.POINTER(UINT) pTimeout)
        self.is_GetTimeout=wrapper(lib.is_GetTimeout)
        #  INT is_WaitForNextImage(HCAM hCam, UINT timeout, ctypes.POINTER(ctypes.c_char_p) ppcMem, ctypes.POINTER(INT) imageID)
        self.is_WaitForNextImage=wrapper(lib.is_WaitForNextImage,
            rconv={"ppcMem":"ctypes"})
        #  INT is_InitEvent(HCAM hCam, HANDLE hEv, INT which)
        self.is_InitEvent=wrapper(lib.is_InitEvent)
        #  INT is_ExitEvent(HCAM hCam, INT which)
        self.is_ExitEvent=wrapper(lib.is_ExitEvent)
        #  INT is_EnableEvent(HCAM hCam, INT which)
        self.is_EnableEvent=wrapper(lib.is_EnableEvent)
        #  INT is_DisableEvent(HCAM hCam, INT which)
        self.is_DisableEvent=wrapper(lib.is_DisableEvent)
        
        
        self._initialized=True
        return

        
        # #  INT is_PrepareStealVideo(HCAM hCam, ctypes.c_int Mode, ULONG StealColorMode)
        # self.is_PrepareStealVideo=wrapper(lib.is_PrepareStealVideo)
        # #  INT is_ReadEEPROM(HCAM hCam, INT Adr, ctypes.c_char_p pcString, INT Count)
        # self.is_ReadEEPROM=wrapper(lib.is_ReadEEPROM)
        # #  INT is_WriteEEPROM(HCAM hCam, INT Adr, ctypes.c_char_p pcString, INT Count)
        # self.is_WriteEEPROM=wrapper(lib.is_WriteEEPROM)
        # #  INT is_SetRopEffect(HCAM hCam, INT effect, INT param, INT reserved)
        # self.is_SetRopEffect=wrapper(lib.is_SetRopEffect)
        # #  INT is_GetRevisionInfo(HCAM hCam, PREVISIONINFO prevInfo)
        # self.is_GetRevisionInfo=wrapper(lib.is_GetRevisionInfo)
        # #  INT is_EnableAutoExit(HCAM hCam, INT nMode)
        # self.is_EnableAutoExit=wrapper(lib.is_EnableAutoExit)
        # #  INT is_SetWhiteBalance(HCAM hCam, INT nMode)
        # self.is_SetWhiteBalance=wrapper(lib.is_SetWhiteBalance)
        # #  INT is_SetWhiteBalanceMultipliers(HCAM hCam, ctypes.c_double dblRed, ctypes.c_double dblGreen, ctypes.c_double dblBlue)
        # self.is_SetWhiteBalanceMultipliers=wrapper(lib.is_SetWhiteBalanceMultipliers)
        # #  INT is_GetWhiteBalanceMultipliers(HCAM hCam, ctypes.POINTER(ctypes.c_double) pdblRed, ctypes.POINTER(ctypes.c_double) pdblGreen, ctypes.POINTER(ctypes.c_double) pdblBlue)
        # self.is_GetWhiteBalanceMultipliers=wrapper(lib.is_GetWhiteBalanceMultipliers)
        # #  INT is_SetColorCorrection(HCAM hCam, INT nEnable, ctypes.POINTER(ctypes.c_double) factors)
        # self.is_SetColorCorrection=wrapper(lib.is_SetColorCorrection)
        # #  INT is_SetBayerConversion(HCAM hCam, INT nMode)
        # self.is_SetBayerConversion=wrapper(lib.is_SetBayerConversion)
        # #  INT is_SetAutoParameter(HCAM hCam, INT param, ctypes.POINTER(ctypes.c_double) pval1, ctypes.POINTER(ctypes.c_double) pval2)
        # self.is_SetAutoParameter=wrapper(lib.is_SetAutoParameter)
        # #  INT is_GetAutoInfo(HCAM hCam, ctypes.POINTER(UC480_AUTO_INFO) pInfo)
        # self.is_GetAutoInfo=wrapper(lib.is_GetAutoInfo)
        # #  INT is_SetGlobalShutter(HCAM hCam, INT mode)
        # self.is_SetGlobalShutter=wrapper(lib.is_SetGlobalShutter)
        # #  INT is_SetExtendedRegister(HCAM hCam, INT index, WORD value)
        # self.is_SetExtendedRegister=wrapper(lib.is_SetExtendedRegister)
        # #  INT is_GetExtendedRegister(HCAM hCam, INT index, ctypes.POINTER(WORD) pwValue)
        # self.is_GetExtendedRegister=wrapper(lib.is_GetExtendedRegister)
        # #  INT is_WriteI2C(HCAM hCam, INT nDeviceAddr, INT nRegisterAddr, ctypes.POINTER(BYTE) pbData, INT nLen)
        # self.is_WriteI2C=wrapper(lib.is_WriteI2C)
        # #  INT is_ReadI2C(HCAM hCam, INT nDeviceAddr, INT nRegisterAddr, ctypes.POINTER(BYTE) pbData, INT nLen)
        # self.is_ReadI2C=wrapper(lib.is_ReadI2C)
        # #  INT is_GetHdrMode(HCAM hCam, ctypes.POINTER(INT) Mode)
        # self.is_GetHdrMode=wrapper(lib.is_GetHdrMode)
        # #  INT is_EnableHdr(HCAM hCam, INT Enable)
        # self.is_EnableHdr=wrapper(lib.is_EnableHdr)
        # #  INT is_SetHdrKneepoints(HCAM hCam, ctypes.POINTER(KNEEPOINTARRAY) KneepointArray, INT KneepointArraySize)
        # self.is_SetHdrKneepoints=wrapper(lib.is_SetHdrKneepoints)
        # #  INT is_GetHdrKneepoints(HCAM hCam, ctypes.POINTER(KNEEPOINTARRAY) KneepointArray, INT KneepointArraySize)
        # self.is_GetHdrKneepoints=wrapper(lib.is_GetHdrKneepoints)
        # #  INT is_GetHdrKneepointInfo(HCAM hCam, ctypes.POINTER(KNEEPOINTINFO) KneepointInfo, INT KneepointInfoSize)
        # self.is_GetHdrKneepointInfo=wrapper(lib.is_GetHdrKneepointInfo)
        # #  INT is_SetOptimalCameraTiming(HCAM hCam, INT Mode, INT Timeout, ctypes.POINTER(INT) pMaxPxlClk, ctypes.POINTER(ctypes.c_double) pMaxFrameRate)
        # self.is_SetOptimalCameraTiming=wrapper(lib.is_SetOptimalCameraTiming)
        # #  INT is_GetSupportedTestImages(HCAM hCam, ctypes.POINTER(INT) SupportedTestImages)
        # self.is_GetSupportedTestImages=wrapper(lib.is_GetSupportedTestImages)
        # #  INT is_GetTestImageValueRange(HCAM hCam, INT TestImage, ctypes.POINTER(INT) TestImageValueMin, ctypes.POINTER(INT) TestImageValueMax)
        # self.is_GetTestImageValueRange=wrapper(lib.is_GetTestImageValueRange)
        # #  INT is_SetSensorTestImage(HCAM hCam, INT Param1, INT Param2)
        # self.is_SetSensorTestImage=wrapper(lib.is_SetSensorTestImage)
        # #  INT is_GetColorConverter(HCAM hCam, INT ColorMode, ctypes.POINTER(INT) pCurrentConvertMode, ctypes.POINTER(INT) pDefaultConvertMode, ctypes.POINTER(INT) pSupportedConvertModes)
        # self.is_GetColorConverter=wrapper(lib.is_GetColorConverter)
        # #  INT is_SetColorConverter(HCAM hCam, INT ColorMode, INT ConvertMode)
        # self.is_SetColorConverter=wrapper(lib.is_SetColorConverter)
        # #  INT is_GetDuration(HCAM hCam, UINT nMode, ctypes.POINTER(INT) pnTime)
        # self.is_GetDuration=wrapper(lib.is_GetDuration)
        # #  INT is_GetSensorScalerInfo(HCAM hCam, ctypes.POINTER(SENSORSCALERINFO) pSensorScalerInfo, INT nSensorScalerInfoSize)
        # self.is_GetSensorScalerInfo=wrapper(lib.is_GetSensorScalerInfo)
        # #  INT is_SetSensorScaler(HCAM hCam, UINT nMode, ctypes.c_double dblFactor)
        # self.is_SetSensorScaler=wrapper(lib.is_SetSensorScaler)
        # #  INT is_ImageFormat(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
        # self.is_ImageFormat=wrapper(lib.is_ImageFormat)
        # #  INT is_FaceDetection(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
        # self.is_FaceDetection=wrapper(lib.is_FaceDetection)
        # #  INT is_Focus(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
        # self.is_Focus=wrapper(lib.is_Focus)
        # #  INT is_ImageStabilization(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
        # self.is_ImageStabilization=wrapper(lib.is_ImageStabilization)
        # #  INT is_ScenePreset(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
        # self.is_ScenePreset=wrapper(lib.is_ScenePreset)
        # #  INT is_Zoom(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
        # self.is_Zoom=wrapper(lib.is_Zoom)
        # #  INT is_Sharpness(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
        # self.is_Sharpness=wrapper(lib.is_Sharpness)
        # #  INT is_Saturation(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
        # self.is_Saturation=wrapper(lib.is_Saturation)
        # #  INT is_TriggerDebounce(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
        # self.is_TriggerDebounce=wrapper(lib.is_TriggerDebounce)
        # #  INT is_ColorTemperature(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
        # self.is_ColorTemperature=wrapper(lib.is_ColorTemperature)
        # #  INT is_Transfer(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_Transfer=wrapper(lib.is_Transfer)
        # #  INT is_BootBoost(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_BootBoost=wrapper(lib.is_BootBoost)
        # #  INT is_DeviceFeature(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_DeviceFeature=wrapper(lib.is_DeviceFeature)
        # #  INT is_Trigger(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_Trigger=wrapper(lib.is_Trigger)
        # #  INT is_DeviceInfo(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_DeviceInfo=wrapper(lib.is_DeviceInfo)
        # #  INT is_Callback(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_Callback=wrapper(lib.is_Callback)
        # #  INT is_OptimalCameraTiming(HCAM hCam, UINT u32Command, ctypes.c_void_p pParam, UINT u32SizeOfParam)
        # self.is_OptimalCameraTiming=wrapper(lib.is_OptimalCameraTiming)
        # #  INT is_SetStarterFirmware(HCAM hCam, ctypes.c_char_p pcFilepath, UINT uFilepathLen)
        # self.is_SetStarterFirmware=wrapper(lib.is_SetStarterFirmware)
        # #  INT is_SetPacketFilter(INT iAdapterID, UINT uFilterSetting)
        # self.is_SetPacketFilter=wrapper(lib.is_SetPacketFilter)
        # #  INT is_GetComportNumber(HCAM hCam, ctypes.POINTER(UINT) pComportNumber)
        # self.is_GetComportNumber=wrapper(lib.is_GetComportNumber)
        # #  INT is_IpConfig(INT iID, UC480_ETH_ADDR_MAC mac, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_IpConfig=wrapper(lib.is_IpConfig)
        # #  INT is_Configuration(UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_Configuration=wrapper(lib.is_Configuration)
        # #  INT is_IO(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_IO=wrapper(lib.is_IO)
        # #  INT is_AutoParameter(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_AutoParameter=wrapper(lib.is_AutoParameter)
        # #  INT is_Convert(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_Convert=wrapper(lib.is_Convert)
        # #  INT is_ParameterSet(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_ParameterSet=wrapper(lib.is_ParameterSet)
        # #  INT is_EdgeEnhancement(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_EdgeEnhancement=wrapper(lib.is_EdgeEnhancement)
        # #  INT is_ImageFile(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_ImageFile=wrapper(lib.is_ImageFile)
        # #  INT is_ImageBuffer(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_ImageBuffer=wrapper(lib.is_ImageBuffer)
        # #  INT is_Measure(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_Measure=wrapper(lib.is_Measure)
        # #  INT is_LUT(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParams)
        # self.is_LUT=wrapper(lib.is_LUT)
        # #  INT is_Gamma(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParams)
        # self.is_Gamma=wrapper(lib.is_Gamma)
        # #  INT is_Memory(HCAM hf, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
        # self.is_Memory=wrapper(lib.is_Memory)
        # #  INT is_Multicast(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParams)
        # self.is_Multicast=wrapper(lib.is_Multicast)

        ### Obsolete ###
        #  INT is_GetCameraType(HCAM hCam)
        #  INT is_SetHwnd(HCAM hCam, HWND hwnd)
        
        ### Undocumented ###
        #  INT is_Renumerate(HCAM hCam, INT nMode)
        #  INT is_GetNumberOfDevices()

        ### Unused ###
        #  INT is_RenderBitmap(HCAM hCam, INT nMemID, HWND hwnd, INT nMode)
        #  INT is_SetDisplayMode(HCAM hCam, INT Mode)
        #  INT is_SetDisplayPos(HCAM hCam, INT x, INT y)
        #  INT is_GetImageHistogram(HCAM hCam, ctypes.c_int nID, INT ColorMode, ctypes.POINTER(DWORD) pHistoMem)
        #  INT is_DirectRenderer(HCAM hCam, UINT nMode, ctypes.c_void_p pParam, UINT SizeOfParam)
        


    def _prep_arg(self, dtype, value):
        if isinstance(value,dtype):
            return value
        if isinstance(value,(list,tuple)):
            cvalue=(dtype*len(value))()
            for i,v in enumerate(value):
                cvalue[i]=v
            return cvalue
        if issubclass(dtype,ctypes_wrap.CStructWrapper):
            if isinstance(value,dtype._struct):
                return value
            return dtype.prep_struct() if value is None else dtype.prep_struct(**value)
        return dtype() if value is None else dtype(value)
    def _parse_arg(self, dtype, value):
        if issubclass(dtype,ctypes_wrap.CStructWrapper):
            return dtype.tup_struct(value)
        return ctypes_wrap.get_value(value)
    def wrap_parfunc(self, func):
        if func is None:
            return None
        size_arg=func.argnames[-1]
        bare_func=ctypes_wrap.CFunctionWrapper(errcheck=errcheck())(func, args=["hCam","nCommand","param"], rvals=[],
            argprep={"pParam":lambda param: ctypes.pointer(param), size_arg: lambda param: ctypes.sizeof(param)})  # pylint: disable=unnecessary-lambda
        def wrapped_func(hCam, nCommand, dtype, value=None):
            value=self._prep_arg(dtype,value)
            bare_func(hCam,nCommand,value)
            return self._parse_arg(dtype,value)
        return wrapped_func

    def wrap_setget_func(self, func):
        bare_func=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(simple=True))(func)
        res_errcheck=errcheck()
        def wrapped_func(*args, check=False):
            result=bare_func(*args)
            if check:
                res_errcheck(result,func,args)
            return result
        return wrapped_func



    def is_GetCameraList(self):
        ncam=self.is_GetNumberOfCameras()
        if ncam==0:
            return []
        for _ in range(10):
            class UC480_CAMERA_LIST(ctypes.Structure):
                _fields_=[  ("dwCount",ctypes.c_ulong),
                            ("uci",UC480_CAMERA_INFO*ncam)  ]
            cam_lst=UC480_CAMERA_LIST()
            cam_lst.dwCount=ncam
            self.is_GetCameraList_lib(ctypes.pointer(cam_lst))
            if cam_lst.dwCount==ncam:
                return [CUC480_CAMERA_INFO.tup_struct(c) for c in cam_lst.uci]
            else:
                ncam=cam_lst.dwCount
        raise uc480Error("can not obtain the camera list: the list size keeps changing")
    
    def is_GetCaptureStatus(self, hcam):
        status=uc480_defs.UC480_CAPTURE_STATUS_INFO()
        self.is_CaptureStatus(hcam,uc480_defs.CAPTURE_STATUS_CMD.IS_CAPTURE_STATUS_INFO_CMD_GET,ctypes.byref(status),ctypes.sizeof(status))
        return CUC480_CAPTURE_STATUS_INFO.tup_struct(status)
    def is_ResetCaptureStatus(self, hcam):
        self.is_CaptureStatus(hcam,uc480_defs.CAPTURE_STATUS_CMD.IS_CAPTURE_STATUS_INFO_CMD_RESET,None,0)


libs={backend:uc480Lib(backend=backend) for backend in ["uc480","ueye"]}
def get_lib(backend):
    """Get and initialize library with the corresponding backend"""
    if backend in libs:
        lib=libs[backend]
        lib.initlib()
        return lib
    raise ValueError("unrecognized backend '{}'; available backends are {}".format(backend,list(libs)))