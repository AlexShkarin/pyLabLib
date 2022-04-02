##########   This file is generated automatically based on pvcam.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class PARAM_TYPE(enum.IntEnum):
    TYPE_INT16                 = _int32(1)
    TYPE_INT32                 = _int32(2)
    TYPE_FLT64                 = _int32(4)
    TYPE_UNS8                  = _int32(5)
    TYPE_UNS16                 = _int32(6)
    TYPE_UNS32                 = _int32(7)
    TYPE_UNS64                 = _int32(8)
    TYPE_ENUM                  = _int32(9)
    TYPE_BOOLEAN               = _int32(11)
    TYPE_INT8                  = _int32(12)
    TYPE_CHAR_PTR              = _int32(13)
    TYPE_VOID_PTR              = _int32(14)
    TYPE_VOID_PTR_PTR          = _int32(15)
    TYPE_INT64                 = _int32(16)
    TYPE_SMART_STREAM_TYPE     = _int32(17)
    TYPE_SMART_STREAM_TYPE_PTR = _int32(18)
    TYPE_FLT32                 = _int32(19)
dPARAM_TYPE={a.name:a.value for a in PARAM_TYPE}
drPARAM_TYPE={a.value:a.name for a in PARAM_TYPE}


class PARAM(enum.IntEnum):
    PARAM_DD_INFO_LENGTH            = _int32(((0<<16) + (1<<24) + 1))
    PARAM_DD_VERSION                = _int32(((0<<16) + (6<<24) + 2))
    PARAM_DD_RETRIES                = _int32(((0<<16) + (6<<24) + 3))
    PARAM_DD_TIMEOUT                = _int32(((0<<16) + (6<<24) + 4))
    PARAM_DD_INFO                   = _int32(((0<<16) + (13<<24) + 5))
    PARAM_CAM_INTERFACE_TYPE        = _int32(((0<<16) + (9<<24) + 10))
    PARAM_CAM_INTERFACE_MODE        = _int32(((0<<16) + (9<<24) + 11))
    PARAM_ADC_OFFSET                = _int32(((2<<16) + (1<<24)     + 195))
    PARAM_CHIP_NAME                 = _int32(((2<<16) + (13<<24)  + 129))
    PARAM_SYSTEM_NAME               = _int32(((2<<16) + (13<<24)  + 130))
    PARAM_VENDOR_NAME               = _int32(((2<<16) + (13<<24)  + 131))
    PARAM_PRODUCT_NAME              = _int32(((2<<16) + (13<<24)  + 132))
    PARAM_CAMERA_PART_NUMBER        = _int32(((2<<16) + (13<<24)  + 133))
    PARAM_COOLING_MODE              = _int32(((2<<16) + (9<<24)      + 214))
    PARAM_PREAMP_DELAY              = _int32(((2<<16) + (6<<24)     + 502))
    PARAM_COLOR_MODE                = _int32(((2<<16) + (9<<24)      + 504))
    PARAM_MPP_CAPABLE               = _int32(((2<<16) + (9<<24)      + 224))
    PARAM_PREAMP_OFF_CONTROL        = _int32(((2<<16) + (7<<24)     + 507))
    PARAM_PREMASK                   = _int32(((2<<16) + (6<<24)     +  53))
    PARAM_PRESCAN                   = _int32(((2<<16) + (6<<24)     +  55))
    PARAM_POSTMASK                  = _int32(((2<<16) + (6<<24)     +  54))
    PARAM_POSTSCAN                  = _int32(((2<<16) + (6<<24)     +  56))
    PARAM_PIX_PAR_DIST              = _int32(((2<<16) + (6<<24)     + 500))
    PARAM_PIX_PAR_SIZE              = _int32(((2<<16) + (6<<24)     +  63))
    PARAM_PIX_SER_DIST              = _int32(((2<<16) + (6<<24)     + 501))
    PARAM_PIX_SER_SIZE              = _int32(((2<<16) + (6<<24)     +  62))
    PARAM_SUMMING_WELL              = _int32(((2<<16) + (11<<24)   + 505))
    PARAM_FWELL_CAPACITY            = _int32(((2<<16) + (7<<24)     + 506))
    PARAM_PAR_SIZE                  = _int32(((2<<16) + (6<<24)     +  57))
    PARAM_SER_SIZE                  = _int32(((2<<16) + (6<<24)     +  58))
    PARAM_ACCUM_CAPABLE             = _int32(((2<<16) + (11<<24)   + 538))
    PARAM_FLASH_DWNLD_CAPABLE       = _int32(((2<<16) + (11<<24)   + 539))
    PARAM_READOUT_TIME              = _int32(((2<<16) + (4<<24)     + 179))
    PARAM_CLEARING_TIME             = _int32(((2<<16) + (16<<24)     + 180))
    PARAM_POST_TRIGGER_DELAY        = _int32(((2<<16) + (16<<24)     + 181))
    PARAM_PRE_TRIGGER_DELAY         = _int32(((2<<16) + (16<<24)     + 182))
    PARAM_CLEAR_CYCLES              = _int32(((2<<16) + (6<<24)     +  97))
    PARAM_CLEAR_MODE                = _int32(((2<<16) + (9<<24)      + 523))
    PARAM_FRAME_CAPABLE             = _int32(((2<<16) + (11<<24)   + 509))
    PARAM_PMODE                     = _int32(((2<<16) + (9 <<24)     + 524))
    PARAM_TEMP                      = _int32(((2<<16) + (1<<24)     + 525))
    PARAM_TEMP_SETPOINT             = _int32(((2<<16) + (1<<24)     + 526))
    PARAM_CAM_FW_VERSION            = _int32(((2<<16) + (6<<24)     + 532))
    PARAM_HEAD_SER_NUM_ALPHA        = _int32(((2<<16) + (13<<24)  + 533))
    PARAM_PCI_FW_VERSION            = _int32(((2<<16) + (6<<24)     + 534))
    PARAM_FAN_SPEED_SETPOINT        = _int32(((2<<16) + (9<<24)      + 710))
    PARAM_CAM_SYSTEMS_INFO          = _int32(((2<<16) + (13<<24)  + 536))
    PARAM_EXPOSURE_MODE             = _int32(((2<<16) + (9<<24)      + 535))
    PARAM_EXPOSE_OUT_MODE           = _int32(((2<<16) + (9<<24)      + 560))
    PARAM_BIT_DEPTH                 = _int32(((2<<16) + (1<<24)     + 511))
    PARAM_IMAGE_FORMAT              = _int32(((2<<16) + (9<<24)      + 248))
    PARAM_IMAGE_COMPRESSION         = _int32(((2<<16) + (9<<24)      + 249))
    PARAM_SCAN_MODE                 = _int32(((3<<16) + (9<<24)      + 250))
    PARAM_SCAN_DIRECTION            = _int32(((3<<16) + (9<<24)      + 251))
    PARAM_SCAN_DIRECTION_RESET      = _int32(((3<<16) + (11<<24)      + 252))
    PARAM_SCAN_LINE_DELAY           = _int32(((3<<16) + (6<<24)      + 253))
    PARAM_SCAN_LINE_TIME            = _int32(((3<<16) + (16<<24)      + 254))
    PARAM_SCAN_WIDTH                = _int32(((3<<16) + (6<<24)      + 255))
    PARAM_FRAME_ROTATE              = _int32(((2<<16) + (9<<24)      + 256))
    PARAM_FRAME_FLIP                = _int32(((2<<16) + (9<<24)      + 257))
    PARAM_GAIN_INDEX                = _int32(((2<<16) + (1<<24)     + 512))
    PARAM_SPDTAB_INDEX              = _int32(((2<<16) + (1<<24)     + 513))
    PARAM_GAIN_NAME                 = _int32(((2<<16) + (13<<24)  + 514))
    PARAM_READOUT_PORT              = _int32(((2<<16) + (9<<24)      + 247))
    PARAM_PIX_TIME                  = _int32(((2<<16) + (6<<24)     + 516))
    PARAM_SHTR_CLOSE_DELAY          = _int32(((2<<16) + (6<<24)     + 519))
    PARAM_SHTR_OPEN_DELAY           = _int32(((2<<16) + (6<<24)     + 520))
    PARAM_SHTR_OPEN_MODE            = _int32(((2<<16) + (9 <<24)     + 521))
    PARAM_SHTR_STATUS               = _int32(((2<<16) + (9 <<24)     + 522))
    PARAM_IO_ADDR                   = _int32(((2<<16) + (6<<24)     + 527))
    PARAM_IO_TYPE                   = _int32(((2<<16) + (9<<24)      + 528))
    PARAM_IO_DIRECTION              = _int32(((2<<16) + (9<<24)      + 529))
    PARAM_IO_STATE                  = _int32(((2<<16) + (4<<24)     + 530))
    PARAM_IO_BITDEPTH               = _int32(((2<<16) + (6<<24)     + 531))
    PARAM_GAIN_MULT_FACTOR          = _int32(((2<<16) + (6<<24)     + 537))
    PARAM_GAIN_MULT_ENABLE          = _int32(((2<<16) + (11<<24)   + 541))
    PARAM_PP_FEAT_NAME              = _int32(((2<<16) + (13<<24) +  542))
    PARAM_PP_INDEX                  = _int32(((2<<16) + (1<<24)    +  543))
    PARAM_ACTUAL_GAIN               = _int32(((2<<16) + (6<<24)     + 544))
    PARAM_PP_PARAM_INDEX            = _int32(((2<<16) + (1<<24)    +  545))
    PARAM_PP_PARAM_NAME             = _int32(((2<<16) + (13<<24) +  546))
    PARAM_PP_PARAM                  = _int32(((2<<16) + (7<<24)    +  547))
    PARAM_READ_NOISE                = _int32(((2<<16) + (6<<24)     + 548))
    PARAM_PP_FEAT_ID                = _int32(((2<<16) + (6<<24)    +  549))
    PARAM_PP_PARAM_ID               = _int32(((2<<16) + (6<<24)    +  550))
    PARAM_SMART_STREAM_MODE_ENABLED = _int32(((2<<16) + (11<<24)  +  700))
    PARAM_SMART_STREAM_MODE         = _int32(((2<<16) + (6<<24)    +  701))
    PARAM_SMART_STREAM_EXP_PARAMS   = _int32(((2<<16) + (14<<24) +  702))
    PARAM_SMART_STREAM_DLY_PARAMS   = _int32(((2<<16) + (14<<24) +  703))
    PARAM_EXP_TIME                  = _int32(((3<<16) + (6<<24)     +   1))
    PARAM_EXP_RES                   = _int32(((3<<16) + (9<<24)      +   2))
    PARAM_EXP_RES_INDEX             = _int32(((3<<16) + (6<<24)     +   4))
    PARAM_EXPOSURE_TIME             = _int32(((3<<16) + (8<<24)     +   8))
    PARAM_BOF_EOF_ENABLE            = _int32(((3<<16) + (9<<24)      +   5))
    PARAM_BOF_EOF_COUNT             = _int32(((3<<16) + (7<<24)     +   6))
    PARAM_BOF_EOF_CLR               = _int32(((3<<16) + (11<<24)   +   7))
    PARAM_CIRC_BUFFER               = _int32(((3<<16) + (11<<24)   + 299))
    PARAM_FRAME_BUFFER_SIZE         = _int32(((3<<16) + (8<<24)     + 300))
    PARAM_BINNING_SER               = _int32(((3<<16) + (9<<24)      + 165))
    PARAM_BINNING_PAR               = _int32(((3<<16) + (9<<24)      + 166))
    PARAM_METADATA_ENABLED          = _int32(((3<<16) + (11<<24)   + 168))
    PARAM_ROI_COUNT                 = _int32(((3<<16) + (6  <<24)   + 169))
    PARAM_CENTROIDS_ENABLED         = _int32(((3<<16) + (11<<24)   + 170))
    PARAM_CENTROIDS_RADIUS          = _int32(((3<<16) + (6  <<24)   + 171))
    PARAM_CENTROIDS_COUNT           = _int32(((3<<16) + (6  <<24)   + 172))
    PARAM_CENTROIDS_MODE            = _int32(((3<<16) + (9   <<24)   + 173))
    PARAM_CENTROIDS_BG_COUNT        = _int32(((3<<16) + (9   <<24)   + 174))
    PARAM_CENTROIDS_THRESHOLD       = _int32(((3<<16) + (7  <<24)   + 175))
    PARAM_TRIGTAB_SIGNAL            = _int32(((3<<16) + (9<<24)      + 180))
    PARAM_LAST_MUXED_SIGNAL         = _int32(((3<<16) + (5<<24)      + 181))
    PARAM_FRAME_DELIVERY_MODE       = _int32(((3<<16) + (9 <<24)     + 400))
