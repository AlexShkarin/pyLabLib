import numpy as np

from ...core.devio import SCPI, data_format, interface, DeviceError, DeviceBackendError
from ...core.utils import funcargparse

import collections


class TektronixError(DeviceError):
    """Generic Tektronix devices error"""
class TektronixBackendError(TektronixError,DeviceBackendError):
    """Generic Tektronix backend communication error"""

TTriggerParameters=collections.namedtuple("TTriggerParameters",["source","level","coupling","slope"])
class ITektronixScope(SCPI.SCPIDevice):
    """
    Generic Tektronix Oscilloscope.
    """
    _wfmpre_comm="WFMP"  # command used to obtain waveform preamble
    _trig_comm="TRIGGER:MAIN"  # command used to set up trigger
    _software_trigger_delay=0.3 # delay between issuing a single acquisition and sending the software trigger; if the trigger is sent sooner, it is ignored
    _probe_attenuation_comm=("PROBE","att")
    # _default_operation_cooldown={"write":2E-3}
    _main_channels_idx=[1,2,3,4]  # ids of main channels (integers)
    _aux_channels=[]  # names of aux channels (strings)
    # horizontal offset method; either ``"delay"`` (use ``"HORizontal:DELay:TIMe"``), ``"pos"`` (use ``"HORizontal:POSition"``, and set ``"HORizontal:DELay:MODe"`` accordingly),
    # or ``"pos_only"`` (use ``"HORizontal:POSition"``, don't set ``"HORizontal:DELay:MODe"`` in case it's not available)
    _hor_offset_method="pos_only"
    Error=TektronixError
    BackendError=TektronixBackendError
    def __init__(self, addr):
        SCPI.SCPIDevice.__init__(self,addr)
        _main_channels=[(i,"ch{}".format(i)) for i in self._main_channels_idx]
        self._add_parameter_class(interface.EnumParameterClass("input_channel",_main_channels,value_case="upper"))
        self._add_parameter_class(interface.EnumParameterClass("channel",_main_channels+self._aux_channels,value_case="upper"))
        self.data_fmt="<i1"
        self._add_info_variable("addr",lambda: self.conn)
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
    _p_slope=interface.EnumParameterClass("slope",["rise",("rise","ris"),"fall"],value_case="upper")
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
    def setup_edge_trigger(self, source, level, coupling="dc", slope="fall"):
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
    _p_trigger_mode=interface.EnumParameterClass("trigger_mode",["auto","norm"],value_case="upper")
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
    
    _p_trigger_state=interface.EnumParameterClass("trigger_state",[("armed","arm"),"ready",("trigger","trig"),"auto",("save","sav"),"scan"],value_case="upper")
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
    def get_horizontal_offset(self):
        """Get horizontal offset (position of the center of the sweep; in seconds)"""
        if self._hor_offset_method=="delay":
            self.write(":HORIZONTAL:DELAY:MODE 1")
            return self.ask(":HORIZONTAL:DELAY:TIME?","float")
        else:
            if self._hor_offset_method=="pos":
                self.write(":HORIZONTAL:DELAY:MODE 0")
            span=self.get_horizontal_span()
            return (self.ask(":HORIZONTAL:POS?","float")/100.-.5)*span
    def set_horizontal_offset(self, offset=0.):
        """Set horizontal offset (position of the center of the sweep; in seconds)"""
        if self._hor_offset_method=="delay":
            self.write(":HORIZONTAL:DELAY:MODE 1")
            self.write(":HORIZONTAL:DELAY:TIME",offset,"float")
        else:
            if self._hor_offset_method=="pos":
                self.write(":HORIZONTAL:DELAY:MODE 0")
            span=self.get_horizontal_span()
            rel_offset=(offset/span*100)+50
            rel_offset=min(max(rel_offset,0),100)
            self.write(":HORIZONTAL:POS",offset,"float")
        return self.get_horizontal_offset()
    @interface.use_parameters(channel="input_channel")
    def get_vertical_span(self, channel):
        """Get channel vertical span (in V)"""
        return self.ask(":{}:SCALE?".format(channel),"float")*10. # scale is per division (10 division per screen)
    @interface.use_parameters(channel="input_channel")
    def set_vertical_span(self, channel, span):
        """Set channel vertical span (in V)"""
        self.write(":{}:SCALE".format(channel),span/10.,"float") # scale is per division (10 division per screen)
        return self.get_vertical_span(channel)
    @interface.use_parameters(channel="input_channel")
    def get_vertical_position(self, channel):
        """Get channel vertical position (offset of the zero volt line; in V)"""
        return self.ask(":{}:POSITION?".format(channel),"float")*self.get_vertical_span(channel)/10. # offset is in divisions (10 division per screen)
    @interface.use_parameters(channel="input_channel")
    def set_vertical_position(self, channel, offset):
        """Set channel vertical position (offset of the zero volt line; in V)"""
        offset/=self.get_vertical_span(channel)/10. # offset is in divisions (10 division per screen)
        self.write(":{}:POSITION".format(channel),offset,"float")
        return self.get_vertical_position(channel)
    

    @interface.use_parameters(channel="input_channel")
    def is_channel_enabled(self, channel):
        """Check if channel is enabled"""
        return self.ask(":SELECT:{}?".format(channel),"bool")
    @interface.use_parameters(channel="input_channel")
    def enable_channel(self, channel, enabled=True):
        """Enable or disable given channel"""
        self.write(":SELECT:{}".format(channel),enabled,"bool")
        return self.is_channel_enabled(channel)
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
    def _change_channel(self, channel=None):
        """Select a new channel is specified"""
        if channel is not None:
            self.select_channel(channel)
    @interface.use_parameters(channel="input_channel",_returns="coupling")
    def get_coupling(self, channel):
        """
        Get channel coupling.

        Can be ``"ac"``, ``"dc"``, or ``"gnd"``.
        """
        return self.ask(":{}:COUPL?".format(channel))
    @interface.use_parameters(channel="input_channel")
    def set_coupling(self, channel, coupling="dc"):
        """
        Set channel coupling.

        Can be ``"ac"``, ``"dc"``, or ``"gnd"``.
        """
        self.write(":{}:COUPL".format(channel),coupling)
        return self.get_coupling(channel)
    @interface.use_parameters(channel="input_channel")
    def get_probe_attenuation(self, channel):
        """Get channel probe attenuation"""
        if not self._probe_attenuation_comm:
            return 1
        comm,kind=self._probe_attenuation_comm
        value=self.ask(":{}:{}?".format(channel,comm),"float")
        return value if kind=="att" else 1./value
    @interface.use_parameters(channel="input_channel")
    def set_probe_attenuation(self, channel, attenuation):
        """Set channel probe attenuation"""
        if self._probe_attenuation_comm:
            comm,kind=self._probe_attenuation_comm
            self.write(":{}:{}".format(channel,comm),attenuation if kind=="att" else 1./attenuation)
        return self.get_probe_attenuation(channel)

    
    def get_points_number(self, kind="send"):
        """
        Get number of datapoints in various context.

        ``kind`` defines the context.
        It can be ``"acq"`` (number of points acquired),
        ``"trace"`` (number of points in the source of the read-out trace; can be lower than ``"acq"`` if the data resultion is reduced, or if the source is not a channel data),
        or ``"send"`` (number of points in the sent waveform; can be lower than ``"trace"`` if :meth:`get_data_pts_range` is used to specify and incomplete range).
        Not all kinds are defined for all scope model (e.g., ``"trace"`` is not defined for TDS20XX oscilloscopes).
        
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
            fmt=self.data_fmt
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
    def get_wfmpre(self, channel=None):
        """
        Get preamble dictionary describing all scaling and format data for the given channel or a list of channels.

        Can be acquired once and used in subsequent multiple reads to save time on re-requesting.
        If `channel` is ``None``, use the currently selected channel.
        """
        if isinstance(channel,list):
            return [self.get_wfmpre(ch) for ch in channel]
        self._change_channel(channel)
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
        wfmpre=wfmpre or self.get_wfmpre()
        self.write(":CURVE?")
        if wfmpre["fmt"].is_ascii():
            data=self.read("raw",timeout=timeout)
        else:
            data=self.read_binary_array_data(timeout=timeout)
        trace=self.parse_array_data(data,wfmpre["fmt"].to_desc())
        if len(trace)!=wfmpre["pts"]:
            raise RuntimeError("received data length {0} is not equal to the number of points {1}".format(len(trace),wfmpre["pts"]))
        return self._scale_data(trace,wfmpre)
    def read_multiple_sweeps(self, channels, wfmpres=None, ensure_fmt=True, timeout=None):
        """
        Read data from a multiple channels channel.

        Args:
            channels: list of channel indices or names
            wfmpres: optional list of preamble dictionaries (obtained using :meth:`get_wfmpre`);
                if it is ``None``, obtain during reading, which slows down the data acquisition a bit
            ensure_fmt: if ``True``, make sure that oscilloscope data format agrees with the one in `wfmpre`.
            timeout: read timeout
        """
        wfmpres=wfmpres or [None]*len(channels)
        if ensure_fmt:
            fmt=wfmpres[0]["fmt"] if wfmpres[0] else self.data_fmt
            if self.get_data_format()!=data_format.DataFormat.from_desc(fmt).to_desc():
                self.set_data_format(fmt=fmt)
        return [self._read_sweep_fast(ch,wfmpre,timeout=timeout) for (ch,wfmpre) in zip(channels,wfmpres)]
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
    Tektronix TDS2000 Oscilloscope.
    """

class DPO2014(ITektronixScope):
    """
    Tektronix DPO2014 Oscilloscope.
    """
    _wfmpre_comm="WFMO"
    _trig_comm="TRIGGER:A"
    _probe_attenuation_comm=("PROBE:GAIN","gain")
    _hor_offset_method="delay"
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