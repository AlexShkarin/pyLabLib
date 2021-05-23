from ...core.utils import py3, general, funcargparse, files as file_utils
from ...core.devio import data_format
from ...core.fileio import binio

import numpy as np
import numpy.random

import time, collections, os.path, zlib, pickle


def gen_uid():
    uid_arr=numpy.random.randint(0,256,size=8,dtype="u1")
    return py3.as_bytes(uid_arr)


class ECamFrame(object):
    """
    A data frame for .ecam format.

    Args:
        data: frame data (numpy array with between 1 and 4 dimensions)
        uid(bytes): 8-byte unique ID of the frame (by default, generate a new random ID).
        timetamps(float): frame timestamp (by default, use current time)
        **kwargs: additional frame blocks (values and meaning depend on the block type, and can be expanded later)
    """
    def __init__(self, data, uid="new", timestamp="new", **kwargs):
        object.__init__(self)
        self.data=data
        self.uid=gen_uid() if uid=="new" else uid
        self.timestamp=time.time() if timestamp=="new" else timestamp
        self.blocks=kwargs
    
    def __getitem__(self, key):
        return self.blocks[key]
    def __setitem__(self, key, value):
        self.blocks[key]=value

    def update_timestamp(self, timestamp=None):
        """Update the frame timestamp (by default, use current time)"""
        self.timestamp=timestamp or time.time()

    def uid_to_int(self):
        """Return UID as an 8-byte integer"""
        return int(np.frombuffer(self.uid,"<u8")[0]) if self.uid else None
    def uid_to_hex(self):
        """Return UID as a 16-symbol hex string"""
        return "".join(["{:02x}".format(d) for d in self.uid]) if self.uid else None






current_version=0x0001
valid_magic=b"eCAM\x0f64\x0b"
valid_versions=[0x0001]
default_pickle_proto=3
_header_fields=[("header_size",4),("image_bytes",8),("version",2),("magic",8),("shape",16),("dtype",2),("stype",2),
                ("uid",8),("timestamp",8)]
_hf_sizes=dict(_header_fields)
def _gen_offsets(fields):
    offsets={}
    off=0
    for n,s in fields:
        offsets[n]=off
        off+=s
    offsets["__end__"]=off
    return offsets
_hf_offsets=_gen_offsets(_header_fields)

THeader=collections.namedtuple("THeader",["header_size","image_bytes","version","shape","dtype","stype","uid","timestamp","blocks"])
stypes={0x00:"none",0x01:"raw",0x10:"zlib"}
stypes_inv=general.invert_dict(stypes)
dtypes=general.merge_dicts(binio.fdtypes,binio.idtypes)
dtypes_inv=general.invert_dict(dtypes)

TBlock=collections.namedtuple("TBlock",["btype","value"])
btypes={0x00:"none",0x01:"skip",0x10:"cam_params",0x20:"pickle"}
btypes_inv=general.invert_dict(btypes)
cam_params={0x01:("name","sp<u2"),0x02:("model","sp<u2"),0x03:("id","sp<u2"),
            0x10:("exposure","<f8"),0x11:("frame_rate","<f8"),
            0x20:("roi",("<u4",)*4),0x21:("binning",("<u2",)*2),0x22:("pixel_max","<u8"),0x23:("pixel_min","<i8"),
            0x30:("acq_mode","sp<u1"),0x31:("read_mode","sp<u1"),0x32:("pixel_mode","sp<u1"),
            0x38:("timing_mode","sp<u1"),0x39:("trigger_mode","sp<u1"),0x3a:("trigger_level","<f8"),
            0x40:("buffer_size","<u4"),0x41:("buffer_filled","<u4"),
            0x80:("status","sp<u2"),0x81:("acq_status","sp<u2")}
cam_params_inv=general.invert_dict(cam_params,kmap=lambda x: x[0])



class ECamFormatError(IOError):
    """Generic ECam reading error"""
    pass

