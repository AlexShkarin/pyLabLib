from .misc import default_placing_message, load_lib
from ...core.utils import py3
from ...core.devio.interface import IDevice

import os.path
import ctypes
import time
import sys
import struct

class ArcusError(RuntimeError):
    """Generic Arcus error."""

HANDLE=ctypes.c_void_p
BOOL=ctypes.c_int
DWORD=ctypes.c_int

class GenericPerformaxStage(IDevice):
    """
    Generic Arcus Performax translation stage.

    Args:
        lib_path(str): path to the PerformaxCom.dll (default is to use the library supplied with the package)
        idx(int): stage index
    """
    _default_operation_cooldown=0.01
    def __init__(self, lib_path=None, idx=0):
        IDevice.__init__(self)
        self._operation_cooldown=self._default_operation_cooldown
        self.dll=self._load_dll(lib_path=lib_path)
        self.dll.fnPerformaxComOpen.argtypes=[DWORD,ctypes.c_char_p]
        self.dll.fnPerformaxComOpen.restype=BOOL
        self.dll.fnPerformaxComClose.argtypes=[HANDLE]
        self.dll.fnPerformaxComClose.restype=BOOL
        self.dll.fnPerformaxComSendRecv.argtypes=[HANDLE,ctypes.c_char_p,DWORD,DWORD,ctypes.c_char_p]
        self.dll.fnPerformaxComSendRecv.restype=BOOL
        self.dll.fnPerformaxComSetTimeouts.argtypes=[DWORD,DWORD]
        self.dll.fnPerformaxComSetTimeouts.restype=BOOL
        self.dll.fnPerformaxComFlush.argtypes=[HANDLE]
        self.dll.fnPerformaxComFlush.restype=BOOL
        self.dll.fnPerformaxComGetProductString.argtypes=[DWORD,ctypes.c_char_p,DWORD]
        self.dll.fnPerformaxComGetProductString.restype=BOOL
        self.idx=idx
        self.handle=None
        self.rbuff=ctypes.create_string_buffer(65536)
        self.open()
        self._add_full_info_node("device_id",self.get_device_id)


    @staticmethod
    def _load_dll(lib_path=None):
        error_message="The library is supplied on on Arcus website;\nAdditional required library: SiUSBXp.dll\n{}".format(default_placing_message)
        if lib_path is None:
            return load_lib("PerformaxCom.dll",locations=("local","global"),call_conv="stdcall",locally=True,error_message=error_message)
        else:
            return load_lib(lib_path,call_conv="stdcall",locally=True,error_message=error_message)
    @staticmethod
    def get_devices_num(lib_path=None):
        """Get number of connected Arcus devices"""
        ndev=DWORD(0)
        dll=GenericPerformaxStage._load_dll(lib_path=lib_path)
        dll.fnPerformaxComGetNumDevices.argtypes=[ctypes.POINTER(DWORD)]
        dll.fnPerformaxComGetNumDevices.restype=BOOL
        dll.fnPerformaxComGetNumDevices(ctypes.byref(ndev))
        return ndev.value
    def open(self):
        """Open the connection to the stage"""
        self.close()
        self.dll.fnPerformaxComSetTimeouts(5000,5000)
        phandle=ctypes.create_string_buffer(b"\x00"*8)
        hlen=ctypes.sizeof(ctypes.c_void_p)
        for _ in range(5):
            code=self.dll.fnPerformaxComOpen(DWORD(int(self.idx)),phandle)
            if code:
                self.handle=struct.unpack("P",phandle.raw[:hlen])[0]
                self.dll.fnPerformaxComFlush(self.handle)
                return
            time.sleep(0.3)
        raise ArcusError("can't connect to the stage with index {}, return code {}".format(self.idx,code))
    def close(self):
        """Close the connection to the stage"""
        if self.handle:
            for _ in range(5):
                if self.dll.fnPerformaxComClose(self.handle):
                    self.handle=None
                    return
                time.sleep(0.3)
            raise ArcusError("can't disconnect from the stage with index {}".format(self.idx))
    def is_opened(self):
        return self.handle is not None
    def _check_handle(self):
        if self.handle is None:
            raise ArcusError("device is not opened")

    def get_device_id(self):
        """Get the device ID"""
        devs=[]
        for n in range(5):
            time.sleep(self._operation_cooldown)
            if not self.dll.fnPerformaxComGetProductString(self.idx,self.rbuff,n):
                raise ArcusError("can't get info for the device with index {}".format(self.idx))
            devs.append(py3.as_str(self.rbuff.value))
        return devs
    def query(self, comm):
        """Send a query to the stage and return the reply"""
        self._check_handle()
        time.sleep(self._operation_cooldown)
        comm=py3.as_builtin_bytes(comm)+b"\x00"
        if self.dll.fnPerformaxComSendRecv(self.handle,comm,len(comm),64,self.rbuff):
            return py3.as_str(self.rbuff.value)
        else:
            raise ArcusError("error sending command {}".format(comm))


