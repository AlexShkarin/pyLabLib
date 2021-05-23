from ...core.gui.qt.thread import controller
from ...core.utils import files as file_utils, general, funcargparse
from ...core.fileio import logfile

from PyQt5 import QtCore
import numpy as np
import threading
import collections
from future.utils import viewitems
import os.path




class StreamFormerThread(controller.QTaskThread):
    """
    Thread that combines data from different sources and aligns it in complete rows.

    Channels can be added using :meth:`add_channel` function. Every time the new row is complete, it is added to the current block.
    When the block is complete (determined by ``block_period`` attribute), :meth:`on_new_block` is called.
    Accumulated data can be accessed with :meth:`get_data` and :meth:`pop_data`.

    Args:
        name: thread name
        devargs: args supplied to :math:`setup` method
        devkwargs: keyword args supplied to :math:`setup` method
        signal_pool: :class:`.SignalPool` for this thread (by default, use the default common pool)

    Attributes:
        block_period: size of a row block which causes :meth:`on_new_block` call

    Commands:
        get_data: get the completed aligned data
        pop_data: pop the completed aligned data (return the data and remove it from the internal storage)
        clear_table: clear the table with the completed aligned data
        clear_all: remove all data (table and all filled channels)
        configure_channel: configure a channel behavior (enable or disable)
        get_channel_status: get channel status (number of datapoints in the queue, maximal queue size, etc.)
        get_source_status: get lengths of signal queues for all the data sources

    Methods to overload:
        :meth:`setup`: set up the thread
        :meth:`cleanup`: clean up the thread 
        :meth:`prepare_new_data`: modify a new data chunk (dictionary of columns) before adding it to the storage
    """
    def setup(self):
        """Set up the thread"""
        pass
    def prepare_new_data(self, columns):
        """
        Prepare a newly acquired chunk.
        
        `column` is a dictionary ``{name: data}`` of newly acquired data,
        where ``name`` is a channel name, and ``data`` is a list of one or more newly acquired values.
        Returned data should be in the same format.
        By default, no modifications are made.
        """
        return columns
    def on_new_block(self):
        """Gets called every time a new block is complete"""
        pass
    def cleanup(self):
        """Clean up the thread"""
        pass

    def setup_task(self, *args, **kwargs):
        self.channels={}
        self.table={}
        self.source_schedulers={}
        self.add_command("get_data")
        self.add_command("pop_data")
        self.add_command("clear_table")
        self.add_command("clear_all")
        self.add_command("configure_channel")
        self.add_command("get_channel_status")
        self.add_command("get_source_status")
        self._row_cnt=0
        self.block_period=1
        self.setup(*args,**kwargs)
    def finalize_task(self):
        self.cleanup()

    class ChannelQueue(object):
        """
        Queue for a single channel.

        Manages adding and updating new datapoints.
        For arguments, see :meth:`.StreamFormerThread.add_channel`.
        """
        QueueStatus=collections.namedtuple("QueueStatus",["queue_len","enabled","max_queue_len"])
        def __init__(self, func=None, max_queue_len=1, required="auto", background=False, enabled=True, fill_on="started", latching=True, expand_list=False, pure_func=True, default=None):
            object.__init__(self)
            funcargparse.check_parameter_range(fill_on,"fill_on",{"started","completed"})
            self.func=func
            self.queue=collections.deque()
            self.required=(func is None) if required=="auto" else required
            self.background=background
            self.max_queue_len=max_queue_len
            self.enabled=enabled
            self.fill_on=fill_on
            self.last_value=default
            self.default=default
            self.latching=latching
            self.expand_list=expand_list
            self.pure_func=pure_func
        def add(self, value):
            """Add a new value (or list of values) to the queue"""
            if self.expand_list and isinstance(value,list):
                vallst=value
            else:
                vallst=[value]
            if self.enabled:
                nvals=len(vallst)
                if not self.required:
                    toadd=1
                    topop=len(self.queue)
                elif self.max_queue_len>0:
                    nstored=len(self.queue)
                    rest_len=self.max_queue_len-nstored
                    if self.max_queue_len<=nvals:
                        topop=nstored
                        toadd=self.max_queue_len
                    else:
                        toadd=nvals
                        topop=max(0,nvals-rest_len)
                else:
                    topop=0
                    toadd=nvals
                for _ in range(topop):
                    self.queue.popleft()
                for v in vallst[-toadd:]:
                    self.queue.append(v)
                if self.latching:
                    self.last_value=vallst[-1]
        def add_from_func(self, n=1):
            """
            Fill the queue from the function (if available)
            
            `n` specifies number of values to add.
            """
            if self.enabled and self.func and self.fill_on=="started":
                if self.pure_func:
                    val=self.func()
                    for _ in range(n):
                        self.queue.append(val)
                else:
                    for _ in range(n):
                        self.queue.append(self.func())
                return True
            return False
        def queued_len(self):
            """Get queue length"""
            return len(self.queue)
        def ready(self):
            """Check if at leas one datapoint is ready"""
            return (not self.enabled) or (not self.required) or self.queue
        def ready_len(self):
            """
            Return length of the stored data.

            Return 0 if no data is ready, or -1 if "infinite" amount of data is ready (e.g., channel is off)
            """
            return -1 if ((not self.enabled) or (not self.required)) else len(self.queue)
        def enable(self, enable=True):
            """Enable or disable the queue"""
            if self.enabled and not enable:
                self.queue.clear()
            self.enabled=enable
        def set_requried(self, required="auto"):
            """Specify if receiving value is required"""
            self.required=(self.func is None) if required=="auto" else required
        def get(self, n=1):
            """
            Pop the oldest values
            
            `n` specifies number of values to pop. Return list of values.
            """
            if not self.enabled:
                return [None]*n
            elif self.queue:
                if self.required:
                    return [self.queue.popleft() for _ in range(n)]
                else:
                    poplen=min(len(self.queue),n)
                    res=[self.queue.popleft() for _ in range(poplen)]
                    if poplen<n:
                        res+=self.get(n-poplen)
                    return res
            elif self.func:
                return [self.func()]*n if self.pure_func else [self.func() for _ in range(n)]
            elif not self.required:
                return [self.last_value]*n
            else:
                raise IndexError("no queued data to get")
        def clear(self):
            """Clear the queue"""
            self.queue.clear()
            self.last_value=self.default
        def get_status(self):
            """
            Get the queue status

            Return tuple ``(queue_len, enabled, max_queue_len)``
            """
            return self.QueueStatus(len(self.queue),self.enabled,self.max_queue_len)
            

    def add_channel(self, name, func=None, max_queue_len=1, enabled=True, required="auto", background=False, fill_on="started", latching=True, expand_list=False, pure_func=True, default=None):
        """
        Add a new channel to the queue.

        Args:
            name (str): channel name
            func: function used to get the channel value if no data has been suppled
            max_queue_len (int): maximal queue length
            enabled (bool): determines if the channel is enabled by default (disabled channel always returns ``None``)
            required: determines if the channel is required to receive the value to complete the row;
                by default, ``False`` if `func` is specified and ``True`` otherwise
            background: if ``required==True``, determines whether receiving a new sample in this channel starts a new row (if ``background==False``),
                or if it's simply added; if all sample-receiving channels have ``background==True``, the func-defined channels will effectively
                be filled when the row is complete (corresponds to ``fill_on=="completed"`` regardless of its actual value).
            fill_on (str): determines when `func` is called to get the channel value;
                can be either ``"started"`` (when the new row is created) or ``"completed"`` (when the new row is complete)
            latching (bool): determines value of non-`required` channel if `func` is not supplied;
                if ``True``, it is equal to the last received values; otherwise, it is default
            expand_list (bool): if ``True`` and the received value is list, assume that it contains several datapoints and add them sequentially
                (note that this would generally required setting `max_queue_len`>1, otherwise only the last received value will show up)
            pure_func (bool): if ``True``, assume that fast consecutive calls to `func` return the same result, and the function has no side-effects
                (in this case, several consecutive calls to `func` are approximated by a single call result repeated necessary number of times)
            default: default channel value
        """
        if name in self.channels:
            raise KeyError("channel {} already exists".format(name))
        self.channels[name]=self.ChannelQueue(func,max_queue_len=max_queue_len,required=required,background=background,enabled=enabled,
            fill_on=fill_on,latching=latching,expand_list=expand_list,pure_func=pure_func,default=default)
        self.table[name]=[]
    def subscribe_source(self, name, srcs, dsts="any", tags=None, parse=None, filt=None):
        """
        Subscribe a source signal to a channels.

        Called automatically for subscribed channels, so it is rarely called explicitly.

        Args:
            name (str): channel name
            srcs(str or [str]): signal source name or list of source names to filter the subscription;
                can be ``"any"`` (any source) or ``"all"`` (only signals specifically having ``"all"`` as a source).
            dsts(str or [str]): signal destination name or list of destination names to filter the subscription;
                can be ``"any"`` (any destination) or ``"all"`` (only source specifically having ``"all"`` as a destination).
            tags: signal tag or list of tags to filter the subscription (any tag by default).
            parse: if not ``None``, specifies a parsing function which takes 3 arguments (`src`, `tag` and `value`)
                and returns a dictionary ``{name: value}`` of channel values to add
                (useful is a single signal contains multiple channel values, e.g., multiple daq channels)
                The function is called in the signal source thread, so it should be quick and non-blocking
            filt(callable): additional filter function which takes 4 arguments: signal source, signal destination, signal tag, signal value,
                and checks whether signal passes the requirements.
        """
        def on_signal(src, tag, value):
            self._add_data(name,value,src=src,tag=tag,parse=parse)
        uid=self.subscribe_commsync(on_signal,srcs=srcs,dsts=dsts,tags=tags,filt=filt,limit_queue=-1)
        self.source_schedulers[name]=self._signal_schedulers[uid]
            
    def _add_data(self, name, value, src=None, tag=None, parse=None):
        """
        Add a value to the channel.

        Called automatically for subscribed channels, so it is rarely called explicitly.

        Args:
            name (str): channel name
            value: value to add
            src (str): specifies values source; supplied to the `parse` function
            tag (str): specifies values tag; supplied to the `parse` function
            parse: if not ``None``, specifies a parsing function which takes 3 arguments (`src`, `tag` and `value`)
                and returns a dictionary ``{name: value}`` of channel values to add
                (useful is a single signal contains multiple channel values, e.g., multiple daq channels)
                The function is called in the signal source thread, so it should be quick and non-blocking
        """
        _max_queued_before=0
        _max_queued_after=0
        if parse is not None:
            row=parse(src,tag,value)
            if not isinstance(row,dict):
                row={name:row}
        else:
            row={name:value}
        for name,value in viewitems(row):
            ch=self.channels[name]
            if not ch.background:
                _max_queued_before=max(_max_queued_before,ch.queued_len())
            self.channels[name].add(value)
            if not ch.background:
                _max_queued_after=max(_max_queued_after,ch.queued_len())
        new_rows=None
        for _,ch in viewitems(self.channels):
            nready=ch.ready_len()
            if nready==0:
                new_rows=0
                break
            elif nready>0:
                new_rows=nready if new_rows is None else min(new_rows,nready)
        if new_rows is not None and new_rows>0:
            new_columns={}
            for n,ch in viewitems(self.channels):
                new_columns[n]=ch.get(new_rows)
            new_columns=self.prepare_new_data(new_columns)
            for n,ch in viewitems(new_columns):
                self.table[n]+=new_columns[n]
            self._row_cnt+=new_rows
            if self._row_cnt>=self.block_period:
                self._row_cnt=0
                self.on_new_block()
        elif _max_queued_after>_max_queued_before:
            for _,ch in viewitems(self.channels):
                chl=ch.queued_len()
                if chl<_max_queued_after:
                    ch.add_from_func(_max_queued_after-chl)




    def get_data(self, nrows=None, columns=None, copy=True):
        """
        Get accumulated data.

        Args:
            nrows: number of rows to get; by default, all complete rows
            columns: list of channel names to get; by default all channels
            copy (bool): if ``True``, return copy of the internal storage table (otherwise the returned data can increase in size).

        Return dictionary ``{name: [value]}`` of channel value lists (all lists have the same length) if columns are not specified,
        or a 2D numpy array if the columns are specified.
        """
        if columns is None and nrows is None:
            return self.table.copy() if copy else self.table
        if nrows is None:
            nrows=len(general.any_item(self.table)[1])
        if columns is None:
            return dict((n,v[:nrows]) for n,v in viewitems(self.table))
        else:
            return np.column_stack([self.table[c][:nrows] for c in columns])
    def pop_data(self, nrows=None, columns=None):
        """
        Pop accumulated data.

        Same as :meth:`get_data`, but removes the returned data from the internal storage.
        """
        if nrows is None:
            table=self.table
            self.table=dict([(n,[]) for n in table])
            if columns is None:
                return dict((n,v) for n,v in viewitems(table))
            else:
                return np.column_stack([table[c] for c in columns])
        else:
            res=self.get_data(nrows=nrows,columns=columns)
            for _,c in viewitems(self.table):
                del c[:nrows]
            return res

    def clear_table(self):
        """Clear table containing all complete rows"""
        self.table=dict([(n,[]) for n in self.table])
    def clear_all(self):
        """Clear everything: table of complete rows and all channel queues"""
        self.table=dict([(n,[]) for n in self.table])
        for _,ch in viewitems(self.channels):
            ch.clear()
        self._partial_rows=[]

    def configure_channel(self, name, enable=True, required="auto", clear=True):
        """
        Reconfigure existing channel.

        Args:
            name (str): channel name
            enabled (bool): determines if the channel is enabled by default (disabled channel always returns ``None``)
            required: determines if the channel is required to receive the value to complete the row;
                by default, ``False`` if `func` is specified and ``True`` otherwise
            clear (bool): if ``True``, clear all channels after reconfiguring
        """
        self.channels[name].enable(enable)
        self.channels[name].set_requried(required)
        if clear:
            self.clear_all()
    def get_channel_status(self):
        """
        Get channel status.

        Return dictionary ``{name: status}``, where ``status`` is a tuple ``(queue_len, enabled, max_queue_len)``.
        """
        status={}
        for n,ch in viewitems(self.channels):
            status[n]=ch.get_status()
        return status
    def get_source_status(self):
        """
        Get source incoming queues status.

        Return dictionary ``{name: queue_le}``.
        """
        status={}
        for n,sch in viewitems(self.source_schedulers):
            status[n]=sch.get_current_len()
        return status





