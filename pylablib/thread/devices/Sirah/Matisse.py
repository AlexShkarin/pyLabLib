from ... import device_thread
from ....devices.Sirah import tuner, FrequencyReadSirahError
from ....core.utils import funcargparse


class SirahMatisseThread(device_thread.DeviceThread):
    """
    Sirah Matisse laser control.

    Device args:
        - ``conn``: device connection (usually, a VISA connection address)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``diode_power``: current laser diode power
        - ``thinet_power``: current thin etalon reflection power
        - ``bifi_position``: position of the BiFi (in steps)
        - ``thinet_position``: position of the thin etalon (in steps)
        - ``thinet_locked``: indicates whether thin etalon lock is active
        - ``piezoet_position``: position of the piezo etalon (normalized)
        - ``piezoet_locked``: indicates whether piezo etalon lock is active
        - ``slowpiezo_position``: position of the slow piezo (normalized)
        - ``slowpiezo_locked``: indicates whether slow piezo lock is active
        - ``fastpiezo_position``: position of the fast piezo (normalized)
        - ``refcell_position``: position of the reference cell (normalized)
        - ``fastpiezo_locked``: indicates whether fast piezo lock to the reference cell is active and successful
        - ``scan_position``: position of the current scanned device (normalized)
        - ``scanning``: indicates whether scanning is in progress

    Commands:
        - ``bifi_move_to``: move the BiFi
        - ``bifi_stop``: stop the BiFi motion 
        - ``thinet_move_to``: move the thin etalon
        - ``thinet_stop``: stop the thin etalon motion
        - ``lock_thinet``: lock the thin etalon
        - ``set_piezoet_position``: set the piezo etalon position
        - ``lock_piezoet``: lock the piezo etalon
        - ``set_slowpiezo_position``: set the slow piezo position
        - ``lock_slowpiezo``: lock the slow piezo
        - ``set_fastpiezo_position``: set the fast piezo position
        - ``lock_fastpiezo``: lock the fast piezo
        - ``set_refcell_position``: set the reference cell position
        - ``set_scan_params``: set the scan parameters (device, direction, limit, speed)
        - ``start_scan``: start or stop the scan
        - ``set_scan_position``: directly set the scan position
    """
    _device_class=""
    def connect_device(self):
        with self.using_devclass("Sirah.SirahMatisse",host=self.remote) as cls:
            self.device=cls(addr=self.conn)  # pylint: disable=not-callable
            self.device.get_diode_power()
    def setup_task(self, conn, remote=None):  # pylint: disable=arguments-differ
        self.conn=conn
        self.remote=remote
        self._fast_update_parameters=set()
        self.add_job("update_measurements",self.update_measurements,.2)
        self.add_job("update_measurements_fast",self.update_measurements_fast,.02)
        self.add_command("change_fast_update_parameters")
        self.add_device_command("bifi_move_to")
        self.add_device_command("bifi_stop")
        self.add_device_command("thinet_move_to")
        self.add_device_command("thinet_stop")
        self.add_command("lock_thinet")
        self.add_device_command("set_piezoet_position")
        self.add_command("lock_piezoet")
        self.add_device_command("set_slowpiezo_position")
        self.add_command("lock_slowpiezo")
        self.add_device_command("set_fastpiezo_position")
        self.add_command("lock_fastpiezo")
        self.add_device_command("set_refcell_position")
        self.add_device_command("set_scan_params")
        self.add_command("start_scan")
        self.add_device_command("set_scan_position")
        self.update_parameters()

    def lock_thinet(self, enable=True):
        """Enable or disable thin etalon lock"""
        if self.open():
            self.device.set_thinet_ctl_status("run" if enable else "stop")
            self.update_parameters()
    def lock_piezoet(self, enable=True):
        """Enable or disable piezo etalon lock"""
        if self.open():
            self.device.set_piezoet_ctl_status("run" if enable else "stop")
            self.update_parameters()
    def lock_slowpiezo(self, enable=True):
        """Enable or disable slow piezo lock"""
        if self.open():
            self.device.set_slowpiezo_ctl_status("run" if enable else "stop")
            self.update_parameters()
    def lock_fastpiezo(self, enable=True):
        """Enable or disable fast piezo lock"""
        if self.open():
            self.device.set_fastpiezo_ctl_status("run" if enable else "stop")
            self.update_parameters()
    def start_scan(self, enable=True):
        """Start or stop the scan"""
        if self.open():
            self.device.set_scan_status("run" if enable else "stop")
            self.update_parameters()
    def change_fast_update_parameters(self, add=None, remove=None):
        """Change the list of parameters which are updated at a higher rate"""
        self._fast_update_parameters=(self._fast_update_parameters|set(add or []))-set(remove or [])
    _status_params={"thinet_locked":"thinet_ctl_status","piezoet_locked":"piezoet_ctl_status","slowpiezo_locked":"slowpiezo_ctl_status","scanning":"scan_status"}
    def update_measurements_fast(self):
        if self.open():
            for n in self._fast_update_parameters:
                try:
                    if n in self._status_params:
                        self.v[n]=self.device.dv[self._status_params[n]]=="run"
                    else:
                        self.v[n]=self.device.dv[n]
                except self.DeviceError:  # pylint: disable=catching-non-exception
                    pass
    def update_measurements(self):
        power_params=["diode_power","thinet_power"]
        position_params=["bifi_position","thinet_position","piezoet_position",
                    "slowpiezo_position","fastpiezo_position","scan_position","refcell_position"]
        locked_params=["fastpiezo_locked"]
        param_defaults={p:0 for p in power_params+position_params}
        param_defaults.update({p:False for p in locked_params})
        param_defaults.update({p:False for p in self._status_params})
        if self.open():
            for n,v in param_defaults.items():
                try:
                    if n in self._status_params:
                        self.v[n]=self.device.dv[self._status_params[n]]=="run"
                    else:
                        self.v[n]=self.device.dv[n]
                except self.DeviceError:  # pylint: disable=catching-non-exception
                    self.v[n]=v
        else:
            for n,v in param_defaults.items():
                self.v[n]=v






