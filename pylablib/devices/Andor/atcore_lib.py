# pylint: disable=wrong-spelling-in-comment

from . import atcore_defs
from .atcore_defs import AT_ERR, drAT_ERR
from .atcore_defs import define_functions
from .atcore_features import feature_types  # pylint: disable=unused-import
from .base import AndorError

from ...core.utils import ctypes_wrap
from ..utils import load_lib

import ctypes
import warnings
import numpy as np



class AndorSDK3LibError(AndorError):
    """Generic Andor SDK3 library error"""
    def __init__(self, func, code):
        self.func=func
        self.code=code
        self.name=drAT_ERR.get(self.code,"UNKNOWN")
        msg="function '{}' raised error {}({})".format(func,code,self.name)
        AndorError.__init__(self,msg)
def errcheck(passing=None):
    """
    Build an error checking function.

    Return a function which checks return codes of Andor SDK3 library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    passing=set(passing) if passing is not None else set()
    passing.add(0) # always allow success
    def errchecker(result, func, arguments):  # pylint: disable=unused-argument
        if result not in passing:
            raise AndorSDK3LibError(func.__name__,result)
        return result
    return errchecker



AT_pWC=ctypes.c_wchar_p
AT_H=atcore_defs.AT_H

class AndorSDK3Lib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return

        solis_path=load_lib.get_program_files_folder("Andor SOLIS")
        sdk3_path=load_lib.get_program_files_folder("Andor SDK3")
        error_message=( "The library is automatically supplied with Andor Solis software or Andor SDK3 software;\n"+
                        load_lib.par_error_message.format("andor_sdk3")+
                        "\nAdditional required libraries: atblkbx.dll, atcl_bitflow.dll, atdevapogee.dll, atdevregcam.dll, atusb_libusb.dll, atusb_libusb10.dll (distributed together with the main library)")
        self.lib=load_lib.load_lib("atcore.dll",locations=("parameter/andor_sdk3",solis_path,sdk3_path,"global"),error_message=error_message,locally=True,call_conv="stdcall")
        lib=self.lib
        define_functions(lib)

        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck())

        #  ctypes.c_int AT_InitialiseLibrary()
        self.AT_InitialiseLibrary=wrapper(lib.AT_InitialiseLibrary)
        #  ctypes.c_int AT_FinaliseLibrary()
        self.AT_FinaliseLibrary=wrapper(lib.AT_FinaliseLibrary)
        #  ctypes.c_int AT_Open(ctypes.c_int CameraIndex, ctypes.POINTER(AT_H) Hndl)
        self.AT_Open=wrapper(lib.AT_Open, rvals=["Hndl"])
        #  ctypes.c_int AT_Close(AT_H Hndl)
        self.AT_Close=wrapper(lib.AT_Close)


        #  ctypes.c_int AT_IsImplemented(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(AT_BOOL) Implemented)
        self.AT_IsImplemented=wrapper(lib.AT_IsImplemented, rvals=["Implemented"])
        #  ctypes.c_int AT_IsReadable(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(AT_BOOL) Readable)
        self.AT_IsReadable=wrapper(lib.AT_IsReadable, rvals=["Readable"])
        #  ctypes.c_int AT_IsWritable(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(AT_BOOL) Writable)
        self.AT_IsWritable=wrapper(lib.AT_IsWritable, rvals=["Writable"])
        #  ctypes.c_int AT_IsReadOnly(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(AT_BOOL) ReadOnly)
        self.AT_IsReadOnly=wrapper(lib.AT_IsReadOnly, rvals=["ReadOnly"])

        #  ctypes.c_int AT_SetInt(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, AT_64 Value)
        self.AT_SetInt=wrapper(lib.AT_SetInt)
        #  ctypes.c_int AT_GetInt(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(AT_64) Value)
        self.AT_GetInt=wrapper(lib.AT_GetInt, rvals=["Value"])
        #  ctypes.c_int AT_GetIntMax(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(AT_64) MaxValue)
        self.AT_GetIntMax=wrapper(lib.AT_GetIntMax, rvals=["MaxValue"])
        #  ctypes.c_int AT_GetIntMin(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(AT_64) MinValue)
        self.AT_GetIntMin=wrapper(lib.AT_GetIntMin, rvals=["MinValue"])

        #  ctypes.c_int AT_SetFloat(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.c_double Value)
        self.AT_SetFloat=wrapper(lib.AT_SetFloat)
        #  ctypes.c_int AT_GetFloat(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(ctypes.c_double) Value)
        self.AT_GetFloat=wrapper(lib.AT_GetFloat, rvals=["Value"])
        #  ctypes.c_int AT_GetFloatMax(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(ctypes.c_double) MaxValue)
        self.AT_GetFloatMax=wrapper(lib.AT_GetFloatMax, rvals=["MaxValue"])
        #  ctypes.c_int AT_GetFloatMin(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(ctypes.c_double) MinValue)
        self.AT_GetFloatMin=wrapper(lib.AT_GetFloatMin, rvals=["MinValue"])

        #  ctypes.c_int AT_SetBool(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, AT_BOOL Value)
        self.AT_SetBool=wrapper(lib.AT_SetBool)
        #  ctypes.c_int AT_GetBool(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(AT_BOOL) Value)
        self.AT_GetBool=wrapper(lib.AT_GetBool, rvals=["Value"])

        #  ctypes.c_int AT_SetEnumIndex(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.c_int Value)
        self.AT_SetEnumIndex=wrapper(lib.AT_SetEnumIndex)
        #  ctypes.c_int AT_SetEnumString(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(AT_WC) String)
        self.AT_SetEnumString=wrapper(lib.AT_SetEnumString)
        #  ctypes.c_int AT_GetEnumIndex(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(ctypes.c_int) Value)
        self.AT_GetEnumIndex=wrapper(lib.AT_GetEnumIndex, rvals=["Value"])
        #  ctypes.c_int AT_GetEnumCount(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(ctypes.c_int) Count)
        self.AT_GetEnumCount=wrapper(lib.AT_GetEnumCount, rvals=["Count"])
        #  ctypes.c_int AT_IsEnumIndexAvailable(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.c_int Index, ctypes.POINTER(AT_BOOL) Available)
        self.AT_IsEnumIndexAvailable=wrapper(lib.AT_IsEnumIndexAvailable, rvals=["Available"])
        #  ctypes.c_int AT_IsEnumIndexImplemented(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.c_int Index, ctypes.POINTER(AT_BOOL) Implemented)
        self.AT_IsEnumIndexImplemented=wrapper(lib.AT_IsEnumIndexImplemented, rvals=["Implemented"])
        #  ctypes.c_int AT_GetEnumStringByIndex(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.c_int Index, ctypes.POINTER(AT_WC) String, ctypes.c_int StringLength)
        self.AT_GetEnumStringByIndex=wrapper(lib.AT_GetEnumStringByIndex, args=["Hndl","Feature","Index","StringLength"],
            rvals=["String"], argprep={"String":lambda StringLength: ctypes_wrap.strprep(StringLength,ctype=AT_pWC,unicode=True)()}, byref=[])

        #  ctypes.c_int AT_SetString(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(AT_WC) String)
        self.AT_SetString=wrapper(lib.AT_SetString)
        #  ctypes.c_int AT_GetString(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(AT_WC) String, ctypes.c_int StringLength)
        self.AT_GetString=wrapper(lib.AT_GetString, args=["Hndl","Feature","StringLength"],
            rvals=["String"], argprep={"String":lambda StringLength: ctypes_wrap.strprep(StringLength,ctype=AT_pWC,unicode=True)()}, byref=[])
        #  ctypes.c_int AT_GetStringMaxLength(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, ctypes.POINTER(ctypes.c_int) MaxStringLength)
        self.AT_GetStringMaxLength=wrapper(lib.AT_GetStringMaxLength, rvals=["MaxStringLength"])

        #  ctypes.c_int AT_Command(AT_H Hndl, ctypes.POINTER(AT_WC) Feature)
        self.AT_Command=wrapper(lib.AT_Command)

        # typedef int (AT_EXP_CONV *FeatureCallback)(AT_H Hndl, const AT_WC* Feature, void* Context);
        self.c_callback=ctypes.WINFUNCTYPE(ctypes.c_int,AT_H,AT_pWC,ctypes.c_void_p)
        #  ctypes.c_int AT_RegisterFeatureCallback(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, FeatureCallback EvCallback, ctypes.c_void_p Context)
        self.AT_RegisterFeatureCallback_lib=wrapper(lib.AT_RegisterFeatureCallback)
        #  ctypes.c_int AT_UnregisterFeatureCallback(AT_H Hndl, ctypes.POINTER(AT_WC) Feature, FeatureCallback EvCallback, ctypes.c_void_p Context)
        self.AT_UnregisterFeatureCallback_lib=wrapper(lib.AT_UnregisterFeatureCallback)

        #  ctypes.c_int AT_QueueBuffer(AT_H Hndl, ctypes.POINTER(AT_U8) Ptr, ctypes.c_int PtrSize)
        self.AT_QueueBuffer=wrapper(lib.AT_QueueBuffer)
        #  ctypes.c_int AT_WaitBuffer(AT_H Hndl, ctypes.POINTER(ctypes.POINTER(AT_U8)) Ptr, ctypes.POINTER(ctypes.c_int) PtrSize, ctypes.c_uint Timeout)
        self.AT_WaitBuffer=wrapper(lib.AT_WaitBuffer, rvals=["Ptr","PtrSize"])
        #  ctypes.c_int AT_Flush(AT_H Hndl)
        self.AT_Flush=wrapper(lib.AT_Flush)

        self._initialized=True



    def AT_RegisterFeatureCallback(self, Hndl, Feature, callback, Context=None, wrap=True):
        if wrap:
            def wrapped_callback(*args):
                try:
                    callback(*args)
                    return 0
                except: # pylint: disable=bare-except
                    return 1
            cb=self.c_callback(wrapped_callback)
        else:
            cb=self.c_callback(callback)
        self.AT_RegisterFeatureCallback_lib(Hndl,Feature,cb,Context)
        return cb
    def AT_UnregisterFeatureCallback(self, Hndl, Feature, callback, Context=None):
        self.AT_UnregisterFeatureCallback_lib(Hndl,Feature,callback,Context)

    # def allocate_buffers(self, handle, nframes, frame_size):
    #     buffs=[]
    #     for _ in range(nframes):
    #         b=ctypes.create_string_buffer(frame_size)
    #         buffs.append(b)
    #     return buffs
    def flush_buffers(self, handle):
        while True:
            try:
                self.AT_WaitBuffer(handle,0)
            except AndorSDK3LibError as e:
                if e.code in {AT_ERR.AT_ERR_TIMEDOUT,AT_ERR.AT_ERR_NODATA}:
                    break
                raise
        self.AT_Flush(handle)






NBError=ImportError
try:
    import numba as nb
    NBError=nb.errors.NumbaError
    nb_uint8_ro=nb.typeof(np.frombuffer(b"\x00",dtype="u1").reshape((1,1))) # for readonly attribute of a numpy array
    nb_width=nb.typeof(np.empty([0]).shape[0]) # pylint: disable=unsubscriptable-object
    @nb.njit(nb.uint16[:,:](nb_uint8_ro,nb_width),parallel=False)
    def read_uint12(raw_data, width):
        """
        Convert packed 12bit data (3 bytes per 2 pixels) into unpacked 16bit data (2 bytes per pixel).

        `raw_data` is a 2D numpy array with the raw frame data of dimensions ``(nrows, stride)``, where ``stride`` is the size of one row in bytes.
        `width` is the size of the resulting row in pixels; if it is 0, assumed to be maximal possible size.

        Function semantics is identical to :func:`read_uint12`, but it is implemented with Numba to speed up calculations.
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
except NBError:
    def read_uint12(raw_data, width):
        """
        Convert packed 12bit data (3 bytes per 2 pixels) into unpacked 16bit data (2 bytes per pixel).

        `raw_data` is a 2D numpy array with the raw frame data of dimensions ``(nrows, stride)``, where ``stride`` is the size of one row in bytes.
        `width` is the size of the resulting row in pixels; if it is 0, assumed to be maximal possible size.
        """
        warnings.warn("Numba is missing, so the 12-bit data unpacking is implemented via Numpy; the performance might suffer")
        data=raw_data.astype("<u2")
        fst_uint8,mid_uint8,lst_uint8=data[:,::3],data[:,1::3],data[:,2::3]
        result=np.empty(shape=(fst_uint8.shape[0],lst_uint8.shape[1]+mid_uint8.shape[1]),dtype="<u2")
        result[:,::2]=(fst_uint8[:,:mid_uint8.shape[1]]<<4)|(mid_uint8&0x0F)
        result[:,1::2]=(mid_uint8[:,:lst_uint8.shape[1]]>>4)|(lst_uint8<<4)
        return result[:,:width] if width else result

wlib=AndorSDK3Lib()