dPARAM={a.name:a.value for a in PARAM}
drPARAM={a.value:a.name for a in PARAM}





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
HWND=ctypes.c_void_p
HGLOBAL=ctypes.c_void_p
HINSTANCE=ctypes.c_void_p
HDC=ctypes.c_void_p
HMODULE=ctypes.c_void_p
HKEY=ctypes.c_void_p
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


rs_bool=ctypes.c_ushort
int8=ctypes.c_byte
uns8=ctypes.c_ubyte
int16=ctypes.c_short
uns16=ctypes.c_ushort
int32=ctypes.c_int
uns32=ctypes.c_uint
flt32=ctypes.c_float
flt64=ctypes.c_double
ulong64=ctypes.c_ulonglong
long64=ctypes.c_longlong
void_ptr=ctypes.c_void_p
void_ptr_ptr=ctypes.POINTER(ctypes.c_void_p)
rs_bool_ptr=ctypes.POINTER(rs_bool)
char_ptr=ctypes.c_char_p
int8_ptr=ctypes.POINTER(int8)
uns8_ptr=ctypes.POINTER(uns8)
int16_ptr=ctypes.POINTER(int16)
uns16_ptr=ctypes.POINTER(uns16)
int32_ptr=ctypes.POINTER(int32)
uns32_ptr=ctypes.POINTER(uns32)
flt32_ptr=ctypes.POINTER(flt32)
flt64_ptr=ctypes.POINTER(flt64)
ulong64_ptr=ctypes.POINTER(ulong64)
long64_ptr=ctypes.POINTER(long64)
rs_bool_const_ptr=ctypes.POINTER(rs_bool)
char_const_ptr=ctypes.c_char_p
int8_const_ptr=ctypes.POINTER(int8)
uns8_const_ptr=ctypes.POINTER(uns8)
int16_const_ptr=ctypes.POINTER(int16)
uns16_const_ptr=ctypes.POINTER(uns16)
int32_const_ptr=ctypes.POINTER(int32)
uns32_const_ptr=ctypes.POINTER(uns32)
flt32_const_ptr=ctypes.POINTER(flt32)
flt64_const_ptr=ctypes.POINTER(flt64)
ulong64_const_ptr=ctypes.POINTER(ulong64)
long64_const_ptr=ctypes.POINTER(long64)
class PVCAM_FRAME_INFO_GUID(ctypes.Structure):
    _fields_=[  ("f1",uns32),
                ("f2",uns16),
                ("f3",uns16),
                ("f4",uns8*8) ]
PPVCAM_FRAME_INFO_GUID=ctypes.POINTER(PVCAM_FRAME_INFO_GUID)
class CPVCAM_FRAME_INFO_GUID(ctypes_wrap.CStructWrapper):
    _struct=PVCAM_FRAME_INFO_GUID


class FRAME_INFO(ctypes.Structure):
    _fields_=[  ("FrameInfoGUID",PVCAM_FRAME_INFO_GUID),
                ("hCam",int16),
                ("FrameNr",int32),
                ("TimeStamp",long64),
                ("ReadoutTime",int32),
                ("TimeStampBOF",long64) ]
PFRAME_INFO=ctypes.POINTER(FRAME_INFO)
class CFRAME_INFO(ctypes_wrap.CStructWrapper):
    _struct=FRAME_INFO


class PL_OPEN_MODES(enum.IntEnum):
    OPEN_EXCLUSIVE=_int32(0)
dPL_OPEN_MODES={a.name:a.value for a in PL_OPEN_MODES}
drPL_OPEN_MODES={a.value:a.name for a in PL_OPEN_MODES}


class PL_COOL_MODES(enum.IntEnum):
    NORMAL_COOL=_int32(0)
    CRYO_COOL  =enum.auto()
    NO_COOL    =enum.auto()
dPL_COOL_MODES={a.name:a.value for a in PL_COOL_MODES}
drPL_COOL_MODES={a.value:a.name for a in PL_COOL_MODES}


class PL_MPP_MODES(enum.IntEnum):
    MPP_UNKNOWN   =_int32(0)
    MPP_ALWAYS_OFF=enum.auto()
    MPP_ALWAYS_ON =enum.auto()
    MPP_SELECTABLE=enum.auto()
dPL_MPP_MODES={a.name:a.value for a in PL_MPP_MODES}
drPL_MPP_MODES={a.value:a.name for a in PL_MPP_MODES}


class PL_SHTR_MODES(enum.IntEnum):
    SHTR_FAULT  =_int32(0)
    SHTR_OPENING=enum.auto()
    SHTR_OPEN   =enum.auto()
    SHTR_CLOSING=enum.auto()
    SHTR_CLOSED =enum.auto()
    SHTR_UNKNOWN=enum.auto()
dPL_SHTR_MODES={a.name:a.value for a in PL_SHTR_MODES}
drPL_SHTR_MODES={a.value:a.name for a in PL_SHTR_MODES}


class PL_PMODES(enum.IntEnum):
    PMODE_NORMAL    =_int32(0)
    PMODE_FT        =enum.auto()
    PMODE_MPP       =enum.auto()
    PMODE_FT_MPP    =enum.auto()
    PMODE_ALT_NORMAL=enum.auto()
    PMODE_ALT_FT    =enum.auto()
    PMODE_ALT_MPP   =enum.auto()
    PMODE_ALT_FT_MPP=enum.auto()
dPL_PMODES={a.name:a.value for a in PL_PMODES}
drPL_PMODES={a.value:a.name for a in PL_PMODES}


class PL_COLOR_MODES(enum.IntEnum):
    COLOR_NONE    =_int32(0)
    COLOR_RESERVED=_int32(1)
    COLOR_RGGB    =_int32(2)
    COLOR_GRBG    =enum.auto()
    COLOR_GBRG    =enum.auto()
    COLOR_BGGR    =enum.auto()
dPL_COLOR_MODES={a.name:a.value for a in PL_COLOR_MODES}
drPL_COLOR_MODES={a.value:a.name for a in PL_COLOR_MODES}


class PL_IMAGE_FORMATS(enum.IntEnum):
    PL_IMAGE_FORMAT_MONO16 =_int32(0)
    PL_IMAGE_FORMAT_BAYER16=enum.auto()
    PL_IMAGE_FORMAT_MONO8  =enum.auto()
    PL_IMAGE_FORMAT_BAYER8 =enum.auto()
    PL_IMAGE_FORMAT_MONO24 =enum.auto()
    PL_IMAGE_FORMAT_BAYER24=enum.auto()
    PL_IMAGE_FORMAT_RGB24  =enum.auto()
    PL_IMAGE_FORMAT_RGB48  =enum.auto()
    PL_IMAGE_FORMAT_RGB72  =enum.auto()
    PL_IMAGE_FORMAT_MONO32 =enum.auto()
    PL_IMAGE_FORMAT_BAYER32=enum.auto()
dPL_IMAGE_FORMATS={a.name:a.value for a in PL_IMAGE_FORMATS}
drPL_IMAGE_FORMATS={a.value:a.name for a in PL_IMAGE_FORMATS}


class PL_IMAGE_COMPRESSIONS(enum.IntEnum):
    PL_IMAGE_COMPRESSION_NONE      =_int32(0)
    PL_IMAGE_COMPRESSION_RESERVED8 =_int32(8)
    PL_IMAGE_COMPRESSION_BITPACK9  =enum.auto()
    PL_IMAGE_COMPRESSION_BITPACK10 =enum.auto()
    PL_IMAGE_COMPRESSION_BITPACK11 =enum.auto()
    PL_IMAGE_COMPRESSION_BITPACK12 =enum.auto()
    PL_IMAGE_COMPRESSION_BITPACK13 =enum.auto()
    PL_IMAGE_COMPRESSION_BITPACK14 =enum.auto()
    PL_IMAGE_COMPRESSION_BITPACK15 =enum.auto()
    PL_IMAGE_COMPRESSION_RESERVED16=_int32(16)
    PL_IMAGE_COMPRESSION_BITPACK17 =enum.auto()
    PL_IMAGE_COMPRESSION_BITPACK18 =enum.auto()
    PL_IMAGE_COMPRESSION_RESERVED24=_int32(24)
    PL_IMAGE_COMPRESSION_RESERVED32=_int32(32)
dPL_IMAGE_COMPRESSIONS={a.name:a.value for a in PL_IMAGE_COMPRESSIONS}
drPL_IMAGE_COMPRESSIONS={a.value:a.name for a in PL_IMAGE_COMPRESSIONS}


class PL_FRAME_ROTATE_MODES(enum.IntEnum):
    PL_FRAME_ROTATE_MODE_NONE =_int32(0)
    PL_FRAME_ROTATE_MODE_90CW =enum.auto()
    PL_FRAME_ROTATE_MODE_180CW=enum.auto()
    PL_FRAME_ROTATE_MODE_270CW=enum.auto()
dPL_FRAME_ROTATE_MODES={a.name:a.value for a in PL_FRAME_ROTATE_MODES}
drPL_FRAME_ROTATE_MODES={a.value:a.name for a in PL_FRAME_ROTATE_MODES}


class PL_FRAME_FLIP_MODES(enum.IntEnum):
    PL_FRAME_FLIP_MODE_NONE=_int32(0)
    PL_FRAME_FLIP_MODE_X   =enum.auto()
    PL_FRAME_FLIP_MODE_Y   =enum.auto()
    PL_FRAME_FLIP_MODE_XY  =enum.auto()
dPL_FRAME_FLIP_MODES={a.name:a.value for a in PL_FRAME_FLIP_MODES}
drPL_FRAME_FLIP_MODES={a.value:a.name for a in PL_FRAME_FLIP_MODES}


class PL_PARAM_ATTRIBUTES(enum.IntEnum):
    ATTR_CURRENT  =_int32(0)
    ATTR_COUNT    =enum.auto()
    ATTR_TYPE     =enum.auto()
    ATTR_MIN      =enum.auto()
    ATTR_MAX      =enum.auto()
    ATTR_DEFAULT  =enum.auto()
    ATTR_INCREMENT=enum.auto()
    ATTR_ACCESS   =enum.auto()
    ATTR_AVAIL    =enum.auto()
dPL_PARAM_ATTRIBUTES={a.name:a.value for a in PL_PARAM_ATTRIBUTES}
drPL_PARAM_ATTRIBUTES={a.value:a.name for a in PL_PARAM_ATTRIBUTES}


class PL_PARAM_ACCESS(enum.IntEnum):
    ACC_READ_ONLY       =_int32(1)
    ACC_READ_WRITE      =enum.auto()
    ACC_EXIST_CHECK_ONLY=enum.auto()
    ACC_WRITE_ONLY      =enum.auto()
dPL_PARAM_ACCESS={a.name:a.value for a in PL_PARAM_ACCESS}
drPL_PARAM_ACCESS={a.value:a.name for a in PL_PARAM_ACCESS}


class PL_IO_TYPE(enum.IntEnum):
    IO_TYPE_TTL=_int32(0)
    IO_TYPE_DAC=enum.auto()
dPL_IO_TYPE={a.name:a.value for a in PL_IO_TYPE}
drPL_IO_TYPE={a.value:a.name for a in PL_IO_TYPE}


class PL_IO_DIRECTION(enum.IntEnum):
    IO_DIR_INPUT       =_int32(0)
    IO_DIR_OUTPUT      =enum.auto()
    IO_DIR_INPUT_OUTPUT=enum.auto()
dPL_IO_DIRECTION={a.name:a.value for a in PL_IO_DIRECTION}
drPL_IO_DIRECTION={a.value:a.name for a in PL_IO_DIRECTION}


class PL_READOUT_PORTS(enum.IntEnum):
    READOUT_PORT_0=_int32(0)
    READOUT_PORT_1=enum.auto()
dPL_READOUT_PORTS={a.name:a.value for a in PL_READOUT_PORTS}
drPL_READOUT_PORTS={a.value:a.name for a in PL_READOUT_PORTS}


class PL_CLEAR_MODES(enum.IntEnum):
    CLEAR_NEVER                =_int32(0)
    CLEAR_AUTO                 =_int32(CLEAR_NEVER)
    CLEAR_PRE_EXPOSURE         =enum.auto()
    CLEAR_PRE_SEQUENCE         =enum.auto()
    CLEAR_POST_SEQUENCE        =enum.auto()
    CLEAR_PRE_POST_SEQUENCE    =enum.auto()
    CLEAR_PRE_EXPOSURE_POST_SEQ=enum.auto()
    MAX_CLEAR_MODE             =enum.auto()
dPL_CLEAR_MODES={a.name:a.value for a in PL_CLEAR_MODES}
drPL_CLEAR_MODES={a.value:a.name for a in PL_CLEAR_MODES}


