from ... import device_thread


class IPumpLaserThread(device_thread.DeviceThread):
    """
    Generic pump laser controller.

    Allows to switch the laser on and off, and to read the output power. 

    Device args:
        - ``conn``: device connection (usually, COM-port address)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``power``: current actual output laser power
        - ``enabled``: indicates whether the laser is on

    Commands:
        - ``enable``: enable or disable the laser output
    """
    _device_class=""
    def connect_device(self):
        with self.using_devclass(self._device_class,host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
            self.device.is_enabled()
    def setup_task(self, conn, remote=None):  # pylint: disable=arguments-differ
        self.conn=conn
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,1.)
        self.add_device_command("enable",post_update=None)

    def update_measurements(self):
        if self.open():
            self.v["power"]=self.device.get_output_power()
            self.v["enabled"]=self.device.is_enabled()
        else:
            self.v["power"]=-1
            self.v["enabled"]=False