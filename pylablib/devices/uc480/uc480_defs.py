##########   This file is generated automatically based on uc480.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class COLORMODE(enum.IntEnum):
    IS_COLORMODE_INVALID              = _int32(0)
    IS_COLORMODE_MONOCHROME           = _int32(1)
    IS_COLORMODE_BAYER                = _int32(2)
    IS_COLORMODE_CBYCRY               = _int32(4)
    IS_COLORMODE_JPEG                 = _int32(8)
    IS_GET_COLOR_MODE                 = _int32(0x8000)
    IS_CM_FORMAT_PLANAR               = _int32(0x2000)
    IS_CM_FORMAT_MASK                 = _int32(0x2000)
    IS_CM_ORDER_BGR                   = _int32(0x0000)
    IS_CM_ORDER_RGB                   = _int32(0x0080)
    IS_CM_ORDER_MASK                  = _int32(0x0080)
    IS_CM_PREFER_PACKED_SOURCE_FORMAT = _int32(0x4000)
    IS_CM_SENSOR_RAW8                 = _int32(11)
    IS_CM_SENSOR_RAW10                = _int32(33)
    IS_CM_SENSOR_RAW12                = _int32(27)
    IS_CM_SENSOR_RAW16                = _int32(29)
    IS_CM_MONO8                       = _int32(6)
    IS_CM_MONO10                      = _int32(34)
    IS_CM_MONO12                      = _int32(26)
    IS_CM_MONO16                      = _int32(28)
    IS_CM_BGR5_PACKED                 = _int32((3  | 0x0000))
    IS_CM_BGR565_PACKED               = _int32((2  | 0x0000))
    IS_CM_RGB8_PACKED                 = _int32((1  | 0x0080))
    IS_CM_BGR8_PACKED                 = _int32((1  | 0x0000))
    IS_CM_RGBA8_PACKED                = _int32((0  | 0x0080))
    IS_CM_BGRA8_PACKED                = _int32((0  | 0x0000))
    IS_CM_RGBY8_PACKED                = _int32((24 | 0x0080))
    IS_CM_BGRY8_PACKED                = _int32((24 | 0x0000))
    IS_CM_RGB10_PACKED                = _int32((25 | 0x0080))
    IS_CM_BGR10_PACKED                = _int32((25 | 0x0000))
    IS_CM_RGB10_UNPACKED              = _int32((35 | 0x0080))
    IS_CM_BGR10_UNPACKED              = _int32((35 | 0x0000))
    IS_CM_RGB12_UNPACKED              = _int32((30 | 0x0080))
    IS_CM_BGR12_UNPACKED              = _int32((30 | 0x0000))
    IS_CM_RGBA12_UNPACKED             = _int32((31 | 0x0080))
    IS_CM_BGRA12_UNPACKED             = _int32((31 | 0x0000))
    IS_CM_JPEG                        = _int32(32)
    IS_CM_UYVY_PACKED                 = _int32(12)
    IS_CM_UYVY_MONO_PACKED            = _int32(13)
    IS_CM_UYVY_BAYER_PACKED           = _int32(14)
    IS_CM_CBYCRY_PACKED               = _int32(23)
    IS_CM_RGB8_PLANAR                 = _int32((1 | 0x0080 | 0x2000))
    IS_CM_ALL_POSSIBLE                = _int32(0xFFFF)
    IS_CM_MODE_MASK                   = _int32(0x007F)
dCOLORMODE={a.name:a.value for a in COLORMODE}
drCOLORMODE={a.value:a.name for a in COLORMODE}


class SENSOR(enum.IntEnum):
    IS_SENSOR_INVALID           = _int32(0x0000)
    IS_SENSOR_C0640R13M         = _int32(0x0001)
    IS_SENSOR_C0640R13C         = _int32(0x0002)
    IS_SENSOR_C1280R23M         = _int32(0x0003)
    IS_SENSOR_C1280R23C         = _int32(0x0004)
    IS_SENSOR_C1280R12M         = _int32(0x0030)
    IS_SENSOR_C1280R12C         = _int32(0x0031)
    IS_SENSOR_C1600R12C         = _int32(0x0008)
    IS_SENSOR_C2048R12C         = _int32(0x000a)
    IS_SENSOR_C2592R12M         = _int32(0x000b)
    IS_SENSOR_C2592R12C         = _int32(0x000c)
    IS_SENSOR_C0640G12M         = _int32(0x0010)
    IS_SENSOR_C0640G12C         = _int32(0x0011)
    IS_SENSOR_C0752G13M         = _int32(0x0012)
    IS_SENSOR_C0752G13C         = _int32(0x0013)
    IS_SENSOR_C1282R13C         = _int32(0x0015)
    IS_SENSOR_C1601R13C         = _int32(0x0017)
    IS_SENSOR_C0753G13M         = _int32(0x0018)
    IS_SENSOR_C0753G13C         = _int32(0x0019)
    IS_SENSOR_C3840R12M         = _int32(0x003E)
    IS_SENSOR_C3840R12C         = _int32(0x003F)
    IS_SENSOR_C0754G13M         = _int32(0x0022)
    IS_SENSOR_C0754G13C         = _int32(0x0023)
    IS_SENSOR_C1284R13C         = _int32(0x0025)
    IS_SENSOR_C1604R13C         = _int32(0x0027)
    IS_SENSOR_C1285R12M         = _int32(0x0028)
    IS_SENSOR_C1285R12C         = _int32(0x0029)
    IS_SENSOR_C1605R12C         = _int32(0x002B)
    IS_SENSOR_C2055R12C         = _int32(0x002D)
    IS_SENSOR_C2595R12M         = _int32(0x002E)
    IS_SENSOR_C2595R12C         = _int32(0x002F)
    IS_SENSOR_C3845R12M         = _int32(0x0040)
    IS_SENSOR_C3845R12C         = _int32(0x0041)
    IS_SENSOR_C0768R12M         = _int32(0x004A)
    IS_SENSOR_C0768R12C         = _int32(0x004B)
    IS_SENSOR_C2592R14C         = _int32(0x020B)
    IS_SENSOR_C1280G12M         = _int32(0x0050)
    IS_SENSOR_C1280G12C         = _int32(0x0051)
    IS_SENSOR_C1280G12N         = _int32(0x0062)
    IS_SENSOR_C1283G12M         = _int32(0x0054)
    IS_SENSOR_C1283G12C         = _int32(0x0055)
    IS_SENSOR_C1283G12N         = _int32(0x0064)
    IS_SENSOR_C1284G12M         = _int32(0x0066)
    IS_SENSOR_C1284G12C         = _int32(0x0067)
    IS_SENSOR_C1284G12N         = _int32(0x0200)
    IS_SENSOR_C1283R12M         = _int32(0x0032)
    IS_SENSOR_C1283R12C         = _int32(0x0033)
    IS_SENSOR_C1286R12M         = _int32(0x003A)
    IS_SENSOR_C1286R12C         = _int32(0x003B)
    IS_SENSOR_C1283R12M_WO      = _int32(0x003C)
    IS_SENSOR_C1283R12C_WO      = _int32(0x003D)
    IS_SENSOR_C1603R12C         = _int32(0x0035)
    IS_SENSOR_C2053R12C         = _int32(0x0037)
    IS_SENSOR_C2593R12M         = _int32(0x0038)
    IS_SENSOR_C2593R12C         = _int32(0x0039)
    IS_SENSOR_C2057R12M_WO      = _int32(0x0044)
    IS_SENSOR_C2053R12C_WO      = _int32(0x0045)
    IS_SENSOR_C2593R12M_WO      = _int32(0x0048)
    IS_SENSOR_C2593R12C_WO      = _int32(0x0049)
    IS_SENSOR_C2048G23M         = _int32(0x0068)
    IS_SENSOR_C2048G23C         = _int32(0x0069)
    IS_SENSOR_C2048G23N         = _int32(0x0212)
    IS_SENSOR_C2048G11M         = _int32(0x006A)
    IS_SENSOR_C2048G11C         = _int32(0x006B)
    IS_SENSOR_C2048G11N         = _int32(0x0214)
    IS_SENSOR_C1600G12M         = _int32(0x006C)
    IS_SENSOR_C1600G12C         = _int32(0x006D)
    IS_SENSOR_C1600G12N         = _int32(0x006E)
    IS_SENSOR_C1603G12M         = _int32(0x0070)
    IS_SENSOR_C1603G12C         = _int32(0x0071)
    IS_SENSOR_C1603G12N         = _int32(0x0072)
    IS_SENSOR_C1604G12M         = _int32(0x0074)
    IS_SENSOR_C1604G12C         = _int32(0x0075)
    IS_SENSOR_C1604G12N         = _int32(0x0202)
    IS_SENSOR_C1920G11M         = _int32(0x021A)
    IS_SENSOR_C1920G11C         = _int32(0x021B)
    IS_SENSOR_C4216R12C         = _int32(0x021D)
    IS_SENSOR_C4912R12M         = _int32(0x0222)
    IS_SENSOR_C4912R12C         = _int32(0x0223)
    IS_SENSOR_C1936G11M         = _int32(0x0226)
    IS_SENSOR_C1936G11C         = _int32(0x0227)
    IS_SENSOR_C0800G13M         = _int32(0x022A)
    IS_SENSOR_C0800G13C         = _int32(0x022B)
    IS_SENSOR_C1920G23M         = _int32(0x022C)
    IS_SENSOR_C1920G23C         = _int32(0x022D)
    IS_SENSOR_C2592G10M         = _int32(0x022E)
    IS_SENSOR_C2592G10C         = _int32(0x022F)
    IS_SENSOR_D1024G13M         = _int32(0x0080)
    IS_SENSOR_D1024G13C         = _int32(0x0081)
    IS_SENSOR_D0640G13M         = _int32(0x0082)
    IS_SENSOR_D0640G13C         = _int32(0x0083)
    IS_SENSOR_D1281G12M         = _int32(0x0084)
    IS_SENSOR_D1281G12C         = _int32(0x0085)
    IS_SENSOR_D0640G12M         = _int32(0x0088)
    IS_SENSOR_D0640G12C         = _int32(0x0089)
    IS_SENSOR_D0640G14M         = _int32(0x0090)
    IS_SENSOR_D0640G14C         = _int32(0x0091)
    IS_SENSOR_D0768G12M         = _int32(0x0092)
    IS_SENSOR_D0768G12C         = _int32(0x0093)
    IS_SENSOR_D1280G12M         = _int32(0x0096)
    IS_SENSOR_D1280G12C         = _int32(0x0097)
    IS_SENSOR_D1600G12M         = _int32(0x0098)
    IS_SENSOR_D1600G12C         = _int32(0x0099)
    IS_SENSOR_D1280G13M         = _int32(0x009A)
    IS_SENSOR_D1280G13C         = _int32(0x009B)
    IS_SENSOR_D0640G13M_R2      = _int32(0x0182)
    IS_SENSOR_D0640G13C_R2      = _int32(0x0183)
    IS_SENSOR_PASSIVE_MULTICAST = _int32(0x0F00)
dSENSOR={a.name:a.value for a in SENSOR}
drSENSOR={a.value:a.name for a in SENSOR}


class ERROR(enum.IntEnum):
    IS_NO_SUCCESS                          = _int32(-1)
    IS_SUCCESS                             = _int32(0)
    IS_INVALID_CAMERA_HANDLE               = _int32(1)
    IS_INVALID_HANDLE                      = _int32(1)
    IS_IO_REQUEST_FAILED                   = _int32(2)
    IS_CANT_OPEN_DEVICE                    = _int32(3)
    IS_CANT_CLOSE_DEVICE                   = _int32(4)
    IS_CANT_SETUP_MEMORY                   = _int32(5)
    IS_NO_HWND_FOR_ERROR_REPORT            = _int32(6)
    IS_ERROR_MESSAGE_NOT_CREATED           = _int32(7)
    IS_ERROR_STRING_NOT_FOUND              = _int32(8)
    IS_HOOK_NOT_CREATED                    = _int32(9)
    IS_TIMER_NOT_CREATED                   = _int32(10)
    IS_CANT_OPEN_REGISTRY                  = _int32(11)
    IS_CANT_READ_REGISTRY                  = _int32(12)
    IS_CANT_VALIDATE_BOARD                 = _int32(13)
    IS_CANT_GIVE_BOARD_ACCESS              = _int32(14)
    IS_NO_IMAGE_MEM_ALLOCATED              = _int32(15)
    IS_CANT_CLEANUP_MEMORY                 = _int32(16)
    IS_CANT_COMMUNICATE_WITH_DRIVER        = _int32(17)
    IS_FUNCTION_NOT_SUPPORTED_YET          = _int32(18)
    IS_OPERATING_SYSTEM_NOT_SUPPORTED      = _int32(19)
    IS_INVALID_VIDEO_IN                    = _int32(20)
    IS_INVALID_IMG_SIZE                    = _int32(21)
    IS_INVALID_ADDRESS                     = _int32(22)
    IS_INVALID_VIDEO_MODE                  = _int32(23)
    IS_INVALID_AGC_MODE                    = _int32(24)
    IS_INVALID_GAMMA_MODE                  = _int32(25)
    IS_INVALID_SYNC_LEVEL                  = _int32(26)
    IS_INVALID_CBARS_MODE                  = _int32(27)
    IS_INVALID_COLOR_MODE                  = _int32(28)
    IS_INVALID_SCALE_FACTOR                = _int32(29)
    IS_INVALID_IMAGE_SIZE                  = _int32(30)
    IS_INVALID_IMAGE_POS                   = _int32(31)
    IS_INVALID_CAPTURE_MODE                = _int32(32)
    IS_INVALID_RISC_PROGRAM                = _int32(33)
    IS_INVALID_BRIGHTNESS                  = _int32(34)
    IS_INVALID_CONTRAST                    = _int32(35)
    IS_INVALID_SATURATION_U                = _int32(36)
    IS_INVALID_SATURATION_V                = _int32(37)
    IS_INVALID_HUE                         = _int32(38)
    IS_INVALID_HOR_FILTER_STEP             = _int32(39)
    IS_INVALID_VERT_FILTER_STEP            = _int32(40)
    IS_INVALID_EEPROM_READ_ADDRESS         = _int32(41)
    IS_INVALID_EEPROM_WRITE_ADDRESS        = _int32(42)
    IS_INVALID_EEPROM_READ_LENGTH          = _int32(43)
    IS_INVALID_EEPROM_WRITE_LENGTH         = _int32(44)
    IS_INVALID_BOARD_INFO_POINTER          = _int32(45)
    IS_INVALID_DISPLAY_MODE                = _int32(46)
    IS_INVALID_ERR_REP_MODE                = _int32(47)
    IS_INVALID_BITS_PIXEL                  = _int32(48)
    IS_INVALID_MEMORY_POINTER              = _int32(49)
    IS_FILE_WRITE_OPEN_ERROR               = _int32(50)
    IS_FILE_READ_OPEN_ERROR                = _int32(51)
    IS_FILE_READ_INVALID_BMP_ID            = _int32(52)
    IS_FILE_READ_INVALID_BMP_SIZE          = _int32(53)
    IS_FILE_READ_INVALID_BIT_COUNT         = _int32(54)
    IS_WRONG_KERNEL_VERSION                = _int32(55)
    IS_RISC_INVALID_XLENGTH                = _int32(60)
    IS_RISC_INVALID_YLENGTH                = _int32(61)
    IS_RISC_EXCEED_IMG_SIZE                = _int32(62)
    IS_DD_MAIN_FAILED                      = _int32(70)
    IS_DD_PRIMSURFACE_FAILED               = _int32(71)
    IS_DD_SCRN_SIZE_NOT_SUPPORTED          = _int32(72)
    IS_DD_CLIPPER_FAILED                   = _int32(73)
    IS_DD_CLIPPER_HWND_FAILED              = _int32(74)
    IS_DD_CLIPPER_CONNECT_FAILED           = _int32(75)
    IS_DD_BACKSURFACE_FAILED               = _int32(76)
    IS_DD_BACKSURFACE_IN_SYSMEM            = _int32(77)
    IS_DD_MDL_MALLOC_ERR                   = _int32(78)
    IS_DD_MDL_SIZE_ERR                     = _int32(79)
    IS_DD_CLIP_NO_CHANGE                   = _int32(80)
    IS_DD_PRIMMEM_NULL                     = _int32(81)
    IS_DD_BACKMEM_NULL                     = _int32(82)
    IS_DD_BACKOVLMEM_NULL                  = _int32(83)
    IS_DD_OVERLAYSURFACE_FAILED            = _int32(84)
    IS_DD_OVERLAYSURFACE_IN_SYSMEM         = _int32(85)
    IS_DD_OVERLAY_NOT_ALLOWED              = _int32(86)
    IS_DD_OVERLAY_COLKEY_ERR               = _int32(87)
    IS_DD_OVERLAY_NOT_ENABLED              = _int32(88)
    IS_DD_GET_DC_ERROR                     = _int32(89)
    IS_DD_DDRAW_DLL_NOT_LOADED             = _int32(90)
    IS_DD_THREAD_NOT_CREATED               = _int32(91)
    IS_DD_CANT_GET_CAPS                    = _int32(92)
    IS_DD_NO_OVERLAYSURFACE                = _int32(93)
    IS_DD_NO_OVERLAYSTRETCH                = _int32(94)
    IS_DD_CANT_CREATE_OVERLAYSURFACE       = _int32(95)
    IS_DD_CANT_UPDATE_OVERLAYSURFACE       = _int32(96)
    IS_DD_INVALID_STRETCH                  = _int32(97)
    IS_EV_INVALID_EVENT_NUMBER             = _int32(100)
    IS_INVALID_MODE                        = _int32(101)
    IS_CANT_FIND_FALCHOOK                  = _int32(102)
    IS_CANT_FIND_HOOK                      = _int32(102)
    IS_CANT_GET_HOOK_PROC_ADDR             = _int32(103)
    IS_CANT_CHAIN_HOOK_PROC                = _int32(104)
    IS_CANT_SETUP_WND_PROC                 = _int32(105)
    IS_HWND_NULL                           = _int32(106)
    IS_INVALID_UPDATE_MODE                 = _int32(107)
    IS_NO_ACTIVE_IMG_MEM                   = _int32(108)
    IS_CANT_INIT_EVENT                     = _int32(109)
    IS_FUNC_NOT_AVAIL_IN_OS                = _int32(110)
    IS_CAMERA_NOT_CONNECTED                = _int32(111)
    IS_SEQUENCE_LIST_EMPTY                 = _int32(112)
    IS_CANT_ADD_TO_SEQUENCE                = _int32(113)
    IS_LOW_OF_SEQUENCE_RISC_MEM            = _int32(114)
    IS_IMGMEM2FREE_USED_IN_SEQ             = _int32(115)
    IS_IMGMEM_NOT_IN_SEQUENCE_LIST         = _int32(116)
    IS_SEQUENCE_BUF_ALREADY_LOCKED         = _int32(117)
    IS_INVALID_DEVICE_ID                   = _int32(118)
    IS_INVALID_BOARD_ID                    = _int32(119)
    IS_ALL_DEVICES_BUSY                    = _int32(120)
    IS_HOOK_BUSY                           = _int32(121)
    IS_TIMED_OUT                           = _int32(122)
    IS_NULL_POINTER                        = _int32(123)
    IS_WRONG_HOOK_VERSION                  = _int32(124)
    IS_INVALID_PARAMETER                   = _int32(125)
    IS_NOT_ALLOWED                         = _int32(126)
    IS_OUT_OF_MEMORY                       = _int32(127)
    IS_INVALID_WHILE_LIVE                  = _int32(128)
    IS_ACCESS_VIOLATION                    = _int32(129)
    IS_UNKNOWN_ROP_EFFECT                  = _int32(130)
    IS_INVALID_RENDER_MODE                 = _int32(131)
    IS_INVALID_THREAD_CONTEXT              = _int32(132)
    IS_NO_HARDWARE_INSTALLED               = _int32(133)
    IS_INVALID_WATCHDOG_TIME               = _int32(134)
    IS_INVALID_WATCHDOG_MODE               = _int32(135)
    IS_INVALID_PASSTHROUGH_IN              = _int32(136)
    IS_ERROR_SETTING_PASSTHROUGH_IN        = _int32(137)
    IS_FAILURE_ON_SETTING_WATCHDOG         = _int32(138)
    IS_NO_USB20                            = _int32(139)
    IS_CAPTURE_RUNNING                     = _int32(140)
    IS_MEMORY_BOARD_ACTIVATED              = _int32(141)
    IS_MEMORY_BOARD_DEACTIVATED            = _int32(142)
    IS_NO_MEMORY_BOARD_CONNECTED           = _int32(143)
    IS_TOO_LESS_MEMORY                     = _int32(144)
    IS_IMAGE_NOT_PRESENT                   = _int32(145)
    IS_MEMORY_MODE_RUNNING                 = _int32(146)
    IS_MEMORYBOARD_DISABLED                = _int32(147)
    IS_TRIGGER_ACTIVATED                   = _int32(148)
    IS_WRONG_KEY                           = _int32(150)
    IS_CRC_ERROR                           = _int32(151)
    IS_NOT_YET_RELEASED                    = _int32(152)
    IS_NOT_CALIBRATED                      = _int32(153)
    IS_WAITING_FOR_KERNEL                  = _int32(154)
    IS_NOT_SUPPORTED                       = _int32(155)
    IS_TRIGGER_NOT_ACTIVATED               = _int32(156)
    IS_OPERATION_ABORTED                   = _int32(157)
    IS_BAD_STRUCTURE_SIZE                  = _int32(158)
    IS_INVALID_BUFFER_SIZE                 = _int32(159)
    IS_INVALID_PIXEL_CLOCK                 = _int32(160)
    IS_INVALID_EXPOSURE_TIME               = _int32(161)
    IS_AUTO_EXPOSURE_RUNNING               = _int32(162)
    IS_CANNOT_CREATE_BB_SURF               = _int32(163)
    IS_CANNOT_CREATE_BB_MIX                = _int32(164)
    IS_BB_OVLMEM_NULL                      = _int32(165)
    IS_CANNOT_CREATE_BB_OVL                = _int32(166)
    IS_NOT_SUPP_IN_OVL_SURF_MODE           = _int32(167)
    IS_INVALID_SURFACE                     = _int32(168)
    IS_SURFACE_LOST                        = _int32(169)
    IS_RELEASE_BB_OVL_DC                   = _int32(170)
    IS_BB_TIMER_NOT_CREATED                = _int32(171)
    IS_BB_OVL_NOT_EN                       = _int32(172)
    IS_ONLY_IN_BB_MODE                     = _int32(173)
    IS_INVALID_COLOR_FORMAT                = _int32(174)
    IS_INVALID_WB_BINNING_MODE             = _int32(175)
    IS_INVALID_I2C_DEVICE_ADDRESS          = _int32(176)
    IS_COULD_NOT_CONVERT                   = _int32(177)
    IS_TRANSFER_ERROR                      = _int32(178)
    IS_PARAMETER_SET_NOT_PRESENT           = _int32(179)
    IS_INVALID_CAMERA_TYPE                 = _int32(180)
    IS_INVALID_HOST_IP_HIBYTE              = _int32(181)
    IS_CM_NOT_SUPP_IN_CURR_DISPLAYMODE     = _int32(182)
    IS_NO_IR_FILTER                        = _int32(183)
    IS_STARTER_FW_UPLOAD_NEEDED            = _int32(184)
    IS_DR_LIBRARY_NOT_FOUND                = _int32(185)
    IS_DR_DEVICE_OUT_OF_MEMORY             = _int32(186)
    IS_DR_CANNOT_CREATE_SURFACE            = _int32(187)
    IS_DR_CANNOT_CREATE_VERTEX_BUFFER      = _int32(188)
    IS_DR_CANNOT_CREATE_TEXTURE            = _int32(189)
    IS_DR_CANNOT_LOCK_OVERLAY_SURFACE      = _int32(190)
    IS_DR_CANNOT_UNLOCK_OVERLAY_SURFACE    = _int32(191)
    IS_DR_CANNOT_GET_OVERLAY_DC            = _int32(192)
    IS_DR_CANNOT_RELEASE_OVERLAY_DC        = _int32(193)
    IS_DR_DEVICE_CAPS_INSUFFICIENT         = _int32(194)
    IS_INCOMPATIBLE_SETTING                = _int32(195)
    IS_DR_NOT_ALLOWED_WHILE_DC_IS_ACTIVE   = _int32(196)
    IS_DEVICE_ALREADY_PAIRED               = _int32(197)
    IS_SUBNETMASK_MISMATCH                 = _int32(198)
    IS_SUBNET_MISMATCH                     = _int32(199)
    IS_INVALID_IP_CONFIGURATION            = _int32(200)
    IS_DEVICE_NOT_COMPATIBLE               = _int32(201)
    IS_NETWORK_FRAME_SIZE_INCOMPATIBLE     = _int32(202)
    IS_NETWORK_CONFIGURATION_INVALID       = _int32(203)
    IS_ERROR_CPU_IDLE_STATES_CONFIGURATION = _int32(204)
    IS_DEVICE_BUSY                         = _int32(205)
    IS_SENSOR_INITIALIZATION_FAILED        = _int32(206)
dERROR={a.name:a.value for a in ERROR}
drERROR={a.value:a.name for a in ERROR}


### CONST ###
IS_OFF                                = _int32(0)
IS_ON                                 = _int32(1)
IS_IGNORE_PARAMETER                   = _int32(-1)
IS_MIN_GAIN                           = _int32(0)
IS_MAX_GAIN                           = _int32(100)
IS_MIN_BL_OFFSET                      = _int32(0)
IS_MAX_BL_OFFSET                      = _int32(255)
IS_MIN_AUTO_BRIGHT_REFERENCE          = _int32(0)
IS_MAX_AUTO_BRIGHT_REFERENCE          = _int32(255)
IS_DEFAULT_AUTO_BRIGHT_REFERENCE      = _int32(128)
IS_MIN_AUTO_SPEED                     = _int32(0)
IS_MAX_AUTO_SPEED                     = _int32(100)
IS_DEFAULT_AUTO_SPEED                 = _int32(50)
IS_DEFAULT_AUTO_WB_OFFSET             = _int32(0)
IS_MIN_AUTO_WB_OFFSET                 = _int32(-50)
IS_MAX_AUTO_WB_OFFSET                 = _int32(50)
IS_DEFAULT_AUTO_WB_SPEED              = _int32(50)
IS_MIN_AUTO_WB_SPEED                  = _int32(0)
IS_MAX_AUTO_WB_SPEED                  = _int32(100)
IS_MIN_AUTO_WB_REFERENCE              = _int32(0)
IS_MAX_AUTO_WB_REFERENCE              = _int32(255)
IS_SAVE_USE_ACTUAL_IMAGE_SIZE         = _int32(0x00010000)
IS_TRIGGER_TIMEOUT                    = _int32(0)
IS_BEST_PCLK_RUN_ONCE                 = _int32(0)
IS_GET_D3D_MEM                        = _int32(0x8000)
IS_BOOTBOOST_ID_MIN                   = _int32(1)
IS_BOOTBOOST_ID_MAX                   = _int32(254)
IS_BOOTBOOST_ID_NONE                  = _int32(0)
IS_BOOTBOOST_ID_ALL                   = _int32(255)
IS_BOOTBOOST_DEFAULT_WAIT_TIMEOUT_SEC = _int32(60)
IS_GAMMA_VALUE_MIN                    = _int32(1)
IS_GAMMA_VALUE_MAX                    = _int32(1000)


class DEVENUM(enum.IntEnum):
    IS_USE_DEVICE_ID           = _int32(0x8000)
    IS_ALLOW_STARTER_FW_UPLOAD = _int32(0x10000)
dDEVENUM={a.name:a.value for a in DEVENUM}
drDEVENUM={a.value:a.name for a in DEVENUM}


class AUTOEXIT(enum.IntEnum):
    IS_GET_AUTO_EXIT_ENABLED = _int32(0x8000)
    IS_DISABLE_AUTO_EXIT     = _int32(0)
    IS_ENABLE_AUTO_EXIT      = _int32(1)
dAUTOEXIT={a.name:a.value for a in AUTOEXIT}
drAUTOEXIT={a.value:a.name for a in AUTOEXIT}


class LIVEFREEZE(enum.IntEnum):
    IS_GET_LIVE          = _int32(0x8000)
    IS_WAIT              = _int32(0x0001)
    IS_DONT_WAIT         = _int32(0x0000)
    IS_FORCE_VIDEO_STOP  = _int32(0x4000)
    IS_FORCE_VIDEO_START = _int32(0x4000)
    IS_USE_NEXT_MEM      = _int32(0x8000)
dLIVEFREEZE={a.name:a.value for a in LIVEFREEZE}
drLIVEFREEZE={a.value:a.name for a in LIVEFREEZE}


class VIDEOFINISH(enum.IntEnum):
    IS_VIDEO_NOT_FINISH = _int32(0)
    IS_VIDEO_FINISH     = _int32(1)
dVIDEOFINISH={a.name:a.value for a in VIDEOFINISH}
drVIDEOFINISH={a.value:a.name for a in VIDEOFINISH}


class RENDER(enum.IntEnum):
    IS_GET_RENDER_MODE           = _int32(0x8000)
    IS_RENDER_DISABLED           = _int32(0x0000)
    IS_RENDER_NORMAL             = _int32(0x0001)
    IS_RENDER_FIT_TO_WINDOW      = _int32(0x0002)
    IS_RENDER_DOWNSCALE_1_2      = _int32(0x0004)
    IS_RENDER_MIRROR_UPDOWN      = _int32(0x0010)
    IS_RENDER_PLANAR_COLOR_RED   = _int32(0x0080)
    IS_RENDER_PLANAR_COLOR_GREEN = _int32(0x0100)
    IS_RENDER_PLANAR_COLOR_BLUE  = _int32(0x0200)
    IS_RENDER_PLANAR_MONO_RED    = _int32(0x0400)
    IS_RENDER_PLANAR_MONO_GREEN  = _int32(0x0800)
    IS_RENDER_PLANAR_MONO_BLUE   = _int32(0x1000)
    IS_RENDER_ROTATE_90          = _int32(0x0020)
    IS_RENDER_ROTATE_180         = _int32(0x0040)
    IS_RENDER_ROTATE_270         = _int32(0x2000)
    IS_USE_AS_DC_STRUCTURE       = _int32(0x4000)
    IS_USE_AS_DC_HANDLE          = _int32(0x8000)
dRENDER={a.name:a.value for a in RENDER}
drRENDER={a.value:a.name for a in RENDER}


class TRIGGER(enum.IntEnum):
    IS_GET_EXTERNALTRIGGER           = _int32(0x8000)
    IS_GET_TRIGGER_STATUS            = _int32(0x8001)
    IS_GET_TRIGGER_MASK              = _int32(0x8002)
    IS_GET_TRIGGER_INPUTS            = _int32(0x8003)
    IS_GET_SUPPORTED_TRIGGER_MODE    = _int32(0x8004)
    IS_GET_TRIGGER_COUNTER           = _int32(0x8000)
    IS_SET_TRIGGER_MASK              = _int32(0x0100)
    IS_SET_TRIGGER_CONTINUOUS        = _int32(0x1000)
    IS_SET_TRIGGER_OFF               = _int32(0x0000)
    IS_SET_TRIGGER_HI_LO             = _int32((0x1000 | 0x0001))
    IS_SET_TRIGGER_LO_HI             = _int32((0x1000 | 0x0002))
    IS_SET_TRIGGER_SOFTWARE          = _int32((0x1000 | 0x0008))
    IS_SET_TRIGGER_HI_LO_SYNC        = _int32(0x0010)
    IS_SET_TRIGGER_LO_HI_SYNC        = _int32(0x0020)
    IS_SET_TRIGGER_PRE_HI_LO         = _int32((0x1000 | 0x0040))
    IS_SET_TRIGGER_PRE_LO_HI         = _int32((0x1000 | 0x0080))
    IS_GET_TRIGGER_DELAY             = _int32(0x8000)
    IS_GET_MIN_TRIGGER_DELAY         = _int32(0x8001)
    IS_GET_MAX_TRIGGER_DELAY         = _int32(0x8002)
    IS_GET_TRIGGER_DELAY_GRANULARITY = _int32(0x8003)
dTRIGGER={a.name:a.value for a in TRIGGER}
drTRIGGER={a.value:a.name for a in TRIGGER}


class PIXELCLOCK(enum.IntEnum):
    IS_GET_PIXEL_CLOCK       = _int32(0x8000)
    IS_GET_DEFAULT_PIXEL_CLK = _int32(0x8001)
    IS_GET_PIXEL_CLOCK_INC   = _int32(0x8005)
dPIXELCLOCK={a.name:a.value for a in PIXELCLOCK}
drPIXELCLOCK={a.value:a.name for a in PIXELCLOCK}


