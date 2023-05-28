from ...core.utils import net
from ...core.devio import interface, comm_backend
from ...core.devio.comm_backend import reraise

import json
import time
import contextlib

c=299792458.

class M2Error(comm_backend.DeviceError):
    """Generic M2 error"""
class M2ParseError(M2Error):
    """M2 parse error"""
    def __init__(self, *args, code=None):
        super().__init__(*args)
        self.code=code
class M2CommunicationError(M2Error,comm_backend.DeviceBackendError):
    """M2 network communication error"""

class ICEBlocDevice(interface.IDevice):
    """
    Generic M2 Ice Bloc device.

    Args:
        addr(str): IP address of the Ice Bloc device.
        port(int): port of the Ice Bloc device.
        timeout(float): default timeout of synchronous operations.
        start_link(bool): if ``True``, initialize device link on creation.
    """
    Error=M2Error
    ReraiseError=M2CommunicationError
    BackendError=net.socket.error
    def __init__(self, addr, port, timeout=5., start_link=True):
        super().__init__()
        self.tx_id=1
        self.conn=(addr,port)
        self.timeout=timeout
        self.socket=None
        self._operation_cooldown=0.02
        self._start_link_on_open=start_link
        self._skipped_replies=0
        self._noreply=False
        self.open()
        self._last_status={}


    def _get_connection_parameters(self):
        return self.conn
    @reraise
    def open(self):
        self.close()
        self.socket=net.ClientSocket(send_method="fixedlen",recv_method="fixedlen",timeout=self.timeout)
        try:
            self.socket.connect(*self.conn)
        except net.socket.error:
            self.socket.close()
            raise
        self._last_status={}
        if self._start_link_on_open:
            self.start_link()
        self._start_link_on_open=True
    @reraise
    def close(self):
        if self.socket is not None:
            self.socket.close()
            self.socket=None
    @reraise
    def is_opened(self):
        return self.socket and self.socket.is_connected()
    @reraise
    def set_timeout(self, timeout):
        """Set timeout for connecting or sending/receiving"""
        self.timeout=timeout
        self.socket.set_timeout(timeout)

    def _build_message(self, op, params, tx_id=None):
        if tx_id is None:
            tx_id=self.tx_id
            self.tx_id=self.tx_id%16383+1
        msg={"message":{"transmission_id":[tx_id],"op":op}}
        if params is not None:
            msg["message"]["parameters"]=dict(params)
        return json.dumps(msg,default=float)
    def _parse_message(self, msg):
        pmsg=json.loads(msg)
        if "message" not in pmsg:
            raise M2Error("could not decode message: {}".format(msg))
        pmsg=pmsg["message"]
        for key in ["transmission_id", "op", "parameters"]:
            if key not in pmsg:
                raise M2Error("parameter '{}' not in the message {}".format(key,msg))
        return pmsg
    _parse_errors=["unknown", "JSON parsing error", "'message' string missing",
                             "'transmission_id' string missing", "No 'transmission_id' value",
                             "'op' string missing", "No operation name",
                             "operation not recognized", "'parameters' string missing", "invalid parameter tag or value"]
    def _parse_reply(self, msg):
        pmsg=self._parse_message(msg)
        if pmsg["op"]=="parse_fail":
            par=pmsg["parameters"]
            perror=par["protocol_error"][0]
            perror_desc="unknown" if perror>=len(self._parse_errors) else self._parse_errors[perror]
            error_msg="device parse error: transmission_id={}, error={}({}), error point='{}'".format(
                par.get("transmission",["NA"])[0],perror,perror_desc,par.get("JSON_parse_error","NA"))
            raise M2ParseError(error_msg,code=perror)
        return pmsg["op"],pmsg["parameters"]
    
    _extra_update_ops=()
    def _is_report_op(self, op):
        return op.endswith("_f_r") or op in self._extra_update_ops
    def _make_report_op(self, op):
        return op if op in self._extra_update_ops else op+"_f_r"
    def _parse_report_op(self, op):
        return op if op in self._extra_update_ops else op[:-4]
    @reraise
    def _recv_reply(self, expected_report=None):
        while True:
            reply=net.recv_JSON(self.socket)
            preply=self._parse_reply(reply)
            if self._is_report_op(preply[0]):
                self._last_status[self._parse_report_op(preply[0])]=preply[1]
            else:
                return preply
            if preply[0]==expected_report:
                return preply
    @reraise
    def flush(self):
        """Flush read buffer"""
        self.socket.recv_all()
    
    @contextlib.contextmanager
    def noreply(self, exhaust_when_done=False):
        """
        Context manager within which the code switches to the no-reply mode,
        where it does not wait for a reply to certain commands (usually element setting commands).
        This allows for faster command issuing, but ignores possible errors returned by the commands.
        If ``exhaust_when_done==True``, receive all sent replies upon exiting the context;
        otherwise, receive them the next time a communication with the device is done.
        """
        norep=self._noreply
        self._noreply=True
        try:
            yield
        finally:
            self._noreply=norep
            if exhaust_when_done and not norep:
                self._exhaust_skipped_replies()
    @reraise
    def query(self, op, params, reply_op="auto", report=False, allow_noreply=False):
        """
        Send a query using the standard device interface.

        `reply_op` is the name of the reply operation (by default, its the operation name plus ``"_reply"``).
        If ``report==True``, request completion report (does not apply to all operation).
        If ``allow_noreply==True``, allow skipping the reply, which allows for faster consecutive command issuing;
        this only works if the no-reply mode is also activated using :meth:`noreply`.
        Return tuple ``(command, args)`` with the reply command name and the corresponding arguments
        (in no-reply mode return ``(None, None)``).
        """
        if report:
            params["report"]="finished"
            self._last_status[op]=None
        msg=self._build_message(op,params)
        if allow_noreply and self._noreply:
            self._exhaust_skipped_replies(leave_max=max(self._max_skipped_replies-1,0))
            self.socket.send(msg)
            self._skipped_replies+=1
            return None,None
        self._exhaust_skipped_replies()
        for t in range(5):
            try:
                time.sleep(self._operation_cooldown)
                self.socket.send(msg)
                preply=self._recv_reply()
                break
            except net.socket.error:
                if t==4:
                    raise
                time.sleep(1.)
        if reply_op=="auto":
            reply_op=op+"_reply"
        if reply_op and preply[0]!=reply_op:
            raise M2Error("unexpected reply op: '{}' (expected '{}')".format(preply[0],reply_op))
        return preply
    @reraise
    def update_reports(self, timeout=0., ignore_replies=None, max_replies=None):
        """
        Check for fresh operation reports.
        
        By default, only receive reports and raise an error on replies; if ``ignore_replies`` is supplies, it is a list of replies which do not raise an error.
        If ``max_replies`` is supplied, it is the maximal number of replies to read before stopping (by default, no limit, i.e., wait a read leads to a timeout).
        """
        timeout=max(timeout,0.001)
        recv_reports=[]
        try:
            with self.socket.using_timeout(timeout):
                while True:
                    preport=self._recv_reply()
                    if not (ignore_replies and (ignore_replies=="all" or preport[0] in ignore_replies)):
                        raise M2Error("received reply while waiting for a report: '{}'".format(preport[0]))
                    recv_reports.append(preport)
                    if max_replies is not None and len(recv_reports)>=max_replies:
                        break
        except M2CommunicationError as err:
            if not isinstance(err.backend_exc,net.SocketTimeout):
                raise
        return recv_reports if ignore_replies else None
    _max_skipped_replies=5
    def _exhaust_skipped_replies(self, leave_max=0):
        while self._skipped_replies>leave_max:
            reps=self.update_reports(timeout=1.,ignore_replies="all",max_replies=self._skipped_replies-leave_max)
            self._skipped_replies-=len(reps)
    def get_last_report(self, op):
        """Get the latest report for the given operation"""
        rep=self._last_status.get(op,None)
        if rep:
            return "fail" if rep["report"][0] else "success"
        return None
    def check_report(self, op):
        """Check and return the latest report for the given operation"""
        self.update_reports()
        report=self.get_last_report(op)
        return report
    @reraise
    def wait_for_report(self, op, error_msg=None, timeout=None):
        """
        Wait for a report for the given operation
        
        `error_msg` specifies the exception message if the report results in an error.
        """
        with self.socket.using_timeout(timeout):
            preport=self._recv_reply(expected_report=self._make_report_op(op))
            if not self._is_report_op(preport[0]):
                raise M2Error("unexpected report op: '{}'".format(preport[0]))
        if "report" in preport[1] and preport[1]["report"][0]!=0:
            if error_msg is None:
                error_msg="error on operation {}; error report {}".format(preport[0][:-4],preport[1])
            raise M2Error(error_msg)
        return preport


    @reraise
    def start_link(self):
        """Initialize device link (called automatically on creation)"""
        reply=self.query("start_link",{"ip_address":self.socket.get_local_name()[0]})[1]
        if reply["status"]!="ok":
            raise M2Error("could not establish link: reply status '{}'".format(reply["status"]))