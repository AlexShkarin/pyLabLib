from ...core.utils import ctypes_wrap
from .misc import default_placing_message, load_lib

import ctypes
import collections
import os.path
import platform

##### Constants #####

Andor_statuscodes = {
		20001: "DRV_ERROR_CODES",
		20002: "DRV_SUCCESS",
		20003: "DRV_VXDNOTINSTALLED",
		20004: "DRV_ERROR_SCAN",
		20005: "DRV_ERROR_CHECK_SUM",
		20006: "DRV_ERROR_FILELOAD",
		20007: "DRV_UNKNOWN_FUNCTION",
		20008: "DRV_ERROR_VXD_INIT",
		20009: "DRV_ERROR_ADDRESS",
		20010: "DRV_ERROR_PAGELOCK",
		20011: "DRV_ERROR_PAGEUNLOCK",
		20012: "DRV_ERROR_BOARDTEST",
		20013: "DRV_ERROR_ACK",
		20014: "DRV_ERROR_UP_FIFO",
		20015: "DRV_ERROR_PATTERN",
		20017: "DRV_ACQUISITION_ERRORS",
		20018: "DRV_ACQ_BUFFER",
		20019: "DRV_ACQ_DOWNFIFO_FULL",
		20020: "DRV_PROC_UNKONWN_INSTRUCTION",
		20021: "DRV_ILLEGAL_OP_CODE",
		20022: "DRV_KINETIC_TIME_NOT_MET",
		20023: "DRV_ACCUM_TIME_NOT_MET",
		20024: "DRV_NO_NEW_DATA",
		20025: "DRV_PCI_DMA_FAIL",
		20026: "DRV_SPOOLERROR",
		20027: "DRV_SPOOLSETUPERROR",
		20028: "DRV_FILESIZELIMITERROR",
		20029: "DRV_ERROR_FILESAVE",
		20033: "DRV_TEMPERATURE_CODES",
		20034: "DRV_TEMPERATURE_OFF",
		20035: "DRV_TEMPERATURE_NOT_STABILIZED",
		20036: "DRV_TEMPERATURE_STABILIZED",
		20037: "DRV_TEMPERATURE_NOT_REACHED",
		20038: "DRV_TEMPERATURE_OUT_RANGE",
		20039: "DRV_TEMPERATURE_NOT_SUPPORTED",
		20040: "DRV_TEMPERATURE_DRIFT",
		20049: "DRV_GENERAL_ERRORS",
		20050: "DRV_INVALID_AUX",
		20051: "DRV_COF_NOTLOADED",
		20052: "DRV_FPGAPROG",
		20053: "DRV_FLEXERROR",
		20054: "DRV_GPIBERROR",
		20055: "DRV_EEPROMVERSIONERROR",
		20064: "DRV_DATATYPE",
		20065: "DRV_DRIVER_ERRORS",
		20066: "DRV_P1INVALID",
		20067: "DRV_P2INVALID",
		20068: "DRV_P3INVALID",
		20069: "DRV_P4INVALID",
		20070: "DRV_INIERROR",
		20071: "DRV_COFERROR",
		20072: "DRV_ACQUIRING",
		20073: "DRV_IDLE",
		20074: "DRV_TEMPCYCLE",
		20075: "DRV_NOT_INITIALIZED",
		20076: "DRV_P5INVALID",
		20077: "DRV_P6INVALID",
		20078: "DRV_INVALID_MODE",
		20079: "DRV_INVALID_FILTER",
		20080: "DRV_I2CERRORS",
		20081: "DRV_I2CDEVNOTFOUND",
		20082: "DRV_I2CTIMEOUT",
		20083: "DRV_P7INVALID",
		20084: "DRV_P8INVALID",
		20085: "DRV_P9INVALID",
		20086: "DRV_P10INVALID",
		20087: "DRV_P11INVALID",
		20089: "DRV_USBERROR",
		20090: "DRV_IOCERROR",
		20091: "DRV_VRMVERSIONERROR",
		20092: "DRV_GATESTEPERROR",
		20093: "DRV_USB_INTERRUPT_ENDPOINT_ERROR",
		20094: "DRV_RANDOM_TRACK_ERROR",
		20095: "DRV_INVALID_TRIGGER_MODE",
		20096: "DRV_LOAD_FIRMWARE_ERROR",
		20097: "DRV_DIVIDE_BY_ZERO_ERROR",
		20098: "DRV_INVALID_RINGEXPOSURES",
		20099: "DRV_BINNING_ERROR",
		20100: "DRV_INVALID_AMPLIFIER",
		20101: "DRV_INVALID_COUNTCONVERT_MODE",
		20990: "DRV_ERROR_NOCAMERA",
		20991: "DRV_NOT_SUPPORTED",
		20992: "DRV_NOT_AVAILABLE",
		20115: "DRV_ERROR_MAP",
		20116: "DRV_ERROR_UNMAP",
		20117: "DRV_ERROR_MDL",
		20118: "DRV_ERROR_UNMDL",
		20119: "DRV_ERROR_BUFFSIZE",
		20121: "DRV_ERROR_NOHANDLE",
		20130: "DRV_GATING_NOT_AVAILABLE",
		20131: "DRV_FPGA_VOLTAGE_ERROR",
		20150: "DRV_OW_CMD_FAIL",
		20151: "DRV_OWMEMORY_BAD_ADDR",
		20152: "DRV_OWCMD_NOT_AVAILABLE",
		20153: "DRV_OW_NO_SLAVES",
		20154: "DRV_OW_NOT_INITIALIZED",
		20155: "DRV_OW_ERROR_SLAVE_NUM",
		20156: "DRV_MSTIMINGS_ERROR",
		20173: "DRV_OA_NULL_ERROR",
		20174: "DRV_OA_PARSE_DTD_ERROR",
		20175: "DRV_OA_DTD_VALIDATE_ERROR",
		20176: "DRV_OA_FILE_ACCESS_ERROR",
		20177: "DRV_OA_FILE_DOES_NOT_EXIST",
		20178: "DRV_OA_XML_INVALID_OR_NOT_FOUND_ERROR",
		20179: "DRV_OA_PRESET_FILE_NOT_LOADED",
		20180: "DRV_OA_USER_FILE_NOT_LOADED",
		20181: "DRV_OA_PRESET_AND_USER_FILE_NOT_LOADED",
		20182: "DRV_OA_INVALID_FILE",
		20183: "DRV_OA_FILE_HAS_BEEN_MODIFIED",
		20184: "DRV_OA_BUFFER_FULL",
		20185: "DRV_OA_INVALID_STRING_LENGTH",
		20186: "DRV_OA_INVALID_CHARS_IN_NAME",
		20187: "DRV_OA_INVALID_NAMING",
		20188: "DRV_OA_GET_CAMERA_ERROR",
		20189: "DRV_OA_MODE_ALREADY_EXISTS",
		20190: "DRV_OA_STRINGS_NOT_EQUAL",
		20191: "DRV_OA_NO_USER_DATA",
		20192: "DRV_OA_VALUE_NOT_SUPPORTED",
		20193: "DRV_OA_MODE_DOES_NOT_EXIST",
		20194: "DRV_OA_CAMERA_NOT_SUPPORTED",
		20195: "DRV_OA_FAILED_TO_GET_MODE",
		20211: "DRV_PROCESSING_FAILED",
}
def text_status(status):
    if status in Andor_statuscodes:
        return Andor_statuscodes[status]
    raise AndorLibError("unrecognized status code: {}".format(status),-1)

