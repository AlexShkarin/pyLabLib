##########   This file is generated automatically based on sc2_defs.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class CAMERATYPE(enum.IntEnum):
    CAMERATYPE_PCO1200HS                     = _int32(0x0100)
    CAMERATYPE_PCO1300                       = _int32(0x0200)
    CAMERATYPE_PCO1600                       = _int32(0x0220)
    CAMERATYPE_PCO2000                       = _int32(0x0240)
    CAMERATYPE_PCO4000                       = _int32(0x0260)
    CAMERATYPE_ROCHEHTC                      = _int32(0x0800)
    CAMERATYPE_284XS                         = _int32(0x0800)
    CAMERATYPE_KODAK1300OEM                  = _int32(0x0820)
    CAMERATYPE_PCO1400                       = _int32(0x0830)
    CAMERATYPE_NEWGEN                        = _int32(0x0840)
    CAMERATYPE_PROVEHR                       = _int32(0x0850)
    CAMERATYPE_PCO_USBPIXELFLY               = _int32(0x0900)
    CAMERATYPE_PCO_DIMAX_STD                 = _int32(0x1000)
    CAMERATYPE_PCO_DIMAX_TV                  = _int32(0x1010)
    CAMERATYPE_PCO_DIMAX_AUTOMOTIVE          = _int32(0x1020)
    CAMERATYPE_PCO_DIMAX_CS                  = _int32(0x1020)
    CAMERASUBTYPE_PCO_DIMAX_Weisscam         = _int32(0x0064)
    CAMERASUBTYPE_PCO_DIMAX_HD               = _int32(0x80FF)
    CAMERASUBTYPE_PCO_DIMAX_HD_plus          = _int32(0xC0FF)
    CAMERASUBTYPE_PCO_DIMAX_X35              = _int32(0x00C8)
    CAMERASUBTYPE_PCO_DIMAX_HS1              = _int32(0x207F)
    CAMERASUBTYPE_PCO_DIMAX_HS2              = _int32(0x217F)
    CAMERASUBTYPE_PCO_DIMAX_HS4              = _int32(0x237F)
    CAMERASUBTYPE_PCO_DIMAX_CS_AM_DEPRECATED = _int32(0x407F)
    CAMERASUBTYPE_PCO_DIMAX_CS_1             = _int32(0x417F)
    CAMERASUBTYPE_PCO_DIMAX_CS_2             = _int32(0x427F)
    CAMERASUBTYPE_PCO_DIMAX_CS_3             = _int32(0x437F)
    CAMERASUBTYPE_PCO_DIMAX_CS_4             = _int32(0x447F)
    CAMERATYPE_SC3_SONYQE                    = _int32(0x1200)
    CAMERATYPE_SC3_EMTI                      = _int32(0x1210)
    CAMERATYPE_SC3_KODAK4800                 = _int32(0x1220)
    CAMERATYPE_PCO_EDGE                      = _int32(0x1300)
    CAMERATYPE_PCO_EDGE_42                   = _int32(0x1302)
    CAMERATYPE_PCO_EDGE_GL                   = _int32(0x1310)
    CAMERATYPE_PCO_EDGE_USB3                 = _int32(0x1320)
    CAMERATYPE_PCO_EDGE_HS                   = _int32(0x1340)
    CAMERATYPE_PCO_EDGE_MT                   = _int32(0x1304)
    CAMERASUBTYPE_PCO_EDGE_SPRINGFIELD       = _int32(0x0006)
    CAMERASUBTYPE_PCO_EDGE_31                = _int32(0x0031)
    CAMERASUBTYPE_PCO_EDGE_42                = _int32(0x0042)
    CAMERASUBTYPE_PCO_EDGE_55                = _int32(0x0055)
    CAMERASUBTYPE_PCO_EDGE_DEVELOPMENT       = _int32(0x0100)
    CAMERASUBTYPE_PCO_EDGE_X2                = _int32(0x0200)
    CAMERASUBTYPE_PCO_EDGE_RESOLFT           = _int32(0x0300)
    CAMERASUBTYPE_PCO_EDGE_GOLD              = _int32(0x0FF0)
    CAMERASUBTYPE_PCO_EDGE_DUAL_CLOCK        = _int32(0x000D)
    CAMERASUBTYPE_PCO_EDGE_DICAM             = _int32(0xDC00)
    CAMERASUBTYPE_PCO_EDGE_42_LT             = _int32(0x8042)
    CAMERATYPE_PCO_FLIM                      = _int32(0x1400)
    CAMERATYPE_PCO_FLOW                      = _int32(0x1500)
    CAMERATYPE_PCO_PANDA                     = _int32(0x1600)
    CAMERATYPE_PCO_FAMILY_PANDA              = _int32(0x1600)
    CAMERATYPE_PCO_FAMILY_EDGE               = _int32(0x1800)
    CAMERATYPE_PCO_FAMILY_DICAM              = _int32(0x1700)
    CAMERATYPE_PCO_FAMILY_DIMAX              = _int32(0x1900)
    CAMERASUBTYPE_PCO_PANDA_42               = _int32(0x0000)
    CAMERASUBTYPE_PCO_PANDA_42_BI            = _int32(0x0001)
    CAMERASUBTYPE_PCO_PANDA_150              = _int32(0x0002)
    CAMERASUBTYPE_PCO_EDGE_42_BI             = _int32(0x0001)
    CAMERASUBTYPE_PCO_DICAM_C1               = _int32(0x0001)
    CAMERASUBTYPE_PCO_DICAM_C2               = _int32(0x0002)
    CAMERASUBTYPE_PCO_DICAM_C3               = _int32(0x0003)
    CAMERASUBTYPE_PCO_DICAM_C4               = _int32(0x0004)
