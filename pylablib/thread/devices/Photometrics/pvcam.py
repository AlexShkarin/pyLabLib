from ..generic import camera


class PvcamCameraThread(camera.GenericCameraThread):
    """
    Generic Pvcam camera device thread.

    See :class:`.camera.GenericCameraThread`.
    """
    parameter_variables=camera.GenericCameraThread.parameter_variables|{"exposure","frame_period","clear_mode","clear_cycles","clearing_time","trigger_mode",
        "readout_mode","detector_size","roi_limits","roi","buffer_size"}
    def _get_camera_attributes(self):  # pylint: disable=arguments-differ
        return super()._get_camera_attributes(enum_as_str=False)
    def connect_device(self):
        with self.using_devclass("Photometrics.PvcamCamera",host=self.remote) as cls:
            self.device=cls(name=self.cam_name)  # pylint: disable=not-callable
    def _get_aux_full_info(self):
        aux_info=super()._get_aux_full_info()
        if self.device:
            if "EXPOSURE_MODE" in self.device.ca:
                trig_modes=self.device.get_attribute_range("EXPOSURE_MODE",parameter="trigger_mode")
                trig_out_modes=self.device.get_attribute_range("EXPOSE_OUT_MODE",error_on_missing=False,default={None:"None"},parameter="trigger_out_mode")
                aux_info["parameter_ranges/trigger_mode"]=(trig_modes,trig_out_modes)
            aux_info["parameter_ranges/clear_mode"]=self.device.get_attribute_range("CLEAR_MODE",error_on_missing=False,default={},parameter="clear_mode")
        return aux_info
    def _prepare_applied_parameters(self, parameters):
        super()._prepare_applied_parameters(parameters)
        if "trigger_mode" in parameters:
            trig_mode_alias={"int":"e_int","ext":"e_trig_first"}
            parameters["trigger_mode"]=trig_mode_alias.get(parameters["trigger_mode"],parameters["trigger_mode"])
    def setup_task(self, cam_name=None, remote=None, misc=None):  # pylint: disable=arguments-differ
        self.cam_name=cam_name
        super().setup_task(remote=remote,misc=misc)
    def _apply_additional_parameters(self, parameters):
        if "add_info" in parameters:
            self.device.enable_metadata(parameters["add_info"])
        super()._apply_additional_parameters(parameters)