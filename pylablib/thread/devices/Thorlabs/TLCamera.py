from ..generic import camera



class ThorlabsTLCameraThread(camera.GenericCameraThread):
    """
    Generic Thorlabs TLCam camera device thread.

    See :class:`.camera.GenericCameraThread`.
    """
    parameter_variables=camera.GenericCameraThread.parameter_variables|{
            "exposure","frame_period","detector_size","buffer_size","acq_status","roi_limits","roi","trigger_mode"}
    parameter_freeze_running={"exposure","detector_size","roi_limits","roi","trigger_mode"}
    _frameinfo_include_fields={"frame_index","framestamp","pixelclock"}
    def connect_device(self):
        with self.using_devclass("Thorlabs.ThorlabsTLCamera",host=self.remote) as cls:
            self.device=cls(serial=self.serial)  # pylint: disable=not-callable
    def setup_task(self, serial, remote=None, misc=None):  # pylint: disable=arguments-differ
        if isinstance(serial,tuple):
            serial=serial[0]
        self.serial=serial
        super().setup_task(remote=remote,misc=misc)