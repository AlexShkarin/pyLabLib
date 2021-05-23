"""
A wrapper for built-in TCP/IP routines.
"""


import socket, json, contextlib
from . import funcargparse, strpack, general, py3


class SocketError(socket.error):
    """
    Base socket error class.
    """
    pass
        
class SocketTimeout(SocketError):
    """
    Socket timeout error.
    """
    pass


def _wait_sock_func(func, timeout, wait_callback):
    if wait_callback is None:
        return func()
    cnt=general.Countdown(timeout)
    while True:
        try:
            return func()
        except socket.timeout:
            wait_callback()
            if cnt.passed():
                raise

def get_local_addr():
    """Get local IP address."""
    return socket.gethostbyname(socket.gethostname())
def get_all_local_addr():
    """Get a list of all local IP address."""
    return socket.gethostbyname_ex(socket.gethostname())[2]
def get_local_hostname():
    """Get a local host name."""
    return socket.gethostbyname_ex(socket.gethostname())[0]

class ClientSocket(object):
    """
    A client socket (used to connect to a server socket).
    
    Args:
        sock (socket.socket): If not ``None``, use already created socket.
        timeout (float): The timeout used for connecting and sending/receiving (``None`` means no timeout).
        wait_callback (callable): Called periodically (every 100ms by default) while waiting for connecting or sending/receiving.
        send_method (str): Default sending method.
        recv_method (str): Default receiving method.
        datatype (str): Type of the returned data; can be ``"bytes"`` (return `bytes` object), ``"str"`` (return `str` object),
            or ``"auto"`` (default Python result: `str` in Python 2 and `bytes` in Python 3)
        nodelay (bool): Whether to enable ``TCP_NODELAY``.
    
    Possible sending/receiving methods are:
        - ``'fixedlen'``: data is sent as is, and receiving requires to know the length of the message;
        - ``'decllen'``: data is prepended by a length, and receiving reads this length and doesn't need predetermined length info.
        
    Attributes:
        sock (socket.socket): Correpsonding Python socket.
        decllen_bo (str): Byteorder of the prependend length for ``'decllen'`` sending method.
            Can be either ``'>'`` (big-endian, default) or ``'<'``.
        decllen_ll (int): Length of the prependend length for ``'decllen'`` sending method; default is 4 bytes.
    """
    _default_wait_callback_timeout=0.1
    def __init__(self, sock=None, timeout=None, wait_callback=None, send_method="decllen", recv_method="decllen", datatype="auto", nodelay=False):
        funcargparse.check_parameter_range(send_method,"send_method",{"fixedlen","decllen"})
        funcargparse.check_parameter_range(recv_method,"recv_method",{"fixedlen","decllen"})
        funcargparse.check_parameter_range(datatype,"datatype",{"auto","str","bytes"})
        object.__init__(self)
        self.nodelay=nodelay
        self.sock=sock or socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        if self.nodelay:
            self.sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
        self.connected=False
        self.timeout=timeout
        self.wait_callback=wait_callback
        if wait_callback is not None:
            self.sock.settimeout(self._default_wait_callback_timeout)
        elif timeout is not None:
            self.sock.settimeout(timeout)
        self.send_method=send_method
        self.recv_method=recv_method
        self.datatype=datatype
        self.decllen_bo=">"
        self.decllen_ll=4
        
    def set_wait_callback(self, wait_callback=None):
        """Set callback function for waiting during connecting or sending/receiving."""
        self.wait_callback=wait_callback
        if wait_callback is not None:
            self.sock.settimeout(self._default_wait_callback_timeout)
        else:
            self.sock.settimeout(self.timeout)
    def set_timeout(self, timeout=None):
        """Set timeout for connecting or sending/receiving."""
        self.timeout=timeout
        if self.wait_callback is None:
            self.sock.settimeout(self.timeout)
    def get_timeout(self):
        """Get timeout for connecting or sending/receiving."""
        return self.timeout
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
    
    def _connect_callback(self):
        self.sock.close()
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        if self.nodelay:
            self.sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
        if self.wait_callback:
            self.sock.settimeout(self._default_wait_callback_timeout)
        elif self.timeout is not None:
            self.sock.settimeout(self.timeout)
        if self.wait_callback:
            self.wait_callback()
    def connect(self, host, port):
        """Connect to a remote host."""
        def sock_func():
            self.sock.connect((host,port))
            self.connected=True
        return _wait_sock_func(sock_func,self.timeout,self._connect_callback)
    def close(self):
        """Close the connection."""
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        try:
            self.sock.close()
        except socket.error:
            pass
        self.connected=False
    def is_connected(self):
        """Check if the connection is opened"""
        return self.connected
    def __bool__(self):
        return self.is_connected()

    def get_local_name(self):
        """Return IP address and port of this socket."""
        return self.sock.getsockname()
    def get_peer_name(self):
        """Return IP address and port of the peer socket."""
        return self.sock.getpeername()
        
    def _recv_wait(self, l):
        sock_func=lambda: self.sock.recv(l)
        try:
            recvd=_wait_sock_func(sock_func,self.timeout,self.wait_callback)
        except socket.timeout:
            raise SocketTimeout("timeout while receiving")
        except ConnectionResetError:
            raise SocketError("connection closed while receiving")
        if len(recvd)==0:
            raise SocketError("connection closed while receiving")
        return recvd
    def _send_wait(self, msg):
        sock_func=lambda: self.sock.send(py3.as_builtin_bytes(msg))
        return _wait_sock_func(sock_func,self.timeout,self.wait_callback)
    
    def recv_fixedlen(self, l):
        """Receive fixed-length message of length `l`."""
        chunks=[]
        lread=0
        while lread<l:
            chunks.append(self._recv_wait(l-lread))
            lread+=len(chunks[-1])
        buf=b"".join(chunks)
        return py3.as_datatype(buf,self.datatype)
    def recv_delimiter(self, delim, lmax=None, chunk_l=1024, strict=False):
        """
        Receive a single message ending with a delimiter `delim` (can be several characters, or list several possible delimiter strings).
        
        `lmax` specifies the maximal received length (`None` means no limit).
        `chunk_l` specifies the size of data chunk to be read in one try.
        If ``strict==False``, keep receiving as much data as possible until a delimiter is found in the end (only works properly if a single line is expected);
        otherwise, receive the data byte-by-byte and stop as soon as a delimiter is found (equivalent ot setting ``chunk_l=1``).
        """
        buf=b""
        if isinstance(delim, py3.anystring):
            delim=[delim]
        delim=[py3.as_builtin_bytes(d) for d in delim]
        if strict:
            chunk_l=1
        while not any([buf.endswith(d) for d in delim]):
            buf=buf+self._recv_wait(chunk_l)
            if (lmax is not None) and len(buf)>lmax:
                break
        return py3.as_datatype(buf,self.datatype)
    def recv_decllen(self):
        """
        Receive variable-length message (prepended by its length).
        
        Length format is described by `decllen_bo` and `decllen_ll` attributes.
        """
        len_msg=self.recv_fixedlen(self.decllen_ll)
        l=strpack.unpack_uint(len_msg,self.decllen_bo)
        return self.recv_fixedlen(l)
    def recv(self, l=None):
        """
        Receive a message using the default method.
        """
        if self.send_method=="decllen":
            return self.recv_decllen()
        else:
            return self.recv_fixedlen(l)
    def recv_all(self, chunk_l=1024):
        """
        Receive all of the data currently in the socket.

        `chunk_l` specifies the size of data chunk to be read in one try.
        For technical reasons, use 1ms timeout (i.e., this operation takes 1ms).
        """
        buf=b""
        with self.using_timeout(1E-3):
            try:
                while True:
                    buf+=self._recv_wait(chunk_l)
            except SocketTimeout:
                pass
        return py3.as_datatype(buf,self.datatype)
    def recv_ack(self, l=None):
        """Receive a message using the default method and send an acknowledgement (message length)."""
        msg=self.recv(l=l)
        ack_msg=strpack.pack_uint(len(msg),self.decllen_ll,self.decllen_bo)
        self.send_fixedlen(ack_msg)
        return msg
    
    def send_fixedlen(self, msg):
        """Send a message as is."""
        sent_total=0
        while sent_total<len(msg):
            try:
                sent=self._send_wait(msg[sent_total:])
            except socket.timeout:
                raise SocketTimeout("timeout while sending")
            if sent==0:
                raise SocketError("connection closed while sending")
            sent_total=sent_total+sent
        return sent_total
    def send_decllen(self, msg):
        """
        Send a message as a variable-length (prepending its length in the sent message).
        
        Length format is described by `decllen_bo` and `decllen_ll` attributes.
        """
        len_msg=strpack.pack_uint(len(msg),self.decllen_ll,self.decllen_bo)
        msg=py3.as_builtin_bytes(msg)
        if self.nodelay:
            return self.send_fixedlen(len_msg+msg)-len(len_msg)
        else:
            self.send_fixedlen(len_msg)
            return self.send_fixedlen(msg)
    def send_delimiter(self, msg, delimiter):
        """
        Send a message with a delimiter `delim` (can be several characters).
        """
        return self.send_fixedlen(msg+delimiter)-len(delimiter)
    def send(self, msg):
        """
        Send a message using the default method.
        """
        if self.send_method=="decllen":
            return self.send_decllen(msg)
        else:
            return self.send_fixedlen(msg)
    def send_ack(self, msg):
        """
        Send a message using default method and wait for acknowledgement (message length).
        
        If the acknowledgement message length doesn't agree, raise :exc:`SocketError`.
        """
        res=self.send(msg)
        ack_msg=self.recv_fixedlen(self.decllen_ll)
        l=strpack.unpack_uint(ack_msg,self.decllen_bo)
        if l!=len(msg):
            raise SocketError("acknowledgement message contains wrong length: expect {}, got {}".format(len(msg),l))
        return res
        
        