class ECamFormatter(object):
    """
    Formatter for .ecam files.

    Class responsible for writing and reading arbitrary ECam frames.

    Args:
        stype(str): storage type for the data. Can be ``"raw"`` (write as raw binary),
            ``"zlib"`` (raw binary compressed using standard Python zlib module), or ``"none"`` (write zeros instead of data).
            Used only for writing; in reading, all storage types are supported.
        dtype: default data dtype. If suppled, any written data will be converted to this dtype,
            and any read data will have this dtype by default (unless specified explicitly). Otherwise, use supplied data dtype when writing.
        shape(tuple): default data shape (tuple of length 2 or 3). If suppled, any written and read data is supposed to have this shape
            (also use this as default shape if none is provided in the file).
    """
    def __init__(self, stype="raw", dtype=None, shape=(None,None)):
        object.__init__(self)
        self.stype=stype
        self.dtype=dtype
        self.shape=shape
    
    def _build_frame(self, header, data):
        blocks={}
        for btype,bvalue in header.blocks:
            if btypes[btype]=="pickle":
                name,val=bvalue
                blocks.setdefault("pickle",{})[name]=val
            elif btypes[btype]=="cam_params":
                blocks["cam_params"]=bvalue
        return ECamFrame(data,header.uid,header.timestamp,**blocks)
    def _read_block(self, f, btype, size):
        if btype not in btypes:
            raise ECamFormatError("bad file format: unknown block type 0x{:04x}".format(btype))
        btype=btypes[btype]
        if btype=="skip":
            f.seek(size,1)
            value=size
        elif btype=="pickle":
            ipos=f.tell()
            parsize=binio.read_num(f,"<u2")
            f.seek(parsize,1)
            name=binio.read_str(f,"sp<u4")
            header_size=(f.tell()-ipos)
            if size>=header_size:
                svalue=f.read(size-header_size)
                value=(name,pickle.loads(svalue))
            else:
                raise ECamFormatError("error reading block: block size {} is too small".format(size))
        elif btype=="cam_params":
            value={}
            epos=f.tell()+size
            while f.tell()<epos:
                pid=binio.read_num(f,"u1")
                if pid not in cam_params:
                    raise ECamFormatError("error reading block: unknown camera param id 0x{:02x}".format(pid))
                name,dtype=cam_params[pid]
                value[name]=binio.read_val(f,dtype)
        return value
    def _read_header(self, f):
        try:
            header_size=binio.read_num(f,"<u4")
        except IndexError:
            raise StopIteration
        if header_size in {0,4} or (header_size<_hf_offsets["__end__"] and header_size not in _hf_offsets.values()):
            raise ECamFormatError("bad file format: header size is {}".format(header_size))
        image_bytes=binio.read_num(f,"<u8")
        if header_size>_hf_offsets["version"]:
            version=binio.read_num(f,"<u2")
            if version not in valid_versions:
                raise ECamFormatError("bad file format: unsupported version 0x{:02x}".format(version))
        else:
            version=None
        if header_size>_hf_offsets["magic"]:
            magic=f.read(8)
            if magic!=valid_magic:
                raise ECamFormatError("bad file format: invalid magic {}".format(magic))
        if header_size>_hf_offsets["shape"]:
            shape=binio.read_val(f,("<u4",)*4)
        else:
            shape=self.shape
        shape=tuple([s for s in shape if s!=0])
        if (None not in self.shape) and shape!=self.shape:
            raise ValueError("data shape {} doesn't agree with the formatter shape {}".format(shape,self.shape))
        dtype=binio.read_num(f,"<u2") if header_size>_hf_offsets["dtype"] else self.dtype
        stype=binio.read_num(f,"<u2") if header_size>_hf_offsets["stype"] else self.stype
        uid=f.read(8) if header_size>_hf_offsets["uid"] else None
        timestamp=binio.read_num(f,"<f8") if header_size>_hf_offsets["timestamp"] else None
        read_bytes=_hf_offsets["__end__"]
        blocks=[]
        while header_size>read_bytes:
            if read_bytes+2>header_size:
                raise ECamFormatError("bad file format: not enough data for a block type")
            btype=binio.read_num(f,"<u2")
            if btype==0x00:
                f.seek(header_size-(read_bytes+2))
                read_bytes=header_size
                break
            if read_bytes+6>header_size:
                raise ECamFormatError("bad file format: not enough data for a block size")
            bsize=binio.read_num(f,"<u4")
            bvalue=self._read_block(f,btype,bsize)
            blocks.append(TBlock(btype,bvalue))
            read_bytes+=(6+bsize)
        return THeader(header_size,image_bytes,version,shape,dtype,stype,uid,timestamp,blocks)
    def _check_data_size(self, df, shape, data_bytes):
        nelem=int(np.prod(shape,dtype="u8"))
        if df.size*nelem!=data_bytes:
            shape_str="x".join([str(s) for s in shape])
            raise ECamFormatError("bad file format: mismatched frame byte size: expect {}x{}={}, got {}".format(
                shape_str,df.size,nelem*df.size,data_bytes))
    def _read_data(self, f, header):
        if header.stype is None:
            raise ECamFormatError("bad file format: not enough header data to read image")
        if header.stype not in stypes:
            raise ECamFormatError("bad file format: unknown storage type 0x{:04x}".format(header.stype))
        stype=stypes[header.stype]
        if stype=="none":
            f.seek(header.image_bytes,1)
            return None
        if (None in header.shape) or header.dtype is None:
            raise ECamFormatError("bad file format: not enough header data to read image")
        if header.dtype not in dtypes:
            raise ECamFormatError("bad file format: unknown data type 0x{:04x}".format(header.dtype))
        dtype=dtypes[header.dtype]
        df=data_format.DataFormat.from_desc(dtype)
        nelem=int(np.prod(header.shape,dtype="u8"))
        if stype=="raw":
            self._check_data_size(df,header.shape,header.image_bytes)
            img=np.fromfile(f,dtype=df.to_desc(),count=nelem)
            if len(img)!=nelem:
                raise ECamFormatError("bad file format: expected {} elements, found {}".format(nelem,len(img)))
            img=img.reshape(header.shape)
        elif stype=="zlib":
            comp_data=f.read(header.image_bytes)
            raw_data=zlib.decompress(comp_data)
            self._check_data_size(df,header.shape,len(raw_data))
            img=np.fromstring(raw_data,dtype=df.to_desc(),count=nelem).reshape(header.shape)
        return img
    def skip_frame(self, f):
        """Skip next frame starting at the current position within the file `f`"""
        header=self._read_header(f)
        f.seek(header.image_bytes,1)
        return header.header_size,header.image_bytes
    def read_frame(self, f, return_format="frame"):
        """
        Read next frame starting at the current position within the file `f`.
        
        `return_format` is the format for return data. Can be ``"frame"`` (return :class:`ECamFrame` object with all metadata),
        ``"image"`` (return only image array), or ``"raw"`` (return tuple ``(header, image)`` with raw data).
        """
        funcargparse.check_parameter_range(return_format,"return_format",{"frame","image","raw"})
        header=self._read_header(f)
        img=self._read_data(f,header)
        if return_format=="frame":
            return self._build_frame(header,img)
        elif return_format=="image":
            return img
        else:
            return header,img


    def _format_frame(self, frame):
        if isinstance(frame,ECamFrame):
            data=np.asarray(frame.data)
            uid=frame.uid
            timestamp=frame.timestamp
            fblocks=frame.blocks
        else:
            data=np.asarray(frame)
            uid,timestamp=None,None
            fblocks={}
        if self.dtype is not None:
            data=data.astype(self.dtype)
        if (None not in self.shape) and data.shape!=self.shape:
            raise ValueError("data shape {} doesn't agree with the formatter shape {}".format(data.shape,self.shape))
        if data.ndim not in [1,2,3,4]:
            raise ValueError("can only save 1D, 2D, 3D, and 4D arrays; got {}D".format(data.ndim))
        df=data_format.DataFormat.from_desc(str(data.dtype))
        dtype=df.to_desc()
        shape=data.shape
        if self.stype=="none":
            dsize=int(np.prod(data.shape,dtype="u8"))*df.size
            data=None
        elif self.stype=="raw":
            data=data.astype(dtype=dtype)
            dsize=int(np.prod(data.shape,dtype="u8"))*df.size
        elif self.stype=="zlib":
            raw_str=data.astype(dtype=dtype).tostring()
            data=zlib.compress(raw_str,level=1)
            dsize=len(data)
        else:
            raise ValueError("unrecognized storage type: {}".format(self.stype))
        blocks=[]
        for k,v in fblocks.items():
            if k=="pickle":
                btype=btypes_inv["pickle"]
                for pn,pv in v.items():
                    bvalue=(pn,pv)
                    blocks.append(TBlock(btype,bvalue))
            elif k=="cam_params":
                btype=btypes_inv["cam_params"]
                blocks.append(TBlock(btype,v))
        header=THeader(-1,dsize,current_version,shape,dtypes_inv[dtype],stypes_inv[self.stype],uid,timestamp,blocks)
        return header,data
    def _write_block(self, f, btype, bvalue):
        btype=btypes[btype]
        if btype=="skip":
            f.write(b"\x00"*bvalue)
        elif btype=="pickle":
            pn,pv=bvalue
            binio.write_num(2,f,"<u2")
            binio.write_num(default_pickle_proto,f,"<u2")
            binio.write_str(pn,f,"sp<u4")
            pickle.dump(pv,f,protocol=default_pickle_proto)
        elif btype=="cam_params":
            for pid,(pn,dtype) in cam_params.items():
                if pn in bvalue:
                    binio.write_num(pid,f,"u1")
                    v=bvalue[pn]
                    binio.write_val(v,f,dtype)
    def _write_header(self, header, f):
        with binio.size_prepend(f,"<u4",4):
            binio.write_num(header.image_bytes,f,"<u8")
            binio.write_num(header.version,f,"<u2")
            f.write(valid_magic)
            if None not in header.shape:
                shape=header.shape+(0,)*(4-len(header.shape))
                np.asarray(shape,dtype="u4").astype("<u4").tofile(f)
            else:
                return
            if header.dtype is not None:
                binio.write_num(header.dtype,f,"<u2")
            else:
                return
            if header.stype is not None:
                binio.write_num(header.stype,f,"<u2")
            else:
                return
            if header.uid is not None:
                f.write(header.uid)
            else:
                return
            if header.timestamp is not None:
                binio.write_num(header.timestamp,f,"<f8")
            else:
                return
            for btype,bvalue in header.blocks:
                binio.write_num(btype,f,"<u2")
                with binio.size_prepend(f,"<u4"):
                    self._write_block(f,btype,bvalue)
    def _write_image(self, header, data, f):
        if data is None:
            f.write("\x00"*header.image_bytes)
        elif isinstance(data,bytes):
            f.write(data)
        elif isinstance(data,np.ndarray):
            data.tofile(f)
        else:
            raise ValueError("don't know how to write data {}".format(data))
    def write_frame(self, frame, f):
        """
        Read the supplied `frame` starting at the current position within the file `f`.
        
        `frame` can be either :class:`ECamFrame` object, or a numpy array (in which case no metadata is saved).
        """
        header,data=self._format_frame(frame)
        self._write_header(header,f)
        self._write_image(header,data,f)
        return header.header_size,header.image_bytes





