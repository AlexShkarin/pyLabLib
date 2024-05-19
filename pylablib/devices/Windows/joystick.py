from ...core.devio import interface
from ...core.utils import py3

from . import winmm_lib
from .winmm_lib import WinMMError

import threading
import collections
import time


TDeviceInfo=collections.namedtuple("TDeviceInfo",["name","id","nbuttons","naxes"])
def _get_device_info(caps):
    return TDeviceInfo(py3.as_str(caps.szPname),(caps.wMid,caps.wPid),caps.wNumButtons,caps.wNumAxes)
def list_joysticks():
    """List all detected joysticks"""
    lib=winmm_lib.WinMMLib()
    js={}
    for i in range(lib.joyGetNumDevs()):
        try:
            caps=lib.joyGetDevCapsA(i)
            if caps.szPname and caps.wMid and caps.wPid:
                js[i]=_get_device_info(caps)
        except WinMMError:
            pass
    return js

TJoystickEvent=collections.namedtuple("TJoystickEvent",["kind","index","old","new","timestamp"])
TJoystickEventEx=collections.namedtuple("TJoystickEventEx",["kind","index","old","new","state","timestamp"])
class Joystick(interface.IDevice):
    """
    Generic Windows joystick device.

    Args:
        idx: joystick index (0-based) in the list returned by :func:`list_joysticks`; if ``None``, use the first valid index.
        expanded_events (bool): if ``True``, the events include the full joystick state; otherwise, they only record the change of the state at the particular event
    """
    Error=WinMMError
    def __init__(self, idx=None, expanded_events=False):
        super().__init__()
        if idx is None:
            js=list_joysticks()
            idx=min(js) if js else 0
        self.lib=winmm_lib.WinMMLib()
        self.idx=idx
        self.caps=self.lib.joyGetDevCapsA(self.idx)
        self.buttons=[False]*self.caps.wNumButtons
        self.axes=[0]*min(self.caps.wNumAxes,3)
        self._axes_limits=[(self.caps.wXmin,self.caps.wXmax),(self.caps.wYmin,self.caps.wYmax),(self.caps.wZmin,self.caps.wZmax)][:len(self.axes)]
        self.evts=[]
        self.expanded_events=expanded_events
        self._thread=None
        self._lock=threading.Lock()
        self._looping=False
        self._max_events=2**16
        self._update_state(update_events=False)
        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("buttons",self.get_buttons)
        self._add_status_variable("axes",self.get_axes)
    def open(self):
        self._opened=True
    def close(self):
        try:
            self.stop()
        finally:
            self._opened=False
    def is_opened(self):
        return self._opened
    def _get_connection_parameters(self):
        return (self.idx,self.expanded_events)
    def start(self):
        """Start the polling loop (used for events recording)"""
        self.stop()
        self._thread=threading.Thread(target=self._loop_update,daemon=True)
        self._looping=True
        self._thread.start()
    def stop(self):
        """Stop the polling loop"""
        if self._thread is None:
            return
        self._looping=False
        self._thread.join()
        self._thread=None
    def _loop_update(self):
        while self._looping:
            self._update_state()
            time.sleep(1E-3)
    def get_device_info(self):
        """
        Get joystick info.

        Return tuple ``(name, id, nbuttons, naxes)``.
        """
        return _get_device_info(self.caps)
    def _update_state(self, update_events=True):
        info=self.lib.joyGetPos(self.idx)
        nbuttons=[bool(info.wButtons&(1<<i)) for i in range(len(self.buttons))]
        naxes=[info.wXpos,info.wYpos,info.wZpos][:len(self.axes)]
        naxes=[(ax-minax)/(maxax-minax)*2-1 for ax,(minax,maxax) in zip(naxes,self._axes_limits)]
        t=time.time()
        with self._lock:
            if update_events:
                for i,(b,nb) in enumerate(zip(self.buttons,nbuttons)):
                    if b!=nb:
                        if self.expanded_events:
                            self.evts.append(TJoystickEventEx("button",i,b,nb,(tuple(self.buttons),tuple(self.axes)),t))
                        else:
                            self.evts.append(TJoystickEvent("button",i,b,nb,t))
                for i,(a,na) in enumerate(zip(self.axes,naxes)):
                    if a!=na:
                        if self.expanded_events:
                            self.evts.append(TJoystickEventEx("axis",i,a,na,(tuple(self.buttons),tuple(self.axes)),t))
                        else:
                            self.evts.append(TJoystickEvent("axis",i,a,na,t))
                if len(self.evts)>self._max_events:
                    self.evts=self.evts[-self._max_events]
            self.axes=naxes
            self.buttons=nbuttons
    def get_buttons(self):
        """Get the buttons state as a list"""
        if self._thread is None:
            self._update_state(update_events=False)
        return list(self.buttons)
    def get_axes(self):
        """Get the axes state as a list"""
        if self._thread is None:
            self._update_state(update_events=False)
        return list(self.axes)
    def get_events(self, n=None, clear=True):
        """
        Get recent joystick events.
        
        Note that in order to capture events, one needs to call the ``start`` method first to start the event loop.
        `n` specifies the number of oldest uncleared events to get (by default, all events).
        If ``clear==True``, remove all returned events from the queue.
        """
        with self._lock:
            if n is None or n>=len(self.evts):
                if clear:
                    result=self.evts
                    self.evts=[]
                    return result
                return list(self.evts)
            result=self.evts[:n]
            if clear:
                del self.evts[:n]
            return result