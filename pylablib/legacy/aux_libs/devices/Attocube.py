from ...core.devio import backend as backend_mod  #@UnresolvedImport
from ...core.utils import py3, general
from ...core.utils.strpack import pack_uint, unpack_uint, pack_int, unpack_int

import re
import collections
import time

_depends_local=["...core.devio.backend"]


class AttocubeError(RuntimeError):
    """Generic Attocube error"""

class ANC300(backend_mod.IBackendWrapper):
    """
    Attocube ANC300 controller.

    Args:
        conn: connection parameters; for Ethernet connection is a tuple ``(addr, port)`` or a string ``"addr:port"``
        backend(str): communication backend; by default, try to determine from the communication parameters
        pwd(str): connection password for Ethernet connection (default is ``"123456"``)
    """
    def __init__(self, conn, backend="auto", pwd="123456"):
        if backend=="auto":
            backend=backend_mod.autodetect_backend(conn)
        if backend=="network":
            conn=backend_mod.NetworkDeviceBackend.combine_conn(conn,{"port":7230})
        instr=backend_mod.new_backend(conn,backend=backend,timeout=3.,term_write="\r\n")
        self.pwd=pwd
        backend_mod.IBackendWrapper.__init__(self,instr)
        self.open()
        self._correction={}
        self._add_settings_node("voltages",self.get_all_voltages,self.set_all_voltages)
        self._add_settings_node("offsets",self.get_all_offsets,self.set_all_offsets)
        self._add_settings_node("frequencies",self.get_all_frequencies,self.set_all_frequencies)
        self._add_status_node("voltage_output",self.get_all_outputs)
        self._add_status_node("capacitance",self.get_all_capacitances)

    def open(self):
        """Open the connection to the stage"""
        res=self.instr.open()
        if self.instr._backend=="network" and self.pwd is not None:
            self.instr.write(self.pwd)
        self.instr.write("echo off")
        self.instr.flush_read()
        self.update_available_axes()
        return res
    
    def query(self, msg):
        """Send a query to the stage and return the reply"""
        self.instr.flush_read()
        self.instr.write(msg)
        reply=self.instr.read_multichar_term(["ERROR","OK"],remove_term=False)
        self.instr.flush_read()
        if reply.upper().endswith(b"ERROR"):
            raise AttocubeError(reply[:-5].strip())
        return reply[:-2].strip()
    
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
        self.axes=list(axes)
        return axes

    def set_mode(self, axis="all", mode="stp"):
        """
        Set axis mode.

        `axis` is either an axis index (starting from 1), or ``"all"`` (all axes).
        `mode` is ``"gnd"`` (ground) or ``"stp"`` (step).
        """
        if axis=="all":
            for ax in self.axes:
                self.set_mode(ax,mode)
            return
        self.query("setm {} {}".format(axis,mode))
    def get_mode(self, axis="all"):
        """
        Get axis mode

        `axis` is either an axis index (starting from 1), or ``"all"`` (all axes).
        """
        if axis=="all":
            return [self.get_mode(ax) for ax in self.axes]
        reply=py3.as_str(self.query("getm {}".format(axis))).strip()
        if reply.startswith("mode = "):
            return reply[7:].strip()
        raise AttocubeError("unexpected reply: {}".format(reply))
    def enable_axis(self, axis, mode="stp"):
        """Enable specific axis (set to step mode)"""
        self.set_mode(axis,mode=mode)
    def disable_axis(self, axis):
        """Disable specific axis (set to ground mode)"""
        self.set_mode(axis,mode="gnd")
    def enable_all(self, mode="stp"):
        """Enable all axes (set to step mode)"""
        self.set_mode("all",mode=mode)
    def disable_all(self):
        """Disable all axes (set to ground mode)"""
        self.set_mode("all",mode="gnd")
    def measure_capacitance(self, axis="all", wait=True):
        """
        Measure axis capacitance; finish in the GND mode.
        
        If ``wait==True``, wait until the capacitance measurement is finished (takes about a second per axis).
        """
        if axis=="all":
            for ax in self.axes:
                self.measure_capacitance(ax,wait=wait)
            return
        self.set_mode(axis,mode="gnd")
        time.sleep(0.05)
        self.set_mode(axis,mode="cap")
        if wait:
            time.sleep(0.05)
            while self.get_mode(axis)!="gnd":
                time.sleep(0.1)

    def _parse_reply(self, reply, name, units):
        patt=name+r"\s*=\s*([\d.]+)\s*"+units
        reply=py3.as_str(reply)
        m=re.match(patt,reply,re.IGNORECASE)
        if not m:
            raise AttocubeError("unexpected reply: {}".format(reply))
        return float(m.groups()[0])
    def get_voltage(self, axis):
        """Get axis step voltage in Volts"""
        reply=self.query("getv {}".format(axis))
        return self._parse_reply(reply,"voltage","V")
    def set_voltage(self, axis, voltage):
        """Set axis step voltage in Volts"""
        self.query("setv {} {}".format(axis,voltage))
        return self.get_voltage(axis)
    def get_offset(self, axis):
        """Get axis offset voltage in Volts"""
        reply=self.query("geta {}".format(axis))
        return self._parse_reply(reply,"voltage","V")
    def set_offset(self, axis, voltage):
        """Set axis offset voltage in Volts"""
        self.query("seta {} {}".format(axis,voltage))
        return self.get_offset(axis)
    def get_output(self, axis):
        """Get axis current output voltage in Volts"""
        reply=self.query("geto {}".format(axis))
        return self._parse_reply(reply,"voltage","V")
    def get_frequency(self, axis):
        """Get axis step frequency in Hz"""
        reply=self.query("getf {}".format(axis))
        return self._parse_reply(reply,"frequency","Hz")
    def set_frequency(self, axis, freq):
        """Set axis step frequency in Hz"""
        self.query("setf {} {}".format(axis,freq))
        return self.get_frequency(axis)
    def get_capacitance(self, axis, measure=False):
        """
        Get capacitance measurement on the axis.
        
        If ``measure==True``, re-measure axis capacitance (takes about a second); otherwise, get the last measurement value.
        """
        if measure:
            self.measure_capacitance(axis,wait=True)
        reply=self.query("getc {}".format(axis))
        return self._parse_reply(reply,"capacitance","nF")*1E-9

    def _get_all_axes_data(self, getter):
        return dict([(a,getter(a)) for a in self.axes])
    def get_all_voltages(self):
        """Get the list of all axes step voltages"""
        return self._get_all_axes_data(self.get_voltage)
    def get_all_offsets(self):
        """Get the list of all axes offset voltages"""
        return self._get_all_axes_data(self.get_offset)
    def get_all_outputs(self):
        """Get the list of all axes offset voltages"""
        return self._get_all_axes_data(self.get_output)
    def get_all_frequencies(self):
        """Get the list of all axes step frequencies"""
        return self._get_all_axes_data(self.get_frequency)
    def get_all_capacitances(self, measure=False):
        """
        Get the list of all axes capacitances
        
        If ``measure==True``, re-measure axes capacitances (takes about a secon0d per axis); otherwise, get the last measurement values.
        """
        return self._get_all_axes_data(lambda axis: self.get_capacitance(axis,measure=measure))
    
    def _set_all_axes_data(self, setter, values):
        if isinstance(values,(tuple,list)):
            values=dict(zip([self.axes,values]))
        for a,v in values.items():
            setter(a,v)
    def set_all_voltages(self, voltages):
        """
        Get all axes step voltages.
        
        `voltages` is a list of step voltage, whose length is equal to the number of active (connected) axes.
        """
        self._set_all_axes_data(self.set_voltage,voltages)
        return self.get_all_voltages()
    def set_all_offsets(self, offsets):
        """
        Get all axes offset voltages
        
        `offsets` is a list of offset voltags, whose length is equal to the number of active (connected) axes.
        """
        self._set_all_axes_data(self.set_offset,offsets)
        return self.get_all_offsets()
    def set_all_frequencies(self, frequencies):
        """
        Get all axes step frequencies
        
        `frequencies` is a list of step frequencies, whose length is equal to the number of active (connected) axes.
        """
        self._set_all_axes_data(self.set_frequency,frequencies)
        return self.get_all_frequencies()

    def set_axis_correction(self, axis, factor=1.):
        """
        Set axis correction factor.

        The factor is automatically applied when the motion is in the negative direction.
        """
        self._correction[axis]=factor
    def move(self, axis, steps=1):
        """Move a given axis for a given number of steps"""
        if steps<0:
            steps*=self._correction.get(axis,1.)
        steps=int(steps)
        if not steps:
            return
        comm="stepu" if steps>0 else "stepd"
        self.query("{} {} {}".format(comm,axis,abs(steps)))
    def wait_for_axis(self, axis, timeout=30.):
        """
        Wait for a given axis to stop moving.

        If the motion is not finished after `timeout` seconds, raise a backend error.
        """
        with self.instr.using_timeout(timeout):
            self.query("stepw {}".format(axis))
    def is_moving(self, axis):
        """Check if a given axis is moving"""
        return self.get_output(axis)!=0.
    def stop(self, axis):
        """Stop motion of a given axis"""
        self.query("stop {}".format(axis))
    def stop_all(self):
        """Stop motion of all axes"""
        for ax in self.axes:
            self.stop(ax)