Andor_AcqMode = {
        1: "AC_ACQMODE_SINGLE",
		2: "AC_ACQMODE_VIDEO",
		4: "AC_ACQMODE_ACCUMULATE",
		8: "AC_ACQMODE_KINETIC",
		16: "AC_ACQMODE_FRAMETRANSFER",
		32: "AC_ACQMODE_FASTKINETICS",
		64: "AC_ACQMODE_OVERLAP",
}

Andor_ReadMode = {
		1: "AC_READMODE_FULLIMAGE",
		2: "AC_READMODE_SUBIMAGE",
		4: "AC_READMODE_SINGLETRACK",
		8: "AC_READMODE_FVB",
		16: "AC_READMODE_MULTITRACK",
		32: "AC_READMODE_RANDOMTRACK",
		64: "AC_READMODE_MULTITRACKSCAN",
}

Andor_TriggerMode = {
		1: "AC_TRIGGERMODE_INTERNAL",
		2: "AC_TRIGGERMODE_EXTERNAL",
		4: "AC_TRIGGERMODE_EXTERNAL_FVB_EM",
		8: "AC_TRIGGERMODE_CONTINUOUS",
		16: "AC_TRIGGERMODE_EXTERNALSTART",
		32: "AC_TRIGGERMODE_EXTERNALEXPOSURE",
		0x40: "AC_TRIGGERMODE_INVERTED",
		0x80: "AC_TRIGGERMODE_EXTERNAL_CHARGESHIFTING",
}

