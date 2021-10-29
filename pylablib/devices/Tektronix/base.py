import numpy as np

from ...core.devio import SCPI, data_format, interface, comm_backend
from ...core.utils import funcargparse, general

import collections


class TektronixError(comm_backend.DeviceError):
    """Generic Tektronix devices error"""
class TektronixBackendError(TektronixError,comm_backend.DeviceBackendError):
    """Generic Tektronix backend communication error"""

def muxchannel(*args, **kwargs):
    """Multiplex the function over its channel argument"""
    if len(args)>0:
        return muxchannel(**kwargs)(args[0])
    def ch_func(self, *_, **__):
        return list(self._main_channels_idx)
    return general.muxcall("channel",special_args={"all":ch_func},mux_argnames=kwargs.get("mux_argnames",None),return_kind=kwargs.get("return_kind","list"),allow_partial=True)
TTriggerParameters=collections.namedtuple("TTriggerParameters",["source","level","coupling","slope"])
class ITektronixScope(SCPI.SCPIDevice):
    """
    Generic Tektronix oscilloscope.
    
    Args:
        addr: device address; usually a VISA address string such as ``"USB0::0x0699::0x0364::C000000::INSTR"``
        nchannels: can specify number of channels on the oscilloscope; by default, autodetect number of channels (might take several seconds on connection)
    """
    _wfmpre_comm="WFMP"  # command used to obtain waveform preamble
    _trig_comm="TRIGGER:MAIN"  # command used to set up trigger
    _software_trigger_delay=0.3 # delay between issuing a single acquisition and sending the software trigger; if the trigger is sent sooner, it is ignored
    _probe_attenuation_comm=("PROBE","att")
    # _default_operation_cooldown={"write":2E-3}
    _main_channels_idx="specify"  # ids of main channels (integers); "specify" means the number is specified in constructor; specified "auto" means that they get autodetected on connection
    _aux_channels=[]  # names of aux channels (strings)
    # horizontal offset method; either ``"delay"`` (use ``"HORizontal:DELay:TIMe"``), ``"pos"`` (use ``"HORizontal:POSition"``, and set ``"HORizontal:DELay:MODe"`` accordingly),
    # or ``"pos_only"`` (use ``"HORizontal:POSition"``, don't set ``"HORizontal:DELay:MODe"`` in case it's not available)
    _hor_offset_method="pos_only"
    _hor_pos_mode="real_center"  # mode of :HORIZONTAL:POS command; can be "real_center", if time position of the sample is specified (0 is centered), or "frac" if fraction to the left is specified (50 is centered)
    _default_backend_timeout=10.
    Error=TektronixError
    ReraiseError=TektronixBackendError
    def __init__(self, addr, nchannels="auto"):
        SCPI.SCPIDevice.__init__(self,addr)
        if self._main_channels_idx=="specify":
            if nchannels=="auto":
                nchannels=self._detect_main_channels_number()
            self._main_channels_idx=list(range(1,nchannels+1))
        self._main_channels=[(i,"ch{}".format(i)) for i in self._main_channels_idx]
        self._add_parameter_class(interface.EnumParameterClass("input_channel",self._main_channels,value_case="upper"))
        self._add_parameter_class(interface.EnumParameterClass("channel",self._main_channels+self._aux_channels,value_case="upper"))
        self.default_data_fmt="<i1"
        self._add_info_variable("channels_number",self.get_channels_number)
        self._add_info_variable("channels",self.get_channels)
        self._add_settings_variable("edge_trigger/source",self.get_edge_trigger_source,self.set_edge_trigger_source)
        self._add_settings_variable("edge_trigger/coupling",self.get_edge_trigger_coupling,self.set_edge_trigger_coupling)
        self._add_settings_variable("edge_trigger/slope",self.get_edge_trigger_slope,self.set_edge_trigger_slope)
        self._add_settings_variable("edge_trigger/level",self.get_trigger_level,self.set_trigger_level)
        self._add_settings_variable("horizontal_span",self.get_horizontal_span,self.set_horizontal_span)
        self._add_settings_variable("horizontal_offset",self.get_horizontal_offset,self.set_horizontal_offset)
        self._add_settings_variable("enabled",self.is_channel_enabled,self.enable_channel,mux=(self._main_channels_idx,))
        self._add_settings_variable("vertical_span",self.get_vertical_span,self.set_vertical_span,mux=(self._main_channels_idx,))
        self._add_settings_variable("vertical_position",self.get_vertical_position,self.set_vertical_position,mux=(self._main_channels_idx,))
        self._add_settings_variable("coupling",self.get_coupling,self.set_coupling,mux=(self._main_channels_idx,))
        self._add_settings_variable("probe_attenuation",self.get_probe_attenuation,self.set_probe_attenuation,mux=(self._main_channels_idx,))

    def _detect_main_channels_number(self):
        ch=1
        while ch<=16:
            if self._is_command_valid(":CH{}:POSITION?".format(ch+1)):
                ch+=1
            else:
                break
        return ch
    def get_channels_number(self):
        """Get the number of channels"""
        return len(self._main_channels_idx)
    def get_channels(self, only_main=False):
        """Get the list of all input channels (if ``only_main==True``) or all available channels (if ``only_main==False``)"""
        channels=["CH{}".format(i) for i in self._main_channels_idx]
        return channels if only_main else channels+self._aux_channels
    @interface.use_parameters
    def normalize_channel_name(self, channel):
        """Normalize channel name as represented by the oscilloscope"""
        return channel
    def grab_single(self, wait=True, software_trigger=False, wait_timeout=None):
        """
        Set single waveform grabbing and wait for acquisition.

        If ``wait==True``, wait until the acquisition is complete; otherwise, return immediately.
        if ``software_trigger==True``, send the software trigger after setup (i.e., the device triggers immediately regardless of the input).
        """
        self.write(":ACQ:STOPAFTER SEQ")
        self.write(":ACQ:STATE ON")
        if software_trigger:
            self.sleep(self._software_trigger_delay)
            self.force_trigger()
        if wait:
            self.wait_sync(timeout=wait_timeout)
    def wait_for_grabbing(self, timeout=None):
        """Wait until the acquisition is complete"""
        self.wait_sync(timeout=timeout)
    def grab_continuous(self, enable=True):
        """Start or stop continuous grabbing"""
        self.write(":ACQ:STOPAFTER RUNSTOP")
        self.write(":ACQ:STATE",enable)
    def stop_grabbing(self):
        """Stop grabbing or waiting (equivalent to ``self.grab_continuous(False)``)"""
        self.grab_continuous(enable=False)
    def is_continuous(self):
        """Check if grabbing is continuous or single"""
        return self.ask(":ACQ:STOPAFTER?").strip().upper().startswith("RUN")
    def is_grabbing(self):
        """
        Check if acquisition is in progress.

        Return ``True`` if the oscilloscope is recording data, or if the trigger is armed/ready and waiting; return ``False`` if the acquisition is stopped.
        To check if the trigger has been triggered, use :meth:`get_trigger_state`.
        """
        return self.ask(":ACQ:STATE?","bool")
    
    # TODO: set trigger kind (edge, etc.)
    @interface.use_parameters(_returns="channel")
    def get_edge_trigger_source(self):
        """
        Get edge trigger source.

        Can be an integer indicating channel number or a name of a special channel.
        """
        return self.ask(self._trig_comm+":EDGE:SOURCE?")
    @interface.use_parameters
    def set_edge_trigger_source(self, channel):
        """
        Get edge trigger source.

        Can be an integer indicating channel number or a name of a special channel.
        """
        self.write(self._trig_comm+":EDGE:SOURCE",channel)
        return self.get_edge_trigger_source()
    _p_coupling=interface.EnumParameterClass("coupling",["ac","dc","gnd"],value_case="upper")
    _p_trigger_coupling=interface.EnumParameterClass("trigger_coupling",["ac","dc"],value_case="upper")
    _p_slope=interface.EnumParameterClass("slope",["rise",("rise","ris"),"fall"],value_case="upper",match_prefix=True)
    @interface.use_parameters(_returns="trigger_coupling")
    def get_edge_trigger_coupling(self):
        """Get edge trigger coupling (``"ac"`` or ``"dc"``)"""
        return self.ask(self._trig_comm+":EDGE:COUPL?")
    @interface.use_parameters(coupling="trigger_coupling")
    def set_edge_trigger_coupling(self, coupling):
        """Set edge trigger coupling (``"ac"`` or ``"dc"``)"""
        self.write(self._trig_comm+":EDGE:COUPL",coupling)
        return self.get_edge_trigger_coupling()
    @interface.use_parameters(_returns="slope")
    def get_edge_trigger_slope(self):
        """Get edge trigger slope (``"fall"`` or ``"rise"``)"""
        return self.ask(self._trig_comm+":EDGE:SLOPE?")
    @interface.use_parameters
    def set_edge_trigger_slope(self, slope):
        """Set edge trigger slope (``"fall"`` or ``"rise"``)"""
        self.write(self._trig_comm+":EDGE:SLOPE",slope)
        return self.get_edge_trigger_slope()
    def get_trigger_level(self):
        """Get edge trigger level (in Volts)"""
        return self.ask(self._trig_comm+":LEVEL?","float")
    def set_trigger_level(self, level):
        """Set edge trigger level (in Volts)"""
        self.write(self._trig_comm+":LEVEL",level)
        return self.get_trigger_level()
    def _get_edge_trigger_params(self):
        return TTriggerParameters(self.get_edge_trigger_source(), self.get_trigger_level(), self.get_edge_trigger_coupling(), self.get_edge_trigger_slope())
    @interface.use_parameters(source="channel")
    def setup_edge_trigger(self, source, level, coupling="dc", slope="rise"):
        """
        Setup edge trigger.

        Set source, level, coupling and slope (see corresponding methods for details).
        """
        self.write(self._trig_comm+":EDGE:SOURCE",source)
        self.write(self._trig_comm+":EDGE:COUPL",coupling)
        self.write(self._trig_comm+":EDGE:SLOPE",slope)
        self.write(self._trig_comm+":LEVEL",level)
        self.write(self._trig_comm+":TYPE","EDGE")
        return self._get_edge_trigger_params()
    _p_trigger_mode=interface.EnumParameterClass("trigger_mode",["auto","norm"],value_case="upper",match_prefix=True)
    @interface.use_parameters(_returns="trigger_mode")
    def get_trigger_mode(self):
        """
        Get trigger mode.

        Can be either ``"auto"`` or ``"norm"``.
        """
        return self.ask(self._trig_comm+":MODE?")
    @interface.use_parameters
    def set_trigger_mode(self, trigger_mode="auto"):
        """
        Set trigger mode.

        Can be either ``"auto"`` or ``"norm"``.
        """
        self.write(self._trig_comm+":MODE",trigger_mode)
        return self.get_trigger_mode()
    
    _p_trigger_state=interface.EnumParameterClass("trigger_state",[("armed","arm"),"ready",("trigger","trig"),"auto",("save","sav"),"scan"],value_case="upper",match_prefix=True)
    @interface.use_parameters(_returns="trigger_state")
    def get_trigger_state(self):
        """
        Get trigger state.

        Can be ``"armed"`` (acquiring pretrigger), ``"ready"`` (pretrigger acquired, wait for trigger event), ``"trigger"`` (triggered, acquiring the rest of the waveform),
        ``"auto"`` (``"auto"`` mode trigger is acquiring data in the absence of trigger), ``"save"`` (acquisition is stopped), or ``"scan"`` (oscilloscope in the scan mode)
        """
        return self.ask("TRIGGER:STATE?")
    def force_trigger(self):
        """Force trigger event"""
        self.write("TRIGGER FORCE")


    def get_horizontal_span(self):
        """Get horizontal span (in seconds)"""
        return self.ask(":HORIZONTAL:SCALE?","float")*10. # scale is per division (10 division per screen)
    def set_horizontal_span(self, span):
        """Set horizontal span (in seconds)"""
        self.write(":HORIZONTAL:SCALE",span/10.,"float") # scale is per division (10 division per screen)
        return self.get_horizontal_span()
    def _to_horizontal_pos(self, center_time):
        if self._hor_pos_mode=="real_center":
            return center_time
        span=self.get_horizontal_span()
        rel_offset=(center_time/span*100)+50
        rel_offset=min(max(rel_offset,0),100)
        return rel_offset
    def _from_horizontal_pos(self, hor_pos):
        if self._hor_pos_mode=="real_center":
            return hor_pos
        span=self.get_horizontal_span()
        return (hor_pos/100.-.5)*span
    def get_horizontal_offset(self):
        """Get horizontal offset (position of the center of the sweep; in seconds)"""
        if self._hor_offset_method=="delay":
            self.write(":HORIZONTAL:DELAY:MODE 1")
            return self.ask(":HORIZONTAL:DELAY:TIME?","float")
        else:
            if self._hor_offset_method=="pos":
                self.write(":HORIZONTAL:DELAY:MODE 0")
            return self._from_horizontal_pos(self.ask(":HORIZONTAL:POS?","float"))
    def set_horizontal_offset(self, offset=0.):
        """Set horizontal offset (position of the center of the sweep; in seconds)"""
        if self._hor_offset_method=="delay":
            self.write(":HORIZONTAL:DELAY:MODE 1")
            self.write(":HORIZONTAL:DELAY:TIME",offset,"float")
        else:
            if self._hor_offset_method=="pos":
                self.write(":HORIZONTAL:DELAY:MODE 0")
            pos=self._to_horizontal_pos(offset)
            self.write(":HORIZONTAL:POS",pos,"float")
        return self.get_horizontal_offset()
    @muxchannel
    @interface.use_parameters(channel="input_channel")
    def get_vertical_span(self, channel):
        """Get channel vertical span (in V)"""
        return self.ask(":{}:SCALE?".format(channel),"float")*10. # scale is per division (10 division per screen)
    @muxchannel(mux_argnames="span")
    @interface.use_parameters(channel="input_channel")
    def set_vertical_span(self, channel, span):
        """Set channel vertical span (in V)"""
        self.write(":{}:SCALE".format(channel),span/10.,"float") # scale is per division (10 division per screen)
        return self._wip.get_vertical_span(channel)
    @muxchannel
    @interface.use_parameters(channel="input_channel")
    def get_vertical_position(self, channel):
        """Get channel vertical position (offset of the zero volt line; in V)"""
        return self.ask(":{}:POSITION?".format(channel),"float")*self._wip.get_vertical_span(channel)/10. # offset is in divisions (10 division per screen)
    @muxchannel(mux_argnames="position")
    @interface.use_parameters(channel="input_channel")
    def set_vertical_position(self, channel, position):
        """Set channel vertical position (offset of the zero volt line; in V)"""
        position/=self._wip.get_vertical_span(channel)/10. # position is in divisions (10 division per screen)
        self.write(":{}:POSITION".format(channel),position,"float")
        return self._wip.get_vertical_position(channel)
    

    @muxchannel
    @interface.use_parameters(channel="input_channel")
    def is_channel_enabled(self, channel):
        """Check if channel is enabled"""
        return self.ask(":SELECT:{}?".format(channel),"bool")
    @muxchannel(mux_argnames="enabled")
    @interface.use_parameters(channel="input_channel")
    def enable_channel(self, channel, enabled=True):
        """Enable or disable given channel"""
        self.write(":SELECT:{}".format(channel),enabled,"bool")
        return self._wip.is_channel_enabled(channel)
    @interface.use_parameters(_returns="input_channel")
    def get_selected_channel(self):
        """
        Get selected source channel.

        Return number if it is a real channel, or a string name otherwise.
        """
        return self.ask(":DATA:SOURCE?").strip()
    @interface.use_parameters(channel="input_channel")
    def select_channel(self, channel):
        """
        Select a channel to read data.

        Doesn't need to be called explicitly, if :meth:`read_multiple_sweeps` or :meth:`read_sweep` are used.
        """
        self.write(":DATA:SOURCE {}".format(channel))
        return self.get_selected_channel()
    def _normalize_channel(self, channel):
        return self._parameters["channel"](channel)
    def _get_channel(self, channel):
        """Get the specified channel, or the current if ``None``"""
        if channel is None:
            return self.get_selected_channel()
        return self._normalize_channel(channel)
    def _change_channel(self, channel=None):
        """Select a new channel if specified"""
        if channel is not None:
            self.select_channel(channel)
    @interface.use_parameters(channel="input_channel",_returns="coupling")
    @muxchannel
    def get_coupling(self, channel):
        """
        Get channel coupling.

        Can be ``"ac"``, ``"dc"``, or ``"gnd"``.
        """
        return self.ask(":{}:COUPL?".format(channel))
    @muxchannel(mux_argnames="coupling")
    @interface.use_parameters(channel="input_channel")
    def set_coupling(self, channel, coupling="dc"):
        """
        Set channel coupling.

        Can be ``"ac"``, ``"dc"``, or ``"gnd"``.
        """
        self.write(":{}:COUPL".format(channel),coupling)
        return self._wip.get_coupling(channel)
    @muxchannel
    @interface.use_parameters(channel="input_channel")
    def get_probe_attenuation(self, channel):
        """Get channel probe attenuation"""
        if not self._probe_attenuation_comm:
            return 1
        comm,kind=self._probe_attenuation_comm
        value=self.ask(":{}:{}?".format(channel,comm),"float")
        return value if kind=="att" else 1./value
    @muxchannel(mux_argnames="attenuation")
    @interface.use_parameters(channel="input_channel")
    def set_probe_attenuation(self, channel, attenuation):
        """Set channel probe attenuation"""
        if self._probe_attenuation_comm:
            comm,kind=self._probe_attenuation_comm
            self.write(":{}:{}".format(channel,comm),attenuation if kind=="att" else 1./attenuation)
        return self._wip.get_probe_attenuation(channel)

    
    def get_points_number(self, kind="send"):
        """
        Get number of datapoints in various context.

        ``kind`` defines the context.
        It can be ``"acq"`` (number of points acquired),
        ``"trace"`` (number of points in the source of the read-out trace; can be lower than ``"acq"`` if the data resolution is reduced, or if the source is not a channel data),
        or ``"send"`` (number of points in the sent waveform; can be lower than ``"trace"`` if :meth:`get_data_pts_range` is used to specify and incomplete range).
        Not all kinds are defined for all scope model (e.g., ``"trace"`` is not defined for TDS2000 series oscilloscopes).
        
        For length of read-out trace, see also :meth:`get_data_pts_range`.
        """
        funcargparse.check_parameter_range(kind,"kind",{"acq","trace","send"})
        if kind=="acq":
            return self.ask(":HORIZONTAL:RECORDLENGTH?","int")
        elif kind=="trace":
            return self.ask(":{}:RECORDLENGTH?".format(self._wfmpre_comm),"int")
        else:
            return self.ask(":{}:NR_PT?".format(self._wfmpre_comm),"int")
    def _set_data_resolution(self, resolution):
        """Implemented in specific oscilloscope classes"""
    def set_points_number(self, pts_num, reset_limits=True):
        """
        Set number of datapoints to record when acquiring a trace.

        If ``reset_limits==True``, reset the datapoints range (:meth:`set_data_pts_range`) to the full range.
        The actual set value (returned by this method) can be different from the requested value.
        """
        if pts_num<5E4:
            self._set_data_resolution("REDUCED")
        else:
            self._set_data_resolution("FULL")
        self.write(":HORIZONTAL:RECORDLENGTH",pts_num,"int")
        if reset_limits:
            self.set_data_pts_range()
        return self.get_points_number(kind="send")
    def get_data_pts_range(self):
        """
        Get range of data points to read.

        The range is defined from 1 to the points number (returned by :meth:`get_points_number`).
        """
        return self.ask(":DATA:START?","int"),min(self.ask(":DATA:STOP?","int"),self.get_points_number())
    def set_data_pts_range(self, rng=None):
        """
        Set range of data points to read.

        The range is defined from 1 to the points number (returned by :meth:`get_points_number` with ``kind="acq"``).
        If ``rng is None``, set the full range.
        """
        if rng is None:
            start,stop=1,self.get_points_number(kind="acq")
        else:
            start,stop=min(rng),max(rng)
        self.write(":DATA:START",start,"int")
        self.write(":DATA:STOP",stop,"int")
        return self.get_data_pts_range()
    
    def set_data_format(self, fmt="default"):
        """
        Set data transfer format.

        `fmt` is a string describing the format; can be either ``"ascii"``, or a numpy-style format string (e.g., ``"<u2"``).
        If ``"default"``, use the oscilloscope default format (usually binary with smallest appropriate byte size).
        """
        if fmt=="default":
            fmt=self.default_data_fmt
        fmt=data_format.DataFormat.from_desc(fmt)
        if fmt.is_ascii():
            self.write(":DATA:ENCDG ASCII")
        else:
            if (fmt.kind not in "iu") or (fmt.size not in {1,2}):
                raise ValueError("format {0} isn't supported".format(fmt))
            if fmt.kind=="i":
                dfmt="RIBINARY"
            else:
                dfmt="RPBINARY"
            if fmt.byteorder==">":
                dfmt="S"+dfmt
            self.write(":DATA:ENCDG",dfmt)
            self.write(":DATA:WIDTH",fmt.size)
        return self.get_data_format()
    def _build_data_format(self, dfmt, size):
        if dfmt.startswith("ASC"):
            return data_format.DataFormat(None,"ascii",None)
        if dfmt[0]=="S":
            border=">"
            dfmt=dfmt[1:]
        else:
            border="<"
        kind="i" if dfmt[1]=="I" else "u"
        return data_format.DataFormat(size,kind,border)
    def get_data_format(self):
        """
        Get data transfer format.

        Return a string describing the format; can be either ``"ascii"``, or a numpy-style format string (e.g., ``"<u2"``).
        """
        dfmt=self.ask(":DATA:ENCDG?").upper()
        size=self.ask(":DATA:WIDTH?","int")
        return self._build_data_format(dfmt,size).to_desc()

    def _build_wfmpre(self, data):
        if len(data)<15:
            raise self.Error("incomplete preamble: {}".format(data))
        wfmpre={}
        wfmpre["fmt"]=data_format.DataFormat.from_desc("ascii") if data[2].startswith("ASC") else self._build_data_format(data[3],data[0])
        wfmpre["pts"]=int(data[5])
        wfmpre["xzero"]=float(data[10])
        wfmpre["xincr"]=float(data[8])
        wfmpre["ptoff"]=int(data[9])
        wfmpre["ymult"]=float(data[12])
        wfmpre["yzero"]=float(data[13])
        wfmpre["yoff"]=float(data[14])
        return wfmpre
    def get_wfmpre(self, channel=None, enable=True):
        """
        Get preamble dictionary describing all scaling and format data for the given channel or a list of channels.

        Can be acquired once and used in subsequent multiple reads to save time on re-requesting.
        If `channel` is ``None``, use the currently selected channel.
        If ``enable==True``, make sure that the requested channel is enabled; getting preamble for disabled channels raises an error.
        """
        if isinstance(channel,(list,tuple)):
            return {self._normalize_channel(ch):self.get_wfmpre(ch,enable=enable) for ch in channel}
        self._change_channel(channel)
        if enable:
            channel=self._get_channel(channel)
            if not self.is_channel_enabled(channel):
                self.enable_channel(channel)
        data=self.ask(":{}?".format(self._wfmpre_comm)).split(";")
        data=[d.strip().upper() for d in data]
        return self._build_wfmpre(data)
    
    def read_raw_data(self, channel=None, fmt=None, timeout=None):
        """
        Request, read and parse raw data at a given channel.

        `fmt` is data format (e.g., ``"i1"``, ``"<i2"``, or ``"ascii"``) or ``"default"``,
        which uses the default oscilloscope format (usually binary with smallest appropriate byte size).
        If `fmt` is ``None``, use the current format.
        If `channel` is ``None``, use the currently selected channel.

        Returned data is raw (i.e., not scaled and without x axis).
        """
        if fmt is None:
            fmt=self.get_data_format()
        else:
            fmt=self.set_data_format(fmt)
        self._change_channel(channel)
        self.write(":CURVE?")
        fmt=data_format.DataFormat.from_desc(fmt)
        if fmt.is_ascii():
            data=self.read("raw",timeout=timeout)
        else:
            data=self.read_binary_array_data(timeout=timeout)
        return self.parse_array_data(data,fmt)
    def _scale_data(self, data, wfmpre=None):
        wfmpre=wfmpre or self.get_wfmpre()
        xpts=(np.arange(len(data))-wfmpre["ptoff"])*wfmpre["xincr"]+wfmpre["xzero"]
        ypts=(data-wfmpre["yoff"])*wfmpre["ymult"]+wfmpre["yzero"]
        return np.column_stack((xpts,ypts))
    
    @interface.use_parameters(channel="input_channel")
    def _read_sweep_fast(self, channel, wfmpre=None, timeout=None):
        self.write(":DATA:SOURCE {}".format(channel))
        wfmpre=wfmpre or self.get_wfmpre(enable=False)
        self.write(":CURVE?")
        if wfmpre["fmt"].is_ascii():
            data=self.read("raw",timeout=timeout)
        else:
            data=self.read_binary_array_data(timeout=timeout)
        trace=self.parse_array_data(data,wfmpre["fmt"].to_desc())
        if len(trace)!=wfmpre["pts"]:
            raise TektronixError("received data length {0} is not equal to the number of points {1}".format(len(trace),wfmpre["pts"]))
        return self._scale_data(trace,wfmpre)
    def read_multiple_sweeps(self, channels, wfmpres=None, ensure_fmt=False, timeout=None, return_wfmpres=None):
        """
        Read data from a multiple channels channel.

        Args:
            channels: list of channel indices or names
            wfmpres: optional list or dictionary of preambles (obtained using :meth:`get_wfmpre`);
                if it is ``None``, obtain during reading, which slows down the data acquisition a bit
            ensure_fmt: if ``True``, make sure that oscilloscope data format agrees with the one in `wfmpre`
            timeout: read timeout
            return_wfmpres: if ``True``, return tuple ``(sweeps, wfmpres)``, where ``wfmpres`` can be used for further sweep readouts.
        """
        if not channels:
            return []
        channels=[self._normalize_channel(ch) for ch in channels]
        if wfmpres is None:
            wfmpres={}
        elif isinstance(wfmpres,(list,tuple)):
            wfmpres=dict(zip(channels,wfmpres))
        if ensure_fmt:
            pre=wfmpres.get(channels[0],None)
            fmt=pre["fmt"] if pre else self.default_data_fmt
            if self.get_data_format()!=data_format.DataFormat.from_desc(fmt).to_desc():
                self.set_data_format(fmt=fmt)
        for ch in channels:
            if ch not in wfmpres:
                wfmpres[ch]=self.get_wfmpre(ch,enable=False)
        sweeps=[self._read_sweep_fast(ch,wfmpres[ch],timeout=timeout) for ch in channels]
        return (sweeps,wfmpres) if return_wfmpres else sweeps
    def read_sweep(self, channel, wfmpre=None, ensure_fmt=True, timeout=None):
        """
        Read data from a single channel.

        Args:
            channel: channel index or name
            wfmpre: optional preamble dictionary (obtained using :meth:`get_wfmpre`);
                if it is ``None``, obtain during reading, which slows down the data acquisition a bit
            ensure_fmt: if ``True``, make sure that oscilloscope data format agrees with the one in `wfmpre`
            timeout: read timeout
        """
        return self.read_multiple_sweeps([channel],[wfmpre],ensure_fmt=ensure_fmt,timeout=timeout)[0]







