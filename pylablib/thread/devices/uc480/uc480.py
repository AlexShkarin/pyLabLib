from ..generic import camera

class UC480CameraThread(camera.GenericCameraThread):
    """
    Generic uc480 camera device thread.

    See :class:`GenericCameraThread`.
    """
    parameter_variables=camera.GenericCameraThread.parameter_variables|{"exposure","frame_period","trigger_mode","detector_size","pixel_rate","gains","buffer_size","acq_status","roi_limits","roi"}
    _frameinfo_include_fields={ "frame_index","framestamp","timestamp_dev","io_status",
                                "timestamp_year","timestamp_month","timestamp_day","timestamp_hour","timestamp_minute","timestamp_second","timestamp_millisecond"}
    def connect_device(self):
        with self.using_devclass("uc480.UC480Camera",host=self.remote) as cls:
            if self.sn is not None:
                dev_id=cls.find_by_serial(serial_number=self.sn,backend=self.backend)  # pylint: disable=no-member
                self.device=cls(dev_id=dev_id,backend=self.backend)  # pylint: disable=not-callable
            else:
                self.device=cls(cam_id=self.id,dev_id=self.dev_id,backend=self.backend)  # pylint: disable=not-callable
    def setup_task(self, idx=None, dev_idx=None, sn=None, backend="uc480", remote=None, misc=None):  # pylint: disable=arguments-differ, arguments-renamed
        self.id=idx
        self.dev_id=dev_idx
        self.sn=sn
        self.backend=backend
        super().setup_task(remote=remote,misc=misc)