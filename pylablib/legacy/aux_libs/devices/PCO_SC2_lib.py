from ...core.utils import ctypes_wrap, py3
from .misc import load_lib

import ctypes
import collections
import os.path
import platform


_depends_local=["...core.utils.ctypes_wrap"]


##### Errors #####

class PCOSC2LibError(RuntimeError):
    """Generic IMAQ error."""
    def __init__(self, func, code, lib=None):
        self.func=func
        self.code=code
        self.name="Unknown"
        self.desc=""
        try:
            if lib is not None:
                self.desc=py3.as_str(lib.PCO_GetErrorText(code))
        except PCOSC2LibError:
            pass
        self.msg="function '{}' raised error {}({}): {}".format(func,code,self.name,self.desc)
        RuntimeError.__init__(self,self.msg)
def errcheck(passing=None, lib=None):
    """
    Build an error checking function.

    Return a function which checks return codes of IMAQ library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    if passing is None:
        passing={0}
    def checker(result, func, arguments):
        if result not in passing:
            raise PCOSC2LibError(func.__name__,result,lib=lib)
        return result
    return checker



##### Types #####

HANDLE=ctypes.c_void_p
BOOL=ctypes.c_int
CHAR=ctypes.c_char
BYTE=ctypes.c_byte
SHORT=ctypes.c_short
LONG=ctypes.c_long
WORD=ctypes.c_uint16
DWORD=ctypes.c_uint32

conv_arr=lambda *args: args[0][:]
def build_arr(ctype, n=None):
	if n is None:
		def build_func(arr):
			carr=(ctype*len(arr))
			for i in range(len(arr)):
				carr[i]=arr[i]
			return carr
	else:
		def build_func(arr):
			carr=(ctype*n)
			for i in range(min(n,len(arr))):
				carr[i]=arr[i]
			return carr
	return build_func



##### Structures #####

PCO_MAXVERSIONHW=10
PCO_MAXVERSIONFW=10
class PCO_SC2_Hardware_DESC(ctypes.Structure):
	_fields_=[  ("szName",CHAR*16),
				("wBatchNo",WORD),
				("wRevision",WORD),
				("wVariant",WORD),
				("ZZwDummy",WORD*20), ]
class CPCO_SC2_Hardware_DESC(ctypes_wrap.StructWrap):
	_struct=PCO_SC2_Hardware_DESC
	_tup_exc={"ZZwDummy"}
	_tup={"szName":ctypes.string_at}

class PCO_SC2_Firmware_DESC(ctypes.Structure):
	_fields_=[  ("szName",CHAR*16),
				("bMinorRev",BYTE),
				("bMajorRev",BYTE),
				("wVariant",WORD),
				("ZZwDummy",WORD*22), ]
class CPCO_SC2_Firmware_DESC(ctypes_wrap.StructWrap):
	_struct=PCO_SC2_Firmware_DESC
	_tup_exc={"ZZwDummy"}
	_tup={"szName":ctypes.string_at}

class PCO_HW_Vers(ctypes.Structure):
	_fields_=[  ("BoardNum",WORD),
				("Board",PCO_SC2_Hardware_DESC*PCO_MAXVERSIONHW), ]
class CPCO_HW_Vers(ctypes_wrap.StructWrap):
	_struct=PCO_HW_Vers
	def tup(self):
		return [CPCO_SC2_Hardware_DESC.tup_struct(s) for s in self.Board[:self.BoardNum]]
class PCO_FW_Vers(ctypes.Structure):
	_fields_=[  ("BoardNum",WORD),
				("Board",PCO_SC2_Firmware_DESC*PCO_MAXVERSIONFW), ]
class CPCO_FW_Vers(ctypes_wrap.StructWrap):
	_struct=PCO_FW_Vers
	def tup(self):
		return [CPCO_SC2_Firmware_DESC.tup_struct(s) for s in self.Board[:self.BoardNum]]

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
				("ZZwDummy",WORD*39), ]
class CPCO_CameraType(ctypes_wrap.StructWrap):
	_struct=PCO_CameraType
	_tup_exc={"wSize","ZZwDummy"}
	_tup={"strHardwareVersion":CPCO_HW_Vers.tup_struct,"strFirmwareVersion":CPCO_FW_Vers.tup_struct}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		return struct


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
				("ZZwDummy",WORD*37), ]
class CPCO_General(ctypes_wrap.StructWrap):
	_struct=PCO_General
	_tup_exc={"wSize","ZZwAlignDummy1","ZZwDummy"}
	_tup={"strCamType":CPCO_CameraType.tup_struct}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		struct.strCamType=CPCO_CameraType.prep_struct(struct.strCamType)
		return struct


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
				("ZZdwDummy",DWORD*40), ]
class CPCO_Description(ctypes_wrap.StructWrap):
	_struct=PCO_Description
	_tup_exc={"wSize","ZZwDummycv","ZZdwDummypr","ZZdwDummy","wDummy1","wDummy2"}
	_tup={"dwPixelRateDESC":conv_arr,"wConvFactDESC":conv_arr,"sCoolingSetpoints":conv_arr,"dwExtSyncFrequency":conv_arr}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		return struct

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
				("ZZdwDummy",DWORD*41), ]
class CPCO_Description2(ctypes_wrap.StructWrap):
	_struct=PCO_Description2
	_tup_exc={"wSize","ZZwAlignDummy1","dwReserved","ZZdwDummy"}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		return struct

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
				("szIntensifierTypeDESC",CHAR*24),
				("dwMCP_RectangleXL_DESC",DWORD),
				("dwMCP_RectangleXR_DESC",DWORD),
				("dwMCP_RectangleYT_DESC",DWORD),
				("dwMCP_RectangleYB_DESC",DWORD),
				("ZZdwDummy",DWORD*23), ]
class CPCO_Description_Intensified(ctypes_wrap.StructWrap):
	_struct=PCO_Description_Intensified
	_tup_exc={"wSize","ZZdwDummy"}
	_tup={"szIntensifierTypeDESC": ctypes.string_at}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		return struct


NUM_SIGNAL_NAMES=4
class PCO_Single_Signal_Desc(ctypes.Structure):
	_fields_=[  ("wSize",WORD),
				("ZZwAlignDummy1",WORD),
				("strSignalName",(CHAR*25)*NUM_SIGNAL_NAMES),
				("wSignalDefinitions",WORD),
				("wSignalTypes",WORD),
				("wSignalPolarity",WORD),
				("wSignalFilter",WORD),
				("dwDummy",DWORD*22), ]
class CPCO_Single_Signal_Desc(ctypes_wrap.StructWrap):
	_struct=PCO_Single_Signal_Desc
	_tup_exc={"wSize","ZZwAlignDummy1","dwDummy"}
	_tup={"strSignalName": lambda s: [ctypes.string_at(ctypes.addressof(s[i])) for i in range(NUM_SIGNAL_NAMES) if s[i][0]!=b'\x00']}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		return struct
NUM_MAX_SIGNALS=20
class PCO_Signal_Description(ctypes.Structure):
	_fields_=[  ("wSize",WORD),
				("wNumOfSignals",WORD),
				("strSingeSignalDesc",PCO_Single_Signal_Desc*NUM_MAX_SIGNALS),
				("dwDummy",DWORD*524), ]
class CPCO_Signal_Description(ctypes_wrap.StructWrap):
	_struct=PCO_Signal_Description
	_tup_exc={"wSize","dwDummy"}
	def tup(self):
		return [CPCO_Single_Signal_Desc.tup_struct(s) for s in self.strSingeSignalDesc[:self.wNumOfSignals]]
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		for i in range(NUM_MAX_SIGNALS):
			struct.strSingeSignalDesc[i]=CPCO_Single_Signal_Desc.prep_struct(struct.strSingeSignalDesc[i])
		return struct


PCO_SENSORDUMMY=7
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
				("ZZdwDummy",DWORD*PCO_SENSORDUMMY),]
class CPCO_Sensor(ctypes_wrap.StructWrap):
	_struct=PCO_Sensor
	_tup_exc={"wSize","ZZwAlignDummy1","ZZdwDummy2","ZZwDummy","ZZdwDummy"}
	_tup={	"strDescription": CPCO_Description.tup_struct,
			"strDescription2": CPCO_Description2.tup_struct,
			"strDescriptionIntensified": CPCO_Description_Intensified.tup_struct,
			"strSignalDesc": CPCO_Signal_Description.tup_struct,}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		struct.strDescription=CPCO_Description.prep_struct(struct.strDescription)
		struct.strDescription2=CPCO_Description2.prep_struct(struct.strDescription2)
		struct.strDescriptionIntensified=CPCO_Description_Intensified.prep_struct(struct.strDescriptionIntensified)
		struct.strSignalDesc=CPCO_Signal_Description.prep_struct(struct.strSignalDesc)
		return struct


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
				("ZZdwDummy",DWORD*11),]
class CPCO_ImageTiming(ctypes_wrap.StructWrap):
	_struct=PCO_ImageTiming
	_tup_exc={"wSize","wDummy","ZZdwDummy"}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		return struct

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
				("ZZdwReserved",DWORD*3),]
class CPCO_Signal(ctypes_wrap.StructWrap):
	_struct=PCO_Signal
	_tup_exc={"wSize","ZZwReserved","ZZdwReserved"}
	_tup={"dwParameter":conv_arr,"dwSignalFunctionality":conv_arr}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		return struct

PCO_TIMINGDUMMY=24
PCO_MAXDELEXPTABLE=16
class PCO_Timing(ctypes.Structure):
	_fields_=[  ("wSize",WORD),
				("wTimeBaseDelay",WORD),
				("wTimeBaseExposure",WORD),
				("wCMOSParameter",WORD),
				("dwCMOSDelayLines",DWORD),
				("dwCMOSExposureLines",DWORD),
				("dwDelayTable",DWORD*PCO_MAXDELEXPTABLE),
				("ZZdwDummy1",DWORD*110),
				("dwCMOSLineTimeMin",DWORD),
				("dwCMOSLineTimeMax",DWORD),
				("dwCMOSLineTime",DWORD),
				("wCMOSTimeBase",WORD),
				("wIntensifiedLoopCount",WORD),
				("dwExposureTable",DWORD*PCO_MAXDELEXPTABLE),
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
				("strSignal",PCO_Signal*NUM_MAX_SIGNALS),
				("wStatusFrameRate",WORD),
				("wFrameRateMode",WORD),
				("dwFrameRate",DWORD),
				("dwFrameRateExposure",DWORD),
				("wTimingControlMode",WORD),
				("wFastTimingMode",WORD),
				("ZZwDummy",WORD*PCO_TIMINGDUMMY),]
class CPCO_Timing(ctypes_wrap.StructWrap):
	_struct=PCO_Timing
	_tup_exc={"wSize","ZZdwDummy1","ZZdwDummy2","ZZdwDummy3","ZZwDummy3","ZZwDummy"}
	_tup={"dwDelayTable":conv_arr,"dwExposureTable":conv_arr,"strSignal":lambda *args: [CPCO_Signal.tup_struct(s) for s in args[0]]}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		for i in range(NUM_MAX_SIGNALS):
			struct.strSignal[i]=CPCO_Signal.prep_struct(struct.strSignal[i])
		return struct


PCO_RAMSEGCNT=4
PCO_STORAGEDUMMY=39
class PCO_Storage(ctypes.Structure):
	_fields_=[  ("wSize",WORD),
				("ZZwAlignDummy1",WORD),
				("dwRamSize",DWORD),
				("wPageSize",WORD),
				("ZZwAlignDummy4",WORD),
				("dwRamSegSize",DWORD*PCO_RAMSEGCNT),
				("ZZdwDummyrs",DWORD*20),
				("wActSeg",WORD),
				("ZZwDummy",WORD*PCO_STORAGEDUMMY),]
class CPCO_Storage(ctypes_wrap.StructWrap):
	_struct=PCO_Storage
	_tup_exc={"wSize","ZZwAlignDummy1","ZZwAlignDummy4","ZZdwDummyrs","ZZwDummy"}
	_tup={"dwRamSegSize":conv_arr}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		return struct


PCO_RECORDINGDUMMY=22
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
				("ZZwDummy",WORD*PCO_RECORDINGDUMMY),]
class CPCO_Recording(ctypes_wrap.StructWrap):
	_struct=PCO_Recording
	_tup_exc={"wSize","ZZwDummy1","ZZwDummy","dwAcquModeExReserved"}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		return struct


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
				("ZZwDummy",WORD*33),]
class CPCO_Segment(ctypes_wrap.StructWrap):
	_struct=PCO_Segment
	_tup_exc={"wSize","ZZwAlignDummy1","ZZwDummy"}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		return struct

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
				("ZZwDummy",WORD*93),]
class CPCO_Image_ColorSet(ctypes_wrap.StructWrap):
	_struct=PCO_Image_ColorSet
	_tup_exc={"wSize","ZZwDummy"}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		return struct

class PCO_Image(ctypes.Structure):
	_fields_=[  ("wSize",WORD),
				("ZZwAlignDummy1",WORD),
				("strSegment",PCO_Segment*PCO_RAMSEGCNT),
				("ZZstrDummySeg",PCO_Segment*14),
				("strColorSet",PCO_Image_ColorSet),
				("wBitAlignment",WORD),
				("wHotPixelCorrectionMode",WORD),
				("ZZwDummy",WORD*38),]
class CPCO_Image(ctypes_wrap.StructWrap):
	_struct=PCO_Image
	_tup_exc={"wSize","ZZwAlignDummy1","ZZstrDummySeg","ZZwDummy"}
	_tup={"strSegment":lambda *args: [CPCO_Segment.tup_struct(s) for s in args[0]],"strColorSet":CPCO_Image_ColorSet.tup_struct}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		for i in range(PCO_RAMSEGCNT):
			struct.strSegment[i]=CPCO_Segment.prep_struct(struct.strSegment[i])
		for i in range(14):
			struct.ZZstrDummySeg[i]=CPCO_Segment.prep_struct(struct.ZZstrDummySeg[i])
		struct.strColorSet=CPCO_Image_ColorSet.prep_struct(struct.strColorSet)
		return struct


class PCO_Buflist(ctypes.Structure):
	_fields_=[  ("sBufNr",SHORT),
				("ZZwAlignDummy",WORD),
				("dwStatusDll",DWORD),
				("dwStatusDrv",DWORD),]
class CPCO_Buflist(ctypes_wrap.StructWrap):
	_struct=PCO_Buflist
	_tup_exc={"ZZwAlignDummy"}

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
				("wCOLOR_PATTERN",WORD),]
class CPCO_METADATA_STRUCT(ctypes_wrap.StructWrap):
	_struct=PCO_METADATA_STRUCT
	_tup_exc={"wSize"}
	_tup={"bIMAGE_COUNTER_BCD":conv_arr,"bIMAGE_TIME_US_BCD":conv_arr}
	def prep(self, struct):
		struct.wSize=ctypes.sizeof(struct)
		return struct




##### Library #####

class PCOSC2Lib(object):
	def __init__(self):
		object.__init__(self)
		self._initialized=False

	def initlib(self):
		if self._initialized:
			return
		error_message="The library is supplied with pco.sdk software"
		self.lib=load_lib("SC2_Cam.dll",locations=("global","local"),error_message=error_message,call_conv="stdcall")
		lib=self.lib

		wrapper=ctypes_wrap.CTypesWrapper(restype=DWORD,errcheck=errcheck(lib=self))
		noret_wrapper=ctypes_wrap.CTypesWrapper()
		max_strlen=512
		strprep=ctypes_wrap.strprep(max_strlen)

		self.PCO_GetErrorText=noret_wrapper(lib.PCO_GetErrorText, [DWORD,ctypes.c_char_p,DWORD], ["code",None,None], 
			rvnames=["text",None], rvprep=[strprep,lambda *args: DWORD(max_strlen)], rvref=[False,False])

		self.PCO_OpenCamera=wrapper(lib.PCO_OpenCamera, [HANDLE,WORD], [None,"index"])
		self.PCO_CloseCamera=wrapper(lib.PCO_CloseCamera, [HANDLE], ["handle"])
		self.PCO_ResetSettingsToDefault=wrapper(lib.PCO_ResetSettingsToDefault, [HANDLE], ["handle"])
		self.PCO_RebootCamera=wrapper(lib.PCO_RebootCamera, [HANDLE], ["handle"])
		self.PCO_ResetLib=wrapper(lib.PCO_ResetLib)
		self.PCO_CheckDeviceAvailability=wrapper(lib.PCO_CheckDeviceAvailability, [HANDLE,WORD], ["handle","interfaces"])

		self.PCO_GetCameraDescription=wrapper(lib.PCO_GetCameraDescription, [HANDLE,PCO_Description], ["handle",None],
			rvprep=[CPCO_Description.prep_struct], rvconv=[CPCO_Description.tup_struct])
		self.PCO_GetGeneral=wrapper(lib.PCO_GetGeneral, [HANDLE,PCO_General], ["handle",None],
			rvprep=[CPCO_General.prep_struct], rvconv=[CPCO_General.tup_struct])
		self.PCO_GetCameraType=wrapper(lib.PCO_GetCameraType, [HANDLE,PCO_CameraType], ["handle",None],
			rvprep=[CPCO_CameraType.prep_struct], rvconv=[CPCO_CameraType.tup_struct])
		self.PCO_GetCameraHealthStatus=wrapper(lib.PCO_GetCameraHealthStatus, [HANDLE,DWORD,DWORD,DWORD], ["handle",None,None,None], rvnames=["warn","err","status"])
		self.PCO_GetTemperature=wrapper(lib.PCO_GetTemperature, [HANDLE,SHORT,SHORT,SHORT], ["handle",None,None,None], rvnames=["ccd","cam","pow"])
		self.PCO_GetInfoString=noret_wrapper(lib.PCO_GetInfoString, [HANDLE,DWORD,ctypes.c_char_p,WORD], ["handle","info_type",None,None], 
			rvnames=["text",None], rvprep=[strprep,lambda *_: WORD(max_strlen)], rvref=[False,False])

		self.PCO_ArmCamera=wrapper(lib.PCO_ArmCamera, [HANDLE], ["handle"])
		self.PCO_SetImageParameters=wrapper(lib.PCO_SetImageParameters, [HANDLE,WORD,WORD,DWORD,ctypes.c_void_p,ctypes.c_int], ["handle","xres","yres","flags",None,None],
			rvnames=[None,"res"], rvref=[False,False])
		self.PCO_SetTimeouts=wrapper(lib.PCO_SetTimeouts, [HANDLE,ctypes.c_void_p,ctypes.c_int], ["handle",None,None], addargs=["comm","img","trans"],
			rvnames=[None,None], rvprep=[lambda *args: (ctypes.c_uint*3)(args[1:]), lambda *_: 3*ctypes.sizeof(ctypes.c_uint)], rvref=[False,False])
		self.PCO_GetCameraSetup=wrapper(lib.PCO_GetCameraSetup, [HANDLE,WORD,ctypes.POINTER(DWORD),WORD], ["handle",None,None,None],
			rvnames=["setup_type","setup","setup_len"], rvprep=[None, lambda *_: (DWORD*4)(), lambda *_: WORD(4)], rvref=[True,False,True], rvconv=[None, conv_arr, None])
		self.PCO_SetCameraSetup_lib=wrapper(lib.PCO_SetCameraSetup, [HANDLE,WORD,ctypes.POINTER(DWORD),WORD], ["handle","setup_type","setup","setup_len"])
		self.PCO_GetSensorStruct=wrapper(lib.PCO_GetSensorStruct, [HANDLE,PCO_Sensor], ["handle",None],
			rvprep=[CPCO_Sensor.prep_struct], rvconv=[CPCO_Sensor.tup_struct])
		self.PCO_SetSensorStruct=wrapper(lib.PCO_SetSensorStruct, [HANDLE,PCO_Sensor], ["handle",None], addargs=["sensor"],
			rvprep=[lambda *args: ctypes.byref(args[1])], rvconv=[CPCO_Sensor.tup_struct])

		self.PCO_GetSizes=wrapper(lib.PCO_GetSizes, [HANDLE,WORD,WORD,WORD,WORD], ["handle",None,None,None,None], rvnames=["xres","yres","xres_max","yres_max"])
		self.PCO_GetSensorFormat=wrapper(lib.PCO_GetSensorFormat, [HANDLE,WORD], ["handle",None])
		self.PCO_SetSensorFormat=wrapper(lib.PCO_SetSensorFormat, [HANDLE,WORD], ["handle","format"])
		self.PCO_GetROI=wrapper(lib.PCO_GetROI, [HANDLE,WORD,WORD,WORD,WORD], ["handle",None,None,None,None], rvnames=["x0","y0","x1","y1"])
		self.PCO_SetROI=wrapper(lib.PCO_SetROI, [HANDLE,WORD,WORD,WORD,WORD], ["handle","x0","y0","x1","y1"])
		self.PCO_GetBinning=wrapper(lib.PCO_GetBinning, [HANDLE,WORD,WORD], ["handle",None,None], rvnames=["hbin","vbin"])
		self.PCO_SetBinning=wrapper(lib.PCO_SetBinning, [HANDLE,WORD,WORD], ["handle","hbin","vbin"])
		self.PCO_GetPixelRate=wrapper(lib.PCO_GetPixelRate, [HANDLE,DWORD], ["handle",None])
		self.PCO_SetPixelRate=wrapper(lib.PCO_SetPixelRate, [HANDLE,DWORD], ["handle","rate"])
		self.PCO_GetConversionFactor=wrapper(lib.PCO_GetConversionFactor, [HANDLE,WORD], ["handle",None])
		self.PCO_SetConversionFactor=wrapper(lib.PCO_SetConversionFactor, [HANDLE,WORD], ["handle","factor"])
		self.PCO_GetDoubleImageMode=wrapper(lib.PCO_GetDoubleImageMode, [HANDLE,WORD], ["handle",None])
		self.PCO_SetDoubleImageMode=wrapper(lib.PCO_SetDoubleImageMode, [HANDLE,WORD], ["handle","mode"])
		self.PCO_GetADCOperation=wrapper(lib.PCO_GetADCOperation, [HANDLE,WORD], ["handle",None])
		self.PCO_SetADCOperation=wrapper(lib.PCO_SetADCOperation, [HANDLE,WORD], ["handle","op"])
		self.PCO_GetIRSensitivity=wrapper(lib.PCO_GetIRSensitivity, [HANDLE,WORD], ["handle",None])
		self.PCO_SetIRSensitivity=wrapper(lib.PCO_SetIRSensitivity, [HANDLE,WORD], ["handle","ir"])
		self.PCO_GetCoolingSetpoints=wrapper(lib.PCO_GetCoolingSetpoints, [HANDLE,WORD,WORD,ctypes.POINTER(SHORT)], ["handle","block_id",None,None], addargs=["num"],
			rvnames=["num","points"], rvprep=[lambda *args: WORD(args[2]), lambda *args: (SHORT*args[2])()], rvconv=[None,conv_arr], rvref=[True,False])
		self.PCO_GetCoolingSetpointTemperature=wrapper(lib.PCO_GetCoolingSetpointTemperature, [HANDLE,SHORT], ["handle",None])
		self.PCO_SetCoolingSetpointTemperature=wrapper(lib.PCO_SetCoolingSetpointTemperature, [HANDLE,SHORT], ["handle","setpoint"])
		self.PCO_GetOffsetMode=wrapper(lib.PCO_GetOffsetMode, [HANDLE,WORD], ["handle",None])
		self.PCO_SetOffsetMode=wrapper(lib.PCO_SetOffsetMode, [HANDLE,WORD], ["handle","mode"])
		self.PCO_GetNoiseFilterMode=wrapper(lib.PCO_GetNoiseFilterMode, [HANDLE,WORD], ["handle",None])
		self.PCO_SetNoiseFilterMode=wrapper(lib.PCO_SetNoiseFilterMode, [HANDLE,WORD], ["handle","mode"])
		
		self.PCO_GetTimingStruct=wrapper(lib.PCO_GetTimingStruct, [HANDLE,PCO_Timing], ["handle",None],
			rvprep=[CPCO_Timing.prep_struct], rvconv=[CPCO_Timing.tup_struct])
		self.PCO_SetTimingStruct=wrapper(lib.PCO_SetTimingStruct, [HANDLE,PCO_Timing], ["handle",None], addargs=["timing"],
			rvprep=[lambda *args: ctypes.byref(args[1])], rvconv=[CPCO_Timing.tup_struct])
		self.PCO_GetCOCRuntime=wrapper(lib.PCO_GetCOCRuntime, [HANDLE,DWORD,DWORD], ["handle",None,None], rvnames=["time_sec","time_ns"])
		self.PCO_GetDelayExposureTime=wrapper(lib.PCO_GetDelayExposureTime, [HANDLE,DWORD,DWORD,WORD,WORD], ["handle",None,None,None,None],
			rvnames=["delay","exposure","delay_timebase","exposure_timebase"])
		self.PCO_SetDelayExposureTime=wrapper(lib.PCO_SetDelayExposureTime, [HANDLE,DWORD,DWORD,WORD,WORD], ["handle","delay","exposure","delay_timebase","exposure_timebase"])
		self.PCO_GetDelayExposureTimeTable=wrapper(lib.PCO_GetDelayExposureTimeTable, [HANDLE,ctypes.POINTER(DWORD),ctypes.POINTER(DWORD),WORD,WORD,WORD],
			["handle",None,None,None,None,"num"], rvnames=["delay","exposure","delay_timebase","exposure_timebase"],
			rvprep=[lambda *args: (DWORD*args[-1])(),lambda *args: (DWORD*args[-1])(),None,None], rvconv=[conv_arr,conv_arr], rvref=[False,False,True,True])
		self.PCO_SetDelayExposureTimeTable=wrapper(lib.PCO_SetDelayExposureTimeTable, [HANDLE,ctypes.POINTER(DWORD),ctypes.POINTER(DWORD),WORD,WORD,WORD],
			["handle",None,None,"delay_timebase","exposure_timebase","num"], addargs=["exposure","delay"], rvnames=[None,None],
			rvprep=[lambda *args: build_arr(DWORD)(args[4]), lambda *args: build_arr(DWORD)(args[5])], rvref=[False,False])
		self.PCO_GetFrameRate=wrapper(lib.PCO_GetFrameRate, [HANDLE,WORD,DWORD,DWORD], ["handle",None,None,None], rvnames=["status","rate","exposure"])
		self.PCO_SetFrameRate=wrapper(lib.PCO_SetFrameRate, [HANDLE,WORD,WORD,DWORD,DWORD], ["handle",None,"mode",None,None], addargs=["rate","exposure"],
			rvnames=["status","rate","exposure"], rvprep=[None,lambda *args:DWORD(args[2]),lambda *args:DWORD(args[3])])
		self.PCO_GetFPSExposureMode=wrapper(lib.PCO_GetFPSExposureMode, [HANDLE,WORD,DWORD], ["handle",None,None], rvnames=["mode","exposure"])
		self.PCO_SetFPSExposureMode=wrapper(lib.PCO_SetFPSExposureMode, [HANDLE,WORD,DWORD], ["handle","mode",None])
		self.PCO_GetTriggerMode=wrapper(lib.PCO_GetTriggerMode, [HANDLE,WORD], ["handle",None])
		self.PCO_SetTriggerMode=wrapper(lib.PCO_SetTriggerMode, [HANDLE,WORD], ["handle","mode"])
		self.PCO_ForceTrigger=wrapper(lib.PCO_ForceTrigger, [HANDLE,WORD], ["handle",None])
		self.PCO_GetCameraBusyStatus=wrapper(lib.PCO_GetCameraBusyStatus, [HANDLE,WORD], ["handle",None])
		self.PCO_GetPowerDownMode=wrapper(lib.PCO_GetPowerDownMode, [HANDLE,WORD], ["handle",None])
		self.PCO_SetPowerDownMode=wrapper(lib.PCO_SetPowerDownMode, [HANDLE,WORD], ["handle","mode"])
		self.PCO_GetUserPowerDownTime=wrapper(lib.PCO_GetUserPowerDownTime, [HANDLE,DWORD], ["handle",None])
		self.PCO_SetUserPowerDownTime=wrapper(lib.PCO_SetUserPowerDownTime, [HANDLE,DWORD], ["handle","mode"])
		self.PCO_GetModulationMode=wrapper(lib.PCO_GetModulationMode, [HANDLE,WORD,DWORD,WORD,DWORD,LONG], ["handle",None,None,None,None,None],
			rvnames=["mode","period","period_timebase","num_exp","mon_offset"])
		self.PCO_SetModulationMode=wrapper(lib.PCO_SetModulationMode, [HANDLE,WORD,DWORD,WORD,DWORD,LONG], ["handle","mode","period","period_timebase","num_exp","mon_offset"])
		self.PCO_GetHWIOSignalCount=wrapper(lib.PCO_GetHWIOSignalCount, [HANDLE,WORD], ["handle",None])
		self.PCO_GetHWIOSignalDescriptor=wrapper(lib.PCO_GetHWIOSignalDescriptor, [HANDLE,WORD,PCO_Single_Signal_Desc], ["handle","num",None],
			rvprep=[CPCO_Single_Signal_Desc.prep_struct], rvconv=[CPCO_Single_Signal_Desc.tup_struct])
		self.PCO_GetHWIOSignal=wrapper(lib.PCO_GetHWIOSignal, [HANDLE,WORD,PCO_Signal], ["handle","num",None],
			rvprep=[CPCO_Signal.prep_struct], rvconv=[CPCO_Signal.tup_struct])
		self.PCO_SetHWIOSignal=wrapper(lib.PCO_SetHWIOSignal, [HANDLE,WORD,PCO_Signal], ["handle","num",None], addargs=["signal"],
			rvprep=[lambda *args: ctypes.byref(args[2])], rvconv=[CPCO_Signal.tup_struct])
		self.PCO_GetImageTiming=wrapper(lib.PCO_GetImageTiming, [HANDLE,PCO_ImageTiming], ["handle",None],
			rvprep=[CPCO_ImageTiming.prep_struct], rvconv=[CPCO_ImageTiming.tup_struct])
		self.PCO_GetCameraSynchMode=wrapper(lib.PCO_GetCameraSynchMode, [HANDLE,WORD], ["handle",None])
		self.PCO_SetCameraSynchMode=wrapper(lib.PCO_SetCameraSynchMode, [HANDLE,WORD], ["handle","mode"])
		self.PCO_GetFastTimingMode=wrapper(lib.PCO_GetFastTimingMode, [HANDLE,WORD], ["handle",None])
		self.PCO_SetFastTimingMode=wrapper(lib.PCO_SetFastTimingMode, [HANDLE,WORD], ["handle","mode"])
		self.PCO_GetExpTrigSignalStatus=wrapper(lib.PCO_GetExpTrigSignalStatus, [HANDLE,WORD], ["handle",None])

		self.PCO_GetRecordingStruct=wrapper(lib.PCO_GetRecordingStruct, [HANDLE,PCO_Recording], ["handle",None],
			rvprep=[CPCO_Recording.prep_struct], rvconv=[CPCO_Recording.tup_struct])
		self.PCO_SetRecordingStruct=wrapper(lib.PCO_SetRecordingStruct, [HANDLE,PCO_Recording], ["handle",None], addargs=["recording"],
			rvprep=[lambda *args: args[1]], rvconv=[CPCO_Recording.tup_struct])
		self.PCO_GetRecordingState=wrapper(lib.PCO_GetRecordingState, [HANDLE,WORD], ["handle",None])
		self.PCO_SetRecordingState=wrapper(lib.PCO_SetRecordingState, [HANDLE,WORD], ["handle","state"])
		self.PCO_GetStorageMode=wrapper(lib.PCO_GetStorageMode, [HANDLE,WORD], ["handle",None])
		self.PCO_SetStorageMode=wrapper(lib.PCO_SetStorageMode, [HANDLE,WORD], ["handle","mode"])
		self.PCO_GetRecorderSubmode=wrapper(lib.PCO_GetRecorderSubmode, [HANDLE,WORD], ["handle",None])
		self.PCO_SetRecorderSubmode=wrapper(lib.PCO_SetRecorderSubmode, [HANDLE,WORD], ["handle","mode"])
		self.PCO_GetAcquireMode=wrapper(lib.PCO_GetAcquireMode, [HANDLE,WORD], ["handle",None])
		self.PCO_SetAcquireMode=wrapper(lib.PCO_SetAcquireMode, [HANDLE,WORD], ["handle","mode"])
		self.PCO_GetAcquireModeEx=wrapper(lib.PCO_GetAcquireModeEx, [HANDLE,WORD,DWORD,DWORD], ["handle",None,None,None], rvnames=["mode","img_num",None])
		self.PCO_SetAcquireModeEx=wrapper(lib.PCO_SetAcquireModeEx, [HANDLE,WORD,DWORD,DWORD], ["handle","mode","img_num",None], rvnames=[None])
		self.PCO_GetAcqEnblSignalStatus=wrapper(lib.PCO_GetAcqEnblSignalStatus, [HANDLE,WORD], ["handle",None])
		self.PCO_GetMetaDataMode=wrapper(lib.PCO_GetMetaDataMode, [HANDLE,WORD,WORD,WORD], ["handle",None,None,None], rvnames=["mode","size","ver"])
		self.PCO_SetMetaDataMode=wrapper(lib.PCO_SetMetaDataMode, [HANDLE,WORD,WORD,WORD], ["handle","mode",None,None], rvnames=["size","ver"])
		self.PCO_GetRecordStopEvent=wrapper(lib.PCO_GetRecordStopEvent, [HANDLE,WORD,DWORD], ["handle",None,None], rvnames=["mode","img_num"])
		self.PCO_SetRecordStopEvent=wrapper(lib.PCO_SetRecordStopEvent, [HANDLE,WORD,DWORD], ["handle","mode","img_num"])
		self.PCO_StopRecord=wrapper(lib.PCO_StopRecord, [HANDLE,WORD,DWORD], ["handle",None,None], rvnames=[None,None])
		self.PCO_SetDateTime=wrapper(lib.PCO_SetDateTime, [HANDLE,BYTE,BYTE,WORD,WORD,BYTE,BYTE], ["handle","day","month","year","hour","minute","second"])
		self.PCO_GetTimestampMode=wrapper(lib.PCO_GetTimestampMode, [HANDLE,WORD], ["handle",None])
		self.PCO_SetTimestampMode=wrapper(lib.PCO_SetTimestampMode, [HANDLE,WORD], ["handle","mode"])

		self.PCO_GetStorageStruct=wrapper(lib.PCO_GetStorageStruct, [HANDLE,PCO_Storage], ["handle",None],
			rvprep=[CPCO_Storage.prep_struct], rvconv=[CPCO_Storage.tup_struct])
		self.PCO_SetStorageStruct=wrapper(lib.PCO_SetStorageStruct, [HANDLE,PCO_Storage], ["handle",None], addargs=["storage"],
			rvprep=[lambda *args: ctypes.byref(args[1])], rvconv=[CPCO_Storage.tup_struct])
		self.PCO_GetCameraRamSize=wrapper(lib.PCO_GetCameraRamSize, [HANDLE,DWORD,DWORD], ["handle",None,None], rvnames=["ram_size","page_size"])
		self.PCO_GetCameraRamSegmentSize=wrapper(lib.PCO_GetCameraRamSegmentSize, [HANDLE,ctypes.POINTER(DWORD)], ["handle",None],
			rvprep=[lambda *args: (DWORD*4)()], rvconv=[conv_arr], rvref=[False])
		self.PCO_SetCameraRamSegmentSize=wrapper(lib.PCO_SetCameraRamSegmentSize, [HANDLE,ctypes.POINTER(DWORD)], ["handle",None], addargs=["seg_sizes"],
			rvprep=[lambda *args: build_arr(DWORD,4)(args[1])], rvnames=[None], rvref=[False])
		self.PCO_ClearRamSegment=wrapper(lib.PCO_ClearRamSegment, [HANDLE], ["handle"])
		self.PCO_GetActiveRamSegment=wrapper(lib.PCO_GetActiveRamSegment, [HANDLE,WORD], ["handle",None])
		self.PCO_SetActiveRamSegment=wrapper(lib.PCO_SetActiveRamSegment, [HANDLE,WORD], ["handle","segment"])
		self.PCO_SetTransferParametersAuto=wrapper(lib.PCO_SetTransferParametersAuto, [HANDLE,ctypes.c_void_p,ctypes.c_int], ["handle",None,None],
			rvprep=[None,0], rvref=[False,False])
		self.PCO_SetActiveLookupTable=wrapper(lib.PCO_SetActiveLookupTable, [HANDLE,DWORD,DWORD], ["handle",None,None],
			rvprep=[lambda *args:args[1], lambda *args:args[2]], addargs=["lut","offset"])

		self.PCO_GetImageStruct=wrapper(lib.PCO_GetImageStruct, [HANDLE,PCO_Image], ["handle",None],
			rvprep=[CPCO_Image.prep_struct], rvconv=[CPCO_Image.tup_struct])
		self.PCO_GetSegmentStruct=wrapper(lib.PCO_GetSegmentStruct, [HANDLE,WORD,PCO_Segment], ["handle","num",None],
			rvprep=[CPCO_Segment.prep_struct], rvconv=[CPCO_Segment.tup_struct])
		self.PCO_GetSegmentImageSettings=wrapper(lib.PCO_GetSegmentImageSettings, [HANDLE,WORD,WORD,WORD,WORD,WORD,WORD,WORD,WORD,WORD], ["handle","num",None,None,None,None,None,None,None,None],
			rvnames=["xres","yres","hbin","vbin","x0","y0","x1","y1"])
		self.PCO_GetNumberOfImagesInSegment=wrapper(lib.PCO_GetNumberOfImagesInSegment, [HANDLE,WORD,DWORD,DWORD], ["handle","num",None,None],
			rvnames=["valid_cnt","max_cnt"])
		self.PCO_GetBitAlignment=wrapper(lib.PCO_GetBitAlignment, [HANDLE,WORD], ["handle",None])
		self.PCO_SetBitAlignment=wrapper(lib.PCO_SetBitAlignment, [HANDLE,WORD], ["handle","alignment"])
		self.PCO_GetHotPixelCorrectionMode=wrapper(lib.PCO_GetHotPixelCorrectionMode, [HANDLE,WORD], ["handle",None])
		self.PCO_SetHotPixelCorrectionMode=wrapper(lib.PCO_SetHotPixelCorrectionMode, [HANDLE,WORD], ["handle","mode"])
		
		self.PCO_AllocateBuffer=wrapper(lib.PCO_AllocateBuffer, [HANDLE,SHORT,DWORD,ctypes.POINTER(WORD),HANDLE], ["handle",None,"size",None,None], addargs=["num","buff","event"],
			rvnames=["num","buff","event"], rvprep=[lambda *args: SHORT(args[2]), lambda *args: ctypes.cast(ctypes.c_voidp(args[3]),ctypes.POINTER(WORD)), lambda *args: HANDLE(args[4]) ])
		self.PCO_FreeBuffer=wrapper(lib.PCO_FreeBuffer, [HANDLE,SHORT], ["handle","num"])
		self.PCO_GetBufferStatus=wrapper(lib.PCO_GetBufferStatus, [HANDLE,SHORT,DWORD,DWORD], ["handle","num",None,None], rvnames=["status_dll","status_driver"])
		self.PCO_GetBuffer=wrapper(lib.PCO_GetBuffer, [HANDLE,SHORT,ctypes.POINTER(WORD),HANDLE], ["handle","num",None,None], rvnames=["buff","event"])

		self.PCO_GetImageEx=wrapper(lib.PCO_GetImageEx, [HANDLE,WORD,DWORD,DWORD,SHORT,WORD,WORD,WORD], ["handle","segment","first_idx","last_idx","num","xres","yres","bpp"])
		self.PCO_AddBufferEx=wrapper(lib.PCO_AddBufferEx, [HANDLE,DWORD,DWORD,SHORT,WORD,WORD,WORD], ["handle","first_idx","last_idx","num","xres","yres","bpp"])
		self.PCO_AddBufferExtern=wrapper(lib.PCO_AddBufferExtern, [HANDLE,HANDLE,WORD,DWORD,DWORD,DWORD,ctypes.c_void_p,DWORD,ctypes.POINTER(DWORD)],
			["handle","event","segment","first_idx","last_idx","sync","buff","len","pstatus"])
		self.PCO_CancelImages=wrapper(lib.PCO_CancelImages, [HANDLE], ["handle"])
		self.PCO_RemoveBuffer=wrapper(lib.PCO_RemoveBuffer, [HANDLE], ["handle"])
		self.PCO_GetPendingBuffer=wrapper(lib.PCO_GetPendingBuffer, [HANDLE,ctypes.c_int], ["handle",None])
		self.PCO_WaitforBuffer_lib=wrapper(lib.PCO_WaitforBuffer, [HANDLE,ctypes.c_int,ctypes.POINTER(PCO_Buflist),ctypes.c_int], ["handle","num","buff_ptr","timeout"])
		self.PCO_EnableSoftROI=wrapper(lib.PCO_EnableSoftROI, [HANDLE,WORD,ctypes.c_void_p,ctypes.c_int], ["handle","flags",None,None], rvnames=[None,"res"], rvref=[False,False])
		self.PCO_GetMetaData=wrapper(lib.PCO_GetMetaData, [HANDLE,SHORT,PCO_METADATA_STRUCT,DWORD,DWORD], ["handle","num",None,None,None], rvnames=["struct",None,None],
			rvprep=[CPCO_METADATA_STRUCT.prep_struct,None,None], rvconv=[CPCO_METADATA_STRUCT.tup_struct,None,None], rvref=[True,False,False])

		kernel32=ctypes.windll.kernel32
		self.CreateEventA=noret_wrapper.wrap(kernel32.CreateEventA, [ctypes.c_void_p,BOOL,BOOL,ctypes.c_char_p], ["attr","man_reset","init_state","name"], restype=HANDLE)
		self.CloseHandle=noret_wrapper.wrap(kernel32.CloseHandle, [HANDLE], ["handle"], restype=BOOL)
		self.ResetEvent=noret_wrapper.wrap(kernel32.ResetEvent, [HANDLE], ["handle"], restype=BOOL)
		self.SetEvent=noret_wrapper.wrap(kernel32.SetEvent, [HANDLE], ["handle"], restype=BOOL)
		self.WaitForSingleObject=noret_wrapper.wrap(kernel32.WaitForSingleObject, [HANDLE, DWORD], ["handle","timeout"], restype=DWORD)
		self.WaitForMultipleObjects=noret_wrapper.wrap(kernel32.WaitForMultipleObjects, [DWORD, ctypes.POINTER(HANDLE), BOOL, DWORD], ["count","handles","wait_all","timeout"], restype=DWORD)

		self.PCO_GetSensorSignalStatus=wrapper(lib.PCO_GetSensorSignalStatus, [HANDLE,DWORD,DWORD,DWORD,DWORD], ["handle",None,None,None,None], rvnames=["status","img_cnt",None,None])
		
		self._initialized=True
	
	def PCO_SetCameraSetup(self, handle, setup_type, setup):
		setup=(setup+[0,0,0,0])[:4]
		dwsetup=(DWORD*4)()
		dwsetup[:4]=setup
		return self.PCO_SetCameraSetup_lib(handle,setup_type,dwsetup,4)

	def PCO_WaitforBuffer(self, handle, nums, timeout):
		buffs=(PCO_Buflist*len(nums))()
		for i,n in enumerate(nums):
			buffs[i].sBufNr=n
		self.PCO_WaitforBuffer_lib(handle,len(nums),buffs,timeout)
		return [CPCO_Buflist.tup_struct(b) for b in buffs]

	def CreateEvent(self, man_reset=True, init_state=False):
		return self.CreateEventA(None,man_reset,init_state,b"\x00")

lib=PCOSC2Lib()



def named_tuple_to_dict(val, norm_strings=True, expand_lists=False):
	if isinstance(val,py3.bytestring) and norm_strings:
		return py3.as_str(val)
	elif isinstance(val,list) and expand_lists:
		val=[named_tuple_to_dict(el,norm_strings=norm_strings,expand_lists=expand_lists) for el in val]
		return dict(enumerate(val))
	elif hasattr(val,"_asdict"):
		val=val._asdict()
		for k in val:
			val[k]=named_tuple_to_dict(val[k],norm_strings=norm_strings,expand_lists=expand_lists)
		return val
	else:
		return val