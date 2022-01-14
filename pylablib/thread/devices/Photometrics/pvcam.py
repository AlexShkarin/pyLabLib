from ..generic import camera


class PvcamCameraThread(camera.GenericCameraThread):
    """
    Generic Pvcam camera device thread.

    See :class:`.camera.GenericCameraThread`.
    """
    parameter_variables=camera.GenericCameraThread.parameter_variables|{"exposure",
        "frame_period","detector_size","roi_limits","roi","buffer_size"}
    def connect_device(self):
        with self.using_devclass("Photometrics.PvcamCamera",host=self.remote) as cls:
            self.device=cls(name=self.cam_name)
    def setup_task(self, cam_name=None, remote=None, misc=None):  # pylint: disable=arguments-differ
        self.cam_name=cam_name
        super().setup_task(remote=remote,misc=misc)
    def _apply_additional_parameters(self, parameters):
        if "add_info" in parameters:
            self.device.enable_metadata(parameters["add_info"])
        super()._apply_additional_parameters(parameters)