class PL_SHTR_OPEN_MODES(enum.IntEnum):
    OPEN_NEVER       =_int32(0)
    OPEN_PRE_EXPOSURE=enum.auto()
    OPEN_PRE_SEQUENCE=enum.auto()
    OPEN_PRE_TRIGGER =enum.auto()
    OPEN_NO_CHANGE   =enum.auto()
dPL_SHTR_OPEN_MODES={a.name:a.value for a in PL_SHTR_OPEN_MODES}
drPL_SHTR_OPEN_MODES={a.value:a.name for a in PL_SHTR_OPEN_MODES}


class PL_EXPOSURE_MODES(enum.IntEnum):
    TIMED_MODE             =_int32(0)
    STROBED_MODE           =enum.auto()
    BULB_MODE              =enum.auto()
    TRIGGER_FIRST_MODE     =enum.auto()
    FLASH_MODE             =enum.auto()
    VARIABLE_TIMED_MODE    =enum.auto()
    INT_STROBE_MODE        =enum.auto()
    MAX_EXPOSE_MODE        =_int32(7)
    EXT_TRIG_INTERNAL      =_int32(((7+0)<<8))
    EXT_TRIG_TRIG_FIRST    =_int32(((7+1)<<8))
    EXT_TRIG_EDGE_RISING   =_int32(((7+2)<<8))
    EXT_TRIG_LEVEL         =_int32(((7+3)<<8))
    EXT_TRIG_SOFTWARE_FIRST=_int32(((7+4)<<8))
    EXT_TRIG_SOFTWARE_EDGE =_int32(((7+5)<<8))
    EXT_TRIG_LEVEL_OVERLAP =_int32(((7+6)<<8))
    EXT_TRIG_LEVEL_PULSED  =_int32(((7+7)<<8))
dPL_EXPOSURE_MODES={a.name:a.value for a in PL_EXPOSURE_MODES}
drPL_EXPOSURE_MODES={a.value:a.name for a in PL_EXPOSURE_MODES}


class PL_SW_TRIG_STATUSES(enum.IntEnum):
    PL_SW_TRIG_STATUS_TRIGGERED=_int32(0)
    PL_SW_TRIG_STATUS_IGNORED  =enum.auto()
dPL_SW_TRIG_STATUSES={a.name:a.value for a in PL_SW_TRIG_STATUSES}
drPL_SW_TRIG_STATUSES={a.value:a.name for a in PL_SW_TRIG_STATUSES}


class PL_EXPOSE_OUT_MODES(enum.IntEnum):
    EXPOSE_OUT_FIRST_ROW      =_int32(0)
    EXPOSE_OUT_ALL_ROWS       =enum.auto()
    EXPOSE_OUT_ANY_ROW        =enum.auto()
    EXPOSE_OUT_ROLLING_SHUTTER=enum.auto()
    EXPOSE_OUT_LINE_TRIGGER   =enum.auto()
    EXPOSE_OUT_GLOBAL_SHUTTER =enum.auto()
    MAX_EXPOSE_OUT_MODE       =enum.auto()
dPL_EXPOSE_OUT_MODES={a.name:a.value for a in PL_EXPOSE_OUT_MODES}
drPL_EXPOSE_OUT_MODES={a.value:a.name for a in PL_EXPOSE_OUT_MODES}


class PL_FAN_SPEEDS(enum.IntEnum):
    FAN_SPEED_HIGH  =_int32(0)
    FAN_SPEED_MEDIUM=enum.auto()
    FAN_SPEED_LOW   =enum.auto()
    FAN_SPEED_OFF   =enum.auto()
dPL_FAN_SPEEDS={a.name:a.value for a in PL_FAN_SPEEDS}
drPL_FAN_SPEEDS={a.value:a.name for a in PL_FAN_SPEEDS}


class PL_TRIGTAB_SIGNALS(enum.IntEnum):
    PL_TRIGTAB_SIGNAL_EXPOSE_OUT=_int32(0)
dPL_TRIGTAB_SIGNALS={a.name:a.value for a in PL_TRIGTAB_SIGNALS}
drPL_TRIGTAB_SIGNALS={a.value:a.name for a in PL_TRIGTAB_SIGNALS}


class PL_FRAME_DELIVERY_MODES(enum.IntEnum):
    PL_FRAME_DELIVERY_MODE_MAX_FPS           =_int32(0)
    PL_FRAME_DELIVERY_MODE_CONSTANT_INTERVALS=enum.auto()
dPL_FRAME_DELIVERY_MODES={a.name:a.value for a in PL_FRAME_DELIVERY_MODES}
drPL_FRAME_DELIVERY_MODES={a.value:a.name for a in PL_FRAME_DELIVERY_MODES}


class PL_CAM_INTERFACE_TYPES(enum.IntEnum):
    PL_CAM_IFC_TYPE_UNKNOWN  =_int32(0)
    PL_CAM_IFC_TYPE_1394     =_int32(0x100)
    PL_CAM_IFC_TYPE_1394_A   =enum.auto()
    PL_CAM_IFC_TYPE_1394_B   =enum.auto()
    PL_CAM_IFC_TYPE_USB      =_int32(0x200)
    PL_CAM_IFC_TYPE_USB_1_1  =enum.auto()
    PL_CAM_IFC_TYPE_USB_2_0  =enum.auto()
    PL_CAM_IFC_TYPE_USB_3_0  =enum.auto()
    PL_CAM_IFC_TYPE_USB_3_1  =enum.auto()
    PL_CAM_IFC_TYPE_PCI      =_int32(0x400)
    PL_CAM_IFC_TYPE_PCI_LVDS =enum.auto()
    PL_CAM_IFC_TYPE_PCIE     =_int32(0x800)
    PL_CAM_IFC_TYPE_PCIE_LVDS=enum.auto()
    PL_CAM_IFC_TYPE_PCIE_X1  =enum.auto()
    PL_CAM_IFC_TYPE_PCIE_X4  =enum.auto()
    PL_CAM_IFC_TYPE_PCIE_X8  =enum.auto()
    PL_CAM_IFC_TYPE_VIRTUAL  =_int32(0x1000)
    PL_CAM_IFC_TYPE_ETHERNET =_int32(0x2000)
dPL_CAM_INTERFACE_TYPES={a.name:a.value for a in PL_CAM_INTERFACE_TYPES}
drPL_CAM_INTERFACE_TYPES={a.value:a.name for a in PL_CAM_INTERFACE_TYPES}


class PL_CAM_INTERFACE_MODES(enum.IntEnum):
    PL_CAM_IFC_MODE_UNSUPPORTED =_int32(0)
    PL_CAM_IFC_MODE_CONTROL_ONLY=enum.auto()
    PL_CAM_IFC_MODE_IMAGING     =enum.auto()
dPL_CAM_INTERFACE_MODES={a.name:a.value for a in PL_CAM_INTERFACE_MODES}
drPL_CAM_INTERFACE_MODES={a.value:a.name for a in PL_CAM_INTERFACE_MODES}


class PL_CENTROIDS_MODES(enum.IntEnum):
    PL_CENTROIDS_MODE_LOCATE=_int32(0)
    PL_CENTROIDS_MODE_TRACK =enum.auto()
    PL_CENTROIDS_MODE_BLOB  =enum.auto()
dPL_CENTROIDS_MODES={a.name:a.value for a in PL_CENTROIDS_MODES}
drPL_CENTROIDS_MODES={a.value:a.name for a in PL_CENTROIDS_MODES}


class PL_SCAN_MODES(enum.IntEnum):
    PL_SCAN_MODE_AUTO                   =_int32(0)
    PL_SCAN_MODE_PROGRAMMABLE_LINE_DELAY=enum.auto()
    PL_SCAN_MODE_PROGRAMMABLE_SCAN_WIDTH=enum.auto()
dPL_SCAN_MODES={a.name:a.value for a in PL_SCAN_MODES}
drPL_SCAN_MODES={a.value:a.name for a in PL_SCAN_MODES}


class PL_SCAN_DIRECTIONS(enum.IntEnum):
    PL_SCAN_DIRECTION_DOWN   =_int32(0)
    PL_SCAN_DIRECTION_UP     =enum.auto()
    PL_SCAN_DIRECTION_DOWN_UP=enum.auto()
dPL_SCAN_DIRECTIONS={a.name:a.value for a in PL_SCAN_DIRECTIONS}
drPL_SCAN_DIRECTIONS={a.value:a.name for a in PL_SCAN_DIRECTIONS}


class PP_FEATURE_IDS(enum.IntEnum):
    PP_FEATURE_RING_FUNCTION                =_int32(0)
    PP_FEATURE_BIAS                         =enum.auto()
    PP_FEATURE_BERT                         =enum.auto()
    PP_FEATURE_QUANT_VIEW                   =enum.auto()
    PP_FEATURE_BLACK_LOCK                   =enum.auto()
    PP_FEATURE_TOP_LOCK                     =enum.auto()
    PP_FEATURE_VARI_BIT                     =enum.auto()
    PP_FEATURE_RESERVED                     =enum.auto()
    PP_FEATURE_DESPECKLE_BRIGHT_HIGH        =enum.auto()
    PP_FEATURE_DESPECKLE_DARK_LOW           =enum.auto()
    PP_FEATURE_DEFECTIVE_PIXEL_CORRECTION   =enum.auto()
    PP_FEATURE_DYNAMIC_DARK_FRAME_CORRECTION=enum.auto()
    PP_FEATURE_HIGH_DYNAMIC_RANGE           =enum.auto()
    PP_FEATURE_DESPECKLE_BRIGHT_LOW         =enum.auto()
    PP_FEATURE_DENOISING                    =enum.auto()
    PP_FEATURE_DESPECKLE_DARK_HIGH          =enum.auto()
    PP_FEATURE_ENHANCED_DYNAMIC_RANGE       =enum.auto()
    PP_FEATURE_FRAME_SUMMING                =enum.auto()
    PP_FEATURE_MAX                          =enum.auto()
dPP_FEATURE_IDS={a.name:a.value for a in PP_FEATURE_IDS}
drPP_FEATURE_IDS={a.value:a.name for a in PP_FEATURE_IDS}


