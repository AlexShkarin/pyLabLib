from ... import device_thread



class SCU3DThread(device_thread.DeviceThread):
    """
    SmarAct SCU3D translation stage controller.

    Device args:
        - ``idx``: stage index
        - ``**kwargs``: additional arguments supplied on the device creation (e.g., ``axis_dir``)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``axis_status``: last measured motor axis status (such as ``"stopped"`` or ``"moving"``); one per axis
        - ``moving``: indicator of whether axis is moving; one per axis

    Commands:
        - ``move_by``: move the given axis by a given number of steps of the given size
        - ``stop_motion``: stop motion at the given axis
    """
    def connect_device(self):
        with self.using_devclass("SmarAct.SCU3D",host=self.remote) as cls:
            self.device=cls(idx=self.idx,**self.dev_kwargs)  # pylint: disable=not-callable
            self.device.get_status()
    def setup_task(self, idx=0, remote=None, **kwargs):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.idx=idx
        self.remote=remote
        self.dev_kwargs=kwargs
        self.add_job("update_measurements",self.update_measurements,.2)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_command("move_by")
        self.add_command("stop_motion")

    def update_measurements(self):
        axes=["x","y","z"]
        if self.open():
            for ax in axes:
                self.v["axis_status",ax]=self.device.get_status(axis=ax)
                self.v["moving",ax]=self.device.is_moving(axis=ax)
        else:
            for ax in axes:
                self.v["axis_status",ax]="stopped"
                self.v["moving",ax]=False
    
    def _stop_wait(self, axis="all"):
        axes=self.device.get_all_axes() if axis=="all" else [axis]
        if any(self.device.is_moving(ax) for ax in axes):
            self.device.stop(axis=axis)
            for ax in axes:
                while self.device.is_moving(ax):
                    self.sleep(0.05)
    def move_by(self, axis, steps, stepsize=10):
        """Move a given axis for a given number of steps of the given size"""
        if self.open():
            self._stop_wait(axis=axis)
            self.device.move_by(axis,steps,stepsize=stepsize)
            self.update_measurements()
    def stop_motion(self, axis):
        """Stop motion at a given axis"""
        if self.open():
            self._stop_wait(axis=axis)
            self.update_measurements()