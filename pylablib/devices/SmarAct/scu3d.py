from .SCU3DControl_lib import wlib as lib, SmarActError, EConfiguration
from ...core.utils import general
from ...core.devio import interface
from ..interface import stage

from ..utils import load_lib

import collections
import time


class LibraryController(load_lib.LibraryController):
    def _do_init(self):
        lib.SA_InitDevices(EConfiguration.SA_SYNCHRONOUS_COMMUNICATION)
    def _do_uninit(self):
        try:
            self.lib.SA_ReleaseDevices()
        except SmarActError:
            pass
libctl=LibraryController(lib)


TDeviceInfo=collections.namedtuple("TDeviceInfo",["device_id","firmware_version","dll_version"])
def _parse_version(v):
    return "{}.{}.{}.{}".format(*[(v>>(n*8))&0xFF for n in range(4)][::-1])
def get_device_info(idx):
    """
    Get info of the devices with the given index.

    Return tuple ``(device_id, firmware_version, dll_version)``.
    """
    with libctl.temp_open():
        try:
            device_id=lib.SA_GetDeviceID(idx)
            dll_version=_parse_version(lib.SA_GetDLLVersion())
            firmware_version=_parse_version(lib.SA_GetDeviceFirmwareVersion(idx))
            return TDeviceInfo(device_id,dll_version,firmware_version)
        except SmarActError:
            return None
def list_devices():
    """List all connected devices"""
    with libctl.temp_open():
        try:
            n=lib.SA_GetNumberOfDevices()
            infos=[get_device_info(i) for i in range(n)]
            return [i for i in infos if i is not None]
        except SmarActError:
            return []
def get_devices_number():
    """Get number of connected SCU3D controller"""
    with libctl.temp_open():
        try:
            return lib.SA_GetNumberOfDevices()
        except SmarActError:
            return 0

