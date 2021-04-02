from . import ArcusPerformaxDriver_lib
from ...core.utils import py3, general
from ...core.devio import interface
from ..interface import stage

import time



class ArcusError(RuntimeError):
    """Generic Arcus error"""


def get_device_info(devid):
    """
    Get info for the given device index (starting from 0).

    Return tuple ``()``.
    """
    lib=ArcusPerformaxDriver_lib.lib
    lib.initlib()
    ndev=lib.fnPerformaxComGetNumDevices()
    if devid>=ndev:
        raise ArcusError("device with index {} doesn't exist; there are {} devices".format(devid,ndev))
    return tuple([devid]+[py3.as_str(lib.fnPerformaxComGetProductString(devid,i)) for i in range(5)])
def list_performax_devices():
    """
    List all performax devices.

    Return list of tuples ``()``, one per device.
    """
    lib=ArcusPerformaxDriver_lib.lib
    lib.initlib()
    ndev=lib.fnPerformaxComGetNumDevices()
    return [get_device_info(d) for d in range(ndev)]


class GenericPerformaxStage(stage.IStage,interface.IDevice):
    """
    Generic Arcus Performax translation stage.

    Args:
        idx(int): stage index
    """
    _default_operation_cooldown=0.01
    def __init__(self, idx=0):
        super().__init__()
        self._operation_cooldown=self._default_operation_cooldown
        self.lib=ArcusPerformaxDriver_lib.lib
        self.lib.initlib()
        self.idx=idx
        self.handle=None
        self.open()
        self._add_info_variable("device_info",self.get_device_info)


    def open(self):
        """Open the connection to the stage"""
        self.close()
        self.lib.fnPerformaxComSetTimeouts(5000,5000)
        for _ in range(5):
            try:
                self.handle=self.lib.fnPerformaxComOpen(self.idx)
                self.lib.fnPerformaxComFlush(self.handle)
                return
            except ArcusPerformaxDriver_lib.ArcusPerformaxLibError:
                time.sleep(0.3)
        raise ArcusError("can't connect to the stage with index {}".format(self.idx))
    def close(self):
        """Close the connection to the stage"""
        if self.handle:
            for _ in range(5):
                try:
                    self.lib.fnPerformaxComClose(self.handle)
                    self.handle=None
                    return
                except ArcusPerformaxDriver_lib.ArcusPerformaxLibError:
                    time.sleep(0.3)
            raise ArcusError("can't disconnect from the stage with index {}".format(self.idx))
    def is_opened(self):
        return self.handle is not None
    def _check_handle(self):
        if self.handle is None:
            raise ArcusError("device is not opened")

    def get_device_info(self):
        """Get the device info"""
        return get_device_info(self.idx)
    def query(self, comm):
        """Send a query to the stage and return the reply"""
        self._check_handle()
        time.sleep(self._operation_cooldown)
        scomm=py3.as_builtin_bytes(comm)+b"\x00"
        try:
            reply=py3.as_str(self.lib.fnPerformaxComSendRecv(self.handle,scomm))
            if reply.startswith("?"):
                raise ArcusError("device returned error: {}".format(reply[1:]))
            return reply
        except ArcusPerformaxDriver_lib.ArcusPerformaxLibError:
            raise ArcusError("error sending device query {}".format(comm))




