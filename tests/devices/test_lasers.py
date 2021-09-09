from .test_basic import DeviceTester

from pylablib.devices import LighthousePhotonics
from pylablib.devices import LaserQuantum
from pylablib.devices import Toptica
from pylablib.devices import M2


class TestLPSproutG(DeviceTester):
    """Testing class for Lighthouse Photonics SproutG laser"""
    devname="lp_sprout"
    devcls=LighthousePhotonics.SproutG
    open_retry=3


class TestLQFinesse(DeviceTester):
    """Testing class for LaserQuantum Finesse laser"""
    devname="lq_finesse"
    devcls=LaserQuantum.Finesse
    open_retry=3


class TestTopticaIBeam(DeviceTester):
    """Testing class for Toptica iBeam Smar laser"""
    devname="toptica_ibeam"
    devcls=Toptica.TopticaIBeam
    open_retry=3


class TestM2Solstis(DeviceTester):
    """Testing class for M2 Solstis laser"""
    devname="m2_solstis"
    devcls=M2.Solstis