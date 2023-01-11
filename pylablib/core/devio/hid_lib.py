from ..utils import ctypes_wrap, ctypes_tools as ctt, py3
from .hid_base import HIDError, HIDLibError

import ctypes
import enum



##### Types declaration #####

USAGE=ctt.USHORT
PHIDP_PREPARSED_DATA=ctypes.c_void_p
PPHIDP_PREPARSED_DATA=ctypes.POINTER(PHIDP_PREPARSED_DATA)
HDEVINFO=ctypes.c_void_p
LPSECURITY_ATTRIBUTES=ctypes.c_void_p


class DIGCF(enum.IntEnum):
    DIGCF_DEFAULT = 0x01
    DIGCF_PRESENT = 0x02
    DIGCF_ALLCLASSES = 0x04
    DIGCF_PROFILE = 0x08
    DIGCF_DEVICEINTERFACE = 0x10

class SP_DEVINFO_DATA(ctypes.Structure):
    _fields_=[  ("cbSize",ctt.DWORD),
                ("ClassGuid",ctt.GUID),
                ("DevInst",ctt.DWORD),
                ("Reserved",ctt.ULONG_PTR) ]
PSP_DEVINFO_DATA=ctypes.POINTER(SP_DEVINFO_DATA)
class CSP_DEVINFO_DATA(ctypes_wrap.CStructWrapper):
    _struct=SP_DEVINFO_DATA
    def prep(self, struct):
        struct.cbSize=ctypes.sizeof(struct)
        return struct

class SP_DEVICE_INTERFACE_DATA(ctypes.Structure):
    _fields_=[  ("cbSize",ctt.DWORD),
                ("InterfaceClassGuid",ctt.GUID),
                ("Flags",ctt.DWORD),
                ("Reserved",ctt.ULONG_PTR) ]
PSP_DEVICE_INTERFACE_DATA=ctypes.POINTER(SP_DEVICE_INTERFACE_DATA)
class CSP_DEVICE_INTERFACE_DATA(ctypes_wrap.CStructWrapper):
    _struct=SP_DEVICE_INTERFACE_DATA
    def prep(self, struct):
        struct.cbSize=ctypes.sizeof(struct)
        return struct

_detail_data_size=4096
class SP_DEVICE_INTERFACE_DETAIL_DATA_A(ctypes.Structure):
    _fields_=[  ("cbSize",ctt.DWORD),
                ("InterfaceClassGuid",ctypes.c_char*_detail_data_size) ]
PSP_DEVICE_INTERFACE_DETAIL_DATA_A=ctypes.POINTER(SP_DEVICE_INTERFACE_DETAIL_DATA_A)
class CSP_DEVICE_INTERFACE_DETAIL_DATA_A(ctypes_wrap.CStructWrapper):
    _struct=SP_DEVICE_INTERFACE_DETAIL_DATA_A
    def prep(self, struct):
        struct.cbSize=8 if ctt.is_64bit else 5
        return struct

class HIDD_ATTRIBUTES(ctypes.Structure):
    _fields_=[  ("Size",ctt.ULONG),
                ("VendorID",ctt.USHORT),
                ("ProductID",ctt.USHORT),
                ("VersionNumber",ctt.USHORT), ]
PHIDD_ATTRIBUTES=ctypes.POINTER(HIDD_ATTRIBUTES)
class CHIDD_ATTRIBUTES(ctypes_wrap.CStructWrapper):
    _struct=HIDD_ATTRIBUTES
    def prep(self, struct):
        struct.Size=ctypes.sizeof(struct)
        return struct

class HIDP_CAPS(ctypes.Structure):
    _fields_=[  ("Usage",USAGE),
                ("UsagePage",USAGE),
                ("InputReportByteLength",ctt.USHORT),
                ("OutputReportByteLength",ctt.USHORT),
                ("FeatureReportByteLength",ctt.USHORT),
                ("Reserved",ctt.USHORT*17),
                ("NumberLinkCollectionNodes",ctt.USHORT),
                ("NumberInputButtonCaps",ctt.USHORT),
                ("NumberInputValueCaps",ctt.USHORT),
                ("NumberOutputButtonCaps",ctt.USHORT),
                ("NumberOutputValueCaps",ctt.USHORT),
                ("NumberInputDataIndices",ctt.USHORT),
                ("NumberOutputDataIndices",ctt.USHORT),
                ("NumberFeatureButtonCaps",ctt.USHORT),
                ("NumberFeatureValueCaps",ctt.USHORT),
                ("NumberFeatureDataIndices",ctt.USHORT), ]
