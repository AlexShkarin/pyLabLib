from ... import device_thread



class XGS600Thread(device_thread.DeviceThread):
    """
    Agilent XGS-600 pressure gauge controller thread.

    Device args:
        - ``conn``: device connection (usually, COM-port address)
        - ``nchannels``: number of channels to emulate when no device is connected (the corresponding pressure variables are set to ``"none"``)

    Variables:
        - ``pressure/<n>``: last measured pressure on a channel ``n`` (starting from 1)
    """
    def connect_device(self):
        with self.using_devclass("Agilent.XGS600",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
    def setup_task(self, conn, remote=None, nchannels=0):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.nchannels=nchannels
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,1)
    def update_measurements(self):
        """Update current measurements"""
        if self.open():
            pressures=self.device.get_all_pressures()
            self.nchannels=len(pressures)
            self.v["pressure"]={ch+1:p for ch,p in enumerate(pressures)}
        else:
            self.v["pressure"]={ch+1:"none" for ch in range(self.nchannels)}
            self.sleep(1.)