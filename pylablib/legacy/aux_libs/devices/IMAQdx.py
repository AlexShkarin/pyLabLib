from ...core.utils import dictionary, py3, general
from ...core.devio import data_format, interface
from ...core.dataproc import image as image_utils

import numpy as np
import contextlib
import time
import collections


from . import IMAQdx_lib
lib=IMAQdx_lib.lib
try:
    lib.initlib()
except (ImportError, OSError):
    pass
IMAQdxError=IMAQdx_lib.IMAQdxGenericError

_depends_local=[".IMAQdx_lib","...core.devio.interface"]

class IMAQdxAttribute(object):
    """
    Object representing an IMAQdx camera parameter.

    Allows to query and set values and get additional information.
    Usually created automatically by an :class:`IMAQdxCamera` instance, but could be created manually.

    Attributes:
        name: attribute name
        display_name: attribute display name (short description name)
        tooltip: longer attribute description
        description: full attribute description (usually, same as `tooltip`)
        units: attribute units (if applicable)
        readable (bool): whether attribute is readable
        writable (bool): whether attribute is writable
        min (float or int): minimal attribute value (if applicable)
        max (float or int): maximal attribute value (if applicable)
        inc (float or int): minimal attribute increment value (if applicable)
        values: list of possible attribute values (if applicable)
    """
    def __init__(self, sid, name):
        object.__init__(self)
        self.sid=sid
        self.name=name
        self.display_name=py3.as_str(lib.IMAQdxGetAttributeDisplayName(sid,name))
        self.tooltip=py3.as_str(lib.IMAQdxGetAttributeTooltip(sid,name))
        self.description=py3.as_str(lib.IMAQdxGetAttributeDescription(sid,name))
        self.units=py3.as_str(lib.IMAQdxGetAttributeUnits(sid,name))
        self.readable=lib.IMAQdxIsAttributeReadable(sid,name)
        self.writable=lib.IMAQdxIsAttributeWritable(sid,name)
        self._attr_type=lib.IMAQdxGetAttributeType(sid,name)
        self.type=IMAQdx_lib.IMAQdxAttributeType_enum[self._attr_type]
        if self._attr_type in [0,1,2,5]:
            self.min=lib.IMAQdxGetAttributeMinimum(sid,name,self._attr_type)
            self.max=lib.IMAQdxGetAttributeMaximum(sid,name,self._attr_type)
            self.inc=lib.IMAQdxGetAttributeIncrement(sid,name,self._attr_type)
        else:
            self.min=self.max=self.inc=None
        if self._attr_type==4:
            self.values=lib.IMAQdxEnumerateAttributeValues(sid,name)
        else:
            self.values=None
    
    def update_minmax(self):
        """Update minimal and maximal attribute limits"""
        if self._attr_type in [0,1,2,5]:
            self.min=lib.IMAQdxGetAttributeMinimum(self.sid,self.name,self._attr_type)
            self.max=lib.IMAQdxGetAttributeMaximum(self.sid,self.name,self._attr_type)
            self.inc=lib.IMAQdxGetAttributeIncrement(self.sid,self.name,self._attr_type)
    def truncate_value(self, value):
        """Truncate value to lie within attribute limits"""
        self.update_minmax()
        if self._attr_type in [0,1,2,5]:
            if value<self.min:
                value=self.min
            elif value>self.max:
                value=self.max
            else:
                inc=self.inc
                if inc>0:
                    value=((value-self.min)//inc)*inc+self.min
        return value

    def get_value(self, enum_as_str=True):
        """
        Get attribute value.
        
        If ``enum_as_str==True``, return enum-style values as strings; otherwise, return corresponding integer values.
        """
        if not self.readable:
            raise IMAQdxError("Attribute {} is not readable".format(self.name))
        val=lib.IMAQdxGetAttribute(self.sid,self.name,self._attr_type)
        if self._attr_type==4 and enum_as_str:
            val=val.Name
        return val
    def set_value(self, value, truncate=True):
        """
        Get attribute value.
        
        If ``truncate==True``, automatically truncate value to lie within allowed range.
        """
        if not self.writable:
            raise IMAQdxError("Attribute {} is not writable".format(self.name))
        if truncate:
            value=self.truncate_value(value)
        return lib.IMAQdxSetAttribute(self.sid,self.name,value,None)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,self.name)




def list_cameras(connected=True):
    """List all cameras available through IMAQdx interface"""
    return lib.IMAQdxEnumerateCameras(connected)