class TableAccumulator(object):
    """
    Data accumulator which receives data chunks and adds them into a common table.

    Can receive either list of columns, or dictionary of named columns; designed to work with :class:`StreamFormerThread`.

    Args:
        channels ([str]): channel names
        memsize(int): maximal number of rows to store
    """
    def __init__(self, channels, memsize=1000000):
        object.__init__(self)
        self.channels=channels
        self.memsize=memsize
        self.data=[self.ChannelData(self.memsize) for _ in channels]

    class ChannelData(object):
        """
        Single channel data manager.

        Manages the internal buffer to keep continuous list, but reduce number of list appends / removals.
        """
        def __init__(self, memsize, chunk_size=None):
            object.__init__(self)
            self.memsize=memsize
            if chunk_size is None:
                chunk_size=max(100,self.memsize//50)
            self.chunk_size=chunk_size
            self.start=0
            self.end=0
            self.data=[]
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
    def add_data(self, data):
        """
        Add new data to the table.

        Data can either be a list of columns, or a dictionary ``{name: [data]}`` with named columns.
        """
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
    def reset_data(self, maxlen=0):
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

    Args:
        channels ([str]): channel names
        data_source (str): source thread which emits new data signals (typically, a name of :class:`StreamFormerThread` thread)
        memsize(int): maximal number of rows to store
    """
    def setup_task(self, channels, data_source, memsize=1000000):
        self.channels=channels
        self.fmt=[None]*len(channels)
        self.table_accum=TableAccumulator(channels=channels,memsize=memsize)
        self.subscribe_commsync(self._accum_data,srcs=data_source,dsts="any",tags="points",limit_queue=100)
        self.subscribe_commsync(self._on_source_reset,srcs=data_source,dsts="any",tags="reset")
        self.logger=None
        self.streaming=False
        self.add_command("start_streaming",self.start_streaming)
        self.add_command("stop_streaming",self.stop_streaming)
        self.data_lock=threading.Lock()

    def start_streaming(self, path, source_trigger=False, append=False):
        """
        Start streaming data to the disk.

        Args:
            path (str): path to the file
            source_trigger (bool): if ``True``, start streaming only after source ``"reset"`` signal; otherwise, start streaming immediately
            append (bool): if ``True``, append new data to the existing file; otherwise, overwrite the file
        """
        self.streaming=not source_trigger
        if not append and os.path.exists(path):
            file_utils.retry_remove(path)
        self.logger=logfile.LogFile(path)
    def stop_streaming(self):
        """Stop streaming data to the disk"""
        self.logger=None
        self.streaming=False

    def preprocess_data(self, data):
        """Preprocess data before adding it to the table (to be overloaded)"""
        return data

    def _on_source_reset(self, src, tag, value):
        with self.data_lock:
            self.table_accum.reset_data()
        if self.logger and not self.streaming:
            self.streaming=True

    def _accum_data(self, src, tag, value):
        with self.data_lock:
            value=self.preprocess_data(value)
            added_len=self.table_accum.add_data(value)
        if self.logger and self.streaming:
            new_data=self.table_accum.get_data_rows(maxlen=added_len)
            self.logger.write_multi_datalines(new_data,columns=self.channels,add_timestamp=False,fmt=self.fmt)

    def get_data_sync(self, channels=None, maxlen=None, fmt="rows"):
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