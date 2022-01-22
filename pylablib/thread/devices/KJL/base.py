from ... import device_thread


class KJL300Thread(device_thread.DeviceThread):
    """
    KJL300 pressure gauge device thread.

    Device args:
        - ``conn``: device connection (usually, COM-port address)
        - ``addr``: RS485 address (required both for RS-485 and for RS-232 communication; factory default is 1)

    Variables:
        - ``pressure``: last measured pressure
    """
    def connect_device(self):
        with self.using_devclass("KJL.KJL300",host=self.remote) as cls:
            self.device=cls(conn=self.conn,addr=self.addr)  # pylint: disable=not-callable
    def setup_task(self, conn, addr=1, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.addr=addr
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