def save_ecam(frames, path, append=True, formatter=None):
    """
    Save `frames` into a .ecam datafile.

    If ``append==False``, clear the file before writing the frames.
    `formatter` specifies :class:`ECamFormatter` instance for frame saving.
    """
    mode="r+b" if (append and os.path.exists(path)) else "wb"
    formatter=formatter or ECamFormatter()
    with open(path,mode) as f:
        f.seek(0,2)
        for fr in frames:
            formatter.write_frame(fr,f)

def save_ecam_single(frame, path, append=True, **kwargs):
    """
    Save a single `frame` into a .ecam datafile.

    If ``append==False``, clear the file before writing the frames.
    ``**kwargs`` specify parameters passed to the :class:`ECamFormatter` constructor for the saving formatter.
    """
    formatter=ECamFormatter(**kwargs)
    save_ecam([frame],path,append=append,formatter=formatter)





class ECamReader(object):
    """
    Reader class for .ecam files.

    Allows transparent access to frames by reading them from the file on the fly (without loading the whole file).
    Supports determining length, indexing (only positive single-element indices) and iteration.

    Args:
        path(str): path to .ecam file.
        same_size(bool): if ``True``, assume that all frames have the same size (including header), which speeds up random access and obtaining number of frames;
            otherwise, the first time the length is determined or a large-index frame is accessed can take a long time (all subsequent calls are faster).
        return_format(str): format for return data. Can be ``"frame"`` (return :class:`ECamFrame` object with all metadata),
            ``"image"`` (return only image array), or ``"raw"`` (return tuple ``(header, image)`` with raw data).
        formatter(ECamFormatter): formatter for saving
    """
    def __init__(self, path, same_size=False, return_format="frame", formatter=None):
        object.__init__(self)
        self.path=file_utils.normalize_path(path)
        self.frame_offsets=[0]
        self.frames_num=None
        self.same_size=same_size
        self.return_format=return_format
        self.formatter=formatter or ECamFormatter()

    def _read_frame_at(self, offset):
        with open(self.path,"rb") as f:
            f.seek(offset)
            return self.formatter.read_frame(f,return_format=self.return_format)
    def _read_next_frame(self, f, skip=False):
        if skip:
            self.formatter.skip_frame(f)
            data=None
        else:
            data=self.formatter.read_frame(f,return_format=self.return_format)
        self.frame_offsets.append(f.tell())
        return data
    def _read_frame(self, idx):
        idx=int(idx)
        if self.same_size:
            if len(self.frame_offsets)==1:
                with open(self.path,"rb") as f:
                    self._read_next_frame(f,skip=True)
            offset=self.frame_offsets[1]*idx
            return self._read_frame_at(offset)
        else:
            if idx<len(self.frame_offsets):
                return self._read_frame_at(self.frame_offsets[idx])
            next_idx=len(self.frame_offsets)-1
            offset=self.frame_offsets[-1]
            with open(self.path,"rb") as f:
                f.seek(offset)
                while next_idx<=idx:
                    data=self._read_next_frame(f,next_idx<idx)
                    next_idx+=1
            return data

    def _fill_offsets(self):
        if self.frames_num is not None:
            return
        if self.same_size:
            file_size=os.path.getsize(self.path)
            if file_size==0:
                self.frames_num=0
            else:
                with open(self.path,"rb") as f:
                    self._read_next_frame(f,skip=True)
                if file_size%self.frame_offsets[1]:
                    raise IOError("File size {} is not a multiple of single frame size {}".format(file_size,self.frame_offsets[1]))
                self.frames_num=file_size//self.frame_offsets[1]
        else:
            offset=self.frame_offsets[-1]
            try:
                with open(self.path,"rb") as f:
                    f.seek(offset)
                    while True:
                        self._read_next_frame(f,skip=True)
            except StopIteration:
                pass
            self.frames_num=len(self.frame_offsets)-1
    
    def size(self):
        """Get the total number of frames"""
        self._fill_offsets()
        return self.frames_num
    __len__=size

    def __getitem__(self, idx):
        if isinstance(idx,slice):
            return list(self.iterrange(idx.start or 0,idx.stop,idx.step or 1))
        try:
            return self._read_frame(idx)
        except StopIteration:
            raise IndexError("index {} is out of range".format(idx))
    def get_data(self, idx):
        """Get a single frame at the given index (only non-negative indices are supported)"""
        return self[idx]
    def __iter__(self):
        return self.iterrange()
    def iterrange(self, *args):
        """
        iterrange([start,] stop[, step])

        Iterate over frames starting with `start` ending at `stop` (``None`` means until the end of file) with the given `step`.
        """
        start,stop,step=0,None,1
        if len(args)==1:
            stop,=args
        elif len(args)==2:
            start,stop=args
        elif len(args)==3:
            start,stop,step=args
        if step<0:
            raise IndexError("format doesn't support reversed indexing")
        try:
            n=start
            while True:
                yield self._read_frame(n)
                n+=step
                if stop is not None and n>=stop:
                    break
        except StopIteration:
            pass
    def read_all(self):
        """Read all available frames"""
        return list(self.iterrange())

def load_ecam(path, return_format="image"):
    """
    Read .ecam file.

    Args:
        path(str): path to .ecam file.
        return_format(str): format for return data. Can be ``"frame"`` (return :class:`ECamFrame` object with all metadata),
            ``"image"`` (return only image array), or ``"raw"`` (return tuple ``(header, image)`` with raw data).
    """
    return list(ECamReader(path,return_format=return_format).iterrange())