class Performax4EXStage(GenericPerformaxStage):
    """
    Arcus Performax 4EX translation stage.

    Args:
        lib_path(str): path to the PerformaxCom.dll (default is to use the library supplied with the package)
        idx(int): stage index
    """
    def __init__(self, lib_path=None, idx=0):
        GenericPerformaxStage.__init__(self,lib_path=lib_path,idx=idx)
        self.set_absolute_mode()
        self.enable_all_outputs()
        self.ignore_limit_errors()
        self._add_settings_node("ignore_limit_errors",self.is_ignoring_limit_errors,self.ignore_limit_errors)
        self._add_status_node("positions",self.get_position,mux=("XYZU",))
        self._add_settings_node("global_speed",self.get_speed,self.set_speed)
        self._add_settings_node("axis_speed",self.get_axis_speed,self.set_axis_speed,mux=("XYZU",0))
        self._add_status_node("axis_status",self.get_status,mux=("XYZU",0))
        self._add_status_node("moving",self.is_moving,mux=("XYZU",0))

    @staticmethod
    def _check_axis(axis):
        if axis.lower() not in ["x","y","z","u"]:
            raise ArcusError("unrecognized axis: {}".format(axis))
        return axis.upper()

    def set_absolute_mode(self):
        """Set absolute motion mode"""
        self.query("ABS")
    def ignore_limit_errors(self, do_ignore=True):
        """
        Switch ignoring limit errors on or off.

        If on, limit error on one axis doesn't stop other axes.
        """
        self.query("IERR={}".format("1" if do_ignore else "0"))
    def is_ignoring_limit_errors(self):
        """
        Check if ignoring limit errors is on.

        If on, limit error on one axis doesn't stop other axes.
        """
        return self.query("IERR")=="1"
    def enable_output(self, axis, enable=True):
        """
        Enable axis output.

        If the output is disabled, the steps are generated by the controller, but not sent to the motors.
        """
        axis=self._check_axis(axis)
        axisn="XYZU".index(axis)+1
        self.query("EO{}={}".format(axisn,"1" if enable else "0"))
    def enable_all_outputs(self, enable=True):
        """Enable output on all axes"""
        self.query("EO={}".format("15" if enable else "0"))
        for axis in "xyzu":
            self.enable_output(axis,enable=enable)

    def get_position(self, axis):
        """Get the current axis position"""
        axis=self._check_axis(axis)
        return int(self.query("P"+axis))
    def set_position_reference(self, axis, position=0):
        """
        Set the current axis position as a reference.
        
        Re-calibrate the position encoder so that the current position is set as `position` (0 by default).
        """
        axis=self._check_axis(axis)
        self.query("P{}={:.0f}".format(axis,position))
    def move_to(self, axis, position):
        """Move a given axis to a given position"""
        axis=self._check_axis(axis)
        self.query("{}{:.0f}".format(axis,position))
    def move(self, axis, steps=1):
        """Move a given axis for a given number of steps"""
        self.move_to(axis,self.get_position(axis)+steps)
    def jog(self, axis, direction):
        """
        Jog a given axis in a given direction.
        
        `direction` can be either ``"-"`` (negative) or ``"+"`` (positive).
        The motion continues until it is explicitly stopped, or unitl a limit is hit.
        """
        axis=self._check_axis(axis)
        if not direction: # 0 or False also mean left
            direction="-"
        if direction in [1, True]:
            direction="+"
        if direction not in ["+","-"]:
            raise ArcusError("unrecognized direction: {}".format(direction))
        self.query("J{}{}".format(axis,direction))
    def stop(self, axis):
        """Stop motion of a given axis"""
        axis=self._check_axis(axis)
        self.query("STOP"+axis)
    def stop_all(self):
        """Stop motion of all axes"""
        for axis in "XYZU":
            self.query("STOP"+axis)

    def get_speed(self):
        """Get the global speed setting (in Hz)"""
        return int(self.query("HS"))
    def get_axis_speed(self, axis):
        """Get the individual axis speed setting (in Hz)"""
        axis=self._check_axis(axis)
        return int(self.query("HS"+axis))
    def set_speed(self, speed):
        """Set the global speed setting (in Hz)"""
        self.query("HS={:.0f}".format(speed))
    def set_axis_speed(self, axis, speed):
        """Set the individual axis speed setting (in Hz)"""
        axis=self._check_axis(axis)
        self.query("HS{}={:.0f}".format(axis,speed))

    _status_bits={  "accel":0x001,"decel":0x002,"moving":0x004,
                    "alarm":0x008,
                    "sw_plus_lim":0x010,"sw_minus_lim":0x020,"sw_home":0x040,
                    "err_plus_lim":0x080,"err_minus_lim":0x100,"err_alarm":0x200,
                    "TOC_timeout":0x800}
    def _get_full_status(self):
        stat=self.query("MST")
        return [int(x) for x in stat.split(":") if x]
    def get_status_n(self, axis):
        """Get the axis status as an integer"""
        axis=self._check_axis(axis)
        axis_n="XYZU".index(axis)
        return self._get_full_status()[axis_n]
    def get_status(self, axis):
        """Get the axis status as a set of string descriptors"""
        statn=self.get_status_n(axis)
        return [ k for k in self._status_bits if self._status_bits[k]&statn ]
    def is_moving(self, axis):
        """Check if a given axis is moving"""
        return bool(self.get_status_n(axis)&0x007)

    def check_limit_error(self, axis):
        """
        Check if the axis hit limit errors.

        Return ``""`` (not errors), ``"+"`` (positive limit error) or ``"-"`` (negative limit error).
        """
        stat=self.get_status_n(axis)
        err=""
        if stat&self._status_bits["err_plus_lim"]:
            err=err+"+"
        if stat&self._status_bits["err_minus_lim"]:
            err=err+"-"
        return err
    def clear_limit_error(self, axis):
        """Clear axis limit errors"""
        axis=self._check_axis(axis)
        self.query("CLR"+axis)

PerformaxStage=Performax4EXStage # for backwards compatibility