class FRAMERATE(enum.IntEnum):
    IS_GET_FRAMERATE         = _int32(0x8000)
    IS_GET_DEFAULT_FRAMERATE = _int32(0x8001)
dFRAMERATE={a.name:a.value for a in FRAMERATE}
drFRAMERATE={a.value:a.name for a in FRAMERATE}


class GAIN(enum.IntEnum):
    IS_GET_MASTER_GAIN         = _int32(0x8000)
    IS_GET_RED_GAIN            = _int32(0x8001)
    IS_GET_GREEN_GAIN          = _int32(0x8002)
    IS_GET_BLUE_GAIN           = _int32(0x8003)
    IS_GET_DEFAULT_MASTER      = _int32(0x8004)
    IS_GET_DEFAULT_RED         = _int32(0x8005)
    IS_GET_DEFAULT_GREEN       = _int32(0x8006)
    IS_GET_DEFAULT_BLUE        = _int32(0x8007)
    IS_GET_GAINBOOST           = _int32(0x8008)
    IS_SET_GAINBOOST_ON        = _int32(0x0001)
    IS_SET_GAINBOOST_OFF       = _int32(0x0000)
    IS_GET_SUPPORTED_GAINBOOST = _int32(0x0002)
dGAIN={a.name:a.value for a in GAIN}
drGAIN={a.value:a.name for a in GAIN}


class GAINFACTOR(enum.IntEnum):
    IS_GET_MASTER_GAIN_FACTOR         = _int32(0x8000)
    IS_GET_RED_GAIN_FACTOR            = _int32(0x8001)
    IS_GET_GREEN_GAIN_FACTOR          = _int32(0x8002)
    IS_GET_BLUE_GAIN_FACTOR           = _int32(0x8003)
    IS_SET_MASTER_GAIN_FACTOR         = _int32(0x8004)
    IS_SET_RED_GAIN_FACTOR            = _int32(0x8005)
    IS_SET_GREEN_GAIN_FACTOR          = _int32(0x8006)
    IS_SET_BLUE_GAIN_FACTOR           = _int32(0x8007)
    IS_GET_DEFAULT_MASTER_GAIN_FACTOR = _int32(0x8008)
    IS_GET_DEFAULT_RED_GAIN_FACTOR    = _int32(0x8009)
    IS_GET_DEFAULT_GREEN_GAIN_FACTOR  = _int32(0x800a)
    IS_GET_DEFAULT_BLUE_GAIN_FACTOR   = _int32(0x800b)
    IS_INQUIRE_MASTER_GAIN_FACTOR     = _int32(0x800c)
    IS_INQUIRE_RED_GAIN_FACTOR        = _int32(0x800d)
    IS_INQUIRE_GREEN_GAIN_FACTOR      = _int32(0x800e)
    IS_INQUIRE_BLUE_GAIN_FACTOR       = _int32(0x800f)
dGAINFACTOR={a.name:a.value for a in GAINFACTOR}
drGAINFACTOR={a.value:a.name for a in GAINFACTOR}


class GLOBALSHUTTER(enum.IntEnum):
    IS_SET_GLOBAL_SHUTTER_ON        = _int32(0x0001)
    IS_SET_GLOBAL_SHUTTER_OFF       = _int32(0x0000)
    IS_GET_GLOBAL_SHUTTER           = _int32(0x0010)
    IS_GET_SUPPORTED_GLOBAL_SHUTTER = _int32(0x0020)
dGLOBALSHUTTER={a.name:a.value for a in GLOBALSHUTTER}
drGLOBALSHUTTER={a.value:a.name for a in GLOBALSHUTTER}


class BLACKLEVEL(enum.IntEnum):
    IS_GET_BL_COMPENSATION     = _int32(0x8000)
    IS_GET_BL_OFFSET           = _int32(0x8001)
    IS_GET_BL_DEFAULT_MODE     = _int32(0x8002)
    IS_GET_BL_DEFAULT_OFFSET   = _int32(0x8003)
    IS_GET_BL_SUPPORTED_MODE   = _int32(0x8004)
    IS_BL_COMPENSATION_DISABLE = _int32(0)
    IS_BL_COMPENSATION_ENABLE  = _int32(1)
    IS_BL_COMPENSATION_OFFSET  = _int32(32)
dBLACKLEVEL={a.name:a.value for a in BLACKLEVEL}
drBLACKLEVEL={a.value:a.name for a in BLACKLEVEL}


class HWGAMMA(enum.IntEnum):
    IS_GET_HW_GAMMA           = _int32(0x8000)
    IS_GET_HW_SUPPORTED_GAMMA = _int32(0x8001)
    IS_SET_HW_GAMMA_OFF       = _int32(0x0000)
    IS_SET_HW_GAMMA_ON        = _int32(0x0001)
dHWGAMMA={a.name:a.value for a in HWGAMMA}
drHWGAMMA={a.value:a.name for a in HWGAMMA}


class SATURATION(enum.IntEnum):
    IS_GET_SATURATION_U     = _int32(0x8000)
    IS_MIN_SATURATION_U     = _int32(0)
    IS_MAX_SATURATION_U     = _int32(200)
    IS_DEFAULT_SATURATION_U = _int32(100)
    IS_GET_SATURATION_V     = _int32(0x8001)
    IS_MIN_SATURATION_V     = _int32(0)
    IS_MAX_SATURATION_V     = _int32(200)
    IS_DEFAULT_SATURATION_V = _int32(100)
dSATURATION={a.name:a.value for a in SATURATION}
drSATURATION={a.value:a.name for a in SATURATION}


class IMAGE(enum.IntEnum):
    IS_AOI_IMAGE_SET_AOI                = _int32(0x0001)
    IS_AOI_IMAGE_GET_AOI                = _int32(0x0002)
    IS_AOI_IMAGE_SET_POS                = _int32(0x0003)
    IS_AOI_IMAGE_GET_POS                = _int32(0x0004)
    IS_AOI_IMAGE_SET_SIZE               = _int32(0x0005)
    IS_AOI_IMAGE_GET_SIZE               = _int32(0x0006)
    IS_AOI_IMAGE_GET_POS_MIN            = _int32(0x0007)
    IS_AOI_IMAGE_GET_SIZE_MIN           = _int32(0x0008)
    IS_AOI_IMAGE_GET_POS_MAX            = _int32(0x0009)
    IS_AOI_IMAGE_GET_SIZE_MAX           = _int32(0x0010)
    IS_AOI_IMAGE_GET_POS_INC            = _int32(0x0011)
    IS_AOI_IMAGE_GET_SIZE_INC           = _int32(0x0012)
    IS_AOI_IMAGE_GET_POS_X_ABS          = _int32(0x0013)
    IS_AOI_IMAGE_GET_POS_Y_ABS          = _int32(0x0014)
    IS_AOI_IMAGE_GET_ORIGINAL_AOI       = _int32(0x0015)
    IS_AOI_IMAGE_POS_ABSOLUTE           = _int32(0x10000000)
    IS_AOI_IMAGE_SET_POS_FAST           = _int32(0x0020)
    IS_AOI_IMAGE_GET_POS_FAST_SUPPORTED = _int32(0x0021)
    IS_AOI_AUTO_BRIGHTNESS_SET_AOI      = _int32(0x0030)
    IS_AOI_AUTO_BRIGHTNESS_GET_AOI      = _int32(0x0031)
    IS_AOI_AUTO_WHITEBALANCE_SET_AOI    = _int32(0x0032)
    IS_AOI_AUTO_WHITEBALANCE_GET_AOI    = _int32(0x0033)
    IS_AOI_MULTI_GET_SUPPORTED_MODES    = _int32(0x0100)
    IS_AOI_MULTI_SET_AOI                = _int32(0x0200)
    IS_AOI_MULTI_GET_AOI                = _int32(0x0400)
    IS_AOI_MULTI_DISABLE_AOI            = _int32(0x0800)
    IS_AOI_MULTI_MODE_X_Y_AXES          = _int32(0x0001)
    IS_AOI_MULTI_MODE_Y_AXES            = _int32(0x0002)
    IS_AOI_MULTI_MODE_GET_MAX_NUMBER    = _int32(0x0003)
    IS_AOI_MULTI_MODE_GET_DEFAULT       = _int32(0x0004)
    IS_AOI_MULTI_MODE_ONLY_VERIFY_AOIS  = _int32(0x0005)
    IS_AOI_MULTI_MODE_GET_MINIMUM_SIZE  = _int32(0x0006)
    IS_AOI_MULTI_MODE_GET_ENABLED       = _int32(0x0007)
    IS_AOI_MULTI_STATUS_SETBYUSER       = _int32(0x00000001)
    IS_AOI_MULTI_STATUS_COMPLEMENT      = _int32(0x00000002)
    IS_AOI_MULTI_STATUS_VALID           = _int32(0x00000004)
    IS_AOI_MULTI_STATUS_CONFLICT        = _int32(0x00000008)
    IS_AOI_MULTI_STATUS_ERROR           = _int32(0x00000010)
    IS_AOI_MULTI_STATUS_UNUSED          = _int32(0x00000020)
    IS_AOI_SEQUENCE_GET_SUPPORTED       = _int32(0x0050)
    IS_AOI_SEQUENCE_SET_PARAMS          = _int32(0x0051)
    IS_AOI_SEQUENCE_GET_PARAMS          = _int32(0x0052)
    IS_AOI_SEQUENCE_SET_ENABLE          = _int32(0x0053)
    IS_AOI_SEQUENCE_GET_ENABLE          = _int32(0x0054)
    IS_AOI_SEQUENCE_INDEX_AOI_1         = _int32(0)
    IS_AOI_SEQUENCE_INDEX_AOI_2         = _int32(1)
    IS_AOI_SEQUENCE_INDEX_AOI_3         = _int32(2)
    IS_AOI_SEQUENCE_INDEX_AOI_4         = _int32(4)
dIMAGE={a.name:a.value for a in IMAGE}
drIMAGE={a.value:a.name for a in IMAGE}


class ROP(enum.IntEnum):
    IS_GET_ROP_EFFECT             = _int32(0x8000)
    IS_GET_SUPPORTED_ROP_EFFECT   = _int32(0x8001)
    IS_SET_ROP_NONE               = _int32(0)
    IS_SET_ROP_MIRROR_UPDOWN      = _int32(8)
    IS_SET_ROP_MIRROR_UPDOWN_ODD  = _int32(16)
    IS_SET_ROP_MIRROR_UPDOWN_EVEN = _int32(32)
    IS_SET_ROP_MIRROR_LEFTRIGHT   = _int32(64)
dROP={a.name:a.value for a in ROP}
drROP={a.value:a.name for a in ROP}


class SUBSAMPLING(enum.IntEnum):
    IS_GET_SUBSAMPLING                   = _int32(0x8000)
    IS_GET_SUPPORTED_SUBSAMPLING         = _int32(0x8001)
    IS_GET_SUBSAMPLING_TYPE              = _int32(0x8002)
    IS_GET_SUBSAMPLING_FACTOR_HORIZONTAL = _int32(0x8004)
    IS_GET_SUBSAMPLING_FACTOR_VERTICAL   = _int32(0x8008)
    IS_SUBSAMPLING_DISABLE               = _int32(0x00)
    IS_SUBSAMPLING_2X_VERTICAL           = _int32(0x0001)
    IS_SUBSAMPLING_2X_HORIZONTAL         = _int32(0x0002)
    IS_SUBSAMPLING_4X_VERTICAL           = _int32(0x0004)
    IS_SUBSAMPLING_4X_HORIZONTAL         = _int32(0x0008)
    IS_SUBSAMPLING_3X_VERTICAL           = _int32(0x0010)
    IS_SUBSAMPLING_3X_HORIZONTAL         = _int32(0x0020)
    IS_SUBSAMPLING_5X_VERTICAL           = _int32(0x0040)
    IS_SUBSAMPLING_5X_HORIZONTAL         = _int32(0x0080)
    IS_SUBSAMPLING_6X_VERTICAL           = _int32(0x0100)
    IS_SUBSAMPLING_6X_HORIZONTAL         = _int32(0x0200)
    IS_SUBSAMPLING_8X_VERTICAL           = _int32(0x0400)
    IS_SUBSAMPLING_8X_HORIZONTAL         = _int32(0x0800)
    IS_SUBSAMPLING_16X_VERTICAL          = _int32(0x1000)
    IS_SUBSAMPLING_16X_HORIZONTAL        = _int32(0x2000)
    IS_SUBSAMPLING_COLOR                 = _int32(0x01)
    IS_SUBSAMPLING_MONO                  = _int32(0x02)
    IS_SUBSAMPLING_MASK_VERTICAL         = _int32((0x0001 | 0x0004 | 0x0010 | 0x0040 | 0x0100 | 0x0400 | 0x1000))
    IS_SUBSAMPLING_MASK_HORIZONTAL       = _int32((0x0002 | 0x0008 | 0x0020 | 0x0080 | 0x0200 | 0x0800 | 0x2000))
dSUBSAMPLING={a.name:a.value for a in SUBSAMPLING}
drSUBSAMPLING={a.value:a.name for a in SUBSAMPLING}


class BINNING(enum.IntEnum):
    IS_GET_BINNING                   = _int32(0x8000)
    IS_GET_SUPPORTED_BINNING         = _int32(0x8001)
    IS_GET_BINNING_TYPE              = _int32(0x8002)
    IS_GET_BINNING_FACTOR_HORIZONTAL = _int32(0x8004)
    IS_GET_BINNING_FACTOR_VERTICAL   = _int32(0x8008)
    IS_BINNING_DISABLE               = _int32(0x00)
    IS_BINNING_2X_VERTICAL           = _int32(0x0001)
    IS_BINNING_2X_HORIZONTAL         = _int32(0x0002)
    IS_BINNING_4X_VERTICAL           = _int32(0x0004)
    IS_BINNING_4X_HORIZONTAL         = _int32(0x0008)
    IS_BINNING_3X_VERTICAL           = _int32(0x0010)
    IS_BINNING_3X_HORIZONTAL         = _int32(0x0020)
    IS_BINNING_5X_VERTICAL           = _int32(0x0040)
    IS_BINNING_5X_HORIZONTAL         = _int32(0x0080)
    IS_BINNING_6X_VERTICAL           = _int32(0x0100)
    IS_BINNING_6X_HORIZONTAL         = _int32(0x0200)
    IS_BINNING_8X_VERTICAL           = _int32(0x0400)
    IS_BINNING_8X_HORIZONTAL         = _int32(0x0800)
    IS_BINNING_16X_VERTICAL          = _int32(0x1000)
    IS_BINNING_16X_HORIZONTAL        = _int32(0x2000)
    IS_BINNING_COLOR                 = _int32(0x01)
    IS_BINNING_MONO                  = _int32(0x02)
    IS_BINNING_MASK_VERTICAL         = _int32((0x0001 | 0x0010 | 0x0004 | 0x0040 | 0x0100 | 0x0400 | 0x1000))
    IS_BINNING_MASK_HORIZONTAL       = _int32((0x0002 | 0x0020 | 0x0008 | 0x0080 | 0x0200 | 0x0800 | 0x2000))
dBINNING={a.name:a.value for a in BINNING}
drBINNING={a.value:a.name for a in BINNING}


class AUTOCONTROL(enum.IntEnum):
    IS_SET_ENABLE_AUTO_GAIN                    = _int32(0x8800)
    IS_GET_ENABLE_AUTO_GAIN                    = _int32(0x8801)
    IS_SET_ENABLE_AUTO_SHUTTER                 = _int32(0x8802)
    IS_GET_ENABLE_AUTO_SHUTTER                 = _int32(0x8803)
    IS_SET_ENABLE_AUTO_WHITEBALANCE            = _int32(0x8804)
    IS_GET_ENABLE_AUTO_WHITEBALANCE            = _int32(0x8805)
    IS_SET_ENABLE_AUTO_FRAMERATE               = _int32(0x8806)
    IS_GET_ENABLE_AUTO_FRAMERATE               = _int32(0x8807)
    IS_SET_ENABLE_AUTO_SENSOR_GAIN             = _int32(0x8808)
    IS_GET_ENABLE_AUTO_SENSOR_GAIN             = _int32(0x8809)
    IS_SET_ENABLE_AUTO_SENSOR_SHUTTER          = _int32(0x8810)
    IS_GET_ENABLE_AUTO_SENSOR_SHUTTER          = _int32(0x8811)
    IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER     = _int32(0x8812)
    IS_GET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER     = _int32(0x8813)
    IS_SET_ENABLE_AUTO_SENSOR_FRAMERATE        = _int32(0x8814)
    IS_GET_ENABLE_AUTO_SENSOR_FRAMERATE        = _int32(0x8815)
    IS_SET_ENABLE_AUTO_SENSOR_WHITEBALANCE     = _int32(0x8816)
    IS_GET_ENABLE_AUTO_SENSOR_WHITEBALANCE     = _int32(0x8817)
    IS_SET_AUTO_REFERENCE                      = _int32(0x8000)
    IS_GET_AUTO_REFERENCE                      = _int32(0x8001)
    IS_SET_AUTO_GAIN_MAX                       = _int32(0x8002)
    IS_GET_AUTO_GAIN_MAX                       = _int32(0x8003)
    IS_SET_AUTO_SHUTTER_MAX                    = _int32(0x8004)
    IS_GET_AUTO_SHUTTER_MAX                    = _int32(0x8005)
    IS_SET_AUTO_SPEED                          = _int32(0x8006)
    IS_GET_AUTO_SPEED                          = _int32(0x8007)
    IS_SET_AUTO_WB_OFFSET                      = _int32(0x8008)
    IS_GET_AUTO_WB_OFFSET                      = _int32(0x8009)
    IS_SET_AUTO_WB_GAIN_RANGE                  = _int32(0x800A)
    IS_GET_AUTO_WB_GAIN_RANGE                  = _int32(0x800B)
    IS_SET_AUTO_WB_SPEED                       = _int32(0x800C)
    IS_GET_AUTO_WB_SPEED                       = _int32(0x800D)
    IS_SET_AUTO_WB_ONCE                        = _int32(0x800E)
    IS_GET_AUTO_WB_ONCE                        = _int32(0x800F)
    IS_SET_AUTO_BRIGHTNESS_ONCE                = _int32(0x8010)
    IS_GET_AUTO_BRIGHTNESS_ONCE                = _int32(0x8011)
    IS_SET_AUTO_HYSTERESIS                     = _int32(0x8012)
    IS_GET_AUTO_HYSTERESIS                     = _int32(0x8013)
    IS_GET_AUTO_HYSTERESIS_RANGE               = _int32(0x8014)
    IS_SET_AUTO_WB_HYSTERESIS                  = _int32(0x8015)
    IS_GET_AUTO_WB_HYSTERESIS                  = _int32(0x8016)
    IS_GET_AUTO_WB_HYSTERESIS_RANGE            = _int32(0x8017)
    IS_SET_AUTO_SKIPFRAMES                     = _int32(0x8018)
    IS_GET_AUTO_SKIPFRAMES                     = _int32(0x8019)
    IS_GET_AUTO_SKIPFRAMES_RANGE               = _int32(0x801A)
    IS_SET_AUTO_WB_SKIPFRAMES                  = _int32(0x801B)
    IS_GET_AUTO_WB_SKIPFRAMES                  = _int32(0x801C)
    IS_GET_AUTO_WB_SKIPFRAMES_RANGE            = _int32(0x801D)
    IS_SET_SENS_AUTO_SHUTTER_PHOTOM            = _int32(0x801E)
    IS_SET_SENS_AUTO_GAIN_PHOTOM               = _int32(0x801F)
    IS_GET_SENS_AUTO_SHUTTER_PHOTOM            = _int32(0x8020)
    IS_GET_SENS_AUTO_GAIN_PHOTOM               = _int32(0x8021)
    IS_GET_SENS_AUTO_SHUTTER_PHOTOM_DEF        = _int32(0x8022)
    IS_GET_SENS_AUTO_GAIN_PHOTOM_DEF           = _int32(0x8023)
    IS_SET_SENS_AUTO_CONTRAST_CORRECTION       = _int32(0x8024)
    IS_GET_SENS_AUTO_CONTRAST_CORRECTION       = _int32(0x8025)
    IS_GET_SENS_AUTO_CONTRAST_CORRECTION_RANGE = _int32(0x8026)
    IS_GET_SENS_AUTO_CONTRAST_CORRECTION_INC   = _int32(0x8027)
    IS_GET_SENS_AUTO_CONTRAST_CORRECTION_DEF   = _int32(0x8028)
    IS_SET_SENS_AUTO_CONTRAST_FDT_AOI_ENABLE   = _int32(0x8029)
    IS_GET_SENS_AUTO_CONTRAST_FDT_AOI_ENABLE   = _int32(0x8030)
    IS_SET_SENS_AUTO_BACKLIGHT_COMP            = _int32(0x8031)
    IS_GET_SENS_AUTO_BACKLIGHT_COMP            = _int32(0x8032)
    IS_GET_SENS_AUTO_BACKLIGHT_COMP_RANGE      = _int32(0x8033)
    IS_GET_SENS_AUTO_BACKLIGHT_COMP_INC        = _int32(0x8034)
    IS_GET_SENS_AUTO_BACKLIGHT_COMP_DEF        = _int32(0x8035)
    IS_SET_ANTI_FLICKER_MODE                   = _int32(0x8036)
    IS_GET_ANTI_FLICKER_MODE                   = _int32(0x8037)
    IS_GET_ANTI_FLICKER_MODE_DEF               = _int32(0x8038)
    IS_GET_AUTO_REFERENCE_DEF                  = _int32(0x8039)
    IS_GET_AUTO_WB_OFFSET_DEF                  = _int32(0x803A)
    IS_GET_AUTO_WB_OFFSET_MIN                  = _int32(0x803B)
    IS_GET_AUTO_WB_OFFSET_MAX                  = _int32(0x803C)
dAUTOCONTROL={a.name:a.value for a in AUTOCONTROL}
drAUTOCONTROL={a.value:a.name for a in AUTOCONTROL}


class AOI(enum.IntEnum):
    IS_SET_AUTO_BRIGHT_AOI = _int32(0x8000)
    IS_GET_AUTO_BRIGHT_AOI = _int32(0x8001)
    IS_SET_IMAGE_AOI       = _int32(0x8002)
    IS_GET_IMAGE_AOI       = _int32(0x8003)
    IS_SET_AUTO_WB_AOI     = _int32(0x8004)
    IS_GET_AUTO_WB_AOI     = _int32(0x8005)
dAOI={a.name:a.value for a in AOI}
drAOI={a.value:a.name for a in AOI}


class HOTPIXEL(enum.IntEnum):
    IS_HOTPIXEL_DISABLE_CORRECTION              = _int32(0x0000)
    IS_HOTPIXEL_ENABLE_SENSOR_CORRECTION        = _int32(0x0001)
    IS_HOTPIXEL_ENABLE_CAMERA_CORRECTION        = _int32(0x0002)
    IS_HOTPIXEL_ENABLE_SOFTWARE_USER_CORRECTION = _int32(0x0004)
    IS_HOTPIXEL_DISABLE_SENSOR_CORRECTION       = _int32(0x0008)
    IS_HOTPIXEL_GET_CORRECTION_MODE             = _int32(0x8000)
    IS_HOTPIXEL_GET_SUPPORTED_CORRECTION_MODES  = _int32(0x8001)
    IS_HOTPIXEL_GET_SOFTWARE_USER_LIST_EXISTS   = _int32(0x8100)
    IS_HOTPIXEL_GET_SOFTWARE_USER_LIST_NUMBER   = _int32(0x8101)
    IS_HOTPIXEL_GET_SOFTWARE_USER_LIST          = _int32(0x8102)
    IS_HOTPIXEL_SET_SOFTWARE_USER_LIST          = _int32(0x8103)
    IS_HOTPIXEL_SAVE_SOFTWARE_USER_LIST         = _int32(0x8104)
    IS_HOTPIXEL_LOAD_SOFTWARE_USER_LIST         = _int32(0x8105)
    IS_HOTPIXEL_GET_CAMERA_FACTORY_LIST_EXISTS  = _int32(0x8106)
    IS_HOTPIXEL_GET_CAMERA_FACTORY_LIST_NUMBER  = _int32(0x8107)
    IS_HOTPIXEL_GET_CAMERA_FACTORY_LIST         = _int32(0x8108)
    IS_HOTPIXEL_GET_CAMERA_USER_LIST_EXISTS     = _int32(0x8109)
    IS_HOTPIXEL_GET_CAMERA_USER_LIST_NUMBER     = _int32(0x810A)
    IS_HOTPIXEL_GET_CAMERA_USER_LIST            = _int32(0x810B)
    IS_HOTPIXEL_SET_CAMERA_USER_LIST            = _int32(0x810C)
    IS_HOTPIXEL_GET_CAMERA_USER_LIST_MAX_NUMBER = _int32(0x810D)
    IS_HOTPIXEL_DELETE_CAMERA_USER_LIST         = _int32(0x810E)
    IS_HOTPIXEL_GET_MERGED_CAMERA_LIST_NUMBER   = _int32(0x810F)
    IS_HOTPIXEL_GET_MERGED_CAMERA_LIST          = _int32(0x8110)
    IS_HOTPIXEL_SAVE_SOFTWARE_USER_LIST_UNICODE = _int32(0x8111)
    IS_HOTPIXEL_LOAD_SOFTWARE_USER_LIST_UNICODE = _int32(0x8112)
dHOTPIXEL={a.name:a.value for a in HOTPIXEL}
drHOTPIXEL={a.value:a.name for a in HOTPIXEL}


class COLORCORR(enum.IntEnum):
    IS_GET_CCOR_MODE             = _int32(0x8000)
    IS_GET_SUPPORTED_CCOR_MODE   = _int32(0x8001)
    IS_GET_DEFAULT_CCOR_MODE     = _int32(0x8002)
    IS_GET_CCOR_FACTOR           = _int32(0x8003)
    IS_GET_CCOR_FACTOR_MIN       = _int32(0x8004)
    IS_GET_CCOR_FACTOR_MAX       = _int32(0x8005)
    IS_GET_CCOR_FACTOR_DEFAULT   = _int32(0x8006)
    IS_CCOR_DISABLE              = _int32(0x0000)
    IS_CCOR_ENABLE               = _int32(0x0001)
    IS_CCOR_ENABLE_NORMAL        = _int32(0x0001)
    IS_CCOR_ENABLE_BG40_ENHANCED = _int32(0x0002)
    IS_CCOR_ENABLE_HQ_ENHANCED   = _int32(0x0004)
    IS_CCOR_SET_IR_AUTOMATIC     = _int32(0x0080)
    IS_CCOR_FACTOR               = _int32(0x0100)
    IS_CCOR_ENABLE_MASK          = _int32((0x0001 | 0x0002 | 0x0004))
dCOLORCORR={a.name:a.value for a in COLORCORR}
drCOLORCORR={a.value:a.name for a in COLORCORR}


class BAYER(enum.IntEnum):
    IS_GET_BAYER_CV_MODE   = _int32(0x8000)
    IS_SET_BAYER_CV_NORMAL = _int32(0x0000)
    IS_SET_BAYER_CV_BETTER = _int32(0x0001)
    IS_SET_BAYER_CV_BEST   = _int32(0x0002)
dBAYER={a.name:a.value for a in BAYER}
drBAYER={a.value:a.name for a in BAYER}


class COLORCONV(enum.IntEnum):
    IS_CONV_MODE_NONE         = _int32(0x0000)
    IS_CONV_MODE_SOFTWARE     = _int32(0x0001)
    IS_CONV_MODE_SOFTWARE_3X3 = _int32(0x0002)
    IS_CONV_MODE_SOFTWARE_5X5 = _int32(0x0004)
    IS_CONV_MODE_HARDWARE_3X3 = _int32(0x0008)
    IS_CONV_MODE_OPENCL_3X3   = _int32(0x0020)
    IS_CONV_MODE_OPENCL_5X5   = _int32(0x0040)
    IS_CONV_MODE_JPEG         = _int32(0x0100)
dCOLORCONV={a.name:a.value for a in COLORCONV}
drCOLORCONV={a.value:a.name for a in COLORCONV}


class EDGEENH(enum.IntEnum):
    IS_GET_EDGE_ENHANCEMENT = _int32(0x8000)
    IS_EDGE_EN_DISABLE      = _int32(0)
    IS_EDGE_EN_STRONG       = _int32(1)
    IS_EDGE_EN_WEAK         = _int32(2)
dEDGEENH={a.name:a.value for a in EDGEENH}
drEDGEENH={a.value:a.name for a in EDGEENH}


class WHITEBALANCE(enum.IntEnum):
    IS_GET_WB_MODE             = _int32(0x8000)
    IS_SET_WB_DISABLE          = _int32(0x0000)
    IS_SET_WB_USER             = _int32(0x0001)
    IS_SET_WB_AUTO_ENABLE      = _int32(0x0002)
    IS_SET_WB_AUTO_ENABLE_ONCE = _int32(0x0004)
    IS_SET_WB_DAYLIGHT_65      = _int32(0x0101)
    IS_SET_WB_COOL_WHITE       = _int32(0x0102)
    IS_SET_WB_U30              = _int32(0x0103)
    IS_SET_WB_ILLUMINANT_A     = _int32(0x0104)
    IS_SET_WB_HORIZON          = _int32(0x0105)
dWHITEBALANCE={a.name:a.value for a in WHITEBALANCE}
drWHITEBALANCE={a.value:a.name for a in WHITEBALANCE}


class EEPROM(enum.IntEnum):
    IS_EEPROM_MIN_USER_ADDRESS = _int32(0)
    IS_EEPROM_MAX_USER_ADDRESS = _int32(63)
    IS_EEPROM_MAX_USER_SPACE   = _int32(64)
dEEPROM={a.name:a.value for a in EEPROM}
drEEPROM={a.value:a.name for a in EEPROM}


class ERRREP(enum.IntEnum):
    IS_GET_ERR_REP_MODE = _int32(0x8000)
    IS_ENABLE_ERR_REP   = _int32(1)
    IS_DISABLE_ERR_REP  = _int32(0)
dERRREP={a.name:a.value for a in ERRREP}
drERRREP={a.value:a.name for a in ERRREP}


class DISPMODE(enum.IntEnum):
    IS_GET_DISPLAY_MODE = _int32(0x8000)
    IS_SET_DM_DIB       = _int32(1)
    IS_SET_DM_DIRECT3D  = _int32(4)
    IS_SET_DM_OPENGL    = _int32(8)
    IS_SET_DM_MONO      = _int32(0x800)
    IS_SET_DM_BAYER     = _int32(0x1000)
    IS_SET_DM_YCBCR     = _int32(0x4000)
dDISPMODE={a.name:a.value for a in DISPMODE}
drDISPMODE={a.value:a.name for a in DISPMODE}


class DIRECTRENDER(enum.IntEnum):
    DR_GET_OVERLAY_DC                   = _int32(1)
    DR_GET_MAX_OVERLAY_SIZE             = _int32(2)
    DR_GET_OVERLAY_KEY_COLOR            = _int32(3)
    DR_RELEASE_OVERLAY_DC               = _int32(4)
    DR_SHOW_OVERLAY                     = _int32(5)
    DR_HIDE_OVERLAY                     = _int32(6)
    DR_SET_OVERLAY_SIZE                 = _int32(7)
    DR_SET_OVERLAY_POSITION             = _int32(8)
    DR_SET_OVERLAY_KEY_COLOR            = _int32(9)
    DR_SET_HWND                         = _int32(10)
    DR_ENABLE_SCALING                   = _int32(11)
    DR_DISABLE_SCALING                  = _int32(12)
    DR_CLEAR_OVERLAY                    = _int32(13)
    DR_ENABLE_SEMI_TRANSPARENT_OVERLAY  = _int32(14)
    DR_DISABLE_SEMI_TRANSPARENT_OVERLAY = _int32(15)
    DR_CHECK_COMPATIBILITY              = _int32(16)
    DR_SET_VSYNC_OFF                    = _int32(17)
    DR_SET_VSYNC_AUTO                   = _int32(18)
    DR_SET_USER_SYNC                    = _int32(19)
    DR_GET_USER_SYNC_POSITION_RANGE     = _int32(20)
    DR_LOAD_OVERLAY_FROM_FILE           = _int32(21)
    DR_STEAL_NEXT_FRAME                 = _int32(22)
    DR_SET_STEAL_FORMAT                 = _int32(23)
    DR_GET_STEAL_FORMAT                 = _int32(24)
    DR_ENABLE_IMAGE_SCALING             = _int32(25)
    DR_GET_OVERLAY_SIZE                 = _int32(26)
    DR_CHECK_COLOR_MODE_SUPPORT         = _int32(27)
    DR_GET_OVERLAY_DATA                 = _int32(28)
    DR_UPDATE_OVERLAY_DATA              = _int32(29)
    DR_GET_SUPPORTED                    = _int32(30)
