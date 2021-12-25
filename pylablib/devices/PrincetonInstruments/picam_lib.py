# pylint: disable=wrong-spelling-in-comment

from . import picam_defs
from .picam_defs import define_functions
from .picam_defs import PicamEnumeratedType, PicamValueType  # pylint: disable=unused-import

from ...core.utils import ctypes_wrap, py3
from ...core.devio.comm_backend import DeviceError
from ..utils import load_lib

import platform
import ctypes
import contextlib


class PicamError(DeviceError):
    """Generic Picam error"""
class PicamLibError(PicamError):
    """Generic Picam library error"""
    def __init__(self, func, code, lib=None):
        self.func=func
        self.code=code
        self.name=picam_defs.drPicamError.get(code,"Unknown")
        self.desc=None
        try:
            if lib is not None:
                self.desc=py3.as_str(lib.Picam_GetEnumerationString(PicamEnumeratedType.PicamEnumeratedType_Error,code))
        except PicamError:
            pass
        descstr="" if self.desc is None else ": {}".format(self.desc)
        self.msg="function '{}' raised error {}({}){}".format(func,self.code,self.name,descstr)
        super().__init__(self.msg)
def errcheck(passing=None, lib=None):
    """
    Build an error checking function.

    Return a function which checks return codes of Picam library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    if passing is None:
        passing={0}
    def errchecker(result, func, arguments):  # pylint: disable=unused-argument
        if result not in passing:
            raise PicamLibError(func.__name__,result,lib=lib)
        return result
    return errchecker



def conv_arr(*args):
    return args[0][:]
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



class PicamLib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return

        picam_path=load_lib.get_program_files_folder("Princeton Instruments/PICam/Runtime")
        error_message="The library is supplied with Princeton Instruments PICam software\n"+load_lib.par_error_message.format("picam")
        archbit=platform.architecture()[0][:2]
        lib_name="picam.dll" if archbit=="64" else "picam32.dll"
        self.lib=load_lib.load_lib(lib_name,locations=("parameter/picam",picam_path,"global"),error_message=error_message,call_conv="stdcall")
        lib=self.lib
        define_functions(lib)

        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(lib=self),default_rvals="pointer")

        #  ctypes.c_int Picam_GetVersion(ctypes.POINTER(piint) major, ctypes.POINTER(piint) minor, ctypes.POINTER(piint) distribution, ctypes.POINTER(piint) released)
        self.Picam_GetVersion=wrapper(lib.Picam_GetVersion)
        #  ctypes.c_int Picam_IsLibraryInitialized(ctypes.POINTER(pibln) inited)
        self.Picam_IsLibraryInitialized=wrapper(lib.Picam_IsLibraryInitialized)
        #  ctypes.c_int Picam_InitializeLibrary()
        self.Picam_InitializeLibrary=wrapper(lib.Picam_InitializeLibrary)
        #  ctypes.c_int Picam_UninitializeLibrary()
        self.Picam_UninitializeLibrary=wrapper(lib.Picam_UninitializeLibrary)

        #  ctypes.c_int Picam_DestroyString(ctypes.c_char_p s)
        lib.Picam_DestroyString.argtypes=[ctypes.c_void_p]
        self.Picam_DestroyString=wrapper(lib.Picam_DestroyString)
        #  ctypes.c_int Picam_GetEnumerationString(ctypes.c_int type, piint value, ctypes.POINTER(ctypes.c_char_p) s)
        lib.Picam_GetEnumerationString.argtypes=lib.Picam_GetEnumerationString.argtypes[:2]+[ctypes.POINTER(ctypes.c_void_p)]
        self.Picam_GetEnumerationString_lib=wrapper.wrap_annotated(lib.Picam_GetEnumerationString)
        
        #  ctypes.c_int Picam_DestroyCameraIDs(ctypes.POINTER(PicamCameraID) id_array)
        self.Picam_DestroyCameraIDs=wrapper(lib.Picam_DestroyCameraIDs, rvals=[])
        #  ctypes.c_int Picam_GetAvailableCameraIDs(ctypes.POINTER(ctypes.POINTER(PicamCameraID)) id_array, ctypes.POINTER(piint) id_count)
        # self.Picam_GetAvailableCameraIDs_lib=wrapper(lib.Picam_GetAvailableCameraIDs)
        self.Picam_GetAvailableCameraIDs_lib=wrapper(lib.Picam_GetAvailableCameraIDs)
        #  ctypes.c_int Picam_GetUnavailableCameraIDs(ctypes.POINTER(ctypes.POINTER(PicamCameraID)) id_array, ctypes.POINTER(piint) id_count)
        self.Picam_GetUnavailableCameraIDs_lib=wrapper(lib.Picam_GetUnavailableCameraIDs)
        #  ctypes.c_int Picam_IsCameraIDConnected(ctypes.POINTER(PicamCameraID) id, ctypes.POINTER(pibln) connected)
        self.Picam_IsCameraIDConnected=wrapper(lib.Picam_IsCameraIDConnected, rvals=["connected"])
        #  ctypes.c_int Picam_IsCameraIDOpenElsewhere(ctypes.POINTER(PicamCameraID) id, ctypes.POINTER(pibln) open_elsewhere)
        self.Picam_IsCameraIDOpenElsewhere=wrapper(lib.Picam_IsCameraIDOpenElsewhere, rvals=["open_elsewhere"])

        #  ctypes.c_int Picam_DestroyHandles(ctypes.POINTER(PicamHandle) handle_array)
        self.Picam_DestroyHandles=wrapper(lib.Picam_DestroyHandles, rvals=[])
        #  ctypes.c_int Picam_OpenFirstCamera(ctypes.POINTER(PicamHandle) camera)
        self.Picam_OpenFirstCamera=wrapper(lib.Picam_OpenFirstCamera)
        #  ctypes.c_int Picam_OpenCamera(ctypes.POINTER(PicamCameraID) id, ctypes.POINTER(PicamHandle) camera)
        self.Picam_OpenCamera=wrapper(lib.Picam_OpenCamera, rvals=["camera"])
        #  ctypes.c_int Picam_CloseCamera(PicamHandle camera)
        self.Picam_CloseCamera=wrapper(lib.Picam_CloseCamera)
        #  ctypes.c_int Picam_GetOpenCameras(ctypes.POINTER(ctypes.POINTER(PicamHandle)) camera_array, ctypes.POINTER(piint) camera_count)
        self.Picam_GetOpenCameras_lib=wrapper(lib.Picam_GetOpenCameras)
        #  ctypes.c_int Picam_IsCameraConnected(PicamHandle camera, ctypes.POINTER(pibln) connected)
        self.Picam_IsCameraConnected=wrapper(lib.Picam_IsCameraConnected, rvals=["connected"])
        #  ctypes.c_int Picam_IsCameraFaulted(PicamHandle camera, ctypes.POINTER(pibln) faulted)
        self.Picam_IsCameraFaulted=wrapper(lib.Picam_IsCameraFaulted, rvals=["faulted"])
        #  ctypes.c_int Picam_GetCameraID(PicamHandle camera, ctypes.POINTER(PicamCameraID) id)
        self.Picam_GetCameraID_lib=wrapper(lib.Picam_GetCameraID)
        self.Picam_GetCameraID=wrapper(lib.Picam_GetCameraID,
            rconv={"id":picam_defs.CPicamCameraID.tup_struct})

        #  ctypes.c_int PicamAdvanced_OpenCameraDevice(ctypes.POINTER(PicamCameraID) id, ctypes.POINTER(PicamHandle) device)
        self.PicamAdvanced_OpenCameraDevice=wrapper(lib.PicamAdvanced_OpenCameraDevice)
        #  ctypes.c_int PicamAdvanced_CloseCameraDevice(PicamHandle device)
        self.PicamAdvanced_CloseCameraDevice=wrapper(lib.PicamAdvanced_CloseCameraDevice)
        #  ctypes.c_int PicamAdvanced_GetOpenCameraDevices(ctypes.POINTER(ctypes.POINTER(PicamHandle)) device_array, ctypes.POINTER(piint) device_count)
        self.PicamAdvanced_GetOpenCameraDevices=wrapper(lib.PicamAdvanced_GetOpenCameraDevices)
        #  ctypes.c_int PicamAdvanced_GetCameraModel(PicamHandle camera, ctypes.POINTER(PicamHandle) model)
        self.PicamAdvanced_GetCameraModel=wrapper(lib.PicamAdvanced_GetCameraModel)
        #  ctypes.c_int PicamAdvanced_GetCameraDevice(PicamHandle camera, ctypes.POINTER(PicamHandle) device)
        self.PicamAdvanced_GetCameraDevice=wrapper(lib.PicamAdvanced_GetCameraDevice)
        
        #  ctypes.c_int Picam_DestroyFirmwareDetails(ctypes.POINTER(PicamFirmwareDetail) firmware_array)
        self.Picam_DestroyFirmwareDetails=wrapper(lib.Picam_DestroyFirmwareDetails, rvals=[])
        #  ctypes.c_int Picam_GetFirmwareDetails(ctypes.POINTER(PicamCameraID) id, ctypes.POINTER(ctypes.POINTER(PicamFirmwareDetail)) firmware_array, ctypes.POINTER(piint) firmware_count)
        self.Picam_GetFirmwareDetails_lib=wrapper(lib.Picam_GetFirmwareDetails, rvals=["firmware_array","firmware_count"])
        
        #  ctypes.c_int Picam_DestroyParameters(ctypes.POINTER(ctypes.c_int) parameter_array)
        self.Picam_DestroyParameters=wrapper(lib.Picam_DestroyParameters, rvals=[])
        #  ctypes.c_int Picam_GetParameters(PicamHandle camera_or_accessory, ctypes.POINTER(ctypes.POINTER(ctypes.c_int)) parameter_array, ctypes.POINTER(piint) parameter_count)
        self.Picam_GetParameters_lib=wrapper(lib.Picam_GetParameters)
        #  ctypes.c_int Picam_RestoreParametersToDefaultValues(PicamHandle camera_or_accessory)
        self.Picam_RestoreParametersToDefaultValues=wrapper(lib.Picam_RestoreParametersToDefaultValues)
        #  ctypes.c_int Picam_AreParametersCommitted(PicamHandle camera_or_accessory, ctypes.POINTER(pibln) committed)
        self.Picam_AreParametersCommitted=wrapper(lib.Picam_AreParametersCommitted)
        #  ctypes.c_int Picam_CommitParameters(PicamHandle camera_or_accessory, ctypes.POINTER(ctypes.POINTER(ctypes.c_int)) failed_parameter_array, ctypes.POINTER(piint) failed_parameter_count)
        self.Picam_CommitParameters_lib=wrapper(lib.Picam_CommitParameters)

        #  ctypes.c_int Picam_GetParameterIntegerValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(piint) value)
        self.Picam_GetParameterIntegerValue=wrapper(lib.Picam_GetParameterIntegerValue)
        #  ctypes.c_int Picam_SetParameterIntegerValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, piint value)
        self.Picam_SetParameterIntegerValue=wrapper(lib.Picam_SetParameterIntegerValue)
        #  ctypes.c_int Picam_CanSetParameterIntegerValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, piint value, ctypes.POINTER(pibln) settable)
        self.Picam_CanSetParameterIntegerValue=wrapper(lib.Picam_CanSetParameterIntegerValue)
        #  ctypes.c_int Picam_GetParameterIntegerDefaultValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(piint) value)
        self.Picam_GetParameterIntegerDefaultValue=wrapper(lib.Picam_GetParameterIntegerDefaultValue)
        #  ctypes.c_int Picam_SetParameterIntegerValueOnline(PicamHandle camera, ctypes.c_int parameter, piint value)
        self.Picam_SetParameterIntegerValueOnline=wrapper(lib.Picam_SetParameterIntegerValueOnline)
        #  ctypes.c_int Picam_ReadParameterIntegerValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(piint) value)
        self.Picam_ReadParameterIntegerValue=wrapper(lib.Picam_ReadParameterIntegerValue)
        
        #  ctypes.c_int Picam_GetParameterLargeIntegerValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(pi64s) value)
        self.Picam_GetParameterLargeIntegerValue=wrapper(lib.Picam_GetParameterLargeIntegerValue)
        #  ctypes.c_int Picam_SetParameterLargeIntegerValue(PicamHandle camera, ctypes.c_int parameter, pi64s value)
        self.Picam_SetParameterLargeIntegerValue=wrapper(lib.Picam_SetParameterLargeIntegerValue)
        #  ctypes.c_int Picam_CanSetParameterLargeIntegerValue(PicamHandle camera, ctypes.c_int parameter, pi64s value, ctypes.POINTER(pibln) settable)
        self.Picam_CanSetParameterLargeIntegerValue=wrapper(lib.Picam_CanSetParameterLargeIntegerValue)
        #  ctypes.c_int Picam_GetParameterLargeIntegerDefaultValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(pi64s) value)
        self.Picam_GetParameterLargeIntegerDefaultValue=wrapper(lib.Picam_GetParameterLargeIntegerDefaultValue)
        
        #  ctypes.c_int Picam_GetParameterFloatingPointValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(piflt) value)
        self.Picam_GetParameterFloatingPointValue=wrapper(lib.Picam_GetParameterFloatingPointValue)
        #  ctypes.c_int Picam_SetParameterFloatingPointValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, piflt value)
        self.Picam_SetParameterFloatingPointValue=wrapper(lib.Picam_SetParameterFloatingPointValue)
        #  ctypes.c_int Picam_CanSetParameterFloatingPointValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, piflt value, ctypes.POINTER(pibln) settable)
        self.Picam_CanSetParameterFloatingPointValue=wrapper(lib.Picam_CanSetParameterFloatingPointValue)
        #  ctypes.c_int Picam_GetParameterFloatingPointDefaultValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(piflt) value)
        self.Picam_GetParameterFloatingPointDefaultValue=wrapper(lib.Picam_GetParameterFloatingPointDefaultValue)
        #  ctypes.c_int Picam_SetParameterFloatingPointValueOnline(PicamHandle camera, ctypes.c_int parameter, piflt value)
        self.Picam_SetParameterFloatingPointValueOnline=wrapper(lib.Picam_SetParameterFloatingPointValueOnline)
        #  ctypes.c_int Picam_ReadParameterFloatingPointValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(piflt) value)
        self.Picam_ReadParameterFloatingPointValue=wrapper(lib.Picam_ReadParameterFloatingPointValue)
        
        #  ctypes.c_int Picam_CanSetParameterOnline(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(pibln) onlineable)
        self.Picam_CanSetParameterOnline=wrapper(lib.Picam_CanSetParameterOnline)
        #  ctypes.c_int Picam_CanReadParameter(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(pibln) readable)
        self.Picam_CanReadParameter=wrapper(lib.Picam_CanReadParameter)
        #  ctypes.c_int Picam_DoesParameterExist(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(pibln) exists)
        self.Picam_DoesParameterExist=wrapper(lib.Picam_DoesParameterExist)
        #  ctypes.c_int Picam_IsParameterRelevant(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(pibln) relevant)
        self.Picam_IsParameterRelevant=wrapper(lib.Picam_IsParameterRelevant)
        #  ctypes.c_int Picam_GetParameterValueType(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(ctypes.c_int) type)
        self.Picam_GetParameterValueType=wrapper(lib.Picam_GetParameterValueType)
        #  ctypes.c_int Picam_GetParameterEnumeratedType(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(ctypes.c_int) type)
        self.Picam_GetParameterEnumeratedType=wrapper(lib.Picam_GetParameterEnumeratedType)
        #  ctypes.c_int Picam_GetParameterValueAccess(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(ctypes.c_int) access)
        self.Picam_GetParameterValueAccess=wrapper(lib.Picam_GetParameterValueAccess)
        
        #  ctypes.c_int Picam_DestroyRois(ctypes.POINTER(PicamRois) rois)
        self.Picam_DestroyRois=wrapper(lib.Picam_DestroyRois, rvals=[])
        #  ctypes.c_int Picam_GetParameterRoisValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamRois)) value)
        self.Picam_GetParameterRoisValue_lib=wrapper(lib.Picam_GetParameterRoisValue)
        #  ctypes.c_int Picam_SetParameterRoisValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(PicamRois) value)
        self.Picam_SetParameterRoisValue_lib=wrapper(lib.Picam_SetParameterRoisValue, rvals=[])
        #  ctypes.c_int Picam_CanSetParameterRoisValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(PicamRois) value, ctypes.POINTER(pibln) settable)
        self.Picam_CanSetParameterRoisValue_lib=wrapper(lib.Picam_CanSetParameterRoisValue, rvals=["settable"])
        #  ctypes.c_int Picam_GetParameterRoisDefaultValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamRois)) value)
        self.Picam_GetParameterRoisDefaultValue_lib=wrapper(lib.Picam_GetParameterRoisDefaultValue)
        
        #  ctypes.c_int Picam_GetParameterConstraintType(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(ctypes.c_int) type)
        self.Picam_GetParameterConstraintType=wrapper(lib.Picam_GetParameterConstraintType)
        #  ctypes.c_int Picam_DestroyCollectionConstraints(ctypes.POINTER(PicamCollectionConstraint) constraint_array)
        self.Picam_DestroyCollectionConstraints=wrapper(lib.Picam_DestroyCollectionConstraints, rvals=[])
        #  ctypes.c_int Picam_GetParameterCollectionConstraint(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.c_int category, ctypes.POINTER(ctypes.POINTER(PicamCollectionConstraint)) constraint)
        self.Picam_GetParameterCollectionConstraint_lib=wrapper(lib.Picam_GetParameterCollectionConstraint)
        #  ctypes.c_int Picam_DestroyRangeConstraints(ctypes.POINTER(PicamRangeConstraint) constraint_array)
        self.Picam_DestroyRangeConstraints=wrapper(lib.Picam_DestroyRangeConstraints, rvals=[])
        #  ctypes.c_int Picam_GetParameterRangeConstraint(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.c_int category, ctypes.POINTER(ctypes.POINTER(PicamRangeConstraint)) constraint)
        self.Picam_GetParameterRangeConstraint_lib=wrapper(lib.Picam_GetParameterRangeConstraint)
        #  ctypes.c_int Picam_DestroyRoisConstraints(ctypes.POINTER(PicamRoisConstraint) constraint_array)
        self.Picam_DestroyRoisConstraints=wrapper(lib.Picam_DestroyRoisConstraints, rvals=[])
        #  ctypes.c_int Picam_GetParameterRoisConstraint(PicamHandle camera, ctypes.c_int parameter, ctypes.c_int category, ctypes.POINTER(ctypes.POINTER(PicamRoisConstraint)) constraint)
        self.Picam_GetParameterRoisConstraint_lib=wrapper(lib.Picam_GetParameterRoisConstraint)
        
        #  ctypes.c_int Picam_StartAcquisition(PicamHandle camera)
        self.Picam_StartAcquisition=wrapper(lib.Picam_StartAcquisition)
        #  ctypes.c_int Picam_StopAcquisition(PicamHandle camera)
        self.Picam_StopAcquisition=wrapper(lib.Picam_StopAcquisition)
        #  ctypes.c_int Picam_IsAcquisitionRunning(PicamHandle camera, ctypes.POINTER(pibln) running)
        self.Picam_IsAcquisitionRunning=wrapper(lib.Picam_IsAcquisitionRunning)
        #  ctypes.c_int Picam_WaitForAcquisitionUpdate(PicamHandle camera, piint readout_time_out, ctypes.POINTER(PicamAvailableData) available, ctypes.POINTER(PicamAcquisitionStatus) status)
        self.Picam_WaitForAcquisitionUpdate=wrapper(lib.Picam_WaitForAcquisitionUpdate,
            rconv={"available": picam_defs.CPicamAvailableData.tup_struct, "status": picam_defs.CPicamAcquisitionStatus.tup_struct})
        #  ctypes.c_int Picam_Acquire(PicamHandle camera, pi64s readout_count, piint readout_time_out, ctypes.POINTER(PicamAvailableData) available, ctypes.POINTER(ctypes.c_int) errors)
        self.Picam_Acquire=wrapper(lib.Picam_Acquire,
            rconv={"available": picam_defs.CPicamAvailableData.tup_struct})
        #  ctypes.c_int PicamAdvanced_GetAcquisitionBuffer(PicamHandle device, ctypes.POINTER(PicamAcquisitionBuffer) buffer)
        self.PicamAdvanced_GetAcquisitionBuffer=wrapper(lib.PicamAdvanced_GetAcquisitionBuffer,
            rconv={"buffer": picam_defs.CPicamAcquisitionBuffer.tup_struct})
        #  ctypes.c_int PicamAdvanced_SetAcquisitionBuffer(PicamHandle device, ctypes.POINTER(PicamAcquisitionBuffer) buffer)
        self.PicamAdvanced_SetAcquisitionBuffer_lib=wrapper(lib.PicamAdvanced_SetAcquisitionBuffer, rvals=[])
        #  ctypes.c_int PicamAdvanced_HasAcquisitionBufferOverrun(PicamHandle device, ctypes.POINTER(pibln) overran)
        self.PicamAdvanced_HasAcquisitionBufferOverrun=wrapper(lib.PicamAdvanced_HasAcquisitionBufferOverrun)
        #  ctypes.c_int PicamAdvanced_CanClearReadoutCountOnline(PicamHandle device, ctypes.POINTER(pibln) clearable)
        self.PicamAdvanced_CanClearReadoutCountOnline=wrapper(lib.PicamAdvanced_CanClearReadoutCountOnline)
        #  ctypes.c_int PicamAdvanced_ClearReadoutCountOnline(PicamHandle device, ctypes.POINTER(pibln) cleared)
        self.PicamAdvanced_ClearReadoutCountOnline=wrapper(lib.PicamAdvanced_ClearReadoutCountOnline)
        
        return



    def destroy_convert(self, arr, count, conv, destroy):
        vals=[conv(arr[i]) for i in range(count)]
        destroy(arr)
        return vals

    def Picam_GetEnumerationString(self, stype, value):
        ptr=self.Picam_GetEnumerationString_lib(stype,value)
        res=ctypes.string_at(ptr)
        self.Picam_DestroyString(ptr)
        return res
    def Picam_GetAvailableCameraIDs(self):
        return self.destroy_convert(*self.Picam_GetAvailableCameraIDs_lib(),conv=picam_defs.CPicamCameraID.tup_struct,destroy=self.Picam_DestroyCameraIDs)
    def Picam_GetUnavailableCameraIDs(self):
        return self.destroy_convert(*self.Picam_GetUnavailableCameraIDs_lib(),conv=picam_defs.CPicamCameraID.tup_struct,destroy=self.Picam_DestroyCameraIDs)
    
    @contextlib.contextmanager
    def _get_id_by_serial(self, serial_number):
        cams,camn=self.Picam_GetAvailableCameraIDs_lib()
        found=None
        for i in range(camn):
            if picam_defs.CPicamCameraID.tup_struct(cams[i]).serial_number==serial_number:
                found=cams[i]
                break
        try:
            yield found
        finally:
            self.Picam_DestroyCameraIDs(cams)
    def Picam_OpenCamera_BySerial(self, serial_number):
        with self._get_id_by_serial(serial_number) as cid:
            return self.Picam_OpenCamera(cid) if cid is not None else None
    def Picam_GetOpenCameras(self):
        return self.destroy_convert(*self.Picam_GetOpenCameras_lib(),conv=picam_defs.PicamHandle,destroy=self.Picam_DestroyHandles)
    def Picam_GetFirmwareDetails(self, camid):
        return self.destroy_convert(*self.Picam_GetFirmwareDetails_lib(camid),conv=picam_defs.CPicamFirmwareDetail.tup_struct,destroy=self.Picam_DestroyFirmwareDetails)
    def Picam_GetFirmwareDetails_ByHandle(self, camera):
        return self.Picam_GetFirmwareDetails(ctypes.pointer(self.Picam_GetCameraID_lib(camera)))
    def Picam_GetFirmwareDetails_BySerial(self, serial_number):
        with self._get_id_by_serial(serial_number) as cid:
            return self.Picam_GetFirmwareDetails(cid) if cid is not None else None

    def Picam_GetParameters(self, camera):
        return self.destroy_convert(*self.Picam_GetParameters_lib(camera),conv=lambda v:v,destroy=self.Picam_DestroyParameters)
    def Picam_CommitParameters(self, camera):
        return self.destroy_convert(*self.Picam_CommitParameters_lib(camera),conv=lambda v:v,destroy=self.Picam_DestroyParameters)
    
    def _parse_rois(self, rois):
        arr,cnt=picam_defs.CPicamRois.tup_struct(rois)
        return [picam_defs.CPicamRoi.tup_struct(arr[i]) for i in range(cnt)]
    _roi_names=list(zip(*picam_defs.PicamRoi._fields_))[0]
    def _build_single_roi(self, kwargs):
        if isinstance(kwargs,tuple):
            kwargs=dict(zip(self._roi_names,kwargs))
        return picam_defs.CPicamRoi.prep_struct_args(**kwargs)
    def _build_rois(self, argsets):
        rois_list=[self._build_single_roi(kwargs) for kwargs in argsets]
        rois_array=(picam_defs.PicamRoi*len(rois_list))()
        for i,r in enumerate(rois_list):
            rois_array[i]=r
        rois=picam_defs.CPicamRois.prep_struct_args(roi_array=rois_array,roi_count=len(rois_list))
        return rois,rois_array

    def Picam_GetParameterRoisValue(self, camera, parameter):
        return self.destroy_convert(self.Picam_GetParameterRoisValue_lib(camera,parameter),1,conv=self._parse_rois,destroy=self.Picam_DestroyRois)[0]
    def Picam_GetParameterRoisDefaultValue(self, camera, parameter):
        return self.destroy_convert(self.Picam_GetParameterRoisDefaultValue_lib(camera,parameter),1,conv=self._parse_rois,destroy=self.Picam_DestroyRois)[0]
    def Picam_SetParameterRoisValue(self, camera, parameter, argsets):
        rois,rois_array=self._build_rois(argsets)  # pylint: disable=unused-variable
        self.Picam_SetParameterRoisValue_lib(camera,parameter,rois)
    def Picam_CanSetParameterRoisValue(self, camera, parameter, argsets):
        rois,rois_array=self._build_rois(argsets)  # pylint: disable=unused-variable
        self.Picam_CanSetParameterRoisValue_lib(camera,parameter,rois)

    def _parse_collection_constrains(self, cons):
        tcons=picam_defs.CPicamCollectionConstraint.tup_struct(cons)
        values=[tcons.values_array[i] for i in range(tcons.values_count)]
        return tcons[:-2]+(values,)
    def Picam_GetParameterCollectionConstraint(self, camera, parameter, category):
        return self.destroy_convert(self.Picam_GetParameterCollectionConstraint_lib(camera,parameter,category),1,
            conv=self._parse_collection_constrains,destroy=self.Picam_DestroyCollectionConstraints)[0]
    def _parse_range_constrains(self, cons):
        tcons=picam_defs.CPicamRangeConstraint.tup_struct(cons)
        excluded=[tcons.excluded_values_array[i] for i in range(tcons.excluded_values_count)]
        outlying=[tcons.outlying_values_array[i] for i in range(tcons.outlying_values_count)]
        return tcons[:-4]+(excluded,outlying)
    def Picam_GetParameterRangeConstraint(self, camera, parameter, category):
        return self.destroy_convert(self.Picam_GetParameterRangeConstraint_lib(camera,parameter,category),1,
            conv=self._parse_range_constrains,destroy=self.Picam_DestroyRangeConstraints)[0]
    def _parse_roi_constrains(self, cons):
        tcons=picam_defs.CPicamRoisConstraint.tup_struct(cons)
        xcons=self._parse_range_constrains(tcons.x_constraint)
        wcons=self._parse_range_constrains(tcons.width_constraint)
        xbins=[tcons.x_binning_limits_array[i] for i in range(tcons.x_binning_limits_count)]
        ycons=self._parse_range_constrains(tcons.y_constraint)
        hcons=self._parse_range_constrains(tcons.height_constraint)
        ybins=[tcons.y_binning_limits_array[i] for i in range(tcons.y_binning_limits_count)]
        return tcons[:5]+(xcons,wcons,xbins,ycons,hcons,ybins)
    def Picam_GetParameterRoisConstraint(self, camera, parameter, category):
        return self.destroy_convert(self.Picam_GetParameterRoisConstraint_lib(camera,parameter,category),1,
            conv=self._parse_roi_constrains,destroy=self.Picam_DestroyRoisConstraints)[0]

    def PicamAdvanced_SetAcquisitionBuffer(self, camera, buff, size):
        buffdesc=picam_defs.CPicamAcquisitionBuffer.prep_struct_args(memory=buff,memory_size=size)
        self.PicamAdvanced_SetAcquisitionBuffer_lib(camera,buffdesc)
        
        


wlib=PicamLib()