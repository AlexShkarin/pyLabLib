from ...core.utils import general
from ...core.devio.interface import IDevice

from .misc import default_placing_message, load_lib

import os.path
import ctypes
import time

class SmarActError(RuntimeError):
    """Generic SmarAct error."""

class SCU3D(IDevice):
    """
    SmarAct SCU3D translation stage.

    Args:
        lib_path(str): path to the SCU3DControl.dll (default is to use the library supplied with the package)
        idx(int): stage index
        axis_mapping(str): 3-symbol string specifying indices of x, y and z axes (can be any permutation of ``"xyz"``)
        axis_dir(str): 3-symbol string specifying default directions of the axes (each symbol be ``"+"`` or ``"-"``)
    """
    def __init__(self, lib_path=None, idx=0, axis_mapping="xyz", axis_dir="+++"):
        IDevice.__init__(self)
        error_message="The library is supplied by the manufacturer with the device;\n{}".format(default_placing_message)
        if lib_path is None:
            self.dll=load_lib("SCU3DControl.dll",locations=("local","global"),call_conv="cdecl",error_message=error_message)
        else:
            self.dll=load_lib(lib_path,call_conv="cdecl",error_message=error_message)
        self.dll.SA_MoveStep_S.argtypes=[ctypes.c_uint,ctypes.c_uint,ctypes.c_int,ctypes.c_uint,ctypes.c_uint]
        self.dll.SA_GetStatus_S.argtypes=[ctypes.c_uint,ctypes.c_uint,ctypes.POINTER(ctypes.c_uint)]
        self.idx=idx
        self.axis_mapping=axis_mapping
        self.axis_dir=axis_dir
        self.open()
        self._add_settings_node("axis_mapping",self.get_axis_mapping,self.set_axis_mapping)
        self._add_settings_node("axis_dir",self.get_axis_dir,self.set_axis_dir)
        self._add_status_node("axis_status",self.get_status,mux=("xyz",))
        self._add_status_node("moving",self.is_moving,mux=("xyz",))

    def open(self):
        """Open the connection to the stage"""
        self._check_status("SA_InitDevices",self.dll.SA_InitDevices(0))
        self.connected=True
    def close(self):
        """Close the connection to the stage"""
        self._check_status("SA_ReleaseDevices",self.dll.SA_ReleaseDevices())
        self.connected=False
    def is_opened(self):
        return self.connected

    _func_status={  0:"SA_OK",
                    1:"SA_INITIALIZATION_ERROR",
                    2:"SA_NOT_INITIALIZED_ERROR",
                    3:"SA_NO_DEVICES_FOUND_ERROR",
                    4:"SA_TOO_MANY_DEVICES_ERROR",
                    5:"SA_INVALID_DEVICE_INDEX_ERROR",
                    6:"SA_INVALID_CHANNEL_INDEX_ERROR",
                    7:"SA_TRANSMIT_ERROR",
                    8:"SA_WRITE_ERROR",
                    9:"SA_INVALID_PARAMETER_ERROR",
                    10:"SA_READ_ERROR",
                    12:"SA_INTERNAL_ERROR",
                    13:"SA_WRONG_MODE_ERROR",
                    14:"SA_PROTOCOL_ERROR",
                    15:"SA_TIMEOUT_ERROR",
                    16:"SA_NOTIFICATION_ALREADY_SET_ERROR",
                    17:"SA_ID_LIST_TOO_SMALL_ERROR",
                    18:"SA_DEVICE_ALREADY_ADDED_ERROR",
                    19:"SA_DEVICE_NOT_FOUND_ERROR",
                    128:"SA_INVALID_COMMAND_ERROR",
                    129:"SA_COMMAND_NOT_SUPPORTED_ERROR",
                    130:"SA_NO_SENSOR_PRESENT_ERROR",
                    131:"SA_WRONG_SENSOR_TYPE_ERROR",
                    132:"SA_END_STOP_REACHED_ERROR",
                    133:"SA_COMMAND_OVERRIDDEN_ERROR",
                    134:"SA_HV_RANGE_ERROR",
                    135:"SA_TEMP_OVERHEAT_ERROR",
                    136:"SA_CALIBRATION_FAILED_ERROR",
                    137:"SA_REFERENCING_FAILED_ERROR",
                    138:"SA_NOT_PROCESSABLE_ERROR",
                    255:"SA_OTHER_ERROR"}
    def _check_status(self, func, status):
        if status:
            if status in self._func_status:
                raise SmarActError("function {} raised error: {} ({})".format(func,status,self._func_status[status]))
            else:
                raise SmarActError("function {} raised unknown error: {}".format(func,status))
    
    def get_axis_mapping(self):
        return self.axis_mapping
    def set_axis_mapping(self, mapping):
        self.axis_mapping=mapping
        return self.get_axis_mapping()
    def get_axis_dir(self):
        return self.axis_dir
    def set_axis_dir(self, dir):
        self.axis_dir=dir
        return self.get_axis_dir()

    def _get_axis(self, axis):
        if axis in list(self.axis_mapping):
            return self.axis_mapping.find(axis)
        return axis
    def move_macrostep(self, axis, steps, voltage, frequency):
        """
        Move along a given axis with a given number of steps.

        `voltage` (in Volts) and `frequency` (in Hz) specify the motion parameters.
        """
        axis=self._get_axis(axis)
        axis_dir=-1 if self.axis_dir[axis]=="-" else 1
        stat=self.dll.SA_MoveStep_S(self.idx,self._get_axis(axis),int(steps)*axis_dir,int(voltage*10),int(frequency))
        self._check_status("SA_MoveStep_S",stat)
    _move_presets=[ (1,25.3,1E3), (1,28,1E3), (1,32,1E3), (1,38,1E3), (1,47,1E3),
                    (1,60.5,1E3), (1,80.8,1E3), (2,65.6,1E3), (2,88.4,1E3), (4,88.4,1E3),
                    (7,100.,1E3), (14,100.,1E3), (28,100.,1E3), (56,100.,1.1E3), (100,100.,2.2E3), 
                    (200,100.,4.4E3), (400,100.,8.8E3), (1E3,100.,10E3), (1.8E3,100.,10E3)]
    def move(self, axis, steps=1, stepsize=10):
        """
        Move along a given axis with a given number of steps using one of the predefined step size.

        `stepsize` can range from 1 (smallest) to 20 (largest).
        """
        par=self._move_presets[max(stepsize-1,0)]
        step_dir=1 if steps>0 else -1
        for _ in range(abs(steps)):
            self.move_macrostep(axis,par[0]*step_dir,par[1],par[2])
            self.wait_for_axis(axis)

    _chan_status={  0:"stopped",
                    1:"setting_amplitude",
                    2:"moving",
                    3:"targeting",
                    4:"holding",
                    5:"calibrating",
                    6:"moving_to_reference"}
    def get_status(self, axis):
        """Get the axis status"""
        val=ctypes.c_uint()
        stat=self.dll.SA_GetStatus_S(self.idx,self._get_axis(axis),ctypes.byref(val))
        self._check_status("SA_GetStatus_S",stat)
        if val.value in self._chan_status:
            return self._chan_status[val.value]
        else:
            raise SmarActError("function SA_GetStatus_S returned unknown status: {}".format(val.value))
    def wait_for_axis(self, axis, status="stopped", timeout=3.):
        """
        Wait until the axis reaches a given status.

        By default the status is ``"stopped"`` (i.e., wait until the motion is finished).
        """
        countdown=general.Countdown(timeout)
        while True:
            cur_status=self.get_status(axis)
            if cur_status==status:
                return
            if countdown.passed():
                raise SmarActError("status waiting timed out")
            time.sleep(1E-2)
    def is_moving(self, axis):
        """Check if a given axis is moving"""
        return self.get_status(axis)=="moving"