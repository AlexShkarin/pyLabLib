##########   This file is generated automatically based on fgrab_prototyp.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
import platform
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
SSIZE_T=LONG_PTR
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
MirEGLNativeWindowType=ctypes.c_void_p
MirEGLNativeDisplayType=ctypes.c_void_p
class siso_board_type(enum.IntEnum):
    PN_MICROENABLE                           =_int32(0xa1)
    PN_MICROENABLEII                         =_int32(0xa2)
    PN_MICROENABLE3I                         =_int32(0xa3)
    PN_MICROENABLE3IXXL                      =_int32(0xa31)
    PN_MICROENABLE4AD1CL                     =_int32(0xa40)
    PN_MICROENABLE4BASE                      =_int32(PN_MICROENABLE4AD1CL)
    PN_MICROENABLE4BASEx4                    =_int32(0xa43)
    PN_MICROENABLE4AD4CL                     =_int32(0xa42)
    PN_MICROENABLE4VD1CL                     =_int32(0xa41)
    PN_MICROENABLE4FULLx1                    =_int32(PN_MICROENABLE4VD1CL)
    PN_MICROENABLE4VD4CL                     =_int32(0xa44)
    PN_MICROENABLE4FULLx4                    =_int32(PN_MICROENABLE4VD4CL)
    PN_MICROENABLE4AS1CL                     =_int32(0xa45)
    PN_MICROENABLE4VQ4GE                     =_int32(0xe44)
    PN_MICROENABLE4GIGEx4                    =_int32(PN_MICROENABLE4VQ4GE)
    PN_MICROENABLE4AQ4GE                     =_int32(0xe42)
    PN_MICROENABLE4_H264CLx1                 =_int32(0xb41)
    PN_MICROENABLE4_H264pCLx1                =_int32(0xb42)
    PN_PX100                                 =_int32(0xc41)
    PN_PX200                                 =_int32(0xc42)
    PN_PX210                                 =_int32(0xc43)
    PN_PX300                                 =_int32(0xc44)
    PN_MICROENABLE5A1CXP4                    =_int32(0xa51)
    PN_MICROENABLE5A1CLHSF2                  =_int32(0xa52)
    PN_MICROENABLE5AQ8CXP6B                  =_int32(0xa53)
    PN_MICROENABLE5AQ8CXP4                   =_int32(PN_MICROENABLE5AQ8CXP6B)
    PN_MICROENABLE5VQ8CXP6B                  =_int32(0xa54)
    PN_MICROENABLE5VQ8CXP4                   =_int32(PN_MICROENABLE5VQ8CXP6B)
    PN_MICROENABLE5AD8CLHSF2                 =_int32(0xa55)
    PN_MICROENABLE5VQ8CXP6D                  =_int32(0xa56)
    PN_MICROENABLE5AQ8CXP6D                  =_int32(0xa57)
    PN_MICROENABLE5VD8CL                     =_int32(0xa58)
    PN_MICROENABLE5VF8CL                     =_int32(PN_MICROENABLE5VD8CL)
    PN_MICROENABLE5A2CLHSF2                  =_int32(0xa59)
    PN_MICROENABLE5AD8CL                     =_int32(0xa5a)
    PN_MICROENABLE5_LIGHTBRIDGE_VCL_PROTOTYPE=_int32(0x750)
    PN_MICROENABLE5_LIGHTBRIDGE_MARATHON_VCL =_int32(0x751)
    PN_MICROENABLE5_LIGHTBRIDGE_VCL          =_int32(0x7510)
    PN_MICROENABLE5_MARATHON_VCL             =_int32(0x7511)
    PN_MICROENABLE5_MARATHON_AF2_DP          =_int32(0x752)
    PN_MICROENABLE5_MARATHON_ACX_QP          =_int32(0x753)
    PN_MICROENABLE5_LIGHTBRIDGE_MARATHON_ACL =_int32(0x754)
    PN_MICROENABLE5_LIGHTBRIDGE_ACL          =_int32(0x7540)
    PN_MICROENABLE5_MARATHON_ACL             =_int32(0x7541)
    PN_MICROENABLE5_MARATHON_ACX_SP          =_int32(0x755)
    PN_MICROENABLE5_MARATHON_ACX_DP          =_int32(0x756)
    PN_MICROENABLE5_MARATHON_VCX_QP          =_int32(0x757)
    PN_MICROENABLE5_MARATHON_VF2_DP          =_int32(0x758)
    PN_MICROENABLE5_LIGHTBRIDGE_MARATHON_VCLx=_int32(0x759)
    PN_MICROENABLE5_MARATHON_VCLx            =_int32(0x7591)
    PN_TDI                                   =_int32(0xb50)
    PN_TDI_I                                 =_int32(0xb500)
    PN_TDI_II                                =_int32(0xb501)
    PN_TGATE_USB                             =_int32(0xb57)
    PN_TGATE_I_USB                           =_int32(0xb570)
    PN_TGATE_II_USB                          =_int32(0xb571)
    PN_TGATE                                 =_int32(0xb5e)
    PN_TGATE_I                               =_int32(0xb5e0)
    PN_TGATE_II                              =_int32(0xb5e1)
    PN_TGATE_35                              =_int32(0xb58)
    PN_TGATE_I_35                            =_int32(0xb580)
    PN_TGATE_II_35                           =_int32(0xb581)
    PN_TGATE_35_USB                          =_int32(0xb59)
    PN_TGATE_I_35_USB                        =_int32(0xb590)
    PN_TGATE_II_35_USB                       =_int32(0xb591)
    PN_TTDI                                  =_int32(0xb5f)
    PN_MICROENABLE5_ABACUS_4G_PROTOTYPE      =_int32(0xb51)
    PN_MICROENABLE5_ABACUS_4G                =_int32(PN_MICROENABLE5_ABACUS_4G_PROTOTYPE)
    PN_MICROENABLE5_ABACUS_4G_BASE           =_int32(0xb52)
    PN_MICROENABLE5_ABACUS_4G_BASE_II        =_int32(0xb53)
    PN_MICROENABLE6_KCU105                   =_int32(0xA60)
    PN_UNKNOWN                               =_int32(0xffff)
    PN_GENERIC_EVA                           =_int32(0x10000000)
    PN_NONE                                  =_int32(0)
dsiso_board_type={a.name:a.value for a in siso_board_type}
drsiso_board_type={a.value:a.name for a in siso_board_type}


# frameindex_t=ctypes.c_int64
frameindex_t=ctypes.c_int32 if platform.architecture()[0]=="32bit" else ctypes.c_int64
class RowFilterModes(enum.IntEnum):
    _NON_TRIGGERED_EOF_CONTROLLED       =_int32(0)
    _NON_TRIGGERED_LINE_COUNT_CONTROLLED=_int32(0x1)
    _TRIGGERED_EOF_CONTROLLED           =_int32(0x2)
    _TRIGGERED_LINE_COUNT_CONTROLLED    =_int32(0x3)
dRowFilterModes={a.name:a.value for a in RowFilterModes}
drRowFilterModes={a.value:a.name for a in RowFilterModes}


class TriggerMode(enum.IntEnum):
    _GRABBER_CONTROLLED        =_int32(0)
    _GRABBER_CONTROLLED_STROBE =_int32(1)
    _GRABBER_CONTROLLED_TRIGGER=_int32(2)
    _SINGLE_SHOT               =_int32(4)
    _EXTERNAL_TRIGGER          =_int32(6)
dTriggerMode={a.name:a.value for a in TriggerMode}
drTriggerMode={a.value:a.name for a in TriggerMode}


class LineTriggerMode(enum.IntEnum):
    _LRM_AUTO   =_int32(0)
    _LRM_EXT_TRG=_int32(1)
dLineTriggerMode={a.name:a.value for a in LineTriggerMode}
drLineTriggerMode={a.value:a.name for a in LineTriggerMode}


class LineTriggerGateMode(enum.IntEnum):
    _LRM_NON_GATED    =_int32(0)
    _LRM_GATED_COUNT  =_int32(1)
    _LRM_GATED_PARTIAL=_int32(2)
    _LRM_GATED        =_int32(3)
dLineTriggerGateMode={a.name:a.value for a in LineTriggerGateMode}
drLineTriggerGateMode={a.value:a.name for a in LineTriggerGateMode}


class TriggerSync(enum.IntEnum):
    _LVAL  =_int32(0)
    _HDSYNC=_int32(1)
dTriggerSync={a.name:a.value for a in TriggerSync}
drTriggerSync={a.value:a.name for a in TriggerSync}


class MeTriggerMode(enum.IntEnum):
    FREE_RUN                     =_int32(0)
    GRABBER_CONTROLLED           =_int32(1)
    ASYNC_TRIGGER                =_int32(2)
    GRABBER_CONTROLLED_SYNCHRON  =_int32(3)
    ASYNC_SOFTWARE_TRIGGER       =_int32(4)
    ASYNC_GATED                  =_int32(5)
    ASYNC_GATED_MULTIFRAME       =_int32(6)
    ASYNC_SOFTWARE_TRIGGER_QUEUED=_int32(7)
dMeTriggerMode={a.name:a.value for a in MeTriggerMode}
drMeTriggerMode={a.value:a.name for a in MeTriggerMode}


class MeLineTriggerMode(enum.IntEnum):
    GRABBER_CONTROLLED_GATED=_int32(6)
dMeLineTriggerMode={a.name:a.value for a in MeLineTriggerMode}
drMeLineTriggerMode={a.value:a.name for a in MeLineTriggerMode}


class MeShaftMode(enum.IntEnum):
    SOURCE_A=_int32(0)
    SOURCE_B=_int32(1)
dMeShaftMode={a.name:a.value for a in MeShaftMode}
drMeShaftMode={a.value:a.name for a in MeShaftMode}


class MeLineShadingMode(enum.IntEnum):
    SHADING_OFF     =_int32(0)
    SHADING_SUB     =_int32(1)
    SHADING_MULT    =_int32(2)
    SHADING_SUB_MULT=_int32(3)
dMeLineShadingMode={a.name:a.value for a in MeLineShadingMode}
drMeLineShadingMode={a.value:a.name for a in MeLineShadingMode}


class MeKneeLutMode(enum.IntEnum):
    FG_INDEP=_int32(0)
    FG_DEP  =_int32(1)
dMeKneeLutMode={a.name:a.value for a in MeKneeLutMode}
drMeKneeLutMode={a.value:a.name for a in MeKneeLutMode}


class MeAreaTriggerMode(enum.IntEnum):
    AREA_FREE_RUN                   =_int32(0)
    AREA_GRABBER_CONTROLLED         =_int32(1)
    AREA_ASYNC_TRIGGER              =_int32(2)
    AREA_GRABBER_CONTROLLED_SYNCHRON=_int32(3)
    AREA_ASYNC_SOFTWARE_TRIGGER     =_int32(4)
