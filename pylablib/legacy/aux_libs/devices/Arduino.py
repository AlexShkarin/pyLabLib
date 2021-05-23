"""
Home-built Arduino devices.
"""

from ...core.devio import backend  #@UnresolvedImport

import time
import collections

_depends_local=["...core.devio.backend"]


class IArduinoDevice(backend.IBackendWrapper):
    """
    Generic Arduino device.
    """
    def __init__(self, port_addr, rate=9600, timeout=10., term_write="\n", term_read="\n"):
        instr=backend.SerialDeviceBackend((port_addr,rate),timeout=timeout,term_write=term_write,term_read=term_read,connect_on_operation=True, no_dtr=True)
        instr._operation_cooldown=0.02
        self._flush_before_op=True
        backend.IBackendWrapper.__init__(self,instr)
    
    def ctrl_reset(self):
        self.instr.instr.setDTR(1)
        with self.instr.single_op():
            pass
        self.instr.instr.setDTR(0)
    def comm(self, comm, timeout=None, flush=False, flush_delay=0.02):
        comm=comm.strip()
        with self.instr.single_op():
            if self._flush_before_op:
                self.instr.flush_read()
            self.instr.write(comm)
            if flush:
                time.sleep(flush_delay)
                return self.instr.flush_read()
    def query(self, query, timeout=None, flush=False, flush_delay=0.02):
        query=query.strip()
        with self.instr.single_op():
            if self._flush_before_op:
                self.instr.flush_read()
            self.instr.write(query)
            resp=self.instr.readline(timeout=timeout)
            if flush:
                time.sleep(flush_delay)
                self.instr.flush_read()
        return resp.strip()
        
        





class FilterCavityLock(IArduinoDevice):
    def __init__(self, port_addr):
        IArduinoDevice.__init__(self,port_addr,timeout=3.)
    
    _modes=["no_laser","calibration","search","locked","sweep","idle"]
    def get_mode(self):
        imode=int(self.query("M"))
        return self._modes[imode]
    def wait_for_mode(self, mode, delay=0.5):
        while self.get_mode()!=mode:
            time.sleep(delay)
            
    def reset(self, sync=False):
        self.comm("C")
        if sync:
            self.wait_for_mode("locked")
            self.reset_stat()
    def lock(self, sync=False):
        self.comm("L")
        if sync:
            self.wait_for_mode("locked")
    def sweep(self):
        self.comm("S")
    def idle(self):
        self.comm("I")
        
    def reset_stat(self):
        self.comm("R")
    LevelStat=collections.namedtuple("LevelStat",["cal_min","cal_max","meas_min","meas_max"])
    def get_stat(self):
        stat=[float(x) for x in self.query("A").split()]
        return self.LevelStat(stat[0],stat[1],stat[4],stat[5]),self.LevelStat(stat[2]-stat[3],stat[2]+stat[3],stat[6],stat[7])
    def get_deviations(self):
        DCstat,PDHstat=self.get_stat()
        DCdev=(DCstat.meas_max-DCstat.meas_min)/(DCstat.cal_max-DCstat.cal_min)
        PDHdev=(PDHstat.meas_max-PDHstat.meas_min)/(PDHstat.cal_max-PDHstat.cal_min)
        return DCdev,PDHdev
        
        



class DAQDevice(IArduinoDevice):
    def __init__(self, port_addr):
        IArduinoDevice.__init__(self,port_addr,rate=57600,timeout=3.)
        self.instr._operation_cooldown=0.005
        self._flush_before_op=False
        
    def get_rate(self):
        return int(self.query("R"))
    
    def get_binning(self):
        return int(self.query("B?"))
    def set_binning(self, binning):
        self.comm("B {}".format(binning))
    def set_binning_time(self, binning_time, repeat=True):
        with self.instr.single_op():
            rate=self.get_rate()
            binning=max(1,binning_time*rate)
            self.set_binning(binning)
            if repeat:
                time.sleep(2.5)
                self.set_binning_time(binning_time,repeat=False)
    
    def get_active_channels(self):
        return int(self.query("C?"))
    def set_active_channels(self, channels):
        return self.comm("C {}".format(channels))
    
    def get_input(self, channel):
        return float(self.query("I {}".format(channel)))
    def get_all_inputs(self):
        inputs=self.query("IA")
        return [float(s.strip()) for s in inputs.strip().split()]
    
    def get_output(self, channel):
        return float(self.query("O? {}".format(channel)))
    def get_all_outputs(self):
        outputs=self.query("OA?")
        return [float(s.strip()) for s in outputs.strip().split()]
    def set_output(self, channel, value):
        with self.instr.single_op():
            self.comm("O {} {}".format(channel,value))
            return self.get_output(channel)
        
        


        
class OpticalSwitchController(IArduinoDevice):
    def __init__(self, port_addr):
        IArduinoDevice.__init__(self,port_addr,timeout=3.)
        self._add_settings_node("state",self.get_state,self.switch)
    
    def get_state(self):
        return bool(int(self.query("r",flush=True,flush_delay=0.1)))
    def switch(self, state):
        self.comm("s{}".format("1" if state else "0"),flush=True,flush_delay=0.1)
        return self.get_state()
        
        


        
class RelaylSwitchController(IArduinoDevice):
    """
    Arduino controller for the remote-controlled BNC inverter board.
    """
    def __init__(self, port_addr):
        IArduinoDevice.__init__(self,port_addr,timeout=3.)
        self._add_settings_node("state",self.get_state,self.switch)
    
    def get_state(self):
        """Get relay switch state"""
        return bool(int(self.query("R?")))
    def switch(self, state):
        """Set relay switch state"""
        self.comm("R{}".format("1" if state else "0"))
        return self.get_state()