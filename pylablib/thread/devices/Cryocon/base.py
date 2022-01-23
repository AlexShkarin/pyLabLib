from ... import device_thread



class Cryocon1xThread(device_thread.DeviceThread):
    """
    Cryocon 1x series (12C, 14C, 18C) temperature controller device thread.

    Device args:
        - ``conn``: device connection (usually, COM-port address)
        - ``channel``: either a single channel or a list of channels whose readings and settings are periodically updated;
            if several channels are involved, then specific channels are the last nodes in the values
            (e.g. ``"temperature"`` for a channel C is stored at ``"temperature/C"``)
        - ``default_value``: value to assign to an unconnected channel or device

    Variables:
        - ``temperature``: last measured temperature
    """
    def connect_device(self):
        with self.using_devclass("Cryocon.Cryocon1x",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
    _all_channels=list("ABCDEFGH")
    def setup_task(self, conn, channel=None, default_value=0, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.default_value=default_value
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
            temperatures={ch:self.device.get_temperature(ch) for ch in self.channels}
            self.close()
        else:
            temperatures={ch:None for ch in self.channels}
            self.sleep(1.)
        for ch,v in temperatures.items():
            self.v["temperature",(ch if self.multichannel else "")]=v if v is not None else self.default_value