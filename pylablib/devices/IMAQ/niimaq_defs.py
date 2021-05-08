##########   This file is generated automatically based on niimaq.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class IMG_ATTR(enum.IntEnum):
    IMG_ATTR_INTERFACE_TYPE                = _int32((0x3FF60000 + 0x0001))
    IMG_ATTR_PIXDEPTH                      = _int32((0x3FF60000 + 0x0002))
    IMG_ATTR_COLOR                         = _int32((0x3FF60000 + 0x0003))
    IMG_ATTR_HASRAM                        = _int32((0x3FF60000 + 0x0004))
    IMG_ATTR_RAMSIZE                       = _int32((0x3FF60000 + 0x0005))
    IMG_ATTR_CHANNEL                       = _int32((0x3FF60000 + 0x0006))
    IMG_ATTR_FRAME_FIELD                   = _int32((0x3FF60000 + 0x0007))
    IMG_ATTR_HORZ_RESOLUTION               = _int32((0x3FF60000 + 0x0009))
    IMG_ATTR_VERT_RESOLUTION               = _int32((0x3FF60000 + 0x000A))
    IMG_ATTR_LUT                           = _int32((0x3FF60000 + 0x000B))
    IMG_ATTR_LINESCAN                      = _int32((0x3FF60000 + 0x000C))
    IMG_ATTR_GAIN                          = _int32((0x3FF60000 + 0x000D))
    IMG_ATTR_CHROMA_FILTER                 = _int32((0x3FF60000 + 0x000E))
    IMG_ATTR_WHITE_REF                     = _int32((0x3FF60000 + 0x000F))
    IMG_ATTR_BLACK_REF                     = _int32((0x3FF60000 + 0x0010))
    IMG_ATTR_DATALINES                     = _int32((0x3FF60000 + 0x0011))
    IMG_ATTR_NUM_EXT_LINES                 = _int32((0x3FF60000 + 0x0012))
    IMG_ATTR_NUM_RTSI_LINES                = _int32((0x3FF60000 + 0x0013))
    IMG_ATTR_NUM_RTSI_IN_USE               = _int32((0x3FF60000 + 0x0014))
    IMG_ATTR_MEM_LOCKED                    = _int32((0x3FF60000 + 0x0065))
    IMG_ATTR_BITSPERPIXEL                  = _int32((0x3FF60000 + 0x0066))
    IMG_ATTR_BYTESPERPIXEL                 = _int32((0x3FF60000 + 0x0067))
    IMG_ATTR_ACQWINDOW_LEFT                = _int32((0x3FF60000 + 0x0068))
    IMG_ATTR_ACQWINDOW_TOP                 = _int32((0x3FF60000 + 0x0069))
    IMG_ATTR_ACQWINDOW_WIDTH               = _int32((0x3FF60000 + 0x006A))
    IMG_ATTR_ACQWINDOW_HEIGHT              = _int32((0x3FF60000 + 0x006B))
    IMG_ATTR_LINE_COUNT                    = _int32((0x3FF60000 + 0x0070))
    IMG_ATTR_FREE_BUFFERS                  = _int32((0x3FF60000 + 0x0071))
    IMG_ATTR_HSCALE                        = _int32((0x3FF60000 + 0x0072))
    IMG_ATTR_VSCALE                        = _int32((0x3FF60000 + 0x0073))
    IMG_ATTR_ACQ_IN_PROGRESS               = _int32((0x3FF60000 + 0x0074))
    IMG_ATTR_START_FIELD                   = _int32((0x3FF60000 + 0x0075))
    IMG_ATTR_FRAME_COUNT                   = _int32((0x3FF60000 + 0x0076))
    IMG_ATTR_LAST_VALID_BUFFER             = _int32((0x3FF60000 + 0x0077))
    IMG_ATTR_ROWBYTES                      = _int32((0x3FF60000 + 0x0078))
    IMG_ATTR_CALLBACK                      = _int32((0x3FF60000 + 0x007B))
    IMG_ATTR_CURRENT_BUFLIST               = _int32((0x3FF60000 + 0x007C))
    IMG_ATTR_FRAMEWAIT_MSEC                = _int32((0x3FF60000 + 0x007D))
    IMG_ATTR_TRIGGER_MODE                  = _int32((0x3FF60000 + 0x007E))
    IMG_ATTR_INVERT                        = _int32((0x3FF60000 + 0x0082))
    IMG_ATTR_XOFF_BUFFER                   = _int32((0x3FF60000 + 0x0083))
    IMG_ATTR_YOFF_BUFFER                   = _int32((0x3FF60000 + 0x0084))
    IMG_ATTR_NUM_BUFFERS                   = _int32((0x3FF60000 + 0x0085))
    IMG_ATTR_LOST_FRAMES                   = _int32((0x3FF60000 + 0x0088))
    IMG_ATTR_COLOR_WHITE_REF               = _int32((0x3FF60000 + 0x008F))
    IMG_ATTR_COLOR_BLACK_REF               = _int32((0x3FF60000 + 0x0090))
    IMG_ATTR_COLOR_CLAMP_START             = _int32((0x3FF60000 + 0x0091))
    IMG_ATTR_COLOR_CLAMP_STOP              = _int32((0x3FF60000 + 0x0092))
    IMG_ATTR_COLOR_ZERO_START              = _int32((0x3FF60000 + 0x0093))
    IMG_ATTR_COLOR_ZERO_STOP               = _int32((0x3FF60000 + 0x0094))
    IMG_ATTR_COLOR_AVG_COUNT               = _int32((0x3FF60000 + 0x0095))
    IMG_ATTR_COLOR_SW_CHROMA_FILTER        = _int32((0x3FF60000 + 0x0096))
    IMG_ATTR_COLOR_NTSC_SETUP_ENABLE       = _int32((0x3FF60000 + 0x0097))
    IMG_ATTR_COLOR_NTSC_SETUP_VALUE        = _int32((0x3FF60000 + 0x0098))
    IMG_ATTR_COLOR_BRIGHTNESS              = _int32((0x3FF60000 + 0x0099))
    IMG_ATTR_COLOR_CONTRAST                = _int32((0x3FF60000 + 0x009A))
    IMG_ATTR_COLOR_SATURATION              = _int32((0x3FF60000 + 0x009B))
    IMG_ATTR_COLOR_TINT                    = _int32((0x3FF60000 + 0x009C))
    IMG_ATTR_COLOR_SW_POST_GAIN            = _int32((0x3FF60000 + 0x009D))
    IMG_ATTR_COLOR_BURST_START             = _int32((0x3FF60000 + 0x009E))
    IMG_ATTR_COLOR_BURST_STOP              = _int32((0x3FF60000 + 0x009F))
    IMG_ATTR_COLOR_BLANK_START             = _int32((0x3FF60000 + 0x00A0))
    IMG_ATTR_COLOR_BLANK_STOP              = _int32((0x3FF60000 + 0x00A1))
    IMG_ATTR_COLOR_IMAGE_X_SHIFT           = _int32((0x3FF60000 + 0x00A2))
    IMG_ATTR_COLOR_GAIN                    = _int32((0x3FF60000 + 0x00A3))
    IMG_ATTR_COLOR_CLAMP_START_REF         = _int32((0x3FF60000 + 0x00A5))
    IMG_ATTR_COLOR_CLAMP_STOP_REF          = _int32((0x3FF60000 + 0x00A6))
    IMG_ATTR_COLOR_ZERO_START_REF          = _int32((0x3FF60000 + 0x00A7))
    IMG_ATTR_COLOR_ZERO_STOP_REF           = _int32((0x3FF60000 + 0x00A8))
    IMG_ATTR_COLOR_BURST_START_REF         = _int32((0x3FF60000 + 0x00A9))
    IMG_ATTR_COLOR_BURST_STOP_REF          = _int32((0x3FF60000 + 0x00AA))
    IMG_ATTR_COLOR_BLANK_START_REF         = _int32((0x3FF60000 + 0x00AB))
    IMG_ATTR_COLOR_BLANK_STOP_REF          = _int32((0x3FF60000 + 0x00AC))
    IMG_ATTR_COLOR_MODE                    = _int32((0x3FF60000 + 0x00AD))
    IMG_ATTR_COLOR_IMAGE_REP               = _int32((0x3FF60000 + 0x00AE))
    IMG_ATTR_GENLOCK_SWITCH_CHAN           = _int32((0x3FF60000 + 0x00AF))
    IMG_ATTR_CLAMP_START                   = _int32((0x3FF60000 + 0x00B0))
    IMG_ATTR_CLAMP_STOP                    = _int32((0x3FF60000 + 0x00B1))
    IMG_ATTR_ZERO_START                    = _int32((0x3FF60000 + 0x00B2))
    IMG_ATTR_ZERO_STOP                     = _int32((0x3FF60000 + 0x00B3))
    IMG_ATTR_COLOR_HUE_OFFS_ANGLE          = _int32((0x3FF60000 + 0x00B5))
    IMG_ATTR_COLOR_IMAGE_X_SHIFT_REF       = _int32((0x3FF60000 + 0x00B6))
    IMG_ATTR_LAST_VALID_FRAME              = _int32((0x3FF60000 + 0x00BA))
    IMG_ATTR_CLOCK_FREQ                    = _int32((0x3FF60000 + 0x00BB))
    IMG_ATTR_BLACK_REF_VOLT                = _int32((0x3FF60000 + 0x00BC))
    IMG_ATTR_WHITE_REF_VOLT                = _int32((0x3FF60000 + 0x00BD))
    IMG_ATTR_COLOR_LOW_REF_VOLT            = _int32((0x3FF60000 + 0x00BE))
    IMG_ATTR_COLOR_HIGH_REF_VOLT           = _int32((0x3FF60000 + 0x00BF))
    IMG_ATTR_GETSERIAL                     = _int32((0x3FF60000 + 0x00C0))
    IMG_ATTR_ROWPIXELS                     = _int32((0x3FF60000 + 0x00C1))
    IMG_ATTR_ACQUIRE_FIELD                 = _int32((0x3FF60000 + 0x00C2))
    IMG_ATTR_PCLK_DETECT                   = _int32((0x3FF60000 + 0x00C3))
    IMG_ATTR_VHA_MODE                      = _int32((0x3FF60000 + 0x00C4))
    IMG_ATTR_BIN_THRESHOLD_LOW             = _int32((0x3FF60000 + 0x00C5))
    IMG_ATTR_BIN_THRESHOLD_HIGH            = _int32((0x3FF60000 + 0x00C6))
    IMG_ATTR_COLOR_LUMA_BANDWIDTH          = _int32((0x3FF60000 + 0x00C7))
    IMG_ATTR_COLOR_CHROMA_TRAP             = _int32((0x3FF60000 + 0x00C8))
    IMG_ATTR_COLOR_LUMA_COMB               = _int32((0x3FF60000 + 0x00C9))
    IMG_ATTR_COLOR_PEAKING_ENABLE          = _int32((0x3FF60000 + 0x00CA))
    IMG_ATTR_COLOR_PEAKING_LEVEL           = _int32((0x3FF60000 + 0x00CB))
    IMG_ATTR_COLOR_CHROMA_PROCESS          = _int32((0x3FF60000 + 0x00CC))
    IMG_ATTR_COLOR_CHROMA_BANDWIDTH        = _int32((0x3FF60000 + 0x00CD))
    IMG_ATTR_COLOR_CHROMA_COMB             = _int32((0x3FF60000 + 0x00CE))
    IMG_ATTR_COLOR_CHROMA_PHASE            = _int32((0x3FF60000 + 0x00CF))
    IMG_ATTR_COLOR_RGB_CORING_LEVEL        = _int32((0x3FF60000 + 0x00D0))
    IMG_ATTR_COLOR_HSL_CORING_LEVEL        = _int32((0x3FF60000 + 0x00D1))
    IMG_ATTR_COLOR_HUE_REPLACE_VALUE       = _int32((0x3FF60000 + 0x00D2))
    IMG_ATTR_COLOR_GAIN_RED                = _int32((0x3FF60000 + 0x00D3))
    IMG_ATTR_COLOR_GAIN_GREEN              = _int32((0x3FF60000 + 0x00D4))
    IMG_ATTR_COLOR_GAIN_BLUE               = _int32((0x3FF60000 + 0x00D5))
    IMG_ATTR_CALIBRATION_DATE_LV           = _int32((0x3FF60000 + 0x00D6))
    IMG_ATTR_CALIBRATION_DATE              = _int32((0x3FF60000 + 0x00D7))
    IMG_ATTR_IMAGE_TYPE                    = _int32((0x3FF60000 + 0x00D8))
    IMG_ATTR_DYNAMIC_RANGE                 = _int32((0x3FF60000 + 0x00D9))
    IMG_ATTR_ACQUIRE_TO_SYSTEM_MEMORY      = _int32((0x3FF60000 + 0x011B))
    IMG_ATTR_ONBOARD_HOLDING_BUFFER_PTR    = _int32((0x3FF60000 + 0x011C))
    IMG_ATTR_SYNCHRONICITY                 = _int32((0x3FF60000 + 0x011D))
    IMG_ATTR_LAST_ACQUIRED_BUFFER_NUM      = _int32((0x3FF60000 + 0x011E))
    IMG_ATTR_LAST_ACQUIRED_BUFFER_INDEX    = _int32((0x3FF60000 + 0x011F))
    IMG_ATTR_LAST_TRANSFERRED_BUFFER_NUM   = _int32((0x3FF60000 + 0x0120))
    IMG_ATTR_LAST_TRANSFERRED_BUFFER_INDEX = _int32((0x3FF60000 + 0x0121))
    IMG_ATTR_SERIAL_NUM_BYTES_RECEIVED     = _int32((0x3FF60000 + 0x012C))
    IMG_ATTR_EXPOSURE_TIME_INTERNAL        = _int32((0x3FF60000 + 0x013C))
    IMG_ATTR_SERIAL_TERM_STRING            = _int32((0x3FF60000 + 0x0150))
    IMG_ATTR_DETECT_VIDEO                  = _int32((0x3FF60000 + 0x01A3))
    IMG_ATTR_ROI_LEFT                      = _int32((0x3FF60000 + 0x01A4))
    IMG_ATTR_ROI_TOP                       = _int32((0x3FF60000 + 0x01A5))
    IMG_ATTR_ROI_WIDTH                     = _int32((0x3FF60000 + 0x01A6))
    IMG_ATTR_ROI_HEIGHT                    = _int32((0x3FF60000 + 0x01A7))
    IMG_ATTR_NUM_ISO_IN_LINES              = _int32((0x3FF60000 + 0x01A8))
    IMG_ATTR_NUM_ISO_OUT_LINES             = _int32((0x3FF60000 + 0x01A9))
    IMG_ATTR_NUM_POST_TRIGGER_BUFFERS      = _int32((0x3FF60000 + 0x01AA))
    IMG_ATTR_EXT_TRIG_LINE_FILTER          = _int32((0x3FF60000 + 0x01AB))
    IMG_ATTR_RTSI_LINE_FILTER              = _int32((0x3FF60000 + 0x01AC))
    IMG_ATTR_NUM_PORTS                     = _int32((0x3FF60000 + 0x01AD))
    IMG_ATTR_CURRENT_PORT_NUM              = _int32((0x3FF60000 + 0x01AE))
    IMG_ATTR_ENCODER_PHASE_A_POLARITY      = _int32((0x3FF60000 + 0x01AF))
    IMG_ATTR_ENCODER_PHASE_B_POLARITY      = _int32((0x3FF60000 + 0x01B0))
    IMG_ATTR_ENCODER_FILTER                = _int32((0x3FF60000 + 0x01B1))
    IMG_ATTR_ENCODER_DIVIDE_FACTOR         = _int32((0x3FF60000 + 0x01B2))
    IMG_ATTR_ENCODER_POSITION              = _int32((0x3FF60000 + 0x01B3))
    IMG_ATTR_TEMPERATURE                   = _int32((0x3FF60000 + 0x01B4))
    IMG_ATTR_LED_PASS                      = _int32((0x3FF60000 + 0x01B5))
    IMG_ATTR_LED_FAIL                      = _int32((0x3FF60000 + 0x01B6))
    IMG_ATTR_SENSOR_PARTIAL_SCAN           = _int32((0x3FF60000 + 0x01B7))
    IMG_ATTR_SENSOR_BINNING                = _int32((0x3FF60000 + 0x01B8))
    IMG_ATTR_SENSOR_GAIN                   = _int32((0x3FF60000 + 0x01B9))
    IMG_ATTR_LIGHTING_MODE                 = _int32((0x3FF60000 + 0x01BB))
    IMG_ATTR_LIGHTING_CURRENT              = _int32((0x3FF60000 + 0x01BC))
    IMG_ATTR_LIGHTING_MAX_CURRENT          = _int32((0x3FF60000 + 0x01BD))
    IMG_ATTR_LIGHTING_EXT_STROBE_5V_TTL    = _int32((0x3FF60000 + 0x01BE))
    IMG_ATTR_LIGHTING_EXT_STROBE_24V       = _int32((0x3FF60000 + 0x01BF))
    IMG_ATTR_SENSOR_EXPOSURE               = _int32((0x3FF60000 + 0x01C0))
    IMG_ATTR_FRAME_RATE                    = _int32((0x3FF60000 + 0x01C1))
    IMG_ATTR_MAX_FRAME_RATE                = _int32((0x3FF60000 + 0x01C2))
    IMG_ATTR_SEND_SOFTWARE_TRIGGER         = _int32((0x3FF60000 + 0x01C3))
    IMG_ATTR_FIXED_FRAME_RATE_MODE         = _int32((0x3FF60000 + 0x01C4))
    IMG_ATTR_UNSIGNED_16BIT_IMAGE          = _int32((0x3FF60000 + 0x01C5))
    IMG_ATTR_POCL_STATUS                   = _int32((0x3FF60000 + 0x01C6))
    IMG_ATTR_ROWPIXELS_ALIGNMENT           = _int32((0x3FF60000 + 0x01C7))
    IMG_ATTR_ROWPIXELS_SUGGESTED_ALIGNMENT = _int32((0x3FF60000 + 0x01C8))
    IMG_ATTR_SUPPORTS_PULSE_UPDATE         = _int32((0x3FF60000 + 0x01C9))
    IMG_ATTR_BAYER_PATTERN                 = _int32((0x3FF60000 + 0x01CB))
    IMG_ATTR_BAYER_RED_GAIN                = _int32((0x3FF60000 + 0x01CC))
    IMG_ATTR_BAYER_GREEN_GAIN              = _int32((0x3FF60000 + 0x01CD))
    IMG_ATTR_BAYER_BLUE_GAIN               = _int32((0x3FF60000 + 0x01CE))
    IMG_ATTR_BAYER_ALGORITHM               = _int32((0x3FF60000 + 0x01CF))
