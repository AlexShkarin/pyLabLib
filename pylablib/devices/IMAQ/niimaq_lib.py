# pylint: disable=wrong-spelling-in-comment

from . import niimaq_defs
from .niimaq_defs import IMG_BUFF, IMG_CMD, IMG_TRIG_ACTION  # pylint: disable=unused-import
from .niimaq_defs import IMG_TRIG_POL, IMG_INT_SIG, IMG_TRIG_DRIVE  # pylint: disable=unused-import
from .niimaq_defs import IMG_SIGNAL_STATE, IMG_SIGNAL_TYPE  # pylint: disable=unused-import
from .niimaq_defs import IMG_ERR_CODE, drIMG_ERR_CODE, IMG_ATTR, dIMG_ATTR  # pylint: disable=unused-import
from .niimaq_defs import SESSION_ID, IMG_ERR
from .niimaq_defs import define_functions
from .niimaq_attrtypes import IMG_ATTR_DOUBLE, IMG_ATTR_UINT64, IMG_ATTR_NA  # pylint: disable=unused-import

from ...core.utils import ctypes_wrap, py3
from ...core.devio.comm_backend import DeviceError
from ..utils import load_lib

import ctypes
import struct


class IMAQError(DeviceError):
    """Generic IMAQ error"""
class IMAQLibError(IMAQError):
    """Generic IMAQ library error"""
    def __init__(self, func, code, lib=None):
        self.func=func
        self.code=code
        self.name=drIMG_ERR_CODE.get(self.code,"UNKNOWN")
        self.desc=""
        try:
            if lib is not None:
                self.desc=py3.as_str(lib.imgShowError(code))
        except IMAQLibError:
            pass
        self.msg="function '{}' raised error {}({}): {}".format(func,code,self.name,self.desc)
        IMAQError.__init__(self,self.msg)
