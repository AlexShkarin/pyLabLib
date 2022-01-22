from ... import device_thread



class FWThread(device_thread.DeviceThread):
    """
    Thorlabs FW102/212 motorized filter wheel device thread.

    Device args:
        - ``conn``: device connection (usually, COM-port address)
        - ``version``: filter wheel version; can be either ``None`` (newer version with USB connection),
            or ``"v1"`` (older version, which has fewer commands and different communication strategy; also requires ``pcount`` set, if it is different from 6)
        - ``**kwargs``: additional arguments supplied on the device creation (e.g., ``respect_bounds`` or ``pcount`` for ``"v1"`` version)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``position``: last measured filter wheel position (starts from 1)
        - ``parameters``: main wheel parameters: speed mode, trigger mode, etc.

    Commands:
        - ``set_position``: set new filter position
    """
    def connect_device(self):
        devclass="Thorlabs.FWv1" if self.version=="v1" else "Thorlabs.FW"
        with self.using_devclass(devclass,host=self.remote) as cls:
            self.device=cls(conn=self.conn,**self.dev_kwargs)  # pylint: disable=not-callable
            self.device.get_position()
    def setup_task(self, conn, version=None, remote=None, **kwargs):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.version=version
        self.remote=remote
        self.dev_kwargs=kwargs
        self.add_job("update_measurements",self.update_measurements,.2)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_device_command("set_position",post_update="update_measurements")
    def update_measurements(self):
        if self.open():
            self.v["position"]=self.device.get_position()
        else:
            self.v["position"]=0


class MDT69xAThread(device_thread.DeviceThread):
    """
    Thorlabs MDT693A/4A high-voltage source device thread.

    Device args:
        - ``conn``: device connection (usually, COM-port address)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``voltage``: last measured output voltages for all 3 axes
        - ``parameters``: main voltage source parameters: maximal voltage, etc.

    Commands:
        - ``set_voltage``: set new output voltage
    """
    def connect_device(self):
        with self.using_devclass("Thorlabs.MDT69xA",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
            self.device.get_voltage()
    def setup_task(self, conn, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,.2)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_device_command("set_voltage",post_update="update_measurements")
    def update_measurements(self):
        if self.open():
            for ax in ["x","y","z"]:
                self.v["voltage",ax]=self.device.get_voltage(ax)
        else:
            for ax in ["x","y","z"]:
                self.v["voltage",ax]=0