dIMG_ATTR={a.name:a.value for a in IMG_ATTR}
drIMG_ATTR={a.value:a.name for a in IMG_ATTR}


class IMG_LUT(enum.IntEnum):
    IMG_LUT_NORMAL         = _int32(0)
    IMG_LUT_INVERSE        = _int32(1)
    IMG_LUT_LOG            = _int32(2)
    IMG_LUT_INVERSE_LOG    = _int32(3)
    IMG_LUT_BINARY         = _int32(4)
    IMG_LUT_INVERSE_BINARY = _int32(5)
    IMG_LUT_USER           = _int32(6)
    IMG_LUT_TYPE_DEFAULT   = _int32(0x00000010)
    IMG_LUT_TYPE_RED       = _int32(0x00000020)
    IMG_LUT_TYPE_GREEN     = _int32(0x00000040)
    IMG_LUT_TYPE_BLUE      = _int32(0x00000080)
    IMG_LUT_TYPE_TAP0      = _int32(0x00000100)
    IMG_LUT_TYPE_TAP1      = _int32(0x00000200)
    IMG_LUT_TYPE_TAP2      = _int32(0x00000400)
    IMG_LUT_TYPE_TAP3      = _int32(0x00000800)
dIMG_LUT={a.name:a.value for a in IMG_LUT}
drIMG_LUT={a.value:a.name for a in IMG_LUT}


class IMG_MODE(enum.IntEnum):
    IMG_FIELD_MODE = _int32(0)
    IMG_FRAME_MODE = _int32(1)
dIMG_MODE={a.name:a.value for a in IMG_MODE}
drIMG_MODE={a.value:a.name for a in IMG_MODE}


class IMG_FILTER(enum.IntEnum):
    IMG_FILTER_NONE = _int32(0)
    IMG_FILTER_NTSC = _int32(1)
    IMG_FILTER_PAL  = _int32(2)
dIMG_FILTER={a.name:a.value for a in IMG_FILTER}
drIMG_FILTER={a.value:a.name for a in IMG_FILTER}


class IMG_FIELD(enum.IntEnum):
    IMG_FIELD_EVEN = _int32(0)
    IMG_FIELD_ODD  = _int32(1)
dIMG_FIELD={a.name:a.value for a in IMG_FIELD}
drIMG_FIELD={a.value:a.name for a in IMG_FIELD}


class IMG_SCALE(enum.IntEnum):
    IMG_SCALE_NONE = _int32(1)
    IMG_SCALE_DIV2 = _int32(2)
    IMG_SCALE_DIV4 = _int32(4)
    IMG_SCALE_DIV8 = _int32(8)
dIMG_SCALE={a.name:a.value for a in IMG_SCALE}
drIMG_SCALE={a.value:a.name for a in IMG_SCALE}


class IMG_TRIGMODE(enum.IntEnum):
    IMG_TRIGMODE_NONE     = _int32(0)
    IMG_TRIGMODE_NOREPEAT = _int32(1)
    IMG_TRIGMODE_REPEAT   = _int32(2)
dIMG_TRIGMODE={a.name:a.value for a in IMG_TRIGMODE}
drIMG_TRIGMODE={a.value:a.name for a in IMG_TRIGMODE}


class IMG_ACQUIRE(enum.IntEnum):
    IMG_ACQUIRE_EVEN        = _int32(0)
    IMG_ACQUIRE_ODD         = _int32(1)
    IMG_ACQUIRE_ALL         = _int32(2)
    IMG_ACQUIRE_ALTERNATING = _int32(3)
dIMG_ACQUIRE={a.name:a.value for a in IMG_ACQUIRE}
drIMG_ACQUIRE={a.value:a.name for a in IMG_ACQUIRE}


class IMG_LUMA(enum.IntEnum):
    IMG_COLOR_LUMA_BANDWIDTH_FULL   = _int32(0)
    IMG_COLOR_LUMA_BANDWIDTH_HIGH   = _int32(1)
    IMG_COLOR_LUMA_BANDWIDTH_MEDIUM = _int32(2)
    IMG_COLOR_LUMA_BANDWIDTH_LOW    = _int32(3)
dIMG_LUMA={a.name:a.value for a in IMG_LUMA}
drIMG_LUMA={a.value:a.name for a in IMG_LUMA}


class IMG_COMB(enum.IntEnum):
    IMG_COLOR_COMB_OFF    = _int32(0)
    IMG_COLOR_COMB_1LINE  = _int32(1)
    IMG_COLOR_COMB_2LINES = _int32(2)
dIMG_COMB={a.name:a.value for a in IMG_COMB}
drIMG_COMB={a.value:a.name for a in IMG_COMB}


class IMG_CHROMA_PROCESS(enum.IntEnum):
    IMG_COLOR_CHROMA_PROCESS_ALWAYS_OFF = _int32(0)
    IMG_COLOR_CHROMA_PROCESS_ALWAYS_ON  = _int32(1)
    IMG_COLOR_CHROMA_PROCESS_AUTODETECT = _int32(2)
dIMG_CHROMA_PROCESS={a.name:a.value for a in IMG_CHROMA_PROCESS}
drIMG_CHROMA_PROCESS={a.value:a.name for a in IMG_CHROMA_PROCESS}


class IMG_CHROMA_BANDWIDTH(enum.IntEnum):
    IMG_COLOR_CHROMA_BANDWIDTH_HIGH = _int32(0)
    IMG_COLOR_CHROMA_BANDWIDTH_LOW  = _int32(1)
dIMG_CHROMA_BANDWIDTH={a.name:a.value for a in IMG_CHROMA_BANDWIDTH}
drIMG_CHROMA_BANDWIDTH={a.value:a.name for a in IMG_CHROMA_BANDWIDTH}


class IMG_RGB(enum.IntEnum):
    IMG_COLOR_RGB_CORING_LEVEL_NOCORING = _int32(0)
    IMG_COLOR_RGB_CORING_LEVEL_C1       = _int32(1)
    IMG_COLOR_RGB_CORING_LEVEL_C3       = _int32(2)
    IMG_COLOR_RGB_CORING_LEVEL_C7       = _int32(3)
dIMG_RGB={a.name:a.value for a in IMG_RGB}
drIMG_RGB={a.value:a.name for a in IMG_RGB}


class IMG_VIDEO(enum.IntEnum):
    IMG_VIDEO_NTSC = _int32(0)
    IMG_VIDEO_PAL  = _int32(1)
dIMG_VIDEO={a.name:a.value for a in IMG_VIDEO}
drIMG_VIDEO={a.value:a.name for a in IMG_VIDEO}


class IMG_EXAMINE_BUFF(enum.IntEnum):
    IMG_LAST_BUFFER    = _int32(0xFFFFFFFE)
    IMG_OLDEST_BUFFER  = _int32(0xFFFFFFFD)
    IMG_CURRENT_BUFFER = _int32(0xFFFFFFFC)
dIMG_EXAMINE_BUFF={a.name:a.value for a in IMG_EXAMINE_BUFF}
drIMG_EXAMINE_BUFF={a.value:a.name for a in IMG_EXAMINE_BUFF}


class IMG_BUFF(enum.IntEnum):
    IMG_BUFF_ADDRESS      = _int32((0x3FF60000 + 0x007E))
    IMG_BUFF_COMMAND      = _int32((0x3FF60000 + 0x007F))
    IMG_BUFF_SKIPCOUNT    = _int32((0x3FF60000 + 0x0080))
    IMG_BUFF_SIZE         = _int32((0x3FF60000 + 0x0082))
    IMG_BUFF_TRIGGER      = _int32((0x3FF60000 + 0x0083))
    IMG_BUFF_NUMBUFS      = _int32((0x3FF60000 + 0x00B0))
    IMG_BUFF_CHANNEL      = _int32((0x3FF60000 + 0x00Bc))
    IMG_BUFF_ACTUALHEIGHT = _int32((0x3FF60000 + 0x0400))
dIMG_BUFF={a.name:a.value for a in IMG_BUFF}
drIMG_BUFF={a.value:a.name for a in IMG_BUFF}


class IMG_CMD(enum.IntEnum):
    IMG_CMD_NEXT    = _int32(0x01)
    IMG_CMD_LOOP    = _int32(0x02)
    IMG_CMD_PASS    = _int32(0x04)
    IMG_CMD_STOP    = _int32(0x08)
    IMG_CMD_INVALID = _int32(0x10)
dIMG_CMD={a.name:a.value for a in IMG_CMD}
drIMG_CMD={a.value:a.name for a in IMG_CMD}


class IMG_TRIG_ACTION(enum.IntEnum):
    IMG_TRIG_ACTION_NONE    = _int32(0)
    IMG_TRIG_ACTION_CAPTURE = _int32(1)
    IMG_TRIG_ACTION_BUFLIST = _int32(2)
    IMG_TRIG_ACTION_BUFFER  = _int32(3)
    IMG_TRIG_ACTION_STOP    = _int32(4)
dIMG_TRIG_ACTION={a.name:a.value for a in IMG_TRIG_ACTION}
drIMG_TRIG_ACTION={a.value:a.name for a in IMG_TRIG_ACTION}


class IMG_MAP(enum.IntEnum):
    IMG_TRIG_MAP_RTSI0_DISABLED = _int32(0x0000000f)
    IMG_TRIG_MAP_RTSI0_EXT0     = _int32(0x00000001)
    IMG_TRIG_MAP_RTSI0_EXT1     = _int32(0x00000002)
    IMG_TRIG_MAP_RTSI0_EXT2     = _int32(0x00000003)
    IMG_TRIG_MAP_RTSI0_EXT3     = _int32(0x00000004)
    IMG_TRIG_MAP_RTSI0_EXT4     = _int32(0x00000005)
    IMG_TRIG_MAP_RTSI0_EXT5     = _int32(0x00000006)
    IMG_TRIG_MAP_RTSI0_EXT6     = _int32(0x00000007)
    IMG_TRIG_MAP_RTSI1_DISABLED = _int32(0x000000f0)
    IMG_TRIG_MAP_RTSI1_EXT0     = _int32(0x00000010)
    IMG_TRIG_MAP_RTSI1_EXT1     = _int32(0x00000020)
    IMG_TRIG_MAP_RTSI1_EXT2     = _int32(0x00000030)
    IMG_TRIG_MAP_RTSI1_EXT3     = _int32(0x00000040)
    IMG_TRIG_MAP_RTSI1_EXT4     = _int32(0x00000050)
    IMG_TRIG_MAP_RTSI1_EXT5     = _int32(0x00000060)
    IMG_TRIG_MAP_RTSI1_EXT6     = _int32(0x00000070)
    IMG_TRIG_MAP_RTSI2_DISABLED = _int32(0x00000f00)
    IMG_TRIG_MAP_RTSI2_EXT0     = _int32(0x00000100)
    IMG_TRIG_MAP_RTSI2_EXT1     = _int32(0x00000200)
    IMG_TRIG_MAP_RTSI2_EXT2     = _int32(0x00000300)
    IMG_TRIG_MAP_RTSI2_EXT3     = _int32(0x00000400)
    IMG_TRIG_MAP_RTSI2_EXT4     = _int32(0x00000500)
    IMG_TRIG_MAP_RTSI2_EXT5     = _int32(0x00000600)
    IMG_TRIG_MAP_RTSI2_EXT6     = _int32(0x00000700)
    IMG_TRIG_MAP_RTSI3_DISABLED = _int32(0x0000f000)
    IMG_TRIG_MAP_RTSI3_EXT0     = _int32(0x00001000)
    IMG_TRIG_MAP_RTSI3_EXT1     = _int32(0x00002000)
    IMG_TRIG_MAP_RTSI3_EXT2     = _int32(0x00003000)
    IMG_TRIG_MAP_RTSI3_EXT3     = _int32(0x00004000)
    IMG_TRIG_MAP_RTSI3_EXT4     = _int32(0x00005000)
    IMG_TRIG_MAP_RTSI3_EXT5     = _int32(0x00006000)
    IMG_TRIG_MAP_RTSI3_EXT6     = _int32(0x00007000)
