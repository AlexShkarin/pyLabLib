"""Routines and classes related to RPyC package"""

from . import module as module_utils, net, library_parameters
library_parameters.library_parameters.update({"remote/rpyc/default_connect_config":{}},overwrite=False)

try:
    import rpyc
except ImportError as err:
    msg=(   "operation requires Python RPyC library. You can install it via PyPi as 'pip install rpyc'. "
            "If it is installed, check if it imports correctly by running 'import rpyc'")
    raise ImportError(msg) from err
import numpy as np

import importlib
import struct
import pickle
import warnings
import socket


_default_packers={"numpy":np.ndarray.tostring,"pickle":pickle.dumps}
_default_unpackers={"pickle":pickle.loads}
def _is_tunnel_service(serv):
    return hasattr(serv,"tunnel_socket")
def _obtain_single(proxy, serv):
    if _is_tunnel_service(serv):
        loc_serv=serv.peer
        async_send=rpyc.async_(serv.tunnel_send)
        async_send(proxy,packer="pickle")
        data=pickle.loads(loc_serv.tunnel_recv())
        return data
    else:
        return rpyc.classic.obtain(proxy)


_numpy_block_size=int(2**20)
def obtain(proxy, serv=None, deep=False, direct=False):
    """
    Obtain a remote netref object by value (i.e., copy it to the local Python instance).

    Wrapper around :func:`rpyc.utils.classic.obtain` with some special cases handling.
    `serv` specifies the current remote service. If it is of type :class:`SocketTunnelService`, use its socket tunnel for faster transfer.
    If ``deep==True`` and ``proxy`` is a container (tuple, list, or dict), run the function recursively for all its sub-elements.
    If ``direct==True``, directly use RPyC ``obtain`` method; otherwise use the custom method, which works better with large numpy arrays,
    but worse with composite types (e.g., lists).
    """
    t=type(proxy) # each isinstance call is performed on the server, so getting type once is faster
    if deep and not direct and issubclass(t,tuple): # tuples are not passed as netrefs, so they need to be checked first
        return tuple([obtain(v,serv=serv) for v in proxy])
    if not issubclass(t,rpyc.BaseNetref):
        return proxy
    if direct:
        return rpyc.classic.obtain(proxy)
    if deep:
        if isinstance(proxy,list):
            return [obtain(v,serv=serv) for v in proxy]
        if isinstance(proxy,dict):
            return {obtain(k,serv=serv):obtain(v,serv=serv) for k,v in proxy.items()}
    if isinstance(proxy,np.ndarray) or (t.__name__=="numpy.ndarray" and all([hasattr(proxy,a) for a in ["shape","dtype","tostring","flatten"]])):
        elsize=np.prod(proxy.shape,dtype="u8")
        bytesize=proxy.dtype.itemsize*elsize
        if bytesize>_numpy_block_size:
            if _is_tunnel_service(serv):
                loc_serv=serv.peer
                async_send=rpyc.async_(serv.tunnel_send)
                async_send(proxy,packer="numpy")
                data=loc_serv.tunnel_recv()
                return np.frombuffer(data,dtype=proxy.dtype.str).reshape(proxy.shape)
            else:
                fproxy=proxy.flatten()
                loc=np.zeros(elsize,dtype=proxy.dtype.str)
                block_size=_numpy_block_size//proxy.dtype.itemsize
                for pos in range(0,elsize,block_size):
                    loc[pos:pos+block_size]=rpyc.classic.obtain(fproxy[pos:pos+block_size])
                return loc.reshape(proxy.shape)
    return rpyc.classic.obtain(proxy)
def transfer(obj, serv):
    """
    Send a local object to the remote PC by value (i.e., copy it to the remote Python instance).

    A 'reversed' version of :func:`obtain`.
    """
    return serv.transfer(obj)
def _get_conn_address(conn, peer=False):
    """Get connection IP address"""
    s=socket.fromfd(conn.fileno(),socket.AF_INET,socket.SOCK_STREAM)
    addr=s.getpeername()[0] if peer else s.getsockname()[0]
    s.close()
    return addr

