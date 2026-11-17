"""PICam ROI conversion with simulated SDK attributes; no camera is required."""

from types import SimpleNamespace

import pytest

from pylablib.devices.PrincetonInstruments import picam


@pytest.fixture(name="make_camera")
def make_camera_fixture(monkeypatch):
    # Keep the public ROI methods and acquisition-pause decorator intact.
    monkeypatch.setattr(picam.PicamCamera,"open",lambda self: None)
    monkeypatch.setattr(picam.PicamCamera,"acquisition_in_progress",lambda self: False)
    monkeypatch.setattr(picam.PicamCamera,"_deallocate_buffer",lambda self: None)

    def make(constraints):
        cam=picam.PicamCamera()
        cam.ca={"ROIs":SimpleNamespace(cons_roi=constraints,update_limits=lambda: None)}
        cam.cav={"Sensor Active Width":constraints.wrng[1],"Sensor Active Height":constraints.hrng[1]}
        return cam
    return make


@pytest.mark.parametrize("axis",["horizontal","vertical"])
@pytest.mark.parametrize("pstep,sstep",[(0,0),(0,1),(1,0)])
def test_single_pixel_axis(make_camera, axis, pstep, sstep):
    constraints=picam.TROIConstraints(0,1,(0,1020,4),(4,1024,4),[1],(0,0,pstep),(1,1,sstep),[1])
    if axis=="horizontal":
        constraints=picam.TROIConstraints(0,1,constraints.yrng,constraints.hrng,[1],constraints.xrng,constraints.wrng,[1])
    cam=make_camera(constraints)
    expected=(4,1000,0,1,1,1) if axis=="vertical" else (0,1,4,1000,1,1)
    kwargs={"hstart":4,"hend":1000} if axis=="vertical" else {"vstart":4,"vend":1000}
    assert cam.set_roi(**kwargs)==expected
    assert cam.get_roi()==expected
    assert cam.get_data_dimensions()==((1,996) if axis=="vertical" else (996,1))
    # Invalid requests on the fixed axis still clamp to its single legal pixel.
    fixed={"vstart":5,"vend":-1,"vbin":8} if axis=="vertical" else {"hstart":5,"hend":-1,"hbin":8}
    assert cam.set_roi(**dict(kwargs,**fixed))==expected


def test_positive_steps_and_binning(make_camera):
    constraints=picam.TROIConstraints(0,1,(0,1020,4),(4,1024,4),[1,2,4],(0,510,2),(2,512,2),[1,2,4])
    cam=make_camera(constraints)
    assert cam.get_roi_limits(2,2)==((8,1024,4,8,4),(4,512,2,4,4))
    assert cam.set_roi(3,1002,5,510,2,2)==(0,1000,4,508,2,2)
    assert cam.get_data_dimensions()==(252,500)
    assert cam.set_roi(-10,2000,-4,600,8,8)==(0,1024,0,512,4,4)


def test_updated_constraints(make_camera):
    constraints=picam.TROIConstraints(0,1,(0,1020,4),(4,1024,4),None,(0,0,1),(1,1,1),None)
    cam=make_camera(constraints)
    attribute=cam.ca["ROIs"]
    calls=[]
    def update():
        calls.append(True)
        attribute.cons_roi=constraints._replace(yrng=(0,0,0),hrng=(1,1,0))
    attribute.update_limits=update
    assert cam.set_roi()==(0,1024,0,1,1,1)
    assert len(calls)==1
