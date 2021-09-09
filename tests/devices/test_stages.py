from pylablib.devices import Attocube
from pylablib.devices import Arcus
from pylablib.devices import Newport
from pylablib.devices import SmarAct
from pylablib.devices import Trinamic
from pylablib.devices import Thorlabs

import pylablib

from .test_basic import DeviceTester

import pytest


class TestANC300(DeviceTester):
    """Testing class for Attocube ANC300 stage interface"""
    devname="attocube_anc300"
    devcls=Attocube.ANC300


class TestANC350(DeviceTester):
    """Testing class for Attocube ANC350 stage interface"""
    devname="attocube_anc350"
    devcls=Attocube.ANC350


class TestArcusPerformax(DeviceTester):
    """Testing class for Arcus Performax stage interface"""
    devname="arcus_performax"
    devcls=Arcus.Performax4EXStage
    open_retry=3

    get_set_all_exclude=["analog_input"]
    @pytest.fixture(scope="class")
    def library_parameters(self):
        pylablib.par["devices/dlls/arcus_performax"]="../dlls"


class TestNewportPicomotor8742(DeviceTester):
    """Testing class for Newport Picomotor 8742 controller interface"""
    devname="newport_picomotor8742"
    devcls=Newport.Picomotor8742
    open_retry=3


class TestSmarActSCUPerformax(DeviceTester):
    """Testing class for SmarAct SCU stage interface"""
    devname="smaract_scu3d"
    devcls=SmarAct.SCU3D
    open_retry=3

    @pytest.fixture(scope="class")
    def library_parameters(self):
        pylablib.par["devices/dlls/smaract_scu3d"]="../dlls"


class TestTrinamicTMCM1110(DeviceTester):
    """Testing class for Trinamic TMCM1110 stage interface"""
    devname="trinamic_tmcm1110"
    devcls=Trinamic.TMCM1110
    open_retry=3


class TestKinesisMotor(DeviceTester):
    """Testing class for Thorlabs Kinesis stage interface"""
    devname="thorlabs_kinesis_motor"
    devcls=Thorlabs.KinesisMotor
    open_retry=3