dMeAreaTriggerMode={a.name:a.value for a in MeAreaTriggerMode}
drMeAreaTriggerMode={a.value:a.name for a in MeAreaTriggerMode}


class MeLineTriggerModeLine(enum.IntEnum):
    LINE_FREE_RUN_LINE                =_int32(0)
    LINE_GRABBER_CONTROLLED_LINE      =_int32(1)
    LINE_ASYNC_TRIGGER_LINE           =_int32(2)
    LINE_ASYNC_GATED_LINE             =_int32(5)
    LINE_GRABBER_CONTROLLED_GATED_LINE=_int32(6)
dMeLineTriggerModeLine={a.name:a.value for a in MeLineTriggerModeLine}
drMeLineTriggerModeLine={a.value:a.name for a in MeLineTriggerModeLine}


class MeLineTriggerModeImage(enum.IntEnum):
    LINE_FREE_RUN_IMAGE                =_int32(0)
    LINE_GRABBER_CONTROLLED_IMAGE      =_int32(1)
    LINE_ASYNC_TRIGGER_IMAGE           =_int32(2)
    LINE_GRABBER_CONTROLLED_GATED_IMAGE=_int32(5)
    LINE_ASYNC_GATED_MULTIBUFFERS_IMAGE=_int32(6)
dMeLineTriggerModeImage={a.name:a.value for a in MeLineTriggerModeImage}
drMeLineTriggerModeImage={a.value:a.name for a in MeLineTriggerModeImage}


class MeRgbComponentMapping(enum.IntEnum):
    FG_MAP_PIXEL0=_int32(0)
    FG_MAP_PIXEL1=_int32(1)
    FG_MAP_PIXEL2=_int32(2)
    FG_MAP_PIXEL3=_int32(3)
dMeRgbComponentMapping={a.name:a.value for a in MeRgbComponentMapping}
drMeRgbComponentMapping={a.value:a.name for a in MeRgbComponentMapping}


class MeCameraLinkFormat(enum.IntEnum):
    FG_CL_SINGLETAP_8_BIT    =_int32(8)
    FG_CL_SINGLETAP_10_BIT   =_int32(10)
    FG_CL_SINGLETAP_12_BIT   =_int32(12)
    FG_CL_SINGLETAP_14_BIT   =_int32(14)
    FG_CL_SINGLETAP_16_BIT   =_int32(16)
    FG_CL_DUALTAP_8_BIT      =_int32(108)
    FG_CL_DUALTAP_10_BIT     =_int32(110)
    FG_CL_DUALTAP_12_BIT     =_int32(112)
    FG_CL_TRIPLETAP_8_BIT    =_int32(120)
    FG_CL_LITE_8_BIT         =_int32(130)
    FG_CL_LITE_10_BIT        =_int32(140)
    FG_CL_RGB                =_int32(500)
    FG_CL_MEDIUM_8_BIT       =_int32(208)
    FG_CL_MEDIUM_10_BIT      =_int32(210)
    FG_CL_MEDIUM_12_BIT      =_int32(212)
    FG_CL_MEDIUM_3_TAP_10_BIT=_int32(219)
    FG_CL_MEDIUM_3_TAP_12_BIT=_int32(220)
    FG_CL_MEDIUM_RGB_24      =_int32(214)
    FG_CL_MEDIUM_RGB_30      =_int32(216)
    FG_CL_MEDIUM_RGB_36      =_int32(218)
    FG_CL_8BIT_FULL_8        =_int32(308)
    FG_CL_8BIT_FULL_10       =_int32(310)
    FG_CL_FULL_8_TAP_10_BIT  =_int32(311)
    FG_CL_FULL_8_TAP_RGB_24  =_int32(320)
    FG_CL_FULL_10_TAP_RGB_24 =_int32(321)
    FG_CL_FULL_8_TAP_RGB_30  =_int32(322)
dMeCameraLinkFormat={a.name:a.value for a in MeCameraLinkFormat}
drMeCameraLinkFormat={a.value:a.name for a in MeCameraLinkFormat}


class MeCameraTypes(enum.IntEnum):
    FG_AREA_GRAY                 =_int32(0)
    FG_AREA_BAYER                =_int32(1)
    FG_LINE_GRAY                 =_int32(2)
    FG_SINGLE_LINE_RGB           =_int32(3)
    FG_DUAL_LINE_RGB             =_int32(4)
    FG_SINGLE_AREA_RGB           =_int32(5)
    FG_DUAL_AREA_RGB             =_int32(6)
    FG_AREA_HSI                  =_int32(7)
    FG_DUAL_LINE_RGB_SHADING     =_int32(8)
    FG_SINGLE_LINE_RGBHSI        =_int32(9)
    FG_SINGLE_AREA_RGB_SEPARATION=_int32(10)
    FG_MEDIUM_LINE_RGB           =_int32(11)
    FG_MEDIUM_LINE_GRAY          =_int32(12)
    FG_MEDIUM_AREA_GRAY          =_int32(13)
    FG_MEDIUM_AREA_RGB           =_int32(14)
    FG_AREA_GRAY12               =_int32(15)
    FG_SEQUENCE_EXTRACTOR_A      =_int32(16)
    FG_SEQUENCE_EXTRACTOR_B      =_int32(17)
    FG_LINE_GRAY12               =_int32(18)
    FG_AREA_RGB36                =_int32(19)
    FG_DUAL_LINE_RGB_SORTING     =_int32(20)
    FG_DUAL_LINE_GRAY12          =_int32(21)
    FG_MEDIUM_LINE_GRAY12        =_int32(22)
    FG_SINGLE_AREA_GRAY12        =_int32(23)
    FG_2D_SHADING_12             =_int32(24)
    DIVISOR_1                    =_int32(25)
    DIVISOR_2                    =_int32(26)
    DIVISOR_4                    =_int32(27)
    DIVISOR_8                    =_int32(28)
    DIVISOR_3                    =_int32(29)
    DIVISOR_16                   =_int32(30)
    DIVISOR_6                    =_int32(31)
dMeCameraTypes={a.name:a.value for a in MeCameraTypes}
drMeCameraTypes={a.value:a.name for a in MeCameraTypes}


class MeSensorReadoutModes2(enum.IntEnum):
    SMODE_UNCHANGED=_int32(0)
    SMODE_REVERSE  =_int32(3)
    SMODE_TAB2_0   =_int32(1)
    SMODE_TAB2_1   =_int32(4)
    SMODE_TAB2_2   =_int32(6)
    SMODE_TAB4_0   =_int32(2)
    SMODE_TAB4_1   =_int32(5)
    SMODE_TAB4_2   =_int32(7)
    SMODE_TAB4_5   =_int32(8)
    SMODE_TAB4_3   =_int32(9)
    SMODE_TAB4_4   =_int32(10)
    SMODE_TAB4_6   =_int32(11)
    SMODE_TAB8_0   =_int32(30)
    SMODE_TAB8_1   =_int32(31)
    SMODE_TAB8_2   =_int32(32)
    SMODE_TAB8_3   =_int32(33)
    SMODE_TAB8_4   =_int32(34)
    SMODE_TAB8_5   =_int32(35)
    SMODE_TAB8_6   =_int32(36)
    SMODE_TAB8_7   =_int32(37)
    SMODE_TAB8_8   =_int32(38)
    SMODE_TAB8_9   =_int32(39)
    SMODE_TAB8_10  =_int32(40)
    SMODE_TAB8_11  =_int32(41)
    SMODE_TAB8_12  =_int32(42)
    SMODE_TAB8_13  =_int32(43)
    SMODE_TAB8_14  =_int32(44)
    SMODE_TAB8_15  =_int32(45)
    SMODE_TAB8_16  =_int32(46)
    SMODE_TAB8_17  =_int32(47)
    SMODE_TAB8_18  =_int32(48)
    SMODE_TAB8_19  =_int32(49)
    SMODE_TAB8_20  =_int32(50)
    SMODE_TAB8_21  =_int32(51)
    SMODE_TAB8_22  =_int32(52)
    SMODE_TAB8_23  =_int32(53)
    SMODE_TAB8_24  =_int32(54)
    SMODE_TAB10_1  =_int32(60)
    SMODE_TAB10_2  =_int32(61)
    SMODE_TAB10_4  =_int32(63)
    SMODE_TAB10_3  =_int32(62)
dMeSensorReadoutModes2={a.name:a.value for a in MeSensorReadoutModes2}
drMeSensorReadoutModes2={a.value:a.name for a in MeSensorReadoutModes2}


class FgParamTypes(enum.IntEnum):
    FG_PARAM_TYPE_INVALID                =_int32(0x0)
    FG_PARAM_TYPE_INT32_T                =_int32(0x1)
    FG_PARAM_TYPE_UINT32_T               =_int32(0x2)
    FG_PARAM_TYPE_INT64_T                =_int32(0x3)
    FG_PARAM_TYPE_UINT64_T               =_int32(0x4)
    FG_PARAM_TYPE_DOUBLE                 =_int32(0x5)
    FG_PARAM_TYPE_CHAR_PTR               =_int32(0x6)
    FG_PARAM_TYPE_SIZE_T                 =_int32(0x7)
    FG_PARAM_TYPE_CHAR_PTR_PTR           =_int32(0x16)
    FG_PARAM_TYPE_STRUCT_FIELDPARAMACCESS=_int32(0x1000)
    FG_PARAM_TYPE_STRUCT_FIELDPARAMINT   =_int32(0x1002)
    FG_PARAM_TYPE_STRUCT_FIELDPARAMINT64 =_int32(0x1003)
    FG_PARAM_TYPE_STRUCT_FIELDPARAMDOUBLE=_int32(0x1005)
    FG_PARAM_TYPE_COMPLEX_DATATYPE       =_int32(0x2000)
    FG_PARAM_TYPE_AUTO                   =_int32((-1))
dFgParamTypes={a.name:a.value for a in FgParamTypes}
drFgParamTypes={a.value:a.name for a in FgParamTypes}


class MeInitFlags(enum.IntEnum):
    FG_INIT_FLAG_DEFAULT    =_int32(0x00)
    FG_INIT_FLAG_SLAVE      =_int32(0x01)
    FG_INIT_FLAGS_VALID_MASK=_int32((~(FG_INIT_FLAG_DEFAULT|FG_INIT_FLAG_SLAVE)))
dMeInitFlags={a.name:a.value for a in MeInitFlags}
drMeInitFlags={a.value:a.name for a in MeInitFlags}