class SocketTunnelService(rpyc.SlaveService):
    """
    Extension of the standard :class:`rpyc.core.service.SlaveService` with built-in network socket tunnel for faster data transfer.

    In order for the tunnel to work, services on both ends need to be subclasses of :class:`SocketTunnelService`.
    Because of the initial setup protocol, the two services are asymmetric: one should be 'server' (corresponding to the listening server),
    and one should be 'client' (external connection). The roles are decided by the `server` constructor parameter.
    """
    _tunnel_block_size=int(2**20)
    def __init__(self, server=False):
        rpyc.SlaveService.__init__(self)
        self.server=server
    _default_tunnel_timeout=10.
    def _recv_socket(self, addr):
        """Set up a listener to receive a socket connection from the other service"""
        def listen(s):
            s.set_timeout(self._default_tunnel_timeout)
            self.tunnel_socket=s
        remote_call=rpyc.async_(self._conn.root._send_socket)
        def port_func(port):
            remote_call(addr,port)
        net.listen(addr,0,listen,port_func=port_func,timeout=self._default_tunnel_timeout,connections_number=1,socket_kwargs={"nodelay":True})
    def _send_socket(self, dst_addr, dst_port):
        """Set up a client socket to connect to the other service"""
        self.tunnel_socket=net.ClientSocket(timeout=self._default_tunnel_timeout,nodelay=True)
        self.tunnel_socket.connect(dst_addr,dst_port)

    def tunnel_send(self, obj, packer=None):
        """
        Send data through the socket tunnel.

        If `packer` is not ``None``, it defines a function to convert `obj` to a bytes string.
        """
        packer=_default_packers.get(packer,packer)
        if packer:
            obj=packer(obj)
        nchunks=(len(obj)-1)//self._tunnel_block_size+1
        self.tunnel_socket.send_fixedlen(struct.pack(">I",nchunks))
        for pos in range(0,len(obj),self._tunnel_block_size):
            self.tunnel_socket.send_decllen(obj[pos:pos+self._tunnel_block_size])
    def tunnel_recv(self, unpacker=None):
        """
        Receive data sent through the socket tunnel.

        If `unpacker` is not ``None``, it defines a function to convert the received bytes string into an object.
        """
        nchunks,=struct.unpack(">I",self.tunnel_socket.recv_fixedlen(4))
        chunks=[]
        for _ in range(nchunks):
            chunks.append(self.tunnel_socket.recv_decllen())
        obj=b"".join(chunks)
        unpacker=_default_unpackers.get(unpacker,unpacker)
        return unpacker(obj) if unpacker else obj

    def obtain(self, proxy):
        """Execute :func:`obtain` on the local instance"""
        return obtain(proxy,self)
    def transfer(self, obj):
        """Execute :func:`transfer` on the local instance"""
        return self.peer.obtain(obj)
    
    def on_connect(self, conn):
        rpyc.SlaveService.on_connect(self,conn)
        self.peer=conn.root
        if not self.server:
            self._recv_socket(_get_conn_address(conn))
    def on_disconnect(self, conn):
        try:
            self.tunnel_socket.close()
        except AttributeError:
            pass
        rpyc.SlaveService.on_disconnect(self,conn)

class DeviceService(SocketTunnelService):
    """
    Device RPyC service.

    Expands on :class:`SocketTunnelService` by adding :meth:`get_device` method,
    which opens local devices, tracks them, and closes them automatically on disconnect.
    """
    def __init__(self, verbose=False):
        SocketTunnelService.__init__(self,server=True)
        self.verbose=verbose
        self.devices=[]
    def on_connect(self, conn):
        SocketTunnelService.on_connect(self,conn)
        self.devices=[]
        if self.verbose:
            conn_addr=_get_conn_address(self._conn,peer=True)
            conn_host=net.get_remote_hostname(conn_addr) or "unknown"
            print("Connected client {} from {}, IP {}".format(self._conn,conn_host,conn_addr))
    def on_disconnect(self, conn):
        if self.verbose and self.devices:
            print("Closing devices {} from client {}".format(self.devices,self._conn))
        for dev in self.devices:
            try:
                dev.close()
            except:  # pylint: disable=bare-except
                pass
        self.devices=[]
        if self.verbose:
            print("Disconnected client {}".format(self._conn))
        SocketTunnelService.on_disconnect(self,conn)
    def get_device_class(self, cls):
        """
        Get remote device class.

        `cls` is the full class name, including the module within ``pylablib.devices``
        (e.g., ``Attocube.ANC300``).
        """
        if self.verbose:
            print("Requesting device class {} from client {}".format(cls,self._conn))
        module,cls=cls.rsplit(".",maxsplit=1)
        try:
            module=importlib.import_module(module)
        except ImportError:
            module=importlib.import_module(module_utils.get_library_name()+".devices."+module)
        module._rpyc=True
        return getattr(module,cls)
    def get_device(self, cls, *args, **kwargs):
        """
        Connect to a device.

        `cls` is the full class name, including the module within ``pylablib.devices``
        (e.g., ``Attocube.ANC300``).
        Stores reference to the connected device and closes it automatically on disconnect.
        """
        cls=self.get_device_class(cls)
        dev=cls(*args,**kwargs)
        self.devices.append(dev)
        return dev

def run_device_service(port=18812, verbose=False):
    """Start :class:`DeviceService` at the given port"""
    if verbose:
        hostips=net.get_all_local_addr()
        hostnames=net.get_local_hostname(full=False),net.get_local_hostname(full=True)
        hostips_list=", ".join(["{}:{}".format(ip,port) for ip in hostips])
        print("Running device service at {} ({}), IP {}".format(hostnames[0],hostnames[1],hostips_list))
    rpyc.ThreadedServer(rpyc.utils.helpers.classpartial(DeviceService,verbose=verbose),port=port).start()

def connect_device_service(addr, port=18812, timeout=3, attempts=2, error_on_fail=True, config=None):
    """
    Connect to the :class:`DeviceService` running at the given address and port
    
    `timeout` and `attempts` define respectively timeout of a single connection attempt, and the number of attempts
    (RPyC default is 3 seconds timeout and 6 attempts).
    If ``error_on_fail==True``, raise error if the connection failed; otherwise, return ``None``
    """
    addr,port=net.as_addr_port(addr,port)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            s=rpyc.SocketStream.connect(addr,port,timeout=timeout,attempts=attempts)
            config=library_parameters.library_parameters["remote/rpyc/default_connect_config"] if config is None else config
            return rpyc.connect_stream(s,SocketTunnelService,config=config).root
        except net.socket.timeout:
            if error_on_fail:
                raise
            return None