from ... import device_thread



class KinesisMotorThread(device_thread.DeviceThread):
    """
    Thorlabs motor controller device thread.

    Device args:
        - ``conn``: serial connection parameters (usually an 8-digit device serial number)
        - ``**kwargs``: additional arguments supplied on the device creation (e.g., ``scale``)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``position``: last measured motor position
        - ``status``: last measured motor status (list containing valid status elements such as ``"moving_fw"`` or ``"sw_fw_lim"``)
        - ``moving``: simplified status, which shows whether the device is moving at all
        - ``parameters``: main stage parameters: homing and velocity parameters, etc.

    Commands:
        - ``move_to``: move to a new position
        - ``set_position_reference``: set current position reference
        - ``jog``: start jogging into a given direction
        - ``home``: home the stage
        - ``stop_motion``: stop motion
        - ``set_velocity``: set maximal velocity and acceleration
    """
    def connect_device(self):
        with self.using_devclass("Thorlabs.KinesisMotor",host=self.remote) as cls:
            self.device=cls(conn=self.conn,**self.dev_kwargs)
            self.device.get_position()
    def setup_task(self, conn, remote=None, **kwargs):
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.dev_kwargs=kwargs
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_command("move_to")
        self.add_command("set_position_reference")
        self.add_command("jog")
        self.add_command("home")
        self.add_command("stop_motion")
        self.add_command("set_velocity")
    def update_measurements(self):
        if self.open():
            self.v["position"]=self.device.get_position()
            self.v["status"]=self.device.get_status()
            self.v["moving"]=self.device.is_moving()
        else:
            self.v["position"]=0
            self.v["status"]=[]
            self.v["moving"]=False
    
    def _stop_wait(self):
        if self.device.is_moving():
            self.device.stop(sync=True)
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
    def home(self):
        """Home the device"""
        if self.open():
            self._stop_wait()
            self.device.home()
            self.update_measurements()
            self.update_parameters()
    def stop_motion(self):
        """Stop motion at a given axis"""
        if self.open():
            self._stop_wait()
            self.update_measurements()
    def set_velocity(self, max_velocity, acceleration=None):
        """Set maximal motion velocity"""
        if self.open():
            self.device.setup_velocity(max_velocity=max_velocity,acceleration=acceleration)
            self.update_parameters()




class MFFThread(device_thread.DeviceThread):
    """
    MFF (Motorized Filter Flip Mount) device device thread.

    Device args:
        - ``conn``: device connection (usually 8-digit device serial number)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``state``: last measured flipper state (0 or 1 if the state is definite, or ``None`` if moving)
        - ``parameters``: flip mirror parameters

    Commands:
        - ``move_to_state``: move to a new state
    """
    def connect_device(self):
        with self.using_devclass("Thorlabs.MFF",host=self.remote) as cls:
            self.device=cls(conn=self.conn,**self.dev_kwargs)
            self.device.get_state()
    def setup_task(self, conn, remote=None, **kwargs):
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.dev_kwargs=kwargs
        self.add_job("update_measurements",self.update_measurements,.2)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_device_command("move_to_state",post_update="update_measurements")
    def update_measurements(self):
        if self.open():
            self.v["state"]=self.device.get_state()
        else:
            self.v["state"]=0