class SirahMatisseTunerThread(SirahMatisseThread):
    """
    Sirah Matisse laser control, which includes tuner capabilities (wavemeter-based feedback).

    Has all the same variable and commands as the standard Matisse thread, but adds several more commands.

    Device args:
        - ``conn``: device connection (usually, a VISA connection address)
        - ``wmversion``: high-finesse wavemeter version
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect
        - ``wmremote``: same as ``remote`` for the wavemeter
        - ``calibration``: calibration data (either the calibration dictionary, or path to the calibration file)

    Commands:
        - ``tune_to_start``: start fine tuning to the given frequency
        - ``tune_to_stop``: stop fine tuning
        - ``fine_scan_start``: start fine scan with the given parameters
        - ``fine_scan_stop``: stop fine scan
        - ``fine_scan_adjust``: adjust fine scan parameters (center and range) during the scan
        - ``coarse_scan_start``: start coarse scan with the given ranges for the birefringent filter and the thin etalon motor positions
        - ``coarse_scan_stop``: stop coarse scan
        - ``stitched_scan_start``: start stitched scan with the given frequency range
        - ``stitched_scan_stop``: stop stitched scan
        - ``stop_tuning``: stop all tuning operations
    """
    _device_class=""
    def connect_device(self):
        super().connect_device()
        with self.using_devclass("HighFinesse.WLM",host=self.wmremote) as cls:
            self.wavemeter=cls(version=self.wmversion)  # pylint: disable=not-callable
            self.wavemeter.get_frequency(error_on_invalid=False)
        self.tuner=tuner.MatisseTuner(self.device,self.wavemeter,calibration=self.calibration)
        self.tuner.set_tune_units("freq")
    def close_device(self):
        self.stop_tuning()
        return super().close_device()
    def setup_task(self, conn, wmversion, remote=None, wmremote="auto", calibration=None):  # pylint: disable=arguments-differ, arguments-renamed
        self.wmversion=wmversion
        self.wmremote=wmremote if wmremote!="auto" else remote
        self.calibration=calibration
        self._lock_frequency=None
        self._fine_device="slow_piezo"
        super().setup_task(conn=conn,remote=remote)
        self.v["stitched_scan/stitching"]=0
        self.v["tuning/locking"]=False
        self.v["fine_tune_device"]=self._fine_device
        self.v["fine_scan/device_range_curr"]=self.v["fine_scan/device_range_start"]=None
        self.v["fine_scan/device_rate_curr"]=None
        self.update_progress(0)
        self.add_command("set_fine_tune_device")
        self.add_batch_job("tune_to",self.tune_to_loop,self.tune_to_finalize)
        self.add_command("tune_to_start")
        self.add_command("tune_to_stop")
        self.add_batch_job("lock_frequency",self.lock_frequency_loop,self.lock_frequency_finalize)
        self.add_command("lock_frequency_start")
        self.add_command("lock_frequency_stop")
        self.add_command("change_lock_frequency")
        self.add_batch_job("fine_scan",self.fine_scan_loop,self.fine_scan_finalize)
        self.add_command("fine_scan_start")
        self.add_command("fine_scan_stop")
        self.add_command("fine_scan_adjust",limit_queue=3,on_full_queue="skip_oldest")
        self.add_batch_job("stitched_scan",self.stitched_scan_loop,self.stitched_scan_finalize)
        self.add_command("coarse_scan_start")
        self.add_command("coarse_scan_stop")
        self.add_batch_job("coarse_scan",self.coarse_scan_loop,self.coarse_scan_finalize)
        self.add_command("stitched_scan_start")
        self.add_command("stitched_scan_stop")
        self.add_command("stop_tuning")
        self.update_scan_status("idle")
        self.update_operation_status("idle")
    
    def finalize_task(self):
        if self.device is not None:
            self.stop_tuning()
        super().finalize_task()
    def update_progress(self, progress):
        """Update current progress"""
        self.v["progress"]=progress
    _scan_status_text={"idle":"Idle","setup":"Setup","running":"In progress"}
    def update_scan_status(self, status):
        """Update scan status (``"status/scan"``)"""
        self.update_status("scan",status,self._scan_status_text[status])
    _operation_status_text={"idle":"Idle","wavemeter_connection":"Changing wavemeter connection",
            "stitched_scan":"Stitched scan","fine_scan":"Fine scan","coarse_scan":"Coarse scan","fine_tuning":"Fine tuning","frequency_locking":"Frequency locking"}
    def update_operation_status(self, status):
        """Update operation status (``"status/operation"``)"""
        curr_status=self.get_variable("status/operation")
        text=self._operation_status_text[status]
        self.update_status("operation",status,text=text)
        return curr_status
    def update_measurements(self):
        if self.open():
            try:
                self.v["last_read_frequency"]=self.tuner.get_last_read_frequency(max_delay=0.5)
            except FrequencyReadSirahError:
                self.v["last_read_frequency"]=0
        else:
            self.v["last_read_frequency"]=0
        return super().update_measurements()
    
    def set_fine_tune_device(self, device):
        """Set device used for fine tuning (``"low_piezo"`` or ``"ref_cell"``)"""
        funcargparse.check_parameter_range(device,"device",["slow_piezo","ref_cell"])
        if self._fine_device==device:
            return
        self.stop_tuning()
        self.v["fine_tune_device"]=self._fine_device=device
    def _tune_to(self, frequency, level="full", fine_threshold=3E9, final_tolerance=None, freq_avg_time=0):
        try:
            if level=="full" and abs(self.tuner.get_frequency()-frequency)<fine_threshold:
                try:
                    self.tuner.set_frequency_average_time(freq_avg_time)
                    self.tuner.set_fine_lock(device=self._fine_device)
                    for _ in self.tuner.fine_tune_to_gen(frequency,tolerance=final_tolerance,device=self._fine_device):
                        yield
                finally:
                    self.tuner.set_frequency_average_time(0)
                if abs(self.tuner.get_frequency()-frequency)<1E9:
                    return
            for _ in self.tuner.tune_to_gen(frequency,level,tolerance=final_tolerance,fine_device=self._fine_device):
                yield
        except FrequencyReadSirahError:
            pass
    def tune_to_loop(self, frequency, level="full", fine_threshold=3E9):
        """
        Fine tune the laser to the given frequency.
        
        `level` can be ``"bifi"`` (only tune the bifi motor), ``"thinet"`` (tune bifi motor and thin etalon),
        or ``"full"`` (full tuning using all elements).
        `fine_threshold` sets the fine tuning threshold; if the current frequency is within `fine_threshold` from the target, try tuning only with a slow piezo first.
        """
        if self.open():
            for _ in self._tune_to(frequency,level=level,fine_threshold=fine_threshold):
                yield
    def tune_to_finalize(self, *args, **kwargs):  # pylint: disable=unused-argument
        if self.open():
            self.tuner.fine_sweep_stop(return_to_start=False)
        self.update_operation_status("idle")
        self.update_parameters()
    def tune_to_start(self, frequency, level="full", fine_threshold=3E9):
        """Start fine tuning job"""
        self.stop_tuning()
        self.update_operation_status("fine_tuning")
        self.start_batch_job("tune_to",0.05,frequency,level=level,fine_threshold=fine_threshold)
    def tune_to_stop(self):
        """Stop fine tuning job"""
        self.stop_batch_job("tune_to")

    def change_lock_frequency(self, frequency):
        """Change target frequency if frequency locking is enabled"""
        if self._lock_frequency is None:
            return False
        self._lock_frequency=frequency
        return True
    def lock_frequency_loop(self, frequency, fine_threshold=10E9, final_tolerance=None):
        """
        Continuously lock the laser frequency to the given value.

        `fine_threshold` sets the maximal frequency change for which fine tuning is attempted first.
        `final_tolerance` is the target frequency tolerance (50 MHz by default).
        """
        if self.open():
            self.v["tuning/locking"]=True
            self._lock_frequency=frequency
            while True:
                curr_lock_frequency=self._lock_frequency
                for _ in self._tune_to(self._lock_frequency,fine_threshold=fine_threshold,final_tolerance=final_tolerance,freq_avg_time=0.2):
                    yield
                    if self._lock_frequency!=curr_lock_frequency:
                        break
    def lock_frequency_finalize(self, *args, **kwargs):  # pylint: disable=unused-argument
        self.v["tuning/locking"]=False
        self._lock_frequency=None
        self.update_operation_status("idle")
    def lock_frequency_start(self, frequency, fine_threshold=10E9, final_tolerance=None):
        """Start frequency locking job"""
        self.stop_tuning()
        self.update_operation_status("frequency_locking")
        self.start_batch_job("lock_frequency",0.05,frequency,fine_threshold=fine_threshold,final_tolerance=final_tolerance)
    def lock_frequency_stop(self):
        """Stop frequency locking job"""
        self.stop_batch_job("lock_frequency")

    def _stop_fine_sweep(self):
        crng=self.v["fine_scan/device_range_curr"]
        start_point=None if crng is None else (crng[0]+crng[1])/2
        self.tuner.fine_sweep_stop(start_point=start_point)
        self.v["fine_scan/device_range_curr"]=self.v["fine_scan/device_range_start"]=None
        self.v["fine_scan/device_rate_curr"]=None
    
    def fine_scan_loop(self, span, rate, kind="continuous"):
        """
        Start and continue fine scan with the given span and at a given rate around the current frequency.

        Currently, only ``kind=="continuous"`` is supported.
        """
        if self.open():
            self.tuner.fine_sweep_stop()
            scan_par=None
            for scan_par in self.tuner.fine_sweep_start_gen(span,up_speed=rate,down_speed=rate,kind="cont_up" if kind=="continuous" else "single_up",device=self._fine_device):
                yield
            if scan_par is not None:
                self.v["fine_scan/device_range_curr"]=self.v["fine_scan/device_range_start"]=scan_par[0]
                self.v["fine_scan/device_rate_curr"]=scan_par[1][0]
            self.update_scan_status("running")
            while True:
                yield
    def fine_scan_finalize(self, *args, **kwargs):  # pylint: disable=unused-argument
        if self.open():
            self._stop_fine_sweep()
        self.update_scan_status("idle")
        self.update_operation_status("idle")
    def fine_scan_start(self, span, rate, kind="continuous"):
        """
        Start fine scan with the given span and at a given rate around the current frequency.

        Currently, only ``kind=="continuous"`` is supported.
        """
        if self.open():
            # funcargparse.check_parameter_range(kind,"kind",["continuous","single"])
            funcargparse.check_parameter_range(kind,"kind",["continuous"])
            self.stop_tuning()
            self.update_operation_status("fine_scan")
            self.update_scan_status("setup")
            self.start_batch_job("fine_scan",0.05,span=span,rate=rate,kind=kind)
    def _sanitize_rng(self, rng, lim, minw):
        rmin,rmax=lim
        r0,r1=max(rmin,min(rng[0],rmax)),max(rmin,min(rng[1],rmax))
        r0,r1=min(r0,r1),max(r0,r1)
        if r1-r0>minw:
            if r1>rmax-minw:
                r1=r0+minw
            else:
                r0=r1-minw
        return r0,r1
    def fine_scan_adjust(self, rng=None, shift=None, span=None):
        """Change the range, shift or change the span of the currently executing fine scan (shift or span change is always relative to the original span)"""
        orng=self.v["fine_scan/device_range_start"]
        if orng is None:
            return
        if rng is None:
            if span is not None:
                center=(orng[0]+orng[1])/2+(shift or 0)
                rng=(center-span,center+span/2)
            elif shift is not None:
                rng=(orng[0]+shift,orng[1]+shift)
            else:
                return
        if self.open():
            rng=self._sanitize_rng(rng,(0,1),min(orng[1]-orng[0],1E-2))
            self.device.set_scan_status("stop")
            self.device.set_scan_params(lower_limit=rng[0],upper_limit=rng[1])
            self.device.set_scan_status("run")
            self.v["fine_scan/device_range_curr"]=tuple(rng)
    def fine_scan_stop(self):
        """Stop currently going fine scan"""
        self.stop_batch_job("fine_scan")

    def coarse_scan_loop(self, bifi_rng, te_rng):
        if self.open():
            self.update_scan_status("running")
            for prog in self.tuner.scan_coarse_gen(bifi_rng,te_rng):
                (i,ni),(j,nj)=prog
                self.update_progress((i*nj+j)/(ni*nj)*100)
                yield
    def coarse_scan_finalize(self, *args, **kwargs):  # pylint: disable=unused-argument
        self.update_scan_status("idle")
        self.update_operation_status("idle")
        self.update_progress(0)
        self.update_parameters()
    def coarse_scan_start(self, bifi_rng, te_rng, wait_time):
        """Start coarse scan within the given range ``(start, stop)`` at a given rate"""
        self.stop_tuning()
        self.update_operation_status("coarse_scan")
        self.update_scan_status("setup")
        self.update_progress(0)
        self.start_batch_job("coarse_scan",wait_time,bifi_rng=bifi_rng,te_rng=te_rng)
    def coarse_scan_stop(self):
        """Stop coarse scan"""
        self.stop_batch_job("coarse_scan")
    
    def stitched_scan_loop(self, scan_range, rate, single_span=15E9):
        if self.open():
            self.tuner.fine_sweep_stop(return_to_start=False)
            self.update_scan_status("running")
            try:
                for sweeping in self.tuner.stitched_scan_gen(scan_range,single_span,rate,device=self._fine_device,segment_end_timeout=5.):
                    self.v["stitched_scan/stitching"]=0 if sweeping else 1
                    if sweeping:
                        f0,f1=scan_range[:2]
                        fc=self.tuner.get_last_read_frequency()
                        if f1!=f0:
                            self.update_progress(max(0,min((fc-f0)/(f1-f0),1))*100)
                    yield
            except FrequencyReadSirahError:
                pass
    def stitched_scan_finalize(self, *args, **kwargs):  # pylint: disable=unused-argument
        self.v["stitched_scan/stitching"]=0
        self.update_scan_status("idle")
        self.update_operation_status("idle")
        self.update_progress(0)
        self.update_parameters()
    def stitched_scan_start(self, scan_range, rate, single_span=15E9):
        """Start stitched scan within the given range ``(start, stop)`` at a given rate"""
        self.stop_tuning()
        self.update_operation_status("stitched_scan")
        self.update_scan_status("setup")
        self.update_progress(0)
        self.start_batch_job("stitched_scan",0.05,scan_range=scan_range,rate=rate,single_span=single_span)
    def stitched_scan_stop(self):
        """Stop stitched scan"""
        self.stop_batch_job("stitched_scan")

    def stop_tuning(self):
        """Stop all tuning and sweeping"""
        self.lock_frequency_stop()
        self.tune_to_stop()
        self.stitched_scan_stop()
        self.coarse_scan_stop()
        self.fine_scan_stop()