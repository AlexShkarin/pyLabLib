from ...core.utils import ctypes_wrap
from .misc import load_lib, default_placing_message

import numpy as np
import numba as nb

import ctypes
import collections
import os.path
import platform

##### Constants #####

AndorSDK3_statuscodes = {
	0: "AT_SUCCESS",
	1: "AT_ERR_NOTINITIALISED",
	2: "AT_ERR_NOTIMPLEMENTED",
	3: "AT_ERR_READONLY",
	4: "AT_ERR_NOTREADABLE",
	5: "AT_ERR_NOTWRITABLE",
	6: "AT_ERR_OUTOFRANGE",
	7: "AT_ERR_INDEXNOTAVAILABLE",
	8: "AT_ERR_INDEXNOTIMPLEMENTED",
	9: "AT_ERR_EXCEEDEDMAXSTRINGLENGTH",
	10: "AT_ERR_CONNECTION",
	11: "AT_ERR_NODATA",
	12: "AT_ERR_INVALIDHANDLE",
	13: "AT_ERR_TIMEDOUT",
	14: "AT_ERR_BUFFERFULL",
	15: "AT_ERR_INVALIDSIZE",
	16: "AT_ERR_INVALIDALIGNMENT",
	17: "AT_ERR_COMM",
	18: "AT_ERR_STRINGNOTAVAILABLE",
	19: "AT_ERR_STRINGNOTIMPLEMENTED",
	20: "AT_ERR_NULL_FEATURE",
	21: "AT_ERR_NULL_HANDLE",
	22: "AT_ERR_NULL_IMPLEMENTED_VAR",
	23: "AT_ERR_NULL_READABLE_VAR",
	24: "AT_ERR_NULL_READONLY_VAR",
	25: "AT_ERR_NULL_WRITABLE_VAR",
	26: "AT_ERR_NULL_MINVALUE",
	27: "AT_ERR_NULL_MAXVALUE",
	28: "AT_ERR_NULL_VALUE",
	29: "AT_ERR_NULL_STRING",
	30: "AT_ERR_NULL_COUNT_VAR",
	31: "AT_ERR_NULL_ISAVAILABLE_VAR",
	32: "AT_ERR_NULL_MAXSTRINGLENGTH",
	33: "AT_ERR_NULL_EVCALLBACK",
	34: "AT_ERR_NULL_QUEUE_PTR",
	35: "AT_ERR_NULL_WAIT_PTR",
	36: "AT_ERR_NULL_PTRSIZE",
	37: "AT_ERR_NOMEMORY",
	38: "AT_ERR_DEVICEINUSE",
	39: "AT_ERR_DEVICENOTFOUND",
	100: "AT_ERR_HARDWARE_OVERFLOW"
}
def text_status(status):
    if status in AndorSDK3_statuscodes:
        return AndorSDK3_statuscodes[status]
    raise AndorSDK3LibError("unrecognized status code: {}".format(status),-1)


