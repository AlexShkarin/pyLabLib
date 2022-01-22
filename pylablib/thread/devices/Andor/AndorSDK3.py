from ..generic import camera


class AndorSDK3CameraThread(camera.GenericCameraThread):
    """
    Generic Andor SDK3 camera device thread.

    See :class:`.camera.GenericCameraThread`.
    """
    parameter_variables=camera.GenericCameraThread.parameter_variables|{"exposure","frame_period",
        "trigger_mode","detector_size","roi_limits","roi","temperature","temperature_monitor","buffer_size","frame_counter_status","missed_frames"}
    _frameinfo_include_fields={"frame_index","timestamp_dev"}
    def connect_device(self):
        with self.using_devclass("Andor.AndorSDK3Camera",host=self.remote) as cls:
            self.device=cls(idx=self.idx)  # pylint: disable=not-callable
    def setup_open_device(self):
        super().setup_open_device()
        self.device.set_overflow_behavior("restart")
    def setup_task(self, idx=0, remote=None, misc=None):  # pylint: disable=arguments-differ
        self.idx=idx
        super().setup_task(remote=remote,misc=misc)
    def acq_finalize_regular(self):
        super().acq_finalize_regular()
        if self.device:
            self.device.reset_overflows_counter()
    def _apply_additional_parameters(self, parameters):
        if "add_info" in parameters:
            self.device.enable_metadata(parameters["add_info"])
        super()._apply_additional_parameters(parameters)

class AndorSDK3ZylaThread(AndorSDK3CameraThread):
    """
    Andor Zyla camera device thread.

    See :class:`.camera.GenericCameraThread`.
    """
    def setup_open_device(self):
        super().setup_open_device()
        self.device.set_cooler(True)