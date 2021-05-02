from .test_basic import DeviceTester

from pylablib.devices import Ophir
from pylablib.devices import Lakeshore
from pylablib.devices import Pfeiffer


class TestOphirVega(DeviceTester):
    """Testing class for Ophir Vega power meter"""
    devname="ophir_vega"
    devcls=Ophir.VegaPowerMeter


class TestLakeshore218(DeviceTester):
    """Testing class for Lakeshore 218 temperature sensor"""
    devname="lakeshore218"
    devcls=Lakeshore.Lakeshore218


class TestPfeifferTPG260(DeviceTester):
    """Testing class for TPG260 pressure sensor"""
    devname="pfeiffer_tpg260"
    devcls=Pfeiffer.TPG260
    get_set_all_exclude=["calibration_factor"]