##########   This file is generated automatically based on dcamapi4.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




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
LPWORD=ctypes.POINTER(WORD)
LONGLONG=ctypes.c_int64
LPLONG=ctypes.POINTER(ctypes.c_long)
HANDLE=ctypes.c_void_p
LPHANDLE=ctypes.POINTER(HANDLE)
HWND=ctypes.c_void_p
HGLOBAL=ctypes.c_void_p
HINSTANCE=ctypes.c_void_p
HDC=ctypes.c_void_p
HMODULE=ctypes.c_void_p
HKEY=ctypes.c_void_p
PVOID=ctypes.c_void_p
LPVOID=ctypes.c_void_p
HDCAM=ctypes.c_void_p
int32=ctypes.c_int
_ui32=ctypes.c_uint
class DCAMERR(enum.IntEnum):
    DCAMERR_BUSY                     =_int32(0x80000101)
    DCAMERR_NOTREADY                 =_int32(0x80000103)
    DCAMERR_NOTSTABLE                =_int32(0x80000104)
    DCAMERR_UNSTABLE                 =_int32(0x80000105)
    DCAMERR_NOTBUSY                  =_int32(0x80000107)
    DCAMERR_EXCLUDED                 =_int32(0x80000110)
    DCAMERR_COOLINGTROUBLE           =_int32(0x80000302)
    DCAMERR_NOTRIGGER                =_int32(0x80000303)
    DCAMERR_TEMPERATURE_TROUBLE      =_int32(0x80000304)
    DCAMERR_TOOFREQUENTTRIGGER       =_int32(0x80000305)
    DCAMERR_ABORT                    =_int32(0x80000102)
    DCAMERR_TIMEOUT                  =_int32(0x80000106)
    DCAMERR_LOSTFRAME                =_int32(0x80000301)
    DCAMERR_MISSINGFRAME_TROUBLE     =_int32(0x80000f06)
    DCAMERR_INVALIDIMAGE             =_int32(0x80000321)
    DCAMERR_NORESOURCE               =_int32(0x80000201)
    DCAMERR_NOMEMORY                 =_int32(0x80000203)
    DCAMERR_NOMODULE                 =_int32(0x80000204)
    DCAMERR_NODRIVER                 =_int32(0x80000205)
    DCAMERR_NOCAMERA                 =_int32(0x80000206)
    DCAMERR_NOGRABBER                =_int32(0x80000207)
    DCAMERR_NOCOMBINATION            =_int32(0x80000208)
    DCAMERR_FAILOPEN                 =_int32(0x80001001)
    DCAMERR_INVALIDMODULE            =_int32(0x80000211)
    DCAMERR_INVALIDCOMMPORT          =_int32(0x80000212)
    DCAMERR_FAILOPENBUS              =_int32(0x81001001)
    DCAMERR_FAILOPENCAMERA           =_int32(0x82001001)
    DCAMERR_INVALIDCAMERA            =_int32(0x80000806)
    DCAMERR_INVALIDHANDLE            =_int32(0x80000807)
    DCAMERR_INVALIDPARAM             =_int32(0x80000808)
    DCAMERR_INVALIDVALUE             =_int32(0x80000821)
    DCAMERR_OUTOFRANGE               =_int32(0x80000822)
    DCAMERR_NOTWRITABLE              =_int32(0x80000823)
    DCAMERR_NOTREADABLE              =_int32(0x80000824)
    DCAMERR_INVALIDPROPERTYID        =_int32(0x80000825)
    DCAMERR_NEWAPIREQUIRED           =_int32(0x80000826)
    DCAMERR_WRONGHANDSHAKE           =_int32(0x80000827)
    DCAMERR_NOPROPERTY               =_int32(0x80000828)
    DCAMERR_INVALIDCHANNEL           =_int32(0x80000829)
    DCAMERR_INVALIDVIEW              =_int32(0x8000082a)
    DCAMERR_INVALIDSUBARRAY          =_int32(0x8000082b)
    DCAMERR_ACCESSDENY               =_int32(0x8000082c)
    DCAMERR_NOVALUETEXT              =_int32(0x8000082d)
    DCAMERR_WRONGPROPERTYVALUE       =_int32(0x8000082e)
    DCAMERR_DISHARMONY               =_int32(0x80000830)
    DCAMERR_FRAMEBUNDLESHOULDBEOFF   =_int32(0x80000832)
    DCAMERR_INVALIDFRAMEINDEX        =_int32(0x80000833)
    DCAMERR_INVALIDSESSIONINDEX      =_int32(0x80000834)
    DCAMERR_NOCORRECTIONDATA         =_int32(0x80000838)
    DCAMERR_CHANNELDEPENDENTVALUE    =_int32(0x80000839)
    DCAMERR_VIEWDEPENDENTVALUE       =_int32(0x8000083a)
    DCAMERR_NOTSUPPORT               =_int32(0x80000f03)
    DCAMERR_FAILREADCAMERA           =_int32(0x83001002)
    DCAMERR_FAILWRITECAMERA          =_int32(0x83001003)
    DCAMERR_CONFLICTCOMMPORT         =_int32(0x83001004)
    DCAMERR_OPTICS_UNPLUGGED         =_int32(0x83001005)
    DCAMERR_FAILCALIBRATION          =_int32(0x83001006)
    DCAMERR_INVALIDMEMBER_3          =_int32(0x84000103)
    DCAMERR_INVALIDMEMBER_5          =_int32(0x84000105)
    DCAMERR_INVALIDMEMBER_7          =_int32(0x84000107)
    DCAMERR_INVALIDMEMBER_8          =_int32(0x84000108)
    DCAMERR_INVALIDMEMBER_9          =_int32(0x84000109)
    DCAMERR_FAILEDOPENRECFILE        =_int32(0x84001001)
    DCAMERR_INVALIDRECHANDLE         =_int32(0x84001002)
    DCAMERR_FAILEDWRITEDATA          =_int32(0x84001003)
    DCAMERR_FAILEDREADDATA           =_int32(0x84001004)
    DCAMERR_NOWRECORDING             =_int32(0x84001005)
    DCAMERR_WRITEFULL                =_int32(0x84001006)
    DCAMERR_ALREADYOCCUPIED          =_int32(0x84001007)
    DCAMERR_TOOLARGEUSERDATASIZE     =_int32(0x84001008)
    DCAMERR_INVALIDWAITHANDLE        =_int32(0x84002001)
    DCAMERR_NEWRUNTIMEREQUIRED       =_int32(0x84002002)
    DCAMERR_VERSIONMISMATCH          =_int32(0x84002003)
    DCAMERR_RUNAS_FACTORYMODE        =_int32(0x84002004)
    DCAMERR_IMAGE_UNKNOWNSIGNATURE   =_int32(0x84003001)
    DCAMERR_IMAGE_NEWRUNTIMEREQUIRED =_int32(0x84003002)
    DCAMERR_IMAGE_ERRORSTATUSEXIST   =_int32(0x84003003)
    DCAMERR_IMAGE_HEADERCORRUPTED    =_int32(0x84004004)
    DCAMERR_IMAGE_BROKENCONTENT      =_int32(0x84004005)
    DCAMERR_UNKNOWNMSGID             =_int32(0x80000801)
    DCAMERR_UNKNOWNSTRID             =_int32(0x80000802)
    DCAMERR_UNKNOWNPARAMID           =_int32(0x80000803)
    DCAMERR_UNKNOWNBITSTYPE          =_int32(0x80000804)
    DCAMERR_UNKNOWNDATATYPE          =_int32(0x80000805)
    DCAMERR_NONE                     =_int32(0)
    DCAMERR_INSTALLATIONINPROGRESS   =_int32(0x80000f00)
    DCAMERR_UNREACH                  =_int32(0x80000f01)
    DCAMERR_UNLOADED                 =_int32(0x80000f04)
    DCAMERR_THRUADAPTER              =_int32(0x80000f05)
    DCAMERR_NOCONNECTION             =_int32(0x80000f07)
    DCAMERR_NOTIMPLEMENT             =_int32(0x80000f02)
    DCAMERR_APIINIT_INITOPTIONBYTES  =_int32(0xa4010003)
    DCAMERR_APIINIT_INITOPTION       =_int32(0xa4010004)
    DCAMERR_INITOPTION_COLLISION_BASE=_int32(0xa401C000)
    DCAMERR_INITOPTION_COLLISION_MAX =_int32(0xa401FFFF)
    DCAMERR_SUCCESS                  =_int32(1)
