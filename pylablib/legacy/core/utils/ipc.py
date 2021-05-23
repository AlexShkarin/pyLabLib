"""
Universal interface for inter-process communication.

Focus on higher throughput for large numpy arrays via shared memory.
"""

from multiprocessing import Array, Pipe
import ctypes
import collections
import pickle
import numpy as np
from . import strpack


class IIPCChannel(object):
    """
    Generic IPC channel interface
    """
    def send(self, data):
        """Send data"""
        pass
    def recv(self, timeout=None):
        """Receive data"""
        pass
    
    def send_numpy(self, data):
        """Send numpy array"""
        return self.send(data)
    def recv_numpy(self, timeout=None):
        """Receive numpy array"""
        return self.recv(timeout=timeout)

    def get_peer_args(self):
        """Get arguments required to create a peer connection"""
        return ()
    @classmethod
    def from_args(cls, *args):
        """Create a peer connection from teh supplied arguments"""
        return cls(*args)


TPipeMsg=collections.namedtuple("TPipeMsg",["id","data"])
_simple_msg=0
_ack_msg=1
_sharedmem_start=16
_sharedmem_recvd=18
class PipeIPCChannel(IIPCChannel):
    """
    Generic IPC channel interface using pipe.
    """
    def __init__(self, pipe_conn=None):
        IIPCChannel.__init__(self)
        self.conn,self.peer_conn=pipe_conn or Pipe()
    
    def get_peer_args(self):
        """Get arguments required to create a peer connection"""
        return ((self.peer_conn,self.conn),)
    
    def _recv_with_timeout(self, timeout):
        if (timeout is None) or self.conn.poll(timeout):
            return self.conn.recv()
        else:
            raise TimeoutError
    def send(self, data):
        """Send data"""
        self.conn.send(data)
    def recv(self, timeout=None):
        """Receive data"""
        return self._recv_with_timeout(timeout)


class SharedMemIPCChannel(PipeIPCChannel):
    """
    Generic IPC channel interface using pipe and shared memory for large arrays.
    """
    _default_array_size=2**24
    def __init__(self, pipe_conn=None, arr=None, arr_size=None):
        PipeIPCChannel.__init__(self,pipe_conn)
        if arr is None:
            self.arr_size=arr_size or self._default_array_size
            self.arr=Array("c",self.arr_size)
        else:
            self.arr=arr
            self.arr_size=len(arr)
    
    def get_peer_args(self):
        """Get arguments required to create a peer connection"""
        return ((self.peer_conn,self.conn),self.arr,self.arr_size)
    
    def _check_strides(self, array):
        """Check if array is stored in memory continuously"""
        esize=array.dtype.itemsize
        for s,st in zip(array.shape[::-1],array.strides[::-1]):
            if st!=esize:
                return False
            esize*=s
        return True
    def send_numpy(self, data, method="auto", timeout=None):
        """Send numpy array"""
        if method=="auto":
            method="pipe" if data.nbytes<2**16 else "shm"
        if method=="pipe":
            return PipeIPCChannel.send_numpy(self,data)
        if not self._check_strides(data): # need continuous array to send
            data=data.copy()
        buff_ptr,count=data.ctypes.get_data(),data.nbytes
        self.conn.send(TPipeMsg(_sharedmem_start,(count,data.dtype.str,data.shape)))
        while count>0:
            chunk_size=min(count,self.arr_size)
            ctypes.memmove(ctypes.addressof(self.arr.get_obj()),buff_ptr,chunk_size)
            count-=chunk_size
            buff_ptr+=chunk_size
            self.conn.send(chunk_size)
            self._recv_with_timeout(timeout)
    def recv_numpy(self, timeout=None):
        """Receive numpy array"""
        msg=self._recv_with_timeout(timeout)
        if not isinstance(msg,TPipeMsg):
            return msg
        if msg.id==_simple_msg:
            return msg.data
        else:
            count,dtype,shape=msg.data
            data=np.empty(shape,dtype=dtype)
            buff_ptr=data.ctypes.get_data()
            while count>0:
                chunk_size=self._recv_with_timeout(timeout)
                ctypes.memmove(buff_ptr,ctypes.addressof(self.arr.get_obj()),chunk_size)
                buff_ptr+=chunk_size
                count-=chunk_size
                self.conn.send(TPipeMsg(_sharedmem_recvd,None))
            return data