dIMG_MAP={a.name:a.value for a in IMG_MAP}
drIMG_MAP={a.value:a.name for a in IMG_MAP}


class IMG_FRAMETIME(enum.IntEnum):
    IMG_FRAMETIME_STANDARD  = _int32(100)
    IMG_FRAMETIME_1SECOND   = _int32(1000)
    IMG_FRAMETIME_2SECONDS  = _int32(2000)
    IMG_FRAMETIME_5SECONDS  = _int32(5000)
    IMG_FRAMETIME_10SECONDS = _int32(10000)
    IMG_FRAMETIME_1MINUTE   = _int32(60000)
    IMG_FRAMETIME_2MINUTES  = _int32(120000)
    IMG_FRAMETIME_5MINUTES  = _int32(300000)
    IMG_FRAMETIME_10MINUTES = _int32(600000)
dIMG_FRAMETIME={a.name:a.value for a in IMG_FRAMETIME}
drIMG_FRAMETIME={a.value:a.name for a in IMG_FRAMETIME}


class IMG_GAIN(enum.IntEnum):
    IMG_GAIN_0DB  = _int32(0)
    IMG_GAIN_3DB  = _int32(1)
    IMG_GAIN_6DB  = _int32(2)
    IMG_GAIN_2_00 = _int32(0)
    IMG_GAIN_1_75 = _int32(1)
    IMG_GAIN_1_50 = _int32(2)
    IMG_GAIN_1_00 = _int32(3)
dIMG_GAIN={a.name:a.value for a in IMG_GAIN}
drIMG_GAIN={a.value:a.name for a in IMG_GAIN}


class IMG_BANDWIDTH(enum.IntEnum):
    IMG_BANDWIDTH_FULL = _int32(0)
    IMG_BANDWIDTH_9MHZ = _int32(1)
dIMG_BANDWIDTH={a.name:a.value for a in IMG_BANDWIDTH}
drIMG_BANDWIDTH={a.value:a.name for a in IMG_BANDWIDTH}


class IMG_WHITEREF(enum.IntEnum):
    IMG_WHITE_REFERENCE_MIN = _int32(0)
    IMG_WHITE_REFERENCE_MAX = _int32(63)
    IMG_BLACK_REFERENCE_MIN = _int32(0)
    IMG_BLACK_REFERENCE_MAX = _int32(63)
dIMG_WHITEREF={a.name:a.value for a in IMG_WHITEREF}
drIMG_WHITEREF={a.value:a.name for a in IMG_WHITEREF}


class IMG_TRIG_POL(enum.IntEnum):
    IMG_TRIG_POLAR_ACTIVEH = _int32(0)
    IMG_TRIG_POLAR_ACTIVEL = _int32(1)
dIMG_TRIG_POL={a.name:a.value for a in IMG_TRIG_POL}
drIMG_TRIG_POL={a.value:a.name for a in IMG_TRIG_POL}


class IMG_EXT_TRIG(enum.IntEnum):
    IMG_EXT_TRIG0           = _int32(0)
    IMG_EXT_TRIG1           = _int32(1)
    IMG_EXT_TRIG2           = _int32(2)
    IMG_EXT_TRIG3           = _int32(3)
    IMG_EXT_RTSI0           = _int32(4)
    IMG_EXT_RTSI1           = _int32(5)
    IMG_EXT_RTSI2           = _int32(6)
    IMG_EXT_RTSI3           = _int32(7)
    IMG_EXT_RTSI4           = _int32(12)
    IMG_EXT_RTSI5           = _int32(13)
    IMG_EXT_RTSI6           = _int32(14)
    IMG_TRIG_ROUTE_DISABLED = _int32(0xFFFFFFFF)
dIMG_EXT_TRIG={a.name:a.value for a in IMG_EXT_TRIG}
drIMG_EXT_TRIG={a.value:a.name for a in IMG_EXT_TRIG}


class IMG_INT_SIG(enum.IntEnum):
    IMG_AQ_DONE         = _int32(8)
    IMG_FRAME_START     = _int32(9)
    IMG_FRAME_DONE      = _int32(10)
    IMG_BUF_COMPLETE    = _int32(11)
    IMG_AQ_IN_PROGRESS  = _int32(15)
    IMG_IMMEDIATE       = _int32(16)
    IMG_FIXED_FREQUENCY = _int32(17)
    IMG_LINE_VALID      = _int32(18)
    IMG_FRAME_VALID     = _int32(19)
dIMG_INT_SIG={a.name:a.value for a in IMG_INT_SIG}
drIMG_INT_SIG={a.value:a.name for a in IMG_INT_SIG}


class IMG_TYPE(enum.IntEnum):
    IMG_IMAGE_U8    = _int32(0)
    IMG_IMAGE_I16   = _int32(1)
    IMG_IMAGE_RGB32 = _int32(4)
    IMG_IMAGE_HSL32 = _int32(5)
    IMG_IMAGE_RGB64 = _int32(6)
    IMG_IMAGE_U16   = _int32(7)
dIMG_TYPE={a.name:a.value for a in IMG_TYPE}
drIMG_TYPE={a.value:a.name for a in IMG_TYPE}


class IMG_COLOR_REP(enum.IntEnum):
    IMG_COLOR_REP_RGB32  = _int32(0)
    IMG_COLOR_REP_RED8   = _int32(1)
    IMG_COLOR_REP_GREEN8 = _int32(2)
    IMG_COLOR_REP_BLUE8  = _int32(3)
    IMG_COLOR_REP_LUM8   = _int32(4)
    IMG_COLOR_REP_HUE8   = _int32(5)
    IMG_COLOR_REP_SAT8   = _int32(6)
    IMG_COLOR_REP_INT8   = _int32(7)
    IMG_COLOR_REP_LUM16  = _int32(8)
    IMG_COLOR_REP_HUE16  = _int32(9)
    IMG_COLOR_REP_SAT16  = _int32(10)
    IMG_COLOR_REP_INT16  = _int32(11)
    IMG_COLOR_REP_RGB48  = _int32(12)
    IMG_COLOR_REP_RGB24  = _int32(13)
    IMG_COLOR_REP_RGB16  = _int32(14)
    IMG_COLOR_REP_HSL32  = _int32(15)
    IMG_COLOR_REP_HSI32  = _int32(16)
    IMG_COLOR_REP_NONE   = _int32(17)
    IMG_COLOR_REP_MONO10 = _int32(18)
dIMG_COLOR_REP={a.name:a.value for a in IMG_COLOR_REP}
drIMG_COLOR_REP={a.value:a.name for a in IMG_COLOR_REP}


class PULSE_TIMEBASE(enum.IntEnum):
    PULSE_TIMEBASE_PIXELCLK       = _int32(0x00000001)
    PULSE_TIMEBASE_50MHZ          = _int32(0x00000002)
    PULSE_TIMEBASE_100KHZ         = _int32(0x00000003)
    PULSE_TIMEBASE_SCALED_ENCODER = _int32(0x00000004)
dPULSE_TIMEBASE={a.name:a.value for a in PULSE_TIMEBASE}
drPULSE_TIMEBASE={a.value:a.name for a in PULSE_TIMEBASE}


class PULSE_MODE(enum.IntEnum):
    PULSE_MODE_TRAIN        = _int32(0x00000001)
    PULSE_MODE_SINGLE       = _int32(0x00000002)
    PULSE_MODE_SINGLE_REARM = _int32(0x00000003)
dPULSE_MODE={a.name:a.value for a in PULSE_MODE}
drPULSE_MODE={a.value:a.name for a in PULSE_MODE}


class PULSE_POL(enum.IntEnum):
    IMG_PULSE_POLAR_ACTIVEH = _int32(0)
    IMG_PULSE_POLAR_ACTIVEL = _int32(1)
dPULSE_POL={a.name:a.value for a in PULSE_POL}
drPULSE_POL={a.value:a.name for a in PULSE_POL}


class IMG_POCL(enum.IntEnum):
    IMG_POCL_UNKNOWN       = _int32(0xFFFFFFFF)
    IMG_POCL_NOT_SUPPORTED = _int32(0)
    IMG_POCL_NO_AUX_POWER  = _int32(1)
    IMG_POCL_BAD_FUSE      = _int32(2)
    IMG_POCL_DISABLED      = _int32(3)
    IMG_POCL_FAULT         = _int32(4)
    IMG_POCL_INITIALIZING  = _int32(5)
    IMG_POCL_INACTIVE      = _int32(6)
    IMG_POCL_ACTIVE        = _int32(7)
dIMG_POCL={a.name:a.value for a in IMG_POCL}
drIMG_POCL={a.value:a.name for a in IMG_POCL}


class IMG_TRIG_DRIVE(enum.IntEnum):
    IMG_TRIG_DRIVE_DISABLED       = _int32(0)
    IMG_TRIG_DRIVE_AQ_IN_PROGRESS = _int32(1)
    IMG_TRIG_DRIVE_AQ_DONE        = _int32(2)
    IMG_TRIG_DRIVE_PIXEL_CLK      = _int32(3)
    IMG_TRIG_DRIVE_UNASSERTED     = _int32(4)
    IMG_TRIG_DRIVE_ASSERTED       = _int32(5)
    IMG_TRIG_DRIVE_HSYNC          = _int32(6)
    IMG_TRIG_DRIVE_VSYNC          = _int32(7)
    IMG_TRIG_DRIVE_FRAME_START    = _int32(8)
    IMG_TRIG_DRIVE_FRAME_DONE     = _int32(9)
    IMG_TRIG_DRIVE_SCALED_ENCODER = _int32(10)
dIMG_TRIG_DRIVE={a.name:a.value for a in IMG_TRIG_DRIVE}
drIMG_TRIG_DRIVE={a.value:a.name for a in IMG_TRIG_DRIVE}


class IMGPLOT(enum.IntEnum):
    IMGPLOT_MONO_8      = _int32(0x00000000)
    IMGPLOT_INVERT      = _int32(0x00000001)
    IMGPLOT_COLOR_RGB24 = _int32(0x00000002)
    IMGPLOT_COLOR_RGB32 = _int32(0x00000004)
    IMGPLOT_MONO_10     = _int32(0x00000008)
    IMGPLOT_MONO_12     = _int32(0x00000010)
    IMGPLOT_MONO_14     = _int32(0x00000020)
    IMGPLOT_MONO_16     = _int32(0x00000040)
    IMGPLOT_MONO_32     = _int32(0x00000080)
    IMGPLOT_AUTO        = _int32(0x00000100)
dIMGPLOT={a.name:a.value for a in IMGPLOT}
drIMGPLOT={a.value:a.name for a in IMGPLOT}


class IMG_BUFFER_LOCATION(enum.IntEnum):
    IMG_HOST_FRAME   = _int32(0)
    IMG_DEVICE_FRAME = _int32(1)
dIMG_BUFFER_LOCATION={a.name:a.value for a in IMG_BUFFER_LOCATION}
drIMG_BUFFER_LOCATION={a.value:a.name for a in IMG_BUFFER_LOCATION}


class IMG_BAYER_PATTERN(enum.IntEnum):
    IMG_BAYER_PATTERN_NONE      = _int32(0xFFFFFFFF)
    IMG_BAYER_PATTERN_GBGB_RGRG = _int32(0)
    IMG_BAYER_PATTERN_GRGR_BGBG = _int32(1)
    IMG_BAYER_PATTERN_BGBG_GRGR = _int32(2)
    IMG_BAYER_PATTERN_RGRG_GBGB = _int32(3)
dIMG_BAYER_PATTERN={a.name:a.value for a in IMG_BAYER_PATTERN}
drIMG_BAYER_PATTERN={a.value:a.name for a in IMG_BAYER_PATTERN}


class IMG_BAYER_ALGORITHM(enum.IntEnum):
    IMG_BAYER_ALGORITHM_BILINEAR = _int32(0)
    IMG_BAYER_ALGORITHM_VNG      = _int32(1)
dIMG_BAYER_ALGORITHM={a.name:a.value for a in IMG_BAYER_ALGORITHM}
drIMG_BAYER_ALGORITHM={a.value:a.name for a in IMG_BAYER_ALGORITHM}


