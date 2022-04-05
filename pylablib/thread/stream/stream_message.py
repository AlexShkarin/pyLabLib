from ...core.utils import functions

import time

import numpy as np
import collections





class IStreamMessage:
    """
    A generic message belonging to a stream.

    Args:
        sn: stream name (usually, references to the stream original source or purpose); could be ``None``, implying an "anonymous" stream
        sid: session numerical ID, a unique ID (usually an incrementing number) which is different for different streaming sessions
        mid: message numerical ID, a unique ID (usually an incrementing number) of the message within the stream
    
    Either `mid` or both IDs can be ``None``, indicating that the corresponding stream does not keep track of these IDs.
    In addition, `sid` and `mid` can be dictionaries (preferably with the same keys), which indicates that this message
    inherits IDs from several streams with the given keys (e.g., it comes from a producer which join several streams together into one).
    """
    _init_args=[]
    def __init__(self, sn=None, sid=None, mid=None):
        super().__init__()
        self.sid=sid
        self.mid=mid
        self.sn=sn
        self._setup_ids()
        if not type(self)._init_args:
            type(self)._init_args=functions.funcsig(self.__init__).arg_names[1:]

    def _setup_ids(self):
        if isinstance(self.sid,dict):
            if self.sn is None:
                raise ValueError("anonymous streams can not have multi-named IDs: sid={}".format(self.sid))
            if not (self.sn in self.sid):
                raise KeyError("stream name {} is not in sid {}".format(self.sn,self.sid))
        elif self.sn is not None:
            self.sid={self.sn:self.sid}
            if self.mid is not None:
                self.mid={self.sn:self.mid}
    def get_ids(self, name=None):
        """
        Get message IDs as a tuple ``(sid, mid)``.

        If `name` is ``None``, assume that the message IDs are not named, and simply return them.
        Otherwise, assume that they are names (i.e., dictionaries), and return IDs for the corresponding name;
        in this case `name` can be either a single name, or a tuple of 2 names, one for ``sid`` and one for ``mid``.
        If either of these names is ``None``, return ``None`` for the corresponding ID.
        """
        if name is None:
            name=self.sn
        if name=="all" or name is None:
            return self.sid,self.mid
        sid=self.sid[name]
        mid=None if self.mid is None else self.mid[name]
        return sid,mid
    def _build_copy_arg(self, name, *arg):
        if arg:
            return arg[0]
        value=getattr(self,name)
        if isinstance(value,dict):
            return dict(value)
        if isinstance(value,list):
            return list(value)
        return value
    def copy(self, *args, **kwargs):
        """
        Make a copy of the message
        
        Any specified keyword parameter replaces or adds to the current message parameter.
        """
        kwargs.update(dict(zip(self._init_args,args)))
        for ca in self._init_args:
            try:
                kwargs[ca]=self._build_copy_arg(ca,*([kwargs[ca]] if ca in kwargs else []))
            except KeyError:
                pass
        return type(self)(**kwargs)


class MetainfoAccessor:
    """Accessor which exposes metainfo dictionary values as attributes"""
    def __init__(self, msg):
        self.msg=msg
    def __getattr__(self, name):
        return self.msg.metainfo[name]