class PP_PARAMETER_IDS(enum.IntEnum):
    PP_PARAMETER_RF_FUNCTION                         =_int32((PP_FEATURE_IDS.PP_FEATURE_RING_FUNCTION.value*10))
    PP_FEATURE_BIAS_ENABLED                          =_int32((PP_FEATURE_IDS.PP_FEATURE_BIAS.value*10))
    PP_FEATURE_BIAS_LEVEL                            =enum.auto()
    PP_FEATURE_BERT_ENABLED                          =_int32((PP_FEATURE_IDS.PP_FEATURE_BERT.value*10))
    PP_FEATURE_BERT_THRESHOLD                        =enum.auto()
    PP_FEATURE_QUANT_VIEW_ENABLED                    =_int32((PP_FEATURE_IDS.PP_FEATURE_QUANT_VIEW.value*10))
    PP_FEATURE_QUANT_VIEW_E                          =enum.auto()
    PP_FEATURE_BLACK_LOCK_ENABLED                    =_int32((PP_FEATURE_IDS.PP_FEATURE_BLACK_LOCK.value*10))
    PP_FEATURE_BLACK_LOCK_BLACK_CLIP                 =enum.auto()
    PP_FEATURE_TOP_LOCK_ENABLED                      =_int32((PP_FEATURE_IDS.PP_FEATURE_TOP_LOCK.value*10))
    PP_FEATURE_TOP_LOCK_WHITE_CLIP                   =enum.auto()
    PP_FEATURE_VARI_BIT_ENABLED                      =_int32((PP_FEATURE_IDS.PP_FEATURE_VARI_BIT.value*10))
    PP_FEATURE_VARI_BIT_BIT_DEPTH                    =enum.auto()
    PP_FEATURE_DESPECKLE_BRIGHT_HIGH_ENABLED         =_int32((PP_FEATURE_IDS.PP_FEATURE_DESPECKLE_BRIGHT_HIGH.value*10))
    PP_FEATURE_DESPECKLE_BRIGHT_HIGH_THRESHOLD       =enum.auto()
    PP_FEATURE_DESPECKLE_BRIGHT_HIGH_MIN_ADU_AFFECTED=enum.auto()
    PP_FEATURE_DESPECKLE_DARK_LOW_ENABLED            =_int32((PP_FEATURE_IDS.PP_FEATURE_DESPECKLE_DARK_LOW.value*10))
    PP_FEATURE_DESPECKLE_DARK_LOW_THRESHOLD          =enum.auto()
    PP_FEATURE_DESPECKLE_DARK_LOW_MAX_ADU_AFFECTED   =enum.auto()
    PP_FEATURE_DEFECTIVE_PIXEL_CORRECTION_ENABLED    =_int32((PP_FEATURE_IDS.PP_FEATURE_DEFECTIVE_PIXEL_CORRECTION.value*10))
    PP_FEATURE_DYNAMIC_DARK_FRAME_CORRECTION_ENABLED =_int32((PP_FEATURE_IDS.PP_FEATURE_DYNAMIC_DARK_FRAME_CORRECTION.value*10))
    PP_FEATURE_HIGH_DYNAMIC_RANGE_ENABLED            =_int32((PP_FEATURE_IDS.PP_FEATURE_HIGH_DYNAMIC_RANGE.value*10))
    PP_FEATURE_DESPECKLE_BRIGHT_LOW_ENABLED          =_int32((PP_FEATURE_IDS.PP_FEATURE_DESPECKLE_BRIGHT_LOW.value*10))
    PP_FEATURE_DESPECKLE_BRIGHT_LOW_THRESHOLD        =enum.auto()
    PP_FEATURE_DESPECKLE_BRIGHT_LOW_MAX_ADU_AFFECTED =enum.auto()
    PP_FEATURE_DENOISING_ENABLED                     =_int32((PP_FEATURE_IDS.PP_FEATURE_DENOISING.value*10))
    PP_FEATURE_DENOISING_NO_OF_ITERATIONS            =enum.auto()
    PP_FEATURE_DENOISING_GAIN                        =enum.auto()
    PP_FEATURE_DENOISING_OFFSET                      =enum.auto()
    PP_FEATURE_DENOISING_LAMBDA                      =enum.auto()
    PP_FEATURE_DESPECKLE_DARK_HIGH_ENABLED           =_int32((PP_FEATURE_IDS.PP_FEATURE_DESPECKLE_DARK_HIGH.value*10))
    PP_FEATURE_DESPECKLE_DARK_HIGH_THRESHOLD         =enum.auto()
    PP_FEATURE_DESPECKLE_DARK_HIGH_MIN_ADU_AFFECTED  =enum.auto()
    PP_FEATURE_ENHANCED_DYNAMIC_RANGE_ENABLED        =_int32((PP_FEATURE_IDS.PP_FEATURE_ENHANCED_DYNAMIC_RANGE.value*10))
    PP_FEATURE_FRAME_SUMMING_ENABLED                 =_int32((PP_FEATURE_IDS.PP_FEATURE_FRAME_SUMMING.value*10))
    PP_FEATURE_FRAME_SUMMING_COUNT                   =enum.auto()
    PP_FEATURE_FRAME_SUMMING_32_BIT_MODE             =enum.auto()
    PP_PARAMETER_ID_MAX                              =enum.auto()
dPP_PARAMETER_IDS={a.name:a.value for a in PP_PARAMETER_IDS}
drPP_PARAMETER_IDS={a.value:a.name for a in PP_PARAMETER_IDS}


class smart_stream_type(ctypes.Structure):
    _fields_=[  ("entries",uns16),
                ("params",ctypes.POINTER(uns32)) ]
Psmart_stream_type=ctypes.POINTER(smart_stream_type)
class Csmart_stream_type(ctypes_wrap.CStructWrapper):
    _struct=smart_stream_type


class PL_SMT_MODES(enum.IntEnum):
    SMTMODE_ARBITRARY_ALL=_int32(0)
    SMTMODE_MAX          =enum.auto()
dPL_SMT_MODES={a.name:a.value for a in PL_SMT_MODES}
drPL_SMT_MODES={a.value:a.name for a in PL_SMT_MODES}


class PL_IMAGE_STATUSES(enum.IntEnum):
    READOUT_NOT_ACTIVE     =_int32(0)
    EXPOSURE_IN_PROGRESS   =enum.auto()
    READOUT_IN_PROGRESS    =enum.auto()
    READOUT_COMPLETE       =enum.auto()
    FRAME_AVAILABLE        =_int32(READOUT_COMPLETE)
    READOUT_FAILED         =enum.auto()
    ACQUISITION_IN_PROGRESS=enum.auto()
    MAX_CAMERA_STATUS      =enum.auto()
dPL_IMAGE_STATUSES={a.name:a.value for a in PL_IMAGE_STATUSES}
drPL_IMAGE_STATUSES={a.value:a.name for a in PL_IMAGE_STATUSES}


class PL_CCS_ABORT_MODES(enum.IntEnum):
    CCS_NO_CHANGE       =_int32(0)
    CCS_HALT            =enum.auto()
    CCS_HALT_CLOSE_SHTR =enum.auto()
    CCS_CLEAR           =enum.auto()
    CCS_CLEAR_CLOSE_SHTR=enum.auto()
    CCS_OPEN_SHTR       =enum.auto()
    CCS_CLEAR_OPEN_SHTR =enum.auto()
dPL_CCS_ABORT_MODES={a.name:a.value for a in PL_CCS_ABORT_MODES}
drPL_CCS_ABORT_MODES={a.value:a.name for a in PL_CCS_ABORT_MODES}


class PL_IRQ_MODES(enum.IntEnum):
    NO_FRAME_IRQS       =_int32(0)
    BEGIN_FRAME_IRQS    =enum.auto()
    END_FRAME_IRQS      =enum.auto()
    BEGIN_END_FRAME_IRQS=enum.auto()
dPL_IRQ_MODES={a.name:a.value for a in PL_IRQ_MODES}
drPL_IRQ_MODES={a.value:a.name for a in PL_IRQ_MODES}


class PL_CIRC_MODES(enum.IntEnum):
    CIRC_NONE        =_int32(0)
    CIRC_OVERWRITE   =enum.auto()
    CIRC_NO_OVERWRITE=enum.auto()
dPL_CIRC_MODES={a.name:a.value for a in PL_CIRC_MODES}
drPL_CIRC_MODES={a.value:a.name for a in PL_CIRC_MODES}


class PL_EXP_RES_MODES(enum.IntEnum):
    EXP_RES_ONE_MILLISEC=_int32(0)
    EXP_RES_ONE_MICROSEC=enum.auto()
    EXP_RES_ONE_SEC     =enum.auto()
dPL_EXP_RES_MODES={a.name:a.value for a in PL_EXP_RES_MODES}
drPL_EXP_RES_MODES={a.value:a.name for a in PL_EXP_RES_MODES}


class PL_SRC_MODES(enum.IntEnum):
    SCR_PRE_OPEN_SHTR  =_int32(0)
    SCR_POST_OPEN_SHTR =enum.auto()
    SCR_PRE_FLASH      =enum.auto()
    SCR_POST_FLASH     =enum.auto()
    SCR_PRE_INTEGRATE  =enum.auto()
    SCR_POST_INTEGRATE =enum.auto()
    SCR_PRE_READOUT    =enum.auto()
    SCR_POST_READOUT   =enum.auto()
    SCR_PRE_CLOSE_SHTR =enum.auto()
    SCR_POST_CLOSE_SHTR=enum.auto()
dPL_SRC_MODES={a.name:a.value for a in PL_SRC_MODES}
drPL_SRC_MODES={a.value:a.name for a in PL_SRC_MODES}


class PL_CALLBACK_EVENT(enum.IntEnum):
    PL_CALLBACK_BOF        =_int32(0)
    PL_CALLBACK_EOF        =enum.auto()
    PL_CALLBACK_CHECK_CAMS =enum.auto()
    PL_CALLBACK_CAM_REMOVED=enum.auto()
    PL_CALLBACK_CAM_RESUMED=enum.auto()
    PL_CALLBACK_MAX        =enum.auto()
dPL_CALLBACK_EVENT={a.name:a.value for a in PL_CALLBACK_EVENT}
drPL_CALLBACK_EVENT={a.value:a.name for a in PL_CALLBACK_EVENT}


class rgn_type(ctypes.Structure):
    _fields_=[  ("s1",uns16),
                ("s2",uns16),
                ("sbin",uns16),
                ("p1",uns16),
                ("p2",uns16),
                ("pbin",uns16) ]
Prgn_type=ctypes.POINTER(rgn_type)
class Crgn_type(ctypes_wrap.CStructWrapper):
    _struct=rgn_type


class io_entry(ctypes.Structure):
    _fields_=[  ("io_port",uns16),
                ("io_type",uns32),
                ("state",flt64),
                ("next",ctypes.c_void_p) ]
Pio_entry=ctypes.POINTER(io_entry)
class Cio_entry(ctypes_wrap.CStructWrapper):
    _struct=io_entry


class io_list(ctypes.Structure):
    _fields_=[  ("pre_open",io_entry),
                ("post_open",io_entry),
                ("pre_flash",io_entry),
                ("post_flash",io_entry),
                ("pre_integrate",io_entry),
                ("post_integrate",io_entry),
                ("pre_readout",io_entry),
                ("post_readout",io_entry),
                ("pre_close",io_entry),
                ("post_close",io_entry) ]
Pio_list=ctypes.POINTER(io_list)
class Cio_list(ctypes_wrap.CStructWrapper):
    _struct=io_list


class active_camera_type(ctypes.Structure):
    _fields_=[  ("shutter_close_delay",uns16),
                ("shutter_open_delay",uns16),
                ("rows",uns16),
                ("cols",uns16),
                ("prescan",uns16),
                ("postscan",uns16),
                ("premask",uns16),
                ("postmask",uns16),
                ("preflash",uns16),
                ("clear_count",uns16),
                ("preamp_delay",uns16),
                ("mpp_selectable",rs_bool),
                ("frame_selectable",rs_bool),
                ("do_clear",int16),
                ("open_shutter",int16),
                ("mpp_mode",rs_bool),
                ("frame_transfer",rs_bool),
                ("alt_mode",rs_bool),
                ("exp_res",uns32),
                ("io_hdr",ctypes.POINTER(io_list)) ]
Pactive_camera_type=ctypes.POINTER(active_camera_type)
class Cactive_camera_type(ctypes_wrap.CStructWrapper):
    _struct=active_camera_type


class PL_MD_FRAME_FLAGS(enum.IntEnum):
    PL_MD_FRAME_FLAG_ROI_TS_SUPPORTED=_int32(0x01)
    PL_MD_FRAME_FLAG_UNUSED_2        =_int32(0x02)
    PL_MD_FRAME_FLAG_UNUSED_3        =_int32(0x04)
    PL_MD_FRAME_FLAG_UNUSED_4        =_int32(0x10)
    PL_MD_FRAME_FLAG_UNUSED_5        =_int32(0x20)
    PL_MD_FRAME_FLAG_UNUSED_6        =_int32(0x40)
    PL_MD_FRAME_FLAG_UNUSED_7        =_int32(0x80)
dPL_MD_FRAME_FLAGS={a.name:a.value for a in PL_MD_FRAME_FLAGS}
drPL_MD_FRAME_FLAGS={a.value:a.name for a in PL_MD_FRAME_FLAGS}


class PL_MD_ROI_FLAGS(enum.IntEnum):
    PL_MD_ROI_FLAG_INVALID    =_int32(0x01)
    PL_MD_ROI_FLAG_HEADER_ONLY=_int32(0x02)
    PL_MD_ROI_FLAG_UNUSED_3   =_int32(0x04)
    PL_MD_ROI_FLAG_UNUSED_4   =_int32(0x10)
    PL_MD_ROI_FLAG_UNUSED_5   =_int32(0x20)
    PL_MD_ROI_FLAG_UNUSED_6   =_int32(0x40)
    PL_MD_ROI_FLAG_UNUSED_7   =_int32(0x80)
dPL_MD_ROI_FLAGS={a.name:a.value for a in PL_MD_ROI_FLAGS}
drPL_MD_ROI_FLAGS={a.value:a.name for a in PL_MD_ROI_FLAGS}


class md_frame_header(ctypes.Structure):
    _pack_=1
    _fields_=[  ("signature",uns32),
                ("version",uns8),
                ("frameNr",uns32),
                ("roiCount",uns16),
                ("timestampBOF",uns32),
                ("timestampEOF",uns32),
                ("timestampResNs",uns32),
                ("exposureTime",uns32),
                ("exposureTimeResNs",uns32),
                ("roiTimestampResNs",uns32),
                ("bitDepth",uns8),
                ("colorMask",uns8),
                ("flags",uns8),
                ("extendedMdSize",uns16),
                ("imageFormat",uns8),
                ("imageCompression",uns8),
                ("_reserved",uns8*6) ]
Pmd_frame_header=ctypes.POINTER(md_frame_header)
class Cmd_frame_header(ctypes_wrap.CStructWrapper):
    _struct=md_frame_header


