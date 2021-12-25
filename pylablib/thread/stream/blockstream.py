from ...core.thread import controller
from ...core.utils import general, funcargparse

from . import stream_manager, stream_message

import numpy as np
import collections



TStreamFormerQueueStatus=collections.namedtuple("TStreamFormerQueueStatus",["enabled","queue_len","max_queue_len"])
class StreamFormerThread(controller.QTaskThread):
    """
    Thread that combines data from different sources and aligns it in complete rows.

    Channels can be added using :meth:`add_channel` function. Every time the new row is complete, it is added to the current block.
    When the block is complete (determined by ``block_period`` attribute), :meth:`on_new_block` is called.
    Accumulated data can be accessed with :meth:`get_data` and :meth:`pop_data`, or by default through ``"stream/data"`` multicast.

    Attributes:
        - ``block_period``: size of a row block which causes :meth:`on_new_block` call

    Commands:
        - ``get_data``: get the completed aligned data in a dictionary form
        - ``pop_data``: pop the completed aligned data (return the data and remove it from the internal storage)
        - ``clear_table``: clear the table with the completed aligned data
        - ``reset``: remove all data (table and all filled channels)
        - ``set_cutoff``: set cutoff for session or message ID of a subscribed source
        - ``configure_channel``: configure a channel behavior (enable or disable)
        - ``get_channel_status``: get channel status (number of datapoints in the queue, maximal queue size, etc.)
        - ``get_source_status``: get lengths of multicast queues for all the data sources

    Methods to overload:
        - :meth:`on_new_block`: called every time a new block is completed; by default, send an multicast with the new block's data
        - :meth:`prepare_new_data`: modify a new data chunk (dictionary of columns) before adding it to the storage
    """
    def prepare_new_data(self, columns):
        """
        Prepare a newly acquired chunk.
        
        `columns` is a dictionary ``{name: data}`` of newly acquired data,
        where ``name`` is a channel name, and ``data`` is a list of one or more newly acquired values.
        Returned data should be in the same format.
        By default, no modifications are made.
        """
        return columns
    def _build_new_block(self):
        data=self.pop_data()
        sid,mid=self.cnt.get_ids()
        self.cnt.next_message(self.sn)
        block=stream_message.DataBlockMessage(data,source=self.name,sid=sid,mid=mid,sn=self.sn)
        return block
    def on_new_block(self):
        """Gets called every time a new block is complete"""
        self.send_multicast(tag="stream/data",value=self._build_new_block())

    def setup_task(self):  # pylint: disable=arguments-differ
        self.channels={}
        self.table={}
        self.source_schedulers={}
        self.add_command("get_data")
        self.add_command("pop_data")
        self.add_command("clear_table")
        self.add_command("reset")
        self.add_command("set_cutoff")
        self.add_command("configure_channel")
        self.add_command("get_channel_status")
        self.add_command("get_scheduled_status")
        self.sn=self.name
        self.cnt=stream_manager.MultiStreamIDCounter()
        self.cnt.add_counter(self.sn)
        self.source_sns={}
        self._row_cnt=0
        self.block_period=1

    class ChannelQueue:
        """
        Queue for a single channel.

        Manages adding and updating new datapoints.
        For arguments, see :meth:`.StreamFormerThread.add_channel`.
        """
        def __init__(self, func=None, max_queue_len=10, required="auto", background=False, enabled=True, fill_on="started", latching=True, expand_list=False, pure_func=True, initial=None):
            funcargparse.check_parameter_range(fill_on,"fill_on",{"started","completed"})
            self.func=func
            self.queue=collections.deque()
            self.required=(func is None) if required=="auto" else required
            self.background=background
            self.max_queue_len=max_queue_len
            self.enabled=enabled
            self.fill_on=fill_on
            self.last_value=initial
            self.initial=initial
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
                elif self.max_queue_len:
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
        def set_required(self, required="auto"):
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
            self.last_value=self.initial
        def get_status(self):
            """
            Get the queue status

            Return tuple ``(enabled, queue_len, max_queue_len)``
            """
            return TStreamFormerQueueStatus(self.enabled,len(self.queue),self.max_queue_len)
            

    def add_channel(self, name, func=None, max_queue_len=10, enabled=True, required="auto", background=False, fill_on="started", latching=True, expand_list=False, pure_func=True, initial=None):
        """
        Add a new channel to the queue.

        If `func` is defined, the channel is usually filled automatically on start/completion of a new row, and no further actions are needed.
        If `func` is ``None``, the channel is supposed to get data from a multicast. In this case, :meth:`subscribe_source` needs to be called to set up this channel.

        Args:
            name (str): channel name
            func: function used to get the channel value if no data has been supplied
            max_queue_len (int): maximal queue length (``None`` means no length limit; not recommended)
            enabled (bool): determines if the channel is enabled by default (disabled channel always returns ``None``)
            required: determines if the channel is required to receive the value to complete the row;
                by default, ``False`` if `func` is specified and ``True`` otherwise
            background: if ``required==True``, determines whether receiving a new sample in this channel starts a new row (if ``background==False``),
                or if it's simply added; if all sample-receiving channels have ``background==True``, the func-defined channels will effectively
                be filled when the row is complete (corresponds to ``fill_on=="completed"`` regardless of its actual value).
            fill_on (str): determines when `func` is called to get the channel value;
                can be either ``"started"`` (when the new row is created) or ``"completed"`` (when the new row is complete)
            latching (bool): determines value of non-'required' channel if `func` is not supplied;
                if ``True``, it is equal to the last received values; otherwise, it is default
            expand_list (bool): if ``True`` and the received value is list, assume that it contains several datapoints and add them sequentially
                (note that this would generally required setting `max_queue_len`>1, otherwise only the last received value will show up in the queue)
            pure_func (bool): if ``True``, assume that fast consecutive calls to `func` return the same result, and the function has no side-effects
                (in this case, several consecutive calls to `func` are replaced by a single call result repeated necessary number of times)
            initial: initial channel value, used before any samples were received
        """
        if name in self.channels:
            raise KeyError("channel {} already exists".format(name))
        self.channels[name]=self.ChannelQueue(func,max_queue_len=max_queue_len,required=required,background=background,enabled=enabled,
            fill_on=fill_on,latching=latching,expand_list=expand_list,pure_func=pure_func,initial=initial)
        self.table[name]=[]
    def subscribe_source(self, name, srcs, tags=None, dsts="any", filt=None, parse="default", sn=None):
        """
        Subscribe a source multicast to a channels.

        Called automatically for subscribed channels, so it is rarely called explicitly.

        Args:
            name (str): source name
            srcs(str or [str]): multicast source name or list of source names to filter the subscription;
                can be ``"any"`` (any source) or ``"all"`` (only multicasts specifically having ``"all"`` as a source).
            tags: multicast tag or list of tags to filter the subscription (any tag by default);
                can also contain Unix shell style pattern (``"*"`` matches everything, ``"?"`` matches one symbol, etc.)
            dsts(str or [str]): multicast destination name or list of destination names to filter the subscription;
                can be ``"any"`` (any destination) or ``"all"`` (only source specifically having ``"all"`` as a destination).
            filt(callable): additional filter function which takes 4 arguments: source, destination, tag, and value,
                and checks whether multicast passes the requirements.
            parse: if not ``None``, specifies a parsing function which takes 3 arguments (`src`, `tag` and `value`)
                and returns a dictionary ``{name: value}`` of channel values to add
                (useful is a single multicast contains multiple channel values, e.g., multiple daq channels)
                The function is called in the multicast source thread, so it should be quick and non-blocking
                By default, any dictionary and :class:`.DataBlockMessage` messages are treated as sets of channels with corresponding names and values,
                while all other values are interpreted as single-channel values for a channel with the given `name`.
        """
        if parse=="default":
            parse=self._parse_default
        if sn is not None:
            self.source_sns[name]=sn
            def on_multicast(src, tag, value):
                self.cnt.receive_message(value,sn=sn)
                if self.cnt.check_cutoff(value,sn=sn):
                    self._add_data(name,value,src=src,tag=tag,parse=parse)
            self.cnt.add_counter(sn)
        else:
            def on_multicast(src, tag, value):
                self._add_data(name,value,src=src,tag=tag,parse=parse)
        self.subscribe_commsync(on_multicast,srcs=srcs,tags=tags,dsts=dsts,filt=filt,limit_queue=None,priority=-5)
    
    def set_cutoff(self, name, sid=None, mid=0, sn=True):
        """
        Set cutoffs for session and message IDs.

        Any arriving subscribed messages with IDs below the cutoff will be ignored.
        if ``sn==False``, assume that the name refers to the subscription source name; otherwise, assume that it refers to the stream name.
        Note that in either case the cutoff is set for the stream, i.e., it affects all sources using the same stream.
        If `sid` or `mid` are ``None``, the cutoff stays the same.
        """
        name=name if sn else self.source_sns[name]
        return self.cnt.set_cutoff(name,sid=sid,mid=mid)
    def _parse_default(self, src, tag, value):  # pylint: disable=unused-argument
        if isinstance(value,stream_message.DataBlockMessage):
            return value.get_data_dict()
        return value
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
                (useful is a single multicast contains multiple channel values, e.g., multiple daq channels)
                The function is called in the multicast source thread, so it should be quick and non-blocking
        """
        _max_queued_before=0
        _max_queued_after=0
        if parse is not None:
            row=parse(src,tag,value)
            if not isinstance(row,dict):
                row={name:row}
        else:
            row={name:value}
        for name,value in row.items():
            ch=self.channels[name]
            if not ch.background:
                _max_queued_before=max(_max_queued_before,ch.queued_len())
            self.channels[name].add(value)
            if not ch.background:
                _max_queued_after=max(_max_queued_after,ch.queued_len())
        new_rows=None
        for _,ch in self.channels.items():
            nready=ch.ready_len()
            if nready==0:
                new_rows=0
                break
            elif nready>0:
                new_rows=nready if new_rows is None else min(new_rows,nready)
        if new_rows is not None and new_rows>0:
            new_columns={}
            for n,ch in self.channels.items():
                new_columns[n]=ch.get(new_rows)
            new_columns=self.prepare_new_data(new_columns)
            for n,ch in new_columns.items():
                self.table[n]+=new_columns[n]
            self._row_cnt+=new_rows
            if self._row_cnt>=self.block_period:
                self._row_cnt=0
                self.on_new_block()
        elif _max_queued_after>_max_queued_before:
            for _,ch in self.channels.items():
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
            return dict((n,v[:nrows]) for n,v in self.table.items())
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
                return dict((n,v) for n,v in table.items())
            else:
                return np.column_stack([table[c] for c in columns])
        else:
            res=self.get_data(nrows=nrows,columns=columns)
            for _,c in self.table.items():
                del c[:nrows]
            return res

    def clear_table(self):
        """Clear table containing all complete rows"""
        self.table=dict([(n,[]) for n in self.table])
    def reset(self):
        """Clear everything: table of complete rows and all channel queues"""
        self.table=dict([(n,[]) for n in self.table])
        for _,ch in self.channels.items():
            ch.clear()
        self._partial_rows=[]
        return self.cnt.next_session(self.sn)

    def configure_channel(self, name, enable=True, required="auto", reset=True):
        """
        Reconfigure existing channel.

        Args:
            name (str): channel name
            enabled (bool): determines if the channel is enabled by default (disabled channel always returns ``None``)
            required: determines if the channel is required to receive the value to complete the row;
                by default, ``False`` if `func` is specified and ``True`` otherwise
            reset (bool): if ``True``, clear all channels after reconfiguring
        """
        self.channels[name].enable(enable)
        self.channels[name].set_required(required)
        if reset:
            self.reset()
    def get_channel_status(self):
        """
        Get channel status.

        Return dictionary ``{name: status}``, where ``status`` is a tuple ``(enabled, queue_len, max_queue_len)``.
        """
        status={}
        for n,ch in self.channels.items():
            status[n]=ch.get_status()
        return status
    def get_scheduled_status(self):
        """Get the total number of pending calls in the queues (includes both commands and source multicasts)"""
        return sum(len(sch) for sch in self._priority_queues.values())