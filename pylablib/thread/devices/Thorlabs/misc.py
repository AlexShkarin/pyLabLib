from ... import device_thread



class PM160Thread(device_thread.DeviceThread):
    """
    Thorlabs PM160 optical Power Meter device thread.

    Device args:
        - ``conn``: device connection (usually, a VISA connection string or a COM port for bluetooth devices)

    Variables:
        - ``reading``: last measured reading
        - ``parameters``: device parameters: range information, wavelength, measurement mode

    Commands:
        - ``configure``: configure sensor mode, range, and wavelength
    """
    default_parameter_values={"wavelength":0,"mode":"power","autorange":False,"range":0}
    parameter_variables=default_parameter_values.keys()
    def connect_device(self):
        with self.using_devclass("Thorlabs.PM160",host=self.remote) as cls:
            self.device=cls(addr=self.conn)  # pylint: disable=not-callable
    def setup_task(self, conn, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,0.5 if remote else 0.05)
        self.add_job("update_parameters",self.update_parameters,1.)
        self.add_command("configure")
    def update_measurements(self):
        if self.open():
            self.v["reading"]=self.device.get_reading()
        else:
            self.v["reading"]=0
            self.sleep(1.)
    def configure(self, sensor_mode=None, rng=None, wavelength=None):
        """
        Configure sensor mode, range, and wavelength.

        `sensor_mode` can be ``"power"``, ``"energy"``, ``"voltage"``, ``"current"``, or ``"frequency"``.
        `range` is the measurement range; can also be ``"full"`` (set max range) or ``"auto"`` (enable autorange).
        """
        if self.open():
            if sensor_mode is not None:
                self.device.set_sensor_mode(sensor_mode)
            if rng=="auto":
                self.device.enable_autorange()
            elif rng is not None:
                self.device.set_range(rng)
            if wavelength is not None:
                self.device.set_wavelength(wavelength)
            self.update_parameters()
            self.update_measurements()