##########   This file is generated automatically based on sc2_camexport.h   ##########

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
SHORT=ctypes.c_short
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
class PCO_Buflist(ctypes.Structure):
    _fields_=[  ("sBufNr",SHORT),
                ("ZZwAlignDummy",WORD),
                ("dwStatusDll",DWORD),
                ("dwStatusDrv",DWORD) ]
PPCO_Buflist=ctypes.POINTER(PCO_Buflist)
class CPCO_Buflist(ctypes_wrap.CStructWrapper):
    _struct=PCO_Buflist


class PCO_OpenStruct(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wInterfaceType",WORD),
                ("wCameraNumber",WORD),
                ("wCameraNumAtInterface",WORD),
                ("wOpenFlags",WORD*10),
                ("dwOpenFlags",DWORD*5),
                ("wOpenPtr",ctypes.c_void_p*6),
                ("zzwDummy",WORD*8) ]
PPCO_OpenStruct=ctypes.POINTER(PCO_OpenStruct)
class CPCO_OpenStruct(ctypes_wrap.CStructWrapper):
    _struct=PCO_OpenStruct


class PCO_SC2_Hardware_DESC(ctypes.Structure):
    _fields_=[  ("szName",ctypes.c_char*16),
                ("wBatchNo",WORD),
                ("wRevision",WORD),
                ("wVariant",WORD),
                ("ZZwDummy",WORD*20) ]
PPCO_SC2_Hardware_DESC=ctypes.POINTER(PCO_SC2_Hardware_DESC)
class CPCO_SC2_Hardware_DESC(ctypes_wrap.CStructWrapper):
    _struct=PCO_SC2_Hardware_DESC


class PCO_SC2_Firmware_DESC(ctypes.Structure):
    _fields_=[  ("szName",ctypes.c_char*16),
                ("bMinorRev",BYTE),
                ("bMajorRev",BYTE),
                ("wVariant",WORD),
                ("ZZwDummy",WORD*22) ]
PPCO_SC2_Firmware_DESC=ctypes.POINTER(PCO_SC2_Firmware_DESC)
class CPCO_SC2_Firmware_DESC(ctypes_wrap.CStructWrapper):
    _struct=PCO_SC2_Firmware_DESC


class PCO_HW_Vers(ctypes.Structure):
    _fields_=[  ("BoardNum",WORD),
                ("Board",PCO_SC2_Hardware_DESC*10) ]
PPCO_HW_Vers=ctypes.POINTER(PCO_HW_Vers)
class CPCO_HW_Vers(ctypes_wrap.CStructWrapper):
    _struct=PCO_HW_Vers


class PCO_FW_Vers(ctypes.Structure):
    _fields_=[  ("DeviceNum",WORD),
                ("Device",PCO_SC2_Firmware_DESC*10) ]
PPCO_FW_Vers=ctypes.POINTER(PCO_FW_Vers)
class CPCO_FW_Vers(ctypes_wrap.CStructWrapper):
    _struct=PCO_FW_Vers


class PCO_CameraType(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wCamType",WORD),
                ("wCamSubType",WORD),
                ("ZZwAlignDummy1",WORD),
                ("dwSerialNumber",DWORD),
                ("dwHWVersion",DWORD),
                ("dwFWVersion",DWORD),
                ("wInterfaceType",WORD),
                ("strHardwareVersion",PCO_HW_Vers),
                ("strFirmwareVersion",PCO_FW_Vers),
                ("ZZwDummy",WORD*39) ]
PPCO_CameraType=ctypes.POINTER(PCO_CameraType)
class CPCO_CameraType(ctypes_wrap.CStructWrapper):
    _struct=PCO_CameraType


class PCO_General(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("ZZwAlignDummy1",WORD),
                ("strCamType",PCO_CameraType),
                ("dwCamHealthWarnings",DWORD),
                ("dwCamHealthErrors",DWORD),
                ("dwCamHealthStatus",DWORD),
                ("sCCDTemperature",SHORT),
                ("sCamTemperature",SHORT),
                ("sPowerSupplyTemperature",SHORT),
                ("ZZwDummy",WORD*37) ]
PPCO_General=ctypes.POINTER(PCO_General)
class CPCO_General(ctypes_wrap.CStructWrapper):
    _struct=PCO_General


class PCO_Description(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wSensorTypeDESC",WORD),
                ("wSensorSubTypeDESC",WORD),
                ("wMaxHorzResStdDESC",WORD),
                ("wMaxVertResStdDESC",WORD),
                ("wMaxHorzResExtDESC",WORD),
                ("wMaxVertResExtDESC",WORD),
                ("wDynResDESC",WORD),
                ("wMaxBinHorzDESC",WORD),
                ("wBinHorzSteppingDESC",WORD),
                ("wMaxBinVertDESC",WORD),
                ("wBinVertSteppingDESC",WORD),
                ("wRoiHorStepsDESC",WORD),
                ("wRoiVertStepsDESC",WORD),
                ("wNumADCsDESC",WORD),
                ("wMinSizeHorzDESC",WORD),
                ("dwPixelRateDESC",DWORD*4),
                ("ZZdwDummypr",DWORD*20),
                ("wConvFactDESC",WORD*4),
                ("sCoolingSetpoints",SHORT*10),
                ("ZZwDummycv",WORD*8),
                ("wSoftRoiHorStepsDESC",WORD),
                ("wSoftRoiVertStepsDESC",WORD),
                ("wIRDESC",WORD),
                ("wMinSizeVertDESC",WORD),
                ("dwMinDelayDESC",DWORD),
                ("dwMaxDelayDESC",DWORD),
                ("dwMinDelayStepDESC",DWORD),
                ("dwMinExposureDESC",DWORD),
                ("dwMaxExposureDESC",DWORD),
                ("dwMinExposureStepDESC",DWORD),
                ("dwMinDelayIRDESC",DWORD),
                ("dwMaxDelayIRDESC",DWORD),
                ("dwMinExposureIRDESC",DWORD),
                ("dwMaxExposureIRDESC",DWORD),
                ("wTimeTableDESC",WORD),
                ("wDoubleImageDESC",WORD),
                ("sMinCoolSetDESC",SHORT),
                ("sMaxCoolSetDESC",SHORT),
                ("sDefaultCoolSetDESC",SHORT),
                ("wPowerDownModeDESC",WORD),
                ("wOffsetRegulationDESC",WORD),
                ("wColorPatternDESC",WORD),
                ("wPatternTypeDESC",WORD),
                ("wDummy1",WORD),
                ("wDummy2",WORD),
                ("wNumCoolingSetpoints",WORD),
                ("dwGeneralCapsDESC1",DWORD),
                ("dwGeneralCapsDESC2",DWORD),
                ("dwExtSyncFrequency",DWORD*4),
                ("dwGeneralCapsDESC3",DWORD),
                ("dwGeneralCapsDESC4",DWORD),
                ("ZZdwDummy",DWORD*40) ]
PPCO_Description=ctypes.POINTER(PCO_Description)
class CPCO_Description(ctypes_wrap.CStructWrapper):
    _struct=PCO_Description


class PCO_Description2(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("ZZwAlignDummy1",WORD),
                ("dwMinPeriodicalTimeDESC2",DWORD),
                ("dwMaxPeriodicalTimeDESC2",DWORD),
                ("dwMinPeriodicalConditionDESC2",DWORD),
                ("dwMaxNumberOfExposuresDESC2",DWORD),
                ("lMinMonitorSignalOffsetDESC2",LONG),
                ("dwMaxMonitorSignalOffsetDESC2",DWORD),
                ("dwMinPeriodicalStepDESC2",DWORD),
                ("dwStartTimeDelayDESC2",DWORD),
                ("dwMinMonitorStepDESC2",DWORD),
                ("dwMinDelayModDESC2",DWORD),
                ("dwMaxDelayModDESC2",DWORD),
                ("dwMinDelayStepModDESC2",DWORD),
                ("dwMinExposureModDESC2",DWORD),
                ("dwMaxExposureModDESC2",DWORD),
                ("dwMinExposureStepModDESC2",DWORD),
                ("dwModulateCapsDESC2",DWORD),
                ("dwReserved",DWORD*16),
                ("ZZdwDummy",DWORD*41) ]
PPCO_Description2=ctypes.POINTER(PCO_Description2)
class CPCO_Description2(ctypes_wrap.CStructWrapper):
    _struct=PCO_Description2


class PCO_Description_Intensified(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wChannelNumberIntensifiedDESC",WORD),
                ("wNumberOfChannelsIntensifiedDESC",WORD),
                ("wMinVoltageIntensifiedDESC",WORD),
                ("wMaxVoltageIntensifiedDESC",WORD),
                ("wVoltageStepIntensifiedDESC",WORD),
                ("wExtendedMinVoltageIntensifiedDESC",WORD),
                ("wMaxLoopCountIntensifiedDESC",WORD),
                ("dwMinPhosphorDecayIntensified_ns_DESC",DWORD),
                ("dwMaxPhosphorDecayIntensified_ms_DESC",DWORD),
                ("dwFlagsIntensifiedDESC",DWORD),
                ("szIntensifierTypeDESC",ctypes.c_char*24),
                ("dwMCP_RectangleXL_DESC",DWORD),
                ("dwMCP_RectangleXR_DESC",DWORD),
                ("dwMCP_RectangleYT_DESC",DWORD),
                ("dwMCP_RectangleYB_DESC",DWORD),
                ("ZZdwDummy",DWORD*23) ]
PPCO_Description_Intensified=ctypes.POINTER(PCO_Description_Intensified)
class CPCO_Description_Intensified(ctypes_wrap.CStructWrapper):
    _struct=PCO_Description_Intensified


class PCO_DescriptionEx(ctypes.Structure):
    _fields_=[  ("wSize",WORD) ]
PPCO_DescriptionEx=ctypes.POINTER(PCO_DescriptionEx)
class CPCO_DescriptionEx(ctypes_wrap.CStructWrapper):
    _struct=PCO_DescriptionEx


class PCO_Single_Signal_Desc(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("ZZwAlignDummy1",WORD),
                ("strSignalName",ctypes.c_char*25*4),
                ("wSignalDefinitions",WORD),
                ("wSignalTypes",WORD),
                ("wSignalPolarity",WORD),
                ("wSignalFilter",WORD),
                ("dwDummy",DWORD*22) ]
PPCO_Single_Signal_Desc=ctypes.POINTER(PCO_Single_Signal_Desc)
class CPCO_Single_Signal_Desc(ctypes_wrap.CStructWrapper):
    _struct=PCO_Single_Signal_Desc


class PCO_Signal_Description(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wNumOfSignals",WORD),
                ("strSingeSignalDesc",PCO_Single_Signal_Desc*20),
                ("dwDummy",DWORD*524) ]
PPCO_Signal_Description=ctypes.POINTER(PCO_Signal_Description)
class CPCO_Signal_Description(ctypes_wrap.CStructWrapper):
    _struct=PCO_Signal_Description


class PCO_Sensor(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("ZZwAlignDummy1",WORD),
                ("strDescription",PCO_Description),
                ("strDescription2",PCO_Description2),
                ("strDescriptionIntensified",PCO_Description_Intensified),
                ("ZZdwDummy2",DWORD*216),
                ("wSensorformat",WORD),
                ("wRoiX0",WORD),
                ("wRoiY0",WORD),
                ("wRoiX1",WORD),
                ("wRoiY1",WORD),
                ("wBinHorz",WORD),
                ("wBinVert",WORD),
                ("wIntensifiedFlags",WORD),
                ("dwPixelRate",DWORD),
                ("wConvFact",WORD),
                ("wDoubleImage",WORD),
                ("wADCOperation",WORD),
                ("wIR",WORD),
                ("sCoolSet",SHORT),
                ("wOffsetRegulation",WORD),
                ("wNoiseFilterMode",WORD),
                ("wFastReadoutMode",WORD),
                ("wDSNUAdjustMode",WORD),
                ("wCDIMode",WORD),
                ("wIntensifiedVoltage",WORD),
                ("wIntensifiedGatingMode",WORD),
                ("dwIntensifiedPhosphorDecay_us",DWORD),
                ("ZZwDummy",WORD*32),
                ("strSignalDesc",PCO_Signal_Description),
                ("ZZdwDummy",DWORD*7) ]
