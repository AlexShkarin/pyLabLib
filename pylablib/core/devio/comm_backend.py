"""
Routines for defining a unified interface across multiple backends.
"""

from ..utils import funcargparse, general, net, py3, module, functions as func_utils
from . import interface
from . import backend_logger
from .base import DeviceError

import time
import re
import contextlib
import warnings
import functools


### Generic backend interface ###


class DeviceBackendError(DeviceError):
    """Generic exception relaying a backend error"""
    def __init__(self, exc):
        msg="backend exception: {} ('{}')".format(repr(exc),str(exc))
        super().__init__(msg)
        self.backend_exc=exc

def reraise(func):
    """Wrapper for a backend method which intercepts backend exceptions and re-emits them as a subclass of :exc:`DeviceBackendError` defined in the class"""
    @functools.wraps(func)
    def wrapped(self, *args, **kwargs):
        if self.Error is None or self.BackendError is None:
            return func(self,*args,**kwargs)
        try:
            return func(self,*args,**kwargs)
        except self.BackendError as exc:
            ReraiseError=getattr(self,"ReraiseError",self.Error)
            raise ReraiseError(exc) from exc
    return wrapped

def logerror(func):
    """Wrapper for a backend method which logs if any errors escaped"""
    @functools.wraps(func)
    def wrapped(self, *args, **kwargs):
        try:
            return func(self,*args,**kwargs)
        except self.Error as exc:
            self._log("error",str(exc))
            raise
    return wrapped

logger=None

class IDeviceCommBackend:
    """
    An abstract class for a device communication backend.
    
    Connection is automatically opened on creation.
    
    Args:
        conn: Connection parameters (depend on the backend).
        timeout (float): Default timeout (in seconds).
        term_write (str): Line terminator for writing operations.
        term_read (str): Line terminator for reading operations.
        datatype (str): Type of the returned data; can be ``"bytes"`` (return ``bytes`` object), ``"str"`` (return ``str`` object),
            or ``"auto"`` (default Python result: ``str`` in Python 2 and ``bytes`` in Python 3)
        reraise_error: if not ``None``, specifies an error to be re-raised on any backend exception (by default, use backend-specific error);
            should be a subclass of :exc:`DeviceBackendError`.
    """
    Error=DeviceBackendError
    BackendError=None
    """Base class for the errors raised by the backend operations"""
    
    _default_operation_cooldown={"default":0.}
    def __init__(self, conn, timeout=None, term_write=None, term_read=None, datatype="auto", reraise_error=None):  # pylint: disable=unused-argument
        funcargparse.check_parameter_range(datatype,"datatype",{"auto","str","bytes"})
        self.datatype=datatype
        self.conn=conn
        self.term_write=term_write
        self.term_read=term_read
        self._operation_cooldown=dict(self._default_operation_cooldown)
        if reraise_error is not None:
            self.Error=reraise_error

    _conn_params=["addr"]
    _default_conn=[None]
    @classmethod
    def _conn_to_dict(cls, conn):
        """Turn connection parameters (tuple or dict) into a full dictionary using class-specific parameter names"""
        if isinstance(conn, dict):
            return conn
        if isinstance(conn, (tuple,list)):
            return dict(zip(cls._conn_params,conn))
        return {cls._conn_params[0]:conn}
    @classmethod
    def combine_conn(cls, conn1, conn2):
        """Combined two connection parameters into a single dictionary (`conn1` overrides `conn2`)"""
        conn=cls._conn_to_dict(conn2).copy()
        conn.update(cls._conn_to_dict(conn1))
        return conn
    @classmethod
    def get_backend_name(cls):
        """Get string representation of the backend (e.g., ``"serial"``, ``"visa"``, or ``"network"``)"""
        return getattr(cls,"_backend",None)

    def _to_datatype(self, data):
        if self.datatype=="auto":
            return data
        if self.datatype=="str":
            return py3.as_str(data)
        return py3.as_bytes(data)
    
    def open(self):
        """Open the connection"""
        pass
    def close(self):
        """Close the connection"""
        pass
    def is_opened(self):
        """Check if the device is connected"""
        return True
    def __bool__(self):
        return self.is_opened()
    __nonzero__=__bool__ # Python 2 compatibility

    def _log(self, operation, value):
        """Log the operation (used for testing and debugging)"""
        if logger:
            logger.log(operation,value)
    
    def lock(self, timeout=None):
        """Lock the access to the device from other threads/processes (isn't necessarily implemented)"""
        pass
    def unlock(self):
        """Unlock the access to the device from other threads/processes (isn't necessarily implemented)"""
        pass
    @contextlib.contextmanager
    def locking(self, timeout=None):  # pylint: disable=unused-argument
        """Context manager for lock & unlock"""
        yield
    
    def setup_cooldown(self, **kwargs):
        """
        Setup cooldown times for various operations.

        The arguments are of the form ``kind=value``, where ``value`` is the cooldown time (in seconds),
        and ``kind`` is the operation kind (common kinds are ``open``, ``close``, ``read``, ``write``, ``timeout``, and ``flush``).
        ``kind`` can also be ``default`` (default value for all kind), or ``all`` (reset all cooldown values to this value).
        The cooldowns of the given kinds are usually called after the corresponding operation (it is necessary for some devices, otherwise the communication can freeze or crush).
        Default cooldown values are specified by ``_default_operation_cooldown`` class attribute dictionary.
        """
        if "all" in kwargs:
            self._operation_cooldown={"default":kwargs.pop("all")}
        self._operation_cooldown.update(kwargs)
    def cooldown(self, kind="default"):
        """
        Cooldown between the operations.
        
        ``kind`` specifies the operation kind (common kinds are ``open``, ``close``, ``read``, ``write``, ``timeout``, and ``flush``);
        ``"default"`` corresponds to the default cooldown (usually, specified as 0).
        Called automatically by various backend operations, so usually there is no need to call explicitly.
        """
        cooldown=self._operation_cooldown.get(kind,self._operation_cooldown.get("default",0))
        if cooldown>0:
            time.sleep(cooldown)
    
    def set_timeout(self, timeout):
        """Set operations timeout (in seconds)"""
        pass
    def get_timeout(self):
        """Get operations timeout (in seconds)"""
        return None
    
    @contextlib.contextmanager
    def using_timeout(self, timeout=None):
        """Context manager for usage of a different timeout inside a block"""
        if timeout is not None:
            to=self.get_timeout()  # pylint: disable=assignment-from-none
            if to!=timeout:
                self.set_timeout(timeout)
        try:
            yield
        finally:
            if timeout is not None and to!=timeout:
                self.set_timeout(to)
    
            
        
    def readline(self, remove_term=True, timeout=None, skip_empty=True):
        """
        Read a single line from the device.
        
        Args:
            remove_term (bool): If ``True``, remove terminal characters from the result.
            timeout: Operation timeout. If ``None``, use the default device timeout.
            skip_empty (bool): If ``True``, ignore empty lines (works only for ``remove_term==True``).
        """
        raise NotImplementedError("IDeviceCommBackend.readline")
    def readlines(self, lines_num, remove_term=True, timeout=None, skip_empty=True):
        """
        Read multiple lines from the device.
        
        Parameters are the same as in :func:`readline`.
        """
        return [self.readline(remove_term=remove_term,timeout=timeout,skip_empty=skip_empty) for _ in range(lines_num)]
    def read(self, size=None):
        """
        Read data from the device.
        
        If `size` is not None, read `size` bytes (the standard timeout applies); otherwise, read all available data (return immediately).
        """
        raise NotImplementedError("IDeviceCommBackend.read")
    def flush_read(self):
        """Flush the device output (read all the available data; return the number of bytes read)"""
        return len(self.read())
    def write(self, data, flush=True, read_echo=False, read_echo_delay=0, read_echo_lines=1):
        """
        Write data to the device.
        
        If ``flush==True``, flush the write buffer.
        If ``read_echo==True``, wait for `read_echo_delay` seconds and then perform :func:`readline` (`read_echo_lines` times).
        """
        raise NotImplementedError("IDeviceCommBackend.write")
    def ask(self, query, delay=0., read_all=False):
        """
        Perform a write followed by a read, with `delay` in between.
        
        If ``read_all==True``, read all the available data; otherwise, read a single line.
        """
        self.write(query)
        if delay:
            time.sleep(delay)
        if read_all:
            return self.read()
        else:
            return self.readline()

    @staticmethod
    def list_resources(desc=False):  # pylint: disable=unused-argument
        """
        List all available resources for this backend.

        If ``desc==False``, return list of connections (usually strings or tuples), which can be used to connect to the device.
        Otherwise, return a list of descriptions, which have more info, but can be backend-dependent.

        Might not be implemented (depending on the backend), in which case returns ``None``.
        """
        return None


