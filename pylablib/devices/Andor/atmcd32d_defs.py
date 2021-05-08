##########   This file is generated automatically based on atmcd32d.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class AT_DDG_POL(enum.IntEnum):
    AT_DDG_POLARITY_POSITIVE = _int32(0)
    AT_DDG_POLARITY_NEGATIVE = _int32(1)
dAT_DDG_POL={a.name:a.value for a in AT_DDG_POL}
drAT_DDG_POL={a.value:a.name for a in AT_DDG_POL}


class AT_DDG_TERM(enum.IntEnum):
    AT_DDG_TERMINATION_50OHMS = _int32(0)
    AT_DDG_TERMINATION_HIGHZ  = _int32(1)
dAT_DDG_TERM={a.name:a.value for a in AT_DDG_TERM}
drAT_DDG_TERM={a.value:a.name for a in AT_DDG_TERM}


class AT_STEPMODE(enum.IntEnum):
    AT_STEPMODE_CONSTANT    = _int32(0)
    AT_STEPMODE_EXPONENTIAL = _int32(1)
    AT_STEPMODE_LOGARITHMIC = _int32(2)
    AT_STEPMODE_LINEAR      = _int32(3)
    AT_STEPMODE_OFF         = _int32(100)
dAT_STEPMODE={a.name:a.value for a in AT_STEPMODE}
drAT_STEPMODE={a.value:a.name for a in AT_STEPMODE}


class AT_GATEMODE(enum.IntEnum):
    AT_GATEMODE_FIRE_AND_GATE = _int32(0)
    AT_GATEMODE_FIRE_ONLY     = _int32(1)
    AT_GATEMODE_GATE_ONLY     = _int32(2)
    AT_GATEMODE_CW_ON         = _int32(3)
    AT_GATEMODE_CW_OFF        = _int32(4)
    AT_GATEMODE_DDG           = _int32(5)
dAT_GATEMODE={a.name:a.value for a in AT_GATEMODE}
drAT_GATEMODE={a.value:a.name for a in AT_GATEMODE}


class DRV_STATUS(enum.IntEnum):
    DRV_ERROR_CODES                        = _int32(20001)
    DRV_SUCCESS                            = _int32(20002)
    DRV_VXDNOTINSTALLED                    = _int32(20003)
    DRV_ERROR_SCAN                         = _int32(20004)
    DRV_ERROR_CHECK_SUM                    = _int32(20005)
    DRV_ERROR_FILELOAD                     = _int32(20006)
    DRV_UNKNOWN_FUNCTION                   = _int32(20007)
    DRV_ERROR_VXD_INIT                     = _int32(20008)
    DRV_ERROR_ADDRESS                      = _int32(20009)
    DRV_ERROR_PAGELOCK                     = _int32(20010)
    DRV_ERROR_PAGEUNLOCK                   = _int32(20011)
    DRV_ERROR_BOARDTEST                    = _int32(20012)
    DRV_ERROR_ACK                          = _int32(20013)
    DRV_ERROR_UP_FIFO                      = _int32(20014)
    DRV_ERROR_PATTERN                      = _int32(20015)
    DRV_ACQUISITION_ERRORS                 = _int32(20017)
    DRV_ACQ_BUFFER                         = _int32(20018)
    DRV_ACQ_DOWNFIFO_FULL                  = _int32(20019)
    DRV_PROC_UNKONWN_INSTRUCTION           = _int32(20020)
    DRV_ILLEGAL_OP_CODE                    = _int32(20021)
    DRV_KINETIC_TIME_NOT_MET               = _int32(20022)
    DRV_ACCUM_TIME_NOT_MET                 = _int32(20023)
    DRV_NO_NEW_DATA                        = _int32(20024)
    DRV_PCI_DMA_FAIL                       = _int32(20025)
    DRV_SPOOLERROR                         = _int32(20026)
    DRV_SPOOLSETUPERROR                    = _int32(20027)
    DRV_FILESIZELIMITERROR                 = _int32(20028)
    DRV_ERROR_FILESAVE                     = _int32(20029)
    DRV_TEMPERATURE_CODES                  = _int32(20033)
    DRV_TEMPERATURE_OFF                    = _int32(20034)
    DRV_TEMPERATURE_NOT_STABILIZED         = _int32(20035)
    DRV_TEMPERATURE_STABILIZED             = _int32(20036)
    DRV_TEMPERATURE_NOT_REACHED            = _int32(20037)
    DRV_TEMPERATURE_OUT_RANGE              = _int32(20038)
    DRV_TEMPERATURE_NOT_SUPPORTED          = _int32(20039)
    DRV_TEMPERATURE_DRIFT                  = _int32(20040)
    DRV_TEMP_CODES                         = _int32(20033)
    DRV_TEMP_OFF                           = _int32(20034)
    DRV_TEMP_NOT_STABILIZED                = _int32(20035)
    DRV_TEMP_STABILIZED                    = _int32(20036)
    DRV_TEMP_NOT_REACHED                   = _int32(20037)
    DRV_TEMP_OUT_RANGE                     = _int32(20038)
    DRV_TEMP_NOT_SUPPORTED                 = _int32(20039)
    DRV_TEMP_DRIFT                         = _int32(20040)
    DRV_GENERAL_ERRORS                     = _int32(20049)
    DRV_INVALID_AUX                        = _int32(20050)
    DRV_COF_NOTLOADED                      = _int32(20051)
    DRV_FPGAPROG                           = _int32(20052)
    DRV_FLEXERROR                          = _int32(20053)
    DRV_GPIBERROR                          = _int32(20054)
    DRV_EEPROMVERSIONERROR                 = _int32(20055)
    DRV_DATATYPE                           = _int32(20064)
    DRV_DRIVER_ERRORS                      = _int32(20065)
    DRV_P1INVALID                          = _int32(20066)
    DRV_P2INVALID                          = _int32(20067)
    DRV_P3INVALID                          = _int32(20068)
    DRV_P4INVALID                          = _int32(20069)
    DRV_INIERROR                           = _int32(20070)
    DRV_COFERROR                           = _int32(20071)
    DRV_ACQUIRING                          = _int32(20072)
    DRV_IDLE                               = _int32(20073)
    DRV_TEMPCYCLE                          = _int32(20074)
    DRV_NOT_INITIALIZED                    = _int32(20075)
    DRV_P5INVALID                          = _int32(20076)
    DRV_P6INVALID                          = _int32(20077)
    DRV_INVALID_MODE                       = _int32(20078)
    DRV_INVALID_FILTER                     = _int32(20079)
    DRV_I2CERRORS                          = _int32(20080)
    DRV_I2CDEVNOTFOUND                     = _int32(20081)
    DRV_I2CTIMEOUT                         = _int32(20082)
    DRV_P7INVALID                          = _int32(20083)
    DRV_P8INVALID                          = _int32(20084)
    DRV_P9INVALID                          = _int32(20085)
    DRV_P10INVALID                         = _int32(20086)
    DRV_P11INVALID                         = _int32(20087)
    DRV_USBERROR                           = _int32(20089)
    DRV_IOCERROR                           = _int32(20090)
    DRV_VRMVERSIONERROR                    = _int32(20091)
    DRV_GATESTEPERROR                      = _int32(20092)
    DRV_USB_INTERRUPT_ENDPOINT_ERROR       = _int32(20093)
    DRV_RANDOM_TRACK_ERROR                 = _int32(20094)
    DRV_INVALID_TRIGGER_MODE               = _int32(20095)
    DRV_LOAD_FIRMWARE_ERROR                = _int32(20096)
    DRV_DIVIDE_BY_ZERO_ERROR               = _int32(20097)
    DRV_INVALID_RINGEXPOSURES              = _int32(20098)
    DRV_BINNING_ERROR                      = _int32(20099)
    DRV_INVALID_AMPLIFIER                  = _int32(20100)
    DRV_INVALID_COUNTCONVERT_MODE          = _int32(20101)
    DRV_USB_INTERRUPT_ENDPOINT_TIMEOUT     = _int32(20102)
    DRV_ERROR_NOCAMERA                     = _int32(20990)
    DRV_NOT_SUPPORTED                      = _int32(20991)
    DRV_NOT_AVAILABLE                      = _int32(20992)
    DRV_ERROR_MAP                          = _int32(20115)
    DRV_ERROR_UNMAP                        = _int32(20116)
    DRV_ERROR_MDL                          = _int32(20117)
    DRV_ERROR_UNMDL                        = _int32(20118)
    DRV_ERROR_BUFFSIZE                     = _int32(20119)
    DRV_ERROR_NOHANDLE                     = _int32(20121)
    DRV_GATING_NOT_AVAILABLE               = _int32(20130)
    DRV_FPGA_VOLTAGE_ERROR                 = _int32(20131)
    DRV_OW_CMD_FAIL                        = _int32(20150)
    DRV_OWMEMORY_BAD_ADDR                  = _int32(20151)
    DRV_OWCMD_NOT_AVAILABLE                = _int32(20152)
    DRV_OW_NO_SLAVES                       = _int32(20153)
    DRV_OW_NOT_INITIALIZED                 = _int32(20154)
    DRV_OW_ERROR_SLAVE_NUM                 = _int32(20155)
    DRV_MSTIMINGS_ERROR                    = _int32(20156)
    DRV_OA_NULL_ERROR                      = _int32(20173)
    DRV_OA_PARSE_DTD_ERROR                 = _int32(20174)
    DRV_OA_DTD_VALIDATE_ERROR              = _int32(20175)
    DRV_OA_FILE_ACCESS_ERROR               = _int32(20176)
    DRV_OA_FILE_DOES_NOT_EXIST             = _int32(20177)
    DRV_OA_XML_INVALID_OR_NOT_FOUND_ERROR  = _int32(20178)
    DRV_OA_PRESET_FILE_NOT_LOADED          = _int32(20179)
    DRV_OA_USER_FILE_NOT_LOADED            = _int32(20180)
    DRV_OA_PRESET_AND_USER_FILE_NOT_LOADED = _int32(20181)
    DRV_OA_INVALID_FILE                    = _int32(20182)
    DRV_OA_FILE_HAS_BEEN_MODIFIED          = _int32(20183)
    DRV_OA_BUFFER_FULL                     = _int32(20184)
    DRV_OA_INVALID_STRING_LENGTH           = _int32(20185)
    DRV_OA_INVALID_CHARS_IN_NAME           = _int32(20186)
    DRV_OA_INVALID_NAMING                  = _int32(20187)
    DRV_OA_GET_CAMERA_ERROR                = _int32(20188)
    DRV_OA_MODE_ALREADY_EXISTS             = _int32(20189)
    DRV_OA_STRINGS_NOT_EQUAL               = _int32(20190)
    DRV_OA_NO_USER_DATA                    = _int32(20191)
    DRV_OA_VALUE_NOT_SUPPORTED             = _int32(20192)
    DRV_OA_MODE_DOES_NOT_EXIST             = _int32(20193)
    DRV_OA_CAMERA_NOT_SUPPORTED            = _int32(20194)
    DRV_OA_FAILED_TO_GET_MODE              = _int32(20195)
    DRV_OA_CAMERA_NOT_AVAILABLE            = _int32(20196)
    DRV_PROCESSING_FAILED                  = _int32(20211)
dDRV_STATUS={a.name:a.value for a in DRV_STATUS}
drDRV_STATUS={a.value:a.name for a in DRV_STATUS}


class AC_ACQMODE(enum.IntEnum):
    AC_ACQMODE_SINGLE        = _int32(1)
    AC_ACQMODE_VIDEO         = _int32(2)
    AC_ACQMODE_ACCUMULATE    = _int32(4)
    AC_ACQMODE_KINETIC       = _int32(8)
    AC_ACQMODE_FRAMETRANSFER = _int32(16)
    AC_ACQMODE_FASTKINETICS  = _int32(32)
    AC_ACQMODE_OVERLAP       = _int32(64)
    AC_ACQMODE_TDI           = _int32(0x80)
dAC_ACQMODE={a.name:a.value for a in AC_ACQMODE}
drAC_ACQMODE={a.value:a.name for a in AC_ACQMODE}


class AC_READMODE(enum.IntEnum):
    AC_READMODE_FULLIMAGE      = _int32(1)
    AC_READMODE_SUBIMAGE       = _int32(2)
    AC_READMODE_SINGLETRACK    = _int32(4)
    AC_READMODE_FVB            = _int32(8)
    AC_READMODE_MULTITRACK     = _int32(16)
    AC_READMODE_RANDOMTRACK    = _int32(32)
    AC_READMODE_MULTITRACKSCAN = _int32(64)
dAC_READMODE={a.name:a.value for a in AC_READMODE}
drAC_READMODE={a.value:a.name for a in AC_READMODE}


class AC_TRIGGERMODE(enum.IntEnum):
    AC_TRIGGERMODE_INTERNAL                = _int32(1)
    AC_TRIGGERMODE_EXTERNAL                = _int32(2)
    AC_TRIGGERMODE_EXTERNAL_FVB_EM         = _int32(4)
    AC_TRIGGERMODE_CONTINUOUS              = _int32(8)
    AC_TRIGGERMODE_EXTERNALSTART           = _int32(16)
    AC_TRIGGERMODE_EXTERNALEXPOSURE        = _int32(32)
    AC_TRIGGERMODE_INVERTED                = _int32(0x40)
    AC_TRIGGERMODE_EXTERNAL_CHARGESHIFTING = _int32(0x80)
    AC_TRIGGERMODE_EXTERNAL_RISING         = _int32(0x0100)
    AC_TRIGGERMODE_EXTERNAL_PURGE          = _int32(0x0200)
dAC_TRIGGERMODE={a.name:a.value for a in AC_TRIGGERMODE}
drAC_TRIGGERMODE={a.value:a.name for a in AC_TRIGGERMODE}


class AC_CAMERATYPE(enum.IntEnum):
    AC_CAMERATYPE_PDA          = _int32(0)
    AC_CAMERATYPE_IXON         = _int32(1)
    AC_CAMERATYPE_ICCD         = _int32(2)
    AC_CAMERATYPE_EMCCD        = _int32(3)
    AC_CAMERATYPE_CCD          = _int32(4)
    AC_CAMERATYPE_ISTAR        = _int32(5)
    AC_CAMERATYPE_VIDEO        = _int32(6)
    AC_CAMERATYPE_IDUS         = _int32(7)
    AC_CAMERATYPE_NEWTON       = _int32(8)
    AC_CAMERATYPE_SURCAM       = _int32(9)
    AC_CAMERATYPE_USBICCD      = _int32(10)
    AC_CAMERATYPE_LUCA         = _int32(11)
    AC_CAMERATYPE_RESERVED     = _int32(12)
    AC_CAMERATYPE_IKON         = _int32(13)
    AC_CAMERATYPE_INGAAS       = _int32(14)
    AC_CAMERATYPE_IVAC         = _int32(15)
    AC_CAMERATYPE_UNPROGRAMMED = _int32(16)
    AC_CAMERATYPE_CLARA        = _int32(17)
    AC_CAMERATYPE_USBISTAR     = _int32(18)
    AC_CAMERATYPE_SIMCAM       = _int32(19)
    AC_CAMERATYPE_NEO          = _int32(20)
    AC_CAMERATYPE_IXONULTRA    = _int32(21)
    AC_CAMERATYPE_VOLMOS       = _int32(22)
    AC_CAMERATYPE_IVAC_CCD     = _int32(23)
    AC_CAMERATYPE_ASPEN        = _int32(24)
    AC_CAMERATYPE_ASCENT       = _int32(25)
    AC_CAMERATYPE_ALTA         = _int32(26)
    AC_CAMERATYPE_ALTAF        = _int32(27)
    AC_CAMERATYPE_IKONXL       = _int32(28)
    AC_CAMERATYPE_CMOS_GEN2    = _int32(29)
    AC_CAMERATYPE_ISTAR_SCMOS  = _int32(30)
    AC_CAMERATYPE_IKONLR       = _int32(31)