class DataStreamMessage(IStreamMessage):
    """
    A generic data stream message.

    In addition to :class:`IStreamMessage`, carries some information about the message and its source.

    Args:
        source: data source, e.g., daq, camera, processor, etc.
        tag: extra message tag
        creation_time: message creation time (if ``None``, use current time)
        metainfo: additional metainfo dictionary; the contents is arbitrary, but it's assumed to be message-wide, i.e., common for all frames in the message;
            `source`, `tag`, and `creation_time` are stored there.
    
    All of the supplied additional data (source, tag, etc.) is automatically added in the metainfo dictionary.
    It can be either directly, e.g., ``msg.metainfo["source"]``, or through the ``.mi`` accessor, e.g., ``msg.mi.source``.
    """
    def __init__(self, source=None, tag=None, creation_time=None, metainfo=None, sn=None, sid=None, mid=None):
        super().__init__(sn=sn,sid=sid,mid=mid)
        self.metainfo=metainfo or {}
        self._add_metainfo_args(source=source,tag=tag,creation_time=creation_time)
        if "creation_time" not in self.metainfo:
            self.metainfo["creation_time"]=time.time()
        self.mi=MetainfoAccessor(self)

    _metainfo_args={"source","tag","creation_time"}  # creation arguments which are automatically added to the metainfo
    def _add_metainfo_args(self, **kwargs):
        for k,v in kwargs.items():
            if v is not None:
                self.metainfo[k]=v
    def _build_copy_arg(self, name, *arg):
        if name in self._metainfo_args:  # already in metainfo
            return arg[0] if arg else None
        if name=="metainfo" and arg:
            uvalue=dict(self.metainfo)
            uvalue.update(arg[0])
            return uvalue
        return super()._build_copy_arg(name,*arg)

class GenericDataStreamMessage(DataStreamMessage):
    """
    Generic data stream message, which contains arbitrary data.

    All methods and attributes (except ``data``) are the same as :class:`DataStreamMessage`.
    """
    def __init__(self, data=None, source=None, tag=None, creation_time=None, metainfo=None, sn=None, sid=None, mid=None):
        super().__init__(source=source,tag=tag,creation_time=creation_time,metainfo=metainfo,sn=sn,sid=sid,mid=mid)
        self.data=data






class DataBlockMessage(DataStreamMessage):
    """
    A message containing a block of several aligned streams of data (e.g., several daq channels, or aligned data streams).

    Also has methods for simple data extraction/modification.

    Args:
        data: dictionary ``{name: values}`` of data chunks corresponding to each stream. All values should have the same length
        order: default order of the data channels (used when they are returned as a list instead of a dictionary); by default, use the dictionary keys ord
        source: data source, e.g., daq, camera, processor, etc.
        tag: extra message tag
        creation_time: message creation time (if ``None``, use current time)
        metainfo: additional metainfo dictionary; the contents is arbitrary, but it's assumed to be message-wide, i.e., common for all frames in the message;
            `source`, `tag`, and `creation_time` are stored there.
    
    All of the supplied additional data (source, tag, etc.) is automatically added in the metainfo dictionary.
    It can be either directly, e.g., ``msg.metainfo["source"]``, or through the ``.mi`` accessor, e.g., ``msg.mi.source``.
    """
    def __init__(self, data, order=None, source=None, tag=None, creation_time=None, metainfo=None, sn=None, sid=None, mid=None):
        super().__init__(source=source,tag=tag,creation_time=creation_time,metainfo=metainfo,sn=sn,sid=sid,mid=mid)
        self.data=data
        self.order=order or list(data)
        if set(self.order)!=set(self.data):
            raise ValueError("data channels order doesn't agree with supplied data channels")
        lch=None,None
        for name,col in data.items():
            if lch[0] is None:
                lch=name,len(col)
            elif len(col)!=lch[1]:
                raise ValueError("channel length doesn't agree: {} for {} vs {} for {}".format(name,len(col),*lch))

    def __len__(self):
        for ch in self.data:
            return len(self.data[ch])
        return 0
    def __bool__(self):
        return len(self)>0

    def __getitem__(self, key):
        return self.data[key]
    def __contains__(self, key):
        return key in self.data

    def filter_columns(self, include=None, exclude=None, strict=True):
        """
        Filter data columns to include and excluded the columns with the given names.

        If ``strict==True`` some of column in `include` are not present in the message, raise an exception.
        """
        if strict and include is not None:
            for ch in include:
                if ch not in self.data:
                    raise KeyError("included data channel {} is missing".format(ch))
        data=set()
        for ch in self.data:
            if include is None or ch in include:
                if exclude is None or ch not in exclude:
                    data.add(ch)
        self.data={ch:val for ch,val in self.data.items() if ch in data}
        self.order=[ch for ch in self.order if ch in data]
        
    def cut_to_size(self, n, from_end=False):
        """
        Cut the message to contain at most ``n`` rows.

        If ``from_end==True``, leave the last `n` rows; otherwise, leave the first `n` rows.
        Return ``True`` if the cut message contains `n` row (i.e., its original length was ``>=n``), and ``False`` otherwise.
        """
        if n==0:
            self.data={ch:[] for ch in self.data}
            return True
        for ch in list(self.data):
            col=self.data[ch]
            if len(col)<n:
                return False
            self.data[ch]=col[-n:] if from_end else col[:n]
        return True
    
    def _normalize_rng(self, rng):
        l=len(self)
        if isinstance(rng,tuple):
            if rng[1] is None:
                rng=rng[0],l
        elif rng>=0:
            rng=0,rng
        else:
            rng=rng,l
        return rng
    def get_data_columns(self, channels=None, rng=None):
        """
        Get table data as a list of columns.
        
        Args:
            channels: list of channels to get; all channels by default (in which case, order is determined by internal ``order`` variable)
            rng: optional cut range for the resulting data; can be a single number (positive to cut from the beginning, negative from the end),
                or a tuple ``(start, end)``.
        """
        order=channels or self.order
        if rng is None:
            return [self.data[ch] for ch in order]
        rng=self._normalize_rng(rng)
        return [self.data[ch][rng[0]:rng[1]] for ch in order]
    def get_data_rows(self, channels=None, rng=None):
        """
        Get table data as a list of rows.
        
        Args:
            channels: list of channels to get; all channels by default
            rng: optional cut range for the resulting data; can be a single number (positive to cut from the beginning, negative from the end),
                or a tuple ``(start, end)``.
        """
        return list(zip(*self.get_data_columns(channels=channels,rng=rng)))
    def get_data_dict(self, channels=None, rng=None):
        """
        Get table data as a dictionary ``{name: column}``.
        
        Args:
            channels: list of channels to get; all channels by default
            rng: optional cut range for the resulting data; can be a single number (positive to cut from the beginning, negative from the end),
                or a tuple ``(start, end)``.
        """
        order=channels or self.order
        if rng is None:
            return dict(self.data)
        rng=self._normalize_rng(rng)
        return {ch:self.data[ch][rng[0]:rng[1]] for ch in order}