### Helper functions ###

def remove_longest_term(msg, terms):
    """
    Remove the longest terminator among `terms` from the end of the message.
    """
    tcs=0
    for t in terms:
        if msg.endswith(py3.as_builtin_bytes(t)):
            tcs=max(tcs,len(t))
    return msg[:-tcs]
    


### Specific backends ###

_backends={}
_backend_errors={}
_backend_install_message=("{name:} package is missing. You can install it via PyPi as 'pip install {pkg:}'. "
    "If it is installed, check if it imports correctly by running 'import {mod:}'")

try:
    try:
        import pyvisa as visa
    except ImportError:
        import visa

    class DeviceVisaError(DeviceBackendError):
        """Visa backend operation error"""

    class VisaDeviceBackend(IDeviceCommBackend):
        """
        NIVisa backend (via pyVISA).
        
        Connection is automatically opened on creation.
        
        Args:
            conn (str): Connection string.
            timeout (float): Default timeout (in seconds).
            term_write (str): Line terminator for writing operations; appended to the data
            term_read (str): Line terminator for reading operations (specifies when :func:`readline` stops).
            do_lock (bool): If ``True``, employ locking operations; otherwise, locking function does nothing.
            datatype (str): Type of the returned data; can be ``"bytes"`` (return `bytes` object), ``"str"`` (return `str` object),
                or ``"auto"`` (default Python result: `str` in Python 2 and `bytes` in Python 3)
            reraise_error: if not ``None``, specifies an error to be re-raised on any backend exception (by default, use backend-specific error);
                should be a subclass of :exc:`DeviceBackendError`.
        """
        _backend="visa"
        BackendError=visa.VisaIOError
        """Base class for the errors raised by the backend operations"""
        Error=DeviceVisaError
        
        if module.cmp_versions(visa.__version__,"1.6")=="<": # older pyvisa versions have a slightly different interface
            @reraise
            def _set_timeout(self, timeout):
                self.instr.timeout=timeout
            @reraise
            def _get_timeout(self):
                return self.instr.timeout
            @reraise
            def _open_resource(self, conn):
                if not self.term_write.endswith(self.term_read):
                    raise NotImplementedError("PyVisa version <1.6 doesn't support different terminators for reading and writing; update to a newer version by running 'pip install --upgrade pyvisa'")
                instr=visa.instrument(conn) # pylint: disable=no-member
                instr.term_chars=self.term_read
                self.term_write=self.term_write[:len(self.term_write)-len(self.term_read)]
                return instr
            _lock_default=False
            def _lock(self, timeout=None):
                raise NotImplementedError("PyVisa version <1.6 doesn't support locking; update to a newer version by running 'pip install --upgrade pyvisa'")
            def _unlock(self):
                raise NotImplementedError("PyVisa version <1.6 doesn't support locking; update to a newer version by running 'pip install --upgrade pyvisa'")
            def _lock_context(self, timeout=None):
                raise NotImplementedError("PyVisa version <1.6 doesn't support locking; update to a newer version by running 'pip install --upgrade pyvisa'")
            @reraise
            def _read_term(self):
                return py3.as_builtin_bytes(self.instr.term_chars)
        else:
            @reraise
            def _set_timeout(self, timeout):
                self.instr.timeout=timeout*1000. # in newer versions timeout is in ms
            @reraise
            def _get_timeout(self):
                return self.instr.timeout/1000. # in newer versions timeout is in ms
            @reraise
            def _open_resource(self, conn):
                instr=visa.ResourceManager().open_resource(conn)
                instr.read_termination=self.term_read
                instr.write_termination=self.term_write
                self.term_read=self.term_write=""
                return instr
            _lock_default=False
            @reraise
            def _lock(self, timeout=None):
                self.instr.lock(timeout=timeout*1000. if timeout is not None else None)
            @reraise
            def _unlock(self):
                self.instr.unlock()
            @reraise
            def _lock_context(self, timeout=None):
                return self.instr.lock_context(timeout=timeout*1000. if timeout is not None else None)
            @reraise
            def _read_term(self):
                return py3.as_builtin_bytes(self.instr.read_termination)
            @staticmethod
            def list_resources(desc=False):
                try:
                    return visa.ResourceManager().list_resources_info() if desc else visa.ResourceManager().list_resources()
                except VisaDeviceBackend.BackendError as e:
                    raise VisaDeviceBackend.Error(e) from e
        if module.cmp_versions(visa.__version__,"1.9")=="<": # older pyvisa versions have a slightly different interface
            @reraise
            def _read_raw(self, size):
                chunk_size=self.instr.chunk_size
                data=bytearray()
                with self.instr.ignore_warning(visa.constants.VI_SUCCESS_DEV_NPRESENT,visa.constants.VI_SUCCESS_MAX_CNT):
                    while len(data)<size:
                        to_read=min(chunk_size,size-len(data))
                        chunk,_=self.instr.visalib.read(self.instr.session,to_read)
                        data.extend(chunk)
                return bytes(data)
        else:
            @reraise
            def _read_raw(self, size):
                return self.instr.read_bytes(size)
        @reraise
        def _read_all(self):
            data=bytearray()
            with self.using_timeout(0):
                while True:
                    try:
                        chunk=self.instr.read_raw()
                        data.extend(chunk)
                    except visa.VisaIOError as err:
                        if err.abbreviation=="VI_ERROR_TMO":
                            return bytes(data)
                        else:
                            raise
        
        def __init__(self, conn, timeout=10., term_write=None, term_read=None, do_lock=None, datatype="auto", reraise_error=None):
            if term_write is None:
                term_write=b"\r\n"
            if term_read is None:
                term_read=b"\n"
            IDeviceCommBackend.__init__(self,conn,term_write=term_write,term_read=term_read,datatype=datatype,reraise_error=reraise_error)
            try:
                self.instr=self._open_resource(self.conn)
                self.opened=True
                self._do_lock=do_lock if do_lock is not None else self._lock_default
                self.cooldown("open")
                self.set_timeout(timeout)
            except self.BackendError as e:
                raise self.Error(e) from e

        @reraise
        def open(self):
            """Open the connection"""
            self.instr.open()
            self.opened=True
            self.cooldown("open")
        @reraise
        def close(self):
            """Close the connection"""
            self.instr.close()
            self.opened=False
            self.cooldown("close")
        def is_opened(self):
            return self.opened

        def lock(self, timeout=None):
            """Lock the access to the device from other threads/processes"""
            if self._do_lock:
                self.lock(timeout=timeout)
        def unlock(self):
            """Unlock the access to the device from other threads/processes"""
            if self._do_lock:
                self.unlock()
        def locking(self, timeout=None):
            """Context manager for lock & unlock"""
            if self._do_lock:
                return self._lock_context(timeout=timeout)
            else:
                return general.DummyResource()
        
        def set_timeout(self, timeout):
            """Set operations timeout (in seconds)"""
            if timeout is not None:
                self._set_timeout(timeout)
                self.cooldown("timeout")
        def get_timeout(self):
            """Get operations timeout (in seconds)"""
            return self._get_timeout()
        
        @logerror
        @reraise
        def readline(self, remove_term=True, timeout=None, skip_empty=True):
            """
            Read a single line from the device.
            
            Args:
                remove_term (bool): If ``True``, remove terminal characters from the result.
                timeout: Operation timeout. If ``None``, use the default device timeout.
                skip_empty (bool): If ``True``, ignore empty lines (works only for ``remove_term==True``).
            """
            with self.using_timeout(timeout):
                while True:
                    result=self.instr.read_raw()
                    if remove_term:
                        term=self._read_term()
                        if term and result.endswith(term):
                            result=result[:-len(term)]
                    if (not skip_empty) or result:
                        break
            self.cooldown("read")
            self._log("read",result)
            return self._to_datatype(result)
        @logerror
        def read(self, size=None):
            """
            Read data from the device.
            
            If `size` is not None, read `size` bytes (the standard timeout applies); otherwise, read all available data (return immediately).
            """
            result=self._read_all() if size is None else self._read_raw(size=size)
            self.cooldown("read")
            self._log("read",result)
            return self._to_datatype(result)
        
        @logerror
        @reraise
        def write(self, data, flush=True, read_echo=False, read_echo_delay=0, read_echo_lines=1):
            """
            Write data to the device.
            
            If ``read_echo==True``, wait for `read_echo_delay` seconds and then perform :func:`readline` (`read_echo_lines` times).
            `flush` parameter is ignored.
            """
            self._log("write",data)
            data=py3.as_builtin_bytes(data)
            if self.term_write:
                data=data+py3.as_builtin_bytes(self.term_write)
            self.instr.write_raw(data)
            self.cooldown("write")
            if read_echo_delay>0.:
                time.sleep(read_echo_delay)
            if read_echo:
                for _ in range(read_echo_lines):
                    self.readline()

        @reraise
        def __repr__(self):
            return "VisaDeviceBackend("+self.instr.__repr__()+")"
                
                
    _backends["visa"]=VisaDeviceBackend
