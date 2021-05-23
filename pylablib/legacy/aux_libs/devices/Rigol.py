from builtins import range

import numpy as np

from ...core.devio import SCPI, data_format  #@UnresolvedImport
from ...core.utils import funcargparse  #@UnresolvedImport
from ...core.utils import general as general_utils  #@UnresolvedImport

_depends_local=["...core.devio.SCPI"]


class DSA1030A(SCPI.SCPIDevice):
    """
    Rigol DSA1030A Spectrum Analyzer.
    """
    def __init__(self, addr):
        SCPI.SCPIDevice.__init__(self,addr,term_write="\n")
        self.data_fmt="<f4"
        self.channel=1
        self._add_settings_node("power_on",self.get_output,None)
        self._add_settings_node("power",self.get_output_level,self.set_output_level)
        self._add_settings_node("frequency_range",self.get_frequency_range,self.set_frequency_range)
        self._add_settings_node("bandwidth",self.get_bandwidth,self.set_bandwidth)
        self._add_settings_node("bandwidth/video",
                lambda: self.get_bandwidth("video"),lambda bw: self.set_bandwidth(bw,"video"))
        self._add_settings_node("bandwidth/resolution",
                lambda: self.get_bandwidth("resolution"),lambda bw: self.set_bandwidth(bw,"resolution"))
        self._add_settings_node("attenuation",self.get_attenuation,self.set_attenuation)
        self._add_settings_node("sweep_points",self.get_sweep_points,self.set_sweep_points)
        
    def select_channel(self, channel):
        self.channel=channel
    def current_channel(self):
        return self.channel
        
    def sweep_single(self, wait_type="sync"):
        self.write(":ABORT;:INIT:CONT OFF;:INIT")
        self.wait(wait_type)
    def sweep_reset(self, wait_type="sync"):
        self.write(":ABORT;:INIT")
        self.wait(wait_type)
    def sweep_continuous(self, enable=True):
        self.write(":INIT:CONT",enable)
        if not enable:
            self.write(":ABORT")
    def is_continuous(self):
        return self.ask(":INIT:CONT?","bool")
    
    def get_output(self):
        return self.ask(":OUTPUT:STATE?","bool")
    def set_output(self, enabled=True):
        self.write(":OUTPUT:STATE",enabled)
    def get_output_level(self):
        return self.ask(":SOURCE:POWER:LEVEL:IMMEDIATE:AMPLITUDE?","float")
    def set_output_level(self, level):
        if level is None:
            self.set_output(False)
            return None
        else:
            self.write(":SOURCE:POWER:LEVEL:IMMEDIATE:AMPLITUDE {:.2E}".format(level))
            return self.get_output_level()
    
    def get_frequency_range(self):
        start=self.ask(":SENSE:FREQUENCY:START?","float")
        stop=self.ask(":SENSE:FREQUENCY:STOP?","float")
        return start,stop
    def set_frequency_range(self, frequency):
        try:
            start,stop=min(frequency),max(frequency)
        except TypeError:
            start,stop=frequency,frequency
        if start-stop>=100.:            
            self.write(":SENSE:FREQUENCY:START {:.10E}".format(start))
            self.write(":SENSE:FREQUENCY:STOP {:.10E}".format(stop))
        else: # go to zero span mode
            self.write(":SENSE:FREQUENCY:SPAN {:.10E}".format(stop-start))
            self.write(":SENSE:FREQUENCY:CENTER {:.10E}".format((start+stop)/2.))
        return self.get_frequency_range()
        
    def get_sweep_points(self):
        return self.ask(":SENSE:SWEEP:POINTS?","int")
    def set_sweep_points(self, pts):
        self.write(":SENSE:SWEEP:POINTS",int(pts))
        return self.get_sweep_points()
    
    def get_bandwidth(self, bw_type="video"):
        if not bw_type in ["video","resolution"]:
            raise ValueError("unrecognized bandwidth type: {0}".format(bw_type))
        return self.ask(":SENSE:BANDWIDTH:{0}?".format(bw_type),"float")
    def set_bandwidth(self, bwidth, bw_type="both"):
        if not bw_type in ["video","resolution","both"]:
            raise ValueError("unrecognized bandwidth type: {0}".format(bw_type))
        if bw_type=="both":
            self.set_bandwidth(bwidth,"video")
            return self.set_bandwidth(bwidth,"resolution")
        else:
            if bwidth is None:
                self.write(":SENSE:BANDWIDTH:{0}:AUTO".format(bw_type),True)
            else:
                self.write(":SENSE:BANDWIDTH:{0}:AUTO".format(bw_type),False)
                self.write(":SENSE:BANDWIDTH:{0}".format(bw_type),bwidth)
            return self.get_bandwidth(bw_type)
            
    def get_attenuation(self):
        return self.ask(":SENSE:POWER:RF:ATTENUATION?","float")
    def set_attenuation(self, att):
        if att is None:
            self.write(":SENSE:POWER:RF:ATTENUATION:AUTO 1")
        else:
            self.write(":SENSE:POWER:RF:ATTENUATION",att)
        return self.get_attenuation()
    
    def autoscale_power(self):
        self.write(":SENSE:POWER:ASCALE")
        
        
    def set_data_format(self, fmt=None):
        fmt=funcargparse.getdefault(fmt,self.data_fmt)
        fmt=data_format.DataFormat.from_desc(fmt)
        fmt.flip_byteorder() # different convention about normal and swapped
        if not (fmt.is_ascii() or fmt.to_desc()[1:] in ["f4"]):
            raise ValueError("Format {0} isn't supported".format(fmt))
        self.write(":FORMAT:TRACE:DATA {0};:FORMAT:BORDER {1}".format(*fmt.to_desc("SCPI")))
    def get_data_format(self):
        enc=self.ask(":FORMAT:TRACE:DATA?")
        border=self.ask(":FORMAT:BORDER?")
        fmt=data_format.DataFormat.from_desc_SCPI(enc,border)
        fmt.flip_byteorder() # different convention about normal and swapped
        return fmt.to_desc()
    def request_data(self, fmt=None):
        fmt=funcargparse.getdefault(fmt,self.data_fmt)
        self.set_data_format(fmt)
        data=self.ask(":TRACE:DATA? TRACE{0}".format(self.channel),"raw")
        return self.parse_trace_data(data,fmt)
            
    def read_sweep(self):
        pts=self.get_sweep_points()
        trace=self.request_data()
        if len(trace)!=pts:
            raise RuntimeError("received data length {0} is not equal to the number of points {1}".format(len(trace),pts))
        freq_range=self.get_frequency_range()
        freqs=np.linspace(freq_range[0],freq_range[1],pts)
        return np.column_stack(( freqs,trace ))
        
    _chunks_ovlap_pts=300
    def grab_single_sweep(self, chunks=1, autoscale=True, auto_step_fraction=0.1, chunks_ovlap_pts="auto", error_retries=3):
        for t in general_utils.RetryOnException(error_retries):
            with t:
                self.wait()
                freq_range=self.get_frequency_range()
                cont=self.is_continuous()
                if autoscale:
                    rbw=self.get_bandwidth("resolution")
                    vbw=self.get_bandwidth("video")
                    pts=self.get_sweep_points()
                    att=self.get_attenuation()
                    self.set_bandwidth(min((freq_range[1]-freq_range[0])/10.,3E6))
                    self.set_sweep_points(1201)
                    self.sweep_single()
                    self.autoscale_power()
                    self.set_bandwidth(rbw,"resolution")
                    self.set_bandwidth(vbw,"video")
                    self.set_attenuation(att)
                opt_step=self.get_bandwidth("resolution")*auto_step_fraction
                if chunks=="auto":
                    opt_pts=(freq_range[1]-freq_range[0])/opt_step
                    if opt_pts<pts:
                        chunks=1
                    elif opt_pts<3001:
                        pts=opt_pts
                        chunks=1
                    else:
                        pts=3001
                        chunks=int(opt_pts//pts+1)
                    if chunks_ovlap_pts=="auto":
                        chunks_ovlap_pts=150
                else:
                    if chunks_ovlap_pts=="auto":
                        chunks_ovlap_pts=0
                self.set_sweep_points(pts)
                if chunks==1:
                    self.sweep_single()
                    data=self.read_sweep()
                else:
                    rel_ovlap=chunks_ovlap_pts/(pts-1.)
                    df=float(freq_range[1]-freq_range[0])/chunks
                    spf=df/(1.-rel_ovlap*2)
                    f0=freq_range[0]-spf*rel_ovlap
                    sweeps=[]
                    for i in range(chunks):
                        self.set_frequency_range((f0+df*i,f0+df*i+spf))
                        self.wait()
                        self.sweep_single()
                        single_sweep=self.read_sweep()[chunks_ovlap_pts:pts-chunks_ovlap_pts]
                        if i!=0:
                            single_sweep=single_sweep[1:,:]
                        sweeps.append(single_sweep)
                    self.set_frequency_range(freq_range)
                    data=np.concatenate(sweeps,axis=0)
                    adj_freq=np.linspace(freq_range[0],freq_range[1],len(data))
                    fstep=(freq_range[1]-freq_range[0])/(len(data)-1.)
                    if abs(data[:,0]-adj_freq).max()>fstep*.1:
                        raise RuntimeError("frequency adjustment error")
                    data[:,0]=adj_freq
                self.sweep_continuous(cont)
                return data
        
        
        
    def apply_settings(self, settings):
        if "power_on" in settings and not settings["power_on"]:
            self.set_output(False)
        SCPI.SCPIDevice.apply_settings(self,settings)
        if "power_on" in settings and settings["power_on"]:
            self.set_output(True)
        self.wait()
        return self.get_settings()