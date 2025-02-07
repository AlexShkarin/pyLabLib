# pylint: disable=wrong-spelling-in-comment

from . import NewClassic_USBCamera_SDK_defs  # pylint: disable=unused-import
from .NewClassic_USBCamera_SDK_defs import define_functions
from .base import MightexError

from ...core.utils import ctypes_wrap, ctypes_tools
import ctypes
from ..utils import load_lib
import platform


class MightexLibError(MightexError):
    """Generic Mightex library error"""
    def __init__(self, func, code):
        self.func=func
        self.code=code
        self.msg="function '{}' returned error code {}".format(func,code)
        super().__init__(self.msg)
def errcheck(passing=None):
    """
    Build an error checking function.

    Return a function which checks return codes of Basler library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    if passing is None:
        passing={1}
    def errchecker(result, func, arguments):  # pylint: disable=unused-argument
        if result not in passing:
            raise MightexLibError(func.__name__,result)
        return result
    return errchecker



class NewClassicLib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return
        archfolder="x86" if platform.architecture()[0][:2]=="32" else "x64"
        error_message="The library is supplied with Mightex S-series software package.\n"
        error_message+="It is located in <SoftwareFolder>/DirectShow/{}/MightexNewClassicCameraEngine\n".format(archfolder)
        error_message+="Once you have it, specify its path as pylablib.par['devices/dlls/mightex_sseries']='path/to/dll/'"
        self.lib=load_lib.load_lib("NewClassic_USBCamera_SDK_DS.dll",call_conv="stdcall",depends=["NewClassicUsbLib.dll"],
            locations=("parameter/mightex_sseries","global"),error_message=error_message)

        lib=self.lib
        define_functions(lib)

        nerrwrapper=ctypes_wrap.CFunctionWrapper(default_rvals="pointer")
        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(),default_rvals="pointer")
        strprep=ctypes_wrap.strprep(128)

        #  SDK_RETURN_CODE NewClassicUSB_InitDevice()
        self.NewClassicUSB_InitDevice=nerrwrapper(lib.NewClassicUSB_InitDevice)
        #  SDK_RETURN_CODE NewClassicUSB_UnInitDevice()
        self.NewClassicUSB_UnInitDevice=nerrwrapper(lib.NewClassicUSB_UnInitDevice)
        
        #  SDK_RETURN_CODE NewClassicUSB_GetModuleNoSerialNo(ctypes.c_int DeviceID, ctypes.c_char_p ModuleNo, ctypes.c_char_p SerialNo)
        self.NewClassicUSB_GetModuleNoSerialNo=wrapper(lib.NewClassicUSB_GetModuleNoSerialNo, rvals=["ModuleNo","SerialNo"],
            argprep={"ModuleNo":strprep,"SerialNo":strprep}, byref=[])
        #  SDK_RETURN_CODE NewClassicUSB_AddDeviceToWorkingSet(ctypes.c_int DeviceID)
        self.NewClassicUSB_AddDeviceToWorkingSet=wrapper(lib.NewClassicUSB_AddDeviceToWorkingSet)
        #  SDK_RETURN_CODE NewClassicUSB_RemoveDeviceFromWorkingSet(ctypes.c_int DeviceID)
        self.NewClassicUSB_RemoveDeviceFromWorkingSet=wrapper(lib.NewClassicUSB_RemoveDeviceFromWorkingSet)
        #  SDK_RETURN_CODE NewClassicUSB_ActiveDeviceInWorkingSet(ctypes.c_int DeviceID, ctypes.c_int Active)
        self.NewClassicUSB_ActiveDeviceInWorkingSet=wrapper(lib.NewClassicUSB_ActiveDeviceInWorkingSet)
        #  SDK_RETURN_CODE NewClassicUSB_StartCameraEngine(HWND ParentHandle, ctypes.c_int CameraBitOption)
        self.NewClassicUSB_StartCameraEngine=wrapper(lib.NewClassicUSB_StartCameraEngine)
        #  SDK_RETURN_CODE NewClassicUSB_StopCameraEngine()
        self.NewClassicUSB_StopCameraEngine=wrapper(lib.NewClassicUSB_StopCameraEngine)

        #  SDK_RETURN_CODE NewClassicUSB_SetCameraWorkMode(ctypes.c_int DeviceID, ctypes.c_int WorkMode)
        self.NewClassicUSB_SetCameraWorkMode=wrapper(lib.NewClassicUSB_SetCameraWorkMode)
        #  SDK_RETURN_CODE NewClassicUSB_ShowFactoryControlPanel(ctypes.c_int DeviceID, ctypes.c_char_p passWord)
        self.NewClassicUSB_ShowFactoryControlPanel=wrapper(lib.NewClassicUSB_ShowFactoryControlPanel)
        #  SDK_RETURN_CODE NewClassicUSB_HideFactoryControlPanel()
        self.NewClassicUSB_HideFactoryControlPanel=wrapper(lib.NewClassicUSB_HideFactoryControlPanel)
        #  SDK_RETURN_CODE NewClassicUSB_SetBayerFilterType(ctypes.c_int FilterType)
        self.NewClassicUSB_SetBayerFilterType=wrapper(lib.NewClassicUSB_SetBayerFilterType)
        #  SDK_RETURN_CODE NewClassicUSB_SetResolution(ctypes.c_int deviceID, ctypes.c_int Resolution, ctypes.c_int Bin)
        self.NewClassicUSB_SetResolution=wrapper(lib.NewClassicUSB_SetResolution)
        #  SDK_RETURN_CODE NewClassicUSB_SetCustomizedResolution(ctypes.c_int deviceID, ctypes.c_int RowSize, ctypes.c_int ColSize, ctypes.c_int Bin)
        self.NewClassicUSB_SetCustomizedResolution=wrapper(lib.NewClassicUSB_SetCustomizedResolution)
        #  SDK_RETURN_CODE NewClassicUSB_SetExposureTime(ctypes.c_int DeviceID, ctypes.c_int exposureTime)
        self.NewClassicUSB_SetExposureTime=wrapper(lib.NewClassicUSB_SetExposureTime)
        #  SDK_RETURN_CODE NewClassicUSB_SetXYStart(ctypes.c_int deviceID, ctypes.c_int XStart, ctypes.c_int YStart)
        self.NewClassicUSB_SetXYStart=wrapper(lib.NewClassicUSB_SetXYStart)
        #  SDK_RETURN_CODE NewClassicUSB_SetGains(ctypes.c_int deviceID, ctypes.c_int RedGain, ctypes.c_int GreenGain, ctypes.c_int BlueGain)
        self.NewClassicUSB_SetGains=wrapper(lib.NewClassicUSB_SetGains)
        #  SDK_RETURN_CODE NewClassicUSB_SetGamma(ctypes.c_int Gamma, ctypes.c_int Contrast, ctypes.c_int Bright, ctypes.c_int Sharp)
        self.NewClassicUSB_SetGamma=wrapper(lib.NewClassicUSB_SetGamma)
        #  SDK_RETURN_CODE NewClassicUSB_SetBWMode(ctypes.c_int BWMode, ctypes.c_int H_Mirror, ctypes.c_int V_Flip)
        self.NewClassicUSB_SetBWMode=wrapper(lib.NewClassicUSB_SetBWMode)
        #  SDK_RETURN_CODE NewClassicUSB_SetMinimumFrameDelay(ctypes.c_int IsMinimumFrameDelay)
        self.NewClassicUSB_SetMinimumFrameDelay=wrapper(lib.NewClassicUSB_SetMinimumFrameDelay)
        #  SDK_RETURN_CODE NewClassicUSB_SoftTrigger(ctypes.c_int DeviceID)
        self.NewClassicUSB_SoftTrigger=wrapper(lib.NewClassicUSB_SoftTrigger)
        #  SDK_RETURN_CODE NewClassicUSB_SetSensorFrequency(ctypes.c_int DeviceID, ctypes.c_int Frequency)
        self.NewClassicUSB_SetSensorFrequency=wrapper(lib.NewClassicUSB_SetSensorFrequency)
        #  SDK_RETURN_CODE NewClassicUSB_SetHBlankingExtension(ctypes.c_int DeviceID, ctypes.c_int HBlanking)
        self.NewClassicUSB_SetHBlankingExtension=wrapper(lib.NewClassicUSB_SetHBlankingExtension)

        #  SDK_RETURN_CODE NewClassicUSB_StartFrameGrab(ctypes.c_int TotalFrames)
        self.NewClassicUSB_StartFrameGrab=wrapper(lib.NewClassicUSB_StartFrameGrab)
        #  SDK_RETURN_CODE NewClassicUSB_StopFrameGrab()
        self.NewClassicUSB_StopFrameGrab=wrapper(lib.NewClassicUSB_StopFrameGrab)

        self.frame_callback=ctypes_tools.WINFUNCTYPE(None,NewClassic_USBCamera_SDK_defs.PTProcessedDataProperty,ctypes.c_char_p)
        #  SDK_RETURN_CODE NewClassicUSB_InstallFrameHooker(ctypes.c_int FrameType, FrameDataCallBack FrameHooker)
        self.NewClassicUSB_InstallFrameHooker=wrapper(lib.NewClassicUSB_InstallFrameHooker)
        #  SDK_RETURN_CODE NewClassicUSB_InstallUSBDeviceHooker(DeviceFaultCallBack USBDeviceHooker)
        self.NewClassicUSB_InstallUSBDeviceHooker=wrapper(lib.NewClassicUSB_InstallUSBDeviceHooker)
        #  ctypes.POINTER(ctypes.c_ubyte) NewClassicUSB_GetCurrentFrame(ctypes.c_int FrameType, ctypes.c_int deviceID, ctypes.POINTER(BYTE) FramePtr)

        self.NewClassicUSB_GetCurrentFrame=wrapper(lib.NewClassicUSB_GetCurrentFrame)
        #  SDK_RETURN_CODE NewClassicUSB_GetDevicesErrorState()
        self.NewClassicUSB_GetDevicesErrorState=wrapper(lib.NewClassicUSB_GetDevicesErrorState)
        #  SDK_RETURN_CODE NewClassicUSB_SetGPIOConfig(ctypes.c_int DeviceID, ctypes.c_ubyte ConfigByte)
        self.NewClassicUSB_SetGPIOConfig=wrapper(lib.NewClassicUSB_SetGPIOConfig)
        #  SDK_RETURN_CODE NewClassicUSB_SetGPIOInOut(ctypes.c_int DeviceID, ctypes.c_ubyte OutputByte, ctypes.POINTER(ctypes.c_ubyte) InputBytePtr)
        self.NewClassicUSB_SetGPIOInOut=wrapper(lib.NewClassicUSB_SetGPIOInOut)

        
    def register_frame_callback(self, callback, frame_type=0, wrap=True):
        if wrap:
            def wrapped_callback(*args):
                try:
                    callback(*args)
                except: # pylint: disable=bare-except
                    pass
            cb=self.frame_callback(wrapped_callback)
        else:
            cb=self.frame_callback(callback)
        self.NewClassicUSB_InstallFrameHooker(frame_type,cb)
        return cb

wlib=NewClassicLib()