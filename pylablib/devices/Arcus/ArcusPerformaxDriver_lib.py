# pylint: disable=wrong-spelling-in-comment

from ...core.utils import ctypes_wrap
from ...core.devio.comm_backend import DeviceError
from .ArcusPerformaxDriver_defs import define_functions
from ..utils import load_lib


class ArcusError(DeviceError):
    """Generic Arcus error"""
class ArcusPerformaxLibError(ArcusError):
    """Generic Arcus Performax library error"""
    def __init__(self, func, arguments):
        self.func=func
        self.arguments=arguments
        self.msg="function '{}' return an error".format(func)
        ArcusError.__init__(self,self.msg)
def errchecker(result, func, arguments):
    if not result:
        raise ArcusPerformaxLibError(func.__name__,arguments)
    return result


class ArcusPerformaxLib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return
        error_message=( "The library is can be downloaded on the manufacturer's website;\n"+
                        load_lib.par_error_message.format("arcus_performax")+
                        "\nAdditional required libraries: SiUSBXp.dll (distributed together with the main library)")
        self.lib=load_lib.load_lib("PerformaxCom.dll",locations=("parameter/arcus_performax","global"),error_message=error_message,depends=["SiUSBXp.dll"],call_conv="cdecl")
        lib=self.lib
        define_functions(lib)

        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errchecker,pointer_byref=True)
        strlen=256
        strprep=ctypes_wrap.strprep(strlen)

        #  AR_BOOL fnPerformaxComGetNumDevices(ctypes.POINTER(AR_DWORD) numDevices)
        self.fnPerformaxComGetNumDevices=wrapper(lib.fnPerformaxComGetNumDevices,rvals=["numDevices"])
        #  AR_BOOL fnPerformaxComGetProductString(AR_DWORD dwNumDevice, ctypes.c_void_p lpDeviceString, AR_DWORD dwOptions)
        self.fnPerformaxComGetProductString=wrapper(lib.fnPerformaxComGetProductString,rvals=["lpDeviceString"],byref=None,
            argprep={"lpDeviceString":strprep})
        
        #  AR_BOOL fnPerformaxComOpen(AR_DWORD dwDeviceNum, ctypes.POINTER(AR_HANDLE) pHandle)
        self.fnPerformaxComOpen=wrapper(lib.fnPerformaxComOpen,rvals=["pHandle"])
        #  AR_BOOL fnPerformaxComClose(AR_HANDLE pHandle)
        self.fnPerformaxComClose=wrapper(lib.fnPerformaxComClose)
        
        #  AR_BOOL fnPerformaxComSetTimeouts(AR_DWORD dwReadTimeout, AR_DWORD dwWriteTimeout)
        self.fnPerformaxComSetTimeouts=wrapper(lib.fnPerformaxComSetTimeouts)
        #  AR_BOOL fnPerformaxComSendRecv(AR_HANDLE Handle, ctypes.c_void_p wBuffer, AR_DWORD dwNumBytesToWrite, AR_DWORD dwNumBytesToRead, ctypes.c_void_p rBuffer)
        self.fnPerformaxComSendRecv=wrapper(lib.fnPerformaxComSendRecv,args=["Handle","wBuffer"],rvals=["rBuffer"],byref=None,
            argprep={"dwNumBytesToWrite":(lambda Handle,wBuffer: len(wBuffer)),"rBuffer":strprep,"dwNumBytesToRead":strlen})
        #  AR_BOOL fnPerformaxComFlush(AR_HANDLE Handle)
        self.fnPerformaxComFlush=wrapper(lib.fnPerformaxComFlush)
        
        self._initialized=True



lib=ArcusPerformaxLib()