dDCAMERR={a.name:a.value for a in DCAMERR}
drDCAMERR={a.value:a.name for a in DCAMERR}


class DCAMBUF_FRAME_OPTION(enum.IntEnum):
    DCAMBUF_FRAME_OPTION__VIEW_ALL         =_int32(0x00000000)
    DCAMBUF_FRAME_OPTION__VIEW_1           =_int32(0x00100000)
    DCAMBUF_FRAME_OPTION__VIEW_2           =_int32(0x00200000)
    DCAMBUF_FRAME_OPTION__VIEW_3           =_int32(0x00300000)
    DCAMBUF_FRAME_OPTION__VIEW_4           =_int32(0x00400000)
    DCAMBUF_FRAME_OPTION__PROC_HIGHCONTRAST=_int32(0x00000010)
    DCAMBUF_FRAME_OPTION__VIEW__STEP       =_int32(0x00100000)
    DCAMBUF_FRAME_OPTION__VIEW__MASK       =_int32(0x00F00000)
    DCAMBUF_FRAME_OPTION__PROC__MASK       =_int32(0x00000FF0)
    end_of_dcambuf_frame_option            =enum.auto()
dDCAMBUF_FRAME_OPTION={a.name:a.value for a in DCAMBUF_FRAME_OPTION}
drDCAMBUF_FRAME_OPTION={a.value:a.name for a in DCAMBUF_FRAME_OPTION}


class DCAMREC_FRAME_OPTION(enum.IntEnum):
    DCAMREC_FRAME_OPTION__VIEW_CURRENT     =_int32(0x00000000)
    DCAMREC_FRAME_OPTION__VIEW_1           =_int32(0x00100000)
    DCAMREC_FRAME_OPTION__VIEW_2           =_int32(0x00200000)
    DCAMREC_FRAME_OPTION__VIEW_3           =_int32(0x00300000)
    DCAMREC_FRAME_OPTION__VIEW_4           =_int32(0x00400000)
    DCAMREC_FRAME_OPTION__PROC_HIGHCONTRAST=_int32(0x00000010)
    DCAMREC_FRAME_OPTION__VIEW__STEP       =_int32(0x00100000)
    DCAMREC_FRAME_OPTION__VIEW__MASK       =_int32(0x00F00000)
    DCAMREC_FRAME_OPTION__PROC__MASK       =_int32(0x00000FF0)
    endof_dcamrec_frame_option             =enum.auto()
dDCAMREC_FRAME_OPTION={a.name:a.value for a in DCAMREC_FRAME_OPTION}
drDCAMREC_FRAME_OPTION={a.value:a.name for a in DCAMREC_FRAME_OPTION}


class DCAMBUF_METADATAOPTION(enum.IntEnum):
    DCAMBUF_METADATAOPTION__VIEW_ALL  =_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__VIEW_ALL.value)
    DCAMBUF_METADATAOPTION__VIEW_1    =_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__VIEW_1.value)
    DCAMBUF_METADATAOPTION__VIEW_2    =_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__VIEW_2.value)
    DCAMBUF_METADATAOPTION__VIEW_3    =_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__VIEW_3.value)
    DCAMBUF_METADATAOPTION__VIEW_4    =_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__VIEW_4.value)
    DCAMBUF_METADATAOPTION__VIEW__STEP=_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__VIEW__STEP.value)
    DCAMBUF_METADATAOPTION__VIEW__MASK=_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__VIEW__MASK.value)
dDCAMBUF_METADATAOPTION={a.name:a.value for a in DCAMBUF_METADATAOPTION}
drDCAMBUF_METADATAOPTION={a.value:a.name for a in DCAMBUF_METADATAOPTION}


class DCAMREC_METADATAOPTION(enum.IntEnum):
    DCAMREC_METADATAOPTION__LOCATION_FRAME  =_int32(0x00000000)
    DCAMREC_METADATAOPTION__LOCATION_FILE   =_int32(0x01000000)
    DCAMREC_METADATAOPTION__LOCATION_SESSION=_int32(0x02000000)
    DCAMREC_METADATAOPTION__LOCATION__MASK  =_int32(0xFF000000)
dDCAMREC_METADATAOPTION={a.name:a.value for a in DCAMREC_METADATAOPTION}
drDCAMREC_METADATAOPTION={a.value:a.name for a in DCAMREC_METADATAOPTION}


class DCAM_PIXELTYPE(enum.IntEnum):
    DCAM_PIXELTYPE_MONO8 =_int32(0x00000001)
    DCAM_PIXELTYPE_MONO16=_int32(0x00000002)
    DCAM_PIXELTYPE_MONO12=_int32(0x00000003)
    DCAM_PIXELTYPE_RGB24 =_int32(0x00000021)
    DCAM_PIXELTYPE_RGB48 =_int32(0x00000022)
    DCAM_PIXELTYPE_BGR24 =_int32(0x00000029)
    DCAM_PIXELTYPE_BGR48 =_int32(0x0000002a)
    DCAM_PIXELTYPE_NONE  =_int32(0x00000000)
dDCAM_PIXELTYPE={a.name:a.value for a in DCAM_PIXELTYPE}
drDCAM_PIXELTYPE={a.value:a.name for a in DCAM_PIXELTYPE}


class DCAM_ATTACHKIND(enum.IntEnum):
    DCAMBUF_ATTACHKIND_TIMESTAMP         =_int32(1)
    DCAMBUF_ATTACHKIND_FRAMESTAMP        =_int32(2)
    DCAMBUF_ATTACHKIND_PRIMARY_TIMESTAMP =_int32(3)
    DCAMBUF_ATTACHKIND_PRIMARY_FRAMESTAMP=_int32(4)
    DCAMBUF_ATTACHKIND_FRAME             =_int32(0)
dDCAM_ATTACHKIND={a.name:a.value for a in DCAM_ATTACHKIND}
drDCAM_ATTACHKIND={a.value:a.name for a in DCAM_ATTACHKIND}


class DCAMCAP_TRANSFERKIND(enum.IntEnum):
    DCAMCAP_TRANSFERKIND_FRAME=_int32(0)
dDCAMCAP_TRANSFERKIND={a.name:a.value for a in DCAMCAP_TRANSFERKIND}
drDCAMCAP_TRANSFERKIND={a.value:a.name for a in DCAMCAP_TRANSFERKIND}


