"""
Routines for defining a unified interface across multiple backends.
"""

from ..utils.py3 import anystring
from builtins import range,zip
from . import interface

import time
import re
from ..utils import funcargparse, general, log, net, py3, module
import contextlib

_depends_local=[".interface"]


### Generic backend interface ###

class IDeviceBackend(object):
    """
    An abstract class for a device communication backend.
    
    Connection is automatically opened on creation.
    
    Args:
        conn: Connection parameters (depend on the backend).
        timeout (float): Default timeout (in seconds).
        term_write (str): Line terminator for writing operations.
        term_read (str): Line terminator for reading operations.
        datatype (str): Type of the returned data; can be ``"bytes"`` (return `bytes` object), ``"str"`` (return `str` object),
            or ``"auto"`` (default Python result: `str` in Python 2 and `bytes` in Python 3)
    """
    Error=RuntimeError
    """Base class for the errors raised by the backend operations""" 
    
    def __init__(self, conn, timeout=None, term_write=None, term_read=None, datatype="auto"):
        object.__init__(self)
        funcargparse.check_parameter_range(datatype,"datatype",{"auto","str","bytes"})
        self.datatype=datatype
        self.conn=conn
        self.term_write=term_write
        self.term_read=term_read

    _conn_params=["addr"]
    _default_conn=[None]
    @classmethod
    def _conn_to_dict(cls, conn):
        if isinstance(conn, dict):
            return conn
        if isinstance(conn, (tuple,list)):
            return dict(zip(cls._conn_params,conn))
        return {cls._conn_params[0]:conn}
    @classmethod
    def combine_conn(cls, conn1, conn2):
        conn=cls._conn_to_dict(conn2).copy()
        conn.update(cls._conn_to_dict(conn1))
        return conn

    def _to_datatype(self, data):
        if self.datatype=="auto":
            return data
        if self.datatype=="str":
            return py3.as_str(data)
        return py3.as_bytes(data)
    
    def open(self):
        """Open the connection."""
        pass
    def close(self):
        """Close the connection."""
        pass
    def is_opened(self):
        """Check if the device is connected"""
        return True
    def __bool__(self):
        return self.is_opened()
    __nonzero__=__bool__ # Python 2 compatibility

    
    def lock(self, timeout=None):
        """Lock the access to the device from other threads/processes (isn't necessarily implemented)."""
        pass
    def unlock(self):
        """Unlock the access to the device from other threads/processes (isn't necessarily implemented)."""
        pass
    def locking(self, timeout=None):
        """Context manager for lock & unlock."""
        return general.DummyResource()
    
    def cooldown(self):
        """Cooldown between the operations (usually, some short time delay)."""
        pass
    
    def set_timeout(self, timeout):
        """Set operations timeout (in seconds)."""
        pass
    def get_timeout(self):
        """Get operations timeout (in seconds)."""
        return None
    
    @contextlib.contextmanager
    def using_timeout(self, timeout=None):
        """Context manager for usage of a different timeout inside a block."""
        if timeout is not None:
            to=self.get_timeout()
            self.set_timeout(timeout)
        try:
            yield
        finally:
            if timeout is not None:
                self.set_timeout(to)
    
            
        
    def readline(self, remove_term=True, timeout=None, skip_empty=True):
        """
        Read a single line from the device.
        
        Args:
            remove_term (bool): If ``True``, remove terminal characters from the result.
            timeout: Operation timeout. If ``None``, use the default device timeout.
            skip_empty (bool): If ``True``, ignore empty lines (works only for ``remove_term==True``).
        """
        raise NotImplementedError("IDeviceBackend.readline")
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
        raise NotImplementedError("IDeviceBackend.read")
    def flush_read(self):
        """Flush the device output (read all the available data; return the number of bytes read)."""
        return len(self.read())
    def write(self, data, flush=True, read_echo=False, read_echo_delay=0, read_echo_lines=1):
        """
        Write data to the device.
        
        If ``flush==True``, flush the write buffer.
        If ``read_echo==True``, wait for `read_echo_delay` seconds and then perform :func:`readline` (`read_echo_lines` times).
        """
        raise NotImplementedError("IDeviceBackend.write")
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
    def list_resources(desc=False):
        """
        List all availabe resources for this backend.

        If ``desc==False``, return list of connections (usually strings), which can be used to connect to the device.
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

class IBackendOpenError(IOError):
    pass

try:
    import visa

    class VisaBackendOpenError(IBackendOpenError,visa.VisaIOError):
        """Visa backend opening error"""
        def __init__(self, e):
            IBackendOpenError.__init__(self)
            visa.VisaIOError.__init__(self,e.error_code)

    class VisaDeviceBackend(IDeviceBackend):
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
        """
        _default_operation_cooldown=0.03
        _backend="visa"
        Error=visa.VisaIOError
        """Base class for the errors raised by the backend operations"""
        BackendOpenError=VisaBackendOpenError
        
        if module.cmp_versions(visa.__version__,"1.6")=="<": # older pyvisa versions have a slightly different interface
            def _set_timeout(self, timeout):
                self.instr.timeout=timeout
            def _get_timeout(self):
                return self.instr.timeout
            def _open_resource(self, conn):
                if not self.term_write.endswith(self.term_read):
                    raise NotImplementedError("PyVisa version <1.6 doesn't support different terminators for reading and writing")
                instr=visa.instrument(conn)
                instr.term_chars=self.term_read
                self.term_write=self.term_write[:len(self.term_write)-len(self.term_read)]
                return instr
            _lock_default=False
            def _lock(self, timeout=None):
                raise NotImplementedError("PyVisa version <1.6 doesn't support locking")
            def _unlock(self):
                raise NotImplementedError("PyVisa version <1.6 doesn't support locking")
            def _lock_context(self, timeout=None):
                raise NotImplementedError("PyVisa version <1.6 doesn't support locking")
            def _read_term(self):
                return py3.as_builtin_bytes(self.instr.term_chars)
        else:
            def _set_timeout(self, timeout):
                self.instr.timeout=timeout*1000. # in newer versions timeout is in ms
            def _get_timeout(self):
                return self.instr.timeout/1000. # in newer versions timeout is in ms
            def _open_resource(self, conn):
                instr=visa.ResourceManager().open_resource(conn)
                instr.read_termination=self.term_read
                instr.write_termination=self.term_write
                self.term_read=self.term_write=""
                return instr
            _lock_default=False ## TODO: figure out GPIB locking issue 
            def _lock(self, timeout=None):
                self.instr.lock(timeout=timeout*1000. if timeout is not None else None)
            def _unlock(self):
                self.instr.unlock()
            def _lock_context(self, timeout=None):
                return self.instr.lock_context(timeout=timeout*1000. if timeout is not None else None)
            def _read_term(self):
                return py3.as_builtin_bytes(self.instr.read_termination)
            @staticmethod
            def list_resources(desc=False):
                return visa.ResourceManager().list_resources_info() if desc else visa.ResourceManager().list_resources()
            
        
        def __init__(self, conn, timeout=10., term_write=None, term_read=None, do_lock=None, datatype="auto"):
            if term_write is None:
                term_write=b"\r\n"
            if term_read is None:
                term_read=b"\n"
            IDeviceBackend.__init__(self,conn,term_write=term_write,term_read=term_read,datatype=datatype)
            try:
                self.instr=self._open_resource(self.conn)
                self.opened=True
                self._operation_cooldown=self._default_operation_cooldown
                self._do_lock=do_lock if do_lock is not None else self._lock_default
                self.cooldown()
                self.set_timeout(timeout)
            except self.Error as e:
                raise VisaBackendOpenError(e)
            
        def open(self):
            """Open the connection."""
            self.instr.open()
            self.opened=True
            self.cooldown()
        def close(self):
            """Close the connection."""
            self.instr.close()
            self.opened=False
            self.cooldown()
        def is_opened(self):
            return self.opened

        def lock(self, timeout=None):
            """Lock the access to the device from other threads/processes."""
            if self._do_lock:
                self.lock(timeout=timeout)
        def unlock(self):
            """Unlock the access to the device from other threads/processes."""
            if self._do_lock:
                self.unlock()
        def locking(self, timeout=None):
            """Context manager for lock & unlock."""
            if self._do_lock:
                return self._lock_context(timeout=timeout)
            else:
                return general.DummyResource()
        
        def cooldown(self):
            """
            Cooldown between the operations.
            
            Sleeping for a short time defined by `_operation_cooldown` attribute (30 ms by default).
            Also can be defined class-wide by `_default_operation_cooldown` class attribute.
            """
            if self._operation_cooldown>0:
                time.sleep(self._operation_cooldown)
        
        def set_timeout(self, timeout):
            """Set operations timeout (in seconds)."""
            if timeout is not None:
                self._set_timeout(timeout)
                self.cooldown()
        def get_timeout(self):
            """Get operations timeout (in seconds)."""
            return self._get_timeout()            
        
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
            self.cooldown()
            return self._to_datatype(result)
        def read(self, size=None):
            """
            Read data from the device.
            
            If `size` is not None, read `size` bytes (the standard timeout applies); otherwise, read all available data (return immediately).
            """
            if size is None:
                with self.using_timeout(0):
                    return self.instr.read_raw(size=size)
            result=self.instr.read_raw(size=size)
            self.cooldown()
            return self._to_datatype(result)
        
        def write(self, data, flush=True, read_echo=False, read_echo_delay=0, read_echo_lines=1):
            """
            Write data to the device.
            
            If ``flush==True``, flush the write buffer.
            If ``read_echo==True``, wait for `read_echo_delay` seconds and then perform :func:`readline` (`read_echo_lines` times).
            """
            data=py3.as_builtin_bytes(data)
            if self.term_write:
                data=data+py3.as_builtin_bytes(self.term_write)
            self.instr.write_raw(data)
            self.cooldown()
            if read_echo_delay>0.:
                time.sleep(read_echo_delay)
            if read_echo:
                for _ in range(read_echo_lines):
                    self.readline()
                    self.cooldown()

        def __repr__(self):
            return "VisaDeviceBackend("+self.instr.__repr__()+")"
                
                
    _backends["visa"]=VisaDeviceBackend
