from .test_basic import DeviceTester

import pytest
import numpy as np


@pytest.fixture
def camera(device):
    device.clear_acquisition()
    if hasattr(device,"set_roi"):
        device.set_roi()
    if hasattr(device,"set_exposure"):
        device.set_exposure(.1)
    yield device

class CameraTester(DeviceTester):
    """
    Generic camera tester.

    In addition to the basic device tests, also performs basic camera testing.
    """
    grab_size=10
    @pytest.mark.devchange(2)
    def test_snap_grab(self, device):
        """Test snapping and grabbing functions"""
        device.set_roi()
        img=device.snap()
        assert isinstance(img,np.ndarray)
        assert img.ndim==2
        assert img.shape==device.get_data_dimensions()
        img*=2
        imgs=device.grab(self.grab_size)
        assert isinstance(imgs,list)
        assert isinstance(imgs[0],np.ndarray)
        assert imgs[0].ndim==2
        assert imgs[0].shape==device.get_data_dimensions()
    def test_multisnap(self, device, stress_factor):
        """Test snapping and grabbing functions"""
        for _ in range(5*stress_factor):
            device.snap()
    def test_multigrab(self, device, stress_factor):
        """Test snapping and grabbing functions"""
        for _ in range(stress_factor):
            device.grab(self.grab_size)
    @pytest.mark.devchange(2)
    def test_get_full_info_acq(self, device):
        """Test info getting errors during acquisition"""
        device.start_acquisition()
        try:
            info=device.get_full_info(self.include)
            print(device,info)
        finally:
            device.stop_acquisition()
    # @pytest.mark.devchange(3)
    # def test_get_set_all_acq(self, device):
    #     """Test getting and re-applying settings error during acquisition"""
    #     stopped_settings=device.get_settings(self.include)
    #     print(device,stopped_settings)
    #     for k in self.get_set_all_exclude:
    #         del stopped_settings[k]
    #     device.start_acquisition()
    #     try:
    #         settings=device.get_settings(self.include)
    #         device.apply_settings(stopped_settings)
    #         new_settings=device.get_settings(self.include)
    #         for k in self.get_set_all_exclude:
    #             del settings[k]
    #             del new_settings[k]
    #         assert new_settings==settings
    #     finally:
    #         device.stop_acquisition()

    @pytest.mark.devchange(1)
    def test_frame_info(self, device):
        """Test frame info consistency"""
        frames,infos=device.grab(self.grab_size,return_info=True)
        assert len(frames)==self.grab_size
        assert len(frames)==len(infos)
        assert [i.frame_index for i in infos]==list(range(self.grab_size))
    def check_acq_params(self, device, setup, running, new_images=None):
        if new_images is None:
            new_images=running
        assert device.is_acquisition_setup()==setup
        assert device.acquisition_in_progress()==running
        assert (device.get_new_images_range() is not None)==new_images
    @pytest.mark.devchange(3)
    def test_acq_info(self, device):
        """Test getting acquisition info"""
        device.set_roi()
        device.clear_acquisition()
        self.check_acq_params(device,False,False)
        device.setup_acquisition()
        self.check_acq_params(device,True,False)
        device.clear_acquisition()
        self.check_acq_params(device,False,False)
        device.start_acquisition()
        device.wait_for_frame(timeout=5.)
        self.check_acq_params(device,True,True)
        device.clear_acquisition()
        self.check_acq_params(device,False,False)
    
    @pytest.mark.devchange(3)
    def test_frame_size(self, device):
        """Test data dimensions and detector size relations"""
        for idx in ["rct","rcb","xyt","xyb"]:
            self.check_get_set(device,"image_indexing",idx)
        device.set_image_indexing("rct")
        if hasattr(device,"set_roi"):
            device.set_roi()
        assert device.get_data_dimensions()==device.get_detector_size()[::-1]




class ROICameraTester(CameraTester):
    """
    ROI camera tester.

    In addition to the basic camera tests, also performs ROI-related testing.
    """
    rois=[]
    # a list of 2-tuples ``(roi_set, roi_get)``, where the first is the ROI supplied to the camera,
    # and the second is the expected resulting ROI (can also be ``"same"``)
    @pytest.mark.devchange(3)
    def test_roi(self, device):
        """
        Test ROI functions.

        Also test that the frame shape and size obeys the specified ROI.
        """
        # basic full ROI
        device.set_roi()
        rr=device.get_roi()
        ds=device.get_detector_size()
        assert len(rr) in (4,6)
        assert rr[:4]==(0,ds[0],0,ds[1])
        # ROI limits
        rlim=device.get_roi_limits()
        print(rlim)
        assert len(rlim)==2 and all([len(rl)==5 for rl in rlim])
        assert rlim[0].max==ds[0],rlim[1].max==ds[1]
        # Data dimensions
        device.set_image_indexing("rct")
        assert device.get_data_dimensions()==device.get_detector_size()[::-1]
        # Check multiple ROIs
        for i,(sr,gr) in enumerate(self.rois):
            print(i,sr)
            # Check setting and getting
            if gr=="same":
                gr=sr
            device.set_roi(*sr)
            rr=device.get_roi()
            print("->",rr)
            if gr is not None:
                assert rr==gr
            # Check image shape and size
            sz=(rr[1]-rr[0]),(rr[3]-rr[2])
            if len(rr)>4:
                sz=sz[0]//rr[4],sz[1]//rr[5]
            for (idx,shp) in [("rct",sz[::-1]),("xyt",sz)]:
                device.set_image_indexing(idx)
                assert device.get_data_dimensions()==shp
                # img=device.grab(self.grab_size)[0]
                img=device.snap()
                assert img.shape==shp