class DCAMCAP_STATUS(enum.IntEnum):
    DCAMCAP_STATUS_ERROR   =_int32(0x0000)
    DCAMCAP_STATUS_BUSY    =_int32(0x0001)
    DCAMCAP_STATUS_READY   =_int32(0x0002)
    DCAMCAP_STATUS_STABLE  =_int32(0x0003)
    DCAMCAP_STATUS_UNSTABLE=_int32(0x0004)
    end_of_dcamcap_status  =enum.auto()
dDCAMCAP_STATUS={a.name:a.value for a in DCAMCAP_STATUS}
drDCAMCAP_STATUS={a.value:a.name for a in DCAMCAP_STATUS}


class DCAMWAIT_EVENT(enum.IntEnum):
    DCAMWAIT_CAPEVENT_TRANSFERRED=_int32(0x0001)
    DCAMWAIT_CAPEVENT_FRAMEREADY =_int32(0x0002)
    DCAMWAIT_CAPEVENT_CYCLEEND   =_int32(0x0004)
    DCAMWAIT_CAPEVENT_EXPOSUREEND=_int32(0x0008)
    DCAMWAIT_CAPEVENT_STOPPED    =_int32(0x0010)
    DCAMWAIT_RECEVENT_STOPPED    =_int32(0x0100)
    DCAMWAIT_RECEVENT_WARNING    =_int32(0x0200)
    DCAMWAIT_RECEVENT_MISSED     =_int32(0x0400)
    DCAMWAIT_RECEVENT_DISKFULL   =_int32(0x1000)
    DCAMWAIT_RECEVENT_WRITEFAULT =_int32(0x2000)
    DCAMWAIT_RECEVENT_SKIPPED    =_int32(0x4000)
    end_of_dcamwait_event        =enum.auto()
dDCAMWAIT_EVENT={a.name:a.value for a in DCAMWAIT_EVENT}
drDCAMWAIT_EVENT={a.value:a.name for a in DCAMWAIT_EVENT}


class DCAMCAP_START(enum.IntEnum):
    DCAMCAP_START_SEQUENCE=_int32((-1))
    DCAMCAP_START_SNAP    =_int32(0)
dDCAMCAP_START={a.name:a.value for a in DCAMCAP_START}
drDCAMCAP_START={a.value:a.name for a in DCAMCAP_START}


class DCAM_IDSTR(enum.IntEnum):
    DCAM_IDSTR_BUS                     =_int32(0x04000101)
    DCAM_IDSTR_CAMERAID                =_int32(0x04000102)
    DCAM_IDSTR_VENDOR                  =_int32(0x04000103)
    DCAM_IDSTR_MODEL                   =_int32(0x04000104)
    DCAM_IDSTR_CAMERAVERSION           =_int32(0x04000105)
    DCAM_IDSTR_DRIVERVERSION           =_int32(0x04000106)
    DCAM_IDSTR_MODULEVERSION           =_int32(0x04000107)
    DCAM_IDSTR_DCAMAPIVERSION          =_int32(0x04000108)
    DCAM_IDSTR_CAMERA_SERIESNAME       =_int32(0x0400012c)
    DCAM_IDSTR_OPTICALBLOCK_MODEL      =_int32(0x04001101)
    DCAM_IDSTR_OPTICALBLOCK_ID         =_int32(0x04001102)
    DCAM_IDSTR_OPTICALBLOCK_DESCRIPTION=_int32(0x04001103)
    DCAM_IDSTR_OPTICALBLOCK_CHANNEL_1  =_int32(0x04001104)
    DCAM_IDSTR_OPTICALBLOCK_CHANNEL_2  =_int32(0x04001105)
dDCAM_IDSTR={a.name:a.value for a in DCAM_IDSTR}
drDCAM_IDSTR={a.value:a.name for a in DCAM_IDSTR}


class DCAMWAIT_TIMEOUT(enum.IntEnum):
    DCAMWAIT_TIMEOUT_INFINITE=_int32(0x80000000)
    end_of_dcamwait_timeout  =enum.auto()
dDCAMWAIT_TIMEOUT={a.name:a.value for a in DCAMWAIT_TIMEOUT}
drDCAMWAIT_TIMEOUT={a.value:a.name for a in DCAMWAIT_TIMEOUT}


class DCAMAPI_INITOPTION(enum.IntEnum):
    DCAMAPI_INITOPTION_APIVER__LATEST    =_int32(0x00000001)
    DCAMAPI_INITOPTION_APIVER__4_0       =_int32(0x00000400)
    DCAMAPI_INITOPTION_MULTIVIEW__DISABLE=_int32(0x00010002)
    DCAMAPI_INITOPTION_ENDMARK           =_int32(0x00000000)
dDCAMAPI_INITOPTION={a.name:a.value for a in DCAMAPI_INITOPTION}
drDCAMAPI_INITOPTION={a.value:a.name for a in DCAMAPI_INITOPTION}


class DCAMBUF_METADATAKIND(enum.IntEnum):
    DCAMBUF_METADATAKIND_TIMESTAMPS =_int32(0x00010000)
    DCAMBUF_METADATAKIND_FRAMESTAMPS=_int32(0x00020000)
    end_of_dcambuf_metadatakind     =enum.auto()
dDCAMBUF_METADATAKIND={a.name:a.value for a in DCAMBUF_METADATAKIND}
drDCAMBUF_METADATAKIND={a.value:a.name for a in DCAMBUF_METADATAKIND}


class DCAMREC_METADATAKIND(enum.IntEnum):
    DCAMREC_METADATAKIND_USERDATATEXT=_int32(0x00000001)
    DCAMREC_METADATAKIND_USERDATABIN =_int32(0x00000002)
    DCAMREC_METADATAKIND_TIMESTAMPS  =_int32(0x00010000)
    DCAMREC_METADATAKIND_FRAMESTAMPS =_int32(0x00020000)
    end_of_dcamrec_metadatakind      =enum.auto()
dDCAMREC_METADATAKIND={a.name:a.value for a in DCAMREC_METADATAKIND}
drDCAMREC_METADATAKIND={a.value:a.name for a in DCAMREC_METADATAKIND}


class DCAMDATA_OPTION(enum.IntEnum):
    DCAMDATA_OPTION__VIEW_ALL  =_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__VIEW_ALL.value)
    DCAMDATA_OPTION__VIEW_1    =_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__VIEW_1.value)
    DCAMDATA_OPTION__VIEW_2    =_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__VIEW_2.value)
    DCAMDATA_OPTION__VIEW_3    =_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__VIEW_3.value)
    DCAMDATA_OPTION__VIEW_4    =_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__VIEW_4.value)
    DCAMDATA_OPTION__VIEW__STEP=_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__VIEW__STEP.value)
    DCAMDATA_OPTION__VIEW__MASK=_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__VIEW__MASK.value)
dDCAMDATA_OPTION={a.name:a.value for a in DCAMDATA_OPTION}
drDCAMDATA_OPTION={a.value:a.name for a in DCAMDATA_OPTION}


class DCAMDATA_KIND(enum.IntEnum):
    DCAMDATA_KIND__REGION=_int32(0x00000001)
    DCAMDATA_KIND__LUT   =_int32(0x00000002)
    DCAMDATA_KIND__NONE  =_int32(0x00000000)
dDCAMDATA_KIND={a.name:a.value for a in DCAMDATA_KIND}
drDCAMDATA_KIND={a.value:a.name for a in DCAMDATA_KIND}


class DCAMDATA_ATTRIBUTE(enum.IntEnum):
    DCAMDATA_ATTRIBUTE__ACCESSREADY=_int32(0x01000000)
    DCAMDATA_ATTRIBUTE__ACCESSBUSY =_int32(0x02000000)
    DCAMDATA_ATTRIBUTE__HASVIEW    =_int32(0x10000000)
    DCAMDATA_ATTRIBUTE__MASK       =_int32(0xFF000000)
