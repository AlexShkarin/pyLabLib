from .SmarActControl_lib import wlib as lib
from .SmarActControl_lib import nameprops, keyprops, SmarActControlLibError
from .SmarActControl_defs import SA_CTL_ERROR, SA_CTL_MOVE_MODE, SA_CTL_UNIT
from .base import SmarActError
from ...core.utils import general, py3, funcargparse
from ...core.devio import interface
from ..interface import stage

from ..utils import load_lib

import collections
import contextlib
import time


class LibraryController(load_lib.LibraryController):
    pass
libctl=LibraryController(lib)


def list_devices():
    """List all connected SmarAct MCS2 devices"""
    with libctl.temp_open():
        devs=py3.as_str(lib.SA_CTL_FindDevices(""))
        return [d.strip() for d in devs.split("\n") if d.strip()]
def get_devices_number():
    """Get number of connected SmarAct MCS2 controller"""
    return len(list_devices())

def get_SDK_version():
    """Get version of MCS2 SDK"""
    with libctl.temp_open():
        return py3.as_str(lib.SA_CTL_GetFullVersionString())


TDeviceInfo=collections.namedtuple("TDeviceInfo",["serial","name"])
TCLMoveParams=collections.namedtuple("TCLMoveParams",["velocity","acceleration","max_step_frequency","hold_time"])
TStepMoveParams=collections.namedtuple("TStepMoveParams",["frequency","amplitude"])
TScanMoveParams=collections.namedtuple("TScanMoveParams",["velocity"])
class MCS2(stage.IMultiaxisStage):
    """
    SmarAct MCS2 translation stage controller.

    Args:
        locator(str): controller locator (returned by :func:`get_devices_number` function)
    """
    Error=SmarActError
    def __init__(self, locator):
        super().__init__(default_axis=0)
        self.locator=locator
        self.handle=None
        self._opid=None
        self.open()
        self._setup_axes()
        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("properties",self.get_all_properties,priority=-2)
        self._add_status_variable("device_status",self.get_device_status)
        self._add_status_variable("module_status",lambda: self.get_module_status("all"))
        self._add_status_variable("axis_status",lambda: self.get_status("all"))
        self._add_status_variable("position",lambda: self.get_position("all"))
        self._add_status_variable("target_position",lambda: self.get_target_position("all"))
        self._add_status_variable("scan_position",lambda: self.get_scan_position("all"))
        def axis_caller(func, tup=True):
            def wrapped(params):
                return [(func(*p,axis=i) if tup else func(p,axis=i)) for i,p in enumerate(params) if i<self.naxes]
            return wrapped
        self._add_settings_variable("cl_move_parameters",lambda: self.get_cl_move_parameters(axis="all"), axis_caller(self.setup_cl_move))
        self._add_settings_variable("step_move_parameters",lambda: self.get_step_move_parameters(axis="all"), axis_caller(self.setup_step_move))
        self._add_settings_variable("scan_move_parameters",lambda: self.get_scan_move_parameters(axis="all"), axis_caller(self.setup_scan_move))
        self._add_settings_variable("range_limit",lambda: self.get_range_limit(axis="all"), axis_caller(self.set_range_limit,tup=False))
    
    def _get_connection_parameters(self):
        return self.locator
    def open(self):
        """Open the connection to the stage"""
        if self._opid is None:
            with libctl.temp_open():
                self.handle=lib.SA_CTL_Open(self.locator,"")
                self._opid=libctl.open().opid
    def close(self):
        """Close the connection to the stage"""
        if self._opid is not None:
            lib.SA_CTL_Close(self.handle)
            self.handle=None
            libctl.close(self._opid)
            self._opid=None
    def _setup_axes(self):
        with self._close_on_error():
            self.naxes=self.get_property("number_of_channels")
            self._update_axes(list(range(self.naxes)))
            self.nmodules=self.get_property("number_of_bus_modules")
            self._base_units={ax:self.get_property("pos_base_unit",ax) for ax in range(self.naxes)}
    def is_opened(self):
        return self.handle is not None

    def _get_property_by_key(self, key, idx, kind="i32"):
        if kind=="i32":
            return lib.SA_CTL_GetProperty_i32(self.handle,idx,key)
        if kind=="i64":
            return lib.SA_CTL_GetProperty_i64(self.handle,idx,key)
        if kind=="str":
            return py3.as_str(lib.SA_CTL_GetProperty_s(self.handle,idx,key))
        raise ValueError("unrecognized property kind: {}".format(kind))
    def get_property(self, name, idx=0):
        """Get stage property with the given name and index"""
        key,_,kind=nameprops[name]
        return self._get_property_by_key(key,idx,kind)
    def get_all_properties(self, scope="all", idx="all"):
        """
        Get all controller properties within the given scope and for the given index.
        
        `scope` can be ``"dev"`` (device properties), ``"mod"`` (module properties), ``"cha"`` (channel properties), or ``"api"`` (api properties);
        it can also be a list of several scopes, or ``"all"``, which includes all properties.
        `idx` is the index and usually applies to ``"cha"`` or ``"mod"`` scopes; for other scopes it should be set to 0 or ``"all"``.
        """
        if scope=="all":
            scope=["dev","mod","cha","api"]
        elif not isinstance(scope,list):
            scope=[scope]
        for s in scope:
            funcargparse.check_parameter_range(s,"scope",["dev","mod","cha","api"])
        props={}
        nscp={"dev":1,"mod":self.nmodules,"cha":self.naxes,"api":1}
        for key,(name,scp,kind) in keyprops.items():
            if scp not in scope:
                continue
            try:
                if idx=="all":
                    if scp in ["dev","api"]:
                        props[name]=self._get_property_by_key(key,0,kind)
                    else:
                        for i in range(nscp[scp]):
                            props.setdefault(name,{})[i]=self._get_property_by_key(key,i,kind)
                elif idx<nscp[scp]:
                    props[name]=self._get_property_by_key(key,idx,kind)
            except SmarActControlLibError as err:
                if err.code not in [SA_CTL_ERROR.SA_CTL_ERROR_FEATURE_NOT_IMPLEMENTED, SA_CTL_ERROR.SA_CTL_ERROR_FEATURE_NOT_SUPPORTED, SA_CTL_ERROR.SA_CTL_ERROR_PERMISSION_DENIED]:
                    raise
        return props
                
    def _set_property_by_key(self, key, value, idx, kind="i32"):
        if kind=="i32":
            return lib.SA_CTL_SetProperty_i32(self.handle,idx,key,int(value))
        if kind=="i64":
            return lib.SA_CTL_SetProperty_i64(self.handle,idx,key,int(value))
        if kind=="str":
            return lib.SA_CTL_SetProperty_s(self.handle,idx,key,str(value))
        raise ValueError("unrecognized property kind: {}".format(kind))
    def set_property(self, name, value, idx=0):
        """Set stage property with the given name and index"""
        key,_,kind=nameprops[name]
        return self._set_property_by_key(key,value,idx,kind)
    

    def get_device_info(self):
        """
        Get the device info of the controller board.

        Return tuple ``(serial, name)``.
        """
        return TDeviceInfo(self.get_property("device_serial_number"),self.get_property("device_name"))


    def get_default_axis(self):
        """Get the default axis (the one automatically applied to channel-related methods)"""
        return self._default_axis
    def set_default_axis(self, axis):
        """
        Set the default axis (the one automatically applied to channel-related methods).

        Can be a zero-based axis index or ``"all"``
        """
        funcargparse.check_parameter_range(axis,"axis",list(range(self.naxes))+["all"])
        self._default_axis=axis
    @contextlib.contextmanager
    def using_default_axis(self, axis):
        """Context manager for temporarily changing the default axis"""
        dax=self.get_default_axis()
        self.set_default_axis(axis)
        try:
            yield
        finally:
            self.set_default_axis(dax)
    _axis_status_bits={ "moving":0x0001,"closed_loop":0x0002,"calibrating":0x004,"referencing":0x0008,
                        "move_delayed":0x0010,"sensor_present":0x0020,"calibrated":0x0040,"referenced":0x0080,
                        "end_stop_reached":0x0100,"range_limit_reached":0x0200,"following_limit_reached":0x0400,
                        "move_failed":0x0800,"streaming":0x1000,"over_temperature":0x400,"reference_mark":0x8000}
    _moving_status_bits=0x0001|0x0004|0x0008
    @stage.muxaxis
    def get_status_n(self, axis=None):
        """Get axis status as an integer"""
        return self.get_property("channel_state",axis)
    @stage.muxaxis
    def get_status(self, axis=None):
        """Get axis status as a set of string descriptors"""
        statn=self.get_property("channel_state",axis)
        return [k for k,m in self._axis_status_bits.items() if statn&m]
    @stage.muxaxis
    def is_moving(self, axis=None):
        """Check if a given axis is moving (including referencing and calibrating)"""
        return bool(self.get_property("channel_state",axis)&self._moving_status_bits)
    def wait_move(self, axis, timeout=30.):
        """Wait for a given axis to stop moving"""
        if axis=="all":
            for ax in self.get_all_axes():
                self.wait_move(ax,timeout=timeout)
            return
        countdown=general.Countdown(timeout)
        while True:
            if not self.get_property("channel_state",axis)&self._moving_status_bits:
                return
            if countdown.passed():
                raise SmarActError("waiting timed out")
            time.sleep(1E-2)

    _dev_status_bits={ "hm_present":0x0001,"movement_locked":0x0002,"internal_comm_failure":0x0100,"streaming":0x1000}
    def get_device_status_n(self):
        """Get device status as an integer"""
        return self.get_property("device_state")
    def get_device_status(self):
        """Get axis status as a set of string descriptors"""
        statn=self.get_property("device_state")
        return [k for k,m in self._dev_status_bits.items() if statn&m]
    _mod_status_bits={ "sm_present":0x0001,"booster_present":0x0002,"adj_active":0x0004,"iom_present":0x0008,
                        "internal_comm_failure":0x0100,"high_voltage_failure":0x1000,"high_voltage_overload":0x2000,"over_temperature":0x4000}
    def get_module_status_n(self, index=0):
        """Get module status as an integer"""
        if index=="all":
            return [self.get_module_status_n(i) for i in range(self.nmodules)]
        return self.get_property("module_state",index)
    def get_module_status(self, index):
        """Get module status as a set of string descriptors"""
        if index=="all":
            return [self.get_module_status(i) for i in range(self.nmodules)]
        statn=self.get_property("module_state",index)
        return [k for k,m in self._mod_status_bits.items() if statn&m]
    
    def _p2d(self, value, axis, avoid_zero=False):
        u=self._base_units[axis]
        if u==SA_CTL_UNIT.SA_CTL_UNIT_METER:
            dvalue=int(value/1E-12)
        elif u==SA_CTL_UNIT.SA_CTL_UNIT_DEGREE:
            dvalue=int(value/1E-9)
        else:
            raise ValueError("unrecognized axis units: {}".format(u))
        if avoid_zero and value!=0:
            dvalue=max(dvalue,1)
        return dvalue
    def _d2p(self, value, axis):
        u=self._base_units[axis]
        if u==SA_CTL_UNIT.SA_CTL_UNIT_METER:
            return value*1E-12
        if u==SA_CTL_UNIT.SA_CTL_UNIT_DEGREE:
            return value*1E-9
        raise ValueError("unrecognized axis units: {}".format(u))
    
    @stage.muxaxis
    def get_cl_move_parameters(self, axis=None):
        """
        Get closed-loop move parameters.

        Return tuple ``(velocity, acceleration, max_step_frequency, hold_time)`` with the maximal move velocity (in m/s or deg/s),
        move acceleration (in m/s^2 or deg/s^2), maximal step frequency (in Hz), and position hold time (in s, or ``"inf"`` if it is infinite)
        """
        velocity=self._d2p(self.get_property("move_velocity",axis),axis)
        acceleration=self._d2p(self.get_property("move_acceleration",axis),axis)
        max_step_frequency=self.get_property("max_cl_frequency",axis)
        hold_time=self.get_property("hold_time",axis)
        hold_time=(hold_time%2**32)/1E3 if hold_time>=0 else "inf"
        return TCLMoveParams(velocity,acceleration,max_step_frequency,hold_time)
    @stage.muxaxis(mux_argnames=["velocity","acceleration","max_step_frequency","hold_time"])
    def setup_cl_move(self, velocity=None, acceleration=None, max_step_frequency=None, hold_time=None, axis=None):
        """
        Set closed-loop move parameters.

        For the meaning of the parameters, see :meth:`get_cl_move_parameters`.
        Note that changing the hold time will only apply after the next move command.
        To apply it without actual moving, you can call :meth:`move_by` method with ``distance=0`` for the appropriate axis.
        If any parameter is ``None``, use the current value.
        """
        if velocity is not None:
            self.set_property("move_velocity",self._p2d(velocity,axis,avoid_zero=True),axis)
        if acceleration is not None:
            self.set_property("move_acceleration",self._p2d(acceleration,axis,avoid_zero=True),axis)
        if max_step_frequency is not None:
            self.set_property("max_cl_frequency",max_step_frequency,axis)
        if hold_time is not None:
            hold_time=-1 if hold_time=="inf" or hold_time<0 else min(int(hold_time*1E3),2**31)
            self.set_property("hold_time",hold_time,axis)
        return self.get_cl_move_parameters(axis)
    @stage.muxaxis
    def get_step_move_parameters(self, axis=None):
        """
        Get step move parameters.

        Return tuple ``(frequency, amplitude)`` with the step frequency (in Hz) and step amplitude (normalized between 0 and 1).
        """
        frequency=self.get_property("step_frequency",axis)
        amplitude=self.get_property("step_amplitude",axis)/65535
        return TStepMoveParams(frequency,amplitude)
    @stage.muxaxis(mux_argnames=["frequency","amplitude"])
    def setup_step_move(self, frequency=None, amplitude=None, axis=None):
        """
        Set step move parameters.

        For the meaning of the parameters, see :meth:`get_step_move_parameters`.
        If any parameter is ``None``, use the current value.
        """
        if frequency is not None:
            self.set_property("step_frequency",int(frequency),axis)
        if amplitude is not None:
            self.set_property("step_amplitude",max(1,min(int(amplitude*65535),65535)),axis)
        return self.get_step_move_parameters(axis)
    @stage.muxaxis
    def get_scan_move_parameters(self, axis=None):
        """
        Get scan move parameters.

        Return tuple ``(velocity)`` with the move velocity (amplitude per second; amplitude is normalized between 0 and 1).
        """
        velocity=self.get_property("scan_velocity",axis)/65535
        return TScanMoveParams(velocity)
    @stage.muxaxis(mux_argnames=["velocity"])
    def setup_scan_move(self, velocity=None, axis=None):
        """
        Set scan move parameters.

        For the meaning of the parameters, see :meth:`get_scan_move_parameters`.
        If any parameter is ``None``, use the current value.
        """
        if velocity is not None:
            self.set_property("step_amplitude",max(1,min(int(velocity*65535),65535)),axis)
        return self.get_scan_move_parameters(axis)
    @stage.muxaxis
    def get_range_limit(self, axis=None):
        """
        Get the movement range limit (in m or deg) for the given axis.
        
        Return ``(min, max)`` if the limit is active or ``None`` otherwise.
        """
        minlim=self._d2p(self.get_property("range_limit_min",axis),axis)
        maxlim=self._d2p(self.get_property("range_limit_max",axis),axis)
        return (minlim,maxlim) if minlim<maxlim else None
    @stage.muxaxis(mux_argnames=["limit"])
    def set_range_limit(self, limit, axis=None):
        """
        Set the movement range limit (in m or deg) for the given axis.
        
        `limit` is either a tuple ``(min, max)`` if the limit is active, or ``None`` otherwise.
        """
        if limit is None:
            # minlim=self.get_property("range_limit_min",axis)
            # self.set_property("range_limit_max",minlim,axis)
            self.set_property("range_limit_min",0,axis)
            self.set_property("range_limit_max",0,axis)
        else:
            minlim,maxlim=min(limit),max(limit)
            self.set_property("range_limit_min",self._p2d(minlim,axis),axis)
            self.set_property("range_limit_max",self._p2d(maxlim,axis),axis)
        return self.get_range_limit(axis)


    @stage.muxaxis
    def get_position(self, axis=None):
        """Get current position (in m or deg) at the given axis"""
        try:
            return self._d2p(self.get_property("position",axis),axis)
        except SmarActControlLibError as err:
            if err.code not in [SA_CTL_ERROR.SA_CTL_ERROR_NO_SENSOR_PRESENT,SA_CTL_ERROR.SA_CTL_ERROR_SENSOR_DISABLED]:
                raise
    @stage.muxaxis(mux_argnames=["position"])
    def set_position_reference(self, position=0, axis=None):
        """
        Get the current position (in m or deg) at the given axis.
        
        This method simply shifts the position sensor reference; the stage does not move.
        """
        try:
            self.set_property("position",self._p2d(position,axis),axis)
            return self.get_position(axis)
        except SmarActControlLibError as err:
            if err.code not in [SA_CTL_ERROR.SA_CTL_ERROR_NO_SENSOR_PRESENT,SA_CTL_ERROR.SA_CTL_ERROR_SENSOR_DISABLED]:
                raise
    @stage.muxaxis
    def get_scan_position(self, axis=None):
        """Get current scan position (piezo voltage; normalized between 0 and 1) at the given axis"""
        return self.get_property("scan_position",axis)/65535
    @stage.muxaxis
    def get_target_position(self, axis=None):
        """Get current target position (in m or deg) at the given axis"""
        try:
            return self._d2p(self.get_property("target_position",axis),axis)
        except SmarActControlLibError as err:
            if err.code not in [SA_CTL_ERROR.SA_CTL_ERROR_NO_SENSOR_PRESENT,SA_CTL_ERROR.SA_CTL_ERROR_SENSOR_DISABLED]:
                raise
    @stage.muxaxis(mux_argnames=["position"])
    def move_to(self, position, axis=None):
        """Move to the given position (in m or deg) at the given axis"""
        self.set_property("move_mode",SA_CTL_MOVE_MODE.SA_CTL_MOVE_MODE_CL_ABSOLUTE,axis)
        lib.SA_CTL_Move(self.handle,axis,self._p2d(position,axis),0)
    @stage.muxaxis(mux_argnames=["distance"])
    def move_by(self, distance, axis=None):
        """Move by the given distance (in m or deg) at the given axis"""
        self.set_property("move_mode",SA_CTL_MOVE_MODE.SA_CTL_MOVE_MODE_CL_RELATIVE,axis)
        lib.SA_CTL_Move(self.handle,axis,self._p2d(distance,axis),0)
    @stage.muxaxis(mux_argnames=["steps"])
    def move_by_steps(self, steps, axis=None):
        """Move by the given number of steps at the given axis"""
        self.set_property("move_mode",SA_CTL_MOVE_MODE.SA_CTL_MOVE_MODE_STEP,axis)
        lib.SA_CTL_Move(self.handle,axis,int(steps),0)
    @stage.muxaxis(mux_argnames=["position"])
    def move_scan_to(self, position, axis=None):
        """Move to the given open-loop position (piezo voltage; normalized between 0 and 1) using just a piezo deflection at the given axis"""
        self.set_property("move_mode",SA_CTL_MOVE_MODE.SA_CTL_MOVE_MODE_SCAN_ABSOLUTE,axis)
        lib.SA_CTL_Move(self.handle,axis,max(0,min(int(position*65535),65535)),0)
    @stage.muxaxis(mux_argnames=["distance"])
    def move_scan_by(self, distance, axis=None):
        """Move by the given open-loop distance (piezo voltage; normalized between -1 and 1) using just a piezo deflection at the given axis"""
        self.set_property("move_mode",SA_CTL_MOVE_MODE.SA_CTL_MOVE_MODE_SCAN_RELATIVE,axis)
        lib.SA_CTL_Move(self.handle,axis,max(-65535,min(int(distance*65535),65535)),0)
    @stage.muxaxis
    def stop(self, axis=None):
        """Stop motion at the given axis"""
        lib.SA_CTL_Stop(self.handle,axis,0)
    
    @stage.muxaxis
    @interface.use_parameters(start_direction="direction")
    def home(self, axis=None, sync=True, start_direction="+", reverse_direction=False, abort_on_stop=False, auto_zero=False, continue_on_found=False, stop_on_found=False):
        """
        Home (reference) the given axis.
        
        If ``sync==True``, wait until the homing is done.
        The other parameters are flags setting up the referencing behavior. See MCS2 programming manual section on reference marks for the details.
        """
        ropt=0
        for v,m in [(not start_direction,0x01),(reverse_direction,0x02),(abort_on_stop,0x04),(auto_zero,0x08),(continue_on_found,0x10),(stop_on_found,0x20)]:
            if v:
                ropt|=m
        self.set_property("referencing_options",ropt,axis)
        lib.SA_CTL_Reference(self.handle,axis,0)
        if sync:
            self.wait_move(axis,timeout=60.)
    @stage.muxaxis
    @interface.use_parameters(direction="direction")
    def calibrate(self, axis=None, sync=True, direction="+", detect_code_inversion=False, advanced_sensor_correction=False, limited_stage_range=False):
        """
        Calibrate the given axis.
        
        If ``sync==True``, wait until the calibration is done.
        The other parameters are flags setting up the calibration behavior. See MCS2 programming manual section on calibrating for the details.
        """
        copt=0
        for v,m in [(not direction,0x01),(detect_code_inversion,0x02),(advanced_sensor_correction,0x04),(limited_stage_range,0x100)]:
            if v:
                copt|=m
        self.set_property("calibrating_options",copt,axis)
        lib.SA_CTL_Calibrate(self.handle,axis,0)
        if sync:
            self.wait_move(axis,timeout=60.)

    
    @stage.muxaxis(mux_argnames=["value"])
    def lowlevel_move(self, value, axis=None):
        """
        Execute the low-level movement command with the given integer value.
        
        The meaning of the value depends on the devices properties (see MCS2 programming manual for the details).
        This is a low-level method, whose high-level functionality is covered by other move methods.
        """
        lib.SA_CTL_Move(self.handle,axis,int(value),0)
    @stage.muxaxis
    def lowlevel_reference(self, axis=None):
        """
        Execute the low-level reference command with the given integer value.
        
        Exact procedure depends on the devices properties (see MCS2 programming manual for the details).
        This is a low-level method, whose high-level functionality is covered by the :meth:`home` method.
        """
        lib.SA_CTL_Reference(self.handle,axis,0)
    @stage.muxaxis
    def lowlevel_calibrate(self, axis=None):
        """
        Execute the low-level calibration command with the given integer value.
        
        Exact procedure depends on the devices properties (see MCS2 programming manual for the details).
        This is a low-level method, whose high-level functionality is covered by the :meth:`calibrate` method.
        """
        lib.SA_CTL_Calibrate(self.handle,axis,0)