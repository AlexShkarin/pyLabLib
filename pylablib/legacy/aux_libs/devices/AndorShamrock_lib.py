from ...core.utils import ctypes_wrap
from .misc import default_placing_message, load_lib

import ctypes
import os.path
import contextlib
import platform


##### Constants #####

Shamrock_errorcodes = {
		20201: "SHAMROCK_COMMUNICATION_ERROR",
		20202: "SHAMROCK_SUCCESS",
		20266: "SHAMROCK_P1INVALID",
		20267: "SHAMROCK_P2INVALID",
		20268: "SHAMROCK_P3INVALID",
		20269: "SHAMROCK_P4INVALID",
		20275: "SHAMROCK_NOT_INITIALIZED",
		20292: "SHAMROCK_NOT_AVAILABLE",
}


##### Errors #####

class ShamrockLibError(RuntimeError):
	"""Generic Andor Shamrock library error"""
	def __init__(self, func, code):
		self.func=func
		self.code=code
		self.text_code=Shamrock_errorcodes.get(code,"UNKNOWN")
		msg="function '{}' raised error {}({})".format(func,code,self.text_code)
		RuntimeError.__init__(self,msg)
def errcheck(passing=None):
	"""
	Build an error checking function.

	Return a function which checks return codes of Andor Shamrock library functions.
	`passing` is a list specifying which return codes are acceptable (by default only 20002, which is success code, is acceptable).
	"""
	passing=set(passing) if passing is not None else set()
	passing.add(20202) # always allow success
	def checker(result, func, arguments):
		if result not in passing:
			raise ShamrockLibError(func.__name__,result)
		return Shamrock_errorcodes[result]
	return checker


##### Library #####

