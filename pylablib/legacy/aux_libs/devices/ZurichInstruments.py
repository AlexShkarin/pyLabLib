from builtins import range
from ...core.utils.py3 import bytestring

from ...core.utils import dictionary, funcargparse  #@UnresolvedImport
from ...core.dataproc import waveforms, fourier  #@UnresolvedImport

try:
    import zhinst.ziPython as zp  #@UnresolvedImport
except ImportError:
    pass
    
import numpy as np
import time




##### Traces sanitizing #####

def get_timestamps_data(trace):
    if trace is None or len(trace)<2:
        return (0.,0.,0.)
    ts=trace[:,0]
    dt=ts[1:]-ts[:-1]
    return dt[0],(dt!=dt[0]).sum()
        
def check_timestamps(trace):
    return get_timestamps_data(trace)[1]==0
def check_all_timestamps(data):
    return all([check_timestamps(s) for s in data])

def get_timestamp_chunks(ts):
    dt=abs(ts[1:]-ts[:-1])
    un,cnts=np.unique(dt,return_counts=True)
    ts0=un[cnts.argmax()]
    jumps=(dt!=ts0).nonzero()[0]
    chunks=[]
    j0=0
    for j in jumps:
        chunks.append((ts[j0],ts[j]))
        j0=j+1
    if j0<len(dt):
        chunks.append((ts[j0],ts[-1]))
    return chunks
def extract_largest_chunk(traces):
    traces=[tr for tr in traces if len(tr)>0]
    if not traces:
        return None
    largest_chunks=[]
    for tr in traces:
        tr_chunks=get_timestamp_chunks(tr[:,0])
        tr_chunks.sort(key=lambda ch: ch[1]-ch[0])
        largest_chunks.append(tr_chunks[-1])
    ovlap=largest_chunks[0]
    for ch in largest_chunks[1:]:
        ovlap=(max(ovlap[0],ch[0]),min(ovlap[1],ch[1]))
    return ovlap
def cut_to_largest_chunk(traces):
    lch=extract_largest_chunk(traces)
    cut_traces=[]
    for tr in traces:
        if len(tr)==0:
            cut_traces.append(tr)
        else:
            ctr=tr[(tr[:,0]>=lch[0])&(tr[:,0]<=lch[1])]
            cut_traces.append(ctr)
    return cut_traces

def align_all_timestamps(data, max_length=None):
    traces=[s for s in data if len(s)>0]
    start_ts=np.max([tr[0,0] for tr in traces])
    start_ts=np.max([waveforms.find_closest_value(tr[:,0],start_ts,approach="top",ordered=True) for tr in traces]) # account for different timestamp steps
    start_pts=[waveforms.find_closest_arg(s[:,0],start_ts,ordered=True) if len(s)>0 else 0 for s in data]
    finish_ts=np.min([tr[-1,0] for tr in traces])
    if max_length:
        if finish_ts<start_ts+max_length:
            return None
        else:
            finish_ts=start_ts+max_length
    finish_ts=np.min([waveforms.find_closest_value(tr[:,0],finish_ts,approach="bottom",ordered=True) for tr in traces])
    finish_pts=[waveforms.find_closest_arg(s[:,0],finish_ts,ordered=True) if len(s)>0 else 0 for s in data]
    data=[s[spt:fpt,:] for s,spt,fpt in zip(data,start_pts,finish_pts)]
    return data


def normalize_time(trace, normalization="full",clockbase=210E6):
    funcargparse.check_parameter_range(normalization,"normalization",{"none","shift","scale","full"})
    if trace.ndim==2:
        trace=trace.copy()
        if normalization in {"shift","full"}:
            trace[:,0]=trace[:,0]-trace[0,0]
        if normalization in {"scale","full"}:
            trace[:,0]=trace[:,0]/clockbase
    else:
        if normalization in {"shift","full"}:
            trace=trace-trace[0]
        if normalization in {"scale","full"}:
            trace=trace/clockbase
    return trace



def filter_transfer_function(f, order, timeconst):
    return 1./(2.j*np.pi*f*timeconst+1)**order
def tc_to_bandwidth(tc, order):
    return (2**(1./order)-1)**.5/(2*np.pi*tc)
def bandwidth_to_tc(bandwidth, order):
    return (2**(1./order)-1)**.5/(2*np.pi*bandwidth)
def filter_amplitude_kernel(t, order, timeconst):
    return np.exp(-t/timeconst)*(np.sign(t)+1)/2.*t**(order-1)
_filter_p_consts=[[1],[1,1],[3,3,1],[15,15,6,1],[105,105,45,10,1],[945,945,420,105,15,1],[10395,10395,4725,1260,210,21,1],[134134,134134,62370,17325,3150,378,28,1]]
def filter_power_kernel(t, order, timeconst):
    cs=_filter_p_consts[order-1]
    tn=abs(t/timeconst)
    s=t*0
    for p,c in enumerate(cs):
        s=s+c*tn**p
    return (np.exp(-tn)*s)/cs[0]
def PSD_filter_compensate(PSD, order, timeconst):
    PSD_filtered=PSD.copy()
    PSD_filtered[:,1]=PSD_filtered[:,1]/abs(filter_transfer_function(PSD[:,0],order,timeconst))**2
    return PSD_filtered
