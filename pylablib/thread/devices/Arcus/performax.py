from ... import device_thread
from ....core.utils import funcargparse



class PerformaxThread(device_thread.DeviceThread):
    """
    Arcus Performax 4EX/4ET or 2EX/2ED translation stage device thread.

    Device args:
        - ``idx``: stage index
        - ``enable``: if ``True``, enable all axes on startup
        - ``kind``: stage kind; can be either ``"4EX"`` (4-axis stage) or ``"2EX"`` (2-axis stage)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``position``: last measured motor position; one per axis
        - ``status``: last measured motor status (list containing valid status elements such as ``"moving"`` or ``"sw_plus_lim"``); one per axis
        - ``speed``: current speed; one per axis
        - ``moving``: simplified status, which shows whether the device is moving at all; one per axis
        - ``parameters``: main stage parameters: homing and velocity parameters, etc.

    Commands:
        - ``move_to``: move the given axis to a new position
        - ``set_position_reference``: set current position reference at the given axis
        - ``jog``: start jogging the given axis into a given direction
        - ``home``: home the given axis
        - ``stop_motion``: stop motion at the given axis
        - ``set_velocity``: set maximal velocity at the given axis
    """
    def connect_device(self):
        cls_name="Arcus.Performax4EXStage" if self.kind=="4EX" else "Arcus.Performax2EXStage"
        with self.using_devclass(cls_name,host=self.remote) as cls:
            self.device=cls(idx=self.idx,enable=self.enable)
            self.device.get_position()
    def setup_task(self, idx=0, enable=True, kind="4EX", remote=None):
        funcargparse.check_parameter_range(kind,"kind",["4EX","2EX"])
        self.device_reconnect_tries=5
        self.idx=idx
        self.kind=kind
        self.enable=enable
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_command("move_to")
        self.add_command("set_position_reference")
        self.add_command("jog")
        self.add_command("home")
        self.add_command("stop_motion")
        self.add_command("set_velocity")
    def update_measurements(self):
        axes="XYZU" if self.kind=="4EX" else "XY"
        if self.open():
            for ax in axes:
                self.v["position",ax]=self.device.get_position(axis=ax)
                self.v["status",ax]=self.device.get_status(axis=ax)
                self.v["speed",ax]=self.device.get_current_axis_speed(axis=ax)
                self.v["moving",ax]=self.device.is_moving(axis=ax)
        else:
            for ax in axes:
                self.v["position",ax]=0
                self.v["status",ax]=[]
                self.v["speed",ax]=0
                self.v["moving",ax]=False
    
    def _stop_wait(self, axis="all"):
        axes=self.device.get_all_axes() if axis=="all" else [axis]
        if any(self.device.is_moving(ax) for ax in axes):
            self.device.stop(axis=axis)
            for ax in axes:
                while self.device.is_moving(ax):
                    self.sleep(0.05)
    def move_to(self, axis, position):
        """Move to `position` (positive or negative)"""
        if self.open():
            self._stop_wait(axis=axis)
            self.device.clear_limit_error(axis)
            self.device.move_to(axis,position)
            self.update_measurements()
    def set_position_reference(self, axis, position=0):
        """Reference to a new position (assign current position to `position`)"""
        if self.open():
            self.device.set_position_reference(axis,position)
            self.update_measurements()
    def jog(self, axis, direction):
        """Start moving in a given direction (``"+"`` or ``"-"``)"""
        if self.open():
            self._stop_wait(axis=axis)
            self.device.clear_limit_error(axis)
            self.device.jog(axis,direction)
            self.update_measurements()
    def home(self, axis, direction, home_mode):
        """Home the axis"""
        if self.open():
            self._stop_wait(axis=axis)
            self.device.home(axis,direction,home_mode)
            self.update_measurements()
            self.update_parameters()
    def stop_motion(self, axis="all"):
        """Stop motion at a given axis"""
        if self.open():
            self._stop_wait(axis=axis)
            self.update_measurements()
    def set_velocity(self, max_velocity, axis="all"):
        """Set maximal motion velocity"""
        if self.open():
            if axis=="all":
                self.device.set_axis_speed("all",0)
                self.device.set_global_speed(max_velocity)
            else:
                self.device.set_axis_speed(axis,max_velocity)
            self.update_parameters()