from ... import device_thread



class Lakeshore218Thread(device_thread.DeviceThread):
    """
    Lakeshore 218 temperature controller device thread.

    Device args:
        - ``conn``: device connection (usually, COM-port address)
        - ``channel``: either a single channel or a list of channels whose readings and settings are periodically updated;
            if several channels are involved, then specific channels are the last nodes in the values
            (e.g. ``"temperature"`` for a channel 3 is stored at ``"temperature/3"``)

    Variables:
        - ``temperature``: last measured temperature
        - ``sensor``: last measured sensor value (in sensor-specific units)
        - ``parameters``: device parameters: whether the channel is enabled
    """
    default_parameter_values={"enabled":False}
    parameter_variables=default_parameter_values.keys()
    def connect_device(self):
        with self.using_devclass("Lakeshore.Lakeshore218",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
    _all_channels=list(range(1,9))
    def setup_task(self, conn, channel=None, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        if channel is None:
            channel=self._all_channels
        self.multichannel=isinstance(channel,(list,tuple))
        self.channels=list(channel) if self.multichannel else [channel]
        self.add_job("update_measurements",self.update_measurements,2.5)
        self.add_job("update_parameters",self.update_parameters,10)
    def update_measurements(self):
        """Update current measurements"""
        if self.open():
            temperatures=self.device.get_all_temperatures()
            sensors=self.device.get_all_sensor_readings()
            self.close()
        else:
            temperatures=[0]*len(self._all_channels)
            sensors=[0]*len(self._all_channels)
            self.sleep(1.)
        for ch in self.channels:
            self.v["temperature",(ch if self.multichannel else "")]=temperatures[ch-1]
            self.v["sensor",(ch if self.multichannel else "")]=sensors[ch-1]
    def update_parameters(self):
        """Update current measurements"""
        if self.open():
            for p in self.default_parameter_values:
                v=self.device.dv[p]
                for ch in self.channels:
                    self.v["parameters",p,(ch if self.multichannel else "")]=v[ch-1]
            self.close()
        else:
            for p,v in self.default_parameter_values.items():
                for ch in self.channels:
                    self.v["parameters",p,(ch if self.multichannel else "")]=v
            self.sleep(1.)