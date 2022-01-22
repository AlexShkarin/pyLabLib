from ..generic import camera


class AndorSDK2CameraThread(camera.GenericCameraThread):
    """
    Generic Andor SDK2 camera device thread.

    See :class:`.camera.GenericCameraThread`.
    """
    parameter_variables=camera.GenericCameraThread.parameter_variables|{"shutter","exposure",
        "frame_period","trigger_mode","detector_size","roi_limits","roi","buffer_size"}
    def connect_device(self):
        with self.using_devclass("Andor.AndorSDK2Camera",host=self.remote) as cls:
            self.device=cls(idx=self.idx)  # pylint: disable=not-callable
    def setup_task(self, idx=0, remote=None, misc=None):  # pylint: disable=arguments-differ
        self.idx=idx
        super().setup_task(remote=remote,misc=misc)

class AndorSDK2IXONThread(AndorSDK2CameraThread):
    """
    Andor IXON camera device thread.

    See :class:`.camera.GenericCameraThread`.
    """
    parameter_variables=AndorSDK2CameraThread.parameter_variables|{"EMCCD_gain","fan_mode","cooler","shutter","temperature","temperature_status","temperature_monitor",
            "hsspeed","vsspeed","preamp","frame_transfer"}

AndorSDK2LucaThread=AndorSDK2IXONThread