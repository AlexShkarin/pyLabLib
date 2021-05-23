from builtins import range
from ...core.utils.py3 import textstring

import numpy as np

from ...core.devio import SCPI, data_format  #@UnresolvedImport
from ...core.utils import funcargparse, general  #@UnresolvedImport

_depends_local=["...core.devio.SCPI"]



class ITektronixScope(SCPI.SCPIDevice):
    """
    Generic Tektronix Oscilloscope.
    """
    def __init__(self, addr):
        SCPI.SCPIDevice.__init__(self,addr)
        self.data_fmt="<i1"
        self._wfmpre="WFMP"
        self._trig="TRIGGER:MAIN"
    
    
    def grab_single(self, wait_type="sync"):
        self.write(":ACQ:STOPAFTER SEQ; :ACQ:STATE ON")
        self.wait(wait_type)
    def grab_continuous(self, enable=True):
        self.write(":ACQ:STOPAFTER RUNSTOP; :ACQ:STATE",enable)
    def is_continuous(self):
        return self.ask(":ACQ:STOPAFTER?").strip().upper().startswith("RUN")
    def is_grabbing(self):
        return self.ask(":ACQ:STATE?","bool")
    
    
    def get_edge_trigger_source(self):
        src=self.ask(self._trig+":EDGE:SOURCE?").upper()
        if src.startswith("CH"):
            return int(src[2:])
        raise RuntimeError("unrecognized trigger source: {}".format(src))
    def get_edge_trigger_coupling(self):
        return self.ask(self._trig+":EDGE:COUPL?").lower()
    def get_edge_trigger_slope(self):
        return self.ask(self._trig+":EDGE:SLOPE?").lower()
    def get_trigger_level(self):
        return self.ask(self._trig+":LEVEL?").lower()
    def set_edge_trigger(self, source, level, coupling="dc", slope="fall"):
        self.write(self._trig+":EDGE:SOURCE","CH{}".format(source))
        self.write(self._trig+":EDGE:COUPL",coupling.upper())
        self.write(self._trig+":EDGE:SLOPE",slope.upper())
        self.write(self._trig+":LEVEL",level)
        self.write(self._trig+":TYPE","EDGE")
        return self.get_edge_trigger_source(), self.get_trigger_level(), self.get_edge_trigger_coupling(), self.get_edge_trigger_slope()
    
    def get_trigger_mode(self):
        return self.ask(self._trig+":MODE?")[:4].lower()
    def set_trigger_mode(self, mode="auto"):
        self.write(self._trig+":MODE", "AUTO" if mode.lower()=="auto" else "NORM")
        return self.get_trigger_mode()
    
    def get_trigger_state(self):
        return self.ask("TRIGGER:STATE?").lower()
    def force_trigger(self):
        self.write("TRIGGER FORCE")
        
    
    def get_horizontal_span(self):
        return self.ask(":HORIZONTAL:SCALE?","float")*10.
    def set_horizontal_span(self, span):
        self.write(":HORIZONTAL:SCALE",span/10.,"float")
        return self.get_horizontal_span()
    def get_horizontal_offset(self):
        return self.ask(":HORIZONTAL:POS?","float")
    def set_horizontal_offset(self, offset=0.):
        self.write(":HORIZONTAL:POS",offset,"float")
        return self.get_horizontal_offset()
    
    def channel_enabled(self, channel):
        return self.ask(":SELECT:CH{}?".format(channel),"bool")
    def enable_channel(self, channel, enabled=True):
        self.write(":SELECT:CH{}".format(channel),enabled,"bool")
        return self.channel_enabled(channel)
    def get_coupling(self, channel):
        return self.ask(":CH{}:COUPL?".format(channel)).lower()
    def set_coupling(self, channel, coupling="dc"):
        self.write(":CH{}:COUPL".format(channel),coupling.upper())
        return self.get_coupling(channel)
    def get_vertical_span(self, channel):
        return self.ask(":CH{}:SCALE?".format(channel),"float")*10. # scale is per division (10 division per screen)
    def set_vertical_span(self, channel, span):
        self.write(":CH{}:SCALE".format(channel),span/10.,"float") # scale is per division (10 division per screen)
        return self.get_vertical_span(channel)
    def get_vertical_position(self, channel):
        return self.ask(":CH{}:POSITION?".format(channel),"float")*self.get_vertical_span(channel)/10. # offset is in divisions (10 division per screen)
    def set_vertical_position(self, channel, offset):
        offset/=self.get_vertical_span(channel)/10. # offset is in divisions (10 division per screen)
        self.write(":CH{}:POSITION".format(channel),offset,"float")
        return self.get_vertical_position(channel)
    
    
    def get_points_number(self, kind="send"):
        funcargparse.check_parameter_range(kind,"kind",{"acq","trace","send"})
        if kind=="acq":
            return self.ask(":HORIZONTAL:RECORDLENGTH?","int")
        elif kind=="trace":
            return self.ask(":{}:RECORDLENGTH?".format(self._wfmpre),"int")
        else:
            return self.ask(":{}:NR_PT?".format(self._wfmpre),"int")
    def _set_data_resolution(self, resolution):
        pass
    def set_points_number(self, pts_num, reset_limts=True):
        if pts_num<5E4:
            self._set_data_resolution("REDUCED")
        else:
            self._set_data_resolution("FULL")
        self.write(":HORIZONTAL:RECORDLENGTH",pts_num,"int")
        if reset_limts:
            self.set_data_pts_range()
        return self.get_points_number(kind="send")
    def get_data_pts_range(self):
        return self.ask(":DATA:START?","int"),min(self.ask(":DATA:STOP?","int"),self.get_points_number())
    def set_data_pts_range(self, rng=None):
        if rng is None:
            start,stop=1,self.get_points_number(kind="acq")
        else:
            start,stop=min(rng),max(rng)
        self.write(":DATA:START",start,"int")
        self.write(":DATA:STOP",stop,"int")
        return self.get_data_pts_range()
    
    def set_data_format(self, fmt=None):
        fmt=funcargparse.getdefault(fmt,self.data_fmt)
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
            return "ascii"
        if dfmt[0]=="S":
            border=">"
            dfmt=dfmt[1:]
        else:
            border="<"
        kind="i" if dfmt[1]=="I" else "u"
        return data_format.DataFormat(size,kind,border)
    def get_data_format(self):
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
    def get_wfmpre(self):
        data=self.ask(":{}?".format(self._wfmpre)).split(";")
        data=[d.strip().upper() for d in data]
        return self._build_wfmpre(data)
    
    def request_data(self, fmt=None):
        fmt=funcargparse.getdefault(fmt,self.data_fmt)
        self.set_data_format(fmt)
        data=self.ask(":CURVE?","raw")
        return self.parse_trace_data(data,fmt)
    def _scale_data(self, data, wfmpre=None):
        wfmpre=wfmpre or self.get_wfmpre()
        xpts=(np.arange(len(data))-wfmpre["ptoff"])*wfmpre["xincr"]+wfmpre["xzero"]
        ypts=(data-wfmpre["yoff"])*wfmpre["ymult"]+wfmpre["yzero"]
        return np.column_stack((xpts,ypts))
    
    def selected_channel(self):
        source=self.ask(":DATA:SOURCE?").strip().upper()
        if not source.startswith("CH") or len(source)!=3:
            raise RuntimeError("source {} is not a channel".format(source))
        return int(source[-1])
    def select_channel(self, channel):
        self.write(":DATA:SOURCE CH{}".format(channel))
        return self.selected_channel()
    
    def _read_sweep_fast(self, channel, wfmpre=None):
        self.write(":DATA:SOURCE CH{}".format(channel))
        wfmpre=wfmpre or self.get_wfmpre()
        data=self.ask(":CURVE?","raw")
        trace=self.parse_trace_data(data,wfmpre["fmt"].to_desc())
        if len(trace)!=wfmpre["pts"]:
            raise RuntimeError("received data length {0} is not equal to the number of points {1}".format(len(trace),wfmpre["pts"]))
        return self._scale_data(trace,wfmpre)
    def read_multiple_sweeps(self, channels, wfmpres=None, ensure_fmt=True):
        wfmpres=wfmpres or [None]*len(channels)
        if ensure_fmt:
            fmt=wfmpres[0]["fmt"] if wfmpres[0] else None
            self.set_data_format(fmt=fmt)
        return [self._read_sweep_fast(ch,wfmpre) for (ch,wfmpre) in zip(channels,wfmpres)]
    def read_sweep(self, channel, wfmpre=None, ensure_fmt=True):
        return self.read_multiple_sweeps([channel],[wfmpre],ensure_fmt=ensure_fmt)[0]
    
    
    
    
