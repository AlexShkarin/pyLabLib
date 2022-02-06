import pytest

from pylablib.core.utils import string, files

import os
import re
import time

def parse_dev(dev):
    m=re.match(r"(\w+)(\(.*\))?$",dev)
    return m[1].strip(),string.from_string(m[2]) if m[2] else None
def read_devlist(name):
    devpath=os.path.split(os.path.abspath(__file__))[0]
    with open(os.path.join(devpath,"devlists",name+".cfg"),"r") as f:
        lns=[ln.strip() for ln in f.readlines() if ln.strip()]
        return [ln for ln in lns if ln[0] not in "#;"]
def get_device_list(config):
    devlists=config.getoption("devlists") or config.getoption("fdl")
    devs=[d for dl in devlists for df in dl.split(";") for d in read_devlist(df)]
    devs+=[d.strip() for dl in config.getoption("devices") for d in dl.split(";") if d.strip()]
    devdict=dict([parse_dev(d) for d in devs])
    return devdict


def pytest_collection_modifyitems(config, items):
    only_dev=(config.getoption("devlists") or config.getoption("devices")) and not (config.getoption("full") or config.getoption("fdl"))
    rootdir=config.rootdir
    maxchange=5 if (config.getoption("full") or config.getoption("fdl")) else int(config.getoption("maxchange"))
    for item in items:
        devchange=item.get_closest_marker("devchange")
        if devchange and devchange.args[0]>maxchange:
            item.add_marker(pytest.mark.skip("skipping test with change {} (maxchange = {})".format(devchange.args[0],maxchange)))
        if only_dev:
            skip=True
            try:
                if files.relative_path(item.fspath,rootdir).lower().startswith("devices"):
                    skip=False
            except OSError:
                pass
            if skip:
                item.add_marker(pytest.mark.skip("skipping non-device test"))

@pytest.fixture(scope="class")
def library_parameters():
    pass


class DeviceOpener:
    def __init__(self, devcls, devargs, open_retry, no_conn_fail=False, post_open=False):
        self.devcls=devcls
        self.devargs=devargs
        self.open_retry=open_retry
        self.no_conn_fail=no_conn_fail
        self.post_open=post_open
        self.device=None
        self.failed=False
    def _fail(self):
        devargstr=", ".join([str(a) for a in self.devargs])
        pytest.xfail("couldn't connect to the device {}({})".format(self.devcls.__name__,devargstr))
    def open(self):
        if self.device is not None:
            return self.device
        if self.failed:
            self._fail()
        try:
            for i in range(self.open_retry+1):
                try:
                    self.device=self.devcls(*self.devargs)
                    if self.post_open:
                        self.post_open(self.device)
                    return self.device
                except Exception:
                    if i==self.open_retry:
                        raise
                    time.sleep(1.)
        except Exception:
            self.failed=True
            if self.no_conn_fail:
                self._fail()
            else:
                raise
    def close(self):
        if self.device is not None:
            self.device.close()
            self.device=None
    def __call__(self):
        return self.open()


@pytest.fixture(scope="class")
def devopener(request, library_parameters):
    devcls=request.cls.devcls
    devargs=getattr(request.cls,"devargs",())
    open_retry=getattr(request.cls,"open_retry",0)
    post_open=getattr(request.cls,"post_open",None)
    devname=request.cls.devname
    devlist=get_device_list(request.config)
    if devname not in devlist:
        pytest.skip("skipping test of missing device {}".format(devname))
    elif devlist[devname] is not None:
        devargs=devlist[devname]
    opener=DeviceOpener(devcls,devargs,open_retry,no_conn_fail=request.config.getoption("dev_no_conn_fail"),post_open=post_open)
    try:
        yield opener
    finally:
        opener.close()



@pytest.fixture
def stress_factor(request):
    return int(request.config.getoption("stressfactor"))