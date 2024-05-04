from ..generic import camera


class AndorSDK2CameraThread(camera.GenericCameraThread):
    """
    Generic Andor SDK2 camera device thread.

    See :class:`.camera.GenericCameraThread`.
    """
    parameter_variables=camera.GenericCameraThread.parameter_variables|{"exposure",
        "frame_period","trigger_mode","detector_size","read_mode","roi_limits","roi","buffer_size",
        "EMCCD_gain","fan_mode","cooler","shutter","temperature","temperature_status","temperature_monitor",
        "channel","oamp","hsspeed","vsspeed","preamp","frame_transfer"}
    full_info_variables=-4  # all except capabilities
    def connect_device(self):
        with self.using_devclass("Andor.AndorSDK2Camera",host=self.remote) as cls:
            self.device=cls(idx=self.idx)  # pylint: disable=not-callable
    def setup_task(self, idx=0, remote=None, misc=None):  # pylint: disable=arguments-differ, arguments-renamed
        self.idx=idx
        super().setup_task(remote=remote,misc=misc)

AndorSDK2IXONThread=AndorSDK2CameraThread
AndorSDK2LucaThread=AndorSDK2CameraThread