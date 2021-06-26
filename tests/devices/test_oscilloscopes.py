from .test_basic import DeviceTester

from pylablib.devices import Tektronix

import pytest
import time
import numpy as np

class GenericOscilloscopeTester(DeviceTester):
    """Testing a generic oscilloscope"""
    
    @pytest.mark.devchange(4)
    def test_grab(self, devopener):
        """Test trace readout"""
        device=devopener()
        channels=list(range(1,device.get_channels_number()+1))
        for ch in channels:
            device.enable_channel(ch)
        device.set_trigger_mode("auto")
        assert device.get_trigger_mode()=="auto"
        device.grab_continuous()
        assert device.is_grabbing()
        time.sleep(2.)
        device.stop_grabbing()
        assert not device.is_grabbing()
        traces=device.read_multiple_sweeps(channels)
        wfmpre=device.get_wfmpre(channels)
        traces_pre=device.read_multiple_sweeps(channels,wfmpres=wfmpre)
        assert [np.all(t==tp) for t,tp in zip(traces,traces_pre)]



class TestTektronixTDS2000(GenericOscilloscopeTester):
    """Testing class for Tektronix TDS2000 series oscilloscope"""
    devname="tektronix_tds2000"
    devcls=Tektronix.TDS2000