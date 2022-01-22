from ... import device_thread



class ANC300Thread(device_thread.DeviceThread):
    """
    Attocube ANC300 controller device thread.

    Device args:
        - ``conn``: connection parameters; for Ethernet connection is a tuple ``(addr, port)``, a string ``"addr:port"``, or a string ``"addr"`` (default port 7240 us assumed)
        - ``backend``: communication backend; by default, try to determine from the communication parameters
        - ``**kwargs``: additional arguments supplied on the device creation (e.g., ``pwd``)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``mode``: output modes of all axes
        - ``enabled``: indicator of whether axis is enabled
        - ``output``: current output voltage
        - ``capacitance``: last measured capacitance
        - ``parameters``: main stage parameters: frequency, amplitude, etc.

    Commands:
        - ``enable``: enable or disable the given axis
        - ``move_by``: move the given axis by a given number of steps
        - ``jog``: continuously jog the given axis in the given direction
        - ``stop_motion``: stop motion at the given axis
        - ``set_axis_parameters``: set parameters (voltage, frequency, offset) for a given axis
    """
    def connect_device(self):
        with self.using_devclass("Attocube.ANC300",host=self.remote) as cls:
            self.device=cls(conn=self.conn,**self.dev_kwargs)  # pylint: disable=not-callable
            self.device.is_enabled()
    def setup_task(self, conn, backend="auto", remote=None, **kwargs):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.backend=backend
        self.remote=remote
        self.dev_kwargs=kwargs
        self.add_job("update_measurements",self.update_measurements,.2)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_command("enable")
        self.add_command("move_by")
        self.add_command("jog")
        self.add_command("stop_motion")
        self.add_command("set_axis_parameters")

    def update_measurements(self):
        if self.open():
            self.v["mode"]=self.rpyc_obtain(self.device.get_mode())
            self.v["enabled"]=self.rpyc_obtain(self.device.is_enabled())
            self.v["output"]=self.rpyc_obtain(self.device.get_output())
            self.v["capacitance"]=self.rpyc_obtain(self.device.get_capacitance())
    
    def _stop_wait(self, axis="all"):
        axes=self.device.get_all_axes() if axis=="all" else [axis]
        if any(self.device.is_moving(ax) for ax in axes):
            self.device.stop(axis=axis)
            for ax in axes:
                while self.device.is_moving(ax):
                    self.sleep(0.05)
    def enable(self, axis="all", enable=True, mode="stp"):
        """Enable or disable a given axis"""
        if self.open():
            self._stop_wait(axis=axis)
            self.device.set_mode(axis,mode=mode if enable else "gnd")
            self.update_measurements()
    def move_by(self, axis, steps):
        """Move a given axis for a given number of steps"""
        if self.open():
            self._stop_wait(axis=axis)
            self.device.move_by(axis,steps)
            self.update_measurements()
    def jog(self, axis, direction):
        """Start moving in a given direction (``"+"`` or ``"-"``)"""
        if self.open():
            self._stop_wait(axis=axis)
            self.device.jog(axis,direction)
            self.update_measurements()
    def stop_motion(self, axis):
        """Stop motion at a given axis"""
        if self.open():
            self._stop_wait(axis=axis)
            self.update_measurements()
    def set_axis_parameters(self, voltage=None, frequency=None, offset=None, axis="all"):
        """Move to `position` (positive or negative)"""
        if self.open():
            self._stop_wait(axis=axis)
            if voltage is not None:
                self.device.set_voltage(axis,voltage)
            if frequency is not None:
                self.device.set_frequency(axis,frequency)
            if offset is not None:
                self.device.set_offset(axis,offset)
            self.update_parameters()