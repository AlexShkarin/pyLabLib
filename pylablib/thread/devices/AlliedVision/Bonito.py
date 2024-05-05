from ..generic import camera
from ....devices.interface.camera import TStatusLineDescription
from ....devices.AlliedVision import Bonito
from ....devices.AlliedVision import BonitoStatusLineChecker




class GenericBonitoCameraThread(camera.GenericCameraThread):
    """
    Generic AlliedVision Bonito camera device thread.

    See :class:`GenericCameraThread`.
    """
    parameter_variables=camera.GenericCameraThread.parameter_variables|{"exposure","frame_period",
        "status_line","bl_offset","buffer_status","buffer_size","detector_size","roi_limits","roi"}
    def _get_metainfo(self, frames, indices, infos):
        metainfo=super()._get_metainfo(frames,indices,infos)
        sline=Bonito.get_status_lines(frames[0][0] if frames[0].ndim==3 else frames[0])
        if sline is not None:
            metainfo["status_line"]=TStatusLineDescription("allvis_bonito",(0,0,0,7),BonitoStatusLineChecker())
        return metainfo



class IMAQBonitoCameraThread(GenericBonitoCameraThread):
    """
    IMAQ-interfaced AlliedVision Bonito camera device thread.

    See :class:`GenericCameraThread`.
    """
    def connect_device(self):
        with self.using_devclass("AlliedVision.BonitoIMAQCamera",host=self.remote) as cls:
            self.device=cls(imaq_name=self.imaq_name)  # pylint: disable=not-callable
        
    def setup_task(self, imaq_name, remote=None, misc=None):  # pylint: disable=arguments-differ, arguments-renamed
        self.imaq_name=imaq_name
        super().setup_task(remote=remote,misc=misc)