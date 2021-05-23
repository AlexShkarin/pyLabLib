from ...core.utils import functions, py3, ctypes_wrap
from .misc import load_lib

import numpy as np
import ctypes
import collections

_depends_local=["...core.utils.ctypes_wrap"]

class IMAQdxGenericError(RuntimeError):
    """Generic IMAQdx error."""
    pass
    
class IMAQdxLibError(IMAQdxGenericError):
    """Generic IMAQdx library error."""
    def __init__(self, func, code, lib=None):
        self.func=func
        self.code=code
        self.desc="Unknown"
        try:
            if lib is not None:
                self.desc=py3.as_str(lib.IMAQdxGetErrorString(code))
        except IMAQdxLibError:
            pass
        self.msg="function '{}' raised error {}({})".format(func,code-0x100000000,self.desc)
        IMAQdxGenericError.__init__(self,self.msg)

def errcheck(passing=None, lib=None):
    """
    Build an error checking function.

    Return a function which checks return codes of IMAQdx library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    if passing is None:
        passing={0}
    def checker(result, func, arguments):
        if result not in passing:
            raise IMAQdxLibError(func.__name__,result,lib=lib)
        return result
    return checker



IMAQdxError=ctypes.c_uint32

IMAQDX_MAX_API_STRING_LENGTH=512
IMAQdxAPIString=ctypes.c_char*IMAQDX_MAX_API_STRING_LENGTH
def to_API_string(value):
    return ctypes.create_string_buffer(py3.as_builtin_bytes(value),IMAQDX_MAX_API_STRING_LENGTH)

IMAQdxSession=ctypes.c_uint32

IMAQdxCameraControlMode=ctypes.c_uint32
IMAQdxCameraControlMode_enum={"controller":0,"listener":1}
IMAQdxBusType=ctypes.c_uint32
class IMAQdxCameraInformation(ctypes.Structure):
    _fields_=[  ("Type",ctypes.c_uint32),
                ("Version",ctypes.c_uint32),
                ("Flags",ctypes.c_uint32),
                ("SerialNumberHi",ctypes.c_uint32),
                ("SerialNumberLo",ctypes.c_uint32),
                ("BusType",IMAQdxBusType),
                ("InterfaceName",IMAQdxAPIString),
                ("VendorName",IMAQdxAPIString),
                ("ModelName",IMAQdxAPIString),
                ("CameraFileName",IMAQdxAPIString),
                ("CameraAttributeURL",IMAQdxAPIString)]
IMAQdxCameraInformation_p=ctypes.POINTER(IMAQdxCameraInformation)
class CIMAQdxCameraInformation(ctypes_wrap.StructWrap):
    _struct=IMAQdxCameraInformation
    _tup_order=["InterfaceName","ModelName","VendorName"]

IMAQdxAttributeType=ctypes.c_uint32
IMAQdxAttributeType_enum={0:"u32", 1:"i64", 2:"f64", 3:"str", 4:"enum", 5:"bool", 6:"command", 7:"blob", 0xFFFFFFFF:"guard"}
class IMAQdxAttributeInformation(ctypes.Structure):
    _fields_=[  ("Type",IMAQdxAttributeType),
                ("Readable",ctypes.c_uint32),
                ("Writable",ctypes.c_uint32),
                ("Name",IMAQdxAPIString)]
IMAQdxAttributeInformation_p=ctypes.POINTER(IMAQdxAttributeInformation)
class CIMAQdxAttributeInformation(ctypes_wrap.StructWrap):
    _struct=IMAQdxAttributeInformation
    _tup_order=["Name","Type","Readable","Writable"]
    _tup={"Name":py3.as_str}
IMAQdxAttributeVisibility=ctypes.c_uint32
IMAQdxAttributeVisibility_enum={"simple":0x1000,"intermediate":0x2000,"advanced":0x4000}
IMAQdxValueType=ctypes.c_uint32
IMAQdxValueType_enum={0:"u32", 1:"i64", 2:"f64", 3:"str", 4:"enum", 5:"bool", 6:"str_disp", 0xFFFFFFFF:"guard"}
class IMAQdxEnumItem(ctypes.Structure):
    _fields_=[  ("Value",ctypes.c_uint32),
                ("Reserved",ctypes.c_uint32),
                ("Name",IMAQdxAPIString)]
IMAQdxEnumItem_p=ctypes.POINTER(IMAQdxEnumItem)
TIMAQdxEnumItem=collections.namedtuple("TIMAQdxEnumItem",["Value","Name"])

IMAQdxGuaranteedAttributes=[
    "CameraInformation::BaseAddress",
    "CameraInformation::BusType",
    "CameraInformation::ModelName",
    "CameraInformation::SerialNumberHigh",
    "CameraInformation::SerialNumberLow",
    "CameraInformation::VendorName",
    "CameraInformation::HostIPAddress",
    "CameraInformation::IPAddress",
    "CameraInformation::PrimaryURLString",
    "CameraInformation::SecondaryURLString",
    "StatusInformation::AcqInProgress",
    "StatusInformation::LastBufferCount",
    "StatusInformation::LastBufferNumber",
    "StatusInformation::LostBufferCount",
    "StatusInformation::LostPacketCount",
    "StatusInformation::RequestedResendPacketCount",
    "StatusInformation::ReceivedResendPackets",
    "StatusInformation::HandledEventCount",
    "StatusInformation::LostEventCount",
    "AcquisitionAttributes::Bayer::GainB",
    "AcquisitionAttributes::Bayer::GainG",
    "AcquisitionAttributes::Bayer::GainR",
    "AcquisitionAttributes::Bayer::Pattern",
    "AcquisitionAttributes::Controller::StreamChannelMode",
    "AcquisitionAttributes::Controller::DesiredStreamChannel",
    "AcquisitionAttributes::FrameInterval",
    "AcquisitionAttributes::IgnoreFirstFrame",
    "OffsetX",
    "OffsetY",
    "Width",
    "Height",
    "PixelFormat",
    "PacketSize",
    "PayloadSize",
    "AcquisitionAttributes::Speed",
    "AcquisitionAttributes::ShiftPixelBits",
    "AcquisitionAttributes::SwapPixelBytes",
    "AcquisitionAttributes::OverwriteMode",
    "AcquisitionAttributes::Timeout",
    "AcquisitionAttributes::VideoMode",
    "AcquisitionAttributes::BitsPerPixel",
    "AcquisitionAttributes::PixelSignedness",
    "AcquisitionAttributes::ReserveDualPackets",
    "AcquisitionAttributes::ReceiveTimestampMode",
    "AcquisitionAttributes::AdvancedEthernet::BandwidthControl::ActualPeakBandwidth",
    "AcquisitionAttributes::AdvancedEthernet::BandwidthControl::DesiredPeakBandwidth",
    "AcquisitionAttributes::AdvancedEthernet::Controller::DestinationMode",
    "AcquisitionAttributes::AdvancedEthernet::Controller::DestinationMulticastAddress",
    "AcquisitionAttributes::AdvancedEthernet::EventParameters::EventsEnabled",
    "AcquisitionAttributes::AdvancedEthernet::EventParameters::MaxOutstandingEvents",
    "AcquisitionAttributes::AdvancedEthernet::TestPacketParameters::TestPacketEnabled",
    "AcquisitionAttributes::AdvancedEthernet::TestPacketParameters::TestPacketTimeout",
    "AcquisitionAttributes::AdvancedEthernet::TestPacketParameters::MaxTestPacketRetries",
    "AcquisitionAttributes::ChunkDataDecoding::ChunkDataDecodingEnabled",
    "AcquisitionAttributes::ChunkDataDecoding::MaximumChunkCopySize",
    "AcquisitionAttributes::AdvancedEthernet::LostPacketMode",
    "AcquisitionAttributes::AdvancedEthernet::ResendParameters::MemoryWindowSize",
    "AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendsEnabled",
    "AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendThresholdPercentage",
    "AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendBatchingPercentage",
    "AcquisitionAttributes::AdvancedEthernet::ResendParameters::MaxResendsPerPacket",
    "AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendResponseTimeout",
    "AcquisitionAttributes::AdvancedEthernet::ResendParameters::NewPacketTimeout",
    "AcquisitionAttributes::AdvancedEthernet::ResendParameters::MissingPacketTimeout",
    "AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendTimerResolution"
]

IMAQdxBufferNumberMode=ctypes.c_uint32
IMAQdxBufferNumberMode_enum={"first":0,"last":1,"number":2,"every":3,"last_new":4}

class IMAQdxLib(object):
    def __init__(self):
        object.__init__(self)
        self._initialized=False

    
    def _new_attr_value(self, attr_type):
        if attr_type==0:
            return ctypes.c_uint32()
        if attr_type==1:
            return ctypes.c_int64()
        if attr_type==2:
            return ctypes.c_double()
        if attr_type==3:
            return IMAQdxAPIString()
        if attr_type==4:
            return IMAQdxEnumItem()
        if attr_type==5:
            return ctypes.c_bool()
        raise ValueError("unknown attribute type: {}".format(attr_type))
    def _to_attr_value(self, value, value_type=None):
        if value_type is None:
            if isinstance(value,int) or isinstance(value,np.long) or isinstance(value,np.integer):
                value_type=1
            elif isinstance(value,float) or isinstance(value,np.floating):
                value_type=2
            elif isinstance(value,py3.anystring):
                value_type=3
            else:
                raise ValueError("can't automatically determine value type for {}".format(value))
        if value_type==0:
            val=ctypes.c_uint32(value)
        elif value_type==1:
            val=ctypes.c_int64(value)
        elif value_type==2:
            val=ctypes.c_double(value)
        elif value_type==3:
            val=to_API_string(value)
        elif value_type==4:
            val=IMAQdxEnumItem(Value=value)
        elif value_type==5:
            val=ctypes.c_bool(value)
        else:
            raise ValueError("unknown attribute type: {}".format(value_type))
        return val,value_type
    def _from_attr_value(self, value, attr_type):
        if attr_type in [0,1,2,5]:
            return value.value
        if attr_type==3:
            return py3.as_str(value.value)
        if attr_type==4:
            return TIMAQdxEnumItem(value.Value,py3.as_str(value.Name))
        raise ValueError("unknown attribute type: {}".format(attr_type))

    def initlib(self):
        if self._initialized:
            return
        error_message="The library is automatically supplied with National Instruments NI-IMAQdx software"
        self.lib=load_lib("niimaqdx.dll",error_message=error_message,call_conv="stdcall")
        self.clib=load_lib("niimaqdx.dll",error_message=error_message,call_conv="cdecl")
        lib=self.lib

        wrapper=ctypes_wrap.CTypesWrapper(restype=IMAQdxError, return_res=False, errcheck=errcheck(lib=self))
        def wrapper_str_rval(func, argtypes, argnames):
            func=wrapper(func,argtypes,argnames,rvprep=[ctypes_wrap.strprep(IMAQDX_MAX_API_STRING_LENGTH)],rvref=[False])
            size_idx=argnames.index("size")
            def wrapped_func(*args):
                args=list(args)
                args[size_idx:size_idx]=[IMAQDX_MAX_API_STRING_LENGTH]
                return func(*args)
            sign=functions.FunctionSignature([n for n in argnames if n not in [None,"size"]],name=func.__name__)
            return sign.wrap_function(wrapped_func)
        self.IMAQdxGetErrorString=wrapper_str_rval(lib.IMAQdxGetErrorString, [IMAQdxError,ctypes.c_char_p,ctypes.c_uint32], ["code",None,"size"])

        self.IMAQdxEnumerateCameras_lib=wrapper(lib.IMAQdxEnumerateCameras,
            [IMAQdxCameraInformation_p,ctypes.POINTER(ctypes.c_uint32),ctypes.c_uint32],["cam_ptr","cnt_ptr","connected"])        
        self.IMAQdxOpenCamera=wrapper(lib.IMAQdxOpenCamera, [ctypes.c_char_p,IMAQdxCameraControlMode,IMAQdxSession], ["name","mode",None])
        self.IMAQdxCloseCamera=wrapper(lib.IMAQdxCloseCamera, [IMAQdxSession], ["sid"])
        self.IMAQdxResetCamera=wrapper(lib.IMAQdxResetCamera, [IMAQdxSession,ctypes.c_uint32], ["sid","reset_all"])


        def attr_prep(sid, name, attr_type):
            return self._new_attr_value(attr_type)
        def attr_conv(v, sid, name, attr_type):
            return self._from_attr_value(v,attr_type)
        self.IMAQdxEnumerateAttributes2_lib=wrapper(lib.IMAQdxEnumerateAttributes2,
            [IMAQdxSession,IMAQdxAttributeInformation_p,ctypes.POINTER(ctypes.c_uint32),ctypes.c_char_p,IMAQdxAttributeVisibility],
            ["sid","attr_ptr","cnt_ptr","root","visibility"])
        self.IMAQdxGetAttribute=wrapper(lib.IMAQdxGetAttribute, [IMAQdxSession,ctypes.c_char_p,IMAQdxAttributeType,ctypes.c_voidp],
            ["sid","name","attr_type",None],rvprep=[attr_prep],rvconv=[attr_conv])
        self.clib.IMAQdxSetAttribute.restype=IMAQdxError
        self.clib.IMAQdxSetAttribute.errcheck=errcheck(lib=self)
        self.IMAQdxGetAttributeType=wrapper(lib.IMAQdxGetAttributeType, [IMAQdxSession,ctypes.c_char_p,IMAQdxAttributeType], ["sid","name",None])
        self.IMAQdxGetAttributeMinimum=wrapper(lib.IMAQdxGetAttributeMinimum,[IMAQdxSession,ctypes.c_char_p,IMAQdxAttributeType,ctypes.c_voidp],
            ["sid","name","attr_type",None],rvprep=[attr_prep],rvconv=[attr_conv])
        self.IMAQdxGetAttributeMaximum=wrapper(lib.IMAQdxGetAttributeMaximum,[IMAQdxSession,ctypes.c_char_p,IMAQdxAttributeType,ctypes.c_voidp],
            ["sid","name","attr_type",None],rvprep=[attr_prep],rvconv=[attr_conv])
        self.IMAQdxGetAttributeIncrement=wrapper(lib.IMAQdxGetAttributeIncrement,[IMAQdxSession,ctypes.c_char_p,IMAQdxAttributeType,ctypes.c_voidp],
            ["sid","name","attr_type",None],rvprep=[attr_prep],rvconv=[attr_conv])
        self.IMAQdxIsAttributeReadable=wrapper(lib.IMAQdxIsAttributeReadable, [IMAQdxSession,ctypes.c_char_p,ctypes.c_bool], ["sid","name",None])
        self.IMAQdxIsAttributeWritable=wrapper(lib.IMAQdxIsAttributeWritable, [IMAQdxSession,ctypes.c_char_p,ctypes.c_bool], ["sid","name",None])
        self.IMAQdxGetAttributeTooltip=wrapper_str_rval(lib.IMAQdxGetAttributeTooltip,
            [IMAQdxSession,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint32], ["sid","name",None,"size"])
        self.IMAQdxGetAttributeUnits=wrapper_str_rval(lib.IMAQdxGetAttributeUnits,
            [IMAQdxSession,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint32], ["sid","name",None,"size"])
        self.IMAQdxGetAttributeDescription=wrapper_str_rval(lib.IMAQdxGetAttributeDescription,
            [IMAQdxSession,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint32], ["sid","name",None,"size"])
        self.IMAQdxGetAttributeDisplayName=wrapper_str_rval(lib.IMAQdxGetAttributeDisplayName,
            [IMAQdxSession,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint32], ["sid","name",None,"size"])
        self.IMAQdxEnumerateAttributeValues_lib=wrapper(lib.IMAQdxEnumerateAttributeValues,
            [IMAQdxSession,ctypes.c_char_p,IMAQdxEnumItem_p,ctypes.POINTER(ctypes.c_uint32)],["sid","name","val_ptr","cnt_ptr"])

        self.IMAQdxConfigureAcquisition=wrapper(lib.IMAQdxConfigureAcquisition, [IMAQdxSession,ctypes.c_uint32,ctypes.c_uint32], ["sid","continuous","buffer_count"])
        self.IMAQdxConfigureGrab=wrapper(lib.IMAQdxConfigureGrab, [IMAQdxSession], ["sid"])
        self.IMAQdxStartAcquisition=wrapper(lib.IMAQdxStartAcquisition, [IMAQdxSession], ["sid"])
        self.IMAQdxStopAcquisition=wrapper(lib.IMAQdxStopAcquisition, [IMAQdxSession], ["sid"])
        self.IMAQdxUnconfigureAcquisition=wrapper(lib.IMAQdxUnconfigureAcquisition, [IMAQdxSession], ["sid"])

        self.IMAQdxGetImageData_lib=wrapper(lib.IMAQdxGetImageData,
            [IMAQdxSession,ctypes.c_voidp,ctypes.c_uint32,IMAQdxBufferNumberMode,ctypes.c_uint32,ctypes.POINTER(ctypes.c_uint32)],
            ["sid","buff_ptr","size","mode","buffer_num","buffer_num_ptr"])

        self._initialized=True
        



    def IMAQdxEnumerateCameras(self, connected):
        cnt=ctypes.c_uint32()
        self.IMAQdxEnumerateCameras_lib(None,ctypes.byref(cnt),connected)
        cams=(IMAQdxCameraInformation*cnt.value)()
        self.IMAQdxEnumerateCameras_lib(cams,ctypes.byref(cnt),connected)
        return [CIMAQdxCameraInformation(c).tup() for c in cams]

    def IMAQdxEnumerateAttributes2(self, sid, root, visibility):
        cnt=ctypes.c_uint32()
        self.IMAQdxEnumerateAttributes2_lib(sid,None,ctypes.byref(cnt),root,visibility)
        attrs=(IMAQdxAttributeInformation*cnt.value)()
        self.IMAQdxEnumerateAttributes2_lib(sid,attrs,ctypes.byref(cnt),root,visibility)
        return [CIMAQdxAttributeInformation(a).tup() for a in attrs]
    def IMAQdxSetAttribute(self, sid, name, value, value_type):
        val,value_type=self._to_attr_value(value,value_type)
        name=py3.as_builtin_bytes(name)
        self.clib.IMAQdxSetAttribute(sid,name,ctypes.c_uint32(value_type),val)
    def IMAQdxEnumerateAttributeValues(self, sid, name):
        cnt=ctypes.c_uint32()
        self.IMAQdxEnumerateAttributeValues_lib(sid,name,None,ctypes.byref(cnt))
        values=(IMAQdxEnumItem*cnt.value)()
        self.IMAQdxEnumerateAttributeValues_lib(sid,name,values,ctypes.byref(cnt))
        return [self._from_attr_value(v,4) for v in values]

    def IMAQdxGetImageData(self, sid, size, mode, buffer_num):
        buff=ctypes.create_string_buffer(size)
        actual_buffer_num=ctypes.c_uint32()
        self.IMAQdxGetImageData_lib(sid,buff,size,mode,buffer_num,ctypes.byref(actual_buffer_num))
        return ctypes.string_at(buff,size),actual_buffer_num.value


lib=IMAQdxLib()