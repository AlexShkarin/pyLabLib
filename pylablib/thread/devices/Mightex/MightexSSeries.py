from ..generic import camera


class MightexSSeriesCameraThread(camera.GenericCameraThread):
    """
    Generic Mightex S Series device thread.

    See :class:`.camera.GenericCameraThread`.
    """
    parameter_variables=camera.GenericCameraThread.parameter_variables|{"detector_size","roi_limits","roi","buffer_size","exposure","frame_period"}
    def connect_device(self):
        with self.using_devclass("Mightex.MightexSSeriesCamera",host=self.remote) as cls:
            self.device=cls(idx=self.mightex_idx)  # pylint: disable=not-callable
    def setup_task(self, idx=0, remote=None, misc=None):  # pylint: disable=arguments-differ, arguments-renamed
        self.mightex_idx=idx
        super().setup_task(remote=remote,misc=misc)