from ...core.devio import comm_backend, interface
from ...core.utils import general, py3

from ..interface import stage
from .base import NewportError, NewportBackendError

import time
import collections


def get_usb_devices_number():
    """Get the number of controllers connected via USB"""
    devs=comm_backend.PyUSBDeviceBackend.list_resources(idVendor=0x104D,idProduct=0x4000)
    return len(devs)


def muxaddr(*args, **kwargs):
    """Multiplex the function over its addr argument"""
    if len(args)>0:
        return muxaddr(**kwargs)(args[0])
    def addr_func(self, *_, **__):
        return self._addr_list
    return general.muxcall("addr",special_args={"all":addr_func},mux_argnames=kwargs.get("mux_argnames",None),return_kind=kwargs.get("return_kind","dict"),allow_partial=True)
TDeviceInfo=collections.namedtuple("TDeviceInfo",["id"])
class Picomotor8742(comm_backend.ICommBackendWrapper,stage.IMultiaxisStage):
    """
    Picomotor 8742 4-axis controller.

    Args:
        conn: connection parameters; can be an index (starting from 0) for USB devices,
            or an IP address (e.g., ``"192.168.0.2"``) or host name (e.g., ``"8742-12345"``) for Ethernet devices
        backend: communication backend; by default, try to determine from the communication parameters
        timeout(float): default operation timeout
        multiaddr: if ``True``, assume that there are several daisy-chained devices connected to the current one;
            in this case, ``get_device_info`` and related methods return dictionaries ``{addr: value}`` for all connected controllers
            instead of simply values for the given controller
        scan: if ``True`` and ``multiaddr==True``, scan for all connected devices (call :meth:`scan_devices`) upon connection
    """
    Error=NewportError
    _axes=[1,2,3,4]
    def __init__(self, conn=0, backend="auto", timeout=5., multiaddr=False, scan=True):
        if isinstance(conn,int):
            conn=(0x104D,0x4000,conn,0x81,0x02) # default device IDs
            backend="pyusb"
        backend=comm_backend.autodetect_backend(conn,default="network") if backend=="auto" else backend
        defaults={"network":{"port":23}}
        term_write="\n\r" if comm_backend.autodetect_backend(conn,"network")=="pyusb" else "\n"
        instr=comm_backend.new_backend(conn,backend=backend,timeout=timeout,term_write=term_write,term_read="\n",defaults=defaults,reraise_error=NewportBackendError)
        time.sleep(0.01)
        instr.flush_read()
        self._addr_list=None
        self._multiaddr=multiaddr
        super().__init__(instr)
        try:
            self.get_id()
        except instr.Error:
            self.close()
            raise NewportError("error connecting to the Picomotor controller")
        if multiaddr:
            if scan:
                self.scan_devices()
            self.get_addr_map()
        self._add_info_variable("device_info",self.get_device_info)
        self._add_status_variable("ethernet_parameters",self.get_ethernet_parameters,priority=-2)
        self._add_status_variable("addr_map",self.get_addr_map)
        self._add_status_variable("motor_type",lambda: self.get_motor_type(addr="all"))
        self._add_status_variable("position",lambda: self.get_position(addr="all"))
        self._add_settings_variable("velocity_parameters",lambda: self.get_velocity_parameters(addr="all"),self._setup_all_velocity)
        self._add_status_variable("moving",lambda: self.is_moving(addr="all"))
    
    def query(self, comm, axis=None, addr=None, read_reply=None):
        if axis is not None:
            comm="{}{}".format(axis,comm)
        if addr is not None:
            addr_header="{}>".format(addr)
            comm=addr_header+comm
        self.instr.write(comm)
        if read_reply is None:
            read_reply=comm.endswith("?")
        if read_reply:
            reply=py3.as_str(self.instr.readline().strip())
            if addr is not None:
                if not reply.startswith(addr_header):
                    raise NewportError("unexpected reply: expected reply starting with '{}', got '{}'".format(addr_header,reply))
                reply=reply[len(addr_header):]
            return reply

    @muxaddr
    def get_id(self, addr=None):
        """Get the device identification string"""
        return self.query("*IDN?",addr=addr)
    @muxaddr
    def get_device_info(self, addr=None):
        """Get the device info of the controller board: ``(id_string,)``"""
        return TDeviceInfo(self.get_id(addr=addr))
    
    @muxaddr
    def reset(self, addr=None):
        """
        Restart the device.
        
        Reboots the CPU and restores all saved settings from the parameter memory.
        """
        self.query("*RST",addr=addr)
        time.sleep(5.)
        return self.get_id(addr=addr)
    @muxaddr
    def save_parameters(self, addr=None):
        """
        Store current parameters to the non-volatile memory.

        Affects axes speed and acceleration, motor types, and Ethernet parameters.
        """
        self.query("SM",addr=addr)
    _p_param_src=interface.EnumParameterClass("param_src",{"factory":0,"memory":1})
    @muxaddr
    @interface.use_parameters(src="param_src")
    def restore_parameters(self, src="memory", addr=None):
        """
        Restore parameters from the non-volatile memory (if ``src=="memory"``) for factory parameters (if ``src=="factory"``).

        Affects axes speed and acceleration, motor types, and Ethernet parameters.
        """
        self.query("*RCL{}".format(src),addr=addr)
    
    _p_reassign=interface.EnumParameterClass("reassign",{"none":0,"conflict":1,"all":2})
    @interface.use_parameters
    def scan_devices(self, reassign="conflict", sync=True):
        """
        Scan for devices connected to the current host device via RS-485 daisy-chaining.

        `reassign` controls how device addresses are assigned during the scan;
        can be ``"none"`` (keep current values; can lead to conflicts if several devices have the same address),
        ``"conflict"`` (change conflicting addresses), or ``"all"`` (assigned all new addresses in sequence starting from the host)

        If ``sync==True``, wait until the scan is done (might take several seconds).
        """
        self.query("SC{}".format(reassign))
        if sync:
            self.wait_for_scan()
            return self.get_addr_map()
    def get_addr_map(self):
        """
        Get address map for devices connected to the current host device via RS-485 daisy-chaining.

        Return tuple ``(addresses, conflict)``, where ``addresses`` is the list of all device addresses,
        and ``conflict==True`` if there address conflicts (several devices having the same address).
        """
        value=int(self.query("SC?"))
        addr_list=[addr for addr in range(1,32) if value&(1<<addr)]
        if self._multiaddr:
            self._addr_list=addr_list
        return addr_list, bool(value%1)
    def wait_for_scan(self, timeout=10.):
        """Wait for the device connection scan to finish"""
        ctd=general.Countdown(timeout)
        while True:
            if int(self.query("SD?")):
                return
            if ctd.passed():
                raise NewportError("timeout while waiting for network scan")
    @muxaddr
    def get_addr(self, addr=None):
        """Get RS-485 address of the given device (host if `addr` is ``None``)"""
        return int(self.query("SA?",addr=addr))
    @muxaddr
    def set_addr(self, new_addr, addr=None):
        """Set RS-485 address of the given device (host if `addr` is ``None``)"""
        self.query("SA{}".format(new_addr),addr=addr)
        return self.get_addr(addr=addr)
    
    
    _p_ipmode=interface.EnumParameterClass("ipmode",{"static":0,"dhcp":1})
    @muxaddr
    def get_ethernet_parameters(self, addr=None):
        """
        Get Ethernet connection parameters.

        Return tuple ``(hostname, ipaddr, ipmode, gateway, netmask)``.
        """
        ipmode="dhcp" if int(self.query("IPMODE?",addr=addr)) else "static"
        params=[self.query(q,addr=addr) for q in ["HOSTNAME?","IPADDR?","GATEWAY?","NETMASK?"]]
        return tuple(params[:1]+[ipmode]+params[1:])
    @muxaddr
    @interface.use_parameters
    def setup_ethernet(self, hostname=None, ipmode=None, ipaddr=None, gateway=None, netmask=None, addr=None):
        """
        Setup Ethernet connection parameters.

        Any ``None`` value remains unchanged.
        Note that these settings only take effect after saving parameters to the memory (:meth:`save_parameters`)
        and restarting the device (:meth:`reset`). If the connection is made through Ethernet, then it will likely be invalidated,
        in which case a new device object with the updated parameters should be created after reset.
        """
        if hostname is not None:
            self.query("HOSTNAME {}".format(hostname),addr=addr)
        if ipmode is not None:
            self.query("IPMODE{}".format(ipmode),addr=addr)
        if ipaddr is not None:
            self.query("IPADDR {}".format(ipaddr),addr=addr)
        if gateway is not None:
            self.query("GATEWAY {}".format(gateway),addr=addr)
        if netmask is not None:
            self.query("NETMASK {}".format(netmask),addr=addr)
        return self.get_ethernet_parameters()

    @muxaddr
    def autodetect_motors(self, addr=None):
        """
        Autodetect connected motors.

        The command involves sending single-step commands to the motors, so it requires all axes to be stopped,
        and it might slightly affect the current position.
        After the detection the types can be stored in the memory via :meth:`save_parameters`.
        """
        self.query("MC",addr=addr)
        self.wait_move("all",addr=addr)
        return self.get_motor_type()
    _p_motor_type=interface.EnumParameterClass("motor_type",{"none":0,"unknown":1,"tiny":2,"standard":3})
    @muxaddr
    @stage.muxaxis
    @interface.use_parameters(_returns="motor_type")
    def get_motor_type(self, axis="all", addr=None):
        """Get type of the given axis motor"""
        return int(self.query("QM?",axis=axis,addr=addr))
    @muxaddr
    @stage.muxaxis(mux_argnames="motor_type")
    @interface.use_parameters
    def set_motor_type(self, axis="all", motor_type="standard", addr=None):
        """Manually set type of the given axis motor"""
        self.query("QM{}".format(motor_type),axis=axis,addr=addr)
        return self.get_motor_type(axis=axis,addr=addr)

    @muxaddr
    @stage.muxaxis
    def move_to(self, axis, position, addr=None):
        """Move to a given position"""
        self.query("PA{}".format(position),axis=axis,addr=addr)
    @muxaddr
    @stage.muxaxis
    def move_by(self, axis, steps=1, addr=None):
        """Move by a given number of steps"""
        self.query("PR{}".format(steps),axis=axis,addr=addr)
    @muxaddr
    @stage.muxaxis
    def get_position(self, axis="all", addr=None):
        """Get the current axis position"""
        return int(self.query("TP?",axis=axis,addr=addr))
    @muxaddr
    @stage.muxaxis
    def set_position_reference(self, axis, position=0, addr=None):
        """Set the current axis position as a reference (the actual motor position stays the same)"""
        self.query("DH{}".format(position),axis=axis,addr=addr)
        return self.get_position(axis=axis,addr=addr)
    @muxaddr
    @stage.muxaxis
    @interface.use_parameters
    def jog(self, axis, direction, addr=0):
        """
        Jog a given axis in a given direction.
        
        `direction` can be either ``"-"`` (negative) or ``"+"`` (positive).
        The motion continues until it is explicitly stopped.
        """
        self.query("MV{}".format("+" if direction else "-"),axis=axis,addr=addr)
    @muxaddr
    @stage.muxaxis
    def is_moving(self, axis="all", addr=None):
        """Check if the axis is moving"""
        return not int(self.query("MD?",axis=axis,addr=addr))
    @muxaddr
    @stage.muxaxis
    def wait_move(self, axis="all", addr=None):
        """Wait until axis motion is done"""
        while self.is_moving(axis=axis,addr=addr):
            time.sleep(0.01)
    @stage.muxaxis
    def _stop_axis(self, axis, addr=None):
        self.query("ST",axis=axis,addr=addr)
    @muxaddr
    def stop(self, axis="all", immediate=False, addr=None):
        """
        Stop motion of a given axis.

        If ``immediate==True`` make an abrupt stop; otherwise, slow down gradually.
        Note that immediate stop has to stop all axes simultaneously, so it only takes ``axis=="all"``.
        """
        if immediate:
            if axis!="all":
                raise NewportError("immediate stop has to be called with axis=='all'")
            self.query("AB",addr=addr)
        else:
            self._stop_axis(axis=axis,addr=addr)
        self.wait_move(axis=axis,addr=addr)

    @muxaddr
    @stage.muxaxis
    def get_velocity_parameters(self, axis="all", addr=None):
        """
        Return velocity parameters ``(speed, accel)`` for the given axis and controller.
        
        ``speed`` and ``accel`` denote, correspondingly, maximal (i.e., steady regime) moving speed and acceleration in steps/s and steps/s^2.
        """
        return int(self.query("VA?",axis=axis,addr=addr)),int(self.query("AC?",axis=axis,addr=addr))
    @muxaddr
    @stage.muxaxis(mux_argnames=["speed","accel"])
    def setup_velocity(self, axis="all", speed=None, accel=None, addr=None):
        """
        Setup velocity parameters ``(speed, accel)`` for the given axis and controller.
        
        ``speed`` and ``accel`` denote, correspondingly, maximal (i.e., steady regime) moving speed and acceleration in steps/s and steps/s^2.
        ``None`` values are left unchanged.
        """
        if speed is not None:
            self.query("VA{}".format(speed),axis=axis,addr=addr)
        if accel is not None:
            self.query("AC{}".format(accel),axis=axis,addr=addr)
        return self.get_velocity_parameters(axis=axis,addr=addr)
    def _setup_all_velocity(self, params):
        if not isinstance(params,dict):
            params={None:params}
        for addr,par in params.items():
            for axis,vp in zip(self._axes,par):
                self.setup_velocity(axis,*vp,addr=addr)
