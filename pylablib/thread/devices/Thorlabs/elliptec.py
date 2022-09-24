from ... import device_thread
import contextlib


class ElliptecMotorThread(device_thread.DeviceThread):
    """
    Thorlabs Elliptec stage device thread.

    Device args:
        - ``conn``: serial connection parameters (usually port or a tuple containing port and baudrate)
        - ``addrs``: list of device addresses (between 0 and 15) connected to this serial port; if ``"all"``, automatically detect all connected devices
        - ``**kwargs``: additional arguments supplied on the device creation (e.g., ``scale``)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``position/<addr>``: last measured motor position
        - ``status/<addr>``: last measured device status
        - ``moving/<addr>``: whether the given axis is moving

    Commands:
        - ``move_to``: move to a new position
        - ``move_by``: move by a new distance
        - ``home``: home the stage
        - ``set_velocity``: set velocity in percent from the maximum
    """
    def connect_device(self):
        with self.using_devclass("Thorlabs.ElliptecMotor",host=self.remote) as cls:
            self.device=cls(conn=self.conn,addrs=self.addrs,**self.dev_kwargs)  # pylint: disable=not-callable
            self.addrs=self.device.get_connected_addrs()
            self.v["moving"]={a:False for a in self.addrs}
    def setup_task(self, conn, addrs="all", remote=None, **kwargs):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.addrs=addrs
        self.remote=remote
        self.dev_kwargs=kwargs
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_command("move_to")
        self.add_command("move_by")
        self.add_command("home")
        self.add_command("set_velocity")
    def update_measurements(self):
        if self.open():
            self.v["position"]=self.device.get_position(addr="all")
            self.v["status"]=self.device.get_status(addr="all")
        else:
            addrs=self.addrs or []
            self.v["position"]={a:0 for a in addrs}
            self.v["status"]={a:"ok" for a in addrs}
            self.v["moving"]={a:False for a in addrs}
    
    @contextlib.contextmanager
    def _moving(self, addr):
        addr=self.device.get_default_addr() if addr is None else addr
        addr=self.device.get_connected_addrs() if addr=="all" else [addr]
        for a in addr:
            self.v["moving",a]=True
        try:
            yield
        finally:
            for a in addr:
                self.v["moving",a]=False
    def move_to(self, position, addr=None):
        """Move to `position` (positive or negative)"""
        if self.open():
            with self._moving(addr):
                self.device.move_to(position,addr=addr)
            self.update_measurements()
    def move_by(self, distance, addr=None):
        """Move by `distance` (positive or negative)"""
        if self.open():
            with self._moving(addr):
                self.device.move_by(distance,addr=addr)
            self.update_measurements()
    def home(self, home_dir="cw", addr=None):
        """Home the device"""
        if self.open():
            with self._moving(addr):
                self.device.home(home_dir=home_dir,addr=addr)
            self.update_measurements()
    def set_velocity(self, velocity=100, addr=None):
        """Set velocity as a percentage from the maximal velocity (0 to 100)"""
        if self.open():
            self.device.set_velocity(velocity,addr=addr)
            self.update_measurements()