Andor_CameraType = {
		0: "AC_CAMERATYPE_PDA",
		1: "AC_CAMERATYPE_IXON",
		2: "AC_CAMERATYPE_ICCD",
		3: "AC_CAMERATYPE_EMCCD",
		4: "AC_CAMERATYPE_CCD",
		5: "AC_CAMERATYPE_ISTAR",
		6: "AC_CAMERATYPE_VIDEO",
		7: "AC_CAMERATYPE_IDUS",
		8: "AC_CAMERATYPE_NEWTON",
		9: "AC_CAMERATYPE_SURCAM",
		10: "AC_CAMERATYPE_USBICCD",
		11: "AC_CAMERATYPE_LUCA",
		12: "AC_CAMERATYPE_RESERVED",
		13: "AC_CAMERATYPE_IKON",
		14: "AC_CAMERATYPE_INGAAS",
		15: "AC_CAMERATYPE_IVAC",
		16: "AC_CAMERATYPE_UNPROGRAMMED",
		17: "AC_CAMERATYPE_CLARA",
		18: "AC_CAMERATYPE_USBISTAR",
		19: "AC_CAMERATYPE_SIMCAM",
		20: "AC_CAMERATYPE_NEO",
		21: "AC_CAMERATYPE_IXONULTRA",
		22: "AC_CAMERATYPE_VOLMOS",
}

Andor_PixelMode = {
		1: "AC_PIXELMODE_8BIT",
		2: "AC_PIXELMODE_14BIT",
		4: "AC_PIXELMODE_16BIT",
		8: "AC_PIXELMODE_32BIT",
        
		0x000000: "AC_PIXELMODE_MONO",
		0x010000: "AC_PIXELMODE_RGB",
		0x020000: "AC_PIXELMODE_CMY",
}

Andor_SetFunction = {
		0x01: "AC_SETFUNCTION_VREADOUT",
		0x02: "AC_SETFUNCTION_HREADOUT",
		0x04: "AC_SETFUNCTION_TEMPERATURE",
		0x08: "AC_SETFUNCTION_MCPGAIN",
		0x10: "AC_SETFUNCTION_EMCCDGAIN",
		0x20: "AC_SETFUNCTION_BASELINECLAMP",
		0x40: "AC_SETFUNCTION_VSAMPLITUDE",
		0x80: "AC_SETFUNCTION_HIGHCAPACITY",
		0x0100: "AC_SETFUNCTION_BASELINEOFFSET",
		0x0200: "AC_SETFUNCTION_PREAMPGAIN",
		0x0400: "AC_SETFUNCTION_CROPMODE",
		0x0800: "AC_SETFUNCTION_DMAPARAMETERS",
		0x1000: "AC_SETFUNCTION_HORIZONTALBIN",
		0x2000: "AC_SETFUNCTION_MULTITRACKHRANGE",
		0x4000: "AC_SETFUNCTION_RANDOMTRACKNOGAPS",
		0x8000: "AC_SETFUNCTION_EMADVANCED",
		0x010000: "AC_SETFUNCTION_GATEMODE",
		0x020000: "AC_SETFUNCTION_DDGTIMES",
		0x040000: "AC_SETFUNCTION_IOC",
		0x080000: "AC_SETFUNCTION_INTELLIGATE",
		0x100000: "AC_SETFUNCTION_INSERTION_DELAY",
		0x200000: "AC_SETFUNCTION_GATESTEP",
		0x400000: "AC_SETFUNCTION_TRIGGERTERMINATION",
		0x800000: "AC_SETFUNCTION_EXTENDEDNIR",
		0x1000000: "AC_SETFUNCTION_SPOOLTHREADCOUNT",
		0x2000000: "AC_SETFUNCTION_REGISTERPACK",
}

Andor_GetFunction = {
		0x01: "AC_GETFUNCTION_TEMPERATURE",
		0x02: "AC_GETFUNCTION_TARGETTEMPERATURE",
		0x04: "AC_GETFUNCTION_TEMPERATURERANGE",
		0x08: "AC_GETFUNCTION_DETECTORSIZE",
		0x10: "AC_GETFUNCTION_MCPGAIN",
		0x20: "AC_GETFUNCTION_EMCCDGAIN",
		0x40: "AC_GETFUNCTION_HVFLAG",
		0x80: "AC_GETFUNCTION_GATEMODE",
		0x0100: "AC_GETFUNCTION_DDGTIMES",
		0x0200: "AC_GETFUNCTION_IOC",
		0x0400: "AC_GETFUNCTION_INTELLIGATE",
		0x0800: "AC_GETFUNCTION_INSERTION_DELAY",
		0x1000: "AC_GETFUNCTION_GATESTEP",
		0x2000: "AC_GETFUNCTION_PHOSPHORSTATUS",
		0x4000: "AC_GETFUNCTION_MCPGAINTABLE",
		0x8000: "AC_GETFUNCTION_BASELINECLAMP",
}