PPCO_Sensor=ctypes.POINTER(PCO_Sensor)
class CPCO_Sensor(ctypes_wrap.CStructWrapper):
    _struct=PCO_Sensor


class PCO_Signal(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wSignalNum",WORD),
                ("wEnabled",WORD),
                ("wType",WORD),
                ("wPolarity",WORD),
                ("wFilterSetting",WORD),
                ("wSelected",WORD),
                ("ZZwReserved",WORD),
                ("dwParameter",DWORD*4),
                ("dwSignalFunctionality",DWORD*4),
                ("ZZdwReserved",DWORD*3) ]
PPCO_Signal=ctypes.POINTER(PCO_Signal)
class CPCO_Signal(ctypes_wrap.CStructWrapper):
    _struct=PCO_Signal


class PCO_ImageTiming(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wDummy",WORD),
                ("FrameTime_ns",DWORD),
                ("FrameTime_s",DWORD),
                ("ExposureTime_ns",DWORD),
                ("ExposureTime_s",DWORD),
                ("TriggerSystemDelay_ns",DWORD),
                ("TriggerSystemJitter_ns",DWORD),
                ("TriggerDelay_ns",DWORD),
                ("TriggerDelay_s",DWORD),
                ("ZZdwDummy",DWORD*11) ]
PPCO_ImageTiming=ctypes.POINTER(PCO_ImageTiming)
class CPCO_ImageTiming(ctypes_wrap.CStructWrapper):
    _struct=PCO_ImageTiming


class PCO_Timing(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wTimeBaseDelay",WORD),
                ("wTimeBaseExposure",WORD),
                ("wCMOSParameter",WORD),
                ("dwCMOSDelayLines",DWORD),
                ("dwCMOSExposureLines",DWORD),
                ("dwDelayTable",DWORD*16),
                ("ZZdwDummy1",DWORD*110),
                ("dwCMOSLineTimeMin",DWORD),
                ("dwCMOSLineTimeMax",DWORD),
                ("dwCMOSLineTime",DWORD),
                ("wCMOSTimeBase",WORD),
                ("wIntensifiedLoopCount",WORD),
                ("dwExposureTable",DWORD*16),
                ("ZZdwDummy2",DWORD*110),
                ("dwCMOSFlags",DWORD),
                ("ZZdwDummy3",DWORD),
                ("wTriggerMode",WORD),
                ("wForceTrigger",WORD),
                ("wCameraBusyStatus",WORD),
                ("wPowerDownMode",WORD),
                ("dwPowerDownTime",DWORD),
                ("wExpTrgSignal",WORD),
                ("wFPSExposureMode",WORD),
                ("dwFPSExposureTime",DWORD),
                ("wModulationMode",WORD),
                ("wCameraSynchMode",WORD),
                ("dwPeriodicalTime",DWORD),
                ("wTimeBasePeriodical",WORD),
                ("ZZwDummy3",WORD),
                ("dwNumberOfExposures",DWORD),
                ("lMonitorOffset",LONG),
                ("strSignal",PCO_Signal*20),
                ("wStatusFrameRate",WORD),
                ("wFrameRateMode",WORD),
                ("dwFrameRate",DWORD),
                ("dwFrameRateExposure",DWORD),
                ("wTimingControlMode",WORD),
                ("wFastTimingMode",WORD),
                ("ZZwDummy",WORD*24) ]
PPCO_Timing=ctypes.POINTER(PCO_Timing)
class CPCO_Timing(ctypes_wrap.CStructWrapper):
    _struct=PCO_Timing


class PCO_Storage(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("ZZwAlignDummy1",WORD),
                ("dwRamSize",DWORD),
                ("wPageSize",WORD),
                ("ZZwAlignDummy4",WORD),
                ("dwRamSegSize",DWORD*4),
                ("ZZdwDummyrs",DWORD*20),
                ("wActSeg",WORD),
                ("ZZwDummy",WORD*39) ]
PPCO_Storage=ctypes.POINTER(PCO_Storage)
class CPCO_Storage(ctypes_wrap.CStructWrapper):
    _struct=PCO_Storage


class PCO_Recording(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wStorageMode",WORD),
                ("wRecSubmode",WORD),
                ("wRecState",WORD),
                ("wAcquMode",WORD),
                ("wAcquEnableStatus",WORD),
                ("ucDay",BYTE),
                ("ucMonth",BYTE),
                ("wYear",WORD),
                ("wHour",WORD),
                ("ucMin",BYTE),
                ("ucSec",BYTE),
                ("wTimeStampMode",WORD),
                ("wRecordStopEventMode",WORD),
                ("dwRecordStopDelayImages",DWORD),
                ("wMetaDataMode",WORD),
                ("wMetaDataSize",WORD),
                ("wMetaDataVersion",WORD),
                ("ZZwDummy1",WORD),
                ("dwAcquModeExNumberImages",DWORD),
                ("dwAcquModeExReserved",DWORD*4),
                ("ZZwDummy",WORD*22) ]
PPCO_Recording=ctypes.POINTER(PCO_Recording)
class CPCO_Recording(ctypes_wrap.CStructWrapper):
    _struct=PCO_Recording


class PCO_Segment(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wXRes",WORD),
                ("wYRes",WORD),
                ("wBinHorz",WORD),
                ("wBinVert",WORD),
                ("wRoiX0",WORD),
                ("wRoiY0",WORD),
                ("wRoiX1",WORD),
                ("wRoiY1",WORD),
                ("ZZwAlignDummy1",WORD),
                ("dwValidImageCnt",DWORD),
                ("dwMaxImageCnt",DWORD),
                ("wRoiSoftX0",WORD),
                ("wRoiSoftY0",WORD),
                ("wRoiSoftX1",WORD),
                ("wRoiSoftY1",WORD),
                ("wRoiSoftXRes",WORD),
                ("wRoiSoftYRes",WORD),
                ("wRoiSoftDouble",WORD),
                ("ZZwDummy",WORD*33) ]
PPCO_Segment=ctypes.POINTER(PCO_Segment)
class CPCO_Segment(ctypes_wrap.CStructWrapper):
    _struct=PCO_Segment


class PCO_Image_ColorSet(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("sSaturation",SHORT),
                ("sVibrance",SHORT),
                ("wColorTemp",WORD),
                ("sTint",SHORT),
                ("wMulNormR",WORD),
                ("wMulNormG",WORD),
                ("wMulNormB",WORD),
                ("sContrast",SHORT),
                ("wGamma",WORD),
                ("wSharpFixed",WORD),
                ("wSharpAdaptive",WORD),
                ("wScaleMin",WORD),
                ("wScaleMax",WORD),
                ("wProcOptions",WORD),
                ("ZZwDummy",WORD*93) ]
PPCO_Image_ColorSet=ctypes.POINTER(PCO_Image_ColorSet)
class CPCO_Image_ColorSet(ctypes_wrap.CStructWrapper):
    _struct=PCO_Image_ColorSet


class PCO_Image(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("ZZwAlignDummy1",WORD),
                ("strSegment",PCO_Segment*4),
                ("ZZstrDummySeg",PCO_Segment*14),
                ("strColorSet",PCO_Image_ColorSet),
                ("wBitAlignment",WORD),
                ("wHotPixelCorrectionMode",WORD),
                ("ZZwDummy",WORD*38) ]
PPCO_Image=ctypes.POINTER(PCO_Image)
class CPCO_Image(ctypes_wrap.CStructWrapper):
    _struct=PCO_Image


class PCO_APIBuffer(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("ZZwAlignDummy1",WORD),
                ("dwBufferStatus",DWORD),
                ("hBufferEvent",HANDLE),
                ("ZZdwBufferAddress",DWORD),
                ("dwBufferSize",DWORD),
                ("dwDrvBufferStatus",DWORD),
                ("dwImageSize",DWORD),
                ("pBufferAdress",ctypes.c_void_p),
                ("ZZwDummy",WORD*32) ]
PPCO_APIBuffer=ctypes.POINTER(PCO_APIBuffer)
class CPCO_APIBuffer(ctypes_wrap.CStructWrapper):
    _struct=PCO_APIBuffer


class PCO_APIManagement(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wCameraNum",WORD),
                ("hCamera",HANDLE),
                ("wTakenFlag",WORD),
                ("wAPIManagementFlags",WORD),
                ("pSC2IFFunc",ctypes.c_void_p*20),
                ("strPCOBuf",PCO_APIBuffer*16),
                ("ZZstrDummyBuf",PCO_APIBuffer*(28-16)),
                ("sBufferCnt",SHORT),
                ("wCameraNumAtInterface",WORD),
                ("wInterface",WORD),
                ("wXRes",WORD),
                ("wYRes",WORD),
                ("wPowerCycleFlag",WORD),
                ("dwIF_param",DWORD*5),
                ("wImageTransferMode",WORD),
                ("wRoiSoftX0",WORD),
                ("wRoiSoftY0",WORD),
                ("wRoiSoftX1",WORD),
                ("wRoiSoftY1",WORD),
                ("wImageTransferParam",WORD*2),
                ("wImageTransferTxWidth",WORD),
                ("wImageTransferTxHeight",WORD),
                ("ZZwDummy",WORD*17) ]
PPCO_APIManagement=ctypes.POINTER(PCO_APIManagement)
class CPCO_APIManagement(ctypes_wrap.CStructWrapper):
    _struct=PCO_APIManagement


class PCO_Camera(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wStructRev",WORD),
                ("strGeneral",PCO_General),
                ("strSensor",PCO_Sensor),
                ("strTiming",PCO_Timing),
                ("strStorage",PCO_Storage),
                ("strRecording",PCO_Recording),
                ("strImage",PCO_Image),
                ("strAPIManager",PCO_APIManagement),
                ("ZZwDummy",WORD*40) ]
PPCO_Camera=ctypes.POINTER(PCO_Camera)
class CPCO_Camera(ctypes_wrap.CStructWrapper):
    _struct=PCO_Camera


class PCO_UserInterfaceInfo(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wZZDummy1",WORD),
                ("wInterfaceID",WORD),
                ("wNumberOfInterfaces",WORD),
                ("wInterfaceType",WORD),
                ("bBitsPerWord",BYTE*4),
                ("dwFrequency",DWORD*12),
                ("dwInterfaceOptions",DWORD),
                ("wInterfaceEnabled",WORD),
                ("dwAllowedEquipment",DWORD),
                ("wHandshakeType",WORD),
                ("wTxBufferMaxSize",WORD),
                ("wRxBufferMaxSize",WORD),
                ("wTxBufferFree",WORD),
                ("wRxBufferAvail",WORD),
                ("wRFU",WORD*4),
                ("wZZDummy2",WORD*25) ]
PPCO_UserInterfaceInfo=ctypes.POINTER(PCO_UserInterfaceInfo)
class CPCO_UserInterfaceInfo(ctypes_wrap.CStructWrapper):
    _struct=PCO_UserInterfaceInfo


class PCO_UserInterfaceSettings(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wZZDummy1",WORD),
                ("wInterfaceID",WORD),
                ("bInterfaceEnable",BYTE),
                ("bClearBuffers",BYTE),
                ("dwFrequency",DWORD),
                ("bBitsPerWord",BYTE),
                ("bReserved",BYTE),
                ("wHandshakeType",WORD),
                ("dwInterfaceOptions",DWORD),
                ("wRFU",WORD*4),
                ("wZZDummy2",WORD*18) ]
PPCO_UserInterfaceSettings=ctypes.POINTER(PCO_UserInterfaceSettings)
class CPCO_UserInterfaceSettings(ctypes_wrap.CStructWrapper):
    _struct=PCO_UserInterfaceSettings


