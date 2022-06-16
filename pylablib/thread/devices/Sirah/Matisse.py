from ... import device_thread


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