class FgImageSourceTypes(enum.IntEnum):
    FG_CAMPORT        =_int32(0)
    FG_CAMERASIMULATOR=_int32(1)
    FG_GENERATOR      =_int32(1)
dFgImageSourceTypes={a.name:a.value for a in FgImageSourceTypes}
drFgImageSourceTypes={a.value:a.name for a in FgImageSourceTypes}


class FgParamEnumGbeCamType(enum.IntEnum):
    RGB8_PACKED =_int32(0)
    BGR8_PACKED =_int32(1)
    RGBA8_PACKED=_int32(2)
    BGRA8_PACKED=_int32(3)
dFgParamEnumGbeCamType={a.name:a.value for a in FgParamEnumGbeCamType}
drFgParamEnumGbeCamType={a.value:a.name for a in FgParamEnumGbeCamType}


class CameraSimulatorTriggerMode(enum.IntEnum):
    SIMULATION_FREE_RUN       =_int32(0)
    RISING_EDGE_TRIGGERS_LINE =_int32(8)
    RISING_EDGE_TRIGGERS_FRAME=_int32(9)
dCameraSimulatorTriggerMode={a.name:a.value for a in CameraSimulatorTriggerMode}
drCameraSimulatorTriggerMode={a.value:a.name for a in CameraSimulatorTriggerMode}


class BOARD_INFORMATION_SELECTOR(enum.IntEnum):
    BINFO_BOARDTYPE   =_int32(0)
    BINFO_POCL        =_int32(1)
    BINFO_PCIE_PAYLOAD=_int32(2)
dBOARD_INFORMATION_SELECTOR={a.name:a.value for a in BOARD_INFORMATION_SELECTOR}
drBOARD_INFORMATION_SELECTOR={a.value:a.name for a in BOARD_INFORMATION_SELECTOR}


class Fg_Info_Selector(enum.IntEnum):
    INFO_APPLET_CAPABILITY_TAGS                =_int32(1)
    INFO_TIMESTAMP_FREQUENCY                   =_int32(100)
    INFO_OWN_BOARDINDEX                        =_int32(101)
    INFO_NR_OF_BOARDS                          =_int32(1000)
    INFO_MAX_NR_OF_BOARDS                      =_int32(1001)
    INFO_BOARDNAME                             =_int32(1010)
    INFO_BOARDTYPE                             =_int32(1011)
    INFO_BOARDSERIALNO                         =_int32(1012)
    INFO_BOARDSUBTYPE                          =_int32(1013)
    INFO_FIRMWAREVERSION                       =_int32(1015)
    INFO_HARDWAREVERSION                       =_int32(1016)
    INFO_PHYSICAL_LOCATION                     =_int32(1017)
    INFO_BOARDSTATUS                           =_int32(1020)
    INFO_PIXELPLANT_PRESENT                    =_int32(1030)
    INFO_CAMERA_INTERFACE                      =_int32(1040)
    INFO_DRIVERVERSION                         =_int32(1100)
    INFO_DRIVERARCH                            =_int32(1101)
    INFO_DRIVERFULLVERSION                     =_int32(1102)
    INFO_BOARDNODENUMBER                       =_int32(1103)
    INFO_DRIVERGROUPAFFINITY                   =_int32(1104)
    INFO_DRIVERAFFINITYMASK                    =_int32(1105)
    INFO_DESIGN_ID                             =_int32(1200)
    INFO_BITSTREAM_ID                          =_int32(1201)
    INFO_APPLET_DESIGN_ID                      =_int32(1202)
    INFO_APPLET_BITSTREAM_ID                   =_int32(1203)
    INFO_FPGA_BITSTREAM_ID                     =_int32(1204)
    INFO_APPLET_FULL_PATH                      =_int32(1300)
    INFO_APPLET_FILE_NAME                      =_int32(1301)
    INFO_APPLET_TYPE                           =_int32(1302)
    INFO_STATUS_PCI_LINK_WIDTH                 =_int32(2001)
    INFO_STATUS_PCI_PAYLOAD_MODE               =_int32(2002)
    INFO_STATUS_PCI_LINK_SPEED                 =_int32(2003)
    INFO_STATUS_PCI_PAYLOAD_SIZE               =_int32(2004)
    INFO_STATUS_PCI_EXPECTED_LINK_WIDTH        =_int32(2005)
    INFO_STATUS_PCI_EXPECTED_LINK_SPEED        =_int32(2006)
    INFO_STATUS_PCI_NATIVE_LINK_SPEED          =_int32(2007)
    INFO_STATUS_PCI_REQUEST_SIZE               =_int32(2008)
    INFO_STATUS_PCI_NROF_INVALID_8B10B_CHARS   =_int32(2101)
    INFO_STATUS_PCI_NROF_8B10B_DISPARITY_ERRORS=_int32(2102)
    INFO_SERVICE_ISRUNNING                     =_int32(3001)
dFg_Info_Selector={a.name:a.value for a in Fg_Info_Selector}
drFg_Info_Selector={a.value:a.name for a in Fg_Info_Selector}


class Fg_BoardStatus_Bits(enum.IntEnum):
    INFO_BOARDSTATUS_CONFIGURED     =_int32(0x00000001)
    INFO_BOARDSTATUS_LOCKED         =_int32(0x00000002)
    INFO_BOARDSTATUS_DEAD_1         =_int32(0x00008000)
    INFO_BOARDSTATUS_RECONFIGURING  =_int32(0x10000000)
    INFO_BOARDSTATUS_REBOOT_REQUIRED=_int32(0x20000000)
    INFO_BOARDSTATUS_OVERTEMP       =_int32(0x40000000)
    INFO_BOARDSTATUS_DEAD_2         =_int32(0x80000000)
    INFO_BOARDSTATUS_DEAD           =_int32((INFO_BOARDSTATUS_DEAD_1|INFO_BOARDSTATUS_DEAD_2))
dFg_BoardStatus_Bits={a.name:a.value for a in Fg_BoardStatus_Bits}
drFg_BoardStatus_Bits={a.value:a.name for a in Fg_BoardStatus_Bits}


class FgProperty(enum.IntEnum):
    PROP_ID_VALUE        =_int32(0)
    PROP_ID_DATATYPE     =_int32(1)
    PROP_ID_NAME         =_int32(2)
    PROP_ID_PARAMETERNAME=_int32(3)
    PROP_ID_VALUELLEN    =_int32(4)
    PROP_ID_ACCESS_ID    =_int32(5)
    PROP_ID_MIN_ID       =_int32(6)
    PROP_ID_MAX_ID       =_int32(7)
    PROP_ID_STEP_ID      =_int32(8)
    PROP_ID_ACCESS       =_int32(9)
    PROP_ID_MIN          =_int32(10)
    PROP_ID_MAX          =_int32(11)
    PROP_ID_STEP         =_int32(12)
    PROP_ID_IS_ENUM      =_int32(13)
    PROP_ID_ENUM_VALUES  =_int32(14)
    PROP_ID_FIELD_SIZE   =_int32(15)
dFgProperty={a.name:a.value for a in FgProperty}
drFgProperty={a.value:a.name for a in FgProperty}


class FgPropertyEnumValues(ctypes.Structure):
    _fields_=[  ("value",ctypes.c_int32),
                ("name",ctypes.c_char*1) ]
PFgPropertyEnumValues=ctypes.POINTER(FgPropertyEnumValues)
class CFgPropertyEnumValues(ctypes_wrap.CStructWrapper):
    _struct=FgPropertyEnumValues


class FgStopAcquireFlags(enum.IntEnum):
    STOP_ASYNC         =_int32(0x00)
    STOP_SYNC_TO_APC   =_int32(0x04)
    STOP_ASYNC_FALLBACK=_int32(0x40000000)
    STOP_SYNC          =_int32(0x80000000)
dFgStopAcquireFlags={a.name:a.value for a in FgStopAcquireFlags}
drFgStopAcquireFlags={a.value:a.name for a in FgStopAcquireFlags}


Fg_ApcFunc_t=ctypes.c_void_p
class Fg_Apc_Flag(enum.IntEnum):
    FG_APC_DEFAULTS             =_int32(0x0)
    FG_APC_BATCH_FRAMES         =_int32(0x1)
    FG_APC_IGNORE_TIMEOUTS      =_int32(0x2)
    FG_APC_IGNORE_APCFUNC_RETURN=_int32(0x4)
    FG_APC_IGNORE_STOP          =_int32(0x8)
    FG_APC_HIGH_PRIORITY        =_int32(0x10)
    FG_APC_DELIVER_ERRORS       =_int32(0x20)
dFg_Apc_Flag={a.name:a.value for a in Fg_Apc_Flag}
drFg_Apc_Flag={a.value:a.name for a in Fg_Apc_Flag}


class FgApcControlFlags(enum.IntEnum):
    FG_APC_CONTROL_BASIC=_int32(0)
dFgApcControlFlags={a.name:a.value for a in FgApcControlFlags}
drFgApcControlFlags={a.value:a.name for a in FgApcControlFlags}


Fg_EventFunc_t=ctypes.c_void_p
class FgEventControlFlags(enum.IntEnum):
    FG_EVENT_DEFAULT_FLAGS=_int32(0)
    FG_EVENT_BATCHED      =_int32(0x1)
dFgEventControlFlags={a.name:a.value for a in FgEventControlFlags}
drFgEventControlFlags={a.value:a.name for a in FgEventControlFlags}


class FgEventNotifiers(enum.IntEnum):
    FG_EVENT_NOTIFY_JOINED   =_int32(0x1)
    FG_EVENT_NOTIFY_TIMESTAMP=_int32(0x2)
    FG_EVENT_NOTIFY_PAYLOAD  =_int32(0x4)
    FG_EVENT_NOTIFY_LOST     =_int32(0x8)
dFgEventNotifiers={a.name:a.value for a in FgEventNotifiers}
drFgEventNotifiers={a.value:a.name for a in FgEventNotifiers}


Fg_AsyncNotifyFunc_t=ctypes.c_void_p
class CCsel(enum.IntEnum):
    CC_EXSYNC         =_int32(0)
    CC_PRESCALER      =_int32(1)
    CC_HDSYNC         =_int32(CC_PRESCALER)
    CC_EXSYNC2        =_int32(CC_PRESCALER)
    CC_STROBEPULSE    =_int32(2)
    CC_CLK            =_int32(3)
    CC_GND            =_int32(4)
    CC_VCC            =_int32(5)
    CC_NOT_EXSYNC     =_int32(6)
    CC_NOT_PRESCALER  =_int32(7)
    CC_NOT_HDSYNC     =_int32(CC_NOT_PRESCALER)
    CC_NOT_EXSYNC2    =_int32(CC_NOT_PRESCALER)
    CC_NOT_STROBEPULSE=_int32(8)
    FG_OTHER          =_int32((-1))
