from pylablib.devices import Thorlabs, OZOptics
from pylablib.devices import NI

from .test_basic import DeviceTester

import pytest


class TestFW102(DeviceTester):
    """Testing class for Thorlabs FW102 filter wheel interface"""
    devname="thorlabs_fw102"
    devcls=Thorlabs.FW
    @pytest.mark.devchange(4)
    def test_motion(self, devopener):
        device=devopener()
        pos=device.get_position()
        npos=pos-1 if pos>1 else pos+1
        device.set_position(npos)
        assert device.get_position()==npos
        device.set_position(pos)
        assert device.get_position()==pos


class TestOZOpticsEPC04(DeviceTester):
    """Testing class for OZOptics EPC04 polarization controller interface"""
    devname="ozoptics_epc04"
    devcls=OZOptics.EPC04


class TestNIDAQ(DeviceTester):
    """Testing class for NI DAQ interface"""
    devname="nidaq"
    devcls=NI.NIDAQ

    ai_rate=1000
    samples=1000
    @classmethod
    def post_open(cls, device):
        device.add_voltage_input("in0","ai0")
        device.add_voltage_input("in1","ai1")
        device.add_digital_input("din1","port0/line1")
        device.add_counter_input("c0","ctr0","pfi0")
        device.setup_clock(cls.ai_rate)
    
    def test_read(self, devopener):
        """Test samples reading"""
        device=devopener()
        v=device.read(self.samples,timeout=self.samples/self.ai_rate*2+2)
        assert v.shape==(self.samples,4)
        device.start()
        v=device.read(self.samples,timeout=self.samples/self.ai_rate*2+2)
        device.stop()
        assert v.shape==(self.samples,4)