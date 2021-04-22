def pytest_addoption(parser):
    parser.addoption("--devices",action="append",default=[],help="list of device names to test",)
    parser.addoption("--devlists",action="append",default=[],help="list of device list files",)
    parser.addoption("--maxchange",default=2,help="maximal allowed change to the device state while testing",)
    parser.addoption("--stressfactor",default=1,help="stress multiplication factor",)
    parser.addoption("--full",action="store_true",help="run maximally complete tests",)