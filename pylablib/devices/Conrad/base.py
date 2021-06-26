from ...core.devio import comm_backend

import struct
import collections


class ConradError(comm_backend.DeviceError):
    """Generic Conrad devices error"""
class ConradBackendError(ConradError,comm_backend.DeviceBackendError):
    """Generic Conrad backend communication error"""


class RelayBoard(comm_backend.ICommBackendWrapper):
    """
    Conrad relay board controller

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
        start_addr: address which is assigned to the first board in the chain upon initialization; all following boards increase the address by 1
    """
    Error=ConradError
    def __init__(self, conn, start_addr=1):
        instr=comm_backend.new_backend(conn,"serial",term_write="",timeout=3.,defaults={"serial":("COM1",19200)},reraise_error=ConradBackendError)
        super().__init__(instr)
        self.start_addr=start_addr
        self._add_info_variable("start_addr",lambda: self.start_addr)
        self._add_info_variable("boards_number",lambda: self.boards_number)
        self._add_status_variable("relays",lambda: self.get_all_relays(0))
        self.open()

    def open(self):
        """Open the connection to the board"""
        res=super().open()
        self._initialize()
        return res

    TMessage=collections.namedtuple("TMessage",["comm","addr","data"])
    def _make_msg(self, comm, addr=1, data=0):
        check_sum=comm^addr^data
        return struct.pack("BBBB",comm,addr,data,check_sum)
    def _parse_msg(self, msg):
        return self.TMessage(*struct.unpack("BBBB",msg)[:3])

    def _initialize(self):
        res=self.query(1,self.start_addr,multi_result=True)
        self.boards_number=len(res)-1
    
    def query(self, comm, addr=1, data=0, multi_result=False):
        """
        Send a query with the given command, address and data.

        If ``multi_result==False``, read a single reply frame;
        otherwise, keep reading until reply with the same command as sent is received (used in initialization and broadcast queries).
        """
        msg=self._make_msg(comm,addr=addr,data=data)
        self.instr.write(msg)
        replies=[self._parse_msg(self.instr.read(4))]
        if multi_result:
            while replies[-1].comm!=comm:
                replies.append(self._parse_msg(self.instr.read(4)))
        return replies if multi_result else replies[0]

    def get_all_relays(self, addr=1):
        """
        Get all relay states.

        If `addr` is not 0, return dictionary ``{relay:value}``, where ``relay`` is the relay index on the board (between 1 and 8 inclusive).
        If ``addr==0`` (broadcast), return dictionary ``{addr:board_state}``, where ``board_state`` is in turn a state dictionary is described above.
        """
        if addr==0:
            reply=self.query(2,0,multi_result=True)
            return {r.addr:{i+1:bool(r.data&(1<<i)) for i in range(8)} for r in reply[:-1]}
        else:
            reply=self.query(2,addr)
            return {i+1:bool(reply.data&(1<<i)) for i in range(8)}
    def set_all_relays(self, values, addr=1):
        """
        Set all relay states.

        `values` can be a list (listing relay states from lowest to highest), or a dictionary ``{relay:value}``, where relays are numbered from 1 to 8.
        Relays without values are kept unchanged.
        If ``addr==0``, broadcast to all boards
        """
        if not isinstance(values,dict):
            values={i+1:v for i,v in enumerate(values)}
        mask=self.query(2,addr).data
        for p,v in values.items():
            bm=1<<(p-1)
            if v:
                mask|=bm
            else:
                mask&=0xFF^bm
        self.query(3,addr,mask,multi_result=(addr==0))
        return self.get_all_relays(addr=addr)

    def get_relay(self, relay, addr=1):
        """Get the state at a given relay (indexed from 1 to 8 inclusive)"""
        return self.get_all_relays(addr=addr)[relay]
    def set_relay(self, relay, enable=True, addr=1):
        """Get the state at a given relay (indexed from 1 to 8 inclusive)"""
        return self.set_all_relays({relay:enable},addr=addr)[relay]