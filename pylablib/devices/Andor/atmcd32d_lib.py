# pylint: disable=spelling

from . import atmcd32d_defs
from .atmcd32d_defs import DRV_STATUS, drDRV_STATUS
from .atmcd32d_defs import define_functions
from .atmcd32d_defs import AT_STEPMODE, AT_GATEMODE  # pylint: disable=unused-import
from .atmcd32d_defs import AC_ACQMODE, AC_READMODE, AC_TRIGGERMODE, AC_EMGAIN, AC_FEATURES  # pylint: disable=unused-import
from .atmcd32d_defs import AC_CAMERATYPE, drAC_CAMERATYPE, AC_PIXELMODE  # pylint: disable=unused-import
from .atmcd32d_defs import AC_SETFUNC, AC_GETFUNC  # pylint: disable=unused-import
from .base import AndorError

from ...core.utils import ctypes_wrap, py3
from ..utils import load_lib

import numpy as np
import platform
import ctypes
import collections



class AndorSDK2LibError(AndorError):
    """Generic Andor SDK2 library error"""
    def __init__(self, func, code):
        self.func=func
        self.code=code
        self.name=drDRV_STATUS.get(self.code,"UNKNOWN")
        msg="function '{}' raised error {}({})".format(func,code,self.name)
        AndorError.__init__(self,msg)