dCCsel={a.name:a.value for a in CCsel}
drCCsel={a.value:a.name for a in CCsel}


class SignalSelectLine(enum.IntEnum):
    FG_SIGNAL_CAM0_EXSYNC     =_int32(2000)
    FG_SIGNAL_CAM0_EXSYNC2    =_int32(2001)
    FG_SIGNAL_CAM0_FLASH      =_int32(2002)
    FG_SIGNAL_CAM0_LVAL       =_int32(2007)
    FG_SIGNAL_CAM0_FVAL       =_int32(2008)
    FG_SIGNAL_CAM0_LINE_START =_int32(2100)
    FG_SIGNAL_CAM0_LINE_END   =_int32(2101)
    FG_SIGNAL_CAM0_FRAME_START=_int32(2102)
    FG_SIGNAL_CAM0_FRAME_END  =_int32(2103)
    FG_SIGNAL_CAM1_EXSYNC     =_int32(2010)
    FG_SIGNAL_CAM1_EXSYNC2    =_int32(2011)
    FG_SIGNAL_CAM1_FLASH      =_int32(2012)
    FG_SIGNAL_CAM1_LVAL       =_int32(2017)
    FG_SIGNAL_CAM1_FVAL       =_int32(2018)
    FG_SIGNAL_CAM1_LINE_START =_int32(2110)
    FG_SIGNAL_CAM1_LINE_END   =_int32(2111)
    FG_SIGNAL_CAM1_FRAME_START=_int32(2112)
    FG_SIGNAL_CAM1_FRAME_END  =_int32(2113)
    FG_SIGNAL_CAM2_EXSYNC     =_int32(2020)
    FG_SIGNAL_CAM2_EXSYNC2    =_int32(2021)
    FG_SIGNAL_CAM2_FLASH      =_int32(2022)
    FG_SIGNAL_CAM2_LVAL       =_int32(2027)
    FG_SIGNAL_CAM2_FVAL       =_int32(2028)
    FG_SIGNAL_CAM2_LINE_START =_int32(2120)
    FG_SIGNAL_CAM2_LINE_END   =_int32(2121)
    FG_SIGNAL_CAM2_FRAME_START=_int32(2122)
    FG_SIGNAL_CAM2_FRAME_END  =_int32(2123)
    FG_SIGNAL_CAM3_EXSYNC     =_int32(2030)
    FG_SIGNAL_CAM3_EXSYNC2    =_int32(2031)
    FG_SIGNAL_CAM3_FLASH      =_int32(2032)
    FG_SIGNAL_CAM3_LVAL       =_int32(2037)
    FG_SIGNAL_CAM3_FVAL       =_int32(2038)
    FG_SIGNAL_CAM3_LINE_START =_int32(2130)
    FG_SIGNAL_CAM3_LINE_END   =_int32(2131)
    FG_SIGNAL_CAM3_FRAME_START=_int32(2132)
    FG_SIGNAL_CAM3_FRAME_END  =_int32(2133)
    FG_SIGNAL_GPI_0           =_int32(1001)
    FG_SIGNAL_GPI_1           =_int32(1011)
    FG_SIGNAL_GPI_2           =_int32(1021)
    FG_SIGNAL_GPI_3           =_int32(1031)
    FG_SIGNAL_GPI_4           =_int32(1041)
    FG_SIGNAL_GPI_5           =_int32(1051)
    FG_SIGNAL_GPI_6           =_int32(1061)
    FG_SIGNAL_GPI_7           =_int32(1071)
    FG_SIGNAL_FRONT_GPI_0     =_int32(1081)
    FG_SIGNAL_FRONT_GPI_1     =_int32(1091)
    FG_SIGNAL_FRONT_GPI_2     =_int32(1101)
    FG_SIGNAL_FRONT_GPI_3     =_int32(1111)
dSignalSelectLine={a.name:a.value for a in SignalSelectLine}
drSignalSelectLine={a.value:a.name for a in SignalSelectLine}


class CcSignalMappingArea(enum.IntEnum):
    CC_PULSEGEN0       =_int32(0)
    CC_PULSEGEN1       =_int32(1)
    CC_PULSEGEN2       =_int32(2)
    CC_PULSEGEN3       =_int32(3)
    CC_NOT_PULSEGEN0   =_int32(6)
    CC_NOT_PULSEGEN1   =_int32(7)
    CC_NOT_PULSEGEN2   =_int32(8)
    CC_NOT_PULSEGEN3   =_int32(9)
    CC_INPUT_BYPASS    =_int32(10)
    CC_NOT_INPUT_BYPASS=_int32(11)
dCcSignalMappingArea={a.name:a.value for a in CcSignalMappingArea}
drCcSignalMappingArea={a.value:a.name for a in CcSignalMappingArea}


class CcSignalMappingLineExtended(enum.IntEnum):
    CC_GPI_0          =_int32(1001)
    CC_NOT_GPI_0      =_int32(1000)
    CC_GPI_1          =_int32(1011)
    CC_NOT_GPI_1      =_int32(1010)
    CC_GPI_2          =_int32(1021)
    CC_NOT_GPI_2      =_int32(1020)
    CC_GPI_3          =_int32(1031)
    CC_NOT_GPI_3      =_int32(1030)
    CC_GPI_4          =_int32(1041)
    CC_NOT_GPI_4      =_int32(1040)
    CC_GPI_5          =_int32(1051)
    CC_NOT_GPI_5      =_int32(1050)
    CC_GPI_6          =_int32(1061)
    CC_NOT_GPI_6      =_int32(1060)
    CC_GPI_7          =_int32(1071)
    CC_NOT_GPI_7      =_int32(1070)
    CC_FRONT_GPI_0    =_int32(1081)
    CC_NOT_FRONT_GPI_0=_int32(1080)
    CC_FRONT_GPI_1    =_int32(1091)
    CC_NOT_FRONT_GPI_1=_int32(1090)
    CC_FRONT_GPI_2    =_int32(1101)
    CC_NOT_FRONT_GPI_2=_int32(1100)
    CC_FRONT_GPI_3    =_int32(1111)
    CC_NOT_FRONT_GPI_3=_int32(1110)
dCcSignalMappingLineExtended={a.name:a.value for a in CcSignalMappingLineExtended}
drCcSignalMappingLineExtended={a.value:a.name for a in CcSignalMappingLineExtended}


class Fg_PoCXPState(enum.IntEnum):
    BOOTING       =_int32(0x001)
    NOCABLE       =_int32(0x002)
    NOPOCXP       =_int32(0x004)
    POCXPOK       =_int32(0x008)
    MIN_CURR      =_int32(0x010)
    MAX_CURR      =_int32(0x020)
    LOW_VOLT      =_int32(0x040)
    OVER_VOLT     =_int32(0x080)
    ADC_Chip_Error=_int32(0x100)
dFg_PoCXPState={a.name:a.value for a in Fg_PoCXPState}
drFg_PoCXPState={a.value:a.name for a in Fg_PoCXPState}


class VantagePointNamingConvention(enum.IntEnum):
    FG_VANTAGEPOINT_TOP_LEFT    =_int32(0)
    FG_VANTAGEPOINT_TOP_RIGHT   =_int32(1)
    FG_VANTAGEPOINT_BOTTOM_LEFT =_int32(2)
    FG_VANTAGEPOINT_BOTTOM_RIGHT=_int32(3)
dVantagePointNamingConvention={a.name:a.value for a in VantagePointNamingConvention}
drVantagePointNamingConvention={a.value:a.name for a in VantagePointNamingConvention}


class TapGeometryNamingConvention(enum.IntEnum):
    FG_GEOMETRY_1X     =_int32(0x01100000)
    FG_GEOMETRY_1X2    =_int32(0x01200000)
    FG_GEOMETRY_2X     =_int32(0x02100000)
    FG_GEOMETRY_2XE    =_int32(0x02110000)
    FG_GEOMETRY_2XM    =_int32(0x02120000)
    FG_GEOMETRY_1X3    =_int32(0x01300000)
    FG_GEOMETRY_3X     =_int32(0x03100000)
    FG_GEOMETRY_1X4    =_int32(0x01400000)
    FG_GEOMETRY_4X     =_int32(0x04100000)
    FG_GEOMETRY_4XE    =_int32(0x04110000)
    FG_GEOMETRY_2X2    =_int32(0x02200000)
    FG_GEOMETRY_2X2E   =_int32(0x02210000)
    FG_GEOMETRY_2X2M   =_int32(0x02220000)
    FG_GEOMETRY_1X8    =_int32(0x01800000)
    FG_GEOMETRY_8X     =_int32(0x08100000)
    FG_GEOMETRY_1X10   =_int32(0x01A00000)
    FG_GEOMETRY_10X    =_int32(0x0A100000)
    FG_GEOMETRY_4X2    =_int32(0x04200000)
    FG_GEOMETRY_4X2E   =_int32(0x04210000)
    FG_GEOMETRY_5X2    =_int32(0x05200000)
    FG_GEOMETRY_1X_1Y  =_int32(0x01100110)
    FG_GEOMETRY_1X_2Y  =_int32(0x01100210)
    FG_GEOMETRY_1X_2YE =_int32(0x01100211)
    FG_GEOMETRY_2X_1Y  =_int32(0x02100110)
    FG_GEOMETRY_2XE_1Y =_int32(0x02110110)
    FG_GEOMETRY_2XM_1Y =_int32(0x02120110)
    FG_GEOMETRY_2X_2Y  =_int32(0x02100210)
    FG_GEOMETRY_2X_2YE =_int32(0x02100211)
    FG_GEOMETRY_2XE_2Y =_int32(0x02110210)
    FG_GEOMETRY_2XE_2YE=_int32(0x02110211)
    FG_GEOMETRY_2XM_2Y =_int32(0x02120210)
    FG_GEOMETRY_2XM_2YE=_int32(0x02120211)
    FG_GEOMETRY_4X_1Y  =_int32(0x04100110)
    FG_GEOMETRY_1X2_1Y =_int32(0x01200110)
    FG_GEOMETRY_1X3_1Y =_int32(0x01300110)
    FG_GEOMETRY_1X4_1Y =_int32(0x01400110)
    FG_GEOMETRY_2X2_1Y =_int32(0x02200110)
    FG_GEOMETRY_2X2E_1Y=_int32(0x02210110)
    FG_GEOMETRY_2X2M_1Y=_int32(0x02220110)
    FG_GEOMETRY_1X2_2YE=_int32(0x01200211)
dTapGeometryNamingConvention={a.name:a.value for a in TapGeometryNamingConvention}
drTapGeometryNamingConvention={a.value:a.name for a in TapGeometryNamingConvention}


