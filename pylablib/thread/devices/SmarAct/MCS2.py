from ... import device_thread



class MCS2Thread(device_thread.DeviceThread):
    """
    SmarAct MCS2 translation stage controller.

    Args:
        locator(str): controller locator (returned by :func:`get_devices_number` function)

    Device args:
        - ``locator``: controller locator (e.g., ``"network:sn:MCS2-00000001"`)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``axis_status``: last measured motor axis status (such as ``"stopped"`` or ``"moving"``); one per axis (integer index starting from 0)
        - ``moving``: indicator of whether axis is moving; one per axis (integer index starting from 0)
        - ``position``: measured position (of ``None`` if no position sensor is present); one per axis (integer index starting from 0)

    Commands:
        - ``move_to``: move the given axis to a given position (in m or deg)
        - ``move_by``: move the given axis by a given distance (in m or deg)
        - ``move_by_steps``: move the given axis by a given number of steps
        - ``stop_motion``: stop motion at the given axis
    """
    def connect_device(self):
        with self.using_devclass("SmarAct.MCS2",host=self.remote) as cls:
            self.device=cls(locator=self.locator)  # pylint: disable=not-callable
            self.axes=self.device.get_all_axes()
    def setup_task(self, locator, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.locator=locator
        self.axes=[]
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,.1)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_device_command("move_to",post_update="update_measurements")
        self.add_device_command("move_by",post_update="update_measurements")
        self.add_device_command("move_by_steps",post_update="update_measurements")
        self.add_device_command("stop_motion",command_name="stop",post_update="update_measurements")

    def update_measurements(self):
        if self.open():
            self.axes=self.device.get_all_axes()
            for ax in self.axes:
                self.v["axis_status",ax]=self.device.get_status(axis=ax)
                self.v["moving",ax]=self.device.is_moving(axis=ax)
                self.v["position",ax]=self.device.get_position(axis=ax)
        else:
            for ax in self.axes:
                self.v["axis_status",ax]="stopped"
                self.v["moving",ax]=False
                self.v["position",ax]=None