from ...core.utils import general

try:
    import websocket
except ImportError:
    websocket=None

from .base import M2Error
from .base import ICEBlocDevice, c

import json
import time
import logging
import threading

def _check_websocket():
    if websocket is None:
        msg=(   "operation requires Python websocket-client library. You can install it via PyPi as 'pip install websocket-client'. "
                "If it is installed, check if it imports correctly by running 'import websocket'")
        raise ImportError(msg)


class Solstis(ICEBlocDevice):
    """
    M2 Solstis Ice Bloc device.

    Args:
        addr(str): IP address of the Ice Bloc device.
        port(int): port of the Ice Bloc device.
        timeout(float): default timeout of synchronous operations.
        start_link(bool): if ``True``, initialize device link on creation.
        use_websocket(bool): if ``True``, use websocket interface (same as used by the web interface) for additional functionality
            (wavemeter connection, etalon value, improved operation stopping);
            ``"auto"`` enables it if websocket package is installed, and disables otherwise
        use_cavity: if ``False`` and any reference cavity methods are used, either ignore them, or use closest available methods instead
    """
    def __init__(self, addr, port, timeout=5., start_link=True, use_websocket="auto", use_cavity=True):
        super().__init__(addr,port,timeout=timeout,start_link=start_link)
        self.use_websocket=(websocket is not None) if use_websocket=="auto" else use_websocket
        self._websocket_lock=threading.Lock()
        self.use_cavity=use_cavity
        self._add_status_variable("web_status",self.get_full_web_status)
        self._add_status_variable("system_status",self.get_system_status)
        self._add_status_variable("fine_tuning_status",self.get_full_fine_tuning_status)
        self._add_status_variable("coarse_tuning_status",self.get_full_coarse_tuning_status)
        self._add_settings_variable("wavemeter_connected",self.is_wavemeter_connected,lambda v: self.connect_wavemeter() if v else self.disconnect_wavemeter())
        self._add_settings_variable("etalon_lock",lambda: self.get_etalon_lock_status()=="on",
                lambda v: self.lock_etalon() if v else self.unlock_etalon())
        self._add_settings_variable("reference_cavity_lock",lambda: self.get_reference_cavity_lock_status()=="on",
                lambda v: self.lock_reference_cavity() if v else self.unlock_reference_cavity())
        self._add_settings_variable("wavemeter_lock",self.is_wavemeter_lock_on,self.lock_wavemeter)

    _terascan_update_op="wavelength"
    _extra_update_ops=(_terascan_update_op,)
    def _wait_for_websocket_status(self, ws, present_key=None, nmax=20):
        full_data={}
        for _ in range(nmax):
            data=ws.recv()
            full_data.update(json.loads(data))
            if present_key is None or present_key in data:
                return full_data
    def _send_websocket_request(self, msg):
        if self.use_websocket:
            _check_websocket()
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
                except (websocket.WebSocketTimeoutException, ConnectionResetError):
                    if t==4:
                        raise
                    time.sleep(5.)
        else:
            raise M2Error("websocket is required to communicate this request")
    def _read_websocket_status(self, present_key=None, nmax=20):
        if self.use_websocket:
            _check_websocket()
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
                except (websocket.WebSocketTimeoutException, ConnectionResetError):
                    if t==4:
                        raise
                    time.sleep(5.)
        else:
            raise M2Error("websocket is required to communicate this request")


    def _check_option(self, option):
        if option=="cavity":
            return self.use_cavity

    def _try_connect_wavemeter(self, sync=True):
        self._send_websocket_request('{"message_type":"task_request","task":["start_wavemeter_link"]}')
        if sync:
            while not self.is_wavemeter_connected():
                time.sleep(0.02)
    def connect_wavemeter(self, sync=True):
        """Connect to the wavemeter (if ``sync==True``, wait until the connection is established)"""
        if not self.use_websocket:
            return
        if self.is_wavemeter_connected():
            return
        self.stop_all_operation()
        self._try_connect_wavemeter(sync=sync)
    def _try_disconnect_wavemeter(self, sync=True):
        self._send_websocket_request('{"message_type":"task_request","task":["job_stop_wavemeter_link"]}')
        if sync:
            for _ in range(25):
                if not self.is_wavemeter_connected():
                    return
                time.sleep(0.02)
    def disconnect_wavemeter(self, sync=True):
        """Disconnect from the wavemeter (if ``sync==True``, wait until the connection is broken)"""
        if not self.use_websocket:
            return
        if not self.is_wavemeter_connected():
            return
        if not sync:
            self._try_disconnect_wavemeter(sync=False)
        else:
            while self.is_wavemeter_connected():
                self.stop_all_operation()
                self.lock_wavemeter(False)
                if self.is_wavemeter_lock_on():
                    time.sleep(1.)
                self._try_disconnect_wavemeter(sync=True)
    def is_wavemeter_connected(self):
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
    



    def get_full_fine_tuning_status(self):
        """Get full fine-tuning status (see M2 Solstis JSON protocol manual for ``"poll_wave_m"`` command)"""
        return self.query("poll_wave_m",{})[1]
    def lock_wavemeter(self, lock=True, sync=True, error_on_fail=True):
        """Lock or unlock the laser to the wavemeter (if ``sync==True``, wait until the operation is complete)"""
        _,reply=self.query("lock_wave_m",{"operation":"on" if lock else "off"})
        if reply["status"][0]==1:
            if error_on_fail:
                raise M2Error("could not lock wavemeter: no wavemeter link")
            else:
                return
        if sync:
            while self.is_wavemeter_lock_on()!=lock:
                time.sleep(0.05)
    def is_wavemeter_lock_on(self):
        """Check if the laser is locked to the wavemeter"""
        return bool(self.get_full_fine_tuning_status()["lock_status"][0])
    def fine_tune_wavelength(self, wavelength, sync=True, timeout=None):
        """
        Fine-tune the wavelength.
        
        Only works if the wavemeter is connected.
        If ``sync==True``, wait until the operation is complete (might take from several seconds up to several minutes).
        """
        _,reply=self.query("set_wave_m",{"wavelength":[wavelength*1E9]},report=True)
        if reply["status"][0]==1:
            raise M2Error("could not fine-tune wavelength: no wavemeter link")
        elif reply["status"][0]==2:
            raise M2Error("could not fine-tune wavelength: {:.3f}nm is out of range".format(wavelength*1E9))
        if sync:
            self.wait_for_fine_tuning(timeout=timeout)
    def check_fine_tuning_report(self):
        """
        Check wavelength fine-tuning report

        Return ``"success"`` or ``"fail"`` if the operation is complete, or ``None`` if it is still in progress.
        """
        return self.check_report("set_wave_m")
    def wait_for_fine_tuning(self, timeout=None):
        """Wait until wavelength fine-tuning is complete"""
        self.wait_for_report("set_wave_m",timeout=timeout)
    _fine_tuning_status=["idle","nolink","tuning","locked"]
    def get_fine_tuning_status(self):
        """
        Get fine-tuning status.

        Return either ``"idle"`` (no tuning or locking), ``"nolink"`` (no wavemeter link),
        ``"tuning"`` (tuning in progress), or ``"locked"`` (tuned and locked to the wavemeter).
        """
        status=self.get_full_fine_tuning_status()["status"][0]
        return self._fine_tuning_status[status]
    def get_fine_wavelength(self):
        """
        Get fine-tuned wavelength.
        
        Only works if the wavemeter is connected.
        """
        return self.get_full_fine_tuning_status()["current_wavelength"][0]*1E-9
    def stop_fine_tuning(self):
        """Stop fine wavelength tuning"""
        _,reply=self.query("stop_wave_m",{})
        if reply["status"][0]==1:
            raise M2Error("could not stop tuning: no wavemeter link")



    def coarse_tune_wavelength(self, wavelength, sync=True):
        """
        Coarse-tune the wavelength.
        
        Only works if the wavemeter is disconnected.
        If ``sync==True``, wait until the operation is complete.
        """
        _,reply=self.query("move_wave_t",{"wavelength":[wavelength*1E9]},report=True)
        if reply["status"][0]==1:
            raise M2Error("could not coarse-tune wavelength: command failed")
        elif reply["status"][0]==2:
            raise M2Error("could not coarse-tune wavelength: {}nm is out of range".format(wavelength*1E9))
        if sync:
            self.wait_for_report("move_wave_t")
    def get_full_coarse_tuning_status(self):
        """Get full coarse-tuning status (see M2 M2 Solstis JSON protocol manual for ``"poll_move_wave_t"`` command)"""
        return self.query("poll_move_wave_t",{})[1]
    _coarse_tuning_status=["done","tuning","fail"]
    def get_coarse_tuning_status(self):
        """
        Get coarse-tuning status.

        Return either ``"done"`` (tuning is done), ``"tuning"`` (tuning in progress), or ``"fail"`` (tuning failed).
        """
        status=self.get_full_coarse_tuning_status()["status"][0]
        return self._coarse_tuning_status[status]
    def get_coarse_wavelength(self):
        """
        Get course-tuned wavelength.
        
        Only works if the wavemeter is disconnected.
        """
        return self.get_full_coarse_tuning_status()["current_wavelength"][0]*1E-9
    def stop_coarse_tuning(self):
        """Stop coarse wavelength tuning"""
        self.query("stop_move_wave_t",{})



    def tune_etalon(self, value, sync=True):
        """
        Tune the etalon to `value` percent.
        
        Only works if the wavemeter is disconnected.
        If ``sync==True``, wait until the operation is complete.
        """
        _,reply=self.query("tune_etalon",{"setting":[value]},report=True)
        if reply["status"][0]==1:
            raise M2Error("could not tune etalon: {} is out of range".format(value))
        elif reply["status"][0]==2:
            raise M2Error("could not tune etalon: command failed")
        if sync:
            self.wait_for_report("tune_etalon")
    def lock_etalon(self, sync=True):
        """
        Lock the etalon.
        
        If ``sync==True``, wait until the operation is complete.
        """
        if self.get_etalon_lock_status()=="on":
            return
        _,reply=self.query("etalon_lock",{"operation":"on"},report=True)
        if reply["status"][0]==1:
            raise M2Error("could not lock etalon")
        if sync:
            self.wait_for_report("etalon_lock")
    def unlock_etalon(self, sync=True):
        """
        Unlock the etalon .
        
        If ``sync==True``, wait until the operation is complete.
        Automatically unlock the reference cavity first (otherwise the operation fails).
        """
        if self.get_etalon_lock_status()=="off":
            return
        self.unlock_reference_cavity(sync=True)
        _,reply=self.query("etalon_lock",{"operation":"off"},report=True)
        if reply["status"][0]==1:
            raise M2Error("could not unlock etalon")
        if sync:
            self.wait_for_report("etalon_lock")
    def get_etalon_lock_status(self):
        """
        Get etalon lock status.

        Return either ``"off"`` (lock is off), ``"on"`` (lock is on), ``"debug"`` (lock in debug condition),
        ``"error"`` (lock had an error), ``"search"`` (lock is searching), or ``"low"`` (lock is off due to low output).
        """
        _,reply=self.query("etalon_lock_status",{})
        if reply["status"][0]==1:
            raise M2Error("could not get etalon status")
        return reply["condition"]



    def tune_laser_resonator(self, value, fine=False, sync=True):
        """
        Tune the laser cavity to `value` percent.
        
        If ``fine==True``, adjust fine tuning; otherwise, adjust coarse tuning.
        Only works if the wavemeter is disconnected.
        If ``sync==True``, wait until the operation is complete.
        """
        op_name="fine_tune_resonator" if fine else "tune_resonator"
        op_pfx="fine" if fine else "coarse"
        _,reply=self.query(op_name,{"setting":[value]},report=True)
        if reply["status"][0]==1:
            raise M2Error("could not {}-tune resonator: {} is out of range".format(op_pfx,value))
        elif reply["status"][0]==2:
            raise M2Error("could not {}-tune resonator: command failed".format(op_pfx))
        if sync:
            self.wait_for_report(op_name)



    def tune_reference_cavity(self, value, fine=False, sync=True):
        """
        Tune the reference cavity to `value` percent.
        
        If ``fine==True``, adjust fine tuning; otherwise, adjust coarse tuning.
        Only works if the wavemeter is disconnected.
        If ``sync==True``, wait until the operation is complete.
        If reference cavity is disabled by setting ``use_cavity=False`` on creation, do nothing.
        """
        if not self._check_option("cavity"):
            return
        op_name="fine_tune_cavity" if fine else "tune_cavity"
        op_pfx="fine" if fine else "coarse"
        _,reply=self.query(op_name,{"setting":[value]},report=True)
        if reply["status"][0]==1:
            raise M2Error("could not {}-tune reference cavity: {} is out of range".format(op_pfx,value))
        elif reply["status"][0]==2:
            raise M2Error("could not {}-tune reference cavity: command failed".format(op_pfx))
        if sync:
            self.wait_for_report(op_name)
    def lock_reference_cavity(self, sync=True):
        """
        Lock the laser to the reference cavity.
        
        Automatically lock etalon first (otherwise the operation fails).
        If ``sync==True``, wait until the operation is complete.
        If reference cavity is disabled by setting ``use_cavity=False`` on creation, do nothing.
        """
        if not self._check_option("cavity"):
            return
        if self.get_reference_cavity_lock_status()=="on":
            return
        self.lock_etalon(sync=True)
        _,reply=self.query("cavity_lock",{"operation":"on"},report=True)
        if reply["status"][0]==1:
            raise M2Error("could not lock reference cavity")
        if sync:
            self.wait_for_report("cavity_lock")
    def unlock_reference_cavity(self, sync=True):
        """
        Unlock the laser from the reference cavity.
        
        If ``sync==True``, wait until the operation is complete.
        If reference cavity is disabled by setting ``use_cavity=False`` on creation, do nothing.
        """
        if not self._check_option("cavity"):
            return
        if self.get_reference_cavity_lock_status()=="off":
            return
        _,reply=self.query("cavity_lock",{"operation":"off"},report=True)
        if reply["status"][0]==1:
            raise M2Error("could not unlock reference cavity")
        if sync:
            self.wait_for_report("cavity_lock")
    def get_reference_cavity_lock_status(self):
        """
        Get the reference cavity lock status.
        
        Return either ``"off"`` (lock is off), ``"on"`` (lock is on), ``"debug"`` (lock in debug condition),
        ``"error"`` (lock had an error), ``"search"`` (lock is searching), ``"low"`` (lock is off due to low output),
        or ``"disabled"`` (reference cavity is disabled by setting ``use_cavity=False`` on creation).
        """
        if not self._check_option("cavity"):
            return "disabled"
        _,reply=self.query("cavity_lock_status",{})
        if reply["status"][0]==1:
            raise M2Error("could not get etalon status")
        return reply["condition"]

    

    def _check_terascan_type(self, scan_type):
        if scan_type not in {"coarse","medium","fine","line"}:
            raise M2Error("unknown terascan type: {}".format(scan_type))
        if scan_type=="coarse":
            raise M2Error("coarse scan is not currently supported by the M2 firmware")
        if scan_type=="line" and not self._check_option("cavity"):
            return "fine"
        return scan_type
    _terascan_rates=[                         50E3,100E3,200E3,500E3,
                        1E6,2E6,5E6,10E6,20E6,50E6,100E6,200E6,500E6,
                        1E9,2E9,5E9,10E9,20E9,50E9,100E9 ]
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
            scan_range(tuple): tuple ``(start, stop)`` with the scan range (in Hz).
            rate(float): scan rate (in Hz/s).
            trunc_rate(bool): if ``True``, truncate the scan rate to the nearest available rate (otherwise, incorrect rate would raise an error).

        If reference cavity is disabled by setting ``use_cavity=False`` on creation and `scan_type` is ``"line"``, use ``"fine"`` instead.
        """
        scan_type=self._check_terascan_type(scan_type)
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
            raise M2Error("could not setup TeraScan: start ({:.3f} THz) is out of range".format(scan_range[0]/1E12))
        elif reply["status"][0]==2:
            raise M2Error("could not setup TeraScan: stop ({:.3f} THz) is out of range".format(scan_range[1]/1E12))
        elif reply["status"][0]==3:
            raise M2Error("could not setup TeraScan: scan out of range")
        elif reply["status"][0]==4:
            raise M2Error("could not setup TeraScan: TeraScan not available")
    def start_terascan(self, scan_type, sync=False, sync_done=False):
        """
        Start terascan.

        Scan parameters are set up separately using :meth:`setup_terascan`.
        Scan type can be ``"medium"`` (BRF+etalon, rate from 100 GHz/s to 1 GHz/s),
        ``"fine"`` (all elements, rate from 20 GHz/s to 1 MHz/s), or ``"line"`` (all elements, rate from 20 GHz/s to 50 kHz/s).
        If reference cavity is disabled by setting ``use_cavity=False`` on creation and `scan_type` is ``"line"``, use ``"fine"`` instead.
        If ``sync==True``, wait until the scan is set up (not until the whole scan is complete).
        If ``sync_done==True``, wait until the whole scan is complete (not recommended, as it can take hours).
        """
        scan_type=self._check_terascan_type(scan_type)
        if sync:
            self.enable_terascan_updates()
        self.lock_wavemeter(False,error_on_fail=False)
        _,reply=self.query("scan_stitch_op",{"scan":scan_type,"operation":"start"},report=True)
        if reply["status"][0]==1:
            raise M2Error("could not start TeraScan: operation failed")
        elif reply["status"][0]==2:
            raise M2Error("could not start TeraScan: TeraScan not available")
        if sync:
            self.wait_for_terascan_update()
        if sync_done:
            self.wait_for_report("scan_stitch_op")
    def enable_terascan_updates(self, enable=True, update_period=0):
        """
        Enable sending periodic terascan updates.

        If enabled, laser will send updates in the beginning and in the end of every terascan segment.
        If ``update_period!=0``, it will also send updates every ``update_period`` percents of the segment (this option is not currently supported by M2 firmware).
        """
        _,reply=self.query("scan_stitch_output",{"operation":("start" if enable else "stop"),"update":[update_period]})
        if reply["status"][0]==1:
            raise M2Error("could not setup TeraScan updates: operation failed")
        if reply["status"][0]==2:
            raise M2Error("could not setup TeraScan updates: incorrect update rate")
        if reply["status"][0]==3:
            raise M2Error("could not setup TeraScan updates: TeraScan not available")
        self._last_status[self._terascan_update_op]=None
    def check_terascan_update(self):
        """
        Check the latest terascan update.

        Return ``None`` if none are available, or a dictionary ``{"wavelength":current_wavelength, "activity":op}``,
        where ``op`` is ``"scanning"`` (scanning in progress), ``"stitching"`` (stitching in progress), ``"finished"`` (scan is finished), or ``"repeat"`` (segment is repeated).
        """
        self.update_reports()
        rep=self._last_status.get(self._terascan_update_op,None)
        return rep
    def wait_for_terascan_update(self):
        """Wait until a new terascan update is available"""
        self.wait_for_report(self._terascan_update_op)
        return self.check_terascan_update()
    def check_terascan_start_report(self):
        """
        Check report on terascan start.

        Return ``"success"`` or ``"fail"`` if the operation is complete, or ``None`` if it is still in progress.
        """
        return self.check_report("scan_stitch_op")
    def stop_terascan(self, scan_type, sync=False):
        """
        Stop terascan of the given type.
        
        If reference cavity is disabled by setting ``use_cavity=False`` on creation and `scan_type` is ``"line"``, use ``"fine"`` instead.
        If ``sync==True``, wait until the operation is complete.
        """
        scan_type=self._check_terascan_type(scan_type)
        _,reply=self.query("scan_stitch_op",{"scan":scan_type,"operation":"stop"},report=True)
        if reply["status"][0]==1:
            raise M2Error("could not stop TeraScan: operation failed")
        elif reply["status"][0]==2:
            raise M2Error("could not stop TeraScan: TeraScan not available")
        if sync:
            self.wait_for_report("scan_stitch_op")
    _terascan_status=["off","cont","single","flyback","on","fail"]
    def get_terascan_status(self, scan_type, web_status=True):
        """
        Get status of a terascan of a given type.

        Return a dictionary with 4 items:
            ``"current"``: current laser frequency (or ``None`` if no scan is in progress)
            ``"range"``: tuple with the fill scan range (or ``None`` if no frequency is available)
            ``"status"``: can be ``"stopped"`` (scan is not in progress), ``"scanning"`` (scan is in progress),
            or ``"stitching"`` (scan is in progress, but currently stitching)
            ``"web"``: whether scan is running in web interface (some failure modes still report ``"scanning"`` through the usual interface);
            only available if the laser web connection is on and if ``web_status==True``.
        
        If reference cavity is disabled by setting ``use_cavity=False`` on creation and `scan_type` is ``"line"``, use ``"fine"`` instead.
        """
        scan_type=self._check_terascan_type(scan_type)
        _,reply=self.query("scan_stitch_status",{"scan":scan_type})
        status={}
        if reply["status"][0]==0:
            status["status"]="stopped"
            status["range"]=None
            status["current"]=None
        elif reply["status"][0]==1:
            if reply["operation"][0]==0:
                status["status"]="stitching"
            elif reply["operation"][0]==1:
                status["status"]="scanning"
            status["range"]=c/(reply["start"][0]/1E9),c/(reply["stop"][0]/1E9)
            status["current"]=c/(reply["current"][0]/1E9) if reply["current"][0] else None
        elif reply["status"][0]==2:
            raise M2Error("could not get TeraScan status: TeraScan not available")
        if web_status and self.use_websocket:
            scan_web_status=self._read_websocket_status(present_key="scan_status")
            status["web"]=self._terascan_status[scan_web_status["scan_status"]]
        else:
            status["web"]=None
        return status



    _fast_scan_types={  "cavity_continuous","cavity_single","cavity_triangular",
                        "etalon_continuous","etalon_single",
                        "resonator_continuous","resonator_single","resonator_ramp","resonator_triangular",
                        "ecd_continuous","ecd_ramp",
                        "fringe_test"}
    _cavity_scan_substitutes={  "cavity_continuous":"resonator_continuous",
                                "cavity_single":"resonator_single",
                                "cavity_triangular":"resonator_triangular"}
    def _check_fast_scan_type(self, scan_type):
        if scan_type not in self._fast_scan_types:
            raise M2Error("unknown fast scan type: {}".format(scan_type))
        if scan_type in self._cavity_scan_substitutes and not self._check_option("cavity"):
            return self._cavity_scan_substitutes[scan_type]
        return scan_type
    def start_fast_scan(self, scan_type, width, period, sync=False, setup_locks=True):
        """
        Setup and start fast scan.

        Args:
            scan_type(str): scan type. Can be ``"cavity_continuous"``, ``"cavity_single"``, ``"cavity_triangular"``,
                ``"etalon_continuous"``, ``"etalon_single"``, 
                ``"resonator_continuous"``, ``"resonator_single"``, ``"resonator_ramp"``, ``"resonator_triangular"``,
                ``"ecd_continuous"``, ``"ecd_ramp"``, or ``"fringe_test"`` (see M2 Solstis JSON protocol manual for details)
            width(float): scan width (in Hz).
            period(float): scan time/period (in s).
            sync(bool): if ``True``, wait until the scan is set up (not until the whole scan is complete).
            setup_locks(bool): if ``True``, automatically setup etalon and reference cavity locks in the appropriate states for etalon, cavity, or resonator scans.
        
        If reference cavity is disabled by setting ``use_cavity=False`` on creation, use resonator scans instead of cavity scans.
        """
        scan_type=self._check_fast_scan_type(scan_type)
        if setup_locks:
            if scan_type.startswith("cavity"):
                self.lock_etalon()
                self.lock_reference_cavity()
            elif scan_type.startswith("resonator"):
                self.lock_etalon()
                self.unlock_reference_cavity()
            elif scan_type.startswith("etalon"):
                self.unlock_reference_cavity()
                self.unlock_etalon()
            self.lock_wavemeter(False,error_on_fail=False)
        _,reply=self.query("fast_scan_start",{"scan":scan_type,"width":[width/1E9],"time":[period]},report=True)
        if reply["status"][0]==1:
            raise M2Error("could not start fast scan: width too great for the current tuning position")
        elif reply["status"][0]==2:
            raise M2Error("could not start fast scan: reference cavity not fitted")
        elif reply["status"][0]==3:
            raise M2Error("could not start fast scan: ERC not fitted")
        elif reply["status"][0]==4:
            raise M2Error("could not start fast scan: invalid scan type")
        elif reply["status"][0]==5:
            raise M2Error("could not start fast scan: time >10000 seconds")
        if sync:
            self.wait_for_report("fast_scan_start")
    def check_fast_scan_start_report(self):
        """
        Check fast scan start report.

        Return ``"success"`` or ``"fail"`` if the operation is complete, or ``None`` if it is still in progress.
        """
        return self.check_report("fast_scan_start")
    def stop_fast_scan(self, scan_type, return_to_start=True, sync=False):
        """
        Stop fast scan of the given type.
        
        If reference cavity is disabled by setting ``use_cavity=False`` on creation, use resonator scans instead of cavity scans.
        If ``return_to_start==True``, return to the center frequency after stopping; otherwise, stay at the current instantaneous frequency.
        If ``sync==True``, wait until the operation is complete.
        """
        scan_type=self._check_fast_scan_type(scan_type)
        op_name="fast_scan_stop" if return_to_start else "fast_scan_stop_nr"
        _,reply=self.query(op_name,{"scan":scan_type})
        if reply["status"][0]==1:
            raise M2Error("could not stop fast scan: operation failed")
        elif reply["status"][0]==2:
            raise M2Error("could not stop fast scan: reference cavity not fitted")
        elif reply["status"][0]==3:
            raise M2Error("could not stop fast scan: ERC not fitted")
        elif reply["status"][0]==4:
            raise M2Error("could not stop fast scan: invalid scan type")
        if sync:
            self.wait_for_report(op_name)
    def get_fast_scan_status(self, scan_type):
        """
        Get status of a fast scan of a given type.

        Return dictionary with 2 items:
            ``"status"``: can be ``"stopped"`` (scan is not in progress), ``"scanning"`` (scan is in progress).
            ``"value"``: current tuner value (in percent); does not necessary correspond to the scan progress.
        
        If reference cavity is disabled by setting ``use_cavity=False`` on creation, use resonator scans instead of cavity scans.
        """
        scan_type=self._check_fast_scan_type(scan_type)
        _,reply=self.query("fast_scan_poll",{"scan":scan_type})
        status={}
        if reply["status"][0]==0:
            status["status"]="stopped"
        elif reply["status"][0]==1:
            status["status"]="scanning"
        elif reply["status"][0]==2:
            raise M2Error("error polling fast scan: reference cavity not fitted")
        elif reply["status"][0]==3:
            raise M2Error("error polling fast scan: ERC not fitted")
        elif reply["status"][0]==4:
            raise M2Error("error polling fast scan: invalid scan type")
        else:
            raise M2Error("could not determine fast scan status: {}".format(reply["status"][0]))
        status["value"]=reply["tuner_value"][0]
        return status


    def stop_scan_web(self, scan_type):
        """
        Stop scan of the current type (terascan or fine scan) using web interface.

        More reliable than native programming interface, but requires activated web interface.
        If reference cavity is disabled by setting ``use_cavity=False`` on creation, use resonator scans instead of cavity scans.
        """
        if not self.use_websocket:
            return
        try:
            scan_type=self._check_terascan_type(scan_type)
            scan_type=scan_type.replace("line","narrow")
            scan_type=scan_type+"_scan"
            terascan=True
        except M2Error:
            scan_type=self._check_fast_scan_type(scan_type)
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
        If ``attempt>0``, it can supply the number of already tried attempts to stop (with ``repeated=False``);
        the more attempts failed, the more drastic measures will be taken to stop (e.g., initialize short terascan or a fast scan, cycle wavemeter connection, etc.)
        Return ``True`` if the operation is success and ``False`` otherwise.
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
                        time.sleep(1.)
                        if attempt>2:
                            self.stop_scan_web(scan_type)
                        if attempt>4 and attempt%2==1:
                            try:
                                self.start_fast_scan("resonator_single",1E9,2,sync=True)
                                time.sleep(6.)
                            except M2Error:
                                pass
                            if self.use_cavity:
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
            if self.get_fine_tuning_status()=="tuning":
                operating=True
                self.stop_fine_tuning()
            if self.get_coarse_tuning_status()=="tuning":
                operating=True
                self.stop_coarse_tuning()
            if (not repeated) or (not operating):
                break
            time.sleep(0.1)
            attempt+=1
            if (attempt>12 and ctd.passed()):
                raise M2Error("could not stop all operations: timed out")
        return not operating