class FramesMessage(DataStreamMessage):
    """
    A message containing a frame bundle and associated information (indices, etc.).

    Also has methods for simple data extraction/modification.

    Args:
        frames: list of frames (2D or 3D numpy arrays for 1 or more frames)
        indices: list of frame indices (if a corresponding array contains several frames, it can be the index of the first frame);
            if ``None``, autofill starting from 0
        frame_info: list of frame chunk infos (one per frame);
            if ``None``, keep as ``None``
        source: frames source, e.g., camera or processor
        tag: extra batch tag
        creation_time: message creation time (if ``None``, use current time)
        step: expected index step between the frames
        chunks: if ``True``, force all `frames` elements to be chunks (of length 1 if necessary);
            otherwise, if all of them are single-frame 2D arrays, keep them this way
        metainfo: additional metainfo dictionary; the contents is arbitrary, but it's assumed to be message-wide, i.e., common for all frames in the message;
            `source`, `tag`, `creation_time`, and `step` are stored there;
            common additional keys are ``"status_line"`` (expected position of the status line), or ``"frame_info_field"`` (fields name for frame-info entries)
    
    All of the supplied additional data (source, tag, etc.) is automatically added in the metainfo dictionary.
    It can be either directly, e.g., ``msg.metainfo["source"]``, or through the ``.mi`` accessor, e.g., ``msg.mi.source``.
    """
    def __init__(self, frames, indices=None, frame_info=None, source=None, tag=None, creation_time=None, step=1, chunks=False, metainfo=None, sn=None, sid=None, mid=None):
        super().__init__(source=source,tag=tag,creation_time=creation_time,metainfo=metainfo,sn=sn,sid=sid,mid=mid)
        self._add_metainfo_args(step=step)
        if isinstance(frames,tuple):
            frames=list(frames)
        elif not isinstance(frames,list):
            frames=[frames]
        self.frames=frames
        if indices is not None:
            if isinstance(indices,tuple):
                indices=list(indices)
            elif not isinstance(indices,list):
                indices=[indices]
            if len(indices)!=len(self.frames):
                raise ValueError("index array length {} is different from the frames array length {}".format(len(indices),len(self.frames)))
        self.indices=indices
        if frame_info is not None:
            if isinstance(frame_info,tuple):
                frame_info=list(frame_info)
            elif not isinstance(frame_info,list):
                frame_info=[frame_info]
            if len(frame_info)!=len(self.frames):
                raise ValueError("frame info array length {} is different from the frames array length {}".format(len(frame_info),len(self.frames)))
        self.frame_info=frame_info
        self.chunks=chunks
        self._setup_chunks()

    def __len__(self):
        return len(self.frames)
    def __bool__(self):
        return len(self)>0

    _metainfo_args=DataBlockMessage._metainfo_args|{"step"}
    def _setup_chunks(self):
        frames=self.frames
        if not self.chunks:
            self.chunks=any([f.ndim>2 for f in frames])
        if self.chunks:
            self.frames=[f[None] if f.ndim==2 else f for f in frames]
        if self.indices is None:
            if self.chunks:
                self.indices=[0]+list(np.cumsum([len(f) for f in self.frames]))[:-1]
            else:
                self.indices=list(range(len(self.frames)))
        elif self.chunks:
            step=self.mi.step
            for i,f in enumerate(self.frames):
                idx=self.indices[i]
                if np.ndim(idx)==0:
                    self.indices[i]=np.arange(idx,idx+f.shape[0]*step,step)
                elif len(f)!=len(idx):
                    raise ValueError("frames and indices array lengths don't agree: {} vs {}".format(len(f),len(idx)))
            if self.frame_info is not None:
                for i,f in enumerate(self.frames):
                    inf=self.frame_info[i]
                    if np.ndim(inf)!=2:
                        raise ValueError("frame info should be a 2-dimensional array in the chunk mode")
                    if len(inf)!=len(f):
                        raise ValueError("frames and indices array lengths don't agree: {} vs {}".format(len(f),len(inf)))

    def nframes(self):
        """Get total number of frames (taking into account that 3D array elements contain multiple frames)"""
        return sum([len(f) for f in self.frames]) if self.chunks else len(self.frames)
    def nbytes(self):
        """Get total size of the frames in the message in bytes"""
        return sum([f.nbytes for f in self.frames])

    def get_missing_frames_number(self, last_frame=None):
        """
        Check the message for missing frames.

        If `last_frame` is not ``None``, it should be the index of the frame preceding this block.
        Assume that the missing frames are only between the blocks.
        Return number of missing frames.
        """
        chunks=self.chunks
        missing=0
        for i in self.indices:
            fi,li=(i[0],i[-1]) if chunks else (i,i)
            if last_frame is not None:
                missing+=fi-last_frame-self.mi.step
            last_frame=li
        return missing
    
    def get_frames_stack(self, n=None, reverse=False, copy=True):
        """
        Get a list of at most `n` frames from the message (if ``None``, return all frames).

        If ``reverse==True``, return last `n` frames (in the reversed order); otherwise, return first `n` frames.
        If ``copy==True``, copy frames (otherwise changing the returned frames can affect the stored frames).
        """
        if n==0:
            return []
        if reverse:
            frames,_,_=self.get_slice((0 if n is None else -n),None,flatten=True,copy=copy)  # pylint: disable=invalid-unary-operand-type
            frames=frames[::-1]
        else:
            frames,_,_=self.get_slice(0,n,flatten=True,copy=copy)
        return frames
    def get_slice(self, start=None, end=None, step=1, copy=False, flatten=False):
        """
        Take a slice of frames within this message.

        A generalization of :meth:`get_frames_stack`, where both start and stop position can be set, as well as frame period.
        Return a tuple ``(frames, indices, frame_info)`` for the frames with the corresponding indices.
        If ``flatten==True`` and the message contains frame chunks (as opposed to individual frames in a list),
        "flatten" the chunks and return a lists of individual frames and indices; otherwise, these lists would contain chunks.
        """
        n=self.nframes()
        if step<0:
            raise ValueError("only positive step can be used")
        if start is None:
            start=0
        elif start<0:
            start=max(start+n,0)
        if end is None:
            end=n
        elif end<0:
            end=max(end+n,0)
        if self.chunks:
            frames=[]
            indices=[]
            frame_info=None if self.frame_info is None else []
            pos=0
            for i,ch in enumerate(self.frames):
                if pos>=end:
                    break
                l=len(ch)
                s=start-pos
                if s<0:
                    s%=step
                e=end-pos
                if s<l:
                    frames.append(ch[s:e:step])
                    indices.append(self.indices[i][s:e:step])
                    if frame_info is not None:
                        frame_info.append(self.frame_info[i][s:e:step])
                pos+=l
            if copy:
                frames=[f.copy() for f in frames]
                indices=[idx.copy() for idx in indices]
                if frame_info is not None:
                    frame_info=[inf.copy() for inf in frame_info]
            if flatten:
                frames=[f for ch in frames for f in ch]
                indices=[idx for ch in indices for idx in ch]
                if frame_info is not None:
                    frame_info=[inf for ch in frame_info for inf in ch]
        else:
            frames=self.frames[start:end:step]
            indices=self.indices[start:end:step]
            frame_info=None if self.frame_info is None else self.frame_info[start:end:step]
            if copy:
                frames=[f.copy() for f in frames]
        return frames,indices,frame_info
    def cut_to_slice(self, start, end, step=1):
        """Cut the frame message to only contain frames given by the slice"""
        self.frames,self.indices,self.frame_info=self.get_slice(start,end,step=step)
    def cut_to_size(self, n, from_end=False):
        """
        Cut contained data to contain at most `n` frames.

        If ``from_end==True``, leave last `n` frames; otherwise, leave first `n` frames.
        Return ``True`` if there are `n` frames after the cut, and ``False`` if there are less than `n`.
        """
        if n==0:
            self.frames=[]
            self.indices=[]
            self.frame_info=None if self.frame_info is None else []
            return True
        start,end=(-n,None) if from_end else (0,n)
        self.cut_to_slice(start,end)
        return self.nframes()==n
        
    def first_frame_index(self):
        """Get index of the first frame (or ``None`` if there are no frames)"""
        if not self.frames:
            return None
        return self.indices[0][0] if self.chunks else self.indices[0]
    def last_frame_index(self):
        """Get index of the last frame (or ``None`` if there are no frames)"""
        if not self.indices:
            return None
        return self.indices[-1][-1] if self.chunks else self.indices[-1]
    def first_frame(self, copy=True):
        """Get the first frame (or ``None`` if there are no frames)"""
        if not self.frames:
            return None
        frame=self.frames[0][0] if self.chunks else self.frames[0]
        return frame.copy() if copy else frame
    def last_frame(self, copy=True):
        """Get the last frame (or ``None`` if there are no frames)"""
        if not self.indices:
            return None
        frame=self.frames[-1][-1] if self.chunks else self.frames[-1]
        return frame.copy() if copy else frame
    def first_frame_info(self):
        """Get info of the first frame (or ``None`` if there are no frames)"""
        if not self.frame_info:
            return None
        return self.frame_info[0][0] if self.chunks else self.frame_info[0]
    def last_frame_info(self):
        """Get info of the last frame (or ``None`` if there are no frames)"""
        if not self.frame_info:
            return None
        return self.frame_info[-1][-1] if self.chunks else self.frame_info[-1]