PHIDP_CAPS=ctypes.POINTER(HIDP_CAPS)
class CHIDP_CAPS(ctypes_wrap.CStructWrapper):
    _struct=HIDP_CAPS
    _tup_exc={"Reserved"}
_hid_string_size=4093






##### Main library class #####

class HIDLib:
    def __init__(self):
        self._initialized=False
    def define_functions(self):
        try:
            self.hidlib=ctypes.windll.LoadLibrary("hid")
            self.setupapilib=ctypes.windll.LoadLibrary("setupapi")
            self.kernel32lib=ctypes.windll.LoadLibrary("kernel32")
        except OSError:
            raise HIDError("this backend is only available on Windows; could not load the required DLLs")
        ctt.decorate(self.kernel32lib.GetLastError,ctt.DWORD,[],argnames=[])
        ctt.decorate(self.kernel32lib.Sleep,None,[ctt.DWORD],argnames=["dwMilliseconds"])
        ctt.decorate(self.kernel32lib.CreateFileW,ctt.HANDLE,[ctt.LPCWSTR,ctt.DWORD,ctt.DWORD,LPSECURITY_ATTRIBUTES,ctt.DWORD,ctt.DWORD,ctt.HANDLE],
            argnames=["lpFileName","dwDesiredAccess","dwShareMode","lpSecurityAttributes","dwCreationDisposition","dwFlagsAndAttributes","hTemplateFile"])
        ctt.decorate(self.kernel32lib.CreateEventA,ctt.HANDLE,[ctt.LPSECURITY_ATTRIBUTES,ctt.BOOL,ctt.BOOL,ctt.LPCSTR],
            argnames=["lpEventAttributes","bManualReset","bInitialState","lpName"])
        ctt.decorate(self.kernel32lib.SetEvent,ctt.BOOL,[ctt.HANDLE],argnames=["hEvent"])
        ctt.decorate(self.kernel32lib.ResetEvent,ctt.BOOL,[ctt.HANDLE],argnames=["hEvent"])
        ctt.decorate(self.kernel32lib.WaitForSingleObject,ctt.DWORD,[ctt.HANDLE,ctt.DWORD],argnames=["hHandle","dwMilliseconds"])
        ctt.decorate(self.kernel32lib.WaitForMultipleObjects,ctt.DWORD,[ctt.DWORD,ctt.LPHANDLE,ctt.BOOL,ctt.DWORD],
            argnames=["nCount","lpHandles","bWaitAll","dwMilliseconds"])
        ctt.decorate(self.kernel32lib.CloseHandle,ctt.BOOL,[ctt.HANDLE],argnames=["hObject"])
        ctt.decorate(self.kernel32lib.ReadFile,ctt.BOOL,[ctt.HANDLE,ctt.LPVOID,ctt.DWORD,ctt.PDWORD,ctt.LPOVERLAPPED],
            argnames=["hFile","lpBuffer","nNumberOfBytesToRead","lpNumberOfBytesRead","lpOverlapped"])
        ctt.decorate(self.kernel32lib.WriteFile,ctt.BOOL,[ctt.HANDLE,ctt.LPVOID,ctt.DWORD,ctt.PDWORD,ctt.LPOVERLAPPED],
            argnames=["hFile","lpBuffer","nNumberOfBytesToWrite","lpNumberOfBytesWritten","lpOverlapped"])
        ctt.decorate(self.kernel32lib.CancelIo,ctt.BOOL,[ctt.HANDLE],argnames=["hFile"])
        ctt.decorate(self.kernel32lib.CancelIoEx,ctt.BOOL,[ctt.HANDLE,ctt.LPOVERLAPPED],argnames=["hFile","lpOverlapped"])
        ctt.decorate(self.kernel32lib.GetOverlappedResult,ctt.BOOL,[ctt.HANDLE,ctt.LPOVERLAPPED,ctt.LPDWORD,ctt.BOOL],
            argnames=["hFile","lpOverlapped","lpNumberOfBytesTransferred","bWait"])
        ctt.decorate(self.kernel32lib.SetCommTimeouts,ctt.BOOL,[ctt.HANDLE,ctt.LPCOMMTIMEOUTS],argnames=["hFile","lpCommTimeouts"])
        ctt.decorate(self.kernel32lib.GetCommTimeouts,ctt.BOOL,[ctt.HANDLE,ctt.LPCOMMTIMEOUTS],argnames=["hFile","lpCommTimeouts"])
        ctt.decorate(self.setupapilib.SetupDiGetClassDevsW,HDEVINFO,[ctt.LPGUID,ctt.LPCWSTR,ctt.HWND,ctt.DWORD],
            argnames=["ClassGuid","Enumerator","hwndParent","Flags"])
        ctt.decorate(self.setupapilib.SetupDiDestroyDeviceInfoList,ctt.BOOL,[HDEVINFO],argnames=["DeviceInfoSet"])
        ctt.decorate(self.setupapilib.SetupDiEnumDeviceInterfaces,ctt.BOOL,[HDEVINFO,PSP_DEVINFO_DATA,ctt.LPGUID,ctt.DWORD,PSP_DEVICE_INTERFACE_DATA],
            argnames=["DeviceInfoSet","DeviceInfoData","InterfaceClassGuid","MemberIndex","DeviceInterfaceData"])
        ctt.decorate(self.setupapilib.SetupDiGetDeviceInterfaceDetailA,ctt.BOOL,[HDEVINFO,PSP_DEVICE_INTERFACE_DATA,PSP_DEVICE_INTERFACE_DETAIL_DATA_A,ctt.DWORD,ctt.PDWORD,PSP_DEVINFO_DATA],
            argnames=["DeviceInfoSet","DeviceInterfaceData","DeviceInterfaceDetailData","DeviceInterfaceDetailDataSize","RequiredSize","DeviceInfoData"])
        ctt.decorate(self.hidlib.HidD_GetHidGuid,None,[ctt.LPGUID],argnames=["HidGuid"])
        ctt.decorate(self.hidlib.HidD_GetPreparsedData,ctt.BOOL,[ctt.HANDLE,PPHIDP_PREPARSED_DATA],argnames=["HidDeviceObject","PreparsedData"])
        ctt.decorate(self.hidlib.HidD_FreePreparsedData,ctt.BOOL,[PHIDP_PREPARSED_DATA],argnames=["PreparsedData"])
        ctt.decorate(self.hidlib.HidP_GetCaps,ctt.BOOL,[ctt.HANDLE,PHIDP_CAPS],argnames=["PreparsedData","Capabilities"])
        ctt.decorate(self.hidlib.HidD_GetAttributes,ctt.BOOLEAN,[ctt.HANDLE,PHIDD_ATTRIBUTES],argnames=["HidDeviceObject","Attributes"])
        ctt.decorate(self.hidlib.HidD_GetIndexedString,ctt.BOOLEAN,[ctt.HANDLE,ctt.ULONG,ctt.LPVOID,ctt.ULONG],
            argnames=["HidDeviceObject","StringIndex","Buffer","BufferLength"])
        ctt.decorate(self.hidlib.HidD_GetManufacturerString,ctt.BOOLEAN,[ctt.HANDLE,ctt.LPVOID,ctt.ULONG],argnames=["HidDeviceObject","Buffer","BufferLength"])
        ctt.decorate(self.hidlib.HidD_GetProductString,ctt.BOOLEAN,[ctt.HANDLE,ctt.LPVOID,ctt.ULONG],argnames=["HidDeviceObject","Buffer","BufferLength"])
        ctt.decorate(self.hidlib.HidD_GetSerialNumberString,ctt.BOOLEAN,[ctt.HANDLE,ctt.LPVOID,ctt.ULONG],argnames=["HidDeviceObject","Buffer","BufferLength"])
        ctt.decorate(self.hidlib.HidD_GetPhysicalDescriptor,ctt.BOOLEAN,[ctt.HANDLE,ctt.LPVOID,ctt.ULONG],argnames=["HidDeviceObject","Buffer","BufferLength"])
        ctt.decorate(self.hidlib.HidD_GetNumInputBuffers,ctt.BOOLEAN,[ctt.HANDLE,ctt.LPULONG],argnames=["HidDeviceObject","NumberBuffers"])
        ctt.decorate(self.hidlib.HidD_SetNumInputBuffers,ctt.BOOLEAN,[ctt.HANDLE,ctt.ULONG],argnames=["HidDeviceObject","NumberBuffers"])
    def errchecker_bool(self, result, func, arguments):  # pylint: disable=unused-argument
        if not result:
            errcode=self.GetLastError()
            raise HIDLibError(func.__name__,errcode)
        return result
    def initlib(self):
        if self._initialized:
            return
        self.define_functions()
        wrapper=ctypes_wrap.CFunctionWrapper()
        hid_strprep=ctypes_wrap.strprep(_hid_string_size,unicode=True)
        self.GetLastError=wrapper(self.kernel32lib.GetLastError)
        self.Sleep=wrapper(self.kernel32lib.Sleep)
        self.CloseHandle=wrapper(self.kernel32lib.CloseHandle)
        self.CreateFileW=wrapper(self.kernel32lib.CreateFileW)
        self.ReadFile=wrapper(self.kernel32lib.ReadFile, rvals=["lpNumberOfBytesRead"])
        self.WriteFile=wrapper(self.kernel32lib.WriteFile, rvals=["lpNumberOfBytesWritten"])
        self.ReadFile_async=self.kernel32lib.ReadFile
        self.WriteFile_async=self.kernel32lib.WriteFile
        self.CancelIo=wrapper(self.kernel32lib.CancelIo)
        self.CancelIoEx=wrapper(self.kernel32lib.CancelIoEx, rvals=[])
        self.GetOverlappedResult=wrapper(self.kernel32lib.GetOverlappedResult, rvals=["lpNumberOfBytesTransferred"])
        self.SetCommTimeouts=wrapper(self.kernel32lib.SetCommTimeouts, rvals=[], byref=["lpCommTimeouts"])
        self.GetCommTimeouts=wrapper(self.kernel32lib.GetCommTimeouts, rvals=["lpCommTimeouts"])
        self.CreateEventA=wrapper(self.kernel32lib.CreateEventA, rvals=[], byref=[])
        self.SetEvent=wrapper(self.kernel32lib.SetEvent)
        self.ResetEvent=wrapper(self.kernel32lib.ResetEvent)
        self.WaitForSingleObject=wrapper(self.kernel32lib.WaitForSingleObject)
        self.SetupDiGetClassDevsW=wrapper(self.setupapilib.SetupDiGetClassDevsW,byref=["ClassGuid"],rvals=[])
        self.SetupDiDestroyDeviceInfoList=wrapper(self.setupapilib.SetupDiDestroyDeviceInfoList,errcheck=self.errchecker_bool)
        self.SetupDiEnumDeviceInterfaces=wrapper(self.setupapilib.SetupDiEnumDeviceInterfaces,byref=["InterfaceClassGuid","DeviceInterfaceData"],rvals=["DeviceInterfaceData"],
            argprep={"DeviceInterfaceData":CSP_DEVICE_INTERFACE_DATA.prep_struct},errcheck=self.errchecker_bool)
        self.SetupDiGetDeviceInterfaceDetailA=wrapper(self.setupapilib.SetupDiGetDeviceInterfaceDetailA,
            args=["DeviceInfoSet","DeviceInterfaceData","DeviceInterfaceDetailData","DeviceInterfaceDetailDataSize","DeviceInfoData"],
            byref=["DeviceInterfaceData","RequiredSize"],rvals=["RequiredSize"], errcheck=self.errchecker_bool)
        self.HidD_GetHidGuid=wrapper(self.hidlib.HidD_GetHidGuid,byref=["HidGuid"],rvals=["HidGuid"],
            argprep={"HidGuid":ctt.GUID})
        self.HidD_GetPreparsedData=wrapper(self.hidlib.HidD_GetPreparsedData,byref=["PreparsedData"],rvals=["PreparsedData"],
            argprep={"PreparsedData":PHIDP_PREPARSED_DATA})
        self.HidD_FreePreparsedData=wrapper(self.hidlib.HidD_FreePreparsedData,byref=[])
        self.HidP_GetCaps=wrapper(self.hidlib.HidP_GetCaps,byref=["Capabilities"],rvals=["Capabilities"],
            argprep={"Capabilities":CHIDP_CAPS.prep_struct}, rconv={"Capabilities":CHIDP_CAPS.tup_struct})
        self.HidD_GetAttributes=wrapper(self.hidlib.HidD_GetAttributes,byref=["Attributes"],rvals=["Attributes"],
            argprep={"Attributes":CHIDD_ATTRIBUTES.prep_struct}, rconv={"Attributes":CHIDD_ATTRIBUTES.tup_struct})
        self.HidD_GetIndexedString=wrapper(self.hidlib.HidD_GetIndexedString,args=["HidDeviceObject","StringIndex"],rvals=["Buffer"],
            argprep={"Buffer":hid_strprep,"BufferLength":_hid_string_size},byref=[],errcheck=self.errchecker_bool)
        self.HidD_GetManufacturerString=wrapper(self.hidlib.HidD_GetManufacturerString,args=["HidDeviceObject"],rvals=["Buffer"],
            argprep={"Buffer":hid_strprep,"BufferLength":_hid_string_size},byref=[],errcheck=self.errchecker_bool)
        self.HidD_GetProductString=wrapper(self.hidlib.HidD_GetProductString,args=["HidDeviceObject"],rvals=["Buffer"],
            argprep={"Buffer":hid_strprep,"BufferLength":_hid_string_size},byref=[],errcheck=self.errchecker_bool)
        self.HidD_GetSerialNumberString=wrapper(self.hidlib.HidD_GetSerialNumberString,args=["HidDeviceObject"],rvals=["Buffer"],
            argprep={"Buffer":hid_strprep,"BufferLength":_hid_string_size},byref=[],errcheck=self.errchecker_bool)
        self.HidD_GetPhysicalDescriptor=wrapper(self.hidlib.HidD_GetPhysicalDescriptor,args=["HidDeviceObject"],rvals=["Buffer"],
            argprep={"Buffer":hid_strprep,"BufferLength":_hid_string_size},byref=[],errcheck=self.errchecker_bool)
        self.HidD_GetNumInputBuffers=wrapper(self.hidlib.HidD_GetNumInputBuffers,rvals=["NumberBuffers"],errcheck=self.errchecker_bool)
        self.HidD_SetNumInputBuffers=wrapper(self.hidlib.HidD_SetNumInputBuffers,errcheck=self.errchecker_bool)
    def WaitForMultipleObjects(self, Handles, bWaitAll, dwMilliseconds):
        lpHandles=(ctt.HANDLE*len(Handles))(*Handles)
        res=self.kernel32lib.WaitForMultipleObjects(len(Handles),lpHandles,bWaitAll,dwMilliseconds)
        return res
    def list_hid_devices(self):
        guid=self.HidD_GetHidGuid()
        hdevinfo=self.SetupDiGetClassDevsW(guid,None,None,DIGCF.DIGCF_DEVICEINTERFACE|DIGCF.DIGCF_PRESENT)
        try:
            paths=[]
            for i in range(256):
                try:
                    dev_intf_data=self.SetupDiEnumDeviceInterfaces(hdevinfo,None,guid,i)
                except HIDLibError as err:
                    if err.code==0x103:  # ERROR_NO_MORE_ITEMS
                        break
                    raise
                dev_intf_detail_data=CSP_DEVICE_INTERFACE_DETAIL_DATA_A().prep_struct()
                self.SetupDiGetDeviceInterfaceDetailA(hdevinfo,dev_intf_data,ctypes.pointer(dev_intf_detail_data),_detail_data_size,None)
                paths.append(py3.as_str(dev_intf_detail_data.InterfaceClassGuid))
        finally:
            self.SetupDiDestroyDeviceInfoList(hdevinfo)
        return paths
    def make_overlapped(self, evt):
        ovl=ctt.OVERLAPPED()
        ovl.hEvent=evt
        return ovl


wlib=HIDLib()