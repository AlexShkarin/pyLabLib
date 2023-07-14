from ... import device_thread



class Standa8SMCThread(device_thread.DeviceThread):
    """
    Generic Standa 8SMC4/8SMC5 controller device.

    Device args:
        - ``conn``: serial connection parameters (usually port or a tuple containing port and baudrate)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``position``: last measured motor position
        - ``encoder``: last measured encoder position
        - ``moving``: simplified status, which shows whether the device is moving at all
        - ``parameters``: main stage parameters: homing and velocity parameters, etc.

    Commands:
        - ``move_to``: move to a new position
        - ``move_by``: move by a given distance
        - ``set_position_reference``: set current position reference
        - ``set_position_reference``: set current position reference
        - ``jog``: start jogging into a given direction
        - ``stop_motion``: stop motion
        - ``set_velocity``: set maximal velocity and acceleration
    """
    def connect_device(self):
        with self.using_devclass("Standa.Standa8SMC",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
    def setup_task(self, conn, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_device_command("move_to",post_update="update_measurements")
        self.add_device_command("move_by",post_update="update_measurements")
        self.add_device_command("set_position_reference",post_update="update_measurements")
        self.add_device_command("set_encoder_reference",post_update="update_measurements")
        self.add_device_command("jog",post_update="update_measurements")
        self.add_device_command("stop_motion",command_name="stop",post_update="update_measurements")
        self.add_command("home")
        self.add_command("set_velocity")
    def update_measurements(self):
        if self.open():
            self.v["position"]=self.device.get_position()
            self.v["encoder"]=self.device.get_encoder()
            self.v["moving"]=self.device.is_moving()
        else:
            self.v["position"]=0
            self.v["encoder"]=0
            self.v["moving"]=False
    
    def _stop_wait(self):
        if self.device.is_moving():
            self.device.stop()
    def home(self):
        """Home the motor"""
        if self.open():
            if self.device.is_moving():
                self.device.stop()
            self.device.home(sync=False)
            self.update_measurements()
            self.device.wait_move(timeout=30.)
            self.update_measurements()
    def set_velocity(self, speed=None, accel=None, decel=None, antiplay=None):
        """Set motion parameters: maximal speed, acceleration, deceleration, anti-play"""
        if self.open():
            self.device.setup_move(speed=speed,accel=accel,decel=decel,antiplay=antiplay)
            self.update_parameters()