dAC_CAMERATYPE={a.name:a.value for a in AC_CAMERATYPE}
drAC_CAMERATYPE={a.value:a.name for a in AC_CAMERATYPE}


class AC_PIXELMODE(enum.IntEnum):
    AC_PIXELMODE_8BIT  = _int32(1)
    AC_PIXELMODE_14BIT = _int32(2)
    AC_PIXELMODE_16BIT = _int32(4)
    AC_PIXELMODE_32BIT = _int32(8)
    AC_PIXELMODE_MONO  = _int32(0x000000)
    AC_PIXELMODE_RGB   = _int32(0x010000)
    AC_PIXELMODE_CMY   = _int32(0x020000)
dAC_PIXELMODE={a.name:a.value for a in AC_PIXELMODE}
drAC_PIXELMODE={a.value:a.name for a in AC_PIXELMODE}


class AC_SETFUNC(enum.IntEnum):
    AC_SETFUNCTION_VREADOUT           = _int32(0x01)
    AC_SETFUNCTION_HREADOUT           = _int32(0x02)
    AC_SETFUNCTION_TEMPERATURE        = _int32(0x04)
    AC_SETFUNCTION_MCPGAIN            = _int32(0x08)
    AC_SETFUNCTION_EMCCDGAIN          = _int32(0x10)
    AC_SETFUNCTION_BASELINECLAMP      = _int32(0x20)
    AC_SETFUNCTION_VSAMPLITUDE        = _int32(0x40)
    AC_SETFUNCTION_HIGHCAPACITY       = _int32(0x80)
    AC_SETFUNCTION_BASELINEOFFSET     = _int32(0x0100)
    AC_SETFUNCTION_PREAMPGAIN         = _int32(0x0200)
    AC_SETFUNCTION_CROPMODE           = _int32(0x0400)
    AC_SETFUNCTION_DMAPARAMETERS      = _int32(0x0800)
    AC_SETFUNCTION_HORIZONTALBIN      = _int32(0x1000)
    AC_SETFUNCTION_MULTITRACKHRANGE   = _int32(0x2000)
    AC_SETFUNCTION_RANDOMTRACKNOGAPS  = _int32(0x4000)
    AC_SETFUNCTION_EMADVANCED         = _int32(0x8000)
    AC_SETFUNCTION_GATEMODE           = _int32(0x010000)
    AC_SETFUNCTION_DDGTIMES           = _int32(0x020000)
    AC_SETFUNCTION_IOC                = _int32(0x040000)
    AC_SETFUNCTION_INTELLIGATE        = _int32(0x080000)
    AC_SETFUNCTION_INSERTION_DELAY    = _int32(0x100000)
    AC_SETFUNCTION_GATESTEP           = _int32(0x200000)
    AC_SETFUNCTION_GATEDELAYSTEP      = _int32(0x200000)
    AC_SETFUNCTION_TRIGGERTERMINATION = _int32(0x400000)
    AC_SETFUNCTION_EXTENDEDNIR        = _int32(0x800000)
    AC_SETFUNCTION_SPOOLTHREADCOUNT   = _int32(0x1000000)
    AC_SETFUNCTION_REGISTERPACK       = _int32(0x2000000)
    AC_SETFUNCTION_PRESCANS           = _int32(0x4000000)
    AC_SETFUNCTION_GATEWIDTHSTEP      = _int32(0x8000000)
    AC_SETFUNCTION_EXTENDED_CROP_MODE = _int32(0x10000000)
    AC_SETFUNCTION_SUPERKINETICS      = _int32(0x20000000)
    AC_SETFUNCTION_TIMESCAN           = _int32(0x40000000)
    AC_SETFUNCTION_CROPMODETYPE       = _int32(0x80000000)
dAC_SETFUNC={a.name:a.value for a in AC_SETFUNC}
drAC_SETFUNC={a.value:a.name for a in AC_SETFUNC}


class AC_GETFUNC(enum.IntEnum):
    AC_GETFUNCTION_TEMPERATURE       = _int32(0x01)
    AC_GETFUNCTION_TARGETTEMPERATURE = _int32(0x02)
    AC_GETFUNCTION_TEMPERATURERANGE  = _int32(0x04)
    AC_GETFUNCTION_DETECTORSIZE      = _int32(0x08)
    AC_GETFUNCTION_MCPGAIN           = _int32(0x10)
    AC_GETFUNCTION_EMCCDGAIN         = _int32(0x20)
    AC_GETFUNCTION_HVFLAG            = _int32(0x40)
    AC_GETFUNCTION_GATEMODE          = _int32(0x80)
    AC_GETFUNCTION_DDGTIMES          = _int32(0x0100)
    AC_GETFUNCTION_IOC               = _int32(0x0200)
    AC_GETFUNCTION_INTELLIGATE       = _int32(0x0400)
    AC_GETFUNCTION_INSERTION_DELAY   = _int32(0x0800)
    AC_GETFUNCTION_GATESTEP          = _int32(0x1000)
    AC_GETFUNCTION_GATEDELAYSTEP     = _int32(0x1000)
    AC_GETFUNCTION_PHOSPHORSTATUS    = _int32(0x2000)
    AC_GETFUNCTION_MCPGAINTABLE      = _int32(0x4000)
    AC_GETFUNCTION_BASELINECLAMP     = _int32(0x8000)
    AC_GETFUNCTION_GATEWIDTHSTEP     = _int32(0x10000)
dAC_GETFUNC={a.name:a.value for a in AC_GETFUNC}
drAC_GETFUNC={a.value:a.name for a in AC_GETFUNC}


class AC_FEATURES(enum.IntEnum):
    AC_FEATURES_POLLING                        = _int32(1)
    AC_FEATURES_EVENTS                         = _int32(2)
    AC_FEATURES_SPOOLING                       = _int32(4)
    AC_FEATURES_SHUTTER                        = _int32(8)
    AC_FEATURES_SHUTTEREX                      = _int32(16)
    AC_FEATURES_EXTERNAL_I2C                   = _int32(32)
    AC_FEATURES_SATURATIONEVENT                = _int32(64)
    AC_FEATURES_FANCONTROL                     = _int32(128)
    AC_FEATURES_MIDFANCONTROL                  = _int32(256)
    AC_FEATURES_TEMPERATUREDURINGACQUISITION   = _int32(512)
    AC_FEATURES_KEEPCLEANCONTROL               = _int32(1024)
    AC_FEATURES_DDGLITE                        = _int32(0x0800)
    AC_FEATURES_FTEXTERNALEXPOSURE             = _int32(0x1000)
    AC_FEATURES_KINETICEXTERNALEXPOSURE        = _int32(0x2000)
    AC_FEATURES_DACCONTROL                     = _int32(0x4000)
    AC_FEATURES_METADATA                       = _int32(0x8000)
    AC_FEATURES_IOCONTROL                      = _int32(0x10000)
    AC_FEATURES_PHOTONCOUNTING                 = _int32(0x20000)
    AC_FEATURES_COUNTCONVERT                   = _int32(0x40000)
    AC_FEATURES_DUALMODE                       = _int32(0x80000)
    AC_FEATURES_OPTACQUIRE                     = _int32(0x100000)
    AC_FEATURES_REALTIMESPURIOUSNOISEFILTER    = _int32(0x200000)
    AC_FEATURES_POSTPROCESSSPURIOUSNOISEFILTER = _int32(0x400000)
    AC_FEATURES_DUALPREAMPGAIN                 = _int32(0x800000)
    AC_FEATURES_DEFECT_CORRECTION              = _int32(0x1000000)
    AC_FEATURES_STARTOFEXPOSURE_EVENT          = _int32(0x2000000)
    AC_FEATURES_ENDOFEXPOSURE_EVENT            = _int32(0x4000000)
    AC_FEATURES_CAMERALINK                     = _int32(0x8000000)
    AC_FEATURES_FIFOFULL_EVENT                 = _int32(0x10000000)
    AC_FEATURES_SENSOR_PORT_CONFIGURATION      = _int32(0x20000000)
    AC_FEATURES_SENSOR_COMPENSATION            = _int32(0x40000000)
    AC_FEATURES_IRIG_SUPPORT                   = _int32(0x80000000)
dAC_FEATURES={a.name:a.value for a in AC_FEATURES}
drAC_FEATURES={a.value:a.name for a in AC_FEATURES}


class AC_EMGAIN(enum.IntEnum):
    AC_EMGAIN_8BIT     = _int32(1)
    AC_EMGAIN_12BIT    = _int32(2)
    AC_EMGAIN_LINEAR12 = _int32(4)
    AC_EMGAIN_REAL12   = _int32(8)
dAC_EMGAIN={a.name:a.value for a in AC_EMGAIN}
drAC_EMGAIN={a.value:a.name for a in AC_EMGAIN}


class AC_FEATURES32(enum.IntEnum):
    AC_FEATURES2_ESD_EVENTS              = _int32(1)
    AC_FEATURES2_DUAL_PORT_CONFIGURATION = _int32(2)
    AC_FEATURES2_OVERTEMP_EVENTS         = _int32(4)
dAC_FEATURES32={a.name:a.value for a in AC_FEATURES32}
drAC_FEATURES32={a.value:a.name for a in AC_FEATURES32}





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
ULONG=ctypes.c_ulong
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
class AT_VersionInfoId(enum.IntEnum):
    AT_SDKVersion         =_int32(0x40000000)
    AT_DeviceDriverVersion=_int32(0x40000001)
dAT_VersionInfoId={a.name:a.value for a in AT_VersionInfoId}
drAT_VersionInfoId={a.value:a.name for a in AT_VersionInfoId}


class AT_DDGLiteChannelId(enum.IntEnum):
    AT_DDGLite_ChannelA=_int32(0x40000000)
    AT_DDGLite_ChannelB=_int32(0x40000001)
    AT_DDGLite_ChannelC=_int32(0x40000002)
dAT_DDGLiteChannelId={a.name:a.value for a in AT_DDGLiteChannelId}
drAT_DDGLiteChannelId={a.value:a.name for a in AT_DDGLiteChannelId}


class AndorCapabilities(ctypes.Structure):
    _fields_=[  ("ulSize",ULONG),
                ("ulAcqModes",ULONG),
                ("ulReadModes",ULONG),
                ("ulTriggerModes",ULONG),
                ("ulCameraType",ULONG),
                ("ulPixelMode",ULONG),
                ("ulSetFunctions",ULONG),
                ("ulGetFunctions",ULONG),
                ("ulFeatures",ULONG),
                ("ulPCICard",ULONG),
                ("ulEMGainCapability",ULONG),
                ("ulFTReadModes",ULONG),
                ("ulFeatures2",ULONG) ]
PAndorCapabilities=ctypes.POINTER(AndorCapabilities)
class CAndorCapabilities(ctypes_wrap.CStructWrapper):
    _struct=AndorCapabilities


class ColorDemosaicInfo(ctypes.Structure):
    _fields_=[  ("iX",ctypes.c_int),
                ("iY",ctypes.c_int),
                ("iAlgorithm",ctypes.c_int),
                ("iXPhase",ctypes.c_int),
                ("iYPhase",ctypes.c_int),
                ("iBackground",ctypes.c_int) ]
PColorDemosaicInfo=ctypes.POINTER(ColorDemosaicInfo)
class CColorDemosaicInfo(ctypes_wrap.CStructWrapper):
    _struct=ColorDemosaicInfo


class WhiteBalanceInfo(ctypes.Structure):
    _fields_=[  ("iSize",ctypes.c_int),
                ("iX",ctypes.c_int),
                ("iY",ctypes.c_int),
                ("iAlgorithm",ctypes.c_int),
                ("iROI_left",ctypes.c_int),
                ("iROI_right",ctypes.c_int),
                ("iROI_top",ctypes.c_int),
                ("iROI_bottom",ctypes.c_int),
                ("iOperation",ctypes.c_int) ]
