# pylint: disable=spelling

from . import ShamrockCIF_defs  # pylint: disable=unused-import
from .ShamrockCIF_defs import SHAMROCK_ERR, drSHAMROCK_ERR
from .ShamrockCIF_defs import SHAMROCK_CONST  # pylint: disable=unused-import
from .ShamrockCIF_defs import define_functions
from .base import AndorError

from ...core.utils import ctypes_wrap, py3
from ..utils import load_lib

import platform
import ctypes
import os



class ShamrockLibError(AndorError):
    """Generic Andor Shamrock library error"""
    def __init__(self, func, code, lib=None):
        self.func=func
        self.code=code
        self.name=drSHAMROCK_ERR.get(self.code,"UNKNOWN")
        self.desc=""
        try:
            if lib is not None:
                self.desc=py3.as_str(lib.ShamrockGetFunctionReturnDescription(code))
        except ShamrockLibError:
            pass
        msg="function '{}' raised error {}({}): {}".format(func,code,self.name,self.desc)
        super().__init__(msg)
def errcheck(passing=None, lib=None):
    """
    Build an error checking function.

    Return a function which checks return codes of Andor Shamrock library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    passing=set(passing) if passing is not None else set()
    passing.add(SHAMROCK_ERR.SHAMROCK_SUCCESS) # always allow success
    def errchecker(result, func, arguments):  # pylint: disable=unused-argument
        if result not in passing:
            raise ShamrockLibError(func.__name__,result,lib=lib)
        return result
    return errchecker




class ShamrockLib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return

        solis_path=load_lib.get_program_files_folder("Andor SOLIS")
        shamrock_path=os.path.join(solis_path,"Shamrock")
        sdk2_path=load_lib.get_program_files_folder("Andor SDK")
        archbit=platform.architecture()[0][:2]
        error_message="The library is automatically supplied with Andor SDK2 software or micromanager plugin\n"+load_lib.par_error_message.format("andor_shamrock")
        lib_names=["atspectrograph.dll","ShamrockCIF{}.dll".format(archbit),"ShamrockCIF.dll"]
        depends=["atshamrock.dll","atshamrock{}.dll".format(archbit),"atmcd{}d.dll".format(archbit),"atmcd{}d_legacy.dll".format(archbit)]
        locations=["parameter/andor_shamrock",sdk2_path,solis_path,shamrock_path,"global"]
        self.lib=load_lib.load_lib(lib_names,locations=locations,depends=depends,depends_required=False,error_message=error_message,call_conv="stdcall")
        lib=self.lib
        define_functions(lib)

        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(lib=self),default_rvals="pointer")
        default_strlen=256
        strprep=ctypes_wrap.strprep(default_strlen)

        
        #  ctypes.c_uint ShamrockInitialize(ctypes.c_char_p IniPath)
        self.ShamrockInitialize=wrapper(lib.ShamrockInitialize)
        #  ctypes.c_uint ShamrockClose()
        self.ShamrockClose=wrapper(lib.ShamrockClose)
        #  ctypes.c_uint ShamrockGetFunctionReturnDescription(ctypes.c_int error, ctypes.c_char_p description, ctypes.c_int MaxDescStrLen)
        self.ShamrockGetFunctionReturnDescription=wrapper(lib.ShamrockGetFunctionReturnDescription, args=["error"], rvals=["description"],
            argprep={"description":strprep,"MaxDescStrLen":default_strlen}, byref=[], errcheck=errcheck())
            
        #  ctypes.c_uint ShamrockGetNumberDevices(ctypes.POINTER(ctypes.c_int) nodevices)
        self.ShamrockGetNumberDevices=wrapper(lib.ShamrockGetNumberDevices)
        #  ctypes.c_uint ShamrockGetSerialNumber(ctypes.c_int device, ctypes.c_char_p serial)
        self.ShamrockGetSerialNumber=wrapper(lib.ShamrockGetSerialNumber, args=["device"], rvals=["serial"],
            argprep={"serial":strprep}, byref=[])
        #  ctypes.c_uint ShamrockEepromGetOpticalParams(ctypes.c_int device, ctypes.POINTER(ctypes.c_float) FocalLength, ctypes.POINTER(ctypes.c_float) AngularDeviation, ctypes.POINTER(ctypes.c_float) FocalTilt)
        self.ShamrockEepromGetOpticalParams=wrapper(lib.ShamrockEepromGetOpticalParams)

        #  ctypes.c_uint ShamrockGratingIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
        self.ShamrockGratingIsPresent=wrapper(lib.ShamrockGratingIsPresent)
        #  ctypes.c_uint ShamrockGetTurret(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) Turret)
        self.ShamrockGetTurret=wrapper(lib.ShamrockGetTurret)
        #  ctypes.c_uint ShamrockSetTurret(ctypes.c_int device, ctypes.c_int Turret)
        self.ShamrockSetTurret=wrapper(lib.ShamrockSetTurret)
        #  ctypes.c_uint ShamrockGetNumberGratings(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) noGratings)
        self.ShamrockGetNumberGratings=wrapper(lib.ShamrockGetNumberGratings)
        #  ctypes.c_uint ShamrockGetGrating(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) grating)
        self.ShamrockGetGrating=wrapper(lib.ShamrockGetGrating)
        #  ctypes.c_uint ShamrockSetGrating(ctypes.c_int device, ctypes.c_int grating)
        self.ShamrockSetGrating=wrapper(lib.ShamrockSetGrating)
        #  ctypes.c_uint ShamrockGetGratingInfo(ctypes.c_int device, ctypes.c_int Grating, ctypes.POINTER(ctypes.c_float) Lines, ctypes.c_char_p Blaze, ctypes.POINTER(ctypes.c_int) Home, ctypes.POINTER(ctypes.c_int) Offset)
        self.ShamrockGetGratingInfo=wrapper(lib.ShamrockGetGratingInfo, args=["device","Grating"], rvals=["Lines","Blaze","Home","Offset"],
            argprep={"Blaze":strprep}, byref=["Lines","Home","Offset"])
        #  ctypes.c_uint ShamrockGetGratingOffset(ctypes.c_int device, ctypes.c_int Grating, ctypes.POINTER(ctypes.c_int) offset)
        self.ShamrockGetGratingOffset=wrapper(lib.ShamrockGetGratingOffset)
        #  ctypes.c_uint ShamrockSetGratingOffset(ctypes.c_int device, ctypes.c_int Grating, ctypes.c_int offset)
        self.ShamrockSetGratingOffset=wrapper(lib.ShamrockSetGratingOffset)
        #  ctypes.c_uint ShamrockGetDetectorOffset(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) offset)
        self.ShamrockGetDetectorOffset=wrapper(lib.ShamrockGetDetectorOffset)
        #  ctypes.c_uint ShamrockSetDetectorOffset(ctypes.c_int device, ctypes.c_int offset)
        self.ShamrockSetDetectorOffset=wrapper(lib.ShamrockSetDetectorOffset)
        #  ctypes.c_uint ShamrockGetDetectorOffsetPort2(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) offset)
        self.ShamrockGetDetectorOffsetPort2=wrapper(lib.ShamrockGetDetectorOffsetPort2)
        #  ctypes.c_uint ShamrockSetDetectorOffsetPort2(ctypes.c_int device, ctypes.c_int offset)
        self.ShamrockSetDetectorOffsetPort2=wrapper(lib.ShamrockSetDetectorOffsetPort2)
        #  ctypes.c_uint ShamrockWavelengthReset(ctypes.c_int device)
        self.ShamrockWavelengthReset=wrapper(lib.ShamrockWavelengthReset)
        
        #  ctypes.c_uint ShamrockWavelengthIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
        self.ShamrockWavelengthIsPresent=wrapper(lib.ShamrockWavelengthIsPresent)
        #  ctypes.c_uint ShamrockGetWavelengthLimits(ctypes.c_int device, ctypes.c_int Grating, ctypes.POINTER(ctypes.c_float) Min, ctypes.POINTER(ctypes.c_float) Max)
        self.ShamrockGetWavelengthLimits=wrapper(lib.ShamrockGetWavelengthLimits)
        #  ctypes.c_uint ShamrockGetWavelength(ctypes.c_int device, ctypes.POINTER(ctypes.c_float) wavelength)
        self.ShamrockGetWavelength=wrapper(lib.ShamrockGetWavelength)
        #  ctypes.c_uint ShamrockSetWavelength(ctypes.c_int device, ctypes.c_float wavelength)
        self.ShamrockSetWavelength=wrapper(lib.ShamrockSetWavelength)
        #  ctypes.c_uint ShamrockAtZeroOrder(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) atZeroOrder)
        self.ShamrockAtZeroOrder=wrapper(lib.ShamrockAtZeroOrder)
        #  ctypes.c_uint ShamrockGotoZeroOrder(ctypes.c_int device)
        self.ShamrockGotoZeroOrder=wrapper(lib.ShamrockGotoZeroOrder)

        #  ctypes.c_uint ShamrockAutoSlitIsPresent(ctypes.c_int device, ctypes.c_int index, ctypes.POINTER(ctypes.c_int) present)
        self.ShamrockAutoSlitIsPresent=wrapper(lib.ShamrockAutoSlitIsPresent)
        #  ctypes.c_uint ShamrockAutoSlitReset(ctypes.c_int device, ctypes.c_int index)
        self.ShamrockAutoSlitReset=wrapper(lib.ShamrockAutoSlitReset)
        #  ctypes.c_uint ShamrockGetAutoSlitWidth(ctypes.c_int device, ctypes.c_int index, ctypes.POINTER(ctypes.c_float) width)
        self.ShamrockGetAutoSlitWidth=wrapper(lib.ShamrockGetAutoSlitWidth)
        #  ctypes.c_uint ShamrockSetAutoSlitWidth(ctypes.c_int device, ctypes.c_int index, ctypes.c_float width)
        self.ShamrockSetAutoSlitWidth=wrapper(lib.ShamrockSetAutoSlitWidth)
        #  ctypes.c_uint ShamrockGetAutoSlitCoefficients(ctypes.c_int device, ctypes.c_int index, ctypes.POINTER(ctypes.c_int) x1, ctypes.POINTER(ctypes.c_int) y1, ctypes.POINTER(ctypes.c_int) x2, ctypes.POINTER(ctypes.c_int) y2)
        self.ShamrockGetAutoSlitCoefficients=wrapper(lib.ShamrockGetAutoSlitCoefficients)
        #  ctypes.c_uint ShamrockSetAutoSlitCoefficients(ctypes.c_int device, ctypes.c_int index, ctypes.c_int x1, ctypes.c_int y1, ctypes.c_int x2, ctypes.c_int y2)
        self.ShamrockSetAutoSlitCoefficients=wrapper(lib.ShamrockSetAutoSlitCoefficients)
        
        #  ctypes.c_uint ShamrockShutterIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
        self.ShamrockShutterIsPresent=wrapper(lib.ShamrockShutterIsPresent)
        #  ctypes.c_uint ShamrockIsModePossible(ctypes.c_int device, ctypes.c_int mode, ctypes.POINTER(ctypes.c_int) possible)
        self.ShamrockIsModePossible=wrapper(lib.ShamrockIsModePossible)
        #  ctypes.c_uint ShamrockGetShutter(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) mode)
        self.ShamrockGetShutter=wrapper(lib.ShamrockGetShutter)
        #  ctypes.c_uint ShamrockSetShutter(ctypes.c_int device, ctypes.c_int mode)
        self.ShamrockSetShutter=wrapper(lib.ShamrockSetShutter)

        #  ctypes.c_uint ShamrockIrisIsPresent(ctypes.c_int device, ctypes.c_int iris, ctypes.POINTER(ctypes.c_int) present)
        self.ShamrockIrisIsPresent=wrapper(lib.ShamrockIrisIsPresent)
        #  ctypes.c_uint ShamrockSetIris(ctypes.c_int device, ctypes.c_int iris, ctypes.c_int value)
        self.ShamrockSetIris=wrapper(lib.ShamrockSetIris)
        #  ctypes.c_uint ShamrockGetIris(ctypes.c_int device, ctypes.c_int iris, ctypes.POINTER(ctypes.c_int) value)
        self.ShamrockGetIris=wrapper(lib.ShamrockGetIris)

        #  ctypes.c_uint ShamrockSetFocusMirror(ctypes.c_int device, ctypes.c_int focus)
        self.ShamrockSetFocusMirror=wrapper(lib.ShamrockSetFocusMirror)
        #  ctypes.c_uint ShamrockGetFocusMirror(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) focus)
        self.ShamrockGetFocusMirror=wrapper(lib.ShamrockGetFocusMirror)
        #  ctypes.c_uint ShamrockGetFocusMirrorMaxSteps(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) steps)
        self.ShamrockGetFocusMirrorMaxSteps=wrapper(lib.ShamrockGetFocusMirrorMaxSteps)
        #  ctypes.c_uint ShamrockFocusMirrorReset(ctypes.c_int device)
        self.ShamrockFocusMirrorReset=wrapper(lib.ShamrockFocusMirrorReset)
        #  ctypes.c_uint ShamrockFocusMirrorIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
        self.ShamrockFocusMirrorIsPresent=wrapper(lib.ShamrockFocusMirrorIsPresent)

        #  ctypes.c_uint ShamrockFilterIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
        self.ShamrockFilterIsPresent=wrapper(lib.ShamrockFilterIsPresent)
        #  ctypes.c_uint ShamrockFilterReset(ctypes.c_int device)
        self.ShamrockFilterReset=wrapper(lib.ShamrockFilterReset)
        #  ctypes.c_uint ShamrockGetFilter(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) filter)
        self.ShamrockGetFilter=wrapper(lib.ShamrockGetFilter)
        #  ctypes.c_uint ShamrockSetFilter(ctypes.c_int device, ctypes.c_int filter)
        self.ShamrockSetFilter=wrapper(lib.ShamrockSetFilter)
        #  ctypes.c_uint ShamrockGetFilterInfo(ctypes.c_int device, ctypes.c_int Filter, ctypes.c_char_p Info)
        self.ShamrockGetFilterInfo=wrapper(lib.ShamrockGetFilterInfo)
        #  ctypes.c_uint ShamrockSetFilterInfo(ctypes.c_int device, ctypes.c_int Filter, ctypes.c_char_p Info)
        self.ShamrockSetFilterInfo=wrapper(lib.ShamrockSetFilterInfo)

        #  ctypes.c_uint ShamrockFlipperMirrorIsPresent(ctypes.c_int device, ctypes.c_int flipper, ctypes.POINTER(ctypes.c_int) present)
        self.ShamrockFlipperMirrorIsPresent=wrapper(lib.ShamrockFlipperMirrorIsPresent)
        #  ctypes.c_uint ShamrockFlipperMirrorReset(ctypes.c_int device, ctypes.c_int flipper)
        self.ShamrockFlipperMirrorReset=wrapper(lib.ShamrockFlipperMirrorReset)
        #  ctypes.c_uint ShamrockGetFlipperMirror(ctypes.c_int device, ctypes.c_int flipper, ctypes.POINTER(ctypes.c_int) port)
        self.ShamrockGetFlipperMirror=wrapper(lib.ShamrockGetFlipperMirror)
        #  ctypes.c_uint ShamrockSetFlipperMirror(ctypes.c_int device, ctypes.c_int flipper, ctypes.c_int port)
        self.ShamrockSetFlipperMirror=wrapper(lib.ShamrockSetFlipperMirror)
        #  ctypes.c_uint ShamrockGetCCDLimits(ctypes.c_int device, ctypes.c_int port, ctypes.POINTER(ctypes.c_float) Low, ctypes.POINTER(ctypes.c_float) High)
        self.ShamrockGetCCDLimits=wrapper(lib.ShamrockGetCCDLimits)

        #  ctypes.c_uint ShamrockAccessoryIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
        self.ShamrockAccessoryIsPresent=wrapper(lib.ShamrockAccessoryIsPresent)
        #  ctypes.c_uint ShamrockGetAccessoryState(ctypes.c_int device, ctypes.c_int Accessory, ctypes.POINTER(ctypes.c_int) state)
        self.ShamrockGetAccessoryState=wrapper(lib.ShamrockGetAccessoryState)
        #  ctypes.c_uint ShamrockSetAccessory(ctypes.c_int device, ctypes.c_int Accessory, ctypes.c_int State)
        self.ShamrockSetAccessory=wrapper(lib.ShamrockSetAccessory)

        #  ctypes.c_uint ShamrockGetPixelWidth(ctypes.c_int device, ctypes.POINTER(ctypes.c_float) Width)
        self.ShamrockGetPixelWidth=wrapper(lib.ShamrockGetPixelWidth)
        #  ctypes.c_uint ShamrockSetPixelWidth(ctypes.c_int device, ctypes.c_float Width)
        self.ShamrockSetPixelWidth=wrapper(lib.ShamrockSetPixelWidth)
        #  ctypes.c_uint ShamrockGetNumberPixels(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) NumberPixels)
        self.ShamrockGetNumberPixels=wrapper(lib.ShamrockGetNumberPixels)
        #  ctypes.c_uint ShamrockSetNumberPixels(ctypes.c_int device, ctypes.c_int NumberPixels)
        self.ShamrockSetNumberPixels=wrapper(lib.ShamrockSetNumberPixels)
        #  ctypes.c_uint ShamrockGetCalibration(ctypes.c_int device, ctypes.POINTER(ctypes.c_float) CalibrationValues, ctypes.c_int NumberPixels)
        self.ShamrockGetCalibration_lib=wrapper(lib.ShamrockGetCalibration, rvals=[])

        return

        # ### Deprecated ###
        # #  ctypes.c_uint ShamrockSlitIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
        # self.ShamrockSlitIsPresent=wrapper(lib.ShamrockSlitIsPresent)
        # #  ctypes.c_uint ShamrockSlitReset(ctypes.c_int device)
        # self.ShamrockSlitReset=wrapper(lib.ShamrockSlitReset)
        # #  ctypes.c_uint ShamrockGetSlit(ctypes.c_int device, ctypes.POINTER(ctypes.c_float) width)
        # self.ShamrockGetSlit=wrapper(lib.ShamrockGetSlit)
        # #  ctypes.c_uint ShamrockSetSlit(ctypes.c_int device, ctypes.c_float width)
        # self.ShamrockSetSlit=wrapper(lib.ShamrockSetSlit)
        # #  ctypes.c_uint ShamrockOutputSlitIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
        # self.ShamrockOutputSlitIsPresent=wrapper(lib.ShamrockOutputSlitIsPresent)
        # #  ctypes.c_uint ShamrockOutputSlitReset(ctypes.c_int device)
        # self.ShamrockOutputSlitReset=wrapper(lib.ShamrockOutputSlitReset)
        # #  ctypes.c_uint ShamrockGetOutputSlit(ctypes.c_int device, ctypes.POINTER(ctypes.c_float) width)
        # self.ShamrockGetOutputSlit=wrapper(lib.ShamrockGetOutputSlit)
        # #  ctypes.c_uint ShamrockSetOutputSlit(ctypes.c_int device, ctypes.c_float width)
        # self.ShamrockSetOutputSlit=wrapper(lib.ShamrockSetOutputSlit)
        # #  ctypes.c_uint ShamrockSetSlitCoefficients(ctypes.c_int device, ctypes.c_int x1, ctypes.c_int y1, ctypes.c_int x2, ctypes.c_int y2)
        # self.ShamrockSetSlitCoefficients=wrapper(lib.ShamrockSetSlitCoefficients)
        # #  ctypes.c_uint ShamrockGetSlitCoefficients(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) x1, ctypes.POINTER(ctypes.c_int) y1, ctypes.POINTER(ctypes.c_int) x2, ctypes.POINTER(ctypes.c_int) y2)
        # self.ShamrockGetSlitCoefficients=wrapper(lib.ShamrockGetSlitCoefficients)
        # #  ctypes.c_uint ShamrockFlipperIsPresent(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) present)
        # self.ShamrockFlipperIsPresent=wrapper(lib.ShamrockFlipperIsPresent)
        # #  ctypes.c_uint ShamrockFlipperReset(ctypes.c_int device)
        # self.ShamrockFlipperReset=wrapper(lib.ShamrockFlipperReset)
        # #  ctypes.c_uint ShamrockGetPort(ctypes.c_int device, ctypes.POINTER(ctypes.c_int) port)
        # self.ShamrockGetPort=wrapper(lib.ShamrockGetPort)
        # #  ctypes.c_uint ShamrockSetPort(ctypes.c_int device, ctypes.c_int port)
        # self.ShamrockSetPort=wrapper(lib.ShamrockSetPort)

    def ShamrockGetCalibration(self, device, NumberPixels):
        values=(ctypes.c_float*NumberPixels)()
        self.ShamrockGetCalibration_lib(device,values,NumberPixels)
        return values[:]


wlib=ShamrockLib()