except ImportError:
    pass
_backend_errors["visa"]=_backend_install_message.format(name="PyVISA",pkg="pyvisa",mod="pyvisa")


try:
    import serial
    
    try:
        import serial.tools.list_ports as serial_list_ports
    except ImportError:
        serial_list_ports=None

    class DeviceSerialError(DeviceBackendError):
        """Serial backend operation error"""

    class SerialDeviceBackend(IDeviceCommBackend):
        """
        Serial backend (via pySerial).
        
        Connection is automatically opened on creation.
        
        Args:
            conn: Connection parameters. Can be either a string (for a port),
                or a list/tuple ``(port, baudrate, bytesize, parity, stopbits, xonxoff, rtscts, dsrdtr)`` supplied to the serial connection
                (default is ``('COM1',19200,8,'N',1,0,0,0)``),
                or a dict with the same parameters.
            timeout (float): Default timeout (in seconds).
            term_write (str): Line terminator for writing operations; appended to the data
            term_read (str): List of possible single-char terminator for reading operations (specifies when :func:`readline` stops).
            connect_on_operation (bool): If ``True``, the connection is normally closed, and is opened only on the operations
                (normally two processes can't be simultaneously connected to the same device).
            open_retry_times (int): Number of times the connection is attempted before giving up.
            no_dtrrts (bool): If ``True``, turn off DTR and RTS status lines before opening (e.g., turns off reset-on-connection for Arduino controllers).
            datatype (str): Type of the returned data; can be ``"bytes"`` (return `bytes` object), ``"str"`` (return `str` object),
                or ``"auto"`` (default Python result: `str` in Python 2 and `bytes` in Python 3)
            reraise_error: if not ``None``, specifies an error to be re-raised on any backend exception (by default, use backend-specific error);
                should be a subclass of :exc:`DeviceBackendError`.
        """
        _backend="serial"
        BackendError=serial.SerialException
        """Base class for the errors raised by the backend operations"""
        Error=DeviceSerialError
        
        _conn_params=["port","baudrate","bytesize","parity","stopbits","xonxoff","rtscts","dsrdtr"]
        _default_conn=["COM1",19200,8,"N",1,0,0,0]

        def __init__(self, conn, timeout=10., term_write=None, term_read=None, connect_on_operation=False, open_retry_times=3, no_dtrrts=False, datatype="auto", reraise_error=None):
            conn_dict=self.combine_conn(conn,self._default_conn)
            if term_write is None:
                term_write=b"\r\n"
            if term_read is None:
                term_read=b"\n"
            if isinstance(term_read,py3.anystring):
                term_read=[term_read]
            IDeviceCommBackend.__init__(self,conn_dict.copy(),term_write=term_write,term_read=term_read,datatype=datatype,reraise_error=reraise_error)
            port=conn_dict.pop("port")
            try:
                self.instr=serial.serial_for_url(port,do_not_open=True,**conn_dict)
                self.opened=True
                if no_dtrrts:
                    try:
                        self.instr.setDTR(0)
                        self.instr.setRTS(0)
                    except self.BackendError:
                        warnings.warn("Cannot set DTR for an unconnected device")
                if not connect_on_operation:
                    self.instr.open()
                self._connect_on_operation=connect_on_operation
                self._opened_stack=0
                self._open_retry_times=open_retry_times
                self.cooldown("open")
                self.set_timeout(timeout)
            except self.BackendError as e:
                raise self.Error(e) from e
        
        @reraise
        def _do_open(self):
            general.retry_wait(self.instr.open, self._open_retry_times, 0.3)
        @reraise
        def _do_close(self):
            general.retry_wait(self.instr.close, self._open_retry_times, 0.3)
        def open(self):
            """Open the connection"""
            if not self._connect_on_operation and not self.opened:
                self._do_open()
            self.opened=True
        def close(self):
            """Close the connection"""
            if not self._connect_on_operation and self.opened:
                self._do_close()
            self.opened=False
        def is_opened(self):
            return self.opened
        def _op_open(self):
            if self._connect_on_operation:
                if not self._opened_stack:
                    self._do_open()
                self._opened_stack=self._opened_stack+1
        def _op_close(self):
            if self._connect_on_operation:
                self._opened_stack=self._opened_stack-1
                if not self._opened_stack:
                    self._do_close()
        @contextlib.contextmanager
        def single_op(self):
            """
            Context manager for a single operation.
            
            If ``connect_on_operation==True`` during creation, wrapping several command in `single_op`
            prevents the connection from being closed and reopened between the operations (only opened in the beginning and closed in the end).
            """
            self._op_open()
            try:
                yield
            finally:
                self._op_close()
            
        @reraise
        def set_timeout(self, timeout):
            """Set operations timeout (in seconds)"""
            if timeout is not None:
                self.instr.timeout=timeout
                self.cooldown("timeout")
        @reraise
        def get_timeout(self):
            """Get operations timeout (in seconds)"""
            return self.instr.timeout
        
        @reraise
        def _read_terms(self, terms=(), timeout=None, error_on_timeout=True):
            result=b""
            singlechar_terms=all(len(t)==1 for t in terms)
            terms=[py3.as_builtin_bytes(t) for t in terms]
            with self.single_op():
                with self.using_timeout(timeout):
                    while True:
                        c=self.instr.read(1 if terms else 8)
                        result=result+c
                        if c==b"":
                            if error_on_timeout and terms:
                                raise self.Error("timeout during read")
                            return result
                        if singlechar_terms:
                            if c in terms:
                                return result
                        else:
                            for t in terms:
                                if result.endswith(t):
                                    return result
        @logerror
        def readline(self, remove_term=True, timeout=None, skip_empty=True, error_on_timeout=True):  # pylint: disable=arguments-differ
            """
            Read a single line from the device.
            
            Args:
                remove_term (bool): If ``True``, remove terminal characters from the result.
                timeout: Operation timeout. If ``None``, use the default device timeout.
                skip_empty (bool): If ``True``, ignore empty lines (works only for ``remove_term==True``).
                error_on_timeout (bool): If ``False``, return an incomplete line instead of raising the error on timeout.
            """
            while True:
                result=self._read_terms(self.term_read or [],timeout=timeout,error_on_timeout=error_on_timeout)
                self.cooldown("read")
                if remove_term and self.term_read:
                    result=remove_longest_term(result,self.term_read)
                if not (skip_empty and remove_term and (not result)):
                    break
            self._log("read",result)
            return self._to_datatype(result)
        @logerror
        @reraise
        def read(self, size=None):
            """
            Read data from the device.
            
            If `size` is not None, read `size` bytes (usual timeout applies); otherwise, read all available data (return immediately).
            """
            with self.single_op():
                if size is None:
                    result=self._read_terms(timeout=0,error_on_timeout=False)
                else:
                    result=self.instr.read(size=size)
                    if len(result)!=size:
                        raise self.Error("read returned less than expected: {} instead of {}".format(len(result),size))
                self.cooldown("read")
                self._log("read",result)
                return self._to_datatype(result)
        @logerror
        def read_multichar_term(self, term, remove_term=True, timeout=None, error_on_timeout=True):
            """
            Read a single line with multiple possible terminators.
            
            Args:
                term: Either a string (single multi-char terminator) or a list of strings (multiple terminators).
                remove_term (bool): If ``True``, remove terminal characters from the result.
                timeout: Operation timeout. If ``None``, use the default device timeout.
                error_on_timeout (bool): If ``False``, return an incomplete line instead of raising the error on timeout.
            """
            if isinstance(term,py3.anystring):
                term=[term]
            result=self._read_terms(term,timeout=timeout,error_on_timeout=error_on_timeout)
            self.cooldown("read")
            if remove_term and term:
                result=remove_longest_term(result,term)
            self._log("read",result)
            return self._to_datatype(result)
        @logerror
        @reraise
        def write(self, data, flush=True, read_echo=False, read_echo_delay=0, read_echo_lines=1):
            """
            Write data to the device.
            
            If ``flush==True``, flush the write buffer.
            If ``read_echo==True``, wait for `read_echo_delay` seconds and then perform :func:`readline` (`read_echo_lines` times).
            """
            self._log("write",data)
            with self.single_op():
                data=py3.as_builtin_bytes(data)
                if self.term_write:
                    data=data+py3.as_builtin_bytes(self.term_write)
                self.instr.write(data)
                self.cooldown("write")
                if flush:
                    self.instr.flush()
                    self.cooldown("flush")
                if read_echo_delay>0.:
                    time.sleep(read_echo_delay)
                if read_echo:
                    for _ in range(read_echo_lines):
                        self.readline()

        @reraise
        def __repr__(self):
            return "SerialDeviceBackend("+self.instr.__repr__()+")"

        @staticmethod
        def list_resources(desc=False):
            if serial_list_ports is not None:
                try:
                    return [(p if desc else p[0]) for p in serial_list_ports.comports()]
                except SerialDeviceBackend.BackendError as e:
                    raise SerialDeviceBackend.Error(e) from e

        
    _backends["serial"]=SerialDeviceBackend