class IMG_ERR_CODE(enum.IntEnum):
    IMG_ERR_GOOD                                        = _int32(0)
    IMG_WRN_BCAM                                        = _int32((0x3FF60000 + 0x0001))
    IMG_WRN_CONF                                        = _int32((0x3FF60000 + 0x0002))
    IMG_WRN_ILCK                                        = _int32((0x3FF60000 + 0x0003))
    IMG_WRN_BLKG                                        = _int32((0x3FF60000 + 0x0004))
    IMG_WRN_BRST                                        = _int32((0x3FF60000 + 0x0005))
    IMG_WRN_OATTR                                       = _int32((0x3FF60000 + 0x0006))
    IMG_WRN_WLOR                                        = _int32((0x3FF60000 + 0x0007))
    IMG_WRN_IATTR                                       = _int32((0x3FF60000 + 0x0008))
    IMG_WRN_LATEST                                      = _int32((0x3FF60000 + 0x000A))
    IMG_ERR_NCAP                                        = _int32((0xBFF60000 + 0x0001))
    IMG_ERR_OVRN                                        = _int32((0xBFF60000 + 0x0002))
    IMG_ERR_EMEM                                        = _int32((0xBFF60000 + 0x0003))
    IMG_ERR_OSER                                        = _int32((0xBFF60000 + 0x0004))
    IMG_ERR_PAR1                                        = _int32((0xBFF60000 + 0x0005))
    IMG_ERR_PAR2                                        = _int32((0xBFF60000 + 0x0006))
    IMG_ERR_PAR3                                        = _int32((0xBFF60000 + 0x0007))
    IMG_ERR_PAR4                                        = _int32((0xBFF60000 + 0x0008))
    IMG_ERR_PAR5                                        = _int32((0xBFF60000 + 0x0009))
    IMG_ERR_PAR6                                        = _int32((0xBFF60000 + 0x000A))
    IMG_ERR_PAR7                                        = _int32((0xBFF60000 + 0x000B))
    IMG_ERR_MXBF                                        = _int32((0xBFF60000 + 0x000C))
    IMG_ERR_DLLE                                        = _int32((0xBFF60000 + 0x000D))
    IMG_ERR_BSIZ                                        = _int32((0xBFF60000 + 0x000E))
    IMG_ERR_MXBI                                        = _int32((0xBFF60000 + 0x000F))
    IMG_ERR_ELCK                                        = _int32((0xBFF60000 + 0x0010))
    IMG_ERR_DISE                                        = _int32((0xBFF60000 + 0x0011))
    IMG_ERR_BBUF                                        = _int32((0xBFF60000 + 0x0012))
    IMG_ERR_NLCK                                        = _int32((0xBFF60000 + 0x0013))
    IMG_ERR_NCAM                                        = _int32((0xBFF60000 + 0x0014))
    IMG_ERR_BINT                                        = _int32((0xBFF60000 + 0x0015))
    IMG_ERR_BROW                                        = _int32((0xBFF60000 + 0x0016))
    IMG_ERR_BROI                                        = _int32((0xBFF60000 + 0x0017))
    IMG_ERR_BCMF                                        = _int32((0xBFF60000 + 0x0018))
    IMG_ERR_NVBL                                        = _int32((0xBFF60000 + 0x0019))
    IMG_ERR_NCFG                                        = _int32((0xBFF60000 + 0x001A))
    IMG_ERR_BBLF                                        = _int32((0xBFF60000 + 0x001B))
    IMG_ERR_BBLE                                        = _int32((0xBFF60000 + 0x001C))
    IMG_ERR_BBLB                                        = _int32((0xBFF60000 + 0x001D))
    IMG_ERR_NAIP                                        = _int32((0xBFF60000 + 0x001E))
    IMG_ERR_VLCK                                        = _int32((0xBFF60000 + 0x001F))
    IMG_ERR_BDMA                                        = _int32((0xBFF60000 + 0x0020))
    IMG_ERR_AIOP                                        = _int32((0xBFF60000 + 0x0021))
    IMG_ERR_TIMO                                        = _int32((0xBFF60000 + 0x0022))
    IMG_ERR_NBUF                                        = _int32((0xBFF60000 + 0x0023))
    IMG_ERR_ZBUF                                        = _int32((0xBFF60000 + 0x0024))
    IMG_ERR_HLPR                                        = _int32((0xBFF60000 + 0x0025))
    IMG_ERR_BTRG                                        = _int32((0xBFF60000 + 0x0026))
    IMG_ERR_NINF                                        = _int32((0xBFF60000 + 0x0027))
    IMG_ERR_NDLL                                        = _int32((0xBFF60000 + 0x0028))
    IMG_ERR_NFNC                                        = _int32((0xBFF60000 + 0x0029))
    IMG_ERR_NOSR                                        = _int32((0xBFF60000 + 0x002A))
    IMG_ERR_BTAC                                        = _int32((0xBFF60000 + 0x002B))
    IMG_ERR_FIFO                                        = _int32((0xBFF60000 + 0x002C))
    IMG_ERR_MLCK                                        = _int32((0xBFF60000 + 0x002D))
    IMG_ERR_ILCK                                        = _int32((0xBFF60000 + 0x002E))
    IMG_ERR_NEPK                                        = _int32((0xBFF60000 + 0x002F))
    IMG_ERR_SCLM                                        = _int32((0xBFF60000 + 0x0030))
    IMG_ERR_SCC1                                        = _int32((0xBFF60000 + 0x0031))
    IMG_ERR_SMALLALLOC                                  = _int32((0xBFF60000 + 0x0032))
    IMG_ERR_ALLOC                                       = _int32((0xBFF60000 + 0x0033))
    IMG_ERR_BADCAMTYPE                                  = _int32((0xBFF60000 + 0x0034))
    IMG_ERR_BADPIXTYPE                                  = _int32((0xBFF60000 + 0x0035))
    IMG_ERR_BADCAMPARAM                                 = _int32((0xBFF60000 + 0x0036))
    IMG_ERR_PALKEYDTCT                                  = _int32((0xBFF60000 + 0x0037))
    IMG_ERR_BFRQ                                        = _int32((0xBFF60000 + 0x0038))
    IMG_ERR_BITP                                        = _int32((0xBFF60000 + 0x0039))
    IMG_ERR_HWNC                                        = _int32((0xBFF60000 + 0x003A))
    IMG_ERR_SERIAL                                      = _int32((0xBFF60000 + 0x003B))
    IMG_ERR_MXPI                                        = _int32((0xBFF60000 + 0x003C))
    IMG_ERR_BPID                                        = _int32((0xBFF60000 + 0x003D))
    IMG_ERR_NEVR                                        = _int32((0xBFF60000 + 0x003E))
    IMG_ERR_SERIAL_TIMO                                 = _int32((0xBFF60000 + 0x003F))
    IMG_ERR_PG_TOO_MANY                                 = _int32((0xBFF60000 + 0x0040))
    IMG_ERR_PG_BAD_TRANS                                = _int32((0xBFF60000 + 0x0041))
    IMG_ERR_PLNS                                        = _int32((0xBFF60000 + 0x0042))
    IMG_ERR_BPMD                                        = _int32((0xBFF60000 + 0x0043))
    IMG_ERR_NSAT                                        = _int32((0xBFF60000 + 0x0044))
    IMG_ERR_HYBRID                                      = _int32((0xBFF60000 + 0x0045))
    IMG_ERR_BADFILFMT                                   = _int32((0xBFF60000 + 0x0046))
    IMG_ERR_BADFILEXT                                   = _int32((0xBFF60000 + 0x0047))
    IMG_ERR_NRTSI                                       = _int32((0xBFF60000 + 0x0048))
    IMG_ERR_MXTRG                                       = _int32((0xBFF60000 + 0x0049))
    IMG_ERR_MXRC                                        = _int32((0xBFF60000 + 0x004A))
    IMG_ERR_OOR                                         = _int32((0xBFF60000 + 0x004B))
    IMG_ERR_NPROG                                       = _int32((0xBFF60000 + 0x004C))
    IMG_ERR_NEOM                                        = _int32((0xBFF60000 + 0x004D))
    IMG_ERR_BDTYPE                                      = _int32((0xBFF60000 + 0x004E))
    IMG_ERR_THRDACCDEN                                  = _int32((0xBFF60000 + 0x004F))
    IMG_ERR_BADFILWRT                                   = _int32((0xBFF60000 + 0x0050))
    IMG_ERR_AEXM                                        = _int32((0xBFF60000 + 0x0051))
    IMG_ERR_FIRST_ERROR                                 = _int32((0xBFF60000 + 0x0001))
    IMG_ERR_NOT_SUPPORTED                               = _int32((0xBFF60000 + 0x0001))
    IMG_ERR_SYSTEM_MEMORY_FULL                          = _int32((0xBFF60000 + 0x0003))
    IMG_ERR_BUFFER_SIZE_TOO_SMALL                       = _int32((0xBFF60000 + 0x000E))
    IMG_ERR_BUFFER_LIST_NOT_LOCKED                      = _int32((0xBFF60000 + 0x0013))
    IMG_ERR_BAD_INTERFACE_FILE                          = _int32((0xBFF60000 + 0x0015))
    IMG_ERR_BAD_USER_RECT                               = _int32((0xBFF60000 + 0x0017))
    IMG_ERR_BAD_CAMERA_FILE                             = _int32((0xBFF60000 + 0x0018))
    IMG_ERR_NO_BUFFERS_CONFIGURED                       = _int32((0xBFF60000 + 0x001A))
    IMG_ERR_BAD_BUFFER_LIST_FINAL_COMMAND               = _int32((0xBFF60000 + 0x001B))
    IMG_ERR_BAD_BUFFER_LIST_COMMAND                     = _int32((0xBFF60000 + 0x001C))
    IMG_ERR_BAD_BUFFER_POINTER                          = _int32((0xBFF60000 + 0x001D))
    IMG_ERR_BOARD_NOT_RUNNING                           = _int32((0xBFF60000 + 0x001E))
    IMG_ERR_VIDEO_LOCK                                  = _int32((0xBFF60000 + 0x001F))
    IMG_ERR_BOARD_RUNNING                               = _int32((0xBFF60000 + 0x0021))
    IMG_ERR_TIMEOUT                                     = _int32((0xBFF60000 + 0x0022))
    IMG_ERR_ZERO_BUFFER_SIZE                            = _int32((0xBFF60000 + 0x0024))
    IMG_ERR_NO_INTERFACE_FOUND                          = _int32((0xBFF60000 + 0x0027))
    IMG_ERR_FIFO_OVERFLOW                               = _int32((0xBFF60000 + 0x002C))
    IMG_ERR_MEMORY_PAGE_LOCK_FAULT                      = _int32((0xBFF60000 + 0x002D))
    IMG_ERR_BAD_CLOCK_FREQUENCY                         = _int32((0xBFF60000 + 0x0038))
    IMG_ERR_BAD_CAMERA_TYPE                             = _int32((0xBFF60000 + 0x0034))
    IMG_ERR_HARDWARE_NOT_CAPABLE                        = _int32((0xBFF60000 + 0x003A))
    IMG_ERR_ATTRIBUTE_NOT_SETTABLE                      = _int32((0xBFF60000 + 0x0044))
    IMG_ERR_ONBOARD_MEMORY_FULL                         = _int32((0xBFF60000 + 0x004D))
    IMG_ERR_BUFFER_NOT_RELEASED                         = _int32((0xBFF60000 + 0x0051))
    IMG_ERR_BAD_LUT_TYPE                                = _int32((0xBFF60000 + 0x0052))
    IMG_ERR_ATTRIBUTE_NOT_READABLE                      = _int32((0xBFF60000 + 0x0053))
    IMG_ERR_BOARD_NOT_SUPPORTED                         = _int32((0xBFF60000 + 0x0054))
    IMG_ERR_BAD_FRAME_FIELD                             = _int32((0xBFF60000 + 0x0055))
    IMG_ERR_INVALID_ATTRIBUTE                           = _int32((0xBFF60000 + 0x0056))
    IMG_ERR_BAD_LINE_MAP                                = _int32((0xBFF60000 + 0x0057))
    IMG_ERR_BAD_CHANNEL                                 = _int32((0xBFF60000 + 0x0059))
    IMG_ERR_BAD_CHROMA_FILTER                           = _int32((0xBFF60000 + 0x005A))
    IMG_ERR_BAD_SCALE                                   = _int32((0xBFF60000 + 0x005B))
    IMG_ERR_BAD_TRIGGER_MODE                            = _int32((0xBFF60000 + 0x005D))
    IMG_ERR_BAD_CLAMP_START                             = _int32((0xBFF60000 + 0x005E))
    IMG_ERR_BAD_CLAMP_STOP                              = _int32((0xBFF60000 + 0x005F))
    IMG_ERR_BAD_BRIGHTNESS                              = _int32((0xBFF60000 + 0x0060))
    IMG_ERR_BAD_CONTRAST                                = _int32((0xBFF60000 + 0x0061))
    IMG_ERR_BAD_SATURATION                              = _int32((0xBFF60000 + 0x0062))
    IMG_ERR_BAD_TINT                                    = _int32((0xBFF60000 + 0x0063))
    IMG_ERR_BAD_HUE_OFF_ANGLE                           = _int32((0xBFF60000 + 0x0064))
    IMG_ERR_BAD_ACQUIRE_FIELD                           = _int32((0xBFF60000 + 0x0065))
    IMG_ERR_BAD_LUMA_BANDWIDTH                          = _int32((0xBFF60000 + 0x0066))
    IMG_ERR_BAD_LUMA_COMB                               = _int32((0xBFF60000 + 0x0067))
    IMG_ERR_BAD_CHROMA_PROCESS                          = _int32((0xBFF60000 + 0x0068))
    IMG_ERR_BAD_CHROMA_BANDWIDTH                        = _int32((0xBFF60000 + 0x0069))
    IMG_ERR_BAD_CHROMA_COMB                             = _int32((0xBFF60000 + 0x006A))
    IMG_ERR_BAD_RGB_CORING                              = _int32((0xBFF60000 + 0x006B))
    IMG_ERR_BAD_HUE_REPLACE_VALUE                       = _int32((0xBFF60000 + 0x006C))
    IMG_ERR_BAD_RED_GAIN                                = _int32((0xBFF60000 + 0x006D))
    IMG_ERR_BAD_GREEN_GAIN                              = _int32((0xBFF60000 + 0x006E))
    IMG_ERR_BAD_BLUE_GAIN                               = _int32((0xBFF60000 + 0x006F))
    IMG_ERR_BAD_START_FIELD                             = _int32((0xBFF60000 + 0x0070))
    IMG_ERR_BAD_TAP_DIRECTION                           = _int32((0xBFF60000 + 0x0071))
    IMG_ERR_BAD_MAX_IMAGE_RECT                          = _int32((0xBFF60000 + 0x0072))
    IMG_ERR_BAD_TAP_TYPE                                = _int32((0xBFF60000 + 0x0073))
    IMG_ERR_BAD_SYNC_RECT                               = _int32((0xBFF60000 + 0x0074))
    IMG_ERR_BAD_ACQWINDOW_RECT                          = _int32((0xBFF60000 + 0x0075))
    IMG_ERR_BAD_HSL_CORING                              = _int32((0xBFF60000 + 0x0076))
    IMG_ERR_BAD_TAP_0_VALID_RECT                        = _int32((0xBFF60000 + 0x0077))
    IMG_ERR_BAD_TAP_1_VALID_RECT                        = _int32((0xBFF60000 + 0x0078))
    IMG_ERR_BAD_TAP_2_VALID_RECT                        = _int32((0xBFF60000 + 0x0079))
    IMG_ERR_BAD_TAP_3_VALID_RECT                        = _int32((0xBFF60000 + 0x007A))
    IMG_ERR_BAD_TAP_RECT                                = _int32((0xBFF60000 + 0x007B))
    IMG_ERR_BAD_NUM_TAPS                                = _int32((0xBFF60000 + 0x007C))
    IMG_ERR_BAD_TAP_NUM                                 = _int32((0xBFF60000 + 0x007D))
    IMG_ERR_BAD_QUAD_NUM                                = _int32((0xBFF60000 + 0x007E))
    IMG_ERR_BAD_NUM_DATA_LINES                          = _int32((0xBFF60000 + 0x007F))
    IMG_ERR_BAD_BITS_PER_COMPONENT                      = _int32((0xBFF60000 + 0x0080))
    IMG_ERR_BAD_NUM_COMPONENTS                          = _int32((0xBFF60000 + 0x0081))
    IMG_ERR_BAD_BIN_THRESHOLD_LOW                       = _int32((0xBFF60000 + 0x0082))
    IMG_ERR_BAD_BIN_THRESHOLD_HIGH                      = _int32((0xBFF60000 + 0x0083))
    IMG_ERR_BAD_BLACK_REF_VOLT                          = _int32((0xBFF60000 + 0x0084))
    IMG_ERR_BAD_WHITE_REF_VOLT                          = _int32((0xBFF60000 + 0x0085))
    IMG_ERR_BAD_FREQ_STD                                = _int32((0xBFF60000 + 0x0086))
    IMG_ERR_BAD_HDELAY                                  = _int32((0xBFF60000 + 0x0087))
    IMG_ERR_BAD_LOCK_SPEED                              = _int32((0xBFF60000 + 0x0088))
    IMG_ERR_BAD_BUFFER_LIST                             = _int32((0xBFF60000 + 0x0089))
    IMG_ERR_BOARD_NOT_INITIALIZED                       = _int32((0xBFF60000 + 0x008A))
    IMG_ERR_BAD_PCLK_SOURCE                             = _int32((0xBFF60000 + 0x008B))
    IMG_ERR_BAD_VIDEO_LOCK_CHANNEL                      = _int32((0xBFF60000 + 0x008C))
    IMG_ERR_BAD_LOCK_SEL                                = _int32((0xBFF60000 + 0x008D))
    IMG_ERR_BAD_BAUD_RATE                               = _int32((0xBFF60000 + 0x008E))
    IMG_ERR_BAD_STOP_BITS                               = _int32((0xBFF60000 + 0x008F))
    IMG_ERR_BAD_DATA_BITS                               = _int32((0xBFF60000 + 0x0090))
    IMG_ERR_BAD_PARITY                                  = _int32((0xBFF60000 + 0x0091))
    IMG_ERR_TERM_STRING_NOT_FOUND                       = _int32((0xBFF60000 + 0x0092))
    IMG_ERR_SERIAL_READ_TIMEOUT                         = _int32((0xBFF60000 + 0x0093))
    IMG_ERR_SERIAL_WRITE_TIMEOUT                        = _int32((0xBFF60000 + 0x0094))
    IMG_ERR_BAD_SYNCHRONICITY                           = _int32((0xBFF60000 + 0x0095))
    IMG_ERR_BAD_INTERLACING_CONFIG                      = _int32((0xBFF60000 + 0x0096))
    IMG_ERR_BAD_CHIP_CODE                               = _int32((0xBFF60000 + 0x0098))
    IMG_ERR_LUT_NOT_PRESENT                             = _int32((0xBFF60000 + 0x0099))
    IMG_ERR_DSPFILTER_NOT_PRESENT                       = _int32((0xBFF60000 + 0x009A))
    IMG_ERR_DEVICE_NOT_FOUND                            = _int32((0xBFF60000 + 0x009B))
    IMG_ERR_ONBOARD_MEM_CONFIG                          = _int32((0xBFF60000 + 0x009C))
    IMG_ERR_BAD_POINTER                                 = _int32((0xBFF60000 + 0x009D))
    IMG_ERR_BAD_BUFFER_LIST_INDEX                       = _int32((0xBFF60000 + 0x009E))
    IMG_ERR_INVALID_BUFFER_ATTRIBUTE                    = _int32((0xBFF60000 + 0x009F))
    IMG_ERR_INVALID_BUFFER_PTR                          = _int32((0xBFF60000 + 0x00A0))
    IMG_ERR_BUFFER_LIST_ALREADY_LOCKED                  = _int32((0xBFF60000 + 0x00A1))
    IMG_ERR_BAD_DEVICE_TYPE                             = _int32((0xBFF60000 + 0x00A2))
    IMG_ERR_BAD_BAR_SIZE                                = _int32((0xBFF60000 + 0x00A3))
    IMG_ERR_NO_VALID_COUNTER_RECT                       = _int32((0xBFF60000 + 0x00A5))
    IMG_ERR_ACQ_STOPPED                                 = _int32((0xBFF60000 + 0x00A6))
    IMG_ERR_BAD_TRIGGER_ACTION                          = _int32((0xBFF60000 + 0x00A7))
    IMG_ERR_BAD_TRIGGER_POLARITY                        = _int32((0xBFF60000 + 0x00A8))
    IMG_ERR_BAD_TRIGGER_NUMBER                          = _int32((0xBFF60000 + 0x00A9))
    IMG_ERR_BUFFER_NOT_AVAILABLE                        = _int32((0xBFF60000 + 0x00AA))
    IMG_ERR_BAD_PULSE_ID                                = _int32((0xBFF60000 + 0x00AC))
    IMG_ERR_BAD_PULSE_TIMEBASE                          = _int32((0xBFF60000 + 0x00AD))
    IMG_ERR_BAD_PULSE_GATE                              = _int32((0xBFF60000 + 0x00AE))
    IMG_ERR_BAD_PULSE_GATE_POLARITY                     = _int32((0xBFF60000 + 0x00AF))
    IMG_ERR_BAD_PULSE_OUTPUT                            = _int32((0xBFF60000 + 0x00B0))
    IMG_ERR_BAD_PULSE_OUTPUT_POLARITY                   = _int32((0xBFF60000 + 0x00B1))
    IMG_ERR_BAD_PULSE_MODE                              = _int32((0xBFF60000 + 0x00B2))
    IMG_ERR_NOT_ENOUGH_RESOURCES                        = _int32((0xBFF60000 + 0x00B3))
    IMG_ERR_INVALID_RESOURCE                            = _int32((0xBFF60000 + 0x00B4))
    IMG_ERR_BAD_FVAL_ENABLE                             = _int32((0xBFF60000 + 0x00B5))
    IMG_ERR_BAD_WRITE_ENABLE_MODE                       = _int32((0xBFF60000 + 0x00B6))
    IMG_ERR_COMPONENT_MISMATCH                          = _int32((0xBFF60000 + 0x00B7))
    IMG_ERR_FPGA_PROGRAMMING_FAILED                     = _int32((0xBFF60000 + 0x00B8))
    IMG_ERR_CONTROL_FPGA_FAILED                         = _int32((0xBFF60000 + 0x00B9))
    IMG_ERR_CHIP_NOT_READABLE                           = _int32((0xBFF60000 + 0x00BA))
    IMG_ERR_CHIP_NOT_WRITABLE                           = _int32((0xBFF60000 + 0x00BB))
    IMG_ERR_I2C_BUS_FAILED                              = _int32((0xBFF60000 + 0x00BC))
    IMG_ERR_DEVICE_IN_USE                               = _int32((0xBFF60000 + 0x00BD))
    IMG_ERR_BAD_TAP_DATALANES                           = _int32((0xBFF60000 + 0x00BE))
    IMG_ERR_BAD_VIDEO_GAIN                              = _int32((0xBFF60000 + 0x00BF))
    IMG_ERR_VHA_MODE_NOT_ALLOWED                        = _int32((0xBFF60000 + 0x00C0))
    IMG_ERR_BAD_TRACKING_SPEED                          = _int32((0xBFF60000 + 0x00C1))
    IMG_ERR_BAD_COLOR_INPUT_SELECT                      = _int32((0xBFF60000 + 0x00C2))
    IMG_ERR_BAD_HAV_OFFSET                              = _int32((0xBFF60000 + 0x00C3))
    IMG_ERR_BAD_HS1_OFFSET                              = _int32((0xBFF60000 + 0x00C4))
    IMG_ERR_BAD_HS2_OFFSET                              = _int32((0xBFF60000 + 0x00C5))
    IMG_ERR_BAD_IF_CHROMA                               = _int32((0xBFF60000 + 0x00C6))
    IMG_ERR_BAD_COLOR_OUTPUT_FORMAT                     = _int32((0xBFF60000 + 0x00C7))
    IMG_ERR_BAD_SAMSUNG_SCHCMP                          = _int32((0xBFF60000 + 0x00C8))
    IMG_ERR_BAD_SAMSUNG_CDLY                            = _int32((0xBFF60000 + 0x00C9))
    IMG_ERR_BAD_SECAM_DETECT                            = _int32((0xBFF60000 + 0x00CA))
    IMG_ERR_BAD_FSC_DETECT                              = _int32((0xBFF60000 + 0x00CB))
    IMG_ERR_BAD_SAMSUNG_CFTC                            = _int32((0xBFF60000 + 0x00CC))
    IMG_ERR_BAD_SAMSUNG_CGTC                            = _int32((0xBFF60000 + 0x00CD))
    IMG_ERR_BAD_SAMSUNG_SAMPLE_RATE                     = _int32((0xBFF60000 + 0x00CE))
    IMG_ERR_BAD_SAMSUNG_VSYNC_EDGE                      = _int32((0xBFF60000 + 0x00CF))
    IMG_ERR_SAMSUNG_LUMA_GAIN_CTRL                      = _int32((0xBFF60000 + 0x00D0))
    IMG_ERR_BAD_SET_COMB_COEF                           = _int32((0xBFF60000 + 0x00D1))
    IMG_ERR_SAMSUNG_CHROMA_TRACK                        = _int32((0xBFF60000 + 0x00D2))
    IMG_ERR_SAMSUNG_DROP_LINES                          = _int32((0xBFF60000 + 0x00D3))
    IMG_ERR_VHA_OPTIMIZATION_NOT_ALLOWED                = _int32((0xBFF60000 + 0x00D4))
    IMG_ERR_BAD_PG_TRANSITION                           = _int32((0xBFF60000 + 0x00D5))
    IMG_ERR_TOO_MANY_PG_TRANSITIONS                     = _int32((0xBFF60000 + 0x00D6))
    IMG_ERR_BAD_CL_DATA_CONFIG                          = _int32((0xBFF60000 + 0x00D7))
    IMG_ERR_BAD_OCCURRENCE                              = _int32((0xBFF60000 + 0x00D8))
    IMG_ERR_BAD_PG_MODE                                 = _int32((0xBFF60000 + 0x00D9))
    IMG_ERR_BAD_PG_SOURCE                               = _int32((0xBFF60000 + 0x00DA))
    IMG_ERR_BAD_PG_GATE                                 = _int32((0xBFF60000 + 0x00DB))
    IMG_ERR_BAD_PG_GATE_POLARITY                        = _int32((0xBFF60000 + 0x00DC))
    IMG_ERR_BAD_PG_WAVEFORM_INITIAL_STATE               = _int32((0xBFF60000 + 0x00DD))
    IMG_ERR_INVALID_CAMERA_ATTRIBUTE                    = _int32((0xBFF60000 + 0x00DE))
    IMG_ERR_BOARD_CLOSED                                = _int32((0xBFF60000 + 0x00DF))
    IMG_ERR_FILE_NOT_FOUND                              = _int32((0xBFF60000 + 0x00E0))
    IMG_ERR_BAD_1409_DSP_FILE                           = _int32((0xBFF60000 + 0x00E1))
    IMG_ERR_BAD_SCARABXCV200_32_FILE                    = _int32((0xBFF60000 + 0x00E2))
    IMG_ERR_BAD_SCARABXCV200_16_FILE                    = _int32((0xBFF60000 + 0x00E3))
    IMG_ERR_BAD_CAMERA_LINK_FILE                        = _int32((0xBFF60000 + 0x00E4))
    IMG_ERR_BAD_1411_CSC_FILE                           = _int32((0xBFF60000 + 0x00E5))
    IMG_ERR_BAD_ERROR_CODE                              = _int32((0xBFF60000 + 0x00E6))
    IMG_ERR_DRIVER_TOO_OLD                              = _int32((0xBFF60000 + 0x00E7))
    IMG_ERR_INSTALLATION_CORRUPT                        = _int32((0xBFF60000 + 0x00E8))
    IMG_ERR_NO_ONBOARD_MEMORY                           = _int32((0xBFF60000 + 0x00E9))
    IMG_ERR_BAD_BAYER_PATTERN                           = _int32((0xBFF60000 + 0x00EA))
    IMG_ERR_CANNOT_INITIALIZE_BOARD                     = _int32((0xBFF60000 + 0x00EB))
    IMG_ERR_CALIBRATION_DATA_CORRUPT                    = _int32((0xBFF60000 + 0x00EC))
    IMG_ERR_DRIVER_FAULT                                = _int32((0xBFF60000 + 0x00ED))
    IMG_ERR_ADDRESS_OUT_OF_RANGE                        = _int32((0xBFF60000 + 0x00EE))
    IMG_ERR_ONBOARD_ACQUISITION                         = _int32((0xBFF60000 + 0x00EF))
    IMG_ERR_NOT_AN_ONBOARD_ACQUISITION                  = _int32((0xBFF60000 + 0x00F0))
    IMG_ERR_BOARD_ALREADY_INITIALIZED                   = _int32((0xBFF60000 + 0x00F1))
    IMG_ERR_NO_SERIAL_PORT                              = _int32((0xBFF60000 + 0x00F2))
    IMG_ERR_BAD_VENABLE_GATING_MODE                     = _int32((0xBFF60000 + 0x00F3))
    IMG_ERR_BAD_1407_LUT_FILE                           = _int32((0xBFF60000 + 0x00F4))
    IMG_ERR_BAD_SYNC_DETECT_LEVEL                       = _int32((0xBFF60000 + 0x00F5))
    IMG_ERR_BAD_1405_GAIN_FILE                          = _int32((0xBFF60000 + 0x00F6))
    IMG_ERR_CLAMP_DAC_NOT_PRESENT                       = _int32((0xBFF60000 + 0x00F7))
    IMG_ERR_GAIN_DAC_NOT_PRESENT                        = _int32((0xBFF60000 + 0x00F8))
    IMG_ERR_REF_DAC_NOT_PRESENT                         = _int32((0xBFF60000 + 0x00F9))
    IMG_ERR_BAD_SCARABXC2S200_FILE                      = _int32((0xBFF60000 + 0x00FA))
    IMG_ERR_BAD_LUT_GAIN                                = _int32((0xBFF60000 + 0x00FB))
    IMG_ERR_BAD_MAX_BUF_LIST_ITER                       = _int32((0xBFF60000 + 0x00FC))
    IMG_ERR_BAD_PG_LINE_NUM                             = _int32((0xBFF60000 + 0x00FD))
    IMG_ERR_BAD_BITS_PER_PIXEL                          = _int32((0xBFF60000 + 0x00FE))
    IMG_ERR_TRIGGER_ALARM                               = _int32((0xBFF60000 + 0x00FF))
    IMG_ERR_BAD_SCARABXC2S200_03052009_FILE             = _int32((0xBFF60000 + 0x0100))
    IMG_ERR_LUT_CONFIG                                  = _int32((0xBFF60000 + 0x0101))
    IMG_ERR_CONTROL_FPGA_REQUIRES_NEWER_DRIVER          = _int32((0xBFF60000 + 0x0102))
    IMG_ERR_CONTROL_FPGA_PROGRAMMING_FAILED             = _int32((0xBFF60000 + 0x0103))
    IMG_ERR_BAD_TRIGGER_SIGNAL_LEVEL                    = _int32((0xBFF60000 + 0x0104))
    IMG_ERR_CAMERA_FILE_REQUIRES_NEWER_DRIVER           = _int32((0xBFF60000 + 0x0105))
    IMG_ERR_DUPLICATED_BUFFER                           = _int32((0xBFF60000 + 0x0106))
    IMG_ERR_NO_ERROR                                    = _int32((0xBFF60000 + 0x0107))
    IMG_ERR_INTERFACE_NOT_SUPPORTED                     = _int32((0xBFF60000 + 0x0108))
    IMG_ERR_BAD_PCLK_POLARITY                           = _int32((0xBFF60000 + 0x0109))
    IMG_ERR_BAD_ENABLE_POLARITY                         = _int32((0xBFF60000 + 0x010A))
    IMG_ERR_BAD_PCLK_SIGNAL_LEVEL                       = _int32((0xBFF60000 + 0x010B))
    IMG_ERR_BAD_ENABLE_SIGNAL_LEVEL                     = _int32((0xBFF60000 + 0x010C))
    IMG_ERR_BAD_DATA_SIGNAL_LEVEL                       = _int32((0xBFF60000 + 0x010D))
    IMG_ERR_BAD_CTRL_SIGNAL_LEVEL                       = _int32((0xBFF60000 + 0x010E))
    IMG_ERR_BAD_WINDOW_HANDLE                           = _int32((0xBFF60000 + 0x010F))
    IMG_ERR_CANNOT_WRITE_FILE                           = _int32((0xBFF60000 + 0x0110))
    IMG_ERR_CANNOT_READ_FILE                            = _int32((0xBFF60000 + 0x0111))
    IMG_ERR_BAD_SIGNAL_TYPE                             = _int32((0xBFF60000 + 0x0112))
    IMG_ERR_BAD_SAMPLES_PER_LINE                        = _int32((0xBFF60000 + 0x0113))
    IMG_ERR_BAD_SAMPLES_PER_LINE_REF                    = _int32((0xBFF60000 + 0x0114))
    IMG_ERR_USE_EXTERNAL_HSYNC                          = _int32((0xBFF60000 + 0x0115))
    IMG_ERR_BUFFER_NOT_ALIGNED                          = _int32((0xBFF60000 + 0x0116))
    IMG_ERR_ROWPIXELS_TOO_SMALL                         = _int32((0xBFF60000 + 0x0117))
    IMG_ERR_ROWPIXELS_NOT_ALIGNED                       = _int32((0xBFF60000 + 0x0118))
    IMG_ERR_ROI_WIDTH_NOT_ALIGNED                       = _int32((0xBFF60000 + 0x0119))
    IMG_ERR_LINESCAN_NOT_ALLOWED                        = _int32((0xBFF60000 + 0x011A))
    IMG_ERR_INTERFACE_FILE_REQUIRES_NEWER_DRIVER        = _int32((0xBFF60000 + 0x011B))
    IMG_ERR_BAD_SKIP_COUNT                              = _int32((0xBFF60000 + 0x011C))
    IMG_ERR_BAD_NUM_X_ZONES                             = _int32((0xBFF60000 + 0x011D))
    IMG_ERR_BAD_NUM_Y_ZONES                             = _int32((0xBFF60000 + 0x011E))
    IMG_ERR_BAD_NUM_TAPS_PER_X_ZONE                     = _int32((0xBFF60000 + 0x011F))
    IMG_ERR_BAD_NUM_TAPS_PER_Y_ZONE                     = _int32((0xBFF60000 + 0x0120))
    IMG_ERR_BAD_TEST_IMAGE_TYPE                         = _int32((0xBFF60000 + 0x0121))
    IMG_ERR_CANNOT_ACQUIRE_FROM_CAMERA                  = _int32((0xBFF60000 + 0x0122))
    IMG_ERR_BAD_CTRL_LINE_SOURCE                        = _int32((0xBFF60000 + 0x0123))
    IMG_ERR_BAD_PIXEL_EXTRACTOR                         = _int32((0xBFF60000 + 0x0124))
    IMG_ERR_BAD_NUM_TIME_SLOTS                          = _int32((0xBFF60000 + 0x0125))
    IMG_ERR_BAD_PLL_VCO_DIVIDER                         = _int32((0xBFF60000 + 0x0126))
    IMG_ERR_CRITICAL_TEMP                               = _int32((0xBFF60000 + 0x0127))
    IMG_ERR_BAD_DPA_OFFSET                              = _int32((0xBFF60000 + 0x0128))
    IMG_ERR_BAD_NUM_POST_TRIGGER_BUFFERS                = _int32((0xBFF60000 + 0x0129))
    IMG_ERR_BAD_DVAL_MODE                               = _int32((0xBFF60000 + 0x012A))
    IMG_ERR_BAD_TRIG_GEN_REARM_SOURCE                   = _int32((0xBFF60000 + 0x012B))
    IMG_ERR_BAD_ASM_GATE_SOURCE                         = _int32((0xBFF60000 + 0x012C))
    IMG_ERR_TOO_MANY_BUFFERS                            = _int32((0xBFF60000 + 0x012D))
    IMG_ERR_BAD_TAP_4_VALID_RECT                        = _int32((0xBFF60000 + 0x012E))
    IMG_ERR_BAD_TAP_5_VALID_RECT                        = _int32((0xBFF60000 + 0x012F))
    IMG_ERR_BAD_TAP_6_VALID_RECT                        = _int32((0xBFF60000 + 0x0130))
    IMG_ERR_BAD_TAP_7_VALID_RECT                        = _int32((0xBFF60000 + 0x0131))
    IMG_ERR_FRONT_END_BANDWIDTH_EXCEEDED                = _int32((0xBFF60000 + 0x0132))
    IMG_ERR_BAD_PORT_NUMBER                             = _int32((0xBFF60000 + 0x0133))
    IMG_ERR_PORT_CONFIG_CONFLICT                        = _int32((0xBFF60000 + 0x0134))
    IMG_ERR_BITSTREAM_INCOMPATIBLE                      = _int32((0xBFF60000 + 0x0135))
    IMG_ERR_SERIAL_PORT_IN_USE                          = _int32((0xBFF60000 + 0x0136))
    IMG_ERR_BAD_ENCODER_DIVIDE_FACTOR                   = _int32((0xBFF60000 + 0x0137))
    IMG_ERR_ENCODER_NOT_SUPPORTED                       = _int32((0xBFF60000 + 0x0138))
    IMG_ERR_BAD_ENCODER_POLARITY                        = _int32((0xBFF60000 + 0x0139))
    IMG_ERR_BAD_ENCODER_FILTER                          = _int32((0xBFF60000 + 0x013A))
    IMG_ERR_ENCODER_POSITION_NOT_SUPPORTED              = _int32((0xBFF60000 + 0x013B))
    IMG_ERR_IMAGE_IN_USE                                = _int32((0xBFF60000 + 0x013C))
    IMG_ERR_BAD_SCARABXL4000_FILE                       = _int32((0xBFF60000 + 0x013D))
    IMG_ERR_BAD_CAMERA_ATTRIBUTE_VALUE                  = _int32((0xBFF60000 + 0x013E))
    IMG_ERR_BAD_PULSE_WIDTH                             = _int32((0xBFF60000 + 0x013F))
    IMG_ERR_FPGA_FILE_NOT_FOUND                         = _int32((0xBFF60000 + 0x0140))
    IMG_ERR_FPGA_FILE_CORRUPT                           = _int32((0xBFF60000 + 0x0141))
    IMG_ERR_BAD_PULSE_DELAY                             = _int32((0xBFF60000 + 0x0142))
    IMG_ERR_BAD_PG_IDLE_SIGNAL_LEVEL                    = _int32((0xBFF60000 + 0x0143))
    IMG_ERR_BAD_PG_WAVEFORM_IDLE_STATE                  = _int32((0xBFF60000 + 0x0144))
    IMG_ERR_64_BIT_MEMORY_NOT_SUPPORTED                 = _int32((0xBFF60000 + 0x0145))
    IMG_ERR_64_BIT_MEMORY_UPDATE_AVAILABLE              = _int32((0xBFF60000 + 0x0146))
    IMG_ERR_32_BIT_MEMORY_LIMITATION                    = _int32((0xBFF60000 + 0x0147))
    IMG_ERR_KERNEL_NOT_LOADED                           = _int32((0xBFF60000 + 0x0148))
    IMG_ERR_BAD_SENSOR_SHUTTER_PERIOD                   = _int32((0xBFF60000 + 0x0149))
    IMG_ERR_BAD_SENSOR_CCD_TYPE                         = _int32((0xBFF60000 + 0x014A))
    IMG_ERR_BAD_SENSOR_PARTIAL_SCAN                     = _int32((0xBFF60000 + 0x014B))
    IMG_ERR_BAD_SENSOR_BINNING                          = _int32((0xBFF60000 + 0x014C))
    IMG_ERR_BAD_SENSOR_GAIN                             = _int32((0xBFF60000 + 0x014D))
    IMG_ERR_BAD_SENSOR_BRIGHTNESS                       = _int32((0xBFF60000 + 0x014E))
    IMG_ERR_BAD_LED_STATE                               = _int32((0xBFF60000 + 0x014F))
    IMG_ERR_64_BIT_NOT_SUPPORTED                        = _int32((0xBFF60000 + 0x0150))
    IMG_ERR_BAD_TRIGGER_DELAY                           = _int32((0xBFF60000 + 0x0151))
    IMG_ERR_LIGHTING_CURRENT_EXCEEDS_LIMITS             = _int32((0xBFF60000 + 0x0152))
    IMG_ERR_LIGHTING_INVALID_MODE                       = _int32((0xBFF60000 + 0x0153))
    IMG_ERR_LIGHTING_EXTERNAL_INVALID_MODE              = _int32((0xBFF60000 + 0x0154))
    IMG_ERR_BAD_SENSOR_EXPOSURE                         = _int32((0xBFF60000 + 0x0155))
    IMG_ERR_BAD_FRAME_RATE                              = _int32((0xBFF60000 + 0x0156))
    IMG_ERR_BAD_SENSOR_PARTIAL_SCAN_BINNING_COMBINATION = _int32((0xBFF60000 + 0x0157))
    IMG_ERR_SOFTWARE_TRIGGER_NOT_CONFIGURED             = _int32((0xBFF60000 + 0x0158))
    IMG_ERR_FREE_RUN_MODE_NOT_ALLOWED                   = _int32((0xBFF60000 + 0x0159))
    IMG_ERR_BAD_LIGHTING_RAMPUP                         = _int32((0xBFF60000 + 0x015A))
    IMG_ERR_AFE_CONFIG_TIMEOUT                          = _int32((0xBFF60000 + 0x015B))
    IMG_ERR_LIGHTING_ARM_TIMEOUT                        = _int32((0xBFF60000 + 0x015C))
    IMG_ERR_LIGHTING_SHORT_CIRCUIT                      = _int32((0xBFF60000 + 0x015D))
    IMG_ERR_BAD_BOARD_HEALTH                            = _int32((0xBFF60000 + 0x015E))
    IMG_ERR_LIGHTING_BAD_CONTINUOUS_CURRENT_LIMIT       = _int32((0xBFF60000 + 0x015F))
    IMG_ERR_LIGHTING_BAD_STROBE_DUTY_CYCLE_LIMIT        = _int32((0xBFF60000 + 0x0160))
    IMG_ERR_LIGHTING_BAD_STROBE_DURATION_LIMIT          = _int32((0xBFF60000 + 0x0161))
    IMG_ERR_BAD_LIGHTING_CURRENT_EXPOSURE_COMBINATION   = _int32((0xBFF60000 + 0x0162))
    IMG_ERR_LIGHTING_HEAD_CONFIG_NOT_FOUND              = _int32((0xBFF60000 + 0x0163))
    IMG_ERR_LIGHTING_HEAD_DATA_CORRUPT                  = _int32((0xBFF60000 + 0x0164))
    IMG_ERR_LIGHTING_ABORT_TIMEOUT                      = _int32((0xBFF60000 + 0x0165))
    IMG_ERR_LIGHTING_BAD_STROBE_CURRENT_LIMIT           = _int32((0xBFF60000 + 0x0166))
    IMG_ERR_DMA_ENGINE_UNRESPONSIVE                     = _int32((0xBFF60000 + 0x0167))
    IMG_ERR_IMAGE_NOT_32BYTE_ALIGNED                    = _int32((0xBFF60000 + 0x0168))
    IMG_ERR_IMAGE_BORDER_NONZERO                        = _int32((0xBFF60000 + 0x0169))
    IMG_ERR_POCL_FAULT                                  = _int32((0xBFF60000 + 0x0170))
    IMG_ERR_POCL_VIDEO_LOCK                             = _int32((0xBFF60000 + 0x0171))
    IMG_ERR_POCL_BAD_FUSE                               = _int32((0xBFF60000 + 0x0172))
    IMG_ERR_POCL_NO_AUX_POWER                           = _int32((0xBFF60000 + 0x0173))
    IMG_ERR_PULSE_UPDATE_NOT_SUPPORTED                  = _int32((0xBFF60000 + 0x0174))
    IMG_ERR_LAST_ERROR                                  = _int32((0xBFF60000 + 0x0174))
