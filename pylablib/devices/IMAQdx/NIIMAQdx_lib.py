# pylint: disable=wrong-spelling-in-comment

from . import NIIMAQdx_defs
from .NIIMAQdx_defs import drIMAQdxError, IMAQdxError as IMAQdxErrorCode
from .NIIMAQdx_defs import IMAQdxBusType, IMAQdxCameraControlMode, IMAQdxBufferNumberMode  # pylint: disable=unused-import
from .NIIMAQdx_defs import IMAQdxAttributeType, IMAQdxAttributeVisibility  # pylint: disable=unused-import
from .NIIMAQdx_defs import IMAQdxCameraInformation, CIMAQdxCameraInformation
from .NIIMAQdx_defs import IMAQdxAttributeInformation, CIMAQdxAttributeInformation
from .NIIMAQdx_defs import IMAQdxEnumItem
from .NIIMAQdx_defs import IMAQdxVideoMode
from .NIIMAQdx_defs import define_functions

from ...core.utils import ctypes_wrap, py3
from ...core.devio.comm_backend import DeviceError
from ..utils import load_lib

import ctypes
import numpy as np


class IMAQdxError(DeviceError):
    """Generic IMAQdx error"""
class IMAQdxLibError(IMAQdxError):
    """Generic IMAQdx library error"""
    def __init__(self, func, code, lib=None):
        self.func=func
        self.code=code
        self.name=drIMAQdxError.get(self.code,"UNKNOWN")
        self.desc=""
        try:
            if lib is not None:
                self.desc=py3.as_str(lib.IMAQdxGetErrorString(code))
        except IMAQdxLibError:
            pass
        self.msg="function '{}' raised error {}({}): {}".format(func,code,self.name,self.desc)
        IMAQdxError.__init__(self,self.msg)