except (ImportError, AttributeError):
    pass
_backend_errors["serial"]=_backend_install_message.format(name="PySerial",pkg="pyserial",mod="serial")




try:
    import ft232

    class DeviceFT232Error(DeviceBackendError):
        """FT232 backend operation error"""

    class FT232DeviceBackend(IDeviceCommBackend):
        """
        FT232 backend (via pyft232).
        
        Connection is automatically opened on creation.
        
        Args:
            conn: Connection parameters. Can be either a string (for a port),
                or a list/tuple ``(port, baudrate, bytesize, parity, stopbits, xonxoff, rtscts)`` supplied to the serial connection
                (default is ``('COM1',19200,8,'N',1,0,0,0)``),
                or a dict with the same parameters.
            timeout (float): Default timeout (in seconds).
            term_write (str): Line terminator for writing operations; appended to the data
            term_read (str): List of possible single-char terminator for reading operations (specifies when :func:`readline` stops).
            open_retry_times (int): Number of times the connection is attempted before giving up.
            datatype (str): Type of the returned data; can be ``"bytes"`` (return `bytes` object), ``"str"`` (return `str` object),
                or ``"auto"`` (default Python result: `str` in Python 2 and `bytes` in Python 3)
            reraise_error: if not ``None``, specifies an error to be re-raised on any backend exception (by default, use backend-specific error);
                should be a subclass of :exc:`DeviceBackendError`.
        """
        _backend="ft232"
        BackendError=ft232.Ft232Exception
        """Base class for the errors raised by the backend operations"""
        Error=DeviceFT232Error
        
        _conn_params=["port","baudrate","bytesize","parity","stopbits","xonxoff","rtscts"]
        _default_conn=[None,9600,8,"N",1,0,0]

        def __init__(self, conn, timeout=10., term_write=None, term_read=None, open_retry_times=3, datatype="auto", reraise_error=None):
            conn_dict=self.combine_conn(conn,self._default_conn)
            if term_write is None:
                term_write=b"\r\n"
            if term_read is None:
                term_read=b"\n"
            if isinstance(term_read,py3.anystring):
                term_read=[term_read]
            conn_dict=conn_dict.copy()
            conn_dict["port"]=str(conn_dict["port"])
            IDeviceCommBackend.__init__(self,conn_dict.copy(),term_write=term_write,term_read=term_read,datatype=datatype,reraise_error=reraise_error)
            port=conn_dict.pop("port")
            self.opened=False
            try:
                self.instr=self._open_instr(port,conn_dict)
                self.opened=True
                self._open_retry_times=open_retry_times
                self.cooldown("open")
                self.set_timeout(timeout)
                self._conn_params=(port,conn_dict,timeout)
            except self.BackendError as e:
                raise self.Error(e) from e

        def _open_instr(self, port, params):
            sig=func_utils.funcsig(ft232.Ft232)
            if "serial_number" in sig.arg_names: # pyft232 v0.11 signature change
                return ft232.Ft232(serial_number=port,**params)
            else:
                return ft232.Ft232(port,**params)
        @reraise
        def _do_open(self):
            if self.is_opened():
                return
            def reopen():
                self.instr=self._open_instr(self._conn_params[0],self._conn_params[1])
                self.set_timeout(self._conn_params[2])
                self.opened=True
            general.retry_wait(reopen, self._open_retry_times, 0.3)
        @reraise
        def _do_close(self):
            if self.is_opened():
                general.retry_wait(self.instr.close, self._open_retry_times, 0.3)
                self.opened=False
        def open(self):
            """Open the connection"""
            self._do_open()
        def close(self):
            """Close the connection"""
            self._do_close()
        def is_opened(self):
            return self.opened
        @contextlib.contextmanager
        def single_op(self):
            """
            Context manager for a single operation.
            
            Does nothing.
            """
            yield
            
        
        @reraise
        def set_timeout(self, timeout):
            """Set operations timeout (in seconds)"""
            if timeout is not None:
                if timeout<1E-3:
                    timeout=1E-3 # 0 is infinite timeout
                self.instr.timeout=timeout
                self.cooldown("timeout")
        @reraise
        def get_timeout(self):
            """Get operations timeout (in seconds)"""
            return self.instr.timeout
        
        
        @reraise
        def _read_terms(self, terms=(), timeout=None, error_on_timeout=True):
            result=b""
            singlechar_terms=all(len(t)==1 for t in terms)
            terms=[py3.as_builtin_bytes(t) for t in terms]
            with self.single_op():
                with self.using_timeout(timeout):
                    while True:
                        c=self.instr.read(1 if terms else 8)
                        result=result+c
                        if c==b"":
                            if error_on_timeout and terms:
                                raise self.Error("timeout during read")
                            return result
                        if singlechar_terms:
                            if c in terms:
                                return result
                        else:
                            for t in terms:
                                if result.endswith(t):
                                    return result
        @logerror
        def readline(self, remove_term=True, timeout=None, skip_empty=True, error_on_timeout=True):  # pylint: disable=arguments-differ
            """
            Read a single line from the device.
            
            Args:
                remove_term (bool): If ``True``, remove terminal characters from the result.
                timeout: Operation timeout. If ``None``, use the default device timeout.
                skip_empty (bool): If ``True``, ignore empty lines (works only for ``remove_term==True``).
                error_on_timeout (bool): If ``False``, return an incomplete line instead of raising the error on timeout.
            """
            while True:
                result=self._read_terms(self.term_read or [],timeout=timeout,error_on_timeout=error_on_timeout)
                self.cooldown("read")
                if remove_term and self.term_read:
                    result=remove_longest_term(result,self.term_read)
                if not (skip_empty and remove_term and (not result)):
                    break
            self._log("read",result)
            return self._to_datatype(result)
        @logerror
        @reraise
        def read(self, size=None):
            """
            Read data from the device.
            
            If `size` is not None, read `size` bytes (usual timeout applies); otherwise, read all available data (return immediately).
            """
            with self.single_op():
                if size is None:
                    result=self._read_terms(timeout=0,error_on_timeout=False)
                else:
                    result=self.instr.read(size=size)
                    if len(result)!=size:
                        raise self.Error("read returned less data than expected")
                self.cooldown("read")
                self._log("read",result)
                return self._to_datatype(result)
        @logerror
        def read_multichar_term(self, term, remove_term=True, timeout=None, error_on_timeout=True):
            """
            Read a single line with multiple possible terminators.
            
            Args:
                term: Either a string (single multi-char terminator) or a list of strings (multiple terminators).
                remove_term (bool): If ``True``, remove terminal characters from the result.
                timeout: Operation timeout. If ``None``, use the default device timeout.
                error_on_timeout (bool): If ``False``, return an incomplete line instead of raising the error on timeout.
            """
            if isinstance(term,py3.anystring):
                term=[term]
            result=self._read_terms(term,timeout=timeout,error_on_timeout=error_on_timeout)
            self.cooldown("read")
            if remove_term and term:
                result=remove_longest_term(result,term)
            self._log("read",result)
            return self._to_datatype(result)
        @logerror
        @reraise
        def write(self, data, flush=True, read_echo=False, read_echo_delay=0, read_echo_lines=1):
            """
            Write data to the device.
            
            If ``flush==True``, flush the write buffer.
            If ``read_echo==True``, wait for `read_echo_delay` seconds and then perform :func:`readline` (`read_echo_lines` times).
            """
            self._log("write",data)
            with self.single_op():
                data=py3.as_builtin_bytes(data)
                if self.term_write:
                    data=data+py3.as_builtin_bytes(self.term_write)
                self.instr.write(data)
                self.cooldown("write")
                if flush:
                    self.instr.flush()
                    self.cooldown("flush")
                if read_echo_delay>0.:
                    time.sleep(read_echo_delay)
                if read_echo:
                    for _ in range(read_echo_lines):
                        self.readline()

        @reraise
        def __repr__(self):
            return "FT232DeviceBackend("+self.instr.__repr__()+")"

        @staticmethod
        def _as_str(v):
            if isinstance(v,py3.anystring):
                return py3.as_str(v)
            if isinstance(v,(tuple,list)):
                return type(v)([FT232DeviceBackend._as_str(e) for e in v])
            return s
        @staticmethod
        def list_resources(desc=False):
            try:
                devices=[FT232DeviceBackend._as_str(d) for d in ft232.list_devices()]
                return [d if desc else d[0] for d in devices]
            except FT232DeviceBackend.BackendError as e:
                raise FT232DeviceBackend.Error(e) from e
        
        
    _backends["ft232"]=FT232DeviceBackend