ANCDevice=ANC300





class ANC350(backend_mod.IBackendWrapper):
    """
    Attocube ANC350 controller.

    Args:
        conn: connection parameters - index of the Attocube ANC350 in the system (for a single controller leave 0)
        timeout(float): default operation timeout
    """
    def __init__(self, conn=0, timeout=5.):
        if isinstance(conn,int):
            conn=(0x16C0,0x055B,conn,0x86,0x02,"libusb0") # default device IDs
        backend_mod.IBackendWrapper.__init__(self,None)
        instr=backend_mod.new_backend(conn,backend="pyusb",timeout=timeout,check_read_size=False)
        self._corr_number=0
        self._tell_telegrams={}
        backend_mod.IBackendWrapper.__init__(self,instr)
        self.open()
        self.instr.read(512)
        self.set_value(0x000A,0,0)
        self.enable_updates(False)
        self.axes=[0,1,2]
        self._add_settings_node("voltages",self.get_all_voltages,self.set_all_voltages)
        self._add_settings_node("offsets",self.get_all_offsets,self.set_all_offsets)
        self._add_settings_node("frequencies",self.get_all_frequencies,self.set_all_frequencies)
        self._add_status_node("positions",self.get_all_positions)
        self._add_status_node("target_positions",self.get_all_target_positions)

    def _check_axis(self, axis):
        if axis not in self.axes:
            raise AttocubeError("invalid axis: {}".format(axis))

    def _make_telegram(self, opcode, address, index=0, data=b"", add_corr=True):
        data=data[:(len(data)//4)*4]
        l=16+len(data)
        if add_corr:
            self._corr_number=(self._corr_number%0xFFFF)+1
            corr_number=self._corr_number
        else:
            corr_number=0
        return b"".join([pack_uint(v,4,"<") for v in [l,opcode,address,index,corr_number]])+data
    Telegram=collections.namedtuple("Telegram",["opcode","address","index","data","corr_number"])
    def _parse_telegram(self, telegram):
        if len(telegram)<20:
            raise ValueError("data is too short: {}".format(len(telegram)))
        l,opcode,address,index,corr_number=[unpack_uint(telegram[i*4:i*4+4],"<") for i in range(5)]
        if len(telegram)!=l+4:
            raise ValueError("wrong telegram length: expected {}, got {}".format(l+4,len(telegram)))
        return self.Telegram(opcode,address,index,telegram[20:],corr_number)
    
    def _read_telegram(self, corr_number=None):
        ctd=general.Countdown(self.instr.timeout)
        while True:
            tg=self._parse_telegram(self.instr.read(512))
            if tg.opcode==3: # ACK
                if corr_number is None or tg.corr_number==corr_number:
                    return tg
                raise AttocubeError("gut unexpected correlation number: {}, expected {}".format(tg.corr_number,corr_number))
            if tg.opcode==4: # TELL
                if (tg.address>>8)!=0x0F:
                    self._tell_telegrams[(tg.address,tg.index)]=tg
            if ctd.passed():
                raise AttocubeError("timeout while read")
    Reply=collections.namedtuple("Reply",["address","index","reason","data"])
    def _write(self, opcode, address, index=0, data=b""):
        if isinstance(data, int):
            data=pack_int(data,4,"<")
        tg=self._make_telegram(opcode,address,index,data,add_corr=False)
        self.instr.write(tg)
    def _query(self, opcode, address, index=0, data=b""):
        if isinstance(data, int):
            data=pack_int(data,4,"<")
        tg=self._make_telegram(opcode,address,index,data)
        self.instr.write(tg)
        resp=self._read_telegram(self._corr_number)
        reason=unpack_uint(resp.data[:4],"<")
        return self.Reply(resp.address,resp.index,reason,resp.data[4:])

    def check_tell(self, timeout=0.01):
        """Check for queued TELL (periodic value update) commands"""
        try:
            with self.instr.using_timeout(timeout):
                self._read_telegram()
        except (AttocubeError,self.instr.Error):
            pass
    def set_value(self, address, index, value, ack=False, return_reason=False):
        """
        Set device value at the given address and index.
        
        If ``ack==True``, request ACK responds and return its value; otherwise, return immediately after set.
        If ``return_reason==True``, return tuple ``(result, reason)``; otherwise, simply return result.
        """
        if ack:
            resp=self._query(0,address,index,value)
            res=resp.data
            if isinstance(value,int):
                res=unpack_int(res,"<")
            return resp.reason,res
        else:
            self._write(0,address,index,value)
    def get_value(self, address, index, as_int=True, return_reason=False):
        """
        Get device value at the given address and index.
        
        If ``as_int==True``, convert the result into a signed integer; otherwise return raw byte string.
        If ``return_reason==True``, return tuple ``(result, reason)``; otherwise, simply return result.
        """
        resp=self._query(1,address,index)
        res=resp.data
        if as_int:
            res=unpack_int(res,"<")
        return (res,resp.reason) if return_reason else res
    def _read_register(self, address):
        idx=0
        res=b""
        while True:
            data=self.get_value(address,idx,as_int=False)
            eoln_pos=data.find(b"\x00")
            if eoln_pos>=0:
                res+=data[:eoln_pos]
                return res
            res+=data
            idx+=1


    def enable_updates(self, enabled=True):
        """Enable or disable periodic TELL updates"""
        self.set_value(0x0145,0,1 if enabled else 0)    
    def get_hardware_id(self):
        """Return device HWID (by default -1)"""
        return self.get_value(0x0168,0)
    
    
    def is_axis_connected(self, axis):
        """Check if axis is connected"""
        self._check_axis(axis)
        return bool(self.get_value(0x3002,axis))
    def enable_axis(self, axis):
        """Enable specific axis"""
        self._check_axis(axis)
        self.set_value(0x3030,axis,1)
    def disable_axis(self, axis):
        self._check_axis(axis)
        """Disable specific axis"""
        self.set_value(0x3030,axis,0)
    def enable_all(self):
        """Enable all axes (set to step mode)"""
        for ax in self.axes:
            self.enable_axis(ax)
    def disable_all(self):
        """Disable all axes (set to ground mode)"""
        for ax in self.axes:
            self.disable_axis(ax)

    def get_voltage(self, axis):
        """Get axis step voltage in Volts"""
        self._check_axis(axis)
        return self.get_value(0x0400,axis)*1E-3
    def set_voltage(self, axis, voltage):
        """Set axis step voltage in Volts"""
        self._check_axis(axis)
        self.set_value(0x0400,axis,int(voltage*1E3))
        return self.get_voltage(axis)
    def get_offset(self, axis):
        """Get axis offset voltage in Volts"""
        self._check_axis(axis)
        return self.get_value(0x0514,axis)*1E-3
    def set_offset(self, axis, voltage):
        """Set axis offset voltage in Volts"""
        self._check_axis(axis)
        self.set_value(0x0514,axis,int(voltage*1E3))
        return self.get_offset(axis)
    def get_frequency(self, axis):
        """Get axis step frequency in Hz"""
        self._check_axis(axis)
        return self.get_value(0x0401,axis)
    def set_frequency(self, axis, freq):
        """Set axis step frequency in Hz"""
        self._check_axis(axis)
        self.set_value(0x0401,axis,int(freq))
        return self.get_frequency(axis)
    
    def _get_all_axes_data(self, getter):
        return dict([(a,getter(a)) for a in self.axes])
    def get_all_voltages(self):
        """Get the list of all axes step voltages"""
        return self._get_all_axes_data(self.get_voltage)
    def get_all_offsets(self):
        """Get the list of all axes offset voltages"""
        return self._get_all_axes_data(self.get_offset)
    def get_all_frequencies(self):
        """Get the list of all axes step frequencies"""
        return self._get_all_axes_data(self.get_frequency)
    def get_all_positions(self):
        """Get the list of all axes positions"""
        return self._get_all_axes_data(self.get_position)
    def get_all_target_positions(self):
        """Get the list of all axes target positions"""
        return self._get_all_axes_data(self.get_target_position)

    def _set_all_axes_data(self, setter, values):
        if isinstance(values,(tuple,list)):
            values=dict(zip([self.axes,values]))
        for a,v in values.items():
            setter(a,v)
    def set_all_voltages(self, voltages):
        """
        Get all axes step voltages.
        
        `voltages` is a list of step voltage, whose length is equal to the number of active (connected) axes.
        """
        self._set_all_axes_data(self.set_voltage,voltages)
        return self.get_all_voltages()
    def set_all_offsets(self, offsets):
        """
        Get all axes offset voltages
        
        `offsets` is a list of offset voltags, whose length is equal to the number of active (connected) axes.
        """
        self._set_all_axes_data(self.set_offset,offsets)
        return self.get_all_offsets()
    def set_all_frequencies(self, frequencies):
        """
        Get all axes step frequencies
        
        `frequencies` is a list of step frequencies, whose length is equal to the number of active (connected) axes.
        """
        self._set_all_axes_data(self.set_frequency,frequencies)
        return self.get_all_frequencies()

    def get_position(self, axis):
        """Get axis position (in m)"""
        self._check_axis(axis)
        return self.get_value(0x0415,axis)*1E-9
    def move_to(self, axis, position):
        """Move to target position (in m)"""
        self._check_axis(axis)
        self.set_value(0x0408,axis,int(position*1E9))
        self.set_value(0x040D,axis,1)
    def move(self, axis, steps=1):
        """Move a given axis for a given number of steps"""
        self._check_axis(axis)
        steps=int(steps)
        if steps>=0:
            tg=self._make_telegram(0,0x0410,axis,b"\x01\x00\x00\x00",add_corr=False)
        else:
            tg=self._make_telegram(0,0x0411,axis,b"\x01\x00\x00\x00",add_corr=False)
            steps=-steps
        for _ in range(steps):
            self.instr.write(tg)
            
    def is_moving(self, axis):
        """Move a given axis for a given number of steps"""
        self._check_axis(axis)
        return bool(self.get_value(0x302E,axis))
    def get_target_position(self, axis):
        """Get the target position for the given axis"""
        self._check_axis(axis)
        return self.get_value(0x0408,axis)*1E-9
    def is_target_reached(self, axis, precision=1E-9):
        """
        Check if the target position is reached.
        
        Precision sets the final positioning precision (in m).
        """
        self._check_axis(axis)
        self.set_value(0x3036,axis,int(precision*1E9))
        return self.get_value(0x3037,axis)
    def wait_for_axis(self, axis, precision=1E-9, timeout=10., period=0.01):
        """
        Wait for a given axis to stop moving or to reach target position.

        If the motion is not finished after `timeout` seconds, raise a backend error.
        Precision sets the final positioning precision (in m).
        """
        self._check_axis(axis)
        ctd=general.Countdown(timeout)
        while True:
            if (not self.is_moving(axis)) or self.is_target_reached(axis):
                return
            if ctd.passed():
                raise AttocubeError("axis waiting timeout error")
            time.sleep(period)

    
    def stop(self, axis):
        """Stop motion of a given axis"""
        self._check_axis(axis)
        self.set_value(0x0410,axis,0)
    def stop_all(self):
        """Stop motion of all axes"""
        for axis in self.axes:
            self.stop(axis)
    
    def jog(self, axis, direction):
        """
        Jog a given axis in a given direction.
        
        `direction` can be either ``"-"`` (negative) or ``"+"`` (positive).
        The motion continues until it is explicitly stopped, or unitl a limit is hit.
        """
        if not direction: # 0 or False also mean left
            direction="-"
        if direction in [1, True]:
            direction="+"
        if direction not in ["+","-"]:
            raise AttocubeError("unrecognized direction: {}".format(direction))
        self._check_axis(axis)
        if direction=="+":
            self.set_value(0x040E,axis,1)
        else:
            self.set_value(0x040F,axis,1)