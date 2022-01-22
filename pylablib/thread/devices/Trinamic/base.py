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
        self.add_command("set_position_reference")
        self.add_command("jog")
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