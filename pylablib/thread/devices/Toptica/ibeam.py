from ..generic import lasers


class TopticaIBeamThread(lasers.IPumpLaserThread):
    """
    Generic pump laser controller.

    Allows to switch the laser on and off, and to read the output power. 

    Device args:
        - ``conn``: device connection (usually, COM-port address)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``enabled``: whether the laser is enabled
        - ``channel_enabled``: whether specific channel is enabled
        - ``channel_power``: specified channel power
        - ``power``: current actual output laser power

    Commands:
        - ``enable``: enable or disable the laser output
        - ``enable_channel``: enable or disable specific channel
        - ``set_channel_power``: set channel power (in W)
    """
    def connect_device(self):
        with self.using_devclass("Toptica.TopticaIBeam",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
            self.device.is_enabled()
    def setup_task(self, conn, remote=None):
        self.conn=conn
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,1.)
        self.add_device_command("enable",post_update="update_measurements")
        self.add_device_command("enable_channel",post_update="update_measurements")
        self.add_device_command("set_channel_power",post_update="update_measurements")

    def update_measurements(self):
        if self.open():
            self.v["enabled"]=self.device.is_enabled()
            self.v["channel_enabled"]=self.device.is_channel_enabled()
            self.v["channel_power"]=self.device.get_channel_power()
            self.v["power"]=self.device.get_output_power()
        else:
            self.v["enabled"]=False
            self.v["channel_enabled"]=[False]*5
            self.v["channel_power"]=[-1]*5
            self.v["power"]=-1