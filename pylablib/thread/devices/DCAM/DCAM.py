from ..generic import camera


class DCAMCameraThread(camera.GenericCameraThread):
    """
    Generic DCAM camera device thread.

    See :class:`.camera.GenericCameraThread`.
    """
    parameter_variables=camera.GenericCameraThread.parameter_variables|{
            "trigger_mode","exposure","detector_size","roi_limits","roi","frame_period","transfer_info","buffer_size"}
    def connect_device(self):
        with self.using_devclass("DCAM.DCAMCamera",host=self.remote) as cls:
            self.device=cls(idx=self.idx)
    def setup_task(self, idx=0, remote=None, misc=None):
        self.idx=idx
        super().setup_task(remote=remote,misc=misc)