except (ImportError,NameError,OSError):
    pass
_backend_errors["ft232"]=_backend_install_message.format(name="pyft232",pkg="pyft232",mod="ft232")



class DeviceNetworkError(DeviceBackendError):
    """Network backend operation error"""

class NetworkDeviceBackend(IDeviceCommBackend):
    """
    Serial backend (via pySerial).
    
    Connection is automatically opened on creation.
    
    Args:
        conn: Connection parameters. Can be either a string ``"IP:port"`` (e.g., ``"127.0.0.1:80"``), or a tuple ``(IP,port)``, where `IP` is a string and `port` is a number.
        timeout (float): Default timeout (in seconds).
        term_write (str): Line terminator for writing operations; appended to the data
        term_read (str): List of possible single-char terminator for reading operations (specifies when :func:`readline` stops).
        datatype (str): Type of the returned data; can be ``"bytes"`` (return `bytes` object), ``"str"`` (return `str` object),
            or ``"auto"`` (default Python result: `str` in Python 2 and `bytes` in Python 3)
        reraise_error: if not ``None``, specifies an error to be re-raised on any backend exception (by default, use backend-specific error);
            should be a subclass of :exc:`DeviceBackendError`.
        
    Note:
        If `term_read` is a string, its behavior is different from the VISA backend:
        instead of being a multi-char terminator it is assumed to be a set of single-char terminators.
        If multi-char terminator is required, `term_read` should be a single-element list instead of a string.
    """
    _backend="network"
    BackendError=net.socket.error
    """Base class for the errors raised by the backend operations"""
    Error=DeviceNetworkError

    def __init__(self, conn, timeout=10., term_write=None, term_read=None, datatype="auto", reraise_error=None):
        if term_write is None:
            term_write="\r\n"
        if term_read is None:
            term_read="\r\n"
        if isinstance(term_read,py3.anystring):
            term_read=[term_read]
        conn=self._conn_to_dict(conn)
        self._split_addr(conn)
        IDeviceCommBackend.__init__(self,conn,term_write=term_write,term_read=term_read,datatype=datatype,reraise_error=reraise_error)
        try:
            self.socket=None
            self.open()
            self.cooldown("open")
            self.set_timeout(timeout)
        except self.BackendError as e:
            raise self.Error(e) from e
    
    _conn_params=["addr","port"]
    _default_conn=["127.0.0.1",80]
    @classmethod
    def _split_addr(cls, conn):
        addr=conn["addr"]
        addr_split=addr.split(":")
        if len(addr_split)==2:
            conn["addr"],conn["port"]=addr_split[0],int(addr_split[1])
        elif len(addr_split)>2:
            raise ValueError("invalid device address: {}".format(conn))
    @reraise
    def open(self):
        """Open the connection"""
        self.close()
        self.socket=net.ClientSocket(send_method="fixedlen",recv_method="fixedlen")
        self.socket.connect(self.conn["addr"],self.conn["port"])
    @reraise
    def close(self):
        """Close the connection"""
        if self.socket is not None:
            self.socket.close()
            self.socket=None
    @reraise
    def is_opened(self):
        return bool(self.socket)
        
    @reraise
    def set_timeout(self, timeout):
        """Set operations timeout (in seconds)"""
        self.socket.set_timeout(timeout)
    @reraise
    def get_timeout(self):
        """Get operations timeout (in seconds)"""
        return self.socket.get_timeout()
    

    @logerror
    @reraise
    def readline(self, remove_term=True, timeout=None, skip_empty=True):
        """
        Read a single line from the device.
        
        Args:
            remove_term (bool): If ``True``, remove terminal characters from the result.
            timeout: Operation timeout. If ``None``, use the default device timeout.
            skip_empty (bool): If ``True``, ignore empty lines (works only for ``remove_term==True``).
        """
        while True:
            with self.using_timeout(timeout):
                result=self.socket.recv_delimiter(self.term_read,strict=True)
            self.cooldown("read")
            if remove_term and self.term_read:
                result=remove_longest_term(result,self.term_read)
            if not (skip_empty and remove_term and (not result)):
                break
        self._log("read",result)
        return self._to_datatype(result)
    @logerror
    @reraise
    def read(self, size=None):
        """
        Read data from the device.
        
        If `size` is not None, read `size` bytes (usual timeout applies); otherwise, read all available data (return immediately).
        """
        if size is None:
            return self.socket.recv_all()
        else:
            result=self.socket.recv_fixedlen(size)
        self.cooldown("read")
        self._log("read",result)
        return self._to_datatype(result)
    @logerror
    @reraise
    def read_multichar_term(self, term, remove_term=True, timeout=None):
        """
        Read a single line with multiple possible terminators.
        
        Args:
            term: Either a string (single multi-char terminator) or a list of strings (multiple terminators).
            remove_term (bool): If ``True``, remove terminal characters from the result.
            timeout: Operation timeout. If ``None``, use the default device timeout.
        """
        if isinstance(term,py3.anystring):
            term=[term]
        with self.socket.using_timeout(timeout):
            result=self.socket.recv_delimiter(term,strict=True)
        self.cooldown("read")
        if remove_term and term:
            result=remove_longest_term(result,term)
        self._log("read",result)
        return self._to_datatype(result)
    @logerror
    @reraise
    def write(self, data, flush=True, read_echo=False, read_echo_delay=0, read_echo_lines=1):
        """
        Write data to the device.
        
        If ``read_echo==True``, wait for `read_echo_delay` seconds and then perform :func:`readline` (`read_echo_lines` times).
        `flush` parameter is ignored.
        """
        self._log("write",data)
        self.socket.send_delimiter(data,self.term_write)
        self.cooldown("write")
        if read_echo_delay>0.:
            time.sleep(read_echo_delay)
        if read_echo:
            for _ in range(read_echo_lines):
                self.readline()

    @reraise
    def __repr__(self):
        return "NetworkDeviceBackend("+self.socket.__repr__()+")"
    
    
