##########   This file is generated automatically based on pylonC.h, GenApiCError.h, PylonCError.h, PFNC.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class PYLONC_ACCESS(enum.IntEnum):
    PYLONC_ACCESS_MODE_MONITOR   = _int32((0))
    PYLONC_ACCESS_MODE_CONTROL   = _int32((1 << 0))
    PYLONC_ACCESS_MODE_STREAM    = _int32((1 << 1))
    PYLONC_ACCESS_MODE_EVENT     = _int32((1 << 2))
    PYLONC_ACCESS_MODE_EXCLUSIVE = _int32((1 << 3))
dPYLONC_ACCESS={a.name:a.value for a in PYLONC_ACCESS}
drPYLONC_ACCESS={a.value:a.name for a in PYLONC_ACCESS}


class GENAPI_ERR(enum.IntEnum):
    GENAPI_E_OK                         = _int32((0))
    GENAPI_E_FAIL                       = _int32((0xC2000001))
    GENAPI_E_INVALID_ARG                = _int32((0xC2000002))
    GENAPI_E_INSUFFICIENT_BUFFER        = _int32((0xC2000003))
    GENAPI_E_INVALID_NODEMAPHANDLE      = _int32((0xC2000004))
    GENAPI_E_NODE_NOT_FOUND             = _int32((0xC2000005))
    GENAPI_E_INVALID_NODEHANDLE         = _int32((0xC2000006))
    GENAPI_E_RESULT_RANGE_EXCEEDED      = _int32((0xC2000007))
    GENAPI_E_LIMITS_EXCEEDED            = _int32((0xC2000008))
    GENAPI_E_PROPERTY_ERROR             = _int32((0xC2000009))
    GENAPI_E_TIMEOUT                    = _int32((0xC200000A))
    GENAPI_E_TYPE_ERROR                 = _int32((0xC200000B))
    GENAPI_E_INDEX_ERROR                = _int32((0xC200000C))
    GENAPI_E_OBJECT_ILLEGAL_STATE       = _int32((0xC200000E))
    GENAPI_E_INVALID_NODECALLBACKHANDLE = _int32((0xC200000F))
    GENAPI_E_LOGICAL_ERROR              = _int32((0xC2000010))
    GENAPI_E_INVALID_FILEHANDLE         = _int32((0xC2000011))
dGENAPI_ERR={a.name:a.value for a in GENAPI_ERR}
drGENAPI_ERR={a.value:a.name for a in GENAPI_ERR}


class PYLONC_ERR(enum.IntEnum):
    PYLON_E_INVALID_DEVICEHANDLE        = _int32((0xC3000001))
    PYLON_E_INVALID_DEVICEINFOHANDLE    = _int32((0xC3000002))
    PYLON_E_INVALID_DEVICEINFO_PROPERTY = _int32((0xC3000003))
    PYLON_E_INVALID_STREAMGRABBERHANDLE = _int32((0xC3000004))
    PYLON_E_INVALID_CHUNKPARSERHANDLE   = _int32((0xC3000005))
    PYLON_E_INVALID_WAITOBJECTHANDLE    = _int32((0xC3000006))
    PYLON_E_INVALID_EVENTGRABBERHANDLE  = _int32((0xC3000007))
    PYLON_E_INVALID_EVENTADAPTERHANDLE  = _int32((0xC3000008))
    PYLON_E_INVALID_CONVERTERHANDLE     = _int32((0xC3000009))
    PYLON_E_INVALID_WAITOBJECTSHANDLE   = _int32((0xC300000A))
    PYLON_E_INVALID_AVIWRITERHANDLE     = _int32((0xC300000B))
    PYLON_E_INVALID_INTERFACEHANDLE     = _int32((0xC300000C))
    PYLON_E_INVALID_INTERFACEINFOHANDLE = _int32((0xC300000D))
    PYLON_E_INVALID_DECOMPRESSORHANDLE  = _int32((0xC300000E))
dPYLONC_ERR={a.name:a.value for a in PYLONC_ERR}
drPYLONC_ERR={a.value:a.name for a in PYLONC_ERR}


class PFNC_COMPONENT(enum.IntEnum):
    PFNC_SINGLE_COMPONENT   = _int32(0x01000000)
    PFNC_MULTIPLE_COMPONENT = _int32(0x02000000)
    PFNC_COMPONENT_MASK     = _int32(0x7F000000)
dPFNC_COMPONENT={a.name:a.value for a in PFNC_COMPONENT}
drPFNC_COMPONENT={a.value:a.name for a in PFNC_COMPONENT}


class PFNC_SIZE(enum.IntEnum):
    PFNC_OCCUPY1BIT       = _int32(0x00010000)
    PFNC_OCCUPY2BIT       = _int32(0x00020000)
    PFNC_OCCUPY4BIT       = _int32(0x00040000)
    PFNC_OCCUPY8BIT       = _int32(0x00080000)
    PFNC_OCCUPY10BIT      = _int32(0x000A0000)
    PFNC_OCCUPY12BIT      = _int32(0x000C0000)
    PFNC_OCCUPY16BIT      = _int32(0x00100000)
    PFNC_OCCUPY24BIT      = _int32(0x00180000)
    PFNC_OCCUPY30BIT      = _int32(0x001E0000)
    PFNC_OCCUPY32BIT      = _int32(0x00200000)
    PFNC_OCCUPY36BIT      = _int32(0x00240000)
    PFNC_OCCUPY40BIT      = _int32(0x00280000)
    PFNC_OCCUPY48BIT      = _int32(0x00300000)
    PFNC_OCCUPY64BIT      = _int32(0x00400000)
    PFNC_PIXEL_SIZE_MASK  = _int32(0x00FF0000)
    PFNC_PIXEL_SIZE_SHIFT = _int32(16)
dPFNC_SIZE={a.name:a.value for a in PFNC_SIZE}
drPFNC_SIZE={a.value:a.name for a in PFNC_SIZE}





##### TYPE DEFINITIONS #####


BYTE=ctypes.c_ubyte
PBYTE=ctypes.POINTER(BYTE)
CHAR=ctypes.c_char
PCHAR=ctypes.c_char_p
UCHAR=ctypes.c_ubyte
PUCHAR=ctypes.POINTER(UCHAR)
ULONG_PTR=ctypes.c_uint64
LONG_PTR=ctypes.c_int64
WORD=ctypes.c_ushort
DWORD=ctypes.c_ulong
LPWORD=ctypes.POINTER(WORD)
LONG=ctypes.c_long
LONGLONG=ctypes.c_int64
LPLONG=ctypes.POINTER(ctypes.c_long)
HANDLE=ctypes.c_void_p
LPHANDLE=ctypes.POINTER(HANDLE)
PHANDLE=ctypes.POINTER(HANDLE)
HWND=ctypes.c_void_p
HGLOBAL=ctypes.c_void_p
HINSTANCE=ctypes.c_void_p
HDC=ctypes.c_void_p
HMODULE=ctypes.c_void_p
HKEY=ctypes.c_void_p
HRESULT=LONG
PVOID=ctypes.c_void_p
LPVOID=ctypes.c_void_p
class RECT(ctypes.Structure):
    _fields_=[  ("left",LONG),
                ("top",LONG),
                ("right",LONG),
                ("bottom",LONG) ]
PRECT=ctypes.POINTER(RECT)
class CRECT(ctypes_wrap.CStructWrapper):
    _struct=RECT


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_=[  ("biSize",DWORD),
                ("biWidth",LONG),
                ("biHeight",LONG),
                ("biPlanes",WORD),
                ("biBitCount",WORD),
                ("biCompression",DWORD),
                ("biSizeImage",DWORD),
                ("biXPelsPerMeter",LONG),
                ("biYPelsPerMeter",LONG),
                ("biClrUsed",DWORD),
                ("biClrImportant",DWORD) ]
PBITMAPINFOHEADER=ctypes.POINTER(BITMAPINFOHEADER)
class CBITMAPINFOHEADER(ctypes_wrap.CStructWrapper):
    _struct=BITMAPINFOHEADER


MirEGLNativeWindowType=ctypes.c_void_p
MirEGLNativeDisplayType=ctypes.c_void_p
class EGenApiNodeType(enum.IntEnum):
    IntegerNode     =_int32(0)
    BooleanNode     =enum.auto()
    FloatNode       =enum.auto()
    CommandNode     =enum.auto()
    StringNode      =enum.auto()
    EnumerationNode =enum.auto()
    EnumEntryNode   =enum.auto()
    Category        =enum.auto()
    _UnknownNodeType=_int32((-1))
dEGenApiNodeType={a.name:a.value for a in EGenApiNodeType}
drEGenApiNodeType={a.value:a.name for a in EGenApiNodeType}


class EGenApiAccessMode(enum.IntEnum):
    NI                 =_int32(0)
    NA                 =enum.auto()
    WO                 =enum.auto()
    RO                 =enum.auto()
    RW                 =enum.auto()
    _UndefinedAccesMode=_int32((-1))
dEGenApiAccessMode={a.name:a.value for a in EGenApiAccessMode}
drEGenApiAccessMode={a.value:a.name for a in EGenApiAccessMode}


class EGenApiNameSpace(enum.IntEnum):
    Custom             =_int32(0)
    Standard           =enum.auto()
    _UndefinedNameSpace=_int32((-1))
dEGenApiNameSpace={a.name:a.value for a in EGenApiNameSpace}
drEGenApiNameSpace={a.value:a.name for a in EGenApiNameSpace}


class EGenApiVisibility(enum.IntEnum):
    Beginner            =_int32(0)
    Expert              =_int32(1)
    Guru                =_int32(2)
    Invisible           =_int32(3)
    _UndefinedVisibility=_int32((-1))
dEGenApiVisibility={a.name:a.value for a in EGenApiVisibility}
drEGenApiVisibility={a.value:a.name for a in EGenApiVisibility}


class EGenApiCachingMode(enum.IntEnum):
    NoCache              =_int32(0)
    WriteThrough         =enum.auto()
    WriteAround          =enum.auto()
    _UndefinedCachingMode=_int32((-1))
dEGenApiCachingMode={a.name:a.value for a in EGenApiCachingMode}
drEGenApiCachingMode={a.value:a.name for a in EGenApiCachingMode}


class EGenApiRepresentation(enum.IntEnum):
    Linear                  =_int32(0)
    Logarithmic             =enum.auto()
    Boolean                 =enum.auto()
    PureNumber              =enum.auto()
    HexNumber               =enum.auto()
    _UndefinedRepresentation=_int32((-1))
dEGenApiRepresentation={a.name:a.value for a in EGenApiRepresentation}
drEGenApiRepresentation={a.value:a.name for a in EGenApiRepresentation}


class EGenApiFileAccessMode(enum.IntEnum):
    GenApiFileReadAccess =_int32(0)
    GenApiFileWriteAccess=enum.auto()
dEGenApiFileAccessMode={a.name:a.value for a in EGenApiFileAccessMode}
drEGenApiFileAccessMode={a.value:a.name for a in EGenApiFileAccessMode}


NODE_HANDLE=ctypes.c_void_p
NODEMAP_HANDLE=ctypes.c_void_p
GENAPI_FILE_HANDLE=ctypes.c_void_p
NODE_CALLBACK_HANDLE=ctypes.c_void_p
class EPylonWaitExResult(enum.IntEnum):
    waitex_timeout  =_int32(0)
    waitex_signaled =_int32(1)
    waitex_abandoned=_int32(2)
    waitex_alerted  =_int32((-1))
dEPylonWaitExResult={a.name:a.value for a in EPylonWaitExResult}
drEPylonWaitExResult={a.value:a.name for a in EPylonWaitExResult}


class EPylonGrabStatus(enum.IntEnum):
    UndefinedGrabStatus=_int32((-1))
    Idle               =enum.auto()
    Queued             =enum.auto()
    Grabbed            =enum.auto()
    Canceled           =enum.auto()
    Failed             =enum.auto()
dEPylonGrabStatus={a.name:a.value for a in EPylonGrabStatus}
drEPylonGrabStatus={a.value:a.name for a in EPylonGrabStatus}


class EPylonPayloadType(enum.IntEnum):
    PayloadType_Undefined     =_int32((-1))
    PayloadType_Image         =enum.auto()
    PayloadType_RawData       =enum.auto()
    PayloadType_File          =enum.auto()
    PayloadType_ChunkData     =enum.auto()
    PayloadType_GenDC         =enum.auto()
    PayloadType_DeviceSpecific=_int32(0x8000)
dEPylonPayloadType={a.name:a.value for a in EPylonPayloadType}
drEPylonPayloadType={a.value:a.name for a in EPylonPayloadType}


class EPylonPixelType(enum.IntEnum):
    PixelType_Undefined                    =_int32((-1))
    PixelType_Mono8                        =_int32(((0x01000000|(8<<16))|0x0001))
    PixelType_Mono8signed                  =_int32(((0x01000000|(8<<16))|0x0002))
    PixelType_Mono10                       =_int32(((0x01000000|(16<<16))|0x0003))
    PixelType_Mono10packed                 =_int32(((0x01000000|(12<<16))|0x0004))
    PixelType_Mono10p                      =_int32(((0x01000000|(10<<16))|0x0046))
    PixelType_Mono12                       =_int32(((0x01000000|(16<<16))|0x0005))
    PixelType_Mono12packed                 =_int32(((0x01000000|(12<<16))|0x0006))
    PixelType_Mono12p                      =_int32(((0x01000000|(12<<16))|0x0047))
    PixelType_Mono16                       =_int32(((0x01000000|(16<<16))|0x0007))
    PixelType_BayerGR8                     =_int32(((0x01000000|(8<<16))|0x0008))
    PixelType_BayerRG8                     =_int32(((0x01000000|(8<<16))|0x0009))
    PixelType_BayerGB8                     =_int32(((0x01000000|(8<<16))|0x000a))
    PixelType_BayerBG8                     =_int32(((0x01000000|(8<<16))|0x000b))
    PixelType_BayerGR10                    =_int32(((0x01000000|(16<<16))|0x000c))
    PixelType_BayerRG10                    =_int32(((0x01000000|(16<<16))|0x000d))
    PixelType_BayerGB10                    =_int32(((0x01000000|(16<<16))|0x000e))
    PixelType_BayerBG10                    =_int32(((0x01000000|(16<<16))|0x000f))
    PixelType_BayerGR12                    =_int32(((0x01000000|(16<<16))|0x0010))
    PixelType_BayerRG12                    =_int32(((0x01000000|(16<<16))|0x0011))
    PixelType_BayerGB12                    =_int32(((0x01000000|(16<<16))|0x0012))
    PixelType_BayerBG12                    =_int32(((0x01000000|(16<<16))|0x0013))
    PixelType_RGB8packed                   =_int32(((0x02000000|(24<<16))|0x0014))
    PixelType_BGR8packed                   =_int32(((0x02000000|(24<<16))|0x0015))
    PixelType_RGBA8packed                  =_int32(((0x02000000|(32<<16))|0x0016))
    PixelType_BGRA8packed                  =_int32(((0x02000000|(32<<16))|0x0017))
    PixelType_RGB10packed                  =_int32(((0x02000000|(48<<16))|0x0018))
    PixelType_BGR10packed                  =_int32(((0x02000000|(48<<16))|0x0019))
    PixelType_RGB12packed                  =_int32(((0x02000000|(48<<16))|0x001a))
    PixelType_BGR12packed                  =_int32(((0x02000000|(48<<16))|0x001b))
    PixelType_RGB16packed                  =_int32(((0x02000000|(48<<16))|0x0033))
    PixelType_BGR10V1packed                =_int32(((0x02000000|(32<<16))|0x001c))
    PixelType_BGR10V2packed                =_int32(((0x02000000|(32<<16))|0x001d))
    PixelType_YUV411packed                 =_int32(((0x02000000|(12<<16))|0x001e))
    PixelType_YUV422packed                 =_int32(((0x02000000|(16<<16))|0x001f))
    PixelType_YUV444packed                 =_int32(((0x02000000|(24<<16))|0x0020))
    PixelType_RGB8planar                   =_int32(((0x02000000|(24<<16))|0x0021))
    PixelType_RGB10planar                  =_int32(((0x02000000|(48<<16))|0x0022))
    PixelType_RGB12planar                  =_int32(((0x02000000|(48<<16))|0x0023))
    PixelType_RGB16planar                  =_int32(((0x02000000|(48<<16))|0x0024))
    PixelType_YUV422_YUYV_Packed           =_int32(((0x02000000|(16<<16))|0x0032))
    PixelType_YUV444planar                 =_int32((((0x80000000|0x02000000)|(24<<16))|0x0044))
    PixelType_YUV422planar                 =_int32(((0x02000000|(16<<16))|0x0042))
    PixelType_YUV420planar                 =_int32(((0x02000000|(12<<16))|0x0040))
    PixelType_YCbCr422_8_YY_CbCr_Semiplanar=_int32(((0x02000000|(16<<16))|0x0113))
    PixelType_YCbCr420_8_YY_CbCr_Semiplanar=_int32(((0x02000000|(12<<16))|0x0112))
    PixelType_BayerGR12Packed              =_int32(((0x01000000|(12<<16))|0x002A))
    PixelType_BayerRG12Packed              =_int32(((0x01000000|(12<<16))|0x002B))
    PixelType_BayerGB12Packed              =_int32(((0x01000000|(12<<16))|0x002C))
    PixelType_BayerBG12Packed              =_int32(((0x01000000|(12<<16))|0x002D))
    PixelType_BayerGR10p                   =_int32(((0x01000000|(10<<16))|0x0056))
    PixelType_BayerRG10p                   =_int32(((0x01000000|(10<<16))|0x0058))
    PixelType_BayerGB10p                   =_int32(((0x01000000|(10<<16))|0x0054))
    PixelType_BayerBG10p                   =_int32(((0x01000000|(10<<16))|0x0052))
    PixelType_BayerGR12p                   =_int32(((0x01000000|(12<<16))|0x0057))
    PixelType_BayerRG12p                   =_int32(((0x01000000|(12<<16))|0x0059))
    PixelType_BayerGB12p                   =_int32(((0x01000000|(12<<16))|0x0055))
    PixelType_BayerBG12p                   =_int32(((0x01000000|(12<<16))|0x0053))
    PixelType_BayerGR16                    =_int32(((0x01000000|(16<<16))|0x002E))
    PixelType_BayerRG16                    =_int32(((0x01000000|(16<<16))|0x002F))
    PixelType_BayerGB16                    =_int32(((0x01000000|(16<<16))|0x0030))
    PixelType_BayerBG16                    =_int32(((0x01000000|(16<<16))|0x0031))
    PixelType_RGB12V1packed                =_int32(((0x02000000|(36<<16))|0X0034))
    PixelType_Data32f                      =_int32(((0x01000000|(32<<16))|0x011C))
    PixelType_Double                       =_int32((((0x80000000|0x01000000)|(64<<16))|0x100))