def recv_JSON(socket, chunk_l=1024, strict=True):
    """
    Receive a complete JSON token from the socket.

    `chunk_l` specifies the size of data chunk to be read in one try.
    If ``strict==False``, keep receiving as much data as possible until the received data forms a complete JSON token.
    otherwise, receive the data byte-by-byte and stop as soon as a token is formed (equivalent ot setting ``chunk_l=1``).
    """
    msg="" if socket.datatype=="str" else b""
    while True:
        msg+=socket.recv_delimiter("}",chunk_l=chunk_l,strict=strict)
        try:
            json.loads(msg)
            return msg
        except ValueError:
            pass
        
        
_listen_wait_callback_timeout=0.1
def listen(host, port, conn_func, port_func=None, wait_callback=None, timeout=None, backlog=10, wrap_socket=True, connections_number=None, socket_args=None):
    """
    Run a server socket at the given host and port.
    
    Args:
        host (str): Server host address. If ``None``, use the local host defined by :func:`socket.gethostname`.
        port (int): Server port. If ``0``, generate an arbitrary free port.
        conn_func (callable): Called with the client socket as a single argument every time a connection is established.
        port_func (callable): Called with the port as a single argument when the listening starts (useful with ``port=0``).
        wait_callback (callable): A callback function which is called periodically (every 100ms by default) while awaiting for connections.
        timeout (float): Timeout for waiting for the connections (``None`` is no timeout).
        backlog (int): Backlog length for the socket (see :meth:`socket.socket.listen`).
        wrap_socket (bool): If ``True``, wrap the client socket of the connection into :class:`ClientSocket` class;
            otherwise, return :class:`socket.socket` object.
        connections_number (int): Specifies maximal number of connections before the listening function returns (by default, the number is unlimited).
        socket_args (dict): parameters passed to :class:`ClientSocket` constructor.
        
    Checking for connections is paused until `conn_func` returns.
    If multiple connections are expected, `conn_func` should spawn a separate processing thread and return.
    """
    if host is None:
        host=socket.gethostbyname(socket.gethostname())
    serv_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    if wait_callback is not None:
        serv_sock.settimeout(_listen_wait_callback_timeout)
    elif timeout is not None:
        serv_sock.settimeout(timeout)
    serv_sock.bind((host,port))
    if port_func:
        port_func(serv_sock.getsockname()[1])
    serv_sock.listen(backlog)
    def sock_func():
        client_sock,_=serv_sock.accept()
        if wrap_socket:
            client_sock=ClientSocket(client_sock,**(socket_args or {}))
        conn_func(client_sock)
    try:
        cnt=0
        while True:
            _wait_sock_func(sock_func,timeout,wait_callback)
            cnt+=1
            if connections_number is not None and cnt>=connections_number:
                return
    finally:
        serv_sock.close()