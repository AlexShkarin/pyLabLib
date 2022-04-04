from .ArcusPerformaxDriver_lib import wlib as lib, ArcusPerformaxLibError
from .base import ArcusError, ArcusBackendError
from ...core.utils import py3, general
from ...core.devio import interface, comm_backend
from ..interface import stage

import time





def get_usb_device_info(devid):
    """
    Get info for the given device index (starting from 0).

    Return tuple ``(index, serial, model, desc, vid, pid)``.
    """
    lib.initlib()
    ndev=lib.fnPerformaxComGetNumDevices()
    if devid>=ndev:
        raise ArcusError("device with index {} doesn't exist; there are {} devices".format(devid,ndev))
    return tuple([devid]+[py3.as_str(lib.fnPerformaxComGetProductString(devid,i)) for i in range(5)])
def list_usb_performax_devices():
    """
    List all performax devices.

    Return list of tuples ``(index, serial, model, desc, vid, pid)``, one per device.
    """
    lib.initlib()
    ndev=lib.fnPerformaxComGetNumDevices()
    return [get_usb_device_info(d) for d in range(ndev)]


class GenericPerformaxStage(stage.IMultiaxisStage):
    """
    Generic Arcus Performax translation stage.

    Args:
        idx(int): stage index; if using a USB connection, specifies a USB device index; if using RS485 connection, specifies device index on the bus
        conn: if not ``None``, defines a connection to RS485 connection. Usually (e.g., for USB-to-RS485 adapters) this is a serial connection,
            which either a name (e.g., ``"COM1"``), or a tuple ``(name, baudrate)`` (e.g., ``("COM1", 9600)``);
            if `conn` is ``None``, assume direct USB connection and use the manufacturer-provided DLL
    """
    _default_operation_cooldown=0.01
    _axis_value_case="upper"
    Error=ArcusError
    def __init__(self, idx=0, conn=None):
        super().__init__()
        self._operation_cooldown=self._default_operation_cooldown
        self.conn=conn
        if conn is None:
            lib.initlib()
            self.instr=None
            self._instr_conn=None
        else:
            self.instr=comm_backend.new_backend(conn,("auto","serial"),term_read="\r",term_write="\r",timeout=3.,datatype="str",
                defaults={"serial":("COM1",9600),"network":("192.168.1.250",5001)},reraise_error=ArcusBackendError)
            self._instr_conn=self.instr.conn
        self.idx=idx
        self.handle=None
        self.open()
        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("device_number",self.get_device_number)


    def _get_connection_parameters(self):
        return self.idx,self._instr_conn
    def open(self):
        """Open the connection to the stage"""
        if self.instr is not None:
            self.instr.open()
        else:
            self.close()
            lib.fnPerformaxComGetNumDevices()  # sometimes needed to set up the dll
            # lib.fnPerformaxComSetTimeouts(5000,5000)
            for _ in range(5):
                try:
                    self.handle=lib.fnPerformaxComOpen(self.idx)
                    lib.fnPerformaxComFlush(self.handle)
                    return
                except ArcusPerformaxLibError:
                    time.sleep(0.3)
            raise ArcusError("can't connect to the stage with index {}".format(self.idx))
    def close(self):
        """Close the connection to the stage"""
        if self.instr is not None:
            self.instr.close()
        elif self.handle is not None:
            for _ in range(5):
                try:
                    lib.fnPerformaxComClose(self.handle)
                    self.handle=None
                    return
                except ArcusPerformaxLibError:
                    time.sleep(0.3)
            raise ArcusError("can't disconnect from the stage with index {}".format(self.idx))
    def is_opened(self):
        if self.instr is not None:
            return bool(self.instr)
        return self.handle is not None
    def _check_handle(self):
        if self.handle is None:
            raise ArcusError("device is not opened")

    def get_device_info(self):
        """Get the device info"""
        if self.instr is not None:
            return (self.idx,self.get_device_number())
        return get_usb_device_info(self.idx)
    def query(self, comm):
        """Send a query to the stage and return the reply"""
        if self.instr is not None:
            if self.instr.get_backend_name()=="network":
                self.instr.write(comm)
            else:
                self.instr.write("@{:02d}{}".format(self.idx,comm))
            return self.instr.readline()
        else:
            self._check_handle()
            time.sleep(self._operation_cooldown)
            scomm=py3.as_builtin_bytes(comm)+b"\x00"
            try:
                reply=py3.as_str(lib.fnPerformaxComSendRecv(self.handle,scomm))
                if reply.startswith("?"):
                    raise ArcusError("device returned error: {}".format(reply[1:]))
                return reply
            except ArcusPerformaxLibError:
                raise ArcusError("error sending device query {}".format(comm))

    def get_device_number(self):
        """
        Get the device number used in RS-485 communications.
        
        Usually it is a string with the format similar to ``"4EX00"``.
        """
        return self.query("DN")
    def set_device_number(self, number, store=True):
        """
        Get the device number used in RS-485 communications.
        
        `number` can be either a full device id (e.g., ``"4EX00"``), or a single number between 0 and 99.
        In order for the change to take effect, the device needs to be power-cycled.
        If ``store==True``, automatically store settings to the memory; otherwise, the settings will be lost
        unless :meth:`store_defaults` is called at some point before the power-cycle.
        """
        if isinstance(number,int):
            number="{}{:02d}".format(self.get_device_number()[:-2],number)
        self.query("DN={}".format(number))
        if store:
            self.store_defaults()
        return self.get_device_number()

    def store_defaults(self):
        """
        Store some of the settings to the memory as defaults.
        
        Applies to device number, baudrate, limit error behavior, polarity, and some other settings.
        """
        self.query("STORE")