dDCAMDATA_ATTRIBUTE={a.name:a.value for a in DCAMDATA_ATTRIBUTE}
drDCAMDATA_ATTRIBUTE={a.value:a.name for a in DCAMDATA_ATTRIBUTE}


class DCAMDATA_REGIONTYPE(enum.IntEnum):
    DCAMDATA_REGIONTYPE__BYTEMASK     =_int32(0x00000001)
    DCAMDATA_REGIONTYPE__RECT16ARRAY  =_int32(0x00000002)
    DCAMDATA_REGIONTYPE__ACCESSREADY  =_int32(DCAMDATA_ATTRIBUTE.DCAMDATA_ATTRIBUTE__ACCESSREADY.value)
    DCAMDATA_REGIONTYPE__ACCESSBUSY   =_int32(DCAMDATA_ATTRIBUTE.DCAMDATA_ATTRIBUTE__ACCESSBUSY.value)
    DCAMDATA_REGIONTYPE__HASVIEW      =_int32(DCAMDATA_ATTRIBUTE.DCAMDATA_ATTRIBUTE__HASVIEW.value)
    DCAMDATA_REGIONTYPE__BODYMASK     =_int32(0x00FFFFFF)
    DCAMDATA_REGIONTYPE__ATTRIBUTEMASK=_int32(DCAMDATA_ATTRIBUTE.DCAMDATA_ATTRIBUTE__MASK.value)
    DCAMDATA_REGIONTYPE__NONE         =_int32(0x00000000)
dDCAMDATA_REGIONTYPE={a.name:a.value for a in DCAMDATA_REGIONTYPE}
drDCAMDATA_REGIONTYPE={a.value:a.name for a in DCAMDATA_REGIONTYPE}


class DCAMDATA_LUTTYPE(enum.IntEnum):
    DCAMDATA_LUTTYPE__SEGMENTED_LINEAR=_int32(0x00000001)
    DCAMDATA_LUTTYPE__MONO16          =_int32(0x00000002)
    DCAMDATA_LUTTYPE__ACCESSREADY     =_int32(DCAMDATA_ATTRIBUTE.DCAMDATA_ATTRIBUTE__ACCESSREADY.value)
    DCAMDATA_LUTTYPE__ACCESSBUSY      =_int32(DCAMDATA_ATTRIBUTE.DCAMDATA_ATTRIBUTE__ACCESSBUSY.value)
    DCAMDATA_LUTTYPE__BODYMASK        =_int32(0x00FFFFFF)
    DCAMDATA_LUTTYPE__ATTRIBUTEMASK   =_int32(DCAMDATA_ATTRIBUTE.DCAMDATA_ATTRIBUTE__MASK.value)
    DCAMDATA_LUTTYPE__NONE            =_int32(0x00000000)
dDCAMDATA_LUTTYPE={a.name:a.value for a in DCAMDATA_LUTTYPE}
drDCAMDATA_LUTTYPE={a.value:a.name for a in DCAMDATA_LUTTYPE}


class DCAMBUF_PROCTYPE(enum.IntEnum):
    DCAMBUF_PROCTYPE__HIGHCONTRASTMODE=_int32(DCAMBUF_FRAME_OPTION.DCAMBUF_FRAME_OPTION__PROC_HIGHCONTRAST.value)
    DCAMBUF_PROCTYPE__NONE            =_int32(0x00000000)
dDCAMBUF_PROCTYPE={a.name:a.value for a in DCAMBUF_PROCTYPE}
drDCAMBUF_PROCTYPE={a.value:a.name for a in DCAMBUF_PROCTYPE}


class DCAM_CODEPAGE(enum.IntEnum):
    DCAM_CODEPAGE__SHIFT_JIS=_int32(932)
    DCAM_CODEPAGE__UTF16_LE =_int32(1200)
    DCAM_CODEPAGE__UTF16_BE =_int32(1201)
    DCAM_CODEPAGE__UTF7     =_int32(65000)
    DCAM_CODEPAGE__UTF8     =_int32(65001)
    DCAM_CODEPAGE__NONE     =_int32(0x00000000)
dDCAM_CODEPAGE={a.name:a.value for a in DCAM_CODEPAGE}
drDCAM_CODEPAGE={a.value:a.name for a in DCAM_CODEPAGE}


class DCAMDEV_CAPDOMAIN(enum.IntEnum):
    DCAMDEV_CAPDOMAIN__DCAMDATA   =_int32(0x00000001)
    DCAMDEV_CAPDOMAIN__FRAMEOPTION=_int32(0x00000002)
    DCAMDEV_CAPDOMAIN__FUNCTION   =_int32(0x00000000)
dDCAMDEV_CAPDOMAIN={a.name:a.value for a in DCAMDEV_CAPDOMAIN}
drDCAMDEV_CAPDOMAIN={a.value:a.name for a in DCAMDEV_CAPDOMAIN}


class DCAMDEV_CAPFLAG(enum.IntEnum):
    DCAMDEV_CAPFLAG_FRAMESTAMP =_int32(0x00000001)
    DCAMDEV_CAPFLAG_TIMESTAMP  =_int32(0x00000002)
    DCAMDEV_CAPFLAG_CAMERASTAMP=_int32(0x00000004)
    DCAMDEV_CAPFLAG_NONE       =_int32(0x00000000)
dDCAMDEV_CAPFLAG={a.name:a.value for a in DCAMDEV_CAPFLAG}
drDCAMDEV_CAPFLAG={a.value:a.name for a in DCAMDEV_CAPFLAG}


class DCAMREC_STATUSFLAG(enum.IntEnum):
    DCAMREC_STATUSFLAG_NONE     =_int32(0x00000000)
    DCAMREC_STATUSFLAG_RECORDING=_int32(0x00000001)
    end_of_dcamrec_statusflag   =enum.auto()
dDCAMREC_STATUSFLAG={a.name:a.value for a in DCAMREC_STATUSFLAG}
drDCAMREC_STATUSFLAG={a.value:a.name for a in DCAMREC_STATUSFLAG}


HDCAMWAIT=ctypes.c_void_p
HDCAMREC=ctypes.c_void_p
class DCAM_GUID(ctypes.Structure):
    _fields_=[  ("Data1",_ui32),
                ("Data2",ctypes.c_ushort),
                ("Data3",ctypes.c_ushort),
                ("Data4",ctypes.c_ubyte*8) ]
PDCAM_GUID=ctypes.POINTER(DCAM_GUID)
class CDCAM_GUID(ctypes_wrap.CStructWrapper):
    _struct=DCAM_GUID


class DCAMAPI_INIT(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("iDeviceCount",int32),
                ("reserved",int32),
                ("initoptionbytes",int32),
                ("initoption",ctypes.POINTER(int32)),
                ("guid",ctypes.POINTER(DCAM_GUID)) ]
PDCAMAPI_INIT=ctypes.POINTER(DCAMAPI_INIT)
class CDCAMAPI_INIT(ctypes_wrap.CStructWrapper):
    _struct=DCAMAPI_INIT


class DCAMDEV_OPEN(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("index",int32),
                ("hdcam",HDCAM) ]
PDCAMDEV_OPEN=ctypes.POINTER(DCAMDEV_OPEN)
class CDCAMDEV_OPEN(ctypes_wrap.CStructWrapper):
    _struct=DCAMDEV_OPEN