TShmemVarDesc=collections.namedtuple("TShmemVarDesc",["offset","size","kind","fixed_size"])
class SharedMemIPCTable(object):
    """
    Shared memory table for exchanging shared variables between processes.

    Can be used instead of channels for variables which are rarely changed but frequently checked (e.g., status),
    or when synchronization of sending and receiving might be difficult
    """
    _default_array_size=2**24
    def __init__(self, pipe_conn=None, arr=None, arr_size=None, lock=True):
        object.__init__(self)
        self.pipe=PipeIPCChannel(pipe_conn)
        if arr is None:
            self.arr_size=arr_size+4 or self._default_array_size
            self.arr=Array("c",self.arr_size,lock=lock)
        else:
            self.arr=arr
            self.arr_size=len(arr)
        self.conn_side=0 if pipe_conn is None else 1
        self.var_table={}
        self.max_offset=4
        self._check_variables()
        self.arr[self.conn_side*2]=1

    def _check_variables(self):
        while True:
            try:
                name,desc=self.pipe.recv(timeout=0.)
                if name in self.var_table:
                    if self.var_table[name]!=desc:
                        raise RuntimeError("received variable {} is already defined".format(name))
                self.var_table[name]=desc
                self.max_offset=max(self.max_offset,desc.offset)
            except TimeoutError:
                return
    def _send_variable(self, name):
        self.pipe.send((name,self.var_table[name]))
    def add_variable(self, name, size, kind="pickle"):
        """
        Add a variable with a given name.

        The variable info is also communicated to the other endpoint.
        `size` determines maximal variable size in bytes. If the actual size ever exceeds it, an exception will be raised.
        `kind` determines the way to convert variable into bytes; can be ``"pickle"`` (universal, but large size overhead),
        ``"nps_###"``` (where ``###`` can be any numpy scalar dtype description, e.g., ``"float"`` or ``"<u2"``) for numpy scalars,
        or ``"npa_###"``` (where ``###`` means the same as for ``nps``) for numpy arrays (in this case the array size and shape need to be communicated separately).
        """
        self._check_variables()
        if name in self.var_table:
            raise RuntimeError("variable {} is already defined".format(name))
        fixed_size=kind.startswith("nps_")
        if not fixed_size:
            size+=8
        if self.max_offset+size>self.arr_size:
            raise RuntimeError("variable {} can't fit into the array (need {} bytes, available {})".format(name,self.max_offset+size,self.arr_size))
        self.var_table[name]=TShmemVarDesc(self.max_offset,size,kind,fixed_size)
        self.max_offset+=size
        self._send_variable(name)
    
    def set_variable(self, name, value):
        """
        Set a variable with a given name.
        
        If the variable is missing, raise an exception.
        """
        if name not in self.var_table:
            self._check_variables()
        desc=self.var_table[name]
        kind=desc.kind
        if kind=="pickle":
            sval=pickle.dumps(value)
        elif kind.startswith("nps_") or kind.startswith("npa_"):
            sval=np.asarray(value,kind[4:]).tostring()
        vlen=len(sval)
        if desc.fixed_size:
            if vlen!=desc.size:
                raise RuntimeError("unexpected variable size {} (expected {})".format(vlen,desc.size))
            self.arr[desc.offset:desc.offset+vlen]=sval
        else:
            if vlen>desc.size-8:
                raise RuntimeError("size of packed variable {} exceeds maximal specified size {}".format(vlen,desc.size-8))
            self.arr[desc.offset:desc.offset+8]=strpack.int2bytes(vlen,8,">")
            self.arr[desc.offset+8:desc.offset+8+vlen]=sval
    __setitem__=set_variable
    def get_variable(self, name, default=None):
        """
        Get a variable with a given name.
        
        If the variable is missing, return `default`.
        """
        if name not in self.var_table:
            self._check_variables()
        if name not in self.var_table:
            return default
        desc=self.var_table[name]
        if desc.fixed_size:
            sval=self.arr[desc.offset:desc.offset+desc.size]
        else:
            vlen=strpack.bytes2int(self.arr[desc.offset:desc.offset+8],">")
            if vlen==0:
                return default
            sval=self.arr[desc.offset+8:desc.offset+8+vlen]
        kind=desc.kind
        if kind=="pickle":
            return pickle.loads(sval)
        elif kind.startswith("nps_"):
            return np.fromstring(sval,dtype=kind[4:])[0]
        elif kind.startswith("npa_"):
            return np.fromstring(sval,dtype=kind[4:])
        return default
    __getitem__=get_variable

    def is_peer_connected(self):
        """Check if the peer is connected (i.e., the other side of the pipe is initialized)"""
        return self.arr[(1-self.conn_side)*2]==b"\x01"
    def close_connection(self):
        """Mark the connection as closed"""
        self.arr[self.conn_side*2+1]=1
    def is_peer_closed(self):
        """Check if the peer is closed"""
        return self.arr[(1-self.conn_side)*2+1]==b"\x01"

    def get_peer_args(self):
        """Get arguments required to create a peer connection"""
        return (self.pipe.get_peer_args()[0],self.arr)
    @classmethod
    def from_args(cls, *args):
        """Create a peer connection from teh supplied arguments"""
        return cls(*args)