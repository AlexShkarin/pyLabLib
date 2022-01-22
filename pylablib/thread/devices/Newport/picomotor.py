from ... import device_thread



class Picomotor8742Thread(device_thread.DeviceThread):
    """
    Picomotor 8742 controller device thread.

    Device args:
        - ``conn``: connection parameters; can be an index (starting from 0) for USB devices,
            or an IP address (e.g., ``"192.168.0.2"``) or host name (e.g., ``"8742-12345"``) for Ethernet devices
        - ``backend``: communication backend; by default, try to determine from the communication parameters
        - ``multiaddr``: if ``True``, assume that there are several daisy-chained devices connected to the current one;
            in this case, ``get_device_info`` and related methods return dictionaries ``{addr: value}`` for all connected controllers
            instead of simply values for the given controller
        - ``**kwargs``: additional arguments supplied on the device creation (e.g., ``scan``)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``position``: last measured motor position
        - ``moving``: indicator of whether axis is moving

    Commands:
        - ``move_to``: move the given axis to a new position
        - ``set_position_reference``: set current position reference at the given axis
        - ``move_by``: move the given axis by a given number of steps
        - ``jog``: start jogging the given axis into a given direction
        - ``stop_motion``: stop motion at the given axis
    """
    def connect_device(self):
        with self.using_devclass("Newport.Picomotor8742",host=self.remote) as cls:
            self.device=cls(conn=self.conn,backend=self.backend,multiaddr=self.multiaddr,**self.dev_kwargs)  # pylint: disable=not-callable
            self.device.is_moving()
    def setup_task(self, conn, backend="auto", multiaddr=False, remote=None, **kwargs):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.backend=backend
        self.multiaddr=multiaddr
        self.remote=remote
        self.dev_kwargs=kwargs
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_command("move_to")
        self.add_command("set_position_reference")
        self.add_command("move_by")
        self.add_command("jog")
        self.add_command("stop_motion")

    def update_measurements(self):
        axes=[1,2,3,4]
        if self.open():
            positions=self.rpyc_obtain(self.device.get_position(axis="all",addr="all"))
            moving=self.rpyc_obtain(self.device.is_moving(axis="all",addr="all"))
        else:
            positions={1:[0]*len(axes)} if self.multiaddr else [0]*len(axes)
            moving={1:[False]*len(axes)} if self.multiaddr else [False]*len(axes)
        if self.multiaddr:
            positions={addr:dict(zip(axes,vals)) for addr,vals in positions.items()}
            moving={addr:dict(zip(axes,vals)) for addr,vals in moving.items()}
        else:
            positions=dict(zip(axes,positions))
            moving=dict(zip(axes,moving))
        self.v["position"]=positions
        self.v["moving"]=moving
    
    def _stop_wait(self, axis="all", addr=None):
        self.device.stop(axis=axis,addr=addr)
    def move_to(self, axis, position, addr=None):
        """Move a given axis to a given position"""
        if self.open():
            self._stop_wait(axis=axis,addr=addr)
            self.device.move_to(axis,position,addr=addr)
            self.update_measurements()
    def set_position_reference(self, axis, position=0, addr=None):
        """Move a given axis to a given position"""
        if self.open():
            self.device.set_position_reference(axis,position,addr=addr)
            self.update_measurements()
    def move_by(self, axis, steps, addr=None):
        """Move a given axis for a given number of steps"""
        if self.open():
            self._stop_wait(axis=axis,addr=addr)
            self.device.move_by(axis,steps,addr=addr)
            self.update_measurements()
    def jog(self, axis, direction, addr=None):
        """Jog a given axis in a given direction"""
        if self.open():
            self._stop_wait(axis=axis,addr=addr)
            self.device.jog(axis,direction,addr=addr)
            self.update_measurements()
    def stop_motion(self, axis, addr=None):
        """Stop motion at a given axis"""
        if self.open():
            self._stop_wait(axis=axis,addr=addr)
            self.update_measurements()