class PCO_LensControlParameters(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wHardwareVersion",WORD),
                ("wBootloaderVersion",WORD),
                ("wSerialNumber",WORD),
                ("bLibraryIdentity",BYTE*48),
                ("dwLENSType",DWORD),
                ("dwStatusFlags",DWORD),
                ("dwInitCounter",DWORD),
                ("dwFNumberMinimum",DWORD),
                ("dwFNumberNumStops",DWORD),
                ("dwFNumberMaximum",DWORD),
                ("dwZoomRangeMin",DWORD),
                ("dwZoomRangeMax",DWORD),
                ("dwZoomPos",DWORD),
                ("dwLastZoomPos",DWORD),
                ("dwApertures",DWORD*50),
                ("dwFocalLength",DWORD),
                ("lFocusMin",LONG),
                ("lFocusMax",LONG),
                ("lFocusCurr",LONG),
                ("lFocusLastCurr",LONG),
                ("wAperturePos",WORD),
                ("wLastAperturePos",WORD),
                ("dwfLastAperturePos",DWORD) ]
PPCO_LensControlParameters=ctypes.POINTER(PCO_LensControlParameters)
class CPCO_LensControlParameters(ctypes_wrap.CStructWrapper):
    _struct=PCO_LensControlParameters


class PCO_LensControl(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("pstrUserInterfaceInfo",ctypes.POINTER(PCO_UserInterfaceInfo)),
                ("pstrUserInterfaceSettings",ctypes.POINTER(PCO_UserInterfaceSettings)),
                ("pstrLensControlParameters",ctypes.POINTER(PCO_LensControlParameters)),
                ("hCamera",HANDLE) ]
PPCO_LensControl=ctypes.POINTER(PCO_LensControl)
class CPCO_LensControl(ctypes_wrap.CStructWrapper):
    _struct=PCO_LensControl


class PCO_Birger(ctypes.Structure):
    _fields_=[  ("wCommand",WORD),
                ("wResult",WORD),
                ("wType",WORD),
                ("bArray",BYTE*128) ]
PPCO_Birger=ctypes.POINTER(PCO_Birger)
class CPCO_Birger(ctypes_wrap.CStructWrapper):
    _struct=PCO_Birger


class PCO_METADATA_STRUCT(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("wVersion",WORD),
                ("bIMAGE_COUNTER_BCD",BYTE*4),
                ("bIMAGE_TIME_US_BCD",BYTE*3),
                ("bIMAGE_TIME_SEC_BCD",BYTE),
                ("bIMAGE_TIME_MIN_BCD",BYTE),
                ("bIMAGE_TIME_HOUR_BCD",BYTE),
                ("bIMAGE_TIME_DAY_BCD",BYTE),
                ("bIMAGE_TIME_MON_BCD",BYTE),
                ("bIMAGE_TIME_YEAR_BCD",BYTE),
                ("bIMAGE_TIME_STATUS",BYTE),
                ("wEXPOSURE_TIME_BASE",WORD),
                ("dwEXPOSURE_TIME",DWORD),
                ("dwFRAMERATE_MILLIHZ",DWORD),
                ("sSENSOR_TEMPERATURE",SHORT),
                ("wIMAGE_SIZE_X",WORD),
                ("wIMAGE_SIZE_Y",WORD),
                ("bBINNING_X",BYTE),
                ("bBINNING_Y",BYTE),
                ("dwSENSOR_READOUT_FREQUENCY",DWORD),
                ("wSENSOR_CONV_FACTOR",WORD),
                ("dwCAMERA_SERIAL_NO",DWORD),
                ("wCAMERA_TYPE",WORD),
                ("bBIT_RESOLUTION",BYTE),
                ("bSYNC_STATUS",BYTE),
                ("wDARK_OFFSET",WORD),
                ("bTRIGGER_MODE",BYTE),
                ("bDOUBLE_IMAGE_MODE",BYTE),
                ("bCAMERA_SYNC_MODE",BYTE),
                ("bIMAGE_TYPE",BYTE),
                ("wCOLOR_PATTERN",WORD) ]
PPCO_METADATA_STRUCT=ctypes.POINTER(PCO_METADATA_STRUCT)
class CPCO_METADATA_STRUCT(ctypes_wrap.CStructWrapper):
    _struct=PCO_METADATA_STRUCT


class PCO_TIMESTAMP_STRUCT(ctypes.Structure):
    _fields_=[  ("wSize",WORD),
                ("dwImgCounter",DWORD),
                ("wYear",WORD),
                ("wMonth",WORD),
                ("wDay",WORD),
                ("wHour",WORD),
                ("wMinute",WORD),
                ("wSecond",WORD),
                ("dwMicroSeconds",DWORD) ]