dCAMERATYPE={a.name:a.value for a in CAMERATYPE}
drCAMERATYPE={a.value:a.name for a in CAMERATYPE}


class INTERFACE_TYPE(enum.IntEnum):
    INTERFACE_FIREWIRE     = _int32(0x0001)
    INTERFACE_CAMERALINK   = _int32(0x0002)
    INTERFACE_USB          = _int32(0x0003)
    INTERFACE_ETHERNET     = _int32(0x0004)
    INTERFACE_SERIAL       = _int32(0x0005)
    INTERFACE_USB3         = _int32(0x0006)
    INTERFACE_CAMERALINKHS = _int32(0x0007)
    INTERFACE_COAXPRESS    = _int32(0x0008)
    INTERFACE_USB31_GEN1   = _int32(0x0009)
dINTERFACE_TYPE={a.name:a.value for a in INTERFACE_TYPE}
drINTERFACE_TYPE={a.value:a.name for a in INTERFACE_TYPE}


class USB_IDS(enum.IntEnum):
    USB_VID                    = _int32(0x1CB2)
    USB_PID_IF_GIGEUSB_20      = _int32(0x0001)
    USB_PID_CAM_PIXFLY_20      = _int32(0x0002)
    USB_PID_IF_GIGEUSB_30      = _int32(0x0003)
    USB_PID_IF_GIGEUSB_30_B1   = _int32(0x0004)
    USB_PID_IF_GIGEUSB_30_B2   = _int32(0x0005)
    USB_PID_CAM_EDGEUSB_30     = _int32(0x0006)
    USB_PID_CAM_FLOW_20        = _int32(0x0007)
    USB_PID_CAM_EDGEHS_20      = _int32(0x0008)
    USB_PID_P5CTR              = _int32(0x0009)
    USB_PID_P5CTR_PROD         = _int32(0x000A)
    USB_PID_CAM_PANDA_20       = _int32(0x000B)
    USB_PID_CAM_PANDA_30       = _int32(0x000C)
    USB_PID_DP3_MAIN           = _int32(0x000D)
    USB_PID_CAM_EDGE_42BI_PRG  = _int32(0x000E)
    USB_PID_CAM_EDGE_42BI      = _int32(0x000F)
    USB_PID_CAM_PANDA_42BI_PRG = _int32(0x0010)
    USB_PID_CAM_PANDA_42BI     = _int32(0x0011)
dUSB_IDS={a.name:a.value for a in USB_IDS}
drUSB_IDS={a.value:a.name for a in USB_IDS}