TFramesDataChunk=collections.namedtuple("TFramesDataChunk",["frame","index","info","len","chunks"])
class FramesAccumulator:
    """
    Frames message accumulator.

    Can accumulate results from several consecutive messages and cut/extract frames similar to the messages.
    """
    def __init__(self):
        self.data=[]
    def add_message(self, msg):
        """Add a new message to the storage"""
        frames,indices,frame_info=msg.frames,msg.indices,msg.frame_info
        if frame_info is None:
            frame_info=[None]*len(frames)
        chunks=[TFramesDataChunk(f,idx,inf,(len(f) if msg.chunks else 1),msg.chunks) for (f,idx,inf) in zip(frames,indices,frame_info)]
        self.data+=chunks
    def nframes(self):
        """Get total number of stored frames"""
        return sum(ch.len for ch in self.data)
    def _expand_chunk(self, ch, flatten):
        if ch.chunks and flatten:
            info=ch.info if ch.info is not None else [None]*len(ch.frame)
            return zip(ch.frame,ch.index,info)
        return [(ch.frame,ch.index,ch.info)]
    def _take_slice_chunks(self, start, end=None, step=1, copy=False):
        n=self.nframes()
        if not n:
            return [],False
        if start is None:
            start=0 if step>0 else n-1
        elif start<0 and step>0:
            start=max(start+n,0)
        if end is None:
            end=n if step>0 else -1
        elif end<0 and step>0:
            end=max(end+n,0)
        chunks=any(ch.chunks for ch in self.data)
        if chunks:
            data=[]
            pos=0
            for ch in self.data:
                if pos>=end:
                    break
                s=start-pos
                if s<0:
                    s%=step
                e=end-pos
                if s<ch.len:
                    if ch.chunks:
                        frame=ch.frame[s:e:step]
                        index=ch.index[s:e:step]
                        info=ch.info[s:e:step] if ch.info is not None else None
                        nlen=len(frame)
                    else:
                        frame,index,info=ch.frame,ch.index,ch.info
                        nlen=1
                    if copy:
                        frame=frame.copy()
                        if ch.chunks:
                            index=index.copy()
                            if info is not None:
                                info=info.copy()
                    data.append(TFramesDataChunk(frame,index,info,nlen,ch.chunks))
                pos+=ch.len
        else:
            data=self.data[start:end:step]
        return data,chunks
    def get_slice(self, start, end=None, step=1, copy=False, flatten=False):
        """
        Get a list of at most `n` frames from the message (if ``None``, return all frames).

        If ``reverse==True``, return last `n` frames (in the reversed order); otherwise, return first `n` frames.
        If ``copy==True``, copy frames (otherwise changing the returned frames can affect the stored frames).
        """
        data,chunks=self._take_slice_chunks(start,end,step,copy=copy)
        if data:
            if chunks:
                frames,indices,frame_info=list(zip(*[r for ch in data for r in self._expand_chunk(ch,flatten)]))
            else:
                frames,indices,frame_info=list(zip(*[ch[:3] for ch in data]))
        else:
            frames,indices,frame_info=[],[],[]
        if all(inf is None for inf in frame_info):
            frame_info=None
        return frames,indices,frame_info
    def cut_to_slice(self, start, end, step=1):
        """Cut the accumulator to only contain frames given by the slice"""
        self.data,_=self._take_slice_chunks(start,end,step,copy=False)
    def cut_to_size(self, n, from_end=False):
        """
        Cut contained data to contain at most `n` frames.

        If ``from_end==True``, leave last `n` frames; otherwise, leave first `n` frames.
        Return ``True`` if there are `n` frames after the cut, and ``False`` if there are less than `n`.
        """
        if n==0:
            self.data=[]
        elif from_end:
            self.cut_to_slice(-n,None)
        else:
            self.cut_to_slice(0,n)
        return self.nframes()==n
    def clear(self):
        """Clear the stored frames"""
        self.data=[]