class SCU3D(stage.IMultiaxisStage):
    """
    SmarAct SCU3D translation stage controller.

    Args:
        idx(int): stage index
        axis_dir(str): 3-symbol string specifying default directions of the axes (each symbol be ``"+"`` or ``"-"``)
    """
    Error=SmarActError
    _axes=list("xyz")
    def __init__(self, idx=0, axis_dir="+++"):
        super().__init__()
        self.idx=idx
        self.axis_dir=list(axis_dir)
        self._opid=None
        self.open()
        self._add_info_variable("device_info",self.get_device_info)
        self._add_settings_variable("axis_dir",self.get_axis_dir,self.set_axis_dir)
        self._add_status_variable("axis_status",self.get_status)
        self._add_status_variable("moving",self.is_moving)

    def _get_connection_parameters(self):
        return self.idx
    def open(self):
        """Open the connection to the stage"""
        if self._opid is None:
            with libctl.temp_open():
                nstages=get_devices_number()
                if self.idx>=nstages:
                    raise SmarActError("stage index {} is not available ({} stage exist)".format(self.idx,nstages))
                self._opid=libctl.open().opid
    def close(self):
        """Close the connection to the stage"""
        if self._opid is not None:
            libctl.close(self._opid)
            self._opid=None
    def is_opened(self):
        return self._opid is not None

    def _parse_version(self, v):
        return "{}.{}.{}.{}".format(*[(v>>(n*8))&0xFF for n in range(4)][::-1])
    def get_device_info(self):
        """
        Get info of the devices with the given index.

        Return tuple ``(device_id, firmware_version, dll_version)``.
        """
        return get_device_info(self.idx)

    def get_axis_dir(self):
        """Get axis direction convention (a string of 3 symbols which are either ``"+"`` or ``"-"`` determining if the axis direction is flipped)"""
        return list(self.axis_dir)
    def set_axis_dir(self, axis_dir):
        """Set axis direction convention (a string of 3 symbols which are either ``"+"`` or ``"-"`` determining if the axis direction is flipped)"""
        self.axis_dir=list(axis_dir)
        return self.get_axis_dir()

    def _axisn(self, axis):
        return self._axes.index(axis)
    @interface.use_parameters
    def move_macrostep(self, axis, steps, voltage, frequency):
        """
        Move along a given axis by a single "macrostep", which consists of several regular steps.

        `voltage` (in Volts) and `frequency` (in Hz) specify the motion parameters.
        This simulates the controller operation, where one "step" at large step sizes consists of several small steps.
        """
        axisn=self._axisn(axis)
        axis_dir=-1 if self.axis_dir[axisn]=="-" else 1
        lib.SA_MoveStep_S(self.idx,axisn,int(steps)*axis_dir,int(voltage*10),int(frequency))
    _move_presets=[ (1,25.3,1E3), (1,28,1E3), (1,32,1E3), (1,38,1E3), (1,47,1E3),
                    (1,60.5,1E3), (1,80.8,1E3), (2,65.6,1E3), (2,88.4,1E3), (4,88.4,1E3),
                    (7,100.,1E3), (14,100.,1E3), (28,100.,1E3), (56,100.,1.1E3), (100,100.,2.2E3), 
                    (200,100.,4.4E3), (400,100.,8.8E3), (1E3,100.,10E3), (1.8E3,100.,10E3)]
    def move_by(self, axis, steps=1, stepsize=10):
        """
        Move along a given axis with a given number of macrosteps using one of the predefined step size.

        `stepsize` can range from 1 (smallest) to 20 (largest), and roughly corresponds to the handheld controller parameters.
        """
        par=self._move_presets[max(stepsize-1,0)]
        step_dir=1 if steps>0 else -1
        for _ in range(abs(steps)):
            self.move_macrostep(axis,par[0]*step_dir,par[1],par[2])
            self.wait_move(axis)

    _chan_status={  0:"stopped",
                    1:"setting_amplitude",
                    2:"moving",
                    3:"targeting",
                    4:"holding",
                    5:"calibrating",
                    6:"moving_to_reference"}
    _p_channel_status=interface.EnumParameterClass("channel_status",general.invert_dict(_chan_status))
    def _get_status_n(self, axis):
        return lib.SA_GetStatus_S(self.idx,self._axisn(axis))
    @stage.muxaxis
    @interface.use_parameters(_returns="channel_status")
    def get_status(self, axis="all"):
        """
        Get the axis status.
        
        Can be ``"stopped"`` (default state), ``"setting_amplitude"`` (setting open-loop step amplitude),
        ``"moving"`` (open-loop movement), ``"targeting"`` (closed-loop movement),
        ``"holding"`` (closed-loop position holding), ``"calibrating"`` (sensor calibration),
        or ``"moving_to_reference"`` (calibrating position sensor).
        """
        return self._get_status_n(axis)
    @interface.use_parameters(status="channel_status")
    def wait_for_status(self, axis, status="stopped", timeout=30.):
        """
        Wait until the axis reaches a given status.

        By default wait for ``"stopped"`` status (i.e., wait until the motion is finished).
        """
        countdown=general.Countdown(timeout)
        while True:
            cur_status=self._get_status_n(axis)
            if cur_status==status:
                return
            if countdown.passed():
                raise SmarActError("status waiting timed out")
            time.sleep(1E-2)
    def wait_move(self, axis, timeout=30.):
        """Wait for a given axis to stop moving"""
        if axis=="all":
            for ax in self.get_all_axes():
                self.wait_move(ax,timeout=timeout)
            return
        return self.wait_for_status(axis,timeout=timeout)
    @stage.muxaxis
    def is_moving(self, axis="all"):
        """Check if a given axis is moving"""
        return self.get_status(axis)=="moving"

    @stage.muxaxis
    @interface.use_parameters
    def stop(self, axis="all"):
        """Stop motion at a given axis"""
        lib.SA_Stop_S(self.idx,self._axisn(axis))