PWhiteBalanceInfo=ctypes.POINTER(WhiteBalanceInfo)
class CWhiteBalanceInfo(ctypes_wrap.CStructWrapper):
    _struct=WhiteBalanceInfo





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
    #  ctypes.c_uint AbortAcquisition()
    addfunc(lib, "AbortAcquisition", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint CancelWait()
    addfunc(lib, "CancelWait", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint CoolerOFF()
    addfunc(lib, "CoolerOFF", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint CoolerON()
    addfunc(lib, "CoolerON", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint DemosaicImage(ctypes.POINTER(WORD) grey, ctypes.POINTER(WORD) red, ctypes.POINTER(WORD) green, ctypes.POINTER(WORD) blue, ctypes.POINTER(ColorDemosaicInfo) info)
    addfunc(lib, "DemosaicImage", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(ColorDemosaicInfo)],
            argnames = ["grey", "red", "green", "blue", "info"] )
    #  ctypes.c_uint EnableKeepCleans(ctypes.c_int iMode)
    addfunc(lib, "EnableKeepCleans", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["iMode"] )
    #  ctypes.c_uint EnableSensorCompensation(ctypes.c_int iMode)
    addfunc(lib, "EnableSensorCompensation", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["iMode"] )
    #  ctypes.c_uint SetIRIGModulation(ctypes.c_char mode)
    addfunc(lib, "SetIRIGModulation", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char],
            argnames = ["mode"] )
    #  ctypes.c_uint FreeInternalMemory()
    addfunc(lib, "FreeInternalMemory", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint GetAcquiredData(ctypes.POINTER(ctypes.c_long) arr, ctypes.c_ulong size)
    addfunc(lib, "GetAcquiredData", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.c_ulong],
            argnames = ["arr", "size"] )
    #  ctypes.c_uint GetAcquiredData16(ctypes.POINTER(WORD) arr, ctypes.c_ulong size)
    addfunc(lib, "GetAcquiredData16", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(WORD), ctypes.c_ulong],
            argnames = ["arr", "size"] )
    #  ctypes.c_uint GetAcquiredFloatData(ctypes.POINTER(ctypes.c_float) arr, ctypes.c_ulong size)
    addfunc(lib, "GetAcquiredFloatData", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_ulong],
            argnames = ["arr", "size"] )
    #  ctypes.c_uint GetAcquisitionProgress(ctypes.POINTER(ctypes.c_long) acc, ctypes.POINTER(ctypes.c_long) series)
    addfunc(lib, "GetAcquisitionProgress", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long)],
            argnames = ["acc", "series"] )
    #  ctypes.c_uint GetAcquisitionTimings(ctypes.POINTER(ctypes.c_float) exposure, ctypes.POINTER(ctypes.c_float) accumulate, ctypes.POINTER(ctypes.c_float) kinetic)
    addfunc(lib, "GetAcquisitionTimings", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)],
            argnames = ["exposure", "accumulate", "kinetic"] )
    #  ctypes.c_uint GetAdjustedRingExposureTimes(ctypes.c_int inumTimes, ctypes.POINTER(ctypes.c_float) fptimes)
    addfunc(lib, "GetAdjustedRingExposureTimes", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["inumTimes", "fptimes"] )
    #  ctypes.c_uint GetAllDMAData(ctypes.POINTER(ctypes.c_long) arr, ctypes.c_ulong size)
    addfunc(lib, "GetAllDMAData", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.c_ulong],
            argnames = ["arr", "size"] )
    #  ctypes.c_uint GetAmpDesc(ctypes.c_int index, ctypes.c_char_p name, ctypes.c_int length)
    addfunc(lib, "GetAmpDesc", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int],
            argnames = ["index", "name", "length"] )
    #  ctypes.c_uint GetAmpMaxSpeed(ctypes.c_int index, ctypes.POINTER(ctypes.c_float) speed)
    addfunc(lib, "GetAmpMaxSpeed", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["index", "speed"] )
    #  ctypes.c_uint GetAvailableCameras(ctypes.POINTER(ctypes.c_long) totalCameras)
    addfunc(lib, "GetAvailableCameras", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long)],
            argnames = ["totalCameras"] )
    #  ctypes.c_uint GetBackground(ctypes.POINTER(ctypes.c_long) arr, ctypes.c_ulong size)
    addfunc(lib, "GetBackground", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.c_ulong],
            argnames = ["arr", "size"] )
    #  ctypes.c_uint GetBaselineClamp(ctypes.POINTER(ctypes.c_int) state)
    addfunc(lib, "GetBaselineClamp", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["state"] )
    #  ctypes.c_uint GetBitDepth(ctypes.c_int channel, ctypes.POINTER(ctypes.c_int) depth)
    addfunc(lib, "GetBitDepth", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["channel", "depth"] )
    #  ctypes.c_uint GetBitsPerPixel(ctypes.c_int readout_index, ctypes.c_int index, ctypes.POINTER(ctypes.c_int) value)
    addfunc(lib, "GetBitsPerPixel", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["readout_index", "index", "value"] )
    #  ctypes.c_uint GetCameraEventStatus(ctypes.POINTER(DWORD) camStatus)
    addfunc(lib, "GetCameraEventStatus", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(DWORD)],
            argnames = ["camStatus"] )
    #  ctypes.c_uint GetCameraHandle(ctypes.c_long cameraIndex, ctypes.POINTER(ctypes.c_long) cameraHandle)
    addfunc(lib, "GetCameraHandle", restype = ctypes.c_uint,
            argtypes = [ctypes.c_long, ctypes.POINTER(ctypes.c_long)],
            argnames = ["cameraIndex", "cameraHandle"] )
    #  ctypes.c_uint GetCameraInformation(ctypes.c_int index, ctypes.POINTER(ctypes.c_long) information)
    addfunc(lib, "GetCameraInformation", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_long)],
            argnames = ["index", "information"] )
    #  ctypes.c_uint GetCameraSerialNumber(ctypes.POINTER(ctypes.c_int) number)
    addfunc(lib, "GetCameraSerialNumber", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["number"] )
    #  ctypes.c_uint GetCapabilities(ctypes.POINTER(AndorCapabilities) caps)
    addfunc(lib, "GetCapabilities", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(AndorCapabilities)],
            argnames = ["caps"] )
    #  ctypes.c_uint GetControllerCardModel(ctypes.c_char_p controllerCardModel)
    addfunc(lib, "GetControllerCardModel", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p],
            argnames = ["controllerCardModel"] )
    #  ctypes.c_uint GetCountConvertWavelengthRange(ctypes.POINTER(ctypes.c_float) minval, ctypes.POINTER(ctypes.c_float) maxval)
    addfunc(lib, "GetCountConvertWavelengthRange", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)],
            argnames = ["minval", "maxval"] )
    #  ctypes.c_uint GetCurrentCamera(ctypes.POINTER(ctypes.c_long) cameraHandle)
    addfunc(lib, "GetCurrentCamera", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long)],
            argnames = ["cameraHandle"] )
    #  ctypes.c_uint GetCYMGShift(ctypes.POINTER(ctypes.c_int) iXshift, ctypes.POINTER(ctypes.c_int) iYShift)
    addfunc(lib, "GetCYMGShift", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["iXshift", "iYShift"] )
    #  ctypes.c_uint GetDDGExternalOutputEnabled(ctypes.c_ulong uiIndex, ctypes.POINTER(ctypes.c_ulong) puiEnabled)
    addfunc(lib, "GetDDGExternalOutputEnabled", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["uiIndex", "puiEnabled"] )
    #  ctypes.c_uint GetDDGExternalOutputPolarity(ctypes.c_ulong uiIndex, ctypes.POINTER(ctypes.c_ulong) puiPolarity)
    addfunc(lib, "GetDDGExternalOutputPolarity", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["uiIndex", "puiPolarity"] )
    #  ctypes.c_uint GetDDGExternalOutputStepEnabled(ctypes.c_ulong uiIndex, ctypes.POINTER(ctypes.c_ulong) puiEnabled)
    addfunc(lib, "GetDDGExternalOutputStepEnabled", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["uiIndex", "puiEnabled"] )
    #  ctypes.c_uint GetDDGExternalOutputTime(ctypes.c_ulong uiIndex, ctypes.POINTER(ctypes.c_ulonglong) puiDelay, ctypes.POINTER(ctypes.c_ulonglong) puiWidth)
    addfunc(lib, "GetDDGExternalOutputTime", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_ulonglong)],
            argnames = ["uiIndex", "puiDelay", "puiWidth"] )
    #  ctypes.c_uint GetDDGTTLGateWidth(ctypes.c_ulonglong opticalWidth, ctypes.POINTER(ctypes.c_ulonglong) ttlWidth)
    addfunc(lib, "GetDDGTTLGateWidth", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_ulonglong)],
            argnames = ["opticalWidth", "ttlWidth"] )
    #  ctypes.c_uint GetDDGGateTime(ctypes.POINTER(ctypes.c_ulonglong) puiDelay, ctypes.POINTER(ctypes.c_ulonglong) puiWidth)
    addfunc(lib, "GetDDGGateTime", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_ulonglong)],
            argnames = ["puiDelay", "puiWidth"] )
    #  ctypes.c_uint GetDDGInsertionDelay(ctypes.POINTER(ctypes.c_int) piState)
    addfunc(lib, "GetDDGInsertionDelay", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["piState"] )
    #  ctypes.c_uint GetDDGIntelligate(ctypes.POINTER(ctypes.c_int) piState)
    addfunc(lib, "GetDDGIntelligate", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["piState"] )
    #  ctypes.c_uint GetDDGIOC(ctypes.POINTER(ctypes.c_int) state)
    addfunc(lib, "GetDDGIOC", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["state"] )
    #  ctypes.c_uint GetDDGIOCFrequency(ctypes.POINTER(ctypes.c_double) frequency)
    addfunc(lib, "GetDDGIOCFrequency", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_double)],
            argnames = ["frequency"] )
    #  ctypes.c_uint GetDDGIOCNumber(ctypes.POINTER(ctypes.c_ulong) numberPulses)
    addfunc(lib, "GetDDGIOCNumber", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["numberPulses"] )
    #  ctypes.c_uint GetDDGIOCNumberRequested(ctypes.POINTER(ctypes.c_ulong) pulses)
    addfunc(lib, "GetDDGIOCNumberRequested", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["pulses"] )
    #  ctypes.c_uint GetDDGIOCPeriod(ctypes.POINTER(ctypes.c_ulonglong) period)
    addfunc(lib, "GetDDGIOCPeriod", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ulonglong)],
            argnames = ["period"] )
    #  ctypes.c_uint GetDDGIOCPulses(ctypes.POINTER(ctypes.c_int) pulses)
    addfunc(lib, "GetDDGIOCPulses", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["pulses"] )
    #  ctypes.c_uint GetDDGIOCTrigger(ctypes.POINTER(ctypes.c_ulong) trigger)
    addfunc(lib, "GetDDGIOCTrigger", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["trigger"] )
    #  ctypes.c_uint GetDDGOpticalWidthEnabled(ctypes.POINTER(ctypes.c_ulong) puiEnabled)
    addfunc(lib, "GetDDGOpticalWidthEnabled", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["puiEnabled"] )
    #  ctypes.c_uint GetDDGLiteGlobalControlByte(ctypes.POINTER(ctypes.c_ubyte) control)
    addfunc(lib, "GetDDGLiteGlobalControlByte", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["control"] )
    #  ctypes.c_uint GetDDGLiteControlByte(ctypes.c_int channel, ctypes.POINTER(ctypes.c_ubyte) control)
    addfunc(lib, "GetDDGLiteControlByte", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte)],
            argnames = ["channel", "control"] )
    #  ctypes.c_uint GetDDGLiteInitialDelay(ctypes.c_int channel, ctypes.POINTER(ctypes.c_float) fDelay)
    addfunc(lib, "GetDDGLiteInitialDelay", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["channel", "fDelay"] )
    #  ctypes.c_uint GetDDGLitePulseWidth(ctypes.c_int channel, ctypes.POINTER(ctypes.c_float) fWidth)
    addfunc(lib, "GetDDGLitePulseWidth", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["channel", "fWidth"] )
    #  ctypes.c_uint GetDDGLiteInterPulseDelay(ctypes.c_int channel, ctypes.POINTER(ctypes.c_float) fDelay)
    addfunc(lib, "GetDDGLiteInterPulseDelay", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["channel", "fDelay"] )
    #  ctypes.c_uint GetDDGLitePulsesPerExposure(ctypes.c_int channel, ctypes.POINTER(ctypes.c_ulong) ui32Pulses)
    addfunc(lib, "GetDDGLitePulsesPerExposure", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["channel", "ui32Pulses"] )
    #  ctypes.c_uint GetDDGPulse(ctypes.c_double wid, ctypes.c_double resolution, ctypes.POINTER(ctypes.c_double) Delay, ctypes.POINTER(ctypes.c_double) Width)
    addfunc(lib, "GetDDGPulse", restype = ctypes.c_uint,
            argtypes = [ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)],
            argnames = ["wid", "resolution", "Delay", "Width"] )
    #  ctypes.c_uint GetDDGStepCoefficients(ctypes.c_ulong mode, ctypes.POINTER(ctypes.c_double) p1, ctypes.POINTER(ctypes.c_double) p2)
    addfunc(lib, "GetDDGStepCoefficients", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)],
            argnames = ["mode", "p1", "p2"] )
    #  ctypes.c_uint GetDDGWidthStepCoefficients(ctypes.c_ulong mode, ctypes.POINTER(ctypes.c_double) p1, ctypes.POINTER(ctypes.c_double) p2)
    addfunc(lib, "GetDDGWidthStepCoefficients", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)],
            argnames = ["mode", "p1", "p2"] )
    #  ctypes.c_uint GetDDGStepMode(ctypes.POINTER(ctypes.c_ulong) mode)
    addfunc(lib, "GetDDGStepMode", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["mode"] )
    #  ctypes.c_uint GetDDGWidthStepMode(ctypes.POINTER(ctypes.c_ulong) mode)
    addfunc(lib, "GetDDGWidthStepMode", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["mode"] )
    #  ctypes.c_uint GetDetector(ctypes.POINTER(ctypes.c_int) xpixels, ctypes.POINTER(ctypes.c_int) ypixels)
    addfunc(lib, "GetDetector", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["xpixels", "ypixels"] )
    #  ctypes.c_uint GetDICameraInfo(ctypes.c_void_p info)
    addfunc(lib, "GetDICameraInfo", restype = ctypes.c_uint,
            argtypes = [ctypes.c_void_p],
            argnames = ["info"] )
    #  ctypes.c_uint GetEMAdvanced(ctypes.POINTER(ctypes.c_int) state)
    addfunc(lib, "GetEMAdvanced", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["state"] )
    #  ctypes.c_uint GetEMCCDGain(ctypes.POINTER(ctypes.c_int) gain)
    addfunc(lib, "GetEMCCDGain", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["gain"] )
    #  ctypes.c_uint GetEMGainRange(ctypes.POINTER(ctypes.c_int) low, ctypes.POINTER(ctypes.c_int) high)
    addfunc(lib, "GetEMGainRange", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["low", "high"] )
    #  ctypes.c_uint GetESDEventStatus(ctypes.POINTER(DWORD) camStatus)
    addfunc(lib, "GetESDEventStatus", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(DWORD)],
            argnames = ["camStatus"] )
    #  ctypes.c_uint GetExternalTriggerTermination(ctypes.POINTER(ctypes.c_ulong) puiTermination)
    addfunc(lib, "GetExternalTriggerTermination", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["puiTermination"] )
    #  ctypes.c_uint GetFastestRecommendedVSSpeed(ctypes.POINTER(ctypes.c_int) index, ctypes.POINTER(ctypes.c_float) speed)
    addfunc(lib, "GetFastestRecommendedVSSpeed", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float)],
            argnames = ["index", "speed"] )
    #  ctypes.c_uint GetFIFOUsage(ctypes.POINTER(ctypes.c_int) FIFOusage)
    addfunc(lib, "GetFIFOUsage", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["FIFOusage"] )
    #  ctypes.c_uint GetFilterMode(ctypes.POINTER(ctypes.c_int) mode)
    addfunc(lib, "GetFilterMode", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["mode"] )
    #  ctypes.c_uint GetFKExposureTime(ctypes.POINTER(ctypes.c_float) time)
    addfunc(lib, "GetFKExposureTime", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float)],
            argnames = ["time"] )
    #  ctypes.c_uint GetFKVShiftSpeed(ctypes.c_int index, ctypes.POINTER(ctypes.c_int) speed)
    addfunc(lib, "GetFKVShiftSpeed", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["index", "speed"] )
    #  ctypes.c_uint GetFKVShiftSpeedF(ctypes.c_int index, ctypes.POINTER(ctypes.c_float) speed)
    addfunc(lib, "GetFKVShiftSpeedF", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["index", "speed"] )
    #  ctypes.c_uint GetFrontEndStatus(ctypes.POINTER(ctypes.c_int) piFlag)
    addfunc(lib, "GetFrontEndStatus", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["piFlag"] )
    #  ctypes.c_uint GetGateMode(ctypes.POINTER(ctypes.c_int) piGatemode)
    addfunc(lib, "GetGateMode", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["piGatemode"] )
    #  ctypes.c_uint GetHardwareVersion(ctypes.POINTER(ctypes.c_uint) PCB, ctypes.POINTER(ctypes.c_uint) Decode, ctypes.POINTER(ctypes.c_uint) dummy1, ctypes.POINTER(ctypes.c_uint) dummy2, ctypes.POINTER(ctypes.c_uint) CameraFirmwareVersion, ctypes.POINTER(ctypes.c_uint) CameraFirmwareBuild)
    addfunc(lib, "GetHardwareVersion", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)],
            argnames = ["PCB", "Decode", "dummy1", "dummy2", "CameraFirmwareVersion", "CameraFirmwareBuild"] )
    #  ctypes.c_uint GetHeadModel(ctypes.c_char_p name)
    addfunc(lib, "GetHeadModel", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p],
            argnames = ["name"] )
    #  ctypes.c_uint GetHorizontalSpeed(ctypes.c_int index, ctypes.POINTER(ctypes.c_int) speed)
    addfunc(lib, "GetHorizontalSpeed", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["index", "speed"] )
    #  ctypes.c_uint GetHSSpeed(ctypes.c_int channel, ctypes.c_int typ, ctypes.c_int index, ctypes.POINTER(ctypes.c_float) speed)
    addfunc(lib, "GetHSSpeed", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["channel", "typ", "index", "speed"] )
    #  ctypes.c_uint GetHVflag(ctypes.POINTER(ctypes.c_int) bFlag)
    addfunc(lib, "GetHVflag", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["bFlag"] )
    #  ctypes.c_uint GetID(ctypes.c_int devNum, ctypes.POINTER(ctypes.c_int) id)
    addfunc(lib, "GetID", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["devNum", "id"] )
    #  ctypes.c_uint GetImageFlip(ctypes.POINTER(ctypes.c_int) iHFlip, ctypes.POINTER(ctypes.c_int) iVFlip)
    addfunc(lib, "GetImageFlip", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["iHFlip", "iVFlip"] )
    #  ctypes.c_uint GetImageRotate(ctypes.POINTER(ctypes.c_int) iRotate)
    addfunc(lib, "GetImageRotate", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["iRotate"] )
    #  ctypes.c_uint GetImages(ctypes.c_long first, ctypes.c_long last, ctypes.POINTER(ctypes.c_long) arr, ctypes.c_ulong size, ctypes.POINTER(ctypes.c_long) validfirst, ctypes.POINTER(ctypes.c_long) validlast)
    addfunc(lib, "GetImages", restype = ctypes.c_uint,
            argtypes = [ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_ulong, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long)],
            argnames = ["first", "last", "arr", "size", "validfirst", "validlast"] )
    #  ctypes.c_uint GetImages16(ctypes.c_long first, ctypes.c_long last, ctypes.POINTER(WORD) arr, ctypes.c_ulong size, ctypes.POINTER(ctypes.c_long) validfirst, ctypes.POINTER(ctypes.c_long) validlast)
    addfunc(lib, "GetImages16", restype = ctypes.c_uint,
            argtypes = [ctypes.c_long, ctypes.c_long, ctypes.POINTER(WORD), ctypes.c_ulong, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long)],
            argnames = ["first", "last", "arr", "size", "validfirst", "validlast"] )
    #  ctypes.c_uint GetImagesPerDMA(ctypes.POINTER(ctypes.c_ulong) images)
    addfunc(lib, "GetImagesPerDMA", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["images"] )
    #  ctypes.c_uint GetIRQ(ctypes.POINTER(ctypes.c_int) IRQ)
    addfunc(lib, "GetIRQ", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["IRQ"] )
    #  ctypes.c_uint GetKeepCleanTime(ctypes.POINTER(ctypes.c_float) KeepCleanTime)
    addfunc(lib, "GetKeepCleanTime", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float)],
            argnames = ["KeepCleanTime"] )
    #  ctypes.c_uint GetMaximumBinning(ctypes.c_int ReadMode, ctypes.c_int HorzVert, ctypes.POINTER(ctypes.c_int) MaxBinning)
    addfunc(lib, "GetMaximumBinning", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["ReadMode", "HorzVert", "MaxBinning"] )
    #  ctypes.c_uint GetMaximumExposure(ctypes.POINTER(ctypes.c_float) MaxExp)
    addfunc(lib, "GetMaximumExposure", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float)],
            argnames = ["MaxExp"] )
    #  ctypes.c_uint GetMaximumNumberRingExposureTimes(ctypes.POINTER(ctypes.c_int) number)
    addfunc(lib, "GetMaximumNumberRingExposureTimes", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["number"] )
    #  ctypes.c_uint GetMCPGain(ctypes.POINTER(ctypes.c_int) piGain)
    addfunc(lib, "GetMCPGain", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["piGain"] )
    #  ctypes.c_uint GetMCPGainRange(ctypes.POINTER(ctypes.c_int) iLow, ctypes.POINTER(ctypes.c_int) iHigh)
    addfunc(lib, "GetMCPGainRange", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["iLow", "iHigh"] )
    #  ctypes.c_uint GetMCPGainTable(ctypes.c_int iNum, ctypes.POINTER(ctypes.c_int) piGain, ctypes.POINTER(ctypes.c_float) pfPhotoepc)
    addfunc(lib, "GetMCPGainTable", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float)],
            argnames = ["iNum", "piGain", "pfPhotoepc"] )
    #  ctypes.c_uint GetMCPVoltage(ctypes.POINTER(ctypes.c_int) iVoltage)
    addfunc(lib, "GetMCPVoltage", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["iVoltage"] )
    #  ctypes.c_uint GetMinimumImageLength(ctypes.POINTER(ctypes.c_int) MinImageLength)
    addfunc(lib, "GetMinimumImageLength", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["MinImageLength"] )
    #  ctypes.c_uint GetMinimumNumberInSeries(ctypes.POINTER(ctypes.c_int) number)
    addfunc(lib, "GetMinimumNumberInSeries", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["number"] )
    #  ctypes.c_uint GetMostRecentColorImage16(ctypes.c_ulong size, ctypes.c_int algorithm, ctypes.POINTER(WORD) red, ctypes.POINTER(WORD) green, ctypes.POINTER(WORD) blue)
    addfunc(lib, "GetMostRecentColorImage16", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["size", "algorithm", "red", "green", "blue"] )
    #  ctypes.c_uint GetMostRecentImage(ctypes.POINTER(ctypes.c_long) arr, ctypes.c_ulong size)
    addfunc(lib, "GetMostRecentImage", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.c_ulong],
            argnames = ["arr", "size"] )
    #  ctypes.c_uint GetMostRecentImage16(ctypes.POINTER(WORD) arr, ctypes.c_ulong size)
    addfunc(lib, "GetMostRecentImage16", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(WORD), ctypes.c_ulong],
            argnames = ["arr", "size"] )
    #  ctypes.c_uint GetMSTimingsData(ctypes.c_void_p TimeOfStart, ctypes.POINTER(ctypes.c_float) pfDifferences, ctypes.c_int inoOfImages)
    addfunc(lib, "GetMSTimingsData", restype = ctypes.c_uint,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.c_int],
            argnames = ["TimeOfStart", "pfDifferences", "inoOfImages"] )
    #  ctypes.c_uint GetMetaDataInfo(ctypes.c_void_p TimeOfStart, ctypes.POINTER(ctypes.c_float) pfTimeFromStart, ctypes.c_uint index)
    addfunc(lib, "GetMetaDataInfo", restype = ctypes.c_uint,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.c_uint],
            argnames = ["TimeOfStart", "pfTimeFromStart", "index"] )
    #  ctypes.c_uint GetMSTimingsEnabled()
    addfunc(lib, "GetMSTimingsEnabled", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint GetNewData(ctypes.POINTER(ctypes.c_long) arr, ctypes.c_ulong size)
    addfunc(lib, "GetNewData", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.c_ulong],
            argnames = ["arr", "size"] )
    #  ctypes.c_uint GetNewData16(ctypes.POINTER(WORD) arr, ctypes.c_ulong size)
    addfunc(lib, "GetNewData16", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(WORD), ctypes.c_ulong],
            argnames = ["arr", "size"] )
    #  ctypes.c_uint GetNewData8(ctypes.POINTER(ctypes.c_ubyte) arr, ctypes.c_ulong size)
    addfunc(lib, "GetNewData8", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ulong],
            argnames = ["arr", "size"] )
    #  ctypes.c_uint GetNewFloatData(ctypes.POINTER(ctypes.c_float) arr, ctypes.c_ulong size)
    addfunc(lib, "GetNewFloatData", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_ulong],
            argnames = ["arr", "size"] )
    #  ctypes.c_uint GetNumberADChannels(ctypes.POINTER(ctypes.c_int) channels)
    addfunc(lib, "GetNumberADChannels", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["channels"] )
    #  ctypes.c_uint GetNumberAmp(ctypes.POINTER(ctypes.c_int) amp)
    addfunc(lib, "GetNumberAmp", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["amp"] )
    #  ctypes.c_uint GetNumberAvailableImages(ctypes.POINTER(ctypes.c_long) first, ctypes.POINTER(ctypes.c_long) last)
    addfunc(lib, "GetNumberAvailableImages", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long)],
            argnames = ["first", "last"] )
    #  ctypes.c_uint GetNumberDDGExternalOutputs(ctypes.POINTER(ctypes.c_ulong) puiCount)
    addfunc(lib, "GetNumberDDGExternalOutputs", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["puiCount"] )
    #  ctypes.c_uint GetNumberDevices(ctypes.POINTER(ctypes.c_int) numDevs)
    addfunc(lib, "GetNumberDevices", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["numDevs"] )
    #  ctypes.c_uint GetNumberFKVShiftSpeeds(ctypes.POINTER(ctypes.c_int) number)
    addfunc(lib, "GetNumberFKVShiftSpeeds", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["number"] )
    #  ctypes.c_uint GetNumberHorizontalSpeeds(ctypes.POINTER(ctypes.c_int) number)
    addfunc(lib, "GetNumberHorizontalSpeeds", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["number"] )
    #  ctypes.c_uint GetNumberHSSpeeds(ctypes.c_int channel, ctypes.c_int typ, ctypes.POINTER(ctypes.c_int) speeds)
    addfunc(lib, "GetNumberHSSpeeds", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["channel", "typ", "speeds"] )
    #  ctypes.c_uint GetNumberMissedExternalTriggers(ctypes.c_uint first, ctypes.c_uint last, ctypes.POINTER(WORD) arr, ctypes.c_uint size)
    addfunc(lib, "GetNumberMissedExternalTriggers", restype = ctypes.c_uint,
            argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(WORD), ctypes.c_uint],
            argnames = ["first", "last", "arr", "size"] )
    #  ctypes.c_uint GetIRIGData(ctypes.POINTER(ctypes.c_ubyte) _uc_irigData, ctypes.c_uint _ui_index)
    addfunc(lib, "GetIRIGData", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint],
            argnames = ["_uc_irigData", "_ui_index"] )
    #  ctypes.c_uint GetMetaData(ctypes.POINTER(ctypes.c_ubyte) data, ctypes.c_uint _ui_index)
    addfunc(lib, "GetMetaData", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint],
            argnames = ["data", "_ui_index"] )
    #  ctypes.c_uint GetNumberNewImages(ctypes.POINTER(ctypes.c_long) first, ctypes.POINTER(ctypes.c_long) last)
    addfunc(lib, "GetNumberNewImages", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long)],
            argnames = ["first", "last"] )
    #  ctypes.c_uint GetNumberPhotonCountingDivisions(ctypes.POINTER(ctypes.c_ulong) noOfDivisions)
    addfunc(lib, "GetNumberPhotonCountingDivisions", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["noOfDivisions"] )
    #  ctypes.c_uint GetNumberPreAmpGains(ctypes.POINTER(ctypes.c_int) noGains)
    addfunc(lib, "GetNumberPreAmpGains", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["noGains"] )
    #  ctypes.c_uint GetNumberRingExposureTimes(ctypes.POINTER(ctypes.c_int) ipnumTimes)
    addfunc(lib, "GetNumberRingExposureTimes", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["ipnumTimes"] )
    #  ctypes.c_uint GetNumberIO(ctypes.POINTER(ctypes.c_int) iNumber)
    addfunc(lib, "GetNumberIO", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["iNumber"] )
    #  ctypes.c_uint GetNumberVerticalSpeeds(ctypes.POINTER(ctypes.c_int) number)
    addfunc(lib, "GetNumberVerticalSpeeds", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["number"] )
    #  ctypes.c_uint GetNumberVSAmplitudes(ctypes.POINTER(ctypes.c_int) number)
    addfunc(lib, "GetNumberVSAmplitudes", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["number"] )
    #  ctypes.c_uint GetNumberVSSpeeds(ctypes.POINTER(ctypes.c_int) speeds)
    addfunc(lib, "GetNumberVSSpeeds", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["speeds"] )
    #  ctypes.c_uint GetOldestImage(ctypes.POINTER(ctypes.c_long) arr, ctypes.c_ulong size)
    addfunc(lib, "GetOldestImage", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.c_ulong],
            argnames = ["arr", "size"] )
    #  ctypes.c_uint GetOldestImage16(ctypes.POINTER(WORD) arr, ctypes.c_ulong size)
    addfunc(lib, "GetOldestImage16", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(WORD), ctypes.c_ulong],
            argnames = ["arr", "size"] )
    #  ctypes.c_uint GetPhosphorStatus(ctypes.POINTER(ctypes.c_int) piFlag)
    addfunc(lib, "GetPhosphorStatus", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["piFlag"] )
    #  ctypes.c_uint GetPhysicalDMAAddress(ctypes.POINTER(ctypes.c_ulong) Address1, ctypes.POINTER(ctypes.c_ulong) Address2)
    addfunc(lib, "GetPhysicalDMAAddress", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong)],
            argnames = ["Address1", "Address2"] )
    #  ctypes.c_uint GetPixelSize(ctypes.POINTER(ctypes.c_float) xSize, ctypes.POINTER(ctypes.c_float) ySize)
    addfunc(lib, "GetPixelSize", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)],
            argnames = ["xSize", "ySize"] )
    #  ctypes.c_uint GetPreAmpGain(ctypes.c_int index, ctypes.POINTER(ctypes.c_float) gain)
    addfunc(lib, "GetPreAmpGain", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["index", "gain"] )
    #  ctypes.c_uint GetPreAmpGainText(ctypes.c_int index, ctypes.c_char_p name, ctypes.c_int length)
    addfunc(lib, "GetPreAmpGainText", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int],
            argnames = ["index", "name", "length"] )
    #  ctypes.c_uint GetCurrentPreAmpGain(ctypes.POINTER(ctypes.c_int) index, ctypes.c_char_p name, ctypes.c_int length)
    addfunc(lib, "GetCurrentPreAmpGain", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_char_p, ctypes.c_int],
            argnames = ["index", "name", "length"] )
    #  ctypes.c_uint GetDualExposureTimes(ctypes.POINTER(ctypes.c_float) exposure1, ctypes.POINTER(ctypes.c_float) exposure2)
    addfunc(lib, "GetDualExposureTimes", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)],
            argnames = ["exposure1", "exposure2"] )
    #  ctypes.c_uint GetQE(ctypes.c_char_p sensor, ctypes.c_float wavelength, ctypes.c_uint mode, ctypes.POINTER(ctypes.c_float) QE)
    addfunc(lib, "GetQE", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_float, ctypes.c_uint, ctypes.POINTER(ctypes.c_float)],
            argnames = ["sensor", "wavelength", "mode", "QE"] )
    #  ctypes.c_uint GetReadOutTime(ctypes.POINTER(ctypes.c_float) ReadOutTime)
    addfunc(lib, "GetReadOutTime", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float)],
            argnames = ["ReadOutTime"] )
    #  ctypes.c_uint GetRegisterDump(ctypes.POINTER(ctypes.c_int) mode)
    addfunc(lib, "GetRegisterDump", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["mode"] )
    #  ctypes.c_uint GetRelativeImageTimes(ctypes.c_uint first, ctypes.c_uint last, ctypes.POINTER(ctypes.c_ulonglong) arr, ctypes.c_uint size)
    addfunc(lib, "GetRelativeImageTimes", restype = ctypes.c_uint,
            argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_ulonglong), ctypes.c_uint],
            argnames = ["first", "last", "arr", "size"] )
    #  ctypes.c_uint GetRingExposureRange(ctypes.POINTER(ctypes.c_float) fpMin, ctypes.POINTER(ctypes.c_float) fpMax)
    addfunc(lib, "GetRingExposureRange", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)],
            argnames = ["fpMin", "fpMax"] )
    #  ctypes.c_uint GetSDK3Handle(ctypes.POINTER(ctypes.c_int) Handle)
    addfunc(lib, "GetSDK3Handle", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["Handle"] )
    #  ctypes.c_uint GetSensitivity(ctypes.c_int channel, ctypes.c_int horzShift, ctypes.c_int amplifier, ctypes.c_int pa, ctypes.POINTER(ctypes.c_float) sensitivity)
    addfunc(lib, "GetSensitivity", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["channel", "horzShift", "amplifier", "pa", "sensitivity"] )
    #  ctypes.c_uint GetShutterMinTimes(ctypes.POINTER(ctypes.c_int) minclosingtime, ctypes.POINTER(ctypes.c_int) minopeningtime)
    addfunc(lib, "GetShutterMinTimes", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["minclosingtime", "minopeningtime"] )
    #  ctypes.c_uint GetSizeOfCircularBuffer(ctypes.POINTER(ctypes.c_long) index)
    addfunc(lib, "GetSizeOfCircularBuffer", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long)],
            argnames = ["index"] )
    #  ctypes.c_uint GetSlotBusDeviceFunction(ctypes.POINTER(DWORD) dwslot, ctypes.POINTER(DWORD) dwBus, ctypes.POINTER(DWORD) dwDevice, ctypes.POINTER(DWORD) dwFunction)
    addfunc(lib, "GetSlotBusDeviceFunction", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(DWORD), ctypes.POINTER(DWORD), ctypes.POINTER(DWORD), ctypes.POINTER(DWORD)],
            argnames = ["dwslot", "dwBus", "dwDevice", "dwFunction"] )
    #  ctypes.c_uint GetSoftwareVersion(ctypes.POINTER(ctypes.c_uint) eprom, ctypes.POINTER(ctypes.c_uint) coffile, ctypes.POINTER(ctypes.c_uint) vxdrev, ctypes.POINTER(ctypes.c_uint) vxdver, ctypes.POINTER(ctypes.c_uint) dllrev, ctypes.POINTER(ctypes.c_uint) dllver)
    addfunc(lib, "GetSoftwareVersion", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)],
            argnames = ["eprom", "coffile", "vxdrev", "vxdver", "dllrev", "dllver"] )
    #  ctypes.c_uint GetSpoolProgress(ctypes.POINTER(ctypes.c_long) index)
    addfunc(lib, "GetSpoolProgress", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long)],
            argnames = ["index"] )
    #  ctypes.c_uint GetStartUpTime(ctypes.POINTER(ctypes.c_float) time)
    addfunc(lib, "GetStartUpTime", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float)],
            argnames = ["time"] )
    #  ctypes.c_uint GetStatus(ctypes.POINTER(ctypes.c_int) status)
    addfunc(lib, "GetStatus", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["status"] )
    #  ctypes.c_uint GetTECStatus(ctypes.POINTER(ctypes.c_int) piFlag)
    addfunc(lib, "GetTECStatus", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["piFlag"] )
    #  ctypes.c_uint GetTemperature(ctypes.POINTER(ctypes.c_int) temperature)
    addfunc(lib, "GetTemperature", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["temperature"] )
    #  ctypes.c_uint GetTemperatureF(ctypes.POINTER(ctypes.c_float) temperature)
    addfunc(lib, "GetTemperatureF", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float)],
            argnames = ["temperature"] )
    #  ctypes.c_uint GetTemperatureRange(ctypes.POINTER(ctypes.c_int) mintemp, ctypes.POINTER(ctypes.c_int) maxtemp)
    addfunc(lib, "GetTemperatureRange", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["mintemp", "maxtemp"] )
    #  ctypes.c_uint GetTemperaturePrecision(ctypes.POINTER(ctypes.c_int) precision)
    addfunc(lib, "GetTemperaturePrecision", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["precision"] )
    #  ctypes.c_uint GetTemperatureStatus(ctypes.POINTER(ctypes.c_float) SensorTemp, ctypes.POINTER(ctypes.c_float) TargetTemp, ctypes.POINTER(ctypes.c_float) AmbientTemp, ctypes.POINTER(ctypes.c_float) CoolerVolts)
    addfunc(lib, "GetTemperatureStatus", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)],
            argnames = ["SensorTemp", "TargetTemp", "AmbientTemp", "CoolerVolts"] )
    #  ctypes.c_uint GetTotalNumberImagesAcquired(ctypes.POINTER(ctypes.c_long) index)
    addfunc(lib, "GetTotalNumberImagesAcquired", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long)],
            argnames = ["index"] )
    #  ctypes.c_uint GetIODirection(ctypes.c_int index, ctypes.POINTER(ctypes.c_int) iDirection)
    addfunc(lib, "GetIODirection", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["index", "iDirection"] )
    #  ctypes.c_uint GetIOLevel(ctypes.c_int index, ctypes.POINTER(ctypes.c_int) iLevel)
    addfunc(lib, "GetIOLevel", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["index", "iLevel"] )
    #  ctypes.c_uint GetUSBDeviceDetails(ctypes.POINTER(WORD) VendorID, ctypes.POINTER(WORD) ProductID, ctypes.POINTER(WORD) FirmwareVersion, ctypes.POINTER(WORD) SpecificationNumber)
    addfunc(lib, "GetUSBDeviceDetails", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["VendorID", "ProductID", "FirmwareVersion", "SpecificationNumber"] )
    #  ctypes.c_uint GetVersionInfo(ctypes.c_int arr, ctypes.c_char_p szVersionInfo, ctypes.c_ulong ui32BufferLen)
    addfunc(lib, "GetVersionInfo", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_ulong],
            argnames = ["arr", "szVersionInfo", "ui32BufferLen"] )
    #  ctypes.c_uint GetVerticalSpeed(ctypes.c_int index, ctypes.POINTER(ctypes.c_int) speed)
    addfunc(lib, "GetVerticalSpeed", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["index", "speed"] )
    #  ctypes.c_uint GetVirtualDMAAddress(ctypes.POINTER(ctypes.c_void_p) Address1, ctypes.POINTER(ctypes.c_void_p) Address2)
    addfunc(lib, "GetVirtualDMAAddress", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p)],
            argnames = ["Address1", "Address2"] )
    #  ctypes.c_uint GetVSAmplitudeString(ctypes.c_int index, ctypes.c_char_p text)
    addfunc(lib, "GetVSAmplitudeString", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_char_p],
            argnames = ["index", "text"] )
    #  ctypes.c_uint GetVSAmplitudeFromString(ctypes.c_char_p text, ctypes.POINTER(ctypes.c_int) index)
    addfunc(lib, "GetVSAmplitudeFromString", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["text", "index"] )
    #  ctypes.c_uint GetVSAmplitudeValue(ctypes.c_int index, ctypes.POINTER(ctypes.c_int) value)
    addfunc(lib, "GetVSAmplitudeValue", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["index", "value"] )
    #  ctypes.c_uint GetVSSpeed(ctypes.c_int index, ctypes.POINTER(ctypes.c_float) speed)
    addfunc(lib, "GetVSSpeed", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["index", "speed"] )
    #  ctypes.c_uint GPIBReceive(ctypes.c_int id, ctypes.c_short address, ctypes.c_char_p text, ctypes.c_int size)
    addfunc(lib, "GPIBReceive", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_short, ctypes.c_char_p, ctypes.c_int],
            argnames = ["id", "address", "text", "size"] )
    #  ctypes.c_uint GPIBSend(ctypes.c_int id, ctypes.c_short address, ctypes.c_char_p text)
    addfunc(lib, "GPIBSend", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_short, ctypes.c_char_p],
            argnames = ["id", "address", "text"] )
    #  ctypes.c_uint I2CBurstRead(BYTE i2cAddress, ctypes.c_long nBytes, ctypes.POINTER(BYTE) data)
    addfunc(lib, "I2CBurstRead", restype = ctypes.c_uint,
            argtypes = [BYTE, ctypes.c_long, ctypes.POINTER(BYTE)],
            argnames = ["i2cAddress", "nBytes", "data"] )
    #  ctypes.c_uint I2CBurstWrite(BYTE i2cAddress, ctypes.c_long nBytes, ctypes.POINTER(BYTE) data)
    addfunc(lib, "I2CBurstWrite", restype = ctypes.c_uint,
            argtypes = [BYTE, ctypes.c_long, ctypes.POINTER(BYTE)],
            argnames = ["i2cAddress", "nBytes", "data"] )
    #  ctypes.c_uint I2CRead(BYTE deviceID, BYTE intAddress, ctypes.POINTER(BYTE) pdata)
    addfunc(lib, "I2CRead", restype = ctypes.c_uint,
            argtypes = [BYTE, BYTE, ctypes.POINTER(BYTE)],
            argnames = ["deviceID", "intAddress", "pdata"] )
    #  ctypes.c_uint I2CReset()
    addfunc(lib, "I2CReset", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint I2CWrite(BYTE deviceID, BYTE intAddress, BYTE data)
    addfunc(lib, "I2CWrite", restype = ctypes.c_uint,
            argtypes = [BYTE, BYTE, BYTE],
            argnames = ["deviceID", "intAddress", "data"] )
    #  ctypes.c_uint IdAndorDll()
    addfunc(lib, "IdAndorDll", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint InAuxPort(ctypes.c_int port, ctypes.POINTER(ctypes.c_int) state)
    addfunc(lib, "InAuxPort", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["port", "state"] )
    #  ctypes.c_uint Initialize(ctypes.c_char_p dir)
    addfunc(lib, "Initialize", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p],
            argnames = ["dir"] )
    #  ctypes.c_uint InitializeDevice(ctypes.c_char_p dir)
    addfunc(lib, "InitializeDevice", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p],
            argnames = ["dir"] )
    #  ctypes.c_uint IsAmplifierAvailable(ctypes.c_int iamp)
    addfunc(lib, "IsAmplifierAvailable", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["iamp"] )
    #  ctypes.c_uint IsCoolerOn(ctypes.POINTER(ctypes.c_int) iCoolerStatus)
    addfunc(lib, "IsCoolerOn", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["iCoolerStatus"] )
    #  ctypes.c_uint IsCountConvertModeAvailable(ctypes.c_int mode)
    addfunc(lib, "IsCountConvertModeAvailable", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint IsInternalMechanicalShutter(ctypes.POINTER(ctypes.c_int) InternalShutter)
    addfunc(lib, "IsInternalMechanicalShutter", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["InternalShutter"] )
    #  ctypes.c_uint IsPreAmpGainAvailable(ctypes.c_int channel, ctypes.c_int amplifier, ctypes.c_int index, ctypes.c_int pa, ctypes.POINTER(ctypes.c_int) status)
    addfunc(lib, "IsPreAmpGainAvailable", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["channel", "amplifier", "index", "pa", "status"] )
    #  ctypes.c_uint IsReadoutFlippedByAmplifier(ctypes.c_int iAmplifier, ctypes.POINTER(ctypes.c_int) iFlipped)
    addfunc(lib, "IsReadoutFlippedByAmplifier", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["iAmplifier", "iFlipped"] )
    #  ctypes.c_uint IsTriggerModeAvailable(ctypes.c_int iTriggerMode)
    addfunc(lib, "IsTriggerModeAvailable", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["iTriggerMode"] )
    #  ctypes.c_uint Merge(ctypes.POINTER(ctypes.c_long) arr, ctypes.c_long nOrder, ctypes.c_long nPoint, ctypes.c_long nPixel, ctypes.POINTER(ctypes.c_float) coeff, ctypes.c_long fit, ctypes.c_long hbin, ctypes.POINTER(ctypes.c_long) output, ctypes.POINTER(ctypes.c_float) start, ctypes.POINTER(ctypes.c_float) step_Renamed)
    addfunc(lib, "Merge", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_float), ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)],
            argnames = ["arr", "nOrder", "nPoint", "nPixel", "coeff", "fit", "hbin", "output", "start", "step_Renamed"] )
    #  ctypes.c_uint OutAuxPort(ctypes.c_int port, ctypes.c_int state)
    addfunc(lib, "OutAuxPort", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["port", "state"] )
    #  ctypes.c_uint PrepareAcquisition()
    addfunc(lib, "PrepareAcquisition", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint SaveAsBmp(ctypes.c_char_p path, ctypes.c_char_p palette, ctypes.c_long ymin, ctypes.c_long ymax)
    addfunc(lib, "SaveAsBmp", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_long, ctypes.c_long],
            argnames = ["path", "palette", "ymin", "ymax"] )
    #  ctypes.c_uint SaveAsCalibratedSif(ctypes.c_char_p path, ctypes.c_int x_data_type, ctypes.c_int x_unit, ctypes.POINTER(ctypes.c_float) x_cal, ctypes.c_float rayleighWavelength)
    addfunc(lib, "SaveAsCalibratedSif", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_float],
            argnames = ["path", "x_data_type", "x_unit", "x_cal", "rayleighWavelength"] )
    #  ctypes.c_uint SaveAsCommentedSif(ctypes.c_char_p path, ctypes.c_char_p comment)
    addfunc(lib, "SaveAsCommentedSif", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p],
            argnames = ["path", "comment"] )
    #  ctypes.c_uint SaveAsEDF(ctypes.c_char_p szPath, ctypes.c_int iMode)
    addfunc(lib, "SaveAsEDF", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_int],
            argnames = ["szPath", "iMode"] )
    #  ctypes.c_uint SaveAsFITS(ctypes.c_char_p szFileTitle, ctypes.c_int typ)
    addfunc(lib, "SaveAsFITS", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_int],
            argnames = ["szFileTitle", "typ"] )
    #  ctypes.c_uint SaveAsRaw(ctypes.c_char_p szFileTitle, ctypes.c_int typ)
    addfunc(lib, "SaveAsRaw", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_int],
            argnames = ["szFileTitle", "typ"] )
    #  ctypes.c_uint SaveAsSif(ctypes.c_char_p path)
    addfunc(lib, "SaveAsSif", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p],
            argnames = ["path"] )
    #  ctypes.c_uint SaveAsSPC(ctypes.c_char_p path)
    addfunc(lib, "SaveAsSPC", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p],
            argnames = ["path"] )
    #  ctypes.c_uint SaveAsTiff(ctypes.c_char_p path, ctypes.c_char_p palette, ctypes.c_int position, ctypes.c_int typ)
    addfunc(lib, "SaveAsTiff", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int],
            argnames = ["path", "palette", "position", "typ"] )
    #  ctypes.c_uint SaveAsTiffEx(ctypes.c_char_p path, ctypes.c_char_p palette, ctypes.c_int position, ctypes.c_int typ, ctypes.c_int mode)
    addfunc(lib, "SaveAsTiffEx", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["path", "palette", "position", "typ", "mode"] )
    #  ctypes.c_uint SaveEEPROMToFile(ctypes.c_char_p cFileName)
    addfunc(lib, "SaveEEPROMToFile", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p],
            argnames = ["cFileName"] )
    #  ctypes.c_uint SaveToClipBoard(ctypes.c_char_p palette)
    addfunc(lib, "SaveToClipBoard", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p],
            argnames = ["palette"] )
    #  ctypes.c_uint SelectDevice(ctypes.c_int devNum)
    addfunc(lib, "SelectDevice", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["devNum"] )
    #  ctypes.c_uint SendSoftwareTrigger()
    addfunc(lib, "SendSoftwareTrigger", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint SetAccumulationCycleTime(ctypes.c_float time)
    addfunc(lib, "SetAccumulationCycleTime", restype = ctypes.c_uint,
            argtypes = [ctypes.c_float],
            argnames = ["time"] )
    #  ctypes.c_uint SetAcqStatusEvent(HANDLE statusEvent)
    addfunc(lib, "SetAcqStatusEvent", restype = ctypes.c_uint,
            argtypes = [HANDLE],
            argnames = ["statusEvent"] )
    #  ctypes.c_uint SetAcquisitionMode(ctypes.c_int mode)
    addfunc(lib, "SetAcquisitionMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetSensorPortMode(ctypes.c_int mode)
    addfunc(lib, "SetSensorPortMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SelectSensorPort(ctypes.c_int port)
    addfunc(lib, "SelectSensorPort", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["port"] )
    #  ctypes.c_uint SetSizeOfCircularBufferMegaBytes(ctypes.c_ulong sizeMB)
    addfunc(lib, "SetSizeOfCircularBufferMegaBytes", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong],
            argnames = ["sizeMB"] )
    #  ctypes.c_uint SelectDualSensorPort(ctypes.c_int port)
    addfunc(lib, "SelectDualSensorPort", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["port"] )
    #  ctypes.c_uint SetAcquisitionType(ctypes.c_int typ)
    addfunc(lib, "SetAcquisitionType", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["typ"] )
    #  ctypes.c_uint SetADChannel(ctypes.c_int channel)
    addfunc(lib, "SetADChannel", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["channel"] )
    #  ctypes.c_uint SetAdvancedTriggerModeState(ctypes.c_int iState)
    addfunc(lib, "SetAdvancedTriggerModeState", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["iState"] )
    #  ctypes.c_uint SetBackground(ctypes.POINTER(ctypes.c_long) arr, ctypes.c_ulong size)
    addfunc(lib, "SetBackground", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.c_ulong],
            argnames = ["arr", "size"] )
    #  ctypes.c_uint SetBaselineClamp(ctypes.c_int state)
    addfunc(lib, "SetBaselineClamp", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["state"] )
    #  ctypes.c_uint SetBaselineOffset(ctypes.c_int offset)
    addfunc(lib, "SetBaselineOffset", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["offset"] )
    #  ctypes.c_uint SetBitsPerPixel(ctypes.c_int state)
    addfunc(lib, "SetBitsPerPixel", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["state"] )
    #  ctypes.c_uint SetCameraLinkMode(ctypes.c_int mode)
    addfunc(lib, "SetCameraLinkMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetCameraStatusEnable(DWORD Enable)
    addfunc(lib, "SetCameraStatusEnable", restype = ctypes.c_uint,
            argtypes = [DWORD],
            argnames = ["Enable"] )
    #  ctypes.c_uint SetChargeShifting(ctypes.c_uint NumberRows, ctypes.c_uint NumberRepeats)
    addfunc(lib, "SetChargeShifting", restype = ctypes.c_uint,
            argtypes = [ctypes.c_uint, ctypes.c_uint],
            argnames = ["NumberRows", "NumberRepeats"] )
    #  ctypes.c_uint SetComplexImage(ctypes.c_int numAreas, ctypes.POINTER(ctypes.c_int) areas)
    addfunc(lib, "SetComplexImage", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["numAreas", "areas"] )
    #  ctypes.c_uint SetCoolerMode(ctypes.c_int mode)
    addfunc(lib, "SetCoolerMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetCountConvertMode(ctypes.c_int Mode)
    addfunc(lib, "SetCountConvertMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["Mode"] )
    #  ctypes.c_uint SetCountConvertWavelength(ctypes.c_float wavelength)
    addfunc(lib, "SetCountConvertWavelength", restype = ctypes.c_uint,
            argtypes = [ctypes.c_float],
            argnames = ["wavelength"] )
    #  ctypes.c_uint SetCropMode(ctypes.c_int active, ctypes.c_int cropHeight, ctypes.c_int reserved)
    addfunc(lib, "SetCropMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["active", "cropHeight", "reserved"] )
    #  ctypes.c_uint SetCurrentCamera(ctypes.c_long cameraHandle)
    addfunc(lib, "SetCurrentCamera", restype = ctypes.c_uint,
            argtypes = [ctypes.c_long],
            argnames = ["cameraHandle"] )
    #  ctypes.c_uint SetCustomTrackHBin(ctypes.c_int bin)
    addfunc(lib, "SetCustomTrackHBin", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["bin"] )
    #  ctypes.c_uint SetDataType(ctypes.c_int typ)
    addfunc(lib, "SetDataType", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["typ"] )
    #  ctypes.c_uint SetDACOutput(ctypes.c_int iOption, ctypes.c_int iResolution, ctypes.c_int iValue)
    addfunc(lib, "SetDACOutput", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["iOption", "iResolution", "iValue"] )
    #  ctypes.c_uint SetDACOutputScale(ctypes.c_int iScale)
    addfunc(lib, "SetDACOutputScale", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["iScale"] )
    #  ctypes.c_uint SetDDGAddress(BYTE t0, BYTE t1, BYTE t2, BYTE t3, BYTE address)
    addfunc(lib, "SetDDGAddress", restype = ctypes.c_uint,
            argtypes = [BYTE, BYTE, BYTE, BYTE, BYTE],
            argnames = ["t0", "t1", "t2", "t3", "address"] )
    #  ctypes.c_uint SetDDGExternalOutputEnabled(ctypes.c_ulong uiIndex, ctypes.c_ulong uiEnabled)
    addfunc(lib, "SetDDGExternalOutputEnabled", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong, ctypes.c_ulong],
            argnames = ["uiIndex", "uiEnabled"] )
    #  ctypes.c_uint SetDDGExternalOutputPolarity(ctypes.c_ulong uiIndex, ctypes.c_ulong uiPolarity)
    addfunc(lib, "SetDDGExternalOutputPolarity", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong, ctypes.c_ulong],
            argnames = ["uiIndex", "uiPolarity"] )
    #  ctypes.c_uint SetDDGExternalOutputStepEnabled(ctypes.c_ulong uiIndex, ctypes.c_ulong uiEnabled)
    addfunc(lib, "SetDDGExternalOutputStepEnabled", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong, ctypes.c_ulong],
            argnames = ["uiIndex", "uiEnabled"] )
    #  ctypes.c_uint SetDDGExternalOutputTime(ctypes.c_ulong uiIndex, ctypes.c_ulonglong uiDelay, ctypes.c_ulonglong uiWidth)
    addfunc(lib, "SetDDGExternalOutputTime", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong, ctypes.c_ulonglong, ctypes.c_ulonglong],
            argnames = ["uiIndex", "uiDelay", "uiWidth"] )
    #  ctypes.c_uint SetDDGGain(ctypes.c_int gain)
    addfunc(lib, "SetDDGGain", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["gain"] )
    #  ctypes.c_uint SetDDGGateStep(ctypes.c_double step_Renamed)
    addfunc(lib, "SetDDGGateStep", restype = ctypes.c_uint,
            argtypes = [ctypes.c_double],
            argnames = ["step_Renamed"] )
    #  ctypes.c_uint SetDDGGateTime(ctypes.c_ulonglong uiDelay, ctypes.c_ulonglong uiWidth)
    addfunc(lib, "SetDDGGateTime", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulonglong, ctypes.c_ulonglong],
            argnames = ["uiDelay", "uiWidth"] )
    #  ctypes.c_uint SetDDGInsertionDelay(ctypes.c_int state)
    addfunc(lib, "SetDDGInsertionDelay", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["state"] )
    #  ctypes.c_uint SetDDGIntelligate(ctypes.c_int state)
    addfunc(lib, "SetDDGIntelligate", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["state"] )
    #  ctypes.c_uint SetDDGIOC(ctypes.c_int state)
    addfunc(lib, "SetDDGIOC", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["state"] )
    #  ctypes.c_uint SetDDGIOCFrequency(ctypes.c_double frequency)
    addfunc(lib, "SetDDGIOCFrequency", restype = ctypes.c_uint,
            argtypes = [ctypes.c_double],
            argnames = ["frequency"] )
    #  ctypes.c_uint SetDDGIOCNumber(ctypes.c_ulong numberPulses)
    addfunc(lib, "SetDDGIOCNumber", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong],
            argnames = ["numberPulses"] )
    #  ctypes.c_uint SetDDGIOCPeriod(ctypes.c_ulonglong period)
    addfunc(lib, "SetDDGIOCPeriod", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulonglong],
            argnames = ["period"] )
    #  ctypes.c_uint SetDDGIOCTrigger(ctypes.c_ulong trigger)
    addfunc(lib, "SetDDGIOCTrigger", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong],
            argnames = ["trigger"] )
    #  ctypes.c_uint SetDDGOpticalWidthEnabled(ctypes.c_ulong uiEnabled)
    addfunc(lib, "SetDDGOpticalWidthEnabled", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong],
            argnames = ["uiEnabled"] )
    #  ctypes.c_uint SetDDGLiteGlobalControlByte(ctypes.c_ubyte control)
    addfunc(lib, "SetDDGLiteGlobalControlByte", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ubyte],
            argnames = ["control"] )
    #  ctypes.c_uint SetDDGLiteControlByte(ctypes.c_int channel, ctypes.c_ubyte control)
    addfunc(lib, "SetDDGLiteControlByte", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_ubyte],
            argnames = ["channel", "control"] )
    #  ctypes.c_uint SetDDGLiteInitialDelay(ctypes.c_int channel, ctypes.c_float fDelay)
    addfunc(lib, "SetDDGLiteInitialDelay", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_float],
            argnames = ["channel", "fDelay"] )
    #  ctypes.c_uint SetDDGLitePulseWidth(ctypes.c_int channel, ctypes.c_float fWidth)
    addfunc(lib, "SetDDGLitePulseWidth", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_float],
            argnames = ["channel", "fWidth"] )
    #  ctypes.c_uint SetDDGLiteInterPulseDelay(ctypes.c_int channel, ctypes.c_float fDelay)
    addfunc(lib, "SetDDGLiteInterPulseDelay", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_float],
            argnames = ["channel", "fDelay"] )
    #  ctypes.c_uint SetDDGLitePulsesPerExposure(ctypes.c_int channel, ctypes.c_ulong ui32Pulses)
    addfunc(lib, "SetDDGLitePulsesPerExposure", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_ulong],
            argnames = ["channel", "ui32Pulses"] )
    #  ctypes.c_uint SetDDGStepCoefficients(ctypes.c_ulong mode, ctypes.c_double p1, ctypes.c_double p2)
    addfunc(lib, "SetDDGStepCoefficients", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong, ctypes.c_double, ctypes.c_double],
            argnames = ["mode", "p1", "p2"] )
    #  ctypes.c_uint SetDDGWidthStepCoefficients(ctypes.c_ulong mode, ctypes.c_double p1, ctypes.c_double p2)
    addfunc(lib, "SetDDGWidthStepCoefficients", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong, ctypes.c_double, ctypes.c_double],
            argnames = ["mode", "p1", "p2"] )
    #  ctypes.c_uint SetDDGStepMode(ctypes.c_ulong mode)
    addfunc(lib, "SetDDGStepMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong],
            argnames = ["mode"] )
    #  ctypes.c_uint SetDDGWidthStepMode(ctypes.c_ulong mode)
    addfunc(lib, "SetDDGWidthStepMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong],
            argnames = ["mode"] )
    #  ctypes.c_uint SetDDGTimes(ctypes.c_double t0, ctypes.c_double t1, ctypes.c_double t2)
    addfunc(lib, "SetDDGTimes", restype = ctypes.c_uint,
            argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double],
            argnames = ["t0", "t1", "t2"] )
    #  ctypes.c_uint SetDDGTriggerMode(ctypes.c_int mode)
    addfunc(lib, "SetDDGTriggerMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetDDGVariableGateStep(ctypes.c_int mode, ctypes.c_double p1, ctypes.c_double p2)
    addfunc(lib, "SetDDGVariableGateStep", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double],
            argnames = ["mode", "p1", "p2"] )
    #  ctypes.c_uint SetDelayGenerator(ctypes.c_int board, ctypes.c_short address, ctypes.c_int typ)
    addfunc(lib, "SetDelayGenerator", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_short, ctypes.c_int],
            argnames = ["board", "address", "typ"] )
    #  ctypes.c_uint SetDMAParameters(ctypes.c_int MaxImagesPerDMA, ctypes.c_float SecondsPerDMA)
    addfunc(lib, "SetDMAParameters", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_float],
            argnames = ["MaxImagesPerDMA", "SecondsPerDMA"] )
    #  ctypes.c_uint SetDriverEvent(HANDLE driverEvent)
    addfunc(lib, "SetDriverEvent", restype = ctypes.c_uint,
            argtypes = [HANDLE],
            argnames = ["driverEvent"] )
    #  ctypes.c_uint SetESDEvent(HANDLE esdEvent)
    addfunc(lib, "SetESDEvent", restype = ctypes.c_uint,
            argtypes = [HANDLE],
            argnames = ["esdEvent"] )
    #  ctypes.c_uint SetEMAdvanced(ctypes.c_int state)
    addfunc(lib, "SetEMAdvanced", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["state"] )
    #  ctypes.c_uint SetEMCCDGain(ctypes.c_int gain)
    addfunc(lib, "SetEMCCDGain", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["gain"] )
    #  ctypes.c_uint SetEMClockCompensation(ctypes.c_int EMClockCompensationFlag)
    addfunc(lib, "SetEMClockCompensation", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["EMClockCompensationFlag"] )
    #  ctypes.c_uint SetEMGainMode(ctypes.c_int mode)
    addfunc(lib, "SetEMGainMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetExposureTime(ctypes.c_float time)
    addfunc(lib, "SetExposureTime", restype = ctypes.c_uint,
            argtypes = [ctypes.c_float],
            argnames = ["time"] )
    #  ctypes.c_uint SetExternalTriggerTermination(ctypes.c_ulong uiTermination)
    addfunc(lib, "SetExternalTriggerTermination", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong],
            argnames = ["uiTermination"] )
    #  ctypes.c_uint SetFanMode(ctypes.c_int mode)
    addfunc(lib, "SetFanMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetFastExtTrigger(ctypes.c_int mode)
    addfunc(lib, "SetFastExtTrigger", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetFastKinetics(ctypes.c_int exposedRows, ctypes.c_int seriesLength, ctypes.c_float time, ctypes.c_int mode, ctypes.c_int hbin, ctypes.c_int vbin)
    addfunc(lib, "SetFastKinetics", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["exposedRows", "seriesLength", "time", "mode", "hbin", "vbin"] )
    #  ctypes.c_uint SetFastKineticsEx(ctypes.c_int exposedRows, ctypes.c_int seriesLength, ctypes.c_float time, ctypes.c_int mode, ctypes.c_int hbin, ctypes.c_int vbin, ctypes.c_int offset)
    addfunc(lib, "SetFastKineticsEx", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["exposedRows", "seriesLength", "time", "mode", "hbin", "vbin", "offset"] )
    #  ctypes.c_uint SetFastKineticsStorageMode(ctypes.c_int mode)
    addfunc(lib, "SetFastKineticsStorageMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetFastKineticsTimeScanMode(ctypes.c_int rows, ctypes.c_int tracks, ctypes.c_int mode)
    addfunc(lib, "SetFastKineticsTimeScanMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["rows", "tracks", "mode"] )
    #  ctypes.c_uint SetFilterMode(ctypes.c_int mode)
    addfunc(lib, "SetFilterMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetFilterParameters(ctypes.c_int width, ctypes.c_float sensitivity, ctypes.c_int range, ctypes.c_float accept, ctypes.c_int smooth, ctypes.c_int noise)
    addfunc(lib, "SetFilterParameters", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_float, ctypes.c_int, ctypes.c_float, ctypes.c_int, ctypes.c_int],
            argnames = ["width", "sensitivity", "range", "accept", "smooth", "noise"] )
    #  ctypes.c_uint SetFKVShiftSpeed(ctypes.c_int index)
    addfunc(lib, "SetFKVShiftSpeed", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["index"] )
    #  ctypes.c_uint SetFPDP(ctypes.c_int state)
    addfunc(lib, "SetFPDP", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["state"] )
    #  ctypes.c_uint SetFrameTransferMode(ctypes.c_int mode)
    addfunc(lib, "SetFrameTransferMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetFrontEndEvent(HANDLE driverEvent)
    addfunc(lib, "SetFrontEndEvent", restype = ctypes.c_uint,
            argtypes = [HANDLE],
            argnames = ["driverEvent"] )
    #  ctypes.c_uint SetFullImage(ctypes.c_int hbin, ctypes.c_int vbin)
    addfunc(lib, "SetFullImage", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["hbin", "vbin"] )
    #  ctypes.c_uint SetFVBHBin(ctypes.c_int bin)
    addfunc(lib, "SetFVBHBin", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["bin"] )
    #  ctypes.c_uint SetGain(ctypes.c_int gain)
    addfunc(lib, "SetGain", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["gain"] )
    #  ctypes.c_uint SetGate(ctypes.c_float delay, ctypes.c_float width, ctypes.c_float stepRenamed)
    addfunc(lib, "SetGate", restype = ctypes.c_uint,
            argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float],
            argnames = ["delay", "width", "stepRenamed"] )
    #  ctypes.c_uint SetGateMode(ctypes.c_int gatemode)
    addfunc(lib, "SetGateMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["gatemode"] )
    #  ctypes.c_uint SetHighCapacity(ctypes.c_int state)
    addfunc(lib, "SetHighCapacity", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["state"] )
    #  ctypes.c_uint SetHorizontalSpeed(ctypes.c_int index)
    addfunc(lib, "SetHorizontalSpeed", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["index"] )
    #  ctypes.c_uint SetHSSpeed(ctypes.c_int typ, ctypes.c_int index)
    addfunc(lib, "SetHSSpeed", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["typ", "index"] )
    #  ctypes.c_uint SetImage(ctypes.c_int hbin, ctypes.c_int vbin, ctypes.c_int hstart, ctypes.c_int hend, ctypes.c_int vstart, ctypes.c_int vend)
    addfunc(lib, "SetImage", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["hbin", "vbin", "hstart", "hend", "vstart", "vend"] )
    #  ctypes.c_uint SetImageFlip(ctypes.c_int iHFlip, ctypes.c_int iVFlip)
    addfunc(lib, "SetImageFlip", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["iHFlip", "iVFlip"] )
    #  ctypes.c_uint SetImageRotate(ctypes.c_int iRotate)
    addfunc(lib, "SetImageRotate", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["iRotate"] )
    #  ctypes.c_uint SetIsolatedCropMode(ctypes.c_int active, ctypes.c_int cropheight, ctypes.c_int cropwidth, ctypes.c_int vbin, ctypes.c_int hbin)
    addfunc(lib, "SetIsolatedCropMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["active", "cropheight", "cropwidth", "vbin", "hbin"] )
    #  ctypes.c_uint SetIsolatedCropModeEx(ctypes.c_int active, ctypes.c_int cropheight, ctypes.c_int cropwidth, ctypes.c_int vbin, ctypes.c_int hbin, ctypes.c_int cropleft, ctypes.c_int cropbottom)
    addfunc(lib, "SetIsolatedCropModeEx", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["active", "cropheight", "cropwidth", "vbin", "hbin", "cropleft", "cropbottom"] )
    #  ctypes.c_uint SetIsolatedCropModeType(ctypes.c_int type)
    addfunc(lib, "SetIsolatedCropModeType", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["type"] )
    #  ctypes.c_uint SetKineticCycleTime(ctypes.c_float time)
    addfunc(lib, "SetKineticCycleTime", restype = ctypes.c_uint,
            argtypes = [ctypes.c_float],
            argnames = ["time"] )
    #  ctypes.c_uint SetMCPGain(ctypes.c_int gain)
    addfunc(lib, "SetMCPGain", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["gain"] )
    #  ctypes.c_uint SetMCPGating(ctypes.c_int gating)
    addfunc(lib, "SetMCPGating", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["gating"] )
    #  ctypes.c_uint SetMessageWindow(HWND wnd)
    addfunc(lib, "SetMessageWindow", restype = ctypes.c_uint,
            argtypes = [HWND],
            argnames = ["wnd"] )
    #  ctypes.c_uint SetMetaData(ctypes.c_int state)
    addfunc(lib, "SetMetaData", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["state"] )
    #  ctypes.c_uint SetMultiTrack(ctypes.c_int number, ctypes.c_int height, ctypes.c_int offset, ctypes.POINTER(ctypes.c_int) bottom, ctypes.POINTER(ctypes.c_int) gap)
    addfunc(lib, "SetMultiTrack", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["number", "height", "offset", "bottom", "gap"] )
    #  ctypes.c_uint SetMultiTrackHBin(ctypes.c_int bin)
    addfunc(lib, "SetMultiTrackHBin", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["bin"] )
    #  ctypes.c_uint SetMultiTrackHRange(ctypes.c_int iStart, ctypes.c_int iEnd)
    addfunc(lib, "SetMultiTrackHRange", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["iStart", "iEnd"] )
    #  ctypes.c_uint SetMultiTrackScan(ctypes.c_int trackHeight, ctypes.c_int numberTracks, ctypes.c_int iSIHStart, ctypes.c_int iSIHEnd, ctypes.c_int trackHBinning, ctypes.c_int trackVBinning, ctypes.c_int trackGap, ctypes.c_int trackOffset, ctypes.c_int trackSkip, ctypes.c_int numberSubFrames)
    addfunc(lib, "SetMultiTrackScan", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["trackHeight", "numberTracks", "iSIHStart", "iSIHEnd", "trackHBinning", "trackVBinning", "trackGap", "trackOffset", "trackSkip", "numberSubFrames"] )
    #  ctypes.c_uint SetNextAddress(ctypes.POINTER(ctypes.c_long) data, ctypes.c_long lowAdd, ctypes.c_long highAdd, ctypes.c_long length, ctypes.c_long physical)
    addfunc(lib, "SetNextAddress", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long],
            argnames = ["data", "lowAdd", "highAdd", "length", "physical"] )
    #  ctypes.c_uint SetNextAddress16(ctypes.POINTER(ctypes.c_long) data, ctypes.c_long lowAdd, ctypes.c_long highAdd, ctypes.c_long length, ctypes.c_long physical)
    addfunc(lib, "SetNextAddress16", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long],
            argnames = ["data", "lowAdd", "highAdd", "length", "physical"] )
    #  ctypes.c_uint SetNumberAccumulations(ctypes.c_int number)
    addfunc(lib, "SetNumberAccumulations", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["number"] )
    #  ctypes.c_uint SetNumberKinetics(ctypes.c_int number)
    addfunc(lib, "SetNumberKinetics", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["number"] )
    #  ctypes.c_uint SetNumberPrescans(ctypes.c_int iNumber)
    addfunc(lib, "SetNumberPrescans", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["iNumber"] )
    #  ctypes.c_uint SetOutputAmplifier(ctypes.c_int typ)
    addfunc(lib, "SetOutputAmplifier", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["typ"] )
    #  ctypes.c_uint SetOverlapMode(ctypes.c_int mode)
    addfunc(lib, "SetOverlapMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetOverTempEvent(HANDLE tempEvent)
    addfunc(lib, "SetOverTempEvent", restype = ctypes.c_uint,
            argtypes = [HANDLE],
            argnames = ["tempEvent"] )
    #  ctypes.c_uint SetPCIMode(ctypes.c_int mode, ctypes.c_int value)
    addfunc(lib, "SetPCIMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["mode", "value"] )
    #  ctypes.c_uint SetPhotonCounting(ctypes.c_int state)
    addfunc(lib, "SetPhotonCounting", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["state"] )
    #  ctypes.c_uint SetPhotonCountingThreshold(ctypes.c_long min, ctypes.c_long max)
    addfunc(lib, "SetPhotonCountingThreshold", restype = ctypes.c_uint,
            argtypes = [ctypes.c_long, ctypes.c_long],
            argnames = ["min", "max"] )
    #  ctypes.c_uint SetPhosphorEvent(HANDLE driverEvent)
    addfunc(lib, "SetPhosphorEvent", restype = ctypes.c_uint,
            argtypes = [HANDLE],
            argnames = ["driverEvent"] )
    #  ctypes.c_uint SetPhotonCountingDivisions(ctypes.c_ulong noOfDivisions, ctypes.POINTER(ctypes.c_long) divisions)
    addfunc(lib, "SetPhotonCountingDivisions", restype = ctypes.c_uint,
            argtypes = [ctypes.c_ulong, ctypes.POINTER(ctypes.c_long)],
            argnames = ["noOfDivisions", "divisions"] )
    #  ctypes.c_uint SetPixelMode(ctypes.c_int bitdepth, ctypes.c_int colormode)
    addfunc(lib, "SetPixelMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["bitdepth", "colormode"] )
    #  ctypes.c_uint SetPreAmpGain(ctypes.c_int index)
    addfunc(lib, "SetPreAmpGain", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["index"] )
    #  ctypes.c_uint SetDualExposureTimes(ctypes.c_float expTime1, ctypes.c_float expTime2)
    addfunc(lib, "SetDualExposureTimes", restype = ctypes.c_uint,
            argtypes = [ctypes.c_float, ctypes.c_float],
            argnames = ["expTime1", "expTime2"] )
    #  ctypes.c_uint SetDualExposureMode(ctypes.c_int mode)
    addfunc(lib, "SetDualExposureMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetRandomTracks(ctypes.c_int numTracks, ctypes.POINTER(ctypes.c_int) areas)
    addfunc(lib, "SetRandomTracks", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["numTracks", "areas"] )
    #  ctypes.c_uint SetReadMode(ctypes.c_int mode)
    addfunc(lib, "SetReadMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetReadoutRegisterPacking(ctypes.c_uint mode)
    addfunc(lib, "SetReadoutRegisterPacking", restype = ctypes.c_uint,
            argtypes = [ctypes.c_uint],
            argnames = ["mode"] )
    #  ctypes.c_uint SetRegisterDump(ctypes.c_int mode)
    addfunc(lib, "SetRegisterDump", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetRingExposureTimes(ctypes.c_int numTimes, ctypes.POINTER(ctypes.c_float) times)
    addfunc(lib, "SetRingExposureTimes", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["numTimes", "times"] )
    #  ctypes.c_uint SetSaturationEvent(HANDLE saturationEvent)
    addfunc(lib, "SetSaturationEvent", restype = ctypes.c_uint,
            argtypes = [HANDLE],
            argnames = ["saturationEvent"] )
    #  ctypes.c_uint SetShutter(ctypes.c_int typ, ctypes.c_int mode, ctypes.c_int closingtime, ctypes.c_int openingtime)
    addfunc(lib, "SetShutter", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["typ", "mode", "closingtime", "openingtime"] )
    #  ctypes.c_uint SetShutterEx(ctypes.c_int typ, ctypes.c_int mode, ctypes.c_int closingtime, ctypes.c_int openingtime, ctypes.c_int extmode)
    addfunc(lib, "SetShutterEx", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["typ", "mode", "closingtime", "openingtime", "extmode"] )
    #  ctypes.c_uint SetShutters(ctypes.c_int typ, ctypes.c_int mode, ctypes.c_int closingtime, ctypes.c_int openingtime, ctypes.c_int exttype, ctypes.c_int extmode, ctypes.c_int dummy1, ctypes.c_int dummy2)
    addfunc(lib, "SetShutters", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["typ", "mode", "closingtime", "openingtime", "exttype", "extmode", "dummy1", "dummy2"] )
    #  ctypes.c_uint SetSifComment(ctypes.c_char_p comment)
    addfunc(lib, "SetSifComment", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p],
            argnames = ["comment"] )
    #  ctypes.c_uint SetSingleTrack(ctypes.c_int centre, ctypes.c_int height)
    addfunc(lib, "SetSingleTrack", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["centre", "height"] )
    #  ctypes.c_uint SetSingleTrackHBin(ctypes.c_int bin)
    addfunc(lib, "SetSingleTrackHBin", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["bin"] )
    #  ctypes.c_uint SetSpool(ctypes.c_int active, ctypes.c_int method, ctypes.c_char_p path, ctypes.c_int framebuffersize)
    addfunc(lib, "SetSpool", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int],
            argnames = ["active", "method", "path", "framebuffersize"] )
    #  ctypes.c_uint SetSpoolThreadCount(ctypes.c_int count)
    addfunc(lib, "SetSpoolThreadCount", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["count"] )
    #  ctypes.c_uint SetStorageMode(ctypes.c_long mode)
    addfunc(lib, "SetStorageMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_long],
            argnames = ["mode"] )
    #  ctypes.c_uint SetTECEvent(HANDLE driverEvent)
    addfunc(lib, "SetTECEvent", restype = ctypes.c_uint,
            argtypes = [HANDLE],
            argnames = ["driverEvent"] )
    #  ctypes.c_uint SetTemperature(ctypes.c_int temperature)
    addfunc(lib, "SetTemperature", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["temperature"] )
    #  ctypes.c_uint SetTemperatureEvent(HANDLE temperatureEvent)
    addfunc(lib, "SetTemperatureEvent", restype = ctypes.c_uint,
            argtypes = [HANDLE],
            argnames = ["temperatureEvent"] )
    #  ctypes.c_uint SetTriggerMode(ctypes.c_int mode)
    addfunc(lib, "SetTriggerMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint SetTriggerInvert(ctypes.c_int mode)
    addfunc(lib, "SetTriggerInvert", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint GetTriggerLevelRange(ctypes.POINTER(ctypes.c_float) minimum, ctypes.POINTER(ctypes.c_float) maximum)
    addfunc(lib, "GetTriggerLevelRange", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)],
            argnames = ["minimum", "maximum"] )
    #  ctypes.c_uint SetTriggerLevel(ctypes.c_float f_level)
    addfunc(lib, "SetTriggerLevel", restype = ctypes.c_uint,
            argtypes = [ctypes.c_float],
            argnames = ["f_level"] )
    #  ctypes.c_uint SetIODirection(ctypes.c_int index, ctypes.c_int iDirection)
    addfunc(lib, "SetIODirection", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["index", "iDirection"] )
    #  ctypes.c_uint SetIOLevel(ctypes.c_int index, ctypes.c_int iLevel)
    addfunc(lib, "SetIOLevel", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["index", "iLevel"] )
    #  ctypes.c_uint SetUserEvent(HANDLE userEvent)
    addfunc(lib, "SetUserEvent", restype = ctypes.c_uint,
            argtypes = [HANDLE],
            argnames = ["userEvent"] )
    #  ctypes.c_uint SetUSGenomics(ctypes.c_long width, ctypes.c_long height)
    addfunc(lib, "SetUSGenomics", restype = ctypes.c_uint,
            argtypes = [ctypes.c_long, ctypes.c_long],
            argnames = ["width", "height"] )
    #  ctypes.c_uint SetVerticalRowBuffer(ctypes.c_int rows)
    addfunc(lib, "SetVerticalRowBuffer", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["rows"] )
    #  ctypes.c_uint SetVerticalSpeed(ctypes.c_int index)
    addfunc(lib, "SetVerticalSpeed", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["index"] )
    #  ctypes.c_uint SetVirtualChip(ctypes.c_int state)
    addfunc(lib, "SetVirtualChip", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["state"] )
    #  ctypes.c_uint SetVSAmplitude(ctypes.c_int index)
    addfunc(lib, "SetVSAmplitude", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["index"] )
    #  ctypes.c_uint SetVSSpeed(ctypes.c_int index)
    addfunc(lib, "SetVSSpeed", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["index"] )
    #  ctypes.c_uint ShutDown()
    addfunc(lib, "ShutDown", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint StartAcquisition()
    addfunc(lib, "StartAcquisition", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint UnMapPhysicalAddress()
    addfunc(lib, "UnMapPhysicalAddress", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint UpdateDDGTimings()
    addfunc(lib, "UpdateDDGTimings", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint WaitForAcquisition()
    addfunc(lib, "WaitForAcquisition", restype = ctypes.c_uint,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_uint WaitForAcquisitionByHandle(ctypes.c_long cameraHandle)
    addfunc(lib, "WaitForAcquisitionByHandle", restype = ctypes.c_uint,
            argtypes = [ctypes.c_long],
            argnames = ["cameraHandle"] )
    #  ctypes.c_uint WaitForAcquisitionByHandleTimeOut(ctypes.c_long cameraHandle, ctypes.c_int iTimeOutMs)
    addfunc(lib, "WaitForAcquisitionByHandleTimeOut", restype = ctypes.c_uint,
            argtypes = [ctypes.c_long, ctypes.c_int],
            argnames = ["cameraHandle", "iTimeOutMs"] )
    #  ctypes.c_uint WaitForAcquisitionTimeOut(ctypes.c_int iTimeOutMs)
    addfunc(lib, "WaitForAcquisitionTimeOut", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["iTimeOutMs"] )
    #  ctypes.c_uint WhiteBalance(ctypes.POINTER(WORD) wRed, ctypes.POINTER(WORD) wGreen, ctypes.POINTER(WORD) wBlue, ctypes.POINTER(ctypes.c_float) fRelR, ctypes.POINTER(ctypes.c_float) fRelB, ctypes.POINTER(WhiteBalanceInfo) info)
    addfunc(lib, "WhiteBalance", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(WhiteBalanceInfo)],
            argnames = ["wRed", "wGreen", "wBlue", "fRelR", "fRelB", "info"] )
    #  ctypes.c_uint OA_Initialize(ctypes.c_char_p pcFilename, ctypes.c_uint uiFileNameLen)
    addfunc(lib, "OA_Initialize", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_uint],
            argnames = ["pcFilename", "uiFileNameLen"] )
    #  ctypes.c_uint OA_IsPreSetModeAvailable(ctypes.c_char_p pcModeName)
    addfunc(lib, "OA_IsPreSetModeAvailable", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p],
            argnames = ["pcModeName"] )
    #  ctypes.c_uint OA_EnableMode(ctypes.c_char_p pcModeName)
    addfunc(lib, "OA_EnableMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p],
            argnames = ["pcModeName"] )
    #  ctypes.c_uint OA_GetModeAcqParams(ctypes.c_char_p pcModeName, ctypes.c_char_p pcListOfParams)
    addfunc(lib, "OA_GetModeAcqParams", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p],
            argnames = ["pcModeName", "pcListOfParams"] )
    #  ctypes.c_uint OA_GetUserModeNames(ctypes.c_char_p pcListOfModes)
    addfunc(lib, "OA_GetUserModeNames", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p],
            argnames = ["pcListOfModes"] )
    #  ctypes.c_uint OA_GetPreSetModeNames(ctypes.c_char_p pcListOfModes)
    addfunc(lib, "OA_GetPreSetModeNames", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p],
            argnames = ["pcListOfModes"] )
    #  ctypes.c_uint OA_GetNumberOfUserModes(ctypes.POINTER(ctypes.c_uint) puiNumberOfModes)
    addfunc(lib, "OA_GetNumberOfUserModes", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_uint)],
            argnames = ["puiNumberOfModes"] )
    #  ctypes.c_uint OA_GetNumberOfPreSetModes(ctypes.POINTER(ctypes.c_uint) puiNumberOfModes)
    addfunc(lib, "OA_GetNumberOfPreSetModes", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_uint)],
            argnames = ["puiNumberOfModes"] )
    #  ctypes.c_uint OA_GetNumberOfAcqParams(ctypes.c_char_p pcModeName, ctypes.POINTER(ctypes.c_uint) puiNumberOfParams)
    addfunc(lib, "OA_GetNumberOfAcqParams", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint)],
            argnames = ["pcModeName", "puiNumberOfParams"] )
    #  ctypes.c_uint OA_AddMode(ctypes.c_char_p pcModeName, ctypes.c_uint uiModeNameLen, ctypes.c_char_p pcModeDescription, ctypes.c_uint uiModeDescriptionLen)
    addfunc(lib, "OA_AddMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint],
            argnames = ["pcModeName", "uiModeNameLen", "pcModeDescription", "uiModeDescriptionLen"] )
    #  ctypes.c_uint OA_WriteToFile(ctypes.c_char_p pcFileName, ctypes.c_uint uiFileNameLen)
    addfunc(lib, "OA_WriteToFile", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_uint],
            argnames = ["pcFileName", "uiFileNameLen"] )
    #  ctypes.c_uint OA_DeleteMode(ctypes.c_char_p pcModeName, ctypes.c_uint uiModeNameLen)
    addfunc(lib, "OA_DeleteMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_uint],
            argnames = ["pcModeName", "uiModeNameLen"] )
    #  ctypes.c_uint OA_SetInt(ctypes.c_char_p pcModeName, ctypes.c_char_p pcModeParam, ctypes.c_int iIntValue)
    addfunc(lib, "OA_SetInt", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int],
            argnames = ["pcModeName", "pcModeParam", "iIntValue"] )
    #  ctypes.c_uint OA_SetFloat(ctypes.c_char_p pcModeName, ctypes.c_char_p pcModeParam, ctypes.c_float fFloatValue)
    addfunc(lib, "OA_SetFloat", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_float],
            argnames = ["pcModeName", "pcModeParam", "fFloatValue"] )
    #  ctypes.c_uint OA_SetString(ctypes.c_char_p pcModeName, ctypes.c_char_p pcModeParam, ctypes.c_char_p pcStringValue, ctypes.c_uint uiStringLen)
    addfunc(lib, "OA_SetString", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint],
            argnames = ["pcModeName", "pcModeParam", "pcStringValue", "uiStringLen"] )
    #  ctypes.c_uint OA_GetInt(ctypes.c_char_p pcModeName, ctypes.c_char_p pcModeParam, ctypes.POINTER(ctypes.c_int) iIntValue)
    addfunc(lib, "OA_GetInt", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["pcModeName", "pcModeParam", "iIntValue"] )
    #  ctypes.c_uint OA_GetFloat(ctypes.c_char_p pcModeName, ctypes.c_char_p pcModeParam, ctypes.POINTER(ctypes.c_float) fFloatValue)
    addfunc(lib, "OA_GetFloat", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_float)],
            argnames = ["pcModeName", "pcModeParam", "fFloatValue"] )
    #  ctypes.c_uint OA_GetString(ctypes.c_char_p pcModeName, ctypes.c_char_p pcModeParam, ctypes.c_char_p pcStringValue, ctypes.c_uint uiStringLen)
    addfunc(lib, "OA_GetString", restype = ctypes.c_uint,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint],
            argnames = ["pcModeName", "pcModeParam", "pcStringValue", "uiStringLen"] )
    #  ctypes.c_uint Filter_SetMode(ctypes.c_uint mode)
    addfunc(lib, "Filter_SetMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_uint],
            argnames = ["mode"] )
    #  ctypes.c_uint Filter_GetMode(ctypes.POINTER(ctypes.c_uint) mode)
    addfunc(lib, "Filter_GetMode", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_uint)],
            argnames = ["mode"] )
    #  ctypes.c_uint Filter_SetThreshold(ctypes.c_float threshold)
    addfunc(lib, "Filter_SetThreshold", restype = ctypes.c_uint,
            argtypes = [ctypes.c_float],
            argnames = ["threshold"] )
    #  ctypes.c_uint Filter_GetThreshold(ctypes.POINTER(ctypes.c_float) threshold)
    addfunc(lib, "Filter_GetThreshold", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_float)],
            argnames = ["threshold"] )
    #  ctypes.c_uint Filter_SetDataAveragingMode(ctypes.c_int mode)
    addfunc(lib, "Filter_SetDataAveragingMode", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["mode"] )
    #  ctypes.c_uint Filter_GetDataAveragingMode(ctypes.POINTER(ctypes.c_int) mode)
    addfunc(lib, "Filter_GetDataAveragingMode", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["mode"] )
    #  ctypes.c_uint Filter_SetAveragingFrameCount(ctypes.c_int frames)
    addfunc(lib, "Filter_SetAveragingFrameCount", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["frames"] )
    #  ctypes.c_uint Filter_GetAveragingFrameCount(ctypes.POINTER(ctypes.c_int) frames)
    addfunc(lib, "Filter_GetAveragingFrameCount", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["frames"] )
    #  ctypes.c_uint Filter_SetAveragingFactor(ctypes.c_int averagingFactor)
    addfunc(lib, "Filter_SetAveragingFactor", restype = ctypes.c_uint,
            argtypes = [ctypes.c_int],
            argnames = ["averagingFactor"] )
    #  ctypes.c_uint Filter_GetAveragingFactor(ctypes.POINTER(ctypes.c_int) averagingFactor)
    addfunc(lib, "Filter_GetAveragingFactor", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["averagingFactor"] )
    #  ctypes.c_uint PostProcessNoiseFilter(ctypes.POINTER(ctypes.c_long) pInputImage, ctypes.POINTER(ctypes.c_long) pOutputImage, ctypes.c_int iOutputBufferSize, ctypes.c_int iBaseline, ctypes.c_int iMode, ctypes.c_float fThreshold, ctypes.c_int iHeight, ctypes.c_int iWidth)
    addfunc(lib, "PostProcessNoiseFilter", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_int, ctypes.c_int],
            argnames = ["pInputImage", "pOutputImage", "iOutputBufferSize", "iBaseline", "iMode", "fThreshold", "iHeight", "iWidth"] )
    #  ctypes.c_uint PostProcessCountConvert(ctypes.POINTER(ctypes.c_long) pInputImage, ctypes.POINTER(ctypes.c_long) pOutputImage, ctypes.c_int iOutputBufferSize, ctypes.c_int iNumImages, ctypes.c_int iBaseline, ctypes.c_int iMode, ctypes.c_int iEmGain, ctypes.c_float fQE, ctypes.c_float fSensitivity, ctypes.c_int iHeight, ctypes.c_int iWidth)
    addfunc(lib, "PostProcessCountConvert", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_int, ctypes.c_int],
            argnames = ["pInputImage", "pOutputImage", "iOutputBufferSize", "iNumImages", "iBaseline", "iMode", "iEmGain", "fQE", "fSensitivity", "iHeight", "iWidth"] )
    #  ctypes.c_uint PostProcessPhotonCounting(ctypes.POINTER(ctypes.c_long) pInputImage, ctypes.POINTER(ctypes.c_long) pOutputImage, ctypes.c_int iOutputBufferSize, ctypes.c_int iNumImages, ctypes.c_int iNumframes, ctypes.c_int iNumberOfThresholds, ctypes.POINTER(ctypes.c_float) pfThreshold, ctypes.c_int iHeight, ctypes.c_int iWidth)
    addfunc(lib, "PostProcessPhotonCounting", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int],
            argnames = ["pInputImage", "pOutputImage", "iOutputBufferSize", "iNumImages", "iNumframes", "iNumberOfThresholds", "pfThreshold", "iHeight", "iWidth"] )
    #  ctypes.c_uint PostProcessDataAveraging(ctypes.POINTER(ctypes.c_long) pInputImage, ctypes.POINTER(ctypes.c_long) pOutputImage, ctypes.c_int iOutputBufferSize, ctypes.c_int iNumImages, ctypes.c_int iAveragingFilterMode, ctypes.c_int iHeight, ctypes.c_int iWidth, ctypes.c_int iFrameCount, ctypes.c_int iAveragingFactor)
    addfunc(lib, "PostProcessDataAveraging", restype = ctypes.c_uint,
            argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["pInputImage", "pOutputImage", "iOutputBufferSize", "iNumImages", "iAveragingFilterMode", "iHeight", "iWidth", "iFrameCount", "iAveragingFactor"] )


