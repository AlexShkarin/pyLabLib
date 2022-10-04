import pylablib

from pylablib.devices import Andor
from pylablib.devices import DCAM
from pylablib.devices import IMAQdx
from pylablib.devices import PhotonFocus
from pylablib.devices import PCO
from pylablib.devices import uc480
from pylablib.devices import Thorlabs
from pylablib.devices import Photometrics
from pylablib.devices import PrincetonInstruments
from pylablib.devices import Basler


from .test_basic_camera import ROICameraTester

import pytest
import numpy as np



def gen_rois(sz, bins=((),), max_factor=4, symm=False):
    if symm:
        base_rois=[(sz//2,-sz//2,sz//2,-sz//2),(sz,-sz,sz//2,-sz//2),(sz//2,-sz//2,sz*2,-sz*2)]
    else:
        base_rois=[(0,sz,0,sz),(0,sz*4,0,sz*2),(sz*2,sz*4,sz,sz*4)]
    base_rois=[
        ((0,None,0,None),None),
        (base_rois[0],("same" if max_factor>=1 else None)),
        (base_rois[1],("same" if max_factor>=2 else None)),
        (base_rois[2],("same" if max_factor>=4 else None)),
        ((sz*2,sz*2,sz*2,sz*2),None),
        ((0,0,sz,sz*4),None),
        ((0,sz*2,10000,10000),None),
        ((1,19,15,64),None),
        ((8,101,3,35),None),
        ((10000,10000,10000,10000),None),
        ((0,1,0,1),None),
        ]
    bins=[b if (b and isinstance(b[0],tuple)) else (b,True) for b in bins]
    rois=[(r+b,(rv if bv else None)) for (r,rv) in base_rois for (b,bv) in bins]
    return rois






class TestAndorSDK2(ROICameraTester):
    """Testing class for Andor SDK2 camera interface"""
    devname="andor_sdk2"
    devcls=Andor.AndorSDK2Camera
    get_set_all_exclude=["acq_parameters/cont"]
    grab_size=10
    rois=gen_rois(128,((1,1),(1,2),(2,2),((0,0),False),((3,3),False),((10,10),False),((100,100),False)))





class TestAndorSDK3(ROICameraTester):
    """Testing class for Andor SDK3 camera interface"""
    devname="andor_sdk3"
    devcls=Andor.AndorSDK3Camera
    grab_size=10
    rois=gen_rois(128,((1,1),(1,2),(2,2),((0,0),False),((3,3),False),((10,10),False),((100,100),False)))
    @classmethod
    def post_open(cls, device):
        device.enable_metadata(True)





class TestDCAM(ROICameraTester):
    """Testing class for DCAM camera interface"""
    devname="dcam"
    devcls=DCAM.DCAMCamera
    grab_size=10
    rois=gen_rois(128,((1,1),((1,2),None),(2,2),((0,0),False),((3,3),False),((10,10),False),((100,100),False)))





class TestPhotonFocusIMAQ(ROICameraTester):
    """Testing class for PhotonFocus camera with NI IMAQ interface"""
    devname="photon_focus_imaq"
    devcls=PhotonFocus.PhotonFocusIMAQCamera
    rois=gen_rois(128)
    
    def check_status_line(self, frames):
        slines=PhotonFocus.get_status_lines(np.asarray(frames))
        assert slines is not None
        assert np.all(slines[1:,0]-slines[:-1,0]==1)
    
    @pytest.fixture(scope="class")
    def library_parameters(self):
        pylablib.par["devices/dlls/pfcam"]="../dlls/libs/x32"
    
    @pytest.mark.devchange(5)
    def test_large_acq(self, devopener):
        """Test large fast acquisition"""
        device=devopener()
        device.set_frame_format("list")
        for roi,ngrab,nbuff in [((0,None,0,None),100,50),((0,32,0,32),10**5,5000)]:
            device.set_roi(*roi)
            device.set_exposure(0)
            device.set_frame_period(0)
            device.enable_status_line(True)
            frames=device.grab(ngrab,buff_size=nbuff)
            assert len(frames)==ngrab
            self.check_status_line(frames)





class TestPhotonFocusSiSo(ROICameraTester):
    """Testing class for PhotonFocus camera with SiliconSoftware interface"""
    devname="photon_focus_siso"
    devcls=PhotonFocus.PhotonFocusSiSoCamera
    rois=gen_rois(128)
    
    def check_status_line(self, frames):
        slines=PhotonFocus.get_status_lines(np.asarray(frames))
        assert slines is not None
        assert np.all(slines[1:,0]-slines[:-1,0]==1)
    
    @pytest.fixture(scope="class")
    def library_parameters(self):
        pylablib.par["devices/dlls/pfcam"]="../dlls/libs/x32"
    
    @pytest.mark.devchange(5)
    def test_large_acq(self, devopener):
        """Test large fast acquisition"""
        device=devopener()
        device.set_frame_format("list")
        device.gav["CAMERA_LINK_CAMTYP"]="FG_CL_DUALTAP_12_BIT"
        device.gav["FORMAT"]="FG_GRAY16"
        device.cav["DataResolution"]="12bit"
        for roi,ngrab,nbuff in [((0,None,0,None),100,50),((0,32,0,32),10**4,1000)]:
            device.set_roi(*roi)
            device.set_exposure(1E-4)
            device.set_frame_period(0)
            device.enable_status_line(True)
            frames=device.grab(ngrab,buff_size=nbuff)
            assert len(frames)==ngrab
            self.check_status_line(frames)




class TestPhotonFocusBitFlow(ROICameraTester):
    """Testing class for PhotonFocus camera with BitFlow interface"""
    devname="photon_focus_bitflow"
    devcls=PhotonFocus.PhotonFocusBitFlowCamera
    rois=gen_rois(128)
    
    def check_status_line(self, frames):
        slines=PhotonFocus.get_status_lines(np.asarray(frames))
        assert slines is not None
        assert np.all(slines[1:,0]-slines[:-1,0]==1)
    
    @pytest.fixture(scope="class")
    def library_parameters(self):
        pylablib.par["devices/dlls/pfcam"]="../dlls/libs/x32"




class TestIMAQdx(ROICameraTester):
    """Testing class for IMAQdx camera interface"""
    devname="imaqdx"
    devcls=IMAQdx.IMAQdxCamera
    grab_size=100
    rois=gen_rois(384,max_factor=0)





class TestTLCam(ROICameraTester):
    """Testing class for Thorlabs TLCam camera interface"""
    devname="thorlabs_tlcam"
    devcls=Thorlabs.ThorlabsTLCamera
    grab_size=100
    # rois=gen_rois(128,((1,1),(1,2),(2,2),((0,0),False),((3,3),False),((10,10),False),((100,100),False)))
    rois=gen_rois(128,((1,1),))





class TestPCO(ROICameraTester):
    """Testing class for PCO SC2 camera interface"""
    devname="pco_sc2"
    devcls=PCO.PCOSC2Camera
    rois=gen_rois(320,((1,1),(1,2),(2,2),((0,0),False),((3,3),False),((10,10),False),((100,100),False)),symm=True)





class TestUC480(ROICameraTester):
    """Testing class for UC480 camera interface"""
    devname="uc480"
    devcls=uc480.UC480Camera
    rois=gen_rois(128,((1,1),(1,2),(2,2),((0,0),False),((3,3),False),((10,10),False),((100,100),False)))
    default_roi=(0,512,0,512)





class TestPvcam(ROICameraTester):
    """Testing class for Photometrics camera interface"""
    devname="pvcam"
    devcls=Photometrics.PvcamCamera
    rois=gen_rois(128,((1,1),((1,2),False),(2,2),((0,0),False),((3,3),False),((10,10),False),((100,100),False)))
    default_roi=(0,512,0,512)
    @classmethod
    def post_open(cls, device):
        device.enable_metadata(True)





class TestPICam(ROICameraTester):
    """Testing class for Princeton Instruments camera interface"""
    devname="picam"
    devcls=PrincetonInstruments.PicamCamera
    rois=gen_rois(64,((1,1),((1,2),False),(2,2),((0,0),False),((3,3),False),((10,10),False),((100,100),False)))
    default_roi=(0,256,0,256)
    _exposure_precision=1E-4
    @classmethod
    def post_open(cls, device):
        device.enable_metadata(True)





class TestBasler(ROICameraTester):
    """Testing class for Basler pylon camera interface"""
    devname="basler_pylon"
    devcls=Basler.BaslerPylonCamera
    rois=gen_rois(64)