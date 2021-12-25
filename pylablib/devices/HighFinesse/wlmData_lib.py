# pylint: disable=wrong-spelling-in-comment

from ...core.utils import ctypes_wrap, files
from ...core.devio.comm_backend import DeviceError
from .wlmData_defs import EGetError, ESetError, drEGetError, drESetError  # pylint: disable=unused-import
from .wlmData_defs import EInst, ECtrlMode, EBaseOperation, EAddOperation  # pylint: disable=unused-import
from .wlmData_defs import EMeasUnit, ECalibration, EAutocalibration, EEvent  # pylint: disable=unused-import
from .wlmData_defs import define_functions
from ..utils import load_lib

import ctypes
import os
import re

class HighFinesseError(DeviceError):
    """Generic HighFinesse device error"""
class WlmDataLibError(HighFinesseError):
    """Generic wlmData library error"""
    def __init__(self, func, arguments, code, func_kind="get"):
        self.func=func
        self.arguments=arguments
        self.code=code
        if func_kind=="get":
            self.name=drEGetError.get(code,"Unknown")
        elif func_kind=="set":
            self.name=drESetError.get(code,"Unknown")
        else:
            self.name=""
        if func_kind in ["get","set"]:
            name_str="{}({})".format(self.code,self.name) if func_kind in ["get","set"] else ""
        else:
            name_str="{}".format(self.code)
        self.msg="function '{}' return an error {}".format(func,name_str)
        HighFinesseError.__init__(self,self.msg)
def errcheck(func_kind="get"):
    def errchecker(result, func, arguments):
        if func_kind in {"gzero","get"}:
            err=result<=0
        elif func_kind=="gezero":
            err=result<0
        else:
            err=result!=0
        if err:
            raise WlmDataLibError(func.__name__,arguments,int(result),func_kind=func_kind)
        return result
    return errchecker