class DCAMDEV_CAPABILITY(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("domain",int32),
                ("capflag",int32),
                ("kind",int32) ]
PDCAMDEV_CAPABILITY=ctypes.POINTER(DCAMDEV_CAPABILITY)
class CDCAMDEV_CAPABILITY(ctypes_wrap.CStructWrapper):
    _struct=DCAMDEV_CAPABILITY


class DCAMDEV_CAPABILITY_LUT(ctypes.Structure):
    _fields_=[  ("hdr",DCAMDEV_CAPABILITY),
                ("linearpointmax",int32) ]
PDCAMDEV_CAPABILITY_LUT=ctypes.POINTER(DCAMDEV_CAPABILITY_LUT)
class CDCAMDEV_CAPABILITY_LUT(ctypes_wrap.CStructWrapper):
    _struct=DCAMDEV_CAPABILITY_LUT


class DCAMDEV_CAPABILITY_REGION(ctypes.Structure):
    _fields_=[  ("hdr",DCAMDEV_CAPABILITY),
                ("horzunit",int32),
                ("vertunit",int32) ]
PDCAMDEV_CAPABILITY_REGION=ctypes.POINTER(DCAMDEV_CAPABILITY_REGION)
class CDCAMDEV_CAPABILITY_REGION(ctypes_wrap.CStructWrapper):
    _struct=DCAMDEV_CAPABILITY_REGION


class DCAMDEV_CAPABILITY_FRAMEOPTION(ctypes.Structure):
    _fields_=[  ("hdr",DCAMDEV_CAPABILITY),
                ("supportproc",int32) ]
PDCAMDEV_CAPABILITY_FRAMEOPTION=ctypes.POINTER(DCAMDEV_CAPABILITY_FRAMEOPTION)
class CDCAMDEV_CAPABILITY_FRAMEOPTION(ctypes_wrap.CStructWrapper):
    _struct=DCAMDEV_CAPABILITY_FRAMEOPTION


class DCAMDEV_STRING(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("iString",int32),
                ("text",ctypes.c_char_p),
                ("textbytes",int32) ]
PDCAMDEV_STRING=ctypes.POINTER(DCAMDEV_STRING)
class CDCAMDEV_STRING(ctypes_wrap.CStructWrapper):
    _struct=DCAMDEV_STRING


class DCAMDATA_HDR(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("iKind",int32),
                ("option",int32),
                ("reserved2",int32) ]
PDCAMDATA_HDR=ctypes.POINTER(DCAMDATA_HDR)
class CDCAMDATA_HDR(ctypes_wrap.CStructWrapper):
    _struct=DCAMDATA_HDR


class DCAMDATA_REGION(ctypes.Structure):
    _fields_=[  ("hdr",DCAMDATA_HDR),
                ("option",int32),
                ("type",int32),
                ("data",ctypes.c_void_p),
                ("datasize",int32),
                ("reserved",int32) ]
PDCAMDATA_REGION=ctypes.POINTER(DCAMDATA_REGION)
class CDCAMDATA_REGION(ctypes_wrap.CStructWrapper):
    _struct=DCAMDATA_REGION


class DCAMDATA_REGIONRECT(ctypes.Structure):
    _fields_=[  ("left",ctypes.c_short),
                ("top",ctypes.c_short),
                ("right",ctypes.c_short),
                ("bottom",ctypes.c_short) ]
PDCAMDATA_REGIONRECT=ctypes.POINTER(DCAMDATA_REGIONRECT)
class CDCAMDATA_REGIONRECT(ctypes_wrap.CStructWrapper):
    _struct=DCAMDATA_REGIONRECT


class DCAMDATA_LUT(ctypes.Structure):
    _fields_=[  ("hdr",DCAMDATA_HDR),
                ("type",int32),
                ("page",int32),
                ("data",ctypes.c_void_p),
                ("datasize",int32),
                ("reserved",int32) ]
PDCAMDATA_LUT=ctypes.POINTER(DCAMDATA_LUT)
class CDCAMDATA_LUT(ctypes_wrap.CStructWrapper):
    _struct=DCAMDATA_LUT


class DCAMDATA_LINEARLUT(ctypes.Structure):
    _fields_=[  ("lutin",int32),
                ("lutout",int32) ]
PDCAMDATA_LINEARLUT=ctypes.POINTER(DCAMDATA_LINEARLUT)
class CDCAMDATA_LINEARLUT(ctypes_wrap.CStructWrapper):
    _struct=DCAMDATA_LINEARLUT


class DCAMPROP_ATTR(ctypes.Structure):
    _fields_=[  ("cbSize",int32),
                ("iProp",int32),
                ("option",int32),
                ("iReserved1",int32),
                ("attribute",int32),
                ("iGroup",int32),
                ("iUnit",int32),
                ("attribute2",int32),
                ("valuemin",ctypes.c_double),
                ("valuemax",ctypes.c_double),
                ("valuestep",ctypes.c_double),
                ("valuedefault",ctypes.c_double),
                ("nMaxChannel",int32),
                ("iReserved3",int32),
                ("nMaxView",int32),
                ("iProp_NumberOfElement",int32),
                ("iProp_ArrayBase",int32),
                ("iPropStep_Element",int32) ]
PDCAMPROP_ATTR=ctypes.POINTER(DCAMPROP_ATTR)
class CDCAMPROP_ATTR(ctypes_wrap.CStructWrapper):
    _struct=DCAMPROP_ATTR


class DCAMPROP_VALUETEXT(ctypes.Structure):
    _fields_=[  ("cbSize",int32),
                ("iProp",int32),
                ("value",ctypes.c_double),
                ("text",ctypes.c_char_p),
                ("textbytes",int32) ]
PDCAMPROP_VALUETEXT=ctypes.POINTER(DCAMPROP_VALUETEXT)
class CDCAMPROP_VALUETEXT(ctypes_wrap.CStructWrapper):
    _struct=DCAMPROP_VALUETEXT


class DCAMBUF_ATTACH(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("iKind",int32),
                ("buffer",ctypes.POINTER(ctypes.c_void_p)),
                ("buffercount",int32) ]
PDCAMBUF_ATTACH=ctypes.POINTER(DCAMBUF_ATTACH)
class CDCAMBUF_ATTACH(ctypes_wrap.CStructWrapper):
    _struct=DCAMBUF_ATTACH


class DCAM_TIMESTAMP(ctypes.Structure):
    _fields_=[  ("sec",_ui32),
                ("microsec",int32) ]
PDCAM_TIMESTAMP=ctypes.POINTER(DCAM_TIMESTAMP)
class CDCAM_TIMESTAMP(ctypes_wrap.CStructWrapper):
    _struct=DCAM_TIMESTAMP


class DCAMBUF_FRAME(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("iKind",int32),
                ("option",int32),
                ("iFrame",int32),
                ("buf",ctypes.c_void_p),
                ("rowbytes",int32),
                ("type",ctypes.c_int),
                ("width",int32),
                ("height",int32),
                ("left",int32),
                ("top",int32),
                ("timestamp",DCAM_TIMESTAMP),
                ("framestamp",int32),
                ("camerastamp",int32) ]
PDCAMBUF_FRAME=ctypes.POINTER(DCAMBUF_FRAME)
class CDCAMBUF_FRAME(ctypes_wrap.CStructWrapper):
    _struct=DCAMBUF_FRAME