dEPylonPixelType={a.name:a.value for a in EPylonPixelType}
drEPylonPixelType={a.value:a.name for a in EPylonPixelType}


class EPylonImageFileFormat(enum.IntEnum):
    ImageFileFormat_Bmp =_int32(0)
    ImageFileFormat_Tiff=_int32(1)
    ImageFileFormat_Jpeg=_int32(2)
    ImageFileFormat_Png =_int32(3)
    ImageFileFormat_Raw =_int32(4)
dEPylonImageFileFormat={a.name:a.value for a in EPylonImageFileFormat}
drEPylonImageFileFormat={a.value:a.name for a in EPylonImageFileFormat}


class EPylonImageOrientation(enum.IntEnum):
    ImageOrientation_TopDown =_int32(0)
    ImageOrientation_BottomUp=enum.auto()
dEPylonImageOrientation={a.name:a.value for a in EPylonImageOrientation}
drEPylonImageOrientation={a.value:a.name for a in EPylonImageOrientation}


class EPylonKeyFrameSelection(enum.IntEnum):
    KeyFrameSelection_NoKeyFrame=_int32(0)
    KeyFrameSelection_KeyFrame  =enum.auto()
    KeyFrameSelection_Auto      =enum.auto()
dEPylonKeyFrameSelection={a.name:a.value for a in EPylonKeyFrameSelection}
drEPylonKeyFrameSelection={a.value:a.name for a in EPylonKeyFrameSelection}


class EPylonShowWindow(enum.IntEnum):
    EPylonShowWindow_SW_HIDE           =_int32(0)
    EPylonShowWindow_SW_SHOWNORMAL     =_int32(1)
    EPylonShowWindow_SW_SHOWMINIMIZED  =_int32(2)
    EPylonShowWindow_SW_SHOWMAXIMIZED  =_int32(3)
    EPylonShowWindow_SW_SHOWNOACTIVATE =_int32(4)
    EPylonShowWindow_SW_SHOW           =_int32(5)
    EPylonShowWindow_SW_MINIMIZE       =_int32(6)
    EPylonShowWindow_SW_SHOWMINNOACTIVE=_int32(7)
    EPylonShowWindow_SW_SHOWNA         =_int32(8)
    EPylonShowWindow_SW_RESTORE        =_int32(9)
    EPylonShowWindow_SW_SHOWDEFAULT    =_int32(10)
    EPylonShowWindow_SW_FORCEMINIMIZE  =_int32(11)
dEPylonShowWindow={a.name:a.value for a in EPylonShowWindow}
drEPylonShowWindow={a.value:a.name for a in EPylonShowWindow}


class EPylonGigEActionCommandStatus(enum.IntEnum):
    PylonGigEActionCommandStatus_Ok        =_int32(0)
    PylonGigEActionCommandStatus_NoRefTime =_int32((-519995373))
    PylonGigEActionCommandStatus_Overflow  =_int32((-519995371))
    PylonGigEActionCommandStatus_ActionLate=_int32((-519995370))
dEPylonGigEActionCommandStatus={a.name:a.value for a in EPylonGigEActionCommandStatus}
drEPylonGigEActionCommandStatus={a.value:a.name for a in EPylonGigEActionCommandStatus}


class EPylonCompressionStatus(enum.IntEnum):
    CompressionStatus_Ok            =_int32(0)
    CompressionStatus_BufferOverflow=enum.auto()
    CompressionStatus_Error         =enum.auto()
dEPylonCompressionStatus={a.name:a.value for a in EPylonCompressionStatus}
drEPylonCompressionStatus={a.value:a.name for a in EPylonCompressionStatus}


class EPylonCompressionMode(enum.IntEnum):
    CompressionMode_Off           =_int32(0)
    CompressionMode_BaslerLossless=enum.auto()
    CompressionMode_BaslerFixRatio=enum.auto()
dEPylonCompressionMode={a.name:a.value for a in EPylonCompressionMode}
drEPylonCompressionMode={a.value:a.name for a in EPylonCompressionMode}


PYLON_DEVICE_HANDLE=ctypes.c_void_p
PYLON_DEVICE_INFO_HANDLE=ctypes.c_void_p
PYLON_INTERFACE_HANDLE=ctypes.c_void_p
PYLON_INTERFACE_INFO_HANDLE=ctypes.c_void_p
PYLON_STREAMGRABBER_HANDLE=ctypes.c_void_p
PYLON_EVENTGRABBER_HANDLE=ctypes.c_void_p
PYLON_CHUNKPARSER_HANDLE=ctypes.c_void_p
PYLON_EVENTADAPTER_HANDLE=ctypes.c_void_p
PYLON_WAITOBJECT_HANDLE=ctypes.c_void_p
PYLON_WAITOBJECTS_HANDLE=ctypes.c_void_p
PYLON_STREAMBUFFER_HANDLE=ctypes.c_void_p
PYLON_DEVICECALLBACK_HANDLE=ctypes.c_void_p
PYLON_FORMAT_CONVERTER_HANDLE=ctypes.c_void_p
PYLON_IMAGE_FORMAT_CONVERTER_HANDLE=ctypes.c_void_p
PYLON_AVI_WRITER_HANDLE=ctypes.c_void_p
PYLON_IMAGE_DECOMPRESSOR_HANDLE=ctypes.c_void_p
class PylonGrabResult_t(ctypes.Structure):
    _fields_=[  ("Context",ctypes.c_void_p),
                ("hBuffer",PYLON_STREAMBUFFER_HANDLE),
                ("pBuffer",ctypes.c_void_p),
                ("Status",ctypes.c_int),
                ("PayloadType",ctypes.c_int),
                ("PixelType",ctypes.c_int),
                ("TimeStamp",ctypes.c_uint64),
                ("SizeX",ctypes.c_int),
                ("SizeY",ctypes.c_int),
                ("OffsetX",ctypes.c_int),
                ("OffsetY",ctypes.c_int),
                ("PaddingX",ctypes.c_int),
                ("PaddingY",ctypes.c_int),
                ("PayloadSize",ctypes.c_uint64),
                ("ErrorCode",ctypes.c_uint),
                ("BlockID",ctypes.c_uint64) ]
PPylonGrabResult_t=ctypes.POINTER(PylonGrabResult_t)
class CPylonGrabResult_t(ctypes_wrap.CStructWrapper):
    _struct=PylonGrabResult_t


class PylonEventResult_t(ctypes.Structure):
    _fields_=[  ("Buffer",ctypes.c_ubyte*576),
                ("ErrorCode",ctypes.c_uint) ]
PPylonEventResult_t=ctypes.POINTER(PylonEventResult_t)
class CPylonEventResult_t(ctypes_wrap.CStructWrapper):
    _struct=PylonEventResult_t


class PylonImagePersistenceOptions_t(ctypes.Structure):
    _fields_=[  ("quality",ctypes.c_int) ]
PPylonImagePersistenceOptions_t=ctypes.POINTER(PylonImagePersistenceOptions_t)
class CPylonImagePersistenceOptions_t(ctypes_wrap.CStructWrapper):
    _struct=PylonImagePersistenceOptions_t


class PylonGigEActionCommandResult_t(ctypes.Structure):
    _fields_=[  ("DeviceAddress",ctypes.c_char*((12+3)+1)),
                ("Status",ctypes.c_int32) ]
PPylonGigEActionCommandResult_t=ctypes.POINTER(PylonGigEActionCommandResult_t)
class CPylonGigEActionCommandResult_t(ctypes_wrap.CStructWrapper):
    _struct=PylonGigEActionCommandResult_t


class PylonDeviceInfo_t(ctypes.Structure):
    _fields_=[  ("FullName",ctypes.c_char*1024),
                ("FriendlyName",ctypes.c_char*64),
                ("VendorName",ctypes.c_char*64),
                ("ModelName",ctypes.c_char*64),
                ("SerialNumber",ctypes.c_char*64),
                ("DeviceClass",ctypes.c_char*64),
                ("DeviceVersion",ctypes.c_char*64),
                ("UserDefinedName",ctypes.c_char*64) ]
PPylonDeviceInfo_t=ctypes.POINTER(PylonDeviceInfo_t)
class CPylonDeviceInfo_t(ctypes_wrap.CStructWrapper):
    _struct=PylonDeviceInfo_t


class PylonInterfaceInfo_t(ctypes.Structure):
    _fields_=[  ("InterfaceID",ctypes.c_char*64),
                ("DeviceClass",ctypes.c_char*64),
                ("FriendlyName",ctypes.c_char*64),
                ("TlType",ctypes.c_char*64) ]
PPylonInterfaceInfo_t=ctypes.POINTER(PylonInterfaceInfo_t)
class CPylonInterfaceInfo_t(ctypes_wrap.CStructWrapper):
    _struct=PylonInterfaceInfo_t


class PylonCompressionInfo_t(ctypes.Structure):
    _fields_=[  ("HasCompressedImage",ctypes.c_ubyte),
                ("CompressionStatus",ctypes.c_int),
                ("Lossy",ctypes.c_ubyte),
                ("PixelType",ctypes.c_int),
                ("SizeX",ctypes.c_int),
                ("SizeY",ctypes.c_int),
                ("OffsetX",ctypes.c_int),
                ("OffsetY",ctypes.c_int),
                ("PaddingX",ctypes.c_int),
                ("PaddingY",ctypes.c_int),
                ("DecompressedImageSize",ctypes.c_size_t),
                ("DecompressedPayloadSize",ctypes.c_size_t) ]
PPylonCompressionInfo_t=ctypes.POINTER(PylonCompressionInfo_t)
class CPylonCompressionInfo_t(ctypes_wrap.CStructWrapper):
    _struct=PylonCompressionInfo_t


