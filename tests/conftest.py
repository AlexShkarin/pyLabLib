import os
import pytest

def pytest_addoption(parser):
    parser.addoption("--devices",action="append",default=[],help="list of device names to test",)
    parser.addoption("--devlists",action="append",default=[],help="list of device list files",)
    parser.addoption("--maxchange",default=2,help="maximal allowed change to the device state while testing",)
    parser.addoption("--dev-no-conn-fail",action="store_true",help="xfail instead of fail if could not connect to the device",)
    parser.addoption("--stressfactor",default=1,help="stress multiplication factor",)
    parser.addoption("--full",action="store_true",help="run maximally complete tests",)
    parser.addoption("--fdl",action="append",default=[],help="combination of --devlists and --full",)


@pytest.fixture(scope="session")
def root_path():
    """Path containing the root test folder"""
    return os.path.split(os.path.abspath(__file__))[0]