Andor_Features = {
		1: "AC_FEATURES_POLLING",
		2: "AC_FEATURES_EVENTS",
		4: "AC_FEATURES_SPOOLING",
		8: "AC_FEATURES_SHUTTER",
		16: "AC_FEATURES_SHUTTEREX",
		32: "AC_FEATURES_EXTERNAL_I2C",
		64: "AC_FEATURES_SATURATIONEVENT",
		128: "AC_FEATURES_FANCONTROL",
		256: "AC_FEATURES_MIDFANCONTROL",
		512: "AC_FEATURES_TEMPERATUREDURINGACQUISITION",
		1024: "AC_FEATURES_KEEPCLEANCONTROL",
		0x0800: "AC_FEATURES_DDGLITE",
		0x1000: "AC_FEATURES_FTEXTERNALEXPOSURE",
		0x2000: "AC_FEATURES_KINETICEXTERNALEXPOSURE",
		0x4000: "AC_FEATURES_DACCONTROL",
		0x8000: "AC_FEATURES_METADATA",
		0x10000: "AC_FEATURES_IOCONTROL",
		0x20000: "AC_FEATURES_PHOTONCOUNTING",
		0x40000: "AC_FEATURES_COUNTCONVERT",
		0x80000: "AC_FEATURES_DUALMODE",
		0x100000: "AC_FEATURES_OPTACQUIRE",
		0x200000: "AC_FEATURES_REALTIMESPURIOUSNOISEFILTER",
		0x400000: "AC_FEATURES_POSTPROCESSSPURIOUSNOISEFILTER",
		0x800000: "AC_FEATURES_DUALPREAMPGAIN",
		0x1000000: "AC_FEATURES_DEFECT_CORRECTION",
		0x2000000: "AC_FEATURES_STARTOFEXPOSURE_EVENT",
		0x4000000: "AC_FEATURES_ENDOFEXPOSURE_EVENT",
		0x8000000: "AC_FEATURES_CAMERALINK",
}

Andor_EMGain = {
		1: "AC_EMGAIN_8BIT",
		2: "AC_EMGAIN_12BIT",
		4: "AC_EMGAIN_LINEAR12",
		8: "AC_EMGAIN_REAL12",
}




class AndorLibError(RuntimeError):
	"""Generic Andor library error"""
	def __init__(self, func, code):
		self.func=func
		self.code=code
		self.text_code=Andor_statuscodes.get(code,"UNKNOWN")
		msg="function '{}' raised error {}({})".format(func,code,self.text_code)
		RuntimeError.__init__(self,msg)
def errcheck(passing=None):
	"""
	Build an error checking function.

	Return a function which checks return codes of Andor library functions.
	`passing` is a list specifying which return codes are acceptable (by default only 20002, which is success code, is acceptable).
	"""
	passing=set(passing) if passing is not None else set()
	passing.add(20002) # always allow success
	def checker(result, func, arguments):
		if result not in passing:
			raise AndorLibError(func.__name__,result)
		return Andor_statuscodes[result]
	return checker

def _int_to_enumlst(num, enums):
	lst=[]
	for k,v in enums.items():
		if num&k:
			lst.append(v)
	return lst

class AndorCapabilities(ctypes.Structure):
	_fields_=[  ("Size",ctypes.c_int32),
				("AcqModes",ctypes.c_int32),
				("ReadModes",ctypes.c_int32),
				("TriggerModes",ctypes.c_int32),
				("CameraType",ctypes.c_int32),
				("PixelMode",ctypes.c_int32),
				("SetFunctions",ctypes.c_int32),
				("GetFunctions",ctypes.c_int32),
				("Features",ctypes.c_int32),
				("PCICard",ctypes.c_int32),
				("EMGainCapability",ctypes.c_int32),
				("FTReadModes",ctypes.c_int32) ]
AndorCapabilities_p=ctypes.POINTER(AndorCapabilities)
class CAndorCapabilities(ctypes_wrap.StructWrap):
	_struct=AndorCapabilities
	_tup={
		"AcqModes": (lambda x: _int_to_enumlst(x,Andor_AcqMode)),
		"ReadModes": (lambda x: _int_to_enumlst(x,Andor_ReadMode)),
		"TriggerModes": (lambda x: _int_to_enumlst(x,Andor_TriggerMode)),
		"CameraType": (lambda x: Andor_CameraType.get(x&0x1F,"UNKNOWN")),
		"PixelMode": (lambda x: _int_to_enumlst(x&0xFFFF,Andor_PixelMode)+[Andor_PixelMode.get(x&0xFFFF0000,"UNKNOWN")]),
		"SetFunctions": (lambda x: _int_to_enumlst(x,Andor_SetFunction)),
		"GetFunctions": (lambda x: _int_to_enumlst(x,Andor_GetFunction)),
		"Features": (lambda x: _int_to_enumlst(x,Andor_Features)),
		"EMGainCapability": (lambda x: _int_to_enumlst(x,Andor_EMGain)),
		"FTReadModes": (lambda x: _int_to_enumlst(x,Andor_ReadMode))
	}
	def prep(self, struct):
		struct.Size=ctypes.sizeof(struct)
		return struct




