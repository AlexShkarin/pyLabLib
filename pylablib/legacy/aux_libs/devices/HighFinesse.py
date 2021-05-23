from .misc import default_lib_folder, load_lib, default_placing_message
from ...core.devio.interface import IDevice
from ...core.utils import general

import os.path
import time
import ctypes


class HFError(RuntimeError):
    """Generic HighFinesse wavemeter error"""

class WS(IDevice):
    """
    HighFinesse WS6/7 precision wavemeter.

    Args:
        lib_path(str): path to the wlmData6.dll or wlmData7.dll (default is to use the library supplied with the package)
        idx(int): wavemeter input index (starts from 1)
        serv_path: path to server executable (last executed by default)
        version: wavemeter version (3-4 digit id number)
        hide_app: if ``True``, start the wavemeter application hidden; otherwise, start it on top
    """
    def __init__(self, lib_path=None, idx=1, serv_path=None, version=None, hide_app=False, timeout=10.):
        IDevice.__init__(self)
        error_message="The library is supplied with the designated HighFinesse wavemeter software;\n{}".format(default_placing_message)
        if lib_path in [6,7,None]:
            lib_path=("wlmData6.dll" if lib_path==6 else "wlmData7.dll"), "wlmData.dll"
            self.dll=load_lib(lib_path,locations=("local","global"),call_conv="stdcall",error_message=error_message)
        else:
            self.dll=load_lib(lib_path,call_conv="stdcall",error_message=error_message)
        
        self.dll.Instantiate.restype=ctypes.c_long
        self.dll.Instantiate.argtypes=[ctypes.c_long,ctypes.c_long,ctypes.c_long,ctypes.c_long]
        self.dll.ControlWLM.restype=ctypes.c_long
        self.dll.ControlWLM.argtypes=[ctypes.c_long,ctypes.c_char_p,ctypes.c_long]
        self.dll.Operation.restype=ctypes.c_long
        self.dll.Operation.argtypes=[ctypes.c_short]
        self.dll.GetFrequencyNum.restype=ctypes.c_double
        self.dll.GetFrequencyNum.argtypes=[ctypes.c_long,ctypes.c_double]
        self.dll.GetWavelengthNum.restype=ctypes.c_double
        self.dll.GetWavelengthNum.argtypes=[ctypes.c_long,ctypes.c_double]
        self.dll.GetExposureModeNum.restype=ctypes.c_long
        self.dll.GetExposureModeNum.argtypes=[ctypes.c_long,ctypes.c_bool]
        self.dll.SetExposureModeNum.restype=ctypes.c_long
        self.dll.SetExposureModeNum.argtypes=[ctypes.c_long,ctypes.c_bool]
        self.dll.GetExposureNum.restype=ctypes.c_long
        self.dll.GetExposureNum.argtypes=[ctypes.c_long,ctypes.c_long,ctypes.c_long]
        self.dll.SetExposureNum.restype=ctypes.c_long
        self.dll.SetExposureNum.argtypes=[ctypes.c_long,ctypes.c_long,ctypes.c_long]
        self.dll.GetSwitcherMode.restype=ctypes.c_bool
        self.dll.GetSwitcherMode.argtypes=[ctypes.c_long]
        self.dll.SetSwitcherMode.restype=ctypes.c_long
        self.dll.SetSwitcherMode.argtypes=[ctypes.c_long]
        self.idx=idx
        self.serv_path=serv_path
        self.version=version
        self.hide_app=hide_app
        self.timeout=timeout
        self.open()
        self._add_status_node("frequency",self.get_frequency)
        self._add_status_node("wavelength",self.get_wavelength)
        self._add_settings_node("exposure_mode",self.get_exposure_mode,self.set_exposure_mode)
        self._add_settings_node("exposure",self.get_exposure,self.set_exposure)
        self._add_settings_node("switcher_mode",self.get_switcher_mode,self.set_switcher_mode)

    def open(self):
        self.dll.ControlWLM(2 if self.hide_app else 1,self.serv_path,self.version or 0)
        ctd=general.Countdown(self.timeout)
        while True:
            if self.dll.Instantiate(-1,0,0,0):
                break
            time.sleep(0.1)
            if ctd.passed():
                raise HFError("Timeout on application start")
        self.start_measurement()
    
    _GetFunc_err={  0:"ErrNoValue: No value",
                            -1:"ErrNoSignal: No signal detected",
                            -2:"ErrBadSignal: No calculable signal detected",
                            -3:"ErrLowSignal: Signal too small / underexposed",
                            -4:"ErrBigSignal: Signal too big / overexposed",
                            -5:"ErrWlmMissing: Wavelength meter is not active", 
                            -6:"ErrNotAvailable: Function is not available", 
                            -8:"ErrNoPulse: Signal can't be separated into pulses", 
                            -7:"InfNothingChanged",
                            -13:"ErrDiv0", 
                            -14:"ErrOutOfRange", 
                            -15:"ErrUnitNotAvaliable"}
    def _check_getfunc_error(self, func_name, err):
        if err>=0:
            return
        if err in self._GetFunc_err:
            raise HFError("{} returned error: {} ({})".format(func_name,err,self._GetFunc_err[err]))
        else:
            raise HFError("{} returned unknown error: {}".format(func_name,err))
    _SetFunc_err={  0:"ResERR_NoErr: No error",
                    -1:"ResERR_WlmMissing: Wavelength meter is not active",
                    -2:"ResERR_CouldNotSet: Could not set value which should be accessible (contact Angstrom)",
                    -3:"ResERR_ParmOutOfRange: Parameter is out of range",
                    -4:"ResERR_WlmOutOfResources: Wavelength meter is out of memory or resources (contact Angstrom if persists)",
                    -5:"ResERR_WlmInternalError: Wavelength meter internal error (contact Angstrom)", 
                    -6:"ResERR_NotAvailable: Parameter setting is not available for this wavelength meter version", 
                    -7:"ResERR_WlmBusy: Wavelength meter is busy with another function (contact Angstrom if persists)", 
                    -8:"ResERR_NotInMeasurementMode: Call is not allowed in measurement mode", 
                    -9:"ResERR_OnlyInMeasurementMode: Call is only allowed in measurement mode", 
                    -10:"ResERR_ChannelNotAvailable: Given channel is not available for this device", 
                    -11:"ResERR_ChannelTemporarilyNotAvailable: Given channel is generally available, but the device is not in switch mode", 
                    -12:"ResERR_CalOptionNotAvailable: Wavelength meter does not dispose of this calibration option", 
                    -13:"ResERR_CalWavelengthOutOfRange: The given calibration wavelength is out of its allowed range", 
                    -14:"ResERR_BadCalibrationSignal: The given wavelength does not match the connected calibration laser or its signal is of bad quality", 
                    -15:"ResERR_UnitNotAvailable: This is not a proper result unit"}
    def _check_setfunc_error(self, func_name, err):
        if err>=0:
            return
        if err in self._SetFunc_err:
            raise HFError("{} returned error: {} ({})".format(func_name,err,self._SetFunc_err[err]))
        else:
            raise HFError("{} returned unknown error: {}".format(func_name,err))
    def get_frequency(self, return_exp_error=True):
        """
        Get the wavemeter readings (in Hz).

        If ``return_exp_error==True``, return ``"under"`` if the meter is underexposed or ``"over"`` is it is overexposed.
        Otherwise, raise an error.
        """
        res=self.dll.GetFrequencyNum(self.idx,0.)
        if int(res)<=0:
            err=int(res)
            if return_exp_error:
                if err==-1:
                    return "nosig"
                if err==-2:
                    return "badsig"
                if err==-3:
                    return "under"
                if err==-4:
                    return "over"
            self._check_getfunc_error("GetFrequencyNum",err)
        return res*1E12

    def get_wavelength(self, return_exp_error=True):
        """
        Get the wavemeter readings (in m, and in vacuum).

        If ``return_exp_error==True``, return ``"under"`` if the meter is underexposed or ``"over"`` is it is overexposed.
        Otherwise, raise an error.
        """
        res=self.dll.GetWavelengthNum(self.idx,0)
        if int(res)<=0:
            err=int(res)
            if return_exp_error:
                if err==-1:
                    return "nosig"
                if err==-2:
                    return "badsig"
                if err==-3:
                    return "under"
                if err==-4:
                    return "over"
            self._check_getfunc_error("GetWavelengthNum",err)
        return res*1E-9

    def start_measurement(self):
        self.dll.Operation(2)
    def stop_measurement(self):
        self.dll.Operation(0)

    def get_exposure_mode(self):
        """Get the exposure mode (0 for manual, 1 for auto)"""
        return bool(self.dll.GetExposureModeNum(self.idx,0))
    def set_exposure_mode(self, auto_exposure=True):
        """Get the exposure mode (manual or auto)"""
        err=self.dll.SetExposureModeNum(self.idx,1 if auto_exposure else 0)
        self._check_setfunc_error("SetExposureModeNum",err)
        return self.get_exposure_mode()

    def get_exposure(self, sensor=1):
        """Get the exposure for a given sensor (starting from 1)"""
        exposure=self.dll.GetExposureNum(self.idx,sensor,0)
        self._check_getfunc_error("GetExposureNum",exposure)
        return exposure
    def set_exposure(self, exposure, sensor=1):
        """Manually set the exposure for a given sensor (starting from 1)"""
        err=self.dll.SetExposureNum(self.idx,sensor,exposure)
        self._check_setfunc_error("SetExposureNum",err)
        return self.get_exposure()

    def get_switcher_mode(self):
        """Get the switcher mode (0 for off, 1 for on)"""
        return self.dll.GetSwitcherMode(0)
    def set_switcher_mode(self, switching=True):
        """Set the switcher mode (True or False)"""        
        err=self.dll.SetSwitcherMode(1 if switching else 0)
        self._check_setfunc_error("SetSwitcherMode",err)
        return self.get_switcher_mode()