dIMG_ERR_CODE={a.name:a.value for a in IMG_ERR_CODE}
drIMG_ERR_CODE={a.value:a.name for a in IMG_ERR_CODE}


class REVISIONS(enum.IntEnum):
    PCIIMAQ1408_REVA = _int32(0x00000000)
    PCIIMAQ1408_REVB = _int32(0x00000001)
    PCIIMAQ1408_REVC = _int32(0x00000002)
    PCIIMAQ1408_REVF = _int32(0x00000003)
    PCIIMAQ1408_REVX = _int32(0x00000004)
dREVISIONS={a.name:a.value for a in REVISIONS}
drREVISIONS={a.value:a.name for a in REVISIONS}


class DEVID(enum.IntEnum):
    IMAQ_PCI_1405  = _int32(0x70CA1093)
    IMAQ_PXI_1405  = _int32(0x70CE1093)
    IMAQ_PCI_1407  = _int32(0xB0411093)
    IMAQ_PXI_1407  = _int32(0xB0511093)
    IMAQ_PCI_1408  = _int32(0xB0011093)
    IMAQ_PXI_1408  = _int32(0xB0111093)
    IMAQ_PCI_1409  = _int32(0xB0B11093)
    IMAQ_PXI_1409  = _int32(0xB0C11093)
    IMAQ_PCI_1410  = _int32(0x71871093)
    IMAQ_PCI_1411  = _int32(0xB0611093)
    IMAQ_PXI_1411  = _int32(0xB0911093)
    IMAQ_PCI_1413  = _int32(0xB0311093)
    IMAQ_PXI_1413  = _int32(0xB0321093)
    IMAQ_PCI_1422  = _int32(0xB0711093)
    IMAQ_PXI_1422  = _int32(0xB0811093)
    IMAQ_PCI_1423  = _int32(0x70281093)
    IMAQ_PXI_1423  = _int32(0x70291093)
    IMAQ_PCI_1424  = _int32(0xB0211093)
    IMAQ_PXI_1424  = _int32(0xB0221093)
    IMAQ_PCI_1426  = _int32(0x715D1093)
    IMAQ_PCIe_1427 = _int32(0x71BF1093)
    IMAQ_PCI_1428  = _int32(0xB0E11093)
    IMAQ_PXI_1428  = _int32(0x707C1093)
    IMAQ_PCIX_1429 = _int32(0x71041093)
    IMAQ_PCIe_1429 = _int32(0x71051093)
    IMAQ_PCIe_1430 = _int32(0x71AE1093)
    IMAQ_PCIe_1433 = _int32(0x74B61093)
    IMAQ_PXIe_1435 = _int32(0x753C1093)
    IMAQ_PXIe_1436 = _int32(0x756E1093)
    IMAQ_17xx      = _int32(0x71EC1093)