class DCAMREC_FRAME(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("iKind",int32),
                ("option",int32),
                ("iFrame",int32),
                ("buf",ctypes.c_void_p),
                ("rowbytes",int32),
                ("type",ctypes.c_int),
                ("width",int32),
                ("height",int32),
                ("left",int32),
                ("top",int32),
                ("timestamp",DCAM_TIMESTAMP),
                ("framestamp",int32),
                ("camerastamp",int32) ]
PDCAMREC_FRAME=ctypes.POINTER(DCAMREC_FRAME)
class CDCAMREC_FRAME(ctypes_wrap.CStructWrapper):
    _struct=DCAMREC_FRAME


class DCAMWAIT_OPEN(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("supportevent",int32),
                ("hwait",HDCAMWAIT),
                ("hdcam",HDCAM) ]
PDCAMWAIT_OPEN=ctypes.POINTER(DCAMWAIT_OPEN)
class CDCAMWAIT_OPEN(ctypes_wrap.CStructWrapper):
    _struct=DCAMWAIT_OPEN


class DCAMWAIT_START(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("eventhappened",int32),
                ("eventmask",int32),
                ("timeout",int32) ]
PDCAMWAIT_START=ctypes.POINTER(DCAMWAIT_START)
class CDCAMWAIT_START(ctypes_wrap.CStructWrapper):
    _struct=DCAMWAIT_START


class DCAMCAP_TRANSFERINFO(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("iKind",int32),
                ("nNewestFrameIndex",int32),
                ("nFrameCount",int32) ]
PDCAMCAP_TRANSFERINFO=ctypes.POINTER(DCAMCAP_TRANSFERINFO)
class CDCAMCAP_TRANSFERINFO(ctypes_wrap.CStructWrapper):
    _struct=DCAMCAP_TRANSFERINFO


class DCAMREC_OPENA(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("reserved",int32),
                ("hrec",HDCAMREC),
                ("path",ctypes.c_char_p),
                ("ext",ctypes.c_char_p),
                ("maxframepersession",int32),
                ("userdatasize",int32),
                ("userdatasize_session",int32),
                ("userdatasize_file",int32),
                ("usertextsize",int32),
                ("usertextsize_session",int32),
                ("usertextsize_file",int32) ]
PDCAMREC_OPENA=ctypes.POINTER(DCAMREC_OPENA)
class CDCAMREC_OPENA(ctypes_wrap.CStructWrapper):
    _struct=DCAMREC_OPENA


class DCAMREC_OPENW(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("reserved",int32),
                ("hrec",HDCAMREC),
                ("path",ctypes.c_wchar_p),
                ("ext",ctypes.c_wchar_p),
                ("maxframepersession",int32),
                ("userdatasize",int32),
                ("userdatasize_session",int32),
                ("userdatasize_file",int32),
                ("usertextsize",int32),
                ("usertextsize_session",int32),
                ("usertextsize_file",int32) ]
PDCAMREC_OPENW=ctypes.POINTER(DCAMREC_OPENW)
class CDCAMREC_OPENW(ctypes_wrap.CStructWrapper):
    _struct=DCAMREC_OPENW


class DCAM_METADATAHDR(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("iKind",int32),
                ("option",int32),
                ("iFrame",int32) ]
PDCAM_METADATAHDR=ctypes.POINTER(DCAM_METADATAHDR)
class CDCAM_METADATAHDR(ctypes_wrap.CStructWrapper):
    _struct=DCAM_METADATAHDR


class DCAM_METADATABLOCKHDR(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("iKind",int32),
                ("option",int32),
                ("iFrame",int32),
                ("in_count",int32),
                ("outcount",int32) ]
PDCAM_METADATABLOCKHDR=ctypes.POINTER(DCAM_METADATABLOCKHDR)
class CDCAM_METADATABLOCKHDR(ctypes_wrap.CStructWrapper):
    _struct=DCAM_METADATABLOCKHDR


class DCAM_USERDATATEXT(ctypes.Structure):
    _fields_=[  ("hdr",DCAM_METADATAHDR),
                ("text",ctypes.c_char_p),
                ("text_len",int32),
                ("codepage",int32) ]
PDCAM_USERDATATEXT=ctypes.POINTER(DCAM_USERDATATEXT)
class CDCAM_USERDATATEXT(ctypes_wrap.CStructWrapper):
    _struct=DCAM_USERDATATEXT


class DCAM_USERDATABIN(ctypes.Structure):
    _fields_=[  ("hdr",DCAM_METADATAHDR),
                ("bin",ctypes.c_void_p),
                ("bin_len",int32),
                ("reserved",int32) ]
PDCAM_USERDATABIN=ctypes.POINTER(DCAM_USERDATABIN)
class CDCAM_USERDATABIN(ctypes_wrap.CStructWrapper):
    _struct=DCAM_USERDATABIN


class DCAM_TIMESTAMPBLOCK(ctypes.Structure):
    _fields_=[  ("hdr",DCAM_METADATABLOCKHDR),
                ("timestamps",ctypes.POINTER(DCAM_TIMESTAMP)),
                ("timestampsize",int32),
                ("timestampvaildsize",int32),
                ("timestampkind",int32),
                ("reserved",int32) ]
PDCAM_TIMESTAMPBLOCK=ctypes.POINTER(DCAM_TIMESTAMPBLOCK)
class CDCAM_TIMESTAMPBLOCK(ctypes_wrap.CStructWrapper):
    _struct=DCAM_TIMESTAMPBLOCK


class DCAM_FRAMESTAMPBLOCK(ctypes.Structure):
    _fields_=[  ("hdr",DCAM_METADATABLOCKHDR),
                ("framestamps",ctypes.POINTER(int32)),
                ("reserved",int32) ]
PDCAM_FRAMESTAMPBLOCK=ctypes.POINTER(DCAM_FRAMESTAMPBLOCK)
class CDCAM_FRAMESTAMPBLOCK(ctypes_wrap.CStructWrapper):
    _struct=DCAM_FRAMESTAMPBLOCK


class DCAM_METADATATEXTBLOCK(ctypes.Structure):
    _fields_=[  ("hdr",DCAM_METADATABLOCKHDR),
                ("text",ctypes.c_void_p),
                ("textsizes",ctypes.POINTER(int32)),
                ("bytesperunit",int32),
                ("reserved",int32),
                ("textcodepage",ctypes.POINTER(int32)) ]
PDCAM_METADATATEXTBLOCK=ctypes.POINTER(DCAM_METADATATEXTBLOCK)
class CDCAM_METADATATEXTBLOCK(ctypes_wrap.CStructWrapper):
    _struct=DCAM_METADATATEXTBLOCK


class DCAM_METADATABINBLOCK(ctypes.Structure):
    _fields_=[  ("hdr",DCAM_METADATABLOCKHDR),
                ("bin",ctypes.c_void_p),
                ("binsizes",ctypes.POINTER(int32)),
                ("bytesperunit",int32),
                ("reserved",int32) ]
PDCAM_METADATABINBLOCK=ctypes.POINTER(DCAM_METADATABINBLOCK)
class CDCAM_METADATABINBLOCK(ctypes_wrap.CStructWrapper):
    _struct=DCAM_METADATABINBLOCK


class DCAMREC_STATUS(ctypes.Structure):
    _fields_=[  ("size",int32),
                ("currentsession_index",int32),
                ("maxframecount_per_session",int32),
                ("currentframe_index",int32),
                ("missingframe_count",int32),
                ("flags",int32),
                ("totalframecount",int32),
                ("reserved",int32) ]
PDCAMREC_STATUS=ctypes.POINTER(DCAMREC_STATUS)
class CDCAMREC_STATUS(ctypes_wrap.CStructWrapper):
    _struct=DCAMREC_STATUS