class PfncFormat(enum.IntEnum):
    Mono1p                       =_int32(0x01010037)
    Mono2p                       =_int32(0x01020038)
    Mono4p                       =_int32(0x01040039)
    Mono8                        =_int32(0x01080001)
    Mono8s                       =_int32(0x01080002)
    Mono10                       =_int32(0x01100003)
    Mono10p                      =_int32(0x010A0046)
    Mono12                       =_int32(0x01100005)
    Mono12p                      =_int32(0x010C0047)
    Mono14                       =_int32(0x01100025)
    Mono14p                      =_int32(0x010E0104)
    Mono16                       =_int32(0x01100007)
    Mono32                       =_int32(0x01200111)
    BayerBG4p                    =_int32(0x01040110)
    BayerBG8                     =_int32(0x0108000B)
    BayerBG10                    =_int32(0x0110000F)
    BayerBG10p                   =_int32(0x010A0052)
    BayerBG12                    =_int32(0x01100013)
    BayerBG12p                   =_int32(0x010C0053)
    BayerBG14                    =_int32(0x0110010C)
    BayerBG14p                   =_int32(0x010E0108)
    BayerBG16                    =_int32(0x01100031)
    BayerGB4p                    =_int32(0x0104010F)
    BayerGB8                     =_int32(0x0108000A)
    BayerGB10                    =_int32(0x0110000E)
    BayerGB10p                   =_int32(0x010A0054)
    BayerGB12                    =_int32(0x01100012)
    BayerGB12p                   =_int32(0x010C0055)
    BayerGB14                    =_int32(0x0110010B)
    BayerGB14p                   =_int32(0x010E0107)
    BayerGB16                    =_int32(0x01100030)
    BayerGR4p                    =_int32(0x0104010D)
    BayerGR8                     =_int32(0x01080008)
    BayerGR10                    =_int32(0x0110000C)
    BayerGR10p                   =_int32(0x010A0056)
    BayerGR12                    =_int32(0x01100010)
    BayerGR12p                   =_int32(0x010C0057)
    BayerGR14                    =_int32(0x01100109)
    BayerGR14p                   =_int32(0x010E0105)
    BayerGR16                    =_int32(0x0110002E)
    BayerRG4p                    =_int32(0x0104010E)
    BayerRG8                     =_int32(0x01080009)
    BayerRG10                    =_int32(0x0110000D)
    BayerRG10p                   =_int32(0x010A0058)
    BayerRG12                    =_int32(0x01100011)
    BayerRG12p                   =_int32(0x010C0059)
    BayerRG14                    =_int32(0x0110010A)
    BayerRG14p                   =_int32(0x010E0106)
    BayerRG16                    =_int32(0x0110002F)
    RGBa8                        =_int32(0x02200016)
    RGBa10                       =_int32(0x0240005F)
    RGBa10p                      =_int32(0x02280060)
    RGBa12                       =_int32(0x02400061)
    RGBa12p                      =_int32(0x02300062)
    RGBa14                       =_int32(0x02400063)
    RGBa16                       =_int32(0x02400064)
    RGB8                         =_int32(0x02180014)
    RGB8_Planar                  =_int32(0x02180021)
    RGB10                        =_int32(0x02300018)
    RGB10_Planar                 =_int32(0x02300022)
    RGB10p                       =_int32(0x021E005C)
    RGB10p32                     =_int32(0x0220001D)
    RGB12                        =_int32(0x0230001A)
    RGB12_Planar                 =_int32(0x02300023)
    RGB12p                       =_int32(0x0224005D)
    RGB14                        =_int32(0x0230005E)
    RGB16                        =_int32(0x02300033)
    RGB16_Planar                 =_int32(0x02300024)
    RGB565p                      =_int32(0x02100035)
    BGRa8                        =_int32(0x02200017)
    BGRa10                       =_int32(0x0240004C)
    BGRa10p                      =_int32(0x0228004D)
    BGRa12                       =_int32(0x0240004E)
    BGRa12p                      =_int32(0x0230004F)
    BGRa14                       =_int32(0x02400050)
    BGRa16                       =_int32(0x02400051)
    BGR8                         =_int32(0x02180015)
    BGR10                        =_int32(0x02300019)
    BGR10p                       =_int32(0x021E0048)
    BGR12                        =_int32(0x0230001B)
    BGR12p                       =_int32(0x02240049)
    BGR14                        =_int32(0x0230004A)
    BGR16                        =_int32(0x0230004B)
    BGR565p                      =_int32(0x02100036)
    R8                           =_int32(0x010800C9)
    R10                          =_int32(0x010A00CA)
    R12                          =_int32(0x010C00CB)
    R16                          =_int32(0x011000CC)
    G8                           =_int32(0x010800CD)
    G10                          =_int32(0x010A00CE)
    G12                          =_int32(0x010C00CF)
    G16                          =_int32(0x011000D0)
    B8                           =_int32(0x010800D1)
    B10                          =_int32(0x010A00D2)
    B12                          =_int32(0x010C00D3)
    B16                          =_int32(0x011000D4)
    Coord3D_ABC8                 =_int32(0x021800B2)
    Coord3D_ABC8_Planar          =_int32(0x021800B3)
    Coord3D_ABC10p               =_int32(0x021E00DB)
    Coord3D_ABC10p_Planar        =_int32(0x021E00DC)
    Coord3D_ABC12p               =_int32(0x022400DE)
    Coord3D_ABC12p_Planar        =_int32(0x022400DF)
    Coord3D_ABC16                =_int32(0x023000B9)
    Coord3D_ABC16_Planar         =_int32(0x023000BA)
    Coord3D_ABC32f               =_int32(0x026000C0)
    Coord3D_ABC32f_Planar        =_int32(0x026000C1)
    Coord3D_AC8                  =_int32(0x021000B4)
    Coord3D_AC8_Planar           =_int32(0x021000B5)
    Coord3D_AC10p                =_int32(0x021400F0)
    Coord3D_AC10p_Planar         =_int32(0x021400F1)
    Coord3D_AC12p                =_int32(0x021800F2)
    Coord3D_AC12p_Planar         =_int32(0x021800F3)
    Coord3D_AC16                 =_int32(0x022000BB)
    Coord3D_AC16_Planar          =_int32(0x022000BC)
    Coord3D_AC32f                =_int32(0x024000C2)
    Coord3D_AC32f_Planar         =_int32(0x024000C3)
    Coord3D_A8                   =_int32(0x010800AF)
    Coord3D_A10p                 =_int32(0x010A00D5)
    Coord3D_A12p                 =_int32(0x010C00D8)
    Coord3D_A16                  =_int32(0x011000B6)
    Coord3D_A32f                 =_int32(0x012000BD)
    Coord3D_B8                   =_int32(0x010800B0)
    Coord3D_B10p                 =_int32(0x010A00D6)
    Coord3D_B12p                 =_int32(0x010C00D9)
    Coord3D_B16                  =_int32(0x011000B7)
    Coord3D_B32f                 =_int32(0x012000BE)
    Coord3D_C8                   =_int32(0x010800B1)
    Coord3D_C10p                 =_int32(0x010A00D7)
    Coord3D_C12p                 =_int32(0x010C00DA)
    Coord3D_C16                  =_int32(0x011000B8)
    Coord3D_C32f                 =_int32(0x012000BF)
    Confidence1                  =_int32(0x010800C4)
    Confidence1p                 =_int32(0x010100C5)
    Confidence8                  =_int32(0x010800C6)
    Confidence16                 =_int32(0x011000C7)
    Confidence32f                =_int32(0x012000C8)
    BiColorBGRG8                 =_int32(0x021000A6)
    BiColorBGRG10                =_int32(0x022000A9)
    BiColorBGRG10p               =_int32(0x021400AA)
    BiColorBGRG12                =_int32(0x022000AD)
    BiColorBGRG12p               =_int32(0x021800AE)
    BiColorRGBG8                 =_int32(0x021000A5)
    BiColorRGBG10                =_int32(0x022000A7)
    BiColorRGBG10p               =_int32(0x021400A8)
    BiColorRGBG12                =_int32(0x022000AB)
    BiColorRGBG12p               =_int32(0x021800AC)
    Data8                        =_int32(0x01080116)
    Data8s                       =_int32(0x01080117)
    Data16                       =_int32(0x01100118)
    Data16s                      =_int32(0x01100119)
    Data32                       =_int32(0x0120011A)
    Data32f                      =_int32(0x0120011C)
    Data32s                      =_int32(0x0120011B)
    Data64                       =_int32(0x0140011D)
    Data64f                      =_int32(0x0140011F)
    Data64s                      =_int32(0x0140011E)
    SCF1WBWG8                    =_int32(0x01080067)
    SCF1WBWG10                   =_int32(0x01100068)
    SCF1WBWG10p                  =_int32(0x010A0069)
    SCF1WBWG12                   =_int32(0x0110006A)
    SCF1WBWG12p                  =_int32(0x010C006B)
    SCF1WBWG14                   =_int32(0x0110006C)
    SCF1WBWG16                   =_int32(0x0110006D)
    SCF1WGWB8                    =_int32(0x0108006E)
    SCF1WGWB10                   =_int32(0x0110006F)
    SCF1WGWB10p                  =_int32(0x010A0070)
    SCF1WGWB12                   =_int32(0x01100071)
    SCF1WGWB12p                  =_int32(0x010C0072)
    SCF1WGWB14                   =_int32(0x01100073)
    SCF1WGWB16                   =_int32(0x01100074)
    SCF1WGWR8                    =_int32(0x01080075)
    SCF1WGWR10                   =_int32(0x01100076)
    SCF1WGWR10p                  =_int32(0x010A0077)
    SCF1WGWR12                   =_int32(0x01100078)
    SCF1WGWR12p                  =_int32(0x010C0079)
    SCF1WGWR14                   =_int32(0x0110007A)
    SCF1WGWR16                   =_int32(0x0110007B)
    SCF1WRWG8                    =_int32(0x0108007C)
    SCF1WRWG10                   =_int32(0x0110007D)
    SCF1WRWG10p                  =_int32(0x010A007E)
    SCF1WRWG12                   =_int32(0x0110007F)
    SCF1WRWG12p                  =_int32(0x010C0080)
    SCF1WRWG14                   =_int32(0x01100081)
    SCF1WRWG16                   =_int32(0x01100082)
    YCbCr8                       =_int32(0x0218005B)
    YCbCr8_CbYCr                 =_int32(0x0218003A)
    YCbCr10_CbYCr                =_int32(0x02300083)
    YCbCr10p_CbYCr               =_int32(0x021E0084)
    YCbCr12_CbYCr                =_int32(0x02300085)
    YCbCr12p_CbYCr               =_int32(0x02240086)
    YCbCr411_8                   =_int32(0x020C005A)
    YCbCr411_8_CbYYCrYY          =_int32(0x020C003C)
    YCbCr420_8_YY_CbCr_Semiplanar=_int32(0x020C0112)
    YCbCr420_8_YY_CrCb_Semiplanar=_int32(0x020C0114)
    YCbCr422_8                   =_int32(0x0210003B)
    YCbCr422_8_CbYCrY            =_int32(0x02100043)
    YCbCr422_8_YY_CbCr_Semiplanar=_int32(0x02100113)
    YCbCr422_8_YY_CrCb_Semiplanar=_int32(0x02100115)
    YCbCr422_10                  =_int32(0x02200065)
    YCbCr422_10_CbYCrY           =_int32(0x02200099)
    YCbCr422_10p                 =_int32(0x02140087)
    YCbCr422_10p_CbYCrY          =_int32(0x0214009A)
    YCbCr422_12                  =_int32(0x02200066)
    YCbCr422_12_CbYCrY           =_int32(0x0220009B)
    YCbCr422_12p                 =_int32(0x02180088)
    YCbCr422_12p_CbYCrY          =_int32(0x0218009C)
    YCbCr601_8_CbYCr             =_int32(0x0218003D)
    YCbCr601_10_CbYCr            =_int32(0x02300089)
    YCbCr601_10p_CbYCr           =_int32(0x021E008A)
    YCbCr601_12_CbYCr            =_int32(0x0230008B)
    YCbCr601_12p_CbYCr           =_int32(0x0224008C)
    YCbCr601_411_8_CbYYCrYY      =_int32(0x020C003F)
    YCbCr601_422_8               =_int32(0x0210003E)
    YCbCr601_422_8_CbYCrY        =_int32(0x02100044)
    YCbCr601_422_10              =_int32(0x0220008D)
    YCbCr601_422_10_CbYCrY       =_int32(0x0220009D)
    YCbCr601_422_10p             =_int32(0x0214008E)
    YCbCr601_422_10p_CbYCrY      =_int32(0x0214009E)
    YCbCr601_422_12              =_int32(0x0220008F)
    YCbCr601_422_12_CbYCrY       =_int32(0x0220009F)
    YCbCr601_422_12p             =_int32(0x02180090)
    YCbCr601_422_12p_CbYCrY      =_int32(0x021800A0)
    YCbCr709_8_CbYCr             =_int32(0x02180040)
    YCbCr709_10_CbYCr            =_int32(0x02300091)
    YCbCr709_10p_CbYCr           =_int32(0x021E0092)
    YCbCr709_12_CbYCr            =_int32(0x02300093)
    YCbCr709_12p_CbYCr           =_int32(0x02240094)
    YCbCr709_411_8_CbYYCrYY      =_int32(0x020C0042)
    YCbCr709_422_8               =_int32(0x02100041)
    YCbCr709_422_8_CbYCrY        =_int32(0x02100045)
    YCbCr709_422_10              =_int32(0x02200095)
    YCbCr709_422_10_CbYCrY       =_int32(0x022000A1)
    YCbCr709_422_10p             =_int32(0x02140096)
    YCbCr709_422_10p_CbYCrY      =_int32(0x021400A2)
    YCbCr709_422_12              =_int32(0x02200097)
    YCbCr709_422_12_CbYCrY       =_int32(0x022000A3)
    YCbCr709_422_12p             =_int32(0x02180098)
    YCbCr709_422_12p_CbYCrY      =_int32(0x021800A4)
    YCbCr2020_8_CbYCr            =_int32(0x021800F4)
    YCbCr2020_10_CbYCr           =_int32(0x023000F5)
    YCbCr2020_10p_CbYCr          =_int32(0x021E00F6)
    YCbCr2020_12_CbYCr           =_int32(0x023000F7)
    YCbCr2020_12p_CbYCr          =_int32(0x022400F8)
    YCbCr2020_411_8_CbYYCrYY     =_int32(0x020C00F9)
    YCbCr2020_422_8              =_int32(0x021000FA)
    YCbCr2020_422_8_CbYCrY       =_int32(0x021000FB)
    YCbCr2020_422_10             =_int32(0x022000FC)
    YCbCr2020_422_10_CbYCrY      =_int32(0x022000FD)
    YCbCr2020_422_10p            =_int32(0x021400FE)
    YCbCr2020_422_10p_CbYCrY     =_int32(0x021400FF)
    YCbCr2020_422_12             =_int32(0x02200100)
    YCbCr2020_422_12_CbYCrY      =_int32(0x02200101)
    YCbCr2020_422_12p            =_int32(0x02180102)
    YCbCr2020_422_12p_CbYCrY     =_int32(0x02180103)
    YUV8_UYV                     =_int32(0x02180020)
    YUV411_8_UYYVYY              =_int32(0x020C001E)
    YUV422_8                     =_int32(0x02100032)
    YUV422_8_UYVY                =_int32(0x0210001F)
    Mono10Packed                 =_int32(0x010C0004)
    Mono12Packed                 =_int32(0x010C0006)
    BayerBG10Packed              =_int32(0x010C0029)
    BayerBG12Packed              =_int32(0x010C002D)
    BayerGB10Packed              =_int32(0x010C0028)
    BayerGB12Packed              =_int32(0x010C002C)
    BayerGR10Packed              =_int32(0x010C0026)
    BayerGR12Packed              =_int32(0x010C002A)
    BayerRG10Packed              =_int32(0x010C0027)
    BayerRG12Packed              =_int32(0x010C002B)
    RGB10V1Packed                =_int32(0x0220001C)
    RGB12V1Packed                =_int32(0x02240034)
    InvalidPixelFormat           =_int32(0)
dPfncFormat={a.name:a.value for a in PfncFormat}
drPfncFormat={a.value:a.name for a in PfncFormat}





##### FUNCTION DEFINITIONS #####





def addfunc(lib, name, restype, argtypes=None, argnames=None):
    if getattr(lib,name,None) is None:
        setattr(lib,name,None)
    else:
        func=getattr(lib,name)
        func.restype=restype
        if argtypes is not None:
            func.argtypes=argtypes
        if argnames is not None:
            func.argnames=argnames

