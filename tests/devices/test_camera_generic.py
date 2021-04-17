from .test_utils import DeviceTester

import numpy as np

class CameraTester(DeviceTester):
    """
    Generic camera tester.

    In addition to the basic device tests, also performs basic camera testing.
    """
    def test_snap_grab(self):
        """Test snapping and grabbing functions"""
        with self.opened() as dev:
            img=dev.snap()
            assert isinstance(img,np.ndarray)
            assert img.ndim==2
            assert img.shape==dev.get_data_dimensions()
            imgs=dev.grab(10)
            assert isinstance(imgs,list)
            assert isinstance(imgs[0],np.ndarray)
            assert imgs[0].ndim==2
            assert imgs[0].shape==dev.get_data_dimensions()
    
    def test_frame_size(self):
        """Test data dimensions and detector size relations"""
        with self.opened() as dev:
            for idx in ["rct","rcb","xyt","xyb"]:
                self.test_get_set("image_indexing",idx)
            dev.set_image_indexing("rct")
            if hasattr(dev,"set_roi"):
                dev.set_roi()
            assert dev.get_data_dimensions()==dev.get_detector_size()[::-1]
        
    def test_all(self):
        with self.opened():
            super().test_all()
            self.test_snap_grab()
            self.test_frame_size()




class ROICameraTester(CameraTester):
    """
    ROI camera tester.

    In addition to the basic camera tests, also performs ROI-related testing.
    """
    def test_roi(self, rois):
        """
        Test ROI functions.

        `rois` is a list of 2-tuples ``(roi_set, roi_get)``,
        where the first is the ROI suppled to the camera, and the second is the expected resulting ROI
        (can also be ``"same"``).
        Also test that the frame shape and size obeys the specified ROI.
        """
        with self.opened() as dev:
            # basic full ROI
            dev.set_roi()
            rr=dev.get_roi()
            ds=dev.get_detector_size()
            assert len(rr) in (4,6)
            assert rr[:4]==(0,ds[0],0,ds[1])
            # ROI limits
            rlim=dev.get_roi_limits()
            assert len(rlim)==2 and all([len(rl)==len(rr) for rl in rlim])
            assert rlim[0][0]==0 and rlim[0][2]==0 and rlim[1][1]==ds[0] and rlim[1][3]==ds[1]
            # Data dimensions
            dev.set_image_indexing("rct")
            assert dev.get_data_dimensions()==dev.get_detector_size()[::-1]
            # Check multiple ROIs
            for sr,gr in rois:
                # Check setting and getting
                if gr=="same":
                    gr=sr
                dev.set_roi(*sr)
                rr=dev.get_roi()
                if gr is not None:
                    assert rr==gr
                # Check image shape and size
                sz=(rr[1]-rr[0]),(rr[3]-rr[2])
                if len(rr)>4:
                    sz=sz[0]//rr[4],sz[1]//rr[5]
                for (idx,shp) in [("rct",sz[::-1]),("xyt",sz)]:
                    dev.set_image_indexing(idx)
                    assert dev.get_data_dimensions()==shp
                    img=dev.snap()
                    assert img.shape==shp