def errcheck(passing=None):
    """
    Build an error checking function.

    Return a function which checks return codes of Andor SDK3 library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    passing=set(passing) if passing is not None else set()
    passing.add(DRV_STATUS.DRV_SUCCESS) # always allow success
    def errchecker(result, func, arguments):  # pylint: disable=unused-argument
        if result not in passing:
            raise AndorSDK2LibError(func.__name__,result)
        return result
    return errchecker

class CAndorCapabilities(atmcd32d_defs.CAndorCapabilities):
    def prep(self, struct):
        struct.ulSize=ctypes.sizeof(struct)
        return struct

TAmpModeSimple=collections.namedtuple("TAmpModeSimple",["channel","oamp","hsspeed","preamp"])
TAmpModeFull=collections.namedtuple("TAmpModeFull",["channel","channel_bitdepth","oamp","oamp_kind","hsspeed","hsspeed_MHz","preamp","preamp_gain"])
class AndorSDK2Lib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return

        solis_path=load_lib.get_program_files_folder("Andor SOLIS")
        sdk2_path=load_lib.get_program_files_folder("Andor SDK")
        archbit=platform.architecture()[0][:2]
        error_message="The library is automatically supplied with Andor Solis software or Andor SDK2 software\n"+load_lib.par_error_message.format("andor_sdk2")
        lib_names=["atmcd{}d_legacy.dll".format(archbit),"atmcd{}d.dll".format(archbit)]
        self.lib=load_lib.load_lib(lib_names,locations=("parameter/andor_sdk2",solis_path,sdk2_path,"global"),error_message=error_message,call_conv="stdcall")
        lib=self.lib
        define_functions(lib)

        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(),default_rvals="pointer")
        default_strlen=256
        strprep=ctypes_wrap.strprep(default_strlen)

        #  ctypes.c_uint Initialize(ctypes.c_char_p dir)
        self.Initialize=wrapper(lib.Initialize)
        #  ctypes.c_uint ShutDown()
        self.ShutDown=wrapper(lib.ShutDown)
        #  ctypes.c_uint GetAvailableCameras(ctypes.POINTER(ctypes.c_long) totalCameras)
        self.GetAvailableCameras=wrapper(lib.GetAvailableCameras)
        #  ctypes.c_uint GetCameraHandle(ctypes.c_long cameraIndex, ctypes.POINTER(ctypes.c_long) cameraHandle)
        self.GetCameraHandle=wrapper(lib.GetCameraHandle)
        #  ctypes.c_uint GetCurrentCamera(ctypes.POINTER(ctypes.c_long) cameraHandle)
        self.GetCurrentCamera=wrapper(lib.GetCurrentCamera)
        #  ctypes.c_uint SetCurrentCamera(ctypes.c_long cameraHandle)
        self.SetCurrentCamera=wrapper(lib.SetCurrentCamera)

        # #  ctypes.c_uint GetCapabilities(ctypes.POINTER(AndorCapabilities) caps)
        self.GetCapabilities=wrapper(lib.GetCapabilities, rvals=["caps"],
            argprep={"caps":CAndorCapabilities.prep_struct}, rconv={"caps":CAndorCapabilities.tup_struct})
        # #  ctypes.c_uint GetControllerCardModel(ctypes.c_char_p controllerCardModel)
        self.GetControllerCardModel=wrapper(lib.GetControllerCardModel, rvals=["controllerCardModel"],
            argprep={"controllerCardModel":strprep}, byref=[])
        # #  ctypes.c_uint GetHeadModel(ctypes.c_char_p name)
        self.GetHeadModel=wrapper(lib.GetHeadModel, rvals=["name"],
            argprep={"name":strprep}, byref=[])
        #  ctypes.c_uint GetHardwareVersion(ctypes.POINTER(ctypes.c_uint) PCB, ctypes.POINTER(ctypes.c_uint) Decode, ctypes.POINTER(ctypes.c_uint) dummy1, ctypes.POINTER(ctypes.c_uint) dummy2, ctypes.POINTER(ctypes.c_uint) CameraFirmwareVersion, ctypes.POINTER(ctypes.c_uint) CameraFirmwareBuild)
        self.GetHardwareVersion=wrapper(lib.GetHardwareVersion)
        #  ctypes.c_uint GetSoftwareVersion(ctypes.POINTER(ctypes.c_uint) eprom, ctypes.POINTER(ctypes.c_uint) coffile, ctypes.POINTER(ctypes.c_uint) vxdrev, ctypes.POINTER(ctypes.c_uint) vxdver, ctypes.POINTER(ctypes.c_uint) dllrev, ctypes.POINTER(ctypes.c_uint) dllver)
        self.GetSoftwareVersion=wrapper(lib.GetSoftwareVersion)
        #  ctypes.c_uint GetVersionInfo(ctypes.c_int arr, ctypes.c_char_p szVersionInfo, ctypes.c_ulong ui32BufferLen)
        self.GetCameraSerialNumber=wrapper(lib.GetCameraSerialNumber) # only iDus, set index=0
        # #  ctypes.c_uint GetPixelSize(ctypes.POINTER(ctypes.c_float) xSize, ctypes.POINTER(ctypes.c_float) ySize)
        self.GetPixelSize=wrapper(lib.GetPixelSize)
        #  ctypes.c_uint GetQE(ctypes.c_char_p sensor, ctypes.c_float wavelength, ctypes.c_uint mode, ctypes.POINTER(ctypes.c_float) QE)
        self.GetQE=wrapper(lib.GetQE)

        #  ctypes.c_uint InAuxPort(ctypes.c_int port, ctypes.POINTER(ctypes.c_int) state)
        self.InAuxPort=wrapper(lib.InAuxPort)
        #  ctypes.c_uint OutAuxPort(ctypes.c_int port, ctypes.c_int state)
        self.OutAuxPort=wrapper(lib.OutAuxPort)
        #  ctypes.c_uint GetNumberIO(ctypes.POINTER(ctypes.c_int) iNumber)
        self.GetNumberIO=wrapper(lib.GetNumberIO)
        #  ctypes.c_uint GetIODirection(ctypes.c_int index, ctypes.POINTER(ctypes.c_int) iDirection)
        self.GetIODirection=wrapper(lib.GetIODirection)
        #  ctypes.c_uint GetIOLevel(ctypes.c_int index, ctypes.POINTER(ctypes.c_int) iLevel)
        self.SetIODirection=wrapper(lib.SetIODirection)
        #  ctypes.c_uint SetIOLevel(ctypes.c_int index, ctypes.c_int iLevel)
        self.GetIOLevel=wrapper(lib.GetIOLevel)
        #  ctypes.c_uint SetIODirection(ctypes.c_int index, ctypes.c_int iDirection)
        self.SetIOLevel=wrapper(lib.SetIOLevel)
        #  ctypes.c_uint SetDACOutput(ctypes.c_int iOption, ctypes.c_int iResolution, ctypes.c_int iValue)
        self.SetDACOutput=wrapper(lib.SetDACOutput)
        #  ctypes.c_uint SetDACOutputScale(ctypes.c_int iScale)
        self.SetDACOutputScale=wrapper(lib.SetDACOutputScale)

        #  ctypes.c_uint GPIBReceive(ctypes.c_int id, ctypes.c_short address, ctypes.c_char_p text, ctypes.c_int size)
        self.GPIBReceive=wrapper(lib.GPIBReceive, rvals=["text"],
            argprep={"text": lambda size: strprep(size)()}, byref=[])
        #  ctypes.c_uint GPIBSend(ctypes.c_int id, ctypes.c_short address, ctypes.c_char_p text)
        self.GPIBSend=wrapper(lib.GPIBSend)
        #  ctypes.c_uint SetDelayGenerator(ctypes.c_int board, ctypes.c_short address, ctypes.c_int typ)
        self.SetDelayGenerator=wrapper(lib.SetDelayGenerator)
        # #  ctypes.c_uint I2CBurstRead(BYTE i2cAddress, ctypes.c_long nBytes, ctypes.POINTER(BYTE) data)
        # lib.I2CBurstRead.restype=ctypes.c_uint
        # lib.I2CBurstRead.argtypes=[BYTE, ctypes.c_long, ctypes.POINTER(BYTE)]
        # lib.I2CBurstRead.argnames=["i2cAddress", "nBytes", "data"]
        # #  ctypes.c_uint I2CBurstWrite(BYTE i2cAddress, ctypes.c_long nBytes, ctypes.POINTER(BYTE) data)
        # lib.I2CBurstWrite.restype=ctypes.c_uint
        # lib.I2CBurstWrite.argtypes=[BYTE, ctypes.c_long, ctypes.POINTER(BYTE)]
        # lib.I2CBurstWrite.argnames=["i2cAddress", "nBytes", "data"]
        # #  ctypes.c_uint I2CRead(BYTE deviceID, BYTE intAddress, ctypes.POINTER(BYTE) pdata)
        # lib.I2CRead.restype=ctypes.c_uint
        # lib.I2CRead.argtypes=[BYTE, BYTE, ctypes.POINTER(BYTE)]
        # lib.I2CRead.argnames=["deviceID", "intAddress", "pdata"]
        # #  ctypes.c_uint I2CReset()
        # lib.I2CReset.restype=ctypes.c_uint
        # lib.I2CReset.argtypes=[]
        # lib.I2CReset.argnames=[]
        # #  ctypes.c_uint I2CWrite(BYTE deviceID, BYTE intAddress, BYTE data)
        # lib.I2CWrite.restype=ctypes.c_uint
        # lib.I2CWrite.argtypes=[BYTE, BYTE, BYTE]
        # lib.I2CWrite.argnames=["deviceID", "intAddress", "data"]

        #  ctypes.c_uint SetTriggerMode(ctypes.c_int mode)
        self.SetTriggerMode=wrapper(lib.SetTriggerMode)
        #  ctypes.c_uint GetExternalTriggerTermination(ctypes.POINTER(ctypes.c_ulong) puiTermination)
        self.GetExternalTriggerTermination=wrapper(lib.GetExternalTriggerTermination)
        #  ctypes.c_uint SetExternalTriggerTermination(ctypes.c_ulong uiTermination)
        self.SetExternalTriggerTermination=wrapper(lib.SetExternalTriggerTermination)
        #  ctypes.c_uint GetTriggerLevelRange(ctypes.POINTER(ctypes.c_float) minimum, ctypes.POINTER(ctypes.c_float) maximum)
        self.GetTriggerLevelRange=wrapper(lib.GetTriggerLevelRange)
        #  ctypes.c_uint SetTriggerLevel(ctypes.c_float f_level)
        self.SetTriggerLevel=wrapper(lib.SetTriggerLevel)
        #  ctypes.c_uint SetTriggerInvert(ctypes.c_int mode)
        self.SetTriggerInvert=wrapper(lib.SetTriggerInvert)
        #  ctypes.c_uint IsTriggerModeAvailable(ctypes.c_int iTriggerMode)
        self.IsTriggerModeAvailable=wrapper(lib.IsTriggerModeAvailable)
        #  ctypes.c_uint SendSoftwareTrigger()
        self.SendSoftwareTrigger=wrapper(lib.SendSoftwareTrigger)
        #  ctypes.c_uint SetAdvancedTriggerModeState(ctypes.c_int iState)
        self.SetAdvancedTriggerModeState=wrapper(lib.SetAdvancedTriggerModeState)
        #  ctypes.c_uint SetFastExtTrigger(ctypes.c_int mode)
        self.SetFastExtTrigger=wrapper(lib.SetFastExtTrigger)
        #  ctypes.c_uint SetChargeShifting(ctypes.c_uint NumberRows, ctypes.c_uint NumberRepeats)
        self.SetChargeShifting=wrapper(lib.SetChargeShifting)

        errcheck_temp=errcheck(passing={20034,20035,20036,20037,20040})
        #  ctypes.c_uint GetTemperature(ctypes.POINTER(ctypes.c_int) temperature)
        self.GetTemperature=wrapper(lib.GetTemperature, rvals=[None,"temperature"], errcheck=errcheck_temp)
        #  ctypes.c_uint GetTemperatureF(ctypes.POINTER(ctypes.c_float) temperature)
        self.GetTemperatureF=wrapper(lib.GetTemperatureF, rvals=[None,"temperature"], errcheck=errcheck_temp)
        #  ctypes.c_uint SetTemperature(ctypes.c_int temperature)
        self.SetTemperature=wrapper(lib.SetTemperature)
        #  ctypes.c_uint GetTemperatureRange(ctypes.POINTER(ctypes.c_int) mintemp, ctypes.POINTER(ctypes.c_int) maxtemp)
        self.GetTemperatureRange=wrapper(lib.GetTemperatureRange)
        #  ctypes.c_uint CoolerON()
        self.CoolerON=wrapper(lib.CoolerON)
        #  ctypes.c_uint CoolerOFF()
        self.CoolerOFF=wrapper(lib.CoolerOFF)
        #  ctypes.c_uint IsCoolerOn(ctypes.POINTER(ctypes.c_int) iCoolerStatus)
        self.IsCoolerOn=wrapper(lib.IsCoolerOn)
        #  ctypes.c_uint SetCoolerMode(ctypes.c_int mode)
        self.SetCoolerMode=wrapper(lib.SetCoolerMode)
        #  ctypes.c_uint SetFanMode(ctypes.c_int mode)
        self.SetFanMode=wrapper(lib.SetFanMode)
        #  ctypes.c_uint GetTECStatus(ctypes.POINTER(ctypes.c_int) piFlag)
        self.GetTECStatus=wrapper(lib.GetTECStatus)

        #  ctypes.c_uint GetNumberADChannels(ctypes.POINTER(ctypes.c_int) channels)
        self.GetNumberADChannels=wrapper(lib.GetNumberADChannels)
        #  ctypes.c_uint SetADChannel(ctypes.c_int channel)
        self.SetADChannel=wrapper(lib.SetADChannel)
        #  ctypes.c_uint GetBitDepth(ctypes.c_int channel, ctypes.POINTER(ctypes.c_int) depth)
        self.GetBitDepth=wrapper(lib.GetBitDepth)
        #  ctypes.c_uint GetNumberAmp(ctypes.POINTER(ctypes.c_int) amp)
        self.GetNumberAmp=wrapper(lib.GetNumberAmp)
        #  ctypes.c_uint SetOutputAmplifier(ctypes.c_int typ)
        self.SetOutputAmplifier=wrapper(lib.SetOutputAmplifier)
        #  ctypes.c_uint IsAmplifierAvailable(ctypes.c_int iamp)
        self.IsAmplifierAvailable=wrapper(lib.IsAmplifierAvailable)
        #  ctypes.c_uint GetNumberPreAmpGains(ctypes.POINTER(ctypes.c_int) noGains)
        self.GetNumberPreAmpGains=wrapper(lib.GetNumberPreAmpGains)
        #  ctypes.c_uint GetPreAmpGain(ctypes.c_int index, ctypes.POINTER(ctypes.c_float) gain)
        self.GetPreAmpGain=wrapper(lib.GetPreAmpGain)
        #  ctypes.c_uint SetPreAmpGain(ctypes.c_int index)
        self.SetPreAmpGain=wrapper(lib.SetPreAmpGain)
        #  ctypes.c_uint IsPreAmpGainAvailable(ctypes.c_int channel, ctypes.c_int amplifier, ctypes.c_int index, ctypes.c_int pa, ctypes.POINTER(ctypes.c_int) status)
        self.IsPreAmpGainAvailable=wrapper(lib.IsPreAmpGainAvailable)
        #  ctypes.c_uint GetPreAmpGainText(ctypes.c_int index, ctypes.c_char_p name, ctypes.c_int length)
        self.GetPreAmpGainText=wrapper(lib.GetPreAmpGainText, args=["index"], rvals=["name"],
            argprep={"name":strprep,"length":default_strlen}, byref=[])
        #  ctypes.c_uint GetAmpDesc(ctypes.c_int index, ctypes.c_char_p name, ctypes.c_int length)
        self.GetAmpDesc=wrapper(lib.GetAmpDesc, args=["index"], rvals=["name"],
            argprep={"name":strprep,"length":default_strlen}, byref=[])
        #  ctypes.c_uint GetAmpMaxSpeed(ctypes.c_int index, ctypes.POINTER(ctypes.c_float) speed)
        self.GetAmpMaxSpeed=wrapper(lib.GetAmpMaxSpeed)
        #  ctypes.c_uint GetSensitivity(ctypes.c_int channel, ctypes.c_int horzShift, ctypes.c_int amplifier, ctypes.c_int pa, ctypes.POINTER(ctypes.c_float) sensitivity)
        self.GetSensitivity=wrapper(lib.GetSensitivity)

        #  ctypes.c_uint GetNumberHSSpeeds(ctypes.c_int channel, ctypes.c_int typ, ctypes.POINTER(ctypes.c_int) speeds)
        self.GetNumberHSSpeeds=wrapper(lib.GetNumberHSSpeeds)
        #  ctypes.c_uint GetHSSpeed(ctypes.c_int channel, ctypes.c_int typ, ctypes.c_int index, ctypes.POINTER(ctypes.c_float) speed)
        self.GetHSSpeed=wrapper(lib.GetHSSpeed)
        #  ctypes.c_uint SetHSSpeed(ctypes.c_int typ, ctypes.c_int index)
        self.SetHSSpeed=wrapper(lib.SetHSSpeed)
        #  ctypes.c_uint GetNumberVSSpeeds(ctypes.POINTER(ctypes.c_int) speeds)
        self.GetNumberVSSpeeds=wrapper(lib.GetNumberVSSpeeds)
        #  ctypes.c_uint GetVSSpeed(ctypes.c_int index, ctypes.POINTER(ctypes.c_float) speed)
        self.GetVSSpeed=wrapper(lib.GetVSSpeed)
        #  ctypes.c_uint SetVSSpeed(ctypes.c_int index)
        self.SetVSSpeed=wrapper(lib.SetVSSpeed)
        #  ctypes.c_uint GetFastestRecommendedVSSpeed(ctypes.POINTER(ctypes.c_int) index, ctypes.POINTER(ctypes.c_float) speed)
        self.GetFastestRecommendedVSSpeed=wrapper(lib.GetFastestRecommendedVSSpeed)
        #  ctypes.c_uint GetNumberVSAmplitudes(ctypes.POINTER(ctypes.c_int) number)
        self.GetNumberVSAmplitudes=wrapper(lib.GetNumberVSAmplitudes)
        #  ctypes.c_uint GetVSAmplitudeValue(ctypes.c_int index, ctypes.POINTER(ctypes.c_int) value)
        self.GetVSAmplitudeValue=wrapper(lib.GetVSAmplitudeValue)
        #  ctypes.c_uint SetVSAmplitude(ctypes.c_int index)
        self.SetVSAmplitude=wrapper(lib.SetVSAmplitude)
        #  ctypes.c_uint GetVSAmplitudeString(ctypes.c_int index, ctypes.c_char_p text)
        self.GetVSAmplitudeString=wrapper(lib.GetVSAmplitudeString, rvals=["text"],
            argprep={"text":strprep}, byref=[])
        #  ctypes.c_uint GetVSAmplitudeFromString(ctypes.c_char_p text, ctypes.POINTER(ctypes.c_int) index)
        self.GetVSAmplitudeFromString=wrapper(lib.GetVSAmplitudeFromString)
        #  ctypes.c_uint SetHighCapacity(ctypes.c_int state)
        self.SetHighCapacity=wrapper(lib.SetHighCapacity)

        #  ctypes.c_uint SetEMGainMode(ctypes.c_int mode)
        self.SetEMGainMode=wrapper(lib.SetEMGainMode)
        #  ctypes.c_uint GetEMGainRange(ctypes.POINTER(ctypes.c_int) low, ctypes.POINTER(ctypes.c_int) high)
        self.GetEMGainRange=wrapper(lib.GetEMGainRange)
        #  ctypes.c_uint GetEMCCDGain(ctypes.POINTER(ctypes.c_int) gain)
        self.GetEMCCDGain=wrapper(lib.GetEMCCDGain)
        #  ctypes.c_uint SetEMCCDGain(ctypes.c_int gain)
        self.SetEMCCDGain=wrapper(lib.SetEMCCDGain)
        #  ctypes.c_uint GetEMAdvanced(ctypes.POINTER(ctypes.c_int) state)
        self.GetEMAdvanced=wrapper(lib.GetEMAdvanced)
        #  ctypes.c_uint SetEMAdvanced(ctypes.c_int state)
        self.SetEMAdvanced=wrapper(lib.SetEMAdvanced)

        #  ctypes.c_uint GetShutterMinTimes(ctypes.POINTER(ctypes.c_int) minclosingtime, ctypes.POINTER(ctypes.c_int) minopeningtime)
        self.GetShutterMinTimes=wrapper(lib.GetShutterMinTimes)
        #  ctypes.c_uint SetShutter(ctypes.c_int typ, ctypes.c_int mode, ctypes.c_int closingtime, ctypes.c_int openingtime)
        self.SetShutter=wrapper(lib.SetShutter)
        #  ctypes.c_uint SetShutterEx(ctypes.c_int typ, ctypes.c_int mode, ctypes.c_int closingtime, ctypes.c_int openingtime, ctypes.c_int extmode)
        self.SetShutterEx=wrapper(lib.SetShutterEx)
        #  ctypes.c_uint IsInternalMechanicalShutter(ctypes.POINTER(ctypes.c_int) InternalShutter)
        self.IsInternalMechanicalShutter=wrapper(lib.IsInternalMechanicalShutter)

        #  ctypes.c_uint GetCountConvertWavelengthRange(ctypes.POINTER(ctypes.c_float) minval, ctypes.POINTER(ctypes.c_float) maxval)
        self.GetCountConvertWavelengthRange=wrapper(lib.GetCountConvertWavelengthRange)
        #  ctypes.c_uint IsCountConvertModeAvailable(ctypes.c_int mode)
        self.IsCountConvertModeAvailable=wrapper(lib.IsCountConvertModeAvailable)
        #  ctypes.c_uint SetCountConvertMode(ctypes.c_int Mode)
        self.SetCountConvertMode=wrapper(lib.SetCountConvertMode)
        #  ctypes.c_uint SetCountConvertWavelength(ctypes.c_float wavelength)
        self.SetCountConvertWavelength=wrapper(lib.SetCountConvertWavelength)

        #  ctypes.c_uint SetPhotonCounting(ctypes.c_int state)
        self.SetPhotonCounting=wrapper(lib.SetPhotonCounting)
        #  ctypes.c_uint SetPhotonCountingThreshold(ctypes.c_long min, ctypes.c_long max)
        self.SetPhotonCountingThreshold=wrapper(lib.SetPhotonCountingThreshold)
        #  ctypes.c_uint GetNumberPhotonCountingDivisions(ctypes.POINTER(ctypes.c_ulong) noOfDivisions)
        self.GetNumberPhotonCountingDivisions=wrapper(lib.GetNumberPhotonCountingDivisions)
        #  ctypes.c_uint SetPhotonCountingDivisions(ctypes.c_ulong noOfDivisions, ctypes.POINTER(ctypes.c_long) divisions)
        self.SetPhotonCountingDivisions=wrapper(lib.SetPhotonCountingDivisions, rvals=[])

        #  ctypes.c_uint SetGate(ctypes.c_float delay, ctypes.c_float width, ctypes.c_float stepRenamed)
        self.SetGate=wrapper(lib.SetGate)
        #  ctypes.c_uint GetGateMode(ctypes.POINTER(ctypes.c_int) piGatemode)
        self.GetGateMode=wrapper(lib.GetGateMode)
        #  ctypes.c_uint SetGateMode(ctypes.c_int gatemode)
        self.SetGateMode=wrapper(lib.SetGateMode)

        #  ctypes.c_uint GetAcquisitionTimings(ctypes.POINTER(ctypes.c_float) exposure, ctypes.POINTER(ctypes.c_float) accumulate, ctypes.POINTER(ctypes.c_float) kinetic)
        self.GetAcquisitionTimings=wrapper(lib.GetAcquisitionTimings)
        #  ctypes.c_uint SetExposureTime(ctypes.c_float time)
        self.SetExposureTime=wrapper(lib.SetExposureTime)
        #  ctypes.c_uint GetMaximumExposure(ctypes.POINTER(ctypes.c_float) MaxExp)
        self.GetMaximumExposure=wrapper(lib.GetMaximumExposure)
        #  ctypes.c_uint SetDualExposureTimes(ctypes.c_float expTime1, ctypes.c_float expTime2)
        self.SetDualExposureTimes=wrapper(lib.SetDualExposureTimes)
        #  ctypes.c_uint SetDualExposureMode(ctypes.c_int mode)
        self.SetDualExposureMode=wrapper(lib.SetDualExposureMode)
        #  ctypes.c_uint GetDualExposureTimes(ctypes.POINTER(ctypes.c_float) exposure1, ctypes.POINTER(ctypes.c_float) exposure2)
        self.GetDualExposureTimes=wrapper(lib.GetDualExposureTimes)
        #  ctypes.c_uint GetMaximumNumberRingExposureTimes(ctypes.POINTER(ctypes.c_int) number)
        self.GetMaximumNumberRingExposureTimes=wrapper(lib.GetMaximumNumberRingExposureTimes)
        #  ctypes.c_uint GetRingExposureRange(ctypes.POINTER(ctypes.c_float) fpMin, ctypes.POINTER(ctypes.c_float) fpMax)
        self.GetRingExposureRange=wrapper(lib.GetRingExposureRange)
        #  ctypes.c_uint GetNumberRingExposureTimes(ctypes.POINTER(ctypes.c_int) ipnumTimes)
        self.GetNumberRingExposureTimes=wrapper(lib.GetNumberRingExposureTimes)
        #  ctypes.c_uint SetRingExposureTimes(ctypes.c_int numTimes, ctypes.POINTER(ctypes.c_float) times)
        self.SetRingExposureTimes=wrapper(lib.SetRingExposureTimes, rvals=["times"], byref=[],
                argprep={"times":lambda numTimes: (ctypes.c_float*numTimes)()},
                rconv={"times": lambda v,_,kwargs: np.ctypeslib.as_array(v,(kwargs["numTimes"],)).copy()})
        #  ctypes.c_uint GetAdjustedRingExposureTimes(ctypes.c_int inumTimes, ctypes.POINTER(ctypes.c_float) fptimes)
        self.GetAdjustedRingExposureTimes=wrapper(lib.GetAdjustedRingExposureTimes, rvals=["fptimes"], byref=[],
                argprep={"fptimes":lambda inumTimes: (ctypes.c_float*inumTimes)()},
                rconv={"fptimes": lambda v,_,kwargs: np.ctypeslib.as_array(v,(kwargs["inumTimes"],)).copy()})

        #  ctypes.c_uint SetAcquisitionMode(ctypes.c_int mode)
        self.SetAcquisitionMode=wrapper(lib.SetAcquisitionMode)
        #  ctypes.c_uint SetNumberAccumulations(ctypes.c_int number)
        self.SetNumberAccumulations=wrapper(lib.SetNumberAccumulations)
        #  ctypes.c_uint SetNumberKinetics(ctypes.c_int number)
        self.SetNumberKinetics=wrapper(lib.SetNumberKinetics)
        #  ctypes.c_uint SetNumberPrescans(ctypes.c_int iNumber)
        self.SetNumberPrescans=wrapper(lib.SetNumberPrescans)
        #  ctypes.c_uint SetKineticCycleTime(ctypes.c_float time)
        self.SetKineticCycleTime=wrapper(lib.SetKineticCycleTime)
        #  ctypes.c_uint SetAccumulationCycleTime(ctypes.c_float time)
        self.SetAccumulationCycleTime=wrapper(lib.SetAccumulationCycleTime)
        #  ctypes.c_uint SetFrameTransferMode(ctypes.c_int mode)
        self.SetFrameTransferMode=wrapper(lib.SetFrameTransferMode)
        #  ctypes.c_uint GetReadOutTime(ctypes.POINTER(ctypes.c_float) ReadOutTime)
        self.GetReadOutTime=wrapper(lib.GetReadOutTime)
        #  ctypes.c_uint GetKeepCleanTime(ctypes.POINTER(ctypes.c_float) KeepCleanTime)
        self.GetKeepCleanTime=wrapper(lib.GetKeepCleanTime)
        #  ctypes.c_uint EnableKeepCleans(ctypes.c_int iMode)
        self.EnableKeepCleans=wrapper(lib.EnableKeepCleans)
        #  ctypes.c_uint SetOverlapMode(ctypes.c_int mode)
        self.SetOverlapMode=wrapper(lib.SetOverlapMode)
        
        #  ctypes.c_uint SetFastKinetics(ctypes.c_int exposedRows, ctypes.c_int seriesLength, ctypes.c_float time, ctypes.c_int mode, ctypes.c_int hbin, ctypes.c_int vbin)
        self.SetFastKinetics=wrapper(lib.SetFastKinetics)
        #  ctypes.c_uint SetFastKineticsEx(ctypes.c_int exposedRows, ctypes.c_int seriesLength, ctypes.c_float time, ctypes.c_int mode, ctypes.c_int hbin, ctypes.c_int vbin, ctypes.c_int offset)
        self.SetFastKineticsEx=wrapper(lib.SetFastKineticsEx)
        #  ctypes.c_uint GetFKExposureTime(ctypes.POINTER(ctypes.c_float) time)
        self.GetFKExposureTime=wrapper(lib.GetFKExposureTime)
        #  ctypes.c_uint GetFKVShiftSpeedF(ctypes.c_int index, ctypes.POINTER(ctypes.c_float) speed)
        self.GetFKVShiftSpeedF=wrapper(lib.GetFKVShiftSpeedF)
        #  ctypes.c_uint SetFKVShiftSpeed(ctypes.c_int index)
        self.SetFKVShiftSpeed=wrapper(lib.SetFKVShiftSpeed)
        #  ctypes.c_uint GetNumberFKVShiftSpeeds(ctypes.POINTER(ctypes.c_int) number)
        self.GetNumberFKVShiftSpeeds=wrapper(lib.GetNumberFKVShiftSpeeds)

        #  ctypes.c_uint GetMCPGain(ctypes.POINTER(ctypes.c_int) piGain)
        self.GetMCPGain=wrapper(lib.GetMCPGain)
        #  ctypes.c_uint GetMCPGainRange(ctypes.POINTER(ctypes.c_int) iLow, ctypes.POINTER(ctypes.c_int) iHigh)
        self.GetMCPGainRange=wrapper(lib.GetMCPGainRange)
        #  ctypes.c_uint GetMCPVoltage(ctypes.POINTER(ctypes.c_int) iVoltage)
        self.GetMCPVoltage=wrapper(lib.GetMCPVoltage)
        #  ctypes.c_uint SetMCPGain(ctypes.c_int gain)
        self.SetMCPGain=wrapper(lib.SetMCPGain)
        #  ctypes.c_uint SetMCPGating(ctypes.c_int gating)
        self.SetMCPGating=wrapper(lib.SetMCPGating)

        #  ctypes.c_uint PrepareAcquisition()
        self.PrepareAcquisition=wrapper(lib.PrepareAcquisition)
        #  ctypes.c_uint StartAcquisition()
        self.StartAcquisition=wrapper(lib.StartAcquisition)
        #  ctypes.c_uint AbortAcquisition()
        self.AbortAcquisition=wrapper(lib.AbortAcquisition)
        #  ctypes.c_uint GetAcquisitionProgress(ctypes.POINTER(ctypes.c_long) acc, ctypes.POINTER(ctypes.c_long) series)
        self.GetAcquisitionProgress=wrapper(lib.GetAcquisitionProgress)
        #  ctypes.c_uint GetStatus(ctypes.POINTER(ctypes.c_int) status)
        self.GetStatus=wrapper(lib.GetStatus)
        #  ctypes.c_uint GetCameraEventStatus(ctypes.POINTER(DWORD) camStatus)
        self.GetCameraEventStatus=wrapper(lib.GetCameraEventStatus)
        #  ctypes.c_uint GetFrontEndStatus(ctypes.POINTER(ctypes.c_int) piFlag)
        self.GetFrontEndStatus=wrapper(lib.GetFrontEndStatus)
        #  ctypes.c_uint WaitForAcquisition()
        self.WaitForAcquisition=wrapper(lib.WaitForAcquisition)
        #  ctypes.c_uint WaitForAcquisitionTimeOut(ctypes.c_int iTimeOutMs)
        self.WaitForAcquisitionTimeOut=wrapper(lib.WaitForAcquisitionTimeOut)
        #  ctypes.c_uint WaitForAcquisitionByHandle(ctypes.c_long cameraHandle)
        self.WaitForAcquisitionByHandle=wrapper(lib.WaitForAcquisitionByHandle)
        #  ctypes.c_uint WaitForAcquisitionByHandleTimeOut(ctypes.c_long cameraHandle, ctypes.c_int iTimeOutMs)
        self.WaitForAcquisitionByHandleTimeOut=wrapper(lib.WaitForAcquisitionByHandleTimeOut)
        #  ctypes.c_uint CancelWait()
        self.CancelWait=wrapper(lib.CancelWait)

        #  ctypes.c_uint SetReadMode(ctypes.c_int mode)
        self.SetReadMode=wrapper(lib.SetReadMode)
        #  ctypes.c_uint GetMaximumBinning(ctypes.c_int ReadMode, ctypes.c_int HorzVert, ctypes.POINTER(ctypes.c_int) MaxBinning)
        self.GetMaximumBinning=wrapper(lib.GetMaximumBinning)
        #  ctypes.c_uint GetMinimumImageLength(ctypes.POINTER(ctypes.c_int) MinImageLength)
        self.GetMinimumImageLength=wrapper(lib.GetMinimumImageLength)
        #  ctypes.c_uint SetSingleTrack(ctypes.c_int centre, ctypes.c_int height)
        self.SetSingleTrack=wrapper(lib.SetSingleTrack)
        #  ctypes.c_uint SetMultiTrack(ctypes.c_int number, ctypes.c_int height, ctypes.c_int offset, ctypes.POINTER(ctypes.c_int) bottom, ctypes.POINTER(ctypes.c_int) gap)
        self.SetMultiTrack=wrapper(lib.SetMultiTrack)
        #  ctypes.c_uint SetRa\ndomTracks(ctypes.c_int numTracks, ctypes.POINTER(ctypes.c_int) areas)
        self.SetRandomTracks_lib=wrapper(lib.SetRandomTracks, args="all", byref=[])
        #  ctypes.c_uint SetImage(ctypes.c_int hbin, ctypes.c_int vbin, ctypes.c_int hstart, ctypes.c_int hend, ctypes.c_int vstart, ctypes.c_int vend)
        self.SetImage=wrapper(lib.SetImage)
        #  ctypes.c_uint SetFVBHBin(ctypes.c_int bin)
        self.SetFVBHBin=wrapper(lib.SetFVBHBin)
        #  ctypes.c_uint GetImageFlip(ctypes.POINTER(ctypes.c_int) iHFlip, ctypes.POINTER(ctypes.c_int) iVFlip)
        self.GetImageFlip=wrapper(lib.GetImageFlip)
        #  ctypes.c_uint GetImageRotate(ctypes.POINTER(ctypes.c_int) iRotate)
        self.SetImageFlip=wrapper(lib.SetImageFlip)
        #  ctypes.c_uint SetImageRotate(ctypes.c_int iRotate)
        self.GetImageRotate=wrapper(lib.GetImageRotate)
        #  ctypes.c_uint SetImageFlip(ctypes.c_int iHFlip, ctypes.c_int iVFlip)
        self.SetImageRotate=wrapper(lib.SetImageRotate)
        #  ctypes.c_uint GetDetector(ctypes.POINTER(ctypes.c_int) xpixels, ctypes.POINTER(ctypes.c_int) ypixels)
        self.GetDetector=wrapper(lib.GetDetector)

        #  ctypes.c_uint GetBaselineClamp(ctypes.POINTER(ctypes.c_int) state)
        self.GetBaselineClamp=wrapper(lib.GetBaselineClamp)
        #  ctypes.c_uint SetBaselineClamp(ctypes.c_int state)
        self.SetBaselineClamp=wrapper(lib.SetBaselineClamp)
        #  ctypes.c_uint SetBaselineOffset(ctypes.c_int offset)
        self.SetBaselineOffset=wrapper(lib.SetBaselineOffset)

        #  ctypes.c_uint GetFilterMode(ctypes.POINTER(ctypes.c_int) mode)
        self.GetFilterMode=wrapper(lib.GetFilterMode)
        #  ctypes.c_uint SetFilterMode(ctypes.c_int mode)
        self.SetFilterMode=wrapper(lib.SetFilterMode)
        #  ctypes.c_uint Filter_SetMode(ctypes.c_uint mode)
        self.Filter_SetMode=wrapper(lib.Filter_SetMode)
        #  ctypes.c_uint Filter_GetMode(ctypes.POINTER(ctypes.c_uint) mode)
        self.Filter_GetMode=wrapper(lib.Filter_GetMode)
        #  ctypes.c_uint Filter_SetThreshold(ctypes.c_float threshold)
        self.Filter_SetThreshold=wrapper(lib.Filter_SetThreshold)
        #  ctypes.c_uint Filter_GetThreshold(ctypes.POINTER(ctypes.c_float) threshold)
        self.Filter_GetThreshold=wrapper(lib.Filter_GetThreshold)
        #  ctypes.c_uint Filter_SetDataAveragingMode(ctypes.c_int mode)
        self.Filter_SetDataAveragingMode=wrapper(lib.Filter_SetDataAveragingMode)
        #  ctypes.c_uint Filter_GetDataAveragingMode(ctypes.POINTER(ctypes.c_int) mode)
        self.Filter_GetDataAveragingMode=wrapper(lib.Filter_GetDataAveragingMode)
        #  ctypes.c_uint Filter_SetAveragingFrameCount(ctypes.c_int frames)
        self.Filter_SetAveragingFrameCount=wrapper(lib.Filter_SetAveragingFrameCount)
        #  ctypes.c_uint Filter_GetAveragingFrameCount(ctypes.POINTER(ctypes.c_int) frames)
        self.Filter_GetAveragingFrameCount=wrapper(lib.Filter_GetAveragingFrameCount)
        #  ctypes.c_uint Filter_SetAveragingFactor(ctypes.c_int averagingFactor)
        self.Filter_SetAveragingFactor=wrapper(lib.Filter_SetAveragingFactor)
        #  ctypes.c_uint Filter_GetAveragingFactor(ctypes.POINTER(ctypes.c_int) averagingFactor)
        self.Filter_GetAveragingFactor=wrapper(lib.Filter_GetAveragingFactor)

        #  ctypes.c_uint GetSizeOfCircularBuffer(ctypes.POINTER(ctypes.c_long) index)
        self.GetSizeOfCircularBuffer=wrapper(lib.GetSizeOfCircularBuffer)
        #  ctypes.c_uint FreeInternalMemory()
        self.FreeInternalMemory=wrapper(lib.FreeInternalMemory)
        #  ctypes.c_uint GetImagesPerDMA(ctypes.POINTER(ctypes.c_ulong) images)
        self.GetImagesPerDMA=wrapper(lib.GetImagesPerDMA)
        #  ctypes.c_uint SetDMAParameters(ctypes.c_int MaxImagesPerDMA, ctypes.c_float SecondsPerDMA)
        self.SetDMAParameters=wrapper(lib.SetDMAParameters)

        buffer16_prep=ctypes_wrap.buffprep(0,"<u2")
        buffer32_prep=ctypes_wrap.buffprep(0,"<u4")
        buffer16_conv=ctypes_wrap.buffconv(0,"<u2")
        buffer32_conv=ctypes_wrap.buffconv(0,"<u4")
        #  ctypes.c_uint GetOldestImage(ctypes.POINTER(ctypes.c_long) arr, ctypes.c_ulong size)
        self.GetOldestImage=wrapper(lib.GetOldestImage, rvals=["arr"],
            argprep={"arr":buffer32_prep}, rconv={"arr":buffer32_conv}, byref=[])
        #  ctypes.c_uint GetOldestImage16(ctypes.POINTER(WORD) arr, ctypes.c_ulong size)
        self.GetOldestImage16=wrapper(lib.GetOldestImage16, rvals=["arr"],
            argprep={"arr":buffer16_prep}, rconv={"arr":buffer16_conv}, byref=[])
        #  ctypes.c_uint GetMostRecentImage(ctypes.POINTER(ctypes.c_long) arr, ctypes.c_ulong size)
        self.GetMostRecentImage=wrapper(lib.GetMostRecentImage, rvals=["arr"],
            argprep={"arr":buffer32_prep}, rconv={"arr":buffer32_conv}, byref=[])
        #  ctypes.c_uint GetMostRecentImage16(ctypes.POINTER(WORD) arr, ctypes.c_ulong size)
        self.GetMostRecentImage16=wrapper(lib.GetMostRecentImage16, rvals=["arr"],
            argprep={"arr":buffer16_prep}, rconv={"arr":buffer16_conv}, byref=[])
        #  ctypes.c_uint GetMostRecentColorImage16(ctypes.c_ulong size, ctypes.c_int algorithm, ctypes.POINTER(WORD) red, ctypes.POINTER(WORD) green, ctypes.POINTER(WORD) blue)
        self.GetMostRecentColorImage16=wrapper(lib.GetMostRecentColorImage16, rvals=["red","green","blue"],
            argprep={ch:buffer16_prep for ch in["red","green","blue"]}, rconv={ch:buffer16_conv for ch in["red","green","blue"]}, byref=[])
        #  ctypes.c_uint GetNumberNewImages(ctypes.POINTER(ctypes.c_long) first, ctypes.POINTER(ctypes.c_long) last)
        self.GetNumberNewImages=wrapper(lib.GetNumberNewImages)
        #  ctypes.c_uint GetNumberAvailableImages(ctypes.POINTER(ctypes.c_long) first, ctypes.POINTER(ctypes.c_long) last)
        self.GetNumberAvailableImages=wrapper(lib.GetNumberAvailableImages)
        #  ctypes.c_uint GetTotalNumberImagesAcquired(ctypes.POINTER(ctypes.c_long) index)
        self.GetTotalNumberImagesAcquired=wrapper(lib.GetTotalNumberImagesAcquired)
        def images_buffer16_prep(size):
            return buffer16_prep(size)
        def images_buffer32_prep(size):
            return buffer32_prep(size)
        def images_buffer16_conv(buff, _, kwargs):
            return buffer16_conv(buff,kwargs["size"])
        def images_buffer32_conv(buff, _, kwargs):
            return buffer32_conv(buff,kwargs["size"])
        #  ctypes.c_uint GetImages(ctypes.c_long first, ctypes.c_long last, ctypes.POINTER(ctypes.c_long) arr, ctypes.c_ulong size, ctypes.POINTER(ctypes.c_long) validfirst, ctypes.POINTER(ctypes.c_long) validlast)
        self.GetImages=wrapper(lib.GetImages, rvals=["arr","validfirst","validlast"],
            argprep={"arr":images_buffer32_prep}, rconv={"arr":images_buffer32_conv}, byref=["validfirst","validlast"])
        #  ctypes.c_uint GetImages16(ctypes.c_long first, ctypes.c_long last, ctypes.POINTER(WORD) arr, ctypes.c_ulong size, ctypes.POINTER(ctypes.c_long) validfirst, ctypes.POINTER(ctypes.c_long) validlast)
        self.GetImages16=wrapper(lib.GetImages16, rvals=["arr","validfirst","validlast"],
            argprep={"arr":images_buffer16_prep}, rconv={"arr":images_buffer16_conv}, byref=["validfirst","validlast"])
        #  ctypes.c_uint GetAcquiredData(ctypes.POINTER(ctypes.c_long) arr, ctypes.c_ulong size)
        self.GetAcquiredData=wrapper(lib.GetAcquiredData, rvals=["arr"],
            argprep={"arr":buffer32_prep}, rconv={"arr":buffer32_conv}, byref=[])
        #  ctypes.c_uint GetAcquiredData16(ctypes.POINTER(WORD) arr, ctypes.c_ulong size)
        self.GetAcquiredData16=wrapper(lib.GetAcquiredData16, rvals=["arr"],
            argprep={"arr":buffer16_prep}, rconv={"arr":buffer16_conv}, byref=[])

        #  ctypes.c_uint GetMetaDataInfo(ctypes.c_void_p TimeOfStart, ctypes.POINTER(ctypes.c_float) pfTimeFromStart, ctypes.c_uint index)
        self.GetMetaDataInfo=wrapper(lib.GetMetaDataInfo)
        #  ctypes.c_uint SetMetaData(ctypes.c_int state)
        self.SetMetaData=wrapper(lib.SetMetaData)
        #  ctypes.c_uint GetMetaData(ctypes.POINTER(ctypes.c_ubyte) data, ctypes.c_uint _ui_index)
        self.GetMetaData=wrapper(lib.GetMetaData)

        #  ctypes.c_uint SetDriverEvent(HANDLE driverEvent)
        self.SetDriverEvent=wrapper(lib.SetDriverEvent)
        #  ctypes.c_uint SetAcqStatusEvent(HANDLE statusEvent)
        self.SetAcqStatusEvent=wrapper(lib.SetAcqStatusEvent)
        #  ctypes.c_uint SetFrontEndEvent(HANDLE driverEvent)
        self.SetFrontEndEvent=wrapper(lib.SetFrontEndEvent)
        #  ctypes.c_uint SetOverTempEvent(HANDLE tempEvent)
        self.SetOverTempEvent=wrapper(lib.SetOverTempEvent)
        #  ctypes.c_uint SetSaturationEvent(HANDLE saturationEvent)
        self.SetSaturationEvent=wrapper(lib.SetSaturationEvent)
        #  ctypes.c_uint SetTECEvent(HANDLE driverEvent)
        self.SetTECEvent=wrapper(lib.SetTECEvent)

        
        self._initialized=True
        
        return

        # #  ctypes.c_uint GetHVflag(ctypes.POINTER(ctypes.c_int) bFlag)
        # lib.GetHVflag.restype=ctypes.c_uint
        # lib.GetHVflag.argtypes=[ctypes.POINTER(ctypes.c_int)]
        # lib.GetHVflag.argnames=["bFlag"]
        # #  ctypes.c_uint GetPhosphorStatus(ctypes.POINTER(ctypes.c_int) piFlag)
        # lib.GetPhosphorStatus.restype=ctypes.c_uint
        # lib.GetPhosphorStatus.argtypes=[ctypes.POINTER(ctypes.c_int)]
        # lib.GetPhosphorStatus.argnames=["piFlag"]
        # #  ctypes.c_uint SetPhosphorEvent(HANDLE driverEvent)
        # lib.SetPhosphorEvent.restype=ctypes.c_uint
        # lib.SetPhosphorEvent.argtypes=[HANDLE]
        # lib.SetPhosphorEvent.argnames=["driverEvent"]
        # #  ctypes.c_uint SetCameraLinkMode(ctypes.c_int mode)
        # lib.SetCameraLinkMode.restype=ctypes.c_uint
        # lib.SetCameraLinkMode.argtypes=[ctypes.c_int]
        # lib.SetCameraLinkMode.argnames=["mode"]
        # #  ctypes.c_uint SetCameraStatusEnable(DWORD Enable)
        # lib.SetCameraStatusEnable.restype=ctypes.c_uint
        # lib.SetCameraStatusEnable.argtypes=[DWORD]
        # lib.SetCameraStatusEnable.argnames=["Enable"]
        # #  ctypes.c_uint SetComplexImage(ctypes.c_int numAreas, ctypes.POINTER(ctypes.c_int) areas)
        # lib.SetComplexImage.restype=ctypes.c_uint
        # lib.SetComplexImage.argtypes=[ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        # lib.SetComplexImage.argnames=["numAreas", "areas"]
        # #  ctypes.c_uint SetCropMode(ctypes.c_int active, ctypes.c_int cropHeight, ctypes.c_int reserved)
        # lib.SetCropMode.restype=ctypes.c_uint
        # lib.SetCropMode.argtypes=[ctypes.c_int, ctypes.c_int, ctypes.c_int]
        # lib.SetCropMode.argnames=["active", "cropHeight", "reserved"]
        # #  ctypes.c_uint SetCustomTrackHBin(ctypes.c_int bin)
        # lib.SetCustomTrackHBin.restype=ctypes.c_uint
        # lib.SetCustomTrackHBin.argtypes=[ctypes.c_int]
        # lib.SetCustomTrackHBin.argnames=["bin"]
        # #  ctypes.c_uint SetIsolatedCropMode(ctypes.c_int active, ctypes.c_int cropheight, ctypes.c_int cropwidth, ctypes.c_int vbin, ctypes.c_int hbin)
        # lib.SetIsolatedCropMode.restype=ctypes.c_uint
        # lib.SetIsolatedCropMode.argtypes=[ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        # lib.SetIsolatedCropMode.argnames=["active", "cropheight", "cropwidth", "vbin", "hbin"]
        #  ctypes.c_uint SetIsolatedCropModeEx(ctypes.c_int active, ctypes.c_int cropheight, ctypes.c_int cropwidth, ctypes.c_int vbin, ctypes.c_int hbin, ctypes.c_int cropleft, ctypes.c_int cropbottom)
        # lib.SetIsolatedCropModeEx.restype=ctypes.c_uint
        # lib.SetIsolatedCropModeEx.argtypes=[ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        # lib.SetIsolatedCropModeEx.argnames=["active", "cropheight", "cropwidth", "vbin", "hbin", "cropleft", "cropbottom"]
        # #  ctypes.c_uint SetIsolatedCropModeType(ctypes.c_int type)
        # lib.SetIsolatedCropModeType.restype=ctypes.c_uint
        # lib.SetIsolatedCropModeType.argtypes=[ctypes.c_int]
        # lib.SetIsolatedCropModeType.argnames=["type"]
        # #  ctypes.c_uint SetMultiTrackHBin(ctypes.c_int bin)
        # lib.SetMultiTrackHBin.restype=ctypes.c_uint
        # lib.SetMultiTrackHBin.argtypes=[ctypes.c_int]
        # lib.SetMultiTrackHBin.argnames=["bin"]
        # #  ctypes.c_uint SetMultiTrackHRange(ctypes.c_int iStart, ctypes.c_int iEnd)
        # lib.SetMultiTrackHRange.restype=ctypes.c_uint
        # lib.SetMultiTrackHRange.argtypes=[ctypes.c_int, ctypes.c_int]
        # lib.SetMultiTrackHRange.argnames=["iStart", "iEnd"]
        #  ctypes.c_uint SetPCIMode(ctypes.c_int mode, ctypes.c_int value)
        # lib.SetPCIMode.restype=ctypes.c_uint
        # lib.SetPCIMode.argtypes=[ctypes.c_int, ctypes.c_int]
        # lib.SetPCIMode.argnames=["mode", "value"]
        # #  ctypes.c_uint SetSingleTrackHBin(ctypes.c_int bin)
        # lib.SetSingleTrackHBin.restype=ctypes.c_uint
        # lib.SetSingleTrackHBin.argtypes=[ctypes.c_int]
        # lib.SetSingleTrackHBin.argnames=["bin"]
        # #  ctypes.c_uint DemosaicImage(ctypes.POINTER(WORD) grey, ctypes.POINTER(WORD) red, ctypes.POINTER(WORD) green, ctypes.POINTER(WORD) blue, ctypes.POINTER(ColorDemosaicInfo) info)
        # lib.DemosaicImage.restype=ctypes.c_uint
        # lib.DemosaicImage.argtypes=[ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(ColorDemosaicInfo)]
        # lib.DemosaicImage.argnames=["grey", "red", "green", "blue", "info"]
        # #  ctypes.c_uint WhiteBalance(ctypes.POINTER(WORD) wRed, ctypes.POINTER(WORD) wGreen, ctypes.POINTER(WORD) wBlue, ctypes.POINTER(ctypes.c_float) fRelR, ctypes.POINTER(ctypes.c_float) fRelB, ctypes.POINTER(WhiteBalanceInfo) info)
        # lib.WhiteBalance.restype=ctypes.c_uint
        # lib.WhiteBalance.argtypes=[ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(WhiteBalanceInfo)]
        # lib.WhiteBalance.argnames=["wRed", "wGreen", "wBlue", "fRelR", "fRelB", "info"]
        # #  ctypes.c_uint PostProcessNoiseFilter(ctypes.POINTER(ctypes.c_long) pInputImage, ctypes.POINTER(ctypes.c_long) pOutputImage, ctypes.c_int iOutputBufferSize, ctypes.c_int iBaseline, ctypes.c_int iMode, ctypes.c_float fThreshold, ctypes.c_int iHeight, ctypes.c_int iWidth)
        # lib.PostProcessNoiseFilter.restype=ctypes.c_uint
        # lib.PostProcessNoiseFilter.argtypes=[ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_int, ctypes.c_int]
        # lib.PostProcessNoiseFilter.argnames=["pInputImage", "pOutputImage", "iOutputBufferSize", "iBaseline", "iMode", "fThreshold", "iHeight", "iWidth"]
        # #  ctypes.c_uint PostProcessCountConvert(ctypes.POINTER(ctypes.c_long) pInputImage, ctypes.POINTER(ctypes.c_long) pOutputImage, ctypes.c_int iOutputBufferSize, ctypes.c_int iNumImages, ctypes.c_int iBaseline, ctypes.c_int iMode, ctypes.c_int iEmGain, ctypes.c_float fQE, ctypes.c_float fSensitivity, ctypes.c_int iHeight, ctypes.c_int iWidth)
        # lib.PostProcessCountConvert.restype=ctypes.c_uint
        # lib.PostProcessCountConvert.argtypes=[ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_int, ctypes.c_int]
        # lib.PostProcessCountConvert.argnames=["pInputImage", "pOutputImage", "iOutputBufferSize", "iNumImages", "iBaseline", "iMode", "iEmGain", "fQE", "fSensitivity", "iHeight", "iWidth"]
        # #  ctypes.c_uint PostProcessPhotonCounting(ctypes.POINTER(ctypes.c_long) pInputImage, ctypes.POINTER(ctypes.c_long) pOutputImage, ctypes.c_int iOutputBufferSize, ctypes.c_int iNumImages, ctypes.c_int iNumframes, ctypes.c_int iNumberOfThresholds, ctypes.POINTER(ctypes.c_float) pfThreshold, ctypes.c_int iHeight, ctypes.c_int iWidth)
        # lib.PostProcessPhotonCounting.restype=ctypes.c_uint
        # lib.PostProcessPhotonCounting.argtypes=[ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int]
        # lib.PostProcessPhotonCounting.argnames=["pInputImage", "pOutputImage", "iOutputBufferSize", "iNumImages", "iNumframes", "iNumberOfThresholds", "pfThreshold", "iHeight", "iWidth"]
        
    


    def SetRandomTracks(self, tracks):
        ntracks=len(tracks)
        areas=(ctypes.c_int32*(ntracks*2))(*[b for t in tracks for b in t])
        self.SetRandomTracks_lib(ntracks,areas)


    def get_amp_mode_description(self, mode):
        """Get full amplifier mode description"""
        ch,oamp,hssp,pa=mode
        bit_depth=self.GetBitDepth(ch)
        oamp_kind=py3.as_str(self.GetAmpDesc(oamp))
        hsspeed_hz=self.GetHSSpeed(ch,oamp,hssp)
        preamp_gain=self.GetPreAmpGain(pa)
        return TAmpModeFull(ch,bit_depth,oamp,oamp_kind,hssp,hsspeed_hz,pa,preamp_gain)
    def get_all_amp_modes(self):
        """
        Get all available preamp modes.

        Each preamp mode is characterized by an AD channel index, amplifier index, channel speed (horizontal scan speed) index and preamp gain index.
        Return list of tuples ``(channel, channel_bitdepth, oamp, oamp_kind, hsspeed, hsspeed_MHz, preamp, preamp_gain)``,
        where ``channel``, ``oamp``, ``hsspeed`` and ``preamp`` are indices, while ``channel_bitdepth``, ``oamp_kind``, ``hsspeed_MHz`` and ``preamp_gain`` are descriptions.
        """
        channels=self.GetNumberADChannels()
        oamps=self.GetNumberAmp()
        preamps=self.GetNumberPreAmpGains()
        modes=[]
        for ch in range(channels):
            bit_depth=self.GetBitDepth(ch)
            for oamp in range(oamps):
                oamp_kind=py3.as_str(self.GetAmpDesc(oamp))
                hsspeeds=self.GetNumberHSSpeeds(ch,oamp)
                for hssp in range(hsspeeds):
                    hsspeed_hz=self.GetHSSpeed(ch,oamp,hssp)
                    for pa in range(preamps):
                        try:
                            preamp_gain=self.GetPreAmpGain(pa)
                            if self.IsPreAmpGainAvailable(ch,oamp,hssp,pa):
                                modes.append(TAmpModeFull(ch,bit_depth,oamp,oamp_kind,hssp,hsspeed_hz,pa,preamp_gain))
                        except AndorSDK2LibError:
                            pass
        return modes
    def set_amp_mode(self, amp_mode):
        """
        Setup preamp mode.

        `amp_mode` is a tuple ``(channel, oamp, hsspeed, preamp)``, specifying AD channel index, amplifier index, channel speed (horizontal scan speed) index and preamp gain index.
        """
        if len(amp_mode)==4:
            amp_mode=TAmpModeSimple(*amp_mode)
        else:
            amp_mode=TAmpModeFull(*amp_mode)
        if amp_mode.channel is not None:
            self.SetADChannel(amp_mode.channel)
        if amp_mode.oamp is not None:
            self.SetOutputAmplifier(amp_mode.oamp)
            if amp_mode.hsspeed is not None:
                self.SetHSSpeed(amp_mode.oamp,amp_mode.hsspeed)
        if amp_mode.preamp is not None:
            self.SetPreAmpGain(amp_mode.preamp)

    def get_EMCCD_gain(self):
        """
        Get current EMCCD gain.

        Return tuple ``(gain, advanced)``.
        """
        gain=self.GetEMCCDGain()
        advanced=self.GetEMAdvanced()
        return gain,advanced
    def set_EMCCD_gain(self, gain, advanced=None):
        """
        Set EMCCD gain.

        Gain goes up to 300 if ``advanced==False`` or higher if ``advanced==True`` (in this mode the sensor can be permanently damaged by strong light).
        """
        if advanced is not None:
            self.SetEMAdvanced(advanced)
        self.SetEMCCDGain(gain)


wlib=AndorSDK2Lib()