class md_frame_header_v3(ctypes.Structure):
    _pack_=1
    _fields_=[  ("signature",uns32),
                ("version",uns8),
                ("frameNr",uns32),
                ("roiCount",uns16),
                ("timestampBOF",ulong64),
                ("timestampEOF",ulong64),
                ("exposureTime",ulong64),
                ("bitDepth",uns8),
                ("colorMask",uns8),
                ("flags",uns8),
                ("extendedMdSize",uns16),
                ("imageFormat",uns8),
                ("imageCompression",uns8),
                ("_reserved",uns8*6) ]
Pmd_frame_header_v3=ctypes.POINTER(md_frame_header_v3)
class Cmd_frame_header_v3(ctypes_wrap.CStructWrapper):
    _struct=md_frame_header_v3


class md_frame_roi_header(ctypes.Structure):
    _pack_=1
    _fields_=[  ("roiNr",uns16),
                ("timestampBOR",uns32),
                ("timestampEOR",uns32),
                ("roi",rgn_type),
                ("flags",uns8),
                ("extendedMdSize",uns16),
                ("roiDataSize",uns32),
                ("_reserved",uns8*3) ]
Pmd_frame_roi_header=ctypes.POINTER(md_frame_roi_header)
class Cmd_frame_roi_header(ctypes_wrap.CStructWrapper):
    _struct=md_frame_roi_header


class PL_MD_EXT_TAGS(enum.IntEnum):
    PL_MD_EXT_TAG_PARTICLE_ID=_int32(0)
    PL_MD_EXT_TAG_PARTICLE_M0=enum.auto()
    PL_MD_EXT_TAG_PARTICLE_M2=enum.auto()
    PL_MD_EXT_TAG_MAX        =enum.auto()
dPL_MD_EXT_TAGS={a.name:a.value for a in PL_MD_EXT_TAGS}
drPL_MD_EXT_TAGS={a.value:a.name for a in PL_MD_EXT_TAGS}


class md_ext_item_info(ctypes.Structure):
    _fields_=[  ("tag",ctypes.c_int),
                ("type",uns16),
                ("size",uns16),
                ("name",ctypes.c_char_p) ]
Pmd_ext_item_info=ctypes.POINTER(md_ext_item_info)
class Cmd_ext_item_info(ctypes_wrap.CStructWrapper):
    _struct=md_ext_item_info


class md_ext_item(ctypes.Structure):
    _fields_=[  ("tagInfo",ctypes.POINTER(md_ext_item_info)),
                ("value",ctypes.c_void_p) ]
Pmd_ext_item=ctypes.POINTER(md_ext_item)
class Cmd_ext_item(ctypes_wrap.CStructWrapper):
    _struct=md_ext_item


class md_ext_item_collection(ctypes.Structure):
    _fields_=[  ("list",md_ext_item*255),
                ("map",ctypes.POINTER(md_ext_item)*255),
                ("count",uns16) ]
Pmd_ext_item_collection=ctypes.POINTER(md_ext_item_collection)
class Cmd_ext_item_collection(ctypes_wrap.CStructWrapper):
    _struct=md_ext_item_collection


class md_frame_roi(ctypes.Structure):
    _fields_=[  ("header",ctypes.POINTER(md_frame_roi_header)),
                ("data",ctypes.c_void_p),
                ("dataSize",uns32),
                ("extMdData",ctypes.c_void_p),
                ("extMdDataSize",uns16) ]
Pmd_frame_roi=ctypes.POINTER(md_frame_roi)
class Cmd_frame_roi(ctypes_wrap.CStructWrapper):
    _struct=md_frame_roi


class md_frame(ctypes.Structure):
    _fields_=[  ("header",ctypes.POINTER(md_frame_header)),
                ("extMdData",ctypes.c_void_p),
                ("extMdDataSize",uns16),
                ("impliedRoi",rgn_type),
                ("roiArray",ctypes.POINTER(md_frame_roi)),
                ("roiCapacity",uns16),
                ("roiCount",uns16) ]
Pmd_frame=ctypes.POINTER(md_frame)
class Cmd_frame(ctypes_wrap.CStructWrapper):
    _struct=md_frame