class TDS2000(ITektronixScope):
    """
    Tektronix TDS2000 series oscilloscope.

    Args:
        addr: device address; usually a VISA address string such as ``"USB0::0x0699::0x0364::C000000::INSTR"``
        nchannels: can specify number of channels on the oscilloscope; by default, autodetect number of channels (might take several seconds on connection)
    """

class DPO2000(ITektronixScope):
    """
    Tektronix DPO2000 series oscilloscope.

    Args:
        addr: device address; usually a VISA address string such as ``"USB0::0x0699::0x0364::C000000::INSTR"``
        nchannels: can specify number of channels on the oscilloscope; by default, autodetect number of channels (might take several seconds on connection)
    """
    _wfmpre_comm="WFMO"
    _trig_comm="TRIGGER:A"
    _probe_attenuation_comm=("PROBE:GAIN","gain")
    _hor_offset_method="delay"
    _hor_pos_mode="frac"
    def _build_wfmpre(self, data):
        wfmpre={}
        wfmpre["fmt"]=data_format.DataFormat.from_desc("ascii") if data[2].startswith("ASC") else self._build_data_format(data[3],data[0])
        wfmpre["pts"]=int(data[6])
        wfmpre["xzero"]=float(data[10])
        wfmpre["xincr"]=float(data[9])
        wfmpre["ptoff"]=int(data[11])
        wfmpre["ymult"]=float(data[13])
        wfmpre["yzero"]=float(data[15])
        wfmpre["yoff"]=float(data[14])
        return wfmpre
    def _set_data_resolution(self, resolution):
        self.write(":DATA:RESOLUTION",resolution)