dDIRECTRENDER={a.name:a.value for a in DIRECTRENDER}
drDIRECTRENDER={a.value:a.name for a in DIRECTRENDER}


class RENUM(enum.IntEnum):
    IS_RENUM_BY_CAMERA = _int32(0)
    IS_RENUM_BY_HOST   = _int32(1)
dRENUM={a.name:a.value for a in RENUM}
drRENUM={a.value:a.name for a in RENUM}


class EVENT(enum.IntEnum):
    IS_SET_EVENT_ODD                      = _int32(0)
    IS_SET_EVENT_EVEN                     = _int32(1)
    IS_SET_EVENT_FRAME                    = _int32(2)
    IS_SET_EVENT_EXTTRIG                  = _int32(3)
    IS_SET_EVENT_VSYNC                    = _int32(4)
    IS_SET_EVENT_SEQ                      = _int32(5)
    IS_SET_EVENT_STEAL                    = _int32(6)
    IS_SET_EVENT_VPRES                    = _int32(7)
    IS_SET_EVENT_CAPTURE_STATUS           = _int32(8)
    IS_SET_EVENT_TRANSFER_FAILED          = _int32(8)
    IS_SET_EVENT_DEVICE_RECONNECTED       = _int32(9)
    IS_SET_EVENT_MEMORY_MODE_FINISH       = _int32(10)
    IS_SET_EVENT_FRAME_RECEIVED           = _int32(11)
    IS_SET_EVENT_WB_FINISHED              = _int32(12)
    IS_SET_EVENT_AUTOBRIGHTNESS_FINISHED  = _int32(13)
    IS_SET_EVENT_OVERLAY_DATA_LOST        = _int32(16)
    IS_SET_EVENT_CAMERA_MEMORY            = _int32(17)
    IS_SET_EVENT_CONNECTIONSPEED_CHANGED  = _int32(18)
    IS_SET_EVENT_AUTOFOCUS_FINISHED       = _int32(19)
    IS_SET_EVENT_FIRST_PACKET_RECEIVED    = _int32(20)
    IS_SET_EVENT_PMC_IMAGE_PARAMS_CHANGED = _int32(21)
    IS_SET_EVENT_DEVICE_PLUGGED_IN        = _int32(22)
    IS_SET_EVENT_DEVICE_UNPLUGGED         = _int32(23)
    IS_SET_EVENT_TEMPERATURE_STATUS       = _int32(24)
    IS_SET_EVENT_REMOVE                   = _int32(128)
    IS_SET_EVENT_REMOVAL                  = _int32(129)
    IS_SET_EVENT_NEW_DEVICE               = _int32(130)
    IS_SET_EVENT_STATUS_CHANGED           = _int32(131)
dEVENT={a.name:a.value for a in EVENT}
drEVENT={a.value:a.name for a in EVENT}


class WINDOWMSG(enum.IntEnum):
    IS_UC480_MESSAGE            = _int32((0x400 + 0x0100))
    IS_FRAME                    = _int32(0x0000)
    IS_SEQUENCE                 = _int32(0x0001)
    IS_TRIGGER                  = _int32(0x0002)
    IS_CAPTURE_STATUS           = _int32(0x0003)
    IS_TRANSFER_FAILED          = _int32(0x0003)
    IS_DEVICE_RECONNECTED       = _int32(0x0004)
    IS_MEMORY_MODE_FINISH       = _int32(0x0005)
    IS_FRAME_RECEIVED           = _int32(0x0006)
    IS_GENERIC_ERROR            = _int32(0x0007)
    IS_STEAL_VIDEO              = _int32(0x0008)
    IS_WB_FINISHED              = _int32(0x0009)
    IS_AUTOBRIGHTNESS_FINISHED  = _int32(0x000A)
    IS_OVERLAY_DATA_LOST        = _int32(0x000B)
    IS_CAMERA_MEMORY            = _int32(0x000C)
    IS_CONNECTIONSPEED_CHANGED  = _int32(0x000D)
    IS_AUTOFOCUS_FINISHED       = _int32(0x000E)
    IS_FIRST_PACKET_RECEIVED    = _int32(0x000F)
    IS_PMC_IMAGE_PARAMS_CHANGED = _int32(0x0010)
    IS_DEVICE_PLUGGED_IN        = _int32(0x0011)
    IS_DEVICE_UNPLUGGED         = _int32(0x0012)
    IS_TEMPERATURE_STATUS       = _int32(0x0013)
    IS_DEVICE_REMOVED           = _int32(0x1000)
    IS_DEVICE_REMOVAL           = _int32(0x1001)
    IS_NEW_DEVICE               = _int32(0x1002)
    IS_DEVICE_STATUS_CHANGED    = _int32(0x1003)
dWINDOWMSG={a.name:a.value for a in WINDOWMSG}
drWINDOWMSG={a.value:a.name for a in WINDOWMSG}


class CAMID(enum.IntEnum):
    IS_GET_CAMERA_ID = _int32(0x8000)
dCAMID={a.name:a.value for a in CAMID}
drCAMID={a.value:a.name for a in CAMID}


class CAMINFO(enum.IntEnum):
    IS_GET_STATUS             = _int32(0x8000)
    IS_EXT_TRIGGER_EVENT_CNT  = _int32(0)
    IS_FIFO_OVR_CNT           = _int32(1)
    IS_SEQUENCE_CNT           = _int32(2)
    IS_LAST_FRAME_FIFO_OVR    = _int32(3)
    IS_SEQUENCE_SIZE          = _int32(4)
    IS_VIDEO_PRESENT          = _int32(5)
    IS_STEAL_FINISHED         = _int32(6)
    IS_STORE_FILE_PATH        = _int32(7)
    IS_LUMA_BANDWIDTH_FILTER  = _int32(8)
    IS_BOARD_REVISION         = _int32(9)
    IS_MIRROR_BITMAP_UPDOWN   = _int32(10)
    IS_BUS_OVR_CNT            = _int32(11)
    IS_STEAL_ERROR_CNT        = _int32(12)
    IS_LOW_COLOR_REMOVAL      = _int32(13)
    IS_CHROMA_COMB_FILTER     = _int32(14)
    IS_CHROMA_AGC             = _int32(15)
    IS_WATCHDOG_ON_BOARD      = _int32(16)
    IS_PASSTHROUGH_ON_BOARD   = _int32(17)
    IS_EXTERNAL_VREF_MODE     = _int32(18)
    IS_WAIT_TIMEOUT           = _int32(19)
    IS_TRIGGER_MISSED         = _int32(20)
    IS_LAST_CAPTURE_ERROR     = _int32(21)
    IS_PARAMETER_SET_1        = _int32(22)
    IS_PARAMETER_SET_2        = _int32(23)
    IS_STANDBY                = _int32(24)
    IS_STANDBY_SUPPORTED      = _int32(25)
    IS_QUEUED_IMAGE_EVENT_CNT = _int32(26)
    IS_PARAMETER_EXT          = _int32(27)
dCAMINFO={a.name:a.value for a in CAMINFO}
drCAMINFO={a.value:a.name for a in CAMINFO}


class IFTYPE(enum.IntEnum):
    IS_INTERFACE_TYPE_USB  = _int32(0x40)
    IS_INTERFACE_TYPE_USB3 = _int32(0x60)
    IS_INTERFACE_TYPE_ETH  = _int32(0x80)
    IS_INTERFACE_TYPE_PMC  = _int32(0xf0)
dIFTYPE={a.name:a.value for a in IFTYPE}
drIFTYPE={a.value:a.name for a in IFTYPE}


class BOARDTYPE(enum.IntEnum):
    IS_BOARD_TYPE_UC480_USB      = _int32((0x40 + 0))
    IS_BOARD_TYPE_UC480_USB_SE   = _int32((0x40 + 0))
    IS_BOARD_TYPE_UC480_USB_RE   = _int32((0x40 + 0))
    IS_BOARD_TYPE_UC480_USB_ME   = _int32((0x40 + 0x01))
    IS_BOARD_TYPE_UC480_USB_LE   = _int32((0x40 + 0x02))
    IS_BOARD_TYPE_UC480_USB_XS   = _int32((0x40 + 0x03))
    IS_BOARD_TYPE_UC480_USB_ML   = _int32((0x40 + 0x05))
    IS_BOARD_TYPE_UC480_USB3_LE  = _int32((0x60 + 0x02))
    IS_BOARD_TYPE_UC480_USB3_XC  = _int32((0x60 + 0x03))
    IS_BOARD_TYPE_UC480_USB3_CP  = _int32((0x60 + 0x04))
    IS_BOARD_TYPE_UC480_USB3_ML  = _int32((0x60 + 0x05))
    IS_BOARD_TYPE_UC480_ETH      = _int32(0x80)
    IS_BOARD_TYPE_UC480_ETH_HE   = _int32(0x80)
    IS_BOARD_TYPE_UC480_ETH_SE   = _int32((0x80 + 0x01))
    IS_BOARD_TYPE_UC480_ETH_RE   = _int32((0x80 + 0x01))
    IS_BOARD_TYPE_UC480_ETH_LE   = _int32((0x80 + 0x02))
    IS_BOARD_TYPE_UC480_ETH_CP   = _int32((0x80 + 0x04))
    IS_BOARD_TYPE_UC480_ETH_SEP  = _int32((0x80 + 0x06))
    IS_BOARD_TYPE_UC480_ETH_REP  = _int32((0x80 + 0x06))
    IS_BOARD_TYPE_UC480_ETH_LEET = _int32((0x80 + 0x07))
    IS_BOARD_TYPE_UC480_ETH_TE   = _int32((0x80 + 0x08))
dBOARDTYPE={a.name:a.value for a in BOARDTYPE}
drBOARDTYPE={a.value:a.name for a in BOARDTYPE}


class CAMTYPE(enum.IntEnum):
    IS_CAMERA_TYPE_UC480_USB      = _int32((0x40 + 0))
    IS_CAMERA_TYPE_UC480_USB_SE   = _int32((0x40 + 0))
    IS_CAMERA_TYPE_UC480_USB_RE   = _int32((0x40 + 0))
    IS_CAMERA_TYPE_UC480_USB_ME   = _int32((0x40 + 0x01))
    IS_CAMERA_TYPE_UC480_USB_LE   = _int32((0x40 + 0x02))
    IS_CAMERA_TYPE_UC480_USB_ML   = _int32((0x40 + 0x05))
    IS_CAMERA_TYPE_UC480_USB3_LE  = _int32((0x60 + 0x02))
    IS_CAMERA_TYPE_UC480_USB3_XC  = _int32((0x60 + 0x03))
    IS_CAMERA_TYPE_UC480_USB3_CP  = _int32((0x60 + 0x04))
    IS_CAMERA_TYPE_UC480_USB3_ML  = _int32((0x60 + 0x05))
    IS_CAMERA_TYPE_UC480_ETH      = _int32(0x80)
    IS_CAMERA_TYPE_UC480_ETH_HE   = _int32(0x80)
    IS_CAMERA_TYPE_UC480_ETH_SE   = _int32((0x80 + 0x01))
    IS_CAMERA_TYPE_UC480_ETH_RE   = _int32((0x80 + 0x01))
    IS_CAMERA_TYPE_UC480_ETH_LE   = _int32((0x80 + 0x02))
    IS_CAMERA_TYPE_UC480_ETH_CP   = _int32((0x80 + 0x04))
    IS_CAMERA_TYPE_UC480_ETH_SEP  = _int32((0x80 + 0x06))
    IS_CAMERA_TYPE_UC480_ETH_REP  = _int32((0x80 + 0x06))
    IS_CAMERA_TYPE_UC480_ETH_LEET = _int32((0x80 + 0x07))
    IS_CAMERA_TYPE_UC480_ETH_TE   = _int32((0x80 + 0x08))
    IS_CAMERA_TYPE_UC480_PMC      = _int32((0xf0 + 0x01))
dCAMTYPE={a.name:a.value for a in CAMTYPE}
drCAMTYPE={a.value:a.name for a in CAMTYPE}


class OSTYPE(enum.IntEnum):
    IS_OS_UNDETERMINED      = _int32(0)
    IS_OS_WIN95             = _int32(1)
    IS_OS_WINNT40           = _int32(2)
    IS_OS_WIN98             = _int32(3)
    IS_OS_WIN2000           = _int32(4)
    IS_OS_WINXP             = _int32(5)
    IS_OS_WINME             = _int32(6)
    IS_OS_WINNET            = _int32(7)
    IS_OS_WINSERVER2003     = _int32(8)
    IS_OS_WINVISTA          = _int32(9)
    IS_OS_LINUX24           = _int32(10)
    IS_OS_LINUX26           = _int32(11)
    IS_OS_WIN7              = _int32(12)
    IS_OS_WIN8              = _int32(13)
    IS_OS_WIN8SERVER        = _int32(14)
    IS_OS_GREATER_THAN_WIN8 = _int32(15)
dOSTYPE={a.name:a.value for a in OSTYPE}
drOSTYPE={a.value:a.name for a in OSTYPE}


class BUSSPEED(enum.IntEnum):
    IS_USB_10            = _int32(0x0001)
    IS_USB_11            = _int32(0x0002)
    IS_USB_20            = _int32(0x0004)
    IS_USB_30            = _int32(0x0008)
    IS_ETHERNET_10       = _int32(0x0080)
    IS_ETHERNET_100      = _int32(0x0100)
    IS_ETHERNET_1000     = _int32(0x0200)
    IS_ETHERNET_10000    = _int32(0x0400)
    IS_USB_LOW_SPEED     = _int32(1)
    IS_USB_FULL_SPEED    = _int32(12)
    IS_USB_HIGH_SPEED    = _int32(480)
    IS_USB_SUPER_SPEED   = _int32(4000)
    IS_ETHERNET_10Base   = _int32(10)
    IS_ETHERNET_100Base  = _int32(100)
    IS_ETHERNET_1000Base = _int32(1000)
    IS_ETHERNET_10GBase  = _int32(10000)
dBUSSPEED={a.name:a.value for a in BUSSPEED}
drBUSSPEED={a.value:a.name for a in BUSSPEED}


class HDR(enum.IntEnum):
    IS_HDR_NOT_SUPPORTED = _int32(0)
    IS_HDR_KNEEPOINTS    = _int32(1)
    IS_DISABLE_HDR       = _int32(0)
    IS_ENABLE_HDR        = _int32(1)
dHDR={a.name:a.value for a in HDR}
drHDR={a.value:a.name for a in HDR}


class TESTIMG(enum.IntEnum):
    IS_TEST_IMAGE_NONE                       = _int32(0x00000000)
    IS_TEST_IMAGE_WHITE                      = _int32(0x00000001)
    IS_TEST_IMAGE_BLACK                      = _int32(0x00000002)
    IS_TEST_IMAGE_HORIZONTAL_GREYSCALE       = _int32(0x00000004)
    IS_TEST_IMAGE_VERTICAL_GREYSCALE         = _int32(0x00000008)
    IS_TEST_IMAGE_DIAGONAL_GREYSCALE         = _int32(0x00000010)
    IS_TEST_IMAGE_WEDGE_GRAY                 = _int32(0x00000020)
    IS_TEST_IMAGE_WEDGE_COLOR                = _int32(0x00000040)
    IS_TEST_IMAGE_ANIMATED_WEDGE_GRAY        = _int32(0x00000080)
    IS_TEST_IMAGE_ANIMATED_WEDGE_COLOR       = _int32(0x00000100)
    IS_TEST_IMAGE_MONO_BARS                  = _int32(0x00000200)
    IS_TEST_IMAGE_COLOR_BARS1                = _int32(0x00000400)
    IS_TEST_IMAGE_COLOR_BARS2                = _int32(0x00000800)
    IS_TEST_IMAGE_GREYSCALE1                 = _int32(0x00001000)
    IS_TEST_IMAGE_GREY_AND_COLOR_BARS        = _int32(0x00002000)
    IS_TEST_IMAGE_MOVING_GREY_AND_COLOR_BARS = _int32(0x00004000)
    IS_TEST_IMAGE_ANIMATED_LINE              = _int32(0x00008000)
    IS_TEST_IMAGE_ALTERNATE_PATTERN          = _int32(0x00010000)
    IS_TEST_IMAGE_VARIABLE_GREY              = _int32(0x00020000)
    IS_TEST_IMAGE_MONOCHROME_HORIZONTAL_BARS = _int32(0x00040000)
    IS_TEST_IMAGE_MONOCHROME_VERTICAL_BARS   = _int32(0x00080000)
    IS_TEST_IMAGE_CURSOR_H                   = _int32(0x00100000)
    IS_TEST_IMAGE_CURSOR_V                   = _int32(0x00200000)
    IS_TEST_IMAGE_COLDPIXEL_GRID             = _int32(0x00400000)
    IS_TEST_IMAGE_HOTPIXEL_GRID              = _int32(0x00800000)
    IS_TEST_IMAGE_VARIABLE_RED_PART          = _int32(0x01000000)
    IS_TEST_IMAGE_VARIABLE_GREEN_PART        = _int32(0x02000000)
    IS_TEST_IMAGE_VARIABLE_BLUE_PART         = _int32(0x04000000)
    IS_TEST_IMAGE_SHADING_IMAGE              = _int32(0x08000000)
    IS_TEST_IMAGE_WEDGE_GRAY_SENSOR          = _int32(0x10000000)
    IS_TEST_IMAGE_ANIMATED_WEDGE_GRAY_SENSOR = _int32(0x20000000)
    IS_TEST_IMAGE_RAMPING_PATTERN            = _int32(0x40000000)
    IS_TEST_IMAGE_CHESS_PATTERN              = _int32(0x80000000)
dTESTIMG={a.name:a.value for a in TESTIMG}
drTESTIMG={a.value:a.name for a in TESTIMG}


class SENSORSCALER(enum.IntEnum):
    IS_DISABLE_SENSOR_SCALER = _int32(0)
    IS_ENABLE_SENSOR_SCALER  = _int32(1)
    IS_ENABLE_ANTI_ALIASING  = _int32(2)
dSENSORSCALER={a.name:a.value for a in SENSORSCALER}
drSENSORSCALER={a.value:a.name for a in SENSORSCALER}


class SEQUENCE(enum.IntEnum):
    IS_LOCK_LAST_BUFFER         = _int32(0x8002)
    IS_GET_ALLOC_ID_OF_THIS_BUF = _int32(0x8004)
    IS_GET_ALLOC_ID_OF_LAST_BUF = _int32(0x8008)
    IS_USE_ALLOC_ID             = _int32(0x8000)
    IS_USE_CURRENT_IMG_SIZE     = _int32(0xC000)
dSEQUENCE={a.name:a.value for a in SEQUENCE}
drSEQUENCE={a.value:a.name for a in SEQUENCE}


class IMGFILETYPE(enum.IntEnum):
    IS_IMG_BMP = _int32(0)
    IS_IMG_JPG = _int32(1)
    IS_IMG_PNG = _int32(2)
    IS_IMG_RAW = _int32(4)
    IS_IMG_TIF = _int32(8)
dIMGFILETYPE={a.name:a.value for a in IMGFILETYPE}
drIMGFILETYPE={a.value:a.name for a in IMGFILETYPE}


class I2C(enum.IntEnum):
    IS_I2C_16_BIT_REGISTER = _int32(0x10000000)
    IS_I2C_0_BIT_REGISTER  = _int32(0x20000000)
    IS_I2C_DONT_WAIT       = _int32(0x00800000)
dI2C={a.name:a.value for a in I2C}
drI2C={a.value:a.name for a in I2C}


class GAMMAMODE(enum.IntEnum):
    IS_GET_GAMMA_MODE = _int32(0x8000)
    IS_SET_GAMMA_OFF  = _int32(0)
    IS_SET_GAMMA_ON   = _int32(1)
dGAMMAMODE={a.name:a.value for a in GAMMAMODE}
drGAMMAMODE={a.value:a.name for a in GAMMAMODE}


class CAPMODE(enum.IntEnum):
    IS_GET_CAPTURE_MODE     = _int32(0x8000)
    IS_SET_CM_ODD           = _int32(0x0001)
    IS_SET_CM_EVEN          = _int32(0x0002)
    IS_SET_CM_FRAME         = _int32(0x0004)
    IS_SET_CM_NONINTERLACED = _int32(0x0008)
    IS_SET_CM_NEXT_FRAME    = _int32(0x0010)
    IS_SET_CM_NEXT_FIELD    = _int32(0x0020)
    IS_SET_CM_BOTHFIELDS    = _int32((0x0001 | 0x0002 | 0x0008))
    IS_SET_CM_FRAME_STEREO  = _int32(0x2004)
dCAPMODE={a.name:a.value for a in CAPMODE}
drCAPMODE={a.value:a.name for a in CAPMODE}


class AUTOFEATURE(enum.IntEnum):
    AC_SHUTTER                         = _int32(0x00000001)
    AC_GAIN                            = _int32(0x00000002)
    AC_WHITEBAL                        = _int32(0x00000004)
    AC_WB_RED_CHANNEL                  = _int32(0x00000008)
    AC_WB_GREEN_CHANNEL                = _int32(0x00000010)
    AC_WB_BLUE_CHANNEL                 = _int32(0x00000020)
    AC_FRAMERATE                       = _int32(0x00000040)
    AC_SENSOR_SHUTTER                  = _int32(0x00000080)
    AC_SENSOR_GAIN                     = _int32(0x00000100)
    AC_SENSOR_GAIN_SHUTTER             = _int32(0x00000200)
    AC_SENSOR_FRAMERATE                = _int32(0x00000400)
    AC_SENSOR_WB                       = _int32(0x00000800)
    AC_SENSOR_AUTO_REFERENCE           = _int32(0x00001000)
    AC_SENSOR_AUTO_SPEED               = _int32(0x00002000)
    AC_SENSOR_AUTO_HYSTERESIS          = _int32(0x00004000)
    AC_SENSOR_AUTO_SKIPFRAMES          = _int32(0x00008000)
    AC_SENSOR_AUTO_CONTRAST_CORRECTION = _int32(0x00010000)
    AC_SENSOR_AUTO_CONTRAST_FDT_AOI    = _int32(0x00020000)
    AC_SENSOR_AUTO_BACKLIGHT_COMP      = _int32(0x00040000)
    ACS_ADJUSTING                      = _int32(0x00000001)
    ACS_FINISHED                       = _int32(0x00000002)
    ACS_DISABLED                       = _int32(0x00000004)
dAUTOFEATURE={a.name:a.value for a in AUTOFEATURE}
drAUTOFEATURE={a.value:a.name for a in AUTOFEATURE}


class IO(enum.IntEnum):
    IO_LED_STATE_1                  = _int32(0)
    IO_LED_STATE_2                  = _int32(1)
    IO_FLASH_MODE_OFF               = _int32(0)
    IO_FLASH_MODE_TRIGGER_LO_ACTIVE = _int32(1)
    IO_FLASH_MODE_TRIGGER_HI_ACTIVE = _int32(2)
    IO_FLASH_MODE_CONSTANT_HIGH     = _int32(3)
    IO_FLASH_MODE_CONSTANT_LOW      = _int32(4)
    IO_FLASH_MODE_FREERUN_LO_ACTIVE = _int32(5)
    IO_FLASH_MODE_FREERUN_HI_ACTIVE = _int32(6)
    IS_FLASH_MODE_PWM               = _int32(0x8000)
    IO_FLASH_MODE_GPIO_1            = _int32(0x0010)
    IO_FLASH_MODE_GPIO_2            = _int32(0x0020)
    IO_FLASH_MODE_GPIO_3            = _int32(0x0040)
    IO_FLASH_MODE_GPIO_4            = _int32(0x0080)
    IO_FLASH_MODE_GPIO_5            = _int32(0x0100)
    IO_FLASH_MODE_GPIO_6            = _int32(0x0200)
    IO_FLASH_GPIO_PORT_MASK         = _int32((0x0010 | 0x0020 | 0x0040 | 0x0080 | 0x0100 | 0x0200))
    IO_GPIO_1                       = _int32(0x0001)
    IO_GPIO_2                       = _int32(0x0002)
    IO_GPIO_3                       = _int32(0x0004)
    IO_GPIO_4                       = _int32(0x0008)
    IO_GPIO_5                       = _int32(0x0010)
    IO_GPIO_6                       = _int32(0x0020)
    IS_GPIO_INPUT                   = _int32(0x0001)
    IS_GPIO_OUTPUT                  = _int32(0x0002)
    IS_GPIO_FLASH                   = _int32(0x0004)
    IS_GPIO_PWM                     = _int32(0x0008)
    IS_GPIO_COMPORT_RX              = _int32(0x0010)
    IS_GPIO_COMPORT_TX              = _int32(0x0020)
    IS_GPIO_MULTI_INTEGRATION_MODE  = _int32(0x0040)
    IS_GPIO_TRIGGER                 = _int32(0x0080)
    IS_GPIO_I2C                     = _int32(0x0100)
    IS_FLASH_AUTO_FREERUN_OFF       = _int32(0)
    IS_FLASH_AUTO_FREERUN_ON        = _int32(1)
dIO={a.name:a.value for a in IO}
drIO={a.value:a.name for a in IO}


class AUTOPAR(enum.IntEnum):
    IS_AWB_GREYWORLD                = _int32(0x0001)
    IS_AWB_COLOR_TEMPERATURE        = _int32(0x0002)
    IS_AUTOPARAMETER_DISABLE        = _int32(0)
    IS_AUTOPARAMETER_ENABLE         = _int32(1)
    IS_AUTOPARAMETER_ENABLE_RUNONCE = _int32(2)
dAUTOPAR={a.name:a.value for a in AUTOPAR}
drAUTOPAR={a.value:a.name for a in AUTOPAR}


class LUT(enum.IntEnum):
    IS_LUT_64                            = _int32(64)
    IS_LUT_128                           = _int32(128)
    IS_LUT_PRESET_ID_IDENTITY            = _int32(0)
    IS_LUT_PRESET_ID_NEGATIVE            = _int32(1)
    IS_LUT_PRESET_ID_GLOW1               = _int32(2)
    IS_LUT_PRESET_ID_GLOW2               = _int32(3)
    IS_LUT_PRESET_ID_ASTRO1              = _int32(4)
    IS_LUT_PRESET_ID_RAINBOW1            = _int32(5)
    IS_LUT_PRESET_ID_MAP1                = _int32(6)
    IS_LUT_PRESET_ID_HOT                 = _int32(7)
    IS_LUT_PRESET_ID_SEPIC               = _int32(8)
    IS_LUT_PRESET_ID_ONLY_RED            = _int32(9)
    IS_LUT_PRESET_ID_ONLY_GREEN          = _int32(10)
    IS_LUT_PRESET_ID_ONLY_BLUE           = _int32(11)
    IS_LUT_PRESET_ID_DIGITAL_GAIN_2X     = _int32(12)
    IS_LUT_PRESET_ID_DIGITAL_GAIN_4X     = _int32(13)
    IS_LUT_PRESET_ID_DIGITAL_GAIN_8X     = _int32(14)
    IS_LUT_CMD_SET_ENABLED               = _int32(0x0001)
    IS_LUT_CMD_SET_MODE                  = _int32(0x0002)
    IS_LUT_CMD_GET_STATE                 = _int32(0x0005)
    IS_LUT_CMD_GET_SUPPORT_INFO          = _int32(0x0006)
    IS_LUT_CMD_SET_USER_LUT              = _int32(0x0010)
    IS_LUT_CMD_GET_USER_LUT              = _int32(0x0011)
    IS_LUT_CMD_GET_COMPLETE_LUT          = _int32(0x0012)
    IS_LUT_CMD_GET_PRESET_LUT            = _int32(0x0013)
    IS_LUT_CMD_LOAD_FILE                 = _int32(0x0100)
    IS_LUT_CMD_SAVE_FILE                 = _int32(0x0101)
    IS_LUT_STATE_ID_FLAG_HARDWARE        = _int32(0x0010)
    IS_LUT_STATE_ID_FLAG_SOFTWARE        = _int32(0x0020)
    IS_LUT_STATE_ID_FLAG_GAMMA           = _int32(0x0100)
    IS_LUT_STATE_ID_FLAG_LUT             = _int32(0x0200)
    IS_LUT_STATE_ID_INACTIVE             = _int32(0x0000)
    IS_LUT_STATE_ID_NOT_SUPPORTED        = _int32(0x0001)
    IS_LUT_STATE_ID_HARDWARE_LUT         = _int32((0x0010 | 0x0200))
    IS_LUT_STATE_ID_HARDWARE_GAMMA       = _int32((0x0010 | 0x0100))
    IS_LUT_STATE_ID_HARDWARE_LUTANDGAMMA = _int32((0x0010 | 0x0200 | 0x0100))
    IS_LUT_STATE_ID_SOFTWARE_LUT         = _int32((0x0020 | 0x0200))
    IS_LUT_STATE_ID_SOFTWARE_GAMMA       = _int32((0x0020 | 0x0100))
    IS_LUT_STATE_ID_SOFTWARE_LUTANDGAMMA = _int32((0x0020 | 0x0200 | 0x0100))
    IS_LUT_MODE_ID_DEFAULT               = _int32(0)
    IS_LUT_MODE_ID_FORCE_HARDWARE        = _int32(1)
    IS_LUT_MODE_ID_FORCE_SOFTWARE        = _int32(2)
    IS_LUT_DISABLED                      = _int32(0)
    IS_LUT_ENABLED                       = _int32(1)
dLUT={a.name:a.value for a in LUT}
drLUT={a.value:a.name for a in LUT}


class GAMMA(enum.IntEnum):
    IS_GAMMA_CMD_SET         = _int32(0x0001)
    IS_GAMMA_CMD_GET_DEFAULT = _int32(0x0002)
    IS_GAMMA_CMD_GET         = _int32(0x0003)
dGAMMA={a.name:a.value for a in GAMMA}
drGAMMA={a.value:a.name for a in GAMMA}


class MULTICAST(enum.IntEnum):
    IS_MC_CMD_FLAG_ACTIVE                                        = _int32(0x1000)
    IS_MC_CMD_FLAG_PASSIVE                                       = _int32(0x2000)
    IS_PMC_CMD_INITIALIZE                                        = _int32((   0x0001 | 0x2000 ))
    IS_PMC_CMD_DEINITIALIZE                                      = _int32((   0x0002 | 0x2000 ))
    IS_PMC_CMD_ADDMCDEVICE                                       = _int32((   0x0003 | 0x2000 ))
    IS_PMC_CMD_REMOVEMCDEVICE                                    = _int32((   0x0004 | 0x2000 ))
    IS_PMC_CMD_STOREDEVICES                                      = _int32((   0x0005 | 0x2000 ))
    IS_PMC_CMD_LOADDEVICES                                       = _int32((   0x0006 | 0x2000 ))
    IS_PMC_CMD_SYSTEM_SET_ENABLE                                 = _int32((   0x0007 | 0x2000 ))
    IS_PMC_CMD_SYSTEM_GET_ENABLE                                 = _int32((   0x0008 | 0x2000 ))
    IS_PMC_CMD_REMOVEALLMCDEVICES                                = _int32((   0x0009 | 0x2000 ))
    IS_AMC_CMD_SET_MC_IP                                         = _int32((   0x0010 | 0x1000 ))
    IS_AMC_CMD_GET_MC_IP                                         = _int32((   0x0011 | 0x1000 ))
    IS_AMC_CMD_SET_MC_ENABLED                                    = _int32((   0x0012 | 0x1000 ))
    IS_AMC_CMD_GET_MC_ENABLED                                    = _int32((   0x0013 | 0x1000 ))
    IS_AMC_CMD_GET_MC_SUPPORTED                                  = _int32((   0x0014 | 0x1000 ))
    IS_AMC_SUPPORTED_FLAG_DEVICE                                 = _int32((   0x0001 ))
    IS_AMC_SUPPORTED_FLAG_FIRMWARE                               = _int32((   0x0002 ))
    IS_PMC_ERRORHANDLING_REJECT_IMAGES                           = _int32(0x01)
    IS_PMC_ERRORHANDLING_IGNORE_MISSING_PARTS                    = _int32(0x02)
    IS_PMC_ERRORHANDLING_MERGE_IMAGES_RELEASE_ON_COMPLETE        = _int32(0x03)
    IS_PMC_ERRORHANDLING_MERGE_IMAGES_RELEASE_ON_RECEIVED_IMGLEN = _int32(0x04)
dMULTICAST={a.name:a.value for a in MULTICAST}
drMULTICAST={a.value:a.name for a in MULTICAST}





##### TYPE DEFINITIONS #####