class PixelFormatNamingConvention(enum.IntEnum):
    Mono8    =_int32(257)
    Mono10   =_int32(258)
    Mono12   =_int32(259)
    Mono14   =_int32(260)
    Mono16   =_int32(261)
    BayerGR8 =_int32(785)
    BayerGR10=_int32(786)
    BayerGR12=_int32(787)
    BayerGR14=_int32(788)
    BayerRG8 =_int32(801)
    BayerRG10=_int32(802)
    BayerRG12=_int32(803)
    BayerRG14=_int32(804)
    BayerGB8 =_int32(817)
    BayerGB10=_int32(818)
    BayerGB12=_int32(819)
    BayerGB14=_int32(820)
    BayerBG8 =_int32(833)
    BayerBG10=_int32(834)
    BayerBG12=_int32(835)
    BayerBG14=_int32(836)
    RGB8     =_int32(1025)
    RGB10    =_int32(1026)
    RGB12    =_int32(1027)
    RGB14    =_int32(1028)
    RGB16    =_int32(1029)
    RGBA8    =_int32(1281)
    RGBA10   =_int32(1282)
    RGBA12   =_int32(1283)
    RGBA14   =_int32(1284)
    RGBA16   =_int32(1285)
dPixelFormatNamingConvention={a.name:a.value for a in PixelFormatNamingConvention}
drPixelFormatNamingConvention={a.value:a.name for a in PixelFormatNamingConvention}


class BayerOrdering(enum.IntEnum):
    GreenFollowedByRed =_int32(3)
    GreenFollowedByBlue=_int32(0)
    RedFollowedByGreen =_int32(2)
    BlueFollowedByGreen=_int32(1)
dBayerOrdering={a.name:a.value for a in BayerOrdering}
drBayerOrdering={a.value:a.name for a in BayerOrdering}


class BayerBilinearLineOrdering(enum.IntEnum):
    RedBlueLineFollowedByGreenLine=_int32(10)
    BlueRedLineFollowedByGreenLine=_int32(11)
    GreenLineFollowedByRedBlueLine=_int32(12)
    GreenLineFollowedByBlueRedLine=_int32(13)
dBayerBilinearLineOrdering={a.name:a.value for a in BayerBilinearLineOrdering}
drBayerBilinearLineOrdering={a.value:a.name for a in BayerBilinearLineOrdering}


class GigEPixelFormat(enum.IntEnum):
    MONO8        =_int32(0)
    MONO8_SIGNED =_int32(1)
    MONO10       =_int32(2)
    MONO10_PACKED=_int32(3)
    MONO12       =_int32(4)
    MONO12_PACKED=_int32(5)
    MONO14       =_int32(7)
    MONO16       =_int32(6)
dGigEPixelFormat={a.name:a.value for a in GigEPixelFormat}
drGigEPixelFormat={a.value:a.name for a in GigEPixelFormat}


class CXPTriggerPackedModes(enum.IntEnum):
    FG_STANDARD        =_int32(0)
    FG_RISING_EDGE_ONLY=_int32(1)
dCXPTriggerPackedModes={a.name:a.value for a in CXPTriggerPackedModes}
drCXPTriggerPackedModes={a.value:a.name for a in CXPTriggerPackedModes}


Fg_AppletIteratorType=ctypes.c_void_p
Fg_AppletIteratorItem=ctypes.c_void_p
class FgAppletIteratorSource(enum.IntEnum):
    FG_AIS_BOARD     =_int32(0)
    FG_AIS_FILESYSTEM=enum.auto()
dFgAppletIteratorSource={a.name:a.value for a in FgAppletIteratorSource}
drFgAppletIteratorSource={a.value:a.name for a in FgAppletIteratorSource}


class FgAppletIntProperty(enum.IntEnum):
    FG_AP_INT_FLAGS           =_int32(0)
    FG_AP_INT_INFO            =enum.auto()
    FG_AP_INT_PARTITION       =enum.auto()
    FG_AP_INT_NR_OF_DMA       =enum.auto()
    FG_AP_INT_NR_OF_CAMS      =enum.auto()
    FG_AP_INT_GROUP_CODE      =enum.auto()
    FG_AP_INT_USER_CODE       =enum.auto()
    FG_AP_INT_BOARD_GROUP_MASK=enum.auto()
    FG_AP_INT_BOARD_USER_CODE =enum.auto()
    FG_AP_INT_ICON_SIZE       =enum.auto()
    FG_AP_INT_LAG             =enum.auto()
    FG_AP_INT_DESIGN_VERSION  =enum.auto()
    FG_AP_INT_DESIGN_REVISION =enum.auto()
dFgAppletIntProperty={a.name:a.value for a in FgAppletIntProperty}
drFgAppletIntProperty={a.value:a.name for a in FgAppletIntProperty}


class FgAppletStringProperty(enum.IntEnum):
    FG_AP_STRING_APPLET_UID         =_int32(0)
    FG_AP_STRING_BITSTREAM_UID      =enum.auto()
    FG_AP_STRING_DESIGN_NAME        =enum.auto()
    FG_AP_STRING_APPLET_NAME        =enum.auto()
    FG_AP_STRING_DESCRIPTION        =enum.auto()
    FG_AP_STRING_CATEGORY           =enum.auto()
    FG_AP_STRING_APPLET_PATH        =enum.auto()
    FG_AP_STRING_ICON               =enum.auto()
    FG_AP_STRING_SUPPORTED_PLATFORMS=enum.auto()
    FG_AP_STRING_TAGS               =enum.auto()
    FG_AP_STRING_VERSION            =enum.auto()
    FG_AP_STRING_APPLET_FILE        =enum.auto()
    FG_AP_STRING_RUNTIME_VERSION    =enum.auto()
dFgAppletStringProperty={a.name:a.value for a in FgAppletStringProperty}
drFgAppletStringProperty={a.value:a.name for a in FgAppletStringProperty}


class LookupTable(ctypes.Structure):
    _fields_=[  ("lut",ctypes.POINTER(ctypes.c_uint)),
                ("id",ctypes.c_uint),
                ("nrOfElements",ctypes.c_uint),
                ("format",ctypes.c_uint),
                ("number",ctypes.c_ubyte) ]
PLookupTable=ctypes.POINTER(LookupTable)
class CLookupTable(ctypes_wrap.CStructWrapper):
    _struct=LookupTable


class KneeLookupTable(ctypes.Structure):
    _fields_=[  ("value",ctypes.POINTER(ctypes.c_double)),
                ("reserved",ctypes.POINTER(ctypes.c_double)),
                ("id",ctypes.c_uint),
                ("nrOfElements",ctypes.c_uint),
                ("format",ctypes.c_uint),
                ("number",ctypes.c_ubyte) ]
PKneeLookupTable=ctypes.POINTER(KneeLookupTable)
class CKneeLookupTable(ctypes_wrap.CStructWrapper):
    _struct=KneeLookupTable


class ShadingParameter(ctypes.Structure):
    _fields_=[  ("offset",ctypes.POINTER(ctypes.c_ubyte)),
                ("cmult",ctypes.POINTER(ctypes.c_ubyte)),
                ("mult",ctypes.POINTER(ctypes.c_float)),
                ("nrOfElements",ctypes.c_uint),
                ("width",ctypes.c_int),
                ("height",ctypes.c_int),
                ("set",ctypes.c_int) ]
PShadingParameter=ctypes.POINTER(ShadingParameter)
class CShadingParameter(ctypes_wrap.CStructWrapper):
    _struct=ShadingParameter


class LineShadingParameter(ctypes.Structure):
    _fields_=[  ("mShadingData",ctypes.c_uint*4096),
                ("mNoOfPixelsInit",ctypes.c_int) ]
PLineShadingParameter=ctypes.POINTER(LineShadingParameter)
class CLineShadingParameter(ctypes_wrap.CStructWrapper):
    _struct=LineShadingParameter


class FieldParameterInt(ctypes.Structure):
    _fields_=[  ("value",ctypes.c_uint32),
                ("index",ctypes.c_uint) ]
PFieldParameterInt=ctypes.POINTER(FieldParameterInt)
class CFieldParameterInt(ctypes_wrap.CStructWrapper):
    _struct=FieldParameterInt


class FieldParameterDouble(ctypes.Structure):
    _fields_=[  ("value",ctypes.c_double),
                ("index",ctypes.c_uint) ]
PFieldParameterDouble=ctypes.POINTER(FieldParameterDouble)
class CFieldParameterDouble(ctypes_wrap.CStructWrapper):
    _struct=FieldParameterDouble


class FieldParameterAccess(ctypes.Structure):
    _fields_=[  ("vtype",ctypes.c_int),
                ("index",ctypes.c_uint),
                ("count",ctypes.c_uint),
                ("p_int32_t",ctypes.POINTER(ctypes.c_int32)) ]
PFieldParameterAccess=ctypes.POINTER(FieldParameterAccess)
class CFieldParameterAccess(ctypes_wrap.CStructWrapper):
    _struct=FieldParameterAccess


class FgApcControl(ctypes.Structure):
    _fields_=[  ("version",ctypes.c_uint),
                ("func",Fg_ApcFunc_t),
                ("data",ctypes.c_void_p),
                ("timeout",ctypes.c_uint),
                ("flags",ctypes.c_uint) ]