class ShamrockLib(object):
	def __init__(self):
		object.__init__(self)
		self._initialized=False
		self._opened_handles_num=0

	def initlib(self):
		if self._initialized:
			return
		arch=platform.architecture()[0]
		winarch="64bit" if platform.machine().endswith("64") else "32bit"
		if arch=="32bit" and winarch=="64bit":
			solis_path=r"C:\Program Files (x86)\Andor SOLIS"
		else:
			solis_path=r"C:\Program Files\Andor SOLIS"
		shamrock_path=os.path.join(solis_path,r"Drivers\Shamrock")
		error_message="The library is supplied with Andor Solis software;\n{}".format(default_placing_message)
		self.lib=load_lib(("atspectrograph.dll","shamrockcif{}.dll".format("" if arch[:2]=="32" else arch[:2])),
			locations=(solis_path,shamrock_path,"local","global"),call_conv="stdcall",locally=True,error_message=error_message,check_order="name")
		lib=self.lib

		self.Shamrock_errorcodes=Shamrock_errorcodes

		wrapper=ctypes_wrap.CTypesWrapper(restype=ctypes.c_uint32,errcheck=errcheck())
		strprep=ctypes_wrap.strprep(256)
		c_float_p=ctypes.POINTER(ctypes.c_float)

		self.ShamrockInitialize=wrapper(lib.ShamrockInitialize, [ctypes.c_char_p], ["dir"])
		self.ShamrockClose=wrapper(lib.ShamrockClose)
		self.ShamrockGetNumberDevices=wrapper(lib.ShamrockGetNumberDevices, [ctypes.c_int32], [None])
		self.ShamrockGetFunctionReturnDescription=wrapper(lib.ShamrockGetFunctionReturnDescription, [ctypes.c_uint32,ctypes.c_char_p,ctypes.c_int32], ["code",None,None],
			rvprep=[strprep,256], rvref=[False,False], rvnames=["desc",None])

		self.ShamrockGetSerialNumber=wrapper(lib.ShamrockGetSerialNumber, [ctypes.c_int32,ctypes.c_char_p], ["idx",None], rvprep=[strprep], rvref=[False])
		self.ShamrockEepromGetOpticalParams=wrapper(lib.ShamrockEepromGetOpticalParams, [ctypes.c_int32,ctypes.c_float,ctypes.c_float,ctypes.c_float], ["idx",None,None,None])

		self.ShamrockGetNumberGratings=wrapper(lib.ShamrockGetNumberGratings, [ctypes.c_int32,ctypes.c_int32], ["idx",None])
		self.ShamrockGetGratingInfo=wrapper(lib.ShamrockGetGratingInfo, [ctypes.c_int32,ctypes.c_int32,ctypes.c_float,ctypes.c_char_p,ctypes.c_int32,ctypes.c_int32],
			["idx","grating",None,None,None,None], rvprep=[None,strprep,None,None], rvref=[True,False,True,True])
		self.ShamrockGratingIsPresent=wrapper(lib.ShamrockGratingIsPresent, [ctypes.c_int32,ctypes.c_int32], ["idx",None])
		self.ShamrockGetTurret=wrapper(lib.ShamrockGetTurret, [ctypes.c_int32,ctypes.c_int32], ["idx",None])
		self.ShamrockSetTurret=wrapper(lib.ShamrockSetTurret, [ctypes.c_int32,ctypes.c_int32], ["idx","turret"])
		self.ShamrockGetGrating=wrapper(lib.ShamrockGetGrating, [ctypes.c_int32,ctypes.c_int32], ["idx",None])
		self.ShamrockSetGrating=wrapper(lib.ShamrockSetGrating, [ctypes.c_int32,ctypes.c_int32], ["idx","grating"])
		self.ShamrockGetGratingOffset=wrapper(lib.ShamrockGetGratingOffset, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["idx","grating",None])
		self.ShamrockSetGratingOffset=wrapper(lib.ShamrockSetGratingOffset, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["idx","grating","offset"])
		self.ShamrockGetDetectorOffset=wrapper(lib.ShamrockGetDetectorOffset, [ctypes.c_int32,ctypes.c_int32], ["idx",None])
		self.ShamrockSetDetectorOffset=wrapper(lib.ShamrockSetDetectorOffset, [ctypes.c_int32,ctypes.c_int32], ["idx","offset"])
		self.ShamrockGetDetectorOffsetPort2=wrapper(lib.ShamrockGetDetectorOffsetPort2, [ctypes.c_int32,ctypes.c_int32], ["idx",None])
		self.ShamrockSetDetectorOffsetPort2=wrapper(lib.ShamrockSetDetectorOffsetPort2, [ctypes.c_int32,ctypes.c_int32], ["idx","offset"])
		self.ShamrockWavelengthReset=wrapper(lib.ShamrockWavelengthReset, [ctypes.c_int32], ["idx"])

		self.ShamrockWavelengthIsPresent=wrapper(lib.ShamrockWavelengthIsPresent, [ctypes.c_int32,ctypes.c_int32], ["idx",None])
		self.ShamrockGetWavelength=wrapper(lib.ShamrockGetWavelength, [ctypes.c_int32,ctypes.c_float], ["idx",None])
		self.ShamrockGetWavelengthLimits=wrapper(lib.ShamrockGetWavelengthLimits, [ctypes.c_int32,ctypes.c_int32,ctypes.c_float,ctypes.c_float], ["idx","grating",None,None])
		self.ShamrockSetWavelength=wrapper(lib.ShamrockSetWavelength, [ctypes.c_int32,ctypes.c_float], ["idx","wavelength"])
		self.ShamrockAtZeroOrder=wrapper(lib.ShamrockAtZeroOrder, [ctypes.c_int32,ctypes.c_int32], ["idx",None])
		self.ShamrockGotoZeroOrder=wrapper(lib.ShamrockGotoZeroOrder, [ctypes.c_int32], ["idx"])

		self.ShamrockAutoSlitIsPresent=wrapper(lib.ShamrockAutoSlitIsPresent, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["idx","slit",None])
		self.ShamrockAutoSlitReset=wrapper(lib.ShamrockAutoSlitReset, [ctypes.c_int32,ctypes.c_int32], ["idx","slit"])
		self.ShamrockGetAutoSlitWidth=wrapper(lib.ShamrockGetAutoSlitWidth, [ctypes.c_int32,ctypes.c_int32,ctypes.c_float], ["idx","slit",None])
		self.ShamrockSetAutoSlitWidth=wrapper(lib.ShamrockSetAutoSlitWidth, [ctypes.c_int32,ctypes.c_int32,ctypes.c_float], ["idx","slit","width"])

		self.ShamrockShutterIsPresent=wrapper(lib.ShamrockShutterIsPresent, [ctypes.c_int32,ctypes.c_int32], ["idx",None])
		self.ShamrockIsModePossible=wrapper(lib.ShamrockIsModePossible, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["idx","mode",None])
		self.ShamrockGetShutter=wrapper(lib.ShamrockGetShutter, [ctypes.c_int32,ctypes.c_int32], ["idx",None])
		self.ShamrockSetShutter=wrapper(lib.ShamrockSetShutter, [ctypes.c_int32,ctypes.c_int32], ["idx","shutter"])

		self.ShamrockFilterIsPresent=wrapper(lib.ShamrockFilterIsPresent, [ctypes.c_int32,ctypes.c_int32], ["idx",None])
		self.ShamrockFilterReset=wrapper(lib.ShamrockFilterReset, [ctypes.c_int32], ["idx"])
		self.ShamrockGetFilter=wrapper(lib.ShamrockGetFilter, [ctypes.c_int32,ctypes.c_int32], ["idx",None])
		self.ShamrockSetFilter=wrapper(lib.ShamrockSetFilter, [ctypes.c_int32,ctypes.c_int32], ["idx","filter"])
		self.ShamrockGetFilterInfo=wrapper(lib.ShamrockGetFilterInfo, [ctypes.c_int32,ctypes.c_int32,ctypes.c_char_p], ["idx","filter",None], rvprep=[strprep], rvref=[False])
		self.ShamrockSetFilterInfo=wrapper(lib.ShamrockSetFilterInfo, [ctypes.c_int32,ctypes.c_int32,ctypes.c_char_p], ["idx","filter","info"])

		self.ShamrockFlipperMirrorIsPresent=wrapper(lib.ShamrockFlipperMirrorIsPresent, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["idx","flipper",None])
		self.ShamrockFlipperMirrorReset=wrapper(lib.ShamrockFlipperMirrorReset, [ctypes.c_int32,ctypes.c_int32], ["idx","flipper"])
		self.ShamrockGetFlipperMirror=wrapper(lib.ShamrockGetFlipperMirror, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["idx","flipper",None])
		self.ShamrockSetFlipperMirror=wrapper(lib.ShamrockSetFlipperMirror, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["idx","flipper","port"])
		self.ShamrockGetCCDLimits=wrapper(lib.ShamrockGetCCDLimits, [ctypes.c_int32,ctypes.c_int32,ctypes.c_float,ctypes.c_float], ["idx","port",None,None])
		
		self.ShamrockAccessoryIsPresent=wrapper(lib.ShamrockAccessoryIsPresent, [ctypes.c_int32,ctypes.c_int32], ["idx",None])
		self.ShamrockGetAccessoryState=wrapper(lib.ShamrockGetAccessoryState, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["idx","accessory",None])
		self.ShamrockSetAccessory=wrapper(lib.ShamrockSetAccessory, [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32], ["idx","accessory","state"])

		self.ShamrockGetPixelWidth=wrapper(lib.ShamrockGetPixelWidth, [ctypes.c_int32,ctypes.c_float], ["idx",None])
		self.ShamrockSetPixelWidth=wrapper(lib.ShamrockSetPixelWidth, [ctypes.c_int32,ctypes.c_float], ["idx","width"])
		self.ShamrockGetNumberPixels=wrapper(lib.ShamrockGetNumberPixels, [ctypes.c_int32,ctypes.c_int32], ["idx",None])
		self.ShamrockSetNumberPixels=wrapper(lib.ShamrockSetNumberPixels, [ctypes.c_int32,ctypes.c_int32], ["idx","number"])
		self.ShamrockGetCalibration=wrapper(lib.ShamrockGetCalibration, [ctypes.c_int32,c_float_p,ctypes.c_int32], ["idx",None,"number"],
			rvprep=[lambda _,n: (ctypes.c_float*n)()], rvref=[False], rvconv=[lambda v,*_: v[:]])

		self._initialized=True

	def open_handle(self, path=""):
		self._opened_handles_num+=1
		if self._opened_handles_num==1:
			self.initlib()
			self.ShamrockInitialize(path)
	def close_handle(self):
		self._opened_handles_num-=1
		if self._opened_handles_num==0:
			lib.ShamrockClose()
	@contextlib.contextmanager
	def using_handle(self):
		try:
			self.open_handle()
			yield
		finally:
			self.close_handle()



lib=ShamrockLib()