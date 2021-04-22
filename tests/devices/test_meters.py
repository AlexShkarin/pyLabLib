from .test_basic import DeviceTester

from pylablib.devices import Ophir

class TestOphirVega(DeviceTester):
    """Testing class for PCO SC2 camera interface"""
    devname="ophir_vega"
    devcls=Ophir.VegaPowerMeter

    