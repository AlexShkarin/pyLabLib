from .NewClassic_USBCamera_SDK_lib import wlib as lib
from .base import MightexError, MightexTimeoutError

from ...core.utils import py3, ctypes_tools
from ...core.devio import interface
from ..interface import camera
from ..utils import load_lib

import numpy as np
import numba as nb
import collections
import ctypes
import time


TCameraInfo=collections.namedtuple("TCameraInfo",["idx","model","serial"])
class LibraryController(load_lib.LibraryController):
    def __init__(self, lib):  # pylint: disable=redefined-outer-name
        super().__init__(lib)
        self.ncams=None
        self.cams=None
    def _do_init(self):
        self.ncams=self.lib.NewClassicUSB_InitDevice()
        self.cams=[]
        for i in range(self.ncams):
            model,serial=self.lib.NewClassicUSB_GetModuleNoSerialNo(i+1)
            self.cams.append(TCameraInfo(i+1,py3.as_str(model).strip(),py3.as_str(serial).strip()))
    def _do_uninit(self):
        self.lib.NewClassicUSB_UnInitDevice()
        self.ncams=None
        self.cams=None
libctl=LibraryController(lib)
def restart_lib():
    libctl.shutdown()




def list_cameras():
    """List all cameras available through Mightex S-series interface"""
    with libctl.temp_open():
        return list(libctl.cams)
def get_cameras_number():
    """Get number of connected Mightex S-series cameras"""
    return len(list_cameras())