AndorSDK3_feature_types={
	"AcquisitionStart": "comm",
	"AcquisitionStop": "comm",
	"CameraDump": "comm",
	"DDGStepUploadModeValues": "comm",
	"I2CRead": "comm",
	"I2CWrite": "comm",
	"SoftwareTrigger": "comm",
	"TimestampClockReset": "comm",

	"AccumulateCount": "int",
	"AcquiredCount": "int",
	"AOIHBin": "int",
	"AOIHeight": "int",
	"AOILeft": "int",
	"AOIStride": "int",
	"AOITop": "int",
	"AOIVBin": "int",
	"AOIWidth": "int",
	"Baseline": "int",
	"BufferOverflowEvent": "int",
	"CameraMemory": "int",
	"DDGIOCNumberOfPulses": "int",
	"DDGIOCPeriod": "int",
	"DDGOutputDelay": "int",
	"DDGOutputWidth": "int",
	"DDGStepCount": "int",
	"DDGStepUploadProgress": "int",
	"DeviceCount": "int",
	"DeviceVideoIndex": "int",
	"EventsMissedEvent": "int",
	"ExposedPixelHeight": "int",
	"ExposureEndEvent": "int",
	"ExposureStartEvent": "int",
	"FrameCount": "int",
	"I2CAddress": "int",
	"I2CByte": "int",
	"I2CByteCount": "int",
	"I2CByteSelector": "int",
	"ImageSizeBytes": "int",
	"LUTIndex": "int",
	"LUTValue": "int",
	"MCPGain": "int",
	"MCPVoltage": "int",
	"MultitrackCount": "int",
	"MultitrackEnd": "int",
	"MultitrackSelector": "int",
	"MultitrackStart": "int",
	"PortSelector": "int",
	"PreAmpGainValue": "int",
	"PreAmpOffsetValue": "int",
	"RowNExposureEndEvent": "int",
	"RowNExposureStartEvent": "int",
	"SensorHeight": "int",
	"SensorWidth": "int",
	"TimestampClock": "int",
	"TimestampClockFrequency": "int",
	"UsbProductId": "int",
	"UsbDeviceId": "int",

	"AlternatingReadoutDirection": "bool",
	"CameraAcquiring": "bool",
	"CameraPresent": "bool",
	"DDGIOCEnable": "bool",
	"DDGOutputEnable": "bool",
	"DDGOutputStepEnable": "bool",
	"DDGOpticalWidthEnable": "bool",
	"DDGStepEnabled": "bool",
	"DDGStepUploadRequired": "bool",
	"DisableShutter": "bool",
	"EventEnable": "bool",
	"ExternalIOReadout": "bool",
	"FastAOIFrameRateEnable": "bool",
	"ForceShutterOpen": "bool",
	"FrameIntervalTiming": "bool",
	"FullAOIControl": "bool",
	"IODirection": "bool",
	"IOState": "bool",
	"IOInvert": "bool",
	"IRPreFlashEnable": "bool",
	"KeepCleanEnable": "bool",
	"KeepCleanPostExposureEnable": "bool",
	"MCPIntelligate": "bool",
	"MetadataEnable": "bool",
	"MetadataFrame": "bool",
	"MetadataFrameInfo": "bool",
	"MetadataTimestamp": "bool",
	"MultitrackBinned": "bool",
	"Overlap": "bool",
	"PIVEnable": "bool",
	"PreTriggerEnable": "bool",
	"RollingShutterGlobalClear": "bool",
	"ScanSpeedControlEnable": "bool",
	"SensorCooling": "bool",
	"ShutterAmpControl": "bool",
	"ShutterState": "bool",
	"SpuriousNoiseFilter": "bool",
	"StaticBlemishCorrection": "bool",
	"SynchronousTriggering": "bool",
	"TransmitFrames": "bool",
	"VerticallyCentreAOI": "bool",
	
	"BackoffTemperatureOffset": "float",
	"BytesPerPixel": "float",
	"CoolerPower": "float",
	"DDGStepDelayCoefficientA": "float",
	"DDGStepDelayCoefficientB": "float",
	"DDGStepWidthCoefficientA": "float",
	"DDGStepWidthCoefficientB": "float",
	"ExposureTime": "float",
	"ExternalTriggerDelay": "float",
	"FrameInterval": "float",
	"FrameRate": "float",
	"HeatSinkTemperature": "float",
	"InputVoltage": "float",
	"LineScanSpeed": "float",
	"PixelHeight": "float",
	"PixelWidth": "float",
	"ReadoutTime": "float",
	"RowReadTime": "float",
	"SensorTemperature": "float",
	"ShutterTransferTime": "float",
	"TargetSensorTemperature": "float",
	
	"CameraFamily": "str",
	"CameraModel": "str",
	"CameraName": "str",
	"ControllerID": "str",
	"DDR2Type": "str",
	"DriverVersion": "str",
	"FirmwareVersion": "str",
	"MicrocodeVersion": "str",
	"SerialNumber": "str",
	"SoftwareVersion": "str",
	
	"AOIBinning": "enum",
	"AOILayout": "enum",
	"AuxiliaryOutSource": "enum",
	"AuxOutSourceTwo": "enum",
	"BitDepth": "enum",
	"ColourFilter": "enum",
	"CycleMode": "enum",
	"DDGOutputPolarity": "enum",
	"DDGOutputSelector": "enum",
	"DDGStepDelayMode": "enum",
	"DDGStepWidthMode": "enum",
	"ElectronicShutteringMode": "enum",
	"EventSelector": "enum",
	"FanSpeed": "enum",
	"GateMode": "enum",
	"InsertionDelay": "enum",
	"IOControl": "enum",
	"IOSelector": "enum",
	"PixelCorrection": "enum",
	"PixelEncoding": "enum",
	"PixelReadoutRate": "enum",
	"PreAmpGain": "enum",
	"PreAmpGainChannel": "enum",
	"PreAmpGainControl": "enum",
	"PreAmpGainSelector": "enum",
	"SensorReadoutMode": "enum",
	"SensorType": "enum",
	"ShutterMode": "enum",
	"ShutterOutputMode": "enum",
	"SimplePreAmpGainControl": "enum",
	"TemperatureControl": "enum",
	"TemperatureStatus": "enum",
	"TriggerMode": "enum"
}

