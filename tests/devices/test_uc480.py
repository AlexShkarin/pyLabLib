from .test_camera_generic import ROICameraTester

from pylablib.devices import uc480


class UC480Tester(ROICameraTester):
    """Testing class for UC480 camera interface"""
    def test_all(self):
        with self.opened():
            super().test_all()
            rois=[( (0,512,0,256,1,1),"same"),
                    ((256,512,128,512,1,1),"same"),
                    ((256,512,128,512,2,2),"same"),
                    ((0,0,0,0,0,0),None),
                    ((512,512,512,512,2,2),None)]
            self.test_roi(rois)
            

def test_uc480():
    UC480Tester(uc480.UC480Camera).test_all()