class WlmDataLib:
    def __init__(self):
        self._initialized=False
        self.dll_path=None
        self.app_folder=None
        self.app_path=None

    _app_subpaths=["Projects\\64","Com-Test"]
    def find_dll_folder(self, version):
        """Find WLM Control folder corresponding to the given wavemeter version among the standard locations"""
        for arch in ["64bit","32bit"]:
            folder=load_lib.get_program_files_folder("HighFinesse",arch=arch)
            if not os.path.exists(folder):
                continue
            subfolders=files.list_dir(folder).folders
            for sf in subfolders:
                m=re.match(r"^Wavelength Meter WS\d (\d+)$",sf)
                if m and int(m[1])==version:
                    return [os.path.join(folder,sf,ssf) for ssf in self._app_subpaths]
    def setup_app_path(self, dll_path):
        """Attempt to find the WLM Control application path based on the DLL path"""
        self.dll_path=dll_path
        path=files.normalize_path(dll_path)
        if path.lower().endswith(".dll"):
            path=os.path.split(path)[0]
        for sp in self._app_subpaths:
            sp=os.path.normcase(sp)
            if path.endswith(sp):
                app_folder=path[:-len(sp)]
                if os.path.exists(app_folder):
                    self.app_folder=app_folder
                    fs=files.list_dir(app_folder,file_filter=r"wlm_ws.*\.exe").files
                    if fs:
                        self.app_path=os.path.join(app_folder,fs[0])
    def initlib(self, location=None):
        if self._initialized:
            return
        all_locations=("parameter/highfinesse_wlm_data","global")
        if isinstance(location,int):
            location=self.find_dll_folder(location)
        if location:
            if isinstance(location,list):
                location=tuple(location)
            elif not isinstance(location,tuple):
                location=(location,)
            all_locations=location+all_locations
        error_message="The library is located in the folder with HighFinesse wavemeter software"
        self.lib,_,path=load_lib.load_lib("wlmData.dll",locations=all_locations,call_conv="stdcall",return_location=True,error_message=error_message)
        self.setup_app_path(path)

        lib=self.lib
        define_functions(lib)
        wrapper=ctypes_wrap.CFunctionWrapper()
        gzwrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck("gzero"))
        gezwrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck("gezero"))
        getwrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck("get"))
        setwrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck("set"))


        #  ctypes.c_int64 Instantiate(ctypes.c_long RFC, ctypes.c_long Mode, ctypes.c_int64 P1, ctypes.c_long P2)
        self.Instantiate=gzwrapper(lib.Instantiate)
        #  ctypes.c_long ControlWLM(ctypes.c_long Action, ctypes.c_int64 App, ctypes.c_long Ver)
        lib.ControlWLM.argtypes=[ctypes.c_long,ctypes.c_char_p,ctypes.c_long]
        self.ControlWLM=gzwrapper(lib.ControlWLM)
        #  ctypes.c_long ControlWLMEx(ctypes.c_long Action, ctypes.c_int64 App, ctypes.c_long Ver, ctypes.c_long Delay, ctypes.c_long Res)
        lib.ControlWLMEx.argtypes=[ctypes.c_long,ctypes.c_char_p,ctypes.c_long,ctypes.c_long,ctypes.c_long]
        self.ControlWLMEx=gzwrapper(lib.ControlWLMEx)
        # #  ctypes.c_int64 SynchroniseWLM(ctypes.c_long Mode, ctypes.c_int64 TS)
        # self.SynchroniseWLM=gzwrapper(lib.SynchroniseWLM)
        #  ctypes.c_long SetMeasurementDelayMethod(ctypes.c_long Mode, ctypes.c_long Delay)
        self.SetMeasurementDelayMethod=gzwrapper(lib.SetMeasurementDelayMethod)
        #  ctypes.c_long SetWLMPriority(ctypes.c_long PPC, ctypes.c_long Res1, ctypes.c_long Res2)
        self.SetWLMPriority=gzwrapper(lib.SetWLMPriority)
        #  ctypes.c_long WaitForWLMEvent(lref Mode, lref IntVal, dref DblVal)
        self.WaitForWLMEvent=gzwrapper(lib.WaitForWLMEvent, args="all", rvals=["Mode","IntVal","DblVal"])
        #  ctypes.c_long WaitForWLMEventEx(lref Ver, lref Mode, lref IntVal, dref DblVal, lref Res1)
        self.WaitForWLMEventEx=gzwrapper(lib.WaitForWLMEventEx, args="all", rvals=["Ver","Mode","IntVal","DblVal","Res1"])
        #  ctypes.c_long WaitForNextWLMEvent(lref Mode, lref IntVal, dref DblVal)
        self.WaitForNextWLMEvent=gzwrapper(lib.WaitForNextWLMEvent, args="all", rvals=["Mode","IntVal","DblVal"])
        #  ctypes.c_long WaitForNextWLMEventEx(lref Ver, lref Mode, lref IntVal, dref DblVal, lref Res1)
        self.WaitForNextWLMEventEx=gzwrapper(lib.WaitForNextWLMEventEx, args="all", rvals=["Ver","Mode","IntVal","DblVal","Res1"])
        #  None ClearWLMEvents()
        self.ClearWLMEvents=gzwrapper(lib.ClearWLMEvents)
        #  ctypes.c_long GetWLMVersion(ctypes.c_long Ver)
        self.GetWLMVersion=getwrapper(lib.GetWLMVersion)
        #  ctypes.c_long GetWLMCount(ctypes.c_long V)
        self.GetWLMCount=wrapper(lib.GetWLMCount)
        #  ctypes.c_long GetWLMIndex(ctypes.c_long Ver)
        self.GetWLMIndex=gezwrapper(lib.GetWLMIndex)
        #  ctypes.c_long PresetWLMIndex(ctypes.c_long Ver)
        self.PresetWLMIndex=gezwrapper(lib.PresetWLMIndex)
        #  ctypes.c_long GetActiveChannel(ctypes.c_long Mode, lref Port, ctypes.c_long Res1)
        self.GetActiveChannel=gzwrapper(lib.GetActiveChannel,rvals=[None,"Port"])
        #  ctypes.c_long SetActiveChannel(ctypes.c_long Mode, ctypes.c_long Port, ctypes.c_long CH, ctypes.c_long Res1)
        self.SetActiveChannel=setwrapper(lib.SetActiveChannel)
        #  ctypes.c_long GetChannelsCount(ctypes.c_long C)
        self.GetChannelsCount=wrapper(lib.GetChannelsCount)
        #  ctypes.c_double ConvertUnit(ctypes.c_double Val, ctypes.c_long uFrom, ctypes.c_long uTo)
        self.ConvertUnit=wrapper(lib.ConvertUnit)
        #  ctypes.c_double ConvertDeltaUnit(ctypes.c_double Base, ctypes.c_double Delta, ctypes.c_long uBase, ctypes.c_long uFrom, ctypes.c_long uTo)
        self.ConvertDeltaUnit=wrapper(lib.ConvertDeltaUnit)
        #  bool GetReduced(bool R)
        self.GetReduced=wrapper(lib.GetReduced)
        #  ctypes.c_long SetReduced(bool R)
        self.SetReduced=setwrapper(lib.SetReduced)
        #  ctypes.c_ushort GetScale(ctypes.c_ushort S)
        self.GetScale=wrapper(lib.GetScale)
        #  ctypes.c_long SetScale(ctypes.c_ushort S)
        self.SetScale=setwrapper(lib.SetScale)

        #  ctypes.c_double GetWavelength(ctypes.c_double WL)
        self.GetWavelength=getwrapper(lib.GetWavelength)
        #  ctypes.c_double GetWavelength2(ctypes.c_double WL2)
        self.GetWavelength2=getwrapper(lib.GetWavelength2)
        #  ctypes.c_double GetWavelengthNum(ctypes.c_long num, ctypes.c_double WL)
        self.GetWavelengthNum=getwrapper(lib.GetWavelengthNum)
        #  ctypes.c_double GetCalWavelength(ctypes.c_long ba, ctypes.c_double WL)
        self.GetCalWavelength=getwrapper(lib.GetCalWavelength)
        #  ctypes.c_double GetCalibrationEffect(ctypes.c_double CE)
        self.GetCalibrationEffect=gzwrapper(lib.GetCalibrationEffect)
        #  ctypes.c_double GetFrequency(ctypes.c_double F)
        self.GetFrequency=getwrapper(lib.GetFrequency)
        #  ctypes.c_double GetFrequency2(ctypes.c_double F2)
        self.GetFrequency2=getwrapper(lib.GetFrequency2)
        #  ctypes.c_double GetFrequencyNum(ctypes.c_long num, ctypes.c_double F)
        self.GetFrequencyNum=getwrapper(lib.GetFrequencyNum)
        #  ctypes.c_double GetLinewidth(ctypes.c_long Index, ctypes.c_double LW)
        self.GetLinewidth=getwrapper(lib.GetLinewidth)
        #  ctypes.c_double GetLinewidthNum(ctypes.c_long num, ctypes.c_double LW)
        self.GetLinewidthNum=getwrapper(lib.GetLinewidthNum)
        #  ctypes.c_double GetDistance(ctypes.c_double D)
        self.GetDistance=getwrapper(lib.GetDistance)
        #  ctypes.c_double GetAnalogIn(ctypes.c_double AI)
        self.GetAnalogIn=wrapper(lib.GetAnalogIn)
        #  ctypes.c_double GetTemperature(ctypes.c_double T)
        self.GetTemperature=getwrapper(lib.GetTemperature)
        #  ctypes.c_long SetTemperature(ctypes.c_double T)
        self.SetTemperature=setwrapper(lib.SetTemperature)
        #  ctypes.c_double GetPressure(ctypes.c_double P)
        self.GetPressure=getwrapper(lib.GetPressure)
        #  ctypes.c_long SetPressure(ctypes.c_long Mode, ctypes.c_double P)
        self.SetPressure=setwrapper(lib.SetPressure)
        #  ctypes.c_double GetExternalInput(ctypes.c_long Index, ctypes.c_double I)
        self.GetExternalInput=gezwrapper(lib.GetExternalInput)
        #  ctypes.c_long SetExternalInput(ctypes.c_long Index, ctypes.c_double I)
        self.SetExternalInput=setwrapper(lib.SetExternalInput)
        #  ctypes.c_ushort GetExposure(ctypes.c_ushort E)
        self.GetExposure=gezwrapper(lib.GetExposure)
        #  ctypes.c_long SetExposure(ctypes.c_ushort E)
        self.SetExposure=setwrapper(lib.SetExposure)
        #  ctypes.c_ushort GetExposure2(ctypes.c_ushort E2)
        self.GetExposure2=gezwrapper(lib.GetExposure2)
        #  ctypes.c_long SetExposure2(ctypes.c_ushort E2)
        self.SetExposure2=setwrapper(lib.SetExposure2)
        #  ctypes.c_long GetExposureNum(ctypes.c_long num, ctypes.c_long arr, ctypes.c_long E)
        self.GetExposureNum=gezwrapper(lib.GetExposureNum)
        #  ctypes.c_long SetExposureNum(ctypes.c_long num, ctypes.c_long arr, ctypes.c_long E)
        self.SetExposureNum=setwrapper(lib.SetExposureNum)
        #  bool GetExposureMode(bool EM)
        self.GetExposureMode=gezwrapper(lib.GetExposureMode)
        #  ctypes.c_long SetExposureMode(bool EM)
        self.SetExposureMode=setwrapper(lib.SetExposureMode)
        #  ctypes.c_long GetExposureModeNum(ctypes.c_long num, bool EM)
        self.GetExposureModeNum=gezwrapper(lib.GetExposureModeNum)
        #  ctypes.c_long SetExposureModeNum(ctypes.c_long num, bool EM)
        self.SetExposureModeNum=setwrapper(lib.SetExposureModeNum)
        #  ctypes.c_long GetExposureRange(ctypes.c_long ER)
        self.GetExposureRange=wrapper(lib.GetExposureRange)
        #  ctypes.c_ushort GetResultMode(ctypes.c_ushort RM)
        self.GetResultMode=wrapper(lib.GetResultMode)
        #  ctypes.c_long SetResultMode(ctypes.c_ushort RM)
        self.SetResultMode=setwrapper(lib.SetResultMode)
        #  ctypes.c_ushort GetRange(ctypes.c_ushort R)
        self.GetRange=wrapper(lib.GetRange)
        #  ctypes.c_long SetRange(ctypes.c_ushort R)
        self.SetRange=setwrapper(lib.SetRange)
        #  ctypes.c_ushort GetPulseMode(ctypes.c_ushort PM)
        self.GetPulseMode=wrapper(lib.GetPulseMode)
        #  ctypes.c_long SetPulseMode(ctypes.c_ushort PM)
        self.SetPulseMode=setwrapper(lib.SetPulseMode)
        #  ctypes.c_ushort GetWideMode(ctypes.c_ushort WM)
        self.GetWideMode=wrapper(lib.GetWideMode)
        #  ctypes.c_long SetWideMode(ctypes.c_ushort WM)
        self.SetWideMode=setwrapper(lib.SetWideMode)
        #  ctypes.c_long GetDisplayMode(ctypes.c_long DM)
        self.GetDisplayMode=wrapper(lib.GetDisplayMode)
        #  ctypes.c_long SetDisplayMode(ctypes.c_long DM)
        self.SetDisplayMode=setwrapper(lib.SetDisplayMode)
        #  bool GetFastMode(bool FM)
        self.GetFastMode=wrapper(lib.GetFastMode)
        #  ctypes.c_long SetFastMode(bool FM)
        self.SetFastMode=setwrapper(lib.SetFastMode)
        #  bool GetLinewidthMode(bool LM)
        self.GetLinewidthMode=wrapper(lib.GetLinewidthMode)
        #  ctypes.c_long SetLinewidthMode(bool LM)
        self.SetLinewidthMode=setwrapper(lib.SetLinewidthMode)
        #  bool GetDistanceMode(bool DM)
        self.GetDistanceMode=wrapper(lib.GetDistanceMode)
        #  ctypes.c_long SetDistanceMode(bool DM)
        self.SetDistanceMode=setwrapper(lib.SetDistanceMode)
        #  ctypes.c_long GetSwitcherMode(ctypes.c_long SM)
        self.GetSwitcherMode=wrapper(lib.GetSwitcherMode)
        #  ctypes.c_long SetSwitcherMode(ctypes.c_long SM)
        self.SetSwitcherMode=setwrapper(lib.SetSwitcherMode)
        #  ctypes.c_long GetSwitcherChannel(ctypes.c_long CH)
        self.GetSwitcherChannel=wrapper(lib.GetSwitcherChannel)
        #  ctypes.c_long SetSwitcherChannel(ctypes.c_long CH)
        self.SetSwitcherChannel=setwrapper(lib.SetSwitcherChannel)
        #  ctypes.c_long GetSwitcherSignalStates(ctypes.c_long Signal, lref Use, lref Show)
        self.GetSwitcherSignalStates=setwrapper(lib.GetSwitcherSignalStates,rvals=["Use","Show"])
        #  ctypes.c_long SetSwitcherSignalStates(ctypes.c_long Signal, ctypes.c_long Use, ctypes.c_long Show)
        self.SetSwitcherSignalStates=setwrapper(lib.SetSwitcherSignalStates)
        #  ctypes.c_long SetSwitcherSignal(ctypes.c_long Signal, ctypes.c_long Use, ctypes.c_long Show)
        self.SetSwitcherSignal=setwrapper(lib.SetSwitcherSignal)
        #  ctypes.c_long GetAutoCalMode(ctypes.c_long ACM)
        self.GetAutoCalMode=wrapper(lib.GetAutoCalMode)
        #  ctypes.c_long SetAutoCalMode(ctypes.c_long ACM)
        self.SetAutoCalMode=setwrapper(lib.SetAutoCalMode)
        #  ctypes.c_long GetAutoCalSetting(ctypes.c_long ACS, lref val, ctypes.c_long Res1, lref Res2)
        self.GetAutoCalSetting=wrapper(lib.GetAutoCalSetting,rvals=[None,"val","Res2"])
        #  ctypes.c_long SetAutoCalSetting(ctypes.c_long ACS, ctypes.c_long val, ctypes.c_long Res1, ctypes.c_long Res2)
        self.SetAutoCalSetting=setwrapper(lib.SetAutoCalSetting)
        #  ctypes.c_ushort GetOperationState(ctypes.c_ushort OS)
        self.GetOperationState=wrapper(lib.GetOperationState)
        #  ctypes.c_long Operation(ctypes.c_ushort Op)
        self.Operation=setwrapper(lib.Operation)
        #  ctypes.c_long SetOperationFile(sref lpFile)
        self.SetOperationFile=setwrapper(lib.SetOperationFile)
        #  ctypes.c_long Calibration(ctypes.c_long Type, ctypes.c_long Unit, ctypes.c_double Value, ctypes.c_long Channel)
        self.Calibration=setwrapper(lib.Calibration)
        # #  ctypes.c_long RaiseMeasurementEvent(ctypes.c_long Mode)
        # lib.RaiseMeasurementEvent.restype=ctypes.c_long
        # lib.RaiseMeasurementEvent.argtypes=[ctypes.c_long]
        # lib.RaiseMeasurementEvent.argnames=["Mode"]
        #  ctypes.c_long TriggerMeasurement(ctypes.c_long Action)
        self.TriggerMeasurement=setwrapper(lib.TriggerMeasurement)
        # #  ctypes.c_long GetTriggerState(ctypes.c_long TS)
        # lib.GetTriggerState.restype=ctypes.c_long
        # lib.GetTriggerState.argtypes=[ctypes.c_long]
        # lib.GetTriggerState.argnames=["TS"]
        #  ctypes.c_long GetInterval(ctypes.c_long I)
        self.GetInterval=wrapper(lib.GetInterval)
        #  ctypes.c_long SetInterval(ctypes.c_long I)
        self.SetInterval=setwrapper(lib.SetInterval)
        #  bool GetIntervalMode(bool IM)
        self.GetIntervalMode=wrapper(lib.GetIntervalMode)
        #  ctypes.c_long SetIntervalMode(bool IM)
        self.SetIntervalMode=setwrapper(lib.SetIntervalMode)
        #  ctypes.c_long GetBackground(ctypes.c_long BG)
        self.GetBackground=wrapper(lib.GetBackground)
        #  ctypes.c_long SetBackground(ctypes.c_long BG)
        self.SetBackground=setwrapper(lib.SetBackground)
        #  bool GetLinkState(bool LS)
        self.GetLinkState=wrapper(lib.GetLinkState)
        #  ctypes.c_long SetLinkState(bool LS)
        self.SetLinkState=setwrapper(lib.SetLinkState)
        #  None LinkSettingsDlg()
        self.LinkSettingsDlg=wrapper(lib.LinkSettingsDlg)

        self._initialized=True
        ### Pattern / Analysis
        # #  ctypes.c_long GetPatternItemSize(ctypes.c_long Index)
        # lib.GetPatternItemSize.restype=ctypes.c_long
        # lib.GetPatternItemSize.argtypes=[ctypes.c_long]
        # lib.GetPatternItemSize.argnames=["Index"]
        # #  ctypes.c_long GetPatternItemCount(ctypes.c_long Index)
        # lib.GetPatternItemCount.restype=ctypes.c_long
        # lib.GetPatternItemCount.argtypes=[ctypes.c_long]
        # lib.GetPatternItemCount.argnames=["Index"]
        # #  ULONG_PTR GetPattern(ctypes.c_long Index)
        # lib.GetPattern.restype=ULONG_PTR
        # lib.GetPattern.argtypes=[ctypes.c_long]
        # lib.GetPattern.argnames=["Index"]
        # #  ULONG_PTR GetPatternNum(ctypes.c_long Chn, ctypes.c_long Index)
        # lib.GetPatternNum.restype=ULONG_PTR
        # lib.GetPatternNum.argtypes=[ctypes.c_long, ctypes.c_long]
        # lib.GetPatternNum.argnames=["Chn", "Index"]
        # #  ctypes.c_long GetPatternData(ctypes.c_long Index, ULONG_PTR PArray)
        # lib.GetPatternData.restype=ctypes.c_long
        # lib.GetPatternData.argtypes=[ctypes.c_long, ULONG_PTR]
        # lib.GetPatternData.argnames=["Index", "PArray"]
        # #  ctypes.c_long GetPatternDataNum(ctypes.c_long Chn, ctypes.c_long Index, ULONG_PTR PArray)
        # lib.GetPatternDataNum.restype=ctypes.c_long
        # lib.GetPatternDataNum.argtypes=[ctypes.c_long, ctypes.c_long, ULONG_PTR]
        # lib.GetPatternDataNum.argnames=["Chn", "Index", "PArray"]
        # #  ctypes.c_long SetPattern(ctypes.c_long Index, ctypes.c_long iEnable)
        # lib.SetPattern.restype=ctypes.c_long
        # lib.SetPattern.argtypes=[ctypes.c_long, ctypes.c_long]
        # lib.SetPattern.argnames=["Index", "iEnable"]
        # #  ctypes.c_long SetPatternData(ctypes.c_long Index, ULONG_PTR PArray)
        # lib.SetPatternData.restype=ctypes.c_long
        # lib.SetPatternData.argtypes=[ctypes.c_long, ULONG_PTR]
        # lib.SetPatternData.argnames=["Index", "PArray"]
        # #  bool GetAnalysisMode(bool AM)
        # lib.GetAnalysisMode.restype=bool
        # lib.GetAnalysisMode.argtypes=[bool]
        # lib.GetAnalysisMode.argnames=["AM"]
        # #  ctypes.c_long SetAnalysisMode(bool AM)
        # lib.SetAnalysisMode.restype=ctypes.c_long
        # lib.SetAnalysisMode.argtypes=[bool]
        # lib.SetAnalysisMode.argnames=["AM"]
        # #  ctypes.c_long GetAnalysisItemSize(ctypes.c_long Index)
        # lib.GetAnalysisItemSize.restype=ctypes.c_long
        # lib.GetAnalysisItemSize.argtypes=[ctypes.c_long]
        # lib.GetAnalysisItemSize.argnames=["Index"]
        # #  ctypes.c_long GetAnalysisItemCount(ctypes.c_long Index)
        # lib.GetAnalysisItemCount.restype=ctypes.c_long
        # lib.GetAnalysisItemCount.argtypes=[ctypes.c_long]
        # lib.GetAnalysisItemCount.argnames=["Index"]
        # #  ULONG_PTR GetAnalysis(ctypes.c_long Index)
        # lib.GetAnalysis.restype=ULONG_PTR
        # lib.GetAnalysis.argtypes=[ctypes.c_long]
        # lib.GetAnalysis.argnames=["Index"]
        # #  ctypes.c_long GetAnalysisData(ctypes.c_long Index, ULONG_PTR PArray)
        # lib.GetAnalysisData.restype=ctypes.c_long
        # lib.GetAnalysisData.argtypes=[ctypes.c_long, ULONG_PTR]
        # lib.GetAnalysisData.argnames=["Index", "PArray"]
        # #  ctypes.c_long SetAnalysis(ctypes.c_long Index, ctypes.c_long iEnable)
        # lib.SetAnalysis.restype=ctypes.c_long
        # lib.SetAnalysis.argtypes=[ctypes.c_long, ctypes.c_long]
        # lib.SetAnalysis.argnames=["Index", "iEnable"]
        # #  ctypes.c_long GetMinPeak(ctypes.c_long M1)
        # lib.GetMinPeak.restype=ctypes.c_long
        # lib.GetMinPeak.argtypes=[ctypes.c_long]
        # lib.GetMinPeak.argnames=["M1"]
        # #  ctypes.c_long GetMinPeak2(ctypes.c_long M2)
        # lib.GetMinPeak2.restype=ctypes.c_long
        # lib.GetMinPeak2.argtypes=[ctypes.c_long]
        # lib.GetMinPeak2.argnames=["M2"]
        # #  ctypes.c_long GetMaxPeak(ctypes.c_long X1)
        # lib.GetMaxPeak.restype=ctypes.c_long
        # lib.GetMaxPeak.argtypes=[ctypes.c_long]
        # lib.GetMaxPeak.argnames=["X1"]
        # #  ctypes.c_long GetMaxPeak2(ctypes.c_long X2)
        # lib.GetMaxPeak2.restype=ctypes.c_long
        # lib.GetMaxPeak2.argtypes=[ctypes.c_long]
        # lib.GetMaxPeak2.argnames=["X2"]
        # #  ctypes.c_long GetAvgPeak(ctypes.c_long A1)
        # lib.GetAvgPeak.restype=ctypes.c_long
        # lib.GetAvgPeak.argtypes=[ctypes.c_long]
        # lib.GetAvgPeak.argnames=["A1"]
        # #  ctypes.c_long GetAvgPeak2(ctypes.c_long A2)
        # lib.GetAvgPeak2.restype=ctypes.c_long
        # lib.GetAvgPeak2.argtypes=[ctypes.c_long]
        # lib.GetAvgPeak2.argnames=["A2"]
        # #  ctypes.c_long SetAvgPeak(ctypes.c_long PA)
        # lib.SetAvgPeak.restype=ctypes.c_long
        # lib.SetAvgPeak.argtypes=[ctypes.c_long]
        # lib.SetAvgPeak.argnames=["PA"]
        #  ctypes.c_long GetAmplitudeNum(ctypes.c_long num, ctypes.c_long Index, ctypes.c_long A)
        # lib.GetAmplitudeNum.restype=ctypes.c_long
        # lib.GetAmplitudeNum.argtypes=[ctypes.c_long, ctypes.c_long, ctypes.c_long]
        # lib.GetAmplitudeNum.argnames=["num", "Index", "A"]
        # #  ctypes.c_double GetIntensityNum(ctypes.c_long num, ctypes.c_double I)
        # lib.GetIntensityNum.restype=ctypes.c_double
        # lib.GetIntensityNum.argtypes=[ctypes.c_long, ctypes.c_double]
        # lib.GetIntensityNum.argnames=["num", "I"]
        # #  ctypes.c_double GetPowerNum(ctypes.c_long num, ctypes.c_double P)
        # lib.GetPowerNum.restype=ctypes.c_double
        # lib.GetPowerNum.argtypes=[ctypes.c_long, ctypes.c_double]
        # lib.GetPowerNum.argnames=["num", "P"]
        # #  ctypes.c_ushort GetDelay(ctypes.c_ushort D)
        # lib.GetDelay.restype=ctypes.c_ushort
        # lib.GetDelay.argtypes=[ctypes.c_ushort]
        # lib.GetDelay.argnames=["D"]
        # #  ctypes.c_long SetDelay(ctypes.c_ushort D)
        # lib.SetDelay.restype=ctypes.c_long
        # lib.SetDelay.argtypes=[ctypes.c_ushort]
        # lib.SetDelay.argnames=["D"]
        # #  ctypes.c_ushort GetShift(ctypes.c_ushort S)
        # lib.GetShift.restype=ctypes.c_ushort
        # lib.GetShift.argtypes=[ctypes.c_ushort]
        # lib.GetShift.argnames=["S"]
        # #  ctypes.c_long SetShift(ctypes.c_ushort S)
        # lib.SetShift.restype=ctypes.c_long
        # lib.SetShift.argtypes=[ctypes.c_ushort]
        # lib.SetShift.argnames=["S"]
        # #  ctypes.c_ushort GetShift2(ctypes.c_ushort S2)
        # lib.GetShift2.restype=ctypes.c_ushort
        # lib.GetShift2.argtypes=[ctypes.c_ushort]
        # lib.GetShift2.argnames=["S2"]
        # #  ctypes.c_long SetShift2(ctypes.c_ushort S2)
        # lib.SetShift2.restype=ctypes.c_long
        # lib.SetShift2.argtypes=[ctypes.c_ushort]
        # lib.SetShift2.argnames=["S2"]

        ### PID / Deviation ###
        # #  bool GetDeviationMode(bool DM)
        # lib.GetDeviationMode.restype=bool
        # lib.GetDeviationMode.argtypes=[bool]
        # lib.GetDeviationMode.argnames=["DM"]
        # #  ctypes.c_long SetDeviationMode(bool DM)
        # lib.SetDeviationMode.restype=ctypes.c_long
        # lib.SetDeviationMode.argtypes=[bool]
        # lib.SetDeviationMode.argnames=["DM"]
        # #  ctypes.c_double GetDeviationReference(ctypes.c_double DR)
        # lib.GetDeviationReference.restype=ctypes.c_double
        # lib.GetDeviationReference.argtypes=[ctypes.c_double]
        # lib.GetDeviationReference.argnames=["DR"]
        # #  ctypes.c_long SetDeviationReference(ctypes.c_double DR)
        # lib.SetDeviationReference.restype=ctypes.c_long
        # lib.SetDeviationReference.argtypes=[ctypes.c_double]
        # lib.SetDeviationReference.argnames=["DR"]
        # #  ctypes.c_long GetDeviationSensitivity(ctypes.c_long DS)
        # lib.GetDeviationSensitivity.restype=ctypes.c_long
        # lib.GetDeviationSensitivity.argtypes=[ctypes.c_long]
        # lib.GetDeviationSensitivity.argnames=["DS"]
        # #  ctypes.c_long SetDeviationSensitivity(ctypes.c_long DS)
        # lib.SetDeviationSensitivity.restype=ctypes.c_long
        # lib.SetDeviationSensitivity.argtypes=[ctypes.c_long]
        # lib.SetDeviationSensitivity.argnames=["DS"]
        # #  ctypes.c_double GetDeviationSignal(ctypes.c_double DS)
        # self.GetDeviationSignal=wrapper(lib.GetDeviationSignal)
        # #  ctypes.c_double GetDeviationSignalNum(ctypes.c_long Port, ctypes.c_double DS)
        # self.GetDeviationSignalNum=setwrapper(lib.GetDeviationSignalNum)
        # #  ctypes.c_long SetDeviationSignal(ctypes.c_double DS)
        # self.SetDeviationSignal=setwrapper(lib.SetDeviationSignal)
        # #  ctypes.c_long SetDeviationSignalNum(ctypes.c_long Port, ctypes.c_double DS)
        # self.SetDeviationSignalNum=setwrapper(lib.SetDeviationSignalNum)
        # #  ctypes.c_double RaiseDeviationSignal(ctypes.c_long iType, ctypes.c_double dSignal)
        # lib.RaiseDeviationSignal.restype=ctypes.c_double
        # lib.RaiseDeviationSignal.argtypes=[ctypes.c_long, ctypes.c_double]
        # lib.RaiseDeviationSignal.argnames=["iType", "dSignal"]
        # #  ctypes.c_long GetPIDCourse(sref PIDC)
        # lib.GetPIDCourse.restype=ctypes.c_long
        # lib.GetPIDCourse.argtypes=[sref]
        # lib.GetPIDCourse.argnames=["PIDC"]
        # #  ctypes.c_long SetPIDCourse(sref PIDC)
        # lib.SetPIDCourse.restype=ctypes.c_long
        # lib.SetPIDCourse.argtypes=[sref]
        # lib.SetPIDCourse.argnames=["PIDC"]
        # #  ctypes.c_long GetPIDCourseNum(ctypes.c_long Port, sref PIDC)
        # lib.GetPIDCourseNum.restype=ctypes.c_long
        # lib.GetPIDCourseNum.argtypes=[ctypes.c_long, sref]
        # lib.GetPIDCourseNum.argnames=["Port", "PIDC"]
        # #  ctypes.c_long SetPIDCourseNum(ctypes.c_long Port, sref PIDC)
        # lib.SetPIDCourseNum.restype=ctypes.c_long
        # lib.SetPIDCourseNum.argtypes=[ctypes.c_long, sref]
        # lib.SetPIDCourseNum.argnames=["Port", "PIDC"]
        # #  ctypes.c_long GetPIDSetting(ctypes.c_long PS, ctypes.c_long Port, lref iSet, dref dSet)
        # lib.GetPIDSetting.restype=ctypes.c_long
        # lib.GetPIDSetting.argtypes=[ctypes.c_long, ctypes.c_long, lref, dref]
        # lib.GetPIDSetting.argnames=["PS", "Port", "iSet", "dSet"]
        # #  ctypes.c_long SetPIDSetting(ctypes.c_long PS, ctypes.c_long Port, ctypes.c_long iSet, ctypes.c_double dSet)
        # lib.SetPIDSetting.restype=ctypes.c_long
        # lib.SetPIDSetting.argtypes=[ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_double]
        # lib.SetPIDSetting.argnames=["PS", "Port", "iSet", "dSet"]
        # #  ctypes.c_long GetLaserControlSetting(ctypes.c_long PS, ctypes.c_long Port, lref iSet, dref dSet, sref sSet)
        # lib.GetLaserControlSetting.restype=ctypes.c_long
        # lib.GetLaserControlSetting.argtypes=[ctypes.c_long, ctypes.c_long, lref, dref, sref]
        # lib.GetLaserControlSetting.argnames=["PS", "Port", "iSet", "dSet", "sSet"]
        # #  ctypes.c_long SetLaserControlSetting(ctypes.c_long PS, ctypes.c_long Port, ctypes.c_long iSet, ctypes.c_double dSet, sref sSet)
        # lib.SetLaserControlSetting.restype=ctypes.c_long
        # lib.SetLaserControlSetting.argtypes=[ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_double, sref]
        # lib.SetLaserControlSetting.argnames=["PS", "Port", "iSet", "dSet", "sSet"]
        # #  ctypes.c_long ClearPIDHistory(ctypes.c_long Port)
        # lib.ClearPIDHistory.restype=ctypes.c_long
        # lib.ClearPIDHistory.argtypes=[ctypes.c_long]
        # lib.ClearPIDHistory.argnames=["Port"]