class IMAQdxCamera(interface.IDevice):
    """
    Generic IMAQdx camera interface.

    Args:
        name: interface name (can be learned by :func:`list_cameras`; usually, but not always, starts with ``"cam"``)
        mode: connection mode; can be ``"controller"`` (full control) or ``"listener"`` (only reading)
        default_visibility: default attribute visibility when listing attributes;
            can be ``"simple"``, ``"intermediate"`` or ``"advanced"`` (higher mode exposes more attributes).
    """
    def __init__(self, name="cam0", mode="controller", default_visibility="simple"):
        interface.IDevice.__init__(self)
        self.init_done=False
        self.name=name
        self.mode=mode
        self.default_visibility=default_visibility
        self.sid=None
        self.open()
        self.image_indexing="rct"
        try:
            attrs=self.list_attributes()
            self.attributes=dictionary.Dictionary(dict([ (a.name.replace("::","/"),a) for a in attrs ]))
        except Exception:
            self.close()
            raise
        self.init_done=True
        self.acq_params=None
        self.frame_counter=0
        self.last_wait_frame=-1
        self.buffers_num=0
        self.post_open()
        self.v=dictionary.ItemAccessor(self.get_value,self.set_value)

        self._add_full_info_node("model_data",self.get_model_data)
        self._add_full_info_node("interface_name",lambda: self.name)
        self._add_status_node("attributes",self.get_all_attributes)
        self._add_status_node("buffer_size",lambda: self.buffers_num)
        self._add_status_node("data_dimensions",self.get_data_dimensions)
        self._add_full_info_node("detector_size",self.get_detector_size)
        self._add_settings_node("roi",self.get_roi,self.set_roi)
        self._add_status_node("roi_limits",self.get_roi_limits)
        self._add_status_node("last_frame",self._last_buffer)
        self._add_status_node("read_frames",lambda: self.frame_counter)

    def open(self, mode=None):
        """Open connection to the camera"""
        mode=self.mode if mode is None else mode
        mode=IMAQdx_lib.IMAQdxCameraControlMode_enum.get(mode,mode)
        self.sid=lib.IMAQdxOpenCamera(self.name,mode)
        self.post_open()
    def close(self):
        """Close connection to the camera"""
        if self.sid is not None:
            lib.IMAQdxCloseCamera(self.sid)
            self.sid=None
    def reset(self):
        """Reset connection to the camera"""
        self.close()
        lib.IMAQdxResetCamera(self.name,False)
        self.open()
    def is_opened(self):
        """Check if the device is connected"""
        return self.sid is not None

    def post_open(self):
        """Action to automatically call on opening"""
        pass

    # _builtin_attrs=["OffsetX","OffsetY","Width","Height","PixelFormat","PayloadSize"]
    _builtin_attrs=["OffsetX","OffsetY","Width","Height","PixelFormat","PayloadSize","StatusInformation::LastBufferNumber","AcquisitionAttributes::BitsPerPixel"]
    def list_attributes(self, root="", visibility=None, add_builtin=True):
        """
        List all attributes at a given root.

        Return list of :class:`IMAQdxAttribute` objects, which allow querying and settings values
        and getting additional information (description, limits, increment).
        """
        visibility=visibility or self.default_visibility
        visibility=IMAQdx_lib.IMAQdxAttributeVisibility_enum.get(visibility,visibility)
        root=root.replace("/","::")
        attrs=lib.IMAQdxEnumerateAttributes2(self.sid,root,visibility)
        attr_names=[a.Name for a in attrs]
        if add_builtin:
            builtin_attrs=[]
            for a in self._builtin_attrs:
                if a not in attr_names:
                    try:
                        lib.IMAQdxGetAttributeDisplayName(self.sid,a)
                        builtin_attrs.append(a)
                    except IMAQdxError:
                        pass
            attr_names+=builtin_attrs
        return [IMAQdxAttribute(self.sid,a) for a in attr_names]

    def get_value(self, name, default=None):
        """Get value of the attribute with a given name"""
        name=name.replace("::","/")
        if (default is not None) and (name not in self.attributes):
            return default
        if self.attributes.is_dictionary(self.attributes[name]):
            return self.get_all_attributes(root=name)
        v=self.attributes[name].get_value()
        if isinstance(v,py3.new_bytes):
            v=py3.as_str(v)
        return v
    def set_value(self, name, value, ignore_missing=False, truncate=True):
        """
        Set value of the attribute with a given name.
        
        If ``truncate==True``, truncate value to lie within attribute range.
        """
        name=name.replace("::","/")
        if (name in self.attributes) or (not ignore_missing):
            if self.attributes.is_dictionary(self.attributes[name]):
                self.set_all_attributes(value,root=name)
            else:
                self.attributes[name].set_value(value,truncate=truncate)

    def get_all_attributes(self, root="", as_dict=False):
        """
        Get values of all attributes with the given `root`.

        If ``as_dict==True``, return ``dict`` object; otherwise, return :class:`.Dictionary` object.
        """
        settings=self.attributes[root].copy().filter_self(lambda a: a.readable).map_self(lambda a: a.get_value())
        return settings.as_dict(style="flat") if as_dict else settings
    def set_all_attributes(self, settings, root="", truncate=True):
        """
        Set values of all attributes with the given `root`.
        
        If ``truncate==True``, truncate value to lie within attribute range.
        """
        settings=dictionary.as_dict(settings,style="flat",copy=False)
        for k in settings:
            if k in self.attributes[root] and self.attributes[root,k].writable:
                self.attributes[root,k].set_value(settings[k],truncate=truncate)

    ModelData=collections.namedtuple("ModelData",["vendor","model","serial_number","bus_type"])
    def get_model_data(self):
        """
        Get camera model data.

        Return tuple ``(vendor, model, serial_number, bus_type)``.
        """
        cam_info=self.v["CameraInformation"]
        return self.ModelData(cam_info["VendorName"],cam_info["ModelName"],(cam_info["SerialNumberHigh"],cam_info["SerialNumberLow"]),cam_info["BusType"])

    def _get_data_dimensions_rc(self):
        return self.v["Height"],self.v["Width"]
    def get_data_dimensions(self):
        """Get the current data dimension (taking ROI and binning into account)"""
        return image_utils.convert_shape_indexing(self._get_data_dimensions_rc(),"rc",self.image_indexing)
    def get_detector_size(self):
        """Get camera detector size (in pixels) as a tuple ``(width, height)``"""
        return self.attributes["Width"].max,self.attributes["Height"].max
    def get_roi(self):
        """
        Get current ROI.

        Return tuple ``(hstart, hend, vstart, vend)``.
        """
        ox=self.v.get("OffsetX",0)
        oy=self.v.get("OffsetY",0)
        w=self.v["Width"]
        h=self.v["Height"]
        return ox,ox+w,oy,oy+h
    def set_roi(self, hstart=0, hend=None, vstart=0, vend=None):
        """
        Setup camera ROI.

        By default, all non-supplied parameters take extreme values.
        """
        for a in ["Width","Height","OffsetX","OffsetY"]:
            if a not in self.attributes or not self.attributes[a].writable:
                return
        det_size=self.get_detector_size()
        if hend is None:
            hend=det_size[0]
        if vend is None:
            vend=det_size[1]
        with self.pausing_acquisition():
            self.v["Width"]=self.attributes["Width"].min
            self.v["Height"]=self.attributes["Height"].min
            self.v["OffsetX"]=hstart
            self.v["OffsetY"]=vstart
            self.v["Width"]=max(self.v["Width"],hend-hstart)
            self.v["Height"]=max(self.v["Height"],vend-vstart)
        return self.get_roi()
    def get_roi_limits(self):
        """
        Get the minimal and maximal ROI parameters.

        Return tuple ``(min_roi, max_roi)``, where each element is in turn 4-tuple describing the ROI.
        """
        params=["OffsetX","OffsetY","Width","Height"]
        minp=tuple([(self.attributes[p].min if p in self.attributes else 0) for p in params])
        maxp=tuple([(self.attributes[p].max if p in self.attributes else 0) for p in params])
        min_roi=(0,0)+minp[2:]
        max_roi=maxp
        return (min_roi,max_roi)
    

    def setup_acquisition(self, continuous, frames):
        """
        Setup acquisition mode.

        `continuous` determines whether acquisition runs continuously, or stops after the given number of frames
        (note that :meth:`.IMAQdxCamera.acquisition_in_progress` would still return ``True`` in this case, even though new frames are no longer acquired).
        `frames` sets up number of frame buffers.
        """
        lib.IMAQdxConfigureAcquisition(self.sid,continuous,frames)
        self.acq_params=(continuous,frames)
        self.buffers_num=frames
    def clear_acquisition(self):
        lib.IMAQdxUnconfigureAcquisition(self.sid)
        self.buffers_num=0
    def start_acquisition(self):
        if self.acq_params is None:
            self.setup_acquisition(True,100)
        lib.IMAQdxStartAcquisition(self.sid)
        self.frame_counter=0
        self.last_wait_frame=-1
    def stop_acquisition(self):
        lib.IMAQdxStopAcquisition(self.sid)
        self.frame_counter=0
        self.last_wait_frame=-1
    def acquisition_in_progress(self):
        """Check if acquisition is in progress"""
        return self.v["StatusInformation/AcqInProgress"]
    def refresh_acquisition(self, delay=0.005):
        """Stop and restart the acquisition, waiting `delay` seconds in between"""
        self.stop_acquisition()
        self.clear_acquisition()
        self.setup_acquisition(0,1)
        self.start_acquisition()
        time.sleep(delay)
        self.stop_acquisition()
        self.clear_acquisition()
    def _last_buffer(self):
        last_buffer=self.v["StatusInformation/LastBufferNumber"]
        return last_buffer if last_buffer<2**31 else -1
    
    @contextlib.contextmanager
    def pausing_acquisition(self):
        """
        Context manager which temporarily pauses acquisition during execution of ``with`` block.

        Useful for applying certain settings which can't be changed during the acquisition.
        """
        acq_params=self.acq_params
        acq_in_progress=self.acquisition_in_progress()
        try:
            self.stop_acquisition()
            self.clear_acquisition()
            yield
        finally:
            if acq_params:
                self.setup_acquisition(*acq_params)
            if acq_in_progress:
                self.start_acquisition()


    def get_new_images_range(self):
        """
        Get the range of the new images.
        
        Return tuple ``(first, last)`` with images range (inclusive).
        If no images are available, return ``None``.
        """
        newest_img=self._last_buffer()
        if not self.acquisition_in_progress() or newest_img<0:
            return None
        if self.frame_counter>newest_img:
            return None
        if self.buffer_valid(self.frame_counter):
            return (self.frame_counter,newest_img)
        if self.buffer_valid(newest_img-self.buffers_num+1) and not self.buffer_valid(newest_img-self.buffers_num):
            return (newest_img-self.buffers_num+1,newest_img)
        valid_buffer=self._get_oldest_valid_buffer(self.frame_counter,newest_img)
        return (valid_buffer,newest_img)
    def wait_for_frame(self, since="lastread", timeout=20., period=1E-3):
        """
        Wait for a new camera frame.

        `since` specifies what constitutes a new frame.
        Can be ``"lastread"`` (wait for a new frame after the last read frame),
        ``"lastwait"`` (wait for a new frame after last :meth:`wait_for_frame` call),
        or ``"now"`` (wait for a new frame acquired after this function call).
        If `timeout` is exceeded, raise :exc:`.IMAQdxGenericError`.
        `period` specifies camera polling period.
        """
        ctd=general.Countdown(timeout)
        last_call_frame=self._last_buffer()
        while not ctd.passed():
            last_frame=self._last_buffer()
            since_last_wait=last_frame-self.last_wait_frame
            self.last_wait_frame=last_frame
            if since=="lastread" and last_frame>=self.frame_counter:
                return
            if since=="now" and last_frame>last_call_frame:
                return
            if since=="lastwait" and since_last_wait>0:
                return
            tl=ctd.time_left()
            time.sleep(period if tl is None else min(period,tl))
        raise IMAQdxError()
        

    def read_data_raw(self, size_bytes, mode, buffer_num=0):
        """Return raw bytes string from the given buffer number"""
        mode=IMAQdx_lib.IMAQdxBufferNumberMode_enum.get(mode,mode)
        return lib.IMAQdxGetImageData(self.sid,size_bytes,mode,buffer_num)
    def buffer_valid(self, buffer_num):
        return self.read_data_raw(0,2,buffer_num=buffer_num)[1]==buffer_num
    def _get_oldest_valid_buffer(self, start, stop):
        if start>stop or not self.buffer_valid(stop):
            return None
        if self.buffer_valid(start):
            return start
        while start<stop-1:
            mid=(start+stop)//2
            start,stop=(start,mid) if self.buffer_valid(mid) else (mid,stop)
        return stop