BOOL=ctypes.c_int
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
ULONG=ctypes.c_ulong
LONGLONG=ctypes.c_int64
LPLONG=ctypes.POINTER(ctypes.c_long)
INT=ctypes.c_int
UINT=ctypes.c_uint
UINT64=ctypes.c_uint64
HANDLE=ctypes.c_void_p
LPHANDLE=ctypes.POINTER(HANDLE)
HWND=ctypes.c_void_p
HGLOBAL=ctypes.c_void_p
HINSTANCE=ctypes.c_void_p
HDC=ctypes.c_void_p
HMODULE=ctypes.c_void_p
HKEY=ctypes.c_void_p
VOID=None
PVOID=ctypes.c_void_p
LPVOID=ctypes.c_void_p
IS_CHAR=ctypes.c_char
HCAM=DWORD
class IS_RANGE_S32(ctypes.Structure):
    _fields_=[  ("s32Min",INT),
                ("s32Max",INT),
                ("s32Inc",INT) ]
PIS_RANGE_S32=ctypes.POINTER(IS_RANGE_S32)
class CIS_RANGE_S32(ctypes_wrap.CStructWrapper):
    _struct=IS_RANGE_S32


class IS_RANGE_F64(ctypes.Structure):
    _fields_=[  ("f64Min",ctypes.c_double),
                ("f64Max",ctypes.c_double),
                ("f64Inc",ctypes.c_double) ]
PIS_RANGE_F64=ctypes.POINTER(IS_RANGE_F64)
class CIS_RANGE_F64(ctypes_wrap.CStructWrapper):
    _struct=IS_RANGE_F64


class BOARDINFO(ctypes.Structure):
    _fields_=[  ("SerNo",ctypes.c_char*12),
                ("ID",ctypes.c_char*20),
                ("Version",ctypes.c_char*10),
                ("Date",ctypes.c_char*12),
                ("Select",ctypes.c_ubyte),
                ("Type",ctypes.c_ubyte),
                ("Reserved",ctypes.c_char*8) ]
PBOARDINFO=ctypes.POINTER(BOARDINFO)
class CBOARDINFO(ctypes_wrap.CStructWrapper):
    _struct=BOARDINFO


PBOARDINFO=ctypes.POINTER(BOARDINFO)
class SENSORINFO(ctypes.Structure):
    _fields_=[  ("SensorID",WORD),
                ("strSensorName",IS_CHAR*32),
                ("nColorMode",ctypes.c_char),
                ("nMaxWidth",DWORD),
                ("nMaxHeight",DWORD),
                ("bMasterGain",BOOL),
                ("bRGain",BOOL),
                ("bGGain",BOOL),
                ("bBGain",BOOL),
                ("bGlobShutter",BOOL),
                ("wPixelSize",WORD),
                ("nUpperLeftBayerPixel",ctypes.c_char),
                ("Reserved",ctypes.c_char*13) ]
PSENSORINFO=ctypes.POINTER(SENSORINFO)
class CSENSORINFO(ctypes_wrap.CStructWrapper):
    _struct=SENSORINFO


PSENSORINFO=ctypes.POINTER(SENSORINFO)
class BAYER_PIXEL(enum.IntEnum):
    BAYER_PIXEL_RED  =_int32(0)
    BAYER_PIXEL_GREEN=_int32(1)
    BAYER_PIXEL_BLUE =_int32(2)
dBAYER_PIXEL={a.name:a.value for a in BAYER_PIXEL}
drBAYER_PIXEL={a.value:a.name for a in BAYER_PIXEL}


class REVISIONINFO(ctypes.Structure):
    _fields_=[  ("size",WORD),
                ("Sensor",WORD),
                ("Cypress",WORD),
                ("Blackfin",DWORD),
                ("DspFirmware",WORD),
                ("USB_Board",WORD),
                ("Sensor_Board",WORD),
                ("Processing_Board",WORD),
                ("Memory_Board",WORD),
                ("Housing",WORD),
                ("Filter",WORD),
                ("Timing_Board",WORD),
                ("Product",WORD),
                ("Power_Board",WORD),
                ("Logic_Board",WORD),
                ("FX3",WORD),
                ("FPGA",WORD),
                ("reserved",BYTE*92) ]
PREVISIONINFO=ctypes.POINTER(REVISIONINFO)
class CREVISIONINFO(ctypes_wrap.CStructWrapper):
    _struct=REVISIONINFO


PREVISIONINFO=ctypes.POINTER(REVISIONINFO)
class UC480_CAPTURE_STATUS(enum.IntEnum):
    IS_CAP_STATUS_API_NO_DEST_MEM         =_int32(0xa2)
    IS_CAP_STATUS_API_CONVERSION_FAILED   =_int32(0xa3)
    IS_CAP_STATUS_API_IMAGE_LOCKED        =_int32(0xa5)
    IS_CAP_STATUS_DRV_OUT_OF_BUFFERS      =_int32(0xb2)
    IS_CAP_STATUS_DRV_DEVICE_NOT_READY    =_int32(0xb4)
    IS_CAP_STATUS_USB_TRANSFER_FAILED     =_int32(0xc7)
    IS_CAP_STATUS_DEV_MISSED_IMAGES       =_int32(0xe5)
    IS_CAP_STATUS_DEV_TIMEOUT             =_int32(0xd6)
    IS_CAP_STATUS_DEV_FRAME_CAPTURE_FAILED=_int32(0xd9)
    IS_CAP_STATUS_ETH_BUFFER_OVERRUN      =_int32(0xe4)
    IS_CAP_STATUS_ETH_MISSED_IMAGES       =_int32(0xe5)
dUC480_CAPTURE_STATUS={a.name:a.value for a in UC480_CAPTURE_STATUS}
drUC480_CAPTURE_STATUS={a.value:a.name for a in UC480_CAPTURE_STATUS}


class UC480_CAPTURE_STATUS_INFO(ctypes.Structure):
    _fields_=[  ("dwCapStatusCnt_Total",DWORD),
                ("reserved",BYTE*60),
                ("adwCapStatusCnt_Detail",DWORD*256) ]
PUC480_CAPTURE_STATUS_INFO=ctypes.POINTER(UC480_CAPTURE_STATUS_INFO)
class CUC480_CAPTURE_STATUS_INFO(ctypes_wrap.CStructWrapper):
    _struct=UC480_CAPTURE_STATUS_INFO


class CAPTURE_STATUS_CMD(enum.IntEnum):
    IS_CAPTURE_STATUS_INFO_CMD_RESET=_int32(1)
    IS_CAPTURE_STATUS_INFO_CMD_GET  =_int32(2)
dCAPTURE_STATUS_CMD={a.name:a.value for a in CAPTURE_STATUS_CMD}
drCAPTURE_STATUS_CMD={a.value:a.name for a in CAPTURE_STATUS_CMD}


class UC480_CAMERA_INFO(ctypes.Structure):
    _fields_=[  ("dwCameraID",DWORD),
                ("dwDeviceID",DWORD),
                ("dwSensorID",DWORD),
                ("dwInUse",DWORD),
                ("SerNo",IS_CHAR*16),
                ("Model",IS_CHAR*16),
                ("dwStatus",DWORD),
                ("dwReserved",DWORD*2),
                ("FullModelName",IS_CHAR*32),
                ("dwReserved2",DWORD*5) ]
PUC480_CAMERA_INFO=ctypes.POINTER(UC480_CAMERA_INFO)
class CUC480_CAMERA_INFO(ctypes_wrap.CStructWrapper):
    _struct=UC480_CAMERA_INFO


PUC480_CAMERA_INFO=ctypes.POINTER(UC480_CAMERA_INFO)
class UC480_CAMERA_LIST(ctypes.Structure):
    _fields_=[  ("dwCount",ULONG),
                ("uci",UC480_CAMERA_INFO*1) ]
PUC480_CAMERA_LIST=ctypes.POINTER(UC480_CAMERA_LIST)
class CUC480_CAMERA_LIST(ctypes_wrap.CStructWrapper):
    _struct=UC480_CAMERA_LIST


PUC480_CAMERA_LIST=ctypes.POINTER(UC480_CAMERA_LIST)
class AUTO_BRIGHT_STATUS(ctypes.Structure):
    _fields_=[  ("curValue",DWORD),
                ("curError",ctypes.c_long),
                ("curController",DWORD),
                ("curCtrlStatus",DWORD) ]
PAUTO_BRIGHT_STATUS=ctypes.POINTER(AUTO_BRIGHT_STATUS)
class CAUTO_BRIGHT_STATUS(ctypes_wrap.CStructWrapper):
    _struct=AUTO_BRIGHT_STATUS


PAUTO_BRIGHT_STATUS=ctypes.POINTER(AUTO_BRIGHT_STATUS)
class AUTO_WB_CHANNNEL_STATUS(ctypes.Structure):
    _fields_=[  ("curValue",DWORD),
                ("curError",ctypes.c_long),
                ("curCtrlStatus",DWORD) ]
PAUTO_WB_CHANNNEL_STATUS=ctypes.POINTER(AUTO_WB_CHANNNEL_STATUS)
class CAUTO_WB_CHANNNEL_STATUS(ctypes_wrap.CStructWrapper):
    _struct=AUTO_WB_CHANNNEL_STATUS


PAUTO_WB_CHANNNEL_STATUS=ctypes.POINTER(AUTO_WB_CHANNNEL_STATUS)
class AUTO_WB_STATUS(ctypes.Structure):
    _fields_=[  ("RedChannel",AUTO_WB_CHANNNEL_STATUS),
                ("GreenChannel",AUTO_WB_CHANNNEL_STATUS),
                ("BlueChannel",AUTO_WB_CHANNNEL_STATUS),
                ("curController",DWORD) ]
PAUTO_WB_STATUS=ctypes.POINTER(AUTO_WB_STATUS)
class CAUTO_WB_STATUS(ctypes_wrap.CStructWrapper):
    _struct=AUTO_WB_STATUS


PAUTO_WB_STATUS=ctypes.POINTER(AUTO_WB_STATUS)
class AUTO_SHUTTER_PHOTOM(enum.IntEnum):
    AS_PM_NONE                =_int32(0)
    AS_PM_SENS_CENTER_WEIGHTED=_int32(0x00000001)
    AS_PM_SENS_CENTER_SPOT    =_int32(0x00000002)
    AS_PM_SENS_PORTRAIT       =_int32(0x00000004)
    AS_PM_SENS_LANDSCAPE      =_int32(0x00000008)
    AS_PM_SENS_CENTER_AVERAGE =_int32(0x00000010)
dAUTO_SHUTTER_PHOTOM={a.name:a.value for a in AUTO_SHUTTER_PHOTOM}
drAUTO_SHUTTER_PHOTOM={a.value:a.name for a in AUTO_SHUTTER_PHOTOM}


class AUTO_GAIN_PHOTOM(enum.IntEnum):
    AG_PM_NONE                =_int32(0)
    AG_PM_SENS_CENTER_WEIGHTED=_int32(0x00000001)
    AG_PM_SENS_CENTER_SPOT    =_int32(0x00000002)
    AG_PM_SENS_PORTRAIT       =_int32(0x00000004)
    AG_PM_SENS_LANDSCAPE      =_int32(0x00000008)
dAUTO_GAIN_PHOTOM={a.name:a.value for a in AUTO_GAIN_PHOTOM}
drAUTO_GAIN_PHOTOM={a.value:a.name for a in AUTO_GAIN_PHOTOM}


class ANTI_FLICKER_MODE(enum.IntEnum):
    ANTIFLCK_MODE_OFF          =_int32(0)
    ANTIFLCK_MODE_SENS_AUTO    =_int32(0x00000001)
    ANTIFLCK_MODE_SENS_50_FIXED=_int32(0x00000002)
    ANTIFLCK_MODE_SENS_60_FIXED=_int32(0x00000004)
dANTI_FLICKER_MODE={a.name:a.value for a in ANTI_FLICKER_MODE}
drANTI_FLICKER_MODE={a.value:a.name for a in ANTI_FLICKER_MODE}


class WHITEBALANCE_MODE(enum.IntEnum):
    WB_MODE_DISABLE          =_int32(0)
    WB_MODE_AUTO             =_int32(0x00000001)
    WB_MODE_ALL_PULLIN       =_int32(0x00000002)
    WB_MODE_INCANDESCENT_LAMP=_int32(0x00000004)
    WB_MODE_FLUORESCENT_DL   =_int32(0x00000008)
    WB_MODE_OUTDOOR_CLEAR_SKY=_int32(0x00000010)
    WB_MODE_OUTDOOR_CLOUDY   =_int32(0x00000020)
    WB_MODE_FLUORESCENT_LAMP =_int32(0x00000040)
    WB_MODE_FLUORESCENT_NL   =_int32(0x00000080)
dWHITEBALANCE_MODE={a.name:a.value for a in WHITEBALANCE_MODE}
drWHITEBALANCE_MODE={a.value:a.name for a in WHITEBALANCE_MODE}


class UC480_AUTO_INFO(ctypes.Structure):
    _fields_=[  ("AutoAbility",DWORD),
                ("sBrightCtrlStatus",AUTO_BRIGHT_STATUS),
                ("sWBCtrlStatus",AUTO_WB_STATUS),
                ("AShutterPhotomCaps",DWORD),
                ("AGainPhotomCaps",DWORD),
                ("AAntiFlickerCaps",DWORD),
                ("SensorWBModeCaps",DWORD),
                ("reserved",DWORD*8) ]
PUC480_AUTO_INFO=ctypes.POINTER(UC480_AUTO_INFO)
class CUC480_AUTO_INFO(ctypes_wrap.CStructWrapper):
    _struct=UC480_AUTO_INFO


PUC480_AUTO_INFO=ctypes.POINTER(UC480_AUTO_INFO)
class DC_INFO(ctypes.Structure):
    _fields_=[  ("nSize",ctypes.c_uint),
                ("hDC",HDC),
                ("nCx",ctypes.c_uint),
                ("nCy",ctypes.c_uint) ]
PDC_INFO=ctypes.POINTER(DC_INFO)
class CDC_INFO(ctypes_wrap.CStructWrapper):
    _struct=DC_INFO


PDC_INFO=ctypes.POINTER(DC_INFO)
class KNEEPOINT(ctypes.Structure):
    _fields_=[  ("x",ctypes.c_double),
                ("y",ctypes.c_double) ]
PKNEEPOINT=ctypes.POINTER(KNEEPOINT)
class CKNEEPOINT(ctypes_wrap.CStructWrapper):
    _struct=KNEEPOINT


PKNEEPOINT=ctypes.c_void_p
class KNEEPOINTARRAY(ctypes.Structure):
    _fields_=[  ("NumberOfUsedKneepoints",INT),
                ("Kneepoint",KNEEPOINT*10) ]
PKNEEPOINTARRAY=ctypes.POINTER(KNEEPOINTARRAY)
class CKNEEPOINTARRAY(ctypes_wrap.CStructWrapper):
    _struct=KNEEPOINTARRAY


PKNEEPOINTARRAY=ctypes.c_void_p
class KNEEPOINTINFO(ctypes.Structure):
    _fields_=[  ("NumberOfSupportedKneepoints",INT),
                ("NumberOfUsedKneepoints",INT),
                ("MinValueX",ctypes.c_double),
                ("MaxValueX",ctypes.c_double),
                ("MinValueY",ctypes.c_double),
                ("MaxValueY",ctypes.c_double),
                ("DefaultKneepoint",KNEEPOINT*10),
                ("Reserved",INT*10) ]
PKNEEPOINTINFO=ctypes.POINTER(KNEEPOINTINFO)
class CKNEEPOINTINFO(ctypes_wrap.CStructWrapper):
    _struct=KNEEPOINTINFO


PKNEEPOINTINFO=ctypes.c_void_p
class UC480_GET_ESTIMATED_TIME_MODE(enum.IntEnum):
    IS_SE_STARTER_FW_UPLOAD=_int32(0x00000001)
    IS_CP_STARTER_FW_UPLOAD=_int32(0x00000002)
    IS_STARTER_FW_UPLOAD   =_int32(0x00000004)
dUC480_GET_ESTIMATED_TIME_MODE={a.name:a.value for a in UC480_GET_ESTIMATED_TIME_MODE}
drUC480_GET_ESTIMATED_TIME_MODE={a.value:a.name for a in UC480_GET_ESTIMATED_TIME_MODE}


class SENSORSCALERINFO(ctypes.Structure):
    _fields_=[  ("nCurrMode",INT),
                ("nNumberOfSteps",INT),
                ("dblFactorIncrement",ctypes.c_double),
                ("dblMinFactor",ctypes.c_double),
                ("dblMaxFactor",ctypes.c_double),
                ("dblCurrFactor",ctypes.c_double),
                ("nSupportedModes",INT),
                ("bReserved",BYTE*84) ]
PSENSORSCALERINFO=ctypes.POINTER(SENSORSCALERINFO)
class CSENSORSCALERINFO(ctypes_wrap.CStructWrapper):
    _struct=SENSORSCALERINFO


class UC480TIME(ctypes.Structure):
    _fields_=[  ("wYear",WORD),
                ("wMonth",WORD),
                ("wDay",WORD),
                ("wHour",WORD),
                ("wMinute",WORD),
                ("wSecond",WORD),
                ("wMilliseconds",WORD),
                ("byReserved",BYTE*10) ]
PUC480TIME=ctypes.POINTER(UC480TIME)
class CUC480TIME(ctypes_wrap.CStructWrapper):
    _struct=UC480TIME


class UC480IMAGEINFO(ctypes.Structure):
    _fields_=[  ("dwFlags",DWORD),
                ("byReserved1",BYTE*4),
                ("u64TimestampDevice",UINT64),
                ("TimestampSystem",UC480TIME),
                ("dwIoStatus",DWORD),
                ("wAOIIndex",WORD),
                ("wAOICycle",WORD),
                ("u64FrameNumber",UINT64),
                ("dwImageBuffers",DWORD),
                ("dwImageBuffersInUse",DWORD),
                ("dwReserved3",DWORD),
                ("dwImageHeight",DWORD),
                ("dwImageWidth",DWORD),
                ("dwHostProcessTime",DWORD) ]
PUC480IMAGEINFO=ctypes.POINTER(UC480IMAGEINFO)
class CUC480IMAGEINFO(ctypes_wrap.CStructWrapper):
    _struct=UC480IMAGEINFO


class IMAGE_FORMAT_CMD(enum.IntEnum):
    IMGFRMT_CMD_GET_NUM_ENTRIES            =_int32(1)
    IMGFRMT_CMD_GET_LIST                   =_int32(2)
    IMGFRMT_CMD_SET_FORMAT                 =_int32(3)
    IMGFRMT_CMD_GET_ARBITRARY_AOI_SUPPORTED=_int32(4)
    IMGFRMT_CMD_GET_FORMAT_INFO            =_int32(5)
dIMAGE_FORMAT_CMD={a.name:a.value for a in IMAGE_FORMAT_CMD}
drIMAGE_FORMAT_CMD={a.value:a.name for a in IMAGE_FORMAT_CMD}


class CAPTUREMODE(enum.IntEnum):
    CAPTMODE_FREERUN                =_int32(0x00000001)
    CAPTMODE_SINGLE                 =_int32(0x00000002)
    CAPTMODE_TRIGGER_SOFT_SINGLE    =_int32(0x00000010)
    CAPTMODE_TRIGGER_SOFT_CONTINUOUS=_int32(0x00000020)
    CAPTMODE_TRIGGER_HW_SINGLE      =_int32(0x00000100)
    CAPTMODE_TRIGGER_HW_CONTINUOUS  =_int32(0x00000200)
dCAPTUREMODE={a.name:a.value for a in CAPTUREMODE}
drCAPTUREMODE={a.value:a.name for a in CAPTUREMODE}


class IMAGE_FORMAT_INFO(ctypes.Structure):
    _fields_=[  ("nFormatID",INT),
                ("nWidth",UINT),
                ("nHeight",UINT),
                ("nX0",INT),
                ("nY0",INT),
                ("nSupportedCaptureModes",UINT),
                ("nBinningMode",UINT),
                ("nSubsamplingMode",UINT),
                ("strFormatName",IS_CHAR*64),
                ("dSensorScalerFactor",ctypes.c_double),
                ("nReserved",UINT*22) ]
PIMAGE_FORMAT_INFO=ctypes.POINTER(IMAGE_FORMAT_INFO)
class CIMAGE_FORMAT_INFO(ctypes_wrap.CStructWrapper):
    _struct=IMAGE_FORMAT_INFO


class IMAGE_FORMAT_LIST(ctypes.Structure):
    _fields_=[  ("nSizeOfListEntry",UINT),
                ("nNumListElements",UINT),
                ("nReserved",UINT*4),
                ("FormatInfo",IMAGE_FORMAT_INFO*1) ]
PIMAGE_FORMAT_LIST=ctypes.POINTER(IMAGE_FORMAT_LIST)
class CIMAGE_FORMAT_LIST(ctypes_wrap.CStructWrapper):
    _struct=IMAGE_FORMAT_LIST


class FDT_CAPABILITY_FLAGS(enum.IntEnum):
    FDT_CAP_INVALID           =_int32(0)
    FDT_CAP_SUPPORTED         =_int32(0x00000001)
    FDT_CAP_SEARCH_ANGLE      =_int32(0x00000002)
    FDT_CAP_SEARCH_AOI        =_int32(0x00000004)
    FDT_CAP_INFO_POSX         =_int32(0x00000010)
    FDT_CAP_INFO_POSY         =_int32(0x00000020)
    FDT_CAP_INFO_WIDTH        =_int32(0x00000040)
    FDT_CAP_INFO_HEIGHT       =_int32(0x00000080)
    FDT_CAP_INFO_ANGLE        =_int32(0x00000100)
    FDT_CAP_INFO_POSTURE      =_int32(0x00000200)
    FDT_CAP_INFO_FACENUMBER   =_int32(0x00000400)
    FDT_CAP_INFO_OVL          =_int32(0x00000800)
    FDT_CAP_INFO_NUM_OVL      =_int32(0x00001000)
    FDT_CAP_INFO_OVL_LINEWIDTH=_int32(0x00002000)
dFDT_CAPABILITY_FLAGS={a.name:a.value for a in FDT_CAPABILITY_FLAGS}
drFDT_CAPABILITY_FLAGS={a.value:a.name for a in FDT_CAPABILITY_FLAGS}


class FDT_INFO_EL(ctypes.Structure):
    _fields_=[  ("nFacePosX",INT),
                ("nFacePosY",INT),
                ("nFaceWidth",INT),
                ("nFaceHeight",INT),
                ("nAngle",INT),
                ("nPosture",UINT),
                ("TimestampSystem",UC480TIME),
                ("nReserved",UINT64),
                ("nReserved2",UINT*4) ]
PFDT_INFO_EL=ctypes.POINTER(FDT_INFO_EL)
class CFDT_INFO_EL(ctypes_wrap.CStructWrapper):
    _struct=FDT_INFO_EL


class FDT_INFO_LIST(ctypes.Structure):
    _fields_=[  ("nSizeOfListEntry",UINT),
                ("nNumDetectedFaces",UINT),
                ("nNumListElements",UINT),
                ("nReserved",UINT*4),
                ("FaceEntry",FDT_INFO_EL*1) ]
PFDT_INFO_LIST=ctypes.POINTER(FDT_INFO_LIST)
class CFDT_INFO_LIST(ctypes_wrap.CStructWrapper):
    _struct=FDT_INFO_LIST


class FDT_CMD(enum.IntEnum):
    FDT_CMD_GET_CAPABILITIES         =_int32(0)
    FDT_CMD_SET_DISABLE              =_int32(1)
    FDT_CMD_SET_ENABLE               =_int32(2)
    FDT_CMD_SET_SEARCH_ANGLE         =_int32(3)
    FDT_CMD_GET_SEARCH_ANGLE         =_int32(4)
    FDT_CMD_SET_SEARCH_ANGLE_ENABLE  =_int32(5)
    FDT_CMD_SET_SEARCH_ANGLE_DISABLE =_int32(6)
    FDT_CMD_GET_SEARCH_ANGLE_ENABLE  =_int32(7)
    FDT_CMD_SET_SEARCH_AOI           =_int32(8)
    FDT_CMD_GET_SEARCH_AOI           =_int32(9)
    FDT_CMD_GET_FACE_LIST            =_int32(10)
    FDT_CMD_GET_NUMBER_FACES         =_int32(11)
    FDT_CMD_SET_SUSPEND              =_int32(12)
    FDT_CMD_SET_RESUME               =_int32(13)
    FDT_CMD_GET_MAX_NUM_FACES        =_int32(14)
    FDT_CMD_SET_INFO_MAX_NUM_OVL     =_int32(15)
    FDT_CMD_GET_INFO_MAX_NUM_OVL     =_int32(16)
    FDT_CMD_SET_INFO_OVL_LINE_WIDTH  =_int32(17)
    FDT_CMD_GET_INFO_OVL_LINE_WIDTH  =_int32(18)
    FDT_CMD_GET_ENABLE               =_int32(19)
    FDT_CMD_GET_SUSPEND              =_int32(20)
    FDT_CMD_GET_HORIZONTAL_RESOLUTION=_int32(21)
    FDT_CMD_GET_VERTICAL_RESOLUTION  =_int32(22)
dFDT_CMD={a.name:a.value for a in FDT_CMD}
drFDT_CMD={a.value:a.name for a in FDT_CMD}


class FOCUS_CAPABILITY_FLAGS(enum.IntEnum):
    FOC_CAP_INVALID            =_int32(0)
    FOC_CAP_AUTOFOCUS_SUPPORTED=_int32(0x00000001)
    FOC_CAP_MANUAL_SUPPORTED   =_int32(0x00000002)
    FOC_CAP_GET_DISTANCE       =_int32(0x00000004)
    FOC_CAP_SET_AUTOFOCUS_RANGE=_int32(0x00000008)
    FOC_CAP_AUTOFOCUS_FDT_AOI  =_int32(0x00000010)
    FOC_CAP_AUTOFOCUS_ZONE     =_int32(0x00000020)
dFOCUS_CAPABILITY_FLAGS={a.name:a.value for a in FOCUS_CAPABILITY_FLAGS}
drFOCUS_CAPABILITY_FLAGS={a.value:a.name for a in FOCUS_CAPABILITY_FLAGS}


class FOCUS_RANGE(enum.IntEnum):
    FOC_RANGE_NORMAL  =_int32(0x00000001)
    FOC_RANGE_ALLRANGE=_int32(0x00000002)
    FOC_RANGE_MACRO   =_int32(0x00000004)
dFOCUS_RANGE={a.name:a.value for a in FOCUS_RANGE}
drFOCUS_RANGE={a.value:a.name for a in FOCUS_RANGE}


class FOCUS_STATUS(enum.IntEnum):
    FOC_STATUS_UNDEFINED=_int32(0x00000000)
    FOC_STATUS_ERROR    =_int32(0x00000001)
    FOC_STATUS_FOCUSED  =_int32(0x00000002)
    FOC_STATUS_FOCUSING =_int32(0x00000004)
    FOC_STATUS_TIMEOUT  =_int32(0x00000008)
    FOC_STATUS_CANCEL   =_int32(0x00000010)
dFOCUS_STATUS={a.name:a.value for a in FOCUS_STATUS}
drFOCUS_STATUS={a.value:a.name for a in FOCUS_STATUS}


class FOCUS_ZONE_WEIGHT(enum.IntEnum):
    FOC_ZONE_WEIGHT_DISABLE=_int32(0)
    FOC_ZONE_WEIGHT_WEAK   =_int32(0x0021)
    FOC_ZONE_WEIGHT_MIDDLE =_int32(0x0032)
    FOC_ZONE_WEIGHT_STRONG =_int32(0x0042)
dFOCUS_ZONE_WEIGHT={a.name:a.value for a in FOCUS_ZONE_WEIGHT}
drFOCUS_ZONE_WEIGHT={a.value:a.name for a in FOCUS_ZONE_WEIGHT}


class FOCUS_ZONE_AOI_PRESET(enum.IntEnum):
    FOC_ZONE_AOI_PRESET_CENTER       =_int32(0)
    FOC_ZONE_AOI_PRESET_UPPER_LEFT   =_int32(0x0001)
    FOC_ZONE_AOI_PRESET_BOTTOM_LEFT  =_int32(0x0002)
    FOC_ZONE_AOI_PRESET_UPPER_RIGHT  =_int32(0x0004)
    FOC_ZONE_AOI_PRESET_BOTTOM_RIGHT =_int32(0x0008)
    FOC_ZONE_AOI_PRESET_UPPER_CENTER =_int32(0x0010)
    FOC_ZONE_AOI_PRESET_BOTTOM_CENTER=_int32(0x0020)
    FOC_ZONE_AOI_PRESET_CENTER_LEFT  =_int32(0x0040)
    FOC_ZONE_AOI_PRESET_CENTER_RIGHT =_int32(0x0080)
dFOCUS_ZONE_AOI_PRESET={a.name:a.value for a in FOCUS_ZONE_AOI_PRESET}
drFOCUS_ZONE_AOI_PRESET={a.value:a.name for a in FOCUS_ZONE_AOI_PRESET}


class FOCUS_CMD(enum.IntEnum):
    FOC_CMD_GET_CAPABILITIES                          =_int32(0)
    FOC_CMD_SET_DISABLE_AUTOFOCUS                     =_int32(1)
    FOC_CMD_SET_ENABLE_AUTOFOCUS                      =_int32(2)
    FOC_CMD_GET_AUTOFOCUS_ENABLE                      =_int32(3)
    FOC_CMD_SET_AUTOFOCUS_RANGE                       =_int32(4)
    FOC_CMD_GET_AUTOFOCUS_RANGE                       =_int32(5)
    FOC_CMD_GET_DISTANCE                              =_int32(6)
    FOC_CMD_SET_MANUAL_FOCUS                          =_int32(7)
    FOC_CMD_GET_MANUAL_FOCUS                          =_int32(8)
    FOC_CMD_GET_MANUAL_FOCUS_MIN                      =_int32(9)
    FOC_CMD_GET_MANUAL_FOCUS_MAX                      =_int32(10)
    FOC_CMD_GET_MANUAL_FOCUS_INC                      =_int32(11)
    FOC_CMD_SET_ENABLE_AF_FDT_AOI                     =_int32(12)
    FOC_CMD_SET_DISABLE_AF_FDT_AOI                    =_int32(13)
    FOC_CMD_GET_AF_FDT_AOI_ENABLE                     =_int32(14)
    FOC_CMD_SET_ENABLE_AUTOFOCUS_ONCE                 =_int32(15)
    FOC_CMD_GET_AUTOFOCUS_STATUS                      =_int32(16)
    FOC_CMD_SET_AUTOFOCUS_ZONE_AOI                    =_int32(17)
    FOC_CMD_GET_AUTOFOCUS_ZONE_AOI                    =_int32(18)
    FOC_CMD_GET_AUTOFOCUS_ZONE_AOI_DEFAULT            =_int32(19)
    FOC_CMD_GET_AUTOFOCUS_ZONE_POS_MIN                =_int32(20)
    FOC_CMD_GET_AUTOFOCUS_ZONE_POS_MAX                =_int32(21)
    FOC_CMD_GET_AUTOFOCUS_ZONE_POS_INC                =_int32(22)
    FOC_CMD_GET_AUTOFOCUS_ZONE_SIZE_MIN               =_int32(23)
    FOC_CMD_GET_AUTOFOCUS_ZONE_SIZE_MAX               =_int32(24)
    FOC_CMD_GET_AUTOFOCUS_ZONE_SIZE_INC               =_int32(25)
    FOC_CMD_SET_AUTOFOCUS_ZONE_WEIGHT                 =_int32(26)
    FOC_CMD_GET_AUTOFOCUS_ZONE_WEIGHT                 =_int32(27)
    FOC_CMD_GET_AUTOFOCUS_ZONE_WEIGHT_COUNT           =_int32(28)
    FOC_CMD_GET_AUTOFOCUS_ZONE_WEIGHT_DEFAULT         =_int32(29)
    FOC_CMD_SET_AUTOFOCUS_ZONE_AOI_PRESET             =_int32(30)
    FOC_CMD_GET_AUTOFOCUS_ZONE_AOI_PRESET             =_int32(31)
    FOC_CMD_GET_AUTOFOCUS_ZONE_AOI_PRESET_DEFAULT     =_int32(32)
    FOC_CMD_GET_AUTOFOCUS_ZONE_ARBITRARY_AOI_SUPPORTED=_int32(33)
    FOC_CMD_SET_MANUAL_FOCUS_RELATIVE                 =_int32(34)
dFOCUS_CMD={a.name:a.value for a in FOCUS_CMD}
drFOCUS_CMD={a.value:a.name for a in FOCUS_CMD}


class IMGSTAB_CAPABILITY_FLAGS(enum.IntEnum):
    IMGSTAB_CAP_INVALID                      =_int32(0)
    IMGSTAB_CAP_IMAGE_STABILIZATION_SUPPORTED=_int32(0x00000001)
