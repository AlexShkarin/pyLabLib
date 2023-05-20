from ...core.utils import general, funcargparse

from .base import M2Error, M2ParseError
from .base import ICEBlocDevice, c

import time

class EMM(ICEBlocDevice):
    """
    M2 EMM Ice Bloc device.

    Args:
        addr(str): IP address of the Ice Bloc device.
        port(int): port of the Ice Bloc device.
        timeout(float): default timeout of synchronous operations.
        start_link(bool): if ``True``, initialize device link on creation.
    """
    def __init__(self, addr, port, timeout=5., start_link=True):
        super().__init__(addr,port,timeout=timeout,start_link=start_link)
        self._add_status_variable("laser_status",self.get_laser_status)
        self._add_status_variable("terascan_status",lambda: self.get_terascan_status("all"))

    _terascan_update_op="automatic_output"
    _extra_update_ops=(_terascan_update_op,)
    def get_laser_status(self):
        """Get the device system status"""
        _,reply=self.query("status",{})
        for k in reply:
            if isinstance(reply[k],list):
                reply[k]=reply[k][0]
        return reply
    



    def fine_tune_wavelength(self, wavelength, beam="visible", sync=True, timeout=None):
        """
        Fine-tune the wavelength.
        
        If ``sync==True``, wait until the operation is complete (might take from several seconds up to several minutes).
        """
        funcargparse.check_parameter_range(beam,"beam",["visible","infrared"],error_type=M2Error)
        _,reply=self.query("wavelength",{"target":[wavelength*1E9],"beam":beam},report=True)
        if reply["status"][0]==1:
            raise M2Error("could not fine-tune wavelength: {:.3f}nm is out of range".format(wavelength*1E9))
        if sync:
            self.wait_for_fine_tuning(timeout=timeout)
    def check_fine_tuning_report(self):
        """
        Check wavelength fine-tuning report

        Return ``"success"`` or ``"fail"`` if the operation is complete, or ``None`` if it is still in progress.
        """
        return self.check_report("wavelength")
    def wait_for_fine_tuning(self, timeout=None):
        """Wait until wavelength fine-tuning is complete"""
        self.wait_for_report("wavelength",timeout=timeout)
    def is_fine_tuning(self):
        """check if fine tuning is in progress"""
        return self.get_laser_status().get("tuning","idle")=="active"
    _fine_tuning_status=["idle","nolink","tuning","locked"]
    def get_fine_tuning_status(self):
        """
        Get fine-tuning status.

        Return either ``"idle"`` (no tuning or locking) or ``"active"`` (tuning in progress).
        """
        return self.get_laser_status().get("tuning","idle")
    def get_fine_wavelength(self):
        """Get fine-tuned wavelength"""
        return self.get_laser_status()["wavelength"]*1E-9
    def stop_fine_tuning(self):
        """Stop fine wavelength tuning"""
        self.query("wavelength_stop",{})


    _terascan_kinds={"medium","fine","ir_medium","ir_fine"}
    def _check_terascan_type(self, scan_type):
        funcargparse.check_parameter_range(scan_type,"scan_type",self._terascan_kinds,error_type=M2Error)
        return scan_type
    _terascan_rates=[   1E6,2E6,5E6,10E6,20E6,50E6,100E6,200E6,500E6,
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
                ``"fine"`` (all elements, rate from 20 GHz/s to 1 MHz/s), ``"ir_medium"`` or ``"ir_fine"`` (same as ``"medium"`` or ``"fine"``, but defined for the IR laser)
            scan_range(tuple): tuple ``(start, stop)`` with the scan range (in Hz).
            rate(float): scan rate (in Hz/s).
            trunc_rate(bool): if ``True``, truncate the scan rate to the nearest available rate (otherwise, incorrect rate would raise an error).
        """
        scan_type=self._check_terascan_type(scan_type)
        if trunc_rate:
            rate=self._trunc_terascan_rate(rate)
        if rate>=1E9:
            fact,units=1E9,"GHz/s"
        else:
            fact,units=1E6,"MHz/s"
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
    _terascan_update_reps=(5,0.5)
    def start_terascan(self, scan_type, sync=False, sync_done=False):
        """
        Start terascan.

        Scan parameters are set up separately using :meth:`setup_terascan`.
        Scan type can be ``"medium"`` (BRF+etalon, rate from 100 GHz/s to 1 GHz/s), ``"fine"`` (all elements, rate from 20 GHz/s to 1 MHz/s),
        ``"ir_medium"`` or ``"ir_fine"`` (same as ``"medium"`` or ``"fine"``, but defined for the IR laser)
        If ``sync==True``, wait until the scan is set up (not until the whole scan is complete).
        If ``sync_done==True``, wait until the whole scan is complete (not recommended, as it can take hours).
        """
        scan_type=self._check_terascan_type(scan_type)
        if sync:
            self.enable_terascan_updates()
        _,reply=self.query("scan_stitch_op",{"scan":scan_type,"operation":"start"},report=True)
        if sync:
            for _ in range(self._terascan_update_reps[0]):
                self.enable_terascan_updates()
                time.sleep(self._terascan_update_reps[1])
        if reply["status"][0]==1:
            raise M2Error("could not start TeraScan: operation failed")
        elif reply["status"][0]==2:
            raise M2Error("could not start TeraScan: TeraScan not available")
        if sync:
            self.wait_for_terascan_update()
        if sync_done:
            self.wait_for_report("scan_stitch_op")
    def enable_terascan_updates(self, enable=True, update_period=1E-2, update_delay=0):
        """
        Enable sending periodic terascan updates.

        If enabled, laser will send updates in the beginning and in the end of every terascan segment.
        If ``update_period!=0``, it will also send updates every ``update_period`` percents of the segment (this option is not currently supported by M2 firmware).
        """
        _,reply=self.query("terascan_output",{"operation":("start" if enable else "stop"),"update":[int(update_period*1E2)],"delay":[int(update_delay*1E2)],"pause":"off"})
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
        where ``op`` is ``"scanning"`` (scanning in progress), ``"stitching"`` (stitching in progress), or ``"repeat"`` (segment is repeated).
        """
        self.update_reports()
        rep=self._last_status.get(self._terascan_update_op,None)
        if rep is not None:
            rep["activity"]={"scan":"scanning","repeat":"repeat"}.get(rep["status"],"stitching")
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
    def get_terascan_status(self, scan_type):
        """
        Get status of a terascan of a given type (or all statuses if ``scan_type=="all"``).

        Return a dictionary with 3 items:
            ``"current"``: current laser frequency (or ``None`` if no scan is in progress)
            ``"range"``: tuple with the fill scan range (or ``None`` if no frequency is available)
            ``"status"``: can be ``"stopped"`` (scan is not in progress), ``"scanning"`` (scan is in progress),
            or ``"stitching"`` (scan is in progress, but currently stitching)
        """
        if scan_type=="all":
            return {k:self.get_terascan_status(k) for k in self._terascan_kinds}
        scan_type=self._check_terascan_type(scan_type)
        try:
            _,reply=self.query("scan_stitch_status",{"scan":scan_type})
        except M2ParseError as err:
            if err.code==9:
                return {"status":"stopped","range":None,"current":None}
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
        return status


    _default_terascan_rates={"fine":100E6,"medium":5E9,"ir_fine":100E6,"ir_medium":5E9}
    def stop_all_operation(self, repeated=True, attempt=0):
        """
        Stop all laser operations (tuning and scanning).

        If ``repeated==True``, repeat trying to stop the operations until succeeded (more reliable, but takes more time).
        If ``attempt>0``, it can supply the number of already tried attempts to stop (with ``repeated=False``);
        the more attempts failed, the more drastic measures will be taken to stop (e.g., initialize short terascan)
        Return ``True`` if the operation is success and ``False`` otherwise.
        """
        ctd=general.Countdown(self.timeout or None)
        while True:
            operating=False
            for scan_type in self._terascan_kinds:
                stat=self.get_terascan_status(scan_type)
                if stat["status"]!="stopped":
                    operating=True
                    self.stop_terascan(scan_type)
                    time.sleep(1.)
                    if attempt>4 and attempt%2==1:
                        rate=self._default_terascan_rates[scan_type]
                        scan_center=(stat["current"] or 400E12)-(attempt-5)*100E9
                        self.setup_terascan(scan_type,(scan_center,scan_center+100E9),rate)
                        self.start_terascan(scan_type)
                        time.sleep(2.)
                        self.stop_terascan(scan_type)
                        time.sleep(2.)
            if self.is_fine_tuning():
                operating=True
                self.stop_fine_tuning()
            if (not repeated) or (not operating):
                break
            time.sleep(0.1)
            attempt+=1
            if (attempt>12 and ctd.passed()):
                raise M2Error("could not stop all operations: timed out")
        return not operating