PPVCAM_FRAME_INFO_GUID=ctypes.POINTER(PVCAM_FRAME_INFO_GUID)
PFRAME_INFO=ctypes.POINTER(FRAME_INFO)
smart_stream_type_ptr=ctypes.POINTER(smart_stream_type)
rgn_ptr=ctypes.POINTER(rgn_type)
rgn_const_ptr=ctypes.POINTER(rgn_type)
io_entry_ptr=ctypes.POINTER(io_entry)
io_list_ptr=ctypes.POINTER(io_list)
io_list_ptr_ptr=ctypes.POINTER(ctypes.POINTER(io_list))
active_camera_ptr=ctypes.POINTER(active_camera_type)
PL_CALLBACK_SIG_LEGACY=ctypes.c_void_p
PL_CALLBACK_SIG_EX=ctypes.c_void_p
PL_CALLBACK_SIG_EX2=ctypes.c_void_p
PL_CALLBACK_SIG_EX3=ctypes.c_void_p



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
    #  rs_bool pl_pvcam_get_ver(ctypes.POINTER(uns16) pvcam_version)
    addfunc(lib, "pl_pvcam_get_ver", restype = rs_bool,
            argtypes = [ctypes.POINTER(uns16)],
            argnames = ["pvcam_version"] )
    #  rs_bool pl_pvcam_init()
    addfunc(lib, "pl_pvcam_init", restype = rs_bool,
            argtypes = [],
            argnames = [] )
    #  rs_bool pl_pvcam_uninit()
    addfunc(lib, "pl_pvcam_uninit", restype = rs_bool,
            argtypes = [],
            argnames = [] )
    #  rs_bool pl_cam_check(int16 hcam)
    addfunc(lib, "pl_cam_check", restype = rs_bool,
            argtypes = [int16],
            argnames = ["hcam"] )
    #  rs_bool pl_cam_close(int16 hcam)
    addfunc(lib, "pl_cam_close", restype = rs_bool,
            argtypes = [int16],
            argnames = ["hcam"] )
    #  rs_bool pl_cam_get_name(int16 cam_num, ctypes.c_char_p camera_name)
    addfunc(lib, "pl_cam_get_name", restype = rs_bool,
            argtypes = [int16, ctypes.c_char_p],
            argnames = ["cam_num", "camera_name"] )
    #  rs_bool pl_cam_get_total(ctypes.POINTER(int16) totl_cams)
    addfunc(lib, "pl_cam_get_total", restype = rs_bool,
            argtypes = [ctypes.POINTER(int16)],
            argnames = ["totl_cams"] )
    #  rs_bool pl_cam_open(ctypes.c_char_p camera_name, ctypes.POINTER(int16) hcam, int16 o_mode)
    addfunc(lib, "pl_cam_open", restype = rs_bool,
            argtypes = [ctypes.c_char_p, ctypes.POINTER(int16), int16],
            argnames = ["camera_name", "hcam", "o_mode"] )
    #  rs_bool pl_cam_register_callback(int16 hcam, int32 callback_event, ctypes.c_void_p callback)
    addfunc(lib, "pl_cam_register_callback", restype = rs_bool,
            argtypes = [int16, int32, ctypes.c_void_p],
            argnames = ["hcam", "callback_event", "callback"] )
    #  rs_bool pl_cam_register_callback_ex(int16 hcam, int32 callback_event, ctypes.c_void_p callback, ctypes.c_void_p context)
    addfunc(lib, "pl_cam_register_callback_ex", restype = rs_bool,
            argtypes = [int16, int32, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["hcam", "callback_event", "callback", "context"] )
    #  rs_bool pl_cam_register_callback_ex2(int16 hcam, int32 callback_event, ctypes.c_void_p callback)
    addfunc(lib, "pl_cam_register_callback_ex2", restype = rs_bool,
            argtypes = [int16, int32, ctypes.c_void_p],
            argnames = ["hcam", "callback_event", "callback"] )
    #  rs_bool pl_cam_register_callback_ex3(int16 hcam, int32 callback_event, ctypes.c_void_p callback, ctypes.c_void_p context)
    addfunc(lib, "pl_cam_register_callback_ex3", restype = rs_bool,
            argtypes = [int16, int32, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["hcam", "callback_event", "callback", "context"] )
    #  rs_bool pl_cam_deregister_callback(int16 hcam, int32 callback_event)
    addfunc(lib, "pl_cam_deregister_callback", restype = rs_bool,
            argtypes = [int16, int32],
            argnames = ["hcam", "callback_event"] )
    #  int16 pl_error_code()
    addfunc(lib, "pl_error_code", restype = int16,
            argtypes = [],
            argnames = [] )
    #  rs_bool pl_error_message(int16 err_code, ctypes.c_char_p msg)
    addfunc(lib, "pl_error_message", restype = rs_bool,
            argtypes = [int16, ctypes.c_char_p],
            argnames = ["err_code", "msg"] )
    #  rs_bool pl_get_param(int16 hcam, uns32 param_id, int16 param_attribute, ctypes.c_void_p param_value)
    addfunc(lib, "pl_get_param", restype = rs_bool,
            argtypes = [int16, uns32, int16, ctypes.c_void_p],
            argnames = ["hcam", "param_id", "param_attribute", "param_value"] )
    #  rs_bool pl_set_param(int16 hcam, uns32 param_id, ctypes.c_void_p param_value)
    addfunc(lib, "pl_set_param", restype = rs_bool,
            argtypes = [int16, uns32, ctypes.c_void_p],
            argnames = ["hcam", "param_id", "param_value"] )
    #  rs_bool pl_get_enum_param(int16 hcam, uns32 param_id, uns32 index, ctypes.POINTER(int32) value, ctypes.c_char_p desc, uns32 length)
    addfunc(lib, "pl_get_enum_param", restype = rs_bool,
            argtypes = [int16, uns32, uns32, ctypes.POINTER(int32), ctypes.c_char_p, uns32],
            argnames = ["hcam", "param_id", "index", "value", "desc", "length"] )
    #  rs_bool pl_enum_str_length(int16 hcam, uns32 param_id, uns32 index, ctypes.POINTER(uns32) length)
    addfunc(lib, "pl_enum_str_length", restype = rs_bool,
            argtypes = [int16, uns32, uns32, ctypes.POINTER(uns32)],
            argnames = ["hcam", "param_id", "index", "length"] )
    #  rs_bool pl_pp_reset(int16 hcam)
    addfunc(lib, "pl_pp_reset", restype = rs_bool,
            argtypes = [int16],
            argnames = ["hcam"] )
    #  rs_bool pl_create_smart_stream_struct(ctypes.POINTER(ctypes.POINTER(smart_stream_type)) array, uns16 entries)
    addfunc(lib, "pl_create_smart_stream_struct", restype = rs_bool,
            argtypes = [ctypes.POINTER(ctypes.POINTER(smart_stream_type)), uns16],
            argnames = ["array", "entries"] )
    #  rs_bool pl_release_smart_stream_struct(ctypes.POINTER(ctypes.POINTER(smart_stream_type)) array)
    addfunc(lib, "pl_release_smart_stream_struct", restype = rs_bool,
            argtypes = [ctypes.POINTER(ctypes.POINTER(smart_stream_type))],
            argnames = ["array"] )
    #  rs_bool pl_create_frame_info_struct(ctypes.POINTER(ctypes.POINTER(FRAME_INFO)) new_frame)
    addfunc(lib, "pl_create_frame_info_struct", restype = rs_bool,
            argtypes = [ctypes.POINTER(ctypes.POINTER(FRAME_INFO))],
            argnames = ["new_frame"] )
    #  rs_bool pl_release_frame_info_struct(ctypes.POINTER(FRAME_INFO) frame_to_delete)
    addfunc(lib, "pl_release_frame_info_struct", restype = rs_bool,
            argtypes = [ctypes.POINTER(FRAME_INFO)],
            argnames = ["frame_to_delete"] )
    #  rs_bool pl_exp_setup_seq(int16 hcam, uns16 exp_total, uns16 rgn_total, ctypes.POINTER(rgn_type) rgn_array, int16 exp_mode, uns32 exposure_time, ctypes.POINTER(uns32) exp_bytes)
    addfunc(lib, "pl_exp_setup_seq", restype = rs_bool,
            argtypes = [int16, uns16, uns16, ctypes.POINTER(rgn_type), int16, uns32, ctypes.POINTER(uns32)],
            argnames = ["hcam", "exp_total", "rgn_total", "rgn_array", "exp_mode", "exposure_time", "exp_bytes"] )
    #  rs_bool pl_exp_start_seq(int16 hcam, ctypes.c_void_p pixel_stream)
    addfunc(lib, "pl_exp_start_seq", restype = rs_bool,
            argtypes = [int16, ctypes.c_void_p],
            argnames = ["hcam", "pixel_stream"] )
    #  rs_bool pl_exp_setup_cont(int16 hcam, uns16 rgn_total, ctypes.POINTER(rgn_type) rgn_array, int16 exp_mode, uns32 exposure_time, ctypes.POINTER(uns32) exp_bytes, int16 buffer_mode)
    addfunc(lib, "pl_exp_setup_cont", restype = rs_bool,
            argtypes = [int16, uns16, ctypes.POINTER(rgn_type), int16, uns32, ctypes.POINTER(uns32), int16],
            argnames = ["hcam", "rgn_total", "rgn_array", "exp_mode", "exposure_time", "exp_bytes", "buffer_mode"] )
    #  rs_bool pl_exp_start_cont(int16 hcam, ctypes.c_void_p pixel_stream, uns32 size)
    addfunc(lib, "pl_exp_start_cont", restype = rs_bool,
            argtypes = [int16, ctypes.c_void_p, uns32],
            argnames = ["hcam", "pixel_stream", "size"] )
    #  rs_bool pl_exp_trigger(int16 hcam, ctypes.POINTER(uns32) flags, uns32 value)
    addfunc(lib, "pl_exp_trigger", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns32), uns32],
            argnames = ["hcam", "flags", "value"] )
    #  rs_bool pl_exp_check_status(int16 hcam, ctypes.POINTER(int16) status, ctypes.POINTER(uns32) bytes_arrived)
    addfunc(lib, "pl_exp_check_status", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16), ctypes.POINTER(uns32)],
            argnames = ["hcam", "status", "bytes_arrived"] )
    #  rs_bool pl_exp_check_cont_status(int16 hcam, ctypes.POINTER(int16) status, ctypes.POINTER(uns32) bytes_arrived, ctypes.POINTER(uns32) buffer_cnt)
    addfunc(lib, "pl_exp_check_cont_status", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16), ctypes.POINTER(uns32), ctypes.POINTER(uns32)],
            argnames = ["hcam", "status", "bytes_arrived", "buffer_cnt"] )
    #  rs_bool pl_exp_check_cont_status_ex(int16 hcam, ctypes.POINTER(int16) status, ctypes.POINTER(uns32) byte_cnt, ctypes.POINTER(uns32) buffer_cnt, ctypes.POINTER(FRAME_INFO) frame_info)
    addfunc(lib, "pl_exp_check_cont_status_ex", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16), ctypes.POINTER(uns32), ctypes.POINTER(uns32), ctypes.POINTER(FRAME_INFO)],
            argnames = ["hcam", "status", "byte_cnt", "buffer_cnt", "frame_info"] )
    #  rs_bool pl_exp_get_latest_frame(int16 hcam, ctypes.POINTER(ctypes.c_void_p) frame)
    addfunc(lib, "pl_exp_get_latest_frame", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(ctypes.c_void_p)],
            argnames = ["hcam", "frame"] )
    #  rs_bool pl_exp_get_latest_frame_ex(int16 hcam, ctypes.POINTER(ctypes.c_void_p) frame, ctypes.POINTER(FRAME_INFO) frame_info)
    addfunc(lib, "pl_exp_get_latest_frame_ex", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(FRAME_INFO)],
            argnames = ["hcam", "frame", "frame_info"] )
    #  rs_bool pl_exp_get_oldest_frame(int16 hcam, ctypes.POINTER(ctypes.c_void_p) frame)
    addfunc(lib, "pl_exp_get_oldest_frame", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(ctypes.c_void_p)],
            argnames = ["hcam", "frame"] )
    #  rs_bool pl_exp_get_oldest_frame_ex(int16 hcam, ctypes.POINTER(ctypes.c_void_p) frame, ctypes.POINTER(FRAME_INFO) frame_info)
    addfunc(lib, "pl_exp_get_oldest_frame_ex", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(FRAME_INFO)],
            argnames = ["hcam", "frame", "frame_info"] )
    #  rs_bool pl_exp_unlock_oldest_frame(int16 hcam)
    addfunc(lib, "pl_exp_unlock_oldest_frame", restype = rs_bool,
            argtypes = [int16],
            argnames = ["hcam"] )
    #  rs_bool pl_exp_stop_cont(int16 hcam, int16 cam_state)
    addfunc(lib, "pl_exp_stop_cont", restype = rs_bool,
            argtypes = [int16, int16],
            argnames = ["hcam", "cam_state"] )
    #  rs_bool pl_exp_abort(int16 hcam, int16 cam_state)
    addfunc(lib, "pl_exp_abort", restype = rs_bool,
            argtypes = [int16, int16],
            argnames = ["hcam", "cam_state"] )
    #  rs_bool pl_exp_finish_seq(int16 hcam, ctypes.c_void_p pixel_stream, int16 hbuf)
    addfunc(lib, "pl_exp_finish_seq", restype = rs_bool,
            argtypes = [int16, ctypes.c_void_p, int16],
            argnames = ["hcam", "pixel_stream", "hbuf"] )
    #  rs_bool pl_io_script_control(int16 hcam, uns16 addr, flt64 state, uns32 location)
    addfunc(lib, "pl_io_script_control", restype = rs_bool,
            argtypes = [int16, uns16, flt64, uns32],
            argnames = ["hcam", "addr", "state", "location"] )
    #  rs_bool pl_io_clear_script_control(int16 hcam)
    addfunc(lib, "pl_io_clear_script_control", restype = rs_bool,
            argtypes = [int16],
            argnames = ["hcam"] )
    #  rs_bool pl_exp_init_seq()
    addfunc(lib, "pl_exp_init_seq", restype = rs_bool,
            argtypes = [],
            argnames = [] )
    #  rs_bool pl_exp_uninit_seq()
    addfunc(lib, "pl_exp_uninit_seq", restype = rs_bool,
            argtypes = [],
            argnames = [] )
    #  rs_bool pl_dd_get_info(int16 hcam, int16 bytes, ctypes.c_char_p text)
    addfunc(lib, "pl_dd_get_info", restype = rs_bool,
            argtypes = [int16, int16, ctypes.c_char_p],
            argnames = ["hcam", "bytes", "text"] )
    #  rs_bool pl_dd_get_info_length(int16 hcam, ctypes.POINTER(int16) bytes)
    addfunc(lib, "pl_dd_get_info_length", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "bytes"] )
    #  rs_bool pl_dd_get_ver(int16 hcam, ctypes.POINTER(uns16) dd_version)
    addfunc(lib, "pl_dd_get_ver", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "dd_version"] )
    #  rs_bool pl_dd_get_retries(int16 hcam, ctypes.POINTER(uns16) max_retries)
    addfunc(lib, "pl_dd_get_retries", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "max_retries"] )
    #  rs_bool pl_dd_set_retries(int16 hcam, uns16 max_retries)
    addfunc(lib, "pl_dd_set_retries", restype = rs_bool,
            argtypes = [int16, uns16],
            argnames = ["hcam", "max_retries"] )
    #  rs_bool pl_dd_get_timeout(int16 hcam, ctypes.POINTER(uns16) m_sec)
    addfunc(lib, "pl_dd_get_timeout", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "m_sec"] )
    #  rs_bool pl_dd_set_timeout(int16 hcam, uns16 m_sec)
    addfunc(lib, "pl_dd_set_timeout", restype = rs_bool,
            argtypes = [int16, uns16],
            argnames = ["hcam", "m_sec"] )
    #  rs_bool pl_ccd_get_adc_offset(int16 hcam, ctypes.POINTER(int16) offset)
    addfunc(lib, "pl_ccd_get_adc_offset", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "offset"] )
    #  rs_bool pl_ccd_set_adc_offset(int16 hcam, int16 offset)
    addfunc(lib, "pl_ccd_set_adc_offset", restype = rs_bool,
            argtypes = [int16, int16],
            argnames = ["hcam", "offset"] )
    #  rs_bool pl_ccd_get_chip_name(int16 hcam, ctypes.c_char_p chip_name)
    addfunc(lib, "pl_ccd_get_chip_name", restype = rs_bool,
            argtypes = [int16, ctypes.c_char_p],
            argnames = ["hcam", "chip_name"] )
    #  rs_bool pl_ccd_get_clear_cycles(int16 hcam, ctypes.POINTER(uns16) clear_cycles)
    addfunc(lib, "pl_ccd_get_clear_cycles", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "clear_cycles"] )
    #  rs_bool pl_ccd_set_clear_cycles(int16 hcam, uns16 clr_cycles)
    addfunc(lib, "pl_ccd_set_clear_cycles", restype = rs_bool,
            argtypes = [int16, uns16],
            argnames = ["hcam", "clr_cycles"] )
    #  rs_bool pl_ccd_get_clear_mode(int16 hcam, ctypes.POINTER(int16) clear_mode)
    addfunc(lib, "pl_ccd_get_clear_mode", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "clear_mode"] )
    #  rs_bool pl_ccd_set_clear_mode(int16 hcam, int16 ccd_clear)
    addfunc(lib, "pl_ccd_set_clear_mode", restype = rs_bool,
            argtypes = [int16, int16],
            argnames = ["hcam", "ccd_clear"] )
    #  rs_bool pl_ccd_get_color_mode(int16 hcam, ctypes.POINTER(uns16) color_mode)
    addfunc(lib, "pl_ccd_get_color_mode", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "color_mode"] )
    #  rs_bool pl_ccd_get_cooling_mode(int16 hcam, ctypes.POINTER(int16) cooling)
    addfunc(lib, "pl_ccd_get_cooling_mode", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "cooling"] )
    #  rs_bool pl_ccd_get_frame_capable(int16 hcam, ctypes.POINTER(rs_bool) frame_capable)
    addfunc(lib, "pl_ccd_get_frame_capable", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(rs_bool)],
            argnames = ["hcam", "frame_capable"] )
    #  rs_bool pl_ccd_get_fwell_capacity(int16 hcam, ctypes.POINTER(uns32) fwell_capacity)
    addfunc(lib, "pl_ccd_get_fwell_capacity", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns32)],
            argnames = ["hcam", "fwell_capacity"] )
    #  rs_bool pl_ccd_get_mpp_capable(int16 hcam, ctypes.POINTER(int16) mpp_capable)
    addfunc(lib, "pl_ccd_get_mpp_capable", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "mpp_capable"] )
    #  rs_bool pl_ccd_get_preamp_dly(int16 hcam, ctypes.POINTER(uns16) preamp_dly)
    addfunc(lib, "pl_ccd_get_preamp_dly", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "preamp_dly"] )
    #  rs_bool pl_ccd_get_preamp_off_control(int16 hcam, ctypes.POINTER(uns32) preamp_off_control)
    addfunc(lib, "pl_ccd_get_preamp_off_control", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns32)],
            argnames = ["hcam", "preamp_off_control"] )
    #  rs_bool pl_ccd_set_preamp_off_control(int16 hcam, uns32 preamp_off_control)
    addfunc(lib, "pl_ccd_set_preamp_off_control", restype = rs_bool,
            argtypes = [int16, uns32],
            argnames = ["hcam", "preamp_off_control"] )
    #  rs_bool pl_ccd_get_preflash(int16 hcam, ctypes.POINTER(uns16) pre_flash)
    addfunc(lib, "pl_ccd_get_preflash", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "pre_flash"] )
    #  rs_bool pl_ccd_get_pmode(int16 hcam, ctypes.POINTER(int16) pmode)
    addfunc(lib, "pl_ccd_get_pmode", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "pmode"] )
    #  rs_bool pl_ccd_set_pmode(int16 hcam, int16 pmode)
    addfunc(lib, "pl_ccd_set_pmode", restype = rs_bool,
            argtypes = [int16, int16],
            argnames = ["hcam", "pmode"] )
    #  rs_bool pl_ccd_get_premask(int16 hcam, ctypes.POINTER(uns16) pre_mask)
    addfunc(lib, "pl_ccd_get_premask", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "pre_mask"] )
    #  rs_bool pl_ccd_get_prescan(int16 hcam, ctypes.POINTER(uns16) prescan)
    addfunc(lib, "pl_ccd_get_prescan", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "prescan"] )
    #  rs_bool pl_ccd_get_postmask(int16 hcam, ctypes.POINTER(uns16) post_mask)
    addfunc(lib, "pl_ccd_get_postmask", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "post_mask"] )
    #  rs_bool pl_ccd_get_postscan(int16 hcam, ctypes.POINTER(uns16) postscan)
    addfunc(lib, "pl_ccd_get_postscan", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "postscan"] )
    #  rs_bool pl_ccd_get_par_size(int16 hcam, ctypes.POINTER(uns16) par_size)
    addfunc(lib, "pl_ccd_get_par_size", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "par_size"] )
    #  rs_bool pl_ccd_get_ser_size(int16 hcam, ctypes.POINTER(uns16) ser_size)
    addfunc(lib, "pl_ccd_get_ser_size", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "ser_size"] )
    #  rs_bool pl_ccd_get_serial_num(int16 hcam, ctypes.POINTER(uns16) serial_num)
    addfunc(lib, "pl_ccd_get_serial_num", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "serial_num"] )
    #  rs_bool pl_ccs_get_status(int16 hcam, ctypes.POINTER(int16) ccs_status)
    addfunc(lib, "pl_ccs_get_status", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "ccs_status"] )
    #  rs_bool pl_ccd_get_summing_well(int16 hcam, ctypes.POINTER(rs_bool) s_well_exists)
    addfunc(lib, "pl_ccd_get_summing_well", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(rs_bool)],
            argnames = ["hcam", "s_well_exists"] )
    #  rs_bool pl_ccd_get_tmp(int16 hcam, ctypes.POINTER(int16) cur_tmp)
    addfunc(lib, "pl_ccd_get_tmp", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "cur_tmp"] )
    #  rs_bool pl_ccd_get_tmp_range(int16 hcam, ctypes.POINTER(int16) tmp_hi_val, ctypes.POINTER(int16) tmp_lo_val)
    addfunc(lib, "pl_ccd_get_tmp_range", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16), ctypes.POINTER(int16)],
            argnames = ["hcam", "tmp_hi_val", "tmp_lo_val"] )
    #  rs_bool pl_ccd_get_tmp_setpoint(int16 hcam, ctypes.POINTER(int16) tmp_setpoint)
    addfunc(lib, "pl_ccd_get_tmp_setpoint", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "tmp_setpoint"] )
    #  rs_bool pl_ccd_set_tmp_setpoint(int16 hcam, int16 tmp_setpoint)
    addfunc(lib, "pl_ccd_set_tmp_setpoint", restype = rs_bool,
            argtypes = [int16, int16],
            argnames = ["hcam", "tmp_setpoint"] )
    #  rs_bool pl_ccd_set_readout_port(int16 unnamed_argument_007, int16 unnamed_argument_008)
    addfunc(lib, "pl_ccd_set_readout_port", restype = rs_bool,
            argtypes = [int16, int16],
            argnames = ["unnamed_argument_007", "unnamed_argument_008"] )
    #  rs_bool pl_ccd_get_pix_par_dist(int16 hcam, ctypes.POINTER(uns16) pix_par_dist)
    addfunc(lib, "pl_ccd_get_pix_par_dist", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "pix_par_dist"] )
    #  rs_bool pl_ccd_get_pix_par_size(int16 hcam, ctypes.POINTER(uns16) pix_par_size)
    addfunc(lib, "pl_ccd_get_pix_par_size", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "pix_par_size"] )
    #  rs_bool pl_ccd_get_pix_ser_dist(int16 hcam, ctypes.POINTER(uns16) pix_ser_dist)
    addfunc(lib, "pl_ccd_get_pix_ser_dist", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "pix_ser_dist"] )
    #  rs_bool pl_ccd_get_pix_ser_size(int16 hcam, ctypes.POINTER(uns16) pix_ser_size)
    addfunc(lib, "pl_ccd_get_pix_ser_size", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "pix_ser_size"] )
    #  rs_bool pl_spdtab_get_bits(int16 hcam, ctypes.POINTER(int16) spdtab_bits)
    addfunc(lib, "pl_spdtab_get_bits", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "spdtab_bits"] )
    #  rs_bool pl_spdtab_get_gain(int16 hcam, ctypes.POINTER(int16) spdtab_gain)
    addfunc(lib, "pl_spdtab_get_gain", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "spdtab_gain"] )
    #  rs_bool pl_spdtab_set_gain(int16 hcam, int16 spdtab_gain)
    addfunc(lib, "pl_spdtab_set_gain", restype = rs_bool,
            argtypes = [int16, int16],
            argnames = ["hcam", "spdtab_gain"] )
    #  rs_bool pl_spdtab_get_max_gain(int16 hcam, ctypes.POINTER(int16) spdtab_max_gain)
    addfunc(lib, "pl_spdtab_get_max_gain", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "spdtab_max_gain"] )
    #  rs_bool pl_spdtab_get_num(int16 hcam, ctypes.POINTER(int16) spdtab_num)
    addfunc(lib, "pl_spdtab_get_num", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "spdtab_num"] )
    #  rs_bool pl_spdtab_set_num(int16 hcam, int16 spdtab_num)
    addfunc(lib, "pl_spdtab_set_num", restype = rs_bool,
            argtypes = [int16, int16],
            argnames = ["hcam", "spdtab_num"] )
    #  rs_bool pl_spdtab_get_entries(int16 hcam, ctypes.POINTER(int16) spdtab_entries)
    addfunc(lib, "pl_spdtab_get_entries", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "spdtab_entries"] )
    #  rs_bool pl_spdtab_get_port(int16 hcam, ctypes.POINTER(int16) spdtab_port)
    addfunc(lib, "pl_spdtab_get_port", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "spdtab_port"] )
    #  rs_bool pl_spdtab_get_port_total(int16 hcam, ctypes.POINTER(int16) total_ports)
    addfunc(lib, "pl_spdtab_get_port_total", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "total_ports"] )
    #  rs_bool pl_spdtab_get_time(int16 hcam, ctypes.POINTER(uns16) spdtab_time)
    addfunc(lib, "pl_spdtab_get_time", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "spdtab_time"] )
    #  rs_bool pl_shtr_get_close_dly(int16 hcam, ctypes.POINTER(uns16) shtr_close_dly)
    addfunc(lib, "pl_shtr_get_close_dly", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "shtr_close_dly"] )
    #  rs_bool pl_shtr_set_close_dly(int16 hcam, uns16 shtr_close_dly)
    addfunc(lib, "pl_shtr_set_close_dly", restype = rs_bool,
            argtypes = [int16, uns16],
            argnames = ["hcam", "shtr_close_dly"] )
    #  rs_bool pl_shtr_get_open_dly(int16 hcam, ctypes.POINTER(uns16) shtr_open_dly)
    addfunc(lib, "pl_shtr_get_open_dly", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "shtr_open_dly"] )
    #  rs_bool pl_shtr_set_open_dly(int16 hcam, uns16 shtr_open_dly)
    addfunc(lib, "pl_shtr_set_open_dly", restype = rs_bool,
            argtypes = [int16, uns16],
            argnames = ["hcam", "shtr_open_dly"] )
    #  rs_bool pl_shtr_get_open_mode(int16 hcam, ctypes.POINTER(int16) shtr_open_mode)
    addfunc(lib, "pl_shtr_get_open_mode", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "shtr_open_mode"] )
    #  rs_bool pl_shtr_set_open_mode(int16 hcam, int16 shtr_open_mode)
    addfunc(lib, "pl_shtr_set_open_mode", restype = rs_bool,
            argtypes = [int16, int16],
            argnames = ["hcam", "shtr_open_mode"] )
    #  rs_bool pl_shtr_get_status(int16 hcam, ctypes.POINTER(int16) shtr_status)
    addfunc(lib, "pl_shtr_get_status", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hcam", "shtr_status"] )
    #  rs_bool pl_exp_get_time_seq(int16 hcam, ctypes.POINTER(uns16) exp_time)
    addfunc(lib, "pl_exp_get_time_seq", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "exp_time"] )
    #  rs_bool pl_exp_set_time_seq(int16 hcam, uns16 exp_time)
    addfunc(lib, "pl_exp_set_time_seq", restype = rs_bool,
            argtypes = [int16, uns16],
            argnames = ["hcam", "exp_time"] )
    #  rs_bool pl_exp_check_progress(int16 hcam, ctypes.POINTER(int16) status, ctypes.POINTER(uns32) bytes_arrived)
    addfunc(lib, "pl_exp_check_progress", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16), ctypes.POINTER(uns32)],
            argnames = ["hcam", "status", "bytes_arrived"] )
    #  rs_bool pl_exp_set_cont_mode(int16 hcam, int16 mode)
    addfunc(lib, "pl_exp_set_cont_mode", restype = rs_bool,
            argtypes = [int16, int16],
            argnames = ["hcam", "mode"] )
    #  rs_bool pl_subsys_do_diag(int16 hcam, uns8 subsys_id, ctypes.POINTER(uns16) err_code)
    addfunc(lib, "pl_subsys_do_diag", restype = rs_bool,
            argtypes = [int16, uns8, ctypes.POINTER(uns16)],
            argnames = ["hcam", "subsys_id", "err_code"] )
    #  rs_bool pl_subsys_get_id(int16 hcam, uns8 subsys_id, ctypes.POINTER(uns16) part_num, ctypes.POINTER(uns8) revision)
    addfunc(lib, "pl_subsys_get_id", restype = rs_bool,
            argtypes = [int16, uns8, ctypes.POINTER(uns16), ctypes.POINTER(uns8)],
            argnames = ["hcam", "subsys_id", "part_num", "revision"] )
    #  rs_bool pl_subsys_get_name(int16 hcam, uns8 subsys_id, ctypes.c_char_p subsys_name)
    addfunc(lib, "pl_subsys_get_name", restype = rs_bool,
            argtypes = [int16, uns8, ctypes.c_char_p],
            argnames = ["hcam", "subsys_id", "subsys_name"] )
    #  rs_bool pl_exp_get_driver_buffer(int16 hcam, ctypes.POINTER(ctypes.c_void_p) pixel_stream, ctypes.POINTER(uns32) byte_cnt)
    addfunc(lib, "pl_exp_get_driver_buffer", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(uns32)],
            argnames = ["hcam", "pixel_stream", "byte_cnt"] )
    #  rs_bool pl_buf_init()
    addfunc(lib, "pl_buf_init", restype = rs_bool,
            argtypes = [],
            argnames = [] )
    #  rs_bool pl_buf_uninit()
    addfunc(lib, "pl_buf_uninit", restype = rs_bool,
            argtypes = [],
            argnames = [] )
    #  rs_bool pl_buf_alloc(ctypes.POINTER(int16) hbuf, int16 exp_total, int16 bit_depth, int16 rgn_total, ctypes.POINTER(rgn_type) rgn_array)
    addfunc(lib, "pl_buf_alloc", restype = rs_bool,
            argtypes = [ctypes.POINTER(int16), int16, int16, int16, ctypes.POINTER(rgn_type)],
            argnames = ["hbuf", "exp_total", "bit_depth", "rgn_total", "rgn_array"] )
    #  rs_bool pl_buf_get_exp_date(int16 hbuf, int16 exp_num, ctypes.POINTER(int16) year, ctypes.POINTER(uns8) month, ctypes.POINTER(uns8) day, ctypes.POINTER(uns8) hour, ctypes.POINTER(uns8) min, ctypes.POINTER(uns8) sec, ctypes.POINTER(uns16) msec)
    addfunc(lib, "pl_buf_get_exp_date", restype = rs_bool,
            argtypes = [int16, int16, ctypes.POINTER(int16), ctypes.POINTER(uns8), ctypes.POINTER(uns8), ctypes.POINTER(uns8), ctypes.POINTER(uns8), ctypes.POINTER(uns8), ctypes.POINTER(uns16)],
            argnames = ["hbuf", "exp_num", "year", "month", "day", "hour", "min", "sec", "msec"] )
    #  rs_bool pl_buf_set_exp_date(int16 hbuf, int16 exp_num, int16 year, uns8 month, uns8 day, uns8 hour, uns8 min, uns8 sec, uns16 msec)
    addfunc(lib, "pl_buf_set_exp_date", restype = rs_bool,
            argtypes = [int16, int16, int16, uns8, uns8, uns8, uns8, uns8, uns16],
            argnames = ["hbuf", "exp_num", "year", "month", "day", "hour", "min", "sec", "msec"] )
    #  rs_bool pl_buf_get_exp_time(int16 hbuf, int16 exp_num, ctypes.POINTER(uns32) exp_msec)
    addfunc(lib, "pl_buf_get_exp_time", restype = rs_bool,
            argtypes = [int16, int16, ctypes.POINTER(uns32)],
            argnames = ["hbuf", "exp_num", "exp_msec"] )
    #  rs_bool pl_buf_get_exp_total(int16 hbuf, ctypes.POINTER(int16) total_exps)
    addfunc(lib, "pl_buf_get_exp_total", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hbuf", "total_exps"] )
    #  rs_bool pl_buf_get_img_bin(int16 himg, ctypes.POINTER(int16) ibin, ctypes.POINTER(int16) jbin)
    addfunc(lib, "pl_buf_get_img_bin", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16), ctypes.POINTER(int16)],
            argnames = ["himg", "ibin", "jbin"] )
    #  rs_bool pl_buf_get_img_handle(int16 hbuf, int16 exp_num, int16 img_num, ctypes.POINTER(int16) himg)
    addfunc(lib, "pl_buf_get_img_handle", restype = rs_bool,
            argtypes = [int16, int16, int16, ctypes.POINTER(int16)],
            argnames = ["hbuf", "exp_num", "img_num", "himg"] )
    #  rs_bool pl_buf_get_img_ofs(int16 himg, ctypes.POINTER(int16) s_ofs, ctypes.POINTER(int16) p_ofs)
    addfunc(lib, "pl_buf_get_img_ofs", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16), ctypes.POINTER(int16)],
            argnames = ["himg", "s_ofs", "p_ofs"] )
    #  rs_bool pl_buf_get_img_ptr(int16 himg, ctypes.POINTER(ctypes.c_void_p) img_addr)
    addfunc(lib, "pl_buf_get_img_ptr", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(ctypes.c_void_p)],
            argnames = ["himg", "img_addr"] )
    #  rs_bool pl_buf_get_img_size(int16 himg, ctypes.POINTER(int16) x_size, ctypes.POINTER(int16) y_size)
    addfunc(lib, "pl_buf_get_img_size", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16), ctypes.POINTER(int16)],
            argnames = ["himg", "x_size", "y_size"] )
    #  rs_bool pl_buf_get_img_total(int16 hbuf, ctypes.POINTER(int16) totl_imgs)
    addfunc(lib, "pl_buf_get_img_total", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hbuf", "totl_imgs"] )
    #  rs_bool pl_buf_get_size(int16 hbuf, ctypes.POINTER(int32) buf_size)
    addfunc(lib, "pl_buf_get_size", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int32)],
            argnames = ["hbuf", "buf_size"] )
    #  rs_bool pl_buf_free(int16 hbuf)
    addfunc(lib, "pl_buf_free", restype = rs_bool,
            argtypes = [int16],
            argnames = ["hbuf"] )
    #  rs_bool pl_buf_get_bits(int16 hbuf, ctypes.POINTER(int16) bit_depth)
    addfunc(lib, "pl_buf_get_bits", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16)],
            argnames = ["hbuf", "bit_depth"] )
    #  rs_bool pl_exp_unravel(int16 hcam, uns16 exposure, ctypes.c_void_p pixel_stream, uns16 rgn_total, ctypes.POINTER(rgn_type) rgn_array, ctypes.POINTER(ctypes.POINTER(uns16)) array_list)
    addfunc(lib, "pl_exp_unravel", restype = rs_bool,
            argtypes = [int16, uns16, ctypes.c_void_p, uns16, ctypes.POINTER(rgn_type), ctypes.POINTER(ctypes.POINTER(uns16))],
            argnames = ["hcam", "exposure", "pixel_stream", "rgn_total", "rgn_array", "array_list"] )
    #  rs_bool pl_exp_wait_start_xfer(int16 hcam, uns32 tlimit)
    addfunc(lib, "pl_exp_wait_start_xfer", restype = rs_bool,
            argtypes = [int16, uns32],
            argnames = ["hcam", "tlimit"] )
    #  rs_bool pl_exp_wait_end_xfer(int16 hcam, uns32 tlimit)
    addfunc(lib, "pl_exp_wait_end_xfer", restype = rs_bool,
            argtypes = [int16, uns32],
            argnames = ["hcam", "tlimit"] )
    #  rs_bool pv_cam_get_ccs_mem(int16 hcam, ctypes.POINTER(uns16) size)
    addfunc(lib, "pv_cam_get_ccs_mem", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns16)],
            argnames = ["hcam", "size"] )
    #  rs_bool pv_cam_send_debug(int16 hcam, ctypes.c_char_p debug_str, uns16 reply_len, ctypes.c_char_p reply_str)
    addfunc(lib, "pv_cam_send_debug", restype = rs_bool,
            argtypes = [int16, ctypes.c_char_p, uns16, ctypes.c_char_p],
            argnames = ["hcam", "debug_str", "reply_len", "reply_str"] )
    #  rs_bool pv_cam_write_read(int16 hcam, uns8 c_class, uns16 write_bytes, ctypes.POINTER(uns8) write_array, ctypes.POINTER(uns8) read_array)
    addfunc(lib, "pv_cam_write_read", restype = rs_bool,
            argtypes = [int16, uns8, uns16, ctypes.POINTER(uns8), ctypes.POINTER(uns8)],
            argnames = ["hcam", "c_class", "write_bytes", "write_array", "read_array"] )
    #  rs_bool pv_dd_active(int16 hcam, ctypes.c_void_p pixel_stream)
    addfunc(lib, "pv_dd_active", restype = rs_bool,
            argtypes = [int16, ctypes.c_void_p],
            argnames = ["hcam", "pixel_stream"] )
    #  rs_bool pv_exp_get_bytes(int16 hcam, ctypes.POINTER(uns32) exp_bytes)
    addfunc(lib, "pv_exp_get_bytes", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns32)],
            argnames = ["hcam", "exp_bytes"] )
    #  rs_bool pv_exp_get_script(int16 hcam, ctypes.POINTER(rs_bool) script_valid)
    addfunc(lib, "pv_exp_get_script", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(rs_bool)],
            argnames = ["hcam", "script_valid"] )
    #  rs_bool pv_exp_get_status(int16 hcam, ctypes.POINTER(int16) status, ctypes.POINTER(uns32) byte_cnt, ctypes.POINTER(uns32) frame_cnt)
    addfunc(lib, "pv_exp_get_status", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(int16), ctypes.POINTER(uns32), ctypes.POINTER(uns32)],
            argnames = ["hcam", "status", "byte_cnt", "frame_cnt"] )
    #  rs_bool pv_exp_set_bytes(int16 hcam, uns32 frame_count, uns32 seq_bytes, ctypes.c_void_p pixel_stream)
    addfunc(lib, "pv_exp_set_bytes", restype = rs_bool,
            argtypes = [int16, uns32, uns32, ctypes.c_void_p],
            argnames = ["hcam", "frame_count", "seq_bytes", "pixel_stream"] )
    #  rs_bool pv_exp_set_script(int16 hcam, rs_bool script_valid)
    addfunc(lib, "pv_exp_set_script", restype = rs_bool,
            argtypes = [int16, rs_bool],
            argnames = ["hcam", "script_valid"] )
    #  rs_bool pv_set_error_code(int16 omode, int16 err_code)
    addfunc(lib, "pv_set_error_code", restype = rs_bool,
            argtypes = [int16, int16],
            argnames = ["omode", "err_code"] )
    #  rs_bool pv_cam_do_reads(int16 hcam)
    addfunc(lib, "pv_cam_do_reads", restype = rs_bool,
            argtypes = [int16],
            argnames = ["hcam"] )
    #  rs_bool pv_free(ctypes.c_void_p block, int16 heap)
    addfunc(lib, "pv_free", restype = rs_bool,
            argtypes = [ctypes.c_void_p, int16],
            argnames = ["block", "heap"] )
    #  ctypes.c_void_p pv_malloc(uns32 size, int16 heap)
    addfunc(lib, "pv_malloc", restype = ctypes.c_void_p,
            argtypes = [uns32, int16],
            argnames = ["size", "heap"] )
    #  ctypes.c_void_p pv_realloc(ctypes.c_void_p block, uns32 size, int16 heap)
    addfunc(lib, "pv_realloc", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, uns32, int16],
            argnames = ["block", "size", "heap"] )
    #  rs_bool pv_script_set_hook(ctypes.POINTER(ctypes.c_void_p) pfn)
    addfunc(lib, "pv_script_set_hook", restype = rs_bool,
            argtypes = [ctypes.POINTER(ctypes.c_void_p)],
            argnames = ["pfn"] )
    #  rs_bool pv_ccd_get_accum_capable(int16 hcam, ctypes.POINTER(rs_bool) accum_capable)
    addfunc(lib, "pv_ccd_get_accum_capable", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(rs_bool)],
            argnames = ["hcam", "accum_capable"] )
    #  rs_bool pv_exp_get_frames(int16 hcam, ctypes.POINTER(uns32) exp_frames)
    addfunc(lib, "pv_exp_get_frames", restype = rs_bool,
            argtypes = [int16, ctypes.POINTER(uns32)],
            argnames = ["hcam", "exp_frames"] )
    #  rs_bool pv_exp_set_frames(int16 hcam, uns32 exp_frames)
    addfunc(lib, "pv_exp_set_frames", restype = rs_bool,
            argtypes = [int16, uns32],
            argnames = ["hcam", "exp_frames"] )
    #  rs_bool pv_exp_set_no_readout_timeout(int16 hcam)
    addfunc(lib, "pv_exp_set_no_readout_timeout", restype = rs_bool,
            argtypes = [int16],
            argnames = ["hcam"] )
    #  rs_bool pv_exp_reset_no_readout_timeout(int16 hcam)
    addfunc(lib, "pv_exp_reset_no_readout_timeout", restype = rs_bool,
            argtypes = [int16],
            argnames = ["hcam"] )
    #  rs_bool pm_cam_write_read(int16 hcam, uns8 c_class, uns16 write_bytes, ctypes.POINTER(uns8) write_array, ctypes.POINTER(uns8) read_array)
    addfunc(lib, "pm_cam_write_read", restype = rs_bool,
            argtypes = [int16, uns8, uns16, ctypes.POINTER(uns8), ctypes.POINTER(uns8)],
            argnames = ["hcam", "c_class", "write_bytes", "write_array", "read_array"] )
    #  rs_bool pl_ddi_get_ver(ctypes.POINTER(uns16) ddi_version)
    addfunc(lib, "pl_ddi_get_ver", restype = rs_bool,
            argtypes = [ctypes.POINTER(uns16)],
            argnames = ["ddi_version"] )
    #  rs_bool pl_cam_get_diags(int16 hcam)
    addfunc(lib, "pl_cam_get_diags", restype = rs_bool,
            argtypes = [int16],
            argnames = ["hcam"] )
    #  rs_bool pl_md_frame_decode(ctypes.POINTER(md_frame) pDstFrame, ctypes.c_void_p pSrcBuf, uns32 srcBufSize)
    addfunc(lib, "pl_md_frame_decode", restype = rs_bool,
            argtypes = [ctypes.POINTER(md_frame), ctypes.c_void_p, uns32],
            argnames = ["pDstFrame", "pSrcBuf", "srcBufSize"] )
    #  rs_bool pl_md_frame_recompose(ctypes.c_void_p pDstBuf, uns16 offX, uns16 offY, uns16 dstWidth, uns16 dstHeight, ctypes.POINTER(md_frame) pSrcFrame)
    addfunc(lib, "pl_md_frame_recompose", restype = rs_bool,
            argtypes = [ctypes.c_void_p, uns16, uns16, uns16, uns16, ctypes.POINTER(md_frame)],
            argnames = ["pDstBuf", "offX", "offY", "dstWidth", "dstHeight", "pSrcFrame"] )
    #  rs_bool pl_md_create_frame_struct_cont(ctypes.POINTER(ctypes.POINTER(md_frame)) pFrame, uns16 roiCount)
    addfunc(lib, "pl_md_create_frame_struct_cont", restype = rs_bool,
            argtypes = [ctypes.POINTER(ctypes.POINTER(md_frame)), uns16],
            argnames = ["pFrame", "roiCount"] )
    #  rs_bool pl_md_create_frame_struct(ctypes.POINTER(ctypes.POINTER(md_frame)) pFrame, ctypes.c_void_p pSrcBuf, uns32 srcBufSize)
    addfunc(lib, "pl_md_create_frame_struct", restype = rs_bool,
            argtypes = [ctypes.POINTER(ctypes.POINTER(md_frame)), ctypes.c_void_p, uns32],
            argnames = ["pFrame", "pSrcBuf", "srcBufSize"] )
    #  rs_bool pl_md_release_frame_struct(ctypes.POINTER(md_frame) pFrame)
    addfunc(lib, "pl_md_release_frame_struct", restype = rs_bool,
            argtypes = [ctypes.POINTER(md_frame)],
            argnames = ["pFrame"] )
    #  rs_bool pl_md_read_extended(ctypes.POINTER(md_ext_item_collection) pOutput, ctypes.c_void_p pExtMdPtr, uns32 extMdSize)
    addfunc(lib, "pl_md_read_extended", restype = rs_bool,
            argtypes = [ctypes.POINTER(md_ext_item_collection), ctypes.c_void_p, uns32],
            argnames = ["pOutput", "pExtMdPtr", "extMdSize"] )