dDEVID={a.name:a.value for a in DEVID}
drDEVID={a.value:a.name for a in DEVID}





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
uInt8=ctypes.c_ubyte
uInt16=ctypes.c_ushort
uInt32=ctypes.c_uint
Int8=ctypes.c_char
Int32=ctypes.c_int
Ptr=ctypes.c_char_p
INTERFACE_ID=uInt32
SESSION_ID=uInt32
PULSE_ID=uInt32
BUFLIST_ID=uInt32
IMG_ERR=Int32
MirEGLNativeWindowType=ctypes.c_void_p
MirEGLNativeDisplayType=ctypes.c_void_p
class IMG_SIGNAL_STATE(enum.IntEnum):
    IMG_SIGNAL_STATE_RISING =_int32(0)
    IMG_SIGNAL_STATE_FALLING=_int32(1)
    IMG_SIGNAL_STATE_HIGH   =_int32(2)
    IMG_SIGNAL_STATE_LOW    =_int32(3)
    IMG_SIGNAL_STATE_HI_Z   =_int32(4)
dIMG_SIGNAL_STATE={a.name:a.value for a in IMG_SIGNAL_STATE}
drIMG_SIGNAL_STATE={a.value:a.name for a in IMG_SIGNAL_STATE}


class IMG_ROI_FIT_MODE(enum.IntEnum):
    IMG_ROI_FIT_LARGER =_int32(0)
    IMG_ROI_FIT_SMALLER=enum.auto()
dIMG_ROI_FIT_MODE={a.name:a.value for a in IMG_ROI_FIT_MODE}
drIMG_ROI_FIT_MODE={a.value:a.name for a in IMG_ROI_FIT_MODE}


class IMG_SIGNAL_TYPE(enum.IntEnum):
    IMG_SIGNAL_NONE            =_int32(0xFFFFFFFF)
    IMG_SIGNAL_EXTERNAL        =_int32(0)
    IMG_SIGNAL_RTSI            =_int32(1)
    IMG_SIGNAL_ISO_IN          =_int32(2)
    IMG_SIGNAL_ISO_OUT         =_int32(3)
    IMG_SIGNAL_STATUS          =_int32(4)
    IMG_SIGNAL_SCALED_ENCODER  =_int32(5)
    IMG_SIGNAL_SOFTWARE_TRIGGER=_int32(6)
