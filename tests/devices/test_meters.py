from .test_basic import DeviceTester

from pylablib.devices import Ophir
from pylablib.devices import Lakeshore
from pylablib.devices import Pfeiffer
from pylablib.devices import HighFinesse
from pylablib.devices import Cryomagnetics


class TestOphirVega(DeviceTester):
    """Testing class for Ophir Vega power meter"""
    devname="ophir_vega"
    devcls=Ophir.VegaPowerMeter
    open_retry=3


class TestLakeshore218(DeviceTester):
    """Testing class for Lakeshore 218 temperature sensor"""
    devname="lakeshore218"
    devcls=Lakeshore.Lakeshore218
    open_retry=3


class TestCryomagneticsLM500(DeviceTester):
    """Testing class for Cryomagnetics LM500 level meter"""
    devname="cryomagnetics_lm500"
    devcls=Cryomagnetics.LM500
    open_retry=3


class TestPfeifferTPG260(DeviceTester):
    """Testing class for TPG260 pressure sensor"""
    devname="pfeiffer_tpg260"
    devcls=Pfeiffer.TPG260
    open_retry=3
    get_set_all_exclude=["calibration_factor"]


class TestWLMWavemeter(DeviceTester):
    """Testing class for High Finesse WLM wavemeter"""
    devname="high_finesse_wlm"
    devcls=HighFinesse.WLM