class AndorSDK3LibError(RuntimeError):
	"""Generic Andor SDK3 library error"""
	def __init__(self, func, code):
		self.func=func
		self.code=code
		self.text_code=AndorSDK3_statuscodes.get(code,"UNKNOWN")
		msg="function '{}' raised error {}({})".format(func,code,self.text_code)
		RuntimeError.__init__(self,msg)
def errcheck(passing=None):
	"""
	Build an error checking function.

	Return a function which checks return codes of Andor library functions.
	`passing` is a list specifying which return codes are acceptable (by default only 20002, which is success code, is acceptable).
	"""
	passing=set(passing) if passing is not None else set()
	passing.add(0) # always allow success
	def checker(result, func, arguments):
		if result not in passing:
			raise AndorSDK3LibError(func.__name__,result)
		return AndorSDK3_statuscodes[result]
	return checker

_default_str_len=512

class AndorSDK3Lib(object):
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
			sdk3_path=r"C:\Program Files (x86)\Andor SDK3"
		else:
			solis_path=r"C:\Program Files\Andor SOLIS"
			sdk3_path=r"C:\Program Files\Andor SDK3"
		error_message=(	"The library is supplied with Andor Solis software or Andor SDK3;\n"
						"Additional required libraries:  atblkbx.dll, atcl_bitflow.dll, atdevapogee.dll, atdevregcam.dll, atusb_libusb.dll, atusb_libusb10.dll;\n"
						"{}").format(default_placing_message)
		self.lib=load_lib("atcore.dll",locations=(solis_path,sdk3_path,"local","global"),call_conv="stdcall",locally=True,error_message=error_message)
		lib=self.lib
		AT_H=ctypes.c_int
		AT_pWC=ctypes.c_wchar_p
		AT_BOOL=ctypes.c_int
		AT_64=ctypes.c_int64
		AT_U8p=ctypes.POINTER(ctypes.c_uint8)

		self.AndorSDK3_statuscodes=AndorSDK3_statuscodes

		wrapper=ctypes_wrap.CTypesWrapper(restype=ctypes.c_uint32,errcheck=errcheck())
		def strprep(*args):
			return ctypes.cast(ctypes.create_unicode_buffer(512),AT_pWC)

		self.AT_InitialiseLibrary=wrapper(lib.AT_InitialiseLibrary)
		self.AT_FinaliseLibrary=wrapper(lib.AT_FinaliseLibrary)
		self.AT_Open=wrapper(lib.AT_Open, [ctypes.c_int,AT_H], ["idx",None])
		self.AT_Close=wrapper(lib.AT_Close, [AT_H], ["handle"])

		self.AT_IsImplemented=wrapper(lib.AT_IsImplemented, [AT_H,AT_pWC,AT_BOOL], ["handle","feature",None])
		self.AT_IsReadable=wrapper(lib.AT_IsReadable, [AT_H,AT_pWC,AT_BOOL], ["handle","feature",None])
		self.AT_IsWritable=wrapper(lib.AT_IsWritable, [AT_H,AT_pWC,AT_BOOL], ["handle","feature",None])
		self.AT_IsReadOnly=wrapper(lib.AT_IsReadOnly, [AT_H,AT_pWC,AT_BOOL], ["handle","feature",None])

		self.AT_SetInt=wrapper(lib.AT_SetInt, [AT_H,AT_pWC,AT_64], ["handle","feature","value"])
		self.AT_GetInt=wrapper(lib.AT_GetInt, [AT_H,AT_pWC,AT_64], ["handle","feature",None])
		self.AT_GetIntMax=wrapper(lib.AT_GetIntMax, [AT_H,AT_pWC,AT_64], ["handle","feature",None])
		self.AT_GetIntMin=wrapper(lib.AT_GetIntMin, [AT_H,AT_pWC,AT_64], ["handle","feature",None])

		self.AT_SetFloat=wrapper(lib.AT_SetFloat, [AT_H,AT_pWC,ctypes.c_double], ["handle","feature","value"])
		self.AT_GetFloat=wrapper(lib.AT_GetFloat, [AT_H,AT_pWC,ctypes.c_double], ["handle","feature",None])
		self.AT_GetFloatMax=wrapper(lib.AT_GetFloatMax, [AT_H,AT_pWC,ctypes.c_double], ["handle","feature",None])
		self.AT_GetFloatMin=wrapper(lib.AT_GetFloatMin, [AT_H,AT_pWC,ctypes.c_double], ["handle","feature",None])

		self.AT_SetBool=wrapper(lib.AT_SetBool, [AT_H,AT_pWC,AT_BOOL], ["handle","feature","value"])
		self.AT_GetBool=wrapper(lib.AT_GetBool, [AT_H,AT_pWC,AT_BOOL], ["handle","feature",None])

		self.AT_SetEnumIndex=wrapper(lib.AT_SetEnumIndex, [AT_H,AT_pWC,ctypes.c_int], ["handle","feature","value"])
		self.AT_SetEnumString=wrapper(lib.AT_SetEnumString, [AT_H,AT_pWC,AT_pWC], ["handle","feature","value"])
		self.AT_GetEnumIndex=wrapper(lib.AT_GetEnumIndex, [AT_H,AT_pWC,ctypes.c_int], ["handle","feature",None])
		self.AT_GetEnumStringByIndex=wrapper(lib.AT_GetEnumStringByIndex, [AT_H,AT_pWC,ctypes.c_int,AT_pWC,ctypes.c_int], ["handle","feature","index",None,"length"], rvprep=[strprep], rvref=[False])
		self.AT_IsEnumIndexAvailable=wrapper(lib.AT_IsEnumIndexAvailable, [AT_H,AT_pWC,ctypes.c_int,AT_BOOL], ["handle","feature","value",None])
		self.AT_IsEnumIndexImplemented=wrapper(lib.AT_IsEnumIndexImplemented, [AT_H,AT_pWC,ctypes.c_int,AT_BOOL], ["handle","feature","value",None])
		self.AT_GetEnumCount=wrapper(lib.AT_GetEnumCount, [AT_H,AT_pWC,ctypes.c_int], ["handle","feature",None])

		self.AT_SetString=wrapper(lib.AT_SetString, [AT_H,AT_pWC,AT_pWC], ["handle","feature","value"])
		self.AT_GetString=wrapper(lib.AT_GetString, [AT_H,AT_pWC,AT_pWC,ctypes.c_int], ["handle","feature",None,"length"], rvprep=[strprep], rvref=[False])
		self.AT_GetStringMaxLength=wrapper(lib.AT_GetStringMaxLength, [AT_H,AT_pWC,ctypes.c_int], ["handle","feature",None])

		self.AT_Command=wrapper(lib.AT_Command, [AT_H,AT_pWC], ["handle","command"])

		self.AT_QueueBuffer=wrapper(lib.AT_QueueBuffer, [AT_H,AT_U8p,ctypes.c_int], ["handle","buffer","size"])
		self.AT_WaitBuffer=wrapper(lib.AT_WaitBuffer, [AT_H,AT_U8p,ctypes.c_int,ctypes.c_uint], ["handle",None,None,"timeout"])
		self.AT_Flush=wrapper(lib.AT_Flush, [AT_H], ["handle"])

		self.c_callback=ctypes.WINFUNCTYPE(ctypes.c_int,AT_H,AT_pWC,ctypes.c_void_p)
		lib.AT_RegisterFeatureCallback.argtypes=[AT_H,AT_pWC,self.c_callback,ctypes.c_voidp]
		lib.AT_RegisterFeatureCallback.restype=ctypes.c_uint32
		lib.AT_RegisterFeatureCallback.errcheck=errcheck()
		def AT_RegisterFeatureCallback(handle, feature, callback, context=None, wrap=True):
			if wrap:
				def wrapped_callback(*args):
					try:
						callback(*args)
						return 0
					except:
						return 1
				cb=self.c_callback(wrapped_callback)
			else:
				cb=self.c_callback(callback)
			lib.AT_RegisterFeatureCallback(handle,feature,cb,context)
			return cb
		self.AT_RegisterFeatureCallback=AT_RegisterFeatureCallback
		lib.AT_UnregisterFeatureCallback.argtypes=[AT_H,AT_pWC,self.c_callback,ctypes.c_voidp]
		lib.AT_UnregisterFeatureCallback.restype=ctypes.c_uint32
		lib.AT_UnregisterFeatureCallback.errcheck=errcheck()
		def AT_UnregisterFeatureCallback(handle, feature, cb):
			lib.AT_UnregisterFeatureCallback(handle,feature,cb,0)
		self.AT_UnregisterFeatureCallback=AT_UnregisterFeatureCallback

		self._initialized=True

	def allocate_buffers(self, handle, nframes, frame_size):
		buffs=[]
		for _ in range(nframes):
			b=ctypes.create_string_buffer(frame_size)
			buffs.append(b)
		return buffs
	def flush_buffers(self, handle):
		while True:
			try:
				self.AT_WaitBuffer(handle,0)
			except AndorSDK3LibError as e:
				if e.code==13:
					break
				raise
		self.AT_Flush(handle)
		return