dIMG_SIGNAL_TYPE={a.name:a.value for a in IMG_SIGNAL_TYPE}
drIMG_SIGNAL_TYPE={a.value:a.name for a in IMG_SIGNAL_TYPE}


class IMG_OVERWRITE_MODE(enum.IntEnum):
    IMG_OVERWRITE_GET_OLDEST        =_int32(0)
    IMG_OVERWRITE_GET_NEXT_ITERATION=_int32(1)
    IMG_OVERWRITE_FAIL              =_int32(2)
    IMG_OVERWRITE_GET_NEWEST        =_int32(3)
dIMG_OVERWRITE_MODE={a.name:a.value for a in IMG_OVERWRITE_MODE}
drIMG_OVERWRITE_MODE={a.value:a.name for a in IMG_OVERWRITE_MODE}


class IMG_SENSOR_PARTIAL_SCAN(enum.IntEnum):
    IMG_SENSOR_PARTIAL_SCAN_OFF    =_int32(0)
    IMG_SENSOR_PARTIAL_SCAN_HALF   =_int32(1)
    IMG_SENSOR_PARTIAL_SCAN_QUARTER=_int32(2)
dIMG_SENSOR_PARTIAL_SCAN={a.name:a.value for a in IMG_SENSOR_PARTIAL_SCAN}
drIMG_SENSOR_PARTIAL_SCAN={a.value:a.name for a in IMG_SENSOR_PARTIAL_SCAN}


class IMG_SENSOR_BINNING(enum.IntEnum):
    IMG_SENSOR_BINNING_OFF=_int32(0)
    IMG_SENSOR_BINNING_1x2=_int32(1)
dIMG_SENSOR_BINNING={a.name:a.value for a in IMG_SENSOR_BINNING}
drIMG_SENSOR_BINNING={a.value:a.name for a in IMG_SENSOR_BINNING}


class IMG_LED_STATE(enum.IntEnum):
    IMG_LED_OFF=_int32(0)
    IMG_LED_ON =_int32(1)
dIMG_LED_STATE={a.name:a.value for a in IMG_LED_STATE}
drIMG_LED_STATE={a.value:a.name for a in IMG_LED_STATE}


class IMG_TIMEBASE(enum.IntEnum):
    IMG_TIMEBASE_PIXELCLK      =_int32(1)
    IMG_TIMEBASE_50MHZ         =_int32(2)
    IMG_TIMEBASE_100KHZ        =_int32(3)
    IMG_TIMEBASE_SCALED_ENCODER=_int32(4)
    IMG_TIMEBASE_MILLISECONDS  =_int32(5)
dIMG_TIMEBASE={a.name:a.value for a in IMG_TIMEBASE}
drIMG_TIMEBASE={a.value:a.name for a in IMG_TIMEBASE}


class IMG_LIGHTING_MODE(enum.IntEnum):
    IMG_LIGHTING_OFF       =_int32(0)
    IMG_LIGHTING_CONTINUOUS=_int32(1)
    IMG_LIGHTING_STROBED   =_int32(2)
dIMG_LIGHTING_MODE={a.name:a.value for a in IMG_LIGHTING_MODE}
drIMG_LIGHTING_MODE={a.value:a.name for a in IMG_LIGHTING_MODE}


class IMG_LIGHTING_EXTERNAL_STROBE_MODE(enum.IntEnum):
    IMG_LIGHTING_EXTERNAL_STROBE_OFF    =_int32(0)
    IMG_LIGHTING_EXTERNAL_STROBE_RISING =_int32(1)
    IMG_LIGHTING_EXTERNAL_STROBE_FALLING=_int32(2)
dIMG_LIGHTING_EXTERNAL_STROBE_MODE={a.name:a.value for a in IMG_LIGHTING_EXTERNAL_STROBE_MODE}
drIMG_LIGHTING_EXTERNAL_STROBE_MODE={a.value:a.name for a in IMG_LIGHTING_EXTERNAL_STROBE_MODE}


