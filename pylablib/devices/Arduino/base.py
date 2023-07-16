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
        dtrrts: determines whether to use DTR/RTS signals for communication; generally, should be set to ``True`` on newer boards (e.g., Leonardo) and to ``False`` on older boards (e.g., Uno);
          settings ``dtrrts=True`` on older boards leads to the board reset upon connection, and settings ``dtrrts=False`` on newer boards leads to the communications getting frozen
    """
    Error=ArduinoError
    def __init__(self, port, rate=9600, timeout=10., term_write="\n", term_read="\n", flush_before_op=True, dtrrts=True):
        self._get_new_instr=lambda: comm_backend.new_backend((port,rate),"serial",term_write=term_write,term_read=term_read,timeout=timeout,no_dtrrts=not dtrrts,reraise_error=ArduinoBackendError)
        self._flush_before_op=flush_before_op
        super().__init__(self._get_new_instr())
    
    def reopen(self):
        """Close and reopen the device connection"""
        self.instr.close()
        time.sleep(0.2)
        self.instr=self._get_new_instr()
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