def errcheck(passing=None, lib=None):
    """
    Build an error checking function.

    Return a function which checks return codes of IMAQ library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    if passing is None:
        passing={0}
    def errchecker(result, func, arguments):  # pylint: disable=unused-argument
        if result not in passing:
            raise IMAQLibError(func.__name__,result,lib=lib)
        return result
    return errchecker



IMAQ_MAX_API_STRING_LENGTH=512
IMAQ_INF_TIMEOUT=0xFFFFFFFF

class IMAQLib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return
        error_message="The library is automatically supplied with National Instruments NI-IMAQ software\n"+load_lib.par_error_message.format("niimaq")
        self.lib=load_lib.load_lib("imaq.dll",locations=("parameter/niimaq","global"),error_message=error_message,call_conv="stdcall")
        self.clib=load_lib.load_lib("imaq.dll",locations=("parameter/niimaq","global"),error_message=error_message,call_conv="cdecl")
        lib=self.lib
        define_functions(lib)

        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(lib=self))
        strprep=ctypes_wrap.strprep(IMAQ_MAX_API_STRING_LENGTH)

        #  Int32 imgShowError(IMG_ERR error, ctypes.c_char_p text)
        self.imgShowError=wrapper(lib.imgShowError, ["error"], argprep={"text":strprep}, byref=None)

        #  Int32 imgInterfaceQueryNames(uInt32 index, ctypes.c_char_p queryName)
        self.imgInterfaceQueryNames=wrapper(lib.imgInterfaceQueryNames, ["index"], argprep={"queryName":strprep}, byref=None)
        #  Int32 imgInterfaceOpen(ctypes.c_char_p interface_name, ctypes.POINTER(INTERFACE_ID) ifid)
        self.imgInterfaceOpen=wrapper(lib.imgInterfaceOpen, ["interface_name"])
        #  Int32 imgInterfaceReset(INTERFACE_ID ifid)
        self.imgInterfaceReset=wrapper(lib.imgInterfaceReset)
        #  Int32 imgSessionOpen(INTERFACE_ID ifid, ctypes.POINTER(SESSION_ID) sid)
        self.imgSessionOpen=wrapper(lib.imgSessionOpen, ["ifid"])
        #  Int32 imgClose(uInt32 void_id, uInt32 freeResources)
        self.imgClose=wrapper(lib.imgClose)

        #  Int32 imgSessionGetROI(SESSION_ID sid, ctypes.POINTER(uInt32) top, ctypes.POINTER(uInt32) left, ctypes.POINTER(uInt32) height, ctypes.POINTER(uInt32) width)
        self.imgSessionGetROI=wrapper(lib.imgSessionGetROI, ["sid"])
        #  Int32 imgSessionConfigureROI(SESSION_ID sid, uInt32 top, uInt32 left, uInt32 height, uInt32 width)
        self.imgSessionConfigureROI=wrapper(lib.imgSessionConfigureROI)
        #  Int32 imgSessionFitROI(SESSION_ID sid, ctypes.c_int fitMode, uInt32 top, uInt32 left, uInt32 height, uInt32 width, ctypes.POINTER(uInt32) fittedTop, ctypes.POINTER(uInt32) fittedLeft, ctypes.POINTER(uInt32) fittedHeight, ctypes.POINTER(uInt32) fittedWidth)
        self.imgSessionFitROI=wrapper(lib.imgSessionFitROI, ["sid","fitMode","top","left","height","width"])

        #  Int32 imgSessionSerialWrite(SESSION_ID sid, ctypes.c_char_p buffer, ctypes.POINTER(uInt32) bufSize, uInt32 timeout)
        self.imgSessionSerialWrite=wrapper(lib.imgSessionSerialWrite, ["sid","buffer","timeout"],
            argprep={"bufSize":lambda buffer:len(buffer)}, byref=["bufSize"])  # pylint: disable=unnecessary-lambda
        #  Int32 imgSessionSerialRead(SESSION_ID sid, ctypes.c_char_p buffer, ctypes.POINTER(uInt32) bufSize, uInt32 timeout)
        self.imgSessionSerialRead=wrapper(lib.imgSessionSerialRead, ["sid","bufSize","timeout"], ["buffer","bufSize"],
            argprep={"buffer":lambda bufSize:ctypes_wrap.strprep(bufSize+1)()}, byref=["bufSize"])
        #  Int32 imgSessionSerialReadBytes(SESSION_ID sid, ctypes.c_char_p buffer, ctypes.POINTER(uInt32) bufferSize, uInt32 timeout)
        self.imgSessionSerialReadBytes=wrapper(lib.imgSessionSerialReadBytes, ["sid","bufferSize","timeout"], ["buffer","bufferSize"],
            argprep={"buffer":lambda bufferSize:ctypes_wrap.strprep(bufferSize+1)()}, byref=["bufferSize"])
        #  Int32 imgSessionSerialFlush(SESSION_ID sid)
        self.imgSessionSerialFlush=wrapper(lib.imgSessionSerialFlush)        

        #  Int32 imgSnap(SESSION_ID sid, ctypes.POINTER(ctypes.c_void_p) bufAddr)
        self.imgSnap=wrapper(lib.imgSnap, ["sid"], rvals=["bufAddr"])
        #  Int32 imgSnapArea(SESSION_ID sid, ctypes.POINTER(ctypes.c_void_p) bufAddr, uInt32 top, uInt32 left, uInt32 height, uInt32 width, uInt32 rowBytes)
        self.imgSnapArea=wrapper(lib.imgSnapArea, rvals=["bufAddr"])
        #  Int32 imgGrabSetup(SESSION_ID sid, uInt32 startNow)
        self.imgGrabSetup=wrapper(lib.imgGrabSetup)
        #  Int32 imgGrab(SESSION_ID sid, ctypes.POINTER(ctypes.c_void_p) bufPtr, uInt32 syncOnVB)
        self.imgGrab=wrapper(lib.imgGrab, ["sid","syncOnVB"])
        #  Int32 imgGrabArea(SESSION_ID sid, ctypes.POINTER(ctypes.c_void_p) bufPtr, uInt32 syncOnVB, uInt32 top, uInt32 left, uInt32 height, uInt32 width, uInt32 rowBytes)
        self.imgGrabArea=wrapper(lib.imgGrabArea, rvals=["bufPtr"])
        #  Int32 imgSessionGetBufferSize(SESSION_ID sid, ctypes.POINTER(uInt32) sizeNeeded)
        self.imgSessionGetBufferSize=wrapper(lib.imgSessionGetBufferSize, ["sid"])

        #  Int32 imgCreateBuffer(SESSION_ID sid, uInt32 where, uInt32 bufferSize, ctypes.POINTER(ctypes.c_void_p) bufAddr)
        self.imgCreateBuffer=wrapper(lib.imgCreateBuffer, rvals=["bufAddr"])
        #  Int32 imgDisposeBuffer(ctypes.c_void_p bufferPtr)
        self.imgDisposeBuffer=wrapper(lib.imgDisposeBuffer)
        #  Int32 imgSessionClearBuffer(SESSION_ID sid, uInt32 buf_num, uInt8 pixel_value)
        self.imgSessionClearBuffer=wrapper(lib.imgSessionClearBuffer)
        #  Int32 imgCreateBufList(uInt32 numElements, ctypes.POINTER(BUFLIST_ID) bufListId)
        self.imgCreateBufList=wrapper(lib.imgCreateBufList, ["numElements"])
        #  Int32 imgDisposeBufList(BUFLIST_ID bid, uInt32 freeResources)
        self.imgDisposeBufList=wrapper(lib.imgDisposeBufList)
        #  Int32 imgGetBufferElement(BUFLIST_ID bid, uInt32 element, uInt32 itemType, ctypes.c_void_p itemValue)
        self.imgGetBufferElement=wrapper(lib.imgGetBufferElement)
        #  Int32 imgSetBufferElement2(BUFLIST_ID bid, uInt32 element, uInt32 itemType, ...)
        self.imgSetBufferElement2=self.clib.imgSetBufferElement2
        self.imgSetBufferElement2.errcheck=errcheck(lib=self)

        #  Int32 imgRingSetup(SESSION_ID sid, uInt32 numberBuffer, ctypes.POINTER(ctypes.c_void_p) bufferList, uInt32 skipCount, uInt32 startnow)
        self.imgRingSetup=wrapper(lib.imgRingSetup)
        #  Int32 imgSequenceSetup(SESSION_ID sid, uInt32 numberBuffer, ctypes.POINTER(ctypes.c_void_p) bufferList, ctypes.POINTER(uInt32) skipCount, uInt32 startnow, uInt32 async)
        self.imgSequenceSetup=wrapper(lib.imgSequenceSetup,alias={"async":"run_async"})
        #  Int32 imgSessionStartAcquisition(SESSION_ID sid)
        self.imgSessionStartAcquisition=wrapper(lib.imgSessionStartAcquisition)
        #  Int32 imgSessionStopAcquisition(SESSION_ID sid)
        self.imgSessionStopAcquisition=wrapper(lib.imgSessionStopAcquisition)
        #  Int32 imgSessionConfigure(SESSION_ID sid, BUFLIST_ID buflist)
        self.imgSessionConfigure=wrapper(lib.imgSessionConfigure)
        #  Int32 imgSessionAcquire(SESSION_ID sid, uInt32 async, CALL_BACK_PTR callback)
        self.imgSessionAcquire=wrapper(lib.imgSessionAcquire,alias={"async":"run_async"})
        #  Int32 imgSessionStatus(SESSION_ID sid, ctypes.POINTER(uInt32) boardStatus, ctypes.POINTER(uInt32) bufIndex)
        self.imgSessionStatus=wrapper(lib.imgSessionStatus,["sid"])
        #  Int32 imgSessionAbort(SESSION_ID sid, ctypes.POINTER(uInt32) bufNum)
        self.imgSessionAbort=wrapper(lib.imgSessionAbort,["sid"])

        #  Int32 imgSessionExamineBuffer2(SESSION_ID sid, uInt32 whichBuffer, ctypes.POINTER(uInt32) bufferNumber, ctypes.POINTER(ctypes.c_void_p) bufferAddr)
        self.imgSessionExamineBuffer2=wrapper(lib.imgSessionExamineBuffer2, ["sid","whichBuffer"])
        #  Int32 imgSessionReleaseBuffer(SESSION_ID sid)
        self.imgSessionReleaseBuffer=wrapper(lib.imgSessionReleaseBuffer)

        #  Int32 imgGetAttribute(uInt32 void_id, uInt32 attribute, ctypes.c_void_p value)
        self.imgGetAttribute=wrapper(lib.imgGetAttribute)
        #  Int32 imgSetAttribute2(uInt32 void_id, uInt32 attribute, ...)
        self.imgSetAttribute2=self.clib.imgSetAttribute2
        self.imgSetAttribute2.errcheck=errcheck(lib=self)
        #  Int32 imgSetAttributeFromVoidPtr(uInt32 void_id, uInt32 attribute, ctypes.c_void_p valuePtr)
        self.imgSetAttributeFromVoidPtr=wrapper(lib.imgSetAttributeFromVoidPtr)
        #  Int32 imgGetCameraAttributeNumeric(SESSION_ID sid, ctypes.c_char_p attributeString, ctypes.POINTER(ctypes.c_double) currentValueNumeric)
        self.imgGetCameraAttributeNumeric=wrapper(lib.imgGetCameraAttributeNumeric, ["sid","attributeString"])
        #  Int32 imgSetCameraAttributeNumeric(SESSION_ID sid, ctypes.c_char_p attributeString, ctypes.c_double newValueNumeric)
        self.imgSetCameraAttributeNumeric=wrapper(lib.imgSetCameraAttributeNumeric)
        #  Int32 imgGetCameraAttributeString(SESSION_ID sid, ctypes.c_char_p attributeString, ctypes.c_char_p currentValueString, uInt32 sizeofCurrentValueString)
        self.imgGetCameraAttributeString=wrapper(lib.imgGetCameraAttributeString, ["sid","attributeString"],
            argprep={"currentValueString":strprep,"sizeofCurrentValueString":IMAQ_MAX_API_STRING_LENGTH}, byref=None)
        #  Int32 imgSetCameraAttributeString(SESSION_ID sid, ctypes.c_char_p attributeString, ctypes.c_char_p newValueString)
        self.imgSetCameraAttributeString=wrapper(lib.imgSetCameraAttributeString)

        #  Int32 imgSessionWaitSignal2(SESSION_ID sid, ctypes.c_int signalType, uInt32 signalIdentifier, uInt32 signalPolarity, uInt32 timeout)
        self.imgSessionWaitSignal2=wrapper(lib.imgSessionWaitSignal2)
        # typedef  uInt32 (NI_CDECL * CALL_BACK_PTR2)(SESSION_ID boardid, IMG_ERR err, IMG_SIGNAL_TYPE signalType, uInt32 signalIdentifier, void* data);
        self.c_callback=ctypes.WINFUNCTYPE(ctypes.c_uint32,SESSION_ID,IMG_ERR,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p)
        #  Int32 imgSessionWaitSignalAsync2(SESSION_ID sid, ctypes.c_int signalType, uInt32 signalIdentifier, uInt32 signalPolarity, CALL_BACK_PTR2 funcptr, ctypes.c_void_p callbackData)
        self.imgSessionWaitSignalAsync2=wrapper(lib.imgSessionWaitSignalAsync2)
        
        #  Int32 imgSessionTriggerConfigure2(SESSION_ID sid, ctypes.c_int trigType, uInt32 trigNum, uInt32 polarity, uInt32 timeout, uInt32 action)
        self.imgSessionTriggerConfigure2=wrapper(lib.imgSessionTriggerConfigure2)
        #  Int32 imgSessionTriggerDrive2(SESSION_ID sid, ctypes.c_int trigType, uInt32 trigNum, uInt32 polarity, uInt32 signal)
        self.imgSessionTriggerDrive2=wrapper(lib.imgSessionTriggerDrive2)
        #  Int32 imgSessionLineTrigSource2(SESSION_ID sid, ctypes.c_int trigType, uInt32 trigNum, uInt32 polarity, uInt32 skip)
        self.imgSessionLineTrigSource2=wrapper(lib.imgSessionLineTrigSource2)
        #  Int32 imgSessionTriggerRead2(SESSION_ID sid, ctypes.c_int trigType, uInt32 trigNum, uInt32 polarity, ctypes.POINTER(uInt32) status)
        self.imgSessionTriggerRead2=wrapper(lib.imgSessionTriggerRead2, rvals=["status"])
        #  Int32 imgSessionTriggerRoute2(SESSION_ID sid, ctypes.c_int srcTriggerType, uInt32 srcTriggerNumber, ctypes.c_int dstTriggerType, uInt32 dstTriggerNumber)
        self.imgSessionTriggerRoute2=wrapper(lib.imgSessionTriggerRoute2)
        #  Int32 imgSessionTriggerClear(SESSION_ID sid)
        self.imgSessionTriggerClear=wrapper(lib.imgSessionTriggerClear)
        #  Int32 imgPulseCreate2(uInt32 timeBase, uInt32 delay, uInt32 width, ctypes.c_int signalType, uInt32 signalIdentifier, uInt32 signalPolarity, ctypes.c_int outputType, uInt32 outputNumber, uInt32 outputPolarity, uInt32 pulseMode, ctypes.POINTER(PULSE_ID) plsID)
        self.imgPulseCreate2=wrapper(lib.imgPulseCreate2, rvals=["plsID"])
        #  Int32 imgPulseDispose(PULSE_ID plsID)
        self.imgPulseDispose=wrapper(lib.imgPulseDispose)
        #  Int32 imgPulseRate(ctypes.c_double delaytime, ctypes.c_double widthtime, ctypes.POINTER(uInt32) delay, ctypes.POINTER(uInt32) width, ctypes.POINTER(uInt32) timebase)
        self.imgPulseRate=wrapper(lib.imgPulseRate, rvals=["delay","width","timebase"])
        #  Int32 imgPulseStart(PULSE_ID pid, SESSION_ID sid)
        self.imgPulseStart=wrapper(lib.imgPulseStart)
        #  Int32 imgPulseUpdate(PULSE_ID pid, SESSION_ID sid, uInt32 delay, uInt32 width)
        self.imgPulseUpdate=wrapper(lib.imgPulseUpdate)
        #  Int32 imgPulseStop(PULSE_ID pid)
        self.imgPulseStop=wrapper(lib.imgPulseStop)
        #  Int32 imgEncoderResetPosition(SESSION_ID sid)
        self.imgEncoderResetPosition=wrapper(lib.imgEncoderResetPosition)

        #  Int32 imgBayerColorDecode(ctypes.c_void_p dst, ctypes.c_void_p src, uInt32 rows, uInt32 cols, uInt32 dstRowPixels, uInt32 srcRowPixels, ctypes.POINTER(uInt32) redLUT, ctypes.POINTER(uInt32) greenLUT, ctypes.POINTER(uInt32) blueLUT, uInt8 bayerPattern, uInt32 bitDepth, uInt32 reserved)
        self.imgBayerColorDecode=wrapper(lib.imgBayerColorDecode, argprep={"reserved":0})
        #  Int32 imgCalculateBayerColorLUT(ctypes.c_double redGain, ctypes.c_double greenGain, ctypes.c_double blueGain, ctypes.POINTER(uInt32) redLUT, ctypes.POINTER(uInt32) greenLUT, ctypes.POINTER(uInt32) blueLUT, uInt32 bitDepth)
        self.imgCalculateBayerColorLUT_lib=wrapper(lib.imgCalculateBayerColorLUT)


        self._initialized=True

    def imgGetAttribute_buff(self, sid, attr, size=32):
        buff=ctypes.create_string_buffer(size)
        self.imgGetAttribute(sid,attr,ctypes.addressof(buff))
        return buff
    # Allocate a relatively large buffer to avoid out-of-bounds writes leading to crashes, if the type is chosen incorrectly
    def imgGetAttribute_uint32(self, sid, attr):
        value=self.imgGetAttribute_buff(sid,attr)
        return struct.unpack("I",value[:4])[0]
    def imgGetAttribute_uint64(self, sid, attr):
        value=self.imgGetAttribute_buff(sid,attr)
        return struct.unpack("Q",value[:8])[0]
    def imgGetAttribute_double(self, sid, attr):
        value=self.imgGetAttribute_buff(sid,attr)
        return struct.unpack("d",value[:8])[0]
    def imgSetAttribute2_uint32(self, sid, attr, value):
        self.imgSetAttribute2(ctypes.c_uint(sid),ctypes.c_uint(attr),ctypes.c_uint32(int(value)))
    def imgSetAttribute2_uint64(self, sid, attr, value):
        self.imgSetAttribute2(ctypes.c_uint(sid),ctypes.c_uint(attr),ctypes.c_uint64(int(value)))
    def imgSetAttribute2_double(self, sid, attr, value):
        self.imgSetAttribute2(ctypes.c_uint(sid),ctypes.c_uint(attr),ctypes.c_double(float(value)))
    def imgSetBufferElement2_uint32(self, bid, element, itemType, value):
        self.imgSetBufferElement2(ctypes.c_uint(bid),ctypes.c_uint(element),ctypes.c_uint(itemType),ctypes.c_uint32(int(value)))
    
    def imgCalculateBayerColorLUT(self, redGain, greenGain, blueGain, bitDepth):
        nel=2**8 if bitDepth<=8 else 2**16
        lut_buffprep=ctypes_wrap.strprep(4*nel,ctype=ctypes.POINTER(niimaq_defs.uInt32))
        redLUT=lut_buffprep()
        greenLUT=lut_buffprep()
        blueLUT=lut_buffprep()
        self.imgCalculateBayerColorLUT_lib(redGain,greenGain,blueGain,redLUT,greenLUT,blueLUT,bitDepth)
        return redLUT,greenLUT,blueLUT


wlib=IMAQLib()