from ...core.dataproc import filters
from ...core.fileio import loadfile
from ...core.utils import general, funcargparse, py3
from .base import GenericSirahError

import numpy as np
import pandas as pd
import time
import contextlib


class FrequencyReadSirahError(GenericSirahError):
    """Sirah error indicating an error while trying to read frequency value"""
    def __init__(self, timeout=None):
        msg="could not read frequency in {} seconds".format(timeout) if timeout is not None else "could not read frequency"
        super().__init__(msg)
class MatisseTuner:
    """
    Matisse tuner.

    Helps to coordinate with an external wavemeter to perform more complicated tasks: motors calibration, fine frequency tuning, and stitching scans.

    Args:
        laser: opened Matisse laser object
        wavemeter: opened wavemeter object (currently only HighFinesse wavemeters are supported)
        calibration: either a calibration dictionary, or a path to the calibration dictionary file
    """
    def __init__(self, laser, wavemeter, calibration=None, ref_cell=True):
        self.laser=laser
        self.wavemeter=wavemeter
        self.apply_calibration(calibration)
        self._tune_units="int"
        self._fine_scan_start=None
        self._freq_avg_time=0
        self._last_read_frequency=None,0
        self._use_ref_cell=ref_cell
    def set_tune_units(self, units="int"):
        """
        Set default units for fine tuning and sweeping (fine sweep or stitched scan).
        
        Can be either ``"int"`` (internal units between 0 and 1) or ``"freq"`` (frequency units; requires calibration).
        """
        funcargparse.check_parameter_range(units,"units",["int","freq"])
        if (self._slow_piezo_cal is None or (self._use_ref_cell and self._ref_cell_cal is None)) and units=="freq":
            raise ValueError("frequency tuning units require calibration")
        self._tune_units=units
    def _check_device(self, device):
        if device=="ref_cell" and not self._use_ref_cell:
            raise ValueError("reference cell is disabled")
    def _to_int_units(self, value, device):
        if self._tune_units=="freq":
            self._check_device(device)
            if device=="slow_piezo":
                value=value/self._slow_piezo_cal
            elif device=="ref_cell":
                value=value/self._ref_cell_cal
        return value
    def apply_calibration(self, calibration):
        """
        Apply the given calibration.

        `calibration` is either a calibration dictionary, or a path to the calibration dictionary file.
        Contains information about the relation between bifi motor and wavelength, thin etalon motor span,
        slow piezo tuning rate (frequency to internal units) and its maximal sweep rate,
        ref cell tuning rate (frequency to internal units) and its maximal sweep rate.
        """
        if isinstance(calibration,py3.textstring):
            try:
                calibration=loadfile.load_dict(calibration)
            except (IOError,RuntimeError):
                raise GenericSirahError("could not load calibration file {}".format(calibration))
        if calibration is None:
            return
        if "te_search_rng" in calibration:
            self._te_search_rng=calibration["te_search_rng"]
        if "te_full_rng" in calibration:
            self._te_full_rng=calibration["te_full_rng"]
        if "te_plateau_scan_steps" in calibration:
            self._te_plateau_scan_steps=calibration["te_plateau_scan_steps"]
        if "te_plateau_step" in calibration:
            self._te_plateau_step=calibration["te_plateau_step"]
            self._te_center_step=max(1,self._te_plateau_step//3)
        if "bifi_full_rng" in calibration:
            self._bifi_full_rng=calibration["bifi_full_rng"]
        if "bifi_freqs" in calibration:
            self._bifi_freqs=calibration["bifi_freqs"]
        if "bifi_step_precision" in calibration:
            prec=calibration["bifi_step_precision"]
            self._bifi_search_step=(prec*8,2,prec)
        if "slow_piezo_cal" in calibration:
            self._slow_piezo_cal=calibration["slow_piezo_cal"]
        if "slow_piezo_max_speed" in calibration:
            self._slow_piezo_max_speed=calibration["slow_piezo_max_speed"]
        if "ref_cell_cal" in calibration:
            self._ref_cell_cal=calibration["ref_cell_cal"]
        if "ref_cell_max_speed" in calibration:
            self._ref_cell_max_speed=calibration["ref_cell_max_speed"]
    def get_frequency(self, timeout=1.):
        """
        Get current frequency reading.

        The only method relying on the wavemeter. Can be extended or overloaded to support different wavemeters.
        """
        avg_countdown=general.Countdown(self._freq_avg_time)
        countdown=general.Countdown(timeout)
        acc=[]
        while True:
            f=self.wavemeter.get_frequency(error_on_invalid=False)
            if isinstance(f,float):
                acc.append(f)
                if avg_countdown.passed():
                    self._last_read_frequency=np.mean(acc),time.time()
                    return self._last_read_frequency[0]
                time.sleep(1E-3)
                countdown.reset()
            elif countdown.passed():
                raise FrequencyReadSirahError(timeout)
            else:
                time.sleep(5E-3)
    def get_last_read_frequency(self, max_delay=1.):
        """Get the last valid read frequency, or ``None`` if none has been acquired yet"""
        if time.time()>self._last_read_frequency[1]+max_delay:
            return self.get_frequency()
        return self._last_read_frequency[0]
    def set_frequency_average_time(self, avg_time=0):
        """Set averaging time for frequency measurements (reduces measured frequency jitter)"""
        self._freq_avg_time=avg_time
    
    def _get_motor_position(self, motor):
        funcargparse.check_parameter_range(motor,"motor",["bifi","thinet"])
        return self.laser.bifi_get_position() if motor=="bifi" else self.laser.thinet_get_position()
    def _move_motor(self, motor, position, wait=True):
        funcargparse.check_parameter_range(motor,"motor",["bifi","thinet"])
        position=max(position,0)
        return self.laser.bifi_move_to(position,wait=wait) if motor=="bifi" else self.laser.thinet_move_to(position,wait=wait)
    def _move_motor_by(self, motor, steps, wait=True, rng=None):
        funcargparse.check_parameter_range(motor,"motor",["bifi","thinet"])
        newpos=self._get_motor_position(motor)+steps
        if rng is not None and (newpos<rng[0] or newpos>=rng[1]):
            return False
        self._move_motor(motor,newpos,wait=wait)
        return True
    def _is_motor_moving(self, motor):
        funcargparse.check_parameter_range(motor,"motor",["bifi","thinet"])
        return self.laser.bifi_is_moving() if motor=="bifi" else self.laser.thinet_is_moving()
    def scan_steps(self, motor, start, stop, step):
        """
        Scan the given motor (``"bifi"`` or ``"thinet"``) in discrete steps within the given range with a given step.

        Return a 4-column numpy array containing motor position, internal diode power, thin etalon reflection power, and wavemeter frequency.
        """
        self.unlock_all()
        diode_power=[]
        thinet_power=[]
        frequency=[]
        start,stop=sorted([start,stop])
        position=np.arange(start,stop,step)
        for p in position:
            self._move_motor(motor,p)
            diode_power.append(self.laser.get_diode_power())
            thinet_power.append(self.laser.get_thinet_power())
            frequency.append(self.get_frequency())
        return np.column_stack([position,diode_power,thinet_power,frequency])
    def scan_centered(self, motor, span, step):
        """
        Scan the given motor (``"bifi"`` or ``"thinet"``) in discrete steps in a given span around the current position.

        After the scan, return the motor to the original position.

        Return a 4-column numpy array containing motor position, internal diode power, thin etalon reflection power, and wavemeter frequency.
        """
        self.unlock_all()
        pos=self._get_motor_position(motor)
        scan=self.scan_steps(motor,pos-span/2,pos+span/2,step)
        self._move_motor(motor,pos)
        return scan
    def scan_quick(self, motor, start, stop, autodir=True):
        """
        Do a quick continuous scan of the given motor (``"bifi"`` or ``"thinet"``) within the given range.

        Compared to :meth:`scan_steps`, which does a series of discrete defined moves, this method does a single continuous move and records values in its progress.
        This is quicker, but does not allow for the step size control, and results in non-uniform recorded positions.
        If ``autodir==False``, first initialize the motor to `start` and then move to `stop`; otherwise, initialize to whichever border is closer.

        Return a 4-column numpy array containing motor position, internal diode power, thin etalon reflection power, and wavemeter frequency.
        """
        self.unlock_all()
        position=[]
        diode_power=[]
        thinet_power=[]
        frequency=[]
        if autodir:
            p=self._get_motor_position(motor)
            if abs(p-start)>abs(p-stop):
                start,stop=stop,start
        self._move_motor(motor,start)
        self._move_motor(motor,stop,wait=False)
        while self._is_motor_moving(motor):
            position.append(self._get_motor_position(motor))
            diode_power.append(self.laser.get_diode_power())
            thinet_power.append(self.laser.get_thinet_power())
            frequency.append(self.get_frequency())
        return np.column_stack([position,diode_power,thinet_power,frequency])
    def scan_quick_centered(self, motor, span):
        """
        Do a quick continuous scan of the given motor (``"bifi"`` or ``"thinet"``) in a given span around the current position.

        After the scan, return the motor to the original position.
        
        Return a 4-column numpy array containing motor position, internal diode power, thin etalon reflection power, and wavemeter frequency.
        """
        self.unlock_all()
        pos=self._get_motor_position(motor)
        scan=self.scan_quick(motor,pos-span/2,pos+span/2)
        self._move_motor(motor,pos)
        return scan
    def scan_both_motors(self, bifi_rng, te_rng, verbose=False):
        """
        Perform a 2D grid scan changing positions of both birefringent filter and thin etalon motors.

        `bifi_rng` and `te_rng` are both 3-tuples ``(start, stop, step)`` specifying the scan ranges.
        If ``verbose==True``, print a message per every birefringent filter position indicating the scan progress.
        
        Return a 5-column numpy array containing birefringent filter motor position, thin etalon motor position, internal diode power, thin etalon reflection power, and wavemeter frequency.
        """
        self.unlock_all()
        diode_power=[]
        thinet_power=[]
        frequency=[]
        bifi_position=np.arange(*bifi_rng)
        te_position=np.arange(*te_rng)
        t0=time.time()
        for i,bfp in enumerate(bifi_position):
            self._move_motor("bifi",bfp)
            for tep in te_position:
                self._move_motor("thinet",tep)
                diode_power.append(self.laser.get_diode_power())
                thinet_power.append(self.laser.get_thinet_power())
                frequency.append(self.get_frequency())
            if verbose:
                dt=time.time()-t0
                tleft=(dt)/(i+1)*(len(bifi_position)-i-1)
                print("{:3d} / {:3d}   {:5.1f}mins left".format(i+1,len(bifi_position),tleft/60))
        bffpos=bifi_position[None,:].repeat(len(te_position),axis=0).flatten()
        tefpos=te_position[:,None].repeat(len(bifi_position),axis=1).flatten()
        return np.column_stack([bffpos,tefpos,diode_power,thinet_power,frequency])
    def scan_both_motors_quick(self, bifi_rng, te_rng, verbose=False):
        """
        Perform a quick 2D grid scan changing positions of both birefringent filter and thin etalon motors.

        For each discrete position of a birefringent filter motor perform a quick scan of the thin etalon motor.
        `bifi_rng` is a 3-tuple ``(start, stop, step)``, while ``te_rng`` is a 2-tuple ``(start, stop)`` specifying the scan ranges.
        If ``verbose==True``, print a message per every birefringent filter position indicating the scan progress.
        
        Return a 5-column numpy array containing birefringent filter motor position, thin etalon motor position, internal diode power, thin etalon reflection power, and wavemeter frequency.
        """
        self.unlock_all()
        bffpos=[]
        tefpos=[]
        diode_power=[]
        thinet_power=[]
        frequency=[]
        bifi_position=np.arange(*bifi_rng)
        t0=time.time()
        for i,bfp in enumerate(bifi_position):
            self._move_motor("bifi",bfp)
            tescan=self.scan_quick("thinet",*te_rng[:2])
            bffpos+=[bfp]*len(tescan)
            tefpos+=list(tescan[:,0])
            diode_power+=list(tescan[:,1])
            thinet_power+=list(tescan[:,2])
            frequency+=list(tescan[:,3])
            if verbose:
                dt=time.time()-t0
                tleft=(dt)/(i+1)*(len(bifi_position)-i-1)
                print("{:3d} / {:3d}   {:5.1f}mins left".format(i+1,len(bifi_position),tleft/60))
        return np.column_stack([bffpos,tefpos,diode_power,thinet_power,frequency])

    def _get_thinet_range(self, t):
        prng=np.percentile(t.EtPower,10),np.percentile(t.EtPower,90)
        cutoff=prng[0]+(prng[1]-prng[0])*0.2
        inrng=t.ThinEt[t.EtPower>=cutoff]
        return np.percentile(inrng,10),np.percentile(inrng,90)
    def _get_motor_calibration(self, scan, cal=None):
        cal=cal or {}
        thinet_rngs=np.array([self._get_thinet_range(t) for _,t in scan.groupby("BiFi")])
        te_rng=np.median(thinet_rngs,axis=0)
        cal["te_search_rng"]=tuple(te_rng)
        cal["te_full_rng"]=tuple(te_rng+np.array([-1,1])*1000)
        fscan=scan[(scan.ThinEt>=te_rng[0])&(scan.ThinEt<te_rng[1])]
        freq_rngs=np.array([(bf,np.percentile(t.Freq,10),np.percentile(t.Freq,90)) for bf,t in fscan.groupby("BiFi")])
        valid_spans=freq_rngs[:,2]-freq_rngs[:,1]<1E12
        freq_rngs=freq_rngs[valid_spans]
        cal["bifi_full_rng"]=freq_rngs[:,0].min(),freq_rngs[:,0].max()
        bifi_freqs=np.column_stack((freq_rngs[:,0],(freq_rngs[:,1]+freq_rngs[:,2])/2))
        maxfreq=np.maximum.accumulate(bifi_freqs[:,1])
        bifi_freqs=bifi_freqs[bifi_freqs[:,1]==maxfreq]
        cal["bifi_freqs"]=bifi_freqs
        return cal
    _bifi_cal_rng=(100000,400000,400)
    _te_cal_rng=(2000,22000)
    def calibrate(self, motors=True, slow_piezo=True, slow_piezo_speeds=None, ref_cell=True, ref_cell_speeds=None, verbose=True, bifi_range=None, thinet_range=None, return_scans=True):
        """
        Calibrate the laser and return the calibration results.

        If ``motors==True``, perform motors calibration (bifi range and wavelengths, thin etalon range).
        If ``slow_piezo==True``, perform slow piezo calibration (ratio between internal tuning units and frequency shift).
        If ``slow_piezo_speeds`` is not ``None``, it defines a list of slow piezo tuning speeds to use for the calibration (in case it depends on the speed).
        If ``ref_cell==True``, perform ref cell calibration (ratio between internal tuning units and frequency shift).
        If ``ref_cell_speeds`` is not ``None``, it defines a list of ref cell tuning speeds to use for the calibration (in case it depends on the speed).
        If `bifi_range` is specified, it is a tuple ``(start, stop, step)`` defining the tested bifi positions (default is between 100000 and 400000 with a step of 400).
        If `thinet_range` is specified, it is a tuple ``(start, stop)`` defining the tested thin etalon position range.
        IF ``verbose==True``, print the progress updates during scan.
        If ``return_scans==True``, return a tuple ``(calibration, scans)``, where ``scans`` is a tuple ``(motor_scan, slow_piezo_scan, ref_cell)`` containing detail scan result tables;
        otherwise, return just the calibration dictionary.
        """
        cal={}
        if motors:
            if verbose:
                print("Calibrating motors")
            bifi_range=self._bifi_cal_rng if bifi_range is None else bifi_range
            thinet_range=self._te_cal_rng if thinet_range is None else thinet_range
            mot_scan=self.scan_both_motors_quick(bifi_range,thinet_range,verbose=verbose)
            mot_scan=pd.DataFrame(mot_scan,columns=["BiFi","ThinEt","Power","EtPower","Freq"])
            cal=self._get_motor_calibration(mot_scan,cal=cal)
            self.apply_calibration(cal)
        else:
            mot_scan=None
        slow_piezo_scan=None
        if slow_piezo and len(self._bifi_freqs):
            if verbose:
                print("Calibrating slow piezo response")
            slow_piezo_cal_freqs=np.linspace(self._bifi_freqs[:,1].min(),self._bifi_freqs[:,1].max(),12)[1:-1]
            slow_piezo_scan=[]
            t0=time.time()
            if slow_piezo_speeds is None:
                slow_piezo_speeds=[self._slow_piezo_max_speed]
            slow_piezo_speeds=sorted(slow_piezo_speeds)
            for i,f in enumerate(slow_piezo_cal_freqs):
                self.tune_to(f,level="thinet")
                for s in slow_piezo_speeds:
                    slope,_=self._estimate_slow_piezo_slope(speed=s)
                    slow_piezo_scan.append((f,s,slope))
                if verbose:
                    dt=time.time()-t0
                    tleft=(dt)/(i+1)*(len(slow_piezo_cal_freqs)-i-1)
                    print("{:3d} / {:3d}   {:5.1f}mins left".format(i+1,len(slow_piezo_cal_freqs),tleft/60))
            slow_piezo_scan=pd.DataFrame(slow_piezo_scan,columns=["Freq","Speed","Slope"])
            split_slow_piezo_scans={s:t for s,t in slow_piezo_scan.groupby("Speed")}
            self._slow_piezo_cal=cal["slow_piezo_cal"]=np.median(split_slow_piezo_scans[min(slow_piezo_speeds)].Slope)
            cal["slow_piezo_cal_all"]=split_slow_piezo_scans
        ref_cell_scan=None
        if ref_cell and len(self._bifi_freqs):
            self._check_device("ref_cell")
            try:
                if verbose:
                    print("Calibrating ref cell response")
                ref_cell_cal_freqs=np.linspace(self._bifi_freqs[:,1].min(),self._bifi_freqs[:,1].max(),12)[1:-1]
                ref_cell_scan=[]
                t0=time.time()
                if ref_cell_speeds is None:
                    ref_cell_speeds=[self._ref_cell_max_speed]
                ref_cell_speeds=sorted(ref_cell_speeds)
                for i,f in enumerate(ref_cell_speeds):
                    for s in slow_piezo_speeds:
                        self.tune_to(f,level="thinet")
                        self._lock_ref_cell()
                        slope,_=self._estimate_ref_cell_slope(speed=s)
                        ref_cell_scan.append((f,s,slope))
                    if verbose:
                        dt=time.time()-t0
                        tleft=(dt)/(i+1)*(len(ref_cell_cal_freqs)-i-1)
                        print("{:3d} / {:3d}   {:5.1f}mins left".format(i+1,len(ref_cell_cal_freqs),tleft/60))
                ref_cell_scan=pd.DataFrame(ref_cell_scan,columns=["Freq","Speed","Slope"])
                split_ref_cell_scans={s:t for s,t in ref_cell_scan.groupby("Speed")}
                self._ref_cell_cal=cal["ref_cell_cal"]=np.median(split_ref_cell_scans[min(ref_cell_speeds)].Slope)
                cal["ref_cell_cal_all"]=split_ref_cell_scans
            except self.laser.Error:
                pass
        if return_scans:
            return cal,(mot_scan,slow_piezo_scan,ref_cell_scan)
        return cal

    def _dfcmp(self, f1, f2, app):
        if app=="below":
            if f1>0 and f2<0:
                return True
            if f1<0 and f2>0:
                return False
        if app=="above":
            if f1<0 and f2>0:
                return True
            if f1>0 and f2<0:
                return False
        return abs(f1)>abs(f2)
    def _pass_plateau(self, motor, step, prec, target=None, fltw=3, approach="both", rng=None, after_steps=0):
        if target is None:
            target=self.get_frequency()
            cldf=0
        else:
            cldf=self.get_frequency()-target
        pdf=cldf
        flt=filters.RunningDecimationFilter(fltw,mode="median")
        while True:
            if not self._move_motor_by(motor,step,rng=rng):
                return
            df=self.get_frequency()-target
            fdf=flt.add(df)
            if fdf is not None:
                if abs(fdf-pdf)>prec:
                    if self._dfcmp(cldf,fdf,app=approach):
                        cldf=fdf
                    else:
                        if after_steps:
                            self._move_motor_by(motor,step*after_steps,rng=rng)
                        return
                pdf=fdf
    def _center_plateau(self, motor, step, prec, target=None, approach="both", rng=None):
        if target is None:
            target=self.get_frequency()
        # self._pass_plateau(motor,-step*5,prec,target=target,approach=approach,rng=rng)
        self._pass_plateau(motor,-step,prec,target=target,approach=approach,rng=rng)
        self._pass_plateau(motor,step,prec,target=target,approach=approach,rng=rng)
        p0=self._get_motor_position(motor)
        self._pass_plateau(motor,-step,prec,target=target,approach=approach,rng=rng)
        p1=self._get_motor_position(motor)
        self._move_motor(motor,(p0+p1)/2)
        return p0,p1
    def _split_plateaus(self, scan, prec, minw=2):
        p0,v0=0,scan[0]
        plats=[]
        for p,v in enumerate(scan):
            if abs(v-v0)>prec:
                if p-p0>=minw:
                    plats.append((p0,p))
                p0,v0=p,v
        if len(scan)-p0>=minw:
            plats.append((p0,len(scan)))
        return plats
    def _get_closest_plateau(self, scan, plats, target):
        dfs=[abs(np.mean(scan[s:e,3])-target) for s,e in plats]
        p=plats[np.argmin(dfs)]
        return scan[p[0]:p[1],:]
    _bifi_full_rng=(1E5,4E5)  # maximal bifi search range
    _bifi_search_step=(800,2,100)  # bifi "zoom-in" parameters ``(init, factor, final)``
    # start with ``init`` step size, and every time the desired frequency is reached, reduce it by ``factor``, until ``final`` (or smaller) step size is reached
    _bifi_pos_dir=1  # direction of bifi tuning corresponding to the increasing frequencies
    _bifi_plateau_freq_span=30E9  # maximal estimate of the frequency variation withing one bifi 'plateau' (frequency changes smaller than that are ignored during tuning)
    _bifi_freqs=np.zeros((0,2))
    def _align_bifi(self, target, approach="both"):
        if len(self._bifi_freqs):
            bifi_pos=self._bifi_freqs[abs(self._bifi_freqs[:,1]-target).argmin(),0]-500
            self._move_motor("bifi",bifi_pos)
        s0,sr,sm=self._bifi_search_step
        s=s0*(1 if target>self.get_frequency() else -1)*self._bifi_pos_dir
        while abs(s)>=sm:
            df=target-self.get_frequency()
            if np.sign(df)*self._bifi_pos_dir==np.sign(s):
                if not self._move_motor_by("bifi",s,rng=self._bifi_full_rng):
                    s=-s
            else:
                s=-s/sr
        s*=sr
        self._center_plateau("bifi",s,self._bifi_plateau_freq_span,target=target,approach=approach,rng=self._bifi_full_rng)
    def _refine_bifi(self, target):
        min_err=None,None
        for t in range(4):
            scan=self.scan_quick("thinet",*self._te_search_rng)
            plat_span=np.percentile(scan[:,3],5),np.percentile(scan[:,3],95)
            target_frac=(target-plat_span[0])/(plat_span[1]-plat_span[0])
            if abs(target_frac-0.5)>0.4:
                if min_err[0] is None or abs(target_frac-0.5)<min_err[0]:
                    min_err=abs(target_frac-0.5),self._get_motor_position("bifi")
                center_te_pos=scan[abs(scan[:,3]-np.median(scan[:,3])).argmin(),0]
                self._move_motor("thinet",center_te_pos)
                time.sleep(0.1)
                plat_dir=1 if target_frac>0.5 else -1
                self._pass_plateau("bifi",self._bifi_search_step[2]*plat_dir//2,self._bifi_plateau_freq_span,after_steps=2)
                if t>1:
                    self._center_plateau("bifi",self._bifi_search_step[2]//2,self._bifi_plateau_freq_span)
            else:
                return scan
        self._move_motor("bifi",min_err[1])
        return scan
    _te_search_rng=(2000,12000)  # initial thin etalon search range
    _te_full_rng=(1000,13000)  # maximal thin etalon tune range (used when zooming in on the target 'plateau' center)
    _te_plateau_freq_span=5E9  # maximal estimate of the frequency variation withing thin etalon 'plateau' (frequency changes smaller than that are ignored during tuning)
    _te_plateau_scan_steps=None  # number of steps over the full te range to search for thin etalon plateau (``None`` means do a quick scan)
    _te_plateau_step=50  # thin etalon motor step used to find the desired 'plateau'
    _te_center_step=20  # thin etalon motor step used for the final probing of the desired 'plateau' boundaries
    _te_lock_frac=0.3  # relative position within the 'plateau' to center the thin etalon lock (0.5 would be in the center, 0 is on the left edge, etc.)
    def _scan_te_plateaus(self):
        if self._te_plateau_scan_steps is None:
            return self.scan_quick("thinet",*self._te_search_rng)
        return self.scan_steps("thinet",self._te_search_rng[0],self._te_search_rng[1],abs(self._te_search_rng[1]-self._te_search_rng[0])//self._te_plateau_scan_steps)
    def _align_te(self, target, prescan=None):
        scan=self._scan_te_plateaus() if (prescan is None or self._te_plateau_scan_steps is not None) else prescan
        plats=self._split_plateaus(scan[:,3],self._te_plateau_freq_span,minw=3)
        if not plats:
            self._move_motor("thinet",np.mean(self._te_search_rng))
            return
        p=self._get_closest_plateau(scan,plats,target)
        self._move_motor("thinet",(p[0,0]+p[-1,0])/2)
        p0,p1=self._center_plateau("thinet",self._te_plateau_step,self._te_plateau_freq_span,target=target,rng=self._te_full_rng)
        scan=self.scan_steps("thinet",p0-self._te_center_step*3,p1+self._te_center_step*3,self._te_center_step)
        plats=self._split_plateaus(scan[:,3],self._te_plateau_freq_span,minw=3)
        if not plats:
            self._move_motor("thinet",np.mean([p0,p1]))
            return
        p=self._get_closest_plateau(scan,plats,target)
        minpos=p[:,2].argmin()
        side=-1 if minpos>len(p)//2 else 1
        etval=p[:,2].min()+(p[:,2].max()-p[:,2].min())*self._te_lock_frac
        pos=(p[0,0]+p[-1,0])/2
        self._move_motor("thinet",pos)
        ctl_par=self.laser.get_thinet_ctl_params()
        self.laser.set_thinet_ctl_params(setpoint=etval/np.median(p[:,1]),P=abs(ctl_par.P)*side,I=abs(ctl_par.I)*side)
        return scan
    
    def _setup_fine_tune_lock(self, device):
        if device=="slow_piezo":
            self._unlock_ref_cell()
        else:
            self._lock_ref_cell()
    def _lock_ref_cell(self):
        self._check_device("ref_cell")
        self.laser.set_scan_status("stop")
        self.laser.set_scan_params(device="none")
        self.laser.set_slowpiezo_ctl_status("run")
        self.laser.set_fastpiezo_ctl_status("run")
    def _unlock_ref_cell(self):
        self.laser.set_scan_status("stop")
        self.laser.set_scan_params(device="none")
        try:
            self.laser.set_fastpiezo_ctl_status("stop")
        except self.laser.Error:
            pass
        self.laser.set_slowpiezo_ctl_status("stop")
        try:
            self.laser.set_refcell_position(np.mean(self._ref_cell_rng))
        except self.laser.Error:
            pass
    def _get_fine_position(self, device):
        self._check_device(device)
        if device=="slow_piezo":
            return self.laser.get_slowpiezo_position()
        return self.laser.get_refcell_position()
    def _set_fine_position(self, device, position):
        self._check_device(device)
        if device=="slow_piezo":
            return self.laser.set_slowpiezo_position(position)
        return self.laser.set_refcell_position(position)
    def _move_cont_gen(self, device, position, speed):
        speed=abs(speed)
        scanpar=self.laser.get_scan_params()
        if scanpar[0]!=device:
            scanpar=("none",)+scanpar[1:]
        self._setup_fine_tune_lock(device)
        self.laser.set_scan_params(device="none")
        _,tune_rng,_=self._get_fine_tune_params(device)
        position=max(tune_rng[0],min(position,tune_rng[1]))
        start=self._get_fine_position(device)
        try:
            if abs(position-start)<1E-3:
                self.laser.set_scan_params(device="none")
                self._set_fine_position(device,position)
                return
            if position>start:
                self.laser.set_scan_params(device=device,mode=(False,False,True),lower_limit=tune_rng[0],upper_limit=position,rise_speed=speed,fall_speed=speed)
            else:
                self.laser.set_scan_params(device=device,mode=(True,True,False),lower_limit=position,upper_limit=tune_rng[1],rise_speed=speed,fall_speed=speed)
            self.laser.set_scan_status("run")
            while self.laser.get_scan_status()=="run":
                yield
        finally:
            self.laser.set_scan_status("stop")
            self.laser.set_scan_params(*scanpar)
            self._get_fine_position(device)
    def _move_cont(self, device, position, speed):
        for _ in self._move_cont_gen(device,position,speed):
            time.sleep(1E-3)

    _slow_piezo_rng=(0,0.7)  # total accessible slow piezo range
    _slow_piezo_max_speed=0.05  # maximal speed speed of slow piezo fine tuning (slow enough to avoid mode hopping, fast enough to be quick)
    _slow_piezo_cal=None  # slow piezo sensitivity (Hz/tuning value)
    _slow_piezo_cal_est=(0.2,7,0.2,10.)  # parameters for slow piezo sensitivity estimation ``(span, segments, delay, tseg_max)``;
    # to estimate the sensitivity, range of ``span`` size around tuning center is split into ``segments`` chunks, slow is estimated over each of them, and then median is returned
    def _estimate_slow_piezo_slope(self, speed=None):
        if speed is None:
            speed=self._slow_piezo_max_speed
        center=np.mean(self._slow_piezo_rng)
        span=min(self._slow_piezo_cal_est[0],speed*self._slow_piezo_cal_est[3])
        poss=center+np.linspace(-span/2,span/2,self._slow_piezo_cal_est[1]+1)
        freqs=[]
        self._move_cont("slow_piezo",poss[0],max(self._slow_piezo_max_speed,speed,0.2))
        for p in poss:
            self._move_cont("slow_piezo",p,speed)
            time.sleep(self._slow_piezo_cal_est[2])
            freqs.append(self.get_frequency())
        df=np.median(np.diff(freqs))
        return (df*self._slow_piezo_cal_est[1])/span,np.column_stack((poss,freqs))
    _ref_cell_rng=(0,0.7)  # total accessible reference cell range
    _ref_cell_max_speed=0.05  # maximal speed speed of ref cell fine tuning (slow enough to avoid mode hopping, fast enough to be quick)
    _ref_cell_cal=None  # reference cell sensitivity (Hz/tuning value)
    _ref_cell_cal_est=(0.2,7,0.2)  # parameters for reference cell sensitivity estimation ``(span, segments, delay)``;
    # to estimate the sensitivity, range of ``span`` size around tuning center is split into ``segments`` chunks, slow is estimated over each of them, and then median is returned
    def _estimate_ref_cell_slope(self, speed=None):
        if speed is None:
            speed=self._ref_cell_max_speed
        center=np.mean(self._ref_cell_rng)
        poss=center+np.linspace(-self._ref_cell_cal_est[0]/2,self._ref_cell_cal_est[0]/2,self._ref_cell_cal_est[1]+1)
        freqs=[]
        for p in poss:
            self._move_cont("ref_cell",p,speed)
            time.sleep(self._ref_cell_cal_est[2])
            freqs.append(self.get_frequency())
        df=np.median(np.diff(freqs))
        return (df*self._ref_cell_cal_est[1])/self._ref_cell_cal_est[0],freqs

    def unlock_all(self):
        """Unlock all relevant locks (slow piezo, fast piezo, piezo etalon, thin etalon)"""
        self._unlock_ref_cell()
        self.laser.set_slowpiezo_position(np.mean(self._slow_piezo_rng))
        self.laser.set_piezoet_ctl_status("stop")
        self.laser.set_piezoet_position(0)
        self.laser.set_thinet_ctl_status("stop")
        self.laser.thinet_clear_errors()
        self.laser.bifi_clear_errors()
    def set_fine_lock(self, device="slow_piezo"):
        """Set fine lock (slow and fast piezo) parameters for the given device (``"low_piezo"`` or ``"ref_cell"``)"""
        funcargparse.check_parameter_range(device,"device",["slow_piezo","ref_cell"])
        self._setup_fine_tune_lock(device)
    
    def _get_fine_tune_params(self, device):
        max_speed=self._slow_piezo_max_speed if device=="slow_piezo" else self._ref_cell_max_speed
        tune_rng=self._slow_piezo_rng if device=="slow_piezo" else self._ref_cell_rng
        cal=self._slow_piezo_cal if device=="slow_piezo" else self._ref_cell_cal
        return max_speed,tune_rng,cal
    def _set_fine_tune_params(self, device, max_speed=None, tune_rng=None, cal=None):
        if device=="slow_piezo":
            self._slow_piezo_max_speed=max_speed if max_speed is not None else self._slow_piezo_max_speed
            self._slow_piezo_rng=tune_rng if tune_rng is not None else self._slow_piezo_rng
            self._slow_piezo_cal=cal if cal is not None else self._slow_piezo_cal
        else:
            self._ref_cell_max_speed=max_speed if max_speed is not None else self._ref_cell_max_speed
            self._ref_cell_rng=tune_rng if tune_rng is not None else self._ref_cell_rng
            self._ref_cell_cal=cal if cal is not None else self._ref_cell_cal
    @contextlib.contextmanager
    def _override_fine_tune_params(self, device, max_speed=None, tune_rng=None, cal=None):
        par=self._get_fine_tune_params(device)
        try:
            self._set_fine_tune_params(device,max_speed=max_speed,tune_rng=tune_rng,cal=cal)
            yield
        finally:
            self._set_fine_tune_params(device,*par)

    _fine_tune_step_par=(0.01,2,0.001,0.1)  # slow piezo "zoom-in" parameters ``(init, factor, final, delay)``
    # start with ``init`` position step, and every time the desired frequency is reached, reduce it by ``factor`` and flip the direction,
    # until ``final`` (or smaller) position step is reached; when the step is within a factor of 10 from ``final``, start applying ``delay`` after every step
    _fine_tune_slope_par=(10,0.05E9,0.2)
    _fine_tune_dir=1  # direction of slow piezo tuning corresponding to the increasing frequencies
    def _fine_tune_step(self, target, device="slow_piezo"):
        max_speed,tune_rng,_=self._get_fine_tune_params(device)
        pos=self._get_fine_position(device)
        df=self.get_frequency()-target
        step=self._fine_tune_step_par[0]*(1 if df<0 else -1)*self._fine_tune_dir
        while abs(step)>self._fine_tune_step_par[2]:
            if pos+step<tune_rng[0]+0.05 or pos+step>tune_rng[1]-0.05:
                break
            for _ in self._move_cont_gen(device,pos+step,max_speed):
                yield
            pos+=step
            ndf=self.get_frequency()-target
            if abs(ndf)>abs(df):
                step=-step/self._fine_tune_step_par[1]
            df=ndf
            if abs(step)<self._fine_tune_step_par[2]*10:
                time.sleep(self._fine_tune_step_par[3])
            yield
    def _fine_tune_slope(self, target, device="slow_piezo", tolerance=None):
        max_speed,tune_rng,cal=self._get_fine_tune_params(device)
        if cal is None:
            raise ValueError("{} calibration is not specified".format(device))
        bound_hit=[False,False]
        dfs=[]
        tolerance=self._fine_tune_slope_par[1] if tolerance is None else tolerance
        for i in range(self._fine_tune_slope_par[0]):
            pos=self._get_fine_position(device)
            if pos<tune_rng[0]+0.07:
                bound_hit[0]=True
            if pos>tune_rng[1]-0.07:
                bound_hit[1]=True
            if all(bound_hit):
                return
            df=self.get_frequency()-target
            dfs.append(abs(df))
            if len(dfs)>=4 and np.min(dfs[-2:])>np.min(dfs[-4:-2])*0.8:
                return
            if abs(df)<tolerance and i>2:
                return
            step=-df/cal
            newpos=max(tune_rng[0]+0.05,min(pos+step,tune_rng[1]-0.05))
            for _ in self._move_cont_gen(device,newpos,max_speed):
                yield
            time.sleep(self._fine_tune_slope_par[2])
            yield
    def fine_tune_to_gen(self, target, device="slow_piezo", method="auto", tolerance=None):
        """
        Same as :meth:`fine_tune_to`, but made as a generator which yields occasionally.
        
        Can be used to run this scan in parallel with some other task, or to be able to interrupt it in the middle.
        """
        funcargparse.check_parameter_range(method,"method",["auto","step","cal"])
        funcargparse.check_parameter_range(device,"device",["slow_piezo","ref_cell"])
        _,_,cal=self._get_fine_tune_params(device)
        if method=="auto":
            method="cal" if cal is not None else "step"
        tune_gen=self._fine_tune_step(target,device=device) if method=="step" else self._fine_tune_slope(target,device=device,tolerance=tolerance)
        for _ in tune_gen:
            yield
    def fine_tune_to(self, target, device="slow_piezo", method="auto", tolerance=None):
        """
        Fine tune the laser to the given target frequency using only fine tuning.
        
        `device` specifies the device used for fine tuning: either ``"slow_piezo"``, or ``"ref_cell"``.
        `method` can be ``"step"`` for step-based binary search method, or ``"cal"`` for slope-based method using the fine tuning calibration (frequency detuning per element position shift).
        (generally faster, but requires a known calibration). If ``method=="auto"``, use ``"cal"`` when the calibration is available and ``"step"`` otherwise.
        `tolerance` gives the final frequency tolerance for the ``"cal"`` tuning method; if ``None``, use the standard value (50MHz by default).
        """
        for _ in self.fine_tune_to_gen(target,device=device,method=method,tolerance=tolerance):
            time.sleep(1E-3)
    
    _tune_local_thinet_range=100E9
    _tune_local_fine_range=25E9
    _tune_local_final_tolerance=1E9
    def tune_to_gen(self, target, level="full", fine_device="slow_piezo", tolerance=None, local_level="none"):
        """
        Same as :meth:`tune_to`, but made as a generator which yields occasionally.
        
        Can be used to run this scan in parallel with some other task, or to be able to interrupt it in the middle.
        """
        funcargparse.check_parameter_range(level,"level",["bifi","thinet","slow_piezo","ref_cell","full"])
        funcargparse.check_parameter_range(fine_device,"fine_device",["slow_piezo","ref_cell"])
        funcargparse.check_parameter_range(local_level,"local_level",["none","thinet","fine"])
        if level=="full":
            level=fine_device
        while True:
            self.unlock_all()
            te_prescan=None
            if local_level=="none" or abs(self.get_frequency()-target)>self._tune_local_thinet_range:
                local_level="none"
                self._move_motor("thinet",np.mean(self._te_search_rng))
                yield
                self._align_bifi(target)
                yield
                te_prescan=self._refine_bifi(target)
                yield
            if level=="bifi":
                self._move_motor("thinet",np.mean(self._te_search_rng))
                return
            if local_level in ["none","thinet"] or abs(self.get_frequency()-target)>self._tune_local_fine_range:
                local_level="thinet"
                self._align_te(target,prescan=te_prescan)
                yield
            self.laser.set_thinet_ctl_status("run")
            self.laser.set_piezoet_ctl_status("run")
            oversamp=self.laser.get_piezoet_drive_params().oversamp
            self.laser.set_piezoet_drive_params(oversamp=oversamp+1 if oversamp<32 else oversamp-1)
            self.laser.set_piezoet_drive_params(oversamp=oversamp)  # cycling oversampling to prevent a certain rare bug where the piezo etalon lock turns off
            if level=="thinet":
                return
            if level=="ref_cell":
                self._lock_ref_cell()
            for _ in self.fine_tune_to_gen(target,device=level,tolerance=tolerance):
                yield
            if abs(self.get_frequency()-target)<max(self._tune_local_final_tolerance,tolerance*2 if tolerance is not None else 0):
                return
            local_level={"none":"none","thinet":"none","fine":"thinet"}[local_level]
    def tune_to(self, target, level="full", fine_device="slow_piezo", tolerance=None, local_level="none"):
        """
        Tune the laser to the given frequency (in Hz) using multiple elements (bifi, thin etalon, piezo etalon, slow piezo / ref cell).
        
        `level` can be ``"bifi"`` (only tune the bifi motor), ``"thinet"`` (tune bifi motor and thin etalon),
        or ``"full"`` (full tuning using all elements).
        `fine_device` specifies the device used for fine tuning: either ``"slow_piezo"``, or ``"ref_cell"``.
        `tolerance` gives the final fine tuning frequency tolerance; if ``None``, use the standard value (50MHz by default).
        `local_level` defines the level on which to start adjustment; can be ``"fine"`` (start with the slow piezo or the ref cell, if the laser is within their tuning range),
        ``"thinet"`` (start with the thin etalon), or ``"none"`` (start with the bifi; default). If using just the finer control does not work, progressively move to the coarser ones.
        """
        for _ in self.tune_to_gen(target,level=level,fine_device=fine_device,tolerance=tolerance,local_level=local_level):
            time.sleep(1E-3)

    def fine_sweep_start_gen(self, span, up_speed, down_speed=None, device="slow_piezo", kind="cont_up", current_pos=0.5):
        """
        Same as :meth:`fine_sweep_start`, but made as a generator which yields occasionally.
        
        Can be used to run this scan in parallel with some other task, or to be able to interrupt it in the middle.
        """
        funcargparse.check_parameter_range(kind,"kind",["cont_up","cont_down","single_up","single_down"])
        funcargparse.check_parameter_range(device,"device",["slow_piezo","ref_cell"])
        span=self._to_int_units(span,device)
        max_speed,tune_rng,_=self._get_fine_tune_params(device)
        up_speed=min(self._to_int_units(abs(up_speed),device),max_speed)
        down_speed=up_speed if down_speed is None else min(self._to_int_units(abs(down_speed),device),max_speed)
        self._setup_fine_tune_lock(device)
        p=self._get_fine_position(device)
        self._fine_scan_start=device,p
        scan_rng=max(tune_rng[0],p-span*current_pos),min(tune_rng[1],p-span*current_pos+span)
        if kind in ["cont_up","single_up"]:
            start=scan_rng[0]
            mode=(False,False,kind=="single_up")
        else:
            start=scan_rng[1]
            mode=(True,kind=="single_down",False)
        for _ in self._move_cont_gen(device,start,max_speed):
            yield
        self.laser.set_scan_params(device=device,mode=mode,lower_limit=scan_rng[0],upper_limit=scan_rng[1],rise_speed=up_speed,fall_speed=down_speed)
        self.laser.set_scan_status("run")
        yield scan_rng,(up_speed,down_speed)
    def fine_sweep_start(self, span, up_speed, down_speed=None, device="slow_piezo", kind="cont_up", current_pos=0.5):
        """
        Start a fine sweep using the slow piezo or the ref cell.

        `span` is a sweep span, `up_speed` and `down_speed` are the corresponding speeds (if `down_speed` is ``None``, use the same as `up_speed`),
        `device` is the scan device (``"slow_piezo"`` or ``"ref_cell"``),
        `kind` is the sweep kind (``"cont_up"``, ``"cont_down"``, ``"single_up"``, or ``"single_down"``),
        and `current_pos` is the relative position of the current position withing the sweep range (0 means that it's the lowest position of the sweep,
        1 means it's the highest, 0.5 means that it's in the center).
        """
        scan_par=None
        for scan_par in self.fine_sweep_start_gen(span,up_speed,down_speed=down_speed,device=device,kind=kind,current_pos=current_pos):
            time.sleep(1E-3)
        return scan_par
    def fine_sweep_stop(self, return_to_start=True, start_point=None):
        """
        Stop currently running fast sweep.

        If ``return_to_start==True``, return to the original start tuning position after the sweeps is stopped;
        otherwise, stay at the current position.
        """
        self.laser.set_scan_status("stop")
        if start_point is None:
            start_point=self._fine_scan_start[1] if self._fine_scan_start is not None else None
        if return_to_start and start_point is not None:
            device=self.laser.get_scan_params()[0]
            if device=="none" and self._fine_scan_start is not None:
                device=self._fine_scan_start[0]
            self._move_cont(device,start_point,self._get_fine_tune_params(device)[0])
        self._fine_scan_start=None
    
    def scan_coarse_gen(self, bifi_rng, te_rng):
        """
        Perform a 2D grid scan changing positions of both birefringent filter and thin etalon motors.

        `bifi_rng` and `te_rng` are both 3-tuples ``(start, stop, step)`` specifying the scan ranges.
        
        Yields a tuple ``((bifi_idx, bifi_npos), (te_idx, te_npos))``,
        where ``bifi_idx`` and ``te_idx`` are the indices of the current birefringent filter and thin etalon motor positions,
        and ``bifi_npos`` and ``te_npos`` are the corresponding total numbers of positions.
        """
        self.unlock_all()
        if (bifi_rng[1]-bifi_rng[0])*bifi_rng[2]<0:
            bifi_rng=bifi_rng[0],bifi_rng[1],-bifi_rng[2]
        if (te_rng[1]-te_rng[0])*te_rng[2]<0:
            te_rng=te_rng[0],te_rng[1],-te_rng[2]
        bifi_position=np.arange(*bifi_rng)
        te_position=np.arange(*te_rng)
        for i,bfp in enumerate(bifi_position):
            self._move_motor("bifi",bfp)
            for j,tep in enumerate(te_position):
                self._move_motor("thinet",tep)
                yield (i,len(bifi_position)),(j,len(te_position))
    
    _default_stitch_tune_precision=5E9
    _default_stitch_tune_maxreps=2
    def stitched_scan_gen(self, full_rng, single_span, speed, device="slow_piezo", overlap=0.1, freq_step=None, segment_end_timeout=None):
        """
        Same as :meth:`stitched_scan`, but made as a generator which yields occasionally.
        
        Can be used to run this scan in parallel with some other task, or to be able to interrupt it in the middle.
        Yields ``True`` whenever the main scanning region is passing, and ``False`` during the stitching intervals.
        """
        f=full_rng[0]
        scandir=1 if full_rng[1]>full_rng[0] else -1
        single_span=abs(single_span)
        freq_step=abs(freq_step) if freq_step is not None else None
        stitch_tune_precision=single_span*.2 if self._tune_units=="freq" else self._default_stitch_tune_precision
        fail_step=freq_step*0.5 if freq_step is not None else (single_span*0.5 if self._tune_units=="freq" else self._default_stitch_tune_precision*2)
        expected_span=single_span if self._tune_units=="freq" else None
        single_span=self._to_int_units(single_span,device)
        speed=self._to_int_units(speed,device)
        local_level="none"
        rep=0
        ctd=general.Countdown(segment_end_timeout)
        furtherst_freq=None
        while (full_rng[1]-f)*scandir>0:
            with self._override_fine_tune_params(device,max_speed=max(self._get_fine_tune_params(device)[0],speed)):
                for _ in self.tune_to_gen(f,fine_device=device,local_level=local_level):
                    yield False
            f0=self.get_frequency()
            scan_freqs=[]
            if abs(f0-f)<stitch_tune_precision:
                p=self._get_fine_position(device)
                yield False
                ctd.stop()
                for _ in self._move_cont_gen(device,p+single_span*scandir,speed):
                    f=self.get_frequency()
                    scan_freqs.append(f)
                    if (f-full_rng[1])*scandir>0:
                        if not ctd.running():
                            ctd.reset()
                        elif ctd.passed():
                            break
                    else:
                        ctd.stop()
                    yield True
                yield False
                f1=self.get_frequency()
            else:
                f1=None
            span_success=f1 is not None and (f1-f0)*scandir>0 and (expected_span is None or ((f1-f0)*scandir>expected_span/4 and (f1-f0)*scandir<expected_span*2) or ctd.passed())
            local_level="fine"
            if span_success and len(scan_freqs)>5:
                df=np.diff(scan_freqs[:-1])
                med_step=np.abs(np.median(df))
                valid_step=np.abs(df)<max(np.abs(med_step)*3,1E9)
                if not valid_step.all():
                    f1=scan_freqs[valid_step.argmin()]
                    if abs(f1-f0)<fail_step/4:
                        span_success=False
                    if valid_step.argmin()<len(valid_step)/2:
                        local_level="none"
            if not span_success:
                local_level="none"
                if rep+1<self._default_stitch_tune_maxreps:
                    rep+=1
                    continue
            if freq_step is None:
                if span_success:
                    f=f1-(f1-f0)*overlap
                else:
                    f=f+fail_step*scandir
                if furtherst_freq is not None:
                    f=max(furtherst_freq,f) if scandir>0 else min(furtherst_freq,f)
            else:
                f+=(freq_step if span_success else fail_step)*scandir
            if furtherst_freq is None:
                furtherst_freq=f
            else:
                furtherst_freq=max(furtherst_freq,f-fail_step/4) if scandir>0 else min(furtherst_freq,f+fail_step/4)
            rep=0
    def stitched_scan(self, full_rng, single_span, speed, device="slow_piezo", overlap=0.1, freq_step=None, segment_end_timeout=None):
        """
        Perform a stitched laser scan.

        Args:
            full_rng: 2-tuple ``(start, stop)`` with the full frequency scan range.
            single_span: magnitude of a single continuous scan segment given in the slow piezo scan units (between 0 and 1)
            speed: single segment scan speed
            device: the scan device (``"slow_piezo"`` or ``"ref_cell"``)
            overlap: overlap of consecutive segments, as a fraction of `single_span`
            freq_step: if ``None``, the start of the next segment is calculated based on the end of the previous segment and `overlap`;
                otherwise, it specifies a fixed frequency step between segments.
        """
        for _ in self.stitched_scan_gen(full_rng,single_span,speed,device=device,overlap=overlap,freq_step=freq_step,segment_end_timeout=segment_end_timeout):
            time.sleep(1E-3)