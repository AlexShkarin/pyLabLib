import pytest

from pylablib.core.utils import string, files

import os
import re

def parse_dev(dev):
    m=re.match(r"(\w+)(\(.*\))?$",dev)
    return m[1].strip(),string.from_string(m[2]) if m[2] else None
def read_devlist(name):
    with open(os.path.join("devices","devlists",name+".cfg"),"r") as f:
        lns=[ln.strip() for ln in f.readlines() if ln.strip()]
        return [ln for ln in lns if ln[0] not in "#;"]
def get_device_list(config):
    devs=[d for dl in config.getoption("devlists") for df in dl.split(";") for d in read_devlist(df)]
    devs+=[d.strip() for dl in config.getoption("devices") for d in dl.split(";") if d.strip()]
    devdict=dict([parse_dev(d) for d in devs])
    return devdict


def pytest_collection_modifyitems(config, items):
    only_dev=(config.getoption("devlists") or config.getoption("devices")) and not config.getoption("full")
    rootdir=config.rootdir
    maxchange=5 if config.getoption("full") else int(config.getoption("maxchange"))
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

@pytest.fixture(scope="class")
def device(request, library_parameters):
    devcls=request.cls.devcls
    devargs=getattr(request.cls,"devargs",())
    open_retry=getattr(request.cls,"open_retry",0)
    devname=request.cls.devname
    devlist=get_device_list(request.config)
    if devname not in devlist:
        pytest.skip("skipping test of missing device {}".format(devname))
    elif devlist[devname] is not None:
        devargs=devlist[devname]
    open_rep=getattr(request.cls,"open_rep",0)
    opened=False
    try:
        try:
            for i in range(open_retry+1):
                try:
                    dev=devcls(*devargs)
                    break
                except Exception:
                    if i==open_retry:
                        raise
        except Exception:
            devargstr=", ".join([str(a) for a in devargs])
            pytest.xfail("couldn't connect to the device {}({})".format(devcls.__name__,devargstr))
        opened=True
        for _ in range(open_rep):
            dev.close()
            opened=False
            for i in range(open_retry+1):
                try:
                    dev.open()
                    break
                except Exception:
                    if i==open_retry:
                        raise
            opened=True
        yield dev
    finally:
        if opened:
            dev.close()


@pytest.fixture
def stress_factor(request):
    return int(request.config.getoption("stressfactor"))