PFgApcControl=ctypes.POINTER(FgApcControl)
class CFgApcControl(ctypes_wrap.CStructWrapper):
    _struct=FgApcControl





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
    #  ctypes.c_int CreateDisplay(ctypes.c_uint nDepth, ctypes.c_uint nWidth, ctypes.c_uint nHeight)
    addfunc(lib, "CreateDisplay", restype = ctypes.c_int,
            argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint],
            argnames = ["nDepth", "nWidth", "nHeight"] )
    #  None SetBufferWidth(ctypes.c_int nId, ctypes.c_uint nWidth, ctypes.c_uint nHeight)
    addfunc(lib, "SetBufferWidth", restype = None,
            argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.c_uint],
            argnames = ["nId", "nWidth", "nHeight"] )
    #  None DrawBuffer(ctypes.c_int nId, ctypes.c_void_p ulpBuf, ctypes.c_int nNr, ctypes.c_char_p cpStr)
    addfunc(lib, "DrawBuffer", restype = None,
            argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p],
            argnames = ["nId", "ulpBuf", "nNr", "cpStr"] )
    #  None CloseDisplay(ctypes.c_int nId)
    addfunc(lib, "CloseDisplay", restype = None,
            argtypes = [ctypes.c_int],
            argnames = ["nId"] )
    #  ctypes.c_int SetDisplayDepth(ctypes.c_int nId, ctypes.c_uint depth)
    addfunc(lib, "SetDisplayDepth", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_uint],
            argnames = ["nId", "depth"] )
    #  ctypes.c_int Fg_InitLibraries(ctypes.c_char_p sisoDir)
    addfunc(lib, "Fg_InitLibraries", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p],
            argnames = ["sisoDir"] )
    #  ctypes.c_int Fg_InitLibrariesEx(ctypes.c_char_p sisoDir, ctypes.c_uint flags, ctypes.c_char_p id, ctypes.c_uint timeout)
    addfunc(lib, "Fg_InitLibrariesEx", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint],
            argnames = ["sisoDir", "flags", "id", "timeout"] )
    #  None Fg_AbortInitLibraries()
    addfunc(lib, "Fg_AbortInitLibraries", restype = None,
            argtypes = [],
            argnames = [] )
    #  None Fg_InitLibrariesStartNextSlave()
    addfunc(lib, "Fg_InitLibrariesStartNextSlave", restype = None,
            argtypes = [],
            argnames = [] )
    #  None Fg_FreeLibraries()
    addfunc(lib, "Fg_FreeLibraries", restype = None,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int Fg_findApplet(ctypes.c_uint BoardIndex, ctypes.c_char_p Path, ctypes.c_size_t Size)
    addfunc(lib, "Fg_findApplet", restype = ctypes.c_int,
            argtypes = [ctypes.c_uint, ctypes.c_char_p, ctypes.c_size_t],
            argnames = ["BoardIndex", "Path", "Size"] )
    #  ctypes.c_void_p Fg_Init(ctypes.c_char_p FileName, ctypes.c_uint BoardIndex)
    addfunc(lib, "Fg_Init", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_char_p, ctypes.c_uint],
            argnames = ["FileName", "BoardIndex"] )
    #  ctypes.c_void_p Fg_InitConfig(ctypes.c_char_p Config_Name, ctypes.c_uint BoardIndex)
    addfunc(lib, "Fg_InitConfig", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_char_p, ctypes.c_uint],
            argnames = ["Config_Name", "BoardIndex"] )
    #  ctypes.c_void_p Fg_InitEx(ctypes.c_char_p FileName, ctypes.c_uint BoardIndex, ctypes.c_int flags)
    addfunc(lib, "Fg_InitEx", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_int],
            argnames = ["FileName", "BoardIndex", "flags"] )
    #  ctypes.c_void_p Fg_InitConfigEx(ctypes.c_char_p Config_Name, ctypes.c_uint BoardIndex, ctypes.c_int flags)
    addfunc(lib, "Fg_InitConfigEx", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_int],
            argnames = ["Config_Name", "BoardIndex", "flags"] )
    #  ctypes.c_int Fg_FreeGrabber(ctypes.c_void_p Fg)
    addfunc(lib, "Fg_FreeGrabber", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["Fg"] )
    #  ctypes.c_void_p Fg_AllocMem(ctypes.c_void_p Fg, ctypes.c_size_t Size, frameindex_t BufCnt, ctypes.c_uint DmaIndex)
    addfunc(lib, "Fg_AllocMem", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, ctypes.c_size_t, frameindex_t, ctypes.c_uint],
            argnames = ["Fg", "Size", "BufCnt", "DmaIndex"] )
    #  ctypes.c_void_p Fg_AllocMemEx(ctypes.c_void_p Fg, ctypes.c_size_t Size, frameindex_t BufCnt)
    addfunc(lib, "Fg_AllocMemEx", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, ctypes.c_size_t, frameindex_t],
            argnames = ["Fg", "Size", "BufCnt"] )
    #  ctypes.c_int Fg_FreeMem(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex)
    addfunc(lib, "Fg_FreeMem", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint],
            argnames = ["Fg", "DmaIndex"] )
    #  ctypes.c_int Fg_FreeMemEx(ctypes.c_void_p Fg, ctypes.c_void_p mem)
    addfunc(lib, "Fg_FreeMemEx", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["Fg", "mem"] )
    #  ctypes.c_void_p Fg_AllocMemHead(ctypes.c_void_p Fg, ctypes.c_size_t Size, frameindex_t BufCnt)
    addfunc(lib, "Fg_AllocMemHead", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, ctypes.c_size_t, frameindex_t],
            argnames = ["Fg", "Size", "BufCnt"] )
    #  ctypes.c_int Fg_FreeMemHead(ctypes.c_void_p Fg, ctypes.c_void_p memHandle)
    addfunc(lib, "Fg_FreeMemHead", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["Fg", "memHandle"] )
    #  ctypes.c_int Fg_AddMem(ctypes.c_void_p Fg, ctypes.c_void_p pBuffer, ctypes.c_size_t Size, frameindex_t bufferIndex, ctypes.c_void_p memHandle)
    addfunc(lib, "Fg_AddMem", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, frameindex_t, ctypes.c_void_p],
            argnames = ["Fg", "pBuffer", "Size", "bufferIndex", "memHandle"] )
    #  ctypes.c_int Fg_DelMem(ctypes.c_void_p Fg, ctypes.c_void_p memHandle, frameindex_t bufferIndex)
    addfunc(lib, "Fg_DelMem", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, frameindex_t],
            argnames = ["Fg", "memHandle", "bufferIndex"] )
    #  ctypes.c_void_p Fg_NumaAllocDmaBuffer(ctypes.c_void_p Fg, ctypes.c_size_t Size)
    addfunc(lib, "Fg_NumaAllocDmaBuffer", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, ctypes.c_size_t],
            argnames = ["Fg", "Size"] )
    #  ctypes.c_int Fg_NumaFreeDmaBuffer(ctypes.c_void_p Fg, ctypes.c_void_p Buffer)
    addfunc(lib, "Fg_NumaFreeDmaBuffer", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["Fg", "Buffer"] )
    #  ctypes.c_int Fg_NumaPinThread(ctypes.c_void_p Fg)
    addfunc(lib, "Fg_NumaPinThread", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["Fg"] )
    #  ctypes.c_int Fg_getNrOfParameter(ctypes.c_void_p Fg)
    addfunc(lib, "Fg_getNrOfParameter", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["Fg"] )
    #  ctypes.c_int Fg_getParameterId(ctypes.c_void_p fg, ctypes.c_int index)
    addfunc(lib, "Fg_getParameterId", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["fg", "index"] )
    #  ctypes.c_char_p Fg_getParameterName(ctypes.c_void_p fg, ctypes.c_int index)
    addfunc(lib, "Fg_getParameterName", restype = ctypes.c_char_p,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["fg", "index"] )
    #  ctypes.c_int Fg_getParameterIdByName(ctypes.c_void_p fg, ctypes.c_char_p name)
    addfunc(lib, "Fg_getParameterIdByName", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p],
            argnames = ["fg", "name"] )
    #  ctypes.c_char_p Fg_getParameterNameById(ctypes.c_void_p fg, ctypes.c_uint id, ctypes.c_uint dma)
    addfunc(lib, "Fg_getParameterNameById", restype = ctypes.c_char_p,
            argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint],
            argnames = ["fg", "id", "dma"] )
    #  ctypes.c_int Fg_setParameter(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_void_p Value, ctypes.c_uint DmaIndex)
    addfunc(lib, "Fg_setParameter", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint],
            argnames = ["Fg", "Parameter", "Value", "DmaIndex"] )
    #  ctypes.c_int Fg_setParameterWithType(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_void_p Value, ctypes.c_uint DmaIndex, ctypes.c_int type)
    addfunc(lib, "Fg_setParameterWithType", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint, ctypes.c_int],
            argnames = ["Fg", "Parameter", "Value", "DmaIndex", "type"] )
    #  ctypes.c_int Fg_getParameter(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_void_p Value, ctypes.c_uint DmaIndex)
    addfunc(lib, "Fg_getParameter", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint],
            argnames = ["Fg", "Parameter", "Value", "DmaIndex"] )
    #  ctypes.c_int Fg_getParameterWithType(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_void_p Value, ctypes.c_uint DmaIndex, ctypes.c_int type)
    addfunc(lib, "Fg_getParameterWithType", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint, ctypes.c_int],
            argnames = ["Fg", "Parameter", "Value", "DmaIndex", "type"] )
    #  ctypes.c_int Fg_freeParameterStringWithType(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_void_p Value, ctypes.c_uint DmaIndex, ctypes.c_int type)
    addfunc(lib, "Fg_freeParameterStringWithType", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint, ctypes.c_int],
            argnames = ["Fg", "Parameter", "Value", "DmaIndex", "type"] )
    #  ctypes.c_int Fg_getParameterEx(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_void_p Value, ctypes.c_uint DmaIndex, ctypes.c_void_p pMem, frameindex_t ImgNr)
    addfunc(lib, "Fg_getParameterEx", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, frameindex_t],
            argnames = ["Fg", "Parameter", "Value", "DmaIndex", "pMem", "ImgNr"] )
    #  ctypes.c_int Fg_getParameterInfoXML(ctypes.c_void_p Fg, ctypes.c_int port, ctypes.c_char_p infoBuffer, ctypes.POINTER(ctypes.c_size_t) infoBufferSize)
    addfunc(lib, "Fg_getParameterInfoXML", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["Fg", "port", "infoBuffer", "infoBufferSize"] )
    #  ctypes.c_int Fg_getBitsPerPixel(ctypes.c_int format)
    addfunc(lib, "Fg_getBitsPerPixel", restype = ctypes.c_int,
            argtypes = [ctypes.c_int],
            argnames = ["format"] )
    #  ctypes.c_int Fg_saveConfig(ctypes.c_void_p Fg, ctypes.c_char_p Filename)
    addfunc(lib, "Fg_saveConfig", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p],
            argnames = ["Fg", "Filename"] )
    #  ctypes.c_int Fg_saveFieldParameterToFile(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_uint DmaIndex, ctypes.c_char_p FileName)
    addfunc(lib, "Fg_saveFieldParameterToFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint, ctypes.c_char_p],
            argnames = ["Fg", "Parameter", "DmaIndex", "FileName"] )
    #  ctypes.c_int Fg_loadConfig(ctypes.c_void_p Fg, ctypes.c_char_p Filename)
    addfunc(lib, "Fg_loadConfig", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p],
            argnames = ["Fg", "Filename"] )
    #  ctypes.c_int Fg_loadFieldParameterFromFile(ctypes.c_void_p Fg, ctypes.c_int Parameter, ctypes.c_uint DmaIndex, ctypes.c_char_p FileName)
    addfunc(lib, "Fg_loadFieldParameterFromFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint, ctypes.c_char_p],
            argnames = ["Fg", "Parameter", "DmaIndex", "FileName"] )
    #  ctypes.c_int Fg_Acquire(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex, frameindex_t PicCount)
    addfunc(lib, "Fg_Acquire", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint, frameindex_t],
            argnames = ["Fg", "DmaIndex", "PicCount"] )
    #  ctypes.c_int Fg_stopAcquire(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex)
    addfunc(lib, "Fg_stopAcquire", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint],
            argnames = ["Fg", "DmaIndex"] )
    #  frameindex_t Fg_getLastPicNumberBlocking(ctypes.c_void_p Fg, frameindex_t PicNr, ctypes.c_uint DmaIndex, ctypes.c_int Timeout)
    addfunc(lib, "Fg_getLastPicNumberBlocking", restype = frameindex_t,
            argtypes = [ctypes.c_void_p, frameindex_t, ctypes.c_uint, ctypes.c_int],
            argnames = ["Fg", "PicNr", "DmaIndex", "Timeout"] )
    #  frameindex_t Fg_getLastPicNumber(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex)
    addfunc(lib, "Fg_getLastPicNumber", restype = frameindex_t,
            argtypes = [ctypes.c_void_p, ctypes.c_uint],
            argnames = ["Fg", "DmaIndex"] )
    #  frameindex_t Fg_getLastPicNumberBlockingEx(ctypes.c_void_p Fg, frameindex_t PicNr, ctypes.c_uint DmaIndex, ctypes.c_int Timeout, ctypes.c_void_p pMem)
    addfunc(lib, "Fg_getLastPicNumberBlockingEx", restype = frameindex_t,
            argtypes = [ctypes.c_void_p, frameindex_t, ctypes.c_uint, ctypes.c_int, ctypes.c_void_p],
            argnames = ["Fg", "PicNr", "DmaIndex", "Timeout", "pMem"] )
    #  frameindex_t Fg_getLastPicNumberEx(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex, ctypes.c_void_p pMem)
    addfunc(lib, "Fg_getLastPicNumberEx", restype = frameindex_t,
            argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p],
            argnames = ["Fg", "DmaIndex", "pMem"] )
    #  ctypes.c_void_p Fg_getImagePtr(ctypes.c_void_p Fg, frameindex_t PicNr, ctypes.c_uint DmaIndex)
    addfunc(lib, "Fg_getImagePtr", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, frameindex_t, ctypes.c_uint],
            argnames = ["Fg", "PicNr", "DmaIndex"] )
    #  ctypes.c_void_p Fg_getImagePtrEx(ctypes.c_void_p Fg, frameindex_t PicNr, ctypes.c_uint DmaIndex, ctypes.c_void_p pMem)
    addfunc(lib, "Fg_getImagePtrEx", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, frameindex_t, ctypes.c_uint, ctypes.c_void_p],
            argnames = ["Fg", "PicNr", "DmaIndex", "pMem"] )
    #  ctypes.c_int Fg_AcquireEx(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex, frameindex_t PicCount, ctypes.c_int nFlag, ctypes.c_void_p memHandle)
    addfunc(lib, "Fg_AcquireEx", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint, frameindex_t, ctypes.c_int, ctypes.c_void_p],
            argnames = ["Fg", "DmaIndex", "PicCount", "nFlag", "memHandle"] )
    #  ctypes.c_int Fg_sendImage(ctypes.c_void_p Fg, frameindex_t startImage, frameindex_t PicCount, ctypes.c_int nFlag, ctypes.c_uint DmaIndex)
    addfunc(lib, "Fg_sendImage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, frameindex_t, frameindex_t, ctypes.c_int, ctypes.c_uint],
            argnames = ["Fg", "startImage", "PicCount", "nFlag", "DmaIndex"] )
    #  ctypes.c_int Fg_sendImageEx(ctypes.c_void_p Fg, frameindex_t startImage, frameindex_t PicCount, ctypes.c_int nFlag, ctypes.c_uint DmaIndex, ctypes.c_void_p memHandle)
    addfunc(lib, "Fg_sendImageEx", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, frameindex_t, frameindex_t, ctypes.c_int, ctypes.c_uint, ctypes.c_void_p],
            argnames = ["Fg", "startImage", "PicCount", "nFlag", "DmaIndex", "memHandle"] )
    #  ctypes.c_int Fg_stopAcquireEx(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex, ctypes.c_void_p memHandle, ctypes.c_int nFlag)
    addfunc(lib, "Fg_stopAcquireEx", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_int],
            argnames = ["Fg", "DmaIndex", "memHandle", "nFlag"] )
    #  frameindex_t Fg_getImage(ctypes.c_void_p Fg, ctypes.c_int Param, frameindex_t PicNr, ctypes.c_uint DmaIndex, ctypes.c_uint Timeout)
    addfunc(lib, "Fg_getImage", restype = frameindex_t,
            argtypes = [ctypes.c_void_p, ctypes.c_int, frameindex_t, ctypes.c_uint, ctypes.c_uint],
            argnames = ["Fg", "Param", "PicNr", "DmaIndex", "Timeout"] )
    #  frameindex_t Fg_getImageEx(ctypes.c_void_p Fg, ctypes.c_int Param, frameindex_t PicNr, ctypes.c_uint DmaIndex, ctypes.c_uint Timeout, ctypes.c_void_p pMem)
    addfunc(lib, "Fg_getImageEx", restype = frameindex_t,
            argtypes = [ctypes.c_void_p, ctypes.c_int, frameindex_t, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p],
            argnames = ["Fg", "Param", "PicNr", "DmaIndex", "Timeout", "pMem"] )
    #  ctypes.c_int Fg_registerApcHandler(ctypes.c_void_p Fg, ctypes.c_uint DmaIndex, ctypes.c_void_p control, ctypes.c_int flags)
    addfunc(lib, "Fg_registerApcHandler", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_int],
            argnames = ["Fg", "DmaIndex", "control", "flags"] )
    #  ctypes.c_int Fg_getLastErrorNumber(ctypes.c_void_p Fg)
    addfunc(lib, "Fg_getLastErrorNumber", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["Fg"] )
    #  ctypes.c_char_p getErrorDescription(ctypes.c_int ErrorNumber)
    addfunc(lib, "getErrorDescription", restype = ctypes.c_char_p,
            argtypes = [ctypes.c_int],
            argnames = ["ErrorNumber"] )
    #  ctypes.c_char_p Fg_getLastErrorDescription(ctypes.c_void_p Fg)
    addfunc(lib, "Fg_getLastErrorDescription", restype = ctypes.c_char_p,
            argtypes = [ctypes.c_void_p],
            argnames = ["Fg"] )
    #  ctypes.c_char_p Fg_getErrorDescription(ctypes.c_void_p Fg, ctypes.c_int ErrorNumber)
    addfunc(lib, "Fg_getErrorDescription", restype = ctypes.c_char_p,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["Fg", "ErrorNumber"] )
    #  ctypes.c_int Fg_getBoardType(ctypes.c_int BoardIndex)
    addfunc(lib, "Fg_getBoardType", restype = ctypes.c_int,
            argtypes = [ctypes.c_int],
            argnames = ["BoardIndex"] )
    #  ctypes.c_char_p Fg_getBoardNameByType(ctypes.c_int BoardType, ctypes.c_int UseShortName)
    addfunc(lib, "Fg_getBoardNameByType", restype = ctypes.c_char_p,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["BoardType", "UseShortName"] )
    #  ctypes.c_uint Fg_getSerialNumber(ctypes.c_void_p Fg)
    addfunc(lib, "Fg_getSerialNumber", restype = ctypes.c_uint,
            argtypes = [ctypes.c_void_p],
            argnames = ["Fg"] )
    #  ctypes.c_char_p Fg_getSWVersion()
    addfunc(lib, "Fg_getSWVersion", restype = ctypes.c_char_p,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_char_p Fg_getAppletVersion(ctypes.c_void_p Fg, ctypes.c_int AppletId)
    addfunc(lib, "Fg_getAppletVersion", restype = ctypes.c_char_p,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["Fg", "AppletId"] )
    #  ctypes.c_int Fg_getAppletId(ctypes.c_void_p Fg, ctypes.c_char_p ignored)
    addfunc(lib, "Fg_getAppletId", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p],
            argnames = ["Fg", "ignored"] )
    #  ctypes.c_int Fg_getParameterProperty(ctypes.c_void_p Fg, ctypes.c_int parameterId, ctypes.c_int propertyId, ctypes.c_void_p buffer, ctypes.POINTER(ctypes.c_int) bufLen)
    addfunc(lib, "Fg_getParameterProperty", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["Fg", "parameterId", "propertyId", "buffer", "bufLen"] )
    #  ctypes.c_int Fg_getParameterPropertyEx(ctypes.c_void_p Fg, ctypes.c_int parameterId, ctypes.c_int propertyId, ctypes.c_int DmaIndex, ctypes.c_void_p buffer, ctypes.POINTER(ctypes.c_int) bufLen)
    addfunc(lib, "Fg_getParameterPropertyEx", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["Fg", "parameterId", "propertyId", "DmaIndex", "buffer", "bufLen"] )
    #  ctypes.c_int Fg_getSystemInformation(ctypes.c_void_p Fg, ctypes.c_int selector, ctypes.c_int propertyId, ctypes.c_int param1, ctypes.c_void_p buffer, ctypes.POINTER(ctypes.c_uint) bufLen)
    addfunc(lib, "Fg_getSystemInformation", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)],
            argnames = ["Fg", "selector", "propertyId", "param1", "buffer", "bufLen"] )
    #  ctypes.c_int Fg_readUserDataArea(ctypes.c_void_p Fg, ctypes.c_int boardId, ctypes.c_uint offs, ctypes.c_uint size, ctypes.c_void_p buffer)
    addfunc(lib, "Fg_readUserDataArea", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p],
            argnames = ["Fg", "boardId", "offs", "size", "buffer"] )
    #  ctypes.c_int Fg_writeUserDataArea(ctypes.c_void_p Fg, ctypes.c_int boardId, ctypes.c_uint offs, ctypes.c_uint size, ctypes.c_void_p buffer)
    addfunc(lib, "Fg_writeUserDataArea", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p],
            argnames = ["Fg", "boardId", "offs", "size", "buffer"] )
    #  frameindex_t Fg_getStatus(ctypes.c_void_p Fg, ctypes.c_int Param, frameindex_t Data, ctypes.c_uint DmaIndex)
    addfunc(lib, "Fg_getStatus", restype = frameindex_t,
            argtypes = [ctypes.c_void_p, ctypes.c_int, frameindex_t, ctypes.c_uint],
            argnames = ["Fg", "Param", "Data", "DmaIndex"] )
    #  frameindex_t Fg_getStatusEx(ctypes.c_void_p Fg, ctypes.c_int Param, frameindex_t Data, ctypes.c_uint DmaIndex, ctypes.c_void_p pMem)
    addfunc(lib, "Fg_getStatusEx", restype = frameindex_t,
            argtypes = [ctypes.c_void_p, ctypes.c_int, frameindex_t, ctypes.c_uint, ctypes.c_void_p],
            argnames = ["Fg", "Param", "Data", "DmaIndex", "pMem"] )
    #  ctypes.c_int Fg_setStatus(ctypes.c_void_p Fg, ctypes.c_int Param, frameindex_t Data, ctypes.c_uint DmaIndex)
    addfunc(lib, "Fg_setStatus", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, frameindex_t, ctypes.c_uint],
            argnames = ["Fg", "Param", "Data", "DmaIndex"] )
    #  ctypes.c_int Fg_setStatusEx(ctypes.c_void_p Fg, ctypes.c_int Param, frameindex_t Data, ctypes.c_uint DmaIndex, ctypes.c_void_p pMem)
    addfunc(lib, "Fg_setStatusEx", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, frameindex_t, ctypes.c_uint, ctypes.c_void_p],
            argnames = ["Fg", "Param", "Data", "DmaIndex", "pMem"] )
    #  ctypes.c_int Fg_getAppletIterator(ctypes.c_int boardIndex, ctypes.c_int src, ctypes.POINTER(Fg_AppletIteratorType) iter, ctypes.c_int flags)
    addfunc(lib, "Fg_getAppletIterator", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(Fg_AppletIteratorType), ctypes.c_int],
            argnames = ["boardIndex", "src", "iter", "flags"] )
    #  ctypes.c_int Fg_freeAppletIterator(Fg_AppletIteratorType iter)
    addfunc(lib, "Fg_freeAppletIterator", restype = ctypes.c_int,
            argtypes = [Fg_AppletIteratorType],
            argnames = ["iter"] )
    #  Fg_AppletIteratorItem Fg_getAppletIteratorItem(Fg_AppletIteratorType iter, ctypes.c_int index)
    addfunc(lib, "Fg_getAppletIteratorItem", restype = Fg_AppletIteratorItem,
            argtypes = [Fg_AppletIteratorType, ctypes.c_int],
            argnames = ["iter", "index"] )
    #  Fg_AppletIteratorItem Fg_findAppletIteratorItem(Fg_AppletIteratorType iter, ctypes.c_char_p path)
    addfunc(lib, "Fg_findAppletIteratorItem", restype = Fg_AppletIteratorItem,
            argtypes = [Fg_AppletIteratorType, ctypes.c_char_p],
            argnames = ["iter", "path"] )
    #  Fg_AppletIteratorItem Fg_addAppletIteratorItem(Fg_AppletIteratorType iter, ctypes.c_char_p path, ctypes.POINTER(ctypes.c_int) numItems)
    addfunc(lib, "Fg_addAppletIteratorItem", restype = Fg_AppletIteratorItem,
            argtypes = [Fg_AppletIteratorType, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["iter", "path", "numItems"] )
    #  ctypes.c_int64 Fg_getAppletIntProperty(Fg_AppletIteratorItem item, ctypes.c_int property)
    addfunc(lib, "Fg_getAppletIntProperty", restype = ctypes.c_int64,
            argtypes = [Fg_AppletIteratorItem, ctypes.c_int],
            argnames = ["item", "property"] )
    #  ctypes.c_char_p Fg_getAppletStringProperty(Fg_AppletIteratorItem item, ctypes.c_int property)
    addfunc(lib, "Fg_getAppletStringProperty", restype = ctypes.c_char_p,
            argtypes = [Fg_AppletIteratorItem, ctypes.c_int],
            argnames = ["item", "property"] )
    #  ctypes.c_uint64 Fg_getEventMask(ctypes.c_void_p Fg, ctypes.c_char_p name)
    addfunc(lib, "Fg_getEventMask", restype = ctypes.c_uint64,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p],
            argnames = ["Fg", "name"] )
    #  ctypes.c_int Fg_getEventPayload(ctypes.c_void_p Fg, ctypes.c_uint64 mask)
    addfunc(lib, "Fg_getEventPayload", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint64],
            argnames = ["Fg", "mask"] )
    #  ctypes.c_char_p Fg_getEventName(ctypes.c_void_p Fg, ctypes.c_uint64 mask)
    addfunc(lib, "Fg_getEventName", restype = ctypes.c_char_p,
            argtypes = [ctypes.c_void_p, ctypes.c_uint64],
            argnames = ["Fg", "mask"] )
    #  ctypes.c_int Fg_getEventCount(ctypes.c_void_p Fg)
    addfunc(lib, "Fg_getEventCount", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["Fg"] )
    #  ctypes.c_int Fg_activateEvents(ctypes.c_void_p Fg, ctypes.c_uint64 mask, ctypes.c_uint enable)
    addfunc(lib, "Fg_activateEvents", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint],
            argnames = ["Fg", "mask", "enable"] )
    #  ctypes.c_int Fg_clearEvents(ctypes.c_void_p Fg, ctypes.c_uint64 mask)
    addfunc(lib, "Fg_clearEvents", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint64],
            argnames = ["Fg", "mask"] )
    #  ctypes.c_uint64 Fg_eventWait(ctypes.c_void_p Fg, ctypes.c_uint64 mask, ctypes.c_uint timeout, ctypes.c_uint flags, ctypes.c_void_p info)
    addfunc(lib, "Fg_eventWait", restype = ctypes.c_uint64,
            argtypes = [ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p],
            argnames = ["Fg", "mask", "timeout", "flags", "info"] )
    #  ctypes.c_int Fg_registerEventCallback(ctypes.c_void_p Fg, ctypes.c_uint64 mask, Fg_EventFunc_t handler, ctypes.c_void_p data, ctypes.c_uint flags, ctypes.c_void_p info)
    addfunc(lib, "Fg_registerEventCallback", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint64, Fg_EventFunc_t, ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p],
            argnames = ["Fg", "mask", "handler", "data", "flags", "info"] )
    #  ctypes.c_int Fg_registerAsyncNotifyCallback(ctypes.c_void_p Fg, Fg_AsyncNotifyFunc_t handler, ctypes.c_void_p context)
    addfunc(lib, "Fg_registerAsyncNotifyCallback", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, Fg_AsyncNotifyFunc_t, ctypes.c_void_p],
            argnames = ["Fg", "handler", "context"] )
    #  ctypes.c_int Fg_unregisterAsyncNotifyCallback(ctypes.c_void_p Fg, Fg_AsyncNotifyFunc_t handler, ctypes.c_void_p context)
    addfunc(lib, "Fg_unregisterAsyncNotifyCallback", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, Fg_AsyncNotifyFunc_t, ctypes.c_void_p],
            argnames = ["Fg", "handler", "context"] )
    #  ctypes.c_int Fg_resetAsyncNotify(ctypes.c_void_p Fg, ctypes.c_ulong notification, ctypes.c_ulong pl, ctypes.c_ulong ph)
    addfunc(lib, "Fg_resetAsyncNotify", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong],
            argnames = ["Fg", "notification", "pl", "ph"] )
    #  ctypes.c_int Fg_setExsync(ctypes.c_void_p Fg, ctypes.c_int Flag, ctypes.c_uint CamPort)
    addfunc(lib, "Fg_setExsync", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint],
            argnames = ["Fg", "Flag", "CamPort"] )
    #  ctypes.c_int Fg_setFlash(ctypes.c_void_p Fg, ctypes.c_int Flag, ctypes.c_uint CamPort)
    addfunc(lib, "Fg_setFlash", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint],
            argnames = ["Fg", "Flag", "CamPort"] )
    #  ctypes.c_int Fg_sendSoftwareTrigger(ctypes.c_void_p Fg, ctypes.c_uint CamPort)
    addfunc(lib, "Fg_sendSoftwareTrigger", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint],
            argnames = ["Fg", "CamPort"] )
    #  ctypes.c_int Fg_sendSoftwareTriggerEx(ctypes.c_void_p Fg, ctypes.c_uint CamPort, ctypes.c_uint Triggers)
    addfunc(lib, "Fg_sendSoftwareTriggerEx", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint],
            argnames = ["Fg", "CamPort", "Triggers"] )
    #  ctypes.c_void_p Fg_AllocShading(ctypes.c_void_p Fg, ctypes.c_int set, ctypes.c_uint CamPort)
    addfunc(lib, "Fg_AllocShading", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint],
            argnames = ["Fg", "set", "CamPort"] )
    #  ctypes.c_int Fg_FreeShading(ctypes.c_void_p Fg, ctypes.c_void_p sh)
    addfunc(lib, "Fg_FreeShading", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["Fg", "sh"] )
    #  ctypes.c_int Shad_GetAccess(ctypes.c_void_p Fg, ctypes.c_void_p sh)
    addfunc(lib, "Shad_GetAccess", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["Fg", "sh"] )
    #  ctypes.c_int Shad_FreeAccess(ctypes.c_void_p Fg, ctypes.c_void_p sh)
    addfunc(lib, "Shad_FreeAccess", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["Fg", "sh"] )
    #  ctypes.c_int Shad_GetMaxLine(ctypes.c_void_p Fg, ctypes.c_void_p sh)
    addfunc(lib, "Shad_GetMaxLine", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["Fg", "sh"] )
    #  ctypes.c_int Shad_SetSubValueLine(ctypes.c_void_p Fg, ctypes.c_void_p sh, ctypes.c_int x, ctypes.c_int channel, ctypes.c_float sub)
    addfunc(lib, "Shad_SetSubValueLine", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_float],
            argnames = ["Fg", "sh", "x", "channel", "sub"] )
    #  ctypes.c_int Shad_SetMultValueLine(ctypes.c_void_p Fg, ctypes.c_void_p sh, ctypes.c_int x, ctypes.c_int channel, ctypes.c_float mult)
    addfunc(lib, "Shad_SetMultValueLine", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_float],
            argnames = ["Fg", "sh", "x", "channel", "mult"] )
    #  ctypes.c_int Shad_SetFixedPatternNoiseLine(ctypes.c_void_p Fg, ctypes.c_void_p sh, ctypes.c_int x, ctypes.c_int channel, ctypes.c_int on)
    addfunc(lib, "Shad_SetFixedPatternNoiseLine", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["Fg", "sh", "x", "channel", "on"] )
    #  ctypes.c_int Shad_WriteActLine(ctypes.c_void_p Fg, ctypes.c_void_p sh, ctypes.c_int Line)
    addfunc(lib, "Shad_WriteActLine", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["Fg", "sh", "Line"] )
    #  ctypes.c_int getLastErrorNumber()
    addfunc(lib, "getLastErrorNumber", restype = ctypes.c_int,
            argtypes = [],
            argnames = [] )


