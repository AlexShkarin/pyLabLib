from ...core.utils import functions

import time

import numpy as np






class IStreamMessage:
    """
    A generic message belonging to a stream.

    Args:
        sn: stream name (usually, references to the stream original source or purpose); could be ``None``, implying an "anonymous" stream
        sid: session numerical ID, a unique ID (usually an incrementing number) which is different for different streaming sessions
        mid: message numerical ID, a unique ID (usually an incrementing number) of the message within the stream
    
    Either `mid` or both IDs can be ``None``, indicating that the corresponding stream does not keep track of these IDs.
    In addition, `sid` and `mid` can be dictionaries (preferrably with the same keys), which indicates that this message
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
        frame_info: list of frame chunk infos (one entry per chunk);
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
                self.indices=[0]+list(np.cumsum([len(f) for f in self.frames]))
            else:
                self.indices=list(range(len(self.frames)))
        elif self.chunks:
            if self.indices is not None:
                step=self.mi.step
                for i,f in enumerate(self.frames):
                    idx=self.indices[i]
                    if np.ndim(idx)==0:
                        self.indices[i]=np.arange(idx,idx+f.shape[0]*step,step)
                    elif len(f)!=len(idx):
                        raise ValueError("frames and indices array lengths don't agree: {} vs {}".format(len(f),len(idx)))

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
    
    def get_frames_stack(self, n=None, reverse=False, add_indices=False, copy=True):
        """
        Get a list of at most `n` frames from the message (if ``None``, return all frames).

        If ``reverse==True``, return last `n` frames (in the reversed order); otherwise, return first `n` frames.
        If ``add_indices==True``, elements of the list are tuples ``(index, img)``; otherwise, they are just images.
        If ``copy==True``, copy frames (otherwise changing the returned frames can affect the stored frames).
        """
        if n==0:
            return []
        if n is None:
            n=self.nframes()
        frames=[]
        indices=[]
        if self.chunks:
            if reverse:
                for i,f in zip(self.indices[::-1],self.frames[::-1]):
                    chunk=f[:-(n-len(frames))-1:-1]
                    add_frames=list(chunk.copy()) if copy else list(chunk)
                    frames+=add_frames
                    if add_indices:
                        indices+=list(i[:-(n-len(frames))-1:-1])
                    if len(frames)>=n:
                        break
            else:
                for i,f in zip(self.indices,self.frames):
                    chunk=f[:n-len(frames)]
                    add_frames=list(chunk.copy()) if copy else list(chunk)
                    frames+=add_frames
                    if add_indices:
                        indices+=list(i[:n-len(frames)])
                    if len(frames)>=n:
                        break
        else:
            frames=self.frames[-n:][::-1] if reverse else self.frames[:n]  # pylint: disable=invalid-unary-operand-type
            if copy:
                frames=[f.copy() for f in frames]
            if add_indices:
                indices=self.indices[-n:][::-1] if reverse else self.indices[:n]  # pylint: disable=invalid-unary-operand-type
        return list(zip(indices,frames)) if add_indices else frames
    def cut_to_size(self, n, from_end=False):
        """
        Cut contained data to contain at most `n` frames.

        If ``from_end==True``, leave last `n` frames; otherwise, leave first `n` frames.
        Return ``True`` if there are `n` frames after the cut, and ``False`` if there are less than `n`.
        """
        if n==0:
            self.data={k:[] for k in self.data}
            return True
        if self.chunks:
            end=None
            size=0
            d=-1 if from_end else 1
            frames=self.frames[::d]
            indices=self.indices[::d]
            for i,f in enumerate(frames):
                if size+len(f)>n:
                    end=i
                    break
                size+=len(f)
            if end is None:
                return size<n
            new_frames=frames[:end]
            new_indices=indices[:end]
            if size<n:
                if from_end:
                    new_frames.append(frames[end][-(n-size):])
                    new_indices.append(indices[end][-(n-size):])
                else:
                    new_frames.append(frames[end][:n-size])
                    new_indices.append(indices[end][:n-size])
            self.frames=new_frames[::d]
            self.indices=new_indices[::d]
            if self.frame_info is not None:
                self.frame_info=self.frame_info[::d][:len(new_frames)][::d]
        else:
            s=slice(-n,None) if from_end else slice(0,n)
            self.frames=self.frames[s]
            if self.indices is not None:
                self.indices=self.indices[s]
            if self.frame_info is not None:
                self.frame_info=self.frame_info[s]
            return len(self.frames)==n
        return True
        
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
        return self.frame_info[0]
    def last_frame_info(self):
        """Get info of the last frame (or ``None`` if there are no frames)"""
        if not self.frame_info:
            return None
        return self.frame_info[-1]