TDeviceInfo=collections.namedtuple("TDeviceInfo",["model","serial"])
class MightexSSeriesCamera(camera.IBinROICamera, camera.IExposureCamera):
    """
    Generic Mightex S Series camera interface.

    Args:
        idx: camera index among the cameras listed using :func:`list_cameras`, starting with 1
    """
    Error=MightexError
    TimeoutError=MightexTimeoutError
    def __init__(self, idx=1):
        super().__init__()
        lib.initlib()
        self.idx=idx
        self._opid=None
        self._sensor_size=None
        self._roi=None
        self._buffer_mgr=None
        self._looper=self.ReceiveLooper()
        self.open()
        self._raw_readout_format=False
        self._add_info_variable("device_info",self.get_device_info)
        self._add_settings_variable("pixel_clock",self.get_pixel_clock,self.set_pixel_clock,ignore_error=(MightexError,))
        self._add_settings_variable("hblanking",self.get_hblanking,self.set_hblanking,ignore_error=(MightexError,))


    def _get_connection_parameters(self):
        return (self.idx,)
    def open(self):
        """Open connection to the camera"""
        if self.is_opened():
            return
        with libctl.temp_open():
            cams=list_cameras()
            if self.idx>len(cams):
                raise MightexError("camera index {} is not available ({} cameras exist)".format(self.idx,len(cams)))
            with self._close_on_error():
                lib.NewClassicUSB_AddDeviceToWorkingSet(self.idx)
                lib.NewClassicUSB_StartCameraEngine(0,8)
                self._opid=libctl.open().opid
                self._initialize_default_parameters()
    def close(self):
        """Close connection to the camera"""
        if self.is_opened():
            try:
                self.clear_acquisition()
            finally:
                try:
                    lib.NewClassicUSB_StopCameraEngine()
                    lib.NewClassicUSB_RemoveDeviceFromWorkingSet(self.idx)
                finally:
                    libctl.close(self._opid)
                    self._opid=None
    def is_opened(self):
        return self._opid is not None
    def _initialize_default_parameters(self):
        self._sensor_size=(w,h)=self._autodetect_dimensions()
        self._min_size=self._autodetect_dimensions(top=False)
        self._roi=(0,w,0,h,1,1)
        self.set_roi()
        self.set_pixel_clock("fast")
        self.set_hblanking("normal")
        self.set_exposure(1E-1)

    def get_device_info(self):
        """
        Get camera information.

        Return tuple ``(model, serial)``.
        """
        return TDeviceInfo(*libctl.cams[self.idx-1][1:])

    _dim_min=(4,4)
    _dim_max=(2**16,2**16)
    _dim_step=(4,4)
    _autodetect_dim_default=(64,64)
    def _autodetect_single_dim(self, dim, rmin, rmax, rstep, default, top=True):
        a,b=(default,rmax) if top else (rmin,default)
        while a+rstep<b:
            m=(a+b)//2
            m-=m%rstep
            try:
                args=[self.idx,default,default,0]
                args[dim+1]=m
                lib.NewClassicUSB_SetCustomizedResolution(*args)
                a,b=(m,b) if top else (a,m)
            except MightexError:
                a,b=(a,m) if top else (m,b)
        return a if top else b
    def _autodetect_dimensions(self, top=True):
        w=self._autodetect_single_dim(0,self._dim_min[0],self._dim_max[0],self._dim_step[0],self._autodetect_dim_default[1],top=top)
        h=self._autodetect_single_dim(1,self._dim_min[1],self._dim_max[1],self._dim_step[1],self._autodetect_dim_default[0],top=top)
        return w,h
    def _get_data_dimensions_rc(self):
        hstart,hend,vstart,vend,hbin=self._roi[:5]
        return (vend-vstart)//hbin,(hend-hstart)//hbin
    def get_detector_size(self):
        return self._sensor_size
    def get_roi(self):
        return tuple(self._roi)
    def _apply_roi(self):
        hstart,hend,vstart,vend,hbin=self._roi[:5]
        lib.NewClassicUSB_SetCustomizedResolution(self.idx,hend-hstart,vend-vstart,0 if hbin==1 else 1)
        lib.NewClassicUSB_SetXYStart(self.idx,hstart,vstart)
    @camera.acqcleared
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None, hbin=1, vbin=1):
        _old_roi=self._roi
        hlim,vlim=self.get_roi_limits(hbin)
        hstart,hend,hbin=self._truncate_roi_axis((hstart,hend,hbin),hlim)
        vstart,vend,_=self._truncate_roi_axis((vstart,vend,hbin),vlim)
        self._roi=(hstart,hend,vstart,vend,hbin,hbin)
        try:
            self._apply_roi()
        except MightexError:
            self._roi=_old_roi
            self._apply_roi()
        return self.get_roi()
    def get_roi_limits(self, hbin=1, vbin=1):
        hbin=2 if hbin>1 else 1
        w,h=self.get_detector_size()
        hlim=camera.TAxisROILimit(self._min_size[0]*hbin,w,self._dim_step[0]*hbin,self._dim_step[0]*hbin,2)
        vlim=camera.TAxisROILimit(self._min_size[1]*hbin,h,self._dim_step[1]*hbin,self._dim_step[1]*hbin,2)
        return hlim,vlim

    _exposure_range=(50E-6,750E-3)
    def get_exposure(self):
        return self._exposure
    def set_exposure(self, exposure):
        exposure=sorted((exposure,)+self._exposure_range)[1]
        iexp=max(np.round(exposure/50E-6),1)
        self._exposure=iexp*50E-6
        lib.NewClassicUSB_SetExposureTime(self.idx,iexp)
        return self.get_exposure()
    def get_frame_timings(self):
        return self._TAcqTimings(self.get_exposure(),self.get_exposure())

    _p_pixel_clock=interface.EnumParameterClass("pixel_clock",{"slow":0,"medium":1,"fast":2})
    @interface.use_parameters(_return="pixel_clock")
    def get_pixel_clock(self):
        """Get pixel clock speed (``"slow"``, ``"medium"``, or ``"fast"``)"""
        return self._pixel_clock
    @interface.use_parameters
    def set_pixel_clock(self, pixel_clock):
        """Set pixel clock speed (``"slow"``, ``"medium"``, or ``"fast"``)"""
        self._pixel_clock=pixel_clock
        lib.NewClassicUSB_SetSensorFrequency(self.idx,pixel_clock)
        return self.get_pixel_clock()

    _p_hblanking=interface.EnumParameterClass("hblanking",{"normal":0,"longer":1,"longest":2})
    @interface.use_parameters(_return="hblanking")
    def get_hblanking(self):
        """Get hblanking speed (``"normal"``, ``"longer"``, or ``"longest"``)"""
        return self._hblanking
    @interface.use_parameters
    def set_hblanking(self, hblanking):
        """Set hblanking speed (``"normal"``, ``"longer"``, or ``"longest"``)"""
        self._hblanking=hblanking
        lib.NewClassicUSB_SetHBlankingExtension(self.idx,hblanking)
        return self.get_hblanking()
    def send_software_trigger(self):
        """Send software trigger signal"""
        lib.NewClassicUSB_SoftTrigger(self.idx)

    
    class ReceiveLooper:
        def __init__(self):
            self.comm=np.zeros(3,dtype="u8")
            self.stat=np.zeros(2,dtype="u8")
            self.buffer=None
            self.nbuff=None
            self.size=None
            self._make_callbacks()
            self._cb=None
        def _make_callbacks(self):
            puint64=nb.types.CPointer(nb.uint64)
            memmove=ctypes.memmove
            @nb.cfunc(nb.types.void(nb.uint64,puint64,puint64),nopython=True)
            def callback_body(psrc, pcomm, pstat): # comm is 2-array [pdst, nbuff, size], stat is 2-array [working, nread]
                comm=nb.carray(pcomm,3)
                stat=nb.carray(pstat,2)
                stat[0]=1
                if comm[0]>0:
                    b=stat[1]%comm[1]
                    memmove(comm[0]+b*comm[2],psrc,comm[2])
                    stat[1]+=1
                else:
                    stat[1]=0
                stat[0]=0
            self._cb_body=callback_body
            _cb_body_ct=ctypes_tools.WINFUNCTYPE(None,ctypes.c_uint64,ctypes.c_uint64,ctypes.c_uint64)(callback_body.address)
            pcomm_=self.comm.ctypes.data
            pstat_=self.stat.ctypes.data
            @nb.cfunc(nb.types.void(nb.uint64,nb.uint64),nopython=True)
            def callback(_, data):
                _cb_body_ct(data,pcomm_,pstat_)
            self._cb_main=callback
        def enable_callback(self):
            """Register and enable the frame callback"""
            self.stat[1]=0
            if self.buffer is not None:
                self._cb=lib.register_frame_callback(self._cb_main.address,wrap=False)
                self.comm[0]=ctypes.addressof(self.buffer)
                self.comm[1]=self.nbuff
                self.comm[2]=self.size
            return self.buffer is not None
        def disable_callback(self):
            """Stop and deregister the frame callback"""
            lib.NewClassicUSB_InstallFrameHooker(0,0)
            self.comm[:]=0
            while self.stat[0]:
                time.sleep(1E-3)
            self._cb=None
        def is_looping(self):
            """Check if the loop is running"""
            return bool(self.comm[0])
        def get_status(self):
            """Get the current loop status, which is the tuple ``(acquired,)``"""
            return (int(self.stat[1]),)
        def allocate(self, nbuff, size):
            """Allocate given number of buffers of the given size"""
            self.buffer=ctypes.create_string_buffer(nbuff*size)
            self.nbuff=nbuff
            self.size=size
        def deallocate(self):
            """Deallocate the buffers"""
            self.disable_callback()
            self.buffer=None
            self.nbuff=None
            self.size=None

    def _allocate_buffers(self, nbuff):
        self._deallocate_buffers()
        shape=self._get_data_dimensions_rc()
        size=shape[0]*shape[1]
        self._looper.allocate(nbuff,size)
    def _deallocate_buffers(self):
        self._looper.deallocate()

    @interface.use_parameters(mode="acq_mode")
    def setup_acquisition(self, mode="sequence", nframes=100):  # pylint: disable=arguments-differ
        """
        Setup acquisition mode.

        `mode` can be either ``"snap"`` (single frame or a fixed number of frames) or ``"sequence"`` (continuous acquisition).
        `nframes` sets up number of frame buffers.
        """
        self.clear_acquisition()
        self._allocate_buffers(nbuff=nframes)
        super().setup_acquisition(mode=mode,nframes=nframes)
    def clear_acquisition(self):
        self.stop_acquisition()
        self._deallocate_buffers()
        super().clear_acquisition()
    def start_acquisition(self, *args, **kwargs):
        self.stop_acquisition()
        super().start_acquisition(*args,**kwargs)
        self._frame_counter.reset(self._acq_params["nframes"])
        self._looper.enable_callback()
        nframes=0x8888 if self._acq_params["mode"]=="sequence" else self._acq_params["nframes"]
        lib.NewClassicUSB_StartFrameGrab(nframes)
    def stop_acquisition(self):
        if self.acquisition_in_progress():
            lib.NewClassicUSB_StopFrameGrab()
            self._looper.disable_callback()
            self._frame_counter.update_acquired_frames(self._get_acquired_frames())
        super().stop_acquisition()
    def acquisition_in_progress(self):
        return self._looper.is_looping()
    def _get_acquired_frames(self):
        return self._looper.get_status()[0]

    _support_chunks=True
    def _read_frames(self, rng, return_info=False):
        shape=self._get_data_dimensions_rc()
        nbuff=self._looper.nbuff
        size=self._looper.size
        data=np.ctypeslib.as_array(ctypes.cast(self._looper.buffer,ctypes.POINTER(ctypes.c_ubyte)),shape=(nbuff,size))
        i0,i1=rng
        if (i1-1)//nbuff==i0//nbuff:
            chunks=[(i0,i1-i0)]
        else:
            cut=(i1//nbuff)*nbuff
            chunks=[(i0,cut-i0),(cut,i1-cut)]
        frames=[data[b%nbuff:b%nbuff+n,:].reshape((n,)+shape).copy() for b,n in chunks]
        return frames,None