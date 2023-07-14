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
        - ``piezoet_position``: position of the piezo etalon (normalized)
        - ``slowpiezo_position``: position of the slow piezo (normalized)
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
        self.add_job("update_measurements",self.update_measurements,.2)
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

    def update_measurements(self):
        params=["diode_power","thinet_power","bifi_position","thinet_position","piezoet_position",
                    "slowpiezo_position","fastpiezo_position","fastpiezo_locked","scan_position","refcell_position"]
        param_defaults={p:(False if p=="fastpiezo_locked" else 0) for p in params}
        if self.open():
            for n,v in param_defaults.items():
                try:
                    self.v[n]=self.device.dv[n]
                except self.DeviceError:  # pylint: disable=catching-non-exception
                    self.v[n]=v
            self.v["scanning"]=self.device.get_scan_status()=="run"
        else:
            for n,v in param_defaults.items():
                self.v[n]=v
            self.v["scanning"]=False






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
        - ``tune_to_stop``: stop fine tuning to the given frequency
        - ``fine_scan_start``: start fine scan with the given parameters
        - ``fine_scan_stop``: stop fine scan with the given parameters
        - ``stitched_scan_start``: start stitched scan with the given frequency range
        - ``stitched_scan_stop``: stop stitched scan with the given frequency range
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
    def setup_task(self, conn, wmversion, remote=None, wmremote="auto", calibration=None):  # pylint: disable=arguments-differ
        self.conn=conn
        self.remote=remote
        self.wmversion=wmversion
        self.wmremote=wmremote if wmremote!="auto" else remote
        self.calibration=calibration
        self._lock_frequency=None
        self._fine_device="slow_piezo"
        self.add_job("update_measurements",self.update_measurements,.2)
        self.v["stitched_scan/stitching"]=0
        self.v["tuning/locking"]=False
        self.v["fine_tune_device"]=self._fine_device
        self.add_command("set_fine_tune_device")
        self.add_batch_job("tune_to",self.tune_to_loop,self.tune_to_finalize)
        self.add_command("tune_to_start")
        self.add_command("tune_to_stop")
        self.add_batch_job("lock_frequency",self.lock_frequency_loop,self.lock_frequency_finalize)
        self.add_command("lock_frequency_start")
        self.add_command("lock_frequency_stop")
        self.add_command("change_lock_frequency")
        self.add_command("fine_scan_start")
        self.add_command("fine_scan_stop")
        self.add_batch_job("stitched_scan",self.stitched_scan_loop,self.stitched_scan_finalize)
        self.add_command("stitched_scan_start")
        self.add_command("stitched_scan_stop")
        self.add_command("stop_tuning")
        self.update_scan_status("idle")
        self.update_operation_status("idle")
    
    def finalize_task(self):
        if self.device is not None:
            self.stop_tuning()
        super().finalize_task()
    _scan_status_text={"idle":"Idle","setup":"Setup","running":"In progress"}
    def update_scan_status(self, status):
        """Update scan status (``"status/scan"``)"""
        self.update_status("scan",status,self._scan_status_text[status])
    _operation_status_text={"idle":"Idle","wavemeter_connection":"Changing wavemeter connection",
            "stitched_scan":"Stitched scan","fine_scan":"Fine scan","fine_tuning":"Fine tuning","frequency_locking":"Frequency locking"}
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
            self.tuner.fine_sweep_stop()
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
    def lock_frequency_loop(self, frequency, fine_threshold=3E9, final_tolerance=None):
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
    def lock_frequency_start(self, frequency, fine_threshold=3E9, final_tolerance=None):
        """Start frequency locking job"""
        self.stop_tuning()
        self.update_operation_status("frequency_locking")
        self.start_batch_job("lock_frequency",0.05,frequency,fine_threshold=fine_threshold,final_tolerance=final_tolerance)
    def lock_frequency_stop(self):
        """Stop frequency locking job"""
        self.stop_batch_job("lock_frequency")

    def fine_scan_start(self, span, rate, kind="continuous"):
        """
        Start fine scan with the given span and at a given rate around the current frequency.

        Currently, only ``kind=="continuous"`` is supported.
        """
        if self.open():
            # funcargparse.check_parameter_range(kind,"kind",["continuous","single"])
            funcargparse.check_parameter_range(kind,"kind",["continuous"])
            self.stop_tuning()
            self.tuner.fine_sweep_stop()
            self.update_operation_status("fine_scan")
            self.update_scan_status("setup")
            self._fine_start_pos=self.device.get_slowpiezo_position()
            self.tuner.fine_sweep_start(span,up_speed=rate,down_speed=rate,kind="cont_up" if kind=="continuous" else "single_up",device=self._fine_device)
            self.update_scan_status("running")
    def fine_scan_stop(self):
        """Stop currently going fine scan"""
        if self.open():
            self.tuner.fine_sweep_stop()
        self.update_scan_status("idle")
        self.update_operation_status("idle")
    
    def stitched_scan_loop(self, scan_range, rate, single_span=15E9):
        if self.open():
            self.tuner.fine_sweep_stop()
            self.update_scan_status("running")
            try:
                for sweeping in self.tuner.stitched_scan_gen(scan_range,single_span,rate,device=self._fine_device):
                    self.v["stitched_scan/stitching"]=0 if sweeping else 1
                    yield
            except FrequencyReadSirahError:
                pass
    def stitched_scan_finalize(self, *args, **kwargs):  # pylint: disable=unused-argument
        self.v["stitched_scan/stitching"]=0
        self.update_scan_status("idle")
        self.update_operation_status("idle")
        self.update_parameters()
    def stitched_scan_start(self, scan_range, rate, single_span=15E9):
        """Start stitched scan within the given range ``(start, stop)`` at a given rate"""
        self.stop_tuning()
        self.update_operation_status("stitched_scan")
        self.update_scan_status("setup")
        self.start_batch_job("stitched_scan",0.05,scan_range=scan_range,rate=rate,single_span=single_span)
    def stitched_scan_stop(self):
        """Stop stitched scan"""
        self.stop_batch_job("stitched_scan")

    def stop_tuning(self):
        """Stop all tuning and sweeping"""
        self.lock_frequency_stop()
        self.tune_to_stop()
        self.stitched_scan_stop()
        self.fine_scan_stop()