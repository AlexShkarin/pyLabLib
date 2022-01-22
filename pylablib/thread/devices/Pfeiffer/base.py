from ... import device_thread



class TPG260Thread(device_thread.DeviceThread):
    """
    Pfeiffer TPG260 pressure gauge device thread.

    Device args:
        - ``conn``: device connection (usually, COM-port address)
        - ``channel``: either a single channel or a list of channels whose readings and settings are periodically updated;
            if several channels are involved, then specific channels are the last nodes in the values
            (e.g. ``"pressure"`` for a channel 1 is stored at ``"pressure/1"``)

    Variables:
        - ``pressure``: last measured pressure, or a dictionary of pressures if ``channel`` is a list or a tuple
        - ``parameters``: device parameters: channel status, gauge kind
    """
    full_info_variables={"cls","conn","pressure","channel_status","gauge_kind","enabled"}
    def connect_device(self):
        with self.using_devclass("Pfeiffer.TPG260",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
    _all_channels=[1,2]
    def setup_task(self, conn, remote=None, channel=1):  # pylint: disable=arguments-differ
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
            for ch in self.channels:
                self.v["pressure",(ch if self.multichannel else "")]=self.device.get_pressure(ch,status_error=False) or 0
        else:
            for ch in self.channels:
                self.v["pressure",(ch if self.multichannel else "")]=0
            self.sleep(1.)
    def update_parameters(self):
        """Update current measurements"""
        if self.open():
            self.v["parameters/enabled"]=self.device.is_enabled()
            for ch in self.channels:
                self.v["parameters/channel_status",(ch if self.multichannel else "")]=self.device.get_channel_status(ch)
            self.close()
        else:
            self.v["parameters/enabled"]=False
            for ch in self.channels:
                self.v["parameters/channel_status",(ch if self.multichannel else "")]="disconnected"
            self.sleep(1.)



class DPG202Thread(device_thread.DeviceThread):
    """
    Pfeiffer DPG202 pressure gauge device thread.

    Device args:
        - ``conn``: device connection (usually, COM-port address)
        - ``channel``: either a single channel or a list of channels whose readings and settings are periodically updated;
            if several channels are involved, then specific channels are the last nodes in the values
            (e.g. ``"pressure"`` for a channel 1 is stored at ``"pressure/1"``)

    Variables:
        - ``pressure``: last measured pressure, or a dictionary of pressures if ``channel`` is a list or a tuple
    """
    def connect_device(self):
        with self.using_devclass("Pfeiffer.DPG202",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
    def setup_task(self, conn, remote=None, channel=1):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.multichannel=isinstance(channel,(list,tuple))
        self.channels=list(channel) if self.multichannel else [channel]
        self.add_job("update_measurements",self.update_measurements,1)
        self.add_job("update_parameters",self.update_parameters,5)
    def update_measurements(self):
        """Update current measurements"""
        if self.open():
            for ch in self.channels:
                self.v["pressure",(ch if self.multichannel else "")]=self.device.get_pressure(address=ch)
            self.close()
        else:
            for ch in self.channels:
                self.v["pressure",(ch if self.multichannel else "")]=0
            self.sleep(1.)