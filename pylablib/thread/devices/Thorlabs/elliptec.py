from ... import device_thread
import contextlib
import warnings


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
        - ``axis_status/<addr>``: last measured device status
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
        self.add_command("move_to",limit_queue=("addr",1),on_full_queue="skip_oldest")
        self.add_command("move_by",limit_queue=("addr",1),on_full_queue="skip_oldest")
        self.add_command("home")
        self.add_command("set_velocity")
    def update_measurements(self):
        if self.open():
            self.v["position"]=self.device.get_position(addr="all")
            self.v["axis_status"]=self.device.get_status(addr="all")
        else:
            addrs=self.addrs or []
            self.v["position"]={a:0 for a in addrs}
            self.v["axis_status"]={a:"ok" for a in addrs}
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
    _dest_tolerance=0.1
    def _is_at_dest(self, dest, addr):
        pos=self.device.get_position(addr=addr)
        pos=pos.values() if isinstance(pos,dict) else [pos]
        return all(abs(p-dest)<self._dest_tolerance for p in pos)
    def _move_half_point(self, dest, addr):
        self.sleep(0.2)
        pos=self.device.get_position(addr=addr)
        if isinstance(pos,dict):
            for a,p in pos.items():
                if abs(p-dest)>self._dest_tolerance:
                    self.device.move_to((p+dest)/2,addr=a)
        else:
            self.device.move_to((pos+dest)/2,addr=addr)
        self.sleep(0.2)
    def move_to(self, position, addr=None):
        """Move to `position` (positive or negative)"""
        if self.open():
            with self._moving(addr):
                for i in range(3):
                    self.device.move_to(position,addr=addr)
                    if self._is_at_dest(position,addr=addr):
                        break
                    warnings.warn("warning: elliptec motor address {} failed {} times to move to {}, got position {} instead".format(addr,i+1,position,self.device.get_position(addr=addr)))
                    self._move_half_point(position,addr)
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