dIMGSTAB_CAPABILITY_FLAGS={a.name:a.value for a in IMGSTAB_CAPABILITY_FLAGS}
drIMGSTAB_CAPABILITY_FLAGS={a.value:a.name for a in IMGSTAB_CAPABILITY_FLAGS}


class IMGSTAB_CMD(enum.IntEnum):
    IMGSTAB_CMD_GET_CAPABILITIES=_int32(0)
    IMGSTAB_CMD_SET_DISABLE     =_int32(1)
    IMGSTAB_CMD_SET_ENABLE      =_int32(2)
    IMGSTAB_CMD_GET_ENABLE      =_int32(3)
dIMGSTAB_CMD={a.name:a.value for a in IMGSTAB_CMD}
drIMGSTAB_CMD={a.value:a.name for a in IMGSTAB_CMD}


class SCENE_CMD(enum.IntEnum):
    SCENE_CMD_GET_SUPPORTED_PRESETS=_int32(1)
    SCENE_CMD_SET_PRESET           =_int32(2)
    SCENE_CMD_GET_PRESET           =_int32(3)
    SCENE_CMD_GET_DEFAULT_PRESET   =_int32(4)
dSCENE_CMD={a.name:a.value for a in SCENE_CMD}
drSCENE_CMD={a.value:a.name for a in SCENE_CMD}


class SCENE_PRESET(enum.IntEnum):
    SCENE_INVALID             =_int32(0)
    SCENE_SENSOR_AUTOMATIC    =_int32(0x00000001)
    SCENE_SENSOR_PORTRAIT     =_int32(0x00000002)
    SCENE_SENSOR_SUNNY        =_int32(0x00000004)
    SCENE_SENSOR_ENTERTAINMENT=_int32(0x00000008)
    SCENE_SENSOR_NIGHT        =_int32(0x00000010)
    SCENE_SENSOR_SPORTS       =_int32(0x00000040)
    SCENE_SENSOR_LANDSCAPE    =_int32(0x00000080)
dSCENE_PRESET={a.name:a.value for a in SCENE_PRESET}
drSCENE_PRESET={a.value:a.name for a in SCENE_PRESET}


class ZOOM_CMD(enum.IntEnum):
    ZOOM_CMD_GET_CAPABILITIES            =_int32(0)
    ZOOM_CMD_DIGITAL_GET_NUM_LIST_ENTRIES=_int32(1)
    ZOOM_CMD_DIGITAL_GET_LIST            =_int32(2)
    ZOOM_CMD_DIGITAL_SET_VALUE           =_int32(3)
    ZOOM_CMD_DIGITAL_GET_VALUE           =_int32(4)
    ZOOM_CMD_DIGITAL_GET_VALUE_RANGE     =_int32(5)
    ZOOM_CMD_DIGITAL_GET_VALUE_DEFAULT   =_int32(6)
dZOOM_CMD={a.name:a.value for a in ZOOM_CMD}
drZOOM_CMD={a.value:a.name for a in ZOOM_CMD}


class ZOOM_CAPABILITY_FLAGS(enum.IntEnum):
    ZOOM_CAP_INVALID     =_int32(0)
    ZOOM_CAP_DIGITAL_ZOOM=_int32(0x00001)
dZOOM_CAPABILITY_FLAGS={a.name:a.value for a in ZOOM_CAPABILITY_FLAGS}
drZOOM_CAPABILITY_FLAGS={a.value:a.name for a in ZOOM_CAPABILITY_FLAGS}


class SHARPNESS_CMD(enum.IntEnum):
    SHARPNESS_CMD_GET_CAPABILITIES =_int32(0)
    SHARPNESS_CMD_GET_VALUE        =_int32(1)
    SHARPNESS_CMD_GET_MIN_VALUE    =_int32(2)
    SHARPNESS_CMD_GET_MAX_VALUE    =_int32(3)
    SHARPNESS_CMD_GET_INCREMENT    =_int32(4)
    SHARPNESS_CMD_GET_DEFAULT_VALUE=_int32(5)
    SHARPNESS_CMD_SET_VALUE        =_int32(6)
dSHARPNESS_CMD={a.name:a.value for a in SHARPNESS_CMD}
drSHARPNESS_CMD={a.value:a.name for a in SHARPNESS_CMD}


class SHARPNESS_CAPABILITY_FLAGS(enum.IntEnum):
    SHARPNESS_CAP_INVALID            =_int32(0x0000)
    SHARPNESS_CAP_SHARPNESS_SUPPORTED=_int32(0x0001)
dSHARPNESS_CAPABILITY_FLAGS={a.name:a.value for a in SHARPNESS_CAPABILITY_FLAGS}
drSHARPNESS_CAPABILITY_FLAGS={a.value:a.name for a in SHARPNESS_CAPABILITY_FLAGS}


class SATURATION_CMD(enum.IntEnum):
    SATURATION_CMD_GET_CAPABILITIES =_int32(0)
    SATURATION_CMD_GET_VALUE        =_int32(1)
    SATURATION_CMD_GET_MIN_VALUE    =_int32(2)
    SATURATION_CMD_GET_MAX_VALUE    =_int32(3)
    SATURATION_CMD_GET_INCREMENT    =_int32(4)
    SATURATION_CMD_GET_DEFAULT_VALUE=_int32(5)
    SATURATION_CMD_SET_VALUE        =_int32(6)
dSATURATION_CMD={a.name:a.value for a in SATURATION_CMD}
drSATURATION_CMD={a.value:a.name for a in SATURATION_CMD}


class SATURATION_CAPABILITY_FLAGS(enum.IntEnum):
    SATURATION_CAP_INVALID             =_int32(0x0000)
    SATURATION_CAP_SATURATION_SUPPORTED=_int32(0x0001)
dSATURATION_CAPABILITY_FLAGS={a.name:a.value for a in SATURATION_CAPABILITY_FLAGS}
drSATURATION_CAPABILITY_FLAGS={a.value:a.name for a in SATURATION_CAPABILITY_FLAGS}


class TRIGGER_DEBOUNCE_MODE(enum.IntEnum):
    TRIGGER_DEBOUNCE_MODE_NONE        =_int32(0x0000)
    TRIGGER_DEBOUNCE_MODE_FALLING_EDGE=_int32(0x0001)
    TRIGGER_DEBOUNCE_MODE_RISING_EDGE =_int32(0x0002)
    TRIGGER_DEBOUNCE_MODE_BOTH_EDGES  =_int32(0x0004)
    TRIGGER_DEBOUNCE_MODE_AUTOMATIC   =_int32(0x0008)
dTRIGGER_DEBOUNCE_MODE={a.name:a.value for a in TRIGGER_DEBOUNCE_MODE}
drTRIGGER_DEBOUNCE_MODE={a.value:a.name for a in TRIGGER_DEBOUNCE_MODE}


class TRIGGER_DEBOUNCE_CMD(enum.IntEnum):
    TRIGGER_DEBOUNCE_CMD_SET_MODE              =_int32(0)
    TRIGGER_DEBOUNCE_CMD_SET_DELAY_TIME        =_int32(1)
    TRIGGER_DEBOUNCE_CMD_GET_SUPPORTED_MODES   =_int32(2)
    TRIGGER_DEBOUNCE_CMD_GET_MODE              =_int32(3)
    TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME        =_int32(4)
    TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_MIN    =_int32(5)
    TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_MAX    =_int32(6)
    TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_INC    =_int32(7)
    TRIGGER_DEBOUNCE_CMD_GET_MODE_DEFAULT      =_int32(8)
    TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_DEFAULT=_int32(9)
dTRIGGER_DEBOUNCE_CMD={a.name:a.value for a in TRIGGER_DEBOUNCE_CMD}
drTRIGGER_DEBOUNCE_CMD={a.value:a.name for a in TRIGGER_DEBOUNCE_CMD}


class RGB_COLOR_MODELS(enum.IntEnum):
    RGB_COLOR_MODEL_SRGB_D50     =_int32(0x0001)
    RGB_COLOR_MODEL_SRGB_D65     =_int32(0x0002)
    RGB_COLOR_MODEL_CIE_RGB_E    =_int32(0x0004)
    RGB_COLOR_MODEL_ECI_RGB_D50  =_int32(0x0008)
    RGB_COLOR_MODEL_ADOBE_RGB_D65=_int32(0x0010)
dRGB_COLOR_MODELS={a.name:a.value for a in RGB_COLOR_MODELS}
drRGB_COLOR_MODELS={a.value:a.name for a in RGB_COLOR_MODELS}


class LENS_SHADING_MODELS(enum.IntEnum):
    LSC_MODEL_AGL =_int32(0x0001)
    LSC_MODEL_TL84=_int32(0x0002)
    LSC_MODEL_D50 =_int32(0x0004)
    LSC_MODEL_D65 =_int32(0x0008)
dLENS_SHADING_MODELS={a.name:a.value for a in LENS_SHADING_MODELS}
drLENS_SHADING_MODELS={a.value:a.name for a in LENS_SHADING_MODELS}


class COLOR_TEMPERATURE_CMD(enum.IntEnum):
    COLOR_TEMPERATURE_CMD_SET_TEMPERATURE                 =_int32(0)
    COLOR_TEMPERATURE_CMD_SET_RGB_COLOR_MODEL             =_int32(1)
    COLOR_TEMPERATURE_CMD_GET_SUPPORTED_RGB_COLOR_MODELS  =_int32(2)
    COLOR_TEMPERATURE_CMD_GET_TEMPERATURE                 =_int32(3)
    COLOR_TEMPERATURE_CMD_GET_RGB_COLOR_MODEL             =_int32(4)
    COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_MIN             =_int32(5)
    COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_MAX             =_int32(6)
    COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_INC             =_int32(7)
    COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_DEFAULT         =_int32(8)
    COLOR_TEMPERATURE_CMD_GET_RGB_COLOR_MODEL_DEFAULT     =_int32(9)
    COLOR_TEMPERATURE_CMD_SET_LENS_SHADING_MODEL          =_int32(10)
    COLOR_TEMPERATURE_CMD_GET_LENS_SHADING_MODEL          =_int32(11)
    COLOR_TEMPERATURE_CMD_GET_LENS_SHADING_MODEL_SUPPORTED=_int32(12)
    COLOR_TEMPERATURE_CMD_GET_LENS_SHADING_MODEL_DEFAULT  =_int32(13)
dCOLOR_TEMPERATURE_CMD={a.name:a.value for a in COLOR_TEMPERATURE_CMD}
drCOLOR_TEMPERATURE_CMD={a.value:a.name for a in COLOR_TEMPERATURE_CMD}


class OPENGL_DISPLAY(ctypes.Structure):
    _fields_=[  ("nWindowID",ctypes.c_int),
                ("pDisplay",ctypes.c_void_p) ]
POPENGL_DISPLAY=ctypes.POINTER(OPENGL_DISPLAY)
class COPENGL_DISPLAY(ctypes_wrap.CStructWrapper):
    _struct=OPENGL_DISPLAY


class IS_POINT_2D(ctypes.Structure):
    _fields_=[  ("s32X",INT),
                ("s32Y",INT) ]
PIS_POINT_2D=ctypes.POINTER(IS_POINT_2D)
class CIS_POINT_2D(ctypes_wrap.CStructWrapper):
    _struct=IS_POINT_2D


class IS_SIZE_2D(ctypes.Structure):
    _fields_=[  ("s32Width",INT),
                ("s32Height",INT) ]
PIS_SIZE_2D=ctypes.POINTER(IS_SIZE_2D)
class CIS_SIZE_2D(ctypes_wrap.CStructWrapper):
    _struct=IS_SIZE_2D


class IS_RECT(ctypes.Structure):
    _fields_=[  ("s32X",INT),
                ("s32Y",INT),
                ("s32Width",INT),
                ("s32Height",INT) ]
PIS_RECT=ctypes.POINTER(IS_RECT)
class CIS_RECT(ctypes_wrap.CStructWrapper):
    _struct=IS_RECT


class AOI_SEQUENCE_PARAMS(ctypes.Structure):
    _fields_=[  ("s32AOIIndex",INT),
                ("s32NumberOfCycleRepetitions",INT),
                ("s32X",INT),
                ("s32Y",INT),
                ("dblExposure",ctypes.c_double),
                ("s32Gain",INT),
                ("s32BinningMode",INT),
                ("s32SubsamplingMode",INT),
                ("s32DetachImageParameters",INT),
                ("dblScalerFactor",ctypes.c_double),
                ("byReserved",BYTE*64) ]
PAOI_SEQUENCE_PARAMS=ctypes.POINTER(AOI_SEQUENCE_PARAMS)
class CAOI_SEQUENCE_PARAMS(ctypes_wrap.CStructWrapper):
    _struct=AOI_SEQUENCE_PARAMS


class RANGE_OF_VALUES_U32(ctypes.Structure):
    _fields_=[  ("u32Minimum",UINT),
                ("u32Maximum",UINT),
                ("u32Increment",UINT),
                ("u32Default",UINT),
                ("u32Infinite",UINT) ]
PRANGE_OF_VALUES_U32=ctypes.POINTER(RANGE_OF_VALUES_U32)
class CRANGE_OF_VALUES_U32(ctypes_wrap.CStructWrapper):
    _struct=RANGE_OF_VALUES_U32


class TRANSFER_CAPABILITY_FLAGS(enum.IntEnum):
    TRANSFER_CAP_IMAGEDELAY    =_int32(0x01)
    TRANSFER_CAP_PACKETINTERVAL=_int32(0x20)
dTRANSFER_CAPABILITY_FLAGS={a.name:a.value for a in TRANSFER_CAPABILITY_FLAGS}
drTRANSFER_CAPABILITY_FLAGS={a.value:a.name for a in TRANSFER_CAPABILITY_FLAGS}


class TRANSFER_CMD(enum.IntEnum):
    TRANSFER_CMD_QUERY_CAPABILITIES                =_int32(0)
    TRANSFER_CMD_SET_IMAGEDELAY_US                 =_int32(1000)
    TRANSFER_CMD_SET_PACKETINTERVAL_US             =_int32(1005)
    TRANSFER_CMD_GET_IMAGEDELAY_US                 =_int32(2000)
    TRANSFER_CMD_GET_PACKETINTERVAL_US             =_int32(2005)
    TRANSFER_CMD_GETRANGE_IMAGEDELAY_US            =_int32(3000)
    TRANSFER_CMD_GETRANGE_PACKETINTERVAL_US        =_int32(3005)
    TRANSFER_CMD_SET_IMAGE_DESTINATION             =_int32(5000)
    TRANSFER_CMD_GET_IMAGE_DESTINATION             =_int32(5001)
    TRANSFER_CMD_GET_IMAGE_DESTINATION_CAPABILITIES=_int32(5002)
dTRANSFER_CMD={a.name:a.value for a in TRANSFER_CMD}
drTRANSFER_CMD={a.value:a.name for a in TRANSFER_CMD}


class TRANSFER_TARGET(enum.IntEnum):
    IS_TRANSFER_DESTINATION_DEVICE_MEMORY=_int32(1)
    IS_TRANSFER_DESTINATION_USER_MEMORY  =_int32(2)
dTRANSFER_TARGET={a.name:a.value for a in TRANSFER_TARGET}
drTRANSFER_TARGET={a.value:a.name for a in TRANSFER_TARGET}


IS_BOOTBOOST_ID=BYTE
class IS_BOOTBOOST_IDLIST(ctypes.Structure):
    _fields_=[  ("u32NumberOfEntries",DWORD),
                ("aList",IS_BOOTBOOST_ID*1) ]
PIS_BOOTBOOST_IDLIST=ctypes.POINTER(IS_BOOTBOOST_IDLIST)
class CIS_BOOTBOOST_IDLIST(ctypes_wrap.CStructWrapper):
    _struct=IS_BOOTBOOST_IDLIST


class IS_BOOTBOOST_CMD(enum.IntEnum):
    IS_BOOTBOOST_CMD_ENABLE          =_int32(0x00010001)
    IS_BOOTBOOST_CMD_ENABLE_AND_WAIT =_int32(0x00010101)
    IS_BOOTBOOST_CMD_DISABLE         =_int32(0x00010011)
    IS_BOOTBOOST_CMD_DISABLE_AND_WAIT=_int32(0x00010111)
    IS_BOOTBOOST_CMD_WAIT            =_int32(0x00010100)
    IS_BOOTBOOST_CMD_GET_ENABLED     =_int32(0x20010021)
    IS_BOOTBOOST_CMD_ADD_ID          =_int32(0x10100001)
    IS_BOOTBOOST_CMD_SET_IDLIST      =_int32(0x10100005)
    IS_BOOTBOOST_CMD_REMOVE_ID       =_int32(0x10100011)
    IS_BOOTBOOST_CMD_CLEAR_IDLIST    =_int32(0x00100015)
    IS_BOOTBOOST_CMD_GET_IDLIST      =_int32(0x30100021)
    IS_BOOTBOOST_CMD_GET_IDLIST_SIZE =_int32(0x20100022)
dIS_BOOTBOOST_CMD={a.name:a.value for a in IS_BOOTBOOST_CMD}
drIS_BOOTBOOST_CMD={a.value:a.name for a in IS_BOOTBOOST_CMD}


class DEVICE_FEATURE_CMD(enum.IntEnum):
    IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_FEATURES                            =_int32(1)
    IS_DEVICE_FEATURE_CMD_SET_LINESCAN_MODE                                 =_int32(2)
    IS_DEVICE_FEATURE_CMD_GET_LINESCAN_MODE                                 =_int32(3)
    IS_DEVICE_FEATURE_CMD_SET_LINESCAN_NUMBER                               =_int32(4)
    IS_DEVICE_FEATURE_CMD_GET_LINESCAN_NUMBER                               =_int32(5)
    IS_DEVICE_FEATURE_CMD_SET_SHUTTER_MODE                                  =_int32(6)
    IS_DEVICE_FEATURE_CMD_GET_SHUTTER_MODE                                  =_int32(7)
    IS_DEVICE_FEATURE_CMD_SET_PREFER_XS_HS_MODE                             =_int32(8)
    IS_DEVICE_FEATURE_CMD_GET_PREFER_XS_HS_MODE                             =_int32(9)
    IS_DEVICE_FEATURE_CMD_GET_DEFAULT_PREFER_XS_HS_MODE                     =_int32(10)
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_DEFAULT                              =_int32(11)
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE                                      =_int32(12)
    IS_DEVICE_FEATURE_CMD_SET_LOG_MODE                                      =_int32(13)
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_VALUE_DEFAULT                 =_int32(14)
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_VALUE_RANGE                   =_int32(15)
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_VALUE                         =_int32(16)
    IS_DEVICE_FEATURE_CMD_SET_LOG_MODE_MANUAL_VALUE                         =_int32(17)
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_GAIN_DEFAULT                  =_int32(18)
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_GAIN_RANGE                    =_int32(19)
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_GAIN                          =_int32(20)
    IS_DEVICE_FEATURE_CMD_SET_LOG_MODE_MANUAL_GAIN                          =_int32(21)
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_MODE_DEFAULT               =_int32(22)
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_MODE                       =_int32(23)
    IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_MODE                       =_int32(24)
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_POSITION_DEFAULT           =_int32(25)
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_POSITION_RANGE             =_int32(26)
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_POSITION                   =_int32(27)
    IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_POSITION                   =_int32(28)
    IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_MODE_DEFAULT                   =_int32(29)
    IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_MODE                           =_int32(30)
    IS_DEVICE_FEATURE_CMD_SET_FPN_CORRECTION_MODE                           =_int32(31)
    IS_DEVICE_FEATURE_CMD_GET_SENSOR_SOURCE_GAIN_RANGE                      =_int32(32)
    IS_DEVICE_FEATURE_CMD_GET_SENSOR_SOURCE_GAIN_DEFAULT                    =_int32(33)
    IS_DEVICE_FEATURE_CMD_GET_SENSOR_SOURCE_GAIN                            =_int32(34)
    IS_DEVICE_FEATURE_CMD_SET_SENSOR_SOURCE_GAIN                            =_int32(35)
    IS_DEVICE_FEATURE_CMD_GET_BLACK_REFERENCE_MODE_DEFAULT                  =_int32(36)
    IS_DEVICE_FEATURE_CMD_GET_BLACK_REFERENCE_MODE                          =_int32(37)
    IS_DEVICE_FEATURE_CMD_SET_BLACK_REFERENCE_MODE                          =_int32(38)
    IS_DEVICE_FEATURE_CMD_GET_ALLOW_RAW_WITH_LUT                            =_int32(39)
    IS_DEVICE_FEATURE_CMD_SET_ALLOW_RAW_WITH_LUT                            =_int32(40)
    IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_SENSOR_BIT_DEPTHS                   =_int32(41)
    IS_DEVICE_FEATURE_CMD_GET_SENSOR_BIT_DEPTH_DEFAULT                      =_int32(42)
    IS_DEVICE_FEATURE_CMD_GET_SENSOR_BIT_DEPTH                              =_int32(43)
    IS_DEVICE_FEATURE_CMD_SET_SENSOR_BIT_DEPTH                              =_int32(44)
    IS_DEVICE_FEATURE_CMD_GET_TEMPERATURE                                   =_int32(45)
    IS_DEVICE_FEATURE_CMD_GET_JPEG_COMPRESSION                              =_int32(46)
    IS_DEVICE_FEATURE_CMD_SET_JPEG_COMPRESSION                              =_int32(47)
    IS_DEVICE_FEATURE_CMD_GET_JPEG_COMPRESSION_DEFAULT                      =_int32(48)
    IS_DEVICE_FEATURE_CMD_GET_JPEG_COMPRESSION_RANGE                        =_int32(49)
    IS_DEVICE_FEATURE_CMD_GET_NOISE_REDUCTION_MODE                          =_int32(50)
    IS_DEVICE_FEATURE_CMD_SET_NOISE_REDUCTION_MODE                          =_int32(51)
    IS_DEVICE_FEATURE_CMD_GET_NOISE_REDUCTION_MODE_DEFAULT                  =_int32(52)
    IS_DEVICE_FEATURE_CMD_GET_TIMESTAMP_CONFIGURATION                       =_int32(53)
    IS_DEVICE_FEATURE_CMD_SET_TIMESTAMP_CONFIGURATION                       =_int32(54)
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT_DEFAULT             =_int32(55)
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT_NUMBER              =_int32(56)
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT_LIST                =_int32(57)
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT                     =_int32(58)
    IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_HEIGHT                     =_int32(59)
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION_DEFAULT=_int32(60)
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION_RANGE  =_int32(61)
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION        =_int32(62)
    IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION        =_int32(63)
    IS_DEVICE_FEATURE_CMD_GET_SENSOR_TEMPERATURE_NUMERICAL_VALUE            =_int32(64)
    IS_DEVICE_FEATURE_CMD_SET_IMAGE_EFFECT                                  =_int32(65)
    IS_DEVICE_FEATURE_CMD_GET_IMAGE_EFFECT                                  =_int32(66)
    IS_DEVICE_FEATURE_CMD_GET_IMAGE_EFFECT_DEFAULT                          =_int32(67)
    IS_DEVICE_FEATURE_CMD_GET_EXTENDED_PIXELCLOCK_RANGE_ENABLE_DEFAULT      =_int32(68)
    IS_DEVICE_FEATURE_CMD_GET_EXTENDED_PIXELCLOCK_RANGE_ENABLE              =_int32(69)
    IS_DEVICE_FEATURE_CMD_SET_EXTENDED_PIXELCLOCK_RANGE_ENABLE              =_int32(70)
    IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_SCOPE                       =_int32(71)
    IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_PARAMS                      =_int32(72)
    IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_SET_PARAMS                      =_int32(73)
    IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_MODE_DEFAULT                =_int32(74)
    IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_MODE                        =_int32(75)
    IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_SET_MODE                        =_int32(76)
    IS_DEVICE_FEATURE_CMD_SET_I2C_TARGET                                    =_int32(77)
    IS_DEVICE_FEATURE_CMD_SET_WIDE_DYNAMIC_RANGE_MODE                       =_int32(78)
    IS_DEVICE_FEATURE_CMD_GET_WIDE_DYNAMIC_RANGE_MODE                       =_int32(79)
    IS_DEVICE_FEATURE_CMD_GET_WIDE_DYNAMIC_RANGE_MODE_DEFAULT               =_int32(80)
    IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_BLACK_REFERENCE_MODES               =_int32(81)
    IS_DEVICE_FEATURE_CMD_SET_LEVEL_CONTROLLED_TRIGGER_INPUT_MODE           =_int32(82)
    IS_DEVICE_FEATURE_CMD_GET_LEVEL_CONTROLLED_TRIGGER_INPUT_MODE           =_int32(83)
    IS_DEVICE_FEATURE_CMD_GET_LEVEL_CONTROLLED_TRIGGER_INPUT_MODE_DEFAULT   =_int32(84)
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_MODE_SUPPORTED_LINE_MODES  =_int32(85)
    IS_DEVICE_FEATURE_CMD_SET_REPEATED_START_CONDITION_I2C                  =_int32(86)
    IS_DEVICE_FEATURE_CMD_GET_REPEATED_START_CONDITION_I2C                  =_int32(87)
    IS_DEVICE_FEATURE_CMD_GET_REPEATED_START_CONDITION_I2C_DEFAULT          =_int32(88)
    IS_DEVICE_FEATURE_CMD_GET_TEMPERATURE_STATUS                            =_int32(89)
    IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_ENABLE                            =_int32(90)
    IS_DEVICE_FEATURE_CMD_SET_MEMORY_MODE_ENABLE                            =_int32(91)
    IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_ENABLE_DEFAULT                    =_int32(92)
    IS_DEVICE_FEATURE_CMD_93                                                =_int32(93)
    IS_DEVICE_FEATURE_CMD_94                                                =_int32(94)
    IS_DEVICE_FEATURE_CMD_95                                                =_int32(95)
    IS_DEVICE_FEATURE_CMD_96                                                =_int32(96)
    IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_EXTERNAL_INTERFACES                 =_int32(97)
    IS_DEVICE_FEATURE_CMD_GET_EXTERNAL_INTERFACE                            =_int32(98)
    IS_DEVICE_FEATURE_CMD_SET_EXTERNAL_INTERFACE                            =_int32(99)
    IS_DEVICE_FEATURE_CMD_EXTENDED_AWB_LIMITS_GET                           =_int32(100)
    IS_DEVICE_FEATURE_CMD_EXTENDED_AWB_LIMITS_SET                           =_int32(101)
    IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_ENABLE_SUPPORTED                  =_int32(102)
dDEVICE_FEATURE_CMD={a.name:a.value for a in DEVICE_FEATURE_CMD}
drDEVICE_FEATURE_CMD={a.value:a.name for a in DEVICE_FEATURE_CMD}


class DEVICE_FEATURE_MODE_CAPS(enum.IntEnum):
    IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_ROLLING                  =_int32(0x00000001)
    IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_GLOBAL                   =_int32(0x00000002)
    IS_DEVICE_FEATURE_CAP_LINESCAN_MODE_FAST                    =_int32(0x00000004)
    IS_DEVICE_FEATURE_CAP_LINESCAN_NUMBER                       =_int32(0x00000008)
    IS_DEVICE_FEATURE_CAP_PREFER_XS_HS_MODE                     =_int32(0x00000010)
    IS_DEVICE_FEATURE_CAP_LOG_MODE                              =_int32(0x00000020)
    IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_ROLLING_GLOBAL_START     =_int32(0x00000040)
    IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_GLOBAL_ALTERNATIVE_TIMING=_int32(0x00000080)
    IS_DEVICE_FEATURE_CAP_VERTICAL_AOI_MERGE                    =_int32(0x00000100)
    IS_DEVICE_FEATURE_CAP_FPN_CORRECTION                        =_int32(0x00000200)
    IS_DEVICE_FEATURE_CAP_SENSOR_SOURCE_GAIN                    =_int32(0x00000400)
    IS_DEVICE_FEATURE_CAP_BLACK_REFERENCE                       =_int32(0x00000800)
    IS_DEVICE_FEATURE_CAP_SENSOR_BIT_DEPTH                      =_int32(0x00001000)
    IS_DEVICE_FEATURE_CAP_TEMPERATURE                           =_int32(0x00002000)
    IS_DEVICE_FEATURE_CAP_JPEG_COMPRESSION                      =_int32(0x00004000)
    IS_DEVICE_FEATURE_CAP_NOISE_REDUCTION                       =_int32(0x00008000)
    IS_DEVICE_FEATURE_CAP_TIMESTAMP_CONFIGURATION               =_int32(0x00010000)
    IS_DEVICE_FEATURE_CAP_IMAGE_EFFECT                          =_int32(0x00020000)
    IS_DEVICE_FEATURE_CAP_EXTENDED_PIXELCLOCK_RANGE             =_int32(0x00040000)
    IS_DEVICE_FEATURE_CAP_MULTI_INTEGRATION                     =_int32(0x00080000)
    IS_DEVICE_FEATURE_CAP_WIDE_DYNAMIC_RANGE                    =_int32(0x00100000)
    IS_DEVICE_FEATURE_CAP_LEVEL_CONTROLLED_TRIGGER              =_int32(0x00200000)
    IS_DEVICE_FEATURE_CAP_REPEATED_START_CONDITION_I2C          =_int32(0x00400000)
    IS_DEVICE_FEATURE_CAP_TEMPERATURE_STATUS                    =_int32(0x00800000)
    IS_DEVICE_FEATURE_CAP_MEMORY_MODE                           =_int32(0x01000000)
    IS_DEVICE_FEATURE_CAP_SEND_EXTERNAL_INTERFACE_DATA          =_int32(0x02000000)
dDEVICE_FEATURE_MODE_CAPS={a.name:a.value for a in DEVICE_FEATURE_MODE_CAPS}
drDEVICE_FEATURE_MODE_CAPS={a.value:a.name for a in DEVICE_FEATURE_MODE_CAPS}


class IS_TEMPERATURE_CONTROL_STATUS(enum.IntEnum):
    TEMPERATURE_CONTROL_STATUS_NORMAL  =_int32(0)
    TEMPERATURE_CONTROL_STATUS_WARNING =_int32(1)
    TEMPERATURE_CONTROL_STATUS_CRITICAL=_int32(2)
dIS_TEMPERATURE_CONTROL_STATUS={a.name:a.value for a in IS_TEMPERATURE_CONTROL_STATUS}
drIS_TEMPERATURE_CONTROL_STATUS={a.value:a.name for a in IS_TEMPERATURE_CONTROL_STATUS}


class NOISE_REDUCTION_MODES(enum.IntEnum):
    IS_NOISE_REDUCTION_OFF     =_int32(0)
    IS_NOISE_REDUCTION_ADAPTIVE=_int32(1)
dNOISE_REDUCTION_MODES={a.name:a.value for a in NOISE_REDUCTION_MODES}
drNOISE_REDUCTION_MODES={a.value:a.name for a in NOISE_REDUCTION_MODES}


class LOG_MODES(enum.IntEnum):
    IS_LOG_MODE_FACTORY_DEFAULT=_int32(0)
    IS_LOG_MODE_OFF            =_int32(1)
    IS_LOG_MODE_MANUAL         =_int32(2)
    IS_LOG_MODE_AUTO           =_int32(3)
dLOG_MODES={a.name:a.value for a in LOG_MODES}
drLOG_MODES={a.value:a.name for a in LOG_MODES}


class VERTICAL_AOI_MERGE_MODES(enum.IntEnum):
    IS_VERTICAL_AOI_MERGE_MODE_OFF                    =_int32(0)
    IS_VERTICAL_AOI_MERGE_MODE_FREERUN                =_int32(1)
    IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_SOFTWARE     =_int32(2)
    IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_FALLING_GPIO1=_int32(3)
    IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_RISING_GPIO1 =_int32(4)
    IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_FALLING_GPIO2=_int32(5)
    IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_RISING_GPIO2 =_int32(6)
dVERTICAL_AOI_MERGE_MODES={a.name:a.value for a in VERTICAL_AOI_MERGE_MODES}
drVERTICAL_AOI_MERGE_MODES={a.value:a.name for a in VERTICAL_AOI_MERGE_MODES}


class VERTICAL_AOI_MERGE_MODE_LINE_TRIGGER(enum.IntEnum):
    IS_VERTICAL_AOI_MERGE_MODE_LINE_FREERUN         =_int32(1)
    IS_VERTICAL_AOI_MERGE_MODE_LINE_SOFTWARE_TRIGGER=_int32(2)
    IS_VERTICAL_AOI_MERGE_MODE_LINE_GPIO_TRIGGER    =_int32(4)
dVERTICAL_AOI_MERGE_MODE_LINE_TRIGGER={a.name:a.value for a in VERTICAL_AOI_MERGE_MODE_LINE_TRIGGER}
drVERTICAL_AOI_MERGE_MODE_LINE_TRIGGER={a.value:a.name for a in VERTICAL_AOI_MERGE_MODE_LINE_TRIGGER}