class IMAQdxPhotonFocusCamera(IMAQdxCamera):
    """
    IMAQdx interface to a PhotonFocus camera.

    Args:
        name: interface name (can be learned by :func:`list_cameras`; usually, but not always, starts with ``"cam"``)
        mode: connection mode; can be ``"controller"`` (full control) or ``"listener"`` (only reading)
        default_visibility: default attribute visibility when listing attributes;
            can be ``"simple"``, ``"intermediate"`` or ``"advanced"`` (higher mode exposes more attributes).
        small_packet_size: if ``True``, automatically set up Ethernet packet size to 1500 bytes.
    """
    def __init__(self, name, mode="controller", default_visibility="simple", small_packet_size=True):
        self.small_packet_size=small_packet_size
        IMAQdxCamera.__init__(self,name,mode=mode,default_visibility=default_visibility)
        self._add_settings_node("exposure",self.get_exposure,self.set_exposure)
        # self._add_status_node("readout_time",self.get_readout_time)
        # self._add_status_node("acq_status",self.get_status)
    def post_open(self):
        if self.init_done and self.small_packet_size:
            self.set_value("AcquisitionAttributes/PacketSize",1500,ignore_missing=True)

    def get_exposure(self):
        """Get current exposure"""
        return self.v["CameraAttributes/AcquisitionControl/ExposureTime"]*1E-6
    def set_exposure(self, exposure):
        """Set current exposure"""
        with self.pausing_acquisition():
            self.v["CameraAttributes/AcquisitionControl/ExposureTime"]=exposure*1E6
        return self.get_exposure()

    def setup_acquisition(self, continuous, frames):
        """
        Setup acquisition mode.

        `continuous` determines whether acquisition runs continuously, or stops after the given number of frames
        (note that :meth:`IMAQdxCamera.acquisition_in_progress` would still return ``True`` in this case, even though new frames are no longer acquired).
        `frames` sets up number of frame buffers.
        """
        IMAQdxCamera.setup_acquisition(self,continuous,frames)
        if continuous:
            self.buffers_num=frames//2 # seems to be the case


    def _get_bpp(self):
        pform=self.v["PixelFormat"]
        if pform.startswith("Mono"):
            pform=pform[4:]
            if pform.endswith("Packed"):
                raise IMAQdxError("packed pixel format isn't currently supported: {}".format("Mono"+pform))
            try:
                return (int(pform)-1)//8+1
            except ValueError:
                pass
        raise IMAQdxError("unrecognized pixel format: {}".format(pform))
    def _bytes_to_frame(self, raw_data):
        dim=self._get_data_dimensions_rc()
        bpp=self._get_bpp()
        dtype=data_format.DataFormat(bpp,"i","<")
        img=np.fromstring(raw_data,dtype=dtype.to_desc("numpy")).reshape((dim[0],dim[1]))
        return image_utils.convert_image_indexing(img,"rct",self.image_indexing)
    def peek_frame(self, mode="last", buffer_num=0):
        """
        Read a frame without marking it as read

        `mode` specifies frame selection mode: can be ``"first"`` (first available), ``"last"`` (last read),
        or ``"number"`` (index determined by `buffer_num`).

        Return tuple ``(frame, buffer_num)``.
        """
        raw_data,buffer_num=self.read_data_raw(self.v["PayloadSize"],mode=mode,buffer_num=buffer_num)
        return self._bytes_to_frame(raw_data),buffer_num
    def read_multiple_images(self, rng=None, peek=False, skip=False, missing_frame="skip"):
        """
        Read multiple images specified by `rng` (by default, all un-read images).

        If ``peek==True``, return images but not mark them as read.
        If ``skip==True``, mark frames as read but don't read them (i.e., reading with ``peek==True`` and ``skip==True`` does nothing).
        `missing_frame` determines what to do with frames which are out of range (missing or lost):
        can be ``"none"`` (replacing them with ``None``), ``"zero"`` (replacing them with zero-filled frame),
        or ``"skip"`` (skipping them).
        """
        new_range=self.get_new_images_range()
        if rng is None:
            rng=new_range
            missing_frame="skip"
        elif new_range:
            rng=rng[0],min(rng[1],new_range[1]) if isinstance(rng,(tuple,list)) else new_range[1]-rng,new_range[1]
        else:
            rng=None
        frames=None if skip else []
        if rng is None:
            return frames
        if not skip:
            frame_bytes=self.v["PayloadSize"]
            dim=self.get_data_dimensions()
            for i in range(rng[0],rng[1]+1):
                raw_data,buffer_num=self.read_data_raw(frame_bytes,mode="number",buffer_num=i)
                frame=self._bytes_to_frame(raw_data)
                if buffer_num==i:
                    frames.append(frame)
                elif missing_frame=="none":
                    frames.append(None)
                elif missing_frame=="zero":
                    frames.append(np.zeros(dim))
        if not peek:
            self.frame_counter=max(self.frame_counter,rng[1]+1)
        if missing_frame!="none":
            frames=np.asarray(frames)
        return frames

    def snap(self, timeout=20.):
        """Snap a single image (with preset image read mode parameters)"""
        self.refresh_acquisition()
        self.setup_acquisition(False,1)
        self.start_acquisition()
        self.wait_for_frame(timeout=timeout)
        frame=self.read_multiple_images()[0]
        self.stop_acquisition()
        self.clear_acquisition()
        return frame