from ...core.dataproc import filters
from ...core.utils import general, funcargparse

import numpy as np
import time


class MatisseTuner:
    """
    Matisse tuner.

    Helps to coordinate with an external wavemeter to perform more complicated tasks: motors calibration, fine frequency tuning, and stitching scans.

    Args:
        laser: opened Matisse laser object
        wavemeter: opened wavemeter object (currently only HighFinesse wavemeters are supported)
    """
    def __init__(self, laser, wavemeter):
        self.laser=laser
        self.wavemeter=wavemeter
    def get_frequency(self, timeout=1.):
        """
        Get current frequency reading.

        The only method relying on the wavemeter. Can be extended or overloaded to support different wavemeters.
        """
        countdown=general.Countdown(timeout)
        while True:
            f=self.wavemeter.get_frequency(error_on_invalid=False)
            if isinstance(f,float):
                return f
            if countdown.passed():
                raise RuntimeError
    
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
    def _pass_plateau(self, motor, step, target, prec, fltw=3, approach="both", rng=None):
        cldf=self.get_frequency()-target
        pdf=cldf
        self._plateau_log.append((self._get_motor_position(motor),self.get_frequency(),cldf,cldf))
        flt=filters.RunningDecimationFilter(fltw,mode="median")
        while True:
            if not self._move_motor_by(motor,step,rng=rng):
                return
            df=self.get_frequency()-target
            self._plateau_log.append((self._get_motor_position(motor),self.get_frequency(),df,cldf))
            fdf=flt.add(df)
            if fdf is not None:
                if abs(fdf-pdf)>prec:
                    if self._dfcmp(cldf,fdf,app=approach):
                        cldf=fdf
                    else:
                        return
                pdf=fdf
    def _center_plateau(self, motor, step, target, prec, approach="both", rng=None):
        self._plateau_log=[]
        self._pass_plateau(motor,-step*5,target,prec,approach=approach,rng=rng)
        self._pass_plateau(motor,step,target,prec,approach=approach,rng=rng)
        p0=self._get_motor_position(motor)
        self._pass_plateau(motor,-step,target,prec,approach=approach,rng=rng)
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
    _bifi_search_step=(1800,3,200)  # bifi "zoom-in" parameters ``(init, factor, final)``
    # start with ``init`` step size, and every time the desired frequency is reached, reduce it by ``factor``, until ``final`` (or smaller) step size is reached
    _bifi_pos_dir=1  # direction of bifi tuning corresponding to the increasing frequencies
    _bifi_plateau_span=50E9  # maximal estimate of the frequency variation withing one bifi 'plateau' (frequency changes smaller than that are ignored during tuning)
    def _align_bifi(self, target, approach="both"):
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
        self._center_plateau("bifi",s,target,self._bifi_plateau_span,approach=approach,rng=self._bifi_full_rng)
    _te_search_rng=(2000,12000)  # initial thin etalon search range
    _te_full_rng=(1000,13000)  # maximal thin etalon tune range (used when zooming in on the target 'plateau' center)
    _te_plateau_span=5E9  # maximal estimate of the frequency variation withing thin etalon 'plateau' (frequency changes smaller than that are ignored during tuning)
    _te_plateau_step=50  # thin etalon motor step used to find the desired 'plateau'
    _te_center_step=20  # thin etalon motor step used for the final probing of the desired 'plateau' boundaries
    _te_lock_frac=0.3  # relative position within the 'plateau' to center the thin etalon lock (0.5 would be in the center, 0 is on the left edge, etc.)
    def _align_te(self, target):
        scan=self.scan_quick("thinet",*self._te_search_rng)
        plats=self._split_plateaus(scan[:,3],self._te_plateau_span,minw=3)
        if not plats:
            self._move_motor("thinet",np.mean(self._te_search_rng))
            return
        p=self._get_closest_plateau(scan,plats,target)
        self._move_motor("thinet",(p[0,0]+p[-1,0])/2)
        p0,p1=self._center_plateau("thinet",self._te_plateau_step,target,self._te_plateau_span,rng=self._te_full_rng)
        scan=self.scan_steps("thinet",p0-self._te_center_step*3,p1+self._te_center_step*3,self._te_center_step)
        plats=self._split_plateaus(scan[:,3],self._te_plateau_span,minw=3)
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
    
    def _move_cont(self, device, position, speed):
        scanpar=self.laser.get_scan_params()
        self.laser.set_scan_status("stop")
        assert device=="slow_piezo"
        start=self.laser.get_slowpiezo_position()
        if position>start:
            self.laser.set_scan_params(device=device,mode=(False,True,True),lower_limit=0,upper_limit=position,rise_speed=speed)
        else:
            self.laser.set_scan_params(device=device,mode=(True,True,True),lower_limit=position,upper_limit=1,fall_speed=speed)
        self.laser.set_scan_status("run")
        self.laser.wait_scan()
        self.laser.set_scan_params(*scanpar)

    def unlock_all(self):
        """Unlock all relevant locks (slow piezo, fast piezo, piezo etalon, thin etalon)"""
        self.laser.set_scan_status("stop")
        self.laser.set_scan_params(device="none")
        self.laser.set_slowpiezo_ctl_status("stop")
        self.laser.set_slowpiezo_position(.35)
        self.laser.set_piezoet_ctl_status("stop")
        self.laser.set_piezoet_position(0)
        self.laser.set_thinet_ctl_status("stop")
        self.laser.thinet_clear_errors()
        self.laser.bifi_clear_errors()
    
    _fine_tune_step=(0.01,2,0.001)  # slow piezo "zoom-in" parameters ``(init, factor, final)``
    # start with ``init`` position step, and every time the desired frequency is reached, reduce it by ``factor`` and flip the direction,
    # until ``final`` (or smaller) position step is reached
    _fine_tune_speed=0.1  # speed of fine tuning (slow enough to avoid mode hopping, fast enough to be quick)
    _fine_tune_dir=1  # direction of slow piezo tuning corresponding to the increasing frequencies
    def slow_piezo_tune_to(self, target):
        """Fine tune the laser to the given target frequency using only slow piezo tuning"""
        pos=self.laser.get_slowpiezo_position()
        df=self.get_frequency()-target
        step=self._fine_tune_step[0]*(1 if df<0 else -1)*self._fine_tune_dir
        while abs(step)>self._fine_tune_step[2]:
            if pos+step<0.05 or pos+step>0.65:
                break
            self._move_cont("slow_piezo",pos+step,self._fine_tune_speed)
            pos+=step
            ndf=self.get_frequency()-target
            if abs(ndf)>abs(df):
                step=-step/self._fine_tune_step[1]
            df=ndf
    
    def tune_to(self, target):
        """Tune the laser to the given frequency using all elements (bifi, thin etalon, piezo etalon, slow piezo)"""
        self.unlock_all()
        self._move_motor("thinet",np.mean(self._te_search_rng))
        self._align_bifi(target)
        self._align_te(target)
        self.laser.set_thinet_ctl_status("run")
        self.laser.set_piezoet_ctl_status("run")
        self.slow_piezo_tune_to(target)

    
    def stitched_scan(self, full_rng, single_span, speed, overlap=0.1, freq_step=None):
        """
        Perform a stitched laser scan.

        Args:
            full_rng: 2-tuple ``(start, stop)`` with the full frequency scan range.
            single_span: magnitude of a single continuous scan segment given in the slow piezo scan units (between 0 and 1)
            speed: single segment scan speed
            overlap: overlap of consecutive segments, as a fraction of `single_span`
            freq_step: if ``None``, the start of the next segment is calculated based on the end of the previous segment and `overlap`;
                otherwise, it specifies a fixed frequency step between segments.
        """
        f=full_rng[0]
        while f<full_rng[1]:
            self.tune_to(f)
            f0=self.get_frequency()
            p=self.laser.get_slowpiezo_position()
            self._move_cont("slow_piezo",min(p+single_span,0.7),speed)
            f1=self.get_frequency()
            if freq_step is None:
                f=f1-(f1-f0)*overlap
            else:
                f+=freq_step