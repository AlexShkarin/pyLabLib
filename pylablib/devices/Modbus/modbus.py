from ...core.utils import py3, crc
from ...core.devio import comm_backend

import struct
import collections
import contextlib



class ModbusError(comm_backend.DeviceError):
    """Generic Modbus device error"""
class ModbusBackendError(ModbusError,comm_backend.DeviceBackendError):
    """Generic Modbus backend communication error"""



TModbusFrame=collections.namedtuple("TModbusFrame",("address","function","data"))
class GenericModbusRTUDevice(comm_backend.ICommBackendWrapper):
    """
    Generic Modbus-connected RTU protocol device.

    Args:
        conn: serial connection parameters (usually port, a tuple containing port and baudrate,
            or a tuple with full specification such as ``("COM1", 9600, 8, 'N', 1)``)
        daddr: default device address
        conn_defaults: default connection parameters (baud rate, parity bits, etc.)
    """
    Error=ModbusError
    def __init__(self, conn, daddr=1, conn_defaults=("COM1",9600)):
        instr=comm_backend.new_backend(conn,"serial",term_read="",term_write="",defaults={"serial":conn_defaults},reraise_error=ModbusBackendError)
        self.mb_daddr=daddr
        super().__init__(instr)
    
    def _mb_get_daddr(self, daddr):
        if daddr is None:
            return self.mb_daddr
        return daddr
    def mb_get_default_address(self):
        """Get device address used by default in Modbus methods"""
        return self.mb_daddr
    def mb_set_default_address(self, daddr):
        """Set device address used by default in Modbus methods"""
        self.mb_daddr=daddr
    @contextlib.contextmanager
    def mb_using_address(self, daddr):
        """Context manager for temporary using a different default device address"""
        cdaddr=self.mb_daddr
        self.mb_daddr=daddr
        try:
            yield
        finally:
            self.mb_daddr=cdaddr

    def _mb_crc(self, msg):
        return crc.crc(msg,0x8005,refin=True,refout=True,init=0xFFFF)
    def _mb_build_comm(self, daddr, func, data):
        msg=struct.pack("BB",daddr,func)+py3.as_bytes(data)
        crcv=struct.pack("<H",self._mb_crc(msg))
        return msg+crcv
    def _mb_send_frame(self, func, data, daddr):
        msg=self._mb_build_comm(daddr,func,data)
        self.instr.write(msg)
    _mb_error_codes={1:"wrong function",2:"wrong address",3:"wrong value",4:"device failure"}
    def _mb_recv_read_reply(self, check_function=True, check_crc=True):
        hdr=self.instr.read(3)
        daddr,func,c=hdr
        if func&0x80:
            data=self.instr.read(2)
        else:
            data=self.instr.read(c+2)
        ecrc=self._mb_crc(hdr+data[:-2])
        rcrc,=struct.unpack("<H",data[-2:])
        if check_crc and ecrc!=rcrc:
            raise ModbusError("CRC error: expected 0x{:04X}, got 0x{:04X}".format(ecrc,rcrc))
        if check_function and func&0x80:
            raise ModbusError("function 0x{:02X} on device {} raised an error 0x{:02X}: {}".format(func&0x7F,daddr,c,self._mb_error_codes.get(c,"unknown")))
        return TModbusFrame(daddr,func,data[:-2])
    def _mb_recv_echo_reply(self):
        hdr=self.instr.read(2)
        daddr,func=hdr
        if func&0x80:
            data=self.instr.read(3)
        else:
            data=self.instr.read(6)
        ecrc=self._mb_crc(hdr+data[:-2])
        rcrc,=struct.unpack("<H",data[-2:])
        if ecrc!=rcrc:
            raise ModbusError("CRC error: expected 0x{:04X}, got 0x{:04X}".format(ecrc,rcrc))
        if func&0x80:
            raise ModbusError("function 0x{:02X} on device {} raised an error 0x{:02X}: {}".format(func&0x7F,daddr,data[0],self._mb_error_codes.get(data[0],"unknown")))
        return TModbusFrame(daddr,func,data[:-2])
    def _mb_check_reply(self, reply, daddr=None, func=None):
        if daddr is not None and reply.address!=daddr:
            raise ValueError("expected reply from address {}, got address {}".format(daddr,reply.address))
        if func is not None and reply.function!=func:
            raise ValueError("expected reply with function {}, got function {}".format(func,reply.function))
    
    def _mb_read_addr_data(self, daddr, function, address, quantity):
        daddr=self._mb_get_daddr(daddr)
        self._mb_send_frame(function,struct.pack(">HH",address,quantity),daddr)
        reply=self._mb_recv_read_reply()
        self._mb_check_reply(reply,daddr,function)
        return reply.data
    def mb_read_coils(self, address, quantity=1, daddr=None):
        """Read Modbus one-bit discrete coils with the given starting address and quantity"""
        return self._mb_read_addr_data(daddr,1,address,quantity)
    def mb_read_discrete_inputs(self, address, quantity, daddr=None):
        """Read Modbus one-bit discrete inputs with the given starting address and quantity"""
        return self._mb_read_addr_data(daddr,2,address,quantity)
    def mb_read_holding_registers(self, address, quantity, daddr=None):
        """Read Modbus two-byte holding registers with the given starting address and quantity"""
        return self._mb_read_addr_data(daddr,3,address,quantity)
    def mb_read_input_registers(self, address, quantity, daddr=None):
        """Read Modbus two-byte input registers with the given starting address and quantity"""
        return self._mb_read_addr_data(daddr,4,address,quantity)

    def _mb_write_addr_data(self, daddr, function, address, argument, data=b""):
        daddr=self._mb_get_daddr(daddr)
        hdr=struct.pack(">HH",address,argument)
        self._mb_send_frame(function,hdr+data,daddr)
        reply=self._mb_recv_echo_reply()
        self._mb_check_reply(reply,daddr,function)
        if reply.data[:4]!=hdr:
            ehdr="0x{:04X}{:04X}".format(address,argument)
            rhdr="0x"+"".join(["{:02X}".format(v) for v in reply.data[:4]])
            raise ModbusBackendError("expected echo reply with values {}, got {}".format(ehdr,rhdr))
    def mb_write_single_coil(self, address, value, daddr=None):
        """Write a single Modbus one-bit discrete coil at the given address"""
        return self._mb_write_addr_data(daddr,5,address,0xFF00 if value else 0x0000)
    def mb_write_single_holding_register(self, address, value, daddr=None):
        """Write a single Modbus two-byte holding register at the given address"""
        return self._mb_write_addr_data(daddr,6,address,int(value))
    def mb_write_multiple_coils(self, address, value, quantity=None, daddr=None):
        """
        Write multiple Modbus one-bit discrete coils with the given starting address and quantity.
        
        `value` is a bytes object with the bit values listed LSB first.
        """
        if quantity is None:
            quantity=len(value)*8
        elif (quantity-1)//8+1!=len(value):
            raise ValueError("{} bit values require {} byte data; got {} bytes".format(quantity,(quantity-1)//8+1,len(value)))
        return self._mb_write_addr_data(daddr,15,address,quantity,data=struct.pack("B",len(value))+value)
    def mb_write_multiple_holding_registers(self, address, value, daddr=None):
        """
        Write a multiple Modbus two-byte holding registers at the given address.
        
        `value` is a bytes object with the values listed LSB first.
        """
        if len(value)%2==1:
            raise ValueError("number of value bytes should be even, got {}".format(len(value)))
        return self._mb_write_addr_data(daddr,16,address,len(value)//2,data=struct.pack("B",len(value))+value)

    def mb_get_device_id(self, daddr=None):
        """Get Modbus device ID (function 17)"""
        daddr=self._mb_get_daddr(daddr)
        self._mb_send_frame(0x11,b"",daddr)
        reply=self._mb_recv_read_reply()
        self._mb_check_reply(reply,daddr,0x11)
        return reply.data
    
    def mb_scan_devices(self, daddrs="all", timeout=0.1, func=1, payload=b""):
        """
        Scan for devices on the bus by sending a specified command and waiting for the reply.

        `daddrs` is a list of addresses to check (``"all"`` means all addresses from 1 to 247 inclusive)
        `timeout` is the timeout to wait for each device reply.
        `func` and `payload` specify the message to send (by default, 'read coil' command with no arguments, which should always return and error)
        Since the addresses are polled consecutively, this function can take a long time (~25s for the default settings).
        """
        if daddrs=="all":
            daddrs=range(1,248)
        detected=set()
        with self.instr.using_timeout(timeout):
            for da in daddrs:
                self._mb_send_frame(func,payload,da)
                try:
                    reply=self._mb_recv_read_reply(check_function=False)
                    detected.add(reply.address)
                except ModbusError:
                    pass
        return sorted(detected)