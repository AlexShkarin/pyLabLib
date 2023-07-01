from ... import device_thread
from ....devices import M2
from ....core.thread import controller

import time


class M2EMMThread(device_thread.DeviceThread):
    """
    M2 EMM laser device thread.

    Device args:
        - ``addr``: ICE box IP address
        - ``port``: ICE box port (usually, 39933)
        - ``wavemeter``: name of the wavemeter thread controller (used for fine tuning interruption routine; not required)

    Variables:
        - ``parameters/fine_wavelength``: last measured laser wavelength (fine tuning regime)
        - ``terascan/stitching``: whether terascan stitching is in effect
        - ``progress``: current scan progress (in percent)
        - ``status/operation``: current laser operation; can be ``"idle"``, ``"stopping"``, ``"terascan"``, or ``"fine_tuning"``.
        - ``status/scan``: current scan progress; can be ``"idle"``, ``"setup"``, or ``"running"``
        - ``status/terascan/result``: result of a terascan; can be ``"running"``, ``"success"`` or ``"fail"`` (failed due to, e.g., stitching error)

    Commands:
        - ``stop_tuning``: stop all laser operation (tuning, sweeps)
        - ``fine_tune_start``: start fine tuning routine
        - ``fine_tune_stop``: stop fine tuning routine
        - ``terascan_start``: start terascan routine
        - ``terascan_stop``: stop terascan routine
    """
    def connect_device(self):
        with self.using_devclass("M2.EMM",host=self.remote) as cls:
            self.device=cls(addr=self.addr,port=self.port,timeout=10.)  # pylint: disable=not-callable
            self.device.set_timeout(120)
            self.device.get_laser_status()
    def setup_task(self, addr, port, wavemeter=None, remote=None):  # pylint: disable=arguments-differ
        self.setup_properties()
        self.addr=addr
        self.port=port
        self.remote=remote
        self.open()
        self.update_progress(0.)
        self.add_command("stop_tuning",limit_queue=1,priority=10)
        self.add_command("fine_tune_start",limit_queue=1,on_full_queue="skip_oldest")
        self.add_command("fine_tune_stop",limit_queue=1,on_full_queue="skip_oldest")
        self.add_batch_job("fine_tune",self.fine_tune_loop,self.fine_tune_finalize)
        self.add_command("terascan_start",limit_queue=1,on_full_queue="skip_oldest")
        self.add_command("terascan_stop",limit_queue=1,on_full_queue="skip_oldest")
        self.add_batch_job("terascan",self.terascan_loop,self.terascan_finalize)
        self.add_job("update_parameters",self.update_parameters,.5)
        self.wavemeter=wavemeter

    def setup_properties(self):
        """Setup initial device variables"""
        self.v["parameters/fine_wavelength"]=-1
        self.v["terascan/stitching"]=0
        self.update_progress(0)
        self.update_operation_status("idle")
        self.update_scan_status("idle")
        self.update_status("terascan/result","success","Success")

    def _apply_calibration_frequency(self, freq, kind=None):  # pylint: disable=unused-argument
        return freq
    def _apply_calibration_wavelength(self, wl, kind=None):
        return M2.c/self._apply_calibration_frequency(M2.c/wl,kind=kind)

    def update_progress(self, progress):
        """Update current progress"""
        self.v["progress"]=progress
    _operation_status_text={"idle":"Idle","stopping":"Stopping","terascan":"Terascan","fine_tuning":"Fine tuning","fast_scan":"Fast scan"}
    def update_operation_status(self, status, reason=None):
        """
        Update operation status (``"status/operation"``).
        
        If `reason` is not ``None``, add it to the status text.
        """
        curr_status=self.get_variable("status/operation")
        text=self._operation_status_text[status]
        if reason is not None:
            if reason in self._operation_status_text:
                reason=self._operation_status_text[reason].lower()
            text="{} for {}".format(text,reason)
        self.update_status("operation",status,text=text)
        return curr_status
    _scan_status_text={"idle":"Idle","setup":"Setup","running":"In progress"}
    def update_scan_status(self, status):
        """Update scan status (``"status/scan"``)"""
        self.update_status("scan",status,self._scan_status_text[status])

    def _stop_all_operations(self, reason=None):
        if self.open():
            self.stop_batch_job("fine_tune")
            self.stop_batch_job("terascan")
            status=self.update_operation_status("stopping",reason=reason)
            self.device.stop_all_operation()
            self.update_operation_status(status)
    def stop_tuning(self):
        """Stop all laser operation and tuning/scanning routines"""
        self._stop_all_operations()
        self.update_operation_status("idle")

    def fine_tune_start(self, wavelength, freq_precision=0., freq_timeout=3.):
        """
        Start fine tuning routine.

        If ``freq_precision>0`` and wavemeter thread name is supplied on setup, invoke early tuning termination.
        In this regime, if the laser frequency is within `freq_precision` of the target frequency for `freq_timeout` seconds, abort the tuning (i.e., assume that it is done). 
        Otherwise, the tuning is done as normal (the laser controller decides when the tuning is done)
        """
        if self.open():
            self._stop_all_operations(reason="fine_tuning")
            self.update_operation_status("fine_tuning")
            self.start_batch_job("fine_tune",0.1,wavelength,freq_precision,freq_timeout)
    def fine_tune_stop(self):
        """Stop fine tuning routine"""
        self.stop_batch_job("fine_tune")
    def fine_tune_loop(self, wavelength, freq_precision=0., freq_timeout=3.):
        tuned=False
        while not tuned:
            try:
                self.device.fine_tune_wavelength(self._apply_calibration_wavelength(wavelength),sync=False)
            except self.DeviceError:  # pylint: disable=catching-non-exception
                return
            tune_start=time.time()
            tune_timeout=30.
            tuned=True
            if self.wavemeter and freq_precision:
                target_freq=M2.c/wavelength
                wavemeter=controller.sync_controller(self.wavemeter)
                t_in_range=None
                while not self.device.check_fine_tuning_report():
                    failed=False
                    if time.time()-tune_start>tune_timeout:
                        failed=True
                    if failed:
                        self.device.stop_fine_tuning()
                        self.sleep(1.)
                        tuned=False
                        break
                    if t_in_range and time.time()-t_in_range>freq_timeout:
                        break
                    freq=wavemeter.get_variable("frequency",None)
                    if freq and not isinstance(freq,str) and freq>0 and abs(freq-target_freq)<=freq_precision:
                        if t_in_range is None:
                            t_in_range=time.time()
                    else:
                        t_in_range=None
                    yield
            else:
                while not self.device.check_fine_tuning_report():
                    if time.time()-tune_start>tune_timeout:
                        self.device.stop_fine_tuning()
                        self.sleep(1.)
                        tuned=False
                        break
                    yield
    def fine_tune_finalize(self, *args, **kwargs):  # pylint: disable=unused-argument
        self.stop_tuning()

    
    def terascan_start(self, scan_type, scan_range, rate, failsafe=True):
        """
        Start terascan routine.

        Args:
            scan_type(str): scan type. Can be ``"medium"`` (BRF+etalon, rate from 100 GHz/s to 1 GHz/s),
                ``"fine"`` (all elements, rate from 20 GHz/s to 1 MHz/s), ``"ir_medium"`` or ``"ir_fine"`` (same as ``"medium"`` or ``"fine"``, but defined for the IR laser)
            scan_range(tuple): tuple ``(start,stop)`` with the scan range (in Hz).
            rate(float): scan rate (in Hz/s).
        """
        if self.open():
            self._stop_all_operations(reason="terascan")
            if scan_type=="auto":
                if rate<10E9:
                    scan_type="fine"
                else:
                    scan_type="medium"
            self.update_operation_status("terascan")
            self.update_scan_status("setup")
            self.update_status("terascan/result","running","Running")
            self.update_progress(0)
            self.start_batch_job("terascan",0.2,scan_type,scan_range,rate,failsafe=failsafe)
    def terascan_stop(self):
        """Stop terascan routine"""
        self.stop_batch_job("terascan")
    def terascan_loop(self, scan_type, scan_range, rate, failsafe):
        while True:
            failed=False
            self.device.enable_terascan_updates()
            self.device.setup_terascan(scan_type,[self._apply_calibration_frequency(f) for f in scan_range],rate)
            self.device.start_terascan(scan_type,sync=True)
            self.update_scan_status("running")
            status_check_period=25 # check completion every 25 seconds
            cnt=0
            progress=0.
            last_frequency=None
            stitching_started=None
            scanning_started=None
            while True:
                cnt=(cnt+1)%status_check_period
                if cnt==0:
                    status=self.device.get_terascan_status(scan_type)
                    if status["status"]=="stopped":
                        self.update_status("terascan/result","success","Success")
                        break
                    stitching_frozen_long=(stitching_started is not None and time.time()-stitching_started>120)
                    scanning_frozen_long=(scanning_started is not None and time.time()-scanning_started>60E9/rate+120.)
                    if stitching_frozen_long or scanning_frozen_long:
                        self.update_status("terascan/result","fail","Fail")
                        if failsafe:
                            self.device.stop_all_operation()
                            time.sleep(3.)
                            if scan_range[0]<scan_range[1]:
                                restart_frequency=max(last_frequency-20E9,scan_range[0])
                            else:
                                restart_frequency=min(last_frequency+20E9,scan_range[0])
                            scan_range=(restart_frequency,scan_range[1])
                        failed=True
                        break
                    curr,rng=status["current"],status["range"]
                    last_frequency=curr
                    progress=max(min((curr-rng[0])/(rng[1]-rng[0]),1.),0.)*100.
                    self.update_progress(progress)
                else:
                    status=self.device.check_terascan_update()
                    if status and status["activity"]=="stitching":
                        self.v["terascan/stitching"]=1
                        if stitching_started is None:
                            stitching_started=time.time()
                        scanning_started=None
                    else:
                        self.v["terascan/stitching"]=0
                        stitching_started=None
                        if scanning_started is None:
                            scanning_started=time.time()
                yield
            if not (failed and failsafe):
                break
    def terascan_finalize(self, *args, **kwargs):  # pylint: disable=unused-argument
        self.device.enable_terascan_updates(False)
        self.update_progress(0)
        self.update_scan_status("idle")
        self.v["terascan/stitching"]=0
        self.stop_tuning()

    def update_parameters(self):
        if self.open():
            self.v["parameters/fine_wavelength"]=self.device.get_fine_wavelength()
            self.v["settings/laser_status"]=self.device.get_laser_status()
        else:
            self.v["parameters/fine_wavelength"]=-1
            self.v["settings/laser_status"]={}