def define_functions(lib):
    #  HRESULT GenApiGetLastErrorMessage(ctypes.c_char_p pBuf, ctypes.POINTER(ctypes.c_size_t) pBufLen)
    addfunc(lib, "GenApiGetLastErrorMessage", restype = HRESULT,
            argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["pBuf", "pBufLen"] )
    #  HRESULT GenApiGetLastErrorDetail(ctypes.c_char_p pBuf, ctypes.POINTER(ctypes.c_size_t) pBufLen)
    addfunc(lib, "GenApiGetLastErrorDetail", restype = HRESULT,
            argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["pBuf", "pBufLen"] )
    #  HRESULT GenApiNodeMapGetNode(NODEMAP_HANDLE hMap, ctypes.c_char_p pName, ctypes.POINTER(NODE_HANDLE) phNode)
    addfunc(lib, "GenApiNodeMapGetNode", restype = HRESULT,
            argtypes = [NODEMAP_HANDLE, ctypes.c_char_p, ctypes.POINTER(NODE_HANDLE)],
            argnames = ["hMap", "pName", "phNode"] )
    #  HRESULT GenApiNodeMapGetNumNodes(NODEMAP_HANDLE hMap, ctypes.POINTER(ctypes.c_size_t) pValue)
    addfunc(lib, "GenApiNodeMapGetNumNodes", restype = HRESULT,
            argtypes = [NODEMAP_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hMap", "pValue"] )
    #  HRESULT GenApiNodeMapGetNodeByIndex(NODEMAP_HANDLE hMap, ctypes.c_size_t index, ctypes.POINTER(NODE_HANDLE) phNode)
    addfunc(lib, "GenApiNodeMapGetNodeByIndex", restype = HRESULT,
            argtypes = [NODEMAP_HANDLE, ctypes.c_size_t, ctypes.POINTER(NODE_HANDLE)],
            argnames = ["hMap", "index", "phNode"] )
    #  HRESULT GenApiNodeMapPoll(NODEMAP_HANDLE hMap, ctypes.c_int64 timestamp)
    addfunc(lib, "GenApiNodeMapPoll", restype = HRESULT,
            argtypes = [NODEMAP_HANDLE, ctypes.c_int64],
            argnames = ["hMap", "timestamp"] )
    #  HRESULT GenApiNodeGetAccessMode(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int) pAccessMode)
    addfunc(lib, "GenApiNodeGetAccessMode", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hNode", "pAccessMode"] )
    #  HRESULT GenApiNodeGetName(NODE_HANDLE hNode, ctypes.c_char_p pBuf, ctypes.POINTER(ctypes.c_size_t) pBufLen)
    addfunc(lib, "GenApiNodeGetName", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hNode", "pBuf", "pBufLen"] )
    #  HRESULT GenApiNodeGetNameSpace(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int) pNamespace)
    addfunc(lib, "GenApiNodeGetNameSpace", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hNode", "pNamespace"] )
    #  HRESULT GenApiNodeGetVisibility(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int) pVisibility)
    addfunc(lib, "GenApiNodeGetVisibility", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hNode", "pVisibility"] )
    #  HRESULT GenApiNodeInvalidateNode(NODE_HANDLE hNode)
    addfunc(lib, "GenApiNodeInvalidateNode", restype = HRESULT,
            argtypes = [NODE_HANDLE],
            argnames = ["hNode"] )
    #  HRESULT GenApiNodeGetCachingMode(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int) pCachingMode)
    addfunc(lib, "GenApiNodeGetCachingMode", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hNode", "pCachingMode"] )
    #  HRESULT GenApiNodeGetToolTip(NODE_HANDLE hNode, ctypes.c_char_p pBuf, ctypes.POINTER(ctypes.c_size_t) pBufLen)
    addfunc(lib, "GenApiNodeGetToolTip", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hNode", "pBuf", "pBufLen"] )
    #  HRESULT GenApiNodeGetDescription(NODE_HANDLE hNode, ctypes.c_char_p pBuf, ctypes.POINTER(ctypes.c_size_t) pBufLen)
    addfunc(lib, "GenApiNodeGetDescription", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hNode", "pBuf", "pBufLen"] )
    #  HRESULT GenApiNodeGetDisplayName(NODE_HANDLE hNode, ctypes.c_char_p pBuf, ctypes.POINTER(ctypes.c_size_t) pBufLen)
    addfunc(lib, "GenApiNodeGetDisplayName", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hNode", "pBuf", "pBufLen"] )
    #  HRESULT GenApiNodeGetType(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int) pType)
    addfunc(lib, "GenApiNodeGetType", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hNode", "pType"] )
    #  HRESULT GenApiNodeGetPollingTime(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int64) pPollingTime)
    addfunc(lib, "GenApiNodeGetPollingTime", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int64)],
            argnames = ["hNode", "pPollingTime"] )
    #  HRESULT GenApiNodeRegisterCallback(NODE_HANDLE hNode, ctypes.c_void_p pCbFunction, ctypes.POINTER(NODE_CALLBACK_HANDLE) phCb)
    addfunc(lib, "GenApiNodeRegisterCallback", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_void_p, ctypes.POINTER(NODE_CALLBACK_HANDLE)],
            argnames = ["hNode", "pCbFunction", "phCb"] )
    #  HRESULT GenApiNodeDeregisterCallback(NODE_HANDLE hNode, NODE_CALLBACK_HANDLE hCb)
    addfunc(lib, "GenApiNodeDeregisterCallback", restype = HRESULT,
            argtypes = [NODE_HANDLE, NODE_CALLBACK_HANDLE],
            argnames = ["hNode", "hCb"] )
    #  HRESULT GenApiNodeImposeAccessMode(NODE_HANDLE hNode, ctypes.c_int imposedAccessMode)
    addfunc(lib, "GenApiNodeImposeAccessMode", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_int],
            argnames = ["hNode", "imposedAccessMode"] )
    #  HRESULT GenApiNodeImposeVisibility(NODE_HANDLE hNode, ctypes.c_int imposedVisibility)
    addfunc(lib, "GenApiNodeImposeVisibility", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_int],
            argnames = ["hNode", "imposedVisibility"] )
    #  HRESULT GenApiNodeIsImplemented(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "GenApiNodeIsImplemented", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hNode", "pResult"] )
    #  HRESULT GenApiNodeIsReadable(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "GenApiNodeIsReadable", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hNode", "pResult"] )
    #  HRESULT GenApiNodeIsWritable(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "GenApiNodeIsWritable", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hNode", "pResult"] )
    #  HRESULT GenApiNodeIsAvailable(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "GenApiNodeIsAvailable", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hNode", "pResult"] )
    #  HRESULT GenApiNodeToString(NODE_HANDLE hNode, ctypes.c_char_p pBuf, ctypes.POINTER(ctypes.c_size_t) pBufLen)
    addfunc(lib, "GenApiNodeToString", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hNode", "pBuf", "pBufLen"] )
    #  HRESULT GenApiNodeToStringEx(NODE_HANDLE hNode, ctypes.c_ubyte verify, ctypes.c_char_p pBuf, ctypes.POINTER(ctypes.c_size_t) pBufLen)
    addfunc(lib, "GenApiNodeToStringEx", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_ubyte, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hNode", "verify", "pBuf", "pBufLen"] )
    #  HRESULT GenApiNodeFromStringEx(NODE_HANDLE hNode, ctypes.c_ubyte verify, ctypes.c_char_p pString)
    addfunc(lib, "GenApiNodeFromStringEx", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_ubyte, ctypes.c_char_p],
            argnames = ["hNode", "verify", "pString"] )
    #  HRESULT GenApiNodeFromString(NODE_HANDLE hNode, ctypes.c_char_p pString)
    addfunc(lib, "GenApiNodeFromString", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_char_p],
            argnames = ["hNode", "pString"] )
    #  HRESULT GenApiNodeGetAlias(NODE_HANDLE hNode, ctypes.POINTER(NODE_HANDLE) phNode)
    addfunc(lib, "GenApiNodeGetAlias", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(NODE_HANDLE)],
            argnames = ["hNode", "phNode"] )
    #  HRESULT GenApiIntegerSetValue(NODE_HANDLE hNode, ctypes.c_int64 value)
    addfunc(lib, "GenApiIntegerSetValue", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_int64],
            argnames = ["hNode", "value"] )
    #  HRESULT GenApiIntegerSetValueEx(NODE_HANDLE hNode, ctypes.c_ubyte verify, ctypes.c_int64 value)
    addfunc(lib, "GenApiIntegerSetValueEx", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_ubyte, ctypes.c_int64],
            argnames = ["hNode", "verify", "value"] )
    #  HRESULT GenApiIntegerGetValue(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int64) pValue)
    addfunc(lib, "GenApiIntegerGetValue", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int64)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiIntegerGetValueEx(NODE_HANDLE hNode, ctypes.c_ubyte verify, ctypes.POINTER(ctypes.c_int64) pValue)
    addfunc(lib, "GenApiIntegerGetValueEx", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_ubyte, ctypes.POINTER(ctypes.c_int64)],
            argnames = ["hNode", "verify", "pValue"] )
    #  HRESULT GenApiIntegerGetMin(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int64) pValue)
    addfunc(lib, "GenApiIntegerGetMin", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int64)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiIntegerGetMax(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int64) pValue)
    addfunc(lib, "GenApiIntegerGetMax", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int64)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiIntegerGetInc(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int64) pValue)
    addfunc(lib, "GenApiIntegerGetInc", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int64)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiIntegerGetRepresentation(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int) pValue)
    addfunc(lib, "GenApiIntegerGetRepresentation", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiBooleanSetValue(NODE_HANDLE hNode, ctypes.c_ubyte value)
    addfunc(lib, "GenApiBooleanSetValue", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_ubyte],
            argnames = ["hNode", "value"] )
    #  HRESULT GenApiBooleanGetValue(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_ubyte) pValue)
    addfunc(lib, "GenApiBooleanGetValue", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiFloatSetValue(NODE_HANDLE hNode, ctypes.c_double value)
    addfunc(lib, "GenApiFloatSetValue", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_double],
            argnames = ["hNode", "value"] )
    #  HRESULT GenApiFloatSetValueEx(NODE_HANDLE hNode, ctypes.c_ubyte verify, ctypes.c_double value)
    addfunc(lib, "GenApiFloatSetValueEx", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_ubyte, ctypes.c_double],
            argnames = ["hNode", "verify", "value"] )
    #  HRESULT GenApiFloatGetValue(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_double) pValue)
    addfunc(lib, "GenApiFloatGetValue", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_double)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiFloatGetValueEx(NODE_HANDLE hNode, ctypes.c_ubyte verify, ctypes.POINTER(ctypes.c_double) pValue)
    addfunc(lib, "GenApiFloatGetValueEx", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_ubyte, ctypes.POINTER(ctypes.c_double)],
            argnames = ["hNode", "verify", "pValue"] )
    #  HRESULT GenApiFloatGetMin(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_double) pValue)
    addfunc(lib, "GenApiFloatGetMin", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_double)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiFloatGetMax(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_double) pValue)
    addfunc(lib, "GenApiFloatGetMax", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_double)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiFloatGetRepresentation(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int) pValue)
    addfunc(lib, "GenApiFloatGetRepresentation", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiFloatGetUnit(NODE_HANDLE hNode, ctypes.c_char_p pBuf, ctypes.POINTER(ctypes.c_size_t) pBufLen)
    addfunc(lib, "GenApiFloatGetUnit", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hNode", "pBuf", "pBufLen"] )
    #  HRESULT GenApiCommandExecute(NODE_HANDLE hNode)
    addfunc(lib, "GenApiCommandExecute", restype = HRESULT,
            argtypes = [NODE_HANDLE],
            argnames = ["hNode"] )
    #  HRESULT GenApiCommandIsDone(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_ubyte) pValue)
    addfunc(lib, "GenApiCommandIsDone", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiEnumerationGetNumEntries(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_size_t) pValue)
    addfunc(lib, "GenApiEnumerationGetNumEntries", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiEnumerationGetEntryByIndex(NODE_HANDLE hNode, ctypes.c_size_t index, ctypes.POINTER(NODE_HANDLE) pEntry)
    addfunc(lib, "GenApiEnumerationGetEntryByIndex", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_size_t, ctypes.POINTER(NODE_HANDLE)],
            argnames = ["hNode", "index", "pEntry"] )
    #  HRESULT GenApiEnumerationGetEntryByName(NODE_HANDLE hNode, ctypes.c_char_p pName, ctypes.POINTER(NODE_HANDLE) pEntry)
    addfunc(lib, "GenApiEnumerationGetEntryByName", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_char_p, ctypes.POINTER(NODE_HANDLE)],
            argnames = ["hNode", "pName", "pEntry"] )
    #  HRESULT GenApiEnumerationEntryGetValue(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int) pValue)
    addfunc(lib, "GenApiEnumerationEntryGetValue", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiEnumerationEntryGetSymbolic(NODE_HANDLE hNode, ctypes.c_char_p pBuf, ctypes.POINTER(ctypes.c_size_t) pBufLen)
    addfunc(lib, "GenApiEnumerationEntryGetSymbolic", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hNode", "pBuf", "pBufLen"] )
    #  HRESULT GenApiSelectorGetNumSelectingFeatures(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_size_t) pValue)
    addfunc(lib, "GenApiSelectorGetNumSelectingFeatures", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiSelectorGetSelectingFeatureByIndex(NODE_HANDLE hNode, ctypes.c_size_t index, ctypes.POINTER(NODE_HANDLE) phNode)
    addfunc(lib, "GenApiSelectorGetSelectingFeatureByIndex", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_size_t, ctypes.POINTER(NODE_HANDLE)],
            argnames = ["hNode", "index", "phNode"] )
    #  HRESULT GenApiSelectorGetNumSelectedFeatures(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_size_t) pValue)
    addfunc(lib, "GenApiSelectorGetNumSelectedFeatures", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiSelectorGetSelectedFeatureByIndex(NODE_HANDLE hNode, ctypes.c_size_t index, ctypes.POINTER(NODE_HANDLE) phNode)
    addfunc(lib, "GenApiSelectorGetSelectedFeatureByIndex", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_size_t, ctypes.POINTER(NODE_HANDLE)],
            argnames = ["hNode", "index", "phNode"] )
    #  HRESULT GenApiRegisterGetValue(NODE_HANDLE hNode, ctypes.c_void_p pBuffer, ctypes.POINTER(ctypes.c_size_t) pLength)
    addfunc(lib, "GenApiRegisterGetValue", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hNode", "pBuffer", "pLength"] )
    #  HRESULT GenApiRegisterSetValue(NODE_HANDLE hNode, ctypes.c_void_p pBuffer, ctypes.c_size_t length)
    addfunc(lib, "GenApiRegisterSetValue", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_void_p, ctypes.c_size_t],
            argnames = ["hNode", "pBuffer", "length"] )
    #  HRESULT GenApiRegisterGetLength(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_size_t) pLength)
    addfunc(lib, "GenApiRegisterGetLength", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hNode", "pLength"] )
    #  HRESULT GenApiRegisterGetAddress(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int64) pAddress)
    addfunc(lib, "GenApiRegisterGetAddress", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int64)],
            argnames = ["hNode", "pAddress"] )
    #  HRESULT GenApiCategoryGetNumFeatures(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_size_t) pValue)
    addfunc(lib, "GenApiCategoryGetNumFeatures", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiCategoryGetFeatureByIndex(NODE_HANDLE hNode, ctypes.c_size_t index, ctypes.POINTER(NODE_HANDLE) phEntry)
    addfunc(lib, "GenApiCategoryGetFeatureByIndex", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_size_t, ctypes.POINTER(NODE_HANDLE)],
            argnames = ["hNode", "index", "phEntry"] )
    #  HRESULT GenApiPortRead(NODE_HANDLE hNode, ctypes.c_void_p pBuffer, ctypes.c_int64 Address, ctypes.c_size_t Length)
    addfunc(lib, "GenApiPortRead", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_void_p, ctypes.c_int64, ctypes.c_size_t],
            argnames = ["hNode", "pBuffer", "Address", "Length"] )
    #  HRESULT GenApiPortWrite(NODE_HANDLE hNode, ctypes.c_void_p pBuffer, ctypes.c_int64 Address, ctypes.c_size_t Length)
    addfunc(lib, "GenApiPortWrite", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_void_p, ctypes.c_int64, ctypes.c_size_t],
            argnames = ["hNode", "pBuffer", "Address", "Length"] )
    #  HRESULT GenApiFilesAreSupported(NODEMAP_HANDLE hMap, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "GenApiFilesAreSupported", restype = HRESULT,
            argtypes = [NODEMAP_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hMap", "pResult"] )
    #  HRESULT GenApiFileExists(NODEMAP_HANDLE hMap, ctypes.c_char_p pFileName, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "GenApiFileExists", restype = HRESULT,
            argtypes = [NODEMAP_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hMap", "pFileName", "pResult"] )
    #  HRESULT GenApiFileOpen(NODEMAP_HANDLE hMap, ctypes.c_char_p pFileName, ctypes.c_int accessMode, ctypes.POINTER(GENAPI_FILE_HANDLE) phFile)
    addfunc(lib, "GenApiFileOpen", restype = HRESULT,
            argtypes = [NODEMAP_HANDLE, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(GENAPI_FILE_HANDLE)],
            argnames = ["hMap", "pFileName", "accessMode", "phFile"] )
    #  HRESULT GenApiFileRead(GENAPI_FILE_HANDLE hFile, ctypes.c_void_p pBuffer, ctypes.POINTER(ctypes.c_size_t) pLength)
    addfunc(lib, "GenApiFileRead", restype = HRESULT,
            argtypes = [GENAPI_FILE_HANDLE, ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hFile", "pBuffer", "pLength"] )
    #  HRESULT GenApiFileWrite(GENAPI_FILE_HANDLE hFile, ctypes.c_void_p pBuffer, ctypes.c_size_t length)
    addfunc(lib, "GenApiFileWrite", restype = HRESULT,
            argtypes = [GENAPI_FILE_HANDLE, ctypes.c_void_p, ctypes.c_size_t],
            argnames = ["hFile", "pBuffer", "length"] )
    #  HRESULT GenApiFileClose(GENAPI_FILE_HANDLE hFile)
    addfunc(lib, "GenApiFileClose", restype = HRESULT,
            argtypes = [GENAPI_FILE_HANDLE],
            argnames = ["hFile"] )
    #  HRESULT GenApiNodeGetPollingTimeInt32(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int32) pollingTime)
    addfunc(lib, "GenApiNodeGetPollingTimeInt32", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int32)],
            argnames = ["hNode", "pollingTime"] )
    #  HRESULT GenApiIntegerSetValueInt32(NODE_HANDLE hNode, ctypes.c_int32 value)
    addfunc(lib, "GenApiIntegerSetValueInt32", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_int32],
            argnames = ["hNode", "value"] )
    #  HRESULT GenApiIntegerSetValueExInt32(NODE_HANDLE hNode, ctypes.c_ubyte verify, ctypes.c_int32 value)
    addfunc(lib, "GenApiIntegerSetValueExInt32", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_ubyte, ctypes.c_int32],
            argnames = ["hNode", "verify", "value"] )
    #  HRESULT GenApiIntegerGetValueInt32(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int32) pValue)
    addfunc(lib, "GenApiIntegerGetValueInt32", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int32)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiIntegerGetValueExInt32(NODE_HANDLE hNode, ctypes.c_ubyte verify, ctypes.POINTER(ctypes.c_int32) pValue)
    addfunc(lib, "GenApiIntegerGetValueExInt32", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.c_ubyte, ctypes.POINTER(ctypes.c_int32)],
            argnames = ["hNode", "verify", "pValue"] )
    #  HRESULT GenApiIntegerGetMinInt32(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int32) pValue)
    addfunc(lib, "GenApiIntegerGetMinInt32", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int32)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiIntegerGetMaxInt32(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int32) pValue)
    addfunc(lib, "GenApiIntegerGetMaxInt32", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int32)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiIntegerGetIncInt32(NODE_HANDLE hNode, ctypes.POINTER(ctypes.c_int32) pValue)
    addfunc(lib, "GenApiIntegerGetIncInt32", restype = HRESULT,
            argtypes = [NODE_HANDLE, ctypes.POINTER(ctypes.c_int32)],
            argnames = ["hNode", "pValue"] )
    #  HRESULT GenApiNodeMapPollInt32(NODEMAP_HANDLE hMap, ctypes.c_int32 timestamp)
    addfunc(lib, "GenApiNodeMapPollInt32", restype = HRESULT,
            argtypes = [NODEMAP_HANDLE, ctypes.c_int32],
            argnames = ["hMap", "timestamp"] )
    #  HRESULT PylonInitialize()
    addfunc(lib, "PylonInitialize", restype = HRESULT,
            argtypes = [],
            argnames = [] )
    #  HRESULT PylonTerminate()
    addfunc(lib, "PylonTerminate", restype = HRESULT,
            argtypes = [],
            argnames = [] )
    #  HRESULT PylonSetProperty(ctypes.c_int propertyId, ctypes.c_void_p pData, ctypes.c_size_t size)
    addfunc(lib, "PylonSetProperty", restype = HRESULT,
            argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_size_t],
            argnames = ["propertyId", "pData", "size"] )
    #  HRESULT PylonGetProperty(ctypes.c_int propertyId, ctypes.c_void_p pData, ctypes.POINTER(ctypes.c_size_t) pSize)
    addfunc(lib, "PylonGetProperty", restype = HRESULT,
            argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["propertyId", "pData", "pSize"] )
    #  HRESULT PylonEnumerateInterfaces(ctypes.POINTER(ctypes.c_size_t) numInterfaces)
    addfunc(lib, "PylonEnumerateInterfaces", restype = HRESULT,
            argtypes = [ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["numInterfaces"] )
    #  HRESULT PylonEnumerateInterfacesByDeviceClass(ctypes.c_char_p pDeviceClass, ctypes.POINTER(ctypes.c_size_t) numInterfaces)
    addfunc(lib, "PylonEnumerateInterfacesByDeviceClass", restype = HRESULT,
            argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["pDeviceClass", "numInterfaces"] )
    #  HRESULT PylonGetInterfaceInfo(ctypes.c_size_t index, ctypes.POINTER(PylonInterfaceInfo_t) pIfInfo)
    addfunc(lib, "PylonGetInterfaceInfo", restype = HRESULT,
            argtypes = [ctypes.c_size_t, ctypes.POINTER(PylonInterfaceInfo_t)],
            argnames = ["index", "pIfInfo"] )
    #  HRESULT PylonCreateInterfaceByIndex(ctypes.c_size_t index, ctypes.POINTER(PYLON_INTERFACE_HANDLE) phIf)
    addfunc(lib, "PylonCreateInterfaceByIndex", restype = HRESULT,
            argtypes = [ctypes.c_size_t, ctypes.POINTER(PYLON_INTERFACE_HANDLE)],
            argnames = ["index", "phIf"] )
    #  HRESULT PylonDestroyInterface(PYLON_INTERFACE_HANDLE hIf)
    addfunc(lib, "PylonDestroyInterface", restype = HRESULT,
            argtypes = [PYLON_INTERFACE_HANDLE],
            argnames = ["hIf"] )
    #  HRESULT PylonInterfaceOpen(PYLON_INTERFACE_HANDLE hIf)
    addfunc(lib, "PylonInterfaceOpen", restype = HRESULT,
            argtypes = [PYLON_INTERFACE_HANDLE],
            argnames = ["hIf"] )
    #  HRESULT PylonInterfaceClose(PYLON_INTERFACE_HANDLE hIf)
    addfunc(lib, "PylonInterfaceClose", restype = HRESULT,
            argtypes = [PYLON_INTERFACE_HANDLE],
            argnames = ["hIf"] )
    #  HRESULT PylonInterfaceIsOpen(PYLON_INTERFACE_HANDLE hIf, ctypes.POINTER(ctypes.c_ubyte) pOpen)
    addfunc(lib, "PylonInterfaceIsOpen", restype = HRESULT,
            argtypes = [PYLON_INTERFACE_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hIf", "pOpen"] )
    #  HRESULT PylonInterfaceGetInterfaceInfo(PYLON_INTERFACE_HANDLE hIf, ctypes.POINTER(PylonInterfaceInfo_t) pIfInfo)
    addfunc(lib, "PylonInterfaceGetInterfaceInfo", restype = HRESULT,
            argtypes = [PYLON_INTERFACE_HANDLE, ctypes.POINTER(PylonInterfaceInfo_t)],
            argnames = ["hIf", "pIfInfo"] )
    #  HRESULT PylonInterfaceGetNodeMap(PYLON_INTERFACE_HANDLE hIf, ctypes.POINTER(NODEMAP_HANDLE) phMap)
    addfunc(lib, "PylonInterfaceGetNodeMap", restype = HRESULT,
            argtypes = [PYLON_INTERFACE_HANDLE, ctypes.POINTER(NODEMAP_HANDLE)],
            argnames = ["hIf", "phMap"] )
    #  HRESULT PylonEnumerateDevices(ctypes.POINTER(ctypes.c_size_t) numDevices)
    addfunc(lib, "PylonEnumerateDevices", restype = HRESULT,
            argtypes = [ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["numDevices"] )
    #  HRESULT PylonGigEEnumerateAllDevices(ctypes.POINTER(ctypes.c_size_t) numDevices)
    addfunc(lib, "PylonGigEEnumerateAllDevices", restype = HRESULT,
            argtypes = [ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["numDevices"] )
    #  HRESULT PylonGigEForceIp(ctypes.c_char_p pMacAddress, ctypes.c_char_p pIpAddress, ctypes.c_char_p pSubnetMask, ctypes.c_char_p pDefaultGateway)
    addfunc(lib, "PylonGigEForceIp", restype = HRESULT,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p],
            argnames = ["pMacAddress", "pIpAddress", "pSubnetMask", "pDefaultGateway"] )
    #  HRESULT PylonGigERestartIpConfiguration(ctypes.c_char_p pMacAddress)
    addfunc(lib, "PylonGigERestartIpConfiguration", restype = HRESULT,
            argtypes = [ctypes.c_char_p],
            argnames = ["pMacAddress"] )
    #  HRESULT PylonGigEChangeIpConfiguration(PYLON_DEVICE_HANDLE hDev, ctypes.c_ubyte EnablePersistentIp, ctypes.c_ubyte EnableDhcp)
    addfunc(lib, "PylonGigEChangeIpConfiguration", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_ubyte, ctypes.c_ubyte],
            argnames = ["hDev", "EnablePersistentIp", "EnableDhcp"] )
    #  HRESULT PylonGigESetPersistentIpAddress(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pIpAddress, ctypes.c_char_p pSubnetMask, ctypes.c_char_p pDefaultGateway)
    addfunc(lib, "PylonGigESetPersistentIpAddress", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p],
            argnames = ["hDev", "pIpAddress", "pSubnetMask", "pDefaultGateway"] )
    #  HRESULT PylonGigEAnnounceRemoteDevice(ctypes.c_char_p pIpAddress)
    addfunc(lib, "PylonGigEAnnounceRemoteDevice", restype = HRESULT,
            argtypes = [ctypes.c_char_p],
            argnames = ["pIpAddress"] )
    #  HRESULT PylonGigERenounceRemoteDevice(ctypes.c_char_p pIpAddress, ctypes.POINTER(ctypes.c_ubyte) pFound)
    addfunc(lib, "PylonGigERenounceRemoteDevice", restype = HRESULT,
            argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["pIpAddress", "pFound"] )
    #  HRESULT PylonGigEGetPersistentIpAddress(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pIpAddress, ctypes.POINTER(ctypes.c_size_t) pIpAddressLen, ctypes.c_char_p pSubnetMask, ctypes.POINTER(ctypes.c_size_t) pSubnetMaskLen, ctypes.c_char_p pDefaultGateway, ctypes.POINTER(ctypes.c_size_t) pDefaultGatewayLen)
    addfunc(lib, "PylonGigEGetPersistentIpAddress", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t), ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t), ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hDev", "pIpAddress", "pIpAddressLen", "pSubnetMask", "pSubnetMaskLen", "pDefaultGateway", "pDefaultGatewayLen"] )
    #  HRESULT PylonGigEBroadcastIpConfiguration(ctypes.c_char_p pMacAddress, ctypes.c_ubyte EnablePersistentIp, ctypes.c_ubyte EnableDHCP, ctypes.c_char_p pIpAddress, ctypes.c_char_p pSubnetMask, ctypes.c_char_p pDefaultGateway, ctypes.c_char_p pUserdefinedName, ctypes.POINTER(ctypes.c_ubyte) pRetval)
    addfunc(lib, "PylonGigEBroadcastIpConfiguration", restype = HRESULT,
            argtypes = [ctypes.c_char_p, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["pMacAddress", "EnablePersistentIp", "EnableDHCP", "pIpAddress", "pSubnetMask", "pDefaultGateway", "pUserdefinedName", "pRetval"] )
    #  HRESULT PylonGigEIssueActionCommand(ctypes.c_uint32 deviceKey, ctypes.c_uint32 groupKey, ctypes.c_uint32 groupMask, ctypes.c_char_p pBroadcastAddress, ctypes.c_uint32 timeoutMs, ctypes.POINTER(ctypes.c_uint32) pNumResults, ctypes.POINTER(PylonGigEActionCommandResult_t) pResults)
    addfunc(lib, "PylonGigEIssueActionCommand", restype = HRESULT,
            argtypes = [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(PylonGigEActionCommandResult_t)],
            argnames = ["deviceKey", "groupKey", "groupMask", "pBroadcastAddress", "timeoutMs", "pNumResults", "pResults"] )
    #  HRESULT PylonGigEIssueScheduledActionCommand(ctypes.c_uint32 deviceKey, ctypes.c_uint32 groupKey, ctypes.c_uint32 groupMask, ctypes.c_uint64 actiontimeNs, ctypes.c_char_p pBroadcastAddress, ctypes.c_uint32 timeoutMs, ctypes.POINTER(ctypes.c_uint32) pNumResults, ctypes.POINTER(PylonGigEActionCommandResult_t) pResults)
    addfunc(lib, "PylonGigEIssueScheduledActionCommand", restype = HRESULT,
            argtypes = [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(PylonGigEActionCommandResult_t)],
            argnames = ["deviceKey", "groupKey", "groupMask", "actiontimeNs", "pBroadcastAddress", "timeoutMs", "pNumResults", "pResults"] )
    #  HRESULT PylonGetDeviceInfo(ctypes.c_size_t index, ctypes.POINTER(PylonDeviceInfo_t) pDi)
    addfunc(lib, "PylonGetDeviceInfo", restype = HRESULT,
            argtypes = [ctypes.c_size_t, ctypes.POINTER(PylonDeviceInfo_t)],
            argnames = ["index", "pDi"] )
    #  HRESULT PylonGetDeviceInfoHandle(ctypes.c_size_t index, ctypes.POINTER(PYLON_DEVICE_INFO_HANDLE) phDi)
    addfunc(lib, "PylonGetDeviceInfoHandle", restype = HRESULT,
            argtypes = [ctypes.c_size_t, ctypes.POINTER(PYLON_DEVICE_INFO_HANDLE)],
            argnames = ["index", "phDi"] )
    #  HRESULT PylonDeviceInfoGetNumProperties(PYLON_DEVICE_INFO_HANDLE hDi, ctypes.POINTER(ctypes.c_size_t) numProperties)
    addfunc(lib, "PylonDeviceInfoGetNumProperties", restype = HRESULT,
            argtypes = [PYLON_DEVICE_INFO_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hDi", "numProperties"] )
    #  HRESULT PylonDeviceInfoGetPropertyValueByName(PYLON_DEVICE_INFO_HANDLE hDi, ctypes.c_char_p pName, ctypes.c_char_p pValue, ctypes.POINTER(ctypes.c_size_t) pBufLen)
    addfunc(lib, "PylonDeviceInfoGetPropertyValueByName", restype = HRESULT,
            argtypes = [PYLON_DEVICE_INFO_HANDLE, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hDi", "pName", "pValue", "pBufLen"] )
    #  HRESULT PylonDeviceInfoGetPropertyValueByIndex(PYLON_DEVICE_INFO_HANDLE hDi, ctypes.c_size_t index, ctypes.c_char_p pBuf, ctypes.POINTER(ctypes.c_size_t) pBufLen)
    addfunc(lib, "PylonDeviceInfoGetPropertyValueByIndex", restype = HRESULT,
            argtypes = [PYLON_DEVICE_INFO_HANDLE, ctypes.c_size_t, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hDi", "index", "pBuf", "pBufLen"] )
    #  HRESULT PylonDeviceInfoGetPropertyName(PYLON_DEVICE_INFO_HANDLE hDi, ctypes.c_size_t index, ctypes.c_char_p pName, ctypes.POINTER(ctypes.c_size_t) pBufLen)
    addfunc(lib, "PylonDeviceInfoGetPropertyName", restype = HRESULT,
            argtypes = [PYLON_DEVICE_INFO_HANDLE, ctypes.c_size_t, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hDi", "index", "pName", "pBufLen"] )
    #  HRESULT PylonCreateDeviceByIndex(ctypes.c_size_t index, ctypes.POINTER(PYLON_DEVICE_HANDLE) phDev)
    addfunc(lib, "PylonCreateDeviceByIndex", restype = HRESULT,
            argtypes = [ctypes.c_size_t, ctypes.POINTER(PYLON_DEVICE_HANDLE)],
            argnames = ["index", "phDev"] )
    #  HRESULT PylonCreateDeviceFromDirectShowID(ctypes.c_int id, ctypes.POINTER(PYLON_DEVICE_HANDLE) phDev)
    addfunc(lib, "PylonCreateDeviceFromDirectShowID", restype = HRESULT,
            argtypes = [ctypes.c_int, ctypes.POINTER(PYLON_DEVICE_HANDLE)],
            argnames = ["id", "phDev"] )
    #  HRESULT PylonDestroyDevice(PYLON_DEVICE_HANDLE hDev)
    addfunc(lib, "PylonDestroyDevice", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE],
            argnames = ["hDev"] )
    #  HRESULT PylonIsDeviceAccessible(ctypes.c_size_t index, ctypes.c_int accessMode, ctypes.POINTER(ctypes.c_ubyte) pIsAccessible)
    addfunc(lib, "PylonIsDeviceAccessible", restype = HRESULT,
            argtypes = [ctypes.c_size_t, ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["index", "accessMode", "pIsAccessible"] )
    #  HRESULT PylonDeviceOpen(PYLON_DEVICE_HANDLE hDev, ctypes.c_int accessMode)
    addfunc(lib, "PylonDeviceOpen", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_int],
            argnames = ["hDev", "accessMode"] )
    #  HRESULT PylonDeviceClose(PYLON_DEVICE_HANDLE hDev)
    addfunc(lib, "PylonDeviceClose", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE],
            argnames = ["hDev"] )
    #  HRESULT PylonDeviceIsOpen(PYLON_DEVICE_HANDLE hDev, ctypes.POINTER(ctypes.c_ubyte) pOpen)
    addfunc(lib, "PylonDeviceIsOpen", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hDev", "pOpen"] )
    #  HRESULT PylonDeviceAccessMode(PYLON_DEVICE_HANDLE hDev, ctypes.POINTER(ctypes.c_int) pAccessMode)
    addfunc(lib, "PylonDeviceAccessMode", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hDev", "pAccessMode"] )
    #  HRESULT PylonDeviceGetDeviceInfo(PYLON_DEVICE_HANDLE hDev, ctypes.POINTER(PylonDeviceInfo_t) pDeviceInfo)
    addfunc(lib, "PylonDeviceGetDeviceInfo", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.POINTER(PylonDeviceInfo_t)],
            argnames = ["hDev", "pDeviceInfo"] )
    #  HRESULT PylonDeviceGetDeviceInfoHandle(PYLON_DEVICE_HANDLE hDev, ctypes.POINTER(PYLON_DEVICE_INFO_HANDLE) phDi)
    addfunc(lib, "PylonDeviceGetDeviceInfoHandle", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.POINTER(PYLON_DEVICE_INFO_HANDLE)],
            argnames = ["hDev", "phDi"] )
    #  HRESULT PylonDeviceGetNumStreamGrabberChannels(PYLON_DEVICE_HANDLE hDev, ctypes.POINTER(ctypes.c_size_t) pNumChannels)
    addfunc(lib, "PylonDeviceGetNumStreamGrabberChannels", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hDev", "pNumChannels"] )
    #  HRESULT PylonDeviceGetStreamGrabber(PYLON_DEVICE_HANDLE hDev, ctypes.c_size_t index, ctypes.POINTER(PYLON_STREAMGRABBER_HANDLE) phStg)
    addfunc(lib, "PylonDeviceGetStreamGrabber", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_size_t, ctypes.POINTER(PYLON_STREAMGRABBER_HANDLE)],
            argnames = ["hDev", "index", "phStg"] )
    #  HRESULT PylonDeviceGetEventGrabber(PYLON_DEVICE_HANDLE hDev, ctypes.POINTER(PYLON_EVENTGRABBER_HANDLE) phEvg)
    addfunc(lib, "PylonDeviceGetEventGrabber", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.POINTER(PYLON_EVENTGRABBER_HANDLE)],
            argnames = ["hDev", "phEvg"] )
    #  HRESULT PylonDeviceGetNodeMap(PYLON_DEVICE_HANDLE hDev, ctypes.POINTER(NODEMAP_HANDLE) phMap)
    addfunc(lib, "PylonDeviceGetNodeMap", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.POINTER(NODEMAP_HANDLE)],
            argnames = ["hDev", "phMap"] )
    #  HRESULT PylonDeviceGetTLNodeMap(PYLON_DEVICE_HANDLE hDev, ctypes.POINTER(NODEMAP_HANDLE) phMap)
    addfunc(lib, "PylonDeviceGetTLNodeMap", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.POINTER(NODEMAP_HANDLE)],
            argnames = ["hDev", "phMap"] )
    #  HRESULT PylonDeviceCreateChunkParser(PYLON_DEVICE_HANDLE hDev, ctypes.POINTER(PYLON_CHUNKPARSER_HANDLE) phChp)
    addfunc(lib, "PylonDeviceCreateChunkParser", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.POINTER(PYLON_CHUNKPARSER_HANDLE)],
            argnames = ["hDev", "phChp"] )
    #  HRESULT PylonDeviceDestroyChunkParser(PYLON_DEVICE_HANDLE hDev, PYLON_CHUNKPARSER_HANDLE hChp)
    addfunc(lib, "PylonDeviceDestroyChunkParser", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, PYLON_CHUNKPARSER_HANDLE],
            argnames = ["hDev", "hChp"] )
    #  HRESULT PylonDeviceCreateEventAdapter(PYLON_DEVICE_HANDLE hDev, ctypes.POINTER(PYLON_EVENTADAPTER_HANDLE) phEva)
    addfunc(lib, "PylonDeviceCreateEventAdapter", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.POINTER(PYLON_EVENTADAPTER_HANDLE)],
            argnames = ["hDev", "phEva"] )
    #  HRESULT PylonDeviceDestroyEventAdapter(PYLON_DEVICE_HANDLE hDev, PYLON_EVENTADAPTER_HANDLE hEva)
    addfunc(lib, "PylonDeviceDestroyEventAdapter", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, PYLON_EVENTADAPTER_HANDLE],
            argnames = ["hDev", "hEva"] )
    #  HRESULT PylonDeviceRegisterRemovalCallback(PYLON_DEVICE_HANDLE hDev, ctypes.c_void_p pCbFunction, ctypes.POINTER(PYLON_DEVICECALLBACK_HANDLE) phCb)
    addfunc(lib, "PylonDeviceRegisterRemovalCallback", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_void_p, ctypes.POINTER(PYLON_DEVICECALLBACK_HANDLE)],
            argnames = ["hDev", "pCbFunction", "phCb"] )
    #  HRESULT PylonDeviceDeregisterRemovalCallback(PYLON_DEVICE_HANDLE hDev, PYLON_DEVICECALLBACK_HANDLE hCb)
    addfunc(lib, "PylonDeviceDeregisterRemovalCallback", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, PYLON_DEVICECALLBACK_HANDLE],
            argnames = ["hDev", "hCb"] )
    #  HRESULT PylonDeviceSetIntegerFeature(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.c_int64 value)
    addfunc(lib, "PylonDeviceSetIntegerFeature", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.c_int64],
            argnames = ["hDev", "pName", "value"] )
    #  HRESULT PylonDeviceGetIntegerFeature(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.POINTER(ctypes.c_int64) pValue)
    addfunc(lib, "PylonDeviceGetIntegerFeature", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64)],
            argnames = ["hDev", "pName", "pValue"] )
    #  HRESULT PylonDeviceGetIntegerFeatureMin(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.POINTER(ctypes.c_int64) pValue)
    addfunc(lib, "PylonDeviceGetIntegerFeatureMin", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64)],
            argnames = ["hDev", "pName", "pValue"] )
    #  HRESULT PylonDeviceGetIntegerFeatureMax(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.POINTER(ctypes.c_int64) pValue)
    addfunc(lib, "PylonDeviceGetIntegerFeatureMax", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64)],
            argnames = ["hDev", "pName", "pValue"] )
    #  HRESULT PylonDeviceGetIntegerFeatureInc(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.POINTER(ctypes.c_int64) pValue)
    addfunc(lib, "PylonDeviceGetIntegerFeatureInc", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64)],
            argnames = ["hDev", "pName", "pValue"] )
    #  HRESULT PylonDeviceGrabSingleFrame(PYLON_DEVICE_HANDLE hDev, ctypes.c_size_t channel, ctypes.c_void_p pBuffer, ctypes.c_size_t bufferSize, ctypes.POINTER(PylonGrabResult_t) pGrabResult, ctypes.POINTER(ctypes.c_ubyte) pReady, ctypes.c_uint32 timeout)
    addfunc(lib, "PylonDeviceGrabSingleFrame", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(PylonGrabResult_t), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint32],
            argnames = ["hDev", "channel", "pBuffer", "bufferSize", "pGrabResult", "pReady", "timeout"] )
    #  HRESULT PylonDeviceSetFloatFeature(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.c_double value)
    addfunc(lib, "PylonDeviceSetFloatFeature", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.c_double],
            argnames = ["hDev", "pName", "value"] )
    #  HRESULT PylonDeviceGetFloatFeature(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.POINTER(ctypes.c_double) pValue)
    addfunc(lib, "PylonDeviceGetFloatFeature", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)],
            argnames = ["hDev", "pName", "pValue"] )
    #  HRESULT PylonDeviceGetFloatFeatureMin(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.POINTER(ctypes.c_double) pValue)
    addfunc(lib, "PylonDeviceGetFloatFeatureMin", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)],
            argnames = ["hDev", "pName", "pValue"] )
    #  HRESULT PylonDeviceGetFloatFeatureMax(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.POINTER(ctypes.c_double) pValue)
    addfunc(lib, "PylonDeviceGetFloatFeatureMax", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)],
            argnames = ["hDev", "pName", "pValue"] )
    #  HRESULT PylonDeviceSetBooleanFeature(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.c_ubyte value)
    addfunc(lib, "PylonDeviceSetBooleanFeature", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.c_ubyte],
            argnames = ["hDev", "pName", "value"] )
    #  HRESULT PylonDeviceGetBooleanFeature(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.POINTER(ctypes.c_ubyte) pValue)
    addfunc(lib, "PylonDeviceGetBooleanFeature", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hDev", "pName", "pValue"] )
    #  HRESULT PylonDeviceExecuteCommandFeature(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName)
    addfunc(lib, "PylonDeviceExecuteCommandFeature", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p],
            argnames = ["hDev", "pName"] )
    #  HRESULT PylonDeviceIsCommandDone(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "PylonDeviceIsCommandDone", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hDev", "pName", "pResult"] )
    #  HRESULT PylonDeviceFeatureFromString(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.c_char_p pValue)
    addfunc(lib, "PylonDeviceFeatureFromString", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.c_char_p],
            argnames = ["hDev", "pName", "pValue"] )
    #  HRESULT PylonDeviceFeatureToString(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.c_char_p pBuf, ctypes.POINTER(ctypes.c_size_t) pBufLen)
    addfunc(lib, "PylonDeviceFeatureToString", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hDev", "pName", "pBuf", "pBufLen"] )
    #  ctypes.c_ubyte PylonDeviceFeatureIsImplemented(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName)
    addfunc(lib, "PylonDeviceFeatureIsImplemented", restype = ctypes.c_ubyte,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p],
            argnames = ["hDev", "pName"] )
    #  ctypes.c_ubyte PylonDeviceFeatureIsAvailable(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName)
    addfunc(lib, "PylonDeviceFeatureIsAvailable", restype = ctypes.c_ubyte,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p],
            argnames = ["hDev", "pName"] )
    #  ctypes.c_ubyte PylonDeviceFeatureIsReadable(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName)
    addfunc(lib, "PylonDeviceFeatureIsReadable", restype = ctypes.c_ubyte,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p],
            argnames = ["hDev", "pName"] )
    #  ctypes.c_ubyte PylonDeviceFeatureIsWritable(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName)
    addfunc(lib, "PylonDeviceFeatureIsWritable", restype = ctypes.c_ubyte,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p],
            argnames = ["hDev", "pName"] )
    #  HRESULT PylonDeviceFeatureGetAccessMode(PYLON_DEVICE_HANDLE hDev, ctypes.c_char_p pName, ctypes.POINTER(ctypes.c_int) pResult)
    addfunc(lib, "PylonDeviceFeatureGetAccessMode", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hDev", "pName", "pResult"] )
    #  HRESULT PylonStreamGrabberOpen(PYLON_STREAMGRABBER_HANDLE hStg)
    addfunc(lib, "PylonStreamGrabberOpen", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE],
            argnames = ["hStg"] )
    #  HRESULT PylonStreamGrabberClose(PYLON_STREAMGRABBER_HANDLE hStg)
    addfunc(lib, "PylonStreamGrabberClose", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE],
            argnames = ["hStg"] )
    #  HRESULT PylonStreamGrabberIsOpen(PYLON_STREAMGRABBER_HANDLE hStg, ctypes.POINTER(ctypes.c_ubyte) pOpen)
    addfunc(lib, "PylonStreamGrabberIsOpen", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hStg", "pOpen"] )
    #  HRESULT PylonStreamGrabberGetWaitObject(PYLON_STREAMGRABBER_HANDLE hStg, ctypes.POINTER(PYLON_WAITOBJECT_HANDLE) phWobj)
    addfunc(lib, "PylonStreamGrabberGetWaitObject", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE, ctypes.POINTER(PYLON_WAITOBJECT_HANDLE)],
            argnames = ["hStg", "phWobj"] )
    #  HRESULT PylonStreamGrabberSetMaxNumBuffer(PYLON_STREAMGRABBER_HANDLE hStg, ctypes.c_size_t numBuffers)
    addfunc(lib, "PylonStreamGrabberSetMaxNumBuffer", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE, ctypes.c_size_t],
            argnames = ["hStg", "numBuffers"] )
    #  HRESULT PylonStreamGrabberGetMaxNumBuffer(PYLON_STREAMGRABBER_HANDLE hStg, ctypes.POINTER(ctypes.c_size_t) pNumBuffers)
    addfunc(lib, "PylonStreamGrabberGetMaxNumBuffer", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hStg", "pNumBuffers"] )
    #  HRESULT PylonStreamGrabberSetMaxBufferSize(PYLON_STREAMGRABBER_HANDLE hStg, ctypes.c_size_t maxSize)
    addfunc(lib, "PylonStreamGrabberSetMaxBufferSize", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE, ctypes.c_size_t],
            argnames = ["hStg", "maxSize"] )
    #  HRESULT PylonStreamGrabberGetMaxBufferSize(PYLON_STREAMGRABBER_HANDLE hStg, ctypes.POINTER(ctypes.c_size_t) pMaxSize)
    addfunc(lib, "PylonStreamGrabberGetMaxBufferSize", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hStg", "pMaxSize"] )
    #  HRESULT PylonStreamGrabberGetPayloadSize(PYLON_DEVICE_HANDLE hDev, PYLON_STREAMGRABBER_HANDLE hStg, ctypes.POINTER(ctypes.c_size_t) payloadsize)
    addfunc(lib, "PylonStreamGrabberGetPayloadSize", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, PYLON_STREAMGRABBER_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hDev", "hStg", "payloadsize"] )
    #  HRESULT PylonStreamGrabberRegisterBuffer(PYLON_STREAMGRABBER_HANDLE hStg, ctypes.c_void_p pBuffer, ctypes.c_size_t BufLen, ctypes.POINTER(PYLON_STREAMBUFFER_HANDLE) phBuf)
    addfunc(lib, "PylonStreamGrabberRegisterBuffer", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(PYLON_STREAMBUFFER_HANDLE)],
            argnames = ["hStg", "pBuffer", "BufLen", "phBuf"] )
    #  HRESULT PylonStreamGrabberDeregisterBuffer(PYLON_STREAMGRABBER_HANDLE hStg, PYLON_STREAMBUFFER_HANDLE hBuf)
    addfunc(lib, "PylonStreamGrabberDeregisterBuffer", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE, PYLON_STREAMBUFFER_HANDLE],
            argnames = ["hStg", "hBuf"] )
    #  HRESULT PylonStreamGrabberPrepareGrab(PYLON_STREAMGRABBER_HANDLE hStg)
    addfunc(lib, "PylonStreamGrabberPrepareGrab", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE],
            argnames = ["hStg"] )
    #  HRESULT PylonStreamGrabberIsStartAndStopStreamingMandatory(PYLON_STREAMGRABBER_HANDLE hStg, ctypes.POINTER(ctypes.c_ubyte) pMandatory)
    addfunc(lib, "PylonStreamGrabberIsStartAndStopStreamingMandatory", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hStg", "pMandatory"] )
    #  HRESULT PylonStreamGrabberStartStreamingIfMandatory(PYLON_STREAMGRABBER_HANDLE hStg)
    addfunc(lib, "PylonStreamGrabberStartStreamingIfMandatory", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE],
            argnames = ["hStg"] )
    #  HRESULT PylonStreamGrabberStopStreamingIfMandatory(PYLON_STREAMGRABBER_HANDLE hStg)
    addfunc(lib, "PylonStreamGrabberStopStreamingIfMandatory", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE],
            argnames = ["hStg"] )
    #  HRESULT PylonStreamGrabberFinishGrab(PYLON_STREAMGRABBER_HANDLE hStg)
    addfunc(lib, "PylonStreamGrabberFinishGrab", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE],
            argnames = ["hStg"] )
    #  HRESULT PylonStreamGrabberFlushBuffersToOutput(PYLON_STREAMGRABBER_HANDLE hStg)
    addfunc(lib, "PylonStreamGrabberFlushBuffersToOutput", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE],
            argnames = ["hStg"] )
    #  HRESULT PylonStreamGrabberCancelGrab(PYLON_STREAMGRABBER_HANDLE hStg)
    addfunc(lib, "PylonStreamGrabberCancelGrab", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE],
            argnames = ["hStg"] )
    #  HRESULT PylonStreamGrabberRetrieveResult(PYLON_STREAMGRABBER_HANDLE hStg, ctypes.POINTER(PylonGrabResult_t) pGrabResult, ctypes.POINTER(ctypes.c_ubyte) pReady)
    addfunc(lib, "PylonStreamGrabberRetrieveResult", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE, ctypes.POINTER(PylonGrabResult_t), ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hStg", "pGrabResult", "pReady"] )
    #  HRESULT PylonStreamGrabberQueueBuffer(PYLON_STREAMGRABBER_HANDLE hStg, PYLON_STREAMBUFFER_HANDLE hBuf, ctypes.c_void_p pContext)
    addfunc(lib, "PylonStreamGrabberQueueBuffer", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE, PYLON_STREAMBUFFER_HANDLE, ctypes.c_void_p],
            argnames = ["hStg", "hBuf", "pContext"] )
    #  HRESULT PylonStreamGrabberGetNodeMap(PYLON_STREAMGRABBER_HANDLE hStg, ctypes.POINTER(NODEMAP_HANDLE) phMap)
    addfunc(lib, "PylonStreamGrabberGetNodeMap", restype = HRESULT,
            argtypes = [PYLON_STREAMGRABBER_HANDLE, ctypes.POINTER(NODEMAP_HANDLE)],
            argnames = ["hStg", "phMap"] )
    #  HRESULT PylonWaitObjectIsValid(PYLON_WAITOBJECT_HANDLE hWobj, ctypes.POINTER(ctypes.c_ubyte) pValid)
    addfunc(lib, "PylonWaitObjectIsValid", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECT_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hWobj", "pValid"] )
    #  HRESULT PylonWaitObjectWait(PYLON_WAITOBJECT_HANDLE hWobj, ctypes.c_uint32 timeout, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "PylonWaitObjectWait", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECT_HANDLE, ctypes.c_uint32, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hWobj", "timeout", "pResult"] )
    #  HRESULT PylonWaitObjectWaitEx(PYLON_WAITOBJECT_HANDLE hWobj, ctypes.c_uint32 timeout, ctypes.c_ubyte alertable, ctypes.POINTER(ctypes.c_int) pWaitResult)
    addfunc(lib, "PylonWaitObjectWaitEx", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECT_HANDLE, ctypes.c_uint32, ctypes.c_ubyte, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hWobj", "timeout", "alertable", "pWaitResult"] )
    #  HRESULT PylonWaitObjectCreate(ctypes.POINTER(PYLON_WAITOBJECT_HANDLE) phWobj)
    addfunc(lib, "PylonWaitObjectCreate", restype = HRESULT,
            argtypes = [ctypes.POINTER(PYLON_WAITOBJECT_HANDLE)],
            argnames = ["phWobj"] )
    #  HRESULT PylonWaitObjectDestroy(PYLON_WAITOBJECT_HANDLE hWobj)
    addfunc(lib, "PylonWaitObjectDestroy", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECT_HANDLE],
            argnames = ["hWobj"] )
    #  HRESULT PylonWaitObjectSignal(PYLON_WAITOBJECT_HANDLE hWobj)
    addfunc(lib, "PylonWaitObjectSignal", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECT_HANDLE],
            argnames = ["hWobj"] )
    #  HRESULT PylonWaitObjectReset(PYLON_WAITOBJECT_HANDLE hWobj)
    addfunc(lib, "PylonWaitObjectReset", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECT_HANDLE],
            argnames = ["hWobj"] )
    #  HRESULT PylonWaitObjectFromW32(HANDLE hW32, ctypes.c_ubyte duplicate, ctypes.POINTER(PYLON_WAITOBJECT_HANDLE) phWobj)
    addfunc(lib, "PylonWaitObjectFromW32", restype = HRESULT,
            argtypes = [HANDLE, ctypes.c_ubyte, ctypes.POINTER(PYLON_WAITOBJECT_HANDLE)],
            argnames = ["hW32", "duplicate", "phWobj"] )
    #  HRESULT PylonWaitObjectGetW32Handle(PYLON_WAITOBJECT_HANDLE hWobj, PHANDLE phW32)
    addfunc(lib, "PylonWaitObjectGetW32Handle", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECT_HANDLE, PHANDLE],
            argnames = ["hWobj", "phW32"] )
    #  HRESULT PylonRTThreadGetPriorityCapabilities(ctypes.POINTER(ctypes.c_int32) pPriorityMin, ctypes.POINTER(ctypes.c_int32) pPriorityMax)
    addfunc(lib, "PylonRTThreadGetPriorityCapabilities", restype = HRESULT,
            argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32)],
            argnames = ["pPriorityMin", "pPriorityMax"] )
    #  HRESULT PylonRTThreadSetPriority(HANDLE hThread, ctypes.c_int32 priority)
    addfunc(lib, "PylonRTThreadSetPriority", restype = HRESULT,
            argtypes = [HANDLE, ctypes.c_int32],
            argnames = ["hThread", "priority"] )
    #  HRESULT PylonRTThreadGetPriority(HANDLE hThread, ctypes.POINTER(ctypes.c_int32) pPriority)
    addfunc(lib, "PylonRTThreadGetPriority", restype = HRESULT,
            argtypes = [HANDLE, ctypes.POINTER(ctypes.c_int32)],
            argnames = ["hThread", "pPriority"] )
    #  HRESULT PylonWaitObjectsCreate(ctypes.POINTER(PYLON_WAITOBJECTS_HANDLE) phWos)
    addfunc(lib, "PylonWaitObjectsCreate", restype = HRESULT,
            argtypes = [ctypes.POINTER(PYLON_WAITOBJECTS_HANDLE)],
            argnames = ["phWos"] )
    #  HRESULT PylonWaitObjectsDestroy(PYLON_WAITOBJECTS_HANDLE hWos)
    addfunc(lib, "PylonWaitObjectsDestroy", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECTS_HANDLE],
            argnames = ["hWos"] )
    #  HRESULT PylonWaitObjectsAdd(PYLON_WAITOBJECTS_HANDLE hWos, PYLON_WAITOBJECT_HANDLE hWobj, ctypes.POINTER(ctypes.c_size_t) pIndex)
    addfunc(lib, "PylonWaitObjectsAdd", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECTS_HANDLE, PYLON_WAITOBJECT_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hWos", "hWobj", "pIndex"] )
    #  HRESULT PylonWaitObjectsAddMany(PYLON_WAITOBJECTS_HANDLE hWos, ctypes.c_size_t numWaitObjects, ...)
    addfunc(lib, "PylonWaitObjectsAddMany", restype = HRESULT,
            argtypes = None,
            argnames = None )
    #  HRESULT PylonWaitObjectsRemoveAll(PYLON_WAITOBJECTS_HANDLE hWos)
    addfunc(lib, "PylonWaitObjectsRemoveAll", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECTS_HANDLE],
            argnames = ["hWos"] )
    #  HRESULT PylonWaitObjectsWaitForAll(PYLON_WAITOBJECTS_HANDLE hWos, ctypes.c_uint32 timeout, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "PylonWaitObjectsWaitForAll", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECTS_HANDLE, ctypes.c_uint32, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hWos", "timeout", "pResult"] )
    #  HRESULT PylonWaitObjectsWaitForAny(PYLON_WAITOBJECTS_HANDLE hWos, ctypes.c_uint32 timeout, ctypes.POINTER(ctypes.c_size_t) pIndex, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "PylonWaitObjectsWaitForAny", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECTS_HANDLE, ctypes.c_uint32, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hWos", "timeout", "pIndex", "pResult"] )
    #  HRESULT PylonWaitObjectsWaitForAny(PYLON_WAITOBJECTS_HANDLE hWos, ctypes.c_uint32 timeout, ctypes.POINTER(ctypes.c_size_t) pIndex, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "PylonWaitObjectsWaitForAny", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECTS_HANDLE, ctypes.c_uint32, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hWos", "timeout", "pIndex", "pResult"] )
    #  HRESULT PylonWaitObjectsWaitForAllEx(PYLON_WAITOBJECTS_HANDLE hWos, ctypes.c_uint32 timeout, ctypes.c_ubyte alertable, ctypes.POINTER(ctypes.c_int) pWaitResult)
    addfunc(lib, "PylonWaitObjectsWaitForAllEx", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECTS_HANDLE, ctypes.c_uint32, ctypes.c_ubyte, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hWos", "timeout", "alertable", "pWaitResult"] )
    #  HRESULT PylonWaitObjectsWaitForAnyEx(PYLON_WAITOBJECTS_HANDLE hWos, ctypes.c_uint32 timeout, ctypes.POINTER(ctypes.c_size_t) pIndex, ctypes.c_ubyte alertable, ctypes.POINTER(ctypes.c_int) pWaitResult)
    addfunc(lib, "PylonWaitObjectsWaitForAnyEx", restype = HRESULT,
            argtypes = [PYLON_WAITOBJECTS_HANDLE, ctypes.c_uint32, ctypes.POINTER(ctypes.c_size_t), ctypes.c_ubyte, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hWos", "timeout", "pIndex", "alertable", "pWaitResult"] )
    #  HRESULT PylonEventGrabberOpen(PYLON_EVENTGRABBER_HANDLE hEvg)
    addfunc(lib, "PylonEventGrabberOpen", restype = HRESULT,
            argtypes = [PYLON_EVENTGRABBER_HANDLE],
            argnames = ["hEvg"] )
    #  HRESULT PylonEventGrabberClose(PYLON_EVENTGRABBER_HANDLE hEvg)
    addfunc(lib, "PylonEventGrabberClose", restype = HRESULT,
            argtypes = [PYLON_EVENTGRABBER_HANDLE],
            argnames = ["hEvg"] )
    #  HRESULT PylonEventGrabberIsOpen(PYLON_EVENTGRABBER_HANDLE hEvg, ctypes.POINTER(ctypes.c_ubyte) pOpen)
    addfunc(lib, "PylonEventGrabberIsOpen", restype = HRESULT,
            argtypes = [PYLON_EVENTGRABBER_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hEvg", "pOpen"] )
    #  HRESULT PylonEventGrabberRetrieveEvent(PYLON_EVENTGRABBER_HANDLE hEvg, ctypes.POINTER(PylonEventResult_t) pEventResult, ctypes.POINTER(ctypes.c_ubyte) pReady)
    addfunc(lib, "PylonEventGrabberRetrieveEvent", restype = HRESULT,
            argtypes = [PYLON_EVENTGRABBER_HANDLE, ctypes.POINTER(PylonEventResult_t), ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hEvg", "pEventResult", "pReady"] )
    #  HRESULT PylonEventGrabberGetWaitObject(PYLON_EVENTGRABBER_HANDLE hEvg, ctypes.POINTER(PYLON_WAITOBJECT_HANDLE) phWobj)
    addfunc(lib, "PylonEventGrabberGetWaitObject", restype = HRESULT,
            argtypes = [PYLON_EVENTGRABBER_HANDLE, ctypes.POINTER(PYLON_WAITOBJECT_HANDLE)],
            argnames = ["hEvg", "phWobj"] )
    #  HRESULT PylonEventGrabberGetNodeMap(PYLON_EVENTGRABBER_HANDLE hEvg, ctypes.POINTER(NODEMAP_HANDLE) phMap)
    addfunc(lib, "PylonEventGrabberGetNodeMap", restype = HRESULT,
            argtypes = [PYLON_EVENTGRABBER_HANDLE, ctypes.POINTER(NODEMAP_HANDLE)],
            argnames = ["hEvg", "phMap"] )
    #  HRESULT PylonEventGrabberGetNumBuffers(PYLON_EVENTGRABBER_HANDLE hEvg, ctypes.POINTER(ctypes.c_size_t) pNumBuffers)
    addfunc(lib, "PylonEventGrabberGetNumBuffers", restype = HRESULT,
            argtypes = [PYLON_EVENTGRABBER_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hEvg", "pNumBuffers"] )
    #  HRESULT PylonEventGrabberSetNumBuffers(PYLON_EVENTGRABBER_HANDLE hEvg, ctypes.c_size_t numBuffers)
    addfunc(lib, "PylonEventGrabberSetNumBuffers", restype = HRESULT,
            argtypes = [PYLON_EVENTGRABBER_HANDLE, ctypes.c_size_t],
            argnames = ["hEvg", "numBuffers"] )
    #  HRESULT PylonEventAdapterDeliverMessage(PYLON_EVENTADAPTER_HANDLE hEva, ctypes.POINTER(PylonEventResult_t) pEventResult)
    addfunc(lib, "PylonEventAdapterDeliverMessage", restype = HRESULT,
            argtypes = [PYLON_EVENTADAPTER_HANDLE, ctypes.POINTER(PylonEventResult_t)],
            argnames = ["hEva", "pEventResult"] )
    #  HRESULT PylonChunkParserAttachBuffer(PYLON_CHUNKPARSER_HANDLE hChp, ctypes.c_void_p pBuffer, ctypes.c_size_t BufLen)
    addfunc(lib, "PylonChunkParserAttachBuffer", restype = HRESULT,
            argtypes = [PYLON_CHUNKPARSER_HANDLE, ctypes.c_void_p, ctypes.c_size_t],
            argnames = ["hChp", "pBuffer", "BufLen"] )
    #  HRESULT PylonChunkParserDetachBuffer(PYLON_CHUNKPARSER_HANDLE hChp)
    addfunc(lib, "PylonChunkParserDetachBuffer", restype = HRESULT,
            argtypes = [PYLON_CHUNKPARSER_HANDLE],
            argnames = ["hChp"] )
    #  HRESULT PylonChunkParserUpdateBuffer(PYLON_CHUNKPARSER_HANDLE hChp, ctypes.c_void_p pBuffer)
    addfunc(lib, "PylonChunkParserUpdateBuffer", restype = HRESULT,
            argtypes = [PYLON_CHUNKPARSER_HANDLE, ctypes.c_void_p],
            argnames = ["hChp", "pBuffer"] )
    #  HRESULT PylonChunkParserHasCRC(PYLON_CHUNKPARSER_HANDLE hChp, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "PylonChunkParserHasCRC", restype = HRESULT,
            argtypes = [PYLON_CHUNKPARSER_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hChp", "pResult"] )
    #  HRESULT PylonChunkParserCheckCRC(PYLON_CHUNKPARSER_HANDLE hChp, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "PylonChunkParserCheckCRC", restype = HRESULT,
            argtypes = [PYLON_CHUNKPARSER_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hChp", "pResult"] )
    #  HRESULT PylonPixelFormatConverterCreate(PYLON_DEVICE_HANDLE hDev, ctypes.c_int outAlign, ctypes.POINTER(PYLON_FORMAT_CONVERTER_HANDLE) phConv)
    addfunc(lib, "PylonPixelFormatConverterCreate", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_int, ctypes.POINTER(PYLON_FORMAT_CONVERTER_HANDLE)],
            argnames = ["hDev", "outAlign", "phConv"] )
    #  HRESULT PylonPixelFormatConverterConvert(PYLON_FORMAT_CONVERTER_HANDLE hConv, ctypes.c_void_p targetBuffer, ctypes.c_size_t targetBufferSize, ctypes.c_void_p sourceBuffer, ctypes.c_size_t sourceBufferSize)
    addfunc(lib, "PylonPixelFormatConverterConvert", restype = HRESULT,
            argtypes = [PYLON_FORMAT_CONVERTER_HANDLE, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t],
            argnames = ["hConv", "targetBuffer", "targetBufferSize", "sourceBuffer", "sourceBufferSize"] )
    #  HRESULT PylonPixelFormatConverterGetOutputBufferSize(PYLON_FORMAT_CONVERTER_HANDLE hConv, ctypes.POINTER(ctypes.c_size_t) pBufSiz)
    addfunc(lib, "PylonPixelFormatConverterGetOutputBufferSize", restype = HRESULT,
            argtypes = [PYLON_FORMAT_CONVERTER_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hConv", "pBufSiz"] )
    #  HRESULT PylonPixelFormatConverterDestroy(PYLON_FORMAT_CONVERTER_HANDLE hConv)
    addfunc(lib, "PylonPixelFormatConverterDestroy", restype = HRESULT,
            argtypes = [PYLON_FORMAT_CONVERTER_HANDLE],
            argnames = ["hConv"] )
    #  HRESULT PylonBitsPerPixel(ctypes.c_int pixelType, ctypes.POINTER(ctypes.c_int) pResult)
    addfunc(lib, "PylonBitsPerPixel", restype = HRESULT,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["pixelType", "pResult"] )
    #  HRESULT PylonIsMono(ctypes.c_int pixelType, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "PylonIsMono", restype = HRESULT,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["pixelType", "pResult"] )
    #  HRESULT PylonIsBayer(ctypes.c_int pixelType, ctypes.POINTER(ctypes.c_ubyte) pResult)
    addfunc(lib, "PylonIsBayer", restype = HRESULT,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["pixelType", "pResult"] )
    #  HRESULT PylonPixelTypeFromString(ctypes.c_char_p pString, ctypes.POINTER(ctypes.c_int) pPixelType)
    addfunc(lib, "PylonPixelTypeFromString", restype = HRESULT,
            argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["pString", "pPixelType"] )
    #  HRESULT PylonDevicePortRead(PYLON_DEVICE_HANDLE hDev, ctypes.c_void_p pBuffer, ctypes.c_int64 Address, ctypes.c_size_t Length)
    addfunc(lib, "PylonDevicePortRead", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_void_p, ctypes.c_int64, ctypes.c_size_t],
            argnames = ["hDev", "pBuffer", "Address", "Length"] )
    #  HRESULT PylonDevicePortWrite(PYLON_DEVICE_HANDLE hDev, ctypes.c_void_p pBuffer, ctypes.c_int64 Address, ctypes.c_size_t Length)
    addfunc(lib, "PylonDevicePortWrite", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_void_p, ctypes.c_int64, ctypes.c_size_t],
            argnames = ["hDev", "pBuffer", "Address", "Length"] )
    #  HRESULT PylonFeaturePersistenceSave(NODEMAP_HANDLE hMap, ctypes.c_char_p pFileName)
    addfunc(lib, "PylonFeaturePersistenceSave", restype = HRESULT,
            argtypes = [NODEMAP_HANDLE, ctypes.c_char_p],
            argnames = ["hMap", "pFileName"] )
    #  HRESULT PylonFeaturePersistenceLoad(NODEMAP_HANDLE hMap, ctypes.c_char_p pFileName, ctypes.c_ubyte verify)
    addfunc(lib, "PylonFeaturePersistenceLoad", restype = HRESULT,
            argtypes = [NODEMAP_HANDLE, ctypes.c_char_p, ctypes.c_ubyte],
            argnames = ["hMap", "pFileName", "verify"] )
    #  HRESULT PylonFeaturePersistenceSaveToString(NODEMAP_HANDLE hMap, ctypes.c_char_p pFeatures, ctypes.POINTER(ctypes.c_size_t) pFeaturesLen)
    addfunc(lib, "PylonFeaturePersistenceSaveToString", restype = HRESULT,
            argtypes = [NODEMAP_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hMap", "pFeatures", "pFeaturesLen"] )
    #  HRESULT PylonFeaturePersistenceLoadFromString(NODEMAP_HANDLE hMap, ctypes.c_char_p pFeatures, ctypes.c_ubyte verify)
    addfunc(lib, "PylonFeaturePersistenceLoadFromString", restype = HRESULT,
            argtypes = [NODEMAP_HANDLE, ctypes.c_char_p, ctypes.c_ubyte],
            argnames = ["hMap", "pFeatures", "verify"] )
    #  HRESULT PylonImagePersistenceSave(ctypes.c_int imageFileFormat, ctypes.c_char_p pFilename, ctypes.c_void_p pBuffer, ctypes.c_size_t bufferSize, ctypes.c_int pixelType, ctypes.c_uint32 width, ctypes.c_uint32 height, ctypes.c_size_t paddingX, ctypes.c_int orientation, ctypes.POINTER(PylonImagePersistenceOptions_t) pOptions)
    addfunc(lib, "PylonImagePersistenceSave", restype = HRESULT,
            argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_size_t, ctypes.c_int, ctypes.POINTER(PylonImagePersistenceOptions_t)],
            argnames = ["imageFileFormat", "pFilename", "pBuffer", "bufferSize", "pixelType", "width", "height", "paddingX", "orientation", "pOptions"] )
    #  HRESULT PylonImagePersistenceLoad(ctypes.c_char_p pFilename, ctypes.c_void_p pBuffer, ctypes.POINTER(ctypes.c_size_t) pBufferSize, ctypes.POINTER(ctypes.c_int) pPixelType, ctypes.POINTER(ctypes.c_uint32) pWidth, ctypes.POINTER(ctypes.c_uint32) pHeight, ctypes.POINTER(ctypes.c_size_t) pPaddingX, ctypes.POINTER(ctypes.c_int) pOrientation)
    addfunc(lib, "PylonImagePersistenceLoad", restype = HRESULT,
            argtypes = [ctypes.c_char_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_int)],
            argnames = ["pFilename", "pBuffer", "pBufferSize", "pPixelType", "pWidth", "pHeight", "pPaddingX", "pOrientation"] )
    #  HRESULT PylonImageFormatConverterCreate(ctypes.POINTER(PYLON_IMAGE_FORMAT_CONVERTER_HANDLE) phConv)
    addfunc(lib, "PylonImageFormatConverterCreate", restype = HRESULT,
            argtypes = [ctypes.POINTER(PYLON_IMAGE_FORMAT_CONVERTER_HANDLE)],
            argnames = ["phConv"] )
    #  HRESULT PylonImageFormatConverterGetNodeMap(PYLON_IMAGE_FORMAT_CONVERTER_HANDLE hConv, ctypes.POINTER(NODEMAP_HANDLE) phMap)
    addfunc(lib, "PylonImageFormatConverterGetNodeMap", restype = HRESULT,
            argtypes = [PYLON_IMAGE_FORMAT_CONVERTER_HANDLE, ctypes.POINTER(NODEMAP_HANDLE)],
            argnames = ["hConv", "phMap"] )
    #  HRESULT PylonImageFormatConverterSetOutputPixelFormat(PYLON_IMAGE_FORMAT_CONVERTER_HANDLE hConv, ctypes.c_int pixelType)
    addfunc(lib, "PylonImageFormatConverterSetOutputPixelFormat", restype = HRESULT,
            argtypes = [PYLON_IMAGE_FORMAT_CONVERTER_HANDLE, ctypes.c_int],
            argnames = ["hConv", "pixelType"] )
    #  HRESULT PylonImageFormatConverterGetOutputPixelFormat(PYLON_IMAGE_FORMAT_CONVERTER_HANDLE hConv, ctypes.POINTER(ctypes.c_int) pPixelType)
    addfunc(lib, "PylonImageFormatConverterGetOutputPixelFormat", restype = HRESULT,
            argtypes = [PYLON_IMAGE_FORMAT_CONVERTER_HANDLE, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hConv", "pPixelType"] )
    #  HRESULT PylonImageFormatConverterSetOutputPaddingX(PYLON_IMAGE_FORMAT_CONVERTER_HANDLE hConv, ctypes.c_size_t paddingX)
    addfunc(lib, "PylonImageFormatConverterSetOutputPaddingX", restype = HRESULT,
            argtypes = [PYLON_IMAGE_FORMAT_CONVERTER_HANDLE, ctypes.c_size_t],
            argnames = ["hConv", "paddingX"] )
    #  HRESULT PylonImageFormatConverterGetOutputPaddingX(PYLON_IMAGE_FORMAT_CONVERTER_HANDLE hConv, ctypes.POINTER(ctypes.c_size_t) pPaddingX)
    addfunc(lib, "PylonImageFormatConverterGetOutputPaddingX", restype = HRESULT,
            argtypes = [PYLON_IMAGE_FORMAT_CONVERTER_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hConv", "pPaddingX"] )
    #  HRESULT PylonImageFormatConverterConvert(PYLON_IMAGE_FORMAT_CONVERTER_HANDLE hConv, ctypes.c_void_p targetBuffer, ctypes.c_size_t targetBufferSize, ctypes.c_void_p sourceBuffer, ctypes.c_size_t sourceBufferSize, ctypes.c_int sourcePixelType, ctypes.c_uint32 sourceWidth, ctypes.c_uint32 sourceHeight, ctypes.c_size_t sourcePaddingX, ctypes.c_int sourceOrientation)
    addfunc(lib, "PylonImageFormatConverterConvert", restype = HRESULT,
            argtypes = [PYLON_IMAGE_FORMAT_CONVERTER_HANDLE, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_size_t, ctypes.c_int],
            argnames = ["hConv", "targetBuffer", "targetBufferSize", "sourceBuffer", "sourceBufferSize", "sourcePixelType", "sourceWidth", "sourceHeight", "sourcePaddingX", "sourceOrientation"] )
    #  HRESULT PylonImageFormatConverterGetBufferSizeForConversion(PYLON_IMAGE_FORMAT_CONVERTER_HANDLE hConv, ctypes.c_int sourcePixelType, ctypes.c_uint32 sourceWidth, ctypes.c_uint32 sourceHeight, ctypes.POINTER(ctypes.c_size_t) pBufSize)
    addfunc(lib, "PylonImageFormatConverterGetBufferSizeForConversion", restype = HRESULT,
            argtypes = [PYLON_IMAGE_FORMAT_CONVERTER_HANDLE, ctypes.c_int, ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hConv", "sourcePixelType", "sourceWidth", "sourceHeight", "pBufSize"] )
    #  HRESULT PylonImageFormatConverterDestroy(PYLON_IMAGE_FORMAT_CONVERTER_HANDLE hConv)
    addfunc(lib, "PylonImageFormatConverterDestroy", restype = HRESULT,
            argtypes = [PYLON_IMAGE_FORMAT_CONVERTER_HANDLE],
            argnames = ["hConv"] )
    #  HRESULT PylonAviWriterCreate(ctypes.POINTER(PYLON_AVI_WRITER_HANDLE) phWriter)
    addfunc(lib, "PylonAviWriterCreate", restype = HRESULT,
            argtypes = [ctypes.POINTER(PYLON_AVI_WRITER_HANDLE)],
            argnames = ["phWriter"] )
    #  HRESULT PylonAviWriterDestroy(PYLON_AVI_WRITER_HANDLE hWriter)
    addfunc(lib, "PylonAviWriterDestroy", restype = HRESULT,
            argtypes = [PYLON_AVI_WRITER_HANDLE],
            argnames = ["hWriter"] )
    #  HRESULT PylonAviWriterOpen(PYLON_AVI_WRITER_HANDLE hWriter, ctypes.c_char_p pFilename, ctypes.c_double framesPerSecondPlayback, ctypes.c_int pixelType, ctypes.c_uint32 width, ctypes.c_uint32 height, ctypes.c_int orientation, ctypes.c_void_p pCompressionOptions)
    addfunc(lib, "PylonAviWriterOpen", restype = HRESULT,
            argtypes = [PYLON_AVI_WRITER_HANDLE, ctypes.c_char_p, ctypes.c_double, ctypes.c_int, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int, ctypes.c_void_p],
            argnames = ["hWriter", "pFilename", "framesPerSecondPlayback", "pixelType", "width", "height", "orientation", "pCompressionOptions"] )
    #  HRESULT PylonAviWriterClose(PYLON_AVI_WRITER_HANDLE hWriter)
    addfunc(lib, "PylonAviWriterClose", restype = HRESULT,
            argtypes = [PYLON_AVI_WRITER_HANDLE],
            argnames = ["hWriter"] )
    #  HRESULT PylonAviWriterIsOpen(PYLON_AVI_WRITER_HANDLE hWriter, ctypes.POINTER(ctypes.c_ubyte) pIsOpen)
    addfunc(lib, "PylonAviWriterIsOpen", restype = HRESULT,
            argtypes = [PYLON_AVI_WRITER_HANDLE, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hWriter", "pIsOpen"] )
    #  HRESULT PylonAviWriterAdd(PYLON_AVI_WRITER_HANDLE hWriter, ctypes.c_void_p pBuffer, ctypes.c_size_t bufferSize, ctypes.c_int pixelType, ctypes.c_uint32 width, ctypes.c_uint32 height, ctypes.c_size_t paddingX, ctypes.c_int orientation, ctypes.c_int keyFrameSelection)
    addfunc(lib, "PylonAviWriterAdd", restype = HRESULT,
            argtypes = [PYLON_AVI_WRITER_HANDLE, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_size_t, ctypes.c_int, ctypes.c_int],
            argnames = ["hWriter", "pBuffer", "bufferSize", "pixelType", "width", "height", "paddingX", "orientation", "keyFrameSelection"] )
    #  HRESULT PylonAviWriterCanAddWithoutConversion(PYLON_AVI_WRITER_HANDLE hWriter, ctypes.c_int pixelType, ctypes.c_uint32 width, ctypes.c_uint32 height, ctypes.c_size_t paddingX, ctypes.c_int orientation, ctypes.POINTER(ctypes.c_ubyte) pCanAddWithoutConversion)
    addfunc(lib, "PylonAviWriterCanAddWithoutConversion", restype = HRESULT,
            argtypes = [PYLON_AVI_WRITER_HANDLE, ctypes.c_int, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_size_t, ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["hWriter", "pixelType", "width", "height", "paddingX", "orientation", "pCanAddWithoutConversion"] )
    #  HRESULT PylonAviWriterGetImageDataBytesWritten(PYLON_AVI_WRITER_HANDLE hWriter, ctypes.POINTER(ctypes.c_size_t) pImageDataBytesWritten)
    addfunc(lib, "PylonAviWriterGetImageDataBytesWritten", restype = HRESULT,
            argtypes = [PYLON_AVI_WRITER_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hWriter", "pImageDataBytesWritten"] )
    #  HRESULT PylonAviWriterGetCountOfAddedImages(PYLON_AVI_WRITER_HANDLE hWriter, ctypes.POINTER(ctypes.c_size_t) pCountOfAddedImages)
    addfunc(lib, "PylonAviWriterGetCountOfAddedImages", restype = HRESULT,
            argtypes = [PYLON_AVI_WRITER_HANDLE, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["hWriter", "pCountOfAddedImages"] )
    #  HRESULT PylonImageWindowCreate(ctypes.c_size_t winIndex, ctypes.c_int x, ctypes.c_int y, ctypes.c_int nWidth, ctypes.c_int nHeight)
    addfunc(lib, "PylonImageWindowCreate", restype = HRESULT,
            argtypes = [ctypes.c_size_t, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["winIndex", "x", "y", "nWidth", "nHeight"] )
    #  HRESULT PylonImageWindowShow(ctypes.c_size_t winIndex, ctypes.c_int nShow)
    addfunc(lib, "PylonImageWindowShow", restype = HRESULT,
            argtypes = [ctypes.c_size_t, ctypes.c_int],
            argnames = ["winIndex", "nShow"] )
    #  HRESULT PylonImageWindowHide(ctypes.c_size_t winIndex)
    addfunc(lib, "PylonImageWindowHide", restype = HRESULT,
            argtypes = [ctypes.c_size_t],
            argnames = ["winIndex"] )
    #  HRESULT PylonImageWindowClose(ctypes.c_size_t winIndex)
    addfunc(lib, "PylonImageWindowClose", restype = HRESULT,
            argtypes = [ctypes.c_size_t],
            argnames = ["winIndex"] )
    #  HRESULT PylonImageWindowGetWindowHandle(ctypes.c_size_t winIndex, ctypes.POINTER(HWND) phWindow)
    addfunc(lib, "PylonImageWindowGetWindowHandle", restype = HRESULT,
            argtypes = [ctypes.c_size_t, ctypes.POINTER(HWND)],
            argnames = ["winIndex", "phWindow"] )
    #  HRESULT PylonImageWindowSetImage(ctypes.c_size_t winIndex, ctypes.c_void_p buffer, ctypes.c_size_t bufferSize, ctypes.c_int pixelType, ctypes.c_uint32 width, ctypes.c_uint32 height, ctypes.c_size_t paddingX, ctypes.c_int orientation)
    addfunc(lib, "PylonImageWindowSetImage", restype = HRESULT,
            argtypes = [ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_size_t, ctypes.c_int],
            argnames = ["winIndex", "buffer", "bufferSize", "pixelType", "width", "height", "paddingX", "orientation"] )
    #  HRESULT PylonImageWindowDisplayImage(ctypes.c_size_t winIndex, ctypes.c_void_p buffer, ctypes.c_size_t bufferSize, ctypes.c_int pixelType, ctypes.c_uint32 width, ctypes.c_uint32 height, ctypes.c_size_t paddingX, ctypes.c_int orientation)
    addfunc(lib, "PylonImageWindowDisplayImage", restype = HRESULT,
            argtypes = [ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_size_t, ctypes.c_int],
            argnames = ["winIndex", "buffer", "bufferSize", "pixelType", "width", "height", "paddingX", "orientation"] )
    #  HRESULT PylonImageWindowDisplayImageGrabResult(ctypes.c_size_t winIndex, ctypes.POINTER(PylonGrabResult_t) grabResult)
    addfunc(lib, "PylonImageWindowDisplayImageGrabResult", restype = HRESULT,
            argtypes = [ctypes.c_size_t, ctypes.POINTER(PylonGrabResult_t)],
            argnames = ["winIndex", "grabResult"] )
    #  HRESULT PylonImageDecompressorCreate(ctypes.POINTER(PYLON_IMAGE_DECOMPRESSOR_HANDLE) phDecompressor)
    addfunc(lib, "PylonImageDecompressorCreate", restype = HRESULT,
            argtypes = [ctypes.POINTER(PYLON_IMAGE_DECOMPRESSOR_HANDLE)],
            argnames = ["phDecompressor"] )
    #  HRESULT PylonImageDecompressorDestroy(PYLON_IMAGE_DECOMPRESSOR_HANDLE hDecompressor)
    addfunc(lib, "PylonImageDecompressorDestroy", restype = HRESULT,
            argtypes = [PYLON_IMAGE_DECOMPRESSOR_HANDLE],
            argnames = ["hDecompressor"] )
    #  HRESULT PylonImageDecompressorSetCompressionDescriptor(PYLON_IMAGE_DECOMPRESSOR_HANDLE hDecompressor, ctypes.c_void_p pCompressionDescriptor, ctypes.c_size_t sizeCompressionDescriptor)
    addfunc(lib, "PylonImageDecompressorSetCompressionDescriptor", restype = HRESULT,
            argtypes = [PYLON_IMAGE_DECOMPRESSOR_HANDLE, ctypes.c_void_p, ctypes.c_size_t],
            argnames = ["hDecompressor", "pCompressionDescriptor", "sizeCompressionDescriptor"] )
    #  HRESULT PylonImageDecompressorGetCompressionInfo(ctypes.c_void_p pPayload, ctypes.c_size_t payloadSize, ctypes.POINTER(PylonCompressionInfo_t) pCompressionInfo)
    addfunc(lib, "PylonImageDecompressorGetCompressionInfo", restype = HRESULT,
            argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(PylonCompressionInfo_t)],
            argnames = ["pPayload", "payloadSize", "pCompressionInfo"] )
    #  HRESULT PylonImageDecompressorDecompressImage(PYLON_IMAGE_DECOMPRESSOR_HANDLE hDecompressor, ctypes.c_void_p pOutputBuffer, ctypes.POINTER(ctypes.c_size_t) pOutputBufferSize, ctypes.c_void_p pPayload, ctypes.c_size_t payloadSize, ctypes.POINTER(PylonCompressionInfo_t) pCompressionInfo)
    addfunc(lib, "PylonImageDecompressorDecompressImage", restype = HRESULT,
            argtypes = [PYLON_IMAGE_DECOMPRESSOR_HANDLE, ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t), ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(PylonCompressionInfo_t)],
            argnames = ["hDecompressor", "pOutputBuffer", "pOutputBufferSize", "pPayload", "payloadSize", "pCompressionInfo"] )
    #  HRESULT PylonDeviceSetIntegerFeatureInt32(PYLON_DEVICE_HANDLE dev, ctypes.c_char_p name, ctypes.c_int32 value)
    addfunc(lib, "PylonDeviceSetIntegerFeatureInt32", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.c_int32],
            argnames = ["dev", "name", "value"] )
    #  HRESULT PylonDeviceGetIntegerFeatureInt32(PYLON_DEVICE_HANDLE dev, ctypes.c_char_p name, ctypes.POINTER(ctypes.c_int32) value)
    addfunc(lib, "PylonDeviceGetIntegerFeatureInt32", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)],
            argnames = ["dev", "name", "value"] )
    #  HRESULT PylonDeviceGetIntegerFeatureMinInt32(PYLON_DEVICE_HANDLE dev, ctypes.c_char_p name, ctypes.POINTER(ctypes.c_int32) value)
    addfunc(lib, "PylonDeviceGetIntegerFeatureMinInt32", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)],
            argnames = ["dev", "name", "value"] )
    #  HRESULT PylonDeviceGetIntegerFeatureMaxInt32(PYLON_DEVICE_HANDLE dev, ctypes.c_char_p name, ctypes.POINTER(ctypes.c_int32) value)
    addfunc(lib, "PylonDeviceGetIntegerFeatureMaxInt32", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)],
            argnames = ["dev", "name", "value"] )
    #  HRESULT PylonDeviceGetIntegerFeatureIncInt32(PYLON_DEVICE_HANDLE dev, ctypes.c_char_p name, ctypes.POINTER(ctypes.c_int32) value)
    addfunc(lib, "PylonDeviceGetIntegerFeatureIncInt32", restype = HRESULT,
            argtypes = [PYLON_DEVICE_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)],
            argnames = ["dev", "name", "value"] )