class LEVEL_CONTROLLED_TRIGGER_INPUT_MODES(enum.IntEnum):
    IS_LEVEL_CONTROLLED_TRIGGER_INPUT_OFF=_int32(0)
    IS_LEVEL_CONTROLLED_TRIGGER_INPUT_ON =_int32(1)
dLEVEL_CONTROLLED_TRIGGER_INPUT_MODES={a.name:a.value for a in LEVEL_CONTROLLED_TRIGGER_INPUT_MODES}
drLEVEL_CONTROLLED_TRIGGER_INPUT_MODES={a.value:a.name for a in LEVEL_CONTROLLED_TRIGGER_INPUT_MODES}


class FPN_CORRECTION_MODES(enum.IntEnum):
    IS_FPN_CORRECTION_MODE_OFF     =_int32(0)
    IS_FPN_CORRECTION_MODE_HARDWARE=_int32(1)
dFPN_CORRECTION_MODES={a.name:a.value for a in FPN_CORRECTION_MODES}
drFPN_CORRECTION_MODES={a.value:a.name for a in FPN_CORRECTION_MODES}


class BLACK_REFERENCE_MODES(enum.IntEnum):
    IS_BLACK_REFERENCE_MODE_OFF         =_int32(0x00000000)
    IS_BLACK_REFERENCE_MODE_COLUMNS_LEFT=_int32(0x00000001)
    IS_BLACK_REFERENCE_MODE_ROWS_TOP    =_int32(0x00000002)
dBLACK_REFERENCE_MODES={a.name:a.value for a in BLACK_REFERENCE_MODES}
drBLACK_REFERENCE_MODES={a.value:a.name for a in BLACK_REFERENCE_MODES}


class SENSOR_BIT_DEPTH(enum.IntEnum):
    IS_SENSOR_BIT_DEPTH_AUTO  =_int32(0x00000000)
    IS_SENSOR_BIT_DEPTH_8_BIT =_int32(0x00000001)
    IS_SENSOR_BIT_DEPTH_10_BIT=_int32(0x00000002)
    IS_SENSOR_BIT_DEPTH_12_BIT=_int32(0x00000004)
dSENSOR_BIT_DEPTH={a.name:a.value for a in SENSOR_BIT_DEPTH}
drSENSOR_BIT_DEPTH={a.value:a.name for a in SENSOR_BIT_DEPTH}


class TIMESTAMP_CONFIGURATION_MODE(enum.IntEnum):
    IS_RESET_TIMESTAMP_ONCE=_int32(1)
dTIMESTAMP_CONFIGURATION_MODE={a.name:a.value for a in TIMESTAMP_CONFIGURATION_MODE}
drTIMESTAMP_CONFIGURATION_MODE={a.value:a.name for a in TIMESTAMP_CONFIGURATION_MODE}


class TIMESTAMP_CONFIGURATION_PIN(enum.IntEnum):
    TIMESTAMP_CONFIGURATION_PIN_NONE   =_int32(0)
    TIMESTAMP_CONFIGURATION_PIN_TRIGGER=_int32(1)
    TIMESTAMP_CONFIGURATION_PIN_GPIO_1 =_int32(2)
    TIMESTAMP_CONFIGURATION_PIN_GPIO_2 =_int32(3)
dTIMESTAMP_CONFIGURATION_PIN={a.name:a.value for a in TIMESTAMP_CONFIGURATION_PIN}
drTIMESTAMP_CONFIGURATION_PIN={a.value:a.name for a in TIMESTAMP_CONFIGURATION_PIN}


class TIMESTAMP_CONFIGURATION_EDGE(enum.IntEnum):
    TIMESTAMP_CONFIGURATION_EDGE_FALLING=_int32(0)
    TIMESTAMP_CONFIGURATION_EDGE_RISING =_int32(1)
dTIMESTAMP_CONFIGURATION_EDGE={a.name:a.value for a in TIMESTAMP_CONFIGURATION_EDGE}
drTIMESTAMP_CONFIGURATION_EDGE={a.value:a.name for a in TIMESTAMP_CONFIGURATION_EDGE}


class IS_TIMESTAMP_CONFIGURATION(ctypes.Structure):
    _fields_=[  ("s32Mode",INT),
                ("s32Pin",INT),
                ("s32Edge",INT) ]
PIS_TIMESTAMP_CONFIGURATION=ctypes.POINTER(IS_TIMESTAMP_CONFIGURATION)
class CIS_TIMESTAMP_CONFIGURATION(ctypes_wrap.CStructWrapper):
    _struct=IS_TIMESTAMP_CONFIGURATION


class IMAGE_EFFECT_MODE(enum.IntEnum):
    IS_IMAGE_EFFECT_DISABLE   =_int32(0)
    IS_IMAGE_EFFECT_SEPIA     =_int32(1)
    IS_IMAGE_EFFECT_MONOCHROME=_int32(2)
    IS_IMAGE_EFFECT_NEGATIVE  =_int32(3)
    IS_IMAGE_EFFECT_CROSSHAIRS=_int32(4)
dIMAGE_EFFECT_MODE={a.name:a.value for a in IMAGE_EFFECT_MODE}
drIMAGE_EFFECT_MODE={a.value:a.name for a in IMAGE_EFFECT_MODE}


class IS_EXTENDED_PIXELCLOCK_RANGE(enum.IntEnum):
    EXTENDED_PIXELCLOCK_RANGE_OFF=_int32(0)
    EXTENDED_PIXELCLOCK_RANGE_ON =_int32(1)
dIS_EXTENDED_PIXELCLOCK_RANGE={a.name:a.value for a in IS_EXTENDED_PIXELCLOCK_RANGE}
drIS_EXTENDED_PIXELCLOCK_RANGE={a.value:a.name for a in IS_EXTENDED_PIXELCLOCK_RANGE}


class IS_MULTI_INTEGRATION_MODE(enum.IntEnum):
    MULTI_INTEGRATION_MODE_OFF     =_int32(0)
    MULTI_INTEGRATION_MODE_SOFTWARE=_int32(1)
    MULTI_INTEGRATION_MODE_GPIO1   =_int32(2)
    MULTI_INTEGRATION_MODE_GPIO2   =_int32(3)
dIS_MULTI_INTEGRATION_MODE={a.name:a.value for a in IS_MULTI_INTEGRATION_MODE}
drIS_MULTI_INTEGRATION_MODE={a.value:a.name for a in IS_MULTI_INTEGRATION_MODE}


class IS_MULTI_INTEGRATION_CYCLES(ctypes.Structure):
    _fields_=[  ("dblIntegration_ms",ctypes.c_double),
                ("dblPause_ms",ctypes.c_double) ]
PIS_MULTI_INTEGRATION_CYCLES=ctypes.POINTER(IS_MULTI_INTEGRATION_CYCLES)
class CIS_MULTI_INTEGRATION_CYCLES(ctypes_wrap.CStructWrapper):
    _struct=IS_MULTI_INTEGRATION_CYCLES


class IS_MULTI_INTEGRATION_SCOPE(ctypes.Structure):
    _fields_=[  ("dblMinIntegration_ms",ctypes.c_double),
                ("dblMaxIntegration_ms",ctypes.c_double),
                ("dblIntegrationGranularity_ms",ctypes.c_double),
                ("dblMinPause_ms",ctypes.c_double),
                ("dblMaxPause_ms",ctypes.c_double),
                ("dblPauseGranularity_ms",ctypes.c_double),
                ("dblMinCycle_ms",ctypes.c_double),
                ("dblMaxCycle_ms",ctypes.c_double),
                ("dblCycleGranularity_ms",ctypes.c_double),
                ("dblMinTriggerCycle_ms",ctypes.c_double),
                ("dblMinTriggerDuration_ms",ctypes.c_double),
                ("nMinNumberOfCycles",UINT),
                ("nMaxNumberOfCycles",UINT),
                ("m_bReserved",BYTE*32) ]
PIS_MULTI_INTEGRATION_SCOPE=ctypes.POINTER(IS_MULTI_INTEGRATION_SCOPE)
class CIS_MULTI_INTEGRATION_SCOPE(ctypes_wrap.CStructWrapper):
    _struct=IS_MULTI_INTEGRATION_SCOPE


class IS_I2C_TARGET(enum.IntEnum):
    I2C_TARGET_DEFAULT    =_int32(0)
    I2C_TARGET_SENSOR_1   =_int32(1)
    I2C_TARGET_SENSOR_2   =_int32(2)
    I2C_TARGET_LOGIC_BOARD=_int32(4)
dIS_I2C_TARGET={a.name:a.value for a in IS_I2C_TARGET}
drIS_I2C_TARGET={a.value:a.name for a in IS_I2C_TARGET}


class IS_MEMORY_MODE(enum.IntEnum):
    IS_MEMORY_MODE_OFF=_int32(0)
    IS_MEMORY_MODE_ON =_int32(1)
dIS_MEMORY_MODE={a.name:a.value for a in IS_MEMORY_MODE}
drIS_MEMORY_MODE={a.value:a.name for a in IS_MEMORY_MODE}


class IS_EXTERNAL_INTERFACE_TYPE(enum.IntEnum):
    IS_EXTERNAL_INTERFACE_TYPE_NONE=_int32(0)
    IS_EXTERNAL_INTERFACE_TYPE_I2C =_int32(1)
dIS_EXTERNAL_INTERFACE_TYPE={a.name:a.value for a in IS_EXTERNAL_INTERFACE_TYPE}
drIS_EXTERNAL_INTERFACE_TYPE={a.value:a.name for a in IS_EXTERNAL_INTERFACE_TYPE}


class IS_EXTERNAL_INTERFACE_REGISTER_TYPE(enum.IntEnum):
    IS_EXTERNAL_INTERFACE_REGISTER_TYPE_8BIT =_int32(0)
    IS_EXTERNAL_INTERFACE_REGISTER_TYPE_16BIT=_int32(1)
    IS_EXTERNAL_INTERFACE_REGISTER_TYPE_NONE =_int32(2)
dIS_EXTERNAL_INTERFACE_REGISTER_TYPE={a.name:a.value for a in IS_EXTERNAL_INTERFACE_REGISTER_TYPE}
drIS_EXTERNAL_INTERFACE_REGISTER_TYPE={a.value:a.name for a in IS_EXTERNAL_INTERFACE_REGISTER_TYPE}


class IS_EXTERNAL_INTERFACE_EVENT(enum.IntEnum):
    IS_EXTERNAL_INTERFACE_EVENT_RISING_VSYNC =_int32(0)
    IS_EXTERNAL_INTERFACE_EVENT_FALLING_VSYNC=_int32(1)
dIS_EXTERNAL_INTERFACE_EVENT={a.name:a.value for a in IS_EXTERNAL_INTERFACE_EVENT}
drIS_EXTERNAL_INTERFACE_EVENT={a.value:a.name for a in IS_EXTERNAL_INTERFACE_EVENT}


class IS_EXTERNAL_INTERFACE_DATA(enum.IntEnum):
    IS_EXTERNAL_INTERFACE_DATA_USER              =_int32(0)
    IS_EXTERNAL_INTERFACE_DATA_TIMESTAMP_FULL    =_int32(1)
    IS_EXTERNAL_INTERFACE_DATA_TIMESTAMP_LOWBYTE =_int32(2)
    IS_EXTERNAL_INTERFACE_DATA_TIMESTAMP_HIGHBYTE=_int32(3)
dIS_EXTERNAL_INTERFACE_DATA={a.name:a.value for a in IS_EXTERNAL_INTERFACE_DATA}
drIS_EXTERNAL_INTERFACE_DATA={a.value:a.name for a in IS_EXTERNAL_INTERFACE_DATA}


class IS_EXTERNAL_INTERFACE_I2C_CONFIGURATION(ctypes.Structure):
    _fields_=[  ("bySlaveAddress",BYTE),
                ("wRegisterAddress",WORD),
                ("byRegisterAddressType",BYTE),
                ("byAckPolling",BYTE),
                ("byReserved",BYTE*11) ]
PIS_EXTERNAL_INTERFACE_I2C_CONFIGURATION=ctypes.POINTER(IS_EXTERNAL_INTERFACE_I2C_CONFIGURATION)
class CIS_EXTERNAL_INTERFACE_I2C_CONFIGURATION(ctypes_wrap.CStructWrapper):
    _struct=IS_EXTERNAL_INTERFACE_I2C_CONFIGURATION


class IS_EXTERNAL_INTERFACE_CONFIGURATION(ctypes.Structure):
    _fields_=[  ("wInterfaceType",WORD),
                ("sInterfaceConfiguration",BYTE*16),
                ("wSendEvent",WORD),
                ("wDataSelection",WORD) ]
PIS_EXTERNAL_INTERFACE_CONFIGURATION=ctypes.POINTER(IS_EXTERNAL_INTERFACE_CONFIGURATION)
class CIS_EXTERNAL_INTERFACE_CONFIGURATION(ctypes_wrap.CStructWrapper):
    _struct=IS_EXTERNAL_INTERFACE_CONFIGURATION


class EXPOSURE_CMD(enum.IntEnum):
    IS_EXPOSURE_CMD_GET_CAPS                       =_int32(1)
    IS_EXPOSURE_CMD_GET_EXPOSURE_DEFAULT           =_int32(2)
    IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MIN         =_int32(3)
    IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MAX         =_int32(4)
    IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_INC         =_int32(5)
    IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE             =_int32(6)
    IS_EXPOSURE_CMD_GET_EXPOSURE                   =_int32(7)
    IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_MIN   =_int32(8)
    IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_MAX   =_int32(9)
    IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_INC   =_int32(10)
    IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE       =_int32(11)
    IS_EXPOSURE_CMD_SET_EXPOSURE                   =_int32(12)
    IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_MIN    =_int32(13)
    IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_MAX    =_int32(14)
    IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_INC    =_int32(15)
    IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE        =_int32(16)
    IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_ENABLE       =_int32(17)
    IS_EXPOSURE_CMD_SET_LONG_EXPOSURE_ENABLE       =_int32(18)
    IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO_DEFAULT=_int32(19)
    IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO_RANGE  =_int32(20)
    IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO        =_int32(21)
    IS_EXPOSURE_CMD_SET_DUAL_EXPOSURE_RATIO        =_int32(22)
dEXPOSURE_CMD={a.name:a.value for a in EXPOSURE_CMD}
drEXPOSURE_CMD={a.value:a.name for a in EXPOSURE_CMD}


class EXPOSURE_CAPS(enum.IntEnum):
    IS_EXPOSURE_CAP_EXPOSURE      =_int32(0x00000001)
    IS_EXPOSURE_CAP_FINE_INCREMENT=_int32(0x00000002)
    IS_EXPOSURE_CAP_LONG_EXPOSURE =_int32(0x00000004)
    IS_EXPOSURE_CAP_DUAL_EXPOSURE =_int32(0x00000008)
dEXPOSURE_CAPS={a.name:a.value for a in EXPOSURE_CAPS}
drEXPOSURE_CAPS={a.value:a.name for a in EXPOSURE_CAPS}


class TRIGGER_CMD(enum.IntEnum):
    IS_TRIGGER_CMD_GET_BURST_SIZE_SUPPORTED     =_int32(1)
    IS_TRIGGER_CMD_GET_BURST_SIZE_RANGE         =_int32(2)
    IS_TRIGGER_CMD_GET_BURST_SIZE               =_int32(3)
    IS_TRIGGER_CMD_SET_BURST_SIZE               =_int32(4)
    IS_TRIGGER_CMD_GET_FRAME_PRESCALER_SUPPORTED=_int32(5)
    IS_TRIGGER_CMD_GET_FRAME_PRESCALER_RANGE    =_int32(6)
    IS_TRIGGER_CMD_GET_FRAME_PRESCALER          =_int32(7)
    IS_TRIGGER_CMD_SET_FRAME_PRESCALER          =_int32(8)
    IS_TRIGGER_CMD_GET_LINE_PRESCALER_SUPPORTED =_int32(9)
    IS_TRIGGER_CMD_GET_LINE_PRESCALER_RANGE     =_int32(10)
    IS_TRIGGER_CMD_GET_LINE_PRESCALER           =_int32(11)
    IS_TRIGGER_CMD_SET_LINE_PRESCALER           =_int32(12)
dTRIGGER_CMD={a.name:a.value for a in TRIGGER_CMD}
drTRIGGER_CMD={a.value:a.name for a in TRIGGER_CMD}


class IS_DEVICE_INFO_HEARTBEAT(ctypes.Structure):
    _fields_=[  ("reserved_1",BYTE*24),
                ("dwRuntimeFirmwareVersion",DWORD),
                ("reserved_2",BYTE*8),
                ("wTemperature",WORD),
                ("wLinkSpeed_Mb",WORD),
                ("reserved_3",BYTE*6),
                ("wComportOffset",WORD),
                ("reserved",BYTE*200) ]
PIS_DEVICE_INFO_HEARTBEAT=ctypes.POINTER(IS_DEVICE_INFO_HEARTBEAT)
class CIS_DEVICE_INFO_HEARTBEAT(ctypes_wrap.CStructWrapper):
    _struct=IS_DEVICE_INFO_HEARTBEAT


class IS_DEVICE_INFO_CONTROL(ctypes.Structure):
    _fields_=[  ("dwDeviceId",DWORD),
                ("reserved",BYTE*148) ]
PIS_DEVICE_INFO_CONTROL=ctypes.POINTER(IS_DEVICE_INFO_CONTROL)
class CIS_DEVICE_INFO_CONTROL(ctypes_wrap.CStructWrapper):
    _struct=IS_DEVICE_INFO_CONTROL


class IS_DEVICE_INFO(ctypes.Structure):
    _fields_=[  ("infoDevHeartbeat",IS_DEVICE_INFO_HEARTBEAT),
                ("infoDevControl",IS_DEVICE_INFO_CONTROL),
                ("reserved",BYTE*240) ]
PIS_DEVICE_INFO=ctypes.POINTER(IS_DEVICE_INFO)
class CIS_DEVICE_INFO(ctypes_wrap.CStructWrapper):
    _struct=IS_DEVICE_INFO


class IS_DEVICE_INFO_CMD(enum.IntEnum):
    IS_DEVICE_INFO_CMD_GET_DEVICE_INFO=_int32(0x02010001)
dIS_DEVICE_INFO_CMD={a.name:a.value for a in IS_DEVICE_INFO_CMD}
drIS_DEVICE_INFO_CMD={a.value:a.name for a in IS_DEVICE_INFO_CMD}


class IS_CALLBACK_CMD(enum.IntEnum):
    IS_CALLBACK_CMD_INSTALL  =_int32(0x00000001)
    IS_CALLBACK_CMD_UNINSTALL=_int32(0x00000002)
dIS_CALLBACK_CMD={a.name:a.value for a in IS_CALLBACK_CMD}
drIS_CALLBACK_CMD={a.value:a.name for a in IS_CALLBACK_CMD}


class IS_CALLBACK_EVENT(enum.IntEnum):
    IS_CALLBACK_EV_IMGPOSTPROC_START=_int32(0x00000001)
dIS_CALLBACK_EVENT={a.name:a.value for a in IS_CALLBACK_EVENT}
drIS_CALLBACK_EVENT={a.value:a.name for a in IS_CALLBACK_EVENT}


class IS_CALLBACK_EVCTX_DATA_PROCESSING(ctypes.Structure):
    _fields_=[  ("pSrcBuf",ctypes.c_void_p),
                ("cbSrcBuf",UINT),
                ("pDestBuf",ctypes.c_void_p),
                ("cbDestBuf",UINT) ]
PIS_CALLBACK_EVCTX_DATA_PROCESSING=ctypes.POINTER(IS_CALLBACK_EVCTX_DATA_PROCESSING)
class CIS_CALLBACK_EVCTX_DATA_PROCESSING(ctypes_wrap.CStructWrapper):
    _struct=IS_CALLBACK_EVCTX_DATA_PROCESSING


class IS_CALLBACK_EVCTX_IMAGE_PROCESSING(ctypes.Structure):
    _fields_=[  ("bufferInfo",IS_CALLBACK_EVCTX_DATA_PROCESSING) ]
PIS_CALLBACK_EVCTX_IMAGE_PROCESSING=ctypes.POINTER(IS_CALLBACK_EVCTX_IMAGE_PROCESSING)
class CIS_CALLBACK_EVCTX_IMAGE_PROCESSING(ctypes_wrap.CStructWrapper):
    _struct=IS_CALLBACK_EVCTX_IMAGE_PROCESSING


class IS_CALLBACK_FDBK_IMAGE_PROCESSING(ctypes.Structure):
    _fields_=[  ("nDummy",UINT) ]
PIS_CALLBACK_FDBK_IMAGE_PROCESSING=ctypes.POINTER(IS_CALLBACK_FDBK_IMAGE_PROCESSING)
class CIS_CALLBACK_FDBK_IMAGE_PROCESSING(ctypes_wrap.CStructWrapper):
    _struct=IS_CALLBACK_FDBK_IMAGE_PROCESSING


IS_CALLBACK_FUNC=ctypes.c_void_p
HCAM_CALLBACK=HCAM
class IS_CALLBACK_INSTALLATION_DATA(ctypes.Structure):
    _fields_=[  ("nEvent",UINT),
                ("pfFunc",IS_CALLBACK_FUNC),
                ("pUserContext",ctypes.c_void_p),
                ("hCallback",HCAM_CALLBACK) ]
PIS_CALLBACK_INSTALLATION_DATA=ctypes.POINTER(IS_CALLBACK_INSTALLATION_DATA)
class CIS_CALLBACK_INSTALLATION_DATA(ctypes_wrap.CStructWrapper):
    _struct=IS_CALLBACK_INSTALLATION_DATA


class IS_OPTIMAL_CAMERA_TIMING_CMD(enum.IntEnum):
    IS_OPTIMAL_CAMERA_TIMING_CMD_GET_PIXELCLOCK=_int32(0x00000001)
    IS_OPTIMAL_CAMERA_TIMING_CMD_GET_FRAMERATE =_int32(0x00000002)
dIS_OPTIMAL_CAMERA_TIMING_CMD={a.name:a.value for a in IS_OPTIMAL_CAMERA_TIMING_CMD}
drIS_OPTIMAL_CAMERA_TIMING_CMD={a.value:a.name for a in IS_OPTIMAL_CAMERA_TIMING_CMD}


class IS_OPTIMAL_CAMERA_TIMING(ctypes.Structure):
    _fields_=[  ("s32Mode",INT),
                ("s32TimeoutFineTuning",INT),
                ("ps32PixelClock",ctypes.POINTER(INT)),
                ("pdFramerate",ctypes.POINTER(ctypes.c_double)) ]
PIS_OPTIMAL_CAMERA_TIMING=ctypes.POINTER(IS_OPTIMAL_CAMERA_TIMING)
class CIS_OPTIMAL_CAMERA_TIMING(ctypes_wrap.CStructWrapper):
    _struct=IS_OPTIMAL_CAMERA_TIMING


PUC480_ETH_ADDR_IPV4=ctypes.c_void_p
class UC480_ETH_ADDR_MAC(ctypes.Structure):
    _fields_=[  ("abyOctet",BYTE*6) ]
PUC480_ETH_ADDR_MAC=ctypes.POINTER(UC480_ETH_ADDR_MAC)
class CUC480_ETH_ADDR_MAC(ctypes_wrap.CStructWrapper):
    _struct=UC480_ETH_ADDR_MAC


PUC480_ETH_ADDR_MAC=ctypes.c_void_p
class UC480_ETH_IP_CONFIGURATION(ctypes.Structure):
    _fields_=[  ("ipAddress",DWORD),
                ("ipSubnetmask",DWORD),
                ("reserved",BYTE*4) ]
PUC480_ETH_IP_CONFIGURATION=ctypes.POINTER(UC480_ETH_IP_CONFIGURATION)
class CUC480_ETH_IP_CONFIGURATION(ctypes_wrap.CStructWrapper):
    _struct=UC480_ETH_IP_CONFIGURATION


PUC480_ETH_IP_CONFIGURATION=ctypes.c_void_p
class UC480_ETH_DEVICESTATUS(enum.IntEnum):
    IS_ETH_DEVSTATUS_READY_TO_OPERATE          =_int32(0x00000001)
    IS_ETH_DEVSTATUS_TESTING_IP_CURRENT        =_int32(0x00000002)
    IS_ETH_DEVSTATUS_TESTING_IP_PERSISTENT     =_int32(0x00000004)
    IS_ETH_DEVSTATUS_TESTING_IP_RANGE          =_int32(0x00000008)
    IS_ETH_DEVSTATUS_INAPPLICABLE_IP_CURRENT   =_int32(0x00000010)
    IS_ETH_DEVSTATUS_INAPPLICABLE_IP_PERSISTENT=_int32(0x00000020)
    IS_ETH_DEVSTATUS_INAPPLICABLE_IP_RANGE     =_int32(0x00000040)
    IS_ETH_DEVSTATUS_UNPAIRED                  =_int32(0x00000100)
    IS_ETH_DEVSTATUS_PAIRING_IN_PROGRESS       =_int32(0x00000200)
    IS_ETH_DEVSTATUS_PAIRED                    =_int32(0x00000400)
    IS_ETH_DEVSTATUS_FORCE_100MBPS             =_int32(0x00001000)
    IS_ETH_DEVSTATUS_NO_COMPORT                =_int32(0x00002000)
    IS_ETH_DEVSTATUS_RECEIVING_FW_STARTER      =_int32(0x00010000)
    IS_ETH_DEVSTATUS_RECEIVING_FW_RUNTIME      =_int32(0x00020000)
    IS_ETH_DEVSTATUS_INAPPLICABLE_FW_RUNTIME   =_int32(0x00040000)
    IS_ETH_DEVSTATUS_INAPPLICABLE_FW_STARTER   =_int32(0x00080000)
    IS_ETH_DEVSTATUS_REBOOTING_FW_RUNTIME      =_int32(0x00100000)
    IS_ETH_DEVSTATUS_REBOOTING_FW_STARTER      =_int32(0x00200000)
    IS_ETH_DEVSTATUS_REBOOTING_FW_FAILSAFE     =_int32(0x00400000)
    IS_ETH_DEVSTATUS_RUNTIME_FW_ERR0           =_int32(0x80000000)
dUC480_ETH_DEVICESTATUS={a.name:a.value for a in UC480_ETH_DEVICESTATUS}
drUC480_ETH_DEVICESTATUS={a.value:a.name for a in UC480_ETH_DEVICESTATUS}


class UC480_ETH_DEVICE_INFO_HEARTBEAT(ctypes.Structure):
    _fields_=[  ("abySerialNumber",BYTE*12),
                ("byDeviceType",BYTE),
                ("byCameraID",BYTE),
                ("wSensorID",WORD),
                ("wSizeImgMem_MB",WORD),
                ("reserved_1",BYTE*2),
                ("dwVerStarterFirmware",DWORD),
                ("dwVerRuntimeFirmware",DWORD),
                ("dwStatus",DWORD),
                ("reserved_2",BYTE*4),
                ("wTemperature",WORD),
                ("wLinkSpeed_Mb",WORD),
                ("macDevice",UC480_ETH_ADDR_MAC),
                ("wComportOffset",WORD),
                ("ipcfgPersistentIpCfg",UC480_ETH_IP_CONFIGURATION),
                ("ipcfgCurrentIpCfg",UC480_ETH_IP_CONFIGURATION),
                ("macPairedHost",UC480_ETH_ADDR_MAC),
                ("reserved_4",BYTE*2),
                ("ipPairedHostIp",DWORD),
                ("ipAutoCfgIpRangeBegin",DWORD),
                ("ipAutoCfgIpRangeEnd",DWORD),
                ("abyUserSpace",BYTE*8),
                ("reserved_5",BYTE*84),
                ("reserved_6",BYTE*64) ]
PUC480_ETH_DEVICE_INFO_HEARTBEAT=ctypes.POINTER(UC480_ETH_DEVICE_INFO_HEARTBEAT)
class CUC480_ETH_DEVICE_INFO_HEARTBEAT(ctypes_wrap.CStructWrapper):
    _struct=UC480_ETH_DEVICE_INFO_HEARTBEAT


PUC480_ETH_DEVICE_INFO_HEARTBEAT=ctypes.c_void_p
class UC480_ETH_CONTROLSTATUS(enum.IntEnum):
    IS_ETH_CTRLSTATUS_AVAILABLE            =_int32(0x00000001)
    IS_ETH_CTRLSTATUS_ACCESSIBLE1          =_int32(0x00000002)
    IS_ETH_CTRLSTATUS_ACCESSIBLE2          =_int32(0x00000004)
    IS_ETH_CTRLSTATUS_PERSISTENT_IP_USED   =_int32(0x00000010)
    IS_ETH_CTRLSTATUS_COMPATIBLE           =_int32(0x00000020)
    IS_ETH_CTRLSTATUS_ADAPTER_ON_DHCP      =_int32(0x00000040)
    IS_ETH_CTRLSTATUS_ADAPTER_SETUP_OK     =_int32(0x00000080)
    IS_ETH_CTRLSTATUS_UNPAIRING_IN_PROGRESS=_int32(0x00000100)
    IS_ETH_CTRLSTATUS_PAIRING_IN_PROGRESS  =_int32(0x00000200)
    IS_ETH_CTRLSTATUS_PAIRED               =_int32(0x00001000)
    IS_ETH_CTRLSTATUS_OPENED               =_int32(0x00004000)
    IS_ETH_CTRLSTATUS_FW_UPLOAD_STARTER    =_int32(0x00010000)
    IS_ETH_CTRLSTATUS_FW_UPLOAD_RUNTIME    =_int32(0x00020000)
    IS_ETH_CTRLSTATUS_REBOOTING            =_int32(0x00100000)
    IS_ETH_CTRLSTATUS_BOOTBOOST_ENABLED    =_int32(0x01000000)
    IS_ETH_CTRLSTATUS_BOOTBOOST_ACTIVE     =_int32(0x02000000)
    IS_ETH_CTRLSTATUS_INITIALIZED          =_int32(0x08000000)
    IS_ETH_CTRLSTATUS_TO_BE_DELETED        =_int32(0x40000000)
    IS_ETH_CTRLSTATUS_TO_BE_REMOVED        =_int32(0x80000000)
dUC480_ETH_CONTROLSTATUS={a.name:a.value for a in UC480_ETH_CONTROLSTATUS}
drUC480_ETH_CONTROLSTATUS={a.value:a.name for a in UC480_ETH_CONTROLSTATUS}


class UC480_ETH_DEVICE_INFO_CONTROL(ctypes.Structure):
    _fields_=[  ("dwDeviceID",DWORD),
                ("dwControlStatus",DWORD),
                ("reserved_1",BYTE*80),
                ("reserved_2",BYTE*64) ]
PUC480_ETH_DEVICE_INFO_CONTROL=ctypes.POINTER(UC480_ETH_DEVICE_INFO_CONTROL)
class CUC480_ETH_DEVICE_INFO_CONTROL(ctypes_wrap.CStructWrapper):
    _struct=UC480_ETH_DEVICE_INFO_CONTROL


PUC480_ETH_DEVICE_INFO_CONTROL=ctypes.c_void_p
class UC480_ETH_ETHERNET_CONFIGURATION(ctypes.Structure):
    _fields_=[  ("ipcfg",UC480_ETH_IP_CONFIGURATION),
                ("mac",UC480_ETH_ADDR_MAC) ]
PUC480_ETH_ETHERNET_CONFIGURATION=ctypes.POINTER(UC480_ETH_ETHERNET_CONFIGURATION)
class CUC480_ETH_ETHERNET_CONFIGURATION(ctypes_wrap.CStructWrapper):
    _struct=UC480_ETH_ETHERNET_CONFIGURATION


PUC480_ETH_ETHERNET_CONFIGURATION=ctypes.c_void_p
class UC480_ETH_AUTOCFG_IP_SETUP(ctypes.Structure):
    _fields_=[  ("ipAutoCfgIpRangeBegin",DWORD),
                ("ipAutoCfgIpRangeEnd",DWORD),
                ("reserved",BYTE*4) ]
PUC480_ETH_AUTOCFG_IP_SETUP=ctypes.POINTER(UC480_ETH_AUTOCFG_IP_SETUP)
class CUC480_ETH_AUTOCFG_IP_SETUP(ctypes_wrap.CStructWrapper):
    _struct=UC480_ETH_AUTOCFG_IP_SETUP


PUC480_ETH_AUTOCFG_IP_SETUP=ctypes.c_void_p
class UC480_ETH_PACKETFILTER_SETUP(enum.IntEnum):
    IS_ETH_PCKTFLT_PASSALL   =_int32(0)
    IS_ETH_PCKTFLT_BLOCKUEGET=_int32(1)
    IS_ETH_PCKTFLT_BLOCKALL  =_int32(2)