def FT_filter_compensate(ft, order, timeconst):
    ft_filtered=ft.copy()
    ft_filtered[:,1]=ft_filtered[:,1]/filter_transfer_function(ft_filtered[:,0],order,timeconst)
    return ft_filtered
def trace_filter_compensate(trace, order, timeconst, truncate=True):
    ft=fourier.fourier_transform(trace,truncate)
    ft=FT_filter_compensate(ft,order,timeconst)
    return fourier.inverse_fourier_transform(ft,False)



class Demod(object):
    def __init__(self, n, dev):
        object.__init__(self)
        demods_n=len(dev["demods"])
        mod_period=demods_n//2
        self.osc=int(dev["demods",n,"oscselect"])
        self.rel_frequency=dev["oscs",self.osc,"freq"]
        self.frequency=self.rel_frequency
        self.sideband_side=None
        if ("mods",n//mod_period,"enable") in dev:
            mod_ena=int(dev["mods",n//mod_period,"enable"])
        else:
            mod_ena=int(dev["mods",n//mod_period,"mode"])
        if mod_ena:
            if n%mod_period==0:
                self.sideband_side=0
            if n%mod_period==1:
                self.sideband_side=1
            elif n%mod_period==2:
                self.sideband_side=-1
        if self.sideband_side:
            carrier_osc=int(dev["demods",(n//mod_period)*mod_period,"oscselect"])
            carrier_freq=dev["oscs",carrier_osc,"freq"]
            self.frequency=carrier_freq+self.rel_frequency*self.sideband_side
        self.order=int(dev["demods",n,"order"])
        self.timeconst=dev["demods",n,"timeconstant"]
        self.rate=dev["demods",n,"rate"]
        self.phaseshift=dev["demods",n,"phaseshift"]/180.*np.pi
        self.input=int(dev["demods",n,"adcselect"])
        self.input_range=int(dev["sigins",self.input,"range"])
    
    def filter_transfer_function(self, f):
        return filter_transfer_function(f,self.order,self.timeconst)
    def filter_amplitude_kernel(self, t):
        return filter_amplitude_kernel(t,self.order,self.timeconst)
    def filter_power_kernel(self, t):
        return filter_power_kernel(t,self.order,self.timeconst)
    def PSD_filter_compensate(self, PSD, relative_frequency=True):
        """
        If relative_frequency=True, frequencies are given relative to the demod frequency;
            otherwise, they're real frequencies of an input signal 
        """
        if relative_frequency:
            return PSD_filter_compensate(PSD,self.order,self.timeconst)
        else:
            PSD=PSD_filter_compensate(np.column_stack((PSD[:,0]-self.frequency,PSD[:,1])), self.order, self.timeconst)
            return np.column_stack((PSD[:,0]+self.frequency,PSD[:,1]))
    def FT_filter_compensate(self, ft, relative_frequency=True):
        if relative_frequency:
            return FT_filter_compensate(ft,self.order,self.timeconst)
        else:
            FT=FT_filter_compensate(np.column_stack((ft[:,0]-self.frequency,ft[:,1])),self.order,self.timeconst)
            return np.column_stack((FT[:,0]+self.frequency,FT[:,1]))
    def trace_filter_compensate(self, trace, truncate=True):
        return trace_filter_compensate(trace,self.order,self.timeconst,truncate)







class ZIDevice(object):
    """
    Generic Zurich Instruments device.
    """
    def __init__(self, dev_id=None, port=8005, api_level=1):
        object.__init__(self)
        #self.server=ziutils.autoConnect(port,api_level)
        for _ in range(5):
            try:
                self.server=zp.ziDAQServer('localhost',port,api_level)
                if self._get_server_devices():
                    break
            finally:
                time.sleep(5.) 
        if dev_id is None:
            devs=self._get_server_devices()
            if not devs:
                raise RuntimeError("No devices were detected")
            dev_id=devs[0]
        self.dev_id=dev_id
        self.ref_timestamp=0
        
    def _get_server_devices(self):
        nodes=[node.lower() for node in self.server.listNodes('/',0)]
        devs=[node for node in nodes if node.startswith("dev")]
        return devs
        
    def close(self):
        self.server.disconnect()
        self.server=None
        
    def __enter__(self):
        return self
    def __exit__(self, *args, **vargs):
        self.close()
        return False
    
    def _build_path(self, rel_path):
        if isinstance(rel_path,list) or isinstance(rel_path,tuple):
            rel_path="/".join([str(e) for e in rel_path])
        else:
            rel_path=str(rel_path)
        return "/{0}/{1}".format(self.dev_id,rel_path)
    
    def get_parameter(self, path, argtype="float"):
        try:
            path=self._build_path(path)
            if argtype=="int":
                return self.server.getInt(path)
            elif argtype=="float":
                return self.server.getDouble(path)
            elif argtype=="str":
                return self.server.getByte(path)
            elif argtype=="sample":
                return self.server.getSample(path)
            elif argtype=="auxin_sample":
                return self.server.getAuxInSample(path)
        except RuntimeError as e:
            raise RuntimeError(e.message+". The path is {}".format(path))
        raise ValueError("unrecognized argtype: {0}".format(argtype))
    def set_parameter(self, path, value):
        try:
            path=self._build_path(path)
            if isinstance(value,float):
                self.server.setDouble(path,value)
            elif isinstance(value,bytestring):
                self.server.setByte(path,value)
            else:
                self.server.setInt(path,value)
        except RuntimeError as e:
            raise RuntimeError(e.message+". The path is {}".format(path))
    def get_default(self, path, argtype="float", default=None):
        try:
            self.get_parameter(path,argtype)
        except RuntimeError:
            return default
    _timestamp_keys={"VALUE","TIMESTAMP"}
    @classmethod
    def filter_settings_dict(cls, settings):
        def undo_array(x):
            try:
                if len(x)==1:
                    return x[0]
                else:
                    return x
            except Exception:
                return x
        def undo_timestamp(d):
            if len(d)==2 and all([k.upper() in cls._timestamp_keys for k in d]):
                return d["VALUE"]
            else:
                return d
        if not dictionary.is_dictionary(settings):
            return undo_array(settings)
        else:
            settings.map_self(undo_timestamp,to_visit="branches")
            settings.map_self(undo_array,to_visit="leafs")
            return settings
    def get_branch(self, path="", rel_paths=True, raw=False):
        try:
            path=self._build_path(path)
            branch=dictionary.Dictionary(self.server.get(path),case_normalization="upper",case_sensitive=False)
            if rel_paths:
                branch=branch.detach_branch(path)
            else:
                branch=branch.detach_branch(self.dev_id)
            if not raw:
                branch=self.filter_settings_dict(branch)
            return branch
        except RuntimeError as e:
            raise RuntimeError(e.message+". The path is {}".format(path))
    def set_branch(self, branch, path=""):
        try:
            settings=dictionary.Dictionary()
            settings.merge_branch(branch,path)
            for p,v in settings.iternodes(to_visit="leafs",include_path=True):
                self.set_parameter(p,v)
        except RuntimeError as e:
            raise RuntimeError(e.message+". The path is {}".format(path))
    get_settings=get_branch
    apply_settings=set_branch
            
    def __getitem__(self, path):
        try:
            return self.get_parameter(path)
        except RuntimeError:
            return self.get_branch(path)
    def __setitem__(self, path, value):
        if dictionary.is_dictionary(value):
            self.set_branch(value,path)
        else:
            self.set_parameter(path,value)
    def __contains__(self, path):
        try:
            self.get_parameter(path)
            return True
        except RuntimeError:
            return False
            
    ### CONTROL ###
    
    def sync(self):
        self.server.sync()
    def flush(self):
        self.server.sync() # flush has been deprecated in the API
            
            
    ### PROPERTIES ###
                
    def get_devtype(self):
        return self.get_parameter("features/devtype","str")
    def get_options(self):
        options=self.get_parameter("features/options","str")
        options=[o.strip() for o in options.split("\n") if not (o.isspace() or o=="")]
        return options
    def get_clockbase(self):
        return self["clockbase"]
    def normalize_time(self, trace, normalization="full"):
        return normalize_time(trace,normalization=normalization,clockbase=self.get_clockbase())

    def get_timestamp(self, subtract_ref_timestamp=True):
        timestamp=self.server.getAuxInSample(self._build_path("auxins/0/sample"))["timestamp"][0]
        if subtract_ref_timestamp:
            return timestamp-self.ref_timestamp
        else:
            return timestamp
    def update_ref_timestamp(self):
        self.ref_timestamp=self.get_timestamp(subtract_ref_timestamp=False)
        
    ### DEMODS ###
    
    def get_demod_sample(self, demod, fmt="complex"):
        funcargparse.check_parameter_range(fmt,"fmt",{"dict","complex"})
        res=self.get_parameter(("demods",demod,"sample"),"sample")
        if fmt=="dict":
            return res
        else:
            return res["x"][0]+1j*res["y"][0]
    
    def get_demods_rates(self):
        raise NotImplementedError("ZIDevice.get_demods_rates")
    def get_demods_num(self):
        return len(self.get_demods_rates())
    def set_demod_rate(self, demod, rate):
        raise NotImplementedError("ZIDevice.set_demod_rate")
    def stop_demod(self, demod):
        self.set_demod_rate(demod,0)
    def get_demod_frequency(self, demod):
        osc=int(self["demods",demod,"oscselect"])
        return self["oscs",osc,"freq"]
    def set_demod_frequency(self, demod, freq):
        osc=int(self["demods",demod,"oscselect"])
        self["oscs",osc,"freq"]=freq
    def get_demod_power(self, demod, sigout, only_enabled=True):
        amplitude=self["sigouts",sigout,"amplitudes",demod]
        enable=(not only_enabled) or self["sigouts",sigout,"enables",demod]
        if enable:
            return np.log10(amplitude**2/(2*50.)/1E-3)*10.
        else:
            return None
    def set_demod_power(self, demod, sigout, power_dBm=None, enable=True):
        if power_dBm is not None:
            amplitude=(10**(power_dBm*0.1)*1E-3*2*50)**0.5
            self["sigouts",sigout,"amplitudes",demod]=amplitude
        self["sigouts",sigout,"enables",demod]=enable
    
    def read_demods(self, trace_length, demods=None, save_frequencies_for=None, buffer_size=None, sanitize_data=True, consistent_length=False):
        return self.read_demods_poll(trace_length,demods=demods,save_frequencies_for=save_frequencies_for,sanitize_data=sanitize_data,consistent_length=consistent_length)
    def get_demod(self, demod_idx):
        return Demod(demod_idx,self)
        
    def read_demod_pts(self, trace_pts, demod, poll_time=None, sanitize_data=True):
        rate=self.get_demods_rates()[demod]
        if not rate:
            return []
        trace_length=(trace_pts/rate*1.2)+0.05
        if poll_time is not None:
            trace_length=max(trace_length,poll_time)
        data=self.read_demods_poll(trace_length,sanitize_data=sanitize_data)
        if data is not None:
            data=data[demod]
            if poll_time is not None:
                chunks=int(len(data)//trace_pts)
                if chunks>0:
                    data=[data[trace_pts*i:trace_pts*(i+1),:] for i in range(chunks)]
                else:
                    data=[]
            else:
                if len(data)>trace_pts:
                    data=[data[:trace_pts,:]]
                else:
                    data=[]
        return data
    def repeat_read_demod_pts(self, trace_pts, demod, traces_num=1, poll_time=None):
        traces=[]
        while len(traces)<traces_num:
            pts=self.read_demod_pts(trace_pts,demod,poll_time=poll_time)
            if pts is not None:
                traces=traces+pts
        return traces[:traces_num]
        
    class DemodTraceAccumulator(object):
        def __init__(self, rate, length, columns=3):
            object.__init__(self)
            self.rate=rate
            self.length=length
            self.columns=columns
            self.points_num=int(np.ceil(rate*length))
            self.data=np.zeros((self.points_num,columns))
            self.position=0
        def add_piece(self, *traces):
            add_l=min([len(t) for t in traces]+[self.points_num-self.position])
            for t in range(self.columns):
                self.data[self.position:self.position+add_l,t]=traces[t][:add_l]
            self.position=self.position+add_l
            if self.position==self.points_num:
                return True
            else:
                return False
        def full(self):
            return self.position==self.points_num
    
    def _parse_demods_data(self, data, demods=None, auxin_demod=None, save_demod_frequency=None):
        dnum=self.get_demods_num()
        demods=demods or range(dnum)
        save_demod_frequency=save_demod_frequency or [False]*dnum
        traces=[]
        if self.dev_id in data:
            data=data[self.dev_id]['demods']
            for d in demods:
                if str(d) in data:
                    if len(data[str(d)]["sample"])>0:
                        sample_data=data[str(d)]['sample']
                        if isinstance(sample_data,list):
                            sample_data=sample_data[0]
                        traces_to_save=[sample_data['timestamp']-self.ref_timestamp,sample_data['x'],sample_data['y']]
                        if save_demod_frequency[d]:
                            traces_to_save.append(sample_data['frequency'])
                        traces.append(traces_to_save)
                    else:
                        traces.append(None)
                else:
                    traces.append(None)
            if auxin_demod is not None:
                auxin_demod=str(auxin_demod)
                if auxin_demod in data and len(data[auxin_demod]["sample"])>0:
                    sample_data=data[auxin_demod]['sample']
                    if isinstance(sample_data,list):
                        sample_data=sample_data[0]
                    traces.append([sample_data['timestamp']-self.ref_timestamp,sample_data['auxin0'],sample_data['auxin1']])
                else:
                    traces.append(None)
        else:
            traces=[[] for _ in demods]
            if auxin_demod is not None:
                traces=traces+[None]
        data=[]
        for d,t in zip(demods,traces):
            if t is None:
                c=4 if save_demod_frequency[d] else 3
                data.append(np.zeros((0,c)))
            else:
                data.append(np.column_stack(t))
        data.append(np.column_stack(traces[-1]))
        return data
    
    def read_demods_poll(self, trace_length, demods=None, save_frequencies_for=None, sanitize_data=True, consistent_length=False):
        rates=self.get_demods_rates()
        demods=demods or range(len(rates))
        length_factor=1.1 if consistent_length else 1.
        max_rate=max(rates)
        max_rate_demod=rates.index(max_rate)
        save_frequencies_for=save_frequencies_for or []
        save_demod_frequency=[(d in save_frequencies_for) for d in range(8)]
        self.sync()
        for d in demods:
            self.server.subscribe(self._build_path(("demods",d,"sample")))
        data=self.server.poll(trace_length*length_factor,500,2)
        for d in demods:
            self.server.unsubscribe(self._build_path(("demods",d,"sample")))
        data=self._parse_demods_data(data,demods,max_rate_demod,save_demod_frequency)
        if sanitize_data or consistent_length:
            if not check_all_timestamps(data):
                return None
            max_length=trace_length*self.get_clockbase() if consistent_length else None
            return align_all_timestamps(data,max_length=max_length)
        else:
            return data
        
    
    ### SCOPE ###
    
    def get_auxin_sample(self, channel, fmt="float"):
        funcargparse.check_parameter_range(fmt,"fmt",{"dict","float"})
        res=self.get_parameter(("auxins/0/sample"),"auxin_sample")
        if fmt=="dict":
            return res
        else:
            return res["ch{}".format(channel)][0]
    
    def get_scope_trace_pts(self):
        return self["scopes/0/length"] 
    def set_scope_trace_pts(self, length):
        self["scopes/0/length"]=length
    _scope_sources=["sigin0","sigin1","sigout0","sigout1"]
    _scope_ranges={"sigin0":"sigins/0/range","sigin1":"sigins/1/range",
                     "sigout0":"sigouts/0/range","sigout1":"sigouts/1/range"}
    def get_scope_source_idx(self, source):
        funcargparse.check_parameter_range(source,"source",self._scope_sources)
        return self._scope_sources.index(source)
    def get_scope_source_range(self, source):
        if isinstance(source,str):
            funcargparse.check_parameter_range(source,"source",self._scope_sources)
        else:
            source=self._scope_sources[source]
        return self[self._scope_ranges[source]]
    def get_scope_timestep_idx(self):
        return self["scopes/0/time"]
    def get_scope_timestep(self, timestep_idx=None):
        if timestep_idx is None:
            timestep_idx=self["scopes/0/time"]
        return 2**timestep_idx/self.get_clockbase()
    def get_scope_time_points(self, length=None):
        length=length or self.get_scope_trace_pts()
        return np.arange(length)*self.get_scope_timestep()
    def setup_trigger(self, channel="continuous", edge="rising", level=0., delay=0., holdoff=0.):
        raise NotImplementedError("ZIDevice.setup_trigger")
    def setup_scope(self, timestep_idx=None, source="sigin0", trace_pts=None, bw_limit=True):
        raise NotImplementedError("ZIDevice.setup_scope")
    def read_scope_poll(self, traces=1, poll_time=None, add_time=False, timeout="auto", fast_flush=False):
        raise NotImplementedError("ZIDevice.read_scope_poll")
    def read_scope(self, timestep_idx=None, source="sigin0", traces=1, trace_pts=None, poll_time=None, add_time=False, bw_limit=True, timeout="auto"):
        self.setup_scope(timestep_idx,source,trace_pts,bw_limit)
        return self.read_scope_poll(traces,poll_time,timeout=timeout,add_time=add_time)
    
    
    
    
    
    
    
class HF2Device(ZIDevice):
    """
    Zurich Instruments HF2 device.
    """
    def __init__(self, dev_id=None, port=8005):
        ZIDevice.__init__(self,dev_id=dev_id,port=port,api_level=1)
        self._scope_trigger=-2
            
            
    ### PROPERTIES ###
    
    def get_clockbase(self):
        return 210E6
    
    
    ### DEMODS ###
    
    def get_demods_rates(self):
        return [self.get_parameter(("demods",d,"rate")) for d in range(6)]
    def set_demod_rate(self, demod, rate):
        if rate<=0:
            rate=0
        self["demods",demod,"rate"]=rate
    
    
    
    ### SCOPE ###
    
    def get_scope_trace_pts(self):
        return 2048
    def set_scope_trace_pts(self, length):
        if length!=2048:
            raise ValueError("for HF2 the number of scope points is always 2048")
    def get_scope_source(self):
        return self._scope_sources[self["scopes/0/channel"]]
    
    def _parse_scope_data(self, data, trace_pts=None):
        path="/{}/scopes/0/wave".format(self.dev_id)
        if path not in data:
            return []
        waves=data[path]
        traces=[]
        rng=self.get_scope_source_range(waves[0]["scopechannel"])
        trace_pts=trace_pts or len(waves[0]["wave"])
        for w in waves:
            if len(w["wave"])==trace_pts:
                traces.append(w["wave"]/(2.**15)*rng)
        return traces
    
    def setup_trigger(self, channel="continuous", edge="rising", level=0., delay=0., holdoff=0.):
        funcargparse.check_parameter_range(channel,"channel",self._scope_sources+["continuous"])
        funcargparse.check_parameter_range(edge,"edge",{"rising","falling"})
        self._scope_trigger=self._scope_sources.index(channel) if channel in self._scope_sources else -2
        self["scopes/0/trigedge"]=(edge=="rising")
        if channel in self._scope_sources:
            rng=self.get_scope_source_range(channel)
            self["scopes/0/triglevel"]=int(level/rng*32767.)
        self["scopes/0/trigholdoff"]=holdoff
    def setup_scope(self, timestep_idx=None, source="sigin0", trace_pts=None, bw_limit=True):
        self["scopes/0/channel"]=self.get_scope_source_idx(source)
        self["scopes/0/bwlimit"]=bw_limit
        if timestep_idx is not None:
            if timestep_idx>15 or timestep_idx<0:
                raise ValueError("timestep_idx is an integer between 0 and 15")
            self["scopes/0/time"]=timestep_idx
        if trace_pts is not None:
            self.set_scope_trace_pts(trace_pts)
        self.server.sync()
    def read_scope_poll(self, traces=1, poll_time=None, add_time=False, timeout="auto", fast_flush=True):
        if add_time:
            raise ValueError("HF2 doesn't support scope timestamps")
        trace_pts=self.get_scope_trace_pts()
        trace_length=trace_pts*self.get_scope_timestep()
        trace_length=max(1E-3,trace_length)
        res=[]
        if poll_time is None:
            total_length=traces*trace_length*1.2
        else:
            total_length=poll_time
        if timeout=="auto":
            timeout=max(total_length*3,1.)
        t=time.time()
        while len(res)<traces:
            if timeout is not None and (time.time()>t+timeout):
                raise RuntimeError("execution timed out; trace length changed during execution?")
            if fast_flush:
                self.server.poll(1E-3,1)
            else:
                #self.server.flush()
                self.server.sync()
            self.server.subscribe(self._build_path(["scopes/0/wave"]))
            self["scopes/0/trigchannel"]=self._scope_trigger
            data=self.server.poll(total_length,500,0,True)
            self["scopes/0/trigchannel"]=-1
            self.server.unsubscribe(self._build_path(["scopes/0/wave"]))
            data=self._parse_scope_data(data,trace_pts=trace_pts)
            if poll_time is not None:
                return data
            res=res+data
            if len(data)==0:
                total_length=total_length*2
            else:
                total_length=total_length/len(data)*(traces-len(res))
        return res[:traces]
        
    
    
    



class UHFDevice(ZIDevice):
    """
    Zurich Instruments UHF device.
    """
    def __init__(self, dev_id=None, port=8004):
        ZIDevice.__init__(self,dev_id=dev_id,port=port,api_level=4)
        
    ### DEMODS ###
    
    def get_demods_rates(self):
        return [self.get_parameter(("demods",d,"rate")) if self.get_parameter(("demods",d,"enable")) else 0. for d in range(8)]
    def set_demod_rate(self, demod, rate):
        if rate<=0:
            self["demods",demod,"enable"]=False
        else:
            self["demods",demod,"rate"]=rate
            self["demods",demod,"enable"]=True
    
    
    ### SCOPE ###
    
    _scope_sources=["sigin0","sigin1","trigin0","trigin1"]+[None]*4+["auxin0","auxin1"]
    _scope_ranges={"sigin0":"sigins/0/range","sigin1":"sigins/1/range"}
    def get_scope_source_idx(self, source):
        funcargparse.check_parameter_range(source,"source",self._scope_sources)
        return self._scope_sources.index(source)
    def get_scope_source_range(self, source):
        if isinstance(source,str):
            funcargparse.check_parameter_range(source,"source",self._scope_sources)
        else:
            source=self._scope_sources[source]
            if source is None:
                raise KeyError("can't access source index {}".format(source))
        if source.startswith("auxin"):
            return 10.
        elif source.startswith("trigin"):
            return 1.
        else:
            return self[self._scope_ranges[source]]
    def get_scope_source(self):
        return self._scope_sources[self["scopes/0/channels/0/inputselect"]]
    
    def _parse_scope_data(self, data, trace_pts=None):
        path=[self.dev_id,"scopes","0","wave"]
        waves=data
        for p in path:
            if p not in waves:
                return [],[]
            waves=waves[p]
        traces=[]
        starts=[]
        trace_pts=trace_pts or waves[0]["totalsamples"]
        bn=0
        blocks=[]
        cstart=None
        for w in waves:
            if w.get("blocknumber",0)!=bn: # missing/extra block
                bn=0
                blocks=[]
                continue
            scale=w["channelscaling"]
            offset=w["channeloffset"]
            blk=((w["wave"]*scale)+offset)[:,0]
            blocks.append(blk)
            if bn==0: # first block of the traces
                cstart=w["timestamp"]-self.ref_timestamp
            if w.get("blockmarker",1)==1: # last block
                tr=blocks[0] if len(blocks)==1 else np.concatenate(blocks)
                if len(tr)==trace_pts:
                    traces.append(tr)
                    starts.append(cstart)
                bn=0
                blocks=[]
            else:
                bn=bn+1
        return traces,starts
    def setup_trigger(self, channel="continuous", edge="rising", level=0., delay=0., holdoff=0.):
        funcargparse.check_parameter_range(channel,"channel",self._scope_sources+["continuous"])
        funcargparse.check_parameter_range(edge,"edge",{"rising","falling","both"})
        if channel=="continuous":
            self["scopes/0/trigenable"]=0
        else:
            self["scopes/0/trigenable"]=1
            self["scopes/0/trigchannel"]=self.get_scope_source_idx(channel)
        self["scopes/0/trigrising" ]=(edge in {"rising" ,"both"})
        self["scopes/0/trigfalling"]=(edge in {"falling","both"})
        self["scopes/0/triglevel"]=level
        self["scopes/0/trigdelay"]=delay
        self["scopes/0/trigholdoff"]=holdoff
        if channel!="continuous":
            self["scopes/0/trigenable"]=0
            self["scopes/0/trigenable"]=1
    def setup_scope(self, timestep_idx=None, source="sigin0", trace_pts=None, bw_limit=True):
        self["scopes/0/channels/0/inputselect"]=self.get_scope_source_idx(source)
        self["scopes/0/channels/0/bwlimit"]=bw_limit
        if timestep_idx is not None:
            if timestep_idx>16 or timestep_idx<0:
                raise ValueError("timestep_idx is an integer between 0 and 16")
            self["scopes/0/time"]=timestep_idx
        if trace_pts is not None:
            self.set_scope_trace_pts(trace_pts)
        self.server.sync()
    def read_scope_poll(self, traces=1, poll_time=None, add_time=False, timeout="auto", fast_flush=False, stop_after=True):
        trace_pts=self.get_scope_trace_pts()
        trace_length=trace_pts*self.get_scope_timestep()
        trace_length=max(0.01,trace_length)
        res=[]
        res_starts=[]
        if poll_time is None:
            total_length=traces*trace_length*1.2+trace_pts/10E6
        else:
            total_length=poll_time
        if timeout=="auto":
            timeout=max(total_length*3,1.)
        poll_to=max(50,min(500,int(total_length*1E3)))
        t=time.time()
        while len(res)<traces:
            if timeout is not None and (time.time()>t+timeout):
                raise RuntimeError("execution timed out; trace length changed during execution?")
            if fast_flush:
                self.server.poll(1E-3,1)
            else:
                self.server.sync()
            self.server.subscribe(self._build_path(["scopes/0/wave"]))
            self["scopes/0/enable"]=1
            data=self.server.poll(total_length,poll_to,0)
            #data=None
            if stop_after:
                self["scopes/0/enable"]=0
            self.server.unsubscribe(self._build_path(["scopes/0/wave"]))
            #return data
            data,starts=self._parse_scope_data(data,trace_pts=trace_pts)
            if add_time:
                ts=self.get_scope_timestep()
                data=[np.column_stack(( np.arange(len(d))*ts,d )) for d in data]
            if poll_time is not None:
                return (data,starts) if add_time else data
            res=res+data
            res_starts=res_starts+starts
            if len(data)==0:
                total_length=total_length*2
            else:
                total_length=total_length/len(data)*(traces-len(res))
        return (res[:traces],res_starts[:traces]) if add_time else res[:traces]
    
    def read_demods_with_scope(self, trace_length, demods=None):
        rates=self.get_demods_rates()
        demods=demods or range(len(rates))
        max_rate=max(rates)
        max_rate_demod=rates.index(max_rate)
        self.sync()
        for d in demods:
            self.server.subscribe(self._build_path(("demods",d,"sample")))
        self.server.subscribe(self._build_path(["scopes/0/wave"]))
        self["scopes/0/enable"]=1
        self.server.sync()
        raw_data=self.server.poll(trace_length,500,2)
        self["scopes/0/enable"]=0
        self.server.unsubscribe(self._build_path(["scopes/0/wave"]))
        for d in demods:
            self.server.unsubscribe(self._build_path(("demods",d,"sample")))
        demod_data=self._parse_demods_data(raw_data,demods,max_rate_demod)
        demod_data=align_all_timestamps(cut_to_largest_chunk(demod_data))
        data_extent=(demod_data[-1][0,0],demod_data[-1][-1,0])
        scope_data=self._parse_scope_data(raw_data,trace_pts=self.get_scope_trace_pts())
        scope_data=[sd for sd in zip(*scope_data) if sd[1]>data_extent[0] and sd[1]<data_extent[1]]
        dts=int(self.get_scope_timestep()*self.get_clockbase())
        scope_data=[np.column_stack(( np.arange(len(d[0]))*dts+d[1],d[0] )) for d in scope_data]
        return demod_data,scope_data
    
    
    
    
    
    

class ZISweeper(object):
    """
    Sweeper interface for Zurich Instruments devices.
    """
    def __init__(self, dev, settings=None):
        object.__init__(self)
        self.settings=dictionary.Dictionary(settings)
        self.settings.merge_branch(self._default_settings,overwrite=False)
        self.dev=dev
    def __getitem__(self, key): return self.settings.__getitem__(key)
    def __setitem__(self, key, value): return self.settings.__setitem__(key,value)

    _default_settings={"log_sweep":False,
                       "wait/initial":5,
                       "wait/settling":5,
                       "wait/integrating":5,
                       "wait/averaging_pause":5,
                       "averaging":1,
                       "tc":None,
                       "order":None}
    def is_set(self):
        return all([k in self.settings for k in ["range","oscillator","demods"]])
    def setup(self, sweep_range, oscillator, demods, settings=None):
        self["range"]=sweep_range
        self["oscillator"]=oscillator
        self["demods"]=funcargparse.as_sequence(demods)
        if settings:
            self.settings.merge_branch(settings,overwrite=True)
        
    def frequency_points(self):
        if self["log_sweep"]:
            start,stop,steps=self["range"]
            logstart,logstop=np.log(start),np.log(stop)
            return np.exp(np.linspace(logstart,logstop,steps))
        else:
            return np.linspace(*self["range"])
    _min_tc=1E-3
    _sampling_rate_per_tc=100.
    _min_sampling_rate=1E3
    _min_int_time=1E-1
    def get_max_tc(self):
        tcs=[self.dev["demods",d,"timeconstant"] for d in self["demods"]]
        return max(max(tcs),self._min_tc)
    
    def get_tc(self, variable_tc=False):
        if self["tc"] is not None:
            for d in self["demods"]:
                self.dev["demods",d,"timeconstant"]=self["tc"][0] if variable_tc else self["tc"]
        if self["order"] is not None:
            for d in self["demods"]:
                self.dev["demods",d,"order"]=self["order"]
        return self.get_max_tc()
    
    def execute(self, result_format=("c","comb"), method="zi"):
        if method=="zi":
            return self.execute_zi(result_format)
        else:
            return self.execute_manual(result_format)
    def execute_manual(self, result_format=("c","comb")):
        funcargparse.check_parameter_range(result_format[0],"result_format",{"xy","c"})
        funcargparse.check_parameter_range(result_format[1],"result_format",{"sep","comb"})
        if not self.is_set():
            raise ValueError("setup sweeper first")
        dev=self.dev
        demods=self["demods"]
        variable_tc=funcargparse.is_sequence(self["tc"])
        tc=self.get_tc(variable_tc=variable_tc)
        sampling_rate=max(self._min_sampling_rate,self._sampling_rate_per_tc/tc)
        initial_rates=dev.get_demods_rates()
        for d in range(dev.get_demods_num()):
            dev.set_demod_rate(d,sampling_rate if (d in demods) else 0)
        avgs=self["averaging"]
        values=[[] for _ in demods]
        freqs=self.frequency_points()
        dev.set_parameter(("oscs",self["oscillator"],"freq"),freqs[0])
        time.sleep(tc*self["wait/initial"])
        for i,f in enumerate(freqs):
            dev.set_parameter(("oscs",self["oscillator"],"freq"),f)
            if variable_tc:
                tc=max(self["tc"][i],self._min_tc)
                sampling_rate=max(self._min_sampling_rate,self._sampling_rate_per_tc/tc)
                for d in demods:
                    dev["demods",d,"timeconstant"]=tc
                    dev.set_demod_rate(d,sampling_rate)
            time.sleep(tc*self["wait/settling"])
            integrating_time=max(tc*self["wait/integrating"],self._min_int_time)
            avg_data=[[] for _ in demods]
            for i in range(avgs):
                while True:
                    data=dev.read_demods(integrating_time*1.1)
                    if data is not None:
                        break
                for d,a in zip(demods,avg_data):
                    a.append(data[d][:,1:].mean(axis=0))
                if i+1<avgs:
                    time.sleep(tc*self["wait/averaging_pause"])
            for v,a in zip(values,avg_data):
                sam_xy=np.mean(a,axis=0)
                if result_format[0]=="xy":
                    v.append(sam_xy)
                else:
                    v.append(sam_xy[0]+1j*sam_xy[1])
        for d,r in enumerate(initial_rates):
            dev.set_demod_rate(d,r)
        if result_format[1]=="sep":
            return [np.column_stack(( freqs,v )) for v in values]
        else:
            return np.column_stack([freqs]+values)
    
    def execute_zi(self, result_format=("c","comb"), poll_time=.1):
        funcargparse.check_parameter_range(result_format[0],"result_format",{"xy","c"})
        funcargparse.check_parameter_range(result_format[1],"result_format",{"sep","comb"})
        dev=self.dev
        if not self.is_set():
            raise ValueError("setup sweeper first")
        tc=self.get_tc()
        if self["order"] is None:
            order=max([dev["demods",d,"order"] for d in self["demods"]])
        else:
            order=self["order"]
        sweeper=self.dev.server.sweep(500)
        sweeper.set("sweep/device",dev.dev_id)
        sweeper.set("sweep/start",self["range"][0])
        sweeper.set("sweep/stop",self["range"][1])
        sweeper.set("sweep/samplecount",self["range"][2])
        sweeper.set("sweep/gridnode","oscs/{}/freq".format(self["oscillator"]))
        sweeper.set("sweep/xmapping",1 if self["log_sweep"] else 0)
        sweeper.set("sweep/scan",0)
        #sweeper.set("sweep/settling/time",0)
        sweeper.set("sweep/settling/time",self["wait/initial"]*tc)
        sweeper.set("sweep/settling/tc",self["wait/settling"])
        sweeper.set("sweep/averaging/tc",self["wait/integrating"])
        '''sweeper.set("sweep/settling/time",self["wait/settling"]*tc)
        sweeper.set("sweep/settling/tc",self["wait/integrating"])
        sweeper.set("sweep/averaging/tc",0)'''
        sweeper.set("sweep/averaging/sample",self["averaging"])
        sweeper.set("sweep/bandwidthcontrol",0)
        sweeper.set("sweep/bandwidth",tc_to_bandwidth(tc,order))
        sweeper.set("sweep/order",order)
        for d in self["demods"]:
            sweeper.subscribe(dev._build_path(("demods",d,"sample")))
            
        sampling_rate=max(self._min_sampling_rate,self._sampling_rate_per_tc/tc)
        initial_rates=dev.get_demods_rates()
        for d in range(dev.get_demods_num()):
            dev.set_demod_rate(d,sampling_rate if (d in self["demods"]) else 0)
        sweeper.execute()
        sweeper.trigger()
        while not(sweeper.finished()):
            time.sleep(poll_time)
        for d,r in enumerate(initial_rates):
            dev.set_demod_rate(d,r)
        sweeper_data=sweeper.read()
        if dev.dev_id not in sweeper_data:
            return None
        values=[]
        freqs=None
        for d in self["demods"]:
            ds=sweeper_data[dev.dev_id]["demods"][str(d)]["sample"]
            if len(ds)==0:
                return None
            ds=ds[0][0]
            if result_format[0]=="xy":
                values.append(np.column_stack(( ds["x"],ds["y"] )))
            else:
                values.append(ds["x"]+1j*ds["y"])
            if freqs is None:
                freqs=ds["frequency"]
        if result_format[1]=="sep":
            return [np.column_stack(( freqs,v )) for v in values]
        else:
            return np.column_stack([freqs]+values)