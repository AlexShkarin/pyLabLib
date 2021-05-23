"""
Traces feature detection: peaks, baseline, local extrema.
"""

from builtins import range

from ..utils import funcargparse
from . import waveforms, specfunc, filters

import numpy as np
import collections

### Baseline ###


class Baseline(collections.namedtuple("Baseline",["position","width"])): # making Sphinx autodoc generate correct docstring
    """
    Baseline (background) for a trace.
    
    `position` is the background level, and `width` is its noise width.  
    """
Baseline.__new__.__defaults__=(0.,1.)

def get_baseline_simple(trace, find_width=True):
    """
    Get the baseline of the 1D trace.
    
    If ``find_width==True``, calculate its width as well. 
    """
    if np.iscomplexobj(trace):
        blr=get_baseline_simple(trace.real,find_width=find_width)
        bli=get_baseline_simple(trace.imag,find_width=find_width)
        return Baseline(blr.position+bli.position,blr.width+bli.width)
    pos=np.median(trace)
    if find_width:
        l=len(trace)
        if l<4:
            width=trace.std()
        else:
            trace=np.sort(trace)
            width=(trace[(3*l//4)]-trace[l//4])/2.
            width=trace[(l//4):(3*l//4)].std()
    else:
        width=1.
    return Baseline(pos,width)
def subtract_baseline(trace):
    """
    Subtract baseline from the trace (make its background zero).
    """
    background=get_baseline_simple(trace,find_width=False).position
    return trace-background


### Peaks ###

class Peak(collections.namedtuple("Peak",["position","height","width","kernel"])): # making Sphinx autodoc generate correct docstring
    """
    A trace peak.
    
    `kernel` defines its shape (for, e.g., generation purposes).  
    """
Peak.__new__.__defaults__=(0.,1.,1.,"generic")
        
        
def find_peaks_cutoff(trace, cutoff, min_width=0, kind="peak", subtract_bl=True):
    """
    Find peaks in the data using cutoff.
    
    Args:
        trace: 1D data array.
        cutoff (float): Cutoff value for the peak finding.
        min_width (int): Minimal uninterrupted width (in datapoints) of a peak. Any peaks this width are ignored.
        kind (str): Peak kind. Can be ``'peak'`` (positive direction), ``'dip'`` (negative direction) or ``'both'`` (both directions).
        subtract_bl (bool): If ``True``, subtract baseline of the trace before checking cutoff.
    
    Returns:
        List of :class:`Peak` objects.
    """
    funcargparse.check_parameter_range(kind, "kind", {"peak","dip","both"})
    if subtract_bl:
        trace=subtract_baseline(trace)
    if kind=="peak":
        state=(trace> cutoff).astype("int")
    elif kind=="dip":
        state=(trace<-cutoff).astype("int")
    else:
        state=(abs(trace)>abs(cutoff)).astype("int")
    edge=state[1:]-state[:-1]
    cross_up=list((edge==1).nonzero()[0])
    if state[0]==1:
        cross_up=[-1]+cross_up
    cross_down=list((edge==-1).nonzero()[0])
    if state[-1]==1:
        cross_down=cross_down+[len(trace)-1]
    assert(len(cross_up)==len(cross_down))
    peaks=[]
    for l,r in zip(cross_up,cross_down):
        assert(r>l)
        if r-l>=min_width:
            w=r-l
            p=(r+l)/2.+1.
            h=np.mean(trace[l+1:r+1])
            peaks.append(Peak(p,h,w))
    return peaks

def rescale_peak(peak, xoff=0., xscale=1., yoff=0, yscale=1.):
    """
    Rescale peak's position, width and height.

    `xscale` rescales position and width, `xoff` shifts position, `yscale` and `yoff` affect peak height.
    """
    return Peak(peak.position*xscale+xoff,peak.height*yscale+yoff,peak.width*xscale,peak.kernel)

def peaks_sum_func(peaks, peak_func="lorentzian"):
    """
    Create a function representing sum of `peaks`.
    
    `peak_func` determines default peak kernel (used if ``peak.kernel=="generic"``).
    Kernel is either a name string or a function taking 3 arguments ``(x, width, height)``.
    """
    def f(x):
        res=None
        for p in peaks:
            pf=specfunc.get_kernel_func(peak_func if p.kernel=="generic" else p.kernel)
            pres=pf(x-p.position,p.width,p.height)
            res=pres if res is None else res+pres
        return res
    return f




def get_kernel(width, kernel_width=None, kernel="lorentzian"):
    """
    Get a finite-sized kernel.

    Return 1D array of length ``2*kernel_width+1`` containing the given kernel.
    By default, ``kernel_width=int(width*3)``.
    """
    kernel=specfunc.get_kernel_func(kernel)
    if kernel_width is None:
        kernel_width=width*3
    xs=np.arange(-int(kernel_width),int(kernel_width)+.5)
    peakk=kernel(xs,width)
    return peakk/np.sum(peakk)

def get_peakdet_kernel(peak_width, background_width, norm_width=None, kernel_width=None, kernel="lorentzian"):
    """
    Get a peak detection kernel.

    Return 1D array of length ``2*kernel_width+1`` containing the kernel.
    The kernel is a sum of narrow positive peak (with the width `peak_width`) and a broad negative peak (with the width `background_width`);
    both widths are specified in datapoints (index).
    Each peak is normalized to have unit sum, i.e., the kernel has zero total sum.
    By default, ``kernel_width=int(background_width*3)``.
    """
    kernel=specfunc.get_kernel_func(kernel)
    if kernel_width is None:
        kernel_width=background_width*3
    xs=np.arange(-int(kernel_width),int(kernel_width)+.5)
    peakk=kernel(xs,peak_width)
    backk=kernel(xs,background_width)
    return peakk/np.sum(peakk)-backk/np.sum(backk)

def multi_scale_peakdet(trace, widths, background_ratio, kind="peak", norm_ratio=None, kernel="lorentzian"):
    """
    Detect multiple peak widths using :func:`get_peakdet_kernel` kernel.

    Args:
        trace: 1D data array.
        widths ([float]): Array of possible peak widths.
        background_ratio (float): ratio of the `background_width` to the `peak_width` in :func:`get_peakdet_kernel`.
        kind (str): Peak kind. Can be ``'peak'`` (positive direction) or ``'dip'`` (negative direction).
        norm_ratio (float): if not ``None``, defines the width of the "normalization region" (in units of the kernel width, same as for the background kernel);
            it is then used to calculate a local trace variance to normalize the peaks magnitude.
        kernel: Peak matching kernel.

    Returns:
        Filtered trace which shows peak 'affinity' at each point.
    """
    funcargparse.check_parameter_range(kind, "kind", {"peak","dip"})
    peakdet_traces=[]
    kernel_width=max(widths)*background_ratio*3
    for w in widths:
        k=get_peakdet_kernel(w,background_ratio*w,kernel_width=kernel_width,kernel=kernel)
        peak_trace=filters.convolve1d(trace,k)
        if norm_ratio:
            nk=get_kernel(norm_ratio*w,kernel_width=kernel_width,kernel=kernel)
            dev_trace=(trace-filters.convolve1d(trace,nk))**2
            norm_trace=filters.convolve1d(dev_trace,nk)**.5
            norm_trace[norm_trace<norm_trace.mean()*1E-3]=norm_trace.mean()*1E-3
            peak_trace/=norm_trace
        peakdet_traces.append(peak_trace)
    return np.max(peakdet_traces,axis=0) if kind=="peak" else -np.min(peakdet_traces,axis=0)



##### Finding minima/maxima #####

def find_local_extrema(wf, region_width=3, kind="max", min_distance=None):
    """
    Find local extrema (minima or maxima) of 1D waveform.
    
    `kind` can be ``"min"`` or ``"max"`` and determines the kind of the extrema. 
    Local minima (maxima) are defined as points which are smaller (greater) than all other points in the region of width `region_width` around it.
    `region_width` is always round up to an odd integer.
    `min_distance` defines the minimal distance between the exterma (``region_width//2`` by default).
    If there are several exterma within `min_distance`, their positions are averaged together.
    """
    if np.ndim(wf)!=1:
        raise ValueError("function only works with 1D arrays")
    dist=int(region_width//2)
    if min_distance is None:
        min_distance=dist
    l=len(wf)
    if kind=="max":
        extf=np.max
    elif kind=="min":
        extf=np.min
    else:
        raise ValueError("unrecognized extremum kind: {}".format(kind))
    if region_width<len(wf)*10 and len(wf)*region_width<=1E7: # faster workaround
        ewf=waveforms.expand_waveform(wf,size=dist,mode="nearest")
        regions=np.column_stack([ewf[i:l+i] for i in range(dist*2+1)])
        ext_values=extf(regions,axis=1)
        ext_idx=np.nonzero(wf==ext_values)[0]
    else:
        ext_idx=[i for i in range(len(wf)) if wf[i]==extf(wf[max(i-dist,0):min(l,i+dist+1)])]
    if min_distance<=1:
        return ext_idx
    filtered_idx=[]
    acc_idx=[]
    for mi in ext_idx:
        if acc_idx and mi-acc_idx[-1]>=min_distance:
            filtered_idx.append(int(np.mean(acc_idx)))
            acc_idx=[]
        acc_idx.append(mi)
    if acc_idx:
        filtered_idx.append(int(np.mean(acc_idx)))
    return filtered_idx




##### Threshold detection with hysteresis

def find_state_hysteretic(wf, threshold_off, threshold_on, normalize=True):
    """
    Determine on/off state in 1D array with hysteretic threshold algorithm.
    
    Return a state array containing ``+1`` for 'on' states and ``-1`` for 'off' states.
    The states switches from 'off' to 'on' when the value goes above `threshold_on`, and from 'on' to 'off' when the value goes below `threshold_off`.
    The intermediate states are determined by the nearest neighbor.
    """
    if threshold_off>threshold_on:
        raise ValueError("threshold_off can't be greater than threshold_on")
    if normalize:
        span=wf.max()-wf.min()
        if not span:
            return np.zeros(len(wf))
        wf=(wf-wf.min())/span
    states=1*(wf>threshold_on)+(-1)*(wf<threshold_off)
    if not states.any():
        return states
    unspec=(states==0).nonzero()[0]
    for u in unspec:
        if u>0:
            states[u]=states[u-1]
    unspec=(states==0).nonzero()[0] # in case the points in the beginning were undefined
    for u in unspec[::-1]:
        if u<len(states)-1:
            states[u]=states[u+1]
    return states

def trigger_hysteretic(wf, threshold_on, threshold_off, init_state="undef", result_kind="separate"):
    """
    Determine indices of rise and fall trigger events with hysteresis thresholds.
    
    Return either two arrays ``(rise_trig, fall_trig)`` containing trigger indices (if ``result_kind=="separate"``),
    or a single array of tuples ``[(dir,pos)]``, where `dir` is the trigger direction (``+1`` or ``-1``) and `pos` is its index  (if ``result_kind=="joined"``).
    Triggers happen when a state switch from 'high' to 'low' (rising) or vice versa (falling).
    The state switches from 'low' to 'high' when the trace value goes above `threshold_on`, and from 'high' to 'low' when the trace value goes below `threshold_off`.
    `init_state` specifies the initial state: ``"low"``, ``"high"``, or ``"undef"`` (undefined state).
    """
    if threshold_off>threshold_on:
        raise ValueError("off threshold level should be below on threshold level")
    trace_pos=wf>threshold_on
    trace_rise=trace_pos[1:]&(~trace_pos[:-1])
    trace_neg=wf<threshold_off
    trace_fall=trace_neg[1:]&(~trace_neg[:-1])
    if init_state=="undef":
        state=0
    elif init_state=="low":
        state=-1
    elif init_state=="high":
        state=1
    else:
        raise ValueError("unrecognized initial state: {}".format(init_state))
    trace_trig=trace_rise.astype(int)-trace_fall.astype(int)
    rise_trig=[]
    fall_trig=[]
    for i in trace_trig.nonzero()[0]:
        if state!=trace_trig[i]:
            state=trace_trig[i]
            if state>0:
                rise_trig.append(i)
            else:
                fall_trig.append(i)
    if result_kind=="separate":
        return rise_trig,fall_trig
    elif result_kind=="joined":
        res=[(1,i) for i in rise_trig]+[(-1,i) for i in fall_trig]
        res.sort(lambda x: x[1])
        return res
    else:
        raise ValueError("unrecognized result kind: {}".format(result_kind))