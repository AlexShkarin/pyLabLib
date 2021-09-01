from ..utils.py3 import textstring, anystring, as_str
from .base import DeviceError
from . import data_format
from . import comm_backend
from ..utils import general as general_utils
from ..utils import funcargparse

import time
import contextlib
import warnings


class SCPIDevice(comm_backend.ICommBackendWrapper):
    """
    A base class for a device controlled with the usual SCPI syntax.
    
    Implements two functions:
        - deals with composing and parsing of standard SCPI commands and simplifying repetitive property access routines
        - implements automatic re-sending and reconnecting on communication failures (fail-safe mode)
    
    Args:
        conn: Connection parameters (depend on the backend). Can also be an opened :class:`.comm_backend.IDeviceCommBackend` class for a custom backend.
        term_write (str): Line terminator for writing operations.
        wait_callback (callable): A function to be called periodically (every 300ms by default) while waiting for operations to complete.
        backend (str): Connection backend (e.g., ``'serial'`` or ``'visa'``).
        backend_defaults: if not ``None``, specifies a dictionary ``{backend: params}`` with default connection parameters (depending on the backend),
            which are added to `conn`
        failsafe (bool): If ``True``, the device is working in a fail-safe mode:
            if an operation times out, attempt to repeat it several times before raising error.
            If ``None``, use the class value `_default_failsafe` (``False`` by default).
        timeout (float): Default timeout (in seconds).
    """
    # All of the following _default_* parameters can be redefined in subclasses
    # Most of these parameters are used to define object attributes, which can be altered individually for different objects (i.e., connections)
    _default_failsafe_operation_timeout=3. # timeout for an operation (read/write/ask) in the failsafe mode
    _default_backend_timeout=3. # timeout for a single backend operation attempt in the failsafe mode (one operation can be attempted several times)
    _default_retry_delay=5. # delay between retrying an operation (in seconds)
    _default_retry_times=5 # maximal number of operation attempts
    _default_operation_timeout=3. # timeout for an operator in the standard (non-failsafe) mode
    _default_wait_sync_timeout=600. # timeout for "sync" wait operation (waiting for the device operation to complete); an operation can be long (e.g., a single frequency sweep), thus the long timeout
    _default_operation_cooldown={"default":0} # operation cooldown (see description of ``setup_cooldown`` method in :class:`.comm_backend.IDeviceCommBackend`)
    _default_write_sync=False # default setting for ``wait_sync`` in ``write`` method
    _default_wait_callback_timeout=.3 # callback call period during wait operations (keeps the thread from complete halting)
    _default_failsafe=False # running in the failsafe mode by default
    _failsafe_warnings=False # whether invocation of failsafe emits a warning
    _allow_concatenate_write=False # allow automatic concatenation of several write operations (see :meth:`using_write_buffer`)
    _concatenate_write_separator=";\n" # separator to join different commands in concatenated write operation (with :meth:`using_write_buffer`)
    Error=DeviceError
    BackendError=comm_backend.DeviceBackendError
    ReraiseError=None
    def __init__(self, conn, term_write=None, term_read=None, wait_callback=None, backend="auto", backend_defaults=None, failsafe=None, timeout=None, backend_params=None):
        self._wait_sync_timeout=self._default_wait_sync_timeout
        failsafe=self._default_failsafe if failsafe is None else failsafe
        self._failsafe=failsafe
        if failsafe:
            self._operation_timeout=self._default_failsafe_operation_timeout if timeout is None else timeout
            self._backend_timeout=min(self._default_backend_timeout,self._operation_timeout) if self._operation_timeout is not None else self._default_backend_timeout
            self._retry_delay=self._default_retry_delay
            self._retry_times=self._default_retry_times
        else:
            self._operation_timeout=self._default_operation_timeout if timeout is None else timeout
            self._backend_timeout=self._operation_timeout
            self._retry_delay=0.
            self._retry_times=0
        self._wait_callback=wait_callback
        self._wait_callback_timeout=self._default_wait_callback_timeout
        instr=comm_backend.new_backend(conn,backend=backend,term_write=term_write,term_read=term_read,
                timeout=self._backend_timeout,defaults=backend_defaults,reraise_error=self.ReraiseError,**(backend_params or {}))
        self.BackendError=instr.Error
        instr.setup_cooldown(**self._default_operation_cooldown)
        comm_backend.ICommBackendWrapper.__init__(self,instr)
        self.conn=conn
        self.backend_defaults=backend_defaults
        self.backend_params=backend_params or {}
        self.backend=instr._backend
        self.term_write=term_write
        self.term_read=term_read
        self._setter_echo=True
        self._concatenate_write=0
        self._write_buffer=""
        self._scpi_parameters={}
        self._command_validity_cache={}
        if self._id_comm is not None:
            self._add_info_variable("scpi_id",self.get_id)
    
    
    def _instr_read(self, raw=False, size=None):
        if size is not None:
            data=self.instr.read(size)
        else:
            data=self.instr.readline(remove_term=not raw)
        return data
    def _instr_write(self, msg):
        return self.instr.write(msg)

    def _add_scpi_parameter(self, name, comm, kind="float", parameter=None, set_delay=0, add_variable=False):
        """
        Add a new SCPI parameter description for easier access.

        Parameter defined with this method can be accessed with :meth:`_get_scpi_parameter` and :meth:`_set_scpi_parameter`.

        Args:
            name: parameter name
            comm: SCPI access command (e.g., ``":TRIG:SOURCE"``)
            kind: parameter kind; can be  ``"string"``, ``"int"``, ``"float"``, ``"bool"``, or ``"param"`` (for parameter values)
            parameter: for ``"param"`` kind it is a device parameter class used to convert this device parameter
            set_delay: delay between setting and getting commands on parameter setting
            add_variable: if ``True``, automatically add a settings variable with the corresponding name
        """
        funcargparse.check_parameter_range(kind,"kind",["string","int","float","param","bool"])
        parameter=self._parameters.get(parameter,parameter)
        self._scpi_parameters[name]=(comm,kind,parameter,set_delay)
        if add_variable:
            self._add_device_variable(name,"settings",lambda: self._get_scpi_parameter(name),lambda v: self._set_scpi_parameter(name,v),multiarg=False)
    def _modify_scpi_parameter(self, name, comm=None, kind=None, parameter=None, set_delay=None):
        """
        Modify the properties of the existing SCPI parameter.

        Arguments are the same as :meth:`_add_scpi_parameter`. ``None`` arguments are preserved.
        """
        cpar=self._scpi_parameters[name]
        comm=cpar[0] if comm is None else comm
        if kind is not None:
            funcargparse.check_parameter_range(kind,"kind",["string","int","float","param","bool"])
        else:
            kind=cpar[1]
        parameter=cpar[2] if parameter is None else self._parameters.get(parameter,parameter)
        set_delay=cpar[3] if set_delay is None else set_delay
        self._scpi_parameters[name]=(comm,kind,parameter,set_delay)
    def _get_scpi_parameter(self, name):
        """Get SCPI parameter with a given name"""
        comm,kind,parameter,_=self._scpi_parameters[name]
        if kind in ["string","int","float","bool"]:
            return self.ask(comm+"?",kind)
        elif kind=="param":
            value=self.ask(comm+"?","string")
            return parameter.i(value)
    def _set_scpi_parameter(self, name, value, result=False):
        """Set SCPI parameter with a given name"""
        comm,kind,parameter,set_delay=self._scpi_parameters[name]
        if kind in ["string","int","float","bool"]:
            self.write(comm,value,kind)
        elif kind=="param":
            self.write(comm,parameter(value),"string")
        if set_delay>0:
            self.sleep(set_delay)
        if result:
            return self._get_scpi_parameter(name)
    
    def reconnect(self, new_instrument=True, ignore_error=True):
        """
        Remake the connection.
        
        If ``new_instrument==True``, create a new backend instance.
        If ``ignore_error==True``, ignore errors on closing.
        """
        try:
            self.close()
        except self.Error:
            if not ignore_error:
                raise
        if new_instrument:
            self.instr=comm_backend.new_backend(self.conn,backend=self.backend,term_write=self.term_write,term_read=self.term_read,
                timeout=self._backend_timeout,defaults=self.backend_defaults,reraise_error=self.ReraiseError,**self.backend_params)
        else:
            self.instr.open()
        
    def sleep(self, delay):
        """Wait for `delay` seconds"""
        if delay is not None and delay>0:
            time.sleep(delay)
    
    @contextlib.contextmanager
    def using_write_buffer(self):
        """
        Context manager for using a write buffer.
        
        While it's active, all the consecutive :meth:`write` operations are bundled together with ``;`` delimiter.
        The actual write is performed at the :meth:`read`/:meth:`ask` operation or at the end of the block.
        """
        self._concatenate_write=self._concatenate_write+1
        try:
            yield
        finally:
            self._concatenate_write=self._concatenate_write-1
            if not self._concatenate_write:
                self._write_retry(flush=True)
                
    _flush_comm=None
    def _flush_retry(self):
        for t in general_utils.RetryOnException(self._retry_times,exceptions=self.Error):
            with t:
                if self._flush_comm is not None:
                    self._instr_write(self._flush_comm)
                    self._instr_read()
                return self.instr.flush_read()
    def _try_recover(self, cnt, silent=True):
        try:
            if (cnt+1)%3==0:
                self.reconnect(ignore_error=False)
            self._flush_retry()
        except self.Error:
            if not silent:
                raise
    def _read_one_try(self, raw=False, size=None, timeout=None, wait_callback=None):
        timeout=self._operation_timeout if timeout is None else timeout
        if wait_callback is not None:
            backend_timeout=self._wait_callback_timeout
        else:
            backend_timeout=min(self._backend_timeout,timeout) if self._failsafe else timeout
        start_time=time.time()
        with self.instr.using_timeout(backend_timeout):
            for t in general_utils.RetryOnException(exceptions=self.Error):
                with t:
                    return self._instr_read(raw=raw,size=size)
                if wait_callback is not None:
                    wait_callback()
                if (time.time()>start_time+timeout) or (not self._failsafe and wait_callback is None):
                    t.reraise()
    def _read_retry(self, raw=False, size=None, timeout=None, wait_callback=None, retry=None):
        self._write_retry(flush=True)
        retry=(timeout is None) if (retry is None) else retry
        locking_timeout=self._operation_timeout if timeout is None else timeout
        for t in general_utils.RetryOnException(self._retry_times,exceptions=self.Error):
            with t:
                with self.instr.locking(timeout=locking_timeout):
                    return self._read_one_try(raw=raw,size=size,timeout=timeout,wait_callback=wait_callback)
            if not retry:
                t.reraise()
            error_msg="read raises error '{}'; waiting {} sec before trying to recover".format(t.error,self._retry_delay)
            if self._failsafe_warnings:
                warnings.warn(error_msg)
            self.sleep(self._retry_delay)
            self._try_recover(t.try_number)
    def _write_retry(self, msg="", flush=False):
        if self._allow_concatenate_write and self._concatenate_write_separator is not None and self._concatenate_write and not flush:
            self._write_buffer=(self._write_buffer+self._concatenate_write_separator+msg) if self._write_buffer else msg
            return
        if self._write_buffer:
            msg=self._write_buffer+self._concatenate_write_separator+msg if msg else self._write_buffer
            self._write_buffer=""
        if msg:
            for t in general_utils.RetryOnException(self._retry_times,exceptions=self.Error):
                with t:
                    with self.instr.locking(timeout=self._operation_timeout):
                        sent=self._instr_write(msg)
                        return sent
                error_msg="write raises error '{}'; waiting {} sec before trying to recover".format(t.error,self._retry_delay)
                if self._failsafe_warnings:
                    warnings.warn(error_msg)
                self.sleep(self._retry_delay)
                self._try_recover(t.try_number)
    def _ask_retry(self, msg, delay=0., raw=False, size=None, timeout=None, wait_callback=None, retry=None):
        self._write_retry(flush=True)
        retry=(timeout is None) if (retry is None) else retry
        locking_timeout=self._operation_timeout if timeout is None else timeout
        for t in general_utils.RetryOnException(self._retry_times,exceptions=self.Error):
            with t:
                with self.instr.locking(timeout=locking_timeout):
                    self._instr_write(msg)
                    self.sleep(delay)
                    return self._read_one_try(raw=raw,size=size,timeout=timeout,wait_callback=wait_callback)
            if not retry:
                t.reraise()
            error_msg="ask raises error '{}'; waiting {} sec before trying to recover".format(t.error,self._retry_delay)
            if self._failsafe_warnings:
                warnings.warn(error_msg)
            self.sleep(self._retry_delay)
            self._try_recover(t.try_number)
                
    
    _id_comm="*IDN?"
    def get_id(self, timeout=None):
        """Get the device IDN. (query SCPI ``'*IDN?'`` command)"""
        return self.ask(self._id_comm,timeout=timeout) if self._id_comm else None
    _reset_comm="*RST"
    def reset(self):
        """Reset the device (by default, ``"*RST"`` command)"""
        return self.write(self._reset_comm)
    _esr_comm="*ESR?"
    def get_esr(self, timeout=None):
        """Get the device status register (by default, ``"*ESR?"`` command)"""
        return self.ask(self._esr_comm,"int",timeout=timeout)
    _cls_comm="*CLS"
    _comm_valid_check_mode="esr"
    def _is_command_valid(self, comm, cached=True, clear_status=True):
        """
        Check if the command or the query is valid.

        Send the command, ignore the output, and then check the status bit 5 (command parsing error).
        If ``cached==True``, only check the validity once, and then just use this value in all further attempts.
        If ``clear_status==True``, clear status register before hand (if it's not cleared, the message queue can overflow, yielding false positives)
        """
        if (not cached) or (comm not in self._command_validity_cache):
            result=True
            if self._comm_valid_check_mode=="esr":
                if clear_status:
                    self.write(self._cls_comm)
                self.write(comm)
                self.flush()
                result=not bool(self.get_esr()&0x20)
            elif self._comm_valid_check_mode=="ret/idn":
                idn_res=self.get_id()
                self.write(comm)
                self.write(self._id_comm)
                result=False
                try:
                    while True:
                        res=self.read()
                        if res==idn_res:
                            break
                        result=True
                except self.Error:
                    pass
            if cached:
                self._command_validity_cache[comm]=result
        else:
            result=self._command_validity_cache[comm]
        return result

    
    _wait_sync_comm="*OPC?"
    def wait_sync(self, timeout=None, wait_callback=None):
        """
        Pause execution of the script until device overlapped commands (e.g., taking sweeps) are complete.
        
        `timeout` and `wait_callback` override default constructor parameters.
        """
        timeout=self._wait_sync_timeout if timeout is None else timeout
        wait_callback=wait_callback or self._wait_callback
        self._ask_retry(self._wait_sync_comm,raw=True,timeout=timeout,wait_callback=wait_callback,retry=True)
    _wait_dev_comm="*WAI"
    def wait_dev(self):
        """
        Pause execution of the device commands until device overlapped commands (e.g., taking sweeps) are complete.

        Note that the code execution is not paused.
        """
        self.write(self._wait_dev_comm)
    def wait(self, wait_type="sync", timeout=None, wait_callback=None):
        """
        Pause execution until device overlapped commands are complete.
        
        `wait_type` is either ``'sync'`` (perform :meth:`wait_sync`), ``'dev'`` (perform :meth:`wait_dev`) or ``'none'`` (do nothing).
        """
        if wait_type=="sync":
            self.wait_sync(timeout=timeout,wait_callback=wait_callback)
        elif wait_type=="dev":
            self.wait_dev()
        elif wait_type!="none":
            raise ValueError("unrecognized wait type: {0}".format(wait_type))
    
    @staticmethod
    def get_arg_type(arg):
        """Autodetect argument type"""
        if isinstance(arg,bool):
            return "bool"
        if isinstance(arg,int):
            return "int"
        if isinstance(arg,float):
            return "float"
        if isinstance(arg,textstring):
            return "string"
        if isinstance(arg,(tuple,list)):
            return [SCPIDevice.get_arg_type(v) for v in arg]
        raise ValueError("can't determine type for argument {0}".format(arg))
    _float_fmt="{:E}"
    _bool_selector=(0,1)
    def _convert_arg(self, arg, arg_type, bool_selector=None):
        if arg_type is None:
            arg_type=self.get_arg_type(arg)
        if arg_type in ["s","string","r","raw"]:
            return arg if isinstance(arg,anystring) else str(arg)
        elif arg_type in ["i","int"]:
            return "{:d}".format(int(arg))
        elif arg_type in ["f","float"]:
            return self._float_fmt.format(float(arg))
        elif arg_type in ["b","bool"]:
            bool_selector=bool_selector or self._bool_selector
            return "{}".format(bool_selector[1] if arg else bool_selector[0])
        elif isinstance(arg_type,(list,tuple)):
            return ",".join([self._convert_arg(a,t,bool_selector=bool_selector) for (a,t) in zip(arg,arg_type)])
        elif arg_type.find(":")>=0:
            if isinstance(arg,(list,tuple)):
                return arg_type.format(*arg)
            else:
                return arg_type.format(arg)
        else:
            raise ValueError("unrecognized arg_type: {0}".format(arg_type))
    def _compose_msg(self, msg, arg=None, arg_type=None, unit=None, bool_selector=None):
        if arg is not None:
            msg=msg+" "+self._convert_arg(arg,arg_type,bool_selector=bool_selector)
            if unit is not None:
                msg=msg+" "+unit
        return msg
    def write(self, msg, arg=None, arg_type=None, unit=None, bool_selector=None, wait_sync=None, read_echo=False, read_echo_delay=0.):
        """
        Send a command.
        
        Args:
            msg (str): Text message.
            arg: Optional argument to append in the end. If a list of arguments is supplied, the result is joined with ``","``.
            arg_type (str): Argument type. Can be ``'raw'`` (in which case data is sent raw), ``'string'``, ``'int'``, ``'float'``,
                ``'bool'``, a format string (such as ``'{:.3f}'``) or a list of argument types (for an iterable argument);
                if format string is used and the argument is a list or a tuple, then it is expanded as a list of arguments
                (e.g., ``arg_type='{0};{1}'`` with ``arg=[1,2]`` will produce a string ``'1;2'``);
                if a list of types is used, each element of `arg` is converted using the corresponding type, and the result is joined with ``","``.
            unit (str): If not ``None``, use it as a unit to append after the value.
            bool_selector (tuple): A tuple ``(false_value, true_value)`` of two strings to represent bool argument;
                by default, use ``._bool_selector`` attribute.
            wait_sync: if ``True``, append the sync command (specified as ``._wait_sync_comm`` attribute, ``"*OPC?"`` by default)
                after the message and pause the execution command is complete;
                useful in long set operations, where the device might ignore later inputs until the current command is complete;
                if ``None``, use the class default ``._default_write_sync`` attribute (``False`` by default).
            read_echo (bool): If ``True``, read a single line after write.
            read_echo_delay (float): The delay between write and read if ``read_echo==True``.
        """
        msg=self._compose_msg(msg,arg,arg_type,unit,bool_selector)
        if wait_sync is None:
            wait_sync=self._default_write_sync
        if wait_sync:
            msg=msg+";"+self._wait_sync_comm
        self._write_retry(msg)
        if read_echo:
            try:
                self.sleep(read_echo_delay)
                self._read_one_try()
            except self.Error:
                pass
        if wait_sync:
            sync_msg=self.read()
            if sync_msg!="1":
                raise DeviceError("unexpected reply to '{}' command: '{}'".format(self._wait_sync_comm,sync_msg))
    def _parse_msg(self, msg, data_type="string"):
        if data_type in ["r","raw"]:
            return msg
        msg=as_str(msg).strip()
        if isinstance(data_type,list):
            split_msg=[m.strip() for m in msg.split(",")]
            if len(split_msg)!=len(data_type):
                raise DeviceError("message '{}' length {} is different from the format length {}".format(msg,len(split_msg),len(data_type)))
            return [self._parse_msg(v,dt) for v,dt in zip(split_msg,data_type)]
        if data_type in ["s","string"]:
            return msg
        elif data_type in ["i","int"]:
            return int(float(msg))
        elif data_type in ["f","float"]:
            return float(msg)
        elif data_type in ["v","value"]:
            msg=msg.split()
            if len(msg)==1:
                return float(msg[0]),None
            elif len(msg)==2:
                return float(msg[0]),msg[1]
            else:
                raise DeviceError("empty response")
        elif data_type in ["b","bool"]:
            msg=msg.lower()
            msg=msg.split()[-1]
            try:
                return bool(int(msg))
            except ValueError:
                return msg!="off"
        elif isinstance(data_type,dict):
            if msg in data_type:
                return data_type(msg)
            else:
                return data_type[int(float(msg))]
        elif hasattr(data_type,"__call__"):
            return data_type(msg)
        else:
            raise ValueError("unrecognized data_type: {0}".format(data_type))
    def _check_reply(self, reply, msg=None):  # pylint: disable=unused-argument
        """
        Check the raw reply returned by the device.

        Called automatically in ``read`` and ``ask`` methods.
        If specified, `msg` is the message sent to the device
        Return ``True`` if the reply is valid and ``False`` otherwise (can also raise an exception from here).
        """
        return True
    def read(self, data_type="string", timeout=None):
        """
        Read data from the device.
        
        `data_type` determines the type of the data. Can be ``'raw'`` (just raw data), ``'string'`` (with trailing and leading spaces stripped),
        ``'int'``, ``'float'``, ``'bool'`` (interprets ``0`` or ``'off'`` as ``False``, anything else as ``True``),
        ``'value'`` (returns tuple ``(value, unit)``, where `value` is float),
        a callable (return the result of this callable applied to the string value),
        a dictionary (return the stored value corresponding to the string value, or to the value converted into integer if the string value is not present),
        or a list of data types (the result is treated as a list of values with the given types separated by commas).
        `timeout` overrides the default value.
        """
        msg=self._read_retry(raw=(data_type=="raw"),timeout=timeout)
        if not self._check_reply(msg):
            raise self.Error("device sent unexpected reply: {}".format(msg))
        return self._parse_msg(msg,data_type)
    def ask(self, msg, data_type="string", delay=0., timeout=None, read_echo=False):
        """
        Write a message and read a reply.
        
        `msg` is the query message, `delay` is the delay between write and read. Other parameters are the same as in :meth:`read`.
        If ``read_echo==True``, assume that the device first echoes the input and skip it.
        """
        for t in general_utils.RetryOnException(self._retry_times,exceptions=ValueError):
            with t:
                if read_echo:
                    self._ask_retry(msg,delay,raw=True,timeout=timeout)
                    reply=self._read_retry(raw=(data_type=="raw"),timeout=timeout)
                else:
                    reply=self._ask_retry(msg,delay,raw=(data_type=="raw"),timeout=timeout)
                if not self._check_reply(reply,msg):
                    raise self.Error("query {} returned unexpected reply: {}".format(msg,reply))
                return self._parse_msg(reply,data_type=data_type)
            if not self._failsafe:
                t.reraise()
            error_msg="ask error in instrument {} returned {}".format(self.instr,reply)
            if self._failsafe_warnings:
                warnings.warn(error_msg)
            self.sleep(0.5)
            self.flush()
            self._try_recover(t.try_number)
    def flush(self, one_line=False):
        """
        Flush the read buffer (read all the available data and return the number of bytes read).
        
        If ``one_line==True``, read only a single line.
        """
        l=0
        try:
            while True:
                l=l+len(self._read_one_try(raw=True,timeout=1E-3))
                if one_line:
                    return l
        except self.Error:
            return l

    def read_binary_array_data(self, include_header=False, timeout=None, flush_term=True):
        """
        Read a binary data in the from the device.

        The data assumes the standard binary transfer header consisting of
        ``"#"`` symbol, then a single digit with the size of the length string, then the length string containing the length of the binary data (in bytes).
        If ``include_header==True``, return the data with the header; otherwise, return only the content.
        If ``flush_term==True``, flush the following line to skip terminator characters after the binary data, which are added by some devices.
        `timeout` overrides the default value.
        """
        data=b""
        header=b""
        header+=self._read_retry(raw=True,size=2,timeout=timeout)
        if header[:1]!=b"#":
            raise DeviceError("malformatted data")
        len_size=int(header[1:2])
        header+=self._read_retry(raw=True,size=len_size,timeout=timeout)
        length=int(header[2:])
        data=self._read_retry(raw=True,size=length,timeout=timeout)
        if flush_term:
            self.flush(one_line=True)
        return (header+data) if include_header else data
    @staticmethod
    def parse_array_data(data, fmt, include_header=False):
        """
        Parse the data returned by the device. `fmt` is :class:`.DataFormat` description in numpy format (e.g., ``"<u2"``).
        
        If ``include_header==True``, the data is assumed to be in a (somewhat) standard SCPI format:
        ``b'#'``, then a single digit ``s`` denoting length of the size block,
        then ``s`` digits denoting length of the data (in bytes) followed by the actual data.
        Otherwise (``include_header==False``), assume that the header is already removed.
        """
        fmt=data_format.DataFormat.from_desc(fmt)
        if include_header:
            if data[:1]!=b"#": # range access to accommodate for bytes type in Py3
                if not fmt.is_ascii():
                    raise ValueError("malformatted data")
                length=None
            else:
                len_size=int(data[1:2]) # range access to accommodate for bytes type in Py3
                length=int(data[2:2+len_size])
                data=data[2+len_size:]
        else:
            length=len(data)
        if length is not None and len(data)!=length:
            if len(data)>length and data[length:]==b"\n"*(len(data)-length):
                data=data[:length]
            else:
                if len(data)>length+20:
                    trailing_bytes="; first 20 trailing bytes are {}".format(data[length:length+20])
                elif len(data)>length:
                    trailing_bytes="; trailing bytes are {}".format(data[length:])
                else:
                    trailing_bytes=""
                raise ValueError("data length {0} doesn't agree with the declared length {1}".format(len(data),length)+trailing_bytes)
        return fmt.convert_from_str(data)
    
    def apply_settings(self, settings):
        """
        Apply the settings.
        
        `settings` is a dict ``{name: value}`` of the available device settings.
        Non-applicable settings are ignored.
        """
        try:
            self._setter_echo=False
            with self.using_write_buffer():
                return comm_backend.ICommBackendWrapper.apply_settings(self,settings)
        finally:
            self._setter_echo=True