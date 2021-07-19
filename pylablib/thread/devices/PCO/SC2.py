from ..generic import camera


class PCOSC2CameraThread(camera.GenericCameraThread):
    """
    Generic PCO SC2 camera device thread.

    See :class:`.camera.GenericCameraThread`.
    """
    parameter_variables=camera.GenericCameraThread.parameter_variables|{
            "exposure","frame_period","pixel_rate","all_pixel_rates","trigger_mode","detector_size","roi_limits","roi","buffer_size"}
    def connect_device(self):
        with self.using_devclass("PCO.PCOSC2Camera",host=self.remote) as cls:
            self.device=cls(idx=self.idx,cam_interface=self.cam_interface,reboot_on_fail=self.reboot_on_fail)
    def setup_open_device(self):
        super().setup_open_device()
        try:
            self._status_line_enabled=self.device.get_status_line_mode()[0]
        except self.device.Error:
            pass
    def _get_metainfo(self, frames, indices, infos):
        metainfo=super()._get_metainfo(frames,indices,infos)
        if self._status_line_enabled:
            metainfo["status_line"]=("pco_sc2",(0,0,0,13))
        return metainfo
    def setup_task(self, idx=0, cam_interface=None, reboot_on_fail=True, remote=None, misc=None):
        self.idx=idx
        self.cam_interface=cam_interface
        self.reboot_on_fail=reboot_on_fail
        self._status_line_enabled=False
        super().setup_task(remote=remote,misc=misc)