class USB_EPS(enum.IntEnum):
    USB_EP_FX2_CTRL_IN       = _int32(0x84)
    USB_EP_FX2_CTRL_OUT      = _int32(0x02)
    USB_EP_FX2_IMG_IN        = _int32(0x86)
    USB_EP_FX3_CTRL_IN       = _int32(0x81)
    USB_EP_FX3_CTRL_OUT      = _int32(0x01)
    USB_EP_FX3_IMG_IN        = _int32(0x82)
    USB_EP_AVR32_CTRL_IN     = _int32(0x81)
    USB_EP_AVR32_CTRL_OUT    = _int32(0x02)
    USB_EP_DIMAX_CS_CTRL_IN  = _int32(0x81)
    USB_EP_DIMAX_CS_CTRL_OUT = _int32(0x01)
dUSB_EPS={a.name:a.value for a in USB_EPS}
drUSB_EPS={a.value:a.name for a in USB_EPS}


class WARNING(enum.IntEnum):
    WARNING_POWERSUPPLYVOLTAGERANGE = _int32(0x00000001)
    WARNING_POWERSUPPLYTEMPERATURE  = _int32(0x00000002)
    WARNING_CAMERATEMPERATURE       = _int32(0x00000004)
    WARNING_SENSORTEMPERATURE       = _int32(0x00000008)
    WARNING_EXTERNAL_BATTERY_LOW    = _int32(0x00000010)
    WARNING_OFFSET_REGULATION_RANGE = _int32(0x00000020)
    WARNING_CAMERARAM               = _int32(0x00020000)
dWARNING={a.name:a.value for a in WARNING}
drWARNING={a.value:a.name for a in WARNING}


class ERROR(enum.IntEnum):
    ERROR_POWERSUPPLYVOLTAGERANGE = _int32(0x00000001)
    ERROR_POWERSUPPLYTEMPERATURE  = _int32(0x00000002)
    ERROR_CAMERATEMPERATURE       = _int32(0x00000004)
    ERROR_SENSORTEMPERATURE       = _int32(0x00000008)
    ERROR_EXTERNAL_BATTERY_LOW    = _int32(0x00000010)
    ERROR_FIRMWARE_CORRUPTED      = _int32(0x00000020)
    ERROR_CAMERAINTERFACE         = _int32(0x00010000)
    ERROR_CAMERARAM               = _int32(0x00020000)
    ERROR_CAMERAMAINBOARD         = _int32(0x00040000)
    ERROR_CAMERAHEADBOARD         = _int32(0x00080000)
dERROR={a.name:a.value for a in ERROR}
drERROR={a.value:a.name for a in ERROR}


class STATUS(enum.IntEnum):
    STATUS_DEFAULT_STATE         = _int32(0x00000001)
    STATUS_SETTINGS_VALID        = _int32(0x00000002)
    STATUS_RECORDING_ON          = _int32(0x00000004)
    STATUS_READ_IMAGE_ON         = _int32(0x00000008)
    STATUS_FRAMERATE_VALID       = _int32(0x00000010)
    STATUS_SEQ_STOP_TRIGGERED    = _int32(0x00000020)
    STATUS_LOCKED_TO_EXTSYNC     = _int32(0x00000040)
    STATUS_EXT_BATTERY_AVAILABLE = _int32(0x00000080)
    STATUS_IS_IN_POWERSAVE       = _int32(0x00000100)
    STATUS_POWERSAVE_LEFT        = _int32(0x00000200)
    STATUS_LOCKED_TO_IRIG        = _int32(0x00000400)
    STATUS_IS_IN_BOOTLOADER      = _int32(0x80000000)
dSTATUS={a.name:a.value for a in STATUS}
drSTATUS={a.value:a.name for a in STATUS}