except ImportError:
    pass
    


try:
    import serial
    
    try:
        import serial.tools.list_ports as serial_list_ports
    except ImportError:
        serial_list_ports=None

    class SerialBackendOpenError(IBackendOpenError,serial.SerialException):
        """Serial backend opening error"""
        def __init__(self, e):
            IBackendOpenError.__init__(self)
            serial.SerialException.__init__(self,*e.args)

    class SerialDeviceBackend(IDeviceBackend):
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
            no_dtr (bool): If ``True``, turn off DTR status line before opening (e.g., turns off reset-on-connection for Arduino controllers).
            datatype (str): Type of the returned data; can be ``"bytes"`` (return `bytes` object), ``"str"`` (return `str` object),
                or ``"auto"`` (default Python result: `str` in Python 2 and `bytes` in Python 3)
        """
        _default_operation_cooldown=0.0
        _backend="serial"
        Error=serial.SerialException
        """Base class for the errors raised by the backend operations"""
        BackendOpenError=SerialBackendOpenError
        
        _conn_params=["port","baudrate","bytesize","parity","stopbits","xonxoff","rtscts","dsrdtr"]
        _default_conn=["COM1",19200,8,"N",1,0,0,0]

        def __init__(self, conn, timeout=10., term_write=None, term_read=None, connect_on_operation=False, open_retry_times=3, no_dtr=False, datatype="auto"):
            conn_dict=self.combine_conn(conn,self._default_conn)
            if term_write is None:
                term_write=b"\r\n"
            if term_read is None:
                term_read=b"\n"
            if isinstance(term_read,anystring):
                term_read=[term_read]
            IDeviceBackend.__init__(self,conn_dict.copy(),term_write=term_write,term_read=term_read,datatype=datatype)
            port=conn_dict.pop("port")
            try:
                self.instr=serial.serial_for_url(port,do_not_open=True,**conn_dict)
                self.opened=True
                if no_dtr:
                    try:
                        self.instr.setDTR(0)
                    except self.Error:
                        log.default_log.debug("Cannot set DTR for an unconnected device",origin="backends/serial",level="misc")
                if not connect_on_operation:
                    self.instr.open()
                self._operation_cooldown=self._default_operation_cooldown
                self._connect_on_operation=connect_on_operation
                self._opened_stack=0
                self._open_retry_times=open_retry_times
                self.cooldown()
                self.set_timeout(timeout)
            except self.Error as e:
                raise SerialBackendOpenError(e)
            
        def _do_open(self):
            general.retry_wait(self.instr.open, self._open_retry_times, 0.3)
        def _do_close(self):
            #general.retry_wait(self.instr.flush, self._open_retry_times, 0.3)
            general.retry_wait(self.instr.close, self._open_retry_times, 0.3)
        def open(self):
            """Open the connection."""
            if not self._connect_on_operation and not self.opened:
                self._do_open()
            self.opened=True
        def close(self):
            """Close the connection."""
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
            
        
        def cooldown(self):
            """
            Cooldown between the operations.
            
            Sleeping for a short time defined by `_operation_cooldown` attribute (no cooldown by default).
            Also defined class-wide by `_default_operation_cooldown` class attribute.
            """
            if self._operation_cooldown>0:
                time.sleep(self._operation_cooldown)
            
        def set_timeout(self, timeout):
            """Set operations timeout (in seconds)."""
            if timeout is not None:
                self.instr.timeout=timeout
                self.cooldown()
        def get_timeout(self):
            """Get operations timeout (in seconds)."""
            return self.instr.timeout
        
        
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
        def readline(self, remove_term=True, timeout=None, skip_empty=True, error_on_timeout=True):
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
                self.cooldown()
                if remove_term and self.term_read:
                    result=remove_longest_term(result,self.term_read)
                if not (skip_empty and remove_term and (not result)):
                    break
            return self._to_datatype(result)
        def read(self, size=None, error_on_timeout=True):
            """
            Read data from the device.
            
            If `size` is not None, read `size` bytes (usual timeout applies); otherwise, read all available data (return immediately).
            """
            with self.single_op():
                if size is None:
                    result=self._read_terms(timeout=0,error_on_timeout=error_on_timeout)
                else:
                    result=self.instr.read(size=size)
                    if len(result)!=size:
                        raise self.Error("read returned less than expected: {} instead of {}".format(len(result),size))
                self.cooldown()
                return self._to_datatype(result)
        def read_multichar_term(self, term, remove_term=True, timeout=None, error_on_timeout=True):
            """
            Read a single line with multiple possible terminators.
            
            Args:
                term: Either a string (single multi-char terminator) or a list of strings (multiple terminators).
                remove_term (bool): If ``True``, remove terminal characters from the result.
                timeout: Operation timeout. If ``None``, use the default device timeout.
                error_on_timeout (bool): If ``False``, return an incomplete line instead of raising the error on timeout.
            """
            if isinstance(term,anystring):
                term=[term]
            result=self._read_terms(term,timeout=timeout,error_on_timeout=error_on_timeout)
            self.cooldown()
            if remove_term and term:
                result=remove_longest_term(result,term)
            return self._to_datatype(result)
        def write(self, data, flush=True, read_echo=False, read_echo_delay=0, read_echo_lines=1):
            """
            Write data to the device.
            
            If ``flush==True``, flush the write buffer.
            If ``read_echo==True``, wait for `read_echo_delay` seconds and then perform :func:`readline` (`read_echo_lines` times).
            """
            with self.single_op():
                data=py3.as_builtin_bytes(data)
                if self.term_write:
                    data=data+py3.as_builtin_bytes(self.term_write)
                self.instr.write(data)
                self.cooldown()
                if flush:
                    self.instr.flush()
                    self.cooldown()
                if read_echo_delay>0.:
                    time.sleep(read_echo_delay)
                if read_echo:
                    for _ in range(read_echo_lines):
                        self.readline()
                        self.cooldown()

        def __repr__(self):
            return "SerialDeviceBackend("+self.instr.__repr__()+")"

        @staticmethod
        def list_resources(desc=False):
            if serial_list_ports is not None:
                return [(p if desc else p[0]) for p in serial_list_ports.comports()]

        
    _backends["serial"]=SerialDeviceBackend
except ImportError:
    pass




try:
    import ft232

    class FT232BackendOpenError(IBackendOpenError,ft232.Ft232Exception):
        """FT232 backend opening error"""
        def __init__(self, e):
            IBackendOpenError.__init__(self)
            msgs=ft232.Ft232Exception.errors
            code=msgs.index(e.msg) if e.msg in msgs else 1
            ft232.Ft232Exception.__init__(self,code)
        def __str__(self):
            return self.msg

    class FT232DeviceBackend(IDeviceBackend):
        """
        FT232 backend (via pyft232).
        
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
            no_dtr (bool): If ``True``, turn off DTR status line before opening (e.g., turns off reset-on-connection for Arduino controllers).
            datatype (str): Type of the returned data; can be ``"bytes"`` (return `bytes` object), ``"str"`` (return `str` object),
                or ``"auto"`` (default Python result: `str` in Python 2 and `bytes` in Python 3)
        """
        _default_operation_cooldown=0.0
        _backend="ft232"
        Error=ft232.Ft232Exception
        """Base class for the errors raised by the backend operations"""
        BackendOpenError=FT232BackendOpenError
        
        _conn_params=["port","baudrate","bytesize","parity","stopbits","xonxoff","rtscts"]
        _default_conn=[None,9600,8,"N",1,0,0]

        def __init__(self, conn, timeout=10., term_write=None, term_read=None, open_retry_times=3, datatype="auto"):
            conn_dict=self.combine_conn(conn,self._default_conn)
            if term_write is None:
                term_write=b"\r\n"
            if term_read is None:
                term_read=b"\n"
            if isinstance(term_read,anystring):
                term_read=[term_read]
            IDeviceBackend.__init__(self,conn_dict.copy(),term_write=term_write,term_read=term_read,datatype=datatype)
            port=conn_dict.pop("port")
            self.opened=False
            try:
                self.instr=ft232.Ft232(port,**conn_dict)
                self.opened=True
                self._operation_cooldown=self._default_operation_cooldown
                self._open_retry_times=open_retry_times
                self.cooldown()
                self.set_timeout(timeout)
                self._conn_params=(port,conn_dict,timeout)
            except self.Error as e:
                raise FT232BackendOpenError(e)
            
        def _do_open(self):
            if self.is_opened():
                return
            def reopen():
                self.instr=ft232.Ft232(self._conn_params[0],**self._conn_params[1])
                self.set_timeout(self._conn_params[2])
                self.opened=True
            general.retry_wait(reopen, self._open_retry_times, 0.3)
        def _do_close(self):
            if self.is_opened():
                general.retry_wait(self.instr.close, self._open_retry_times, 0.3)
                self.opened=False
        def open(self):
            """Open the connection."""
            self._do_open()
        def close(self):
            """Close the connection."""
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
            
        
        def cooldown(self):
            """
            Cooldown between the operations.
            
            Sleeping for a short time defined by `_operation_cooldown` attribute (no cooldown by default).
            Also defined class-wide by `_default_operation_cooldown` class attribute.
            """
            if self._operation_cooldown>0:
                time.sleep(self._operation_cooldown)
            
        def set_timeout(self, timeout):
            """Set operations timeout (in seconds)."""
            if timeout is not None:
                if timeout<1E-3:
                    timeout=1E-3 # 0 is infinite timeout
                self.instr.timeout=timeout
                self.cooldown()
        def get_timeout(self):
            """Get operations timeout (in seconds)."""
            return self.instr.timeout
        
        
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
                                raise self.Error(4)
                            return result
                        if singlechar_terms:
                            if c in terms:
                                return result
                        else:
                            for t in terms:
                                if result.endswith(t):
                                    return result
        def readline(self, remove_term=True, timeout=None, skip_empty=True, error_on_timeout=True):
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
                self.cooldown()
                if remove_term and self.term_read:
                    result=remove_longest_term(result,self.term_read)
                if not (skip_empty and remove_term and (not result)):
                    break
            return self._to_datatype(result)
        def read(self, size=None, error_on_timeout=True):
            """
            Read data from the device.
            
            If `size` is not None, read `size` bytes (usual timeout applies); otherwise, read all available data (return immediately).
            """
            with self.single_op():
                if size is None:
                    result=self._read_terms(timeout=0,error_on_timeout=error_on_timeout)
                else:
                    result=self.instr.read(size=size)
                    if len(result)!=size:
                        raise self.Error(4)
                self.cooldown()
                return self._to_datatype(result)
        def read_multichar_term(self, term, remove_term=True, timeout=None, error_on_timeout=True):
            """
            Read a single line with multiple possible terminators.
            
            Args:
                term: Either a string (single multi-char terminator) or a list of strings (multiple terminators).
                remove_term (bool): If ``True``, remove terminal characters from the result.
                timeout: Operation timeout. If ``None``, use the default device timeout.
                error_on_timeout (bool): If ``False``, return an incomplete line instead of raising the error on timeout.
            """
            if isinstance(term,anystring):
                term=[term]
            result=self._read_terms(term,timeout=timeout,error_on_timeout=error_on_timeout)
            self.cooldown()
            if remove_term and term:
                result=remove_longest_term(result,term)
            return self._to_datatype(result)
        def write(self, data, flush=True, read_echo=False, read_echo_delay=0, read_echo_lines=1):
            """
            Write data to the device.
            
            If ``flush==True``, flush the write buffer.
            If ``read_echo==True``, wait for `read_echo_delay` seconds and then perform :func:`readline` (`read_echo_lines` times).
            """
            with self.single_op():
                data=py3.as_builtin_bytes(data)
                if self.term_write:
                    data=data+py3.as_builtin_bytes(self.term_write)
                self.instr.write(data)
                self.cooldown()
                if flush:
                    self.instr.flush()
                    self.cooldown()
                if read_echo_delay>0.:
                    time.sleep(read_echo_delay)
                if read_echo:
                    for _ in range(read_echo_lines):
                        self.readline()
                        self.cooldown()

        def __repr__(self):
            return "FT232DeviceBackend("+self.instr.__repr__()+")"

        @staticmethod
        def list_resources(desc=False):
            return [d if desc else d[0] for d in ft232.list_devices()]
        
        
    _backends["ft232"]=FT232DeviceBackend
except (ImportError,NameError,OSError):
    pass



class NetworkBackendOpenError(IBackendOpenError,net.socket.error):
    """Network backend opening error"""
    def __init__(self, e):
        IBackendOpenError.__init__(self)
        net.socket.error.__init__(self,*e.args)

class NetworkDeviceBackend(IDeviceBackend):
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
        
    Note:
        If `term_read` is a string, its behavior is different from the VISA backend:
        instead of being a multi-char terminator it is assumed to be a set of single-char terminators.
        If multi-char terminator is required, `term_read` should be a single-element list instead of a string.
    """
    _default_operation_cooldown=0.0
    _backend="network"
    Error=net.socket.error
    """Base class for the errors raised by the backend operations"""
    BackendOpenError=NetworkBackendOpenError

    def __init__(self, conn, timeout=10., term_write=None, term_read=None, datatype="auto"):
        if term_write is None:
            term_write="\r\n"
        if term_read is None:
            term_read="\r\n"
        if isinstance(term_read,anystring):
            term_read=[term_read]
        conn=self._conn_to_dict(conn)
        self._split_addr(conn)
        IDeviceBackend.__init__(self,conn,term_write=term_write,term_read=term_read,datatype=datatype)
        try:
            self.socket=None
            self.open()
            self._operation_cooldown=self._default_operation_cooldown
            self.cooldown()
            self.set_timeout(timeout)
        except self.Error as e:
            raise NetworkBackendOpenError(e)
    
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
    def open(self):
        """Open the connection."""
        self.close()
        self.socket=net.ClientSocket(send_method="fixedlen",recv_method="fixedlen")
        self.socket.connect(self.conn["addr"],self.conn["port"])
    def close(self):
        """Close the connection."""
        if self.socket is not None:
            self.socket.close()
            self.socket=None
    def is_opened(self):
        return bool(self.socket)
        
    def cooldown(self):
        """
        Cooldown between the operations.
        
        Sleeping for a short time defined by `_operation_cooldown` attribute (no cooldown by default).
        Also defined class-wide by `_default_operation_cooldown` class attribute.
        """
        if self._operation_cooldown>0:
            time.sleep(self._operation_cooldown)
        
    def set_timeout(self, timeout):
        """Set operations timeout (in seconds)."""
        self.socket.set_timeout(timeout)
    def get_timeout(self):
        """Get operations timeout (in seconds)."""
        return self.socket.get_timeout()
    
    
    def readline(self, remove_term=True, timeout=None, skip_empty=True, error_on_timeout=True):
        """
        Read a single line from the device.
        
        Args:
            remove_term (bool): If ``True``, remove terminal characters from the result.
            timeout: Operation timeout. If ``None``, use the default device timeout.
            skip_empty (bool): If ``True``, ignore empty lines (works only for ``remove_term==True``).
            error_on_timeout (bool): If ``False``, return an incomplete line instead of raising the error on timeout.
        """
        while True:
            try:
                with self.using_timeout(timeout):
                    result=self.socket.recv_delimiter(self.term_read,strict=True)
            except net.SocketTimeout:
                if error_on_timeout:
                    raise
            self.cooldown()
            if remove_term and self.term_read:
                result=remove_longest_term(result,self.term_read)
            if not (skip_empty and remove_term and (not result)):
                break
        return self._to_datatype(result)
    def read(self, size=None, error_on_timeout=True):
        """
        Read data from the device.
        
        If `size` is not None, read `size` bytes (usual timeout applies); otherwise, read all available data (return immediately).
        """
        if size is None:
            return self.socket.recv_all()
        else:
            try:
                data=self.socket.recv_fixedlen(size)
            except net.SocketTimeout:
                if error_on_timeout:
                    raise
        return self._to_datatype(data)
    def read_multichar_term(self, term, remove_term=True, timeout=None, error_on_timeout=True):
        """
        Read a single line with multiple possible terminators.
        
        Args:
            term: Either a string (single multi-char terminator) or a list of strings (multiple terminators).
            remove_term (bool): If ``True``, remove terminal characters from the result.
            timeout: Operation timeout. If ``None``, use the default device timeout.
            error_on_timeout (bool): If ``False``, return an incomplete line instead of raising the error on timeout.
        """
        if isinstance(term,anystring):
                term=[term]
        result=self.socket.recv_delimiter(term,strict=True)
        self.cooldown()
        if remove_term and term:
            result=remove_longest_term(result,term)
        return self._to_datatype(result)
    def write(self, data, flush=True, read_echo=False, read_echo_delay=0, read_echo_lines=1):
        """
        Write data to the device.
        
        If ``read_echo==True``, wait for `read_echo_delay` seconds and then perform :func:`readline` (`read_echo_lines` times).
        `flush` parameter is ignored.
        """
        self.socket.send_delimiter(data,self.term_write)
        self.cooldown()
        if read_echo_delay>0.:
            time.sleep(read_echo_delay)
        if read_echo:
            for _ in range(read_echo_lines):
                self.readline()
                self.cooldown()

    def __repr__(self):
        return "NetworkDeviceBackend("+self.socket.__repr__()+")"
    
    
