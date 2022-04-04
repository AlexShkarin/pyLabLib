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
    device.set_frame_format("list")
    device.set_frame_info_format("namedtuple")
    yield device

class CameraTester(DeviceTester):
    """
    Generic camera tester.

    In addition to the basic device tests, also performs basic camera testing.
    """
    grab_size=10
    default_roi=()
    @pytest.mark.devchange(2)
    def test_snap_grab(self, devopener):
        """Test snapping and grabbing functions"""
        device=devopener()
        device.set_roi(*self.default_roi)
        img=device.snap()
        assert isinstance(img,np.ndarray)
        assert img.ndim==2
        assert img.shape==device.get_data_dimensions()
        img*=2
        imgs,infos=device.grab(self.grab_size,return_info=True)
        assert isinstance(imgs,list) and isinstance(infos,list) and len(imgs)==self.grab_size and len(infos)==self.grab_size
        assert isinstance(imgs[0],np.ndarray)
        assert imgs[0].ndim==2
        assert imgs[0].shape==device.get_data_dimensions()
    def test_multisnap(self, devopener, stress_factor):
        """Test snapping and grabbing functions"""
        device=devopener()
        for _ in range(5*stress_factor):
            device.snap()
    def test_multigrab(self, devopener, stress_factor):
        """Test snapping and grabbing functions"""
        device=devopener()
        device.set_roi(*self.default_roi)
        for _ in range(stress_factor):
            device.grab(self.grab_size)
    @pytest.mark.devchange(2)
    def test_get_full_info_acq(self, devopener):
        """Test info getting errors during acquisition"""
        device=devopener()
        device.set_roi(*self.default_roi)
        device.start_acquisition()
        try:
            info=device.get_full_info(self.include)
            print(device,info)
        finally:
            device.stop_acquisition()
    # @pytest.mark.devchange(3)
    # def test_get_set_all_acq(self, devopener):
    #     """Test getting and re-applying settings error during acquisition"""
    #     device=devopener()
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
    def test_frame_info(self, devopener):
        """Test frame info consistency"""
        device=devopener()
        device.set_roi(*self.default_roi)
        frames,infos=device.grab(self.grab_size,return_info=True)
        assert len(frames)==self.grab_size
        assert len(frames)==len(infos)
        assert [i.frame_index for i in infos]==list(range(self.grab_size))
    @pytest.mark.devchange(1)
    def test_frame_format(self, devopener):
        """Test frame format consistency"""
        device=devopener()
        device.set_roi(*self.default_roi)
        for meta_ena in [True,False]:
            if hasattr(device,"enable_metadata"):
                device.enable_metadata(meta_ena)
            elif meta_ena:
                continue
            for ff,fif in [("list","namedtuple"),("list","dict"),("list","list"),("list","array"),("array","array"),("chunks","array")]:
                device.set_frame_format(ff)
                device.set_frame_info_format(fif)
                frames,infos=device.grab(self.grab_size,return_info=True)
                nframes=sum(len(ch) for ch in frames) if ff=="chunks" else len(frames)
                assert nframes==self.grab_size
                if ff=="array":
                    assert isinstance(frames,np.ndarray)
                else:
                    assert isinstance(frames,list)
                assert len(frames)==len(infos)
                if fif=="namedtuple":
                    fidx=[i.frame_index for i in infos]
                elif fif=="dict":
                    fidx=[i["frame_index"] for i in infos]
                elif fif=="list":
                    fidx=[i[0] for i in infos]
                elif fif=="array":
                    if ff=="list":
                        fidx=[i[0] for i in infos]
                    elif ff=="array":
                        fidx=infos[:,0]
                    elif ff=="chunks":
                        fidx=np.concatenate([i[:,0] for i in infos])
                assert list(fidx)==list(range(self.grab_size))
    def check_acq_params(self, device, setup, running, new_images=None):
        if new_images is None:
            new_images=running
        assert device.is_acquisition_setup()==setup
        assert device.acquisition_in_progress()==running
        assert (device.get_new_images_range() is not None)==new_images
    @pytest.mark.devchange(3)
    def test_acq_info(self, devopener):
        """Test getting acquisition info"""
        device=devopener()
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
    def test_frame_size(self, devopener):
        """Test data dimensions and detector size relations"""
        device=devopener()
        for idx in ["rct","rcb","xyt","xyb"]:
            self.check_get_set(device,"image_indexing",idx)
        device.set_image_indexing("rct")
        if hasattr(device,"set_roi"):
            device.set_roi()
        assert device.get_data_dimensions()==device.get_detector_size()[::-1]
    _exposure_precision=1E-6
    def _assert_settings(self, old_settings, new_settings):
        if "exposure" in old_settings:
            assert "exposure" in new_settings
            old_exp,new_exp=old_settings["exposure"],new_settings["exposure"]
            assert abs(old_exp-new_exp)<abs(old_exp+new_exp)*self._exposure_precision
            del old_settings["exposure"]
            del new_settings["exposure"]
        super()._assert_settings(old_settings,new_settings)




class ROICameraTester(CameraTester):
    """
    ROI camera tester.

    In addition to the basic camera tests, also performs ROI-related testing.
    """
    rois=[]
    # a list of 2-tuples ``(roi_set, roi_get)``, where the first is the ROI supplied to the camera,
    # and the second is the expected resulting ROI (can also be ``"same"``)
    @pytest.mark.devchange(3)
    def test_roi(self, devopener):
        """
        Test ROI functions.

        Also test that the frame shape and size obeys the specified ROI.
        """
        device=devopener()
        # basic full ROI
        device.set_roi()
        rr=device.get_roi()
        ds=device.get_detector_size()
        assert len(rr) in (4,6)
        assert rr[:4]==(0,ds[0],0,ds[1])
        # ROI limits
        rlim=device.get_roi_limits()
        if rlim[0].min==rlim[0].max and rlim[1].min==rlim[1].max:
            return
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
            def wrap(v, p, up):
                if v is None:
                    return None
                return (v-1)%p+1 if up else v%p
            sr=(wrap(sr[0],ds[0],False),wrap(sr[1],ds[0],True),wrap(sr[2],ds[1],False),wrap(sr[3],ds[1],True))+sr[4:]
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