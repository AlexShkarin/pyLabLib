from ... import device_thread



class ANC350Thread(device_thread.DeviceThread):
    """
    Attocube ANC350 controller device thread.

    Device args:
        - ``conn``: connection parameters - index of the Attocube ANC350 in the system (for a single controller leave 0)
        - ``**kwargs``: additional arguments supplied on the device creation (e.g., ``timeout``)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``connected``: indicator of whether axis is connected
        - ``enabled``: indicator of whether axis is enabled
        - ``position``: last measured motor position
        - ``axis_status``: last measured axis status (list containing valid status elements such as ``"running"`` or ``"limit"``)
        - ``moving``: indicator of whether axis is moving
        - ``capacitance``: last measured capacitance

    Commands:
        - ``enable``: enable or disable the given axis
        - ``move_to``: move the given axis to a new position
        - ``move_by_steps``: move the given axis by a given number of steps
        - ``stop_motion``: stop motion at the given axis
        - ``set_axis_parameters``: set parameters (voltage, frequency, offset) for a given axis
    """
    def connect_device(self):
        with self.using_devclass("Attocube.ANC350",host=self.remote) as cls:
            self.device=cls(conn=self.conn,**self.dev_kwargs)  # pylint: disable=not-callable
            self.device.is_enabled()
    def setup_open_device(self):
        self.device.get_capacitance(measure=True)
        return super().setup_open_device()
    def setup_task(self, conn=0, remote=None, **kwargs):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.dev_kwargs=kwargs
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_command("enable")
        self.add_command("move_to")
        self.add_command("move_by_steps")
        self.add_command("jog")
        self.add_command("stop_motion")
        self.add_command("set_axis_parameters")

    def update_measurements(self):
        axes=[0,1,2]
        if self.open():
            for ax in axes:
                self.v["connected",ax]=self.device.is_connected(axis=ax)
                self.v["enabled",ax]=self.device.is_enabled(axis=ax)
                self.v["position",ax]=self.device.get_position(axis=ax)
                self.v["axis_status",ax]=self.device.get_status(axis=ax)
                self.v["moving",ax]=self.device.is_moving(axis=ax)
                self.v["capacitance",ax]=self.device.get_capacitance(axis=ax)
        else:
            for ax in axes:
                self.v["connected",ax]=False
                self.v["enabled",ax]=False
                self.v["position",ax]=0
                self.v["axis_status",ax]=[]
                self.v["moving",ax]=False
                self.v["capacitance",ax]=0
    
    def _stop_wait(self, axis="all"):
        axes=self.device.get_all_axes() if axis=="all" else [axis]
        if any(self.device.is_moving(ax) for ax in axes):
            self.device.stop(axis=axis)
            for ax in axes:
                while self.device.is_moving(ax):
                    self.sleep(0.05)
    def enable(self, axis="all", enable=True):
        """Enable or disable a given axis"""
        if self.open():
            self._stop_wait(axis=axis)
            self.device.enable_axis(axis,enable)
            self.update_measurements()
    def move_to(self, axis, position):
        """Move to `position` (positive or negative)"""
        if self.open():
            self._stop_wait(axis=axis)
            self.device.move_to(axis,position)
            self.update_measurements()
    def move_by_steps(self, axis, steps):
        """Move along a given axis by a given number of steps"""
        if self.open():
            self._stop_wait(axis=axis)
            self.device.move_by_steps(axis,steps)
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