PPCO_TIMESTAMP_STRUCT=ctypes.POINTER(PCO_TIMESTAMP_STRUCT)
class CPCO_TIMESTAMP_STRUCT(ctypes_wrap.CStructWrapper):
    _struct=PCO_TIMESTAMP_STRUCT





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
    #  DWORD GetError(DWORD dwerr)
    addfunc(lib, "GetError", restype = DWORD,
            argtypes = [DWORD],
            argnames = ["dwerr"] )
    #  DWORD GetErrorSource(DWORD dwerr)
    addfunc(lib, "GetErrorSource", restype = DWORD,
            argtypes = [DWORD],
            argnames = ["dwerr"] )
    #  None PCO_GetErrorText(DWORD dwerr, ctypes.c_char_p pbuf, DWORD dwlen)
    addfunc(lib, "PCO_GetErrorText", restype = None,
            argtypes = [DWORD, ctypes.c_char_p, DWORD],
            argnames = ["dwerr", "pbuf", "dwlen"] )
    #  ctypes.c_int PCO_GetGeneral(HANDLE ph, ctypes.POINTER(PCO_General) strGeneral)
    addfunc(lib, "PCO_GetGeneral", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_General)],
            argnames = ["ph", "strGeneral"] )
    #  ctypes.c_int PCO_GetCameraType(HANDLE ph, ctypes.POINTER(PCO_CameraType) strCamType)
    addfunc(lib, "PCO_GetCameraType", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_CameraType)],
            argnames = ["ph", "strCamType"] )
    #  ctypes.c_int PCO_GetCameraHealthStatus(HANDLE ph, ctypes.POINTER(DWORD) dwWarn, ctypes.POINTER(DWORD) dwErr, ctypes.POINTER(DWORD) dwStatus)
    addfunc(lib, "PCO_GetCameraHealthStatus", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD), ctypes.POINTER(DWORD), ctypes.POINTER(DWORD)],
            argnames = ["ph", "dwWarn", "dwErr", "dwStatus"] )
    #  ctypes.c_int PCO_ResetSettingsToDefault(HANDLE ph)
    addfunc(lib, "PCO_ResetSettingsToDefault", restype = ctypes.c_int,
            argtypes = [HANDLE],
            argnames = ["ph"] )
    #  ctypes.c_int PCO_GetTemperature(HANDLE ph, ctypes.POINTER(SHORT) sCCDTemp, ctypes.POINTER(SHORT) sCamTemp, ctypes.POINTER(SHORT) sPowTemp)
    addfunc(lib, "PCO_GetTemperature", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(SHORT), ctypes.POINTER(SHORT), ctypes.POINTER(SHORT)],
            argnames = ["ph", "sCCDTemp", "sCamTemp", "sPowTemp"] )
    #  ctypes.c_int PCO_GetInfoString(HANDLE ph, DWORD dwinfotype, ctypes.c_char_p buf_in, WORD size_in)
    addfunc(lib, "PCO_GetInfoString", restype = ctypes.c_int,
            argtypes = [HANDLE, DWORD, ctypes.c_char_p, WORD],
            argnames = ["ph", "dwinfotype", "buf_in", "size_in"] )
    #  ctypes.c_int PCO_GetCameraName(HANDLE ph, ctypes.c_char_p szCameraName, WORD wSZCameraNameLen)
    addfunc(lib, "PCO_GetCameraName", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.c_char_p, WORD],
            argnames = ["ph", "szCameraName", "wSZCameraNameLen"] )
    #  ctypes.c_int PCO_GetFirmwareInfo(HANDLE ph, WORD wDeviceBlock, ctypes.POINTER(PCO_FW_Vers) pstrFirmWareVersion)
    addfunc(lib, "PCO_GetFirmwareInfo", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.POINTER(PCO_FW_Vers)],
            argnames = ["ph", "wDeviceBlock", "pstrFirmWareVersion"] )
    #  ctypes.c_int PCO_GetCameraSetup(HANDLE ph, ctypes.POINTER(WORD) wType, ctypes.POINTER(DWORD) dwSetup, ctypes.POINTER(WORD) wLen)
    addfunc(lib, "PCO_GetCameraSetup", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(DWORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wType", "dwSetup", "wLen"] )
    #  ctypes.c_int PCO_SetCameraSetup(HANDLE ph, WORD wType, ctypes.POINTER(DWORD) dwSetup, WORD wLen)
    addfunc(lib, "PCO_SetCameraSetup", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.POINTER(DWORD), WORD],
            argnames = ["ph", "wType", "dwSetup", "wLen"] )
    #  ctypes.c_int PCO_RebootCamera(HANDLE ph)
    addfunc(lib, "PCO_RebootCamera", restype = ctypes.c_int,
            argtypes = [HANDLE],
            argnames = ["ph"] )
    #  ctypes.c_int PCO_GetPowerSaveMode(HANDLE ph, ctypes.POINTER(WORD) wMode, ctypes.POINTER(WORD) wDelayMinutes)
    addfunc(lib, "PCO_GetPowerSaveMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wMode", "wDelayMinutes"] )
    #  ctypes.c_int PCO_SetPowerSaveMode(HANDLE ph, WORD wMode, WORD wDelayMinutes)
    addfunc(lib, "PCO_SetPowerSaveMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD],
            argnames = ["ph", "wMode", "wDelayMinutes"] )
    #  ctypes.c_int PCO_GetBatteryStatus(HANDLE ph, ctypes.POINTER(WORD) wBatteryType, ctypes.POINTER(WORD) wBatteryLevel, ctypes.POINTER(WORD) wPowerStatus, ctypes.POINTER(WORD) wReserved, WORD wNumReserved)
    addfunc(lib, "PCO_GetBatteryStatus", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), WORD],
            argnames = ["ph", "wBatteryType", "wBatteryLevel", "wPowerStatus", "wReserved", "wNumReserved"] )
    #  ctypes.c_int PCO_GetFanControlParameters(HANDLE hCam, ctypes.POINTER(WORD) wMode, ctypes.POINTER(WORD) wValue, ctypes.POINTER(WORD) wReserved, WORD wNumReserved)
    addfunc(lib, "PCO_GetFanControlParameters", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), WORD],
            argnames = ["hCam", "wMode", "wValue", "wReserved", "wNumReserved"] )
    #  ctypes.c_int PCO_SetFanControlParameters(HANDLE hCam, WORD wMode, WORD wValue, WORD wReserved)
    addfunc(lib, "PCO_SetFanControlParameters", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD, WORD],
            argnames = ["hCam", "wMode", "wValue", "wReserved"] )
    #  ctypes.c_int PCO_GetSensorStruct(HANDLE ph, ctypes.POINTER(PCO_Sensor) strSensor)
    addfunc(lib, "PCO_GetSensorStruct", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_Sensor)],
            argnames = ["ph", "strSensor"] )
    #  ctypes.c_int PCO_SetSensorStruct(HANDLE ph, ctypes.POINTER(PCO_Sensor) strSensor)
    addfunc(lib, "PCO_SetSensorStruct", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_Sensor)],
            argnames = ["ph", "strSensor"] )
    #  ctypes.c_int PCO_GetCameraDescription(HANDLE ph, ctypes.POINTER(PCO_Description) strDescription)
    addfunc(lib, "PCO_GetCameraDescription", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_Description)],
            argnames = ["ph", "strDescription"] )
    #  ctypes.c_int PCO_GetCameraDescriptionEx(HANDLE ph, ctypes.POINTER(PCO_DescriptionEx) strDescription, WORD wType)
    addfunc(lib, "PCO_GetCameraDescriptionEx", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_DescriptionEx), WORD],
            argnames = ["ph", "strDescription", "wType"] )
    #  ctypes.c_int PCO_GetSensorFormat(HANDLE ph, ctypes.POINTER(WORD) wSensor)
    addfunc(lib, "PCO_GetSensorFormat", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wSensor"] )
    #  ctypes.c_int PCO_SetSensorFormat(HANDLE ph, WORD wSensor)
    addfunc(lib, "PCO_SetSensorFormat", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wSensor"] )
    #  ctypes.c_int PCO_GetSizes(HANDLE ph, ctypes.POINTER(WORD) wXResAct, ctypes.POINTER(WORD) wYResAct, ctypes.POINTER(WORD) wXResMax, ctypes.POINTER(WORD) wYResMax)
    addfunc(lib, "PCO_GetSizes", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wXResAct", "wYResAct", "wXResMax", "wYResMax"] )
    #  ctypes.c_int PCO_GetROI(HANDLE ph, ctypes.POINTER(WORD) wRoiX0, ctypes.POINTER(WORD) wRoiY0, ctypes.POINTER(WORD) wRoiX1, ctypes.POINTER(WORD) wRoiY1)
    addfunc(lib, "PCO_GetROI", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wRoiX0", "wRoiY0", "wRoiX1", "wRoiY1"] )
    #  ctypes.c_int PCO_SetROI(HANDLE ph, WORD wRoiX0, WORD wRoiY0, WORD wRoiX1, WORD wRoiY1)
    addfunc(lib, "PCO_SetROI", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD, WORD, WORD],
            argnames = ["ph", "wRoiX0", "wRoiY0", "wRoiX1", "wRoiY1"] )
    #  ctypes.c_int PCO_GetBinning(HANDLE ph, ctypes.POINTER(WORD) wBinHorz, ctypes.POINTER(WORD) wBinVert)
    addfunc(lib, "PCO_GetBinning", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wBinHorz", "wBinVert"] )
    #  ctypes.c_int PCO_SetBinning(HANDLE ph, WORD wBinHorz, WORD wBinVert)
    addfunc(lib, "PCO_SetBinning", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD],
            argnames = ["ph", "wBinHorz", "wBinVert"] )
    #  ctypes.c_int PCO_GetPixelRate(HANDLE ph, ctypes.POINTER(DWORD) dwPixelRate)
    addfunc(lib, "PCO_GetPixelRate", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD)],
            argnames = ["ph", "dwPixelRate"] )
    #  ctypes.c_int PCO_SetPixelRate(HANDLE ph, DWORD dwPixelRate)
    addfunc(lib, "PCO_SetPixelRate", restype = ctypes.c_int,
            argtypes = [HANDLE, DWORD],
            argnames = ["ph", "dwPixelRate"] )
    #  ctypes.c_int PCO_GetConversionFactor(HANDLE ph, ctypes.POINTER(WORD) wConvFact)
    addfunc(lib, "PCO_GetConversionFactor", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wConvFact"] )
    #  ctypes.c_int PCO_SetConversionFactor(HANDLE ph, WORD wConvFact)
    addfunc(lib, "PCO_SetConversionFactor", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wConvFact"] )
    #  ctypes.c_int PCO_GetDoubleImageMode(HANDLE ph, ctypes.POINTER(WORD) wDoubleImage)
    addfunc(lib, "PCO_GetDoubleImageMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wDoubleImage"] )
    #  ctypes.c_int PCO_SetDoubleImageMode(HANDLE ph, WORD wDoubleImage)
    addfunc(lib, "PCO_SetDoubleImageMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wDoubleImage"] )
    #  ctypes.c_int PCO_GetADCOperation(HANDLE ph, ctypes.POINTER(WORD) wADCOperation)
    addfunc(lib, "PCO_GetADCOperation", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wADCOperation"] )
    #  ctypes.c_int PCO_SetADCOperation(HANDLE ph, WORD wADCOperation)
    addfunc(lib, "PCO_SetADCOperation", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wADCOperation"] )
    #  ctypes.c_int PCO_GetIRSensitivity(HANDLE ph, ctypes.POINTER(WORD) wIR)
    addfunc(lib, "PCO_GetIRSensitivity", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wIR"] )
    #  ctypes.c_int PCO_SetIRSensitivity(HANDLE ph, WORD wIR)
    addfunc(lib, "PCO_SetIRSensitivity", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wIR"] )
    #  ctypes.c_int PCO_GetCoolingSetpoints(HANDLE ph, WORD wBlockID, ctypes.POINTER(WORD) wNumSetPoints, ctypes.POINTER(SHORT) sCoolSetpoints)
    addfunc(lib, "PCO_GetCoolingSetpoints", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.POINTER(WORD), ctypes.POINTER(SHORT)],
            argnames = ["ph", "wBlockID", "wNumSetPoints", "sCoolSetpoints"] )
    #  ctypes.c_int PCO_GetCoolingSetpointTemperature(HANDLE ph, ctypes.POINTER(SHORT) sCoolSet)
    addfunc(lib, "PCO_GetCoolingSetpointTemperature", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(SHORT)],
            argnames = ["ph", "sCoolSet"] )
    #  ctypes.c_int PCO_SetCoolingSetpointTemperature(HANDLE ph, SHORT sCoolSet)
    addfunc(lib, "PCO_SetCoolingSetpointTemperature", restype = ctypes.c_int,
            argtypes = [HANDLE, SHORT],
            argnames = ["ph", "sCoolSet"] )
    #  ctypes.c_int PCO_GetOffsetMode(HANDLE ph, ctypes.POINTER(WORD) wOffsetRegulation)
    addfunc(lib, "PCO_GetOffsetMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wOffsetRegulation"] )
    #  ctypes.c_int PCO_SetOffsetMode(HANDLE ph, WORD wOffsetRegulation)
    addfunc(lib, "PCO_SetOffsetMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wOffsetRegulation"] )
    #  ctypes.c_int PCO_GetNoiseFilterMode(HANDLE ph, ctypes.POINTER(WORD) wNoiseFilterMode)
    addfunc(lib, "PCO_GetNoiseFilterMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wNoiseFilterMode"] )
    #  ctypes.c_int PCO_SetNoiseFilterMode(HANDLE ph, WORD wNoiseFilterMode)
    addfunc(lib, "PCO_SetNoiseFilterMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wNoiseFilterMode"] )
    #  ctypes.c_int PCO_GetHWIOSignalCount(HANDLE ph, ctypes.POINTER(WORD) wNumSignals)
    addfunc(lib, "PCO_GetHWIOSignalCount", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wNumSignals"] )
    #  ctypes.c_int PCO_GetHWIOSignalDescriptor(HANDLE ph, WORD wSignalNum, ctypes.POINTER(PCO_Single_Signal_Desc) pstrSignal)
    addfunc(lib, "PCO_GetHWIOSignalDescriptor", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.POINTER(PCO_Single_Signal_Desc)],
            argnames = ["ph", "wSignalNum", "pstrSignal"] )
    #  ctypes.c_int PCO_GetColorCorrectionMatrix(HANDLE ph, ctypes.POINTER(ctypes.c_double) pdMatrix)
    addfunc(lib, "PCO_GetColorCorrectionMatrix", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(ctypes.c_double)],
            argnames = ["ph", "pdMatrix"] )
    #  ctypes.c_int PCO_GetDSNUAdjustMode(HANDLE ph, ctypes.POINTER(WORD) wDSNUAdjustMode, ctypes.POINTER(WORD) wReserved)
    addfunc(lib, "PCO_GetDSNUAdjustMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wDSNUAdjustMode", "wReserved"] )
    #  ctypes.c_int PCO_SetDSNUAdjustMode(HANDLE ph, WORD wDSNUAdjustMode, WORD wReserved)
    addfunc(lib, "PCO_SetDSNUAdjustMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD],
            argnames = ["ph", "wDSNUAdjustMode", "wReserved"] )
    #  ctypes.c_int PCO_InitDSNUAdjustment(HANDLE ph, WORD wDSNUAdjustMode, WORD wReserved)
    addfunc(lib, "PCO_InitDSNUAdjustment", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD],
            argnames = ["ph", "wDSNUAdjustMode", "wReserved"] )
    #  ctypes.c_int PCO_GetCDIMode(HANDLE ph, ctypes.POINTER(WORD) wCDIMode)
    addfunc(lib, "PCO_GetCDIMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wCDIMode"] )
    #  ctypes.c_int PCO_SetCDIMode(HANDLE ph, WORD wCDIMode)
    addfunc(lib, "PCO_SetCDIMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wCDIMode"] )
    #  ctypes.c_int PCO_GetLookupTableInfo(HANDLE ph, WORD wLUTNum, ctypes.POINTER(WORD) wNumberOfLuts, ctypes.c_char_p Description, WORD wDescLen, ctypes.POINTER(WORD) wIdentifier, ctypes.POINTER(BYTE) bInputWidth, ctypes.POINTER(BYTE) bOutputWidth, ctypes.POINTER(WORD) wFormat)
    addfunc(lib, "PCO_GetLookupTableInfo", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.POINTER(WORD), ctypes.c_char_p, WORD, ctypes.POINTER(WORD), ctypes.POINTER(BYTE), ctypes.POINTER(BYTE), ctypes.POINTER(WORD)],
            argnames = ["ph", "wLUTNum", "wNumberOfLuts", "Description", "wDescLen", "wIdentifier", "bInputWidth", "bOutputWidth", "wFormat"] )
    #  ctypes.c_int PCO_GetActiveLookupTable(HANDLE ph, ctypes.POINTER(WORD) wIdentifier, ctypes.POINTER(WORD) wParameter)
    addfunc(lib, "PCO_GetActiveLookupTable", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wIdentifier", "wParameter"] )
    #  ctypes.c_int PCO_SetActiveLookupTable(HANDLE ph, ctypes.POINTER(WORD) wIdentifier, ctypes.POINTER(WORD) wParameter)
    addfunc(lib, "PCO_SetActiveLookupTable", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wIdentifier", "wParameter"] )
    #  ctypes.c_int PCO_GetIntensifiedGatingMode(HANDLE ph, ctypes.POINTER(WORD) wIntensifiedGatingMode, ctypes.POINTER(WORD) wReserved)
    addfunc(lib, "PCO_GetIntensifiedGatingMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wIntensifiedGatingMode", "wReserved"] )
    #  ctypes.c_int PCO_SetIntensifiedGatingMode(HANDLE ph, WORD wIntensifiedGatingMode, WORD wReserved)
    addfunc(lib, "PCO_SetIntensifiedGatingMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD],
            argnames = ["ph", "wIntensifiedGatingMode", "wReserved"] )
    #  ctypes.c_int PCO_GetIntensifiedMCP(HANDLE ph, ctypes.POINTER(WORD) wIntensifiedVoltage, ctypes.POINTER(WORD) wReserved, ctypes.POINTER(DWORD) dwIntensifiedPhosphorDecay_us, ctypes.POINTER(DWORD) dwReserved1, ctypes.POINTER(DWORD) dwReserved2)
    addfunc(lib, "PCO_GetIntensifiedMCP", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(DWORD), ctypes.POINTER(DWORD), ctypes.POINTER(DWORD)],
            argnames = ["ph", "wIntensifiedVoltage", "wReserved", "dwIntensifiedPhosphorDecay_us", "dwReserved1", "dwReserved2"] )
    #  ctypes.c_int PCO_SetIntensifiedMCP(HANDLE ph, WORD wIntensifiedVoltage, WORD wFlags, WORD wReserved, DWORD dwIntensifiedPhosphorDecay_us, DWORD dwReserved1, DWORD dwReserved2)
    addfunc(lib, "PCO_SetIntensifiedMCP", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD, WORD, DWORD, DWORD, DWORD],
            argnames = ["ph", "wIntensifiedVoltage", "wFlags", "wReserved", "dwIntensifiedPhosphorDecay_us", "dwReserved1", "dwReserved2"] )
    #  ctypes.c_int PCO_GetTimingStruct(HANDLE ph, ctypes.POINTER(PCO_Timing) strTiming)
    addfunc(lib, "PCO_GetTimingStruct", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_Timing)],
            argnames = ["ph", "strTiming"] )
    #  ctypes.c_int PCO_SetTimingStruct(HANDLE ph, ctypes.POINTER(PCO_Timing) strTiming)
    addfunc(lib, "PCO_SetTimingStruct", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_Timing)],
            argnames = ["ph", "strTiming"] )
    #  ctypes.c_int PCO_GetDelayExposureTime(HANDLE ph, ctypes.POINTER(DWORD) dwDelay, ctypes.POINTER(DWORD) dwExposure, ctypes.POINTER(WORD) wTimeBaseDelay, ctypes.POINTER(WORD) wTimeBaseExposure)
    addfunc(lib, "PCO_GetDelayExposureTime", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD), ctypes.POINTER(DWORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "dwDelay", "dwExposure", "wTimeBaseDelay", "wTimeBaseExposure"] )
    #  ctypes.c_int PCO_SetDelayExposureTime(HANDLE ph, DWORD dwDelay, DWORD dwExposure, WORD wTimeBaseDelay, WORD wTimeBaseExposure)
    addfunc(lib, "PCO_SetDelayExposureTime", restype = ctypes.c_int,
            argtypes = [HANDLE, DWORD, DWORD, WORD, WORD],
            argnames = ["ph", "dwDelay", "dwExposure", "wTimeBaseDelay", "wTimeBaseExposure"] )
    #  ctypes.c_int PCO_GetDelayExposureTimeTable(HANDLE ph, ctypes.POINTER(DWORD) dwDelay, ctypes.POINTER(DWORD) dwExposure, ctypes.POINTER(WORD) wTimeBaseDelay, ctypes.POINTER(WORD) wTimeBaseExposure, WORD wCount)
    addfunc(lib, "PCO_GetDelayExposureTimeTable", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD), ctypes.POINTER(DWORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), WORD],
            argnames = ["ph", "dwDelay", "dwExposure", "wTimeBaseDelay", "wTimeBaseExposure", "wCount"] )
    #  ctypes.c_int PCO_SetDelayExposureTimeTable(HANDLE ph, ctypes.POINTER(DWORD) dwDelay, ctypes.POINTER(DWORD) dwExposure, WORD wTimeBaseDelay, WORD wTimeBaseExposure, WORD wCount)
    addfunc(lib, "PCO_SetDelayExposureTimeTable", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD), ctypes.POINTER(DWORD), WORD, WORD, WORD],
            argnames = ["ph", "dwDelay", "dwExposure", "wTimeBaseDelay", "wTimeBaseExposure", "wCount"] )
    #  ctypes.c_int PCO_GetTriggerMode(HANDLE ph, ctypes.POINTER(WORD) wTriggerMode)
    addfunc(lib, "PCO_GetTriggerMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wTriggerMode"] )
    #  ctypes.c_int PCO_SetTriggerMode(HANDLE ph, WORD wTriggerMode)
    addfunc(lib, "PCO_SetTriggerMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wTriggerMode"] )
    #  ctypes.c_int PCO_ForceTrigger(HANDLE ph, ctypes.POINTER(WORD) wTriggered)
    addfunc(lib, "PCO_ForceTrigger", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wTriggered"] )
    #  ctypes.c_int PCO_GetCameraBusyStatus(HANDLE ph, ctypes.POINTER(WORD) wCameraBusyState)
    addfunc(lib, "PCO_GetCameraBusyStatus", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wCameraBusyState"] )
    #  ctypes.c_int PCO_GetPowerDownMode(HANDLE ph, ctypes.POINTER(WORD) wPowerDownMode)
    addfunc(lib, "PCO_GetPowerDownMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wPowerDownMode"] )
    #  ctypes.c_int PCO_SetPowerDownMode(HANDLE ph, WORD wPowerDownMode)
    addfunc(lib, "PCO_SetPowerDownMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wPowerDownMode"] )
    #  ctypes.c_int PCO_GetUserPowerDownTime(HANDLE ph, ctypes.POINTER(DWORD) dwPowerDownTime)
    addfunc(lib, "PCO_GetUserPowerDownTime", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD)],
            argnames = ["ph", "dwPowerDownTime"] )
    #  ctypes.c_int PCO_SetUserPowerDownTime(HANDLE ph, DWORD dwPowerDownTime)
    addfunc(lib, "PCO_SetUserPowerDownTime", restype = ctypes.c_int,
            argtypes = [HANDLE, DWORD],
            argnames = ["ph", "dwPowerDownTime"] )
    #  ctypes.c_int PCO_GetExpTrigSignalStatus(HANDLE ph, ctypes.POINTER(WORD) wExpTrgSignal)
    addfunc(lib, "PCO_GetExpTrigSignalStatus", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wExpTrgSignal"] )
    #  ctypes.c_int PCO_GetCOCRuntime(HANDLE ph, ctypes.POINTER(DWORD) dwTime_s, ctypes.POINTER(DWORD) dwTime_ns)
    addfunc(lib, "PCO_GetCOCRuntime", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD), ctypes.POINTER(DWORD)],
            argnames = ["ph", "dwTime_s", "dwTime_ns"] )
    #  ctypes.c_int PCO_GetFPSExposureMode(HANDLE ph, ctypes.POINTER(WORD) wFPSExposureMode, ctypes.POINTER(DWORD) dwFPSExposureTime)
    addfunc(lib, "PCO_GetFPSExposureMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(DWORD)],
            argnames = ["ph", "wFPSExposureMode", "dwFPSExposureTime"] )
    #  ctypes.c_int PCO_SetFPSExposureMode(HANDLE ph, WORD wFPSExposureMode, ctypes.POINTER(DWORD) dwFPSExposureTime)
    addfunc(lib, "PCO_SetFPSExposureMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.POINTER(DWORD)],
            argnames = ["ph", "wFPSExposureMode", "dwFPSExposureTime"] )
    #  ctypes.c_int PCO_GetModulationMode(HANDLE ph, ctypes.POINTER(WORD) wModulationMode, ctypes.POINTER(DWORD) dwPeriodicalTime, ctypes.POINTER(WORD) wTimebasePeriodical, ctypes.POINTER(DWORD) dwNumberOfExposures, ctypes.POINTER(LONG) lMonitorOffset)
    addfunc(lib, "PCO_GetModulationMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(DWORD), ctypes.POINTER(WORD), ctypes.POINTER(DWORD), ctypes.POINTER(LONG)],
            argnames = ["ph", "wModulationMode", "dwPeriodicalTime", "wTimebasePeriodical", "dwNumberOfExposures", "lMonitorOffset"] )
    #  ctypes.c_int PCO_SetModulationMode(HANDLE ph, WORD wModulationMode, DWORD dwPeriodicalTime, WORD wTimebasePeriodical, DWORD dwNumberOfExposures, LONG lMonitorOffset)
    addfunc(lib, "PCO_SetModulationMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, DWORD, WORD, DWORD, LONG],
            argnames = ["ph", "wModulationMode", "dwPeriodicalTime", "wTimebasePeriodical", "dwNumberOfExposures", "lMonitorOffset"] )
    #  ctypes.c_int PCO_GetFrameRate(HANDLE ph, ctypes.POINTER(WORD) wFrameRateStatus, ctypes.POINTER(DWORD) dwFrameRate, ctypes.POINTER(DWORD) dwFrameRateExposure)
    addfunc(lib, "PCO_GetFrameRate", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(DWORD), ctypes.POINTER(DWORD)],
            argnames = ["ph", "wFrameRateStatus", "dwFrameRate", "dwFrameRateExposure"] )
    #  ctypes.c_int PCO_SetFrameRate(HANDLE ph, ctypes.POINTER(WORD) wFrameRateStatus, WORD wFrameRateMode, ctypes.POINTER(DWORD) dwFrameRate, ctypes.POINTER(DWORD) dwFrameRateExposure)
    addfunc(lib, "PCO_SetFrameRate", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), WORD, ctypes.POINTER(DWORD), ctypes.POINTER(DWORD)],
            argnames = ["ph", "wFrameRateStatus", "wFrameRateMode", "dwFrameRate", "dwFrameRateExposure"] )
    #  ctypes.c_int PCO_GetHWIOSignal(HANDLE ph, WORD wSignalNum, ctypes.POINTER(PCO_Signal) pstrSignal)
    addfunc(lib, "PCO_GetHWIOSignal", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.POINTER(PCO_Signal)],
            argnames = ["ph", "wSignalNum", "pstrSignal"] )
    #  ctypes.c_int PCO_SetHWIOSignal(HANDLE ph, WORD wSignalNum, ctypes.POINTER(PCO_Signal) pstrSignal)
    addfunc(lib, "PCO_SetHWIOSignal", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.POINTER(PCO_Signal)],
            argnames = ["ph", "wSignalNum", "pstrSignal"] )
    #  ctypes.c_int PCO_GetImageTiming(HANDLE ph, ctypes.POINTER(PCO_ImageTiming) pstrImageTiming)
    addfunc(lib, "PCO_GetImageTiming", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_ImageTiming)],
            argnames = ["ph", "pstrImageTiming"] )
    #  ctypes.c_int PCO_GetCameraSynchMode(HANDLE ph, ctypes.POINTER(WORD) wCameraSynchMode)
    addfunc(lib, "PCO_GetCameraSynchMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wCameraSynchMode"] )
    #  ctypes.c_int PCO_SetCameraSynchMode(HANDLE ph, WORD wCameraSynchMode)
    addfunc(lib, "PCO_SetCameraSynchMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wCameraSynchMode"] )
    #  ctypes.c_int PCO_GetFastTimingMode(HANDLE hCam, ctypes.POINTER(WORD) wFastTimingMode)
    addfunc(lib, "PCO_GetFastTimingMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["hCam", "wFastTimingMode"] )
    #  ctypes.c_int PCO_SetFastTimingMode(HANDLE hCam, WORD wFastTimingMode)
    addfunc(lib, "PCO_SetFastTimingMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["hCam", "wFastTimingMode"] )
    #  ctypes.c_int PCO_GetSensorSignalStatus(HANDLE hCam, ctypes.POINTER(DWORD) dwStatus, ctypes.POINTER(DWORD) dwImageCount, ctypes.POINTER(DWORD) dwReserved1, ctypes.POINTER(DWORD) dwReserved2)
    addfunc(lib, "PCO_GetSensorSignalStatus", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD), ctypes.POINTER(DWORD), ctypes.POINTER(DWORD), ctypes.POINTER(DWORD)],
            argnames = ["hCam", "dwStatus", "dwImageCount", "dwReserved1", "dwReserved2"] )
    #  ctypes.c_int PCO_GetCmosLineTiming(HANDLE hCam, ctypes.POINTER(WORD) wParameter, ctypes.POINTER(WORD) wTimeBase, ctypes.POINTER(DWORD) dwLineTime, ctypes.POINTER(DWORD) dwReserved, WORD wReservedLen)
    addfunc(lib, "PCO_GetCmosLineTiming", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(DWORD), ctypes.POINTER(DWORD), WORD],
            argnames = ["hCam", "wParameter", "wTimeBase", "dwLineTime", "dwReserved", "wReservedLen"] )
    #  ctypes.c_int PCO_SetCmosLineTiming(HANDLE hCam, WORD wParameter, WORD wTimeBase, DWORD dwLineTime, ctypes.POINTER(DWORD) dwReserved, WORD wReservedLen)
    addfunc(lib, "PCO_SetCmosLineTiming", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD, DWORD, ctypes.POINTER(DWORD), WORD],
            argnames = ["hCam", "wParameter", "wTimeBase", "dwLineTime", "dwReserved", "wReservedLen"] )
    #  ctypes.c_int PCO_GetCmosLineExposureDelay(HANDLE hCam, ctypes.POINTER(DWORD) dwExposureLines, ctypes.POINTER(DWORD) dwDelayLines, ctypes.POINTER(DWORD) dwReserved, WORD wReservedLen)
    addfunc(lib, "PCO_GetCmosLineExposureDelay", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD), ctypes.POINTER(DWORD), ctypes.POINTER(DWORD), WORD],
            argnames = ["hCam", "dwExposureLines", "dwDelayLines", "dwReserved", "wReservedLen"] )
    #  ctypes.c_int PCO_SetCmosLineExposureDelay(HANDLE hCam, DWORD dwExposureLines, DWORD dwDelayLines, ctypes.POINTER(DWORD) dwReserved, WORD wReservedLen)
    addfunc(lib, "PCO_SetCmosLineExposureDelay", restype = ctypes.c_int,
            argtypes = [HANDLE, DWORD, DWORD, ctypes.POINTER(DWORD), WORD],
            argnames = ["hCam", "dwExposureLines", "dwDelayLines", "dwReserved", "wReservedLen"] )
    #  ctypes.c_int PCO_GetIntensifiedLoopCount(HANDLE hCam, ctypes.POINTER(WORD) wIntensifiedLoopCount, ctypes.POINTER(WORD) wReserved)
    addfunc(lib, "PCO_GetIntensifiedLoopCount", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["hCam", "wIntensifiedLoopCount", "wReserved"] )
    #  ctypes.c_int PCO_SetIntensifiedLoopCount(HANDLE hCam, WORD wIntensifiedLoopCount, WORD wReserved)
    addfunc(lib, "PCO_SetIntensifiedLoopCount", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD],
            argnames = ["hCam", "wIntensifiedLoopCount", "wReserved"] )
    #  ctypes.c_int PCO_GetStorageStruct(HANDLE ph, ctypes.POINTER(PCO_Storage) strStorage)
    addfunc(lib, "PCO_GetStorageStruct", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_Storage)],
            argnames = ["ph", "strStorage"] )
    #  ctypes.c_int PCO_SetStorageStruct(HANDLE ph, ctypes.POINTER(PCO_Storage) strStorage)
    addfunc(lib, "PCO_SetStorageStruct", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_Storage)],
            argnames = ["ph", "strStorage"] )
    #  ctypes.c_int PCO_GetCameraRamSize(HANDLE ph, ctypes.POINTER(DWORD) dwRamSize, ctypes.POINTER(WORD) wPageSize)
    addfunc(lib, "PCO_GetCameraRamSize", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "dwRamSize", "wPageSize"] )
    #  ctypes.c_int PCO_GetCameraRamSegmentSize(HANDLE ph, ctypes.POINTER(DWORD) dwRamSegSize)
    addfunc(lib, "PCO_GetCameraRamSegmentSize", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD)],
            argnames = ["ph", "dwRamSegSize"] )
    #  ctypes.c_int PCO_SetCameraRamSegmentSize(HANDLE ph, ctypes.POINTER(DWORD) dwRamSegSize)
    addfunc(lib, "PCO_SetCameraRamSegmentSize", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD)],
            argnames = ["ph", "dwRamSegSize"] )
    #  ctypes.c_int PCO_ClearRamSegment(HANDLE ph)
    addfunc(lib, "PCO_ClearRamSegment", restype = ctypes.c_int,
            argtypes = [HANDLE],
            argnames = ["ph"] )
    #  ctypes.c_int PCO_GetActiveRamSegment(HANDLE ph, ctypes.POINTER(WORD) wActSeg)
    addfunc(lib, "PCO_GetActiveRamSegment", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wActSeg"] )
    #  ctypes.c_int PCO_SetActiveRamSegment(HANDLE ph, WORD wActSeg)
    addfunc(lib, "PCO_SetActiveRamSegment", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wActSeg"] )
    #  ctypes.c_int PCO_GetRecordingStruct(HANDLE ph, ctypes.POINTER(PCO_Recording) strRecording)
    addfunc(lib, "PCO_GetRecordingStruct", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_Recording)],
            argnames = ["ph", "strRecording"] )
    #  ctypes.c_int PCO_SetRecordingStruct(HANDLE ph, ctypes.POINTER(PCO_Recording) strRecording)
    addfunc(lib, "PCO_SetRecordingStruct", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_Recording)],
            argnames = ["ph", "strRecording"] )
    #  ctypes.c_int PCO_GetStorageMode(HANDLE ph, ctypes.POINTER(WORD) wStorageMode)
    addfunc(lib, "PCO_GetStorageMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wStorageMode"] )
    #  ctypes.c_int PCO_SetStorageMode(HANDLE ph, WORD wStorageMode)
    addfunc(lib, "PCO_SetStorageMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wStorageMode"] )
    #  ctypes.c_int PCO_GetRecorderSubmode(HANDLE ph, ctypes.POINTER(WORD) wRecSubmode)
    addfunc(lib, "PCO_GetRecorderSubmode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wRecSubmode"] )
    #  ctypes.c_int PCO_SetRecorderSubmode(HANDLE ph, WORD wRecSubmode)
    addfunc(lib, "PCO_SetRecorderSubmode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wRecSubmode"] )
    #  ctypes.c_int PCO_GetRecordingState(HANDLE ph, ctypes.POINTER(WORD) wRecState)
    addfunc(lib, "PCO_GetRecordingState", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wRecState"] )
    #  ctypes.c_int PCO_SetRecordingState(HANDLE ph, WORD wRecState)
    addfunc(lib, "PCO_SetRecordingState", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wRecState"] )
    #  ctypes.c_int PCO_ArmCamera(HANDLE ph)
    addfunc(lib, "PCO_ArmCamera", restype = ctypes.c_int,
            argtypes = [HANDLE],
            argnames = ["ph"] )
    #  ctypes.c_int PCO_GetAcquireMode(HANDLE ph, ctypes.POINTER(WORD) wAcquMode)
    addfunc(lib, "PCO_GetAcquireMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wAcquMode"] )
    #  ctypes.c_int PCO_SetAcquireMode(HANDLE ph, WORD wAcquMode)
    addfunc(lib, "PCO_SetAcquireMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wAcquMode"] )
    #  ctypes.c_int PCO_GetAcquireModeEx(HANDLE ph, ctypes.POINTER(WORD) wAcquMode, ctypes.POINTER(DWORD) dwNumberImages, ctypes.POINTER(DWORD) dwReserved)
    addfunc(lib, "PCO_GetAcquireModeEx", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(DWORD), ctypes.POINTER(DWORD)],
            argnames = ["ph", "wAcquMode", "dwNumberImages", "dwReserved"] )
    #  ctypes.c_int PCO_SetAcquireModeEx(HANDLE ph, WORD wAcquMode, DWORD dwNumberImages, ctypes.POINTER(DWORD) dwReserved)
    addfunc(lib, "PCO_SetAcquireModeEx", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, DWORD, ctypes.POINTER(DWORD)],
            argnames = ["ph", "wAcquMode", "dwNumberImages", "dwReserved"] )
    #  ctypes.c_int PCO_GetAcqEnblSignalStatus(HANDLE ph, ctypes.POINTER(WORD) wAcquEnableState)
    addfunc(lib, "PCO_GetAcqEnblSignalStatus", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wAcquEnableState"] )
    #  ctypes.c_int PCO_SetDateTime(HANDLE ph, BYTE ucDay, BYTE ucMonth, WORD wYear, WORD wHour, BYTE ucMin, BYTE ucSec)
    addfunc(lib, "PCO_SetDateTime", restype = ctypes.c_int,
            argtypes = [HANDLE, BYTE, BYTE, WORD, WORD, BYTE, BYTE],
            argnames = ["ph", "ucDay", "ucMonth", "wYear", "wHour", "ucMin", "ucSec"] )
    #  ctypes.c_int PCO_GetTimestampMode(HANDLE ph, ctypes.POINTER(WORD) wTimeStampMode)
    addfunc(lib, "PCO_GetTimestampMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wTimeStampMode"] )
    #  ctypes.c_int PCO_SetTimestampMode(HANDLE ph, WORD wTimeStampMode)
    addfunc(lib, "PCO_SetTimestampMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wTimeStampMode"] )
    #  ctypes.c_int PCO_GetRecordStopEvent(HANDLE ph, ctypes.POINTER(WORD) wRecordStopEventMode, ctypes.POINTER(DWORD) dwRecordStopDelayImages)
    addfunc(lib, "PCO_GetRecordStopEvent", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(DWORD)],
            argnames = ["ph", "wRecordStopEventMode", "dwRecordStopDelayImages"] )
    #  ctypes.c_int PCO_SetRecordStopEvent(HANDLE ph, WORD wRecordStopEventMode, DWORD dwRecordStopDelayImages)
    addfunc(lib, "PCO_SetRecordStopEvent", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, DWORD],
            argnames = ["ph", "wRecordStopEventMode", "dwRecordStopDelayImages"] )
    #  ctypes.c_int PCO_StopRecord(HANDLE ph, ctypes.POINTER(WORD) wReserved0, ctypes.POINTER(DWORD) dwReserved1)
    addfunc(lib, "PCO_StopRecord", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(DWORD)],
            argnames = ["ph", "wReserved0", "dwReserved1"] )
    #  ctypes.c_int PCO_GetImageStruct(HANDLE ph, ctypes.POINTER(PCO_Image) strImage)
    addfunc(lib, "PCO_GetImageStruct", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_Image)],
            argnames = ["ph", "strImage"] )
    #  ctypes.c_int PCO_GetSegmentStruct(HANDLE ph, WORD wSegment, ctypes.POINTER(PCO_Segment) strSegment)
    addfunc(lib, "PCO_GetSegmentStruct", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.POINTER(PCO_Segment)],
            argnames = ["ph", "wSegment", "strSegment"] )
    #  ctypes.c_int PCO_GetSegmentImageSettings(HANDLE ph, WORD wSegment, ctypes.POINTER(WORD) wXRes, ctypes.POINTER(WORD) wYRes, ctypes.POINTER(WORD) wBinHorz, ctypes.POINTER(WORD) wBinVert, ctypes.POINTER(WORD) wRoiX0, ctypes.POINTER(WORD) wRoiY0, ctypes.POINTER(WORD) wRoiX1, ctypes.POINTER(WORD) wRoiY1)
    addfunc(lib, "PCO_GetSegmentImageSettings", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wSegment", "wXRes", "wYRes", "wBinHorz", "wBinVert", "wRoiX0", "wRoiY0", "wRoiX1", "wRoiY1"] )
    #  ctypes.c_int PCO_GetNumberOfImagesInSegment(HANDLE ph, WORD wSegment, ctypes.POINTER(DWORD) dwValidImageCnt, ctypes.POINTER(DWORD) dwMaxImageCnt)
    addfunc(lib, "PCO_GetNumberOfImagesInSegment", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.POINTER(DWORD), ctypes.POINTER(DWORD)],
            argnames = ["ph", "wSegment", "dwValidImageCnt", "dwMaxImageCnt"] )
    #  ctypes.c_int PCO_GetBitAlignment(HANDLE ph, ctypes.POINTER(WORD) wBitAlignment)
    addfunc(lib, "PCO_GetBitAlignment", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wBitAlignment"] )
    #  ctypes.c_int PCO_SetBitAlignment(HANDLE ph, WORD wBitAlignment)
    addfunc(lib, "PCO_SetBitAlignment", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wBitAlignment"] )
    #  ctypes.c_int PCO_GetHotPixelCorrectionMode(HANDLE ph, ctypes.POINTER(WORD) wHotPixelCorrectionMode)
    addfunc(lib, "PCO_GetHotPixelCorrectionMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD)],
            argnames = ["ph", "wHotPixelCorrectionMode"] )
    #  ctypes.c_int PCO_SetHotPixelCorrectionMode(HANDLE ph, WORD wHotPixelCorrectionMode)
    addfunc(lib, "PCO_SetHotPixelCorrectionMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wHotPixelCorrectionMode"] )
    #  ctypes.c_int PCO_PlayImagesFromSegmentHDSDI(HANDLE ph, WORD wSegment, WORD wInterface, WORD wMode, WORD wSpeed, DWORD dwRangeLow, DWORD dwRangeHigh, DWORD dwStartPos)
    addfunc(lib, "PCO_PlayImagesFromSegmentHDSDI", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD, WORD, WORD, DWORD, DWORD, DWORD],
            argnames = ["ph", "wSegment", "wInterface", "wMode", "wSpeed", "dwRangeLow", "dwRangeHigh", "dwStartPos"] )
    #  ctypes.c_int PCO_GetPlayPositionHDSDI(HANDLE ph, ctypes.POINTER(WORD) wStatus, ctypes.POINTER(DWORD) dwPlayPosition)
    addfunc(lib, "PCO_GetPlayPositionHDSDI", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(DWORD)],
            argnames = ["ph", "wStatus", "dwPlayPosition"] )
    #  ctypes.c_int PCO_GetInterfaceOutputFormat(HANDLE ph, ctypes.POINTER(WORD) wDestInterface, ctypes.POINTER(WORD) wFormat, ctypes.POINTER(WORD) wReserved1, ctypes.POINTER(WORD) wReserved2)
    addfunc(lib, "PCO_GetInterfaceOutputFormat", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wDestInterface", "wFormat", "wReserved1", "wReserved2"] )
    #  ctypes.c_int PCO_SetInterfaceOutputFormat(HANDLE ph, WORD wDestInterface, WORD wFormat, WORD wReserved1, WORD wReserved2)
    addfunc(lib, "PCO_SetInterfaceOutputFormat", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD, WORD, WORD],
            argnames = ["ph", "wDestInterface", "wFormat", "wReserved1", "wReserved2"] )
    #  ctypes.c_int PCO_GetMetaDataMode(HANDLE ph, ctypes.POINTER(WORD) wMetaDataMode, ctypes.POINTER(WORD) wMetaDataSize, ctypes.POINTER(WORD) wMetaDataVersion)
    addfunc(lib, "PCO_GetMetaDataMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wMetaDataMode", "wMetaDataSize", "wMetaDataVersion"] )
    #  ctypes.c_int PCO_SetMetaDataMode(HANDLE ph, WORD wMetaDataMode, ctypes.POINTER(WORD) wMetaDataSize, ctypes.POINTER(WORD) wMetaDataVersion)
    addfunc(lib, "PCO_SetMetaDataMode", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wMetaDataMode", "wMetaDataSize", "wMetaDataVersion"] )
    #  ctypes.c_int PCO_SetColorSettings(HANDLE ph, ctypes.POINTER(PCO_Image_ColorSet) strColorSet)
    addfunc(lib, "PCO_SetColorSettings", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_Image_ColorSet)],
            argnames = ["ph", "strColorSet"] )
    #  ctypes.c_int PCO_GetColorSettings(HANDLE ph, ctypes.POINTER(PCO_Image_ColorSet) strColorSet)
    addfunc(lib, "PCO_GetColorSettings", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_Image_ColorSet)],
            argnames = ["ph", "strColorSet"] )
    #  ctypes.c_int PCO_DoWhiteBalance(HANDLE ph, WORD wMode, ctypes.POINTER(WORD) wParam, WORD wParamLen)
    addfunc(lib, "PCO_DoWhiteBalance", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.POINTER(WORD), WORD],
            argnames = ["ph", "wMode", "wParam", "wParamLen"] )
    #  ctypes.c_int PCO_OpenCamera(ctypes.POINTER(HANDLE) ph, WORD wCamNum)
    addfunc(lib, "PCO_OpenCamera", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(HANDLE), WORD],
            argnames = ["ph", "wCamNum"] )
    #  ctypes.c_int PCO_OpenCameraEx(ctypes.POINTER(HANDLE) ph, ctypes.POINTER(PCO_OpenStruct) strOpenStruct)
    addfunc(lib, "PCO_OpenCameraEx", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(HANDLE), ctypes.POINTER(PCO_OpenStruct)],
            argnames = ["ph", "strOpenStruct"] )
    #  ctypes.c_int PCO_CloseCamera(HANDLE ph)
    addfunc(lib, "PCO_CloseCamera", restype = ctypes.c_int,
            argtypes = [HANDLE],
            argnames = ["ph"] )
    #  ctypes.c_int PCO_AllocateBuffer(HANDLE ph, ctypes.POINTER(SHORT) sBufNr, DWORD size, ctypes.POINTER(ctypes.POINTER(WORD)) wBuf, ctypes.POINTER(HANDLE) hEvent)
    addfunc(lib, "PCO_AllocateBuffer", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(SHORT), DWORD, ctypes.POINTER(ctypes.POINTER(WORD)), ctypes.POINTER(HANDLE)],
            argnames = ["ph", "sBufNr", "size", "wBuf", "hEvent"] )
    #  ctypes.c_int PCO_WaitforBuffer(HANDLE ph, ctypes.c_int nr_of_buffer, ctypes.POINTER(PCO_Buflist) bl, ctypes.c_int timeout)
    addfunc(lib, "PCO_WaitforBuffer", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.c_int, ctypes.POINTER(PCO_Buflist), ctypes.c_int],
            argnames = ["ph", "nr_of_buffer", "bl", "timeout"] )
    #  ctypes.c_int PCO_GetBuffer(HANDLE ph, SHORT sBufNr, ctypes.POINTER(ctypes.POINTER(WORD)) wBuf, ctypes.POINTER(HANDLE) hEvent)
    addfunc(lib, "PCO_GetBuffer", restype = ctypes.c_int,
            argtypes = [HANDLE, SHORT, ctypes.POINTER(ctypes.POINTER(WORD)), ctypes.POINTER(HANDLE)],
            argnames = ["ph", "sBufNr", "wBuf", "hEvent"] )
    #  ctypes.c_int PCO_FreeBuffer(HANDLE ph, SHORT sBufNr)
    addfunc(lib, "PCO_FreeBuffer", restype = ctypes.c_int,
            argtypes = [HANDLE, SHORT],
            argnames = ["ph", "sBufNr"] )
    #  ctypes.c_int PCO_AddBuffer(HANDLE ph, DWORD dw1stImage, DWORD dwLastImage, SHORT sBufNr)
    addfunc(lib, "PCO_AddBuffer", restype = ctypes.c_int,
            argtypes = [HANDLE, DWORD, DWORD, SHORT],
            argnames = ["ph", "dw1stImage", "dwLastImage", "sBufNr"] )
    #  ctypes.c_int PCO_AddBufferEx(HANDLE ph, DWORD dw1stImage, DWORD dwLastImage, SHORT sBufNr, WORD wXRes, WORD wYRes, WORD wBitPerPixel)
    addfunc(lib, "PCO_AddBufferEx", restype = ctypes.c_int,
            argtypes = [HANDLE, DWORD, DWORD, SHORT, WORD, WORD, WORD],
            argnames = ["ph", "dw1stImage", "dwLastImage", "sBufNr", "wXRes", "wYRes", "wBitPerPixel"] )
    #  ctypes.c_int PCO_GetBufferStatus(HANDLE ph, SHORT sBufNr, ctypes.POINTER(DWORD) dwStatusDll, ctypes.POINTER(DWORD) dwStatusDrv)
    addfunc(lib, "PCO_GetBufferStatus", restype = ctypes.c_int,
            argtypes = [HANDLE, SHORT, ctypes.POINTER(DWORD), ctypes.POINTER(DWORD)],
            argnames = ["ph", "sBufNr", "dwStatusDll", "dwStatusDrv"] )
    #  ctypes.c_int PCO_CancelImages(HANDLE ph)
    addfunc(lib, "PCO_CancelImages", restype = ctypes.c_int,
            argtypes = [HANDLE],
            argnames = ["ph"] )
    #  ctypes.c_int PCO_RemoveBuffer(HANDLE ph)
    addfunc(lib, "PCO_RemoveBuffer", restype = ctypes.c_int,
            argtypes = [HANDLE],
            argnames = ["ph"] )
    #  ctypes.c_int PCO_GetImage(HANDLE ph, WORD wSegment, DWORD dw1stImage, DWORD dwLastImage, SHORT sBufNr)
    addfunc(lib, "PCO_GetImage", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, DWORD, DWORD, SHORT],
            argnames = ["ph", "wSegment", "dw1stImage", "dwLastImage", "sBufNr"] )
    #  ctypes.c_int PCO_GetImageEx(HANDLE ph, WORD wSegment, DWORD dw1stImage, DWORD dwLastImage, SHORT sBufNr, WORD wXRes, WORD wYRes, WORD wBitPerPixel)
    addfunc(lib, "PCO_GetImageEx", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, DWORD, DWORD, SHORT, WORD, WORD, WORD],
            argnames = ["ph", "wSegment", "dw1stImage", "dwLastImage", "sBufNr", "wXRes", "wYRes", "wBitPerPixel"] )
    #  ctypes.c_int PCO_GetPendingBuffer(HANDLE ph, ctypes.POINTER(ctypes.c_int) count)
    addfunc(lib, "PCO_GetPendingBuffer", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(ctypes.c_int)],
            argnames = ["ph", "count"] )
    #  ctypes.c_int PCO_CheckDeviceAvailability(HANDLE ph, WORD wNum)
    addfunc(lib, "PCO_CheckDeviceAvailability", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD],
            argnames = ["ph", "wNum"] )
    #  ctypes.c_int PCO_SetTransferParameter(HANDLE ph, ctypes.c_void_p buffer, ctypes.c_int ilen)
    addfunc(lib, "PCO_SetTransferParameter", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.c_void_p, ctypes.c_int],
            argnames = ["ph", "buffer", "ilen"] )
    #  ctypes.c_int PCO_GetTransferParameter(HANDLE ph, ctypes.c_void_p buffer, ctypes.c_int ilen)
    addfunc(lib, "PCO_GetTransferParameter", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.c_void_p, ctypes.c_int],
            argnames = ["ph", "buffer", "ilen"] )
    #  ctypes.c_int PCO_SetTransferParametersAuto(HANDLE ph, ctypes.c_void_p buffer, ctypes.c_int ilen)
    addfunc(lib, "PCO_SetTransferParametersAuto", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.c_void_p, ctypes.c_int],
            argnames = ["ph", "buffer", "ilen"] )
    #  ctypes.c_int PCO_CamLinkSetImageParameters(HANDLE ph, WORD wxres, WORD wyres)
    addfunc(lib, "PCO_CamLinkSetImageParameters", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD],
            argnames = ["ph", "wxres", "wyres"] )
    #  ctypes.c_int PCO_SetImageParameters(HANDLE ph, WORD wxres, WORD wyres, DWORD dwflags, ctypes.c_void_p param, ctypes.c_int ilen)
    addfunc(lib, "PCO_SetImageParameters", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD, DWORD, ctypes.c_void_p, ctypes.c_int],
            argnames = ["ph", "wxres", "wyres", "dwflags", "param", "ilen"] )
    #  ctypes.c_int PCO_SetTimeouts(HANDLE ph, ctypes.c_void_p buf_in, ctypes.c_uint size_in)
    addfunc(lib, "PCO_SetTimeouts", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.c_void_p, ctypes.c_uint],
            argnames = ["ph", "buf_in", "size_in"] )
    #  ctypes.c_int PCO_GetImageTransferMode(HANDLE ph, ctypes.c_void_p param, ctypes.c_int ilen)
    addfunc(lib, "PCO_GetImageTransferMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.c_void_p, ctypes.c_int],
            argnames = ["ph", "param", "ilen"] )
    #  ctypes.c_int PCO_SetImageTransferMode(HANDLE ph, ctypes.c_void_p param, ctypes.c_int ilen)
    addfunc(lib, "PCO_SetImageTransferMode", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.c_void_p, ctypes.c_int],
            argnames = ["ph", "param", "ilen"] )
    #  ctypes.c_int PCO_AddBufferExtern(HANDLE ph, HANDLE hEvent, WORD wActSeg, DWORD dw1stImage, DWORD dwLastImage, DWORD dwSynch, ctypes.c_void_p pBuf, DWORD dwLen, ctypes.POINTER(DWORD) dwStatus)
    addfunc(lib, "PCO_AddBufferExtern", restype = ctypes.c_int,
            argtypes = [HANDLE, HANDLE, WORD, DWORD, DWORD, DWORD, ctypes.c_void_p, DWORD, ctypes.POINTER(DWORD)],
            argnames = ["ph", "hEvent", "wActSeg", "dw1stImage", "dwLastImage", "dwSynch", "pBuf", "dwLen", "dwStatus"] )
    #  ctypes.c_int PCO_GetMetaData(HANDLE ph, SHORT sBufNr, ctypes.POINTER(PCO_METADATA_STRUCT) pMetaData, DWORD dwReserved1, DWORD dwReserved2)
    addfunc(lib, "PCO_GetMetaData", restype = ctypes.c_int,
            argtypes = [HANDLE, SHORT, ctypes.POINTER(PCO_METADATA_STRUCT), DWORD, DWORD],
            argnames = ["ph", "sBufNr", "pMetaData", "dwReserved1", "dwReserved2"] )
    #  ctypes.c_int PCO_GetDeviceStatus(HANDLE ph, WORD wNum, ctypes.POINTER(DWORD) dwStatus, WORD wStatusLen)
    addfunc(lib, "PCO_GetDeviceStatus", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.POINTER(DWORD), WORD],
            argnames = ["ph", "wNum", "dwStatus", "wStatusLen"] )
    #  ctypes.c_int PCO_ControlCommandCall(HANDLE ph, ctypes.c_void_p buf_in, ctypes.c_uint size_in, ctypes.c_void_p buf_out, ctypes.c_uint size_out)
    addfunc(lib, "PCO_ControlCommandCall", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint],
            argnames = ["ph", "buf_in", "size_in", "buf_out", "size_out"] )
    #  ctypes.c_int PCO_ResetLib()
    addfunc(lib, "PCO_ResetLib", restype = ctypes.c_int,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int PCO_EnableSoftROI(HANDLE ph, WORD wSoftROIFlags, ctypes.c_void_p unnamed_argument_001, ctypes.c_int unnamed_argument_002)
    addfunc(lib, "PCO_EnableSoftROI", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, ctypes.c_void_p, ctypes.c_int],
            argnames = ["ph", "wSoftROIFlags", "unnamed_argument_001", "unnamed_argument_002"] )
    #  ctypes.c_int PCO_GetAPIManagement(HANDLE ph, ctypes.POINTER(WORD) wFlags, ctypes.POINTER(PCO_APIManagement) pstrApi)
    addfunc(lib, "PCO_GetAPIManagement", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(PCO_APIManagement)],
            argnames = ["ph", "wFlags", "pstrApi"] )
    #  None PCO_GetErrorTextSDK(DWORD dwError, ctypes.c_char_p pszErrorString, DWORD dwErrorStringLength)
    addfunc(lib, "PCO_GetErrorTextSDK", restype = None,
            argtypes = [DWORD, ctypes.c_char_p, DWORD],
            argnames = ["dwError", "pszErrorString", "dwErrorStringLength"] )
    #  ctypes.c_int PCO_GetFlimModulationParameter(HANDLE ph, ctypes.POINTER(WORD) wSourceSelect, ctypes.POINTER(WORD) wOutputWaveform, ctypes.POINTER(WORD) wReserved1, ctypes.POINTER(WORD) wReserved2)
    addfunc(lib, "PCO_GetFlimModulationParameter", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wSourceSelect", "wOutputWaveform", "wReserved1", "wReserved2"] )
    #  ctypes.c_int PCO_SetFlimModulationParameter(HANDLE ph, WORD wSourceSelect, WORD wOutputWaveform, WORD wReserved1, WORD wReserved2)
    addfunc(lib, "PCO_SetFlimModulationParameter", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD, WORD, WORD],
            argnames = ["ph", "wSourceSelect", "wOutputWaveform", "wReserved1", "wReserved2"] )
    #  ctypes.c_int PCO_GetFlimPhaseSequenceParameter(HANDLE ph, ctypes.POINTER(WORD) wPhaseNumber, ctypes.POINTER(WORD) wPhaseSymmetry, ctypes.POINTER(WORD) wPhaseOrder, ctypes.POINTER(WORD) wTapSelect, ctypes.POINTER(WORD) wReserved1, ctypes.POINTER(WORD) wReserved2)
    addfunc(lib, "PCO_GetFlimPhaseSequenceParameter", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wPhaseNumber", "wPhaseSymmetry", "wPhaseOrder", "wTapSelect", "wReserved1", "wReserved2"] )
    #  ctypes.c_int PCO_SetFlimPhaseSequenceParameter(HANDLE ph, WORD wPhaseNumber, WORD wPhaseSymmetry, WORD wPhaseOrder, WORD wTapSelect, WORD wReserved1, WORD wReserved2)
    addfunc(lib, "PCO_SetFlimPhaseSequenceParameter", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD, WORD, WORD, WORD, WORD],
            argnames = ["ph", "wPhaseNumber", "wPhaseSymmetry", "wPhaseOrder", "wTapSelect", "wReserved1", "wReserved2"] )
    #  ctypes.c_int PCO_GetFlimImageProcessingFlow(HANDLE ph, ctypes.POINTER(WORD) wAsymmetryCorrection, ctypes.POINTER(WORD) wCalculationMode, ctypes.POINTER(WORD) wReferencingMode, ctypes.POINTER(WORD) wThresholdLow, ctypes.POINTER(WORD) wThresholdHigh, ctypes.POINTER(WORD) wOutputMode, ctypes.POINTER(WORD) wReserved1, ctypes.POINTER(WORD) wReserved2, ctypes.POINTER(WORD) wReserved3, ctypes.POINTER(WORD) wReserved4)
    addfunc(lib, "PCO_GetFlimImageProcessingFlow", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(WORD)],
            argnames = ["ph", "wAsymmetryCorrection", "wCalculationMode", "wReferencingMode", "wThresholdLow", "wThresholdHigh", "wOutputMode", "wReserved1", "wReserved2", "wReserved3", "wReserved4"] )
    #  ctypes.c_int PCO_SetFlimImageProcessingFlow(HANDLE ph, WORD wAsymmetryCorrection, WORD wCalculationMode, WORD wReferencingMode, WORD wThresholdLow, WORD wThresholdHigh, WORD wOutputMode, WORD wReserved1, WORD wReserved2, WORD wReserved3, WORD wReserved4)
    addfunc(lib, "PCO_SetFlimImageProcessingFlow", restype = ctypes.c_int,
            argtypes = [HANDLE, WORD, WORD, WORD, WORD, WORD, WORD, WORD, WORD, WORD, WORD],
            argnames = ["ph", "wAsymmetryCorrection", "wCalculationMode", "wReferencingMode", "wThresholdLow", "wThresholdHigh", "wOutputMode", "wReserved1", "wReserved2", "wReserved3", "wReserved4"] )
    #  ctypes.c_int PCO_GetFlimMasterModulationFrequency(HANDLE ph, ctypes.POINTER(DWORD) dwFrequency)
    addfunc(lib, "PCO_GetFlimMasterModulationFrequency", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD)],
            argnames = ["ph", "dwFrequency"] )
    #  ctypes.c_int PCO_SetFlimMasterModulationFrequency(HANDLE ph, DWORD dwFrequency)
    addfunc(lib, "PCO_SetFlimMasterModulationFrequency", restype = ctypes.c_int,
            argtypes = [HANDLE, DWORD],
            argnames = ["ph", "dwFrequency"] )
    #  ctypes.c_int PCO_GetFlimRelativePhase(HANDLE ph, ctypes.POINTER(DWORD) dwPhaseMilliDeg)
    addfunc(lib, "PCO_GetFlimRelativePhase", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD)],
            argnames = ["ph", "dwPhaseMilliDeg"] )
    #  ctypes.c_int PCO_SetFlimRelativePhase(HANDLE ph, DWORD dwPhaseMilliDeg)
    addfunc(lib, "PCO_SetFlimRelativePhase", restype = ctypes.c_int,
            argtypes = [HANDLE, DWORD],
            argnames = ["ph", "dwPhaseMilliDeg"] )
    #  ctypes.c_int PCO_InitLensControl(HANDLE hCamera, ctypes.POINTER(HANDLE) phLensControl)
    addfunc(lib, "PCO_InitLensControl", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(HANDLE)],
            argnames = ["hCamera", "phLensControl"] )
    #  ctypes.c_int PCO_CleanupLensControl()
    addfunc(lib, "PCO_CleanupLensControl", restype = ctypes.c_int,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int PCO_CloseLensControl(HANDLE hLensControl)
    addfunc(lib, "PCO_CloseLensControl", restype = ctypes.c_int,
            argtypes = [HANDLE],
            argnames = ["hLensControl"] )
    #  ctypes.c_int PCO_GetLensFocus(HANDLE hLens, ctypes.POINTER(LONG) lFocusPos, ctypes.POINTER(DWORD) dwflags)
    addfunc(lib, "PCO_GetLensFocus", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(LONG), ctypes.POINTER(DWORD)],
            argnames = ["hLens", "lFocusPos", "dwflags"] )
    #  ctypes.c_int PCO_SetLensFocus(HANDLE hLens, ctypes.POINTER(LONG) lFocusPos, DWORD dwflagsin, ctypes.POINTER(DWORD) dwflagsout)
    addfunc(lib, "PCO_SetLensFocus", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(LONG), DWORD, ctypes.POINTER(DWORD)],
            argnames = ["hLens", "lFocusPos", "dwflagsin", "dwflagsout"] )
    #  ctypes.c_int PCO_GetAperture(HANDLE hLens, ctypes.POINTER(WORD) wAperturePos, ctypes.POINTER(DWORD) dwflags)
    addfunc(lib, "PCO_GetAperture", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), ctypes.POINTER(DWORD)],
            argnames = ["hLens", "wAperturePos", "dwflags"] )
    #  ctypes.c_int PCO_SetAperture(HANDLE hLens, ctypes.POINTER(WORD) wAperturePos, DWORD dwflagsin, ctypes.POINTER(DWORD) dwflagsout)
    addfunc(lib, "PCO_SetAperture", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(WORD), DWORD, ctypes.POINTER(DWORD)],
            argnames = ["hLens", "wAperturePos", "dwflagsin", "dwflagsout"] )
    #  ctypes.c_int PCO_GetApertureF(HANDLE hLens, ctypes.POINTER(DWORD) dwfAperturePos, ctypes.POINTER(WORD) wAperturePos, ctypes.POINTER(DWORD) dwflags)
    addfunc(lib, "PCO_GetApertureF", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD), ctypes.POINTER(WORD), ctypes.POINTER(DWORD)],
            argnames = ["hLens", "dwfAperturePos", "wAperturePos", "dwflags"] )
    #  ctypes.c_int PCO_SetApertureF(HANDLE hLens, ctypes.POINTER(DWORD) dwfAperturePos, DWORD dwflagsin, ctypes.POINTER(DWORD) dwflagsout)
    addfunc(lib, "PCO_SetApertureF", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(DWORD), DWORD, ctypes.POINTER(DWORD)],
            argnames = ["hLens", "dwfAperturePos", "dwflagsin", "dwflagsout"] )
    #  ctypes.c_int PCO_SendBirgerCommand(HANDLE hLens, ctypes.POINTER(PCO_Birger) pstrBirger, ctypes.c_char_p szcmd, ctypes.c_int inumdelim)
    addfunc(lib, "PCO_SendBirgerCommand", restype = ctypes.c_int,
            argtypes = [HANDLE, ctypes.POINTER(PCO_Birger), ctypes.c_char_p, ctypes.c_int],
            argnames = ["hLens", "pstrBirger", "szcmd", "inumdelim"] )


