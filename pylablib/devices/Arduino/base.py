from ...core.devio import comm_backend

import time


class ArduinoError(comm_backend.DeviceError):
    """Generic Arduino devices error"""
class ArduinoBackendError(ArduinoError,comm_backend.DeviceBackendError):
    """Generic Arduino backend communication error"""


class IArduinoDevice(comm_backend.ICommBackendWrapper):
    """
    Generic Arduino device.

    Args:
        port: serial port name
        rate: baud rate
        timeout: default communication timeout
        term_write: default write terminating character (automatically appended on every sent message)
        term_read: default read terminating character (used to determine when the incoming message is received completely)
        flush_before_op: if ``True`` (default), automatically flush input buffer on comm/query
    """
    Error=ArduinoError
    def __init__(self, port, rate=9600, timeout=10., term_write="\n", term_read="\n", flush_before_op=True):
        instr=comm_backend.new_backend((port,rate),"serial",term_write=term_write,term_read=term_read,timeout=timeout,no_dtrrts=True,reraise_error=ArduinoBackendError)
        self._flush_before_op=flush_before_op
        super().__init__(instr)
    
    def reset_board(self):
        """Reset the board by pulsing the DTR and RTS lines"""
        self.instr.instr.setDTR(1)
        self.instr.instr.setRTS(1)
        self.instr.instr.setDTR(0)
        self.instr.instr.setRTS(0)
    def comm(self, comm, timeout=None, flush=False, flush_delay=0.02):
        """
        Send a device command.

        If `timeout` is not ``None``, it specifies a custom timeout for the operation.
        If ``flush==True``, then wait for `flush_delay` seconds after the write and read everything returned by the device.
        """
        if self._flush_before_op:
            self.instr.flush_read()
        with self.instr.using_timeout(timeout):
            self.instr.write(comm)
            if flush:
                time.sleep(flush_delay)
                return self.instr.flush_read()
    def query(self, query, timeout=None, query_delay=0, flush=False, flush_delay=0.02):
        """
        Send a device query and return the reply.

        If `timeout` is not ``None``, it specifies a custom timeout for the reply read operation.
        If ``query_delay>0``, it specifies the delay between write and subsequent read attempt.
        If ``flush==True``, then wait for `flush_delay` seconds after the write and read everything returned by the device.
        """
        if self._flush_before_op:
            self.instr.flush_read()
        self.instr.write(query)
        time.sleep(query_delay)
        resp=self.instr.readline(timeout=timeout)
        if flush:
            time.sleep(flush_delay)
            self.instr.flush_read()
        return resp.strip()