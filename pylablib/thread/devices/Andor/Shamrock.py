from ... import device_thread
from ....core.thread import controller
from ...stream import stream_manager, stream_message

import numpy as np

class ShamrockSpectrographThread(device_thread.DeviceThread):
    """
    Shamrock spectrograph device thread.

    Device args:
        - ``idx``: spectrograph index (starting from 0)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``parameters``: basic changeable parameters: center wavelength, camera x-axis calibration, grating, etc.
        - ``full_info``: full device info: grating parameters, model number, etc.

    Commands:
        - ``set_grating``: select the grating
        - ``set_grating_offset``: set the grating offset
        - ``set_detector_offset``: set the detector offset
        - ``set_turret``: set the turret
        - ``set_wavelength``: set wavelength center
        - ``reset_wavelength``: reset wavelength center
        - ``goto_zero_order``: set grating to zero order
        - ``set_slit_width``: set slit width
        - ``reset_slit``: reset slit width
        - ``set_shutter``: set shutter mode
        - ``set_filter``: set filter
        - ``reset_filter``: reset filter
        - ``set_flipper_port``: set flipper ports
        - ``reset_flipper``: reset flipper ports
        - ``set_iris_width``: set input iris width
        - ``set_focus_mirror_position``: set focus mirror position
        - ``reset_focus_mirror``: reset focus mirror position
        - ``setup_calibration``: specify the pixel width and the number of pixels for the x-axis calibration
        - ``setup_camera``: set the corresponding Andor camera, whose frames are used to generate spectra
    """
    def connect_device(self):
        with self.using_devclass("Andor.ShamrockSpectrograph",host=self.remote) as cls:
            self.device=cls(idx=self.idx)  # pylint: disable=not-callable
    def setup_task(self, idx, remote=None):  # pylint: disable=arguments-differ
        self.idx=idx
        self.remote=remote
        self.cam_thread=None
        self.cam_thread_sid=None
        self.spec_tag_out=None
        self.setup_info()
        self.update_measurements(set_default=True)
        self.add_job("update_measurements",self.update_measurements,0.5)
        self.update_parameters(set_default=True)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_device_command("set_grating",post_update="update_parameters")
        self.add_device_command("set_grating_offset",post_update="update_parameters")
        self.add_device_command("set_detector_offset",post_update="update_parameters")
        self.add_device_command("set_turret",post_update="update_parameters")
        self.add_device_command("set_wavelength",post_update="update_parameters")
        self.add_device_command("reset_wavelength",post_update="update_parameters")
        self.add_device_command("goto_zero_order",post_update="update_parameters")
        self.add_device_command("set_slit_width",post_update="update_parameters")
        self.add_device_command("reset_slit",post_update="update_parameters")
        self.add_device_command("set_shutter",post_update="update_parameters")
        self.add_device_command("set_filter",post_update="update_parameters")
        self.add_device_command("reset_filter",post_update="update_parameters")
        self.add_device_command("set_flipper_port",post_update="update_parameters")
        self.add_device_command("reset_flipper",post_update="update_parameters")
        self.add_device_command("set_iris_width",post_update="update_parameters")
        self.add_device_command("set_focus_mirror_position",post_update="update_parameters")
        self.add_device_command("reset_focus_mirror",post_update="update_parameters")
        self.add_command("setup_calibration")
        self.add_command("setup_camera")
        self.setup_calibration()
        self.v["camera_thread"]=None
    def setup_camera(self, cam_thread=None, tag_in="frames/new", tag_out="spectra/new"):
        if self.cam_thread is not None:
            self.unsubscribe(self.cam_thread_sid)
            self.cam_thread_sid=None
        self.v["camera_thread"]=cam_thread
        self.cam_thread=cam_thread
        if self.cam_thread is not None:
            self.spec_tag_out=tag_out
            self.cam_thread_sid=self.subscribe_commsync(self._on_new_frames,srcs=self.cam_thread,tags=tag_in)
            self.msg_src=stream_manager.StreamSource(builder=stream_message.FramesMessage,sn=self.name)
            cam=controller.sync_controller(cam_thread)
            pixel_size=cam.dcsi.get_pixel_size()
            det_size=cam.dcsi.get_detector_size()
            if pixel_size and det_size:
                self.setup_calibration(number_pixels=det_size[0],pixel_width=pixel_size[0])
    def _on_new_frames(self, src, tag, msg):  # pylint: disable=unused-argument
        self.msg_src.receive_message(msg)
        cal=self.v["parameters/calibration"]
        frames,indices,_=msg.get_slice(flatten=True)
        metainfo={k:msg.metainfo[k] for k in ["tag","creation_time","step","roi"] if k in msg.metainfo}
        rows=[f[0] for f in frames]
        if not rows:
            return
        roi=metainfo.get("roi",None)
        if roi is not None and cal is not None:
            cal=cal[roi[0]:roi[1]]
            if len(roi)>4:
                hbin=roi[4]
                cal=cal[hbin//2::hbin]
        if cal is None or len(rows[0])!=len(cal):
            cal=np.arange(len(rows[0]))
        specs=[np.column_stack((cal,r)) for r in rows]
        self.send_multicast(dst="any",tag=self.spec_tag_out,value=self.msg_src.build_message(frames=specs,indices=indices,source=self.name,metainfo=metainfo))
    def setup_info(self):
        default_info={"device_info":None,"optical_parameters":None,"grating_infos":[],
                      "wavelength_present":False,"wavelength_limits":[],
                      "slits_present":[False]*4,"irises_present":[False]*2,
                      "focus_mirror_present":False,"focus_mirror_max":0,
                      "shutter_present":False,"filter_present":False,"flippers_present":[False]*2}
        self.v["full_info"]=default_info
        if self.open():
            self.set_variable("full_info",self.device.get_full_info(default_info),update=True)
    def update_parameters(self, set_default=False):  # pylint: disable=arguments-differ
        default_parameters={"zero_order":0,"slit_widths":[None]*4,"iris_widths":[None]*2,
                            "focus_mirror":0,"shutter_mode":None,"filter":0,"flipper_ports":[None]*2}
        if set_default:
            self.set_variable("parameters",default_parameters,update=True)
        if self.open():
            self.set_variable("parameters",self.device.get_full_info(default_parameters),update=True)
        elif not set_default:
            self.set_variable("parameters",default_parameters,update=True)
    def update_measurements(self, set_default=False):
        default_parameters={"grating":0,"wavelength":0,"calibration":None}
        if set_default:
            self.set_variable("parameters",default_parameters,update=True)
        if self.open():
            parameters=self.device.get_full_info(default_parameters)
            self.set_variable("parameters",parameters,update=True)
        elif not set_default:
            self.set_variable("parameters",default_parameters,update=True)
    
    def setup_calibration(self, number_pixels=None, pixel_width=None):
        if self.open():
            if number_pixels is not None:
                self.device.set_number_pixels(number_pixels)
            if pixel_width is not None:
                self.device.set_pixel_width(pixel_width)
            self.update_parameters()