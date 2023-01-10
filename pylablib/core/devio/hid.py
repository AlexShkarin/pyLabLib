from .hid_base import HIDError, HIDLibError, HIDTimeoutError
from .hid_lib import wlib as lib
from ..utils import py3, funcargparse

import ctypes
import collections
import contextlib
import threading
import time





TDeviceDescription=collections.namedtuple("TDeviceDescription",["path","manufacturer","product","serial","vendor_id","product_id","version"])
def _get_device_description(path):
    f=lib.CreateFileW(path,0xC0000000,0x03,None,3,0,None)
    try:
        try:
            manufacturer=lib.HidD_GetManufacturerString(f)
        except HIDError:
            manufacturer=None
        try:
            product=lib.HidD_GetProductString(f)
        except HIDError:
            product=None
        try:
            serial=lib.HidD_GetSerialNumberString(f)
        except HIDError:
            serial=None
        try:
            attrs=lib.HidD_GetAttributes(f)
            vid=attrs.VendorID
            pid=attrs.ProductID
            ver=attrs.VersionNumber
        except HIDError:
            vid,pid,ver=None,None,None
        return TDeviceDescription(path,manufacturer,product,serial,vid,pid,ver)
    finally:
        lib.CloseHandle(f)
def list_devices():
    """
    List HID devices.

    Return list of tuples ``(path, manufacturer, product, serial, vendor_id, product_id, version)``, where ``path`` is the string path used for connection.
    """
    lib.initlib()
    paths=lib.list_hid_devices()
    return [_get_device_description(p) for p in paths]