def errcheck(passing=None, lib=None):
    """
    Build an error checking function.

    Return a function which checks return codes of IMAQdx library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    if passing is None:
        passing={0}
    def errchecker(result, func, arguments):  # pylint: disable=unused-argument
        if result not in passing:
            raise IMAQdxLibError(func.__name__,result,lib=lib)
        return result
    return errchecker


IMAQdxAPIStringLength=512
IMAQdxAPIString=ctypes.c_char*IMAQdxAPIStringLength
class CIMAQdxEnumItem(NIIMAQdx_defs.CIMAQdxEnumItem):
    _tup_exc=["Reserved"]
    _conv={"Name":py3.as_str}



class IMAQdxLib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return
        error_message="The library is automatically supplied with National Instruments NI-IMAQdx software\n"+load_lib.par_error_message.format("niimaqdx")
        self.lib=load_lib.load_lib("niimaqdx.dll",locations=("parameter/niimaqdx","global"),error_message=error_message,call_conv="stdcall")
        self.clib=load_lib.load_lib("niimaqdx.dll",locations=("parameter/niimaqdx","global"),error_message=error_message,call_conv="cdecl")
        lib=self.lib
        define_functions(lib)

        wrapper=ctypes_wrap.CFunctionWrapper(return_res=False, errcheck=errcheck(lib=self))
        strprep=ctypes_wrap.strprep(IMAQdxAPIStringLength)

        #  ctypes.c_int IMAQdxGetErrorString(ctypes.c_int error, ctypes.c_char_p message, uInt32 messageLength)
        self.IMAQdxGetErrorString=wrapper(lib.IMAQdxGetErrorString, args=["error"], rvals=["message"],
            argprep={"message":strprep,"messageLength":IMAQdxAPIStringLength}, byref=[])

        #  ctypes.c_int IMAQdxEnumerateCameras(ctypes.POINTER(IMAQdxCameraInformation) cameraInformationArray, ctypes.POINTER(uInt32) count, bool32 connectedOnly)
        self.IMAQdxEnumerateCameras_lib=wrapper(lib.IMAQdxEnumerateCameras, args="all", rvals=["cameraInformationArray","count"], byref=["count"])
        #  ctypes.c_int IMAQdxResetCamera(ctypes.c_char_p name, bool32 resetAll)
        self.IMAQdxResetCamera=wrapper(lib.IMAQdxResetCamera)
        #  ctypes.c_int IMAQdxOpenCamera(ctypes.c_char_p name, ctypes.c_int mode, ctypes.POINTER(IMAQdxSession) id)
        self.IMAQdxOpenCamera=wrapper(lib.IMAQdxOpenCamera, rvals=["id"])
        #  ctypes.c_int IMAQdxCloseCamera(IMAQdxSession id)
        self.IMAQdxCloseCamera=wrapper(lib.IMAQdxCloseCamera)


        def attr_prep(type):  # pylint: disable=redefined-builtin
            return self._new_attr_value(type)
        def attr_conv(v, _, kwargs):
            return self._from_attr_value(v,kwargs["type"])
        #  ctypes.c_int IMAQdxEnumerateAttributes2(IMAQdxSession id, ctypes.POINTER(IMAQdxAttributeInformation) attributeInformationArray, ctypes.POINTER(uInt32) count, ctypes.c_char_p root, ctypes.c_int visibility)
        self.IMAQdxEnumerateAttributes2_lib=wrapper(lib.IMAQdxEnumerateAttributes2, args="all", rvals=["attributeInformationArray","count"], byref=["count"])
        #  ctypes.c_int IMAQdxGetAttribute(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_int type, ctypes.c_void_p value)
        self.IMAQdxGetAttribute=wrapper(lib.IMAQdxGetAttribute, rvals=["value"],
            argprep={"value":attr_prep}, rconv={"value":attr_conv})
        #  ctypes.c_int IMAQdxSetAttribute(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_int type, ...)
        self.clib.IMAQdxSetAttribute.restype=IMAQdxErrorCode
        self.clib.IMAQdxSetAttribute.errcheck=errcheck(lib=self)
        #  ctypes.c_int IMAQdxGetAttributeMinimum(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_int type, ctypes.c_void_p value)
        self.IMAQdxGetAttributeMinimum=wrapper(lib.IMAQdxGetAttributeMinimum, rvals=["value"],
            argprep={"value":attr_prep}, rconv={"value":attr_conv})
        #  ctypes.c_int IMAQdxGetAttributeMaximum(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_int type, ctypes.c_void_p value)
        self.IMAQdxGetAttributeMaximum=wrapper(lib.IMAQdxGetAttributeMaximum, rvals=["value"],
            argprep={"value":attr_prep}, rconv={"value":attr_conv})
        #  ctypes.c_int IMAQdxGetAttributeIncrement(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_int type, ctypes.c_void_p value)
        self.IMAQdxGetAttributeIncrement=wrapper(lib.IMAQdxGetAttributeIncrement, rvals=["value"],
            argprep={"value":attr_prep}, rconv={"value":attr_conv})
        #  ctypes.c_int IMAQdxGetAttributeType(IMAQdxSession id, ctypes.c_char_p name, ctypes.POINTER(ctypes.c_int) type)
        self.IMAQdxGetAttributeType=wrapper(lib.IMAQdxGetAttributeType, rvals=["type"])
        #  ctypes.c_int IMAQdxIsAttributeReadable(IMAQdxSession id, ctypes.c_char_p name, ctypes.POINTER(bool32) readable)
        self.IMAQdxIsAttributeReadable=wrapper(lib.IMAQdxIsAttributeReadable, rvals=["readable"])
        #  ctypes.c_int IMAQdxIsAttributeWritable(IMAQdxSession id, ctypes.c_char_p name, ctypes.POINTER(bool32) writable)
        self.IMAQdxIsAttributeWritable=wrapper(lib.IMAQdxIsAttributeWritable, rvals=["writable"])
        #  ctypes.c_int IMAQdxGetAttributeVisibility(IMAQdxSession id, ctypes.c_char_p name, ctypes.POINTER(ctypes.c_int) visibility)
        self.IMAQdxGetAttributeVisibility=wrapper(lib.IMAQdxGetAttributeVisibility, rvals=["visibility"])
        #  ctypes.c_int IMAQdxEnumerateAttributeValues(IMAQdxSession id, ctypes.c_char_p name, ctypes.POINTER(IMAQdxEnumItem) list, ctypes.POINTER(uInt32) size)
        self.IMAQdxEnumerateAttributeValues_lib=wrapper(lib.IMAQdxEnumerateAttributeValues, args="all", rvals=["list","size"], byref=["size"])
        #  ctypes.c_int IMAQdxGetAttributeTooltip(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_char_p tooltip, uInt32 length)
        self.IMAQdxGetAttributeTooltip=wrapper(lib.IMAQdxGetAttributeTooltip, args=["id","name"], rvals=["tooltip"],
            argprep={"tooltip":strprep,"length":IMAQdxAPIStringLength}, byref=[])
        #  ctypes.c_int IMAQdxGetAttributeUnits(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_char_p units, uInt32 length)
        self.IMAQdxGetAttributeUnits=wrapper(lib.IMAQdxGetAttributeUnits, args=["id","name"], rvals=["units"],
            argprep={"units":strprep,"length":IMAQdxAPIStringLength}, byref=[])
        #  ctypes.c_int IMAQdxGetAttributeDescription(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_char_p description, uInt32 length)
        self.IMAQdxGetAttributeDescription=wrapper(lib.IMAQdxGetAttributeDescription, args=["id","name"], rvals=["description"],
            argprep={"description":strprep,"length":IMAQdxAPIStringLength}, byref=[])
        #  ctypes.c_int IMAQdxGetAttributeDisplayName(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_char_p displayName, uInt32 length)
        self.IMAQdxGetAttributeDisplayName=wrapper(lib.IMAQdxGetAttributeDisplayName, args=["id","name"], rvals=["displayName"],
            argprep={"displayName":strprep,"length":IMAQdxAPIStringLength}, byref=[])
        #  ctypes.c_int IMAQdxEnumerateVideoModes(IMAQdxSession id, ctypes.POINTER(IMAQdxVideoMode) videoModeArray, ctypes.POINTER(uInt32) count, ctypes.POINTER(uInt32) currentMode)
        self.IMAQdxEnumerateVideoModes_lib=wrapper(lib.IMAQdxEnumerateVideoModes, args="all", rvals=["videoModeArray","count","currentMode"], byref=["count","currentMode"])

        #  ctypes.c_int IMAQdxConfigureAcquisition(IMAQdxSession id, bool32 continuous, uInt32 bufferCount)
        self.IMAQdxConfigureAcquisition=wrapper(lib.IMAQdxConfigureAcquisition)
        #  ctypes.c_int IMAQdxConfigureGrab(IMAQdxSession id)
        self.IMAQdxConfigureGrab=wrapper(lib.IMAQdxConfigureGrab)
        #  ctypes.c_int IMAQdxStartAcquisition(IMAQdxSession id)
        self.IMAQdxStartAcquisition=wrapper(lib.IMAQdxStartAcquisition)
        #  ctypes.c_int IMAQdxStopAcquisition(IMAQdxSession id)
        self.IMAQdxStopAcquisition=wrapper(lib.IMAQdxStopAcquisition)
        #  ctypes.c_int IMAQdxUnconfigureAcquisition(IMAQdxSession id)
        self.IMAQdxUnconfigureAcquisition=wrapper(lib.IMAQdxUnconfigureAcquisition)
        #  ctypes.c_int IMAQdxDispose(ctypes.c_void_p buffer)
        self.IMAQdxDispose=wrapper(lib.IMAQdxDispose)

        #  ctypes.c_int IMAQdxGetImage(IMAQdxSession id, ctypes.c_void_p image, ctypes.c_int mode, uInt32 desiredBufferNumber, ctypes.POINTER(uInt32) actualBufferNumber)
        self.IMAQdxGetImage=wrapper(lib.IMAQdxGetImage, rvals=["actualBufferNumber"])
        #  ctypes.c_int IMAQdxGetImageData(IMAQdxSession id, ctypes.c_void_p buffer, uInt32 bufferSize, ctypes.c_int mode, uInt32 desiredBufferNumber, ctypes.POINTER(uInt32) actualBufferNumber)
        self.IMAQdxGetImageData=wrapper(lib.IMAQdxGetImageData, rvals=["actualBufferNumber"])

        #  ctypes.c_int IMAQdxDiscoverEthernetCameras(ctypes.c_char_p address, uInt32 timeout)
        self.IMAQdxDiscoverEthernetCameras=wrapper(lib.IMAQdxDiscoverEthernetCameras)
        #  ctypes.c_int IMAQdxResetEthernetCameraAddress(ctypes.c_char_p name, ctypes.c_char_p address, ctypes.c_char_p subnet, ctypes.c_char_p gateway, uInt32 timeout)
        self.IMAQdxResetEthernetCameraAddress=wrapper(lib.IMAQdxResetEthernetCameraAddress)
        
        #  ctypes.c_int IMAQdxWriteRegister(IMAQdxSession id, uInt32 offset, uInt32 value)
        self.IMAQdxWriteRegister=wrapper(lib.IMAQdxWriteRegister)
        #  ctypes.c_int IMAQdxReadRegister(IMAQdxSession id, uInt32 offset, ctypes.POINTER(uInt32) value)
        self.IMAQdxReadRegister=wrapper(lib.IMAQdxReadRegister, rvals=["value"])
        #  ctypes.c_int IMAQdxWriteMemory(IMAQdxSession id, uInt32 offset, ctypes.c_char_p values, uInt32 count)
        self.IMAQdxWriteMemory=wrapper(lib.IMAQdxWriteMemory, args=["id", "offset", "values"], argprep={"count": lambda values: len(values)})  # pylint: disable=unnecessary-lambda
        #  ctypes.c_int IMAQdxReadMemory(IMAQdxSession id, uInt32 offset, ctypes.c_char_p values, uInt32 count)
        self.IMAQdxReadMemory=wrapper(lib.IMAQdxReadMemory, args=["id", "offset", "count"], argprep={"values": lambda count: ctypes.create_string_buffer(count)})  # pylint: disable=unnecessary-lambda
        #  ctypes.c_int IMAQdxWriteAttributes(IMAQdxSession id, ctypes.c_char_p filename)
        self.IMAQdxWriteAttributes=wrapper(lib.IMAQdxWriteAttributes)
        #  ctypes.c_int IMAQdxReadAttributes(IMAQdxSession id, ctypes.c_char_p filename)
        self.IMAQdxReadAttributes=wrapper(lib.IMAQdxReadAttributes)
        
        # typedef     uInt32 (NI_FUNC *FrameDoneEventCallbackPtr)(IMAQdxSession id, uInt32 bufferNumber, void* callbackData);
        self.c_frame_done_callback=ctypes.WINFUNCTYPE(ctypes.c_uint32, NIIMAQdx_defs.IMAQdxSession, ctypes.c_uint32, ctypes.c_void_p)
        #  ctypes.c_int IMAQdxRegisterFrameDoneEvent(IMAQdxSession id, uInt32 bufferInterval, FrameDoneEventCallbackPtr callbackFunction, ctypes.c_void_p callbackData)
        self.IMAQdxRegisterFrameDoneEvent_lib=wrapper(lib.IMAQdxRegisterFrameDoneEvent)
        # typedef     uInt32 (NI_FUNC *PnpEventCallbackPtr)(IMAQdxSession id, IMAQdxPnpEvent pnpEvent, void* callbackData);
        self.c_pnp_callback=ctypes.WINFUNCTYPE(ctypes.c_uint32, NIIMAQdx_defs.IMAQdxSession, ctypes.c_int, ctypes.c_void_p)
        #  ctypes.c_int IMAQdxRegisterPnpEvent(IMAQdxSession id, ctypes.c_int event, PnpEventCallbackPtr callbackFunction, ctypes.c_void_p callbackData)
        self.IMAQdxRegisterPnpEvent_lib=wrapper(lib.IMAQdxRegisterPnpEvent)
        # typedef     void (NI_FUNC *AttributeUpdatedEventCallbackPtr)(IMAQdxSession id, const char* name, void* callbackData);
        self.c_attr_updated_callback=ctypes.WINFUNCTYPE(None, NIIMAQdx_defs.IMAQdxSession, ctypes.c_char_p, ctypes.c_void_p)
        #  ctypes.c_int IMAQdxRegisterAttributeUpdatedEvent(IMAQdxSession id, ctypes.c_char_p name, AttributeUpdatedEventCallbackPtr callbackFunction, ctypes.c_void_p callbackData)
        self.IMAQdxRegisterAttributeUpdatedEvent_lib=wrapper(lib.IMAQdxRegisterAttributeUpdatedEvent)

        ### Bare wrappers (normally not used) ###
        #  ctypes.c_int IMAQdxSnap(IMAQdxSession id, ctypes.c_void_p image)
        self.IMAQdxSnap=wrapper(lib.IMAQdxSnap)
        #  ctypes.c_int IMAQdxGrab(IMAQdxSession id, ctypes.c_void_p image, bool32 waitForNextBuffer, ctypes.POINTER(uInt32) actualBufferNumber)
        self.IMAQdxGrab=wrapper(lib.IMAQdxGrab)
        #  ctypes.c_int IMAQdxSequence(IMAQdxSession id, ctypes.POINTER(ctypes.c_void_p) images, uInt32 count)
        self.IMAQdxSequence=wrapper(lib.IMAQdxSequence)

        ### Deprecated / too new ###
        #  ctypes.c_int IMAQdxEnumerateAttributes(IMAQdxSession id, ctypes.POINTER(IMAQdxAttributeInformation) attributeInformationArray, ctypes.POINTER(uInt32) count, ctypes.c_char_p root)
        #  ctypes.c_int IMAQdxEnumerateAttributes3(IMAQdxSession id, ctypes.POINTER(IMAQdxAttributeInformation) attributeInformationArray, ctypes.POINTER(uInt32) count, ctypes.c_char_p root, ctypes.c_int visibility)
        
        self._initialized=True
        



    def to_API_string(self, value):
        return ctypes.create_string_buffer(py3.as_builtin_bytes(value),IMAQdxAPIStringLength)
    numeric_attr_types=[IMAQdxAttributeType.IMAQdxAttributeTypeU32, IMAQdxAttributeType.IMAQdxAttributeTypeI64, IMAQdxAttributeType.IMAQdxAttributeTypeF64, IMAQdxAttributeType.IMAQdxAttributeTypeBool]
    def _new_attr_value(self, attr_type):
        if attr_type==IMAQdxAttributeType.IMAQdxAttributeTypeU32:
            return ctypes.c_uint32()
        if attr_type==IMAQdxAttributeType.IMAQdxAttributeTypeI64:
            return ctypes.c_int64()
        if attr_type==IMAQdxAttributeType.IMAQdxAttributeTypeF64:
            return ctypes.c_double()
        if attr_type==IMAQdxAttributeType.IMAQdxAttributeTypeString:
            return IMAQdxAPIString()
        if attr_type==IMAQdxAttributeType.IMAQdxAttributeTypeEnum:
            return IMAQdxEnumItem()
        if attr_type==IMAQdxAttributeType.IMAQdxAttributeTypeBool:
            return ctypes.c_bool()
        raise ValueError("unknown attribute type: {}".format(attr_type))
    def _to_attr_value(self, value, value_type=None):
        if value_type is None:
            if isinstance(value,int) or isinstance(value,np.integer):
                value_type=IMAQdxAttributeType.IMAQdxAttributeTypeI64
            elif isinstance(value,float) or isinstance(value,np.floating):
                value_type=IMAQdxAttributeType.IMAQdxAttributeTypeF64
            elif isinstance(value,py3.anystring):
                value_type=IMAQdxAttributeType.IMAQdxAttributeTypeString
            else:
                raise ValueError("can't automatically determine value type for {}".format(value))
        if value_type==IMAQdxAttributeType.IMAQdxAttributeTypeU32:
            val=ctypes.c_uint32(value)
        elif value_type==IMAQdxAttributeType.IMAQdxAttributeTypeI64:
            val=ctypes.c_int64(value)
        elif value_type==IMAQdxAttributeType.IMAQdxAttributeTypeF64:
            val=ctypes.c_double(value)
        elif value_type==IMAQdxAttributeType.IMAQdxAttributeTypeString:
            val=self.to_API_string(value)
        elif value_type==IMAQdxAttributeType.IMAQdxAttributeTypeEnum:
            val=IMAQdxEnumItem(Value=value)
        elif value_type==IMAQdxAttributeType.IMAQdxAttributeTypeBool:
            val=ctypes.c_bool(value)
        else:
            raise ValueError("unknown attribute type: {}".format(value_type))
        return val,value_type
    def _from_attr_value(self, value, attr_type):
        if attr_type in [IMAQdxAttributeType.IMAQdxAttributeTypeU32,IMAQdxAttributeType.IMAQdxAttributeTypeI64,
                        IMAQdxAttributeType.IMAQdxAttributeTypeF64,IMAQdxAttributeType.IMAQdxAttributeTypeBool]:
            return value.value
        if attr_type==IMAQdxAttributeType.IMAQdxAttributeTypeString:
            return py3.as_str(value.value)
        if attr_type==IMAQdxAttributeType.IMAQdxAttributeTypeEnum:
            return CIMAQdxEnumItem.tup_struct(value)
        raise ValueError("unknown attribute type: {}".format(attr_type))



    def IMAQdxEnumerateCameras(self, connected):
        _,cnt=self.IMAQdxEnumerateCameras_lib(None,0,connected)
        cams=(IMAQdxCameraInformation*cnt)()
        self.IMAQdxEnumerateCameras_lib(cams,cnt,connected)
        return [CIMAQdxCameraInformation(c).tup() for c in cams]

    def IMAQdxEnumerateAttributes2(self, sid, root, visibility):
        _,cnt=self.IMAQdxEnumerateAttributes2_lib(sid,None,0,root,visibility)
        attrs=(IMAQdxAttributeInformation*cnt)()
        self.IMAQdxEnumerateAttributes2_lib(sid,attrs,cnt,root,visibility)
        return [CIMAQdxAttributeInformation(a).tup() for a in attrs]
    def IMAQdxSetAttribute(self, sid, name, value, value_type):
        val,value_type=self._to_attr_value(value,value_type)
        name=py3.as_builtin_bytes(name)
        self.clib.IMAQdxSetAttribute(sid,name,ctypes.c_uint32(value_type),val)
    def IMAQdxEnumerateAttributeValues(self, sid, name):
        _,cnt=self.IMAQdxEnumerateAttributeValues_lib(sid,name,None,0)
        values=(IMAQdxEnumItem*cnt)()
        self.IMAQdxEnumerateAttributeValues_lib(sid,name,values,cnt)
        return [self._from_attr_value(v,IMAQdxAttributeType.IMAQdxAttributeTypeEnum) for v in values]
    def IMAQdxEnumerateVideoModes(self, sid):
        _,cnt,_=self.IMAQdxEnumerateVideoModes_lib(sid,None,0,0)
        modes=(IMAQdxVideoMode*cnt)()
        _,_,cmode=self.IMAQdxEnumerateVideoModes_lib(sid,modes,cnt,0)
        return [self._from_attr_value(m,IMAQdxAttributeType.IMAQdxAttributeTypeEnum) for m in modes],cmode

    def IMAQdxGetImageData_newbuff(self, sid, size, mode, buffer_num):
        buff=ctypes.create_string_buffer(size)
        actual_buffer_num=self.IMAQdxGetImageData(sid,buff,size,mode,buffer_num)
        return ctypes.string_at(buff,size),actual_buffer_num

    def _wrap_callback(self, callback, callback_type, wrap=True):
        if wrap:
            def wrapped_callback(*args):
                try:
                    callback(*args)
                except: # pylint: disable=bare-except
                    pass
            return callback_type(wrapped_callback)
        else:
            return callback_type(callback)
    def IMAQdxRegisterFrameDoneEvent(self, sid, bufferInterval, callbackFunction, callbackData=None, wrap=True):
        cb=self._wrap_callback(callbackFunction,self.c_frame_done_callback,wrap=wrap)
        self.IMAQdxRegisterFrameDoneEvent_lib(sid,bufferInterval,cb,callbackData)
        return cb
    def IMAQdxRegisterPnpEvent(self, sid, event, callbackFunction, callbackData=None, wrap=True):
        cb=self._wrap_callback(callbackFunction,self.c_pnp_callback,wrap=wrap)
        self.IMAQdxRegisterPnpEvent_lib(sid,event,cb,callbackData)
        return cb
    def IMAQdxRegisterAttributeUpdatedEvent(self, sid, name, callbackFunction, callbackData=None, wrap=True):
        cb=self._wrap_callback(callbackFunction,self.c_attr_updated_callback,wrap=wrap)
        self.IMAQdxRegisterAttributeUpdatedEvent_lib(sid,name,cb,callbackData)
        return cb

wlib=IMAQdxLib()