from ...core.devio import comm_backend, SCPI, interface
from ...core.utils import funcargparse

from ..interface import stage

class PhysikInstrumenteError(comm_backend.DeviceError):
    """Generic Physik Instrumente error"""
class PhysikInstrumenteBackendError(PhysikInstrumenteError,comm_backend.DeviceBackendError):
    """Generic Physik Instrumente backend communication error"""




class GenericPIController(comm_backend.ICommBackendWrapper,stage.IMultiaxisStage):
    """
    Generic Physik Instrumente controller.

    Args:
        conn: connection parameters (usually port or a tuple containing port and baudrate)
        auto_online: if ``True``, switch to the online mode upon connection;
            in this online mode controller parameters are controlled remotely instead of the front panel (including external voltages),
            while in the offline mode most of the parameters are still controlled manually, and the remote connection is mostly used for readout
    """
    Error=PhysikInstrumenteError
    def __init__(self, conn, auto_online=True):
        instr=comm_backend.new_backend(conn,term_read="\n",term_write="\n",timeout=3.,datatype="str",defaults={"serial":("COM1",9600)},reraise_error=PhysikInstrumenteBackendError)
        super().__init__(instr)
        self.auto_online=auto_online
        self._add_info_variable("device_id",self.get_id)
        self._add_settings_variable("online",self.is_online_enabled,self.enable_online)
        with self._close_on_error():
            self.open()

    def _assign_axes(self):
        pass
    def open(self):
        res=super().open()
        self.instr.flush_read()
        self._assign_axes()
        if self.auto_online:
            self.query("ONL 1",reply=False)
        return res
    
    _float_fmt="{:.5E}"
    @classmethod
    def _conv_value(cls, value):
        if isinstance(value,float):
            return cls._float_fmt.format(value)
        if isinstance(value,bool):
            return "1" if value else "0"
        return str(value)
    @classmethod
    def _check_value_kind(cls, kind):
        funcargparse.check_parameter_range(kind,"kind",["str","float","int","bool"])
    @classmethod
    def _parse_value(cls, value, kind):
        if kind=="float":
            return float(value)
        if kind=="int":
            return int(value)
        if kind=="bool":
            return bool(int(value))
        return value
    @classmethod
    def _build_command(cls, args):
        if not isinstance(args,(list,tuple)):
            args=[args]
        args=[cls._conv_value(a) for a in args]
        return " ".join(args)
    def _read_reply(self, multiline=False):
        replies=[]
        while True:
            r=self.instr.readline()
            replies.append(r.strip())
            if not r.endswith(" "):
                break
        if not multiline and len(replies)!=1:
            raise PhysikInstrumenteError("reply contains {} lines, expected only one line".format(len(replies)))
        return replies if multiline else replies[0]
    def _map_result(self, result, func):
        if isinstance(result,dict):
            return {k:func(v) for k,v in result.items()}
        return func(result)
    def _ensure_single_axis(self, axis):
        if axis is None and len(self._axes)>1:
            raise ValueError("this command requires explicitly supplied axis")

    def query(self, comm, multiline=False, reply=True):
        """
        Query a single command to the controller.

        If ``multiline==True``, expect a multi-line reply and return a list with separate reply lines;
        otherwise, expect a single-line reply and raise an error if multi-line reply is received.

        If ``reply==False``, expect no reply at all (used for, e.g., set commands).
        """
        command=self._build_command(comm)
        self.instr.write(command)
        if reply:
            return self._read_reply(multiline=multiline)
    def _combine_axes_values(self, axis=None, value=None):
        single_axis=False
        if isinstance(value,dict):
            axis=list(value.keys())
            value=list(value.values())
        else:
            if axis is None:
                axis=self.get_all_axes()
                single_axis=len(axis)==1
            elif not isinstance(axis,(list,tuple)):
                axis=[axis]
                single_axis=True
            if isinstance(value,(list,tuple)):
                if len(value)!=len(axis):
                    raise ValueError("supplied values {} have different length from the supplied axis {}".format(value,axis))
            else:
                value=[value]*len(axis)
        axis=[self._resolve_axis(ax) for ax in axis]
        return axis,single_axis,value
    def query_axis(self, comm, axis=None, subidx=None, kind="str"):
        """
        Query the given command for the given axis.

        `axis` can be a single axis name (e.g., ``"A"``), a list of axes, or ``None``, which queries all axes.
        If `axis` is a single axis, simply return the corresponding value; otherwise, return a dict ``{axis: value}``.
        `kind` can specify value kind: ``"str"`` (return as is), ``"float"``, ``"int"``, or ``"bool"``.
        """
        self._check_value_kind(kind)
        axis,single_axis,_=self._combine_axes_values(axis,None)
        if not isinstance(comm,(list,tuple)):
            comm=[comm]
        if subidx is None:
            grps=[(a,) for a in axis]
        else:
            grps=[(a,subidx) for a in axis]
        comm+=[p for t in grps for p in t if p is not None]
        reply=self.query(comm,multiline=True)
        if len(reply)!=len(axis):
            raise PhysikInstrumenteError("unexpected reply size: expected {} lines, got {} lines".format(len(axis),len(reply)))
        res=[]
        for a,r in zip(axis,reply):
            if r.startswith(a+"="):
                r=r[len(a)+1:]
            res.append(r.strip())
        res=[self._parse_value(r,kind) for r in res]
        return res[0] if single_axis else dict(zip(axis,res))
    def set_axis(self, comm, value, axis=None, subidx=None, reply=False):
        """
        Query the given value for the given axis.

        `value` can be a single value (set the same for all specified axes), a list of values (one per axis), or a dict ``{axis: value}``.
        `axis` can be a single axis name (e.g., ``"A"``), a list of axes, or ``None``, which queries all axes.
        If ``reply==False``, expect no reply.
        """
        axis,_,value=self._combine_axes_values(axis,value)
        if not isinstance(comm,(list,tuple)):
            comm=[comm]
        if subidx is None:
            grps=[(a,v) for a,v in zip(axis,value)]
        else:
            grps=[(a,subidx,v) for a,v in zip(axis,value)]
        comm+=[p for t in grps for p in t if p is not None]
        return self.query(comm,multiline=True,reply=reply)
    
    def get_id(self):
        """Get the device ID string"""
        return self.query("*IDN?")
    def get_help(self):
        """Get the help for all commands; might take a long time on low-speed serial connections"""
        return self.query("HLP?",multiline=True)
    
    def is_online_enabled(self):
        """Check if online mode is enabled"""
        return bool(int(self.query("ONL?")))
    def enable_online(self, enable=True):
        """Enable or disable online mode"""
        self.query(("ONL",bool(enable)),reply=False)
        return self.is_online_enabled()

    def get_axis_parameter(self, pid, axis=None, kind="str"):
        """Get value of the given parameter id for the given axis (all axes by default)"""
        return self.query_axis("SPA?",axis=axis,subidx=pid,kind=kind)
    def set_axis_parameter(self, pid, value, axis=None, kind="str"):
        """Get value of the given parameter id for the given axis (all axes by default)"""
        self.set_axis("SPA",value,axis=axis,subidx=pid)
        return self.get_axis_parameter(pid,axis=axis,kind=kind)




