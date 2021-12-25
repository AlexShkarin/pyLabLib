# pylint: disable=wrong-spelling-in-comment

from ...core.utils import ctypes_wrap
from .SCU3DControl_defs import Error, drError
from .SCU3DControl_defs import EConfiguration  # pylint: disable=unused-import
from .SCU3DControl_defs import define_functions

from ...core.devio.comm_backend import DeviceError
from ..utils import load_lib

import ctypes



class SmarActError(DeviceError):
    """Generic SmarAct error"""
class SCU3DControlLibError(SmarActError):
    """Generic Arcus Performax library error"""
    def __init__(self, func, arguments, code):
        self.func=func
        self.arguments=arguments
        self.code=code
        self.name=drError.get(code,"UNKNOWN")
        self.msg="function '{}' return an error {}({})".format(func,self.code,self.name)
        SmarActError.__init__(self,self.msg)
def errchecker(result, func, arguments):
    if result!=Error.SA_OK:
        raise SCU3DControlLibError(func.__name__,arguments,result)
    return result


class SCU3DControlLib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return
        error_message="The library is supplied together with the controller\n"+load_lib.par_error_message.format("smaract_scu3d")
        self.lib=load_lib.load_lib("SCU3DControl.dll",locations=("parameter/smaract_scu3d","global"),error_message=error_message,call_conv="cdecl")
        lib=self.lib
        define_functions(lib)

        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errchecker,default_rvals="pointer",pointer_byref=True)
        
        #  SA_STATUS SA_GetDLLVersion(ctypes.POINTER(ctypes.c_uint) version)
        self.SA_GetDLLVersion=wrapper(lib.SA_GetDLLVersion)
        #  SA_STATUS SA_GetAvailableDevices(ctypes.POINTER(ctypes.c_uint) idList, ctypes.POINTER(ctypes.c_uint) idListSize)
        self.SA_GetAvailableDevices_lib=wrapper(lib.SA_GetAvailableDevices,args="all",rvals=["idListSize"])
        #  SA_STATUS SA_AddDeviceToInitDevicesList(ctypes.c_uint deviceId)
        self.SA_AddDeviceToInitDevicesList=wrapper(lib.SA_AddDeviceToInitDevicesList)
        #  SA_STATUS SA_ClearInitDevicesList()
        self.SA_ClearInitDevicesList=wrapper(lib.SA_ClearInitDevicesList)
        #  SA_STATUS SA_InitDevices(ctypes.c_uint configuration)
        self.SA_InitDevices=wrapper(lib.SA_InitDevices)
        #  SA_STATUS SA_ReleaseDevices()
        self.SA_ReleaseDevices=wrapper(lib.SA_ReleaseDevices)
        #  SA_STATUS SA_GetNumberOfDevices(ctypes.POINTER(ctypes.c_uint) number)
        self.SA_GetNumberOfDevices=wrapper(lib.SA_GetNumberOfDevices)

        #  SA_STATUS SA_GetDeviceID(SA_INDEX deviceIndex, ctypes.POINTER(ctypes.c_uint) deviceId)
        self.SA_GetDeviceID=wrapper(lib.SA_GetDeviceID)
        #  SA_STATUS SA_GetDeviceFirmwareVersion(SA_INDEX deviceIndex, ctypes.POINTER(ctypes.c_uint) version)
        self.SA_GetDeviceFirmwareVersion=wrapper(lib.SA_GetDeviceFirmwareVersion)
        #  SA_STATUS SA_SetClosedLoopMaxFrequency_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint frequency)
        self.SA_SetClosedLoopMaxFrequency_S=wrapper(lib.SA_SetClosedLoopMaxFrequency_S)
        #  SA_STATUS SA_GetClosedLoopMaxFrequency_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) frequency)
        self.SA_GetClosedLoopMaxFrequency_S=wrapper(lib.SA_GetClosedLoopMaxFrequency_S)
        #  SA_STATUS SA_SetZero_S(SA_INDEX deviceIndex, SA_INDEX channelIndex)
        self.SA_SetZero_S=wrapper(lib.SA_SetZero_S)
        #  SA_STATUS SA_GetSensorPresent_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) present)
        self.SA_GetSensorPresent_S=wrapper(lib.SA_GetSensorPresent_S)
        #  SA_STATUS SA_SetSensorType_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint type)
        self.SA_SetSensorType_S=wrapper(lib.SA_SetSensorType_S)
        #  SA_STATUS SA_GetSensorType_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) type)
        self.SA_GetSensorType_S=wrapper(lib.SA_GetSensorType_S)
        #  SA_STATUS SA_SetPositionerAlignment_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint alignment, ctypes.c_uint forwardAmplitude, ctypes.c_uint backwardAmplitude)
        self.SA_SetPositionerAlignment_S=wrapper(lib.SA_SetPositionerAlignment_S)
        #  SA_STATUS SA_GetPositionerAlignment_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) alignment, ctypes.POINTER(ctypes.c_uint) forwardAmplitude, ctypes.POINTER(ctypes.c_uint) backwardAmplitude)
        self.SA_GetPositionerAlignment_S=wrapper(lib.SA_GetPositionerAlignment_S)
        #  SA_STATUS SA_SetSafeDirection_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint direction)
        self.SA_SetSafeDirection_S=wrapper(lib.SA_SetSafeDirection_S)
        #  SA_STATUS SA_GetSafeDirection_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) direction)
        self.SA_GetSafeDirection_S=wrapper(lib.SA_GetSafeDirection_S)
        #  SA_STATUS SA_SetScale_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int reserved, ctypes.c_uint inverted)
        self.SA_SetScale_S=wrapper(lib.SA_SetScale_S)
        #  SA_STATUS SA_GetScale_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_int) reserved, ctypes.POINTER(ctypes.c_uint) inverted)
        self.SA_GetScale_S=wrapper(lib.SA_GetScale_S)
        #  SA_STATUS SA_MoveStep_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int steps, ctypes.c_uint amplitude, ctypes.c_uint frequency)
        self.SA_MoveStep_S=wrapper(lib.SA_MoveStep_S)
        #  SA_STATUS SA_SetAmplitude_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint amplitude)
        self.SA_SetAmplitude_S=wrapper(lib.SA_SetAmplitude_S)
        #  SA_STATUS SA_MovePositionAbsolute_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int position, ctypes.c_uint holdTime)
        self.SA_MovePositionAbsolute_S=wrapper(lib.SA_MovePositionAbsolute_S)
        #  SA_STATUS SA_MovePositionRelative_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int diff, ctypes.c_uint holdTime)
        self.SA_MovePositionRelative_S=wrapper(lib.SA_MovePositionRelative_S)
        #  SA_STATUS SA_MoveAngleAbsolute_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int angle, ctypes.c_int revolution, ctypes.c_uint holdTime)
        self.SA_MoveAngleAbsolute_S=wrapper(lib.SA_MoveAngleAbsolute_S)
        #  SA_STATUS SA_MoveAngleRelative_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int angleDiff, ctypes.c_int revolutionDiff, ctypes.c_uint holdTime)
        self.SA_MoveAngleRelative_S=wrapper(lib.SA_MoveAngleRelative_S)
        #  SA_STATUS SA_CalibrateSensor_S(SA_INDEX deviceIndex, SA_INDEX channelIndex)
        self.SA_CalibrateSensor_S=wrapper(lib.SA_CalibrateSensor_S)
        #  SA_STATUS SA_MoveToReference_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint holdTime, ctypes.c_uint autoZero)
        self.SA_MoveToReference_S=wrapper(lib.SA_MoveToReference_S)
        #  SA_STATUS SA_MoveToEndStop_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint direction, ctypes.c_uint holdTime, ctypes.c_uint autoZero)
        self.SA_MoveToEndStop_S=wrapper(lib.SA_MoveToEndStop_S)
        #  SA_STATUS SA_Stop_S(SA_INDEX deviceIndex, SA_INDEX channelIndex)
        self.SA_Stop_S=wrapper(lib.SA_Stop_S)
        #  SA_STATUS SA_GetStatus_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) status)
        self.SA_GetStatus_S=wrapper(lib.SA_GetStatus_S)
        #  SA_STATUS SA_GetAmplitude_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) amplitude)
        self.SA_GetAmplitude_S=wrapper(lib.SA_GetAmplitude_S)
        #  SA_STATUS SA_GetPosition_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_int) position)
        self.SA_GetPosition_S=wrapper(lib.SA_GetPosition_S)
        #  SA_STATUS SA_GetAngle_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_int) angle, ctypes.POINTER(ctypes.c_int) revolution)
        self.SA_GetAngle_S=wrapper(lib.SA_GetAngle_S)
        #  SA_STATUS SA_GetPhysicalPositionKnown_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) known)
        self.SA_GetPhysicalPositionKnown_S=wrapper(lib.SA_GetPhysicalPositionKnown_S)
        
        self._initialized=True

    def SA_GetAvailableDevices(self):
        nmax=256
        devids=(ctypes.c_uint*nmax)()
        ndev=self.SA_GetAvailableDevices_lib(devids,nmax)
        return devids[:ndev]



wlib=SCU3DControlLib()