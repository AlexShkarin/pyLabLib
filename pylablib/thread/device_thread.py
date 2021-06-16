from ..core.thread import controller
from ..core.utils import rpyc_utils, module as module_utils

import importlib


class DeviceThread(controller.QTaskThread):
    """
    Expansion of :class:`.QTaskThread` equipped to deal with a single device.

    Contains methods to open/close the device, obtaining device settings and info, and dealing with remote devices (e.g., connected to other PCs).

    Args:
        name: thread name
        args: args supplied to :meth:`setup_task` method
        kwargs: keyword args supplied to :meth:`setup_task` method
        multicast_pool: :class:`.MulticastPool` for this thread (by default, use the default common pool)

    Attributes:
        device: managed device. Its opening should be specified in an overloaded :meth:`connect_device` method,
            and it is actually opened by calling :meth:`open_device` method (which also handles status updates and duplicate opening issues)
        qd: device query accessor, which routes device method call through a command
            ``ctl.qd.method(*args,**kwarg)`` is equivalent to ``ctl.device.method(args,kwargs)`` called as a synchronous command in the device thread
        qdi: device query accessor, ignores and silences any exceptions (including missing /stopped controller); similar to ``.csi`` accessor for synchronous commands
        device_reconnect_tries: number of attempts to connect to the device before when calling :meth:`open` before giving up and declaring it unavailable
        settings_variables: list of variables to list when requesting full info (e.g., using ``get_settings`` command);
            by default, read all variables, but if it takes too long, some can be omitted
        full_info_variables: list of variables to list when requesting full info (e.g., using ``get_full_info`` command);
            by default, read all variables, but if it takes too long, some can be omitted

    Methods to overload:
        - :meth:`setup_task`: executed on the thread startup (between synchronization points ``"start"`` and ``"run"``)
        - :meth:`finalize_task`: executed on thread cleanup (attempts to execute in any case, including exceptions); by default, close the device connection if it is opened
        - :meth:`connect_device`: create the device class and assign it to ``.device`` attribute; if connection failed, can leave the attribute ``None``
        - :meth:`open_device`: re-open currently closed device (by default, call ``.open`` method of the device)
        - :meth:`close_device`: close currently opened device (by default, call ``.close`` method of the device)

    Methods to use:
        - :meth:`setup_full_info_job`: setup recurring job to update full info variables; reduces the lag when getting them from other threads
        - :meth:`rpyc_devclass`: get device class on local or remote PC; can be used to transparently implement remote devices
        - :meth:`rpyc_obtain`: transfer values returned by the remote device to the local Python instance
        
    Commands:
        - ``open``: open the device, if not already opened
        - ``close``: close the device, if opened
        - ``get_settings``: get device settings
        - ``get_full_info``: get full info of the device
    """
    def __init__(self, name=None, args=None, kwargs=None, multicast_pool=None):
        super().__init__(name=name,multicast_pool=multicast_pool,args=args,kwargs=kwargs)
        self.device=None
        self.add_command("open",self.open)
        self.add_command("close",self.close)
        self.add_command("get_settings",self.get_settings)
        self.add_command("get_full_info",self.get_full_info)
        self.add_command("_device_method",self._device_method)
        self._full_info_job=False
        self.settings_variables=None
        self.full_info_variables=None
        self.device_reconnect_tries=0
        self._tried_device_connect=0
        self.rpyc_serv=None
        self.qd=self.DeviceMethodAccessor(self,ignore_errors=False)
        self.qdi=self.DeviceMethodAccessor(self,ignore_errors=True)
        
    def finalize_task(self):
        self.close()
        rpyc_serv=self.rpyc_serv
        self.device=None
        self.rpyc_serv=None
        if rpyc_serv is not None:
            try:
                rpyc_serv.getconn().close()
            except EOFError:
                pass

    def connect_device(self):
        """
        Connect the device and assign it to the ``self.device`` attribute.

        Should be overloaded in subclasses.
        In case of connection error, can leave ``self.device`` as ``None``, which symbolizes connection failure.
        """
    def open_device(self):
        """
        Open the device which has been previously closed.

        By default, call ``.open`` method of the device.
        """
        self.device.open()
    def close_device(self):
        """
        Close the device which is currently opened.

        By default, call ``.close`` method of the device.
        """
        self.device.close()

    def rpyc_devclass(self, cls, host=None, port=18812, timeout=3., attempts=2):
        """
        Get a local or remote device class on a different PC via RPyC.

        Can replace straightforward device creation for remote devices,
        i.e., instead of ``self.device=DeviceModule.DeviceClass(*args,**kwargs)``
        one would call ``self.device=self.rpyc_devclass("DeviceModule","DeviceClass",host,port)(*args,**kwargs)``.

        Args:
            cls: full device class name, including the containing module (``pylablib.devices`` can be omitted)
            host: address of the remote host (it should be running RPyC server; see :func:`.rpyc_utils.run_device_service` for details);
                if ``None`` (default), use local device class, which is exactly the same as simply creating device class without using this function
            port: port of the remote host
            timeout: remote connection timeout per attempt
            attempts: total number of connection attempts
        """
        if host is None:
            module,cls=cls.rsplit(".",maxsplit=1)
            try:
                module=importlib.import_module(module)
            except ImportError:
                module=importlib.import_module(module_utils.get_library_name()+".devices."+module)
            return getattr(module,cls)
        else:
            self.rpyc_serv=rpyc_utils.connect_device_service(host,port=port,timeout=timeout,attempts=attempts,error_on_fail=False)
            if not self.rpyc_serv:
                return None
            return self.rpyc_serv.get_device_class(cls)
    def rpyc_obtain(self, obj):
        """
        Obtain (i.e., transfer to the local PC) an object returned by the device.

        Only required for relatively complicated objects such as numpy arrays or custom classes (e.g., :class:`.Dictionary` objects).
        Most simple objects of built-in classes (numbers, strings, lists, tuples, dicts) don't need to use this method.
        If current device is local, return `obj` as is.
        """
        if self.rpyc_serv is not None:
            return rpyc_utils.obtain(obj,serv=self.rpyc_serv)
        return obj

    def open(self):
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
                self.open_device()
            if self.device.is_opened():
                self.update_status("connection","opened","Connected")
                self._tried_device_connect=0
                return True
        self._tried_device_connect+=1
        self.update_status("connection","closed","Disconnected")
        return False
    def close(self):
        """
        Close the device.

        Automatically called on the thread finalization, usually shouldn't be called explicitly.
        """
        if self.device is not None and self.device.is_opened():
            self.update_status("connection","closing","Disconnecting...")
            self.close_device()
            self.update_status("connection","closed","Disconnected")

    def get_settings(self):
        """Get device settings"""
        return self.rpyc_obtain(self.device.get_settings(include=self.settings_variables)) if self.device is not None else {}
    
    def setup_full_info_job(self, period=2.):
        """
        Setup a job which periodically obtains full information (by calling ``get_full_info`` method) from the device

        Useful if obtaining settings takes a lot of time, and they might be needed by some other thread on a short notice.

        Args:
            period: job period
        """
        if not self._full_info_job:
            self.add_job("update_full_info",self.update_full_info,period)
            self._full_info_job=True
    def update_full_info(self):
        """
        Update full info of the device.

        A function for a job which is setup in :meth:`DeviceThread.setup_full_info_job`. Normally doesn't need to be called explicitly.
        """
        self.v["full_info"]=self.rpyc_obtain(self.device.get_full_info(include=self.full_info_variables))
    def get_full_info(self):
        """
        Get full device info.
        
        If the full info job is set up using :meth:`DeviceThread.setup_full_info_job`, use the last cached version of the full info;
        otherwise, request a new version from the device.
        """
        if self.device:
            return self.v["full_info"] if self._full_info_job else self.rpyc_obtain(self.device.get_full_info(include=self.full_info_variables))
        else:
            return {}
    def _device_method(self, name, args, kwargs):
        """Call a device method"""
        if self.open_device():
            return getattr(self.device,name)(*args,**kwargs)
        return None
    class DeviceMethodAccessor:
        """
        Accessor object designed to simplify calling device commands.

        Automatically created by the thread, so doesn't need to be invoked externally.
        """
        def __init__(self, parent, ignore_errors=False):
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