class PIE516(GenericPIController):
    """
    Physik Instrumente E-516 controller.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
        auto_online: if ``True``, switch to the online mode upon connection;
            in this online mode controller parameters such as voltages or positions are controlled remotely instead of the front panel (including external voltages),
            while in the offline mode most of the parameters are still controlled manually, and the remote connection is mostly used for readout
    """
    def __init__(self, conn, auto_online=True):
        super().__init__(conn,auto_online=auto_online)
        self._add_settings_variable("servo",self.is_servo_enabled,self.enable_servo)
        self._add_settings_variable("drift_compensation",self.is_drift_compensation_enabled,self.enable_drift_compensation)
        self._add_settings_variable("velocity_control",self.is_velocity_control_enabled,self.enable_velocity_control)
        self._add_status_variable("voltage",self.get_voltage)
        self._add_status_variable("voltage_setpoint",self.get_voltage_setpoint)
        self._add_settings_variable("voltage_lowlim",self.get_voltage_lower_limit,self.set_voltage_lower_limit)
        self._add_settings_variable("voltage_upplim",self.get_voltage_upper_limit,self.set_voltage_upper_limit)
        self._add_status_variable("position",self.get_position)
        self._add_status_variable("target_position",self.get_target_position)
        self._add_settings_variable("position_lowlim",self.get_position_lower_limit,self.set_position_lower_limit)
        self._add_settings_variable("position_upplim",self.get_position_upper_limit,self.set_position_upper_limit)
        self._add_settings_variable("velocity",self.get_velocity,self.set_velocity)

    def _assign_axes(self):
        self._update_axes(list(self.query("SAI?")))

    def is_servo_enabled(self, axis=None):
        """Check if the servo is enabled on the given axis (all axes by default)"""
        return self.query_axis("SVO?",axis=axis,kind="bool")
    def enable_servo(self, enable=True, axis=None):
        """Enable or disable servo on the given axis (all axes by default)"""
        self.set_axis("SVO",enable,axis=axis)
        return self.is_servo_enabled(axis=axis)
    def is_drift_compensation_enabled(self, axis=None):
        """Check if the drift compensation is enabled on the given axis (all axes by default)"""
        return self.query_axis("DCO?",axis=axis,kind="bool")
    def enable_drift_compensation(self, enable=True, axis=None):
        """Enable or disable drift compensation on the given axis (all axes by default)"""
        self.set_axis("DCO",enable,axis=axis)
        return self.is_drift_compensation_enabled(axis=axis)
    def is_velocity_control_enabled(self, axis=None):
        """Check if the velocity control is enabled on the given axis (all axes by default)"""
        return self.query_axis("VCO?",axis=axis,kind="bool")
    def enable_velocity_control(self, enable=True, axis=None):
        """Enable or disable velocity control on the given axis (all axes by default)"""
        self.set_axis("VCO",enable,axis=axis)
        return self.is_velocity_control_enabled(axis=axis)
    
    def get_voltage_setpoint(self, axis=None):
        """Get the current voltage setpoint on the given axis (all axes by default)"""
        return self.query_axis("SVA?",axis=axis,kind="float")
    def get_voltage(self, axis=None):
        """Get the actual voltage value on the given axis (all axes by default)"""
        return self.query_axis("VOL?",axis=axis,kind="float")
    def set_voltage(self, voltage, axis=None):
        """Get the target voltage on the given axis (all axes by default)"""
        self.set_axis("SVA",voltage,axis=axis)
        return self.get_voltage_setpoint(axis=axis)
    def get_voltage_lower_limit(self, axis=None):
        """Get the lower output voltage limit on the given axis (all axes by default)"""
        return self.query_axis("VMI?",axis=axis,kind="float")
    def set_voltage_lower_limit(self, voltage, axis=None):
        """Get the lower output voltage limit on the given axis (all axes by default)"""
        self.set_axis("VMI",voltage,axis=axis)
        return self.get_voltage_lower_limit(axis=axis)
    def get_voltage_upper_limit(self, axis=None):
        """Get the upper output voltage limit on the given axis (all axes by default)"""
        return self.query_axis("VMA?",axis=axis,kind="float")
    def set_voltage_upper_limit(self, voltage, axis=None):
        """Get the upper output voltage limit on the given axis (all axes by default)"""
        self.set_axis("VMA",voltage,axis=axis)
        return self.get_voltage_upper_limit(axis=axis)
    
    def get_velocity(self, axis=None):
        """Get velocity on the given axis (all axes by default)"""
        return self.query_axis("VEL?",axis=axis,kind="float")
    def set_velocity(self, velocity, axis=None):
        """Set velocity on the given axis (all axes by default)"""
        self.set_axis("VEL",velocity,axis=axis)
        return self.get_velocity(axis=axis)
    def get_position(self, axis=None):
        """Get the current position on the given axis"""
        return self.query_axis("POS?",axis=axis,kind="float")
    def get_target_position(self, axis=None):
        """Get the target motion position on the given axis"""
        return self.query_axis("MOV?",axis=axis,kind="float")
    def move_to(self, position, axis=None):
        """Move the given axis to the given position"""
        self._ensure_single_axis(axis)
        self.set_axis("MOV",position,axis=axis)
        return self.get_target_position(axis=axis)
    def move_by(self, distance, axis=None):
        """Move the given axis by the given distance"""
        self._ensure_single_axis(axis)
        self.set_axis("MVR",distance,axis=axis)
        return self.get_target_position(axis=axis)
    def stop(self, axis=None):
        """Stop motion on the given axis (all axes by default)"""
        self.set_axis("STP",value=None,axis=axis)
    def get_position_lower_limit(self, axis=None):
        """Get the lower position limit on the given axis (all axes by default)"""
        return self.query_axis("NLM?",axis=axis,kind="float")
    def set_position_lower_limit(self, position, axis=None):
        """Get the lower position limit on the given axis (all axes by default)"""
        self.set_axis("NLM",position,axis=axis)
        return self.get_position_lower_limit(axis=axis)
    def get_position_upper_limit(self, axis=None):
        """Get the upper position limit on the given axis (all axes by default)"""
        return self.query_axis("PLM?",axis=axis,kind="float")
    def set_position_upper_limit(self, position, axis=None):
        """Get the upper position limit on the given axis (all axes by default)"""
        self.set_axis("PLM",position,axis=axis)
        return self.get_position_upper_limit(axis=axis)