def read_uint12(raw_data, width):
	"""
	Convert packed 12bit data (3 bytes per 2 pixels) into unpacked 16bit data (2 bytes per pixel).

	`raw_data` is a 2D numpy array with the raw frame data of dimensions ``(nrows, stride)``, where ``stride`` is the size of one row in bytes.
	`width` is the size of the resulting row in pixels; if it is 0, assumed to be maximal possible size.
	"""
	data=raw_data.astype("<u2")
	fst_uint8,mid_uint8,lst_uint8=data[:,::3],data[:,1::3],data[:,2::3]
	result=np.empty(shape=(fst_uint8.shape[0],lst_uint8.shape[1]+mid_uint8.shape[1]),dtype="<u2")
	result[:,::2]=(fst_uint8[:,:mid_uint8.shape[1]]<<4)|(mid_uint8&0x0F)
	result[:,1::2]=(mid_uint8[:,:lst_uint8.shape[1]]>>4)|(lst_uint8<<4)
	return result[:,:width] if width else result

try:
	nb_uint8_ro=nb.typeof(np.frombuffer(b"\x00",dtype="u1").reshape((1,1))) # for readonly attribute of a numpy array
	nb_width=nb.typeof(np.zeros([0]).shape[0])
	@nb.njit(nb.uint16[:,:](nb_uint8_ro,nb_width),parallel=False)
	def nb_read_uint12(raw_data, width):
		"""
		Convert packed 12bit data (3 bytes per 2 pixels) into unpacked 16bit data (2 bytes per pixel).

		`raw_data` is a 2D numpy array with the raw frame data of dimensions ``(nrows, stride)``, where ``stride`` is the size of one row in bytes.
		`width` is the size of the resulting row in pixels; if it is 0, assumed to be maximal possible size.

		Funcation semantics is identical to :func:`read_uint12`, but it is implemented with Numba to speed up calculations.
		"""
		h,s=raw_data.shape
		if width==0:
			width=(s*2)//3
		out=np.empty((h,width),dtype=nb.uint16)
		chwidth=width//2
		for i in range(h):
			for j in range(chwidth):
				fst_uint8=nb.uint16(raw_data[i,j*3])
				mid_uint8=nb.uint16(raw_data[i,j*3+1])
				lst_uint8=nb.uint16(raw_data[i,j*3+2])
				out[i,j*2]=(fst_uint8<<4)|(mid_uint8&0x0F)
				out[i,j*2+1]=(mid_uint8>>4)|(lst_uint8<<4)
			if width%2==1:
				fst_uint8=nb.uint16(raw_data[i,chwidth*3])
				mid_uint8=nb.uint16(raw_data[i,chwidth*3+1])
				out[i,width-1]=(fst_uint8<<4)|(mid_uint8&0x0F)
		return out
except nb.errors.NumbaError:
	nb_read_uint12=read_uint12

lib=AndorSDK3Lib()