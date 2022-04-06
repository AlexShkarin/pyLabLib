from ..generic import camera
from ....devices.interface.camera import TStatusLineDescription
from ....devices.PhotonFocus import StatusLineChecker
from ....devices import PhotonFocus




class GenericPhotonFocusCameraThread(camera.GenericCameraThread):
    """
    Generic PhotonFocus camera device thread.

    See :class:`GenericCameraThread`.
    """
    parameter_variables=camera.GenericCameraThread.parameter_variables|{"exposure","frame_period","cfr","trigger_interleave",
        "status_line","bl_offset","buffer_status","buffer_size","detector_size","roi_limits","roi"}
    def _get_camera_attributes(self):  # pylint: disable=arguments-differ
        return super()._get_camera_attributes(enum_as_str=False)
    def _get_metainfo(self, frames, indices, infos):
        metainfo=super()._get_metainfo(frames,indices,infos)
        sline_pos=PhotonFocus.get_status_line_position(frames[0][0] if frames[0].ndim==3 else frames[0])
        if sline_pos:
            row,transp=sline_pos
            line_rect=(0,-1,row,-1) if transp else (row,-1,0,-1)
            metainfo["status_line"]=TStatusLineDescription("photon_focus",line_rect,StatusLineChecker())
        return metainfo
    
    def apply_parameters(self, parameters, update=True, pause="default"):
        if self.device and [p for p in parameters if not p.startswith("tag/")]==["roi"]:
            par_roi=parameters["roi"]
            dev_roi=self.device.get_roi()
            if dev_roi[1]-dev_roi[0]==par_roi[1]-par_roi[0] and dev_roi[3]-dev_roi[2]==par_roi[3]-par_roi[2]:
                parameters["fast_roi"]=parameters.pop("roi")
        super().apply_parameters(parameters,update=update,pause=pause)
    def _apply_additional_parameters(self, parameters):
        super()._apply_additional_parameters(parameters)
        if "fast_roi" in parameters:
            self.device.fast_shift_roi(parameters["fast_roi"][0],parameters["fast_roi"][2])




class IMAQPhotonFocusCameraThread(GenericPhotonFocusCameraThread):
    """
    IMAQ-interfaced PhotonFocus camera device thread.

    See :class:`GenericCameraThread`.
    """
    parameter_variables=GenericPhotonFocusCameraThread.parameter_variables|{"triggers_in_cfg","triggers_out_cfg"}
    def connect_device(self):
        with self.using_devclass("PhotonFocus.PhotonFocusIMAQCamera",host=self.remote) as cls:
            self.device=cls(imaq_name=self.imaq_name,pfcam_port=self.pfcam_port)  # pylint: disable=not-callable
        
    def setup_task(self, imaq_name, pfcam_port, remote=None, misc=None):  # pylint: disable=arguments-differ
        self.imaq_name=imaq_name
        self.pfcam_port=pfcam_port
        super().setup_task(remote=remote,misc=misc)




class SiliconSoftwarePhotonFocusCameraThread(GenericPhotonFocusCameraThread):
    """
    SiliconSoftware-interfaced PhotonFocus camera device thread.

    See :class:`GenericCameraThread`.
    """
    def connect_device(self):
        with self.using_devclass("PhotonFocus.PhotonFocusSiSoCamera",host=self.remote) as cls:
            self.device=cls(siso_board=self.siso_board,siso_applet=self.siso_applet,siso_port=self.siso_port,pfcam_port=self.pfcam_port)  # pylint: disable=not-callable
        
    def setup_task(self, siso_board, siso_applet, siso_port, pfcam_port, remote=None, misc=None):  # pylint: disable=arguments-differ
        self.siso_board=siso_board
        self.siso_applet=siso_applet
        self.siso_port=siso_port
        self.pfcam_port=pfcam_port
        super().setup_task(remote=remote,misc=misc)