class PIE515(stage.IMultiaxisStage,SCPI.SCPIDevice):
    """
    Physik Instrumente E-515 controller.

    Args:
        conn: connection parameters (usually port or a tuple containing port and baudrate)
        auto_online: if ``True``, switch to the online mode upon connection;
            in this online mode controller parameters are controlled remotely instead of the front panel (including external voltages),
            while in the offline mode most of the parameters are still controlled manually, and the remote connection is mostly used for readout
    """
    Error=PhysikInstrumenteError
    ReraiseError=PhysikInstrumenteBackendError
    def __init__(self, conn, auto_online=True):
        self._auto_online=auto_online
        self._last_selected_axis=1
        self._current_selected_axis=1
        super().__init__(conn,term_write="\n",term_read="\n",backend="serial",backend_defaults={"serial":("COM1",9600,8,'N',1,True,False,False)},default_axis=None)
        self._add_status_variable("online",self.is_online_enabled)
        self._add_status_variable("servo",lambda: self.is_servo_enabled(axis="all"))
        self._add_status_variable("voltage",lambda: self.get_voltage(axis="all"))
        self._add_status_variable("voltage_setpoint",lambda: self.get_voltage_setpoint(axis="all"))
        self._add_settings_variable("voltage_lowlim",lambda: self.get_voltage_lower_limit(axis="all"),lambda v: self.set_voltage_lower_limit(v,axis="all"))
        self._add_settings_variable("voltage_upplim",lambda: self.get_voltage_upper_limit(axis="all"),lambda v: self.set_voltage_upper_limit(v,axis="all"))
        self._add_status_variable("position",lambda: self.get_position(axis="all"))
        self._add_status_variable("target_position",lambda: self.get_target_position(axis="all"))
        self._add_settings_variable("position_lowlim",lambda: self.get_position_lower_limit(axis="all"),lambda v: self.set_position_lower_limit(v,axis="all"))
        self._add_settings_variable("position_upplim",lambda: self.get_position_upper_limit(axis="all"),lambda v: self.set_position_upper_limit(v,axis="all"))
        self.open()
    def open(self):
        res=super().open()
        with self._close_on_error():
            self.write("INST:SEL CH1")
            self.write("SOUR:VOLT:UNIT VOLT")
            self.write("POS:VOLT:UNIT DEF")
            if self._auto_online:
                self.enable_online(safe=True)
        return res
    def close(self):
        if self.is_opened():
            self.write("DEV:CONT LOC")
        super().close()

    _axes=[1,2,3]
    _bool_selector=("OFF","ON")
    def _setup_to_measured(self):
        self.set_voltage(self.get_voltage(axis="all"),axis="all")
        self.move_to(self.get_position(axis="all"),axis="all")
    def is_online_enabled(self):
        """Check if online mode is enabled"""
        return self.ask("DEV:CONT?").lower()=="rem"
    def enable_online(self, enable=True, safe=False):
        """
        Enable or disable online mode.
        
        If ``safe==True`` and ``enable==True``, set the current voltage and position setpoints to be equal to the currently read values;
        this avoids sudden change of output voltages when enabling the online mode. Note that this only works if all servo modes are off
        (enabling online mode always forcibly turns them off, which might lead to the output voltage jump).
        """
        if safe and enable:
            self._setup_to_measured()
        self.write("DEV:CONT","REM" if enable else "LOC")
        return self.is_online_enabled()
    
    def _set_current_axis(self, axis, assign=False):
        if axis is None:
            axis=self._current_selected_axis
        elif assign:
            self._current_selected_axis=axis
        if axis!=self._last_selected_axis:
            self.write("INST:SEL CH{}".format(axis))
            self._last_selected_axis=axis
    def get_current_axis(self):
        """Select the current measurement channel"""
        ch=self.ask("INST:SEL?")
        return int(ch[2:])
    @interface.use_parameters
    def select_axis(self, axis):
        """Select the current default axis"""
        self._set_current_axis(axis,assign=True)
        return self.get_current_axis()
    @stage.muxaxis
    @interface.use_parameters
    def is_servo_enabled(self, axis=None):
        """Check if the servo is enabled on the given axis (current axis by default)"""
        self._set_current_axis(axis)
        return self.ask("DEV:SERV?","bool")
    @stage.muxaxis
    @interface.use_parameters
    def enable_servo(self, enable=True, axis=None):
        """Enable or disable servo on the given axis (current axis by default)"""
        self._set_current_axis(axis)
        self.write("DEV:SERV",enable,"bool")
        return self.is_servo_enabled(axis=axis)
    
    @stage.muxaxis
    @interface.use_parameters
    def get_voltage_setpoint(self, axis=None):
        """Get the current voltage setpoint on the given axis (current axis by default)"""
        self._set_current_axis(axis)
        return self.ask("SOUR:VOLT?","float")
    @stage.muxaxis
    @interface.use_parameters
    def get_voltage(self, axis=None):
        """Get the actual voltage value on the given axis (current axis by default)"""
        self._set_current_axis(axis)
        return self.ask("MEAS:VOLT?","float")
    @stage.muxaxis(mux_argnames="voltage")
    @interface.use_parameters
    def set_voltage(self, voltage, axis=None):
        """Get the target voltage on the given axis (current axis by default)"""
        self._set_current_axis(axis)
        self.write("SOUR:VOLT",voltage)
        return self.get_voltage_setpoint(axis=axis)
    @stage.muxaxis
    @interface.use_parameters
    def get_voltage_lower_limit(self, axis=None):
        """Get the lower output voltage limit on the given axis (current axis by default)"""
        self._set_current_axis(axis)
        return self.ask("SOUR:VOLT:LIM:LOW?","float")
    @stage.muxaxis(mux_argnames="voltage")
    @interface.use_parameters
    def set_voltage_lower_limit(self, voltage, axis=None):
        """Get the lower output voltage limit on the given axis (current axis by default)"""
        self._set_current_axis(axis)
        self.write("SOUR:VOLT:LIM:LOW",voltage)
        return self.get_voltage_lower_limit(axis=axis)
    @stage.muxaxis
    @interface.use_parameters
    def get_voltage_upper_limit(self, axis=None):
        """Get the upper output voltage limit on the given axis (current axis by default)"""
        self._set_current_axis(axis)
        return self.ask("SOUR:VOLT:LIM:HIGH?","float")
    @stage.muxaxis(mux_argnames="voltage")
    @interface.use_parameters
    def set_voltage_upper_limit(self, voltage, axis=None):
        """Get the upper output voltage limit on the given axis (current axis by default)"""
        self._set_current_axis(axis)
        self.write("SOUR:VOLT:LIM:HIGH",voltage)
        return self.get_voltage_upper_limit(axis=axis)
    
    @stage.muxaxis
    @interface.use_parameters
    def get_position(self, axis=None):
        """Get current measured position on the given axis (current axis by default)"""
        self._set_current_axis(axis)
        return self.ask("MEAS:POS?","float")
    @stage.muxaxis
    @interface.use_parameters
    def get_target_position(self, axis=None):
        """Get the target motion position on the given axis"""
        self._set_current_axis(axis)
        return self.ask("SOUR:POS?","float")
    @stage.muxaxis
    @interface.use_parameters
    def move_to(self, position, axis=None):
        """Move the given axis to the given position"""
        self._set_current_axis(axis)
        self.write("SOUR:POS",position)
        return self.get_target_position(axis=axis)
    @stage.muxaxis
    @interface.use_parameters
    def move_by(self, distance, axis=None):
        """Move the given axis by the given distance"""
        position=self.get_target_position(axis=axis)
        return self.move_to(position+distance,axis=axis)
    @stage.muxaxis
    @interface.use_parameters
    def get_position_lower_limit(self, axis=None):
        """Get the lower position limit on the given axis (current axis by default)"""
        self._set_current_axis(axis)
        return self.ask("SOUR:POS:LIM:LOW?","float")
    @stage.muxaxis
    @interface.use_parameters(mux_argnames="position")
    def set_position_lower_limit(self, position, axis=None):
        """Get the lower position limit on the given axis (current axis by default)"""
        self._set_current_axis(axis)
        self.write("SOUR:POS:LIM:LOW",position)
        return self.get_position_lower_limit(axis=axis)
    @stage.muxaxis
    @interface.use_parameters
    def get_position_upper_limit(self, axis=None):
        """Get the upper position limit on the given axis (current axis by default)"""
        self._set_current_axis(axis)
        return self.ask("SOUR:POS:LIM:HIGH?","float")
    @stage.muxaxis(mux_argnames="position")
    @interface.use_parameters
    def set_position_upper_limit(self, position, axis=None):
        """Get the upper position limit on the given axis (current axis by default)"""
        self._set_current_axis(axis)
        self.write("SOUR:POS:LIM:HIGH",position)
        return self.get_position_upper_limit(axis=axis)