class DPO2014(ITektronixScope):
    """
    Tektronix DPO2014 Oscilloscope.
    """
    def __init__(self, addr):
        ITektronixScope.__init__(self,addr)
        self._wfmpre="WFMO"
        self._trig="TRIGGER:A"
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
        
#     def get_vertical_offset(self, channel):
#         return self.ask(":CH{}:OFFSET?".format(channel),"float")
#     def set_vertical_offset(self, channel, offset):
#         self.write(":CH{}:OFFSET".format(channel),offset,"float")
#         return self.get_vertical_offset(channel)
        
    def get_horizontal_offset(self):
        return self.ask(":HORIZONTAL:DELAY:TIME?","float") if self.ask(":HORIZONTAL:DELAY:MODE?","bool") else 0
    def set_horizontal_offset(self, offset=0.):
        if offset:
            self.write(":HORIZONTAL:DELAY:TIME",offset,"float")
        else:
            self.write(":HORIZONTAL:DELAY:MODE",False,"bool")
        return self.get_horizontal_offset()
        
class TDS2000(ITektronixScope):
    """
    Tektronix TDS2000 Oscilloscope.
    """
    def __init__(self, addr):
        ITektronixScope.__init__(self,addr)






class MDO3000(SCPI.SCPIDevice):
    """
    Tektronix MDO3000 Oscilloscope with the Spectrum Analyzer add-on.
    """
    _default_operation_cooldown=0.02
    def __init__(self, addr):
        SCPI.SCPIDevice.__init__(self,addr)
        self.data_fmt_scope="<i1"
        self.data_fmt_spec="<f4"
        self._wfmpre="WFMO"
        self._rel_sweep_step=5.
        self._add_settings_node("avg",self.get_avg,self.set_avg)
        self._add_settings_node("frequency_range",self.get_frequency_range,self.set_frequency_range)
        self._add_settings_node("bandwidth",self.get_bandwidth,self.set_bandwidth)
        self._add_settings_node("rel_sweep_step",self.get_rel_sweep_step,self.set_rel_sweep_step)
        self._add_settings_node("ref_level",self.get_ref_level,self.set_ref_level)
        self._add_settings_node("rf_avg",self.get_rf_avg,self.set_rf_avg)
        self._add_settings_node("rf_mode",self.get_rf_mode,self.set_rf_mode)
        self._add_settings_node("channel",self.get_selected_channel,self.select_channel)
    
    
    ### TRIGGER ###
    
    def get_avg(self):
        mode=self.ask(":ACQ:MODE?").upper()
        if mode=="AVERAGE":
            return self.ask(":ACQ:NUMAVG?","int")
        else:
            return 1
    def set_avg(self, avg):
        if avg is True or avg>1:
            self.write(":ACQ:MODE AVERAGE")
            if avg is not True:
                self.write(":ACQ:NUMAVG",avg)
                self.set_rf_avg(avg)
        else:
            self.write(":ACQ:MODE SAMPLE")
        return self.get_avg()
    
    def grab_single(self, avg=None, wait_type="sync"):
        if avg is not None:
            self.set_avg(avg)
        self.write(":ACQ:STOPAFTER SEQ")
        self.write(":ACQ:STATE ON")
        self.wait(wait_type)
    def grab_continuous(self, enable=True):
        self.write(":ACQ:STOPAFTER RUNSTOP")
        self.write(":ACQ:STATE",enable)
    def is_continuous(self):
        return self.ask(":ACQ:STOPAFTER?").strip().upper().startswith("RUN")
    def is_grabbing(self):
        return self.ask(":ACQ:STATE?")
    
    
    ### SCOPE ###
    
    def get_horizontal_span(self):
        return self.ask(":HORIZONTAL:SCALE?","float")*10.
    def set_horizontal_span(self, span):
        self.write(":HORIZONTAL:SCALE",span/10.,"float")
        return self.get_horizontal_span()
    
    def channel_enabled(self, channel):
        return self.ask(":SELECT:CH{}?".format(channel),"bool")
    def enable_channel(self, channel, enabled=True):
        self.write(":SELECT:CH{}".format(channel),enabled,"bool")
        return self.channel_enabled(channel)
    def get_vertical_span(self, channel):
        return self.ask(":CH{}:SCALE?".format(channel),"float")*10.
    def set_vertical_span(self, channel, span):
        self.write(":CH{}:SCALE".format(channel),span/10.,"float")
        return self.get_vertical_span(channel)
    
    
    ### SPECTRUM ANALYZER ##
    
    def get_frequency_range(self):
        center=self.ask(":RF:FREQ?","float")
        span=self.ask(":RF:SPAN?","float")
        return center-span/2., center+span/2.
    def set_frequency_range(self, frequency):
        try:
            start,stop=min(frequency),max(frequency)
        except TypeError:
            start,stop=frequency,frequency
        self.write(":RF:FREQ",(start+stop)/2.)
        self.write(":RF:SPAN",stop-start)
        return self.get_frequency_range()
    
    def get_bandwidth(self):
        return self.ask(":RF:RBW?","float")
    def set_bandwidth(self, bwidth):
        self.write(":RF:RBW:MODE MANUAL")
        self.write(":RF:RBW",bwidth)
        return self.get_bandwidth()
        
    def get_rel_sweep_step(self):
        return self._rel_sweep_step
    def set_rel_sweep_step(self, step):
        if step>0:
            self._rel_sweep_step=step
        return self._rel_sweep_step
        
    def get_rf_avg(self):
        return self.ask(":RF:RF_AVERAGE:NUMAVG?","int")
    def set_rf_avg(self, avg):
        self.write(":RF:RF_AVERAGE:NUMAVG", avg)
        return self.get_rf_avg()
    
    def get_ref_level(self):
        return self.ask(":RF:REFLEVEL?","float")
    def set_ref_level(self, level):
        self.write(":RF:REFLEVEL",level)
        return self.get_ref_level()
        
    _rf_trace_kind={"normal":"RF_NORMAL","avg":"RF_AVERAGE","max":"RF_MAXHOLD","min":"RF_MINHOLD"}
    _inv_rf_trace_kind=general.invert_dict(_rf_trace_kind)
    def _get_rf_trace_kind(self, kind):
        try:
            return self._rf_trace_kind[kind]
        except KeyError:
            funcargparse.check_parameter_range(kind,"kind",self._rf_trace_kind)
    def enable_rf_channel(self, kind="normal", enable=True):
        self.write(":SELECT:{} {}".format(self._get_rf_trace_kind(kind),1 if enable else 0))
    
    _rf_modes={"min":"MINUSPEAK","max":"PLUSPEAK","sample":"SAMPLE","avg":"AVERAGE"}
    _inv_rf_modes=general.invert_dict(_rf_modes)
    def get_rf_mode(self, kind="normal"):
        mode=self.ask(":RF:DETECT:{}?".format(self._get_rf_trace_kind(kind))).strip().upper()
        return self._inv_rf_modes[mode]
    def set_rf_mode(self, mode="max", kind="norm"):
        try:
            mode=self._rf_modes[mode]
        except KeyError:
            funcargparse.check_parameter_range(mode,"mode",self._rf_modes)
        self.write(":RF:DETECT:MODE MANUAL")
        self.write(":RF:DETECT:{} {}".format(self._get_rf_trace_kind(kind),mode))
        return self.get_rf_mode(kind)
            
    
    ### DATA TRANSFER ###
    
    def get_points_number(self, kind="send"):
        funcargparse.check_parameter_range(kind,"kind",{"acq","trace","send"})
        if kind=="acq":
            return self.ask(":HORIZONTAL:RECORDLENGTH?","int")
        elif kind=="trace":
            return self.ask(":{}:RECORDLENGTH?".format(self._wfmpre),"int")
        else:
            return self.ask(":{}:NR_PT?".format(self._wfmpre),"int")
    def _set_data_resolution(self, resolution):
        pass
    def set_points_number(self, pts_num, reset_limts=True):
        if pts_num<5E4:
            self._set_data_resolution("REDUCED")
        else:
            self._set_data_resolution("FULL")
        self.write(":HORIZONTAL:RECORDLENGTH",pts_num,"int")
        if reset_limts:
            self.set_data_pts_range()
        return self.get_points_number(kind="send")
    def get_data_pts_range(self):
        return self.ask(":DATA:START?","int"),min(self.ask(":DATA:STOP?","int"),self.get_points_number())
    def set_data_pts_range(self, rng=None):
        if rng is None:
            start,stop=1,self.get_points_number(kind="acq")
        else:
            start,stop=min(rng),max(rng)
        self.write(":DATA:START",start,"int")
        self.write(":DATA:STOP",stop,"int")
        return self.get_data_pts_range()
    
    def _get_default_data_format(self, fmt):
        if fmt is not None:
            return fmt
        src=self.ask(":DATA:SOURCE?").strip().upper()
        return self.data_fmt_scope if src.startswith("CH") else self.data_fmt_spec
        
    def set_data_format(self, fmt=None):
        fmt=self._get_default_data_format(fmt)
        fmt=data_format.DataFormat.from_desc(fmt)
        if fmt.is_ascii():
            self.write(":DATA:ENCDG ASCII")
        else:
            if fmt.kind=="i":
                dfmt="RIBINARY"
            elif fmt.kind=="u":
                dfmt="RPBINARY"
            else:
                dfmt="FPBINARY"
            if fmt.byteorder=="<":
                dfmt="S"+dfmt
            self.write(":DATA:ENCDG",dfmt)
            self.write(":DATA:WIDTH",fmt.size)
        return self.get_data_format()
    def get_data_format(self):
        dfmt=self.ask(":DATA:ENCDG?").upper()
        size=self.ask(":DATA:WIDTH?","int")
        if dfmt.startswith("ASC"):
            return "ascii"
        if dfmt[0]=="S":
            border="<"
            dfmt=dfmt[1:]
        else:
            border=">"
        if dfmt[:2]=="RP":
            kind="u"
        elif dfmt[:2]=="RI":
            kind="i"
        else:
            kind="f"
        fmt=data_format.DataFormat(size,kind,border)
        return fmt.to_desc()
    
    def request_data(self, fmt=None, set_fmt=True):
        fmt=self._get_default_data_format(fmt)
        if set_fmt:
            self.set_data_format(fmt)
        data=self.ask(":CURVE?","raw")
        return self.parse_trace_data(data,fmt)
    
    def _scale_time_data(self, data):
        xzero=self.ask(":{}:XZERO?".format(self._wfmpre),"float")
        xincr=self.ask(":{}:XINCR?".format(self._wfmpre),"float")
        xpts=np.arange(len(data))*xincr+xzero
        ymult=self.ask(":{}:YMULT?".format(self._wfmpre),"float")
        yzero=self.ask(":{}:YZERO?".format(self._wfmpre),"float")
        yoff=self.ask(":{}:YOFF?".format(self._wfmpre),"float")
        ypts=(data-yoff)*ymult+yzero
        return np.column_stack((xpts,ypts))
    def read_trace(self, channel):
        self.select_channel(channel)
        pts=self.get_points_number(kind="send")
        trace=self.request_data()
        if len(trace)!=pts:
            raise RuntimeError("received data length {0} is not equal to the number of points {1}".format(len(trace),pts))
        return self._scale_time_data(trace)
    
    def _scale_rf_data(self, data):
        center=self.ask(":RF:FREQ?","float")
        span=self.ask(":RF:SPAN?","float")
        xpts=np.linspace(center-span/2.,center+span/2.,len(data))
        return np.column_stack((xpts,data))
    def read_sweep(self, kind="normal"):
        self.select_channel(self._get_rf_trace_kind(kind))
        pts=self.get_points_number(kind="send")
        trace=self.request_data()
        if len(trace)!=pts:
            raise RuntimeError("received data length {0} is not equal to the number of points {1}".format(len(trace),pts))
        return self._scale_rf_data(trace)
    def _read_sweep_fast(self, pts, fmt):
        trace=self.request_data(fmt, set_fmt=False)
        if len(trace)!=pts:
            raise RuntimeError("received data length {0} is not equal to the number of points {1}".format(len(trace),pts))
        return self._scale_rf_data(trace)
        
    def grab_rf_sweep(self, kind="avg", avg=None, freq_step=None):
        if freq_step is None:
            self.grab_single(avg=avg)
            return self.read_sweep(kind)
        if freq_step=="auto":
            freq_step=self._rel_sweep_step*self.get_bandwidth()
        freq_range=self.get_frequency_range()
        center,span=(freq_range[0]+freq_range[1])/2.,freq_range[1]-freq_range[0]
        tr_pts=self.get_points_number()
        if tr_pts!=751:
            raise RuntimeError("expected {} points per trace; got {}".format(751,tr_pts))
        tr_span=(tr_pts-1)*freq_step
        pts=int(span/(freq_step*2.))*2+1
        if pts<=tr_pts:
            self.set_frequency_range((center-tr_span/2.,center+tr_span/2.))
            sweep=self.grab_rf_sweep(kind,avg,freq_step=None)
            self.set_frequency_range(freq_range)
            dpts=(tr_pts-pts)//2
            return sweep[dpts:tr_pts-dpts]
        core_pts=501
        step_span=(core_pts-1)*freq_step
        chunks_n=(pts-2)//(core_pts-1)+1
        chunks=[]
        for ch in range(chunks_n):
            tr_center=freq_range[0]+step_span*(ch+0.5)
            self.set_frequency_range((tr_center-tr_span/2.,tr_center+tr_span/2.))
            self.grab_single(avg=avg)
            chunks.append(self.read_sweep(kind))
        for c in range(len(chunks)-1):
            chunks[c]=chunks[c][(tr_pts-core_pts)//2:-(tr_pts-core_pts)//2-1]
        last_pts=(pts-2)%(core_pts-1)+1
        chunks[-1]=chunks[-1][(tr_pts-core_pts)//2:(tr_pts-core_pts)//2+last_pts+1]
        self.set_frequency_range(freq_range)
        return np.concatenate(chunks)
        
    
    def get_selected_channel(self):
        source=self.ask(":DATA:SOURCE?").strip().upper()
        if source.startswith("CH") and len(source)==3:
            return int(source[-1])
        if source.startswith("RF"):
            return self._inv_rf_trace_kind[source]
        raise RuntimeError("source {} is not a channel".format(source))
    def select_channel(self, channel):
        if not isinstance(channel,textstring):
            channel="CH{}".format(channel)
        elif channel in self._rf_trace_kind:
            channel=self._get_rf_trace_kind(channel)
        self.write(":DATA:SOURCE {}".format(channel))
        return self.get_selected_channel()