class Performax4EXStage(GenericPerformaxStage):
    """
    Arcus Performax 4EX/4ET translation stage.

    Args:
        idx(int): stage index; if using a USB connection, specifies a USB device index; if using RS485 connection, specifies device index on the bus
        conn: if not ``None``, defines a connection to RS485 connection. Usually (e.g., for USB-to-RS485 adapters) this is a serial connection,
            which either a name (e.g., ``"COM1"``), or a tuple ``(name, baudrate)`` (e.g., ``("COM1", 9600)``);
            if `conn` is ``None``, assume direct USB connection and use the manufacturer-provided DLL
        enable: if ``True``, enable all axes on startup
    """
    _axes=list("XYZU")
    _speed_comm="HS"
    _split_comms=False
    _individual_home=False
    _analog_inputs=range(1,9)
    def __init__(self, idx=0, conn=None, enable=True):
        super().__init__(idx=idx,conn=conn)
        with self._close_on_error():
            self.enable_absolute_mode()
            if enable:
                self.enable_axis()
            self.enable_limit_errors(False)
        self._add_status_variable("baudrate",self.get_baudrate)
        self._add_settings_variable("limit_errors_enabled",self.limit_errors_enabled,self.enable_limit_errors)
        self._add_status_variable("current_limit_errors",self.check_limit_error)
        self._add_status_variable("position",self.get_position)
        self._add_status_variable("encoder",self.get_encoder)
        self._add_status_variable("current_speed",self.get_current_axis_speed)
        self._add_settings_variable("enabled",self.is_enabled,lambda v: self.enable_axis("all",v))
        self._add_settings_variable("global_speed",self.get_global_speed,self.set_global_speed)
        self._add_settings_variable("axis_speed",self.get_axis_speed,lambda v: self.set_axis_speed("all",v))
        self._add_status_variable("axis_status",self.get_status)
        self._add_status_variable("moving",self.is_moving)
        self._add_status_variable("digital_input",self.get_digital_input_register,priority=-2)
        self._add_settings_variable("digital_output",self.get_digital_output_register,priority=-2)
        self._add_settings_variable("analog_input",self.get_analog_input,priority=-2,mux=(self._analog_inputs,))


    _p_baudrate=interface.EnumParameterClass("baudrate",{9600:1,19200:2,38400:3,57600:4,115200:5})
    @interface.use_parameters(_returns="baudrate")
    def get_baudrate(self):
        """Get current baud rate"""
        return int(self.query("DB"))
    @interface.use_parameters
    def set_baudrate(self, baudrate, store=True):
        """
        Set current baud rate.
        
        Acceptable values are 9600 (default), 19200, 38400, 57600, and 115200.
        In order for the change to take effect, the device needs to be power-cycled.
        If ``store==True``, automatically store settings to the memory; otherwise, the settings will be lost
        unless :meth:`store_defaults` is called at some point before the power-cycle.
        """
        self.query("DB={}".format(baudrate))
        if store:
            self.store_defaults()
        return self.get_baudrate()


    def enable_absolute_mode(self, enable=True):
        """Set absolute motion mode"""
        self.query("ABS" if enable else "REL")
    def enable_limit_errors(self, enable=True, autoclear=True):
        """
        Enable limit errors.

        If on, reaching limit switch on an axis puts it into an error state, which immediately stops this an all other axes;
        any further motion command on this axis will raise an error (it is still possible to restart motion on other axes);
        the axis motion can only be resumed by calling :meth:`clear_limit_error`.
        If off, the limited axis still stops, but the other axes are unaffected.
        If ``autoclear==True`` and ``enable==False``, also clear the current limit errors on all exs.
        """
        self.query("IERR={}".format(0 if enable else 1))
        if not enable and autoclear:
            self.clear_limit_error(axis="all")
    def limit_errors_enabled(self):
        """
        Check if global limit errors are enabled.

        If on, reaching limit switch on an axis puts it into an error state, which immediately stops this an all other axes;
        any further motion command on this axis will raise an error (it is still possible to restart motion on other axes);
        the axis motion can only be resumed by calling :meth:`clear_limit_error`.
        If off, the limited axis still stops, but the other axes are unaffected.
        """
        return not bool(int(self.query("IERR")))
    
    def _axisn(self, axis):
        return self._axes.index(axis)+1
    @stage.muxaxis
    @interface.use_parameters
    def is_enabled(self, axis="all"):
        """Check if the axis output is enabled"""
        return bool(int(self.query("EO{}".format(self._axisn(axis)))))
    @stage.muxaxis(mux_argnames="enable")
    @interface.use_parameters
    def enable_axis(self, axis="all", enable=True):
        """
        Enable axis output.

        If the output is disabled, the steps are generated by the controller, but not sent to the motors.
        """
        self.query("EO{}={}".format(self._axisn(axis),1 if enable else 0))

    @stage.muxaxis
    @interface.use_parameters
    def get_position(self, axis="all"):
        """Get the current axis pulse position"""
        return int(self.query("P"+axis))
    @interface.use_parameters
    def set_position_reference(self, axis, position=0):
        """
        Set the current axis pulse position as a reference.
        
        Re-calibrate the pulse position counter so that the current position is set as `position` (0 by default).
        """
        self.query("P{}={:.0f}".format(axis,position))
    @stage.muxaxis
    @interface.use_parameters
    def get_encoder(self, axis="all"):
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
    @interface.use_parameters
    def jog(self, axis, direction):
        """
        Jog a given axis in a given direction.
        
        `direction` can be either ``"-"`` (negative) or ``"+"`` (positive).
        The motion continues until it is explicitly stopped, or until a limit is hit.
        """
        self.query("J{}{}".format(axis,"+" if direction else "-"))
    @stage.muxaxis
    @interface.use_parameters
    def stop(self, axis="all", immediate=False):
        """
        Stop motion of a given axis.

        If ``immediate==True`` make an abrupt stop; otherwise, slow down gradually.
        """
        comm="ABORT" if immediate else "STOP"
        self.query("{}{}".format(comm,axis))

    _p_home_mode=interface.EnumParameterClass("home_mode",{"only_home_input":0,"only_limit_input":1,"home_and_zidx_input":2,"only_zidx_input":3,"only_home_input_lowspeed":4})
    @interface.use_parameters
    def home(self, axis, direction, home_mode):
        """
        Home the given axis using a given home mode.

        `direction` can be ``"+"`` or ``"-"``
        The mode can be ``"only_home_input"``, ``"only_home_input_lowspeed"``, ``"only_limit_input"``, ``"only_zidx_input"``, or ``"home_and_zidx_input"``.
        For meaning, see Arcus PMX manual.
        """
        if self._individual_home:
            comm=["H","L","HZ","Z","HL"][home_mode]
            self.query("{}{}{}".format(comm,axis,direction))
        else:
            self.query("H{}{}{}".format(axis,direction,home_mode))

    def get_global_speed(self):
        """Get the global speed setting (in Hz); overridden by a non-zero axis speed"""
        return int(self.query(self._speed_comm))
    @stage.muxaxis
    @interface.use_parameters
    def get_axis_speed(self, axis="all"):
        """Get the individual axis speed setting (in Hz); 0 means that the global speed is used"""
        return int(self.query(self._speed_comm+axis))
    def set_global_speed(self, speed):
        """Set the global speed setting (in Hz); overridden by a non-zero axis speed"""
        self.query("{}={:.0f}".format(self._speed_comm,speed))
        return self.get_global_speed()
    @stage.muxaxis(mux_argnames="speed")
    @interface.use_parameters
    def set_axis_speed(self, axis, speed):
        """Set the individual axis speed setting (in Hz); 0 means that the global speed is used"""
        self.query("{}{}={:.0f}".format(self._speed_comm,axis,speed))
        return self._wap.get_axis_speed(axis)
    @stage.muxaxis
    @interface.use_parameters
    def get_current_axis_speed(self, axis="all"):
        """Get the instantaneous speed (in Hz)"""
        if self._split_comms:
            return int(self.query("PS{}".format(axis)))
        else:
            speeds=[int(x) for x in self.query("PS").split(":") if x]
            return speeds[self._axisn(axis)-1]

    _status_bits={  "accel":0x001,"decel":0x002,"moving":0x004,
                    "alarm":0x008,
                    "sw_plus_lim":0x010,"sw_minus_lim":0x020,"sw_home":0x040,
                    "err_plus_lim":0x080,"err_minus_lim":0x100,"err_alarm":0x200,
                    "TOC_timeout":0x800}
    def _get_full_status(self):
        if self._split_comms:
            return [int(self.query("MST{}".format(x))) for x in self._axes]
        else:
            stat=self.query("MST")
            return [int(x) for x in stat.split(":") if x]
    @stage.muxaxis
    @interface.use_parameters
    def get_status_n(self, axis="all"):
        """Get the axis status as an integer"""
        return self._get_full_status()[self._axisn(axis)-1]
    @stage.muxaxis
    def get_status(self, axis="all"):
        """Get the axis status as a set of string descriptors"""
        statn=self.get_status_n(axis)
        return [ k for k in self._status_bits if self._status_bits[k]&statn ]
    @stage.muxaxis
    def is_moving(self, axis="all"):
        """Check if a given axis is moving"""
        return bool(self.get_status_n(axis)&0x007)
    def wait_move(self, axis, timeout=None, period=0.05):
        """Wait until motion is done"""
        if axis=="all":
            for ax in self._axes:
                self.wait_move(ax,timeout=timeout,period=period)
            return
        ctd=general.Countdown(timeout)
        while True:
            if not self.is_moving(axis):
                return
            if ctd.passed():
                raise ArcusError("waiting for motion on axis {} caused a timeout".format(axis))
            time.sleep(period)

    @stage.muxaxis
    def check_limit_error(self, axis="all"):
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
    @stage.muxaxis
    @interface.use_parameters
    def clear_limit_error(self, axis="all"):
        """Clear axis limit errors"""
        self.query("CLR"+axis)

    def get_analog_input(self, channel):
        """Get voltage (in V) at a given input (starting with 1)"""
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