_backends["network"]=NetworkDeviceBackend




try:
    import usb
    import usb.backend.libusb0
    import usb.backend.libusb1
    import usb.backend.openusb

    class PyUSBBackendOpenError(IBackendOpenError,usb.USBError):
        """USB backend opening error"""
        def __init__(self, e):
            IBackendOpenError.__init__(self)
            usb.USBError.__init__(self,*e.args)

    class PyUSBDeviceBackend(IDeviceBackend):
        """
        USB backend (via PyUSB package).
        
        Connection is automatically opened on creation.
        
        Args:
            conn: Connection parameters. Can be either a string (for a port),
                or a list/tuple ``(vendorID, productID, index, endpoint_read, endpoint_write, backend)`` supplied to the connection
                (default is ``(0x0000,0x0000,0,0x00,0x00,'libusb0')``, which is invalid for most devices),
                or a dict with the same parameters. 
            timeout (float): Default timeout (in seconds).
            term_write (str): Line terminator for writing operations; appended to the data
            term_read (str): List of possible single-char terminator for reading operations (specifies when :func:`readline` stops).
            datatype (str): Type of the returned data; can be ``"bytes"`` (return `bytes` object), ``"str"`` (return `str` object),
                or ``"auto"`` (default Python result: `str` in Python 2 and `bytes` in Python 3)
        """
        _default_operation_cooldown=0.0
        _backend="pyusb"
        Error=usb.USBError
        """Base class for the errors raised by the backend operations"""
        BackendOpenError=PyUSBBackendOpenError
        
        _conn_params=["vendorID","productID","index","endpoint_read","endpoint_write","backend"]
        _default_conn=[0x0000,0x0000,0,0x00,0x01,"libusb1"]
        _usb_backends={"libusb0":usb.backend.libusb0, "libusb1":usb.backend.libusb1, "openusb":usb.backend.openusb}

        def __init__(self, conn, timeout=10., term_write=None, term_read=None, check_read_size=True, datatype="auto"):
            conn_dict=self.combine_conn(conn,self._default_conn)
            funcargparse.check_parameter_range(conn_dict["backend"],"usb_backend",self._usb_backends)
            if isinstance(term_read,anystring):
                term_read=[term_read]
            self._operation_cooldown=self._default_operation_cooldown
            IDeviceBackend.__init__(self,conn_dict.copy(),term_write=term_write,term_read=term_read,datatype=datatype)
            self.timeout=timeout
            self.check_read_size=check_read_size
            try:
                self.open()
            except self.Error as e:
                raise PyUSBBackendOpenError(e)
            
        def open(self):
            """Open the connection."""
            idx=self.conn["index"]
            backend=self._usb_backends[self.conn["backend"]].get_backend()
            all_devs=list(usb.core.find(idVendor=self.conn["vendorID"],idProduct=self.conn["productID"],backend=backend,find_all=True))
            if len(all_devs)<idx+1:
                raise PyUSBBackendOpenError("can't find device with index {}; {} devices found".format(idx,len(all_devs)))
            self.instr=all_devs[idx]
            self.ep_read=self.conn["endpoint_read"]
            self.ep_write=self.conn["endpoint_write"]
            self.cooldown()
            self.opened=True
        def close(self):
            """Close the connection."""
            self.instr.finalize()
            self.opened=False
        def is_opened(self):
            return self.opened
            
        
        def cooldown(self):
            """
            Cooldown between the operations.
            
            Sleeping for a short time defined by `_operation_cooldown` attribute (no cooldown by default).
            Also defined class-wide by `_default_operation_cooldown` class attribute.
            """
            if self._operation_cooldown>0:
                time.sleep(self._operation_cooldown)
            
        def set_timeout(self, timeout):
            """Set operations timeout (in seconds)."""
            if timeout is not None:
                self.timeout=timeout
        def get_timeout(self):
            """Get operations timeout (in seconds)."""
            return self.timeout
        def _timeout(self):
            return None if self.timeout is None else int(self.timeout*1000)
        
        
        def _read_terms(self, terms=(), read_block_size=65536, timeout=None, error_on_timeout=True):
            result=b""
            singlechar_terms=all(len(t)==1 for t in terms)
            terms=[py3.as_builtin_bytes(t) for t in terms]
            while True:
                c=self.instr.read(self.ep_read,1 if terms else read_block_size,timeout=self._timeout()).tobytes()
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
        def readline(self, remove_term=True, timeout=None, skip_empty=True, error_on_timeout=True):
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
                self.cooldown()
                if remove_term and self.term_read:
                    result=remove_longest_term(result,self.term_read)
                if not (skip_empty and remove_term and (not result)):
                    break
            return self._to_datatype(result)
        def read(self, size=None, max_read_size=65536, error_on_timeout=True):
            """
            Read data from the device.
            
            If `size` is not None, read `size` bytes (usual timeout applies); otherwise, read all available data (return immediately).
            """
            if size is None:
                result=self._read_terms(read_block_size=max_read_size,timeout=0,error_on_timeout=error_on_timeout)
            else:
                result=self.instr.read(self.ep_read,size,timeout=self._timeout()).tobytes()
                if len(result)!=size and self.check_read_size:
                    raise self.Error("read returned less than expected {} instead of {}".format(len(result),size))
            self.cooldown()
            return self._to_datatype(result)
        def read_multichar_term(self, term, remove_term=True, timeout=None, error_on_timeout=True):
            """
            Read a single line with multiple possible terminators.
            
            Args:
                term: Either a string (single multi-char terminator) or a list of strings (multiple terminators).
                remove_term (bool): If ``True``, remove terminal characters from the result.
                timeout: Operation timeout. If ``None``, use the default device timeout.
                error_on_timeout (bool): If ``False``, return an incomplete line instead of raising the error on timeout.
            """
            if isinstance(term,anystring):
                term=[term]
            result=self._read_terms(term,timeout=timeout,error_on_timeout=error_on_timeout)
            self.cooldown()
            if remove_term and term:
                result=remove_longest_term(result,term)
            return self._to_datatype(result)
        def write(self, data, read_echo=False, read_echo_delay=0, read_echo_lines=1):
            """
            Write data to the device.
            
            If ``read_echo==True``, wait for `read_echo_delay` seconds and then perform :func:`readline` (`read_echo_lines` times).
            """
            data=py3.as_builtin_bytes(data)
            if self.term_write:
                data=data+py3.as_builtin_bytes(self.term_write)
            self.instr.write(self.ep_write,data,timeout=self._timeout())
            self.cooldown()
            if read_echo:
                if read_echo_delay>0.:
                    time.sleep(read_echo_delay)
                for _ in range(read_echo_lines):
                    self.readline()
                    self.cooldown()

        def __repr__(self):
            return "PyUSBDeviceBackend("+self.instr.__repr__()+")"
        
        
    _backends["pyusb"]=PyUSBDeviceBackend