class SENSORTYPE(enum.IntEnum):
    SENSOR_ICX285AL               = _int32(0x0010)
    SENSOR_ICX285AK               = _int32(0x0011)
    SENSOR_ICX263AL               = _int32(0x0020)
    SENSOR_ICX263AK               = _int32(0x0021)
    SENSOR_ICX274AL               = _int32(0x0030)
    SENSOR_ICX274AK               = _int32(0x0031)
    SENSOR_ICX407AL               = _int32(0x0040)
    SENSOR_ICX407AK               = _int32(0x0041)
    SENSOR_ICX414AL               = _int32(0x0050)
    SENSOR_ICX414AK               = _int32(0x0051)
    SENSOR_ICX407BLA              = _int32(0x0060)
    SENSOR_KAI2000M               = _int32(0x0110)
    SENSOR_KAI2000CM              = _int32(0x0111)
    SENSOR_KAI2001M               = _int32(0x0120)
    SENSOR_KAI2001CM              = _int32(0x0121)
    SENSOR_KAI2002M               = _int32(0x0122)
    SENSOR_KAI2002CM              = _int32(0x0123)
    SENSOR_KAI4010M               = _int32(0x0130)
    SENSOR_KAI4010CM              = _int32(0x0131)
    SENSOR_KAI4011M               = _int32(0x0132)
    SENSOR_KAI4011CM              = _int32(0x0133)
    SENSOR_KAI4020M               = _int32(0x0140)
    SENSOR_KAI4020CM              = _int32(0x0141)
    SENSOR_KAI4021M               = _int32(0x0142)
    SENSOR_KAI4021CM              = _int32(0x0143)
    SENSOR_KAI4022M               = _int32(0x0144)
    SENSOR_KAI4022CM              = _int32(0x0145)
    SENSOR_KAI11000M              = _int32(0x0150)
    SENSOR_KAI11000CM             = _int32(0x0151)
    SENSOR_KAI11002M              = _int32(0x0152)
    SENSOR_KAI11002CM             = _int32(0x0153)
    SENSOR_KAI16000AXA            = _int32(0x0160)
    SENSOR_KAI16000CXA            = _int32(0x0161)
    SENSOR_MV13BW                 = _int32(0x1010)
    SENSOR_MV13COL                = _int32(0x1011)
    SENSOR_CIS2051_V1_FI_BW       = _int32(0x2000)
    SENSOR_CIS2051_V1_FI_COL      = _int32(0x2001)
    SENSOR_CIS1042_V1_FI_BW       = _int32(0x2002)
    SENSOR_CIS2051_V1_BI_BW       = _int32(0x2010)
    SENSOR_TC285SPD               = _int32(0x2120)
    SENSOR_CYPRESS_RR_V1_BW       = _int32(0x3000)
    SENSOR_CYPRESS_RR_V1_COL      = _int32(0x3001)
    SENSOR_CMOSIS_CMV12000_BW     = _int32(0x3100)
    SENSOR_CMOSIS_CMV12000_COL    = _int32(0x3101)
    SENSOR_QMFLIM_V2B_BW          = _int32(0x4000)
    SENSOR_GPIXEL_GSENSE2020_BW   = _int32(0x5000)
    SENSOR_GPIXEL_GSENSE2020_COL  = _int32(0x5001)
    SENSOR_GPIXEL_GSENSE2020BI_BW = _int32(0x5002)
    SENSOR_GPIXEL_GSENSE5130_BW   = _int32(0x5004)
    SENSOR_GPIXEL_GSENSE5130_COL  = _int32(0x5005)
dSENSORTYPE={a.name:a.value for a in SENSORTYPE}
drSENSORTYPE={a.value:a.name for a in SENSORTYPE}


class CAPS1(enum.IntEnum):
    GENERALCAPS1_NOISE_FILTER                    = _int32(0x00000001)
    GENERALCAPS1_HOTPIX_FILTER                   = _int32(0x00000002)
    GENERALCAPS1_HOTPIX_ONLY_WITH_NOISE_FILTER   = _int32(0x00000004)
    GENERALCAPS1_TIMESTAMP_ASCII_ONLY            = _int32(0x00000008)
    GENERALCAPS1_DATAFORMAT2X12                  = _int32(0x00000010)
    GENERALCAPS1_RECORD_STOP                     = _int32(0x00000020)
    GENERALCAPS1_HOT_PIXEL_CORRECTION            = _int32(0x00000040)
    GENERALCAPS1_NO_EXTEXPCTRL                   = _int32(0x00000080)
    GENERALCAPS1_NO_TIMESTAMP                    = _int32(0x00000100)
    GENERALCAPS1_NO_ACQUIREMODE                  = _int32(0x00000200)
    GENERALCAPS1_DATAFORMAT4X16                  = _int32(0x00000400)
    GENERALCAPS1_DATAFORMAT5X16                  = _int32(0x00000800)
    GENERALCAPS1_NO_RECORDER                     = _int32(0x00001000)
    GENERALCAPS1_FAST_TIMING                     = _int32(0x00002000)
    GENERALCAPS1_METADATA                        = _int32(0x00004000)
    GENERALCAPS1_SETFRAMERATE_ENABLED            = _int32(0x00008000)
    GENERALCAPS1_CDI_MODE                        = _int32(0x00010000)
    GENERALCAPS1_CCM                             = _int32(0x00020000)
    GENERALCAPS1_EXTERNAL_SYNC                   = _int32(0x00040000)
    GENERALCAPS1_NO_GLOBAL_SHUTTER               = _int32(0x00080000)
    GENERALCAPS1_GLOBAL_RESET_MODE               = _int32(0x00100000)
    GENERALCAPS1_EXT_ACQUIRE                     = _int32(0x00200000)
    GENERALCAPS1_FAN_LED_CONTROL                 = _int32(0x00400000)
    GENERALCAPS1_ROI_VERT_SYMM_TO_HORZ_AXIS      = _int32(0x00800000)
    GENERALCAPS1_ROI_HORZ_SYMM_TO_VERT_AXIS      = _int32(0x01000000)
    GENERALCAPS1_COOLING_SETPOINTS               = _int32(0x02000000)
    GENERALCAPS1_USER_INTERFACE                  = _int32(0x04000000)
    GENERALCAPS1_ENHANCED_DESCRIPTOR_INTENSIFIED = _int32(0x20000000)
    GENERALCAPS1_HW_IO_SIGNAL_DESCRIPTOR         = _int32(0x40000000)
    GENERALCAPS1_ENHANCED_DESCRIPTOR_2           = _int32(0x80000000)
