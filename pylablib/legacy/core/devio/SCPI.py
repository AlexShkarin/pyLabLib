import time
import contextlib

from ..utils.py3 import textstring, as_str
from . import data_format
from . import backend as backend_module  #@UnresolvedImport
from ..utils import general as general_utils  #@UnresolvedImport
from ..utils import log #@UnresolvedImport
from ..utils import general #@UnresolvedImport
from ..utils import funcargparse #@UnresolvedImport

_depends_local=[".backend"]


class SCPIDevice(backend_module.IBackendWrapper):
    """
    A base class for a device controlled with the usual SCPI syntax.
    
    Implements two functions:
        - deals with composing and parsing of standard SCPI commands.
        - implements automatic re-sending and reconnecting on communication failures (fail-safe mode)
    
    Args:
        conn: Connection parameters (depend on the backend). Can also be an opened :class:`.backend.IDeviceBackend` class for a custom backend.
        term_write (str): Line terminator for writing operations.
        wait_callback (callable): A function to be called periodically (every 300ms by default) while waiting for operations to complete.
        backend (str): Connection backend (``'serial'`` or ``'visa'``).
        failsafe (bool): If ``True``, the device is working in a fail-safe mode:
            if an operation times out, attempt to repeat it several times before raising error.
            If ``None``, use the class value `_default_failsafe` (``False`` by default).
        timeout (float): Default timeout (in seconds).
    """
    # All of the following _default_* parameters can be redefined in subclasses
    # Most of these parameters are used to define object attributes, which can be altered individually for different objects (i.e., connections)
    _default_failsafe_operation_timeout=5. # timeout for an operaton (read/write/ask) in the failsafe mode
    _default_backend_timeout=3. # timeout for a single backend operation attempt in the failsafe mode (one operation can be attempted several times)
    _default_retry_delay=5. # delay between retrying an operation (in seconds)
    _default_retry_times=5 # maximal number of operation attempts
    _default_operation_timeout=3. # timeout for an operator in the standard (non-failsafe) mode
    _default_wait_sync_timeout=600. # timeout for "sync" wait operation (waiting for the device operation to complete); an operation can be long (e.g., a single frequency sweep), thus the long timeout
    _default_operation_cooldown=0.02 # operation cooldown (see backend description)
    _default_wait_callback_timeout=.3 # callback call period during wait operations (keeps the thread from complete halting)
    _default_failsafe=False # running in the failsafe mode by default
    _allow_concatenate_write=False # allow automatic concatenation of several write operations (see :meth:`using_write_buffer`)
    _concatenate_write_separator=";\n" # separator to join different commands in concatenated write operation (with :meth:`using_write_buffer`)
    def __init__(self, conn, term_write=None, term_read=None, wait_callback=None, backend="visa", failsafe=None, timeout=None, backend_params=None):
        self._wait_sync_timeout=self._default_wait_sync_timeout
        failsafe=self._default_failsafe if failsafe is None else failsafe
        self._failsafe=failsafe
        if failsafe:
            self._operation_timeout=self._default_failsafe_operation_timeout if timeout is None else timeout
            self._backend_timeout=self._default_backend_timeout
            self._retry_delay=self._default_retry_delay
            self._retry_times=self._default_retry_times
        else:
            self._operation_timeout=self._default_operation_timeout if timeout is None else timeout
            self._backend_timeout=self._operation_timeout
            self._retry_delay=0.
            self._retry_times=0
        self._wait_callback=wait_callback
        self._wait_callback_timeout=self._default_wait_callback_timeout
        instr=backend_module.new_backend(conn,backend=backend,term_write=term_write,term_read=term_read,timeout=self._backend_timeout,**(backend_params or {}))
        instr._operation_cooldown=self._default_operation_cooldown
        backend_module.IBackendWrapper.__init__(self,instr)
        self.conn=conn
        self.backend_params=backend_params or {}
        self.backend=instr._backend
        self.term_write=term_write
        self.term_read=term_read
        self._setter_echo=True
        self._concatenate_write=0
        self._write_buffer=""
        self._debug_conn=False
        self._scpi_parameters={}
        self._command_validity_cache={}
    
    
    def _instr_read(self, raw=False):
        data=self.instr.readline(remove_term=not raw)
        if self._debug_conn:
            debug_msg="Reading from instr: {}".format(data)
            log.default_log.debug(debug_msg,origin="devices/SCPI",level="misc")
        return data
    def _instr_write(self, msg):
        if self._debug_conn:
            debug_msg="Writing to instr: {}".format(msg)
            log.default_log.debug(debug_msg,origin="devices/SCPI",level="misc")
        return self.instr.write(msg)

    def _add_scpi_parameter(self, name, comm, kind="float", options=None, add_node=False):
        """
        Add a new SCPI parameter description for easier access.

        Parameter defined with this method can be accessed with :meth:`_get_scpi_parameter` and :meth:`_set_scpi_parameter`.

        Args:
            name: parameter name
            comm: SCPI access command (e.g., ``":TRIG:SOURCE"``)
            kind: parameter kind; can be  ``"int"``, ``"float"``, ``"bool"``, or ``"enum"`` (for text/enum values)
            options: for ``"enum"`` kind it is a dictionary ``{scpi_value: return_value}``,
                where ``scpi_value`` is a return SCPI value text (upper case) and ``return_value`` is the value accepted/returned by the set/get method.
            add_node: if ``True``, automatically add a settings node with the corresponding name
        """
        funcargparse.check_parameter_range(kind,"kind",["int","float","enum","bool"])
        ioptions=general.invert_dict(options) if options else {}
        self._scpi_parameters[name]=(comm,kind,options or {},ioptions)
        if add_node:
            self._add_settings_node(name,lambda: self._get_scpi_parameter(name),lambda v: self._set_scpi_parameter(name,v),multiarg=False)
    def _get_scpi_parameter(self, name):
        """Get SCPI parameter with a given name"""
        comm,kind,options,_=self._scpi_parameters[name]
        if kind in ["int","float","bool"]:
            return self.ask(comm+"?",kind)
        elif kind=="enum":
            value=self.ask(comm+"?","string")
            return options[value.upper()]
    def _set_scpi_parameter(self, name, value):
        """Set SCPI parameter with a given name"""
        comm,kind,_,ioptions=self._scpi_parameters[name]
        if kind in ["int","float","bool"]:
            self.write(comm,value,kind)
        elif kind=="enum":
            funcargparse.check_parameter_range(value,"value",ioptions)
            self.write("{} {}".format(comm,ioptions[value]))
        return self._get_scpi_parameter(name)
    
    def reconnect(self, new_instrument=True):
        """
        Remake the connection.
        
        If ``new_instrument==True``, create a new backend instance.
        """
        try:
            self.close()
        except self.instr.Error:
            pass
        if new_instrument:
            self.instr=backend_module.new_backend(self.conn,backend=self.backend,term_write=self.term_write,term_read=self.term_read,timeout=self._backend_timeout,**self.backend_params)
        else:
            self.instr.open()
        
    def sleep(self, delay):
        """Wait for `delay` seconds."""
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
        for t in general_utils.RetryOnException(self._retry_times,exceptions=self.instr.Error):
            with t:
                response=self.instr.ask(self._flush_comm or self._id_comm)
                self.flush()
                return response
    def _try_recover(self, cnt, silent=True):
        try:
            if cnt%2==0:
                self.reconnect()
            self._flush_retry()
        except self.instr.Error:
            if not silent:
                raise
    def _read_one_try(self, raw=False, timeout=None, wait_callback=None):
        timeout=self._operation_timeout if timeout is None else timeout
        if wait_callback is not None:
            backend_timeout=self._wait_callback_timeout
        else:
            backend_timeout=min(self._backend_timeout,timeout) if self._failsafe else timeout
        start_time=time.time()
        with self.instr.using_timeout(backend_timeout):
            for t in general_utils.RetryOnException(exceptions=self.instr.Error):
                with t:
                    return self._instr_read(raw=raw)
                if wait_callback is not None:
                    wait_callback()
                if (time.time()>start_time+timeout) or (not self._failsafe and wait_callback is None):
                    t.reraise()
    def _read_retry(self, raw=False, timeout=None, wait_callback=None, retry=None):
        self._write_retry(flush=True)
        retry=(timeout is None) if (retry is None) else retry
        locking_timeout=self._operation_timeout if timeout is None else timeout
        for t in general_utils.RetryOnException(self._retry_times,exceptions=self.instr.Error):
            with t:
                with self.instr.locking(timeout=locking_timeout):
                    return self._read_one_try(raw,timeout=timeout,wait_callback=wait_callback)
            if not retry:
                t.reraise()
            error_msg="read raises IOError; waiting {0} sec before trying to recover".format(self._retry_delay)
            log.default_log.info(error_msg,origin="devices/SCPI",level="warning")
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
            for t in general_utils.RetryOnException(self._retry_times,exceptions=self.instr.Error):
                with t:
                    with self.instr.locking(timeout=self._operation_timeout):
                        sent=self._instr_write(msg)
                        return sent
                error_msg="write raises IOError; waiting {0} sec before trying to recover".format(self._retry_delay)
                log.default_log.info(error_msg,origin="devices/SCPI",level="warning")
                self.sleep(self._retry_delay)
                self._try_recover(t.try_number)
    def _ask_retry(self, msg, delay=0., raw=False, timeout=None, wait_callback=None, retry=None):
        self._write_retry(flush=True)
        retry=(timeout is None) if (retry is None) else retry
        locking_timeout=self._operation_timeout if timeout is None else timeout
        for t in general_utils.RetryOnException(self._retry_times,exceptions=self.instr.Error):
            with t:
                with self.instr.locking(timeout=locking_timeout):
                    self._instr_write(msg)
                    self.sleep(delay)
                    return self._read_one_try(raw,timeout=timeout,wait_callback=wait_callback)
            if not retry:
                t.reraise()
            error_msg="ask raises IOError; waiting {0} sec before trying to recover".format(self._retry_delay)
            log.default_log.info(error_msg,origin="devices/SCPI",level="warning")
            self.sleep(self._retry_delay)
            self._try_recover(t.try_number)
                
    
    _id_comm="*IDN?" 
    def get_id(self, timeout=None):
        """Get the device IDN. (query SCPI ``'*IDN?'`` command)."""
        return self.ask(self._id_comm,timeout=timeout)
    _reset_comm="*RST"
    def reset(self):
        """Reset the device (by default, ``"*RST"`` command)"""
        return self.write(self._reset_comm)
    _esr_comm="*ESR?"
    def get_esr(self, timeout=None):
        """Get the device status register (by default, ``"*ESR?"`` command)"""
        return self.ask(self._esr_comm,"int")
    def _is_command_valid(self, comm, cached=True):
        """
        Check if the command or the query is valid.

        Send the command, ignore the output, and then check the status bit 5 (command parsing error).
        If ``cached==True``, only check the validity once, and then just use this value in all further attempts.
        """
        if (not cached) or (comm not in self._command_validity_cache):
            self.write(comm)
            self.flush()
            result=not bool(self.get_esr()&0x20)
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
        if isinstance(arg,bool):
            return "bool"
        if isinstance(arg,int):
            return "int"
        if isinstance(arg,float):
            return "float"
        if isinstance(arg,textstring):
            return "string"
        raise ValueError("can't determine type for argument {0}".format(arg))
    _float_fmt="E"
    def _compose_msg(self, msg, arg=None, arg_type=None, unit=None, fmt=None, bool_selector=("OFF","ON")):
        if arg is not None:
            if fmt is not None:
                val=("{"+fmt+"}").format(arg)
            else:
                if arg_type is None:
                    arg_type=self.get_arg_type(arg)
                if arg_type=="string" or arg_type=="raw":
                    val=arg
                elif arg_type=="int":
                    val="{:d}".format(int(arg))
                elif arg_type=="float":
                    val=("{:"+self._float_fmt+"}").format(float(arg))
                elif arg_type=="bool":
                    val="{}".format(bool_selector[1] if arg else bool_selector[0])
                else:
                    raise ValueError("unrecognized arg_type: {0}".format(arg_type))
            msg=msg+" "+val
            if unit is not None:
                msg=msg+" "+unit
        return msg
    def write(self, msg, arg=None, arg_type=None, unit=None, fmt=None, bool_selector=("OFF","ON"), read_echo=False, read_echo_delay=0.):
        """
        Send a command.
        
        Args:
            msg (str): Text message.
            arg: Optional argument to append in the end.
            arg_type (str): Argument type. Can be ``'raw'`` (in which case data is sent raw), ``'string'``, ``'int'``, ``'float'``,
                ``'bool'`` or ``'value'``.
            unit (str): If ``arg_type=='value'``, use it as a unit to append after the value.
            fmt (str): If not ``None``, is a :meth:`str.format` string to convert arg.
            bool_selector (tuple): A tuple ``(false_value, true_value)`` of two strings to represent bool argument.
            read_echo (bool): If ``True``, read a single line after write.
            read_echo_delay (float): The delay between write and read if ``read_echo==True``.
        """
        msg=self._compose_msg(msg,arg,arg_type,unit,fmt,bool_selector)
        self._write_retry(msg)
        if read_echo:
            try:
                self.sleep(read_echo_delay)
                self._read_one_try()
            except self.instr.Error:
                pass
    def _parse_msg(self, msg, data_type="string"):
        if data_type=="raw":
            return msg
        msg=as_str(msg)
        msg=msg.strip()
        if data_type=="string":
            return msg
        elif data_type=="int":
            return int(float(msg))
        elif data_type=="float":
            return float(msg)
        elif data_type=="value":
            msg=msg.split()
            if len(msg)==1:
                return float(msg[0]),None
            elif len(msg)==2:
                return float(msg[0]),msg[1]
            else:
                raise ValueError("empty response")
        elif data_type=="bool":
            msg=msg.lower()
            if msg=="off" or int(msg)==0:
                return False
            else:
                return True
        else:
            raise ValueError("unrecognized data_type: {0}".format(data_type))
    def read(self, data_type="string", timeout=None):
        """
        Read data from the device.
        
        `data_type` determines the type of the data. Can be ``'raw'`` (just raw data), ``'string'`` (with trailing and leading spaces stripped),
        ``'int'``, ``'float'``, ``'bool'`` (interprets ``0`` or ``'off'`` as ``False``, anything else as ``True``), or
        ``'value'`` (returns tuple ``(value, unit)``, where `value` is float).
        `timeout` overrides the default value.
        """
        msg=self._read_retry(raw=(data_type=="raw"),timeout=timeout)
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
                return self._parse_msg(reply,data_type=data_type)
            if not self._failsafe:
                t.reraise()
            error_msg="ask error in instrument {} returned {}".format(self.instr,reply)
            log.default_log.info(error_msg,origin="devices/SCPI",level="warning")
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
                l=l+len(self._read_one_try(raw=True,timeout=0))
                if one_line:
                    return l
        except self.instr.Error:
            return l
    
    @staticmethod
    def parse_trace_data(data, fmt):
        """
        Parse the data returned by the device. `fmt` is :class:`.DataFormat` description.
        
        The data is assumed to be in a (somewhat) standard SCPI format:
        ``b'#'``, then a single digit ``s`` denoting length of the size block,
        then ``s`` digits denoting length of the data (in bytes) followed by the actual data.
        """
        fmt=data_format.DataFormat.from_desc(fmt)
        if data[:1]!=b"#": # range access to accommodate for bytes type in Py3
            if not fmt.is_ascii():
                raise ValueError("malformed data")
            length=None
        else:
            len_size=int(data[1:2]) # range access to accommodate for bytes type in Py3
            length=int(data[2:2+len_size])
            data=data[2+len_size:]
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
                return backend_module.IBackendWrapper.apply_settings(self,settings)
        finally:
            self._setter_echo=True