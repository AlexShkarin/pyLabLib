from ... import device_thread



class PIE516Thread(device_thread.DeviceThread):
    """
    Physik Instrumente E-516 controller device thread.

    Device args:
        - ``conn``: serial connection parameters (usually port or a tuple containing port and baudrate)
        - ``default_axes``: default assumed when the device could not be connected; if the connection is established, ignore it and use device-provided axes
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``position``: last measured servo position
        - ``voltage``: current voltage
        - ``servo``: whether servo mode is on
        - ``drift_compensation``: whether drift compensation mode is on
        - ``velocity_control``: whether velocity limit mode is on
        - ``parameters``: main stage parameters: homing and velocity parameters, etc.

    Commands:
        - ``move_to``: move to a new position (only if servo mode is on)
        - ``set_voltage``: set output voltage (only if servo mode is off)
        - ``stop_motion``: stop motion
        - ``setup_motion``: setup motion parameters (servo mode, velocity limit, etc.)
    """
    def connect_device(self):
        with self.using_devclass("PhysikInstrumente.PIE516",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
            self.device.get_position()
    def setup_task(self, conn=None, default_axes=("A","B","C"), remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.default_axes=default_axes
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_command("move_to")
        self.add_command("stop_motion")
        self.add_command("set_voltage")
        self.add_command("setup_motion")
    def update_measurements(self):
        if self.open():
            self.v["position"]=self.device.get_position()
            self.v["voltage"]=self.device.get_voltage()
            self.v["servo"]=self.device.is_servo_enabled()
            self.v["drift_compensation"]=self.device.is_drift_compensation_enabled()
            self.v["velocity_control"]=self.device.is_velocity_control_enabled()
        else:
            for ax in self.default_axes:
                self.v["position",ax]=0
                self.v["voltage",ax]=0
                self.v["servo",ax]=False
                self.v["drift_compensation",ax]=False
                self.v["velocity_control",ax]=False
    
    def _stop_wait(self, axis="all"):
        self.device.stop(axis=None if axis=="all" else axis)
    def move_to(self, position, axis="all"):
        """Move to `position` (only if servo mode is on)"""
        if self.open():
            axis=None if axis=="all" else axis
            self._stop_wait(axis=axis)
            self.device.move_to(position,axis=axis)
            self.update_measurements()
    def stop_motion(self, axis="all"):
        """Stop motion at a given axis"""
        if self.open():
            self._stop_wait(axis=axis)
            self.update_measurements()
    def set_voltage(self, voltage, axis="all"):
        """Set output voltage (only if servo mode is off)"""
        if self.open():
            axis=None if axis=="all" else axis
            self._stop_wait(axis=axis)
            self.device.set_voltage(voltage,axis=axis)
            self.update_measurements()
    def setup_motion(self, servo=None, drift_compensation=None, velocity_control=None, velocity=None, axis="all"):
        """
        Setup motion parameters for the given axis.

        Any parameters set to ``None`` do not change.

        Args:
            servo: servo (position feedback) mode enabled or disabled
            drift_compensation: drift compensation mode enabled or disabled
            velocity_control: velocity limit mode enabled or disable (only matters if servo is on)
            velocity: velocity limit (only matters if servo and velocity are on)
        """
        if self.open():
            axis=None if axis=="all" else axis
            if servo is not None:
                self.device.enable_servo(servo,axis=axis)
            if drift_compensation is not None:
                self.device.enable_drift_compensation(drift_compensation,axis=axis)
            if velocity_control is not None:
                self.device.enable_velocity_control(velocity_control,axis=axis)
            if velocity is not None:
                self.device.set_velocity(velocity,axis=axis)
            self.update_parameters()
            self.update_measurements()



class PIE515Thread(device_thread.DeviceThread):
    """
    Physik Instrumente E-515 controller device thread.

    Device args:
        - ``conn``: serial connection parameters (usually port or a tuple containing port and baudrate)
        - ``default_axes``: default assumed when the device could not be connected; if the connection is established, ignore it and use device-provided axes
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``position``: last measured servo position
        - ``voltage``: current voltage
        - ``servo``: whether servo mode is on

    Commands:
        - ``move_to``: move to a new position (only if servo mode is on)
        - ``set_voltage``: set output voltage (only if servo mode is off)
        - ``setup_motion``: setup motion parameters (servo mode)
    """
    def connect_device(self):
        with self.using_devclass("PhysikInstrumente.PIE515",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
            self.device.get_position()
    def setup_task(self, conn=None, default_axes=(1,2,3), remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.default_axes=default_axes
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_command("move_to")
        self.add_command("set_voltage")
        self.add_command("setup_motion")
    def update_measurements(self):
        if self.open():
            axes=self.device.get_all_axes()
            self.v["position"]=dict(zip(axes,self.device.get_position(axis="all")))
            self.v["voltage"]=dict(zip(axes,self.device.get_voltage(axis="all")))
            self.v["servo"]=dict(zip(axes,self.device.is_servo_enabled(axis="all")))
        else:
            for ax in self.default_axes:
                self.v["position",ax]=0
                self.v["voltage",ax]=0
                self.v["servo",ax]=False
    
    def move_to(self, position, axis="all"):
        """Move to `position` (only if servo mode is on)"""
        if self.open():
            self.device.move_to(position,axis=axis)
            self.update_measurements()
    def set_voltage(self, voltage, axis="all"):
        """Set output voltage (only if servo mode is off)"""
        if self.open():
            self.device.set_voltage(voltage,axis=axis)
            self.update_measurements()
    def setup_motion(self, servo=None, axis="all"):
        """
        Setup motion parameters for the given axis.

        Any parameters set to ``None`` do not change.

        Args:
            servo: servo (position feedback) mode enabled or disabled
        """
        if self.open():
            if servo is not None:
                self.device.enable_servo(servo,axis=axis)
            self.update_parameters()
            self.update_measurements()