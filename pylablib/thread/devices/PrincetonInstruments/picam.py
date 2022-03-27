from ..generic import camera


class PicamCameraThread(camera.GenericCameraThread):
    """
    Generic Picam camera device thread.

    See :class:`.camera.GenericCameraThread`.
    """
    parameter_variables=camera.GenericCameraThread.parameter_variables|{"exposure",
        "frame_period","detector_size","roi_limits","roi","buffer_size"}
    def _get_camera_attributes(self):  # pylint: disable=arguments-differ
        return super()._get_camera_attributes(enum_as_str=False)
    def _set_camera_attribute(self, name, value):
        old_value=self.device.cav[name]
        try:
            self.device.cav[name]=value
            self.device._commit_parameters()
        except self.device.Error:
            self.device.cav[name]=old_value
            raise
    def connect_device(self):
        with self.using_devclass("PrincetonInstruments.PicamCamera",host=self.remote) as cls:
            self.device=cls(serial_number=self.serial_number)  # pylint: disable=not-callable
    def setup_task(self, serial_number=None, remote=None, misc=None):  # pylint: disable=arguments-differ
        self.serial_number=serial_number
        super().setup_task(remote=remote,misc=misc)
    def _apply_additional_parameters(self, parameters):
        if "add_info" in parameters:
            self.device.enable_metadata(parameters["add_info"])
        super()._apply_additional_parameters(parameters)