class HIDevice:
    """
    Generic HID-based device interface.

    Args:
        path: HID path (usually obtained using :func:`.hid.list_devices`)
        timeout: communication timeout
        rep_fmt: HID report format; can be ``"raw"`` (read/write raw data from/to HID),
            ``"lenpfx"`` (assume a format where the first byte for the report indicates the payload size),
            or a tuple ``(parser, builder)`` of two functions, where the ``parser`` takes a single raw report data argument and returns a parsed value,
            while ``builder`` takes 2 arguments (data to be written and the output report size) and return the bytes to be sent to HID.
    """
    def __init__(self, path, timeout=3., rep_fmt="lenpfx"):
        if isinstance(rep_fmt,tuple):
            if len(rep_fmt)!=2:
                raise ValueError("report format should be a 2-tuple (parser, builder), got {} instead".format(rep_fmt))
        else:
            funcargparse.check_parameter_range(rep_fmt,"rep_fmt",["raw","lenpfx"])
        lib.initlib()
        self.path=path
        self._file=None
        self._readbuffsize=2**20
        self._rep_fmt=rep_fmt
        self.timeout=timeout
        self.open()
    
    def open(self):
        """Open the device connection if it is not opened yet"""
        if self.is_opened():
            return
        access=0x80000000|0x40000000  # GENERIC_READ | GENERIC_WRITE
        share_mode=0x01|0x02  # FILE_SHARE_READ | FILE_SHARE_WRITE
        disposition=3  # OPEN_EXISTING
        self._file=lib.CreateFileW(self.path,access,share_mode,None,disposition,0,None)
        try:
            ppd=lib.HidD_GetPreparsedData(self._file)
            try:
                self._caps=lib.HidP_GetCaps(ppd)
            finally:
                lib.HidD_FreePreparsedData(ppd)
            self._setup_device()
            self._reader=self.Reader(self._file,self._caps,self._readbuffsize,self._make_parser())
            self._reader.start_loop()
        except HIDError:
            self.close()
            raise
    def _make_parser(self):
        if self._rep_fmt=="raw":
            return lambda m: m
        if self._rep_fmt=="lenpfx":
            def parse(m):
                l=min(m[0],len(m)-1)
                return m[1:l+1]
            return parse
        return self._rep_fmt[0]
    def _build_msg(self, data, msglen):
        if self._rep_fmt=="raw":
            return data
        if self._rep_fmt=="lenpfx":
            if msglen is not None and len(data)>=msglen:
                raise HIDError("required data size {} is larger than the maximal packet size {}".format(len(data)+1,msglen))
            return bytes([len(data)])+data+b"\x00"*(msglen-len(data)-1)
        return self._rep_fmt[1](data,msglen)
    def _setup_device(self):
        ninp=lib.HidD_GetNumInputBuffers(self._file)
        while ninp<2**28:
            try:
                ninp*=2
                lib.HidD_SetNumInputBuffers(self._file,ninp)
            except HIDLibError as err:
                if err.code==0x57:  # ERROR_INVALID_PARAMETER
                    break
                raise
    def close(self):
        """Close the device connection"""
        if self._file is None:
            return
        self._reader.stop_loop()
        self._reader=None
        lib.CloseHandle(self._file)
        self._file=None
    def is_opened(self):
        """Check if the device connection is opened"""
        return self._file is not None
    def _check_open(self):
        if self._file is None:
            raise HIDError("can not perform operation on the closed device")
    def __repr__(self):
        return "{}('{}')".format(type(self).__name__,self.path)
    
    def get_description(self):
        """
        Get device description
        
        Return tuple ``(path, manufacturer, product, serial, vendor_id, product_id, version)``, where ``path`` is the string path used for connection.
        """
        return _get_device_description(self.path)
    def get_timeout(self):
        """Get device communication timeout"""
        return self.timeout
    def set_timeout(self, timeout):
        """Set device communication timeout"""
        self.timeout=timeout
    
    class Reader:
        def __init__(self, f, caps, buffsize, parser):
            self.f=f
            self.msglen=caps.InputReportByteLength
            self.nreadbuff=lib.HidD_GetNumInputBuffers(self.f)
            self.readbuffsize=self.msglen*self.nreadbuff
            self.readbuff=ctypes.create_string_buffer(self.readbuffsize)
            self.storebuffsize=buffsize
            self.storebuff=bytearray(self.storebuffsize)
            self.nread=0
            self.npassed=0
            self.parser=parser
            self._looping=False
            self._thread=None
            self._data_wait_size=None
            self._data_ready=threading.Event()
            self._executing=threading.Event()
            self._read_lock=threading.Lock()
        def loop_read(self):
            while self._looping:
                self._executing.wait()
                with self._read_lock:
                    chread=lib.ReadFile(self.f,self.readbuff,self.readbuffsize,None)
                    if not chread:
                        time.sleep(1E-3)
                        continue
                    data=self.parser(self.readbuff.raw[:chread])
                    start=self.nread%self.storebuffsize
                    end=(self.nread+len(data))%self.storebuffsize
                    if end>start:
                        self.storebuff[start:end]=data
                    else:
                        self.storebuff[start:]=data[:self.storebuffsize-start]
                        self.storebuff[:end]=data[self.storebuffsize-start:]
                    self.nread+=len(data)
                    self.npassed=max(self.npassed,self.nread-self.storebuffsize)
                    if self._data_wait_size is not None and self.nread>=self._data_wait_size:
                        self._data_ready.set()
        def start_loop(self):
            """Start the read loop"""
            self.stop_loop()
            self._thread=threading.Thread(target=self.loop_read,daemon=True)
            self._looping=True
            self._executing.set()
            self.nread=0
            self.npassed=0
            self._thread.start()
        def stop_loop(self):
            """Stop the read loop"""
            if self._thread is not None:
                self._looping=False
                self._executing.set()
                self._thread.join()
                self._thread=None
        def pause(self, pause=True):
            """Pause or resume the read loop"""
            if pause:
                self._executing.clear()
                self._read_lock.acquire()
                self._read_lock.release()
            else:
                self._executing.set()
        @contextlib.contextmanager
        def pausing(self, do_pause=True):
            if not do_pause:
                yield
                return
            paused=not self._executing.is_set()
            self._executing.clear()
            try:
                with self._read_lock:
                    yield
            finally:
                if not paused:
                    self._executing.set()
        def _wait_for_nread(self, nread, timeout=None):
            if self.nread>=nread:
                return
            self._data_ready.clear()
            self._data_wait_size=nread
            try:
                self._data_ready.wait(timeout=timeout)
            except TimeoutError:
                raise HIDTimeoutError("timeout while read")
            finally:
                self._data_wait_size=None
        def read(self, nbytes=None, timeout=None, peek=False):
            """
            Read the given number of bytes from the read buffer.
            
            If `nbytes` is ``None``, return all read bytes.
            If `timeout` is not ``None``, it can define the read operation timeout; otherwise, use the default timeout specified on creation.
            If ``peek==True``, return the bytes but keep them in the buffer.
            """
            if nbytes is None:
                nbytes=self.nread-self.npassed
            else:
                self._wait_for_nread(self.npassed+nbytes,timeout=timeout)
            if not nbytes:
                return b""
            start=self.npassed%self.storebuffsize
            end=(self.npassed+nbytes)%self.storebuffsize
            if end>start:
                result=bytes(self.storebuff[start:end])
            else:
                result=bytes(self.storebuff[end:]+self.storebuff[:start])
            if not peek:
                self.npassed+=nbytes
            return result
        def get_pending(self):
            """Get the number of bytes in the read buffer"""
            return self.nread-self.npassed

    def get_pending(self):
        """Get the number of bytes in the read buffer"""
        self._check_open()
        return self._reader.get_pending()
    def read(self, nbytes=None, timeout=None):
        """
        Read the given number of bytes from the read buffer.
        
        If `nbytes` is ``None``, return all read bytes.
        If `timeout` is not ``None``, it can define the read operation timeout; otherwise, use the default timeout specified on creation.
        """
        self._check_open()
        if timeout is None:
            timeout=self.timeout
        return self._reader.read(nbytes=nbytes,timeout=timeout)
    def write(self, data):
        """Write the given data to the device"""
        self._check_open()
        if isinstance(data,py3.textstring):
            data=py3.as_bytes(data)
        if not isinstance(data,(bytes,bytearray)):
            data=bytes(data)
        data=self._build_msg(data,self._caps.OutputReportByteLength)
        with self._reader.pausing():
            nwrite=lib.WriteFile(self._file,data,len(data),None)
        return nwrite



class VCHIDevice(HIDevice):
    def read_msg(self):
        hdr=self.read(2)
        disc=b""
        for _ in range(100):
            if hdr==b"\xab\xcd":
                break
            disc+=hdr[:1]
            hdr=hdr[1:]+self.read(1)
        if disc and disc!=b"\x0d\x0a":
            print("discarded",list(disc))
        if hdr!=b"\xab\xcd":
            raise HIDError("could not find the header")
        l=self.read(1)[0]
        new_msg=self.get_pending()<=l
        return (hdr+bytes([l])+self.read(l),new_msg)
    def exhaust_msg(self, nmax=100):
        msgs=[]
        for _ in range(nmax):
            m,nm=self.read_msg()
            msgs.append(m)
            if nm:
                break
        return msgs