_backends["network"]=NetworkDeviceBackend




try:
    import usb
    import usb.backend.libusb0
    import usb.backend.libusb1
    import usb.backend.openusb

    class DeviceUSBError(DeviceBackendError):
        """USB backend operation error"""

    class PyUSBDeviceBackend(IDeviceCommBackend):
        """
        USB backend (via PyUSB package).
        
        Connection is automatically opened on creation.
        
        Args:
            conn: Connection parameters. Can be either a string (for a port),
                or a list/tuple ``(vendorID, productID, index, endpoint_read, endpoint_write, backend)`` supplied to the connection
                (default is ``(0x0000,0x0000,0,0x00,0x01,'libusb1')``, which is invalid for most devices),
                or a dict with the same parameters.
                ``vendorID`` and ``productID`` specify device kind, ``index`` is an integer index (starting from zero) of the device
                among several identical (i.e., with the same ids) ones, and ``endpoint_read`` and ``endpoint_write`` specify connection endpoints for the specific device.
            timeout (float): Default timeout (in seconds).
            term_write (str): Line terminator for writing operations; appended to the data
            term_read (str): List of possible single-char terminator for reading operations (specifies when :func:`readline` stops).
            datatype (str): Type of the returned data; can be ``"bytes"`` (return `bytes` object), ``"str"`` (return `str` object),
                or ``"auto"`` (default Python result: `str` in Python 2 and `bytes` in Python 3)
            reraise_error: if not ``None``, specifies an error to be re-raised on any backend exception (by default, use backend-specific error);
                should be a subclass of :exc:`DeviceBackendError`.
        """
        _backend="pyusb"
        BackendError=usb.USBError
        """Base class for the errors raised by the backend operations"""
        Error=DeviceUSBError
        
        _conn_params=["vendorID","productID","index","endpoint_read","endpoint_write","backend"]
        _default_conn=[0x0000,0x0000,0,0x00,0x01,"libusb1"]
        _usb_backends={"libusb0":usb.backend.libusb0, "libusb1":usb.backend.libusb1, "openusb":usb.backend.openusb}

        def __init__(self, conn, timeout=10., term_write=None, term_read=None, check_read_size=True, datatype="auto", reraise_error=None):
            conn_dict=self.combine_conn(conn,self._default_conn)
            funcargparse.check_parameter_range(conn_dict["backend"],"usb_backend",self._usb_backends)
            if isinstance(term_read,py3.anystring):
                term_read=[term_read]
            IDeviceCommBackend.__init__(self,conn_dict.copy(),term_write=term_write,term_read=term_read,datatype=datatype,reraise_error=reraise_error)
            self.timeout=timeout
            self.check_read_size=check_read_size
            try:
                self.open()
            except self.BackendError as e:
                raise self.Error(e) from e
            self.cooldown("open")
            
        @reraise
        def open(self):
            """Open the connection"""
            idx=self.conn["index"]
            backend=self._usb_backends[self.conn["backend"]].get_backend()
            all_devs=list(usb.core.find(idVendor=self.conn["vendorID"],idProduct=self.conn["productID"],backend=backend,find_all=True))
            if len(all_devs)<idx+1:
                raise self.Error("can't find device with VID=0x{:04x} PID=0x{:04x} index {}; {} devices found".format(
                        self.conn["vendorID"],self.conn["productID"],idx,len(all_devs)))
            self.instr=all_devs[idx]
            self.ep_read=self.conn["endpoint_read"]
            self.ep_write=self.conn["endpoint_write"]
            self.cooldown("open")
            self.opened=True
        @reraise
        def close(self):
            """Close the connection"""
            self.instr.finalize()
            self.opened=False
        def is_opened(self):
            return self.opened
            
        
        def set_timeout(self, timeout):
            """Set operations timeout (in seconds)"""
            if timeout is not None:
                self.timeout=timeout
        def get_timeout(self):
            """Get operations timeout (in seconds)"""
            return self.timeout
        def _timeout(self, timeout=None):
            timeout=self.timeout if timeout is None else timeout
            return None if timeout is None else int(timeout*1000)
        
        
        @reraise
        def _read_terms(self, terms=(), read_block_size=65536, timeout=None, error_on_timeout=True):
            result=b""
            singlechar_terms=all(len(t)==1 for t in terms)
            terms=[py3.as_builtin_bytes(t) for t in terms]
            while True:
                try:
                    c=self.instr.read(self.ep_read,1 if terms else read_block_size,timeout=self._timeout(timeout)).tobytes()
                except self.BackendError:
                    c=b""
                result=result+c
                if c==b"":
                    if error_on_timeout and terms:
                        raise self.Error("timeout during read")
                    return result
                if not terms:
                    return result
                if singlechar_terms:
                    if c in terms:
                        return result
                else:
                    for t in terms:
                        if result.endswith(t):
                            return result
        @logerror
        def readline(self, remove_term=True, timeout=None, skip_empty=True, error_on_timeout=True):  # pylint: disable=arguments-differ
            """
            Read a single line from the device.
            
            Args:
                remove_term (bool): If ``True``, remove terminal characters from the result.
                timeout: Operation timeout. If ``None``, use the default device timeout.
                skip_empty (bool): If ``True``, ignore empty lines (works only for ``remove_term==True``).
                error_on_timeout (bool): If ``False``, return an incomplete line instead of raising the error on timeout.
            """
            while True:
                result=self._read_terms(self.term_read or [],timeout=timeout,error_on_timeout=error_on_timeout)
                self.cooldown("read")
                if remove_term and self.term_read:
                    result=remove_longest_term(result,self.term_read)
                if not (skip_empty and remove_term and (not result)):
                    break
            self._log("read",result)
            return self._to_datatype(result)
        @logerror
        @reraise
        def read(self, size=None, max_read_size=65536):  # pylint: disable=arguments-differ
            """
            Read data from the device.
            
            If `size` is not None, read `size` bytes (usual timeout applies); otherwise, read all available data (return immediately).
            """
            if size is None:
                result=self._read_terms(read_block_size=max_read_size,timeout=1E-3,error_on_timeout=False)
            else:
                result=self.instr.read(self.ep_read,size,timeout=self._timeout()).tobytes()
                if len(result)!=size and self.check_read_size:
                    raise self.Error("read returned less than expected {} instead of {}".format(len(result),size))
            self.cooldown("read")
            self._log("read",result)
            return self._to_datatype(result)
        @logerror
        def read_multichar_term(self, term, remove_term=True, timeout=None, error_on_timeout=True):
            """
            Read a single line with multiple possible terminators.
            
            Args:
                term: Either a string (single multi-char terminator) or a list of strings (multiple terminators).
                remove_term (bool): If ``True``, remove terminal characters from the result.
                timeout: Operation timeout. If ``None``, use the default device timeout.
                error_on_timeout (bool): If ``False``, return an incomplete line instead of raising the error on timeout.
            """
            if isinstance(term,py3.anystring):
                term=[term]
            result=self._read_terms(term,timeout=timeout,error_on_timeout=error_on_timeout)
            self.cooldown("read")
            if remove_term and term:
                result=remove_longest_term(result,term)
            self._log("read",result)
            return self._to_datatype(result)
        @logerror
        @reraise
        def write(self, data, flush=True, read_echo=False, read_echo_delay=0, read_echo_lines=1):
            """
            Write data to the device.
            
            If ``read_echo==True``, wait for `read_echo_delay` seconds and then perform :func:`readline` (`read_echo_lines` times).
            `flush` parameter is ignored.
            """
            self._log("write",data)
            data=py3.as_builtin_bytes(data)
            if self.term_write:
                data=data+py3.as_builtin_bytes(self.term_write)
            self.instr.write(self.ep_write,data,timeout=self._timeout())
            self.cooldown("write")
            if read_echo:
                if read_echo_delay>0.:
                    time.sleep(read_echo_delay)
                for _ in range(read_echo_lines):
                    self.readline()

        @reraise
        def __repr__(self):
            return "PyUSBDeviceBackend("+self.instr.__repr__()+")"

        
        @staticmethod
        def list_resources(desc=False, **kwargs):
            try:
                devs=list(usb.core.find(find_all=True,**kwargs))
            except PyUSBDeviceBackend.BackendError as e:
                raise PyUSBDeviceBackend.Error from e
            if desc:
                return devs
            indices={}
            res=[]
            for d in devs:
                vid,pid=d.idVendor,d.idProduct
                i=indices.get((vid,pid),0)
                indices[(vid,pid)]=i+1
                res.append((vid,pid,i))
            return res
        
        
    _backends["pyusb"]=PyUSBDeviceBackend
