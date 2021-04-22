from pylablib.devices import Andor
from pylablib.devices import PhotonFocus
from pylablib.devices import PCO
from pylablib.devices import uc480
from pylablib.devices import Thorlabs

from .test_basic_camera import ROICameraTester

import pytest
import numpy as np



def gen_rois(sz, bins=((),)):
    base_rois=[
        ((0,None,0,None),None),
        ((0,sz*4,0,sz*2),"same"),
        ((sz*2,sz*4,sz,sz*4),"same"),
        ((sz*2,sz*2,sz*2,sz*2),None),
        ((0,0,sz,sz*4),None),
        ((0,sz*2,10000,10000),None),
        ((10000,10000,10000,10000),None),
        ((0,1,0,1),None),
        ]
    bins=[b if (b and isinstance(b[0],tuple)) else (b,True) for b in bins]
    rois=[(r+b,(rv if bv else None)) for (r,rv) in base_rois for (b,bv) in bins]
    return rois






class TestAndorSDK3(ROICameraTester):
    """Testing class for Andor SDK3 camera interface"""
    devname="andor_sdk3"
    devcls=Andor.AndorSDK3Camera
    grab_size=10
    rois=gen_rois(128,((1,1),(1,2),(2,2),((0,0),False),((3,3),False),((10,10),False),((100,100),False)))





class TestPhotonFocusIMAQ(ROICameraTester):
    """Testing class for PhotonFocus camera with NI IMAQ interface"""
    devname="photon_focus_imaq"
    devcls=PhotonFocus.PhotonFocusIMAQCamera
    rois=gen_rois(128)
    
    def check_status_line(self, frames):
        slines=PhotonFocus.get_status_lines(np.asarray(frames))
        assert slines is not None
        assert np.all(slines[1:,1]-slines[:-1,1]==1)
    
    @pytest.mark.devchange(5)
    def test_acq(self, device):
        for roi,ngrab,nbuff in [((0,None,0,None),100,50),((0,32,0,32),10**5,5000)]:
            device.set_roi(*roi)
            device.set_exposure(0)
            device.set_frame_period(0)
            device.enable_status_line(True)
            frames=device.grab(ngrab,buff_size=nbuff)
            assert len(frames)==ngrab
            self.check_status_line(frames)





class TestTLCam(ROICameraTester):
    """Testing class for PCO SC2 camera interface"""
    devname="thorlabs_tlcam"
    devcls=Thorlabs.ThorlabsTLCamera
    grab_size=100
    rois=gen_rois(128,((1,1),(1,2),(2,2),((0,0),False),((3,3),False),((10,10),False),((100,100),False)))





class TestPCO(ROICameraTester):
    """Testing class for PCO SC2 camera interface"""
    devname="pco_sc2"
    devcls=PCO.PCOSC2Camera
    rois=gen_rois(160,((1,1),(1,2),(2,2),((0,0),False),((3,3),False),((10,10),False),((100,100),False)))





class TestUC480(ROICameraTester):
    """Testing class for UC480 camera interface"""
    devname="uc480"
    devcls=uc480.UC480Camera
    rois=gen_rois(128,((1,1),(1,2),(2,2),((0,0),False),((3,3),False),((10,10),False),((100,100),False)))