class Performax4EXStage(GenericPerformaxStage):
    """
    Arcus Performax 4EX translation stage.

    Args:
        idx(int): stage index
        enable: if ``True``, enable all axes on startup
    """
    _axes=list("XYZU")
    _speed_comm="HS"
    def __init__(self, idx=0, enable=True):
        super().__init__()
        self._add_parameter_class(interface.EnumParameterClass("axis",self._axes,value_case="upper"))
        self.enable_absolute_mode()
        if enable:
            self.enable_all()
        self.enable_global_limit_errors(False)
        self._add_settings_variable("global_limit_errors",self.global_limit_errors_enabled,self.enable_global_limit_errors)
        self._add_status_variable("position",self.get_position,mux=(self._axes,))
        self._add_status_variable("encoder",self.get_encoder,mux=(self._axes,))
        self._add_settings_variable("enabled",self.is_enabled,self.enable,mux=(self._axes,))
        self._add_settings_variable("global_speed",self.get_global_speed,self.set_global_speed)
        self._add_settings_variable("axis_speed",self.get_axis_speed,self.set_axis_speed,mux=(self._axes,))
        self._add_status_variable("axis_status",self.get_status,mux=(self._axes,))
        self._add_status_variable("moving",self.is_moving,mux=(self._axes,))
        self._add_status_variable("digital_input",self.get_digital_input_register,priority=-2)
        self._add_settings_variable("digital_output",self.get_digital_output_register,priority=-2)
        self._add_settings_variable("analog_input",self.get_analog_input,priority=-2,mux=(range(1,9),))

    def enable_absolute_mode(self, enable=True):
        """Set absolute motion mode"""
        self.query("ABS" if enable else "REL")
    def enable_global_limit_errors(self, enable=True):
        """
        Enable global limit errors.

        If on, reaching limit on one axis raises an error and stop other axes; otherwise, the limited axis still stops, but the other axes are unaffected.
        """
        self.query("IERR={}".format(0 if enable else 1))
    def global_limit_errors_enabled(self):
        """
        Check if global limit errors are enabled.

        If on, reaching limit on one axis raises an error and stop other axes; otherwise, the limited axis still stops, but the other axes are unaffected.
        """
        return not bool(int(self.query("IERR")))
    
    def _axisn(self, axis):
        return self._axes.index(axis)+1
    @interface.use_parameters
    def is_enabled(self, axis):
        """Check if the axis output is enabled"""
        return bool(int(self.query("EO{}".format(self._axisn(axis)))))
    @interface.use_parameters
    def enable(self, axis, enable=True):
        """
        Enable axis output.

        If the output is disabled, the steps are generated by the controller, but not sent to the motors.
        """
        self.query("EO{}={}".format(self._axisn(axis),1 if enable else 0))
    def enable_all(self, enable=True):
        """Enable output on all axes"""
        self.query("EO={}".format(2**len(self._axes)-1 if enable else 0))
        for axis in self._axes:
            self.enable(axis,enable=enable)

    @interface.use_parameters
    def get_position(self, axis):
        """Get the current axis pulse position"""
        return int(self.query("P"+axis))
    @interface.use_parameters
    def set_position_reference(self, axis, position=0):
        """
        Set the current axis pulse position as a reference.
        
        Re-calibrate the pulse position counter so that the current position is set as `position` (0 by default).
        """
        self.query("P{}={:.0f}".format(axis,position))
    @interface.use_parameters
    def get_encoder(self, axis):
        """Get the current axis encoder value"""
        return int(self.query("E"+axis))
    @interface.use_parameters
    def set_encoder_reference(self, axis, position=0):
        """
        Set the current axis encoder value as a reference.
        
        Re-calibrate the encoder counter so that the current position is set as `position` (0 by default).
        """
        self.query("E{}={:.0f}".format(axis,position))
    @interface.use_parameters
    def move_to(self, axis, position):
        """Move a given axis to a given position"""
        self.query("{}{:.0f}".format(axis,position))
    def move_by(self, axis, steps=1):
        """Move a given axis for a given number of steps"""
        self.move_to(axis,self.get_position(axis)+steps)
    _p_direction=interface.EnumParameterClass("direction",[("+",True),(1,True),("-",False),(0,False)])
    @interface.use_parameters
    def jog(self, axis, direction):
        """
        Jog a given axis in a given direction.
        
        `direction` can be either ``"-"`` (negative) or ``"+"`` (positive).
        The motion continues until it is explicitly stopped, or until a limit is hit.
        """
        self.query("J{}{}".format(axis,"+" if direction else "-"))
    @interface.use_parameters
    def stop(self, axis):
        """Stop motion of a given axis"""
        self.query("STOP"+axis)
    def stop_all(self):
        """Stop motion of all axes"""
        for axis in self._axes:
            self.query("STOP"+axis)

    _p_home_mode=interface.EnumParameterClass("home_mode",{"only_home_input":0,"only_limit_input":1,"home_and_zidx_input":2,"only_zidx_input":3,"only_home_input_lowspeed":4})
    @interface.use_parameters
    def home(self, axis, direction, home_mode):
        """
        Home the given axis using a given home mode.

        The mode can be ``"only_home_input"``, ``"only_home_input_lowspeed"``, ``"only_limit_input"``, ``"only_zidx_input"``, or ``"home_and_zidx_input"``.
        For meaning, see Arcus PMX-4EX manual.
        """
        self.query("H{}{}{}".format(axis,direction,home_mode))

    def get_global_speed(self):
        """Get the global speed setting (in Hz); overridden by a non-zero axis speed"""
        return int(self.query(self._speed_comm))
    @interface.use_parameters
    def get_axis_speed(self, axis):
        """Get the individual axis speed setting (in Hz); 0 means that the global speed is used"""
        return int(self.query(self._speed_comm+axis))
    def set_global_speed(self, speed):
        """Set the global speed setting (in Hz); overridden by a non-zero axis speed"""
        self.query("{}={:.0f}".format(self._speed_comm,speed))
    @interface.use_parameters
    def set_axis_speed(self, axis, speed):
        """Set the individual axis speed setting (in Hz); 0 means that the global speed is used"""
        self.query("{}{}={:.0f}".format(self._speed_comm,axis,speed))

    _status_bits={  "accel":0x001,"decel":0x002,"moving":0x004,
                    "alarm":0x008,
                    "sw_plus_lim":0x010,"sw_minus_lim":0x020,"sw_home":0x040,
                    "err_plus_lim":0x080,"err_minus_lim":0x100,"err_alarm":0x200,
                    "TOC_timeout":0x800}
    def _get_full_status(self):
        stat=self.query("MST")
        return [int(x) for x in stat.split(":") if x]
    @interface.use_parameters
    def get_status_n(self, axis):
        """Get the axis status as an integer"""
        return self._get_full_status()[self._axisn(axis)]
    def get_status(self, axis):
        """Get the axis status as a set of string descriptors"""
        statn=self.get_status_n(axis)
        return [ k for k in self._status_bits if self._status_bits[k]&statn ]
    def is_moving(self, axis):
        """Check if a given axis is moving"""
        return bool(self.get_status_n(axis)&0x007)
    def wait_move(self, axis, timeout=None, period=0.05):
        """Wait until motion is done"""
        ctd=general.Countdown(timeout)
        while True:
            if not self.is_moving(axis):
                return
            if ctd.passed():
                raise ArcusError("waiting for motion on axis {} caused a timeout".format(axis))
            time.sleep(period)

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
    @interface.use_parameters
    def clear_limit_error(self, axis):
        """Clear axis limit errors"""
        self.query("CLR"+axis)

    def get_analog_input(self, channel):
        """Get voltage (in V) at a given input (1 through 8)"""
        return int(self.query("AI{}".format(channel)))*1E-3
    def get_digital_input(self, channel):
        """Get value (0 or 1) at a given digital input (1 through 8)"""
        return int(self.query("DI{}".format(channel)))
    def get_digital_input_register(self):
        """Get all 8 digital inputs as a single 8-bit integer"""
        return int(self.query("DI"))
    def get_digital_output(self, channel):
        """Get value (0 or 1) at a given digital output (1 through 8)"""
        return int(self.query("DO{}".format(channel)))
    def get_digital_output_register(self):
        """Get all 8 digital inputs as a single 8-bit integer"""
        return int(self.query("DO"))
    def set_digital_output(self, channel, value):
        """Set value (0 or 1) at a given digital output (1 through 8)"""
        self.query("DO{}={}".format(channel,1 if value else 0))
        return self.get_digital_output(channel)
    def set_digital_output_register(self, value):
        """Set all 8 digital inputs as a single 8-bit integer"""
        self.query("DO={}".format(int(value)))
        return self.get_digital_output_register()