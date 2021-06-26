from .test_basic import DeviceTester

from pylablib.devices import AWG

import pytest

class GenericAWGTester(DeviceTester):
    """Testing a generic AWG"""
    @pytest.mark.devchange(5)
    def test_output(self, devopener):
        device=devopener()
        for ch in range(1,device.get_channels_number()+1):
            device.enable_output(True,channel=ch)
            assert device.is_output_enabled(channel=ch)
            device.enable_output(False,channel=ch)
            assert not device.is_output_enabled(channel=ch)
    
    devfunctions=["sine"]
    @pytest.mark.devchange(5)
    def test_functions(self, devopener):
        device=devopener()
        for ch in range(1,device.get_channels_number()+1):
            for f in self.devfunctions:
                device.set_function(f,channel=ch)
                assert device.get_function(channel=ch)==f



class TestRSInstekAFG21000(GenericAWGTester):
    """Testing class for RSInstek AFG 21000 series AWG"""
    devname="rsinstek_21000"
    devcls=AWG.RSInstekAFG21000