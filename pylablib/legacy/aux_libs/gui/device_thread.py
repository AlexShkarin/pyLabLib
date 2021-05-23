from ...core.gui.qt.thread import controller
from ...core.utils import rpyc as rpyc_utils

class DeviceThread(controller.QTaskThread):
    """
    Expansion of :class:`.QTaskThread` equipped to deal with a single device.

    Args:
        name: thread name
        devargs: args supplied to :math:`setup_task` method
        devkwargs: keyword args supplied to :math:`setup_task` method
        signal_pool: :class:`.SignalPool` for this thread (by default, use the default common pool)

    Attributes:
        device: managed device. Its opening should be specified in an overloaded :meth:`connect_device` method,
            and it is actually opened by calling :meth:`open_device` method (which also handles status updates and duplicate opening issues)
        qd: device query accessor, which routes device method call through a command
            ``ctl.qd.method(*args,**kwarg)`` is equivalent to ``ctl.device.method(args,kwargs)`` called as a query in the device thread
        qdi: device query accessor, ignores and silences any exceptions (including missing /stopped controller); similar to ``.qi`` accessor for queries

    Methods to overload:
        setup_task: executed on the thread startup (between synchronization points ``"start"`` and ``"run"``)
        finalize_task: executed on thread cleanup (attempts to execute in any case, including exceptions); by default, close the device connection if it is opened
        connect_device: create the device class and assign it to ``.device`` attribute; if connection failed, can leave the attribute ``None``
        device_open: re-open currently closed device (by default, call ``.open`` method of the device)
        device_close: close currently opened device (by default, call ``.close`` method of the device)
        
    Commands:
        open_device: open the device, if not already opened
        close_device: close the device, if opened
        get_settings: get device settings
        get_full_info: get full info of the device
    """
    def __init__(self, name=None, devargs=None, devkwargs=None, signal_pool=None):
        controller.QTaskThread.__init__(self,name=name,signal_pool=signal_pool,setupargs=devargs,setupkwargs=devkwargs)
        self.device=None
        self.add_command("open_device",self.open_device)
        self.add_command("close_device",self.close_device)
        self.add_command("get_settings",self.get_settings)
        self.add_command("get_full_info",self.get_full_info)
        self.add_command("_device_method",self._device_method)
        self._full_info_job=False
        self._full_info_nodes=None
        self.device_reconnect_tries=0
        self._tried_device_connect=0
        self.qd=self.DeviceMethodAccessor(self,ignore_errors=False)
        self.qdi=self.DeviceMethodAccessor(self,ignore_errors=True)
        
    def finalize_task(self):
        self.close_device()

    def connect_device(self):
        """
        Connect the device and assign it to the ``self.device`` attribute.

        Should be overloaded in subclasses.
        In case of connection error, can leave ``self.device`` as ``None``, which symbolizes connection failure.
        """
        pass
    def device_open(self):
        """
        Open the device which has been previously closed.

        By default, call ``.open`` method of the device.
        """
        self.device.open()
    def device_close(self):
        """
        Close the device which is currently opened.

        By default, call ``.close`` method of the device.
        """
        self.device.close()
    def open_device(self):
        """
        Open the device by calling :meth:`connect_device`.

        Return ``True`` if connection was a success (or the device is already connected) and ``False`` otherwise.
        """
        if self.device is not None and self.device.is_opened():
            return True
        if self.device is None and (self.device_reconnect_tries>=0 and self._tried_device_connect>self.device_reconnect_tries):
            return False
        self.update_status("connection","opening","Connecting...")
        if self.device is None:
            self.connect_device()
        if self.device is not None:
            if not self.device.is_opened():
                self.device_open()
            if self.device.is_opened():
                self.update_status("connection","opened","Connected")
                self._tried_device_connect=0
                return True
        self._tried_device_connect+=1
        self.update_status("connection","closed","Disconnected")
        return False
    def close_device(self):
        """
        Close the device.

        Automatically called on the thread finalization, ususally shouldn't be called explicitly.
        """
        if self.device is not None and self.device.is_opened():
            self.update_status("connection","closing","Disconnecting...")
            self.device_close()
            self.update_status("connection","closed","Disconnected")

    def get_settings(self):
        """Get device settings"""
        return self.device.get_settings() if self.device is not None else {}
    
    def setup_full_info_job(self, period=2., nodes=None):
        """
        Setup a job which periodically obtains full information (by calling ``get_full_info`` method) from the device

        Useful if obtaining settings takes a lot of time, and they might be needed by some other thread on a short notice.

        Args:
            period: job period
            node: specifies info nodes to be requested (by default, all available nodes)
        """
        if not self._full_info_job:
            self._full_info_nodes=nodes
            self.add_job("update_full_info",self.update_full_info,period)
            self._full_info_job=True
    def update_full_info(self):
        """
        Update full info of the device.

        A function for a job which is setup in :meth:`DeviceThread.setup_full_info_job`. Normally doesn't need to be called explicitly.
        """
        self["full_info"]=self.device.get_full_info(nodes=self._full_info_nodes)
    def get_full_info(self):
        """
        Get full device info
        
        If the full info job is set up using :meth:`DeviceThread.setup_full_info_job`, use the last cached version of the full info;
        otherwise, request a new version from the device.
        """
        if self.device:
            return self["full_info"] if self._full_info_job else self.device.get_full_info(nodes=self._full_info_nodes)
        else:
            return {}
    def _device_method(self, name, args, kwargs):
        """Call a device method"""
        if self.open_device():
            return getattr(self.device,name)(*args,**kwargs)
        return None
    class DeviceMethodAccessor(object):
        """
        Accessor object designed to simplify calling device commands.

        Automatically created by the thread, so doesn't need to be invoked externally.
        """
        def __init__(self, parent, ignore_errors=False):
            object.__init__(self)
            self.parent=parent
            self.ignore_errors=ignore_errors
            self._calls={}
        def __getattr__(self, name):
            if name not in self._calls:
                parent=self.parent
                def remcall(*args, **kwargs):
                    return parent.call_query("_device_method",[name,args,kwargs],ignore_errors=self.ignore_errors)
                self._calls[name]=remcall
            return self._calls[name]