dCAPS1={a.name:a.value for a in CAPS1}
drCAPS1={a.value:a.name for a in CAPS1}


class CAPS3(enum.IntEnum):
    GENERALCAPS3_HDSDI_1G5          = _int32(0x00000001)
    GENERALCAPS3_HDSDI_3G           = _int32(0x00000002)
    GENERALCAPS3_IRIG_B_UNMODULATED = _int32(0x00000004)
    GENERALCAPS3_IRIG_B_MODULATED   = _int32(0x00000008)
    GENERALCAPS3_CAMERA_SYNC        = _int32(0x00000010)
    GENERALCAPS3_RESERVED0          = _int32(0x00000020)
    GENERALCAPS3_HS_READOUT_MODE    = _int32(0x00000040)
    GENERALCAPS3_EXT_SYNC_1HZ_MODE  = _int32(0x00000080)
dCAPS3={a.name:a.value for a in CAPS3}
drCAPS3={a.value:a.name for a in CAPS3}


class BATTERY(enum.IntEnum):
    BATTERY_STATUS_MAINS_AVAILABLE = _int32(0x0001)
    BATTERY_STATUS_CONNECTED       = _int32(0x0002)
    BATTERY_STATUS_CHARGING        = _int32(0x0004)
dBATTERY={a.name:a.value for a in BATTERY}
drBATTERY={a.value:a.name for a in BATTERY}


class POWERSAVE(enum.IntEnum):
    POWERSAVE_MODE_OFF                = _int32(0x0000)
    POWERSAVE_MODE_ON                 = _int32(0x0001)
    POWERSAVE_MODE_DO_NOT_USE_BATTERY = _int32(0x0002)
dPOWERSAVE={a.name:a.value for a in POWERSAVE}
drPOWERSAVE={a.value:a.name for a in POWERSAVE}


class PIXELRATE(enum.IntEnum):
    PIXELRATE_10MHZ = _int32(10000000)
    PIXELRATE_20MHZ = _int32(20000000)
    PIXELRATE_40MHZ = _int32(40000000)
    PIXELRATE_5MHZ  = _int32(5000000)
dPIXELRATE={a.name:a.value for a in PIXELRATE}
drPIXELRATE={a.value:a.name for a in PIXELRATE}


class FRAMERATE(enum.IntEnum):
    SET_FRAMERATE_MODE_AUTO                          = _int32(0x0000)
    SET_FRAMERATE_MODE_FRAMERATE_HAS_PRIORITY        = _int32(0x0001)
    SET_FRAMERATE_MODE_EXPTIME_HAS_PRIORITY          = _int32(0x0002)
    SET_FRAMERATE_MODE_STRICT                        = _int32(0x0003)
    SET_FRAMERATE_STATUS_OK                          = _int32(0x0000)
    SET_FRAMERATE_STATUS_FPS_LIMITED_BY_READOUT      = _int32(0x0001)
    SET_FRAMERATE_STATUS_FPS_LIMITED_BY_EXPTIME      = _int32(0x0002)
    SET_FRAMERATE_STATUS_EXPTIME_CUT_TO_FRAMETIME    = _int32(0x0004)
    SET_FRAMERATE_STATUS_NOT_YET_VALIDATED           = _int32(0x8000)
    SET_FRAMERATE_STATUS_ERROR_SETTINGS_INCONSISTENT = _int32(0x8001)