except ImportError:
    pass
_backend_errors["pyusb"]=_backend_install_message.format(name="PyUSB",pkg="pyusb",mod="usb")
    

class DeviceRecordedError(DeviceBackendError):
    """Recorded backend operation error"""

class RecordedDeviceBackend(IDeviceCommBackend):
    """
    Recorded backend.
    
    Connection is automatically opened on creation.
    
    Args:
        conn: connection parameters (recorded log path)
        datatype (str): Type of the returned data; can be ``"bytes"`` (return `bytes` object), ``"str"`` (return `str` object),
            or ``"auto"`` (default Python result: `str` in Python 2 and `bytes` in Python 3)
        reraise_error: if not ``None``, specifies an error to be re-raised on any backend exception (by default, use backend-specific error);
            should be a subclass of :exc:`DeviceBackendError`.
    """
    BackendError=IOError
    _backend="recorded"
    Error=DeviceRecordedError
    
    _conn_params=["path"]
    _default_conn=[None]

    def __init__(self, conn, datatype="auto", reraise_error=None):
        conn_dict=self.combine_conn(conn,self._default_conn)
        IDeviceCommBackend.__init__(self,conn_dict.copy(),datatype=datatype,reraise_error=reraise_error)
        self.log=None
        self.log_section=None
        self.log_pos=0
        try:
            self.open()
        except IOError as e:
            raise self.Error(e) from e
    
    @reraise
    def open(self):
        """Open the connection"""
        if self.log is None:
            self.log=dict(backend_logger.load_logfile(self.conn["path"]))
    def close(self):
        """Close the connection"""
        self.log=None
    def is_opened(self):
        return self.log is not None

    def start(self, header):
        """Start recorded section"""
        if header not in self.log:
            raise self.Error(IOError("header {} is missing from the record".format(header)))
        self.log_section=header
        self.log_pos=0
    def stop(self):
        """Stop logging section"""
        self.log_section=None
        self.log_pos=0
    @contextlib.contextmanager
    def section(self, header):
        self.start(header)
        try:
            yield
        finally:
            self.stop()

    def _get_value(self, operation):
        if self.log is None:
            raise self.Error(IOError("device is not opened"))
        if self.log_section is None:
            raise self.Error(IOError("log section is not selected"))
        section=self.log[self.log_section]
        if len(section)<=self.log_pos:
            raise self.Error(IOError("section is over"))
        op,val=section[self.log_pos]
        self.log_pos+=1
        if operation[0]!=op:
            raise self.Error(IOError("requested operation {}, recorded {}".format(operation,op)))
        return val
    def readline(self, remove_term=True, timeout=None, skip_empty=True):
        """
        Read a single line from the device.
        
        Args:
            remove_term (bool): If ``True``, remove terminal characters from the result.
            timeout: Operation timeout. If ``None``, use the default device timeout.
            skip_empty (bool): If ``True``, ignore empty lines (works only for ``remove_term==True``).
        """
        result=self._get_value("read")
        return self._to_datatype(result)
    def read(self, size=None):
        """
        Read data from the device.
        
        If `size` is not None, read `size` bytes (usual timeout applies); otherwise, read all available data (return immediately).
        """
        result=self._get_value("read")
        return self._to_datatype(result)
    def write(self, data, flush=True, read_echo=False, read_echo_delay=0, read_echo_lines=1):
        """
        Write data to the device.
        
        If ``flush==True``, flush the write buffer.
        If ``read_echo==True``, wait for `read_echo_delay` seconds and then perform :func:`readline` (`read_echo_lines` times).
        """
        value=self._get_value("write")
        if value!=data:
            raise self.Error(IOError("requested write {}, recorded {}".format(data,value)))
        return value

    def __repr__(self):
        return "RecordedDeviceBackend("+self.conn["path"]+")"

    
