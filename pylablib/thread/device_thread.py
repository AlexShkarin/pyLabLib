from ..core.thread import controller
from ..core.utils import rpyc_utils, module as module_utils, dictionary
from ..core.devio.base import DeviceError

import importlib
import contextlib
import gc


class DeviceThread(controller.QTaskThread):
    """
    Expansion of :class:`.QTaskThread` equipped to deal with a single device.

    Contains methods to open/close the device, obtaining device settings and info, and dealing with remote devices (e.g., connected to other PCs).

    Attributes:
        device: managed device. Its opening should be specified in an overloaded :meth:`connect_device` method,
            and it is actually opened by calling :meth:`open_device` method (which also handles status updates and duplicate opening issues)
        dca: device query accessor, which routes device method call through an asynchronous command
            ``ctl.dca.method(*args,**kwarg)`` is equivalent to ``ctl.device.method(args,kwargs)`` called as an asynchronous command in the device thread
        dcs: device query accessor, which routes device method call through a synchronous command
            ``ctl.dcs.method(*args,**kwarg)`` is equivalent to ``ctl.device.method(args,kwargs)`` called as a synchronous command in the device thread
        dcsi: device query accessor, ignores and silences any exceptions (including missing /stopped controller); similar to ``.csi`` accessor for synchronous commands
        device_reconnect_tries: number of attempts to connect to the device before when calling :meth:`open` before giving up and declaring it unavailable
        parameter_variables: list of variables to list when requesting full info (e.g., using ``update_parameters`` command);
            by default, read all variables, but if it takes too long, some can be omitted
        full_info_variables: list of variables to list when requesting full info (e.g., using ``get_full_info`` command);
            by default, read all variables, but if it takes too long, some can be omitted

    Methods to overload:
        - :meth:`setup_task`: executed on the thread startup (between synchronization points ``"start"`` and ``"run"``)
        - :meth:`finalize_task`: executed on thread cleanup (attempts to execute in any case, including exceptions); by default, close the device connection if it is opened
        - :meth:`connect_device`: create the device class and assign it to ``.device`` attribute; if connection failed, can leave the attribute ``None``
        - :meth:`open_device`: re-open currently closed device (by default, call ``.open`` method of the device)
        - :meth:`close_device`: close currently opened device (by default, call ``.close`` method of the device)
        - :meth:`setup_open_device`: setup the device after opening (either initial connection, or re-opening)
        - :meth:`_get_parameter`: return the current device parameters which need to be shown to other threads;
            by default, get all device variables specified by ``parameter_variables`` class attribute (all settings by default)
        - :meth:`_get_disconnected_parameters`: return the parameters substitute when the device is disconnected (i.e., the thread is in the dummy mode);
            by default, return ``default_parameter_values`` class attribute (``None`` by default)

    Methods to use:
        - :meth:`setup_full_info_job`: setup recurring job to update full info variables; reduces the lag when getting them from other threads
        - :meth:`add_device_command`: add a command which simply calls a device method and optionally updates the parameters afterwards
        - :meth:`rpyc_devclass`: get device class on local or remote PC; can be used to transparently implement remote devices
        - :meth:`using_devclass`: context manager simplifying usage of :meth:`rpyc_devclass`
        - :meth:`rpyc_obtain`: transfer values returned by the remote device to the local Python instance
        
    Commands:
        - ``open``: open the device, if not already opened
        - ``close``: close the device, if opened
        - ``update_parameters``: update the stored parameter and return the current value;
            intended to fit between :meth:`get_full_info`, which returns the full information only upon request,
            and :meth:`update_measurements`, which frequently updates the most relevant parameters.
        - ``apply_parameters``: apply the parameters supplied as a dictionary
        - ``get_full_info``: get full info of the device
    """
    parameter_variables="settings"
    default_parameter_values={}
    full_info_variables=None
    def __init__(self, name=None, args=None, kwargs=None, multicast_pool=None):
        super().__init__(name=name,multicast_pool=multicast_pool,args=args,kwargs=kwargs)
        self.device=None
        self.add_command("open")
        self.add_command("close")
        self.add_command("update_parameters")
        self.add_command("apply_parameters")
        self.add_command("get_full_info")
        self.add_command("_device_method")
        self._full_info_job=False
        self.device_reconnect_tries=2
        self._tried_device_connect=0
        self._keep_closed=False
        self.rpyc_serv=None
        self.remote=None
        self.DeviceError=DeviceError
        self.dca=self.DeviceMethodAccessor(self,sync=False,ignore_errors=True)
        self.dcs=self.DeviceMethodAccessor(self,sync=True,ignore_errors=False)
        self.dcsi=self.DeviceMethodAccessor(self,sync=True,ignore_errors=True)
        
    def finalize_task(self):
        self.close()
        self.device=None
        self.rpyc_serv=None
        gc.collect()

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
        try:
            self.device.open()
        except (OSError, self.DeviceError):  # type: ignore
            raise self.ConnectionFailError
    def setup_open_device(self):
        """
        Set up the device after opening.

        Called both after initial connection and after reopening.
        By default, do nothing.
        """
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
            cls=getattr(module,cls)
        else:
            self.rpyc_serv=rpyc_utils.connect_device_service(host,port=port,timeout=timeout,attempts=attempts,error_on_fail=False)
            if not self.rpyc_serv:
                return None
            cls=self.rpyc_serv.get_device_class(cls)
        self.DeviceError=self.rpyc_obtain(cls.Error)
        return cls
    def rpyc_obtain(self, obj, deep=False, direct=False):
        """
        Obtain (i.e., transfer to the local PC) an object returned by the device.

        If ``deep==True`` and ``obj`` is a container (tuple, list, or dict), run the function recursively for all its sub-elements;
        otherwise, convert it all at once.
        If ``direct==True``, directly use RPyC ``obtain`` method; otherwise use the custom method, which works better with large numpy arrays,
        but worse with composite types (e.g., lists).
        Only required for relatively complicated objects such as numpy arrays or custom classes (e.g., :class:`.Dictionary` objects).
        Most simple objects of built-in classes (numbers, strings, lists, tuples, dicts) don't need to use this method.
        If current device is local, return `obj` as is.
        """
        if self.rpyc_serv is not None:
            return rpyc_utils.obtain(obj,serv=self.rpyc_serv,deep=deep,direct=direct)
        return obj

    class ConnectionFailError(Exception):
        """Error which can be raised on opening failure"""

    @contextlib.contextmanager
    def using_devclass(self, cls, host, timeout=3., attempts=2):
        """
        Context manager for simplifying device opening.

        Creates a class based on `cls` and `host` parameters, catches device opening errors,
        and automatically closes device and sets it to ``None`` if that happens.
        If `host` is ``"disconnect"``, skip device connection (can be used for e.g., temporarily unavailable or buggy device).
        """
        if host=="disconnect":
            raise self.ConnectionFailError
        try:
            cls=self.rpyc_devclass(cls,host=host,timeout=timeout,attempts=attempts)
        except IOError:
            raise self.ConnectionFailError
        if cls is None:
            raise self.ConnectionFailError
        try:
            yield cls
        except (OSError, self.DeviceError):  # type: ignore
            if self.device is not None:
                self.device.close()
                self.device=None
    def open(self, reopen=False):
        """
        Open the device by calling :meth:`connect_device`.

        If ``reopen==False`` and the device was explicitly closed using :meth:`close` with ``keep_closed=True``, skip reopening it;
        in effect, this method then becomes a "soft" opening, which tries to open initially closed or previously failed device, but not an explicitly closed one.
        Return ``True`` if connection was a success (or the device is already connected) and ``False`` otherwise.
        """
        if self.device is not None and self.device.is_opened():
            return True
        if self._keep_closed:
            if reopen:
                self._keep_closed=False
            else:
                return False
        if self.device is None and (self.device_reconnect_tries>=0 and self._tried_device_connect>self.device_reconnect_tries):
            return False
        self.update_status("connection","opening","Connecting...")
        if self.device is None:
            try:
                self.connect_device()
                if self.device is not None:
                    self.setup_open_device()
            except self.ConnectionFailError:
                pass
        if self.device is not None:
            if not self.device.is_opened():
                try:
                    self.open_device()
                except self.ConnectionFailError:
                    pass
                if self.device.is_opened():
                    self.setup_open_device()
            if self.device.is_opened():
                self.update_status("connection","opened","Connected")
                self._tried_device_connect=0
                return True
        self._tried_device_connect+=1
        self.update_status("connection","closed","Disconnected")
        return False
    def is_opened(self):
        """Check if the device is connected and opened"""
        return self.device is not None and self.device.is_opened()
    def close(self, keep_closed=False):
        """
        Close the device.

        If ``keep_closed==True``, then a latter call to :meth:`open` will not reopen the device unless ``reopen=True`` is supplied explicitly.
        Automatically called on the thread finalization, usually shouldn't be called explicitly.
        """
        if self.device is not None and self.device.is_opened():
            self.update_status("connection","closing","Disconnecting...")
            self.close_device()
            self.update_status("connection","closed","Disconnected")
        self._keep_closed=self._keep_closed or keep_closed

    def _get_device_parameters_dictionary(self, include=None):
        if not self.device:
            return dictionary.Dictionary()
        if include=="settings":
            par=self.device.get_settings()
        else:
            par=self.device.get_full_info(include=include)
        return dictionary.Dictionary(self.rpyc_obtain(par))
    def _get_parameters(self):
        """Get device parameters (can be overloaded in subclasses)"""
        return self._get_device_parameters_dictionary(include=self.parameter_variables)
    def _get_disconnected_parameters(self):
        """Get default device parameters if it is disconnected (can be overloaded in subclasses)"""
        return self.default_parameter_values
    def update_parameters(self):
        """Get device parameters and update their value in the thread variables"""
        if self.open():
            parameters=self._get_parameters()
        else:
            parameters=self._get_disconnected_parameters()
        self.set_variable("parameters",parameters,update=True,notify=True)
        return parameters
    def apply_parameters(self, parameters, update=True):
        """Apply device parameters"""
        if self.open():
            self.device.apply_settings(parameters)
            if update:
                self.update_parameters()
    
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
        self.v["full_info"]=self._get_device_parameters_dictionary(self.full_info_variables)
    def _get_aux_full_info(self):
        """
        Get additional full info parts which are not returned by the class by default.

        Usually involves classes with complicated behavior which can not be saved in a files, e.g., camera attributes or parameter classes.
        """
        aux_info={}
        if self.device and hasattr(self.device,"_parameters"):
            aux_info.update({"device_parameters":self.device._parameters})
        return aux_info
    def get_full_info(self, add_aux=False):
        """
        Get full device info.
        
        If the full info job is set up using :meth:`DeviceThread.setup_full_info_job`, use the last cached version of the full info;
        otherwise, request a new version from the device.
        If ``add_aux==True``, include possible custom info which involves non-savable classes, e.g., camera attribute classes.
        """
        if self.device:
            info=self.v["full_info"] if self._full_info_job else self._get_device_parameters_dictionary(include=self.full_info_variables)
            if add_aux:
                info.update(self._get_aux_full_info() or {})
            return info
        else:
            return dictionary.Dictionary()

    def add_device_command(self, name, command_name=None, post_update="update_parameters", limit_queue=None, on_full_queue="skip_current", priority=0):
        """
        Add command which calls a specified device method.
        
        `command_name` specifies the device method to call; by default, same as `name`.
        `post_update` is a string or a list of strings which specifies which update methods to call after the command.
        Check if the devices is opened, do nothing if it is not.
        """
        if not isinstance(post_update,(list,tuple)):
            post_update=[] if post_update is None else [post_update]
        command_name=command_name or name
        def command(*args, **kwargs):
            if self.open():
                meth=getattr(self.device,command_name)
                meth(*args,**kwargs)
                for pm in post_update:
                    getattr(self,pm)()
        self.add_command(name,command,limit_queue=limit_queue,on_full_queue=on_full_queue,priority=priority)
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
        def __init__(self, parent, sync=True, ignore_errors=False):
            self.parent=parent
            self.sync=sync
            self.ignore_errors=ignore_errors
            self._calls={}
        def __getattr__(self, name):
            if name not in self._calls:
                parent=self.parent
                def remcall(*args, **kwargs):
                    return parent.call_command("_device_method",[name,args,kwargs],sync=self.sync,ignore_errors=self.ignore_errors)
                self._calls[name]=remcall
            return self._calls[name]