dFRAMERATE={a.name:a.value for a in FRAMERATE}
drFRAMERATE={a.value:a.name for a in FRAMERATE}


class TRIGGER(enum.IntEnum):
    TRIGGER_MODE_AUTOTRIGGER                  = _int32(0x0000)
    TRIGGER_MODE_SOFTWARETRIGGER              = _int32(0x0001)
    TRIGGER_MODE_EXTERNALTRIGGER              = _int32(0x0002)
    TRIGGER_MODE_EXTERNALEXPOSURECONTROL      = _int32(0x0003)
    TRIGGER_MODE_SOURCE_HDSDI                 = _int32(0x0102)
    TRIGGER_MODE_EXTERNAL_SYNCHRONIZED        = _int32(0x0004)
    TRIGGER_MODE_FAST_EXTERNALEXPOSURECONTROL = _int32(0x0005)
    TRIGGER_MODE_EXTERNAL_CDS                 = _int32(0x0006)
    TRIGGER_MODE_SLOW_EXTERNALEXPOSURECONTROL = _int32(0x0007)
dTRIGGER={a.name:a.value for a in TRIGGER}
drTRIGGER={a.value:a.name for a in TRIGGER}


class ACQUIRE_MODE(enum.IntEnum):
    ACQUIRE_MODE_AUTO                   = _int32(0x0000)
    ACQUIRE_MODE_EXTERNAL               = _int32(0x0001)
    ACQUIRE_MODE_EXTERNAL_FRAME_TRIGGER = _int32(0x0002)
    ACQUIRE_MODE_USE_FOR_LIVEVIEW       = _int32(0x0003)
    ACQUIRE_MODE_IMAGE_SEQUENCE         = _int32(0x0004)
dACQUIRE_MODE={a.name:a.value for a in ACQUIRE_MODE}
drACQUIRE_MODE={a.value:a.name for a in ACQUIRE_MODE}


class ACQUIRE_CONTROL(enum.IntEnum):
    ACQUIRE_CONTROL_OFF        = _int32(0x0000)
    ACQUIRE_CONTROL_FORCE_LOW  = _int32(0x0001)
    ACQUIRE_CONTROL_FORCE_HIGH = _int32(0x0002)
dACQUIRE_CONTROL={a.name:a.value for a in ACQUIRE_CONTROL}
drACQUIRE_CONTROL={a.value:a.name for a in ACQUIRE_CONTROL}


class TIMESTAMP_MODE(enum.IntEnum):
    TIMESTAMP_MODE_OFF            = _int32(0)
    TIMESTAMP_MODE_BINARY         = _int32(1)
    TIMESTAMP_MODE_BINARYANDASCII = _int32(2)
    TIMESTAMP_MODE_ASCII          = _int32(3)
dTIMESTAMP_MODE={a.name:a.value for a in TIMESTAMP_MODE}
drTIMESTAMP_MODE={a.value:a.name for a in TIMESTAMP_MODE}


class METADATA_MODE(enum.IntEnum):
    METADATA_MODE_OFF  = _int32(0x0000)
    METADATA_MODE_ON   = _int32(0x0001)
    METADATA_MODE_TEST = _int32(0x8000)
dMETADATA_MODE={a.name:a.value for a in METADATA_MODE}
drMETADATA_MODE={a.value:a.name for a in METADATA_MODE}


class SIGNAL_STATE(enum.IntEnum):
    SIGNAL_STATE_BUSY      = _int32(0x00000001)
    SIGNAL_STATE_IDLE      = _int32(0x00000002)
    SIGNAL_STATE_EXP       = _int32(0x00000004)
    SIGNAL_STATE_READ      = _int32(0x00000008)
    SIGNAL_STATE_FIFO_FULL = _int32(0x00000010)
dSIGNAL_STATE={a.name:a.value for a in SIGNAL_STATE}
drSIGNAL_STATE={a.value:a.name for a in SIGNAL_STATE}





##### TYPE DEFINITIONS #####





##### FUNCTION DEFINITIONS #####


