from ... import device_thread



class VegaPowerMeterThread(device_thread.DeviceThread):
    """
    Ophir Vega power meter device thread.

    Device args:
        - ``conn``: device connection (usually, COM-port address)

    Variables:
        - ``power``: last measured power
        - ``parameters``: device parameters: range information, filter and diffuser state, wavelength

    Commands:
        - ``configure``: configure filter and range index
    """
    default_parameter_values={"range_idx":0,"range_info":(0,[],0),"filter_in":False,"diffuser_in":False,"wavelength":0}
    parameter_variables=default_parameter_values.keys()
    def connect_device(self):
        with self.using_devclass("Ophir.VegaPowerMeter",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
            self.device.get_power()
    def setup_task(self, conn, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,0.01 if remote else 0.002)
        self.add_job("update_parameters",self.update_parameters,1.)
    def update_measurements(self):
        """Update current measurements"""
        if self.open():
            power=self.device.get_power()
            self.v["power"]=self.device.get_range() if power=="over" else power
        else:
            self.v["power"]=0
            self.sleep(1.)
    def configure(self, filter_in=True, rng_idx=0, wavelength=None):
        """
        Configure filter settings and range index.

        `rng_idx` is the range index from 0 (highest) to maximal (lowest); auto-ranging is -1.
        """
        if self.open():
            if filter_in is not None:
                self.device.set_filter(filter_in=filter_in)
            if rng_idx is not None:
                self.device.set_range_idx(rng_idx)
            if wavelength is not None:
                self.device.set_wavelength(wavelength)