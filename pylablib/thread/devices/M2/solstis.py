from ... import device_thread
from ....devices import M2
from ....core.thread import controller

import time
import numpy as np


class M2Thread(device_thread.DeviceThread):
    """
    M2 SolsTiS laser device thread.

    Device args:
        - ``addr``: ICE box IP address
        - ``port``: ICE box port (usually, 39933)
        - ``use_websocket``: if ``True``, use websocket interface (same as used by the web interface) for additional functionality
            (wavemeter connection, element tuning values, improved operation stopping)
        - ``use_cavity``: if ``False`` and any reference cavity methods are used, either ignore them, or use closest available methods instead
        - ``wavemeter``: name of the wavemeter thread controller (used for fine tuning interruption routine; not required)

    Variables:
        - ``parameters/fine_wavelength``: last measured laser wavelength (fine tuning regime)
        - ``parameters/coarse_wavelength``: last measured laser wavelength (coarse tuning regime)
        - ``parameters/wavemeter_connected``: whether wavemeter connection is on
        - ``parameters/web_status``: full laser web status (only if ``use_websocket==True`` on creation)
        - ``terascan/stitching``: whether terascan stitching is in effect
        - ``progress``: current scan progress (in percent)
        - ``status/operation``: current laser operation; can be ``"idle"``, ``"stopping"``, ``"wavemeter_connection"``,
            ``"terascan"``, ``"fast_scan"``, ``"coarse_scan"``, ``"coarse_tuning"``, ``"fine_tuning"``, or ``"element_tuning"``.
        - ``status/scan``: current scan progress; can be ``"idle"``, ``"setup"``, or ``"running"``
        - ``status/terascan/result``: result of a terascan; can be ``"running"``, ``"success"`` or ``"fail"`` (failed due to, e.g., stitching error)

    Commands:
        - ``set_wavemeter_connection``: turn wavemeter connection on or off (only if ``use_websocket==True``)
        - ``stop_tuning``: stop all laser operation (tuning, sweeps)
        - ``tune_element``: set laser element (etalon, resonator, cavity) position
        - ``coarse_tune``: coarse-tune the laser (coarse tuning using BRF, or fine tuning)
        - ``fine_tune_start``: start fine tuning routine
        - ``fine_tune_stop``: stop fine tuning routine
        - ``terascan_start``: start terascan routine
        - ``terascan_stop``: stop terascan routine
        - ``fast_scan_start``: start fast scan routine
        - ``fast_scan_stop``: stop fast scan routine
        - ``coarse_scan_start``: start coarse scan (manual changing of BRF and etalon) routine
        - ``coarse_scan_stop``: stop coarse scan (manual changing of BRF and etalon) routine
    """
    def connect_device(self):
        with self.using_devclass("M2.Solstis",host=self.remote) as cls:
            self.device=cls(addr=self.addr,port=self.port,use_websocket=self.use_websocket,use_cavity=self.use_cavity,timeout=10.)  # pylint: disable=not-callable
            self.device.set_timeout(120)
            self.device.get_coarse_wavelength()
    def setup_task(self, addr, port, use_websocket=True, use_cavity=True, wavemeter=None, remote=None):  # pylint: disable=arguments-differ
        self.setup_properties()
        self.addr=addr
        self.port=port
        self.use_websocket=use_websocket
        self.use_cavity=use_cavity
        self.remote=remote
        self.open()
        self.update_progress(0.)
        self.add_command("set_wavemeter_connection",self.set_wavemeter_connection,limit_queue=1,on_full_queue="skip_oldest")
        self.add_command("stop_tuning",limit_queue=1,priority=10)
        self.add_command("tune_element",limit_queue=1,on_full_queue="skip_oldest")
        self.add_command("coarse_tune",limit_queue=1,on_full_queue="skip_oldest")
        self.add_command("fine_tune_start",limit_queue=1,on_full_queue="skip_oldest")
        self.add_command("fine_tune_stop",limit_queue=1,on_full_queue="skip_oldest")
        self.add_batch_job("fine_tune",self.fine_tune_loop,self.fine_tune_finalize)
        self.add_command("terascan_start",limit_queue=1,on_full_queue="skip_oldest")
        self.add_command("terascan_stop",limit_queue=1,on_full_queue="skip_oldest")
        self.add_batch_job("terascan",self.terascan_loop,self.terascan_finalize)
        self.add_command("fast_scan_start",limit_queue=1,on_full_queue="skip_oldest")
        self.add_command("fast_scan_stop",limit_queue=1,on_full_queue="skip_oldest")
        self.add_batch_job("fast_scan",self.fast_scan_loop,self.fast_scan_finalize)
        self.add_command("coarse_scan_start",limit_queue=1,on_full_queue="skip_oldest")
        self.add_command("coarse_scan_stop",limit_queue=1,on_full_queue="skip_oldest")
        self.add_batch_job("coarse_scan",self.coarse_scan_loop,self.coarse_scan_finalize)
        self.add_job("update_parameters",self.update_parameters,.5)
        self.add_job("update_web_status",self.update_web_status,2.)
        self.wavemeter=wavemeter

    def setup_properties(self):
        """Setup initial device variables"""
        self.v["parameters/fine_wavelength"]=-1
        self.v["parameters/coarse_wavelength"]=-1
        self.v["parameters/wavemeter_connected"]=False
        self.v["terascan/stitching"]=0
        self.update_progress(0)
        self.update_operation_status("idle")
        self.update_scan_status("idle")
        self.update_status("terascan/result","success","Success")

    def update_progress(self, progress):
        """Update current progress"""
        self.v["progress"]=progress
    def update_operation_status(self, status, reason=None):
        """
        Update operation status (``"status/operation"``).
        
        If `reason` is not ``None``, add it to the status text.
        """
        status_text={"idle":"Idle","stopping":"Stopping","wavemeter_connection":"Changing wavemeter connection",
            "terascan":"Terascan","fast_scan":"Fast scan","coarse_scan":"Coarse scan",
            "coarse_tuning":"Coarse tuning","fine_tuning":"Fine tuning","element_tuning":"Element tuning"}
        curr_status=self.get_variable("status/operation")
        text=status_text[status]
        if reason is not None:
            if reason in status_text:
                reason=status_text[reason].lower()
            text="{} for {}".format(text,reason)
        self.update_status("operation",status,text=text)
        return curr_status
    def update_scan_status(self, status):
        """Update scan status (``"status/scan"``)"""
        status_text={"idle":"Idle","setup":"Setup","running":"In progress"}
        self.update_status("scan",status,status_text[status])

    def _stop_all_operations(self, reason=None):
        if self.open():
            self.stop_batch_job("coarse_scan")
            self.stop_batch_job("fine_tune")
            self.stop_batch_job("terascan")
            self.stop_batch_job("fast_scan")
            status=self.update_operation_status("stopping",reason=reason)
            self.device.stop_all_operation()
            self.update_operation_status(status)
    def stop_tuning(self):
        """Stop all laser operation and tuning/scanning routines"""
        self._stop_all_operations()
        self.update_operation_status("idle")
    def set_wavemeter_connection(self, connected):
        """Set wavemeter connection (called automatically if required for commands/routines)"""
        if self.use_websocket and self.open():
            status=self.update_operation_status("wavemeter_connection")
            if connected:
                self.device.connect_wavemeter()
            else:
                self.device.disconnect_wavemeter()
            self.update_operation_status(status)

    def coarse_tune(self, wavelength):
        """Coarse tune laser wavelength"""
        if self.open():
            self._stop_all_operations(reason="coarse_tuning")
            self.set_wavemeter_connection(False)
            self.update_operation_status("coarse_tuning")
            try:
                self.device.coarse_tune_wavelength(wavelength,sync=False)
            except self.device.Error:
                pass
            self.update_operation_status("idle")
    def tune_element(self, element, value):
        """
        Tune internal laser element.
        
        `element` can be ``"etalon"``, ``"resonator"``, ``"resonator_fine"``, ``"cavity"``, or ``"cavity_fine"``.
        """
        if self.open():
            self._stop_all_operations(reason="element_tuning")
            self.update_operation_status("element_tuning")
            if element=="etalon":
                self.device.tune_etalon(value)
            elif element=="resonator":
                self.device.tune_laser_resonator(value)
            elif element=="resonator_fine":
                self.device.tune_laser_resonator(value,fine=True)
            elif element=="cavity":
                self.device.tune_reference_cavity(value)
            elif element=="cavity_fine":
                self.device.tune_reference_cavity(value,fine=True)
            else:
                raise ValueError("unrecognized elements: {}".format(element))
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
            self.set_wavemeter_connection(True)
            try:
                self.device.fine_tune_wavelength(wavelength,sync=False)
            except self.device.Error:
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
                    if self.device.get_etalon_lock_status()=="error" or self.device.get_reference_cavity_lock_status()=="error":
                        failed=True
                    if time.time()-tune_start>tune_timeout:
                        failed=True
                    if failed:
                        self.device.stop_fine_tuning()
                        self.device.unlock_etalon()
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
                    if self.device.get_etalon_lock_status()=="error" or self.device.get_reference_cavity_lock_status()=="error":
                        self.device.stop_fine_tuning()
                        self.device.unlock_etalon()
                        tuned=False
                        break
                    if time.time()-tune_start>tune_timeout:
                        self.device.stop_fine_tuning()
                        self.device.unlock_etalon()
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
                ``"fine"`` (all elements, rate from 20 GHz/s to 1 MHz/s), ``"line"`` (all elements, rate from 20 GHz/s to 50 kHz/s),
                or ``"auto"`` (auto-select based on rate: ``"line"`` below 1GHz/s, ``"fine"`` below 10GHz/s, ``"medium"`` otherwise)
            scan_range(tuple): tuple ``(start,stop)`` with the scan range (in Hz).
            rate(float): scan rate (in Hz/s).
        """
        if self.open():
            self._stop_all_operations(reason="terascan")
            if scan_type=="auto":
                if rate<1E9:
                    scan_type="line"
                elif rate<10E9:
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
            self.set_wavemeter_connection(True)
            self.device.unlock_etalon()
            self.device.enable_terascan_updates()
            self.device.setup_terascan(scan_type,scan_range,rate)
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
                    status=self.device.get_terascan_status(scan_type,web_status=False)
                    if status["status"]=="stopped":
                        self.update_status("terascan/result","success","Success")
                        break
                    stitching_frozen=(stitching_started is not None and time.time()-stitching_started>60)
                    scanning_frozen=(scanning_started is not None and time.time()-scanning_started>30E9/rate+60.)
                    stitching_frozen_long=(stitching_started is not None and time.time()-stitching_started>120)
                    scanning_frozen_long=(scanning_started is not None and time.time()-scanning_started>60E9/rate+120.)
                    if stitching_frozen or scanning_frozen:
                        status=self.device.get_terascan_status(scan_type)
                        if status["web"]=="fail" or (stitching_frozen_long or scanning_frozen_long):
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
                    if status["activity"]=="stitching":
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

    def fast_scan_start(self, scan_type, width, time, fine_tune=None):  # pylint: disable=redefined-outer-name
        """
        Start fine sweep routine.

        Args:
            scan_type(str): scan type. Can be ``"cavity_continuous"``, ``"cavity_single"``, ``"cavity_triangular"``,
                ``"resonator_continuous"``, ``"resonator_single"``, ``"resonator_ramp"``, ``"resonator_triangular"``,
                ``"ect_continuous"``, ``"ecd_ramp"``, or ``"fringe_test"`` (see ICE manual for details)
            width(float): scan width (in Hz).
            time(float): scan time/period (in s).
            fine_tune: if not ``None``, fine tune to this frequency before starting the fine sweep
        """
        if self.open():
            self._stop_all_operations(reason="fast_scan")
            self.update_operation_status("fast_scan")
            self.update_scan_status("setup")
            self.update_progress(0)
            self.start_batch_job("fast_scan",0.1,scan_type,width,time,fine_tune=fine_tune)
    def fast_scan_stop(self):
        """Stop fine sweep routine"""
        self.stop_batch_job("fast_scan")
    def fast_scan_loop(self, scan_type, width, time, fine_tune=None):  # pylint: disable=redefined-outer-name
        if fine_tune is not None:
            for y in self.fine_tune_loop(*fine_tune):
                yield y
            self.device.stop_all_operation()
        try:
            self.device.start_fast_scan(scan_type,width,time,sync=True)
        except self.device.Error:
            return
        self.update_scan_status("running")
        while True:
            status=self.device.get_fast_scan_status(scan_type)
            self.update_progress(status["value"])
            if status["status"]=="stopped":
                break
            yield
    def fast_scan_finalize(self, *args, **kwargs):  # pylint: disable=unused-argument
        self.update_progress(0)
        self.update_scan_status("idle")
        self.stop_tuning()

    def coarse_scan_start(self, wavelength_rng, etalon_rng, step_period=0.):
        """
        Start coarse scan routine.

        "Manually" step coarse wavelength and etalon values withing the given ranges.

        Args:
            wavelength_rng: tuple ``(start, stop)`` with coarse (BRF-set) wavelength to sweep over
            etalon_rng: tuple ``(start, stop)`` with etalon positions (between 0 and 100) to sweep over
            step_period: time to wait at every wavelength + etalon combination
        """
        if self.open():
            self._stop_all_operations(reason="coarse_scan")
            self.update_operation_status("coarse_scan")
            self.update_scan_status("setup")
            self.update_progress(0)
            self.start_batch_job("coarse_scan",step_period,wavelength_rng,etalon_rng)
    def coarse_scan_stop(self):
        """Stop coarse scan routine"""
        self.stop_batch_job("coarse_scan")
    def coarse_scan_loop(self, wavelength_rng, etalon_rng):
        self.set_wavemeter_connection(False)
        self.device.unlock_etalon()
        for wl in wavelength_rng[:2]:
            if wl<500E-9 or wl>1.5E-6:
                raise ValueError("wrong wavelength: {}".format(wl))
        if abs((wavelength_rng[0]-wavelength_rng[1])/wavelength_rng[2])>1E6:
            raise ValueError("too many wavelength points: {}".format(abs((wavelength_rng[0]-wavelength_rng[1])/wavelength_rng[2])))
        for et in etalon_rng[:2]:
            if et<0 or et>100:
                raise ValueError("wrong etalon value: {}".format(et))
        if abs((etalon_rng[0]-etalon_rng[1])/etalon_rng[2])>1E6:
            raise ValueError("too many etalon points: {}".format(abs((etalon_rng[0]-etalon_rng[1])/etalon_rng[2])))
        self.update_scan_status("running")
        wldir=1 if wavelength_rng[1]-wavelength_rng[0]>0 else -1
        wavelengths=np.arange(wavelength_rng[0],wavelength_rng[1],abs(wavelength_rng[2])*wldir)
        for i,wl in enumerate(wavelengths):
            self.device.coarse_tune_wavelength(wl)
            for et in np.arange(*etalon_rng):
                self.device.tune_etalon(et)
                yield
            self.update_progress((i+1.)/len(wavelengths)*100.)
    def coarse_scan_finalize(self, *args, **kwargs):  # pylint: disable=unused-argument
        self.update_progress(0)
        self.update_scan_status("idle")
        self.stop_tuning()

    def update_parameters(self):
        if self.open():
            self.v["parameters/fine_wavelength"]=self.device.get_fine_wavelength()
            self.v["parameters/coarse_wavelength"]=self.device.get_coarse_wavelength()
            self.v["settings/system_status"]=self.device.get_system_status()
        else:
            self.v["parameters/fine_wavelength"]=-1
            self.v["parameters/coarse_wavelength"]=-1
            self.v["settings/system_status"]={}
    def update_web_status(self):
        if self.v["status/operation"]!="sweep/terascan":
            if self.open():
                self.v["parameters/web_status"]=self.device.get_full_web_status() or {}
                self.v["parameters/wavemeter_connected"]=self.get_variable("parameters/web_status/wlm_fitted",False)