dUC480_ETH_PACKETFILTER_SETUP={a.name:a.value for a in UC480_ETH_PACKETFILTER_SETUP}
drUC480_ETH_PACKETFILTER_SETUP={a.value:a.name for a in UC480_ETH_PACKETFILTER_SETUP}


class UC480_ETH_LINKSPEED_SETUP(enum.IntEnum):
    IS_ETH_LINKSPEED_100MB =_int32(100)
    IS_ETH_LINKSPEED_1000MB=_int32(1000)
dUC480_ETH_LINKSPEED_SETUP={a.name:a.value for a in UC480_ETH_LINKSPEED_SETUP}
drUC480_ETH_LINKSPEED_SETUP={a.value:a.name for a in UC480_ETH_LINKSPEED_SETUP}


class UC480_ETH_ADAPTER_INFO(ctypes.Structure):
    _fields_=[  ("dwAdapterID",DWORD),
                ("dwDeviceLinkspeed",DWORD),
                ("ethcfg",UC480_ETH_ETHERNET_CONFIGURATION),
                ("reserved_2",BYTE*2),
                ("bIsEnabledDHCP",BOOL),
                ("autoCfgIp",UC480_ETH_AUTOCFG_IP_SETUP),
                ("bIsValidAutoCfgIpRange",BOOL),
                ("dwCntDevicesKnown",DWORD),
                ("dwCntDevicesPaired",DWORD),
                ("wPacketFilter",WORD),
                ("reserved_3",BYTE*38),
                ("reserved_4",BYTE*64) ]
PUC480_ETH_ADAPTER_INFO=ctypes.POINTER(UC480_ETH_ADAPTER_INFO)
class CUC480_ETH_ADAPTER_INFO(ctypes_wrap.CStructWrapper):
    _struct=UC480_ETH_ADAPTER_INFO


PUC480_ETH_ADAPTER_INFO=ctypes.c_void_p
class UC480_ETH_DRIVER_INFO(ctypes.Structure):
    _fields_=[  ("dwMinVerStarterFirmware",DWORD),
                ("dwMaxVerStarterFirmware",DWORD),
                ("reserved_1",BYTE*8),
                ("reserved_2",BYTE*64) ]
PUC480_ETH_DRIVER_INFO=ctypes.POINTER(UC480_ETH_DRIVER_INFO)
class CUC480_ETH_DRIVER_INFO(ctypes_wrap.CStructWrapper):
    _struct=UC480_ETH_DRIVER_INFO


PUC480_ETH_DRIVER_INFO=ctypes.c_void_p
class UC480_ETH_DEVICE_INFO(ctypes.Structure):
    _fields_=[  ("infoDevHeartbeat",UC480_ETH_DEVICE_INFO_HEARTBEAT),
                ("infoDevControl",UC480_ETH_DEVICE_INFO_CONTROL),
                ("infoAdapter",UC480_ETH_ADAPTER_INFO),
                ("infoDriver",UC480_ETH_DRIVER_INFO) ]
PUC480_ETH_DEVICE_INFO=ctypes.POINTER(UC480_ETH_DEVICE_INFO)
class CUC480_ETH_DEVICE_INFO(ctypes_wrap.CStructWrapper):
    _struct=UC480_ETH_DEVICE_INFO


PUC480_ETH_DEVICE_INFO=ctypes.c_void_p
class UC480_COMPORT_CONFIGURATION(ctypes.Structure):
    _fields_=[  ("wComportNumber",WORD) ]
PUC480_COMPORT_CONFIGURATION=ctypes.POINTER(UC480_COMPORT_CONFIGURATION)
class CUC480_COMPORT_CONFIGURATION(ctypes_wrap.CStructWrapper):
    _struct=UC480_COMPORT_CONFIGURATION


PUC480_COMPORT_CONFIGURATION=ctypes.c_void_p
class IPCONFIG_CAPABILITY_FLAGS(enum.IntEnum):
    IPCONFIG_CAP_PERSISTENT_IP_SUPPORTED=_int32(0x01)
    IPCONFIG_CAP_AUTOCONFIG_IP_SUPPORTED=_int32(0x04)
dIPCONFIG_CAPABILITY_FLAGS={a.name:a.value for a in IPCONFIG_CAPABILITY_FLAGS}
drIPCONFIG_CAPABILITY_FLAGS={a.value:a.name for a in IPCONFIG_CAPABILITY_FLAGS}


class IPCONFIG_CMD(enum.IntEnum):
    IPCONFIG_CMD_QUERY_CAPABILITIES        =_int32(0)
    IPCONFIG_CMD_SET_PERSISTENT_IP         =_int32(0x01010000)
    IPCONFIG_CMD_SET_AUTOCONFIG_IP         =_int32(0x01040000)
    IPCONFIG_CMD_SET_AUTOCONFIG_IP_BYDEVICE=_int32(0x01040100)
    IPCONFIG_CMD_RESERVED1                 =_int32(0x01080000)
    IPCONFIG_CMD_GET_PERSISTENT_IP         =_int32(0x02010000)
    IPCONFIG_CMD_GET_AUTOCONFIG_IP         =_int32(0x02040000)
    IPCONFIG_CMD_GET_AUTOCONFIG_IP_BYDEVICE=_int32(0x02040100)
dIPCONFIG_CMD={a.name:a.value for a in IPCONFIG_CMD}
drIPCONFIG_CMD={a.value:a.name for a in IPCONFIG_CMD}


class CONFIGURATION_SEL(enum.IntEnum):
    IS_CONFIG_CPU_IDLE_STATES_BIT_AC_VALUE=_int32(0x01)
    IS_CONFIG_CPU_IDLE_STATES_BIT_DC_VALUE=_int32(0x02)
    IS_CONFIG_IPO_NOT_ALLOWED             =_int32(0)
    IS_CONFIG_IPO_ALLOWED                 =_int32(1)
    IS_CONFIG_OPEN_MP_DISABLE             =_int32(0)
    IS_CONFIG_OPEN_MP_ENABLE              =_int32(1)
    IS_CONFIG_INITIAL_PARAMETERSET_NONE   =_int32(0)
    IS_CONFIG_INITIAL_PARAMETERSET_1      =_int32(1)
    IS_CONFIG_INITIAL_PARAMETERSET_2      =_int32(2)
    IS_CONFIG_ETH_CONFIGURATION_MODE_OFF  =_int32(0)
    IS_CONFIG_ETH_CONFIGURATION_MODE_ON   =_int32(1)
    IS_CONFIG_TRUSTED_PAIRING_OFF         =_int32(0)
    IS_CONFIG_TRUSTED_PAIRING_ON          =_int32(1)
dCONFIGURATION_SEL={a.name:a.value for a in CONFIGURATION_SEL}
drCONFIGURATION_SEL={a.value:a.name for a in CONFIGURATION_SEL}


class CONFIGURATION_CMD(enum.IntEnum):
    IS_CONFIG_CMD_GET_CAPABILITIES                   =_int32(1)
    IS_CONFIG_CPU_IDLE_STATES_CMD_GET_ENABLE         =_int32(2)
    IS_CONFIG_CPU_IDLE_STATES_CMD_SET_DISABLE_ON_OPEN=_int32(4)
    IS_CONFIG_CPU_IDLE_STATES_CMD_GET_DISABLE_ON_OPEN=_int32(5)
    IS_CONFIG_OPEN_MP_CMD_GET_ENABLE                 =_int32(6)
    IS_CONFIG_OPEN_MP_CMD_SET_ENABLE                 =_int32(7)
    IS_CONFIG_OPEN_MP_CMD_GET_ENABLE_DEFAULT         =_int32(8)
    IS_CONFIG_INITIAL_PARAMETERSET_CMD_SET           =_int32(9)
    IS_CONFIG_INITIAL_PARAMETERSET_CMD_GET           =_int32(10)
    IS_CONFIG_ETH_CONFIGURATION_MODE_CMD_SET_ENABLE  =_int32(11)
    IS_CONFIG_ETH_CONFIGURATION_MODE_CMD_GET_ENABLE  =_int32(12)
    IS_CONFIG_IPO_CMD_GET_ALLOWED                    =_int32(13)
    IS_CONFIG_IPO_CMD_SET_ALLOWED                    =_int32(14)
    IS_CONFIG_CMD_TRUSTED_PAIRING_SET                =_int32(15)
    IS_CONFIG_CMD_TRUSTED_PAIRING_GET                =_int32(16)
    IS_CONFIG_CMD_TRUSTED_PAIRING_GET_DEFAULT        =_int32(17)
    IS_CONFIG_CMD_RESERVED_1                         =_int32(18)
dCONFIGURATION_CMD={a.name:a.value for a in CONFIGURATION_CMD}
drCONFIGURATION_CMD={a.value:a.name for a in CONFIGURATION_CMD}


class CONFIGURATION_CAPS(enum.IntEnum):
    IS_CONFIG_CPU_IDLE_STATES_CAP_SUPPORTED     =_int32(0x00000001)
    IS_CONFIG_OPEN_MP_CAP_SUPPORTED             =_int32(0x00000002)
    IS_CONFIG_INITIAL_PARAMETERSET_CAP_SUPPORTED=_int32(0x00000004)
    IS_CONFIG_IPO_CAP_SUPPORTED                 =_int32(0x00000008)
    IS_CONFIG_TRUSTED_PAIRING_CAP_SUPPORTED     =_int32(0x00000010)
dCONFIGURATION_CAPS={a.name:a.value for a in CONFIGURATION_CAPS}
drCONFIGURATION_CAPS={a.value:a.name for a in CONFIGURATION_CAPS}


class IO_FLASH_PARAMS(ctypes.Structure):
    _fields_=[  ("s32Delay",INT),
                ("u32Duration",UINT) ]
PIO_FLASH_PARAMS=ctypes.POINTER(IO_FLASH_PARAMS)
class CIO_FLASH_PARAMS(ctypes_wrap.CStructWrapper):
    _struct=IO_FLASH_PARAMS


class IO_PWM_PARAMS(ctypes.Structure):
    _fields_=[  ("dblFrequency_Hz",ctypes.c_double),
                ("dblDutyCycle",ctypes.c_double) ]
PIO_PWM_PARAMS=ctypes.POINTER(IO_PWM_PARAMS)
class CIO_PWM_PARAMS(ctypes_wrap.CStructWrapper):
    _struct=IO_PWM_PARAMS


class IO_GPIO_CONFIGURATION(ctypes.Structure):
    _fields_=[  ("u32Gpio",UINT),
                ("u32Caps",UINT),
                ("u32Configuration",UINT),
                ("u32State",UINT),
                ("u32Reserved",UINT*12) ]
PIO_GPIO_CONFIGURATION=ctypes.POINTER(IO_GPIO_CONFIGURATION)
class CIO_GPIO_CONFIGURATION(ctypes_wrap.CStructWrapper):
    _struct=IO_GPIO_CONFIGURATION


class IO_CMD(enum.IntEnum):
    IS_IO_CMD_GPIOS_GET_SUPPORTED           =_int32(1)
    IS_IO_CMD_GPIOS_GET_SUPPORTED_INPUTS    =_int32(2)
    IS_IO_CMD_GPIOS_GET_SUPPORTED_OUTPUTS   =_int32(3)
    IS_IO_CMD_GPIOS_GET_DIRECTION           =_int32(4)
    IS_IO_CMD_GPIOS_SET_DIRECTION           =_int32(5)
    IS_IO_CMD_GPIOS_GET_STATE               =_int32(6)
    IS_IO_CMD_GPIOS_SET_STATE               =_int32(7)
    IS_IO_CMD_LED_GET_STATE                 =_int32(8)
    IS_IO_CMD_LED_SET_STATE                 =_int32(9)
    IS_IO_CMD_LED_TOGGLE_STATE              =_int32(10)
    IS_IO_CMD_FLASH_GET_GLOBAL_PARAMS       =_int32(11)
    IS_IO_CMD_FLASH_APPLY_GLOBAL_PARAMS     =_int32(12)
    IS_IO_CMD_FLASH_GET_SUPPORTED_GPIOS     =_int32(13)
    IS_IO_CMD_FLASH_GET_PARAMS_MIN          =_int32(14)
    IS_IO_CMD_FLASH_GET_PARAMS_MAX          =_int32(15)
    IS_IO_CMD_FLASH_GET_PARAMS_INC          =_int32(16)
    IS_IO_CMD_FLASH_GET_PARAMS              =_int32(17)
    IS_IO_CMD_FLASH_SET_PARAMS              =_int32(18)
    IS_IO_CMD_FLASH_GET_MODE                =_int32(19)
    IS_IO_CMD_FLASH_SET_MODE                =_int32(20)
    IS_IO_CMD_PWM_GET_SUPPORTED_GPIOS       =_int32(21)
    IS_IO_CMD_PWM_GET_PARAMS_MIN            =_int32(22)
    IS_IO_CMD_PWM_GET_PARAMS_MAX            =_int32(23)
    IS_IO_CMD_PWM_GET_PARAMS_INC            =_int32(24)
    IS_IO_CMD_PWM_GET_PARAMS                =_int32(25)
    IS_IO_CMD_PWM_SET_PARAMS                =_int32(26)
    IS_IO_CMD_PWM_GET_MODE                  =_int32(27)
    IS_IO_CMD_PWM_SET_MODE                  =_int32(28)
    IS_IO_CMD_GPIOS_GET_CONFIGURATION       =_int32(29)
    IS_IO_CMD_GPIOS_SET_CONFIGURATION       =_int32(30)
    IS_IO_CMD_FLASH_GET_GPIO_PARAMS_MIN     =_int32(31)
    IS_IO_CMD_FLASH_SET_GPIO_PARAMS         =_int32(32)
    IS_IO_CMD_FLASH_GET_AUTO_FREERUN_DEFAULT=_int32(33)
    IS_IO_CMD_FLASH_GET_AUTO_FREERUN        =_int32(34)
    IS_IO_CMD_FLASH_SET_AUTO_FREERUN        =_int32(35)
dIO_CMD={a.name:a.value for a in IO_CMD}
drIO_CMD={a.value:a.name for a in IO_CMD}


class AUTOPARAMETER_CMD(enum.IntEnum):
    IS_AWB_CMD_GET_SUPPORTED_TYPES           =_int32(1)
    IS_AWB_CMD_GET_TYPE                      =_int32(2)
    IS_AWB_CMD_SET_TYPE                      =_int32(3)
    IS_AWB_CMD_GET_ENABLE                    =_int32(4)
    IS_AWB_CMD_SET_ENABLE                    =_int32(5)
    IS_AWB_CMD_GET_SUPPORTED_RGB_COLOR_MODELS=_int32(6)
    IS_AWB_CMD_GET_RGB_COLOR_MODEL           =_int32(7)
    IS_AWB_CMD_SET_RGB_COLOR_MODEL           =_int32(8)
    IS_AES_CMD_GET_SUPPORTED_TYPES           =_int32(9)
    IS_AES_CMD_SET_ENABLE                    =_int32(10)
    IS_AES_CMD_GET_ENABLE                    =_int32(11)
    IS_AES_CMD_SET_TYPE                      =_int32(12)
    IS_AES_CMD_GET_TYPE                      =_int32(13)
    IS_AES_CMD_SET_CONFIGURATION             =_int32(14)
    IS_AES_CMD_GET_CONFIGURATION             =_int32(15)
    IS_AES_CMD_GET_CONFIGURATION_DEFAULT     =_int32(16)
    IS_AES_CMD_GET_CONFIGURATION_RANGE       =_int32(17)
dAUTOPARAMETER_CMD={a.name:a.value for a in AUTOPARAMETER_CMD}
drAUTOPARAMETER_CMD={a.value:a.name for a in AUTOPARAMETER_CMD}


class AES_MODE(enum.IntEnum):
    IS_AES_MODE_PEAK=_int32(0x01)
    IS_AES_MODE_MEAN=_int32(0x02)
dAES_MODE={a.name:a.value for a in AES_MODE}
drAES_MODE={a.value:a.name for a in AES_MODE}


class AES_CONFIGURATION(ctypes.Structure):
    _fields_=[  ("nMode",INT),
                ("pConfiguration",CHAR*1) ]
PAES_CONFIGURATION=ctypes.POINTER(AES_CONFIGURATION)
class CAES_CONFIGURATION(ctypes_wrap.CStructWrapper):
    _struct=AES_CONFIGURATION


class AES_PEAK_WHITE_CONFIGURATION(ctypes.Structure):
    _fields_=[  ("rectUserAOI",IS_RECT),
                ("nFrameSkip",UINT),
                ("nHysteresis",UINT),
                ("nReference",UINT),
                ("nChannel",UINT),
                ("f64Maximum",ctypes.c_double),
                ("f64Minimum",ctypes.c_double),
                ("reserved",CHAR*32) ]
PAES_PEAK_WHITE_CONFIGURATION=ctypes.POINTER(AES_PEAK_WHITE_CONFIGURATION)
class CAES_PEAK_WHITE_CONFIGURATION(ctypes_wrap.CStructWrapper):
    _struct=AES_PEAK_WHITE_CONFIGURATION


class AES_PEAK_WHITE_CONFIGURATION_RANGE(ctypes.Structure):
    _fields_=[  ("rangeFrameSkip",IS_RANGE_S32),
                ("rangeHysteresis",IS_RANGE_S32),
                ("rangeReference",IS_RANGE_S32),
                ("reserved",CHAR*32) ]
PAES_PEAK_WHITE_CONFIGURATION_RANGE=ctypes.POINTER(AES_PEAK_WHITE_CONFIGURATION_RANGE)
class CAES_PEAK_WHITE_CONFIGURATION_RANGE(ctypes_wrap.CStructWrapper):
    _struct=AES_PEAK_WHITE_CONFIGURATION_RANGE


class AES_CHANNEL(enum.IntEnum):
    IS_AES_CHANNEL_MONO =_int32(0x01)
    IS_AES_CHANNEL_RED  =_int32(0x01)
    IS_AES_CHANNEL_GREEN=_int32(0x02)
    IS_AES_CHANNEL_BLUE =_int32(0x04)
dAES_CHANNEL={a.name:a.value for a in AES_CHANNEL}
drAES_CHANNEL={a.value:a.name for a in AES_CHANNEL}


class BUFFER_CONVERSION_PARAMS(ctypes.Structure):
    _fields_=[  ("pSourceBuffer",ctypes.c_char_p),
                ("pDestBuffer",ctypes.c_char_p),
                ("nDestPixelFormat",INT),
                ("nDestPixelConverter",INT),
                ("nDestGamma",INT),
                ("nDestEdgeEnhancement",INT),
                ("nDestColorCorrectionMode",INT),
                ("nDestSaturationU",INT),
                ("nDestSaturationV",INT),
                ("reserved",BYTE*32) ]
PBUFFER_CONVERSION_PARAMS=ctypes.POINTER(BUFFER_CONVERSION_PARAMS)
class CBUFFER_CONVERSION_PARAMS(ctypes_wrap.CStructWrapper):
    _struct=BUFFER_CONVERSION_PARAMS


class CONVERT_CMD(enum.IntEnum):
    IS_CONVERT_CMD_APPLY_PARAMS_AND_CONVERT_BUFFER=_int32(1)
dCONVERT_CMD={a.name:a.value for a in CONVERT_CMD}
drCONVERT_CMD={a.value:a.name for a in CONVERT_CMD}


class PARAMETERSET_CMD(enum.IntEnum):
    IS_PARAMETERSET_CMD_LOAD_EEPROM                  =_int32(1)
    IS_PARAMETERSET_CMD_LOAD_FILE                    =_int32(2)
    IS_PARAMETERSET_CMD_SAVE_EEPROM                  =_int32(3)
    IS_PARAMETERSET_CMD_SAVE_FILE                    =_int32(4)
    IS_PARAMETERSET_CMD_GET_NUMBER_SUPPORTED         =_int32(5)
    IS_PARAMETERSET_CMD_GET_HW_PARAMETERSET_AVAILABLE=_int32(6)
    IS_PARAMETERSET_CMD_ERASE_HW_PARAMETERSET        =_int32(7)
dPARAMETERSET_CMD={a.name:a.value for a in PARAMETERSET_CMD}
drPARAMETERSET_CMD={a.value:a.name for a in PARAMETERSET_CMD}


class EDGE_ENHANCEMENT_CMD(enum.IntEnum):
    IS_EDGE_ENHANCEMENT_CMD_GET_RANGE  =_int32(1)
    IS_EDGE_ENHANCEMENT_CMD_GET_DEFAULT=_int32(2)
    IS_EDGE_ENHANCEMENT_CMD_GET        =_int32(3)
    IS_EDGE_ENHANCEMENT_CMD_SET        =_int32(4)
dEDGE_ENHANCEMENT_CMD={a.name:a.value for a in EDGE_ENHANCEMENT_CMD}
drEDGE_ENHANCEMENT_CMD={a.value:a.name for a in EDGE_ENHANCEMENT_CMD}


class PIXELCLOCK_CMD(enum.IntEnum):
    IS_PIXELCLOCK_CMD_GET_NUMBER =_int32(1)
    IS_PIXELCLOCK_CMD_GET_LIST   =_int32(2)
    IS_PIXELCLOCK_CMD_GET_RANGE  =_int32(3)
    IS_PIXELCLOCK_CMD_GET_DEFAULT=_int32(4)
    IS_PIXELCLOCK_CMD_GET        =_int32(5)
    IS_PIXELCLOCK_CMD_SET        =_int32(6)
dPIXELCLOCK_CMD={a.name:a.value for a in PIXELCLOCK_CMD}
drPIXELCLOCK_CMD={a.value:a.name for a in PIXELCLOCK_CMD}


class IMAGE_FILE_PARAMS(ctypes.Structure):
    _fields_=[  ("pwchFileName",ctypes.c_wchar_p),
                ("nFileType",UINT),
                ("nQuality",UINT),
                ("ppcImageMem",ctypes.POINTER(ctypes.c_char_p)),
                ("pnImageID",ctypes.POINTER(UINT)),
                ("reserved",BYTE*32) ]
PIMAGE_FILE_PARAMS=ctypes.POINTER(IMAGE_FILE_PARAMS)
class CIMAGE_FILE_PARAMS(ctypes_wrap.CStructWrapper):
    _struct=IMAGE_FILE_PARAMS


class IMAGE_FILE_CMD(enum.IntEnum):
    IS_IMAGE_FILE_CMD_LOAD=_int32(1)
    IS_IMAGE_FILE_CMD_SAVE=_int32(2)
dIMAGE_FILE_CMD={a.name:a.value for a in IMAGE_FILE_CMD}
drIMAGE_FILE_CMD={a.value:a.name for a in IMAGE_FILE_CMD}


class BLACKLEVEL_MODES(enum.IntEnum):
    IS_AUTO_BLACKLEVEL_OFF=_int32(0)
    IS_AUTO_BLACKLEVEL_ON =_int32(1)
dBLACKLEVEL_MODES={a.name:a.value for a in BLACKLEVEL_MODES}
drBLACKLEVEL_MODES={a.value:a.name for a in BLACKLEVEL_MODES}


class BLACKLEVEL_CAPS(enum.IntEnum):
    IS_BLACKLEVEL_CAP_SET_AUTO_BLACKLEVEL=_int32(1)
    IS_BLACKLEVEL_CAP_SET_OFFSET         =_int32(2)
dBLACKLEVEL_CAPS={a.name:a.value for a in BLACKLEVEL_CAPS}
drBLACKLEVEL_CAPS={a.value:a.name for a in BLACKLEVEL_CAPS}


class BLACKLEVEL_CMD(enum.IntEnum):
    IS_BLACKLEVEL_CMD_GET_CAPS          =_int32(1)
    IS_BLACKLEVEL_CMD_GET_MODE_DEFAULT  =_int32(2)
    IS_BLACKLEVEL_CMD_GET_MODE          =_int32(3)
    IS_BLACKLEVEL_CMD_SET_MODE          =_int32(4)
    IS_BLACKLEVEL_CMD_GET_OFFSET_DEFAULT=_int32(5)
    IS_BLACKLEVEL_CMD_GET_OFFSET_RANGE  =_int32(6)
    IS_BLACKLEVEL_CMD_GET_OFFSET        =_int32(7)
    IS_BLACKLEVEL_CMD_SET_OFFSET        =_int32(8)
dBLACKLEVEL_CMD={a.name:a.value for a in BLACKLEVEL_CMD}
drBLACKLEVEL_CMD={a.value:a.name for a in BLACKLEVEL_CMD}


class IMGBUF_CMD(enum.IntEnum):
    IS_IMGBUF_DEVMEM_CMD_GET_AVAILABLE_ITERATIONS=_int32(1)
    IS_IMGBUF_DEVMEM_CMD_GET_ITERATION_INFO      =_int32(2)
    IS_IMGBUF_DEVMEM_CMD_TRANSFER_IMAGE          =_int32(3)
    IS_IMGBUF_DEVMEM_CMD_RELEASE_ITERATIONS      =_int32(4)
dIMGBUF_CMD={a.name:a.value for a in IMGBUF_CMD}
drIMGBUF_CMD={a.value:a.name for a in IMGBUF_CMD}


class ID_RANGE(ctypes.Structure):
    _fields_=[  ("s32First",INT),
                ("s32Last",INT) ]
PID_RANGE=ctypes.POINTER(ID_RANGE)
class CID_RANGE(ctypes_wrap.CStructWrapper):
    _struct=ID_RANGE


class IMGBUF_ITERATION_INFO(ctypes.Structure):
    _fields_=[  ("u32IterationID",UINT),
                ("rangeImageID",ID_RANGE),
                ("bReserved",BYTE*52) ]
PIMGBUF_ITERATION_INFO=ctypes.POINTER(IMGBUF_ITERATION_INFO)
class CIMGBUF_ITERATION_INFO(ctypes_wrap.CStructWrapper):
    _struct=IMGBUF_ITERATION_INFO


class IMGBUF_ITEM(ctypes.Structure):
    _fields_=[  ("u32IterationID",UINT),
                ("s32ImageID",INT) ]
PIMGBUF_ITEM=ctypes.POINTER(IMGBUF_ITEM)
class CIMGBUF_ITEM(ctypes_wrap.CStructWrapper):
    _struct=IMGBUF_ITEM


class MEASURE_SHARPNESS_AOI_INFO(ctypes.Structure):
    _fields_=[  ("u32NumberAOI",UINT),
                ("u32SharpnessValue",UINT),
                ("rcAOI",IS_RECT) ]
PMEASURE_SHARPNESS_AOI_INFO=ctypes.POINTER(MEASURE_SHARPNESS_AOI_INFO)
class CMEASURE_SHARPNESS_AOI_INFO(ctypes_wrap.CStructWrapper):
    _struct=MEASURE_SHARPNESS_AOI_INFO


class MEASURE_CMD(enum.IntEnum):
    IS_MEASURE_CMD_SHARPNESS_AOI_SET       =_int32(1)
    IS_MEASURE_CMD_SHARPNESS_AOI_INQUIRE   =_int32(2)
    IS_MEASURE_CMD_SHARPNESS_AOI_SET_PRESET=_int32(3)
dMEASURE_CMD={a.name:a.value for a in MEASURE_CMD}
drMEASURE_CMD={a.value:a.name for a in MEASURE_CMD}


class MEASURE_SHARPNESS_AOI_PRESETS(enum.IntEnum):
    IS_MEASURE_SHARPNESS_AOI_PRESET_1=_int32(1)
dMEASURE_SHARPNESS_AOI_PRESETS={a.name:a.value for a in MEASURE_SHARPNESS_AOI_PRESETS}
drMEASURE_SHARPNESS_AOI_PRESETS={a.value:a.name for a in MEASURE_SHARPNESS_AOI_PRESETS}


IS_LUT_PRESET=INT
class IS_LUT_CONFIGURATION_64(ctypes.Structure):
    _fields_=[  ("dblValues",ctypes.c_double*64*3),
                ("bAllChannelsAreEqual",BOOL) ]
PIS_LUT_CONFIGURATION_64=ctypes.POINTER(IS_LUT_CONFIGURATION_64)
class CIS_LUT_CONFIGURATION_64(ctypes_wrap.CStructWrapper):
    _struct=IS_LUT_CONFIGURATION_64


class IS_LUT_CONFIGURATION_PRESET_64(ctypes.Structure):
    _fields_=[  ("predefinedLutID",IS_LUT_PRESET),
                ("lutConfiguration",IS_LUT_CONFIGURATION_64) ]
PIS_LUT_CONFIGURATION_PRESET_64=ctypes.POINTER(IS_LUT_CONFIGURATION_PRESET_64)
class CIS_LUT_CONFIGURATION_PRESET_64(ctypes_wrap.CStructWrapper):
    _struct=IS_LUT_CONFIGURATION_PRESET_64


class IS_LUT_STATE(ctypes.Structure):
    _fields_=[  ("bLUTEnabled",BOOL),
                ("nLUTStateID",INT),
                ("nLUTModeID",INT),
                ("nLUTBits",INT) ]
PIS_LUT_STATE=ctypes.POINTER(IS_LUT_STATE)
class CIS_LUT_STATE(ctypes_wrap.CStructWrapper):
    _struct=IS_LUT_STATE


class IS_LUT_SUPPORT_INFO(ctypes.Structure):
    _fields_=[  ("bSupportLUTHardware",BOOL),
                ("bSupportLUTSoftware",BOOL),
                ("nBitsHardware",INT),
                ("nBitsSoftware",INT),
                ("nChannelsHardware",INT),
                ("nChannelsSoftware",INT) ]
PIS_LUT_SUPPORT_INFO=ctypes.POINTER(IS_LUT_SUPPORT_INFO)
class CIS_LUT_SUPPORT_INFO(ctypes_wrap.CStructWrapper):
    _struct=IS_LUT_SUPPORT_INFO


class IS_MEMORY_CMD(enum.IntEnum):
    IS_MEMORY_GET_SIZE=_int32(1)
    IS_MEMORY_READ    =_int32(2)
    IS_MEMORY_WRITE   =_int32(3)
dIS_MEMORY_CMD={a.name:a.value for a in IS_MEMORY_CMD}
drIS_MEMORY_CMD={a.value:a.name for a in IS_MEMORY_CMD}


class IS_MEMORY_DESCRIPTION(enum.IntEnum):
    IS_MEMORY_USER_1=_int32(1)
    IS_MEMORY_USER_2=_int32(2)
dIS_MEMORY_DESCRIPTION={a.name:a.value for a in IS_MEMORY_DESCRIPTION}
drIS_MEMORY_DESCRIPTION={a.value:a.name for a in IS_MEMORY_DESCRIPTION}


class IS_MEMORY_ACCESS(ctypes.Structure):
    _fields_=[  ("u32Description",UINT),
                ("u32Offset",UINT),
                ("pu8Data",ctypes.POINTER(ctypes.c_ubyte)),
                ("u32SizeOfData",UINT) ]
PIS_MEMORY_ACCESS=ctypes.POINTER(IS_MEMORY_ACCESS)
class CIS_MEMORY_ACCESS(ctypes_wrap.CStructWrapper):
    _struct=IS_MEMORY_ACCESS


class IS_MEMORY_SIZE(ctypes.Structure):
    _fields_=[  ("u32Description",UINT),
                ("u32SizeBytes",UINT) ]
PIS_MEMORY_SIZE=ctypes.POINTER(IS_MEMORY_SIZE)
class CIS_MEMORY_SIZE(ctypes_wrap.CStructWrapper):
    _struct=IS_MEMORY_SIZE


class IS_MULTI_AOI_DESCRIPTOR(ctypes.Structure):
    _fields_=[  ("nPosX",UINT),
                ("nPosY",UINT),
                ("nWidth",UINT),
                ("nHeight",UINT),
                ("nStatus",UINT) ]
PIS_MULTI_AOI_DESCRIPTOR=ctypes.POINTER(IS_MULTI_AOI_DESCRIPTOR)
class CIS_MULTI_AOI_DESCRIPTOR(ctypes_wrap.CStructWrapper):
    _struct=IS_MULTI_AOI_DESCRIPTOR


class IS_MULTI_AOI_CONTAINER(ctypes.Structure):
    _fields_=[  ("nNumberOfAOIs",UINT),
                ("pMultiAOIList",ctypes.POINTER(IS_MULTI_AOI_DESCRIPTOR)) ]
PIS_MULTI_AOI_CONTAINER=ctypes.POINTER(IS_MULTI_AOI_CONTAINER)
class CIS_MULTI_AOI_CONTAINER(ctypes_wrap.CStructWrapper):
    _struct=IS_MULTI_AOI_CONTAINER


class IS_PMC_READONLYDEVICEDESCRIPTOR(ctypes.Structure):
    _fields_=[  ("ipCamera",DWORD),
                ("ipMulticast",DWORD),
                ("u32CameraId",UINT),
                ("u32ErrorHandlingMode",UINT) ]
