from . import SCU3DControl_lib
from ...core.utils import general
from ...core.devio import interface

import time

class SmarActError(RuntimeError):
    """Generic SmarAct error"""

class SCU3D(interface.IDevice):
    """
    SmarAct SCU3D translation stage.

    Args:
        idx(int): stage index
        axis_mapping(str): 3-symbol string specifying indices of x, y and z axes (can be any permutation of ``"xyz"``)
        axis_dir(str): 3-symbol string specifying default directions of the axes (each symbol be ``"+"`` or ``"-"``)
    """
    def __init__(self, idx=0, axis_mapping="xyz", axis_dir="+++"):
        interface.IDevice.__init__(self)
        self.lib=SCU3DControl_lib.lib
        self.lib.initlib()
        self.connected=False
        self.idx=idx
        self.axis_mapping=axis_mapping
        self.axis_dir=axis_dir
        self.open()
        self._add_settings_variable("axis_mapping",self.get_axis_mapping,self.set_axis_mapping)
        self._add_settings_variable("axis_dir",self.get_axis_dir,self.set_axis_dir)
        self._add_status_variable("axis_status",self.get_status,mux=("xyz",))
        self._add_status_variable("moving",self.is_moving,mux=("xyz",))

    def open(self):
        """Open the connection to the stage"""
        if not self.connected:
            self.lib.SA_InitDevices(SCU3DControl_lib.EConfiguration.SA_SYNCHRONOUS_COMMUNICATION)
            self.connected=True
    def close(self):
        """Close the connection to the stage"""
        if self.connected:
            self.lib.SA_ReleaseDevices()
            self.connected=False
    def is_opened(self):
        return self.connected

    def get_axis_mapping(self):
        """Get axis mapping (a permutation of ``"xyz"`` describing the correspondence between these axes and channel numbers)"""
        return self.axis_mapping
    def set_axis_mapping(self, mapping):
        """Set axis mapping (a permutation of ``"xyz"`` describing the correspondence between these axes and channel numbers)"""
        self.axis_mapping=mapping
        return self.get_axis_mapping()
    def get_axis_dir(self):
        """Get axis direction convention (a string of 3 symbols which are either ``"+"`` or ``"-"`` determining if the axis direction is flipped)"""
        return self.axis_dir
    def set_axis_dir(self, axis_dir):
        """Set axis direction convention (a string of 3 symbols which are either ``"+"`` or ``"-"`` determining if the axis direction is flipped)"""
        self.axis_dir=axis_dir
        return self.get_axis_dir()

    def _get_axis(self, axis):
        if axis in list(self.axis_mapping):
            return self.axis_mapping.find(axis)
        return axis
    def move_macrostep(self, axis, steps, voltage, frequency):
        """
        Move along a given axis by a single "macrostep", which consists of several regular steps.

        `voltage` (in Volts) and `frequency` (in Hz) specify the motion parameters.
        This simulates the controller operation, where one "step" at large step sizes consists of several small steps.
        """
        axis=self._get_axis(axis)
        axis_dir=-1 if self.axis_dir[axis]=="-" else 1
        self.lib.SA_MoveStep_S(self.idx,axis,int(steps)*axis_dir,int(voltage*10),int(frequency))
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
    def get_status(self, axis):
        """
        Get the axis status.
        
        Can be ``"stopped"`` (default state), ``"setting_amplitude"`` (setting open-loop step amplitude),
        ``"moving"`` (open-loop movement), ``"targeting"`` (closed-loop movement),
        ``"holding"`` (closed-loop position holding), ``"calibrating"`` (sensort calibration),
        or ``"moving_to_reference"`` (calibrating position sensor).
        """
        status=self.lib.SA_GetStatus_S(self.idx,self._get_axis(axis))
        return self._chan_status[status]
    def wait_for_status(self, axis, status="stopped", timeout=3.):
        """
        Wait until the axis reaches a given status.

        By default wait for ``"stopped"`` status (i.e., wait until the motion is finished).
        """
        countdown=general.Countdown(timeout)
        while True:
            cur_status=self.get_status(axis)
            if cur_status==status:
                return
            if countdown.passed():
                raise SmarActError("status waiting timed out")
            time.sleep(1E-2)
    def wait_move(self, axis, timeout=3.):
        """Wait for a given axis to stop moving."""
    def is_moving(self, axis):
        """Check if a given axis is moving"""
        return self.get_status(axis)=="moving"