except ImportError:
    pass
    

    
    
_serial_re=re.compile(r"^com\d+",re.IGNORECASE)
def _is_serial_addr(addr):
    return isinstance(addr,anystring) and bool(_serial_re.match(addr))
_network_re=re.compile(r"(\d+\.){3}\d+(:\d+)?",re.IGNORECASE)
def _is_network_addr(addr):
    return isinstance(addr,anystring) and bool(_network_re.match(addr))
def autodetect_backend(conn):
    """
    Try to determine the backend by the connection.

    The assumed default backend is ``'visa'``.
    """
    if isinstance(conn, (tuple,list)):
        conn=conn[0]
    elif isinstance(conn, dict):
        if "addr" in conn and _is_network_addr(conn["addr"]):
            return "network"
        if "port" in conn and _is_serial_addr(conn["port"]):
            return "serial"
        return "visa"
    if _is_network_addr(conn):
        return "network"
    if _is_serial_addr(conn):
        return "serial"
    return "visa"
def new_backend(conn, timeout=None, backend="auto", **kwargs):
    """
    Build new backend with the supplied parameters.
    
    Args:
        conn: Connection parameters (depend on the backend).
        timeout (float): Default timeout (in seconds).
        backend (str): Backend type. Available backends are ``'auto'`` (try to autodetect), ``'visa'``, ``'serial'``, ``'ft232'``, and ``'network'``.
        **kwargs: parameters sent to the backend.
    """
    if isinstance(conn,IDeviceBackend):
        return conn
    if backend=="auto":
        backend=autodetect_backend(conn)
    funcargparse.check_parameter_range(backend,"backend",_backends)
    return _backends[backend](conn,timeout=timeout,**kwargs)






### Interface for a generic device class ###

class IBackendWrapper(interface.IDevice):
    """
    A base class for an instrument using a communication backend.
    
    Args:
        instr: Backend (assumed to be already opened).
    """
    def __init__(self, instr):
        interface.IDevice.__init__(self)
        self.instr=instr
        
    def open(self):
        """Open the backend."""
        return self.instr.open()
    def close(self):
        """Close the backend."""
        return self.instr.close()
    def is_opened(self):
        """Check if the device is connected"""
        return bool(self.instr)
    
    def lock(self, timeout=None):
        """Lock the access to the device from other threads/processes (isn't necessarily implemented)."""
        return self.instr.lock(timeout=timeout)
    def unlock(self):
        """Unlock the access to the device from other threads/processes (isn't necessarily implemented)."""
        return self.instr.unlock()
    def locking(self, timeout=None):
        """Context manager for lock & unlock."""
        return self.instr.locking(timeout=timeout)