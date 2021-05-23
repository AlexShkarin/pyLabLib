from ...core.utils import py3, ctypes_wrap
from .misc import load_lib
from .IMAQ_lib_const import IMAQ_errors, IMAQ_attrs_inv
from .IMAQ_lib_const import IMAQ_signal_type_inv, IMAQ_int_signal_inv, IMAQ_signal_state_inv, IMAQ_trig_pol_inv, IMAQ_trig_action_inv, IMAQ_trig_drive_src_inv, IMAQInfiniteTimout

import numpy as np
import ctypes
import collections

_depends_local=["...core.utils.ctypes_wrap"]

class IMAQLibError(RuntimeError):
    """Generic IMAQ error."""
    def __init__(self, func, code, lib=None):
        self.func=func
        self.code=code
        self.name=IMAQ_errors.get(self.code,"Unknown")
        self.desc=""
        try:
            if lib is not None:
                self.desc=py3.as_str(lib.imgShowError(code))
        except IMAQLibError:
            pass
        self.msg="function '{}' raised error {}({}): {}".format(func,code,self.name,self.desc)
        RuntimeError.__init__(self,self.msg)
def errcheck(passing=None, lib=None):
    """
    Build an error checking function.

    Return a function which checks return codes of IMAQ library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    if passing is None:
        passing={0}
    def checker(result, func, arguments):
        if result not in passing:
            raise IMAQLibError(func.__name__,result,lib=lib)
        return result
    return checker


IMAQError=ctypes.c_uint32

IMAQ_MAX_API_STRING_LENGTH=512
IMAQAPIString=ctypes.c_char*IMAQ_MAX_API_STRING_LENGTH
def to_API_string(value):
    return ctypes.create_string_buffer(py3.as_builtin_bytes(value),IMAQ_MAX_API_STRING_LENGTH)

IMAQInterfaceID=ctypes.c_uint32
IMAQSessionID=ctypes.c_uint32
IMAQSignalType=ctypes.c_uint32



class IMAQLib(object):
    def __init__(self):
        object.__init__(self)
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return
        error_message="The library is automatically supplied with National Instruments NI-IMAQ software"
        self.lib=load_lib("imaq.dll",error_message=error_message,call_conv="stdcall")
        self.clib=load_lib("imaq.dll",error_message=error_message,call_conv="cdecl")
        lib=self.lib

        wrapper=ctypes_wrap.CTypesWrapper(restype=IMAQError, return_res=False, errcheck=errcheck(lib=self))
        strprep=ctypes_wrap.strprep(IMAQ_MAX_API_STRING_LENGTH)

        self.imgShowError=wrapper.wrap(lib.imgShowError, [ctypes.c_uint32, ctypes.c_char_p], ["errid", None], rvprep=[strprep], rvref=[False], errcheck=errcheck())

        self.imgInterfaceQueryNames=wrapper.wrap(lib.imgInterfaceQueryNames, [ctypes.c_uint32, ctypes.c_char_p], ["idx", None], rvprep=[strprep], rvref=[False])
        self.imgInterfaceOpen=wrapper.wrap(lib.imgInterfaceOpen, [ctypes.c_char_p, IMAQInterfaceID], ["name", None])
        self.imgInterfaceReset=wrapper.wrap(lib.imgInterfaceReset, [IMAQInterfaceID], ["ifid"])
        self.imgSessionOpen=wrapper.wrap(lib.imgSessionOpen, [IMAQInterfaceID, IMAQSessionID], ["ifid", None])
        self.imgClose=wrapper.wrap(lib.imgClose, [ctypes.c_uint32], ["id"])

        self.imgSessionSerialWrite=wrapper.wrap(lib.imgSessionSerialWrite, [IMAQSessionID,ctypes.c_char_p,ctypes.c_uint32,ctypes.c_uint32],
            ["sid","message",None,"timeout"], rvprep=[lambda *args: ctypes.c_uint32(len(args[1]))])
        self.imgSessionSerialRead=wrapper.wrap(lib.imgSessionSerialRead, [IMAQSessionID,ctypes.c_char_p,ctypes.c_uint32,ctypes.c_uint32],
            ["sid",None,None,"timeout"], rvprep=[strprep, lambda *args: ctypes.c_uint32(IMAQ_MAX_API_STRING_LENGTH)], rvnames=["message","size"], rvref=[False,True])
        self.imgSessionSerialReadBytes=wrapper.wrap(lib.imgSessionSerialReadBytes, [IMAQSessionID,ctypes.c_char_p,ctypes.c_uint32,ctypes.c_uint32],
            ["sid",None,None,"timeout"], rvprep=[lambda *args: ctypes.create_string_buffer(args[-1]+1), lambda *args: ctypes.c_uint32(args[-1])],
            rvnames=["message","size"], rvref=[False,True], addargs=["size"])
        self.imgSessionSerialFlush=wrapper.wrap(lib.imgSessionSerialFlush, [IMAQSessionID], ["sid"])

        self.imgSessionGetROI=wrapper.wrap(lib.imgSessionGetROI, [IMAQSessionID]+[ctypes.c_uint32]*4, ["sid"]+[None]*4)
        self.imgSessionConfigureROI=wrapper.wrap(lib.imgSessionConfigureROI, [IMAQSessionID]+[ctypes.c_uint32]*4, ["sid","top","left","height","width"])
        self.imgSessionFitROI=wrapper.wrap(lib.imgSessionFitROI, [IMAQSessionID]+[ctypes.c_uint32]*9, ["sid","fit_mode","top","left","height","width"]+[None]*4)

        self.imgSnap=wrapper.wrap(lib.imgSnap, [IMAQSessionID,ctypes.c_void_p], ["sid",None])
        self.imgSnapArea=wrapper.wrap(lib.imgSnapArea, [IMAQSessionID,ctypes.c_void_p]+[ctypes.c_uint32]*5, ["sid",None,"top","left","hight","width","row_pixels"])
        self.imgSessionGetBufferSize=wrapper.wrap(lib.imgSessionGetBufferSize, [IMAQSessionID,ctypes.c_uint32], ["sid",None])

        self.imgCreateBuffer=wrapper.wrap(lib.imgCreateBuffer, [IMAQSessionID,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p], ["sid","where","buff_size",None])
        self.imgDisposeBuffer=wrapper.wrap(lib.imgDisposeBuffer, [ctypes.c_void_p], ["buffer"])
        self.imgSessionClearBuffer=wrapper.wrap(lib.imgSessionClearBuffer, [IMAQSessionID,ctypes.c_uint32,ctypes.c_uint8], ["sid","buff_num","value"])

        
        self.imgRingSetup=wrapper.wrap(lib.imgRingSetup, [IMAQSessionID,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32],
            ["sid","buff_num","buffer","skip_count","start_now"])
        self.imgSequenceSetup=wrapper.wrap(lib.imgSequenceSetup, [IMAQSessionID,ctypes.c_uint32,ctypes.c_void_p,ctypes.POINTER(ctypes.c_uint32),ctypes.c_uint32,ctypes.c_uint32],
            ["sid","buff_num","buffer","skip_counts","start_now","run_async"])
        self.imgSessionStartAcquisition=wrapper.wrap(lib.imgSessionStartAcquisition, [IMAQSessionID], ["sid"])
        self.imgSessionStopAcquisition=wrapper.wrap(lib.imgSessionStopAcquisition, [IMAQSessionID], ["sid"])
        self.imgSessionStatus=wrapper.wrap(lib.imgSessionStatus,[IMAQSessionID,ctypes.c_uint32,ctypes.c_uint32],["sid",None,None])
        self.imgSessionAbort=wrapper.wrap(lib.imgSessionAbort,[IMAQSessionID,ctypes.c_uint32],["sid",None])

        self.imgGetAttribute_lib=wrapper.wrap(lib.imgGetAttribute, [IMAQSessionID,ctypes.c_uint32,ctypes.c_void_p], ["sid","attr",None], 
            rvprep=[lambda *args:args[-1]], addargs=["value"])
        self.imgSetAttribute2_lib=self.clib.imgSetAttribute2
        self.imgSetAttribute2_lib.restype=IMAQError
        self.imgSetAttribute2_lib.errcheck=errcheck(lib=self)
        self.imgGetCameraAttributeNumeric=wrapper.wrap(lib.imgGetCameraAttributeNumeric, [IMAQSessionID,ctypes.c_char_p,ctypes.c_double], ["sid","attr",None])
        self.imgSetCameraAttributeNumeric=wrapper.wrap(lib.imgSetCameraAttributeNumeric, [IMAQSessionID,ctypes.c_char_p,ctypes.c_double], ["sid","attr","value"])
        self.imgGetCameraAttributeString=wrapper.wrap(lib.imgGetCameraAttributeString, [IMAQSessionID,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint32],
            ["sid","attr",None,None], rvprep=[strprep, lambda *args: IMAQ_MAX_API_STRING_LENGTH], rvnames=["value",None], rvref=[False,False])
        self.imgSetCameraAttributeString=wrapper.wrap(lib.imgSetCameraAttributeString, [IMAQSessionID,ctypes.c_char_p,ctypes.c_char_p], ["sid","attr","value"])

        self.imgSessionWaitSignal2=wrapper.wrap(lib.imgSessionWaitSignal2, [IMAQSessionID,IMAQSignalType,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_uint32],
            ["sid","signal_type","signal_id","signal_state","timeout"])
        self.imgSessionTriggerConfigure2=wrapper.wrap(lib.imgSessionTriggerConfigure2, [IMAQSessionID,IMAQSignalType]+[ctypes.c_uint32]*4,
            ["sid","trig_type","trig_num","polarity","timeout","action"])
        self.imgSessionTriggerDrive2=wrapper.wrap(lib.imgSessionTriggerDrive2, [IMAQSessionID,IMAQSignalType]+[ctypes.c_uint32]*3,
            ["sid","trig_type","trig_num","polarity","source"])
        self.imgSessionLineTrigSource2=wrapper.wrap(lib.imgSessionLineTrigSource2, [IMAQSessionID,IMAQSignalType]+[ctypes.c_uint32]*3,
            ["sid","trig_type","trig_num","polarity","skip_counts"])
        self.imgSessionTriggerRead2=wrapper.wrap(lib.imgSessionTriggerRead2, [IMAQSessionID,IMAQSignalType]+[ctypes.c_uint32]*3,
            ["sid","trig_type","trig_num","polarity",None])
        self.imgSessionTriggerRoute2=wrapper.wrap(lib.imgSessionTriggerRoute2, [IMAQSessionID,IMAQSignalType,ctypes.c_uint32,IMAQSignalType,ctypes.c_uint32],
            ["sid","src_trig_type","src_trig_num","dst_trig_type","dst_trig_num"])
        self.imgSessionTriggerClear=wrapper.wrap(lib.imgSessionTriggerClear, [IMAQSessionID], ["sid"])
        

        self._initialized=True

    def imgGetAttribute_uint32(self, sid, attr):
        attr=IMAQ_attrs_inv.get(attr,attr)
        value=ctypes.c_uint32()
        self.imgGetAttribute_lib(sid,attr,value)
        return value.value
    def imgGetAttribute_double(self, sid, attr):
        attr=IMAQ_attrs_inv.get(attr,attr)
        value=ctypes.c_double()
        self.imgGetAttribute_lib(sid,attr,value)
        return value.value
    def imgSetAttribute2_uint32(self, sid, attr, value):
        attr=IMAQ_attrs_inv.get(attr,attr)
        self.imgSetAttribute2_lib(sid,attr,ctypes.c_uint32(int(value)))
    def imgSetAttribute2_double(self, sid, attr, value):
        attr=IMAQ_attrs_inv.get(attr,attr)
        self.imgSetAttribute2_lib(sid,attr,ctypes.c_double(float(value)))
    


lib=IMAQLib()