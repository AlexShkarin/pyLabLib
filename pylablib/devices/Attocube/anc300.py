from ...core.devio import comm_backend, interface
from ...core.utils import py3

import numpy as np

import re
import collections
import time

from ..interface import stage
from .base import AttocubeError, AttocubeBackendError


def muxaxis(*args, **kwargs):
    return stage.muxaxis(*args,return_kind="dict",**kwargs)
TDeviceInfo=collections.namedtuple("TDeviceInfo",["serial","version"])
class ANC300(comm_backend.ICommBackendWrapper,stage.IMultiaxisStage):
    """
    Attocube ANC300 controller.

    Args:
        conn: connection parameters; for Ethernet connection is a tuple ``(addr, port)``, a string ``"addr:port"``, or a string ``"addr"`` (default port 7240 us assumed)
        backend(str): communication backend; by default, try to determine from the communication parameters
        pwd(str): connection password for Ethernet connection (default is ``"123456"``)
    """
    Error=AttocubeError
    def __init__(self, conn, backend="auto", pwd="123456"):
        defaults={"serial":("COM1",38400,8,"N",1,0), "network":{"port":7230}}
        instr=comm_backend.new_backend(conn,backend=backend,timeout=3.,defaults=defaults,term_write="\r\n",reraise_error=AttocubeBackendError)
        self.pwd=pwd
        super().__init__(instr)
        self.open()
        self._correction={}
        self._add_info_variable("device_info",self.get_device_info)
        self._add_info_variable("axes_serial",self.get_axis_serial)
        self._add_status_variable("modes",self.get_mode)
        self._add_settings_variable("voltages",self.get_voltage,lambda v: self.set_voltage("all",v),ignore_error=AttocubeError)
        self._add_settings_variable("offsets",self.get_offset,lambda v: self.set_offset("all",v),ignore_error=AttocubeError)
        self._add_settings_variable("frequencies",self.get_frequency,lambda v: self.set_frequency("all",v),ignore_error=AttocubeError)
        self._add_status_variable("external_inputs",self.get_external_input_modes)
        self._add_status_variable("voltage_outputs",self.get_output)
        self._add_status_variable("capacitances",self.get_capacitance)
        self._add_status_variable("trigger_inputs",self.get_trigger_input,priority=-5)

    def open(self):
        """Open the connection to the stage"""
        res=self.instr.open()
        if self.instr._backend=="network" and self.pwd is not None:
            self.instr.write(self.pwd)
        self.instr.write("echo off")
        self.instr.read_multichar_term(["ERROR","OK"],remove_term=False)
        time.sleep(0.05)
        self.instr.flush_read()
        self.update_available_axes()
        return res
    
    def query(self, msg):
        """Send a query to the stage and return the reply"""
        self.instr.flush_read()
        self.instr.write(msg)
        reply=self.instr.read_multichar_term(["ERROR","OK"],remove_term=False)
        # self.instr.flush_read()
        if reply.upper().endswith(b"ERROR"):
            err=py3.as_str(reply)[:-5].strip()
            raise AttocubeError(err)
        return py3.as_str(reply[:-2].strip())
    
    def update_available_axes(self):
        """
        Update the list of available axes.
        
        Need to call only if the hardware configuration of the ANC module has changed.
        """
        axes=[]
        for ax in range(1,8):
            try:
                self.query("getm {}".format(ax))
                axes.append(ax)
            except AttocubeError:
                pass
        self._update_axes(axes)
        return list(axes)

    def get_device_info(self):
        """Get the device info of the controller board: ``(serial, version)``"""
        return TDeviceInfo(self.query("getcser"),self.query("ver"))
    @muxaxis
    @interface.use_parameters
    def get_axis_serial(self, axis="all"):
        """Get serial number of the controller board"""
        return self.query("getser {}".format(axis))

    @muxaxis(mux_argnames="mode")
    @interface.use_parameters
    def set_mode(self, axis="all", mode="stp"):
        """
        Set axis mode.

        `axis` is either an axis index (starting from 1), or ``"all"`` (all axes).
        `mode` can be ``"gnd"`` (ground), ``"stp"`` (step), ``"cap"`` (measure capacitance, then ground),
        ``"offs"`` (offset only, no stepping), ``"stp+"`` (offset with added stepping waveform), ``"stp-"`` (offset with subtracted stepping).
        Note that not all modes are supported by all modules:
        ANM150 doesn't support offset voltage (``"offs"``, ``"stp+"``, ``"stp-"`` modes),
        ANM200 doesn't support stepping (``"stp"``, ``"stp+"``, ``"stp-"`` modes).
        """
        self.query("setm {} {}".format(axis,mode))
        return self._wip.get_mode(axis=axis)
    @muxaxis
    @interface.use_parameters
    def get_mode(self, axis="all"):
        """
        Get axis mode.

        `axis` is either an axis index (starting from 1), or ``"all"`` (all axes).
        See :meth:`set_mode` for the description of the modes.
        """
        reply=self.query("getm {}".format(axis)).strip()
        if reply.startswith("mode = "):
            return reply[7:].strip()
        raise AttocubeError("unexpected reply: {}".format(reply))
    @muxaxis
    def is_enabled(self, axis="all"):
        """Check if the axis is enabled"""
        return self.get_mode(axis) in ["stp","stp+","stp-","off","in"]
    def enable_axis(self, axis="all", mode="stp"):
        """Enable specific axis (set to step mode)"""
        self.set_mode(axis,mode=mode)
    def disable_axis(self, axis="all"):
        """Disable specific axis (set to ground mode)"""
        self.set_mode(axis,mode="gnd")
    @interface.use_parameters
    def _wait_for_capacitance(self, axis):
        self.query("capw {}".format(axis))
    @muxaxis
    def measure_capacitance(self, axis="all", wait=True):
        """
        Measure axis capacitance; finish in the GND mode.
        
        If ``wait==True``, wait until the capacitance measurement is finished (takes about a second per axis).
        """
        if self.get_mode(axis)!="gnd":
            self.set_mode(axis,mode="gnd")
            time.sleep(0.1)
        self.set_mode(axis,mode="cap")
        if wait:
            self._wait_for_capacitance(axis)

    def _parse_string_reply(self, reply, name):
        patt="^"+name+r"\s*=\s*(.+)\s*$"
        m=re.match(patt,reply,re.IGNORECASE)
        if not m:
            raise AttocubeError("unexpected reply: {}".format(reply))
        return m[1]
    def _parse_float_reply(self, reply, name, units):
        patt="^"+name+r"\s*=\s*([\d.]+)\s*"+units+"$"
        m=re.match(patt,reply,re.IGNORECASE)
        if not m:
            raise AttocubeError("unexpected reply: {}".format(reply))
        return float(m[1])
    @muxaxis
    @interface.use_parameters
    def get_voltage(self, axis="all"):
        """Get axis step amplitude in Volts"""
        reply=self.query("getv {}".format(axis))
        return self._parse_float_reply(reply,"voltage","V")
    @muxaxis(mux_argnames="voltage")
    @interface.use_parameters
    def set_voltage(self, axis, voltage):
        """Set axis step amplitude in Volts"""
        self.query("setv {} {}".format(axis,voltage))
        return self._wip.get_voltage(axis)
    @muxaxis
    @interface.use_parameters
    def get_offset(self, axis="all"):
        """Get axis offset voltage in Volts"""
        reply=self.query("geta {}".format(axis))
        return self._parse_float_reply(reply,"voltage","V")
    @muxaxis(mux_argnames="voltage")
    @interface.use_parameters
    def set_offset(self, axis, voltage):
        """Set axis offset voltage in Volts"""
        self.query("seta {} {}".format(axis,voltage))
        return self._wip.get_offset(axis)
    @muxaxis
    @interface.use_parameters
    def get_output(self, axis="all"):
        """Get axis current output voltage in Volts"""
        reply=self.query("geto {}".format(axis))
        return self._parse_float_reply(reply,"voltage","V")
    @muxaxis
    @interface.use_parameters
    def get_frequency(self, axis="all"):
        """Get axis step frequency in Hz"""
        reply=self.query("getf {}".format(axis))
        return self._parse_float_reply(reply,"frequency","Hz")
    @muxaxis(mux_argnames="freq")
    @interface.use_parameters
    def set_frequency(self, axis, freq):
        """Set axis step frequency in Hz"""
        self.query("setf {} {}".format(axis,freq))
        return self._wip.get_frequency(axis)
    @muxaxis
    @interface.use_parameters
    def get_capacitance(self, axis="all", measure=False):
        """
        Get capacitance measurement on the axis.
        
        If ``measure==True``, re-measure axis capacitance (takes about a second); otherwise, get the last measurement value.
        """
        if measure:
            self._wip.measure_capacitance(axis,wait=True)
        reply=self.query("getc {}".format(axis))
        return self._parse_float_reply(reply,"capacitance","nF")*1E-9
    
    _p_pattern_kind=interface.EnumParameterClass("pattern_kind",["up","down"])
    @interface.use_parameters(kind="pattern_kind")
    def get_voltage_pattern(self, axis, kind):
        """
        Get axis voltage pattern.

        `kind` be either ``"up"`` for up pattern or ``"down"`` for down pattern.
        The pattern is a numpy array of 256 numbers from 0 to 255 corresponding to the output voltage from 0 to the axis voltage.
        This pattern is output (repeatedly) for each step. The default is a simple linear ramp.
        """
        comm="getpu" if kind=="up" else "getpd"
        data=self.query("{} {}".format(comm,axis))
        return np.array([int(v) for v in data.split()])
    @interface.use_parameters(kind="pattern_kind")
    def set_voltage_pattern(self, axis, kind, pattern=None):
        """
        Set axis voltage pattern.

        `kind` be either ``"up"`` for up pattern or ``"down"`` for down pattern.
        The pattern is an array of 256 numbers from 0 to 255 corresponding to the output voltage from 0 to the axis voltage.
        This pattern is output (repeatedly) for each step. The default is a simple linear ramp, which is set if ``pattern is None``.
        """
        if pattern is None:
            pattern=np.arange(256) if kind=="up" else np.arange(255,-1,-1)
        else:
            pattern=np.array(pattern,dtype=int)
            if len(pattern)!=256:
                raise ValueError("pattern length should be 256; received {}".format(len(pattern)))
            pattern[pattern<0]=0
            pattern[pattern>255]=255
        spattern=" ".join([str(v) for v in pattern])
        comm="setpu" if kind=="up" else "setpd"
        self.query("{} {} {}".format(comm,axis,spattern))
        return self._wip.get_voltage_pattern(axis,kind)

    def _parse_trigger_reply(self, reply):
        v=self._parse_string_reply(reply,"trigger")
        return "off" if v=="off" else int(v)
    @muxaxis
    @interface.use_parameters
    def get_trigger_input(self, axis="all"):
        """
        Get trigger input lines for the given axis.

        Return tuple ``(up, down)`` with values for up and down step triggers, which can be either integer with the trigger line number, or ``"off"`` if the trigger is off.
        """
        tup=self._parse_trigger_reply(self.query("gettu {}".format(axis)))
        tdown=self._parse_trigger_reply(self.query("gettd {}".format(axis)))
        return (tup,tdown)
    @muxaxis(mux_argnames=("up","down"))
    @interface.use_parameters
    def set_trigger_input(self, axis, up=None, down=None):
        """
        Set trigger input lines for the given axis.

        `up` and `down` are can be integer with the trigger line number, ``"off"`` if the trigger is off, or ``None`` (keep the value unchanged).
        """
        if up is not None:
            self.query("settu {} {}".format(axis,up))
        if down is not None:
            self.query("settd {} {}".format(axis,down))
        return self._wip.get_trigger_input(axis)
    @muxaxis
    @interface.use_parameters
    def get_external_input_modes(self, axis="all"):
        """
        Get external BNC input modes.

        Return tuple ``(acin, dcin)`` indicating whether AC-IN and DC-IN channels are enabled.
        """
        reply=self.query("getaci {}".format(axis))
        acin=self._parse_string_reply(reply,"acin")=="on"
        reply=self.query("getdci {}".format(axis))
        dcin=self._parse_string_reply(reply,"dcin")=="on"
        return acin,dcin
    @muxaxis(mux_argnames=("acin","dcin"))
    @interface.use_parameters
    def set_external_input_modes(self, axis, acin=None, dcin=None):
        """
        Enable or disable external BNC inputs.

        `acin` and `dcin` are can be boolean indicating if the corresponding input is enabled, or ``None`` (keep the value unchanged).
        """
        if acin is not None:
            self.query("setaci {} {}".format(axis,"on" if acin else "off"))
        if dcin is not None:
            self.query("setdci {} {}".format(axis,"on" if dcin else "off"))
        return self._wip.get_external_input_modes(axis)


    @interface.use_parameters
    def get_axis_correction(self, axis):
        """
        Get axis correction factor.

        The factor is automatically applied when the motion is in the negative direction.
        """
        return self._correction[axis]
    @interface.use_parameters
    def set_axis_correction(self, axis, factor=1.):
        """
        Set axis correction factor.

        The factor is automatically applied when the motion is in the negative direction.
        """
        self._correction[axis]=factor
    
    @interface.use_parameters
    def jog(self, axis, direction):
        """
        Jog continuously in the given direction (``"+"`` or ``"-"``).
        
        The motion will continue until another move or stop command is called.
        """
        comm="stepu" if direction else "stepd"
        self.query("{} {} c".format(comm,axis))
    @interface.use_parameters
    def move_by(self, axis, steps=1):
        """Move a given axis for a given number of steps"""
        if steps<0:
            steps*=self._correction.get(axis,1.)
        steps=int(steps)
        if not steps:
            return
        comm="stepu" if steps>0 else "stepd"
        self.query("{} {} {}".format(comm,axis,abs(steps)))
    @interface.use_parameters
    def wait_move(self, axis, timeout=30.):
        """
        Wait for a given axis to stop moving.

        If the motion is not finished after `timeout` seconds, raise a backend error.
        """
        if axis=="all":
            for ax in self.get_all_axes():
                self.wait_move(ax,timeout=timeout)
            return
        with self.instr.using_timeout(timeout):
            self.query("stepw {}".format(axis))
    def is_moving(self, axis):
        """Check if a given axis is moving"""
        return self.get_output(axis)!=0.
    @muxaxis
    @interface.use_parameters
    def stop(self, axis="all"):
        """Stop motion of a given axis"""
        self.query("stop {}".format(axis))