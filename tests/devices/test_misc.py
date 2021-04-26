from pylablib.devices import Thorlabs

from .test_basic import DeviceTester

import pytest


class TestFW102(DeviceTester):
    """Testing class for Thorlabs FW102 filter wheel interface"""
    devname="thorlabs_fw102"
    devcls=Thorlabs.FW
    @pytest.mark.devchange(4)
    def test_motion(self, device):
        pos=device.get_position()
        npos=pos-1 if pos>1 else pos+1
        device.set_position(npos)
        assert device.get_position()==npos
        device.set_position(pos)
        assert device.get_position()==pos