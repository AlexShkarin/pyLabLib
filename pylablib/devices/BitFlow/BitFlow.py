import os
import contextlib
import re

@contextlib.contextmanager
def _using_dll_folders():
    if hasattr(os,"add_dll_directory"):
        os_paths=os.environ.get("PATH","").split(os.pathsep)
        include_re=[r".*BitFlow.*\\Bin.*",r".*\\CameraLink\\Serial"]
        add_paths=[os.path.abspath(p) for p in os_paths if any(re.match(r,p,flags=re.IGNORECASE) for r in include_re)]
        added_dirs=[]
        try:
            for p in add_paths:
                try:
                    added_dirs.append(os.add_dll_directory(p)) # pylint: disable=no-member
                except OSError:  # missing folder
                    pass
            yield
        finally:
            for d in added_dirs:
                d.close()
    else:
        yield
try:
    with _using_dll_folders():
        from BFModule import BufferAcquisition
except ImportError:
    BufferAcquisition=None

def _check_library():
    if BufferAcquisition is None:
        msg=(   "operation requires Python BFModule library. You can download it from the BitFlow website and install following the provide instructions. "
                "If it is installed, check if it imports correctly by running 'import BFModule'")
        raise ImportError(msg)


from ...core.devio import interface, comm_backend
from ..interface import camera

import numpy as np
import collections
import ctypes
import threading
import xml.etree.ElementTree as ET
import tempfile


class BitFlowError(comm_backend.DeviceError):
    """Generic BitFlow devices error"""
class BitFlowTimeoutError(BitFlowError):
    """BitFlow frame timeout error"""



TDeviceInfo=collections.namedtuple("TDeviceInfo",["idx","model","idreg"])
def list_cameras():
    """List all cameras available through BitFlow interface"""
    _check_library()
    cameras=[]
    for i in range(8):
        Acq=BufferAcquisition.clsCircularAcquisition()
        try:
            Acq.Open(i,BufferAcquisition.OpenOptions.NoOpenErrorMess)
            model=Acq.GetBoardInfo(BufferAcquisition.InquireParams.Model)
            idreg=Acq.GetBoardInfo(BufferAcquisition.InquireParams.IDReg)
            cameras.append(TDeviceInfo(i,model,idreg))
            Acq.Close()
        except ValueError:
            pass
    return cameras
def get_cameras_number():
    """Get number of connected BitFlow cameras"""
    return len(list_cameras())