class AndorLib(object):
	def __init__(self):
		object.__init__(self)
		self._initialized=False

	def initlib(self):
		if self._initialized:
			return
		arch=platform.architecture()[0]
		winarch="64bit" if platform.machine().endswith("64") else "32bit"
		if arch=="32bit" and winarch=="64bit":
			solis_path=r"C:\Program Files (x86)\Andor SOLIS"
		else:
			solis_path=r"C:\Program Files\Andor SOLIS"
		error_message="The library is supplied with Andor Solis software or Andor SDK2;\n{}".format(default_placing_message)
		names=["atmcd.dll","atmcd{}d_legacy.dll".format(arch[:2]),"atmcd{}d.dll".format(arch[:2])]
		check_order=[(solis_path,names[0]),(solis_path,names[1])]+[("local",names[2])]+[("global",n) for n in names]+[(solis_path,names[2])]
		self.lib=load_lib(names,call_conv="stdcall",error_message=error_message,check_order=check_order)
		lib=self.lib

		self.Andor_statuscodes=Andor_statuscodes

		wrapper=ctypes_wrap.CTypesWrapper(restype=ctypes.c_uint32,errcheck=errcheck())
		strprep=ctypes_wrap.strprep(256)

		self.Initialize=wrapper(lib.Initialize, [ctypes.c_char_p], ["dir"])
		self.ShutDown=wrapper(lib.ShutDown)
		self.GetAvailableCameras=wrapper(lib.GetAvailableCameras, [ctypes.c_int32], [None])
		self.GetCameraHandle=wrapper(lib.GetCameraHandle, [ctypes.c_uint32,ctypes.c_int32], ["idx",None])
		self.GetCurrentCamera=wrapper(lib.GetCurrentCamera, [ctypes.c_int32], [None])
		self.SetCurrentCamera=wrapper(lib.SetCurrentCamera, [ctypes.c_int32], ["handle"])

		self.GetCapabilities=wrapper(lib.GetCapabilities, [AndorCapabilities], [None], rvprep=[CAndorCapabilities.prep_struct], rvconv=[CAndorCapabilities.tup_struct])
		self.GetControllerCardModel=wrapper(lib.GetControllerCardModel, [ctypes.c_char_p], [None], rvprep=[strprep], rvref=[False])
		self.GetHeadModel=wrapper(lib.GetHeadModel, [ctypes.c_char_p], [None], rvprep=[strprep], rvref=[False])
		self.GetCameraSerialNumber=wrapper(lib.GetCameraSerialNumber, [ctypes.c_int32], [None])
		self.GetPixelSize=wrapper(lib.GetPixelSize, [ctypes.c_float,ctypes.c_float], [None,None])
		self.SetFanMode=wrapper(lib.SetFanMode, [ctypes.c_int32], ["mode"])

		self.InAuxPort=wrapper(lib.InAuxPort, [ctypes.c_int32,ctypes.c_int32], ["port",None])
		self.OutAuxPort=wrapper(lib.OutAuxPort, [ctypes.c_int32,ctypes.c_int32], ["port","state"])

		self.SetTriggerMode=wrapper(lib.SetTriggerMode, [ctypes.c_int32], ["mode"])
		self.GetExternalTriggerTermination=wrapper(lib.GetExternalTriggerTermination, [ctypes.c_int32], [None])
		self.SetExternalTriggerTermination=wrapper(lib.SetExternalTriggerTermination, [ctypes.c_int32], ["termination"])
		self.GetTriggerLevelRange=wrapper(lib.GetTriggerLevelRange, [ctypes.c_float,ctypes.c_float], [None,None])
		self.SetTriggerLevel=wrapper(lib.SetTriggerLevel, [ctypes.c_float], ["mode"])
		self.SetTriggerInvert=wrapper(lib.SetTriggerInvert, [ctypes.c_int32], ["mode"])
		self.IsTriggerModeAvailable=wrapper(lib.IsTriggerModeAvailable, [ctypes.c_int32], ["mode"])
		self.SendSoftwareTrigger=wrapper(lib.SendSoftwareTrigger)
		
		errcheck_temp=errcheck(passing={20034,20035,20036,20037,20040})
		self.GetTemperature=wrapper(lib.GetTemperature, [ctypes.c_int32], [None], return_res=(True,1), errcheck=errcheck_temp)
		self.GetTemperatureF=wrapper(lib.GetTemperatureF, [ctypes.c_float], [None], return_res=(True,1), errcheck=errcheck_temp)
		self.SetTemperature=wrapper(lib.SetTemperature, [ctypes.c_int32], ["temperature"])
		self.GetTemperatureRange=wrapper(lib.GetTemperatureRange, [ctypes.c_int32,ctypes.c_int32], [None,None])
		self.CoolerON=wrapper(lib.CoolerON)
		self.CoolerOFF=wrapper(lib.CoolerOFF)
		self.IsCoolerOn=wrapper(lib.IsCoolerOn, [ctypes.c_int32], [None])

		self.GetNumberADChannels=wrapper(lib.GetNumberADChannels, [ctypes.c_int32], [None])
		self.SetADChannel=wrapper(lib.SetADChannel, [ctypes.c_int32], ["channel"])
		self.GetBitDepth=wrapper(lib.GetBitDepth, [ctypes.c_int32,ctypes.c_int32], ["channel",None])
		self.GetNumberAmp=wrapper(lib.GetNumberAmp, [ctypes.c_int32], [None])
		self.SetOutputAmplifier=wrapper(lib.SetOutputAmplifier, [ctypes.c_int32], ["typ"])
		self.IsAmplifierAvailable=wrapper(lib.IsAmplifierAvailable, [ctypes.c_int32], ["amp"])
		self.GetNumberPreAmpGains=wrapper(lib.GetNumberPreAmpGains, [ctypes.c_int32], [None])
		self.GetPreAmpGain=wrapper(lib.GetPreAmpGain, [ctypes.c_int32,ctypes.c_float], ["index",None])
		self.SetPreAmpGain=wrapper(lib.SetPreAmpGain, [ctypes.c_int32], ["index"])
		self.IsPreAmpGainAvailable=wrapper(lib.IsPreAmpGainAvailable, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["channel","amplifier","index","preamp",None])

		self.GetNumberHSSpeeds=wrapper(lib.GetNumberHSSpeeds, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["channel","typ",None])
		self.GetHSSpeed=wrapper(lib.GetHSSpeed, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_float], ["channel","typ","index",None])
		self.SetHSSpeed=wrapper(lib.SetHSSpeed, [ctypes.c_int32,ctypes.c_int32], ["typ","index"])
		self.GetNumberVSSpeeds=wrapper(lib.GetNumberVSSpeeds, [ctypes.c_int32], [None])
		self.GetVSSpeed=wrapper(lib.GetVSSpeed, [ctypes.c_int32,ctypes.c_float], ["index",None])
		self.SetVSSpeed=wrapper(lib.SetVSSpeed, [ctypes.c_int32], ["index"])
		self.GetFastestRecommendedVSSpeed=wrapper(lib.GetFastestRecommendedVSSpeed, [ctypes.c_int32,ctypes.c_float], [None,None])
		self.GetVSAmplitudeValue=wrapper(lib.GetVSAmplitudeValue, [ctypes.c_int32,ctypes.c_int32], ["index",None])
		self.SetVSAmplitude=wrapper(lib.SetVSAmplitude, [ctypes.c_int32], ["state"])

		self.GetGateMode=wrapper(lib.GetGateMode, [ctypes.c_int32], [None])
		self.SetGateMode=wrapper(lib.SetGateMode, [ctypes.c_int32], ["mode"])
		self.SetEMGainMode=wrapper(lib.SetEMGainMode, [ctypes.c_int32], ["mode"])
		self.GetEMGainRange=wrapper(lib.GetEMGainRange, [ctypes.c_int32,ctypes.c_int32], [None,None])
		self.GetEMCCDGain=wrapper(lib.GetEMCCDGain, [ctypes.c_int32], [None])
		self.SetEMCCDGain=wrapper(lib.SetEMCCDGain, [ctypes.c_int32], ["gain"])
		self.GetEMAdvanced=wrapper(lib.GetEMAdvanced, [ctypes.c_int32], [None])
		self.SetEMAdvanced=wrapper(lib.SetEMAdvanced, [ctypes.c_int32], ["state"])
		# self.SetMCPGating=wrapper(lib.SetMCPGating, [ctypes.c_int32], ["mode"])
		# self.GetMCPGainRange=wrapper(lib.GetMCPGainRange, [ctypes.c_int32,ctypes.c_int32], [None,None])
		# self.SetMCPGain=wrapper(lib.SetMCPGain, [ctypes.c_int32], ["gain"])

		self.GetShutterMinTimes=wrapper(lib.GetShutterMinTimes, [ctypes.c_int32,ctypes.c_int32], [None,None])
		self.SetShutter=wrapper(lib.SetShutter, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["typ","mode","closing_time","opening_time"])
		self.SetShutterEx=wrapper(lib.SetShutterEx, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["typ","mode","closing_time","opening_time","extmode"])

		self.SetAcquisitionMode=wrapper(lib.SetAcquisitionMode, [ctypes.c_uint32], ["mode"])
		self.GetAcquisitionTimings=wrapper(lib.GetAcquisitionTimings, [ctypes.c_float,ctypes.c_float,ctypes.c_float], [None,None,None])
		self.SetExposureTime=wrapper(lib.SetExposureTime, [ctypes.c_float], ["time"])
		self.SetNumberAccumulations=wrapper(lib.SetNumberAccumulations, [ctypes.c_int32], ["number"])
		self.SetNumberKinetics=wrapper(lib.SetNumberKinetics, [ctypes.c_int32], ["number"])
		self.SetNumberPrescans=wrapper(lib.SetNumberPrescans, [ctypes.c_int32], ["number"])
		self.SetKineticCycleTime=wrapper(lib.SetKineticCycleTime, [ctypes.c_float], ["time"])
		self.SetAccumulationCycleTime=wrapper(lib.SetAccumulationCycleTime, [ctypes.c_float], ["time"])
		self.SetFrameTransferMode=wrapper(lib.SetFrameTransferMode, [ctypes.c_uint32], ["mode"])
		self.GetReadOutTime=wrapper(lib.GetReadOutTime, [ctypes.c_float], [None])
		self.GetKeepCleanTime=wrapper(lib.GetKeepCleanTime, [ctypes.c_float], [None])

		self.PrepareAcquisition=wrapper(lib.PrepareAcquisition)
		self.StartAcquisition=wrapper(lib.StartAcquisition)
		self.AbortAcquisition=wrapper(lib.AbortAcquisition)
		self.GetAcquisitionProgress=wrapper(lib.GetAcquisitionProgress, [ctypes.c_int32,ctypes.c_int32], [None,None])
		self.GetStatus=wrapper(lib.GetStatus, [ctypes.c_int32], [None])
		self.WaitForAcquisition=wrapper(lib.WaitForAcquisition)
		self.WaitForAcquisitionTimeOut=wrapper(lib.WaitForAcquisitionTimeOut, [ctypes.c_int32], ["timeout_ms"])
		self.WaitForAcquisitionByHandle=wrapper(lib.WaitForAcquisitionByHandle, [ctypes.c_int32], ["handle"])
		self.WaitForAcquisitionByHandleTimeOut=wrapper(lib.WaitForAcquisitionByHandleTimeOut, [ctypes.c_int32,ctypes.c_int32], ["handle","timeout_ms"])
		self.CancelWait=wrapper(lib.CancelWait)

		self.SetReadMode=wrapper(lib.SetReadMode, [ctypes.c_uint32], ["mode"])
		self.GetMaximumBinning=wrapper(lib.GetMaximumBinning, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["read_mode","horiz_vert",None])
		self.GetMinimumImageLength=wrapper(lib.GetMinimumImageLength, [ctypes.c_int32], [None])
		self.SetSingleTrack=wrapper(lib.SetSingleTrack, [ctypes.c_int32,ctypes.c_int32], ["center","height"])
		self.SetMultiTrack=wrapper(lib.SetMultiTrack, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["number","height","offset",None,None])
		ctypes_wrap.setup_func(lib.SetRandomTracks ,[ctypes.c_int32,ctypes.POINTER(ctypes.c_int32)], errcheck=errcheck())
		def SetRandomTracks(tracks):
			ntracks=len(tracks)
			areas=(ctypes.c_int32*(ntracks*2))(*[b for t in tracks for b in t])
			lib.SetRandomTracks(ntracks,areas)
		self.SetRandomTracks=SetRandomTracks
		self.SetImage=wrapper(lib.SetImage, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["hbin","vbin","hstart","hend","vstart","vend"])
		self.GetDetector=wrapper(lib.GetDetector, [ctypes.c_int32,ctypes.c_int32], [None,None])
		self.GetSizeOfCircularBuffer=wrapper(lib.GetSizeOfCircularBuffer, [ctypes.c_int32], [None])
		buffer16_prep=ctypes_wrap.buffprep(0,"<u2")
		buffer32_prep=ctypes_wrap.buffprep(0,"<u4")
		buffer16_conv=ctypes_wrap.buffconv(0,"<u2")
		buffer32_conv=ctypes_wrap.buffconv(0,"<u4")
		self.GetOldestImage  =wrapper(lib.GetOldestImage  , [ctypes.c_char_p,ctypes.c_uint32], [None,"size"], rvprep=[buffer32_prep], rvconv=[buffer32_conv], rvref=[False])
		self.GetOldestImage16=wrapper(lib.GetOldestImage16, [ctypes.c_char_p,ctypes.c_uint32], [None,"size"], rvprep=[buffer16_prep], rvconv=[buffer16_conv], rvref=[False])
		self.GetMostRecentImage  =wrapper(lib.GetMostRecentImage  , [ctypes.c_char_p,ctypes.c_uint32], [None,"size"], rvprep=[buffer32_prep], rvconv=[buffer32_conv], rvref=[False])
		self.GetMostRecentImage16=wrapper(lib.GetMostRecentImage16, [ctypes.c_char_p,ctypes.c_uint32], [None,"size"], rvprep=[buffer16_prep], rvconv=[buffer16_conv], rvref=[False])
		self.GetNumberNewImages=wrapper(lib.GetNumberNewImages, [ctypes.c_int32,ctypes.c_int32], [None,None])
		def images_buffer16_prep(first, last, size):
			return buffer16_prep(size)
		def images_buffer32_prep(first, last, size):
			return buffer32_prep(size)
		def images_buffer16_conv(buff, first, last, size):
			return buffer16_conv(buff,size)
		def images_buffer32_conv(buff, first, last, size):
			return buffer32_conv(buff,size)
		self.GetImages=wrapper(lib.GetImages, [ctypes.c_int32,ctypes.c_int32,ctypes.c_char_p,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["first","last",None,"size",None,None],
			rvprep=[images_buffer32_prep,None,None], rvconv=[images_buffer32_conv,None,None], rvref=[False,True,True])
		self.GetImages16=wrapper(lib.GetImages16, [ctypes.c_int32,ctypes.c_int32,ctypes.c_char_p,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["first","last",None,"size",None,None],
			rvprep=[images_buffer16_prep,None,None], rvconv=[images_buffer16_conv,None,None], rvref=[False,True,True])

		self._initialized=True

	AmpModeSimple=collections.namedtuple("AmpModeSimple",["channel","oamp","hsspeed","preamp"])
	AmpModeFull=collections.namedtuple("AmpModeFull",["channel","channel_bitdepth","oamp","oamp_kind","hsspeed","hsspeed_MHz","preamp","preamp_gain"])
	_oamp_kinds=["EMCCD/Conventional","CCD/ExtendedNIR"]
	def get_all_amp_modes(self):
		"""
		Get all available pream modes.

		Each preamp mode is characterized by an AD channel index, amplifier index, channel speed (horizontal scan speed) index and preamp gain index.
		Return list of tuples ``(channel, channel_bitdepth, oamp, oamp_kind, hsspeed, hsspeed_MHz, preamp, preamp_gain)``,
		where ``channel``, ``oamp``, ``hsspeed`` and ``preamp`` are indices, while ``channel_bitdepth``, ``oamp_kind``, ``hsspeed_MHz`` and ``preamp_gain`` are descriptions.
		"""
		channels=self.GetNumberADChannels()
		oamps=self.GetNumberAmp()
		preamps=self.GetNumberPreAmpGains()
		modes=[]
		for ch in range(channels):
			bit_depth=self.GetBitDepth(ch)
			for oamp in range(oamps):
				hsspeeds=self.GetNumberHSSpeeds(ch,oamp)
				for hssp in range(hsspeeds):
					hsspeed_hz=self.GetHSSpeed(ch,oamp,hssp)
					for pa in range(preamps):
						preamp_gain=self.GetPreAmpGain(pa)
						try:
							self.IsPreAmpGainAvailable(ch,oamp,hssp,pa)
							modes.append(self.AmpModeFull(ch,bit_depth,oamp,self._oamp_kinds[oamp],hssp,hsspeed_hz,pa,preamp_gain))
						except AndorLibError:
							pass
		return modes

	def set_amp_mode(self, amp_mode):
		"""
		Setup preamp mode.

		`amp_mode` is a tuple ``(channel, oamp, hsspeed, preamp)``, specifying AD channel index, amplifier index, channel speed (horizontal scan speed) index and preamp gain index.
		"""
		if len(amp_mode)==4:
			amp_mode=self.AmpModeSimple(*amp_mode)
		else:
			amp_mode=self.AmpModeFull(*amp_mode)
		if amp_mode.channel is not None:
			self.SetADChannel(amp_mode.channel)
		if amp_mode.oamp is not None:
			self.SetOutputAmplifier(amp_mode.oamp)
			if amp_mode.hsspeed is not None:
				self.SetHSSpeed(amp_mode.oamp,amp_mode.hsspeed)
		if amp_mode.preamp is not None:
			self.SetPreAmpGain(amp_mode.preamp)

	def get_EMCCD_gain(self):
		"""
		Get current EMCCD gain.

		Return tuple ``(gain, advanced)``.
		"""
		advanced=self.GetEMAdvanced()
		gain=self.GetEMCCDGain()
		return advanced, gain
	def set_EMCCD_gain(self, gain, advanced=None):
		"""
		Set EMCCD gain.

		Gain goes up to 300 if ``advanced==False`` or higher if ``advanced==True`` (in this mode the sensor can be permanently damaged by strong light).
		"""
		if advanced is not None:
			self.SetEMAdvanced(advanced)
		self.SetEMCCDGain(gain)


lib=AndorLib()