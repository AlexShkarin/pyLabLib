from __future__ import print_function # Python 2 compatibility
from ...core.utils import net, general
from ...core.devio.interface import IDevice

import websocket

import json
import time
import logging
import threading
import sys


c=299792458.

class M2Error(RuntimeError):
    """
    M2 communication error.
    """
    pass
class M2ICE(IDevice):
    """
    M2 ICE device.

    Args:
        addr(str): IP address of the ICE device.
        port(int): port of the ICE device.
        timeout(float): default timeout of synchronous operations.
        start_link(bool): if ``True``, initialize device link on creation.
        use_websocket(bool): if ``True``, use websocket interface (same as used by the web interface) for additional functionality
            (wavemeter connection, etalon value, improved operation stopping)
        only_websocket(bool): if ``True``, only use websocket operations (raises error on most standard methods, mostly used to monitor status).
    """
    def __init__(self, addr, port, timeout=5., start_link=True, use_websocket=True, only_websocket=False):
        IDevice.__init__(self)
        self.tx_id=1
        self.conn=(addr,port)
        self.timeout=timeout
        self.socket=None
        self._operation_cooldown=0.02
        if not only_websocket:
            self.open()
            if start_link:
                self.start_link()
        self._last_status={}
        self.use_websocket=use_websocket
        self._websocket_lock=threading.Lock()
        self._add_status_node("web_status",self.get_full_web_status)
        self._add_status_node("system_status",self.get_system_status)
        self._add_settings_node("wavemeter_connected",self.is_wavelemeter_connected,lambda v: self.connect_wavemeter() if v else self.disconnect_wavemeter())
        self._add_settings_node("etalon_lock",lambda: self.get_etalon_lock_status()=="on",
                lambda v: self.lock_etalon() if v else self.unlock_etalon())
        self._add_settings_node("reference_cavity_lock",lambda: self.get_reference_cavity_lock_status()=="on",
                lambda v: self.lock_reference_cavity() if v else self.unlock_reference_cavity())
        self._add_settings_node("wavemeter_lock",self.is_wavelemeter_lock_on,self.lock_wavemeter)


    def open(self):
        self.close()
        self.socket=net.ClientSocket(send_method="fixedlen",recv_method="fixedlen",timeout=self.timeout)
        try:
            self.socket.connect(*self.conn)
        except net.socket.error:
            self.socket.close()
            raise
        self._last_status={}
    def close(self):
        if self.socket is not None:
            self.socket.close()
            self.socket=None
    def is_opened(self):
        return self.socket.is_connected()
    def set_timeout(self, timeout):
        """Set timeout for connecting or sending/receiving."""
        self.timeout=timeout
        self.socket.set_timeout(timeout)

    def _build_message(self, op, params, tx_id=None):
        if tx_id is None:
            tx_id=self.tx_id
            self.tx_id=self.tx_id%16383+1
        msg={"message":{"transmission_id":[tx_id],"op":op,"parameters":dict(params)}}
        return json.dumps(msg,default=float)
    def _parse_message(self, msg):
        pmsg=json.loads(msg)
        if "message" not in pmsg:
            raise M2Error("coudn't decode message: {}".format(msg))
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
            raise M2Error(error_msg)
        return pmsg["op"],pmsg["parameters"]
    
    _terascan_update_op="wavelength"
    def _is_report_op(self, op):
        return op.endswith("_f_r") or op==self._terascan_update_op
    def _make_report_op(self, op):
        return op if op==self._terascan_update_op else op+"_f_r"
    def _parse_report_op(self, op):
        return op if op==self._terascan_update_op else op[:-4]
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
    def flush(self):
        """Flush read buffer"""
        self.socket.recv_all()
    def query(self, op, params, reply_op="auto", report=False):
        """
        Send a query using the standard device interface.

        `reply_op` is the name of the reply operation (by default, its the operation name plus ``"_reply"``).
        If ``report==True``, request completion report (doesn't apply to all operation).
        """
        if report:
            params["report"]="finished"
            self._last_status[op]=None
        msg=self._build_message(op,params)
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
                print("M2 query timeout",file=sys.stderr)
        if reply_op=="auto":
            reply_op=op+"_reply"
        if reply_op and preply[0]!=reply_op:
            raise M2Error("unexpected reply op: '{}' (expected '{}')".format(preply[0],reply_op))
        return preply
    def update_reports(self, timeout=0.):
        """Check for fresh operation reports."""
        timeout=max(timeout,0.001)
        try:
            with self.socket.using_timeout(timeout):
                preport=self._recv_reply()
                raise M2Error("received reply while waiting for a report: '{}'".format(preport[0]))
        except net.SocketTimeout:
            pass
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


    def start_link(self):
        """Initialize device link (called automatically on creation)."""
        reply=self.query("start_link",{"ip_address":self.socket.get_local_name()[0]})[1]
        if reply["status"]!="ok":
            raise M2Error("couldn't establish link: reply status '{}'".format(reply["status"]))

    def _send_websocket_request(self, msg):
        if self.use_websocket:
            for t in range(5):
                try:
                    with self._websocket_lock:
                        ws=websocket.create_connection("ws://{}:8088/control.htm".format(self.conn[0]),timeout=10.)
                        try:
                            self._wait_for_websocket_status(ws,present_key="wlm_fitted")
                            self._wait_for_websocket_status(ws,present_key="wlm_fitted")
                            ws.send(msg)
                            return
                        finally:
                            logging.getLogger("websocket").setLevel(logging.CRITICAL)
                            ws.close()
                except websocket.WebSocketTimeoutException:
                    if t==4:
                        raise
                    time.sleep(5.)
                    print("M2 websocket timeout",file=sys.stderr)
        else:
            raise RuntimeError("'websocket' library is requried to communicate this request")
    def _wait_for_websocket_status(self, ws, present_key=None, nmax=20):
        full_data={}
        for _ in range(nmax):
            data=ws.recv()
            full_data.update(json.loads(data))
            if present_key is None or present_key in data:
                return full_data
    def _read_websocket_status(self, present_key=None, nmax=20):
        if self.use_websocket:
            for t in range(5):
                try:
                    with self._websocket_lock:
                        ws=websocket.create_connection("ws://{}:8088/control.htm".format(self.conn[0]),timeout=5.)
                        try:
                            return self._wait_for_websocket_status(ws,present_key=present_key,nmax=nmax)
                        finally:
                            ws.recv()
                            logging.getLogger("websocket").setLevel(logging.CRITICAL)
                            ws.close()
                except websocket.WebSocketTimeoutException:
                    if t==4:
                        raise
                    time.sleep(5.)
                    print("M2 websocket timeout",file=sys.stderr)
        else:
            raise RuntimeError("'websocket' library is requried to communicate this request")
    def _try_connect_wavemeter(self, sync=True):
        self._send_websocket_request('{"message_type":"task_request","task":["start_wavemeter_link"]}')
        if sync:
            while not self.is_wavelemeter_connected():
                time.sleep(0.02)
    def connect_wavemeter(self, sync=True):
        """Connect to the wavemeter (if ``sync==True``, wait until the connection is established)"""
        if not self.use_websocket:
            return
        if self.is_wavelemeter_connected():
            return
        self.stop_all_operation()
        self._try_connect_wavemeter(sync=sync)
    def _try_disconnect_wavemeter(self, sync=True):
        self._send_websocket_request('{"message_type":"task_request","task":["job_stop_wavemeter_link"]}')
        if sync:
            for _ in range(25):
                if not self.is_wavelemeter_connected():
                    return
                time.sleep(0.02)
    def disconnect_wavemeter(self, sync=True):
        """Disconnect from the wavemeter (if ``sync==True``, wait until the connection is broken)"""
        if not self.use_websocket:
            return
        if not self.is_wavelemeter_connected():
            return
        if not sync:
            self._try_disconnect_wavemeter(sync=False)
        else:
            while self.is_wavelemeter_connected():
                self.stop_all_operation()
                self.lock_wavemeter(False)
                if self.is_wavelemeter_lock_on():
                    time.sleep(1.)
                self._try_disconnect_wavemeter(sync=True)
    def is_wavelemeter_connected(self):
        """Check if the wavemeter is connected"""
        return bool(self._read_websocket_status(present_key="wlm_fitted")["wlm_fitted"]) if self.use_websocket else None

    def get_system_status(self):
        """Get the device system status"""
        _,reply=self.query("get_status",{})
        for k in reply:
            if isinstance(reply[k],list):
                reply[k]=reply[k][0]
        return reply
    def get_full_web_status(self):
        """
        Get full websocket status.
        
        Return a large dictionary containing all the information available in the web interface.
        """
        return self._read_websocket_status(present_key="boot_files") if self.use_websocket else None
    def _as_web_status(self, status):
        if status=="auto":
            status="new" if self.use_websocket else None
        if status=="new":
            return self.get_full_web_status()
        if status is None:
            return None
        return status
    
    def get_full_tuning_status(self):
        """Get full fine-tuning status (see M2 ICE manual for ``"poll_wave_m"`` command)"""
        return self.query("poll_wave_m",{})[1]
    def lock_wavemeter(self, lock=True, sync=True, error_on_fail=True):
        """Lock or unlock the laser to the wavemeter (if ``sync==True``, wait until the operation is complete)"""
        _,reply=self.query("lock_wave_m",{"operation":"on" if lock else "off"})
        if reply["status"][0]==1:
            if error_on_fail:
                raise M2Error("can't lock wavemeter: no wavemeter link")
            else:
                return
        if sync:
            while self.is_wavelemeter_lock_on()!=lock:
                time.sleep(0.05)
    def is_wavelemeter_lock_on(self):
        """Check if the laser is locked to the wavemeter"""
        return bool(self.get_full_tuning_status()["lock_status"][0])

    def tune_wavelength(self, wavelength, sync=True, timeout=None):
        """
        Fine-tune the wavelength.
        
        Only works if the wavemeter is connected.
        If ``sync==True``, wait until the operation is complete (might take from several seconds up to several minutes).
        """
        _,reply=self.query("set_wave_m",{"wavelength":[wavelength*1E9]},report=True)
        if reply["status"][0]==1:
            raise M2Error("can't tune wavelength: no wavemeter link")
        elif reply["status"][0]==2:
            raise M2Error("can't tune wavelength: {}nm is out of range".format(wavelength*1E9))
        if sync:
            self.wait_for_report("set_wave_m",timeout=timeout)
    def check_tuning_report(self):
        """
        Check wavelength fine-tuning report

        Return ``"success"`` or ``"fail"`` if the operation is complete, or ``None`` if it is still in progress.
        """
        return self.check_report("set_wave_m")
    def wait_for_tuning(self, timeout=None):
        """Wait until wavelength fine-tuning is complete"""
        self.wait_for_report("set_wave_m",timeout=timeout)
    def get_tuning_status(self):
        """
        Get fine-tuning status.

        Return either ``"idle"`` (no tuning or locking), ``"nolink"`` (no wavemeter link),
        ``"tuning"`` (tuning in progress), or ``"locked"`` (tuned and locked to the wavemeter).
        """
        status=self.get_full_tuning_status()["status"][0]
        return ["idle","nolink","tuning","locked"][status]
    def get_wavelength(self):
        """
        Get fine-tuned wavelength.
        
        Only works if the wavemeter is connected.
        """
        return self.get_full_tuning_status()["current_wavelength"][0]*1E-9
    def stop_tuning(self):
        """Stop fine wavelength tuning."""
        _,reply=self.query("stop_wave_m",{})
        if reply["status"][0]==1:
            raise M2Error("can't stop tuning: no wavemeter link")

    def tune_wavelength_table(self, wavelength, sync=True):
        """
        Coarse-tune the wavelength.
        
        Only works if the wavemeter is disconnected.
        If ``sync==True``, wait until the operation is complete.
        """
        _,reply=self.query("move_wave_t",{"wavelength":[wavelength*1E9]},report=True)
        if reply["status"][0]==1:
            raise M2Error("can't tune wavelength: command failed")
        elif reply["status"][0]==2:
            raise M2Error("can't tune wavelength: {}nm is out of range".format(wavelength*1E9))
        if sync:
            self.wait_for_report("move_wave_t")
    def get_full_tuning_status_table(self):
        """Get full coarse-tuning status (see M2 ICE manual for ``"poll_move_wave_t"`` command)"""
        return self.query("poll_move_wave_t",{})[1]
    def get_tuning_status_table(self):
        """
        Get coarse-tuning status.

        Return either ``"done"`` (tuning is done), ``"tuning"`` (tuning in progress), or ``"fail"`` (tuning failed).
        """
        status=self.get_full_tuning_status_table()["status"][0]
        return ["done","tuning","fail"][status]
    def get_wavelength_table(self):
        """
        Get course-tuned wavelength.
        
        Only works if the wavemeter is disconnected.
        """
        return self.get_full_tuning_status_table()["current_wavelength"][0]*1E-9
    def stop_tuning_table(self):
        """Stop coarse wavelength tuning."""
        self.query("stop_move_wave_t",{})

    def tune_etalon(self, perc, sync=True):
        """
        Tune the etalon to `perc` percent.
        
        Only works if the wavemeter is disconnected.
        If ``sync==True``, wait until the operation is complete.
        """
        _,reply=self.query("tune_etalon",{"setting":[perc]},report=True)
        if reply["status"][0]==1:
            raise M2Error("can't tune etalon: {} is out of range".format(perc))
        elif reply["status"][0]==2:
            raise M2Error("can't tune etalon: command failed")
        if sync:
            self.wait_for_report("tune_etalon")
    def lock_etalon(self, sync=True):
        """
        Lock the etalon (if ``sync==True``, wait until the operation is complete).
        """
        if self.get_etalon_lock_status()=="on":
            return
        _,reply=self.query("etalon_lock",{"operation":"on"},report=True)
        if reply["status"][0]==1:
            raise M2Error("can't lock etalon")
        if sync:
            self.wait_for_report("etalon_lock")
    def unlock_etalon(self, sync=True):
        """
        Lock the etalon (if ``sync==True``, wait until the operation is complete).
        """
        if self.get_etalon_lock_status()=="off":
            return
        self.unlock_reference_cavity(sync=True)
        _,reply=self.query("etalon_lock",{"operation":"off"},report=True)
        if reply["status"][0]==1:
            raise M2Error("can't unlock etalon")
        if sync:
            self.wait_for_report("etalon_lock")
    def get_etalon_lock_status(self):
        """
        Get etalon lock status.

        Return either ``"off"`` (lock is off), ``"on"`` (lock is on), ``"debug"`` (lock in debug condition),
        ``"errorr"`` (lock had an error), ``"search"`` (lock is searching), or ``"low"`` (lock is off due to low output).
        """
        _,reply=self.query("etalon_lock_status",{})
        if reply["status"][0]==1:
            raise M2Error("can't get etalon status")
        return reply["condition"]

    def tune_reference_cavity(self, perc, fine=False, sync=True):
        """
        Tune the reference cavity to `perc` percent.
        
        If ``fine==True``, adjust fine tuning; otherwise, adjust coarse tuning.
        Only works if the wavemeter is disconnected.
        If ``sync==True``, wait until the operation is complete.
        """
        _,reply=self.query("fine_tune_cavity" if fine else "tune_cavity",{"setting":[perc]},report=True)
        if reply["status"][0]==1:
            raise M2Error("can't tune reference cavity: {} is out of range".format(perc))
        elif reply["status"][0]==2:
            raise M2Error("can't tune reference cavity: command failed")
        if sync:
            self.wait_for_report("fine_tune_cavity")
    def lock_reference_cavity(self, sync=True):
        """
        Lock the laser to the reference cavity.
        
        If ``sync==True``, wait until the operation is complete.
        """
        if self.get_reference_cavity_lock_status()=="on":
            return
        self.lock_etalon(sync=True)
        _,reply=self.query("cavity_lock",{"operation":"on"},report=True)
        if reply["status"][0]==1:
            raise M2Error("can't lock reference cavity")
        if sync:
            self.wait_for_report("cavity_lock")
    def unlock_reference_cavity(self, sync=True):
        """
        Unlock the laser from the reference cavity.
        
        If ``sync==True``, wait until the operation is complete.
        """
        if self.get_reference_cavity_lock_status()=="off":
            return
        _,reply=self.query("cavity_lock",{"operation":"off"},report=True)
        if reply["status"][0]==1:
            raise M2Error("can't unlock reference cavity")
        if sync:
            self.wait_for_report("cavity_lock")
    def get_reference_cavity_lock_status(self):
        """
        Get the reference cavity lock status.
        
        Return either ``"off"`` (lock is off), ``"on"`` (lock is on), ``"debug"`` (lock in debug condition),
        ``"errorr"`` (lock had an error), ``"search"`` (lock is searching), or ``"low"`` (lock is off due to low output).
        """
        _,reply=self.query("cavity_lock_status",{})
        if reply["status"][0]==1:
            raise M2Error("can't get etalon status")
        return reply["condition"]

    def tune_laser_resonator(self, perc, fine=False, sync=True):
        """
        Tune the laser cavity to `perc` percent.
        
        If ``fine==True``, adjust fine tuning; otherwise, adjust coarse tuning.
        Only works if the wavemeter is disconnected.
        If ``sync==True``, wait until the operation is complete.
        """
        _,reply=self.query("fine_tune_resonator" if fine else "tune_resonator",{"setting":[perc]},report=True)
        if reply["status"][0]==1:
            raise M2Error("can't tune resonator: {} is out of range".format(perc))
        elif reply["status"][0]==2:
            raise M2Error("can't tune resonator: command failed")
        if sync:
            self.wait_for_report("fine_tune_resonator")

    
    def _check_terascan_type(self, scan_type):
        if scan_type not in {"coarse","medium","fine","line"}:
            raise M2Error("unknown terascan type: {}".format(scan_type))
        if scan_type=="coarse":
            raise M2Error("coarse scan is not currently available")
    _terascan_rates=[50E3,100E3,200E3,500E3, 1E6,2E6,5E6,10E6,20E6,50E6,100E6,200E6,500E6, 1E9,2E9,5E9,10E9,15E9,20E9, 50E9, 100E9]
    def _trunc_terascan_rate(self, rate):
        for tr in self._terascan_rates[::-1]:
            if rate>=tr*(1-1E-5):
                return tr
        return self._terascan_rates[0]
    def setup_terascan(self, scan_type, scan_range, rate, trunc_rate=True):
        """
        Setup terascan.

        Args:
            scan_type(str): scan type. Can be ``"medium"`` (BRF+etalon, rate from 100 GHz/s to 1 GHz/s),
                ``"fine"`` (all elements, rate from 20 GHz/s to 1 MHz/s), or ``"line"`` (all elements, rate from 20 GHz/s to 50 kHz/s).
            scan_range(tuple): tuple ``(start,stop)`` with the scan range (in Hz).
            rate(float): scan rate (in Hz/s).
            trunc_rate(bool): if ``True``, truncate the scan rate to the nearest available rate (otherwise, incorrect rate would raise an error).
        """
        self._check_terascan_type(scan_type)
        if trunc_rate:
            rate=self._trunc_terascan_rate(rate)
        if rate>=1E9:
            fact,units=1E9,"GHz/s"
        elif rate>=1E6:
            fact,units=1E6,"MHz/s"
        else:
            fact,units=1E3,"kHz/s"
        params={"scan":scan_type,"start":[c/scan_range[0]*1E9],"stop":[c/scan_range[1]*1E9],"rate":[rate/fact],"units":units}
        _,reply=self.query("scan_stitch_initialise",params)
        if reply["status"][0]==1:
            raise M2Error("can't setup TeraScan: start ({:.3f} THz) is out of range".format(scan_range[0]/1E12))
        elif reply["status"][0]==2:
            raise M2Error("can't setup TeraScan: stop ({:.3f} THz) is out of range".format(scan_range[1]/1E12))
        elif reply["status"][0]==3:
            raise M2Error("can't setup TeraScan: scan out of range")
        elif reply["status"][0]==4:
            raise M2Error("can't setup TeraScan: TeraScan not available")
    def start_terascan(self, scan_type, sync=False, sync_done=False):
        """
        Start terascan.

        Scan type can be ``"medium"`` (BRF+etalon, rate from 100 GHz/s to 1 GHz/s), ``"fine"`` (all elements, rate from 20 GHz/s to 1 MHz/s),
        or ``"line"`` (all elements, rate from 20 GHz/s to 50 kHz/s).
        If ``sync==True``, wait until the scan is set up (not until the whole scan is complete).
        If ``sync_done==True``, wait until the whole scan is complete.
        """
        self._check_terascan_type(scan_type)
        if sync:
            self.enable_terascan_updates()
        self.lock_wavemeter(False,error_on_fail=False)
        _,reply=self.query("scan_stitch_op",{"scan":scan_type,"operation":"start"},report=True)
        if reply["status"][0]==1:
            raise M2Error("can't start TeraScan: operation failed")
        elif reply["status"][0]==2:
            raise M2Error("can't start TeraScan: TeraScan not available")
        if sync:
            self.wait_for_terascan_update()
        if sync_done:
            self.wait_for_report("scan_stitch_op")
    def enable_terascan_updates(self, enable=True, update_period=0):
        """
        Enable sending periodic terascan updates.

        If enabled, laser will send updates in the beginning and in the end of every terascan segment.
        If ``update_period!=0``, it will also send updates every ``update_period`` percents of the segment (this option doesn't seem to be working currently).
        """
        _,reply=self.query("scan_stitch_output",{"operation":("start" if enable else "stop"),"update":[update_period]})
        if reply["status"][0]==1:
            raise M2Error("can't setup TeraScan updates: operation failed")
        if reply["status"][0]==2:
            raise M2Error("can't setup TeraScan updates: incorrect update rate")
        if reply["status"][0]==3:
            raise M2Error("can't setup TeraScan: TeraScan not available")
        self._last_status[self._terascan_update_op]=None
    def check_terascan_update(self):
        """
        Check the latest terascan update.

        Return ``None`` if none are available, or a dictionary ``{"wavelength":current_wavelength, "operation":op}``,
        where ``op`` is ``"scanning"`` (scanning in progress), ``"stitching"`` (stitching in progress), ``"finished"`` (scan is finished), or ``"repeat"`` (segment is repeated).
        """
        self.update_reports()
        rep=self._last_status.get(self._terascan_update_op,None)
        return rep
    def wait_for_terascan_update(self):
        """Wait until a new terascan update is available"""
        self.wait_for_report(self._terascan_update_op)
        return self.check_terascan_update()
    def check_terascan_report(self):
        """
        Check report on terascan start.

        Return ``"success"`` or ``"fail"`` if the operation is complete, or ``None`` if it is still in progress.
        """
        return self.check_report("scan_stitch_op")
    def stop_terascan(self, scan_type, sync=False):
        """
        Stop terascan of the given type.
        
        If ``sync==True``, wait until the operation is complete.
        """
        self._check_terascan_type(scan_type)
        _,reply=self.query("scan_stitch_op",{"scan":scan_type,"operation":"stop"},report=True)
        if reply["status"][0]==1:
            raise M2Error("can't stop TeraScan: operation failed")
        elif reply["status"][0]==2:
            raise M2Error("can't stop TeraScan: TeraScan not available")
        if sync:
            self.wait_for_report("scan_stitch_op")
    _web_scan_status_str=['off','cont','single','flyback','on','fail']
    def get_terascan_status(self, scan_type, web_status="auto"):
        """
        Get status of a terascan of a given type.

        Return dictionary with 4 items:
            ``"current"``: current laser frequency
            ``"range"``: tuple with the fill scan range
            ``"status"``: can be ``"stopped"`` (scan is not in progress), ``"scanning"`` (scan is in progress),
            or ``"stitching"`` (scan is in progress, but currently stitching)
            ``"web"``: where scan is running in web interface (some failure modes still report ``"scanning"`` through the usual interface);
            only available if the laser web connection is on.
        """
        self._check_terascan_type(scan_type)
        _,reply=self.query("scan_stitch_status",{"scan":scan_type})
        status={}
        if reply["status"][0]==0:
            status["status"]="stopped"
            status["range"]=None
        elif reply["status"][0]==1:
            if reply["operation"][0]==0:
                status["status"]="stitching"
            elif reply["operation"][0]==1:
                status["status"]="scanning"
            status["range"]=c/(reply["start"][0]/1E9),c/(reply["stop"][0]/1E9)
            status["current"]=c/(reply["current"][0]/1E9) if reply["current"][0] else 0
        elif reply["status"][0]==2:
            raise M2Error("can't stop TeraScan: TeraScan not available")
        if web_status=="auto":
            web_status=self.use_websocket
        if web_status:
            scan_web_status=self._read_websocket_status(present_key="scan_status")
            status["web"]=self._web_scan_status_str[scan_web_status["scan_status"]]
        else:
            status["web"]=None
        return status

    _fast_scan_types={"cavity_continuous","cavity_single","cavity_triangular",
                "etalon_continuous","etalon_single",
                "resonator_continuous","resonator_single","resonator_ramp","resonator_triangular",
                "ecd_continuous","ecd_ramp",
                "fringe_test"}
    def _check_fast_scan_type(self, scan_type):
        if scan_type not in self._fast_scan_types:
            raise M2Error("unknown fast scan type: {}".format(scan_type))
    def start_fast_scan(self, scan_type, width, time, sync=False, setup_locks=True):
        """
        Setup and start fast scan.

        Args:
            scan_type(str): scan type. Can be ``"cavity_continuous"``, ``"cavity_single"``, ``"cavity_triangular"``,
                ``"etalon_continuous"``, ``"etalon_single"``, 
                ``"resonator_continuous"``, ``"resonator_single"``, ``"resonator_ramp"``, ``"resonator_triangular"``,
                ``"ecd_continuous"``, ``"ecd_ramp"``, or ``"fringe_test"`` (see ICE manual for details)
            width(float): scan width (in Hz).
            time(float): scan time/period (in s).
            sync(bool): if ``True``, wait until the scan is set up (not until the whole scan is complete).
            setup_locks(bool): if ``True``, automatically setup etalon and reference cavity locks in the appropriate states.
        """
        self._check_fast_scan_type(scan_type)
        if setup_locks:
            if scan_type.startswith("cavity"):
                self.lock_etalon()
                self.lock_reference_cavity()
            elif scan_type.startswith("resonator"):
                self.lock_etalon()
                self.unlock_reference_cavity()
            elif scan_type.startswith("etalon"):
                self.unlock_etalon()
                self.unlock_reference_cavity()
            self.lock_wavemeter(False,error_on_fail=False)
        _,reply=self.query("fast_scan_start",{"scan":scan_type,"width":[width/1E9],"time":[time]},report=True)
        if reply["status"][0]==1:
            raise M2Error("can't start fast scan: width too great for the current tuning position")
        elif reply["status"][0]==2:
            raise M2Error("can't start fast scan: reference cavity not fitted")
        elif reply["status"][0]==3:
            raise M2Error("can't start fast scan: ERC not fitted")
        elif reply["status"][0]==4:
            raise M2Error("can't start fast scan: invalid scan type")
        elif reply["status"][0]==5:
            raise M2Error("can't start fast scan: time >10000 seconds")
        if sync:
            self.wait_for_report("fast_scan_start")
    def check_fast_scan_report(self):
        """
        Check fast scan report.

        Return ``"success"`` or ``"fail"`` if the operation is complete, or ``None`` if it is still in progress.
        """
        return self.check_report("fast_scan_start")
    def stop_fast_scan(self, scan_type, return_to_start=True, sync=False):
        """
        Stop fast scan of the given type.
        
        If ``return_to_start==True``, return to the center frequency after stopping; otherwise, stay at the current instantaneous frequency.
        If ``sync==True``, wait until the operation is complete.
        """
        self._check_fast_scan_type(scan_type)
        _,reply=self.query("fast_scan_stop" if return_to_start else "fast_scan_stop_nr",{"scan":scan_type})
        if reply["status"][0]==1:
            raise M2Error("can't stop fast scan: operation failed")
        elif reply["status"][0]==2:
            raise M2Error("can't stop fast scan: reference cavity not fitted")
        elif reply["status"][0]==3:
            raise M2Error("can't stop fast scan: ERC not fitted")
        elif reply["status"][0]==4:
            raise M2Error("can't stop fast scan: invalid scan type")
        if sync:
            self.wait_for_report("fast_scan_stop")
    def get_fast_scan_status(self, scan_type):
        """
        Get status of a fast scan of a given type.

        Return dictionary with 4 items:
            ``"status"``: can be ``"stopped"`` (scan is not in progress), ``"scanning"`` (scan is in progress).
            ``"value"``: current tuner value (in percent).
        """
        self._check_fast_scan_type(scan_type)
        _,reply=self.query("fast_scan_poll",{"scan":scan_type})
        status={}
        if reply["status"][0]==0:
            status["status"]="stopped"
        elif reply["status"][0]==1:
            status["status"]="scanning"
        elif reply["status"][0]==2:
            raise M2Error("can't poll fast scan: reference cavity not fitted")
        elif reply["status"][0]==3:
            raise M2Error("can't poll fast scan: ERC not fitted")
        elif reply["status"][0]==4:
            raise M2Error("can't poll fast scan: invalid scan type")
        else:
            raise M2Error("can't determine fast scan status: {}".format(reply["status"][0]))
        status["value"]=reply["tuner_value"][0]
        return status


    def stop_scan_web(self, scan_type):
        """
        Stop scan of the current type (terascan or fine scan) using web interface.

        More reliable than native programming interface, but requires activated web interface.
        """
        if not self.use_websocket:
            return
        try:
            self._check_terascan_type(scan_type)
            scan_type=scan_type.replace("line","narrow")
            scan_type=scan_type+"_scan"
            terascan=True
        except M2Error:
            self._check_fast_scan_type(scan_type)
            scan_type=scan_type.replace("continuous","cont")
            terascan=False
        scan_task=scan_type+"_stop"
        if terascan:
            self._send_websocket_request('{"message_type":"page_update", "stop_scan_stitching":1}')
        self._send_websocket_request('{{"message_type":"task_request","task":["{}"]}}'.format(scan_task))
    _default_terascan_rates={"line":10E6,"fine":100E6,"medium":5E9}
    def stop_all_operation(self, repeated=True, attempt=0):
        """
        Stop all laser operations (tuning and scanning).

        More reliable than native programming interface, but requires activated web interface.
        If ``repeated==True``, repeat trying to stop the operations until succeeded (more reliable, but takes more time).
        Return ``True`` if the operation is success otherwise ``False``.
        """
        ctd=general.Countdown(self.timeout or None)
        while True:
            operating=False
            if not (self.use_websocket and self.get_full_web_status()["scan_status"]==0):
                for scan_type in ["medium","fine","line"]:
                    stat=self.get_terascan_status(scan_type,web_status=False)
                    if stat["status"]!="stopped":
                        operating=True
                        self.stop_terascan(scan_type)
                        time.sleep(1)
                        if attempt>2:
                            self.stop_scan_web(scan_type)
                        if attempt>4 and attempt%2==1:
                            try:
                                self.start_fast_scan("resonator_single",1E9,2,sync=True)
                                time.sleep(6.)
                            except M2Error:
                                pass
                            try:
                                self.start_fast_scan("cavity_single",1E9,2,sync=True)
                                time.sleep(6.)
                            except M2Error:
                                pass
                            rate=self._default_terascan_rates[scan_type]
                            scan_center=(stat["current"] or 400E12)-(attempt-5)*100E9
                            self.setup_terascan(scan_type,(scan_center,scan_center+100E9),rate)
                            self.start_terascan(scan_type)
                            time.sleep(2.)
                            self.stop_terascan(scan_type)
                            self.stop_scan_web(scan_type)
                            time.sleep(2.)
                        if attempt>6 and attempt%2==0 and self.use_websocket:
                            self._try_disconnect_wavemeter()
                            time.sleep(4.)
                            self._try_connect_wavemeter()
                            time.sleep(4.)
                for scan_type in self._fast_scan_types:
                    try:
                        if self.get_fast_scan_status(scan_type)["status"]!="stopped":
                            operating=True
                            self.stop_fast_scan(scan_type)
                            time.sleep(0.5)
                            if attempt>2:
                                self.stop_scan_web(scan_type)
                            if attempt>6 and attempt%2==0 and self.use_websocket:
                                self._try_disconnect_wavemeter()
                                time.sleep(4.)
                                self._try_connect_wavemeter()
                                time.sleep(4.)
                    except M2Error:
                        pass
            if self.get_tuning_status()=="tuning":
                operating=True
                self.stop_tuning()
            if self.get_tuning_status_table()=="tuning":
                operating=True
                self.stop_tuning_table()
            if (not repeated) or (not operating):
                break
            time.sleep(0.1)
            attempt+=1
            if (attempt>12 and ctd.passed()):
                raise M2Error("coudn't stop all operations: timed out")
        return not operating