from ... import device_thread



class TMCM1110Thread(device_thread.DeviceThread):
    """
    Trinamic stepper motor controller TMCM-1110 controlled device thread.

    Device args:
        - ``conn``: serial connection parameters (usually port or a tuple containing port and baudrate)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``position``: last measured motor position
        - ``speed``: current speed
        - ``moving``: simplified status, which shows whether the device is moving at all
        - ``parameters``: main stage parameters: homing and velocity parameters, etc.

    Commands:
        - ``move_to``: move to a new position
        - ``move_by``: move by a given distance
        - ``set_position_reference``: set current position reference
        - ``jog``: start jogging into a given direction
        - ``stop_motion``: stop motion
        - ``set_velocity``: set maximal velocity and acceleration
    """
    def connect_device(self):
        with self.using_devclass("Trinamic.TMCM1110",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
            self.device.get_position()
    def setup_task(self, conn, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_command("move_to")
        self.add_command("move_by")
        self.add_command("set_position_reference")
        self.add_command("jog")
        self.add_command("home")
        self.add_command("stop_motion")
        self.add_command("set_velocity")
    def update_measurements(self):
        if self.open():
            self.v["position"]=self.device.get_position()
            self.v["speed"]=self.device.get_current_speed()
            self.v["moving"]=self.device.is_moving()
        else:
            self.v["position"]=0
            self.v["speed"]=0
            self.v["moving"]=False
    
    def _stop_wait(self):
        if self.device.is_moving():
            self.device.stop()
    def move_to(self, position):
        """Move to `position` (positive or negative)"""
        if self.open():
            self._stop_wait()
            self.device.move_to(position)
            self.update_measurements()
    def move_by(self, distance):
        """Move by `distance` (positive or negative)"""
        if self.open():
            self._stop_wait()
            self.device.move_by(distance)
            self.update_measurements()
    def set_position_reference(self, position=0):
        """Reference to a new position (assign current position to `position`)"""
        if self.open():
            self.device.set_position_reference(position)
            self.update_measurements()
    def jog(self, direction):
        """Start moving in a given direction (``"+"`` or ``"-"``)"""
        if self.open():
            self._stop_wait()
            self.device.jog(direction)
            self.update_measurements()
    def home(self, sync=True):
        """Home the motor and wait until the homing is done (if `sync` is ``True``)"""
        if self.open():
            self._stop_wait()
            self.device.home(wait=sync)
            self.update_measurements()
    def stop_motion(self):
        """Stop motion"""
        if self.open():
            self._stop_wait()
            self.update_measurements()
    def set_velocity(self, max_velocity, acceleration=None, pulse_divisor=None, ramp_divisor=None):
        """Set maximal motion velocity"""
        if self.open():
            self.device.setup_velocity(speed=max_velocity,accel=acceleration,pulse_divisor=pulse_divisor,ramp_divisor=ramp_divisor)
            self.update_parameters()



class TMCMx110Thread(device_thread.DeviceThread):
    """
    Trinamic multi-axis stepper motor controller TMCM-x110 (1110, 3110, 6110) thread.

    Device args:
        - ``conn``: serial connection parameters (usually port or a tuple containing port and baudrate)
        - ``naxes``: maximal number of axes to check for upon connection; if the actual number is larger, use only first ``naxes`` axes
        - ``ensure_naxes``: number of axes whose immediate parameters (position, speed, and movement status) are always present as thread variables,
            and are set to ``0`` or ``False`` if the corresponding axis is not connected;
            does not apply to more complicated parameters (e.g., homing parameter), which still will be missing
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``position/<ax>``: last measured motor position at the given axis
        - ``speed/<ax>``: current speed at the given axis
        - ``moving/<ax>``: simplified status, which shows whether the device is moving at all at the given axis
        - ``connected/<ax>``: whether the axis is connected at all
        - ``parameters``: main stage parameters: homing and velocity parameters, etc.

    Commands:
        - ``move_to``: move to a new position
        - ``move_by``: move by a given distance
        - ``set_position_reference``: set current position reference
        - ``jog``: start jogging into a given direction
        - ``stop_motion``: stop motion
        - ``set_velocity``: set maximal velocity and acceleration
    """
    def connect_device(self):
        with self.using_devclass("Trinamic.TMCMx110",host=self.remote) as cls:
            self.device=cls(conn=self.conn,naxes=self.naxes)  # pylint: disable=not-callable
            self.device.get_position()
    def setup_task(self, conn, naxes=None, ensure_naxes=0, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.naxes=naxes
        self.ensure_naxes=ensure_naxes
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_command("move_to")
        self.add_command("move_by")
        self.add_command("set_position_reference")
        self.add_command("jog")
        self.add_command("home")
        self.add_command("stop_motion")
        self.add_command("set_velocity")
    def update_measurements(self):
        naxes=0
        if self.open():
            naxes=len(self.device.get_all_axes())
            for ax in range(naxes):
                self.v["position",ax]=self.device.get_position(axis=ax)
                self.v["speed",ax]=self.device.get_current_speed(axis=ax)
                self.v["moving",ax]=self.device.is_moving(axis=ax)
                self.v["connected",ax]=True
        for ax in range(naxes,self.ensure_naxes):
            self.v["position",ax]=0
            self.v["speed",ax]=0
            self.v["moving",ax]=False
            self.v["connected",ax]=False
    
    def _stop_wait(self, axis=0):
        if self.device.is_moving(axis=axis):
            self.device.stop(axis=axis)
    def move_to(self, position, axis=0):
        """Move to `position` (positive or negative)"""
        if self.open():
            self._stop_wait(axis=axis)
            self.device.move_to(position,axis=axis)
            self.update_measurements()
    def move_by(self, distance, axis=0):
        """Move by `distance` (positive or negative)"""
        if self.open():
            self._stop_wait(axis=axis)
            self.device.move_by(distance,axis=axis)
            self.update_measurements()
    def set_position_reference(self, position=0, axis=0):
        """Reference to a new position (assign current position to `position`)"""
        if self.open():
            self.device.set_position_reference(position,axis=axis)
            self.update_measurements()
    def jog(self, direction, axis=0):
        """Start moving in a given direction (``"+"`` or ``"-"``)"""
        if self.open():
            self._stop_wait(axis=axis)
            self.device.jog(direction,axis=axis)
            self.update_measurements()
    def home(self, axis=0, sync=True):
        """Home the motor and wait until the homing is done (if `sync` is ``True``)"""
        if self.open():
            self._stop_wait(axis=axis)
            self.device.home(axis=axis,wait=sync)
            self.update_measurements()
    def stop_motion(self, axis=0):
        """Stop motion"""
        if self.open():
            self._stop_wait(axis=axis)
            self.update_measurements()
    def set_velocity(self, max_velocity, acceleration=None, pulse_divisor=None, ramp_divisor=None, axis=0):
        """Set maximal motion velocity"""
        if self.open():
            self.device.setup_velocity(speed=max_velocity,accel=acceleration,pulse_divisor=pulse_divisor,ramp_divisor=ramp_divisor,axis=axis)
            self.update_parameters()