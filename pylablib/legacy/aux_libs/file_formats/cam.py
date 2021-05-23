"""
Standard .cam format.

A .cam file is a set of frames (in raw binary <u2 format),
each of which is prepended by two 4-byte integers denoting the frame dimensions.
"""


from ...core.utils import files as file_utils

import os.path
import numpy as np




def _read_cam_frame(f, skip=False):
    size=np.fromfile(f,"<u4",count=2)
    if len(size)==0 and file_utils.eof(f):
        raise StopIteration
    if len(size)<2:
        raise IOError("not enough cam data to read the frame size")
    w,h=size
    if not skip:
        data=np.fromfile(f,"<u2",count=w*h)
        if len(data)<w*h:
            raise IOError("not enough cam data to read the frame: {} pixels available instead of {}".format(len(data),w*h))
        return data.reshape((w,h))
    else:
        f.seek(w*h*2,1)
        return None

class CamReader(object):
    """
    Reader class for .cam files.

    Allows transparent access to frames by reading them from the file on the fly (without loading the whole file).
    Supports determining length, indexing (only positive single-element indices) and iteration.

    Args:
        path(str): path to .cam file.
        same_size(bool): if ``True``, assume that all frames have the same size, which speeds up random access and obtaining number of frames;
            otherwise, the first time the length is determined or a large-index frame is accessed can take a long time (all subsequent calls are faster).
    """
    def __init__(self, path, same_size=False):
        object.__init__(self)
        self.path=file_utils.normalize_path(path)
        self.frame_offsets=[0]
        self.frames_num=None
        self.same_size=same_size

    def _read_frame_at(self, offset):
        with open(self.path,"rb") as f:
            f.seek(offset)
            return _read_cam_frame(f)
    def _read_next_frame(self, f, skip=False):
        data=_read_cam_frame(f,skip=skip)
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






##### Simple interface functions #####
def iter_cam_frames(path, start=0, step=1):
    """
    Iterate of frames in a .cam datafile.

    Yield 2D array (one array per frame).
    Frames are loaded only when yielded, so the function is suitable for large files.
    """
    return CamReader(path).iterrange(start,None,step)
def load_cam(path, same_size=True):
    """
    Load .cam datafile.

    Return list of 2D numpy arrays, one array per frame.
    If ``same_size==True``, raise error if different frames have different size.
    """
    frames=[]
    for f in iter_cam_frames(path):
        if same_size and frames and f.shape!=frames[0].shape:
            raise IOError("camera frame {} has a different size: {}x{} instead of {}x{}".format(len(frames),*(f.shape+frames[0].shape)))
        frames.append(f)
    return frames
def combine_cam_frames(path, func, init=None, start=0, step=1, max_frames=None, return_total=False):
    """
    Combine .cam frames using the function `func`.

    `func` takes 2 arguments (the accumulated result and a new frame) and returns the combined result.
    `init` is the initial result value; if ``init is None`` it is initialized to the first frame.
    If `max_frames` is not ``None``, it specifies the maximal number of frames to read.
    If ``return_total==True'``, return a tuple ``(result, n)'``, where `n` is the total number of frames.
    """
    n=0
    result=init
    for f in iter_cam_frames(path,start=start,step=step):
        if result is None:
            result=f
        else:
            result=func(result,f)
        n+=1
        if max_frames and n>=max_frames:
            break
    return (result,n) if return_total else result


def save_cam(frames, path, append=True):
    """
    Save `frames` into a .cam datafile.

    If ``append==False``, clear the file before writing the frames.
    """
    mode="ab" if append else "wb"
    with open(path,mode) as f:
        for fr in frames:
            np.array(fr.shape).astype("<u4").tofile(f)
            fr.astype("<u2").tofile(f)