from ... import device_thread


class ITR90Thread(device_thread.DeviceThread):
    """
    Leybold ITR90 pressure gauge device thread.

    Device args:
        - ``conn``: device connection (usually, COM-port address)

    Variables:
        - ``pressure``: last measured pressure
    """
    def connect_device(self):
        with self.using_devclass("Leybold.ITR90",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
    def setup_task(self, conn, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_job("update_parameters",self.update_parameters,5)
    def update_measurements(self):
        """Update current measurements"""
        if self.open():
            self.v["pressure"]=self.device.get_pressure()
        else:
            self.v["pressure"]=0
            self.sleep(1.)