class DCAM_METADATABLOCK(ctypes.Structure):
    _fields_=[  ("hdr",DCAM_METADATABLOCKHDR),
                ("buf",ctypes.c_void_p),
                ("unitsizes",ctypes.POINTER(int32)),
                ("bytesperunit",int32),
                ("userdata_kind",int32) ]
PDCAM_METADATABLOCK=ctypes.POINTER(DCAM_METADATABLOCK)
class CDCAM_METADATABLOCK(ctypes_wrap.CStructWrapper):
    _struct=DCAM_METADATABLOCK





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
    #  ctypes.c_int dcamapi_init(ctypes.POINTER(DCAMAPI_INIT) param)
    addfunc(lib, "dcamapi_init", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(DCAMAPI_INIT)],
            argnames = ["param"] )
    #  ctypes.c_int dcamapi_uninit()
    addfunc(lib, "dcamapi_uninit", restype = ctypes.c_int,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int dcamdev_open(ctypes.POINTER(DCAMDEV_OPEN) param)
    addfunc(lib, "dcamdev_open", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(DCAMDEV_OPEN)],
            argnames = ["param"] )
    #  ctypes.c_int dcamdev_close(HDCAM h)
    addfunc(lib, "dcamdev_close", restype = ctypes.c_int,
            argtypes = [HDCAM],
            argnames = ["h"] )
    #  ctypes.c_int dcamdev_showpanel(HDCAM h, int32 iKind)
    addfunc(lib, "dcamdev_showpanel", restype = ctypes.c_int,
            argtypes = [HDCAM, int32],
            argnames = ["h", "iKind"] )
    #  ctypes.c_int dcamdev_getcapability(HDCAM h, ctypes.POINTER(DCAMDEV_CAPABILITY) param)
    addfunc(lib, "dcamdev_getcapability", restype = ctypes.c_int,
            argtypes = [HDCAM, ctypes.POINTER(DCAMDEV_CAPABILITY)],
            argnames = ["h", "param"] )
    #  ctypes.c_int dcamdev_getstring(HDCAM h, ctypes.POINTER(DCAMDEV_STRING) param)
    addfunc(lib, "dcamdev_getstring", restype = ctypes.c_int,
            argtypes = [HDCAM, ctypes.POINTER(DCAMDEV_STRING)],
            argnames = ["h", "param"] )
    #  ctypes.c_int dcamdev_setdata(HDCAM h, ctypes.POINTER(DCAMDATA_HDR) param)
    addfunc(lib, "dcamdev_setdata", restype = ctypes.c_int,
            argtypes = [HDCAM, ctypes.POINTER(DCAMDATA_HDR)],
            argnames = ["h", "param"] )
    #  ctypes.c_int dcamdev_getdata(HDCAM h, ctypes.POINTER(DCAMDATA_HDR) param)
    addfunc(lib, "dcamdev_getdata", restype = ctypes.c_int,
            argtypes = [HDCAM, ctypes.POINTER(DCAMDATA_HDR)],
            argnames = ["h", "param"] )
    #  ctypes.c_int dcamprop_getattr(HDCAM h, ctypes.POINTER(DCAMPROP_ATTR) param)
    addfunc(lib, "dcamprop_getattr", restype = ctypes.c_int,
            argtypes = [HDCAM, ctypes.POINTER(DCAMPROP_ATTR)],
            argnames = ["h", "param"] )
    #  ctypes.c_int dcamprop_getvalue(HDCAM h, int32 iProp, ctypes.POINTER(ctypes.c_double) pValue)
    addfunc(lib, "dcamprop_getvalue", restype = ctypes.c_int,
            argtypes = [HDCAM, int32, ctypes.POINTER(ctypes.c_double)],
            argnames = ["h", "iProp", "pValue"] )
    #  ctypes.c_int dcamprop_setvalue(HDCAM h, int32 iProp, ctypes.c_double fValue)
    addfunc(lib, "dcamprop_setvalue", restype = ctypes.c_int,
            argtypes = [HDCAM, int32, ctypes.c_double],
            argnames = ["h", "iProp", "fValue"] )
    #  ctypes.c_int dcamprop_setgetvalue(HDCAM h, int32 iProp, ctypes.POINTER(ctypes.c_double) pValue, int32 option)
    addfunc(lib, "dcamprop_setgetvalue", restype = ctypes.c_int,
            argtypes = [HDCAM, int32, ctypes.POINTER(ctypes.c_double), int32],
            argnames = ["h", "iProp", "pValue", "option"] )
    #  ctypes.c_int dcamprop_queryvalue(HDCAM h, int32 iProp, ctypes.POINTER(ctypes.c_double) pValue, int32 option)
    addfunc(lib, "dcamprop_queryvalue", restype = ctypes.c_int,
            argtypes = [HDCAM, int32, ctypes.POINTER(ctypes.c_double), int32],
            argnames = ["h", "iProp", "pValue", "option"] )
    #  ctypes.c_int dcamprop_getnextid(HDCAM h, ctypes.POINTER(int32) pProp, int32 option)
    addfunc(lib, "dcamprop_getnextid", restype = ctypes.c_int,
            argtypes = [HDCAM, ctypes.POINTER(int32), int32],
            argnames = ["h", "pProp", "option"] )
    #  ctypes.c_int dcamprop_getname(HDCAM h, int32 iProp, ctypes.c_char_p text, int32 textbytes)
    addfunc(lib, "dcamprop_getname", restype = ctypes.c_int,
            argtypes = [HDCAM, int32, ctypes.c_char_p, int32],
            argnames = ["h", "iProp", "text", "textbytes"] )
    #  ctypes.c_int dcamprop_getvaluetext(HDCAM h, ctypes.POINTER(DCAMPROP_VALUETEXT) param)
    addfunc(lib, "dcamprop_getvaluetext", restype = ctypes.c_int,
            argtypes = [HDCAM, ctypes.POINTER(DCAMPROP_VALUETEXT)],
            argnames = ["h", "param"] )
    #  ctypes.c_int dcambuf_alloc(HDCAM h, int32 framecount)
    addfunc(lib, "dcambuf_alloc", restype = ctypes.c_int,
            argtypes = [HDCAM, int32],
            argnames = ["h", "framecount"] )
    #  ctypes.c_int dcambuf_attach(HDCAM h, ctypes.POINTER(DCAMBUF_ATTACH) param)
    addfunc(lib, "dcambuf_attach", restype = ctypes.c_int,
            argtypes = [HDCAM, ctypes.POINTER(DCAMBUF_ATTACH)],
            argnames = ["h", "param"] )
    #  ctypes.c_int dcambuf_release(HDCAM h, int32 iKind)
    addfunc(lib, "dcambuf_release", restype = ctypes.c_int,
            argtypes = [HDCAM, int32],
            argnames = ["h", "iKind"] )
    #  ctypes.c_int dcambuf_lockframe(HDCAM h, ctypes.POINTER(DCAMBUF_FRAME) pFrame)
    addfunc(lib, "dcambuf_lockframe", restype = ctypes.c_int,
            argtypes = [HDCAM, ctypes.POINTER(DCAMBUF_FRAME)],
            argnames = ["h", "pFrame"] )
    #  ctypes.c_int dcambuf_copyframe(HDCAM h, ctypes.POINTER(DCAMBUF_FRAME) pFrame)
    addfunc(lib, "dcambuf_copyframe", restype = ctypes.c_int,
            argtypes = [HDCAM, ctypes.POINTER(DCAMBUF_FRAME)],
            argnames = ["h", "pFrame"] )
    #  ctypes.c_int dcambuf_copymetadata(HDCAM h, ctypes.POINTER(DCAM_METADATAHDR) hdr)
    addfunc(lib, "dcambuf_copymetadata", restype = ctypes.c_int,
            argtypes = [HDCAM, ctypes.POINTER(DCAM_METADATAHDR)],
            argnames = ["h", "hdr"] )
    #  ctypes.c_int dcamcap_start(HDCAM h, int32 mode)
    addfunc(lib, "dcamcap_start", restype = ctypes.c_int,
            argtypes = [HDCAM, int32],
            argnames = ["h", "mode"] )
    #  ctypes.c_int dcamcap_stop(HDCAM h)
    addfunc(lib, "dcamcap_stop", restype = ctypes.c_int,
            argtypes = [HDCAM],
            argnames = ["h"] )
    #  ctypes.c_int dcamcap_status(HDCAM h, ctypes.POINTER(int32) pStatus)
    addfunc(lib, "dcamcap_status", restype = ctypes.c_int,
            argtypes = [HDCAM, ctypes.POINTER(int32)],
            argnames = ["h", "pStatus"] )
    #  ctypes.c_int dcamcap_transferinfo(HDCAM h, ctypes.POINTER(DCAMCAP_TRANSFERINFO) param)
    addfunc(lib, "dcamcap_transferinfo", restype = ctypes.c_int,
            argtypes = [HDCAM, ctypes.POINTER(DCAMCAP_TRANSFERINFO)],
            argnames = ["h", "param"] )
    #  ctypes.c_int dcamcap_firetrigger(HDCAM h, int32 iKind)
    addfunc(lib, "dcamcap_firetrigger", restype = ctypes.c_int,
            argtypes = [HDCAM, int32],
            argnames = ["h", "iKind"] )
    #  ctypes.c_int dcamcap_record(HDCAM h, HDCAMREC hrec)
    addfunc(lib, "dcamcap_record", restype = ctypes.c_int,
            argtypes = [HDCAM, HDCAMREC],
            argnames = ["h", "hrec"] )
    #  ctypes.c_int dcamwait_open(ctypes.POINTER(DCAMWAIT_OPEN) param)
    addfunc(lib, "dcamwait_open", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(DCAMWAIT_OPEN)],
            argnames = ["param"] )
    #  ctypes.c_int dcamwait_close(HDCAMWAIT hWait)
    addfunc(lib, "dcamwait_close", restype = ctypes.c_int,
            argtypes = [HDCAMWAIT],
            argnames = ["hWait"] )
    #  ctypes.c_int dcamwait_start(HDCAMWAIT hWait, ctypes.POINTER(DCAMWAIT_START) param)
    addfunc(lib, "dcamwait_start", restype = ctypes.c_int,
            argtypes = [HDCAMWAIT, ctypes.POINTER(DCAMWAIT_START)],
            argnames = ["hWait", "param"] )
    #  ctypes.c_int dcamwait_abort(HDCAMWAIT hWait)
    addfunc(lib, "dcamwait_abort", restype = ctypes.c_int,
            argtypes = [HDCAMWAIT],
            argnames = ["hWait"] )
    #  ctypes.c_int dcamrec_openA(ctypes.POINTER(DCAMREC_OPENA) param)
    addfunc(lib, "dcamrec_openA", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(DCAMREC_OPENA)],
            argnames = ["param"] )
    #  ctypes.c_int dcamrec_openW(ctypes.POINTER(DCAMREC_OPENW) param)
    addfunc(lib, "dcamrec_openW", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(DCAMREC_OPENW)],
            argnames = ["param"] )
    #  ctypes.c_int dcamrec_close(HDCAMREC hrec)
    addfunc(lib, "dcamrec_close", restype = ctypes.c_int,
            argtypes = [HDCAMREC],
            argnames = ["hrec"] )
    #  ctypes.c_int dcamrec_lockframe(HDCAMREC hrec, ctypes.POINTER(DCAMREC_FRAME) pFrame)
    addfunc(lib, "dcamrec_lockframe", restype = ctypes.c_int,
            argtypes = [HDCAMREC, ctypes.POINTER(DCAMREC_FRAME)],
            argnames = ["hrec", "pFrame"] )
    #  ctypes.c_int dcamrec_copyframe(HDCAMREC hrec, ctypes.POINTER(DCAMREC_FRAME) pFrame)
    addfunc(lib, "dcamrec_copyframe", restype = ctypes.c_int,
            argtypes = [HDCAMREC, ctypes.POINTER(DCAMREC_FRAME)],
            argnames = ["hrec", "pFrame"] )
    #  ctypes.c_int dcamrec_writemetadata(HDCAMREC hrec, ctypes.POINTER(DCAM_METADATAHDR) hdr)
    addfunc(lib, "dcamrec_writemetadata", restype = ctypes.c_int,
            argtypes = [HDCAMREC, ctypes.POINTER(DCAM_METADATAHDR)],
            argnames = ["hrec", "hdr"] )
    #  ctypes.c_int dcamrec_lockmetadata(HDCAMREC hrec, ctypes.POINTER(DCAM_METADATAHDR) hdr)
    addfunc(lib, "dcamrec_lockmetadata", restype = ctypes.c_int,
            argtypes = [HDCAMREC, ctypes.POINTER(DCAM_METADATAHDR)],
            argnames = ["hrec", "hdr"] )
    #  ctypes.c_int dcamrec_copymetadata(HDCAMREC hrec, ctypes.POINTER(DCAM_METADATAHDR) hdr)
    addfunc(lib, "dcamrec_copymetadata", restype = ctypes.c_int,
            argtypes = [HDCAMREC, ctypes.POINTER(DCAM_METADATAHDR)],
            argnames = ["hrec", "hdr"] )
    #  ctypes.c_int dcamrec_lockmetadatablock(HDCAMREC hrec, ctypes.POINTER(DCAM_METADATABLOCKHDR) hdr)
    addfunc(lib, "dcamrec_lockmetadatablock", restype = ctypes.c_int,
            argtypes = [HDCAMREC, ctypes.POINTER(DCAM_METADATABLOCKHDR)],
            argnames = ["hrec", "hdr"] )
    #  ctypes.c_int dcamrec_copymetadatablock(HDCAMREC hrec, ctypes.POINTER(DCAM_METADATABLOCKHDR) hdr)
    addfunc(lib, "dcamrec_copymetadatablock", restype = ctypes.c_int,
            argtypes = [HDCAMREC, ctypes.POINTER(DCAM_METADATABLOCKHDR)],
            argnames = ["hrec", "hdr"] )
    #  ctypes.c_int dcamrec_pause(HDCAMREC hrec)
    addfunc(lib, "dcamrec_pause", restype = ctypes.c_int,
            argtypes = [HDCAMREC],
            argnames = ["hrec"] )
    #  ctypes.c_int dcamrec_resume(HDCAMREC hrec)
    addfunc(lib, "dcamrec_resume", restype = ctypes.c_int,
            argtypes = [HDCAMREC],
            argnames = ["hrec"] )
    #  ctypes.c_int dcamrec_status(HDCAMREC hrec, ctypes.POINTER(DCAMREC_STATUS) pStatus)
    addfunc(lib, "dcamrec_status", restype = ctypes.c_int,
            argtypes = [HDCAMREC, ctypes.POINTER(DCAMREC_STATUS)],
            argnames = ["hrec", "pStatus"] )


