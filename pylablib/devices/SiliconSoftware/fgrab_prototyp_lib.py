# pylint: disable=wrong-spelling-in-comment

from .fgrab_define_defs import FG_STATUS, drFG_STATUS, FG_PARAM
from .fgrab_prototyp_defs import FgParamTypes, FgProperty
from .fgrab_prototyp_defs import define_functions

from ...core.utils import ctypes_wrap, functions as func_utils
from ...core.devio.comm_backend import DeviceError
from ..utils import load_lib

import ctypes


class SiliconSoftwareError(DeviceError):
    """Generic Silicon Software error"""
class SIFgrabLibError(SiliconSoftwareError):
    """Generic SiliconSoftware frame grabber library error"""
    def __init__(self, func, code, desc=""):
        self.func=func
        self.code=code
        self.name=drFG_STATUS.get(self.code,"UNKNOWN")
        self.desc=desc
        self.msg="function '{}' raised error {}({}): {}".format(func,code,self.name,self.desc)
        super().__init__(self.msg)
def last_error_desc(lib, s=None):
    code=lib.Fg_getLastErrorNumber(s)
    desc=lib.Fg_getLastErrorDescription(s)
    return code,desc
def errcheck(lib, check=None, sarg=0):
    """
    Build an error checking function.

    If `check` is not ``True``, it can be an additional checking method taking the result and the arguments;
    otherwise, any result always passes.
    `sarg` is the position of the frame grabber struct argument, which is used to get the error code and description.
    """
    def errchecker(result, func, arguments):
        s=None if sarg is None else arguments[sarg]
        if check is not None:
            valid=func_utils.call_cut_args(check,result,*arguments)
        else:
            valid=True
        if not valid:
            code,desc=last_error_desc(lib,s)
            raise SIFgrabLibError(func.__name__,code=code,desc=desc)
        return result
    return errchecker



# frameindex_t=ctypes.c_int32 if platform.architecture()[0]=="32bit" else ctypes.c_int64 # TODO: implement in defa