_backends["recorded"]=RecordedDeviceBackend




    
    
_serial_re=re.compile(r"^com\d+",re.IGNORECASE)
def _is_serial_addr(addr):
    return isinstance(addr,py3.anystring) and bool(_serial_re.match(addr))
_network_re=re.compile(r"(\d+\.){3}\d+(:\d+)?",re.IGNORECASE)
def _is_network_addr(addr):
    return isinstance(addr,py3.anystring) and bool(_network_re.match(addr))
_visa_re=re.compile(r"\w+(::\w+)+",re.IGNORECASE)
def _is_visa_addr(addr):
    return isinstance(addr,py3.anystring) and bool(_visa_re.match(addr))
def autodetect_backend(conn, default="visa"):
    """
    Try to determine the backend by the connection.

    `default` specifies the default backend which is returned if the backend is unclear.
    """
    if isinstance(conn, (tuple,list)):
        if len(conn)>=2 and isinstance(conn[0],int) and (0<=conn[0]<65536) and isinstance(conn[1],int) and (0<=conn[1]<65536): # PID / VID
            return "pyusb"
        conn=conn[0]
    elif isinstance(conn, dict):
        if "addr" in conn and _is_network_addr(conn["addr"]):
            return "network"
        if "port" in conn and _is_serial_addr(conn["port"]):
            return "serial"
        if "vendorID" in conn and "productID" in conn:
            return "pyusb"
        return default
    if _is_network_addr(conn):
        return "network"
    if _is_serial_addr(conn):
        return "serial"
    if _is_visa_addr(conn):
        return "visa"
    return default
def _as_backend(backend, conn=None):
    if backend=="auto":
        backend=autodetect_backend(conn)
    if isinstance(backend,tuple) and len(backend)==2 and backend[0]=="auto":
        backend=autodetect_backend(conn,default=backend[1])
    if isinstance(backend,type) and issubclass(backend,IDeviceCommBackend):
        return backend
    if backend in _backends:
        return _backends[backend]
    error_text=_backend_errors.get(backend,None)
    raise ValueError("could not find backend {}".format(backend)+(": "+error_text if error_text else ""))
def new_backend(conn, backend="auto", defaults=None, **kwargs):
    """
    Build new backend with the supplied parameters.
    
    Args:
        conn: Connection parameters (depend on the backend). Can be simply connection parameters (tuple or dict) for the given backend
            (e.g., ``"192.168.0.1"`` or ``("COM1",19200)``), a tuple ``(backend, conn)`` which specifies both backend and connection
            (in which case it overrides the supplied backend), or an already opened backend (in which case it is returned as is)
        backend (str): Backend type. Available backends are ``'auto'`` (try to autodetect based on the connection),
            ``'visa'``, ``'serial'``, ``'ft232'``, ``'network'``, and ``"pyusb"``. Can also be directly a backend class (more appropriate for custom backends),
            or a tuple ``('auto', backend)``, which is analogous to ``'auto'``, but it returns the specified ``backend`` if the autodetection fails;
            by default, the fallback backend is ``'visa'``, so ``'auto'`` is exactly the same as ``('auto', 'visa')``.
        defaults: if not ``None``, specifies a dictionary ``{backend: params}`` with default connection parameters (depending on the backend),
            which are added to the connection parameters
        **kwargs: parameters sent to the backend.
    """
    if isinstance(conn,IDeviceCommBackend):
        return conn
    if isinstance(conn,tuple) and conn and (conn[0] in _backends or (isinstance(conn[0],type) and issubclass(conn[0],IDeviceCommBackend))):
        return new_backend(conn[1],backend=conn[0],**kwargs)
    backend=_as_backend(backend,conn)
    backend_name=getattr(backend,"_backend",None)
    if defaults is not None and backend_name is not None and backend_name in defaults:
        conn=backend.combine_conn(conn,defaults[backend_name])
    return backend(conn,**kwargs)
def backend_error(backend, conn=None):
    """
    Return error class corresponding to the current backend.

    Like :func:`new_backend`, allows setting ``backend="auto"``, in which case `conn` is used to try and autodetect the backend kind
    (not completely reliable, should be avoided).
    """
    return _as_backend(backend,conn).Error
def list_backend_resources(backend=None, desc=False):
    """
    List all resources for the given backend.

    If `backend` is ``None``, return dictionary ``{backend: resources}`` for all available backends.
    If ``desc==False``, return list of connections (usually strings or tuples), which can be used to connect to the device.
    Otherwise, return a list of descriptions, which have more info, but can be backend-dependent.
    """
    if backend is None:
        res={n:b.list_resources(desc=desc) for (n,b) in _backends.items()}
        return {n:r for n,r in res.items() if r is not None}
    else:
        return _as_backend(backend).list_resources(desc=desc)




### Interface for a generic device class employing a communication backend ###

class ICommBackendWrapper(interface.IDevice):
    """
    A base class for an instrument using a communication backend.
    
    Args:
        instr: Backend (assumed to be already opened).
    """
    def __init__(self, instr):
        super().__init__()
        self.instr=instr
        self._connection_parameters=self.instr.conn
        
    def open(self):
        """Open the backend"""
        return self.instr.open()
    def close(self):
        """Close the backend"""
        return self.instr.close()
    def is_opened(self):
        """Check if the device is connected"""
        return bool(self.instr)
    def _get_connection_parameters(self):
        return self._connection_parameters
    
    def lock(self, timeout=None):
        """Lock the access to the device from other threads/processes (isn't necessarily implemented)"""
        return self.instr.lock(timeout=timeout)
    def unlock(self):
        """Unlock the access to the device from other threads/processes (isn't necessarily implemented)"""
        return self.instr.unlock()
    def locking(self, timeout=None):
        """Context manager for lock & unlock"""
        return self.instr.locking(timeout=timeout)