class BitFlowFrameGrabber(camera.IROICamera):
    """
    Generic BitFlow frame grabber interface.

    Compared to :class:`BitFlowCamera`, has more permissive initialization arguments,
    which simplifies its use as a base class for expanded cameras.

    Args:
        bitflow_idx: board index, starting from 0
        bitflow_camfile: if not ``None``, a path to a valid camera file used for this frame grabber and camera combination;
            in this case, a temporary camera file is generated based on the provided one and used to change some otherwise unavailable camera parameters
            such as ROI and pixel bit depth (they are otherwise fixed to whatever is specified in the default camera file)
        do_open: if ``False``, skip the last step of opening the device (should be opened in a subclass)
    """
    Error=BitFlowError
    TimeoutError=BitFlowTimeoutError
    def __init__(self, bitflow_idx=0, bitflow_camfile=None, do_open=True, **kwargs):
        _check_library()
        super().__init__(**kwargs)
        self.bitflow_idx=bitflow_idx
        self.bitflow_camfile=bitflow_camfile
        if bitflow_camfile is not None:
            self._camed=CameraFileEditor()
            try:
                self._camed.load(bitflow_camfile)
            except (OSError,ET.ParseError,ValueError):
                raise BitFlowError("could not open or parse camera file {}".format(bitflow_camfile))
        else:
            self._camed=None
        self._temp_folder=None
        self._max_detector_size=None
        self._acq=None
        self._buffer_mgr=self.BufferManager(self)
        self._frame_merge=1
        self._max_frame_merge=None
        
        self._add_info_variable("device_info",self.get_device_info)

        if do_open:
            self.open()


    def _get_connection_parameters(self):
        return self.bitflow_idx,self.bitflow_camfile
    def open(self):
        """Open connection to the camera"""
        super().open()
        if self._acq is None:
            self._acq=BufferAcquisition.clsCircularAcquisition()
            if self._camed is not None:
                if self._temp_folder is None:
                    self._temp_folder=tempfile.TemporaryDirectory()
                camfile=os.path.join(self._temp_folder.name,"camera_file.bfml")
                self._camed.save(camfile)
                self._acq.Open(self.bitflow_idx,camfile)
            else:
                self._acq.Open(self.bitflow_idx,BufferAcquisition.OpenOptions.NoOpenErrorMess)
            if self._max_detector_size is None:
                self._max_detector_size=self._get_grabber_data_dimensions_rc()
            self.stop_acquisition()
            try:
                self._acq.AqCleanup()
            except RuntimeError:
                pass
    def close(self):
        """Close connection to the camera"""
        if self._acq is not None:
            self.clear_acquisition()
            if self._acq.isBoardOpen():
                self._acq.Close()
            self._acq=None
            if self._temp_folder is not None:
                self._temp_folder.cleanup()
                self._temp_folder=None
        super().close()
    def is_opened(self):
        """Check if the device is connected"""
        return bool(self._acq is not None and self._acq.isBoardOpen())
    def _change_board_parameters(self, size=None, fmt=None, bpp=None):
        if self._camed is None:
            return False
        if any(v is not None for v in [size,fmt,bpp]):
            if size is not None:
                size=(size[0],size[1]*self._frame_merge)
            if self._camed.set_mode_parameters(size=size,fmt=fmt,bpp=bpp):
                opened=self.is_opened()
                self.close()
                if opened:
                    self.open()
        return True
    def _get_board_info(self, kind):
        ids={   "width":BufferAcquisition.InquireParams.XSize,
                "height":BufferAcquisition.InquireParams.YSize,
                "bpp":BufferAcquisition.InquireParams.BitsPerPix,
                "bypp":BufferAcquisition.InquireParams.BytesPerPix,}
        return self._acq.GetBoardInfo(ids.get(kind,kind))
    def get_device_info(self):
        """
        Get camera model data.

        Return tuple ``(idx, model, idreg)`` with the board index, model number and the setting of the ID switch on the board
        """
        model=self._acq.GetBoardInfo(BufferAcquisition.InquireParams.Model)
        idreg=self._acq.GetBoardInfo(BufferAcquisition.InquireParams.IDReg)
        return TDeviceInfo(self.bitflow_idx,model,idreg)

    def _get_grabber_data_dimensions_rc(self, split=True):
        h,w=self._get_board_info("height"),self._get_board_info("width")
        return (h//self._frame_merge,w) if split else (h,w)
    def _get_data_dimensions_rc(self):
        return self._get_grabber_data_dimensions_rc()
    def get_detector_size(self):
        r,c=self._max_detector_size
        return c,r
    get_grabber_detector_size=get_detector_size
    def get_roi(self):
        h,w=self._get_grabber_data_dimensions_rc()
        return 0,w,0,h
    get_grabber_roi=get_roi
    @camera.acqcleared
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None):
        h,w=self._max_detector_size
        hend=w if hend is None else min(w,hend)
        vend=h if vend is None else min(h,vend)
        self._change_board_parameters(size=(hend,vend))
        return self.get_roi()
    set_grabber_roi=set_roi
    def get_roi_limits(self, hbin=1, vbin=1):
        w,h=self._max_detector_size
        wmin,hmin=(w,h) if self._camed is None else (1,1)
        hlim=camera.TAxisROILimit(wmin,w,1,1,1)
        vlim=camera.TAxisROILimit(hmin,h,1,1,1)
        return hlim,vlim
    get_grabber_roi_limits=get_roi_limits


    class BufferManager:
        """Buffer manager: stores, constantly reads and re-schedules buffers, keeps track of acquired frames and buffer overflow events"""
        def __init__(self, cam):
            self.stop_requested=False
            self.counter=0
            self.cam=cam
            self._buffer_loop_thread=None
        def reset(self):
            """Reset counter (on frame acquisition)"""
            self.counter=0
        def _acq_loop(self):
            while not self.stop_requested:
                try:
                    self.cam._acq.WaitForFrame(1)
                    self.counter+=self.cam._frame_merge
                except RuntimeError:
                    pass
        def start_loop(self):
            """Start buffer scheduling loop"""
            self.stop_loop()
            self.reset()
            self.stop_requested=False
            self._buffer_loop_thread=threading.Thread(target=self._acq_loop,daemon=True)
            self._buffer_loop_thread.start()
        def stop_loop(self):
            """Stop buffer scheduling loop"""
            if self._buffer_loop_thread is not None:
                self.stop_requested=True
                self._buffer_loop_thread.join()
                self._buffer_loop_thread=None
        def is_running(self):
            """Check if the buffer loop is running"""
            return self._buffer_loop_thread is not None
        def get_status(self):
            """Get counter status: tuple ``(acquired,)``"""
            return (self.counter,)
    
    def _get_number_of_buffer(self):
        return self._acq.GetNumberOfBuffers()*self._frame_merge
    @camera.acqcleared
    def _set_frame_merge(self, frame_merge):
        roi=self.get_grabber_roi()
        self._frame_merge=max(frame_merge,self._max_frame_merge) if self._max_frame_merge else frame_merge
        self.set_grabber_roi(*roi)
    @interface.use_parameters(mode="acq_mode")
    def setup_acquisition(self, mode="sequence", nframes=100, frame_merge=1):  # pylint: disable=arguments-differ
        """
        Setup acquisition mode.

        `mode` can be either ``"snap"`` (single frame or a fixed number of frames) or ``"sequence"`` (continuous acquisition).
        `nframes` sets up number of frames in the acquisition buffer.
        `frame_merge` specifies the number of frames to merge together to from one buffer; if it is larger than 1,
        several camera frames will be merged into a single frame grabber "super-frame" for acquisition, to lower the effective frame rate
        (which is capped at 2-4kFPS due to the necessity of Python loops). This is done transparently for the user, so the only visible change
        is the fact that the number of acquired frames is always updated in quanta of ``frame_merge``.
        """
        self.clear_acquisition()
        self._set_frame_merge(frame_merge)
        nframes=max(nframes,2*self._frame_merge)
        nframes=(((nframes-1)//self._frame_merge)+1)*self._frame_merge
        super().setup_acquisition(mode=mode,nframes=nframes,frame_merge=frame_merge)
        self._acq.BufferSetup(nframes//self._frame_merge)
        self._acq.AqSetup(BufferAcquisition.SetupOptions.DisableAqErrorSig)
    def clear_acquisition(self):
        """Clear all acquisition details and free all buffers"""
        if self._acq_params:
            self.stop_acquisition()
            try:
                self._acq.AqCleanup()
            except RuntimeError:
                pass
            self._acq.BufferCleanup()
            super().clear_acquisition()
    def start_acquisition(self, *args, **kwargs):
        self.stop_acquisition()
        super().start_acquisition(*args,**kwargs)
        self._acq.AqControl(BufferAcquisition.AcqCommands.Start,BufferAcquisition.AcqControlOptions.Wait)
        self._frame_counter.reset(self._get_number_of_buffer())
        self._buffer_mgr.start_loop()
    def stop_acquisition(self):
        if self.acquisition_in_progress():
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
            try:
                self._acq.AqControl(BufferAcquisition.AcqCommands.Stop,BufferAcquisition.AcqControlOptions.Wait)
            except RuntimeError:
                pass
        self._buffer_mgr.stop_loop()
    def acquisition_in_progress(self):
        stat=self._acq.GetAcqStatus()
        return bool(stat.Start and not stat.Stop)


    
    def _get_acquired_frames(self):
        if not self._buffer_mgr.is_running():
            return None
        return self._buffer_mgr.get_status()[0]
    def _wait_for_next_frame(self, timeout=20., idx=None):
        super()._wait_for_next_frame(timeout,idx=idx)

    
    def _get_buffer_bypp(self):
        return self._get_board_info("bypp")
    def _get_buffer_ctype(self):
        bypp=self._get_buffer_bypp()
        if bypp<=1:
            return ctypes.c_uint8
        if bypp<=2:
            return ctypes.c_uint16
        if bypp<=4:
            return ctypes.c_uint32
        if bypp<=8:
            return ctypes.c_uint64
        raise BitFlowError("could not find data type for {} bytes per pixel".format(bypp))
    _support_chunks=True
    def _get_buffer(self, idx, dim, ctype, n=1):
        bidx,sidx=idx//self._frame_merge,idx%self._frame_merge
        buff=self._acq.GetBuffer(bidx).ctypes.data
        framebytes=ctypes.sizeof(ctype)*dim[0]*dim[1]
        return np.ctypeslib.as_array(ctypes.cast(buff+framebytes*sidx,ctypes.POINTER(ctype)),shape=(n,)+dim).copy()
    def _range_to_chunks(self, rng, sz):
        s,e=rng
        chunks=[(p,sz) for p in range((s//sz)*sz,e,sz)]
        if s%sz:
            c=chunks[0]
            chunks[0]=(c[0]+s%sz,c[1]-s%sz)
        if e%sz:
            c=chunks[-1]
            chunks[-1]=(c[0],(e-1)%sz+1)
        return chunks
    def _read_frames(self, rng, return_info=False):
        dim=self._get_grabber_data_dimensions_rc()
        ctype=self._get_buffer_ctype()
        nbuff=self._get_number_of_buffer()
        chunks=self._range_to_chunks(rng,self._frame_merge)
        parsed_frames=[self._convert_indexing(self._get_buffer(p%nbuff,dim=dim,ctype=ctype,n=n),"rct",axes=(-2,-1)) for p,n in chunks]
        return parsed_frames,None





class BitFlowCamera(BitFlowFrameGrabber):
    """
    Generic BitFlow camera interface.

    Args:
        idx: board index, starting from 0
    """
    def __init__(self, idx=0, camfile=None):
        super().__init__(bitflow_idx=idx,bitflow_camfile=camfile)





class CameraFileEditor:
    """
    Camera file editor based on XML ElementTree parser.
    
    Provides methods for loading and saving the tree, and to change basic parameters in the default operational mode.
    """
    def __init__(self):
        self.tree=None
    def load(self, path, clean=True):
        """Load file from the given path and optionally check the structure remove the non-default modes"""
        self.tree=ET.parse(path)
        if clean:
            self.clean_modes()
    def save(self, path):
        """Save file to the given path"""
        if self.tree is not None:
            self.tree.write(path)
    def _check_node(self, node, tag=None, attrib=None, nchildren=None, children_tags=None):
        if tag is not None and node.tag!=tag:
            raise ValueError("expected tag {}, got {}".format(tag,node.tag))
        if attrib is not None and node.attrib!=attrib:
            raise ValueError("expected attrib {}, got {}".format(attrib,node.attrib))
        if nchildren is not None and len(node)!=nchildren:
            raise ValueError("expected {} children, got {}".format(nchildren,len(node)))
        if children_tags is not None and {ch.tag for ch in node}!=set(children_tags):
            raise ValueError("expected children tags {}, got {}".format(children_tags,{ch.tag for ch in node}))
    def clean_modes(self):
        """Check the loaded tree structure and remove non-default operational modes"""
        if self.tree is None:
            return
        node=self.tree.getroot()
        self._check_node(node,tag="bitflow_config",nchildren=1)
        node=node[0]
        self._check_node(node,tag="camera",nchildren=2,children_tags={"features","modes"})
        node=node.find("modes")
        for ch in list(node):
            if ch.attrib.get("name")!="Default":
                node.remove(ch)
        if len(node)==0:
            raise ValueError("could not find default configuration")
        if len(node)>1:
            raise ValueError("multiple default configurations")
    def _get_subnode_text(self, node, subnode, asint=False):
        if not node.findall(subnode):
            return None
        text=node.find(subnode).text
        return int(text) if asint else text
    def get_mode_parameters(self):
        """
        Get default operational mode parameters.
        
        Return tuple ``(size, fmt, bpp)`` with the acquisition size ``(xsize, ysize)``, format (e.g., ``"1X2-1Y"``) and the number of bits per pixel.
        If the tree is not loaded or mode is not present, return ``None``.
        """
        if self.tree is None:
            return None
        node=self.tree.find("camera/modes/mode")
        if not node.findall("mode_roi"):
            return None
        node=node.find("mode_roi")
        xsize=self._get_subnode_text(node,"xsize",asint=True)
        ysize=self._get_subnode_text(node,"ysize",asint=True)
        fmt=self._get_subnode_text(node,"format")
        bpp=self._get_subnode_text(node,"bitdepth",asint=True)
        return (xsize,ysize),fmt,bpp
    def _set_subnode_text(self, node, subnode, text):
        if not node.findall(subnode):
            node.append(ET.Element(subnode))
        node=node.find(subnode)
        changed=node.text!=text
        node.text=text
        return changed
    def set_mode_parameters(self, size=None, fmt=None, bpp=None):
        """
        Get default operational mode parameters.

        `size` is the acquisition size ``(xsize, ysize)``, `fmt` is the tap format (e.g., ``"1X2-1Y"``), and `bpp` is the number of bits per pixel.
        Parameters set to ``None`` stay unchanged.
        Return ``True`` if any parameters have changed their values and ``False`` otherwise.
        """
        if self.tree is None:
            return
        node=self.tree.find("camera/modes/mode")
        if not node.findall("mode_roi"):
            node.append(ET.Element("mode_roi"))
        node=node.find("mode_roi")
        changed=False
        if size is not None:
            changed=self._set_subnode_text(node,"xsize",str(size[0])) or changed
            changed=self._set_subnode_text(node,"ysize",str(size[1])) or changed
        if fmt is not None:
            changed=self._set_subnode_text(node,"format",str(fmt)) or changed
        if bpp is not None:
            changed=self._set_subnode_text(node,"bitdepth",str(bpp)) or changed
        return changed