CALL_BACK_PTR=ctypes.c_void_p
CALL_BACK_PTR2=ctypes.c_void_p



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
    #  Int32 imgInterfaceOpen(ctypes.c_char_p interface_name, ctypes.POINTER(INTERFACE_ID) ifid)
    addfunc(lib, "imgInterfaceOpen", restype = Int32,
            argtypes = [ctypes.c_char_p, ctypes.POINTER(INTERFACE_ID)],
            argnames = ["interface_name", "ifid"] )
    #  Int32 imgSessionOpen(INTERFACE_ID ifid, ctypes.POINTER(SESSION_ID) sid)
    addfunc(lib, "imgSessionOpen", restype = Int32,
            argtypes = [INTERFACE_ID, ctypes.POINTER(SESSION_ID)],
            argnames = ["ifid", "sid"] )
    #  Int32 imgClose(uInt32 void_id, uInt32 freeResources)
    addfunc(lib, "imgClose", restype = Int32,
            argtypes = [uInt32, uInt32],
            argnames = ["void_id", "freeResources"] )
    #  Int32 imgSnap(SESSION_ID sid, ctypes.POINTER(ctypes.c_void_p) bufAddr)
    addfunc(lib, "imgSnap", restype = Int32,
            argtypes = [SESSION_ID, ctypes.POINTER(ctypes.c_void_p)],
            argnames = ["sid", "bufAddr"] )
    #  Int32 imgSnapArea(SESSION_ID sid, ctypes.POINTER(ctypes.c_void_p) bufAddr, uInt32 top, uInt32 left, uInt32 height, uInt32 width, uInt32 rowBytes)
    addfunc(lib, "imgSnapArea", restype = Int32,
            argtypes = [SESSION_ID, ctypes.POINTER(ctypes.c_void_p), uInt32, uInt32, uInt32, uInt32, uInt32],
            argnames = ["sid", "bufAddr", "top", "left", "height", "width", "rowBytes"] )
    #  Int32 imgGrabSetup(SESSION_ID sid, uInt32 startNow)
    addfunc(lib, "imgGrabSetup", restype = Int32,
            argtypes = [SESSION_ID, uInt32],
            argnames = ["sid", "startNow"] )
    #  Int32 imgGrab(SESSION_ID sid, ctypes.POINTER(ctypes.c_void_p) bufPtr, uInt32 syncOnVB)
    addfunc(lib, "imgGrab", restype = Int32,
            argtypes = [SESSION_ID, ctypes.POINTER(ctypes.c_void_p), uInt32],
            argnames = ["sid", "bufPtr", "syncOnVB"] )
    #  Int32 imgGrabArea(SESSION_ID sid, ctypes.POINTER(ctypes.c_void_p) bufPtr, uInt32 syncOnVB, uInt32 top, uInt32 left, uInt32 height, uInt32 width, uInt32 rowBytes)
    addfunc(lib, "imgGrabArea", restype = Int32,
            argtypes = [SESSION_ID, ctypes.POINTER(ctypes.c_void_p), uInt32, uInt32, uInt32, uInt32, uInt32, uInt32],
            argnames = ["sid", "bufPtr", "syncOnVB", "top", "left", "height", "width", "rowBytes"] )
    #  Int32 imgRingSetup(SESSION_ID sid, uInt32 numberBuffer, ctypes.POINTER(ctypes.c_void_p) bufferList, uInt32 skipCount, uInt32 startnow)
    addfunc(lib, "imgRingSetup", restype = Int32,
            argtypes = [SESSION_ID, uInt32, ctypes.POINTER(ctypes.c_void_p), uInt32, uInt32],
            argnames = ["sid", "numberBuffer", "bufferList", "skipCount", "startnow"] )
    #  Int32 imgSequenceSetup(SESSION_ID sid, uInt32 numberBuffer, ctypes.POINTER(ctypes.c_void_p) bufferList, ctypes.POINTER(uInt32) skipCount, uInt32 startnow, uInt32 async)
    addfunc(lib, "imgSequenceSetup", restype = Int32,
            argtypes = [SESSION_ID, uInt32, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(uInt32), uInt32, uInt32],
            argnames = ["sid", "numberBuffer", "bufferList", "skipCount", "startnow", "async"] )
    #  Int32 imgSessionStartAcquisition(SESSION_ID sid)
    addfunc(lib, "imgSessionStartAcquisition", restype = Int32,
            argtypes = [SESSION_ID],
            argnames = ["sid"] )
    #  Int32 imgSessionStopAcquisition(SESSION_ID sid)
    addfunc(lib, "imgSessionStopAcquisition", restype = Int32,
            argtypes = [SESSION_ID],
            argnames = ["sid"] )
    #  Int32 imgSessionStatus(SESSION_ID sid, ctypes.POINTER(uInt32) boardStatus, ctypes.POINTER(uInt32) bufIndex)
    addfunc(lib, "imgSessionStatus", restype = Int32,
            argtypes = [SESSION_ID, ctypes.POINTER(uInt32), ctypes.POINTER(uInt32)],
            argnames = ["sid", "boardStatus", "bufIndex"] )
    #  Int32 imgSessionConfigureROI(SESSION_ID sid, uInt32 top, uInt32 left, uInt32 height, uInt32 width)
    addfunc(lib, "imgSessionConfigureROI", restype = Int32,
            argtypes = [SESSION_ID, uInt32, uInt32, uInt32, uInt32],
            argnames = ["sid", "top", "left", "height", "width"] )
    #  Int32 imgSessionGetROI(SESSION_ID sid, ctypes.POINTER(uInt32) top, ctypes.POINTER(uInt32) left, ctypes.POINTER(uInt32) height, ctypes.POINTER(uInt32) width)
    addfunc(lib, "imgSessionGetROI", restype = Int32,
            argtypes = [SESSION_ID, ctypes.POINTER(uInt32), ctypes.POINTER(uInt32), ctypes.POINTER(uInt32), ctypes.POINTER(uInt32)],
            argnames = ["sid", "top", "left", "height", "width"] )
    #  Int32 imgSessionGetBufferSize(SESSION_ID sid, ctypes.POINTER(uInt32) sizeNeeded)
    addfunc(lib, "imgSessionGetBufferSize", restype = Int32,
            argtypes = [SESSION_ID, ctypes.POINTER(uInt32)],
            argnames = ["sid", "sizeNeeded"] )
    #  Int32 imgGetAttribute(uInt32 void_id, uInt32 attribute, ctypes.c_void_p value)
    addfunc(lib, "imgGetAttribute", restype = Int32,
            argtypes = [uInt32, uInt32, ctypes.c_void_p],
            argnames = ["void_id", "attribute", "value"] )
    #  Int32 imgCreateBuffer(SESSION_ID sid, uInt32 where, uInt32 bufferSize, ctypes.POINTER(ctypes.c_void_p) bufAddr)
    addfunc(lib, "imgCreateBuffer", restype = Int32,
            argtypes = [SESSION_ID, uInt32, uInt32, ctypes.POINTER(ctypes.c_void_p)],
            argnames = ["sid", "where", "bufferSize", "bufAddr"] )
    #  Int32 imgDisposeBuffer(ctypes.c_void_p bufferPtr)
    addfunc(lib, "imgDisposeBuffer", restype = Int32,
            argtypes = [ctypes.c_void_p],
            argnames = ["bufferPtr"] )
    #  Int32 imgCreateBufList(uInt32 numElements, ctypes.POINTER(BUFLIST_ID) bufListId)
    addfunc(lib, "imgCreateBufList", restype = Int32,
            argtypes = [uInt32, ctypes.POINTER(BUFLIST_ID)],
            argnames = ["numElements", "bufListId"] )
    #  Int32 imgDisposeBufList(BUFLIST_ID bid, uInt32 freeResources)
    addfunc(lib, "imgDisposeBufList", restype = Int32,
            argtypes = [BUFLIST_ID, uInt32],
            argnames = ["bid", "freeResources"] )
    #  Int32 imgGetBufferElement(BUFLIST_ID bid, uInt32 element, uInt32 itemType, ctypes.c_void_p itemValue)
    addfunc(lib, "imgGetBufferElement", restype = Int32,
            argtypes = [BUFLIST_ID, uInt32, uInt32, ctypes.c_void_p],
            argnames = ["bid", "element", "itemType", "itemValue"] )
    #  Int32 imgSessionConfigure(SESSION_ID sid, BUFLIST_ID buflist)
    addfunc(lib, "imgSessionConfigure", restype = Int32,
            argtypes = [SESSION_ID, BUFLIST_ID],
            argnames = ["sid", "buflist"] )
    #  Int32 imgSessionAcquire(SESSION_ID sid, uInt32 async, CALL_BACK_PTR callback)
    addfunc(lib, "imgSessionAcquire", restype = Int32,
            argtypes = [SESSION_ID, uInt32, CALL_BACK_PTR],
            argnames = ["sid", "async", "callback"] )
    #  Int32 imgSessionAbort(SESSION_ID sid, ctypes.POINTER(uInt32) bufNum)
    addfunc(lib, "imgSessionAbort", restype = Int32,
            argtypes = [SESSION_ID, ctypes.POINTER(uInt32)],
            argnames = ["sid", "bufNum"] )
    #  Int32 imgSessionReleaseBuffer(SESSION_ID sid)
    addfunc(lib, "imgSessionReleaseBuffer", restype = Int32,
            argtypes = [SESSION_ID],
            argnames = ["sid"] )
    #  Int32 imgSessionClearBuffer(SESSION_ID sid, uInt32 buf_num, uInt8 pixel_value)
    addfunc(lib, "imgSessionClearBuffer", restype = Int32,
            argtypes = [SESSION_ID, uInt32, uInt8],
            argnames = ["sid", "buf_num", "pixel_value"] )
    #  Int32 imgSessionGetLostFramesList(SESSION_ID sid, ctypes.POINTER(uInt32) framelist, uInt32 numEntries)
    addfunc(lib, "imgSessionGetLostFramesList", restype = Int32,
            argtypes = [SESSION_ID, ctypes.POINTER(uInt32), uInt32],
            argnames = ["sid", "framelist", "numEntries"] )
    #  Int32 imgSessionSetUserLUT8bit(SESSION_ID sid, uInt32 lutType, ctypes.POINTER(uInt8) lut)
    addfunc(lib, "imgSessionSetUserLUT8bit", restype = Int32,
            argtypes = [SESSION_ID, uInt32, ctypes.POINTER(uInt8)],
            argnames = ["sid", "lutType", "lut"] )
    #  Int32 imgSessionSetUserLUT16bit(SESSION_ID sid, uInt32 lutType, ctypes.POINTER(uInt16) lut)
    addfunc(lib, "imgSessionSetUserLUT16bit", restype = Int32,
            argtypes = [SESSION_ID, uInt32, ctypes.POINTER(uInt16)],
            argnames = ["sid", "lutType", "lut"] )
    #  Int32 imgGetCameraAttributeNumeric(SESSION_ID sid, ctypes.c_char_p attributeString, ctypes.POINTER(ctypes.c_double) currentValueNumeric)
    addfunc(lib, "imgGetCameraAttributeNumeric", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)],
            argnames = ["sid", "attributeString", "currentValueNumeric"] )
    #  Int32 imgSetCameraAttributeNumeric(SESSION_ID sid, ctypes.c_char_p attributeString, ctypes.c_double newValueNumeric)
    addfunc(lib, "imgSetCameraAttributeNumeric", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_char_p, ctypes.c_double],
            argnames = ["sid", "attributeString", "newValueNumeric"] )
    #  Int32 imgGetCameraAttributeString(SESSION_ID sid, ctypes.c_char_p attributeString, ctypes.c_char_p currentValueString, uInt32 sizeofCurrentValueString)
    addfunc(lib, "imgGetCameraAttributeString", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_char_p, ctypes.c_char_p, uInt32],
            argnames = ["sid", "attributeString", "currentValueString", "sizeofCurrentValueString"] )
    #  Int32 imgSetCameraAttributeString(SESSION_ID sid, ctypes.c_char_p attributeString, ctypes.c_char_p newValueString)
    addfunc(lib, "imgSetCameraAttributeString", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_char_p, ctypes.c_char_p],
            argnames = ["sid", "attributeString", "newValueString"] )
    #  Int32 imgSessionSerialWrite(SESSION_ID sid, ctypes.c_char_p buffer, ctypes.POINTER(uInt32) bufSize, uInt32 timeout)
    addfunc(lib, "imgSessionSerialWrite", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_char_p, ctypes.POINTER(uInt32), uInt32],
            argnames = ["sid", "buffer", "bufSize", "timeout"] )
    #  Int32 imgSessionSerialRead(SESSION_ID sid, ctypes.c_char_p buffer, ctypes.POINTER(uInt32) bufSize, uInt32 timeout)
    addfunc(lib, "imgSessionSerialRead", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_char_p, ctypes.POINTER(uInt32), uInt32],
            argnames = ["sid", "buffer", "bufSize", "timeout"] )
    #  Int32 imgSessionSerialReadBytes(SESSION_ID sid, ctypes.c_char_p buffer, ctypes.POINTER(uInt32) bufferSize, uInt32 timeout)
    addfunc(lib, "imgSessionSerialReadBytes", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_char_p, ctypes.POINTER(uInt32), uInt32],
            argnames = ["sid", "buffer", "bufferSize", "timeout"] )
    #  Int32 imgSessionSerialFlush(SESSION_ID sid)
    addfunc(lib, "imgSessionSerialFlush", restype = Int32,
            argtypes = [SESSION_ID],
            argnames = ["sid"] )
    #  Int32 imgPulseCreate2(uInt32 timeBase, uInt32 delay, uInt32 width, ctypes.c_int signalType, uInt32 signalIdentifier, uInt32 signalPolarity, ctypes.c_int outputType, uInt32 outputNumber, uInt32 outputPolarity, uInt32 pulseMode, ctypes.POINTER(PULSE_ID) plsID)
    addfunc(lib, "imgPulseCreate2", restype = Int32,
            argtypes = [uInt32, uInt32, uInt32, ctypes.c_int, uInt32, uInt32, ctypes.c_int, uInt32, uInt32, uInt32, ctypes.POINTER(PULSE_ID)],
            argnames = ["timeBase", "delay", "width", "signalType", "signalIdentifier", "signalPolarity", "outputType", "outputNumber", "outputPolarity", "pulseMode", "plsID"] )
    #  Int32 imgPulseDispose(PULSE_ID plsID)
    addfunc(lib, "imgPulseDispose", restype = Int32,
            argtypes = [PULSE_ID],
            argnames = ["plsID"] )
    #  Int32 imgPulseRate(ctypes.c_double delaytime, ctypes.c_double widthtime, ctypes.POINTER(uInt32) delay, ctypes.POINTER(uInt32) width, ctypes.POINTER(uInt32) timebase)
    addfunc(lib, "imgPulseRate", restype = Int32,
            argtypes = [ctypes.c_double, ctypes.c_double, ctypes.POINTER(uInt32), ctypes.POINTER(uInt32), ctypes.POINTER(uInt32)],
            argnames = ["delaytime", "widthtime", "delay", "width", "timebase"] )
    #  Int32 imgPulseStart(PULSE_ID pid, SESSION_ID sid)
    addfunc(lib, "imgPulseStart", restype = Int32,
            argtypes = [PULSE_ID, SESSION_ID],
            argnames = ["pid", "sid"] )
    #  Int32 imgPulseUpdate(PULSE_ID pid, SESSION_ID sid, uInt32 delay, uInt32 width)
    addfunc(lib, "imgPulseUpdate", restype = Int32,
            argtypes = [PULSE_ID, SESSION_ID, uInt32, uInt32],
            argnames = ["pid", "sid", "delay", "width"] )
    #  Int32 imgPulseStop(PULSE_ID pid)
    addfunc(lib, "imgPulseStop", restype = Int32,
            argtypes = [PULSE_ID],
            argnames = ["pid"] )
    #  Int32 imgSessionWaitSignal2(SESSION_ID sid, ctypes.c_int signalType, uInt32 signalIdentifier, uInt32 signalPolarity, uInt32 timeout)
    addfunc(lib, "imgSessionWaitSignal2", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_int, uInt32, uInt32, uInt32],
            argnames = ["sid", "signalType", "signalIdentifier", "signalPolarity", "timeout"] )
    #  Int32 imgSessionWaitSignalAsync2(SESSION_ID sid, ctypes.c_int signalType, uInt32 signalIdentifier, uInt32 signalPolarity, CALL_BACK_PTR2 funcptr, ctypes.c_void_p callbackData)
    addfunc(lib, "imgSessionWaitSignalAsync2", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_int, uInt32, uInt32, CALL_BACK_PTR2, ctypes.c_void_p],
            argnames = ["sid", "signalType", "signalIdentifier", "signalPolarity", "funcptr", "callbackData"] )
    #  Int32 imgSessionTriggerDrive2(SESSION_ID sid, ctypes.c_int trigType, uInt32 trigNum, uInt32 polarity, uInt32 signal)
    addfunc(lib, "imgSessionTriggerDrive2", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_int, uInt32, uInt32, uInt32],
            argnames = ["sid", "trigType", "trigNum", "polarity", "signal"] )
    #  Int32 imgSessionTriggerRead2(SESSION_ID sid, ctypes.c_int trigType, uInt32 trigNum, uInt32 polarity, ctypes.POINTER(uInt32) status)
    addfunc(lib, "imgSessionTriggerRead2", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_int, uInt32, uInt32, ctypes.POINTER(uInt32)],
            argnames = ["sid", "trigType", "trigNum", "polarity", "status"] )
    #  Int32 imgSessionTriggerRoute2(SESSION_ID sid, ctypes.c_int srcTriggerType, uInt32 srcTriggerNumber, ctypes.c_int dstTriggerType, uInt32 dstTriggerNumber)
    addfunc(lib, "imgSessionTriggerRoute2", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_int, uInt32, ctypes.c_int, uInt32],
            argnames = ["sid", "srcTriggerType", "srcTriggerNumber", "dstTriggerType", "dstTriggerNumber"] )
    #  Int32 imgSessionTriggerClear(SESSION_ID sid)
    addfunc(lib, "imgSessionTriggerClear", restype = Int32,
            argtypes = [SESSION_ID],
            argnames = ["sid"] )
    #  Int32 imgSessionTriggerConfigure2(SESSION_ID sid, ctypes.c_int trigType, uInt32 trigNum, uInt32 polarity, uInt32 timeout, uInt32 action)
    addfunc(lib, "imgSessionTriggerConfigure2", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_int, uInt32, uInt32, uInt32, uInt32],
            argnames = ["sid", "trigType", "trigNum", "polarity", "timeout", "action"] )
    #  Int32 imgSessionSaveBufferEx(SESSION_ID sid, ctypes.c_void_p buffer, ctypes.c_char_p file_name)
    addfunc(lib, "imgSessionSaveBufferEx", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_void_p, ctypes.c_char_p],
            argnames = ["sid", "buffer", "file_name"] )
    #  Int32 imgShowError(IMG_ERR error, ctypes.c_char_p text)
    addfunc(lib, "imgShowError", restype = Int32,
            argtypes = [IMG_ERR, ctypes.c_char_p],
            argnames = ["error", "text"] )
    #  Int32 imgInterfaceReset(INTERFACE_ID ifid)
    addfunc(lib, "imgInterfaceReset", restype = Int32,
            argtypes = [INTERFACE_ID],
            argnames = ["ifid"] )
    #  Int32 imgInterfaceQueryNames(uInt32 index, ctypes.c_char_p queryName)
    addfunc(lib, "imgInterfaceQueryNames", restype = Int32,
            argtypes = [uInt32, ctypes.c_char_p],
            argnames = ["index", "queryName"] )
    #  Int32 imgCalculateBayerColorLUT(ctypes.c_double redGain, ctypes.c_double greenGain, ctypes.c_double blueGain, ctypes.POINTER(uInt32) redLUT, ctypes.POINTER(uInt32) greenLUT, ctypes.POINTER(uInt32) blueLUT, uInt32 bitDepth)
    addfunc(lib, "imgCalculateBayerColorLUT", restype = Int32,
            argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(uInt32), ctypes.POINTER(uInt32), ctypes.POINTER(uInt32), uInt32],
            argnames = ["redGain", "greenGain", "blueGain", "redLUT", "greenLUT", "blueLUT", "bitDepth"] )
    #  Int32 imgBayerColorDecode(ctypes.c_void_p dst, ctypes.c_void_p src, uInt32 rows, uInt32 cols, uInt32 dstRowPixels, uInt32 srcRowPixels, ctypes.POINTER(uInt32) redLUT, ctypes.POINTER(uInt32) greenLUT, ctypes.POINTER(uInt32) blueLUT, uInt8 bayerPattern, uInt32 bitDepth, uInt32 reserved)
    addfunc(lib, "imgBayerColorDecode", restype = Int32,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, uInt32, uInt32, uInt32, uInt32, ctypes.POINTER(uInt32), ctypes.POINTER(uInt32), ctypes.POINTER(uInt32), uInt8, uInt32, uInt32],
            argnames = ["dst", "src", "rows", "cols", "dstRowPixels", "srcRowPixels", "redLUT", "greenLUT", "blueLUT", "bayerPattern", "bitDepth", "reserved"] )
    #  Int32 imgSessionLineTrigSource2(SESSION_ID sid, ctypes.c_int trigType, uInt32 trigNum, uInt32 polarity, uInt32 skip)
    addfunc(lib, "imgSessionLineTrigSource2", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_int, uInt32, uInt32, uInt32],
            argnames = ["sid", "trigType", "trigNum", "polarity", "skip"] )
    #  Int32 imgSessionFitROI(SESSION_ID sid, ctypes.c_int fitMode, uInt32 top, uInt32 left, uInt32 height, uInt32 width, ctypes.POINTER(uInt32) fittedTop, ctypes.POINTER(uInt32) fittedLeft, ctypes.POINTER(uInt32) fittedHeight, ctypes.POINTER(uInt32) fittedWidth)
    addfunc(lib, "imgSessionFitROI", restype = Int32,
            argtypes = [SESSION_ID, ctypes.c_int, uInt32, uInt32, uInt32, uInt32, ctypes.POINTER(uInt32), ctypes.POINTER(uInt32), ctypes.POINTER(uInt32), ctypes.POINTER(uInt32)],
            argnames = ["sid", "fitMode", "top", "left", "height", "width", "fittedTop", "fittedLeft", "fittedHeight", "fittedWidth"] )
    #  Int32 imgEncoderResetPosition(SESSION_ID sid)
    addfunc(lib, "imgEncoderResetPosition", restype = Int32,
            argtypes = [SESSION_ID],
            argnames = ["sid"] )
    #  Int32 imgSessionCopyBufferByNumber(SESSION_ID sid, uInt32 bufNumber, ctypes.c_void_p userBuffer, ctypes.c_int overwriteMode, ctypes.POINTER(uInt32) copiedNumber, ctypes.POINTER(uInt32) copiedIndex)
    addfunc(lib, "imgSessionCopyBufferByNumber", restype = Int32,
            argtypes = [SESSION_ID, uInt32, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(uInt32), ctypes.POINTER(uInt32)],
            argnames = ["sid", "bufNumber", "userBuffer", "overwriteMode", "copiedNumber", "copiedIndex"] )
    #  Int32 imgSessionCopyAreaByNumber(SESSION_ID sid, uInt32 bufNumber, uInt32 top, uInt32 left, uInt32 height, uInt32 width, ctypes.c_void_p userBuffer, uInt32 rowPixels, ctypes.c_int overwriteMode, ctypes.POINTER(uInt32) copiedNumber, ctypes.POINTER(uInt32) copiedIndex)
    addfunc(lib, "imgSessionCopyAreaByNumber", restype = Int32,
            argtypes = [SESSION_ID, uInt32, uInt32, uInt32, uInt32, uInt32, ctypes.c_void_p, uInt32, ctypes.c_int, ctypes.POINTER(uInt32), ctypes.POINTER(uInt32)],
            argnames = ["sid", "bufNumber", "top", "left", "height", "width", "userBuffer", "rowPixels", "overwriteMode", "copiedNumber", "copiedIndex"] )
    #  Int32 imgSetAttribute2(uInt32 void_id, uInt32 attribute, ...)
    addfunc(lib, "imgSetAttribute2", restype = Int32,
            argtypes = None,
            argnames = None )
    #  Int32 imgSetBufferElement2(BUFLIST_ID bid, uInt32 element, uInt32 itemType, ...)
    addfunc(lib, "imgSetBufferElement2", restype = Int32,
            argtypes = None,
            argnames = None )
    #  Int32 imgSessionExamineBuffer2(SESSION_ID sid, uInt32 whichBuffer, ctypes.POINTER(uInt32) bufferNumber, ctypes.POINTER(ctypes.c_void_p) bufferAddr)
    addfunc(lib, "imgSessionExamineBuffer2", restype = Int32,
            argtypes = [SESSION_ID, uInt32, ctypes.POINTER(uInt32), ctypes.POINTER(ctypes.c_void_p)],
            argnames = ["sid", "whichBuffer", "bufferNumber", "bufferAddr"] )
    #  Int32 imgPlot2(ctypes.c_void_p hwnd, ctypes.c_void_p buffer, uInt32 leftBufOffset, uInt32 topBufOffset, uInt32 xsize, uInt32 ysize, uInt32 xpos, uInt32 ypos, uInt32 flags)
    addfunc(lib, "imgPlot2", restype = Int32,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, uInt32, uInt32, uInt32, uInt32, uInt32, uInt32, uInt32],
            argnames = ["hwnd", "buffer", "leftBufOffset", "topBufOffset", "xsize", "ysize", "xpos", "ypos", "flags"] )
    #  Int32 imgPlotDC2(ctypes.c_void_p hdc, ctypes.c_void_p buffer, uInt32 xbuffoff, uInt32 ybuffoff, uInt32 xsize, uInt32 ysize, uInt32 xscreen, uInt32 yscreen, uInt32 flags)
    addfunc(lib, "imgPlotDC2", restype = Int32,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, uInt32, uInt32, uInt32, uInt32, uInt32, uInt32, uInt32],
            argnames = ["hdc", "buffer", "xbuffoff", "ybuffoff", "xsize", "ysize", "xscreen", "yscreen", "flags"] )
    #  Int32 imgSetAttributeFromVoidPtr(uInt32 void_id, uInt32 attribute, ctypes.c_void_p valuePtr)
    addfunc(lib, "imgSetAttributeFromVoidPtr", restype = Int32,
            argtypes = [uInt32, uInt32, ctypes.c_void_p],
            argnames = ["void_id", "attribute", "valuePtr"] )


