from ... import device_thread
import contextlib
import warnings

import time


class ElliptecMotorThread(device_thread.DeviceThread):
    """
    Thorlabs Elliptec stage device thread.

    Device args:
        - ``conn``: serial connection parameters (usually port or a tuple containing port and baudrate)
        - ``addrs``: list of device addresses (between 0 and 15) connected to this serial port; if ``"all"``, automatically detect all connected devices
        - ``dest_tolerance``: destination position tolerance (either a single value, or a dictionary ``{addr: value}``); if after moving the stage position
            is more than ``dest_tolerance`` away from the target, re-issue the movement command
        - ``ensure_addrs``: list of device addresses which are ensured to be in the description; if a stage at a given address is empty,
            still specify is parameters but set them into "default" values (e.g., position of 0); in contrast if an address in ``addrs`` is not connected,
            the corresponding parameter values are not set up at all.
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
            self.ensure_addrs=[a for a in self.ensure_addrs if a not in self.addrs]
            self.v["moving"]={a:False for a in self.addrs+self.ensure_addrs}
            self.v["axis_connected"]={a:(a in self.addrs) for a in self.addrs+self.ensure_addrs}
    def setup_task(self, conn, addrs="all", dest_tolerance=0.1, ensure_addrs=None, remote=None, **kwargs):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.addrs=addrs
        self.ensure_addrs=([] if addrs=="all" else addrs) if ensure_addrs is None else ensure_addrs
        self.remote=remote
        self.dev_kwargs=kwargs
        self.dest_tolerance=dest_tolerance
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_command("move_to",limit_queue=("addr",5),on_full_queue="skip_oldest")
        self.add_command("move_by",limit_queue=("addr",5),on_full_queue="skip_oldest")
        self.add_command("home")
        self.add_command("set_velocity")
    def _open_addr(self, addr=None):
        if not self.open():
            return False
        return addr is None or addr=="all" or addr in self.addrs
    def update_measurements(self):
        if self.open():
            position=self.device.get_position(addr="all")
            axis_status=self.device.get_status(addr="all")
            for a in self.addrs+self.ensure_addrs:
                self.v["position",a]=position.get(a,0)
                self.v["axis_status",a]=axis_status.get(a,"ok")
        else:
            addrs=self.ensure_addrs if self.addrs=="all" else self.addrs+self.ensure_addrs
            self.v["position"]={a:0 for a in addrs}
            self.v["axis_status"]={a:"ok" for a in addrs}
            self.v["moving"]={a:False for a in addrs}
            self.v["axis_connected"]={a:False for a in addrs}
    
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
    _default_dest_tolerance=0.1
    def _get_dest_tolerance(self, addr):
        if isinstance(self.dest_tolerance,dict):
            return self.dest_tolerance.get(addr,self.dest_tolerance.get(None,self._default_dest_tolerance))
        return self.dest_tolerance
    def _is_at_dest(self, dest, addr):
        pos=self.device.get_position(addr=addr)
        pos=pos.values() if isinstance(pos,dict) else [pos]
        return all(abs(p-dest)<self._get_dest_tolerance(addr) for p in pos)
    def _move_half_point(self, dest, addr):
        self.sleep(0.2)
        pos=self.device.get_position(addr=addr)
        if isinstance(pos,dict):
            for a,p in pos.items():
                if abs(p-dest)>self._get_dest_tolerance(addr):
                    self.device.move_to((p+dest)/2,addr=a)
        else:
            self.device.move_to((pos+dest)/2,addr=addr)
        self.sleep(0.2)
    def move_to(self, position, addr=None, update=True):
        """Move to `position` (positive or negative)"""
        if self._open_addr(addr):
            with self._moving(addr):
                for i in range(3):
                    try:
                        self.device.move_to(position,addr=addr)
                        if self._is_at_dest(position,addr=addr):
                            break
                        warnings.warn("warning: elliptec motor address {} failed {} times to move to {}, got position {} instead".format(addr,i+1,position,self.device.get_position(addr=addr)))
                        self._move_half_point(position,addr)
                    except self.device.Error as err:
                        warnings.warn("warning: movement caused an error {}; reconnecting".format(err))
                        self.device.close()
                        time.sleep(1.)
                        self.device.open()
            if update:
                self.update_measurements()
    def move_by(self, distance, addr=None):
        """Move by `distance` (positive or negative)"""
        if self._open_addr(addr):
            with self._moving(addr):
                self.device.move_by(distance,addr=addr)
            self.update_measurements()
    def home(self, home_dir="cw", addr=None):
        """Home the device"""
        if self._open_addr(addr):
            with self._moving(addr):
                self.device.home(home_dir=home_dir,addr=addr)
            self.update_measurements()
    def set_velocity(self, velocity=100, addr=None):
        """Set velocity as a percentage from the maximal velocity (0 to 100)"""
        if self._open_addr(addr):
            self.device.set_velocity(velocity,addr=addr)
            self.update_measurements()