class RemoteDeviceThread(DeviceThread):
    """
    Expansion of :class:`DeviceThread` equipped to deal with a remote device (via RPyC library).

    All arguments, attributes and commands are the same as in :class:`DeviceThread`.
    """
    def __init__(self, name=None, devargs=None, devkwargs=None, signal_pool=None):
        DeviceThread.__init__(self,name=name,signal_pool=signal_pool,devargs=devargs,devkwargs=devkwargs)
        self.rpyc=False
        self.rpyc_serv=None

    def rpyc_device(self, remote, module, device, *args, **kwargs):
        """
        Create a remote device on a different PC via RPyC.

        Can replace straightforward device creation for remote devices,
        i.e., instead of ``self.device = DeviceModule.DeviceClass(*args,**kwargs)``
        one would call ``self.device = self.rpyc_device(host,"DeviceModule","DeviceClass",*args,**kwargs)``.

        Args:
            remote: address of the remote host (it should be running RPyC server; see :func:`.rpyc.run_device_service` for details)
            module: device class module name
            device: device class name
            args: arguments supplied to the device constructor.
            kwargs: keyword arguments supplied to the device constructor.
        """
        self.rpyc=True
        self.rpyc_serv=rpyc_utils.connect_device_service(remote)
        if not self.rpyc_serv:
            return None
        return self.rpyc_serv.get_device(module,device,*args,**kwargs)
    def rpyc_obtain(self, obj):
        """
        Obtain (i.e., transfer to the local PC) an object returned by the device.

        If current device is local, return `obj` as is.
        """
        if self.rpyc:
            return rpyc_utils.obtain(obj,serv=self.rpyc_serv)
        return obj

    def finalize_task(self):
        DeviceThread.finalize_task(self)
        rpyc_serv=self.rpyc_serv
        self.device=None
        self.rpyc_serv=None
        if rpyc_serv is not None:
            try:
                rpyc_serv.getconn().close()
            except EOFError:
                pass
        
    def get_settings(self):
        return self.rpyc_obtain(self.device.get_settings()) if self.device is not None else {}
    def update_full_info(self):
        self["full_info"]=self.rpyc_obtain(self.device.get_full_info(nodes=self._full_info_nodes))
    def get_full_info(self):
        if self.device:
            return self["full_info"] if self._full_info_job else self.rpyc_obtain(self.device.get_full_info(nodes=self._full_info_nodes))
        else:
            return {}