PIS_PMC_READONLYDEVICEDESCRIPTOR=ctypes.POINTER(IS_PMC_READONLYDEVICEDESCRIPTOR)
class CIS_PMC_READONLYDEVICEDESCRIPTOR(ctypes_wrap.CStructWrapper):
    _struct=IS_PMC_READONLYDEVICEDESCRIPTOR





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
    #  INT is_CaptureStatus(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
    addfunc(lib, "is_CaptureStatus", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "nSizeOfParam"] )
    #  INT is_SetSaturation(HCAM hCam, INT ChromU, INT ChromV)
    addfunc(lib, "is_SetSaturation", restype = INT,
            argtypes = [HCAM, INT, INT],
            argnames = ["hCam", "ChromU", "ChromV"] )
    #  INT is_PrepareStealVideo(HCAM hCam, ctypes.c_int Mode, ULONG StealColorMode)
    addfunc(lib, "is_PrepareStealVideo", restype = INT,
            argtypes = [HCAM, ctypes.c_int, ULONG],
            argnames = ["hCam", "Mode", "StealColorMode"] )
    #  INT is_GetNumberOfDevices()
    addfunc(lib, "is_GetNumberOfDevices", restype = INT,
            argtypes = [],
            argnames = [] )
    #  INT is_StopLiveVideo(HCAM hCam, INT Wait)
    addfunc(lib, "is_StopLiveVideo", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "Wait"] )
    #  INT is_FreezeVideo(HCAM hCam, INT Wait)
    addfunc(lib, "is_FreezeVideo", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "Wait"] )
    #  INT is_CaptureVideo(HCAM hCam, INT Wait)
    addfunc(lib, "is_CaptureVideo", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "Wait"] )
    #  INT is_IsVideoFinish(HCAM hCam, ctypes.POINTER(INT) pValue)
    addfunc(lib, "is_IsVideoFinish", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(INT)],
            argnames = ["hCam", "pValue"] )
    #  INT is_HasVideoStarted(HCAM hCam, ctypes.POINTER(BOOL) pbo)
    addfunc(lib, "is_HasVideoStarted", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(BOOL)],
            argnames = ["hCam", "pbo"] )
    #  INT is_AllocImageMem(HCAM hCam, INT width, INT height, INT bitspixel, ctypes.POINTER(ctypes.c_char_p) ppcImgMem, ctypes.POINTER(ctypes.c_int) pid)
    addfunc(lib, "is_AllocImageMem", restype = INT,
            argtypes = [HCAM, INT, INT, INT, ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_int)],
            argnames = ["hCam", "width", "height", "bitspixel", "ppcImgMem", "pid"] )
    #  INT is_SetImageMem(HCAM hCam, ctypes.c_char_p pcMem, ctypes.c_int id)
    addfunc(lib, "is_SetImageMem", restype = INT,
            argtypes = [HCAM, ctypes.c_char_p, ctypes.c_int],
            argnames = ["hCam", "pcMem", "id"] )
    #  INT is_FreeImageMem(HCAM hCam, ctypes.c_char_p pcMem, ctypes.c_int id)
    addfunc(lib, "is_FreeImageMem", restype = INT,
            argtypes = [HCAM, ctypes.c_char_p, ctypes.c_int],
            argnames = ["hCam", "pcMem", "id"] )
    #  INT is_GetImageMem(HCAM hCam, ctypes.POINTER(ctypes.c_void_p) pMem)
    addfunc(lib, "is_GetImageMem", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(ctypes.c_void_p)],
            argnames = ["hCam", "pMem"] )
    #  INT is_GetActiveImageMem(HCAM hCam, ctypes.POINTER(ctypes.c_char_p) ppcMem, ctypes.POINTER(ctypes.c_int) pnID)
    addfunc(lib, "is_GetActiveImageMem", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_int)],
            argnames = ["hCam", "ppcMem", "pnID"] )
    #  INT is_InquireImageMem(HCAM hCam, ctypes.c_char_p pcMem, ctypes.c_int nID, ctypes.POINTER(ctypes.c_int) pnX, ctypes.POINTER(ctypes.c_int) pnY, ctypes.POINTER(ctypes.c_int) pnBits, ctypes.POINTER(ctypes.c_int) pnPitch)
    addfunc(lib, "is_InquireImageMem", restype = INT,
            argtypes = [HCAM, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["hCam", "pcMem", "nID", "pnX", "pnY", "pnBits", "pnPitch"] )
    #  INT is_GetImageMemPitch(HCAM hCam, ctypes.POINTER(INT) pPitch)
    addfunc(lib, "is_GetImageMemPitch", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(INT)],
            argnames = ["hCam", "pPitch"] )
    #  INT is_SetAllocatedImageMem(HCAM hCam, INT width, INT height, INT bitspixel, ctypes.c_char_p pcImgMem, ctypes.POINTER(ctypes.c_int) pid)
    addfunc(lib, "is_SetAllocatedImageMem", restype = INT,
            argtypes = [HCAM, INT, INT, INT, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["hCam", "width", "height", "bitspixel", "pcImgMem", "pid"] )
    #  INT is_CopyImageMem(HCAM hCam, ctypes.c_char_p pcSource, ctypes.c_int nID, ctypes.c_char_p pcDest)
    addfunc(lib, "is_CopyImageMem", restype = INT,
            argtypes = [HCAM, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p],
            argnames = ["hCam", "pcSource", "nID", "pcDest"] )
    #  INT is_CopyImageMemLines(HCAM hCam, ctypes.c_char_p pcSource, ctypes.c_int nID, ctypes.c_int nLines, ctypes.c_char_p pcDest)
    addfunc(lib, "is_CopyImageMemLines", restype = INT,
            argtypes = [HCAM, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p],
            argnames = ["hCam", "pcSource", "nID", "nLines", "pcDest"] )
    #  INT is_AddToSequence(HCAM hCam, ctypes.c_char_p pcMem, INT nID)
    addfunc(lib, "is_AddToSequence", restype = INT,
            argtypes = [HCAM, ctypes.c_char_p, INT],
            argnames = ["hCam", "pcMem", "nID"] )
    #  INT is_ClearSequence(HCAM hCam)
    addfunc(lib, "is_ClearSequence", restype = INT,
            argtypes = [HCAM],
            argnames = ["hCam"] )
    #  INT is_GetActSeqBuf(HCAM hCam, ctypes.POINTER(INT) pnNum, ctypes.POINTER(ctypes.c_char_p) ppcMem, ctypes.POINTER(ctypes.c_char_p) ppcMemLast)
    addfunc(lib, "is_GetActSeqBuf", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(INT), ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_char_p)],
            argnames = ["hCam", "pnNum", "ppcMem", "ppcMemLast"] )
    #  INT is_LockSeqBuf(HCAM hCam, INT nNum, ctypes.c_char_p pcMem)
    addfunc(lib, "is_LockSeqBuf", restype = INT,
            argtypes = [HCAM, INT, ctypes.c_char_p],
            argnames = ["hCam", "nNum", "pcMem"] )
    #  INT is_UnlockSeqBuf(HCAM hCam, INT nNum, ctypes.c_char_p pcMem)
    addfunc(lib, "is_UnlockSeqBuf", restype = INT,
            argtypes = [HCAM, INT, ctypes.c_char_p],
            argnames = ["hCam", "nNum", "pcMem"] )
    #  INT is_GetError(HCAM hCam, ctypes.POINTER(INT) pErr, ctypes.POINTER(ctypes.c_char_p) ppcErr)
    addfunc(lib, "is_GetError", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(INT), ctypes.POINTER(ctypes.c_char_p)],
            argnames = ["hCam", "pErr", "ppcErr"] )
    #  INT is_SetErrorReport(HCAM hCam, INT Mode)
    addfunc(lib, "is_SetErrorReport", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "Mode"] )
    #  INT is_ReadEEPROM(HCAM hCam, INT Adr, ctypes.c_char_p pcString, INT Count)
    addfunc(lib, "is_ReadEEPROM", restype = INT,
            argtypes = [HCAM, INT, ctypes.c_char_p, INT],
            argnames = ["hCam", "Adr", "pcString", "Count"] )
    #  INT is_WriteEEPROM(HCAM hCam, INT Adr, ctypes.c_char_p pcString, INT Count)
    addfunc(lib, "is_WriteEEPROM", restype = INT,
            argtypes = [HCAM, INT, ctypes.c_char_p, INT],
            argnames = ["hCam", "Adr", "pcString", "Count"] )
    #  INT is_SetColorMode(HCAM hCam, INT Mode)
    addfunc(lib, "is_SetColorMode", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "Mode"] )
    #  INT is_GetColorDepth(HCAM hCam, ctypes.POINTER(INT) pnCol, ctypes.POINTER(INT) pnColMode)
    addfunc(lib, "is_GetColorDepth", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(INT), ctypes.POINTER(INT)],
            argnames = ["hCam", "pnCol", "pnColMode"] )
    #  INT is_RenderBitmap(HCAM hCam, INT nMemID, HWND hwnd, INT nMode)
    addfunc(lib, "is_RenderBitmap", restype = INT,
            argtypes = [HCAM, INT, HWND, INT],
            argnames = ["hCam", "nMemID", "hwnd", "nMode"] )
    #  INT is_SetDisplayMode(HCAM hCam, INT Mode)
    addfunc(lib, "is_SetDisplayMode", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "Mode"] )
    #  INT is_SetDisplayPos(HCAM hCam, INT x, INT y)
    addfunc(lib, "is_SetDisplayPos", restype = INT,
            argtypes = [HCAM, INT, INT],
            argnames = ["hCam", "x", "y"] )
    #  INT is_SetHwnd(HCAM hCam, HWND hwnd)
    addfunc(lib, "is_SetHwnd", restype = INT,
            argtypes = [HCAM, HWND],
            argnames = ["hCam", "hwnd"] )
    #  INT is_GetVsyncCount(HCAM hCam, ctypes.POINTER(ctypes.c_long) pIntr, ctypes.POINTER(ctypes.c_long) pActIntr)
    addfunc(lib, "is_GetVsyncCount", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long)],
            argnames = ["hCam", "pIntr", "pActIntr"] )
    #  INT is_GetDLLVersion()
    addfunc(lib, "is_GetDLLVersion", restype = INT,
            argtypes = [],
            argnames = [] )
    #  INT is_InitEvent(HCAM hCam, HANDLE hEv, INT which)
    addfunc(lib, "is_InitEvent", restype = INT,
            argtypes = [HCAM, HANDLE, INT],
            argnames = ["hCam", "hEv", "which"] )
    #  INT is_ExitEvent(HCAM hCam, INT which)
    addfunc(lib, "is_ExitEvent", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "which"] )
    #  INT is_EnableEvent(HCAM hCam, INT which)
    addfunc(lib, "is_EnableEvent", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "which"] )
    #  INT is_DisableEvent(HCAM hCam, INT which)
    addfunc(lib, "is_DisableEvent", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "which"] )
    #  INT is_SetExternalTrigger(HCAM hCam, INT nTriggerMode)
    addfunc(lib, "is_SetExternalTrigger", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "nTriggerMode"] )
    #  INT is_SetTriggerCounter(HCAM hCam, INT nValue)
    addfunc(lib, "is_SetTriggerCounter", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "nValue"] )
    #  INT is_SetRopEffect(HCAM hCam, INT effect, INT param, INT reserved)
    addfunc(lib, "is_SetRopEffect", restype = INT,
            argtypes = [HCAM, INT, INT, INT],
            argnames = ["hCam", "effect", "param", "reserved"] )
    #  INT is_InitCamera(ctypes.POINTER(HCAM) phCam, HWND hWnd)
    addfunc(lib, "is_InitCamera", restype = INT,
            argtypes = [ctypes.POINTER(HCAM), HWND],
            argnames = ["phCam", "hWnd"] )
    #  INT is_ExitCamera(HCAM hCam)
    addfunc(lib, "is_ExitCamera", restype = INT,
            argtypes = [HCAM],
            argnames = ["hCam"] )
    #  INT is_GetCameraInfo(HCAM hCam, PBOARDINFO pInfo)
    addfunc(lib, "is_GetCameraInfo", restype = INT,
            argtypes = [HCAM, PBOARDINFO],
            argnames = ["hCam", "pInfo"] )
    #  ULONG is_CameraStatus(HCAM hCam, INT nInfo, ULONG ulValue)
    addfunc(lib, "is_CameraStatus", restype = ULONG,
            argtypes = [HCAM, INT, ULONG],
            argnames = ["hCam", "nInfo", "ulValue"] )
    #  INT is_GetCameraType(HCAM hCam)
    addfunc(lib, "is_GetCameraType", restype = INT,
            argtypes = [HCAM],
            argnames = ["hCam"] )
    #  INT is_GetNumberOfCameras(ctypes.POINTER(INT) pnNumCams)
    addfunc(lib, "is_GetNumberOfCameras", restype = INT,
            argtypes = [ctypes.POINTER(INT)],
            argnames = ["pnNumCams"] )
    #  INT is_GetUsedBandwidth(HCAM hCam)
    addfunc(lib, "is_GetUsedBandwidth", restype = INT,
            argtypes = [HCAM],
            argnames = ["hCam"] )
    #  INT is_GetFrameTimeRange(HCAM hCam, ctypes.POINTER(ctypes.c_double) min, ctypes.POINTER(ctypes.c_double) max, ctypes.POINTER(ctypes.c_double) intervall)
    addfunc(lib, "is_GetFrameTimeRange", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)],
            argnames = ["hCam", "min", "max", "intervall"] )
    #  INT is_SetFrameRate(HCAM hCam, ctypes.c_double FPS, ctypes.POINTER(ctypes.c_double) newFPS)
    addfunc(lib, "is_SetFrameRate", restype = INT,
            argtypes = [HCAM, ctypes.c_double, ctypes.POINTER(ctypes.c_double)],
            argnames = ["hCam", "FPS", "newFPS"] )
    #  INT is_GetFramesPerSecond(HCAM hCam, ctypes.POINTER(ctypes.c_double) dblFPS)
    addfunc(lib, "is_GetFramesPerSecond", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(ctypes.c_double)],
            argnames = ["hCam", "dblFPS"] )
    #  INT is_GetSensorInfo(HCAM hCam, PSENSORINFO pInfo)
    addfunc(lib, "is_GetSensorInfo", restype = INT,
            argtypes = [HCAM, PSENSORINFO],
            argnames = ["hCam", "pInfo"] )
    #  INT is_GetRevisionInfo(HCAM hCam, PREVISIONINFO prevInfo)
    addfunc(lib, "is_GetRevisionInfo", restype = INT,
            argtypes = [HCAM, PREVISIONINFO],
            argnames = ["hCam", "prevInfo"] )
    #  INT is_EnableAutoExit(HCAM hCam, INT nMode)
    addfunc(lib, "is_EnableAutoExit", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "nMode"] )
    #  INT is_EnableMessage(HCAM hCam, INT which, HWND hWnd)
    addfunc(lib, "is_EnableMessage", restype = INT,
            argtypes = [HCAM, INT, HWND],
            argnames = ["hCam", "which", "hWnd"] )
    #  INT is_SetHardwareGain(HCAM hCam, INT nMaster, INT nRed, INT nGreen, INT nBlue)
    addfunc(lib, "is_SetHardwareGain", restype = INT,
            argtypes = [HCAM, INT, INT, INT, INT],
            argnames = ["hCam", "nMaster", "nRed", "nGreen", "nBlue"] )
    #  INT is_SetWhiteBalance(HCAM hCam, INT nMode)
    addfunc(lib, "is_SetWhiteBalance", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "nMode"] )
    #  INT is_SetWhiteBalanceMultipliers(HCAM hCam, ctypes.c_double dblRed, ctypes.c_double dblGreen, ctypes.c_double dblBlue)
    addfunc(lib, "is_SetWhiteBalanceMultipliers", restype = INT,
            argtypes = [HCAM, ctypes.c_double, ctypes.c_double, ctypes.c_double],
            argnames = ["hCam", "dblRed", "dblGreen", "dblBlue"] )
    #  INT is_GetWhiteBalanceMultipliers(HCAM hCam, ctypes.POINTER(ctypes.c_double) pdblRed, ctypes.POINTER(ctypes.c_double) pdblGreen, ctypes.POINTER(ctypes.c_double) pdblBlue)
    addfunc(lib, "is_GetWhiteBalanceMultipliers", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)],
            argnames = ["hCam", "pdblRed", "pdblGreen", "pdblBlue"] )
    #  INT is_SetColorCorrection(HCAM hCam, INT nEnable, ctypes.POINTER(ctypes.c_double) factors)
    addfunc(lib, "is_SetColorCorrection", restype = INT,
            argtypes = [HCAM, INT, ctypes.POINTER(ctypes.c_double)],
            argnames = ["hCam", "nEnable", "factors"] )
    #  INT is_SetSubSampling(HCAM hCam, INT mode)
    addfunc(lib, "is_SetSubSampling", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "mode"] )
    #  INT is_ForceTrigger(HCAM hCam)
    addfunc(lib, "is_ForceTrigger", restype = INT,
            argtypes = [HCAM],
            argnames = ["hCam"] )
    #  INT is_GetBusSpeed(HCAM hCam)
    addfunc(lib, "is_GetBusSpeed", restype = INT,
            argtypes = [HCAM],
            argnames = ["hCam"] )
    #  INT is_SetBinning(HCAM hCam, INT mode)
    addfunc(lib, "is_SetBinning", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "mode"] )
    #  INT is_ResetToDefault(HCAM hCam)
    addfunc(lib, "is_ResetToDefault", restype = INT,
            argtypes = [HCAM],
            argnames = ["hCam"] )
    #  INT is_SetCameraID(HCAM hCam, INT nID)
    addfunc(lib, "is_SetCameraID", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "nID"] )
    #  INT is_SetBayerConversion(HCAM hCam, INT nMode)
    addfunc(lib, "is_SetBayerConversion", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "nMode"] )
    #  INT is_SetHardwareGamma(HCAM hCam, INT nMode)
    addfunc(lib, "is_SetHardwareGamma", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "nMode"] )
    #  INT is_GetCameraList(PUC480_CAMERA_LIST pucl)
    addfunc(lib, "is_GetCameraList", restype = INT,
            argtypes = [PUC480_CAMERA_LIST],
            argnames = ["pucl"] )
    #  INT is_SetAutoParameter(HCAM hCam, INT param, ctypes.POINTER(ctypes.c_double) pval1, ctypes.POINTER(ctypes.c_double) pval2)
    addfunc(lib, "is_SetAutoParameter", restype = INT,
            argtypes = [HCAM, INT, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)],
            argnames = ["hCam", "param", "pval1", "pval2"] )
    #  INT is_GetAutoInfo(HCAM hCam, ctypes.POINTER(UC480_AUTO_INFO) pInfo)
    addfunc(lib, "is_GetAutoInfo", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(UC480_AUTO_INFO)],
            argnames = ["hCam", "pInfo"] )
    #  INT is_GetImageHistogram(HCAM hCam, ctypes.c_int nID, INT ColorMode, ctypes.POINTER(DWORD) pHistoMem)
    addfunc(lib, "is_GetImageHistogram", restype = INT,
            argtypes = [HCAM, ctypes.c_int, INT, ctypes.POINTER(DWORD)],
            argnames = ["hCam", "nID", "ColorMode", "pHistoMem"] )
    #  INT is_SetTriggerDelay(HCAM hCam, INT nTriggerDelay)
    addfunc(lib, "is_SetTriggerDelay", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "nTriggerDelay"] )
    #  INT is_SetGainBoost(HCAM hCam, INT mode)
    addfunc(lib, "is_SetGainBoost", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "mode"] )
    #  INT is_SetGlobalShutter(HCAM hCam, INT mode)
    addfunc(lib, "is_SetGlobalShutter", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "mode"] )
    #  INT is_SetExtendedRegister(HCAM hCam, INT index, WORD value)
    addfunc(lib, "is_SetExtendedRegister", restype = INT,
            argtypes = [HCAM, INT, WORD],
            argnames = ["hCam", "index", "value"] )
    #  INT is_GetExtendedRegister(HCAM hCam, INT index, ctypes.POINTER(WORD) pwValue)
    addfunc(lib, "is_GetExtendedRegister", restype = INT,
            argtypes = [HCAM, INT, ctypes.POINTER(WORD)],
            argnames = ["hCam", "index", "pwValue"] )
    #  INT is_SetHWGainFactor(HCAM hCam, INT nMode, INT nFactor)
    addfunc(lib, "is_SetHWGainFactor", restype = INT,
            argtypes = [HCAM, INT, INT],
            argnames = ["hCam", "nMode", "nFactor"] )
    #  INT is_Renumerate(HCAM hCam, INT nMode)
    addfunc(lib, "is_Renumerate", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "nMode"] )
    #  INT is_WriteI2C(HCAM hCam, INT nDeviceAddr, INT nRegisterAddr, ctypes.POINTER(BYTE) pbData, INT nLen)
    addfunc(lib, "is_WriteI2C", restype = INT,
            argtypes = [HCAM, INT, INT, ctypes.POINTER(BYTE), INT],
            argnames = ["hCam", "nDeviceAddr", "nRegisterAddr", "pbData", "nLen"] )
    #  INT is_ReadI2C(HCAM hCam, INT nDeviceAddr, INT nRegisterAddr, ctypes.POINTER(BYTE) pbData, INT nLen)
    addfunc(lib, "is_ReadI2C", restype = INT,
            argtypes = [HCAM, INT, INT, ctypes.POINTER(BYTE), INT],
            argnames = ["hCam", "nDeviceAddr", "nRegisterAddr", "pbData", "nLen"] )
    #  INT is_GetHdrMode(HCAM hCam, ctypes.POINTER(INT) Mode)
    addfunc(lib, "is_GetHdrMode", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(INT)],
            argnames = ["hCam", "Mode"] )
    #  INT is_EnableHdr(HCAM hCam, INT Enable)
    addfunc(lib, "is_EnableHdr", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "Enable"] )
    #  INT is_SetHdrKneepoints(HCAM hCam, ctypes.POINTER(KNEEPOINTARRAY) KneepointArray, INT KneepointArraySize)
    addfunc(lib, "is_SetHdrKneepoints", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(KNEEPOINTARRAY), INT],
            argnames = ["hCam", "KneepointArray", "KneepointArraySize"] )
    #  INT is_GetHdrKneepoints(HCAM hCam, ctypes.POINTER(KNEEPOINTARRAY) KneepointArray, INT KneepointArraySize)
    addfunc(lib, "is_GetHdrKneepoints", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(KNEEPOINTARRAY), INT],
            argnames = ["hCam", "KneepointArray", "KneepointArraySize"] )
    #  INT is_GetHdrKneepointInfo(HCAM hCam, ctypes.POINTER(KNEEPOINTINFO) KneepointInfo, INT KneepointInfoSize)
    addfunc(lib, "is_GetHdrKneepointInfo", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(KNEEPOINTINFO), INT],
            argnames = ["hCam", "KneepointInfo", "KneepointInfoSize"] )
    #  INT is_SetOptimalCameraTiming(HCAM hCam, INT Mode, INT Timeout, ctypes.POINTER(INT) pMaxPxlClk, ctypes.POINTER(ctypes.c_double) pMaxFrameRate)
    addfunc(lib, "is_SetOptimalCameraTiming", restype = INT,
            argtypes = [HCAM, INT, INT, ctypes.POINTER(INT), ctypes.POINTER(ctypes.c_double)],
            argnames = ["hCam", "Mode", "Timeout", "pMaxPxlClk", "pMaxFrameRate"] )
    #  INT is_GetSupportedTestImages(HCAM hCam, ctypes.POINTER(INT) SupportedTestImages)
    addfunc(lib, "is_GetSupportedTestImages", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(INT)],
            argnames = ["hCam", "SupportedTestImages"] )
    #  INT is_GetTestImageValueRange(HCAM hCam, INT TestImage, ctypes.POINTER(INT) TestImageValueMin, ctypes.POINTER(INT) TestImageValueMax)
    addfunc(lib, "is_GetTestImageValueRange", restype = INT,
            argtypes = [HCAM, INT, ctypes.POINTER(INT), ctypes.POINTER(INT)],
            argnames = ["hCam", "TestImage", "TestImageValueMin", "TestImageValueMax"] )
    #  INT is_SetSensorTestImage(HCAM hCam, INT Param1, INT Param2)
    addfunc(lib, "is_SetSensorTestImage", restype = INT,
            argtypes = [HCAM, INT, INT],
            argnames = ["hCam", "Param1", "Param2"] )
    #  INT is_GetColorConverter(HCAM hCam, INT ColorMode, ctypes.POINTER(INT) pCurrentConvertMode, ctypes.POINTER(INT) pDefaultConvertMode, ctypes.POINTER(INT) pSupportedConvertModes)
    addfunc(lib, "is_GetColorConverter", restype = INT,
            argtypes = [HCAM, INT, ctypes.POINTER(INT), ctypes.POINTER(INT), ctypes.POINTER(INT)],
            argnames = ["hCam", "ColorMode", "pCurrentConvertMode", "pDefaultConvertMode", "pSupportedConvertModes"] )
    #  INT is_SetColorConverter(HCAM hCam, INT ColorMode, INT ConvertMode)
    addfunc(lib, "is_SetColorConverter", restype = INT,
            argtypes = [HCAM, INT, INT],
            argnames = ["hCam", "ColorMode", "ConvertMode"] )
    #  INT is_WaitForNextImage(HCAM hCam, UINT timeout, ctypes.POINTER(ctypes.c_char_p) ppcMem, ctypes.POINTER(INT) imageID)
    addfunc(lib, "is_WaitForNextImage", restype = INT,
            argtypes = [HCAM, UINT, ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(INT)],
            argnames = ["hCam", "timeout", "ppcMem", "imageID"] )
    #  INT is_InitImageQueue(HCAM hCam, INT nMode)
    addfunc(lib, "is_InitImageQueue", restype = INT,
            argtypes = [HCAM, INT],
            argnames = ["hCam", "nMode"] )
    #  INT is_ExitImageQueue(HCAM hCam)
    addfunc(lib, "is_ExitImageQueue", restype = INT,
            argtypes = [HCAM],
            argnames = ["hCam"] )
    #  INT is_SetTimeout(HCAM hCam, UINT nMode, UINT Timeout)
    addfunc(lib, "is_SetTimeout", restype = INT,
            argtypes = [HCAM, UINT, UINT],
            argnames = ["hCam", "nMode", "Timeout"] )
    #  INT is_GetTimeout(HCAM hCam, UINT nMode, ctypes.POINTER(UINT) pTimeout)
    addfunc(lib, "is_GetTimeout", restype = INT,
            argtypes = [HCAM, UINT, ctypes.POINTER(UINT)],
            argnames = ["hCam", "nMode", "pTimeout"] )
    #  INT is_GetDuration(HCAM hCam, UINT nMode, ctypes.POINTER(INT) pnTime)
    addfunc(lib, "is_GetDuration", restype = INT,
            argtypes = [HCAM, UINT, ctypes.POINTER(INT)],
            argnames = ["hCam", "nMode", "pnTime"] )
    #  INT is_GetSensorScalerInfo(HCAM hCam, ctypes.POINTER(SENSORSCALERINFO) pSensorScalerInfo, INT nSensorScalerInfoSize)
    addfunc(lib, "is_GetSensorScalerInfo", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(SENSORSCALERINFO), INT],
            argnames = ["hCam", "pSensorScalerInfo", "nSensorScalerInfoSize"] )
    #  INT is_SetSensorScaler(HCAM hCam, UINT nMode, ctypes.c_double dblFactor)
    addfunc(lib, "is_SetSensorScaler", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_double],
            argnames = ["hCam", "nMode", "dblFactor"] )
    #  INT is_GetImageInfo(HCAM hCam, INT nImageBufferID, ctypes.POINTER(UC480IMAGEINFO) pImageInfo, INT nImageInfoSize)
    addfunc(lib, "is_GetImageInfo", restype = INT,
            argtypes = [HCAM, INT, ctypes.POINTER(UC480IMAGEINFO), INT],
            argnames = ["hCam", "nImageBufferID", "pImageInfo", "nImageInfoSize"] )
    #  INT is_ImageFormat(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
    addfunc(lib, "is_ImageFormat", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "nSizeOfParam"] )
    #  INT is_FaceDetection(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
    addfunc(lib, "is_FaceDetection", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "nSizeOfParam"] )
    #  INT is_Focus(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
    addfunc(lib, "is_Focus", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "nSizeOfParam"] )
    #  INT is_ImageStabilization(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
    addfunc(lib, "is_ImageStabilization", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "nSizeOfParam"] )
    #  INT is_ScenePreset(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
    addfunc(lib, "is_ScenePreset", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "nSizeOfParam"] )
    #  INT is_Zoom(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
    addfunc(lib, "is_Zoom", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "nSizeOfParam"] )
    #  INT is_Sharpness(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
    addfunc(lib, "is_Sharpness", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "nSizeOfParam"] )
    #  INT is_Saturation(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
    addfunc(lib, "is_Saturation", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "nSizeOfParam"] )
    #  INT is_TriggerDebounce(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
    addfunc(lib, "is_TriggerDebounce", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "nSizeOfParam"] )
    #  INT is_ColorTemperature(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT nSizeOfParam)
    addfunc(lib, "is_ColorTemperature", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "nSizeOfParam"] )
    #  INT is_DirectRenderer(HCAM hCam, UINT nMode, ctypes.c_void_p pParam, UINT SizeOfParam)
    addfunc(lib, "is_DirectRenderer", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nMode", "pParam", "SizeOfParam"] )
    #  INT is_HotPixel(HCAM hCam, UINT nMode, ctypes.c_void_p pParam, UINT SizeOfParam)
    addfunc(lib, "is_HotPixel", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nMode", "pParam", "SizeOfParam"] )
    #  INT is_AOI(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT SizeOfParam)
    addfunc(lib, "is_AOI", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "SizeOfParam"] )
    #  INT is_Transfer(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_Transfer", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_BootBoost(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_BootBoost", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_DeviceFeature(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_DeviceFeature", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_Exposure(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_Exposure", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_Trigger(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_Trigger", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_DeviceInfo(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_DeviceInfo", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_Callback(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_Callback", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_OptimalCameraTiming(HCAM hCam, UINT u32Command, ctypes.c_void_p pParam, UINT u32SizeOfParam)
    addfunc(lib, "is_OptimalCameraTiming", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "u32Command", "pParam", "u32SizeOfParam"] )
    #  INT is_SetStarterFirmware(HCAM hCam, ctypes.c_char_p pcFilepath, UINT uFilepathLen)
    addfunc(lib, "is_SetStarterFirmware", restype = INT,
            argtypes = [HCAM, ctypes.c_char_p, UINT],
            argnames = ["hCam", "pcFilepath", "uFilepathLen"] )
    #  INT is_SetPacketFilter(INT iAdapterID, UINT uFilterSetting)
    addfunc(lib, "is_SetPacketFilter", restype = INT,
            argtypes = [INT, UINT],
            argnames = ["iAdapterID", "uFilterSetting"] )
    #  INT is_GetComportNumber(HCAM hCam, ctypes.POINTER(UINT) pComportNumber)
    addfunc(lib, "is_GetComportNumber", restype = INT,
            argtypes = [HCAM, ctypes.POINTER(UINT)],
            argnames = ["hCam", "pComportNumber"] )
    #  INT is_IpConfig(INT iID, UC480_ETH_ADDR_MAC mac, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_IpConfig", restype = INT,
            argtypes = [INT, UC480_ETH_ADDR_MAC, UINT, ctypes.c_void_p, UINT],
            argnames = ["iID", "mac", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_Configuration(UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_Configuration", restype = INT,
            argtypes = [UINT, ctypes.c_void_p, UINT],
            argnames = ["nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_IO(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_IO", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_AutoParameter(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_AutoParameter", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_Convert(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_Convert", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_ParameterSet(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_ParameterSet", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_EdgeEnhancement(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_EdgeEnhancement", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_PixelClock(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_PixelClock", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_ImageFile(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_ImageFile", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_Blacklevel(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_Blacklevel", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_ImageBuffer(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_ImageBuffer", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_Measure(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_Measure", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_LUT(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParams)
    addfunc(lib, "is_LUT", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParams"] )
    #  INT is_Gamma(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParams)
    addfunc(lib, "is_Gamma", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParams"] )
    #  INT is_Memory(HCAM hf, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParam)
    addfunc(lib, "is_Memory", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hf", "nCommand", "pParam", "cbSizeOfParam"] )
    #  INT is_Multicast(HCAM hCam, UINT nCommand, ctypes.c_void_p pParam, UINT cbSizeOfParams)
    addfunc(lib, "is_Multicast", restype = INT,
            argtypes = [HCAM, UINT, ctypes.c_void_p, UINT],
            argnames = ["hCam", "nCommand", "pParam", "cbSizeOfParams"] )


