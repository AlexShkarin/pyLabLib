import pywinusb.hid as hid  #@UnresolvedImport
from ...core.devio import backend  #@UnresolvedImport
from ...core.utils import numerical, general  #@UnresolvedImport
from ...core.utils import log #@UnresolvedImport

import time
import threading

_depends_local=["...core.devio.backend"]

class IVaunixDevice(backend.IBackendWrapper):
    """
    Generic Vaunix device.
    """
    def __init__(self, product_id=None, idx=0):
        backend.IBackendWrapper.__init__(self,self._find_device(product_id,idx))
        self._responses={}
        self._events={}
        self._event_lock=threading.Lock()
        self._pause_handler=False
        self._pause_start_event=threading.Event()
        self.instr.open()
        self.instr.set_raw_data_handler(self._response_handler)
        self._retry_count=5
        self._recv_timeout=5.
        
    def close(self):
        self._pause_handler=True
        self._pause_start_event.wait()
        self.instr.close()
        
    @staticmethod
    def _find_device(product_id, idx):
        if product_id:
            devices=hid.HidDeviceFilter(vendor_id=0x041F,product_id=product_id).get_devices()
        else:
            devices=hid.HidDeviceFilter(vendor_id=0x041F).get_devices()
        if len(devices)<=idx:
            raise RuntimeError("can't find device index {}".format(idx))
        devices.sort(key=lambda d: str(d))
        return devices[idx]
    
    @staticmethod
    def _build_query(comm, count, value):
        data=[0]+[comm]+[count]
        byteblock=[(value>>(i*8))&0xFF for i in range(count)]
        data=data+byteblock
        return data+[0]*(9-len(data))
    @staticmethod
    def _parse_response(data):
        comm=data[1]
        count=data[2]
        byteblock=data[3:3+count]
        value=sum([ (b<<(8*i)) for i,b in enumerate(byteblock) ])
        return comm,value
    def _response_handler(self, data):
        if self._pause_handler:
            self._pause_start_event.set()
            time.sleep(.5)  # pausing the response thread seems to reduce the possibility of inst.close() crashing (more wait time for closing resources?)  
            return
        with self._event_lock:
            comm,value=self._parse_response(data)
            self._responses[comm]=value
            if comm not in self._events:
                self._events[comm]=threading.Event()
            self._events[comm].set()
    def _try_recv_data(self, comm):
        with self._event_lock:
            if comm not in self._events:
                self._events[comm]=threading.Event()
            evt=self._events[comm]
        if evt.wait(timeout=self._recv_timeout):
            evt.clear()
            return self._responses.pop(comm)
        else:
            raise RuntimeError("no data received with command 0x{:02x}".format(comm))
    def send_data(self, comm, count, value):
        query=self._build_query(comm,count,value)
        self.instr.send_output_report(query)
        time.sleep(0.05)
    def recv_data(self, comm):
        for t in general.RetryOnException(self._retry_count,RuntimeError):
            with t:
                return self._try_recv_data(comm)
            error_msg="receiving command 0x{:02x} failed; retrying...".format(comm)
            log.default_log.info(error_msg,origin="devices/Vaunix",level="warning")
    def query_data(self, send_comm, recv_comm=None, send_count=0, send_value=0):
        comm=send_comm if recv_comm is None else recv_comm
        for t in general.RetryOnException(self._retry_count,RuntimeError):
            with t:
                self.send_data(send_comm,send_count,send_value)
                return self._try_recv_data(comm)
            error_msg="querying command 0x{:02x} failed; retrying...".format(comm)
            log.default_log.info(error_msg,origin="devices/Vaunix",level="warning")
        
        
        
class LMS(IVaunixDevice):
    """
    Vaunix LMS (LabBrick) microwave generator.
    """
    def __init__(self, product_id=None, idx=0):
        IVaunixDevice.__init__(self,product_id=product_id,idx=idx)
        self._max_power=10.
        self._min_power=-45.
        self._add_settings_node("power_on",self.get_output,None)
        self._add_settings_node("power",self.get_output_level,self.set_output_level)
        self._add_settings_node("frequency",self.get_frequency,self.set_frequency)
        self._add_settings_node("extref",self.get_extref,self.set_extref)
        
    def get_output(self):
        return bool(self.query_data(0x0A))
    def set_output(self, output=True):
        self.send_data(0x8A,1,int(output))
        return self.get_output()
    
    def get_extref(self):
        return not bool(self.query_data(0x23))
    def set_extref(self, extref=True):
        self.send_data(0xA3,1,int(not extref))
        return self.get_extref()
    
    def get_output_level(self):
        level=self.query_data(0x0D)
        return self._max_power-level*0.25 # weird power encoding
    def set_output_level(self, level):
        level=numerical.limit_to_range(level,self._min_power,self._max_power)
        level=int((self._max_power-level)/0.25) # weird power encoding
        self.send_data(0x8D,1,level)
        return self.get_output_level()
    def get_frequency(self):
        return self.query_data(0x44)*10. # units of 10's of Hz
    def set_frequency(self, frequency):
        frequency=numerical.limit_to_range(frequency,0.5E9,2.3E9)
        self.send_data(0xC4,4,int(frequency/10.)) # units of 10's of Hz
        return self.get_frequency()
    
    def save_as_default(self):
        self.send_data(0x8C,3,0x315542)
    
    
    def apply_settings(self, settings):
        if "power_on" in settings and not settings["power_on"]:
            self.set_output(False)
        IVaunixDevice.apply_settings(self,settings)
        if "power_on" in settings and settings["power_on"]:
            self.set_output(True)
        return self.get_settings()