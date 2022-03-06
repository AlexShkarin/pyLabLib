from ...core.thread import controller
from . import stream_message, stream_manager

import threading



class TableAccumulator:
    """
    Data accumulator which receives data chunks and adds them into a common table.

    Can receive either list of columns, or dictionary of named columns; designed to work with :class:`StreamFormerThread`.

    Args:
        channels([str]): channel names
        memsize(int): maximal number of rows to store
    """
    def __init__(self, channels, memsize=10**6):
        self.channels=channels
        self.memsize=memsize
        self.data=[self.ChannelData(self.memsize) for _ in channels]

    class ChannelData:
        """
        Single channel data manager.

        Manages the internal buffer to keep continuous list, but reduce number of list appends / removals.
        """
        def __init__(self, memsize, chunk_size=None):
            self.memsize=memsize
            if chunk_size is None:
                chunk_size=max(100,self.memsize//50)
            self.chunk_size=chunk_size
            self.start=0
            self.end=0
            self.data=[]
        def __len__(self):
            return self.end
        def add_data(self, data):
            """Add data (list of values) to the buffer"""
            l=len(data)
            if l+self.end>len(self.data):
                self.data.extend([0]*(len(data)+self.chunk_size))
            self.data[self.end:self.end+l]=data
            self.end+=l
            self.start=max(0,self.end-self.memsize)
            if self.start>self.chunk_size:
                del self.data[:self.start]
                self.end-=self.start
                self.start=0
        def reset_data(self):
            """Clean the buffer"""
            self.start=0
            self.end=0
            self.data=[]
        def get_data(self, l=None):
            """Get last at most `l` samples from the buffer (if `l` is ``None``, get all samples)"""
            start=max(0,(self.end-self.start)-l) if l is not None else 0
            return self.data[self.start+start:self.end]
    def __len__(self):
        if self.data:
            return len(self.data[0])
        return 0
    def add_data(self, data):
        """
        Add new data to the table.

        Data can either be a list of columns, or a dictionary ``{name: [data]}`` with named columns.
        """
        if isinstance(data,stream_message.DataBlockMessage):
            data=data.data
        if isinstance(data,dict):
            table_data=[]
            for ch in self.channels:
                if ch not in data:
                    raise KeyError("data doesn't contain channel {}".format(ch))
                table_data.append(data[ch])
            data=table_data
        minlen=min([len(incol) for incol in data])
        for col,incol in zip(self.data,data):
            col.add_data(incol[:minlen])
        return minlen
    def change_channels(self, channels):
        """
        Change channels in the table.
        
        All the accumulated data will be reset.
        """
        self.channels=channels
        self.data=[self.ChannelData(self.memsize) for _ in channels]
    def reset_data(self):
        """Clear all data in the table"""
        for col in self.data:
            col.reset_data()
    
    def get_data_columns(self, channels=None, maxlen=None):
        """
        Get table data as a list of columns.
        
        Args:
            channels: list of channels to get; all channels by default
            maxlen: maximal column length (if stored length is larger, return last `maxlen` rows)
        """
        channels=channels or self.channels
        chidx=[self.channels.index(ch) for ch in channels]
        data=[self.data[i].get_data(maxlen) for i in chidx]
        return data
    def get_data_rows(self, channels=None, maxlen=None):
        """
        Get table data as a list of rows.
        
        Args:
            channels: list of channels to get; all channels by default
            maxlen: maximal column length (if stored length is larger, return last `maxlen` rows)
        """
        return list(zip(*self.get_data_columns(channels=channels,maxlen=maxlen)))
    def get_data_dict(self, channels=None, maxlen=None):
        """
        Get table data as a dictionary ``{name: column}``.
        
        Args:
            channels: list of channels to get; all channels by default
            maxlen: maximal column length (if stored length is larger, return last `maxlen` rows)
        """
        channels=channels or self.channels
        channels=list(set(channels))
        return dict(zip(channels,self.get_data_columns(channels=channels,maxlen=maxlen)))






class TableAccumulatorThread(controller.QTaskThread):
    """
    Table accumulator thread which provides async access to :class:`TableAccumulator` instance.

    Setup args:
        - ``channels ([str])``: channel names
        - ``src (str)``: name of a source thread which emits new data signals (typically, a name of :class:`StreamFormerThread` thread)
        - ``tag (str)``: tag of the source multicast
        - ``memsize (int)``: maximal number of rows to store

    Commands:
        - ``get_data``: get some of the accumulated data
        - ``reset``: clear stored data
    """
    def setup_task(self, channels, src, tag, memsize=10**6):  # pylint: disable=arguments-differ
        self.channels=channels
        self.table_accum=TableAccumulator(channels=channels,memsize=memsize)
        self.subscribe_direct(self._accum_data,srcs=src,tags=tag)
        self.cnt=stream_manager.StreamIDCounter()
        self.data_lock=threading.Lock()
        self.add_direct_call_command("get_data")
        self.add_direct_call_command("reset",error_on_async=False)

    def preprocess_data(self, data):
        """Preprocess data before adding it to the table (to be overloaded)"""
        return data

    def _accum_data(self, src, tag, value):  # pylint: disable=unused-argument
        with self.data_lock:
            if hasattr(value,"get_ids") and self.cnt.receive_message(value):
                self.table_accum.reset_data()
            value=self.preprocess_data(value)
            self.table_accum.add_data(value)

    def get_data(self, channels=None, maxlen=None, fmt="rows"):
        """
        Get accumulated table data.
        
        Args:
            channels: list of channels to get; all channels by default
            maxlen: maximal column length (if stored length is larger, return last `maxlen` rows)
            fmt (str): return format; can be ``"rows"`` (list of rows), ``"columns"`` (list of columns), or ``"dict"`` (dictionary of named columns)
        """
        with self.data_lock:
            if fmt=="columns":
                return self.table_accum.get_data_columns(channels=channels,maxlen=maxlen)
            elif fmt=="rows":
                return self.table_accum.get_data_rows(channels=channels,maxlen=maxlen)
            elif fmt=="dict":
                return self.table_accum.get_data_dict(channels=channels,maxlen=maxlen)
            else:
                raise ValueError("unrecognized data format: {}".format(fmt))
    def reset(self):
        """Clear all data in the table"""
        with self.data_lock:
            self.table_accum.reset_data()
    def set_cutoff(self, sid=None, mid=0, reset=True):
        """Set incoming stream cutoff"""
        with self.data_lock:
            self.cnt.set_cutoff(sid=sid,mid=mid)
            if reset:
                self.table_accum.reset_data()