class Performax2EXStage(Performax4EXStage):
    """
    Arcus Performax 2EX/2ED translation stage.

    Args:
        idx(int): stage index; if using a USB connection, specifies a USB device index; if using RS485 connection, specifies device index on the bus
        conn: if not ``None``, defines a connection to RS485 connection. Usually (e.g., for USB-to-RS485 adapters) this is a serial connection,
            which either a name (e.g., ``"COM1"``), or a tuple ``(name, baudrate)`` (e.g., ``("COM1", 9600)``);
            if `conn` is ``None``, assume direct USB connection and use the manufacturer-provided DLL
        enable: if ``True``, enable all axes on startup
    """
    _axes=list("XY")
    _speed_comm="HSPD"
    _split_comms=True
    _individual_home=True
    _analog_inputs=range(1,3)





class PerformaxDMXJSAStage(GenericPerformaxStage):
    """
    Arcus Performax DMX-J-SA translation stage.

    Args:
        idx(int): stage index; if using a USB connection, specifies a USB device index; if using RS485 connection, specifies device index on the bus
        conn: if not ``None``, defines a connection to RS485 connection. Usually (e.g., for USB-to-RS485 adapters) this is a serial connection,
            which either a name (e.g., ``"COM1"``), or a tuple ``(name, baudrate)`` (e.g., ``("COM1", 9600)``);
            if `conn` is ``None``, assume direct USB connection and use the manufacturer-provided DLL
        enable: if ``True``, enable all axes on startup
        autoclear: if ``True``, automatically clear limit error before the motion start
    """
    def __init__(self, idx=0, conn=None, enable=True, autoclear=True):
        super().__init__(idx=idx,conn=conn)
        with self._close_on_error():
            self.enable_absolute_mode()
            if enable:
                self.enable_axis()
        self.autoclear=autoclear
        self._add_status_variable("current_limit_errors",self.check_limit_error)
        self._add_status_variable("position",self.get_position)
        self._add_settings_variable("enabled",self.is_enabled,self.enable_axis)
        self._add_settings_variable("axis_speed",self.get_axis_speed,self.set_axis_speed)
        self._add_status_variable("axis_status",self.get_status)
        self._add_status_variable("moving",self.is_moving)
        self._add_status_variable("digital_input",self.get_digital_input_register,priority=-2)
        self._add_settings_variable("digital_output",self.get_digital_output_register,priority=-2)



    def enable_absolute_mode(self, enable=True):
        """Set absolute motion mode"""
        self.query("ABS" if enable else "REL")
    
    def _clearlim(self):
        if self.autoclear:
            self.clear_limit_error()
    @interface.use_parameters
    def is_enabled(self):
        """Check if the output is enabled"""
        return bool(int(self.query("EO")))
    @interface.use_parameters
    def enable_axis(self, enable=True):
        """
        Enable output.

        If the output is disabled, the steps are generated by the controller, but not sent to the motors.
        """
        self.query("EO={}".format(1 if enable else 0))

    @interface.use_parameters
    def get_position(self):
        """Get the current pulse position"""
        return int(self.query("PX"))
    @interface.use_parameters
    def set_position_reference(self, position=0):
        """
        Set the current pulse position as a reference.
        
        Re-calibrate the pulse position counter so that the current position is set as `position` (0 by default).
        """
        self.query("PX={:.0f}".format(position))
    @interface.use_parameters
    def move_to(self, position):
        """Move to a given position"""
        self._clearlim()
        self.query("X{:.0f}".format(position))
    def move_by(self, steps=1):
        """Move for a given number of steps"""
        self.move_to(self.get_position()+steps)
    @interface.use_parameters
    def jog(self, direction):
        """
        Jog in a given direction.
        
        `direction` can be either ``"-"`` (negative) or ``"+"`` (positive).
        The motion continues until it is explicitly stopped, or until a limit is hit.
        """
        self._clearlim()
        self.query("J{}".format("+" if direction else "-"))
    @interface.use_parameters
    def stop(self, immediate=False):
        """
        Stop motion.

        If ``immediate==True`` make an abrupt stop; otherwise, slow down gradually.
        """
        comm="ABORT" if immediate else "STOP"
        self.query("{}".format(comm))

    _p_home_mode=interface.EnumParameterClass("home_mode",{"only_home_input":0,"only_limit_input":1,"only_home_input_lowspeed":2})
    @interface.use_parameters
    def home(self, direction, home_mode):
        """
        Home using a given home mode.

        `direction` can be ``"+"`` or ``"-"``
        The mode can be ``"only_home_input"``, ``"only_home_input_lowspeed"``, or ``"only_limit_input"``.
        For meaning, see Arcus PMX manual.
        """
        comm=["H","L","HL"][home_mode]
        self.query("{}{}".format(comm,direction))

    def get_axis_speed(self):
        """Get the speed setting (in Hz)"""
        return int(self.query("HSPD"))
    def set_axis_speed(self, speed):
        """Set the speed setting (in Hz)"""
        self.query("HSPD={:.0f}".format(speed))
        return self.get_axis_speed()
    
    _status_bits={  "running":0x001,"accel":0x002,"decel":0x004,"sw_home":0x008,
                    "sw_minus_lim":0x010,"sw_plus_lim":0x020,
                    "err_plus_lim":0x040,"err_minus_lim":0x080,
                    "TOC_timeout":0x400}
    def get_status_n(self):
        """Get the status as an integer"""
        return int(self.query("MST"))
    def get_status(self):
        """Get the status as a set of string descriptors"""
        statn=self.get_status_n()
        return [ k for k in self._status_bits if self._status_bits[k]&statn ]
    def is_moving(self):
        """Check if motor is moving"""
        return bool(self.get_status_n()&0x007)
    def wait_move(self, timeout=None, period=0.05):
        """Wait until motion is done"""
        ctd=general.Countdown(timeout)
        while True:
            if not self.is_moving():
                return
            if ctd.passed():
                raise ArcusError("waiting for motion caused a timeout")
            time.sleep(period)

    def check_limit_error(self):
        """
        Check if the motor hit limit errors.

        Return ``""`` (not errors), ``"+"`` (positive limit error) or ``"-"`` (negative limit error).
        """
        stat=self.get_status_n()
        err=""
        if stat&self._status_bits["err_plus_lim"]:
            err=err+"+"
        if stat&self._status_bits["err_minus_lim"]:
            err=err+"-"
        return err
    @interface.use_parameters
    def clear_limit_error(self):
        """Clear limit error"""
        self.query("CLR")

    def get_digital_input(self, channel):
        """Get value (0 or 1) at a given digital input (1 through 5)"""
        return int(self.query("DI{}".format(channel)))
    def get_digital_input_register(self):
        """Get all 5 digital inputs as a single 5-bit integer"""
        return int(self.query("DI"))
    def get_digital_output(self, channel):
        """Get value (0 or 1) at a given digital output (1 through 2)"""
        return int(self.query("DO{}".format(channel)))
    def get_digital_output_register(self):
        """Get all 2 digital outputs as a single 2-bit integer"""
        return int(self.query("DO"))
    def set_digital_output(self, channel, value):
        """Set value (0 or 1) at a given digital output (1 through 2)"""
        self.query("DO{}={}".format(channel,1 if value else 0))
        return self.get_digital_output(channel)
    def set_digital_output_register(self, value):
        """Set all 2 digital inputs as a single 2-bit integer"""
        self.query("DO={}".format(int(value)))
        return self.get_digital_output_register()