from ... import device_thread



class KinesisMotorThread(device_thread.DeviceThread):
    """
    Thorlabs motor controller device thread.

    Device args:
        - ``conn``: serial connection parameters (usually an 8-digit device serial number)
        - ``**kwargs``: additional arguments supplied on the device creation (e.g., ``scale``)
        - ``move_precision``: if not ``None``, can specify a move command precision;
            if the current position is more than ``move_precision`` away from the last entered target and the motor is stopped, reinitialize the movement.
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``position``: last measured motor position
        - ``axis_status``: last measured motor axis status (list containing valid status elements such as ``"moving_fw"`` or ``"sw_fw_lim"``)
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
            self.device=cls(conn=self.conn,**self.dev_kwargs)  # pylint: disable=not-callable
            self.device.get_position()
    def setup_task(self, conn, remote=None, move_precision=None, **kwargs):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.move_precision=move_precision
        self._last_move_to=None
        self.dev_kwargs=kwargs
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_command("move_to")
        self.add_command("set_position_reference")
        self.add_command("jog")
        self.add_command("home")
        self.add_command("stop_motion")
        self.add_command("set_velocity")
    def _check_move_precision(self):
        if (self.move_precision is not None) and (self._last_move_to is not None) and (not self.v["moving"]):
            if abs(self.v["position"]-self._last_move_to)>self.move_precision:
                self.move_to(self._last_move_to)
            else:
                self._last_move_to=None
    def update_measurements(self):
        if self.open():
            self.v["position"]=self.device.get_position()
            self.v["axis_status"]=self.device.get_status()
            self.v["moving"]=self.device.is_moving()
            self._check_move_precision()
        else:
            self.v["position"]=0
            self.v["axis_status"]=[]
            self.v["moving"]=False
    
    def _stop_wait(self, reset_move_to=True):
        if self.device.is_moving():
            self.device.stop(sync=True)
        if reset_move_to:
            self._last_move_to=None
    def move_to(self, position):
        """Move to `position` (positive or negative)"""
        if self.open():
            self._stop_wait()
            self.device.move_to(position)
            self._last_move_to=position
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



class KinesisPiezoMotorThread(device_thread.DeviceThread):
    """
    Thorlabs piezo motor controller device thread.

    Device args:
        - ``conn``: serial connection parameters (usually an 8-digit device serial number)
        - ``**kwargs``: additional arguments supplied on the device creation (e.g., ``default_channel``)
        - ``default_channels``: number of channels used by default if the device could not be connected
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``position``: last measured motor position
        - ``axis_status``: last measured motor axis status (list containing valid status elements such as ``"moving_fw"`` or ``"sw_fw_lim"``)
        - ``moving``: simplified status, which shows whether the device is moving at all
        - ``parameters``: main stage parameters: homing and velocity parameters, etc.

    Commands:
        - ``move_to``: move to a new position
        - ``set_position_reference``: set current position reference
        - ``jog``: start jogging into a given direction
        - ``stop_motion``: stop motion
        - ``setup_drive``: set maximal velocity and acceleration, as well as the drive voltage
    """
    def connect_device(self):
        with self.using_devclass("Thorlabs.KinesisPiezoMotor",host=self.remote) as cls:
            self.device=cls(conn=self.conn,**self.dev_kwargs)  # pylint: disable=not-callable
            self.device.get_position()
    def setup_task(self, conn, remote=None, default_channels=1, **kwargs):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.dev_kwargs=kwargs
        self.default_channels=default_channels
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_command("move_to")
        self.add_command("set_position_reference")
        self.add_command("move_by")
        self.add_command("jog")
        self.add_command("stop_motion")
        self.add_command("setup_drive")
    def update_measurements(self):
        if self.open():
            for ch in self.device.get_all_axes():
                self.v["position",ch]=self.device.get_position(channel=ch)
                self.v["axis_status",ch]=self.device.get_status(channel=ch)
                self.v["moving",ch]=self.device.is_moving(channel=ch)
        else:
            for ch in range(1,self.default_channels+1):
                self.v["position",ch]=0
                self.v["axis_status",ch]=[]
                self.v["moving",ch]=False
    
    def _stop_wait(self, channel=None):
        if self.device.is_moving(channel=channel):
            self.device.stop(channel=channel,sync=True)
    def move_to(self, position, channel=None):
        """Move to `position` (positive or negative) at a given channel"""
        if self.open():
            self._stop_wait(channel=channel)
            self.device.move_to(position,channel=channel)
            self.update_measurements()
    def set_position_reference(self, position=0, channel=None):
        """Reference to a new position (assign current position to `position`) on a given channel"""
        if self.open():
            self.device.set_position_reference(position,channel=channel)
            self.update_measurements()
    def move_by(self, distance, channel=None):
        """Move by `distance` (positive or negative) at a given channel"""
        if self.open():
            self._stop_wait(channel=channel)
            self.device.move_by(distance,channel=channel)
            self.update_measurements()
    def jog(self, direction, channel=None):
        """Start moving in a given direction (``"+"`` or ``"-"``) on a given channel"""
        if self.open():
            self._stop_wait(channel=channel)
            self.device.jog(direction,channel=channel)
            self.update_measurements()
    def stop_motion(self, channel=None):
        """Stop motion at a given channel"""
        if self.open():
            self._stop_wait(channel=channel)
            self.update_measurements()
    def setup_drive(self, velocity=None, voltage=None, acceleration=None, channel=None):
        """Set maximal motion velocity, maximal voltage, and acceleration on a given channel"""
        if self.open():
            self.device.setup_velocity(max_voltage=voltage,velocity=velocity,acceleration=acceleration,channel=channel)
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
            self.device=cls(conn=self.conn,**self.dev_kwargs)  # pylint: disable=not-callable
            self.device.get_state()
    def setup_task(self, conn, remote=None, **kwargs):  # pylint: disable=arguments-differ
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



class ThorlabsKinesisQuadDetectorThread(device_thread.DeviceThread):
    """
    Thorlabs Kinesis quadrature detector thread.

    Device args:
        - ``conn``: serial connection parameters (usually an 8-digit device serial number)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``readings``: last measured sensor readings
        - ``parameters``: device parameters: pid gains, mode, output parameters, etc.
    
    Commands:
        - ``set_operation_mode``: set operation mode (typically either ``"open_loop"`` or ``"closed_loop"``)
        - ``set_manual_output``: set manual outputs in the open loop mode
    """
    default_parameter_values={"enabled":False}
    parameter_variables=default_parameter_values.keys()
    def connect_device(self):
        with self.using_devclass("Thorlabs.KinesisQuadDetector",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
            self.device.get_readings()
    def setup_task(self, conn, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,.2)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_command("set_operation_mode")
        self.add_command("set_manual_output")
    def update_measurements(self):
        """Update current measurements"""
        if self.open():
            self.v["readings"]=self.device.get_readings()._asdict()
            self.v["mode"]=self.device.get_operation_mode()
        else:
            for k in ["xdiff","ydiff","sum","xout","yout"]:
                self.v["readings",k]=0
            self.v["mode"]="open_loop"
            self.sleep(1.)
    
    def set_operation_mode(self, mode):
        """Set current operation mode: ``"monitor"``, ``"open_loop"``, ``"closed_loop"``, or ``"auto_loop"``"""
        if self.open():
            self.device.set_operation_mode(mode)
            self.update_measurements()
    def set_manual_output(self, xpos=None, ypos=None, set_open_loop=True):
        """
        Set current manual output values (used in open loop mode).
        
        If ``set_open_loop==True``, explicitly move the device into the open loop mode first.
        """
        if self.open():
            if set_open_loop:
                self.device.set_operation_mode("open_loop")
            self.device.set_manual_output(xpos=xpos,ypos=ypos)
            self.update_measurements()