class SIFgrabLib:

    def __init__(self):
        self._initialized=False


    def initlib(self):
        if self._initialized:
            return
        error_message="The library is automatically supplied with Silicon Software Runtime software\n"+load_lib.par_error_message.format("sisofgrab")
        self.lib=load_lib.load_lib("fglib5.dll",locations=("parameter/sisofgrab","global"),error_message=error_message,call_conv="cdecl")
        lib=self.lib
        define_functions(lib)

        max_applet_name_length=1024
        apstrprep=ctypes_wrap.strprep(max_applet_name_length)
        wrapper=ctypes_wrap.CFunctionWrapper()
        wrapper_rz=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(lib,check=lambda v:v==0))
        wrapper_rnz=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(lib,check=lambda v:bool(v)))  # pylint: disable=unnecessary-lambda
        wrapper_rgez=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(lib,check=lambda v:v>=0))
        wrapper_init_rnz=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(lib,check=lambda v:bool(v),sarg=None))  # pylint: disable=unnecessary-lambda
        wrapper_init_rgez=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(lib,check=lambda v:v>=0,sarg=None))
        
        #  ctypes.c_int Fg_getLastErrorNumber(ctypes.c_void_p Fg)
        self.Fg_getLastErrorNumber=wrapper(lib.Fg_getLastErrorNumber)
        #  ctypes.c_char_p getErrorDescription(ctypes.c_int ErrorNumber)
        self.getErrorDescription=wrapper(lib.getErrorDescription)
        #  ctypes.c_char_p Fg_getErrorDescription(ctypes.c_void_p Fg, ctypes.c_int ErrorNumber)
        self.Fg_getErrorDescription=wrapper(lib.Fg_getErrorDescription)
        #  ctypes.c_char_p Fg_getLastErrorDescription(ctypes.c_void_p Fg)
        self.Fg_getLastErrorDescription=wrapper(lib.Fg_getLastErrorDescription)
        
        # Optional methods #
        #  ctypes.c_int Fg_InitLibraries(ctypes.c_char_p sisoDir)
        self.Fg_InitLibraries=wrapper_rnz(lib.Fg_InitLibraries)
        #  ctypes.c_int Fg_InitLibrariesEx(ctypes.c_char_p sisoDir, ctypes.c_uint flags, ctypes.c_char_p id, ctypes.c_uint timeout)
        self.Fg_InitLibrariesEx=wrapper_rnz(lib.Fg_InitLibrariesEx)
        #  None Fg_AbortInitLibraries()
        self.Fg_AbortInitLibraries=wrapper(lib.Fg_AbortInitLibraries)
        #  None Fg_InitLibrariesStartNextSlave()
        self.Fg_InitLibrariesStartNextSlave=wrapper(lib.Fg_InitLibrariesStartNextSlave)
        #  None Fg_FreeLibraries()
        self.Fg_FreeLibraries=wrapper(lib.Fg_FreeLibraries)

        #  ctypes.c_int Fg_getAppletIterator(ctypes.c_int boardIndex, ctypes.c_int src, ctypes.POINTER(Fg_AppletIteratorType) iter, ctypes.c_int flags)
        self.Fg_getAppletIterator=wrapper_init_rgez(lib.Fg_getAppletIterator, rvals=[None,"iter"])
        #  ctypes.c_int Fg_freeAppletIterator(Fg_AppletIteratorType iter)
        self.Fg_freeAppletIterator=wrapper_rz(lib.Fg_freeAppletIterator)
        #  Fg_AppletIteratorItem Fg_getAppletIteratorItem(Fg_AppletIteratorType iter, ctypes.c_int index)
        self.Fg_getAppletIteratorItem=wrapper_rnz(lib.Fg_getAppletIteratorItem)
        #  ctypes.c_int64 Fg_getAppletIntProperty(Fg_AppletIteratorItem item, ctypes.c_int property)
        self.Fg_getAppletIntProperty=wrapper(lib.Fg_getAppletIntProperty)
        #  ctypes.c_char_p Fg_getAppletStringProperty(Fg_AppletIteratorItem item, ctypes.c_int property)
        self.Fg_getAppletStringProperty=wrapper(lib.Fg_getAppletStringProperty)
        #  Fg_AppletIteratorItem Fg_findAppletIteratorItem(Fg_AppletIteratorType iter, ctypes.c_char_p path)
        self.Fg_findAppletIteratorItem=wrapper_rnz(lib.Fg_findAppletIteratorItem)
        #  Fg_AppletIteratorItem Fg_addAppletIteratorItem(Fg_AppletIteratorType iter, ctypes.c_char_p path, ctypes.POINTER(ctypes.c_int) numItems)
        self.Fg_addAppletIteratorItem=wrapper_rnz(lib.Fg_addAppletIteratorItem)
        #  ctypes.c_int Fg_findApplet(ctypes.c_uint BoardIndex, ctypes.c_char_p Path, ctypes.c_size_t Size)
        self.Fg_findApplet=wrapper(lib.Fg_findApplet, argprep={"Path":apstrprep,"Size":max_applet_name_length}, byref=None)
        
        #  ctypes.c_char_p Fg_getSWVersion()
        self.Fg_getSWVersion=wrapper(lib.Fg_getSWVersion)
        #  ctypes.c_int Fg_getBoardType(ctypes.c_int BoardIndex)
        self.Fg_getBoardType=wrapper_init_rgez(lib.Fg_getBoardType)
        #  ctypes.c_uint Fg_getSerialNumber(ctypes.c_void_p Fg)
        self.Fg_getSerialNumber=wrapper(lib.Fg_getSerialNumber)
        #  ctypes.c_int Fg_getAppletId(ctypes.c_void_p Fg, ctypes.c_char_p ignored)
        self.Fg_getAppletId=wrapper(lib.Fg_getAppletId, args=["Fg"], rvals=[None])
        #  ctypes.c_char_p Fg_getAppletVersion(ctypes.c_void_p Fg, ctypes.c_int AppletId)
        self.Fg_getAppletVersion=wrapper(lib.Fg_getAppletVersion)
        #  ctypes.c_char_p Fg_getBoardNameByType(ctypes.c_int BoardType, ctypes.c_int UseShortName)
        self.Fg_getBoardNameByType=wrapper_init_rnz(lib.Fg_getBoardNameByType)
        #  ctypes.c_int Fg_getSystemInformation(ctypes.c_void_p Fg, ctypes.c_int selector, ctypes.c_int propertyId, ctypes.c_int param1, ctypes.c_void_p buffer, ctypes.POINTER(ctypes.c_uint) bufLen)
        self.Fg_getSystemInformation_lib=wrapper_rz(lib.Fg_getSystemInformation, args="all", rvals=["bufLen"])

        
        #  ctypes.c_void_p Fg_Init(ctypes.c_char_p FileName, ctypes.c_uint BoardIndex)
        self.Fg_Init=wrapper_init_rnz(lib.Fg_Init)
        #  ctypes.c_void_p Fg_InitConfig(ctypes.c_char_p Config_Name, ctypes.c_uint BoardIndex)
        self.Fg_InitEx=wrapper_init_rnz(lib.Fg_InitEx)
        #  ctypes.c_void_p Fg_InitConfigEx(ctypes.c_char_p Config_Name, ctypes.c_uint BoardIndex, ctypes.c_int flags)
        self.Fg_InitConfig=wrapper_init_rnz(lib.Fg_InitConfig)
        #  ctypes.c_void_p Fg_InitEx(ctypes.c_char_p FileName, ctypes.c_uint BoardIndex, ctypes.c_int flags)
        self.Fg_InitConfigEx=wrapper_init_rnz(lib.Fg_InitConfigEx)
        #  ctypes.c_int Fg_FreeGrabber(ctypes.c_void_p Fg)
        self.Fg_FreeGrabber=wrapper_rz(lib.Fg_FreeGrabber)
        #  ctypes.c_int Fg_loadConfig(ctypes.c_void_p Fg, ctypes.c_char_p Filename)
        self.Fg_loadConfig=wrapper_rz(lib.Fg_loadConfig)
        #  ctypes.c_int Fg_saveConfig(ctypes.c_void_p Fg, ctypes.c_char_p Filename)
        self.Fg_saveConfig=wrapper_rz(lib.Fg_saveConfig)

        #  ctypes.c_int Fg_getNrOfParameter(ctypes.c_void_p Fg)
        self.Fg_getNrOfParameter=wrapper_rgez(lib.Fg_getNrOfParameter)
        #  ctypes.c_int Fg_getParameterId(ctypes.c_void_p fg, ctypes.c_int index)
        self.Fg_getParameterId=wrapper_rgez(lib.Fg_getParameterId)
        #  ctypes.c_char_p Fg_getParameterName(ctypes.c_void_p fg, ctypes.c_int index)
        self.Fg_getParameterName=wrapper_rnz(lib.Fg_getParameterName)
        #  ctypes.c_int Fg_getParameterIdByName(ctypes.c_void_p fg, ctypes.c_char_p name)
        self.Fg_getParameterIdByName=wrapper_rgez(lib.Fg_getParameterIdByName)
        #  ctypes.c_char_p Fg_getParameterNameById(ctypes.c_void_p fg, ctypes.c_uint id, ctypes.c_uint dma)
        self.Fg_getParameterNameById=wrapper_rnz(lib.Fg_getParameterNameById)
        
        #  ctypes.c_int Fg_setParameter(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_void_p Value, ctypes.c_uint DmaIndex)
        self.Fg_setParameter=wrapper_rz(lib.Fg_setParameter, byref=["Value"])
        #  ctypes.c_int Fg_setParameterWithType(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_void_p Value, ctypes.c_uint DmaIndex, ctypes.c_int type)
        self.Fg_setParameterWithType=wrapper_rz(lib.Fg_setParameterWithType, byref=["Value"])
        #  ctypes.c_int Fg_getParameter(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_void_p Value, ctypes.c_uint DmaIndex)
        self.Fg_getParameter=wrapper_rz(lib.Fg_getParameter)
        #  ctypes.c_int Fg_getParameterWithType(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_void_p Value, ctypes.c_uint DmaIndex, ctypes.c_int type)
        self.Fg_getParameterWithType=wrapper_rz(lib.Fg_getParameterWithType)
        #  ctypes.c_int Fg_freeParameterStringWithType(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_void_p Value, ctypes.c_uint DmaIndex, ctypes.c_int type)
        self.Fg_freeParameterStringWithType=wrapper(lib.Fg_freeParameterStringWithType)
        #  ctypes.c_int Fg_getParameterEx(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_void_p Value, ctypes.c_uint DmaIndex, ctypes.c_void_p pMem, frameindex_t ImgNr)
        self.Fg_getParameterEx=wrapper_rz(lib.Fg_getParameterEx)
        #  ctypes.c_int Fg_getParameterProperty(ctypes.c_void_p Fg, ctypes.c_int parameterId, ctypes.c_int propertyId, ctypes.c_void_p buffer, ctypes.POINTER(ctypes.c_int) bufLen)
        self.Fg_getParameterProperty_lib=wrapper_rz(lib.Fg_getParameterProperty, args="all", rvals=["bufLen"])
        #  ctypes.c_int Fg_getParameterPropertyEx(ctypes.c_void_p Fg, ctypes.c_int parameterId, ctypes.c_int propertyId, ctypes.c_int DmaIndex, ctypes.c_void_p buffer, ctypes.POINTER(ctypes.c_int) bufLen)
        self.Fg_getParameterPropertyEx_lib=wrapper_rz(lib.Fg_getParameterPropertyEx, args="all", rvals=["bufLen"])
        #  ctypes.c_int Fg_getParameterInfoXML(ctypes.c_void_p Fg, ctypes.c_int port, ctypes.c_char_p infoBuffer, ctypes.POINTER(ctypes.c_size_t) infoBufferSize)
        self.Fg_getParameterInfoXML_lib=wrapper_rz(lib.Fg_getParameterInfoXML, args="all", rvals=["infoBufferSize"])
        #  ctypes.c_int Fg_getBitsPerPixel(ctypes.c_int format)
        self.Fg_getBitsPerPixel=wrapper_rgez(lib.Fg_getBitsPerPixel)
        
        #  frameindex_t Fg_getStatus(ctypes.c_void_p Fg, ctypes.c_int Param, frameindex_t Data, ctypes.c_uint DmaIndex)
        self.Fg_getStatus=wrapper_rgez(lib.Fg_getStatus)
        #  frameindex_t Fg_getStatusEx(ctypes.c_void_p Fg, ctypes.c_int Param, frameindex_t Data, ctypes.c_uint DmaIndex, ctypes.c_void_p pMem)
        self.Fg_getStatusEx=wrapper_rgez(lib.Fg_getStatusEx)
        #  ctypes.c_int Fg_setStatus(ctypes.c_void_p Fg, ctypes.c_int Param, frameindex_t Data, ctypes.c_uint DmaIndex)
        self.Fg_setStatus=wrapper_rgez(lib.Fg_setStatus)
        #  ctypes.c_int Fg_setStatusEx(ctypes.c_void_p Fg, ctypes.c_int Param, frameindex_t Data, ctypes.c_uint DmaIndex, ctypes.c_void_p pMem)
        self.Fg_setStatusEx=wrapper_rgez(lib.Fg_setStatusEx)
        
        #  ctypes.c_void_p Fg_AllocMem(ctypes.c_void_p Fg, ctypes.c_size_t Size, frameindex_t BufCnt, ctypes.c_uint DmaIndex)
        self.Fg_AllocMem=wrapper_rnz(lib.Fg_AllocMem)
        #  ctypes.c_void_p Fg_AllocMemEx(ctypes.c_void_p Fg, ctypes.c_size_t Size, frameindex_t BufCnt)
        self.Fg_AllocMemEx=wrapper_rnz(lib.Fg_AllocMemEx)
        #  ctypes.c_int Fg_FreeMem(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex)
        self.Fg_FreeMem=wrapper_rz(lib.Fg_FreeMem)
        #  ctypes.c_int Fg_FreeMemEx(ctypes.c_void_p Fg, ctypes.c_void_p mem)
        self.Fg_FreeMemEx=wrapper_rz(lib.Fg_FreeMemEx)
        #  ctypes.c_void_p Fg_AllocMemHead(ctypes.c_void_p Fg, ctypes.c_size_t Size, frameindex_t BufCnt)
        self.Fg_AllocMemHead=wrapper_rnz(lib.Fg_AllocMemHead)
        #  ctypes.c_int Fg_FreeMemHead(ctypes.c_void_p Fg, ctypes.c_void_p memHandle)
        self.Fg_FreeMemHead=wrapper_rz(lib.Fg_FreeMemHead)
        #  ctypes.c_int Fg_AddMem(ctypes.c_void_p Fg, ctypes.c_void_p pBuffer, ctypes.c_size_t Size, frameindex_t bufferIndex, ctypes.c_void_p memHandle)
        self.Fg_AddMem=wrapper_rgez(lib.Fg_AddMem)
        #  ctypes.c_int Fg_DelMem(ctypes.c_void_p Fg, ctypes.c_void_p memHandle, frameindex_t bufferIndex)
        self.Fg_DelMem=wrapper_rz(lib.Fg_DelMem)
        
        #  ctypes.c_int Fg_Acquire(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex, frameindex_t PicCount)
        self.Fg_Acquire=wrapper_rz(lib.Fg_Acquire)
        #  ctypes.c_int Fg_AcquireEx(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex, frameindex_t PicCount, ctypes.c_int nFlag, ctypes.c_void_p memHandle)
        self.Fg_AcquireEx=wrapper_rz(lib.Fg_AcquireEx)
        #  ctypes.c_int Fg_stopAcquire(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex)
        self.Fg_stopAcquire=wrapper_rz(lib.Fg_stopAcquire)
        #  ctypes.c_int Fg_stopAcquireEx(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex, ctypes.c_void_p memHandle, ctypes.c_int nFlag)
        self.Fg_stopAcquireEx=wrapper_rz(lib.Fg_stopAcquireEx)
        #  frameindex_t Fg_getLastPicNumberBlocking(ctypes.c_void_p Fg, frameindex_t PicNr, ctypes.c_uint DmaIndex, ctypes.c_int Timeout)
        self.Fg_getLastPicNumberBlocking=wrapper_rgez(lib.Fg_getLastPicNumberBlocking)
        #  frameindex_t Fg_getLastPicNumber(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex)
        self.Fg_getLastPicNumber=wrapper_rgez(lib.Fg_getLastPicNumber)
        #  frameindex_t Fg_getLastPicNumberBlockingEx(ctypes.c_void_p Fg, frameindex_t PicNr, ctypes.c_uint DmaIndex, ctypes.c_int Timeout, ctypes.c_void_p pMem)
        self.Fg_getLastPicNumberBlockingEx=wrapper_rgez(lib.Fg_getLastPicNumberBlockingEx)
        #  frameindex_t Fg_getLastPicNumberEx(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex, ctypes.c_void_p pMem)
        self.Fg_getLastPicNumberEx=wrapper_rgez(lib.Fg_getLastPicNumberEx)
        #  ctypes.c_void_p Fg_getImagePtr(ctypes.c_void_p Fg, frameindex_t PicNr, ctypes.c_uint DmaIndex)
        self.Fg_getImagePtr=wrapper_rnz(lib.Fg_getImagePtr)
        #  ctypes.c_void_p Fg_getImagePtrEx(ctypes.c_void_p Fg, frameindex_t PicNr, ctypes.c_uint DmaIndex, ctypes.c_void_p pMem)
        self.Fg_getImagePtrEx=wrapper_rnz(lib.Fg_getImagePtrEx)
        #  frameindex_t Fg_getImage(ctypes.c_void_p Fg, ctypes.c_int Param, frameindex_t PicNr, ctypes.c_uint DmaIndex, ctypes.c_uint Timeout)
        self.Fg_getImage=wrapper_rgez(lib.Fg_getImage)
        #  frameindex_t Fg_getImageEx(ctypes.c_void_p Fg, ctypes.c_int Param, frameindex_t PicNr, ctypes.c_uint DmaIndex, ctypes.c_uint Timeout, ctypes.c_void_p pMem)
        self.Fg_getImageEx=wrapper_rgez(lib.Fg_getImageEx)
        
        #  ctypes.c_int Fg_sendSoftwareTrigger(ctypes.c_void_p Fg, ctypes.c_uint CamPort)
        self.Fg_sendSoftwareTrigger=wrapper_rz(lib.Fg_sendSoftwareTrigger)
        #  ctypes.c_int Fg_sendSoftwareTriggerEx(ctypes.c_void_p Fg, ctypes.c_uint CamPort, ctypes.c_uint Triggers)
        self.Fg_sendSoftwareTriggerEx=wrapper_rz(lib.Fg_sendSoftwareTriggerEx)
        #  ctypes.c_int Fg_setExsync(ctypes.c_void_p Fg, ctypes.c_int Flag, ctypes.c_uint CamPort)
        self.Fg_setExsync=wrapper_rgez(lib.Fg_setExsync)
        #  ctypes.c_int Fg_setFlash(ctypes.c_void_p Fg, ctypes.c_int Flag, ctypes.c_uint CamPort)
        self.Fg_setFlash=wrapper_rgez(lib.Fg_setFlash)
        
        #  ctypes.c_void_p Fg_NumaAllocDmaBuffer(ctypes.c_void_p Fg, ctypes.c_size_t Size)
        self.Fg_NumaAllocDmaBuffer=wrapper_rnz(lib.Fg_NumaAllocDmaBuffer)
        #  ctypes.c_int Fg_NumaFreeDmaBuffer(ctypes.c_void_p Fg, ctypes.c_void_p Buffer)
        self.Fg_NumaFreeDmaBuffer=wrapper_rz(lib.Fg_NumaFreeDmaBuffer)
        #  ctypes.c_int Fg_NumaPinThread(ctypes.c_void_p Fg)
        self.Fg_NumaPinThread=wrapper_rz(lib.Fg_NumaPinThread)
        
        #  ctypes.c_int Fg_readUserDataArea(ctypes.c_void_p Fg, ctypes.c_int boardId, ctypes.c_uint offs, ctypes.c_uint size, ctypes.c_void_p buffer)
        self.Fg_readUserDataArea=wrapper_rz(lib.Fg_readUserDataArea)
        #  ctypes.c_int Fg_writeUserDataArea(ctypes.c_void_p Fg, ctypes.c_int boardId, ctypes.c_uint offs, ctypes.c_uint size, ctypes.c_void_p buffer)
        self.Fg_writeUserDataArea=wrapper_rz(lib.Fg_writeUserDataArea)
        

        self._initialized=True


        ## Applet-related ##
        # #  ctypes.c_int Fg_sendImage(ctypes.c_void_p Fg, frameindex_t startImage, frameindex_t PicCount, ctypes.c_int nFlag, ctypes.c_uint DmaIndex)
        # self.Fg_sendImage=wrapper(lib.Fg_sendImage)
        # #  ctypes.c_int Fg_sendImageEx(ctypes.c_void_p Fg, frameindex_t startImage, frameindex_t PicCount, ctypes.c_int nFlag, ctypes.c_uint DmaIndex, ctypes.c_void_p memHandle)
        # self.Fg_sendImageEx=wrapper(lib.Fg_sendImageEx)
        # #  ctypes.c_int Fg_saveFieldParameterToFile(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_uint DmaIndex, ctypes.c_char_p FileName)
        # self.Fg_saveFieldParameterToFile=wrapper(lib.Fg_saveFieldParameterToFile)
        # #  ctypes.c_int Fg_loadFieldParameterFromFile(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_uint DmaIndex, ctypes.c_char_p FileName)
        # self.Fg_loadFieldParameterFromFile=wrapper(lib.Fg_loadFieldParameterFromFile)
        
        ## Events and callbacks ##
        # #  ctypes.c_uint64 Fg_getEventMask(ctypes.c_void_p Fg, ctypes.c_char_p name)
        # self.Fg_getEventMask=wrapper(lib.Fg_getEventMask)
        # #  ctypes.c_int Fg_getEventPayload(ctypes.c_void_p Fg, ctypes.c_uint64 mask)
        # self.Fg_getEventPayload=wrapper(lib.Fg_getEventPayload)
        # #  ctypes.c_char_p Fg_getEventName(ctypes.c_void_p Fg, ctypes.c_uint64 mask)
        # self.Fg_getEventName=wrapper(lib.Fg_getEventName)
        # #  ctypes.c_int Fg_getEventCount(ctypes.c_void_p Fg)
        # self.Fg_getEventCount=wrapper(lib.Fg_getEventCount)
        # #  ctypes.c_int Fg_activateEvents(ctypes.c_void_p Fg, ctypes.c_uint64 mask, ctypes.c_uint enable)
        # self.Fg_activateEvents=wrapper(lib.Fg_activateEvents)
        # #  ctypes.c_int Fg_clearEvents(ctypes.c_void_p Fg, ctypes.c_uint64 mask)
        # self.Fg_clearEvents=wrapper(lib.Fg_clearEvents)
        # #  ctypes.c_uint64 Fg_eventWait(ctypes.c_void_p Fg, ctypes.c_uint64 mask, ctypes.c_uint timeout, ctypes.c_uint flags, ctypes.c_void_p info)
        # self.Fg_eventWait=wrapper(lib.Fg_eventWait)
        # #  ctypes.c_int Fg_registerEventCallback(ctypes.c_void_p Fg, ctypes.c_uint64 mask, Fg_EventFunc_t handler, ctypes.c_void_p data, ctypes.c_uint flags, ctypes.c_void_p info)
        # self.Fg_registerEventCallback=wrapper(lib.Fg_registerEventCallback)
        # #  ctypes.c_int Fg_registerAsyncNotifyCallback(ctypes.c_void_p Fg, Fg_AsyncNotifyFunc_t handler, ctypes.c_void_p context)
        # self.Fg_registerAsyncNotifyCallback=wrapper(lib.Fg_registerAsyncNotifyCallback)
        # #  ctypes.c_int Fg_unregisterAsyncNotifyCallback(ctypes.c_void_p Fg, Fg_AsyncNotifyFunc_t handler, ctypes.c_void_p context)
        # self.Fg_unregisterAsyncNotifyCallback=wrapper(lib.Fg_unregisterAsyncNotifyCallback)
        # #  ctypes.c_int Fg_resetAsyncNotify(ctypes.c_void_p Fg, ctypes.c_ulong notification, ctypes.c_ulong pl, ctypes.c_ulong ph)
        # self.Fg_resetAsyncNotify=wrapper(lib.Fg_resetAsyncNotify)
        # #  ctypes.c_int Fg_registerApcHandler(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex, ctypes.c_void_p control, ctypes.c_int flags)
        # self.Fg_registerApcHandler=wrapper(lib.Fg_registerApcHandler)
        
        ## Shading ##
        # #  ctypes.c_void_p Fg_AllocShading(ctypes.c_void_p Fg, ctypes.c_int set, ctypes.c_uint CamPort)
        # self.Fg_AllocShading=wrapper(lib.Fg_AllocShading)
        # #  ctypes.c_int Fg_FreeShading(ctypes.c_void_p Fg, ctypes.c_void_p sh)
        # self.Fg_FreeShading=wrapper(lib.Fg_FreeShading)
        # #  ctypes.c_int Shad_GetAccess(ctypes.c_void_p Fg, ctypes.c_void_p sh)
        # self.Shad_GetAccess=wrapper(lib.Shad_GetAccess)
        # #  ctypes.c_int Shad_FreeAccess(ctypes.c_void_p Fg, ctypes.c_void_p sh)
        # self.Shad_FreeAccess=wrapper(lib.Shad_FreeAccess)
        # #  ctypes.c_int Shad_GetMaxLine(ctypes.c_void_p Fg, ctypes.c_void_p sh)
        # self.Shad_GetMaxLine=wrapper(lib.Shad_GetMaxLine)
        # #  ctypes.c_int Shad_SetSubValueLine(ctypes.c_void_p Fg, ctypes.c_void_p sh, ctypes.c_int x, ctypes.c_int channel, ctypes.c_float sub)
        # self.Shad_SetSubValueLine=wrapper(lib.Shad_SetSubValueLine)
        # #  ctypes.c_int Shad_SetMultValueLine(ctypes.c_void_p Fg, ctypes.c_void_p sh, ctypes.c_int x, ctypes.c_int channel, ctypes.c_float mult)
        # self.Shad_SetMultValueLine=wrapper(lib.Shad_SetMultValueLine)
        # #  ctypes.c_int Shad_SetFixedPatternNoiseLine(ctypes.c_void_p Fg, ctypes.c_void_p sh, ctypes.c_int x, ctypes.c_int channel, ctypes.c_int on)
        # self.Shad_SetFixedPatternNoiseLine=wrapper(lib.Shad_SetFixedPatternNoiseLine)
        # #  ctypes.c_int Shad_WriteActLine(ctypes.c_void_p Fg, ctypes.c_void_p sh, ctypes.c_int Line)
        # self.Shad_WriteActLine=wrapper(lib.Shad_WriteActLine)
        





    def Fg_getParameterProperty(self, Fg, parameterId, propertyId):
        l=self.Fg_getParameterProperty_lib(Fg,parameterId,propertyId,None,0)
        buff=ctypes.create_string_buffer(l)
        l=self.Fg_getParameterProperty_lib(Fg,parameterId,propertyId,ctypes.cast(buff,ctypes.c_void_p),l)
        return buff[:l][:-1]
    def Fg_getParameterPropertyEx(self, Fg, parameterId, propertyId, DmaIndex):
        l=self.Fg_getParameterPropertyEx_lib(Fg,parameterId,propertyId,DmaIndex,None,0)
        buff=ctypes.create_string_buffer(l)
        l=self.Fg_getParameterPropertyEx_lib(Fg,parameterId,propertyId,DmaIndex,ctypes.cast(buff,ctypes.c_void_p),l)
        return buff[:l][:-1]
    def Fg_getSystemInformation(self, Fg, selector, propertyId, param1):
        l=self.Fg_getSystemInformation_lib(Fg,selector,propertyId,param1,None,0)
        buff=ctypes.create_string_buffer(l)
        l=self.Fg_getSystemInformation_lib(Fg,selector,propertyId,param1,ctypes.cast(buff,ctypes.c_void_p),l)
        return buff[:l][:-1]
    def Fg_getParameterInfoXML(self, Fg, port):
        l=self.Fg_getParameterInfoXML_lib(Fg,port,None,0)
        buff=ctypes.create_string_buffer(l)
        l=self.Fg_getParameterInfoXML_lib(Fg,port,ctypes.cast(buff,ctypes.c_char_p),l)
        return buff[:l][:-1]

    _property_types={   FgParamTypes.FG_PARAM_TYPE_INT32_T:   ctypes.c_int32,
                        FgParamTypes.FG_PARAM_TYPE_UINT32_T:  ctypes.c_uint32,
                        FgParamTypes.FG_PARAM_TYPE_INT64_T:   ctypes.c_int64,
                        FgParamTypes.FG_PARAM_TYPE_UINT64_T:  ctypes.c_uint64,
                        FgParamTypes.FG_PARAM_TYPE_DOUBLE:    ctypes.c_double,
                        FgParamTypes.FG_PARAM_TYPE_CHAR_PTR:  ctypes.c_char_p,
                        # FgParamTypes.FG_PARAM_TYPE_CHAR_PTR_PTR:    ctypes.POINTER(ctypes.c_char_p),
                        # FgParamTypes.FG_PARAM_TYPE_STRUCT_FIELDPARAMACCESS:   FieldParameterAccess,
                        # FgParamTypes.FG_PARAM_TYPE_STRUCT_FIELDPARAMINT:      FieldParameterInt,
                        # FgParamTypes.FG_PARAM_TYPE_STRUCT_FIELDPARAMINT64:    FieldParameterAccess,
                        # FgParamTypes.FG_PARAM_TYPE_STRUCT_FIELDPARAMDOUBLE:   FieldParameterDouble,
                        }
    def Fg_getParameterWithType_auto(self, Fg, Parameter, DmaIndex, ptype=None):
        if ptype is None:
            ptype=int(self.Fg_getParameterPropertyEx(Fg,Parameter,FgProperty.PROP_ID_DATATYPE,DmaIndex))
        if ptype not in self._property_types:
            raise SIFgrabLibError(self.Fg_getParameterPropertyEx,FG_STATUS.FG_ERROR,desc="can't deal with parameter type {}".format(ptype))
        if ptype==FgParamTypes.FG_PARAM_TYPE_CHAR_PTR:
            l=int(self.Fg_getParameterPropertyEx(Fg,Parameter,FgProperty.PROP_ID_VALUELLEN,DmaIndex))
            v=ctypes.create_string_buffer(l)
            pv=v
        else:
            v=self._property_types[ptype]()
            pv=ctypes.byref(v)
        self.Fg_getParameterWithType(Fg,Parameter,pv,DmaIndex,ptype)
        return v.value
    def Fg_setParameterWithType_auto(self, Fg, Parameter, Value, DmaIndex, ptype=None):
        if ptype is None:
            ptype=int(self.Fg_getParameterPropertyEx(Fg,Parameter,FgProperty.PROP_ID_DATATYPE,DmaIndex))
        if ptype not in self._property_types:
            raise SIFgrabLibError(self.Fg_getParameterPropertyEx,FG_STATUS.FG_ERROR,desc="can't deal with parameter type {}".format(ptype))
        if ptype==FgParamTypes.FG_PARAM_TYPE_CHAR_PTR:
            l=int(self.Fg_getParameterPropertyEx(Fg,Parameter,FgProperty.PROP_ID_VALUELLEN,DmaIndex))
            v=ctypes.create_string_buffer(l)
            Value=Value[:l]
            v[:len(Value)]=Value
        else:
            v=self._property_types[ptype](Value)
        self.Fg_setParameterWithType(Fg,Parameter,v,DmaIndex,ptype)

    def Fg_getParameterEx_auto(self, Fg, Parameter, DmaIndex, pMem, ImgNr):
        ptypes={FG_PARAM.FG_IMAGE_TAG:ctypes.c_uint, FG_PARAM.FG_TIMESTAMP:ctypes.c_uint, FG_PARAM.FG_TIMESTAMP_LONG:ctypes.c_uint64, FG_PARAM.FG_TRANSFER_LEN:ctypes.c_size_t}
        v=ptypes[Parameter]()
        self.Fg_getParameterEx(Fg,Parameter,ctypes.byref(v),DmaIndex,pMem,ImgNr)
        return v.value


wlib=SIFgrabLib()