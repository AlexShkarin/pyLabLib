from ..generic import camera


class BaslerPylonCameraThread(camera.GenericCameraThread):
    """
    Generic Basler pylon camera device thread.

    See :class:`.camera.GenericCameraThread`.
    """
    parameter_variables=camera.GenericCameraThread.parameter_variables|{"detector_size","roi_limits","roi","buffer_size","exposure","frame_period"}
    def _get_camera_attributes(self):  # pylint: disable=arguments-differ
        return super()._get_camera_attributes(enum_as_str=False)
    def connect_device(self):
        with self.using_devclass("Basler.BaslerPylonCamera",host=self.remote) as cls:
            self.device=cls(idx=self.basler_idx,name=self.basler_name)  # pylint: disable=not-callable
    def setup_task(self, idx=0, name=None, remote=None, misc=None):  # pylint: disable=arguments-differ, arguments-renamed
        self.basler_idx=idx
        self.basler_name=name
        super().setup_task(remote=remote,misc=misc)